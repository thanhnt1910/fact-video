"""Ảnh bìa YouTube 1280x720 cho RN1 (Roanoke). Chạy: python assets/bia/RN1/tao_bia.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

R = Path(__file__).resolve().parents[3]
A = R / "assets" / "anh_en" / "RN1"
F = R / "assets" / "fonts" / "Anton-Regular.ttf"
W, H = 1280, 720

# nền: đầm cây bách tối, mờ nhẹ, ám đỏ nâu
bg = ImageOps.fit(Image.open(A / "S43.jpg").convert("RGB"), (W, H), Image.LANCZOS, centering=(0.5, 0.6))
bg = ImageEnhance.Brightness(bg).enhance(0.42)
bg = ImageEnhance.Contrast(bg).enhance(1.25).filter(ImageFilter.GaussianBlur(2))
bg = Image.blend(bg, Image.new("RGB", (W, H), (60, 20, 10)), 0.28)

# ảnh cây khắc "CRO" bên phải, khung đỏ
tree = Image.open(A / "S30.jpg").convert("RGB")
tw, th = 430, 640
tree = ImageOps.fit(tree, (tw, th), Image.LANCZOS, centering=(0.5, 0.42))
tree = ImageEnhance.Contrast(tree).enhance(1.15)
x0, y0 = 770, 40
frame = Image.new("RGB", (tw + 16, th + 16), (200, 30, 25))
bg.paste(frame, (x0 - 8, y0 - 8))
bg.paste(tree, (x0, y0))

# tối dần về bên trái để chữ nổi
g = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(g)
for x in range(W):
    d.line([(x, 0), (x, H)], fill=int(235 * max(0, 1 - x / 820) ** 1.2))
bg = Image.composite(Image.new("RGB", (W, H), (8, 6, 6)), bg, g)

im = bg.copy()
dr = ImageDraw.Draw(im)

def text(xy, s, size, fill, stroke=0):
    f = ImageFont.truetype(str(F), size)
    dr.text(xy, s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))

text((50, 40), "HISTORY MYSTERIES DAILY", 30, (230, 190, 90))
text((46, 120), "115 PEOPLE", 150, (255, 255, 255), 4)
text((46, 270), "VANISHED", 190, (235, 40, 30), 5)
text((50, 490), "AND LEFT ONE WORD:", 58, (255, 255, 255), 2)
text((50, 560), "CROATOAN", 112, (240, 200, 90), 4)
im.save(R / "assets" / "bia" / "RN1" / "RN1_thumbnail.jpg", quality=92)
print("ok")
