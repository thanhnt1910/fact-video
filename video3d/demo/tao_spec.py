#!/usr/bin/env python3
"""Spec đoạn demo 3D «Khoa thi năm 1442» (khoảng 80 giây) — hướng dựng mới: kể theo hành trình,
cắt cảnh nhanh, cận cảnh, mực loang, tua thời gian, bia tự khắc chữ.
  python3 demo/tao_spec.py [thư mục giọng/chuan]   -> specs/demo1442.json
Dùng lại toàn bộ bối cảnh của Tập 1 (qtg/tao_spec.py, phần dựng thế giới)."""
import json, os, random, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
# --- dựng thế giới: chạy phần đầu qtg/tao_spec.py (đến trước phần trạng thái theo cảnh) ---
src = open(os.path.join(ROOT, 'qtg', 'tao_spec.py'), encoding='utf-8').read()
W = {'__file__': os.path.join(ROOT, 'qtg', 'tao_spec.py'), '__name__': 'qtg_world'}
argv0 = sys.argv; sys.argv = [argv0[0]]
exec(compile(src[:src.index('# ---------- trạng thái các nhóm')], 'qtg_world', 'exec'), W)
sys.argv = argv0
B, GRP, TER, G, T, HS, LT, PR = W['B'], W['GRP'], W['TER'], W['G'], W['T'], W['HS'], W['LT'], W['PR']
CZ, EX, MPX, TL, LL, LLs, KX, KZ = W['CZ'], W['EX'], W['MPX'], W['TL'], W['LL'], W['LLs'], W['KX'], W['KZ']

# --- thời gian theo giọng ---
segs = json.load(open(os.path.join(HERE, 'loi_doc.json'), encoding='utf-8'))
VOICE = sys.argv[1] if len(sys.argv) > 1 else None
dur = json.load(open(os.path.join(VOICE, 'thoi_luong.json'))) if VOICE else {}
def tieng(t): return len(re.findall(r"[\wÀ-ỹ]+", t))
LEAD = {'muc': 3.2, 'thi': 0.5, 'thoi_gian': 0.3, 'khac': 0.6, 'nay': 0.4}
TAIL = {'thi': 2.2, 'san_rong': 0.6, 'thoi_gian': 1.2, 'nay': 4.0}
t = 0.0; SEG = {}; voice_items = []; subs = []
for s in segs:
    t0 = t; t += LEAD.get(s['canh'], 0.35); d = dur.get(str(s['n']), tieng(s['text']) / 3.3)
    voice_items.append({'n': s['n'], 'at': round(t, 3)}); subs.append({'t0': round(t, 2), 't1': round(t + d, 2), 'text': s['text']})
    t += d + TAIL.get(s['canh'], 0.35); SEG[s['canh']] = (round(t0, 3), round(t, 3))
TOTAL = round(t, 3)

def V(*a): return list(a)
shots = []
def shot(name, dur_, cam, env='day', **k): shots.append({'name': name, 'dur': round(dur_, 3), 'cam': cam, 'env': env, **k})
def span(c): return SEG[c][1] - SEG[c][0]

# ===== 1. Giọt mực loang thành sa bàn; dòng sáng (sĩ tử) đổ về Thăng Long =====
d = span('muc')
shot('muc', d, {'from': {'pos': V(MPX + 1500, 9500, -5200), 'look': V(MPX + 900, 0, 900)}, 'to': {'pos': V(TL[0] + 260, 900, TL[1] - 1100), 'look': V(TL[0], 0, TL[1])},
               'fov': 44, 'tilt': [0.0, 0.5], 'far': 30000, 'near': 60, 'ease': 'inout'}, 'map',
     ink=[{'at': 0.25, 'dur': 3.2, 'kind': 'reveal', 'c': [0.47, 0.42], 'pow': 1.8}])
