"""
Vẽ ảnh minh họa bằng AI (miễn phí): FLUX.1 schnell trên Cloudflare Workers AI.
Cần GitHub Secrets: CF_ACCOUNT_ID, CF_API_TOKEN (tài khoản dự phòng: CF_ACCOUNT_ID_2, CF_API_TOKEN_2).

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
MODEL2 = "@cf/black-forest-labs/flux-2-klein-4b"   # đẹp hơn, vẽ thẳng khung 16:9, ít tốn lượt hơn
# Phong cách chung: tranh vẽ 2D (không giả ảnh chụp), để người xem không nhầm là ảnh tư liệu thật
STYLE = ("2D animated illustration in the style of a modern history explainer cartoon, lively expressive characters, "
         "dynamic composition, clean bold outlines, cel shading, warm rich colors, detailed painted background, "
         "historically accurate clothing and setting, no text, no watermark, not photorealistic, not 3D")
STYLE_ID = "2d-v2"   # đổi khi đổi phong cách -> ảnh cũ trong bộ nhớ đệm không bị dùng lại
# ẢNH MÔ PHỎNG (cho đoạn không có ảnh tư liệu): giống ảnh chụp cũ cùng thời, nhưng KHÔNG vẽ mặt người thật
# nhận ra được (người quay lưng / ở xa / trong bóng tối). Trên video luôn có nhãn "Ảnh minh họa".
STYLE_PHOTO = ("realistic historical documentary photograph, period-accurate clothing, objects and setting, "
               "natural light, muted faded colors, slight film grain, shot on a vintage film camera, "
               "people seen from behind, in silhouette or at a distance with faces not clearly visible, "
               "no text, no letters, no watermark, no logo, no modern objects")
STYLE_PHOTO_ID = "photo-v1"
CUTOUT_HINT = ("full body, whole figure visible from head to feet, centered, isolated on a plain pure white background, "
               "no shadow, no ground, no signature")
RIG_POSE = ("standing upright facing the viewer, front view, arms held slightly away from the body, "
            "hands open, legs slightly apart, both feet visible")


_CF_OUT = {"v": False}   # Cloudflare đã hết lượt trong lần chạy này -> chuyển thẳng sang nguồn dự phòng
_CF_IDX = {"i": 0}       # đang dùng tài khoản Cloudflare thứ mấy (CF_..., rồi CF_..._2)


def _accounts():
    out = []
    for suf in ("", "_2", "_3"):
        a = os.environ.get("CF_ACCOUNT_ID" + suf, "").strip()
        t = os.environ.get("CF_API_TOKEN" + suf, "").strip()
        if a and t and (a, t) not in out:
            out.append((a, t))
    return out


def _creds():
    acc = _accounts()
    if not acc:
        return "", ""
    return acc[min(_CF_IDX["i"], len(acc) - 1)]


def _next_account(log=print):
    """Tài khoản hiện tại hết lượt -> chuyển sang tài khoản dự phòng (nếu có). Trả về True nếu chuyển được."""
    if _CF_IDX["i"] + 1 < len(_accounts()):
        _CF_IDX["i"] += 1
        _CF_OUT["v"] = False
        log(f"     🔁 Cloudflare tài khoản {_CF_IDX['i']} hết lượt, chuyển sang tài khoản {_CF_IDX['i'] + 1}")
        return True
    return False


def _cloudflare(full, out, steps):
    acc, tok = _creds()
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


def _klein(full, out, wide, seed=None):
    """FLUX.2 klein 4B trên Cloudflare (gửi dạng multipart/form-data)."""
    import uuid
    acc, tok = _creds()
    if not acc or not tok:
        raise RuntimeError("Chưa có CF_ACCOUNT_ID / CF_API_TOKEN")
    w, h = (1344, 768) if wide else (1024, 1024)
    fields = {"prompt": full[:2000], "width": str(w), "height": str(h)}
    if seed is not None:
        fields["seed"] = str(int(seed))
    bnd = uuid.uuid4().hex
    body = b"".join(f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
                    for k, v in fields.items()) + f"--{bnd}--\r\n".encode()
    url = f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/{MODEL2}"
    for attempt in range(4):
        req = urllib.request.Request(url, data=body, method="POST",
                                     headers={"Authorization": f"Bearer {tok}",
                                              "Content-Type": f"multipart/form-data; boundary={bnd}"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                raw, ctype = r.read(), r.headers.get("Content-Type", "")
            if ctype.startswith("image/"):
                data = raw
            else:
                res = json.loads(raw.decode())
                img = (res.get("result") or {}).get("image")
                if not img:
                    raise RuntimeError(json.dumps(res)[:300])
                data = base64.b64decode(img)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
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


def generate(prompt, out, cutout=False, seed=None, steps=4, log=print, wide=False, style=None, cheap=False):
    """Vẽ 1 ảnh bằng FLUX.2 klein (Cloudflare); lỗi riêng mô hình này thì thử FLUX.1 schnell.
    Tài khoản Cloudflare hết lượt miễn phí -> tự chuyển sang tài khoản dự phòng (CF_ACCOUNT_ID_2 / CF_API_TOKEN_2).
    Hết lượt cả các tài khoản thì báo lỗi (429/limit) để video được hoãn sang lần chạy sau.
    Có sẵn file thì dùng lại (không tốn lượt)."""
    out = Path(out)
    if out.exists() and out.stat().st_size > 10000:
        return out
    full = f"{prompt}, {CUTOUT_HINT if cutout else ''}, {style or STYLE}".replace(", ,", ",")
    while True:
        if _CF_OUT["v"] and not _next_account(log):
            raise RuntimeError("Cloudflare AI hết lượt miễn phí hôm nay (429/limit)")
        try:
            if cheap:   # FLUX.1 schnell: ~80 neurons/ảnh thay vì ~1.400 của FLUX.2 klein (mức miễn phí 10.000/ngày)
                _cloudflare(full, out, max(steps, 6))
                if wide:
                    to_wide(out)
            else:
                try:
                    _klein(full, out, wide, seed)
                except RuntimeError as e:
                    if _CF_OUT["v"]:
                        raise
                    log(f"     ↪️  FLUX.2 lỗi ({str(e)[:80]}), thử FLUX.1")
                    _cloudflare(full, out, steps)
            log(f"     🎨 {out.name}")
            return out
        except RuntimeError:
            if _CF_OUT["v"] and _next_account(log):
                continue
            raise


def to_wide(path, width=1344):
    """FLUX.1 schnell chỉ trả ảnh vuông: cắt viền đen/trắng thừa, cắt giữa về khung 16:9 rồi phóng lên 1344x756.
    Ảnh đã ngang sẵn thì để nguyên."""
    import numpy as np
    from PIL import Image
    p = Path(path)
    im = Image.open(p).convert("RGB")
    if im.width / im.height >= 1.7:
        return p
    a = np.asarray(im.convert("L"), np.int16)
    rows = np.where((a.mean(1) > 14) & (a.mean(1) < 245) | (a.std(1) > 6))[0]
    cols = np.where((a.mean(0) > 14) & (a.mean(0) < 245) | (a.std(0) > 6))[0]
    if len(rows) > a.shape[0] // 2 and len(cols) > a.shape[1] // 2:
        im = im.crop((int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1))
    w, h = im.size
    ch = min(h, round(w * 9 / 16))
    cw = min(w, round(ch * 16 / 9))
    x0, y0 = (w - cw) // 2, max(0, (h - ch) * 45 // 100)
    im = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((width, round(width * 9 / 16)), Image.LANCZOS)
    im.save(p, quality=93)
    return p


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
