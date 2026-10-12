"""
ÂM THANH VÀ GIỌNG ĐỌC (kế hoạch, mục "🎧 Âm thanh và giọng đọc").

1. Chuẩn hóa chữ trước khi đọc (chỉ bản gửi cho Gemini, chữ trên màn hình giữ nguyên):
   số → chữ, viết tắt / đơn vị → chữ, tên nước ngoài theo tu_dien_phat_am.json.
2. Chỉ dẫn sắc thái giọng theo loai_canh (hook, vong_lap, boi_canh, leo_thang, cu_lat, ket).
3. Thư viện tiếng động assets/sfx/<loại>/: file thật (CC0/PD, ghi nguồn trong nguon.json cùng thư mục) nếu có,
   không thì dùng âm TỰ TỔNG HỢP bằng code (không bản quyền, tự lưu thành assets/sfx/<loại>/tu_tao.wav).
4. Dựng "lớp tiếng động" cho cả video: tiếng nền theo cảnh (nhỏ hơn giọng ~20 dB), tiếng nhấn ở hook,
   tiếng "vút" khi đổi nơi chốn, tiếng dâng lên + khoảng lặng trước cú lật.
"""
import json
import re
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
SFX_DIR = ROOT / "assets" / "sfx"
DICT_FILE = ROOT / "tu_dien_phat_am.json"
SR = 44100

# ------------------------------------------------------------------ 1. chuẩn hóa chữ
DIGITS = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]


def _read3(n, full):
    """Đọc số < 1000. full=True: luôn đọc hàng trăm (kể cả 'không trăm')."""
    tr, ch, dv = n // 100, n // 10 % 10, n % 10
    out = []
    if tr or full:
        out += [DIGITS[tr], "trăm"]
    if ch == 0:
        if dv and (tr or full):
            out += ["linh", DIGITS[dv]]
        elif dv:
            out.append(DIGITS[dv])
    elif ch == 1:
        out.append("mười")
        if dv:
            out.append("lăm" if dv == 5 else DIGITS[dv])
    else:
        out += [DIGITS[ch], "mươi"]
        if dv == 1:
            out.append("mốt")
        elif dv == 5:
            out.append("lăm")
        elif dv == 4:
            out.append("tư")
        elif dv:
            out.append(DIGITS[dv])
    return out


def so_thanh_chu(n):
    """Số nguyên -> chữ tiếng Việt (vd 1701 -> 'một nghìn bảy trăm linh một')."""
    n = int(n)
    if n == 0:
        return "không"
    units = ["", "nghìn", "triệu", "tỷ"]
    groups = []
    while n:
        groups.append(n % 1000)
        n //= 1000
    words = []
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if g == 0:
            continue
        words += _read3(g, full=(i < len(groups) - 1))
        if units[i]:
            words.append(units[i])
    return " ".join(words)


UNITS = [(r"km/h", "ki-lô-mét một giờ"), (r"km²", "ki-lô-mét vuông"), (r"km", "ki-lô-mét"), (r"kg", "ki-lô-gam"),
         (r"m²", "mét vuông"), (r"cm", "xăng-ti-mét"), (r"m", "mét"), (r"%", "phần trăm"), (r"°C", "độ C")]
ABBR = [(r"\bTCN\b", "trước Công nguyên"), (r"\bSCN\b", "sau Công nguyên"), (r"\bTK\b", "thế kỷ"),
        (r"\bThế chiến 1\b", "Thế chiến thứ nhất"), (r"\bThế chiến 2\b", "Thế chiến thứ hai")]


def _num_token(s):
    """'1.701' / '2,5' / '1911' -> chữ."""
    s = s.strip()
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        return so_thanh_chu(int(s.replace(".", "")))
    m = re.fullmatch(r"(\d+),(\d+)", s)
    if m:
        dec = m.group(2)
        dec_words = so_thanh_chu(int(dec)) if not dec.startswith("0") else " ".join(DIGITS[int(c)] for c in dec)
        return f"{so_thanh_chu(int(m.group(1)))} phẩy {dec_words}"
    return so_thanh_chu(int(s))


def load_dict():
    try:
        d = json.loads(DICT_FILE.read_text(encoding="utf-8"))
        return {k: v for k, v in d.items() if not k.startswith("_")}
    except Exception:
        return {}


