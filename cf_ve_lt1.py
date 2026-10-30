"""Vẽ thử ảnh lt1 trên Cloudflare (FLUX.2 klein), cùng prompt với Kaggle, KHÔNG dùng ảnh vector.
  python cf_ve_lt1.py 19015,19033   -> assets/anh_chibi/lt1_cf/<n>.jpg
"""
import io
import json
import sys
from pathlib import Path

import ai_images as ai

ROOT = Path(__file__).resolve().parent
items = {i["n"]: i for i in json.loads((ROOT / "ke-hoach/chibi/lt1_chibi.json").read_text(encoding="utf-8"))}
want = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else sorted(items)
out = ROOT / "assets/anh_chibi/lt1_cf"
out.mkdir(parents=True, exist_ok=True)
for n in want:
    tmp = out / f"{n}.raw"
    try:
        ai._klein(items[n]["prompt"], tmp, True, seed=n)
        from PIL import Image
        Image.open(tmp).convert("RGB").save(out / f"{n}.jpg", quality=92)
        tmp.unlink()
        print("ok", n, flush=True)
    except Exception as e:
        print("lỗi", n, e, flush=True)
