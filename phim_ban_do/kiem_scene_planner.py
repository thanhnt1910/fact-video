"""Kiểm Scene Planner trước khi vẽ ảnh (quy-tac/anh/quy-trinh-anh.md).
python phim_ban_do/kiem_scene_planner.py <mã video> [--file đường_dẫn.json]
Đọc ke-hoach/anh/<mã>/scene-planner.json. Thoát mã 1 nếu có ❌. Không gọi mạng, không vẽ ảnh."""
import json, os, re, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ma = sys.argv[1]
fp = sys.argv[sys.argv.index('--file') + 1] if '--file' in sys.argv else f'{R}/ke-hoach/anh/{ma}/scene-planner.json'
KP = json.load(open(f'{R}/quy-tac/anh/khoi-prompt.json', encoding='utf-8'))
TAGS = {'historical_evidence': 0, 'cautious_reconstruction': 1, 'artistic_choice': 2}
LV = {'A': 0, 'B': 1, 'C': 2}  # càng lớn càng "nhẹ" bằng chứng
def ver(path, pat):
    m = re.search(pat, open(f'{R}/quy-tac/anh/{path}', encoding='utf-8').read()); return m.group(1) if m else '?'
CUR = {'master': ver('master-style.md', r'\(v([\d.]+)'), 'period': ver('period-ly-tong.md', r'\(v([\d.]+)'), 'khoi_prompt': str(KP['phien_ban']).split('-')[0]}
BIEN = 1800
# từ cấm trong prompt nếu cảnh không dùng khối cho phép nó
CAM = [(r'conical|bamboo hat', 'VN_NON_DAN_PHU'), (r'flag|pennant|banner', 'VN_CO'), (r'\bsacks?\b', None), (r'lantern', None),
       (r'\bcap\b|peaked', None), (r'uniform', None), (r'\bgun|rifle|musket', None), (r'\bstar\b', None)]
d = json.load(open(fp, encoding='utf-8'))
sc = d['scenes'] if isinstance(d, dict) else d
bad, warn = [], []
B = lambda i, m: bad.append(f'❌ {i}: {m}')
W = lambda i, m: warn.append(f'⚠️ {i}: {m}')
BB = ['main_characters', 'positions', 'groups', 'scene_id', 'segment_ids', 'scene_type', 'expected_people', 'expected_horses', 'composition', 'camera', 'lighting', 'blocks_used', 'detail_tags',
      'free_text_details', 'image_prompt', 'prompt_sha256', 'prompt_version', 'bible_versions', 'plan_status', 'reference_images']
import hashlib
for s in sc:
    i = s.get('scene_id', '?')
    for k in BB:
        if k not in s: B(i, f'thiếu trường {k}')
    if any(k not in s for k in BB): continue
    p = s['image_prompt']
    if hashlib.sha256(p.encode()).hexdigest() != s['prompt_sha256']: B(i, 'prompt_sha256 không khớp prompt')
    if len(p) > BIEN: B(i, f'prompt {len(p)} ký tự (tối đa {BIEN} cho klein)')
    if KP['STYLE']['text'] not in p: B(i, 'prompt thiếu nguyên văn khối STYLE')
    if s['expected_people'] and KP['ANATOMY']['text'] not in p: B(i, 'cảnh có người nhưng thiếu nguyên văn khối ANATOMY')
    if s['free_text_details']: B(i, f'free_text_details không rỗng: {s["free_text_details"]} (chỉ được dùng sau khi chủ kênh duyệt)')
    used = set(s['blocks_used'])
    for b in used:
        if b not in KP or not isinstance(KP[b], dict): B(i, f'khối {b} không có trong khoi-prompt.json')
    tagged = {}
    for t in s['detail_tags']:
        for k in ('item', 'block', 'tag', 'bible_ref'):
            if k not in t: B(i, f'detail_tags thiếu {k}: {t}')
        b, tg = t.get('block'), t.get('tag')
        if tg not in TAGS: B(i, f'nhãn "{tg}" không hợp lệ (chỉ historical_evidence, cautious_reconstruction, artistic_choice)'); continue
        if b in KP and isinstance(KP[b], dict) and TAGS[tg] < TAGS[KP[b]['tag']]: B(i, f'nhãn {tg} của "{t.get("item")}" mạnh hơn nhãn của khối {b} ({KP[b]["tag"]})')
        tagged[b] = tg
        kb = KP.get(b)
        if isinstance(kb, dict) and t.get('evidence_level') != kb.get('evidence_level'): B(i, f'evidence_level của "{t.get("item")}" ({t.get("evidence_level")}) khác mức gốc của khối {b} ({kb.get("evidence_level")}); không được gộp hay đổi mức')
    for b in used:
        if b in KP and isinstance(KP[b], dict) and KP[b]['tag'] != 'style_rule' and b not in tagged: B(i, f'khối {b} (mức {KP[b]["tag"]}) chưa có trong detail_tags')
    for pat, blk in CAM:
        if re.search(pat, p, re.I) and (blk is None or blk not in used):
            B(i, f'prompt có "{pat}" nhưng cảnh không dùng khối cho phép ({blk or "không có khối nào"}) → chi tiết tự suy diễn')
    n = re.findall(r'\b(\d+)\b|\b(EXACTLY \w+)', p)
    if s['expected_horses'] and 'horse' not in p.lower(): B(i, 'expected_horses > 0 nhưng prompt không nhắc ngựa')
    if s['expected_horses'] and 'EXACTLY' not in p: W(i, 'cảnh có ngựa nhưng prompt không dùng "EXACTLY N horses"')
    g = s['groups']
    if not isinstance(g, list) or not g: B(i, 'groups rỗng: phải khai nhóm nhân vật')
    else:
        for x in g:
            for k in ('name', 'count', 'position', 'role'):
                if k not in x: B(i, f'groups thiếu {k}: {x}')
        if sum(x.get('count', 0) for x in g) != s['expected_people']: B(i, f'tổng count các nhóm ({sum(x.get("count", 0) for x in g)}) khác expected_people ({s["expected_people"]})')
    if not s['main_characters']: B(i, 'thiếu main_characters')
    if not s['positions']: B(i, 'thiếu positions')
    for r in s['reference_images']:
        if r.get('purpose') not in ('face_only', 'costume_only', 'style_only'): B(i, f'ảnh tham chiếu thiếu mục đích hợp lệ: {r}')
    if len(s['reference_images']) > 2: B(i, 'quá 2 ảnh tham chiếu')
    for k, v in s['bible_versions'].items():
        if CUR.get(k) != v: B(i, f'bible_versions.{k}={v} khác bản hiện hành {CUR.get(k)} (ảnh sẽ STALE)')
    if s['plan_status'] not in ('PLAN_DRAFT', 'PLAN_CHECKED', 'PLAN_OWNER_REVIEW', 'PLAN_APPROVED'): B(i, 'plan_status không hợp lệ')
print(f'Phiên bản hiện hành: {CUR}; {len(sc)} cảnh')
print('\n'.join(bad + warn)); print(f'{len(bad)} lỗi ❌, {len(warn)} cảnh báo ⚠️')
sys.exit(1 if bad else 0)
