"""Tiểu cảnh phóng vào từ một điểm trên bản đồ (giống cảnh cày tịch điền của Lê Hoàn): khung giấy nổi lên, cảnh nhỏ có người và đồ vật cử động, rồi thu về.
Chữ ký như mapprops: f(d, x, y, s, u, t, arg); u = tiến độ 0..1 của tiểu cảnh, t = giây tuyệt đối. Vẽ trên canvas 2x."""
import math
from build2 import font
INK = (30, 22, 16, 255); SKIN = (232, 196, 150, 255)
def _lw(s, k=0.1): return max(2, int(s * k))
def _ln(d, pts, col, w): d.line(pts, fill=col, width=max(2, int(w)), joint='curve')
def _e(d, cx, cy, rx, ry, fill, outline=INK, w=2): d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=fill, outline=outline, width=w)
def _poly(d, pts, fill, outline=INK): d.polygon(pts, fill=fill, outline=outline)
def _sky(d, x0, y0, x1, y1, top, bot, n=14):
    for i in range(n):
        a = i / (n - 1); c = tuple(int(top[k] * (1 - a) + bot[k] * a) for k in range(3))
        d.rectangle((x0, y0 + (y1 - y0) * i / n, x1, y0 + (y1 - y0) * (i + 1) / n + 1), fill=c + (255,))
def _frame(d, x, y, s, u, sky=((150, 190, 226), (236, 228, 200)), dy=0.0):
    """Khung giấy, phóng ra từ điểm bản đồ lúc vào và thu về lúc ra. Trả về (s, x0, y0, x1, y1, hor)."""
    _D = max(1.0, globals().get("_DUR", 8.0)); g = max(0.0, min(1.0, u * _D / 0.6, (1.0 - u) * _D / 0.5)); g = g * g * (3 - 2 * g)
    s = s * (0.62 + 0.38 * g); W2, H2 = s * 10.5, s * 6.0
    x0, y0, x1, y1 = x - W2, y - H2, x + W2, y + H2 * 0.92
    d.rounded_rectangle((x0 + s * 0.35, y0 + s * 0.5, x1 + s * 0.35, y1 + s * 0.5), radius=int(s * 0.9), fill=(40, 30, 20, 80))
    _sky(d, x0, y0, x1, y1, sky[0], sky[1])
    return s, x0, y0, x1, y1, y - s * 1.7
def _edge(d, x0, y0, x1, y1, s): d.rounded_rectangle((x0, y0, x1, y1), radius=int(s * 0.9), outline=INK, width=_lw(s, 0.12))
def _ground(d, x0, hor, x1, y1, col, s):
    d.rectangle((x0 + s * 0.12, hor, x1 - s * 0.12, y1 - s * 0.06), fill=col + (255,))
def _hills(d, x, hor, s, cols=((176, 200, 168), (160, 190, 160), (172, 198, 166))):
    for cx, cw, ch, col in ((-6.5, 3.7, 2.3, cols[0]), (-0.5, 4.9, 2.9, cols[1]), (6.1, 4.0, 2.1, cols[2])):
        d.pieslice((x + cx * s - cw * s, hor - ch * s, x + cx * s + cw * s, hor + ch * s), 180, 360, fill=col + (255,))
def _bird(d, bx, by, s, t, k=0):
    fl = math.sin(t * 9 + k) * s * 0.18; _ln(d, [(bx - s * 0.4, by + fl), (bx, by), (bx + s * 0.4, by + fl)], (70, 70, 76, 255), s * 0.07)
def _man(d, x, y, s, robe, hat=None, bald=False, child=False, face=1, walk=0.0, bow=0.0, arms=None, beard=False):
    """Người vẽ phẳng: chân bước, áo dài, đầu có mũ hoặc trọc hoặc búi tóc (trẻ con). y là mặt đất dưới chân. bow 0..1 cúi người."""
    k = 0.62 if child else 1.0; s = s * k * 1.45
    sw = math.sin(walk) * s * 0.35
    for sg in (-1, 1):
        _ln(d, [(x + sg * s * 0.14, y - s * 0.9), (x + sg * s * 0.14 + sw * sg, y)], (84, 66, 50, 255), s * 0.22)
    bx = x + bow * s * 0.5 * face; ty = y - s * 1.9 + bow * s * 0.5
    _poly(d, [(x - s * 0.5, y - s * 0.15), (x + s * 0.5, y - s * 0.15), (bx + s * 0.38, ty + s * 0.45), (bx - s * 0.38, ty + s * 0.45)], robe + (255,))
    if arms == 'up':
        for sg in (-1, 1): _ln(d, [(bx + sg * s * 0.34, ty + s * 0.6), (bx + sg * s * 0.62, ty - s * 0.2)], SKIN, s * 0.16)
    elif arms == 'front':
        for sg in (-1, 1): _ln(d, [(bx + sg * s * 0.34, ty + s * 0.6), (bx + face * s * 0.6, ty + s * 0.95)], SKIN, s * 0.16)
    hx, hy = bx, ty + s * 0.15
    _e(d, hx, hy, s * 0.3, s * 0.34, SKIN)
    if beard: _poly(d, [(hx - s * 0.24, hy + s * 0.05), (hx + s * 0.24, hy + s * 0.05), (hx, hy + s * 0.6)], (244, 242, 236, 255))
    if bald: pass
    elif child:
        for sg in (-1, 1): _e(d, hx + sg * s * 0.3, hy - s * 0.3, s * 0.15, s * 0.15, (54, 46, 44, 255))
        d.pieslice((hx - s * 0.3, hy - s * 0.4, hx + s * 0.3, hy + s * 0.1), 180, 360, fill=(54, 46, 44, 255), outline=INK)
    elif hat: d.pieslice((hx - s * 0.4, hy - s * 0.55, hx + s * 0.4, hy + s * 0.12), 180, 360, fill=hat + (255,), outline=INK)
    else: d.pieslice((hx - s * 0.34, hy - s * 0.45, hx + s * 0.34, hy + s * 0.1), 180, 360, fill=(54, 46, 44, 255), outline=INK)