def chuan_hoa(text, tu_dien=None):
    """Bản chữ gửi cho giọng đọc."""
    t = text
    for k, v in sorted((tu_dien if tu_dien is not None else load_dict()).items(), key=lambda kv: -len(kv[0])):
        t = re.sub(r"(?<!\w)" + re.escape(k) + r"(?!\w)", v, t)
    for rx, rep in ABBR:
        t = re.sub(rx, rep, t)
    # ngày/tháng: 14/4/1912 -> ngày mười bốn tháng tư năm ...
    def _date(m):
        d, mo, y = m.group(1), m.group(2), m.group(3)
        thang = "tư" if int(mo) == 4 else so_thanh_chu(int(mo))
        s = f"ngày {so_thanh_chu(int(d))} tháng {thang}"
        return s + (f" năm {so_thanh_chu(int(y))}" if y else "")
    t = re.sub(r"(?<![\d/])(\d{1,2})/(\d{1,2})(?:/(\d{4}))?(?![\d/])", _date, t)
    t = re.sub(r"(?<![\d/])(\d{1,2})/(\d{4})(?![\d/])",
               lambda m: f"tháng {'tư' if int(m.group(1)) == 4 else so_thanh_chu(int(m.group(1)))} năm {so_thanh_chu(int(m.group(2)))}", t)
    # số + đơn vị
    for u, rep in UNITS:
        t = re.sub(r"(\d[\d.,]*)\s*" + re.escape(u) + r"(?![\w²])", lambda m, rep=rep: f"{_num_token(m.group(1))} {rep}", t)
    t = re.sub(r"\d{1,3}(?:\.\d{3})+|\d+,\d+|\d+", lambda m: _num_token(m.group(0)), t)
    return re.sub(r"\s{2,}", " ", t).strip()


# ------------------------------------------------------------------ 2. sắc thái giọng theo đoạn
SAC_THAI = {
    "hook": "This is the HOOK: urgent, gripping, punchy delivery; lean on the strange detail; no slow intro.",
    "vong_lap": "Lower the voice slightly, as if sharing a secret with the listener; a little slower, intriguing.",
    "boi_canh": "Calm, clear, matter-of-fact storytelling; steady pace.",
    "leo_thang": "Building tension: gradually faster and more intense, like events are getting out of control.",
    "cu_lat": "THE TWIST: slow down, weigh each word, a short dramatic pause before the key phrase; restrained, not shouting.",
    "ket": "Closing line: deep, warm, slow and reflective; let the last words settle.",
    "chuong": "Start of a new chapter: calm and inviting, clear pacing.",
}


def sac_thai(loai):
    return SAC_THAI.get(loai or "", SAC_THAI["boi_canh"])


# ------------------------------------------------------------------ 3. tiếng động tự tổng hợp
def _t(sec):
    return np.arange(int(sec * SR)) / SR


def _lp(x, cutoff):
    """Lọc thông thấp 1 cực (nhanh, đủ cho tiếng nền)."""
    a = np.exp(-2 * np.pi * cutoff / SR)
    from scipy.signal import lfilter
    return lfilter([1 - a], [1, -a], x)


def _hp(x, cutoff):
    return x - _lp(x, cutoff)


def _bp(x, lo, hi):
    from scipy.signal import butter, sosfilt
    sos = butter(2, [lo / (SR / 2), min(0.99, hi / (SR / 2))], btype="band", output="sos")
    return sosfilt(sos, x)


def _smooth_noise(sec, rate, rng):
    """Đường cong ngẫu nhiên mượt (dùng làm biên độ dao động chậm)."""
    n = int(sec * SR)
    k = max(2, int(sec * rate) + 2)
    pts = rng.uniform(0, 1, k)
    return np.interp(np.linspace(0, k - 1, n), np.arange(k), pts)


def _norm(x, peak=0.8):
    m = float(np.max(np.abs(x))) or 1.0
    return (x / m * peak).astype(np.float32)


def s_gio(sec=12, seed=1):
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, int(sec * SR))
    env = 0.35 + 0.65 * _smooth_noise(sec, 0.35, rng) ** 1.5
    y = _bp(x, 180, 900) * env + 0.4 * _bp(x, 900, 2600) * env ** 2
    return _norm(y, 0.7)


