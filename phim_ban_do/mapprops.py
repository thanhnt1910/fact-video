"""Hình minh họa nổi trên bản đồ (quả cam, lá cờ, hội nghị, kho trống, cầu gãy...).
Dùng: PROPS.append((t0, t1, loại, (lon, lat), tham_số)) trong tệp nội dung; vẽ bằng draw(d, ...).
Mọi hàm vẽ trên canvas 2x; s là đơn vị kích thước (ik), u là tiến độ 0..1, t là thời gian tuyệt đối."""
import math, random
from build2 import font
INK = (30, 22, 16, 255)
SKIN = (232, 196, 150, 255)
def _lw(s, k=0.1): return max(2, int(s * k))
def _clamp(v): return max(0.0, min(1.0, v))

def _person(d, x, y, s, robe, hat=None, beard=False, arm=0.0):
    d.polygon([(x - s * 0.6, y + s * 0.9), (x + s * 0.6, y + s * 0.9), (x + s * 0.42, y - s * 0.3), (x - s * 0.42, y - s * 0.3)], fill=robe + (255,), outline=INK)
    if arm > 0:
        for sx in (-1, 1):
            d.line([(x + sx * s * 0.4, y - s * 0.1), (x + sx * s * 0.75, y - s * (0.3 + 1.1 * arm))], fill=SKIN, width=_lw(s, 0.18))
            d.ellipse((x + sx * s * 0.75 - s * 0.16, y - s * (0.3 + 1.1 * arm) - s * 0.16, x + sx * s * 0.75 + s * 0.16, y - s * (0.3 + 1.1 * arm) + s * 0.16), fill=SKIN, outline=INK)
    d.ellipse((x - s * 0.34, y - s * 1.0, x + s * 0.34, y - s * 0.28), fill=SKIN, outline=INK)
    if beard: d.polygon([(x - s * 0.3, y - s * 0.55), (x + s * 0.3, y - s * 0.55), (x, y + s * 0.25)], fill=(244, 242, 236, 255), outline=INK)
    if hat: d.pieslice((x - s * 0.42, y - s * 1.25, x + s * 0.42, y - s * 0.55), 180, 360, fill=hat + (255,), outline=INK)
    else: d.pieslice((x - s * 0.36, y - s * 1.2, x + s * 0.36, y - s * 0.6), 180, 360, fill=(54, 46, 44, 255), outline=INK)

def orange(d, x, y, s, u, t, arg):
    sq = _clamp((u - 0.22) / 0.15)
    rx = s * 2.3 * (1 + 0.2 * sq); ry = s * 2.3 * (1 - 0.24 * sq)
    d.ellipse((x - rx * 0.9, y + ry * 0.85, x + rx * 0.9, y + ry * 1.2), fill=(40, 30, 20, 70))
    d.ellipse((x - rx, y - ry, x + rx, y + ry), fill=(244, 148, 30, 255), outline=INK, width=_lw(s, 0.12))
    d.ellipse((x - rx * 0.6, y - ry * 0.75, x - rx * 0.2, y - ry * 0.4), fill=(255, 208, 118, 210))
    d.polygon([(x, y - ry), (x + s * 1.0, y - ry - s * 0.55), (x + s * 0.55, y - ry + s * 0.12)], fill=(70, 140, 60, 255), outline=INK)
    for sx in (-1, 1):
        for k in range(3):
            fx = x + sx * rx * (0.98 - 0.12 * sq); fy = y - ry * 0.55 + k * ry * 0.55
            d.ellipse((fx - s * 0.5, fy - s * 0.42, fx + s * 0.5, fy + s * 0.42), fill=SKIN, outline=INK)
    if sq > 0.4:
        r = random.Random(7); p = _clamp((u - 0.3) / 0.4)
        for i in range(18):
            a = r.uniform(0, 6.283); dd = s * (1.5 + 4.5 * p) * r.uniform(0.6, 1.1)
            px = x + math.cos(a) * dd * 1.2; py = y + math.sin(a) * dd * 0.8 + p * p * s * 1.5
            rr = s * 0.28 * (1 - 0.5 * p)
            d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=(250, 170, 40, int(235 * (1 - p * 0.6))))
        for i in range(8):
            a = i * 0.785 + 0.3; d.line([(x + math.cos(a) * rx * 1.15, y + math.sin(a) * ry * 1.15), (x + math.cos(a) * rx * (1.35 + 0.4 * p), y + math.sin(a) * ry * (1.35 + 0.4 * p))], fill=(255, 226, 150, 230), width=_lw(s, 0.14))

def banner(d, x, y, s, u, t, txt):
    h = s * 8.5; w = s * 9.0; ch = s * 4.6
    d.line([(x, y), (x, y - h)], fill=(80, 56, 34, 255), width=_lw(s, 0.3))
    d.ellipse((x - s * 0.3, y - h - s * 0.3, x + s * 0.3, y - h + s * 0.3), fill=(214, 170, 60, 255), outline=INK)
    top = []; bot = []
    for i in range(13):
        q = i / 12; wv = math.sin(t * 3.2 + q * 4.2) * s * 0.35 * q
        top.append((x + q * w, y - h + wv)); bot.append((x + q * w, y - h + ch + wv * 1.2))
    d.polygon(top + bot[::-1], fill=(188, 52, 42, 255), outline=INK)
    if txt:
        words = txt.split(); half = (len(words) + 1) // 2; lines = [" ".join(words[:half]), " ".join(words[half:])]
        f = font(int(s * 1.05)); cy = y - h + ch * 0.5 - (len(lines) - 1) * s * 0.65
        for i, ln in enumerate(lines):
            if not ln: continue
            bb = d.textbbox((0, 0), ln, font=f); tw = bb[2] - bb[0]
            d.text((x + w * 0.5 - tw / 2 + math.sin(t * 3.2 + 2.1) * s * 0.15, cy + i * s * 1.3 - (bb[3] - bb[1]) / 2), ln, font=f, fill=(250, 240, 214, 255))

