"""
VIDEO DÀI 16:9 (YouTube / Facebook) kể chuyện bằng ảnh + chuyển cảnh, giọng Gemini Sadaltager.

Kịch bản: trường "long" trong scripts/<mã>.json
  "long": {
    "title": "Tiêu đề YouTube (≤ 95 ký tự)",
    "title_card": "Tiêu đề hiện trên màn hình (có thể **tô màu**)",
    "description": "Đoạn mô tả đầu cho YouTube",
    "voice": "Sadaltager",                       (không có thì lấy config long.voice)
    "chapters": [
      {"title": "", "beats": [...]},             chương đầu không có tiêu đề = đoạn mở đầu gây tò mò
      {"title": "Thành phố đói khát", "beats": [
         {"text": "lời kể (2–4 câu)", "ai": "mô tả ảnh tiếng Anh cho FLUX", "label": "Strasbourg · 1518"},
         {"text": "...", "image": {"url": "...", "credit": "..."}}     ảnh tư liệu (như video ngắn)
      ]}
    ]
  }

  python long_video.py scripts/SL1.json      -> output/<mã>/<mã>_dai.mp4 (+ ảnh bìa, mô tả YouTube)
Lỗi giọng Gemini (hết lượt) -> dừng, không đổi giọng; lần chạy sau làm tiếp (âm thanh đã đọc được lưu lại).
"""
import array
import hashlib
import json
import math
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

import audio_fx
import make_video as mv
import motion

ROOT = Path(__file__).resolve().parent
TTS_CACHE = ROOT / "assets" / "tts_cache"
AI_CACHE = ROOT / "assets" / "ai_cache"
SR = mv.SR
FPS = 24
# ảnh FLUX là ảnh vuông, sẽ bị cắt trên/dưới cho vừa khung 16:9 -> dặn bố cục rộng, chủ thể ở giữa
WIDE_HINT = "wide cinematic composition, main subject centered with space above and below"
CARD_TITLE, CARD_CHAPTER, CARD_END = 3.0, 3.2, 6.0
GAP = 0.6   # nghỉ sau mỗi chương

LONG_STYLE = ("Native Vietnamese narrator (Northern accent, Hanoi) for a long-form history documentary on YouTube. "
              "Warm, deep, knowledgeable male storyteller with a hint of mystery; calm, unhurried, engaging; "
              "clear diction and natural Vietnamese tones; vary the pace, slow down before surprising facts; "
              "leave a natural pause between paragraphs. Pronounce foreign names naturally. Never robotic.")

log = mv.log


def _fmt(sec):
    sec = int(sec)
    return f"{sec // 60:02d}:{sec % 60:02d}" if sec < 3600 else f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


# ------------------------------------------------------------------ giọng đọc
def chapter_audio(text, voice, work):
    """Đọc 1 chương bằng Gemini (có lưu tạm). Trả về mẫu âm 24 kHz."""
    import gemini_tts
    TTS_CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(f"{voice}|{LONG_STYLE}|{text}".encode()).hexdigest()[:16]
    wav = TTS_CACHE / f"{key}.wav"
    if not wav.exists():
        t = time.time()
        raw = gemini_tts.synth(text, LONG_STYLE, voice, log=log)
        tmp = work / f"{key}_raw.wav"
        tmp.write_bytes(raw)
        mv.run_ffmpeg(["-i", str(tmp), "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", str(wav)])
        log(f"     🎙️  Gemini đọc xong 1 chương ({time.time() - t:.0f}s)")
    return mv.read_wav(wav)


def split_by_pauses(samples, weights):
    """Chia âm thanh 1 chương thành các đoạn theo khoảng lặng gần nhất với tỉ lệ độ dài chữ."""
    x = np.frombuffer(samples.tobytes(), np.int16).astype(np.float32)
    win = int(0.02 * SR)
    k = len(x) // win
    rms = np.sqrt((x[:k * win].reshape(k, win) ** 2).mean(1) + 1e-6)
    speech = rms[rms > np.percentile(rms, 40)]
    thr = max(150.0, 0.1 * float(np.median(speech)) if len(speech) else 150.0)
    quiet = rms < thr
    # cắt lặng đầu/cuối
    nz = np.where(~quiet)[0]
    a, b = (nz[0], nz[-1] + 1) if len(nz) else (0, k)
    runs, i = [], a
    while i < b:
        if quiet[i]:
            j = i
            while j < b and quiet[j]:
                j += 1
            if j - i >= 12:            # ≥ 0,24 giây
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


