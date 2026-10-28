"""Ghép tiếng động (tự tổng hợp, không dính bản quyền) vào video Góc IoT theo mốc hình.
Dùng: python goc-iot/sfx_video.py <thư mục có events.json> <video.mp4 không tiếng> <ra.mp4> [âm lượng]
events.json do dung_hinh.cjs xuất ra (chế độ test hoặc full). Giọng đọc, khi có, nên trộn thêm sau."""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import audio_fx

def main():
    d, vin, vout = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    vol = float(sys.argv[4]) if len(sys.argv) > 4 else 0.6
    info = json.loads((d / "events.json").read_text(encoding="utf-8"))
    sr = audio_fx.SFX_SR
    n = int((info["total"] + 1.0) * sr)
    track = np.zeros(n)
    for e in info["events"]:
        clip = audio_fx.get_sfx(e["name"]) * e["gain"]
        st = int(max(0.0, e["t"]) * sr)
        en = min(n, st + len(clip))
        track[st:en] += clip[:en - st]
    track = np.clip(track * vol, -1, 1)
    wav = d / "sfx.wav"
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((track * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vin, "-i", str(wav), "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", vout], check=True)
    print("ok", vout, len(info["events"]), "tiếng động")

if __name__ == "__main__":
    main()
