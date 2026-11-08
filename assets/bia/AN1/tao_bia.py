"""Ảnh bìa YouTube 1280x720 cho AN1 (Andrée). Chạy: python assets/bia/AN1/tao_bia.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

R = Path(__file__).resolve().parents[3]
A = R / "assets" / "anh_en" / "AN1"
F = R / "assets" / "fonts" / "Anton-Regular.ttf"
W, H = 1280, 720

# nền: trại trên băng (S57), tối, ám xanh lạnh
bg = ImageOps.fit(Image.open(A / "S57.jpg").convert("L").convert("RGB"), (W, H), Image.LANCZOS, centering=(0.5, 0.5))
bg = ImageEnhance.Brightness(bg).enhance(0.45)
bg = ImageEnhance.Contrast(bg).enhance(1.2).filter(ImageFilter.GaussianBlur(3))
bg = Image.blend(bg, Image.new("RGB", (W, H), (10, 30, 55)), 0.35)

# ảnh khí cầu Örnen nằm trên băng bên phải, khung vàng
ph = Image.open(A / "S30.jpg").convert("L").convert("RGB")
tw, th = 560, 620
ph = ImageOps.fit(ph, (tw, th), Image.LANCZOS, centering=(0.45, 0.5))
ph = ImageEnhance.Contrast(ph).enhance(1.15)
x0, y0 = 690, 50
bg.paste(Image.new("RGB", (tw + 16, th + 16), (230, 190, 90)), (x0 - 8, y0 - 8))
bg.paste(ph, (x0, y0))

# tối dần về bên trái để chữ nổi
g = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(g)
for x in range(W):
    d.line([(x, 0), (x, H)], fill=int(235 * max(0, 1 - x / 760) ** 1.2))
im = Image.composite(Image.new("RGB", (W, H), (5, 8, 14)), bg, g)
dr = ImageDraw.Draw(im)


def text(xy, s, size, fill, stroke=0):
    dr.text(xy, s, font=ImageFont.truetype(str(F), size), fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))


logo = Image.open(R / "assets" / "logo" / "history-mysteries-daily.png").convert("RGBA").resize((96, 96), Image.LANCZOS)
im.paste(logo, (46, 28), logo)
text((156, 52), "HISTORY MYSTERIES DAILY", 30, (230, 190, 90))
text((46, 120), "FOUND", 170, (255, 255, 255), 4)
text((46, 290), "33 YEARS", 135, (235, 40, 30), 5)
text((50, 445), "LATER", 135, (255, 255, 255), 4)
text((52, 625), "1897 · NORTH POLE BALLOON", 40, (240, 200, 90), 2)
im.save(R / "assets" / "bia" / "AN1" / "AN1_thumbnail.jpg", quality=92)
print("ok")
