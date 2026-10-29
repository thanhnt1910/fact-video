"""Vẽ hàng loạt ảnh chibi cho một video: FLUX.1 schnell (GGUF Q8) + LoRA Muapi/chibi-characters-flux-dev trên GPU Kaggle miễn phí.

  python kaggle_chibi_ve.py lt1                      -> vẽ mọi cảnh trong ke-hoach/chibi/lt1_chibi.json
  python kaggle_chibi_ve.py lt1 chi_ve=19004,19024   -> chỉ vẽ lại các đoạn này
  python kaggle_chibi_ve.py lt1 dot=2                -> đổi hạt giống (seed = số đoạn + 1000 x (dot-1)), dùng khi vẽ lại ảnh lỗi
  python kaggle_chibi_ve.py lt1 chi_tai_lai=1        -> chỉ tải lại kết quả các lượt trước (không vẽ)

Đầu vào: ke-hoach/chibi/<mã>_chibi.json, danh sách {n, lora, seed, prompt}; n = số đoạn lời kể, độ mạnh LoRA ghi sẵn từng cảnh.
Đầu ra: assets/anh_chibi/<mã>/<n>.jpg (1344x768), log ở logs/chibi/<mã>_ve.log.
Chia lượt (mỗi lượt một kernel Kaggle, chạy lần lượt, không song song) để một lượt hỏng không mất cả bộ."""
import json
import os
import shutil
import sys
import time
from pathlib import Path

import kaggle_draw as kd

ROOT = Path(__file__).resolve().parent
SIZE = (1344, 768)
LORA_REPO = "Muapi/chibi-characters-flux-dev"
PER_RUN = 32
SLUG = "ngs-chibi-ve"

KERNEL = r'''
import json, os, sys, time, subprocess, traceback, gc
t0 = time.time()
def log(*a):
    print(f"[{time.time()-t0:6.0f}s]", *a, flush=True)
os.environ["HF_HOME"] = "/tmp/hf"
if __HFTOK__:
    os.environ["HF_TOKEN"] = __HFTOK__
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "diffusers>=0.33", "gguf", "transformers",
                "accelerate", "sentencepiece", "protobuf", "peft"], check=True)
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"])
log("cài xong thư viện")
import torch, numpy as np
from huggingface_hub import snapshot_download, hf_hub_download, HfApi
from diffusers import FluxPipeline, FluxTransformer2DModel, GGUFQuantizationConfig
ITEMS = json.loads(__ITEMS__); W, H = __SIZE__; LORA_REPO = __LORA__
OUT = "/kaggle/working/out"; os.makedirs(OUT, exist_ok=True)
log("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "KHÔNG CÓ GPU", "| số cảnh:", len(ITEMS))
dt = torch.float16
base = snapshot_download("black-forest-labs/FLUX.1-schnell", allow_patterns=[
    "model_index.json", "scheduler/*", "text_encoder/*", "text_encoder_2/*", "tokenizer/*", "tokenizer_2/*",
    "vae/*", "transformer/config.json"])
te = FluxPipeline.from_pretrained(base, transformer=None, vae=None, torch_dtype=torch.bfloat16)
embeds = {}
for it in ITEMS:
    with torch.no_grad():
        pe, ppe, _ = te.encode_prompt(prompt=it["prompt"], prompt_2=it["prompt"], device="cpu", max_sequence_length=256)
    embeds[it["n"]] = (pe.to(dt), ppe.to(dt))
log("mã hóa xong câu mô tả", len(embeds))
del te; gc.collect()
ckpt = "https://huggingface.co/city96/FLUX.1-schnell-gguf/blob/main/flux1-schnell-Q8_0.gguf"
transformer = FluxTransformer2DModel.from_single_file(ckpt, quantization_config=GGUFQuantizationConfig(compute_dtype=dt),
                                                      torch_dtype=dt, config=base, subfolder="transformer")
pipe = FluxPipeline.from_pretrained(base, transformer=transformer, text_encoder=None, text_encoder_2=None,
                                    tokenizer=None, tokenizer_2=None, torch_dtype=dt)
pipe.to("cuda")
log("tải xong FLUX.1 schnell Q8")
lora_ok = False
try:
    fs = [f for f in HfApi().list_repo_files(LORA_REPO) if f.endswith(".safetensors")]
    log("file trong", LORA_REPO, fs)
    pipe.load_lora_weights(hf_hub_download(LORA_REPO, fs[0]), adapter_name="chibi")
    lora_ok = True; log("nạp LoRA xong")
except Exception as e:
    log("LỖI nạp LoRA, vẽ không LoRA:", repr(e)[:400]); traceback.print_exc()
lats = {}; loi = []
for it in sorted(ITEMS, key=lambda x: x["lora"]):
    n = it["n"]
    try:
        if lora_ok:
            pipe.set_adapters(["chibi"], adapter_weights=[float(it["lora"])])
        t1 = time.time(); pe, ppe = embeds[n]
        lat = pipe(prompt_embeds=pe.to("cuda"), pooled_prompt_embeds=ppe.to("cuda"), width=W, height=H,
                   num_inference_steps=4, guidance_scale=0.0, output_type="latent",
                   generator=torch.Generator("cuda").manual_seed(int(it["seed"]))).images
        lats[n] = lat.cpu(); log("vẽ xong", n, "LoRA", it["lora"], f"{time.time()-t1:.0f}s")
    except Exception as e:
        loi.append(n); log("LỖI vẽ", n, repr(e)[:300]); traceback.print_exc()
vsf, vae, proc = pipe.vae_scale_factor, pipe.vae, pipe.image_processor
pipe.transformer = None; del pipe, transformer; gc.collect(); torch.cuda.empty_cache()
vae.to("cuda", torch.float32); vae.enable_tiling()
from diffusers import FluxPipeline as _FP
done = []
for n, lat in lats.items():
    try:
        with torch.no_grad():
            l = _FP._unpack_latents(lat.to("cuda"), H, W, vsf)
            l = l.float() / vae.config.scaling_factor + vae.config.shift_factor
            im = vae.decode(l, return_dict=False)[0]
        img = proc.postprocess(im, output_type="pil")[0]
        if float(np.asarray(img).mean()) < 3:
            log("ẢNH ĐEN", n); loi.append(n); continue
        img.save(f"{OUT}/{n}.png"); done.append(n)
    except Exception as e:
        loi.append(n); log("LỖI giải mã", n, repr(e)[:300])
json.dump({"done": done, "loi": loi, "lora": lora_ok}, open(f"{OUT}/done.json", "w"), ensure_ascii=False)
log("XONG", len(done), "/", len(ITEMS))
'''


