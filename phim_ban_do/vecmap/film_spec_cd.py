"""Bảng cảnh video Chu Du (cd) bằng bản đồ vector: thời điểm từng đoạn theo giọng đọc thật -> spec_cd.js (hình) + sfx_cd.json (âm thanh).
Chạy: python phim_ban_do/vecmap/film_spec_cd.py ; vẽ khung: FILM=film_cd.html GEO_JS=geo_cd.js SPEC_JS=spec_cd.js SFX_JSON=sfx_cd.json python phim_ban_do/vecmap/ve_film.py still <giây>..."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KB = json.load(open(ROOT / "ke-hoach/thu-giong-hai/cd_full.json", encoding="utf-8"))
DUR = json.load(open(ROOT / "assets/thu_giong_hai/cd_chuan/thoi_luong.json"))
LEAD, GAP, TAIL = 0.5, 0.45, 1.5   # khớp quy ước kiem_video.py
S, D = {}, {}
PS = []
t = LEAD
for i, b in enumerate(KB, 1):
    d = DUR[str(b["n"])]
    PS.append((t, d, b["text"]))
    S[i] = t; D[i] = d
    t += d + GAP
TOTAL = t + TAIL
A = lambda i, off=0.0: S[i] + off
E_ = lambda i: S[i] + D[i]

NG, TA, LB = "#c9742a", "#3a64a8", "#4a8a45"       # Ngô (cam), Tào (xanh dương), Lưu Bị (xanh lá)
RD, BRN = "#7a1f1f", "#6b5a45"
cam, items, sfx = [], [], []

# ---------- địa danh (kinh độ, vĩ độ; vị trí ước lượng cho minh họa) ----------
LG = (117.0, 31.1)      # Lư Giang
KK = (119.45, 32.2)     # Kinh Khẩu (nơi Tôn Quyền đóng khi Chu Du dâng thư)
SCG = (116.0, 29.72)    # Sài Tang
HK = (114.3, 30.55)     # Hạ Khẩu
XB = (113.72, 29.75)    # Xích Bích (bờ nam)
OL = (113.92, 29.99)    # Ô Lâm (bờ bắc, quân Tào)
NQ = (112.2, 30.35)     # Nam Quận / Giang Lăng
TD = (112.15, 32.03)    # Tương Dương
BK = (113.1, 29.37)     # Ba Khâu
TDO = (104.07, 30.67)   # Thành Đô (đất Thục)
HT = (107.03, 33.07)    # Hán Trung (Trương Lỗ)
QT = (108.9, 34.25)     # Quan Trung (Mã Siêu)
CA = (112.2, 30.05)     # Công An (Lưu Bị)

TG = [(106.55, 29.56), (107.6, 30.0), (108.4, 30.8), (109.5, 31.05), (110.4, 30.8), (111.3, 30.7), (112.2, 30.35), (112.55, 30.1), (112.9, 29.82),
      (113.15, 29.62), (113.45, 29.72), (113.75, 29.82), (114.0, 29.95), (114.15, 30.3), (114.3, 30.55), (114.9, 30.4), (115.4, 30.1), (116.0, 29.72),
      (116.6, 29.9), (117.05, 30.5), (117.7, 30.9), (118.4, 31.35), (118.8, 32.05), (119.45, 32.22), (120.2, 31.95), (121.0, 31.75), (121.4, 31.6)]
HAN = [(107.03, 33.07), (108.5, 32.9), (110.0, 32.6), (111.2, 32.3), (112.15, 32.03), (112.5, 31.5), (113.0, 31.0), (113.5, 30.6), (113.9, 30.5), (114.3, 30.58)]
XIANG = [(112.9, 27.2), (112.95, 28.3), (112.85, 28.9)]
RIVERS = [{"id": "truonggiang", "w": 4.4, "pts": TG, "amb": 3}, {"id": "han", "w": 3.0, "pts": HAN, "amb": 1}, {"id": "tuong", "w": 2.4, "pts": XIANG, "amb": 0}]
LAKES = [{"name": "dongdinh", "pts": [(112.3, 29.1), (112.65, 29.4), (112.95, 29.33), (113.0, 29.1), (112.9, 28.85), (112.55, 28.8), (112.3, 28.9)]},
         {"name": "badương", "pts": [(115.95, 29.6), (116.35, 29.75), (116.7, 29.4), (116.55, 28.95), (116.2, 28.8), (116.0, 29.1)]},
         {"name": "thaihu", "pts": [(119.8, 31.1), (120.2, 31.5), (120.55, 31.25), (120.3, 30.95)]}]


def sl(a, b, riv=TG):
    """đoạn sông từ gần a đến gần b (đi xuôi hay ngược theo thứ tự a -> b)."""
    ia = min(range(len(riv)), key=lambda k: (riv[k][0] - a[0]) ** 2 + (riv[k][1] - a[1]) ** 2)
    ib = min(range(len(riv)), key=lambda k: (riv[k][0] - b[0]) ** 2 + (riv[k][1] - b[1]) ** 2)
    pts = riv[ia:ib + 1] if ia <= ib else list(reversed(riv[ib:ia + 1]))
    return [a] + pts + [b] if ia != ib else [a, b]


KEEP = set()


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


def card(title, sub, i, off=0.4, dur=3.4, col=NG, **kw):
    kw.setdefault("w", int(max(len(title) * 31 + 60, len(sub or "") * 17 + 70, 420)))
    add("card", A(i, off), min(A(i, off + dur), E_(i) - 0.1), title=title, sub=sub, col=col, fi=0.5, fo=0.5, **kw)


GUESS = [("lửa|cháy|khói|hỏa", "fire"), ("tên |mũi tên|bắn", "arrow"), ("gió", "wind"), ("thuyền|sông", "ship"), ("quân|binh|vạn", "people"), ("thư", "letter"),
         ("tuổi|sinh|năm ", "calendar"), ("bệnh|mất", "cross"), ("tiểu thuyết|truyện|tầng|chính văn|chú giải|sử |Tam quốc", "book"), ("nhà", "house"), ("nhạc", "music"),
         ("\\?", "question"), ("Tôn Quyền|vua|chí lớn", "crown"), ("khóc|tang", "drop"), ("tính|cân", "scale")]
RICH = {}   # đoạn bắt đầu -> (đoạn cuối, biểu tượng, tiêu đề, các dòng, độ trễ giây)


def _in_rich(i):
    return any(a <= i <= v[0] for a, v in RICH.items())


def guess_icon(text):
    for pat, ic in GUESS:
        if re.search(pat, text):
            return ic
    return "scroll"


def chip(text, i0, i1=None, off=0.0, dur=None, ic=None, lines=None):
    """khung mô tả (banner) ở dưới màn hình: biểu tượng động + tiêu đề (+ dòng phụ)."""
    if _in_rich(i0) and ic is None:
        return
    i1 = i1 or i0
    t0 = A(i0, off)
    t1 = E_(i1) if dur is None else min(E_(i1), t0 + dur)
    add("banner", t0, t1, title=text, lines=lines or [], ic=ic or guess_icon(text), col=NG, fi=0.5, fo=0.5)


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


def big(text, i, off=0.3, dur=2.6, y=560, fs=190, col=RD):
    add("big", A(i, off), min(E_(i) - 0.1, A(i, off + dur)), text=text, col=col, fi=0.4, fo=0.7, y=y, fs=fs)


def ring(p, i, off=0.4, col=NG, dur=1.8, t1_i=None):
    add("ring", A(i, off), E_(t1_i or i), lon=p[0], lat=p[1], col=col, dur=dur)


def fire(p, t0, t1, s=18):
    add("fire", t0, t1, lon=p[0], lat=p[1], s=s, fi=0.6, fo=0.8)


def melee(p, i, off, t1_i=None, n=3, hits=True):
    t0, t1 = A(i, off), E_(t1_i or i)
    add("clash", t0, t1, lon=p[0], lat=p[1], n=n, c1=NG, c2=TA, fi=0.3, fo=0.5)
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


def defeat(p, side, i, off=0.5, t1_i=None, n=6):
    add("defeat", A(i, off), E_(t1_i or i) + 0.5, lon=p[0], lat=p[1], side=side, n=n, fi=0.2, fo=0.8)
    fx("gong", A(i, off) + 0.3)



RICH.update({
    4: (4, "book", "Trong Tam quốc diễn nghĩa", ["Chu Du tài giỏi nhưng hẹp hòi", "Không chịu nổi việc Gia Cát Lượng giỏi hơn mình"], 0.2),
    5: (5, "sword", "Ba lần bày mưu hại", ["Lần nào cũng bị Gia Cát Lượng nhìn thấu", "và đi trước một bước"], 0.2),
    7: (8, "scroll", "Một câu chuyện quá gọn", ["Người thông minh, kẻ ghen tị, kẻ thua, người thắng", "Nhưng có thật như thế không?"], 0.2),
    12: (12, "calendar", "Chu Du sinh khoảng năm 175", ["Ở vùng Lư Giang", "Năm sinh suy ra từ tuổi lúc ông mất"], 0.2),
    13: (14, "people", "Bạn thân của Tôn Sách", ["Cùng tuổi nhau", "Chỉ riêng Chu Du được Tôn Sách xem là bạn như thế"], 3.2),
    15: (16, "house", "Nhường nhà cho bạn", ["Một ngôi nhà lớn ở phía nam con đường", "Người như vậy khó mà hẹp hòi"], 0.2),
    17: (17, "music", "Đôi tai tinh tế", ["Ai đánh sai một nốt, dù đang uống rượu,", "ông cũng nhận ra ngay"], 0.2),
    18: (18, "eye", "Nhạy bén như người đọc thế trận", ["Hợp với một vị tướng"], 0.2),
    19: (19, "sword", "Mùa đông năm 208", ["Tào Tháo kéo quân xuống phía nam", "Nước Ngô đứng trước lựa chọn lớn"], 3.4),
    23: (23, "people", "Xin 5 vạn quân tinh nhuệ", ["Tôn Quyền đáp: đã chọn 3 vạn người, sẽ tiếp tế thêm"], 3.6),
    24: (24, "ship", "Chính văn ghi gọn hơn", ["Chu Du xin 3 vạn quân, tiến lên đóng ở Hạ Khẩu"], 0.2),
    28: (28, "fire", "Hỏa công", ["Mấy chục chiến thuyền nhỏ và nhanh", "Chất đầy củi, cỏ khô, rót dầu"], 0.2),
    29: (29, "wind", "Gió đông nam nổi lên rất gấp", ["Chi tiết trong chú giải (Giang biểu truyện)"], 0.2),
    31: (31, "fire", "Khói lửa ngút trời", ["Người và ngựa chết cháy, chết đuối rất đông", "Quân Tào thua, rút về giữ Nam Quận"], 0.2),
    33: (33, "question", "Phần vinh quang đi đâu?", ["Gia Cát Lượng không có mặt trong những câu này", "Tiểu thuyết đã chuyển nó đi đâu, ta sẽ hỏi sau"], 0.2),
    35: (36, "arrow", "Mũi tên lạc trúng sườn phải", ["Vết thương rất nặng, phải rút về nghỉ", "Tào Nhân định kéo quân đến đánh"], 3.4),
    38: (39, "shield", "Gượng dậy đi khắp doanh trại", ["Tào Nhân thấy ông còn đứng được, không dám tiến", "Ngoan cường, không phải yếu đuối vì tức giận"], 0.2),
    40: (40, "scroll", "Nghĩ về bạn hôm nay, đối thủ ngày mai", [], 0.2),
    43: (43, "crown", "Tôn Quyền không nghe", ["Còn cần các anh hùng khác để đối phó Tào Tháo"], 0.2),
    44: (45, "scale", "Chu Du không ghét Gia Cát Lượng", ["Ông lo về cả nhóm người của Lưu Bị", "Coi đó là việc của quốc gia"], 0.2),
    46: (47, "book", "Không có chuyện hai người đấu trí", ["Điều đó không chứng minh hai người chưa từng gặp", "Nhưng bộ sử không dựng chuyện Chu Du bị chọc tức"], 0.2),
    48: (48, "calendar", "Năm 210: kế hoạch lớn", ["Xin Tôn Quyền cho đi lấy đất Thục"], 0.2),
    50: (51, "crown", "Chí lớn của Chu Du", ["Làm cho nước Ngô lớn lên", "Tôn Quyền đồng ý, Chu Du về Giang Lăng chuẩn bị quân"], 0.2),
    53: (53, "cross", "Mất vì bệnh", ["Ở Ba Khâu, lúc 36 tuổi", "Sử không ghi lý do nào là vì tức giận"], 0.2),
    54: (54, "book", "Bùi Tùng Chi ghi chú", ["Nơi mất phải là Ba Lăng ngày nay", "khác với tên Ba Khâu trong chính văn"], 0.2),
    56: (56, "scroll", "Tiến cử Lỗ Túc", ["Trí và mưu của Lỗ Túc đủ để thay ông"], 0.2),
    57: (57, "heart", "Nằm bệnh vẫn lo giữ nước", ["Không phải người chết vì một lần bị chọc tức"], 0.2),
    59: (60, "drop", "Tôn Quyền khóc bạn", ["Nói Chu Du có tài giúp vua, mất sớm", "Không nói ông hẹp hòi"], 0.2),
    62: (62, "book", "Lời bình của Trần Thọ", ["Chu Du và Lỗ Túc: hiểu biết, quyết đoán vượt người thường", "Là những kỳ tài"], 0.2),
    63: (63, "book", "Người sống gần thời Chu Du nhất", ["Không vẽ ông thành kẻ ghen tị", "Họ vẽ một người quyết đoán và đáng tiếc"], 0.2),
    64: (64, "question", "Vì sao tiểu thuyết cho ông hộc máu?", [], 0.2),
    65: (65, "book", "Kể từ phía nước Thục", ["Trong Tam quốc diễn nghĩa, Gia Cát Lượng", "là người khôn ngoan nhất"], 0.2),
    66: (67, "scale", "Cần một người đứng đối diện", ["Chu Du giỏi, nổi tiếng, thắng một trận lớn", "Thắng được người như thế, Gia Cát Lượng càng giỏi"], 0.2),
    68: (68, "scale", "Lấy bớt công trạng", ["Chuyển sang nhân vật mình yêu", "Rồi thêm tính hẹp hòi để có lý do thua"], 0.2),
    69: (70, "question", "Người kể chuyện chọn phe", ["Chọn luôn ai là người tốt, ai bị hạ xuống", "Chu Du thành người nhỏ nhen để truyện đẹp hơn"], 0.2),
    71: (71, "sword", "Như một kịch bản sân khấu", ["Ba lần bị chọc, ba lần thua, lần thứ ba hộc máu"], 3.0),
    73: (73, "scroll", "Sử chỉ có:", ["Một mũi tên, một con sông,", "một trận lửa và một căn bệnh"], 0.2),
    74: (75, "layers", "Tầng 1: chính văn", ["Chỉ huy Xích Bích, bị tên bắn trúng sườn", "Gượng dậy làm Tào Nhân lui, mất vì bệnh lúc 36 tuổi"], 0.2),
    76: (77, "book", "Tầng 2: chú giải", ["Tiến cử Lỗ Túc, Tôn Quyền khóc", "Có số quân Tào và chi tiết về gió, độ chắc thấp hơn"], 0.2),
    78: (79, "book", "Tầng 3: tiểu thuyết", ["Chu Du hẹp hòi, ba lần bị qua mặt rồi tức chết", "Không có trong những đoạn chính văn đã đọc"], 0.2),
    80: (81, "question", "Một điều cần nói thật", ["Mới đọc kỹ truyện Chu Du và truyện Lỗ Túc", "Chưa đọc truyện Gia Cát Lượng, nên không kết luận hai người chưa gặp nhau"], 0.2),
    82: (83, "check", "Điều chắc chắn", ["Chính văn về Chu Du: không có chuyện bị chọc tức đến chết", "Sử ghi mất vì bệnh; không có bằng chứng cho chuyện tức chết"], 3.4),
    85: (86, "heart", "Chu Du trong sử", ["Mất khi mới 36 tuổi", "Tiếc nhất: chưa kịp làm nốt kế hoạch lớn"], 0.2),
    87: (88, "question", "Bạn nghĩ đến ai?", ["Người thắng trận Xích Bích, hay kẻ tức chết vì bị qua mặt?", "Bạn biết họ từ sử hay từ truyện?"], 0.2),
})

# ============ 1. Mở đầu (1–11) ============
C(1, 113.7, 29.85, 3.0); C(2, 113.7, 29.85, 3.6); C(3, 114.3, 30.3, 5.0); C(4, 114.3, 30.0, 6.5); C(6, 113.8, 29.9, 4.0); C(9, 113.5, 30.3, 9.0); C(11, 113.5, 30.6, 11.0)
city("Xích Bích", XB, "v", 1, 3, 30); city("Ô Lâm", OL, "s", 1, 1, 24)
army([(113.9, 29.9), (114.0, 30.0), (114.1, 30.1)], "s", 1, 0.2, 4.0, n=8, t1_i=1, flag=True, u="ship")
fire((113.88, 29.92), A(1, 2.0), E_(2), 20); fx("fire", A(1, 2.0), E_(2)); fx("drum", A(1, 0.4), A(2, 0))
card("Chu Du", "đại tướng nước Ngô", 1, 0.4, 3.2)
big("36 TUỔI", 2, 1.6, 3.0, 300, 170); fx("gong", A(2, 1.6))
card("Chu Du", "đại tướng nước Ngô", 3, 0.3, 3.0); card("Gia Cát Lượng", "quân sư của Lưu Bị", 3, 3.5, 3.0, col=LB)
chip("Tam quốc diễn nghĩa: tài giỏi nhưng hẹp hòi", 4, 4, 0.2, 7.5)
chip("Mưu hại Gia Cát Lượng, nhưng bị nhìn thấu", 5, 5, 0.2)
big("3 LẦN", 6, 0.3, 1.8, 460, 200); big("HỘC MÁU", 6, 2.1, 1.8, 700, 150)
chip("Câu chuyện nghe một lần là nhớ", 7, 8, 0.2)
big("?", 9, 0.3, 2.6, 600, 280); chip("Chu Du có thật sự chết như thế?", 9, 9, 0.3, 4.4)


# ============ 2. Người bạn thuở nhỏ (12–18) ============
C(12, 117.0, 31.1, 2.6); C(13, 117.4, 31.2, 3.0); C(16, 117.2, 31.1, 2.2); C(18, 117.4, 31.0, 3.4)
city("Lư Giang", LG, "v", 12, 18, 30); chip("Chu Du sinh khoảng năm 175", 12, 12, 0.2)
card("Chu Du", "cùng tuổi với Tôn Sách", 13, 0.3, 2.6); card("Tôn Sách", "người đặt nền cho nước Ngô", 13, 3.0, 2.3)
chip("Chỉ Chu Du được xem là bạn thân", 14, 14, 0.2); mark("dot", (116.93, 31.06), 15, 0.3, 16, s=24, col=NG)
chip("Nhường ngôi nhà lớn cho Tôn Sách", 15, 16, 0.2)
chip("Giỏi âm nhạc: nghe ra từng nốt sai", 17, 17, 0.2); chip("Tinh tế, nhạy bén, hợp với tướng đọc thế trận", 18, 18, 0.2)

# ============ 3. Mùa đông năm 208 (19–26) ============
C(19, 113.5, 31.0, 8.0); C(21, 113.4, 31.0, 7.0); C(22, 112.7, 31.0, 4.4); C(23, 115.0, 30.4, 6.5); C(24, 115.0, 30.3, 5.0); C(26, 114.3, 30.55, 3.4)
chip("Mùa đông năm 208", 19, 19, 0.2)
army([(112.1, 33.5), TD, (112.3, 31.0), NQ], "s", 19, 0.4, 5.0, n=18, t1_i=20, flag=True, u="inf")
city("Tương Dương", TD, "s", 19, 22, 26); city("Nam Quận", NQ, "s", 20, 23, 24); city("Sài Tang", SCG, "v", 19, 26, 26)
card("Tào Tháo", "kéo quân xuống phía nam", 19, 0.3, 3.2, col=TA)
big("80 VẠN", 20, 1.0, 3.4, 330, 170); chip("Lời tuyên bố của Tào Tháo (Giang biểu truyện)", 20, 20, 0.2, 4.0)
chip("Chu Du tính: chỉ 15 đến 16 vạn, và đã mệt mỏi", 21, 21, 0.2)
add("area", A(22), E_(22), pts=[[111.6, 31.5], [112.8, 31.5], [112.8, 32.5], [111.6, 32.5]], col=TA, op=0.28, fi=0.6, fo=0.6)
chip("Thêm 7 đến 8 vạn hàng binh của Lưu Biểu, lòng chưa chắc theo Tào", 22, 22, 0.2)
card("Tôn Quyền", "chúa nước Ngô", 23, 0.3, 3.0); chip("Xin 5 vạn quân, được 3 vạn", 23, 23, 3.4)
army(sl(SCG, HK), "v", 24, 0.5, 5.0, n=14, t1_i=24, flag=True, u="ship"); city("Hạ Khẩu", HK, "v", 24, 26, 26)
chip("Chu Du xin 3 vạn quân, đóng ở Hạ Khẩu", 24, 24, 0.2)
big("80 VẠN", 25, 0.3, 2.0, 420, 150, col=TA); big("3 VẠN", 25, 2.8, 2.4, 420, 150, col=NG)
card("Chu Du", "dám đặt cược vì thấy rõ con số thật", 26, 0.3, 3.2, w=900)

# ============ 4. Trận lửa trên sông (27–33) ============
C(27, 113.8, 29.85, 2.6); C(28, 113.8, 29.82, 2.2); C(30, 113.85, 29.9, 1.8); C(31, 113.7, 29.95, 3.0); C(32, 113.5, 30.2, 4.0); C(33, 113.8, 29.85, 6.5)
city("Xích Bích", XB, "v", 27, 33, 30); city("Ô Lâm", OL, "s", 27, 31, 24)
army(sl((113.55, 29.7), XB), "v", 27, 0.3, 3.0, n=10, t1_i=27, flag=True, u="ship")
army([(114.15, 30.2), (114.05, 30.08), (113.98, 29.98)], "s", 27, 0.6, 3.0, n=14, t1_i=27, flag=True, u="ship")
card("Hoàng Cái", "tướng nước Ngô, nghĩ ra cách đánh bằng lửa", 27, 1.0, 5.0, w=1150)
army(sl((113.45, 29.72), (113.75, 29.82)), "v", 28, 0.3, 3.0, n=10, t1_i=28, flag=True, u="ship")
chip("Mấy chục chiến thuyền nhỏ, chất củi, cỏ khô, rót dầu", 28, 28, 0.2)
for k in range(4):
    mark("arrow", (113.55 + k * 0.1, 29.9 - k * 0.02), 29, 0.6 + 0.2 * k, 29, s=20, col="#5a7a9a", ang=-35)
chip("Gió đông nam nổi lên rất gấp", 29, 29, 0.2)
army(sl((113.65, 29.78), (113.86, 29.93)), "v", 30, 0.2, 4.0, n=10, t1_i=30, flag=True, u="ship", col="#d9501c")
for dx, dy in [(0, 0), (0.06, -0.03), (-0.05, 0.04), (0.1, 0.0), (-0.1, 0.02)]:
    fire((OL[0] + dx, OL[1] + dy), A(30, 3.2), E_(31) + 1.0, 20)
fx("fire", A(30, 3.0), E_(31)); fx("arrow", A(30, 0.5), A(30, 3.0)); fx("drum", A(30, 0.4), E_(30))
chip("Khói lửa ngút trời, người và ngựa chết cháy, chết đuối", 31, 31, 0.2, 5.0)
defeat((113.9, 29.95), "s", 31, 1.8, 31, 6)
route("tao_rut", [OL, (113.7, 30.2), (112.9, 30.3), NQ], TA, 31, 3.2, 3.6, t1_i=31, w=6, arrow=True, chev=True)
card("Chu Du", "người xin quân, điều binh, quyết định", 32, 0.3, 4.6, w=1000); ring(XB, 32, 0.6, NG, 1.8)
chip("Gia Cát Lượng không có mặt trong những câu này", 33, 33, 0.2); mark("q", (114.1, 30.4), 33, 1.0, 33, s=40)

# ============ 5. Mũi tên và người gượng dậy (34–39) ============
C(34, 112.4, 30.4, 3.0); C(35, 112.4, 30.3, 1.8); C(36, 112.5, 30.4, 2.4); C(38, 112.4, 30.5, 3.0); C(39, 112.4, 30.4, 1.8)
city("Nam Quận", NQ, "s", 34, 39, 28)
card("Chu Du và Trình Phổ", "tiến đánh Nam Quận", 34, 0.3, 3.2, w=900)
army(sl((113.1, 29.62), (112.45, 30.15)), "v", 34, 0.5, 3.4, n=12, t1_i=34, flag=True, u="ship")
card("Tào Nhân", "giữ Nam Quận", 35, 0.2, 2.6, col=TA); chip("Hai bên chỉ cách một con sông lớn", 35, 35, 3.0)
arrows((112.1, 30.5), (112.5, 30.15), 35, 3.6, 35, 8); mark("x", (112.55, 30.15), 35, 5.6, 35, s=22)
chip("Tên lạc trúng sườn phải, vết thương rất nặng", 36, 36, 0.2)
chip("Tào Nhân định kéo quân đến đánh", 36, 36, 4.2)
card("Chu Du", "gượng dậy, đi xem khắp doanh trại", 37, 0.3, 4.4, w=1000)
army([(112.4, 30.2), (112.45, 30.3), (112.5, 30.4)], "v", 37, 0.6, 4.0, n=1, t1_i=37, flag=False, u="inf")
route("nhan_lui", [NQ, (112.0, 31.0), TD], TA, 38, 0.4, 4.0, t1_i=38, w=6, arrow=True, chev=True)
army([NQ, (112.0, 31.0), TD], "s", 38, 0.6, 4.0, n=8, t1_i=38, flag=True, u="inf", stay=False)
chip("Tào Nhân không dám tiến, rút quân", 38, 38, 0.2)
chip("Ngoan cường, không phải yếu đuối vì tức giận", 39, 39, 0.2)

# ============ 6. Người nhìn xa (40–47) ============
C(40, 119.0, 31.6, 5.0); C(41, 117.0, 31.2, 8.0); C(43, 117.0, 31.2, 8.0); C(45, 114.0, 30.6, 7.0); C(47, 113.8, 30.4, 8.0)
city("Kinh Khẩu", KK, "v", 40, 43, 26); city("Công An", CA, "s", 41, 44, 24)
chip("Nghĩ về bạn hôm nay, đối thủ ngày mai", 40, 40, 0.2)
card("Tôn Quyền", "nhận thư của Chu Du", 41, 0.3, 3.0)
route("thu", [NQ, (114.5, 31.2), (117.0, 32.0), KK], NG, 41, 0.3, 4.0, t1_i=41, w=4, arrow=True)
chip("Đưa Lưu Bị về Ngô, xây cung điện, cấp mỹ nữ và châu báu", 41, 41, 3.2)
card("Lưu Bị", "bị giữ chân ở Ngô", 42, 0.3, 2.8, col=LB); card("Quan Vũ, Trương Phi", "tách khỏi chủ", 42, 3.0, 2.4, col=LB)
chip("Tôn Quyền không nghe", 43, 43, 0.2); chip("Còn cần các anh hùng khác chống Tào Tháo", 43, 43, 2.4)
chip("Chu Du lo cho cả nhóm Lưu Bị, không ghét riêng Gia Cát Lượng", 44, 44, 0.2)
chip("Lưu Bị chỉ được nhắc khi Gia Cát Lượng sang gặp Tôn Quyền", 45, 45, 0.2)
route("luong_su", [CA, (113.5, 30.6), (115.0, 30.4), SCG], LB, 45, 2.0, 4.0, t1_i=45, w=4, arrow=True)
chip("Không có dòng nào kể hai người đấu trí", 46, 46, 0.2)
chip("Điều đó không chứng minh hai người chưa từng gặp", 46, 46, 3.6)
chip("Nhưng bộ sử không dựng chuyện Chu Du bị chọc tức", 47, 47, 0.2)

# ============ 7. Kế hoạch cuối cùng (48–57) ============
C(48, 112.5, 30.8, 8.0); C(49, 107.0, 31.8, 9.5); C(50, 107.0, 32.0, 9.5); C(51, 116.0, 31.0, 8.0); C(52, 113.1, 29.6, 2.8); C(54, 113.1, 29.6, 2.8); C(55, 116.0, 30.6, 8.0); C(57, 114.0, 30.4, 9.0)
chip("Năm 210: xin đi lấy đất Thục", 48, 48, 0.2)
route("thuc", sl(NQ, TDO)[:-1] + [(106.55, 29.56), (105.4, 30.2), TDO], NG, 48, 1.0, 4.0, t1_i=49, w=6, arrow=True, chev=True)
army(sl(NQ, (106.55, 29.56)), "v", 48, 1.2, 5.0, n=12, t1_i=49, flag=True, u="ship", stay=False)
city("Thành Đô", TDO, "s", 48, 50, 26); city("Hán Trung", HT, "s", 49, 50, 26); city("Quan Trung", QT, "s", 49, 50, 24)
card("Tôn Du", "cùng Chu Du lấy Thục", 49, 0.3, 3.0)
route("ltrung", [TDO, (105.5, 32.0), HT], NG, 49, 3.4, 4.0, t1_i=49, w=5, arrow=True)
card("Mã Siêu", "kết giao ở phía bắc", 49, 4.5, 3.0, col=TA)
chip("Đánh Trương Lỗ, để Tôn Du giữ đất", 49, 49, 0.2, 3.4)
chip("Chí lớn: làm cho nước Ngô lớn lên", 50, 50, 0.2)
chip("Tôn Quyền đồng ý, Chu Du về chuẩn bị", 51, 51, 0.2); city("Giang Lăng", NQ, "v", 51, 51, 26)
army(sl(KK, NQ), "v", 51, 0.4, 4.0, n=1, t1_i=51, flag=False, u="ship")
city("Ba Khâu", BK, "v", 52, 56, 28); mark("x", BK, 52, 2.4, 53, s=26); ring(BK, 52, 2.6, RD, 2.0, 53)
big("36 TUỔI", 52, 0.4, 3.0, 300, 150); chip("Mất vì bệnh, sử không ghi vì tức giận", 53, 53, 0.2)
chip("Bùi Tùng Chi: nơi mất phải là Ba Lăng ngày nay", 54, 54, 0.2); fx("gong", A(52, 2.6))
route("thu2", [BK, (114.4, 30.6), (116.8, 31.0), KK], NG, 55, 0.5, 4.0, t1_i=56, w=4, arrow=True)
card("Chu Du", "tiến cử Lỗ Túc trước khi mất", 55, 0.3, 4.2, w=1000)
chip("Trí và mưu của Lỗ Túc đủ để thay ông", 56, 56, 0.2)
chip("Nằm bệnh vẫn lo tìm người giữ nước", 57, 57, 0.2)

# ============ 8. Người chủ khóc bạn (58–63) ============
C(58, 118.2, 31.4, 6.0); C(60, 118.2, 31.4, 6.0); C(61, 116.0, 30.8, 9.0); C(63, 115.5, 30.8, 10.0)
city("Kinh Khẩu", KK, "v", 58, 60, 26)
card("Tôn Quyền", "mặc áo tang trắng, đến khóc", 58, 0.3, 4.6, w=1000); ring(KK, 58, 0.8, NG, 2.0, 58)
chip("Chu Du có tài giúp vua, nay mất sớm", 59, 59, 0.2); chip("Biết nương tựa vào ai?", 59, 59, 3.0)
chip("Không nói hẹp hòi, mà nói: tài giúp vua", 60, 60, 0.2)
card("Trần Thọ", "tác giả bộ Tam quốc chí", 61, 0.3, 3.4, col=BRN)
chip("Chu Du và Lỗ Túc: hiểu biết, quyết đoán vượt người thường", 62, 62, 0.2)
chip("Người đương thời: quyết đoán và đáng tiếc", 63, 63, 0.2)

# ============ 9. Vì sao truyện khác (64–73) ============
C(64, 111.0, 31.2, 12.0); C(65, 106.5, 31.3, 7.0); C(66, 113.0, 30.6, 8.0); C(68, 113.5, 30.4, 5.0); C(71, 114.0, 30.4, 9.0); C(73, 113.5, 30.4, 6.5)
chip("Vì sao tiểu thuyết cho ông hộc máu mà chết?", 64, 64, 0.2)
lab("THỤC", (106.2, 31.0), LB, 65, 67, fs=64, op=0.5); city("Thành Đô", TDO, "s", 65, 66, 24)
chip("Tam quốc diễn nghĩa kể từ phía nước Thục", 65, 65, 0.2); 
chip("Cần người đối diện để làm nổi bật Gia Cát Lượng", 66, 66, 0.2)
chip("Chu Du giỏi, nổi tiếng, thắng trận lớn", 67, 67, 0.2)
city("Xích Bích", XB, "v", 68, 70, 28)
route("cong", [XB, (113.6, 30.2), CA], NG, 68, 0.6, 4.5, t1_i=68, w=5, arrow=True)
city("Công An", CA, "s", 68, 70, 24); chip("Lấy bớt công trạng của Chu Du, chuyển sang nhân vật mình yêu", 68, 68, 0.2)
chip("Rồi thêm tính hẹp hòi để có lý do thua", 68, 68, 5.0)
chip("Người kể chọn phe, chọn luôn ai bị hạ xuống", 69, 69, 0.2)
chip("Chu Du thành người nhỏ nhen để truyện đẹp hơn cho phe Gia Cát Lượng", 70, 70, 0.2)
chip("Ba lần bị chọc, ba lần thua, lần ba hộc máu", 71, 71, 2.8)

chip("Sử không có nhịp ba lần như thế", 73, 73, 0.2)
mark("arrow", (113.2, 30.0), 73, 2.2, 73, s=18, col=RD, ang=-50); mark("boat", (113.6, 29.55), 73, 2.8, 73, s=24)
fire((113.88, 29.93), A(73, 3.4), E_(73) + 0.4, 16); mark("x", BK, 73, 4.4, 73, s=18)

# ============ 10. Phần nào là thật (74–88) ============
C(74, 113.5, 30.4, 7.0); C(75, 113.3, 30.0, 5.0); C(76, 114.0, 30.4, 6.5); C(79, 113.5, 30.4, 8.0); C(82, 113.2, 30.3, 5.5); C(84, 115.0, 30.8, 11.0); C(86, 111.0, 31.0, 12.0); C(87, 113.5, 30.4, 14.0)
chip("Tầng 1: chính văn", 74, 74, 0.2); city("Xích Bích", XB, "v", 75, 76, 28)
fire((113.88, 29.93), A(75, 0.4), A(75, 3.0), 16); mark("x", (112.55, 30.15), 75, 3.4, 75, s=20); mark("x", BK, 75, 6.0, 75, s=20); city("Ba Khâu", BK, "v", 75, 76, 26)
chip("Chỉ huy Xích Bích, tên trúng sườn, gượng dậy, mất vì bệnh", 75, 75, 0.2, 6.0)
chip("Tiến cử Lỗ Túc, Tôn Quyền khóc", 76, 76, 0.2, 3.0); chip("Tầng 2: số quân Tào và chi tiết về gió", 76, 76, 3.6)
chip("Độ chắc thấp hơn chính văn", 77, 77, 0.2)
chip("Tầng 3: tiểu thuyết, Chu Du hẹp hòi, ba lần bị qua mặt", 78, 78, 0.2); chip("Không có trong những đoạn chính văn đã đọc", 79, 79, 0.2)
chip("Mới đọc truyện Chu Du và truyện Lỗ Túc", 80, 80, 0.2); chip("Chưa đọc truyện Gia Cát Lượng", 81, 81, 0.2)
big("BỆNH", 82, 3.0, 3.0, 560, 220, col=RD); chip("Chính văn: không có chuyện bị chọc tức đến chết", 82, 82, 0.2)
chip("Không có bằng chứng, và nó đến từ tiểu thuyết", 83, 83, 0.2)
city("Lư Giang", LG, "v", 84, 84, 24); city("Xích Bích", XB, "v", 84, 84, 24); city("Nam Quận", NQ, "s", 84, 84, 24); city("Ba Khâu", BK, "v", 84, 84, 24)
for k, p in enumerate([LG, XB, NQ, BK]):
    ring(p, 84, 0.6 + 2.2 * k, NG, 1.8)
chip("Nhường nhà, thắng trận lửa, gượng dậy, lo người thay mình", 84, 84, 0.2)
chip("Đó là Chu Du trong sử: mất khi 36 tuổi", 85, 85, 0.2)
route("ke_hoach", sl(NQ, TDO), NG, 86, 1.0, 4.0, t1_i=86, w=5, arrow=True, chev=True); city("Thành Đô", TDO, "s", 86, 86, 24)
chip("Tiếc nhất: chưa kịp làm nốt kế hoạch lớn", 86, 86, 0.2)
big("?", 87, 0.3, 3.0, 620, 300); chip("Bạn nghĩ đến người thắng Xích Bích, hay kẻ tức chết?", 87, 87, 0.2)
chip("Bạn biết họ từ sử hay từ truyện?", 88, 88, 0.2)


# ============ Hiệu ứng theo ý tưởng của chủ kênh (mặt nhân vật, thư bay, thanh quân số, chuông, ba tầng tư liệu...) ============
def face(name, p, hat, col, i0, i1, off=0.3, **kw):
    add("face", A(i0, off), E_(i1), lon=p[0], lat=p[1], name=name, hat=hat, col=col, fi=0.3, fo=0.5, **kw)


def letter(a, b, i, off, dur, i1=None, **kw):
    add("letter", A(i, off), min(E_(i1 or i), A(i, off + dur + (1.6 if kw.get("stamp") else 0.3))), a=list(a), b=list(b), dur=dur, fi=0.2, fo=0.5, **kw)
    fx("arrow", A(i, off), A(i, off + 0.8))
    if kw.get("stamp"):
        fx("drum", A(i, off + dur), A(i, off + dur + 0.4))


def hud(kind, t0, t1, **kw):
    add(kind, t0, t1, fi=0.5, fo=0.6, **kw)


# --- chương 1 ---
face("Chu Du", XB, "general", NG, 1, 3, 0.4, dx=-70, fall=[A(2, 2.6), A(3, 99), A(3, 99)], beard=False)
face("Gia Cát Lượng", HK, "scholar", LB, 3, 3, 3.4, dx=0)
fx("drum", A(1, 0.3), A(1, 3.5))
tiers_t0 = A(10, 0.3)
# --- chương 2 ---
face("Chu Du", LG, "general", NG, 12, 18, 0.6, dx=-110)
face("Tôn Sách", LG, "king", NG, 13, 16, 0.6, dx=110, r=40)
add("house", A(15, 0.5), A(15, 3.4), a=[116.9, 31.06], b=[117.1, 31.06], dur=2.6, fi=0.2, fo=0.5)
add("notes", A(17, 0.3), E_(17), lon=LG[0], lat=LG[1], wt=[A(17, 4.4), A(17, 6.4)], fi=0.4, fo=0.5)
for k, f0 in enumerate([261, 294, 330, 294, 261]):
    fx("pluck", A(17, 0.5 + 0.8 * k), A(17, 1.2 + 0.8 * k), f=f0)
fx("pluck", A(17, 4.4), A(17, 5.0), f=233, bad=1)
# --- chương 3 ---
face("Tào Tháo", TD, "lord", TA, 19, 20, 0.5, dx=-100)
hud("bars", A(20, 0.3), E_(22), bars=[{"label": "Tào Tháo xưng", "val": 1.0, "txt": "80 vạn quân", "col": TA}, {"label": "Chu Du tính", "val": 0.22, "txt": "15–16 vạn + 7–8 vạn hàng binh", "col": NG}], note="Lời trong chú giải, độ chắc thấp hơn chính văn")
face("Tôn Quyền", SCG, "king", NG, 23, 24, 0.3, dx=-100, r=40)
face("Chu Du", SCG, "general", NG, 23, 26, 0.3, dx=100, mv={"to": list(HK), "t0": A(24, 0.8), "t1": A(24, 5.0)})
big("3 VẠN", 24, 0.2, 2.4, 300, 150, col=NG)
# --- chương 4 ---
face("Hoàng Cái", XB, "general", NG, 27, 29, 0.4, dx=-110, r=38)
face("Chu Du", XB, "general", NG, 27, 33, 0.4, dx=110)
face("Tào Nhân", OL, "general", TA, 27, 31, 0.6, dx=110, r=36)
army([OL, (113.7, 30.2), (112.9, 30.3), NQ], "s", 31, 3.2, 3.4, n=8, t1_i=31, flag=True, u="inf", col="#8a8f98", stay=False)
add("glow", A(33, 0.3), E_(33), lon=XB[0], lat=XB[1], r=170, op=0.85, fi=0.8, fo=0.8)
# --- chương 5 ---
face("Chu Du", (112.55, 30.15), "general", NG, 34, 39, 0.4, dx=0, fall=[A(35, 5.6), A(37, 0.4), A(37, 2.2)])
face("Tào Nhân", NQ, "general", TA, 34, 39, 0.4, dx=-120, r=38, mv={"to": list(TD), "t0": A(38, 0.5), "t1": A(38, 4.2)})
fx("arrow", A(35, 5.2), A(35, 5.8))
add("glow", A(37, 0.8), E_(39), lon=112.55, lat=30.15, r=130, op=0.7, fi=1.0, fo=1.0)
# --- chương 6 ---
face("Chu Du", NQ, "general", NG, 40, 44, 0.3, dx=-100)
face("Tôn Quyền", KK, "king", NG, 40, 44, 0.3, dx=0, r=40)
letter(NQ, KK, 41, 0.3, 3.4)
letter(KK, NQ, 43, 0.3, 2.6, stamp="KHÔNG NGHE", sc="#b3261e")
face("Lưu Bị", CA, "lord", LB, 42, 43, 0.3, dx=-120, r=38, mv={"to": [118.6, 32.0], "t0": A(42, 1.5), "t1": A(42, 5.0)})
face("Quan Vũ", CA, "general", LB, 42, 43, 0.3, dx=0, r=36)
face("Trương Phi", CA, "general", LB, 42, 43, 0.3, dx=120, r=36)
# --- chương 7 ---
letter(NQ, KK, 48, 0.3, 3.2); letter(KK, NQ, 51, 0.2, 2.6, stamp="ĐỒNG Ý", sc="#2e7d32")
face("Chu Du", KK, "general", NG, 51, 51, 0.3, dx=-80, mv={"to": list(NQ), "t0": A(51, 1.5), "t1": A(51, 4.4)})
face("Chu Du", NQ, "general", NG, 52, 53, 0.0, dx=-80, mv={"to": list(BK), "t0": A(52, 0.2), "t1": A(52, 2.4)}, fall=[A(52, 3.2), A(53, 99), A(53, 99)])
hud("dim", A(52, 2.8), E_(53), a=0.5)
add("glow", A(55, 0.2), E_(57), lon=BK[0], lat=BK[1], r=130, op=0.75, fi=1.0, fo=1.0)
letter(BK, KK, 55, 0.6, 4.4)
face("Lỗ Túc", KK, "lord", NG, 55, 56, 0.6, dx=100, r=38)
# --- chương 8 ---
army([(118.75, 32.0), (119.2, 32.12), KK], "v", 58, 0.3, 4.0, n=14, t1_i=60, flag=True, u="inf", col="#f4f4f0")
face("Tôn Quyền", KK, "mourn", NG, 58, 60, 0.4, dx=0, r=44)
# --- chương 9 ---
hud("panels2", A(65, 0.4), E_(66))
face("Chu Du", XB, "general", NG, 68, 70, 0.3, dx=-110)
face("Gia Cát Lượng", CA, "scholar", LB, 68, 70, 0.3, dx=110)
add("token", A(68, 0.8), E_(68) + 0.3, a=list(XB), b=list(CA), dur=4.2, name="công trạng", fi=0.3, fo=0.6)
hud("bells", A(71, 0.3), E_(72), gap=2.4)
for k in range(3):
    fx("gong", A(71, 0.6 + k * 2.4))
hud("icons4", A(73, 0.4), E_(73) + 0.2, gap=1.5, items=[{"ic": "arrow", "txt": "một mũi tên", "col": "#b3261e"}, {"ic": "ship", "txt": "một con sông", "col": "#3a64a8"}, {"ic": "fire", "txt": "một trận lửa", "col": "#d9501c"}, {"ic": "cross", "txt": "một căn bệnh", "col": "#6b5a45"}])
# --- chương 10 ---
hud("tiers", A(74, 0.3), E_(79), hl=[[A(74, 0.3), A(76, 2.8), 0], [A(76, 2.8), A(78, 0.0), 1], [A(78, 0.0), E_(79), 2]],
    ic=[[A(75, 1.0), 0, "arrow"], [A(75, 3.5), 0, "fire"], [A(75, 6.2), 0, "cross"], [A(76, 0.5), 0, "letter"], [A(76, 3.0), 0, "drop"], [A(76, 5.4), 1, "people"], [A(77, 0.6), 1, "wind"], [A(78, 0.6), 2, "book"], [A(78, 3.0), 2, "question"]])

for _a, (_b, _ic, _ti, _ls, _off) in RICH.items():
    add("banner", A(_a, _off), E_(_b), title=_ti, lines=_ls, ic=_ic, col=(LB if _ic == "question" else NG), fi=0.5, fo=0.5)

# ---- phụ đề theo từng đoạn ----
def _wrap(txt, w=36):
    out, cur = [], ""
    for wd_ in txt.split():
        if cur and len(cur) + 1 + len(wd_) > w:
            out.append(cur); cur = wd_
        else:
            cur = (cur + " " + wd_).strip()
    if cur:
        out.append(cur)
    return out


def _pages(t, mx=66):
    parts = [p.strip() for p in re.split(r"(?<=[.?!])\s+", t) if p.strip()]
    pages = []
    for p in parts:
        cl = [c.strip() for c in re.split(r"(?<=,)\s+", p) if c.strip()] if len(p) > mx else [p]
        pages.extend(cl)
    out, cur = [], ""
    for p in pages:
        if cur and len(cur + " " + p) > mx:
            out.append(cur); cur = p
        else:
            cur = (cur + " " + p).strip()
    if cur:
        out.append(cur)
    res = []
    for p in out:
        if len(_wrap(p)) > 2:
            ws = p.split(); h = len(ws) // 2; res += [" ".join(ws[:h]), " ".join(ws[h:])]
        else:
            res.append(p)
    return res


ASR = json.load(open(ROOT / "phim_ban_do/asr_cd.json", encoding="utf-8"))
for _i, _b in enumerate(KB, 1):
    _pg = _pages(_b["text"])
    _w = ASR.get(str(_b["n"])) or []
    _tot = sum(len(p.split()) for p in _pg)
    _cw = 0; _starts = []
    for p in _pg:
        if _w:
            _k = min(len(_w) - 1, round(_cw * len(_w) / _tot))
            _starts.append(max(0.0, _w[_k][1] - 0.05))
        else:
            _starts.append(0.05 + (D[_i] - 0.1) * _cw / _tot)
        _cw += len(p.split())
    _starts[0] = 0.0
    for _k, p in enumerate(_pg):
        _t0 = S[_i] + _starts[_k]
        _t1 = S[_i] + (_starts[_k + 1] if _k + 1 < len(_pg) else D[_i] + 0.05)
        add("sub", _t0, _t1, lines=_wrap(p), fi=0.1, fo=0.1)

# camera: giữ khung của đoạn đang kể, chỉ chuyển ở 2,4 giây cuối
cam.sort(key=lambda k: k[0])
res = []
for k in cam:
    if res and k[0] - res[-1][0] > 2.6 and (res[-1][1:] != k[1:]):
        res.append([round(k[0] - 2.4, 3)] + res[-1][1:])
    res.append(k)
cam[:] = res
if cam[0][0] > 0:
    cam.insert(0, [0.0] + cam[0][1:])
cam.append([TOTAL] + cam[-1][1:])
FORTS = []   # thành chỉ hiện khi có mục city (có tên), không vẽ thành vô danh
SPEC = {"dur": round(TOTAL, 2), "rivers": RIVERS, "lakes": LAKES, "forts": FORTS, "cam": cam, "items": items, "fade0": 0.5, "fade1": 1.5, "starts": {i: round(S[i], 2) for i in S}}
(HERE / "spec_cd.js").write_text("window.SPEC=" + json.dumps(SPEC, ensure_ascii=False) + ";", encoding="utf-8")
json.dump({"dur": TOTAL, "sfx": sfx, "starts": {i: S[i] for i in S}, "pstarts": {str(b["n"]): PS[k][0] for k, b in enumerate(KB)}, "durs": {i: D[i] for i in D}}, open(HERE / "sfx_cd.json", "w"), indent=1)
print("tổng", round(TOTAL, 1), "giây =", round(TOTAL / 60, 2), "phút;", len(items), "mục hình;", len(sfx), "mục âm thanh")
