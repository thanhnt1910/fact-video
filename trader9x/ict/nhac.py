"""Nhạc nền lo-fi tự tổng hợp (không bản quyền). python nhac.py <giây> [ra.wav]"""
import sys, wave
import numpy as np
T = float(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else "music.wav"
sr = 44100; n = int(T * sr); t = np.arange(n) / sr; L = np.zeros(n); R = np.zeros(n)
def note(m): return 440 * 2 ** ((m - 69) / 12)
beat = 60 / 88; bar = beat * 4
prog = [[45, 57, 60, 64, 67], [41, 57, 60, 65, 69], [48, 55, 60, 64, 67], [43, 55, 59, 62, 67]]  # Am9 F C G
rng = np.random.default_rng(3)
for i in range(int(T / bar) + 1):
    s0 = int(i * bar * sr)
    if s0 >= n: break
    ch = prog[i % 4]; s1 = min(n, int((i + 1) * bar * sr + sr)); tt = np.arange(s1 - s0) / sr
    env = np.minimum(1, tt / 0.4) * np.exp(-tt * 0.35)
    for j, m in enumerate(ch[1:]):
        sig = 0.03 * np.sin(2 * np.pi * note(m) * tt) * env; L[s0:s1] += sig * (0.4 + 0.05 * j); R[s0:s1] += sig * (0.6 - 0.05 * j)
    tb = np.arange(min(int(bar * sr), n - s0)) / sr
    b = 0.12 * np.sin(2 * np.pi * note(ch[0] - 12) * tb) * np.minimum(1, tb / 0.02) * np.exp(-tb * 0.8); L[s0:s0 + len(b)] += b; R[s0:s0 + len(b)] += b
    for k in range(8):
        p = int(s0 + k * beat / 2 * sr); ln = min(int(0.4 * sr), n - p)
        if ln <= 0: continue
        tp = np.arange(ln) / sr; m = ch[1:][[0, 2, 1, 3, 2, 1, 3, 2][k]] + 12
        pl = 0.02 * np.sin(2 * np.pi * note(m) * tp) * np.exp(-tp * 9); L[p:p + ln] += pl * (0.3 if k % 2 else 0.7); R[p:p + ln] += pl * (0.7 if k % 2 else 0.3)
for k in range(int(T / beat)):
    p = int(k * beat * sr)
    if p >= n: break
    if k % 4 in (0, 2):
        ln = min(int(.25 * sr), n - p); tk = np.arange(ln) / sr
        s = 0.30 * np.sin(2 * np.pi * (48 + 70 * np.exp(-tk * 35)) * tk) * np.exp(-tk * 12); L[p:p + ln] += s; R[p:p + ln] += s
    for h in (0, .5):
        q = int(p + h * beat * sr); ln = min(int(.03 * sr), n - q)
        if ln > 0: s = 0.018 * rng.standard_normal(ln) * np.exp(-np.arange(ln) / sr * 120); L[q:q + ln] += s; R[q:q + ln] += s
fade = np.minimum(1, np.minimum(t / 1.0, (T - t) / 2.5)); st = np.stack([L * fade, R * fade], 1); st /= np.abs(st).max() / 0.75
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st * 32767).astype("<i2").tobytes())
