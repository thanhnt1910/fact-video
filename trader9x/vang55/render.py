"""Video dọc TikTok: Vàng lỗ 55 triệu/lượng. python render.py still t1 t2 ... | render out.mp4 t0 t1
Dòng thời gian đọc từ times.json [{id,start,dur}] (nếu thiếu thì ước lượng)."""
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
BG = (12, 14, 22); PANEL = (22, 26, 38); LINE = (44, 52, 70)
GOLD = (246, 192, 64); GOLD2 = (255, 224, 140); WHITE = (244, 246, 250); MUTED = (150, 160, 180)
RED = (240, 84, 84); GREEN = (46, 200, 132); BLUE = (80, 160, 255)
FD = "/usr/share/fonts/opentype/inter/"
_fc = {}
def F(sz, w="Bold"):
    k = (sz, w)
    if k not in _fc:
        fam = "InterDisplay-" if sz >= 60 else "Inter-"
        _fc[k] = ImageFont.truetype(FD + fam + w + ".otf", sz)
    return _fc[k]

# ---------- nội dung ----------
CH = {"h": "MỞ ĐẦU", "d": "01 · CƠN SỐT ĐỈNH", "l": "02 · LỊCH SỬ VÀNG SẬP", "c": "03 · KHOẢNG CHÊNH 16 TRIỆU",
      "p": "04 · HAI PHE", "k": "05 · NÊN LÀM GÌ"}
CAP = {
 "h1": "Cuối tháng 1, người ta xếp hàng từ sáng sớm để mua vàng. Vàng miếng lên **191 triệu**/lượng, **cao nhất lịch sử**.",
 "h2": "Giờ tiệm vàng chỉ mua lại **135 triệu**. Ai mua đúng đỉnh đang ~~lỗ hơn 55 triệu~~ mỗi lượng.",
 "h3": "Lạ hơn, vàng Việt Nam vẫn đắt hơn thế giới khoảng **16 triệu**/lượng. Tiền đó từ đâu ra, và có nên bắt đáy?",
 "d1": "Trong 1 năm tính tới cuối tháng 1, vàng thế giới gần như **tăng gấp đôi**. Ai chưa có vàng đều sợ mình bị bỏ lại.",
 "d2": "Ngày 29/1, vàng lập đỉnh **5.594 USD/ounce**. Hôm sau ~~rơi gần 10%~~ trong một phiên.",
 "d3": "Đó là cú giảm trong một ngày ~~mạnh nhất kể từ năm 1983~~.",
 "d4": "Vậy mà ở Việt Nam, người ta còn xếp hàng dài hơn. Ngày vía Thần Tài, có người xếp hàng từ **2–3 giờ sáng**.",
 "d5": "Giờ vàng thế giới chỉ còn quanh **3.900 USD**, ~~mất khoảng 30%~~ so với đỉnh.",
 "l1": "Vàng an toàn, nhưng **an toàn không có nghĩa là không sập**.",
 "l2": "Năm 1980, vàng lập đỉnh **850 USD** rồi rơi suốt hai thập kỷ. Người mua đỉnh chờ ~~hơn 20 năm~~.",
 "l3": "Năm 2011, vàng miếng lên **49 triệu**, rồi nằm quanh 35 triệu suốt ~~gần 9 năm~~.",
 "l4": "Lần nào trước khi sập, vàng cũng **tăng quá nóng**, và ai cũng tin nó còn tăng mãi.",
 "l5": "Khác biệt lần này: các **ngân hàng trung ương** vẫn mua vàng rất mạnh. Nên không ai dám chắc lịch sử sẽ lặp lại.",
 "c1": "Nhưng với người Việt, còn một rủi ro riêng. Đó là **khoảng chênh 16 triệu**.",
 "c2": "Từ năm 2012, Nhà nước **độc quyền sản xuất vàng miếng**, nên nguồn cung bị hạn chế suốt nhiều năm.",
 "c3": "Độc quyền đã bỏ từ **tháng 10/2025**. Nhưng nhập khẩu vẫn cần hạn mức và giấy phép, nên hàng chưa về nhiều.",
 "c4": "Năm nay khoảng chênh có lúc **gần 30 triệu**, có lúc **chỉ hơn 1 triệu**. Người mua đang cược cả vào một khoảng chênh lên xuống như tàu lượn.",
 "c5": "Khoảng chênh gồm: nguồn cung hạn chế, chênh mua bán **3–4 triệu**, chi phí thuế và vận chuyển, cộng tâm lý đám đông.",
 "p1": "**Phe thứ nhất:** tiền giấy năm nào cũng mất giá, còn vàng sập rồi cũng lên lại.",
 "p2": "~~Phe thứ hai:~~ mua lúc này là chấp nhận lỗ ngay từ đầu, vì phải trả thêm **16 triệu** so với thế giới.",
 "k1": "Câu hỏi đúng hơn là: nếu đây chưa phải đáy, **bạn chờ được bao lâu?**",
 "k2": "Người cẩn thận chỉ dùng **một phần nhỏ tài sản**, không vay để mua, và chia nhỏ ra mua nhiều lần.",
 "k3": "Hãy coi khoảng chênh như **đèn giao thông**. Chênh thấp thì dễ thở, chênh cao thì đứng lại, đừng chen.",
 "k4": "Đừng dùng tiền học, tiền chữa bệnh hay tiền cưới. Mua ở **nơi được cấp phép** và lấy hóa đơn.",
 "k5": "Vàng vẫn có thể là của để dành tốt. Nhưng không hiểu khoảng chênh và chu kỳ, bạn rất dễ thành **người mua đỉnh tiếp theo**.",
 "k6": "Đây không phải khuyến nghị đầu tư. **Bạn đang ở phe nào?** Để lại bình luận nhé.",
}
IDS = list(CAP)

