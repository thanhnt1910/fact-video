import sys, os, math, subprocess, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from data import build

W, H, FPS = 1080, 1920, 30
FD = "/usr/share/fonts/opentype/inter/"
_fc = {}
def F(size, w="Bold"):
    k = (size, w)
    if k not in _fc: _fc[k] = ImageFont.truetype(FD + ("InterDisplay-" if size >= 60 else "Inter-") + w + ".otf", size)
    return _fc[k]
BG = (10, 13, 20); PANEL = (17, 22, 32); LINE = (34, 42, 56); GRID = (24, 30, 43)
WHITE = (236, 240, 246); MUTED = (145, 155, 172); DIM = (80, 90, 108)
GOLD = (245, 190, 60); GREEN = (38, 194, 129); RED = (240, 82, 82); BLUE = (64, 160, 255); ORANGE = (255, 140, 40); PURPLE = (180, 130, 255)
def clamp(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def prog(t, a, d=0.5): return ease((t - a) / d)
def mix(c, a, base=BG): a = clamp(a); return tuple(int(base[i] + (c[i] - base[i]) * a) for i in range(3))
def vn(x, dec=1): return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")

D = build(); N = len(D["c"])
SQ1, BRK_DN, WALK, TOUCH, ENTRY, SQ2, BRK2 = 9, 26, 45, 58, 59, 64, 81

# ---------- layout ----------
CX0, CX1 = 40, 925
PY0, PY1 = 300, 1090
MY0, MY1 = 1150, 1420
VIEW = 40
BW = (CX1 - CX0) / VIEW

class Cam:
    def __init__(s, vs, nb):
        s.vs = vs; s.nb = nb
        s.plo, s.phi = s._interp(s._prange)
        s.mlo, s.mhi = s._interp(s._mrange)
    def _interp(s, fn):
        a0, b0 = math.floor(s.vs), math.floor(s.nb)
        fa, fb = s.vs - a0, s.nb - b0
        r = lambda a, b: np.array(fn(a, b))
        v = (r(a0, b0) * (1 - fa) + r(a0 + 1, b0) * fa) * (1 - fb) + (r(a0, b0 + 1) * (1 - fa) + r(a0 + 1, b0 + 1) * fa) * fb
        return v
    def _idx(s, a, b):
        i0 = max(0, int(a)); i1 = min(N, max(i0 + 8, int(b) + 1), int(a) + VIEW)
        return i0, max(i0 + 1, i1)
    def _prange(s, a, b):
        i0, i1 = s._idx(a, b)
        lo, hi = D["l"][i0:i1].min(), D["h"][i0:i1].max()
        lo = min(lo, np.nanmin(D["lo"][i0:i1])); hi = max(hi, np.nanmax(D["up"][i0:i1]))
        span = max(hi - lo, 60); pad = span * .14
        return lo - pad, hi + pad * 1.4
    def _mrange(s, a, b):
        return 0.0, 10.0
    def x(s, i): return CX0 + (i - s.vs + .5) * BW
    def py(s, p): return PY1 - (p - s.plo) / (s.phi - s.plo) * (PY1 - PY0)
    def my(s, v): return MY1 - (v - s.mlo) / (s.mhi - s.mlo) * (MY1 - MY0)
    def vis(s, i): return s.vs - .5 <= i <= s.vs + VIEW - .5

# ---------- helpers ----------
def tokens(text):
    out = []
    for part in re.split(r"(\*\*.+?\*\*|\+\+.+?\+\+|~~.+?~~)", text):
        if not part: continue
        col = WHITE
        if part.startswith("**"): col, part = GOLD, part[2:-2]
        elif part.startswith("++"): col, part = GREEN, part[2:-2]
        elif part.startswith("~~"): col, part = RED, part[2:-2]
        for w in re.split(r"(\s+)", part):
            if w: out.append((w, col))
    return out
def rich(d, x, y, text, font, maxw, a=1.0, lh=54, base=WHITE):
    lines = [[]]; cur = 0
    for w, c in tokens(text):
        if c == WHITE: c = base
        tw = d.textlength(w, font=font)
        if w.isspace():
            if lines[-1]: lines[-1].append((w, c)); cur += tw
            continue
        if cur + tw > maxw and lines[-1]:
            while lines[-1] and lines[-1][-1][0].isspace(): cur -= d.textlength(lines[-1].pop()[0], font=font)
            lines.append([]); cur = 0
        lines[-1].append((w, c)); cur += tw
    for i, ln in enumerate(lines):
        xx = x
        for w, c in ln:
            d.text((xx, y + i * lh), w, font=font, fill=mix(c, a)); xx += d.textlength(w, font=font)
    return len(lines)

def pill(d, xy, text, a, col, size=24, anchor="mm", solid=False):
    if a <= 0: return
    f = F(size, "Bold"); tw = d.textlength(text, font=f); x, y = xy
    if anchor == "lm": x += tw / 2 + 14
    if anchor == "rm": x -= tw / 2 + 14
    x = max(tw / 2 + 24, min(W - tw / 2 - 24, x))
    box = [x - tw / 2 - 14, y - size * .85, x + tw / 2 + 14, y + size * .85]
    if solid:
        d.rounded_rectangle(box, int(size * .5), fill=mix(col, a)); d.text((x, y), text, font=f, fill=mix(BG, a, col), anchor="mm")
    else:
        d.rounded_rectangle(box, int(size * .5), fill=mix((22, 28, 40), a), outline=mix(col, a), width=2); d.text((x, y), text, font=f, fill=mix(col, a), anchor="mm")

def dashed(d, p0, p1, col, w=2, dash=10):
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1]); n = max(1, int(L / dash))
    for i in range(0, n, 2):
        a0, a1 = i / n, min(1, (i + 1) / n)
        d.line([(p0[0] + (p1[0] - p0[0]) * a0, p0[1] + (p1[1] - p0[1]) * a0), (p0[0] + (p1[0] - p0[0]) * a1, p0[1] + (p1[1] - p0[1]) * a1)], fill=col, width=w)

