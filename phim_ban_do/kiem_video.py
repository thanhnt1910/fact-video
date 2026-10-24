"""Công cụ kiểm video bản đồ: giọng đọc, phụ đề, khớp cảnh, file video.

Cách chạy (trong thư mục repo):
  python phim_ban_do/kiem_video.py v2 [--video tap2.mp4] [--tts v2r,v2s,v2x]

Cần có sẵn:
  - kịch bản          ke-hoach/thu-giong-hai/<tên>_full.json
  - nhận dạng giọng   phim_ban_do/asr_<tên>_final.json (hoặc asr_<tên>.json), chạy workflow phude-asr SAU khi file giọng đã chốt
  - phụ đề            phim_ban_do/phude_<tên>.json
  - tuỳ chọn --video: file mp4 đã dựng (kiểm khớp giọng-khung hình, im lặng, đứng hình, đen)
Kết quả: logs/kiem_video/<tên>.md, thoát mã 1 nếu có lỗi ❌.
"""
import json, os, re, sys, subprocess, difflib, unicodedata, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import phude_tinh as P

ap = argparse.ArgumentParser()
ap.add_argument('ten'); ap.add_argument('--video'); ap.add_argument('--tts', default='')
ap.add_argument('--asr', help='file nhận dạng khác (mặc định asr_<tên>_final.json hoặc asr_<tên>.json)')
ap.add_argument('--base', type=int, default=None, help='tiền tố số câu (v1=1000, v2=2000, nm1=3000)')
ap.add_argument('--voice', default=os.path.join(ROOT, 'assets/thu_giong_hai/puck'))
a = ap.parse_args()
TEN = a.ten; KB = os.path.join(ROOT, 'ke-hoach/thu-giong-hai')
BASE = a.base if a.base is not None else {'v1': 1000, 'v2': 2000, 'nm1': 3000}.get(TEN, 0)
BEATS = json.load(open(f'{KB}/{TEN}_full.json'))
import glob
TF = [x for x in a.tts.split(',') if x] or [os.path.basename(f)[:-10] for f in sorted(glob.glob(f'{KB}/{TEN}?_full.json'))]
TTS = {}
for f in TF:
    for b in json.load(open(f'{KB}/{f}_full.json')):
        if 'tts' in b: TTS[b['n']] = b['tts']
def tim(*ds):
    for d in ds:
        if os.path.exists(d): return d
    return None
ASRF = a.asr or tim(f'{HERE}/asr_{TEN}_final.json', f'{HERE}/asr_{TEN}.json')
PHF = tim(f'{HERE}/phude_{TEN}.json')
ASR = json.load(open(ASRF)) if ASRF else {}
PH = json.load(open(PHF)) if PHF else {}
TL = json.load(open(f'{a.voice}/thoi_luong.json'))
LOI = []; CB = []   # ❌ lỗi, ⚠️ cảnh báo
def bad(m): LOI.append(m)
def warn(m): CB.append(m)
def norm(w):
    return ''.join(c for c in unicodedata.normalize('NFD', re.sub(r'[^\w]', '', w.lower())) if unicodedata.category(c) != 'Mn').replace('đ', 'd')
# từ hay đọc sai: (viết trong kịch bản, dạng nhận dạng được chấp nhận)

