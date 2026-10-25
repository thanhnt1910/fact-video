"""
THỬ MÔ HÌNH ẢNH -> VIDEO MỞ KHÁC (LTX-Video) trên GPU Kaggle, để so với Wan 2.2.

  python kaggle_i2v_thu.py LH5Q 020,029,024

- Ảnh nguồn: assets/anh_2d/<MÃ>/<số>.jpg. Mô tả chuyển động: ke-hoach/nhan-vat/<MÃ>_dong.json (khóa = số ảnh); không có thì dùng câu chung.
- Clip 704x480, 97 khung / 24 fps (khoảng 4 giây). Kết quả: logs/kaggle_i2v/<MÃ>_<số>.mp4 và ket_qua.txt.
- Prompt chuyển động KHÔNG chứa tên riêng người thật.
"""
import base64
import io
import json
import os
import shutil
import sys
import time
from pathlib import Path

import kaggle_draw

ROOT = Path(__file__).resolve().parent
SLUG = "ngs-ltx-i2v"
OUT = ROOT / "logs" / "kaggle_i2v"
STYLE = "2D cartoon illustration, same art style and colours as the first frame, smooth natural motion, consistent characters, no morphing, no text"
NEG = "text, subtitles, watermark, logo, blurry, low quality, deformed hands, extra fingers, extra limbs, morphing face, distorted, flicker, static image, jpeg artifacts"

KERNEL = r'''
import json, os, sys, time, subprocess, traceback, gc, base64, io
t0 = time.time()
def log(*a):
    print(f"[{time.time()-t0:6.0f}s]", *a, flush=True)
os.environ["HF_HOME"] = "/tmp/hf"
if __HFTOK__:
    os.environ["HF_TOKEN"] = __HFTOK__
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"])
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "git+https://github.com/huggingface/diffusers.git",
                "transformers", "accelerate", "ftfy", "imageio", "imageio-ffmpeg", "sentencepiece", "protobuf"], check=True)
log("cài xong thư viện")
import torch, numpy as np
from PIL import Image
from diffusers import LTXImageToVideoPipeline
from diffusers.utils import export_to_video
JOBS = json.loads(__JOBS__)
OUT = "/kaggle/working/out"
os.makedirs(OUT, exist_ok=True)
log("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "KHÔNG CÓ GPU")
MID = "Lightricks/LTX-Video"
res = {"jobs": {}}

def load(dt):
    p = LTXImageToVideoPipeline.from_pretrained(MID, torch_dtype=dt)
    p.enable_model_cpu_offload()
    try:
        p.vae.enable_tiling()
    except Exception:
        pass
    return p

dt = torch.float16
pipe = load(dt)
log("tải xong LTX-Video", str(dt))
for j in JOBS:
    img = Image.open(io.BytesIO(base64.b64decode(j["img"]))).convert("RGB").resize((j["w"], j["h"]), Image.LANCZOS)
    for attempt in range(2):
        try:
            t1 = time.time()
            frames = pipe(image=img, prompt=j["prompt"], negative_prompt=j["neg"], width=j["w"], height=j["h"],
                          num_frames=j["frames"], num_inference_steps=j["steps"], guidance_scale=3.0,
                          generator=torch.Generator("cuda").manual_seed(0)).frames[0]
            arr = np.asarray(frames[len(frames) // 2])
            if float(arr.mean()) < (3 if arr.max() > 1.5 else 3 / 255) or not np.isfinite(arr.astype(float)).all():
                raise RuntimeError("video đen hoặc NaN (tràn số fp16)")
            export_to_video(frames, f"{OUT}/{j['key']}.mp4", fps=24)
            sec = time.time() - t1
            res["jobs"][j["key"]] = {"giay_chay": round(sec), "dtype": str(dt), "khung": j["frames"], "buoc": j["steps"]}
            log("xong", j["key"], f"{sec:.0f}s", str(dt))
            break
        except Exception as e:
            log("LỖI", j["key"], repr(e)[:400]); traceback.print_exc()
            res["jobs"][j["key"]] = {"loi": repr(e)[:400]}
            if dt == torch.float16 and attempt == 0:
                del pipe; gc.collect(); torch.cuda.empty_cache()
                dt = torch.bfloat16; pipe = load(dt); log("chuyển sang bf16")
            else:
                break
res["tong_giay"] = round(time.time() - t0)
json.dump(res, open(f"{OUT}/ket_qua.json", "w"), ensure_ascii=False, indent=1)
log("XONG", res)
'''