# ------------------------------------------------------------------ hình ảnh
def beat_images(script, beats, work):
    import ai_images
    import images
    from PIL import Image
    credits, used_ai = [], False
    scenes = script.get("scenes", [])
    for b in beats:   # "image": {"scene": n} -> dùng lại ảnh tư liệu của cảnh n trong video ngắn
        im = b.get("image")
        if isinstance(im, dict) and "scene" in im and not im.get("url"):
            n = int(im["scene"])
            src = scenes[n].get("image") if 0 <= n < len(scenes) else None
            if src:
                b["image"] = dict(src)
            else:
                b.pop("image")
    # mỗi ảnh tư liệu chỉ tải 1 lần, beat nào dùng lại cùng ảnh thì dùng chung
    uniq = {}
    for b in beats:
        if b.get("image"):
            k = json.dumps(b["image"], sort_keys=True, ensure_ascii=False)
            uniq.setdefault(k, {"image": b["image"]})
    if uniq:
        pseudo = {"topic": script.get("topic", ""), "scenes": list(uniq.values())}
        credits = images.fetch_scene_images(pseudo, work / "arch", log)
        for b in beats:
            if b.get("image"):
                src = uniq[json.dumps(b["image"], sort_keys=True, ensure_ascii=False)].get("image_src")
                if src:
                    b["image_src"] = src
        missing = [v["image"].get("url", "")[-70:] for v in uniq.values() if v["image"].get("url") and not v.get("image_src")]
        if missing:
            # ảnh tư liệu đã chọn mà tải không được: không dựng với ảnh thiếu (sẽ lặp ảnh cũ), báo lỗi để thử lại
            raise RuntimeError(f"không tải được {len(missing)} ảnh tư liệu (sẽ thử lại lần chạy sau): " + "; ".join(missing[:3]))
    AI_CACHE.mkdir(parents=True, exist_ok=True)
    import os
    quota_hit = 0
    only_kaggle = os.environ.get("AI_SOURCE", "").strip().lower() == "kaggle"
    pending = []   # [(beat, key)] chưa vẽ được trên Cloudflare
    # ẢNH MÔ PHỎNG (đoạn không có ảnh tư liệu): phong cách ảnh chụp cũ, không vẽ mặt người thật (không đóng nhãn lên ảnh)
    for b in beats:
        if b.get("mo_phong") and not b.get("image_src"):
            key = hashlib.sha1((ai_images.STYLE_PHOTO_ID + "|" + b["mo_phong"]).encode()).hexdigest()[:16]
            f = AI_CACHE / f"mp_{key}.jpg"
            try:
                ai_images.generate(b["mo_phong"] + ", " + WIDE_HINT, f, log=log, wide=True, style=ai_images.photo_style(b["mo_phong"]),
                                   cheap=True)
                ai_images.to_wide(f)   # ảnh cũ trong bộ nhớ đệm còn khung vuông
                b["image_src"] = f.resolve().as_uri()
                b["_ai"] = True
                b.setdefault("fit", False)
                used_ai = True
            except Exception as e:
                log(f"     ⚠️  không tạo được ảnh mô phỏng: {e}")
                raise RuntimeError(f"thiếu ảnh mô phỏng (sẽ thử lại lần chạy sau): {e}")
    for b in beats:
        if b.get("ai") and not b.get("image_src"):
            key = hashlib.sha1((ai_images.STYLE_ID + "|" + b["ai"]).encode()).hexdigest()[:16]
            cached = (AI_CACHE / f"{key}.jpg").exists()
            if (quota_hit or only_kaggle) and not cached:
                pending.append((b, key))
                continue
            try:
                f = ai_images.generate(b["ai"] + ", " + WIDE_HINT, AI_CACHE / f"{key}.jpg", log=log, wide=True)
                b["image_src"] = f.resolve().as_uri()
                b["_ai"] = True
                b.setdefault("fit", False)   # tranh AI: phủ kín khung 16:9
                used_ai = True
            except Exception as e:
                log(f"     ⚠️  không vẽ được ảnh: {e}")
                msg = str(e).lower()
                if any(k in msg for k in ("429", "neuron", "limit", "quota", "exceeded")):
                    quota_hit += 1
                    pending.append((b, key))
    if pending and os.environ.get("KAGGLE_KEY", "").strip():
        # Cloudflare hết lượt -> vẽ phần còn lại bằng đúng mô hình FLUX.2 klein 4B trên máy GPU miễn phí của Kaggle
        import kaggle_draw
        uniq = {}
        for b, key in pending:
            uniq.setdefault(key, f"{b['ai']}, {WIDE_HINT}, {ai_images.STYLE}")
        log(f"     ☁️  Cloudflare hết lượt / chọn Kaggle: vẽ {len(uniq)} tranh trên Kaggle")
        try:
            res = kaggle_draw.draw_batch([(k, p, 1344, 768) for k, p in uniq.items()], AI_CACHE, log=log, model="klein")
        except Exception as e:
            log(f"     ⚠️  Kaggle lỗi: {e}")
            res = {}
        left = []
        for b, key in pending:
            f = AI_CACHE / f"{key}.jpg"
            if f.exists():
                b["image_src"] = f.resolve().as_uri()
                b.setdefault("fit", False)
                used_ai = True
            else:
                left.append((b, key))
        pending = left
    quota_hit = len(pending)
    if quota_hit:
        # ảnh đã vẽ được vẫn lưu lại, lần chạy sau vẽ nốt
        raise RuntimeError(f"còn {quota_hit} ảnh AI chưa vẽ được (hết lượt Cloudflare, Kaggle cũng chưa vẽ được), sẽ thử lại lần chạy sau")
    prev, prev_fit, prev_ai = None, None, False
    for b in beats:
        if not b.get("image_src"):
            b["image_src"] = prev
            b["_ai"] = prev_ai
            if prev_fit is not None:
                b.setdefault("fit", prev_fit)
        prev = b.get("image_src") or prev
        prev_ai = bool(b.get("_ai"))
        if b.get("image_src") and "fit" not in b:
            try:
                w, h = Image.open(b["image_src"].replace("file://", "")).size
                b["fit"] = h > w * 0.95 or w < 1200
            except Exception:
                b["fit"] = False
        prev_fit = b.get("fit")
    return credits, used_ai


