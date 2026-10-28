"""Thẻ thông tin 960x900 cho video 'Tên đường' (vẽ bằng code, không AI). Mỗi hàm nhận (ts, u): giây và tiến độ trong câu."""
import json, math, os
from PIL import Image, ImageDraw, ImageFilter
PW, PH = 960, 900
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SEA, LAND, EDGE, GOLD, WHITE, BLUE = (10, 38, 78), (58, 98, 150), (150, 190, 235), (255, 210, 74), (255, 255, 255), (11, 78, 162)
INK = (6, 18, 36)
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x, s=1.5): x = max(0.0, min(1.0, x)); c = s + 1; return 1 + c * (x - 1) ** 3 + s * (x - 1) ** 2
_FONT = {}
def setfonts(BVP, BARLOW, PLAY): _FONT.update(BVP=BVP, BARLOW=BARLOW, PLAY=PLAY)
def tw(d, s, f): return d.textbbox((0, 0), s, font=f)[2]
def ctext(d, x, y, s, f, fill): d.text((x - tw(d, s, f) / 2, y), s, font=f, fill=fill)
def wrap(d, s, f, wmax):
    out, line = [], ''
    for w in s.split():
        t = (line + ' ' + w).strip()
        if tw(d, t, f) > wmax and line: out.append(line); line = w
        else: line = t
    if line: out.append(line)
    return out
def base():
    im = Image.new('RGB', (PW, PH), SEA); return im, ImageDraw.Draw(im)
# ---------- bản đồ Việt Nam (đất liền, đảo, Hoàng Sa, Trường Sa; không vẽ biên giới, không đường lạ) ----------
LON0, LON1, LAT0, LAT1 = 101.5, 118.5, 6.0, 23.8
S = min(PW / ((LON1 - LON0) * math.cos(math.radians(14))), PH / (LAT1 - LAT0)); KX = S * math.cos(math.radians(14))
OX = (PW - (LON1 - LON0) * KX) / 2
def mp(lon, lat): return (OX + (lon - LON0) * KX, (LAT1 - lat) * S)
_MAP = {}
K3 = 3
def vnmap():
    if 'm' in _MAP: return _MAP['m']
    im = Image.new('RGB', (PW * K3, PH * K3), SEA); d = ImageDraw.Draw(im)
    J = json.load(open(f'{R}/assets/ten_duong/ne_10m_land.json'))
    for f in J['features']:
        g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in polys:
            xs = [p[0] for p in poly[0]]; ys = [p[1] for p in poly[0]]
            if max(xs) < LON0 - 1 or min(xs) > LON1 + 1 or max(ys) < LAT0 - 1 or min(ys) > LAT1 + 1: continue
            d.polygon([(a * K3, b * K3) for a, b in (mp(*p) for p in poly[0])], fill=LAND, outline=EDGE, width=2)
            for h in poly[1:]: d.polygon([(a * K3, b * K3) for a, b in (mp(*p) for p in h)], fill=SEA)
    BV = _FONT['BVP']
    import random
    for (lon, lat, k, rr) in [(112.0, 16.4, 9, 0.7), (113.6, 9.6, 22, 2.4), (114.3, 10.6, 5, 1.0)]:
        rnd = random.Random(int(lon * 10))
        for _ in range(k):
            x, y = mp(lon + rnd.uniform(-rr, rr), lat + rnd.uniform(-rr * 0.9, rr * 0.9)); x *= K3; y *= K3; d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=GOLD)
    f = BV(26 * K3, False)
    for s_, lon, lat in [('Quần đảo Hoàng Sa', 112.0, 15.4), ('(Việt Nam)', 112.0, 14.9), ('Quần đảo Trường Sa', 114.3, 7.1), ('(Việt Nam)', 114.3, 6.6)]:
        x, y = mp(lon, lat); d.text((x * K3 - tw(d, s_, f) / 2, y * K3), s_, font=f, fill=GOLD)
    f = BV(32 * K3, False); x, y = mp(112.3, 20.0)
    for i, s_ in enumerate(('BIỂN', 'ĐÔNG')): d.text((x * K3 - tw(d, s_, f) / 2, y * K3 + i * 38 * K3), s_, font=f, fill=(110, 150, 210))
    _MAP['m'] = im; return im
