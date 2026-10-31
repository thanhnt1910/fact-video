"""Thử bộ kiểm quy chuẩn ảnh bằng các trường hợp mẫu (không gọi mạng, không vẽ ảnh).  python phim_ban_do/test_kiem_anh.py"""
import copy, hashlib, json, os, sys
sys.argv = ['x', 'lt1v4']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kiem_scene_planner as K, anh_quy_tac as Q
KP = K.KP; S = KP['STYLE']['text']; A = KP['ANATOMY']['text']; CUR = K.CUR
def cau(prompt, **kw):
    d = dict(scene_id='T', segment_ids=[1], scene_type='army', expected_people=3, expected_horses=0, main_characters=['lính Đại Việt'],
             positions='ba lính đứng trước cổng', groups=[dict(name='lính', count=3, position='tiền cảnh', role='gác', horses=0, mounted=0)],
             composition='x', camera='wide', lighting='dawn', blocks_used=['VN_AO_VAI', 'VN_DAU'],
             detail_tags=[dict(item='áo', block='VN_AO_VAI', tag='artistic_choice', evidence_level='C', bible_ref='period-ly-tong#C Quần áo lính'),
                          dict(item='tóc', block='VN_DAU', tag='artistic_choice', evidence_level='C', bible_ref='period-ly-tong#C Mũ')],
             free_text_details=[], image_prompt=prompt, prompt_version='p1', bible_versions=dict(CUR), plan_status='PLAN_DRAFT', reference_images=[])
    d.update(kw); d['prompt_sha256'] = hashlib.sha256(d['image_prompt'].encode()).hexdigest(); return d
P0 = f"Three soldiers at a gate. {KP['VN_AO_VAI']['text']}, bare heads with black hair tied in a topknot. {A} {S}"
def chay(s):
    K.bad.clear(); K.warn.clear(); K.kiem_canh(s); return list(K.bad)
kq = []
def thu(ten, cho_loi, s=None, ky_vong=None, anh=None, w=False):
    if False and w and anh is None and cho_loi is True:   # (đã gỡ 01/11/2026: chủ kênh duyệt mục 5 nên 26 quy tắc mới chặn như quy tắc cũ; tham số w giữ để tương thích)
        K.bad.clear(); K.warn.clear(); K.kiem_canh(s)
        okw = any(ky_vong in l and 'quy tắc chưa duyệt' in l for l in K.warn) and not any(ky_vong in l for l in K.bad); kq.append(okw)
        print(('PASS ' if okw else 'FAIL ') + ten + ' [cảnh báo, không chặn]' + ('' if okw else f'  -> warn={K.warn[:2]} bad={K.bad[:2]}')); return
    if anh is None: loi = chay(s)
    else:
        K.bad.clear(); K.warn.clear(); K.kiem_anh(anh, [s] if s else []); loi = list(K.bad)
    dat = (not loi) if cho_loi is False else any(ky_vong in l for l in loi)
    kq.append(dat); print(('PASS ' if dat else 'FAIL ') + ten + ('' if dat else f'   [{ky_vong}] -> {loi}'))
    if cho_loi is True and dat: print('      ↳ ' + [l for l in loi if ky_vong in l][0][:170])
# --- cảnh
base = cau(P0)
thu('1 Cảnh hợp lệ không có lỗi', False, base)
# số ngựa
H = f"Three riders. EXACTLY three horses with three riders, each rider upright on exactly one horse. {A} {S}"
hg = lambda h, m: [dict(name='kỵ binh', count=3, position='tiền cảnh', role='cưỡi', horses=h, mounted=m)]
thu('2a Cảnh 3 ngựa hợp lệ', False, cau(H, expected_horses=3, groups=hg(3, 3), blocks_used=[], detail_tags=[]))
thu('2b Số ngựa các nhóm (2) khác expected_horses (3)', True, cau(H, expected_horses=3, groups=hg(2, 2), blocks_used=[], detail_tags=[]), 'tổng horses')
thu('2c Prompt ghi EXACTLY two horses, kế hoạch 3', True, cau(H.replace('three horses', 'two horses'), expected_horses=3, groups=hg(3, 3), blocks_used=[], detail_tags=[]), 'EXACTLY two')
thu('2d expected_horses=0 nhưng prompt nhắc kỵ binh', True, cau(P0 + ' cavalry'), 'nhắc ngựa')
thu('2e Mỗi kỵ binh một ngựa: mounted 2, horses 3', True, cau(H, expected_horses=3, groups=hg(3, 2), blocks_used=[], detail_tags=[]), 'mỗi kỵ binh một ngựa')
thu('2f expected_horses=3 nhưng prompt thiếu "EXACTLY N horses"', True, cau(f"Three riders on horses. {A} {S}", expected_horses=3, groups=hg(3, 3), blocks_used=[], detail_tags=[]), 'không có "EXACTLY')
# detail_tags
b = copy.deepcopy(base); del b['detail_tags']
thu('3a Thiếu hẳn trường detail_tags', True, b, 'thiếu trường detail_tags')
thu('3b detail_tags rỗng nhưng có khối mức C', True, cau(P0, detail_tags=[]), 'chưa có trong detail_tags')
t = copy.deepcopy(base['detail_tags']); t[0]['bible_ref'] = 'period-ly-tong#C Mũ nón thần kỳ'
thu('4a bible_ref: hạng mục không tồn tại trong Bible', True, cau(P0, detail_tags=t), 'không tồn tại')
t = copy.deepcopy(base['detail_tags']); t[0]['bible_ref'] = 'period-khong-co#C Mũ'
thu('4b bible_ref: file không tồn tại', True, cau(P0, detail_tags=t), 'không tồn tại')
t = copy.deepcopy(base['detail_tags']); t[0]['bible_ref'] = 'period-ly-tong#Z Mũ'
thu('4c bible_ref: mục Z không tồn tại', True, cau(P0, detail_tags=t), 'không tồn tại')
t = copy.deepcopy(base['detail_tags']); t[0]['evidence_level'] = 'B'
thu('5a Đổi evidence_level (C → B)', True, cau(P0, detail_tags=t), 'không được gộp hay đổi mức')
t = copy.deepcopy(base['detail_tags']); t[0]['tag'] = 'historical_evidence'; t[0]['evidence_level'] = 'A'
thu('5b Nâng nhãn artistic_choice lên historical_evidence', True, cau(P0, detail_tags=t), 'mạnh hơn nhãn')
# nhóm và tổng
thu('6a Thiếu groups', True, cau(P0, groups=[]), 'groups rỗng')
thu('6b Tổng số người các nhóm không khớp', True, cau(P0, groups=[dict(name='lính', count=2, position='tiền cảnh', role='gác', horses=0, mounted=0)]), 'tổng count')
g = cau(P0); del g['groups']
thu('6c Thiếu hẳn trường groups', True, g, 'thiếu trường groups')
# tham chiếu
for rid in ('19901', 'lt1v4-test-01', 'lt1v4-test-12'):
    thu(f'7 Ảnh cũ {rid} làm tham chiếu', True, cau(P0, reference_images=[dict(image_id=rid, purpose='costume_only')]), 'không hợp lệ')
