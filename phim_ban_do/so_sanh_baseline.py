"""So sánh trước/sau khi sửa bộ kiểm (chỉ đọc baseline). python phim_ban_do/so_sanh_baseline.py
1) Chạy bộ test GỐC (tag b0, 44 phép) với mã kiểm MỚI: phải 44/44.
2) Chạy bộ test b1 (70 phép) với mã kiểm MỚI: chỉ 26 phép "quy tắc mới" được phép đổi hành vi (đổi từ chặn sang cảnh báo).
3) Chạy mã kiểm MỚI trên planner/dữ liệu CŨ (b1): đầu ra phải giống từng dòng với baseline.
4) SHA-256 bốn tài liệu APPROVED so với baseline b1."""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BL = json.load(open(f'{R}/phim_ban_do/baseline_kiem/baseline.json', encoding='utf-8'))
def sh(*a, **k): return subprocess.run(a, capture_output=True, text=True, **k)
def extract(tag, d):
    p = subprocess.Popen(['git', 'archive', tag, 'phim_ban_do', 'quy-tac', 'ke-hoach/anh', 'ke-hoach/chibi/lt1t2_chibi.json', 'ke-hoach/thu-giong-hai/lt1v4_full.json', 'cf_ve_lt1t2.py', 'ai_images.py'], cwd=R, stdout=subprocess.PIPE)
    subprocess.run(['tar', '-x', '-C', d], stdin=p.stdout, check=True); p.wait()
def tests(d):
    out = sh(sys.executable, 'phim_ban_do/test_kiem_anh.py', cwd=d).stdout
    return [(m.group(1), m.group(2).split('  ↳')[0].split('  [')[0]) for l in out.splitlines() for m in [re.match(r'(PASS|FAIL) (.*)', l)] if m]
KQ = []
def ghi(ok, s): KQ.append(ok); print(('ĐẠT  ' if ok else 'LỆCH ') + s)
NEW = ['phim_ban_do/kiem_scene_planner.py', 'phim_ban_do/anh_quy_tac.py', 'quy-tac/anh/quyet-dinh.json']
res = {}
for tag in ('b0', 'b1'):
    d = tempfile.mkdtemp(); extract(BL['tag_git'][tag], d)
    for f in NEW:
        os.makedirs(os.path.dirname(f'{d}/{f}'), exist_ok=True); shutil.copy(f'{R}/{f}', f'{d}/{f}')
    res[tag] = tests(d)
    if tag == 'b1':   # đầu ra mã mới trên planner cũ
        base = [l for l in open(f'{R}/phim_ban_do/baseline_kiem/b1_val_out.txt', encoding='utf-8').read().splitlines() if not l.startswith('exit ')]
        reg = f'{d}/quy-tac/anh/quyet-dinh.json'; os.rename(reg, reg + '.tam')
        o = sh(sys.executable, 'phim_ban_do/kiem_scene_planner.py', 'lt1v4', cwd=d).stdout.splitlines()
        ghi(o == base, f'3a. Mã kiểm MỚI (chưa có registry) trên planner/dữ liệu CŨ (b1): đầu ra {"giống hệt" if o == base else "KHÁC"} baseline ({len(base)} dòng)')
        os.rename(reg + '.tam', reg)
        o = sh(sys.executable, 'phim_ban_do/kiem_scene_planner.py', 'lt1v4', cwd=d).stdout.splitlines()
        them = [l for l in o if l not in base and not re.search(r'lỗi ❌', l)]; mat = [l for l in base if l not in o and not re.search(r'lỗi ❌', l)]
        ghi(not mat and all('QK-' in l or 'DQ-' in l for l in them), f'3b. Mã MỚI + registry trên planner CŨ: mất {len(mat)} dòng baseline; thêm {len(them)} dòng, đều là dòng của registry (mã DQ-, planner cũ chưa khai quyet_dinh_ap_dung nên registry báo thiếu liên kết, đúng như thiết kế)')
    shutil.rmtree(d)
b0 = [t for t in BL['baseline']['b0']['tests']]
r0 = res['b0']
ghi(len(r0) == 44 and all(a == 'PASS' for a, _ in r0) and [n for _, n in r0] == [t['ten'] for t in b0], f'1. Bộ test GỐC (b0, {len(r0)} phép) chạy với mã MỚI: {sum(a == "PASS" for a, _ in r0)}/{len(r0)} đạt, cùng tên và thứ tự như baseline')
b1 = {t['ten']: t['ket_qua'] for t in BL['baseline']['b1']['tests']}
r1 = res['b1']
loch = [n.split('  ->')[0].strip() for a, n in r1 if a != b1.get(n)]
ghi(len(r1) == 70 and len(loch) <= 26 and all(re.match(r'(16[b-h]|17[bc]|18[b-e]|19[ab]|20|21[ad]) ', n) for n in loch), f'2. Bộ test b1 (70 phép) với mã MỚI: {len(loch)} phép đổi hành vi (8 phép còn lại trong 26 phép mới là trường hợp hợp lệ, không đổi); cả {len(loch)} đều thuộc nhóm quy tắc mới (voi, bản đồ, đoạn, giữ lâu, duyệt nghệ thuật) chuyển từ chặn sang cảnh báo (Cách B)')
for n in loch: print('     - ' + n[:120])
cur = {f: hashlib.sha256(open(f'{R}/{f}', 'rb').read()).hexdigest() for f in ('quy-tac/anh/master-style.md', 'quy-tac/anh/period-ly-tong.md', 'quy-tac/anh/khoi-prompt.json', 'quy-tac/anh/quy-trinh-anh.md')}
sb = BL['baseline']['b1']['sha256']
for f, h in cur.items(): ghi(h == sb[f], f'4. SHA-256 {f.split("/")[-1]} {"không đổi" if h == sb[f] else "KHÁC baseline"}')
print(f'\nKết luận: {"ĐẠT, hành vi cũ không đổi" if all(KQ) else "CÓ LỆCH, xem các dòng LỆCH"}')
sys.exit(0 if all(KQ) else 1)