def hall(d, x, y, s, u, t, txt):
    w = s * 4.8
    d.rectangle((x - w, y - s * 0.6, x + w, y + s * 0.5), fill=(176, 150, 112, 255), outline=INK)
    for k in range(5):
        px = x - w + k * w / 2
        d.rectangle((px - s * 0.2, y - s * 3.6, px + s * 0.2, y - s * 0.6), fill=(150, 62, 44, 255), outline=INK)
    d.polygon([(x - w * 1.25, y - s * 3.5), (x - w * 0.8, y - s * 5.2), (x + w * 0.8, y - s * 5.2), (x + w * 1.25, y - s * 3.5)], fill=(120, 66, 50, 255), outline=INK)
    d.polygon([(x - w * 0.9, y - s * 5.2), (x, y - s * 6.6), (x + w * 0.9, y - s * 5.2)], fill=(140, 76, 56, 255), outline=INK)
    for sx in (-1, 1):
        d.ellipse((x + sx * w * 0.9 - s * 0.35, y - s * 3.4, x + sx * w * 0.9 + s * 0.35, y - s * 2.5), fill=(240, 120, 40, 255), outline=INK)
    sp = _clamp((u - 0.45) / 0.2); cols = [(120, 90, 60), (60, 90, 120), (140, 60, 60), (70, 110, 80), (110, 80, 110), (150, 120, 60), (80, 80, 100)]
    for i in range(7):
        px = x + (i - 3) * s * 1.35; py = y + s * 1.9 + (i % 2) * s * 0.35
        _person(d, px, py, s * 0.72, cols[i], beard=True, arm=sp * (0.7 + 0.3 * math.sin(t * 9 + i)) if sp > 0 else 0)
    if sp > 0 and txt:
        bs = s * (3.2 + 0.5 * math.sin(t * 10)) * min(1, sp * 1.8)
        cx, cy = x, y - s * 8.2; pts = []
        for i in range(20):
            rr = bs * (1.0 if i % 2 == 0 else 0.62); a = i * math.pi / 10; pts.append((cx + math.cos(a) * rr * 1.5, cy + math.sin(a) * rr))
        d.polygon(pts, fill=(250, 214, 80, 255), outline=INK)
        f = font(int(s * 1.9)); bb = d.textbbox((0, 0), txt, font=f)
        d.text((cx - (bb[2] - bb[0]) / 2, cy - (bb[3] - bb[1]) / 2 - bb[1] * 0.3), txt, font=f, fill=(150, 30, 26, 255))

def granary(d, x, y, s, u, t, arg):
    for dx in (-2.6, -0.9, 0.9, 2.6): d.line([(x + dx * s, y + s * 0.5), (x + dx * s, y + s * 1.9)], fill=(90, 62, 36, 255), width=_lw(s, 0.22))
    d.rectangle((x - s * 3.4, y - s * 2.2, x + s * 3.4, y + s * 0.5), fill=(190, 160, 118, 255), outline=INK, width=_lw(s))
    d.polygon([(x - s * 4.2, y - s * 2.2), (x, y - s * 4.6), (x + s * 4.2, y - s * 2.2)], fill=(122, 74, 52, 255), outline=INK)
    open_ = _clamp(u * 3)
    d.rectangle((x - s * 1.1, y - s * 1.8, x + s * 1.1, y + s * 0.5), fill=(26, 18, 14, 255), outline=INK)
    d.polygon([(x - s * 1.1, y - s * 1.8), (x - s * (1.1 + 1.1 * open_), y - s * 1.2), (x - s * (1.1 + 1.1 * open_), y + s * 0.5), (x - s * 1.1, y + s * 0.5)], fill=(120, 84, 50, 255), outline=INK)
    d.polygon([(x + s * 1.1, y - s * 1.8), (x + s * (1.1 + 1.1 * open_), y - s * 1.2), (x + s * (1.1 + 1.1 * open_), y + s * 0.5), (x + s * 1.1, y + s * 0.5)], fill=(120, 84, 50, 255), outline=INK)
    sx_, sy_ = x + s * 5.4, y + s * 0.9
    d.ellipse((sx_ - s * 0.9, sy_ - s * 0.85, sx_ + s * 0.9, sy_ + s * 0.9), fill=(214, 184, 120, 255), outline=INK)
    d.line([(sx_ - s * 1.2, sy_ - s * 1.1), (sx_ + s * 1.2, sy_ + s * 1.1)], fill=(190, 40, 34, 255), width=_lw(s, 0.28))
    d.line([(sx_ + s * 1.2, sy_ - s * 1.1), (sx_ - s * 1.2, sy_ + s * 1.1)], fill=(190, 40, 34, 255), width=_lw(s, 0.28))
    for i in range(3):
        q = (t * 0.7 + i * 0.33) % 1
        d.arc((x - s * 3 + q * s * 5, y - s * 1.5 - q * s * 1.5, x - s * 2 + q * s * 5, y - s * 0.5 - q * s * 1.5), 200, 340, fill=(230, 220, 190, int(200 * (1 - q))), width=_lw(s, 0.12))

def bridge(d, x, y, s, u, t, arg):
    d.rectangle((x - s * 7, y - s * 0.4, x + s * 7, y + s * 2.6), fill=(70, 130, 180, 255), outline=INK)
    for sx in (-1, 1): d.rectangle((x + (sx * 7 if sx > 0 else -11) * s, y - s * 1.2, x + (11 if sx > 0 else -7) * s, y + s * 2.8), fill=(150, 130, 84, 255), outline=INK)
    fall = _clamp((u - 0.2) / 0.5)
    for i in range(5):
        px = x - s * 7 + i * s * 1.4
        if px + s * 1.4 < x - s * 0.5:
            d.rectangle((px, y - s * 1.2, px + s * 1.3, y - s * 0.6), fill=(150, 104, 60, 255), outline=INK)
        else:
            dy = fall * fall * s * 3.2 * (1 + 0.2 * i); rot = fall * 0.6
            d.polygon([(px, y - s * 1.2 + dy), (px + s * 1.3, y - s * (1.2 - rot) + dy), (px + s * 1.3, y - s * (0.6 - rot) + dy), (px, y - s * 0.6 + dy)], fill=(150, 104, 60, 255), outline=INK)
    ft = _clamp((u - 0.5) / 0.3)
    for k in range(3):
        ang = -0.25 - ft * (0.9 + 0.1 * k); bx = x + s * (8 + k * 1.3); by = y - s * 1.2
        d.line([(bx, by), (bx + math.cos(ang) * s * 4.5, by + math.sin(ang) * s * 4.5 * -1 * -1)], fill=(100, 70, 40, 255), width=_lw(s, 0.45))
    for k in range(5):
        tx = x - s * 10.5 + k * s * 0.9
        d.polygon([(tx - s * 0.35, y - s * 1.2), (tx, y - s * 2.5), (tx + s * 0.35, y - s * 1.2)], fill=(120, 96, 70, 255), outline=INK)

