"""
CHUYỂN ĐỘNG CHO ẢNH TĨNH (dùng chung cho video ngắn và video dài)

1. Parallax 2.5D: ước lượng độ sâu của ảnh (mô hình Depth Anything V2 Small, chạy CPU bằng onnxruntime),
   rồi khi máy quay lướt, vật ở gần dịch nhiều hơn vật ở xa -> ảnh tĩnh trông như cảnh 3D.
   - Bản đồ độ sâu lưu ở assets/ai_cache/depth (GitHub Actions lưu đệm sẵn), mỗi ảnh chỉ tính 1 lần.
   - Không tải được mô hình / lỗi: trả về None -> cảnh đó dùng chuyển động cũ (Ken Burns), video không hỏng.

2. Hiệu ứng hạt phủ lên ảnh: bụi bay (dust), tàn lửa (embers), mưa (rain), tuyết (snow), sương (mist).
   - Kịch bản có thể ghi "fx": "rain" | "snow+dust" | "none" cho từng cảnh / từng đoạn video dài.
   - Không ghi thì tự chọn theo nội dung (mô tả ảnh AI, lời kể, tên ảnh): "jungle, misty" -> sương...

Cấu hình trong config.json:
  "motion": {"parallax": true, "parallax_strength": 1.0, "fx": true, "fx_strength": 1.0}

  python motion.py anh.jpg      -> thử: in ra hiệu ứng tự chọn, lưu bản đồ độ sâu cạnh ảnh
"""
import hashlib
import math
import os
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlparse

import numpy as np

ROOT = Path(__file__).resolve().parent
DEPTH_CACHE = ROOT / "assets" / "ai_cache" / "depth"
MODEL_DIR = Path(os.environ.get("FV_MODEL_DIR", Path.home() / ".cache" / "fact-video"))
MODEL_FILE = "depth_anything_v2_vits.onnx"
# Depth Anything V2 Small (giấy phép Apache-2.0), bản ONNX đóng sẵn
MODEL_URL = "https://github.com/fabio-sim/Depth-Anything-ONNX/releases/download/v2.0.0/depth_anything_v2_vits.onnx"
DEPTH_VER = "v2s-1"      # đổi khi đổi cách xử lý bản đồ độ sâu -> tính lại

FX_NAMES = ("dust", "embers", "rain", "snow", "mist", "rays", "lightning", "flicker", "shake")
DEFAULTS = {"parallax": True, "parallax_strength": 1.0, "fx": True, "fx_strength": 1.0,
            "dof": 0.6,              # đổi tiêu điểm theo độ sâu (0 = tắt)
            "transition": "zoom",    # "zoom" = lao vào ảnh + vệt sáng; "fade" = tan mờ như cũ
            "light": True,           # tia nắng, chớp, lửa hắt, rung máy
            "fx_auto": True}         # False: chỉ dùng hiệu ứng ghi tay "fx" trong kịch bản


def settings(cfg):
    m = dict(DEFAULTS)
    m.update((cfg or {}).get("motion") or {})
    return m


def _log(msg):
    print(msg, flush=True)


def _path(src):
    s = str(src)
    return unquote(urlparse(s).path) if s.startswith("file:") else s


# ------------------------------------------------------------------ độ sâu
_SESSION = None
_FAILED = False


def _session(log=_log):
    global _SESSION, _FAILED
    if _SESSION is not None or _FAILED:
        return _SESSION
    try:
        import onnxruntime as ort
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        f = MODEL_DIR / MODEL_FILE
        if not f.exists() or f.stat().st_size < 50_000_000:
            log("     ⬇️  tải mô hình độ sâu Depth Anything V2 (khoảng 100 MB, chỉ lần đầu)")
            tmp = f.with_suffix(".part")
            urllib.request.urlretrieve(MODEL_URL, tmp)
            tmp.replace(f)
        so = ort.SessionOptions()
        so.log_severity_level = 3
        _SESSION = ort.InferenceSession(str(f), so, providers=["CPUExecutionProvider"])
    except Exception as e:
        _FAILED = True
        log(f"     ⚠️  không dùng được mô hình độ sâu ({e}) -> ảnh chỉ chuyển động kiểu cũ")
    return _SESSION


