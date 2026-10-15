"""Dựng thử video xem trước (KHÔNG giọng đọc): mỗi cảnh = clip (nếu có) hoặc ảnh tĩnh phóng nhẹ, kèm phụ đề lời kể.
  python dung_thu.py TQ2           -> assets/dung_thu/TQ2_dung_thu.mp4 (1280x720, 24 fps)
Thời lượng mỗi cảnh ước theo độ dài lời kể (~14 ký tự/giây). Clip lấy theo thứ tự ưu tiên:
assets/clips_2d/<mã>/<số>.mp4 (Veo; bỏ các clip thử Wan trong BO_QUA) và assets/clips_2d/<mã>_nhe/<số>.mp4 (hoạt hình nhẹ).
Cảnh thuộc nhóm hoạt hình nhẹ (có trong <mã>_nhe.json) luôn dùng bản nhẹ, không dùng Veo."""
import json
import subprocess
import sys
import textwrap
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BO_QUA = {"TQ2": {"003", "041", "050"}}  # clip thử Wan (giật)
W, H, FPS = 1280, 720, 24
FONT = ROOT / "assets" / "fonts" / "Lora-Variable.ttf"


def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr[-600:])


def seg(i, k, text, dur, clip, out, work):
    tf = work / f"{i:03d}.txt"
    tf.write_text("\n".join(textwrap.wrap(text, 62)[:3]), encoding="utf-8")
    dt = (f"drawtext=fontfile={FONT}:textfile={tf}:fontcolor=white:fontsize=26:line_spacing=6:box=1:boxcolor=black@0.6:boxborderw=12:"
          f"x=(w-text_w)/2:y=h-text_h-34")
    if clip:
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},tpad=stop_mode=clone:stop_duration=30,trim=duration={dur:.2f},{dt}"
        sh("ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(clip), "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p", str(out))
    else:
        n = int(dur * FPS)
        vf = (f"scale=2560:-1,zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},{dt}")
        sh("ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(ROOT / "assets" / "anh_2d" / ID / f"{k}.jpg"), "-vf", vf, "-an",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p", str(out))


def main():
    global ID
    ID = sys.argv[1]
    script = json.loads((ROOT / "scripts" / f"{ID}.json").read_text(encoding="utf-8"))
    nhe = set(json.loads((ROOT / "ke-hoach" / "nhan-vat" / f"{ID}_nhe.json").read_text(encoding="utf-8"))["anh"])
    work = ROOT / "assets" / "dung_thu" / "tmp"
    work.mkdir(parents=True, exist_ok=True)
    jobs, rows = [], []
    for ch in script["long"]["chapters"]:
        for b in ch["beats"]:
            k = Path(b["anh_file"]).stem
            veo = ROOT / "assets" / "clips_2d" / ID / f"{k}.mp4"
            lt = ROOT / "assets" / "clips_2d" / f"{ID}_nhe" / f"{k}.mp4"
            clip = lt if (k in nhe and lt.exists()) else (veo if veo.exists() and k not in BO_QUA.get(ID, ()) and k not in nhe else None)
            dur = max(3.0, len(b["text"]) / 14 + 0.4)
            i = len(jobs)
            jobs.append((i, k, b["text"], dur, clip, work / f"{i:03d}.mp4", work))
            rows.append((k, "nhe" if clip and clip == lt else ("veo" if clip else "tinh"), dur))
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(lambda a: seg(*a), jobs))
    lst = work / "list.txt"
    lst.write_text("".join(f"file '{j[5]}'\n" for j in jobs))
    out = ROOT / "assets" / "dung_thu" / f"{ID}_dung_thu.mp4"
    sh("ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out))
    tot = sum(r[2] for r in rows)
    for t in ("veo", "nhe", "tinh"):
        print(t, sum(1 for r in rows if r[1] == t))
    print(f"tổng ~{tot/60:.1f} phút ->", out)


if __name__ == "__main__":
    main()