def heat(d, x, y, s, u, t, arg):
    r = s * 2.6
    for k in range(12):
        a = k * math.pi / 6 + t * 0.8; d.line([(x + math.cos(a) * r * 1.2, y + math.sin(a) * r * 1.2), (x + math.cos(a) * r * (1.7 + 0.2 * math.sin(t * 5 + k)), y + math.sin(a) * r * (1.7 + 0.2 * math.sin(t * 5 + k)))], fill=(250, 190, 40, 255), width=_lw(s, 0.26))
    d.ellipse((x - r, y - r, x + r, y + r), fill=(252, 206, 56, 255), outline=INK, width=_lw(s, 0.14))
    for k in range(4):
        yy = y + r * 1.9 + k * s * 0.9; pts = [(x - s * 4.5 + i * s * 0.6, yy + math.sin(i * 0.9 + t * 6 + k) * s * 0.28) for i in range(16)]
        d.line(pts, fill=(222, 120, 50, 200), width=_lw(s, 0.16))
    for k in range(5):
        q = (t * 0.8 + k * 0.2) % 1; px = x + (k - 2) * s * 1.7
        d.ellipse((px - s * 0.22, y + r * 1.3 + q * s * 3.5, px + s * 0.22, y + r * 1.3 + q * s * 3.5 + s * 0.5), fill=(90, 160, 220, int(220 * (1 - q))))

def tomb(d, x, y, s, u, t, arg):
    d.ellipse((x - s * 4, y - s * 1.6, x + s * 4, y + s * 1.4), fill=(124, 104, 74, 255), outline=INK, width=_lw(s))
    d.rectangle((x - s * 0.6, y - s * 3.8, x + s * 0.6, y - s * 0.6), fill=(160, 156, 148, 255), outline=INK)
    d.polygon([(x - s * 0.6, y - s * 3.8), (x, y - s * 4.4), (x + s * 0.6, y - s * 3.8)], fill=(160, 156, 148, 255), outline=INK)
    p = _clamp((u - 0.3) / 0.6); r = random.Random(5)
    for i in range(16):
        a = r.uniform(0, math.pi); sp = r.uniform(0.6, 2.2)
        px = x + math.cos(a) * sp * s * p * 2.4 * (1 if i % 2 else -1); py = y - s * 0.5 - math.sin(a) * sp * s * p * 1.7 + p * p * s * 2.4
        d.rectangle((px - s * 0.18, py - s * 0.1, px + s * 0.18, py + s * 0.1), fill=(100, 78, 50, int(255 * (1 - p * 0.5))), outline=INK)
    for k in range(3):
        q = (t * 0.5 + k * 0.33) % 1; d.ellipse((x - s * 1 + k * s - q * s, y - s * 4.5 - q * s * 3, x + s * 0.4 + k * s, y - s * 3.5 - q * s * 3), fill=(210, 206, 198, int(150 * (1 - q))))

def statue(d, x, y, s, u, t, arg):
    d.rectangle((x - s * 2.8, y + s * 0.3, x + s * 2.8, y + s * 1.2), fill=(140, 96, 56, 255), outline=INK)
    for sx in (-1.6, 1.6):
        wr = s * 0.9; d.ellipse((x + sx * s - wr, y + s * 0.8, x + sx * s + wr, y + s * 0.8 + wr * 2), fill=(90, 62, 36, 255), outline=INK)
    gold = (236, 190, 60, 255)
    d.polygon([(x - s * 0.9, y + s * 0.3), (x + s * 0.9, y + s * 0.3), (x + s * 0.55, y - s * 1.9), (x - s * 0.55, y - s * 1.9)], fill=gold, outline=INK)
    d.ellipse((x - s * 0.5, y - s * 3.0, x + s * 0.5, y - s * 1.9), fill=gold, outline=INK)
    d.polygon([(x - s * 0.6, y - s * 3.0), (x - s * 0.4, y - s * 3.7), (x, y - s * 3.2), (x + s * 0.4, y - s * 3.7), (x + s * 0.6, y - s * 3.0)], fill=(250, 220, 110, 255), outline=INK)
    for k in range(5):
        a = k * 1.26 + t * 2; d.line([(x + math.cos(a) * s * 1.3, y - s * 1.6 + math.sin(a) * s * 1.3), (x + math.cos(a) * s * 1.7, y - s * 1.6 + math.sin(a) * s * 1.7)], fill=(255, 240, 160, int(180 + 70 * math.sin(t * 6 + k))), width=_lw(s, 0.12))

def seal(d, x, y, s, u, t, arg):
    fl = math.sin(t * 2) * s * 0.3
    for k in range(10):
        a = k * math.pi / 5 + t * 0.5; d.line([(x + math.cos(a) * s * 3.2, y + fl + math.sin(a) * s * 3.2), (x + math.cos(a) * s * 4.4, y + fl + math.sin(a) * s * 4.4)], fill=(255, 224, 120, 210), width=_lw(s, 0.18))
    d.rectangle((x - s * 1.7, y - s * 0.8 + fl, x + s * 1.7, y + s * 1.6 + fl), fill=(176, 40, 34, 255), outline=INK, width=_lw(s, 0.12))
    d.rectangle((x - s * 1.1, y - s * 0.3 + fl, x + s * 1.1, y + s * 1.1 + fl), outline=(250, 226, 160, 255), width=_lw(s, 0.14))
    d.ellipse((x - s * 0.9, y - s * 2.2 + fl, x + s * 0.9, y - s * 0.5 + fl), fill=(214, 170, 60, 255), outline=INK)
    d.line([(x, y - s * 0.5 + fl), (x - s * 0.6, y + s * 3.0 + fl)], fill=(190, 40, 34, 255), width=_lw(s, 0.3))
    d.line([(x, y - s * 0.5 + fl), (x + s * 0.6, y + s * 3.2 + fl)], fill=(190, 40, 34, 255), width=_lw(s, 0.3))

