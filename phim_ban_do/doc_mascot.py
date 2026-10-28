"""Nhân vật đèn (avatar kênh) có mắt, mũi, miệng, tay chân, cầm thước chỉ lên ảnh minh họa. Vẽ bằng PIL, hoạt hình theo thời gian.
draw_mascot(frame_rgba, cx, foot_y, t, target=(x,y) hoặc None, talk=0..1) -> vẽ trực tiếp lên frame."""
import math
from PIL import Image, ImageDraw
import os
LOGO = os.environ.get('LOGO', '/tmp/lh/assets/logo/nguoi-gac-su.png')
def _lamp():
    im = Image.open(LOGO).convert('RGBA').crop((196, 58, 290, 238))
    from PIL import ImageDraw as _D, ImageFilter as _F
    a = im.copy(); px = a.load(); w, h = a.size
    # bỏ nền nâu sẫm của logo: lan từ mép vào, điểm tối thì trong suốt
    seen = set(); st = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    while st:
        x, y = st.pop()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h): continue
        r, g, b, _ = px[x, y]
        if max(r, g, b) > 120: continue
        seen.add((x, y)); px[x, y] = (r, g, b, 0); st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    al = a.split()[3].filter(_F.GaussianBlur(0.8)); a.putalpha(al); return a
_L = _lamp()
INK = (46, 30, 18, 255); LIMB = (236, 206, 150, 255); GOLD = (222, 168, 70, 255); SKIN = (246, 214, 150, 255)
def draw_mascot(fr, cx, foot_y, t, target=None, talk=0.0, H=600):
    S = 3; w, h = fr.size
    lay = Image.new('RGBA', (w * 1, h * 1), (0, 0, 0, 0))
    k = H / 180.0; lw, lh = int(94 * k), int(180 * k)
    bob = math.sin(t * 3.2) * H * 0.012
    leg = H * 0.20
    body_top = foot_y - leg - lh + bob
    lamp = _L.resize((lw, lh), Image.LANCZOS)
    d = ImageDraw.Draw(lay)
    # chân (2 chân, bước nhẹ)
    for sg in (-1, 1):
        sw = math.sin(t * 3.2 + (0 if sg < 0 else math.pi)) * H * 0.02
        hx = cx + sg * lw * 0.20; hy = body_top + lh - H * 0.02 + bob * 0
        fx = hx + sw; fy = foot_y
        d.line([(hx, hy), (fx, fy - H * 0.02)], fill=LIMB, width=int(H * 0.028))
        d.ellipse((fx - H * 0.06 + sg * H * 0.012, fy - H * 0.04, fx + H * 0.06 + sg * H * 0.012, fy + H * 0.005), fill=INK)
    # tay trái (buông, đung đưa)
    sx, sy = cx - lw * 0.30, body_top + lh * 0.55
    ax = sx - H * 0.10 + math.sin(t * 2.4) * H * 0.012; ay = sy + H * 0.20
    d.line([(sx, sy), ((sx + ax) / 2 - H * 0.03, (sy + ay) / 2), (ax, ay)], fill=LIMB, width=int(H * 0.026), joint='curve')
    d.ellipse((ax - H * 0.034, ay - H * 0.034, ax + H * 0.034, ay + H * 0.034), fill=SKIN, outline=INK, width=3)
    # thân đèn
    lay.alpha_composite(lamp, (int(cx - lw / 2), int(body_top)))
    d = ImageDraw.Draw(lay)
    # mắt, mũi, miệng trên ô kính
    gx, gy = cx, body_top + lh * 0.50
    look = 0.0
    if target: look = max(-1, min(1, (target[0] - cx) / 600)); lookv = max(-1, min(1, (target[1] - gy) / 900))
    else: lookv = 0
    blink = 1.0 if (t % 3.6) > 0.14 else 0.15
    for sg in (-1, 1):
        ex = gx + sg * lw * 0.115; ey = gy - lh * 0.07; r = lw * 0.075
        d.ellipse((ex - r, ey - r * blink, ex + r, ey + r * blink), fill=(255, 252, 240, 255), outline=INK, width=3)
        if blink > 0.5: d.ellipse((ex + look * r * 0.45 - r * 0.45, ey + lookv * r * 0.3 - r * 0.45, ex + look * r * 0.45 + r * 0.45, ey + lookv * r * 0.3 + r * 0.45), fill=INK)
    d.polygon([(gx, gy - lh * 0.02), (gx - lw * 0.035, gy + lh * 0.045), (gx + lw * 0.035, gy + lh * 0.045)], fill=(214, 140, 60, 255), outline=INK)
    mo = 0.15 + 0.55 * talk; mw = lw * 0.12; my = gy + lh * 0.095
    d.ellipse((gx - mw, my - mo * lh * 0.035, gx + mw, my + mo * lh * 0.045), fill=(120, 30, 30, 255) if talk > 0.15 else None, outline=INK, width=3)
    # tay phải cầm thước chỉ
    sx, sy = cx + lw * 0.30, body_top + lh * 0.52
    if target:
        dx, dy = target[0] - sx, target[1] - sy; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        reach = H * 0.20; hx, hy = sx + ux * reach * 0.55 + math.sin(t * 5) * 2, sy + uy * reach * 0.55 - H * 0.04
        ln = min(max(40, math.hypot(target[0] - hx, target[1] - hy) - 20), H * 1.1); tipx, tipy = hx + ux * ln, hy + uy * ln
        back = (hx - ux * H * 0.10, hy - uy * H * 0.10)
        nx, ny = -uy, ux; tw = H * 0.016
        d.polygon([(back[0] + nx * tw, back[1] + ny * tw), (tipx + nx * tw, tipy + ny * tw), (tipx - nx * tw, tipy - ny * tw), (back[0] - nx * tw, back[1] - ny * tw)], fill=(196, 140, 74, 255), outline=INK)
        for i in range(1, 12):
            px, py = back[0] + (tipx - back[0]) * i / 12, back[1] + (tipy - back[1]) * i / 12
            d.line([(px + nx * tw, py + ny * tw), (px + nx * tw * (0.2 if i % 2 else 0.5), py + ny * tw * (0.2 if i % 2 else 0.5))], fill=INK, width=2)
        d.ellipse((tipx - 7, tipy - 7, tipx + 7, tipy + 7), fill=(230, 60, 50, 255), outline=INK, width=2)
    else:
        hx, hy = sx + H * 0.10, sy + H * 0.20
    d.line([(sx, sy), ((sx + hx) / 2 + H * 0.03, (sy + hy) / 2), (hx, hy)], fill=LIMB, width=int(H * 0.026), joint='curve')
    d.ellipse((hx - H * 0.034, hy - H * 0.034, hx + H * 0.034, hy + H * 0.034), fill=SKIN, outline=INK, width=3)
    fr.alpha_composite(lay)
    return (tipx, tipy) if target else None