def view(ts, c, z, t0=0.3, t1=1.8):
    """Cắt và phóng bản đồ: zoom từ toàn cảnh (1) tới z quanh điểm c=(lon,lat)."""
    k = ease((ts - t0) / (t1 - t0)); zz = 1 + (z - 1) * k
    cx, cy = mp(*c); w, h = PW / zz, PH / zz
    fx, fy = PW / 2, PH / 2; cx = fx + (cx - fx) * k; cy = fy + (cy - fy) * k
    x0 = max(0, min(PW - w, cx - w / 2)); y0 = max(0, min(PH - h, cy - h / 2))
    im = vnmap().crop((int(x0 * K3), int(y0 * K3), int((x0 + w) * K3), int((y0 + h) * K3))).resize((PW, PH), Image.LANCZOS)
    return im, (lambda lon, lat: ((mp(lon, lat)[0] - x0) * zz, (mp(lon, lat)[1] - y0) * zz))
def pin(d, x, y, label, t, dx=14, dy=-12, big=False):
    f = _FONT['BVP'](40); a = ease(t)
    d.ellipse((x - 26 * a, y - 26 * a, x + 26 * a, y + 26 * a), outline=GOLD, width=4); d.ellipse((x - 11 * a, y - 11 * a, x + 11 * a, y + 11 * a), fill=GOLD)
    if a > 0.5:
        w = tw(d, label, f); xx = x + dx if dx >= 0 else x + dx - w
        d.rounded_rectangle((xx - 10, y + dy - 6, xx + w + 10, y + dy + 54), radius=12, fill=(6, 18, 36)); d.text((xx, y + dy), label, font=f, fill=WHITE)
def arrow(d, a, b, p):
    x = a[0] + (b[0] - a[0]) * p; y = a[1] + (b[1] - a[1]) * p
    d.line([a, (x, y)], fill=GOLD, width=8)
    if p > 0.05:
        ang = math.atan2(b[1] - a[1], b[0] - a[0]); d.polygon([(x, y), (x - 32 * math.cos(ang - 0.45), y - 32 * math.sin(ang - 0.45)), (x - 32 * math.cos(ang + 0.45), y - 32 * math.sin(ang + 0.45))], fill=GOLD)
def card_map(ts, u, pins, link=None, title=None, center=(106.0, 20.8), z=4.0):
    im, tf = view(ts, center, z); d = ImageDraw.Draw(im)
    pts = {k: tf(*v[:2]) for k, v in pins.items()}
    if link: arrow(d, pts[link[0]], pts[link[1]], ease((ts - 2.2) / 1.2))
    for i, (k, v) in enumerate(pins.items()):
        pin(d, pts[k][0], pts[k][1], k, (ts - 1.6 - 0.6 * i) / 0.5, v[2], v[3])
    if title:
        d.rectangle((0, 0, PW, 78), fill=(6, 18, 36)); ctext(d, PW / 2, 16, title, _FONT['BVP'](38), WHITE)
    return im
