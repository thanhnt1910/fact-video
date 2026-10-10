"""
Vẽ tranh FLUX.1 schnell trên máy có card đồ họa miễn phí của Kaggle (khoảng 30 giờ/tuần).

  draw_batch([(key, prompt, width, height), ...], out_dir) -> {key: đường dẫn ảnh}

Cách chạy: đẩy một "kernel" (script) lên Kaggle bằng API, Kaggle tự chạy trên GPU,
xong thì tải ảnh về. Cần biến môi trường KAGGLE_KEY (GitHub Secrets); tên đăng nhập ghi ở config.json.
"""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SLUG = "ngs-flux-draw"

KERNEL_CODE = r'''
import json, os, sys, time, subprocess, traceback
t0 = time.time()
def log(*a):
    print(f"[{time.time()-t0:6.0f}s]", *a, flush=True)
os.environ["HF_HOME"] = "/tmp/hf"
if __HFTOK__:
    os.environ["HF_TOKEN"] = __HFTOK__
import datetime
log("bắt đầu lúc", datetime.datetime.utcnow().strftime("%H:%M:%S UTC"))
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "diffusers>=0.32", "gguf", "transformers",
                "accelerate", "sentencepiece", "protobuf"], check=True)
# torchao có sẵn trên Kaggle lệch phiên bản với diffusers mới -> gỡ đi (không cần dùng)
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"])
log("cài xong thư viện")
import torch
from huggingface_hub import snapshot_download
from diffusers import FluxPipeline, FluxTransformer2DModel, GGUFQuantizationConfig
JOBS = json.loads(__JOBS__)
OUT = "/kaggle/working/out"
os.makedirs(OUT, exist_ok=True)
log("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "KHÔNG CÓ GPU")
dt = torch.float16
base = snapshot_download("black-forest-labs/FLUX.1-schnell", allow_patterns=[
    "model_index.json", "scheduler/*", "text_encoder/*", "text_encoder_2/*", "tokenizer/*", "tokenizer_2/*", "vae/*"])
log("tải xong bộ mã hóa chữ + VAE")
ckpt = "https://huggingface.co/city96/FLUX.1-schnell-gguf/blob/main/flux1-schnell-Q8_0.gguf"
transformer = FluxTransformer2DModel.from_single_file(
    ckpt, quantization_config=GGUFQuantizationConfig(compute_dtype=dt), torch_dtype=dt)
log("tải xong FLUX (Q8)")
pipe = FluxPipeline.from_pretrained(base, transformer=transformer, torch_dtype=dt)
# mã hóa chữ bằng CPU (fp32) cho chắc, rồi bỏ khỏi bộ nhớ
pipe.text_encoder.to("cpu", torch.float32); pipe.text_encoder_2.to("cpu", torch.float32)
embeds = {}
for j in JOBS:
    with torch.no_grad():
        pe, ppe, _ = pipe.encode_prompt(prompt=j["prompt"], prompt_2=j["prompt"], device="cpu", max_sequence_length=256)
    embeds[j["key"]] = (pe.to(dt), ppe.to(dt))
log(f"mã hóa xong {len(JOBS)} câu mô tả")
pipe.text_encoder = None; pipe.text_encoder_2 = None
import gc; gc.collect()
pipe.to("cuda")
done = []
for j in JOBS:
    try:
        pe, ppe = embeds[j["key"]]
        img = pipe(prompt_embeds=pe.to("cuda"), pooled_prompt_embeds=ppe.to("cuda"),
                   width=j["w"], height=j["h"], num_inference_steps=4, guidance_scale=0.0,
                   generator=torch.Generator("cuda").manual_seed(j.get("seed", 0))).images[0]
        img.save(f"{OUT}/{j['key']}.png")
        done.append(j["key"])
        log("vẽ xong", j["key"])
    except Exception as e:
        log("LỖI", j["key"], repr(e)[:300]); traceback.print_exc()
json.dump({"done": done}, open(f"{OUT}/done.json", "w"))
log("XONG", len(done), "/", len(JOBS))
'''