def _roof(d, cx, y, w, h, col=(120, 70, 50), tile=(150, 92, 66)):
    """Mái ngói cong hai đầu cong lên."""
    _poly(d, [(cx - w, y), (cx - w * 1.08, y - h * 0.25), (cx - w * 0.5, y - h * 0.62), (cx, y - h), (cx + w * 0.5, y - h * 0.62), (cx + w * 1.08, y - h * 0.25), (cx + w, y)], col + (255,))
    for i in range(1, 5): _ln(d, [(cx - w * (1 - i * 0.2), y - h * 0.05), (cx - w * (0.8 - i * 0.2) * 0.9, y - h * (0.2 + i * 0.12))], tile + (255,), 2)
def _hall(d, cx, base, w, h, wall=(196, 170, 130), roof=(120, 70, 50), door=True, t=0.0, s=1.0):
    d.rectangle((cx - w * 0.8, base - h * 0.5, cx + w * 0.8, base), fill=wall + (255,), outline=INK)
    for i in range(5): _ln(d, [(cx - w * 0.8 + i * w * 0.4, base - h * 0.5), (cx - w * 0.8 + i * w * 0.4, base)], (150, 100, 66, 255), s * 0.2)
    if door: d.rectangle((cx - w * 0.16, base - h * 0.34, cx + w * 0.16, base), fill=(52, 34, 24, 255), outline=INK)
    _roof(d, cx, base - h * 0.5, w, h * 0.55, roof)
def _flag(d, px, py, s, t, col, ph=0.0, L=2.0, Hh=1.1):
    _ln(d, [(px, py + s * 0.2), (px, py - s * 3.6)], (86, 58, 34, 255), s * 0.16)
    top = py - s * 3.5; n = 8
    def w(u, v): return (px + u * L * s, top + v * Hh * s + math.sin(t * 5 + ph + u * 4.0) * s * 0.16 * u)
    up = [w(i / n, 0) for i in range(n + 1)]; dn = [w(i / n, 1.0) for i in range(n + 1)][::-1]
    d.polygon(up + dn, fill=col + (255,), outline=INK)
def _lamp(d, x, y, s, t):
    d.polygon([(x - s * 0.35, y), (x + s * 0.35, y), (x + s * 0.2, y - s * 0.3), (x - s * 0.2, y - s * 0.3)], fill=(150, 100, 70, 255), outline=INK)
    f = 1 + math.sin(t * 13) * 0.12; _poly(d, [(x - s * 0.1, y - s * 0.3), (x, y - s * 0.3 - s * 0.5 * f), (x + s * 0.1, y - s * 0.3)], (252, 190, 60, 255))
def _title(d, x, y, s, txt, u):
    return  # phụ đề đã nói đúng câu ấy; không đặt thêm chữ trong tiểu cảnh
    f = font(int(max(10, s * 0.62))); bb = d.textbbox((0, 0), txt, font=f); w = bb[2] - bb[0]
    d.rounded_rectangle((x - w / 2 - s * 0.35, y - s * 0.1, x + w / 2 + s * 0.35, y + (bb[3] - bb[1]) + s * 0.5), radius=int(s * 0.3), fill=(30, 22, 16, 205))
    d.text((x - w / 2, y + s * 0.12), txt, font=f, fill=(250, 244, 226, 255))

