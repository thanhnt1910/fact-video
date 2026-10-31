"""Hàm dùng chung cho quy chuẩn ảnh (quy-tac/anh/quy-trinh-anh.md): bible_ref, giới hạn vẽ lại, ảnh tham chiếu được duyệt.
Không gọi mạng, không vẽ ảnh."""
import json, os, re
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
LAN_VE_LAI_TOI_DA = 3            # sau lần vẽ đầu
TONG_LAN = 1 + LAN_VE_LAI_TOI_DA # attempt tối đa = 4
TRANG_THAI_ANH = ('PASS', 'REVIEW', 'REGENERATE', 'MANUAL_REVIEW', 'SUPERSEDED', 'STALE')

def phien_ban_hien_hanh():
    def ver(f):
        m = re.search(r'\(v([\d.]+)', open(f'{R}/quy-tac/anh/{f}', encoding='utf-8').read()); return m.group(1) if m else '?'
    kp = json.load(open(f'{R}/quy-tac/anh/khoi-prompt.json', encoding='utf-8'))
    return {'master': ver('master-style.md'), 'period': ver('period-ly-tong.md'), 'khoi_prompt': str(kp['phien_ban']).split('-')[0]}

def giai_bible_ref(ref):
    """'period-ly-tong#C Mũ' → True nếu file có thật và mục 'C' có dòng bảng bắt đầu bằng 'Mũ'.
    'master-style#1' / 'period-ly-tong#E' → True nếu có mục đó. Trả (ok, lý do)."""
    if not isinstance(ref, str) or '#' not in ref: return False, 'bible_ref phải có dạng "<file>#<mục>"'
    f, m = ref.split('#', 1); path = f'{R}/quy-tac/anh/{f}.md'
    if not os.path.exists(path): return False, f'file {f}.md không tồn tại'
    txt = open(path, encoding='utf-8').read()
    mm = re.match(r'^([A-Z]|\d+)(?:\s+(.+))?$', m.strip())
    if not mm: return False, f'mục "{m}" không đúng dạng (chữ cái hoặc số, rồi tên hạng mục)'
    sec, kw = mm.group(1), mm.group(2)
    parts = re.split(r'(?m)^## ', txt)
    body = next((p for p in parts if re.match(rf'{re.escape(sec)}[.\s]', p)), None)
    if body is None: return False, f'không có mục "{sec}" trong {f}.md'
    if not kw: return True, ''
    for line in body.split('\n'):
        if line.startswith('|'):
            c = line.strip('|').split('|')[0].strip()
            if c.lower().startswith(kw.lower()): return True, ''
    return False, f'mục {sec} của {f}.md không có hạng mục bắt đầu bằng "{kw}"'

def tham_chieu_duoc_duyet(ma):
    p = f'{R}/ke-hoach/anh/{ma}/tham-chieu-duoc-duyet.json'
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'anh': []}

def tham_chieu_hop_le(ma, image_id):
    """Chỉ hợp lệ khi: có trong danh sách chủ kênh duyệt, bản ghi ảnh PASS, và bible_versions khớp phiên bản hiện hành."""
    ds = {x['image_id']: x for x in tham_chieu_duoc_duyet(ma).get('anh', [])}
    if image_id not in ds: return False, f'ảnh {image_id} không có trong tham-chieu-duoc-duyet.json (chưa được chủ kênh duyệt)'
    e = ds[image_id]
    if not e.get('duyet_boi') or not e.get('ngay'): return False, 'thiếu duyet_boi hoặc ngay'
    ap = f'{R}/ke-hoach/anh/{ma}/anh.json'
    rec = next((x for x in json.load(open(ap, encoding='utf-8'))['images'] if x['image_id'] == image_id), None) if os.path.exists(ap) else None
    if not rec: return False, f'ảnh {image_id} không có trong anh.json'
    if rec['status'] != 'PASS': return False, f'ảnh {image_id} có trạng thái {rec["status"]}, chỉ PASS mới làm tham chiếu'
    if rec.get('bible_versions') != phien_ban_hien_hanh(): return False, f'ảnh {image_id} vẽ theo Bible {rec.get("bible_versions")}, khác phiên bản hiện hành (STALE)'
    return True, ''

def quyet_dinh_ve(records, scene_id):
    """Có được vẽ (lần đầu hoặc vẽ lại tự động) không? Trả (mã, lý do). Mã: VE | DA_PASS | MANUAL_REVIEW.
    Bỏ qua ảnh STALE/SUPERSEDED (ảnh trước quy chuẩn)."""
    rs = sorted([r for r in records if r['scene_id'] == scene_id and r['status'] not in ('STALE',)], key=lambda r: r['attempt'])
    if not rs: return 'VE', 'chưa vẽ lần nào (attempt 1)'
    last = rs[-1]
    if last['status'] == 'PASS': return 'DA_PASS', f'attempt {last["attempt"]} đã PASS, không vẽ lại'
    if last['status'] == 'MANUAL_REVIEW' and not last.get('owner_unlock'): return 'MANUAL_REVIEW', 'đã chuyển MANUAL_REVIEW, chờ chủ kênh'
    if last['attempt'] >= TONG_LAN: return 'MANUAL_REVIEW', f'đã {last["attempt"]} lần (1 + {LAN_VE_LAI_TOI_DA} lần vẽ lại), phải chuyển MANUAL_REVIEW'
    return 'VE', f'vẽ lại, sẽ là attempt {last["attempt"] + 1}/{TONG_LAN}'

if __name__ == '__main__':
    import sys
    ma, sid = sys.argv[1], int(sys.argv[2])
    ap = f'{R}/ke-hoach/anh/{ma}/anh.json'
    recs = json.load(open(ap, encoding='utf-8'))['images'] if os.path.exists(ap) else []
    c, why = quyet_dinh_ve(recs, sid); print(c, why); sys.exit(0 if c == 'VE' else 3)
