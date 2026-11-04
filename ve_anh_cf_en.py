"""Vẽ ảnh minh họa bí ẩn bằng Cloudflare AI (FLUX) cho các ô trong anh_ai.json; ô còn lại dùng ảnh tư liệu.
  python ve_anh_cf_en.py ke-hoach/roanoke/roanoke.json [lam_lai=S01,S18]
Ảnh ra: assets/anh_en/<mã>/ai/<ô>.jpg (đã có thì bỏ qua, không tốn lượt). Hết mọi tài khoản Cloudflare thì dừng ngay.
Lọc tự động: viền tối quanh khung -> vẽ lại với hạt giống khác (tối đa 3 lần). Báo cáo: logs/ve_anh_en.txt."""
import json, os, random, sys
from pathlib import Path
import numpy as np
from PIL import Image

import ai_images

ROOT = Path(__file__).resolve().parent
MOOD = ", moody mysterious atmosphere, dramatic chiaroscuro, drifting fog, cinematic, painterly"


def has_border(path):
    a = np.asarray(Image.open(path).convert("L"), dtype=float)
    h, w = a.shape
    inner = a[h // 6: -h // 6, w // 6: -w // 6].mean()
    for edge in (a[:10, :], a[-10:, :], a[:, :10], a[:, -10:]):
        if edge.std() < 6 and abs(edge.mean() - inner) > 45:
            return True
    return False


def main():
    script = Path(sys.argv[1]); d = json.loads(script.read_text(encoding="utf-8"))
    redo = set()
    for a in sys.argv[2:]:
        if a.startswith("lam_lai="): redo = {x.strip() for x in a.split("=", 1)[1].split(",") if x.strip()}
    prompts = json.loads((script.parent / "anh_ai.json").read_text(encoding="utf-8"))
    out = ROOT / "assets" / "anh_en" / d["id"] / "ai"; out.mkdir(parents=True, exist_ok=True)
    (ROOT / "logs").mkdir(exist_ok=True)
    rep, ok, fail = [], 0, 0
    for slot, p in prompts.items():
        dest = out / f"{slot}.jpg"
        if slot in redo and dest.exists(): dest.unlink()
        if dest.exists():
            rep.append(f"{slot}: đã có"); continue
        style = ai_images.photo_style(p) + MOOD
        done = False
        for k in range(3):
            tmp = out / f"{slot}_t{k}.png"
            try:
                ai_images.generate(p, tmp, wide=True, style=style, seed=random.randint(1, 10**6), cheap=True)
            except RuntimeError as e:
                rep.append(f"{slot}: ⛔ {str(e)[:120]}")
                print("\n".join(rep)); (ROOT / "logs" / "ve_anh_en.txt").write_text("\n".join(rep), encoding="utf-8")
                print("⛔ Cloudflare hết lượt hoặc lỗi: DỪNG."); sys.exit(3)
            if has_border(tmp):
                rep.append(f"{slot}: lần {k + 1} có viền, vẽ lại"); tmp.unlink(); continue
            Image.open(tmp).convert("RGB").resize((1344, 768), Image.LANCZOS).save(dest, quality=92)
            tmp.unlink(); rep.append(f"{slot}: ✅"); ok += 1; done = True; break
        if not done: fail += 1; rep.append(f"{slot}: ❌ 3 lần đều lỗi viền")
    rep.append(f"Tổng: vẽ mới {ok}, lỗi {fail}")
    (ROOT / "logs" / "ve_anh_en.txt").write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
