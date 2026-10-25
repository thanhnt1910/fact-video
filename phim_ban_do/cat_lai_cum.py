"""Cắt lại cụm giọng thành từng đoạn theo mốc chữ nhận dạng (thay cho cắt theo chỗ lặng hay lệch).
python phim_ban_do/cat_lai_cum.py <kịch bản đoạn.json> <kịch bản cụm.json> <asr cụm.json> <thư mục mp3 cụm> <thư mục ra> [kích thước cụm]
Mỗi cụm là file <n>.mp3 (n = 1..); nhận dạng cho mốc từng chữ; căn chữ nhận dạng với chữ kịch bản (difflib), nội suy giữa các điểm khớp;
ranh giới giữa hai đoạn đặt ở chỗ năng lượng thấp nhất trong khoảng ±0,3 giây quanh mốc."""
import json, os, re, subprocess, sys, difflib
import numpy as np
SR = 24000
def tok(t): return re.sub(r'[^\w\s]', ' ', t.lower()).split()
def main():
    kb = json.load(open(sys.argv[1], encoding='utf-8')); kc = json.load(open(sys.argv[2], encoding='utf-8'))
    asr = json.load(open(sys.argv[3], encoding='utf-8')); vd, out = sys.argv[4], sys.argv[5]; per = int(sys.argv[6]) if len(sys.argv) > 6 else 16
    sizes = [int(x) for x in sys.argv[7].split(',')] if len(sys.argv) > 7 else None
    offs = [0]
    for z in (sizes or []): offs.append(offs[-1] + z)
    os.makedirs(out, exist_ok=True); rep = []
    for ci, c in enumerate(kc):
        g = kb[offs[ci]:offs[ci + 1]] if sizes else kb[ci * per:(ci + 1) * per]; W = asr[str(c['n'])]
        x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f"{vd}/{c['n']}.mp3", '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
        S = []; own = []
        for pi, b in enumerate(g):
            w = tok(b['text']); S += w; own += [pi] * len(w)
        A = [re.sub(r'[^\w]', '', w[0].lower()) for w in W]
        sm = difflib.SequenceMatcher(None, S, A, autojunk=False)
        mp = {}   # chỉ số chữ kịch bản -> chỉ số chữ nhận dạng
        for blk in sm.get_matching_blocks():
            for k in range(blk.size): mp[blk.a + k] = blk.b + k
        ks = sorted(mp); assert ks, 'không khớp chữ nào'
        def amap(i):
            if i in mp: return float(mp[i])
            lo = [k for k in ks if k < i]; hi = [k for k in ks if k > i]
            if lo and hi: a, b2 = lo[-1], hi[0]; return mp[a] + (mp[b2] - mp[a]) * (i - a) / (b2 - a)
            if lo: return mp[lo[-1]] + (i - lo[-1])
            return max(0.0, mp[hi[0]] - (hi[0] - i))
        # mốc ranh giới: giữa chữ cuối đoạn i và chữ đầu đoạn i+1
        bounds = [0.0]; idx = 0
        for pi in range(len(g) - 1):
            idx += len(tok(g[pi]['text'])); a_last = amap(idx - 1); a_first = amap(idx)
            ia = min(len(W) - 1, max(0, int(round(a_last)))); ib = min(len(W) - 1, max(0, int(round(a_first))))
            t_end = W[ia][2]; t_next = W[ib][1] if ib > ia else W[ia][2] + 0.05
            t = (t_end + max(t_end, t_next)) / 2
            lo, hi = int(max(0, t - 0.3) * SR), int(min(len(x) / SR, t + 0.3) * SR)
            seg = np.abs(x[lo:hi]); k = np.ones(int(0.02 * SR)) / int(0.02 * SR); e = np.convolve(seg, k, 'same')
            t = (lo + int(np.argmin(e))) / SR; bounds.append(t)
        bounds.append(len(x) / SR)
        for pi, b in enumerate(g):
            s, e = int(bounds[pi] * SR), int(bounds[pi + 1] * SR); seg = x[s:e].copy(); fd = int(0.012 * SR)
            if len(seg) > 4 * fd: seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd)
            p = f"{out}/{b['n']}.mp3"
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-', '-ar', '44100', '-b:a', '128k', p], input=(seg * 32767).astype(np.int16).tobytes(), check=True)
            rep.append((b['n'], round(len(seg) / SR, 2), round(len(tok(b['text'])) / max(0.1, len(seg) / SR), 2)))
    json.dump(rep, open(out + '/bao_cao.json', 'w'))
    print('đã cắt', len(rep), 'đoạn')
if __name__ == '__main__': main()
