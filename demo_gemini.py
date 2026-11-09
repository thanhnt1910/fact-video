"""
Nghe thử giọng Gemini TTS: đọc 4 cảnh đầu video Bạch tuộc bằng nhiều giọng.
  python demo_gemini.py "Sulafat,Aoede,Kore"
Kết quả: demo/gemini-<giọng>.mp3
"""
import json
import subprocess
import sys
from pathlib import Path

import audio_fx
import gemini_tts
import make_video as mv

ROOT = Path(__file__).resolve().parent
DEFAULT = ["Sulafat", "Aoede", "Despina", "Leda", "Kore", "Achernar", "Charon", "Sadaltager", "Puck"]
DESC = {"Sulafat": "Nữ - ấm áp", "Aoede": "Nữ - nhẹ nhàng", "Despina": "Nữ - mượt", "Leda": "Nữ - trẻ trung",
        "Kore": "Nữ - chắc giọng", "Achernar": "Nữ - mềm", "Charon": "Nam - truyền đạt",
        "Sadaltager": "Nam - hiểu biết", "Puck": "Nam - sôi nổi"}

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def main():
    voices = [v.strip() for v in (sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip()
                                  else ",".join(DEFAULT)).split(",") if v.strip()]
    script = json.loads((ROOT / "kich-ban-cu" / "DV1.json").read_text(encoding="utf-8"))
    scenes = script["scenes"][:4]
    out = ROOT / "demo"
    out.mkdir(exist_ok=True)
    work = ROOT / "output" / "_gemini"
    work.mkdir(parents=True, exist_ok=True)
    pron = script.get("pronounce", {})
    # Nếu có file lời thử riêng (nhánh khoa-hoc) thì đọc lời và phong cách trong đó
    own = ROOT / "ke-hoach" / "giong-thu-khoa-hoc.json"
    own_cfg = json.loads(own.read_text(encoding="utf-8")) if own.exists() else None

    # Chế độ đọc TỪNG CÂU cho video khoa học (nhánh khoa-hoc): demo/era/<giọng>/NN.wav
    # Đối số thứ hai: mã video (ví dụ cavendish) -> file giong-video-khoa-hoc-<mã>.json, ra demo/<mã>/<giọng>/NN.wav
    vkey = sys.argv[2].strip() if len(sys.argv) > 2 else ""
    vid = ROOT / "ke-hoach" / (f"giong-video-khoa-hoc-{vkey}.json" if vkey else "giong-video-khoa-hoc.json")
    if vid.exists():
        cfg = json.loads(vid.read_text(encoding="utf-8"))
        ok = 0
        for v in voices:
            d = out / (vkey or "era") / v.lower()
            d.mkdir(parents=True, exist_ok=True)
            for it in cfg["sentences"]:
                f = d / f"{it['n']:02d}.wav"
                if f.exists():
                    ok += 1
                    continue
                try:
                    f.write_bytes(gemini_tts.synth(it["say"], cfg["style"], v))
                    ok += 1
                    print(f"OK {v} {it['n']:02d}: {it['text'][:50]}", flush=True)
                except Exception as e:
                    print(f"LỖI {v} {it['n']:02d}: {e}", flush=True)
        (out / "list.txt").write_text("", encoding="utf-8")
        sys.exit(0 if ok else 1)

    # Gửi cả đoạn trong 1 lần gọi (ít tốn lượt), lời dặn tổng hợp theo từng cảnh
    parts, hints_all = [], []
    for s in scenes:
        t, hints = gemini_tts.clean_text(s["voice"], pron)
        parts.append(t)
        hints_all += hints
    text = "\n\n".join(parts)
    if own_cfg:
        text = own_cfg["text"]
    style = (gemini_tts.BASE_STYLE + " Structure: 1) hook — " + gemini_tts.SCENE_STYLE["hook"] +
             " 2) " + gemini_tts.SCENE_STYLE["compare"] + " 3-4) " + gemini_tts.SCENE_STYLE["explain"] +
             " Leave a short beat between paragraphs.")
    if hints_all:
        style += " Specific emphasis: " + "; ".join(hints_all[:6]) + "."
    if own_cfg:
        style = own_cfg["style"]
    print("STYLE:", style, "\nTEXT:", text, flush=True)

    done = []
    for v in voices:
        print(f"\n== {v} ==", flush=True)
        try:
            wav = gemini_tts.synth(text, style, v)
        except Exception as e:
            print(f"LỖI {v}: {e}", flush=True)
            continue
        raw = work / f"{v}.wav"
        raw.write_bytes(wav)
        mp3 = out / f"gemini-{v.lower()}.mp3"
        mv.run_ffmpeg(["-i", str(raw), "-af", f"{audio_fx.VOICE_CHAIN},loudnorm=I=-14:TP=-1.5:LRA=11",
                       "-ar", "44100", "-b:a", "128k", str(mp3)])
        done.append(f"Gemini {v} ({DESC.get(v, '')})|{mp3.name}")
        print(f"OK {v}", flush=True)
    (out / "list.txt").write_text("".join(x + "\n" for x in done), encoding="utf-8")
    if not done:
        sys.exit(1)


if __name__ == "__main__":
    main()