def main():
    ma = sys.argv[1]
    keys = [x.strip() for x in sys.argv[2].split(",") if x.strip()]
    dong_f = ROOT / "ke-hoach" / "nhan-vat" / f"{ma}_dong.json"
    dong = json.loads(dong_f.read_text(encoding="utf-8")) if dong_f.exists() else {}
    OUT.mkdir(parents=True, exist_ok=True)
    from PIL import Image
    jobs = []
    for k in keys:
        f = ROOT / "assets" / "anh_2d" / ma / f"{k}.jpg"
        im = Image.open(f).convert("RGB").resize((704, 480), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=92)
        motion = dong.get(k) or "gentle natural movement of the characters, slow camera push-in"
        jobs.append({"key": f"{ma}_{k}", "prompt": f"{motion}. {STYLE}", "neg": NEG,
                     "img": base64.b64encode(buf.getvalue()).decode(), "w": 704, "h": 480, "frames": 97, "steps": 40})
    user, env = kaggle_draw._env()
    work = ROOT / "output" / "_kaggle_i2v"
    shutil.rmtree(work, ignore_errors=True)
    (work / "k").mkdir(parents=True)
    code = KERNEL.replace("__JOBS__", repr(json.dumps(jobs))).replace("__HFTOK__", repr(os.environ.get("HF_TOKEN", "").strip()))
    (work / "k" / "run.py").write_text(code, encoding="utf-8")
    meta = {"id": f"{user}/{SLUG}", "title": SLUG, "code_file": "run.py", "language": "python", "kernel_type": "script",
            "is_private": True, "enable_gpu": True, "enable_internet": True, "enable_tpu": False,
            "dataset_sources": [], "competition_sources": [], "kernel_sources": [], "model_sources": []}
    (work / "k" / "kernel-metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    print(f"Gửi {len(jobs)} ảnh sang Kaggle (LTX-Video)", flush=True)
    kaggle_draw._kaggle(["kernels", "push", "-p", str(work / "k")], env)
    t0, last = time.time(), None
    while time.time() - t0 < 150 * 60:
        time.sleep(45)
        st = kaggle_draw._kaggle(["kernels", "status", f"{user}/{SLUG}"], env, check=False).lower()
        short = (st.strip().splitlines() or [""])[-1].split("status")[-1].strip(' "')
        if short != last:
            print(f"  {(time.time() - t0) / 60:5.1f} phút: {short}", flush=True)
            last = short
        if any(w in st for w in ("complete", "error", "cancel")):
            break
    (work / "out").mkdir(exist_ok=True)
    kaggle_draw._kaggle(["kernels", "output", f"{user}/{SLUG}", "-p", str(work / "out"), "-o"], env, check=False)
    lines = [f"Kaggle: {last} sau {(time.time() - t0) / 60:.0f} phút"]
    for lg in (work / "out").glob("*.log"):
        shutil.copy(lg, OUT / "kaggle_log.txt")
    rj = next(iter((work / "out").rglob("ket_qua.json")), None)
    if rj:
        lines.append(rj.read_text(encoding="utf-8"))
    for j in jobs:
        f = next(iter((work / "out").rglob(f"{j['key']}.mp4")), None)
        if f:
            shutil.copy(f, OUT / f"{j['key']}.mp4")
            lines.append(f"{j['key']}.mp4: có")
        else:
            lines.append(f"{j['key']}.mp4: KHÔNG có (xem kaggle_log.txt)")
    (OUT / "ket_qua.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
