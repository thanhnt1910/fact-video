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
OS_IN, OS_MIN, OS_OUT, MID_UP, OB_IN, MID_DN, OS2 = 26, 28, 31, 43, 50, 68, 80
PK1 = 48 + int(np.argmax(D["h"][48:56])); PK2 = 60 + int(np.argmax(D["h"][60:72]))
RPK1 = 44 + int(np.argmax(D["rsi"][44:58])); RPK2 = 58 + int(np.argmax(D["rsi"][58:72]))

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
        span = max(hi - lo, 60); pad = span * .14
        return lo - pad, hi + pad * 1.4
    def _mrange(s, a, b):
        return 0.0, 100.0
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

def draw_price(d, cam, a=1.0, ema_n=0, ema_a=1.0):
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
    if ema_n > 0 and ema_a > 0:
        series_line(d, cam, "e12", min(ema_n, N - 1), mix(BLUE, ema_a * a), 4, cam.py)
        series_line(d, cam, "e26", min(ema_n, N - 1), mix(ORANGE, ema_a * a), 4, cam.py)
    if nb > 0 and a > .5:
        li = min(N - 1, k if fr > 0 else k - 1)
        last = D["o"][li] + (D["c"][li] - D["o"][li]) * (fr if (fr > 0 and li == k) else 1)
        col = GREEN if last >= D["o"][li] else RED
        y = cam.py(last); dashed(d, (CX0, y), (CX1, y), mix(col, .6 * a), 1, 6)
        f = F(21, "Bold"); txt = vn(last, 2); tw = d.textlength(txt, font=f)
        d.rounded_rectangle([CX1 + 2, y - 17, CX1 + 16 + tw, y + 17], 6, fill=mix(col, a)); d.text((CX1 + 9, y), txt, font=f, fill=BG, anchor="lm")

def draw_macd(d, cam, a, hl=None, upto=None):
    """Panel RSI 14: mức 70/50/30, vùng quá mua/quá bán."""
    if a <= 0: return
    n = cam.nb if upto is None else upto
    d.rounded_rectangle([CX0 - 8, MY0 - 46, CX1 + 8, MY1 + 10], 16, fill=mix(PANEL, a), outline=mix(LINE, a), width=2)
    d.text((CX0 + 8, MY0 - 30), "RSI 14", font=F(22, "Bold"), fill=mix(MUTED, a), anchor="lm")
    li = max(0, min(N - 1, int(math.ceil(n)) - 1))
    if n > 0: d.text((CX0 + 100, MY0 - 30), vn(D["rsi"][li], 2), font=F(22, "Bold"), fill=mix(BLUE, a), anchor="lm")
    y70, y50, y30 = cam.my(70), cam.my(50), cam.my(30)
    ob_a = (.55 if hl == "ob" else .22) * a; os_a = (.55 if hl == "os" else .22) * a
    d.rectangle([CX0, cam.my(100), CX1, y70], fill=mix((70, 26, 30), ob_a / .55 * .9))
    d.rectangle([CX0, y30, CX1, cam.my(0)], fill=mix((16, 60, 44), os_a / .55 * .9))
    for lv, y, col, key in [(70, y70, RED, "ob"), (50, y50, GOLD if hl == "mid" else DIM, "mid"), (30, y30, GREEN, "os")]:
        w_ = 3 if hl == key else 1
        dashed(d, (CX0, y), (CX1, y), mix(col, a), w_, 10)
        d.text((CX1 + 12, y), str(lv), font=F(22, "Bold"), fill=mix(col if lv != 50 or hl == "mid" else MUTED, a), anchor="lm")
    if n <= 0: return
    la = a if hl in (None, "line", "ob", "os", "mid") else a
    series_line(d, cam, "rsi", min(n, N - 1), mix(BLUE, la), 5 if hl == "line" else 4, cam.my)

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