def load_times():
    if os.path.exists("times.json"):
        return json.load(open("times.json"))
    cfg = json.load(open("/home/claude/fact-video/trader9x/vang55_cau.json"))
    t, out = 0.4, []
    for s in cfg["doan"]:
        d = len(s["text"].split()) / 3.4
        out.append({"id": s["id"], "start": t, "dur": d}); t += d + 0.25
    return out
TL = load_times()
TOTAL = TL[-1]["start"] + TL[-1]["dur"] + 1.6
SEG = {s["id"]: s for s in TL}

# ---------- tiện ích ----------
def ease(x): x = max(0., min(1., x)); return 1 - (1 - x) ** 3
def smooth(x): x = max(0., min(1., x)); return x * x * (3 - 2 * x)
def lerp(a, b, x): return a + (b - a) * x
def mix(c1, c2, a): return tuple(int(lerp(c1[i], c2[i], a)) for i in range(3))

def text_c(d, xy, s, f, fill, anchor="mm"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)

def fit(s, sz, maxw, w="Black"):
    while sz > 20 and F(sz, w).getlength(s) > maxw: sz -= 2
    return F(sz, w)

def rrect(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)

def parse_rich(s):
    """**vàng** ~~đỏ~~ → [(từ, màu)]"""
    state, words = None, []
    for tok in s.split(" "):
        txt, col = "", None
        i = 0
        while i < len(tok):
            m = tok[i:i+2]
            if m in ("**", "~~"):
                state = None if state else m; i += 2; continue
            if col is None: col = state
            txt += tok[i]; i += 1
        if txt:
            words.append((txt, GOLD if col == "**" else RED if col == "~~" else WHITE))
    return words

def _wid(f, ws): return f.getlength(" ".join(x[0] for x in ws))
def _two(f, ws, maxw):
    if _wid(f, ws) <= maxw * 0.62 or len(ws) < 4: return [ws] if _wid(f, ws) <= maxw else None
    best = None
    for i in range(2, len(ws) - 1):
        m = max(_wid(f, ws[:i]), _wid(f, ws[i:]))
        if m <= maxw and (best is None or m < best[0]): best = (m, i)
    return None if best is None else [ws[:best[1]], ws[best[1]:]]
def _split(f, ws, maxw):
    r = _two(f, ws, maxw)
    if r: return [r]
    n = len(ws); cands = [i for i in range(3, n - 2)]
    def score(i):
        return abs(i - n / 2) - (3 if ws[i - 1][0][-1] in ",:" else 0)
    i = min(cands, key=score)
    return _split(f, ws[:i], maxw) + _split(f, ws[i:], maxw)
def chunks(words, f, maxw):
    sents, cur = [], []
    for w in words:
        cur.append(w)
        if w[0][-1] in ".?!": sents.append(cur); cur = []
    if cur: sents.append(cur)
    out = []
    for st in sents: out += _split(f, st, maxw)
    return out

CAPF = F(54, "ExtraBold")
CAPCH = {k: chunks(parse_rich(v), CAPF, 930) for k, v in CAP.items()}

# ---------- nền ----------
def make_bg():
    im = Image.new("RGB", (W, H), BG)
    g = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(g)
    gd.ellipse((-300, -250, 900, 700), fill=70); gd.ellipse((500, 1200, 1500, 2200), fill=45)
    g = g.filter(ImageFilter.GaussianBlur(220))
    im = Image.composite(Image.new("RGB", (W, H), (70, 52, 14)), im, g)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line((x, 0, x, H), fill=(20, 23, 33))
    for y in range(0, H, 60): d.line((0, y, W, y), fill=(20, 23, 33))
    return im
BGIMG = make_bg()