# --- sổ ảnh
def rec(i, sid, att, st, dem=(3, 0), kh=(3, 0), **k):
    r = dict(image_id=i, scene_id=sid, attempt=att, status=st, bible_versions=dict(CUR), prompt_sha256='x',
             dem_thu_cong=dict(nguoi=dem[0], ngua=dem[1], nguoi_dem='chủ kênh', ngay='2026-11-02') if dem else None,
             ke_hoach=dict(nguoi=kh[0], ngua=kh[1]) if kh else None); r.update(k); return r
thu('8a Sổ ảnh hợp lệ (PASS, số đếm khớp)', False, anh=[rec('a1', 1, 1, 'PASS')])
thu('8b PASS nhưng số người thực tế khác dự kiến', True, anh=[rec('a1', 1, 1, 'PASS', dem=(2, 0))], ky_vong='khác dự kiến')
thu('8c Số ngựa thực tế khác dự kiến vẫn PASS', True, anh=[rec('a1', 1, 1, 'PASS', dem=(3, 2), kh=(3, 3))], ky_vong='khác dự kiến')
thu('8d Thiếu dem_thu_cong', True, anh=[rec('a1', 1, 1, 'REVIEW', dem=None)], ky_vong='thiếu dem_thu_cong')
thu('8e Thiếu ke_hoach (không có bản chụp số dự kiến)', True, anh=[rec('a1', 1, 1, 'REVIEW', kh=None)], ky_vong='thiếu ke_hoach')
thu('9a attempt 4 chưa PASS mà vẫn REGENERATE', True, anh=[rec('a1', 1, 4, 'REGENERATE')], ky_vong='phải là MANUAL_REVIEW')
thu('9b attempt 5 (vượt 1 + 3 lần vẽ lại)', True, anh=[rec('a4', 1, 4, 'MANUAL_REVIEW'), rec('a5', 1, 5, 'REGENERATE')], ky_vong='vượt')
thu('9c Vẽ tiếp sau MANUAL_REVIEW chưa có owner_unlock', True, anh=[rec('a3', 1, 3, 'MANUAL_REVIEW'), rec('a4', 1, 4, 'REVIEW')], ky_vong='MANUAL_REVIEW khi chưa có owner_unlock')
thu('9d attempt 4 chuyển MANUAL_REVIEW là đúng', False, anh=[rec('a4', 1, 4, 'MANUAL_REVIEW')])
thu('10 Bản ghi ảnh dùng tham chiếu chưa duyệt', True, anh=[rec('a1', 1, 1, 'PASS', reference_images=[dict(image_id='lt1v4-test-01', purpose='style_only')])], ky_vong='không hợp lệ')
# quyết định vẽ
qd = lambda rs, sid=1: Q.quyet_dinh_ve(rs, sid)[0]
cases = [('11a Chưa vẽ → VE', qd([]), 'VE'), ('11b attempt 1 REGENERATE → VE', qd([rec('a', 1, 1, 'REGENERATE')]), 'VE'), ('11c attempt 3 REGENERATE → VE (lần vẽ lại thứ 3)', qd([rec('a', 1, 3, 'REGENERATE')]), 'VE'),
         ('11d attempt 4 chưa PASS → MANUAL_REVIEW', qd([rec('a', 1, 4, 'REGENERATE')]), 'MANUAL_REVIEW'), ('11e đã PASS → DA_PASS', qd([rec('a', 1, 2, 'PASS')]), 'DA_PASS'),
         ('11f MANUAL_REVIEW chưa unlock → MANUAL_REVIEW', qd([rec('a', 1, 2, 'MANUAL_REVIEW')]), 'MANUAL_REVIEW'),
         ('11g 24 ảnh thử STALE không tính là đã vẽ', qd([rec('a', 1, 4, 'STALE')]), 'VE')]
for ten, got, want in cases:
    ok = got == want; kq.append(ok); print(('PASS ' if ok else 'FAIL ') + ten + ('' if ok else f'  [{got}]'))
