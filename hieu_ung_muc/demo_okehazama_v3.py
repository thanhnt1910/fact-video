"""Okehazama v2: quân đông hành quân, camera chạy theo, giông bão, xung phong, mực loang. Không máu, không chữ."""
import sys, subprocess, wave, numpy as np, cv2
W, H, FPS, T = 1280, 720, 24, 20.0
def fractal(seed, w, h):
    r = np.random.RandomState(seed); n = np.zeros((h, w), np.float32)
    for k, a in ((5, .45), (12, .28), (28, .17), (60, .1)):
        n += a * cv2.resize(r.rand(k, max(2, int(k * w / h))).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    return (n - n.min()) / (n.max() - n.min())
WW = 6400
NZ = fractal(3, W, H); GN = fractal(9, WW, 260)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
PAPER = np.array((208, 231, 243), np.float32)
def ridge_layer(seed, base, amp, blur, a, col):
    r = np.random.RandomState(seed); p = cv2.resize(r.rand(1, 40).astype(np.float32), (WW, 1), interpolation=cv2.INTER_CUBIC)[0]
    top = base - p * amp
    y = np.arange(H)[:, None]; m = (y > top[None, :]).astype(np.float32)
    m = cv2.GaussianBlur(m, (0, 0), blur) * a
    return m[..., None], np.array(col, np.float32)
LAY = [(ridge_layer(11, 300, 190, 10, .22, (125, 122, 118)), .12), (ridge_layer(12, 360, 150, 6, .34, (105, 102, 98)), .25), (ridge_layer(13, 430, 100, 3, .5, (90, 88, 84)), .45)]
def smooth(u): u = np.clip(u, 0, 1); return u * u * (3 - 2 * u)
# --- quân
rng = np.random.RandomState(7)
BLUE = (140, 100, 55); BLUE2 = (115, 110, 110); INK = (46, 44, 44); RED = (45, 45, 150)
IMA = []
for i in range(330):
    row = i // 6; col = i % 6
    tx = 2380 + rng.uniform(0, 640); ty = rng.uniform(535, 660)
    IMA.append(dict(tx=tx, ty=ty, D=700 + row * 38 + rng.uniform(0, 30), ph=rng.rand() * 6.28, ban=rng.rand() < .14, sc=rng.uniform(-260, -40), sy=rng.uniform(-40, 50), r=rng.rand()))
ODA = []
for i in range(150):
    ODA.append(dict(wave=i % 5 >= 3, x0=4500 + rng.uniform(0, 520), ty=rng.uniform(540, 655), ph=rng.rand() * 6.28, ban=rng.rand() < .2, r=rng.rand(), tx=2560 + rng.uniform(0, 380)))
# camera
KF = [(0, 700, 560, .55), (5.9, 2300, 560, .6), (6.1, 3500, 560, .72), (8.2, 3600, 570, .9), (11.2, 2900, 575, .95), (12.3, 2760, 570, .8), (13.2, 2760, 545, .85), (15.6, 2735, 505, 1.7), (16.6, 2735, 505, 1.7)]
def camera(t):
    for i in range(len(KF) - 1):
        a, b = KF[i], KF[i + 1]
        if a[0] <= t <= b[0]:
            u = smooth((t - a[0]) / (b[0] - a[0])); return tuple(a[k] + (b[k] - a[k]) * u for k in (1, 2, 3))
    return KF[-1][1:]
def soldier(img, sx, sy, s, col, phase, run=False, ban=None, sit=False, lean=0.0, t=0):
    h = 40 * s * (0.6 if sit else 1.0)
    sw = np.sin(phase) * (11 if run else 6) * s
    x, y = int(sx), int(sy)
    if not sit:
        cv2.line(img, (x - int(4 * s), y), (x - int(4 * s) + int(sw), y - int(h * .45)), col, max(1, int(4 * s)), cv2.LINE_AA)
        cv2.line(img, (x + int(4 * s), y), (x + int(4 * s) - int(sw), y - int(h * .45)), col, max(1, int(4 * s)), cv2.LINE_AA)
    bob = int(abs(np.sin(phase)) * 3 * s) if not sit else 0
    y -= bob; L = lean * 6 * s
    body = np.array([[x - 10 * s, y - h * .4], [x + 10 * s, y - h * .4], [x + 7 * s + L, y - h * .9], [x - 7 * s + L, y - h * .9]], np.int32)
    cv2.fillPoly(img, [body], col, cv2.LINE_AA)
    cv2.circle(img, (int(x + L), int(y - h * 1.0)), max(2, int(6 * s)), col, -1, cv2.LINE_AA)
    cv2.ellipse(img, (int(x + L), int(y - h * 1.07)), (int(10 * s), int(4 * s)), 0, 180, 360, col, -1, cv2.LINE_AA)
    if not sit:
        cv2.line(img, (x + int(12 * s), y), (x + int(12 * s) + int(L * 1.4), int(y - h * 1.85)), col, max(1, int(2 * s)), cv2.LINE_AA)
    if ban is not None:
        px, py = int(x - 9 * s - L * .3), int(y - h * 1.0)
        top = int(py - 62 * s)
        cv2.line(img, (px, py), (px, top), (50, 55, 70), max(1, int(2 * s)), cv2.LINE_AA)
        wv = 5 * s * np.sin(t * 7 + phase)
        pts = np.array([[px, top], [px - 15 * s + wv, top + 2], [px - 15 * s + wv * 1.4, top + 46 * s], [px, top + 46 * s]], np.int32)
        cv2.fillPoly(img, [pts], ban, cv2.LINE_AA)
def remap(t):
    t = np.asarray(t, dtype=float)
    a, b = 11.0, 14.4  # đoạn quay chậm (thời gian video), tốc độ truyện 0.35
    return np.where(t < a, t, np.where(t < b, a + .35 * (t - a), a + .35 * (b - a) + (t - b)))
def frame(tv):
    t = float(remap(tv))
    cx, cy, z = camera(t)
    storm = smooth((t - 7.8) / 2.0) * (1 - smooth((t - 14.0) / 2.0))
    # trời + núi (parallax)
    f = np.zeros((H, W, 3), np.float32); f[:] = PAPER
    f *= (0.97 + .05 * NZ[..., None])
    for ((m, col), par) in LAY:
        off = int(cx * par) % (WW - W); mm = m[:, off:off + W]
        f = f * (1 - mm) + col * mm
    hor = int(H * .62 - (cy - 520) * z * .35)
    # nền đất: dải mực loãng cuộn theo camera
    off = int(cx * z * .5) % (WW - W)
    gtex = GN[:, off:off + W]
    gm = np.clip((yy - hor) / 14, 0, 1)[..., None]
    f = f * (1 - .55 * gm) + np.array((150, 158, 162), np.float32) * .55 * gm * (0.85 + .3 * cv2.resize(gtex, (W, H))[..., None])
    mist = (NZ + .15 * np.sin(xx / 120 + t * .6)) ** 2
    f = f * (1 - .07 * mist[..., None]) + 240 * .07 * mist[..., None]
    lay = f
    def toscr(wx, wy):
        s = (0.8 + (wy - 500) / 200 * .55) * z
        return (wx - cx) * z + W / 2, hor + (wy - 520) * z * 1.15 + 60 * z, s
    items = []
    pm = smooth(t / 5.8); clash = smooth((t - 11.4) / 2.2)
    for q in IMA:
        walking = pm < 1
        x = q['tx'] - (1 - pm) * q['D'] * 3.2 + q['sc'] * clash ** 1.4 * .6
        y = q['ty'] + q['sy'] * clash
        sit = (not walking) and t < 8 + q['r'] * 2.5
        col = BLUE if clash < .5 else BLUE2
        items.append((y, 'b', x, y, q, walking, sit, col, clash))
    oa = smooth((t - 6.0) / 5.4)
    for q in ODA:
        if t < 6.0: continue
        oq = smooth((t - 6.0 - (1.3 if q['wave'] else 0)) / (5.4 - (.3 if q['wave'] else 0)))
        x = q['x0'] - oq * (q['x0'] - q['tx']) + (clash * 120 if clash > 0 else 0)
        items.append((q['ty'], 'o', x, q['ty'], q, oq < 1, False, INK, clash))
    items.sort(key=lambda a: a[0])
    # lều
    for tx_ in (2500, 2700, 2900):
        sx, sy, s = toscr(tx_, 545)
        tent = np.array([[sx - 80 * s, sy], [sx + 80 * s, sy], [sx, sy - 85 * s]], np.int32)
        cv2.fillPoly(lay, [tent], (150, 135, 120) if clash < .6 else (190, 190, 190), cv2.LINE_AA)
    for (_, kind, x, y, q, mv, sit, col, cl) in items:
        sx, sy, s = toscr(x, y)
        if sx < -60 or sx > W + 60: continue
        run = kind == 'o'
        ph = q['ph'] + t * (13 if run else 7) if mv else q['ph']
        soldier(lay, sx, sy, s, col, ph, run=run and mv, ban=((BLUE if cl < .5 else BLUE2) if kind == 'b' else RED) if q['ban'] else None, sit=sit, lean=-1.1 if (run and mv) else (-cl if kind == 'b' else 0), t=t)
    # cờ lớn của hai bên
    def bigflag(wx, col, fall=0):
        sx, sy, s = toscr(wx, 540)
        ang = fall * 1.3
        p2 = (int(sx + np.sin(ang) * 200 * s), int(sy - np.cos(ang) * 200 * s))
        cv2.line(lay, (int(sx), int(sy)), p2, (60, 70, 85), max(2, int(4 * s)), cv2.LINE_AA)
        pts = [p2]
        for k in range(1, 9):
            u = k / 8; pts.append((int(p2[0] - u * 100 * s), int(p2[1] + 8 * s * np.sin(t * 6 + u * 4) * u + u * 22 * s * (1 - fall))))
        pts2 = [(px, py + int(48 * s)) for px, py in reversed(pts)]
        cv2.fillPoly(lay, [np.array(pts + pts2, np.int32)], col, cv2.LINE_AA)
    bigflag(2740, BLUE if clash < .5 else BLUE2, fall=smooth((t - 12.4) / 1.4))
    if t >= 6.0:
        bigflag(q_x := (4560 - oa * (4560 - 2640)), RED)
    # bụi sau quân Oda
    if 6.2 < t < 12.5:
        d = np.zeros((H, W), np.uint8)
        for k in range(26):
            wx = 4500 - oa * (4500 - 2560) + 60 + k * 26 + (k % 3) * 10
            sx, sy, s = toscr(wx, 590 + (k * 37) % 90)
            cv2.circle(d, (int(sx), int(sy - 8 * s)), int(26 * s + (k % 5) * 6 * s), 255, -1, cv2.LINE_AA)
        d = cv2.GaussianBlur(d, (0, 0), 14 * z).astype(np.float32)[..., None] / 255 * (0.5 if t < 11.5 else .5 * (1 - smooth((t - 11.5) / 1))) * (NZ[..., None] > .38)
        lay = lay * (1 - d * .6) + 110 * d * .6
    f = lay
    # mực loang tại trại
    if t > 11.6:
        sx, sy, s = toscr(2740, 590)
        k = smooth((t - 11.6) / 2.4)
        dd = np.sqrt(((xx - sx) / 1.3) ** 2 + (yy - sy) ** 2) / (330 * z) + (NZ - .5) * .5
        m = np.clip((k * 1.15 - dd) * 7, 0, 1)[..., None] * (1 - smooth((t - 14.4) / 1.6) * .8)
        f = f * (1 - .55 * m) + np.array((46, 44, 44), np.float32) * .55 * m * (0.6 + .4 * NZ[..., None])
    # lửa trại + khói (trước giông)
    fire = np.clip(1 - storm * 1.6, 0, 1) * (1 - clash)
    if fire > 0.02:
        glow = np.zeros((H, W), np.float32)
        for i_, fx in enumerate((2450, 2640, 2840, 3000)):
            sx, sy, s = toscr(fx, 600 + (i_ % 2) * 25)
            fl_ = .75 + .25 * np.sin(t * 17 + i_ * 2.1) * np.sin(t * 11 + i_)
            cv2.circle(glow, (int(sx), int(sy - 10 * s)), int(70 * s * fl_), 1.0, -1, cv2.LINE_AA)
            for k in range(6):
                u = ((t * .6 + k / 6 + i_ * .13) % 1.0)
                cv2.circle(lay, (int(sx + np.sin(u * 5 + k) * 10 * s + u * 30), int(sy - 20 * s - u * 130 * s)), int((4 + u * 11) * s), (150, 150, 150), -1, cv2.LINE_AA)
        glow = cv2.GaussianBlur(glow, (0, 0), 28)[..., None] * .55 * fire
        f = f + glow * np.array((30, 110, 210), np.float32)
        f = np.clip(f, 0, 255)
    # đường tốc độ lúc xung phong
    sp = smooth((t - 8.2) / .8) * (1 - smooth((t - 11.2) / .5))
    if sp > .02:
        sl = np.zeros((H, W), np.uint8); r_ = np.random.RandomState(int(t * 24) % 211)
        for _ in range(int(40 * sp)):
            y0 = r_.randint(int(H * .4), H); x0 = r_.randint(0, W); L_ = r_.randint(120, 420)
            cv2.line(sl, (x0, y0), (x0 + L_, y0), 255, 1, cv2.LINE_AA)
        f = f * (1 - .28 * sl[..., None] / 255.) + 230 * .28 * sl[..., None] / 255.
    # lá và bụi bay theo gió
    r2 = np.random.RandomState(5)
    for k in range(70):
        bx = r2.uniform(0, W * 2); by = r2.uniform(H * .25, H * .95); spd = r2.uniform(60, 190)
        x_ = (bx - (t * spd)) % (W + 80) - 40; y_ = by + np.sin(t * 2 + k) * 14
        c_ = (95, 100, 105)
        cv2.ellipse(f, (int(x_), int(y_)), (int(2 + k % 2), 1), (t * 90 + k * 30) % 180, 0, 360, c_, -1, cv2.LINE_AA)
    # sóng mực khi va chạm
    if 11.4 < t < 13.4:
        sx, sy, s = toscr(2740, 585); u = (t - 11.4) / 2.0
        ring = np.abs(np.sqrt(((xx - sx) / 1.0) ** 2 + ((yy - sy) * 1.7) ** 2) - u * 640 * z)
        ra = np.clip(1 - ring / (14 + 18 * u), 0, 1) * (1 - u) * (.6 + .4 * NZ)
        f = f * (1 - .55 * ra[..., None]) + np.array((40, 38, 38), np.float32) * .55 * ra[..., None]
    # giông
    f = f * (1 - .38 * storm) + np.array((98, 96, 94), np.float32) * .38 * storm
    if storm > 0:
        rain = np.zeros((H, W), np.uint8); rr = np.random.RandomState(int(t * 24) % 997)
        for _ in range(int(650 * storm)):
            x0 = rr.randint(0, W + 60); y0 = rr.randint(-40, H)
            cv2.line(rain, (x0, y0), (x0 - 18, y0 + 56), 255, 1, cv2.LINE_AA)
        a = (rain[..., None] / 255.) * .5; f = f * (1 - a) + 235 * a
    fl = max(0, 1 - abs(t - 9.9) / .1) + max(0, 1 - abs(t - 10.3) / .06) * .6 + max(0, 1 - abs(t - 11.3) / .12)
    if fl > 0: f = f * (1 - fl * .8) + 255 * fl * .8
    # chuyển cảnh mực loang (5.5-6.5)
    k_ = max(0, 1 - abs(t - 6.0) / .55)
    if k_ > 0:
        mk = np.clip((smooth(k_) * 1.5 - NZ) * 9, 0, 1)[..., None]
        f = f * (1 - mk) + np.array((38, 36, 36), np.float32) * mk
    # vignette + hạt phim
    vg = 1 - .30 * np.clip(((xx - W / 2) / (W * .7)) ** 2 + ((yy - H / 2) / (H * .75)) ** 2, 0, 1)
    f = f * vg[..., None]
    f = f + (np.random.RandomState(int(tv * 24) % 1000).randn(H, W, 1).astype(np.float32) * 4)
    # rung khi va chạm
    out = np.clip(f, 0, 255)
    if 11.4 < t < 12.6:
        a = 16 * np.exp(-(t - 11.4) * 3.0); M = np.float32([[1, 0, np.sin(t * 70) * a], [0, 1, np.cos(t * 83) * a]])
        out = cv2.warpAffine(out, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    fade = smooth((tv - 18.6) / 1.3)
    out = out * (1 - fade) + PAPER * fade
    if tv < .5: out = out * (tv / .5) + PAPER * (1 - t / .5)
    return out
def audio(path):
    sr = 22050; n = int(T * sr); r = np.random.RandomState(1); t = np.arange(n) / sr; a = np.zeros(n)
    rain = np.convolve(r.randn(n), np.ones(8) / 8, 'same')
    ts = remap(t); env = smooth((ts - 7.8) / 2.0) * (1 - smooth((ts - 14) / 2.0)); a += .2 * rain * env
    for tt, g in ((9.9, 1.0), (10.3, .6), (11.86, 1.0)):
        m = (t > tt) & (t < tt + 1.8); d = np.exp(-(t[m] - tt) * 2.0)
        a[m] += g * 2.6 * np.convolve(r.randn(m.sum()), np.ones(160) / 160, 'same') * d
    for tt in np.arange(1.0, 12.0, .62 if True else 1):  # trống hành quân, dồn dập dần
        step = max(.28, .62 - .03 * tt)
    tt = 1.0
    while tt < 12.1:
        m = (t > tt) & (t < tt + .4); d = np.exp(-(t[m] - tt) * 11)
        a[m] += (.35 + .35 * min(1, tt / 10)) * np.sin(2 * np.pi * 55 * (t[m] - tt)) * d
        tt += max(.3, .66 - .04 * tt)
    m = (t > 12.14) & (t < 16.5); noise = np.convolve(r.randn(m.sum()), np.ones(10) / 10, 'same')
    a[m] += 1.1 * noise * np.exp(-(t[m] - 12.14) * .9)
    a = np.clip(a / (np.abs(a).max() + 1e-9) * .85, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((a * 32767).astype(np.int16).tobytes())
if __name__ == '__main__':
    out = sys.argv[1]
    if len(sys.argv) > 2:
        for s in sys.argv[2:]:
            cv2.imwrite(f'/tmp/v2_{float(s):05.2f}.jpg', frame(float(s)).astype(np.uint8)); 
        sys.exit()
    wav = out + '.wav'; audio(wav)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', wav, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', out], stdin=subprocess.PIPE)
    for i in range(int(T * FPS)): p.stdin.write(frame(i / FPS).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
