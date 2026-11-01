"""Bảng cảnh video Nguyên Mông (nm5) bằng bản đồ vector: thời điểm từng đoạn theo giọng đọc thật -> spec_nm5.js (hình) + sfx_nm5.json (âm thanh).
Chạy: python phim_ban_do/vecmap/film_spec_nm2.py ; vẽ khung: SPEC_JS=spec_nm5.js SFX_JSON=sfx_nm5.json python phim_ban_do/vecmap/ve_film.py still <giây>..."""
import json, re, textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KB = json.load(open(ROOT / "ke-hoach/thu-giong-hai/nm5_full.json", encoding="utf-8"))
DUR = json.load(open(ROOT / "assets/thu_giong_hai/sadaltager/thoi_luong_nm5.json"))   # giọng gốc (chưa chuẩn hóa)
BASE = 34000
LEAD, GAP, TAIL = 1.0, 0.35, 4.0
S, D, TXT = {}, {}, {}
PS = []  # từng đoạn đọc giọng (đã tách câu): (bắt đầu, độ dài, chữ)
t = LEAD
for i, b in enumerate(KB, 1):
    d = DUR[str(b["n"])]
    PS.append((t, d, b["text"]))
    S[i] = t; D[i] = d; TXT[i] = b["text"]
    t += d + GAP
TOTAL = t + TAIL
A = lambda i, off=0.0: S[i] + off
E_ = lambda i: S[i] + D[i]

V, SO = "#c9742a", "#3a64a8"
BRN = "#6b5a45"
TL = (105.85, 21.03); VD = (107.45, 21.10); BLN = (105.44, 21.29); QH = (104.90, 21.72); BT = (106.36, 21.10)
CT = (105.15, 19.00); LS = (106.76, 21.85); VK = (106.38, 21.07); DM = (106.00, 20.58); TH = (105.78, 19.80)
HT = (106.02, 20.84); CD = (105.80, 20.98); TKT = (106.22, 20.70); BDG = (106.80, 20.95); LH = (106.35, 20.55); TM = (107.20, 22.35)
cam, items, sfx = [], [], []


KEEP = {6, 7, 42, 44, 51, 57, 59, 67}


def C(i, lon, lat, wd, off=0.0, hold=True):
    cam.append([A(i, off), lon, lat, wd] + ([1] if i in KEEP else []))
    if hold and D[i] > 3.0:
        cam.append([E_(i) - 1.2, lon, lat, wd])


def add(k, t0, t1=None, **kw):
    d = {"k": k, "t0": round(t0, 2)}
    if t1 is not None:
        d["t1"] = round(t1, 2)
    d.update(kw)
    items.append(d)
    return d


def fx(kind, t0, t1=None, **kw):
    d = {"s": kind, "t0": round(t0, 2)}
    if t1 is not None:
        d["t1"] = round(t1, 2)
    d.update(kw)
    sfx.append(d)


def city(name, p, side, i0, i1, fs=28, **kw):
    kw.setdefault("big", 1 if name in ("Thăng Long", "Vạn Kiếp", "Lạng Sơn") else 0)
    add("city", A(i0), E_(i1), lon=p[0], lat=p[1], name=name, side=side, fs=fs, fi=0.6, fo=0.6, **kw)


def card(title, sub, i, off=0.4, dur=3.4, col=V, **kw):
    add("card", A(i, off), min(A(i, off + dur), E_(i) - 0.1), title=title, sub=sub, col=col, fi=0.5, fo=0.5, **kw)


def chip(text, i0, i1, w=520):
    add("chip", A(i0), E_(i1), text=text, w=w, fi=0.6, fo=0.6, x=70, y=110)


def _cap(i, off, dur, t1_i=None):
    return round(max(1.6, min(dur, E_(t1_i or i) - A(i, off) - 0.5)), 2)


def route(rid, pts, col, i, off, dur, t1_i=None, w=6, fo=0.8, **kw):
    dur = _cap(i, off, dur, t1_i)
    add("route", A(i, off), E_(t1_i or i), id=rid, pts=[list(p) for p in pts], col=col, dur=dur, w=w, fi=0.2, fo=fo, **kw)


def army(pts, side, i, off, dur, n=12, t1_i=None, stay=True, flag=True, u="inf", col=None):
    dur = _cap(i, off, dur, t1_i)
    d = add("army", A(i, off), E_(t1_i or i), pts=[list(p) for p in pts], side=side, n=n, dur=dur, stay=stay, flag=flag, u=u, fi=0.2, fo=0.8)
    if col:
        d["col"] = col
    if u == "cav":
        fx("hoof", d["t0"], d["t0"] + dur)
    elif u == "ship":
        fx("water", d["t0"], d["t0"] + dur)


def lab(text, p, col, i0, i1, fs=46, op=0.6, **kw):
    add("label", A(i0), E_(i1), lon=p[0], lat=p[1], text=text, col=col, fs=fs, op=op, fi=0.8, fo=0.8, **kw)


def mark(shape, p, i, off=0.3, i1=None, **kw):
    add("mark", A(i, off), E_(i1 or i), shape=shape, lon=p[0], lat=p[1], fi=0.3, fo=0.5, **kw)


def defeat(p, side, i, off=0.5, t1_i=None, n=6):
    add("defeat", A(i, off), E_(t1_i or i) + 0.5, lon=p[0], lat=p[1], side=side, n=n, fi=0.2, fo=0.8)
    fx("gong", A(i, off) + 0.3)


def fire(p, t0, t1, s=18):
    add("fire", t0, t1, lon=p[0], lat=p[1], s=s, fi=0.6, fo=0.8)



def melee(p, i, off, t1_i=None, n=3, hits=True):
    t0, t1 = A(i, off), E_(t1_i or i)
    add("clash", t0, t1, lon=p[0], lat=p[1], n=n, c1=V, c2=SO, fi=0.3, fo=0.5)
    if hits:
        tt = t0
        while tt < t1 - 0.5:
            fx("clash", tt); tt += 1.6


