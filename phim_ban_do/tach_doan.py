"""Tách đoạn giọng dài thành đoạn ngắn bằng cách CẮT file giọng đã đạt (dùng mốc từng chữ của nhận dạng), không đọc lại bằng Gemini.
python phim_ban_do/tach_doan.py <tên> [--toi_thieu 14] [--toi_da 32] [--thu]
Đầu vào: ke-hoach/thu-giong-hai/<tên>_full.json, phim_ban_do/asr_<tên>.json, assets/thu_giong_hai/puck/*.mp3 (nên chạy kiem_giong.py sạch trước).
Kết quả: ghi đè <tên>_full.json (đánh số lại liên tục từ số đầu), mp3, thoi_luong.json, hash.json, asr_<tên>.json; ghi bảng ánh xạ cũ -> mới vào ke-hoach/thu-giong-hai/<tên>_tach.json
({"cu": [số mới đầu, số mới cuối]}) để file nội dung bản đồ đổi theo. Bản gốc cất ở ke-hoach/thu-giong-hai/<tên>_full_truoc_tach.json."""
import json, os, re, sys, subprocess, difflib, hashlib, shutil
import numpy as np
tên = sys.argv[1]; thu = '--thu' in sys.argv
def opt(k, d): return int(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
MIN, MAX = opt('--toi_thieu', 14), opt('--toi_da', 32)
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
FP = f'{R}/ke-hoach/thu-giong-hai/{tên}_full.json'; VD = f'{R}/assets/thu_giong_hai/puck'; AP = f'{R}/phim_ban_do/asr_{tên}.json'
beats = json.load(open(FP, encoding='utf-8')); asr = json.load(open(AP, encoding='utf-8'))
dur = json.load(open(f'{VD}/thoi_luong.json')); H = json.load(open(f'{VD}/hash.json'))
SR = 44100
def norm(w): return re.sub(r'[^\w]', '', w.lower())
def nw(t): return len(t.split())
def groups(text):
    ss = [s for s in re.split(r'(?<=[.!?…])\s+', text.strip()) if s]
    out, cur = [], []
    for s in ss:
        if cur and (nw(' '.join(cur)) >= MIN or nw(' '.join(cur)) + nw(s) > MAX): out.append(cur); cur = []
        cur.append(s)
    if cur:
        if out and nw(' '.join(cur)) < 8 and nw(' '.join(out[-1] + cur)) <= MAX + 6: out[-1] += cur
        else: out.append(cur)
    return [' '.join(g) for g in out]
def wav(n):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{VD}/{n}.mp3', '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True)
    return np.frombuffer(p.stdout, np.int16)
