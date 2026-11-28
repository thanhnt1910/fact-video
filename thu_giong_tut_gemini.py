"""Nghe thử nhiều giọng Gemini TTS trên đoạn mẫu Tutankhamun (giong-thu/tutankhamun.json).
Kết quả: giong-thu/gemini-<giọng>.mp3 và giong-thu/gemini-list.txt"""
import json, sys
from pathlib import Path
import audio_fx, gemini_tts
import make_video as mv
ROOT = Path(__file__).resolve().parent
J = json.loads((ROOT / "giong-thu" / "tutankhamun.json").read_text(encoding="utf-8"))
out = ROOT / "giong-thu"; work = ROOT / "output" / "_gemini_tut"; work.mkdir(parents=True, exist_ok=True)
text = "\n\n".join(gemini_tts.clean_text(d, J["pron"])[0] for d in J["doan"])
style = (gemini_tts.BASE_STYLE + " This is a calm, precise 'fact-checker' narrator investigating a famous legend: "
         "steady and curious, not theatrical. Pause about half a second before the reveal that starts with 'Kết quả'. "
         "Leave a short beat between paragraphs.")
print("TEXT:", text, flush=True)
done = []
for v in J["gemini"]:
    print(f"== {v} ==", flush=True)
    try:
        wav = gemini_tts.synth(text, style, v)
    except Exception as e:
        print(f"LỖI {v}: {e}", flush=True); continue
    raw = work / f"{v}.wav"; raw.write_bytes(wav)
    mp3 = out / f"gemini-{v.lower()}.mp3"
    mv.run_ffmpeg(["-i", str(raw), "-af", f"{audio_fx.VOICE_CHAIN},loudnorm=I=-14:TP=-1.5:LRA=11",
                   "-ar", "44100", "-b:a", "128k", str(mp3)])
    done.append(f"Gemini {v}|{mp3.name}"); print(f"OK {v}", flush=True)
(out / "gemini-list.txt").write_text("".join(x + "\n" for x in done), encoding="utf-8")
if not done: sys.exit(1)