def arrows(a, b, i, off, t1_i=None, n=12, col=None, h=60):
    t0, t1 = A(i, off), E_(t1_i or i)
    d = add("volley", t0, t1, a=list(a), b=list(b), n=n, h=h, sp=0.7, fi=0.3, fo=0.5)
    if col:
        d["col"] = col
    fx("arrow", t0, t1)


def shell(a, b, i, off, t1_i=None, n=4, h=90):
    t0, t1 = A(i, off), E_(t1_i or i)
    add("shell", t0, t1, a=list(a), b=list(b), n=n, h=h, sp=0.35, fi=0.3, fo=0.5)
    tt = t0 + 0.6
    while tt < t1 - 0.3:
        fx("drum", tt, tt + 1.0); tt += 2.8


def retreat(rid, pts, side, i, off, dur, t1_i=None, n=10, u="inf", col=None, dest=True):
    c = V if side == "v" else SO
    route(rid, pts, c, i, off, dur, t1_i=t1_i, w=6, arrow=True, chev=True)
    army(pts, side, i, off + 0.2, dur, n=n, t1_i=t1_i, flag=True, u=u, col=col)
    if dest:
        add("mark", A(i, off + dur * 0.8), E_(t1_i or i), shape="flag", lon=pts[-1][0], lat=pts[-1][1], s=26, col=c, fi=0.4, fo=0.6)
        add("ring", A(i, off + dur * 0.9), E_(t1_i or i), lon=pts[-1][0], lat=pts[-1][1], col=c, dur=1.8)




# vị trí bổ sung
NB = (106.25, 21.45); PL = (105.88, 21.20); VN = (102.6, 24.9); DL = (100.2, 25.6); NA = (105.6, 18.9); BC = (106.4, 17.7); TB = (106.35, 20.45); SC = (105.1, 21.9); BD = (105.86, 21.0)
RD = "#7a1f1f"
fmt = lambda: None

# ---------- hệ thống sông (vẽ trên bản đồ; thuyền chỉ được chạy trên sông hoặc biển) ----------
HONG = [(103.97, 22.45), (104.5, 22.0), (104.87, 21.72), (105.2, 21.45), (105.42, 21.30), (105.5, 21.17), (105.66, 21.10), (105.80, 21.07), (105.88, 20.98), (105.97, 20.82), (106.04, 20.66), (106.13, 20.52), (106.28, 20.35), (106.52, 20.24)]
DUONG = [(105.84, 21.05), (105.95, 21.09), (106.08, 21.10), (106.22, 21.10), (106.38, 21.08)]
CAU = [(105.85, 21.62), (105.95, 21.42), (106.10, 21.24), (106.28, 21.13), (106.38, 21.08)]
THUONG = [(106.76, 21.85), (106.62, 21.58), (106.50, 21.33), (106.42, 21.14), (106.38, 21.08)]
THAIBINH = [(106.38, 21.08), (106.45, 20.95), (106.52, 20.80), (106.60, 20.60), (106.68, 20.44), (106.72, 20.34)]
BACHDANG = [(106.38, 21.08), (106.52, 21.07), (106.63, 21.01), (106.73, 20.96), (106.82, 20.91), (106.88, 20.82), (106.93, 20.72), (107.0, 20.62)]
RIVERS = [{"id": "hong", "w": 3.8, "pts": HONG, "amb": 3}, {"id": "duong", "w": 2.6, "pts": DUONG, "amb": 1}, {"id": "cau", "w": 2.4, "pts": CAU, "amb": 1},
          {"id": "thuong", "w": 2.4, "pts": THUONG, "amb": 1}, {"id": "thaibinh", "w": 3.2, "pts": THAIBINH, "amb": 2}, {"id": "bachdang", "w": 3.4, "pts": BACHDANG, "amb": 2}]
rev = lambda l: list(reversed(l))
W_TL_BLN = [TL, (105.80, 21.07), (105.66, 21.10), (105.5, 21.17), BLN]
W_TL_DOWN = [TL, (105.88, 20.98), (105.97, 20.82), (106.04, 20.66), (106.13, 20.52)]
W_TL_SEA = [TL, (105.88, 20.98), (105.97, 20.82), (106.04, 20.66), (106.13, 20.52), (106.28, 20.35), (106.52, 20.24), (106.9, 20.0)]
W_BD = [(106.04, 20.66), (105.97, 20.82), (105.88, 20.98), (105.87, 21.0)]
W_TL_BT = [TL, (105.9, 21.07), (106.05, 21.10), (106.22, 21.10), BT]
W_CAU = [(106.38, 21.08), (106.28, 21.13), (106.16, 21.2)]
W_BD_UP = [(108.6, 20.72), (107.6, 20.72), (107.2, 20.72), (107.0, 20.62)] + rev(BACHDANG)[1:]
W_SEA_VD = [(107.95, 20.74), (107.7, 20.75), (107.5, 20.78)]

# ============ 1. Cái kho rỗng (1–6) ============
C(1, 105.95, 21.05, 1.2); C(2, 106.1, 21.15, 1.6); C(3, 106.0, 21.0, 2.4); C(4, 106.0, 21.0, 3.0); C(5, 106.0, 21.0, 3.0); C(6, 104.5, 23.2, 6.0)
city("Thăng Long", TL, "v", 1, 5, 30)
mark("flag", TL, 1, 0.3, 1, s=34, col=SO)
army([(105.55, 21.45), (105.7, 21.25), TL], "s", 1, 0.2, 4.0, n=14, t1_i=1, flag=True, u="inf")
add("big", A(1, 2.6), E_(1), text="KHO TRỐNG", col=RD, fi=0.5, fo=0.8, y=300, fs=150)
fx("march", A(1, 0.2), E_(1)); fx("gong", A(1, 2.6))
chip("Thăng Long, năm 1258", 2, 2, 560)
retreat("lui_ch", [TL, (105.7, 21.3), QH], "s", 2, 0.6, 5.0, n=10, u="cav", dest=False)
chip("Lần thứ hai, năm 1285", 3, 3, 620)
add("ring", A(3, 0.4), E_(3), lon=TL[0], lat=TL[1], col=SO, dur=1.8); add("ring", A(3, 2.4), E_(3), lon=TL[0], lat=TL[1], col=SO, dur=1.8)
add("big", A(4, 0.4), E_(4), text="BA LẦN", col=RD, fi=0.5, fo=0.8, y=340, fs=190); fx("drum", A(4, 0.3), E_(4))
add("big", A(5, 0.3), A(5, 3.0), text="?", col=RD, fi=0.4, fo=0.8, y=620, fs=300)

