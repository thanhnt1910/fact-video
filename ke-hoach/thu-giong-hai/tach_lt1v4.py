"""Tách đoạn dài của lt1v4 theo yêu cầu chủ kênh 01/11/2026: GIỮ NGUYÊN CÂU CHỮ (không thêm, bớt, đổi từ).
Chỉ được: (1) cắt đoạn tại ranh giới câu hoặc dấu phẩy, viết hoa chữ đầu đoạn mới; (2) đổi dấu hai chấm/chấm phẩy thành dấu phẩy
(bộ kiểm cấm hai ký tự này vì giọng đọc dễ đọc sai). Không ghi đè lt1v4_full.json.
python ke-hoach/thu-giong-hai/tach_lt1v4.py  ->  lt1v4_tach_full.json + lt1v4_tach_anh-xa.json"""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__))
src = json.load(open(f'{D}/lt1v4_full.json', encoding='utf-8'))
# n cũ -> danh sách đoạn mới (mỗi đoạn là chuỗi). Chuỗi nguồn được cắt bằng dấu '|' đặt tại chỗ cắt
CAT = {
 20005: ('Người đó là Lý Thường Kiệt, thái úy triều Lý. Trước mắt ông là hai câu hỏi sinh tử, nên chờ hay đánh trước, và nếu đánh thì phải đánh vào đâu?',),
 20008: (None, '|'), 20009: (None, '|'), 20010: (None, '|'), 20011: (None, '|'), 20016: (None, '|'), 20018: (None, '|'), 20019: (None, '|'),
 20023: (None, '|'), 20027: (None, '|'), 20030: (None, '|'), 20033: (None, '|'), 20039: (None, '|'), 20043: (None, '|'), 20045: (None, '|'),
 20048: (None, '|'), 20051: (None, '|'), 20056: (None, '|'), 20063: (None, '|'),
}
COM = {20013: 'ch', 20017: 'ch', 20020: 'ch', 20025: 'ch', 20047: 'ch', 20067: 'ch'}   # chỉ đổi ':' ';' -> ','
def cau(t): return [s for s in re.split(r'(?<=[.!?])\s+', t.strip()) if s]
out, amap = [], {}
def them(old, x, texts):
    ids = []
    for t in texts:
        n = 20001 + len(out); out.append(dict(n=n, chuong=x['chuong'], tone=x['tone'], text=t)); ids.append(n)
    amap[str(old)] = ids
for x in src:
    n, t = x['n'], x['text'].strip()
    if n in COM or n == 20005: t = re.sub(r'\s*[:;]\s*', ', ', t)          # đổi dấu, không đổi từ
    if n in CAT and CAT[n][-1] == '|':
        s = cau(t); assert len(s) == 2, n; them(n, x, s)
    elif n == 20054:
        a, b = t.split(', đồng thời ', 1); them(n, x, [a + '.', 'Đồng thời ' + b])
    elif n == 20062:
        s = cau(t); a, b = s[1].split(', còn ', 1); them(n, x, [s[0] + ' ' + a + '.', 'Còn ' + b])
    elif n == 20064:
        s = cau(t); a, b = s[1].split(', khép lại ', 1); them(n, x, [s[0] + ' ' + a + '.', 'Khép lại ' + b])
    else: them(n, x, [t])
# kiểm: ghép lại phải ra đúng các từ ban đầu (bỏ dấu câu, không phân biệt hoa thường)
norm = lambda s: re.sub(r'[^\w\s]', '', s.lower()).split()
for old, ids in amap.items():
    o = next(y for y in src if y['n'] == int(old))['text']; nw = ' '.join(next(y for y in out if y['n'] == i)['text'] for i in ids)
    assert norm(o) == norm(nw), (old, o, nw)
json.dump(out, open(f'{D}/lt1v4_tach_full.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(dict(ghi_chu='Ánh xạ số thứ tự đoạn: khóa là n cũ (lt1v4_full.json), giá trị là n mới (lt1v4_tach_full.json). Từ ngữ không đổi (đã kiểm bằng so sánh từ).', ds_cu_sang_moi=amap,
               vi_tri_cu_sang_moi={str(i + 1): [m - 20000 for m in amap[str(x['n'])]] for i, x in enumerate(src)}), open(f'{D}/lt1v4_tach_anh-xa.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(src), 'đoạn cũ ->', len(out), 'đoạn mới')
