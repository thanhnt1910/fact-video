"""
BIẾN ẢNH 2D CỦA MỘT TẬP THÀNH CLIP CHUYỂN ĐỘNG, MIỄN PHÍ trên GPU Kaggle (Wan 2.2 TI2V-5B, Apache-2.0).

  python kaggle_animate_2d.py TQ2 003,041,050

- Ảnh nguồn: assets/anh_2d/<MÃ>/<số>.jpg. Mô tả chuyển động: ke-hoach/nhan-vat/<MÃ>_dong.json (nhóm A + B).
- Mỗi clip 480p (832x480), 81 khung / 24 fps, khoảng 3,4 giây; trên T4 mất khoảng 11 phút/clip.
- Kết quả: assets/clips_2d/<MÃ>/<số>.mp4 (đúng chỗ pipeline đọc `clip_file`) và logs/kaggle_video/<MÃ>_ket_qua.txt.
- Mỗi lần chạy tối đa 12 clip (khoảng 2,5 giờ) để không vượt giới hạn của GitHub Actions; làm phần còn lại ở lần chạy sau.
Dùng lại mã kernel của kaggle_animate.py. Cần KAGGLE_KEY (GitHub Secrets), HF_TOKEN nếu có.
"""
import base64
import io
import json
import os
import shutil
import sys
import time
from pathlib import Path

import kaggle_animate as ka
import kaggle_draw

ROOT = Path(__file__).resolve().parent
MAX_CLIP = 12


def main():
    from PIL import Image
    ma = sys.argv[1]
    keys = [k.strip() for k in (sys.argv[2] if len(sys.argv) > 2 else "").split(",") if k.strip()]
    mo = json.loads((ROOT / "ke-hoach" / "nhan-vat" / f"{ma}_dong.json").read_text(encoding="utf-8"))
    motion = {**mo.get("nhom_A", {}), **mo.get("nhom_B", {})}
    out_clip = ROOT / "assets" / "clips_2d" / ma
    out_log = ROOT / "logs" / "kaggle_video"
    out_clip.mkdir(parents=True, exist_ok=True)
    out_log.mkdir(parents=True, exist_ok=True)
    if len(keys) > MAX_CLIP:
        print(f"Chỉ làm {MAX_CLIP} clip đầu; còn lại: {','.join(keys[MAX_CLIP:])} (chạy lại sau)")
        keys = keys[:MAX_CLIP]
    jobs = []
    for k in keys:
        src = ROOT / "assets" / "anh_2d" / ma / f"{k}.jpg"
        if k not in motion or not src.exists():
            print(f"Bỏ qua {k}: thiếu ảnh hoặc chưa có mô tả chuyển động")
            continue
        buf = io.BytesIO()
        Image.open(src).convert("RGB").resize((832, 480), Image.LANCZOS).save(buf, "JPEG", quality=90)
        jobs.append({"key": f"{ma}_{k}", "prompt": f"{motion[k]} {ka.STYLE}", "neg": ka.NEG,
                     "img": base64.b64encode(buf.getvalue()).decode(), "w": 832, "h": 480, "frames": 81, "steps": 25})
    if not jobs:
        raise SystemExit("Không có clip nào để làm")

    user, env = kaggle_draw._env()
    work = ROOT / "output" / "_kaggle_video"
    shutil.rmtree(work, ignore_errors=True)
    (work / "k").mkdir(parents=True)
    code = ka.KERNEL.replace("__JOBS__", repr(json.dumps(jobs))).replace(
        "__HFTOK__", repr(os.environ.get("HF_TOKEN", "").strip()))
    (work / "k" / "run.py").write_text(code, encoding="utf-8")
    meta = {"id": f"{user}/{ka.SLUG}", "title": ka.SLUG, "code_file": "run.py", "language": "python",
            "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": True,
            "enable_tpu": False, "dataset_sources": [], "competition_sources": [], "kernel_sources": [],
            "model_sources": []}
    (work / "k" / "kernel-metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    print(f"Gửi {len(jobs)} ảnh sang Kaggle (Wan 2.2 TI2V-5B)", flush=True)
    kaggle_draw._kaggle(["kernels", "push", "-p", str(work / "k")], env)
    t0, last = time.time(), None
    while time.time() - t0 < 175 * 60:
        time.sleep(45)
        st = kaggle_draw._kaggle(["kernels", "status", f"{user}/{ka.SLUG}"], env, check=False).lower()
        short = (st.strip().splitlines() or [""])[-1].split("status")[-1].strip(' "')
        if short != last:
            print(f"  {(time.time() - t0) / 60:5.1f} phút: {short}", flush=True)
            last = short
        if any(w in st for w in ("complete", "error", "cancel")):
            break
    (work / "out").mkdir(exist_ok=True)
    kaggle_draw._kaggle(["kernels", "output", f"{user}/{ka.SLUG}", "-p", str(work / "out"), "-o"], env, check=False)
    lines = [f"Kaggle: {last} sau {(time.time() - t0) / 60:.0f} phút"]
    for lg in (work / "out").glob("*.log"):
        shutil.copy(lg, out_log / f"{ma}_kaggle_log.txt")
    rj = next(iter((work / "out").rglob("ket_qua.json")), None)
    if rj:
        lines.append(rj.read_text(encoding="utf-8"))
    for j in jobs:
        k = j["key"].split("_", 1)[1]
        f = next(iter((work / "out").rglob(f"{j['key']}.mp4")), None)
        if f:
            shutil.copy(f, out_clip / f"{k}.mp4")
            lines.append(f"{k}.mp4: có")
        else:
            lines.append(f"{k}.mp4: KHÔNG có (xem {ma}_kaggle_log.txt)")
    (out_log / f"{ma}_ket_qua.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        (ROOT / "logs" / "kaggle_video").mkdir(parents=True, exist_ok=True)
        (ROOT / "logs" / "kaggle_video" / "loi.txt").write_text(traceback.format_exc(), encoding="utf-8")
        traceback.print_exc()
        sys.exit(1)
