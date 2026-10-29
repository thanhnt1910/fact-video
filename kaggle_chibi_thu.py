"""Thử nhiều kiểu chibi: FLUX.1 schnell (Q8) + LoRA chibi công khai trên Hugging Face, vẽ trên GPU Kaggle miễn phí.
Cùng ba cảnh, cùng hạt giống, mỗi kiểu một hàng để so sánh. Ra: logs/chibi/<kiểu>_<cảnh>.jpg và logs/chibi/tong_hop.jpg.

  python kaggle_chibi_thu.py                -> gửi lên Kaggle, đợi, tải kết quả
  python kaggle_chibi_thu.py chi_tai_lai=1  -> chỉ tải lại kết quả lần chạy trước

Danh sách kiểu nằm ở STYLES (repo LoRA, tên file, câu mở đầu, độ mạnh). Không biết tên file thì để None, mã tự tìm file .safetensors trong repo.
Kernel cũng in ra các LoRA chibi khác tìm được trên Hugging Face để chọn tiếp vòng sau."""
import json
import os
import shutil
import sys
import time
from pathlib import Path

import kaggle_draw as kd

ROOT = Path(__file__).resolve().parent
SLUG = "ngs-chibi-thu"

STYLES = [
    {"key": "goc", "ten": "Không LoRA (chỉ viết trong câu lệnh)", "repo": None, "file": None, "scale": 0.0,
     "mo_dau": "chibi style illustration, super deformed, big head, small body, cute, flat colors, thick outline"},
    {"key": "muapi", "ten": "Muapi chibi-characters-flux-dev", "repo": "Muapi/chibi-characters-flux-dev", "file": None, "scale": 1.0,
     "mo_dau": "A vibrant chibi-style illustration"},
    {"key": "loli", "ten": "LoliOverflow chibi", "repo": "LoliOverflow/chibi", "file": "chibi.safetensors", "scale": 1.0,
     "mo_dau": "chibi, super deformed, cute"},
]
SCENES = [
    {"key": "vua", "prompt": "a young king in a golden dragon robe and a crown sitting on a throne in a red palace hall, "
                             "ancient Vietnam 11th century, simple background"},
    {"key": "phuc", "prompt": "three princes in armor with spears hiding behind a stone wall at night in front of a palace gate, "
                              "ancient Vietnam, lanterns, moon"},
    {"key": "tre", "prompt": "a little boy in a brown robe waving beside a stone pagoda by a river in an ancient Vietnamese village at dawn"},
]
SIZE = (1152, 768)

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
STYLES = json.loads(__STYLES__); SCENES = json.loads(__SCENES__); W, H = __SIZE__
SEED = 7
OUT = "/kaggle/working/out"; os.makedirs(OUT, exist_ok=True)
log("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "KHÔNG CÓ GPU")
try:   # gợi ý các LoRA chibi khác để chọn vòng sau
    ms = list(HfApi().list_models(search="chibi", filter="lora", sort="downloads", direction=-1, limit=40))
    for m in ms: log("ỨNG VIÊN", m.id, "| tải:", getattr(m, "downloads", "?"), "| thẻ:", [t for t in (m.tags or []) if "flux" in t.lower()][:3])
except Exception as e:
    log("không liệt kê được ứng viên", repr(e)[:200])
dt = torch.float16
base = snapshot_download("black-forest-labs/FLUX.1-schnell", allow_patterns=[
    "model_index.json", "scheduler/*", "text_encoder/*", "text_encoder_2/*", "tokenizer/*", "tokenizer_2/*",
    "vae/*", "transformer/config.json"])
te = FluxPipeline.from_pretrained(base, transformer=None, vae=None, torch_dtype=torch.bfloat16)
embeds = {}
for s in STYLES:
    for sc in SCENES:
        p = f'{s["mo_dau"]}, {sc["prompt"]}'
        with torch.no_grad():
            pe, ppe, _ = te.encode_prompt(prompt=p, prompt_2=p, device="cpu", max_sequence_length=256)
        embeds[(s["key"], sc["key"])] = (pe.to(dt), ppe.to(dt))
log("mã hóa xong câu mô tả", len(embeds))
del te; gc.collect()
ckpt = "https://huggingface.co/city96/FLUX.1-schnell-gguf/blob/main/flux1-schnell-Q8_0.gguf"
transformer = FluxTransformer2DModel.from_single_file(ckpt, quantization_config=GGUFQuantizationConfig(compute_dtype=dt),
                                                      torch_dtype=dt, config=base, subfolder="transformer")
pipe = FluxPipeline.from_pretrained(base, transformer=transformer, text_encoder=None, text_encoder_2=None,
                                    tokenizer=None, tokenizer_2=None, torch_dtype=dt)
pipe.to("cuda")
log("tải xong FLUX.1 schnell Q8")
lats = {}; trangthai = {}
for s in STYLES:
    loaded = False
    if s["repo"]:
        try:
            fn = s["file"]
            if not fn:
                fs = [f for f in HfApi().list_repo_files(s["repo"]) if f.endswith(".safetensors")]
                log("file trong", s["repo"], fs); fn = fs[0]
            path = hf_hub_download(s["repo"], fn)
            pipe.load_lora_weights(path, adapter_name="chibi"); pipe.set_adapters(["chibi"], adapter_weights=[s["scale"]])
            loaded = True; log("nạp LoRA", s["key"], fn)
        except Exception as e:
            log("LỖI nạp LoRA", s["key"], repr(e)[:400]); traceback.print_exc(); trangthai[s["key"]] = "lỗi nạp: " + repr(e)[:200]; continue
    for sc in SCENES:
        try:
            t1 = time.time(); pe, ppe = embeds[(s["key"], sc["key"])]
            lat = pipe(prompt_embeds=pe.to("cuda"), pooled_prompt_embeds=ppe.to("cuda"), width=W, height=H,
                       num_inference_steps=4, guidance_scale=0.0, output_type="latent",
                       generator=torch.Generator("cuda").manual_seed(SEED)).images
            lats[(s["key"], sc["key"])] = lat.cpu(); log("vẽ xong", s["key"], sc["key"], f"{time.time()-t1:.0f}s")
        except Exception as e:
            log("LỖI vẽ", s["key"], sc["key"], repr(e)[:300]); traceback.print_exc()
    if loaded:
        try: pipe.unload_lora_weights()
        except Exception as e: log("không gỡ được LoRA", repr(e)[:200])
vsf, vae, proc = pipe.vae_scale_factor, pipe.vae, pipe.image_processor
pipe.transformer = None; del pipe, transformer; gc.collect(); torch.cuda.empty_cache()
vae.to("cuda", torch.float32); vae.enable_tiling()
from diffusers import FluxPipeline as _FP
done = []
for (sk, ck), lat in lats.items():
    try:
        with torch.no_grad():
            l = _FP._unpack_latents(lat.to("cuda"), H, W, vsf)
            l = l.float() / vae.config.scaling_factor + vae.config.shift_factor
            im = vae.decode(l, return_dict=False)[0]
        img = proc.postprocess(im, output_type="pil")[0]
        if float(np.asarray(img).mean()) < 3: log("ẢNH ĐEN", sk, ck); continue
        img.save(f"{OUT}/{sk}_{ck}.png"); done.append(f"{sk}_{ck}")
    except Exception as e:
        log("LỖI giải mã", sk, ck, repr(e)[:300])
json.dump({"done": done, "trangthai": trangthai}, open(f"{OUT}/done.json", "w"), ensure_ascii=False)
log("XONG", len(done), "/", len(STYLES) * len(SCENES))
'''


def main():
    user, env = kd._env()
    work = ROOT / "output" / "_chibi"
    if "chi_tai_lai=1" not in sys.argv:
        shutil.rmtree(work, ignore_errors=True)
        (work / "k").mkdir(parents=True)
        code = (KERNEL.replace("__STYLES__", repr(json.dumps(STYLES, ensure_ascii=False)))
                .replace("__SCENES__", repr(json.dumps(SCENES, ensure_ascii=False)))
                .replace("__SIZE__", repr(SIZE))
                .replace("__HFTOK__", repr(os.environ.get("HF_TOKEN", "").strip())))
        (work / "k" / "chibi.py").write_text(code, encoding="utf-8")
        meta = {"id": f"{user}/{SLUG}", "title": SLUG, "code_file": "chibi.py", "language": "python",
                "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": True,
                "enable_tpu": False, "dataset_sources": [], "competition_sources": [], "kernel_sources": [], "model_sources": []}
        (work / "k" / "kernel-metadata.json").write_text(json.dumps(meta), encoding="utf-8")
        print("Gửi sang Kaggle", flush=True)
        kd._kaggle(["kernels", "push", "-p", str(work / "k")], env)
        t0 = time.time(); last = None
        while time.time() - t0 < 100 * 60:
            time.sleep(30)
            st = kd._kaggle(["kernels", "status", f"{user}/{SLUG}"], env, check=False).lower()
            short = (st.strip().splitlines()[-1] if st.strip() else "").split("status")[-1].strip(' "')
            if short != last:
                print(f"{(time.time() - t0) / 60:4.1f} phút: {short}", flush=True); last = short
            if any(w in st for w in ("complete", "error", "cancel")):
                break
    (work / "out").mkdir(parents=True, exist_ok=True)
    kd._kaggle(["kernels", "output", f"{user}/{SLUG}", "-p", str(work / "out"), "-o"], env, check=False)
    dst = ROOT / "logs" / "chibi"
    dst.mkdir(parents=True, exist_ok=True)
    from PIL import Image, ImageDraw
    for lg in (work / "out").glob("*.log"):
        shutil.copy(lg, dst / "kaggle_chibi.log")
    got = {}
    for s in STYLES:
        for sc in SCENES:
            f = next(iter((work / "out").rglob(f"{s['key']}_{sc['key']}.png")), None)
            if f and f.stat().st_size > 10000:
                Image.open(f).convert("RGB").save(dst / f"{s['key']}_{sc['key']}.jpg", quality=90); got[(s['key'], sc['key'])] = dst / f"{s['key']}_{sc['key']}.jpg"
    print(f"Nhận {len(got)}/{len(STYLES) * len(SCENES)} ảnh")
    if got:
        tw, th = 576, 384
        sheet = Image.new("RGB", (tw * len(SCENES), (th + 28) * len(STYLES)), (20, 20, 20))
        d = ImageDraw.Draw(sheet)
        for r, s in enumerate(STYLES):
            d.text((8, r * (th + 28) + 8), s["ten"], fill=(255, 220, 120))
            for c, sc in enumerate(SCENES):
                p = got.get((s["key"], sc["key"]))
                if p:
                    sheet.paste(Image.open(p).resize((tw, th)), (c * tw, r * (th + 28) + 28))
        sheet.save(dst / "tong_hop.jpg", quality=88)


if __name__ == "__main__":
    main()