def s_bien(sec=12, seed=2):
    rng = np.random.default_rng(seed)
    t = _t(sec)
    x = rng.normal(0, 1, len(t))
    swell = np.zeros_like(t)
    p = 0.0
    while p < sec:                      # từng con sóng 5-8 giây: dâng lên rồi vỡ, rút
        d = rng.uniform(5, 8)
        m = (t >= p) & (t < p + d)
        u = (t[m] - p) / d
        swell[m] = np.sin(np.pi * u) ** 2 * (0.6 + 0.4 * rng.random())
        p += d * rng.uniform(0.6, 0.85)
    y = _lp(x, 700) * (0.25 + swell) + 0.35 * _bp(x, 1500, 5000) * swell ** 3
    return _norm(y, 0.7)


def s_mua(sec=12, seed=3):
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, int(sec * SR))
    y = 0.5 * _bp(x, 800, 7000)
    drops = np.zeros_like(x)
    for p in rng.integers(0, len(x) - 400, int(sec * 60)):
        drops[p:p + 300] += rng.uniform(0.2, 1) * np.exp(-np.arange(300) / 40) * rng.normal(0, 1, 300)
    y += _hp(drops, 1200)
    return _norm(y, 0.6)


def s_sam(sec=6, seed=4):
    rng = np.random.default_rng(seed)
    t = _t(sec)
    x = rng.normal(0, 1, len(t))
    crack = _hp(x, 1500) * np.exp(-t / 0.08) * 0.8
    rumble = _lp(x, 120) * (np.exp(-t / 1.8) * (0.6 + 0.4 * _smooth_noise(sec, 4, rng)))
    return _norm(crack + 6 * rumble, 0.9)


def s_tim_dap(sec=8, bpm=72, seed=5):
    t = _t(sec)
    y = np.zeros_like(t)
    beat = 60 / bpm
    for k in range(int(sec / beat) + 1):
        for off, amp in ((0, 1.0), (0.28, 0.7)):
            p = k * beat + off
            m = (t >= p) & (t < p + 0.18)
            tt = t[m] - p
            y[m] += amp * np.sin(2 * np.pi * (55 - 60 * tt) * tt) * np.exp(-tt / 0.05)
    return _norm(_lp(y, 200), 0.9)


def s_dong_ho(sec=8, seed=6):
    rng = np.random.default_rng(seed)
    t = _t(sec)
    y = np.zeros_like(t)
    for k in range(int(sec * 2)):
        p = k * 0.5
        m = (t >= p) & (t < p + 0.03)
        tt = t[m] - p
        f = 3200 if k % 2 == 0 else 2600
        y[m] += np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.006) + 0.3 * rng.normal(0, 1, m.sum()) * np.exp(-tt / 0.003)
    return _norm(y, 0.7)


def s_radio(sec=8, seed=7):
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, int(sec * SR))
    y = _bp(x, 900, 3500) * (0.5 + 0.5 * _smooth_noise(sec, 3, rng))
    clicks = (rng.random(len(x)) < 0.0004) * rng.normal(0, 4, len(x))
    return _norm(y + clicks, 0.6)


def s_dien_bao(sec=8, seed=8, text="SOS CQD MGY"):
    """Tiếng điện báo Morse (tín hiệu cầu cứu của tàu biển đầu thế kỷ 20)."""
    morse = {"S": "...", "O": "---", "C": "-.-.", "Q": "--.-", "D": "-..", "M": "--", "G": "--.", "Y": "-.--"}
    unit = 0.07
    seq = []
    for word in text.split():
        for ch in word:
            for sym in morse.get(ch, ""):
                seq.append((1 if sym == "." else 3, True))
                seq.append((1, False))
            seq.append((2, False))
        seq.append((4, False))
    n = int(sec * SR)
    y = np.zeros(n)
    p = 0.0
    while p < sec:
        for length, on in seq:
            d = length * unit
            if on:
                a, b = int(p * SR), min(n, int((p + d) * SR))
                if a >= n:
                    break
                tt = np.arange(b - a) / SR
                y[a:b] += np.sin(2 * np.pi * 680 * tt) * np.minimum(1, np.minimum(tt, d - tt) / 0.004)
            p += d
        p += 1.0
    rng = np.random.default_rng(seed)
    return _norm(y + 0.05 * _bp(rng.normal(0, 1, n), 500, 3000), 0.6)


