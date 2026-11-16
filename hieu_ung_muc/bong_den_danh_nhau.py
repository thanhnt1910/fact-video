"""Hai võ sĩ dạng bóng đen toàn thân (rig khớp xương) đấu kiếm: giao kiếm, chém trúng, người thua rơi kiếm rồi gục, người thắng giơ kiếm lên trời. Không máu."""
import sys, math, wave, subprocess, numpy as np, cv2
from canh_ko import ridge, slash, KO, smooth, PAPER, W, H, FPS, xx, yy, NZ
from PIL import Image
T = 10.2; GROUND = 628; S = 1.12; INK = (20, 18, 20)
DEF = dict(tA=8, hA=0, thF=20, shF=-10, thB=-20, shB=-5, gx=45, gy=72, sA=40, w=0)
def keys(lst):
    out, cur = [], dict(DEF)
    for t, d in lst: cur = dict(cur); cur.update(d); out.append((t, cur))
    return out
def pose_at(K, t):
    if t <= K[0][0]: return dict(K[0][1])
    for i in range(len(K) - 1):
        a, b = K[i], K[i + 1]
        if a[0] <= t <= b[0]:
            u = smooth((t - a[0]) / max(1e-6, b[0] - a[0])); return {k: a[1][k] + (b[1][k] - a[1][k]) * u for k in a[1]}
    return dict(K[-1][1])
def xat(X, t):
    if t <= X[0][0]: return X[0][1]
    for i in range(len(X) - 1):
        a, b = X[i], X[i + 1]
        if a[0] <= t <= b[0]: return a[1] + (b[1] - a[1]) * smooth((t - a[0]) / (b[0] - a[0]))
    return X[-1][1]
# --- biên đạo (thời gian truyện). A = người thắng (trái, quay phải), B = người thua (phải, quay trái)
GUARD = dict(tA=8, thF=22, shF=-8, thB=-22, shB=-6, gx=48, gy=75, sA=38)
HIGH = dict(tA=-4, gx=14, gy=138, sA=8, thF=15, shF=-12, thB=-28, shB=-8)
CLASH = dict(tA=14, gx=58, gy=92, sA=62, thF=34, shF=-14, thB=-26, shB=-6)
KA = keys([(0, GUARD), (1.4, GUARD), (1.5, dict(w=12)), (3.0, dict(w=12)), (3.1, dict(w=0, **GUARD)), (3.15, HIGH), (3.5, CLASH), (3.75, dict(tA=2, gx=34, gy=84, sA=48, thF=18, shF=-8, thB=-24)),
           (4.15, dict(tA=-6, gx=18, gy=120, sA=20, thF=12, shF=-10, thB=-34, shB=-4)), (4.6, dict(tA=34, gx=66, gy=62, sA=108, thF=52, shF=-12, thB=-40, shB=-2)),
           (5.1, dict(tA=30, gx=62, gy=58, sA=122)), (5.7, GUARD), (6.1, dict(tA=-2, gx=8, gy=118, sA=2, thF=10, shF=-8, thB=-14, shB=-6)),
           (6.5, dict(tA=-8, hA=-10, gx=6, gy=162, sA=2, thF=8, shF=-6, thB=-12, shB=-4)), (10.0, dict(tA=-8, hA=-10, gx=6, gy=164, sA=2))])
KB = keys([(0, GUARD), (1.4, GUARD), (1.5, dict(w=12)), (3.0, dict(w=12)), (3.1, dict(w=0, **GUARD)), (3.2, HIGH), (3.5, CLASH), (3.75, dict(tA=2, gx=34, gy=84, sA=48, thF=18, shF=-8, thB=-24)),
           (4.2, dict(tA=-4, gx=22, gy=112, sA=30, thF=14, shF=-10, thB=-30)), (4.6, dict(tA=6, gx=40, gy=80, sA=70)),
           (4.95, dict(tA=-34, hA=-12, gx=-6, gy=118, sA=-60, thF=30, shF=-30, thB=-50, shB=-10)), (5.5, dict(tA=-12, hA=0, gx=-10, gy=45, sA=-110, thF=95, shF=-4, thB=-6, shB=100)),
           (6.05, dict(tA=-86, hA=-8, gx=-60, gy=40, sA=-100, thF=75, shF=20, thB=-30, shB=40)), (10.2, dict(tA=-86, hA=-8, gx=-60, gy=40, sA=-100, thF=75, shF=20, thB=-30, shB=40))])