# thư mục thật
K.bad.clear(); real = json.load(open(f'{Q.R}/ke-hoach/anh/lt1v4/anh.json', encoding='utf-8'))['images']; K.kiem_anh(real, [])
ok = not K.bad and all((not r['duoc_dung_lam_tham_chieu'] and r['status'] == 'STALE') or r['image_id'] == 'CR-LTK-B2' for r in real) and sum(r['status'] != 'STALE' for r in real) == 1; kq.append(ok)
print(('PASS ' if ok else 'FAIL ') + f'12 Sổ ảnh thật: {len(real)} ảnh, ảnh cũ đều STALE; ngoại lệ duy nhất CR-LTK-B2 (PASS, chủ kênh duyệt), 0 lỗi {K.bad[:2]}')
ds = Q.tham_chieu_duoc_duyet('lt1v4')['anh']; ok = [x['image_id'] for x in ds] == ['CR-LTK-B2'] and ds[0]['muc_dich'] == 'face_only' and ds[0]['duyet_boi'] == 'chủ kênh' and Q.tham_chieu_hop_le('lt1v4', 'CR-LTK-B2')[0]; kq.append(ok); print(('PASS ' if ok else 'FAIL ') + f'13 Danh sách ảnh tham chiếu được duyệt: {len(ds)} ảnh (chỉ CR-LTK-B2, face_only; Tông Đản chưa có)')

# --- ảnh cũ không thể lọt qua dù bị ghi nhầm vào danh sách duyệt; ảnh hợp lệ thì qua được
import shutil
d = f'{Q.R}/ke-hoach/anh/tmp_test'; os.makedirs(d, exist_ok=True)
try:
    json.dump({'anh': [dict(image_id='lt1v4-test-01', duyet_boi='x', ngay='2026-11-02'), dict(image_id='ok-1', duyet_boi='chủ kênh', ngay='2026-11-02'), dict(image_id='cu-1', duyet_boi='chủ kênh', ngay='2026-11-02')]}, open(f'{d}/tham-chieu-duoc-duyet.json', 'w'))
    json.dump({'images': [dict(image_id='lt1v4-test-01', scene_id=1, attempt=1, status='STALE', bible_versions='khong-co'), dict(image_id='ok-1', scene_id=1, attempt=1, status='PASS', bible_versions=dict(CUR)),
                          dict(image_id='cu-1', scene_id=2, attempt=1, status='PASS', bible_versions={'master': '1.1', 'period': '1.2', 'khoi_prompt': '1.2'})]}, open(f'{d}/anh.json', 'w'))
    for ten, iid, want in [('14a Ảnh STALE bị ghi nhầm vào danh sách duyệt vẫn bị chặn', 'lt1v4-test-01', False), ('14b Ảnh PASS theo phiên bản hiện hành, đã duyệt: được dùng', 'ok-1', True),
                           ('14c Ảnh PASS nhưng vẽ theo phiên bản Bible cũ: bị chặn', 'cu-1', False), ('14d Ảnh không có trong danh sách: bị chặn', 'khac', False)]:
        ok, why = Q.tham_chieu_hop_le('tmp_test', iid); good = ok == want; kq.append(good); print(('PASS ' if good else 'FAIL ') + ten + (f'  ↳ {why[:110]}' if why else ''))
finally: shutil.rmtree(d)
# --- script vẽ cũ không còn tự gọi 19901 làm tham chiếu
import subprocess
code = "import sys,runpy,urllib.request as u; sys.argv=['cf_ve_lt1t2.py','19905','ref']; import ai_images as ai; ai._creds=lambda:('a','b'); u.urlopen=lambda *a,**k:(_ for _ in ()).throw(RuntimeError('chặn mạng')); runpy.run_path('cf_ve_lt1t2.py',run_name='__main__')"
out = subprocess.run([sys.executable, '-c', code], cwd=Q.R, capture_output=True, text=True, timeout=60).stdout
ok = 'bỏ ảnh tham chiếu chưa được chủ kênh duyệt' in out; kq.append(ok)
print(('PASS ' if ok else 'FAIL ') + '15 cf_ve_lt1t2.py ref: tham chiếu 19901 bị bỏ vì chưa duyệt  ↳ ' + out.strip().split('\n')[0][:120])
# --- voi (chỉ voi, kiểm như người/ngựa)
EP = f"Procession. EXACTLY two elephants in single file, each led by one attendant on foot. {A} {S}"
eg = lambda e, n=2: [dict(name='người dắt voi', count=n, position='cạnh voi', role='dắt', horses=0, mounted=0, elephants=e)]
pairs = lambda n: [dict(handler=f'người {k}', elephant=f'voi {k}') for k in range(1, n + 1)]
ev = lambda p=EP, **k: cau(p, expected_people=2, expected_elephants=2, groups=eg(2), elephant_pairs=pairs(2), blocks_used=[], detail_tags=[], **k)
thu('16a Cảnh 2 voi, 2 người dắt, 2 cặp: hợp lệ', False, ev())
thu('16b Tổng voi các nhóm khác expected_elephants', True, cau(EP, expected_people=2, expected_elephants=2, groups=eg(1), elephant_pairs=pairs(2), blocks_used=[], detail_tags=[]), 'tổng elephants', w=True)
thu('16c Prompt ghi EXACTLY three elephants, kế hoạch 2', True, ev(EP.replace('two elephants', 'three elephants')), 'EXACTLY three', w=True)
thu('16d Thiếu "EXACTLY N elephants" trong prompt', True, ev(f"Procession with two elephants. {A} {S}"), 'không có "EXACTLY', w=True)
thu('16e Thiếu cặp người dắt – voi', True, cau(EP, expected_people=2, expected_elephants=2, groups=eg(2), elephant_pairs=pairs(1), blocks_used=[], detail_tags=[]), 'elephant_pairs phải có', w=True)
thu('16f Hai người cùng dắt một con voi', True, cau(EP, expected_people=2, expected_elephants=2, groups=eg(2), elephant_pairs=[dict(handler='a', elephant='voi 1'), dict(handler='b', elephant='voi 1')], blocks_used=[], detail_tags=[]), 'chỉ xuất hiện đúng một lần', w=True)
thu('16g expected_elephants=0 nhưng prompt nhắc voi', True, cau(P0 + ' elephant'), 'nhắc voi', w=True)
thu('16h Còn dùng expected_animals_other', True, cau(P0, expected_animals_other={'voi': 1}), 'expected_animals_other', w=True)
rv = lambda i, st, dv, kv, **k: rec(i, 'E', 1, st, dem=(2, 0), kh=(2, 0), **k) | dict(dem_thu_cong=dict(nguoi=2, ngua=0, voi=dv, nguoi_dem='chủ kênh', ngay='2026-11-02') if dv is not None else dict(nguoi=2, ngua=0, nguoi_dem='chủ kênh', ngay='2026-11-02'), ke_hoach=dict(nguoi=2, ngua=0, voi=kv))
pe = ev() | dict(scene_id='E')
def anhE(recs):
    K.bad.clear(); K.warn.clear(); K.kiem_anh(recs, [pe]); return [l for l in K.bad + K.warn if 'QK-' in l or '❌' in l]
