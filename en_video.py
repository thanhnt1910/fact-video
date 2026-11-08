"""
VIDEO DÀI TIẾNG ANH (History Mysteries Daily): giọng Gemini Orus + ảnh tư liệu + phụ đề tiếng Anh.

  python en_video.py tai-anh  ke-hoach/roanoke/roanoke.json     tải ảnh đã chọn (anh_chon.json) về assets/anh_en/<mã>/
  python en_video.py giong    ke-hoach/roanoke/roanoke.json     đọc giọng từng cụm 8 đoạn, lưu assets/tts_cache
  python en_video.py dung     ke-hoach/roanoke/roanoke.json     ghép video 1080p + bản xem nhanh + phụ đề .srt

anh_chon.json (cạnh file kịch bản): {"S01": {"url": "...", "credit": "...", "ay": 0.5}, ...}
  ay = vị trí cắt dọc khi ảnh cao hơn khung (0 trên, 1 dưới). Ô không có ảnh thì dùng ảnh của ô gần nhất.
"""
import os

# Quy tắc giọng: khóa hết lượt thì đổi khóa khác; mọi khóa đều hết thì DỪNG, không đợi (chủ kênh 04/11/2026)
os.environ.setdefault("GEMINI_MAX_WAIT", "0")

import array
import hashlib
import json
import math
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

import demo_giong_en  # noqa: F401  (thay lời dặn tiếng Việt của gemini_tts bằng bản tiếng Anh)
import gemini_tts
import images
import make_video as mv

ROOT = Path(__file__).resolve().parent
SR = mv.SR
W, H, FPS = 1920, 1080, 25
CLUSTER = 8                 # số đoạn đọc một lượt (giữ hạn mức Gemini, chủ kênh chốt 24/10)
GAP_BEAT = 0.25             # nghỉ thêm giữa hai đoạn
INTRO, OUTRO = 3.0, 4.0
TTS_CACHE = ROOT / "assets" / "tts_cache"
LOGO = ROOT / "assets" / "logo" / "history-mysteries-daily.png"

STYLE = demo_giong_en.STYLE + (
    " Keep exactly the same voice, volume and pace from the first sentence to the last. "
    "Do not read stage directions. Read the capitalized word CROATOAN as 'kro-uh-TAN'.")


def log(*a):
    print(*a, flush=True)


