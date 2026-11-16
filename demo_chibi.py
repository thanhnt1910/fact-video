"""Dựng thử 15 giây chibi có chuyển động (ảnh tĩnh + nhân vật cắt rời + hiệu ứng + tiếng).
  python demo_chibi.py -> out/nb1_demo_chuyen_dong.mp4  (cần: rembg, opencv, pillow, numpy, ffmpeg)"""
import math, subprocess, wave, random
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1920, 1080, 30, 15.0
SRC = Path("assets/anh_2d/NB1"); OUT = Path("out"); OUT.mkdir(exist_ok=True)
FONT = "assets/bia/fonts/Oswald.ttf"
random.seed(7); np.random.seed(7)


def font(sz, bold=True):
    f = ImageFont.truetype(FONT, sz)
    try:
        f.set_variation_by_name("Bold" if bold else "Regular")
    except Exception:
        pass
    return f


def load(k):
    im = cv2.imread(str(SRC / f"{k}.jpg"))
    return cv2.resize(im, (W, int(im.shape[0] * W / im.shape[1])), interpolation=cv2.INTER_LANCZOS4)


def cutout(k):
    from rembg import remove, new_session
    im = Image.open(SRC / f"{k}.jpg").convert("RGB").resize((W, int(768 * W / 1344)), Image.LANCZOS)
    return np.asarray(remove(im, session=new_session("isnet-anime")))  # RGBA


# ---------- chuẩn bị ----------
A = load("004"); B = load("007"); C = load("006")
sp = cutout("007")                                   # Hideyoshi chạy (RGBA)
mask = (sp[:, :, 3] > 20).astype(np.uint8) * 255
mask_d = cv2.dilate(mask, np.ones((25, 25), np.uint8))
B_clean = cv2.inpaint(B, mask_d, 6, cv2.INPAINT_TELEA)  # phông không còn nhân vật (để nhân vật cắt rời chuyển động)
ys, xs = np.where(mask > 0)
FEET = (float(xs.mean()), float(ys.max()))           # điểm chân để nảy/nghiêng quanh đó
BH = A.shape[0]


def cam(z, px=0.0, py=0.0, sx=0.0, sy=0.0):
    """ma trận 3x3: phóng to z quanh tâm khung, dịch (px,py) + rung (sx,sy)"""
    cx, cy = W / 2, BH / 2
    M = np.array([[z, 0, cx - z * cx + px + sx], [0, z, cy - z * cy + py + sy], [0, 0, 1]], float)
    return M


