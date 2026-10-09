"""
Tạo file nghe thử giọng đọc (chỉ có giọng, không hình) cho nhiều giọng VieNeu.

  python demo_voices.py "Ngọc Linh,Thục Đoan,Thiện Minh"   # danh sách giọng
  python demo_voices.py                                    # dùng danh sách mặc định

Kết quả: demo/<tên-giọng>.mp3 (đã có nhấn nhá + xử lý giọng như video thật).
"""
import json
import sys
import time
from pathlib import Path

import audio_fx
import make_video as mv

ROOT = Path(__file__).resolve().parent
DEFAULT = ["Ngọc Linh", "Thục Đoan", "Quỳnh Anh", "Mỹ Duyên", "Kim Thanh", "Trúc Ly",
           "Ngọc Huyền", "Đoan Trang", "Thiện Minh", "Thanh Bình", "Thái Sơn"]
DEMO_SCRIPT = "kich-ban-cu/DV1.json"
DEMO_SCENES = 4  # ~20–25 giây

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def slug(name):
    import unicodedata
    s = unicodedata.normalize("NFD", name).encode("ascii", "ignore").decode().replace("Đ", "D").replace("đ", "d")
    return "".join(c if c.isalnum() else "-" for c in s).strip("-").lower() or "giong"


def main():
    voices = [v.strip() for v in (sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else ",".join(DEFAULT)).split(",") if v.strip()]
    script = json.loads((ROOT / DEMO_SCRIPT).read_text(encoding="utf-8"))
    script["scenes"] = script["scenes"][:DEMO_SCENES]
    out_dir = ROOT / "demo"
    out_dir.mkdir(exist_ok=True)
    done = []
    for v in voices:
        t = time.time()
        cfg = mv.load_config()
        cfg["vieneu"]["voice"] = v
        cfg["vieneu"]["ref_audio"] = ""
        work = ROOT / "output" / "_demo" / slug(v)
        work.mkdir(parents=True, exist_ok=True)
        print(f"\n== {v} ==", flush=True)
        try:
            scenes = mv.voices_vieneu(script, cfg, work)
        except Exception as e:
            print(f"LỖI {v}: {e}", flush=True)
            continue
        audio = mv.array.array("h")
        for samples, _ in scenes:
            audio.extend(samples)
            audio.extend(mv.silence(0.45))
        raw = work / "demo.wav"
        mv.write_wav(raw, audio)
        mp3 = out_dir / f"{slug(v)}.mp3"
        mv.run_ffmpeg(["-i", str(raw), "-af", f"{audio_fx.VOICE_CHAIN},loudnorm=I=-14:TP=-1.5:LRA=11",
                       "-ar", "44100", "-b:a", "128k", str(mp3)])
        done.append(f"{v}|{mp3.name}")
        print(f"OK {v} -> {mp3.name} ({time.time() - t:.0f}s)", flush=True)
    (ROOT / "demo" / "list.txt").write_text("\n".join(done) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