for ten, recs, want in [('17a PASS, voi thực tế 2 khớp dự kiến 2', [rv('e1', 'PASS', 2, 2)], None), ('17b PASS nhưng voi thực tế 3, dự kiến 2', [rv('e1', 'PASS', 3, 2)], 'số voi thực tế'),
                        ('17c Cảnh có voi nhưng thiếu voi trong dem_thu_cong', [rv('e1', 'REVIEW', None, 2)], 'thiếu "voi"'), ('17d Voi lệch thì REVIEW được (không PASS)', [rv('e1', 'REVIEW', 3, 2)], None)]:
    loi = anhE(recs); ok = (not loi) if want is None else any(want in l for l in loi); kq.append(ok); print(('PASS ' if ok else 'FAIL ') + ten + ('' if ok else f'  -> {loi}'))
# --- bản đồ, đoạn dùng nhiều cảnh, cảnh giữ lâu, chi tiết nghệ thuật
real = json.load(open(f'{Q.R}/ke-hoach/anh/lt1v4/scene-planner.json', encoding='utf-8')); RS = real['scenes']
mp = copy.deepcopy(next(x for x in RS if x['scene_id'] == 'M1'))
thu('18a Bản đồ thật M1 bị chặn NEEDS_REVIEW, không lỗi', False, mp)
thu('18b Bản đồ tự đặt toa_do trong planner', True, dict(mp, toa_do=[1, 2]), 'tự đặt toa_do', w=True)
thu('18c Bản đồ thiếu danh sách dữ liệu cần xác minh', True, {k: v for k, v in mp.items() if k != 'map_items'}, 'thiếu map_data_ref', w=True)
thu('18d Bản đồ còn NEEDS_REVIEW mà map_status không chặn', True, dict(mp, map_status='READY'), 'không phải BLOCKED', w=True)
thu('18e Bản đồ NEEDS_REVIEW không được PLAN_APPROVED', True, dict(mp, plan_status='PLAN_APPROVED'), 'không thể PLAN_APPROVED', w=True)
mj = json.load(open(f'{Q.R}/ke-hoach/anh/lt1v4/ban-do-can-xac-minh.json', encoding='utf-8'))['items']
ok = len(mj) == 33 and all(x['loai'] in ('DIA_LY', 'DUONG_QUAN_SU', 'DIEN_GIAI') and x['toa_do'] is None and not x['duoc_ve'] and ((x['trang_thai'] == 'VERIFIED' and x.get('nguon_xac_minh')) or x['trang_thai'] == 'NEEDS_REVIEW') for x in mj); kq.append(ok)
print(('PASS ' if ok else 'FAIL ') + f'18f {len(mj)} mục xác minh bản đồ: VERIFIED phải kèm nguồn, còn lại NEEDS_REVIEW; không mục nào có tọa độ hay được vẽ')
def doan(sc, cuts):
    K.bad.clear(); K.warn.clear(); K.kiem_doan(sc, cuts); return [l for l in K.bad + K.warn if 'QK-' in l or '❌' in l]
no66 = [x for x in RS]
loi = doan(no66, {}); ok = any('đoạn 87' in l and 'segment_cuts' in l for l in loi); kq.append(ok); print(('PASS ' if ok else 'FAIL ') + '19a Đoạn 87 (66 cũ) dùng hai cảnh mà thiếu segment_cuts bị chặn')
bad_cut = {'87': [dict(thu_tu=1, scene='L25', cau='Một lần khác, ông dựng phòng tuyến bên sông, bảo vệ từng tấc đất quê hương.'), dict(thu_tu=2, scene='L03', cau='Một lần, ông đưa quân vượt biên giới, đánh vào đất địch.')]}
loi = doan(no66, bad_cut); ok = any('sai thứ tự' in l for l in loi); kq.append(ok); print(('PASS ' if ok else 'FAIL ') + '19b Thứ tự cắt đoạn 87 (66 cũ) sai so với lời đọc bị chặn')
loi = doan(no66, real['segment_cuts']); ok = not loi; kq.append(ok); print(('PASS ' if ok else 'FAIL ') + f'19c segment_cuts thật của đoạn 87 (66 cũ) hợp lệ {loi[:1]}')
nm = [dict(x) for x in RS]
for x in nm:
    if x['scene_id'] == 'L32': x.pop('motion_plan')
