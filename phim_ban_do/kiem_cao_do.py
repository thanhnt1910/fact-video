"""Kiểm cao độ giọng đọc từng đoạn TRƯỚC khi dựng (chủ kênh báo 27/10/2026: video Lê Hoàn đang to rõ bỗng trầm hẳn).

Gemini mỗi lượt gọi có thể trôi sang giọng trầm hơn cho cả cụm. Âm lượng và tốc độ đã chuẩn hóa nhưng cao độ thì không.
Cách dùng: python phim_ban_do/kiem_cao_do.py <tên> [--dir assets/thu_giong_hai/<tên>_chuan] [--cum 8] [--nguong 0.12]
Báo ❌ cho cụm có cao độ trung bình lệch quá ngưỡng so với trung vị cả video; đoạn lẻ lệch chỉ ⚠️ (đọc lại cụm đó, cùng cum với các cụm còn lại).
Thoát mã 1 nếu có ❌.
"""
import argparse, glob, os, re, subprocess, sys
import numpy as np

SR = 16000

def doc(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.int16).astype(float)

def f0_trung_vi(x):
    fl, hop = int(0.04 * SR), int(0.02 * SR)
    lo, hi = int(SR / 300), int(SR / 70)
    out = []
    for i in range(0, len(x) - fl, hop):
        f = x[i:i + fl]
        if np.sqrt((f ** 2).mean()) < 800:
            continue
        f = f - f.mean()
        ac = np.correlate(f, f, 'full')[fl - 1:]
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] / ac[0] > 0.45:
            out.append(SR / k)
    return float(np.median(out)) if len(out) > 10 else float('nan')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ten')
    ap.add_argument('--dir')
    ap.add_argument('--cum', type=int, default=8)
    ap.add_argument('--nguong', type=float, default=0.08, help='lệch tương đối so với trung vị video')
    a = ap.parse_args()
    d = a.dir or f'assets/thu_giong_hai/{a.ten}_chuan'
    def so(p):
        return int(re.sub(r'\D', '', os.path.splitext(os.path.basename(p))[0]) or 0)
    files = sorted(glob.glob(os.path.join(d, '*.mp3')), key=so)
    if not files:
        print('Không có file giọng trong', d); sys.exit(2)
    ns = [so(p) for p in files]
    f0 = np.array([f0_trung_vi(doc(p)) for p in files])
    med = float(np.nanmedian(f0))
    print(f'{a.ten}: {len(files)} đoạn, cao độ trung vị {med:.0f} Hz, ngưỡng ±{a.nguong*100:.0f}%')
    loi = 0
    # theo cụm liên tiếp theo thứ tự đọc (cụm = a.cum đoạn kề nhau)
    for i in range(0, len(files), a.cum):
        g = f0[i:i + a.cum]
        tb = float(np.nanmean(g))
        if abs(tb - med) / med > a.nguong:
            loi += 1
            print(f'❌ cụm {ns[i]}–{ns[min(i+a.cum,len(ns))-1]}: trung bình {tb:.0f} Hz ({(tb-med)/med*100:+.0f}%), giọng trôi cả cụm: đọc lại cụm này')
    # đoạn lẻ cao thấp tự nhiên theo ngữ điệu, chỉ cảnh báo khi nằm liền nhau từ 3 đoạn trở lên về cùng một phía
    lech = [(n, (v - med) / med) for n, v in zip(ns, f0) if v == v and abs(v - med) / med > 2 * a.nguong]
    for n, r in lech:
        print(f'⚠️ {n}: {r*100:+.0f}% so với trung vị (đoạn lẻ, nghe thử nếu nằm gần chỗ đổi giọng)')
    print(f'{loi} ❌')
    sys.exit(1 if loi else 0)

if __name__ == '__main__':
    main()