XA = [(0, 330), (1.5, 330), (3.0, 525), (3.5, 548), (3.75, 520), (4.15, 505), (4.6, 628), (5.7, 640), (6.1, 600), (10, 600)]
XB = [(0, 960), (1.5, 960), (3.0, 760), (3.5, 735), (3.75, 770), (4.2, 770), (4.6, 770), (4.95, 835), (5.5, 880), (6.05, 925), (10.2, 925)]
DROP = 4.7; HIT = 4.6
def fig(img, root, face, P, t, colA, sword=True, horns=True, ph=0):
    p = dict(P)
    if p['w'] > 0:
        s_ = math.sin(ph); c_ = math.cos(ph)
        p['thF'] += p['w'] * s_; p['shF'] -= p['w'] * .8 * max(0, c_); p['thB'] -= p['w'] * s_; p['shB'] -= p['w'] * .8 * max(0, -c_)
    L1, L2, TL = 75, 74, 85
    ra = lambda a: math.radians(a)
    hip = np.array([0., 0.])
    sh = hip + TL * np.array([math.sin(ra(p['tA'])), math.cos(ra(p['tA']))])
    head = sh + 31 * np.array([math.sin(ra(p['tA'] + p['hA'])), math.cos(ra(p['tA'] + p['hA']))])
    kF = hip + L1 * np.array([math.sin(ra(p['thF'])), -math.cos(ra(p['thF']))]); fF = kF + L2 * np.array([math.sin(ra(p['shF'])), -math.cos(ra(p['shF']))])
    kB = hip + L1 * np.array([math.sin(ra(p['thB'])), -math.cos(ra(p['thB']))]); fB = kB + L2 * np.array([math.sin(ra(p['shB'])), -math.cos(ra(p['shB']))])
    G = np.array([p['gx'], p['gy']], float); d_ = np.array([math.sin(ra(p['sA'])), math.cos(ra(p['sA']))]); G2 = G - 20 * d_
    def ik(sp, tg, a=50, b=48):
        v = tg - sp; d = min(np.hypot(*v), a + b - 1); th = math.atan2(v[1], v[0])
        al = math.acos(np.clip((a * a + d * d - b * b) / (2 * a * d), -1, 1))
        es = [sp + a * np.array([math.cos(th + al), math.sin(th + al)]), sp + a * np.array([math.cos(th - al), math.sin(th - al)])]
        e = min(es, key=lambda q: q[1]); hnd = sp + (tg - sp) * min(1, (a + b - 1) / max(1e-6, np.hypot(*v))) if np.hypot(*v) > a + b - 1 else tg
        return e, hnd
    eF, hF = ik(sh + np.array([4, -4]), G); eB, hB = ik(sh + np.array([-8, -4]), G2)
    low = min(fF[1], fB[1], kF[1] - 6, kB[1] - 6, hF[1] - 6, hB[1] - 6, head[1] - 18, hip[1] - 14, sh[1] - 12)
    sy = -low
    def T_(q): return (int(root + face * S * q[0]), int(GROUND - S * (q[1] + sy)))
    def limb(a, b, w1, w2):
        a_, b_ = np.array(T_(a), float), np.array(T_(b), float); v = b_ - a_; n = np.array([-v[1], v[0]]) / (np.hypot(*v) + 1e-6)
        pts = np.array([a_ + n * w1 * S / 2, a_ - n * w1 * S / 2, b_ - n * w2 * S / 2, b_ + n * w2 * S / 2], np.int32)
        cv2.fillConvexPoly(img, pts, colA, cv2.LINE_AA); cv2.circle(img, tuple(b_.astype(int)), int(w2 * S / 2), colA, -1, cv2.LINE_AA)
    # bóng dưới đất
    cv2.ellipse(img, (int(root + face * S * 5), GROUND + 6), (int(70 * S), int(9 * S)), 0, 0, 360, (150, 150, 150), -1, cv2.LINE_AA)
    limb(hip, kB, 24, 18); limb(kB, fB, 17, 13); cv2.ellipse(img, T_(fB + np.array([6, 0])), (int(15 * S), int(5 * S)), 0, 0, 360, colA, -1, cv2.LINE_AA)
    limb(hip, kF, 26, 19); limb(kF, fF, 18, 13); cv2.ellipse(img, T_(fF + np.array([6, 0])), (int(15 * S), int(5 * S)), 0, 0, 360, colA, -1, cv2.LINE_AA)
    # hakama (váy) + thân
    waist = hip + np.array([0, -6]); mid = (hip + (kF + kB) / 2) + np.array([0, 4])
    cv2.fillPoly(img, [np.array([T_(waist + np.array([-23, 0])), T_(waist + np.array([23, 0])), T_(mid + np.array([34, -4])), T_(mid + np.array([-34, -4]))], np.int32)], colA, cv2.LINE_AA)
    limb(hip + np.array([0, 4]), sh, 40, 46)
    cv2.circle(img, T_(sh), int(21 * S), colA, -1, cv2.LINE_AA)
    cv2.rectangle(img, (T_(sh)[0] - int(24 * S), T_(sh)[1] - int(6 * S)), (T_(sh)[0] + int(24 * S), T_(sh)[1] + int(10 * S)), colA, -1)
    limb(sh + np.array([-8, -4]), eB, 14, 11); limb(eB, hB, 11, 9)
    cv2.circle(img, T_(head), int(17 * S), colA, -1, cv2.LINE_AA)
    hp = T_(head)
    if horns:
        cv2.ellipse(img, (hp[0], hp[1] - int(4 * S)), (int(25 * S), int(21 * S)), 0, 180, 360, colA, -1, cv2.LINE_AA)
        cv2.line(img, (hp[0] - int(6 * S), hp[1] - int(18 * S)), (hp[0] - int(28 * S), hp[1] - int(50 * S)), colA, max(2, int(5 * S)), cv2.LINE_AA)
        cv2.line(img, (hp[0] + int(6 * S), hp[1] - int(18 * S)), (hp[0] + int(30 * S), hp[1] - int(48 * S)), colA, max(2, int(5 * S)), cv2.LINE_AA)
    else:
        sw_ = math.sin(t * 6) * 4
        cv2.line(img, (hp[0] - face * int(8 * S), hp[1] - int(12 * S)), (hp[0] - face * int(34 * S), hp[1] - int((24 + sw_) * S)), colA, max(2, int(6 * S)), cv2.LINE_AA)  # búi tóc
        cv2.ellipse(img, (hp[0], hp[1] - int(8 * S)), (int(19 * S), int(15 * S)), 0, 180, 360, colA, -1, cv2.LINE_AA)
    limb(sh + np.array([4, -4]), eF, 15, 12); limb(eF, hF, 12, 10)
    if sword:
        a_, b_ = T_(G - 20 * d_), T_(G + 128 * d_)
        cv2.line(img, a_, b_, colA, max(3, int(6 * S)), cv2.LINE_AA)
        gp = T_(G + 4 * d_); cv2.line(img, (gp[0] - int(10 * S), gp[1]), (gp[0] + int(10 * S), gp[1]), colA, max(2, int(4 * S)), cv2.LINE_AA)
    return T_(G + 128 * d_), T_(G), T_(sh)
