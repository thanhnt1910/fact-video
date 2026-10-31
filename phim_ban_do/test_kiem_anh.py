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
def thu(ten, cho_loi, s=None, ky_vong=None, anh=None):
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
ok = not K.bad and all(not r['duoc_dung_lam_tham_chieu'] and r['status'] == 'STALE' for r in real); kq.append(ok)
print(('PASS ' if ok else 'FAIL ') + f'12 Sổ ảnh thật: {len(real)} ảnh cũ đều STALE, không ảnh nào được dùng làm tham chiếu, 0 lỗi {K.bad[:2]}')
ds = Q.tham_chieu_duoc_duyet('lt1v4')['anh']; ok = ds == []; kq.append(ok); print(('PASS ' if ok else 'FAIL ') + f'13 Danh sách ảnh tham chiếu được duyệt: {len(ds)} ảnh (rỗng = chưa có ảnh hợp lệ)')

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
print(f'\nTổng: {sum(kq)}/{len(kq)} phép kiểm đạt'); sys.exit(0 if all(kq) else 1)
