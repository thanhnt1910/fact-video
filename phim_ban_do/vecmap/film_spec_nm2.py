"""Bảng cảnh video Nguyên Mông (nm2) bằng bản đồ vector: thời điểm từng đoạn theo giọng đọc thật -> spec_nm2.js (hình) + sfx_nm2.json (âm thanh).
Chạy: python phim_ban_do/vecmap/film_spec_nm2.py ; vẽ khung: SPEC_JS=spec_nm2.js SFX_JSON=sfx_nm2.json python phim_ban_do/vecmap/ve_film.py still <giây>..."""
import json, re, textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KB = json.load(open(ROOT / "ke-hoach/thu-giong-hai/nm2_full.json", encoding="utf-8"))
DUR = json.load(open(ROOT / "assets/thu_giong_hai/nm2_chuan/thoi_luong.json"))
BASE = 22000
LEAD, GAP, TAIL = 1.0, 0.35, 4.0
S, D, TXT = {}, {}, {}
t = LEAD
for b in KB:
    i = b["n"] - BASE
    S[i], D[i], TXT[i] = t, DUR[str(b["n"])], b["text"]
    t += D[i] + GAP
TOTAL = t + TAIL
A = lambda i, off=0.0: S[i] + off
E_ = lambda i: S[i] + D[i]

V, SO = "#c9742a", "#3a64a8"
BRN = "#6b5a45"
TL = (105.85, 21.03); VD = (107.45, 21.10); BLN = (105.62, 21.28); QH = (104.90, 21.72); BT = (106.45, 21.17)
CT = (105.15, 19.00); LS = (106.76, 21.85); VK = (106.38, 21.07); DM = (106.00, 20.58); TH = (105.78, 19.80)
HT = (106.02, 20.84); CD = (105.80, 20.98); TKT = (106.22, 20.70); BDG = (106.80, 20.95); LH = (106.35, 20.55); TM = (107.20, 22.35)
cam, items, sfx = [], [], []


def C(i, lon, lat, wd, off=0.0, hold=True):
    cam.append([A(i, off), lon, lat, wd])
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
    add("city", A(i0), E_(i1), lon=p[0], lat=p[1], name=name, side=side, fs=fs, fi=0.6, fo=0.6, **kw)


def card(title, sub, i, off=0.4, dur=3.4, col=V, **kw):
    add("card", A(i, off), min(A(i, off + dur), E_(i) - 0.1), title=title, sub=sub, col=col, fi=0.5, fo=0.5, **kw)


def chip(text, i0, i1, w=520):
    add("chip", A(i0), E_(i1), text=text, w=w, fi=0.6, fo=0.6, x=70, y=110)


def route(rid, pts, col, i, off, dur, t1_i=None, w=6, fo=0.8):
    add("route", A(i, off), E_(t1_i or i), id=rid, pts=[list(p) for p in pts], col=col, dur=dur, w=w, fi=0.2, fo=fo)


def army(pts, side, i, off, dur, n=12, t1_i=None, stay=True, flag=True, u="inf", col=None):
    d = add("army", A(i, off), E_(t1_i or i), pts=[list(p) for p in pts], side=side, n=n, dur=dur, stay=stay, flag=flag, u=u, fi=0.2, fo=0.8)
    if col:
        d["col"] = col


def lab(text, p, col, i0, i1, fs=46, op=0.6, **kw):
    add("label", A(i0), E_(i1), lon=p[0], lat=p[1], text=text, col=col, fs=fs, op=op, fi=0.8, fo=0.8, **kw)


def mark(shape, p, i, off=0.3, i1=None, **kw):
    add("mark", A(i, off), E_(i1 or i), shape=shape, lon=p[0], lat=p[1], fi=0.3, fo=0.5, **kw)


def fire(p, t0, t1, s=18):
    add("fire", t0, t1, lon=p[0], lat=p[1], s=s, fi=0.6, fo=0.8)


# ---- phụ đề: mỗi đoạn một khối, hai đến ba dòng (khi có mốc nhận dạng thì thay bằng phụ đề theo chữ) ----
for i in S:
    lines = textwrap.wrap(TXT[i], 52)
    add("sub", A(i, 0.05), E_(i) + 0.1, lines=lines, fi=0.25, fo=0.25)

