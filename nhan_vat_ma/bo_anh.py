import sys, io
sys.path.insert(0,'nhan_vat_ma')
import cairosvg
from PIL import Image
from puppet import *
def png(look,pose,face,bg="#f3e9d2"):
    svg=render_svg(look,pose,face,bg=bg)
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=600))).convert("RGB")
W,H=600,800
def sheet(name,look,cells):
    im=Image.new("RGB",(W*len(cells),H))
    for i,(p,f) in enumerate(cells): im.paste(png(look,p,FACES[f]),(i*W,0))
    im.save(f"/tmp/nv_{name}.png")
sheet("nobunaga",NOBUNAGA,[(pose_stand(),"giận"),(pose_point(),"tinh nghịch"),(pose_bow(),"bình thản"),(pose_banner(),"ngạc nhiên")])
sheet("hideyoshi",HIDEYOSHI,[(pose_stand(),"tinh nghịch"),(pose_point(),"ngạc nhiên"),(pose_bow(),"tinh nghịch"),(pose_cheer(),"tinh nghịch")])
sheet("ieyasu",IEYASU,[(pose_stand(),"buồn ngủ"),(pose_bowl(),"buồn ngủ"),(pose_bow(),"bình thản"),(pose_point(),"ngạc nhiên")])
sheet("ba_nguoi",NOBUNAGA,[])if False else None
tri=Image.new("RGB",(W*3,H))
for i,(lk,p,f) in enumerate(((NOBUNAGA,pose_stand(),"giận"),(HIDEYOSHI,pose_stand(),"tinh nghịch"),(IEYASU,pose_bowl(),"buồn ngủ"))): tri.paste(png(lk,p,FACES[f]),(i*W,0))
tri.save("/tmp/nv_ba.png")
