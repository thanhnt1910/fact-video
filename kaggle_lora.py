"""
Huấn luyện LoRA nhân vật cho FLUX.2 klein 4B trên GPU Kaggle, rồi vẽ thử ngay trong cùng một lần chạy
(so sánh CÓ LoRA và KHÔNG có LoRA cùng cảnh, cùng hạt giống).

  python kaggle_lora.py liubei                 -> đọc ke-hoach/lora/liubei/ (ảnh + lora.json), huấn luyện, vẽ thử
  python kaggle_lora.py liubei chi_tai_lai=1   -> chỉ tải lại kết quả của lần chạy Kaggle trước

Thư mục ke-hoach/lora/<tên>/ gồm:
  *.jpg                ảnh huấn luyện (khoảng 15-25 ảnh, cùng một nhân vật)
  lora.json            {"trigger": "liubei_han", "mo_ta": {"004": "câu mô tả cảnh bằng tiếng Anh", ...},
                        "chung": "2D franco-belgian ligne claire comic illustration of ancient China",
                        "buoc": 600, "rank": 16, "do_phan_giai": 768,
                        "thu": [{"key": "t01", "prompt": "..."}]}
Kết quả: logs/lora/<tên>/ (ảnh thử có/không LoRA, pytorch_lora_weights.safetensors, nhật ký).

Script huấn luyện: examples/dreambooth/train_dreambooth_lora_flux2_klein.py của diffusers (bản chính thức).
GPU Kaggle (T4/P100) không có FP8 nên dùng NF4 của bitsandbytes (--bnb_quantization_config_path).
"""
import base64
import io
import json
import os
import shutil
import sys
import time
from pathlib import Path

import kaggle_draw as kd

ROOT = Path(__file__).resolve().parent
SLUG = "ngs-flux-lora"

KERNEL = r'''
import json, os, sys, time, subprocess, traceback, base64, glob, shutil, gc
t0 = time.time()
def log(*a):
    print(f"[{time.time()-t0:6.0f}s]", *a, flush=True)
def sh(cmd, check=True):
    log("$", cmd[:200]); r = subprocess.run(cmd, shell=True)
    if check and r.returncode != 0: raise RuntimeError(f"lệnh lỗi {r.returncode}: {cmd[:120]}")
os.environ["HF_HOME"] = "/tmp/hf"
if __HFTOK__:
    os.environ["HF_TOKEN"] = __HFTOK__
CFG = json.loads(__CFG__)
IMGS = json.loads(__IMGS__)
OUT = "/kaggle/working/out"; os.makedirs(OUT, exist_ok=True)
W = "/kaggle/working/lora_data"; os.makedirs(W, exist_ok=True)

sh(f"{sys.executable} -m pip uninstall -y -q torchao", check=False)
sh(f"{sys.executable} -m pip install -q -U git+https://github.com/huggingface/diffusers.git transformers accelerate peft bitsandbytes sentencepiece protobuf ftfy tensorboard datasets")
import torch
log("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "KHÔNG CÓ GPU", torch.cuda.get_device_capability(0) if torch.cuda.is_available() else "")

# --- dữ liệu: ảnh + metadata.jsonl (file_name, text) ---
trig = CFG["trigger"]
with open(f"{W}/metadata.jsonl", "w", encoding="utf-8") as fm:
    for name, b64 in IMGS.items():
        open(f"{W}/{name}.jpg", "wb").write(base64.b64decode(b64))
        cap = f'{trig}, {CFG["mo_ta"].get(name, "a man standing")}, {CFG["chung"]}'
        fm.write(json.dumps({"file_name": f"{name}.jpg", "text": cap}, ensure_ascii=False) + "\n")
log("ảnh huấn luyện:", len(IMGS))

# --- script huấn luyện chính thức ---
sh("rm -rf /tmp/dz && git clone -q --depth 1 --filter=blob:none --sparse https://github.com/huggingface/diffusers /tmp/dz && cd /tmp/dz && git sparse-checkout set examples/dreambooth")
json.dump({"load_in_4bit": True, "bnb_4bit_quant_type": "nf4", "bnb_4bit_use_double_quant": True}, open("/tmp/bnb.json", "w"))
MODEL = "black-forest-labs/FLUX.2-klein-4B"
LORA_DIR = "/kaggle/working/lora_out"
cmd = (f"cd /tmp/dz/examples/dreambooth && accelerate launch --num_processes 1 --mixed_precision bf16 train_dreambooth_lora_flux2_klein.py "
       f"--pretrained_model_name_or_path={MODEL} --instance_data_dir={W} --caption_column=text --output_dir={LORA_DIR} "
       f"--bnb_quantization_config_path=/tmp/bnb.json --mixed_precision=bf16 --gradient_checkpointing --cache_latents --offload "
       f"--instance_prompt='{trig}' --resolution={CFG['do_phan_giai']} --center_crop --train_batch_size=1 --guidance_scale=1 "
       f"--use_8bit_adam --gradient_accumulation_steps=4 --optimizer=adamW --learning_rate=1e-4 --lr_scheduler=constant "
       f"--lr_warmup_steps=50 --max_train_steps={CFG['buoc']} --rank={CFG['rank']} --seed=0 --report_to=tensorboard")
train_ok = True
try:
    sh(cmd)
except Exception as e:
    train_ok = False; log("HUẤN LUYỆN LỖI", repr(e)[:300]); traceback.print_exc()
log("huấn luyện xong" if train_ok else "huấn luyện KHÔNG xong", f"{(time.time()-t0)/60:.1f} phút")
wf = glob.glob(f"{LORA_DIR}/pytorch_lora_weights.safetensors")
if wf:
    shutil.copy(wf[0], f"{OUT}/pytorch_lora_weights.safetensors")

# --- vẽ thử: cùng cảnh, cùng hạt giống, có và không có LoRA ---
gc.collect(); torch.cuda.empty_cache()
if wf:
    try:
        from diffusers import Flux2KleinPipeline
        pipe = Flux2KleinPipeline.from_pretrained(MODEL, torch_dtype=torch.bfloat16)
        pipe.enable_model_cpu_offload()
        for j in CFG["thu"]:
            seed = j.get("seed", 1)
            for tag, use in (("khong", False), ("co", True)):
                if use:
                    pipe.load_lora_weights(LORA_DIR, weight_name="pytorch_lora_weights.safetensors")
                prompt = (trig + ", " + j["prompt"]) if use else j["prompt"]
                try:
                    img = pipe(prompt=prompt, width=j.get("w", 1344), height=j.get("h", 768), guidance_scale=1.0,
                               num_inference_steps=4, generator=torch.Generator("cuda").manual_seed(seed)).images[0]
                    img.save(f"{OUT}/{j['key']}_{tag}.png"); log("thử", j["key"], tag)
                except Exception as e:
                    log("LỖI vẽ thử", j["key"], tag, repr(e)[:200])
                if use:
                    pipe.unload_lora_weights()
    except Exception as e:
        log("LỖI bước vẽ thử", repr(e)[:300]); traceback.print_exc()
json.dump({"train_ok": train_ok}, open(f"{OUT}/done.json", "w"))
log("XONG")
'''