# ------------------------------------------------------------------ dữ liệu
def load(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    d["_dir"] = Path(path).resolve().parent
    return d


def beats_of(d):
    out = []
    for ci, ch in enumerate(d["chapters"]):
        for b in ch["beats"]:
            out.append(dict(b, chapter=ci, ctitle=ch.get("title", "")))
    return out


def img_dir(d):
    p = ROOT / "assets" / "anh_en" / d["id"]
    p.mkdir(parents=True, exist_ok=True)
    return p


# ------------------------------------------------------------------ tải ảnh
def tai_anh(d):
    sel = json.loads((d["_dir"] / "anh_chon.json").read_text(encoding="utf-8"))
    out = img_dir(d)
    credits = {}
    for slot, info in sel.items():
        dest = out / f"{slot}.jpg"
        if dest.exists() and dest.stat().st_size > 5000:
            credits[slot] = info.get("credit", "")
            continue
        raw = out / f"{slot}_raw"
        try:
            images._download(info["url"], raw)
            im = Image.open(raw).convert("RGB")
            im.thumbnail((2600, 2600))
            im.save(dest, quality=92)
            credits[slot] = info.get("credit", "")
            log(f"  ✅ {slot} {im.size} {info.get('credit', '')[:70]}")
        except Exception as e:
            log(f"  ⚠️  {slot}: {e}")
        finally:
            raw.unlink(missing_ok=True)
    (out / "credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"Đã có {len(list(out.glob('S*.jpg')))} ảnh")


# ------------------------------------------------------------------ giọng
def split_by_pauses(samples, weights, minrun=12):
    x = np.frombuffer(samples.tobytes(), np.int16).astype(np.float32)
    win = int(0.02 * SR)
    k = len(x) // win
    rms = np.sqrt((x[:k * win].reshape(k, win) ** 2).mean(1) + 1e-6)
    speech = rms[rms > np.percentile(rms, 40)]
    thr = max(150.0, 0.1 * float(np.median(speech)) if len(speech) else 150.0)
    quiet = rms < thr
    nz = np.where(~quiet)[0]
    a, b = (nz[0], nz[-1] + 1) if len(nz) else (0, k)
    runs, i = [], a
    while i < b:
        if quiet[i]:
            j = i
            while j < b and quiet[j]:
                j += 1
            if j - i >= minrun:
                runs.append(((i + j) / 2, j - i))
            i = j
        else:
            i += 1
    total = b - a
    cum = np.cumsum(weights)[:-1] / sum(weights)
    cuts, last = [], a
    for c in cum:
        exp = a + c * total
        cands = [r for r in runs if r[0] > last + 25]
        if cands:
            best = min(cands, key=lambda r: abs(r[0] - exp) - 0.6 * r[1])
            pos = best[0] if abs(best[0] - exp) < 0.25 * total else exp
        else:
            pos = exp
        cuts.append(int(pos))
        last = pos
    bounds = [a] + cuts + [b]
    return [(bounds[n] * win, bounds[n + 1] * win) for n in range(len(bounds) - 1)], (a * win, b * win)


def clusters(bs):
    """Cụm tối đa 8 đoạn, chia đều trong từng chương, không vượt ranh giới chương."""
    by = {}
    for b in bs:
        by.setdefault(b["chapter"], []).append(b)
    out = []
    for ci in sorted(by):
        c = by[ci]
        k = math.ceil(len(c) / CLUSTER)
        size = math.ceil(len(c) / k)
        out += [c[i:i + size] for i in range(0, len(c), size)]
    return out


def cluster_audio(texts, voice, work, extra="", style_base="", take=0):
    # extra: hướng dẫn phát âm riêng của từng kịch bản (trường "style" trong json).
    # Để trống thì khóa bộ nhớ đệm giữ nguyên như cũ, nên giọng RN1 đã đọc không phải đọc lại.
    style = (style_base or STYLE) + extra
    text = "\n\n".join(texts)
    key = hashlib.sha1(f"{voice}|{style}|{text}".encode()).hexdigest()[:16]
    TTS_CACHE.mkdir(parents=True, exist_ok=True)
    wav = TTS_CACHE / f"en_{key}.wav"
    if take:      # đọc lại: ghi ra file riêng của lượt này, chưa thay bản đang giữ
        wav = TTS_CACHE / f"en_{key}_t{take}.wav"
        wav.unlink(missing_ok=True)
    if not wav.exists():
        t = time.time()
        raw = gemini_tts.synth(text, style, voice, log=log)
        tmp = work / f"{key}_{take}_raw.wav"
        tmp.write_bytes(raw)
        mv.run_ffmpeg(["-i", str(tmp), "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", str(wav)])
        log(f"   🎙️  đọc xong 1 cụm {len(texts)} đoạn ({time.time() - t:.0f}s)")
    return mv.read_wav(wav)


def style_base(d):
    f = d.get("style_file")
    return (ROOT / f).read_text(encoding="utf-8").strip() if f else ""


def beat_groups(d):
    """cum=1: mỗi đoạn lời kể đọc riêng một lượt gọi; mặc định gom cụm."""
    bs = beats_of(d)
    return [[b] for b in bs] if d.get("cum") == 1 else clusters(bs)


def speech_len(audio):
    x = np.frombuffer(audio.tobytes(), np.int16).astype(np.float32)
    win = int(0.02 * SR)
    k = len(x) // win
    if k < 2:
        return 0.0
    r = np.sqrt((x[:k * win].reshape(k, win) ** 2).mean(1) + 1e-6)
    nz = np.where(r > 0.1 * np.median(r[r > np.percentile(r, 40)]))[0]
    return (nz[-1] - nz[0] + 1) * win / SR if len(nz) else 0.0


def giong(d):
    work = ROOT / "output" / d["id"] / "_work"
    work.mkdir(parents=True, exist_ok=True)
    voice = d.get("voice", "Orus")
    sb = style_base(d)
    extra = d.get("style", "")
    cs = beat_groups(d)
    log(f"Giọng {voice}: {len(cs)} lượt gọi" + (" (mỗi đoạn một lượt)" if d.get("cum") == 1 else ""))

    def fail(i, e):
        log(f"⛔ DỪNG ở lượt {i + 1}/{len(cs)}: {str(e)[:300]}")
        log("   Mọi khóa Gemini đều hết lượt (hoặc lỗi giọng). Các đoạn đã đọc được giữ trong bộ nhớ đệm; chạy lại sau khi hạn mức hồi.")
        sys.exit(3)

    for i, c in enumerate(cs):
        try:
            cluster_audio([b["text"] for b in c], voice, work, extra, sb)
        except Exception as e:
            fail(i, e)
        log(f"  lượt {i + 1}/{len(cs)} ✔")
    if d.get("cum") != 1:
        return
    # Đọc lại đoạn nào Gemini đọc sai (nhịp lệch xa so với cả video, thường là bỏ câu hoặc đọc thừa):
    # tối đa 3 lượt mỗi đoạn, giữ bản có nhịp gần chuẩn nhất. Không chỉnh âm thanh.
    def info(i):
        c = cs[i]
        text = "\n\n".join(b["text"] for b in c)
        style = (sb or STYLE) + extra
        key = hashlib.sha1(f"{voice}|{style}|{text}".encode()).hexdigest()[:16]
        return key, len(text.split())
    rates = []
    for i in range(len(cs)):
        key, w = info(i)
        L = speech_len(mv.read_wav(TTS_CACHE / f"en_{key}.wav"))
        rates.append(w / L if L else 0)
    med = float(np.median([r for r in rates if r]))
    log(f"Nhịp chuẩn: {med:.2f} chữ/giây")
    for i, c in enumerate(cs):
        key, w = info(i)
        ok = TTS_CACHE / f"en_{key}.ok"
        dev = lambda r: abs(r / med - 1) if r else 9
        if ok.exists() or dev(rates[i]) <= 0.25:
            ok.write_text("ok")
            continue
        best, best_dev, best_take = rates[i], dev(rates[i]), 0
        log(f"  ⚠ đoạn {i + 1}: nhịp {rates[i]:.2f} lệch {best_dev * 100:.0f}%, đọc lại")
        for take in (1, 2):
            try:
                a = cluster_audio([b["text"] for b in c], voice, work, extra, sb, take)
            except Exception as e:
                fail(i, e)
            L = speech_len(a)
            r = w / L if L else 0
            log(f"     lượt {take}: nhịp {r:.2f} (lệch {dev(r) * 100:.0f}%)")
            if dev(r) < best_dev:
                best, best_dev, best_take = r, dev(r), take
            if best_dev <= 0.25:
                break
        if best_take:
            (TTS_CACHE / f"en_{key}.wav").write_bytes((TTS_CACHE / f"en_{key}_t{best_take}.wav").read_bytes())
        for t in (1, 2):
            (TTS_CACHE / f"en_{key}_t{t}.wav").unlink(missing_ok=True)
        ok.write_text("ok")
        log(f"     giữ lượt {best_take}, lệch {best_dev * 100:.0f}%")


def timeline(d):
    """Đọc (hoặc lấy từ cache) giọng, trả về (mẫu âm toàn bộ, danh sách đoạn có mốc thời gian)."""
    work = ROOT / "output" / d["id"] / "_work"
    work.mkdir(parents=True, exist_ok=True)
    voice = d.get("voice", "Orus")
    narr = array.array("h")
    narr.extend(mv.silence(INTRO))
    t = INTRO
    items = []
    groups = beat_groups(d)
    for gi, c in enumerate(groups):
        texts = [b["text"] for b in c]
        audio = cluster_audio(texts, voice, work, d.get("style", ""), style_base(d))
        segs, (a, b) = split_by_pauses(audio, [max(10, len(x)) for x in texts])
        for (s0, s1), beat in zip(segs, c):
            seg = audio[s0:s1]
            st = t + 0.0
            parts = split_caption(beat["text"])
            cue_cuts = []
            if len(parts) > 1 and len(seg) > SR:
                # mốc đổi dòng phụ đề bám theo chỗ ngắt thật của giọng, không chia theo số ký tự
                sub, _ = split_by_pauses(seg, [max(8, len(q)) for q in parts], minrun=6)
                cue_cuts = [sb[1] / SR for sb in sub[:-1]]
            narr.extend(seg)
            t += len(seg) / SR
            narr.extend(mv.silence(GAP_BEAT))
            t += GAP_BEAT
            items.append(dict(beat, start=st, end=st + len(seg) / SR, cue_cuts=cue_cuts))
        # nghỉ dài hơn khi sang chương
        if gi + 1 < len(groups) and groups[gi + 1][0]["chapter"] == c[0]["chapter"]:
            continue
        narr.extend(mv.silence(0.5))
        t += 0.5
    narr.extend(mv.silence(OUTRO))
    return narr, items, t + 0.0


WPS_UOC = 2.1              # nhịp giọng Orus đo ở RN1 (từ mỗi giây), dùng cho bản dựng không giọng


def timeline_uoc(d):
    """Mốc thời gian ước theo số từ (chưa có giọng): trả về (âm thanh im lặng, đoạn, tổng thời lượng)."""
    t = INTRO
    items = []
    for c in clusters(beats_of(d)):
        for b in c:
            dur = max(2.0, len(b["text"].split()) / WPS_UOC)
            items.append(dict(b, start=t, end=t + dur))
            t += dur + GAP_BEAT
        t += 0.5
    t += OUTRO
    narr = array.array("h")
    narr.extend(mv.silence(t))
    return narr, items, t


# ------------------------------------------------------------------ hình
def compose(src, dest, ay=0.5):
    """Khung 2560x1440: ảnh đặt trọn trong khung, nền là chính ảnh phóng to, làm mờ, tối."""
    cw, ch = 2560, 1440
    im = Image.open(src).convert("RGB")
    iw, ih = im.size
    bg = im.copy()
    s = max(cw / iw, ch / ih)
    bg = bg.resize((int(iw * s) + 1, int(ih * s) + 1), Image.LANCZOS)
    x0, y0 = (bg.width - cw) // 2, int((bg.height - ch) * ay)
    bg = bg.crop((x0, y0, x0 + cw, y0 + ch)).filter(ImageFilter.GaussianBlur(40))
    bg = ImageEnhance.Brightness(bg).enhance(0.45)
    ratio = iw / ih
    if abs(ratio - cw / ch) < 0.12:
        s2 = max(cw / iw, ch / ih)         # gần 16:9: phủ kín khung
        fg = im.resize((int(iw * s2) + 1, int(ih * s2) + 1), Image.LANCZOS)
        x0, y0 = (fg.width - cw) // 2, int((fg.height - ch) * ay)
        canvas = fg.crop((x0, y0, x0 + cw, y0 + ch))
    else:
        s2 = min(cw * 0.96 / iw, ch * 0.96 / ih)
        fg = im.resize((max(1, int(iw * s2)), max(1, int(ih * s2))), Image.LANCZOS)
        canvas = bg.copy()
        canvas.paste(fg, ((cw - fg.width) // 2, (ch - fg.height) // 2))
    # chỉnh màu nhẹ cho đồng bộ: hơi ấm, tối viền
    canvas = ImageEnhance.Color(canvas).enhance(0.9)
    canvas = ImageEnhance.Contrast(canvas).enhance(1.04)
    canvas.save(dest, quality=93)


def render_shot(args):
    """Zoom chậm + lia nhẹ, tính vị trí cắt theo điểm ảnh LẺ (PIL affine, nội suy bilinear) rồi đẩy khung thô vào ffmpeg.
    Không dùng zoompan của ffmpeg: nó làm tròn vị trí cắt theo số nguyên nên ảnh bị rung khi chuyển động chậm."""
    png, out, dur, kind = args[:4]
    fi, fo = (args[4], args[5]) if len(args) > 5 else (True, True)   # cảnh dài chia đôi: không mờ đen ở chỗ nối
    n = max(2, int(round(dur * FPS)))
    z0, z1 = (1.0, 1.1) if kind % 2 == 0 else (1.1, 1.0)
    sw, sh = int(W * 1.1), int(H * 1.1)          # nguồn đủ lớn: zoom 1.1 vẫn không phải phóng to ảnh
    src = Image.open(png).convert("RGB").resize((sw, sh), Image.LANCZOS)
    fade = min(0.4, dur / 4)
    fades = ([f"fade=t=in:st=0:d={fade:.2f}"] if fi else []) + \
            ([f"fade=t=out:st={max(0, dur - fade):.2f}:d={fade:.2f}"] if fo else [])
    vf = ",".join(fades + ["format=yuv420p"])
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", str(FPS), str(out)]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for i in range(n):
            t = i / (n - 1)
            e = t * t * (3 - 2 * t)              # vào ra mềm, không giật đầu và cuối
            z = z0 + (z1 - z0) * e
            cw, ch = sw / z, sh / z
            fx = {0: 0.5, 1: e, 2: 0.5, 3: 1 - e}[kind % 4]
            fy = {0: 0.5, 1: 0.5, 2: e, 3: 0.5}[kind % 4]
            x0, y0 = (sw - cw) * fx, (sh - ch) * fy
            fr = src.transform((W, H), Image.AFFINE, (cw / W, 0, x0, 0, ch / H, y0), resample=Image.BILINEAR)
            pr.stdin.write(fr.tobytes())
        pr.stdin.close()
        if pr.wait() != 0:
            raise RuntimeError(f"ffmpeg lỗi khi dựng {out}")
    finally:
        if pr.poll() is None:
            pr.kill()
    return out


def render_job(job):
    if job[0] == "map":
        import ban_do_en
        _, spec, out, dur = job
        return ban_do_en.render_map_shot(spec, out, dur, fps=FPS)
    return render_shot(job)


def _num(k):
    import re
    m = re.search(r"\d+", k)
    return int(m.group()) if m else 0


def slot_images(d, slots):
    """Ảnh cho từng ô: ảnh AI (assets/anh_en/<mã>/ai/<ô>.jpg) nếu có, không thì ảnh tư liệu; ô thiếu dùng ô gần nhất."""
    folder = img_dir(d)
    have = {p.stem: p for p in folder.glob("S*.jpg")}
    for p in (folder / "ai").glob("S*.jpg"):
        have[p.stem] = p          # ảnh AI thay ảnh tư liệu cùng ô (hoặc làm ô mới như S29B)
    names = sorted(slots)
    res, miss = {}, []
    for s in names:
        if s in have:
            res[s] = have[s]
        else:
            miss.append(s)
    for s in miss:
        near = sorted(have, key=lambda k: abs(_num(k) - _num(s)))
        if not near:
            raise SystemExit("Chưa có ảnh nào: chạy tai-anh trước")
        res[s] = have[near[0]]
    return res, miss


# ------------------------------------------------------------------ phụ đề
def ts(sec):
    h, r = divmod(max(0, sec), 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def split_caption(text, maxc=100):
    """Tách đoạn thành các cụm ≤ 2 dòng, theo câu."""
    import re
    sent = re.split(r"(?<=[.!?])\s+", text.strip())
    parts, cur = [], ""
    for s in sent:
        if cur and len(cur) + 1 + len(s) > maxc:
            parts.append(cur)
            cur = s
        else:
            cur = (cur + " " + s).strip()
    if cur:
        parts.append(cur)
    out = []
    for p in parts:      # câu quá dài thì cắt ở dấu phẩy gần giữa
        while len(p) > maxc * 1.25 and "," in p:
            i = p.rfind(",", 0, int(maxc * 1.1))
            if i < 20:
                break
            out.append(p[:i + 1].strip())
            p = p[i + 1:].strip()
        out.append(p)
    return out


def wrap2(t, per=52):
    if len(t) <= per:
        return t
    mid = len(t) // 2
    i = t.rfind(" ", 0, mid + 8)
    j = t.find(" ", mid)
    k = i if i > 10 and (j < 0 or mid - i <= j - mid) else j
    if k < 0:
        return t
    return t[:k] + "\\N" + t[k + 1:]


def write_subs(items, total, d, out_ass, out_srt):
    ev, srt, n = [], [], 0
    for it in items:
        parts = split_caption(it["text"])
        wt = [max(8, len(p)) for p in parts]
        dur = it["end"] - it["start"]
        t0 = it["start"]
        cc = it.get("cue_cuts") or []
        for q, (p, w) in enumerate(zip(parts, wt)):
            if len(cc) == len(parts) - 1:
                t1 = it["start"] + cc[q] if q < len(cc) else it["end"]
            else:
                t1 = t0 + dur * w / sum(wt)
            n += 1
            ev.append(f"Dialogue: 0,{ts(t0)},{ts(t1 - 0.03)},Main,,0,0,0,,{wrap2(p)}")
            h1, m1 = divmod(t0, 3600)
            srt.append(f"{n}\n{_srt(t0)} --> {_srt(t1 - 0.03)}\n{p}\n")
            t0 = t1
    title = d.get("title_card", "THE LOST COLONY OF ROANOKE")
    sub = d.get("subtitle_card", "History Mysteries Daily")
    ev.append(f"Dialogue: 1,{ts(0.4)},{ts(INTRO - 0.2)},Title,,0,0,0,,{{\\fad(500,500)}}{title}")
    ev.append(f"Dialogue: 1,{ts(0.9)},{ts(INTRO - 0.2)},Sub,,0,0,0,,{{\\fad(500,500)}}{sub}")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,DejaVu Sans,46,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.2,1.2,2,120,120,64,1
Style: Title,DejaVu Serif,84,&H004BA9D8,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,4,2,5,100,100,0,1
Style: Sub,DejaVu Sans,40,&H00F2E9D3,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,6,0,1,3,1,5,100,100,-170,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    out_ass.write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    out_srt.write_text("\n".join(srt), encoding="utf-8")


def _srt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# ------------------------------------------------------------------ dựng
def dung_thu(d):
    """Dựng bản không giọng (thời lượng ước theo số từ) để duyệt hình, bản đồ và nhịp cảnh."""
    dung(d, co_giong=False)


def dung(d, co_giong=True):
    out_dir = ROOT / "output" / d["id"]
    work = out_dir / ("_work" if co_giong else "_work_thu")
    work.mkdir(parents=True, exist_ok=True)
    if co_giong:
        narr, items, total = timeline(d)
        log(f"Giọng xong: {total / 60:.1f} phút, {len(items)} đoạn")
    else:
        narr, items, total = timeline_uoc(d)
        log(f"Bản KHÔNG GIỌNG: thời lượng ước {total / 60:.1f} phút, {len(items)} đoạn")

    # ghép đoạn cùng ô ảnh liên tiếp thành một cảnh
    # câu có trường "map" (khai báo trong ban_do.json cạnh kịch bản) dùng cảnh bản đồ động thay cho ảnh
    mapp = d["_dir"] / "ban_do.json"
    maps = json.loads(mapp.read_text(encoding="utf-8")) if mapp.exists() else {}
    shots = []
    for it in items:
        key = it.get("map") if it.get("map") in maps else it["slot"]
        if shots and shots[-1]["slot"] == key:
            shots[-1]["end"] = it["end"]
        else:
            shots.append({"slot": key, "start": it["start"], "end": it["end"], "chapter": it["chapter"]})
    shots[0]["start"] = 0.0
    for a, b in zip(shots, shots[1:]):
        a["end"] = b["start"]
    shots[-1]["end"] = total
    paths, miss = slot_images(d, {s["slot"] for s in shots if s["slot"] not in maps})
    if miss:
        log(f"⚠️  Ô chưa có ảnh (dùng ảnh gần nhất): {', '.join(miss)}")
    sel = {}
    selp = d["_dir"] / "anh_chon.json"
    if selp.exists():
        sel = json.loads(selp.read_text(encoding="utf-8"))

    # tách cảnh quá dài (> 14 giây) để hình có lúc đổi khung
    jobs, listing = [], []
    for k, s in enumerate(shots):
        dur = s["end"] - s["start"]
        if s["slot"] in maps:
            out = work / f"shot_{k:03d}_map.mp4"
            jobs.append(("map", maps[s["slot"]], out, dur))
            listing.append(out)
            continue
        nsub = max(1, int(math.ceil(dur / 13.0)))
        for j in range(nsub):
            png = work / f"{s['slot']}.png"
            if not png.exists():
                compose(paths[s["slot"]], png, sel.get(s["slot"], {}).get("ay", 0.5))
            out = work / f"shot_{k:03d}_{j}.mp4"
            jobs.append((png, out, dur / nsub, k + j, j == 0, j == nsub - 1))
            listing.append(out)
    log(f"{len(shots)} cảnh, {len(jobs)} đoạn hình")
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=3) as ex:
        for i, _ in enumerate(ex.map(render_job, jobs)):
            if i % 10 == 0:
                log(f"   … {i + 1}/{len(jobs)} ({time.time() - t0:.0f}s)")
    lst = work / "list.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in listing), encoding="utf-8")
    silent = work / "silent.mp4"
    mv.run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(silent)])

    # âm thanh: giọng chuẩn hóa một mức
    raw = work / "voice.wav"
    mv.write_wav(raw, narr)
    voice = work / "voice_norm.wav"
    if co_giong and not d.get("giong_goc"):
        mv.run_ffmpeg(["-i", str(raw), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", str(voice)])
    elif co_giong:
        # "giong_goc": true trong json: giữ nguyên giọng Gemini, không cân âm lượng hay chỉnh tốc độ
        log("Giọng gốc: không cân âm lượng, không chỉnh tốc độ")
        mv.run_ffmpeg(["-i", str(raw), "-ar", "44100", str(voice)])
    else:
        mv.run_ffmpeg(["-i", str(raw), "-ar", "44100", str(voice)])

    ass, srt = out_dir / f"{d['id']}.en.ass", out_dir / f"{d['id']}.en.srt"
    write_subs(items, total, d, ass, srt)
    final = out_dir / f"{d['id']}_{'dai' if co_giong else 'thu'}.mp4"
    # logo kênh: vuông 130 px, độ đậm 0,8, góc trên bên phải, cách mép phải 44 px và mép trên 34 px (giống video bản đồ)
    fc = (f"[0:v]ass='{ass.as_posix()}'[v];[2:v]scale=130:130,format=rgba,colorchannelmixer=aa=0.8[lg];"
          f"[v][lg]overlay=W-w-44:34[o]")
    mv.run_ffmpeg(["-i", str(silent), "-i", str(voice), "-i", str(LOGO), "-filter_complex", fc, "-map", "[o]", "-map", "1:a",
                   "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-b:a", "160k", "-shortest",
                   "-movflags", "+faststart", str(final)])
    prev = out_dir / f"{d['id']}_{'' if co_giong else 'thu_'}xem_nhanh.mp4"
    mv.run_ffmpeg(["-i", str(final), "-vf", "scale=854:-2", "-c:v", "libx264", "-preset", "veryfast", "-crf", "30",
                   "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", str(prev)])
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", str(final)], text=True).strip())
    log(f"✅ {final.name}: {dur / 60:.2f} phút, {final.stat().st_size / 1e6:.0f} MB; bản xem nhanh {prev.stat().st_size / 1e6:.0f} MB")
    km = out_dir / "khung_mau"
    km.mkdir(exist_ok=True)
    for k, s in enumerate(shots):
        if s["slot"] in maps or k % 6 == 0:
            tmid = s["start"] + (s["end"] - s["start"]) * (0.8 if s["slot"] in maps else 0.5)
            mv.run_ffmpeg(["-ss", f"{tmid:.2f}", "-i", str(final), "-frames:v", "1", "-vf", "scale=960:-2",
                           "-q:v", "4", str(km / f"{k:03d}_{s['slot']}.jpg")])
    (out_dir / "bao_cao.json").write_text(json.dumps(
        {"phut": round(dur / 60, 2), "so_doan": len(items), "so_canh": len(shots), "o_thieu_anh": miss,
         "mb": round(final.stat().st_size / 1e6)}, ensure_ascii=False, indent=1), encoding="utf-8")
    # mốc chương cho phần mô tả YouTube
    lines, seen = [], set()
    for it in items:
        if it["ctitle"] and it["chapter"] not in seen:
            seen.add(it["chapter"])
            m, s = divmod(int(it["start"]), 60)
            lines.append(f"{m:02d}:{s:02d} {it['ctitle']}")
    (out_dir / "chuong.txt").write_text("00:00 Intro\n" + "\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    cmd, path = sys.argv[1], sys.argv[2]
    d = load(path)
    {"tai-anh": tai_anh, "giong": giong, "dung": dung, "dung-thu": dung_thu}[cmd](d)
