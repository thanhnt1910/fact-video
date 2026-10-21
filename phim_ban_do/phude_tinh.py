"""Tính thời điểm phụ đề theo giọng đọc: python phude_tinh.py <kịch bản.json> <thư mục giọng> <ra.json>
Mỗi câu chia thành cụm (theo dấu câu), cụm nào dưới 3 chữ gộp vào cụm kế; mốc cắt khớp khoảng lặng thật trong tệp giọng."""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import thu_giong_hai_cum as H
SR = 16000
H.SR = SR
def cum(text):
    parts = [p for p in re.split(r'(?<=[,;:.!?…—])\s+', text.strip()) if p]
    out = []
    for p in parts:
        if out and (len(out[-1].split()) < 3): out[-1] += ' ' + p
        else: out.append(p)
    if len(out) > 1 and len(out[-1].split()) < 3:
        last = out.pop(); out[-1] += ' ' + last
    return out
def chu_moc(x, vs, ve, words):
    """Mốc bắt đầu từng chữ trong cụm [vs,ve]: tiếng Việt mỗi chữ một âm tiết, nên cắt ở chỗ năng lượng thấp,
    độ dài mỗi chữ bám theo độ dài kỳ vọng (quy hoạch động)."""
    N = len(words)
    if N <= 1: return [round(vs, 3)]
    hop = SR // 100
    k = np.ones(hop * 3) / (hop * 3)
    e = np.sqrt(np.convolve((x.astype(np.float64) / 32768.0) ** 2, k, 'same'))
    f0, f1 = int(vs * 100), int(ve * 100)
    env = np.array([e[min(len(e) - 1, i * hop)] for i in range(f0, f1 + 1)]); M = len(env) - 1
    if M < N: return [round(vs + (ve - vs) * i / N, 3) for i in range(N)]
    env = env / (env.max() + 1e-9)
    w = np.array([1.0 + 0.12 * len(t) for t in words]); L = M * w / w.sum()
    INF = 1e18
    cost = np.full((N, M + 1), INF); back = np.zeros((N, M + 1), int); cost[0][0] = 0
    for i in range(1, N):
        lo_i, hi_i = int(0.55 * L[i - 1]), int(1.6 * L[i - 1]) + 1
        for f in range(1, M):
            best, bj = INF, 0
            for g in range(max(0, f - hi_i), f - lo_i + 1):
                if cost[i - 1][g] >= INF: continue
                d = ((f - g) - L[i - 1]) / L[i - 1]
                c = cost[i - 1][g] + 1.2 * d * d
                if c < best: best, bj = c, g
            if best < INF: cost[i][f] = best + 4.0 * env[f]; back[i][f] = bj
    fin, fj = INF, None
    for f in range(1, M):
        d = ((M - f) - L[N - 1]) / L[N - 1]; c = cost[N - 1][f] + 1.2 * d * d
        if c < fin: fin, fj = c, f
    if fj is None: return [round(vs + (ve - vs) * i / N, 3) for i in range(N)]
    cuts = [fj]
    for i in range(N - 1, 1, -1): cuts.append(back[i][cuts[-1]])
    cuts = [0] + cuts[::-1]
    return [round(vs + c / 100.0, 3) for c in cuts]
def _nor(w): return re.sub(r'[^\w]', '', w.lower())
def asr_moc(words, asr):
    """Mốc bắt đầu từng chữ của lời kể theo kết quả nhận dạng giọng (asr: [[chữ, bắt đầu, kết thúc], ...])."""
    import difflib
    if not asr: return None
    a = [_nor(w) for w in words]; b = [_nor(r[0]) for r in asr]
    t = [None] * len(words)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
            for k in range(i2 - i1): t[i1 + k] = asr[j1 + k][1]
        elif tag == 'replace':
            st, en = asr[j1][1], asr[j2 - 1][2]
            for k in range(i2 - i1): t[i1 + k] = st + (en - st) * k / (i2 - i1)
    known = [i for i, v in enumerate(t) if v is not None]
    if len(known) < 0.5 * len(words): return None
    end = asr[-1][2]
    for i in range(len(t)):
        if t[i] is not None: continue
        l = max([k for k in known if k < i], default=None); r = min([k for k in known if k > i], default=None)
        if l is None: t[i] = max(0.0, t[r] - 0.28 * (r - i))
        elif r is None: t[i] = min(end, t[l] + 0.28 * (i - l))
        else: t[i] = t[l] + (t[r] - t[l]) * (i - l) / (r - l)
    for i in range(1, len(t)): t[i] = max(t[i], t[i - 1])
    return [round(v, 3) for v in t]