def canh_chua(d, x, y, s, u, t, arg):
    """Cậu bé được mẹ đưa đến nhà thiền sư: chùa mái cong, cây, thiền sư dắt cậu bé vào cổng, người mẹ đứng nhìn."""
    s, x0, y0, x1, y1, hor = _frame(d, x, y, s, u)
    _hills(d, x, hor, s); _ground(d, x0, hor, x1, y1, (150, 176, 104), s)
    d.rectangle((x0 + s * 0.12, hor, x1 - s * 0.12, hor + s * 0.4), fill=(124, 156, 90, 255))
    _e(d, x + s * 6.7, y0 + s * 1.9, s * 0.9, s * 0.9, (255, 236, 160, 255), (255, 236, 160, 255))
    for k in range(3): _bird(d, x - s * 6 + ((t * 0.5 + k * 0.3) % 1) * s * 12, y0 + s * (1.2 + 0.6 * k), s, t, k)
    base = y + s * 2.2
    # chùa
    _hall(d, x + s * 3.8, base, s * 3.2, s * 4.8, (212, 188, 140), (118, 66, 48), True, t, s)
    d.rectangle((x + s * 3.4, base - s * 1.0, x + s * 4.2, base), fill=(52, 34, 24, 255), outline=INK)
    # cây bồ đề
    _ln(d, [(x - s * 1.2, base), (x - s * 1.25, base - s * 3.0)], (96, 66, 44, 255), s * 0.42)
    for dx, dy, r in ((-1.2, 3.8, 1.5), (-2.2, 3.1, 1.1), (-0.2, 3.2, 1.1), (-1.2, 4.7, 1.0)):
        _e(d, x + dx * s + math.sin(t * 1.5 + dx) * s * 0.06, base - dy * s, r * s, r * s * 0.85, (96, 150, 78, 255))
    for k in range(5):
        a = (t * 0.35 + k * 0.2) % 1.0; _e(d, x - s * (0.4 + k * 0.5) + math.sin(a * 9) * s * 0.3, base - s * 3.5 + a * s * 3.4, s * 0.1, s * 0.06, (150, 190, 90, 255), (110, 150, 70, 255), 1)
    # cậu bé và thiền sư tiến vào cổng, mẹ đứng lại
    p = min(1.0, u * 1.6); wk = t * 4.5
    _man(d, x - s * 6.6, base, s * 1.15, (140, 74, 90), None, False, False, 1, 0.0)
    xs = x - s * 3.2 + p * s * 3.8
    _man(d, xs, base, s * 1.25, (214, 160, 56), None, True, False, 1, wk, 0.0, 'front', False)
    _man(d, xs + s * 0.95, base, s * 1.25, (112, 150, 190), None, False, True, 1, wk + 1.0)
    _ln(d, [(xs + s * 0.35, base - s * 1.1), (xs + s * 0.75, base - s * 0.9)], SKIN, s * 0.14)
    _title(d, x, y0 + s * 0.15, s, 'Năm ba tuổi, được đưa đến nhà thiền sư', u)
    _edge(d, x0, y0, x1, y1, s)

def canh_ngoa_trieu(d, x, y, s, u, t, arg):
    """Vua nằm nghe việc nước: giường thấp, gối, đèn dầu đất nung nhấp nháy, quan quỳ tâu, hai quan đứng hầu."""
    s, x0, y0, x1, y1, hor = _frame(d, x, y, s, u, ((92, 70, 70), (180, 140, 100)))
    d.rectangle((x0 + s * 0.12, y0 + s * 0.12, x1 - s * 0.12, y1 - s * 0.06), fill=(150, 112, 80, 255))
    for i in range(6): _ln(d, [(x0 + s * (1.6 + i * 3.6), y0 + s * 0.2), (x0 + s * (1.6 + i * 3.6), y1 - s * 0.1)], (110, 74, 50, 255), s * 0.34)
    d.rectangle((x0 + s * 0.12, y + s * 1.3, x1 - s * 0.12, y1 - s * 0.06), fill=(190, 150, 108, 255))
    for i in range(7): _ln(d, [(x0 + s * 0.2, y + s * (1.6 + i * 0.55)), (x1 - s * 0.2, y + s * (1.6 + i * 0.55))], (160, 120, 84, 255), s * 0.05)
    for sg in (-1, 1): d.polygon([(x + sg * s * 2.2, y0 + s * 0.12), (x + sg * s * 6.6, y0 + s * 0.12), (x + sg * s * 6.0, y + s * 1.2), (x + sg * s * 2.8, y + s * 1.2)], fill=(150, 40, 40, 255), outline=INK)
    base = y + s * 2.9
    # giường thấp có mái che nhỏ
    d.rounded_rectangle((x - s * 4.4, base - s * 1.05, x + s * 4.4, base - s * 0.3), radius=int(s * 0.2), fill=(168, 54, 44, 255), outline=INK)
    d.rectangle((x - s * 4.2, base - s * 0.3, x + s * 4.2, base + s * 0.2), fill=(110, 70, 44, 255), outline=INK)
    for sx in (-4.0, 4.0): d.rectangle((x + sx * s - s * 0.12, base + s * 0.2, x + sx * s + s * 0.12, base + s * 0.8), fill=(90, 60, 40, 255))
    # vua nằm nghiêng, đầu gối cao
    d.rounded_rectangle((x - s * 4.0, base - s * 1.65, x - s * 2.5, base - s * 1.0), radius=int(s * 0.3), fill=(236, 214, 150, 255), outline=INK)
    _e(d, x - s * 2.9, base - s * 1.75, s * 0.42, s * 0.46, SKIN)
    d.pieslice((x - s * 3.3, base - s * 2.25, x - s * 2.5, base - s * 1.6), 180, 360, fill=(30, 30, 40, 255), outline=INK)
    d.rounded_rectangle((x - s * 2.6, base - s * 1.55, x + s * 3.3, base - s * 0.85), radius=int(s * 0.3), fill=(224, 176, 52, 255), outline=INK)
    br = math.sin(t * 1.6) * s * 0.04; _ln(d, [(x - s * 1.0, base - s * 1.55 + br), (x + s * 0.4, base - s * 1.62 + br)], (190, 140, 40, 255), s * 0.1)
    # quan quỳ tâu và quan đứng hầu
    _man(d, x + s * 5.9, base + s * 0.9, s * 1.05, (60, 80, 140), (40, 40, 52), False, False, -1, 0.0, 0.5 + 0.1 * math.sin(t * 2), 'front')
    _man(d, x - s * 6.2, base + s * 0.9, s * 1.1, (80, 110, 70), (40, 40, 52), False, False, 1, 0.0, 0.0, 'front')
    _man(d, x - s * 5.0, base + s * 1.1, s * 1.1, (150, 90, 60), (40, 40, 52), False, False, 1, 0.0, 0.0, 'front')
    _lamp(d, x + s * 7.6, base + s * 0.3, s * 1.3, t); _lamp(d, x - s * 7.6, base + s * 0.3, s * 1.3, t + 0.7)
    _title(d, x, y0 + s * 0.15, s, 'Lê Ngọa Triều: vua nằm nghe việc nước', u)
    _edge(d, x0, y0, x1, y1, s)

