"""Đồng điệu giọng: kéo âm sắc (EQ theo phổ trung bình) và cao độ từng đoạn về giọng chuẩn.
python phim_ban_do/dong_dieu_giong.py <thư_mục_vào> <thư_mục_ra> <id_đầu> <id_cuối> <id_chuẩn_đầu> <id_chuẩn_cuối>"""
import sys, subprocess, json, numpy as np
from pathlib import Path
from scipy.signal import stft, istft
SR = 24000
def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()
def ltas(y):
    f, t, Z = stft(y, SR, nperseg=1024, noverlap=768)
    P = np.abs(Z) ** 2; e = P.sum(0); m = e > np.percentile(e, 40)
    return f, np.log(P[:, m].mean(1) + 1e-10), Z
def f0med(y):
    y = y[::SR // 16000] if SR % 16000 == 0 else y
    out = []
    for s in range(0, len(y) - 640, 320):
        fr = y[s:s + 640]
        if fr.std() < 0.01: continue
        fr = fr - fr.mean(); a = np.correlate(fr, fr, "full")[639:]
        k = 53 + np.argmax(a[53:228])
        if a[k] / a[0] > 0.5: out.append(16000 / k)
    return float(np.median(out)) if out else 0.0
def smooth(x, n=9): return np.convolve(np.pad(x, n, mode="edge"), np.ones(2 * n + 1) / (2 * n + 1), "valid")
def main():
    di, do, a, b, ra, rb = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    do.mkdir(parents=True, exist_ok=True)
    R = [load(Path(di) / f"{n}.mp3") for n in range(ra, rb + 1)]
    tl = np.mean([ltas(y)[1] for y in R], 0); tf = np.median([f0med(y) for y in R])
    rep = {}
    for n in range(a, b + 1):
        y = load(Path(di) / f"{n}.mp3"); f, l, _ = ltas(y)
        g = smooth(tl - l); g = np.clip(g, -np.log(2.2), np.log(2.2)) * 0.5   # nửa log-năng lượng = biên độ; giới hạn ±7 dB
        ff, tt, Z = stft(y, SR, nperseg=1024, noverlap=768)
        Z = Z * np.exp(g)[:, None]
        _, y2 = istft(Z, SR, nperseg=1024, noverlap=768)
        y2 = y2[:len(y)].astype(np.float32); y2 *= np.sqrt((y ** 2).mean() / ((y2 ** 2).mean() + 1e-12))
        p = f0med(y2); ratio = float(np.clip(tf / p, 0.88, 1.12)) if p else 1.0
        tmp = do / f"_{n}.wav"
        import wave
        with wave.open(str(tmp), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y2, -1, 1) * 32767).astype(np.int16).tobytes())
        flt = "anull"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp), "-af", flt, "-ar", "44100", "-b:a", "128k", str(do / f"{n}.mp3")], check=True)
        tmp.unlink(); rep[n] = {"f0_truoc": round(p, 1), "ti_so_cao_do": round(ratio, 3)}
    json.dump(rep, open(do / "dong_dieu.json", "w"), indent=1)
    print("xong", len(rep), "đoạn; f0 chuẩn", round(tf, 1))
main()