# ---------- cảnh ----------
def card(d, box, title=None, col=GOLD):
    rrect(d, box, 28, fill=PANEL, outline=LINE, width=2)
    if title:
        x0, y0 = box[0] + 36, box[1] + 30
        f = F(30, "Bold"); tw = f.getlength(title)
        rrect(d, (x0, y0, x0 + tw + 32, y0 + 50), 12, fill=col)
        text_c(d, (x0 + 16, y0 + 25), title, f, BG, "lm")

def big_num(d, cx, cy, s, sz, col, a=1.0, maxw=860):
    f = fit(s, sz, maxw)
    text_c(d, (cx, cy), s, f, mix(BG, col, a))

def count(v0, v1, p): return lerp(v0, v1, ease(p))

def fmt(v, dec=0):
    s = f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s

def chart(d, box, pts, labels=None, col=GOLD, prog=1.0, ymin=None, ymax=None, fill=True, dots=()):
    x0, y0, x1, y1 = box
    ys = [p[1] for p in pts]; lo = ymin if ymin is not None else min(ys); hi = ymax if ymax is not None else max(ys)
    xs = [p[0] for p in pts]; xa, xb = min(xs), max(xs)
    P = [(x0 + (x - xa) / (xb - xa) * (x1 - x0), y1 - (y - lo) / (hi - lo) * (y1 - y0)) for x, y in pts]
    for k in range(5):
        yy = y0 + k * (y1 - y0) / 4; d.line((x0, yy, x1, yy), fill=LINE, width=1)
    n = (len(P) - 1) * prog; k = int(n); fr = n - k
    seg = P[:k + 1] + ([(lerp(P[k][0], P[k + 1][0], fr), lerp(P[k][1], P[k + 1][1], fr))] if k + 1 < len(P) else [])
    if fill and len(seg) > 1:
        d.polygon(seg + [(seg[-1][0], y1), (seg[0][0], y1)], fill=mix(PANEL, col, 0.18))
    if len(seg) > 1: d.line(seg, fill=col, width=7, joint="curve")
    for i, (px, py) in enumerate(P):
        if i <= n + 1e-6 and i in dots:
            d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=col, outline=WHITE, width=3)
    return P

def pill(d, xy, s, col, fg=BG, sz=32, anchor="mm"):
    f = F(sz, "ExtraBold"); tw = f.getlength(s); x, y = xy
    if anchor == "mm": x -= tw / 2 + 18
    elif anchor == "rm": x -= tw + 36
    rrect(d, (x, y - sz * 0.85, x + tw + 36, y + sz * 0.85), int(sz * 0.85), fill=col)
    text_c(d, (x + 18, y), s, f, fg, "lm")

def chip_row(d, y, items, prog):
    for i, (s, col) in enumerate(items):
        a = ease(prog * len(items) * 1.2 - i)
        if a <= 0: continue
        f = F(40, "ExtraBold")
        rrect(d, (110, y + i * 104, 970, y + i * 104 + 84), 20, fill=mix(PANEL, col, 0.22 * a), outline=mix(PANEL, col, a), width=3)
        d.ellipse((140, y + i * 104 + 28, 168, y + i * 104 + 56), fill=mix(PANEL, col, a))
        text_c(d, (192, y + i * 104 + 42), s, f, mix(PANEL, WHITE, a), "lm")

TOP, BOT = 250, 1180   # vùng hình chính
CX = W // 2

