#!/usr/bin/env python3
"""Tạo hiệu ứng âm thanh cho video Thales từ danh sách sự kiện (scripts/dump_sfx.ts).
Dùng: python3 scripts/sfx_thales.py sfx.json out.wav
Âm thanh được tổng hợp bằng numpy, không dùng mẫu có bản quyền."""
import json, sys
import numpy as np
from scipy.signal import butter, lfilter
from scipy.io import wavfile

SR = 44100
rng = np.random.default_rng(7)


def T(d):
    return np.arange(int(d * SR)) / SR


def noise(d):
    return rng.standard_normal(int(d * SR))


def lp(x, fc, o=2):
    b, a = butter(o, fc / (SR / 2), 'low')
    return lfilter(b, a, x)


def hp(x, fc, o=2):
    b, a = butter(o, fc / (SR / 2), 'high')
    return lfilter(b, a, x)


def bp(x, lo, hi, o=2):
    b, a = butter(o, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)], 'band')
    return lfilter(b, a, x)


def ex(d, tau):
    return np.exp(-T(d) / tau)


def sine(f, d, ph=0.0):
    return np.sin(2 * np.pi * f * T(d) + ph)


def sweep(f0, f1, d, exp=True):
    t = T(d)
    if exp:
        f = f0 * (f1 / f0) ** (t / d)
        phase = 2 * np.pi * f0 * d / np.log(f1 / f0) * ((f1 / f0) ** (t / d) - 1)
    else:
        phase = 2 * np.pi * (f0 * t + (f1 - f0) * t * t / (2 * d))
    return np.sin(phase)


def fade(x, a=0.004, b=0.01):
    n = len(x)
    na, nb = max(1, int(a * SR)), max(1, int(b * SR))
    x = x.copy()
    x[:na] *= np.linspace(0, 1, na)
    x[-nb:] *= np.linspace(1, 0, nb)
    return x


def bell(f, d, tau, partials=((1, 1), (2.76, 0.35), (5.4, 0.12))):
    out = np.zeros(int(d * SR))
    for r, a in partials:
        out += a * sine(f * r, d) * ex(d, tau / (1 + 0.5 * (r - 1)))
    return fade(out)


def S_step(v=1):
    f = rng.uniform(0.85, 1.15)
    d = 0.14
    return v * fade(0.8 * lp(noise(d), 900 * f) * ex(d, 0.03) + 0.7 * sine(95 * f, d) * ex(d, 0.045))


def S_hoof(v=1):
    f = rng.uniform(0.85, 1.15)
    d = 0.16
    return v * 0.8 * fade(0.7 * sine(72 * f, d) * ex(d, 0.05) + 0.5 * lp(noise(d), 700 * f) * ex(d, 0.03) + 0.2 * bp(noise(d), 1500, 3500) * ex(d, 0.012))


def S_bell(v=1):
    f = rng.choice([1046, 1175, 1318])
    return v * 0.6 * bell(f, 1.0, 0.45)


def S_pop(v=1):
    f = rng.uniform(0.95, 1.1)
    d = 0.12
    return v * fade(0.7 * sweep(650 * f, 1150 * f, d) * ex(d, 0.05) + 0.2 * sine(2300 * f, d) * ex(d, 0.02))


def S_tick(v=1):
    d = 0.04
    return v * 0.5 * fade(hp(noise(d), 2500) * ex(d, 0.006) + 0.3 * sine(1800, d) * ex(d, 0.01))


def S_chime(v=1):
    out = np.zeros(int(1.8 * SR))
    for f, d, tau, a in ((880, 1.8, 0.7, 1.0), (1318.5, 1.6, 0.6, 0.7), (1760, 1.4, 0.5, 0.4)):
        b = bell(f, d, tau)
        out[: len(b)] += a * b
    return v * 0.6 * out


def S_success(v=1):
    notes = [523.25, 659.25, 783.99, 1046.5]
    out = np.zeros(int(1.4 * SR))
    for i, f in enumerate(notes):
        b = bell(f, 0.9, 0.35, ((1, 1), (2, 0.3), (3, 0.1)))
        s = int(i * 0.09 * SR)
        out[s:s + len(b)] += b[: len(out) - s]
    return v * 0.55 * out


def S_whoosh(v=1, d=0.8, up=False, down=False):
    n = noise(d)
    bands = [(300, 700), (700, 1600), (1600, 3600)]
    t = T(d) / d
    out = np.zeros(len(n))
    centers = [0.25, 0.5, 0.75]
    if up:
        pass
    if down:
        centers = centers[::-1]
    for (lo, hi), c in zip(bands, centers):
        out += bp(n, lo, hi) * np.exp(-((t - c) ** 2) / 0.03)
    env = np.sin(np.pi * np.clip(t, 0, 1)) ** 1.3
    return v * 0.5 * fade(out * env, 0.02, 0.05)