def cut_times(text, parts, words, x):
    """Thời điểm cắt giữa các phần (giây), chọn chỗ yên lặng nhất gần khoảng nghỉ giữa hai chữ."""
    sw = text.split(); asr_t = [norm(w[0]) for w in words]; sw_t = [norm(w) for w in sw]
    sm = difflib.SequenceMatcher(None, sw_t, asr_t, autojunk=False); mp = {}
    for a, b, k in sm.get_matching_blocks():
        for j in range(k): mp[a + j] = b + j
    cuts = []; idx = 0; L = len(x) / SR
    for gi in range(len(parts) - 1):
        idx += nw(parts[gi]); last, first = idx - 1, idx
        e = next((words[mp[i]][2] for i in range(last, max(-1, last - 6), -1) if i in mp), None)
        s = next((words[mp[i]][1] for i in range(first, min(len(sw), first + 6)) if i in mp), None)
        if e is None or s is None:   # dự phòng: theo tỉ lệ chữ
            cuts.append(L * idx / len(sw)); continue
        lo, hi = min(e, s) - 0.05, max(e, s) + 0.05
        a, b = int(max(0, lo) * SR), int(min(L, hi) * SR)
        seg = np.abs(x[a:b].astype(np.float32)); w = int(0.01 * SR)
        if len(seg) < 2 * w: cuts.append((e + s) / 2); continue
        rms = np.sqrt(np.convolve(seg ** 2, np.ones(w) / w, 'valid'))
        cuts.append((a + int(np.argmin(rms)) + w // 2) / SR)
    return cuts
new, mp_old, tmp = [], {}, f'{VD}/_tach'
os.makedirs(tmp, exist_ok=True); n_new = min(b['n'] for b in beats) - 1; asr_new = {}; dur_new = {}
for b in beats:
    n = str(b['n']); parts = groups(b['text']); first = n_new + 1
    ok = n in asr and os.path.exists(f'{VD}/{n}.mp3') and H.get(n) == hashlib.md5((b['text'] + b['tone'] + 'Puck').encode()).hexdigest()
    if ok:
        x = wav(n); words = asr[n]
        cuts = cut_times(b['text'], parts, words, x) if len(parts) > 1 else []
        bounds = [0.0] + cuts + [len(x) / SR]
    else: print('chưa có giọng khớp, để đọc lại:', n)
    for gi, p in enumerate(parts):
        n_new += 1
        if not ok:
            new.append(dict(n=n_new, chuong=b['chuong'], tone=b['tone'], text=p)); continue
        a, e = bounds[gi], bounds[gi + 1]
        seg = x[int(a * SR):int(e * SR)].astype(np.float32); f = int(0.008 * SR)
        if len(seg) > 2 * f: seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 's16le', '-ac', '1', '-ar', str(SR), '-i', '-', '-b:a', '128k', f'{tmp}/{n_new}.mp3'], input=seg.astype(np.int16).tobytes(), check=True)
        dur_new[str(n_new)] = len(seg) / SR
        asr_new[str(n_new)] = [[w[0], round(w[1] - a, 3), round(w[2] - a, 3)] for w in words if a - 0.02 <= (w[1] + w[2]) / 2 < e + 0.02]
        tone = 'light' if any(k in p for k in ('đôi chân', 'dũng sĩ, ông', 'chuyến đi dạo', 'hứa, nhưng')) else b['tone']
        new.append(dict(n=n_new, chuong=b['chuong'], tone=tone, text=p))
    mp_old[n] = [first, n_new]
print(len(beats), 'đoạn ->', len(new), 'đoạn; ngắn nhất', min(nw(x['text']) for x in new), 'chữ, dài nhất', max(nw(x['text']) for x in new))
if thu:
    for x in new[:12]: print(x['n'], nw(x['text']), x['text'][:80])
    shutil.rmtree(tmp); sys.exit(0)
shutil.copy(FP, f'{R}/ke-hoach/thu-giong-hai/{tên}_full_truoc_tach.json')
for b in beats:
    p = f'{VD}/{b["n"]}.mp3'
    if os.path.exists(p): os.remove(p)
for f in os.listdir(tmp): shutil.move(f'{tmp}/{f}', f'{VD}/{f}')
os.rmdir(tmp)
for b in beats: dur.pop(str(b['n']), None); H.pop(str(b['n']), None)
for k in [k for k in list(dur) if k not in dur_new and int(k) >= min(b['n'] for b in beats)]: dur.pop(k, None); H.pop(k, None)
dur.update(dur_new)
for x in new:
    if str(x['n']) in dur_new: H[str(x['n'])] = hashlib.md5((x['text'] + x['tone'] + 'Puck').encode()).hexdigest()
json.dump(dur, open(f'{VD}/thoi_luong.json', 'w')); json.dump(H, open(f'{VD}/hash.json', 'w'))
json.dump(new, open(FP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for b in beats: asr.pop(str(b['n']), None)
asr.update(asr_new); json.dump(asr, open(AP, 'w', encoding='utf-8'), ensure_ascii=False)
if os.path.exists(AP + '.h.json'): os.remove(AP + '.h.json')
json.dump(mp_old, open(f'{R}/ke-hoach/thu-giong-hai/{tên}_tach.json', 'w'), ensure_ascii=False)
print('xong; bảng ánh xạ:', f'{tên}_tach.json')
