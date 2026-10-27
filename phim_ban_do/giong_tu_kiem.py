"""Giọng đọc tự kiểm trong một lần chạy: python phim_ban_do/giong_tu_kiem.py <tên> [số vòng, mặc định 2]
Mỗi vòng: chuẩn hóa giọng -> nhận dạng KHÔNG gợi ý (chỉ đoạn mới/đổi) -> kiem_ngoai (chữ thừa/mất/lặp) và kiem_giong -> đoạn lỗi thì xóa
giọng thô và đọc lại riêng từng đoạn (cum=1, tốn ít lượt Gemini nhất) -> vòng sau kiểm lại. Cuối cùng ghi báo cáo văn bản logs/giong_tu_kiem_<tên>.md."""
import json, os, re, subprocess, sys
ten = sys.argv[1]; vong_max = int(sys.argv[2]) if len(sys.argv) > 2 else 2
P = 'python'; TG = 'ke-hoach/thu-giong-hai'; RAW = 'assets/thu_giong_hai/puck'
def run(*a, check=False):
    r = subprocess.run(a, capture_output=True, text=True); print('$', ' '.join(a), '->', r.returncode, flush=True)
    if r.stdout: print(r.stdout[-3000:])
    if r.stderr and r.returncode: print(r.stderr[-1500:])
    return r
def xoa(n):
    for f in (f'{RAW}/{n}.mp3',): 
        if os.path.exists(f): os.remove(f)
    for f in (f'{RAW}/thoi_luong.json', f'{RAW}/hash.json'):
        if os.path.exists(f):
            d = json.load(open(f)); d.pop(str(n), None); json.dump(d, open(f, 'w'))
    for f in (f'phim_ban_do/asr_{ten}.json', f'phim_ban_do/asr_{ten}_ngoai.json'):
        if os.path.exists(f):
            d = json.load(open(f)); d.pop(str(n), None); json.dump(d, open(f, 'w'), ensure_ascii=False)
rep = [f'# Tự kiểm giọng {ten}\n']; con_loi = []
for v in range(1, vong_max + 1):
    run(P, 'phim_ban_do/chuan_hoa_giong.py', ten)
    run(P, 'phim_ban_do/phude_asr.py', f'{TG}/{ten}_full.json', f'assets/thu_giong_hai/{ten}_chuan', f'phim_ban_do/asr_{ten}.json', 'medium', 'khong_goi_y')
    r = run(P, 'phim_ban_do/kiem_ngoai.py', ten)
    bad = {}
    for l in r.stdout.splitlines():
        m = re.match(r'❌ (\d+) (.*)', l)
        if m: bad[m.group(1)] = m.group(2)
    rep.append(f'## Vòng {v}: {len(bad)} đoạn nghi lỗi')
    rep += [f'- {n}: {w}' for n, w in bad.items()]
    con_loi = bad
    if not bad or v == vong_max: break
    for n in bad: xoa(n)
    open(f'{TG}/cum.txt', 'w').write('1')
    r = run(P, 'thu_giong_hai_cum.py', f'{TG}/{ten}_full.json', 'Puck', 'assets/thu_giong_hai', '1')
    rep.append(f'(đã đọc lại {len(bad)} đoạn riêng; thoát mã {r.returncode})')
rep.append('\n## Kết quả cuối\n' + ('Sạch.' if not con_loi else 'Còn nghi lỗi (có thể do nhận dạng nghe nhầm, nên nghe lại): ' + ', '.join(f'{n} ({w})' for n, w in con_loi.items())))
os.makedirs('logs', exist_ok=True); open(f'logs/giong_tu_kiem_{ten}.md', 'w', encoding='utf-8').write('\n'.join(rep) + '\n'); print('\n'.join(rep))
