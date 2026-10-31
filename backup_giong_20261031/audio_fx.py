"""
Âm thanh cho video: hiệu ứng (sfx) tự tổng hợp, lịch phát hiệu ứng khớp với chuyển động hình,
và phân tích kịch bản giọng đọc thành từng đoạn có nhấn nhá.

Muốn dùng hiệu ứng của riêng bạn: đặt file WAV vào assets/sfx/ với đúng tên
(transition.wav, pop.wav, tick.wav, chime.wav, impact.wav, reveal.wav, outro.wav;
phong cách kể chuyện: story_turn.wav, story_boom.wav, story_tap.wav, story_dong.wav, story_bell.wav, ambience.wav)
— file đó sẽ được dùng thay âm tự tạo.
"""
import re
import wave
from pathlib import Path

import numpy as np

SFX_SR = 44100
ROOT = Path(__file__).resolve().parent


# ======================================================================= tổng hợp âm
def _t(sec):
    return np.arange(int(sec * SFX_SR)) / SFX_SR


def _env(n, attack=0.004, decay=0.25, sr=SFX_SR):
    t = np.arange(n) / sr
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay)


def _bandpass_noise(sec, f0, f1, q=1.6, seed=3):
    """Tiếng gió lọc dải, tần số quét từ f0 -> f1 (biquad cập nhật theo khối)."""
    rng = np.random.default_rng(seed)
    n = int(sec * SFX_SR)
    x = rng.uniform(-1, 1, n)
    y = np.zeros(n)
    x1 = x2 = y1 = y2 = 0.0
    block = 64
    for s in range(0, n, block):
        p = s / n
        f = f0 * (f1 / f0) ** p
        w0 = 2 * np.pi * f / SFX_SR
        alpha = np.sin(w0) / (2 * q)
        b0, b2 = alpha, -alpha
        a0, a1, a2 = 1 + alpha, -2 * np.cos(w0), 1 - alpha
        for i in range(s, min(n, s + block)):
            xi = x[i]
            yi = (b0 * xi + b2 * x2 - a1 * y1 - a2 * y2) / a0
            x2, x1 = x1, xi
            y2, y1 = y1, yi
            y[i] = yi
    return y


def _norm(x, peak=0.9):
    m = np.max(np.abs(x)) or 1.0
    return x / m * peak


def sfx_transition():
    """Chuyển cảnh: tiếng 'vút' mềm, quét lên cao, kết thúc gọn (không rè)."""
    sec = 0.34
    n = int(sec * SFX_SR)
    air = _bandpass_noise(sec, 350, 5200, q=2.2)
    t = np.arange(n) / n
    env = (np.sin(np.pi * np.clip(t / 0.75, 0, 1)) ** 2) * (1 - 0.6 * t)
    tone = np.sin(2 * np.pi * np.cumsum(np.linspace(260, 720, n)) / SFX_SR) * 0.18 * env
    return _norm(air * env * 0.9 + tone, 0.55)


def sfx_pop():
    """Hiện phần tử: tiếng 'bóp' tròn, vui tai."""
    n = int(0.12 * SFX_SR)
    f = np.geomspace(1100, 380, n)
    ph = 2 * np.pi * np.cumsum(f) / SFX_SR
    x = np.sin(ph) * _env(n, 0.002, 0.035)
    x += 0.25 * np.sin(2 * ph) * _env(n, 0.002, 0.02)
    return _norm(x, 0.6)


def sfx_tick():
    """Mốc thời gian / phần tử nhỏ: tiếng 'tách' gỗ ngắn."""
    n = int(0.06 * SFX_SR)
    t = np.arange(n) / SFX_SR
    x = (np.sin(2 * np.pi * 1850 * t) + 0.5 * np.sin(2 * np.pi * 2900 * t)) * _env(n, 0.0008, 0.012)
    return _norm(x, 0.45)


def _bell(freq, sec=1.1, decay=0.45, peak=0.6):
    t = _t(sec)
    parts = [(1.0, 1.0), (2.0, 0.42), (3.01, 0.22), (4.16, 0.10), (5.43, 0.05)]
    x = sum(a * np.sin(2 * np.pi * freq * m * t) * np.exp(-t / (decay / (1 + 0.6 * k)))
            for k, (m, a) in enumerate(parts))
    x *= np.clip(t / 0.003, 0, 1)
    return _norm(x, peak)


