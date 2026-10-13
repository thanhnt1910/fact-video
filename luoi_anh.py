"""Ghép ảnh 2D thành lưới đánh số để xem nhanh (3x3 ảnh mỗi tờ): python luoi_anh.py ST3 <thư_mục_ra> [từ] [đến]"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ma, out = sys.argv[1], Path(sys.argv[2])
lo = int(sys.argv[3]) if len(sys.argv) > 3 else 1
hi = int(sys.argv[4]) if len(sys.argv) > 4 else 999
out.mkdir(parents=True, exist_ok=True)
src = sorted(Path("assets/anh_2d", ma).glob("*.jpg"))
src = [p for p in src if lo <= int(p.stem) <= hi]
try:
    f = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
except Exception:
    f = ImageFont.load_default()
tw, th = 640, 360
for s in range(0, len(src), 9):
    grp = src[s:s + 9]
    W = Image.new("RGB", (3 * tw + 8, 3 * th + 8), (20, 20, 20))
    d = ImageDraw.Draw(W)
    for i, p in enumerate(grp):
        im = Image.open(p).convert("RGB").resize((tw, th))
        x, y = (i % 3) * (tw + 4), (i // 3) * (th + 4)
        W.paste(im, (x, y))
        d.rectangle([x, y, x + 62, y + 32], fill=(0, 0, 0))
        d.text((x + 6, y + 2), p.stem, fill=(255, 220, 90), font=f)
    W.save(out / f"luoi_{grp[0].stem}-{grp[-1].stem}.jpg", quality=86)
print(len(src), "ảnh")