# ============ 2. Hai sứ giả (7–14) ============
city("Đại Lý", DL, "s", 6, 7, 26); city("Vân Nam", VN, "s", 6, 9, 26); city("Thăng Long", TL, "v", 8, 14, 28); lab("ĐẠI VIỆT", (105.3, 21.75), V, 8, 14, fs=46, op=0.55)
army([DL, (101.5, 25.3), VN], "s", 6, 0.6, 5.0, n=14, t1_i=7, flag=True, u="cav")
C(7, 103.3, 24.2, 4.8); C(8, 105.2, 22.0, 4.2); C(9, 103.8, 23.8, 4.4); C(10, 105.3, 22.0, 4.0); C(12, 105.3, 22.0, 4.0); C(14, 105.0, 22.2, 5.2)
card("Trần Thái Tông", "vua nhà Trần", 8, 0.8, 3.2); card("Trần Thủ Độ", "người nắm quyền trong triều", 8, 3.6, 3.0)
card("Ngột Lương Hợp Thai", "tướng Mông Cổ ở Vân Nam", 9, 0.4, 3.4, col=SO)
route("su", [VN, (104.0, 23.5), (105.0, 22.5)], SO, 10, 0.4, 4.0, t1_i=10, w=5, arrow=True)
army([VN, (104.0, 23.5), (105.0, 22.5)], "s", 10, 0.6, 4.0, n=2, t1_i=10, flag=True, u="cav", stay=False)
add("mark", A(11, 0.6), E_(11), shape="q", lon=105.0, lat=22.5, s=44, fi=0.3, fo=0.5)
chip("Hai sứ giả không trở về", 11, 11, 700)
fx("hoof", A(10, 0.6), E_(10))

# ============ 3. Chín ngày ở Thăng Long (15–30) ============
C(15, 105.0, 22.0, 3.2); C(16, 105.4, 21.4, 1.4); C(17, 105.7, 21.2, 1.0); C(18, 105.9, 21.05, 0.9); C(20, 105.95, 21.0, 1.1); C(22, 105.85, 21.0, 0.8); C(24, 105.9, 21.0, 0.9); C(25, 105.9, 21.0, 0.9); C(27, 105.4, 21.5, 2.0); C(29, 105.9, 21.0, 2.0)
city("Bình Lệ Nguyên", BLN, "v", 15, 16, 26); city("Phù Lỗ", PL, "v", 17, 17, 26); city("Thăng Long", TL, "v", 15, 30, 28); city("Đông Bộ Đầu", BD, "v", 25, 26, 24); city("Quy Hóa", QH, "v", 27, 27, 26)
army([QH, (105.2, 21.55), BLN], "s", 15, 0.4, 5.0, n=16, t1_i=16, flag=True, u="cav")
chip("Đầu năm 1258", 16, 16, 560)
army(W_TL_BLN, "v", 16, 0.8, 4.0, n=10, t1_i=16, flag=True, u="ship")
melee(BLN, 16, 2.6, 16); defeat(BLN, "v", 16, 3.9, 16, 5); card("Trần Thái Tông", "ra trận, quân Đại Việt thua", 16, 0.4, 2.2)
arrows(BLN, PL, 17, 0.3, 17, 10, col="#cfe0ff"); melee(PL, 17, 1.2, 17)
route("tien1258", [BLN, PL, TL], SO, 17, 0.2, 4.0, t1_i=17, w=5, arrow=True)
add("big", A(18, 0.3), A(18, 2.8), text="?", col=RD, fi=0.4, fo=0.8, y=600, fs=260)
card("Trần Thủ Độ", "đầu thần chưa rơi xuống đất", 19, 0.4, 3.6, w=900)
retreat("rutvua", W_TL_DOWN, "v", 20, 0.6, 5.0, n=10, u="ship")
chip("Vườn không nhà trống", 21, 21, 700)
army([(105.6, 21.5), (105.75, 21.25), TL], "s", 22, 0.4, 4.0, n=16, t1_i=23, flag=True, u="inf")
add("big", A(22, 3.0), E_(22), text="KHO TRỐNG", col=RD, fi=0.5, fo=0.8, y=300, fs=140); fx("gong", A(22, 3.0))
add("big", A(24, 0.3), E_(24), text="9 NGÀY", col=RD, fi=0.5, fo=0.8, y=560, fs=190); fx("drum", A(24, 0.3), E_(24))
army(W_BD, "v", 25, 0.3, 4.0, n=12, t1_i=26, flag=True, u="ship")
melee(BD, 25, 2.2, 26); arrows((105.95, 20.88), BD, 25, 1.4, 26, 12); defeat((105.9, 21.12), "s", 26, 1.2, 26, 6)
retreat("rut1258", [TL, (105.5, 21.4), QH], "s", 27, 0.4, 5.0, n=10, u="cav")
arrows((105.45, 21.42), (105.25, 21.52), 27, 2.4, 27, 10); melee((105.15, 21.55), 27, 3.2, 27, n=2)
chip("Hai bên đều nhận phần thắng", 29, 29, 800)
chip("Nhường ngôi cho thái tử, vua Trần Thánh Tông", 30, 30, 1000)

