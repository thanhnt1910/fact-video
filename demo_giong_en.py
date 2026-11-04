"""
Nghe thử giọng Gemini TTS cho kênh tiếng Anh (History Mysteries Daily).
  python demo_giong_en.py "Charon,Orus,Enceladus"
Kết quả: demo/gemini-en-<giọng>.mp3 và demo/list.txt (để workflow gửi Telegram).

Dùng lại gemini_tts.synth của repo (nhiều khóa, tự đổi model), chỉ khác lời dặn giọng và đoạn văn là tiếng Anh.
Với model cũ (generateContent) gemini_tts dặn "Vietnamese text" nên ở đây thay bằng bản dặn tiếng Anh,
không sửa file gemini_tts.py dùng chung.
"""
import base64
import sys
from pathlib import Path

import audio_fx
import gemini_tts
import make_video as mv

ROOT = Path(__file__).resolve().parent
DEFAULT = ["Charon", "Orus", "Enceladus"]
DESC = {"Charon": "Nam - truyền đạt", "Orus": "Nam - chắc giọng", "Enceladus": "Nam - hồi hộp"}

STYLE = (
    "Native American English narrator for a documentary channel about real historical mysteries. "
    "Calm, serious and slightly hushed, like telling a true story late at night. "
    "Clear diction, steady medium pace. Slow down and lower the voice before a surprising fact, "
    "then reveal it with quiet intensity. Leave a short natural pause between sentences. "
    "Never robotic, never news-anchor flat."
)

# Đoạn đầu Script 1 (Roanoke), khoảng 30 giây.
TEXT = (
    "In 1587, more than one hundred English settlers built a colony on Roanoke Island. "
    "Then their leader, John White, sailed home for supplies. "
    "War with Spain kept him away for almost three years. "
    "When he finally returned in August 1590, the village was empty. "
    "There was no sign of a fight.\n\n"
    "Carved into a post was a single word: CROATOAN. "
    "On a nearby tree were three letters: C, R, O. "
    "That was all. The colonists were never seen again."
)


def _synth_generate_en(model, text, style, voice, key):
    prompt = f"{style}\n\nRead the following English text aloud exactly as written:\n{text}"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    res = gemini_tts._post(f"{gemini_tts.API}/models/{model}:generateContent", body, key)
    part = res["candidates"][0]["content"]["parts"][0]["inlineData"]
    return gemini_tts._wav_from_any(base64.b64decode(part["data"]), part.get("mimeType", ""))


gemini_tts._synth_generate = _synth_generate_en


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else ",".join(DEFAULT)
    voices = [v.strip() for v in arg.split(",") if v.strip()]
    out = ROOT / "demo"
    out.mkdir(exist_ok=True)
    work = ROOT / "output" / "_gemini_en"
    work.mkdir(parents=True, exist_ok=True)

    done = []
    for v in voices:
        print(f"\n== {v} ==", flush=True)
        try:
            wav = gemini_tts.synth(TEXT, STYLE, v)
        except Exception as e:
            print(f"LỖI {v}: {e}", flush=True)
            continue
        raw = work / f"{v}.wav"
        raw.write_bytes(wav)
        mp3 = out / f"gemini-en-{v.lower()}.mp3"
        mv.run_ffmpeg(["-i", str(raw), "-af", f"{audio_fx.VOICE_CHAIN},loudnorm=I=-14:TP=-1.5:LRA=11",
                       "-ar", "44100", "-b:a", "128k", str(mp3)])
        done.append(f"Gemini EN {v} ({DESC.get(v, '')})|{mp3.name}")
        print(f"OK {v}", flush=True)
    (out / "list.txt").write_text("".join(x + "\n" for x in done), encoding="utf-8")
    if not done:
        sys.exit(1)


if __name__ == "__main__":
    main()
