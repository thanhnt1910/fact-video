#!/usr/bin/env python3
"""Sinh spec dựng Tập 1 «Quốc Tử Giám Thăng Long» cho engine arch3d.js.
  python3 tao_spec.py [thư mục giọng/chuan]   -> ../specs/qtg1.json
Không có thư mục giọng thì ước thời lượng 3,3 tiếng/giây (để xem thử bố cục)."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
segs = json.load(open(os.path.join(HERE, 'loi_doc.json')))
VOICE = sys.argv[1] if len(sys.argv) > 1 else None
dur = json.load(open(os.path.join(VOICE, 'thoi_luong.json'))) if VOICE else {}
def tieng(t): return len(re.findall(r"[\wÀ-ỹ]+", t))
def sdur(s): return dur.get(str(s['n']), tieng(s['text']) / 3.3)

CHAP_START = {'mo_dem', 'bc_ban_do', 'ht_van_mieu', 'hs_buoi_hoc', 'nv_le_van_thinh', 'bd_le_trung_hung', 'kt_unesco'}
LEAD = {'mo_dem': 3.0, 'mo_tieu_de': 1.0}           # giây nhạc trước lời ở đầu cảnh
TAIL = {'mo_tieu_de': 3.5, 'kt_cau_ket': 1.5, 'kt_tap_sau': 3.0}

# ---------- thời gian: mỗi cảnh (canh) gồm các đoạn lời liên tiếp ----------
order = []
for s in segs:
    if not order or order[-1][0] != s['canh']: order.append((s['canh'], []))
    order[-1][1].append(s)
t = 0.0; CANH = {}; voice_items = []; subs = []
for canh, ss_ in order:
    t0 = t; t += LEAD.get(canh, 1.6 if canh in CHAP_START else 0.7)
    for i, s in enumerate(ss_):
        d = sdur(s); voice_items.append({'n': s['n'], 'at': round(t, 3)})
        subs.append({'t0': round(t, 2), 't1': round(t + d, 2), 'text': s['text']}); t += d + (0.45 if i < len(ss_) - 1 else 0)
    t += TAIL.get(canh, 0.6)
    CANH[canh] = (round(t0, 3), round(t, 3))
TOTAL = t

# ---------- bối cảnh ----------
B, G, T, HS, C, BD, LT, TER, P = [], [], [], [], [], [], [], [], []
GRP = {}     # nhóm công trình Văn Miếu -> list chỉ số trong B (để gán show sau)
def addb(d, grp=None):
    B.append(d)
    if grp: GRP.setdefault(grp, []).append(d)
    return d

# === Văn Miếu – Quốc Tử Giám (gốc toạ độ) ===
X = 38; ZN = 330
def wall(a, b, h=2.6, grp='walls', **k): addb({'type': 'wall', 'from': a, 'to': b, 'h': h, **k}, grp)
wall([-X, 0], [-X, ZN]); wall([X, 0], [X, ZN]); wall([-X, ZN], [X, ZN])
for z, gap in [(0, 10), (75, 10), (135, 6), (200, 10), (268, 9)]: wall([-X, z], [-gap, z]); wall([gap, z], [X, z])
addb({'type': 'gate', 'pos': [0, 0], 'cw': 9, 'ch': 5.6, 'd': 6, 'sw': 5, 'sh': 3.8, 'tiers': 2, 'plaque': '文廟門'}, 'gates')
addb({'type': 'gate', 'pos': [0, 75], 'cw': 8, 'ch': 5, 'd': 5.5, 'sw': 4.5, 'sh': 3.4, 'tiers': 1, 'plaque': '大中門'}, 'gates')
addb({'type': 'khueVanCac', 'pos': [0, 135], 's': 7.2}, 'kvc')
addb({'type': 'gate', 'pos': [0, 135], 'cw': 5, 'ch': 3.4, 'd': 3, 'sides': False, 'tiers': 1}, 'prekvc')
for x in (-20, 20): addb({'type': 'gate', 'pos': [x, 135], 'cw': 4, 'ch': 3.4, 'd': 3, 'sides': False, 'tiers': 1}, 'gates')
addb({'type': 'gate', 'pos': [0, 200], 'cw': 9, 'ch': 5.4, 'd': 6, 'sw': 5, 'sh': 3.8, 'tiers': 1, 'plaque': '大成門'}, 'mieu')
addb({'type': 'gate', 'pos': [0, 268], 'cw': 7, 'ch': 4.8, 'd': 5, 'sw': 4, 'sh': 3.2, 'tiers': 1, 'plaque': '太學門'}, 'qtg')
addb({'type': 'pond', 'pos': [0, 167], 'size': [24, 24], 'rail': True, 'tint': [0.5, 0.6, 0.55]}, 'gieng')
for sg in (-1, 1):
    addb({'type': 'hall', 'pos': [sg * 22, 167], 'rot': 90, 'w': 50, 'd': 7, 'colH': 3.4, 'base': 0.5, 'walls': 'none', 'steps': False, 'roofH': 2.6, 'spacing': 4.2, 'ov': 1.4}, 'nhabia')
    addb({'type': 'stelae', 'from': [sg * 21, 144], 'to': [sg * 21, 190], 'count': 41, 'rows': 2, 'rowGap': 2.4, 'face': -sg}, 'bia')
addb({'type': 'hall', 'pos': [0, 246], 'w': 38, 'd': 12, 'colH': 4.6, 'walls': 'all', 'roofH': 5.2, 'pearl': True}, 'mieu')
addb({'type': 'hall', 'pos': [0, 261], 'w': 28, 'd': 7, 'colH': 3.8, 'walls': 'all', 'roofH': 3.6, 'steps': False}, 'mieu')
for sg in (-1, 1): addb({'type': 'hall', 'pos': [sg * 30, 222], 'w': 28, 'd': 7, 'colH': 3.4, 'walls': 'back', 'roofH': 3.2, 'rot': 90 if sg < 0 else -90}, 'mieu')
addb({'type': 'hall', 'pos': [0, 312], 'w': 40, 'd': 14, 'colH': 5, 'tiers': 2, 'roofH': 3.4, 'upperH': 3.2, 'walls': 'back', 'rot': 180, 'pearl': True}, 'qtg')
for sg in (-1, 1):
    addb({'type': 'hall', 'pos': [sg * 31, 298], 'rot': 90 if sg < 0 else -90, 'w': 24, 'd': 6.5, 'colH': 3.4, 'walls': 'back', 'roofH': 3}, 'qtg')
    addb({'type': 'hall', 'pos': [sg * 19, 283], 'w': 6, 'd': 6, 'colH': 3.6, 'tiers': 2, 'roofH': 2, 'upperH': 2.4, 'walls': 'back', 'spacing': 3}, 'qtg')
for (x, z, w, d) in [(0, 312, 42, 16), (-31, 298, 8, 26), (31, 298, 8, 26)]: addb({'type': 'box', 'pos': [x, z], 'size': [w, 0.7, d], 'mat': 'stone'}, 'nen')
addb({'type': 'scaffold', 'pos': [0, 312], 'size': [44, 18, 14]}, 'gian')
addb({'type': 'pond', 'pos': [0, -48], 'size': [100, 46], 'rim': 1.2, 'tint': [0.45, 0.55, 0.5]}, 'ho')
addb({'type': 'hall', 'pos': [0, -48], 'w': 7, 'd': 7, 'colH': 3.2, 'walls': 'none', 'roofH': 2.6, 'base': 0.9, 'steps': False, 'spacing': 3.5}, 'ho')
for x in (-6.5, -2.2, 2.2, 6.5): addb({'type': 'wall', 'from': [x - 0.45, -3], 'to': [x + 0.45, -3], 'h': 6.5 if abs(x) < 3 else 5.5, 't': 0.9, 'mat': 'plaster'}, 'gates')
addb({'type': 'stela1', 'pos': [-11, 0, 172]}, 'khac')
for txt, z in [('Nhập đạo', 37), ('Thành đạt', 105), ('Vườn bia tiến sĩ', 167), ('Đại Thành', 234), ('Thái Học', 300)]:
    addb({'type': 'label', 'pos': [0, 32, z], 'text': txt, 'size': 9}, 'nhan_' + txt)
for txt, z in [('Ngô Sĩ Liên', 150), ('Lương Thế Vinh', 160), ('Lê Quý Đôn', 172), ('Ngô Thì Nhậm', 184)]:
    addb({'type': 'label', 'pos': [-21, 4.2, z], 'text': txt, 'size': 0.55}, 'ten_' + txt)
G += [{'rect': [-X, 0, X, ZN], 'mat': 'grass', 'y': 0.06}]
for z0, z1 in [(0, 75), (75, 135)]: G.append({'rect': [-3, z0, 3, z1], 'mat': 'pave', 'y': 0.14, 'tile': 2})
G += [{'rect': [-16, 135, 16, 200], 'mat': 'pave', 'y': 0.14, 'tile': 2}, {'rect': [-X, 200, X, ZN], 'mat': 'pave', 'y': 0.14, 'tile': 2},
      {'rect': [-60, -20, 60, -3.5], 'mat': 'road', 'y': 0.09}, {'rect': [-58, -3.5, 58, -1], 'mat': 'pave', 'y': 0.14, 'tile': 2},
      {'rect': [-60, -100, -44, 360], 'mat': 'road', 'y': 0.09}, {'rect': [44, -100, 60, 360], 'mat': 'road', 'y': 0.09},
      {'rect': [-60, 336, 60, 352], 'mat': 'road', 'y': 0.09}, {'rect': [-54, -76, 54, -20], 'mat': 'grass', 'y': 0.07}, {'rect': [-7, -53, 7, -43], 'mat': 'grass', 'y': 0.3}]
T += [{'rect': [-36, 3, -14, 72], 'count': 16, 'h': [8, 15]}, {'rect': [14, 3, 36, 72], 'count': 16, 'h': [8, 15]},
      {'rect': [-36, 78, -14, 132], 'count': 12, 'h': [8, 14]}, {'rect': [14, 78, 36, 132], 'count': 12, 'h': [8, 14]},
      {'rect': [-36, 138, -28, 198], 'count': 8, 'h': [9, 15]}, {'rect': [28, 138, 36, 198], 'count': 8, 'h': [9, 15]},
      {'rect': [-14, 204, 14, 232], 'count': 3, 'h': [13, 17], 'avoid': [[-6, 204, 6, 240]]},
      {'rect': [-53, -75, 53, -21], 'count': 26, 'h': [8, 13], 'avoid': [[-51, -72, 51, -24], [-10, -40, 10, -14]]},
      {'rect': [-420, -300, 420, 700], 'count': 420, 'h': [7, 13], 'avoid': [[-62, -80, 62, 355]]},
      {'rect': [-43, -18, -39, 340], 'count': 30, 'h': [9, 14]}, {'rect': [39, -18, 43, 340], 'count': 30, 'h': [9, 14]}]
HS += [{'rect': [-420, -300, 420, 700], 'count': 320, 'avoid': [[-62, -80, 62, 355]]}]
LT += [{'points': [[x, 3.2, z] for z in range(10, 330, 22) for x in (-3.8, 3.8) if not (128 < z < 205)]},
       {'points': [[x, 2.6, z] for x in range(-12, 13, 6) for z in (154.2, 179.8)] + [[x, 2.6, z] for z in range(158, 178, 6) for x in (-12.6, 12.6)]},
       {'points': [[x, 3.6, 252.6] for x in range(-17, 18, 5)] + [[x, 4.0, 318.8] for x in range(-18, 19, 6)]}]

# === Kinh thành Thăng Long (0, 2600) ===
CZ = 2600
def cwall(a, b): addb({'type': 'wall', 'from': a, 'to': b, 'h': 5.5, 't': 1.4})
for (a, b) in [([-150, CZ - 150], [-12, CZ - 150]), ([12, CZ - 150], [150, CZ - 150]), ([150, CZ - 150], [150, CZ + 150]), ([150, CZ + 150], [-150, CZ + 150]), ([-150, CZ + 150], [-150, CZ - 150])]: cwall(a, b)
addb({'type': 'gate', 'pos': [0, CZ - 150], 'cw': 12, 'ch': 7, 'd': 8, 'sw': 7, 'sh': 5, 'tiers': 2, 'mat': 'brick'})
addb({'type': 'gate', 'pos': [0, CZ - 40], 'cw': 9, 'ch': 5.5, 'd': 6, 'sw': 5, 'sh': 4, 'tiers': 1, 'mat': 'plaster'})
for (a, b) in [([-70, CZ - 40], [-14, CZ - 40]), ([14, CZ - 40], [70, CZ - 40])]: addb({'type': 'wall', 'from': a, 'to': b, 'h': 3})
addb({'type': 'hall', 'pos': [0, CZ + 40], 'w': 44, 'd': 20, 'colH': 6, 'base': 2.6, 'tiers': 2, 'roofH': 4, 'upperH': 3.6, 'walls': 'back', 'rot': 180, 'pearl': True})
addb({'type': 'hall', 'pos': [0, CZ + 95], 'w': 32, 'd': 14, 'colH': 5, 'base': 1.4, 'walls': 'all', 'roofH': 4.4})
for sg in (-1, 1): addb({'type': 'hall', 'pos': [sg * 58, CZ + 10], 'rot': 90 if sg < 0 else -90, 'w': 46, 'd': 10, 'colH': 4.2, 'walls': 'back', 'roofH': 3.6})
addb({'type': 'box', 'pos': [0, CZ + 22], 'size': [16, 2.6, 6], 'mat': 'stone'})
addb({'type': 'board', 'pos': [-30, CZ - 25], 'w': 6, 'h': 3, 'rot': 20})
addb({'type': 'pond', 'pos': [300, CZ], 'size': [140, 1600], 'rim': 0.01, 'tint': [0.62, 0.5, 0.38]})
G += [{'rect': [-150, CZ - 150, 150, CZ + 150], 'mat': 'grass', 'y': 0.06}, {'rect': [-70, CZ - 40, 70, CZ + 30], 'mat': 'pave', 'y': 0.14, 'tile': 2},
      {'rect': [-8, CZ - 150, 8, CZ - 40], 'mat': 'pave', 'y': 0.14, 'tile': 2}, {'rect': [-700, CZ - 240, 228, CZ - 170], 'mat': 'dirt', 'y': 0.09}]
T += [{'rect': [-145, CZ - 145, 145, CZ + 145], 'count': 60, 'h': [9, 15], 'avoid': [[-80, CZ - 60, 80, CZ + 120], [-12, CZ - 150, 12, CZ - 30]]}, {'rect': [-700, CZ - 700, 220, CZ + 700], 'count': 320, 'avoid': [[-170, CZ - 170, 170, CZ + 170]]}]
HS += [{'rect': [-700, CZ - 700, 220, CZ + 700], 'count': 260, 'avoid': [[-175, CZ - 175, 175, CZ + 175]], 'style': 'village', 'hgt': [3, 5]}]

# === Làng quê và chùa (-2600, 0) ===
VX = -2600
addb({'type': 'gate', 'pos': [VX, -60], 'cw': 5, 'ch': 4.2, 'd': 3, 'sides': False, 'tiers': 1, 'mat': 'plaster'})
addb({'type': 'hall', 'pos': [VX + 40, 40], 'w': 14, 'd': 9, 'colH': 3.6, 'walls': 'back', 'roofH': 3.4, 'base': 0.7})
addb({'type': 'hall', 'pos': [VX - 40, 30], 'w': 11, 'd': 7, 'colH': 3.0, 'walls': 'back', 'roofH': 3.0, 'base': 0.4, 'roofMat': 'thatch', 'curl': 0.15})
addb({'type': 'hall', 'pos': [VX - 30, -30], 'rot': 90, 'w': 8, 'd': 6, 'colH': 2.8, 'walls': 'all', 'roofH': 2.8, 'base': 0.3, 'roofMat': 'thatch', 'curl': 0.1})
addb({'type': 'desks', 'origin': [VX - 44.5, 28.5], 'rows': 2, 'cols': 4, 'dx': 2.4, 'dz': 2.3, 'y': 0.4, 'rot': 3.14159})
G += [{'rect': [VX - 3, -140, VX + 3, 140], 'mat': 'dirt', 'y': 0.09}, {'rect': [VX + 3, 30, VX + 34, 34], 'mat': 'dirt', 'y': 0.09}, {'rect': [VX - 34, 26, VX - 3, 30], 'mat': 'dirt', 'y': 0.09}]
T += [{'rect': [VX - 220, -260, VX + 220, 260], 'count': 220, 'h': [6, 12], 'avoid': [[VX - 6, -150, VX + 6, 150], [VX + 30, 30, VX + 50, 50], [VX - 50, 22, VX - 30, 40], [VX - 36, -38, VX - 24, -22]]},
      {'rect': [VX + 22, 28, VX + 28, 34], 'count': 1, 'h': [18, 19], 'wide': 2.2}]
HS += [{'rect': [VX - 200, -220, VX + 200, 220], 'count': 70, 'avoid': [[VX - 8, -150, VX + 8, 150], [VX + 28, 28, VX + 52, 52], [VX - 52, 20, VX - 28, 40], [VX - 38, -40, VX - 22, -20]], 'style': 'village', 'w': [5, 8], 'd': [7, 10], 'hgt': [2.5, 3.5]}]
LT += [{'points': [[VX - 32.6, 1.9, -25.2]]}]

# === Trường thi (2600, 0) ===
EX = 2600
addb({'type': 'fence', 'rect': [EX - 80, -60, EX + 80, 60]})
addb({'type': 'tents', 'rect': [EX - 70, -48, EX + 70, 40], 'rows': 8, 'cols': 14}, 'leu')
addb({'type': 'hall', 'pos': [EX, 50], 'w': 7, 'd': 7, 'colH': 3, 'base': 4.5, 'tiers': 2, 'roofH': 2.2, 'upperH': 2.2, 'walls': 'none', 'steps': False})
addb({'type': 'gate', 'pos': [EX, -60], 'cw': 6, 'ch': 4.5, 'd': 3, 'sides': False, 'tiers': 1, 'mat': 'wood'})
addb({'type': 'board', 'pos': [EX + 14, -70], 'w': 7, 'h': 3.2, 'rot': 180})
G += [{'rect': [EX - 80, -60, EX + 80, 60], 'mat': 'dirt', 'y': 0.09}, {'rect': [EX - 4, -140, EX + 4, -60], 'mat': 'dirt', 'y': 0.09}]
T += [{'rect': [EX - 300, -300, EX + 300, 300], 'count': 160, 'avoid': [[EX - 90, -150, EX + 90, 70]]}]
HS += [{'rect': [EX - 300, -300, EX + 300, 300], 'count': 60, 'avoid': [[EX - 95, -150, EX + 95, 75]], 'style': 'village', 'hgt': [2.5, 4]}]

# === Giảng đường (2600, 2600) ===
KX, KZ = 2600, 2600
addb({'type': 'hall', 'pos': [KX, KZ], 'w': 26, 'd': 16, 'colH': 5.5, 'walls': 'back', 'roofH': 5, 'base': 0.6, 'spacing': 4.3})
addb({'type': 'desks', 'origin': [KX - 7.8, KZ - 3.4], 'rows': 4, 'cols': 7, 'dx': 2.6, 'dz': 2.3, 'y': 0.6, 'rot': 3.14159})
addb({'type': 'box', 'pos': [KX, 0.6, KZ - 6.6], 'size': [7, 0.5, 2.4], 'mat': 'darkwood'})
G += [{'rect': [KX - 60, KZ - 60, KX + 60, KZ + 60], 'mat': 'pave', 'y': 0.14, 'tile': 2}]
T += [{'rect': [KX - 200, KZ - 200, KX + 200, KZ + 200], 'count': 120, 'avoid': [[KX - 25, KZ - 20, KX + 25, KZ + 40]]}]
LT += [{'points': [[x, 4.6, KZ + 7.6] for x in range(KX - 12, KX + 13, 6)]}]

# === Núi Phượng Hoàng (-2600, 2600) ===
MX, MZ = -2600, 2600
TER.append({'pos': [MX, MZ], 'size': [1400, 1400], 'height': 14, 'scale': 0.01, 'peak': [MX, MZ + 260, 260, 150], 'flat': [[MX, MZ - 300, 90]], 'seg': 160})
T += [{'rect': [MX - 650, MZ - 650, MX + 650, MZ + 650], 'count': 700, 'h': [7, 13], 'avoid': [[MX - 8, MZ - 320, MX + 8, MZ + 40]]}]
addb({'type': 'hall', 'pos': [MX + 10, MZ + 30], 'w': 7, 'd': 5, 'colH': 2.6, 'walls': 'all', 'roofH': 2.6, 'base': 0.4, 'roofMat': 'thatch', 'curl': 0.1, 'onGround': True})

# === Sa bàn địa hình (20000, 0) ===
MPX = 20000
TL, THH, PX = [MPX - 120, 2250], [MPX + 60, 900], [MPX + 120, -2350]
TER.append({'pos': [MPX, 0], 'size': [2800, 6400], 'height': 380, 'scale': 0.0018, 'mount': 'west', 'seed': 7, 'seg': 220, 'vivid': True, 'ocean': True,
            'coast': {'x0': 520, 'amp': 140, 'freq': 0.0007, 'tilt': 0.04},
            'rivers': [[[[MPX - 700, 3100], [MPX - 300, 2600], [MPX - 120, 2250], [MPX + 250, 1900], [MPX + 800, 1550]], 22], [[[MPX - 300, -2500], [MPX + 120, -2350], [MPX + 450, -2280]], 10]],
            'flat': [[TL[0], TL[1], 120], [THH[0], THH[1], 80], [PX[0], PX[1], 90]]})
addb({'type': 'marker', 'pos': TL, 'text': 'Thăng Long', 'h': 260, 'size': 130, 'onGround': True}, 'mk_tl')
addb({'type': 'marker', 'pos': PX, 'text': 'Phú Xuân', 'h': 260, 'size': 130, 'onGround': True}, 'mk_px')
addb({'type': 'marker', 'pos': THH, 'text': 'Thanh Hóa', 'h': 220, 'size': 110, 'onGround': True}, 'mk_th')
addb({'type': 'route', 'points': [TL, [MPX - 40, 1500], THH, [MPX + 80, 0], [MPX + 40, -1100], [MPX + 80, -1800], PX], 'r': 12, 'lift': 24}, 'duong')

# ---------- mô hình làm sẵn CC0 (Poly Haven, đã rút gọn) ----------
PR = []
cay = [[sg * x, z] for sg in (-1, 1) for x, z in [(9, 12), (11, 30), (8.5, 48), (10.5, 64), (9, 88), (11, 108), (9.5, 124)]]
for k, m in enumerate(['island_tree_01', 'island_tree_02', 'island_tree_03']): PR.append({'model': m, 'points': cay[k::3], 'scale': [0.75, 0.95]})
for r in ([-36, 4, -5, 72], [5, 4, 36, 72], [-36, 79, -5, 132], [5, 79, 36, 132]): PR.append({'model': 'grass_medium_01', 'rect': r, 'count': 14, 'scale': [0.9, 1.4], 'shadow': False})
PR += [{'model': 'fern_02', 'rect': [-14, 150, -12.6, 184], 'count': 8, 'scale': [0.7, 1.0], 'shadow': False}, {'model': 'fern_02', 'rect': [12.6, 150, 14, 184], 'count': 8, 'scale': [0.7, 1.0], 'shadow': False},
       {'model': 'ceramic_pot', 'points': [[-6, 237], [6, 237], [-6, 304], [6, 304], [VX + 35, 46], [VX + 45, 46]], 'scale': [1.5, 1.7], 'rot': 0},
       {'model': 'pachira_aquatica_01', 'points': [[-6, 237, 0.95], [6, 237, 0.95], [-6, 304, 0.95], [6, 304, 0.95]], 'scale': [0.6, 0.7], 'rot': 0},
       {'model': 'boulder_01', 'points': [[-50, -66], [48, -30], [-46, -28], [MX + 6, MZ - 220], [MX - 9, MZ - 150]], 'scale': [0.4, 0.8]},
       {'model': 'fern_02', 'rect': [VX - 60, -30, VX + 60, 60], 'count': 30, 'scale': [0.8, 1.2], 'avoid': [[VX - 6, -150, VX + 6, 150]], 'shadow': False},
       {'model': 'chinese_tea_table', 'points': [[VX + 40, 42.2, 0.7]], 'scale': 1.0, 'rot': 0}]

# ---------- trạng thái các nhóm Văn Miếu theo cảnh ----------
NOW = {'walls', 'gates', 'kvc', 'gieng', 'nhabia', 'bia', 'mieu', 'qtg', 'ho'}
LY0 = {'walls', 'gieng', 'ho', 'prekvc'}
LY1 = LY0 | {'mieu'}; LY2 = LY1 | {'qtg'}; LE = LY2 | {'gates', 'nhabia', 'bia'}; NG = (LE - {'prekvc'}) | {'kvc'}
STATE = {}   # canh hoặc (canh, i) -> tập nhóm ; mặc định NOW

# ---------- cảnh quay ----------
SH = []   # (canh, phần) -> shot
def V(*a): return list(a)
def shot(canh, cam, env='day', frac=1.0, vm=None, cap=None, people=(), env2=None, extra=None):
    SH.append({'canh': canh, 'cam': cam, 'env': env, 'env2': env2, 'frac': frac, 'vm': vm, 'cap': cap, 'people': list(people), 'extra': extra or {}})
def YEAR(y, txt, at=0.3): return [{'style': 'year', 'year': y, 'text': txt, 'at': at, 'dur': 5.5}]

# 1. Mở đầu
shot('mo_dem', {'from': {'pos': V(0, 1.6, 196), 'look': V(0, 2.5, 150)}, 'to': {'pos': V(0, 3.2, 184), 'look': V(0, 7, 135)}, 'tilt': 0.45, 'shadow': 60}, 'night')
shot('mo_canh', {'from': {'pos': V(-15.5, 2.0, 146), 'look': V(-21.5, 1.4, 160)}, 'to': {'pos': V(-15.5, 2.3, 176), 'look': V(-21.5, 1.3, 194)}, 'ease': 'linear', 'fov': 44, 'tilt': 0.7}, 'dawn', 0.5,
     people=[{'crowd': {'rect': [-14, 140, 14, 196], 'count': 12, 'costume': 'scholar', 'alongZ': 0.5}}])
shot('mo_canh', {'from': {'pos': V(EX - 60, 30, -110), 'look': V(EX, 0, 0)}, 'to': {'pos': V(EX - 20, 22, -90), 'look': V(EX, 0, 0)}, 'tilt': 1.0}, 'day', 0.5, people=['thi_sinh'])
shot('mo_hoi', {'orbit': {'center': V(0, 0, 170), 'a': [210, 250], 'r': [220, 200], 'y': [120, 95]}, 'fov': 42, 'tilt': 1.1, 'shadow': 230}, 'dusk')
shot('mo_tieu_de', {'from': {'pos': V(60, 140, -60), 'look': V(0, 0, 170)}, 'to': {'pos': V(30, 170, -30), 'look': V(0, 0, 175)}, 'tilt': 1.2, 'shadow': 230}, 'dusk', env2='night',
     cap=[{'style': 'title', 'over': 'LỊCH SỬ ĐẠI HỌC VIỆT NAM · TẬP 1', 'cn': '國子監', 'text': 'QUỐC TỬ GIÁM THĂNG LONG', 'at': 0.4, 'dur': 99}])
# 2. Bối cảnh
shot('bc_ban_do', {'from': {'pos': V(MPX - 900, 2600, -1800), 'look': V(MPX, 0, 900)}, 'to': {'pos': V(TL[0] - 500, 700, TL[1] - 1100), 'look': V(TL[0], 0, TL[1])}, 'fov': 50, 'tilt': 0.3, 'shadow': 2600, 'far': 12000}, 'map',
     cap=YEAR('1010', 'Nhà Lý dời đô về Thăng Long'))
shot('bc_truoc_ly', {'from': {'pos': V(TL[0] - 300, 900, TL[1] - 400), 'look': V(TL[0] - 200, 0, TL[1] + 300)}, 'to': {'pos': V(TL[0] - 900, 1100, TL[1] - 1400), 'look': V(TL[0] - 500, 0, TL[1] - 200)}, 'fov': 50, 'tilt': 0.3, 'shadow': 2000, 'far': 12000}, 'map')
shot('bc_chua', {'from': {'pos': V(VX + 30, 3.2, 58), 'look': V(VX + 40, 2.0, 44)}, 'to': {'pos': V(VX + 36, 2.6, 54), 'look': V(VX + 40, 1.8, 44)}, 'fov': 42, 'tilt': 0.5}, 'dawn', people=['chua'])
shot('bc_lang', {'from': {'pos': V(VX - 33, 2.4, 40), 'look': V(VX - 40, 1.2, 29)}, 'to': {'pos': V(VX - 37, 2.0, 38), 'look': V(VX - 41, 1.0, 29)}, 'fov': 44, 'tilt': 0.55}, 'day', people=['lop_lang'])
shot('bc_trieu', {'from': {'pos': V(-34, 3.0, CZ - 30), 'look': V(0, 6, CZ + 40)}, 'to': {'pos': V(22, 6.0, CZ - 20), 'look': V(0, 8, CZ + 40)}, 'fov': 46, 'tilt': 0.6, 'shadow': 140}, 'day', people=['trieu'])
# 3. Hình thành
shot('ht_van_mieu', {'from': {'pos': V(-60, 30, 170), 'look': V(0, 2, 240)}, 'to': {'pos': V(-36, 16, 205), 'look': V(0, 4, 245)}, 'fov': 46, 'tilt': 0.7, 'shadow': 140}, 'dawn', vm=('LY0', 'LY1'),
     cap=YEAR('1070', 'Vua Lý Thánh Tông dựng Văn Miếu'), people=['le_mieu'])
shot('ht_khoa_thi', {'from': {'pos': V(0, 5, CZ - 34), 'look': V(0, 1, CZ - 10)}, 'to': {'pos': V(-12, 3.5, CZ - 26), 'look': V(-28, 3, CZ - 25)}, 'fov': 46, 'tilt': 0.6}, 'day',
     cap=YEAR('1075', 'Khoa thi Nho học đầu tiên'), people=['thi_dau'])
shot('ht_qtg', {'from': {'pos': V(30, 22, 250), 'look': V(0, 3, 300)}, 'to': {'pos': V(10, 6, 272), 'look': V(0, 6, 312)}, 'fov': 46, 'tilt': 0.6, 'shadow': 140}, 'day', vm=('LY1', 'LY2'),
     cap=YEAR('1076', 'Vua Lý Nhân Tông lập Quốc Tử Giám'), people=['hoang_tu'])
shot('ht_toan_canh', {'from': {'pos': V(90, 120, 110), 'look': V(0, 0, 250)}, 'to': {'pos': V(110, 160, 60), 'look': V(0, 0, 230)}, 'fov': 42, 'tilt': 1.0, 'shadow': 230}, 'day', 0.4, vm='LY2')
shot('ht_toan_canh', {'from': {'pos': V(130, 230, -120), 'look': V(0, 0, 165)}, 'to': {'pos': V(90, 260, -60), 'look': V(0, 0, 170)}, 'fov': 42, 'tilt': 0.6, 'shadow': 260}, 'day', 0.6, vm='NOW', extra={'labels5': True})
shot('ht_1086', {'from': {'pos': V(-24, 2.2, CZ - 34), 'look': V(-30, 3.6, CZ - 25)}, 'to': {'pos': V(-26, 2.0, CZ - 30), 'look': V(-30, 3.6, CZ - 25)}, 'fov': 42, 'tilt': 0.5}, 'day',
     cap=YEAR('1086', 'Khoa thi chọn người giỏi văn học'), people=['doc_bang'])
# 4. Đời sống học tập
shot('hs_buoi_hoc', {'from': {'pos': V(-6, 2.0, 262), 'look': V(0, 2.5, 300)}, 'to': {'pos': V(-3, 1.8, 284), 'look': V(0, 3.5, 312)}, 'fov': 46, 'tilt': 0.5}, 'dawn', vm='LY2', people=['vao_lop'])
shot('hs_hoc_gi', {'from': {'pos': V(KX + 8, 3.4, KZ + 12), 'look': V(KX - 1, 1.2, KZ - 3)}, 'to': {'pos': V(KX + 3, 2.6, KZ + 9), 'look': V(KX - 1, 1.3, KZ - 5)}, 'fov': 46, 'tilt': 0.45}, 'inside', people=['lop_trong'])
shot('hs_tran', {'from': {'pos': V(7, 2.4, 292), 'look': V(0, 2.5, 268)}, 'to': {'pos': V(6, 2.4, 290), 'look': V(0, 2.6, 268)}, 'fov': 48, 'tilt': 0.5}, 'day', vm='LY2',
     cap=YEAR('1253', 'Đổi tên thành Quốc học viện'), people=['vao_cong'])
shot('hs_tam_khoi', {'from': {'pos': V(0, 4, CZ - 10), 'look': V(0, 4, CZ + 30)}, 'to': {'pos': V(0, 3, CZ + 4), 'look': V(0, 4, CZ + 30)}, 'fov': 44, 'tilt': 0.6}, 'day',
     cap=YEAR('1247', 'Trạng nguyên, bảng nhãn, thám hoa'), people=['tam_khoi'])
shot('hs_kinh_trai', {'from': {'pos': V(MPX + 1400, 1500, -500), 'look': V(MPX, 0, 1500)}, 'to': {'pos': V(MPX + 1100, 1200, 0), 'look': V(MPX, 0, 1500)}, 'fov': 46, 'tilt': 0.3, 'shadow': 2000, 'far': 12000}, 'map',
     cap=YEAR('1256', 'Kinh trạng nguyên và trại trạng nguyên'))
shot('hs_thi', {'from': {'pos': V(EX + 120, 70, -140), 'look': V(EX, 0, -10)}, 'to': {'pos': V(EX + 80, 50, -120), 'look': V(EX, 0, 0)}, 'fov': 44, 'tilt': 0.9, 'shadow': 160}, 'day', people=['thi_sinh'])
shot('hs_truong_thi', {'from': {'pos': V(EX - 40, 1.7, -40), 'look': V(EX - 20, 1.0, -10)}, 'to': {'pos': V(EX - 30, 1.7, -24), 'look': V(EX - 10, 1.0, 6)}, 'ease': 'linear', 'fov': 46, 'tilt': 0.6, 'shadow': 60}, 'day', people=['thi_sinh'])
shot('hs_so_lieu', {'orbit': {'center': V(EX, 0, 0), 'a': [200, 240], 'r': 170, 'y': [110, 130]}, 'fov': 42, 'tilt': 1.0, 'shadow': 180}, 'dusk', people=['thi_sinh'],
     cap=[{'style': 'year', 'year': '183', 'text': 'khoa thi (1075–1919)', 'at': 1.0, 'dur': 5}, {'style': 'year', 'year': '2.898', 'text': 'tiến sĩ', 'at': 6.5, 'dur': 5}])
shot('hs_vinh_quy', {'from': {'pos': V(VX + 9, 2.2, -86), 'look': V(VX, 1.6, -128)}, 'to': {'pos': V(VX + 8, 2.4, -90), 'look': V(VX, 1.6, -118)}, 'fov': 46, 'tilt': 0.55}, 'day', people=['vinh_quy'])
shot('hs_khac_bia', {'from': {'pos': V(-6, 2.0, 178), 'look': V(-11, 1.2, 172)}, 'to': {'pos': V(-7, 1.6, 176), 'look': V(-11, 1.4, 172)}, 'fov': 40, 'tilt': 0.6, 'shadow': 40}, 'day', vm=('LY2', 'LE'),
     cap=YEAR('1484', 'Vua Lê Thánh Tông cho dựng bia tiến sĩ'), people=['tho_da'], extra={'khac': True})
shot('hs_nguyen_khi', {'from': {'pos': V(-16, 1.6, 150), 'look': V(-21, 2.0, 156)}, 'to': {'pos': V(-17, 1.9, 158), 'look': V(-21, 1.9, 162)}, 'fov': 36, 'tilt': 0.8, 'shadow': 40}, 'dawn', vm='LE',
     cap=[{'style': 'title', 'text': 'Hiền tài là nguyên khí quốc gia', 'sub': 'Bia tiến sĩ khoa thi năm 1442', 'at': 2.5, 'dur': 99}])
shot('hs_vuon_bia', {'orbit': {'center': V(0, 2, 167), 'a': [-60, -10], 'r': [48, 40], 'y': [14, 9]}, 'fov': 44, 'tilt': 0.7, 'shadow': 80}, 'day', vm='LE', people=[{'crowd': {'rect': [-14, 140, 14, 196], 'count': 10, 'costume': 'scholar', 'alongZ': 0.5}}])
# 5. Nhân vật
shot('nv_le_van_thinh', {'from': {'pos': V(VX - 25.5, 1.8, -18.5), 'look': V(VX - 30.5, 0.9, -24.5)}, 'to': {'pos': V(VX - 26.6, 1.5, -20), 'look': V(VX - 30.5, 0.8, -24.5)}, 'fov': 40, 'tilt': 0.6, 'shadow': 30}, 'night', 0.5, people=['lvt_nho'],
     cap=[{'text': 'Lê Văn Thịnh', 'sub': 'Thủ khoa khoa thi đầu tiên, năm 1075', 'at': 0.5, 'dur': 8}])
shot('nv_le_van_thinh', {'from': {'pos': V(-8, 4.5, CZ + 18), 'look': V(0, 4, CZ + 40)}, 'to': {'pos': V(-4, 4.2, CZ + 24), 'look': V(0, 4, CZ + 40)}, 'fov': 42, 'tilt': 0.6}, 'day', 0.5, people=['lvt_thay'])
shot('nv_chu_van_an_truong', {'from': {'pos': V(VX - 30, 2.6, 46), 'look': V(VX - 40, 1.2, 30)}, 'to': {'pos': V(VX - 34, 2.2, 42), 'look': V(VX - 41, 1.1, 30)}, 'fov': 44, 'tilt': 0.55}, 'day', people=['cva_lang'],
     cap=[{'text': 'Chu Văn An', 'sub': 'Người thầy thời Trần', 'at': 0.5, 'dur': 7}])
shot('nv_chu_van_an_qtg', {'from': {'pos': V(10, 2.2, 296), 'look': V(0, 2.5, 306)}, 'to': {'pos': V(6, 2.0, 300), 'look': V(0, 2.5, 307)}, 'fov': 42, 'tilt': 0.55}, 'day', vm='LY2', people=['cva_day'])
shot('nv_that_tram', {'from': {'pos': V(6, 3.4, CZ + 6), 'look': V(0, 3.4, CZ + 30)}, 'to': {'pos': V(3, 3.6, CZ + 12), 'look': V(0, 3.8, CZ + 31)}, 'fov': 44, 'tilt': 0.6}, 'gray', people=['tau_vua'])
shot('nv_ve_nui', {'path': [{'pos': V(MX - 14, 0, MZ - 330), 'look': V(MX, 0, MZ - 250)}, {'pos': V(MX - 22, 0, MZ - 200), 'look': V(MX, 0, MZ - 120)}, {'pos': V(MX + 40, 0, MZ - 60), 'look': V(MX + 10, 0, MZ + 30)}], 'tilt': 0.6, 'fov': 46, 'shadow': 120, 'ground': True}, 'mist', people=['cva_nui'])
shot('nv_ten_bia', {'from': {'pos': V(-15.5, 2.0, 146), 'look': V(-21.5, 2.2, 158)}, 'to': {'pos': V(-15.5, 2.1, 182), 'look': V(-21.5, 2.2, 192)}, 'ease': 'linear', 'fov': 44, 'tilt': 0.6, 'shadow': 60}, 'day', vm='LE', extra={'tenbia': True})
# 6. Biến cố
shot('bd_le_trung_hung', {'from': {'pos': V(-4, 3, 271), 'look': V(-19, 4.5, 284)}, 'to': {'pos': V(-7, 3.6, 274), 'look': V(-19, 4.5, 284)}, 'fov': 44, 'tilt': 0.6}, 'day', vm='LE', people=['tho_sua'],
     cap=YEAR('1762', 'Sửa sang lại Quốc Tử Giám'))
shot('bd_doi_do', {'from': {'pos': V(MPX + 1900, 3000, -1400), 'look': V(MPX, 0, 600)}, 'to': {'pos': V(MPX + 1700, 2700, -3700), 'look': V(MPX + 60, 0, -1850)}, 'fov': 50, 'tilt': 0.3, 'shadow': 3000, 'far': 14000}, 'map',
     cap=YEAR('1802', 'Nhà Nguyễn đóng đô ở Phú Xuân'), extra={'route': True})
shot('bd_hoai_duc', {'from': {'pos': V(30, 18, 230), 'look': V(0, 2, 300)}, 'to': {'pos': V(20, 12, 250), 'look': V(0, 3, 305)}, 'fov': 46, 'tilt': 0.6}, 'gray', vm='LE', people=[{'crowd': {'rect': [-20, 272, 20, 298], 'count': 3, 'costume': 'scholar', 'alongZ': 0.5}}])
shot('bd_khue_van', {'orbit': {'center': V(0, 6, 135), 'look': [V(0, 6.5, 135)], 'a': [-30, 25], 'r': [52, 46], 'y': [5.5, 4.2]}, 'fov': 38, 'tilt': 0.5, 'shadow': 80}, 'dawn', vm=('LE', 'NG'),
     cap=YEAR('1805', 'Dựng Khuê Văn Các'))
shot('bd_gieng', {'from': {'pos': V(0, 2.8, 192), 'look': V(0, 4, 135)}, 'to': {'pos': V(2, 2.6, 186), 'look': V(0, 5, 135)}, 'fov': 40, 'tilt': 0.4, 'shadow': 80}, 'dusk', vm='NG')
shot('bd_khoa_cuoi', {'from': {'pos': V(EX - 100, 30, -100), 'look': V(EX, 0, 0)}, 'to': {'pos': V(EX - 140, 60, -150), 'look': V(EX, 0, 0)}, 'fov': 44, 'tilt': 0.9, 'shadow': 180}, 'dusk',
     cap=YEAR('1919', 'Khoa thi Hội cuối cùng'), extra={'leu_tan': True})
shot('bd_chien_tranh', {'from': {'pos': V(28, 10, 270), 'look': V(0, 2, 310)}, 'to': {'pos': V(20, 8, 280), 'look': V(0, 1, 312)}, 'fov': 46, 'tilt': 0.6}, 'gray', vm=('NG', 'WAR'))
shot('bd_trung_tu', {'from': {'pos': V(46, 30, 250), 'look': V(0, 2, 305)}, 'to': {'pos': V(30, 20, 262), 'look': V(0, 4, 310)}, 'fov': 46, 'tilt': 0.7, 'shadow': 120}, 'day', vm=('WAR', 'TRUNGTU'), extra={'nam_trung_tu': True})
# 7. Ngày nay
shot('kt_unesco', {'from': {'pos': V(16, 2.2, 146), 'look': V(21.5, 1.6, 160)}, 'to': {'pos': V(16, 2.4, 176), 'look': V(21.5, 1.4, 192)}, 'ease': 'linear', 'fov': 44, 'tilt': 0.7}, 'day', vm='NOW',
     cap=YEAR('2010', 'Bia tiến sĩ là Di sản tư liệu thế giới'), people=['du_khach'])
shot('kt_ho_van', {'from': {'pos': V(-40, 3, -70), 'look': V(0, 3, -48)}, 'to': {'pos': V(-30, 2.4, -66), 'look': V(0, 3, -46)}, 'fov': 42, 'tilt': 0.5, 'shadow': 80}, 'dawn', vm='NOW')
shot('kt_ngay_nay', {'from': {'pos': V(-12, 2.0, 282), 'look': V(0, 1.5, 296)}, 'to': {'pos': V(-6, 2.4, 286), 'look': V(0, 2, 300)}, 'fov': 44, 'tilt': 0.5}, 'day', vm='NOW', people=['tre_em'])
shot('kt_cau_ket', {'from': {'pos': V(40, 25, 240), 'look': V(0, 0, 175)}, 'to': {'pos': V(90, 180, 20), 'look': V(0, 0, 170)}, 'fov': 42, 'tilt': [0.6, 1.3], 'shadow': 260}, 'dusk', vm='NOW')
shot('kt_tap_sau', {'from': {'pos': V(EX - 60, 14, -80), 'look': V(EX, 0, 0)}, 'to': {'pos': V(EX - 30, 8, -60), 'look': V(EX, 0, 0)}, 'fov': 44, 'tilt': 0.9}, 'night', vm='NOW',
     cap=[{'style': 'title', 'over': 'TẬP SAU', 'text': 'Khoa cử và bia tiến sĩ', 'at': 0.5, 'dur': 99}], extra={'fadeOut': 2.0, 'leu_dem': True})

# ---------- đặt thời gian cho cảnh quay ----------
shots, stt = [], {}
by = {}
for s in SH: by.setdefault(s['canh'], []).append(s)
for canh, _ in order:
    a, b = CANH[canh]; L = b - a; acc = a
    for s in by[canh]:
        d = L * s['frac']; s['t0'], s['t1'] = acc, acc + d; acc += d
TL_ORDER = sorted(SH, key=lambda s: s['t0'])

# trạng thái Văn Miếu theo thời gian
SETS = {'NOW': NOW, 'LY0': LY0, 'LY1': LY1, 'LY2': LY2, 'LE': LE, 'NG': NG, 'WAR': (NG - {'qtg'}) | {'nen'}, 'TRUNGTU': NG | {'gian'}}
win = {}
def addwin(g, a, b, rise=0, sink=0): win.setdefault(g, []).append([round(a, 3), round(b, 3), rise, sink])
for s in TL_ORDER:
    vm = s['vm'] or 'NOW'
    if isinstance(vm, tuple):    # chuyển trạng thái giữa cảnh: nhóm mới mọc lên, nhóm mất đi lún xuống
        A, Bset = SETS[vm[0]], SETS[vm[1]]; mid = s['t0'] + (s['t1'] - s['t0']) * 0.3
        for g in A | Bset:
            if g in A and g in Bset: addwin(g, s['t0'], s['t1'])
            elif g in Bset: addwin(g, mid, s['t1'], 3.5, 0)
            else: addwin(g, s['t0'], s['t1'] - (s['t1'] - mid) * 0.4, 0, 2.5)
        if vm == ('WAR', 'TRUNGTU'):   # giàn giáo rồi nhà Thái Học dựng lại
            win.pop('gian', None); win.setdefault('gian', []).append([round(s['t0'] + 1.0, 3), round(s['t1'] - 3.0, 3), 1.5, 1.5])
            win['qtg'] = [w for w in win.get('qtg', []) if not (s['t0'] <= w[0] < s['t1'])]
            addwin('qtg', s['t1'] - 6.0, s['t1'], 3.0, 0)
    else:
        for g in SETS[vm]: addwin(g, s['t0'], s['t1'])
# nhóm luôn có ở mọi cảnh không phải Văn Miếu không quan trọng (ở xa); gộp các khoảng liền nhau
def merge(ws):
    ws = sorted(ws); out = []
    for w in ws:
        if out and abs(w[0] - out[-1][1]) < 1e-3 and w[2] == 0 and out[-1][3] == 0: out[-1][1] = w[1]; out[-1][3] = w[3]
        else: out.append(list(w))
    return out
for g, items in GRP.items():
    if g in ('walls',):
        continue
    ws = merge(win.get(g, []))
    for d in items: d['show'] = ws if ws else [[0, 0.001]]
# nhãn
def canh_win(canh, i=0, a=0.0, b=None):
    s = [x for x in TL_ORDER if x['canh'] == canh][i]; return s['t0'] + a, (s['t1'] if b is None else s['t0'] + b)
s5 = [x for x in TL_ORDER if x['canh'] == 'ht_toan_canh'][1]
for k, txt in enumerate(['Nhập đạo', 'Thành đạt', 'Vườn bia tiến sĩ', 'Đại Thành', 'Thái Học']):
    st = s5['t0'] + (s5['t1'] - s5['t0']) * (0.25 + 0.13 * k)
    for d in GRP['nhan_' + txt]: d['show'] = [[round(st, 2), round(s5['t1'] - 0.3, 2), 0, 0]]
sb = [x for x in TL_ORDER if x['canh'] == 'nv_ten_bia'][0]
for k, txt in enumerate(['Ngô Sĩ Liên', 'Lương Thế Vinh', 'Lê Quý Đôn', 'Ngô Thì Nhậm']):
    st = sb['t0'] + (sb['t1'] - sb['t0']) * (0.08 + 0.15 * k)
    for d in GRP['ten_' + txt]: d['show'] = [[round(st, 2), round(sb['t1'] - 0.2, 2), 0, 0]]
kb = [x for x in TL_ORDER if x['canh'] == 'hs_khac_bia'][0]
for d in GRP['khac']: d['show'] = [[round(kb['t0'], 2), round(kb['t1'], 2), 0, 0]]
dd = [x for x in TL_ORDER if x['canh'] == 'bd_doi_do'][0]
for d in GRP['duong']: d['grow'] = [round(dd['t0'] + 1.5, 2), round(dd['t1'] - 2.0, 2)]
for g in ('mk_tl', 'mk_px', 'mk_th'):
    ws = []
    for s in TL_ORDER:
        if s['env'] == 'map':
            if g == 'mk_px' and s['canh'] != 'bd_doi_do': continue
            if g == 'mk_th' and s['canh'] != 'hs_kinh_trai': continue
            ws.append([round(s['t0'], 2), round(s['t1'], 2), 0, 0])
    for d in GRP[g]: d['show'] = ws or [[0, 0.001]]
# lều thi: tàn dần ở cảnh 1919
lt_ws = [[0, round(TOTAL + 5, 2), 0, 0]]
kc = [x for x in TL_ORDER if x['canh'] == 'bd_khoa_cuoi'][0]
lt_ws = [[0, round(kc['t1'] - 0.5, 2), 0, 4.0], [round(kc['t1'], 2), round(TOTAL + 5, 2), 0, 0]]
for d in GRP['leu']: d['show'] = lt_ws

# ---------- người theo cảnh ----------
def vis(s): return [round(s['t0'], 2), round(s['t1'], 2)]
def add_people(s, key):
    v = vis(s); t0 = s['t0']
    if isinstance(key, dict):
        c = dict(key['crowd']); c['vis'] = v; C.append(c); return
    if key == 'thi_sinh':
        C.append({'grid': {'origin': [EX - 61.8, -42.5], 'rows': 8, 'cols': 14, 'dx': 10.0, 'dz': 11.0}, 'pose': 'write', 'costume': 'scholar', 'face': 1.5708, 'vis': v})
        C.append({'rect': [EX - 76, -56, EX + 76, 56], 'count': 8, 'costume': 'official', 'alongZ': 0.3, 'vis': v})
    elif key == 'chua':
        P.append({'pos': [VX + 40, 44.6], 'y': 0.7, 'face': 0, 'costume': 'monk', 'pose': 'teach', 'vis': v})
        C.append({'grid': {'origin': [VX + 37.2, 48.4], 'rows': 2, 'cols': 4, 'dx': 1.9, 'dz': 1.5}, 'pose': 'kneel', 'costume': 'child', 'face': 3.1416, 'vis': v})
    elif key == 'lop_lang':
        P.append({'pos': [VX - 40, 26.6], 'y': 0.4, 'face': 0, 'costume': 'teacher', 'pose': 'teach', 'vis': v})
        C.append({'grid': {'origin': [VX - 44.5, 29.15], 'rows': 2, 'cols': 4, 'dx': 2.4, 'dz': 2.3}, 'pose': 'write', 'costume': 'child', 'face': 3.1416, 'y': 0.4, 'vis': v})
    elif key in ('trieu', 'tau_vua', 'lvt_thay', 'tam_khoi'):
        P.append({'pos': [0, CZ + 32], 'y': 2.6, 'face': 3.1416, 'costume': 'king', 'pose': 'stand', 'vis': v})
        for sg in (-1, 1): C.append({'grid': {'origin': [sg * 8 - (6 if sg > 0 else 0) * 0 + (0 if sg < 0 else 0), CZ - 18], 'rows': 6, 'cols': 4, 'dx': 2.0 * sg, 'dz': 3.0}, 'pose': 'stand', 'costume': 'official', 'face': -1.5708 * sg, 'vis': v})
        if key == 'tau_vua': P.append({'pos': [0, CZ + 17.5], 'face': 0, 'costume': 'teacher', 'pose': 'bow', 'vis': v})
        if key == 'lvt_thay': P.append({'pos': [-3, CZ + 31.5], 'y': 2.6, 'face': 1.2, 'costume': 'official', 'pose': 'teach', 'vis': v}); P.append({'pos': [1.5, CZ + 31.5], 'y': 2.6, 'face': -1.9, 'costume': 'prince', 'pose': 'stand', 'vis': v, 'h': 0.82})
        if key == 'tam_khoi': C.append({'line': [[-3, CZ + 14], [3, CZ + 14]], 'count': 3, 'pose': 'bow', 'costume': 'laureate', 'face': 0, 'vis': v})
    elif key == 'le_mieu':
        C.append({'grid': {'origin': [-9, 228], 'rows': 3, 'cols': 7, 'dx': 3.0, 'dz': 2.6}, 'pose': 'bow', 'costume': 'official', 'face': 0, 'vis': v})
    elif key == 'thi_dau':
        C.append({'grid': {'origin': [-12, CZ - 30], 'rows': 4, 'cols': 9, 'dx': 3.0, 'dz': 3.0}, 'pose': 'write', 'costume': 'scholar', 'face': 0, 'vis': v})
        C.append({'line': [[-14, CZ - 14], [14, CZ - 14]], 'count': 5, 'pose': 'stand', 'costume': 'official', 'face': 3.1416, 'vis': v})
    elif key == 'doc_bang':
        C.append({'rect': [-36, CZ - 34, -24, CZ - 28], 'count': 14, 'still': True, 'pose': 'stand', 'costume': ['scholar', 'commoner'], 'face': 0.3, 'vis': v})
    elif key == 'hoang_tu':
        for i in range(4): P.append({'path': [[-1.5 + i, 266], [-1.5 + i, 300]], 'pos': [0, 266], 'once': True, 't0': t0 + 2 + i * 1.2, 'speed': 0.9, 'costume': 'prince', 'vis': v, 'h': 0.85})
        P.append({'pos': [0, 306.5], 'y': 0.9, 'face': 3.1416, 'costume': 'teacher', 'pose': 'stand', 'vis': v})
    elif key == 'vao_lop':
        for i in range(14): P.append({'path': [[-1.2 + (i % 2) * 2.4, 270], [-1.2 + (i % 2) * 2.4, 304]], 'pos': [0, 270], 'once': True, 't0': t0 + (i // 2) * 1.4, 'speed': 1.0, 'costume': 'scholar', 'vis': v})
    elif key == 'vao_cong':
        for i in range(10): P.append({'path': [[-1.5 + (i % 3) * 1.5, 250 - i * 2.4], [-1.5 + (i % 3) * 1.5, 284]], 'pos': [0, 250], 'once': True, 't0': t0, 'speed': 1.0, 'costume': 'prince' if i % 3 == 0 else 'commoner' if i % 3 == 1 else 'scholar', 'vis': v})
    elif key == 'lop_trong':
        P.append({'pos': [KX, KZ - 6.6], 'y': 1.1, 'face': 0, 'costume': 'teacher', 'pose': 'teach', 'vis': v})
        C.append({'grid': {'origin': [KX - 7.8, KZ - 2.75], 'rows': 4, 'cols': 7, 'dx': 2.6, 'dz': 2.3}, 'pose': 'write', 'costume': 'scholar', 'face': 3.1416, 'y': 0.6, 'vis': v})
    elif key == 'vinh_quy':
        path = [[VX, -140], [VX, 40]]
        for i, (role, carry) in enumerate([('commoner', 'flag'), ('commoner', 'flag'), ('laureate', None), ('commoner', 'parasol'), ('official', None), ('commoner', 'flag'), ('commoner', 'flag')]):
            P.append({'path': [[VX + (0.9 if i % 2 else -0.9) * (0 if role == 'laureate' else 1), -125 - i * 2.6], [VX + (0.9 if i % 2 else -0.9) * (0 if role == 'laureate' else 1), 40]], 'pos': [VX, -120], 'once': True, 't0': t0, 'speed': 1.0, 'costume': role, 'carry': carry, 'vis': v})
        for sg in (-1, 1): C.append({'line': [[VX + sg * 4.5, -110], [VX + sg * 4.5, -20]], 'count': 26, 'pose': 'stand', 'costume': ['commoner', 'commoner', 'child'], 'face': -1.5708 * sg, 'vis': v})
    elif key == 'tho_da':
        P.append({'pos': [-11.2, 173.1], 'face': 3.1416, 'costume': 'commoner', 'pose': 'hammer', 'carry': 'chisel', 'vis': v})
        P.append({'pos': [-12.9, 174.8], 'face': 2.4, 'costume': 'official', 'pose': 'stand', 'vis': v})
    elif key == 'lvt_nho':
        P.append({'pos': [VX - 30, -24.2], 'face': 0.6, 'costume': 'scholar', 'h': 0.8, 'pose': 'write', 'vis': v})
    elif key == 'cva_lang':
        P.append({'pos': [VX - 40, 26.6], 'y': 0.4, 'face': 0, 'costume': 'teacher', 'pose': 'teach', 'vis': v})
        C.append({'grid': {'origin': [VX - 44.5, 29.15], 'rows': 2, 'cols': 4, 'dx': 2.4, 'dz': 2.3}, 'pose': 'write', 'costume': 'scholar', 'face': 3.1416, 'y': 0.4, 'vis': v})
        C.append({'grid': {'origin': [VX - 46, 36], 'rows': 3, 'cols': 7, 'dx': 2.0, 'dz': 1.8}, 'pose': 'kneel', 'costume': 'scholar', 'face': 3.1416, 'vis': v})
    elif key == 'cva_day':
        P.append({'pos': [0, 306.0], 'y': 0.9, 'face': 3.1416, 'costume': 'teacher', 'pose': 'teach', 'vis': v})
        P.append({'pos': [0, 302.0], 'face': 0, 'costume': 'prince', 'pose': 'kneel', 'vis': v, 'h': 0.85})
        C.append({'line': [[-5, 300.5], [5, 300.5]], 'count': 6, 'pose': 'kneel', 'costume': 'scholar', 'face': 0, 'vis': v})
    elif key == 'cva_nui':
        P.append({'path': [[MX - 2, MZ - 300], [MX - 3, MZ - 200], [MX + 4, MZ - 90], [MX + 10, MZ + 20]], 'pos': [MX, MZ - 300], 'once': True, 't0': t0, 'speed': 1.0, 'costume': 'teacher', 'carry': 'staff', 'vis': v})
    elif key == 'tho_sua':
        C.append({'rect': [-26, 278, -12, 290], 'count': 6, 'still': True, 'pose': 'hammer', 'costume': 'commoner', 'vis': v})
    elif key == 'du_khach':
        C.append({'rect': [12, 140, 15, 196], 'count': 14, 'costume': ['tourist', 'tourist', 'student_girl', 'student_boy'], 'alongZ': 0.9, 'vis': v})
    elif key == 'tre_em':
        C.append({'grid': {'origin': [-6, 292], 'rows': 2, 'cols': 7, 'dx': 2.0, 'dz': 1.6}, 'pose': 'kneel', 'costume': ['student_boy', 'student_girl'], 'face': 0, 'vis': v, 'h': 0.78})
        P.append({'pos': [0, 300], 'face': 3.1416, 'costume': 'tourist', 'pose': 'teach', 'vis': v})
for s in TL_ORDER:
    for k in s['people']: add_people(s, k)
# du khách và học trò lác đác trong Văn Miếu ở các cảnh hiện tại
for s in TL_ORDER:
    if s['vm'] == 'NOW' and not s['people']:
        C.append({'rect': [-2.5, 6, 2.5, 130], 'count': 14, 'costume': ['tourist', 'student_girl', 'student_boy'], 'alongZ': 1, 'vis': vis(s)})

# ---------- chim ----------
s0 = TL_ORDER[0]
BD += [{'count': 9, 'from': [160, 70, -60], 'to': [-160, 85, 160], 't0': CANH['mo_hoi'][0], 't1': CANH['mo_hoi'][0] + 9, 'spread': 10, 'size': 1.3},
       {'count': 7, 'from': [MX - 200, 120, MZ - 300], 'to': [MX + 200, 140, MZ + 100], 't0': CANH['nv_ve_nui'][0], 't1': CANH['nv_ve_nui'][1], 'spread': 14, 'size': 1.4}]

# ---------- xuất shot ----------
out_shots = []
for i, s in enumerate(TL_ORDER):
    cam = dict(s['cam'])
    if cam.get('ground') and 'path' in cam:     # máy quay men theo địa hình núi: nâng y theo mặt đất (ước bằng tham số)
        pass
    d = {'name': f"{s['canh']}", 'dur': round(s['t1'] - s['t0'], 3), 'cam': cam, 'env': s['env']}
    if s['env2']: d['env2'] = s['env2']
    if s['cap']: d['captions'] = s['cap']
    if s['canh'] == 'mo_dem' and i == 0: d['fadeIn'] = 2.0
    if s['extra'].get('fadeOut'): d['fadeOut'] = s['extra']['fadeOut']
    if s['extra'].get('nam_trung_tu'):
        L = s['t1'] - s['t0']; d['captions'] = [{'style': 'year', 'year': y, 'text': tx, 'at': L * f, 'dur': L * 0.24} for y, tx, f in
              [('1906', 'Người Pháp xếp hạng di tích', 0.0), ('1962', 'Di tích quốc gia', 0.25), ('1994', 'Dựng lại nhà che bia', 0.5), ('1999–2000', 'Xây lại nhà Thái Học', 0.75)]]
    if s['canh'] in ('bd_le_trung_hung',):
        L = s['t1'] - s['t0']; d['captions'] = [{'style': 'year', 'year': '1762', 'text': 'Sửa sang lại Quốc Tử Giám', 'at': 0.3, 'dur': L * 0.4}, {'style': 'year', 'year': '1785', 'text': 'Đổi tên thành nhà Thái Học', 'at': L * 0.42, 'dur': L * 0.3},
                                                    {'style': 'year', 'year': '1768', 'text': 'Chuông Bích Ung được đúc', 'at': L * 0.74, 'dur': L * 0.25}]
    if s['canh'] == 'bd_hoai_duc':
        d['captions'] = YEAR('1805', 'Học đường phủ Hoài Đức')
    out_shots.append(d)

# máy quay đường núi: tính độ cao theo địa hình trong JS bằng 'yOff' (engine cộng groundH)
spec = {'engine': 'arch3d.js', 'size': [1920, 1080], 'fps': 30, 'seed': 1076,
        'world': {'chatLieu': 'chat_lieu/', 'hdri': {'ngay': 'chat_lieu/troi_ngay.hdr', 'chieu': 'chat_lieu/troi_chieu.hdr'}, 'groundMat': 'grass', 'sun': [-0.55, 0.42, -0.3], 'haze': [0.8, 0.74, 0.64], 'fog': 0.0012, 'sunPower': 3.2, 'skyTop': [0.24, 0.4, 0.66], 'clouds': 16},
        'quality': {'shadow': 2048, 'reflScale': 0.4, 'bloom': 0.5, 'grade': 1.0}, 'props': PR,
        'terrains': TER, 'ground': G, 'buildings': B, 'trees': T, 'houses': HS, 'crowds': C, 'people': P, 'birds': BD, 'lanterns': LT,
        'shots': out_shots, 'subs': subs,
        'audio': {'ambience': {'wind': 0.2, 'water': 0.08, 'birds': 0.35},
                  'music': {'style': 'pentatonic', 'gain': [[0, 0], [2, 0.55], [TOTAL - 4, 0.55], [TOTAL, 0]]},
                  'voice': {'dir': 'giong/qtg1/leda/chuan', 'items': voice_items, 'gain': 1.0, 'duck': 0.6},
                  'cues': [{'at': 0.4, 'type': 'bell', 'gain': 0.5}] + [{'at': round(CANH[c][0] + 0.2, 2), 'type': 'bell', 'gain': 0.35} for c in CHAP_START if c != 'mo_dem']}}
OUT = os.path.join(HERE, '..', 'specs', 'qtg1.json')
json.dump(spec, open(OUT, 'w'), ensure_ascii=False)
print(f'{len(out_shots)} cảnh quay, tổng {TOTAL / 60:.2f} phút, {len(subs)} phụ đề; người: {len(P)} + {len(C)} nhóm')