# ============ 4. Quả cam và tiếng đánh (31–42) ============
C(31, 106.0, 21.5, 4.5); C(32, 106.0, 21.0, 4.5); C(34, 106.2, 21.8, 2.6); C(35, 106.4, 21.2, 0.8); C(37, 106.5, 21.8, 3.0); C(38, 106.3, 21.6, 3.0); C(40, 105.9, 21.1, 1.2); C(41, 105.9, 21.1, 1.2); C(42, 107.4, 18.3, 6.0)
chip("Hơn hai mươi năm sau", 31, 31, 640)
city("Chiêm Thành", CT, "v", 32, 32, 26); city("Lạng Sơn", LS, "v", 32, 38, 26); city("Bình Than", BT, "v", 35, 36, 26); city("Thăng Long", TL, "v", 38, 41, 28)
route("duongbo", [(107.0, 22.6), LS, TL, (105.8, 20.0), CT], SO, 32, 0.4, 6.0, t1_i=32, w=5, arrow=True)
army([(107.0, 22.6), LS, (106.4, 21.5)], "s", 33, 0.3, 4.0, n=3, t1_i=34, flag=True, u="cav", col=BRN)
retreat("diai", [(106.4, 21.5), LS, (107.0, 22.6)], "s", 34, 0.4, 4.0, n=3, u="cav", col=BRN, dest=False)
chip("Cuối năm 1282, hội nghị Bình Than", 35, 35, 860)
army(W_TL_BT, "v", 35, 0.4, 5.0, n=8, t1_i=36, flag=True, u="ship")
card("Trần Quốc Toản", "quả cam bị bóp nát, theo giai thoại", 36, 0.4, 4.2, w=1000)
chip("Năm 1284", 37, 37, 400)
army([(107.2, 22.4), LS], "s", 37, 0.3, 4.0, n=16, t1_i=38, flag=True, u="cav")
card("Thoát Hoan", "con trai Hốt Tất Liệt", 37, 2.6, 3.2, col=SO)
add("ring", A(40, 0.4), A(40, 3.0), lon=TL[0], lat=TL[1], col=V, dur=1.6); add("ring", A(40, 1.6), E_(40), lon=TL[0], lat=TL[1], col=V, dur=1.6)
card("Điện Diên Hồng", "các cụ già đồng thanh: đánh", 40, 0.4, 4.0, w=1000); fx("horn", A(40, 0.3))
card("Trần Quốc Tuấn", "Hưng Đạo Vương, chỉ huy toàn quân", 41, 0.4, 3.8, w=900)
army([(108.2, 19.3), (108.5, 17.6), (109.3, 15.2)], "s", 42, 0.4, 5.0, n=10, t1_i=42, flag=True, u="ship"); card("Toa Đô", "tướng nhà Nguyên ở phía nam", 42, 2.8, 3.2, col=SO)

# ============ 5. Quân Nguyên vào nhà (43–70) ============
C(43, 106.4, 21.8, 2.6); C(44, 105.9, 20.0, 6.0); C(45, 106.3, 21.6, 1.8); C(47, 106.2, 21.35, 1.5); C(49, 106.1, 21.1, 2.6); C(50, 106.0, 21.1, 1.8); C(51, 106.1, 20.7, 3.0); C(52, 106.0, 20.6, 1.4); C(55, 105.9, 21.0, 1.6); C(57, 105.8, 19.8, 4.5); C(59, 106.0, 20.8, 1.8); C(62, 105.95, 20.85, 0.9); C(64, 105.9, 21.0, 1.2); C(66, 106.0, 21.2, 2.4); C(68, 106.2, 21.2, 3.2)
chip("27 tháng 1 năm 1285", 43, 43, 700)
city("Lạng Sơn", LS, "v", 43, 44, 26); city("Nội Bàng", NB, "v", 45, 45, 26); city("Vạn Kiếp", VK, "v", 46, 47, 26); city("Thăng Long", TL, "v", 44, 70, 28)
army([(107.2, 22.5), LS, NB, (106.3, 21.3)], "s", 43, 0.4, 7.0, n=20, t1_i=47, flag=True, u="cav")
route("chay", [SC, (105.6, 21.6), (106.0, 21.35)], SO, 44, 0.4, 4.0, t1_i=44, w=5, arrow=True)
route("toado1285", [BC, (105.95, 18.4), NA, TH, (105.9, 20.3), DM], SO, 44, 1.6, 6.0, t1_i=44, w=5, arrow=True, chev=True)
army([BC, (105.95, 18.4), NA, TH], "s", 44, 1.8, 6.0, n=12, t1_i=44, flag=True, u="inf")
add("big", A(44, 3.0), E_(44), text="HAI PHÍA", col=RD, fi=0.5, fo=0.8, y=560, fs=140)
melee(NB, 45, 1.0, 45); defeat(NB, "v", 45, 2.6, 45, 5); chip("Ải Nội Bàng, đầu tháng hai", 45, 45, 800)
retreat("luiVK", [NB, (106.35, 21.3), VK], "v", 46, 0.4, 4.0, n=10, u="inf")
army(W_CAU, "s", 47, 0.3, 3.5, n=10, t1_i=47, flag=True, u="ship"); melee((106.3, 21.12), 47, 1.2, 47)
defeat((106.3, 21.16), "v", 48, 0.6, 48, 6)
add("mark", A(49, 0.8), E_(49), shape="q", lon=106.2, lat=21.1, s=44, fi=0.3, fo=0.5)
route("duong", [VK, (106.1, 21.1), TL], SO, 50, 0.3, 4.0, t1_i=50, w=6, arrow=True, chev=True)
army([VK, (106.1, 21.1), TL], "s", 50, 0.5, 4.0, n=18, t1_i=50, flag=True, u="inf")
retreat("luibien", W_TL_SEA, "v", 51, 0.4, 5.0, n=10, u="ship", dest=False)
melee(DM, 52, 1.0, 52); card("Trần Bình Trọng", "chặn giặc ở bãi Đà Mạc", 52, 0.4, 3.4); city("Đà Mạc", DM, "v", 52, 54, 26)
mark("x", DM, 54, 0.4, 54); fx("gong", A(54, 0.4))
chip("Lần thứ hai: kho đã trống", 55, 55, 760); add("ring", A(55, 1.0), E_(55), lon=TL[0], lat=TL[1], col=SO, dur=1.8)
fire((TL[0] + .1, TL[1] + .06), A(56, 0.5), E_(56), 14); chip("Vườn không nhà trống", 56, 56, 700)
army([BC, (105.95, 18.4), NA, (105.5, 19.6), TH], "s", 57, 0.4, 6.0, n=12, t1_i=58, flag=True, u="cav")
city("Nghệ An", NA, "v", 57, 58, 26); city("Thanh Hóa", TH, "v", 57, 59, 26)
add("big", A(59, 0.2), A(59, 2.0), text="?", col=RD, fi=0.3, fo=0.6, y=600, fs=260)
chip("Thiếu lương, thiếu nước sạch, bệnh tật", 60, 60, 900); add("sick", A(60, 0.2), E_(60) + 1.0, fi=1.0, fo=1.5)
chip("Giữa năm 1285: quân Trần phản công", 61, 61, 900)
city("Hàm Tử", HT, "v", 62, 62, 26); city("Tây Kết", TKT, "v", 63, 63, 26); city("Chương Dương", CD, "v", 64, 66, 26)
army([(106.15, 20.8), HT], "v", 62, 0.3, 3.0, n=12, t1_i=62, flag=True, u="inf"); melee(HT, 62, 1.6, 62); card("Trần Nhật Duật", "đánh quân của Toa Đô", 62, 0.3, 3.0)
melee(TKT, 63, 0.8, 63); mark("x", TKT, 63, 2.0, 63); fx("gong", A(63, 2.0))
arrows((105.95, 21.02), (105.84, 20.99), 64, 0.6, 65, 12); melee(CD, 64, 1.6, 65); card("Trần Quang Khải", "dẫn quân chủ lực", 64, 0.3, 3.0)
retreat("luiNguyen", [CD, (105.7, 21.4), LS], "s", 66, 0.4, 5.0, n=12, u="inf", dest=False)
retreat("OMN", W_TL_SEA, "s", 67, 0.4, 5.0, n=4, u="ship", dest=False)
add("big", A(68, 0.4), E_(68), text="6 THÁNG", col=RD, fi=0.5, fo=0.8, y=520, fs=170)