# ============ Chương 1: Hai ba ngày (1–4) ============
C(1, 106.65, 21.15, 2.2); C(2, 106.9, 21.05, 2.4); C(3, 106.6, 21.1, 3.0); C(4, 106.4, 21.0, 4.0)
city("Thăng Long", TL, "v", 1, 9, 28); city("Vân Đồn", VD, "v", 1, 4, 28)
route("giai", [VD, (106.9, 21.2), (106.3, 21.2), TL], V, 1, 0.5, 6.0, t1_i=2, w=5)
army([VD, (106.9, 21.2), (106.3, 21.2), TL], "v", 1, 0.8, 7.0, n=3, t1_i=2, flag=True, u="cav")
card("Trần Khánh Dư", "bị xiềng tay, giải về kinh", 1, 0.4, 3.4)
army([(108.4, 20.7), (107.6, 20.85), (106.9, 21.0)], "s", 2, 0.4, 6.0, n=10, t1_i=2, flag=True, u="ship")
chip("Hạm đội quân Nguyên đã vượt qua", 2, 2, 800)
add("big", A(3, 0.2), A(3, 3.2), text="?", col="#7a1f1f", fi=0.4, fo=0.8, y=620, fs=300)
add("big", A(4, 0.4), E_(4), text="QUÂN LƯƠNG", col="#7a1f1f", fi=0.6, fo=0.8, y=560, fs=170)
fx("march", A(1, 0.8), E_(2)); fx("drum", A(3), E_(4))

# ============ Chương 2: Lần thứ nhất (5–11) ============
C(5, 105.45, 21.45, 1.5); C(8, 105.65, 21.25, 1.0); C(9, 105.75, 21.1, 0.9); C(10, 105.4, 21.5, 1.5); C(11, 105.3, 21.7, 2.0)
city("Bình Lệ Nguyên", BLN, "v", 5, 8, 26); city("Quy Hóa", QH, "v", 5, 11, 26)
chip("Cuối năm 1257", 5, 7, 560)
army([QH, (105.2, 21.55), BLN], "s", 5, 0.4, 5.0, n=16, t1_i=8, flag=True, u="cav")
army([TL, (105.75, 21.2), BLN], "v", 5, 2.5, 5.0, n=10, t1_i=8, flag=True, u="ship")
card("Trần Thái Tông", "đích thân ra trận", 5, 2.8, 3.4)
fx("horn", A(5, 0.3)); fx("water", A(5, 2.5), E_(6)); fx("march", A(5, 0.4), E_(8))
card("Trần Thủ Độ", "Thái sư", 8, 0.4, 3.4)
add("ring", A(9, 3.0), E_(9), lon=TL[0] + .03, lat=TL[1], col="#b3261e", dur=1.6); fx("clash", A(9, 3.0)); fx("drum", A(9, 2.5), E_(9))
mark("x", (TL[0] + .06, TL[1] + .04), 9, 3.3)
army([TL, (105.5, 21.4), QH], "s", 10, 0.3, 5.0, n=12, t1_i=10, flag=True, u="cav")
mark("x", (105.1, 21.55), 10, 3.0); fx("clash", A(10, 3.0))
add("mark", A(11, 0.4), E_(11), shape="q", lon=105.6, lat=21.4, s=40, fi=0.3, fo=0.4)

# ============ Chương 3: Bình Than (12–18) ============
C(12, 106.15, 21.15, 1.1); C(13, 106.42, 21.15, 0.6); C(14, 106.43, 21.16, 0.5); C(16, 106.42, 21.15, 0.6); C(18, 106.35, 21.15, 0.7)
city("Bình Than", BT, "v", 12, 18, 28); city("Thăng Long", TL, "v", 12, 12, 26)
chip("Mùa đông năm 1282", 12, 13, 640)
army([TL, (106.1, 21.1), (106.38, 21.15)], "v", 12, 0.5, 5.0, n=8, t1_i=18, flag=True, u="ship")
army([(106.7, 21.1), (106.55, 21.15), (106.5, 21.17)], "v", 13, 0.3, 3.0, n=1, t1_i=15, flag=False, u="ship", col=BRN)
card("Trần Khánh Dư", "đang bán than ở Chí Linh", 13, 1.2, 3.4)
card("Trần Quốc Toản", "Hoài Văn hầu, còn trẻ", 16, 2.6, 3.2)
chip("Quả cam bị bóp nát", 17, 17, 640)
army([(106.5, 21.2), (106.45, 21.25), (106.4, 21.3)], "v", 17, 1.5, 4.0, n=8, t1_i=18, flag=True, u="inf")
add("mark", A(18, 3.0), E_(18), shape="q", lon=106.2, lat=21.35, s=40, fi=0.3, fo=0.4)