def sword_free(img, t):
    if t < DROP: return
    u = t - DROP; x0, y0 = 790.0, 380.0; vx, vy, g = 300.0, -420.0, 1700.0
    x = x0 + vx * u; y = y0 + vy * u + .5 * g * u * u; ang = 4 * u * 2.5
    if y >= GROUND: 
        tl = math.sqrt(2 * (GROUND - y0 + 0) / g) if False else None
        x, y, ang = x0 + vx * 0.95, GROUND, math.radians(-10)
    c = (math.sin(ang), -math.cos(ang))
    cv2.line(img, (int(x - c[0] * 20), int(y - c[1] * 20)), (int(x + c[0] * 120), int(y + c[1] * 120)), INK, 6, cv2.LINE_AA)
# --- nền: hoàng hôn + núi
BG = np.zeros((H, W, 3), np.float32); BG[:] = PAPER; BG *= (.97 + .05 * NZ[..., None])
dd = np.sqrt((xx - 930) ** 2 + (yy - 250) ** 2)
BG = BG * (1 - .85 * np.clip((150 - dd) / 6, 0, 1))[..., None] + np.array((70, 70, 200), np.float32) * (.85 * np.clip((150 - dd) / 6, 0, 1))[..., None]
glow = np.clip(1 - dd / 520, 0, 1)[..., None] ** 2; BG = BG * (1 - .35 * glow) + np.array((120, 150, 235), np.float32) * .35 * glow
for sd, b, am, bl, a in ((21, 360, 200, 9, .28), (22, 430, 150, 5, .42), (23, 500, 90, 3, .55)):
    m = ridge(sd, b, am, bl, a); BG = BG * (1 - m) + np.array((95, 92, 90), np.float32) * m