# ============ 6. Lần thứ ba: chuẩn bị (71–77) ============
C(71, 106.5, 21.3, 4.5); C(73, 107.0, 21.4, 3.6); C(75, 107.4, 21.0, 2.6); C(77, 106.2, 21.1, 2.4)
chip("Năm 1286: Trần Ích Tắc được phong vua An Nam", 71, 71, 1100); chip("Cuối năm 1287", 73, 73, 560)
card("Hốt Tất Liệt", "hoãn việc đánh Nhật Bản", 72, 0.4, 3.4, col=SO)
route("bo3", [(107.0, 22.5), LS, (106.6, 21.5), VK], SO, 73, 0.3, 8.0, t1_i=74, w=6, arrow=True, chev=True)
route("thuy3", W_BD_UP, SO, 73, 0.5, 11.0, t1_i=74, w=6, arrow=True, chev=True)
army([(107.0, 22.5), LS, (106.6, 21.5), VK], "s", 73, 0.4, 8.0, n=18, t1_i=75, flag=True, u="cav")
army(W_BD_UP, "s", 73, 0.6, 11.0, n=14, t1_i=75, flag=True, u="ship")
card("Thoát Hoan", "đạo quân đi bộ", 74, 0.3, 3.0, col=SO); card("Ô Mã Nhi", "đạo quân đi thuyền", 74, 3.2, 3.0, col=SO)
city("Vạn Kiếp", VK, "v", 74, 74, 26)
army([(109.3, 20.7), (108.4, 20.74), (107.7, 20.75)], "s", 75, 0.3, 7.0, n=10, t1_i=75, flag=True, u="ship", col=BRN)
card("Trương Văn Hổ", "chỉ huy đoàn thuyền chở lương", 75, 2.4, 3.4, col=SO)
fx("march", A(73, 0.3), E_(75)); fx("water", A(73, 0.5), E_(75)); fx("horn", A(73, 0.2))
card("Trần Quốc Tuấn", "lại được giao chỉ huy toàn quân", 77, 0.4, 3.6)

# ============ 7. Vân Đồn (78–85) ============
C(78, 106.4, 21.2, 3.2); C(79, 107.45, 21.1, 1.6); C(80, 107.45, 21.1, 1.2); C(82, 107.45, 21.1, 1.2); C(83, 107.55, 21.05, 1.0); C(85, 107.2, 21.0, 2.4)
city("Vân Đồn", VD, "v", 79, 85, 28)
card("Trần Khánh Dư", "từng bị lấy hết của cải", 78, 0.4, 3.6)
army(W_SEA_VD, "s", 80, 0.3, 4.0, n=8, t1_i=80, flag=True, u="ship")
route("goive", [VD, (106.9, 21.2), TL], V, 80, 2.4, 4.0, t1_i=80, w=5, arrow=True)
add("big", A(81, 0.3), A(81, 2.6), text="?", col=RD, fi=0.4, fo=0.8, y=620, fs=260)
army([(108.9, 20.7), (108.2, 20.74), (107.75, 20.75)], "s", 82, 0.3, 5.0, n=10, t1_i=83, flag=True, u="ship", col=BRN)
chip("Khoảng tháng giêng năm 1288", 83, 83, 800)
army([(107.42, 20.8), (107.52, 20.77), (107.66, 20.75)], "v", 83, 0.4, 3.5, n=10, t1_i=84, flag=True, u="ship")
arrows((107.35, 21.14), (107.62, 21.02), 83, 1.0, 84, 14); melee((107.66, 21.0), 83, 1.8, 84)
fire((107.7, 21.0), A(84, 0.4), E_(84), 16); fx("fire", A(84, 0.4), E_(84))
mark("x", (107.68, 21.0), 84, 0.8, 84); mark("x", (107.74, 21.0), 84, 1.4, 84)
card("Trương Văn Hổ", "chạy thoát chỉ với một chiếc thuyền", 84, 2.0, 3.4, col=SO)
chip("Quân Nguyên mất nguồn lương", 85, 85, 760)

