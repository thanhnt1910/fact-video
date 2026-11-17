#!/usr/bin/env python3
"""Kiểm giọng văn theo quy-tac/thuy-mac-giong-van.md.
Cách dùng: python phim_ban_do/kiem_giong_van.py <mã>   (đọc ke-hoach/thu-giong-hai/<mã>_full.json)"""
import json, os, re, sys, statistics
CUM = {'Đúng lúc ấy': 2, 'Vì thế': 2, 'Vì vậy': 2, 'Thế là': 2, 'Đó là': 2, 'Trong khi đó': 2, 'Trong lúc ấy': 2,
       'Cùng lúc ấy': 2, 'Lập tức': 2, 'tưởng như': 2, 'Rồi': 3, 'Còn': 3, 'Nhưng': 4}
TOM = ['đánh tan', 'tan vỡ', 'đánh bại', 'thắng lớn', 'giành chiến thắng', 'đánh tơi tả', 'bị đánh tan']

def cau(t): return [s for s in re.split(r'(?<=[.?!])\s+', t.strip()) if s]

def main(ma):
    p = os.path.join(os.path.dirname(__file__), '..', 'ke-hoach', 'thu-giong-hai', f'{ma}_full.json')
    J = json.load(open(p, encoding='utf-8')); loi, canh = [], []
    C = [s for d in J for s in cau(d['text'])]
    for c, gh in CUM.items():
        n = sum(1 for s in C if s.startswith(c)) if c[0].isupper() else sum(s.count(c) for s in C)
        if n > gh: loi.append(f'❌ cụm "{c}" dùng {n} lần (tối đa {gh})')
    n = sum(s.lower().count(w) for s in C for w in TOM)
    if n > 3: loi.append(f'❌ động từ tóm lược ({", ".join(TOM)}) dùng {n} lần (tối đa 3)')
    L = [len(s.split()) for s in C]
    sd = statistics.pstdev(L)
    print(f'== {ma}: {len(C)} câu, trung bình {statistics.mean(L):.1f} chữ, độ lệch {sd:.1f}, câu dưới 8 chữ: {sum(x < 8 for x in L)}')
    if sd < 5.5: canh.append(f'⚠️ nhịp câu đều (độ lệch {sd:.1f}, nên ≥5,5)')
    if all('nhip' in d for d in J):
        cao = [s for d in J if d['nhip'] in ('lang', 'cao_trao', 'chi_tiet_nguoi') for s in cau(d['text'])]
        if not any(len(s.split()) < 8 for s in cao): loi.append('❌ khối cao trào thiếu câu ngắn dưới 8 chữ để nhấn')
    # mở đầu hai đoạn liền nhau bằng cùng ba chữ
    for a, b in zip(J, J[1:]):
        if a['text'].split()[:3] == b['text'].split()[:3]: canh.append(f'⚠️ {a["n"]}, {b["n"]}: mở đầu giống nhau')
    for x in loi + canh: print(x)
    print(f'   -> {len(loi)} ❌, {len(canh)} ⚠️')
    return 1 if loi else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
