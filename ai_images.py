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
CUTOUT_HINT = "full body, whole figure visible from head to feet, centered, isolated on a plain pure white background"


def generate(prompt, out, cutout=False, seed=None, steps=8, log=print):
    """Vẽ 1 ảnh. Trả về đường dẫn. Có sẵn file thì dùng lại (không tốn lượt)."""
    out = Path(out)
    if out.exists() and out.stat().st_size > 10000:
        return out
    acc = os.environ.get("CF_ACCOUNT_ID", "").strip()
    tok = os.environ.get("CF_API_TOKEN", "").strip()
    if not acc or not tok:
        raise RuntimeError("Chưa có CF_ACCOUNT_ID / CF_API_TOKEN")
    full = f"{prompt}, {CUTOUT_HINT if cutout else ''}, {STYLE}".replace(", ,", ",")
    body = {"prompt": full[:2000], "steps": steps}
    if seed is not None:
        body["seed"] = int(seed)
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
            log(f"     🎨 {out.name}")
            return out
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:300]
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(10 * (attempt + 1))
                continue
            raise RuntimeError(f"Cloudflare AI HTTP {e.code}: {msg}")
    raise RuntimeError("Cloudflare AI: thử lại nhiều lần vẫn lỗi")


_SESSION = None


def cutout(src, out):
    """Tách nền (rembg), cắt sát viền nhân vật."""
    global _SESSION
    from PIL import Image
    from rembg import new_session, remove
    out = Path(out)
    if out.exists():
        return out
    if _SESSION is None:
        _SESSION = new_session("isnet-general-use")
    im = Image.open(src).convert("RGBA")
    res = remove(im, session=_SESSION, post_process_mask=True)
    bbox = res.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()
    if bbox:
        res = res.crop(bbox)
    res.save(out)
    return out
