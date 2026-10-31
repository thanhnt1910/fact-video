"""Kiểm Scene Planner và sổ ảnh (quy-tac/anh/quy-trinh-anh.md).
python phim_ban_do/kiem_scene_planner.py <mã video> [--file planner.json] [--anh anh.json]
Đọc ke-hoach/anh/<mã>/scene-planner.json và anh.json. Thoát mã 1 nếu có ❌. Không gọi mạng, không vẽ ảnh."""
import hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anh_quy_tac as Q
R = Q.R
ma = sys.argv[1]
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
fp = arg('--file', f'{R}/ke-hoach/anh/{ma}/scene-planner.json')
ap = arg('--anh', f'{R}/ke-hoach/anh/{ma}/anh.json')
KP = json.load(open(f'{R}/quy-tac/anh/khoi-prompt.json', encoding='utf-8'))
TAGS = {'historical_evidence': 0, 'cautious_reconstruction': 1, 'artistic_choice': 2}
CUR = Q.phien_ban_hien_hanh()
BIEN = 1800
SO = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12}
CAM = [(r'conical|bamboo hat', 'VN_NON_DAN_PHU'), (r'flag|pennant|banner', 'VN_CO'), (r'\bsacks?\b', None), (r'lantern', None),
       (r'\bcap\b|peaked', None), (r'uniform', None), (r'\bgun|rifle|musket', None), (r'\bstar\b', None)]
bad, warn = [], []
B = lambda i, m: bad.append(f'❌ {i}: {m}')
W = lambda i, m: warn.append(f'⚠️ {i}: {m}')
BB = ['scene_id', 'segment_ids', 'scene_type', 'expected_people', 'expected_horses', 'main_characters', 'positions', 'groups', 'composition', 'camera',
      'lighting', 'blocks_used', 'detail_tags', 'free_text_details', 'image_prompt', 'prompt_sha256', 'prompt_version', 'bible_versions', 'plan_status', 'reference_images']

