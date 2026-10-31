"""Tạo character-reference.json (kế hoạch ảnh Character Reference cho Lý Thường Kiệt và Tông Đản). Không vẽ, không gọi mạng.
Chỉ là ỨNG VIÊN: ảnh vẽ xong chỉ vào tham-chieu-duoc-duyet.json khi chủ kênh duyệt (không có chân dung đương thời; mọi tạo hình là artistic_choice C)."""
import hashlib, json, os, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, f'{R}/phim_ban_do')
import anh_quy_tac as Q
KP = json.load(open(f'{R}/quy-tac/anh/khoi-prompt.json', encoding='utf-8')); CUR = Q.phien_ban_hien_hanh()
T = lambda b: KP[b]['text']
sc = []
def C(cid, ten, seed, blocks, layout, extra, ft, tags_who, ghi_chu):
    parts = [layout] + [T(b) for b in blocks] + ([extra] if extra else []) + [T('ANATOMY'), T('STYLE')]
    prompt = ' '.join(x.strip() if x.strip().endswith('.') else x.strip() + '.' for x in parts)
    sc.append(dict(scene_id=cid, segment_ids=[], scene_type='portrait', expected_people=1, expected_horses=0, expected_elephants=0, main_characters=[ten],
        positions='một người đứng giữa khung, nền trơn, không đạo cụ', groups=[dict(name=ten, count=1, position='giữa khung', role='tham chiếu nhân vật', faction='viet', horses=0, mounted=0, elephants=0)],
        composition='một nhân vật, nền trơn xám nâu nhạt, không bối cảnh, không đạo cụ', camera=layout.split(':')[0], lighting='ánh sáng mềm một hướng', scenery='plain background',
        blocks_used=blocks, detail_tags=[dict(item=KP[b]['text'][:60], block=b, tag=KP[b]['tag'], evidence_level=KP[b]['evidence_level'], who=ten, bible_ref=KP[b]['bible_ref']) for b in blocks],
        free_text_details=[dict(item=i, tag='artistic_choice', evidence_level='C', reason=r, owner_approved=False, id=f'{cid}-AC{k+1}', approval_scope='visual_only') for k, (i, r) in enumerate(ft)],
        image_prompt=prompt, prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(), prompt_version='p1', prompt_chars=len(prompt), bible_versions=dict(CUR), reference_images=[],
        plan_status='PLAN_OWNER_REVIEW', risk='Medium', seed=seed, ghi_chu=ghi_chu, image_status='CANDIDATE_NOT_DRAWN'))
H = 'Half-length portrait: one {w} stands facing three-quarters toward the viewer with a calm stern expression, hands relaxed at his sides, plain soft grey-brown background, no props, nothing in his hands'
Fl = 'Full-length portrait: one {w} stands upright facing three-quarters toward the viewer, feet visible, plain soft grey-brown background, no props, nothing in his hands'
LB = ['VN_TUONG_LY_THUONG_KIET', 'VN_TUONG']
LT = 'Lý Thường Kiệt'; TD = 'Tông Đản'
for k, (lay, seed) in enumerate([(H, 11), (H, 12), (Fl, 13)], 1):
    C(f'CR-LTK-{k}', LT, seed, LB, lay.format(w='elderly Vietnamese general'), '', [], LT, 'Lý Thường Kiệt: người lớn tuổi, râu bạc (mức C, không có chân dung đương thời). Ba ứng viên khác nhau về khung hình/hạt giống.')
TDX = 'a younger Vietnamese general in his forties with a short black beard'
for k, (lay, seed) in enumerate([(H, 21), (H, 22), (Fl, 23)], 1):
    C(f'CR-TD-{k}', TD, seed, ['VN_TUONG'], lay.format(w=TDX), '', [('Tông Đản trẻ hơn Lý Thường Kiệt, khoảng bốn mươi tuổi, râu đen ngắn', 'không có tư liệu về diện mạo Tông Đản (cùng chi tiết AC ở cảnh L12)')], TD, 'Tông Đản: trẻ hơn, râu đen ngắn (mức C). Dùng khối VN_TUONG cho trang phục.')
# Râu của Lý Thường Kiệt KHÔNG phải dữ kiện lịch sử (chủ kênh 01/11/2026): màu râu là artistic_choice (C). Các phương án so sánh không dùng khối VN_TUONG_LY_THUONG_KIET (khối này ghi râu bạc, chưa đổi Bible).
MC = 'mature Vietnamese general'
for cid, rau, seed, vi in [('CR-LTK-B1', 'a full black beard', 12, 'râu đen'), ('CR-LTK-B2', 'a full black beard streaked with grey', 12, 'râu đen pha bạc'),
                           ('CR-LTK-B3', 'a full black beard', 15, 'râu đen (hạt giống khác)'), ('CR-LTK-B4', 'a full black beard streaked with grey', 15, 'râu đen pha bạc (hạt giống khác)')]:
    C(cid, LT, seed, ['VN_TUONG'], H.format(w=MC), f'The general has {rau}.', [(f'Lý Thường Kiệt: {vi}', 'màu râu không có tư liệu đã kiểm chứng; chủ kênh yêu cầu coi là lựa chọn nghệ thuật'), ('Lý Thường Kiệt: tuổi "mature" (không nêu số tuổi)', 'độ tuổi diện mạo không có tư liệu')],
      LT, f'Phương án so sánh màu râu: {vi}. Giữ khung hình và hạt giống như CR-LTK-2 (B1, B2) hoặc hạt giống khác (B3, B4).')
RAU = {'CR-LTK-1': 'bạc', 'CR-LTK-2': 'bạc', 'CR-LTK-3': 'bạc', 'CR-LTK-B1': 'đen', 'CR-LTK-B2': 'đen pha bạc', 'CR-LTK-B3': 'đen', 'CR-LTK-B4': 'đen pha bạc'}
for x in sc:
    if x['scene_id'] in RAU: x['chi_tiet_rau'] = dict(mau=RAU[x['scene_id']], tag='artistic_choice', evidence_level='C', la_du_kien_lich_su=False, ghi_chu='Màu râu Lý Thường Kiệt chưa có tư liệu kiểm chứng cho 1075–1077; không coi là đặc điểm lịch sử.')
# giữ nhận xét đã ghi cho các ứng viên cũ
_old = f'{R}/ke-hoach/anh/lt1v4/character-reference.json'
if os.path.exists(_old):
    prev = {x['scene_id']: x for x in json.load(open(_old, encoding='utf-8'))['scenes']}
    for x in sc:
        p = prev.get(x['scene_id'])
        if p:
            for k in ('image_status', 'review_note', 'image_file', 'nguoi_dem_so_bo', 'duoc_dung_lam_tham_chieu'):
                if k in p: x[k] = p[k]
# Hai nhân vật phải nhìn khác nhau rõ ràng: ghi nhận để chủ kênh kiểm
json.dump(dict(project='lt1v4', loai='character_reference', plan_version='1', plan_status='PLAN_OWNER_REVIEW', bible_versions=dict(CUR),
               quy_tac=['Mọi tạo hình là artistic_choice (C): không có chân dung đương thời đáng tin của hai người.', 'Ảnh vẽ xong chỉ là ứng viên (CANDIDATE); chỉ vào tham-chieu-duoc-duyet.json khi chủ kênh duyệt, kèm mục đích face_only.',
                        'Tham chiếu chỉ dùng cho khuôn mặt/độ tuổi/râu/dáng, không sao chép bố cục; không dùng làm căn cứ lịch sử.'], scenes=sc),
          open(f'{R}/ke-hoach/anh/lt1v4/character-reference.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(sc), 'ứng viên')
