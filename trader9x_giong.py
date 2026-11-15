"""Đọc giọng cho video Trader9x: từng đoạn một lần gọi Gemini (cum = 1), lưu wav đã xử lý.
python trader9x_giong.py trader9x/macd_cau.json
- Giọng chính đọc toàn bộ kịch bản; các giọng thử chỉ đọc 'cau_thu' để nghe so sánh.
- Đoạn đã có file thì bỏ qua (chạy lại chỉ đọc phần còn thiếu). Mọi khóa hết lượt thì dừng, giữ phần đã đọc."""
import json, subprocess, sys, wave
from pathlib import Path
import gemini_tts, audio_fx

def doc(text, style, voice, out):
    if out.exists():
        return "có sẵn"
    raw = out.with_suffix(".raw.wav")
    raw.write_bytes(gemini_tts.synth(text, style, voice))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af",
                    audio_fx.VOICE_CHAIN + ",loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "1", str(out)], check=True)
    raw.unlink()
    with wave.open(str(out)) as w:
        return f"{w.getnframes() / w.getframerate():.2f}s"

def main():
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    root = Path("assets/trader9x") / cfg["ma"]
    jobs = [(cfg["giong_chinh"], s) for s in cfg["doan"]]
    jobs += [(v, s) for v in cfg.get("giong_thu", []) for s in cfg["doan"] if s["id"] in cfg.get("cau_thu", [])]
    ok = loi = 0
    for voice, s in jobs:
        out = root / voice / f"{s['id']}.wav"
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            r = doc(s["text"], cfg["style"], voice, out)
            ok += 1
            print(f"✅ {voice:11s} {s['id']:9s} {r}", flush=True)
        except Exception as e:
            loi += 1
            print(f"❌ {voice:11s} {s['id']:9s} {str(e)[:200]}", flush=True)
            if "hết lượt" in str(e):
                print("Mọi khóa Gemini hết lượt: dừng, lần sau đọc tiếp phần còn thiếu.")
                break
    print(f"Xong: {ok} đoạn có giọng, {loi} lỗi.")

if __name__ == "__main__":
    main()
