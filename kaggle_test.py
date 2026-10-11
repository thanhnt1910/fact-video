"""Thử vẽ trên Kaggle bằng đúng câu mô tả của 4 tranh đã vẽ trên Cloudflare, để so sánh (logs/kaggle_test.jpg)."""
import json
from pathlib import Path
from PIL import Image
import ai_images, kaggle_draw
WIDE_HINT = "wide cinematic composition, main subject centered with space above and below"  # giống long_video.py
ROOT = Path(__file__).resolve().parent


def beat(sid, n):
    d = json.loads((ROOT / "scripts" / f"{sid}.json").read_text(encoding="utf-8"))
    bs = [b for ch in d["long"]["chapters"] for b in ch["beats"]]
    return f"{bs[n - 1]['ai']}, {WIDE_HINT}, {ai_images.STYLE}"


jobs = [("t1", beat("ST1", 44), 1344, 768), ("t2", beat("SL2", 3), 1344, 768),
        ("t3", beat("SL2", 37), 1344, 768), ("t4", beat("BA1", 2), 1344, 768)]
res = kaggle_draw.draw_batch(jobs, ROOT / "output" / "_kt", model="klein")
ims = [Image.open(res[k]) for k, *_ in jobs if k in res]
if ims:
    sheet = Image.new("RGB", (672 * 2, 384 * ((len(ims) + 1) // 2)))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((672, 384)), ((i % 2) * 672, (i // 2) * 384))
    sheet.save(ROOT / "logs" / "kaggle_test.jpg", quality=88)
print("kết quả:", list(res))
