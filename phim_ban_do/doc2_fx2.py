"""Cảnh động ghép từ nhiều mảnh (nền + đồ vật + nhân vật + thời tiết), mỗi câu kể một bố cục KHÁC nhau.
spec_for(n, text) -> spec (duy nhất toàn video); render(spec, t) -> ảnh RGB 820x560."""
import math, random
from PIL import Image, ImageDraw
from doc2_fx import W, H, INK, COLS, _flag, _man, _cloud, _sun
PAL = {  # trời trên, trời dưới, nền đất, đồi xa, đồi gần, nước
    'binh_minh': ((255, 214, 170), (252, 232, 190), (150, 118, 76), (214, 186, 150), (176, 150, 104), (150, 190, 214)),
    'trua': ((200, 228, 244), (252, 240, 206), (156, 120, 74), (176, 200, 160), (132, 168, 104), (120, 170, 206)),
    'hoang_hon': ((250, 160, 110), (254, 214, 150), (140, 100, 66), (200, 140, 110), (150, 100, 84), (200, 150, 140)),
    'dem': ((40, 48, 96), (96, 90, 130), (80, 66, 60), (66, 70, 110), (50, 58, 90), (60, 80, 130)),
    'u_am': ((170, 176, 184), (212, 212, 208), (130, 112, 90), (150, 160, 160), (116, 130, 124), (130, 150, 166)),
    'xuan': ((210, 236, 220), (254, 244, 210), (164, 130, 80), (170, 206, 150), (126, 176, 96), (130, 196, 210)),
}
BACK = ['doi', 'song', 'ruong', 'nui', 'bien', 'san', 'dien', 'pho', 'rung']
PIECES = ['chua', 'thap', 'thuyen', 'cau', 'lieu', 'trong', 'cong', 'nha', 'cay', 'co', 'lua', 'den', 'bia', 'xe', 'rom', 'trang']
FIGS = ['quan', 'quan_than', 'vua', 'su', 'dan', 'tre', 'nong', 'doan_di']
KEYS = [  # từ khóa -> (nền, đồ vật, nhân vật, thời tiết)
    (('chùa', 'sư ', 'thiền', 'nhà sư', 'vạn hạnh', 'lục tổ'), None, ['chua'], ['su'], None),
    (('thuyền', 'sông', 'bến', 'đường thủy', 'sông hồng', 'tô lịch', 'nước'), 'song', ['thuyen'], [], None),
    (('biển', 'cửa biển', 'bão', 'sóng'), 'bien', ['thuyen'], [], None),
    (('núi', 'đèo', 'rừng', 'đồi', 'sơn'), 'nui', [], [], None),
    (('ruộng', 'lúa', 'nông', 'cày', 'dân', 'thuế', 'mùa'), 'ruong', ['lua'], ['nong', 'dan'], None),
    (('đêm', 'mộng', 'ngủ', 'tối', 'trăng', 'khuya'), None, ['trang', 'den'], [], 'dem'),
    (('mưa', 'bão'), None, [], [], 'mua'),
    (('đánh', 'chiến', 'quân', 'giặc', 'tống', 'vây', 'binh', 'dẹp', 'tấn công', 'đuổi', 'giao tranh'), 'san', ['co', 'trong'], ['quan'], None),
    (('thành', 'kinh đô', 'dời đô', 'đóng đô', 'thăng long', 'hoa lư', 'đại la', 'cung', 'xây'), 'pho', ['cong', 'co'], ['dan'], None),
    (('vua', 'ngôi', 'triều', 'quan', 'lên ngôi', 'thái tử', 'hoàng', 'phong', 'vạn tuế'), 'dien', ['co'], ['vua', 'quan_than'], None),
    (('mất', 'băng hà', 'tang', 'chết', 'qua đời'), None, ['bia', 'den'], ['quan_than'], 'u_am'),
    (('đi ', 'về ', 'đường', 'rời', 'vượt', 'chạy'), 'doi', ['cay', 'xe'], ['doan_di'], None),
    (('con', 'cháu', 'mẹ', 'cha', 'nuôi', 'trẻ', 'sinh'), None, ['nha', 'cay'], ['tre', 'dan'], None),
    (('lửa', 'đốt', 'cháy'), None, ['den'], [], 'u_am'),
]
_ASSIGN = {}
COMPAT = {'dien': ['co', 'den', 'bia', 'trong', 'lieu'], 'song': ['thuyen', 'cau', 'co', 'den', 'cay', 'nha', 'thap', 'chua'], 'bien': ['thuyen', 'co', 'den', 'trang'],
          'ruong': ['lua', 'nha', 'cay', 'co', 'rom', 'xe', 'trang'], 'san': ['co', 'trong', 'lieu', 'den', 'bia', 'cong', 'thap', 'cay'],
          'pho': ['cong', 'nha', 'co', 'den', 'cay', 'xe', 'chua', 'thap', 'trong'], 'doi': ['cay', 'xe', 'nha', 'co', 'chua', 'thap', 'trang', 'rom', 'den', 'lieu'],
          'nui': ['cay', 'chua', 'thap', 'nha', 'co', 'lieu', 'den', 'trang'], 'rung': ['cay', 'lieu', 'den', 'xe', 'nha', 'bia', 'trang', 'co']}
