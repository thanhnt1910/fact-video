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

# Phong cách kể chuyện lịch sử có biên độ cao thấp (video sử nghiêm túc, giọng Puck). Dùng khi đoạn có tone thuộc TONE_KE.
STYLE_KE = ("Native Vietnamese storyteller (Northern accent) narrating a stirring heroic epic of Vietnamese history, like a proud national-history broadcaster rousing an audience. "
            "Bright, resonant, energetic and commanding voice at a medium-high pitch; confident, brisk, driving pace; strong emphasis on names, titles and deeds; "
            "rising, ringing intonation on triumphs and turning points; short dramatic pauses before reveals. "
            "Never low-pitched, never sleepy, never mumbling, never whispering, no gloomy drone; solemn moments are firm and measured, not deep or slow. "
            "Clear diction, natural Vietnamese tones, full of life and fighting spirit. ")
TONE_KE = {"hook": "Hushed, gripping urgency like the opening of a thriller; voice trembles with tension on the hostage image, then rises with curiosity on the questions.",
           "tense": "Tense and urgent: low, tight voice, quicker pace, sharp emphasis, a held breath before the danger.",
           "story": "One continuous, flowing, stirring performance from start to end: keep the same bright heroic voice and energy throughout; let the pitch rise on questions, victories and the founding of the nation, and stay firm and clear (not deep or slow) in tense or sad moments.",
           "wry": "Knowing and slightly wry about the absurd chaos of the situation, rising pitch on each new claimant, never mocking any hero.",
           "warm": "Warm, lively and affectionate with a spark of admiration for a clever, bold boy; brighter and higher pitch.",
           "epic": "Proud, rising and majestic, chest-voice confidence, ringing emphasis on names and titles.",
           "grave": "Hushed, solemn and ominous, low and slow, long pauses, quiet dread.",
           "reflect": "Thoughtful and measured with gravitas, softer and lower, a long reflective pause before the closing line."}

def main():
    src, voices, out = sys.argv[1], [v for v in sys.argv[2].split(",") if v], Path(sys.argv[3])
    beats = json.loads(Path(src).read_text(encoding="utf-8"))
    for v in voices:
        d = out / v.lower(); d.mkdir(parents=True, exist_ok=True)
        old = d / 'thoi_luong.json'; dur = json.loads(old.read_text()) if old.exists() else {}; hs = d / 'hash.json'; H = json.loads(hs.read_text()) if hs.exists() else {}
        for b in beats:
            import hashlib; hh = hashlib.md5((b['text']+b['tone']+v).encode()).hexdigest()
            if H.get(str(b['n'])) == hh and (d / f"{b['n']}.mp3").exists() and str(b['n']) in dur: continue
            style = (STYLE_KE + TONE_KE[b["tone"]]) if b["tone"] in TONE_KE else STYLE_HAI + TONE[b["tone"]]
            try:
                wav = gemini_tts.synth(b["text"], style, v)
            except Exception as e:
                print("LỖI", v, b["n"], str(e)[:200], flush=True); continue
            w = d / f"{b['n']}.wav"; w.write_bytes(wav)
            mp3 = d / f"{b['n']}.mp3"
            subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(w),"-af",audio_fx.VOICE_CHAIN,"-ar","44100","-b:a","128k",str(mp3)],check=True)
            w.unlink()
            with wave.open(io.BytesIO(wav)) as f: dur[str(b["n"])] = f.getnframes()/f.getframerate()
            H[str(b['n'])] = hh; hs.write_text(json.dumps(H)); (d / 'thoi_luong.json').write_text(json.dumps(dur))
            print("OK", v, b["n"], round(dur[str(b['n'])],1), flush=True)
        (d / "thoi_luong.json").write_text(json.dumps(dur), encoding="utf-8")
if __name__ == "__main__": main()