loi = doan(nm, real['segment_cuts']); ok = any('L32' in l and 'motion_plan' in l for l in loi); kq.append(ok); print(('PASS ' if ok else 'FAIL ') + '20 Ảnh giữ ~31 giây (L32) thiếu motion_plan bị chặn')
la = copy.deepcopy(next(x for x in RS if x['scene_id'] == 'L04'))
la['free_text_details'][0]['owner_approved'] = True; la['free_text_details'][0].pop('approved_by', None); la['free_text_details'][0].pop('approved_date', None)
thu('21a Duyệt chi tiết nghệ thuật thiếu approved_by/ngày', True, la, 'thiếu approved_by', w=True)
la['free_text_details'][0].update(approved_by='chủ kênh', approved_date='2026-11-02')
thu('21b Duyệt đủ thông tin vẫn giữ evidence_level C: hợp lệ', False, la)
la['free_text_details'][0]['evidence_level'] = 'B'
thu('21c Sau duyệt đổi lựa chọn nghệ thuật thành mức B (dữ kiện): bị chặn', True, la, 'không khớp')
la['free_text_details'][0].update(evidence_level='C', approval_scope='historical')
thu('21d approval_scope không phải visual_only: bị chặn', True, la, 'visual_only', w=True)
# --- kiến trúc 4 tầng: cổng sản xuất, phạm vi, AUTO, registry, hồ sơ nhân vật, tài liệu APPROVED
import hashlib as _h
REGJ = json.load(open(f'{Q.R}/quy-tac/anh/quyet-dinh.json', encoding='utf-8'))
def tinh(ten, ok, ghi=''):
    kq.append(bool(ok)); print(('PASS ' if ok else 'FAIL ') + ten + (f'  [{ghi}]' if (ghi and not ok) else ''))
# Cách B: quy tắc mới PROPOSED chỉ cảnh báo; khi chủ kênh duyệt (APPROVED + block) mới chặn
old_q = dict(K.QKS)
K.QKS['QK-VOI'] = dict(id='QK-VOI', trang_thai='APPROVED', che_do='block')
loi = chay(cau(EP, expected_people=2, expected_elephants=2, groups=eg(1), elephant_pairs=pairs(2), blocks_used=[], detail_tags=[]))
tinh('22a Sau khi QK-VOI APPROVED thì cùng lỗi voi chuyển thành ❌ chặn', any('tổng elephants' in l for l in loi), loi)
K.QKS.clear(); K.QKS.update(old_q)
tinh('22b Năm quy tắc "kiểm thêm" (voi, bản đồ, đoạn, giữ lâu, duyệt nghệ thuật) đã APPROVED bởi chủ kênh 01/11/2026 và chặn; QK-HOSO (không thuộc mục 5) vẫn PROPOSED', all(K.QKS[k]['trang_thai'] == 'APPROVED' and K.QKS[k]['che_do'] == 'block' and K.QKS[k].get('nguoi_duyet') and K.QKS[k].get('ngay_duyet') for k in ('QK-VOI', 'QK-BANDO', 'QK-DOAN', 'QK-GIULAU', 'QK-DUYET-NT')) and K.QKS['QK-HOSO']['trang_thai'] == 'PROPOSED')
# cổng trước khi vẽ
def gate(s): K.bad.clear(); K.warn.clear(); return K.cong_san_xuat(s)
ap = lambda s: dict(s, plan_status='PLAN_APPROVED')
ok_, why = gate(ap(base)); tinh('23a Cổng cho phép cảnh sạch đã PLAN_APPROVED', ok_, why)
ok_, why = gate(base); tinh('23b Cổng chặn cảnh chưa PLAN_APPROVED', not ok_ and any('chưa PLAN_APPROVED' in w for w in why))
ok_, why = gate(ap(cau(P0, groups=[dict(name='lính', count=2, position='tiền cảnh', role='gác', horses=0, mounted=0)]))); tinh('23c Cổng chặn khi có lỗi quy tắc cũ đã APPROVED (số người)', not ok_ and any('lỗi quy tắc đã APPROVED' in w for w in why))
ok_, why = gate(ap(base | dict(free_text_details=[dict(item='mái che', tag='artistic_choice', evidence_level='C', reason='x', owner_approved=False)]))); tinh('23d Cổng chặn chi tiết nghệ thuật chưa duyệt', not ok_ and any('chưa được chủ kênh duyệt' in w for w in why))
ok_, why = gate(ap(base | dict(thay_mat=True, ho_so_nhan_vat=[dict(ma='ly-thuong-kiet', giai_doan=['S1'])]))); tinh('23e Cổng chặn khi vi phạm quy tắc còn PROPOSED (QK-HOSO: râu S1 UNDECIDED, cảnh báo không phải giấy phép)', not ok_ and any('quy tắc chưa duyệt' in w for w in why))
ok_, why = gate(ap(base | dict(free_text_details=[dict(item='bản vẽ', tag='artistic_choice', evidence_level='C', reason='x', owner_approved=True, approved_by='a', approved_date='d', decision_mode='MUST_VERIFY')]))); tinh('23f Cổng chặn MUST_VERIFY chưa VERIFIED kèm nguồn', not ok_ and any('MUST_VERIFY' in w for w in why))
ok_, why = gate(ap(base | dict(quyet_dinh_ap_dung=['DQ-001']))); tinh('23g Cổng chặn cảnh dùng quyết định mới PROPOSED', not ok_ and any('DQ-001' in w for w in why))
rs = [x for x in RS if x.get('render') != 'vector_map']; res = [gate(x)[0] for x in rs + [x for x in RS if x.get('render') == 'vector_map']]
tinh(f'23h Planner thật đang PLAN_OWNER_REVIEW: cổng chặn cả {len(res)} cảnh (không cảnh nào vào sản xuất)', not any(res))
# phạm vi và AUTO với quyết định giả định APPROVED (bản sao, không ghi file)
dq_ok = lambda i, **kw: dict(next(d for d in REGJ['quyet_dinh'] if d['id'] == i), trang_thai='APPROVED', nguoi_duyet='x', ngay_duyet='d', **kw)
S35 = next(x for x in RS if x['scene_id'] == 'L35'); S25 = next(x for x in RS if x['scene_id'] == 'L25'); S32 = next(x for x in RS if x['scene_id'] == 'L32')
for ten, dq, sc_, want_ok, mode in [('24a DQ-001 APPROVED, cảnh năm 1105 (ngoài 1075–1077) → OWNER_APPROVAL', 'DQ-001', S35, False, 'OWNER_APPROVAL'), ('24b DQ-003 APPROVED, cảnh 1077 trong phạm vi', 'DQ-003', S25, True, None),
                                    ('24c DQ-002 APPROVED, cảnh niên đại không rõ → MUST_VERIFY', 'DQ-002', dict(S25, nien_dai_canh=[1075, None]), False, 'MUST_VERIFY'), ('24d DQ-004 GLOBAL dùng được ở cảnh bất kỳ', 'DQ-004', dict(S32, nien_dai_canh=[1500, 1600]), True, None)]:
    ok_, why, md = K.dq_hop_le(dq_ok(dq, canh_ngoai_pham_vi_duoc_duyet={}), sc_); tinh(ten, ok_ == want_ok and md == mode, (ok_, why, md))
