"""
THỬ BIẾN TRANH THÀNH VIDEO MIỄN PHÍ trên GPU Kaggle (T4 16 GB), mô hình mở Wan 2.2 TI2V-5B (giấy phép Apache-2.0).

  python kaggle_animate.py scripts/ST1.json 0,3      -> tranh AI số 0 và số 3 trong video dài của ST1

- Lấy tranh trong bộ nhớ đệm assets/ai_cache (chưa có thì vẽ bằng FLUX), gửi sang Kaggle kèm mô tả chuyển động.
- Kaggle chạy Wan 2.2 (16:9, 480p, khoảng 3,4 giây/clip), xong thì tải clip về logs/kaggle_video/.
- Ghi thời gian chạy từng clip vào logs/kaggle_video/ket_qua.txt để ước tính 30 giờ GPU/tuần làm được bao nhiêu.
Cần KAGGLE_KEY (GitHub Secrets) + kaggle_username trong config.json; HF_TOKEN nếu có.
"""
import base64
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

import kaggle_draw

ROOT = Path(__file__).resolve().parent
SLUG = "ngs-wan-i2v"
OUT = ROOT / "logs" / "kaggle_video"

# mô tả chuyển động riêng cho từng tranh thử (tiếng Anh); không có thì dùng mô tả tranh
MOTION = {
    "ST1": {
        0: "The lone soldier slowly walks forward along the jungle path, away from the camera, rifle on his shoulder; "
           "palm leaves sway gently in the breeze; morning mist drifts between the trees; slow camera push-in",
        3: "The young man in a dark suit stands on the wooden pier, breathes and slowly turns his head, a slight smile; "
           "the wooden sailboats gently rock on the water; porters in the background move crates; light breeze",
    }
}
STYLE = ("2D hand-drawn illustration, same art style and colors as the first frame, smooth natural motion, "
         "correct anatomy, no morphing, no text")
