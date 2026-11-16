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
GUARD = dict(tA=10, thF=40, shF=-20, thB=-34, shB=-14, gx=50, gy=78, sA=40)
HIGH = dict(tA=-4, gx=14, gy=138, sA=8, thF=15, shF=-12, thB=-28, shB=-8)
CLASH = dict(tA=14, gx=58, gy=92, sA=62, thF=34, shF=-14, thB=-26, shB=-6)
KA = keys([(0, GUARD), (1.4, GUARD), (1.5, dict(w=12)), (3.0, dict(w=12)), (3.1, dict(w=0, **GUARD)), (3.15, HIGH), (3.5, CLASH), (3.75, dict(tA=2, gx=34, gy=84, sA=48, thF=18, shF=-8, thB=-24)),
           (4.15, dict(tA=-6, gx=18, gy=120, sA=20, thF=12, shF=-10, thB=-34, shB=-4)), (4.6, dict(tA=34, gx=66, gy=62, sA=108, thF=52, shF=-12, thB=-40, shB=-2)),
           (5.1, dict(tA=30, gx=62, gy=58, sA=122)), (5.7, GUARD), (6.1, dict(tA=0, gx=26, gy=124, sA=6, thF=20, shF=-12, thB=-20, shB=-8)),
           (6.5, dict(tA=-6, hA=-12, gx=30, gy=166, sA=8, thF=26, shF=-14, thB=-26, shB=-10)), (10.0, dict(tA=-6, hA=-12, gx=30, gy=168, sA=8))])
KB = keys([(0, GUARD), (1.4, GUARD), (1.5, dict(w=12)), (3.0, dict(w=12)), (3.1, dict(w=0, **GUARD)), (3.2, HIGH), (3.5, CLASH), (3.75, dict(tA=2, gx=34, gy=84, sA=48, thF=18, shF=-8, thB=-24)),
           (4.2, dict(tA=-4, gx=22, gy=112, sA=30, thF=14, shF=-10, thB=-30)), (4.6, dict(tA=6, gx=40, gy=80, sA=70)),
           (4.95, dict(tA=-34, hA=-12, gx=-6, gy=118, sA=-60, thF=30, shF=-30, thB=-50, shB=-10)), (5.5, dict(tA=-14, hA=0, gx=-14, gy=50, sA=-110, thF=72, shF=-2, thB=-8, shB=98)),
           (6.05, dict(tA=-88, hA=-6, gx=-62, gy=14, sA=-95, thF=82, shF=88, thB=76, shB=84)), (10.2, dict(tA=-88, hA=-6, gx=-62, gy=14, sA=-95, thF=82, shF=88, thB=76, shB=84))])
XA = [(0, 330), (1.5, 330), (3.0, 525), (3.5, 548), (3.75, 520), (4.15, 505), (4.6, 628), (5.7, 640), (6.1, 600), (10, 600)]
XB = [(0, 960), (1.5, 960), (3.0, 760), (3.5, 735), (3.75, 770), (4.2, 770), (4.6, 770), (4.95, 835), (5.5, 880), (6.05, 925), (10.2, 925)]
DROP = 4.7; HIT = 4.6
K = 2  # siêu mẫu
def cap(m, p, q, w1, w2):
    a_, b_ = np.array(p, float), np.array(q, float); v = b_ - a_; n = np.array([-v[1], v[0]]) / (np.hypot(*v) + 1e-6)
    cv2.fillConvexPoly(m, np.array([a_ + n * w1 / 2, a_ - n * w1 / 2, b_ - n * w2 / 2, b_ + n * w2 / 2], np.int32), 255, cv2.LINE_AA)
    cv2.circle(m, tuple(a_.astype(int)), int(w1 / 2), 255, -1, cv2.LINE_AA); cv2.circle(m, tuple(b_.astype(int)), int(w2 / 2), 255, -1, cv2.LINE_AA)
