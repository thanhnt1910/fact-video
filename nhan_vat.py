"""
Thử GIỮ NHÂN VẬT GIỐNG NHAU giữa các tranh 2D (miễn phí, GPU Kaggle, FLUX.2 klein 4B).

  python nhan_vat.py ST3

Bước 1: vẽ bảng nhân vật (toàn thân, nền trắng) từ đoạn mô tả cố định trong ke-hoach/nhan-vat/<mã>.json
Bước 2: vẽ mỗi cảnh thử 2 lần: (a) có đưa ảnh nhân vật làm tham chiếu, (b) chỉ bằng chữ, để so sánh
Kết quả: logs/nhan_vat/<mã>/*.jpg và lưới ảnh logs/nhan_vat/<mã>/so_sanh.jpg
"""
import json
import os
import shutil
import sys
from pathlib import Path

import kaggle_draw as kd

ROOT = Path(__file__).resolve().parent
SLUG = "ngs-flux-ref"

KERNEL = r'''
import json, os, sys, time, subprocess, traceback, gc
t0 = time.time()
def log(*a):
    print(f"[{time.time()-t0:6.0f}s]", *a, flush=True)
os.environ["HF_HOME"] = "/tmp/hf"
if __HFTOK__:
    os.environ["HF_TOKEN"] = __HFTOK__
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"])
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "diffusers", "transformers", "accelerate",
                "sentencepiece", "protobuf"], check=True)
try:
    from diffusers import Flux2KleinPipeline
except Exception:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "git+https://github.com/huggingface/diffusers.git"], check=True)
    from diffusers import Flux2KleinPipeline
import torch, numpy as np
from PIL import Image
J = json.loads(__JOBS__)
OUT = "/kaggle/working/out"
os.makedirs(OUT, exist_ok=True)
log("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "KHÔNG CÓ GPU")
def load(dt):
    p = Flux2KleinPipeline.from_pretrained("black-forest-labs/FLUX.2-klein-4B", torch_dtype=dt)
    p.enable_model_cpu_offload()
    return p
dt = torch.float16
pipe = load(dt)
log("tải xong FLUX.2 klein 4B")
def draw(prompt, w, h, seed, refs=None):
    global pipe, dt
    if refs:   # thu nhỏ ảnh tham chiếu cho đỡ tốn bộ nhớ card đồ họa
        refs = [r.resize((320, int(320 * r.height / r.width))) for r in refs]
    kw = dict(prompt=prompt, width=w, height=h, guidance_scale=1.0, num_inference_steps=4,
              generator=torch.Generator("cuda").manual_seed(seed))
    if refs:
        kw["image"] = refs
    img = pipe(**kw).images[0]
    if float(np.asarray(img).mean()) < 3 and dt == torch.float16:   # ảnh đen: chuyển sang bf16
        del pipe; gc.collect(); torch.cuda.empty_cache()
        dt = torch.bfloat16; pipe = load(dt); log("chuyển sang bf16")
        kw["generator"] = torch.Generator("cuda").manual_seed(seed)
        img = pipe(**kw).images[0]
    return img
sheets = {}
for k, prompt in J["sheets"].items():
    try:
        t1 = time.time()
        img = draw(prompt, 768, 1024, 7)
        img.save(f"{OUT}/sheet_{k}.png"); sheets[k] = img
        log("bảng nhân vật", k, f"{time.time()-t1:.0f}s")
    except Exception as e:
        log("LỖI bảng", k, repr(e)[:300]); traceback.print_exc(); gc.collect(); torch.cuda.empty_cache()
for s in J["scenes"]:
    for mode in ("ref", "text"):
        try:
            t1 = time.time()
            refs = [sheets[c] for c in s["chars"] if c in sheets] if mode == "ref" else None
            if mode == "ref" and not refs:
                continue
            img = draw(s["prompt_" + mode], 1152, 640, 11, refs)
            img.save(f"{OUT}/{s['key']}_{mode}.png")
            log("cảnh", s["key"], mode, f"{time.time()-t1:.0f}s")
        except Exception as e:
            log("LỖI cảnh", s["key"], mode, repr(e)[:400]); traceback.print_exc(); gc.collect(); torch.cuda.empty_cache()
json.dump({"done": True}, open(f"{OUT}/done.json", "w"))
log("XONG")
'''