def kiem_canh(s):
    i = s.get('scene_id', '?')
    miss = [k for k in BB if k not in s]
    for k in miss: B(i, f'thiếu trường {k}')
    if miss: return
    p = s['image_prompt']
    if hashlib.sha256(p.encode()).hexdigest() != s['prompt_sha256']: B(i, 'prompt_sha256 không khớp prompt')
    if len(p) > BIEN: B(i, f'prompt {len(p)} ký tự (tối đa {BIEN} cho klein)')
    if KP['STYLE']['text'] not in p: B(i, 'prompt thiếu nguyên văn khối STYLE')
    if s['expected_people'] and KP['ANATOMY']['text'] not in p: B(i, 'cảnh có người nhưng thiếu nguyên văn khối ANATOMY')
    if s['free_text_details']: B(i, f'free_text_details không rỗng: {s["free_text_details"]} (chỉ được dùng sau khi chủ kênh duyệt)')
    used = set(s['blocks_used'])
    for b in used:
        if b not in KP or not isinstance(KP[b], dict): B(i, f'khối {b} không có trong khoi-prompt.json')
    # --- detail_tags
    tagged = {}
    for t in s['detail_tags']:
        miss = [k for k in ('item', 'block', 'tag', 'evidence_level', 'bible_ref') if k not in t]
        if miss: B(i, f'detail_tags thiếu {miss}: {t}'); continue
        b, tg = t['block'], t['tag']
        ok, why = Q.giai_bible_ref(t['bible_ref'])
        if not ok: B(i, f'bible_ref "{t["bible_ref"]}" của "{t["item"]}" không tồn tại: {why}')
        if b not in used: B(i, f'detail_tags nhắc khối {b} không nằm trong blocks_used')
        if tg not in TAGS: B(i, f'nhãn "{tg}" không hợp lệ (chỉ historical_evidence, cautious_reconstruction, artistic_choice)'); continue
        kb = KP.get(b)
        if isinstance(kb, dict):
            if TAGS[tg] < TAGS.get(kb['tag'], 9): B(i, f'nhãn {tg} của "{t["item"]}" mạnh hơn nhãn của khối {b} ({kb["tag"]})')
            if t['evidence_level'] != kb.get('evidence_level'): B(i, f'evidence_level của "{t["item"]}" ({t["evidence_level"]}) khác mức gốc của khối {b} ({kb.get("evidence_level")}); không được gộp hay đổi mức')
        tagged[b] = tg
    for b in used:
        if b in KP and isinstance(KP[b], dict) and KP[b]['tag'] != 'style_rule' and b not in tagged: B(i, f'khối {b} (mức {KP[b]["evidence_level"]}) chưa có trong detail_tags')
    for pat, blk in CAM:
        if re.search(pat, p, re.I) and (blk is None or blk not in used):
            B(i, f'prompt có "{pat}" nhưng cảnh không dùng khối cho phép ({blk or "không có khối nào"}) → chi tiết tự suy diễn')
    # --- nhóm, số người, số ngựa (kiểm tương tự nhau)
    g = s['groups']
    if not isinstance(g, list) or not g: B(i, 'groups rỗng: phải khai nhóm nhân vật')
    else:
        for x in g:
            for k in ('name', 'count', 'position', 'role', 'horses', 'mounted'):
                if k not in x: B(i, f'groups thiếu {k}: {x}')
            if x.get('mounted', 0) > x.get('count', 0): B(i, f'nhóm "{x.get("name")}": mounted ({x.get("mounted")}) lớn hơn count ({x.get("count")})')
            if x.get('mounted', 0) != x.get('horses', 0): B(i, f'nhóm "{x.get("name")}": mỗi kỵ binh một ngựa nhưng mounted={x.get("mounted")} khác horses={x.get("horses")}')
        sp, sh = sum(x.get('count', 0) for x in g), sum(x.get('horses', 0) for x in g)
        if sp != s['expected_people']: B(i, f'tổng count các nhóm ({sp}) khác expected_people ({s["expected_people"]})')
        if sh != s['expected_horses']: B(i, f'tổng horses các nhóm ({sh}) khác expected_horses ({s["expected_horses"]})')
    if not s['main_characters']: B(i, 'thiếu main_characters')
    if not s['positions']: B(i, 'thiếu positions')
    n = s['expected_horses']
    if n:
        m = re.search(r'EXACTLY (\w+) horses', p)
        if not m: B(i, f'expected_horses={n} nhưng prompt không có "EXACTLY N horses"')
        else:
            v = m.group(1); v = int(v) if v.isdigit() else SO.get(v.lower())
            if v != n: B(i, f'prompt ghi EXACTLY {m.group(1)} horses nhưng expected_horses={n}')
    elif re.search(r'horse|cavalry|mounted', p, re.I): B(i, 'expected_horses=0 nhưng prompt nhắc ngựa hoặc kỵ binh')
    # --- ảnh tham chiếu: chỉ ảnh được chủ kênh duyệt và còn hợp lệ
    if len(s['reference_images']) > 2: B(i, 'quá 2 ảnh tham chiếu')
    for r in s['reference_images']:
        if r.get('purpose') not in ('face_only', 'costume_only', 'style_only'): B(i, f'ảnh tham chiếu thiếu mục đích hợp lệ: {r}')
        ok, why = Q.tham_chieu_hop_le(ma, r.get('image_id'))
        if not ok: B(i, f'ảnh tham chiếu không hợp lệ: {why}')
    for k, v in s['bible_versions'].items():
        if CUR.get(k) != v: B(i, f'bible_versions.{k}={v} khác bản hiện hành {CUR.get(k)} (ảnh sẽ STALE)')
    if s['plan_status'] not in ('PLAN_DRAFT', 'PLAN_CHECKED', 'PLAN_OWNER_REVIEW', 'PLAN_APPROVED'): B(i, 'plan_status không hợp lệ')