def curve(m, pts, w0, w1):
    n = len(pts)
    for i in range(n - 1): cap(m, pts[i], pts[i + 1], w0 + (w1 - w0) * i / (n - 1), w0 + (w1 - w0) * (i + 1) / (n - 1))
def fig(m, root, face, P, t, sword=True, horns=True, ph=0):
    p = dict(P)
    if p['w'] > 0:
        s_ = math.sin(ph); c_ = math.cos(ph)
        p['thF'] += p['w'] * s_; p['shF'] -= p['w'] * .8 * max(0, c_); p['thB'] -= p['w'] * s_; p['shB'] -= p['w'] * .8 * max(0, -c_)
    p['tA'] += 1.6 * math.sin(t * 3.1) + (1.2 * math.sin(ph * 2) if p['w'] > 0 else 0)  # thở và nhún bước
    L1, L2, TL = 75, 74, 85
    ra = math.radians
    hip = np.array([0., 0.])
    sh = hip + TL * np.array([math.sin(ra(p['tA'])), math.cos(ra(p['tA']))])
    head = sh + 30 * np.array([math.sin(ra(p['tA'] + p['hA'])), math.cos(ra(p['tA'] + p['hA']))])
    kF = hip + L1 * np.array([math.sin(ra(p['thF'])), -math.cos(ra(p['thF']))]); fF = kF + L2 * np.array([math.sin(ra(p['shF'])), -math.cos(ra(p['shF']))])
    kB = hip + L1 * np.array([math.sin(ra(p['thB'])), -math.cos(ra(p['thB']))]); fB = kB + L2 * np.array([math.sin(ra(p['shB'])), -math.cos(ra(p['shB']))])
    G = np.array([p['gx'], p['gy']], float); d_ = np.array([math.sin(ra(p['sA'])), math.cos(ra(p['sA']))]); G2 = G - 22 * d_
    def ik(sp, tg, a=50, b=48):
        v = tg - sp; dist = np.hypot(*v); d = min(dist, a + b - 1); th = math.atan2(v[1], v[0])
        al = math.acos(np.clip((a * a + d * d - b * b) / (2 * a * d), -1, 1))
        es = [sp + a * np.array([math.cos(th + al), math.sin(th + al)]), sp + a * np.array([math.cos(th - al), math.sin(th - al)])]
        e = min(es, key=lambda q: q[1]); hnd = sp + (tg - sp) * ((a + b - 1) / dist) if dist > a + b - 1 else tg
        return e, hnd
    shF_ = sh + np.array([5, -5]); shB_ = sh + np.array([-9, -5])
    eF, hF = ik(shF_, G); eB, hB = ik(shB_, G2)
    low = min(fF[1], fB[1], kF[1] - 7, kB[1] - 7, hF[1] - 6, hB[1] - 6, head[1] - 18, hip[1] - 16, sh[1] - 14)
    sy = -low
    def T_(q): return (int(K * (root + face * S * q[0])), int(K * (GROUND - S * (q[1] + sy))))
    k = K * S
    # chân
    cap(m, T_(hip), T_(kB), 25 * k, 17 * k); cap(m, T_(kB), T_(fB), 16 * k, 11 * k); cv2.ellipse(m, T_(fB + np.array([7, -1])), (int(14 * k), int(5 * k)), 0, 0, 360, 255, -1, cv2.LINE_AA)
    cap(m, T_(hip), T_(kF), 27 * k, 18 * k); cap(m, T_(kF), T_(fF), 17 * k, 11 * k); cv2.ellipse(m, T_(fF + np.array([7, -1])), (int(14 * k), int(5 * k)), 0, 0, 360, 255, -1, cv2.LINE_AA)
    # hakama: váy xòe
    wob = math.sin(t * 5 + ph * .3) * 3
    hemc = (kF + kB) / 2 + np.array([0, -22]); wa = hip + np.array([0, -4])
    poly = [wa + np.array([-21, 4]), wa + np.array([21, 4]), wa + np.array([26, -26]), hemc + np.array([41 + wob, 8]), hemc + np.array([20, -4 + wob]), hemc + np.array([-20, -4 - wob]), hemc + np.array([-41 - wob, 8]), wa + np.array([-26, -26])]
    cv2.fillPoly(m, [np.array([T_(q) for q in poly], np.int32)], 255, cv2.LINE_AA)
    # thân kimono: ngực rộng, eo thon
    ax = np.array([math.sin(ra(p['tA'])), math.cos(ra(p['tA']))]); nx = np.array([ax[1], -ax[0]])
    def at(u, w): return hip + ax * (TL * u) + nx * w
    torso = [at(0, -19), at(0, 19), at(.35, 17), at(.8, 27), at(1.0, 22), at(1.0, -22), at(.8, -27), at(.35, -17)]
    cv2.fillPoly(m, [np.array([T_(q) for q in torso], np.int32)], 255, cv2.LINE_AA)
    # obi + đuôi dây lưng
    for sgn, ln in ((-1, 30), (1, 22)):
        a0 = hip + np.array([-12, 2]); cv2.line(m, T_(a0), T_(a0 + np.array([-ln - math.sin(t * 6 + sgn) * 7, -18 + sgn * 5 + math.sin(t * 5) * 4])), 255, max(2, int(5 * k)), cv2.LINE_AA)
    cv2.circle(m, T_(sh + np.array([0, -2])), int(23 * k), 255, -1, cv2.LINE_AA)  # vai
    cap(m, T_(sh + np.array([0, 3])), T_(head - (head - sh) * .5), 15 * k, 12 * k)  # cổ
    # tay sau + ống tay áo
    cap(m, T_(shB_), T_(eB), 15 * k, 12 * k); cap(m, T_(eB), T_(hB), 12 * k, 9 * k)
    cv2.fillPoly(m, [np.array([T_(eB + np.array([0, 4])), T_(eB + np.array([-6, -22 + math.sin(t * 7) * 4])), T_(eB + np.array([18, -20])), T_(eB + np.array([14, 2]))], np.int32)], 255, cv2.LINE_AA)
    # đầu
    hp = T_(head); hr = int(16.5 * k)
    cv2.circle(m, hp, hr, 255, -1, cv2.LINE_AA)
    if horns:
        cv2.ellipse(m, (hp[0], hp[1] - int(4 * k)), (int(24 * k), int(20 * k)), 0, 180, 360, 255, -1, cv2.LINE_AA)  # mũ trụ
        cv2.rectangle(m, (hp[0] - int(26 * k), hp[1] - int(5 * k)), (hp[0] + int(26 * k), hp[1] + int(1 * k)), 255, -1)
        for sg in (-1, 1):
            pts = [(hp[0] + sg * int((8 + 24 * u + 14 * u * u) * k), hp[1] - int((18 + 44 * u - 18 * u * u) * k)) for u in np.linspace(0, 1, 9)]
            curve(m, pts, 6.5 * k, 1.8 * k)
        cv2.circle(m, (hp[0], hp[1] - int(24 * k)), int(5 * k), 255, -1, cv2.LINE_AA)
        cv2.fillPoly(m, [np.array([(hp[0] - int(22 * k), hp[1] + int(2 * k)), (hp[0] - int(28 * k), hp[1] + int(20 * k)), (hp[0] - int(14 * k), hp[1] + int(6 * k))], np.int32)], 255, cv2.LINE_AA)  # giáp che gáy
    else:
        cv2.ellipse(m, (hp[0], hp[1] - int(6 * k)), (int(18 * k), int(15 * k)), 0, 180, 360, 255, -1, cv2.LINE_AA)
        bun = (hp[0] - face * int(6 * k), hp[1] - int(22 * k)); cv2.circle(m, bun, int(7 * k), 255, -1, cv2.LINE_AA)
        tail = [(hp[0] - face * int((14 + 10 * u) * k), hp[1] - int((16 - 12 * u + 5 * math.sin(t * 6 + u * 3)) * k)) for u in np.linspace(0, 1, 7)]
        curve(m, tail, 6 * k, 2 * k)
    # tay trước + tay áo
    cap(m, T_(shF_), T_(eF), 16 * k, 13 * k); cap(m, T_(eF), T_(hF), 13 * k, 9.5 * k)
    cv2.fillPoly(m, [np.array([T_(eF + np.array([0, 4])), T_(eF + np.array([-6, -24 + math.sin(t * 8) * 4])), T_(eF + np.array([20, -22])), T_(eF + np.array([15, 2]))], np.int32)], 255, cv2.LINE_AA)
    if sword:
        n_ = np.array([d_[1], -d_[0]])
        pts = [G - 24 * d_] + [G + (14 + 118 * u) * d_ + n_ * (7 * 4 * u * (1 - u) * -1) for u in np.linspace(0, 1, 14)]
        curve(m, [T_(q) for q in pts[:3]], 6 * k, 6 * k); curve(m, [T_(q) for q in pts[2:]], 5 * k, 1.6 * k)
        cv2.ellipse(m, T_(G + 12 * d_), (int(11 * k), int(3.5 * k)), -math.degrees(math.atan2(d_[1], d_[0])) * face * -1 if False else 0, 0, 360, 255, -1, cv2.LINE_AA)
        g2 = T_(G + 12 * d_); cv2.circle(m, g2, int(7.5 * k), 255, -1, cv2.LINE_AA)
    tip = T_(G + 128 * d_)
    return (tip[0] // K, tip[1] // K), T_(G), T_(sh)
def sword_free(m, t):
    if t < DROP: return
    u = t - DROP; x0, y0 = 790.0, 380.0; vx, vy, g = 300.0, -420.0, 1700.0
    x = x0 + vx * u; y = y0 + vy * u + .5 * g * u * u; ang = 10 * u
    if y >= GROUND: x, y, ang = x0 + vx * 0.95, GROUND, math.radians(-10)
    c = (math.sin(ang), -math.cos(ang))
    pts = [(int(K * (x + c[0] * (-24 + 142 * u_)) + 0), int(K * (y + c[1] * (-24 + 142 * u_)))) for u_ in np.linspace(0, 1, 10)]
    curve(m, pts, 6 * K, 2 * K)
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
    base = BG.copy()
    xa, xb = xat(XA, s), xat(XB, s)
    # bóng đất
    for xx_, ff in ((xa, 1), (xb, -1)): cv2.ellipse(base, (int(xx_ + ff * 8), GROUND + 7), (78, 10), 0, 0, 360, (150, 150, 150), -1, cv2.LINE_AA)
    base = cv2.GaussianBlur(base, (0, 0), .01) if False else base
    mask = np.zeros((H * K, W * K), np.float32)
    ntap = 4
    for j in range(ntap):  # mờ chuyển động (màn trập 180 độ)
        tj = t - (ntap - 1 - j) * (0.5 / FPS) / (ntap - 1) * 1.0
        sj = float(real2story(max(0, tj)))
        xaj, xbj = xat(XA, sj), xat(XB, sj)
        PAj, PBj = pose_at(KA, sj), pose_at(KB, sj)
        mj = np.zeros((H * K, W * K), np.uint8)
        tipA, gA, shA = fig(mj, xaj, 1, PAj, sj, True, True, sj * 11)
        fig(mj, xbj, -1, PBj, sj, sj < DROP, False, sj * 11 + 1.5)
        sword_free(mj, sj)
        mask += mj.astype(np.float32) / ntap
    am = cv2.resize(mask, (W, H), interpolation=cv2.INTER_AREA)[..., None] / 255.
    img = base * (1 - am) + np.array(INK, np.float32) * am
    PA = pose_at(KA, s)
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
