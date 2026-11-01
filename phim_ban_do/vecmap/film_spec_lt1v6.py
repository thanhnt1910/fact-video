"""Dựng bảng cảnh cho video Lý Thường Kiệt (lt1v6): thời điểm từng đoạn theo giọng đọc thật -> spec.js (hình) + sfx.json (âm thanh).
Chạy: python phim_ban_do/vecmap/film_spec.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KB = json.load(open(ROOT / "ke-hoach/thu-giong-hai/lt1v6_full.json", encoding="utf-8"))
DUR = json.load(open(ROOT / "assets/thu_giong_hai/lt1v6_chuan/thoi_luong.json"))
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


def volley(a, b, i0, i1, off=0.0, n=14, h=60, col=None, sp=0.7):
    d = add("volley", A(i0, off), E_(i1), a=list(a), b=list(b), n=n, h=h, sp=sp, fi=0.3, fo=0.5)
    if col:
        d["col"] = col


def lab(text, p, col, i0, i1, fs=46, op=0.6, **kw):
    add("label", A(i0), E_(i1), lon=p[0], lat=p[1], text=text, col=col, fs=fs, op=op, fi=0.8, fo=0.8, **kw)


# thời lượng bắt đầu/kết thúc một khoảng đoạn
SPAN = lambda i0, i1: E_(i1) - A(i0)
def cc(scene, i0, i1, lon, lat, wd=0.2, zin=3.2, zout=2.0, breach=None, **kw):
    """Cận cảnh trên bản đồ: camera zoom vào (lon,lat) ở đầu đoạn i0, giữ đến cuối đoạn i1 rồi zoom ra."""
    ts = A(i0) + zin - 0.4
    sp = (breach / (0.78 * (E_(i1) - ts))) if breach else 0.5
    cam.append([A(i0), lon, lat, 1.0]); cam.append([A(i0) + zin, lon, lat, wd]); cam.append([E_(i1) - 0.2, lon + 0.002, lat - 0.004, wd * 0.96])
    add("cc", A(i0) - 0.2, E_(i1) + 0.6, scene=scene, lon=lon, lat=lat, ts=ts, sp=round(sp, 4), fi=0.8, fo=0.6)


# ============ Chương 1: Hai nước cờ — hook (1–6) ============
C(1, *UC, 0.55); C(2, *UC, 0.55); C(3, 107.2, 22.4, 6.0); C(4, 106.9, 21.9, 8.6); C(5, 106.9, 21.9, 8.6); C(6, 106.6, 21.9, 7.5)
add("siege", 0, E_(2) + 0.2, ph=[[0, .97], [E_(1), .97], [A(2), .45], [E_(2), .6]])
add("chip", A(1), E_(2), text="Ung Châu, năm 1075", w=700, fi=0.6, fo=0.4)
fx("fire", A(1), E_(1)); fx("drum", A(2), E_(2))
lab("ĐẠI VIỆT", (105.0, 21.2), "#8a4a14", 3, 6, fs=54); lab("TỐNG", (109.2, 24.3), "#27487f", 3, 6, fs=54)
route("ra_khoi", [(105.8, 21.1), (106.6, 21.9), UC], V, 3, 0.5, 4.0, t1_i=3, w=7)
add("big", A(5, 0.2), A(5, 3.4), text="?", col="#7a1f1f", fi=0.4, fo=0.8, y=620, fs=300)
# ============ Chương 2: Người cầm cờ tiết (7–18) ============
C(7, *TL, 1.1); C(9, *TL, 1.8); C(13, 105.9, 20.2, 7.0); C(16, *TL, 1.8); C(17, 108.0, 23.2, 6.0)
city("Thăng Long", TL, "v", 7, 18, 28)
card("Phường Thái Hòa", "kinh thành Thăng Long", 7, 0.6, 4.0)
add("army", A(8, 0.3), E_(8), pts=[list(TL), [105.55, 21.2], [105.95, 21.4], [106.3, 21.1], list(TL)], side="v", n=3, dur=6.5, stay=True, flag=False, u="cav", fi=0.2, fo=0.6)
route("champa", [TL, (105.8, 20.2), (106.0, 19.0), (106.4, 18.0)], V, 13, 0.4, 5.0, t1_i=14, w=6)
army([TL, (105.8, 20.2), (106.0, 19.0), (106.4, 18.0)], "v", 13, 0.6, 5.5, n=16, t1_i=14, flag=False)
lab("hướng Chiêm Thành", (106.7, 18.4), "#8a4a14", 13, 14, fs=34, op=0.8, it=True, ls=2)
chip("Năm 1069", 13, 14, 400); chip("Năm 1075", 16, 16, 400)
card("Thái úy", "một trong những chức quân sự cao nhất", 16, 0.5, 4.5)
add("mark", A(17, 0.5), E_(18), shape="arrow", lon=107.4, lat=23.4, s=26, col="#b3261e", ang=125, fi=0.3, fo=0.5)
fx("march", A(13, 0.6), E_(14)); fx("horn", A(17, 0.5))
# ============ Chương 3: Chờ hay đánh (19–32) ============
C(19, 109.6, 24.7, 5.5); C(23, 109.9, 24.9, 4.5); C(25, 107.2, 22.1, 6.0); C(28, 107.2, 22.1, 6.0); C(30, 107.4, 22.6, 7.0)
lab("TỐNG", (111.3, 25.9), "#27487f", 19, 24, fs=52)
city("Quế Châu", QC, "s", 19, 24, 30)
card("Vương An Thạch", "người cải cách của nhà Tống", 21, 0.5, 4.5, col=SO)
card("Thẩm Khởi, Lưu Di", "hai quan nhà Tống ở biên giới", 24, 0.6, 5.5, col=SO)
route("tong_doa", [QC, (109.2, 24.2), (108.0, 23.3), (106.9, 22.4)], "#27487f", 23, 3.5, 4.0, t1_i=24, w=5)
for k, p in enumerate([(110.0, 25.1), (110.5, 25.0), (110.2, 25.5)]):
    add("mark", A(24, 3.0 + .4 * k), E_(24), shape="boat", lon=p[0], lat=p[1], s=26, fi=0.3, fo=0.5)
fx("drum", A(23, 3.5), E_(24))
add("mark", A(25, 0.3), E_(26), shape="q", lon=105.7, lat=21.6, s=40, fi=0.3, fo=0.4)
lab("chờ", (105.3, 21.4), "#555", 25, 26, fs=44, op=0.85)
lab("đánh trước", (107.6, 22.6), "#8a4a14", 25, 27, fs=44, op=0.9)
add("big", A(27, 0.3), E_(27), text="?", col="#7a1f1f", fi=0.4, fo=0.6, y=640, fs=320)
route("danh_truoc", [TL, (106.5, 21.7), (107.4, 22.4), UC], V, 28, 0.4, 4.0, t1_i=29, w=8)
army([TL, (106.5, 21.7), (107.4, 22.4), UC], "v", 28, 1.0, 6.0, n=12, t1_i=29, flag=False)
card("Lý Thường Kiệt", "chỉ huy chiến dịch", 29, 0.4, 4.5)
fx("horn", A(28, 1.0))
add("big", A(30, 0.2), E_(30), text="THANH MIÊU", col="#7a1f1f", fi=0.5, fo=0.8, y=560, fs=130)
card("Phép thanh miêu", "bắt dân vay tiền, trả cả vốn lẫn lãi", 30, 2.0, 4.5, w=1300, col=SO)
# ============ Chương 4: Đánh vào đâu (33–40) ============
C(33, 107.8, 22.0, 5.6); C(35, 108.5, 21.6, 3.0); C(36, 107.9, 22.1, 4.4); C(38, 108.75, 23.15, 2.4); C(39, 108.4, 22.8, 1.6); C(40, *UC, 0.55)
route("thuy", SEA, "#1f5f8b", 33, 0.8, 3.2, t1_i=35, w=7); route("bo", LAND, V, 33, 0.8, 4.8, t1_i=36, w=7)
army(SEA, "v", 34, 0.4, 5.0, n=8, t1_i=35, flag=False, u="ship"); army(LAND, "v", 36, 0.4, 7.0, n=14, t1_i=37, flag=False)
fx("horn", A(33, 0.9)); fx("water", A(34, 0.4), E_(35)); fx("march", A(36, 0.4), E_(37))
city("Khâm Châu", KC, "s", 34, 40, 28); city("Liêm Châu", LC, "s", 34, 40, 28); city("Ung Châu", UC, "s", 36, 40, 30)
add("ring", A(35, 0.6), E_(35), lon=KC[0], lat=KC[1], dur=1.6); add("ring", A(35, 2.4), E_(35), lon=LC[0], lat=LC[1], dur=1.6)
add("fire", A(35, 1.0), E_(40), lon=KC[0], lat=KC[1], s=20, fi=0.6, fo=0.8); add("fire", A(35, 2.8), E_(40), lon=LC[0], lat=LC[1], s=20, fi=0.6, fo=0.8)
fx("clash", A(35, 0.6)); fx("clash", A(35, 2.4))
city("ải Côn Lôn", CL, "v", 38, 39, 26)
army([QC, (109.4, 24.4), CL], "s", 38, 0.3, 4.0, n=14, t1_i=38, flag=False)
add("ring", A(38, 3.0), E_(39), lon=CL[0], lat=CL[1], dur=1.8); fx("clash", A(38, 3.0)); fx("arrow", A(38, 2.2), A(38, 4.0))
volley((CL[0] + .15, CL[1] - .12), (CL[0] - .02, CL[1] + .02), 38, 38, 2.0, n=14, h=70)
add("ring", A(39, 0.5), E_(39), lon=UC[0], lat=UC[1], col="#27487f", dur=2.0)
add("big", A(40, 0.2), A(40, 3.0), text="?", col="#7a1f1f", fi=0.4, fo=0.8, y=620, fs=260)
# ============ Chương 5: Bốn mươi ngày (41–53) ============
C(41, *UC, 0.55); C(48, *UC, 0.55); C(50, 108.1, 22.3, 3.0, 1.0); C(52, 107.8, 22.0, 5.0)
add("chip", A(41), E_(42), text="Ung Châu, đầu năm 1076", w=860, fi=0.6, fo=0.5)
add("siege", A(41), E_(42) + 0.3, ph=[[A(41), .15], [E_(42), .3]])
cc("uc", 43, 49, *UC, wd=0.2, breach=14.2)
add("big", A(47, 0.5), A(47, 4.0), text="40 NGÀY", col="#7a1f1f", fi=0.5, fo=0.8, y=140, fs=120)
fx("drum", A(41), E_(42)); fx("fire", A(47, 2.0), E_(49))
add("chip", A(47), E_(49), text="Ung Châu thất thủ", w=720, fi=0.6, fo=0.5)
army([UC, (108.5, 22.4), KC], "v", 50, 0.5, 4.0, n=14, t1_i=50, stay=False, flag=False)
fx("march", A(50, 0.5), E_(50))
route("rut", [UC, (107.3, 22.3), LS, TL], V, 52, 0.5, 4.0, w=5); army([UC, (107.3, 22.3), LS, TL], "v", 52, 0.8, 5.0, n=12, flag=False)
add("mark", A(53, 0.3), E_(53), shape="q", lon=106.9, lat=21.9, s=40, fi=0.3, fo=0.4)
# ============ Chương 6: Giữ sông bằng gì (54–68) ============
C(54, 109.7, 24.8, 5.0); C(56, 108.8, 23.5, 6.2); C(57, 106.5, 21.6, 3.2); C(58, 106.3, 21.4, 2.0); C(59, 106.15, 21.3, 1.4); C(60, 106.08, 21.21, 1.0)
card("Quách Quỳ", "chỉ huy bộ binh nhà Tống", 55, 0.5, 4.5, col=SO)
route("tong_nam", [QC, (109.2, 24.2), UC, (107.3, 22.3), LS, (106.3, 21.4)], "#27487f", 54, 0.4, 7.0, t1_i=56, w=7)
army([QC, (109.2, 24.2), UC, (107.3, 22.3), LS, (106.3, 21.4)], "s", 54, 1.0, 9.0, n=18, t1_i=56, flag=False)
city("sông Như Nguyệt", (106.05, 21.19), "v", 57, 60, 28)
add("river", A(58, 0.5), E_(60) + 1.0, fence=1.0, arrive=2.4, waves=[[A(60, 2.0), A(60, 5.0)], [A(60, 6.0), A(60, 9.0)], [A(60, 9.5), A(60, 12.5)]], sick=A(68, 0.5))
fx("water", A(57), E_(60))
cc("nn", 61, 66, 106.05, 21.19, wd=0.2)
fx("arrow", A(62, 1.5), E_(64)); fx("clash", A(63, 1.0)); fx("clash", A(64, 2.0))
C(67, 106.06, 21.2, 0.85); C(68, 106.06, 21.2, 0.85)
add("sick", A(68, 0.3), E_(68) + 3.5, fi=1.2, fo=1.5)
# ============ Chương 7: Bài thơ bên sông (69–77) ============
C(69, 106.06, 21.2, 0.85)
add("night", A(69, 0.3), E_(77) - 0.5, a=0.62, moon=True, fi=1.5, fo=1.5)
add("poem", A(71, 0.2), E_(71), lines=["Nam quốc sơn hà Nam đế cư", "Tiệt nhiên định phận tại thiên thư", "Như hà nghịch lỗ lai xâm phạm", "Nhữ đẳng hành khan thủ bại hư"], gap=2.4, fi=0.5, fo=0.8)
card("Đền hai anh em họ Trương", "theo truyền thuyết", 72, 0.8, 4.5, col="#8a8a8a")
fx("insect", A(69), E_(77)); fx("wind", A(69), E_(77))
# ============ Chương 8: Khi nào thì dừng (78–86) ============
C(78, 106.06, 21.2, 0.85); C(80, 106.2, 21.4, 1.4, 0.5); C(84, 106.3, 21.7, 3.0); C(86, 106.8, 22.4, 5.0)
add("mark", A(84, 0.4), E_(85), shape="flag", lon=106.15, lat=21.3, s=30, col="#ffffff", fi=.4, fo=.6)
add("mark", A(81, 0.4), E_(81), shape="q", lon=106.1, lat=21.35, s=36, fi=.3, fo=.4)
route("lui", [(106.3, 21.4), LS, (107.3, 22.3), UC, QC], "#27487f", 86, 0.3, 4.0, w=6)
# ============ Chương 9: Đòi lại đất (87–97) ============
C(87, 107.0, 23.5, 10.0); C(92, 106.5, 22.5, 4.0); C(93, 107.4, 22.2, 4.5)
city("Quảng Nguyên", QN, "v", 90, 97, 26)
route("voi", [TL, (106.2, 22.0), (107.0, 23.4), (107.5, 25.6)], V, 89, 0.4, 5.0, t1_i=89, w=6)
army([TL, (106.2, 22.0), (107.0, 23.4), (107.5, 25.6)], "v", 89, 0.6, 6.0, n=5, t1_i=89, flag=False)
lab("nơi triều đình nhà Tống ở (rất xa về phía bắc)", (107.4, 26.0), "#27487f", 89, 89, fs=30, op=0.85, it=True, ls=1)
card("Đào Tống Nguyên", "mang năm con voi sang thương lượng", 89, 0.5, 4.5)
chip("Năm 1078", 89, 89, 400); chip("Năm 1079", 90, 91, 400); chip("Năm 1081", 92, 92, 400); chip("Năm 1084", 93, 94, 400)
add("area", A(90, 1.0), E_(90), pts=[[106.0, 22.3], [106.6, 22.95], [106.7, 22.4], [106.3, 22.0]], col=V, op=0.4, fi=1.0, fo=0.5)
add("label", A(90, 1.5), E_(90), lon=106.3, lat=22.2, text="Thuận Châu", col="#8a4a14", fs=34, op=0.95, fi=.6, fo=.5, sw=6)
add("area", A(93, 2.0), E_(94) + 1, pts=[[106.2, 22.6], [107.0, 22.9], [107.1, 22.2], [106.5, 22.1]], col=V, op=0.35, fi=1.0, fo=1.0)
card("Một số huyện và động", "số cụ thể còn cần đối chiếu", 94, 0.2, 3.5)
# ============ Chương 10: Những năm cuối (98–105) ============
C(98, *TL, 1.8); C(100, 105.6, 19.6, 6.0); C(101, 106.3, 18.8, 6.5); C(103, *TL, 1.5)
card("Thái úy", "giữ trọng trách trong triều", 98, 0.5, 4.0)
city("Diễn Châu", (105.6, 19.0), "v", 100, 100, 28)
chip("Năm 1103", 100, 100, 400); chip("Năm 1104", 101, 102, 400); chip("Năm 1105", 104, 104, 400)
army([TL, (105.8, 20.2), (105.6, 19.0)], "v", 100, 0.4, 4.0, n=14, t1_i=100, flag=False)
lab("Chiêm Thành", (106.6, 18.0), "#555", 101, 102, fs=34, op=0.85, it=True, ls=2)
army([TL, (105.8, 20.2), (106.0, 19.0), (106.5, 17.8)], "v", 102, 0.4, 5.5, n=14, t1_i=102, flag=False)
card("Lý Thường Kiệt qua đời", "năm 1105", 104, 0.4, 5.0)
fx("march", A(100, 0.4), E_(102)); fx("gong", A(104, 0.4))
# ============ Chương 11: Trở lại bên sông (106–115) ============
C(106, 107.0, 22.4, 6.0); C(108, 106.6, 21.9, 4.0); C(111, 106.6, 21.9, 4.0); C(114, 106.1, 21.25, 1.2)
route("hai1", [(105.9, 21.1), LS, UC], V, 107, 0.3, 3.5, t1_i=108, w=7)
route("hai2", [(106.9, 22.2), (106.4, 21.4), (106.1, 21.25)], "#1f5f8b", 108, 1.0, 2.5, t1_i=110, w=7)
card("Hai nước cờ", "của cùng một người", 109, 0.5, 5.0)
add("night", A(114, 0.0), TOTAL - 0.1, a=0.55, moon=True, fi=1.5, fo=1.0)
add("poem", A(114, 0.4), TOTAL - 0.1, lines=["Nam quốc sơn hà Nam đế cư", "Tiệt nhiên định phận tại thiên thư"], gap=1.6, fi=0.8, fo=1.0)
fx("insect", A(114), TOTAL); fx("wind", A(114), TOTAL)

# ---- camera: thêm khóa đầu / cuối và sắp theo thời gian ----
cam.sort(key=lambda k: k[0])
if cam[0][0] > 0:
    cam.insert(0, [0.0] + cam[0][1:])
cam.append([TOTAL] + cam[-1][1:])
# bộ ghi nhớ: giữ camera đứng yên trong cùng một đoạn nếu không có khóa mới (khóa liên tiếp tự nội suy)
SPEC = {"dur": round(TOTAL, 2), "cam": cam, "items": items, "fade0": 1.0, "fade1": 3.0, "starts": {i: round(S[i], 2) for i in S}}
(HERE / "spec_lt1v6.js").write_text("window.SPEC=" + json.dumps(SPEC, ensure_ascii=False) + ";", encoding="utf-8")
json.dump({"dur": TOTAL, "sfx": sfx, "starts": {i: S[i] for i in S}, "durs": {i: D[i] for i in D}}, open(HERE / "sfx_lt1v6.json", "w"), indent=1)
print("tổng", round(TOTAL, 1), "giây =", round(TOTAL / 60, 2), "phút;", len(items), "mục hình;", len(sfx), "mục âm thanh")

