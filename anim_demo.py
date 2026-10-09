"""
Đoạn mẫu 15 giây kiểu HOẠT HÌNH CẮT GIẤY (16:9): ảnh AI (FLUX, Cloudflare) -> tách nền -> cho nhân vật chuyển động.
Chuyện: bà Troffea nhảy múa giữa phố Strasbourg 1518, đám đông lần lượt kéo đến nhảy theo.
Kết quả: demo/anim-demo.mp4
"""
import json
import subprocess
import sys
from pathlib import Path

import ai_images
import make_video as mv
import music

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "ai" / "demo"
FPS = 30
TOTAL = 15.0

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BG = ("a narrow medieval street in Strasbourg in 1518, half-timbered houses on both sides, cobblestone ground, "
      "a gothic cathedral spire in the distance, summer afternoon, empty street, wide establishing shot, eye level")
CHARS = [
    # id, prompt, seed
    ("troffea", "a medieval peasant woman in a long red dress and white linen headscarf dancing wildly, "
                "both arms raised above her head, one knee lifted, eyes closed, ecstatic", 11),
    ("man", "a medieval peasant man in a brown wool tunic and hose dancing frantically, arms flailing, exhausted face", 23),
    ("woman", "a medieval townswoman in a blue dress and white apron dancing with arms spread wide, skirt swirling", 37),
    ("old", "an old medieval man with a long grey beard and a wooden walking stick dancing clumsily", 41),
    ("piper", "a medieval street musician with a feathered cap playing the bagpipes, standing, side view", 53),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("▶️  Vẽ ảnh bằng FLUX (Cloudflare Workers AI)")
    bg = ai_images.generate(BG, OUT / "bg.jpg", seed=7)
    cuts = {}
    for cid, prompt, seed in CHARS:
        raw = ai_images.generate(prompt, OUT / f"{cid}.jpg", cutout=True, seed=seed)
        cuts[cid] = ai_images.cutout(raw, OUT / f"{cid}.png")
    print("✂️  Đã tách nền", len(cuts), "nhân vật")

    U = lambda p: Path(p).resolve().as_uri()
    data = {
        "total": TOTAL, "channel": "Người Gác Sử", "bg": U(bg),
        "chars": [
            {"src": U(cuts["troffea"]), "x": 0.50, "ground": 70, "h": 640, "depth": 0.0, "enter": 0.3, "from": "right",
             "walk": 1.8, "amp": 42, "sway": 10, "speed": 6.5, "flip": True},
            {"src": U(cuts["man"]), "x": 0.27, "ground": 120, "h": 600, "depth": 0.35, "enter": 5.0, "from": "left",
             "amp": 30, "sway": 9, "speed": 6.0, "phase": 0.4},
            {"src": U(cuts["woman"]), "x": 0.73, "ground": 120, "h": 600, "depth": 0.35, "enter": 6.6, "from": "right",
             "amp": 32, "sway": 8, "speed": 6.3, "phase": 1.1, "flip": True},
            {"src": U(cuts["old"]), "x": 0.12, "ground": 150, "h": 560, "depth": 0.6, "enter": 8.2, "from": "left",
             "amp": 18, "sway": 6, "speed": 5.0, "phase": 0.7},
            {"src": U(cuts["piper"]), "x": 0.88, "ground": 150, "h": 560, "depth": 0.6, "enter": 9.6, "from": "right",
             "amp": 6, "sway": 3, "speed": 3.0, "faceLeft": True},
        ],
        "captions": [
            {"t0": 0.6, "t1": 4.6, "text": "Strasbourg · **Tháng 7 năm 1518**"},
            {"t0": 4.9, "t1": 9.4, "text": "Một người phụ nữ bắt đầu nhảy… và **không dừng lại**"},
            {"t0": 9.7, "t1": 14.6, "text": "Vài ngày sau, **hơn 30 người** nhảy theo"},
        ],
    }

    from playwright.sync_api import sync_playwright
    demo = ROOT / "demo"
    demo.mkdir(exist_ok=True)
    silent = demo / "anim-demo-silent.mp4"
    n = int(TOTAL * FPS)
    cmd = [mv.ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS),
           "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           str(silent)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": 1920, "height": 1080})
        page.goto((ROOT / "templates" / "cutout.html").as_uri())
        page.evaluate("d => window.setup(d)", data)
        page.wait_for_timeout(300)
        for i in range(n):
            page.evaluate(f"window.renderAt({i / FPS})")
            proc.stdin.write(page.screenshot(type="jpeg", quality=90))
            if i in (int(2.5 * FPS), int(7.5 * FPS), int(12.5 * FPS)):
                page.screenshot(path=str(ROOT / "logs" / f"anim-{i // FPS:02d}s.jpg"), type="jpeg", quality=80)
        b.close()
    proc.stdin.close()
    proc.wait()

    track, credit = music.pick({"id": "anim", "topic": "su-la", "music": "Danse Macabre"}, print)
    final = demo / "anim-demo.mp4"
    if track:
        mv.run_ffmpeg(["-i", str(silent), "-stream_loop", "-1", "-i", str(track), "-filter_complex",
                       f"[1:a]loudnorm=I=-16:TP=-2,afade=t=in:d=1,afade=t=out:st={TOTAL - 2}:d=2[a]",
                       "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                       "-t", str(TOTAL), "-movflags", "+faststart", str(final)])
    else:
        silent.rename(final)
    (demo / "anim-demo.txt").write_text(f"🎵 Nhạc: {credit}\n" if credit else "", encoding="utf-8")
    print("✅ Xong", final)


if __name__ == "__main__":
    main()
