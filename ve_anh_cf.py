"""Vẽ lại ảnh TQ9 bằng FLUX.2 klein trên Cloudflare, đúng prompt trong TQ9_anh.json (không thêm style).
Ảnh ra assets/anh_2d/TQ9CF/NNN.jpg (không đè bộ chính). Dùng: python ve_anh_cf.py 004,028,..."""
import json, sys, io
from pathlib import Path
from PIL import Image
import ai_images as A

keys = [k.strip() for k in sys.argv[1].split(",") if k.strip()]
data = {str(d["key"]).zfill(3): d for d in json.load(open("ke-hoach/nhan-vat/TQ9_anh.json", encoding="utf-8"))}
out_dir = Path(("assets/anh_2d/TQ9CF" + (sys.argv[3] if len(sys.argv) > 3 else ""))); out_dir.mkdir(parents=True, exist_ok=True)
ok, fail = [], []
for k in keys:
    d = data.get(k)
    if not d: fail.append((k, "không có trong TQ9_anh.json")); continue
    out = out_dir / f"{k}.jpg"
    if out.exists() and out.stat().st_size > 10000: ok.append(k); continue
    tmp = out_dir / f"{k}.raw"
    for att in range(3):
        try:
            if A._CF_OUT["v"] and not A._next_account(print):
                raise RuntimeError("hết lượt Cloudflare mọi tài khoản")
            A._klein(d["prompt"][:2000], tmp, True, int(k) + 1000 * int(sys.argv[2] if len(sys.argv) > 2 else 0) + 1000)
            im = Image.open(tmp).convert("RGB")
            if im.size != (1344, 768): im = im.resize((1344, 768), Image.LANCZOS)
            im.save(out, quality=93); tmp.unlink(missing_ok=True)
            print("🎨", k, len(d["prompt"]), "ký tự"); ok.append(k); break
        except RuntimeError as e:
            print("⚠️", k, str(e)[:150])
            if A._CF_OUT["v"] and A._next_account(print): continue
            if A._CF_OUT["v"]: fail.append((k, "hết lượt")); break
    else:
        fail.append((k, "lỗi"))
    if fail and fail[-1][1] == "hết lượt": break
print("ĐẠT", ok); print("LỖI", fail)
sys.exit(1 if fail else 0)
