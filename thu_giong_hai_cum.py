"""Đọc kịch bản hài theo cụm câu (ít lượt gọi Gemini): python thu_giong_hai_cum.py <file.json> <giọng> <thư mục ra> [số câu mỗi cụm]
Chỉ đọc các câu còn thiếu; mỗi cụm gọi Gemini 1 lần rồi cắt thành từng câu theo khoảng lặng (như long_video.py)."""
import io, json, subprocess, sys, wave, hashlib
from pathlib import Path
import numpy as np
import gemini_tts, audio_fx
from thu_giong_hai import STYLE_HAI, TONE
SR = 24000

def split_by_pauses(samples, weights):
    """Chia âm thanh 1 chương thành các đoạn theo khoảng lặng gần nhất với tỉ lệ độ dài chữ."""
    x = np.frombuffer(samples.tobytes(), np.int16).astype(np.float32)
    win = int(0.02 * SR)
    k = len(x) // win
    rms = np.sqrt((x[:k * win].reshape(k, win) ** 2).mean(1) + 1e-6)
    speech = rms[rms > np.percentile(rms, 40)]
    thr = max(150.0, 0.1 * float(np.median(speech)) if len(speech) else 150.0)
    quiet = rms < thr
    # cắt lặng đầu/cuối
    nz = np.where(~quiet)[0]
    a, b = (nz[0], nz[-1] + 1) if len(nz) else (0, k)
    runs, i = [], a
    while i < b:
        if quiet[i]:
            j = i
            while j < b and quiet[j]:
                j += 1
            if j - i >= 12:            # ≥ 0,24 giây
                runs.append(((i + j) / 2, j - i))
            i = j
        else:
            i += 1
    total = b - a
    cum = np.cumsum(weights)[:-1] / sum(weights)
    cuts, last = [], a
    for c in cum:
        exp = a + c * total
        cands = [r for r in runs if r[0] > last + 25]
        if cands:
            best = min(cands, key=lambda r: abs(r[0] - exp) - 0.6 * r[1])
            pos = best[0] if abs(best[0] - exp) < 0.25 * total else exp
        else:
            pos = exp
        cuts.append(int(pos))
        last = pos
    bounds = [a] + cuts + [b]
    return [(bounds[n] * win, bounds[n + 1] * win) for n in range(len(bounds) - 1)], (a * win, b * win)

def main():
    src, voice, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    per = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    beats = json.loads(Path(src).read_text(encoding="utf-8"))
    d = out / voice.lower(); d.mkdir(parents=True, exist_ok=True)
    fd = d / "thoi_luong.json"; dur = json.loads(fd.read_text()) if fd.exists() else {}
    hs = d / "hash.json"; H = json.loads(hs.read_text()) if hs.exists() else {}
    todo = [b for b in beats if not (str(b["n"]) in dur and (d / f"{b['n']}.mp3").exists())]
    print("còn thiếu", len(todo), "câu", flush=True)
    chunks, cur = [], []
    for b in todo:
        if cur and (len(cur) >= per or b["n"] != cur[-1]["n"] + 1): chunks.append(cur); cur = []
        cur.append(b)
    if cur: chunks.append(cur)
    for ch in chunks:
        calm = sum(1 for b in ch if b["tone"] == "calm") > len(ch) / 2
        style = STYLE_HAI + TONE["calm" if calm else "light"] + " Read each sentence as its own beat with a clear short pause between sentences."
        text = "\n\n".join(b.get("tts", b["text"]) for b in ch)
        try: wav = gemini_tts.synth(text, style, voice)
        except Exception as e: print("LỖI cụm", ch[0]["n"], str(e)[:200], flush=True); continue
        with wave.open(io.BytesIO(wav)) as f:
            global SR; SR = f.getframerate(); x = np.frombuffer(f.readframes(f.getnframes()), np.int16)
        spans, _ = split_by_pauses(x, [max(1, len(b.get("tts", b["text"]).split())) for b in ch])
        for b, (s, e) in zip(ch, spans):
            s, e = max(0, int(s - 0.05 * SR)), min(len(x), int(e + 0.08 * SR))
            seg = x[s:e]; w = d / f"{b['n']}.wav"
            with wave.open(str(w), "wb") as o: o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes(seg.tobytes())
            mp3 = d / f"{b['n']}.mp3"
            subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(w),"-af",audio_fx.VOICE_CHAIN,"-ar","44100","-b:a","128k",str(mp3)],check=True); w.unlink()
            dur[str(b["n"])] = len(seg) / SR
            H[str(b["n"])] = hashlib.md5((b["text"]+b["tone"]+voice).encode()).hexdigest()
        hs.write_text(json.dumps(H)); fd.write_text(json.dumps(dur))
        print("OK cụm", ch[0]["n"], "-", ch[-1]["n"], round(len(x)/SR, 1), "giây", flush=True)

if __name__ == "__main__": main()
