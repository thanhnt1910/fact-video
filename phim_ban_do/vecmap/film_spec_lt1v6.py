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



import math
SH = []
def shot(scene, i0, i1, lon, lat, wd=0.115, map_=False, **kw):
    SH.append(dict(scene=scene, i0=i0, i1=i1, lon=lon, lat=lat, wd=wd, map=map_, kw=kw))

KEYS = {"canhGac", "thaiUy", "xuatQuan", "ai", "uc", "phongTuyen", "nn", "camp", "trongDen", "binhMinh", "leuDem", "voi", "vinhBinh", "tl", "bien", "nha", "hauCan", "songSang"}
KEYFX = {   # âm thanh riêng + hiệu ứng riêng của từng cảnh zoom chính: (loại, từ giây tương đối, đến giây tương đối)
    "xuatQuan": [("drum", 0.0, 99), ("horn", 0.8, 0)],
    "ai": [("horn", 0.2, 0), ("clash", 2.0, 0), ("arrow", 1.0, 99), ("clash", 6.5, 0)],
    "uc": [("drum", 0.0, 99), ("fire", 3.0, 99), ("clash", 5.0, 0), ("arrow", 2.0, 99), ("clash", 9.0, 0)],
    "nn": [("water", 0.0, 99), ("arrow", 2.0, 99), ("clash", 4.0, 0), ("clash", 7.0, 0)],
    "camp": [("wind", 0.0, 99), ("insect", 0.0, 99)],
    "trongDen": [("insect", 0.0, 99), ("wind", 0.0, 99), ("gong", 0.3, 0)],
    "voi": [("hoof", 0.0, 99), ("horn", 0.5, 0)],
    "tl": [("gong", 0.3, 0)],
    "nha": [("wind", 0.0, 99)],
    "songSang": [("water", 0.0, 99), ("wind", 0.0, 99)],
    "canhGac": [("wind", 0.0, 99), ("march", 0.5, 99)],
    "thaiUy": [("gong", 0.3, 0)],
    "phongTuyen": [("march", 0.0, 99), ("wind", 0.0, 99)],
    "binhMinh": [("water", 0.0, 99), ("insect", 0.0, 99)],
    "leuDem": [("fire", 0.0, 99), ("wind", 0.0, 99)],
    "vinhBinh": [("gong", 0.4, 0), ("wind", 0.0, 99)],
    "bien": [("water", 0.0, 99), ("wind", 0.0, 99)],
    "hauCan": [("march", 0.0, 99), ("wind", 0.0, 99)],
}
NAMED = [("Thăng Long", TL), ("Ung Châu", UC), ("sông Như Nguyệt", (106.06, 21.20)), ("Lạng Sơn", LS), ("Khâm Châu", KC), ("Quế Lâm", QC), ("Quảng Tây", (109.85, 24.90))]
PLACE = {"phuong": ("Thăng Long", TL), "giaDinh": ("Thăng Long", TL), "trieuDuong": ("Thăng Long", TL), "thaiUy": ("Thăng Long", TL),
         "hopBan": ("Thăng Long", TL), "ngoaiGiao": ("Thăng Long", TL), "tuoiGia": ("Thăng Long", TL),
         "hamDoi": ("Chiêm Thành", (107.05, 17.40)), "chiemThanh": ("Chiêm Thành", (107.55, 16.40)),
         "trieuTong": ("Triều đình nhà Tống", QC), "taoLuyen": ("Quảng Tây", (109.85, 24.90)), "xuongThuyen": ("Ung Châu", UC),
         "khamChau": ("Khâm Châu", KC), "duongBien": ("Liêm Châu", LC), "mattThanh": ("Ung Châu", UC), "daoDat": ("Ung Châu", UC),
         "thanhHoang": ("Ung Châu", UC), "doDem": ("Ung Châu", UC), "dienChau": ("Diễn Châu", (105.80, 19.30)),
         "bien": ("Nghệ An", (106.50, 17.80)), "nghiNgoi": ("sông Như Nguyệt", (106.22, 21.42))}

