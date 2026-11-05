"""Cân giọng đồng đều theo ÂM SẮC (chủ kênh yêu cầu 05/11/2026, từ video Chu Du).

Vì sao: cân chỉ bằng cao độ (asetrate) làm dịch vùng cộng hưởng nên nghe thành người khác (đo ở Chu Du: 9008 xa mốc 0,9 -> 1,57).
Cách làm: với mỗi đoạn thử 3 bản (A: không đổi cao độ; B: kéo hết về cao độ mốc; C: kéo nửa đường), đều dùng rubberband giữ nguyên formant,
chuẩn tốc độ (0,90-1,10) và loudnorm -16. So phổ trung bình (40 dải mel) với đoạn mốc do chủ kênh chọn; chọn bản gần mốc nhất.
Đoạn nào vẫn xa mốc (> trung vị + 4 MAD) thì in ra để ĐỌC LẠI (không cố chỉnh tiếp).
Dùng: python phim_ban_do/can_giong_am_sac.py <tên> --goc <thư mục mp3 gốc> --kich-ban <json> --moc 9012,9013,9014,9015 --f0 147 --wps 3.9 --ra assets/thu_giong_hai/<tên>_chuan
"""
import argparse, json, os, subprocess, sys, tempfile
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kiem_cao_do import doc, f0_trung_vi
SR = 16000

def mel_fb(n=40, nfft=512):
    f = lambda m: 700 * (10 ** (m / 2595) - 1); m = lambda h: 2595 * np.log10(1 + h / 700)
    pts = f(np.linspace(m(80), m(7600), n + 2)); b = np.floor((nfft + 1) * pts / SR).astype(int)
    fb = np.zeros((n, nfft // 2 + 1))
    for i in range(n):
        l, c, r = b[i], b[i + 1], b[i + 2]
        for k in range(l, c): fb[i, k] = (k - l) / max(1, c - l)
        for k in range(c, r): fb[i, k] = (r - k) / max(1, r - c)
    return fb
FB = mel_fb()

def vec(x):
    fl, hop = 512, 256; w = np.hanning(fl); fr = []
    for i in range(0, len(x) - fl, hop):
        f = x[i:i + fl]
        if np.sqrt((f ** 2).mean()) < 800: continue
        fr.append(np.log(FB @ (np.abs(np.fft.rfft(f * w)) ** 2) + 1e-3))
    return np.array(fr).mean(0)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('ten'); ap.add_argument('--goc', required=True); ap.add_argument('--kich-ban', required=True)
    ap.add_argument('--moc', required=True); ap.add_argument('--f0', type=float, default=147); ap.add_argument('--wps', type=float, default=3.9)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    txt = {str(x['n']): x['text'] for x in json.load(open(a.kich_ban, encoding='utf-8'))}
    ns = sorted(int(os.path.splitext(f)[0]) for f in os.listdir(a.goc) if f.endswith('.mp3'))
    tmp = tempfile.mkdtemp(); cand = {}
    for n in ns:
        x = doc(f'{a.goc}/{n}.mp3'); dur = len(x) / SR; f0 = f0_trung_vi(x); wps = len(txt[str(n)].split()) / dur
        s = min(1.10, max(0.90, a.wps / wps)); full = min(1.15, max(0.87, a.f0 / f0))
        for m, r in (('A', 1.0), ('B', full), ('C', 1 + 0.5 * (full - 1))):
            o = f'{tmp}/{n}{m}.mp3'
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{a.goc}/{n}.mp3', '-af', f'rubberband=pitch={r:.4f}:tempo={s:.4f}:formant=preserved:transients=crisp:phase=independent:window=short,loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '24000', o], check=True)
            cand[(n, m)] = o
    ref = np.mean([vec(doc(cand[(int(n), 'A')])) for n in a.moc.split(',')], 0)   # mốc cũng qua cùng bước xử lý
    os.makedirs(a.ra, exist_ok=True); dur_out = {}; xa = []; rows = []
    for n in ns:
        best = None
        for m in 'ABC':
            g = doc(cand[(n, m)]); f0 = f0_trung_vi(g); wps = len(txt[str(n)].split()) / (len(g) / SR)
            td = float(np.sqrt(((vec(g) - ref) ** 2).mean()))
            sc = td + 3 * max(0, abs(f0 - a.f0) / a.f0 - 0.04) + 2 * max(0, abs(wps - a.wps) / a.wps - 0.08)
            if best is None or sc < best[0]: best = (sc, m, td, f0, wps, len(g) / SR)
        subprocess.run(['cp', cand[(n, best[1])], f'{a.ra}/{n}.mp3']); dur_out[str(n)] = round(best[5], 3); rows.append((n, best))
    json.dump(dur_out, open(f'{a.ra}/thoi_luong.json', 'w'), indent=1)
    sc = np.array([r[1][0] for r in rows]); med = np.median(sc); mad = np.median(abs(sc - med)); thr = med + 4 * mad
    print(f'{a.ten}: {len(ns)} đoạn, điểm lệch trung vị {med:.2f}, MAD {mad:.2f}, ngưỡng đọc lại {thr:.2f}')
    xa = [(n, b) for n, b in rows if b[0] > thr]
    for n, b in sorted(xa, key=lambda z: -z[1][0]): print(f'  ĐỌC LẠI {n}: bản {b[1]} âm sắc {b[2]:.2f} cao độ {b[3]:.0f} Hz nhịp {b[4]:.2f} chữ/giây')
    json.dump([n for n, _ in xa], open(f'{a.ra}/can_doc_lai.json', 'w'))
    sys.exit(1 if xa else 0)
main()
