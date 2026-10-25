"""Thành phần hình ảnh mới cho phim bản đồ (bản dựng 3): sông, thẻ chương, thẻ nhân vật, thẻ câu nói, thẻ hài,
thanh sức mạnh, bản đồ nhỏ, đài bắn tên, hào, địa đạo, đồ vật rơi dọc đường."""
import math, os, random
from PIL import Image, ImageDraw, ImageFont
import build2 as B
from build2 import font, W, H, ease, clamp
import mapdraw as MD

INK = (30, 22, 16, 255)
CREAM = (246, 238, 214, 255)
GOLD = (246, 206, 102, 255)


def font_i(sz):
    p = os.path.join(os.path.dirname(B.FONT), 'Lora-Italic-Variable.ttf')
    try:
        f = ImageFont.truetype(p, int(sz))
        try:
            f.set_variation_by_name('Italic')
        except Exception:
            pass
        return f
    except Exception:
        return font(sz, False)


def lerp(a, b, u):
    return a + (b - a) * u


# ------------------------------------------------------------ sông
def smooth(P, n=10):
    """Làm mượt đường gấp khúc bằng Catmull-Rom."""
    if len(P) < 3:
        return list(P)
    Q = [P[0]] + list(P) + [P[-1]]
    out = []
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
        for k in range(n):
            u = k / n
            u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in (0, 1)))
    out.append(P[-1])
    return out


def draw_river(d, P, wpx, t, K):
    """P: các điểm màn hình (đã nhân K). Vẽ dòng sông có bờ và vệt nước chảy."""
    if len(P) < 2:
        return
    S = smooth(P, 8)
    d.line(S, fill=(58, 96, 128, 255), width=int(wpx * 1.45), joint='curve')
    d.line(S, fill=(104, 160, 196, 255), width=int(wpx), joint='curve')
    # vệt sáng chạy theo dòng
    tot = sum(math.dist(S[i], S[i + 1]) for i in range(len(S) - 1))
    if tot < 10:
        return
    seg = 46 * K
    off = (t * 40 * K) % (seg * 2)
    pos = -off
    i = 0
    acc = 0.0
    while pos < tot:
        a, b = pos, pos + seg * 0.8
        if b > 0:
            pa = _at(S, max(a, 0)); pb = _at(S, min(b, tot))
            d.line([pa, pb], fill=(214, 236, 248, 190), width=max(2, int(wpx * 0.22)))
        pos += seg * 2


def _at(S, dist):
    acc = 0.0
    for i in range(len(S) - 1):
        L = math.dist(S[i], S[i + 1])
        if acc + L >= dist:
            r = (dist - acc) / max(L, 1e-6)
            return (lerp(S[i][0], S[i + 1][0], r), lerp(S[i][1], S[i + 1][1], r))
        acc += L
    return S[-1]


# ------------------------------------------------------------ thẻ chương
def title_layer(year, name, sub):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(im)
    f1, f2, f3 = font(130), font(96), font(40, False)
    _g = ImageDraw.Draw(Image.new('RGBA', (4, 4)))
    for _sz in range(130, 50, -4):  # chữ lớn phải nằm gọn trong khung (lề tối thiểu 60 px)
        f1 = font(_sz)
        if _g.textlength(year, font=f1) <= (W - 160): break
    for _sz in range(96, 40, -4):
        f2 = font(_sz)
        if _g.textlength(name, font=f2) <= (W - 160): break
    for _sz in range(40, 24, -2):
        f3 = font(_sz, False)
        if _g.textlength(sub, font=f3) <= (W - 160): break
    y0 = H // 2 - 190
    t1 = year
    w1 = g.textlength(t1, font=f1)
    g.text((W / 2 - w1 / 2 + 5, y0 + 6), t1, font=f1, fill=(0, 0, 0, 230))
    g.text((W / 2 - w1 / 2, y0), t1, font=f1, fill=GOLD)
    g.line([(W / 2 - 330, y0 + 175), (W / 2 + 330, y0 + 175)], fill=GOLD, width=4)
    w2 = g.textlength(name, font=f2)
    g.text((W / 2 - w2 / 2 + 4, y0 + 205), name, font=f2, fill=(0, 0, 0, 230))
    g.text((W / 2 - w2 / 2, y0 + 200), name, font=f2, fill=(250, 244, 228, 255))
    w3 = g.textlength(sub, font=f3)
    g.text((W / 2 - w3 / 2 + 2, y0 + 335), sub, font=f3, fill=(0, 0, 0, 230))
    g.text((W / 2 - w3 / 2, y0 + 333), sub, font=f3, fill=(224, 212, 184, 255))
    return im


