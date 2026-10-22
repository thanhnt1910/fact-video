"""
VIDEO NGƯỜI THẬT NHẢY, MIỄN PHÍ trên GPU Kaggle: lấy chuyển động từ một video nhảy mẫu, áp lên người trong một ảnh.
Mô hình: Wan 2.2 Animate 14B (bản Diffusers, Apache-2.0), nén 4-bit để vừa GPU T4 16 GB.

File này TÁCH RIÊNG, không sửa gì ở các phần khác của repo (chỉ dùng lại _env/_kaggle của kaggle_draw.py).
Kernel Kaggle mới: ngs-dance-animate; dataset đầu vào: ngs-dance-input (đều riêng tư, không đụng ngs-wan-i2v / ngs-flux-draw).

Hai bước, vì chạy lâu (vài giờ) nên không giữ GitHub Actions chờ:

  python kaggle_dance.py gui --ten abc --anh dance_in/abc/anh.jpg --mau dance_in/abc/mau.mp4 [--tong 30 --doan 10 --bat-dau 0]
      cắt video mẫu, đẩy dataset + kernel lên Kaggle rồi thoát ngay.

  python kaggle_dance.py lay --ten abc --mau dance_in/abc/mau.mp4 [--cho 0]
      xem Kaggle xong chưa; xong thì tải các đoạn về, ghép và gắn nhạc của video mẫu -> output/dance/abc.mp4

  Thêm --thu ở bước gui: chỉ làm 3 giây để thử trước (khuyến nghị lần đầu).

Lưu ý: kernel dùng một slug cố định nên mỗi lần chỉ chạy MỘT video; không chạy cùng lúc với các kernel Kaggle khác của repo.
Cần KAGGLE_KEY (GitHub Secrets) + kaggle_username trong config.json; HF_TOKEN nếu có.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import kaggle_draw

ROOT = Path(__file__).resolve().parent
SLUG = "ngs-dance-animate"
DATASET = "ngs-dance-input"
WORK = ROOT / "output" / "_kaggle_dance"
FPS = 30

NEG = ("blurry, low quality, distorted, deformed, extra limbs, extra fingers, morphing face, static, "
       "text, watermark, subtitles, jpeg artifacts")
PROMPT = "A person dancing energetically, smooth natural motion, correct anatomy, same outfit and face as the reference image"

KERNEL = r'''
import json, os, sys, time, subprocess, traceback, gc, glob, urllib.request
t0 = time.time()
def log(*a):
    print(f"[{time.time()-t0:6.0f}s]", *a, flush=True)
os.environ["HF_HOME"] = "/tmp/hf"
_tok = __HFTOK__
if _tok:
    os.environ["HF_TOKEN"] = _tok
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"])
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "git+https://github.com/huggingface/diffusers.git",
                "transformers", "accelerate", "bitsandbytes", "onnxruntime", "loguru", "omegaconf", "matplotlib",
                "opencv-python-headless", "imageio", "imageio-ffmpeg", "ftfy", "sentencepiece", "protobuf"], check=True)
# easy-dwpose chạy bằng ONNX (không cần mmpose); --no-deps để khỏi kéo onnxruntime-gpu bản cũ
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--no-deps", "easy-dwpose"], check=True)
log("cài xong thư viện")
import numpy as np, cv2, torch
from PIL import Image
from diffusers import AutoencoderKLWan, WanAnimatePipeline
from diffusers.quantizers import PipelineQuantizationConfig
from diffusers.utils import export_to_video

OUT = "/kaggle/working/out"
os.makedirs(OUT, exist_ok=True)
jf = glob.glob("/kaggle/input/**/job.json", recursive=True)
if not jf:
    raise SystemExit("không thấy job.json trong dữ liệu đầu vào")
IN = os.path.dirname(jf[0])
JOB = json.load(open(jf[0]))
json.dump(JOB, open(f"{OUT}/job.json", "w"))
W, H = JOB["w"], JOB["h"]
MID = "Wan-AI/Wan2.2-Animate-14B-Diffusers"
log("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "KHÔNG CÓ GPU", f"| khung {W}x{H}")

# ---------- tiền xử lý: khung xương (pose) + khuôn mặt (face) từ video nhảy mẫu ----------
os.makedirs("/tmp/dwp", exist_ok=True)
os.chdir("/tmp/dwp")                      # easy-dwpose tải mô hình ONNX vào ./checkpoints
from easy_dwpose import DWposeDetector
dw = DWposeDetector(device="cpu")
yunet = "/tmp/yunet.onnx"
if not os.path.exists(yunet):
    urllib.request.urlretrieve("https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/"
                               "face_detection_yunet_2023mar.onnx", yunet)
fd = cv2.FaceDetectorYN.create(yunet, "", (320, 320), 0.6)

def read_clip(path):
    cap = cv2.VideoCapture(path)
    fr = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
        h, w = f.shape[:2]
        ar = W / H
        if w / h > ar:                      # video rộng hơn khung: cắt hai bên
            nw = int(h * ar); x0 = (w - nw) // 2; f = f[:, x0:x0 + nw]
        else:                               # video cao hơn khung: cắt trên dưới
            nh = int(w / ar); y0 = (h - nh) // 2; f = f[y0:y0 + nh]
        fr.append(cv2.resize(f, (W * 2, H * 2), interpolation=cv2.INTER_AREA))
    cap.release()
    return fr

def face_crops(frames):
    out, box = [], None
    for f in frames:
        bgr = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
        fd.setInputSize((bgr.shape[1], bgr.shape[0]))
        _, faces = fd.detect(bgr)
        if faces is not None and len(faces):
            x, y, w, h = faces[np.argmax(faces[:, 2] * faces[:, 3]), :4]
            cx, cy, s = x + w / 2, y + h / 2, 1.6 * max(w, h)
            nb = np.array([cx, cy, s])
            box = nb if box is None else 0.6 * box + 0.4 * nb      # làm mượt để mặt không rung
        if box is None:
            box = np.array([f.shape[1] / 2, f.shape[0] * 0.2, f.shape[1] * 0.3])   # chưa thấy mặt: đoán ở nửa trên khung
        cx, cy, s = box
        x0, y0 = int(max(0, cx - s / 2)), int(max(0, cy - s / 2))
        x1, y1 = int(min(f.shape[1], cx + s / 2)), int(min(f.shape[0], cy + s / 2))
        c = f[y0:y1, x0:x1]
        if c.size == 0:
            c = f
        out.append(Image.fromarray(cv2.resize(c, (512, 512), interpolation=cv2.INTER_AREA)))
    return out

def pose_frames(frames):
    out = []
    for f in frames:
        p = dw(Image.fromarray(f), detect_resolution=512, include_face=False, include_hands=True)
        out.append(p.convert("RGB").resize((W, H), Image.LANCZOS))
    return out

# ---------- mã hóa câu mô tả bằng CPU (bf16) rồi bỏ bộ mã hóa chữ (chạy fp16 trên T4 dễ tràn số) ----------
te = WanAnimatePipeline.from_pretrained(MID, transformer=None, vae=None, torch_dtype=torch.bfloat16)
with torch.no_grad():
    pe, _ = te.encode_prompt(prompt=JOB["prompt"], do_classifier_free_guidance=False, device="cpu", max_sequence_length=226)
del te; gc.collect()
log("mã hóa câu mô tả xong")

def load(dt):
    q = PipelineQuantizationConfig(quant_backend="bitsandbytes_4bit",
                                   quant_kwargs={"load_in_4bit": True, "bnb_4bit_quant_type": "nf4", "bnb_4bit_compute_dtype": dt},
                                   components_to_quantize=["transformer"])
    vae = AutoencoderKLWan.from_pretrained(MID, subfolder="vae", torch_dtype=torch.float32)
    p = WanAnimatePipeline.from_pretrained(MID, vae=vae, text_encoder=None, tokenizer=None, torch_dtype=dt,
                                           quantization_config=q)
    p.enable_model_cpu_offload()
    try:
        p.vae.enable_tiling()
    except Exception:
        pass
    return p

dt = torch.float16
pipe = load(dt)
log("tải xong Wan 2.2 Animate 14B (4-bit)", str(dt))
ref = Image.open(f"{IN}/anh.jpg").convert("RGB").resize((W, H), Image.LANCZOS)
res = {"clips": {}}

for c in JOB["clips"]:
    key = c["key"]
    try:
        t1 = time.time()
        frames = read_clip(f"{IN}/{c['file']}")
        log(key, "đọc", len(frames), "khung; làm pose + face")
        pose, face = pose_frames(frames), face_crops(frames)
        n = min(len(pose), len(face))
        pose, face = pose[:n], face[:n]
        log(key, "tiền xử lý xong", round(time.time() - t1), "giây; bắt đầu tạo video")
        for attempt in range(2):
            try:
                out = pipe(image=ref, pose_video=pose, face_video=face, prompt_embeds=pe.to("cuda", dt),
                           height=H, width=W, segment_frame_length=77, prev_segment_conditioning_frames=1,
                           guidance_scale=1.0, num_inference_steps=JOB["steps"], mode="animate",
                           generator=torch.Generator("cuda").manual_seed(0)).frames[0]
                arr = np.asarray(out[len(out) // 2])
                if float(arr.mean()) < (3 if arr.max() > 1.5 else 3 / 255):
                    raise RuntimeError("video đen (tràn số fp16)")
                export_to_video(out, f"{OUT}/{key}.mp4", fps=JOB["fps"])
                break
            except Exception as e:
                log("LỖI", key, repr(e)[:400]); traceback.print_exc()
                if dt == torch.float16 and attempt == 0:
                    del pipe; gc.collect(); torch.cuda.empty_cache()
                    dt = torch.bfloat16; pipe = load(dt); log("chuyển sang bf16")
                else:
                    raise
        sec = time.time() - t1
        res["clips"][key] = {"giay": round(sec), "khung": len(out), "dtype": str(dt)}
        log("xong", key, f"{sec:.0f}s")
    except Exception as e:
        res["clips"][key] = {"loi": repr(e)[:400]}
        log("BỎ", key, repr(e)[:300])
    gc.collect(); torch.cuda.empty_cache()
res["tong_giay"] = round(time.time() - t0)
json.dump(res, open(f"{OUT}/ket_qua.json", "w"), ensure_ascii=False, indent=1)
log("XONG", res)
'''


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"Lỗi lệnh: {' '.join(map(str, cmd))}\n{(r.stderr or r.stdout)[-1500:]}")
    return r.stdout


def duration(p):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(p)]).strip())


def cmd_gui(a):
    mau, anh = Path(a.mau), Path(a.anh)
    if not mau.exists() or not anh.exists():
        sys.exit(f"Thiếu file: {mau if not mau.exists() else anh}")
    total = 3.0 if a.thu else a.tong
    avail = duration(mau) - a.bat_dau
    if avail < total:
        print(f"[!] Video mẫu chỉ còn {avail:.1f}s kể từ giây {a.bat_dau}; dùng {avail:.1f}s")
        total = avail
    shutil.rmtree(WORK, ignore_errors=True)
    ds = WORK / "dataset"
    ds.mkdir(parents=True)
    from PIL import Image, ImageOps
    # cắt ảnh cho đúng tỉ lệ khung (giữ phần trên, không bóp méo) để kernel không phải kéo giãn ảnh
    ImageOps.fit(Image.open(anh).convert("RGB"), (a.rong * 2, a.cao * 2), Image.LANCZOS,
                 centering=(0.5, 0.0)).save(ds / "anh.jpg", quality=92)
    clips, t, i = [], 0.0, 0
    while t < total - 0.05:
        ln = min(a.doan, total - t)
        f = f"in_{i:02d}.mp4"
        # nhỏ gọn (cạnh ngắn 480), đúng 30 khung/giây, không tiếng
        sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(a.bat_dau + t), "-i", str(mau), "-t", str(ln), "-r", str(FPS),
            "-vf", "scale=-2:'min(960,ih)'", "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", "-an", str(ds / f)])
        clips.append({"key": f"{a.ten}_{i:02d}", "file": f, "giay": round(ln, 2)})
        t += ln
        i += 1
    job = {"ten": a.ten, "w": a.rong, "h": a.cao, "fps": FPS, "steps": a.buoc_suy_luan, "prompt": a.prompt or PROMPT,
           "neg": NEG, "bat_dau": a.bat_dau, "tong": round(total, 2), "clips": clips}
    (ds / "job.json").write_text(json.dumps(job, ensure_ascii=False, indent=1), encoding="utf-8")
    size = sum(p.stat().st_size for p in ds.iterdir()) / 1e6
    print(f"Chuẩn bị xong: {len(clips)} đoạn, tổng {total:.1f}s, khung {a.rong}x{a.cao}, dữ liệu {size:.1f} MB")

    user, env = kaggle_draw._env()
    (ds / "dataset-metadata.json").write_text(json.dumps(
        {"title": DATASET, "id": f"{user}/{DATASET}", "licenses": [{"name": "CC0-1.0"}], "isPrivate": True}), encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "kaggle", "datasets", "create", "-p", str(ds)],
                       capture_output=True, text=True, env=env)
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode != 0 or "error" in out.lower():
        print("Dataset đã có hoặc tạo lỗi, thử đẩy phiên bản mới...")
        kaggle_draw._kaggle(["datasets", "version", "-p", str(ds), "-m", f"{a.ten} {time.strftime('%Y-%m-%d %H:%M')}"], env)
    print("Đợi Kaggle xử lý dataset...", flush=True)
    for _ in range(40):
        st = kaggle_draw._kaggle(["datasets", "status", f"{user}/{DATASET}"], env, check=False).strip().lower()
        if "ready" in st:
            break
        time.sleep(15)
    else:
        sys.exit(f"Dataset chưa sẵn sàng sau 10 phút: {st}")

    k = WORK / "k"
    k.mkdir()
    code = KERNEL.replace("__HFTOK__", repr(os.environ.get("HF_TOKEN", "").strip()))
    (k / "run.py").write_text(code, encoding="utf-8")
    meta = {"id": f"{user}/{SLUG}", "title": SLUG, "code_file": "run.py", "language": "python",
            "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": True,
            "enable_tpu": False, "dataset_sources": [f"{user}/{DATASET}"], "competition_sources": [],
            "kernel_sources": [], "model_sources": []}
    (k / "kernel-metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    kaggle_draw._kaggle(["kernels", "push", "-p", str(k)], env)
    print(f"Đã gửi kernel {user}/{SLUG}. Kaggle chạy nền; vài giờ sau chạy: python kaggle_dance.py lay --ten {a.ten} --mau {a.mau}")


def cmd_lay(a):
    user, env = kaggle_draw._env()
    t0 = time.time()
    while True:
        st = kaggle_draw._kaggle(["kernels", "status", f"{user}/{SLUG}"], env, check=False).lower()
        short = (st.strip().splitlines() or [""])[-1].split("status")[-1].strip(' "')
        print(f"Kaggle: {short}", flush=True)
        if any(w in st for w in ("complete", "error", "cancel")):
            break
        if time.time() - t0 >= a.cho * 60:
            print("Kaggle chưa chạy xong; lát nữa chạy lại bước 'lay'.")
            return
        time.sleep(60)
    out = WORK / "out"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    kaggle_draw._kaggle(["kernels", "output", f"{user}/{SLUG}", "-p", str(out), "-o"], env, check=False)
    logs_dir = ROOT / "logs" / "kaggle_dance"
    logs_dir.mkdir(parents=True, exist_ok=True)
    for lg in out.glob("*.log"):
        shutil.copy(lg, logs_dir / f"{a.ten}_kaggle_log.txt")
    jf = next(iter(out.rglob("job.json")), None)
    if not jf:
        sys.exit("Không thấy job.json trong kết quả; xem logs/kaggle_dance/ để biết lỗi")
    job = json.loads(jf.read_text(encoding="utf-8"))
    if job.get("ten") != a.ten:
        sys.exit(f"Kết quả trên Kaggle là của video '{job.get('ten')}', không phải '{a.ten}'")
    parts = []
    for c in job["clips"]:
        f = next(iter(out.rglob(f"{c['key']}.mp4")), None)
        if not f:
            print(f"[!] Thiếu đoạn {c['key']} (xem logs/kaggle_dance/{a.ten}_kaggle_log.txt)")
            break           # ghép liền mạch từ đầu tới đoạn lỗi đầu tiên
        parts.append(f)
    if not parts:
        sys.exit("Không có đoạn nào để ghép")
    lst = out / "list.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    dest = ROOT / "output" / "dance"
    dest.mkdir(parents=True, exist_ok=True)
    merged = out / "merged.mp4"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264",
        "-pix_fmt", "yuv420p", "-an", str(merged)])
    final = dest / f"{a.ten}.mp4"
    got = duration(merged)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(merged)]
    if a.mau and Path(a.mau).exists():       # nhạc lấy đúng đoạn của video mẫu để khớp nhịp nhảy
        cmd += ["-ss", str(job["bat_dau"]), "-t", f"{got:.2f}", "-i", str(a.mau), "-map", "0:v", "-map", "1:a?",
                "-c:v", "copy", "-c:a", "aac", "-shortest"]
    else:
        cmd += ["-c:v", "copy"]
    sh(cmd + [str(final)])
    print(f"Xong: {final} ({got:.1f}s, {len(parts)}/{len(job['clips'])} đoạn)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="lenh", required=True)
    g = sub.add_parser("gui")
    g.add_argument("--ten", required=True)
    g.add_argument("--anh", required=True)
    g.add_argument("--mau", required=True)
    g.add_argument("--tong", type=float, default=30)
    g.add_argument("--doan", type=float, default=10, help="độ dài mỗi đoạn (giây)")
    g.add_argument("--bat-dau", type=float, default=0)
    g.add_argument("--rong", type=int, default=368, help="bội số của 16")
    g.add_argument("--cao", type=int, default=640, help="bội số của 16")
    g.add_argument("--buoc-suy-luan", type=int, default=20)
    g.add_argument("--prompt", default="")
    g.add_argument("--thu", action="store_true", help="chỉ làm 3 giây để thử")
    g.set_defaults(f=cmd_gui)
    l = sub.add_parser("lay")
    l.add_argument("--ten", required=True)
    l.add_argument("--mau", default="")
    l.add_argument("--cho", type=float, default=0, help="số phút chờ Kaggle xong (0 = chỉ xem một lần)")
    l.set_defaults(f=cmd_lay)
    a = ap.parse_args()
    if a.lenh == "gui" and (a.rong % 16 or a.cao % 16):
        sys.exit("--rong và --cao phải là bội số của 16")
    a.f(a)


if __name__ == "__main__":
    main()