def scene(d, im, sid, p, lt):
    """p: tiến độ 0–1 trong đoạn, lt: giây kể từ đầu đoạn"""
    a = ease(lt / 0.5)
    if sid == "h1":
        card(d, (70, TOP, W - 70, BOT), "VÀNG MIẾNG · 29/01/2026")
        v = count(150, 191.3, lt / 1.6)
        big_num(d, CX, 600, fmt(v, 1), 230, GOLD, a)
        text_c(d, (CX, 760), "triệu đồng / lượng", F(48, "SemiBold"), MUTED)
        if lt > 1.5: pill(d, (CX, 900), "ĐỈNH CAO NHẤT LỊCH SỬ", GOLD, sz=40)
        # hàng người
        n = int(min(14, lt * 3))
        for i in range(n):
            x = 150 + i * 56; y = 1060
            d.ellipse((x, y - 70, x + 30, y - 40), fill=MUTED); rrect(d, (x - 4, y - 36, x + 34, y + 20), 12, fill=MUTED)
    elif sid == "h2":
        card(d, (70, TOP, W - 70, BOT), "GIÁ TIỆM MUA LẠI · 11/2026")
        text_c(d, (CX, 430), "191,3", F(110, "Black"), MUTED); d.line((CX - 170, 430, CX + 170, 430), fill=RED, width=8)
        text_c(d, (CX, 520), "↓", F(90, "Black"), RED)
        big_num(d, CX, 640, "135", 190, WHITE, a)
        text_c(d, (CX, 760), "triệu đồng / lượng", F(44, "SemiBold"), MUTED)
        if lt > 1.2:
            b = ease((lt - 1.2) / 0.5)
            big_num(d, CX, 950, "−" + fmt(count(0, 55, (lt - 1.2) / 1.2)) + " TRIỆU", 150, RED, b)
            text_c(d, (CX, 1070), "mỗi lượng, nếu mua đúng đỉnh", F(38, "SemiBold"), mix(PANEL, MUTED, b))
    elif sid == "h3":
        card(d, (70, TOP, W - 70, BOT), "VÀNG VN vs THẾ GIỚI (quy đổi)")
        base = 870; h1 = 420 * ease(lt / 0.8); h2 = 470 * ease(lt / 0.8)
        rrect(d, (220, base - h1, 460, base), 16, fill=BLUE); rrect(d, (620, base - h2, 860, base), 16, fill=GOLD)
        text_c(d, (340, base + 50), "Thế giới", F(40, "Bold"), MUTED); text_c(d, (740, base + 50), "Việt Nam", F(40, "Bold"), MUTED)
        if lt > 0.9:
            b = ease((lt - 0.9) / 0.5)
            d.line((620, base - 420, 860, base - 420), fill=mix(PANEL, WHITE, b), width=4)
            pill(d, (740, base - 445 - 70 * b), "+16 TRIỆU", RED, WHITE, sz=46)
        if p > 0.55:
            text_c(d, (CX, 1060), "Tiền đó từ đâu ra?", F(60, "Black"), mix(PANEL, GOLD, ease((p - .55) * 5)))
    elif sid == "d1":
        card(d, (70, TOP, W - 70, BOT), "VÀNG THẾ GIỚI · 12 THÁNG TỚI 01/2026")
        pts = [(0, 2.8), (1, 2.9), (2, 3.0), (3, 3.3), (4, 3.3), (5, 3.4), (6, 3.35), (7, 3.5), (8, 3.8), (9, 4.1), (10, 4.3), (11, 4.6), (12, 5.59)]
        chart(d, (140, 420, 940, 1000), pts, prog=ease(lt / 2.2), ymin=2.4, ymax=5.9, dots=(0, 12))
        big_num(d, CX, 400 + 0, "", 10, GOLD)
        if lt > 1.5: pill(d, (300, 380), "GẦN ×2", GOLD, sz=56)
        text_c(d, (CX, 1085), "đường minh họa xu hướng, không phải dữ liệu từng ngày", F(26, "Medium"), MUTED)
    elif sid in ("d2", "d3"):
        card(d, (70, TOP, W - 70, BOT), "ĐỈNH 29/01 → SẬP 30/01")
        pts = [(0, 5.05), (1, 5.2), (2, 5.33), (3, 5.594), (4, 5.05)]
        pr = 1 if sid == "d3" else ease(lt / 2.0) * 0.75 + (0.25 * ease((lt - 2.6) / 0.8) if lt > 2.6 else 0)
        P = chart(d, (160, 470, 920, 1000), pts, prog=pr, ymin=4.9, ymax=5.7, col=GOLD, fill=False, dots=(3,))
        pill(d, (P[3][0], P[3][1] - 60), "5.594 USD/oz", GOLD, sz=38)
        if pr > 0.97:
            d.line((P[4][0], P[4][1], P[4][0], P[4][1]), fill=RED)
            pill(d, (P[4][0] - 10, P[4][1] + 70), "≈ −10% / 1 phiên", RED, WHITE, sz=38, anchor="rm")
        if sid == "d3":
            b = ease(lt / 0.5)
            rrect(d, (150, 330, 930, 430), 22, fill=mix(PANEL, RED, b * 0.9))
            text_c(d, (CX, 380), "MẠNH NHẤT TỪ NĂM 1983", F(52, "Black"), mix(PANEL, WHITE, b))
    elif sid == "d4":
        card(d, (70, TOP, W - 70, BOT), "VÍA THẦN TÀI · 26/02/2026")
        # đồng hồ
        cx, cy, r = CX, 560, 190
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(30, 35, 50), outline=GOLD, width=10)
        for i in range(12):
            an = i / 12 * 2 * math.pi; d.line((cx + math.sin(an) * (r - 30), cy - math.cos(an) * (r - 30), cx + math.sin(an) * (r - 12), cy - math.cos(an) * (r - 12)), fill=MUTED, width=6)
        hr = 2 + min(1, lt / 2.5); ah = hr / 12 * 2 * math.pi; am = (hr % 1) * 2 * math.pi
        d.line((cx, cy, cx + math.sin(ah) * 100, cy - math.cos(ah) * 100), fill=WHITE, width=14)
        d.line((cx, cy, cx + math.sin(am) * 150, cy - math.cos(am) * 150), fill=GOLD, width=8)
        big_num(d, CX, 880, "2–3 GIỜ SÁNG", 110, WHITE, a)
        text_c(d, (CX, 990), "đã có người xếp hàng mua vàng", F(42, "SemiBold"), MUTED)
    elif sid == "d5":
        card(d, (70, TOP, W - 70, BOT), "VÀNG THẾ GIỚI HIỆN TẠI")
        big_num(d, CX, 520, fmt(count(5594, 3900, lt / 2.0)), 220, WHITE, 1)
        text_c(d, (CX, 670), "USD / ounce", F(48, "SemiBold"), MUTED)
        if lt > 1.6: big_num(d, CX, 880, "−30% TỪ ĐỈNH", 130, RED, ease((lt - 1.6) / .5))
    elif sid == "l1":
        card(d, (70, TOP, W - 70, BOT))
        text_c(d, (CX, 560), "AN TOÀN", F(140, "Black"), mix(PANEL, GREEN, a))
        text_c(d, (CX, 715), "≠", F(130, "Black"), WHITE)
        text_c(d, (CX, 870), "KHÔNG SẬP", F(140, "Black"), mix(PANEL, RED, ease((lt - .6) / .5)))
    elif sid == "l2":
        card(d, (70, TOP, W - 70, BOT), "LẦN SẬP 1 · 1980 → 1999")
        pts = [(1980, 850), (1982, 400), (1985, 320), (1988, 440), (1993, 360), (1996, 390), (1999, 252), (2002, 300), (2005, 450), (2008, 870)]
        P = chart(d, (150, 470, 930, 960), pts, prog=ease(lt / 3.0), ymin=150, ymax=950, dots=(0, 6, 9), col=GOLD)
        pill(d, (P[0][0] + 120, P[0][1] - 10), "850$", GOLD, sz=36)
        if lt > 1.8: pill(d, (P[6][0], P[6][1] + 60), "252$ · 1999", RED, WHITE, sz=34)
        if lt > 3.0: pill(d, (P[9][0] - 60, P[9][1] - 40), "hồi lại ~2008", GREEN, sz=32, anchor="rm")
        if p > 0.6: big_num(d, CX, 1080, "CHỜ HƠN 20 NĂM", 80, RED, ease((p - .6) * 5))
    elif sid == "l3":
        card(d, (70, TOP, W - 70, BOT), "LẦN SẬP 2 · VÀNG MIẾNG VN (triệu/lượng)")
        pts = [(2011, 49), (2012, 45), (2013, 38), (2014, 35), (2015, 34), (2016, 35), (2017, 36), (2018, 36), (2019, 42), (2020, 56)]
        P = chart(d, (150, 470, 930, 960), pts, prog=ease(lt / 3.0), ymin=25, ymax=60, dots=(0, 3, 9))
        pill(d, (P[0][0] + 110, P[0][1] - 10), "49 tr · 2011", GOLD, sz=34)
        if lt > 1.2: pill(d, (P[3][0], P[3][1] + 60), "≈35 tr", RED, WHITE, sz=34)
        if lt > 3: pill(d, (P[9][0], P[9][1] - 50), "8/2020", GREEN, sz=32, anchor="rm")
        if p > 0.55: big_num(d, CX, 1080, "GẦN 9 NĂM MỚI VỀ BỜ", 74, RED, ease((p - .55) * 5))
    elif sid == "l4":
        card(d, (70, TOP, W - 70, BOT), "ĐIỂM CHUNG TRƯỚC MỖI LẦN SẬP")
        chip_row(d, 470, [("1980: tăng quá nóng", GOLD), ("2011: tăng quá nhanh", GOLD), ("Ai cũng tin sẽ tăng mãi", RED)], ease(lt / 2.2))
        if lt > 2.4: text_c(d, (CX, 960), "2026: gần ×2 trong 1 năm", F(54, "Black"), mix(PANEL, WHITE, ease((lt - 2.4) / .5)))
    elif sid == "l5":
        card(d, (70, TOP, W - 70, BOT), "ĐIỂM KHÁC LẦN NÀY", GREEN)
        text_c(d, (CX, 450), "Ngân hàng trung ương mua ròng", F(44, "Bold"), MUTED)
        big_num(d, CX, 610, fmt(count(0, 321, lt / 1.5)) + " TẤN", 170, GREEN, a)
        text_c(d, (CX, 750), "riêng quý III/2026 · +42% so với cùng kỳ", F(40, "SemiBold"), WHITE)
        if p > 0.5: text_c(d, (CX, 960), "Lịch sử chưa chắc lặp lại y hệt", F(52, "Black"), mix(PANEL, GOLD, ease((p - .5) * 5)))
    elif sid == "c1":
        card(d, (70, TOP, W - 70, BOT), "RỦI RO RIÊNG CỦA NGƯỜI VIỆT", RED)
        s = 1 + 0.06 * math.sin(lt * 4) * (1 - ease(lt / 2))
        big_num(d, CX, 640, "+16 TRIỆU", int(190 * s), RED, a)
        text_c(d, (CX, 800), "đắt hơn thế giới mỗi lượng", F(46, "SemiBold"), MUTED)
    elif sid == "c2":
        card(d, (70, TOP, W - 70, BOT), "NĂM 2012 · NGHỊ ĐỊNH 24")
        big_num(d, CX, 500, "2012", 200, GOLD, a)
        chip_row(d, 680, [("Nhà nước độc quyền vàng miếng", GOLD), ("SJC: thương hiệu quốc gia", GOLD), ("Nhập khẩu bị kiểm soát chặt", RED)], ease(lt / 2.5))
    elif sid == "c3":
        card(d, (70, TOP, W - 70, BOT), "10/10/2025 · NGHỊ ĐỊNH 232", GREEN)
        chip_row(d, 430, [("Bỏ độc quyền vàng miếng", GREEN), ("Nhập khẩu: hạn mức hằng năm", RED), ("Giấy phép cho từng lần nhập", RED)], ease(lt / 2.6))
        if p > 0.6: text_c(d, (CX, 960), "Cửa đã mở, hàng chưa về nhiều", F(54, "Black"), mix(PANEL, GOLD, ease((p - .6) * 5)))
    elif sid == "c4":
        card(d, (70, TOP, W - 70, BOT), "CHÊNH VN – THẾ GIỚI 2026 (triệu/lượng)")
        pts = [(0, 30), (1, 12.4), (1.5, 1.2), (2, 20.6), (3, 4.3), (4, 16)]
        P = chart(d, (150, 460, 930, 1000), pts, prog=ease(lt / 3.5), ymin=0, ymax=34, col=GOLD, dots=(0, 2, 3, 4, 5))
        labs = [("≈30 · T3", GOLD), ("12 · đầu T6", GOLD), ("≈1 · giữa T6", GREEN), (">20 · cuối T6", RED), ("≈4,3 · cuối T8", GREEN), ("≈16 · nay", RED)]
        for i, (s, col) in enumerate(labs):
            if ease(lt / 3.5) * 5 >= i - 0.01 and i in (0, 2, 3, 5):
                off = -55 if i in (0, 3, 5) else 55
                pill(d, (min(max(P[i][0], 200), 880), P[i][1] + off), s, col, BG if col != RED else WHITE, sz=30)
        if p > 0.6: text_c(d, (CX, 1115), "Lên xuống như tàu lượn", F(46, "Black"), mix(PANEL, WHITE, ease((p - .6) * 5)))
    elif sid == "c5":
        card(d, (70, TOP, W - 70, BOT), "16 TRIỆU GỒM 4 MẢNH")
        items = [("1", "Nguồn cung hạn chế", GOLD), ("2", "Chênh mua–bán 3–4 tr", RED), ("3", "Chi phí thật: thuế, vận chuyển", BLUE), ("4", "Tâm lý đám đông", GREEN)]
        for i, (n, s, col) in enumerate(items):
            b = ease(lt * 1.3 - i * 0.9)
            if b <= 0: continue
            x = 110 + (i % 2) * 440; y = 420 + (i // 2) * 330
            rrect(d, (x, y, x + 420, y + 300), 24, fill=mix(PANEL, col, 0.2 * b), outline=mix(PANEL, col, b), width=4)
            text_c(d, (x + 210, y + 90), n, F(110, "Black"), mix(PANEL, col, b))
            words = s.split(" "); l1 = " ".join(words[:3]); l2 = " ".join(words[3:])
            text_c(d, (x + 210, y + 195), l1, fit(l1, 38, 380, "Bold"), mix(PANEL, WHITE, b))
            if l2: text_c(d, (x + 210, y + 245), l2, fit(l2, 38, 380, "Bold"), mix(PANEL, WHITE, b))
    elif sid in ("p1", "p2"):
        on1 = sid == "p1"
        for i, (t1, t2, col, ok) in enumerate([("PHE 1", "Vàng là chân ái", GREEN, on1), ("PHE 2", "Mua là lỗ từ đầu", RED, not on1)]):
            x = 90 + i * 460; y0 = TOP + 40
            k = 1.0 if ok else 0.35
            rrect(d, (x, y0, x + 440, BOT - 40), 28, fill=mix(BG, PANEL, k), outline=mix(BG, col, k), width=5 if ok else 2)
            text_c(d, (x + 220, y0 + 90), t1, F(64, "Black"), mix(BG, col, k))
            text_c(d, (x + 220, y0 + 180), t2, fit(t2, 44, 400, "ExtraBold"), mix(BG, WHITE, k))
            pts = ["Tiền giấy mất giá", "Sập rồi lại lên", "NHTW vẫn gom vàng"] if i == 0 else ["Trả thêm ~16 tr", "Chênh mua–bán 3–4 tr", "Vàng không trả lãi"]
            for j, s in enumerate(pts):
                yy = y0 + 330 + j * 150; bb = k * (ease((lt - 0.4 - j * 0.5) / 0.4) if ok else 1)
                rrect(d, (x + 30, yy - 50, x + 410, yy + 50), 18, fill=mix(BG, mix(PANEL, col, 0.18), bb))
                text_c(d, (x + 220, yy), s, fit(s, 34, 350, "Bold"), mix(BG, WHITE, bb))
    elif sid == "k1":
        card(d, (70, TOP, W - 70, BOT))
        text_c(d, (CX, 520), "Nếu chưa phải đáy…", F(70, "Black"), MUTED)
        big_num(d, CX, 700, "BẠN CHỜ", 150, GOLD, ease((lt - .6) / .5))
        big_num(d, CX, 870, "BAO LÂU?", 150, GOLD, ease((lt - 1.0) / .5))
    elif sid == "k2":
        card(d, (70, TOP, W - 70, BOT), "NGƯỜI CẨN THẬN THƯỜNG LÀM", GREEN)
        chip_row(d, 450, [("✓  Chỉ một phần nhỏ tài sản", GREEN), ("✓  Không vay để mua", GREEN), ("✓  Chia nhỏ, mua nhiều lần", GREEN)], ease(lt / 2.6))
    elif sid == "k3":
        card(d, (70, TOP, W - 70, BOT), "KHOẢNG CHÊNH = ĐÈN GIAO THÔNG")
        rrect(d, (390, 400, 690, 1000), 60, fill=(16, 18, 26), outline=LINE, width=4)
        g_on = p < 0.55; r_on = p >= 0.55
        d.ellipse((440, 440, 640, 640), fill=RED if r_on else (60, 26, 26))
        d.ellipse((440, 660, 640, 860), fill=GREEN if g_on else (20, 56, 40))
        text_c(d, (250, 540), "Chênh cao", F(40, "Bold"), RED if r_on else MUTED); text_c(d, (250, 590), "đứng lại", F(40, "Bold"), RED if r_on else MUTED)
        text_c(d, (850, 760), "Chênh thấp", F(40, "Bold"), GREEN if g_on else MUTED); text_c(d, (850, 810), "dễ thở hơn", F(40, "Bold"), GREEN if g_on else MUTED)
    elif sid == "k4":
        card(d, (70, TOP, W - 70, BOT), "ĐỪNG DÙNG TIỀN NÀY", RED)
        for i, s in enumerate(["Tiền học", "Chữa bệnh", "Tiền cưới"]):
            b = ease((lt - i * 0.4) / 0.4); x = 110 + i * 290
            rrect(d, (x, 420, x + 270, 560), 22, fill=mix(PANEL, RED, 0.25 * b), outline=mix(PANEL, RED, b), width=4)
            text_c(d, (x + 135, 490), s, F(42, "ExtraBold"), mix(PANEL, WHITE, b))
        if p > 0.45:
            b = ease((p - .45) * 5)
            rrect(d, (110, 680, 970, 1000), 26, fill=mix(PANEL, GREEN, 0.18 * b), outline=mix(PANEL, GREEN, b), width=4)
            text_c(d, (CX, 780), "Mua ở nơi được cấp phép", F(54, "Black"), mix(PANEL, WHITE, b))
            text_c(d, (CX, 880), "và lấy hóa đơn", F(54, "Black"), mix(PANEL, GREEN, b))
    elif sid == "k5":
        card(d, (70, TOP, W - 70, BOT), "TÓM LẠI")
        rows = [("−30%", "vàng thế giới từ đỉnh", RED), ("−55 tr", "mỗi lượng nếu mua đỉnh", RED), ("+16 tr", "chênh với thế giới", GOLD)]
        for i, (n, s, col) in enumerate(rows):
            b = ease((lt - i * 0.5) / 0.4); y = 450 + i * 160
            text_c(d, (330, y), n, F(84, "Black"), mix(PANEL, col, b), "rm")
            text_c(d, (370, y), s, F(42, "Bold"), mix(PANEL, WHITE, b), "lm")
        if p > 0.5: text_c(d, (CX, 1030), "Hiểu chênh & chu kỳ trước khi mua", F(48, "Black"), mix(PANEL, GOLD, ease((p - .5) * 5)))
    elif sid == "k6":
        card(d, (70, TOP, W - 70, BOT))
        text_c(d, (CX, 520), "BẠN Ở PHE NÀO?", F(110, "Black"), GOLD)
        for i, (s, col) in enumerate([("PHE 1 · Giữ vàng", GREEN), ("PHE 2 · Đứng ngoài", RED)]):
            b = ease((lt - .4 - i * .3) / .4)
            rrect(d, (140, 650 + i * 150, 940, 770 + i * 150), 60, fill=mix(PANEL, col, b))
            text_c(d, (CX, 710 + i * 150), s, F(50, "Black"), mix(PANEL, BG, b))
        text_c(d, (CX, 1060), "Bình luận cho mình biết nhé 💬"[:-2], F(40, "SemiBold"), MUTED)

def caption(d, sid, lt, dur):
    ch = CAPCH[sid]
    wc = [sum(len(w[0]) for ln in c for w in ln) for c in ch]; tot = sum(wc)
    acc, k = 0, 0
    for i, n in enumerate(wc):
        if lt < (acc + n) / tot * dur: k = i; break
        acc += n; k = i
    c = ch[k]; cstart = acc / tot * dur
    a = ease((lt - cstart) / 0.18)
    y0 = 1260 + (0 if len(c) == 2 else 38)
    for li, ln in enumerate(c):
        s = " ".join(w[0] for w in ln); tw = CAPF.getlength(s); x = (W - tw) / 2; y = y0 + li * 76 + (1 - a) * 14
        for w, col in ln:
            for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3), (2, 2), (-2, 2), (2, -2), (-2, -2)):
                d.text((x + dx, y + dy), w, font=CAPF, fill=(0, 0, 0))
            d.text((x, y), w, font=CAPF, fill=mix(BG, col, a))
            x += CAPF.getlength(w + " ")