# ------------------------------------------------------------ thẻ nhân vật (icon cờ màu + tên)
def card3(name, role, col):
    f1, f2 = font(46), font(28, False)
    g0 = ImageDraw.Draw(Image.new('RGBA', (4, 4)))
    w = int(max(g0.textlength(name, font=f1), g0.textlength(role, font=f2)) + 150)
    im = Image.new('RGBA', (w, 118), (0, 0, 0, 0))
    g = ImageDraw.Draw(im)
    g.rounded_rectangle((0, 0, w, 118), 16, fill=(16, 10, 6, 228), outline=col + (255,), width=3)
    # cờ lớn
    fx, fy = 26, 100
    g.line([(fx, fy), (fx, 16)], fill=(130, 100, 64, 255), width=6)
    g.polygon([(fx, 16), (fx + 62, 30), (fx + 50, 46), (fx + 62, 62), (fx, 56)], fill=col + (255,), outline=(240, 230, 205, 255))
    g.text((112, 14), name, font=f1, fill=(250, 240, 215, 255))
    g.text((112, 70), role, font=f2, fill=(215, 200, 170, 255))
    return im


# ------------------------------------------------------------ thẻ câu nói
def wrap(txt, f, maxw, g):
    words = txt.split()
    lines, cur = [], ''
    for w_ in words:
        tr = (cur + ' ' + w_).strip()
        if g.textlength(tr, font=f) <= maxw:
            cur = tr
        else:
            lines.append(cur)
            cur = w_
    lines.append(cur)
    return lines


import os as _os
_P = bool(_os.environ.get('PORTRAIT'))


def quote_layer(text, who, col):
    f = font_i(50)
    fw = font(34)
    g0 = ImageDraw.Draw(Image.new('RGBA', (4, 4)))
    lines = wrap(text, f, 800 if _P else 1020, g0)
    lh = 68
    h = len(lines) * lh + 150
    w = 980 if _P else 1200
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    g = ImageDraw.Draw(im)
    g.rounded_rectangle((0, 0, w, h), 24, fill=(14, 9, 5, 232), outline=col + (255,), width=4)
    g.rectangle((0, 0, 18, h), fill=col + (255,))
    g.text((46, -8), '“', font=font(170), fill=GOLD)
    for i, l in enumerate(lines):
        g.text((120, 36 + i * lh), l, font=f, fill=(250, 244, 228, 255))
    tw = g.textlength('— ' + who, font=fw)
    g.text((w - 50 - tw, h - 64), '— ' + who, font=fw, fill=col + (255,) if sum(col) > 200 else GOLD)
    return im


