"""
VIDEO NGẮN KHUNG MỚI (kế hoạch Người Gác Sử, mục 1): 60-80 giây, dọc 1080x1920.

Kịch bản: khóa "ngan" trong scripts/<mã>.json
  {"hook_text": "chữ to trên màn hình đầu (**tô màu**)",
   "hooks": ["các phiên bản hook để thử", ...],       # không đọc, chỉ để chọn
   "caption": "dòng đầu caption ...",
   "beats": [{"loai_canh": "hook|vong_lap|boi_canh|leo_thang|cu_lat|ket",
              "text": "lời đọc",
              "the": {...},                              # THẺ THÔNG TIN (tùy chọn) hiện suốt cảnh, kiểu video Emu:
                  # {"type": "number", "pre": "Khoảng", "value": "20.000", "unit": "con emu", "caption": "…"}
                  # {"type": "explain", "title": "Quân đội vào cuộc", "bullets": ["2 súng máy", "10.000 viên đạn"]}
                  # {"type": "text", "text": "Quân đội **rút lui**", "sub": "Báo chí gọi là …"}
                  # {"type": "outro", "recap": "2 súng máy · 10.000 viên đạn · emu vẫn thắng"}
              "doi_canh": true,                          # sang nơi chốn / thời điểm khác
              "chuyen_canh": "wipeleft",                 # ghi đè chuyển cảnh vào cảnh này, tùy chọn
              "images": [{"url": "...", "credit": "..."} | {"mo_phong": "prompt tiếng Anh"}]}]}

- Mỗi hình đứng 2-4 giây (nhiều hình cho một câu dài); không zoom / cắt cận lại cùng một hình.
- Không có phụ đề chạy liên tục: chỉ chữ hook (cảnh đầu) và các thẻ thông tin chính ở phần dưới-giữa khung
  (mép dưới cách đáy 560 px). Cảnh có thẻ: ảnh ngang đặt ở nửa trên, thẻ bên dưới trên nền tối dần (như video Emu).
- Giọng Gemini đọc nhanh 1,12 lần.
- Chuyển cảnh theo mục "Chuyển cảnh" của kế hoạch: cấu trúc câu chuyện trước, rồi bảng màu ngẫu nhiên theo mã chuyện.
"""
import array
import hashlib
import json
import math
import random
import re
import subprocess
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

import make_video as mv

ROOT = Path(__file__).resolve().parent
W, H, FPS = 1080, 1920, 30
SR = mv.SR
SPEED = 1.12
AMBER = "#FFC66B"
SHORT_STYLE = ("Native Vietnamese narrator (Northern accent, Hanoi) for a short vertical true-history video. "
               "Deep, warm male storyteller with a hint of mystery; lively, gripping pace; clear diction and natural "
               "Vietnamese tones; punchy first sentence; slow down and pause briefly at '…' before the twist. Never robotic.")
log = mv.log

# ------------------------------------------------------------------ chuyển cảnh (kế hoạch, mục "Chuyển cảnh")
LIGHT = ["fade", "dissolve", "hblur"]
DIRECTION = ["smoothleft", "smoothright", "smoothup", "smoothdown", "wipeleft", "wiperight", "wipeup", "wipedown"]
EMPHASIS = ["fadeblack", "fadewhite", "circleopen", "circleclose"]
BANNED = {"zoomin", "pixelize", "squeezeh", "squeezev", "radial", "distance"}
FAVOR = {"bi-an": ["dissolve", "hblur", "fade", "smoothleft", "smoothright", "wipedown"],
         "su-la": ["smoothleft", "smoothright", "wipeleft", "wiperight", "fade", "dissolve"],
         "sinh-ton": ["smoothleft", "smoothup", "fade", "dissolve", "wiperight"],
         "phi-vu": ["wipeleft", "wiperight", "wipeup", "fade", "smoothleft"]}


def _dir_of(tr):
    for d in ("left", "right", "up", "down"):
        if tr.endswith(d):
            return d
    return ""


def choose_transitions(shots, sid, topic):
    """Gán shots[i]['tr'], ['trd'] (giây) cho lần chuyển VÀO cảnh i (i >= 1)."""
    rnd = random.Random(f"palette|{sid}")
    fav = FAVOR.get(topic, LIGHT + DIRECTION)
    pool = list(dict.fromkeys(fav + rnd.sample(LIGHT + DIRECTION, 4)))
    palette = rnd.sample(pool, k=min(len(pool), rnd.randint(4, 6)))
    if not any(p in LIGHT for p in palette):
        palette[0] = rnd.choice(LIGHT)
    pl = [p for p in palette if p in LIGHT] or LIGHT
    pd = [p for p in palette if p in DIRECTION] or ["smoothleft"]
    r2 = random.Random(f"scene|{sid}")
    prev = ""
    for i, s in enumerate(shots):
        if i == 0:
            s["tr"], s["trd"] = "cut", 0.0
            continue
        kind, first = s["loai"], s["first_in_beat"]
        tr, d = None, round(r2.uniform(0.3, 0.5), 2)
        if first and s.get("override") and s["override"] not in BANNED:
            tr = s["override"]                                   # 2. ghi đè trong kịch bản
        elif kind in ("hook", "vong_lap", "boi_canh") and shots[i - 1]["loai"] in ("hook", "vong_lap", "boi_canh"):
            tr = "cut"                                           # 6 giây đầu: cắt thẳng, nhịp nhanh
        elif first and kind == "cu_lat" and shots[i - 1]["loai"] != "cu_lat":
            tr, d = ("fadeblack" if topic in ("bi-an",) or s.get("mat") else "fadewhite"), 0.5
        elif first and kind == "ket" and shots[i - 1]["loai"] != "ket":
            tr, d = "fade", 0.6                                  # sang câu kết: tan chậm
        elif not first:
            tr = "cut" if r2.random() < 0.6 else "dissolve"     # cùng một khoảnh khắc
        elif s.get("doi_canh"):
            tr = r2.choice([x for x in pd if _dir_of(x) != _dir_of(prev)] or pd)
        else:
            x = r2.random()                                      # tầng 2: ngẫu nhiên trong bảng màu
            tr = "cut" if x < 0.55 else (r2.choice(pl) if x < 0.8 else r2.choice(pd))
        if tr == prev and tr != "cut":
            alt = [p for p in pl + pd if p != prev and _dir_of(p) != _dir_of(prev)]
            tr = r2.choice(alt) if alt else "cut"
        if tr != "cut" and prev != "cut" and _dir_of(tr) and _dir_of(tr) == _dir_of(prev):
            tr = r2.choice(pl)
        s["tr"], s["trd"] = tr, (0.0 if tr == "cut" else d)
        prev = tr
    return palette


