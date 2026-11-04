"""Kiểm giọng đọc từng đoạn TRƯỚC KHI dựng: python phim_ban_do/kiem_giong.py <tên> [--xoa] [--nguong 0.9]
So nhận dạng (asr_<tên>.json) với kịch bản (ke-hoach/thu-giong-hai/<tên>_full.json). Đoạn nào khớp dưới ngưỡng, hoặc chưa có nhận dạng, thì in ra;
với --xoa thì xóa đoạn đó khỏi thoi_luong.json, hash.json, mp3 và nhận dạng để đẩy chay.txt đọc lại (cum.txt phải là 1).
Quy trình: đọc từng đoạn -> chạy nhận dạng -> kiem_giong -> (--xoa, đọc lại, nhận dạng lại) đến khi sạch -> mới dựng. Thoát mã 1 nếu còn đoạn lỗi."""
import json, os, sys, difflib, re
tên = sys.argv[1]; xoa = '--xoa' in sys.argv
ng = float(sys.argv[sys.argv.index('--nguong') + 1]) if '--nguong' in sys.argv else 0.9
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
kb = json.load(open(f'{R}/ke-hoach/thu-giong-hai/{tên}_full.json', encoding='utf-8'))
asr = json.load(open(f'{R}/phim_ban_do/asr_{tên}.json', encoding='utf-8'))
VD = f'{R}/assets/thu_giong_hai/puck'
def chuan(t): return re.sub(r'[^\w\s]', ' ', t.lower()).split()
xau = []
for b in kb:
    n = str(b['n']); w = asr.get(n)
    if not w: xau.append((n, 0.0, 'chưa có nhận dạng')); continue
    r = difflib.SequenceMatcher(None, chuan(b['text']), chuan(' '.join(x[0] for x in w))).ratio()
    if r < ng: xau.append((n, r, ' '.join(x[0] for x in w)[:70]))
for n, r, t in xau: print(f'❌ {n}: khớp {r:.0%} | {t}')
print(f'{len(kb) - len(xau)}/{len(kb)} đoạn đạt (ngưỡng {ng:.0%})')
if xau and xoa:
    dur = json.load(open(f'{VD}/thoi_luong.json')); H = json.load(open(f'{VD}/hash.json'))
    for n, _, _ in xau:
        dur.pop(n, None); H.pop(n, None); asr.pop(n, None)
        if os.path.exists(f'{VD}/{n}.mp3'): os.remove(f'{VD}/{n}.mp3')
    json.dump(dur, open(f'{VD}/thoi_luong.json', 'w')); json.dump(H, open(f'{VD}/hash.json', 'w'))
    json.dump(asr, open(f'{R}/phim_ban_do/asr_{tên}.json', 'w', encoding='utf-8'), ensure_ascii=False)
    print('đã xóa', len(xau), 'đoạn; đặt cum.txt = 1 và đẩy chay.txt để đọc lại')
sys.exit(1 if xau else 0)