def _wait(user, env, slug, timeout_min):
    t0 = time.time(); last = None
    while time.time() - t0 < timeout_min * 60:
        time.sleep(30)
        st = kd._kaggle(["kernels", "status", f"{user}/{slug}"], env, check=False).lower()
        short = (st.strip().splitlines()[-1] if st.strip() else "").split("status")[-1].strip(' "')
        if short != last:
            print(f"{(time.time() - t0) / 60:4.1f} phút: {short}", flush=True); last = short
        if any(w in st for w in ("complete", "error", "cancel")):
            return short
    return "hết giờ chờ"


def main():
    args = [a for a in sys.argv[1:] if "=" not in a]
    opts = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
    ma = args[0] if args else "lt1"
    items = json.loads((ROOT / "ke-hoach" / "chibi" / f"{ma}_chibi.json").read_text(encoding="utf-8"))
    if opts.get("chi_ve"):
        want = {int(x) for x in opts["chi_ve"].replace(" ", "").split(",") if x}
        items = [i for i in items if i["n"] in want]
    dot = int(opts.get("dot", 1))
    for i in items:
        i["seed"] = i["n"] + 1000 * (dot - 1)
    dst = ROOT / "assets" / "anh_chibi" / ma
    dst.mkdir(parents=True, exist_ok=True)
    logdir = ROOT / "logs" / "chibi"
    logdir.mkdir(parents=True, exist_ok=True)
    user, env = kd._env()
    work = ROOT / "output" / "_chibi_ve"
    got, loi = [], []
    chunks = [items[k:k + PER_RUN] for k in range(0, len(items), PER_RUN)]
    for ci, chunk in enumerate(chunks, 1):
        out = work / f"out{ci}"
        if "chi_tai_lai" not in opts:
            shutil.rmtree(work / "k", ignore_errors=True)
            (work / "k").mkdir(parents=True)
            code = (KERNEL.replace("__ITEMS__", repr(json.dumps(chunk, ensure_ascii=False)))
                    .replace("__SIZE__", repr(SIZE)).replace("__LORA__", repr(LORA_REPO))
                    .replace("__HFTOK__", repr(os.environ.get("HF_TOKEN", "").strip())))
            (work / "k" / "chibi.py").write_text(code, encoding="utf-8")
            meta = {"id": f"{user}/{SLUG}", "title": SLUG, "code_file": "chibi.py", "language": "python",
                    "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": True,
                    "enable_tpu": False, "dataset_sources": [], "competition_sources": [], "kernel_sources": [], "model_sources": []}
            (work / "k" / "kernel-metadata.json").write_text(json.dumps(meta), encoding="utf-8")
            print(f"Lượt {ci}/{len(chunks)}: gửi {len(chunk)} cảnh sang Kaggle", flush=True)
            kd._kaggle(["kernels", "push", "-p", str(work / "k")], env)
            print("   kết thúc:", _wait(user, env, SLUG, 150), flush=True)
        shutil.rmtree(out, ignore_errors=True)
        out.mkdir(parents=True, exist_ok=True)
        kd._kaggle(["kernels", "output", f"{user}/{SLUG}", "-p", str(out), "-o"], env, check=False)
        for lg in out.glob("*.log"):
            shutil.copy(lg, logdir / f"{ma}_ve_luot{ci}.log")
        from PIL import Image
        for it in chunk:
            f = next(iter(out.rglob(f"{it['n']}.png")), None)
            if f and f.stat().st_size > 10000:
                Image.open(f).convert("RGB").save(dst / f"{it['n']}.jpg", quality=92)
                got.append(it["n"])
            else:
                loi.append(it["n"])
        print(f"   lượt {ci}: nhận {sum(1 for it in chunk if it['n'] in got)}/{len(chunk)} ảnh", flush=True)
    print(f"TỔNG: nhận {len(got)}/{len(items)} ảnh; thiếu: {sorted(loi)}", flush=True)
    (logdir / f"{ma}_ve.log").write_text(f"nhận {len(got)}/{len(items)}\nthiếu: {sorted(loi)}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