# ------------------------------------------------------------ thẻ hài
def joke_layer(icon, text, t, k):
    """icon: 'fire' | 'scroll' | 'skull' | 'flag' | 'coin' ; k: 0..1 độ hiện."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(im)
    r = 150 * (0.72 + 0.28 * ease(min(1, k * 1.6))) * (1 + 0.04 * math.sin(t * 6))
    cx, cy = W // 2, (640 if _P else 400)
    g.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(246, 238, 214, 245), outline=(60, 44, 28, 255), width=8)
    g.ellipse((cx - r + 18, cy - r + 18, cx + r - 18, cy + r - 18), outline=(176, 130, 60, 255), width=4)
    if icon == 'fire':
        MD.fire(g, cx, cy + r * 0.55, r * 0.62, t, 7)
    elif icon == 'scroll':
        MD.scroll(g, cx, cy, r * 0.62)
    elif icon == 'skull':
        MD.skull(g, cx, cy, r * 0.62)
    elif icon == 'flag':
        MD.whiteflag(g, cx, cy, r * 0.62)
    elif icon == 'coin':
        g.ellipse((cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5), fill=(222, 176, 60, 255), outline=INK, width=6)
        g.rectangle((cx - r * 0.12, cy - r * 0.2, cx + r * 0.12, cy + r * 0.2), outline=INK, width=6)
    f = font(66)
    lines = wrap(text, f, (W - 140) if _P else 1500, g)
    wt = max(g.textlength(l, font=f) for l in lines)
    lh = 84
    g.rounded_rectangle((W / 2 - wt / 2 - 40, cy + r + 24, W / 2 + wt / 2 + 40, cy + r + 64 + lh * len(lines)), 22, fill=(14, 9, 5, 232), outline=GOLD, width=3)
    for i, l in enumerate(lines):
        lw = g.textlength(l, font=f)
        g.text((W / 2 - lw / 2, cy + r + 36 + i * lh), l, font=f, fill=(250, 244, 228, 255))
    return im


# ------------------------------------------------------------ thanh sức mạnh
def meter_layer(title, rows):
    """rows: [(nhãn, màu, giá trị 0..1)]"""
    n = len(rows)
    w, h = 560, 80 + n * 58
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    g = ImageDraw.Draw(im)
    g.rounded_rectangle((0, 0, w, h), 18, fill=(14, 9, 5, 225), outline=(176, 130, 60, 255), width=3)
    g.text((26, 14), title, font=font(36), fill=GOLD)
    for i, (lab, col, v) in enumerate(rows):
        y = 74 + i * 58
        g.text((26, y + 4), lab, font=font(27, False), fill=(232, 222, 196, 255))
        x0, x1 = 176, w - 28
        g.rounded_rectangle((x0, y + 6, x1, y + 38), 10, fill=(60, 50, 40, 255))
        vv = max(0.0, min(1.0, v))
        if vv > 0.01:
            g.rounded_rectangle((x0, y + 6, x0 + (x1 - x0) * vv, y + 38), 10, fill=col + (255,))
    return im


def table_layer(title, rows, w=1180):
    """Khung so sánh/sơ đồ: rows [(nhãn trái, nội dung phải)]; tự xuống dòng, luôn nằm gọn trong w."""
    pad = 30
    ft, fl, fr = font(40), font(30), font(30, False)
    im0 = Image.new('RGBA', (8, 8)); g0 = ImageDraw.Draw(im0)
    lw = max(int(g0.textlength(l, font=fl)) for l, _ in rows) + 28
    lw = min(lw, 360)
    rw = w - 2 * pad - lw - 30
    def wrap(t, f, mw):
        out, cur = [], ''
        for wd in t.split():
            tr = (cur + ' ' + wd).strip()
            if g0.textlength(tr, font=f) <= mw: cur = tr
            else:
                if cur: out.append(cur)
                cur = wd
        if cur: out.append(cur)
        return out or ['']
    blocks = [(wrap(l, fl, lw - 10), wrap(r, fr, rw)) for l, r in rows]
    lh = 40
    hs = [max(len(a), len(b)) * lh + 22 for a, b in blocks]
    h = pad + 56 + sum(hs) + pad
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    g = ImageDraw.Draw(im)
    g.rounded_rectangle((0, 0, w - 1, h - 1), 20, fill=(14, 9, 5, 232), outline=(176, 130, 60, 255), width=3)
    g.text((pad, pad - 4), title, font=ft, fill=GOLD)
    y = pad + 62
    for (la, ra), hh in zip(blocks, hs):
        g.line((pad, y - 6, w - pad, y - 6), fill=(110, 84, 48, 255), width=2)
        for i, ln in enumerate(la): g.text((pad, y + i * lh), ln, font=fl, fill=GOLD)
        for i, ln in enumerate(ra): g.text((pad + lw + 30, y + i * lh), ln, font=fr, fill=(236, 226, 200, 255))
        y += hh
    return im


# ------------------------------------------------------------ bản đồ nhỏ
def minimap_base(pyr3, w=380, h=230):
    im = pyr3.resize((w, h), Image.LANCZOS).convert('RGBA')
    g = ImageDraw.Draw(im)
    g.rectangle((0, 0, w - 1, h - 1), outline=(60, 44, 28, 255), width=4)
    return im


# ------------------------------------------------------------ vật thể
def tower(d, x, y, s, t, col=(120, 84, 48)):
    """Đài canh bằng gỗ, có lính cung."""
    ink = INK
    for dx in (-0.8, 0.8):
        d.line([(x + dx * s, y + s * 0.9), (x + dx * s * 0.62, y - s * 1.9)], fill=(90, 62, 36, 255), width=max(3, int(s * 0.2)))
    d.line([(x - 0.7 * s, y + s * 0.3), (x + 0.7 * s, y - s * 1.0)], fill=(90, 62, 36, 255), width=max(2, int(s * 0.12)))
    d.line([(x + 0.7 * s, y + s * 0.3), (x - 0.7 * s, y - s * 1.0)], fill=(90, 62, 36, 255), width=max(2, int(s * 0.12)))
    d.rectangle((x - s * 1.05, y - s * 2.2, x + s * 1.05, y - s * 1.8), fill=col + (255,), outline=ink)
    d.polygon([(x - s * 1.2, y - s * 2.2), (x, y - s * 3.1), (x + s * 1.2, y - s * 2.2)], fill=(150, 60, 44, 255), outline=ink)
    for dx in (-0.5, 0.5):
        d.ellipse((x + dx * s - s * 0.2, y - s * 2.6, x + dx * s + s * 0.2, y - s * 2.2), fill=(232, 196, 150, 255), outline=ink)


def debris(d, x, y, s, u):
    """Đài đổ: các mảnh gỗ văng ra và bụi."""
    r = random.Random(3)
    for i in range(14):
        a = r.uniform(0, math.pi)
        sp = r.uniform(0.6, 2.2)
        px = x + math.cos(a) * sp * s * u * 2.2 * (1 if i % 2 else -1)
        py = y - math.sin(a) * sp * s * u * 1.6 + u * u * s * 2.4
        d.rectangle((px - s * 0.16, py - s * 0.08, px + s * 0.16, py + s * 0.08), fill=(100, 70, 40, int(255 * (1 - u * 0.6))), outline=INK)
    rr = s * (0.8 + 2.4 * u)
    d.ellipse((x - rr * 1.4, y - rr * 0.5, x + rr * 1.4, y + rr * 0.5), outline=(226, 208, 170, int(210 * (1 - u))), width=5)


def sack(d, x, y, s, a=255):
    d.ellipse((x - s * 0.5, y - s * 0.45, x + s * 0.5, y + s * 0.5), fill=(214, 184, 120, a), outline=INK)
    d.polygon([(x - s * 0.2, y - s * 0.4), (x, y - s * 0.75), (x + s * 0.2, y - s * 0.4)], fill=(214, 184, 120, a), outline=INK)
    d.line([(x - s * 0.22, y - s * 0.4), (x + s * 0.22, y - s * 0.4)], fill=(120, 80, 40, a), width=max(2, int(s * 0.1)))


def saddle(d, x, y, s, a=255):
    d.arc((x - s * 0.6, y - s * 0.5, x + s * 0.6, y + s * 0.4), 180, 360, fill=(120, 74, 38, a), width=max(3, int(s * 0.28)))
    d.line([(x - s * 0.6, y - s * 0.05), (x + s * 0.6, y - s * 0.05)], fill=(120, 74, 38, a), width=max(3, int(s * 0.22)))


def boat(d,x,y,s,col,face=1):
    """Thuyền chiến nhỏ có buồm."""
    d.polygon([(x-s*1.4,y),(x+s*1.4,y),(x+s*0.9,y+s*0.55),(x-s*0.9,y+s*0.55)],fill=col+(255,),outline=INK)
    d.line([(x,y),(x,y-s*1.5)],fill=(60,44,28,255),width=max(2,int(s*0.12)))
    d.polygon([(x,y-s*1.5),(x+face*s*1.0,y-s*0.7),(x,y-s*0.2)],fill=(236,226,200,255),outline=INK)