def _env():
    cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    user = os.environ.get("KAGGLE_USERNAME") or cfg.get("kaggle_username", "")
    key = os.environ.get("KAGGLE_KEY", "").strip()
    if not user or not key:
        raise RuntimeError("Chưa có KAGGLE_KEY / kaggle_username")
    # Kaggle CLI mới dùng KAGGLE_API_TOKEN (khóa kiểu mới); bản cũ dùng KAGGLE_USERNAME + KAGGLE_KEY
    env = dict(os.environ, KAGGLE_USERNAME=user, KAGGLE_KEY=key, KAGGLE_API_TOKEN=key)
    return user, env


def _kaggle(args, env, check=True):
    r = subprocess.run([sys.executable, "-m", "kaggle"] + args, capture_output=True, text=True, env=env)
    if check and r.returncode != 0:
        raise RuntimeError(f"kaggle {' '.join(args[:2])}: {(r.stderr or r.stdout)[-500:]}")
    return (r.stdout or "") + (r.stderr or "")


def draw_batch(jobs, out_dir, log=print, timeout_min=110):
    """jobs: [(key, prompt, w, h)] -> {key: Path}. Ảnh lỗi thì không có trong kết quả."""
    if not jobs:
        return {}
    user, env = _env()
    work = ROOT / "output" / "_kaggle"
    shutil.rmtree(work, ignore_errors=True)
    (work / "k").mkdir(parents=True)
    payload = json.dumps([{"key": k, "prompt": p, "w": w, "h": h, "seed": i} for i, (k, p, w, h) in enumerate(jobs)],
                         ensure_ascii=False)
    (work / "k" / "draw.py").write_text(KERNEL_CODE.replace("__JOBS__", repr(payload)).replace("__HFTOK__", repr(os.environ.get("HF_TOKEN", "").strip())), encoding="utf-8")
    meta = {"id": f"{user}/{SLUG}", "title": SLUG, "code_file": "draw.py", "language": "python",
            "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": True,
            "enable_tpu": False, "dataset_sources": [], "competition_sources": [], "kernel_sources": [],
            "model_sources": []}
    (work / "k" / "kernel-metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    log(f"     🖥️  Gửi {len(jobs)} tranh sang Kaggle (GPU miễn phí)")
    _kaggle(["kernels", "push", "-p", str(work / "k")], env)
    t0 = time.time()
    status = ""
    last = None
    while time.time() - t0 < timeout_min * 60:
        time.sleep(30)
        st = _kaggle(["kernels", "status", f"{user}/{SLUG}"], env, check=False).lower()
        status = st.strip().splitlines()[-1] if st.strip() else ""
        short = status.split("status")[-1].strip(' "')
        if short != last:
            log(f"     🖥️  {(time.time() - t0) / 60:4.1f} phút: {short}")
            last = short
        if any(w in st for w in ("complete", "error", "cancel")):
            break
    log(f"     🖥️  Kaggle: {status} ({(time.time() - t0) / 60:.0f} phút)")
    (work / "out").mkdir(exist_ok=True)
    _kaggle(["kernels", "output", f"{user}/{SLUG}", "-p", str(work / "out"), "-o"], env, check=False)
    # nhật ký Kaggle để kiểm tra lỗi
    logs = list((work / "out").glob("*.log"))
    if logs:
        (ROOT / "logs").mkdir(exist_ok=True)
        shutil.copy(logs[0], ROOT / "logs" / "kaggle_last.txt")
    res = {}
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for k, *_ in jobs:
        f = next(iter((work / "out").rglob(f"{k}.png")), None)
        if f and f.stat().st_size > 10000:
            dest = out_dir / f"{k}.jpg"
            from PIL import Image
            Image.open(f).convert("RGB").save(dest, quality=92)
            res[k] = dest
    log(f"     🖥️  Nhận về {len(res)}/{len(jobs)} tranh từ Kaggle")
    return res