def build_cam():
    """Bản đồ là chính, chỉ zoom vào các cảnh chính (KEYS). Cảnh khác ở lại bản đồ, máy quay trôi theo."""
    last_city = {}
    for h in SH:
        key = h["scene"] in KEYS
        h["key"] = key
        if not key:
            h["map"] = True
            lo, la = h["lon"], h["lat"]
            h["wd"] = 3.2; h["lat"] = max(h["lat"], 19.6)
    prev = None
    for k, h in enumerate(SH):
        ts0, te = A(h["i0"]), E_(h["i1"]); span = te - ts0
        zin = min(2.6, span * 0.45); zout = min(1.9, span * 0.4)
        h["zin"], h["zout"] = zin, zout
        if h["key"]:
            base = prev["wd"] if prev and not prev["key"] else 1.0
            if prev is None:
                cam.append([ts0, h["lon"], h["lat"], 1.2])
            else:
                dist = math.hypot(h["lon"] - prev["lon"], h["lat"] - prev["lat"])
                tb = (E_(prev["i1"]) + ts0) / 2
                if dist > 1.2:
                    cam.append([tb, (prev["lon"] + h["lon"]) / 2, (prev["lat"] + h["lat"]) / 2, min(dist * 1.2 + 0.6, 10)])
                cam.append([ts0 + 0.2, h["lon"], h["lat"], max(0.6, min(base, 1.2))])
            cam.append([ts0 + zin, h["lon"], h["lat"], h["wd"]])
            cam.append([te - zout, h["lon"] + 0.002, h["lat"] - 0.003, h["wd"] * 0.96])
            kw = dict(h["kw"]); sp = kw.pop("sp", None) or ((kw.pop("breach") / (0.78 * (te - ts0 - zin))) if "breach" in kw else 1.0); kw.pop("breach", None)
            add("cc", ts0 - 0.2, te + 0.6, scene=h["scene"], lon=h["lon"], lat=h["lat"], ts=ts0 + zin - 0.4, sp=round(sp, 4), fi=0.8, fo=0.6, **kw)
            add("ring", ts0 - 0.6, ts0 + 1.2, lon=h["lon"], lat=h["lat"], dur=1.8, fi=0.1, fo=0.4)
            fx("arrow", ts0, ts0 + 0.3)
            for kind, o0, o1 in KEYFX.get(h["scene"], []):
                fx(kind, ts0 + zin + o0, (te if o1 == 99 else ts0 + zin + o0 + 4)) if o1 == 99 else fx(kind, ts0 + zin + o0)
        else:
            if prev is not None and prev["key"]:
                cam.append([ts0 + 1.3, h["lon"], h["lat"], h["wd"]])
            else:
                dist = math.hypot(h["lon"] - prev["lon"], h["lat"] - prev["lat"]) if prev else 0
                if prev is not None and dist > 6:
                    cam.append([(E_(prev["i1"]) + ts0) / 2, (prev["lon"] + h["lon"]) / 2, (prev["lat"] + h["lat"]) / 2, min(dist * 1.2 + 0.6, 10)])
                cam.append([ts0 + 0.9, h["lon"], h["lat"], h["wd"]])
            cam.append([te - 0.4, h["lon"] + 0.01, h["lat"] - 0.008, h["wd"] * 0.97])
            pl = PLACE.get(h["scene"])
            if not pl:
                nm = min(NAMED, key=lambda q: math.hypot(q[1][0] - h["lon"], q[1][1] - h["lat"]))
                if math.hypot(nm[1][0] - h["lon"], nm[1][1] - h["lat"]) < 0.9: pl = nm
            if pl and last_city.get(pl[0], -9) < ts0 - 0.1:
                add("city", ts0 + 0.5, te, lon=pl[1][0], lat=pl[1][1], name=pl[0], side="e", fs=30, fi=0.6, fo=0.6)
                last_city[pl[0]] = te
            if not any(x.get("k") in ("army", "route") and x["t0"] <= te and x.get("t1", 0) >= ts0 for x in items):
                add("ring", ts0 + 0.6, ts0 + 2.6, lon=h["lon"], lat=h["lat"], dur=1.8, fi=0.1, fo=0.4)
        prev = h