def sfx_chime():
    """Lật sự thật / con số: tiếng chuông 'ding' sáng."""
    return _bell(1318.5, 1.0, 0.38, 0.5)


def sfx_impact():
    """Mở đầu (hook): cú 'bùm' trầm êm + lớp không khí, tạo cảm giác bất ngờ."""
    sec = 0.9
    n = int(sec * SFX_SR)
    t = np.arange(n) / SFX_SR
    f = 55 + 70 * np.exp(-t / 0.06)
    body = np.sin(2 * np.pi * np.cumsum(f) / SFX_SR) * _env(n, 0.003, 0.28)
    air = _bandpass_noise(0.25, 2500, 600, q=0.9, seed=9)
    air = np.pad(air * _env(len(air), 0.001, 0.06), (0, n - len(air)))
    return _norm(body + 0.35 * air, 0.75)


def sfx_reveal():
    """Cảnh câu khẳng định: 2 nốt đi lên ngắn gọn."""
    a = _bell(880.0, 0.5, 0.18, 0.5)
    b = _bell(1318.5, 0.7, 0.25, 0.5)
    off = int(0.09 * SFX_SR)
    out = np.zeros(off + len(b))
    out[:len(a)] += a
    out[off:off + len(b)] += b
    return _norm(out, 0.5)


def sfx_outro():
    """Kết: hợp âm rải lấp lánh (Đô - Mi - Son - Đô)."""
    notes = [1046.5, 1318.5, 1568.0, 2093.0]
    step = int(0.085 * SFX_SR)
    bells = [_bell(f, 1.2, 0.5, 0.45) for f in notes]
    out = np.zeros(step * len(notes) + len(bells[-1]))
    for i, b in enumerate(bells):
        out[i * step:i * step + len(b)] += b
    return _norm(out, 0.55)