# ============ Chương 4: Mượn đường (19–22) ============
C(19, 106.0, 20.5, 4.5); C(20, 106.3, 21.5, 2.0); C(21, 105.9, 21.1, 1.2); C(22, 105.9, 21.1, 1.2)
chip("Năm 1284", 19, 20, 400)
city("Chiêm Thành", CT, "v", 19, 19, 26); city("Lạng Sơn", LS, "v", 19, 22, 26); city("Thăng Long", TL, "v", 19, 22, 28)
route("muon", [LS, (106.4, 20.8), (105.8, 19.8), CT], "#3a64a8", 19, 0.5, 5.0, t1_i=19, w=5)
army([(107.2, 22.3), LS], "s", 20, 0.3, 4.0, n=16, t1_i=22, flag=True, u="cav")
card("Thoát Hoan", "con trai Hốt Tất Liệt", 20, 2.4, 3.2, col=SO)
card("Trần Thánh Tông", "triệu các cụ già về điện Diên Hồng", 21, 0.3, 4.5, w=1100)
add("ring", A(22, 0.3), A(22, 3.0), lon=TL[0], lat=TL[1], col="#c9742a", dur=1.6); add("ring", A(22, 1.3), E_(22), lon=TL[0], lat=TL[1], col="#c9742a", dur=1.6)
card("Trần Hưng Đạo", "tổng chỉ huy quân đội", 22, 3.0, 3.4)
fx("horn", A(22, 0.3)); fx("march", A(20, 0.3), E_(21))

# ============ Chương 5: Lần thứ hai (23–29) ============
C(23, 106.1, 21.0, 2.2); C(25, 106.0, 20.6, 2.0); C(26, 106.0, 20.6, 1.4); C(27, 105.9, 20.2, 2.6); C(28, 105.9, 20.9, 2.0); C(29, 105.9, 21.0, 1.4)
chip("Năm 1285", 23, 23, 400)
city("Vạn Kiếp", VK, "v", 23, 25, 26); city("Thăng Long", TL, "v", 23, 29, 28); city("Đà Mạc", DM, "v", 25, 26, 26); city("Thanh Hóa", TH, "v", 27, 29, 26)
army([LS, (106.5, 21.4), VK, (106.1, 21.0), TL], "s", 23, 0.4, 12.0, n=18, t1_i=28, flag=True, u="cav")
army([(105.15, 19.0), TH, (105.9, 20.3), DM], "s", 24, 0.3, 8.0, n=16, t1_i=26, flag=True, u="ship")
army([VK, (106.2, 21.0), DM, TH], "v", 23, 1.0, 10.0, n=10, t1_i=27, flag=True, u="inf")
add("ring", A(23, 2.0), E_(23), lon=VK[0], lat=VK[1], col="#b3261e", dur=1.6); fx("clash", A(23, 2.0)); fx("drum", A(23, 1.5), E_(23))
card("Trần Bình Trọng", "Bảo Nghĩa Vương", 25, 0.4, 3.4); mark("x", DM, 26, 0.9, 26)
fx("gong", A(26, 0.9))
chip("Vào Thanh Hóa lánh giặc", 27, 27, 760)
chip("Vườn không nhà trống", 29, 29, 700)
fire((TL[0] + .08, TL[1] + .05), A(29, 0.6), E_(29), 18); fire((TL[0] - .1, TL[1] - .08), A(29, 1.5), E_(29), 16)
fx("fire", A(29, 0.6), E_(29)); fx("march", A(23, 0.4), E_(25)); fx("water", A(24, 0.3), E_(25))