def header(d, sid, t):
    rrect(d, (60, 120, 112, 172), 12, fill=GOLD); text_c(d, (86, 146), "Au", F(30, "Black"), BG)
    text_c(d, (130, 146), "TRADER9XVN", F(36, "Black"), WHITE, "lm"); text_c(d, (130 + F(36, "Black").getlength("TRADER9XVN") + 14, 148), "· GIÁ VÀNG", F(30, "Bold"), MUTED, "lm")
    text_c(d, (W - 60, 146), CH[sid[0]], F(28, "Bold"), GOLD, "rm")
    d.rectangle((60, 196, W - 60, 202), fill=(32, 38, 52)); d.rectangle((60, 196, 60 + (W - 120) * min(1, t / TOTAL), 202), fill=GOLD)
    text_c(d, (CX, 1680), "© trader9xvn · Nguồn: tổng hợp báo chí · Không phải khuyến nghị đầu tư", F(24, "Medium"), (120, 128, 146))

_WM = None
def watermark(im):
    global _WM
    if _WM is None:
        _WM = Image.new("RGBA", (W, H), (0, 0, 0, 0)); wd = ImageDraw.Draw(_WM)
        f = F(30, "ExtraBold"); s = "© trader9xvn"; tw = f.getlength(s)
        wd.text((W - 100 - tw, BOT - 58), s, font=f, fill=(255, 255, 255, 80))
    out = im.convert("RGBA"); out.alpha_composite(_WM); return out.convert("RGB")

