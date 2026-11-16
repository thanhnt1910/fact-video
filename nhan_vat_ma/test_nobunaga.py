import sys, io, math
sys.path.insert(0, 'nhan_vat_ma')
import cairosvg
from PIL import Image, ImageDraw, ImageFont
from puppet import *

def png(look, pose, face, bg="#f3e9d2"):
    svg = render_svg(look, pose, face, bg=bg)
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=600))).convert("RGB")

poses = [("đứng", pose_stand()), ("đi", pose_walk(1.0)), ("chỉ tay", pose_point()),
         ("cúi chào", pose_bow()), ("cầm cờ", pose_banner())]
faces = ["giận", "ngạc nhiên", "tinh nghịch"]
W, H = 600, 800
sheet = Image.new("RGB", (W * 5, H * 1 + H * 0), "white")
for i, (n, p) in enumerate(poses):
    sheet.paste(png(NOBUNAGA, p, FACES[faces[i % 3]]), (i * W, 0))
sheet.save("/tmp/nb_poses.png")
row = Image.new("RGB", (W * 3, H))
for i, f in enumerate(faces):
    row.paste(png(NOBUNAGA, pose_stand(), FACES[f]), (i * W, 0))
row.save("/tmp/nb_faces.png")
# nhóm ba người
trio = Image.new("RGB", (W * 3, H))
for i, (lk, f) in enumerate(((NOBUNAGA, "giận"), (HIDEYOSHI, "tinh nghịch"), (IEYASU, "buồn ngủ"))):
    trio.paste(png(lk, pose_stand(), FACES[f]), (i * W, 0))
trio.save("/tmp/nb_trio.png")