# ===== 2. Bình minh ở cổng kinh thành: dòng người áo dài tiến vào, máy quay thấp sát đất =====
d = span('cong')
shot('cong_a', d * 0.55, {'from': {'pos': V(3.5, 0.45, CZ - 196), 'look': V(0, 3.5, CZ - 150)}, 'to': {'pos': V(2.0, 0.55, CZ - 186), 'look': V(0, 4.2, CZ - 150)}, 'fov': 38, 'tilt': 0.3, 'shadow': 60, 'dof': {'aperture': 0.0016, 'maxblur': 0.008}}, 'dawn')
shot('cong_b', d * 0.45, {'from': {'pos': V(-30, 36, CZ - 230), 'look': V(0, 0, CZ - 160)}, 'to': {'pos': V(-18, 30, CZ - 214), 'look': V(0, 0, CZ - 150)}, 'fov': 44, 'tilt': 0.9, 'shadow': 120}, 'dawn')
# ===== 3. Trường thi: tua nhanh bốn ngày, sĩ tử vơi dần từ 450 còn 33 =====
d = span('thi')
shot('thi', d, {'from': {'pos': V(EX - 72, 9, -62), 'look': V(EX - 30, 0, -20)}, 'to': {'pos': V(EX - 60, 30, -80), 'look': V(EX - 10, 0, -5)}, 'fov': 46, 'tilt': 1.0, 'shadow': 120, 'ease': 'linear'}, 'day',
     sunCycle=4, captions=[{'style': 'year', 'count': [450, 33], 'text': 'sĩ tử còn lại sau bốn vòng thi', 'at': 0.2, 'dur': d - 0.4}])
# ===== 4. Sân rồng: 33 người quỳ làm bài; cận cảnh ngòi bút =====
d = span('san_rong')
shot('san_rong_a', d * 0.5, {'from': {'pos': V(0, 0.9, CZ - 4), 'look': V(0, 3.2, CZ + 30)}, 'to': {'pos': V(0, 3.6, CZ - 1), 'look': V(0, 4.0, CZ + 30)}, 'fov': 40, 'tilt': 0.4, 'shadow': 50}, 'day')
shot('san_rong_b', d * 0.5, {'from': {'pos': V(0.32, 0.72, CZ + 6.05), 'look': V(0.02, 0.36, CZ + 6.55)}, 'to': {'pos': V(0.22, 0.66, CZ + 6.15), 'look': V(0.0, 0.36, CZ + 6.6)},
                             'fov': 40, 'tilt': 0.0, 'near': 0.02, 'shadow': 4, 'dof': {'aperture': 0.012, 'maxblur': 0.012}}, 'day')
# ===== 5. Đêm chấm bài: người chấm già bên đèn dầu, chồng quyển thi =====
GX = 5200
d = span('cham')
shot('cham', d, {'from': {'pos': V(GX + 2.6, 1.25, 3.2), 'look': V(GX, 0.9, 0)}, 'to': {'pos': V(GX + 1.5, 1.1, 2.0), 'look': V(GX, 0.85, 0)}, 'fov': 38, 'tilt': 0.3, 'near': 0.05, 'shadow': 8,
                 'dof': {'aperture': 0.006, 'maxblur': 0.01}}, 'night')
# ===== 6. Bảng vàng mở ra trên tường thành; đám đông; trống =====
d = span('bang')
shot('bang_a', d * 0.45, {'from': {'pos': V(-6, 1.7, CZ - 172), 'look': V(-20, 3.0, CZ - 151)}, 'to': {'pos': V(-9, 1.7, CZ - 168), 'look': V(-20, 3.4, CZ - 151)}, 'fov': 42, 'tilt': 0.3, 'shadow': 40,
                           'dof': {'focus': 6.0, 'aperture': 0.004, 'maxblur': 0.01}}, 'day')
shot('bang_b', d * 0.55, {'from': {'pos': V(-19.0, 3.3, CZ - 156.5), 'look': V(-19.6, 3.3, CZ - 151)}, 'to': {'pos': V(-18.9, 3.6, CZ - 155.2), 'look': V(-18.9, 3.6, CZ - 151)}, 'fov': 36, 'tilt': 0.2, 'near': 0.1, 'shadow': 20}, 'day')
# ===== 7. Bốn mươi hai năm: cùng góc máy, ngày đêm vụt qua, bảng vàng phai, năm đếm lên =====
d = span('thoi_gian')
shot('thoi_gian', d, {'from': {'pos': V(-4, 2.2, CZ - 178), 'look': V(-14, 3.0, CZ - 151)}, 'to': {'pos': V(-5, 2.6, CZ - 180), 'look': V(-14, 3.2, CZ - 151)}, 'fov': 46, 'tilt': 0.4, 'shadow': 60, 'ease': 'linear'}, 'day',
     sunCycle=9, captions=[{'style': 'year', 'count': [1442, 1484], 'text': 'bốn mươi hai năm', 'at': 0.2, 'dur': d - 0.3}])
