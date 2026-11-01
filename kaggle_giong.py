"""Nhân bản giọng trên GPU Kaggle: F5-TTS tiếng Việt + đoạn mẫu cố định (giọng nghe_B3), đọc cả video cùng một giọng.
  python kaggle_giong.py <kịch_bản.json> <thư_mục_ra> [mau=<wav>:<txt>] [seed=7] [gioi_han=N]    -> gửi Kaggle, đợi, tải về <thư_mục_ra>/<n>.mp3
  python kaggle_giong.py chi_tai_lai=1 ...   -> chỉ tải lại kết quả lần chạy trước"""
import base64, json, os, shutil, subprocess, sys, time
from pathlib import Path
import kaggle_draw as kd

ROOT = Path(__file__).resolve().parent
SLUG = "ngs-giong-clone"
MAU_WAV = ROOT / "ke-hoach/thu-giong-hai/giong_mau/b3_mau.wav"
MAU_TXT = ROOT / "ke-hoach/thu-giong-hai/giong_mau/b3_mau.txt"

KERNEL = r'''
import json, os, sys, time, subprocess, traceback, base64, glob, gc
t0 = time.time()
def log(*a): print(f"[{time.time()-t0:6.0f}s]", *a, flush=True)
os.environ["HF_HOME"] = "/tmp/hf"
if __HFTOK__: os.environ["HF_TOKEN"] = __HFTOK__
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "f5-tts", "soundfile", "huggingface_hub"], check=False)
log("cài xong")
import torch, soundfile as sf, numpy as np
from huggingface_hub import snapshot_download, HfApi
OUT = "/kaggle/working/out"; os.makedirs(OUT, exist_ok=True)
log("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "KHÔNG CÓ GPU")
BEATS = json.loads(__BEATS__); SEED = __SEED__
REF = "/kaggle/working/mau.wav"; open(REF, "wb").write(base64.b64decode(__MAU__)); REF_TXT = __MAUTXT__
# --- tìm mô hình tiếng Việt ---
repo = None
for cand in ["hynt/F5-TTS-Vietnamese-ViVoice"]:
    try:
        d = snapshot_download(cand); repo = cand; break
    except Exception as e: log("không tải được", cand, str(e)[:120])
if repo is None:
    try:
        for m in HfApi().list_models(search="F5-TTS-Vietnamese", sort="downloads", direction=-1, limit=10): log("ỨNG VIÊN", m.id)
    except Exception as e: log("tìm lỗi", e)
    raise SystemExit("không có mô hình")
log("repo", repo, "files:", [os.path.relpath(p, d) for p in glob.glob(d + "/**/*", recursive=True) if os.path.isfile(p)][:30])
for fn in ("README.md", "config.json"):
    try: log("=====", fn, "=====\n" + open(os.path.join(d, fn), encoding="utf-8").read()[:2500])
    except Exception as e: log("không đọc", fn, e)
ck = sorted([p for p in glob.glob(d + "/**/*", recursive=True) if p.endswith((".pt", ".safetensors"))], key=lambda p: -os.path.getsize(p))
vocab = [p for p in glob.glob(d + "/**/*", recursive=True) if os.path.basename(p).startswith("vocab") and p.endswith(".txt")]
if not vocab:   # tìm vocab ở repo khác của cùng tác giả hoặc bản tiếng Việt khác
    try:
        from huggingface_hub import hf_hub_download, list_repo_files
        cands = ["hynt/F5-TTS-Vietnamese-ViVoice"] + [m.id for m in HfApi().list_models(search="F5-TTS-Vietnamese", sort="downloads", direction=-1, limit=15)] + [m.id for m in HfApi().list_models(search="F5-TTS-Viet", limit=15)]
        seen = set()
        for r in cands:
            if r in seen: continue
            seen.add(r)
            try:
                fl = list_repo_files(r); vf = [f for f in fl if "vocab" in f.lower()]
                log("ỨNG VIÊN", r, vf[:3])
                for f in vf:
                    if f.endswith(".txt"):
                        pth = hf_hub_download(r, f)
                        n = sum(1 for _ in open(pth, encoding="utf-8"))
                        log("  vocab", r, f, "dòng:", n)
                        if abs(n - 2566) <= 3 or n == 2567: vocab = [pth]; break
            except Exception as e: log("  lỗi", r, str(e)[:100])
            if vocab: break
    except Exception as e: log("tìm vocab lỗi", e)
log("ckpt", ck[:3], "vocab", vocab)
from f5_tts.api import F5TTS
f5 = None
for name in ["F5TTS_Base", "F5TTS_v1_Base"]:
    try:
        f5 = F5TTS(model=name, ckpt_file=ck[0], vocab_file=vocab[0] if vocab else "", device="cuda"); log("nạp được với", name); break
    except Exception as e:
        log("nạp lỗi", name, str(e)[:200]); traceback.print_exc()
if f5 is None: raise SystemExit("không nạp được F5")
done = {}
for i, b in enumerate(BEATS):
    n = b["n"]; txt = b["text"].strip()
    try:
        wav, sr, _ = f5.infer(ref_file=REF, ref_text=REF_TXT, gen_text=txt, seed=SEED, remove_silence=False, speed=1.0, nfe_step=32, cfg_strength=2.0)
        sf.write(f"{OUT}/{n}.wav", wav, sr); done[n] = round(len(wav) / sr, 2)
        if i < 3 or i % 10 == 0: log("xong", n, done[n], "s /", len(txt.split()), "chữ")
    except Exception as e:
        log("LỖI", n, str(e)[:200]); traceback.print_exc()
    gc.collect(); torch.cuda.empty_cache()
json.dump(done, open(f"{OUT}/done.json", "w"))
log("XONG", len(done), "/", len(BEATS))
'''