def canh_van_tue(d, x, y, s, u, t, arg):
    """Lễ tôn lên ngôi: sân điện, thềm bậc, ngai vàng, hai hàng quan cúi lạy rồi giơ tay hô vạn tuế, cờ phấp phới."""
    s, x0, y0, x1, y1, hor = _frame(d, x, y, s, u)
    d.rectangle((x0 + s * 0.12, hor - s * 0.6, x1 - s * 0.12, y1 - s * 0.06), fill=(206, 190, 154, 255))
    d.rectangle((x0 + s * 0.12, hor - s * 0.6, x1 - s * 0.12, hor), fill=(170, 150, 120, 255))
    for i in range(6): _ln(d, [(x0 + s * 0.2, hor + s * (0.6 + i * 0.8)), (x1 - s * 0.2, hor + s * (0.6 + i * 0.8))], (190, 172, 138, 255), s * 0.05)
    base = hor + s * 0.2
    _hall(d, x, base, s * 4.6, s * 3.2, (206, 178, 126), (118, 62, 44), False, t, s)
    # ba bậc thềm đỏ và ngai vàng
    for i in range(3): d.rectangle((x - s * (2.6 - i * 0.2), base + s * 0.22 * i + s * 0.05, x + s * (2.6 - i * 0.2), base + s * 0.22 * (i + 1) + s * 0.05), fill=(180 - i * 12, 60, 48, 255), outline=INK)
    d.rectangle((x - s * 0.7, base - s * 2.2, x + s * 0.7, base - s * 0.3), fill=(224, 176, 52, 255), outline=INK)
    d.rectangle((x - s * 0.9, base - s * 2.45, x + s * 0.9, base - s * 2.2), fill=(224, 176, 52, 255), outline=INK)
    _man(d, x, base - s * 0.1, s * 1.1, (224, 176, 52), (224, 176, 52), False, False, 1, 0.0, 0.0, 'front')
    cyc = (t * 0.45) % 1.0; down = 0.5 - 0.5 * math.cos(min(1.0, cyc * 2.0) * math.pi) if cyc < 0.5 else 1.0 - (cyc - 0.5) * 0.0
    up = cyc >= 0.5
    cols = [(60, 80, 140), (150, 70, 70), (70, 120, 90), (130, 100, 60)]
    for row, (yy, sc) in enumerate(((y + s * 2.4, 1.0), (y + s * 3.3, 1.12), (y + s * 4.2, 1.22))):
        for i in range(5):
            for sg in (-1, 1):
                px = x + sg * (s * 2.2 + i * s * 1.15 * sc)
                _man(d, px, yy, s * 0.9 * sc, cols[(i + row) % 4], (40, 40, 52), False, False, 1, 0.0, 0.0 if up else down * 0.9, 'up' if up else None)
    _flag(d, x - s * 7.0, base + s * 0.3, s, t, (190, 52, 42), 0.0); _flag(d, x + s * 7.0, base + s * 0.3, s, t, (190, 52, 42), 1.5)
    if up:
        f = font(int(s * 0.82)); w = d.textbbox((0, 0), 'Vạn tuế!', font=f)
        d.text((x - (w[2] - w[0]) / 2, y0 + s * 0.2 - math.sin((cyc - 0.5) * 6.28) * s * 0.05), 'Vạn tuế!', font=f, fill=(255, 240, 190, 255), stroke_width=int(s * 0.07), stroke_fill=(120, 40, 30, 255))
    _title(d, x, y0 + s * 0.15, s, 'Cả triều tôn Lý Công Uẩn lên ngôi', u) if not up else None
    _edge(d, x0, y0, x1, y1, s)

