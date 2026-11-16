"""Cảnh tướng đối đầu cận cảnh: quay chậm, hai vệt mực chéo, chữ K.O. Không máu."""
import sys, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
W, H, FPS, T = 1280, 720, 24, 6.5
FONT = '/home/claude/fact-video/assets/bia/fonts/'
import glob
OSW = [f for f in glob.glob(FONT + '*') if 'swald' in f][0]
def fractal(seed, w, h):
    r = np.random.RandomState(seed); n = np.zeros((h, w), np.float32)
    for k, a in ((5, .45), (12, .28), (28, .17), (60, .1)):
        n += a * cv2.resize(r.rand(k, max(2, int(k * w / h))).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    return (n - n.min()) / (n.max() - n.min())
NZ = fractal(4, W, H); yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
PAPER = np.array((208, 231, 243), np.float32)
def smooth(u): u = np.clip(u, 0, 1); return u * u * (3 - 2 * u)
def ridge(seed, base, amp, blur, a):
    r = np.random.RandomState(seed); p = cv2.resize(r.rand(1, 12).astype(np.float32), (W, 1), interpolation=cv2.INTER_CUBIC)[0]
    m = (yy > (base - p * amp)[None, :]).astype(np.float32); return cv2.GaussianBlur(m, (0, 0), blur)[..., None] * a
BG = np.zeros((H, W, 3), np.float32); BG[:] = PAPER; BG *= (.97 + .05 * NZ[..., None])
for sd, b, am, bl, a in ((21, 330, 200, 9, .25), (22, 400, 150, 5, .38), (23, 470, 90, 3, .5)):
    m = ridge(sd, b, am, bl, a); BG = BG * (1 - m) + np.array((100, 98, 95), np.float32) * m
gm = np.clip((yy - 560) / 20, 0, 1)[..., None]; BG = BG * (1 - .5 * gm) + np.array((145, 152, 156), np.float32) * .5 * gm * (.85 + .3 * NZ[..., None])
def general(img, cx, gy, s, col, face, run, t, fall=0.0, lunge=0.0):
    c = lambda x, y: (int(cx + face * x * s), int(gy - y * s))
    sw = np.sin(run) * 24 * (1 - fall)
    for lx, d in ((-18, 1), (18, -1)):
        cv2.line(img, c(lx, 0), c(lx + sw * d * .6 + 6 * lunge * face, 120), col, int(15 * s), cv2.LINE_AA)
    cv2.fillPoly(img, [np.array([c(-48, 120), c(48, 120), c(36, 280), c(-36, 280)], np.int32)], col, cv2.LINE_AA)
    for sx_ in (-52, 52):
        cv2.fillPoly(img, [np.array([c(sx_ - 22, 285), c(sx_ + 22, 285), c(sx_ + 18, 240), c(sx_ - 18, 240)], np.int32)], col, cv2.LINE_AA)
    cv2.circle(img, c(0, 318), int(30 * s), col, -1, cv2.LINE_AA)
    cv2.ellipse(img, c(0, 328), (int(46 * s), int(34 * s)), 0, 180, 360, col, -1, cv2.LINE_AA)
    cv2.line(img, c(-30, 340), c(-62, 392), col, int(7 * s), cv2.LINE_AA); cv2.line(img, c(30, 340), c(62, 392), col, int(7 * s), cv2.LINE_AA)  # sừng mũ
    cv2.ellipse(img, c(0, 355), (int(14 * s), int(10 * s)), 0, 0, 360, col, -1, cv2.LINE_AA)  # trang sức mũ
    a0 = c(30, 250); a1 = c(30 + 120 + 60 * lunge, 250 + 30 - 60 * lunge)
    cv2.line(img, a0, a1, col, int(14 * s), cv2.LINE_AA)
    tip = c(30 + 120 + 60 * lunge + 150, 250 + 30 - 60 * lunge + 80 * (1 - lunge))
    cv2.line(img, a1, tip, (200, 205, 210), max(2, int(5 * s)), cv2.LINE_AA)
def slash(img, p0, p1, k, th=34):
    n = 60
    for i in range(int(n * k)):
        u = i / n; x = p0[0] + (p1[0] - p0[0]) * u; y = p0[1] + (p1[1] - p0[1]) * u
        w = th * np.sin(np.pi * min(1, u * 1.15 + .08)) ** .6
        for j in range(3):
            cv2.circle(img, (int(x + np.sin(u * 40 + j) * 5), int(y + np.cos(u * 33 + j) * 5)), max(1, int(w * (.5 + .25 * j))), (30, 28, 28), -1, cv2.LINE_AA)
def textimg(txt, size):
    f = ImageFont.truetype(OSW, size); im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bb = d.textbbox((0, 0), txt, font=f); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((W - tw) / 2 - bb[0], (H - th) / 2 - bb[1]), txt, font=f, fill=(175, 28, 24, 255), stroke_width=10, stroke_fill=(245, 238, 225, 255))
    return im
