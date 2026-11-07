"""Kiểm cắt giọng: python phim_ban_do/kiem_cat.py <tên> [--sua]
Tên là mã có hậu tố l (vd vn1l): đọc ke-hoach/thu-giong-hai/<tên>_full.json, phim_ban_do/asr_<tên>.json, assets/thu_giong_hai/<tên>_chuan.
Lỗi 1: >=2 chữ cuối đoạn dính sát hết file (nhận dạng bịa, giọng bị cụt). Lỗi 2: chữ đầu bắt đầu sau 1 giây (lời của đoạn trước tràn sang).
--sua: nối phần tràn (đến chỗ lặng đầu tiên >=0,2 s sau 0,5 s) về cuối đoạn trước, cắt khỏi đoạn này, cập nhật thoi_luong.json, xóa nhận dạng hai đoạn. Thoát mã 3 nếu đã sửa (phải nhận dạng lại), 1 nếu còn lỗi."""
import json, os, re, subprocess, sys
ten = sys.argv[1]; sua = '--sua' in sys.argv
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
kb = json.load(open(f'{R}/ke-hoach/thu-giong-hai/{ten}_full.json', encoding='utf-8'))
ap = f'{R}/phim_ban_do/asr_{ten}.json'; asr = json.load(open(ap, encoding='utf-8'))
VD = f'{R}/assets/thu_giong_hai/{ten}_chuan'; dur = json.load(open(f'{VD}/thoi_luong.json'))
bad = []
for i, b in enumerate(kb):
    n = str(b['n']); w = asr.get(n) or []
    if not w: bad.append((i, n, 'chưa có nhận dạng')); continue
    coll = sum(1 for x in w if x[1] >= dur[n] - .08)
    if coll >= 2: bad.append((i, n, f'{coll} chữ dính cuối file (giọng cụt)'))
    if w[0][1] > 1.0 and i > 0: bad.append((i, n, f'chữ đầu bắt đầu {w[0][1]:.2f}s (lời đoạn trước tràn sang)'))
for _, n, m in bad: print(f'❌ {n}: {m}')
if not bad: print('✅ cắt giọng sạch'); sys.exit(0)
if not sua: sys.exit(1)
done = set()
for i, n, m in bad:
    if 'tràn' not in m: continue
    pn = str(kb[i - 1]['n'])
    sil = subprocess.run(['ffmpeg', '-nostats', '-i', f'{VD}/{n}.mp3', '-af', 'silencedetect=n=-35dB:d=0.2', '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', sil)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', sil)]
    cut = None
    for a, e in zip(st, en):
        if a >= .5: cut = (a, e); break
    if not cut: print(f'⚠ {n}: không tìm thấy chỗ lặng để cắt'); continue
    a, e = cut; mid = (a + e) / 2
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{VD}/{n}.mp3', '-t', f'{a + .05:.3f}', '/tmp/_p.wav'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{VD}/{pn}.mp3', '/tmp/_q.wav'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '/tmp/_q.wav', '-i', '/tmp/_p.wav', '-filter_complex', 'concat=n=2:v=0:a=1', '-b:a', '128k', f'{VD}/_n.mp3'], check=True); os.replace(f'{VD}/_n.mp3', f'{VD}/{pn}.mp3')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{mid:.3f}', '-i', f'{VD}/{n}.mp3', '-b:a', '128k', f'{VD}/_n.mp3'], check=True); os.replace(f'{VD}/_n.mp3', f'{VD}/{n}.mp3')
    for k in (pn, n):
        dur[k] = round(float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{VD}/{k}.mp3'])), 2); asr.pop(k, None); done.add(k)
    print(f'🔧 đã nối phần tràn của {n} (đến {a:.2f}s) về {pn}')
json.dump(dur, open(f'{VD}/thoi_luong.json', 'w')); json.dump(asr, open(ap, 'w'), ensure_ascii=False)
sys.exit(3 if done else 1)