def s_vut(sec=0.9, seed=9):
    rng = np.random.default_rng(seed)
    t = _t(sec)
    x = rng.normal(0, 1, len(t))
    env = np.sin(np.pi * t / sec) ** 2
    from scipy.signal import butter, sosfilt
    out = np.zeros_like(x)
    blocks = 16
    for k in range(blocks):      # dải lọc quét từ trầm lên bổng
        a, b = k * len(x) // blocks, (k + 1) * len(x) // blocks
        f = 400 * (8 ** (k / blocks))
        sos = butter(2, [f / (SR / 2), min(0.99, 2.2 * f / (SR / 2))], btype="band", output="sos")
        out[a:b] = sosfilt(sos, x[a:b])
    return _norm(out * env, 0.8)


def s_hit(sec=2.5, seed=10):
    """Tiếng nhấn mạnh: trống trầm + tiếng vang."""
    rng = np.random.default_rng(seed)
    t = _t(sec)
    body = np.sin(2 * np.pi * (48 + 40 * np.exp(-t / 0.08)) * t) * np.exp(-t / 0.55)
    click = _hp(rng.normal(0, 1, len(t)), 2000) * np.exp(-t / 0.01) * 0.4
    tail = _lp(rng.normal(0, 1, len(t)), 300) * np.exp(-t / 0.9) * 0.25
    return _norm(body + click + tail, 0.95)


def s_rise(sec=2.2, seed=11):
    """Tiếng dâng lên trước cú lật: nhiễu và âm trầm tăng dần, tắt đột ngột."""
    rng = np.random.default_rng(seed)
    t = _t(sec)
    u = t / sec
    tone = np.sin(2 * np.pi * (70 + 160 * u ** 2) * t) * u ** 2
    noise = _bp(rng.normal(0, 1, len(t)), 600, 4000) * u ** 3
    y = 0.7 * tone + 0.5 * noise
    y[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    return _norm(y, 0.85)


def s_dong_co_tau(sec=12, seed=12):
    """Máy hơi nước của tàu biển: tiếng ầm trầm + nhịp piston đều."""
    rng = np.random.default_rng(seed)
    t = _t(sec)
    hum = _lp(rng.normal(0, 1, len(t)), 90) * 3
    pulse = (0.6 + 0.4 * np.sin(2 * np.pi * 1.6 * t)) * _lp(rng.normal(0, 1, len(t)), 250)
    return _norm(hum + pulse + 0.15 * np.sin(2 * np.pi * 42 * t), 0.7)


def s_coi_tau(sec=4.5, seed=13):
    """Còi tàu biển hơi nước: âm trầm nhiều bồi âm, lên dần rồi tắt."""
    t = _t(sec)
    env = np.clip(t / 0.35, 0, 1) * np.clip((sec - t) / 0.8, 0, 1)
    f = 108 * (1 + 0.004 * np.sin(2 * np.pi * 5 * t))
    y = sum(a * np.sin(2 * np.pi * f * k * t) for k, a in ((1, 1), (2, 0.6), (3, 0.45), (4, 0.25), (5, 0.15), (6, 0.08)))
    rng = np.random.default_rng(seed)
    y = y * env + 0.08 * _bp(rng.normal(0, 1, len(t)), 300, 2000) * env
    return _norm(y, 0.8)


def s_kim_loai(sec=4, seed=14):
    """Tiếng thép cọt kẹt, rên rỉ của thân tàu."""
    rng = np.random.default_rng(seed)
    t = _t(sec)
    f0 = 140 + 60 * _smooth_noise(sec, 1.2, rng)
    ph = 2 * np.pi * np.cumsum(f0) / SR
    y = sum(a * np.sin(k * ph * 1.37 ** (k - 1)) for k, a in ((1, 1), (2, 0.5), (3, 0.3)))
    env = np.sin(np.pi * t / sec) ** 1.5 * (0.5 + 0.5 * _smooth_noise(sec, 3, rng))
    return _norm(y * env, 0.6)


def s_nuoc(sec=4, seed=15):
    """Tiếng nước bắn, sóng vỗ mạn xuồng."""
    rng = np.random.default_rng(seed)
    t = _t(sec)
    x = rng.normal(0, 1, len(t))
    y = np.zeros_like(t)
    for p in rng.uniform(0, sec - 0.5, int(sec * 3)):
        m = (t >= p) & (t < p + 0.45)
        tt = t[m] - p
        y[m] += np.exp(-tt / 0.12) * rng.uniform(0.3, 1)
    return _norm(_bp(x, 300, 3000) * (0.15 + y), 0.6)


def s_dam_dong(sec=10, seed=16):
    """Tiếng người xôn xao ở xa (không rõ lời)."""
    rng = np.random.default_rng(seed)
    t = _t(sec)
    y = np.zeros_like(t)
    for _ in range(14):           # mỗi "giọng" là nhiễu lọc theo vùng nói, biên độ lên xuống như câu nói
        f = rng.uniform(250, 700)
        v = _bp(rng.normal(0, 1, len(t)), f, f * 2.2)
        syl = (_smooth_noise(sec, rng.uniform(3, 6), rng) > 0.45) * _smooth_noise(sec, 0.4, rng)
        y += v * _lp(syl.astype(float), 12)
    return _norm(_lp(y, 2500), 0.55)


def s_buoc_chan(sec=6, seed=17):
    rng = np.random.default_rng(seed)
    t = _t(sec)
    y = np.zeros_like(t)
    for k in range(int(sec / 0.55)):
        p = k * 0.55 + rng.uniform(-0.03, 0.03)
        m = (t >= p) & (t < p + 0.12)
        tt = t[m] - p
        y[m] += _lp(rng.normal(0, 1, m.sum()), 500) * np.exp(-tt / 0.025) * 4
    return _norm(y, 0.7)


def s_lat_giay(sec=3, seed=18):
    rng = np.random.default_rng(seed)
    t = _t(sec)
    y = np.zeros_like(t)
    for p in (0.2, 1.3, 2.2):
        m = (t >= p) & (t < p + 0.4)
        tt = t[m] - p
        y[m] += _bp(rng.normal(0, 1, m.sum()), 2000, 8000) * np.sin(np.pi * tt / 0.4) ** 2
    return _norm(y, 0.5)


def s_lua(sec=10, seed=19):
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, int(sec * SR))
    y = _lp(x, 400) * 0.8
    pops = (rng.random(len(x)) < 0.0006) * rng.normal(0, 6, len(x))
    return _norm(y + _hp(pops, 1500), 0.6)