# ---------- phần ghép vào khung dọc ----------
_ENV = None
def _env(T, D, TOTAL):
    global _ENV
    if _ENV is None:
        import subprocess, numpy as np
        vd = os.environ['VOICE_DIR']; SR = 8000; e = np.zeros(int((TOTAL + 2) * SR), np.float32)
        for n in T:
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{vd}/{n}.mp3', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
            v = np.abs(np.frombuffer(raw, np.float32)); i0 = int((T[n] + 0.12) * SR); j = min(len(e), i0 + len(v)); e[i0:j] = v[:j - i0]
        e = np.convolve(e, np.ones(400) / 400, 'same'); _ENV = (e / max(1e-6, e.max()), SR)
    return _ENV
def overlay(out, t, tgt, T, D, TOTAL, W=1080, H=1920, top=1290):
    import numpy as np
    e, SR = _env(T, D, TOTAL); i = int(t * SR); talk = float(min(1, e[i] * 2.4)) if 0 <= i < len(e) else 0.0
    panel = Image.new('RGBA', (W, H - top), (30, 22, 16, 255)); d = ImageDraw.Draw(panel)
    for y in range(H - top): d.line([(0, y), (W, y)], fill=(30 + int(14 * y / (H - top)), 22 + int(8 * y / (H - top)), 16, 255))
    d.line([(0, 0), (W, 0)], fill=(222, 168, 70, 255), width=5)
    out.alpha_composite(panel, (0, top))
    draw_mascot(out, 250, H - 36, t, tgt, talk, H=470)
    return out

