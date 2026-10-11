"""
Dựng khung hình video dài 16:9 NHANH (thay cho chụp màn hình từng khung bằng trình duyệt).

- Trình duyệt (templates/long.html) chỉ vẽ các LỚP TĨNH một lần: lớp phủ (đèn, viền tối, logo kênh),
  hạt phim, nhãn địa danh, thẻ chương.
- Python (Pillow) ghép từng khung: ảnh đã chỉnh màu + chuyển động máy quay chậm (Ken Burns) + tan ảnh + lớp tĩnh.
- Chia đoạn cho nhiều nhân CPU, mỗi đoạn mã hóa riêng rồi nối lại (không mã hóa lại).

Chuyển động, độ mờ, màu… giữ đúng như long.html để video giống bản xem thử trên trình duyệt.
"""
import math
import multiprocessing as mp
import os
import subprocess
import time
from pathlib import Path
from urllib.parse import unquote, urlparse

import numpy as np
from PIL import Image, ImageFilter

W, H = 1920, 1080
PW, PH = int(W * 1.1), int(H * 1.1)       # .img có inset -5% -> rộng hơn khung 10%
BG = (11, 6, 4)                           # #0b0604
XF = 1.0                                  # thời gian tan ảnh (giây)
LAMP_LEVELS = 7
NOISE_VARIANTS = 12


def _path(src):
    if src.startswith("file:"):
        return unquote(urlparse(src).path)
    return src


# ------------------------------------------------------------------ chỉnh màu như CSS filter
def _sepia(a):
    k = 1 - a
    return np.array([[0.393 + 0.607 * k, 0.769 - 0.769 * k, 0.189 - 0.189 * k],
                     [0.349 - 0.349 * k, 0.686 + 0.314 * k, 0.168 - 0.168 * k],
                     [0.272 - 0.272 * k, 0.534 - 0.534 * k, 0.131 + 0.869 * k]], np.float32)


def _saturate(s):
    return np.array([[0.213 + 0.787 * s, 0.715 - 0.715 * s, 0.072 - 0.072 * s],
                     [0.213 - 0.213 * s, 0.715 + 0.285 * s, 0.072 - 0.072 * s],
                     [0.213 - 0.213 * s, 0.715 - 0.715 * s, 0.072 + 0.928 * s]], np.float32)


def grade(im, sepia=0.3, contrast=1.06, bright=0.88, sat=0.85):
    """sepia(0.3) contrast(1.06) brightness(0.88) saturate(0.85) theo đúng thứ tự CSS."""
    a = np.asarray(im.convert("RGB"), np.float32) / 255.0
    a = a @ _sepia(sepia).T
    a = (a - 0.5) * contrast + 0.5
    a = np.clip(a, 0, 1) * bright
    if sat != 1:
        a = a @ _saturate(sat).T
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def _cover(im, w, h, ay=0.5):
    """Phủ kín khung w x h; ay = vị trí cắt theo chiều dọc (0.35: giữ phần trên nhiều hơn, tránh mất đầu nhân vật)."""
    s = max(w / im.width, h / im.height)
    r = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    x, y = (r.width - w) // 2, int((r.height - h) * ay)
    return r.crop((x, y, x + w, y + h))


def _fit_box(im):
    s = min(PW / im.width, PH / im.height)
    fw, fh = round(im.width * s), round(im.height * s)
    return fw, fh, (PW - fw) // 2, (PH - fh) // 2


def make_depth_plate(src, depth, fit):
    """Bản đồ độ sâu đặt đúng vị trí như make_plate (float32 PH x PW). Ảnh đặt giữa nền mờ: chỉ phần ảnh có độ sâu,
    mép ảnh và nền mờ đứng yên (không bị xé)."""
    import motion
    im = Image.open(_path(src))
    d = motion.load_depth(depth, im.size)
    if d is None:
        return None
    dimg = Image.fromarray((d * 255 + 0.5).astype(np.uint8))
    if not fit:
        return np.asarray(_cover(dimg, PW, PH, 0.35), np.float32) / 255.0
    fw, fh, x0, y0 = _fit_box(im)
    out = np.full((PH, PW), motion.FOCUS, np.float32)
    fd = np.asarray(dimg.resize((fw, fh), Image.BILINEAR), np.float32) / 255.0
    m = motion.edge_taper(fw, fh)
    out[y0:y0 + fh, x0:x0 + fw] = fd * m + motion.FOCUS * (1 - m)
    return out