def meeting(d, x, y, s, u, t, arg):
    d.ellipse((x - s * 4.2, y - s * 1.3, x + s * 4.2, y + s * 1.9), fill=(150, 104, 60, 255), outline=INK, width=_lw(s))
    d.ellipse((x - s * 3.2, y - s * 0.9, x + s * 3.2, y + s * 1.3), fill=(176, 130, 80, 255))
    d.ellipse((x - s * 0.55, y - s * 0.8, x + s * 0.55, y + s * 0.1), fill=(250, 160, 50, 255), outline=INK)
    cols = [(60, 90, 120), (140, 60, 60), (70, 110, 80), (110, 80, 110), (150, 120, 60), (80, 80, 100)]
    for i in range(6):
        a = math.pi + i * math.pi / 5; px = x + math.cos(a) * s * 4.4; py = y - s * 0.6 + math.sin(a) * s * 2.3 - s * 1.0
        _person(d, px, py, s * 0.75, cols[i], hat=(40, 40, 50))
    for sx in (-1, 1):
        d.line([(x + sx * s * 3.6, y + s * 1.5), (x + sx * s * 3.9, y + s * 3.5)], fill=INK, width=_lw(s, 0.12))
    if arg:
        px = x - s * 8.2 + math.sin(t * 2) * s * 0.2; py = y + s * 2.0
        _person(d, px, py, s * 0.62, (214, 150, 50), hat=(190, 50, 40))
        d.ellipse((px + s * 0.55, py - s * 0.15, px + s * 1.05, py + s * 0.35), fill=(244, 148, 30, 255), outline=INK)
        d.line([(px - s * 1.4, py - s * 0.9), (px - s * 1.0, py - s * 1.5)], fill=(60, 60, 60, 255), width=_lw(s, 0.1))

def scrolls2(d, x, y, s, u, t, arg):
    for sx, col in ((-1, (188, 52, 42)), (1, (52, 142, 86))):
        cx = x + sx * s * 3.6
        d.rectangle((cx - s * 1.9, y - s * 2.4, cx + s * 1.9, y + s * 2.4), fill=(242, 230, 198, 255), outline=INK, width=_lw(s, 0.12))
        for k in range(4): d.line([(cx - s * 1.2, y - s * 1.5 + k * s * 0.8), (cx + s * 1.2, y - s * 1.5 + k * s * 0.8)], fill=(120, 96, 64, 255), width=_lw(s, 0.1))
        d.line([(cx, y + s * 2.4), (cx, y + s * 4.6)], fill=(70, 50, 30, 255), width=_lw(s, 0.2))
        d.polygon([(cx, y + s * 4.6), (cx + sx * s * 2.2, y + s * 4.9), (cx + sx * s * 2.0, y + s * 5.8), (cx, y + s * 5.5)], fill=col + (255,), outline=INK)
    for i, sg in enumerate((-1, 1)): d.line([(x - s * 0.8, y - s * 0.5 + sg * s * 0.5), (x + s * 0.8, y - s * 0.5 + sg * s * 0.5)], fill=(40, 30, 24, 255), width=_lw(s, 0.22))

def pawn(d, x, y, s, u, t, arg):
    sw = math.sin(t * 2.5) * s * 0.35
    d.ellipse((x - s * 1.8, y + s * 2.2, x + s * 1.8, y + s * 3.0), fill=(40, 30, 20, 80))
    d.polygon([(x - s * 1.5, y + s * 2.7), (x + s * 1.5, y + s * 2.7), (x + s * 0.7, y), (x - s * 0.7, y)], fill=(236, 190, 60, 255), outline=INK)
    d.ellipse((x - s * 0.95, y - s * 1.9, x + s * 0.95, y), fill=(236, 190, 60, 255), outline=INK)
    d.polygon([(x - s * 0.8, y - s * 1.7), (x - s * 0.55, y - s * 2.6), (x, y - s * 2.0), (x + s * 0.55, y - s * 2.6), (x + s * 0.8, y - s * 1.7)], fill=(190, 52, 42, 255), outline=INK)
    hx, hy = x + sw, y - s * 6.5
    d.ellipse((hx - s * 1.2, hy - s * 0.8, hx + s * 1.2, hy + s * 0.9), fill=SKIN, outline=INK)
    for k, off in enumerate((-0.8, -0.3, 0.3, 0.8)):
        d.line([(hx + off * s, hy + s * 0.5), (x + off * s * 0.6 + sw * 0.3, y - s * (1.9 - abs(off)))], fill=(60, 50, 44, 255), width=_lw(s, 0.07))

def calendar(d, x, y, s, u, t, arg):
    n = int(1 + _clamp(u * 1.05) * (int(arg or 9) - 1))
    d.rounded_rectangle((x - s * 3.4, y - s * 3.8, x + s * 3.4, y + s * 3.6), s * 0.5, fill=(250, 244, 226, 255), outline=INK, width=_lw(s, 0.14))
    d.rounded_rectangle((x - s * 3.4, y - s * 3.8, x + s * 3.4, y - s * 2.1), s * 0.5, fill=(188, 52, 42, 255), outline=INK, width=_lw(s, 0.14))
    f = font(int(s * 5.6)); bb = d.textbbox((0, 0), str(n), font=f)
    d.text((x - (bb[2] - bb[0]) / 2, y - s * 1.5 - bb[1] * 0.5), str(n), font=f, fill=(46, 38, 58, 255))
    f2 = font(int(s * 1.1)); tx = 'NGÀY'; b2 = d.textbbox((0, 0), tx, font=f2)
    d.text((x - (b2[2] - b2[0]) / 2, y - s * 3.5), tx, font=f2, fill=(250, 240, 214, 255))

def bowl(d, x, y, s, u, t, arg):
    d.ellipse((x - s * 3.0, y - s * 0.6, x + s * 3.0, y + s * 0.7), fill=(240, 232, 214, 255), outline=INK, width=_lw(s, 0.12))
    d.pieslice((x - s * 3.0, y - s * 1.9, x + s * 3.0, y + s * 2.1), 0, 180, fill=(214, 120, 70, 255), outline=INK, width=_lw(s, 0.12))
    d.ellipse((x - s * 2.6, y - s * 0.45, x + s * 2.6, y + s * 0.5), fill=(246, 240, 226, 255), outline=INK)
    for dx in (-0.5, 0.5): d.line([(x + dx * s, y - s * 0.2), (x + dx * s + s * 3.0, y - s * 3.4)], fill=(120, 80, 44, 255), width=_lw(s, 0.18))
    for k in range(3):
        q = (t * 0.6 + k * 0.33) % 1; d.line([(x - s * 1.2 + k * s * 1.2, y - s * 0.9 - q * s * 1.2), (x - s * 0.9 + k * s * 1.2, y - s * 1.5 - q * s * 1.2)], fill=(150, 150, 150, int(160 * (1 - q))), width=_lw(s, 0.1))

def cross(d, x, y, s, u, t, arg):
    p = _clamp(u * 3)
    d.line([(x - s * 3 * p, y - s * 3 * p), (x + s * 3 * p, y + s * 3 * p)], fill=(190, 40, 34, 255), width=_lw(s, 0.55))
    d.line([(x + s * 3 * p, y - s * 3 * p), (x - s * 3 * p, y + s * 3 * p)], fill=(190, 40, 34, 255), width=_lw(s, 0.55))