def _infer(rgb):
    """rgb uint8 HxWx3 -> độ sâu nghịch đảo (lớn = gần) HxW float32."""
    import cv2
    sess = _session()
    if sess is None:
        return None
    inp = sess.get_inputs()[0]
    size = inp.shape[2] if isinstance(inp.shape[2], int) else 518
    x = cv2.resize(rgb, (size, size), interpolation=cv2.INTER_CUBIC).astype(np.float32) / 255.0
    x = (x - np.array([0.485, 0.456, 0.406], np.float32)) / np.array([0.229, 0.224, 0.225], np.float32)
    x = x.transpose(2, 0, 1)[None]
    out = np.asarray(sess.run(None, {inp.name: x})[0]).reshape(size, size).astype(np.float32)
    return cv2.resize(out, (rgb.shape[1], rgb.shape[0]), interpolation=cv2.INTER_CUBIC)


def _prepare(d):
    """Chuẩn hóa về 0..1, làm mềm, nới rộng vật ở gần ra mép (che chỗ ảnh bị kéo giãn khi dịch)."""
    import cv2
    lo, hi = np.percentile(d, 2), np.percentile(d, 98)
    d = np.clip((d - lo) / max(1e-6, hi - lo), 0, 1).astype(np.float32)
    h, w = d.shape
    k = max(3, int(min(w, h) * 0.012) | 1)
    d = cv2.dilate(d, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    d = cv2.GaussianBlur(d, (0, 0), sigmaX=min(w, h) * 0.006)
    return d


def depth_map(src, log=_log):
    """Đường dẫn PNG xám 8-bit (trắng = gần), cùng kích thước ảnh; None nếu không tính được."""
    import cv2
    from PIL import Image
    p = Path(_path(src))
    if not p.is_file():
        return None
    try:
        key = hashlib.sha1(p.read_bytes() + DEPTH_VER.encode()).hexdigest()[:16]
    except Exception:
        return None
    out = DEPTH_CACHE / f"{key}.png"
    if out.exists():
        return out
    if _session(log) is None:
        return None
    try:
        im = Image.open(p).convert("RGB")
        if max(im.size) > 1600:          # mô hình chỉ nhìn 518 px, ảnh to chỉ làm chậm
            im.thumbnail((1600, 1600))
        d = _infer(np.asarray(im))
        if d is None:
            return None
        d = _prepare(d)
        DEPTH_CACHE.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(out), (d * 255 + 0.5).astype(np.uint8))
        return out
    except Exception as e:
        log(f"     ⚠️  không tính được độ sâu cho {p.name}: {e}")
        return None


def load_depth(path, size):
    """PNG độ sâu -> float32 0..1 đúng kích thước (w, h)."""
    import cv2
    d = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if d is None:
        return None
    if (d.shape[1], d.shape[0]) != tuple(size):
        d = cv2.resize(d, tuple(size), interpolation=cv2.INTER_LINEAR)
    return d.astype(np.float32) / 255.0


# ------------------------------------------------------------------ đường đi máy quay (giống hệt bên scene.html)
def camera(kind, p, strength=1.0):
    """Trả về (cx, cy, zk): độ dịch ngang/dọc (tỉ lệ khung) cho vật ở gần nhất, và mức "đẩy vào" theo độ sâu.
    p: 0..1 tiến độ cảnh. kind 0..3 xoay vòng theo thứ tự cảnh."""
    s = strength
    e = 0.5 - 0.5 * math.cos(math.pi * p)       # mượt ở hai đầu
    if kind == 0:     # đẩy vào, hơi trôi lên
        return 0.006 * s * (e - 0.5), -0.008 * s * (e - 0.5), 0.07 * s * e
    if kind == 1:     # lia trái -> phải
        return 0.030 * s * (e - 0.5), 0.0, 0.02 * s * e
    if kind == 2:     # kéo ra
        return -0.006 * s * (e - 0.5), 0.006 * s * (e - 0.5), 0.07 * s * (1 - e)
    return -0.030 * s * (e - 0.5), 0.004 * s * (e - 0.5), 0.02 * s * e   # lia phải -> trái