# ===== 8. Văn Miếu năm 1484: bia và rùa đá nhô lên, thợ đục đá =====
d = span('khac')
shot('khac', d, {'from': {'pos': V(-9.0, 0.7, 147.0), 'look': V(-15, 2.0, 150)}, 'to': {'pos': V(-10.0, 1.1, 152.4), 'look': V(-15, 2.1, 150)}, 'fov': 42, 'tilt': 0.3, 'shadow': 20,
                 'dof': {'aperture': 0.003, 'maxblur': 0.01}}, 'day')
# ===== 9. Chữ tự khắc trên mặt bia, ánh vàng rồi lặn vào đá =====
d = span('chu')
shot('chu', d, {'from': {'pos': V(-12.6, 1.95, 150.4), 'look': V(-14.9, 1.9, 150.0)}, 'to': {'pos': V(-13.2, 1.95, 150.2), 'look': V(-14.9, 1.95, 150.0)}, 'fov': 40, 'tilt': 0.0, 'near': 0.05, 'shadow': 6}, 'day')
# ===== 10. Tên Nguyễn Trực =====
d = span('ten')
shot('ten', d, {'from': {'pos': V(-14.05, 2.2, 150.3), 'look': V(-14.9, 2.2, 150.22)}, 'to': {'pos': V(-14.3, 2.2, 150.25), 'look': V(-14.9, 2.2, 150.22)}, 'fov': 34, 'tilt': 0.0, 'near': 0.02, 'shadow': 4,
                'dof': {'aperture': 0.01, 'maxblur': 0.012}}, 'day')
# ===== 11. Kéo lùi qua năm thế kỷ: 82 bia mọc lên, nhà bia, du khách hôm nay; mực phủ kín, hết =====
d = span('nay')
shot('nay', d, {'from': {'pos': V(-12.0, 1.8, 150.6), 'look': V(-15, 2.0, 150)}, 'to': {'pos': V(30, 42, 118), 'look': V(-10, 0, 168)}, 'fov': 44, 'tilt': [0.3, 1.0], 'shadow': 90, 'ease': 'in'}, 'day', env2='dusk',
     ink=[{'at': d - 2.2, 'dur': 1.8, 'kind': 'cover', 'c': [0.5, 0.5], 'pow': 1.4}], fadeOut=0.6)

# căn tổng thời lượng cảnh đúng bằng lời
acc = 0
for s in shots: s['t0'] = round(acc, 3); acc += s['dur']
shots[-1]['dur'] = round(shots[-1]['dur'] + TOTAL - acc, 3)
T0 = {s['name']: s['t0'] for s in shots}
def win(name, a=0, b=None): s = next(x for x in shots if x['name'] == name); return [round(s['t0'] + a, 2), round(s['t0'] + (b if b is not None else s['dur']), 2)]

# ===== trạng thái công trình Văn Miếu: thời Lê (1484) rồi ngày nay =====
t_nay = T0['nay']
for grp, items in GRP.items():
    for b in items:
        if grp in ('bia', 'nhabia'): b['show'] = [[round(t_nay + (0.8 if grp == 'bia' else 2.2), 2), 9999, 2.0, 0]]
        elif grp in ('kvc', 'gieng', 'leu'): b['show'] = [[round(t_nay + 3.0, 2), 9999, 1.5, 0]] if grp != 'leu' else [[0, 0.001]]
        elif grp == 'duong': b['show'] = [[0, 0.001]]
        else: b.pop('show', None)
for b in B:
    if b.get('type') == 'board': b['show'] = [[0, 0.001]]
    if b.get('type') == 'label' and b['pos'][0] < 10000: b['show'] = [[0, 0.001]]   # nhãn tên trong Văn Miếu của Tập 1