def chia_ngan(rows, toi_da=7):
    """Chia cụm dài thành các đoạn phụ đề ngắn (tối đa toi_da chữ), mỗi đoạn có mốc từng chữ riêng."""
    out = []
    for r in rows:
        w = r[0].split(); tm = r[5] if len(r) >= 6 and r[5] else None
        if len(w) <= toi_da or not tm or len(tm) != len(w): out.append(r); continue
        k = -(-len(w) // toi_da); base, ex = divmod(len(w), k); i = 0; parts = []
        for j in range(k):
            m = base + (1 if j < ex else 0); parts.append((i, i + m)); i += m
        for j, (a, b) in enumerate(parts):
            e = tm[parts[j + 1][0]] if j + 1 < len(parts) else r[2]
            ve = r[4] if j + 1 == len(parts) else min(e, tm[b - 1] + 0.4)
            out.append([' '.join(w[a:b]), round(tm[a] if j else r[1], 3), round(e, 3), round(tm[a], 3), round(ve, 3), tm[a:b]])
    return out
def main():
    src, vd, dst = sys.argv[1:4]
    ASR = json.load(open(sys.argv[4], encoding='utf-8')) if len(sys.argv) > 4 else {}
    beats = json.load(open(src, encoding='utf-8')); res = {}
    for b in beats:
        n = b['n']; cl = cum(b['text'])
        raw = subprocess.run(['ffmpeg','-v','error','-i',f'{vd}/{n}.mp3','-f','s16le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
        x = np.frombuffer(raw, np.int16)
        if len(cl) == 1 or len(x) < SR:
            _env = np.sqrt(np.convolve((x.astype(np.float64) / 32768.0) ** 2, np.ones(SR // 50) / (SR // 50), 'same')); _v = np.where(_env > max(0.006, 0.08 * float(np.percentile(_env, 98))))[0]
            _vs, _ve = ((_v[0] / SR, _v[-1] / SR) if len(_v) else (0.0, len(x) / SR))
            _r = [cl[0], 0.0, len(x)/SR, round(_vs, 3), round(_ve, 3), chu_moc(x, _vs, _ve, cl[0].split())]
            _am = asr_moc(b['text'].split(), ASR.get(str(n)))
            if _am: _r[5] = _am
            res[str(n)] = chia_ngan([_r]); continue
        spans, _ = H.split_by_pauses(x, [max(1, len(c.split())) for c in cl])
        hop = SR // 100
        env = np.sqrt(np.convolve((x.astype(np.float64) / 32768.0) ** 2, np.ones(hop * 2) / (hop * 2), 'same'))
        thr = max(0.006, 0.08 * float(np.percentile(env, 98)))
        rows = []
        for c, (s, e) in zip(cl, spans):
            s, e = int(s), int(e)
            seg = np.where(env[s:e] > thr)[0]
            vs, ve = ((s + seg[0]) / SR, (s + seg[-1]) / SR) if len(seg) else (s / SR, e / SR)
            rows.append([c, round(s / SR, 3), round(e / SR, 3), round(vs, 3), round(ve, 3), chu_moc(x, vs, ve, c.split())])
        changed = True
        while changed and len(rows) > 1:
            changed = False
            for i, r in enumerate(rows):
                if (r[4] - r[3]) / max(1, len(r[0].split())) < 0.15:
                    j = i + 1 if i + 1 < len(rows) else i - 1
                    a, b2 = sorted((i, j)); A, B = rows[a], rows[b2]
                    rows[a:b2 + 1] = [[A[0] + ' ' + B[0], A[1], B[2], A[3], B[4], chu_moc(x, A[3], B[4], (A[0] + ' ' + B[0]).split())]]
                    changed = True; break
        am = asr_moc(b['text'].split(), ASR.get(str(n)))
        if am:
            k = 0
            for r in rows:
                m = len(r[0].split()); r[5] = am[k:k + m]; k += m
        res[str(n)] = chia_ngan(rows)
    json.dump(res, open(dst, 'w'), ensure_ascii=False)
    print(len(res), 'câu,', sum(len(v) for v in res.values()), 'cụm')
if __name__ == '__main__': main()