def S_thud(v=1):
    d = 0.4
    return v * 0.9 * fade(sine(58, d) * ex(d, 0.12) + 0.6 * lp(noise(d), 300) * ex(d, 0.05) + 0.2 * sine(110, d) * ex(d, 0.08))


def S_crash(v=1):
    d = 1.6
    out = 0.6 * lp(noise(d), 5000) * ex(d, 0.3) + 0.4 * bp(noise(d), 800, 2500) * ex(d, 0.5)
    for k in range(7):
        s = int(rng.uniform(0, 0.9) * SR)
        th = S_thud(rng.uniform(0.3, 0.8))
        e = min(len(th), len(out) - s)
        out[s:s + e] += th[:e] * 0.9
    out += 0.5 * sine(48, d) * ex(d, 0.35)
    return v * 0.8 * fade(out, 0.002, 0.2)


def S_creak(v=1, d=0.9):
    t = T(d)
    f = 190 + 70 * np.sin(2 * np.pi * 5 * t) + 40 * np.sin(2 * np.pi * 11 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
    out = bp(saw, 400, 1800) * (0.5 + 0.5 * np.sin(2 * np.pi * 8 * t) ** 2)
    return v * 0.45 * fade(out * np.sin(np.pi * t / d) ** 0.7)


def S_rope(v=1, d=0.8):
    t = T(d)
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 17 * t)
    return v * 0.5 * fade(bp(noise(d), 1200, 3200) * am * np.sin(np.pi * t / d), 0.05, 0.1)


def S_slip(v=1):
    d = 0.5
    tri = 2 * np.abs(2 * ((np.cumsum(np.linspace(900, 200, int(d * SR))) / SR) % 1) - 1) - 1
    return v * 0.45 * fade(tri * ex(d, 0.25) + 0.3 * bp(noise(d), 800, 3000) * ex(d, 0.15), 0.005, 0.05)


def S_servo(v=1, d=2.6):
    t = T(d)
    f = 110 + 120 * (t / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
    out = lp(saw, 1400) * (0.7 + 0.3 * np.sin(2 * np.pi * 14 * t))
    env = np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.3)
    return v * 0.3 * out * env


def S_wood(v=1):
    d = 0.14
    return v * 0.8 * fade(sine(rng.uniform(380, 460), d) * ex(d, 0.035) + 0.5 * lp(noise(d), 2500) * ex(d, 0.015))


def S_water(v=1, d=5.6):
    t = T(d)
    n = lp(noise(d), 900)
    swell = np.sin(np.pi * t / d) ** 2
    gur = 0.6 + 0.4 * np.sin(2 * np.pi * 0.9 * t + 3 * np.sin(2 * np.pi * 0.13 * t))
    return v * 0.9 * n * swell * gur


def S_rumble(v=1, d=1.8):
    t = T(d)
    out = lp(noise(d), 160) * 1.5 + 0.6 * sine(42, d)
    return v * 0.8 * fade(out * np.sin(np.pi * t / d) ** 0.8, 0.05, 0.2)


def S_bad(v=1):
    out = np.zeros(int(0.6 * SR))
    for i, f in enumerate([330, 247]):
        d = 0.24
        tri = 2 * np.abs(2 * ((f * T(d)) % 1) - 1) - 1
        s = int(i * 0.2 * SR)
        out[s:s + len(tri)] += fade(tri * ex(d, 0.15)) [: len(out) - s] * 0.6
    return v * 0.5 * out


def S_question(v=1):
    out = np.zeros(int(0.8 * SR))
    for i, f in enumerate([523, 698]):
        b = bell(f, 0.5, 0.3, ((1, 1), (2, 0.2)))
        s = int(i * 0.16 * SR)
        out[s:s + len(b)] += b[: len(out) - s]
    return v * 0.6 * out


def S_zoom(v=1, d=3.4):
    t = T(d)
    s = sweep(180, 1500, d)
    env = (t / d) ** 1.5 * np.minimum(1, (d - t) / 0.05 + 0.0)
    out = 0.5 * s * env + 0.15 * bp(noise(d), 600, 3500) * env
    return v * 0.7 * fade(out, 0.01, 0.02)


