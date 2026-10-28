"""Khung dọc 'thẻ ảnh + đèn cầm thước' cho video bản đồ. Gọi từ mapfilm3.frame khi DOC2=1: nhận khung bản đồ (không phụ đề), trả về khung hoàn chỉnh.
Cảnh nhỏ (canh_*) -> thẻ cảnh; chân dung nhân vật (CARDS3) -> thẻ chân dung; cảnh đánh nhau (QUIET/BATT) và các đoạn còn lại -> thẻ bản đồ (cắt từ khung bản đồ)."""
import math, os, json, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from lamp import lamp, CW, CH
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
W, H = 1080, 1920
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if not os.path.exists(FB): FB = os.environ.get('FONT', ROOT + '/assets/fonts/Lora-Variable.ttf')
FS = ROOT + '/assets/fonts/BeVietnamPro-BlackItalic.ttf'
_F = {}
def font(p, s):
    if (p, s) not in _F: _F[(p, s)] = ImageFont.truetype(p, s)
    return _F[(p, s)]
def back(x, s=1.7):
    x = max(0, min(1, x)); c = s + 1; return 1 + c * (x - 1) ** 3 + s * (x - 1) ** 2
clamp = lambda x: max(0.0, min(1.0, x))
# ---------- nền, bảng đỏ ----------
def _bg():
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H): d.line([(0, y), (W, y)], fill=(250 - int(14 * y / H), 238 - int(22 * y / H), 208 - int(34 * y / H)))
    rnd = random.Random(5)
    for _ in range(90):
        x, y, r = rnd.randint(0, W), rnd.randint(150, 1150), rnd.randint(6, 26); d.ellipse((x - r, y - r, x + r, y + r), fill=(236, 218, 184))
    for i in range(0, W + 120, 120): d.ellipse((i - 60, 120, i + 60, 240), outline=(232, 208, 168), width=5)
    return im.convert('RGBA')