def cur_seg(t):
    s = TL[0]
    for x in TL:
        if t >= x["start"] - 0.12: s = x
    return s

def frame(t):
    im = BGIMG.copy(); d = ImageDraw.Draw(im)
    s = cur_seg(t); sid = s["id"]; lt = t - s["start"]
    nxt = TL[TL.index(s) + 1]["start"] if s is not TL[-1] else TOTAL
    scene(d, im, sid, max(0, lt) / max(0.1, nxt - s["start"]), max(0, lt))
    if lt <= s["dur"] + 0.15: caption(d, sid, max(0, lt), s["dur"])
    header(d, sid, t)
    im = watermark(im)
    # chuyển cảnh chớp nhẹ ở đầu chương
    if TL.index(s) > 0 and TL[TL.index(s) - 1]["id"][0] != sid[0] and lt < 0.25:
        ov = Image.new("RGB", (W, H), BG); im = Image.blend(im, ov, 0.6 * (1 - lt / 0.25))
    if t > TOTAL - 0.8: im = Image.blend(im, Image.new("RGB", (W, H), BG), min(1, (t - TOTAL + 0.8) / 0.8))
    return im

if __name__ == "__main__":
    if sys.argv[1] == "still":
        for x in sys.argv[2:]:
            frame(float(x)).save(f"still_{x}.jpg", quality=88)
    elif sys.argv[1] == "info":
        print("tổng", round(TOTAL, 2))
    elif sys.argv[1] == "render":
        out, t0, t1 = sys.argv[2], float(sys.argv[3]), min(float(sys.argv[4]), TOTAL)
        tmp = out[:-4] + ".tmp.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            p.stdin.write(frame(i / FPS).tobytes())
        p.stdin.close()
        if p.wait() == 0: os.replace(tmp, out)