_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'icon_nhan_vat')
_CACHE = {}
def _slug(name):
    import unicodedata, re
    t = unicodedata.normalize('NFD', name.replace('đ', 'd').replace('Đ', 'D'))
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in t if unicodedata.category(c) != 'Mn').lower())
def _backdrop(W=1080, top=1290):
    if 'bd' not in _CACHE:
        im = Image.new('RGBA', (W, top)); d = ImageDraw.Draw(im)
        for y in range(top): d.line([(0, y), (W, y)], fill=(70 - int(24 * y / top), 54 - int(20 * y / top), 40 - int(16 * y / top), 255))
        _CACHE['bd'] = im
    return _CACHE['bd']
def _portrait(name, bw, bh):
    key = ('p', name, bw, bh)
    if key in _CACHE: return _CACHE[key]
    for ext in ('jpg', 'png'):
        p = os.path.join(_ICON, _slug(name) + '.' + ext)
        if os.path.exists(p): break
    else: _CACHE[key] = None; return None
    im = Image.open(p).convert('RGB'); w, h = im.size; sc = max(bw / w, bh / h)
    im = im.resize((int(w * sc) + 2, int(h * sc) + 2), Image.LANCZOS); _CACHE[key] = im; return im
ACTIVE = False
def stage(out, t, C, n, chip, logo, font, clamp, ease, top=1290):
    global ACTIVE; ACTIVE = False
    """Khung minh họa phía trên: cảnh nhỏ (canh_*) hoặc chân dung nhân vật đang được nhắc; không có thì để nguyên bản đồ."""
    import mapscenes as MS, mapprops as MP
    W = out.size[0]; kind = None
    for pr in getattr(C, 'PROPS', []):
        if pr[2].startswith('canh_') and pr[0] <= t <= pr[1]:
            kind = ('scene', pr, min(clamp((t - pr[0]) / 0.4), clamp((pr[1] - t) / 0.4)))
    if kind is None:
        for c in getattr(C, 'CARDS3', []):
            if c[0] <= t <= c[1] and _portrait(c[2], 860, 640) is not None:
                kind = ('face', c, min(clamp((t - c[0]) / 0.4), clamp((c[1] - t) / 0.4)))
    if kind is None: return out
    ACTIVE = True; k = ease(kind[2]); lay = _backdrop().copy(); d = ImageDraw.Draw(lay)
    if kind[0] == 'scene':
        pr = kind[1]; MS._DUR = pr[1] - pr[0]; sl = Image.new('RGBA', lay.size, (0, 0, 0, 0))
        MP.draw(ImageDraw.Draw(sl), pr[2], W / 2, 600, 46 * (pr[6] if len(pr) > 6 else 1.0), (t - pr[0]) / max(1e-6, pr[1] - pr[0]), t, pr[5])
        lay.alpha_composite(sl)
    else:
        c = kind[1]; im = _portrait(c[2], 860, 640); u = clamp((t - c[0]) / max(0.01, c[1] - c[0])); z = 1.0 + 0.06 * u
        cw, ch = 860 / z, 640 / z; x0 = (im.width - cw) / 2; y0 = max(0, (im.height - ch) * 0.25)
        pic = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((860, 640), Image.LANCZOS).convert('RGBA')
        mk = Image.new('L', (860, 640), 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, 859, 639), radius=36, fill=255)
        d.rounded_rectangle((W / 2 - 440, 235, W / 2 + 440, 895), radius=44, fill=(222, 168, 70, 255)); lay.paste(pic, (int(W / 2 - 430), 245), mk)
        f1 = font(60, True); f2 = font(38, False)
        for txt, f, y, col in ((c[2], f1, 918, (255, 236, 190, 255)), (c[3], f2, 996, (222, 190, 130, 255))):
            w = d.textbbox((0, 0), txt, font=f)[2]; d.text(((W - w) / 2, y), txt, font=f, fill=col)
    out2 = out.copy(); out2.paste(Image.blend(out.crop((0, 0, lay.size[0], lay.size[1])), lay, k), (0, 0))
    out2.alpha_composite(chip, (50, 40)) if chip is not None else None
    out2.alpha_composite(logo, (W - 44 - 130, 34))
    return out2
