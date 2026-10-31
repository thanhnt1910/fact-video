"""Âm thanh video lt1v3: ghép giọng đọc theo mốc từng đoạn + nhạc nền + hiệu ứng tự tổng hợp (không dùng tiếng có bản quyền) -> ra/am.wav.
Chạy: python phim_ban_do/vecmap/film_am.py"""
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy import signal

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SR = 44100
SP = json.load(open(HERE / "sfx.json"))
TOTAL = SP["dur"]
N = int(TOTAL * SR) + SR
rng = np.random.default_rng(7)


def noise(n):
    return rng.standard_normal(n).astype(np.float32)


def lp(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), "low")
    return signal.lfilter(b, a, x).astype(np.float32)


def hp(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), "high")
    return signal.lfilter(b, a, x).astype(np.float32)


def bp(x, lo, hi):
    b, a = signal.butter(2, [lo / (SR / 2), hi / (SR / 2)], "band")
    return signal.lfilter(b, a, x).astype(np.float32)


def env_win(n, fi=0.8, fo=0.8):
    e = np.ones(n, np.float32)
    a, b = int(fi * SR), int(fo * SR)
    if a > 0:
        e[:min(a, n)] *= np.linspace(0, 1, min(a, n))
    if b > 0:
        e[-min(b, n):] *= np.linspace(1, 0, min(b, n))
    return e


def put(track, x, t0, gain=1.0):
    i = int(t0 * SR)
    if i >= len(track):
        return
    j = min(len(track), i + len(x))
    track[i:j] += x[:j - i] * gain


def thump(f=70, dur=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * (f + 40 * np.exp(-t * 30)) * t) * np.exp(-t * 9)).astype(np.float32)


def step():
    n = int(0.12 * SR)
    return lp(noise(n), 700) * np.exp(-np.arange(n) / SR * 40).astype(np.float32)


def clash():
    n = int(0.6 * SR); t = np.arange(n) / SR
    x = hp(noise(n), 1500) * np.exp(-t * 18)
    for f in (1180, 1870, 2630, 3450):
        x += 0.25 * np.sin(2 * np.pi * f * t) * np.exp(-t * 7)
    return (x * 0.7).astype(np.float32)


def whoosh():
    n = int(0.3 * SR)
    x = bp(noise(n), 1200, 4500) * np.sin(np.linspace(0, np.pi, n)).astype(np.float32)
    return x


def horn(dur=3.2):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 150 + 26 * np.minimum(t / 1.2, 1)
    x = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR).astype(np.float32)
    x = lp(x, 900) * np.minimum(t / 0.9, 1) * np.exp(-np.maximum(t - 1.6, 0) * 1.3)
    return x.astype(np.float32)


def gong(dur=4.0):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in ((95, 1, .9), (151, .6, 1.1), (238, .4, 1.5), (301, .25, 2)))
    return (x * 0.6).astype(np.float32)


def cricket_train(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    carrier = np.sin(2 * np.pi * 4300 * t)
    gate = (np.sin(2 * np.pi * 28 * t) > 0.3) * (np.sin(2 * np.pi * 2.2 * t) > -0.2)
    return (carrier * gate * 0.5).astype(np.float32)


def build():
    voice = np.zeros(N, np.float32)
    for i, st in SP["starts"].items():
        n = 20000 + int(i)
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(ROOT / f"assets/thu_giong_hai/lt1v3_chuan/{n}.mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        put(voice, np.frombuffer(raw, np.float32), float(st))
    # hạ nền khi có giọng (đường bao trơn)
    env = np.abs(voice)
    env = lp(env, 4, 1)
    duck = 1.0 - 0.5 * np.clip(env / (np.percentile(env, 90) + 1e-6), 0, 1)

    bed = np.zeros(N, np.float32)
    # nhạc nền: nốt kéo dài rất nhẹ (rê thứ) + sóng chậm
    t = np.arange(N) / SR
    pad = sum(a * np.sin(2 * np.pi * f * t + p) for f, a, p in ((73.4, .5, 0), (110.0, .35, 1), (146.8, .25, 2), (174.6, .18, 3), (220.0, .1, 4)))
    pad = pad * (0.6 + 0.4 * np.sin(2 * np.pi * t / 14.0)) * 0.05
    wind = lp(noise(N), 420) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 9.0 + 1)) * 0.06
    bed += pad.astype(np.float32) + wind.astype(np.float32)

    fxm = np.zeros(N, np.float32)
    for e in SP["sfx"]:
        k, t0 = e["s"], e["t0"]
        t1 = e.get("t1", t0 + 4)
        d = max(0.5, t1 - t0)
        if k == "march":
            tt = t0
            while tt < t1:
                put(fxm, step(), tt, 0.5 * min(1, (tt - t0) / 1.0, (t1 - tt) / 1.0)); tt += 0.52 + rng.random() * 0.05
        elif k == "drum":
            tt = t0
            while tt < t1:
                put(fxm, thump(), tt, 0.55); put(fxm, thump(55), tt + 0.52, 0.35); tt += 1.4
        elif k == "horn":
            put(fxm, horn(), t0, 0.55)
        elif k == "gong":
            put(fxm, gong(), t0, 0.7)
        elif k == "clash":
            for j in range(4):
                put(fxm, clash(), t0 + j * 0.22 + rng.random() * 0.08, 0.5)
        elif k == "arrow":
            tt = t0
            while tt < t1:
                put(fxm, whoosh(), tt, 0.4); tt += 0.12 + rng.random() * 0.22
        elif k == "fire":
            n = int(d * SR); x = lp(noise(n), 500) * 0.5
            cr = np.zeros(n, np.float32); idx = rng.integers(0, n, int(d * 40)); cr[idx] = rng.random(len(idx)) * 1.5
            x += hp(lp(cr, 6000), 1200) * 0.6
            put(fxm, x * env_win(n, 0.8, 0.8), t0, 0.5)
        elif k == "water":
            n = int(d * SR); x = lp(noise(n), 900) * (0.6 + 0.4 * np.sin(np.arange(n) / SR * 1.7))
            put(fxm, x.astype(np.float32) * env_win(n, 1.0, 1.0), t0, 0.35)
        elif k == "insect":
            n = int(d * SR); put(fxm, cricket_train(d) * env_win(n, 1.5, 1.5), t0, 0.12)
        elif k == "wind":
            n = int(d * SR); put(fxm, lp(noise(n), 600) * env_win(n, 1.5, 1.5), t0, 0.1)
    # trộn
    out = voice * 1.0 + (bed + fxm * 0.8) * duck
    # chuẩn hóa nhẹ
    out = out[:int(TOTAL * SR)]
    pk = np.max(np.abs(out))
    out = out / max(pk, 1e-6) * 0.89
    (HERE / "ra").mkdir(exist_ok=True)
    import wave
    with wave.open(str(HERE / "ra/am.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())
    print("ghi ra/am.wav", round(len(out) / SR, 1), "giây; đỉnh trước chuẩn hóa", round(float(pk), 2))


build()
