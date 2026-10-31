"""Dựng bảng cảnh cho video Lý Thường Kiệt (lt1v3): thời điểm từng đoạn theo giọng đọc thật -> spec.js (hình) + sfx.json (âm thanh).
Chạy: python phim_ban_do/vecmap/film_spec.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KB = json.load(open(ROOT / "ke-hoach/thu-giong-hai/lt1v3_full.json", encoding="utf-8"))
DUR = json.load(open(ROOT / "assets/thu_giong_hai/lt1v3_chuan/thoi_luong.json"))
LEAD, GAP, TAIL = 1.0, 0.35, 4.0
S, D = {}, {}
t = LEAD
for i, b in enumerate(KB, 1):
    S[i], D[i] = t, DUR[str(b["n"])]
    t += D[i] + GAP
TOTAL = t + TAIL
A = lambda i, off=0.0: S[i] + off
E_ = lambda i: S[i] + D[i]          # hết đoạn i

V, SO = "#c9742a", "#3a64a8"
TL = (105.85, 21.03); LS = (106.76, 21.85); UC = (108.37, 22.82); KC = (108.65, 21.96); LC = (109.12, 21.66)
QC = (110.29, 25.27); CL = (108.75, 23.15); QN = (106.26, 22.67)
SEA = [(107.2, 20.95), (107.9, 21.2), (108.3, 21.55), (108.65, 21.96), (109.0, 21.8), (109.12, 21.66)]
LAND = [TL, (106.3, 21.45), LS, (106.75, 22.12), (107.5, 22.5), UC]
TONG_ROAD = [QC, (109.2, 24.2), UC, (107.3, 22.3), LS, (106.3, 21.4)]
cam, items, sfx = [], [], []


def C(i, lon, lat, wd, off=0.0, hold=True):
    cam.append([A(i, off), lon, lat, wd])
    if hold and D[i] > 3.0:          # giữ khung đến gần hết đoạn rồi mới chuyển sang cảnh sau
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


def card(title, sub, i, off=0.4, dur=4.0, col=V, **kw):
    add("card", A(i, off), A(i, off + dur), title=title, sub=sub, col=col, fi=0.5, fo=0.5, **kw)


def chip(text, i0, i1, w=520):
    add("chip", A(i0), E_(i1), text=text, w=w, fi=0.6, fo=0.6)


def route(rid, pts, col, i, off, dur, t1_i=None, w=6, fo=0.8):
    add("route", A(i, off), E_(t1_i or i), id=rid, pts=[list(p) for p in pts], col=col, dur=dur, w=w, fi=0.2, fo=fo)


def army(pts, side, i, off, dur, n=14, t1_i=None, stay=True, flag=True, u="inf"):
    add("army", A(i, off), E_(t1_i or i) + (0.0 if stay else 0.0), pts=[list(p) for p in pts], side=side, n=n, dur=dur, stay=stay, flag=flag, u=u, fi=0.2, fo=0.8)


def lab(text, p, col, i0, i1, fs=46, op=0.6, **kw):
    add("label", A(i0), E_(i1), lon=p[0], lat=p[1], text=text, col=col, fs=fs, op=op, fi=0.8, fo=0.8, **kw)


# ============ Chương 1: Bốn mươi ngày (1–5) ============
C(1, *UC, 0.55); C(2, *UC, 0.55); C(3, 107.2, 22.4, 6.0, 0.0); C(4, 106.9, 21.9, 8.6, 0.0); C(5, 106.6, 21.9, 7.5)
add("siege", 0, E_(2) + 0.2, ph=[[0, .97], [E_(1), .97], [A(2), .45], [E_(2), .6]])
add("chip", A(1), E_(2), text="Ung Châu, năm 1075", w=640, fi=0.6, fo=0.4)
fx("fire", A(1), E_(1)); fx("drum", A(2), E_(2))
lab("ĐẠI VIỆT", (105.0, 21.2), "#8a4a14", 3, 5, fs=54)
lab("TỐNG", (109.2, 24.3), "#27487f", 3, 5, fs=54)
army([(105.8, 21.1), (106.6, 21.9), UC], "v", 3, 0.5, 5.0, n=14, t1_i=4, flag=True)
fx("march", A(3, 0.5), E_(4))
add("big", A(4, 0.2), A(4, 3.0), text="?", col="#7a1f1f", fi=0.4, fo=0.8, y=620, fs=300)
card("Lý Thường Kiệt", "Thái úy triều Lý", 5, 0.6, 5.0)
city("Thăng Long", TL, "v", 3, 9, 30)

# ============ Chương 2: Người cầm cờ tiết (6–9) ============
C(6, *TL, 1.1); C(7, 105.95, 21.15, 2.2); C(8, 105.9, 19.6, 8.0); C(9, 106.6, 22.0, 8.6)
card("Phường Thái Hòa", "kinh thành Thăng Long", 6, 0.4, 4.0)
add("army", A(7, 0.3), E_(7), pts=[list(TL), [105.55, 21.2], [105.95, 21.4], [106.3, 21.1], list(TL)], side="v", n=3, dur=6.5, stay=True, flag=True, u="cav", fi=0.2, fo=0.6)
card("Cờ tiết", "thay vua đi tuần thú", 7, 0.5, 3.5)
route("champa", [TL, (105.8, 20.2), (106.0, 19.0), (106.4, 18.0)], V, 8, 0.4, 5.0, w=6)
army([TL, (105.8, 20.2), (106.0, 19.0), (106.4, 18.0)], "v", 8, 0.6, 5.5, n=16, flag=True)
lab("hướng Chiêm Thành", (106.7, 18.4), "#8a4a14", 8, 8, fs=34, op=0.8, it=True, ls=2)
chip("Năm 1069", 8, 8, 400); chip("Năm 1075", 9, 9, 400)
add("mark", A(9, 3.5), E_(9) + .3, shape="arrow", lon=107.4, lat=23.4, s=26, col="#b3261e", ang=125, fi=0.3, fo=0.5)
add("ring", A(9, 4.0), E_(9), lon=108.9, lat=24.0, col="#b3261e", dur=1.6)
card("Thái úy", "thống lĩnh toàn bộ binh quyền", 9, 0.4, 3.5)
fx("march", A(7, 0.3), E_(8)); fx("horn", A(9, 4.0))

# ============ Chương 3: Chờ hay đánh (10–18) ============
C(10, 109.6, 24.7, 5.5); C(11, 109.9, 24.9, 4.5); C(12, 109.8, 24.7, 4.5); C(13, 107.2, 22.1, 6.0); C(14, 107.2, 22.1, 6.0); C(15, 107.4, 22.6, 7.0); C(18, 107.4, 22.8, 7.0)
lab("TỐNG", (111.3, 25.9), "#27487f", 10, 12, fs=52)
card("Vương An Thạch", "tể tướng nhà Tống", 10, 0.5, 4.5, col=SO)
city("Quế Châu", QC, "s", 10, 12, 30)
card("Thẩm Khởi, Lưu Di", "được phái đến vùng Quế Châu", 11, 0.6, 5.0, col=SO)
route("tong_doa", [QC, (109.2, 24.2), (108.0, 23.3), (106.9, 22.4)], "#27487f", 11, 3.5, 4.0, t1_i=12, w=5)
for k, p in enumerate([(110.0, 25.1), (110.5, 25.0), (110.2, 25.5)]):
    add("mark", A(12, 0.4 + .4 * k), E_(12), shape="boat", lon=p[0], lat=p[1], s=26, fi=0.3, fo=0.5)
add("mark", A(12, 3.2), E_(12), shape="x", lon=107.4, lat=22.7, s=24, fi=0.3, fo=0.5)
add("mark", A(12, 3.6), E_(12), shape="x", lon=106.2, lat=22.4, s=24, fi=0.3, fo=0.5)
fx("drum", A(11, 3.5), E_(12))
# 13–14: hai lối
add("mark", A(13, 0.3), E_(13), shape="q", lon=105.7, lat=21.6, s=40, fi=0.3, fo=0.4)
lab("chờ", (105.3, 21.4), "#555", 13, 13, fs=44, op=0.85)
lab("đánh trước", (107.6, 22.6), "#8a4a14", 13, 14, fs=44, op=0.9)
route("danh_truoc", [TL, (106.5, 21.7), (107.4, 22.4), UC], V, 14, 0.4, 4.0, w=8)
army([TL, (106.5, 21.7), (107.4, 22.4), UC], "v", 14, 1.0, 6.0, n=12, flag=True)
card("Tông Đản", "cùng Lý Thường Kiệt cất quân", 14, 0.3, 4.0)
city("Thăng Long", TL, "v", 10, 18, 28)
fx("horn", A(14, 1.0))
add("big", A(15, 0.4), E_(16), text="THANH MIÊU", col="#7a1f1f", fi=0.5, fo=0.8, y=560, fs=130)
card("Phép thanh miêu", "vay tiền khi lúa còn non, mùa gặt trả cả vốn lẫn lãi", 16, 0.4, 5.5, w=1500, col=SO)
add("big", A(17, 0.3), E_(17), text="?", col="#7a1f1f", fi=0.4, fo=0.6, y=640, fs=320)
card("Hai lý do", "danh nghĩa cứu dân, và mối đe dọa sát biên giới", 18, 0.6, 5.0, w=1300)
# ============ Chương 4: Đánh vào đâu (19–26) ============
C(19, 107.8, 22.0, 5.6); C(20, 108.5, 21.6, 3.0); C(21, 107.9, 22.1, 4.4); C(22, 107.6, 22.0, 5.6); C(24, 108.9, 23.6, 4.2); C(25, 108.8, 23.1, 1.6); C(26, 108.4, 22.8, 1.4); C(27, *UC, .55)
route("thuy", SEA, "#1f5f8b", 19, 0.8, 3.2, t1_i=26, w=7)
route("bo", LAND, V, 19, 0.8, 4.8, t1_i=26, w=7)
card("Đạo thủy", "Lý Thường Kiệt chỉ huy", 19, 1.0, 3.5, col="#1f5f8b")
army(SEA, "v", 19, 1.2, 5.0, n=8, t1_i=20, flag=True, u="ship")
army(LAND, "v", 19, 1.2, 7.0, n=14, t1_i=21, flag=True)
fx("horn", A(19, 0.9)); fx("water", A(19, 1.2), E_(20)); fx("march", A(19, 1.2), E_(21))
city("Khâm Châu", KC, "s", 19, 26, 28); city("Liêm Châu", LC, "s", 19, 26, 28); city("Ung Châu", UC, "s", 19, 26, 30)
add("ring", A(20, 0.8), E_(20), lon=KC[0], lat=KC[1], dur=1.6); add("ring", A(20, 2.6), E_(20), lon=LC[0], lat=LC[1], dur=1.6)
fx("clash", A(20, 0.8)); fx("clash", A(20, 2.6))
card("Tông Đản", "đạo bộ tiến về Ung Châu", 21, 0.3, 4.0)
add("mark", A(22, 0.3), E_(22), shape="q", lon=107.7, lat=22.4, s=40, fi=0.3, fo=0.4)
card("Trương Thủ Tiết", "quan trấn giữ Quảng Tây", 24, 0.3, 4.5, col=SO)
army([QC, (109.4, 24.4), CL], "s", 24, 0.5, 5.0, n=14, t1_i=25, flag=True)
add("mark", A(25, 0.2), E_(25), shape="dot", lon=CL[0] + .08, lat=CL[1] - .06, s=24, col=V, fi=0.4, fo=0.5)
city("ải Côn Lôn", CL, "v", 25, 25, 26)
add("ring", A(25, 3.5), E_(25), lon=CL[0], lat=CL[1], dur=1.8); fx("clash", A(25, 3.5)); fx("arrow", A(25, 2.6), A(25, 4.2))
add("mark", A(26, 0.3), E_(26), shape="x", lon=CL[0], lat=CL[1], s=24, fi=0.3, fo=0.5)
add("ring", A(26, 1.0), E_(26), lon=UC[0], lat=UC[1], col="#27487f", dur=2.0)

# ============ Chương 5: Bốn mươi ngày bên tường thành (27–33) ============
C(27, *UC, .55); C(28, *UC, .55); C(29, *UC, .55); C(30, *UC, .55); C(31, 108.1, 22.3, 3.0, 1.0); C(32, 107.8, 22.0, 5.0); C(33, 107.6, 21.9, 5.0)
add("siege", A(27), E_(31) + .5, ph=[[A(27), .15], [E_(27), .25], [A(28), .3], [E_(28) - 1.5, .68], [E_(28), .8], [A(29, 0.5), .85], [A(29, 2.0), .99], [E_(30), 1.0]])
card("Tô Giám", "tri châu Ung Châu", 27, 0.4, 4.0, col=SO)
chip("Hơn bốn mươi ngày", 27, 28, 640)
fx("drum", A(27), E_(28)); fx("fire", A(29, 1.5), E_(30))
add("chip", A(29), E_(30), text="Ung Châu thất thủ", w=640, fi=0.6, fo=0.5)
army([UC, (108.5, 22.4), KC], "v", 31, 0.5, 4.0, n=14, t1_i=31, stay=False, flag=True)
fx("march", A(31, 0.5), E_(31))
add("mark", A(32, 0.3), E_(32), shape="q", lon=107.6, lat=22.2, s=40, fi=0.3, fo=0.4)
route("rut", [UC, (107.3, 22.3), LS, TL], V, 33, 0.5, 4.0, w=5)
army([UC, (107.3, 22.3), LS, TL], "v", 33, 0.8, 5.0, n=12, flag=True)

# ============ Chương 6: Giữ sông bằng gì (34–44) ============
C(34, 109.7, 24.8, 5.0); C(35, 108.2, 20.5, 8.5); C(36, 108.8, 23.5, 6.2); C(37, 106.5, 21.6, 3.2); C(39, 106.3, 21.4, 2.0); C(41, 106.15, 21.3, 1.4); C(42, 106.08, 21.21, 1.0); C(44, 106.06, 21.2, 0.85); C(45, 106.06, 21.2, 0.85)
card("Quách Quỳ", "chiêu thảo sứ, thống lĩnh đại quân", 34, 0.5, 4.5, col=SO)
route("cc", [(105.4, 17.9), (105.7, 19.0), TL], "#6a6a6a", 35, 0.5, 4.0, t1_i=35, w=4); route("cc2", [(103.4, 17.9), (104.6, 19.2), (105.5, 20.5), TL], "#6a6a6a", 35, 1.2, 4.0, t1_i=35, w=4)
lab("Chiêm Thành", (106.6, 17.9), "#555", 35, 35, fs=34, op=0.85, it=True, ls=2); lab("Chân Lạp", (103.4, 18.2), "#555", 35, 35, fs=34, op=0.85, it=True, ls=2)
route("tong_nam", TONG_ROAD, "#27487f", 36, 0.5, 4.5, t1_i=37, w=8)
army(TONG_ROAD, "s", 36, 0.8, 6.0, n=24, t1_i=37, flag=True)
fx("march", A(36, 0.8), E_(37)); fx("drum", A(36, 0.8), E_(37))
city("Thăng Long", TL, "v", 36, 40, 28)
add("label", A(37, 1.2), E_(38), lon=106.4, lat=21.5, text="sông Như Nguyệt", col="#2c4f6b", fs=32, op=0.9, it=True, ls=2, sw=6, fi=.5, fo=.5)
card("Như Nguyệt", "tức sông Cầu ngày nay", 37, 0.8, 4.0, col="#1f5f8b")
add("mark", A(38, 0.3), E_(38), shape="q", lon=106.2, lat=21.35, s=40, fi=0.3, fo=0.4)
# trận Như Nguyệt: hàng rào từ đoạn 40, tiến công ở đoạn 43–44
add("river", A(40, 0.5), E_(48) + 2.5, fence=1.0, arrive=2.4, waves=[[A(43, 0.8), A(43, 3.0)], [A(43, 4.2), A(43, 6.4)], [A(44, 0.3), A(44, 2.6)]], sick=A(49, 1.5))
fx("water", A(40), E_(44)); fx("arrow", A(43, 0.8), E_(44)); fx("clash", A(43, 1.9)); fx("clash", A(43, 5.3)); fx("clash", A(44, 1.5))
add("chip", A(36), E_(44), text="Cuối năm 1076", w=560, fi=0.6, fo=0.5)
card("Quân Tống", "bờ bắc, phải xuống nước trước hàng rào", 43, 0.4, 4.0, col=SO, x=1000, y=170, w=800)

# ============ Chương 7: Bài thơ bên sông (45–48) ============
add("night", A(45, 0.3), E_(48) - 0.5, a=0.62, moon=True, fi=1.5, fo=1.5)
add("poem", A(46, 0.2), E_(47), lines=["Nam quốc sơn hà Nam đế cư", "Tiệt nhiên định phận tại thiên thư", "Như hà nghịch lỗ lai xâm phạm", "Nhữ đẳng hành khan thủ bại hư"], gap=2.0, fi=0.8, fo=1.4)
card("Đền hai anh em họ Trương", "theo truyền thuyết", 45, 0.8, 4.5, col="#8a8a8a")
fx("insect", A(45), E_(48)); fx("wind", A(45), E_(48))
# ============ Chương 8: Khi nào thì dừng (49–53) ============
C(49, 106.06, 21.2, 0.85); C(50, 106.2, 21.4, 1.4, 0.5); C(51, 106.3, 21.7, 3.0); C(52, 106.8, 22.4, 5.0); C(53, 106.5, 22.6, 4.0)
add("sick", A(49, 1.0), E_(49) + 3.5, fi=1.2, fo=1.5)
add("mark", A(50, 0.4), E_(51), shape="flag", lon=106.15, lat=21.3, s=30, col="#ffffff", fi=.4, fo=.6)
add("mark", A(50, 0.6), E_(50), shape="q", lon=106.1, lat=21.35, s=36, fi=.3, fo=.4)
route("lui", [(106.3, 21.4), LS, (107.3, 22.3), UC, QC], "#27487f", 52, 0.3, 4.0, w=6)
city("Quảng Nguyên", QN, "v", 52, 59, 26); city("Tư Lang", (106.6, 22.9), "v", 53, 53, 24); city("Tô Mậu", (106.0, 22.1), "v", 53, 53, 24)
add("area", A(52, 2.5), E_(53) + 4, pts=[[106.0, 22.3], [106.6, 22.95], [106.7, 22.4], [106.3, 22.0]], col="#27487f", op=0.3, fi=1.0, fo=1.0)

# ============ Chương 9: Đòi lại đất (54–59) ============
C(54, 107.0, 23.5, 10.0); C(57, 106.5, 22.5, 4.0); C(58, 107.4, 22.2, 4.5); C(59, 106.9, 22.2, 3.0)
route("voi", [TL, (106.2, 22.0), (107.0, 23.4), (107.5, 25.6)], V, 54, 0.4, 5.0, t1_i=54, w=6)
army([TL, (106.2, 22.0), (107.0, 23.4), (107.5, 25.6)], "v", 54, 0.6, 6.0, n=5, t1_i=54, flag=True)
lab("kinh đô nhà Tống (rất xa về phía bắc)", (107.4, 26.0), "#27487f", 54, 54, fs=30, op=0.85, it=True, ls=1)
card("Đào Tống Nguyên", "mang năm con voi thuần sang biếu", 54, 0.5, 4.5)
chip("Năm 1078", 54, 56, 400); chip("Năm 1079", 57, 57, 400); chip("Năm 1081", 58, 58, 400); chip("Năm 1084", 59, 59, 400)
add("area", A(57, 1.0), E_(57), pts=[[106.0, 22.3], [106.6, 22.95], [106.7, 22.4], [106.3, 22.0]], col=V, op=0.4, fi=1.0, fo=0.5)
add("label", A(57, 1.5), E_(57), lon=106.3, lat=22.2, text="Thuận Châu", col="#8a4a14", fs=34, op=0.95, fi=.6, fo=.5, sw=6)
army([UC, (107.3, 22.3), LS], "v", 58, 0.4, 5.0, n=10, stay=False, flag=False)
city("trại Vĩnh Bình", (106.75, 22.15), "s", 59, 59, 24)
add("area", A(59, 3.5), E_(59) + 2, pts=[[106.2, 22.6], [107.0, 22.9], [107.1, 22.2], [106.5, 22.1]], col=V, op=0.35, fi=1.0, fo=1.0)
card("Sáu huyện và ba động", "nhà Tống phải trả", 59, 3.0, 4.0)
# ============ Chương 10: Những năm cuối (60–64) ============
C(60, *TL, 1.8); C(61, 105.6, 19.6, 6.0); C(63, 106.3, 18.8, 6.5); C(64, *TL, 1.5)
card("Thái úy", "giữ binh quyền cả nước", 60, 0.5, 4.0)
city("Diễn Châu", (105.6, 19.0), "v", 61, 62, 28)
chip("Năm 1103", 61, 62, 400); chip("Năm 1104", 63, 63, 400); chip("Năm 1105", 64, 64, 400)
add("mark", A(61, 3.0), E_(62), shape="flag", lon=105.6, lat=19.05, s=34, col="#b3261e", fi=.5, fo=.6)
army([TL, (105.8, 20.2), (105.6, 19.0)], "v", 62, 0.4, 5.0, n=14, flag=True)
route("ca", [(105.6, 19.0), (106.2, 18.3), (106.5, 17.7)], "#b3261e", 62, 3.5, 3.0, w=5)
lab("Chiêm Thành", (106.6, 18.0), "#555", 63, 63, fs=34, op=0.85, it=True, ls=2)
army([TL, (105.8, 20.2), (106.0, 19.0), (106.5, 17.8)], "v", 63, 1.0, 5.5, n=14, t1_i=63, flag=True)
add("ring", A(63, 6.5), E_(63), lon=106.5, lat=17.9, dur=1.6, col="#2b7a3a")
card("Lý Thường Kiệt qua đời", "mùa hạ, tháng sáu năm 1105", 64, 3.0, 5.0)
fx("march", A(62, 0.4), E_(63)); fx("gong", A(64, 3.0))
# ============ Chương 11: Trở lại bên sông (65–68) ============
C(65, 107.0, 22.4, 6.0); C(66, 107.4, 22.5, 5.0); C(67, 106.6, 21.9, 4.0); C(68, 106.1, 21.25, 1.2)
route("hai1", [(105.9, 21.1), LS, UC], V, 65, 0.3, 3.5, t1_i=66, w=7)
route("hai2", [(106.9, 22.2), (106.4, 21.4), (106.1, 21.25)], "#1f5f8b", 66, 3.0, 2.5, t1_i=67, w=7)
add("big", A(65, 0.2), E_(65) - 0.4, text="HAI TRẬN", col="#7a1f1f", fi=0.5, fo=0.6, y=560, fs=150)
card("Hai nước cờ", "của cùng một người", 67, 0.5, 5.0)
add("night", A(68, 0.0), TOTAL - 0.1, a=0.55, moon=True, fi=1.5, fo=1.0)
add("poem", A(68, 0.4), TOTAL - 0.1, lines=["Nam quốc sơn hà Nam đế cư", "Tiệt nhiên định phận tại thiên thư"], gap=1.6, fi=0.8, fo=1.0)
fx("insect", A(68), TOTAL); fx("wind", A(68), TOTAL)

# ---- camera: thêm khóa đầu / cuối và sắp theo thời gian ----
cam.sort(key=lambda k: k[0])
if cam[0][0] > 0:
    cam.insert(0, [0.0] + cam[0][1:])
cam.append([TOTAL] + cam[-1][1:])
# bộ ghi nhớ: giữ camera đứng yên trong cùng một đoạn nếu không có khóa mới (khóa liên tiếp tự nội suy)
SPEC = {"dur": round(TOTAL, 2), "cam": cam, "items": items, "fade0": 1.0, "fade1": 3.0, "starts": {i: round(S[i], 2) for i in S}}
(HERE / "spec.js").write_text("window.SPEC=" + json.dumps(SPEC, ensure_ascii=False) + ";", encoding="utf-8")
json.dump({"dur": TOTAL, "sfx": sfx, "starts": {i: S[i] for i in S}, "durs": {i: D[i] for i in D}}, open(HERE / "sfx.json", "w"), indent=1)
print("tổng", round(TOTAL, 1), "giây =", round(TOTAL / 60, 2), "phút;", len(items), "mục hình;", len(sfx), "mục âm thanh")
