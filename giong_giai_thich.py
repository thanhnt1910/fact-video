"""Đọc video kiến thức từng câu một, giọng Puck, kiểu giải thích rõ ràng:
python giong_giai_thich.py <file.json> <giọng> <thư mục ra>   (json: [{n,text}])"""
import json, subprocess, sys, wave, io, hashlib
from pathlib import Path
import gemini_tts, audio_fx, am_thanh

STYLE = ("Native Vietnamese narrator (Northern accent) of a short knowledge video: confident, clear, "
         "friendly and punchy, medium-fast pace, natural tones, slight urgency on the first line. "
         "Never robotic, never news-anchor flat. ")

def main():
    src, v, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    beats = json.loads(Path(src).read_text(encoding="utf-8"))
    d = out / v.lower(); d.mkdir(parents=True, exist_ok=True)
    jd, jh = d / "thoi_luong.json", d / "hash.json"
    dur = json.loads(jd.read_text()) if jd.exists() else {}
    H = json.loads(jh.read_text()) if jh.exists() else {}
    for b in beats:
        n = str(b["n"]); text = am_thanh.chuan_hoa(b["text"])
        hh = hashlib.md5((text + v).encode()).hexdigest()
        if H.get(n) == hh and (d / f"{n}.mp3").exists() and n in dur: continue
        try:
            wav = gemini_tts.synth(text, STYLE, v)
        except Exception as e:
            print("LỖI", n, str(e)[:200], flush=True); continue
        w = d / f"{n}.wav"; w.write_bytes(wav)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(w),"-af",audio_fx.VOICE_CHAIN,
                        "-ar","44100","-b:a","128k",str(d / f"{n}.mp3")], check=True)
        w.unlink()
        with wave.open(io.BytesIO(wav)) as f: dur[n] = f.getnframes() / f.getframerate()
        H[n] = hh; jh.write_text(json.dumps(H)); jd.write_text(json.dumps(dur))
        print("OK", n, round(dur[n], 1), flush=True)
if __name__ == "__main__": main()