def s_tau_hoa(sec=10, seed=20):
    rng = np.random.default_rng(seed)
    t = _t(sec)
    y = np.zeros_like(t)
    for k in range(int(sec / 0.32)):
        p = k * 0.32
        m = (t >= p) & (t < p + 0.2)
        tt = t[m] - p
        y[m] += _bp(rng.normal(0, 1, m.sum()), 200, 1500) * np.exp(-tt / 0.06) * (1.2 if k % 4 == 0 else 0.7)
    rumble = _lp(rng.normal(0, 1, len(t)), 100) * 2
    return _norm(y + rumble, 0.7)


def s_may_bay(sec=10, seed=21):
    """Máy bay cánh quạt bay ngang xa."""
    rng = np.random.default_rng(seed)
    t = _t(sec)
    f = 95 * (1 + 0.05 * np.sin(2 * np.pi * 0.08 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = sum(a * np.sin(k * ph) for k, a in ((1, 1), (2, 0.7), (3, 0.5), (4, 0.3)))
    env = np.sin(np.pi * t / sec) ** 1.2
    return _norm((y + 0.3 * _lp(rng.normal(0, 1, len(t)), 600)) * env, 0.6)


SYNTH = {"gio": s_gio, "bien": s_bien, "mua": s_mua, "bao_sam": s_sam, "sam": s_sam, "tim_dap": s_tim_dap,
         "dong_ho": s_dong_ho, "radio": s_radio, "dien_bao": s_dien_bao, "vut": s_vut, "hit": s_hit, "rise": s_rise,
         "dong_co_tau": s_dong_co_tau, "coi_tau": s_coi_tau, "kim_loai": s_kim_loai, "nuoc": s_nuoc,
         "dam_dong": s_dam_dong, "buoc_chan": s_buoc_chan, "lat_giay": s_lat_giay, "lua": s_lua,
         "tau_hoa": s_tau_hoa, "may_bay": s_may_bay}
# tiếng một lần (không lặp làm nền)
ONE_SHOT = {"hit", "rise", "vut", "coi_tau", "bao_sam", "sam", "lat_giay"}


def _read_any(path):
    """Đọc file âm thanh bất kỳ -> mono float32 44,1 kHz (dùng ffmpeg cho mp3/ogg)."""
    import subprocess
    import make_video as mv
    raw = subprocess.run([mv.ffmpeg_exe(), "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def _write_wav(path, x):
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


_FETCH_FAILED = set()


def _fetch_real(d):
    """Tải tiếng động thật (CC0/PD, ghi trong <thư mục>/nguon.json) nếu chưa có file."""
    f = d / "nguon.json"
    if not f.exists() or d in _FETCH_FAILED:
        return
    try:
        info = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return
    for it in info.get("files", []):
        dest = d / it["file"]
        if dest.exists() or not it.get("url"):
            continue
        try:
            import urllib.request
            req = urllib.request.Request(it["url"], headers={
                "User-Agent": "NguoiGacSuVideo/1.0 (https://github.com/thanhnt1910/fact-video; educational history videos)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                dest.write_bytes(r.read())
        except Exception as e:
            _FETCH_FAILED.add(d)
            print(f"     (không tải được tiếng động {it['file']}: {e}; dùng âm tự tổng hợp)")


def load_sfx(label, variant=0):
    """Mẫu âm cho 1 nhãn: ưu tiên file thật trong assets/sfx/<nhãn>/ (đã ghi nguồn), không có thì tự tổng hợp."""
    d = SFX_DIR / label
    _fetch_real(d)
    real = sorted(p for p in d.glob("*") if p.suffix.lower() in (".wav", ".mp3", ".ogg", ".flac")
                  and not p.name.startswith("tu_tao")) if d.exists() else []
    if real:
        return _read_any(real[variant % len(real)])
    if label not in SYNTH:
        return None
    f = d / "tu_tao.wav"
    if not f.exists():
        _write_wav(f, SYNTH[label]())
        if not (d / "nguon.json").exists():
            (d / "nguon.json").write_text(json.dumps({"tu_tao.wav": {
            "nguon": "tự tổng hợp bằng code (am_thanh.py, numpy/scipy) trong repo fact-video",
                "giay_phep": "không có bản quyền của bên thứ ba (âm do chính kênh tạo ra)"}}, ensure_ascii=False, indent=1),
                encoding="utf-8")
    with wave.open(str(f)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32767


def _db(x):
    return 10 ** (x / 20)


def _rms(x):
    return float(np.sqrt(np.mean(x.astype(np.float64) ** 2)) + 1e-9)


def build_bed(events, total, voice_rms=0.1):
    """events: [{"label", "start", "dur", "db"}] (db: mức so với RMS giọng; nền mặc định -20).
    Trả về mảng mono float32 dài total giây."""
    out = np.zeros(int(total * SR) + 1, np.float32)
    for k, e in enumerate(events):
        x = load_sfx(e["label"], k)
        if x is None or not len(x):
            continue
        a = int(max(0, e["start"]) * SR)
        if a >= len(out):
            continue
        if e["label"] in ONE_SHOT or e.get("one_shot"):
            seg = x[: len(out) - a]
            level = _db(e.get("db", -12)) * voice_rms / max(1e-6, float(np.max(np.abs(seg))) * 0.35)
        else:
            n = int(min(e["dur"], total - e["start"]) * SR)
            if n <= 0:
                continue
            reps = int(np.ceil(n / len(x))) + 1
            seg = np.tile(x, reps)[(k * 7919) % len(x):][:n]          # bắt đầu ở chỗ khác nhau cho đỡ lặp
            fade = min(int(0.6 * SR), n // 3)
            if fade > 0:
                seg = seg.copy()
                seg[:fade] *= np.linspace(0, 1, fade)
                seg[-fade:] *= np.linspace(1, 0, fade)
            level = _db(e.get("db", -20)) * voice_rms / _rms(seg)
        b = min(len(out), a + len(seg))
        out[a:b] += (seg[: b - a] * level).astype(np.float32)
    return out


def save_bed(path, bed):
    _write_wav(Path(path), bed)


def labels_ok(labels):
    """Nhãn hợp lệ (có file thật hoặc có thể tự tổng hợp)."""
    return [lb for lb in labels if lb in SYNTH or (SFX_DIR / lb).exists()]


# ------------------------------------------------------------------ 4. trộn âm thanh
def _voice_rms(wav_path):
    with wave.open(str(wav_path)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32767
    win = 1024
    k = len(x) // win
    if not k:
        return 0.1
    r = np.sqrt((x[:k * win].reshape(k, win) ** 2).mean(1))
    sp = r[r > np.percentile(r, 50)]
    return float(np.sqrt(np.mean(sp ** 2))) if len(sp) else 0.1


def voice_bed(narration_wav, events, total, quiet=None):
    """Lớp tiếng động (mono 44,1 kHz) có mức tính theo độ lớn giọng; quiet=(a, b): lặng hẳn trước cú lật."""
    bed = build_bed(events, total, _voice_rms(narration_wav))
    if quiet:
        a, b = int(quiet[0] * SR), int(quiet[1] * SR)
        r = int(0.08 * SR)
        g = np.ones(len(bed), np.float32)
        g[a:b] = 0
        g[max(0, a - r):a] *= np.linspace(1, 0, a - max(0, a - r))
        g[b:b + r] *= np.linspace(0, 1, len(g[b:b + r]))
        # tiếng dâng lên kết thúc đúng lúc lặng: giữ nguyên phần trước a
        bed = bed * g
    return bed


def mix(video, narration_wav, total, music_track, out, cfg, bed_wav=None, quiet=None, fade_out=2.5,
        music_lufs=None, log=print):
    """Giọng (lọc ù, nén nhẹ, giảm 's' chói, chuẩn -16 LUFS) + nhạc nền thấp hơn giọng ~18-20 dB, tự hạ khi có giọng
    + lớp tiếng động; cả video chuẩn hóa -14 LUFS, đỉnh không quá -1 dBTP (kế hoạch, mục Âm thanh A.)."""
    import audio_fx
    import make_video as mv
    voice_chain = (audio_fx.VOICE_CHAIN.replace("alimiter", "deesser=i=0.4:m=0.5:f=0.5:s=o,alimiter")
                   + ",loudnorm=I=-16:TP=-2:LRA=9")
    args = ["-i", str(video), "-i", str(narration_wav)]
    graph = [f"[1:a]{voice_chain},aresample=44100,asplit=2[v][vk]"]
    mix_in = ["[v]"]
    idx = 2
    if music_track:
        args += ["-stream_loop", "-1", "-i", str(music_track)]
        ml = music_lufs if music_lufs is not None else cfg.get("music_lufs_moi", -34)
        q = f",volume=enable='between(t,{quiet[0]:.2f},{quiet[1]:.2f})':volume=0.05" if quiet else ""
        graph += [f"[{idx}:a]loudnorm=I={ml}:LRA=11:TP=-8,aresample=44100,afade=t=in:d=1.2,"
                  f"afade=t=out:st={max(0, total - fade_out):.2f}:d={fade_out}{q}[mr]",
                  f"[mr][vk]sidechaincompress=threshold=0.05:ratio=2:attack=60:release=600[m]"]
        mix_in.append("[m]")
        idx += 1
    else:
        graph.append("[vk]anullsink")
    if bed_wav:
        args += ["-i", str(bed_wav)]
        graph.append(f"[{idx}:a]aresample=44100,afade=t=out:st={max(0, total - fade_out):.2f}:d={fade_out}[s]")
        mix_in.append("[s]")
    graph.append(f"{''.join(mix_in)}amix=inputs={len(mix_in)}:duration=first:normalize=0,"
                 "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]")
    mv.run_ffmpeg(args + ["-filter_complex", ";".join(graph), "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                          "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart",
                          str(out)])
    try:   # ghi lại độ lớn thực tế để kiểm tra
        import subprocess
        r = subprocess.run([mv.ffmpeg_exe(), "-hide_banner", "-nostats", "-i", str(out), "-af", "ebur128=peak=true",
                            "-f", "null", "-"], capture_output=True, text=True)
        tail = r.stderr[r.stderr.rfind("Summary:"):]
        I = re.search(r"I:\s*(-?[\d.]+) LUFS", tail)
        P = re.search(r"Peak:\s*(-?[\d.]+) dBFS", tail)
        log(f"  🔈 Âm lượng cuối: {I.group(1) if I else '?'} LUFS, đỉnh {P.group(1) if P else '?'} dBTP")
    except Exception:
        pass