tinh('24e Quyết định APPROVED áp cho phiên bản Bible khác bị coi là ngoài phạm vi', not K.dq_hop_le(dq_ok('DQ-004', phien_ban_ap_dung=dict(period='1.9')), S32)[0])
K.REG['DQ-009'] = dq_ok('DQ-001', id='DQ-009')
K.bad.clear(); K.warn.clear(); K.kiem_canh(dict(base, free_text_details=[dict(item='bản đồ', tag='artistic_choice', evidence_level='C', reason='x', owner_approved=False, decision_mode='AUTO', quyet_dinh='DQ-001')]))
tinh('25a AUTO nhưng quyết định chưa APPROVED: bị đánh dấu coi như OWNER_APPROVAL', any('QK-AUTO' in l or 'AUTO' in l for l in K.warn), K.warn)
K.bad.clear(); K.warn.clear(); K.kiem_canh(dict(base, nien_dai_canh=[1075, 1077], free_text_details=[dict(item='bản đồ', tag='artistic_choice', evidence_level='C', reason='x', owner_approved=False, decision_mode='AUTO', quyet_dinh='DQ-009')]))
tinh('25b AUTO có quyết định APPROVED đúng phạm vi: không bị hạ cấp', not any('AUTO' in l for l in K.warn + K.bad), K.warn + K.bad)
K.REG.pop('DQ-009')
# toàn vẹn registry
def kr(reg=None, prof=None, ar=None): K.bad.clear(); K.warn.clear(); K.kiem_registry(reg, RS, prof, ar); return list(K.bad)
PR = [json.load(open(f'{Q.R}/quy-tac/anh/nhan-vat/{n}.json', encoding='utf-8')) for n in ('ly-thuong-kiet', 'tong-dan')]
tinh('26a Registry và 2 hồ sơ nhân vật thật: 0 lỗi', not kr(None, PR), kr(None, PR))
mut = lambda **kw: dict(REGJ, quyet_dinh=[dict(REGJ['quyet_dinh'][0], **kw)] + REGJ['quyet_dinh'][1:])
for ten, kw, want in [('26b Quyết định PROPOSED đặt AUTO bị chặn', dict(trang_thai='PROPOSED', decision_mode='AUTO'), 'chưa APPROVED không được đặt AUTO'), ('26c Mục C bị đổi thành dữ kiện lịch sử', dict(la_du_kien_lich_su=True), 'la_du_kien_lich_su'),
                      ('26d Mục C duyệt ngoài visual_only', dict(approval_scope='historical'), 'visual_only'), ('26e Mục C thiếu ghi chú "không phải dữ kiện lịch sử"', dict(ghi_chu_bat_buoc='ok'), 'KHÔNG phải dữ kiện'),
                      ('26f Quyết định PERIOD thiếu niên đại', dict(pham_vi=dict(cap='PERIOD', thoi_ky='Lý')), 'nien_dai'), ('26g Quyết định trỏ tới cảnh không tồn tại', dict(danh_sach_canh=['L99']), 'không tồn tại'),
                      ('26h APPROVED thiếu người duyệt', dict(trang_thai='APPROVED', nguoi_duyet=None), 'nguoi_duyet')]:
    loi = kr(mut(**kw)); tinh(ten, any(want in l for l in loi), loi)
