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
import gc
log("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "KHÔNG CÓ GPU")
dt = torch.float16
base = snapshot_download("black-forest-labs/FLUX.1-schnell", allow_patterns=[
    "model_index.json", "scheduler/*", "text_encoder/*", "text_encoder_2/*", "tokenizer/*", "tokenizer_2/*",
    "vae/*", "transformer/config.json"])
log("tải xong bộ mã hóa chữ + VAE")
# 1) mã hóa câu mô tả bằng CPU (bf16, tránh lỗi tràn số của T5 khi chạy fp16), xong thì bỏ khỏi bộ nhớ
te = FluxPipeline.from_pretrained(base, transformer=None, vae=None, torch_dtype=torch.bfloat16)
embeds = {}
for j in JOBS:
    with torch.no_grad():
        pe, ppe, _ = te.encode_prompt(prompt=j["prompt"], prompt_2=j["prompt"], device="cpu", max_sequence_length=256)
    embeds[j["key"]] = (pe.to(dt), ppe.to(dt))
log(f"mã hóa xong {len(JOBS)} câu mô tả")
del te; gc.collect()
# 2) FLUX.1 schnell bản nén Q8 (vừa card 16 GB)
ckpt = "https://huggingface.co/city96/FLUX.1-schnell-gguf/blob/main/flux1-schnell-Q8_0.gguf"
transformer = FluxTransformer2DModel.from_single_file(
    ckpt, quantization_config=GGUFQuantizationConfig(compute_dtype=dt), torch_dtype=dt,
    config=base, subfolder="transformer")
log("tải xong FLUX (Q8)")
pipe = FluxPipeline.from_pretrained(base, transformer=transformer, text_encoder=None, text_encoder_2=None,
                                    tokenizer=None, tokenizer_2=None, torch_dtype=dt)
pipe.to("cuda")
# 3) vẽ hết (giữ bản nháp ẩn trên CPU), rồi mới bỏ mô hình vẽ khỏi card để có chỗ đổi ra ảnh
lats = {}
for j in JOBS:
    try:
        t1 = time.time()
        pe, ppe = embeds[j["key"]]
        lat = pipe(prompt_embeds=pe.to("cuda"), pooled_prompt_embeds=ppe.to("cuda"),
                   width=j["w"], height=j["h"], num_inference_steps=4, guidance_scale=0.0, output_type="latent",
                   generator=torch.Generator("cuda").manual_seed(j.get("seed", 0))).images
        lats[j["key"]] = lat.cpu()
        log("vẽ xong", j["key"], f"{time.time()-t1:.0f}s")
    except Exception as e:
        log("LỖI", j["key"], repr(e)[:300]); traceback.print_exc()
vsf = pipe.vae_scale_factor
vae, proc = pipe.vae, pipe.image_processor
pipe.transformer = None
del pipe, transformer; gc.collect(); torch.cuda.empty_cache()
vae.to("cuda", torch.float32)
vae.enable_tiling()
import numpy as np
from diffusers import FluxPipeline as _FP
done = []
for j in JOBS:
    if j["key"] not in lats:
        continue
    try:
        with torch.no_grad():
            lat = _FP._unpack_latents(lats[j["key"]].to("cuda"), j["h"], j["w"], vsf)
            lat = lat.float() / vae.config.scaling_factor + vae.config.shift_factor
            im = vae.decode(lat, return_dict=False)[0]
        img = proc.postprocess(im, output_type="pil")[0]
        if float(np.asarray(img).mean()) < 3:
            log("ẢNH ĐEN (lỗi số học)", j["key"]); continue
        img.save(f"{OUT}/{j['key']}.png")
        done.append(j["key"])
    except Exception as e:
        log("LỖI giải mã", j["key"], repr(e)[:300]); traceback.print_exc()
log("giải mã xong", len(done))
json.dump({"done": done}, open(f"{OUT}/done.json", "w"))
log("XONG", len(done), "/", len(JOBS))
'''

KERNEL_KLEIN = r'''
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
log("cài xong thư viện")
import torch, numpy as np
JOBS = json.loads(__JOBS__)
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
done = []
for j in JOBS:
    for attempt in range(2):
        try:
            t1 = time.time()
            kw = {}
            if j.get("img"):   # chế độ SỬA ẢNH: ảnh gốc + câu lệnh sửa
                import base64, io
                from PIL import Image as _I
                kw["image"] = _I.open(io.BytesIO(base64.b64decode(j["img"]))).convert("RGB")
            img = pipe(prompt=j["prompt"], width=j["w"], height=j["h"], guidance_scale=1.0, num_inference_steps=4,
                       generator=torch.Generator("cuda").manual_seed(j.get("seed", 0)), **kw).images[0]
            if float(np.asarray(img).mean()) < 3:
                raise RuntimeError("ảnh đen (tràn số fp16)")
            img.save(f"{OUT}/{j['key']}.png"); done.append(j["key"])
            log("vẽ xong", j["key"], f"{time.time()-t1:.0f}s", str(dt))
            break
        except Exception as e:
            log("LỖI", j["key"], repr(e)[:300])
            if dt == torch.float16:   # chuyển sang bf16 rồi thử lại
                del pipe; gc.collect(); torch.cuda.empty_cache()
                dt = torch.bfloat16; pipe = load(dt); log("chuyển sang bf16")
            else:
                traceback.print_exc(); break
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


def draw_batch(jobs, out_dir, log=print, timeout_min=110, model="klein"):
    """jobs: [(key, prompt, w, h)] -> {key: Path}. Ảnh lỗi thì không có trong kết quả."""
    if not jobs:
        return {}
    user, env = _env()
    work = ROOT / "output" / "_kaggle"
    shutil.rmtree(work, ignore_errors=True)
    (work / "k").mkdir(parents=True)
    # mỗi job: (key, prompt, w, h) hoặc (key, prompt, w, h, seed); không ghi seed thì lấy theo thứ tự
    import base64
    payload = json.dumps([{"key": j[0], "prompt": j[1], "w": j[2], "h": j[3], "seed": (j[4] if len(j) > 4 else i),
                           "img": (base64.b64encode(Path(j[5]).read_bytes()).decode() if len(j) > 5 and j[5] else "")}
                          for i, j in enumerate(jobs)], ensure_ascii=False)
    (work / "k" / "draw.py").write_text((KERNEL_KLEIN if model == "klein" else KERNEL_CODE).replace("__JOBS__", repr(payload)).replace("__HFTOK__", repr(os.environ.get("HF_TOKEN", "").strip())), encoding="utf-8")
    meta = {"id": f"{user}/{SLUG}", "title": SLUG, "code_file": "draw.py", "language": "python",
            "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": True,
            "enable_tpu": False, "dataset_sources": [], "competition_sources": [], "kernel_sources": [],
            "model_sources": []}
    (work / "k" / "kernel-metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    if os.environ.get("CHI_TAI_LAI") == "1":
        log("     🖥️  Chỉ tải lại kết quả của lần chạy Kaggle trước")
    else:
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
