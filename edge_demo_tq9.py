"""Đọc thử 10 câu đầu TQ9 bằng Edge TTS (miễn phí, không giới hạn theo khóa), thử vài mức cao độ và tốc độ,
đo cao độ trung vị (F0) để so với giọng mẫu nghe_C1 (113 Hz)."""
import asyncio, subprocess, json, sys, wave
from pathlib import Path
import numpy as np, edge_tts
import am_thanh, gemini_tts
s = json.load(open("scripts/TQ9.json", encoding="utf-8"))
beats = [b["text"] for c in s["long"]["chapters"] for b in c["beats"]][:10]
tu = am_thanh.load_dict()
texts = [am_thanh.chuan_hoa(gemini_tts.clean_text(t)[0], tu) for t in beats]
out = Path("assets/thu_giong_hai/edge"); out.mkdir(parents=True, exist_ok=True)
VOICE = "vi-VN-NamMinhNeural"
CFG = [("goc", "+0Hz", "+0%"), ("t10", "-10Hz", "-5%"), ("t20", "-20Hz", "-5%"), ("t30", "-30Hz", "-8%")]

def f0(path):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "/tmp/_f.wav"], check=True)
    w = wave.open("/tmp/_f.wav"); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float); sr = 16000
    win = int(.04 * sr); lo, hi = int(sr / 300), int(sr / 60); v = []
    for i in range(0, len(x) - win, int(.02 * sr)):
        f = x[i:i + win]
        if np.sqrt((f ** 2).mean()) < 300: continue
        f = f - f.mean(); ac = np.correlate(f, f, "full")[win - 1:]; ac /= ac[0] + 1e-9
        k = lo + np.argmax(ac[lo:hi])
        if ac[k] > .5: v.append(sr / k)
    return float(np.median(v)), float(np.percentile(v, 10)), float(np.percentile(v, 90))

async def main():
    for name, pitch, rate in CFG:
        parts = []
        for i, t in enumerate(texts, 1):
            p = out / f"_{name}_{i:02d}.mp3"
            await edge_tts.Communicate(t, VOICE, rate=rate, pitch=pitch).save(str(p)); parts.append(p)
        lst = out / f"_{name}.txt"
        sil = out / "_sil.mp3"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.6", "-b:a", "96k", str(sil)], check=True)
        lst.write_text("".join(f"file '{p.resolve()}'\nfile '{sil.resolve()}'\n" for p in parts))
        res = out / f"edge_NamMinh_{name}.mp3"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-ar", "24000", "-b:a", "96k", str(res)], check=True)
        m, a, b = f0(res)
        print(f"{name}: pitch {pitch} rate {rate} -> F0 trung vị {m:.0f} Hz (p10 {a:.0f}, p90 {b:.0f}); mẫu nghe_C1: 113 Hz (p10 92, p90 167)", flush=True)
        for p in parts: p.unlink()
asyncio.run(main())