# ============ Chương 6: Phản công (30–37) ============
C(30, 105.95, 20.9, 0.9); C(33, 105.95, 20.85, 0.8); C(34, 105.85, 20.95, 0.8); C(35, 106.05, 20.9, 1.1); C(36, 106.2, 20.7, 0.8)
chip("Mùa hạ năm 1285", 30, 30, 700)
city("Hàm Tử", HT, "v", 30, 33, 26); city("Chương Dương", CD, "v", 33, 36, 26); city("Tây Kết", TKT, "v", 35, 37, 26)
army([(105.9, 20.84), (105.97, 20.84)], "s", 30, 0.2, 3.0, n=14, t1_i=33, flag=True, u="inf")
army([(106.15, 20.8), (106.08, 20.84)], "v", 30, 0.6, 3.0, n=12, t1_i=33, flag=True, u="inf")
card("Trần Nhật Duật", "chỉ huy trận Hàm Tử", 30, 3.0, 3.2)
chip("Người Tống theo Đại Việt, vẫn mặc áo Tống", 31, 31, 1000)
add("ring", A(32, 2.0), E_(32), lon=HT[0], lat=HT[1], col="#b3261e", dur=1.6); fx("clash", A(32, 2.0)); fx("arrow", A(32, 1.4), A(32, 3.4))
army([HT, (105.88, 20.9), (105.7, 21.1)], "s", 33, 0.5, 3.5, n=12, t1_i=33, stay=False, flag=False, u="inf")
card("Trần Quang Khải", "Thượng tướng", 34, 0.3, 3.2)
army([(105.68, 20.98), CD], "s", 34, 0.1, 2.0, n=14, t1_i=34, flag=True, u="inf")
army([(105.95, 21.02), (105.86, 20.99)], "v", 34, 0.2, 2.2, n=14, t1_i=34, flag=True, u="inf")
add("ring", A(34, 3.0), E_(34), lon=CD[0], lat=CD[1], col="#b3261e", dur=1.6); fx("clash", A(34, 3.0)); fx("drum", A(34, 2.0), E_(34))
army([CD, (105.7, 21.4), LS], "s", 35, 0.3, 4.0, n=10, t1_i=35, stay=False, flag=False, u="inf")
mark("x", TKT, 35, 2.4); fx("gong", A(35, 2.4))
card("Toa Đô", "tướng Nguyên mượn đường", 36, 0.3, 3.2, col=SO)
fx("march", A(30, 0.5), E_(30))

# ============ Chương 7: Lần thứ ba (38–47) ============
C(38, 107.0, 21.4, 3.2); C(39, 107.0, 21.1, 2.6); C(40, 107.2, 21.1, 1.6); C(42, 107.3, 21.1, 1.2); C(43, 107.3, 21.1, 1.0); C(45, 106.9, 21.4, 3.0); C(46, 106.4, 20.8, 1.6); C(47, 106.7, 20.9, 1.6)
chip("Cuối năm 1287", 38, 38, 640)
city("Lạng Sơn", LS, "v", 38, 40, 26); city("Vân Đồn", VD, "v", 38, 45, 28); city("Long Hưng", LH, "v", 46, 47, 26); city("Bạch Đằng", BDG, "v", 47, 47, 26)
army([(107.0, 22.5), LS, (106.6, 21.5), VK], "s", 38, 0.3, 14.0, n=18, t1_i=47, flag=True, u="cav")
army([(108.6, 20.7), (107.6, 21.0), VD, (106.8, 20.9), LH], "s", 38, 0.5, 20.0, n=14, t1_i=46, flag=True, u="ship")
army([(109.2, 20.7), (108.3, 20.9), (107.65, 21.0)], "s", 39, 0.2, 8.0, n=10, t1_i=43, flag=True, u="ship", col=BRN)
card("Trương Văn Hổ", "chỉ huy thuyền lương", 39, 2.6, 3.2, col=SO)
card("Trần Hưng Đạo", "giao giữ biển Vân Đồn", 39, 0.2, 2.4)
card("Trần Khánh Dư", "không chặn nổi hạm đội", 40, 2.0, 3.2)
route("giai2", [VD, (106.9, 21.2), TL], V, 40, 0.6, 5.0, w=5)
chip("Xin hoãn hai ba ngày", 41, 41, 640)
army([(107.3, 21.0), (107.5, 21.08)], "v", 42, 0.5, 3.5, n=8, t1_i=43, flag=True, u="ship")
add("ring", A(43, 1.8), E_(43), lon=107.62, lat=21.02, col="#b3261e", dur=1.6); fx("clash", A(43, 1.8)); fx("water", A(43, 1.8), E_(43))
mark("x", (107.68, 21.0), 43, 2.4); mark("x", (107.74, 21.0), 43, 2.8)
chip("Lương thực, khí giới bị bắt", 43, 44, 700)
route("tin", [VD, (107.0, 21.5), LS], "#3a64a8", 45, 0.5, 4.0, w=4)
army([VD, (107.0, 21.5), LS], "s", 45, 0.8, 5.0, n=6, t1_i=45, stay=False, flag=False, u="inf")
fire(LH, A(46, 0.9), E_(46), 20); fx("fire", A(46, 0.9), E_(46))
add("mark", A(47, 0.4), E_(47), shape="q", lon=106.8, lat=20.95, s=40, fi=0.3, fo=0.4)
fx("march", A(38, 0.3), E_(40)); fx("water", A(38, 0.5), E_(40)); fx("horn", A(38, 0.2))