# ---------- thẻ chữ ----------
def count(a, b, p): return int(round(a + (b - a) * ease(p)))
def card_year(ts, u, year, line1, line2=None, prev=None):
    im, d = base()
    for y in range(PH): d.line([(0, y), (PW, y)], fill=(10 + y // 40, 38 + y // 30, 78 + y // 18))
    p = ease(ts / 1.0); n = count(year - 60 if year < 1900 else year - 30, year, p)
    ctext(d, PW / 2, 150, str(n), _FONT['BARLOW'](300), GOLD)
    sc = back((ts - 0.7) / 0.5)
    f = _FONT['BVP'](58); y = 520
    for l in wrap(d, line1, f, 820): ctext(d, PW / 2, y, l, f, WHITE); y += 78
    if line2 and ts > 1.4:
        f2 = _FONT['BVP'](40, False); y += 20
        for l in wrap(d, line2, f2, 800): ctext(d, PW / 2, y, l, f2, (170, 195, 230)); y += 56
    return im
def card_text(ts, u, big, lines, small=None):
    im, d = base()
    for y in range(PH): d.line([(0, y), (PW, y)], fill=(10 + y // 40, 38 + y // 30, 78 + y // 18))
    f = _FONT['PLAY'](78); ls = []
    for l in wrap(d, big, f, 840): ls.append(l)
    y = 300 - 50 * len(ls); a = ease(ts / 0.6)
    for l in ls: ctext(d, PW / 2, y + (1 - a) * 40, l, f, GOLD); y += 104
    f2 = _FONT['BVP'](42, False); y += 30
    for i, s in enumerate(lines):
        if ts > 0.8 + 0.5 * i:
            for l in wrap(d, s, f2, 800): ctext(d, PW / 2, y, l, f2, WHITE); y += 58
    return im
def box(d, x, y, w, h, text, fill, fg=WHITE, size=30, sub=None):
    d.rounded_rectangle((x, y, x + w, y + h), radius=22, fill=fill, outline=WHITE, width=3)
    f = _FONT['BVP'](size)
    ls = wrap(d, text, f, w - 24); yy = y + h / 2 - (len(ls) * (size + 8)) / 2 - (14 if sub else 0)
    for l in ls: ctext(d, x + w / 2, yy, l, f, fg); yy += size + 8
    if sub: ctext(d, x + w / 2, yy + 4, sub, _FONT['BVP'](24, False), (210, 225, 250))
def card_family(ts, u):
    im, d = base()
    def conn(a, b, p):
        d.line([a, (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)], fill=GOLD, width=5)
    pA = ease((ts - 0.4) / 0.5); pB = ease((ts - 1.2) / 0.5); pC = ease((ts - 2.0) / 0.5); pD = ease((ts - 2.8) / 0.5)
    if pA > 0: box(d, 40, 90, 400, 150, 'Trần Nguyên Đán', (60, 98, 150), sub='quan Tư đồ' if pA > 0.9 else None)
    if pB > 0: conn((240, 240), (240, 400), pB)
    if pB > 0.9: box(d, 40, 400, 400, 150, 'Trần Thị Thái', (120, 70, 120), sub='mẹ')
    if pC > 0: box(d, 520, 400, 400, 150, 'Nguyễn Phi Khanh', (60, 98, 150), sub='cha' if pC > 0.9 else None)
    if pC > 0.9: d.line([(440, 475), (520, 475)], fill=GOLD, width=5)
    if pD > 0:
        conn((480, 475), (480, 640), pD)
        if pD > 0.9: box(d, 220, 640, 520, 190, 'Nguyễn Trãi', BLUE, size=56, sub='hiệu Ức Trai')
    return im
def card_books(ts, u):
    im, d = base(); names = [('Quân trung từ mệnh tập', 'thư từ gửi tướng nhà Minh'), ('Quốc âm thi tập', 'thơ bằng chữ Nôm'), ('Ức Trai thi tập', 'tập thơ chữ Hán')]
    for i, (a, b) in enumerate(names):
        p = back((ts - 0.3 - 0.7 * i) / 0.5)
        if p <= 0: continue
        y = 60 + i * 280 + (1 - min(1, p)) * 80
        d.rounded_rectangle((70, y, 890, y + 230), radius=26, fill=(236, 220, 180), outline=(150, 110, 60), width=6)
        d.rectangle((70, y, 130, y + 230), fill=(150, 56, 44)); d.rectangle((830, y, 890, y + 230), fill=(150, 56, 44))
        f = _FONT['PLAY'](46); ctext(d, PW / 2, y + 46, a, f, INK); ctext(d, PW / 2, y + 140, b, _FONT['BVP'](32, False), (90, 60, 30))
    return im
def card_timeline(ts, u):
    im, d = base(); items = [('Nhà Hồ', 'Nguyễn Trãi làm quan', (60, 98, 150)), ('Quân nhà Minh sang', 'chiếm nước ta', (150, 56, 44)), ('Nhà Hồ sụp đổ', '', (90, 90, 110))]
    for i, (a, b, c) in enumerate(items):
        p = ease((ts - 0.3 - 0.9 * i) / 0.5)
        if p <= 0: continue
        y = 90 + i * 270
        if i: d.line([(PW / 2, y - 90), (PW / 2, y)], fill=GOLD, width=6)
        box(d, 140 + (1 - p) * 300, y, 680, 170, a, c, size=46, sub=b or None)
    return im
def card_street(ts, u):
    im, d = base()
    for y in range(PH): d.line([(0, y), (PW, y)], fill=(10 + y // 40, 38 + y // 30, 78 + y // 18))
    data = [('HÀ NỘI', 'Đường Nguyễn Trãi', 2.17, 'bắt đầu từ Ngã Tư Sở', 'Mang tên ông từ năm 1980'), ('THÀNH PHỐ HỒ CHÍ MINH', 'Đường Nguyễn Trãi (Quận 5)', 5.33, 'từ Công trường Phù Đổng đến đường Nguyễn Thị Nhỏ', 'Mang tên ông từ năm 1955')]
    for i, (city, name, km, line, nm) in enumerate(data):
        p = ease((ts - 0.2 - 2.4 * i) / 0.6)
        if p <= 0: continue
        y = 30 + i * 440 + (1 - p) * 60
        d.rounded_rectangle((30, y, PW - 30, y + 410), radius=28, fill=(12, 48, 98), outline=WHITE, width=3)
        d.rounded_rectangle((30, y, PW - 30, y + 74), radius=28, fill=BLUE); ctext(d, PW / 2, y + 12, city, _FONT['BVP'](40), WHITE)
        ctext(d, PW / 2, y + 90, name, _FONT['BVP'](38), (190, 210, 240))
        v = km * ease((ts - 0.7 - 2.4 * i) / 1.0); ctext(d, PW / 2 - 70, y + 120, f'{v:.2f}'.replace('.', ','), _FONT['BARLOW'](150), GOLD); d.text((PW / 2 + 110, y + 210), 'km', font=_FONT['BVP'](52), fill=WHITE)
        f = _FONT['BVP'](28, False); yy = y + 305
        for l in wrap(d, line, f, 840): ctext(d, PW / 2, yy, l, f, (190, 210, 240)); yy += 40
        if ts > 1.9 + 2.4 * i: ctext(d, PW / 2, y + 368, nm, _FONT['BVP'](32), WHITE)
    return im
def card_city(ts, u, i):
    im, d = base()
    for y in range(PH): d.line([(0, y), (PW, y)], fill=(10 + y // 40, 38 + y // 30, 78 + y // 18))
    data = [('HÀ NỘI', 'Đường Nguyễn Trãi', 2.17, 'bắt đầu từ Ngã Tư Sở', 'Mang tên ông từ năm 1980'), ('THÀNH PHỐ HỒ CHÍ MINH', 'Đường Nguyễn Trãi (Quận 5)', 5.33, 'từ Công trường Phù Đổng đến đường Nguyễn Thị Nhỏ', 'Mang tên ông từ năm 1955')][i]
    city, name, km, line, nm = data; p = ease(ts / 0.6); y = 90 + (1 - p) * 60
    d.rounded_rectangle((50, y, PW - 50, y + 720), radius=30, fill=(12, 48, 98), outline=WHITE, width=4)
    d.rounded_rectangle((50, y, PW - 50, y + 100), radius=30, fill=BLUE); ctext(d, PW / 2, y + 22, city, _FONT['BVP'](50), WHITE)
    ctext(d, PW / 2, y + 130, name, _FONT['BVP'](46), (190, 210, 240))
    v = km * ease((ts - 0.5) / 1.2); ctext(d, PW / 2 - 90, y + 200, f'{v:.2f}'.replace('.', ','), _FONT['BARLOW'](280), GOLD); d.text((PW / 2 + 150, y + 350), 'km', font=_FONT['BVP'](70), fill=WHITE)
    f = _FONT['BVP'](36, False); yy = y + 520
    for l in wrap(d, line, f, 640): ctext(d, PW / 2 + 90, yy, l, f, (190, 210, 240)); yy += 48
    if ts > 2.0: ctext(d, PW / 2, y + 635, nm, _FONT['BVP'](42), WHITE)
    return im