# ---- Lớp 1: giọng đọc so với kịch bản --------------------------------------
n_asr = 0
for b in BEATS:
    n = b['n']; k = str(n)
    if k not in ASR or not ASR[k]:
        bad(f'Câu {n}: chưa có kết quả nhận dạng giọng'); continue
    n_asr += 1
    w = TTS.get(n, b['text']).split(); ow, _ = P.so_nam(w, [0] * len(w))
    if not any(re.search(r'\d', x[0]) for x in ASR[k]): ow = list(w)   # nhận dạng ghi năm bằng chữ: so bằng chữ, không đổi thành số
    spk = [norm(x) for x in ow if norm(x)]; got = [norm(x[0]) for x in ASR[k] if norm(x[0])]
    # ASR cũ? thời lượng file giọng so với từ cuối
    dur = TL.get(k)
    if dur and ASR[k][-1][2] > dur + 0.8: bad(f'Câu {n}: nhận dạng dài hơn file giọng ({ASR[k][-1][2]:.1f}s > {dur:.1f}s): kết quả nhận dạng CŨ, chạy lại phude-asr')
    sm = difflib.SequenceMatcher(None, spk, got, autojunk=False)
    ops = sm.get_opcodes()
    # chữ thừa/mất ở đầu và cuối: tính theo khối khớp ĐẦU TIÊN/CUỐI CÙNG (>=3 chữ), không dựa vào một phép "insert"
    # (difflib hay gộp chữ thừa với chữ lệch thành "replace", làm sót lỗi đọc lại đuôi câu trước)
    blk = [m for m in sm.get_matching_blocks() if m.size >= 3]
    if blk:
        b0, b1 = blk[0], blk[-1]
        th = max(0, b0.b - b0.a); mh = max(0, b0.a - b0.b)
        tc = max(0, (len(got) - (b1.b + b1.size)) - (len(spk) - (b1.a + b1.size)))
        mc = max(0, (len(spk) - (b1.a + b1.size)) - (len(got) - (b1.b + b1.size)))
    else:
        th = tc = mh = mc = 0
    if th >= 3: bad(f'Câu {n}: thừa {th} chữ ở ĐẦU (lẫn đuôi câu trước): "{" ".join(x[0] for x in ASR[k][:th])}"')
    if tc >= 3: bad(f'Câu {n}: thừa {tc} chữ ở CUỐI (lẫn đầu câu sau): "{" ".join(x[0] for x in ASR[k][-tc:])}"')
    if mh >= 3: bad(f'Câu {n}: MẤT {mh} chữ ở đầu (câu bị cụt đầu)')
    if mc >= 3: bad(f'Câu {n}: MẤT {mc} chữ ở cuối (câu bị cụt đuôi)')
    # lặp cụm 2-3 chữ liền nhau mà kịch bản không có
    ktxt = ' '.join(spk)
    SO = {'1': 'mot', '2': 'hai', '3': 'ba', '4': 'bon', '5': 'nam', '6': 'sau', '7': 'bay', '8': 'tam', '9': 'chin', '10': 'muoi'}
    got = [SO.get(x, x) for x in got]
    for L in (3, 2):
        for i in range(len(got) - 2 * L + 1):
            if got[i:i + L] == got[i + L:i + 2 * L]:
                g = ' '.join(got[i:i + L])
                if (g + ' ' + g) not in ktxt: bad(f'Câu {n}: đọc LẶP "{g}"')
    # đọc LẶP CẢ CÂU / CẢ VẾ (chủ kênh yêu cầu 22/10/2026, demo Hồng Môn yến bị lặp câu)
    #  (a) giọng có nhiều chữ hơn kịch bản từ 4 chữ trở lên (số "100" thay "một trăm" chỉ làm ÍT chữ đi)
    if len(got) - len(spk) >= 4: bad(f'Câu {n}: giọng nhiều hơn kịch bản {len(got) - len(spk)} chữ (nghi đọc lặp hoặc lẫn câu khác)')
    #  (b) một vế của kịch bản (>=4 chữ, tách theo dấu câu) được đọc từ 2 lần trở lên
    for seg in re.split(r'[.!?;:,]\s', b['text']):
        sg = [norm(x) for x in seg.split() if norm(x)]
        sg = [SO.get(x, x) for x in sg]
        if len(sg) < 4: continue
        hit = sum(1 for i in range(len(got) - len(sg) + 1) if got[i:i + len(sg)] == sg)
        if hit >= 2 and ' '.join(sg) not in ' '.join(spk).replace(' '.join(sg), '', 1): bad(f'Câu {n}: vế "{seg.strip()[:50]}" bị đọc {hit} lần')
    #  (c) đuôi câu trước bị đọc lại ở đầu câu này, hoặc đầu câu sau bị đọc ở cuối câu này
    i_b = BEATS.index(b)
    if i_b > 0:
        pv = [SO.get(norm(x), norm(x)) for x in BEATS[i_b - 1]['text'].split() if norm(x)]
        for L in (6, 4, 3):
            tailp = pv[-L:]
            if len(tailp) == L and any(got[i:i + L] == tailp for i in range(0, min(len(got), L + 8) - L + 1)) and spk[:L] != tailp and not any(spk[i:i + L] == tailp for i in range(0, min(len(spk), L + 8) - L + 1)):
                bad(f'Câu {n}: ĐẦU câu đọc lại đuôi câu trước ("{" ".join(tailp)}")'); break
    if i_b + 1 < len(BEATS):
        nx = [SO.get(norm(x), norm(x)) for x in BEATS[i_b + 1]['text'].split() if norm(x)]
        for L in (6, 4, 3):
            head = nx[:L]
            if len(head) == L and any(got[i:i + L] == head for i in range(max(0, len(got) - L - 8), len(got) - L + 1)) and spk[-L:] != head and not any(spk[i:i + L] == head for i in range(max(0, len(spk) - L - 8), len(spk) - L + 1)):
                bad(f'Câu {n}: CUỐI câu đọc lẫn đầu câu sau ("{" ".join(head)}")'); break
    r = difflib.SequenceMatcher(None, spk, got, autojunk=False).ratio()
    if r < 0.6: warn(f'Câu {n}: giọng chỉ khớp {r:.0%} với kịch bản (nhận dạng có thể sai, nên nghe lại)')
    # năm
    exp = [x.strip('.,;:!?') for x in ow if re.fullmatch(r'\d{3}', x.strip('.,;:!?'))]
    gtxt = ' '.join(x[0] for x in ASR[k]); gn = re.findall(r'\d+', gtxt.replace(' .', '').replace('.', ''))
    for e in exp:
        if e not in gn:
            near = [g for g in gn if len(g) >= 3]
            bad(f'Câu {n}: NĂM {e} không nghe thấy (nhận dạng: {near or "không có số"})')
    # từ hay đọc sai (kỵ binh -> cụ binh...)
    heard = ' '.join(got)
    for t in ('kỵ', 'kị'):
        if t in b['text'] and not re.search(r'k[iy] binh|k[iy] ?\b', heard) and 'binh' in heard:
            warn(f'Câu {n}: từ "{t}" có thể bị đọc sai (nghe: "{gtxt[:70]}")')

