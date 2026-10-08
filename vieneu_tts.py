"""
Cầu nối giọng đọc VieNeu-TTS. Chạy bằng Python trong .venv-tts (Python 3.12),
được make_video.py gọi tự động. Có thể chạy tay:

  .venv-tts\\Scripts\\python.exe vieneu_tts.py --list
  .venv-tts\\Scripts\\python.exe vieneu_tts.py --samples          # đọc thử câu mẫu bằng mọi giọng có sẵn
  .venv-tts\\Scripts\\python.exe vieneu_tts.py --samples --ref giong-mau\\giong-cua-toi.wav
  .venv-tts\\Scripts\\python.exe vieneu_tts.py jobs.json           # dùng nội bộ
"""
import json
import os
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
SAMPLE = "Bạch tuộc có… ba trái tim! Nghe thật khó tin, đúng không? Nhưng đó là sự thật. Hóa ra là vậy!"


def load(mode=None):
    from vieneu import Vieneu
    t = time.time()
    tts = Vieneu(mode=mode) if mode else Vieneu()
    print(f"[vieneu] đã nạp mô hình sau {time.time() - t:.0f}s", flush=True)
    return tts


def _parse_voice(v):
    """VieNeu trả về chuỗi dạng '⭐ Hải Đăng — Nam · Bắc · Phong cách tự nhiên' (hoặc tuple/dict)."""
    if isinstance(v, dict):
        name = v.get("name") or v.get("id") or str(v)
        return name, v.get("description", name)
    if isinstance(v, (list, tuple)) and v:
        return str(v[-1]), str(v[0])
    text = str(v).replace("⭐", "").strip()
    name = text.split(" — ")[0].strip()
    return name, text


def preset_list(tts):
    raw = tts.list_preset_voices()
    return [_parse_voice(v) for v in (raw if isinstance(raw, (list, tuple)) else list(raw))]


def preset_names(tts):
    return [n for n, _ in preset_list(tts)]


def synth(tts, text, voice=None, ref=None, out=None):
    kw = {}
    if ref:
        kw["ref_audio"] = str(ref)
    elif voice:
        kw["voice"] = voice
    audio = tts.infer(text, **kw)
    tts.save(audio, str(out))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    if args[0] == "--list":
        tts = load()
        for name, desc in preset_list(tts):
            print(f"{name}    |    {desc}")
        return
    if args[0] == "--samples":
        ref = args[args.index("--ref") + 1] if "--ref" in args else None
        out_dir = ROOT / "giong-mau" / "nghe-thu"
        out_dir.mkdir(parents=True, exist_ok=True)
        tts = load()
        if ref:
            out = out_dir / ("nhan-ban_" + Path(ref).stem + ".wav")
            synth(tts, SAMPLE, ref=ref, out=out)
            print(f"[vieneu] {out.name}", flush=True)
            return
        for n in preset_names(tts):
            safe = "".join(c if c.isalnum() else "-" for c in n)
            out = out_dir / f"{safe}.wav"
            try:
                synth(tts, SAMPLE, voice=n, out=out)
                print(f"[vieneu] OK {n} -> {out.name}", flush=True)
            except Exception as e:
                print(f"[vieneu] LỖI {n}: {e}", flush=True)
        return

    # jobs.json: {"voice": "...", "ref_audio": "...", "items": [{"text": "...", "out": "..."}]}
    job = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    tts = load(job.get("mode"))
    ref = job.get("ref_audio") or None
    if ref and not Path(ref).is_absolute():
        ref = str(ROOT / ref)
    for i, it in enumerate(job["items"], 1):
        t = time.time()
        synth(tts, it["text"], voice=job.get("voice"), ref=ref, out=it["out"])
        print(f"[vieneu] câu {i}/{len(job['items'])} xong ({time.time() - t:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