# ===== đạo cụ mới =====
VIET = '*' * 14
B.append({'type': 'flow', 'win': [round(T0['muc'] + 2.6, 2), round(T0['muc'] + shots[0]['dur'], 2)], 'hide': round(T0['muc'] + shots[0]['dur'], 2), 'n': 10, 'size': 14, 'lift': 25,
          'paths': [LLs(p) for p in [[(16.47, 107.58), (17.5, 106.5), (18.7, 105.7), (19.8, 105.78), (20.4, 105.75), (21.03, 105.85)],
                                     [(19.8, 105.78), (20.5, 105.8), (21.03, 105.85)], [(22.3, 105.6), (21.6, 105.7), (21.03, 105.85)], [(21.3, 106.6), (21.1, 106.2), (21.03, 105.85)],
                                     [(20.9, 107.1), (21.0, 106.5), (21.03, 105.85)], [(18.3, 105.9), (19.0, 105.6), (19.8, 105.78), (20.6, 105.8), (21.03, 105.85)],
                                     [(21.5, 104.9), (21.3, 105.4), (21.03, 105.85)], [(20.5, 106.3), (20.8, 106.0), (21.03, 105.85)]]]})
# bàn và quyển thi ở sân rồng (cận cảnh ngòi bút)
B.append({'type': 'box', 'pos': [0.0, CZ + 6.6], 'size': [1.0, 0.34, 0.5], 'mat': 'darkwood'})
B.append({'type': 'paper', 'pos': [0.0, CZ + 6.6], 'w': 0.42, 'h': 0.3, 'y': 0.345, 'px': 640, 'cols': ['*' * 9] * 10,
          'reveal': [round(T0['san_rong_b'] - 0.5, 2), round(T0['san_rong_b'] + shots[[s['name'] for s in shots].index('san_rong_b')]['dur'] + 3, 2)], 'brush': True, 'sleeve': 0x26344f})
# bàn chấm bài ban đêm: chồng quyển, đèn dầu
B.append({'type': 'box', 'pos': [GX, 0], 'size': [1.6, 0.5, 0.8], 'mat': 'darkwood'})
B.append({'type': 'paper', 'pos': [GX + 0.05, 0.02], 'w': 0.5, 'h': 0.36, 'y': 0.505, 'px': 640, 'cols': ['*' * 10] * 12})
for k in range(7): B.append({'type': 'box', 'pos': [GX - 0.55, 0.505 + k * 0.012, -0.1], 'size': [0.4, 0.011, 0.3], 'mat': 'plaster'})
B.append({'type': 'hall', 'pos': [GX, 1.0], 'w': 9, 'd': 7, 'colH': 3.2, 'walls': 'back', 'roofH': 2.6, 'base': 0.0, 'steps': False})
LT.append({'points': [[GX - 1.7, 2.3, -0.9], [GX - 3.2, 2.6, 2.6], [GX + 3.2, 2.6, 2.6]]})
# bảng vàng trên tường thành
B.append({'type': 'banner', 'pos': [-19.6, CZ - 151.0], 'rot': 180, 'top': 5.0, 'w': 3.0, 'h': 4.0, 'px': 600,
          'cols': ['大寶三年壬戌科', '第一甲進士及第', '阮直', '阮如堵', '梁如鵠', '第二甲', VIET[:9], VIET[:9], VIET[:9], VIET[:9]], 'bigCols': [2],
          'show': [[round(T0['bang_a'] + 0.3, 2), round(T0['thoi_gian'] + shots[[s['name'] for s in shots].index('thoi_gian')]['dur'] * 0.7, 2), 1.4, 1.2]]})
# bia tiến sĩ đầu tiên trên lưng rùa (mọc lên ở cảnh khắc, chữ tự khắc ở cảnh "chu" và "ten")
r0 = T0['chu']; r1 = T0['ten'] + 0.6
B.append({'type': 'bia', 'pos': [-15.0, 150.0], 'rot': 90, 'w': 1.15, 'h': 1.7, 'glow': 0.9,
          'cols': ['大寶三年壬戌科進士題名記', VIET, VIET, VIET, VIET, VIET, VIET, '第一甲進士及第三名', '阮直', '阮如堵', '梁如鵠'], 'bigCols': [0, 8],
          'reveal': [round(r0 + 0.2, 2), round(r1, 2)], 'show': [[round(T0['khac'] + 0.2, 2), 9999, 2.6, 0]]})