ALT = {'dien': ['san', 'pho'], 'san': ['pho', 'doi', 'dien'], 'pho': ['san', 'doi', 'song'], 'song': ['doi', 'pho', 'ruong'], 'doi': ['nui', 'rung', 'ruong'], 'ruong': ['doi', 'rung'], 'nui': ['rung', 'doi'], 'bien': ['song'], 'rung': ['nui', 'doi']}
CAP = 15
def _features(text):
    s = ' ' + text.lower() + ' '; bk, pcs, fgs, wx = None, [], [], None
    for keys, b, p, f, w in KEYS:
        if any(k in s for k in keys):
            bk = bk or b; pcs += p; fgs += f; wx = wx or w
    return bk, pcs, fgs, wx
def assign_all(texts):
    if _ASSIGN: return
    used = set(); prev = []; pals = list(PAL); cnt = {}
    for n in sorted(texts):
        bk, pcs, fgs, wx = _features(texts[n])
        best = None
        for att in range(400):
            r = random.Random(n * 7919 + att)
            pal = wx if wx in PAL else r.choice([p for p in pals if not prev or p != prev[-1][1]])
            b = bk or r.choice([x for x in BACK if not any(x == q[0] for q in prev[-2:])] or BACK)
            if cnt.get(b, 0) >= CAP: b = min(ALT.get(b, BACK), key=lambda q: cnt.get(q, 0)) if att % 3 else r.choice(ALT.get(b, BACK))
            ok = COMPAT.get(b, PIECES)
            ps = [x for x in dict.fromkeys(pcs) if x in ok][:2]
            while len(ps) < 2 + (att % 2): ps.append(r.choice(ok))
            ps = list(dict.fromkeys(ps))
            fg = list(dict.fromkeys(fgs))[:2] or [r.choice(FIGS)]
            if r.random() < 0.4 and len(fg) < 2: fg.append(r.choice(FIGS))
            fg = list(dict.fromkeys(fg))
            key = (b, pal, tuple(sorted(ps)), tuple(sorted(fg)))
            sim = any(k[0] == b and k[1] == pal and len(set(k[2]) & set(ps)) >= 2 for k in used)
            if key not in used and not sim: best = (key, r.randint(0, 10 ** 6)); break
        if best is None: best = ((b, pal, tuple(sorted(ps)), tuple(sorted(fg))), r.randint(0, 10 ** 6))
        used.add(best[0]); prev.append(best[0]); cnt[best[0][0]] = cnt.get(best[0][0], 0) + 1
        _ASSIGN[n] = dict(back=best[0][0], pal=best[0][1], pieces=list(best[0][2]), figs=list(best[0][3]), seed=best[1], rain=(wx == 'mua'))