# ---------------------------------------------------------------- bộ âm KỂ CHUYỆN ("style": "story")
def _fft_band(x, lo, hi):
    """Lọc dải nhanh bằng FFT (dùng cho đoạn dài)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SFX_SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def sfx_story_turn():
    """Chuyển cảnh: tiếng lật trang giấy cũ + làn hơi trầm."""
    sec = 0.55
    n = int(sec * SFX_SR)
    t = np.arange(n) / SFX_SR
    rng = np.random.default_rng(21)
    paper = _fft_band(rng.uniform(-1, 1, n), 1400, 7000)
    flutter = np.zeros(n)
    for c, w, a in [(0.07, 0.05, 0.6), (0.17, 0.07, 1.0), (0.30, 0.10, 0.75), (0.42, 0.08, 0.35)]:
        flutter += a * np.exp(-((t - c) / w) ** 2)
    air = _fft_band(rng.uniform(-1, 1, n), 120, 700) * np.sin(np.pi * np.clip(t / sec, 0, 1)) ** 2
    return _norm(paper * flutter * 0.8 + air * 0.5, 0.5)


def sfx_story_boom():
    """Mở đầu: tiếng 'thình' trầm, vang dài như tiếng trống trong hang đá."""
    sec = 2.2
    n = int(sec * SFX_SR)
    t = np.arange(n) / SFX_SR
    f = 42 + 55 * np.exp(-t / 0.09)
    body = np.sin(2 * np.pi * np.cumsum(f) / SFX_SR) * _env(n, 0.004, 0.55)
    rng = np.random.default_rng(5)
    rumble = _fft_band(rng.uniform(-1, 1, n), 30, 260) * _env(n, 0.01, 0.8)
    return _norm(body + 0.6 * rumble / (np.max(np.abs(rumble)) or 1), 0.8)


def sfx_story_tap():
    """Hiện ý / mốc thời gian: tiếng gõ gỗ trầm, rất nhẹ."""
    n = int(0.16 * SFX_SR)
    t = np.arange(n) / SFX_SR
    x = (np.sin(2 * np.pi * 330 * t) + 0.45 * np.sin(2 * np.pi * 760 * t)) * _env(n, 0.0015, 0.035)
    return _norm(x, 0.4)


def sfx_story_dong():
    """Sự thật bất ngờ / con số: tiếng chuông đồng trầm, ngân xa."""
    return _bell(196.0, 2.6, 1.1, 0.5)


def sfx_story_bell():
    """Kết: hai tiếng chuông nhà thờ cổ từ xa."""
    a = _bell(146.8, 3.2, 1.4, 0.5)
    b = _bell(110.0, 3.4, 1.6, 0.45)
    off = int(1.05 * SFX_SR)
    out = np.zeros(off + len(b))
    out[:len(a)] += a
    out[off:off + len(b)] += b * 0.8
    return _norm(out, 0.5)


def ambience_pad(sec, seed=7):
    """Nền không khí suốt video: tiếng ù trầm + gió nhẹ, lên xuống chậm."""
    n = int(sec * SFX_SR)
    t = np.arange(n) / SFX_SR
    drone = (np.sin(2 * np.pi * 55 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.05 * t))
             + 0.7 * np.sin(2 * np.pi * 82.4 * t + 1) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.071 * t + 2))
             + 0.35 * np.sin(2 * np.pi * 110.3 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.043 * t + 4)))
    rng = np.random.default_rng(seed)
    wind = _fft_band(rng.uniform(-1, 1, n), 180, 900)
    wind = wind / (np.max(np.abs(wind)) or 1) * (0.35 + 0.65 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.06 * t)))
    x = drone / 2.2 + wind * 0.55
    fade = np.clip(t / 2.5, 0, 1) * np.clip((sec - t) / 2.5, 0, 1)
    return _norm(x * fade, 1.0)


SYNTH = {
    "transition": sfx_transition, "pop": sfx_pop, "tick": sfx_tick, "chime": sfx_chime,
    "impact": sfx_impact, "reveal": sfx_reveal, "outro": sfx_outro,
    "story_turn": sfx_story_turn, "story_boom": sfx_story_boom, "story_tap": sfx_story_tap,
    "story_dong": sfx_story_dong, "story_bell": sfx_story_bell,
}


def _load_wav_mono(path):
    with wave.open(str(path), "rb") as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(w.getnframes())
    if sw != 2:
        raise ValueError("chỉ hỗ trợ WAV 16-bit")
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    if sr != SFX_SR:
        idx = np.arange(0, len(x), sr / SFX_SR)
        x = np.interp(idx, np.arange(len(x)), x)
    return x


_CACHE = {}


def get_sfx(name):
    if name not in _CACHE:
        custom = ROOT / "assets" / "sfx" / f"{name}.wav"
        _CACHE[name] = _load_wav_mono(custom) if custom.exists() else SYNTH[name]()
    return _CACHE[name]


# ======================================================================= lịch phát hiệu ứng
def _slots(n, t0, t1):
    if n <= 0:
        return []
    if n == 1:
        return [t0]
    return [t0 + (t1 - t0) * i / (n - 1) for i in range(n)]


def story_events(scene, is_first):
    """Lịch hiệu ứng cho phong cách kể chuyện (khớp hoạt ảnh mờ dần trong scene.html)."""
    t, d = scene["type"], scene["dur"]
    ev = []
    # chuyển cảnh: chỉ tan hình, không chèn tiếng (nhạc nền dẫn dắt) — muốn có tiếng thì đặt file
    # assets/sfx/story_turn.wav, máy sẽ dùng file đó
    if not is_first and (ROOT / "assets" / "sfx" / "story_turn.wav").exists():
        ev.append((-0.32, "story_turn", 0.75))
    if t == "hook":
        ev.append((0.0, "story_boom", 1.0))
    elif t in ("explain", "timeline"):
        n = len(scene.get("bullets") or scene.get("items") or [])
        a, b = (0.7, max(0.8, d * 0.62)) if t == "explain" else (0.5, max(0.6, d * 0.65))
        ev += [(x + 0.1, "story_tap", 0.7) for x in _slots(n, a, b)]
    elif t == "compare":
        ev += [(0.35, "story_tap", 0.7), (min(0.85, d * 0.3) + 0.1, "story_tap", 0.7)]
    elif t == "number":
        ev.append((0.3, "story_dong", 0.6))
    elif t == "text":
        ev.append((0.25, "story_dong", 0.55))
    elif t == "outro":
        ev.append((0.1, "story_bell", 0.7))
    return ev


def scene_events(scene, is_first, style=""):
    """Trả về [(giây_tương_đối, tên_sfx, độ_to)] khớp với hoạt ảnh trong templates/scene.html."""
    if style == "story":
        return story_events(scene, is_first)
    t, d = scene["type"], scene["dur"]
    ev = []
    if not is_first:
        ev.append((-0.14, "transition", 0.8))
    if t == "hook":
        ev += [(0.0, "impact", 1.0), (0.3, "chime", 0.55)]
    elif t == "explain":
        if scene.get("icon"):
            ev.append((0.05, "pop", 0.7))
        n = len(scene.get("bullets") or [])
        ev += [(x + 0.05, "pop", 0.85) for x in _slots(n, 0.7, max(0.8, d * 0.62))]
    elif t == "compare":
        ev += [(0.3, "pop", 0.8), (0.58, "tick", 0.9), (min(0.85, d * 0.3) + 0.05, "pop", 0.8)]
        if scene.get("winner") in ("left", "right"):
            ev.append((d * 0.45, "chime", 0.6))
    elif t == "number":
        ev += [(0.18, "pop", 0.8), (1.45, "chime", 0.8)]
    elif t == "timeline":
        n = len(scene.get("items") or [])
        ev += [(x + 0.08, "tick", 1.0) for x in _slots(n, 0.5, max(0.6, d * 0.65))]
    elif t == "text":
        ev.append((0.22, "reveal", 0.75))
    elif t == "outro":
        ev.append((0.05, "outro", 0.9))
    return ev


def build_sfx_track(scenes, total, out_path, volume=0.5, style="", ambience=0.0):
    n = int((total + 1.5) * SFX_SR)
    track = np.zeros(n)
    if ambience > 0:
        custom = ROOT / "assets" / "sfx" / "ambience.wav"
        pad = _load_wav_mono(custom) if custom.exists() else ambience_pad(total + 1.5)
        pad = np.resize(pad, n) if len(pad) < n else pad[:n]
        track += pad * ambience
    for i, s in enumerate(scenes):
        for rel, name, gain in scene_events(s, i == 0, style):
            clip = get_sfx(name) * gain
            st = int(max(0.0, s["start"] + rel) * SFX_SR)
            en = min(n, st + len(clip))
            track[st:en] += clip[:en - st]
    track = np.clip(track * volume, -1, 1)
    with wave.open(str(out_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SFX_SR)
        w.writeframes((track * 32767).astype(np.int16).tobytes())


# ======================================================================= nhấn nhá giọng đọc
# Thẻ đặt ĐẦU câu, áp dụng cho cả câu đó:
#   [nhấn]  đọc chậm hơn, to hơn, giọng hơi cao — dùng cho câu "đinh" / sự thật bất ngờ
#   [nhanh] đọc nhanh — câu dẫn, câu phụ
#   [chậm]  đọc chậm, rõ — con số, tên riêng
#   [cao]   giọng cao hơn, hào hứng
#   [trầm]  giọng thấp hơn, bí ẩn
#   [nhỏ]   nói nhỏ lại, như kể bí mật
#   [ngừng] thêm khoảng lặng 0,5 giây trước câu
# Dấu "…" giữa câu = ngừng hồi hộp (tách thành 2 đoạn, chèn khoảng lặng).
# Các thẻ khác trong ngoặc vuông (vd [cười]) được giữ nguyên cho VieNeu.
STYLES = {
    "nhấn": {"tempo": 0.9, "pitch": 1.03, "gain_db": 2.5},
    "nhan": {"tempo": 0.9, "pitch": 1.03, "gain_db": 2.5},
    "nhanh": {"tempo": 1.12},
    "chậm": {"tempo": 0.88},
    "cham": {"tempo": 0.88},
    "cao": {"pitch": 1.045, "gain_db": 1.0},
    "trầm": {"pitch": 0.96, "tempo": 0.95},
    "tram": {"pitch": 0.96, "tempo": 0.95},
    "nhỏ": {"gain_db": -5.0, "tempo": 0.96},
    "nho": {"gain_db": -5.0, "tempo": 0.96},
}
PAUSE_TAGS = {"ngừng", "ngung"}
TAG_RE = re.compile(r"\[([^\]]+)\]")


def _merge(a, b):
    out = dict(a)
    for k, v in b.items():
        if k == "gain_db":
            out[k] = out.get(k, 0) + v
        else:
            out[k] = out.get(k, 1.0) * v
    return out


def parse_voice(text, scene_type="", auto=True, pauses=None):
    """Tách lời thoại 1 cảnh thành các đoạn [{"tts": chữ cho máy đọc, "show": chữ phụ đề,
    "style": {...}, "pause_before": giây, "pause_after": giây}]."""
    p = {"ellipsis": 0.38, "period": 0.16, "comma": 0.0, "exclaim": 0.22, "question": 0.34, "tag": 0.5}
    if pauses:
        p.update(pauses)
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    segs = []
    for si, sent in enumerate(sentences):
        style, pause_before = {}, 0.0
        while True:
            m = re.match(r"\s*\[([^\]]+)\]\s*", sent)
            if not m:
                break
            tag = m.group(1).strip().lower()
            if tag in STYLES:
                style = _merge(style, STYLES[tag])
            elif tag in PAUSE_TAGS:
                pause_before += p["tag"]
            else:
                break  # thẻ cảm xúc của VieNeu, để nguyên
            sent = sent[m.end():]
        if auto and not style:
            if scene_type == "hook" and si == 0:
                style = {"tempo": 0.94, "gain_db": 1.5, "pitch": 1.02}
            elif sent.rstrip().endswith("!"):
                style = {"pitch": 1.02, "gain_db": 0.8}
        parts = [x.strip() for x in re.split(r"\s*(?:…|\.\.\.)\s*", sent) if x.strip()]
        for pi, part in enumerate(parts):
            last = pi == len(parts) - 1
            if not last:
                after = p["ellipsis"]
            elif part.endswith("?"):
                after = p["question"]
            elif part.endswith("!"):
                after = p["exclaim"]
            else:
                after = p["period"]
            tts = part if last else part + ","
            segs.append({
                "tts": tts,
                "show": TAG_RE.sub("", part).strip() + ("" if last else "…"),
                "style": style,
                "pause_before": pause_before if pi == 0 else 0.0,
                "pause_after": after,
            })
    if segs:
        segs[-1]["pause_after"] = 0.0
    return segs


def style_filter(style):
    """Chuỗi bộ lọc ffmpeg cho 1 đoạn: đổi cao độ (asetrate) + tốc độ (atempo) + âm lượng."""
    tempo = float(style.get("tempo", 1.0))
    pitch = float(style.get("pitch", 1.0))
    gain = float(style.get("gain_db", 0.0))
    f = []
    if abs(pitch - 1) > 1e-3:
        f.append(f"asetrate=24000*{pitch:.4f},aresample=24000")
        tempo = tempo / pitch
    if abs(tempo - 1) > 1e-3:
        f.append(f"atempo={max(0.5, min(2.0, tempo)):.4f}")
    if abs(gain) > 1e-3:
        f.append(f"volume={gain:.2f}dB")
    return ",".join(f)


# Chuỗi xử lý giọng kiểu "radio": cắt ù trầm, giảm đục, tăng độ rõ, nén nhẹ.
VOICE_CHAIN = ("highpass=f=75,"
               "equalizer=f=230:t=q:w=1.0:g=-2.5,"
               "equalizer=f=3200:t=q:w=1.2:g=3.0,"
               "equalizer=f=9000:t=q:w=1.5:g=1.5,"
               "acompressor=threshold=-20dB:ratio=3:attack=6:release=90:makeup=3,"
               "alimiter=limit=0.95")
