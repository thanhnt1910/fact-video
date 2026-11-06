"""Dựng video dọc 9:16 kiểu bản đồ phủ kín khung (series "Cách họ cai trị").
python phim_ban_do/dung_9x16.py <tên> <thư mục giọng đã chuẩn hóa> <ra.mp4> [--thu <giây>] [--nproc 4]
Trang dựng: phim_ban_do/doc9x16/trang.html (hàm render(t)); mốc thời gian theo thoi_luong.json của giọng thật.
Mỗi khung chụp bằng Chromium (playwright), ghép bằng ffmpeg; âm thanh: các đoạn giọng nối cách nhau 0,4 giây."""
import json, os, subprocess, sys
from pathlib import Path
ten, vd, out = sys.argv[1], sys.argv[2], sys.argv[3]
thu = float(sys.argv[sys.argv.index('--thu') + 1]) if '--thu' in sys.argv else None
nproc = int(sys.argv[sys.argv.index('--nproc') + 1]) if '--nproc' in sys.argv else 4
R = Path(__file__).resolve().parent.parent
D = R / 'phim_ban_do' / 'doc9x16'
kb = json.load(open(R / f'ke-hoach/thu-giong-hai/{ten}_full.json', encoding='utf-8'))
dur = json.load(open(Path(vd) / 'thoi_luong.json'))
GAP, T0, FPS = 0.4, 0.3, 24
thieu = [b['n'] for b in kb if str(b['n']) not in dur]
if thieu: sys.exit(f'Thiếu giọng các đoạn: {thieu}')
(D / 'data.js').write_text('const SCRIPT=' + json.dumps([{'n': b['n'], 'text': b.get('hien', b['text'])} for b in kb], ensure_ascii=False) +
                           ';\nwindow.DURS=' + json.dumps({str(b['n']): dur[str(b['n'])] for b in kb}) + ';\n', encoding='utf-8')
# âm thanh: đặt từng đoạn đúng mốc của trang dựng
t, lst = T0, []
for b in kb:
    lst.append((t, Path(vd) / f'{b["n"]}.mp3')); t += dur[str(b['n'])] + GAP
total = t + 1.2
inp, flt = [], []
for i, (st, p) in enumerate(lst):
    inp += ['-i', str(p)]; flt.append(f'[{i}]adelay={int(st*1000)}:all=1[a{i}]')
flt.append(''.join(f'[a{i}]' for i in range(len(lst))) + f'amix=inputs={len(lst)}:normalize=0:duration=longest,apad=whole_dur={total:.2f}[m]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inp, '-filter_complex', ';'.join(flt), '-map', '[m]', '-t', f'{total:.2f}', '-ar', '44100', '-ac', '2', str(D / 'giong.wav')], check=True)
# tiếng hiệu ứng: lấy sự kiện từ trang dựng, tổng hợp, trộn bằng sidechain (tự hạ khi có giọng đọc)
sfx_ok = '--khong-sfx' not in sys.argv
if sfx_ok:
    sys.path.insert(0, str(D)); import sfx
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--allow-file-access-from-files']); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto('file://' + str(D / 'trang.html')); pg.wait_for_timeout(500); ev = pg.evaluate('window.SFX||[]'); br.close()
    sfx.write(str(D / 'sfx.wav'), sfx.render(ev, total), total)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(D / 'giong.wav'), '-i', str(D / 'sfx.wav'), '-filter_complex',
        '[0]asplit[v1][v2];[1][v1]sidechaincompress=threshold=0.02:ratio=4:attack=12:release=300:makeup=1[d];[v2][d]amix=inputs=2:normalize=0:duration=first[m]',
        '-map', '[m]', '-ar', '44100', '-ac', '2', str(D / 'tron.wav')], check=True)
    print('tiếng hiệu ứng:', len(ev), 'sự kiện')
AUD = 'tron.wav' if sfx_ok else 'giong.wav'
N = int(total * FPS) if thu is None else int(thu * FPS)
# khung hình
RECS = r'''
import sys, subprocess
from playwright.sync_api import sync_playwright
a, b, outp, page = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
with sync_playwright() as p:
    br = p.chromium.launch(args=['--allow-file-access-from-files']); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('pageerror', lambda e: print('LỖI TRANG', e)); pg.goto('file://' + page); pg.wait_for_timeout(800)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '24', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-crf', '19', outp], stdin=subprocess.PIPE)
    for i in range(a, b):
        pg.evaluate(f'render({i/24})'); ff.stdin.write(pg.screenshot(type='jpeg', quality=93))
    ff.stdin.close(); ff.wait()
'''
(D / '_rec.py').write_text(RECS)
q = (N + nproc - 1) // nproc
procs = []
for i in range(nproc):
    a, b = i * q, min(N, (i + 1) * q)
    if a < b: procs.append(subprocess.Popen([sys.executable, str(D / '_rec.py'), str(a), str(b), str(D / f'p{i}.mp4'), str(D / 'trang.html')]))
for p in procs:
    if p.wait(): sys.exit('Chụp khung lỗi')
(D / 'list.txt').write_text(''.join(f"file '{D / f'p{i}.mp4'}'\n" for i in range(len(procs))))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(D / 'list.txt'), '-i', str(D / AUD), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', out], check=True)
print('xong', out, f'{total:.1f} giây')
