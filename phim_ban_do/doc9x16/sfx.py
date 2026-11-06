"""Tiếng hiệu ứng cho video dọc 9:16 (tổng hợp bằng numpy, không cần file ngoài).
Sự kiện lấy từ trang dựng: window.SFX = [[giây, loại, tham số]]. Mỗi loại ứng với một hiệu ứng trên bản đồ.
Quy ước mức: đỉnh mỗi tiếng khoảng -3 dBFS (mức thực do sidechain quyết định) trở xuống; khi trộn, dùng sidechain để TỰ HẠ khi có giọng đọc."""
import numpy as np, wave
SR = 44100
rng = np.random.default_rng(7)
def fit(y,n):
    y=np.asarray(y)[:n]; return np.pad(y,(0,n-len(y)))
def t_(d): return np.arange(int(d * SR)) / SR
def env(n, a=.005, r=.1):
    e = np.ones(n); na = max(1, int(a * SR)); nr = max(1, int(r * SR)); e[:na] = np.linspace(0, 1, na); e[-nr:] = np.minimum(e[-nr:], np.linspace(1, 0, nr)); return e
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for i, v in enumerate(x): s = (1 - a) * v + a * s; y[i] = s
    return y
def bp(x, lo, hi): return lp(x, hi) - lp(x, lo)
def noise(d): return rng.standard_normal(int(d * SR))
def pop(f=520, d=.22, g=1.0):
    t = t_(d); return g * np.sin(2 * np.pi * (f + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 16)
def ping(f=760, d=.55, g=.8):
    t = t_(d); return g * (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * f * 2.01 * t)) * np.exp(-t * 7)
def chime(f=660, d=.9, g=.8):
    t = t_(d); return g * (np.sin(2 * np.pi * f * t) * np.exp(-t * 4.5) + .6 * np.sin(2 * np.pi * f * 1.5 * t) * np.exp(-t * 5.5) + .3 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 7))
def thud(f=70, d=.28, g=1.0):
    t = t_(d); n = bp(noise(d), 60, 420) * 6; return g * (np.sin(2 * np.pi * (f + 40 * np.exp(-t * 28)) * t) * np.exp(-t * 14) + .25 * n * np.exp(-t * 40))
def stamp(g=1.0):
    n = int(.4 * SR); return fit(thud(55, .4, g), n) + fit(bp(noise(.05), 800, 3000) * np.exp(-t_(.05) * 70) * 5, n) * .6
def whoosh(d=.8, lo=300, hi=2800, g=.7, up=True):
    n = noise(d); y = bp(n, lo, hi) * 4; t = np.linspace(0, 1, len(y)); e = np.sin(np.pi * t) ** 2 if up else (1 - t) ** 2; return g * y * e
def flag(g=1.0):
    n = int(.45 * SR); return fit(whoosh(.45, 600, 3500, .8), n) + fit(np.pad(bp(noise(.04), 1500, 5000) * np.exp(-t_(.04) * 90) * 6, (int(.4 * SR), 0)), n) * .5
def coin(g=.8):
    t = t_(.16); return g * (np.sin(2 * np.pi * 2300 * t) * np.exp(-t * 28) + .7 * np.sin(2 * np.pi * 3100 * t) * np.exp(-t * 24))
def question(g=.8):
    t = t_(.55); f = 360 + 260 * np.clip(t / .35, 0, 1) ** 2; ph = 2 * np.pi * np.cumsum(f) / SR; return g * np.sin(ph) * env(len(t), .02, .25) * .7
def step(g=.9):
    t = t_(.07); return g * bp(noise(.07), 120, 900) * 14 * np.exp(-t * 55)
def murmur(d=3.0, g=.6):
    n = bp(noise(d), 180, 900) * 5; m = 1 + .5 * np.sin(2 * np.pi * np.arange(len(n)) / SR * 5.3); return g * n * m * env(len(n), d * .4, d * .4)
def swell(d=1.6, g=.5):
    t = t_(d); y = (np.sin(2 * np.pi * 110 * t) + .6 * np.sin(2 * np.pi * 165 * t)) * np.sin(np.pi * t / d) ** 2; return g * y
def render(events, total):
    out = np.zeros(int(total * SR) + SR * 3)
    def put(t, y):
        i = int(t * SR); y = np.asarray(y)
        if i < 0 or i >= len(out): return
        j = min(len(out), i + len(y)); out[i:j] += y[:j - i]
    for ev in events:
        t, k = ev[0], ev[1]; p = ev[2] if len(ev) > 2 else {}
        g = p.get('g', 1.0)
        if k == 'pop': put(t, pop(p.get('f', 520), g=g))
        elif k == 'ping': put(t, ping(p.get('f', 760), g=g))
        elif k == 'chime': put(t, chime(p.get('f', 660), g=g))
        elif k == 'thud': put(t, thud(p.get('f', 70), g=g))
        elif k == 'stamp': put(t, stamp(g))
        elif k == 'whoosh': put(t, whoosh(p.get('d', .8), g=.7 * g))
        elif k == 'flag': put(t, flag(g))
        elif k == 'coin': put(t, coin(.8 * g))
        elif k == 'question': put(t, question(g))
        elif k == 'steps':
            n = int(p.get('n', 6)); dt = p.get('dt', .42)
            for i in range(n): put(t + i * dt + (.05 if i % 2 else 0), step(g * (.85 if i % 2 else 1)))
        elif k == 'murmur': put(t, murmur(p.get('d', 3.0), .6 * g))
        elif k == 'swell': put(t, swell(p.get('d', 1.6), .5 * g))
    pk = np.abs(out).max() or 1; out = out / pk * (10 ** (-3 / 20))   # đỉnh -3 dBFS (còn bị sidechain hạ thêm khi có giọng)
    return out
def write(path, mono, total):
    n = int(total * SR); y = np.zeros(n); m = min(n, len(mono)); y[:m] = mono[:m]
    st = np.stack([y, y], 1); a = (np.clip(st, -1, 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())
