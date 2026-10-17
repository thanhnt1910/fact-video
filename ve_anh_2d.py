"""
Vẽ hàng loạt tranh 2D cho một câu chuyện (miễn phí, GPU Kaggle, FLUX.2 klein 4B).

  python ve_anh_2d.py ST3                 -> vẽ mọi ảnh chưa có trong assets/anh_2d/ST3/
  python ve_anh_2d.py ST3 007,031 2       -> vẽ lại ảnh số 007 và 031 với hạt giống mới (đợt 2)

Danh sách câu mô tả: ke-hoach/nhan-vat/<mã>_anh.json (do tao_<mã>.py tạo). Ảnh ra: assets/anh_2d/<mã>/<số>.jpg
"""
import json
import os
import sys
from pathlib import Path

import kaggle_draw

ROOT = Path(__file__).resolve().parent


def main():
    ma = sys.argv[1]
    redo = [x.strip() for x in (sys.argv[2] if len(sys.argv) > 2 else "").split(",") if x.strip()]
    dot = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    items = json.loads((ROOT / "ke-hoach" / "nhan-vat" / f"{ma}_anh.json").read_text(encoding="utf-8"))
    out = ROOT / "assets" / "anh_2d" / (ma + os.environ.get("OUT_SUFFIX", ""))
    out.mkdir(parents=True, exist_ok=True)
    jobs = []
    for it in items:
        k = it["key"]
        f = out / f"{k}.jpg"
        if redo:
            if k not in redo:
                continue
        elif f.exists():
            continue
        jobs.append((k, it["prompt"], 1344, 768, int(k) + 1000 * dot, it.get("refs", [])))
    print(f"Cần vẽ {len(jobs)} ảnh (đợt {dot})")
    if not jobs:
        return
    os.environ.pop('X', None)
    rd = ROOT / "ke-hoach" / "nhan-vat" / "refs"
    names = {n for j in jobs for n in j[5]}
    refs = {n: rd / f"{n}.jpg" for n in names if (rd / f"{n}.jpg").exists()}
    res = kaggle_draw.draw_batch(jobs, out, model="klein", timeout_min=150, refs=refs)
    print(f"Nhận về {len(res)}/{len(jobs)} ảnh")
    miss = [j[0] for j in jobs if j[0] not in res]
    if miss:
        print("Chưa vẽ được:", ",".join(miss))


if __name__ == "__main__":
    main()
