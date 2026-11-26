"""Vẽ tranh thủy mặc trên Kaggle (FLUX.2 klein 4B, khung 16:9 1344x768) cho một danh sách ke-hoach/nhan-vat/<mã>_anh.json.
Mã lấy từ dòng cuối ke-hoach/thu-giong-hai/kg_thuy_mac_chay.txt (vd "lan1 NBTM28A NBTM28B"). Kết quả: assets/anh_2d/<mã>_kg/<key>.jpg"""
import json, sys
from pathlib import Path
from kaggle_draw import draw_batch
ma = Path("ke-hoach/thu-giong-hai/kg_thuy_mac_chay.txt").read_text().strip().split()[1:]
jobs, dest = [], {}
for m in ma:
    for it in json.loads(Path(f"ke-hoach/nhan-vat/{m}_anh.json").read_text(encoding="utf-8")):
        jobs.append((it["key"], it["prompt"][:2000], it.get("w", 1344), it.get("h", 768), it.get("seed", len(jobs))))
        dest[it["key"]] = m
tmp = Path("output/_kg_out")
res = draw_batch(jobs, tmp, model="klein", timeout_min=150)
log = []
for k, m in dest.items():
    if k in res:
        out = Path(f"assets/anh_2d/{m}_kg"); out.mkdir(parents=True, exist_ok=True)
        res[k].rename(out / f"{k}.jpg"); log.append(f"{k}: OK")
    else:
        log.append(f"{k}: LỖI")
Path("logs").mkdir(exist_ok=True)
Path("logs/kg_thuy_mac.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
print(f"{len(res)}/{len(jobs)}")