def run(name, chi_tai_lai=False, timeout_min=170, log=print):
    src = ROOT / "ke-hoach" / "lora" / name
    cfg = json.loads((src / "lora.json").read_text(encoding="utf-8"))
    cfg.setdefault("buoc", 600); cfg.setdefault("rank", 16); cfg.setdefault("do_phan_giai", 768)
    cfg.setdefault("chung", "2D franco-belgian ligne claire comic illustration of ancient China")
    cfg.setdefault("mo_ta", {}); cfg.setdefault("thu", [])
    from PIL import Image
    imgs = {}
    for f in sorted(src.glob("*.jpg")):
        buf = io.BytesIO()
        im = Image.open(f).convert("RGB"); im.thumbnail((768, 768)); im.save(buf, "JPEG", quality=82)
        imgs[f.stem] = base64.b64encode(buf.getvalue()).decode()
    if not imgs:
        raise SystemExit(f"Không có ảnh .jpg trong {src}")
    user, env = kd._env()
    work = ROOT / "output" / "_kaggle_lora"
    shutil.rmtree(work, ignore_errors=True)
    (work / "k").mkdir(parents=True)
    code = (KERNEL.replace("__CFG__", repr(json.dumps(cfg, ensure_ascii=False)))
            .replace("__IMGS__", repr(json.dumps(imgs)))
            .replace("__HFTOK__", repr(os.environ.get("HF_TOKEN", "").strip())))
    (work / "k" / "lora.py").write_text(code, encoding="utf-8")
    log(f"Mã kernel: {len(code) / 1e6:.2f} MB")
    meta = {"id": f"{user}/{SLUG}", "title": SLUG, "code_file": "lora.py", "language": "python",
            "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": True,
            "enable_tpu": False, "dataset_sources": [], "competition_sources": [], "kernel_sources": [],
            "model_sources": []}
    (work / "k" / "kernel-metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    if not chi_tai_lai:
        log(f"Gửi {len(imgs)} ảnh huấn luyện '{name}' sang Kaggle ({cfg['buoc']} bước, rank {cfg['rank']})")
        kd._kaggle(["kernels", "push", "-p", str(work / "k")], env)
    t0 = time.time(); last = None; st = ""
    while time.time() - t0 < timeout_min * 60:
        time.sleep(60)
        st = kd._kaggle(["kernels", "status", f"{user}/{SLUG}"], env, check=False).lower()
        short = (st.strip().splitlines()[-1] if st.strip() else "").split("status")[-1].strip(' "')
        if short != last:
            log(f"{(time.time() - t0) / 60:5.1f} phút: {short}"); last = short
        if any(w in st for w in ("complete", "error", "cancel")):
            break
    (work / "out").mkdir(exist_ok=True)
    kd._kaggle(["kernels", "output", f"{user}/{SLUG}", "-p", str(work / "out"), "-o"], env, check=False)
    dest = ROOT / "logs" / "lora" / name
    dest.mkdir(parents=True, exist_ok=True)
    for f in (work / "out").rglob("*"):
        if f.is_file() and f.suffix in (".png", ".safetensors", ".log", ".json"):
            if f.suffix == ".png":
                Image.open(f).convert("RGB").save(dest / (f.stem + ".jpg"), quality=92)
            else:
                shutil.copy(f, dest / f.name)
    log(f"Đã lưu kết quả ở {dest}")
    return dest


if __name__ == "__main__":
    a = sys.argv[1:]
    run(a[0], chi_tai_lai="chi_tai_lai=1" in a)