def make_plate(src, fit):
    """Ảnh nền của một cảnh, kích thước PW x PH, đã chỉnh màu."""
    im = Image.open(_path(src)).convert("RGB")
    if not fit:
        return grade(_cover(im, PW, PH, 0.35))
    # ảnh dọc / nhỏ: nền là chính ảnh đó phóng to, làm mờ, tối; ảnh gốc đặt giữa, hiện trọn
    bg = _cover(im, PW // 4, PH // 4).filter(ImageFilter.GaussianBlur(10)).resize((PW, PH), Image.BILINEAR)
    bg = grade(bg, sepia=0.4, contrast=1.0, bright=0.45, sat=1.0)
    fw, fh, x0, y0 = _fit_box(im)
    fg = grade(im.resize((fw, fh), Image.LANCZOS))
    bg.paste(fg, (x0, y0))
    return bg


# ------------------------------------------------------------------ lớp tĩnh vẽ bằng trình duyệt
JS_PREP = """
() => {
  for (const id of ['imgs','shade','lamp','noise','vig','brand','label','card'])
    document.getElementById(id).style.display = 'none';
  document.documentElement.style.background = 'transparent';
  document.body.style.background = 'transparent';
  document.getElementById('root').style.background = 'transparent';
}"""
JS_SHOW = """
(a) => {
  for (const id of ['imgs','shade','lamp','noise','vig','brand','label','card'])
    document.getElementById(id).style.display = a.show.includes(id) ? '' : 'none';
  if (a.lamp != null) document.getElementById('lamp').style.opacity = a.lamp;
  if (a.noise) document.getElementById('noise').style.transform = `translate(${a.noise[0]}px, ${a.noise[1]}px)`;
  const lab = document.getElementById('label');
  if (a.label != null) { lab.textContent = a.label; lab.style.opacity = 1; }
  const card = document.getElementById('card');
  if (a.card) {
    card.querySelector('.k').textContent = a.card.kicker || '';
    card.querySelector('.t').innerHTML = rich(a.card.title || '');
    card.querySelector('.s').textContent = a.card.sub || '';
    card.querySelector('.r').style.display = a.card.sub ? '' : 'none';
    card.style.opacity = 1;
  }
}"""


def lamp_level(t):
    return 0.8 + 0.12 * math.sin(t * 7.1) * math.sin(t * 2.3)


def render_layers(page, channel, labels, cards, work):
    """Vẽ các lớp tĩnh ra PNG. Trả về dict đường dẫn."""
    work.mkdir(parents=True, exist_ok=True)
    page.evaluate("c => { document.getElementById('brand').textContent = c; }", channel)
    page.evaluate(JS_PREP)
    out = {"lamp": [], "noise": [], "label": {}, "card": []}

    def snap(name, **a):
        page.evaluate(JS_SHOW, {"show": a.pop("show"), **a})
        p = work / name
        page.screenshot(path=str(p), type="png", omit_background=True)
        return str(p)

    for k in range(LAMP_LEVELS):
        lv = 0.68 + 0.24 * k / (LAMP_LEVELS - 1)
        out["lamp"].append(snap(f"ov_{k}.png", show=["shade", "lamp", "vig", "brand"], lamp=lv))
    for k in range(NOISE_VARIANTS):
        f = k * 7 + 3
        out["noise"].append(snap(f"noise_{k}.png", show=["noise"], noise=[(f * 37) % 80 - 40, (f * 53) % 80 - 40]))
    for i, lab in enumerate(sorted(set(labels))):
        out["label"][lab] = snap(f"label_{i}.png", show=["label"], label=lab)
    for i, c in enumerate(cards):
        out["card"].append(snap(f"card_{i}.png", show=["card"], card=c))
    return out


# ------------------------------------------------------------------ ghép khung
def _clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def _ov(path):
    """Lớp RGBA -> (1-alpha, màu đã nhân alpha) để ghép nhanh: ra = ảnh*(1-a) + màu*a."""
    a = np.asarray(Image.open(path).convert("RGBA"))
    al = a[..., 3:4].astype(np.uint16)
    inv = np.repeat((255 - al).astype(np.uint8), 3, axis=2)
    pre = ((a[..., :3].astype(np.uint16) * al + 127) // 255).astype(np.uint8)
    return inv, pre


class Compositor:
    def __init__(self, shots, cards, layers, motion_cfg=None):
        import motion
        self.mc = motion.settings({"motion": motion_cfg})
        self.fx = motion.FX(W, H, self.mc["fx_strength"]) if self.mc["fx"] else None
        self.grid = None
        self.shots = shots
        self.cards = cards
        self.ov = [_ov(p) for p in layers["lamp"]]
        self.noise = [_ov(p) for p in layers["noise"]]
        self.labels = {k: _ov(p) for k, p in layers["label"].items()}
        self.card_img = [np.ascontiguousarray(np.asarray(Image.open(p).convert("RGB"))) for p in layers["card"]]
        self.bg = np.empty((H, W, 3), np.uint8)
        self.bg[:] = BG
        self.plates = {}

    def plate(self, i):
        if i not in self.plates:
            if len(self.plates) > 4:
                self.plates.pop(next(iter(self.plates)))
            s = self.shots[i]
            pl = np.ascontiguousarray(np.asarray(make_plate(s["src"], s.get("fit"))))
            dp = None
            if self.mc["parallax"] and s.get("depth"):
                try:
                    dp = make_depth_plate(s["src"], s["depth"], s.get("fit"))
                except Exception:
                    dp = None
            bl = None
            if dp is not None and self.mc["dof"] > 0 and not s.get("fit"):
                import cv2
                bl = cv2.GaussianBlur(pl, (0, 0), sigmaX=PW * 0.0045)
            self.plates[i] = (pl, dp, bl)
        return self.plates[i]

    def shot_frame(self, i, lt):
        import cv2
        s = self.shots[i]
        p = _clamp((lt + XF) / (s["dur"] + 2 * XF))
        d = i % 4
        if s.get("fit"):
            z, tx, ty = 1 + 0.05 * p, 0.0, 0.0
        else:
            z = [1.04 + 0.10 * p, 1.14 - 0.10 * p, 1.10, 1.10][d]
            tx = [0, 0, -2.5 + 5 * p, 2.5 - 5 * p][d] / 100 * PW
            ty = [-1 * p, 1 * p, 0, 0][d] / 100 * PH
        # CSS: scale(z) translate(t) quanh tâm -> điểm khung X ứng với điểm ảnh (X - tâm)/z - t + tâm_ảnh
        import motion
        if self.mc["transition"] == "zoom":
            z *= motion.kick(lt, s["dur"], XF, i > 0, i + 1 < len(self.shots))
        if self.mc["light"] and "shake" in str(s.get("fx", "")):
            dx, dy = motion.shake(s["start"] + lt)
            tx, ty = tx + dx * W, ty + dy * H
        a = 1 / z
        m = np.array([[a, 0, PW / 2 - tx - (W / 2) * a + 0.5 * a - 0.5],
                      [0, a, PH / 2 - ty - (H / 2) * a + 0.5 * a - 0.5]], np.float64)
        plate, dp, bl = self.plate(i)
        if dp is None:
            return cv2.warpAffine(plate, m, (W, H), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                                  borderMode=cv2.BORDER_REPLICATE)
        # parallax 2.5D: tọa độ lấy mẫu = Ken Burns như cũ + độ lệch theo độ sâu
        if self.grid is None:
            self.grid = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
        xs = self.grid[0] * np.float32(a) + np.float32(m[0, 2])
        ys = self.grid[1] * np.float32(a) + np.float32(m[1, 2])
        dz = cv2.warpAffine(dp, m, (W, H), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
        kind = [0, 2, 3, 1][i % 4]      # cùng hướng với kiểu Ken Burns của cảnh
        cam = motion.camera(kind, p, self.mc["parallax_strength"] * (0.6 if s.get("fit") else 1.0))
        mx, my = motion.parallax_maps(xs, ys, dz, PW, PH, cam)
        sharp = cv2.remap(plate, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        if bl is None:
            return sharp
        # đổi tiêu điểm: chỗ xa độ sâu đang lấy nét thì mờ dần (như ống kính máy quay)
        blur = cv2.remap(bl, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        wb = np.clip(np.abs(dz - np.float32(motion.focal(i, p))) * np.float32(1.2), 0, 1) * np.float32(self.mc["dof"])
        return cv2.blendLinear(sharp, blur, 1 - wb, wb)

    @staticmethod
    def _over(img, layer):
        import cv2
        inv, pre = layer
        return cv2.add(cv2.multiply(img, inv, scale=1 / 255), pre)

    def frame(self, t):
        import cv2
        # thẻ chương che kín cả khung -> không cần ghép ảnh
        cv = 0.0
        ci = -1
        for k, c in enumerate(self.cards):
            if c["start"] <= t < c["start"] + c["dur"]:
                lt = t - c["start"]
                cv, ci = min(_clamp(lt / 0.6), _clamp((c["dur"] - lt) / 0.6)), k
                break
        if ci >= 0 and cv >= 0.999:
            return self.card_img[ci]
        img = self.bg
        leak_q = 0.0
        for i, s in enumerate(self.shots):
            lt = t - s["start"]
            if lt < -XF or lt > s["dur"] + XF:
                continue
            a, b = _clamp((lt + XF) / XF), _clamp((s["dur"] + XF - lt) / XF)
            o = b if s["start"] <= 0.01 else min(a, b)
            if o <= 0.002:
                continue
            if i > 0 and lt < 0:
                leak_q = max(leak_q, a)
            fr = self.shot_frame(i, lt)
            if self.fx is not None and s.get("fx"):
                fr = self.fx.apply(fr, s["fx"], t, light=self.mc["light"])
            img = fr if o >= 0.998 else cv2.addWeighted(img, 1 - o, fr, o, 0)
        if leak_q > 0 and self.fx is not None and self.mc["transition"] == "zoom":
            img = self.fx.leak(img, leak_q)
        lv = round((_clamp(lamp_level(t), 0.68, 0.92) - 0.68) / 0.24 * (LAMP_LEVELS - 1))
        img = self._over(img, self.ov[lv])
        img = self._over(img, self.noise[int(t * 12) % NOISE_VARIANTS])
        # nhãn địa danh / năm
        for s in self.shots:
            if s.get("label") and s["start"] + 0.6 <= t < s["start"] + min(s["dur"], 6):
                end = s["start"] + min(s["dur"], 6)
                lo = min(_clamp((t - s["start"] - 0.6) / 0.5), _clamp((end - t) / 0.5))
                withlab = self._over(img, self.labels[s["label"]])
                img = withlab if lo >= 0.998 else cv2.addWeighted(img, 1 - lo, withlab, lo, 0)
                break
        if ci >= 0 and cv > 0.002:
            img = cv2.addWeighted(img, 1 - cv, self.card_img[ci], cv, 0)
        return img


def _encode_range(args):
    comp, i0, i1, fps, out, ffmpeg, crf = args
    cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
           "-pix_fmt", "yuv420p", "-g", str(fps * 2), str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(i0, i1):
        proc.stdin.write(np.ascontiguousarray(comp.frame(i / fps)).data)
    proc.stdin.close()
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg lỗi ở đoạn {out}")
    return str(out)


_COMP = None


def _worker(args):
    return _encode_range((_COMP,) + tuple(args))


def render(shots, cards, layers, total, fps, out, ffmpeg, work, log=print, workers=None, crf=20, motion_cfg=None):
    """Dựng video câm `out` dài `total` giây."""
    global _COMP
    _COMP = Compositor(shots, cards, layers, motion_cfg)
    n = int(math.ceil(total * fps))
    workers = workers or max(1, os.cpu_count() or 1)
    # chia nhiều đoạn hơn số nhân để chia việc đều; cắt ở ranh giới GOP
    parts = max(workers * 3, 1)
    step = max(fps * 2, int(math.ceil(n / parts / (fps * 2))) * fps * 2)
    jobs = [(i0, min(n, i0 + step), fps, work / f"seg_{k:03d}.mp4", ffmpeg, crf)
            for k, i0 in enumerate(range(0, n, step))]
    t0 = time.time()
    log(f"     {n} khung hình, {len(jobs)} đoạn, {workers} luồng")
    ctx = mp.get_context("fork")
    with ctx.Pool(workers) as pool:
        segs = []
        for k, s in enumerate(pool.imap(_worker, jobs)):
            segs.append(s)
            if (k + 1) % max(1, len(jobs) // 4) == 0:
                log(f"     … {k + 1}/{len(jobs)} đoạn ({time.time() - t0:.0f} giây)")
    lst = work / "segs.txt"
    lst.write_text("".join(f"file '{Path(s).resolve()}'\n" for s in segs))
    subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(out)], check=True)
    for s in segs:
        Path(s).unlink(missing_ok=True)
    log(f"     dựng khung hình xong trong {time.time() - t0:.0f} giây")
    return out


def review_sheet(shots, cards, layers, out, cols=8, motion_cfg=None):
    """Ảnh duyệt video dài: 1 khung giữa mỗi cảnh ảnh, xếp lưới, đánh số để kiểm tra trước khi gửi."""
    from PIL import ImageDraw, ImageFont
    comp = Compositor(shots, cards, layers, motion_cfg)
    tw, th = 320, 180
    tiles = []
    for i, s in enumerate(shots):
        t = s["start"] + min(s["dur"] * 0.5, 3.0)
        im = Image.fromarray(np.ascontiguousarray(comp.frame(t))).resize((tw, th), Image.BILINEAR)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 34, 20], fill=(0, 0, 0))
        d.text((4, 3), str(i + 1), fill=(255, 210, 120), font=ImageFont.load_default(size=14))
        tiles.append(im)
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 4), rows * (th + 4)), (10, 10, 10))
    for k, im in enumerate(tiles):
        sheet.paste(im, ((k % cols) * (tw + 4), (k // cols) * (th + 4)))
    sheet.save(out, quality=82)
    return out
