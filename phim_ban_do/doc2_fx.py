"""Cảnh động vẽ bằng code (không bản đồ) cho thẻ minh họa video dọc. render(kind, t, seed) -> ảnh RGB 820x560."""
import math, random
from PIL import Image, ImageDraw
W, H = 820, 560
INK = (70, 40, 24)
def _sky(d, t, top=(255, 232, 178), bot=(252, 212, 150)):
    for y in range(H): k = y / H; d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3)))
def _sun(d, t, x=640, y=130, r=58):
    for i in range(14):
        a = i * math.pi / 7 + t * 0.4; d.line([(x + math.cos(a) * (r + 14), y + math.sin(a) * (r + 14)), (x + math.cos(a) * (r + 40 + 8 * math.sin(t * 3 + i)), y + math.sin(a) * (r + 40 + 8 * math.sin(t * 3 + i)))], fill=(255, 190, 90), width=6)
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 205, 96), outline=(214, 140, 50), width=5)
def _cloud(d, x, y, s=1.0):
    for dx, dy, r in ((0, 0, 34), (40, -14, 40), (84, 0, 32), (42, 12, 36)):
        d.ellipse((x + dx * s - r * s, y + dy * s - r * s, x + dx * s + r * s, y + dy * s + r * s), fill=(255, 250, 238))
def _hills(d, t, base=400):
    for k, (col, amp, ph, y0) in enumerate((((196, 170, 118), 40, 0.0, base - 40), ((164, 140, 92), 55, 1.7, base + 10))):
        pts = [(0, H)] + [(x, y0 - amp * (0.5 + 0.5 * math.sin(x / 130 + ph))) for x in range(0, W + 20, 20)] + [(W, H)]; d.polygon(pts, fill=col)
def _ground(d, y=470):
    d.rectangle((0, y, W, H), fill=(150, 112, 70)); d.rectangle((0, y, W, y + 10), fill=(112, 150, 70))
    for x in range(0, W, 46): d.line([(x, y + 28), (x + 24, y + 28)], fill=(126, 92, 56), width=4)
def _flag(d, x, y, h, col, t, w=70, ph=0.0):
    d.line([(x, y), (x, y - h)], fill=INK, width=6); pts = [(x, y - h)]
    for i in range(0, w + 1, 7): pts.append((x + i, y - h + 6 * math.sin(t * 6 + i / 12 + ph) + i * 0.0))
    pts += [(x + w, y - h + 46 + 5 * math.sin(t * 6 + w / 12 + ph)), (x, y - h + 46)]; d.polygon(pts, fill=col, outline=INK)
def _man(d, x, y, s, robe, t, ph=0.0, walk=True, hat=(60, 40, 30), spear=False, dirn=1):
    sw = math.sin(t * 9 + ph) if walk else 0; bob = abs(sw) * 4 * s if walk else 0; y = y - bob
    d.line([(x - 5 * s, y), (x - 5 * s + sw * 10 * s * dirn, y + 38 * s)], fill=INK, width=max(3, int(6 * s)))
    d.line([(x + 5 * s, y), (x + 5 * s - sw * 10 * s * dirn, y + 38 * s)], fill=INK, width=max(3, int(6 * s)))
    d.polygon([(x - 14 * s, y), (x + 14 * s, y), (x + 10 * s, y - 40 * s), (x - 10 * s, y - 40 * s)], fill=robe, outline=INK)
    d.ellipse((x - 10 * s, y - 62 * s, x + 10 * s, y - 40 * s), fill=(244, 206, 164), outline=INK, width=2)
    d.polygon([(x - 13 * s, y - 56 * s), (x + 13 * s, y - 56 * s), (x, y - 72 * s)], fill=hat, outline=INK)
    if spear:
        d.line([(x + 14 * s * dirn, y + 6 * s), (x + 20 * s * dirn, y - 96 * s)], fill=INK, width=max(3, int(5 * s))); d.polygon([(x + 20 * s * dirn - 5 * s, y - 94 * s), (x + 20 * s * dirn + 5 * s, y - 94 * s), (x + 20 * s * dirn, y - 116 * s)], fill=(210, 210, 214), outline=INK)