def check_images(script, beats, log, kind="dai"):
    """Kiểm tra mọi ảnh trước khi đọc giọng / dựng (đỡ tốn tiền nếu ảnh hỏng).
    Ảnh mô phỏng AI lỗi -> tự tạo lại (tối đa 2 lần). Ảnh tư liệu lỗi -> dừng, báo để đổi ảnh."""
    import os
    import ai_images
    import kiem_tra_anh
    groups = {}
    kiem_tra_anh.STORY = (script.get("long") or {}).get("title") or script.get("title", "")
    for k, b in enumerate(beats):
        src = b.get("image_src")
        if not src:
            continue
        spec = b.get("image") if isinstance(b.get("image"), dict) else {}
        g = groups.setdefault(src, {"src": src, "texts": [], "ai": bool(b.get("_ai")), "label": b.get("label", ""),
                                    "allow_soft": bool(spec.get("cho_phep_mo")), "beats": [], "title": (spec.get("credit") or (("ảnh mô phỏng: " + b["mo_phong"])
                                                                                  if b.get("mo_phong") else ""))[:220]})
        if not g["texts"] and k > 0:
            g["texts"].append("(câu trước, để hiểu ngữ cảnh) " + gemini_clean(beats[k - 1].get("text", "")))
        g["texts"].append(gemini_clean(b.get("text", "")))
        if k + 1 < len(beats) and beats[k + 1].get("image_src") in (None, src):
            g["texts"].append("(câu sau) " + gemini_clean(beats[k + 1].get("text", "")))
        g["beats"].append(b)
    items = list(groups.values())
    res = kiem_tra_anh.check(items, script["id"], kind, log)
    for attempt in range(2):
        redo = [it for it in items if it["ai"] and any(m == "loi" for m, _ in res.get(it["src"], []))]
        redo = [it for it in redo if it["beats"][0].get("mo_phong")]
        if not redo:
            break
        for it in redo:
            b = it["beats"][0]
            f = Path(it["src"].replace("file://", ""))
            log(f"     🔁 tạo lại ảnh mô phỏng lỗi: {f.name} (lần {attempt + 1})")
            f.unlink(missing_ok=True)
            ai_images.generate(b["mo_phong"] + ", " + WIDE_HINT + f", variation {attempt + 2}", f, log=log, wide=True,
                               style=ai_images.photo_style(b["mo_phong"]), cheap=True)
        res = kiem_tra_anh.check(items, script["id"], kind, log)
    bad = [it for it in items if any(m == "loi" for m, _ in res.get(it["src"], []))]
    if bad and os.environ.get("FV_IMG_STRICT", "1") not in ("0", "no"):
        lines = []
        for it in bad:
            lines.append(Path(it["src"]).name + ": " + "; ".join(t for m, t in res[it["src"]] if m == "loi"))
        raise RuntimeError("ảnh không đạt kiểm tra, chưa dựng (xem logs/anh_%s_%s_kiemtra.txt):\n  " % (script["id"], kind)
                           + "\n  ".join(lines))