FOCUS = 0.45     # độ sâu "đứng yên"; gần hơn thì dịch theo một chiều, xa hơn dịch chiều ngược lại


def edge_taper(w, h, frac=0.06):
    """Mặt nạ 0 ở mép -> 1 ở trong: mép ảnh không dịch (dùng cho ảnh đặt giữa nền mờ)."""
    fx = np.clip(np.minimum(np.arange(w), np.arange(w)[::-1]) / max(1, w * frac), 0, 1)
    fy = np.clip(np.minimum(np.arange(h), np.arange(h)[::-1]) / max(1, h * frac), 0, 1)
    m = np.outer(fy, fx).astype(np.float32)
    return m * m * (3 - 2 * m)


def parallax_maps(xs, ys, d, cw, ch, cam):
    """Biến tọa độ lấy mẫu (xs, ys trên ảnh kích thước cw x ch) theo độ sâu d (đã ở cùng lưới).
    Trả về (mx, my) cho cv2.remap."""
    cx, cy, zk = cam
    dd = d - FOCUS
    # lấy mẫu lệch theo độ sâu; dấu trừ ở phần zk: vật gần phình to khi máy đẩy vào
    mx = xs + dd * (cx * cw - (xs - cw * 0.5) * zk)
    my = ys + dd * (cy * ch - (ys - ch * 0.5) * zk)
    return mx, my


# ------------------------------------------------------------------ nhịp thời gian dùng chung (giống hệt bên scene.html)
def _hash(k):
    v = math.sin(k * 12.9898 + 78.233) * 43758.5453
    return v - math.floor(v)


def focal(i, p):
    """Độ sâu đang được lấy nét. Cảnh chẵn: kéo nét từ xa vào gần (lộ chủ thể); cảnh lẻ: nét ở gần, nền mềm."""
    if i % 2 == 0:
        e = min(1.0, p / 0.45)
        e = e * e * (3 - 2 * e)
        return 0.15 + 0.65 * e
    return 0.75


def lightning(t):
    """0..1: chớp đôi, khoảng 6,5 giây một lần ở thời điểm ngẫu nhiên cố định."""
    k = math.floor(t / 6.5)
    dt = t - (k * 6.5 + _hash(k) * 4.0)
    if dt < 0 or dt > 0.8:
        return 0.0
    v = math.exp(-dt * 9)
    if dt > 0.2:
        v += 0.7 * math.exp(-(dt - 0.2) * 11)
    return min(1.0, v)


def flicker(t):
    """0..1 ánh lửa chập chờn."""
    v = 0.55 + 0.25 * math.sin(t * 11.3) * math.sin(t * 3.7 + 1.1) + 0.2 * math.sin(t * 23.1 + 2.0)
    return max(0.0, min(1.0, v))


def shake(t):
    """(dx, dy) theo tỉ lệ khung: rung tay máy nhẹ liên tục + cú rung mạnh khoảng 4 giây một lần."""
    dx = (math.sin(t * 7.1) + 0.6 * math.sin(t * 13.3 + 1)) * 0.0012
    dy = (math.cos(t * 6.3) + 0.6 * math.sin(t * 11.7 + 2)) * 0.0012
    k = math.floor(t / 4.2)
    dt = t - (k * 4.2 + _hash(k + 3) * 2.0)
    if 0 <= dt < 1.2:
        a = 0.010 * math.exp(-dt * 4.5)
        dx += a * math.sin(dt * 47)
        dy += a * 0.8 * math.cos(dt * 39)
    return dx, dy


