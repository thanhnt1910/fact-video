"""Đọc thử TỪNG CÂU của TQ9 bằng đúng cách video dài sẽ đọc (cùng chỉ dẫn giọng, cân âm lượng từng câu).
Dùng: python doc_mau_tq9.py 1-10  -> assets/thu_giong_hai/TQ9_NNN.mp3 và TQ9_mau.mp3 (ghép liền)"""
import array, json, subprocess, sys, tempfile
from pathlib import Path
import make_video as mv
import long_video as L
import am_thanh, gemini_tts

a, b = [int(x) for x in sys.argv[1].split("-")]
s = json.load(open("scripts/TQ9.json", encoding="utf-8"))
beats = [x for c in s["long"]["chapters"] for x in c["beats"]]
tu = am_thanh.load_dict()
extra = (am_thanh.sac_thai("hook", False) + " " + s.get("giong_them", "")).strip()
out = Path("assets/thu_giong_hai"); out.mkdir(parents=True, exist_ok=True)
work = Path(tempfile.mkdtemp()); full = array.array("h")
for i in range(a, b + 1):
    t = gemini_tts.clean_text(beats[i - 1]["text"])[0]
    one = L._can_am_luong(L.chapter_audio(am_thanh.chuan_hoa(t, tu), s["long"]["voice"], work, extra))
    wav = work / f"{i:03d}.wav"; mv.write_wav(wav, one)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(wav), "-b:a", "96k", str(out / f"TQ9_{i:03d}.mp3")], check=True)
    full.extend(one); full.extend(mv.silence(0.35))
    print("🎙️", i, round(len(one) / 24000, 1), "giây", flush=True)
mv.write_wav(work / "mau.wav", full)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(work / "mau.wav"), "-b:a", "96k", str(out / "TQ9_mau.mp3")], check=True)
