"""Dựng video dọc 'Tên đường' (1080x1920): python tenduong.py <tên> [out.mp4] [giây_bắt_đầu giây_kết_thúc | still giây...]
Đọc ke-hoach/thu-giong-hai/<tên>_full.json, giọng assets/thu_giong_hai/<tên>_chuan, ke-hoach/ten-duong/<tên>_meta.json (biển, mốc năm, ảnh từng câu)."""
import json, math, os, random, subprocess, sys
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFilter, ImageFont
ten = sys.argv[1]; R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
W, H, FPS = 1080, 1920, 24
FD = f'{R}/assets/fonts/tenduong'
F = {}
def font(name, s, var=None):
    k = (name, s, var)
    if k not in F:
        f = ImageFont.truetype(f'{FD}/{name}', s)
        if var:
            try: f.set_variation_by_axes([var])
            except Exception: pass
        F[k] = f
    return F[k]
BARLOW = lambda s: font('BarlowCondensed-SemiBold.ttf', s)
PLAY = lambda s, w=700: font('PlayfairDisplay[wght].ttf', s, w)
BVP = lambda s, b=True: font('BeVietnamPro-Bold.ttf' if b else 'BeVietnamPro-Medium.ttf', s)
BLUE, BLUE_D, WHITE, GOLD = (11, 78, 162), (7, 52, 112), (255, 255, 255), (255, 210, 74)
meta = json.load(open(f'{R}/ke-hoach/ten-duong/{ten}_meta.json', encoding='utf-8'))
beats = json.load(open(f'{R}/ke-hoach/thu-giong-hai/{ten}_full.json', encoding='utf-8'))
VD = f'{R}/assets/thu_giong_hai/{ten}_chuan'
dur = json.load(open(f'{VD}/thoi_luong.json'))
LEAD = 1.0; T = {}; D = {}; t = LEAD
for b in beats: T[b['n']] = t; D[b['n']] = dur[str(b['n'])]; t += D[b['n']]
TOTAL = t + 1.2
TEXT = {b['n']: b['text'] for b in beats}
ASRP = f'{R}/phim_ban_do/asr_{ten}.json'; ASR = json.load(open(ASRP)) if os.path.exists(ASRP) else {}
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x, s=1.6): x = max(0.0, min(1.0, x)); c = s + 1; return 1 + c * (x - 1) ** 3 + s * (x - 1) ** 2
# ---------- nền ----------
def _bg():
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H): k = y / H; d.line([(0, y), (W, y)], fill=(int(8 + 6 * k), int(20 + 22 * k), int(38 + 40 * k)))
    for x in range(0, W, 90): d.line([(x, 0), (x, H)], fill=(255, 255, 255, 0) if False else (20, 40, 70), width=1)
    for y in range(0, H, 90): d.line([(0, y), (W, y)], fill=(20, 40, 70), width=1)
    return im.convert('RGBA')
