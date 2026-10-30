"""Dựng thử cảnh bản đồ vector mới: python phim_ban_do/vecmap/ve.py still 0 3 6 9.5 | clip 10
Khung hình do trình duyệt vẽ từng thời điểm (T(t)), ghép bằng ffmpeg."""
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / "ra"
OUT.mkdir(exist_ok=True)


def main():
    mode, args = sys.argv[1], sys.argv[2:]
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto((HERE / "trang.html").as_uri())
        pg.evaluate("window.ready")
        if mode == "still":
            for a in args:
                pg.evaluate(f"T({a})")
                pg.screenshot(path=str(OUT / f"khung_{a}.jpg"), type="jpeg", quality=90)
                print("ok", a)
        else:
            dur, fps = float(args[0]), 30
            n = int(dur * fps)
            fr = OUT / "fr"
            fr.mkdir(exist_ok=True)
            for i in range(n):
                pg.evaluate(f"T({i / fps})")
                pg.screenshot(path=str(fr / f"{i:04d}.jpg"), type="jpeg", quality=88)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(fr / "%04d.jpg"),
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                            str(OUT / "thu_bando.mp4")], check=True)
            print("xong", OUT / "thu_bando.mp4")
        b.close()


main()