def spec_for(n, texts):
    assign_all(texts); return _ASSIGN[n]
# ---------- nền ----------
def _grad(d, a, b):
    for y in range(H): k = y / H; d.line([(0, y), (W, y)], fill=tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3)))
def _hills(d, c, base, amp, ph, sh=0.0):
    pts = [(0, H)] + [(x, base - amp * (0.5 + 0.5 * math.sin((x + sh) / 130 + ph))) for x in range(0, W + 20, 20)] + [(W, H)]; d.polygon(pts, fill=c)
def back(d, spec, t, P, rnd):
    top, bot, gr, h1, h2, wt = P; k = spec['back']; gy = 440
    _grad(d, top, bot)
    if k == 'doi': _hills(d, h1, 360, 60, rnd.random() * 6, t * 6); _hills(d, h2, 410, 50, rnd.random() * 6, t * 12); d.rectangle((0, gy, W, H), fill=gr)
    elif k == 'song':
        _hills(d, h1, 330, 50, rnd.random() * 6); d.rectangle((0, 380, W, H), fill=wt)
        for i in range(8): y = 400 + i * 20; xs = (t * 30 + i * 53) % 90; [d.line([(x - xs, y), (x - xs + 40, y)], fill=tuple(min(255, c + 36) for c in wt), width=3) for x in range(0, W + 90, 90)]
        d.rectangle((0, 380, W, 392), fill=gr); d.rectangle((0, 462, W, H), fill=gr); d.rectangle((0, 462, W, 472), fill=(112, 150, 70))
    elif k == 'ruong':
        _hills(d, h1, 300, 40, rnd.random() * 6)
        for i in range(7):
            y = 330 + i * 32; d.polygon([(0, y), (W, y - 12), (W, y + 24), (0, y + 36)], fill=(110 + 14 * (i % 2), 170 - 10 * (i % 2), 82), outline=INK)
            for x in range(20, W, 46): hh = 8 + 3 * math.sin(t * 2 + x + i); d.line([(x, y + 16), (x, y + 16 - hh)], fill=(214, 200, 90), width=3)
    elif k == 'nui':
        rr = random.Random(spec['seed'])
        for j, c in enumerate((h1, h2)):
            pts = [(0, H)]; x = -40
            while x < W + 80: pts += [(x, 400 - 30 * j), (x + rr.randint(60, 120), 190 + j * 70 + rr.randint(0, 60))]; x += rr.randint(120, 200)
            pts += [(W, H)]; d.polygon(pts, fill=c)
        d.rectangle((0, gy, W, H), fill=gr)
    elif k == 'bien':
        d.rectangle((0, 330, W, H), fill=wt)
        for i in range(12): y = 345 + i * 18; xs = (t * 50 + i * 41) % 100; [d.arc((x - xs, y - 8, x - xs + 60, y + 8), 0, 180, fill=tuple(min(255, c + 40) for c in wt), width=3) for x in range(0, W + 100, 100)]
    elif k == 'san':
        d.rectangle((0, 120, W, 300), fill=(176, 120, 84)); d.rectangle((0, 300, W, H), fill=(196, 170, 132))
        for x in range(0, W, 41): d.line([(x, 300), (x - 60, H)], fill=(170, 144, 106), width=2)
        for x in range(30, W, 140): d.rectangle((x, 130, x + 14, 300), fill=(150, 56, 44), outline=INK, width=2)
    elif k == 'dien':
        wall = [(228, 192, 142), (214, 176, 150), (236, 210, 160), (196, 170, 140)][spec['seed'] % 4]; col = [(168, 62, 48), (110, 74, 44), (186, 140, 50), (70, 96, 120)][(spec['seed'] // 4) % 4]
        carpet = [(176, 40, 36), (60, 80, 120), (96, 120, 60), (140, 60, 100)][(spec['seed'] // 16) % 4]; sp = [90, 120, 150, 200][(spec['seed'] // 64) % 4]
        d.rectangle((0, 0, W, H), fill=wall)
        for x in range(10, W, sp): d.rectangle((x, 0, x + 34, 380), fill=col, outline=INK, width=3)
        if spec['seed'] % 3 == 0:
            for x in range(60, W, 240): d.rectangle((x, 90, x + 90, 200), fill=(246, 230, 190), outline=INK, width=3); d.line([(x + 45, 90), (x + 45, 200)], fill=INK, width=2); d.line([(x, 145), (x + 90, 145)], fill=INK, width=2)
        d.rectangle((0, 380, W, H), fill=(150, 108, 66)); d.rectangle((250, 380, 570, H), fill=carpet)
    elif k == 'pho':
        _hills(d, h1, 340, 40, rnd.random() * 6); d.rectangle((0, 450, W, H), fill=gr)
        for i in range(9):
            x = i * 100 - 20; hh = 70 + (i * 37) % 40; d.rectangle((x, 440 - hh, x + 84, 440), fill=(196, 160, 112), outline=INK, width=3); d.polygon([(x - 8, 440 - hh), (x + 92, 440 - hh), (x + 70, 400 - hh), (x + 14, 400 - hh)], fill=(150, 62, 48 + (i % 3) * 14), outline=INK)
    elif k == 'rung':
        d.rectangle((0, 400, W, H), fill=gr)
        for i in range(10): x = i * 90 + (i * 31) % 40; hh = 220 + (i * 53) % 90; d.rectangle((x + 20, 440 - hh, x + 32, 440), fill=(98, 66, 40)); d.ellipse((x - 20, 330 - hh // 3, x + 70, 330 + hh // 3 - 60), fill=(80 + (i % 3) * 20, 130 + (i % 2) * 20, 70), outline=INK, width=2)
# ---------- đồ vật ----------
def piece(d, name, x, y, s, t, rnd, P):
    gr = P[2]
    if name == 'chua':
        d.rectangle((x - 70 * s, y - 70 * s, x + 70 * s, y), fill=(210, 176, 120), outline=INK, width=3); d.polygon([(x - 100 * s, y - 70 * s), (x + 100 * s, y - 70 * s), (x + 60 * s, y - 120 * s), (x - 60 * s, y - 120 * s)], fill=(150, 62, 48), outline=INK); d.rectangle((x - 18 * s, y - 50 * s, x + 18 * s, y), fill=(70, 40, 30))
    elif name == 'thap':
        for i in range(5): w = (50 - i * 7) * s; yy = y - i * 36 * s; d.rectangle((x - w, yy - 34 * s, x + w, yy), fill=(214, 184, 130), outline=INK, width=2); d.polygon([(x - w - 10 * s, yy - 34 * s), (x + w + 10 * s, yy - 34 * s), (x, yy - 52 * s)], fill=(150, 62, 48), outline=INK)
    elif name == 'thuyen':
        bx = x + 12 * math.sin(t * 1.2); by = y + 4 * math.sin(t * 2)
        d.polygon([(bx - 70 * s, by), (bx + 70 * s, by), (bx + 52 * s, by + 22 * s), (bx - 52 * s, by + 22 * s)], fill=(120, 78, 44), outline=INK); d.line([(bx, by), (bx, by - 90 * s)], fill=INK, width=4); d.polygon([(bx, by - 86 * s), (bx, by - 6 * s), (bx + 52 * s, by - 6 * s)], fill=(255, 246, 226), outline=INK)
    elif name == 'cau':
        d.rectangle((x - 110 * s, y - 24 * s, x + 110 * s, y - 10 * s), fill=(150, 108, 66), outline=INK, width=2)
        for i in range(-4, 5): d.rectangle((x + i * 24 * s - 4, y - 10 * s, x + i * 24 * s + 4, y + 20 * s), fill=(110, 76, 44))
    elif name == 'lieu':
        d.polygon([(x - 80 * s, y), (x + 80 * s, y), (x + 40 * s, y - 70 * s), (x - 40 * s, y - 70 * s)], fill=(168, 58, 48), outline=INK)
    elif name == 'trong':
        sh = 4 * math.sin(t * 14); d.ellipse((x - 44 * s, y - 70 * s + sh, x + 44 * s, y), fill=(160, 70, 52), outline=INK, width=3); d.line([(x - 40 * s, y - 36 * s), (x + 40 * s, y - 36 * s)], fill=(250, 214, 120), width=4)
        d.line([(x + 60 * s, y - 100 * s), (x + 20 * s + sh, y - 60 * s)], fill=INK, width=5)
    elif name == 'cong':
        d.rectangle((x - 90 * s, y - 110 * s, x + 90 * s, y), fill=(190, 150, 100), outline=INK, width=3); d.pieslice((x - 46 * s, y - 130 * s, x + 46 * s, y - 30 * s), 180, 360, fill=(70, 40, 30)); d.rectangle((x - 46 * s, y - 80 * s, x + 46 * s, y), fill=(70, 40, 30)); d.polygon([(x - 110 * s, y - 110 * s), (x + 110 * s, y - 110 * s), (x + 70 * s, y - 160 * s), (x - 70 * s, y - 160 * s)], fill=(150, 62, 48), outline=INK)
    elif name == 'nha':
        d.rectangle((x - 50 * s, y - 50 * s, x + 50 * s, y), fill=(206, 170, 120), outline=INK, width=3); d.polygon([(x - 66 * s, y - 50 * s), (x + 66 * s, y - 50 * s), (x, y - 100 * s)], fill=(130, 100, 56), outline=INK); d.rectangle((x - 12 * s, y - 30 * s, x + 12 * s, y), fill=(70, 44, 30))
    elif name == 'cay':
        d.rectangle((x - 6 * s, y - 70 * s, x + 6 * s, y), fill=(98, 66, 40)); d.ellipse((x - 46 * s, y - 140 * s, x + 46 * s, y - 50 * s), fill=(96, 150, 78), outline=INK, width=3)
    elif name == 'co':
        _flag(d, x, y, 120 * s, COLS[int(rnd.random() * 6)], t, int(60 * s + 10), rnd.random() * 3)
    elif name == 'lua':
        for i in range(-3, 4): d.line([(x + i * 14 * s, y), (x + i * 14 * s + 8 * math.sin(t * 2 + i), y - 40 * s)], fill=(222, 190, 60), width=4)
    elif name == 'den':
        d.polygon([(x - 26 * s, y), (x + 26 * s, y), (x + 18 * s, y - 20 * s), (x - 18 * s, y - 20 * s)], fill=(140, 90, 56), outline=INK)
        f = 1 + 0.2 * math.sin(t * 12); d.polygon([(x, y - 62 * s * f), (x - 12 * s, y - 20 * s), (x + 12 * s, y - 20 * s)], fill=(255, 150, 50), outline=(190, 60, 20))
        for i in range(4): yy = y - 70 * s - ((t * 40 + i * 20) % 80) * s; d.ellipse((x - 8 + 5 * math.sin(yy / 10), yy, x + 8 + 5 * math.sin(yy / 10), yy + 14), fill=(224, 220, 214))
    elif name == 'bia':
        d.rectangle((x - 30 * s, y - 100 * s, x + 30 * s, y), fill=(170, 170, 176), outline=INK, width=3); d.pieslice((x - 30 * s, y - 126 * s, x + 30 * s, y - 74 * s), 180, 360, fill=(170, 170, 176), outline=INK)
    elif name == 'xe':
        d.rectangle((x - 50 * s, y - 40 * s, x + 50 * s, y - 14 * s), fill=(150, 108, 66), outline=INK, width=2); a = t * 5
        for sg in (-1, 1): cx = x + sg * 34 * s; d.ellipse((cx - 22 * s, y - 40 * s, cx + 22 * s, y + 4 * s), outline=INK, width=4); d.line([(cx, y - 18 * s), (cx + 20 * s * math.cos(a), y - 18 * s + 20 * s * math.sin(a))], fill=INK, width=3)
    elif name == 'rom':
        for i in range(3): d.polygon([(x + i * 56 * s - 30 * s, y), (x + i * 56 * s + 30 * s, y), (x + i * 56 * s, y - 56 * s)], fill=(226, 196, 100), outline=INK)
    elif name == 'trang':
        _sun(d, t, x, y - 170 * s, int(40 * s + 10)) if P[0][2] > 150 else (d.ellipse((x - 40 * s, y - 200 * s, x + 40 * s, y - 120 * s), fill=(250, 244, 214), outline=(214, 200, 150), width=4))
# ---------- nhân vật ----------
def figs(d, name, x, y, t, rnd):
    if name == 'quan':
        for r in range(2):
            for i in range(4): _man(d, x - 120 + i * 62 + r * 26 + 20 * math.sin(t * 1.5), y + r * 30, 0.9 + r * 0.1, COLS[(i + r) % 6], t, i + r, spear=True)
    elif name == 'quan_than':
        for i in range(4): _man(d, x - 130 + i * 86, y + (i % 2) * 14, 0.85, COLS[(i + 1) % 6], t, 0, walk=False, hat=(50, 36, 30))
    elif name == 'vua':
        _man(d, x, y + 6 * math.sin(t * 2), 1.4, (240, 188, 48), t, 0, walk=False, hat=(176, 40, 36))
    elif name == 'su':
        _man(d, x, y, 1.2, (214, 150, 56), t, 1, walk=False, hat=(214, 150, 56))
    elif name == 'dan':
        for i in range(3): _man(d, x - 80 + i * 80, y + 8 * (i % 2), 0.9, COLS[(i + 2) % 6], t, i, hat=(214, 190, 110))
    elif name == 'tre':
        _man(d, x, y, 0.65, COLS[3], t, 2); _man(d, x + 54, y + 4, 0.6, COLS[1], t, 4)
    elif name == 'nong':
        _man(d, x, y, 1.0, (130, 100, 70), t, 0, walk=False, hat=(214, 190, 110)); d.line([(x + 18, y - 20 + 8 * math.sin(t * 4)), (x + 50, y + 20)], fill=INK, width=5)
    elif name == 'doan_di':
        for i in range(4): _man(d, (x - 150 + i * 90 + t * 40) % (W + 120) - 40, y + (i % 2) * 14, 0.9, COLS[i % 6], t, i)
def render(spec, t):
    rnd = random.Random(spec['seed']); P = PAL[spec['pal']]
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); back(d, spec, t, P, rnd)
    if spec['back'] in ('doi', 'song', 'ruong', 'nui', 'pho', 'rung', 'bien'):
        _cloud(d, (t * (12 + rnd.randint(0, 14)) + rnd.randint(0, 600)) % (W + 240) - 160, 70 + rnd.randint(0, 80), 0.8 + rnd.random() * 0.6)
    gy = {'dien': 470, 'san': 440, 'song': 410, 'bien': 400, 'ruong': 470}.get(spec['back'], 450)
    slots = [150, 410, 670]; rnd.shuffle(slots)
    for i, nm in enumerate(spec['pieces']): piece(d, nm, slots[i % 3] + rnd.randint(-50, 50), gy + rnd.randint(-6, 14), 0.8 + rnd.random() * 0.5, t, rnd, P)
    fx = [260, 560]; rnd.shuffle(fx)
    for i, nm in enumerate(spec['figs']): figs(d, nm, fx[i % 2], gy + 56 + rnd.randint(0, 18), t, rnd)
    if spec['rain']:
        for k in range(70): x = (k * 97 + t * 220) % W; y = (k * 53 + t * 700) % H; d.line([(x, y), (x - 8, y + 24)], fill=(214, 228, 240), width=2)
    return im