def _subject(src, depth, box):
    """Điểm chủ thể (x, y theo tỉ lệ ảnh gốc) trong vùng box, theo bản đồ độ sâu.
    Không lấy "chỗ gần máy nhất" (thường là mặt đất ở đáy ảnh) mà lấy vật NHÔ LÊN so với nền cùng hàng:
    độ sâu trừ trung vị độ sâu của từng hàng (mặt đất / bầu trời thay đổi đều theo hàng nên bị trừ hết).
    Trả về điểm phía trên của vật (đầu người / đầu con vật) để khung cận không cắt mất đầu."""
    l, t, r, b = box
    if depth:
        try:
            import cv2
            d = cv2.imread(str(depth), cv2.IMREAD_GRAYSCALE)
            h, w = d.shape
            sub = d[int(t * h):max(int(t * h) + 2, int(b * h)), int(l * w):max(int(l * w) + 2, int(r * w))]
            sub = cv2.resize(sub, (160, max(2, round(160 * sub.shape[0] / sub.shape[1]))), interpolation=cv2.INTER_AREA)
            sub = sub.astype("float32")
            sal = np.clip(sub - np.median(sub, axis=1, keepdims=True), 0, None)
            sal = cv2.GaussianBlur(sal, (0, 0), 2)
            if float(sal.max()) > 18:
                thr = float(np.percentile(sal, 92))
                ys, xs = np.nonzero(sal >= max(thr, sal.max() * 0.35))
                if len(xs) > 15:
                    sh, sw = sal.shape
                    x = xs.mean() / sw
                    y = np.percentile(ys, 20) / sh          # phần trên của vật
                    return l + (r - l) * x, t + (b - t) * y
        except Exception:
            pass
    return (l + r) / 2, t + (b - t) * 0.4


def _box_at(size, cx, cy, frac, within):
    """Khung 16:9 (tỉ lệ ảnh gốc) rộng bằng frac khung 'within', tâm gần (cx, cy), nằm gọn trong 'within'."""
    W0, H0 = size
    l, t, r, b = within
    bw_px = (r - l) * W0 * frac
    bh_px = bw_px * 9 / 16
    if bh_px > (b - t) * H0:
        bh_px = (b - t) * H0
        bw_px = bh_px * 16 / 9
    bw, bh = bw_px / W0, bh_px / H0
    x0 = min(max(cx - bw / 2, l), r - bw)
    y0 = min(max(cy - bh * 0.4, t), b - bh)
    return [round(x0, 4), round(y0, 4), round(x0 + bw, 4), round(y0 + bh, 4)], bw_px


def split_shots(shots, shot_max=5.5, min_px=880, log=print):
    """Ảnh hiện quá lâu -> chia thành 2-3 khung: toàn cảnh -> cận cảnh chủ thể -> trung cảnh (cắt thẳng, máy quay
    đổi hướng), để hình thay đổi mỗi ~4-6 giây như phim tài liệu. Ảnh nhỏ thì cận ít hơn để không vỡ."""
    from PIL import Image
    out, n_new = [], 0
    for s in shots:
        k = min(3, math.ceil(s["dur"] / shot_max)) if s["dur"] > shot_max * 1.25 else 1
        if k < 2 or not s.get("src"):
            out.append(s)
            continue
        try:
            import long_render
            W0, H0 = Image.open(long_render._path(s["src"])).size
        except Exception:
            out.append(s)
            continue
        if s.get("fit"):
            # ảnh dọc / nhỏ: khung ngang lấy trọn bề rộng ảnh (phần quan trọng), cận hơn ở khung sau
            within = [0.0, 0.0, 1.0, 1.0]
        else:
            # vùng toàn cảnh đang hiện (phủ kín 16:9, cắt dọc ở 35% như make_plate)
            if W0 / H0 >= 16 / 9:
                w = H0 * 16 / 9 / W0
                within = [(1 - w) / 2, 0.0, (1 + w) / 2, 1.0]
            else:
                hh = W0 * 9 / 16 / H0
                within = [0.0, (1 - hh) * 0.35, 1.0, (1 - hh) * 0.35 + hh]
        cx, cy = _subject(s["src"], s.get("depth"), within)
        full_px = (within[2] - within[0]) * W0
        frac_close = max(0.55, min_px / full_px) if full_px else 1
        small = frac_close > 0.85 and not s.get("fit")
        if small:                  # ảnh nhỏ: chỉ cận nhẹ 1 khung (cận sâu sẽ vỡ)
            frac_close, k = 0.8, min(k, 2)
        boxes = []
        if s.get("fit"):
            b1, px1 = _box_at((W0, H0), cx, cy, 1.0, within)
            if px1 >= min_px:
                boxes.append(b1)
            b2, px2 = _box_at((W0, H0), cx, cy, max(0.62, min_px / W0), within)
            if px2 >= min_px * 0.9 and b2 != (boxes[0] if boxes else None):
                boxes.append(b2)
        else:
            boxes.append(_box_at((W0, H0), cx, cy, frac_close, within)[0])
            # trung cảnh: lệch sang phía còn lại của ảnh
            ox = (within[0] + within[2]) - cx
            boxes.append(_box_at((W0, H0), ox, cy, max(0.75, frac_close), within)[0])
        parts = [dict(s, crop=None)] + [dict(s, crop=b, fit=False, label="") for b in boxes]
        parts = parts[:k]
        if len(parts) < 2:
            out.append(s)
            continue
        n = len(parts)
        cuts = [s["start"] + s["dur"] * j / n for j in range(n + 1)]
        for j in range(1, n):     # cắt đúng đầu câu nếu có câu bắt đầu gần đó
            near = [b for b in s.get("beat_starts", []) if abs(b - cuts[j]) < 1.6 and cuts[j - 1] + 2.5 < b < cuts[j + 1] - 2.5]
            if near:
                cuts[j] = min(near, key=lambda b: abs(b - cuts[j]))
        for j, part in enumerate(parts):
            part["start"] = cuts[j]
            part["dur"] = cuts[j + 1] - cuts[j]
            part["cut_in"] = j > 0
            part["cut_out"] = j < len(parts) - 1
            out.append(part)
        n_new += len(parts) - 1
    log(f"  ✂️  Chia nhỏ cảnh dài: thêm {n_new} khung cận cảnh / trung cảnh ({len(out)} khung)")
    return out