def series_line(d, cam, key, upto, col, w, ymap):
    i0 = max(0, int(math.floor(cam.vs - .5))); k = int(upto); fr = upto - k
    pts = [(cam.x(i), ymap(D[key][i])) for i in range(i0, min(k + 1, N))]
    if fr > 0 and k + 1 < N: pts.append((cam.x(k) + BW * fr, ymap(D[key][k] + (D[key][k + 1] - D[key][k]) * fr)))
    pts = [p for p in pts if CX0 - BW <= p[0] <= CX1 + BW]
    if len(pts) > 1: d.line(pts, fill=col, width=w, joint="curve")

# ---------- chart ----------
def draw_grid(d, cam, a=1.0):
    span = cam.phi - cam.plo; step = 25 if span < 200 else 50 if span < 420 else 100
    p = math.ceil(cam.plo / step) * step
    while p < cam.phi:
        y = cam.py(p)
        if PY0 < y < PY1:
            d.line([(CX0, y), (CX1, y)], fill=mix(GRID, a)); d.text((CX1 + 10, y), vn(p, 0), font=F(22, "Medium"), fill=mix(DIM, a), anchor="lm")
        p += step
    for i in range(0, N + 1, 6):
        x = cam.x(i) - BW / 2
        if CX0 <= x <= CX1:
            d.line([(x, PY0), (x, PY1)], fill=mix(GRID, a))
            if i // 6 < len(D["days"]): d.text((x + 6, PY1 - 34), D["days"][i // 6], font=F(20, "SemiBold"), fill=mix(DIM, a))
    d.text((CX0 + 4, PY0 - 36), "XAUUSD · H4", font=F(24, "Bold"), fill=mix(MUTED, a))
    d.text(((CX0 + CX1) / 2, (PY0 + PY1) / 2), "XAUUSD", font=F(120, "Black"), fill=mix((16, 20, 30), a), anchor="mm")

def draw_bands(d, cam, upto, a=1.0, hl=None):
    if upto <= 0 or a <= 0: return
    i0 = max(0, int(math.floor(cam.vs - .5))); k = min(int(upto), N - 1)
    idx = [i for i in range(i0, k + 1) if CX0 - BW <= cam.x(i) <= CX1 + BW]
    if len(idx) < 2: return
    top = [(cam.x(i), cam.py(D["up"][i])) for i in idx]; bot = [(cam.x(i), cam.py(D["lo"][i])) for i in idx]
    d.polygon(top + bot[::-1], fill=mix((20, 34, 56), a * (1.0 if hl in (None, "band") else .6)))
    bw_ = 5 if hl == "band" else 3; mw_ = 5 if hl == "mid" else 3
    bc = BLUE if hl in (None, "band", "sq", "walk") else tuple(int(c * .45 + BG[j] * .55) for j, c in enumerate(BLUE))
    mc = ORANGE if hl in (None, "mid", "touch") else tuple(int(c * .45 + BG[j] * .55) for j, c in enumerate(ORANGE))
    d.line(top, fill=mix(bc, a), width=bw_, joint="curve"); d.line(bot, fill=mix(bc, a), width=bw_, joint="curve")
    d.line([(cam.x(i), cam.py(D["mid"][i])) for i in idx], fill=mix(mc, a), width=mw_, joint="curve")

