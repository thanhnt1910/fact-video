"""
Vẽ ảnh minh họa bằng AI (miễn phí): FLUX.1 schnell trên Cloudflare Workers AI.
Cần GitHub Secrets: CF_ACCOUNT_ID, CF_API_TOKEN.

  generate(prompt, out_path)          -> ảnh 1024x1024 (jpg)
  cutout(in_path, out_png)            -> tách nền, cắt sát nhân vật (png trong suốt)

Phong cách chung của kênh được ghép vào mọi prompt (STYLE) để các ảnh trông cùng một bộ.
"""
import base64
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

MODEL = "@cf/black-forest-labs/flux-1-schnell"
STYLE = ("vintage storybook illustration, painterly oil paint texture, warm sepia and amber tones, "
         "soft lantern light, muted colors, detailed, historical, no text, no watermark")
CUTOUT_HINT = ("full body, whole figure visible from head to feet, centered, isolated on a plain pure white background, "
               "no shadow, no ground, no signature")
RIG_POSE = ("standing upright facing the viewer, front view, arms held slightly away from the body, "
            "hands open, legs slightly apart, both feet visible")


_CF_OUT = {"v": False}   # Cloudflare đã hết lượt trong lần chạy này -> chuyển thẳng sang nguồn dự phòng


def _cloudflare(full, out, steps):
    acc = os.environ.get("CF_ACCOUNT_ID", "").strip()
    tok = os.environ.get("CF_API_TOKEN", "").strip()
    if not acc or not tok:
        raise RuntimeError("Chưa có CF_ACCOUNT_ID / CF_API_TOKEN")
    body = {"prompt": full[:2000], "steps": steps}
    # FLUX schnell trên Cloudflare không nhận tham số seed
    url = f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/{MODEL}"
    for attempt in range(4):
        req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                     headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                res = json.loads(r.read().decode())
            img = (res.get("result") or {}).get("image")
            if not img:
                raise RuntimeError(json.dumps(res)[:300])
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(base64.b64decode(img))
            return out
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:300]
            if "neurons" in msg or "4006" in msg:
                _CF_OUT["v"] = True
                raise RuntimeError(f"Cloudflare AI hết lượt miễn phí hôm nay (429/limit): {msg[:120]}")
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(10 * (attempt + 1))
                continue
            raise RuntimeError(f"Cloudflare AI HTTP {e.code}: {msg}")
    raise RuntimeError("Cloudflare AI: thử lại nhiều lần vẫn lỗi (429/limit)")


def _pollinations(full, out, wide):
    """Nguồn dự phòng miễn phí (cũng là FLUX), không cần khóa; chậm và có giới hạn tốc độ."""
    from urllib.parse import quote
    import random
    w, h = (1344, 768) if wide else (1024, 1024)
    url = (f"https://image.pollinations.ai/prompt/{quote(full[:900])}"
           f"?width={w}&height={h}&model=flux&nologo=true&private=true&seed={random.randint(1, 10**6)}")
    last = ""
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "nguoi-gac-su-video/1.0"})
            with urllib.request.urlopen(req, timeout=180) as r:
                data, ctype = r.read(), r.headers.get("Content-Type", "")
            if not ctype.startswith("image") or len(data) < 10000:
                raise RuntimeError(f"không phải ảnh ({ctype}, {len(data)} byte)")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            time.sleep(3)
            return out
        except Exception as e:
            last = str(e)[:200]
            time.sleep(15 * (attempt + 1))
    raise RuntimeError(f"Pollinations lỗi (limit): {last}")


def generate(prompt, out, cutout=False, seed=None, steps=4, log=print, wide=False):
    """Vẽ 1 ảnh: Cloudflare trước, hết lượt thì sang Pollinations. Có sẵn file thì dùng lại (không tốn lượt).
    steps=4 là mức chuẩn của FLUX schnell (8 bước tốn gấp đôi lượt mà không đẹp hơn rõ rệt)."""
    out = Path(out)
    if out.exists() and out.stat().st_size > 10000:
        return out
    full = f"{prompt}, {CUTOUT_HINT if cutout else ''}, {STYLE}".replace(", ,", ",")
    if not _CF_OUT["v"]:
        try:
            _cloudflare(full, out, steps)
            log(f"     🎨 {out.name}")
            return out
        except RuntimeError as e:
            if not _CF_OUT["v"]:
                raise
            log("     ↪️  Cloudflare hết lượt hôm nay, chuyển sang nguồn vẽ dự phòng (Pollinations)")
    _pollinations(full, out, wide)
    log(f"     🎨 {out.name} (dự phòng)")
    return out


_SESSION = None


def clean_cutout(png):
    """Xóa bóng trắng / chữ ký sót dưới chân, giữ lại mảng nhân vật lớn nhất."""
    import numpy as np
    from PIL import Image
    from scipy import ndimage
    im = Image.open(png).convert("RGBA")
    a = np.array(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3]
    mx, mn = rgb.max(-1), rgb.min(-1)
    sat = (mx - mn) / (mx + 1e-3)
    h = al.shape[0]
    low = np.zeros_like(al, bool)
    low[int(h * 0.85):] = True
    al[(mx > 140) & (sat < 0.16) & low] = 0
    lab, n = ndimage.label(al > 40)
    if n > 1:
        sizes = ndimage.sum(np.ones_like(al), lab, range(1, n + 1))
        keep = 1 + int(np.argmax(sizes))
        al[(lab != keep) & (lab > 0)] = 0
    a[..., 3] = al
    out = Image.fromarray(a.astype(np.uint8))
    bbox = out.getchannel("A").getbbox()
    (out.crop(bbox) if bbox else out).save(png)
    return png


def cutout(src, out):
    """Tách nền (rembg), cắt sát viền nhân vật."""
    global _SESSION
    out = Path(out)
    if out.exists():
        return out
    from PIL import Image
    from rembg import new_session, remove
    if _SESSION is None:
        _SESSION = new_session("isnet-general-use")
    im = Image.open(src).convert("RGBA")
    res = remove(im, session=_SESSION, post_process_mask=True)
    bbox = res.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()
    if bbox:
        res = res.crop(bbox)
    res.save(out)
    clean_cutout(out)
    return out