def camp(d, x, y, s, u, t, arg):
    from mapdraw import fire
    for k, (dx, c) in enumerate(((-3.2, (176, 60, 48)), (3.2, (176, 60, 48)), (0, (190, 96, 60)))):
        cx = x + dx * s; cy = y + (0 if k < 2 else -s * 0.8)
        d.polygon([(cx - s * 1.8, cy + s * 1.3), (cx, cy - s * 2.2), (cx + s * 1.8, cy + s * 1.3)], fill=c + (255,), outline=INK)
        d.polygon([(cx - s * 0.5, cy + s * 1.3), (cx, cy - s * 0.2), (cx + s * 0.5, cy + s * 1.3)], fill=(40, 28, 22, 255))
    fire(d, x, y + s * 2.4, s * 0.9, t, 11)

def pennant_row(d, x, y, s, u, t, arg):
    for k in range(5):
        px = x + (k - 2) * s * 1.6; d.line([(px, y), (px, y - s * 3.6)], fill=(80, 56, 34, 255), width=_lw(s, 0.14))
        d.polygon([(px, y - s * 3.6), (px + s * 1.2, y - s * 3.2 + math.sin(t * 4 + k) * s * 0.15), (px, y - s * 2.6)], fill=(188, 52, 42, 255) if arg != 'g' else (52, 142, 86, 255), outline=INK)

def ping(d, x, y, s, u, t, arg):
    col = (188, 52, 42) if arg == 'r' else (52, 142, 86)
    for k in range(3):
        q = (t * 0.5 + k / 3.0) % 1; rr = s * (0.8 + 3.6 * q)
        d.ellipse((x - rr, y - rr * 0.7, x + rr, y + rr * 0.7), outline=col + (int(230 * (1 - q)),), width=_lw(s, 0.2))
    d.ellipse((x - s * 0.45, y - s * 0.45, x + s * 0.45, y + s * 0.45), fill=col + (255,), outline=INK)

def storm(d, x, y, s, u, t, arg):
    """Bão trên biển: mây đen, mưa xiên, tia chớp lóe lên theo nhịp, sóng cuộn quanh vùng thuyền."""
    r = random.Random(23)
    # mây
    for k, (dx, dy, rx, ry, g) in enumerate(((2.2, -7.8, 3.6, 1.7, 58), (5.4, -8.6, 4.4, 2.1, 46), (8.6, -7.7, 3.4, 1.6, 62), (4.6, -7.0, 4.0, 1.4, 70))):
        wob = math.sin(t * 0.9 + k) * s * 0.25
        d.ellipse((x + dx * s - rx * s + wob, y + dy * s - ry * s, x + dx * s + rx * s + wob, y + dy * s + ry * s), fill=(g, g + 4, g + 14, 235), outline=(20, 20, 30, 255))
    # mưa xiên
    for i in range(260):
        px = x + (r.uniform(-9, 9)) * s; ph = (t * 1.6 + r.random()) % 1
        py = y - 6.0 * s + ph * 9.0 * s
        d.line([(px, py), (px - s * 0.35, py + s * 0.95)], fill=(226, 236, 252, 125), width=_lw(s, 0.10))
    # sóng cuộn
    for k in range(7):
        q = (t * 0.55 + k / 7.0) % 1; rr = s * (1.4 + 4.4 * q)
        d.arc((x - rr * 1.5, y + s * 1.5 - rr * 0.55, x + rr * 1.5, y + s * 1.5 + rr * 0.55), 200, 340, fill=(240, 246, 255, int(220 * (1 - q))), width=_lw(s, 0.16))
    # tia chớp: lóe vài lần mỗi chu kỳ 2,6 giây, đánh thẳng xuống đoàn thuyền
    cyc = (t % 2.6) / 2.6
    if cyc < 0.16 or 0.22 < cyc < 0.3:
        bx = x + s * 1.2 + math.sin(int(t / 2.6) * 2.1) * s * 1.6
        pts = [(bx + s * 0.6, y - s * 6.4), (bx - s * 0.3, y - s * 4.6), (bx + s * 0.5, y - s * 4.4), (bx - s * 0.5, y - s * 2.4), (bx + s * 0.25, y - s * 2.2), (bx - s * 0.4, y - s * 1.0), (bx + s * 0.2, y - s * 1.0), (bx - s * 0.1, y - s * 0.2)]
        d.line(pts, fill=(255, 255, 255, 255), width=_lw(s, 0.34))
        d.line(pts, fill=(255, 238, 140, 255), width=_lw(s, 0.16))
        d.ellipse((bx - s * 0.5, y - s * 0.6, bx + s * 0.5, y + s * 0.2), fill=(255, 250, 200, 255))

def _ship(d, x, y, s, tilt, col, flame=0.0, sink=0.0):
    """Một chiếc thuyền chiến lớn, có cột buồm và buồm; tilt (rad) nghiêng, sink 0..1 chìm dần."""
    c, sn = math.cos(tilt), math.sin(tilt)
    def R(px, py): return (x + px * c - py * sn, y + sink * s * 1.6 + px * sn + py * c)
    hull = [R(-2.2 * s, 0), R(2.4 * s, 0), R(1.8 * s, 0.9 * s), R(-1.7 * s, 0.9 * s)]
    d.polygon([R(-2.2 * s, -0.25 * s), R(-1.9 * s, 0)] + hull[1:2] + [R(2.7 * s, -0.4 * s)] + hull[2:], fill=col + (255,), outline=INK)
    d.line([R(0, 0), R(0, -3.6 * s)], fill=(70, 46, 28, 255), width=_lw(s, 0.16))
    d.polygon([R(0.1 * s, -3.4 * s), R(1.9 * s, -0.5 * s), R(0.1 * s, -0.5 * s)], fill=(236, 226, 200, 255), outline=INK)
    d.polygon([R(-0.1 * s, -3.0 * s), R(-1.5 * s, -0.7 * s), R(-0.1 * s, -0.7 * s)], fill=(214, 202, 172, 255), outline=INK)
    if flame > 0:
        for k in range(4):
            fx, fy = R((-0.6 + k * 0.5) * s, -0.8 * s - (k % 2) * s * 0.6)
            h = s * (0.5 + 0.5 * flame) * (0.8 + 0.4 * math.sin(k * 2.0 + flame * 9))
            d.polygon([(fx - h * 0.35, fy), (fx, fy - h * 1.5), (fx + h * 0.35, fy)], fill=(255, 150, 40, 235))
            d.polygon([(fx - h * 0.18, fy), (fx, fy - h * 0.9), (fx + h * 0.18, fy)], fill=(255, 226, 120, 245))

