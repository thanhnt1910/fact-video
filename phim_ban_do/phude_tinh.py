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
def main():
    src, vd, dst = sys.argv[1:4]
    beats = json.load(open(src, encoding='utf-8')); res = {}
    for b in beats:
        n = b['n']; cl = cum(b['text'])
        raw = subprocess.run(['ffmpeg','-v','error','-i',f'{vd}/{n}.mp3','-f','s16le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
        x = np.frombuffer(raw, np.int16)
        if len(cl) == 1 or len(x) < SR: res[str(n)] = [[cl[0], 0.0, len(x)/SR]]; continue
        spans, _ = H.split_by_pauses(x, [max(1, len(c.split())) for c in cl])
        hop = SR // 100
        env = np.sqrt(np.convolve((x.astype(np.float64) / 32768.0) ** 2, np.ones(hop * 2) / (hop * 2), 'same'))
        thr = max(0.006, 0.08 * float(np.percentile(env, 98)))
        rows = []
        for c, (s, e) in zip(cl, spans):
            s, e = int(s), int(e)
            seg = np.where(env[s:e] > thr)[0]
            vs, ve = ((s + seg[0]) / SR, (s + seg[-1]) / SR) if len(seg) else (s / SR, e / SR)
            rows.append([c, round(s / SR, 3), round(e / SR, 3), round(vs, 3), round(ve, 3)])
        changed = True
        while changed and len(rows) > 1:
            changed = False
            for i, r in enumerate(rows):
                if (r[4] - r[3]) / max(1, len(r[0].split())) < 0.15:
                    j = i + 1 if i + 1 < len(rows) else i - 1
                    a, b2 = sorted((i, j)); A, B = rows[a], rows[b2]
                    rows[a:b2 + 1] = [[A[0] + ' ' + B[0], A[1], B[2], A[3], B[4]]]
                    changed = True; break
        res[str(n)] = rows
    json.dump(res, open(dst, 'w'), ensure_ascii=False)
    print(len(res), 'câu,', sum(len(v) for v in res.values()), 'cụm')
if __name__ == '__main__': main()