def kiem_anh(recs, planner):
    """Sổ ảnh: số người/ngựa thực tế ghi riêng, giới hạn vẽ lại, ảnh tham chiếu."""
    plan = {s['scene_id']: s for s in planner}
    by = {}
    for r in recs:
        i = r.get('image_id', '?')
        for k in ('image_id', 'scene_id', 'attempt', 'status', 'bible_versions', 'prompt_sha256'):
            if k not in r: B(i, f'bản ghi ảnh thiếu {k}')
        if r.get('status') not in Q.TRANG_THAI_ANH: B(i, f'status "{r.get("status")}" không hợp lệ'); continue
        if r['status'] in ('STALE', 'SUPERSEDED'): continue
        by.setdefault(r['scene_id'], []).append(r)
        d, kh = r.get('dem_thu_cong'), r.get('ke_hoach')
        if r['status'] in ('PASS', 'REVIEW', 'REGENERATE', 'MANUAL_REVIEW'):
            if not d or any(k not in d for k in ('nguoi', 'ngua', 'nguoi_dem', 'ngay')): B(i, 'thiếu dem_thu_cong {nguoi, ngua, nguoi_dem, ngay}: số thực tế phải ghi riêng')
            if not kh or any(k not in kh for k in ('nguoi', 'ngua')): B(i, 'thiếu ke_hoach {nguoi, ngua}: bản chụp số lượng dự kiến tại lúc vẽ')
        if d and kh:
            if d is kh or (d.get('nguoi') == kh.get('nguoi') and d.get('ngua') == kh.get('ngua') and not d.get('nguoi_dem')): B(i, 'dem_thu_cong trùng ke_hoach và không có người đếm: nghi ghi đè số dự kiến')
            if r['status'] == 'PASS' and (d['nguoi'] != kh['nguoi'] or d['ngua'] != kh['ngua']): B(i, f'PASS nhưng số thực tế (người {d["nguoi"]}, ngựa {d["ngua"]}) khác dự kiến (người {kh["nguoi"]}, ngựa {kh["ngua"]})')
        if r['scene_id'] in plan and kh:
            s = plan[r['scene_id']]
            if (kh['nguoi'], kh['ngua']) != (s['expected_people'], s['expected_horses']): W(i, 'ke_hoach trong bản ghi khác expected_* hiện tại của planner (planner đã đổi sau khi vẽ?)')
        for ref in r.get('reference_images', []) or []:
            ok, why = Q.tham_chieu_hop_le(ma, ref.get('image_id') if isinstance(ref, dict) else ref)
            if not ok: B(i, f'dùng ảnh tham chiếu không hợp lệ: {why}')
    for sid, rs in by.items():
        rs.sort(key=lambda r: r['attempt'])
        if rs[-1]['attempt'] > Q.TONG_LAN and not any(r.get('owner_unlock') for r in rs): B(f'cảnh {sid}', f'attempt {rs[-1]["attempt"]} vượt {Q.TONG_LAN} (1 lần đầu + {Q.LAN_VE_LAI_TOI_DA} lần vẽ lại) khi chưa có owner_unlock')
        for r in rs:
            if r['attempt'] == Q.TONG_LAN and r['status'] not in ('PASS', 'MANUAL_REVIEW'): B(r['image_id'], f'attempt {Q.TONG_LAN} chưa PASS thì phải là MANUAL_REVIEW, đang là {r["status"]}')
        for a, b in zip(rs, rs[1:]):
            if a['status'] == 'MANUAL_REVIEW' and not (a.get('owner_unlock') or b.get('owner_unlock')): B(b['image_id'], 'vẽ tiếp sau MANUAL_REVIEW khi chưa có owner_unlock')

if __name__ == '__main__':
    d = json.load(open(fp, encoding='utf-8')) if os.path.exists(fp) else []
    sc = d['scenes'] if isinstance(d, dict) else d
    for s in sc: kiem_canh(s)
    if os.path.exists(ap): kiem_anh(json.load(open(ap, encoding='utf-8'))['images'], sc)
    print(f'Phiên bản hiện hành: {CUR}; {len(sc)} cảnh')
    print('\n'.join(bad + warn)); print(f'{len(bad)} lỗi ❌, {len(warn)} cảnh báo ⚠️')
    sys.exit(1 if bad else 0)