def ship_strike(d, x, y, s, u, t, arg):
    """Cận cảnh: ba thuyền chiến giữa sóng lớn, sét đánh trúng thuyền giữa, cháy rồi đắm dần."""
    # biển và sóng
    for k in range(9):
        wx = x + (k - 4) * s * 1.35; ph = math.sin(t * 1.7 + k * 0.8)
        d.arc((wx - s * 1.1, y + s * 1.0 + ph * s * 0.2, wx + s * 1.1, y + s * 2.3 + ph * s * 0.2), 200, 340, fill=(236, 244, 255, 220), width=_lw(s, 0.12))
    for k in range(6):
        wy = y + s * (1.6 + k * 0.45); d.arc((x - s * 5.6, wy - s * 0.3, x + s * 5.6, wy + s * 0.3), 200, 340, fill=(200, 220, 240, 130), width=_lw(s, 0.07))
    hit = _clamp((u - 0.25) / 0.2)
    sink = _clamp((u - 0.55) / 0.4)
    rock = math.sin(t * 2.1) * 0.10
    _ship(d, x - s * 4.3, y + s * 0.5 + math.sin(t * 1.3) * s * 0.15, s, 0.08 + rock, (120, 70, 130), 0.0, sink * 0.5)
    _ship(d, x + s * 4.3, y + s * 0.3 + math.sin(t * 1.1 + 2) * s * 0.15, s, -0.10 - rock, (120, 70, 130), 0.0, sink * 0.8)
    _ship(d, x, y + s * 0.2 + math.sin(t * 1.6 + 1) * s * 0.18, s, 0.16 * hit + rock, (140, 80, 140), hit * (1 - sink * 0.5), sink)
    # mây đen phía trên
    for k, (dx, dy, rx, ry, g) in enumerate(((-3.0, -8.2, 3.2, 1.3, 52), (0.4, -9.0, 4.0, 1.6, 44), (3.4, -8.1, 3.0, 1.2, 58))):
        d.ellipse((x + dx * s - rx * s, y + dy * s - ry * s, x + dx * s + rx * s, y + dy * s + ry * s), fill=(g, g + 4, g + 14, 245), outline=(20, 20, 30, 255))
    # mưa
    r = random.Random(7)
    for i in range(110):
        px = x + r.uniform(-6.5, 6.5) * s; ph = (t * 1.8 + r.random()) % 1
        py = y - 7.0 * s + ph * 9.6 * s
        d.line([(px, py), (px - s * 0.3, py + s * 0.85)], fill=(226, 236, 252, 150), width=_lw(s, 0.07))
    # tia sét đánh vào đỉnh cột thuyền giữa, lóe theo nhịp
    cyc = (t % 2.6) / 2.6
    if cyc < 0.16 or 0.22 < cyc < 0.3:
        top = (x, y - s * 3.4)
        pts = [(x - s * 0.8, y - s * 7.6), (x + s * 0.5, y - s * 6.1), (x - s * 0.3, y - s * 5.8), (x + s * 0.7, y - s * 4.6), (x - s * 0.1, y - s * 4.4), top]
        d.line(pts, fill=(255, 255, 255, 255), width=_lw(s, 0.34))
        d.line(pts, fill=(255, 238, 140, 255), width=_lw(s, 0.16))

def stakes(d, x, y, s, u, t, arg):
    """Cận cảnh: lòng sông với các hàng cọc nhọn; cọc được đóng thụt lên xuống theo nhịp búa và mọc dần. Dải sông dời lên trên để không che quân."""
    y = y - s * 2.6
    d.polygon([(x - s * 6.5, y - s * 2.4), (x + s * 6.5, y - s * 2.9), (x + s * 6.5, y + s * 2.1), (x - s * 6.5, y + s * 1.8)], fill=(96, 142, 168, 150), outline=(40, 70, 90, 220))
    for k in range(5):
        wy = y + (k - 2) * s * 0.85
        d.arc((x - s * 6.0, wy - s * 0.25, x + s * 6.0, wy + s * 0.25), 190, 350, fill=(220, 238, 250, 120), width=_lw(s, 0.06))
    rows = 3; per = 8; total = rows * per
    shown = int(total * _clamp(u * 1.3))
    n = 0
    for rw in range(rows):
        for k in range(per):
            n += 1
            if n > shown: break
            px = x + (k - (per - 1) / 2) * s * 1.55 + (rw % 2) * s * 0.7
            py = y + (rw - 1) * s * 1.35 + (k - per / 2) * s * 0.08
            # nhịp đóng: mỗi cọc có pha riêng, thụt xuống khi búa giáng rồi nhô lên lại
            ph = (t * 1.25 + n * 0.37) % 1.0
            drive = 0.5 + 0.5 * math.cos(ph * 2 * math.pi)
            hit = max(0.0, 1.0 - ph * 6.0)
            h = s * (1.35 + 0.65 * drive) * (0.45 if n >= shown - 1 else 1.0)
            d.polygon([(px - s * 0.2, py), (px + s * 0.2, py), (px + s * 0.12, py - h * 0.8), (px, py - h), (px - s * 0.12, py - h * 0.8)], fill=(124, 82, 46, 255), outline=INK)
            d.line([(px - s * 0.2, py), (px + s * 0.2, py)], fill=(30, 50, 70, 200), width=_lw(s, 0.1))
            if hit > 0:  # bụi nước văng lên khi cọc lún xuống
                d.arc((px - s * 0.45, py - s * 0.2, px + s * 0.45, py + s * 0.2), 200, 340, fill=(255, 255, 255, int(220 * hit)), width=_lw(s, 0.08))
    # lính hai bên bờ, một người giơ búa đóng cọc theo nhịp
    for bx_ in (x - s * 7.4, x + s * 7.4):
        _person(d, bx_, y + s * 0.4, s * 0.8, (70, 110, 150), hat=(60, 120, 70))
    sw = abs(math.sin(t * 5.0)) * 0.6
    _person(d, x - s * 8.8, y - s * 0.4, s * 0.8, (60, 100, 140), hat=(60, 120, 70), arm=sw)


# ---- tiểu cảnh: cày ruộng (trâu kéo cày, người cày, bụi đất, chim cò, cỏ lay) ----
def _ln(d, pts, col, w):
    d.line(pts, fill=col, width=max(1, int(w)))