def canh_ben_song(d, x, y, s, u, t, arg):
    """Đại La bên sông Hồng: tường thành, sông nước, thuyền buồm cập bến, người gánh hàng lên bến, ruộng bằng phẳng."""
    s, x0, y0, x1, y1, hor = _frame(d, x, y, s, u)
    _hills(d, x, hor - s * 0.2, s); _ground(d, x0, hor, x1, y1, (156, 182, 108), s)
    d.rectangle((x0 + s * 0.12, y + s * 1.2, x1 - s * 0.12, y1 - s * 0.06), fill=(86, 142, 190, 255))
    for i in range(6):
        pts = [(x0 + s * 0.3 + j * s * 0.6, y + s * (1.9 + i * 0.7) + math.sin(t * 2 + j * 0.8 + i) * s * 0.07) for j in range(34)]
        _ln(d, pts, (150, 196, 226, 255), s * 0.07)
    # thành
    d.rectangle((x - s * 8.2, hor - s * 1.3, x - s * 2.0, hor + s * 1.0), fill=(196, 176, 140, 255), outline=INK)
    for i in range(13): d.rectangle((x - s * 8.2 + i * s * 0.5, hor - s * 1.7, x - s * 8.2 + i * s * 0.5 + s * 0.3, hor - s * 1.3), fill=(196, 176, 140, 255), outline=INK)
    _hall(d, x - s * 5.0, hor - s * 1.3, s * 2.2, s * 2.6, (206, 178, 126), (118, 62, 44), True, t, s)
    _flag(d, x - s * 2.6, hor - s * 1.3, s * 0.9, t, (52, 142, 86))
    # đồng bằng bên phải
    for i in range(7):
        _ln(d, [(x + s * 2.5, hor + s * (0.2 + i * 0.28)), (x + s * 9.8, hor + s * (0.2 + i * 0.28))], (126, 156, 84, 255), s * 0.08)
    # thuyền buồm vào bến
    p = (u * 1.7) % 1.0
    for k, (bx0, by0, c) in enumerate(((x + s * 9.0, y + s * 3.4, (214, 190, 130)), (x + s * 10.5, y + s * 2.2, (200, 120, 90)))):
        bx = bx0 - p * s * 11.5 + (0 if k == 0 else -s * 2.5); by = by0 + math.sin(t * 2 + k) * s * 0.08
        if bx < x0 + s * 1.5: continue
        _poly(d, [(bx - s * 1.5, by), (bx + s * 1.5, by), (bx + s * 1.1, by + s * 0.65), (bx - s * 1.1, by + s * 0.65)], (130, 84, 52, 255))
        _ln(d, [(bx, by), (bx, by - s * 2.6)], (86, 58, 34, 255), s * 0.14)
        _poly(d, [(bx + s * 0.08, by - s * 2.5), (bx + s * 1.3, by - s * 0.5), (bx + s * 0.08, by - s * 0.5)], c + (255,))
    # người gánh hàng trên bờ
    for k in range(3):
        px = x - s * 1.0 + ((t * 0.25 + k * 0.33) % 1.0) * s * 7.5; py = hor + s * (1.2 + 0.1 * k)
        _man(d, px, py, s * 0.9, [(150, 100, 70), (90, 120, 90), (120, 110, 150)][k], (214, 184, 112), False, False, 1, t * 5 + k)
        _ln(d, [(px - s * 0.8, py - s * 1.5), (px + s * 0.8, py - s * 1.6)], (110, 80, 50, 255), s * 0.1)
    _title(d, x, y0 + s * 0.15, s, 'Đại La: sông chảy bên thành, đất rộng và bằng phẳng', u)
    _edge(d, x0, y0, x1, y1, s)