# ===== người =====
P, C = [], []
def vis_of(name, a=0, b=None): return [win(name, a, b)]
rng = random.Random(1442)
# dòng sĩ tử vào cổng kinh thành
for i in range(36):
    x = rng.uniform(-5.0, 5.0); z0 = CZ - 193.5 + i * 0.95
    P.append({'path': [[x, z0], [x * 0.6, CZ - 150]], 'pos': [x, z0], 'once': True, 't0': round(T0['cong_a'] - 1.5, 2), 'speed': rng.uniform(1.0, 1.3), 'costume': 'scholar',
              'carry': 'staff' if i % 5 == 0 else None, 'vis': vis_of('cong_a') + vis_of('cong_b')})
# 450 sĩ tử ở trường thi, vơi dần còn 33
ts = win('thi'); idx = list(range(450)); rng.shuffle(idx); keep = set(idx[:33])
for k in range(450):
    r, c = divmod(k, 30); end = ts[1] if k in keep else round(ts[0] + 0.6 + (ts[1] - ts[0] - 1.8) * (0.25 + 0.75 * rng.random()) ** 0.9, 2)
    P.append({'pos': [EX - 65 + c * 4.5 + rng.uniform(-0.3, 0.3), -48 + r * 6.2 + rng.uniform(-0.3, 0.3)], 'face': 0, 'costume': 'scholar', 'pose': 'write', 'vis': [[ts[0], end]]})
B.append({'type': 'desks', 'origin': [EX - 65, -47.4], 'rows': 15, 'cols': 30, 'dx': 4.5, 'dz': 6.2, 'y': 0.0, 'rot': 0, 'show': [ts]})
# sân rồng: 33 người quỳ làm bài, quan đứng hai bên, vua trên điện
vs = vis_of('san_rong_a') + vis_of('san_rong_b')
for k in range(33):
    r, c = divmod(k, 11)
    if (r, c) == (0, 5): continue
    P.append({'pos': [-12.5 + c * 2.5, CZ + 6.6 + r * 2.6 + (0 if r else 0)], 'face': 0, 'costume': 'scholar', 'pose': 'write', 'vis': vs})
P.append({'pos': [0.0, CZ + 6.15], 'face': 0, 'costume': 'scholar', 'pose': 'write', 'vis': vis_of('san_rong_a')})
B.append({'type': 'desks', 'origin': [-12.5, CZ + 7.0], 'rows': 3, 'cols': 11, 'dx': 2.5, 'dz': 2.6, 'y': 0.0, 'rot': 0, 'show': [vs[0][:1] + [vs[1][1]]]})
C.append({'line': [[-18, CZ + 2], [-18, CZ + 18]], 'count': 7, 'costume': 'official', 'pose': 'stand', 'face': 1.5708, 'vis': vs})
C.append({'line': [[18, CZ + 2], [18, CZ + 18]], 'count': 7, 'costume': 'official', 'pose': 'stand', 'face': -1.5708, 'vis': vs})
P.append({'pos': [0, CZ + 32], 'y': 2.6, 'face': 3.1416, 'costume': 'king', 'pose': 'stand', 'vis': vs})
# người chấm bài: già, râu trắng, ngồi đọc bên đèn
P.append({'pos': [GX, -0.62], 'face': 0, 'costume': 'teacher', 'pose': 'write', 'robe': [0.36, 0.1, 0.1], 'hat': 'quan', 'vis': vis_of('cham')})
# đám đông xem bảng vàng
vb = vis_of('bang_a') + vis_of('bang_b')
C.append({'rect': [-26, CZ - 166, -12, CZ - 155], 'count': 34, 'costume': ['scholar', 'commoner', 'scholar', 'commoner', 'official'], 'still': True, 'pose': 'stand', 'face': 3.1416, 'vis': vb})
for i in range(4): P.append({'path': [[-4 - i * 1.5, CZ - 175], [-14 - i, CZ - 160]], 'pos': [-4, CZ - 175], 'once': True, 't0': round(T0['bang_a'], 2), 'speed': 1.2, 'costume': 'scholar', 'vis': vb})
# thợ đục bia năm 1484
vk = vis_of('khac') + vis_of('chu')
P.append({'pos': [-14.0, 151.6], 'face': -2.4, 'costume': 'commoner', 'pose': 'hammer', 'carry': 'chisel', 'vis': vk})
P.append({'pos': [-14.2, 148.3], 'face': -0.8, 'costume': 'commoner', 'pose': 'hammer', 'carry': 'chisel', 'vis': vis_of('khac')})
P.append({'pos': [-11.5, 149.0], 'face': -1.4, 'costume': 'official', 'pose': 'stand', 'vis': vis_of('khac')})
# du khách hôm nay
C.append({'rect': [-10, 140, 10, 196], 'count': 26, 'costume': ['tourist', 'student_girl', 'tourist', 'student_boy'], 'alongZ': 0.7, 'vis': [win('nay', 2.5)]})