TRANSITIONS = ["fade", "push", "whip", "fade", "flash", "zoom", "push", "whip"]


def assign_transitions(shots, on=True):
    """Kiểu chuyển cảnh vào mỗi khung: đầu chương (có nhãn "Phần ...") -> tối dần rồi sáng lại; còn lại luân phiên
    tan ảnh / đẩy ngang / lia nhanh (whip) / lóe sáng / zoom xuyên, không lặp liền nhau."""
    prev = ""
    for i, s in enumerate(shots):
        if not on or i == 0:
            s["tr"] = "fade"
        elif str(s.get("label", "")).startswith("Phần "):
            s["tr"] = "dip"
        else:
            k = int(hashlib.md5(f"{i}|{s.get('src')}".encode()).hexdigest(), 16) % len(TRANSITIONS)
            tr = TRANSITIONS[k]
            if tr == prev:
                tr = TRANSITIONS[(k + 1) % len(TRANSITIONS)]
            s["tr"] = tr
        prev = s["tr"]


def gemini_clean(t):
    try:
        import gemini_tts
        return gemini_tts.clean_text(t)[0]
    except Exception:
        return t


# ------------------------------------------------------------------ dựng
def build(script, cfg, out_dir):
    L = script["long"]
    lc = cfg.get("long", {})
    voice = L.get("voice") or lc.get("voice", "Sadaltager")
    work = out_dir / "_work_dai"
    work.mkdir(parents=True, exist_ok=True)
    chapters = L["chapters"]
    beats_all = [b for ch in chapters for b in ch["beats"]]

    log("  🖼️  Ảnh cho video dài")
    pending = None
    try:
        credits, used_ai = beat_images(script, beats_all, work)
    except RuntimeError as e:
        # thiếu ảnh AI: vẫn đọc giọng trước (lưu lại), lần sau chỉ còn phải vẽ nốt ảnh
        pending, credits, used_ai = e, [], True

    if pending is None:
        check_images(script, beats_all, log)

    log(f"  🎙️  Giọng Gemini {voice} ({len(chapters)} chương)")
    mcfg_auto = motion.settings(cfg).get("fx_auto", True)
    import gemini_tts
    narr = array.array("h")
    shots, cards, marks, spoken = [], [], [], []
    t = 0.0

    def add_silence(sec):
        nonlocal t
        narr.extend(mv.silence(sec))
        t += sec

    chapter_cards = lc.get("chapter_cards", False)
    for ci, ch in enumerate(chapters):
        chap_label = ""
        if ch.get("title"):
            num = sum(1 for c in chapters[:ci + 1] if c.get("title"))
            marks.append((t, ch["title"]))
            if chapter_cards:
                cards.append({"start": t, "dur": CARD_CHAPTER, "kicker": f"Phần {num}", "title": ch["title"]})
                add_silence(CARD_CHAPTER)
            else:
                # không chen thẻ chương che kín màn hình (làm đứt mạch kể): chỉ hiện nhãn nhỏ ở góc
                chap_label = f"Phần {num} · {ch['title']}"
        elif ci == 0:
            marks.append((0.0, "Mở đầu"))
        texts = [gemini_tts.clean_text(b["text"])[0] for b in ch["beats"]]
        audio = chapter_audio("\n\n".join(texts), voice, work)
        segs, (a, b) = split_by_pauses(audio, [max(10, len(x)) for x in texts])
        narr.extend(audio[a:b])
        for (s0, s1), beat in zip(segs, ch["beats"]):
            st, en = t + (s0 - a) / SR, t + (s1 - a) / SR
            spoken.append({"start": st, "speech_end": en, "text": beat.get("text", "")})
            if shots and beat.get("image_src") and shots[-1]["src"] == beat.get("image_src") \
                    and not beat.get("label") and not chap_label and abs(shots[-1]["start"] + shots[-1]["dur"] - st) < 1.5:
                # cùng một ảnh với đoạn trước: kéo dài cảnh cũ (máy quay lướt chậm liền mạch), không tan ảnh vào chính nó
                shots[-1]["dur"] = en - shots[-1]["start"]
                shots[-1].setdefault("beat_starts", []).append(st)   # chỗ cắt khung đẹp: đầu câu mới
                continue
            shots.append({"start": st, "dur": (s1 - s0) / SR, "src": beat.get("image_src"),
                          "fit": bool(beat.get("fit")), "label": beat.get("label", "") or chap_label,
                          "fx": motion.pick_fx(beat, auto=mcfg_auto), "ai": bool(beat.get("_ai"))})
            chap_label = ""      # nhãn chương chỉ hiện ở khung đầu của chương
        t += (b - a) / SR
        add_silence(GAP)
        if ci == 0 and len(chapters) > 1:
            cards.append({"start": t, "dur": CARD_TITLE, "kicker": cfg.get("channel", ""),
                          "title": L.get("title_card") or L["title"], "sub": cfg.get("catchphrase", "")})
            add_silence(CARD_TITLE)
    if pending:
        raise pending
    cards.append({"start": t, "dur": CARD_END, "kicker": "Cảm ơn bạn đã nghe chuyện", "title": cfg.get("catchphrase", ""),
                  "sub": f"Đăng ký {cfg.get('channel', '')} để mở trang sử tiếp theo"})
    add_silence(CARD_END)
    total = t
    # ảnh kéo dài lấp chỗ thẻ tiêu đề
    for i, s in enumerate(shots):
        nxt = shots[i + 1]["start"] if i + 1 < len(shots) else total
        s["dur"] = max(0.5, nxt - s["start"])
    mv.write_wav(work / "narration.wav", narr)
    # dữ liệu thời gian cho bước tự kiểm tra (review.py): đoạn nào nói gì, ảnh nào hiện lúc nào
    (work / "review_data.json").write_text(json.dumps({
        "total": total, "spoken": spoken, "cards": cards,
        "shots": [{"start": s["start"], "dur": s["dur"], "src": Path(str(s["src"])).name, "label": s.get("label", "")}
                  for s in shots]}, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"  ⏱️  Thời lượng {_fmt(total)} · {len(shots)} cảnh ảnh")

    # ---- khung hình: trình duyệt vẽ lớp tĩnh + ảnh bìa, Python ghép từng khung (nhanh, chạy nhiều nhân)
    import long_render
    from playwright.sync_api import sync_playwright
    vis = [s for s in shots if s["src"]]
    mcfg = motion.settings(cfg)
    if mcfg["parallax"]:
        log("  🌀 Bản đồ độ sâu cho hiệu ứng 3D (parallax)")
        depths = {}
        for s in vis:
            if s["src"] not in depths:
                depths[s["src"]] = motion.depth_map(s["src"], log=log)
            s["depth"] = str(depths[s["src"]]) if depths[s["src"]] else None
        log(f"     {sum(1 for v in depths.values() if v)}/{len(depths)} ảnh có độ sâu")
    if not mcfg["fx"]:
        for s in vis:
            s["fx"] = ""
    if lc.get("shot_max", 0):     # tắt mặc định (cận cảnh bằng zoom dễ giật, sai chủ thể); dùng thêm ảnh thay thế
        vis = split_shots(vis, float(lc["shot_max"]), log=log)
    assign_transitions(vis, lc.get("transitions", True))
    silent = work / "silent.mp4"
    with sync_playwright() as p:
        br = p.chromium.launch()
        page = br.new_page(viewport={"width": 1920, "height": 1080})
        page.goto((ROOT / "templates" / "long.html").as_uri())
        page.evaluate("() => document.fonts.ready")
        # ảnh bìa YouTube
        key = next((s["src"] for s in vis if not s["fit"]), vis[0]["src"])
        page.evaluate("a => window.thumb(a[0], a[1], a[2])", [key, cfg.get("channel", ""), L.get("title_card") or L["title"]])
        page.wait_for_timeout(300)
        page.screenshot(path=str(out_dir / f"{script['id']}_dai_thumbnail.jpg"), type="jpeg", quality=92)
        # ảnh bìa cho Facebook: chữ ở giữa (Facebook cắt lưới video thành khung dọc)
        page.goto((ROOT / "templates" / "long.html").as_uri())
        page.evaluate("() => document.fonts.ready")
        page.evaluate("a => window.thumb(a[0], a[1], a[2], 'center')",
                      [key, cfg.get("channel", ""), L.get("title_card") or L["title"]])
        page.wait_for_timeout(300)
        page.screenshot(path=str(out_dir / f"{script['id']}_dai_thumbnail_fb.jpg"), type="jpeg", quality=92)
        page.goto((ROOT / "templates" / "long.html").as_uri())
        page.evaluate("() => document.fonts.ready")
        layers = long_render.render_layers(page, cfg.get("channel", ""), [s["label"] for s in vis if s.get("label")],
                                           cards, work / "layers")
        br.close()
    long_render.render(vis, cards, layers, total, FPS, silent, mv.ffmpeg_exe(), work, log=log, motion_cfg=mcfg)
    try:
        long_render.review_sheet(vis, cards, layers, out_dir / f"{script['id']}_dai_review.jpg", motion_cfg=mcfg)
    except Exception as e:
        log(f"     (không tạo được ảnh duyệt: {e})")

    # ---- âm thanh: giọng + nhạc (tự hạ khi có giọng)
    import music
    track, mcredit = music.pick({"id": script["id"] + "-dai", "topic": script.get("topic", ""),
                                 "music": L.get("music") or script.get("music")}, log)
    final = out_dir / f"{script['id']}_dai.mp4"
    args = ["-i", str(silent), "-i", str(work / "narration.wav")]
    graph = [f"[1:a]{audio_fx.VOICE_CHAIN},aresample=44100,asplit=2[v][vk]"]
    if track:
        args += ["-stream_loop", "-1", "-i", str(track)]
        dk = cfg.get("music_duck", {})
        graph += [f"[2:a]loudnorm=I={cfg.get('music_lufs', -17)}:LRA=11:TP=-3,aresample=44100,afade=t=in:d=2,"
                  f"afade=t=out:st={max(0, total - 3):.2f}:d=3[mr]",
                  f"[mr][vk]sidechaincompress=threshold={dk.get('threshold', 0.06)}:ratio={dk.get('ratio', 3)}:attack=40:release=500[m]",
                  f"[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]"]
    else:
        graph += ["[vk]anullsink", "[v]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]"]
    mv.run_ffmpeg(args + ["-filter_complex", ";".join(graph), "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                          "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart",
                          str(final)])

    # ---- mô tả YouTube
    lines = [f"TIÊU ĐỀ YOUTUBE: {L['title'][:95]}", "", "MÔ TẢ:", L.get("description", script.get("caption", "")), "",
             "📌 Mục lục:"] + [f"{_fmt(s)} {name}" for s, name in marks] + [
             "", " ".join("#" + h.lstrip("#") for h in script.get("hashtags", [])), "",
             "📌 Video sử dụng giọng đọc AI" + (" và một số tranh minh họa tạo bằng AI." if used_ai else ".")]
    short = mv._short_credits(credits)
    if short:
        lines.append("📷 Ảnh tư liệu: " + "; ".join(short) + " · nguồn Wikimedia Commons")
    if mcredit:
        lines.append(f"🎵 Nhạc: {mcredit}")
    import binh_luan
    lines += binh_luan.lines(script, "dai")   # bình luận ghim + phụ của chủ kênh cho Facebook / YouTube
    lines += ["", "──── GHI CHÚ (không đăng) ────", "Nguồn kiểm chứng:"] + [f"- {s}" for s in script.get("sources", [])]
    try:
        en_note = subtitles_and_english(script, L, spoken, marks, credits, mcredit, used_ai, out_dir)
    except Exception as e:   # phụ đề / bản dịch lỗi không được làm hỏng video
        log(f"     ⚠️  phụ đề / bản tiếng Anh lỗi: {e}")
        en_note = []
    lines += en_note
    (out_dir / f"{script['id']}_dai_youtube.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"✅ Video dài: {final.name} ({_fmt(total)})")
    return final, total


def subtitles_and_english(script, L, spoken, marks, credits, mcredit, used_ai, out_dir):
    """Phụ đề tiếng Việt + tiếng Anh (.srt) và tiêu đề/mô tả tiếng Anh. Trả về vài dòng hướng dẫn để ghép vào file mô tả."""
    import subtitles
    sid = script["id"]
    spoken = [s for s in spoken if s.get("text")]
    segs = [(s["start"], s["speech_end"], s["text"]) for s in spoken]
    subtitles.write_srt(out_dir / f"{sid}_dai_vi.srt", subtitles.cues(segs))
    note = ["", "──── PHỤ ĐỀ ────",
            f"YouTube Studio → video → Phụ đề → Thêm ngôn ngữ → Tiếng Việt → Tải tệp lên → {sid}_dai_vi.srt"]
    payload = {"title": L["title"], "description": L.get("description", script.get("caption", "")),
               "chapters": [name for _, name in marks], "lines": [s["text"] for s in spoken]}
    en = subtitles.translate(payload, log)
    if not en:
        return note
    segs_en = [(a, b, t) for (a, b, _), t in zip(segs, en["lines"])]
    subtitles.write_srt(out_dir / f"{sid}.en_US.srt", subtitles.cues(segs_en))
    tags = " ".join("#" + h.lstrip("#").replace(" ", "") for h in en.get("hashtags", []))
    out = [f"TITLE: {en['title'][:95]}", "", "DESCRIPTION:", en["description"], "",
           "🇻🇳 Narrated in Vietnamese. Turn on English subtitles (CC).", "", "📌 Chapters:"]
    out += [f"{_fmt(t)} {name}" for (t, _), name in zip(marks, en["chapters"])]
    out += ["", tags, "",
            "📌 This video uses an AI voice" + (" and AI-generated illustrations (FLUX)." if used_ai else ".")]
    short = mv._short_credits(credits)
    if short:
        out.append("📷 Archival images: " + "; ".join(short) + " · via Wikimedia Commons")
    if mcredit:
        out.append(f"🎵 Music: {mcredit}")
    (out_dir / f"{sid}_dai_youtube_en.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    note += [f"Thêm tiếp ngôn ngữ Tiếng Anh: dán Tiêu đề + Mô tả trong file {sid}_dai_youtube_en.txt, "
             f"rồi tải phụ đề {sid}.en_US.srt (Facebook tự nhận tiếng Anh theo tên file)."]
    return note


def images_review(script, out_dir):
    """Chỉ chuẩn bị ảnh (ảnh tư liệu + vẽ tranh AI) và xuất bảng duyệt, chưa đọc giọng, chưa dựng video.
    logs: <id>_anh.jpg (lưới ảnh đánh số theo đoạn) + <id>_anh.txt (số, nguồn, lời đọc, prompt)."""
    from PIL import Image, ImageDraw, ImageFont
    work = out_dir / "_work_dai"
    work.mkdir(parents=True, exist_ok=True)
    beats = [b for ch in script["long"]["chapters"] for b in ch["beats"]]
    pending = None
    try:
        beat_images(script, beats, work)
    except RuntimeError as e:
        pending = e
    tw, th, cols = 384, 216, 6
    tiles, rows_txt = [], []
    font = ImageFont.load_default(size=18)
    for i, b in enumerate(beats):
        src = b.get("image_src")
        kind = "AI" if b.get("ai") else ("TL" if b.get("image") else "=")
        im = Image.new("RGB", (tw, th), (40, 0, 0))
        if src:
            try:
                im = Image.open(src.replace("file://", "")).convert("RGB")
                im.thumbnail((tw, th))
                bg = Image.new("RGB", (tw, th), (15, 15, 15))
                bg.paste(im, ((tw - im.width) // 2, (th - im.height) // 2))
                im = bg
            except Exception:
                pass
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 70, 26], fill=(0, 0, 0))
        d.text((5, 3), f"{i + 1} {kind}", fill=(255, 210, 120), font=font)
        tiles.append(im)
        rows_txt.append(f"{i + 1:>3} [{kind}] {b.get('text', '')[:140]}\n      → {b.get('ai') or (b.get('image') or {}).get('credit', '(dùng ảnh đoạn trước)')[:140]}")
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 4), rows * (th + 4)), (0, 0, 0))
    for k, im in enumerate(tiles):
        sheet.paste(im, ((k % cols) * (tw + 4), (k // cols) * (th + 4)))
    sheet.save(out_dir / f"{script['id']}_anh.jpg", quality=85)
    (out_dir / f"{script['id']}_anh.txt").write_text("\n".join(rows_txt) + "\n", encoding="utf-8")
    # bảng duyệt cỡ lớn: chỉ tranh AI, mỗi trang 6 tranh 800px để soi chi tiết (chân, đầu, nét mặt, chữ)
    big, seen = [], set()
    for i, b in enumerate(beats):
        src = b.get("image_src")
        if b.get("ai") and src and src not in seen:
            seen.add(src)
            big.append((i + 1, src))
    for old in out_dir.glob(f"{script['id']}_anh_lon_*.jpg"):
        old.unlink()
    font2 = ImageFont.load_default(size=30)
    for pg in range(0, len(big), 6):
        page = Image.new("RGB", (1608, 1380), (0, 0, 0))
        for k, (n, src) in enumerate(big[pg:pg + 6]):
            try:
                im = Image.open(src.replace("file://", "")).convert("RGB").resize((800, 457))
            except Exception:
                continue
            d = ImageDraw.Draw(im)
            d.rectangle([0, 0, 64, 40], fill=(0, 0, 0))
            d.text((8, 4), str(n), fill=(255, 210, 120), font=font2)
            page.paste(im, ((k % 2) * 808, (k // 2) * 461))
        page.save(out_dir / f"{script['id']}_anh_lon_{pg // 6 + 1}.jpg", quality=82)
    n_ai = sum(1 for b in beats if b.get("ai"))
    log(f"  🖼️  Bảng duyệt ảnh: {len(beats)} đoạn, {n_ai} tranh AI" + (f" · {pending}" if pending else ""))


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    cfg = mv.load_config()
    bad = 0
    only_images = "--images-only" in sys.argv
    for arg in [a for a in sys.argv[1:] if not a.startswith("--")]:
        script = json.loads(Path(arg).read_text(encoding="utf-8"))
        if not script.get("long"):
            continue
        out_dir = ROOT / "output" / script["id"]
        out_dir.mkdir(parents=True, exist_ok=True)
        log(f"▶️  Video dài {script['id']}: {script['long']['title']}")
        if only_images:
            images_review(script, out_dir)
            continue
        try:
            build(script, cfg, out_dir)
        except Exception as e:
            log(f"❌ Video dài {script['id']}: {e}")
            bad += 1
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
