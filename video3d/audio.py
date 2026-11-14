"""TQ VIDEO — procedural sound design (no external assets needed)."""
import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 44100
rng = np.random.default_rng(7)


def bp(x, lo, hi, order=2):
    return signal.sosfilt(signal.butter(order, [lo, hi], 'bandpass', fs=SR, output='sos'), x)


def lp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, 'lowpass', fs=SR, output='sos'), x)


def hp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, 'highpass', fs=SR, output='sos'), x)


def env_exp(n, k):
    return np.exp(-np.arange(n) / SR * k)


def add(buf, snd, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= buf.shape[1] or i + len(snd) <= 0:
        return
    s = snd[: max(0, buf.shape[1] - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[0, i:i + len(s)] += s * gain * l * 1.41
    buf[1, i:i + len(s)] += s * gain * r * 1.41


# ---------- one-shot sounds ----------
def taiko(big=1.0):
    n = int(SR * 1.4); t = np.arange(n) / SR
    f = 48 + 85 * np.exp(-t * 22)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (5 / big))
    thump = lp(rng.standard_normal(n), 220) * np.exp(-t * 28) * 2.5
    slap = hp(rng.standard_normal(n), 1500) * np.exp(-t * 90) * 0.3
    return (body + thump + slap) * 0.8


def boom():
    n = int(SR * 4); t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(30 + 40 * np.exp(-t * 6)) / SR) * np.exp(-t * 1.1)
    rumble = lp(rng.standard_normal(n), 160, 4) * np.exp(-t * 1.6) * 6
    crack = hp(rng.standard_normal(n), 900) * np.exp(-t * 18) * 0.8
    return (sub + rumble + crack) * 0.9


def whoosh(dur=1.5):
    n = int(SR * dur); u = np.linspace(0, 1, n)
    nz = rng.standard_normal(n)
    low, high = bp(nz, 150, 700), bp(nz, 900, 4000)
    sweep = np.sin(np.pi * u)
    return (low * (1 - sweep) + high * sweep) * np.sin(np.pi * u) ** 2 * 1.5


def gong(base=92, decay=1.0):
    n = int(SR * 6 * decay); t = np.arange(n) / SR
    out = np.zeros(n)
    for k, (m, d) in enumerate([(1, .6), (1.48, .9), (2.03, 1.2), (2.71, 1.6), (3.9, 2.4), (5.2, 3.2)]):
        f = base * m * (1 + 0.004 * np.sin(2 * np.pi * 0.7 * t))
        out += np.sin(2 * np.pi * np.cumsum(f) / SR + k) * np.exp(-t * d / decay) / (1 + k * 0.5)
    out += hp(rng.standard_normal(n), 2000) * np.exp(-t * 40) * 0.2
    return out * 0.5


def horn(dur=2.5):
    n = int(SR * dur); t = np.arange(n) / SR
    f = 98 * (1 + 0.006 * np.sin(2 * np.pi * 5 * t)) * (0.97 + 0.03 * np.minimum(1, t * 3))
    ph = np.cumsum(f) / SR
    saw = (2 * (ph % 1) - 1) + 0.5 * (2 * ((ph * 1.5) % 1) - 1)
    e = np.minimum(1, t / 0.5) * np.minimum(1, (dur - t) / 0.6)
    return lp(saw, 900, 3) * e * 0.5


def splash():
    n = int(SR * 0.9); t = np.arange(n) / SR
    s = bp(rng.standard_normal(n), 300, 5000) * np.exp(-t * 7) * np.minimum(1, t * 200)
    s += lp(rng.standard_normal(n), 300) * np.exp(-t * 10) * 1.5
    return s * 0.6


def arrow(flight):
    n = int(SR * (flight + 0.3)); t = np.arange(n) / SR
    fl = int(SR * flight)
    f = 2600 - 1300 * np.clip(t / flight, 0, 1)
    wh = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.04 + bp(rng.standard_normal(n), 2000, 6000) * 0.05
    e = np.clip(t / flight, 0, 1) ** 2 * (t < flight)
    out = wh * e
    th = lp(rng.standard_normal(n - fl), 500) * np.exp(-np.arange(n - fl) / SR * 30) * 0.6
    out[fl:] += th
    tw = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25) * 0.2  # bow release
    return out + tw


def pluck(freq, dur=2.2, bright=0.5):
    """Karplus-Strong plucked string (dan tranh-like)."""
    n = int(SR * dur); p = max(2, int(SR / freq)); out = np.zeros(n)
    buf = lp(rng.uniform(-1, 1, p), 1500 + 5000 * bright, 1) if p > 20 else rng.uniform(-1, 1, p)
    k = 0
    while k < n:
        m = min(p, n - k); out[k:k + m] = buf[:m]
        buf = 0.4985 * (buf + np.roll(buf, 1)); k += p
    return out * np.minimum(1, np.arange(n) / (SR * 0.004))