def canh_thang_long(d, x, y, s, u, t, arg):
    """Mặt bằng kinh thành nhìn từ trên cao: tường thành chữ nhật, bốn cửa sáng lên lần lượt kèm tên, điện ở giữa."""
    y = y + s * 2.9
    s, x0, y0, x1, y1, hor = _frame(d, x, y, s, u, ((150, 164, 140), (150, 164, 140)))
    d.rectangle((x0 + s * 0.12, y0 + s * 0.12, x1 - s * 0.12, y1 - s * 0.06), fill=(150, 176, 112, 255))
    cx, cy = x, y + s * 0.5; w, h = s * 5.6, s * 3.3
    d.rectangle((cx - w - s * 0.5, cy - h - s * 0.5, cx + w + s * 0.5, cy + h + s * 0.5), fill=(86, 142, 190, 255), outline=INK)  # hào
    d.rectangle((cx - w, cy - h, cx + w, cy + h), fill=(214, 198, 160, 255), outline=INK, width=_lw(s, 0.2))
    d.rectangle((cx - w * 0.7, cy - h * 0.62, cx + w * 0.7, cy + h * 0.62), outline=(176, 150, 110, 255), width=_lw(s, 0.1))
    _roof(d, cx, cy + s * 0.2, s * 2.2, s * 1.9, (118, 62, 44)); d.rectangle((cx - s * 1.8, cy + s * 0.2, cx + s * 1.8, cy + s * 0.9), fill=(206, 178, 126, 255), outline=INK)
    for dx in (-3.6, 3.6): _roof(d, cx + dx * s, cy + s * 0.6, s * 0.95, s * 1.1, (140, 82, 56)); d.rectangle((cx + dx * s - s * 0.8, cy + s * 0.6, cx + dx * s + s * 0.8, cy + s * 1.0), fill=(206, 178, 126, 255), outline=INK)
    for dx in (-1.3, 1.3): _roof(d, cx + dx * s, cy + s * 2.2, s * 0.8, s * 0.9, (140, 82, 56)); d.rectangle((cx + dx * s - s * 0.7, cy + s * 2.2, cx + dx * s + s * 0.7, cy + s * 2.5), fill=(206, 178, 126, 255), outline=INK)
    gates = (('Tường Phù', 'phía đông', cx + w, cy, 1, 0), ('Diệu Đức', 'phía bắc', cx, cy - h, 0, -1), ('Quảng Phúc', 'phía tây', cx - w, cy, -1, 0), ('Đại Hưng', 'phía nam', cx, cy + h, 0, 1))
    f = font(int(s * 0.58)); on = int(u * 5.2)
    for i, (nm, dr, gx, gy, ax, ay) in enumerate(gates):
        lit = on > i
        d.rectangle((gx - s * (0.4 if ay else 0.25), gy - s * (0.25 if ay else 0.4), gx + s * (0.4 if ay else 0.25), gy + s * (0.25 if ay else 0.4)), fill=(224, 176, 52, 255) if lit else (110, 80, 54, 255), outline=INK)
        if lit:
            r = s * (0.8 + 0.3 * math.sin(t * 4 + i)); d.ellipse((gx - r, gy - r, gx + r, gy + r), outline=(255, 214, 90, 150), width=_lw(s, 0.1))
            bb = d.textbbox((0, 0), nm, font=f); tw = bb[2] - bb[0]; tx = gx + ax * (s * 0.95 + (tw if ax > 0 else 0)) - (tw if ax < 0 else 0) - (tw / 2 if ay else 0) if not ay else gx - tw / 2
            ty = gy - s * 0.3 + ay * s * 0.9 - (s * 0.9 if ay < 0 else 0) if ay else gy - s * 0.25
            if ay < 0: ty = gy - s * 1.15
            if ay > 0: ty = gy + s * 0.7
            if ax > 0: tx = gx + s * 0.6 - tw * 0.0
            if ax < 0: tx = gx - s * 0.6 - tw
            d.rounded_rectangle((tx - s * 0.2, ty - s * 0.05, tx + tw + s * 0.2, ty + (bb[3] - bb[1]) + s * 0.25), radius=int(s * 0.15), fill=(30, 22, 16, 215))
            d.text((tx, ty), nm, font=f, fill=(250, 244, 226, 255))
    _edge(d, x0, y0, x1, y1, s)

