"""Vẽ ảnh lt1 trên Cloudflare (FLUX.2 klein), chỉ từ lời mô tả, KHÔNG dùng ảnh vector.
  python cf_ve_lt1.py 19015,19033   -> assets/anh_chibi/lt1_cf/<n>.jpg
  python cf_ve_lt1.py all           -> mọi cảnh
Hết lượt tài khoản này thì tự chuyển tài khoản kế; hết cả ba thì dừng và ghi 'HET_LUOT' để chạy tiếp hôm sau.
"""
import json
import sys
from pathlib import Path

from PIL import Image

import ai_images as ai

ROOT = Path(__file__).resolve().parent
items = {i["n"]: i for i in json.loads((ROOT / "ke-hoach/chibi/lt1_chibi.json").read_text(encoding="utf-8"))}
arg = sys.argv[1] if len(sys.argv) > 1 else "all"
want = sorted(items) if arg == "all" else [int(x) for x in arg.split(",") if x]
out = ROOT / "assets/anh_chibi/lt1_cf"
out.mkdir(parents=True, exist_ok=True)
for n in want:
    tmp = out / f"{n}.raw"
    for attempt in range(3):
        try:
            ai._klein(items[n]["prompt"], tmp, True, seed=n)
            Image.open(tmp).convert("RGB").save(out / f"{n}.jpg", quality=92)
            tmp.unlink()
            print("ok", n, flush=True)
            break
        except Exception as e:
            if "hết lượt" in str(e):
                if ai._next_account(print):
                    continue
                print("HET_LUOT", n, flush=True)
                sys.exit(3)
            print("lỗi", n, str(e)[:200], flush=True)
            break
