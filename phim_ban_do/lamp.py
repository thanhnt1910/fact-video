"""Nhân vật đèn vẽ từ đầu (vector, siêu mẫu 2x): thân đèn tròn trịa, mặt biểu cảm, lửa cử động, tay chân mềm, thước chỉ ngắn."""
import math
from PIL import Image, ImageDraw, ImageFilter
GOLD = (214, 150, 52); GOLD_D = (150, 96, 30); GOLD_L = (255, 206, 110); INK = (74, 40, 22); GLOVE = (255, 248, 232); SHOE = (176, 52, 44)
CW, CH = 640, 860   # khung vẽ nhân vật (đơn vị cục bộ), gốc chân ở (320, 840)
def _grad(w, h, top, bot):
    im = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(im)
    for y in range(h): d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * y / max(1, h - 1)) for i in range(3)) + (255,))
    return im
def _limb(d, pts, w, col):
    d.line(pts, fill=col, width=w, joint='curve')
    for p in (pts[0], pts[-1]): d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=col)
def lamp(t, talk=0.0, mood="happy", point=None, wave=0.0, blink_phase=None):
    blink_phase = t if blink_phase is None else blink_phase
    """Trả về RGBA (CW x CH) và toạ độ đầu thước (cục bộ) nếu có point=(góc độ, độ dài)."""
    S = 2; im = Image.new('RGBA', (CW * S, CH * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sc = lambda *v: tuple(x * S for x in v)
    bob = math.sin(t * 4.0) * 5; step = math.sin(t * 4.0)
    cx = 320; base_y = 600 + bob
    # chân
    for sg in (-1, 1):
        hx = cx + sg * 62; ph = step * sg * 10
        _limb(d, [sc(hx, base_y - 4 + 0), sc(hx + ph * 0.3, base_y + 60), sc(hx + ph, 835 - 14)], 22 * S, INK)
        d.ellipse(sc(hx + ph - 44 + sg * 6, 812, hx + ph + 44 + sg * 6, 846), fill=SHOE, outline=INK, width=3 * S)
    # tay trái (sau thân): vẫy khi wave>0
    ang = -0.6 - wave * (1.6 + 0.5 * math.sin(t * 9)) if wave > 0 else 0.5 + 0.08 * math.sin(t * 3)
    sx, sy = cx - 150, 400 + bob
    ex, ey = sx - 40 * math.cos(ang) - 20, sy + 70 - 90 * math.sin(max(0, -ang)) if wave > 0 else sy + 80
    hx2, hy2 = (sx - 85 - 20 * wave, sy - 40 * wave * 2.2 + 85 * (1 - wave)) if wave > 0 else (sx - 62, sy + 150)
    _limb(d, [sc(sx, sy), sc((sx + hx2) / 2 - 22, (sy + hy2) / 2), sc(hx2, hy2)], 20 * S, INK)
    d.ellipse(sc(hx2 - 27, hy2 - 27, hx2 + 27, hy2 + 27), fill=GLOVE, outline=INK, width=3 * S)
    # vòng treo + nắp
    d.ellipse(sc(cx - 34, 24 + bob, cx + 34, 92 + bob), outline=GOLD_D, width=12 * S)
    d.polygon([sc(cx - 150, 160 + bob), sc(cx - 60, 82 + bob), sc(cx + 60, 82 + bob), sc(cx + 150, 160 + bob)], fill=GOLD, outline=INK)
    d.rounded_rectangle(sc(cx - 185, 150 + bob, cx + 185, 190 + bob), radius=12 * S, fill=GOLD_L, outline=INK, width=4 * S)
    # thân kính
    gx0, gy0, gx1, gy1 = cx - 160, 190 + bob, cx + 160, 560 + bob
    glass = _grad(int(gx1 - gx0) * S, int(gy1 - gy0) * S, (255, 238, 176), (255, 168, 60))
    msk = Image.new('L', glass.size, 0); ImageDraw.Draw(msk).rounded_rectangle((0, 0, glass.size[0] - 1, glass.size[1] - 1), radius=44 * S, fill=255)
    im.paste(glass, (int(gx0 * S), int(gy0 * S)), msk)
    d.rounded_rectangle(sc(gx0, gy0, gx1, gy1), radius=44 * S, outline=INK, width=6 * S)
    for px in (gx0 + 6, gx1 - 6): d.line([sc(px, gy0 + 20), sc(px, gy1 - 20)], fill=GOLD_D, width=9 * S)
    # lửa trong đèn (nhấp nháy) phía sau mặt
    fl = 1 + 0.12 * math.sin(t * 13) + 0.06 * math.sin(t * 23); fy = gy0 + 60
    d.polygon([sc(cx, fy - 30 * fl), sc(cx - 34, fy + 52), sc(cx, fy + 78), sc(cx + 34, fy + 52)], fill=(255, 112, 40, 255), outline=(190, 60, 20, 255))
    d.polygon([sc(cx, fy + 2 - 12 * fl), sc(cx - 18, fy + 52), sc(cx, fy + 66), sc(cx + 18, fy + 52)], fill=(255, 226, 120, 255))
    # mặt
    ey = gy0 + 190; big = 1.18 if mood == 'wow' else 1.0
    blink = 0.12 if (blink_phase % 3.4) < 0.14 else 1.0
    lx = 0.0; ly = 0.0
    if point: lx = math.cos(point[0]) * 6; ly = math.sin(point[0]) * 6
    for sg in (-1, 1):
        ex_ = cx + sg * 66; r = 36 * big
        d.ellipse(sc(ex_ - r, ey - r * blink, ex_ + r, ey + r * blink), fill=(255, 255, 255, 255), outline=INK, width=4 * S)
        if blink > 0.5:
            pr = 17 * big; d.ellipse(sc(ex_ - pr + lx, ey - pr + ly, ex_ + pr + lx, ey + pr + ly), fill=INK)
            d.ellipse(sc(ex_ - 6 + lx, ey - 12 + ly, ex_ + 6 + lx, ey - 0 + ly), fill=(255, 255, 255, 255))
        brow = -10 if mood == 'wow' else 0
        d.line([sc(ex_ - 30, ey - r - 14 + brow + sg * 4), sc(ex_ + 30, ey - r - 22 + brow - sg * 4)], fill=INK, width=7 * S)
    for sg in (-1, 1): d.ellipse(sc(cx + sg * 112 - 24, ey + 52, cx + sg * 112 + 24, ey + 82), fill=(255, 140, 130, 150))
    d.polygon([sc(cx, ey + 18), sc(cx - 10, ey + 50), sc(cx + 10, ey + 50)], fill=(224, 112, 52, 255), outline=INK)
    mo = max(talk, 0.9 if mood == 'wow' else 0); my = ey + 88
    if mo < 0.12: d.arc(sc(cx - 44, my - 26, cx + 44, my + 26), 15, 165, fill=INK, width=7 * S)
    else:
        mh = 14 + 38 * mo; mw = 38 if mood != 'wow' else 26
        d.ellipse(sc(cx - mw, my - mh * 0.4, cx + mw, my + mh), fill=(120, 24, 28, 255), outline=INK, width=5 * S)
        d.ellipse(sc(cx - mw * 0.6, my + mh * 0.35, cx + mw * 0.6, my + mh * 0.95), fill=(244, 128, 130, 255))
    # đế
    d.polygon([sc(cx - 150, 556 + bob), sc(cx + 150, 556 + bob), sc(cx + 124, 610 + bob), sc(cx - 124, 610 + bob)], fill=GOLD, outline=INK)
    d.rounded_rectangle(sc(cx - 140, 596 + bob, cx + 140, 624 + bob), radius=10 * S, fill=GOLD_D, outline=INK, width=4 * S)
    # tay phải + thước
    sx, sy = cx + 150, 400 + bob; tip = None
    if point:
        a, L = point; hx3, hy3 = sx + 74 * math.cos(a), sy + 74 * math.sin(a) + 10
        _limb(d, [sc(sx, sy), sc((sx + hx3) / 2, (sy + hy3) / 2 + 22), sc(hx3, hy3)], 20 * S, INK)
        bx, by = hx3 - 46 * math.cos(a), hy3 - 46 * math.sin(a); tx, ty = hx3 + L * math.cos(a), hy3 + L * math.sin(a)
        nx, ny = -math.sin(a) * 9, math.cos(a) * 9
        d.polygon([sc(bx + nx, by + ny), sc(tx + nx, ty + ny), sc(tx - nx, ty - ny), sc(bx - nx, by - ny)], fill=(236, 190, 110, 255), outline=INK)
        for i in range(1, 8):
            px, py = bx + (tx - bx) * i / 8, by + (ty - by) * i / 8; d.line([sc(px + nx, py + ny), sc(px + nx * 0.2, py + ny * 0.2)], fill=INK, width=3 * S)
        d.ellipse(sc(tx - 10, ty - 10, tx + 10, ty + 10), fill=(226, 52, 44, 255), outline=INK, width=3 * S); tip = (tx, ty)
        d.ellipse(sc(hx3 - 27, hy3 - 27, hx3 + 27, hy3 + 27), fill=GLOVE, outline=INK, width=3 * S)
    else:
        hx3, hy3 = sx + 62, sy + 150
        _limb(d, [sc(sx, sy), sc(sx + 50, sy + 60), sc(hx3, hy3)], 20 * S, INK); d.ellipse(sc(hx3 - 27, hy3 - 27, hx3 + 27, hy3 + 27), fill=GLOVE, outline=INK, width=3 * S)
    return im.resize((CW, CH), Image.LANCZOS), tip
if __name__ == '__main__':
    im, _ = lamp(0.4, 0.8, 'happy', (-1.05, 200)); bg = Image.new('RGBA', im.size, (176, 70, 52, 255)); bg.alpha_composite(im); bg.convert('RGB').save('/tmp/dm/lamp_test.jpg')
