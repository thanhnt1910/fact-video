"""Đọc thử giọng VieNeu-TTS v3 Turbo (CPU, ONNX) cho một đoạn kịch bản.
Cấu hình: ke-hoach/thu-giong-hai/vieneu_thu.txt
  dòng 1: mã kịch bản và danh sách số đoạn, vd "tm28 1 2 3 4 68 69 70"
  các dòng sau: tên giọng có sẵn (preset), mỗi dòng một giọng
Kết quả: assets/thu_giong/vieneu/<mã>_<giọng>.mp3 và logs/vieneu_thu.txt (danh sách giọng, thời gian chạy)."""
import json, subprocess, time, unicodedata, re
from pathlib import Path
from vieneu import Vieneu
L = [x.strip() for x in Path("ke-hoach/thu-giong-hai/vieneu_thu.txt").read_text(encoding="utf-8").splitlines() if x.strip()]
ma, *ids = L[0].split(); ids = [int(i) for i in ids]; voices = L[1:]
J = json.load(open(f"ke-hoach/thu-giong-hai/{ma}_full.json", encoding="utf-8"))
doan = [J[i - 1]["text"] for i in ids]
out = Path("assets/thu_giong/vieneu"); out.mkdir(parents=True, exist_ok=True)
log = []
tts = Vieneu()
log.append("Giọng có sẵn: " + "; ".join(f"{a} ({b})" for a, b in tts.list_preset_voices()))
def slug(s): return re.sub(r"[^a-z0-9]+", "_", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()).strip("_")
for v in voices:
    t0 = time.time()
    try:
        parts = [tts.infer(d, voice=v) for d in doan]
        import numpy as np
        sr = 48000; gap = np.zeros(int(sr * .45), np.float32)
        a = np.concatenate(sum([[p, gap] for p in parts], []))
        w = out / f"{ma}_{slug(v)}.wav"; tts.save(a, str(w))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(w), "-b:a", "128k", str(w.with_suffix(".mp3"))], check=True); w.unlink()
        log.append(f"{v}: OK {time.time()-t0:.0f}s")
    except Exception as e:
        log.append(f"{v}: LỖI {e!r}"[:300])
Path("logs").mkdir(exist_ok=True); Path("logs/vieneu_thu.txt").write_text("\n".join(log) + "\n", encoding="utf-8"); print("\n".join(log))