# ============ 8. Thăng Long lần thứ ba (86–96) ============
C(86, 106.0, 21.1, 2.6); C(88, 106.4, 20.55, 1.8); C(90, 106.4, 21.2, 2.4); C(92, 106.7, 21.4, 3.0); C(94, 106.6, 21.7, 2.2); C(95, 106.78, 21.85, 1.6); C(96, 107.0, 22.2, 3.0)
city("Thăng Long", TL, "v", 86, 89, 28); city("Thái Bình", TB, "v", 88, 88, 24); city("Vạn Kiếp", VK, "v", 90, 92, 26); city("Lạng Sơn", LS, "v", 92, 96, 26); city("Bạch Đằng", BDG, "v", 92, 97, 26)
army([VK, (106.2, 21.1), TL], "s", 86, 0.3, 4.0, n=14, t1_i=87, flag=True, u="inf")
chip("Lần thứ ba: kinh thành vắng người", 86, 86, 860)
add("ring", A(87, 0.6), E_(87), lon=TL[0], lat=TL[1], col=SO, dur=1.8); add("big", A(87, 2.0), E_(87), text="CHỜ THUYỀN LƯƠNG", col=RD, fi=0.5, fo=0.8, y=300, fs=110)
route("long", [TL, (106.1, 20.6), TB], SO, 88, 0.3, 4.0, t1_i=88, w=4, arrow=True)
arrows((106.4, 21.1), (106.2, 21.0), 89, 0.5, 89, 10); add("sick", A(90, 0.0), E_(90), fi=0.8, fo=1.0)
chip("Ngày 5 tháng 3: rút về Vạn Kiếp", 90, 90, 900)
retreat("rutVK", [TL, (106.2, 21.1), VK], "s", 90, 1.0, 4.0, n=14, u="inf")
card("Thoát Hoan", "họp các tướng, quyết định rút", 91, 0.3, 3.4, col=SO)
route("duongbo2", [VK, (106.5, 21.5), LS], SO, 92, 0.4, 4.0, t1_i=93, w=6, arrow=True, chev=True)
route("duongthuy2", [VK, (106.6, 21.1), BDG], SO, 92, 0.6, 4.0, t1_i=93, w=6, arrow=True, chev=True)
army([VK, (106.5, 21.5), LS], "s", 94, 0.3, 4.0, n=14, t1_i=95, flag=True, u="cav")
defeat((106.45, 21.4), "s", 94, 1.0, 94, 4); defeat((106.62, 21.62), "s", 94, 2.4, 94, 4); arrows((106.4, 21.5), (106.5, 21.45), 94, 1.2, 94, 8)
add("ring", A(95, 1.6), E_(95), lon=LS[0], lat=LS[1], col="#b3261e", dur=1.6); fx("clash", A(95, 1.6)); card("Thoát Hoan", "trúng mũi tên tẩm độc, theo sử chép", 95, 0.3, 3.4, col=SO, w=1000)
chip("Rút qua núi biên giới", 96, 96, 700)

# ============ 9. Cọc trên sông Bạch Đằng (97–107) ============
RIV = [(106.40, 21.10), (106.52, 21.07), (106.63, 21.01), (106.73, 20.96), (106.82, 20.91), (106.88, 20.82), (106.93, 20.72), (107.0, 20.62)]
STK = [(106.69, 20.985), (106.72, 20.965), (106.745, 20.955), (106.765, 20.94), (106.785, 20.93), (106.80, 20.92), (106.815, 20.905), (106.835, 20.89), (106.70, 20.96), (106.73, 20.98), (106.76, 20.955), (106.79, 20.915), (106.82, 20.90)]
C(97, 106.74, 20.97, 1.1); C(100, 106.74, 20.97, 0.95); C(104, 106.78, 20.94, 1.1); C(106, 106.7, 21.0, 1.0); C(107, 106.5, 21.0, 2.4)
chip("Sông Bạch Đằng, ngày 9 tháng 4 năm 1288", 97, 97, 1000)
add("tide", A(97), E_(105) + 1.5, pts=[list(p) for p in RIV], stakes=[list(p) for p in STK], w=16, show=2.0,
    lv=[[A(97), 1.0], [A(99, 0.5), 1.0], [A(101, 0.0), 0.95], [A(102, 3.0), 0.9], [A(103, 1.0), 0.08], [E_(105), 0.08], [E_(105) + 1.5, 0.5]], fi=0.6, fo=0.8)
army(rev(BACHDANG)[:6], "s", 101, 0.2, 10.0, n=16, t1_i=105, flag=True, u="ship")
army([(106.63, 21.01), (106.82, 20.91), (106.88, 20.82), (106.73, 20.96)], "v", 102, 0.4, 8.0, n=6, t1_i=103, flag=True, u="ship")
add("big", A(98, 0.3), A(98, 3.0), text="CỌC GỖ", col=RD, fi=0.4, fo=0.8, y=360, fs=140)
add("big", A(99, 0.2), A(99, 2.6), text="NƯỚC LÊN", col="#3a64a8", fi=0.4, fo=0.8, y=360, fs=130)
add("big", A(103, 0.1), A(103, 2.4), text="NƯỚC RÚT", col=RD, fi=0.3, fo=0.8, y=360, fs=130)
army([(106.52, 21.07), (106.63, 21.01), (106.73, 20.96)], "v", 104, 0.2, 4.0, n=12, t1_i=105, flag=True, u="ship")
arrows((106.70, 21.03), (106.78, 20.95), 104, 0.5, 104, 14); melee((106.76, 20.95), 103, 1.0, 104)
fire((106.78, 20.94), A(105, 0.4), E_(105), 16); fx("fire", A(105, 0.4), E_(105))
add("ring", A(103, 0.8), E_(104), lon=106.76, lat=20.95, col="#b3261e", dur=1.6); fx("drum", A(103, 0.5), E_(104)); fx("water", A(97), E_(104))
card("Ô Mã Nhi", "bị bắt", 105, 1.4, 3.0, col=SO); fx("horn", A(105, 1.4))
route("tron", [BDG, (107.0, 21.6), TM], SO, 106, 0.4, 3.0, t1_i=106, w=4, arrow=True, chev=True)
chip("Năm 938: Ngô Quyền cũng đánh bằng cọc và thủy triều", 107, 107, 1200)

