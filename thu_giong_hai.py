"""Đọc thử kịch bản hài bằng Gemini TTS, từng câu một: python thu_giong_hai.py <file.json> <giọng,giọng> <thư mục ra>
Mỗi câu ra <thư mục>/<giọng>/NNN.mp3 (đã chỉnh giọng) kèm thoi_luong.json."""
import json, subprocess, sys, wave, io
from pathlib import Path
import gemini_tts, audio_fx

STYLE_HAI = ("Native Vietnamese storyteller (Northern accent) narrating a history video in a funny, witty, deadpan-comedy way, "
             "like a lively friend telling gossip about famous people: clear diction, natural tones, fast comedic timing, "
             "a sly smile in the voice, a tiny pause before each punchline, then deliver it lightly. "
             "Never robotic, never news-anchor flat. ")
TONE = {"light": "Playful and amused.",
        "calm": "Calmer and more serious for this line, only a hint of dry humour, no laughing."}

def main():
    src, voices, out = sys.argv[1], [v for v in sys.argv[2].split(",") if v], Path(sys.argv[3])
    beats = json.loads(Path(src).read_text(encoding="utf-8"))
    for v in voices:
        d = out / v.lower(); d.mkdir(parents=True, exist_ok=True); dur = {}
        for b in beats:
            style = STYLE_HAI + TONE[b["tone"]]
            try:
                wav = gemini_tts.synth(b["text"], style, v)
            except Exception as e:
                print("LỖI", v, b["n"], str(e)[:200], flush=True); continue
            w = d / f"{b['n']}.wav"; w.write_bytes(wav)
            mp3 = d / f"{b['n']}.mp3"
            subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(w),"-af",audio_fx.VOICE_CHAIN,"-ar","44100","-b:a","128k",str(mp3)],check=True)
            w.unlink()
            with wave.open(io.BytesIO(wav)) as f: dur[b["n"]] = f.getnframes()/f.getframerate()
            print("OK", v, b["n"], round(dur[b["n"]],1), flush=True)
        (d / "thoi_luong.json").write_text(json.dumps(dur), encoding="utf-8")
if __name__ == "__main__": main()
