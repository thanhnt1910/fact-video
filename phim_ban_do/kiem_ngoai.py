"""Kiểm giọng đọc bằng nhận dạng KHÔNG gợi ý (asr_<tên>_ngoai.json): chữ thừa, chữ mất, lặp ở đầu/cuối câu.
Chạy: python phim_ban_do/kiem_ngoai.py <tên>   -> in danh sách câu nghi lỗi, thoát mã 1 nếu có. Bỏ qua khác dấu thanh và số (nhận dạng hay viết số bằng chữ số)."""
import json, re, sys, unicodedata, difflib
tên = sys.argv[1]; R = __file__.rsplit('/phim_ban_do/', 1)[0] if '/phim_ban_do/' in __file__ else '.'
SO = set('không một hai ba bốn năm sáu bảy tám chín mười mươi mốt tư lăm trăm nghìn linh'.split())
def bd(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower().replace('đ', 'd')) if unicodedata.category(c) != 'Mn')
SO = {bd(x) for x in SO}
def tok(s): return [w for w in re.sub(r'[^\w\s]', ' ', bd(s)).split() if w not in SO and not w.isdigit()]
asr = json.load(open(f'{R}/phim_ban_do/asr_{tên}_ngoai.json', encoding='utf-8'))
kb = {str(x['n']): x['text'] for x in json.load(open(f'{R}/ke-hoach/thu-giong-hai/{tên}_full.json', encoding='utf-8'))}
bad = []
for n, t in kb.items():
    s = tok(t); h = tok(' '.join(w[0] for w in asr.get(n, [])))
    if not h: bad.append((n, 'chưa có nhận dạng')); continue
    sm = difflib.SequenceMatcher(None, s, h, autojunk=False); r = sm.ratio(); why = []
    ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
    for op, i1, i2, j1, j2 in ops:
        if j2 - j1 >= 3 and i2 - i1 == 0 or (j1 == 0 and j2 - j1 >= 2 and i1 == 0) or (j2 == len(h) and j2 - j1 >= 2 and i2 == len(s)):
            why.append(f'thừa {" ".join(h[j1:j2])!r} ở {"đầu" if j1 == 0 else "cuối" if j2 == len(h) else "giữa"}')
        if i2 - i1 >= 3 and j2 - j1 == 0: why.append(f'mất {" ".join(s[i1:i2])!r}')
    if len(h) - len(s) >= 3: why.append(f'nhiều hơn kịch bản {len(h) - len(s)} chữ')
    if r < 0.7: why.append(f'khớp {r:.0%}')
    if why: bad.append((n, '; '.join(why)))
for n, w in bad: print('❌', n, w)
print(f'{len(kb) - len(bad)}/{len(kb)} câu sạch'); sys.exit(1 if bad else 0)