def kick(lt, dur, xf, has_prev=True, has_next=True):
    """Hệ số phóng to thêm khi chuyển cảnh kiểu "lao vào ảnh": trong lúc cảnh mới hiện lên, cảnh cũ phóng nhanh tới,
    cảnh mới thu từ to về bình thường -> cảm giác máy quay lao xuyên qua ảnh."""
    k = 1.0
    if has_next and lt > dur - xf:
        q = min(1.0, (lt - (dur - xf)) / xf)
        k *= 1 + 0.22 * q * q
    if has_prev and lt < 0:
        q = min(1.0, -lt / xf)
        k *= 1 + 0.16 * q * q
    return k


# ------------------------------------------------------------------ tự chọn hiệu ứng hạt
_KEYS = [
    ("rain", r"\b(rain|rainy|storm|stormy|downpour|monsoon|thunder|lightning)\b|mưa|bão|giông"),
    ("snow", r"\b(snow|snowy|blizzard|winter|frozen|frost|icy|antarctic|arctic|ural)\b|tuyết|băng giá|nam cực|bắc cực"),
    ("embers", r"\b(fire|fires|flame|flames|burning|burnt|candle|candles|torch|torches|campfire|ember|embers|explosion|explode|blaze|furnace|lamp light|lamplight)\b|lửa|cháy|đuốc|nến|nổ"),
    ("mist", r"\b(mist|misty|fog|foggy|haze|hazy|smoke|smoky|steam|jungle|rainforest|swamp|dawn|moor)\b|sương|khói|rừng rậm|rừng"),
]


_MODS = [   # hiệu ứng ánh sáng / máy quay đi kèm
    ("lightning", r"\b(storm|stormy|thunder|thunderstorm|lightning)\b|bão|sấm|sét|giông"),
    ("flicker", r"\b(fire|fires|flame|flames|burning|candle|candles|torch|torches|campfire|lamp|lamps|lantern|furnace)\b|lửa|cháy|đuốc|nến|đèn"),
    ("rays", r"\b(sunlight|sunbeam|sunbeams|sun rays|morning light|jungle|forest|rainforest|cathedral|church|temple|window light|dawn)\b|nắng|bình minh|rừng"),
    ("shake", r"\b(explosion|explode|exploded|bomb|bombs|bombing|blast|cannon|cannons|artillery|bombard|bombardment|shelling|earthquake|crash|collapse)\b|nổ|pháo|bom|động đất|sập"),
]


def pick_fx(item, default="dust", auto=True):
    """item: cảnh video ngắn hoặc đoạn video dài. "fx" ghi sẵn thì dùng luôn.
    auto=False: chỉ dùng hiệu ứng ghi tay trong kịch bản (không tự đoán)."""
    fx = item.get("fx")
    if isinstance(fx, str) and fx.strip():
        return "" if fx.strip().lower() in ("none", "off", "khong", "không") else fx.strip().lower()
    if not auto:
        return ""
    im = item.get("image") if isinstance(item.get("image"), dict) else {}
    text = " ".join(str(x) for x in (item.get("ai"), im.get("url"), im.get("credit"),
                                     item.get("text"), item.get("voice"), item.get("sub"))
                    if x).lower()
    out = [default] if default else []
    for name, rx in _KEYS:
        if re.search(rx, text):
            out = ["mist", "dust"] if name == "mist" else [name]
            break
    for name, rx in _MODS:
        if re.search(rx, text) and name not in out:
            out.append(name)
    return "+".join(out)


def _norm_fx(fx):
    return [x for x in str(fx or "").replace(",", "+").split("+") if x.strip() in FX_NAMES]