def canh_khan(d, x, y, s, u, t, arg):
    """Bão ở vùng biển Biện Sơn: thuyền chòng chành, mây đen, sét; vua đốt hương khấn; cuối cảnh gió sấm lặng, trời sáng."""
    y = y - s * 1.8
    s, x0, y0, x1, y1, hor = _frame(d, x, y, s, u, ((46, 52, 78), (120, 128, 150)))
    calm = max(0.0, min(1.0, (u - 0.62) / 0.2)); dark = 1.0 - calm
    _sky(d, x0 + 2, y0 + 2, x1 - 2, hor + s * 0.5, (int(46 + 130 * calm), int(52 + 140 * calm), int(78 + 130 * calm)), (int(120 + 110 * calm), int(128 + 100 * calm), int(150 + 70 * calm)))
    for k in range(4):
        cxx = x - s * 6 + k * s * 4.2 + math.sin(t * 0.4 + k) * s * 0.3; _e(d, cxx, y0 + s * (1.4 + 0.2 * (k % 2)), s * (2.4 - calm), s * (0.9 - 0.3 * calm), (int(58 + 140 * calm), int(62 + 140 * calm), int(80 + 130 * calm)), (40, 44, 60), 0)
    if dark > 0.5 and (t * 1.7) % 2.6 < 0.28:
        sx = x + s * 1.5; pts = [(sx, y0 + s * 2.0)]
        for i in range(1, 6): pts.append((pts[-1][0] + (-1) ** i * s * 0.55, y0 + s * (2.0 + i * 0.75)))
        _ln(d, pts, (255, 246, 190, 255), s * 0.18)
    d.rectangle((x0 + 2, hor + s * 0.5, x1 - 2, y1 - 2), fill=(int(46 + 60 * calm), int(86 + 80 * calm), int(128 + 60 * calm)))
    for i in range(7):
        amp = s * (0.5 * dark + 0.1); pts = [(x0 + s * 0.2 + j * s * 0.55, hor + s * (0.9 + i * 0.62) + math.sin(t * 3.0 + j * 0.7 + i) * amp) for j in range(38)]
        _ln(d, pts, (190, 214, 236, 255), s * 0.09)
    rock = math.sin(t * 2.4) * 0.12 * dark; bx = x; by = y + s * 2.2 + math.sin(t * 2.4) * s * 0.3 * dark
    cs, sn = math.cos(rock), math.sin(rock)
    def R(px, py): return (bx + (px * cs - py * sn) * s, by + (px * sn + py * cs) * s)
    d.polygon([R(-3.6, 0), R(3.6, 0), R(2.7, 1.0), R(-2.7, 1.0)], fill=(130, 84, 52, 255), outline=INK)
    d.polygon([R(-1.8, -0.6), R(1.8, -0.6), R(1.8, 0), R(-1.8, 0)], fill=(176, 120, 76, 255), outline=INK)
    _ln(d, [R(0, 0), R(0, -3.4)], (86, 58, 34, 255), s * 0.16); d.polygon([R(0.1, -3.3), R(2.2, -0.9), R(0.1, -0.9)], fill=(222, 206, 160, 255), outline=INK)
    mx, my = R(-0.6, -0.1); _man(d, mx, my, s * 1.0, (224, 176, 52), (224, 176, 52), False, False, 1, 0.0, 0.0, 'up')
    ax, ay = R(-0.1, -2.1)
    if dark > 0.1:
        _ln(d, [(ax, ay), (ax, ay - s * 0.7)], (120, 80, 50, 255), s * 0.08)
        for k in range(5):
            a = (t * 0.8 + k * 0.2) % 1.0; _e(d, ax + math.sin(a * 9 + k) * s * 0.3, ay - s * 0.8 - a * s * 1.6, s * (0.12 + 0.2 * a), s * (0.1 + 0.18 * a), (210, 210, 214, int(150 * (1 - a))), (210, 210, 214, 0), 0)
        _e(d, ax, ay - s * 0.72, s * 0.1, s * 0.1, (255, 130, 40, 255), (255, 130, 40, 255), 0)
    if dark > 0.1:
        for k in range(26):
            rx = x0 + s * 0.6 + ((k * 37 + t * 22) % 100) / 100 * (x1 - x0 - s * 1.2); ry = y0 + s * 0.5 + ((k * 53 + t * 38) % 100) / 100 * (y1 - y0 - s)
            _ln(d, [(rx, ry), (rx - s * 0.18, ry + s * 0.45)], (200, 218, 240, int(200 * dark)), s * 0.04)
    _title(d, x, y0 + s * 0.15, s, 'Biện Sơn: gió sấm, vua đốt hương khấn trời' if dark > 0.1 else 'Khấn xong, gió sấm đều lặng', u)
    _edge(d, x0, y0, x1, y1, s)

def canh_nhat_thuc(d, x, y, s, u, t, arg):
    """Nhật thực: trời ban ngày, mặt trăng trượt che mặt trời, trời tối dần, điện Long An bên dưới, chim bay về tổ, rồi sáng lại."""
    s, x0, y0, x1, y1, hor = _frame(d, x, y, s, u)
    cov = math.sin(max(0.0, min(1.0, (u - 0.1) / 0.8)) * math.pi); cov = cov ** 0.8
    k = 1.0 - 0.78 * cov
    _sky(d, x0 + 2, y0 + 2, x1 - 2, y1 - 2, (int(150 * k), int(190 * k), int(226 * k)), (int(236 * k), int(228 * k), int(200 * k)))
    sx, sy = x + s * 5.6, y0 + s * 2.3
    for r, a in ((2.2, 40), (1.8, 70), (1.5, 120)): _e(d, sx, sy, s * r, s * r, (255, 236, 160, int(a * (0.4 + 0.6 * cov))), (255, 236, 160, 0), 0)
    _e(d, sx, sy, s * 1.1, s * 1.1, (255, 240, 170, 255), (255, 240, 170, 255), 0)
    mx = sx + (1.0 - 2 * max(0.0, min(1.0, (u - 0.1) / 0.8))) * s * 2.6
    _e(d, mx, sy, s * 1.12, s * 1.12, (int(40 * k + 14), int(44 * k + 14), int(60 * k + 20)), (20, 20, 30), 0)
    if cov > 0.8: d.ellipse((sx - s * 1.6, sy - s * 1.6, sx + s * 1.6, sy + s * 1.6), outline=(255, 246, 200, 190), width=_lw(s, 0.08))
    _hills(d, x, hor, s, ((int(176 * k), int(200 * k), int(168 * k)), (int(160 * k), int(190 * k), int(160 * k)), (int(172 * k), int(198 * k), int(166 * k))))
    d.rectangle((x0 + s * 0.12, hor, x1 - s * 0.12, y1 - s * 0.06), fill=(int(156 * k), int(182 * k), int(108 * k), 255))
    base = hor + s * 1.6
    _hall(d, x - s * 2.0, base, s * 3.6, s * 5.2, (int(206 * k), int(178 * k), int(126 * k)), (int(118 * k), int(62 * k), int(44 * k)), True, t, s)
    for sx2, c in ((x + s * 3.6, (190, 52, 42)), (x + s * 7.0, (190, 52, 42))): _flag(d, sx2, base, s * 0.9, t, tuple(int(v * k) for v in c))
    for i in range(5): _man(d, x + s * (3.0 + i * 1.2), base + s * 1.6, s * 0.8, [(60, 80, 140), (150, 70, 70), (70, 120, 90)][i % 3], (40, 40, 52), False, False, 1, 0.0, 0.0, 'up' if cov > 0.4 else None)
    for j in range(3):
        a = (u * 1.2 + j * 0.18) % 1.0; bx = x - s * 8 + a * s * 9; by = y0 + s * (4.4 - 2.0 * min(1.0, a * 1.2) * cov)
        if cov > 0.35: _bird(d, bx, by, s, t, j)
    _title(d, x, y0 + s * 0.15, s, 'Ngày 29 tháng 3: nhật thực giữa ban ngày', u)
    _edge(d, x0, y0, x1, y1, s)