def S_lock(v=1):
    d = 0.3
    return v * 0.8 * fade(hp(noise(0.03), 1500) * 1.0 if False else sine(2100, d) * ex(d, 0.1) + 0.5 * sine(1400, d) * ex(d, 0.06))


def S_shimmer(v=1):
    d = 1.2
    out = np.zeros(int(d * SR))
    for k in range(6):
        f = rng.uniform(2000, 4200)
        s = int(rng.uniform(0, 0.3) * SR)
        b = bell(f, 0.8, 0.25, ((1, 1),))
        e = min(len(b), len(out) - s)
        out[s:s + e] += b[:e] * 0.25
    return v * out


def S_swing(v=1, d=2.8):
    t = T(d)
    s = sweep(500, 110, d)
    n = bp(noise(d), 300, 1500)
    env = np.sin(np.pi * t / d) ** 1.2
    return v * 0.4 * fade((0.5 * s + 0.5 * n) * env, 0.05, 0.1)


def S_scratch(v=1, d=4.2):
    t = T(d)
    n = bp(noise(d), 2500, 7000)
    am = np.clip(np.sin(2 * np.pi * 3.1 * t) + 0.6 * np.sin(2 * np.pi * 7.3 * t), 0, None)
    return v * 0.35 * n * am * np.minimum(1, (d - t) / 0.3)


KINDS = {
    'step': S_step, 'hoof': S_hoof, 'bell': S_bell, 'pop': S_pop, 'tick': S_tick, 'chime': S_chime,
    'success': S_success, 'thud': S_thud, 'crash': S_crash, 'creak': S_creak, 'rope': S_rope, 'slip': S_slip,
    'servo': S_servo, 'wood': S_wood, 'water': S_water, 'rumble': S_rumble, 'bad': S_bad, 'question': S_question,
    'zoom': S_zoom, 'lock': S_lock, 'shimmer': S_shimmer, 'swing': S_swing, 'scratch': S_scratch,
    'whoosh': lambda v=1, d=0.9: S_whoosh(v, d),
    'whooshUp': lambda v=1, d=1.2: S_whoosh(v, d, up=True),
    'whooshDown': lambda v=1, d=1.2: S_whoosh(v, d, down=True),
}


def chirp():
    out = np.zeros(int(0.5 * SR))
    for i in range(int(rng.integers(2, 4))):
        d = 0.09
        c = fade(sweep(rng.uniform(2800, 3400), rng.uniform(3800, 4600), d) * ex(d, 0.05))
        s = int(i * 0.13 * SR)
        out[s:s + len(c)] += c[: len(out) - s]
    return 0.12 * out


def main(src, dst):
    data = json.load(open(src))
    total = data['total']
    n = int((total + 2) * SR)
    L = np.zeros(n)
    R = np.zeros(n)

    def put(sig, t, pan, v=1.0):
        s = int(t * SR)
        if s < 0 or s >= n:
            return
        e = min(len(sig), n - s)
        a = (pan + 1) * np.pi / 4
        L[s:s + e] += sig[:e] * np.cos(a) * v
        R[s:s + e] += sig[:e] * np.sin(a) * v

    for e in data['events']:
        k = e['k']
        fn = KINDS[k]
        kw = {'v': e.get('v', 1.0)}
        if e.get('d'):
            kw['d'] = e['d']
        try:
            sig = fn(**kw)
        except TypeError:
            sig = fn(kw['v'])
        put(sig, e['t'], e.get('pan', 0), 1.0)

    # gió nền
    w = lp(rng.standard_normal(n), 380, 2) * 0.9 + 0.25 * bp(rng.standard_normal(n), 1200, 2400)
    tt = np.arange(n) / SR
    wmod = 0.55 + 0.45 * np.sin(2 * np.pi * 0.07 * tt + 1.0) * np.sin(2 * np.pi * 0.031 * tt)
    wind = w * wmod * 0.03
    fadew = np.minimum(1, tt / 2.5) * np.minimum(1, (total + 1.5 - tt) / 2.5)
    L += wind * fadew
    R += np.roll(wind, 900) * fadew
    # chim hót thưa
    t = 3.0
    while False:
        put(chirp(), t, rng.uniform(-0.8, 0.8))
        t += rng.uniform(7, 13)

    peak = max(np.abs(L).max(), np.abs(R).max())
    g = 0.89 / peak
    L = np.tanh(L * g * 1.1) / np.tanh(1.1)
    R = np.tanh(R * g * 1.1) / np.tanh(1.1)
    out = np.stack([L, R], 1)
    wavfile.write(dst, SR, (out * 32000).astype(np.int16))
    print('ok', dst, round(total, 1), 's, events', len(data['events']))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