# ============ 10. Sau trận (108–119) ============
C(108, 106.5, 21.0, 2.6); C(110, 106.2, 21.2, 2.8); C(111, 106.8, 20.8, 3.0); C(113, 106.8, 22.3, 4.8); C(115, 106.8, 22.8, 5.0); C(116, 106.0, 21.0, 3.6); C(118, 106.35, 21.1, 2.2); C(119, 106.0, 21.0, 3.6)
chip("Năm 1289: thả phần lớn tù binh", 110, 110, 900)
retreat("traTB", [(106.9, 21.3), LS, (107.1, 22.6)], "s", 110, 0.8, 4.0, n=6, u="inf", dest=False)
card("Ô Mã Nhi", "bị đòi về, thuyền chìm giữa đường, theo lời kể", 111, 0.4, 4.0, col=SO, w=1100)
retreat("hoatLiet", [(106.9, 21.3), LS, (107.4, 23.1)], "s", 113, 0.6, 4.0, n=8, u="cav", dest=False)
chip("Năm 1294: Hốt Tất Liệt mất", 115, 115, 760)
for q, (lbl, off) in enumerate((("LẦN 1", 0.4), ("LẦN 2", 2.4))):
    pass
add("ring", A(117, 0.5), E_(117), lon=TL[0], lat=TL[1], col=SO, dur=1.8); add("ring", A(117, 2.5), E_(117), lon=TL[0], lat=TL[1], col=SO, dur=1.8); add("ring", A(117, 4.5), E_(117), lon=TL[0], lat=TL[1], col=SO, dur=1.8)
city("Thăng Long", TL, "v", 116, 119, 28); city("Vân Đồn", VD, "v", 117, 117, 26); city("Vạn Kiếp", VK, "v", 118, 118, 26)
card("Trần Quốc Tuấn", "mất ở Vạn Kiếp, năm 1300", 118, 0.5, 4.0)
add("night", A(118, 0.0), TOTAL - 0.1, a=0.40, moon=True, fi=1.5, fo=1.0)
add("big", A(119, 0.4), TOTAL - 1.0, text="BA LẦN", col=RD, fi=0.8, fo=1.2, y=340, fs=170)
fx("wind", A(115), TOTAL)


# ---- nhịp máy quay: không đổi cảnh nhanh hơn lời đọc; khung rộng đủ thấy cảnh ----
def _dedupe_cam():
    ks = sorted(cam, key=lambda k: k[0])
    out = []
    for k in ks:
        if out and abs(k[1] - out[-1][1]) < 1e-9 and abs(k[2] - out[-1][2]) < 1e-9 and abs(k[3] - out[-1][3]) < 1e-9:
            continue
        if out and k[0] - out[-1][0] < 4.2 and len(k) <= 4:
            continue
        out.append(k[:])
    for k in out:
        if k[3] < 2.0 and k[0] > 6 and len(k) <= 4: k[3] = 2.0
    # chuyển cảnh nhanh rồi đứng yên: máy quay trôi chậm (dưới ~1 điểm ảnh mỗi khung) làm hình bị rung
    res = []
    for q, k in enumerate(out):
        if res and k[0] - res[-1][0] > 3.4:
            a0 = res[-1]
            res.append([round(a0[0] + 2.6, 3), k[1], k[2], k[3]])
        res.append(k[:4])
    cam[:] = res
_dedupe_cam()

# ============ Các cảnh zoom chính (cận cảnh có hiệu ứng và âm thanh riêng) ============
def _state(t):
    ks = sorted(cam, key=lambda k: k[0])
    if not ks: return [t, 106.0, 21.0, 2.0]
    if t <= ks[0][0]: return ks[0][:]
    for a, b in zip(ks, ks[1:]):
        if a[0] <= t <= b[0]:
            u = (t - a[0]) / max(1e-6, b[0] - a[0]); import math as _m
            return [t, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u, _m.exp(_m.log(a[3]) + (_m.log(b[3]) - _m.log(a[3])) * u)]
    return ks[-1][:]
ZS = [("nmKho", 1, 1, TL, [("gong", 1.0, 0), ("wind", 0.0, 99), ("march", 0.3, 99)]),
      ("nmPho", 22, 23, TL, [("march", 0.0, 99), ("wind", 0.0, 99)]),
      ("nmDienHong", 40, 40, TL, [("horn", 0.4, 0), ("drum", 0.2, 99)]),
      ("nmBinhTrong", 52, 54, DM, [("fire", 0.0, 99), ("clash", 0.6, 0), ("gong", 6.0, 0)]),
      ("camp", 60, 60, (105.95, 20.95), [("wind", 0.0, 99), ("insect", 0.0, 99)]),
      ("nmHamTu", 62, 64, HT, [("clash", 0.8, 0), ("arrow", 0.3, 99), ("drum", 0.3, 99), ("clash", 4.0, 0)]),
      ("nmVanDon", 83, 84, VD, [("water", 0.0, 99), ("fire", 1.5, 99), ("arrow", 0.5, 99), ("clash", 3.0, 0)]),
      ("nmCoc", 97, 100, BDG, [("water", 0.0, 99), ("wind", 0.0, 99), ("drum", 6.0, 99)]),
      ("nmBachDang", 101, 105, BDG, [("water", 0.0, 99), ("fire", 1.5, 99), ("arrow", 0.6, 99), ("drum", 0.5, 99), ("clash", 2.0, 0), ("clash", 5.0, 0), ("horn", 11.0, 0)])]