spec = {'engine': 'arch3d.js', 'size': [1920, 1080], 'fps': 30, 'seed': 1442,
        'world': {'chatLieu': 'chat_lieu/', 'hdri': {'ngay': 'chat_lieu/troi_ngay.hdr', 'chieu': 'chat_lieu/troi_chieu.hdr'}, 'logDepth': False, 'groundMat': 'grass',
                  'sun': [-0.55, 0.42, -0.3], 'haze': [0.8, 0.74, 0.64], 'fog': 0.0012, 'sunPower': 3.2, 'skyTop': [0.24, 0.4, 0.66]},
        'quality': {'shadow': 2048, 'reflScale': 0.4, 'bloom': 0.5, 'grade': 1.0, 'dof': True}, 'props': PR,
        'terrains': TER, 'ground': G, 'buildings': B, 'trees': T, 'houses': HS, 'crowds': C, 'people': P, 'birds': [], 'lanterns': LT,
        'shots': shots, 'subs': subs,
        'audio': {'ambience': {'wind': 0.18, 'birds': 0.25},
                  'music': {'style': 'pentatonic', 'gain': [[0, 0], [3, 0.5], [TOTAL - 3, 0.6], [TOTAL, 0]]},
                  'voice': {'dir': 'giong/demo1442/leda/chuan', 'items': voice_items, 'gain': 1.0, 'duck': 0.6},
                  'cues': [{'at': round(T0['muc'] + 0.25, 2), 'type': 'ink', 'gain': 0.9}, {'at': round(T0['muc'] + 2.6, 2), 'type': 'whoosh', 'dur': 2.5, 'gain': 0.5},
                           {'at': round(T0['cong_a'] + 0.2, 2), 'type': 'crowd', 'dur': span('cong'), 'gain': 0.5},
                           *[{'at': round(T0['thi'] + k * span('thi') / 4, 2), 'type': 'taiko', 'gain': 0.55} for k in range(4)],
                           *[{'at': round(T0['san_rong_b'] + 0.15 + k * 0.62, 2), 'type': 'brush', 'dur': 0.5, 'gain': 0.9} for k in range(int(span('san_rong') * 0.5 / 0.62))],
                           {'at': round(T0['bang_a'] + 0.2, 2), 'type': 'taiko', 'gain': 0.8}, {'at': round(T0['bang_a'] + 0.5, 2), 'type': 'crowd', 'dur': span('bang'), 'gain': 0.7},
                           {'at': round(T0['thoi_gian'] + 0.1, 2), 'type': 'whoosh', 'dur': span('thoi_gian'), 'gain': 0.45},
                           *[{'at': round(T0['khac'] + 0.6 + k * 1.2, 2), 'type': 'chisel', 'k': 3, 'gain': 0.8} for k in range(int(span('khac') / 1.2))],
                           *[{'at': round(T0['chu'] + 0.3 + k * 0.9, 2), 'type': 'chisel', 'k': 2, 'gain': 0.45} for k in range(int((span('chu') + span('ten')) / 0.9))],
                           {'at': round(T0['nay'] + 0.3, 2), 'type': 'bell', 'gain': 0.6}, {'at': round(TOTAL - 2.3, 2), 'type': 'ink', 'gain': 0.7}]}}
OUT = os.path.join(ROOT, 'specs', 'demo1442.json')
json.dump(spec, open(OUT, 'w'), ensure_ascii=False)
print(f'{len(shots)} cảnh, {TOTAL:.1f} giây, {len(P)} người + {len(C)} nhóm')