def _buffalo(d, x, y, s, ph):
    """Trâu quay mặt sang phải: thân xám đen, sừng cong ra sau, bốn chân bước luân phiên."""
    body = (74, 78, 86, 255); dark = (48, 50, 58, 255)
    for lx, p in ((-1.0, 0.0), (-0.45, 3.1), (0.55, 1.6), (1.1, 4.7)):
        a = math.sin(ph + p) * 0.45
        _ln(d, [(x + lx * s, y + s * 0.5), (x + (lx + a) * s, y + s * 1.55)], dark, s * 0.2)
        d.ellipse((x + (lx + a) * s - s * 0.14, y + s * 1.48, x + (lx + a) * s + s * 0.2, y + s * 1.62), fill=(30, 28, 30, 255))
    _ln(d, [(x - s * 1.5, y - s * 0.1), (x - s * 1.9, y + s * 0.5 + math.sin(ph * 0.7) * s * 0.15)], dark, s * 0.12)
    d.ellipse((x - s * 1.6, y - s * 0.7, x + s * 1.5, y + s * 0.85), fill=body, outline=INK)
    d.ellipse((x - s * 0.9, y - s * 0.55, x + s * 0.3, y - s * 0.05), fill=(96, 100, 108, 150))
    d.polygon([(x + s * 1.1, y - s * 0.55), (x + s * 1.95, y - s * 0.35), (x + s * 2.25, y + s * 0.2), (x + s * 1.2, y + s * 0.55)], fill=body, outline=INK)
    d.ellipse((x + s * 1.85, y - s * 0.02, x + s * 2.3, y + s * 0.34), fill=(150, 142, 138, 255), outline=INK)
    d.arc((x + s * 1.0, y - s * 1.2, x + s * 1.9, y - s * 0.3), 200, 340, fill=(226, 218, 196, 255), width=max(2, int(s * 0.14)))
    d.ellipse((x + s * 1.55, y - s * 0.35, x + s * 1.7, y - s * 0.2), fill=(250, 250, 250, 255))
    d.ellipse((x + s * 1.6, y - s * 0.31, x + s * 1.68, y - s * 0.23), fill=INK)

def _egret(d, x, y, s, ph):
    """Cò trắng đứng/bước theo luống cày."""
    _ln(d, [(x - s * 0.1, y), (x - s * 0.12, y + s * 0.55)], (60, 50, 40, 255), s * 0.07)
    _ln(d, [(x + s * 0.08, y), (x + s * 0.1, y + s * 0.55)], (60, 50, 40, 255), s * 0.07)
    d.ellipse((x - s * 0.38, y - s * 0.3, x + s * 0.38, y + s * 0.15), fill=(250, 250, 248, 255), outline=INK)
    _ln(d, [(x + s * 0.25, y - s * 0.15), (x + s * 0.5, y - s * 0.55 + math.sin(ph) * s * 0.06)], (250, 250, 248, 255), s * 0.1)
    d.polygon([(x + s * 0.5, y - s * 0.6), (x + s * 0.8, y - s * 0.52), (x + s * 0.5, y - s * 0.5)], fill=(240, 190, 60, 255))