# ============ Chương 8: Bạch Đằng (48–56) ============
RIV = [(106.40, 21.10), (106.52, 21.07), (106.63, 21.01), (106.73, 20.96), (106.82, 20.91), (106.88, 20.82), (106.93, 20.72), (107.0, 20.62)]
STK = [(106.69, 20.985), (106.72, 20.965), (106.745, 20.955), (106.765, 20.94), (106.785, 20.93), (106.80, 20.92), (106.815, 20.905), (106.835, 20.89), (106.70, 20.96), (106.73, 20.98), (106.76, 20.955), (106.79, 20.915), (106.82, 20.925), (106.85, 20.87)]
C(48, 106.74, 20.97, 0.95); C(52, 106.78, 20.94, 1.1); C(53, 106.8, 20.95, 1.2); C(54, 106.7, 21.0, 0.9); C(55, 106.35, 20.55, 2.0); C(56, 106.35, 20.55, 2.0)
chip("Tháng ba năm 1288", 48, 48, 640)
add("tide", A(48), E_(52) + 1.5, pts=[list(p) for p in RIV], stakes=[list(p) for p in STK], w=16, show=2.0,
    lv=[[A(48), 1.0], [A(49, 0.5), 1.0], [A(50, 0.0), 0.95], [A(50, 3.0), 0.08], [E_(52), 0.08], [E_(52) + 1.5, 0.5]], fi=0.6, fo=0.8)
city("Bạch Đằng", BDG, "v", 48, 52, 26)
army([(107.0, 20.7), (106.9, 20.8), (106.76, 20.95), (106.72, 20.97)], "s", 48, 0.2, 14.0, n=16, t1_i=52, flag=True, u="ship")
army([(106.62, 21.02), (106.82, 20.91), (106.88, 20.84), (106.7, 20.97), (106.62, 21.02)], "v", 49, 0.5, 9.0, n=6, t1_i=52, flag=True, u="ship")
army([(106.55, 21.06), (106.7, 20.99), (106.78, 20.94)], "v", 50, 0.6, 4.0, n=12, t1_i=52, flag=True, u="ship")
army([(106.98, 20.7), (106.85, 20.88), (106.78, 20.94)], "s", 51, 0.0, 5.0, n=10, t1_i=52, flag=False, u="ship", col=BRN)
fire((106.78, 20.94), A(51, 4.0), E_(52), 16); fx("fire", A(51, 4.0), E_(52))
add("ring", A(50, 3.0), E_(51), lon=106.76, lat=20.95, col="#b3261e", dur=1.6); fx("clash", A(50, 3.0)); fx("drum", A(50, 3.0), E_(51)); fx("water", A(48), E_(51))
add("big", A(52, 0.3), A(52, 3.6), text="400 THUYỀN", col="#7a1f1f", fi=0.4, fo=0.8, y=360, fs=120)
card("Ô Mã Nhi", "bị bắt sống", 52, 3.4, 3.0, col=SO)
route("tron", [BDG, (107.0, 21.6), TM], "#3a64a8", 52, 1.0, 4.0, w=4)
army([BDG, (107.0, 21.6), TM], "s", 52, 1.2, 5.0, n=6, t1_i=52, stay=False, flag=False, u="inf")
city("Tư Minh", TM, "s", 52, 52, 24)
card("Trần Thánh Tông", "mời các tướng bị bắt", 53, 0.3, 3.0)
chip("Ngô Quyền cũng dùng cách này năm 938", 54, 54, 900)
city("Long Hưng", LH, "v", 55, 56, 26)
card("Trần Nhân Tông", "làm thơ báo thắng trận", 56, 0.3, 3.2)
fx("horn", A(52, 3.4)); fx("gong", A(55, 0.5))

