"""Kiểm máy quay trước khi dựng: câu nào nhắc địa danh (trong LOC của nội dung) mà địa danh đó nằm ngoài khung hình
(hoặc bị phụ đề che) ở 25% và 70% thời lượng câu. Cần cùng biến môi trường như mapfilm3 (SCRIPT, VOICE_DIR, CONTENT, WORLD, WORLDMOD...).
Chạy: python kiem_camera.py   -> in danh sách câu lệch; thoát mã 1 nếu có. Sửa bằng FOC.append((câu,câu,[điểm],True)) trong file nội dung."""
import sys, os, json
sys.argv = ['x', 'none']
import mapfilm3 as F
C = F.C; txt = {x['n']: x['text'] for x in json.load(open(os.environ['SCRIPT'], encoding='utf-8'))}
names = [k for k in C.LOC if k not in ('Kế', 'Đàm', 'Ngô', 'Hứa Du')]
bad = 0
for n in sorted(F.T):
    miss = []
    for nm in names:
        if nm in txt[n]:
            lon, lat = C.LOC[nm][:2]
            for fr in (0.25, 0.7):
                x, y = F.View(F.T[n] + F.D[n] * fr).sc(lon, lat, 1)
                if not (60 < x < 1700 and 90 < y < 840): miss.append((nm, fr, int(x), int(y)))
    if miss: bad += 1; print('❌', n - getattr(C, 'BASE', 0), round(F.T[n]), miss[:3])
print(f'{bad} câu có địa danh ngoài khung/dưới phụ đề'); sys.exit(1 if bad else 0)
