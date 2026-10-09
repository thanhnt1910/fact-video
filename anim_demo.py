"""
Đoạn mẫu 15 giây HOẠT HÌNH CÓ KHỚP XƯƠNG (16:9):
  1) FLUX (Cloudflare, miễn phí) vẽ nhân vật ở tư thế chuẩn + phông cảnh
  2) tách nền, dọn bóng/chữ ký thừa
  3) rig/rig.py (MediaPipe + AnimatedDrawings) cho nhân vật đi bộ và nhảy múa thật (tay chân gập theo khớp)
  4) ghép cảnh: phông + nhân vật + chữ + nhạc

  AD_PY=<python có animated_drawings> python anim_demo.py
Kết quả: demo/anim-demo.mp4
"""
import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

import ai_images
import make_video as mv
import music

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "ai" / "rig"
WORK = ROOT / "output" / "_anim"
FPS = 30
TOTAL = 15.0

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BG = ("a narrow medieval street in Strasbourg in 1518, half-timbered houses on both sides, cobblestone ground, "
      "a gothic cathedral spire in the distance, summer afternoon, empty street, wide establishing shot, eye level")
P = ai_images.RIG_POSE
CHARS = {
    "troffea": f"a medieval peasant woman in a red dress with a calf-length skirt and a white linen headscarf, {P}, joyful face",
    "man": f"a medieval peasant man in a brown wool tunic, baggy trousers and leather boots, {P}, wild excited face",
    "woman": f"a medieval townswoman in a blue dress with a calf-length skirt and a white apron, {P}, smiling",
    "old": f"an old medieval man with a long grey beard in a brown tunic and trousers, {P}, tired face",
}


def prep():
    OUT.mkdir(parents=True, exist_ok=True)
    print("▶️  Vẽ ảnh bằng FLUX (Cloudflare Workers AI)", flush=True)
    bg = ai_images.generate(BG, OUT / "bg.jpg")
    for cid, prompt in CHARS.items():
        raw = ai_images.generate(prompt, OUT / f"{cid}.jpg", cutout=True)
        ai_images.cutout(raw, OUT / f"{cid}.png")
    return bg


def rig():
    jobs = [{"png": str(OUT / f"{cid}.png"), "out": str(WORK / cid), "motions": {"walk": 3.0, "dance": 7.0}}
            for cid in CHARS]
    WORK.mkdir(parents=True, exist_ok=True)
    jf = WORK / "jobs.json"
    jf.write_text(json.dumps(jobs))
    py = os.environ.get("AD_PY", sys.executable)
    print("🦴 Rig nhân vật (tìm khớp + bẻ theo chuyển động)", flush=True)
    r = subprocess.run([py, str(ROOT / "rig" / "rig.py"), str(jf)], capture_output=True, text=True)
    for line in (r.stdout + r.stderr).splitlines():
        if "khung hình" in line or "Error" in line or "rror:" in line:
            print("  ", line, flush=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        raise SystemExit("rig lỗi")


def seq(cid, motion):
    d = WORK / cid / motion
    frames = sorted(d.glob("*.png"))
    return {"frames": [f.resolve().as_uri() for f in frames], "fps": FPS}, Image.open(frames[0]).size


def foot_frac(cid):
    """Tỉ lệ khoảng hở dưới chân (so với chiều cao khung) khi đứng/đi, để đặt chân chạm mặt đường."""
    import numpy as np
    lows = []
    for f in sorted((WORK / cid / "walk").glob("*.png"))[::6]:
        a = np.array(Image.open(f).getchannel("A"))
        rows = np.where(a.max(1) > 60)[0]
        if len(rows):
            lows.append((a.shape[0] - 1 - rows[-1]) / a.shape[0])
    return float(np.median(lows)) if lows else 0.0


def compose(bg):
    chars = []
    layout = [  # id, x, ground, h, depth, enter, from, speed, phase, mirror
        ("troffea", 0.50, 70, 700, 0.0, 0.3, "right", 1.0, 0.0, False),
        ("man", 0.28, 120, 680, 0.3, 5.0, "left", 0.92, 1.3, True),
        ("woman", 0.71, 120, 680, 0.3, 6.6, "right", 1.07, 2.9, False),
        ("old", 0.13, 165, 640, 0.55, 8.2, "left", 0.8, 4.1, True),
    ]
    for cid, x, ground, h, depth, enter, frm, speed, phase, mirror in layout:
        walk, size = seq(cid, "walk")
        dance, _ = seq(cid, "dance")
        gap = foot_frac(cid) * h * (1 - depth * 0.35)
        chars.append({"x": x, "ground": ground - gap, "h": h, "aspect": size[0] / size[1], "depth": depth, "enter": enter,
                      "from": frm, "walk": 2.2, "speed": speed, "phase": phase, "mirror": mirror,
                      "seqs": {"walk": walk, "dance": dance}})
    data = {"total": TOTAL, "channel": "Người Gác Sử", "bg": Path(bg).resolve().as_uri(), "chars": chars,
            "captions": [
                {"t0": 0.6, "t1": 4.6, "text": "Strasbourg · **Tháng 7 năm 1518**"},
                {"t0": 4.9, "t1": 9.4, "text": "Một người phụ nữ bắt đầu nhảy… và **không dừng lại**"},
                {"t0": 9.7, "t1": 14.6, "text": "Vài ngày sau, **hơn 30 người** nhảy theo"}]}

    from playwright.sync_api import sync_playwright
    demo = ROOT / "demo"
    demo.mkdir(exist_ok=True)
    silent = WORK / "silent.mp4"
    n = int(TOTAL * FPS)
    cmd = [mv.ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS),
           "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           str(silent)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    print("🎬 Ghép cảnh", flush=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": 1920, "height": 1080})
        page.goto((ROOT / "templates" / "rigscene.html").as_uri())
        page.evaluate("d => window.setup(d)", data)
        for i in range(n):
            page.evaluate(f"window.renderAt({i / FPS})")
            proc.stdin.write(page.screenshot(type="jpeg", quality=90))
            if i in (int(1.5 * FPS), int(7.5 * FPS), int(12.5 * FPS)):
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
        silent.replace(final)
    (demo / "anim-demo.txt").write_text(f"🎵 Nhạc: {credit}\n" if credit else "", encoding="utf-8")
    # bảng kiểm tra khớp xương
    tiles = [Image.open(WORK / cid / "walk_rig" / "joints.png").convert("RGBA") for cid in CHARS
             if (WORK / cid / "walk_rig" / "joints.png").exists()]
    if tiles:
        for t in tiles:
            t.thumbnail((360, 480))
        sheet = Image.new("RGB", (370 * len(tiles), 480), (60, 60, 60))
        for k, t in enumerate(tiles):
            sheet.paste(t, (k * 370, 0), t)
        sheet.save(ROOT / "logs" / "anim-joints.jpg", quality=85)
    print("✅ Xong", final, flush=True)


def main():
    (ROOT / "logs").mkdir(exist_ok=True)
    bg = prep()
    rig()
    compose(bg)


if __name__ == "__main__":
    main()
