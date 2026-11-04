"""Bản đồ động cho video kênh tiếng Anh (History Mysteries Daily).

Mỗi cảnh bản đồ là một đoạn video: bản đồ vùng cực kiểu cổ, máy quay phóng/lia từ khung đầu tới khung cuối,
rồi điểm đánh dấu hiện lên với vòng sáng lan ra, nhãn tên mờ dần vào; mũi tên và đường đi được vẽ dần.

Dữ liệu cảnh nằm trong ke-hoach/<chủ đề>/ban_do.json, ví dụ:
  "M09": {
    "from": {"lat": 82, "lon": 20, "km": 2600},        khung đầu (tâm và bề ngang khung, tính bằng km)
    "to":   {"lat": 82.6, "lon": 28, "km": 1300},      khung cuối
    "markers": [{"lat": 82.93, "lon": 29.87, "label": "Landing site", "style": "x"}],
    "arrows":  [{"pts": [[82.93, 29.87], [90, 0]], "label": "~500 miles", "dash": true}],
    "lat_line": 82                                       tô sáng một vòng vĩ tuyến (tùy chọn)
  }
Cách dùng riêng:
  python ban_do_en.py demo ke-hoach/andree/ban_do.json M06,M09 out.mp4   dựng thử vài cảnh (mỗi cảnh 6 giây)
  python ban_do_en.py anh  ke-hoach/andree/ban_do.json M09 out.png        xuất một khung cuối để soi
Dữ liệu bờ biển: Natural Earth 1:10m (phạm vi công cộng), đã cắt sẵn ở assets/ban_do/bac_cuc_10m.json.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
W, H, FPS = 1920, 1080, 30
SS = 2                                   # vẽ gấp đôi rồi thu nhỏ cho mượt nét
R_EARTH = 6371.0
LON0 = 25.0                              # kinh tuyến giữa (hướng xuống dưới màn hình)
FONT = ROOT / "assets" / "fonts" / "Lora-Variable.ttf"
FONT_I = ROOT / "assets" / "fonts" / "Lora-Italic-Variable.ttf"

SEA_TOP, SEA_BOT = (17, 27, 35), (9, 15, 21)
LAND = (122, 104, 78)
LAND_EDGE = (190, 170, 128)
GRID = (60, 78, 88)
MARK = (232, 76, 61)
GOLD = (236, 200, 120)
TEXT = (240, 232, 214)

REGIONS = [  # nhãn vùng cố định (chữ nghiêng, mờ), chỉ hiện khi nằm trong khung
    ("NORTH POLE", 90, 0, 1.0), ("SVALBARD", 77.0, 7.0, 0.9), ("FRANZ JOSEF LAND", 82.4, 57.0, 0.8),
    ("NORWAY", 63.5, 10.5, 1.0), ("SWEDEN", 61.0, 15.8, 1.0), ("RUSSIA", 67.0, 55.0, 1.0),
    ("GREENLAND", 76.0, -40.0, 1.0), ("ARCTIC OCEAN", 85.0, 60.0, 0.8), ("BARENTS SEA", 74.0, 38.0, 0.8),
    ("CANADA", 72.0, -95.0, 1.0), ("FRANCE", 46.8, 2.5, 1.0),
]


def proj(lat, lon):
    """Phép chiếu nổi cực bắc, trả về km (x sang phải, y lên trên về phía cực)."""
    lat = np.asarray(lat, dtype=np.float64)
    lon = np.asarray(lon, dtype=np.float64)
    r = 2 * R_EARTH * np.tan(np.radians(90 - lat) / 2)
    a = np.radians(lon - LON0)
    return r * np.sin(a), -r * np.cos(a)


_LAND = None


_LEVELS = {}


def _thin(pts, tol):
    """Bỏ điểm cách điểm giữ trước đó dưới tol km (làm một lần lúc nạp, không làm mỗi khung)."""
    keep = [0]
    last = pts[0]
    d2 = tol * tol
    for i in range(1, len(pts)):
        dx, dy = pts[i, 0] - last[0], pts[i, 1] - last[1]
        if dx * dx + dy * dy >= d2:
            keep.append(i)
            last = pts[i]
    return pts[keep]


def land(km_per_px=0.0):
    """Đa giác đất liền (km), chọn bản giản lược hợp với mức phóng hiện tại."""
    global _LAND
    if _LAND is None:
        d = json.loads((ROOT / "assets" / "ban_do" / "bac_cuc_10m.json").read_text(encoding="utf-8"))
        rings = []
        for r in d["rings"]:
            a = np.asarray(r, dtype=np.float64)
            x, y = proj(a[:, 1], a[:, 0])
            rings.append(np.stack([x, y], 1))
        _LAND = rings
    tol = 0.0
    for t in (8.0, 3.0, 1.0):
        if km_per_px >= t:
            tol = t
            break
    if tol not in _LEVELS:
        out = []
        for pts in _LAND:
            q = _thin(pts, tol) if tol else pts
            if len(q) < 3:
                continue
            ext = q.max(0) - q.min(0)
            if tol and max(ext) < tol * 1.5:          # đảo nhỏ hơn khoảng một điểm ảnh ở mức phóng này
                continue
            out.append((q, (q[:, 0].min(), q[:, 0].max(), q[:, 1].min(), q[:, 1].max())))
        _LEVELS[tol] = out
    return _LEVELS[tol]


def font(size, italic=False):
    return ImageFont.truetype(str(FONT_I if italic else FONT), int(size * SS))


class Cam:
    def __init__(self, lat, lon, km):
        self.cx, self.cy = proj(lat, lon)
        self.cx, self.cy = float(self.cx), float(self.cy)
        self.km = km

    @staticmethod
    def lerp(a, b, t):
        c = Cam.__new__(Cam)
        c.cx = a.cx + (b.cx - a.cx) * t
        c.cy = a.cy + (b.cy - a.cy) * t
        c.km = math.exp(math.log(a.km) + (math.log(b.km) - math.log(a.km)) * t)   # phóng theo tỉ lệ, đều mắt
        return c

    def px(self, x, y):
        s = W * SS / self.km
        # tâm khung đặt ở 44% chiều cao (không phải 50%) để điểm đánh dấu nằm trên vùng phụ đề
        return (W * SS / 2 + (np.asarray(x) - self.cx) * s, H * SS * 0.44 - (np.asarray(y) - self.cy) * s)

    def ll(self, lat, lon):
        x, y = proj(lat, lon)
        X, Y = self.px(x, y)
        return float(X), float(Y)


_SEA = None


def sea():
    global _SEA
    if _SEA is None:
        g = np.linspace(0, 1, H * SS)[:, None, None]
        top, bot = np.array(SEA_TOP), np.array(SEA_BOT)
        arr = (top + (bot - top) * g) * np.ones((1, W * SS, 1))
        rng = np.random.default_rng(3)
        arr += rng.normal(0, 2.2, arr.shape)         # hạt nhẹ cho giống giấy in cũ
        _SEA = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return _SEA


def clip_poly(q, x0, y0, x1, y1):
    """Cắt đa giác theo khung chữ nhật (Sutherland-Hodgman), tránh tô phần nằm ngoài khung."""
    def clip(p, inside, inter):
        if len(p) == 0:
            return p
        prev = np.roll(p, 1, axis=0)
        ip, iq = inside(p), inside(prev)
        out = []
        for a, b, ia, ib in zip(prev, p, iq, ip):
            if ib:
                if not ia:
                    out.append(inter(a, b))
                out.append(b)
            elif ia:
                out.append(inter(a, b))
        return np.array(out) if out else np.empty((0, 2))

    def ix(a, b, x):
        t = (x - a[0]) / (b[0] - a[0])
        return np.array([x, a[1] + t * (b[1] - a[1])])

    def iy(a, b, y):
        t = (y - a[1]) / (b[1] - a[1])
        return np.array([a[0] + t * (b[0] - a[0]), y])

    q = clip(q, lambda p: p[:, 0] >= x0, lambda a, b: ix(a, b, x0))
    q = clip(q, lambda p: p[:, 0] <= x1, lambda a, b: ix(a, b, x1))
    q = clip(q, lambda p: p[:, 1] >= y0, lambda a, b: iy(a, b, y0))
    q = clip(q, lambda p: p[:, 1] <= y1, lambda a, b: iy(a, b, y1))
    return q


def draw_base(cam):
    im = sea().copy()
    d = ImageDraw.Draw(im)
    half_w = cam.km / 2
    half_h = cam.km * H / W / 2
    x0, x1, y0, y1 = cam.cx - half_w, cam.cx + half_w, cam.cy - half_h, cam.cy + half_h
    lw = max(1, int(1.2 * SS))
    # lưới kinh vĩ tuyến
    for lat in range(50, 90, 5):
        lon = np.linspace(-180, 180, 721)
        X, Y = cam.px(*proj(np.full_like(lon, lat), lon))
        d.line(list(zip(X, Y)), fill=GRID, width=lw)
    for lon in range(-180, 180, 15):
        lat = np.linspace(50, 89.9, 200)
        X, Y = cam.px(*proj(lat, np.full_like(lat, lon)))
        d.line(list(zip(X, Y)), fill=GRID, width=lw)
    # đất liền
    for pts, (a, b, c, e) in land(cam.km / (W * SS) * 1.5):
        if b < x0 or a > x1 or e < y0 or c > y1:
            continue
        X, Y = cam.px(pts[:, 0], pts[:, 1])
        q = np.stack([X, Y], 1)
        keep = np.ones(len(q), bool)
        keep[1:] = np.abs(np.diff(q, axis=0)).sum(1) > 1.5      # bỏ điểm sát nhau dưới 1,5 điểm ảnh
        q = q[keep]
        if len(q) < 3:
            continue
        M = 20 * SS
        if q[:, 0].min() < -M or q[:, 1].min() < -M or q[:, 0].max() > W * SS + M or q[:, 1].max() > H * SS + M:
            q = clip_poly(q, -M, -M, W * SS + M, H * SS + M)
            if len(q) < 3:
                continue
        poly = [tuple(p) for p in q]
        d.polygon(poly, fill=LAND)
        d.line(poly + [poly[0]], fill=LAND_EDGE, width=lw)
    return im


def draw_regions(d, cam, busy):
    """Nhãn vùng (chữ nghiêng, mờ): bỏ qua nhãn sát mép khung hoặc đè lên nhãn/điểm đánh dấu."""
    f = font(26, italic=True)
    m = 50 * SS
    for name, lat, lon, alpha in REGIONS:
        X, Y = cam.ll(lat, lon)
        bb = d.textbbox((X, Y), name, font=f, anchor="mm")
        if bb[0] < m or bb[1] < m or bb[2] > W * SS - m or bb[3] > H * SS - 190 * SS:   # chừa vùng phụ đề
            continue
        if any(not (bb[2] < b[0] or bb[0] > b[2] or bb[3] < b[1] or bb[1] > b[3]) for b in busy):
            continue
        col = tuple(int(c * 0.62 * alpha + 20) for c in TEXT) + (255,)
        d.text((X, Y), name, font=f, fill=col, anchor="mm")


def ease(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


BUSY = []


def label_box(d, x, y, text, alpha, size=34, dx=34, dy=-30):
    if alpha <= 0:
        return
    f = font(size)
    tx, ty = x + dx * SS, y + dy * SS
    bbox = d.textbbox((tx, ty), text, font=f, anchor="lm")
    pad = 12 * SS
    if bbox[2] + pad > W * SS - 60 * SS:           # chữ không tràn khỏi khung: lật sang trái điểm đánh dấu
        tx = x - dx * SS
        bbox = d.textbbox((tx, ty), text, font=f, anchor="rm")
        anchor = "rm"
    else:
        anchor = "lm"
    a = int(210 * alpha)
    BUSY.append((bbox[0] - pad * 2, bbox[1] - pad * 2, bbox[2] + pad * 2, bbox[3] + pad * 2))
    d.rounded_rectangle((bbox[0] - pad, bbox[1] - pad * 0.7, bbox[2] + pad, bbox[3] + pad * 0.7),
                        radius=8 * SS, fill=(12, 16, 20, a), outline=GOLD + (int(180 * alpha),), width=SS)
    d.text((tx, ty), text, font=f, fill=TEXT + (int(255 * alpha),), anchor=anchor)


def draw_marker(d, x, y, t, style="dot"):
    """t: thời gian kể từ lúc điểm xuất hiện (giây). Vòng sáng lan ra lặp lại mỗi 1,6 giây."""
    if t < 0:
        return
    pop = ease(t / 0.35)
    for k in range(2):
        ph = ((t - k * 0.8) % 1.6) / 1.6 if t - k * 0.8 >= 0 else None
        if ph is None:
            continue
        r = (14 + 70 * ph) * SS
        a = int(200 * (1 - ph))
        d.ellipse((x - r, y - r, x + r, y + r), outline=MARK + (a,), width=int(3 * SS))
    r = 11 * SS * pop
    if style == "x":
        L = 13 * SS * pop
        d.line((x - L, y - L, x + L, y + L), fill=MARK + (255,), width=int(5 * SS))
        d.line((x - L, y + L, x + L, y - L), fill=MARK + (255,), width=int(5 * SS))
    else:
        d.ellipse((x - r - 3 * SS, y - r - 3 * SS, x + r + 3 * SS, y + r + 3 * SS), fill=(255, 245, 230, 255))
        d.ellipse((x - r, y - r, x + r, y + r), fill=MARK + (255,))


def draw_arrow(d, cam, pts, prog, dash=False, label=None, alpha=1.0, ldx=18, ldy=28):
    """Vẽ dần đường đi qua các điểm (lat, lon) theo tiến độ prog 0..1, có đầu mũi tên khi đã vẽ xong."""
    if prog <= 0:
        return
    lat = []
    lon = []
    for (a1, o1), (a2, o2) in zip(pts, pts[1:]):       # chia nhỏ để đường cong theo phép chiếu
        for s in np.linspace(0, 1, 40, endpoint=False):
            lat.append(a1 + (a2 - a1) * s)
            lon.append(o1 + (o2 - o1) * s)
    lat.append(pts[-1][0])
    lon.append(pts[-1][1])
    X, Y = cam.px(*proj(np.array(lat), np.array(lon)))
    q = np.stack([X, Y], 1)
    seg = np.sqrt((np.diff(q, axis=0) ** 2).sum(1))
    cum = np.concatenate([[0], np.cumsum(seg)])
    L = cum[-1] * min(1.0, prog)
    n = int(np.searchsorted(cum, L))
    path = q[:max(2, n)]
    col = GOLD + (int(255 * alpha),)
    w = int(5 * SS)
    if dash:
        step, on = 26 * SS, 16 * SS
        pos = 0.0
        cumd = np.concatenate([[0], np.cumsum(np.sqrt((np.diff(path, axis=0) ** 2).sum(1)))])
        while pos < cumd[-1]:
            a, b = pos, min(pos + on, cumd[-1])
            pa = np.array([np.interp(a, cumd, path[:, 0]), np.interp(a, cumd, path[:, 1])])
            pb = np.array([np.interp(b, cumd, path[:, 0]), np.interp(b, cumd, path[:, 1])])
            d.line((tuple(pa), tuple(pb)), fill=col, width=w)
            pos += step
    else:
        d.line([tuple(p) for p in path], fill=col, width=w, joint="curve")
    if prog >= 1 and len(path) >= 2:
        p1, p0 = path[-1], path[-6] if len(path) > 6 else path[0]
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        s = 22 * SS
        tip = [tuple(p1), (p1[0] - s * math.cos(ang - 0.45), p1[1] - s * math.sin(ang - 0.45)),
               (p1[0] - s * math.cos(ang + 0.45), p1[1] - s * math.sin(ang + 0.45))]
        d.polygon(tip, fill=col)
        if label:
            mid = path[len(path) // 2]
            label_box(d, mid[0], mid[1], label, alpha * ease((prog - 1) * 3 + 1), size=28, dx=ldx, dy=ldy)


_CACHE = {}


def frame(spec, t, dur):
    """Một khung hình ở giây t của cảnh dài dur giây."""
    move = min(3.2, dur * 0.45)
    c0 = Cam(**spec["from"]) if "from" in spec else Cam(**spec["to"])
    c1 = Cam(**spec["to"])
    cam = Cam.lerp(c0, c1, ease(t / move))
    if t >= move:                              # máy quay đã dừng: nền giống nhau, vẽ một lần rồi dùng lại
        key = (id(spec), "base")
        if _CACHE.get("key") != key:
            _CACHE.update(key=key, im=finish_base(draw_base(cam)))
        base = _CACHE["im"]
    else:
        base = finish_base(draw_base(cam))
    ov = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    BUSY.clear()
    t_show = move * 0.85                      # điểm và đường hiện khi máy quay sắp dừng
    if "lat_line" in spec:
        lat = spec["lat_line"]
        lon = np.linspace(-180, 180, 1441)
        X, Y = cam.px(*proj(np.full_like(lon, lat), lon))
        a = ease((t - t_show) / 0.8)
        d.line(list(zip(X, Y)), fill=GOLD + (int(230 * a),), width=int(4 * SS))
        mx, my = cam.ll(lat, spec.get("lat_label_lon", 0))
        label_box(d, mx, my, spec.get("lat_label", f"{lat}° North"), a, size=28, dx=0, dy=-36)
    for i, ar in enumerate(spec.get("arrows", [])):
        st = t_show + ar.get("delay", 0.3 * i)
        draw_arrow(d, cam, ar["pts"], (t - st) / ar.get("draw", 1.6), ar.get("dash", False), ar.get("label"),
                   ldx=ar.get("ldx", 18), ldy=ar.get("ldy", 28))
    for i, m in enumerate(spec.get("markers", [])):
        st = t_show + m.get("delay", 0.45 * i)
        x, y = cam.ll(m["lat"], m["lon"])
        draw_marker(d, x, y, t - st, m.get("style", "dot"))
        label_box(d, x, y, m["label"], ease((t - st - 0.25) / 0.5), size=m.get("size", 34))
        BUSY.append((x - 30 * SS, y - 30 * SS, x + 30 * SS, y + 30 * SS))
    for ar in spec.get("arrows", []):               # chỗ đường đi đã chiếm (thô): các điểm đầu cuối
        for la, lo in ar["pts"]:
            x, y = cam.ll(la, lo)
            BUSY.append((x - 25 * SS, y - 25 * SS, x + 25 * SS, y + 25 * SS))
    draw_regions(d, cam, BUSY)
    if spec.get("title"):
        a = ease(t / 0.6)
        d.text((70 * SS, 60 * SS), spec["title"], font=font(30), fill=GOLD + (int(230 * a),), anchor="lm")
    ov = ov.reduce(SS)
    out = base.copy()
    out.alpha_composite(ov)
    return out.convert("RGB")


def finish_base(im):
    """Thu nhỏ nền vẽ gấp đôi về 1920x1080, làm tối viền; trả RGBA để phủ lớp điểm đánh dấu."""
    im = im.resize((W, H), Image.LANCZOS)
    return vignette(im).convert("RGBA")


_VIG = None


def vignette(im):
    global _VIG
    if _VIG is None:
        y, x = np.mgrid[0:H, 0:W]
        r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
        v = np.clip(1.0 - 0.38 * np.clip(r - 0.55, 0, None) ** 1.4, 0.45, 1.0)
        _VIG = Image.fromarray((v * 255).astype(np.uint8)).convert("RGB")
    from PIL import ImageChops
    return ImageChops.multiply(im.convert("RGB"), _VIG)


def render_map_shot(spec, out, dur, caption=None, fps=None):
    """Dựng một cảnh bản đồ thành mp4 (cùng định dạng với render_shot của en_video.py)."""
    fps = fps or FPS
    n = max(2, int(round(dur * fps)))
    fade = min(0.4, dur / 4)
    vf = f"fade=t=in:st=0:d={fade:.2f},fade=t=out:st={max(0, dur - fade):.2f}:d={fade:.2f},format=yuv420p"
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
           "-i", "-", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", str(fps), str(out)]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for i in range(n):
            fr = frame(spec, i / fps, dur)
            if caption:
                fr = add_caption(fr, caption)
            pr.stdin.write(fr.tobytes())
        pr.stdin.close()
        if pr.wait() != 0:
            raise RuntimeError(f"ffmpeg lỗi khi dựng {out}")
    finally:
        if pr.poll() is None:
            pr.kill()
    return out


def add_caption(im, text):
    """Phụ đề cho bản demo (video thật dùng phụ đề ASS của en_video.py)."""
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(str(FONT), 38)
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) > W - 260:
            lines.append(cur)
            cur = w_
        else:
            cur = t
    lines.append(cur)
    y = H - 70 - 50 * (len(lines) - 1)
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=(255, 255, 255), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0))
        y += 50
    return im


def load_maps(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    cmd, path = sys.argv[1], sys.argv[2]
    maps = load_maps(path)
    if cmd == "anh":
        key, out = sys.argv[3], sys.argv[4]
        spec = maps[key]
        frame(spec, 6.0, 6.0).save(out, quality=92)
    elif cmd == "demo":
        keys, out = sys.argv[3].split(","), Path(sys.argv[4])
        dur = float(sys.argv[5]) if len(sys.argv) > 5 else 6.0
        work = out.parent / "_demo_ban_do"
        work.mkdir(parents=True, exist_ok=True)
        parts = []
        for k in keys:
            p = work / f"{k}.mp4"
            render_map_shot(maps[k], p, maps[k].get("demo_dur", dur), maps[k].get("demo_caption"))
            parts.append(p)
            print("✔", k, flush=True)
        lst = work / "list.txt"
        lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts), encoding="utf-8")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
        print("✅", out)