def warp(img, M, border=cv2.BORDER_REPLICATE):
    return cv2.warpAffine(img, M[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=border)


def ease_out_back(x):
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def over(frame, rgba_img):
    a = rgba_img[:, :, 3:4].astype(np.float32) / 255
    return (frame * (1 - a) + rgba_img[:, :, :3][:, :, ::-1].astype(np.float32) * a).astype(np.uint8) if rgba_img.shape[2] == 4 else frame


def text_layer(txt, sz, fill, stroke=(0, 0, 0), sw=8, angle=0.0, scale=1.0, alpha=1.0):
    f = font(int(sz * scale))
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    bb = d.textbbox((0, 0), txt, font=f, stroke_width=int(sw * scale))
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    lay = Image.new("RGBA", (tw + 40, th + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((20 - bb[0], 20 - bb[1]), txt, font=f, fill=fill, stroke_width=int(sw * scale), stroke_fill=stroke)
    if angle:
        lay = lay.rotate(angle, expand=True, resample=Image.BICUBIC)
    if alpha < 1:
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    return lay


def paste_center(frame, lay, cx, cy):
    x, y = int(cx - lay.width / 2), int(cy - lay.height / 2)
    arr = np.asarray(lay)
    x0, y0 = max(x, 0), max(y, 0); x1, y1 = min(x + lay.width, W), min(y + lay.height, H)
    if x1 <= x0 or y1 <= y0:
        return
    sub = arr[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32); a = sub[:, :, 3:4] / 255
    frame[y0:y1, x0:x1] = (frame[y0:y1, x0:x1] * (1 - a) + sub[:, :, :3][:, :, ::-1] * a).astype(np.uint8)


def caption(frame, txt, t, t0, t1):
    if not (t0 <= t <= t1):
        return
    k = min(1, (t - t0) / 0.25) * min(1, (t1 - t) / 0.25)
    lay = text_layer(txt, 58, (255, 255, 255), sw=7, alpha=max(0, k))
    paste_center(frame, lay, W / 2, H - 150)


def stamp(frame, t, t0):
    if t < t0:
        return 0.0
    u = t - t0
    sc = 1 + 1.4 * max(0, 1 - u / 0.14) ** 2
    lay = text_layer("GIAI THOẠI", 120, (210, 30, 30), stroke=(255, 235, 235), sw=5, angle=8, scale=sc, alpha=min(1, u / 0.06))
    box = Image.new("RGBA", (lay.width + 50, lay.height + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
    d.rounded_rectangle((5, 5, box.width - 6, box.height - 6), 26, outline=(210, 30, 30, 255), width=int(10 * sc), fill=(255, 245, 240, 215))
    box.alpha_composite(lay, (25, 15))
    box = box.rotate(0)
    paste_center(frame, box, 1400, 230)
    return math.exp(-9 * u)   # độ rung màn hình sau cú đóng dấu


def shake(amp, t):
    return amp * math.sin(t * 80), amp * math.cos(t * 67)


# ---------- ba cảnh ----------
def scene_a(t):
    st = 1.25
    amp = 0.0
    z = 1.0 + 0.12 * t / 5
    if t >= st:
        amp = 16 * math.exp(-9 * (t - st))
    sx, sy = shake(amp, t)
    f = warp(A, cam(z, -20 * t, 0, sx, sy))
    s = stamp(f, t, st)
    # chữ tượng thanh BỐP!
    if t >= 2.4:
        u = t - 2.4; sc = ease_out_back(min(1, u / 0.25))
        paste_center(f, text_layer("BỐP!", 150, (255, 224, 40), sw=12, angle=-10, scale=max(sc, 0.05)), 560, 430 - 10 * math.sin(u * 14) * math.exp(-3 * u))
        if u < 0.12:
            f = cv2.addWeighted(f, 1 - 0.35 * (1 - u / 0.12), np.full_like(f, 255), 0.35 * (1 - u / 0.12), 0)
    caption(f, "Giai thoại kể: Nobunaga nhào bột, Hideyoshi nặn bánh, Ieyasu ngồi ăn", t, 0.5, 5.0)
    return f


RAIN = [(random.uniform(0, W), random.uniform(0, H), random.uniform(60, 130), random.uniform(1900, 2700)) for _ in range(240)]


def rain(f, t, alpha=0.5):
    ov = f.copy()
    for x0, y0, ln, sp_ in RAIN:
        y = (y0 + sp_ * t) % (H + 200) - 100; x = (x0 - 0.35 * sp_ * t) % (W + 200) - 100
        cv2.line(ov, (int(x), int(y)), (int(x - ln * 0.35), int(y + ln)), (255, 240, 225), 2, cv2.LINE_AA)
    return cv2.addWeighted(f, 1 - alpha, ov, alpha, 0)


def scene_b(t):
    z = 1.08 + 0.10 * t / 5
    sx, sy = shake(3.5, t * 1.3)
    M = cam(z, 0, 0, sx, sy)
    f = warp(B_clean, M)
    beat = abs(math.sin(math.pi * 3.0 * t))
    ang = 4.5 * math.sin(2 * math.pi * 1.5 * t)
    sc = 1.07 + 0.035 * beat
    L = np.eye(3); L[:2] = cv2.getRotationMatrix2D(FEET, ang, sc)
    L[1, 2] += -34 * beat + 16
    L[0, 2] += 22 * math.sin(2 * math.pi * 0.7 * t)
    spw = cv2.warpAffine(sp, (M @ L)[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    f = over(f, spw)
    f = rain(f, t)
    if t >= 0.4:
        u = t - 0.4; sc2 = ease_out_back(min(1, u / 0.25))
        paste_center(f, text_layer("CHẠY!!!", 190, (255, 255, 255), stroke=(200, 40, 20), sw=14, angle=7, scale=max(sc2, 0.05)), 1500, 260 + 6 * math.sin(t * 18))
    caption(f, "Còn Hideyoshi thì chạy. Chạy rất nhanh.", t, 0.4, 5.0)
    return f


LEAVES = [(random.uniform(0, W), random.uniform(-H, 0), random.uniform(120, 260), random.uniform(0.5, 1.6), random.uniform(14, 30),
           random.choice([(30, 120, 230), (40, 70, 200), (30, 180, 240), (20, 100, 180)]), random.uniform(0, 6)) for _ in range(46)]


def scene_c(t):
    z = 1.0 + 0.10 * t / 5
    breathe = 1 + 0.006 * math.sin(2 * math.pi * 0.45 * t)
    f = warp(C, cam(z * breathe, -30 * t, 5 * math.sin(t * 0.9), 0, 0))
    for x0, y0, vy, sw_, sz, col, ph in LEAVES:
        y = (y0 + vy * (t + 2)) % (H + 300) - 150; x = x0 + 70 * math.sin(sw_ * (t + ph)) + 20 * t
        cv2.ellipse(f, (int(x) % W, int(y)), (int(sz), int(sz * 0.55)), (t * 120 * sw_ + ph * 40) % 360, 0, 360, col, -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(x) % W, int(y)), (int(sz), int(sz * 0.55)), (t * 120 * sw_ + ph * 40) % 360, 0, 360, (15, 40, 90), 2, cv2.LINE_AA)
    if t >= 0.6:
        n = int(min(1, (t - 0.6) / 1.8) * len("...vẫn đang chờ..."))
        paste_center(f, text_layer("...vẫn đang chờ..."[:max(n, 1)], 120, (255, 245, 210), sw=10, scale=1.0), W / 2, 150)
    caption(f, "Ieyasu thì… ngồi đợi.", t, 0.4, 5.0)
    return f


def frame(t):
    ov = 0.3
    if t < 5 - ov / 2:
        return scene_a(t)
    if t < 5 + ov / 2:
        k = (t - (5 - ov / 2)) / ov
        return cv2.addWeighted(scene_a(min(t, 5.0)), 1 - k, scene_b(max(t - 5, 0)), k, 0)
    if t < 10 - ov / 2:
        return scene_b(t - 5)
    if t < 10 + ov / 2:
        k = (t - (10 - ov / 2)) / ov
        return cv2.addWeighted(scene_b(min(t - 5, 5.0)), 1 - k, scene_c(max(t - 10, 0)), k, 0)
    return scene_c(t - 10)


def audio(path):
    sr = 44100; n = int(sr * DUR); x = np.zeros(n)
    tt = np.arange(n) / sr

    def add(t0, sig, g=1.0):
        i = int(t0 * sr); j = min(n, i + len(sig))
        x[i:j] += g * sig[:j - i]
    # cú đóng dấu: sóng thấp + tiếng quét giấy ngắn
    d = np.arange(int(0.5 * sr)) / sr
    add(1.25, np.sin(2 * np.pi * (45 - 20 * d) * d) * np.exp(-9 * d) * 0.9 + np.sin(2 * np.pi * 110 * d) * np.exp(-14 * d) * 0.35)
    sw = np.random.randn(int(0.2 * sr)) * np.linspace(0, 1, int(0.2 * sr)) ** 2 * 0.25
    add(1.05, sw)
    d = np.arange(int(0.25 * sr)) / sr          # "bốp"
    add(2.4, (np.random.randn(len(d)) * np.exp(-30 * d) * 0.5 + np.sin(2 * np.pi * 180 * d) * np.exp(-20 * d) * 0.6))
    # mưa + bước chạy
    rn = np.random.randn(int(5 * sr)); rn = np.convolve(rn, np.ones(6) / 6, mode="same") * 0.12
    add(5.0, rn * np.minimum(1, np.arange(len(rn)) / (0.4 * sr)) * np.minimum(1, (len(rn) - np.arange(len(rn))) / (0.4 * sr)))
    for k in range(15):
        d = np.arange(int(0.12 * sr)) / sr
        add(5.1 + k / 3.0, np.sin(2 * np.pi * 95 * d) * np.exp(-30 * d) * 0.45)
    add(5.4, np.random.randn(int(0.15 * sr)) * np.exp(-np.arange(int(0.15 * sr)) / (0.03 * sr)) * 0.3)  # "chạy!!!" xuất hiện
    # chuông nhẹ + gió lá
    d = np.arange(int(2.5 * sr)) / sr
    add(10.4, (np.sin(2 * np.pi * 880 * d) * 0.25 + np.sin(2 * np.pi * 1320 * d) * 0.12) * np.exp(-2.2 * d))
    wind = np.convolve(np.random.randn(int(4.6 * sr)), np.ones(40) / 40, mode="same") * 0.05
    add(10.2, wind * np.minimum(1, np.arange(len(wind)) / (0.5 * sr)))
    x = x / max(1e-6, np.abs(x).max()) * 0.85
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    wav = OUT / "nb1_demo.wav"; mp4 = OUT / "nb1_demo_chuyen_dong.mp4"
    audio(wav)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", str(wav), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                          "-shortest", str(mp4)], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(np.ascontiguousarray(frame(i / FPS)).tobytes())
    p.stdin.close(); p.wait(); print("xong", mp4)