def plough(d, x, y, s, u, t, arg):
    """Tiểu cảnh người cày ruộng: ruộng đất nâu, trâu kéo cày chậm rãi, đất lật theo lưỡi cày, bụi bay, cò trắng bay theo."""
    # phóng ra từ điểm trên bản đồ lúc vào và thu về lúc ra (hiệu ứng "zoom vào tiểu cảnh")
    g = min(1.0, u * 7.0, (1.0 - u) * 7.0); g = max(0.0, g); g = g * g * (3 - 2 * g)
    s = s * (0.18 + 0.82 * g)
    W2, H2 = s * 10.5, s * 6.0
    # bóng đổ và khung giấy
    d.rounded_rectangle((x - W2 + s * 0.35, y - H2 + s * 0.5, x + W2 + s * 0.35, y + H2 * 0.92 + s * 0.5), radius=int(s * 0.9), fill=(40, 30, 20, 80))
    top = y - H2; hor = y - s * 1.7; bot = y + H2 * 0.92
    d.rounded_rectangle((x - W2, top, x + W2, bot), radius=int(s * 0.9), fill=(222, 234, 208, 255), outline=INK, width=_lw(s, 0.12))
    # trời, núi xa, mặt trời
    d.ellipse((x + s * 6.3, top + s * 0.9, x + s * 8.1, top + s * 2.7), fill=(255, 236, 160, 255))
    d.ellipse((x + s * 5.9, top + s * 0.5, x + s * 8.5, top + s * 3.1), outline=(255, 236, 160, 120), width=_lw(s, 0.1))
    for cx, cw, ch, col in ((-6.5, 3.7, 2.3, (176, 200, 168)), (-0.5, 4.9, 2.9, (160, 190, 160)), (6.1, 4.0, 2.1, (172, 198, 166))):
        d.pieslice((x + cx * s - cw * s, hor - ch * s, x + cx * s + cw * s, hor + ch * s), 180, 360, fill=col + (255,))
    # cánh chim bay trên trời
    for k in range(3):
        bx = x - s * 6.5 + ((t * 0.55 + k * 0.33) % 1.0) * s * 13 ; by = top + s * (1.4 + 0.7 * k) + math.sin(t * 2 + k) * s * 0.15
        fl = math.sin(t * 9 + k) * s * 0.18
        _ln(d, [(bx - s * 0.4, by + fl), (bx, by), (bx + s * 0.4, by + fl)], (70, 70, 76, 255), s * 0.07)
    # mặt ruộng: nửa đã cày (trái) sẫm, nửa chưa cày (phải) nhạt
    d.rounded_rectangle((x - W2 + s * 0.12, hor, x + W2 - s * 0.12, bot - s * 0.06), radius=int(s * 0.8), fill=(168, 126, 82, 255), corners=(False, False, True, True))
    d.rectangle((x - W2 + s * 0.12, hor, x + W2 - s * 0.12, hor + s * 0.5), fill=(138, 160, 96, 255))
    px = x - s * 0.8 + math.sin(t * 0.5) * s * 0.35
    d.rounded_rectangle((x - W2 + s * 0.12, hor + s * 0.5, px, bot - s * 0.06), radius=int(s * 0.8), fill=(118, 80, 50, 255), corners=(False, False, False, True))
    scroll_ = (t * 1.4) % 1.0
    for i in range(10):
        fy = hor + s * (0.95 + i * 0.62)
        pts = []
        for j in range(0, 41):
            fx = x - W2 + s * 0.15 + (px - (x - W2 + s * 0.15)) * j / 40
            pts.append((fx, fy + math.sin(j * 0.55 - scroll_ * 6.283 + i) * s * 0.07))
        _ln(d, pts, (88, 58, 36, 255), s * 0.13)
        _ln(d, [(a, b + s * 0.1) for a, b in pts], (150, 108, 70, 255), s * 0.05)
        # luống chưa cày: gốc rạ
        for j in range(0, 12):
            gx = px + s * 0.6 + j * (x + W2 - s * 0.5 - px) / 12
            if gx < x + W2 - s * 0.3:
                _ln(d, [(gx, fy), (gx + math.sin(t * 2.5 + i + j) * s * 0.05, fy - s * 0.28)], (120, 138, 70, 255), s * 0.05)
    # bước đi
    ph = t * 3.2
    base_y = y + s * 0.9
    ub = s * 1.15
    bx_ = px + s * 5.0 + math.sin(ph * 2) * s * 0.03
    by_ = base_y + s * 1.35 - ub * 1.55 - abs(math.sin(ph * 2)) * s * 0.05
    # trục cày nối từ ách trên cổ trâu xuống lưỡi cày
    nx, ny = bx_ + ub * 1.05, by_ - ub * 0.25
    d.polygon([(px + s * 0.35, base_y + s * 0.62), (px + s * 0.55, base_y + s * 0.8), (nx + s * 0.05, ny + s * 0.2), (nx - s * 0.1, ny - s * 0.05)], fill=(130, 92, 56, 255), outline=INK)
    _ln(d, [(nx - s * 0.15, ny - s * 0.45), (nx + s * 0.25, ny + s * 0.55)], (96, 66, 40, 255), s * 0.2)
    # lưỡi cày và đất lật
    d.polygon([(px + s * 0.1, base_y + s * 0.8), (px + s * 0.7, base_y + s * 0.8), (px + s * 0.4, base_y + s * 1.2)], fill=(70, 74, 84, 255), outline=INK)
    for k in range(7):
        a = ((t * 1.3 + k * 0.17) % 1.0)
        cx = px - s * (0.1 + 1.5 * a); cy = base_y + s * 0.85 - math.sin(a * 3.1416) * s * 0.8 + a * a * s * 0.7
        r = s * (0.13 - 0.06 * a)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(112, 76, 46, int(255 * (1 - a * 0.5))))
    for k in range(5):
        a = ((t * 0.9 + k * 0.23) % 1.0)
        cx = px - s * (0.2 + 2.2 * a); cy = base_y + s * 1.05 - a * s * 0.35
        r = s * (0.12 + 0.3 * a)
        d.ellipse((cx - r, cy - r * 0.6, cx + r, cy + r * 0.6), fill=(196, 168, 128, int(140 * (1 - a))))
    # người cày: nón lá, áo nâu, hai tay giữ cán cày
    fx_ = px - s * 1.3 + math.sin(ph * 2) * s * 0.03
    fy_ = base_y - s * 0.05
    for sg in (-1, 1):
        a = math.sin(ph + (0 if sg < 0 else 3.14)) * 0.4
        _ln(d, [(fx_ + sg * s * 0.12, fy_ + s * 0.7), (fx_ + sg * s * 0.12 + a * s, fy_ + s * 1.5)], (96, 74, 54, 255), s * 0.22)
    d.polygon([(fx_ - s * 0.5, fy_ + s * 0.85), (fx_ + s * 0.5, fy_ + s * 0.85), (fx_ + s * 0.38, fy_ - s * 0.5), (fx_ - s * 0.3, fy_ - s * 0.5)], fill=(116, 84, 56, 255), outline=INK)
    d.ellipse((fx_ - s * 0.3, fy_ - s * 1.08, fx_ + s * 0.3, fy_ - s * 0.5), fill=SKIN, outline=INK)
    d.polygon([(fx_ - s * 0.95, fy_ - s * 0.88), (fx_ + s * 0.05, fy_ - s * 1.75), (fx_ + s * 1.0, fy_ - s * 0.88)], fill=(214, 184, 112, 255), outline=INK)
    hx, hy = px + s * 0.3, base_y + s * 0.8
    _ln(d, [(hx, hy), (fx_ + s * 0.5, fy_ - s * 0.1)], (130, 92, 56, 255), s * 0.15)
    _ln(d, [(fx_ + s * 0.25, fy_ + s * 0.1), (fx_ + s * 0.55, fy_ - s * 0.05)], SKIN, s * 0.17)
    # trâu
    _buffalo(d, bx_, by_, ub, ph * 2)
    # cò trắng đi theo luống vừa cày
    for k in range(3):
        ex = px - s * (2.2 + k * 1.9) + math.sin(t * 0.8 + k * 2) * s * 0.3
        ey = base_y + s * (1.5 + 0.35 * k) - abs(math.sin(t * 2.2 + k * 1.7)) * s * 0.1
        _egret(d, ex, ey, s * 0.9, t * 3 + k)
    # cỏ lay ở mép dưới khung
    for j in range(46):
        gx = x - W2 + s * 0.4 + j * (2 * W2 - s * 0.8) / 45
        gh = s * (0.55 + 0.35 * ((j * 37) % 7) / 7)
        sway = math.sin(t * 2.2 + j * 0.6) * s * 0.22
        _ln(d, [(gx, bot - s * 0.18), (gx + sway, bot - s * 0.18 - gh)], (96, 140, 70, 255), s * 0.08)
        _ln(d, [(gx + s * 0.07, bot - s * 0.18), (gx + sway * 1.2 + s * 0.1, bot - s * 0.18 - gh * 0.8)], (126, 168, 84, 255), s * 0.05)
    d.rounded_rectangle((x - W2, top, x + W2, bot), radius=int(s * 0.9), outline=INK, width=_lw(s, 0.12))

KINDS_EXTRA = dict(ship_strike=ship_strike, stakes=stakes)

KINDS = dict(ping=ping, orange=orange, banner=banner, hall=hall, granary=granary, bridge=bridge, heat=heat, tomb=tomb, statue=statue, seal=seal,
             meeting=meeting, scrolls2=scrolls2, pawn=pawn, calendar=calendar, bowl=bowl, cross=cross, camp=camp, pennants=pennant_row, storm=storm, ship_strike=ship_strike, stakes=stakes, plough=plough)

def draw(d, kind, x, y, s, u, t, arg):
    KINDS[kind](d, x, y, s, u, t, arg)