# ============ Chương 9: Hai người bị gạt ra (57–65) ============
C(57, 105.9, 21.0, 1.6); C(58, 106.4, 21.5, 2.4); C(59, 106.5, 21.6, 2.6); C(60, 106.7, 21.1, 2.4); C(62, 106.4, 21.15, 1.2); C(63, 107.2, 21.1, 1.6); C(65, 106.6, 21.1, 3.0)
city("Thăng Long", TL, "v", 57, 57, 28)
fire(TL, A(57, 0.4), A(57, 3.8), 18)
army([(107.0, 22.4), LS], "s", 58, 0.2, 3.0, n=12, t1_i=58, flag=True, u="cav")
chip("Năm 1294: Hốt Tất Liệt qua đời", 59, 59, 900)
army([LS, (107.1, 22.6), (107.4, 23.1)], "s", 59, 1.6, 4.0, n=12, t1_i=59, stay=False, flag=False, u="cav")
city("Vân Đồn", VD, "v", 60, 65, 26); city("Bạch Đằng", BDG, "v", 60, 65, 26)
add("ring", A(60, 0.4), A(60, 2.6), lon=VD[0], lat=VD[1], col="#c9742a", dur=1.6); add("ring", A(60, 3.8), A(60, 6.2), lon=BDG[0], lat=BDG[1], col="#c9742a", dur=1.6)
chip("Cả hai lần, thuyền lương rơi vào tay Đại Việt", 61, 61, 1100)
city("Bình Than", BT, "v", 62, 63, 26)
add("mark", A(62, 1.8), E_(62), shape="flag", lon=BT[0], lat=BT[1], s=30, col=V, fi=.4, fo=.6)
card("Trần Quốc Toản", "chết khi đang đuổi đánh quân Nguyên", 62, 0.3, 4.0, w=1100)
card("Trần Khánh Dư", "bị dân Vân Đồn kiện, vua vẫn không bỏ", 63, 0.3, 4.5, w=1200)
add("night", A(65, 0.0), TOTAL - 0.1, a=0.45, moon=True, fi=1.5, fo=1.0)
fx("wind", A(57), TOTAL); fx("gong", A(62, 0.3))

# ---- camera ----
cam.sort(key=lambda k: k[0])
if cam[0][0] > 0:
    cam.insert(0, [0.0] + cam[0][1:])
cam.append([TOTAL] + cam[-1][1:])
SPEC = {"dur": round(TOTAL, 2), "cam": cam, "items": items, "fade0": 1.0, "fade1": 3.0, "starts": {i: round(S[i], 2) for i in S}}
(HERE / "spec_nm2.js").write_text("window.SPEC=" + json.dumps(SPEC, ensure_ascii=False) + ";", encoding="utf-8")
json.dump({"dur": TOTAL, "sfx": sfx, "starts": {i: S[i] for i in S}, "durs": {i: D[i] for i in D}}, open(HERE / "sfx_nm2.json", "w"), indent=1)
print("tổng", round(TOTAL, 1), "giây =", round(TOTAL / 60, 2), "phút;", len(items), "mục hình;", len(sfx), "mục âm thanh")