pm = json.loads(json.dumps(PR)); pm[0]['giai_doan'][0]['dac_diem']['rau'].update(gia_tri='bạc')
tinh('27a Màu râu UNDECIDED nhưng đã khóa giá trị bị chặn', any('UNDECIDED' in l for l in kr(None, pm)))
pm = json.loads(json.dumps(PR)); pm[0]['anh_tham_chieu_da_duyet'] = ['CR-LTK-2']
tinh('27b Hồ sơ nhân vật ghi ảnh tham chiếu chưa có trong danh sách duyệt bị chặn', any('tham-chieu-duoc-duyet' in l for l in kr(None, pm)))
pm = json.loads(json.dumps(PR)); pm[0]['ung_vien_chua_duyet'][0]['duoc_dung_lam_tham_chieu'] = True
tinh('27c Ứng viên chưa duyệt bị đánh dấu dùng làm tham chiếu bị chặn', any('chưa được duyệt' in l for l in kr(None, pm)))
tinh('27d Râu Lý Thường Kiệt: S2 đã APPROVED "đen pha bạc" (C, OWNER_APPROVAL, visual_only, không phải dữ kiện lịch sử, DQ-005); S1, S3, S4 vẫn UNDECIDED; Tông Đản UNDECIDED', all((g['dac_diem']['rau']['trang_thai'] == 'APPROVED' and g['dac_diem']['rau']['gia_tri'].startswith('đen pha bạc') and g['dac_diem']['rau']['quyet_dinh'] == 'DQ-005') if g['id'] == 'S2' else (g['dac_diem']['rau']['trang_thai'] == 'UNDECIDED' and g['dac_diem']['rau']['gia_tri'] is None) for g in PR[0]['giai_doan']) and all(g['dac_diem']['rau']['evidence_level'] == 'C' and g['dac_diem']['rau']['decision_mode'] == 'OWNER_APPROVAL' and g['dac_diem']['rau']['approval_scope'] == 'visual_only' and g['dac_diem']['rau']['la_du_kien_lich_su'] is False for p_ in PR for g in p_['giai_doan']) and all(g['dac_diem']['rau']['trang_thai'] == 'UNDECIDED' for g in PR[1]['giai_doan']))
tinh('27e Danh sách ảnh tham chiếu được duyệt chỉ có CR-LTK-B2; hồ sơ Lý Thường Kiệt khớp; Tông Đản chưa có ảnh duyệt', [x['image_id'] for x in Q.tham_chieu_duoc_duyet('lt1v4')['anh']] == ['CR-LTK-B2'] and PR[0]['anh_tham_chieu_da_duyet'] == ['CR-LTK-B2'] and PR[1]['anh_tham_chieu_da_duyet'] == [] and all(r.get('reference_images') == [dict(image_id='CR-LTK-B2', purpose='face_only')] for r in RS if r['scene_id'] in ('L04', 'L11')))
# tài liệu APPROVED và phiên bản không đổi so với baseline b1
BL = json.load(open(f'{Q.R}/phim_ban_do/baseline_kiem/baseline.json', encoding='utf-8'))['baseline']['b1']['sha256']
for fn in ('quy-tac/anh/master-style.md', 'quy-tac/anh/period-ly-tong.md', 'quy-tac/anh/khoi-prompt.json', 'quy-tac/anh/quy-trinh-anh.md'):
    if fn.endswith('quy-trinh-anh.md'):   # chủ kênh duyệt mục 5 và nâng v1.3 (01/11/2026): SHA mới ghi ở sau_duyet_2026-11-01.json, baseline vẫn nguyên
        SD = json.load(open(f'{Q.R}/phim_ban_do/baseline_kiem/sau_duyet_2026-11-01.json', encoding='utf-8'))['sha256']
        h_ = _h.sha256(open(f'{Q.R}/{fn}', 'rb').read()).hexdigest()
        tinh('28 quy-trinh-anh.md khớp SHA-256 sau khi chủ kênh duyệt mục 5 (v1.3), khác baseline b1', h_ == SD[fn] and h_ != BL[fn])
    else: tinh(f'28 {fn.split("/")[-1]} giống hệt baseline (SHA-256)', _h.sha256(open(f'{Q.R}/{fn}', 'rb').read()).hexdigest() == BL[fn])
tinh('29 bible_versions của lt1v4 vẫn 1.3 và planner chưa PLAN_APPROVED', real['bible_versions'] == dict(master='1.3', period='1.3', khoi_prompt='1.3') and real['plan_status'] == 'PLAN_OWNER_REVIEW' and not any(x['plan_status'] == 'PLAN_APPROVED' for x in RS))
tinh('30 Không quyết định PROPOSED nào là AUTO', all(not (d['trang_thai'] == 'PROPOSED' and d['decision_mode'] == 'AUTO') for d in REGJ['quyet_dinh']))
tinh('31 Registry: DQ-001..004 APPROVED bởi chủ kênh 01/11/2026 (C, OWNER_APPROVAL, visual_only); DQ-005 râu CHARACTER APPROVED; chưa mục nào AUTO', {d['id'] for d in REGJ['quyet_dinh']} == {'DQ-001', 'DQ-002', 'DQ-003', 'DQ-004', 'DQ-005'} and all(d['trang_thai'] == 'APPROVED' and d['nguoi_duyet'] == 'chủ kênh' and d['ngay_duyet'] == '2026-11-01' and d['evidence_level'] == 'C' and d['decision_mode'] == 'OWNER_APPROVAL' and d['approval_scope'] == 'visual_only' and d['la_du_kien_lich_su'] is False for d in REGJ['quyet_dinh']))
# --- liên kết hồ sơ nhân vật và quyết định râu chỉ khi thấy mặt
S04 = next(x for x in RS if x['scene_id'] == 'L04'); S08 = next(x for x in RS if x['scene_id'] == 'L08'); S11 = next(x for x in RS if x['scene_id'] == 'L11')
S1T = base | dict(thay_mat=True, ho_so_nhan_vat=[dict(ma='ly-thuong-kiet', giai_doan=['S1'])])
K.bad.clear(); K.warn.clear(); K.kiem_canh(S1T)
tinh('32a Cảnh thấy mặt Lý Thường Kiệt giai đoạn S1 mà râu UNDECIDED: cảnh báo cần chủ kênh quyết', any('QK-HOSO' in l and 'UNDECIDED' in l for l in K.warn) and not any('QK-HOSO' in l for l in K.bad))
for sc_ in (S04, S11):
    K.bad.clear(); K.warn.clear(); K.kiem_canh(sc_)
    tinh(f'32a2 {sc_["scene_id"]} (S2, thấy mặt): râu đã quyết (DQ-005), không còn cảnh báo UNDECIDED; prompt có râu đen pha bạc, không còn "grey beard"', not any('UNDECIDED' in l for l in K.warn + K.bad) and 'black beard lightly streaked with grey' in sc_['image_prompt'] and 'grey beard' not in sc_['image_prompt'] and 'DQ-005' in sc_['quyet_dinh_ap_dung'])