PARTS = {1: ("Định nghĩa", "RSI là gì?"), 2: ("Thuật ngữ & ứng dụng", "Học trên biểu đồ vàng thật")}
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
TERMS = [("Đường RSI", "Đường dao động từ **0 đến 100**, đo sức mạnh của các nhịp tăng so với nhịp giảm.", BLUE),
         ("Quá bán (dưới 30)", "RSI **dưới 30**: giá đã giảm quá nhanh, lực bán ~~có thể sắp cạn~~.", GREEN),
         ("Đường 50 (Midline)", "RSI **trên 50**: phe ++mua++ chiếm ưu thế. RSI **dưới 50**: phe ~~bán~~ chiếm ưu thế.", GOLD),
         ("Quá mua (trên 70)", "RSI **trên 70**: giá đã tăng quá nhanh, thị trường đang **nóng**.", RED),
         ("Phân kỳ (Divergence)", "Giá và RSI **đi ngược nhau**: giá đỉnh cao hơn, RSI đỉnh thấp hơn → động lượng **suy yếu**.", PURPLE)]
P2 = [  # (t0, term, caption or None)
    (0.0, 0, None), (7.0, 0, "r_app"),
    (13.0, 1, None), (19.0, 1, "os1"), (25.0, 1, "os2"), (31.0, 1, "entry"),
    (36.0, 2, None), (42.0, 2, "mid_up"),
    (48.0, 3, None), (54.0, 3, "ob1"), (60.0, 3, "ob2"),
    (66.0, 4, None), (72.0, 4, "div1"), (77.0, 4, "div2"), (82.0, 4, "div3"),
    (88.0, None, "now1"), (93.0, None, "now2"), (98.0, None, "now3")]