def main():
    args = [a for a in sys.argv[1:] if "=" not in a]
    kv = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
    kich, outd = Path(args[0]), Path(args[1])
    user, env = kd._env()
    work = ROOT / "output" / "_giong"
    if "chi_tai_lai" not in kv:
        shutil.rmtree(work, ignore_errors=True); (work / "k").mkdir(parents=True)
        beats = json.loads(kich.read_text(encoding="utf-8"))
        gh = int(kv.get("gioi_han", 0)) or len(beats)
        beats = [{"n": b["n"], "text": b.get("tts", b["text"])} for b in beats[:gh]]
        code = (KERNEL.replace("__BEATS__", repr(json.dumps(beats, ensure_ascii=False)))
                .replace("__SEED__", kv.get("seed", "7"))
                .replace("__MAU__", repr(base64.b64encode(MAU_WAV.read_bytes()).decode()))
                .replace("__MAUTXT__", repr(MAU_TXT.read_text(encoding="utf-8").strip()))
                .replace("__HFTOK__", repr(os.environ.get("HF_TOKEN", "").strip())))
        (work / "k" / "giong.py").write_text(code, encoding="utf-8")
        meta = {"id": f"{user}/{SLUG}", "title": SLUG, "code_file": "giong.py", "language": "python", "kernel_type": "script",
                "is_private": True, "enable_gpu": True, "enable_internet": True, "enable_tpu": False,
                "dataset_sources": [], "competition_sources": [], "kernel_sources": [], "model_sources": []}
        (work / "k" / "kernel-metadata.json").write_text(json.dumps(meta), encoding="utf-8")
        print("Gửi sang Kaggle", flush=True)
        kd._kaggle(["kernels", "push", "-p", str(work / "k")], env)
        t0 = time.time(); last = None
        while time.time() - t0 < 100 * 60:
            time.sleep(30)
            st = kd._kaggle(["kernels", "status", f"{user}/{SLUG}"], env, check=False).lower()
            short = (st.strip().splitlines()[-1] if st.strip() else "").split("status")[-1].strip(' "')
            if short != last: print(f"{(time.time() - t0) / 60:4.1f} phút: {short}", flush=True); last = short
            if any(w in st for w in ("complete", "error", "cancel")): break
    (work / "out").mkdir(parents=True, exist_ok=True)
    kd._kaggle(["kernels", "output", f"{user}/{SLUG}", "-p", str(work / "out"), "-o"], env, check=False)
    outd.mkdir(parents=True, exist_ok=True)
    for lg in (work / "out").glob("*.log"): shutil.copy(lg, outd / "kaggle_giong.log")
    got = 0
    for w in (work / "out").rglob("*.wav"):
        if w.name == "mau.wav": continue
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(w), "-ac", "1", "-ar", "44100", "-b:a", "128k", str(outd / (w.stem + ".mp3"))], check=True); got += 1
    print(f"Nhận {got} đoạn")

if __name__ == "__main__":
    main()