NNP = (106.05, 21.19); TLP = TL
HN = (105.85, 21.03)
# ===== Chương 1: mở đầu (1–6) =====
shot("hoBien", 1, 1, 106.80, 21.88, tau0=0)
add("chip", A(1), E_(1), text="Biên giới, cuối năm 1075", w=860, fi=0.6, fo=0.4, y=130)
shot("canhGac", 2, 2, 106.30, 21.62)
shot("haiHuong", 3, 4, 106.45, 21.55, mir=1)
shot("nhinBac", 5, 6, 106.62, 21.72)
add("big", A(5, 0.2), A(5, 3.4), text="?", col="#7a1f1f", fi=0.4, fo=0.8, y=200, fs=260)
# ===== Chương 2: Người cầm cờ tiết (7–18) =====
shot("phuong", 7, 7, 105.83, 21.04); card("Phường Thái Hòa", "kinh thành Thăng Long", 7, 1.0, 3.6)
shot("giaDinh", 8, 9, 105.80, 21.07, mir=1)
shot("trieuDuong", 10, 12, 105.87, 21.03)
shot("hamDoi", 13, 13, 107.05, 17.40); chip("Năm 1069", 13, 14, 400)
shot("chiemThanh", 14, 14, 107.55, 16.40, mir=1)
shot("thaiUy", 15, 16, 105.89, 21.01); card("Thái úy", "một trong những chức quân sự cao nhất", 16, 2.0, 4.5)
shot("tongBien", 17, 18, 107.30, 22.20); chip("Năm 1075", 17, 18, 400)
# ===== Chương 3: Chờ hay đánh (19–32) =====
shot("trieuTong", 19, 20, 110.29, 25.27); chip("Triều đình nhà Tống", 19, 20, 700)
shot("vuongAnThach", 21, 21, 110.75, 25.80, mir=1)
shot("taoLuyen", 22, 23, 109.85, 24.90)
shot("xuongThuyen", 24, 24, 108.75, 23.15)
shot("hopBan", 25, 26, 105.90, 21.05, mir=1)
shot("thapCanh", 27, 27, 106.20, 21.40)
add("big", A(27, 0.3), E_(27), text="?", col="#7a1f1f", fi=0.4, fo=0.6, y=200, fs=240)
shot("xuatQuan", 28, 29, 105.95, 21.30)
shot("thanhMieu", 30, 30, 109.55, 24.25); add("big", A(30, 0.5), A(30, 3.2), text="THANH MIÊU", col="#7a1f1f", fi=0.5, fo=0.8, y=160, fs=110)
shot("leuQuan", 31, 32, 106.70, 21.80, mir=1)
# ===== Chương 4: Đánh vào đâu (33–40) =====
shot("map33", 33, 33, 107.60, 21.90, wd=3.4, map_=True)
army([HN, (106.3, 21.4), LS, (107.5, 22.4), UC], "v", 33, 0.3, 4.6, n=14, t1_i=33)
army([HN, (106.8, 20.7), (107.8, 21.1), KC], "v", 33, 0.8, 4.2, n=12, t1_i=33)
shot("duongBien", 34, 34, 108.05, 21.45)
shot("khamChau", 35, 35, 108.65, 21.96, mir=1); chip("Khâm Châu và Liêm Châu", 35, 35, 760)
shot("duongNui", 36, 37, 107.70, 22.45)
shot("ai", 38, 39, *CL); chip("Cửa ải Côn Lôn", 38, 39, 640)
shot("ucXa", 40, 40, *UC, tau0=0)
add("big", A(40, 0.3), A(40, 3.0), text="?", col="#7a1f1f", fi=0.4, fo=0.8, y=200, fs=240)
# ===== Chương 5: Bốn mươi ngày (41–53) =====
shot("mattThanh", 41, 41, UC[0] + 0.004, UC[1] + 0.003); chip("Ung Châu, đầu năm 1076", 41, 42, 860)
shot("daoDat", 42, 43, UC[0] - 0.006, UC[1] - 0.004, mir=1)
shot("uc", 44, 46, *UC, breach=14.2)
shot("doDem", 47, 47, UC[0] + 0.01, UC[1] - 0.006); add("big", A(47, 0.3), A(47, 4.0), text="40 NGÀY", col="#7a1f1f", fi=0.5, fo=0.8, y=140, fs=120)
shot("thanhHoang", 48, 49, UC[0] - 0.003, UC[1] + 0.002, mir=1)
shot("rutQuan", 50, 51, 107.30, 22.30)
shot("tramGac", 52, 53, 106.76, 21.85)
# ===== Chương 6: Giữ sông bằng gì (54–68) =====
shot("tongKetTap", 54, 54, 109.00, 24.00); chip("Năm 1076", 54, 56, 400)
shot("quachQuy", 55, 55, 108.50, 23.50, mir=1)
shot("nhinSong", 56, 56, 106.10, 21.30)
shot("mapNN", 57, 60, 106.06, 21.20, wd=0.45, map_=True)
add("route", A(57, 0.5), E_(60), id="nnline", pts=[[105.93, 21.15], [106.05, 21.19], [106.18, 21.22]], col=V, dur=4, w=7, fi=0.2, fo=0.8)
army([(106.12, 21.7), (106.1, 21.42), (106.08, 21.22)], "s", 57, 0.6, 7.0, n=14, t1_i=60)
lab("sông Như Nguyệt", (106.06, 21.17), "#3a64a8", 57, 60, fs=40, op=0.8)
chip("Sông Như Nguyệt", 57, 60, 620)
shot("phongTuyen", 61, 61, 106.04, 21.18, mir=1)
shot("gacDem", 62, 62, 106.07, 21.20)
shot("nn", 63, 64, *NNP, sp=0.45, tau0=4)
shot("quanDuBi", 65, 66, 106.12, 21.23, mir=1)
shot("camp", 67, 68, 106.00, 21.30, tau0=20); add("sick", A(67, 0.5), E_(68) + 2.0, fi=1.2, fo=1.5)
# ===== Chương 7: Bài thơ bên sông (69–77) =====
shot("denDem", 69, 70, 106.00, 21.22)
shot("trongDen", 71, 73, 106.03, 21.20)
add("night", A(69, 0.5), E_(73) + 0.5, a=0.55, moon=True, fi=1.5, fo=1.5)
add("poem", A(71, 0.2), E_(71), lines=["Nam quốc sơn hà Nam đế cư", "Tiệt nhiên định phận tại thiên thư", "Như hà nghịch lỗ lai xâm phạm", "Nhữ đẳng hành khan thủ bại hư"], gap=1.4, fi=0.8, fo=0.8)
card("Đền hai anh em họ Trương", "theo truyền thuyết", 72, 0.8, 4.5, col="#8a8a8a")
shot("binhMinh", 74, 77, 106.08, 21.21, mir=1)
fx("insect", A(69), E_(73)); fx("wind", A(69), E_(77))
# ===== Chương 8: Khi nào thì dừng (78–86) =====
shot("nghiNgoi", 78, 78, 106.22, 21.42)
shot("luongTong", 79, 80, 106.15, 21.60, mir=1)
shot("leuDem", 81, 83, 106.30, 21.45)
shot("thuongLuong", 84, 85, 106.45, 21.70, mir=1)
shot("tongRut", 86, 86, 106.80, 22.40)
# ===== Chương 9: Đòi lại đất (87–97) =====
shot("ngoaiGiao", 87, 88, 105.92, 21.05)
shot("voi", 89, 89, 107.00, 23.40, mir=1); card("Đào Tống Nguyên", "mang năm con voi sang thương lượng", 89, 0.3, 3.6); chip("Năm 1078", 87, 89, 400)
shot("traDat", 90, 90, 106.26, 22.67); chip("Năm 1079", 90, 90, 400)
shot("traTu", 91, 92, 106.55, 22.40, mir=1); chip("Năm 1081", 91, 92, 400)
shot("vinhBinh", 93, 94, 107.40, 22.25); chip("Năm 1084", 93, 94, 400); card("Một số huyện và động", "số cụ thể còn cần đối chiếu", 94, 0.2, 3.0)
shot("mapBien", 95, 97, 106.8, 22.4, wd=2.2, map_=True)
add("route", A(95, 0.4), E_(97), id="bien", pts=[[106.0, 22.4], [106.6, 22.7], [107.3, 22.5], [108.0, 22.6]], col=V, dur=5, w=7, fi=0.2, fo=0.8)
lab("vùng đất được trao trả", (106.8, 22.75), V, 95, 97, fs=40, op=0.8)
# ===== Chương 10: Những năm cuối (98–105) =====
shot("tl", 98, 99, *HN, tau0=260, badge=1, mir=1); card("Thái úy", "giữ trọng trách trong triều", 98, 3.0, 4.0)
shot("dienChau", 100, 100, 105.80, 19.30); chip("Năm 1103", 100, 100, 400)
shot("bien", 101, 102, 106.50, 17.80, tau0=0, mir=1); chip("Năm 1104", 101, 102, 400)
shot("tuoiGia", 103, 103, 105.88, 21.02)
shot("nha", 104, 105, 105.83, 21.00); chip("Năm 1105", 104, 105, 400); fx("gong", A(104, 0.4))
# ===== Chương 11: Trở lại bên sông (106–115) =====
shot("mapKet", 106, 109, 107.2, 22.0, wd=2.6, map_=True)
add("city", A(106), E_(109), lon=UC[0], lat=UC[1], name="Ung Châu, 1075", side="e", fs=30, fi=0.6, fo=0.6)
add("city", A(106), E_(109), lon=NNP[0], lat=NNP[1], name="Như Nguyệt, 1076", side="e", fs=30, fi=0.6, fo=0.6)
army([NNP, (106.4, 21.8), (107.4, 22.4), UC], "v", 106, 0.5, 5.0, n=12, t1_i=109)
card("Hai nước cờ", "của cùng một người", 109, 0.5, 5.0)
shot("nga3", 110, 111, 106.40, 21.60)
shot("hauCan", 112, 113, 106.00, 21.30, mir=1)
shot("songSang", 114, 115, 106.05, 21.20)
add("poem", A(114, 0.4), TOTAL - 0.1, lines=["Nam quốc sơn hà Nam đế cư", "Tiệt nhiên định phận tại thiên thư"], gap=1.6, fi=0.8, fo=1.0)
build_cam()

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
    for p in parts:   # câu dài: tách tiếp theo dấu phẩy rồi theo độ dài
        cl = [c.strip() for c in _re.split(r"(?<=,)\s+", p) if c.strip()] if len(p) > mx else [p]
        pages.extend(cl)
    out, cur = [], ""
    for p in pages:
        if cur and len(cur + " " + p) > mx: out.append(cur); cur = p
        else: cur = (cur + " " + p).strip()
    if cur: out.append(cur)
    res = []
    for p in out:   # trang vẫn dài hơn 2 dòng: cắt theo từ
        if len(_wrap(p)) > 2:
            ws = p.split(); h = len(ws) // 2; res += [" ".join(ws[:h]), " ".join(ws[h:])]
        else: res.append(p)
    return res
for _i, _b in enumerate(KB, 1):
    _pages_ = _pages(_b["text"])
    _tot = sum(len(p.split()) for p in _pages_); _t0 = S[_i] + 0.05; _span = D[_i] - 0.1
    for p in _pages_:
        _d = _span * len(p.split()) / _tot
        add("sub", _t0, _t0 + _d, lines=_wrap(p), fi=0.1, fo=0.1); _t0 += _d

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

