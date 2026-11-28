"""Nghe thử nhiều giọng VieNeu-TTS trên đoạn mẫu Tutankhamun (giong-thu/tutankhamun.json).
Kết quả: giong-thu/vieneu-<giọng>.mp3 và logs/vieneu_tut.txt"""
import json, re, subprocess, time, unicodedata
from pathlib import Path
import numpy as np
from vieneu import Vieneu
J = json.load(open("giong-thu/tutankhamun.json", encoding="utf-8"))
doan = []
for d in J["doan"]:
    for k, v in J["pron"].items(): d = d.replace(k, v)
    doan.append(d)
out = Path("giong-thu"); out.mkdir(exist_ok=True); Path("logs").mkdir(exist_ok=True)
def slug(s): return re.sub(r"[^a-z0-9]+", "_", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()).strip("_")
tts = Vieneu(); log = []; done = []
for v in J["vieneu"]:
    t0 = time.time()
    try:
        parts = [tts.infer(d, voice=v) for d in doan]
        sr = 48000; gap = np.zeros(int(sr * .45), np.float32)
        a = np.concatenate(sum([[p, gap] for p in parts], []))
        w = out / f"vieneu-{slug(v)}.wav"; tts.save(a, str(w))
        m = w.with_suffix(".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(w), "-b:a", "128k", str(m)], check=True); w.unlink()
        log.append(f"{v}: OK {time.time()-t0:.0f}s"); done.append(f"VieNeu {v}|{m.name}")
    except Exception as e:
        log.append(f"{v}: LỖI {e!r}"[:300])
Path("logs/vieneu_tut.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
(out / "vieneu-list.txt").write_text("".join(x + "\n" for x in done), encoding="utf-8")
print("\n".join(log))