def chirp_bird():
    d = rng.uniform(0.08, 0.22); n = int(SR * d); t = np.arange(n) / SR
    f0 = rng.uniform(2600, 4200); f = f0 * (1 + rng.uniform(-0.35, 0.35) * t / d + 0.08 * np.sin(2 * np.pi * rng.uniform(20, 45) * t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2 * 0.25


def birds_bed(n, density=0.8):
    out = np.zeros(n); t = 0.0
    while t < n / SR - 0.5:
        k = int(rng.integers(1, 5)); base = t
        for _ in range(k):
            s = chirp_bird(); i = int(base * SR); m = min(len(s), n - i); out[i:i + m] += s[:m]; base += len(s) / SR + rng.uniform(0.03, 0.12)
        t += rng.exponential(1.2 / density)
    return out


def pentatonic_bed(n, keys, seed=3):
    """Gentle pentatonic melody on plucked strings over a soft drone (D F G A C)."""
    r = np.random.default_rng(seed); scale = [146.83, 174.61, 196.0, 220.0, 261.63, 293.66, 349.23, 392.0, 440.0]
    out = np.zeros(n); t = 0.6; i = 4
    while t < n / SR - 1:
        i = int(np.clip(i + r.choice([-2, -1, -1, 0, 1, 1, 2]), 0, len(scale) - 1))
        s = pluck(scale[i], 2.4, 0.4); j = int(t * SR); m = min(len(s), n - j); out[j:j + m] += s[:m] * 0.5
        if r.random() < 0.25:  # grace note / ornament
            s2 = pluck(scale[max(0, i - 1)], 1.6, 0.3); j2 = j + int(0.16 * SR); m2 = min(len(s2), n - j2)
            if m2 > 0: out[j2:j2 + m2] += s2[:m2] * 0.3
        t += r.choice([0.55, 0.8, 0.8, 1.1, 1.6])
    tt = np.arange(n) / SR
    drone = lp(sum(np.sin(2 * np.pi * f * tt) for f in (73.42, 110.0)) * 0.12, 400)
    kt = np.array([k[0] for k in keys]); kg = np.array([k[1] for k in keys])
    return (out + drone) * np.interp(tt, kt, kg)


# ---------- beds ----------
def water_bed(n):
    t = np.arange(n) / SR
    b = lp(np.cumsum(rng.standard_normal(n)) * 0.02, 700)
    b = b - lp(b, 30)
    lap = bp(rng.standard_normal(n), 300, 1400) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.35 * t) * np.sin(2 * np.pi * 0.13 * t + 1)) ** 2
    return b * 0.6 + lap * 0.25


def wind_bed(n):
    t = np.arange(n) / SR
    g = 0.5 + 0.3 * np.sin(2 * np.pi * 0.07 * t) + 0.2 * np.sin(2 * np.pi * 0.19 * t + 2)
    return bp(rng.standard_normal(n), 250, 1200) * g * 0.5


def fire_bed(n, level):
    roar = lp(rng.standard_normal(n), 280, 3) * 1.6 + bp(rng.standard_normal(n), 500, 2500) * 0.25
    out = roar * level
    # crackles
    dens = 4 + 70 * level
    k = rng.random(n) < dens / SR
    idx = np.nonzero(k)[0]
    imp = np.zeros(n); imp[idx] = rng.uniform(-1, 1, len(idx)) * (0.4 + level[idx])
    kern = hp(rng.standard_normal(int(SR * 0.012)), 1800) * env_exp(int(SR * 0.012), 300)
    out += np.convolve(imp, kern, 'same') * 1.2
    return out


def music_bed(n, keys):
    t = np.arange(n) / SR
    notes = [73.42, 110.0, 146.83, 174.61, 220.0]  # D minor
    pad = np.zeros(n)
    for f in notes:
        for d in (-0.15, 0.15):
            ph = np.cumsum(np.full(n, f + d)) / SR
            pad += 2 * (ph % 1) - 1
    pad = lp(pad, 650, 3) / len(notes)
    kt = np.array([k[0] for k in keys]); kg = np.array([k[1] for k in keys])
    return pad * np.interp(t, kt, kg)


def reverb(x, secs=2.4, wet=0.25):
    n = int(SR * secs)
    ir = rng.standard_normal(n) * env_exp(n, 3.0 / secs * 2.3)
    ir = lp(ir, 5000); ir /= np.sqrt((ir ** 2).sum())
    y = signal.fftconvolve(x, ir)[: len(x)]
    return x * (1 - wet) + y * wet * 3


# ---------- mixer ----------
def load_voice(V, n):
    import os, subprocess
    d = V['dir']; out = np.zeros(n)
    for it in V['items']:
        f = os.path.join(d, f"{it['n']}.mp3")
        if not os.path.exists(f): raise SystemExit(f'thiếu giọng {f}')
        pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
        x = np.frombuffer(pcm, np.int16).astype(np.float64) / 32768.0; i = int(it['at'] * SR); m = min(len(x), n - i)
        if m > 0: out[i:i + m] += x[:m]
    return np.stack([out, out])