P2_DUR = 104.0
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
NB_P2 = [(0, 2), (12, 20), (13, 22), (19, 29), (25, 30), (30, 32), (36, 34), (42, 40), (47, 45), (54, 50), (60, 53), (66, 56), (72, 67), (82, 69), (87, 83), (93, 90)]
VS_P2 = [(0, 0), (36, 0), (47, 6), (60, 14), (72, 28), (87, 44), (93, 50)]
CAPS = {
 "r_app": "26–28/10 vàng hồi lên, đường RSI cũng **leo dần** từ gần 30 lên quanh **55**.",
 "os1": "30/10: vàng ~~sập về 3.871~~, RSI rơi xuống **22** – vùng **quá bán**.",
 "os2": "02/11: RSI **vượt lại lên trên 30** quanh **3.903** – thoát quá bán, lực mua ++quay lại++.",
 "entry": "Ví dụ: **vào lệnh** khi nến xác nhận đóng cửa, **SL** dưới đáy gần nhất (~3.860).",
 "mid_up": "04/11: RSI **vượt lên trên 50** quanh **3.971** → xu hướng tăng **được xác nhận**.",
 "ob1": "05/11: vàng lên **4.147,6**, RSI vọt lên **73** – vùng **quá mua**.",
 "ob2": "Quá mua **không phải lệnh bán ngay**: xu hướng mạnh có thể giữ RSI trên 70 khá lâu. Chờ xác nhận.",
 "div1": "10/11: giá lập đỉnh mới **4.149**, cao hơn đỉnh ngày 05/11…",
 "div2": "…nhưng RSI chỉ lên **65**, thấp hơn mức **73** → **phân kỳ giảm**.",
 "div3": "Cùng ngày 10/11 RSI **thủng 50**; đến 12/11 vàng ~~rơi về 3.853~~, RSI lại **dưới 30**.",
 "now1": "Hiện tại: phiên **13/11** đóng cửa quanh **3.876**, RSI khoảng **35**.",
 "now2": "RSI đã rời vùng quá bán nhưng vẫn **dưới 50** → phe bán còn chiếm ưu thế.",
 "now3": "Chờ RSI **vượt lại 50** để xác nhận. Đừng bắt đáy chỉ vì RSI từng xuống dưới 30.",
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
    d.text((x0, y0 + 100), "RSI", font=f, fill=mix(MUTED, a))
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
        d.text((W / 2, 920), "Tập sau: Bollinger Bands – đo biến động", font=F(38, "SemiBold"), fill=mix(WHITE, prog(t, .6)), anchor="mm")
        pill(d, (W / 2, 1040), "Theo dõi để không bỏ lỡ", prog(t, .9), GOLD, 34, solid=True)
        footer(d, gt)
        if t > du - .4: im = Image.blend(Image.new("RGB", (W, H)), im, clamp((du - t) / .4))
        return im
    ema_n, ema_a, ma, hl, part = 0, 1.0, 0, None, 1
    title, sub = "RSI là gì?", "Định nghĩa & cách tính"
    if name == "intro": cam = Cam(50, N); ma = 1
    elif name == "card1": cam = Cam(0, 2)
    elif name == "p1":
        nb = 2 + 12 * eio((t - .3) / 8.5); cam = Cam(0, nb); ma = prog(t, 3.5, .6) * (1 - prog(t, 10.2, .3))
    elif name == "card2": cam = Cam(0, 14); ma = 1
    elif name == "p2":
        part = 2; k, tb, bd = p2_beat(t); term = P2[k][1]
        cam = Cam(ramp(t, VS_P2), ramp(t, NB_P2)); ma = prog(t, 0, .5)
        hl = {0: "line", 1: "os", 2: "mid", 3: "ob"}.get(term) if term is not None else None
        if term is not None: title, sub = TERMS[term][0], f"Thuật ngữ {term + 1}/5 · ứng dụng trên XAUUSD"
        else: title, sub = "Hiện tại: vàng ~3.876", "RSI đang nói gì?"
    else:  # check
        cam = Cam(50, N); ma = 1; part = 2; title, sub = "Checklist", "Dùng RSI cho đúng"
    dimc = .25 if name == "intro" else 1.0
    draw_grid(d, cam, dimc)
    draw_price(d, cam, dimc, ema_n, ema_a)
    draw_macd(d, cam, ma * dimc, hl)
    if name == "intro":
        a = prog(t, .1, .5)
        im.paste(Image.blend(im, Image.new("RGB", (W, H), BG), .55)); d = ImageDraw.Draw(im)
        logo(d, W / 2 - 55, 520, 110, a)
        d.text((W / 2, 690), "TRADER9X MASTERCLASS", font=F(34, "Bold"), fill=mix(GOLD, a), anchor="mm")
        d.text((W / 2, 840), "RSI", font=F(260, "Black"), fill=mix(WHITE, prog(t, .3)), anchor="mm")
        d.text((W / 2, 1000), "Định nghĩa · Thuật ngữ & Ứng dụng", font=F(42, "SemiBold"), fill=mix(GOLD, prog(t, .6)), anchor="mm")
        d.text((W / 2, 1070), "Ví dụ thật trên Vàng XAU/USD", font=F(34, "Medium"), fill=mix(MUTED, prog(t, .8)), anchor="mm")
        if t > du - .3: im = Image.blend(Image.new("RGB", (W, H), BG), im, clamp((du - t) / .3))
        return im
    header(d, part, title, sub)
    if name == "p1":
        ab = prog(t, 10.5)
        if ab > 0:
            d.rounded_rectangle([CX0, MY0 - 20, CX1, MY1], 24, fill=mix(PANEL, ab), outline=mix(GOLD, ab), width=3)
            fb = F(56, "Black"); parts = [("RSI = 100 − ", WHITE), ("100 ÷ (1 + RS)", GOLD)]
            tw = sum(d.textlength(p_, font=fb) for p_, _ in parts); xx = (CX0 + CX1) / 2 - tw / 2
            for p_, c in parts: d.text((xx, MY0 + 70), p_, font=fb, fill=mix(c, ab), anchor="lm"); xx += d.textlength(p_, font=fb)
            fs = F(36, "Bold"); parts = [("RS = ", WHITE), ("TB tăng", GREEN), (" ÷ ", WHITE), ("TB giảm", RED), (" của 14 nến", MUTED)]
            tw = sum(d.textlength(p_, font=fs) for p_, _ in parts); xx = (CX0 + CX1) / 2 - tw / 2
            for p_, c in parts: d.text((xx, MY0 + 160), p_, font=fs, fill=mix(c, ab), anchor="lm"); xx += d.textlength(p_, font=fs)
            d.text(((CX0 + CX1) / 2, MY0 + 225), "Kết quả luôn nằm trong khoảng 0 – 100", font=F(30, "Medium"), fill=mix(MUTED, ab), anchor="mm")
        caption(d, t, [(.2, 3.5, "**RSI** – Relative Strength Index, chỉ số sức mạnh tương đối, do J. Welles Wilder giới thiệu năm 1978."),
                       (3.5, 10.5, "RSI đo **tốc độ và độ mạnh** của các nhịp giá: phe ++mua++ hay phe ~~bán~~ đang chiếm ưu thế."),
                       (10.5, 17.0, "Công thức so **trung bình nến tăng** với **trung bình nến giảm** của 14 nến, quy về thang **0 – 100**.")])
    elif name == "p2":
        k, tb, bd = p2_beat(t); term, cap = P2[k][1], P2[k][2]
        legend(d, 1, [("RSI 14", BLUE), ("Quá mua > 70", RED), ("Quá bán < 30", GREEN)], MY1 + 36)
        # persistent annotations (vị trí thật trên dữ liệu)
        def on(beat_t, d0=.5): return prog(t, beat_t, d0)
        def rmark(i, col, txt, a, dy=-48, anchor="mm", dx=0):
            if not cam.vis(i) or cam.nb < i + 1: return
            p_ = (cam.x(i), cam.my(D["rsi"][i])); circle(d, p_, 18, col, a)
            pill(d, (p_[0] + dx, p_[1] + dy), txt, a, col, 22, anchor=anchor, solid=True)
            return p_
        if 19 <= t < 48: rmark(OS_MIN, GREEN, "Quá bán · 22", on(19), dy=46, anchor="rm", dx=-10)
        if 25 <= t < 48:
            p_ = rmark(OS_OUT, GREEN, "Vượt lên 30", on(25), dy=-46, anchor="lm", dx=22)
            if p_: dashed(d, (p_[0], p_[1] - 20), (p_[0], cam.py(D["h"][OS_OUT]) + 14), mix(GREEN, on(25) * .6), 2, 8)
        if 31 <= t < 36:
            ae = on(31); xe = cam.x(OS_OUT); ent = D["c"][OS_OUT]; sl = 3860.0
            for val, txt, col in [(ent, f"Entry {vn(ent, 0)}", GOLD), (sl, "SL 3.860", RED)]:
                y_ = cam.py(val); x2 = xe + (cam.x(OS_OUT + 4) - xe) * ae
                d.line([(xe, y_), (x2, y_)], fill=mix(col, ae), width=4)
                pill(d, (x2 + 10, y_ + (-24 if col == GOLD else 24)), txt, ae, col, 22, anchor="lm", solid=True)
        if 42 <= t < 66: rmark(MID_UP, GOLD, "Vượt 50", on(42), dy=42, anchor="lm", dx=22)
        if 54 <= t < 66: rmark(RPK1, RED, "Quá mua · 73", on(54), dy=40)
        if 72 <= t < 88:
            ad = prog(t, 72, .9)
            p1, p2 = (cam.x(PK1), cam.py(D["h"][PK1]) - 12), (cam.x(PK2), cam.py(D["h"][PK2]) - 12)
            d.line([p1, (p1[0] + (p2[0] - p1[0]) * ad, p1[1] + (p2[1] - p1[1]) * ad)], fill=PURPLE, width=5)
            for pt in ((p1, p2) if ad >= 1 else (p1,)): d.ellipse([pt[0] - 8, pt[1] - 8, pt[0] + 8, pt[1] + 8], fill=PURPLE)
            pill(d, ((p1[0] + p2[0]) / 2, min(p1[1], p2[1]) - 40), "Giá: đỉnh cao hơn", prog(t, 72.5), PURPLE, 22, solid=True)
            if t >= 77:
                aq = prog(t, 77, .9)
                q1, q2 = (cam.x(RPK1), cam.my(D["rsi"][RPK1]) - 10), (cam.x(RPK2), cam.my(D["rsi"][RPK2]) - 10)
                d.line([q1, (q1[0] + (q2[0] - q1[0]) * aq, q1[1] + (q2[1] - q1[1]) * aq)], fill=PURPLE, width=5)
                for pt in ((q1, q2) if aq >= 1 else (q1,)): d.ellipse([pt[0] - 8, pt[1] - 8, pt[0] + 8, pt[1] + 8], fill=PURPLE)
                pill(d, ((q1[0] + q2[0]) / 2, cam.my(50) + 34), "RSI: 73 → 65 (thấp hơn)", prog(t, 77.5), PURPLE, 22, solid=True)
            if t >= 82:
                rmark(MID_DN, GOLD, "Thủng 50", on(82), dy=40, anchor="lm", dx=22)
                if cam.nb > OS2 + 1: rmark(OS2, GREEN, "Dưới 30", prog(t, 84), dy=-44)
        if t >= 93:
            an = prog(t, 88); x = cam.x(N - 1); y = cam.py(D["c"][-1])
            pill(d, (x - 30, y + 64), "13/11 · 3.875,7", an, GOLD, 24, anchor="rm", solid=True)
        if t >= 88:
            p_ = (cam.x(N - 1), cam.my(D["rsi"][-1])); circle(d, p_, 22, GOLD, prog(t, 88))
            pill(d, (p_[0] - 34, p_[1] - 40), f"RSI {vn(D['rsi'][-1], 1)}", prog(t, 88), GOLD, 22, anchor="rm", solid=True)
        # bottom box: term card or application caption
        if cap is None and term is not None:
            a = min(prog(tb, 0, .35), clamp((bd - tb) / .3)); term_card(d, term, a)
        elif cap:
            caption(d, tb, [(0.1, bd, CAPS[cap])])
    elif name == "check":
        im.paste(Image.blend(im, Image.new("RGB", (W, H), BG), .78 * prog(t, 0, .4))); d = ImageDraw.Draw(im); header(d, 2, title, sub)
        a = prog(t, .2)
        d.rounded_rectangle([40, 300, W - 40, 1400], 26, fill=mix(PANEL, a), outline=mix(GOLD, a), width=3)
        d.text((80, 350), "Dùng RSI hiệu quả", font=F(50, "ExtraBold"), fill=mix(GOLD, a))
        items = ["Quá mua / quá bán là **cảnh báo**, không phải lệnh",
                 "Ưu tiên tín hiệu **thuận xu hướng lớn**",
                 "Đường **50** giúp xác nhận xu hướng",
                 "**Phân kỳ** cần cấu trúc giá xác nhận",
                 "Vàng biến động mạnh: **luôn đặt Stop Loss**"]
        for i, it in enumerate(items):
            ai = prog(t, .8 + i * .9); y = 470 + i * 180
            d.ellipse([80, y, 130, y + 50], fill=mix(GREEN, ai))
            d.line([(93, y + 26), (103, y + 36), (119, y + 15)], fill=mix(BG, ai, GREEN), width=5)
            rich(d, 160, y + 2, it, F(40, "SemiBold"), W - 240, ai, 52)
        caption(d, t, [(5.6, 11.0, "Không chỉ báo nào đúng 100%. Dùng RSI như **bộ lọc**, không phải nút bấm mua/bán.")])
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