def draw_price(d, cam, a=1.0, ema_n=0, ema_a=1.0, hl=None):
    draw_bands(d, cam, ema_n, ema_a * a, hl)
    nb = cam.nb; k = int(nb); fr = nb - k
    for i in range(max(0, int(cam.vs) - 1), min(N, k + 1)):
        if not cam.vis(i): continue
        o, h, l, c = D["o"][i], D["h"][i], D["l"][i], D["c"][i]
        if i == k:
            if fr <= 0: break
            c = o + (c - o) * fr; h = max(o, c) + (h - max(D["o"][i], D["c"][i])) * fr; l = min(o, c) - (min(D["o"][i], D["c"][i]) - l) * fr
        col = mix(GREEN if c >= o else RED, a)
        x = cam.x(i); d.line([(x, cam.py(h)), (x, cam.py(l))], fill=col, width=3)
        y0, y1 = sorted([cam.py(o), cam.py(c)]); d.rectangle([x - BW * .34, y0, x + BW * .34, max(y1, y0 + 2)], fill=col)
    if nb > 0 and a > .5:
        li = min(N - 1, k if fr > 0 else k - 1)
        last = D["o"][li] + (D["c"][li] - D["o"][li]) * (fr if (fr > 0 and li == k) else 1)
        col = GREEN if last >= D["o"][li] else RED
        y = cam.py(last); dashed(d, (CX0, y), (CX1, y), mix(col, .6 * a), 1, 6)
        f = F(21, "Bold"); txt = vn(last, 2); tw = d.textlength(txt, font=f)
        d.rounded_rectangle([CX1 + 2, y - 17, CX1 + 16 + tw, y + 17], 6, fill=mix(col, a)); d.text((CX1 + 9, y), txt, font=f, fill=BG, anchor="lm")

def draw_macd(d, cam, a, hl=None, upto=None):
    """Panel độ rộng dải (Bandwidth %) = (dải trên − dải dưới) / dải giữa."""
    if a <= 0: return
    n = cam.nb if upto is None else upto
    d.rounded_rectangle([CX0 - 8, MY0 - 46, CX1 + 8, MY1 + 10], 16, fill=mix(PANEL, a), outline=mix(LINE, a), width=2)
    d.text((CX0 + 8, MY0 - 30), "BB Width 20 2", font=F(22, "Bold"), fill=mix(MUTED, a), anchor="lm")
    li = max(0, min(N - 1, int(math.ceil(n)) - 1))
    if n > 0: d.text((CX0 + 190, MY0 - 30), vn(D["bw"][li], 2) + "%", font=F(22, "Bold"), fill=mix(PURPLE, a), anchor="lm")
    for lv in (2, 4, 6, 8):
        y = cam.my(lv); d.line([(CX0, y), (CX1, y)], fill=mix(GRID, a)); d.text((CX1 + 12, y), f"{lv}%", font=F(20, "Bold"), fill=mix(DIM, a), anchor="lm")
    if hl == "sq":
        d.rectangle([CX0, cam.my(4), CX1, cam.my(0)], fill=mix((50, 40, 14), a * .9))
        d.text((CX0 + 12, cam.my(4) + 18), "Vùng co thắt (dải hẹp)", font=F(22, "Bold"), fill=mix(GOLD, a), anchor="lm")
    if n <= 0: return
    series_line(d, cam, "bw", min(n, N - 1), mix(PURPLE, a), 5 if hl == "sq" else 4, cam.my)

def legend(d, a, items, y):
    x = CX0
    for name, col in items:
        d.rounded_rectangle([x, y - 5, x + 30, y + 5], 3, fill=mix(col, a))
        d.text((x + 40, y), name, font=F(26, "SemiBold"), fill=mix(WHITE, a), anchor="lm")
        x += 40 + d.textlength(name, font=F(26, "SemiBold")) + 40