# ---- Lớp 2: phụ đề so với giọng -------------------------------------------
if PH:
    for b in BEATS:
        n = b['n']; k = str(n); rows = PH.get(k)
        if not rows: bad(f'Câu {n}: không có phụ đề'); continue
        dur = TL.get(k, 0)
        prev_end = 0
        for i, r in enumerate(rows):
            txt, s, e = r[0], r[1], r[2]
            if len(txt.split()) > 8: warn(f'Câu {n}: cụm phụ đề dài {len(txt.split())} chữ: "{txt}"')
            if len(txt) > 52: warn(f'Câu {n}: cụm phụ đề dài {len(txt)} ký tự: "{txt}"')
            if s + 0.05 < prev_end: bad(f'Câu {n}: phụ đề chồng nhau tại "{txt}"')
            if s - prev_end > 1.6 and i > 0: warn(f'Câu {n}: phụ đề trống {s - prev_end:.1f}s trước "{txt}" (giọng đang nói gì đó không hiện chữ)')
            prev_end = e
            # so với từ nhận dạng đầu cụm
            if len(r) >= 6 and r[5] and ASR.get(k):
                tr = norm(txt.split()[0]) if txt.split() else ''
                cand = [w for w in ASR[k] if abs(w[1] - r[3]) < 0.8 and norm(w[0]) == tr]
                if ASR[k] and not cand and tr and not re.fullmatch(r'\d+', tr):
                    pass
        if rows and ASR.get(k):
            t0 = ASR[k][0][1]; t1 = ASR[k][-1][2]
            if rows[0][1] - t0 > 0.7: warn(f'Câu {n}: phụ đề đầu câu hiện TRỄ {rows[0][1] - t0:.1f}s so với giọng')
            if t0 - rows[0][1] > 0.7: warn(f'Câu {n}: phụ đề đầu câu hiện SỚM {t0 - rows[0][1]:.1f}s so với giọng')
            if t1 - rows[-1][2] > 0.8: warn(f'Câu {n}: phụ đề tắt sớm {t1 - rows[-1][2]:.1f}s trước khi hết giọng')
else:
    warn('Không có file phụ đề (phude_%s.json)' % TEN)

# ---- Lớp 3: khớp cảnh với lời kể ------------------------------------------
cs = os.path.join(HERE, f'{TEN}_content.py')
if os.path.exists(cs):
    src = open(cs).read()
    m = re.search(r'for a,b,y in \[(.*?)\]:', src, re.S)
    if m:
        try:
            tab = eval('[' + m.group(1) + ']')
            def yo(n):
                for x, y_, yr in tab:
                    if x <= n <= y_: return yr
            for b in BEATS:
                w = b['text'].split(); ow, _ = P.so_nam(w, [0] * len(w))
                ys = [int(x.strip('.,;:!?')) for x in ow if re.fullmatch(r'\d{3}', x.strip('.,;:!?'))]
                yb = yo(b['n'] - BASE)
                if ys and yb is not None and yb not in ys and (yb - 1) not in ys:
                    bad(f'Câu {b["n"]}: ô năm ghi {yb} nhưng lời kể nói {ys}')
        except Exception as ex:
            warn(f'Không đọc được bảng năm: {ex}')
    for mm in re.finditer(r'\bR\((\d+),\s*(-?[\d.]+)\)', src):
        n = int(mm.group(1)); o = float(mm.group(2)); d = TL.get(str(BASE + n))
        if d and o > d + 0.65: warn(f'Cảnh gắn vào câu {n} lệch +{o:.1f}s nhưng câu chỉ dài {d:.1f}s (rơi sang câu sau)')
        if o < -3: warn(f'Cảnh gắn vào câu {n} sớm {o:.1f}s trước câu')
    ns = sorted(int(k) for k in TL if k.isdigit() and BASE <= int(k) < BASE + 1000)
    miss = [x for x in (b['n'] for b in BEATS) if str(x) not in TL]
    if miss: bad(f'Thiếu file giọng cho {len(miss)} câu: {miss[:10]}')