COLS = [(168, 58, 48), (62, 110, 150), (96, 140, 78), (176, 128, 52), (120, 78, 138), (60, 70, 96)]
def army(t, seed):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); _sky(d, t, (244, 214, 170), (252, 196, 140)); _hills(d, t, 330); _ground(d, 400)
    p = min(1.0, t / 3.5); p = 1 - (1 - p) ** 2; rnd = random.Random(seed)
    for row in range(3):
        for i in range(5):
            xl = -60 + (150 + i * 46 + row * 22) * p + 0 - 120 * (1 - p) * 0; xr = W + 60 - (150 + i * 46 + row * 22) * p
            yy = 410 + row * 32
            _man(d, xl, yy, 0.9 + row * 0.12, COLS[(i + row) % 3], t, i + row, spear=True, dirn=1)
            _man(d, xr, yy, 0.9 + row * 0.12, COLS[3 + (i + row) % 3], t, i * 2 + row, spear=True, dirn=-1)
    _flag(d, 70 + 50 * p, 300, 120, COLS[0], t); _flag(d, W - 120 - 50 * p, 300, 120, COLS[3], t, ph=2)
    for k in range(10):
        x = (rnd.random() * W + t * 120) % W; y = 520 - rnd.random() * 60; r = 8 + 10 * abs(math.sin(t * 2 + k)); d.ellipse((x - r, y - r / 2, x + r, y + r / 2), fill=(214, 190, 150))
    if p >= 0.95:
        f = (t - 3.3); 
        if 0 < f < 0.5: r = 150 * f / 0.5; d.ellipse((W / 2 - r, 430 - r, W / 2 + r, 430 + r), outline=(255, 244, 190), width=10)
    return im
def city(t, seed):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); _sky(d, t); _sun(d, t, 120, 120, 50); _cloud(d, (t * 20) % (W + 200) - 140, 90); _hills(d, t, 360)
    d.rectangle((0, 400, W, H), fill=(120, 164, 196))
    for i in range(7): y = 430 + i * 20; d.line([(0, y), (W, y)], fill=(160, 196, 220), width=3)
    wx0, wx1, wy = 130, 690, 300
    d.rectangle((wx0, wy, wx1, 440), fill=(186, 150, 104), outline=INK, width=4)
    for x in range(wx0, wx1, 40): d.rectangle((x + 5, wy - 22, x + 30, wy), fill=(186, 150, 104), outline=INK, width=3)
    d.rectangle((350, 330, 470, 440), fill=(70, 40, 30), outline=INK, width=4); d.pieslice((350, 290, 470, 370), 180, 360, fill=(70, 40, 30), outline=INK)
    d.polygon([(310, 300), (510, 300), (470, 240), (350, 240)], fill=(150, 62, 48), outline=INK); d.rectangle((360, 244, 460, 300), fill=(214, 172, 100), outline=INK, width=3)
    d.polygon([(330, 244), (490, 244), (410, 196)], fill=(150, 62, 48), outline=INK)
    _flag(d, 410, 200, 80, COLS[0], t); _flag(d, 160, 300, 70, COLS[1], t, ph=1); _flag(d, 660, 300, 70, COLS[2], t, ph=2)
    bx = (t * 70) % (W + 200) - 100; d.polygon([(bx, 470), (bx + 90, 470), (bx + 72, 492), (bx + 18, 492)], fill=(120, 78, 44), outline=INK); d.line([(bx + 45, 470), (bx + 45, 420)], fill=INK, width=4); d.polygon([(bx + 45, 424), (bx + 45, 466), (bx + 82, 466)], fill=(255, 246, 226), outline=INK)
    for i in range(5): _man(d, 190 + i * 100 + math.sin(t + i) * 6, 440, 0.55, COLS[i % 6], t, i, walk=False)
    return im
