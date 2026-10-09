"""
So sánh giọng: Gemini Sadaltager (gốc) và VieNeu nhân bản theo mẫu Sadaltager (miễn phí, không giới hạn).
  1) Gemini đọc 1 câu mẫu ~8 giây  -> giong-mau/sadaltager-ref.wav (dùng làm giọng mẫu cho VieNeu)
  2) Gemini đọc đoạn đầu chuyện 1518 -> demo/so-sanh-1-gemini.mp3
  3) VieNeu nhân bản đọc cùng đoạn   -> demo/so-sanh-2-vieneu-nhan-ban.mp3
  4) VieNeu giọng có sẵn đang dùng   -> demo/so-sanh-3-vieneu-hien-tai.mp3
"""
import array
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

import audio_fx
import gemini_tts
import make_video as mv

ROOT = Path(__file__).resolve().parent
VOICE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else "Sadaltager"
REF_TEXT = ("Năm một nghìn năm trăm mười tám, ở một thành phố châu Âu, "
            "đã xảy ra một chuyện kỳ lạ mà đến nay vẫn chưa ai giải thích được.")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def to_mp3(src, dst):
    mv.run_ffmpeg(["-i", str(src), "-af", f"{audio_fx.VOICE_CHAIN},loudnorm=I=-14:TP=-1.5:LRA=11",
                   "-ar", "44100", "-b:a", "128k", str(dst)])


def trim_ref(wav_bytes, out, max_sec=8.0):
    """Cắt mẫu ≤ 8 giây tại khoảng lặng gần nhất, 24 kHz mono."""
    tmp = out.with_suffix(".raw.wav")
    tmp.write_bytes(wav_bytes)
    mv.run_ffmpeg(["-i", str(tmp), "-ac", "1", "-ar", "24000", str(tmp.with_suffix(".24k.wav"))])
    with wave.open(str(tmp.with_suffix(".24k.wav"))) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64)
    sr = 24000
    win = int(0.03 * sr)
    k = len(x) // win
    rms = np.sqrt((x[:k * win].reshape(k, win) ** 2).mean(1))
    quiet = rms < max(300, np.percentile(rms, 20))
    end = len(x)
    if len(x) > max_sec * sr:
        lim = int(max_sec * sr / win)
        cand = [i for i in range(int(4 * sr / win), lim) if quiet[i]]
        end = (cand[-1] if cand else lim) * win
    start = 0
    while start < k and quiet[start]:
        start += 1
    y = x[start * win:end].astype(np.int16)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(y.tobytes())
    print(f"Mẫu giọng: {len(y) / sr:.1f} giây -> {out}")


def main():
    script = json.loads((ROOT / "scripts" / "SL1.json").read_text(encoding="utf-8"))
    script["scenes"] = script["scenes"][:4]
    out = ROOT / "demo"
    out.mkdir(exist_ok=True)
    work = ROOT / "output" / "_clone"
    work.mkdir(parents=True, exist_ok=True)
    ref = ROOT / "giong-mau" / f"{VOICE.lower()}-ref.wav"
    ref.parent.mkdir(exist_ok=True)
    done = []

    # 1) mẫu giọng
    if not ref.exists():
        style = gemini_tts.BASE_STYLE + " Calm, clear, steady pace, neutral storytelling tone."
        trim_ref(gemini_tts.synth(REF_TEXT, style, VOICE), ref)

    # 2) Gemini đọc đoạn mẫu
    pron = script.get("pronounce", {})
    parts = [gemini_tts.clean_text(s["voice"], pron)[0] for s in script["scenes"]]
    try:
        wav = gemini_tts.synth("\n\n".join(parts), gemini_tts.BASE_STYLE + " Leave a short beat between paragraphs.", VOICE)
        (work / "gemini.wav").write_bytes(wav)
        to_mp3(work / "gemini.wav", out / "so-sanh-1-gemini.mp3")
        done.append(f"1. Gemini {VOICE} (gốc, có giới hạn lượt)|so-sanh-1-gemini.mp3")
    except Exception as e:
        print("Gemini lỗi:", e)

    # 3) VieNeu nhân bản theo mẫu, 4) VieNeu giọng hiện tại
    for tag, use_ref, name in [("2", True, "VieNeu nhân bản theo mẫu " + VOICE + " (miễn phí, không giới hạn)"),
                               ("3", False, "VieNeu giọng đang dùng")]:
        cfg = mv.load_config()
        cfg["vieneu"]["ref_audio"] = str(ref) if use_ref else ""
        w = work / ("ref" if use_ref else "preset")
        w.mkdir(exist_ok=True)
        try:
            scenes = mv.voices_vieneu(script, cfg, w)
        except Exception as e:
            print(f"VieNeu lỗi ({name}):", e)
            continue
        audio = array.array("h")
        for samples, _ in scenes:
            audio.extend(samples)
            audio.extend(mv.silence(0.45))
        mv.write_wav(w / "demo.wav", audio)
        fname = f"so-sanh-{tag}-{'vieneu-nhan-ban' if use_ref else 'vieneu-hien-tai'}.mp3"
        to_mp3(w / "demo.wav", out / fname)
        done.append(f"{tag}. {name}|{fname}")
    (out / "list.txt").write_text("".join(x + "\n" for x in done), encoding="utf-8")
    print("\n".join(done))
    if not done:
        sys.exit(1)


if __name__ == "__main__":
    main()