gm = np.clip((yy - 590) / 16, 0, 1)[..., None]; BG = BG * (1 - .6 * gm) + np.array((140, 148, 152), np.float32) * .6 * gm * (.85 + .3 * NZ[..., None])
def real2story(t): return t if t < HIT else (HIT if t < HIT + .12 else t - .12)
def frame(t):
    s = float(real2story(t))
    img = np.ascontiguousarray(np.clip(BG, 0, 255).astype(np.uint8))
    # mây trôi
    xa, xb = xat(XA, s), xat(XB, s)
    PA, PB = pose_at(KA, s), pose_at(KB, s)
    ph = s * 11
    tipA, gA, shA = fig(img, xa, 1, PA, s, INK, True, True, ph)
    tipB, gB, shB = fig(img, xb, -1, PB, s, INK, s < DROP, False, ph + 1.5)
    sword_free(img, s)
    out = img.astype(np.float32)
    # tia lửa khi hai thanh kiếm chạm
    sp = max(0, 1 - abs(s - 3.5) / .16)
    if sp > 0:
        cxp, cyp = (xa + xb) / 2 + 4, 330
        for k in range(14):
            an = k / 14 * 6.28; L1_ = 40 + 80 * sp
            cv2.line(out, (int(cxp), int(cyp)), (int(cxp + math.cos(an) * L1_), int(cyp + math.sin(an) * L1_)), (255, 255, 255), 2, cv2.LINE_AA)
        out = out * (1 - .5 * sp) + 255 * .5 * sp
    # vệt chém khi trúng
    sl = smooth((s - 4.45) / .15) * (1 - smooth((s - 4.8) / .25))
    if sl > .02 and s >= 4.45:
        ov = np.zeros((H, W), np.uint8); cxm = xb - 30
        cv2.ellipse(ov, (int(cxm), 380), (150, 120), 0, 200, 340, 255, 9, cv2.LINE_AA)
        a = (ov[..., None] / 255.) * sl; out = out * (1 - a) + 255 * a
    fl = max(0, 1 - abs(s - 4.6) / .1) * .9
    # sét khi giơ kiếm
    lt = max(0, 1 - abs(s - 6.55) / .12) + max(0, 1 - abs(s - 6.85) / .07) * .6
    if lt > 0:
        ov = np.zeros((H, W), np.uint8); px, py = 620 + int(shA[0] * 0 + (tipA[0] - 620) * 0), 0; tx_, ty_ = tipA
        pts = [(tx_ + 30, 0)]
        for k in range(1, 9): pts.append((int(tx_ + 30 - 30 * k / 8 + np.random.RandomState(k).randint(-26, 26)), int(ty_ * k / 8)))
        pts.append((tx_, ty_)); cv2.polylines(ov, [np.array(pts, np.int32)], False, 255, 5, cv2.LINE_AA)
        a = ov[..., None] / 255. * min(1, lt); out = out * (1 - a) + 255 * a; fl = max(fl, lt * .55)
    out = out * (1 - fl) + 255 * fl
    # camera
    z = 1 + .1 * smooth((s - 4.4) / .2) * (1 - smooth((s - 4.9) / .8)) + .38 * smooth((s - 6.3) / 2.8)
    cx = 640 + (xa - 640) * smooth((s - 6.3) / 2.8); cy = 420 - 40 * smooth((s - 6.3) / 2.8)
    sh_ = 0
    if 4.6 <= s < 5.0: sh_ = 14 * math.exp(-(s - 4.6) * 8)
    M = cv2.getRotationMatrix2D((cx, cy), 0, z); M[0, 2] += math.sin(t * 90) * sh_; M[1, 2] += math.cos(t * 77) * sh_
    out = cv2.warpAffine(out, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    o8 = np.ascontiguousarray(np.clip(out, 0, 255).astype(np.uint8))
    if s > 7.2: slash(o8, (60, 40), (1230, 690), smooth((s - 7.2) / .3))
    if s > 7.45: slash(o8, (1230, 60), (50, 680), smooth((s - 7.45) / .3))
    out = o8.astype(np.float32)
    if s > 7.85:
        k = smooth((s - 7.85) / .2); sc = 1.9 - .9 * k
        im = KO.resize((int(W * sc), int(H * sc)), Image.LANCZOS); a_ = np.asarray(im).astype(np.float32)
        y0 = int(H / 2 - im.height / 2); x0 = int(W / 2 - im.width / 2)
        y1, y2, x1, x2 = max(0, y0), min(H, y0 + im.height), max(0, x0), min(W, x0 + im.width)
        al = a_[y1 - y0:y2 - y0, x1 - x0:x2 - x0, 3:4] / 255 * k
        out[y1:y2, x1:x2] = out[y1:y2, x1:x2] * (1 - al) + a_[y1 - y0:y2 - y0, x1 - x0:x2 - x0, :3][..., ::-1] * al
        if s < 8.25:
            a2 = 16 * math.exp(-(s - 7.85) * 9); Mx = np.float32([[1, 0, math.sin(t * 90) * a2], [0, 1, math.cos(t * 77) * a2]]); out = cv2.warpAffine(out, Mx, (W, H), borderMode=cv2.BORDER_REFLECT)
    vg = 1 - .3 * np.clip(((xx - W / 2) / (W * .7)) ** 2 + ((yy - H / 2) / (H * .75)) ** 2, 0, 1)
    out = out * vg[..., None] + np.random.RandomState(int(t * 24)).randn(H, W, 1).astype(np.float32) * 4
    fade = smooth((t - 9.5) / .7); out = out * (1 - fade) + PAPER * fade
    if t < .4: out = out * (t / .4) + PAPER * (1 - t / .4)
    return np.clip(out, 0, 255)
def audio(path):
    sr = 22050; n = int(T * sr); r = np.random.RandomState(2); a = np.zeros(n)
    def put(tt, sig, g=1.0):
        i = int(tt * sr); sig = sig[:max(0, n - i)]; a[i:i + len(sig)] += g * sig
    def whoosh(d=.35):
        m = int(d * sr); x = np.convolve(r.randn(m), np.ones(40) / 40, 'same') * np.sin(np.linspace(0, np.pi, m)) ** 1.5; return x * 1.2
    def clang():
        m = int(.9 * sr); t_ = np.arange(m) / sr; return (np.sin(2 * np.pi * 1760 * t_) + .7 * np.sin(2 * np.pi * 2637 * t_) + .5 * np.sin(2 * np.pi * 3520 * t_) + .3 * r.randn(m)) * np.exp(-t_ * 7)
    def thud(f=70, d=.5):
        m = int(d * sr); t_ = np.arange(m) / sr; return np.sin(2 * np.pi * f * t_) * np.exp(-t_ * 9) * 1.4 + np.convolve(r.randn(m), np.ones(30) / 30, 'same') * np.exp(-t_ * 14)
    s2r = lambda s_: s_ if s_ < HIT else s_ + .12
    for tt in (3.0, 4.2): put(s2r(tt), whoosh(.4), .5)
    put(s2r(3.5), clang(), .8); put(s2r(3.5), whoosh(.2), .4)
    put(s2r(4.6), thud(90, .5), 1.1); put(s2r(4.6), clang(), .3)
    put(s2r(5.95), thud(60, .6), .9); put(s2r(5.45), thud(75, .4), .5)
    put(s2r(4.7 + .95), thud(300, .1), .3)
    m = int(1.8 * sr); th = np.convolve(r.randn(m), np.ones(160) / 160, 'same') * np.exp(-np.arange(m) / sr * 1.8) * 2.4; put(s2r(6.55), th, 1.0)
    a = np.clip(a / (np.abs(a).max() + 1e-9) * .85, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((a * 32767).astype(np.int16).tobytes())
if __name__ == '__main__':
    out = sys.argv[1]
    if len(sys.argv) > 2:
        for s_ in sys.argv[2:]: cv2.imwrite(f'/tmp/bd_{float(s_):04.1f}.jpg', frame(float(s_)).astype(np.uint8))
        sys.exit()
    wav = out + '.wav'; audio(wav)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', wav, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', out], stdin=subprocess.PIPE)
    for i in range(int(T * FPS)): p.stdin.write(frame(i / FPS).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