K.bad.clear(); K.warn.clear(); K.kiem_canh(S08)
tinh('32b Cảnh nhìn từ phía sau (L08) không cần quyết định râu', not any('UNDECIDED' in l for l in K.warn))
K.bad.clear(); K.warn.clear(); K.kiem_canh(dict(S08, ho_so_nhan_vat=[dict(ma='ly-thuong-kiet', giai_doan=['S9'])]))
tinh('32c Giai đoạn không có trong hồ sơ bị đánh dấu', any('không có giai đoạn S9' in l for l in K.warn))
ok_, why = gate(ap(S1T)); tinh('32d Cổng chặn cảnh thấy mặt mà râu chưa quyết (kể cả nếu giả sử PLAN_APPROVED)', not ok_ and any('UNDECIDED' in w for w in why))
# --- DQ-005 (phạm vi CHARACTER) và L33 (lính Tống được trao trả)
d5 = next(d for d in REGJ['quyet_dinh'] if d['id'] == 'DQ-005')
tinh('33a DQ-005 áp dụng cho cảnh khai Lý Thường Kiệt S2 (L11)', K.dq_hop_le(d5, S11)[0])
tinh('33b DQ-005 không áp dụng cho cảnh khai giai đoạn S1 hoặc không khai hồ sơ → ngoài phạm vi', not K.dq_hop_le(d5, S1T)[0] and not K.dq_hop_le(d5, base)[0])
tinh('33c Registry thiếu nhan_vat/giai_doan trong phạm vi CHARACTER bị chặn', any('CHARACTER' in l for l in kr(dict(REGJ, quyet_dinh=[dict(d5, pham_vi=dict(cap='CHARACTER'))] + [d for d in REGJ['quyet_dinh'] if d['id'] != 'DQ-005']))))
S33 = next(x for x in RS if x['scene_id'] == 'L33')
tinh('33d L33 có đúng 8 dân + 4 lính Tống không vũ khí + 2 lính Đại Việt = 14 người; prompt khớp', S33['expected_people'] == 14 and [g['count'] for g in S33['groups']] == [8, 4, 2] and 'four unarmed Song soldiers' in S33['image_prompt'] and 'carry nothing' in S33['image_prompt'])
a22 = next(f for f in S33['free_text_details'] if f['id'] == 'AC22'); a20 = next(f for f in S33['free_text_details'] if f['id'] == 'AC20')
tinh('33e AC22 (lính Tống được trao trả) và AC20 (dân) đều đã duyệt 01/11/2026; cả hai C, visual_only, không phải dữ kiện lịch sử', a22['owner_approved'] is True and a22['approved_by'] == 'chủ kênh' and a20['owner_approved'] is True and a22['evidence_level'] == a20['evidence_level'] == 'C' and a22['approval_scope'] == 'visual_only')
tinh('33f Mọi chi tiết ngoài khối (AC01..AC24) đã duyệt bởi chủ kênh 01/11/2026 và vẫn là C, visual_only', {f['id'] for x in RS for f in x.get('free_text_details', []) if f['owner_approved']} == {f'AC{i:02d}' for i in range(1, 25)} and all(f['evidence_level'] == 'C' and f['approval_scope'] == 'visual_only' and f['la_du_kien_lich_su'] is False for x in RS for f in x.get('free_text_details', [])))
BD = json.load(open(f'{Q.R}/ke-hoach/anh/lt1v4/ban-do-can-xac-minh.json', encoding='utf-8'))
tinh('33g Bản đồ: chủ kênh duyệt danh sách và chấp nhận nguồn thứ cấp; 9 mục VERIFIED kèm nguồn, không mục nào có tọa độ hay được vẽ; 7 bản đồ vẫn bị chặn', len(BD['items']) == 33 and BD['chu_kenh_duyet_danh_sach']['trang_thai'] == 'APPROVED' and sum(x['trang_thai'] == 'VERIFIED' for x in BD['items']) == 9 and all(x['toa_do'] is None and x['duoc_ve'] is False for x in BD['items']) and all(x.get('map_status') == 'BLOCKED_NEEDS_REVIEW' for x in RS if x.get('render') == 'vector_map'))
tinh('33h Kịch bản của planner là bản tách 91 đoạn (đã thêm câu cảm ơn), từ ngữ khớp bản gốc trừ đoạn cuối chủ kênh duyệt; bản gốc 68 đoạn còn nguyên', real['script'].endswith('lt1v4_tach_full.json') and real['so_doan'] == 91 and len(json.load(open(f'{Q.R}/ke-hoach/thu-giong-hai/lt1v4_tach_full.json', encoding='utf-8'))) == 91 and len(json.load(open(f'{Q.R}/ke-hoach/thu-giong-hai/lt1v4_full.json', encoding='utf-8'))) == 68)
d1 = next(d for d in REGJ['quyet_dinh'] if d['id'] == 'DQ-001')
tinh('33i DQ-001: ngoại lệ chỉ L04 và L35 (chủ kênh duyệt), L11 vẫn trong phạm vi, cảnh khác ngoài phạm vi vẫn không được', set(d1['canh_ngoai_pham_vi_duoc_duyet']) == {'L04', 'L35'} and K.dq_hop_le(d1, S35)[0] and K.dq_hop_le(d1, S04)[0] and K.dq_hop_le(d1, S11)[0] and not K.dq_hop_le(d1, dict(S25, scene_id='L99', nien_dai_canh=[1105, 1105]))[0])
print(f'\nTổng: {sum(kq)}/{len(kq)} phép kiểm đạt'); sys.exit(0 if all(kq) else 1)
