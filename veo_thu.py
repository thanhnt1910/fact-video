"""
THỬ AI BIẾN ẢNH THÀNH VIDEO (Veo 3.1 Lite qua Gemini API) cho 1 tranh của kịch bản.

  python veo_thu.py scripts/ST1.json [số_đoạn=0] [giây=4] ["mô tả chuyển động tiếng Anh"]

- Lấy tranh AI của đoạn video dài thứ <số_đoạn> (trong bộ nhớ đệm assets/ai_cache, chưa có thì vẽ bằng FLUX).
- Tạo 2 clip: ngang 16:9 (video dài) và dọc 9:16 (hook video ngắn, cắt giữa tranh).
- Chỉ dùng bản Lite (rẻ nhất), không có thì dùng Fast; không bao giờ dùng bản thường (đắt gấp 8 lần).
Kết quả: logs/veo/<mã>_ngang.mp4, <mã>_doc.mp4 (đã bỏ tiếng), <mã>_veo.txt (model, prompt, thời gian).
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "logs" / "veo"

# chuyển động mô tả bằng tiếng Anh; giữ nét vẽ của tranh, không chữ
MOTION_HINT = ("Keep the exact same 2D hand-drawn illustration style, colors and characters as the starting image. "
               "Smooth, natural, subtle motion only; correct anatomy and hands; no morphing; no text, no captions, "
               "no watermark, no new characters, no scene cut.")


def pick_model(client, log=print):
    names = [m.name.split("/")[-1] for m in client.models.list()]
    veo = [n for n in names if n.startswith("veo-3")]
    log(f"Model Veo có sẵn: {', '.join(veo) or '(không có)'}")
    for want in ("lite", "fast"):
        c = sorted(n for n in veo if want in n and "3.1" in n) or sorted(n for n in veo if want in n)
        if c:
            return c[-1]
    raise SystemExit("Không tìm thấy Veo Lite/Fast trong tài khoản; dừng để tránh dùng bản đắt.")


def source_image(script, idx, log=print):
    import ai_images
    beats = [b for ch in script["long"]["chapters"] for b in ch["beats"] if b.get("ai")]
    b = beats[idx]
    key = hashlib.sha1((ai_images.STYLE_ID + "|" + b["ai"]).encode()).hexdigest()[:16]
    f = ROOT / "assets" / "ai_cache" / f"{key}.jpg"
    if not f.exists():
        import long_video
        log("Tranh chưa có trong bộ nhớ đệm, vẽ lại bằng FLUX")
        ai_images.generate(b["ai"] + ", " + long_video.WIDE_HINT, f, log=log, wide=True)
    return f, b


def run(client, model, img_path, prompt, aspect, seconds, out, log=print):
    from google.genai import types
    t0 = time.time()
    op = client.models.generate_videos(
        model=model, prompt=prompt, image=types.Image.from_file(location=str(img_path)),
        config=types.GenerateVideosConfig(aspect_ratio=aspect, duration_seconds=seconds, number_of_videos=1, resolution="720p"))
    while not op.done:
        time.sleep(10)
        op = client.operations.get(op)
    if getattr(op, "error", None):
        raise RuntimeError(f"Veo lỗi: {op.error}")
    vids = (op.response.generated_videos if op.response else None) or []
    if not vids:
        raise RuntimeError(f"Veo không trả về video (có thể bị bộ lọc an toàn chặn): {op.response}")
    raw = out.with_suffix(".raw.mp4")
    client.files.download(file=vids[0].video)
    vids[0].video.save(str(raw))
    # bỏ tiếng Veo tự tạo (video của kênh dùng giọng kể + nhạc riêng)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(raw), "-an", "-c:v", "copy", str(out)], check=True)
    raw.unlink(missing_ok=True)
    try:
        import chi_phi
        chi_phi.add_video(model, seconds)
    except Exception:
        pass
    log(f"  ✅ {out.name}: {time.time() - t0:.0f} giây")
    return time.time() - t0


def main():
    from google import genai
    from PIL import Image
    script = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    seconds = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    OUT.mkdir(parents=True, exist_ok=True)
    import gemini_keys
    keys = gemini_keys.all_keys()
    only = os.environ.get("VEO_ONLY", "").strip()   # "ngang" hoặc "doc": chỉ tạo 1 clip cho đỡ tốn
    client = genai.Client(api_key=keys[0])
    model = pick_model(client)
    print(f"Dùng model: {model}; {len(keys)} khóa")
    img, beat = source_image(script, idx)
    sid = script["id"]
    motion = sys.argv[4].strip() if len(sys.argv) > 4 and sys.argv[4].strip() else (beat.get("veo") or beat["ai"])
    prompt = motion + ". " + MOTION_HINT
    # ảnh dọc cho hook: cắt giữa tranh ngang
    im = Image.open(img).convert("RGB")
    w, h = im.size
    cw = int(h * 9 / 16)
    x0 = max(0, (w - cw) // 2)
    vert = OUT / f"{sid}_nguon_doc.jpg"
    im.crop((x0, 0, x0 + cw, h)).resize((720, 1280), Image.LANCZOS).save(vert, quality=95)
    horiz = OUT / f"{sid}_nguon_ngang.jpg"
    im.save(horiz, quality=95)
    notes = [f"model: {model}", f"giây mỗi clip: {seconds}", f"prompt: {prompt}"]
    for name, src, aspect in (("ngang", horiz, "16:9"), ("doc", vert, "9:16")):
        if only and only != name:
            continue
        done = False
        for n, k in enumerate(keys, 1):   # thử lần lượt từng khóa tới khi có khóa tạo được
            try:
                dt = run(genai.Client(api_key=k), model, src, prompt, aspect, seconds, OUT / f"{sid}_{name}.mp4")
                notes.append(f"{name} ({aspect}): khóa số {n} (…{k[-4:]}) xong sau {dt:.0f} giây")
                done = True
                break
            except Exception as e:
                msg = " ".join(str(e).split())[:400]
                print(f"  ⚠️  {name} khóa {n}: {msg}")
                notes.append(f"{name} ({aspect}) khóa số {n} (…{k[-4:]}): LỖI {msg}")
        if not done:
            notes.append(f"{name}: không khóa nào tạo được Veo")
    (OUT / f"{sid}_veo.txt").write_text("\n".join(notes) + "\n", encoding="utf-8")
    print("\n".join(notes))
    import chi_phi
    print(chi_phi.summary() or "")


if __name__ == "__main__":
    main()
