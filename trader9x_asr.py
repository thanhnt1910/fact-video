"""Nhận dạng giọng từng đoạn (faster-whisper) và so với kịch bản: báo đoạn thừa/thiếu chữ."""
import json, sys, re, difflib
from pathlib import Path
from faster_whisper import WhisperModel

def norm(s):
    return re.sub(r"[^\w\s]", " ", s.lower()).split()

cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
voice = sys.argv[2] if len(sys.argv) > 2 else cfg["giong_chinh"]
m = WhisperModel("medium", device="cpu", compute_type="int8")
out = []
for s in cfg["doan"]:
    p = Path("assets/trader9x") / cfg["ma"] / voice / f"{s['id']}.wav"
    if not p.exists(): continue
    segs, _ = m.transcribe(str(p), language="vi", beam_size=5, vad_filter=False)
    txt = " ".join(x.text.strip() for x in segs)
    a, b = norm(s["text"]), norm(txt)
    r = difflib.SequenceMatcher(None, a, b).ratio()
    out.append({"id": s["id"], "khop": round(r, 3), "kich_ban": s["text"], "nghe": txt})
    print(f"{'✅' if r >= .8 else '⚠️'} {s['id']:9s} {r:.2f} | {txt}", flush=True)
Path(f"trader9x/asr_{cfg['ma']}_{voice}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