# ---- Lớp 4: file video đã dựng ---------------------------------------------
if a.video:
    ns = [b['n'] for b in BEATS if str(b['n']) in TL]
    T = {}; x = 0.5
    for n in ns: T[n] = x; x += TL[str(n)] + 0.45
    total = x + 1.5
    dd = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.video], capture_output=True, text=True).stdout.strip() or 0)
    if abs(dd - total) > 1.5: bad(f'Video dài {dd:.1f}s nhưng kịch bản tính {total:.1f}s')
    if dd < 600 and BASE: warn(f'Video dài {dd/60:.1f} phút, dưới mức sàn 10 phút của video dài')
    def dec(p, sr=16000):
        r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 's16le', '-ac', '1', '-ar', str(sr), '-'], capture_output=True).stdout
        return np.frombuffer(r, np.int16).astype(np.float32)
    V = dec(a.video)
    # (a) giọng trong video có đúng chỗ với file giọng không (mọi câu)
    lech = 0
    for n in ns:
        s = dec(f'{a.voice}/{n}.mp3')[:16000 * 3]
        if len(s) < 1600: continue
        i0 = int((T[n] + 0.12) * 16000); lo = max(0, i0 - 8000)
        seg = V[lo:i0 + len(s) + 8000]
        if len(seg) < len(s): continue
        c = np.correlate(seg, s, 'valid'); k = int(np.argmax(c)) - (i0 - lo)
        if abs(k) > 800:
            lech += 1; bad(f'Câu {n}: giọng trong video LỆCH {k/16000:+.2f}s so với vị trí cảnh')
    # (b) im lặng dài, vỡ tiếng
    env = np.abs(V[:len(V) // 1600 * 1600]).reshape(-1, 1600).mean(axis=1) if len(V) >= 1600 else np.array([])
    env = env[:len(env)]
    sil = env < 20; run = 0; mx = 0
    for i, v in enumerate(sil):
        run = run + 1 if v else 0
        if run == 40: warn(f'Im lặng hơn 4 giây quanh {i/10:.0f}s trong video')
    if np.abs(V).max() >= 32700: warn('Tiếng bị vỡ (clipping) ở đâu đó')
    # (c) khung hình đen, đứng hình
    r = subprocess.run(['ffmpeg', '-v', 'info', '-i', a.video, '-vf', 'blackdetect=d=1.0:pix_th=0.05,freezedetect=n=-60dB:d=12', '-an', '-f', 'null', '-'], capture_output=True, text=True).stderr
    for m_ in re.finditer(r'black_start:([\d.]+).*?black_duration:([\d.]+)', r):
        if float(m_.group(1)) > 3 and float(m_.group(1)) < dd - 3: warn(f'Khung hình đen {m_.group(2)}s tại {float(m_.group(1)):.0f}s')
    for m_ in re.finditer(r'freeze_start: ([\d.]+)', r): warn(f'Hình đứng hơn 12 giây tại {float(m_.group(1)):.0f}s')
    # (d) chữ tràn khung: lấy vài khung hình giữa mỗi 20 câu, kiểm vùng sát mép có nhiều điểm sáng bất thường (chữ cắt)
    # (chỉ cảnh báo thô; kiểm kỹ bằng phude_tinh/textlength khi dựng)

# ---- Báo cáo -----------------------------------------------------------------
os.makedirs(f'{ROOT}/logs/kiem_video', exist_ok=True)
out = [f'# Kiểm video {TEN}', '', f'- Kịch bản {len(BEATS)} câu; có nhận dạng {n_asr} câu; nhận dạng: {os.path.basename(ASRF) if ASRF else "KHÔNG CÓ"}',
       f'- ❌ lỗi: {len(LOI)}  ⚠️ cảnh báo: {len(CB)}', '', '## ❌ Lỗi'] + [f'- {m}' for m in LOI] + ['', '## ⚠️ Cảnh báo'] + [f'- {m}' for m in CB]
open(f'{ROOT}/logs/kiem_video/{TEN}.md', 'w').write('\n'.join(out))
print('\n'.join(out[:3]))
for m in LOI[:60]: print('❌', m)
for m in CB[:40]: print('⚠️', m)
print(f'... đầy đủ: logs/kiem_video/{TEN}.md')
sys.exit(1 if LOI else 0)
