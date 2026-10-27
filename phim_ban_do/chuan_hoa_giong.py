"""Chuẩn hóa giọng đọc từng đoạn (làm trên bản sao, không tốn hạn mức Gemini): python phim_ban_do/chuan_hoa_giong.py <tên> [--nguon assets/thu_giong_hai/puck]
Quy tắc ở quy-tac/su-viet.md: atempo về tốc độ trung vị (chỉ khi lệch quá 5%, giới hạn 0,90–1,10), loudnorm I=-16:TP=-1.5:LRA=11,
chỉnh độ lợi về đúng -16 LUFS, alimiter=0.89. Ghi assets/thu_giong_hai/<tên>_chuan/<n>.mp3 và thoi_luong.json mới. In bảng tốc độ và âm lượng theo nhóm."""
import json, os, re, subprocess, sys, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from kiem_cao_do import doc as _doc, f0_trung_vi as _f0
TRIM = json.load(open(f'ke-hoach/thu-giong-hai/{sys.argv[1]}_cat_duoi.json')) if os.path.exists(f'ke-hoach/thu-giong-hai/{sys.argv[1]}_cat_duoi.json') else {}  # n -> giây (mốc nhận dạng trên bản chuẩn) cắt bỏ phần đọc thừa sau đó
ten = sys.argv[1]
nguon = sys.argv[sys.argv.index('--nguon') + 1] if '--nguon' in sys.argv else 'assets/thu_giong_hai/puck'
kb = json.load(open(f'ke-hoach/thu-giong-hai/{ten}_full.json', encoding='utf-8'))
dst = f'assets/thu_giong_hai/{ten}_chuan'; os.makedirs(dst, exist_ok=True)
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip())
def lufs(p):
    r = subprocess.run(['ffmpeg','-nostats','-i',p,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    m = re.findall(r'I:\s+(-?[\d.]+) LUFS', r); return float(m[-1]) if m else -23.0
nw = {b['n']: len(re.sub(r'[^\w\s]', ' ', b['text']).split()) for b in kb}
d0 = {b['n']: dur(f'{nguon}/{b["n"]}.mp3') for b in kb}
wps = {n: nw[n] / d0[n] for n in nw}
med = statistics.median(wps.values())
f0 = {n: _f0(_doc(f'{nguon}/{n}.mp3')) for n in nw}
f0m = statistics.median(v for v in f0.values() if v == v)
print(f'cao độ trung vị {f0m:.0f} Hz')
print(f'tốc độ trung vị {med:.2f} chữ/giây')
out = {}; rep = []
for b in kb:
    n = b['n']; src = f'{nguon}/{n}.mp3'; dp = f'{dst}/{n}.mp3'
    r = wps[n] / med; tempo = 1.0
    if abs(r - 1) > 0.05: tempo = max(0.90, min(1.10, r))   # nhanh hơn trung vị thì làm chậm (atempo<1) hay ngược lại: atempo = r làm giọng nhanh lên khi r>1
    tempo = 1 / r if abs(r - 1) > 0.05 else 1.0
    tempo = max(0.90, min(1.10, tempo))
    tmp = f'/tmp/_ch_{n}.wav'
    pr = 1.0
    if f0[n] == f0[n] and abs(f0m / f0[n] - 1) > 0.03: pr = max(0.90, min(1.10, f0m / f0[n]))   # kéo cao độ từng đoạn về trung vị (tối đa 10%), giữ nguyên tốc độ
    cut = ''
    if str(n) in TRIM: cut = f'atrim=end={TRIM[str(n)] * tempo:.3f},'
    af = f'{cut}rubberband=tempo={tempo:.4f}:pitch={pr:.4f}:formant=preserved,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=none'
    subprocess.run(['ffmpeg','-y','-v','error','-i',src,'-af',af,'-ar','24000','-ac','1',tmp],check=True)
    L = lufs(tmp); g = -16.0 - L
    subprocess.run(['ffmpeg','-y','-v','error','-i',tmp,'-af',f'volume={g:.2f}dB,alimiter=limit=0.89','-ar','24000','-ac','1','-b:a','96k',dp],check=True)
    os.remove(tmp)
    out[str(n)] = round(dur(dp), 3); rep.append((n, wps[n], tempo, L, lufs(dp)))
json.dump(out, open(f'{dst}/thoi_luong.json', 'w'))
ws = [wps[n] / (1 / next(t for m, w, t, l1, l2 in rep if m == n)) for n in nw]
print('đoạn đã chỉnh tốc độ:', sum(1 for _, _, t, _, _ in rep if abs(t - 1) > 1e-3), '/', len(rep))
print(f'âm lượng sau chuẩn hóa: {min(r[4] for r in rep):.1f} đến {max(r[4] for r in rep):.1f} LUFS')
tong = sum(out.values()); print(f'tổng thời lượng giọng {tong/60:.2f} phút')
