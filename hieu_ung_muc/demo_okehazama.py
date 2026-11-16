"""Mô phỏng trận Okehazama bằng mã, phong cách mực: quân là bóng người, giông, mực loang. Không máu."""
import sys, subprocess, wave, numpy as np, cv2
W, H, FPS, T = 1280, 720, 24, 10.0
rng = np.random.RandomState(7)
def fractal(seed, w=W, h=H):
    r = np.random.RandomState(seed); n = np.zeros((h, w), np.float32)
    for k, a in ((6, .45), (14, .28), (30, .17), (70, .1)):
        n += a * cv2.resize(r.rand(k, int(k * w / h)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    return (n - n.min()) / (n.max() - n.min())
NZ = fractal(3); PAPER_N = fractal(5)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
# nền: giấy + núi mực
paper = np.zeros((H, W, 3), np.float32); paper[:] = (208, 231, 243)
paper *= (0.96 + 0.06 * PAPER_N[..., None])
def ridge(base, amp, seed, col, blur):
    r = np.random.RandomState(seed); p = cv2.resize(r.rand(1, 14).astype(np.float32), (W, 1), interpolation=cv2.INTER_CUBIC)[0]
    top = (base - p * amp).astype(np.float32)
    m = (yy > top[None, :].repeat(H, 0)).astype(np.float32)
    m = cv2.GaussianBlur(m, (0, 0), blur)
    return m[..., None] * np.array(col, np.float32)
bg = paper.copy()
for base, amp, seed, a, bl in ((300, 150, 11, .22, 9), (360, 110, 12, .32, 6), (410, 70, 13, .42, 3)):
    m = ridge(base, amp, seed, (1, 1, 1), bl)[..., :1]
    bg = bg * (1 - a * m) + np.array((110, 105, 100), np.float32) * a * m
gy = (yy > 470).astype(np.float32)[..., None]; gy = cv2.GaussianBlur(gy[..., 0], (0, 0), 5)[..., None]
bg = bg * (1 - .12 * gy) + np.array((150, 160, 165), np.float32) * .12 * gy
# quân
def mk(n, x0, x1, y0, y1):
    return [(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.rand()) for _ in range(n)]
IMA = mk(46, 330, 620, 505, 650)   # trại Imagawa, ngồi nghỉ
ODA = mk(56, 1250, 1500, 520, 660)  # quân Oda từ bên phải
for_scatter = [(rng.uniform(-260, -60), rng.uniform(-30, 30)) for _ in IMA]
def soldier(img, x, y, col, up=1.0, spear=True, lean=0.0, sit=False):
    s = 1.0 + (y - 480) / 330 * 1.1
    h = 40 * s * (0.62 if sit else 1.0)
    x, y = int(x), int(y)
    cv2.line(img, (x - int(5 * s), y), (x - int(5 * s) + int(lean * 4), y - int(h * .45)), col, max(1, int(5 * s)), cv2.LINE_AA)
    cv2.line(img, (x + int(5 * s), y), (x + int(5 * s) + int(lean * 4), y - int(h * .45)), col, max(1, int(5 * s)), cv2.LINE_AA)
    body = np.array([[x - 11 * s, y - h * .4], [x + 11 * s, y - h * .4], [x + 8 * s + lean * 5, y - h * .9], [x - 8 * s + lean * 5, y - h * .9]], np.int32)
    cv2.fillPoly(img, [body], col, cv2.LINE_AA)
    cv2.circle(img, (x + int(lean * 5), int(y - h * 1.0)), max(2, int(7 * s)), col, -1, cv2.LINE_AA)
    cv2.ellipse(img, (x + int(lean * 5), int(y - h * 1.08)), (int(11 * s), int(5 * s)), 0, 180, 360, col, -1, cv2.LINE_AA)  # nón
    if spear:
        cv2.line(img, (x + int(14 * s), y), (x + int(14 * s) + int(lean * 8), int(y - h * 1.9)), col, max(1, int(2 * s)), cv2.LINE_AA)
def flag(img, x, y, col, t, fall=0.0, length=95):
    top = (int(x), int(y - 190))
    ang = fall * 1.3
    p2 = (int(x + np.sin(ang) * 190), int(y - np.cos(ang) * 190))
    cv2.line(img, (int(x), int(y)), p2, (60, 70, 85), 4, cv2.LINE_AA)
    pts = [p2]
    for k in range(1, 9):
        u = k / 8; pts.append((int(p2[0] - u * length * np.cos(ang * .5) + 0), int(p2[1] + 6 * np.sin(t * 6 + u * 4) * u + u * 22 * (1 - fall))))
    pts2 = [(px, py + 46) for px, py in reversed(pts)]
    cv2.fillPoly(img, [np.array(pts + pts2, np.int32)], col, cv2.LINE_AA)
INK = (50, 48, 48); IND = (140, 100, 55); RED = (45, 45, 150)
def frame(t):
    f = bg.copy()
    storm = np.clip((t - 2.3) / 2.5, 0, 1) * (1 - np.clip((t - 8.4) / 1.6, 0, 1))
    mist = (NZ + .15 * np.sin(xx / 120 + t * .6)) ** 2
    f = f * (1 - .08 * mist[..., None]) + 240 * .08 * mist[..., None]
    lay = np.zeros_like(f) + f
    # trại Imagawa
    shake = 0
    ratio_dis = np.clip((t - 6.2) / 2.0, 0, 1)
    for i, (x, y, r) in enumerate(IMA):
        dx = for_scatter[i][0] * ratio_dis ** 1.5 * 0.6 if t > 5.6 else 0
        dy = for_scatter[i][1] * ratio_dis
        cv2.line(lay, (int(x + dx), int(y)), (int(x + dx), int(y)), IND, 1)
        soldier(lay, x + dx, y + dy, IND if ratio_dis < .5 else (110, 108, 108), sit=(t < 5.2 + r * .5), spear=(t > 5.2), lean=-1 * ratio_dis)
    for tx in (380, 520):
        tent = np.array([[tx - 70, 520], [tx + 70, 520], [tx, 440]], np.int32)
        cv2.fillPoly(lay, [tent], (150, 135, 120) if ratio_dis < .6 else (190, 190, 190), cv2.LINE_AA)
    flag(lay, 470, 520, IND, t, fall=np.clip((t - 6.8) / 1.2, 0, 1))
    # quân Oda lao vào
    adv = np.clip((t - 3.6) / 4.2, 0, 1)
    adv = adv * adv * (3 - 2 * adv) if t < 6.5 else min(1, adv)
    for x, y, r in ODA:
        xo = x - adv * 1000 - (r * 40)
        if -60 < xo < W + 60:
            soldier(lay, xo, y + 6 * np.sin(t * 9 + r * 6) * (adv > 0), INK, lean=-1.3 if adv > 0 else 0)
    flag(lay, 1180 - adv * 1000, 560, RED, t)
    # bụi mực sau quân Oda
    if adv > 0:
        m = np.clip(1 - np.abs((xx - (1250 - adv * 1000 + 120)) / 220), 0, 1) * (yy > 480)
        m = (m * (NZ > .45)).astype(np.float32)[..., None]
        lay = lay * (1 - .35 * m) + 90 * .35 * m
    f = lay
    # mực loang tại trại sau va chạm
    if t > 6.4:
        k = np.clip((t - 6.4) / 2.0, 0, 1)
        d = np.sqrt(((xx - 480) / 1.3) ** 2 + (yy - 560) ** 2) / 330 + (NZ - .5) * .45
        m = np.clip((k * 1.2 - d) * 8, 0, 1)[..., None] * (1 - np.clip((t - 8.6) / 1.2, 0, 1) * .8)
        f = f * (1 - .6 * m) + np.array((48, 46, 46), np.float32) * .6 * m * (0.6 + .4 * NZ[..., None])
    # trời tối, mưa
    f = f * (1 - .32 * storm) + np.array((110, 108, 106), np.float32) * .32 * storm
    if storm > 0:
        rain = np.zeros((H, W), np.uint8)
        rr = np.random.RandomState(int(t * 24) % 997)
        n = int(500 * storm)
        for _ in range(n):
            x0 = rr.randint(0, W); y0 = rr.randint(-40, H)
            cv2.line(rain, (x0, y0), (x0 - 14, y0 + 46), 255, 1, cv2.LINE_AA)
        f = f * (1 - .45 * (rain[..., None] / 255.)) + 235 * .45 * (rain[..., None] / 255.)
    # chớp
    fl = max(0, 1 - abs(t - 4.55) / .12) + max(0, 1 - abs(t - 5.05) / .07) * .6
    if fl > 0:
        f = f * (1 - fl * .8) + 255 * fl * .8
    # đóng khung giấy, mờ cuối
    out = np.clip(f, 0, 255)
    fade = np.clip((t - 9.2) / 0.8, 0, 1)
    out = out * (1 - fade) + paper * fade
    if t < .6: out = out * (t / .6) + paper * (1 - t / .6)
    return out
def audio(path):
    sr = 22050; n = int(T * sr); r = np.random.RandomState(1)
    t = np.arange(n) / sr; a = np.zeros(n)
    noise = r.randn(n); rain = np.convolve(noise, np.ones(8) / 8, 'same')
    env = np.clip((t - 2.3) / 2.5, 0, 1) * (1 - np.clip((t - 8.4) / 1.6, 0, 1))
    a += .18 * rain * env
    for tt, g in ((4.55, 1.0), (5.05, .6)):
        m = (t > tt) & (t < tt + 1.6); d = np.exp(-(t[m] - tt) * 2.2)
        low = np.convolve(r.randn(m.sum()), np.ones(160) / 160, 'same')
        a[m] += g * 2.5 * low * d
    for tt in np.arange(5.4, 7.6, .46):
        m = (t > tt) & (t < tt + .35); d = np.exp(-(t[m] - tt) * 14)
        a[m] += .5 * np.sin(2 * np.pi * 60 * (t[m] - tt)) * d
    a = np.clip(a / (np.abs(a).max() + 1e-9) * .85, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((a * 32767).astype(np.int16).tobytes())
out = sys.argv[1]; wav = out + '.wav'; audio(wav)
p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-i', wav, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', out], stdin=subprocess.PIPE)
for i in range(int(T * FPS)):
    p.stdin.write(frame(i / FPS).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