KO = textimg('K.O.', 330)
def frame(t):
    # thời gian truyện: quay chậm 2.2-3.4
    s = t if t < 2.2 else 2.2 + .25 * (t - 2.2) if t < 3.4 else 2.5 + (t - 3.4)
    z = 1 + .55 * smooth((t - 1.4) / 2.0) + .02 * np.sin(t * 3); 
    f = BG.copy()
    lay = np.zeros((H, W, 3), np.float32) + f; lay8 = np.ascontiguousarray(np.clip(lay, 0, 255).astype(np.uint8))
    ap = smooth(s / 2.4)
    gy = 640; face_dir = 1
    xl = 200 + 260 * ap; xr = 1080 - 260 * ap
    fall = smooth((t - 3.4) / 1.4)
    lungeL = smooth((s - 1.7) / .6)
    general(lay8, xl, gy, 1.0, (140, 100, 55), 1, s * 16, t, lunge=lungeL)
    xr_ = xr + fall * 160
    general(lay8, xr_, gy + fall * 20, 1.0, (46, 44, 44), -1, s * 16, t, fall=fall, lunge=smooth((s - 1.9) / .6))
    out = lay8.astype(np.float32)
    # zoom vào điểm giữa hai tướng
    cx0 = (xl + xr) / 2; M = cv2.getRotationMatrix2D((cx0, 420), 0, z); out = cv2.warpAffine(out, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    # chớp trắng lúc chạm
    fl = max(0, 1 - abs(t - 2.75) / .1)
    out = out * (1 - fl * .9) + 255 * fl * .9
    # hai vệt mực chéo
    o8 = np.ascontiguousarray(np.clip(out, 0, 255).astype(np.uint8))
    if t > 2.8: slash(o8, (60, 40), (1230, 690), smooth((t - 2.8) / .35))
    if t > 3.05: slash(o8, (1230, 60), (50, 680), smooth((t - 3.05) / .35))
    out = o8.astype(np.float32)
    # chữ K.O. đóng xuống
    if t > 3.5:
        u = smooth((t - 3.5) / .22); sc = 1.9 - .9 * u
        im = KO.resize((int(W * sc), int(H * sc)), Image.LANCZOS)
        a = np.asarray(im).astype(np.float32); y0 = int(H / 2 - im.height / 2); x0 = int(W / 2 - im.width / 2)
        al = a[..., 3:4] / 255 * u
        y1, y2, x1, x2 = max(0, y0), min(H, y0 + im.height), max(0, x0), min(W, x0 + im.width)
        sub = al[y1 - y0:y2 - y0, x1 - x0:x2 - x0]
        out[y1:y2, x1:x2] = out[y1:y2, x1:x2] * (1 - sub) + a[y1 - y0:y2 - y0, x1 - x0:x2 - x0, :3][..., ::-1] * sub
    # rung lúc đóng chữ
    if 3.5 < t < 3.9:
        a = 18 * np.exp(-(t - 3.5) * 9); Mx = np.float32([[1, 0, np.sin(t * 90) * a], [0, 1, np.cos(t * 77) * a]]); out = cv2.warpAffine(out, Mx, (W, H), borderMode=cv2.BORDER_REFLECT)
    vg = 1 - .3 * np.clip(((xx - W / 2) / (W * .7)) ** 2 + ((yy - H / 2) / (H * .75)) ** 2, 0, 1)
    out = out * vg[..., None] + np.random.RandomState(int(t * 24)).randn(H, W, 1).astype(np.float32) * 4
    fade = smooth((t - 5.7) / .8); out = out * (1 - fade) + PAPER * fade
    if t < .3: out = out * (t / .3) + PAPER * (1 - t / .3)
    return np.clip(out, 0, 255)
if __name__ == '__main__':
    out = sys.argv[1]
    if len(sys.argv) > 2:
        for s_ in sys.argv[2:]: cv2.imwrite(f'/tmp/ko_{float(s_):04.1f}.jpg', frame(float(s_)).astype(np.uint8))
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(int(T * FPS)): p.stdin.write(frame(i / FPS).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
