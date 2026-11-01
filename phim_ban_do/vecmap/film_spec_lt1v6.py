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
    add("chip", A(i0), E_(i1), text=text, w=w, fi=0.6, fo=0.6, y=130)


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



SPAN = lambda i0, i1: E_(i1) - A(i0)
def cc(scene, i0, i1, lon, lat, wd=0.15, zin=3.0, zout=1.8, w0=1.0, breach=None, **kw):
    """Cận cảnh trên bản đồ cho đoạn i0..i1: camera zoom từ bản đồ vào (lon,lat), giữ, rồi zoom ra."""
    ts = A(i0) + zin - 0.4
    sp = kw.pop("sp", None) or ((breach / (0.78 * (E_(i1) - ts))) if breach else 1.0)
    cam.append([A(i0), lon, lat, w0]); cam.append([A(i0) + zin, lon, lat, wd]); cam.append([E_(i1) - zout, lon + 0.002, lat - 0.004, wd * 0.96]); cam.append([E_(i1) + 0.1, lon, lat, 0.7])
    add("cc", A(i0) - 0.2, E_(i1) + 0.6, scene=scene, lon=lon, lat=lat, ts=ts, sp=round(sp, 4), fi=0.8, fo=0.6, **kw)

NNP = (106.05, 21.19); CHM = (106.4, 18.0); TLP = TL
# ===== Chương 1: hook (1–6) =====
cc("uc", 1, 2, *UC, zin=0.6, w0=0.25, tau0=16, sp=0.35)
add("chip", A(1), E_(2), text="Ung Châu, năm 1075", w=700, fi=0.6, fo=0.4, y=130)
cc("march", 3, 4, 106.4, 21.5, side="v", n=12, dir=1, carry=1)
cc("nn", 5, 6, *NNP, sp=0.1)
add("big", A(5, 0.2), A(5, 3.4), text="?", col="#7a1f1f", fi=0.4, fo=0.8, y=200, fs=260)
# ===== Chương 2: Người cầm cờ tiết (7–18) =====
cc("tl", 7, 12, *TLP, tau0=2, badge=1)
card("Phường Thái Hòa", "kinh thành Thăng Long", 7, 3.2, 4.0)
cc("bien", 13, 14, *CHM, tau0=0)
chip("Năm 1069", 13, 14, 400)
cc("tl", 15, 18, *TLP, tau0=40, badge=1)
chip("Năm 1075", 16, 16, 400); card("Thái úy", "một trong những chức quân sự cao nhất", 16, 3.2, 4.5)
# ===== Chương 3: Chờ hay đánh (19–32) =====
cc("camp", 19, 22, *QC, tau0=3)
card("Vương An Thạch", "người cải cách của nhà Tống", 21, 3.0, 4.5, col=SO)
cc("xuong", 23, 24, *QC)
cc("tl", 25, 27, *TLP, tau0=90)
add("big", A(27, 0.3), E_(27), text="?", col="#7a1f1f", fi=0.4, fo=0.6, y=200, fs=260)
cc("march", 28, 29, 106.4, 21.5, side="v", n=14, dir=1, badge=dict(kind="v", name="Lý Thường Kiệt", sub="chỉ huy chiến dịch"))
cc("tl", 30, 32, 105.2, 21.5, tau0=150)
add("big", A(30, 0.5), A(30, 3.5), text="THANH MIÊU", col="#7a1f1f", fi=0.5, fo=0.8, y=160, fs=110)
card("Phép thanh miêu", "bắt dân vay tiền, trả cả vốn lẫn lãi", 31, 0.4, 4.5, w=1300, col=SO)
# ===== Chương 4: Đánh vào đâu (33–40) =====
cc("bien", 33, 35, *KC, tau0=0)
chip("Khâm Châu và Liêm Châu", 33, 35, 760)
cc("march", 36, 37, 108.0, 22.6, side="v", n=14, dir=1, carry=1)
cc("ai", 38, 39, *CL)
chip("Cửa ải Côn Lôn", 38, 39, 640)
cc("uc", 40, 40, *UC, tau0=0, sp=0.05)
add("big", A(40, 0.3), A(40, 3.0), text="?", col="#7a1f1f", fi=0.4, fo=0.8, y=200, fs=240)
# ===== Chương 5: Bốn mươi ngày (41–53) =====
cc("uc", 41, 49, *UC, breach=14.2)
add("chip", A(41), E_(42), text="Ung Châu, đầu năm 1076", w=860, fi=0.6, fo=0.5, y=130)
add("big", A(47, 0.5), A(47, 4.0), text="40 NGÀY", col="#7a1f1f", fi=0.5, fo=0.8, y=140, fs=120)
cc("march", 50, 53, 107.3, 22.3, side="v", n=12, dir=-1, carry=1)
# ===== Chương 6: Giữ sông bằng gì (54–68) =====
cc("march", 54, 56, 108.0, 23.0, side="s", n=16, dir=1, badge=dict(kind="s", name="Quách Quỳ", sub="chỉ huy bộ binh nhà Tống"))
add("chip", A(54), E_(56), text="Năm 1076", w=400, fi=0.6, fo=0.5, y=130)
cc("nn", 57, 60, *NNP, sp=0.16)
add("chip", A(57), E_(60), text="Sông Như Nguyệt", w=620, fi=0.6, fo=0.5, y=130)
cc("nn", 61, 66, *NNP, sp=0.45, tau0=4)
cc("camp", 67, 68, 106.0, 21.3, tau0=20)
add("sick", A(67, 0.5), E_(68) + 2.0, fi=1.2, fo=1.5)
# ===== Chương 7: Bài thơ bên sông (69–77) =====
cc("den", 69, 77, 106.05, 21.2)
add("night", A(69, 0.5), E_(77) - 0.5, a=0.55, moon=True, fi=1.5, fo=1.5)
add("poem", A(71, 0.2), E_(71), lines=["Nam quốc sơn hà Nam đế cư", "Tiệt nhiên định phận tại thiên thư", "Như hà nghịch lỗ lai xâm phạm", "Nhữ đẳng hành khan thủ bại hư"], gap=2.4, fi=0.5, fo=0.8)
card("Đền hai anh em họ Trương", "theo truyền thuyết", 72, 0.8, 4.5, col="#8a8a8a")
fx("insect", A(69), E_(77)); fx("wind", A(69), E_(77))
# ===== Chương 8: Khi nào thì dừng (78–86) =====
cc("camp", 78, 80, 106.2, 21.4, tau0=40)
cc("dam", 81, 85, 106.25, 21.5)
cc("march", 86, 86, 106.8, 22.4, side="s", n=14, dir=-1)
# ===== Chương 9: Đòi lại đất (87–97) =====
cc("voi", 87, 89, 107.0, 23.4)
card("Đào Tống Nguyên", "mang năm con voi sang thương lượng", 89, 0.3, 4.0)
chip("Năm 1078", 87, 89, 400)
cc("giao", 90, 91, *QN)
chip("Năm 1079", 90, 91, 400)
cc("giao", 92, 94, 107.4, 22.2, tau0=30)
chip("Năm 1081 và 1084", 92, 94, 640)
card("Một số huyện và động", "số cụ thể còn cần đối chiếu", 94, 0.2, 3.5)
cc("tl", 95, 97, *TLP, tau0=200)
# ===== Chương 10: Những năm cuối (98–105) =====
cc("tl", 98, 99, *TLP, tau0=260, badge=1)
card("Thái úy", "giữ trọng trách trong triều", 98, 3.0, 4.0)
cc("march", 100, 100, 105.6, 19.0, side="v", n=12, dir=1)
chip("Năm 1103", 100, 100, 400)
cc("bien", 101, 102, *CHM, tau0=0)
chip("Năm 1104", 101, 102, 400)
cc("tl", 103, 103, *TLP, tau0=320)
cc("nha", 104, 105, *TLP)
chip("Năm 1105", 104, 105, 400)
fx("gong", A(104, 0.4))
# ===== Chương 11: Trở lại bên sông (106–115) =====
cc("uc", 106, 107, *UC, tau0=0, sp=0.5)
cc("nn", 108, 109, *NNP, sp=0.5, tau0=4)
card("Hai nước cờ", "của cùng một người", 109, 0.5, 5.0)
cc("tl", 110, 111, *TLP, tau0=380)
cc("camp", 112, 113, 106.0, 21.3, tau0=60)
cc("den", 114, 115, 106.05, 21.2)
add("night", A(114, 0.0), TOTAL - 0.1, a=0.55, moon=True, fi=1.5, fo=1.0)
add("poem", A(114, 0.4), TOTAL - 0.1, lines=["Nam quốc sơn hà Nam đế cư", "Tiệt nhiên định phận tại thiên thư"], gap=1.6, fi=0.8, fo=1.0)
fx("insect", A(114), TOTAL); fx("wind", A(114), TOTAL)


# ---- phụ đề theo từng đoạn (chia trang theo dấu câu, mốc theo số chữ) ----
import re as _re
def _wrap(txt, w=46):
    out, cur = [], ""
    for wd_ in txt.split():
        if cur and len(cur) + 1 + len(wd_) > w:
            out.append(cur); cur = wd_
        else:
            cur = (cur + " " + wd_).strip()
    if cur: out.append(cur)
    return out
for _i, _b in enumerate(KB, 1):
    _t = _b["text"]; _parts = [p.strip() for p in _re.split(r"(?<=[.?!])\s+", _t) if p.strip()]
    _pages, _cur = [], ""
    for p in _parts:
        if _cur and len((_cur + " " + p)) > 100: _pages.append(_cur); _cur = p
        else: _cur = (_cur + " " + p).strip()
    if _cur: _pages.append(_cur)
    _tot = sum(len(p.split()) for p in _pages); _t0 = S[_i] + 0.05; _span = D[_i] - 0.1
    for p in _pages:
        _d = _span * len(p.split()) / _tot
        add("sub", _t0, _t0 + _d, lines=_wrap(p), fi=0.12, fo=0.12); _t0 += _d

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