# ---------- brand / chrome ----------
def logo(d, x, y, s, a=1.0):
    d.rounded_rectangle([x, y, x + s, y + s], int(s * .22), fill=mix((30, 24, 8), a), outline=mix(GOLD, a), width=max(2, s // 28))
    cw = s * .13; gap = s * .08; x0 = x + (s - (3 * cw + 2 * gap)) / 2
    for i, (bt, bb, col) in enumerate([(.37, .77, RED), (.25, .65, GREEN), (.10, .49, GREEN)]):
        cx = x0 + i * (cw + gap)
        d.line([(cx + cw / 2, y + s * bt - s * .06), (cx + cw / 2, y + s * bb + s * .06)], fill=mix(col, a), width=max(2, s // 40))
        d.rectangle([cx, y + s * bt, cx + cw, y + s * bb], fill=mix(col, a))
    d.line([(x + s * .16, y + s * .82), (x + s * .84, y + s * .82)], fill=mix(GOLD, a), width=max(2, s // 30))
def wordmark(d, x, y, size, a=1.0, anchor="la"):
    f = F(size, "Black"); w1 = d.textlength("TRADER", font=f); w2 = d.textlength("9X", font=f)
    if anchor == "ma": x -= (w1 + w2) / 2
    d.text((x, y), "TRADER", font=f, fill=mix(WHITE, a)); d.text((x + w1, y), "9X", font=f, fill=mix(GOLD, a))


PARTS = {1: ("Định nghĩa", "Bollinger Bands là gì?"), 2: ("Thuật ngữ & ứng dụng", "Học trên biểu đồ vàng thật")}
def header(d, part, title, sub, a=1.0):
    logo(d, 40, 54, 46, a)
    d.text((98, 77), "TRADER9X MASTERCLASS · XAUUSD", font=F(23, "Bold"), fill=mix(GOLD, a), anchor="lm")
    d.text((W - 40, 77), f"PHẦN {part}/2", font=F(23, "Bold"), fill=mix(GOLD, a), anchor="rm")
    d.text((40, 118), title, font=F(60, "ExtraBold"), fill=mix(WHITE, a))
    d.text((42, 196), sub, font=F(28, "Medium"), fill=mix(MUTED, a))
CAP_Y = 1470
def caption(d, t, caps, y=CAP_Y):
    for a0, a1, txt in caps:
        if a0 <= t < a1:
            a = min(prog(t, a0, .3), clamp((a1 - t) / .25)); off = (1 - a) * 16
            d.rounded_rectangle([40, y + off, W - 40, y + 220 + off], 22, fill=mix(PANEL, a), outline=mix(LINE, a), width=2)
            d.rectangle([40, y + 24 + off, 47, y + 196 + off], fill=mix(GOLD, a))
            rich(d, 78, y + 34 + off, txt, F(42, "SemiBold"), W - 160, a, 58)

def footer(d, gt):
    y = 1730
    d.rectangle([40, y, W - 40, y + 6], fill=(26, 32, 44)); d.rectangle([40, y, 40 + (W - 80) * gt / TOTAL, y + 6], fill=GOLD)
    d.text((W / 2, 1822), "Nội dung giáo dục, không phải khuyến nghị đầu tư.", font=F(22, "Medium"), fill=DIM, anchor="mm")
    d.text((W / 2, 1854), "Nến H4 dựng lại theo giá ngày thực tế 26/10–13/11/2026 (MetalCharts) · © 2026 Trader9x", font=F(21, "Medium"), fill=DIM, anchor="mm")

def circle(d, xy, r, col, a, w=4):
    x, y = xy; d.ellipse([x - r, y - r, x + r, y + r], outline=mix(col, a), width=w)


# ---------- timeline (old-time units; voice_tl stretches them) ----------
SC = []
def scene(n, du): SC.append((n, du))
scene("intro", 3.2); scene("card1", 2.2); scene("p1", 17.0); scene("card2", 2.2)
# Phần 2: beats (start, term index or None, title, sub)
TERMS = [("Dải giữa (SMA 20)", "Trung bình giá đóng cửa của **20 nến** – đường xương sống của chỉ báo.", ORANGE),
         ("Dải trên & dải dưới", "Cách dải giữa **±2 độ lệch chuẩn**: biến động lớn thì dải ++nở ra++, thị trường yên thì dải **co lại**.", BLUE),
         ("Co thắt (Squeeze)", "Độ rộng dải xuống **rất thấp**: thị trường đang **nén lại**, thường trước một cú chạy mạnh.", GOLD),
         ("Bám dải (Walking the band)", "Nến liên tục đóng **sát hoặc ngoài dải trên/dưới**: xu hướng đang **rất mạnh**.", GREEN),
         ("Hồi về dải giữa", "Trong xu hướng tăng, nhịp hồi về **dải giữa** thường là nơi giá **tìm lại lực**.", ORANGE)]
P2 = [  # (t0, term, caption or None)
    (0.0, 0, None), (7.0, 0, "m_app"),
    (13.0, 1, None), (19.0, 1, "b_app"),
    (25.0, 2, None), (31.0, 2, "sq1"), (37.0, 2, "sq2"),
    (43.0, 3, None), (49.0, 3, "w1"), (55.0, 3, "w2"),
    (60.0, 4, None), (66.0, 4, "r1"), (72.0, 4, "r2"), (77.0, 2, "sq3"),
    (84.0, None, "now1"), (89.0, None, "now2"), (94.0, None, "now3")]
P2_DUR = 100.0
scene("p2", P2_DUR); scene("check", 11.0); scene("outro", 4.5)
TOTAL = sum(du for _, du in SC)
def locate(gt):
    acc = 0
    for n, du in SC:
        if gt < acc + du: return n, gt - acc, du
        acc += du
    return SC[-1][0], SC[-1][1] - 1e-3, SC[-1][1]
def p2_beat(t):
    k = 0
    for i, b in enumerate(P2):
        if t >= b[0]: k = i
    t0 = P2[k][0]; t1 = P2[k + 1][0] if k + 1 < len(P2) else P2_DUR
    return k, t - t0, t1 - t0

def ramp(t, pts):
    """piecewise-linear (smoothstep per segment) value from [(t, v), ...]"""
    if t <= pts[0][0]: return pts[0][1]
    for (a, va), (b, vb) in zip(pts, pts[1:]):
        if t <= b: return va + (vb - va) * eio((t - a) / (b - a))
    return pts[-1][1]
NB_P2 = [(0, 2), (12, 14), (13, 16), (24, 21), (31, 24), (37, 26), (42, 31), (48, 40), (55, 52), (60, 54), (66, 58), (72, 60), (77, 64), (83, 82), (89, 90)]
VS_P2 = [(0, 0), (43, 0), (55, 14), (72, 22), (83, 44), (89, 50)]
CAPS = {
 "m_app": "27/10: giá đi **trên dải giữa** (~4.017) – phe mua đang giữ nhịp hồi.",
 "b_app": "Giá đi **bên trong hai dải** phần lớn thời gian. Dải **hẹp** = thị trường yên, dải **rộng** = biến động mạnh.",
 "sq1": "27–30/10: độ rộng dải chỉ còn **~2,3–2,6%** – dải **co thắt**, thị trường đang **nén lại**.",
 "sq2": "30/10: giá ~~phá mạnh xuống dưới dải dưới~~, vàng sập về **3.871**. Co thắt không báo trước hướng – chờ nến phá dải.",
 "w1": "04–05/11: nhiều nến đóng cửa **trên dải trên**, giá ++bám dải++ lên **4.147,6**.",
 "w2": "Đóng ngoài dải trên trong xu hướng mạnh thường là **tiếp diễn**, chưa phải lệnh bán.",
 "r1": "06/11: giá hồi về **dải giữa** quanh **4.030–4.040** rồi bật lên – dải giữa thành **hỗ trợ động**.",
 "r2": "Ví dụ: **vào lệnh** khi nến bật lên đóng cửa trên dải giữa (~4.063), **SL** dưới đáy gần nhất (~4.020).",
 "sq3": "09–10/11: dải lại **co thắt** (~3,5%). Lần này giá ~~phá xuống~~, 12/11 đóng dưới dải dưới, vàng về **3.853**.",
 "now1": "Hiện tại: phiên **13/11** đóng cửa quanh **3.876**, nằm **dưới dải giữa** (~3.943).",
 "now2": "Dải đang **mở rộng** (~6,8%) → biến động còn lớn, xu hướng ngắn hạn nghiêng ~~giảm~~.",
 "now3": "Chờ giá **lấy lại dải giữa** để xác nhận, đừng vội bắt đáy.",
}
def chapter_card(im, t, du, num):
    title, sub = PARTS[num]
    a = min(prog(t, 0, .35), clamp((du - t) / .3))
    im.paste(Image.blend(im, Image.new("RGB", (W, H), BG), .82 * a))
    d = ImageDraw.Draw(im)
    d.text((W / 2, 760), "PHẦN", font=F(40, "Bold"), fill=mix(MUTED, a), anchor="mm")
    d.text((W / 2, 880), f"{num:02d}", font=F(190, "Black"), fill=mix(GOLD, a), anchor="mm")
    w = 240 * prog(t, .15, .5); d.rectangle([W / 2 - w, 1000, W / 2 + w, 1005], fill=mix(GOLD, a))
    d.text((W / 2, 1070), title, font=F(66, "ExtraBold"), fill=mix(WHITE, a), anchor="mm")
    d.text((W / 2, 1140), sub, font=F(34, "Medium"), fill=mix(MUTED, a), anchor="mm")

def div_sketch(d, x0, y0, a):
    # mini schematic: price higher high vs macd lower high
    f = F(22, "SemiBold")
    d.text((x0, y0), "Giá", font=f, fill=mix(MUTED, a))
    pts = [(x0 + 60, y0 + 70), (x0 + 110, y0 + 20), (x0 + 150, y0 + 55), (x0 + 200, y0 + 5), (x0 + 240, y0 + 60)]
    d.line(pts, fill=mix(WHITE, a), width=3); d.line([pts[1], pts[3]], fill=mix(PURPLE, a), width=4)
    d.text((x0, y0 + 100), "BB", font=f, fill=mix(MUTED, a))
    q = [(x0 + 60, y0 + 175), (x0 + 110, y0 + 110), (x0 + 150, y0 + 160), (x0 + 200, y0 + 135), (x0 + 240, y0 + 175)]
    d.line(q, fill=mix(BLUE, a), width=3); d.line([q[1], q[3]], fill=mix(PURPLE, a), width=4)


def term_card(d, ti, a):
    nm, df, col = TERMS[ti]
    y = CAP_Y + 12; off = (1 - a) * 16
    d.rounded_rectangle([40, y + off, W - 40, y + 228 + off], 22, fill=mix(PANEL, a), outline=mix(col, a), width=3)
    d.text((76, y + 36 + off), f"THUẬT NGỮ {ti + 1}/5", font=F(22, "Bold"), fill=mix(MUTED, a), anchor="lm")
    d.text((76, y + 84 + off), nm, font=F(46, "ExtraBold"), fill=mix(col, a), anchor="lm")
    rich(d, 76, y + 124 + off, df, F(31, "SemiBold"), W - 160, a, 42)

def frame(gt):
    name, t, du = locate(gt)
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    if name == "outro":
        a = prog(t, .1, .5)
        logo(d, W / 2 - 85, 560, 170, a)
        wordmark(d, W / 2, 780, 88, prog(t, .3), anchor="ma")
        d.text((W / 2, 920), "Tập sau: EMA cross – giao cắt đường trung bình", font=F(38, "SemiBold"), fill=mix(WHITE, prog(t, .6)), anchor="mm")
        pill(d, (W / 2, 1040), "Theo dõi để không bỏ lỡ", prog(t, .9), GOLD, 34, solid=True)
        footer(d, gt)
        if t > du - .4: im = Image.blend(Image.new("RGB", (W, H)), im, clamp((du - t) / .4))
        return im
    ema_n, ema_a, ma, hl, part = 0, 1.0, 0, None, 1
    title, sub = "Bollinger Bands là gì?", "Định nghĩa & cách tính"
    if name == "intro": cam = Cam(50, N); ma = 1; ema_n = N
    elif name == "card1": cam = Cam(0, 2)
    elif name == "p1":
        nb = 2 + 12 * eio((t - .3) / 8.5); cam = Cam(0, nb); ema_n = 14 * eio((t - 3.5) / 6.0)
    elif name == "card2": cam = Cam(0, 14); ema_n = 14; ema_a = .7
    elif name == "p2":
        part = 2; k, tb, bd = p2_beat(t); term = P2[k][1]
        cam = Cam(ramp(t, VS_P2), ramp(t, NB_P2)); ma = prog(t, 0, .5)
        hl = {0: "mid", 1: "band", 2: "sq", 3: "walk", 4: "touch"}.get(term) if term is not None else None
        ema_n = cam.nb
        if term is not None: title, sub = TERMS[term][0], f"Thuật ngữ {term + 1}/5 · ứng dụng trên XAUUSD"
        else: title, sub = "Hiện tại: vàng ~3.876", "Bollinger Bands đang nói gì?"
    else:  # check
        cam = Cam(50, N); ma = 1; ema_n = N; part = 2; title, sub = "Checklist", "Dùng Bollinger Bands cho đúng"
    dimc = .25 if name == "intro" else 1.0
    draw_grid(d, cam, dimc)
    draw_price(d, cam, dimc, ema_n, ema_a, hl)
    draw_macd(d, cam, ma * dimc, hl)
    if name == "intro":
        a = prog(t, .1, .5)
        im.paste(Image.blend(im, Image.new("RGB", (W, H), BG), .55)); d = ImageDraw.Draw(im)
        logo(d, W / 2 - 55, 520, 110, a)
        d.text((W / 2, 690), "TRADER9X MASTERCLASS", font=F(34, "Bold"), fill=mix(GOLD, a), anchor="mm")
        d.text((W / 2, 800), "BOLLINGER", font=F(150, "Black"), fill=mix(WHITE, prog(t, .3)), anchor="mm")
        d.text((W / 2, 930), "BANDS", font=F(150, "Black"), fill=mix(GOLD, prog(t, .4)), anchor="mm")
        d.text((W / 2, 1040), "Định nghĩa · Thuật ngữ & Ứng dụng", font=F(42, "SemiBold"), fill=mix(GOLD, prog(t, .6)), anchor="mm")
        d.text((W / 2, 1105), "Ví dụ thật trên Vàng XAU/USD", font=F(34, "Medium"), fill=mix(MUTED, prog(t, .8)), anchor="mm")
        if t > du - .3: im = Image.blend(Image.new("RGB", (W, H), BG), im, clamp((du - t) / .3))
        return im
    header(d, part, title, sub)
    if name == "p1":
        legend(d, prog(t, 3.5), [("Dải giữa SMA 20", ORANGE), ("Dải trên / dưới ±2σ", BLUE)], MY0 - 10)
        ab = prog(t, 10.5)
        if ab > 0:
            d.rounded_rectangle([CX0, MY0 + 30, CX1, MY1], 24, fill=mix(PANEL, ab), outline=mix(GOLD, ab), width=3)
            fb = F(48, "Black"); fs = F(40, "Bold")
            for y_, parts, f_ in [(MY0 + 85, [("Dải giữa = ", WHITE), ("SMA 20", ORANGE)], fb),
                                  (MY0 + 165, [("Dải trên/dưới = ", WHITE), ("SMA 20 ± 2σ", BLUE)], fs)]:
                tw = sum(d.textlength(p_, font=f_) for p_, _ in parts); xx = (CX0 + CX1) / 2 - tw / 2
                for p_, c in parts: d.text((xx, y_), p_, font=f_, fill=mix(c, ab), anchor="lm"); xx += d.textlength(p_, font=f_)
            d.text(((CX0 + CX1) / 2, MY0 + 225), "σ = độ lệch chuẩn của 20 nến – thước đo biến động", font=F(28, "Medium"), fill=mix(MUTED, ab), anchor="mm")
        caption(d, t, [(.2, 3.5, "**Bollinger Bands** do John Bollinger phát triển đầu thập niên 1980, để đo **biến động** của giá."),
                       (3.5, 10.5, "Gồm **3 đường** bao quanh giá: dải giữa, dải trên và dải dưới. Dải tự **nở ra** khi biến động lớn, **co lại** khi thị trường yên."),
                       (10.5, 17.0, "Dải giữa là **SMA 20**. Dải trên và dưới cách dải giữa **2 độ lệch chuẩn** của cùng 20 nến.")])
    elif name == "p2":
        k, tb, bd = p2_beat(t); term, cap = P2[k][1], P2[k][2]
        legend(d, 1, [("Dải giữa", ORANGE), ("Dải trên/dưới", BLUE), ("Độ rộng dải", PURPLE)], MY1 + 36)
        # persistent annotations (vị trí thật trên dữ liệu)
        def on(beat_t, d0=.5): return prog(t, beat_t, d0)
        def pmark(i, yv, col, txt, a, dy=-48, anchor="mm", dx=0, r=18):
            if not cam.vis(i) or cam.nb < i + 1: return None
            p_ = (cam.x(i), cam.py(yv)); circle(d, p_, r, col, a)
            if txt: pill(d, (p_[0] + dx, p_[1] + dy), txt, a, col, 22, anchor=anchor, solid=True)
            return p_
        def wmark(i, col, txt, a, dy=-44, anchor="mm", dx=0):
            if not cam.vis(i) or cam.nb < i + 1: return
            p_ = (cam.x(i), cam.my(D["bw"][i])); circle(d, p_, 16, col, a)
            pill(d, (p_[0] + dx, p_[1] + dy), txt, a, col, 22, anchor=anchor, solid=True)
        if 31 <= t < 43: wmark(SQ1, GOLD, "Co thắt ~2,3%", on(31), dy=-40, anchor="lm", dx=20)
        if 37 <= t < 43: pmark(BRK_DN, D["c"][BRK_DN], RED, "Phá dải dưới", on(37), dy=48, anchor="rm", dx=-14)
        if 49 <= t < 60:
            for j, i in enumerate((44, 45, 50, 51)): pmark(i, D["c"][i], GREEN, None, on(49 + j * .2), r=14)
            pmark(51, D["h"][51], GREEN, "Bám dải trên", on(49.8), dy=-46, anchor="rm", dx=-10, r=1)
        if 66 <= t < 77: pmark(TOUCH, D["l"][TOUCH], ORANGE, "Chạm dải giữa", on(66), dy=48)
        if 72 <= t < 77:
            ae = on(72); xe = cam.x(ENTRY); ent = D["c"][ENTRY]; sl = 4020.0
            for val, txt, col in [(ent, f"Entry {vn(ent, 0)}", GOLD), (sl, "SL 4.020", RED)]:
                y_ = cam.py(val); x2 = xe + (cam.x(ENTRY - 6) - xe) * ae
                d.line([(x2, y_), (xe, y_)], fill=mix(col, ae), width=4)
                pill(d, (x2 - 10, y_ + (-24 if col == GOLD else 24)), txt, ae, col, 22, anchor="rm", solid=True)
        if 77 <= t < 84:
            wmark(SQ2, GOLD, "Co thắt ~3,5%", on(77), dy=-40, anchor="rm", dx=-20)
            pmark(BRK2, D["c"][BRK2], RED, "Đóng dưới dải dưới", prog(t, 80), dy=48, anchor="rm", dx=-14)
        if t >= 84:
            an = prog(t, 84); x = cam.x(N - 1); y = cam.py(D["c"][-1])
            pill(d, (x - 30, y + 64), "13/11 · 3.875,7", an, GOLD, 24, anchor="rm", solid=True)
            pill(d, (x - 30, cam.py(D["mid"][-1]) - 34), f"Dải giữa {vn(D['mid'][-1], 0)}", an, ORANGE, 22, anchor="rm", solid=True)
        # bottom box: term card or application caption
        if cap is None and term is not None:
            a = min(prog(tb, 0, .35), clamp((bd - tb) / .3)); term_card(d, term, a)
        elif cap:
            caption(d, tb, [(0.1, bd, CAPS[cap])])
    elif name == "check":
        im.paste(Image.blend(im, Image.new("RGB", (W, H), BG), .78 * prog(t, 0, .4))); d = ImageDraw.Draw(im); header(d, 2, title, sub)
        a = prog(t, .2)
        d.rounded_rectangle([40, 300, W - 40, 1400], 26, fill=mix(PANEL, a), outline=mix(GOLD, a), width=3)
        d.text((80, 350), "Dùng Bollinger Bands hiệu quả", font=F(46, "ExtraBold"), fill=mix(GOLD, a))
        items = ["Chạm dải **không phải** lệnh mua/bán",
                 "**Co thắt** báo sắp chạy mạnh, **không** báo hướng",
                 "Xu hướng mạnh: giá có thể **bám dải** rất lâu",
                 "Kết hợp **dải giữa** với cấu trúc giá",
                 "Vàng biến động mạnh: **luôn đặt Stop Loss**"]
        for i, it in enumerate(items):
            ai = prog(t, .8 + i * .9); y = 470 + i * 180
            d.ellipse([80, y, 130, y + 50], fill=mix(GREEN, ai))
            d.line([(93, y + 26), (103, y + 36), (119, y + 15)], fill=mix(BG, ai, GREEN), width=5)
            rich(d, 160, y + 2, it, F(40, "SemiBold"), W - 240, ai, 52)
        caption(d, t, [(5.6, 11.0, "Không chỉ báo nào đúng 100%. Dùng Bollinger Bands như **bộ lọc**, không phải nút bấm mua/bán.")])
    footer(d, gt)
    if name.startswith("card"):
        chapter_card(im, t, du, int(name[-1])); d = ImageDraw.Draw(im); footer(d, gt)
    return im


def render(out, t0, t1):
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(out + ".tmp.mp4", out)

def starts():
    acc = 0; out = {}
    for n, du in SC: out[n] = acc; acc += du
    return out
if __name__ == "__main__":
    if sys.argv[1] == "still":
        ts = [float(x) for x in sys.argv[2:]]
        ims = [frame(t) for t in ts]; sh = Image.new("RGB", (432 * len(ims), 768))
        for i, m in enumerate(ims): sh.paste(m.resize((432, 768)), (i * 432, 0))
        sh.save("stills.jpg", quality=85)
    elif sys.argv[1] == "info": print(TOTAL, starts())
    else: render(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))