def road(t, seed):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); _sky(d, t, (214, 232, 214), (250, 232, 184)); _sun(d, t, 600, 120, 46); _cloud(d, (t * 16) % (W + 220) - 150, 80, 1.2)
    off = (t * 90) % 410
    for k, (col, y0, amp) in enumerate((((174, 190, 150), 330, 60), ((142, 164, 112), 380, 46))):
        sh = (t * (20 + 30 * k)) % 260; pts = [(0, H)] + [(x, y0 - amp * (0.5 + 0.5 * math.sin((x + sh) / 110 + k))) for x in range(0, W + 20, 20)] + [(W, H)]; d.polygon(pts, fill=col)
    d.rectangle((0, 430, W, H), fill=(196, 160, 104)); d.rectangle((0, 430, W, 440), fill=(130, 170, 80))
    for i in range(-1, 4): x = i * 205 - off % 205 + 0; d.line([(x, 520), (x + 80, 520)], fill=(166, 130, 84), width=8)
    for i in range(-1, 4):
        x = i * 300 - (t * 130) % 300; d.rectangle((x + 20, 360, x + 30, 440), fill=(102, 72, 44)); d.ellipse((x - 20, 290, x + 70, 370), fill=(98, 142, 76), outline=INK, width=3)
    _man(d, 330, 465, 1.5, COLS[0], t, 0, spear=False); _man(d, 470, 475, 1.4, COLS[1], t, 2)
    return im
def court(t, seed):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); d.rectangle((0, 0, W, H), fill=(226, 190, 140))
    for x in range(0, W, 120): d.rectangle((x + 10, 0, x + 46, 380), fill=(168, 62, 48), outline=INK, width=3)
    d.rectangle((0, 380, W, H), fill=(150, 108, 66)); d.rectangle((250, 380, 570, H), fill=(176, 40, 36))
    d.rectangle((330, 240, 490, 380), fill=(120, 76, 40), outline=INK, width=4); d.rectangle((310, 360, 510, 392), fill=(150, 98, 52), outline=INK, width=4)
    _man(d, 410, 360 + 6 * math.sin(t * 2), 1.5, (240, 188, 48), t, 0, walk=False, hat=(176, 40, 36))
    for k, sx in enumerate((-1, 1)):
        for i in range(4):
            bow = 0.5 + 0.5 * math.sin(t * 2.2 + i * 0.8 + k); _man(d, 410 + sx * (170 + i * 52), 470 + i * 8, 0.85, COLS[(i + k * 2) % 6], t, 0, walk=False, hat=(50, 36, 30))
    d.ellipse((380, 70, 440, 130), fill=(250, 220, 120), outline=INK, width=3)
    return im
def land(t, seed):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); _sky(d, t, (248, 226, 180), (252, 206, 150)); _sun(d, t, 640 + 20 * math.sin(t * 0.5), 150); _cloud(d, (t * 18) % (W + 240) - 160, 70); _cloud(d, (t * 11 + 400) % (W + 240) - 160, 160, 0.8); _hills(d, t, 380)
    d.rectangle((0, 450, W, H), fill=(128, 170, 202))
    for i in range(6): y = 470 + i * 16; xs = (t * 40 + i * 70) % 120; [d.line([(x - xs, y), (x - xs + 50, y)], fill=(170, 204, 226), width=3) for x in range(0, W + 120, 120)]
    return im
KIND = {'army': army, 'city': city, 'road': road, 'court': court, 'land': land}
def pick(text, n):
    s = ' ' + text.lower() + ' '
    for kind, keys in (('army', ('quân', 'đánh', 'chiến', 'giặc', 'tống', 'vây', 'binh', 'tấn công', 'đuổi', 'dẹp', 'giao tranh')), ('city', ('thành', 'kinh đô', 'dời đô', 'đóng đô', 'kinh sư', 'thăng long', 'hoa lư', 'đại la', 'cung điện', 'xây')), ('court', ('vua', 'ngôi', 'triều', 'quan', 'lên ngôi', 'thái tử', 'hoàng')), ('road', ('đi ', 'đường', 'về ', 'sông', 'thuyền', 'đến ', 'rời', 'vượt'))):
        if any(k in s for k in keys): return kind
    return 'land'
def render(kind, t):
    return KIND[kind](t, 7).convert('RGB')
