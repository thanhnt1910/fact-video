# Ảnh bìa Chu Du (có logo kênh, đặt giống video bản đồ). Dùng: python assets/bia/CD1/tao_bia.py [khung.png]
import sys
sys.path.insert(0,'assets/bia/NQ1')
from PIL import Image, ImageDraw, ImageFilter
import tao_bia as B
src=sys.argv[1] if len(sys.argv)>1 else 'assets/bia/CD1/khung.png'
W,Y,R=B.WHITE,B.YEL,B.RED; font=B.font
def crop(src):
    return Image.open(src).convert('RGB').crop((260,330,1220,870))   # bỏ phụ đề đáy, Chu Du lệch phải
def ngang(out):
    im=crop(src).resize((1920,1080),Image.LANCZOS).convert('RGBA')
    g=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(g)
    for x in range(1050): d.line([(x,0),(x,1080)],fill=(20,12,5,int(235*(1-x/1050)**1.1)))
    g2=Image.new('RGBA',im.size,(0,0,0,0)); d2=ImageDraw.Draw(g2)
    for y in range(260): d2.line([(0,1080-y),(1920,1080-y)],fill=(15,10,5,int(200*(1-y/260))))
    im.alpha_composite(g2); im.alpha_composite(g)
    d=ImageDraw.Draw(im)
    d.polygon([(80,70),(470,62),(462,140),(72,146)],fill=R); d.text((100,80),'XÍCH BÍCH 208',font=font(B.EXB,50),fill=W)
    B.shadow_text(im,(75,220),'CHẾT',font(B.BLK,190),W,7)
    B.shadow_text(im,(75,430),'VÌ TỨC?',font(B.BLK,190),Y,7)
    d=ImageDraw.Draw(im)
    t='Chu Du có thật sự bị Gia Cát Lượng chọc tức?'
    d.text((85,760),'Chu Du có thật sự bị',font=font(B.LORA,56),fill=W)
    d.text((85,830),'Gia Cát Lượng chọc tức?',font=font(B.LORA,56),fill=W)
    B.add_logo(im)
    d.line([(85,990),(165,990)],fill=Y,width=4); d.text((185,963),'Người Gác Sử',font=font(B.LORA,44),fill=Y)
    im.convert('RGB').save(out,quality=93); return im.convert('RGB')
def fb(im,out):
    im.crop((0,45,1920,1080-45+0)).resize((1200,int(1200*990/1920)),Image.LANCZOS).crop((0,0,1200,630)).save(out,quality=92) if False else im.resize((1200,675),Image.LANCZOS).crop((0,22,1200,652)).save(out,quality=92)
def doc(out):
    fr=crop(src).resize((1080,608),Image.LANCZOS)
    im=Image.new('RGBA',(1080,1920),(25,16,8,255))
    bg=Image.open(src).convert('RGB').resize((3413,1920)).crop((1100,0,2180,1920)).filter(ImageFilter.GaussianBlur(28))
    im.paste(bg.convert('RGBA'),(0,0)); im.alpha_composite(Image.new('RGBA',im.size,(15,10,5,150)))
    im.alpha_composite(fr.convert('RGBA'),(0,880))
    d=ImageDraw.Draw(im)
    d.polygon([(70,150),(470,142),(462,214),(62,220)],fill=R); d.text((92,158),'XÍCH BÍCH 208',font=font(B.EXB,46),fill=W)
    B.shadow_text(im,(70,250),'CHẾT',font(B.BLK,220),W,7)
    B.shadow_text(im,(70,480),'VÌ TỨC?',font(B.BLK,200),Y,7)
    d=ImageDraw.Draw(im)
    d.text((75,1625),'Chu Du có thật sự bị',font=font(B.LORA,56),fill=W)
    d.text((75,1700),'Gia Cát Lượng chọc tức?',font=font(B.LORA,56),fill=Y)
    B.add_logo(im); d.text((75,1810),'Người Gác Sử',font=font(B.LORA,44),fill=Y)
    im.convert('RGB').save(out,quality=93)
if __name__=='__main__':
    im=ngang('assets/bia/CD1/CD1_dai_thumbnail.jpg'); fb(im,'assets/bia/CD1/CD1_dai_thumbnail_fb.jpg'); doc('assets/bia/CD1/CD1_thumbnail_tiktok.jpg')