WD_CLOSE = 0.115
for sc, i0, i1, (lo, la), fxs in ZS:
    ts0, te = A(i0), E_(i1); span = te - ts0
    zin = min(2.6, span * 0.4); zout = min(1.8, span * 0.35)
    st0 = _state(ts0)
    cam[:] = [k for k in cam if not (ts0 - 1e-6 <= k[0] <= te + 1e-6)]
    cam.append([ts0, st0[1], st0[2], st0[3]])
    cam.append([ts0 + zin, lo, la, WD_CLOSE])
    cam.append([te - zout, lo, la, WD_CLOSE])
    add("cc", ts0 - 0.2, te + 0.6, scene=sc, lon=lo, lat=la, ts=ts0 + zin - 0.4, sp=1.0, fi=0.8, fo=0.6)
    add("ring", ts0 - 0.6, ts0 + 1.2, lon=lo, lat=la, dur=1.8, fi=0.1, fo=0.4)
    fx("arrow", ts0, ts0 + 0.3)
    for kind, o0, o1 in fxs:
        if o1 == 99: fx(kind, ts0 + zin + o0, te)
        else: fx(kind, ts0 + zin + o0)


# ---- kiểm: thuyền chỉ đi trên sông hoặc biển ----
import re as _re2
from matplotlib.path import Path as _MP
_g = open(HERE / "geo_nhe.js", encoding="utf-8").read(); _G = json.loads(_g[_g.index("{"):_g.rindex("}") + 1])
_polys = [_MP([tuple(map(float, q.split(","))) for q in _re2.findall(r"[-\d.]+,[-\d.]+", part)]) for part in _G["land"].split("M")[1:]]
def _xy(lon, lat): return ((lon - _G["lon0"]) * _G["k"] * _G["scale"], (_G["lat1"] - lat) * _G["scale"])
def _land(lon, lat):
    p = _xy(lon, lat); return any(pl.contains_point(p) for pl in _polys)
def _dseg(p, a, b):
    ax, ay, bx, by, px, py = a[0], a[1], b[0], b[1], p[0], p[1]
    dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy
    u = 0 if L == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
    return ((px - ax - u * dx) ** 2 + (py - ay - u * dy) ** 2) ** 0.5
def _on_water(lon, lat):
    if not _land(lon, lat): return True
    for r in RIVERS:
        for a, b in zip(r["pts"], r["pts"][1:]):
            if _dseg((lon, lat), a, b) < 0.045: return True
    return False
_bad = []
for it in items:
    if it["k"] == "army" and it.get("u") == "ship":
        pts = it["pts"]; n = 0; m = 0; _f = []
        for a, b in zip(pts, pts[1:]):
            for q in range(25):
                u = q / 24; n += 1; _w = _on_water(a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u); m += (not _w); (_f.append((round(a[0] + (b[0] - a[0]) * u, 2), round(a[1] + (b[1] - a[1]) * u, 2))) if not _w and len(_f) < 4 else None)
        if m: _bad.append((it["t0"], round(100 * m / n), pts[0], pts[-1], _f))
if _bad:
    for b in _bad: print("THUYỀN TRÊN CẠN:", b)
    raise SystemExit("có đường thuyền đi trên đất liền")
print("kiểm thuyền: mọi đường thuyền nằm trên sông hoặc biển")
FORTS = [{"lon": TL[0], "lat": TL[1], "side": "v", "big": 1}, {"lon": VK[0], "lat": VK[1], "side": "v"}, {"lon": LS[0], "lat": LS[1], "side": "v"}, {"lon": TH[0], "lat": TH[1], "side": "v"},
         {"lon": NA[0], "lat": NA[1], "side": "v"}, {"lon": TB[0], "lat": TB[1], "side": "v"}, {"lon": NB[0], "lat": NB[1], "side": "v"}, {"lon": QH[0], "lat": QH[1], "side": "v"}, {"lon": 106.55, "lat": 21.27, "side": "v"}]

# ---- phụ đề theo từng đoạn (chia trang theo dấu câu, mốc theo số chữ) ----
import re as _re
def _wrap(txt, w=36):
    out, cur = [], ""
    for wd_ in txt.split():
        if cur and len(cur) + 1 + len(wd_) > w:
            out.append(cur); cur = wd_
        else:
            cur = (cur + " " + wd_).strip()
    if cur: out.append(cur)
    return out
def _pages(t, mx=66):
    parts = [p.strip() for p in _re.split(r"(?<=[.?!])\s+", t) if p.strip()]
    pages = []
    for p in parts:
        cl = [c.strip() for c in _re.split(r"(?<=,)\s+", p) if c.strip()] if len(p) > mx else [p]
        pages.extend(cl)
    out, cur = [], ""
    for p in pages:
        if cur and len(cur + " " + p) > mx: out.append(cur); cur = p
        else: cur = (cur + " " + p).strip()
    if cur: out.append(cur)
    res = []
    for p in out:
        if len(_wrap(p)) > 2:
            ws = p.split(); h = len(ws) // 2; res += [" ".join(ws[:h]), " ".join(ws[h:])]
        else: res.append(p)
    return res
for _i, _b in enumerate(KB, 1):
    _pg = _pages(_b["text"])
    _tot = sum(len(p.split()) for p in _pg); _t0 = S[_i] + 0.05; _span = D[_i] - 0.1
    for p in _pg:
        _d = _span * len(p.split()) / _tot
        add("sub", _t0, _t0 + _d, lines=_wrap(p), fi=0.1, fo=0.1); _t0 += _d

cam.sort(key=lambda k: k[0])
if cam[0][0] > 0:
    cam.insert(0, [0.0] + cam[0][1:])
cam.append([TOTAL] + cam[-1][1:])
SPEC = {"dur": round(TOTAL, 2), "rivers": RIVERS, "forts": FORTS, "cam": cam, "items": items, "fade0": 1.0, "fade1": 3.0, "starts": {i: round(S[i], 2) for i in S}}
(HERE / "spec_nm5.js").write_text("window.SPEC=" + json.dumps(SPEC, ensure_ascii=False) + ";", encoding="utf-8")
json.dump({"dur": TOTAL, "sfx": sfx, "starts": {i: S[i] for i in S}, "pstarts": {str(b["n"]): PS[k][0] for k, b in enumerate(KB)}, "durs": {i: D[i] for i in D}}, open(HERE / "sfx_nm5.json", "w"), indent=1)
print("tổng", round(TOTAL, 1), "giây =", round(TOTAL / 60, 2), "phút;", len(items), "mục hình;", len(sfx), "mục âm thanh")