def make_audio(spec, log, dur, out_wav):
    A = spec.get('audio', {})
    n = int(dur * SR) + SR
    beds = np.zeros((2, n)); fx = np.zeros((2, n))
    amb = A.get('ambience', {})
    if amb.get('water', 0):
        w = water_bed(n) * amb['water']; beds[0] += w; beds[1] += np.roll(w, 300)
    if amb.get('birds', 0):
        w = birds_bed(n) * amb['birds']; beds[0] += w; beds[1] += np.roll(w, 2200)
    if amb.get('wind', 0):
        w = wind_bed(n) * amb['wind']; beds[0] += w; beds[1] += np.roll(w, 900)
    if A.get('fire', 0) and log['fire']:
        fps = spec.get('fps', 30)
        fa = np.array(log['fire']); fa = np.clip(fa / max(10.0, fa.max()), 0, 1) ** 0.7
        level = np.interp(np.arange(n) / SR, np.arange(len(fa)) / fps, fa)
        for ch in (0, 1):
            beds[ch] += fire_bed(n, level) * A['fire'] * 0.6
    sp = A.get('splash', 0)
    for t in log['splash'] if sp else []:
        add(fx, splash(), t, sp * rng.uniform(0.5, 1), rng.uniform(-0.6, 0.6))
    ar = A.get('arrows', 0)
    for t0, t1 in log['arrows'] if ar else []:
        add(fx, arrow(t1 - t0), t0, ar * rng.uniform(0.4, 1) * 0.5, rng.uniform(-0.7, 0.7))
    ig = A.get('ignite', 0)
    for t in log['ignite'] if ig else []:
        add(fx, whoosh(0.8), t - 0.3, ig * 0.35, rng.uniform(-0.5, 0.5))
    music = np.zeros((2, n))
    for d in A.get('drums', []):
        step = 60 / d.get('bpm', 100) / 2; pat = d.get('pattern', 'X.x.X.xx'); i = 0; t = d['from']
        while t < d['to']:
            c = pat[i % len(pat)]
            if c != '.':
                ramp = 0.6 + 0.4 * (t - d['from']) / max(0.1, d['to'] - d['from']) if d.get('crescendo') else 1
                add(music, taiko(1.3 if c == 'X' else 0.8), t, d.get('gain', 0.8) * (1 if c == 'X' else 0.55) * ramp, rng.uniform(-0.3, 0.3))
            t += step; i += 1
    if A.get('music'):
        mb = pentatonic_bed if A['music'].get('style') == 'pentatonic' else music_bed
        m = mb(n, A['music']['gain']); music[0] += m; music[1] += np.roll(m, 200)
    for c in A.get('cues', []):
        typ, at, g = c['type'], c['at'], c.get('gain', 1.0)
        snd = {'boom': boom, 'gong': gong, 'horn': lambda: horn(c.get('dur', 2.5)), 'whoosh': lambda: whoosh(c.get('dur', 1.5)),
               'taiko': taiko, 'splash': splash, 'bell': lambda: gong(58, 1.6)}[typ]()
        add(music if typ in ('gong', 'horn', 'taiko', 'bell') else fx, snd, at, g, c.get('pan', 0))
    music = np.stack([reverb(music[0], 2.6, 0.3), reverb(music[1], 2.8, 0.3)])
    fx = np.stack([reverb(fx[0], 1.2, 0.15), reverb(fx[1], 1.3, 0.15)])
    mix = beds * 0.5 + fx * 0.8 + music * 0.7
    V = A.get('voice')
    if V:   # lời đọc (đã loudnorm −16 LUFS): nền nhạc đặt ở mức thấp cố định và nhún xuống khi có tiếng
        voice = load_voice(V, n)
        a1 = 1 - np.exp(-1 / (SR * 0.12)); e = signal.lfilter([a1], [1, a1 - 1], np.abs(voice[0])); e = signal.lfilter([a1], [1, a1 - 1], e[::-1])[::-1]
        e = np.clip(e / (np.percentile(e[e > 1e-4], 60) + 1e-9) if (e > 1e-4).any() else e, 0, 1)
        duck = 1 - V.get('duck', 0.6) * e
        rms = np.sqrt(np.mean(mix ** 2)) + 1e-9
        mix = mix / rms * V.get('bed', 0.03) * duck + voice * V.get('gain', 1.0)
        mix = mix[:, : int(dur * SR)]
        fo = int(SR * 0.6); mix[:, -fo:] *= np.linspace(1, 0, fo); mix[:, :int(SR * 0.3)] *= np.linspace(0, 1, int(SR * 0.3))
        lim = 0.8; o = np.abs(mix) > lim; mix[o] = np.sign(mix[o]) * (lim + (1 - lim) * np.tanh((np.abs(mix[o]) - lim) / (1 - lim)))   # chỉ nén đỉnh, không đẩy âm lượng
        wavfile.write(out_wav, SR, (mix.T * 32767).astype(np.int16)); return
    mix = mix[:, : int(dur * SR)]
    fo = int(SR * 0.6); mix[:, -fo:] *= np.linspace(1, 0, fo); mix[:, :int(SR * 0.3)] *= np.linspace(0, 1, int(SR * 0.3))
    mix = np.tanh(mix / (np.abs(mix).max() + 1e-9) * 1.4) / np.tanh(1.4) * 0.89
    wavfile.write(out_wav, SR, (mix.T * 32767).astype(np.int16))
