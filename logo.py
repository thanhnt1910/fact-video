"""Gắn logo kênh vào góc video (config.json -> "logo"). Dùng: silent = logo.ap_dung(silent, work, ffmpeg, "dai"|"ngan", log)"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def ap_dung(video, work, ffmpeg, kieu, cfg, log=print):
    lg = (cfg.get("logo") or {})
    if not lg.get("bat", True) or kieu not in lg:
        return video
    p = lg[kieu]
    f = ROOT / lg.get("file", "assets/logo/nguoi-gac-su.png")
    if not f.exists():
        log(f"  (không thấy logo {f}, bỏ qua)")
        return video
    out = Path(work) / f"{Path(video).stem}_logo.mp4"
    w, m, top, op = int(p["rong"]), int(p["le"]), int(p.get("tren", p["le"])), float(p.get("do_dam", 0.9))
    x = f"W-w-{m}" if p.get("goc", "phai") == "phai" else str(m)
    graph = f"[1:v]scale={w}:{w}:flags=lanczos,format=rgba,colorchannelmixer=aa={op}[lg];[0:v][lg]overlay={x}:{top}:format=auto,format=yuv420p"
    r = subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-i", str(f), "-filter_complex", graph,
                        "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-an", str(out)], capture_output=True, text=True)
    if r.returncode:
        log(f"  (gắn logo lỗi, dùng video không logo: {r.stderr[-300:]})")
        return video
    log(f"  🏷️  Đã gắn logo kênh vào góc trên bên {'phải' if p.get('goc', 'phai') == 'phai' else 'trái'}")
    return out