def main():
    ma = sys.argv[1]
    cfg = json.loads((ROOT / "ke-hoach" / "nhan-vat" / f"{ma}.json").read_text(encoding="utf-8"))
    style = cfg["phong_cach"]
    sheets = {k: f"Character reference sheet, one single character, full body from head to feet, standing facing the viewer, "
                 f"neutral pose, plain pure white background, {v}, {style}" for k, v in cfg["nhan_vat"].items()}
    scenes = []
    for s in cfg["canh_thu"]:
        desc = "; ".join(cfg["nhan_vat"][c] for c in s["nhan_vat"])
        scenes.append({
            "key": s["key"], "chars": s["nhan_vat"],
            "prompt_ref": f"{s['mo_ta']}. Keep each character exactly as in the reference images (same face, hair, clothes). {style}",
            "prompt_text": f"{s['mo_ta']}. Characters: {desc}. {style}"})
    user, env = kd._env()
    work = ROOT / "output" / "_kaggle_ref"
    shutil.rmtree(work, ignore_errors=True)
    (work / "k").mkdir(parents=True)
    payload = json.dumps({"sheets": sheets, "scenes": scenes}, ensure_ascii=False)
    (work / "k" / "draw.py").write_text(KERNEL.replace("__JOBS__", repr(payload)).replace(
        "__HFTOK__", repr(os.environ.get("HF_TOKEN", "").strip())), encoding="utf-8")
    meta = {"id": f"{user}/{SLUG}", "title": SLUG, "code_file": "draw.py", "language": "python", "kernel_type": "script",
            "is_private": True, "enable_gpu": True, "enable_internet": True, "enable_tpu": False,
            "dataset_sources": [], "competition_sources": [], "kernel_sources": [], "model_sources": []}
    (work / "k" / "kernel-metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    print("Gửi sang Kaggle…")
    kd._kaggle(["kernels", "push", "-p", str(work / "k")], env)
    import time
    t0, last = time.time(), None
    while time.time() - t0 < 100 * 60:
        time.sleep(30)
        st = kd._kaggle(["kernels", "status", f"{user}/{SLUG}"], env, check=False).lower()
        short = st.strip().splitlines()[-1].split("status")[-1].strip(' "') if st.strip() else ""
        if short != last:
            print(f"{(time.time() - t0) / 60:4.1f} phút: {short}", flush=True)
            last = short
        if any(w in st for w in ("complete", "error", "cancel")):
            break
    (work / "out").mkdir(exist_ok=True)
    kd._kaggle(["kernels", "output", f"{user}/{SLUG}", "-p", str(work / "out"), "-o"], env, check=False)
    dest = ROOT / "logs" / "nhan_vat" / ma
    dest.mkdir(parents=True, exist_ok=True)
    for f in (work / "out").glob("*.log"):
        shutil.copy(f, dest / "kaggle.txt")
    from PIL import Image
    got = []
    for f in sorted((work / "out").rglob("*.png")):
        Image.open(f).convert("RGB").save(dest / (f.stem + ".jpg"), quality=90)
        got.append(f.stem)
    print("Nhận về:", got)
    # lưới so sánh: hàng trên bảng nhân vật, hàng dưới mỗi cảnh (có tham chiếu | chỉ chữ)
    try:
        sh = [dest / f"sheet_{k}.jpg" for k in cfg["nhan_vat"] if (dest / f"sheet_{k}.jpg").exists()]
        if sh:
            W = Image.new("RGB", (len(sh) * 240, 320), "white")
            for i, p in enumerate(sh):
                W.paste(Image.open(p).resize((240, 320)), (i * 240, 0))
            W.save(dest / "bang_nhan_vat.jpg", quality=88)
    except Exception as e:
        print("lưới lỗi:", e)


if __name__ == "__main__":
    main()