def canh_cua_tay(d, x, y, s, u, t, arg):
    """Cửa Quảng Phúc: cổng thành lớn đóng chặt; lính canh trong cung xông ra, tướng chạy tới; quân mai phục lùi dần, cờ phấp phới. Không có máu."""
    s, x0, y0, x1, y1, hor = _frame(d, x, y, s, u, ((140, 150, 170), (214, 200, 170)))
    d.rectangle((x0 + s * 0.12, hor + s * 0.2, x1 - s * 0.12, y1 - s * 0.06), fill=(196, 176, 140, 255))
    for i in range(5): _ln(d, [(x0 + s * 0.2, hor + s * (0.9 + i * 0.9)), (x1 - s * 0.2, hor + s * (0.9 + i * 0.9))], (176, 156, 122, 255), s * 0.05)
    # tường thành và cổng
    d.rectangle((x0 + s * 0.12, hor - s * 2.4, x1 - s * 0.12, hor + s * 0.2), fill=(186, 164, 128, 255), outline=INK)
    for i in range(21): d.rectangle((x0 + s * 0.3 + i * s * 1.0, hor - s * 2.9, x0 + s * 0.3 + i * s * 1.0 + s * 0.6, hor - s * 2.4), fill=(186, 164, 128, 255), outline=INK)
    gw = s * 2.4; opn = max(0.0, min(1.0, (u - 0.28) / 0.25))
    d.rectangle((x - gw, hor - s * 2.1, x + gw, hor + s * 0.2), fill=(52, 34, 24, 255), outline=INK)
    for sg in (-1, 1): d.polygon([(x + sg * gw, hor - s * 2.1), (x + sg * (gw - gw * 0.9 * opn), hor - s * 2.1 + s * 0.2 * opn), (x + sg * (gw - gw * 0.9 * opn), hor + s * 0.2 - s * 0.1 * opn), (x + sg * gw, hor + s * 0.2)], fill=(130, 84, 50, 255), outline=INK)
    _roof(d, x, hor - s * 2.1, gw * 1.5, s * 1.6, (118, 62, 44))
    _flag(d, x - s * 7.5, hor - s * 2.4, s * 1.1, t, (52, 142, 86)); _flag(d, x + s * 7.5, hor - s * 2.4, s * 1.1, t, (196, 110, 40), 1.5)
    base = hor + s * 2.6
    # quân trong cung (xanh) xông ra, quân mai phục (cam) lùi sang phải
    for i in range(6):
        px = x - s * 0.6 + (u * 1.5 - i * 0.07) * s * 4.6 * min(1.0, max(0.0, opn * 2)); py = base + s * ((i % 3) * 0.55 - 0.3)
        if opn > 0.02: _man(d, px, py, s * 0.9, (52, 142, 86), (70, 70, 78), False, False, 1, t * 6 + i, 0.0, 'front')
    for i in range(6):
        px = x + s * (3.4 + (i % 3) * 1.3) + max(0.0, u - 0.4) * s * 6.0 + (i // 3) * s * 0.7; py = base + s * ((i % 3) * 0.55 - 0.3)
        if px < x1 - s * 0.8: _man(d, px, py, s * 0.9, (196, 110, 40), (70, 70, 78), False, False, -1, t * 6 + i)
    # tướng chạy tới cổng
    gx = x - s * 8.0 + min(1.0, u * 1.6) * s * 7.0
    _man(d, gx, base + s * 0.6, s * 1.15, (176, 50, 44), (60, 60, 70), False, False, 1, t * 7, 0.0, 'front')
    _title(d, x, y0 + s * 0.15, s, 'Cửa Quảng Phúc: lính canh xông ra, quân mai phục thua chạy', u)
    _edge(d, x0, y0, x1, y1, s)

SCENES = dict(canh_chua=canh_chua, canh_ngoa_trieu=canh_ngoa_trieu, canh_van_tue=canh_van_tue, canh_ben_song=canh_ben_song, canh_thang_long=canh_thang_long,
              canh_khan=canh_khan, canh_nhat_thuc=canh_nhat_thuc, canh_cua_tay=canh_cua_tay)