# ------------------------------------------------------------------ hiệu ứng hạt (Python, cho video dài)
PRESETS = {
    #           số hạt  bán kính (tỉ lệ chiều cao)  màu (RGB)          độ đậm
    "dust":   dict(n=70, r=(0.0011, 0.0032), color=(255, 214, 160), a=(0.25, 0.65)),
    "embers": dict(n=48, r=(0.0014, 0.0040), color=(255, 150, 60), a=(0.45, 0.95)),
    "snow":   dict(n=120, r=(0.0018, 0.0055), color=(245, 248, 255), a=(0.45, 0.90)),
    "rain":   dict(n=170, r=(0.0006, 0.0011), color=(205, 218, 232), a=(0.16, 0.34)),
}


class FX:
    """Vẽ lớp hạt theo thời gian t lên ảnh RGB uint8 (cộng sáng). Mọi thứ cố định theo seed -> dựng lại vẫn y hệt."""

    def __init__(self, w, h, strength=1.0, seed=7):
        self.w, self.h, self.k = w, h, strength
        self.lw, self.lh = w // 2, h // 2           # vẽ ở nửa độ phân giải rồi phóng lên (mềm và nhanh)
        self.rng = np.random.default_rng(seed)
        self.p = {name: self._params(name) for name in PRESETS}
        self._mist = None

    def _params(self, name):
        c = PRESETS[name]
        n = c["n"]
        g = np.random.default_rng(sum(ord(ch) * 131 ** i for i, ch in enumerate(name)) % 2**31)
        q = dict(x=g.random(n), y=g.random(n), ph=g.random(n) * 6.283, f=0.3 + g.random(n) * 0.9,
                 r=c["r"][0] + g.random(n) * (c["r"][1] - c["r"][0]), a=c["a"][0] + g.random(n) * (c["a"][1] - c["a"][0]),
                 z=0.4 + g.random(n) * 0.6)
        if name == "dust":
            big = g.random(n) < 0.12                  # vài hạt to, mờ (như bụi ngoài tiêu cự)
            q["r"] = np.where(big, q["r"] * 3.2, q["r"])
            q["a"] = np.where(big, q["a"] * 0.35, q["a"])
            q["vx"] = (g.random(n) - 0.35) * 0.010
            q["vy"] = -(0.004 + g.random(n) * 0.010)
        elif name == "embers":
            q["vx"] = (g.random(n) - 0.5) * 0.02
            q["vy"] = -(0.04 + g.random(n) * 0.07)
        elif name == "snow":
            q["vx"] = (g.random(n) - 0.5) * 0.01
            q["vy"] = (0.03 + 0.06 * q["z"])
            q["r"] = q["r"] * (0.5 + q["z"])
        elif name == "rain":
            q["vy"] = 1.1 + q["z"] * 0.8
            q["vx"] = q["vy"] * 0.18
            q["len"] = 0.025 + q["z"] * 0.035
        return q

    def _pos(self, q, t, wob):
        # đơn vị theo chiều cao khung, quấn vòng qua mép
        H, Wr = 1.0, self.w / self.h
        m = 0.06
        x = (q["x"] * (Wr + 2 * m) + q["vx"] * t + wob * np.sin(t * q["f"] + q["ph"])) % (Wr + 2 * m) - m
        y = (q["y"] * (H + 2 * m) + q["vy"] * t) % (H + 2 * m) - m
        return x, y

    def _layer(self, names, t):
        import cv2
        L = np.zeros((self.lh, self.lw, 3), np.uint8)
        s = self.lh            # 1 đơn vị = chiều cao lớp
        for name in names:
            if name == "mist":
                continue
            q, c = self.p[name], PRESETS[name]["color"]
            if name == "rain":
                x, y = self._pos(q, t, 0.0)
                for i in range(len(x)):
                    a = q["a"][i] * self.k
                    col = (int(c[0] * a), int(c[1] * a), int(c[2] * a))   # mảng là RGB, vẽ thẳng
                    x0, y0 = x[i] * s, y[i] * s
                    ln = q["len"][i] * s
                    cv2.line(L, (int(x0), int(y0)), (int(x0 - ln * 0.18), int(y0 - ln)), col,
                             max(1, int(round(q["r"][i] * s * 2))), cv2.LINE_AA)
                continue
            wob = {"dust": 0.012, "embers": 0.02, "snow": 0.03}[name]
            x, y = self._pos(q, t, wob)
            if name == "embers":
                tw = 0.55 + 0.45 * np.sin(t * (6 + q["f"] * 9) + q["ph"]) * np.sin(t * 2.3 + q["ph"] * 2)
                life = np.clip(1.4 - y * 1.1, 0.0, 1.0)       # tàn lửa mờ dần khi bay cao
                al = q["a"] * np.clip(tw, 0.1, 1) * life
            elif name == "dust":
                al = q["a"] * (0.55 + 0.45 * np.sin(t * q["f"] * 1.7 + q["ph"]))
            else:
                al = q["a"]
            for i in range(len(x)):
                a = float(al[i]) * self.k
                if a <= 0.01:
                    continue
                col = (int(c[0] * a), int(c[1] * a), int(c[2] * a))
                cv2.circle(L, (int(x[i] * s * 16), int(y[i] * s * 16)), max(1, int(q["r"][i] * s * 16)), col, -1,
                           cv2.LINE_AA, shift=4)
        if L.any():
            glow = cv2.GaussianBlur(L, (0, 0), sigmaX=max(1.0, self.lh * 0.004))
            L = cv2.addWeighted(L, 0.8, glow, 1.6, 0)
        return L

    def _mist_tex(self):
        if self._mist is None:
            import cv2
            g = np.random.default_rng(11)
            acc = np.zeros((self.lh, self.lw * 2), np.float32)
            for octv, amp in ((3, 1.0), (6, 0.5), (12, 0.25)):
                small = g.random((octv, octv * 2)).astype(np.float32)
                acc += amp * cv2.resize(small, (self.lw * 2, self.lh), interpolation=cv2.INTER_CUBIC)
            acc = (acc - acc.min()) / max(1e-6, acc.max() - acc.min())
            acc = np.clip((acc - 0.35) / 0.65, 0, 1) ** 1.5
            # sương dày hơn ở nửa dưới khung
            acc *= np.linspace(0.45, 1.0, self.lh, dtype=np.float32)[:, None]
            self._mist = np.concatenate([acc, acc], axis=1)        # quấn vòng liền mạch
        return self._mist

    def _rays_tex(self):
        """Hai bộ tia nắng chéo từ góc trên (vẽ 1 lần), đổi qua lại chậm để tia sáng "thở"."""
        if getattr(self, "_rays", None) is None:
            import cv2
            out = []
            for seed in (3, 8):
                g = np.random.default_rng(seed)
                L = np.zeros((self.lh, self.lw), np.float32)
                ox, oy = -0.15 * self.lw, -0.25 * self.lh
                for _ in range(9):
                    ang = math.radians(25 + g.random() * 45)
                    wdt = math.radians(1.5 + g.random() * 4)
                    ln = 2.2 * max(self.lw, self.lh)
                    pts = np.array([[ox, oy],
                                    [ox + ln * math.cos(ang - wdt), oy + ln * math.sin(ang - wdt)],
                                    [ox + ln * math.cos(ang + wdt), oy + ln * math.sin(ang + wdt)]], np.int32)
                    tmp = np.zeros_like(L)
                    cv2.fillConvexPoly(tmp, pts, 0.35 + g.random() * 0.65)
                    L = np.maximum(L, tmp)
                L = cv2.GaussianBlur(L, (0, 0), sigmaX=self.lh * 0.025)
                yy, xx = np.mgrid[0:self.lh, 0:self.lw].astype(np.float32)
                L *= np.exp(-np.hypot(xx - ox, yy - oy) / (1.1 * max(self.lw, self.lh)))   # mờ dần khi xa nguồn
                out.append(L / max(1e-6, L.max()))
            self._rays = out
        return self._rays

    def _add_light(self, img, a2d, color):
        """Cộng sáng một lớp xám (nửa độ phân giải, 0..1) nhuộm màu."""
        import cv2
        a = cv2.resize(a2d, (self.w, self.h), interpolation=cv2.INTER_LINEAR)
        lay = (a[..., None] * np.array(color, np.float32)).clip(0, 255).astype(np.uint8)
        return cv2.add(img, lay)

    def leak(self, img, q):
        """Vệt sáng ấm quét ngang lúc chuyển cảnh (q: 0..1 tiến độ chuyển cảnh)."""
        import cv2
        a = math.sin(math.pi * q)
        if a <= 0.01:
            return img
        yy, xx = np.mgrid[0:self.lh // 2, 0:self.lw // 2].astype(np.float32)
        cx, cy = (-0.2 + 1.4 * q) * self.lw / 2, 0.35 * self.lh / 2
        m = np.exp(-(((xx - cx) / (0.55 * self.lw / 2)) ** 2 + ((yy - cy) / (0.9 * self.lh / 2)) ** 2))
        lay = cv2.resize(m * (0.28 * a * self.k), (self.w, self.h), interpolation=cv2.INTER_LINEAR)
        out = img.astype(np.float32)
        out += lay[..., None] * np.array([255, 150, 70], np.float32)
        out = out * (1 + 0.05 * a)
        return out.clip(0, 255).astype(np.uint8)

    def apply(self, img, fx, t, opacity=1.0, light=True):
        """img: RGB uint8 HxW (đúng w, h đã khai báo). Trả về ảnh mới."""
        import cv2
        names = _norm_fx(fx)
        if not names or opacity <= 0.01 or self.k <= 0:
            return img
        if light and "flicker" in names:     # ánh lửa hắt: cả cảnh ấm lên / tối đi theo nhịp lửa
            f = flicker(t)
            g = 0.92 + 0.14 * f * self.k
            img = (img.astype(np.float32) * np.array([g * 1.04, g, g * 0.90], np.float32)).clip(0, 255).astype(np.uint8)
        if light and "rays" in names:
            r1, r2 = self._rays_tex()
            w = 0.5 + 0.5 * math.sin(t * 0.35)
            a = (r1 * w + r2 * (1 - w)) * (0.32 + 0.08 * math.sin(t * 0.9)) * self.k * opacity
            img = self._add_light(img, a, (255, 236, 196))
        if light and "lightning" in names:
            v = lightning(t) * self.k * opacity
            if v > 0.01:
                img = (img.astype(np.float32) * (1 + 0.5 * v) + 30 * v * np.array([0.85, 0.9, 1.0], np.float32)) \
                    .clip(0, 255).astype(np.uint8)
        if "mist" in names:
            tex = self._mist_tex()
            ox = int((t * self.lw * 0.025) % (self.lw * 2))
            m = tex[:, ox:ox + self.lw]
            ox2 = int((t * self.lw * 0.045 + self.lw * 0.7) % (self.lw * 2))
            m = 0.6 * m + 0.4 * tex[:, ox2:ox2 + self.lw]
            a = cv2.resize(m, (self.w, self.h), interpolation=cv2.INTER_LINEAR) * (0.15 * self.k * opacity)
            a3 = a[..., None]
            img = (img.astype(np.float32) * (1 - a3) + np.array([214, 206, 192], np.float32) * a3).astype(np.uint8)
        rest = [n for n in names if n in PRESETS]
        if rest:
            L = self._layer(rest, t)
            L = cv2.resize(L, (self.w, self.h), interpolation=cv2.INTER_LINEAR)
            if opacity < 0.999:
                L = cv2.multiply(L, np.full_like(L, int(opacity * 255)), scale=1 / 255)
            img = cv2.add(img, L)
        return img


if __name__ == "__main__":
    for a in sys.argv[1:]:
        print(a, "->", pick_fx({"image": {"url": a}}))
        d = depth_map(a)
        print("   độ sâu:", d)