BG = _bg()
LOGO = Image.open(os.environ.get('LOGO', f'{R}/assets/logo/nguoi-gac-su.png')).convert('RGBA').resize((130, 130), Image.LANCZOS)
LOGO.putalpha(LOGO.split()[3].point(lambda v: int(v * 0.8)))
# ---------- biển tên đường ----------
def sign(p):
    name = meta['ten_duong'].upper(); sub = meta['danh_hieu']
    w, h = 800, 250; im = Image.new('RGBA', (w + 40, h + 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((16, 24, w + 20, h + 30), radius=26, fill=(0, 0, 0, 150)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d.rounded_rectangle((12, 12, w + 8, h + 8), radius=26, fill=BLUE, outline=WHITE, width=8); d.rounded_rectangle((28, 28, w - 8, h - 8), radius=16, outline=WHITE, width=3)
    f = BARLOW(124); tw = d.textbbox((0, 0), name, font=f)[2]
    if tw > w - 80: f = BARLOW(int(124 * (w - 80) / tw)); tw = d.textbbox((0, 0), name, font=f)[2]
    d.text((10 + w / 2 - tw / 2, 34), name, font=f, fill=WHITE)
    f2 = BVP(34, False); tw2 = d.textbbox((0, 0), sub, font=f2)[2]; d.text((10 + w / 2 - tw2 / 2, 176), sub, font=f2, fill=WHITE)
    s = back(p, 1.2); a = int(255 * min(1, p * 3))
    im2 = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    if a < 255: im2.putalpha(im2.split()[3].point(lambda v: int(v * a / 255)))
    return im2
# ---------- ảnh ----------
_IM = {}
def load(fn):
    if fn not in _IM:
        p = f'{R}/assets/ten_duong/{ten}/chon/{fn}'
        im = Image.open(p).convert('RGB') if os.path.exists(p) else None
        if im is None:
            im = Image.new('RGB', (1280, 960)); d = ImageDraw.Draw(im)
            for y in range(960): d.line([(0, y), (1280, y)], fill=(40 + y // 30, 60 + y // 25, 90 + y // 20))
        _IM[fn] = im
    return _IM[fn]
PW, PH = 960, 900
def photo(fn, u, mode):
    im = load(fn); s0 = max(PW / im.width, PH / im.height)
    z = 1.04 + 0.12 * u if mode != 'out' else 1.16 - 0.12 * u
    s = s0 * z; w, h = int(im.width * s), int(im.height * s); r = im.resize((w, h), Image.BILINEAR)
    px = {'trai': 0.35 + 0.3 * u, 'phai': 0.65 - 0.3 * u}.get(mode, 0.5); py = 0.5
    x0 = int((w - PW) * px); y0 = int((h - PH) * py); return r.crop((x0, y0, x0 + PW, y0 + PH))
def _banner(img, big, sub=None):
    im = img.copy().convert('RGBA'); d = ImageDraw.Draw(im); h = 190 if sub else 130
    ov = Image.new('RGBA', (PW, h), (6, 18, 36, 215)); im.alpha_composite(ov, (0, PH - h - 44))
    d = ImageDraw.Draw(im); f = PLAY(64); tw_ = d.textbbox((0, 0), big, font=f)[2]; d.text(((PW - tw_) / 2, PH - h - 44 + 14), big, font=f, fill=GOLD + (255,))
    if sub: f = BVP(34, False); tw_ = d.textbbox((0, 0), sub, font=f)[2]; d.text(((PW - tw_) / 2, PH - h - 44 + 106), sub, font=f, fill=WHITE + (255,))
    return im.convert('RGB')
def _portrait(fn, big, sub):
    im = load(fn).convert('RGB'); bg = im.resize((PW, PH), Image.BILINEAR).filter(ImageFilter.GaussianBlur(30)); bg = Image.blend(bg, Image.new('RGB', (PW, PH), (6, 18, 36)), 0.5)
    s = min(PW / im.width, (PH - 150) / im.height); r = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    bg.paste(r, ((PW - r.width) // 2, 20)); d = ImageDraw.Draw(bg)
    f = PLAY(54); w1 = d.textbbox((0, 0), big, font=f)[2]; d.text(((PW - w1) / 2, PH - 130), big, font=f, fill=GOLD)
    f = BVP(30, False); w2 = d.textbbox((0, 0), sub, font=f)[2]; d.text(((PW - w2) / 2, PH - 60), sub, font=f, fill=WHITE); return bg
def card_for(n, ts, u):
    import tdcards as C
    C.setfonts(BVP, BARLOW, PLAY)
    ph = lambda: (lambda m: photo(m['file'], u, m.get('mode', 'vao')))(meta['anh'][str(n)])
    if n == 19001: return ph(), meta['anh'][str(n)]
    if n == 19002: return _portrait(meta['anh'][str(n)]['file'], 'Ức Trai · sinh năm 1380', 'chân dung theo truyền thống'), {}
    if n == 19003: return C.card_map(ts, u, {'Chí Linh': (106.38, 21.13, 24, -70), 'Nhị Khê': (105.87, 20.80, -24, 10)}, ('Chí Linh', 'Nhị Khê'), 'Từ Chí Linh về Nhị Khê', (106.12, 20.96), 8.0), {}
    if n == 19004: return C.card_family(ts, u), {}
    if n == 19005: return C.card_year(ts, u, 1400, 'Đỗ Thái học sinh', '20 tuổi, học vị tương đương tiến sĩ'), {}
    if n == 19006: return C.card_text(ts, u, 'Ngự sử đài chánh chưởng', ['Chức quan giữ việc giám sát các quan khác']), {}
    if n == 19007: return C.card_timeline(ts, u), {}
    if n == 19008: return C.card_map(ts, u, {'Lam Sơn': (105.38, 19.93, 24, -20), 'Hà Nội': (105.85, 21.03, 24, -60)}, ('Hà Nội', 'Lam Sơn'), 'Nguyễn Trãi tìm đến Lê Lợi ở Lam Sơn', (105.6, 20.5), 6.0), {}
    if n == 19009: return _banner(ph(), '1428 · Bình Ngô đại cáo', 'tuyên bố nước ta độc lập'), meta['anh'][str(n)]
    if n == 19010: return C.card_books(ts, u), {}
    if n == 19011: return C.card_year(ts, u, 1442, 'Vụ án Lệ Chi Viên', 'vua Lê Thái Tông qua đột ngột'), {}
    if n == 19012: return C.card_text(ts, u, 'Bị kết tội', ['cả gia đình cũng bị liên lụy']), {}
    if n == 19013: return _banner(ph(), '1464 · được minh oan', 'vua Lê Thánh Tông khôi phục danh dự'), meta['anh'][str(n)]
    if n == 19014: return _banner(ph(), '1980 · UNESCO', 'Danh nhân văn hóa thế giới'), meta['anh'][str(n)]
    if n == 19016: return C.card_city(ts, u, 0), {}
    if n == 19017: return C.card_city(ts, u, 1), {}
    if n == 19015: return C.card_text(ts, u, 'Đường Nguyễn Trãi gần nhà bạn nằm ở đâu?', []), {}
    return ph(), meta['anh'][str(n)]
def frame_photo(t):
    if os.environ.get('TDC'):
        idx = [i for i, b in enumerate(beats) if T[b['n']] <= t]; idx = idx[-1] if idx else 0; n = beats[idx]['n']; ts = max(0.0, t - T[n])
        img, m = card_for(n, ts, ts / max(0.1, D[n]))
        if idx > 0 and ts < 0.35:
            pn = beats[idx - 1]['n']; old, _ = card_for(pn, D[pn], 1.0); img = Image.blend(old.convert('RGB'), img.convert('RGB'), ease(ts / 0.35))
        return img.convert('RGB'), m
    if os.environ.get('TD2D'):
        import doc2_fx2 as FX
        n = [b['n'] for b in beats if T[b['n']] <= t]; n = n[-1] if n else beats[0]['n']
        sp = FX.spec_for(n, TEXT); im = FX.render(sp, max(0.0, t - T[n])).convert('RGB').resize((PW, PH), Image.LANCZOS)
        return im, {'ghi_nguon': ''}
    cur = None
    for b in beats:
        if T[b['n']] <= t: cur = b
    cur = cur or beats[0]; n = cur['n']; m = meta['anh'].get(str(n)) or meta['anh'].get('mac_dinh')
    u = (t - T[n]) / max(0.1, D[n]); img = photo(m['file'], u, m.get('mode', 'vao'))
    # chuyển mờ 0.4 giây với ảnh trước nếu khác file
    idx = [b['n'] for b in beats].index(n)
    if idx > 0 and t - T[n] < 0.4:
        pm = meta['anh'].get(str(beats[idx - 1]['n'])) or meta['anh'].get('mac_dinh')
        if pm['file'] != m['file']:
            old = photo(pm['file'], 1.0, pm.get('mode', 'vao')); img = Image.blend(old, img, ease((t - T[n]) / 0.4))
    return img, m
def card(img, credit):
    c = Image.new('RGBA', (PW + 60, PH + 60), (0, 0, 0, 0)); sh = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((18, 26, PW + 44, PH + 50), fill=(0, 0, 0, 170)); c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(c); d.rectangle((14, 14, PW + 46, PH + 46), fill=WHITE); c.paste(img, (30, 30))
    if credit:
        f = BVP(22, False); tw = d.textbbox((0, 0), credit, font=f)[2]; x = 30 + PW - tw - 24
        ov = Image.new('RGBA', (tw + 20, 36), (0, 0, 0, 150)); c.alpha_composite(ov, (x - 10, 30 + PH - 44)); d.text((x, 30 + PH - 40), credit, font=f, fill=WHITE)
    return c
# ---------- mốc năm ----------
def timeline(t, cur_n):
    ms = meta['moc']; d_im = Image.new('RGBA', (W, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(d_im); x0, x1, y = 90, W - 90, 52
    d.line([(x0, y), (x1, y)], fill=(60, 90, 140, 255), width=8)
    reached = [m for m in ms if m['n'] <= cur_n]; last = reached[-1] if reached else None
    if last: d.line([(x0, y), (x0 + (x1 - x0) * (ms.index(last)) / (len(ms) - 1), y)], fill=GOLD + (255,), width=8)
    for i, m in enumerate(ms):
        x = x0 + (x1 - x0) * i / (len(ms) - 1); on = m['n'] <= cur_n; now = last is m
        r = (22 + 6 * math.sin(t * 5)) if now else (14 if on else 10)
        d.ellipse((x - r, y - r, x + r, y + r), fill=GOLD + (255,) if on else (60, 90, 140, 255), outline=WHITE + (255,) if on else None, width=3)
        f = BVP(30 if now else 26); tw = d.textbbox((0, 0), str(m['nam']), font=f)[2]
        d.text((x - tw / 2, y + 30), str(m['nam']), font=f, fill=WHITE + (255,) if on else (130, 160, 205, 255))
    return d_im
# ---------- phụ đề chạy chữ ----------
WORDS = {}
_D = {'một': 1, 'mốt': 1, 'hai': 2, 'ba': 3, 'bốn': 4, 'tư': 4, 'năm': 5, 'lăm': 5, 'sáu': 6, 'bảy': 7, 'tám': 8, 'chín': 9}
def _doc_nam(tk, i):
    """Đọc số năm dạng 'một nghìn ba trăm tám mươi' hoặc 'một trăm chín mươi hai' bắt đầu ở tk[i]; trả (giá trị, số chữ dùng) hoặc None."""
    import re as _re
    g = lambda j: _re.sub(r'[^\w]', '', tk[j].lower()) if j < len(tk) else ''
    k = i; v = 0
    if g(k) in _D and g(k + 1) == 'nghìn': v = _D[g(k)] * 1000; k += 2
    if g(k) in _D and g(k + 1) == 'trăm': v += _D[g(k)] * 100; k += 2
    elif v == 0: return None
    if g(k) in ('linh', 'lẻ') and g(k + 1) in _D: return v + _D[g(k + 1)], k + 2 - i
    if g(k) == 'mười':
        v += 10; k += 1
        if g(k) in ('lăm', 'một', 'hai', 'ba', 'bốn', 'sáu', 'bảy', 'tám', 'chín') and g(k) != 'năm': v += _D[g(k)]; k += 1
    elif g(k) in _D and g(k + 1) == 'mươi':
        v += _D[g(k)] * 10; k += 2
        if g(k) in _D and not (g(k) == 'năm' and g(k + 1) in ('tuổi', 'sau', 'trước')): v += _D[g(k)]; k += 1
    return v, k - i
def words(n):
    if n in WORDS: return WORDS[n]
    src = TEXT[n].split(); a = ASR.get(str(n), []); row = []
    for i, w in enumerate(src):
        if a: j = round(i * (len(a) - 1) / max(1, len(src) - 1)); s, e = a[j][1], a[j][2]
        else: s = 0.15 + (D[n] - 0.45) * i / len(src); e = 0.15 + (D[n] - 0.45) * (i + 1) / len(src)
        row.append((w, T[n] + s, T[n] + e))
    import re as _re
    out = []; i = 0
    while i < len(row):
        r = _doc_nam([x[0] for x in row], i + 1) if _re.sub(r'[^\w]', '', row[i][0].lower()) == 'năm' and i + 1 < len(row) else None
        if r:
            val, used = r; last = row[i + used][0]; tail = _re.search(r'[^\w]+$', last)
            out.append(row[i]); out.append((str(val) + (tail.group(0) if tail else ''), row[i + 1][1], row[i + used][2])); i += used + 1
        else: out.append(row[i]); i += 1
    WORDS[n] = out; return out
def subs(t, n):
    row = words(n); fnt = BVP(54); lay = Image.new('RGBA', (W, 380), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); x0, x1 = 70, W - 70; lines = []; line = []; wd = 0
    for w in row:
        ww = d.textbbox((0, 0), w[0] + ' ', font=fnt)[2]
        if wd + ww > x1 - x0 and line: lines.append(line); line = []; wd = 0
        line.append((w, ww)); wd += ww
    lines.append(line); idx = max(0, sum(1 for w in row if w[1] <= t) - 1); acc = 0; li = 0
    for i, ln in enumerate(lines):
        acc += len(ln)
        if idx < acc: li = i; break
    s = max(0, min(li - 1, len(lines) - 4)); vis = lines[s:s + 4]; hh = 76 * len(vis) + 30
    panel = Image.new('RGBA', (W - 80, hh), (6, 18, 36, 190)); lay.paste(panel, (40, 0), panel); y = 18
    for ln in vis:
        tw = sum(ww for _, ww in ln); x = (W - tw) / 2
        for (w, a, b), ww in ln:
            on = t >= a; now = a <= t <= b + 0.1
            col = GOLD + (255,) if now else (WHITE + (255,) if on else (150, 172, 205, 255)); d.text((x, y), w, font=fnt, fill=col); x += ww
        y += 76
    return lay
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lamp import lamp, CW, CH
def den(t, n):
    since = t - T[n]; talk = 0.0
    if 0.1 < since < D[n] - 0.25: talk = 0.5 + 0.5 * abs(math.sin(t * 9.0))
    fresh = 0 <= since < 0.6
    seg = int(t / 3.5); gk = (seg * 7 + n) % 5; larm = 1 if gk == 1 else (2 if gk == 3 else 0)
    ang = -0.95 + 0.08 * math.sin(t * 3.0) - (0.3 * math.sin(min(1, since / 0.35) * math.pi) if fresh else 0.0)
    L, _ = lamp(t, talk, 'happy', None if t < 1.6 else (ang, 300), 1.0 if t < 1.6 else 0.0, larm=larm, stride=1.0)
    hop = (50 * abs(math.sin(min(1, since / 0.6) * math.pi)) if fresh else 0.0) + 14 * talk * abs(math.sin(t * 7.0))
    sc = 0.46; L = L.resize((int(CW * sc), int(CH * sc)), Image.LANCZOS)
    return L, hop
def frame(t):
    f = BG.copy(); n = [b['n'] for b in beats if T[b['n']] <= t]; n = n[-1] if n else beats[0]['n']
    img, m = frame_photo(t); cred = m.get('ghi_nguon', '')
    c = card(img, cred); pop = ease(min(1, t / 0.8)); sc = 0.9 + 0.1 * pop
    c2 = c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS) if sc < 0.999 else c
    f.alpha_composite(c2, (int(W / 2 - c2.width / 2), int(370 + 480 - c2.height / 2) if False else int(405 + (c.height - c2.height) / 2)))
    sg = sign(min(1, t / 1.0)); f.alpha_composite(sg, (int(60 + (800 + 40 - sg.width) / 2), int(60 + (300 - sg.height) / 2)))
    f.alpha_composite(timeline(t, n), (0, 1385))
    f.alpha_composite(subs(t, n), (0, 1520))
    L, hop = den(t, n); f.alpha_composite(L, (-40, int(1330 - L.height - hop + 20)))
    f.alpha_composite(LOGO, (W - 44 - 130, 34))
    d = ImageDraw.Draw(f); d.rectangle((0, H - 14, W, H), fill=(6, 18, 36, 255)); d.rectangle((0, H - 14, int(W * t / TOTAL), H), fill=GOLD + (255,))
    if t < 0.3: f.alpha_composite(Image.new('RGBA', (W, H), (8, 20, 38, int(255 * (1 - t / 0.3)))))
    if t > TOTAL - 1.0: f.alpha_composite(Image.new('RGBA', (W, H), (8, 20, 38, int(255 * (t - (TOTAL - 1.0))))))
    return f.convert('RGB')
def _job(i): return frame(i / FPS).tobytes()
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'still':
        os.makedirs('/tmp/proto', exist_ok=True)
        for s in sys.argv[3:]: frame(float(s)).save(f'/tmp/proto/td_{s}.jpg', quality=90); print('ok', s)
        sys.exit(0)
    out = sys.argv[2] if len(sys.argv) > 2 else f'{R}/{ten}_video.mp4'
    f0 = int((float(sys.argv[3]) if len(sys.argv) > 4 else 0) * FPS); f1 = int((float(sys.argv[4]) if len(sys.argv) > 4 else TOTAL) * FPS)
    lst = f'{R}/{ten}_voice.txt'; open(lst, 'w').write(''.join(f"file '{VD}/{b['n']}.mp3'\n" for b in beats))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=mono', '-t', str(LEAD), '/tmp/_sil.wav'], check=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-ar', '44100', '-ac', '1', '/tmp/_voice.wav'], check=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', '/tmp/_sil.wav', '-i', '/tmp/_voice.wav', '-filter_complex', '[0][1]concat=n=2:v=0:a=1,apad=pad_dur=3[a]', '-map', '[a]', '-t', f'{TOTAL:.2f}', '/tmp/_audio.wav'], check=True)
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', '/tmp/_audio.wav',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', out], stdin=subprocess.PIPE)
    with Pool(int(os.environ.get('NPROC', 4))) as p:
        for b in p.imap(_job, range(f0, f1), chunksize=8): ff.stdin.write(b)
    ff.stdin.close(); ff.wait(); print('xong', out, round(TOTAL, 1), 'giây')