NEG = ("text, subtitles, watermark, logo, blurry, low quality, deformed hands, extra fingers, extra limbs, "
       "morphing face, distorted, flicker, static image, jpeg artifacts")

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
from diffusers import AutoencoderKLWan, WanImageToVideoPipeline
from diffusers.utils import export_to_video
JOBS = json.loads(__JOBS__)
OUT = "/kaggle/working/out"
os.makedirs(OUT, exist_ok=True)
log("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "KHÔNG CÓ GPU")
MID = "Wan-AI/Wan2.2-TI2V-5B-Diffusers"
res = {"jobs": {}}

# 1) mã hóa câu mô tả bằng CPU (bf16) rồi bỏ bộ mã hóa chữ (UMT5 rất lớn, chạy fp16 dễ tràn số)
te = WanImageToVideoPipeline.from_pretrained(MID, transformer=None, vae=None, torch_dtype=torch.bfloat16)
emb = {}
for j in JOBS:
    with torch.no_grad():
        pe, ne = te.encode_prompt(prompt=j["prompt"], negative_prompt=j["neg"], do_classifier_free_guidance=True,
                                  device="cpu", max_sequence_length=226)
    emb[j["key"]] = (pe, ne)
del te; gc.collect()
log("mã hóa xong", len(JOBS), "câu mô tả")

def load(dt):
    vae = AutoencoderKLWan.from_pretrained(MID, subfolder="vae", torch_dtype=torch.float32)
    p = WanImageToVideoPipeline.from_pretrained(MID, vae=vae, text_encoder=None, tokenizer=None, torch_dtype=dt)
    p.enable_model_cpu_offload()
    try:
        p.vae.enable_tiling()
    except Exception:
        pass
    return p

dt = torch.float16
pipe = load(dt)
log("tải xong Wan 2.2 TI2V-5B", str(dt))
for j in JOBS:
    img = Image.open(io.BytesIO(base64.b64decode(j["img"]))).convert("RGB").resize((j["w"], j["h"]), Image.LANCZOS)
    for attempt in range(2):
        try:
            t1 = time.time()
            pe, ne = emb[j["key"]]
            frames = pipe(image=img, prompt_embeds=pe.to("cuda", dt), negative_prompt_embeds=ne.to("cuda", dt),
                          height=j["h"], width=j["w"], num_frames=j["frames"], guidance_scale=5.0,
                          num_inference_steps=j["steps"], generator=torch.Generator("cuda").manual_seed(0)).frames[0]
            arr = np.asarray(frames[len(frames) // 2])
            if float(arr.mean()) < (3 if arr.max() > 1.5 else 3 / 255):
                raise RuntimeError("video đen (tràn số fp16)")
            export_to_video(frames, f"{OUT}/{j['key']}.mp4", fps=24)
            sec = time.time() - t1
            res["jobs"][j["key"]] = {"giay_chay": round(sec), "dtype": str(dt), "khung": j["frames"],
                                     "kich_thuoc": f"{j['w']}x{j['h']}", "buoc": j["steps"]}
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
    import ai_images
    script = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    sid = script["id"]
    idxs = [int(x) for x in (sys.argv[2] if len(sys.argv) > 2 else "0").split(",") if x.strip()]
    beats = [b for ch in script["long"]["chapters"] for b in ch["beats"] if b.get("ai")]
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = []
    for i in idxs:
        b = beats[i]
        key = hashlib.sha1((ai_images.STYLE_ID + "|" + b["ai"]).encode()).hexdigest()[:16]
        f = ROOT / "assets" / "ai_cache" / f"{key}.jpg"
        if not f.exists():
            import long_video
            print(f"Tranh {i} chưa có trong bộ nhớ đệm, vẽ lại bằng FLUX")
            ai_images.generate(b["ai"] + ", " + long_video.WIDE_HINT, f, wide=True)
        shutil.copy(f, OUT / f"{sid}_{i}_nguon.jpg")
        motion = MOTION.get(sid, {}).get(i) or b["ai"]
        # ảnh nhỏ gọn đúng kích thước khung (mã gửi lên Kaggle có giới hạn dung lượng)
        from PIL import Image
        import io
        buf = io.BytesIO()
        im = Image.open(f).convert("RGB")
        im = im.resize((832, round(832 * im.height / im.width)), Image.LANCZOS)
        top = max(0, (im.height - 480) // 2)
        im.crop((0, top, 832, top + 480)).save(buf, "JPEG", quality=90)
        jobs.append({"key": f"{sid}_{i}", "prompt": f"{motion}. {STYLE}", "neg": NEG,
                     "img": base64.b64encode(buf.getvalue()).decode(), "w": 832, "h": 480, "frames": 81, "steps": 25})

    user, env = kaggle_draw._env()
    work = ROOT / "output" / "_kaggle_video"
    shutil.rmtree(work, ignore_errors=True)
    (work / "k").mkdir(parents=True)
    code = KERNEL.replace("__JOBS__", repr(json.dumps(jobs))).replace(
        "__HFTOK__", repr(os.environ.get("HF_TOKEN", "").strip()))
    (work / "k" / "run.py").write_text(code, encoding="utf-8")
    meta = {"id": f"{user}/{SLUG}", "title": SLUG, "code_file": "run.py", "language": "python",
            "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": True,
            "enable_tpu": False, "dataset_sources": [], "competition_sources": [], "kernel_sources": [],
            "model_sources": []}
    (work / "k" / "kernel-metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    print(f"Gửi {len(jobs)} tranh sang Kaggle (Wan 2.2 TI2V-5B)", flush=True)
    kaggle_draw._kaggle(["kernels", "push", "-p", str(work / "k")], env)
    t0, last = time.time(), None
    while time.time() - t0 < 170 * 60:
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
    lines = [f"Kaggle: {last} sau {(time.time() - t0) / 60:.0f} phút (kể cả thời gian chờ máy, cài thư viện, tải mô hình)"]
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
    try:
        main()
    except Exception:
        import traceback
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "loi.txt").write_text(traceback.format_exc(), encoding="utf-8")
        traceback.print_exc()
        sys.exit(1)