BG = _bg()
def _panel():
    top = 1215; im = Image.new('RGBA', (W, H - top + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for y in range(H - top + 40): d.line([(0, y), (W, y)], fill=(186 - int(40 * y / (H - top)), 74 - int(18 * y / (H - top)), 56 - int(14 * y / (H - top)), 255))
    d.rectangle((0, 0, W, 14), fill=(255, 206, 110, 255))
    for x in range(0, W, 54): d.polygon([(x, 14), (x + 27, 40), (x + 54, 14)], fill=(255, 206, 110, 255))
    return im, top - 14
PANEL, PY = _panel()
_logo = Image.open(os.environ.get('LOGO', ROOT + '/assets/logo/nguoi-gac-su.png')).convert('RGBA').resize((120, 120), Image.LANCZOS)
# ---------- thẻ ----------
def card(img, tag=None, tilt=-1.6):
    ih = img.height; ch = ih + 100
    c = Image.new('RGBA', (880, ch + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    sh = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((26, 36, 866, ch + 16), radius=34, fill=(60, 30, 10, 120)); c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d.rounded_rectangle((20, 20, 860, ch - 30), radius=34, fill=(255, 252, 244, 255), outline=(176, 110, 50, 255), width=5)
    m = Image.new('L', (820, ih), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 819, ih - 1), radius=22, fill=255); c.paste(img.convert('RGBA'), (30, 30), m)
    if tag:
        f = font(FB, 44); w = d.textbbox((0, 0), tag, font=f)[2]
        d.rounded_rectangle((440 - w / 2 - 28, ih - 54, 440 + w / 2 + 28, ih + 30), radius=24, fill=(186, 62, 48, 255), outline=(255, 232, 170, 255), width=4); d.text((440 - w / 2, ih - 40), tag, font=f, fill=(255, 244, 214, 255))
    d.rectangle((350, 0, 530, 44), fill=(255, 222, 130, 200))
    return c.rotate(tilt, resample=Image.BICUBIC, expand=True)
def sticker(txt, p, t, tilt=-8):
    f = font(FS, 62); tw = ImageDraw.Draw(Image.new('RGBA', (4, 4))).textbbox((0, 0), txt, font=f)[2]
    if tw > 760:
        f = font(FS, 46); tw = ImageDraw.Draw(Image.new('RGBA', (4, 4))).textbbox((0, 0), txt, font=f)[2]
    im = Image.new('RGBA', (tw + 90, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 14, tw + 82, 130), radius=26, fill=(255, 226, 70, 255), outline=(120, 40, 20, 255), width=6); d.text((45, 30), txt, font=f, fill=(176, 36, 30, 255))
    s = max(0.01, back(p)); a = int(255 * min(1, p * 4))
    im2 = im.resize((max(1, int(im.size[0] * s)), max(1, int(im.size[1] * s))), Image.LANCZOS).rotate(math.sin(t * 6) * 4 + tilt, expand=True)
    if a < 255: im2.putalpha(im2.split()[3].point(lambda v: int(v * a / 255)))
    return im2
# ---------- dữ liệu theo nội dung ----------
_ICON = ROOT + '/assets/icon_nhan_vat'; _IMG = {}
def _slug(name):
    import unicodedata, re
    t = unicodedata.normalize('NFD', name.replace('đ', 'd').replace('Đ', 'D'))
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in t if unicodedata.category(c) != 'Mn').lower())
def portrait(name):
    key = ('p', name)
    if key not in _IMG:
        for ext in ('jpg', 'png'):
            p = f'{_ICON}/{_slug(name)}.{ext}'
            if os.path.exists(p): _IMG[key] = Image.open(p).convert('RGB').resize((820, 700), Image.LANCZOS); break
        else: _IMG[key] = None
    return _IMG[key]
def scene_img(kind, u, tt, dur):
    import mapscenes as MS, mapprops as MP
    lay = Image.new('RGBA', (820, 700), (0, 0, 0, 0)); MS._DUR = dur
    MP.draw(ImageDraw.Draw(lay), kind, 410, 350, 38, u, tt, ''); bg = Image.new('RGBA', lay.size, (252, 240, 214, 255)); bg.alpha_composite(lay); return bg.convert('RGB').crop((0, 92, 820, 612))
class Ctx: pass
X = Ctx(); X.ready = False
def setup(C, B):
    if X.ready: return
    X.C, X.B = C, B; X.ready = True
    asrp = os.environ.get('ASR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'asr_ly1.json'))
    X.asr = json.load(open(asrp)) if os.path.exists(asrp) else {}
    # nhãn dán: số năm, ghi chú ngắn, khung đùa
    ev = []
    for nx in []:
        cn, big, small, dl = nx[0], nx[1], nx[2], nx[3]; ev.append((B.T[cn] + dl, B.T[cn] + dl + 2.6, big, 'num'))
    for x in getattr(C, 'NOTES', []):
        if len(x[4]) <= 38: ev.append((x[0], min(x[1], x[0] + 3.0), x[4], 'note'))
    for (t0, t1, icon, txt) in getattr(C, 'JOKES', []):
        if len(txt) <= 40: ev.append((t0, min(t1, t0 + 3.0), txt, 'joke'))
    ev.sort(); X.stick = ev
    X.words = {}
    for n, txt in B.texts.items():
        src = txt.split(); a = X.asr.get(str(n), []); row = []
        for i, w in enumerate(src):
            if a: j = round(i * (len(a) - 1) / max(1, len(src) - 1)); s, e = a[j][1], a[j][2]
            else: s = D(B, n) * i / len(src); e = D(B, n) * (i + 1) / len(src)
            row.append((w, B.T[n] + 0.12 + s, B.T[n] + 0.12 + e))
        X.words[n] = row
    X.env = None
def D(B, n): return B.D[n]
def _env(B, TOTAL):
    if X.env is None:
        SR = 8000; e = np.zeros(int((TOTAL + 2) * SR), np.float32); vd = os.environ['VOICE_DIR']
        for n in B.T:
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{vd}/{n}.mp3', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
            v = np.abs(np.frombuffer(raw, np.float32)); i0 = int((B.T[n] + 0.12) * SR); j = min(len(e), i0 + len(v)); e[i0:j] = v[:j - i0]
        e = np.convolve(e, np.ones(500) / 500, 'same'); X.env = (e / max(1e-6, e.max()), SR)
    return X.env
def _subs(f, t, n, B):
    row = X.words.get(n)
    if not row: return
    d = ImageDraw.Draw(f); fnt = font(FB, 49); x0, x1 = 575, 1045; lines = []; line = []; wdt = 0
    for w in row:
        ww = d.textbbox((0, 0), w[0] + ' ', font=fnt)[2]
        if wdt + ww > x1 - x0 and line: lines.append(line); line = []; wdt = 0
        line.append((w, ww)); wdt += ww
    lines.append(line); idx = max(0, sum(1 for w in row if w[1] <= t) - 1); acc = 0; li = 0
    for i, ln in enumerate(lines):
        acc += len(ln)
        if idx < acc: li = i; break
    s = max(0, min(li - 1, len(lines) - 4)); y = 1290
    for ln in lines[s:s + 4]:
        x = x0
        for (w, a, b), ww in ln:
            on = t >= a; now = a <= t <= b + 0.1
            col = (255, 226, 90, 255) if now else ((255, 250, 236, 255) if on else (240, 190, 170, 255))
            d.text((x, y), w, font=fnt, fill=col, stroke_width=4, stroke_fill=(110, 36, 28, 255)); x += ww
        y += 76
def compose(out, t, n, C, B, TOTAL, quiet, chap, year):
    setup(C, B); f = BG.copy()
    # chọn thẻ
    mode = 'map'; t0 = 0.0; img = None; tag = None; _k = ''; _sp = {'figs': []}
    if not quiet:
        for pr in getattr(C, 'PROPS', []):
            if pr[2].startswith('canh_') and pr[0] <= t <= pr[1]: mode = 'scene'; t0 = pr[0]; pr_ = pr
        if mode == 'map':
            for c in getattr(C, 'CARDS3', []):
                if c[0] <= t <= c[1] and portrait(c[2]) is not None: mode = 'face'; t0 = c[0]; tag = c[2]; img = portrait(c[2])
    if mode == 'scene': img = scene_img(pr_[2], (t - pr_[0]) / max(1e-6, pr_[1] - pr_[0]), t, pr_[1] - pr_[0])
    if mode == 'map':
        import doc2_fx2 as FX
        _sp = FX.spec_for(n, B.texts); _k = _sp['back']; img = FX.render(_sp, max(0.0, t - B.T[n]))
        # thẻ bản đồ đứng yên theo chương: không nảy lại mỗi giây
        t0 = B.T[n] if False else 0.0
    u = t - t0; pop = back(min(1, u / 0.45)) if mode != 'map' else 1.0
    shake = (math.sin(u * 60) * 14 * max(0, 1 - u / 0.4)) if (mode == 'face' and tag == 'Lê Hoàn') else 0
    c = card(img, tag, -1.6 if int(t0 * 10) % 2 else 1.4); sc = (0.55 + 0.45 * pop) if (mode != 'map' and u < 0.45) else 1.0 + 0.012 * math.sin(t * 2)
    c = c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS); cx = W / 2 + shake; cy = (700 if mode != 'scene' else 620) + ((1 - min(1, u / 0.45)) * 160 if mode != 'map' else 0)
    if mode != 'map' and u < 0.5:
        d = ImageDraw.Draw(f, 'RGBA'); rnd = random.Random(int(t0 * 100))
        for _ in range(14):
            a = rnd.uniform(0, 6.28); r0 = 430 + u * 400; r1 = r0 + 160
            d.line([(W / 2 + r0 * math.cos(a), 700 + r0 * math.sin(a) * 0.9), (W / 2 + r1 * math.cos(a), 700 + r1 * math.sin(a) * 0.9)], fill=(255, 200, 110, int(180 * (1 - u / 0.5))), width=7)
    f.alpha_composite(c, (int(cx - c.width / 2), int(cy - c.height / 2)))
    wow = False; k = 0
    for (a, b, txt, kind) in X.stick:
        if a <= t <= b:
            p = min((t - a) / 0.35, (b - t) / 0.3, 1); s_ = sticker(txt, p, t, -8 if k % 2 == 0 else 6)
            sx = 300 if k % 2 == 0 else 790; f.alpha_composite(s_, (int(sx - s_.width / 2), int(330 - s_.height / 2))); wow = wow or (t - a) < 1.2; k += 1; break
        k += 1
    f.alpha_composite(PANEL, (0, PY))
    e, SR = _env(B, TOTAL); i = int(t * SR); talk = float(min(1, e[i] * 2.5)) if 0 <= i < len(e) else 0.0
    wave = 1.0 if t < 1.6 else 0.0
    # cử động: mỗi ~3,5 giây đổi một kiểu; nhún theo nhịp nói; nhảy lên khi thẻ mới hiện hoặc nhãn dán bật
    seg = int(t / 3.5); gk = (seg * 7 + n) % 5
    larm = 1 if (wow or gk == 1) else (2 if gk == 3 else 0)
    run = 1.9 if (mode == 'map' and 'quan' in _sp['figs']) or gk == 4 else 1.0
    since = (t - t0) if mode != 'map' else (t - B.T[n]); fresh = since < 0.6 and since >= 0
    ang = -1.28 + 0.10 * math.sin(t * 3.0) - (0.35 * math.sin(min(1, since / 0.35) * math.pi) if fresh else 0.0)
    ln = 330 + (40 * math.sin(min(1, since / 0.35) * math.pi) if fresh else 0.0)
    L, _ = lamp(t, talk, 'wow' if wow else 'happy', None if wave else (ang, ln), wave, larm=larm, stride=run)
    hop = 70 * abs(math.sin(min(1, since / 0.6) * math.pi)) if fresh else 0.0
    hop += 22 * talk * abs(math.sin(t * 7.0)) + (26 * abs(math.sin(t * 8.0)) if run > 1.5 else 0.0)
    sq = 1 + 0.025 * math.sin(t * 8.0 if wow else t * 4.0) + (0.05 if hop > 30 else 0.0)
    L = L.resize((int(CW * 0.92 * (2 - sq)), int(CH * 0.92 * sq)), Image.LANCZOS)
    sway = 3.5 * math.sin(t * 2.2) + (6 * math.sin(t * 8.0) if run > 1.5 else 0.0)
    Lp = Image.new('RGBA', (L.width + 200, L.height + 200), (0, 0, 0, 0)); Lp.alpha_composite(L, (100, 100))
    Lp = Lp.rotate(sway, resample=Image.BICUBIC, center=(100 + L.width // 2, 100 + L.height - 20))
    f.alpha_composite(Lp, (int(60 - 100), int(H - 40 - L.height - 100 - hop)))
    _subs(f, t, n, B); d = ImageDraw.Draw(f)
    d.rounded_rectangle((36, 40, 760, 150), radius=34, fill=(186, 62, 48, 255), outline=(255, 222, 130, 255), width=5)
    d.text((70, 52), str(year), font=font(FS, 56), fill=(255, 234, 160, 255)); d.text((218, 60), 'sau Công nguyên', font=font(FB, 26), fill=(255, 240, 210, 255)); d.text((218, 96), chap, font=font(FB, 26), fill=(255, 240, 210, 255))
    f.alpha_composite(_logo, (W - 36 - 120, 36))
    d.rectangle((0, H - 14, W, H), fill=(80, 36, 26, 255)); d.rectangle((0, H - 14, int(W * t / TOTAL), H), fill=(255, 206, 110, 255))
    if t < 0.4: f.alpha_composite(Image.new('RGBA', (W, H), (250, 238, 208, int(255 * (1 - t / 0.4)))))
    if t > TOTAL - 1.0: f.alpha_composite(Image.new('RGBA', (W, H), (250, 238, 208, int(255 * (t - (TOTAL - 1.0))))))
    return f.convert('RGB')