def check_transitions(shots, sid, palette):
    used = [s["tr"] for s in shots[1:]]
    cnt = {}
    for t in used:
        cnt[t] = cnt.get(t, 0) + 1
    non_cut = {k: v for k, v in cnt.items() if k != "cut"}
    lines = [f"CHUYỂN CẢNH {sid} (video ngắn) · bảng màu: {', '.join(palette)}",
             "Thứ tự: " + " → ".join(used),
             "Số lần: " + ", ".join(f"{k} {v}" for k, v in sorted(cnt.items(), key=lambda x: -x[1]))]
    errs = []
    if used:
        for k, v in non_cut.items():
            if v / len(used) > 0.4:
                errs.append(f"'{k}' chiếm {v}/{len(used)} lần chuyển (> 40%)")
        for k in cnt:
            if k in BANNED:
                errs.append(f"dùng hiệu ứng bị cấm: {k}")
    lines += [f"❌ {e}" for e in errs] or ["✅ Đạt (không hiệu ứng nào chiếm quá 40%, không dùng hiệu ứng bị cấm)"]
    (ROOT / "logs").mkdir(exist_ok=True)
    (ROOT / "logs" / f"chuyen_canh_{sid}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    log("  🎞️  " + lines[2])
    return errs


def _ease(x):
    return x * x * (3 - 2 * x)


_NOISE = None


def transition(a, b, q, kind):
    """Khung chuyển từ a sang b, q 0 -> 1."""
    import cv2
    global _NOISE
    q = max(0.0, min(1.0, q))
    e = _ease(q)
    if kind == "fade":
        return cv2.addWeighted(a, 1 - e, b, e, 0)
    if kind == "dissolve":
        if _NOISE is None:
            _NOISE = np.random.RandomState(7).rand(H // 4, W // 4).astype(np.float32)
            _NOISE = cv2.resize(_NOISE, (W, H), interpolation=cv2.INTER_NEAREST)
        m = (_NOISE < q)[..., None]
        return np.where(m, b, a)
    if kind == "hblur":
        k = int(1 + 160 * math.sin(math.pi * q))
        mix = cv2.addWeighted(a, 1 - e, b, e, 0)
        return cv2.blur(mix, (k, 1)) if k > 2 else mix
    if kind.startswith("smooth") or kind.startswith("wipe"):
        d = _dir_of(kind)
        horiz = d in ("left", "right")
        n = W if horiz else H
        off = int(round(e * n))
        out = np.empty_like(a)
        if kind.startswith("smooth"):          # cả hai hình cùng trượt
            if d == "left":
                out[:, :W - off] = a[:, off:]; out[:, W - off:] = b[:, :off]
            elif d == "right":
                out[:, off:] = a[:, :W - off]; out[:, :off] = b[:, W - off:]
            elif d == "up":
                out[:H - off] = a[off:]; out[H - off:] = b[:off]
            else:
                out[off:] = a[:H - off]; out[:off] = b[H - off:]
            return out
        out[:] = a                               # gạt: hình mới lộ ra sau một mép thẳng
        if d == "left":
            out[:, W - off:] = b[:, W - off:]
        elif d == "right":
            out[:, :off] = b[:, :off]
        elif d == "up":
            out[H - off:] = b[H - off:]
        else:
            out[:off] = b[:off]
        return out
    if kind in ("fadeblack", "fadewhite"):
        col = 0 if kind == "fadeblack" else 255
        c = np.full_like(a, col)
        return cv2.addWeighted(a, 1 - q * 2, c, q * 2, 0) if q < 0.5 else cv2.addWeighted(c, 2 - q * 2, b, q * 2 - 1, 0)
    if kind in ("circleopen", "circleclose"):
        yy, xx = np.ogrid[:H, :W]
        r = math.hypot(W, H) / 2 * (e if kind == "circleopen" else 1 - e)
        m = ((xx - W / 2) ** 2 + (yy - H / 2) ** 2 <= r * r)[..., None]
        return np.where(m, b, a) if kind == "circleopen" else np.where(m, a, b)
    return b


# ------------------------------------------------------------------ hình
def _path(src):
    from urllib.parse import unquote, urlparse
    s = str(src)
    return unquote(urlparse(s).path) if s.startswith("file:") else s


def grade(im):
    import long_render
    return long_render.grade(im, sepia=0.22, contrast=1.06, bright=0.95, sat=0.9)


def make_plate(src, depth=None, top=False):
    """Khung dọc 1080x1920 (lớn hơn 6% để máy quay trôi nhẹ): ảnh dọc phủ kín; ảnh ngang thành dải giữa màn hình,
    nền trên/dưới là chính ảnh phóng to làm mờ."""
    PW, PH = int(W * 1.06), int(H * 1.06)
    im = Image.open(_path(src)).convert("RGB")
    w, h = im.size
    if w / h <= 0.8:
        s = max(PW / w, PH / h)
        r = im.resize((max(PW, round(w * s)), max(PH, round(h * s))), Image.LANCZOS)
        x, y = (r.width - PW) // 2, int((r.height - PH) * 0.35)
        return grade(r.crop((x, y, x + PW, y + PH)))
    bg = im.resize((max(1, PW // 8), max(1, round(PW // 8 * h / w))), Image.BILINEAR)
    s = max(PW / bg.width, PH / bg.height)
    bg = bg.resize((round(bg.width * s) + 2, round(bg.height * s) + 2), Image.BILINEAR)
    bg = bg.crop(((bg.width - PW) // 2, (bg.height - PH) // 2, (bg.width - PW) // 2 + PW, (bg.height - PH) // 2 + PH))
    bg = bg.filter(ImageFilter.GaussianBlur(18))
    import long_render
    bg = long_render.grade(bg, sepia=0.3, contrast=1.0, bright=0.42, sat=0.9)
    if top:   # cảnh có thẻ chữ: ảnh trọn bề ngang ở nửa trên, mép dưới tan dần vào nền mờ (kiểu video Emu)
        band = im.resize((PW, max(1, round(PW * h / w))), Image.LANCZOS)
        mh = int(PH * 0.47)
        if band.height > mh:
            yc = int((band.height - mh) * 0.3)
            band = band.crop((0, yc, PW, yc + mh))
        band = grade(band)
        y0 = int(PH * 0.075)
        fade = min(160, band.height // 3)
        mask = np.full((band.height, PW), 255, np.uint8)
        mask[-fade:] = (np.linspace(1, 0, fade) ** 1.3 * 255).astype(np.uint8)[:, None]
        bg.paste(band, (0, y0), Image.fromarray(mask))
        return bg
    # dải ảnh: thấy ít nhất 55% bề ngang (ảnh vuông: 80%), cao tối đa 74% khung
    vis = 0.55 if w / h >= 1.5 else 0.8 if w / h <= 1.1 else 0.66
    bw = PW / vis
    bh = bw * h / w
    if bh > PH * 0.74:
        bh = PH * 0.74
        bw = bh * w / h
    band = im.resize((max(PW, round(bw)), round(bh)), Image.LANCZOS)
    # chủ thể (vật nhô lên theo bản đồ độ sâu) ở giữa bề ngang
    cx = 0.5
    if depth:
        try:
            import long_video
            cx, _ = long_video._subject(src, depth, [0, 0, 1, 1])
        except Exception:
            cx = 0.5
    x0 = int(min(max(cx * band.width - PW / 2, 0), band.width - PW))
    band = grade(band.crop((x0, 0, x0 + PW, band.height)))
    y0 = int((PH - band.height) * 0.36)   # dải ảnh hơi cao hơn giữa để phụ đề phía dưới ít che chủ thể
    bg.paste(band, (0, y0))
    return bg


def shot_frame(plate, lt, dur, k):
    """Máy quay trôi rất nhẹ (không phải zoom cận): đẩy vào 3%, xen kẽ hướng."""
    import cv2
    PH_, PW_ = plate.shape[:2]
    p = max(0.0, min(1.0, lt / max(0.1, dur)))
    z = 1.0 + 0.03 * (p if k % 2 == 0 else 1 - p)
    sw, sh = W / z, H / z
    cx = PW_ / 2 + (8 if k % 4 in (1, 2) else -8) * (p - 0.5)
    cy = PH_ / 2
    x0, y0 = cx - sw / 2, cy - sh / 2
    m = np.array([[sw / W, 0, x0], [0, sh / H, y0]], np.float64)
    return cv2.warpAffine(plate, m, (W, H), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                          borderMode=cv2.BORDER_REPLICATE)


# ------------------------------------------------------------------ phụ đề
def _plain(t):
    return re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", t)).strip()


WEAK_END = {"của", "và", "các", "những", "một", "là", "với", "cho", "từ", "ở", "trong", "khi", "thì", "mà", "đã",
            "vẫn", "còn", "rằng", "như", "để", "bị", "được", "tên", "về", "nhất", "có", "không", "cũng", "này", "ấy",
            "người", "con", "chiếc", "tàu", "năm", "tháng", "ngày", "ông", "bà", "cô"}


COMPOUND = set("""thuyền trưởng|thế giới|cứu sinh|hàng hải|hàng hóa|gia đình|đại tây|tây dương|con tàu|lảo đảo|nhà văn|
truyện ngắn|hư cấu|giả thuyết|hợp lý|rò rỉ|xảy ra|cướp bóc|đánh nhau|dấu vết|bốc khói|tan biến|bữa sáng|tách trà|lời đồn|
nổi tiếng|chi tiết|câu chuyện|biến mất|thủy thủ|duy nhất|nhật ký|trước đó|quần áo|đồ đạc|chỗ cũ|mãi mãi|bao giờ|tàu buồm|
cầm lái|nhìn thấy|trèo lên|con gái|bắt nguồn|đầu tiên|mọi người|sắp nổ|khoang tàu|đi biển|hóa ra|thức ăn|còn nguyên|
quân đội|súng máy|nông dân|lúa mì|chiến tranh|người lính|đà điểu|ruộng lúa|báo chí|quốc hội|bộ trưởng|thiếu tá|
viên đạn|chiến dịch|khẩu súng|đầu hàng|cấp trên|khu rừng|hòn đảo|truyền đơn|sự thật|lịch sử|bí ẩn|có thật|
năm sau|tháng sau|ngày sau|vì sao|tại sao|như thể|hơn cả|vẫn còn|đã từng|không ai|không còn|xuống xuồng|dừng lại|tiếng nhất|bỏ tàu|vụ nổ|vừa tan|chiến thắng|trở về|ra khỏi|tìm thấy""".replace("\n", "").split("|"))


def chunk_words(text, lo=2, hi=6):
    """Cụm phụ đề ngắn (khoảng 2-4 từ tiếng Việt, tối đa 6 tiếng), ngắt ở dấu câu; trong mỗi vế câu chọn chỗ ngắt
    sao cho cụm đều nhau, không tách từ ghép ('thuyền | trưởng') và không kết thúc bằng hư từ ('của', 'một'...).
    **Từ khóa** giữ nguyên một khối."""
    toks = re.findall(r"\*\*[^*]+\*\*[.,!?…;:]*|\S+", text)
    phrases, cur = [], []
    for tk in toks:
        cur.append(tk)
        if re.search(r"[.,!?…;:]\**$", tk):
            phrases.append(cur)
            cur = []
    if cur:
        phrases.append(cur)

    def size(tk):
        return len(tk.strip("*.,!?…;:").split()) or 1

    def bare(tk):
        return tk.strip("*.,!?…;:").lower()

    res = []
    for ph in phrases:
        m = len(ph)
        best = [(0.0, [])] + [(1e9, None)] * m        # DP theo vị trí token
        for j in range(1, m + 1):
            for i in range(j - 1, -1, -1):
                L = sum(size(x) for x in ph[i:j])
                if L > hi and j - i > 1:
                    break
                if best[i][1] is None:
                    continue
                c = best[i][0] + 0.35 * (L - 4) ** 2 + (3 if L < lo and m > 1 else 0)
                if j < m:
                    last = bare(ph[j - 1]).split()[-1] if bare(ph[j - 1]) else ""
                    if last in WEAK_END:
                        c += 4
                    if not ph[j - 1].endswith("**") and not ph[j].startswith("**") and \
                            (bare(ph[j - 1]).split() or [""])[-1] + " " + (bare(ph[j]).split() or [""])[0] in COMPOUND:
                        c += 7
                if c < best[j][0]:
                    best[j] = (c, best[i][1] + [j])
        cuts = [0] + (best[m][1] or [m])
        for a, b in zip(cuts, cuts[1:]):
            s = " ".join(ph[a:b])
            s = re.sub(r"\s+([.,!?…;:])", r"\1", s)
            s = re.sub(r"[,;:]$", "", s).strip()
            res.append(s)
    # vế quá ngắn (1 tiếng) gộp vào cụm trước
    out = []
    for s in res:
        if out and size(s) <= 1 and len(out[-1].split()) + 1 <= hi + 1:
            out[-1] += " " + s
        else:
            out.append(s)
    return out


def auto_keywords(s):
    """Tô màu con số (nếu tác giả chưa đánh dấu)."""
    if "**" in s:
        return s
    return re.sub(r"(?<!\*)(\b\d[\d.,/]*(?:\s?(?:tuổi|ngày|tháng|năm|thùng|người|thủy thủ))?)", r"**\1**", s)


# ------------------------------------------------------------------ dựng
def _beat_images(script, beats, work):
    """Tải / vẽ ảnh của từng cảnh. Trả về (credits, used_ai)."""
    import ai_images
    import images
    import long_video
    uniq = {}
    for b in beats:
        for im in b["images"]:
            if im.get("url"):
                uniq.setdefault(json.dumps(im, sort_keys=True, ensure_ascii=False), {"image": im})
    credits = []
    if uniq:
        credits = images.fetch_scene_images({"topic": script.get("topic", ""), "scenes": list(uniq.values())},
                                            work / "arch", log)
        miss = [k for k, v in uniq.items() if not v.get("image_src")]
        if miss:
            raise RuntimeError(f"không tải được {len(miss)} ảnh tư liệu (sẽ thử lại lần chạy sau)")
    used_ai = False
    long_video.AI_CACHE.mkdir(parents=True, exist_ok=True)
    for b in beats:
        for im in b["images"]:
            if im.get("url"):
                im["_src"] = uniq[json.dumps({k: v for k, v in im.items() if not k.startswith("_")},
                                             sort_keys=True, ensure_ascii=False)]["image_src"]
            elif im.get("mo_phong"):
                key = hashlib.sha1((ai_images.STYLE_PHOTO_ID + "|" + im["mo_phong"]).encode()).hexdigest()[:16]
                f = long_video.AI_CACHE / f"mp_{key}.jpg"
                ai_images.generate(im["mo_phong"] + ", " + long_video.WIDE_HINT, f, log=log, wide=True,
                                   style=ai_images.photo_style(im["mo_phong"]), cheap=True)
                ai_images.to_wide(f)
                im["_src"], im["_ai"] = f.resolve().as_uri(), True
                used_ai = True
    return credits, used_ai


def _check(script, beats):
    """Kiểm tra ảnh trước khi đọc giọng (dùng chung bước kiểm tra của video dài: tạo lại ảnh mô phỏng lỗi)."""
    import long_video
    pseudo = []
    for b in beats:
        for im in b["images"]:
            pseudo.append({"image_src": im["_src"], "_ai": bool(im.get("_ai")), "mo_phong": im.get("mo_phong"),
                           "text": b["text"], "image": {k: v for k, v in im.items() if not k.startswith("_")}})
    long_video.check_images(script, pseudo, log, kind="ngan")


def narration(beats, voice, work):
    import gemini_tts
    import long_video
    texts = [gemini_tts.clean_text(b["text"])[0] for b in beats]
    full = "\n\n".join(texts)
    long_video.TTS_CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(f"{voice}|{SHORT_STYLE}|{SPEED}|{full}".encode()).hexdigest()[:16]
    wav = long_video.TTS_CACHE / f"ngan_{key}.wav"
    if not wav.exists():
        t = time.time()
        raw = gemini_tts.synth(full, SHORT_STYLE, voice, log=log)
        tmp = work / f"{key}_raw.wav"
        tmp.write_bytes(raw)
        mv.run_ffmpeg(["-i", str(tmp), "-af", f"atempo={SPEED}", "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16",
                       str(wav)])
        log(f"  🎙️  Gemini đọc xong ({time.time() - t:.0f}s), tốc độ x{SPEED}")
    audio = mv.read_wav(wav)
    segs, (a, b) = long_video.split_by_pauses(audio, [max(8, len(x)) for x in texts])
    return audio, segs, (a, b)


def _trim(samples, margin=0.04):
    """Cắt khoảng lặng thừa đầu/cuối một câu đọc (giữ lại margin giây)."""
    x = np.frombuffer(samples.tobytes(), np.int16).astype(np.float32)
    win = int(0.02 * SR)
    k = len(x) // win
    if k < 3:
        return samples
    rms = np.sqrt((x[:k * win].reshape(k, win) ** 2).mean(1) + 1e-6)
    speech = rms[rms > np.percentile(rms, 30)]
    thr = max(120.0, 0.08 * float(np.median(speech)) if len(speech) else 120.0)
    nz = np.where(rms > thr)[0]
    if not len(nz):
        return samples
    a = max(0, nz[0] * win - int(margin * SR))
    b = min(len(x), (nz[-1] + 1) * win + int(margin * SR))
    return samples[a:b]


def narration_styled(beats, voice, work, huyen_bi=False):
    """Kế hoạch (Âm thanh và giọng đọc, B): đọc TỪNG CẢNH với chỉ dẫn sắc thái theo loai_canh, chữ đã chuẩn hóa
    (số, viết tắt, từ điển phát âm), rồi ghép lại với khoảng nghỉ chủ động: 0,25-0,35 giây giữa các cảnh,
    0,7 giây trước cú lật. Trả về (mẫu âm, [(bắt đầu, kết thúc) từng cảnh], tổng thời lượng, khoảng lặng trước cú lật)."""
    import concurrent.futures as cf
    import am_thanh
    import gemini_tts
    import long_video
    tu = am_thanh.load_dict()
    long_video.TTS_CACHE.mkdir(parents=True, exist_ok=True)
    jobs = []
    for b in beats:
        txt = am_thanh.chuan_hoa(gemini_tts.clean_text(b["text"])[0], tu)
        style = SHORT_STYLE + " " + am_thanh.sac_thai(b.get("loai_canh"), huyen_bi)
        key = hashlib.sha1(f"v2|{voice}|{style}|{SPEED}|{txt}".encode()).hexdigest()[:16]
        jobs.append((txt, style, long_video.TTS_CACHE / f"nganb_{key}.wav"))

    def one(job):
        txt, style, wav = job
        if wav.exists():
            return False
        raw = gemini_tts.synth(txt, style, voice, log=log)
        tmp = work / f"{wav.stem}_raw.wav"
        tmp.write_bytes(raw)
        mv.run_ffmpeg(["-i", str(tmp), "-af", f"atempo={SPEED}", "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16",
                       str(wav)])
        return True

    t = time.time()
    with cf.ThreadPoolExecutor(3) as ex:
        made = sum(ex.map(one, jobs))
    if made:
        log(f"  🎙️  Gemini đọc {made}/{len(jobs)} cảnh, mỗi cảnh một sắc thái ({time.time() - t:.0f}s), tốc độ x{SPEED}")
    lead, tail = 0.15, 0.5
    narr = array.array("h", mv.silence(lead))
    pos, times, twist_gap, seen_twist = lead, [], None, False
    for i, (b, (_, _, wav)) in enumerate(zip(beats, jobs)):
        if i:
            if b.get("loai_canh") == "cu_lat" and not seen_twist:
                gap = 0.7
            elif b.get("doi_canh"):
                gap = 0.35
            else:
                gap = 0.25
            if b.get("loai_canh") == "cu_lat" and not seen_twist:
                twist_gap = (pos, pos + gap)
            narr.extend(mv.silence(gap))
            pos += gap
        seen_twist = seen_twist or b.get("loai_canh") == "cu_lat"
        a = _trim(mv.read_wav(wav))
        narr.extend(a)
        times.append((pos, pos + len(a) / SR))
        pos += len(a) / SR
    narr.extend(mv.silence(tail))
    return narr, times, pos + tail, twist_gap


def sfx_events(beats, times, total, twist_gap):
    """Lớp tiếng động cho video ngắn (dày, theo nhịp nhanh): tiếng nền theo nhãn am_thanh của từng cảnh,
    tiếng nhấn ngay giây đầu, tiếng "vút" khi đổi nơi chốn, tiếng dâng lên rồi lặng trước cú lật."""
    import am_thanh
    ev = [{"label": "hit", "start": 0.0, "db": -8}]
    for i, (b, (s, e)) in enumerate(zip(beats, times)):
        start = 0.0 if i == 0 else s
        end = times[i + 1][0] if i + 1 < len(times) else total
        for lb in am_thanh.labels_ok(b.get("am_thanh") or []):
            if lb in am_thanh.ONE_SHOT:
                ev.append({"label": lb, "start": start + 0.05, "db": -14})
            else:
                ev.append({"label": lb, "start": max(0, start - 0.3), "dur": end - start + 0.6, "db": -20})
        if i and b.get("doi_canh"):
            ev.append({"label": "vut", "start": max(0, s - 0.45), "db": -16})
    if twist_gap:
        ev.append({"label": "rise", "start": max(0, twist_gap[0] + 0.2 - 2.2), "db": -12})
    return ev


CARD_TOP_MIN = 560    # thẻ chữ không được cao quá mức này (để nửa trên dành cho ảnh)


def _count_steps(value, n=14):
    """Các giá trị đếm dần cho con số lớn ("20.000" -> "0", "1.400", ... "20.000")."""
    m = re.match(r"^([^\d]*)([\d.,]+)(.*)$", str(value))
    if not m or re.search(r"[:/]", str(value)):
        return [str(value)]
    digits = m.group(2)
    if "," in digits and "." not in digits and len(digits.split(",")[-1]) != 3:
        return [str(value)]          # số thập phân (2,5) thì không đếm
    target = int(re.sub(r"[.,]", "", digits))
    if target < 10:
        return [str(value)]
    out = []
    for k in range(1, n + 1):
        e = 1 - (1 - k / n) ** 3
        out.append(m.group(1) + f"{round(target * e):,}".replace(",", ".") + m.group(3))
    out[-1] = str(value)
    return out


def render_overlays(script, cfg, cards, work):
    """cards: [{"card": {...}, ...}] -> mỗi thẻ thêm "frames": [(thời điểm tương đối, png)]."""
    from playwright.sync_api import sync_playwright
    work.mkdir(parents=True, exist_ok=True)
    topic = (cfg.get("topics") or {}).get(script.get("topic", ""), {})
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch()
        page = br.new_page(viewport={"width": W, "height": H})
        page.goto((ROOT / "templates" / "ngan.html").as_uri())
        page.evaluate("() => document.fonts.ready")

        def snap(name, **a):
            top_y = page.evaluate("a => window.show(a)", dict(a, accent=AMBER))
            page.wait_for_timeout(30)
            f = work / name
            page.screenshot(path=str(f), type="png", omit_background=True)
            return str(f), top_y

        out["top"] = snap("top.png", id="top", icon=topic.get("icon", ""), label=topic.get("label", ""),
                          brand=cfg.get("channel", ""))[0]
        for i, c in enumerate(cards):
            cd = dict(c["card"])
            if cd.get("type") == "outro":
                cd.setdefault("text", cfg.get("catchphrase", ""))
                cd.setdefault("follow", cfg.get("follow", ""))
            frames = []
            if cd.get("type") == "explain" and len(cd.get("bullets") or []) > 1:
                nb = len(cd["bullets"])
                for k in range(1, nb + 1):   # gạch đầu dòng hiện lần lượt trong 60% đầu của cảnh
                    f, y = snap(f"card_{i}_{k}.png", id="card", card=dict(cd, shown=k))
                    frames.append(((k - 1) / nb * 0.6, f, y))
            elif cd.get("type") == "number":
                steps = _count_steps(cd.get("value", ""))
                for k, v in enumerate(steps):  # con số đếm dần trong 1,2 giây đầu (giá trị tuyệt đối, giây)
                    f, y = snap(f"card_{i}_{k}.png", id="card", card=dict(cd, value_now=v))
                    frames.append((-(0.15 + 1.2 * k / max(1, len(steps) - 1)), f, y))
            else:
                f, y = snap(f"card_{i}.png", id="card", card=cd)
                frames.append((0.0, f, y))
            hi = min(y for _, _, y in frames)
            if hi < CARD_TOP_MIN:
                log(f"  ⚠️  thẻ chữ cảnh {c['beat'] + 1} cao quá (mép trên y={hi:.0f}), nên rút gọn chữ")
            c["frames"] = [(t, f) for t, f, _ in frames]
        br.close()
    return out


def build(script, cfg, out_dir, variant="moi"):
    """variant="moi": tiếng động theo cảnh + nhạc nền tự hạ + giọng đổi sắc thái theo đoạn (kế hoạch, mục Âm thanh).
    variant="cu": bản cũ chỉ ảnh + giọng đọc một lượt (dùng cho thử nghiệm A/B), xuất <mã>_ban_cu.mp4."""
    import cv2
    import long_render
    import motion
    sid = script["id"]
    N = script["ngan"]
    voice = cfg.get("gemini_voice", "Sadaltager")
    huyen_bi = (script.get("phong_cach") == "huyen-bi") and variant == "moi"
    if huyen_bi:
        voice = N.get("giong") or script.get("giong") or voice     # giọng trầm riêng cho kịch bản huyền bí
    work = out_dir / ("_work_ngan" if variant == "moi" else "_work_ngan_cu")
    work.mkdir(parents=True, exist_ok=True)
    beats = [dict(b, images=[dict(im) for im in b["images"]]) for b in N["beats"]]

    if variant == "moi":
        import nguon_anh
        nguon_anh.record(script, log)      # chặn ảnh không phải PD/CC0, lưu bằng chứng giấy phép
    log("  🖼️  Ảnh cho video ngắn" + ("" if variant == "moi" else " (bản cũ A/B)"))
    credits, used_ai = _beat_images(script, beats, work)
    if variant == "moi":
        _check(script, beats)

    log(f"  🎙️  Giọng Gemini {voice}")
    twist_gap = None
    if variant == "moi":
        narr, times, total, twist_gap = narration_styled(beats, voice, work, huyen_bi)
    else:
        audio, segs, (a0, b0) = narration(beats, voice, work)
        lead = 0.15
        narr = array.array("h", mv.silence(lead))
        narr.extend(audio[a0:b0])
        tail = 0.5
        narr.extend(mv.silence(tail))
        total = lead + (b0 - a0) / SR + tail
        # mốc thời gian từng câu (giây trong video)
        times = [(lead + (s - a0) / SR, lead + (e - a0) / SR) for s, e in segs]
    shots, cards = [], []
    for i, (b, (s, e)) in enumerate(zip(beats, times)):
        start = 0.0 if i == 0 else s
        end = times[i + 1][0] if i + 1 < len(times) else total
        card = b.get("the")
        if i == 0 and N.get("hook_text") and not card:
            card = {"type": "hook", "text": N["hook_text"]}
        if card == "giu" and cards and abs(cards[-1]["end"] - start) < 0.05:
            cards[-1]["end"] = end                     # giữ nguyên thẻ của cảnh trước
        elif isinstance(card, dict):
            cards.append({"card": card, "start": start, "end": end, "beat": i})
        has_card = bool(card)
        n = len(b["images"])
        for j, im in enumerate(b["images"]):
            shots.append({"src": im["_src"], "ai": bool(im.get("_ai")), "start": start + (end - start) * j / n,
                          "end": start + (end - start) * (j + 1) / n, "loai": b.get("loai_canh", "leo_thang"),
                          "first_in_beat": j == 0, "doi_canh": bool(b.get("doi_canh")), "top": has_card,
                          "override": b.get("chuyen_canh"), "mat": bool(b.get("co_nguoi_mat"))})
    log(f"  🪧 {len(cards)} thẻ thông tin (không phụ đề chạy liên tục)")
    long_dur = [s for s in shots if s["end"] - s["start"] > 4.05]
    log(f"  ⏱️  {total:.1f} giây · {len(shots)} hình · trung bình {total / max(1, len(shots)):.1f} giây/hình"
        + (f" · ⚠️ {len(long_dur)} hình đứng quá 4 giây" if long_dur else ""))
    palette = choose_transitions(shots, sid, script.get("topic", ""))
    errs = check_transitions(shots, sid, palette)
    if errs:
        raise RuntimeError("chuyển cảnh không đạt: " + "; ".join(errs))

    ov = render_overlays(script, cfg, cards, work / "ov")
    L_top = long_render._ov(ov["top"])
    for c in cards:
        d = c["end"] - c["start"]
        c["layers"] = [(c["start"] + (-t if t < 0 else t * d), long_render._ov(f)) for t, f in c["frames"]]

    # độ sâu để đặt chủ thể giữa dải ảnh
    depths = {}
    for s in shots:
        if s["src"] not in depths:
            try:
                depths[s["src"]] = motion.depth_map(s["src"], log=log)
            except Exception:
                depths[s["src"]] = None
    plates = {}

    def plate(i):
        src = shots[i]["src"]
        key = (src, shots[i]["top"])
        if key not in plates:
            if len(plates) > 6:
                plates.pop(next(iter(plates)))
            plates[key] = np.ascontiguousarray(np.asarray(make_plate(src, depths.get(src), top=shots[i]["top"])))
        return plates[key]

    def over(img, layer):
        import cv2
        inv, pre = layer
        return cv2.add(cv2.multiply(img, inv, scale=1 / 255), pre)

    def frame_of(i, t):
        # plan: không đóng chữ "Ảnh minh họa" lên ảnh (dùng nhãn nội dung AI của nền tảng khi đăng)
        return shot_frame(plate(i), t - shots[i]["start"], shots[i]["end"] - shots[i]["start"], i)

    silent = work / "silent.mp4"
    n = int(math.ceil(total * FPS))
    cmd = [mv.ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
           "-pix_fmt", "yuv420p", str(silent)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    si = 0
    review = []
    for f in range(n):
        t = f / FPS
        while si + 1 < len(shots) and t >= shots[si + 1]["start"]:
            si += 1
        img = frame_of(si, t)
        nx = si + 1
        if nx < len(shots) and shots[nx]["tr"] != "cut":
            d = shots[nx]["trd"]
            if t >= shots[nx]["start"] - d:
                q = (t - (shots[nx]["start"] - d)) / d
                img = transition(img, frame_of(nx, t), q, shots[nx]["tr"])
        img = over(img, L_top)
        for c in cards:   # thẻ thông tin: hiện dần 0,25 s, tắt dần 0,2 s cuối cảnh
            if c["start"] <= t < c["end"]:
                lay = c["layers"][0][1]
                for tt, ly in c["layers"]:
                    if t >= tt:
                        lay = ly
                a = min(1.0, (t - c["start"] - 0.05) / 0.25, (c["end"] - t) / 0.2)
                if a > 0:
                    withc = over(img, lay)
                    img = withc if a >= 1 else cv2.addWeighted(withc, a, img, 1 - a, 0)
                break
        if abs(t - (shots[si]["start"] + shots[si]["end"]) / 2) < 0.5 / FPS:
            review.append(img.copy())
        proc.stdin.write(np.ascontiguousarray(img).data)
    proc.stdin.close()
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError("ffmpeg lỗi khi dựng video ngắn")
    log(f"  🎬 Dựng {n} khung hình ({time.time() - t0:.0f}s)")

    mv.write_wav(work / "narration.wav", narr)
    import audio_fx
    import music
    track, mcredit = music.pick({"id": sid + "-ngan", "topic": script.get("topic", ""),
                                 "music": N.get("music") or script.get("music")}, log)
    final = out_dir / (f"{sid}.mp4" if variant == "moi" else f"{sid}_ban_cu.mp4")
    if variant == "moi":
        import am_thanh
        ev = sfx_events(beats, times, total, twist_gap)
        quiet = (twist_gap[0] + 0.2, twist_gap[1]) if twist_gap else None
        bed = am_thanh.voice_bed(work / "narration.wav", ev, total, quiet=quiet)
        am_thanh.save_bed(work / "sfx.wav", bed)
        log(f"  🔊 Tiếng động: {', '.join(sorted({e['label'] for e in ev}))}")
        am_thanh.mix(silent, work / "narration.wav", total, track, final, cfg, bed_wav=work / "sfx.wav", quiet=quiet,
                     fade_out=2.5, log=log)
    else:
        args = ["-i", str(silent), "-i", str(work / "narration.wav")]
        graph = [f"[1:a]{audio_fx.VOICE_CHAIN},aresample=44100,asplit=2[v][vk]"]
        if track:
            args += ["-stream_loop", "-1", "-i", str(track)]
            dk = cfg.get("music_duck", {})
            graph += [f"[2:a]loudnorm=I={cfg.get('music_lufs', -17)}:LRA=11:TP=-3,aresample=44100,afade=t=in:d=1,"
                      f"afade=t=out:st={max(0, total - 1.2):.2f}:d=1.2[mr]",
                      f"[mr][vk]sidechaincompress=threshold={dk.get('threshold', 0.06)}:ratio={dk.get('ratio', 3)}:"
                      f"attack=40:release=500[m]",
                      "[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]"]
        else:
            graph += ["[vk]anullsink", "[v]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]"]
        mv.run_ffmpeg(args + ["-filter_complex", ";".join(graph), "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                              "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart",
                              str(final)])
        log(f"  🅰️  Bản cũ cho thử nghiệm A/B: {final.name}")
        return final, total
    # lưới khung hình để kiểm tra (không gửi Telegram)
    try:
        thumbs = [Image.fromarray(r).resize((216, 384)) for r in review]
        cols = 8
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 220, rows * 388), (12, 12, 12))
        for k, th in enumerate(thumbs):
            sheet.paste(th, ((k % cols) * 220 + 2, (k // cols) * 388 + 2))
        sheet.save(out_dir / f"{sid}_review.jpg", quality=85)
        Image.fromarray(review[0]).save(out_dir / f"{sid}_thumbnail.jpg", quality=92) if review else None
    except Exception as e:
        log(f"     (không tạo được lưới khung hình: {e})")
    script["_credits"] = credits
    script["_music_credit"] = mcredit
    try:
        make_covers(script, cfg, beats, out_dir, work, log)
    except Exception as e:
        log(f"     ⚠️  không tạo được ảnh bìa: {e}")
    write_caption(script, cfg, out_dir, used_ai)
    return final, total


def make_covers(script, cfg, beats, out_dir, work, log=print):
    """Ảnh bìa riêng (không phải khung hình đầu): ảnh phủ kín, làm tối, chữ RẤT to gây tò mò + nhãn đỏ.
    Kịch bản: ngan.anh_bia = [{"anh": "beat:ảnh" (vd "1:0"), "nhan": "BÍ ẨN 150 NĂM", "to": "10 người\nbiến mất",
    "nho": "Con tàu vẫn còn nguyên…"}]. Xuất <mã>_bia_1.jpg… và <mã>_thumbnail.jpg = phương án 1."""
    import cv2
    import long_render
    from playwright.sync_api import sync_playwright
    specs = script["ngan"].get("anh_bia") or []
    if not specs:
        return []
    outs = []
    with sync_playwright() as p:
        br = p.chromium.launch()
        page = br.new_page(viewport={"width": W, "height": H})
        page.goto((ROOT / "templates" / "ngan.html").as_uri())
        page.evaluate("() => document.fonts.ready")
        for k, sp in enumerate(specs, 1):
            bi, ii = (int(x) for x in str(sp.get("anh", "0:0")).split(":"))
            im = beats[bi]["images"][ii]
            src = Image.open(_path(im["_src"])).convert("RGB")
            w, h = src.size
            s = max(W / w, H / h)
            r = src.resize((max(W, round(w * s)), max(H, round(h * s))), Image.LANCZOS)
            fx = float(sp.get("x", 0.5))
            x0 = int(min(max(fx * r.width - W / 2, 0), r.width - W))
            y0 = int((r.height - H) * 0.4)
            base = long_render.grade(r.crop((x0, y0, x0 + W, y0 + H)), sepia=0.15, contrast=1.18, bright=0.8, sat=1.0)
            a = np.asarray(base).astype(np.float32)
            yy = np.linspace(0, 1, H)[:, None, None]
            xx = np.linspace(-1, 1, W)[None, :, None]
            shade = 0.55 + 0.45 * np.clip(1 - 1.6 * np.abs(yy - 0.62), 0, 1)   # tối phần chữ, sáng giữa-dưới
            vig = 1 - 0.35 * (xx ** 2)
            a = np.clip(a * shade * vig, 0, 255).astype(np.uint8)
            page.evaluate("a => window.show(a)", {"id": "thumb", "accent": AMBER, "tag": sp.get("nhan", ""),
                                                   "big": sp.get("to", ""), "small": sp.get("nho", "")})
            page.wait_for_timeout(40)
            f = work / f"bia_{k}.png"
            page.screenshot(path=str(f), type="png", omit_background=True)
            inv, pre = long_render._ov(f)
            img = cv2.add(cv2.multiply(np.ascontiguousarray(a), inv, scale=1 / 255), pre)
            out = out_dir / f"{script['id']}_bia_{k}.jpg"
            Image.fromarray(img).save(out, quality=93)
            outs.append(out)
        br.close()
    if outs:
        import shutil
        shutil.copy(outs[0], out_dir / f"{script['id']}_thumbnail.jpg")
        log(f"  🖼️  Ảnh bìa: {len(outs)} phương án ({', '.join(o.name for o in outs)})")
    return outs


def write_caption(script, cfg, out_dir, used_ai):
    N = script["ngan"]
    tags = " ".join("#" + t.lstrip("#") for t in (script.get("hashtags") or []))
    short = mv._short_credits(script.get("_credits"))
    lines_social = [N.get("caption") or script.get("caption", script["title"]), "",
                    cfg.get("follow", "👉 Theo dõi để mở trang sử tiếp theo"), cfg.get("catchphrase", ""), "", tags]
    if short:
        lines_social += ["", "📷 Ảnh tư liệu: " + "; ".join(short)]
    if script.get("_music_credit"):
        m = script["_music_credit"]
        lines_social.append(f"🎵 Nhạc: {m}")
    if used_ai:
        lines_social.append("Video có sử dụng tranh minh họa tạo bằng AI.")
    lines = ["════ FACEBOOK REELS / TIKTOK / YOUTUBE SHORTS — copy nguyên khối dưới đây ════", *lines_social, "",
             f"Tiêu đề YouTube Shorts: {script['title'][:95]}",
             "Tag YouTube: " + ", ".join(script.get("tu_khoa") or [t.lstrip("#") for t in script.get("hashtags", [])]),
             *__import__("binh_luan").lines(script, "ngan"), "",
             "════ GHI CHÚ (không đăng) ════", "Nhớ bật nhãn \"Nội dung do AI tạo\" khi đăng.",
             "Các phiên bản hook khác để thử:"] + [f"- {h}" for h in N.get("hooks", [])] + \
        ["Nguồn kiểm chứng:"] + [f"- {s}" for s in script.get("sources", [])]
    if script.get("_credits"):
        lines += ["Nguồn ảnh đầy đủ:"] + [f"- {c}" for c in script["_credits"]]
    (out_dir / f"{script['id']}_caption.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
