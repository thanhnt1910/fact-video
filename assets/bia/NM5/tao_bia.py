# Bìa nm5 "3 lần đánh quân Nguyên Mông". Dùng: python assets/bia/NM5/tao_bia.py <khung.jpg> (khung: giây 3 của video, cảnh kho lương)
import sys
sys.path.insert(0,'assets/bia/NQ1')
from tao_bia import *
def ngang(src,out):
    im=Image.open(src).convert('RGB').crop((0,60,1280,780)).resize((1920,1080),Image.LANCZOS).convert('RGBA')
    g=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(g)
    for x in range(1000): d.line([(x,0),(x,1080)],fill=(20,12,5,int(235*(1-x/1000)**1.1)))
    im.alpha_composite(g)
    d=ImageDraw.Draw(im)
    d.polygon([(80,70),(640,62),(632,140),(72,146)],fill=RED)
    d.text((100,80),'NGUYÊN MÔNG 1258–1288',font=font(EXB,46),fill=WHITE)
    shadow_text(im,(75,200),'KHO',font(BLK,170),WHITE,7)
    shadow_text(im,(75,400),'TRỐNG',font(BLK,170),YEL,7)
    d=ImageDraw.Draw(im)
    t,t2='Vì sao ba lần chiếm Thăng Long','mà không giữ nổi?'
    d.text((85,760),t,font=fit(t,LORA,800,50),fill=WHITE); d.text((85,830),t2,font=font(LORA,50),fill=YEL)
    add_logo(im)
    d.line([(85,990),(165,990)],fill=YEL,width=4); d.text((185,963),'Người Gác Sử',font=font(LORA,44),fill=YEL)
    im.convert('RGB').save(out,quality=93)
def doc(src,out):
    fr=Image.open(src).convert('RGB').crop((420,110,1500,800)).resize((1080,690),Image.LANCZOS)
    im=Image.new('RGBA',(1080,1920),(25,16,8,255))
    bg=Image.open(src).convert('RGB').resize((3413,1920)).crop((1000,0,2080,1920)).filter(ImageFilter.GaussianBlur(28))
    im.paste(bg.convert('RGBA'),(0,0)); im.alpha_composite(Image.new('RGBA',im.size,(15,10,5,150)))
    im.alpha_composite(fr.convert('RGBA'),(0,860))
    d=ImageDraw.Draw(im)
    d.polygon([(70,150),(700,142),(692,214),(62,220)],fill=RED)
    d.text((92,158),'NGUYÊN MÔNG 1258–1288',font=font(EXB,44),fill=WHITE)
    shadow_text(im,(70,250),'KHO',font(BLK,230),WHITE,7)
    shadow_text(im,(70,500),'TRỐNG',font(BLK,230),YEL,7)
    d=ImageDraw.Draw(im)
    d.text((75,1590),'Vì sao ba lần chiếm',font=font(LORA,56),fill=WHITE)
    d.text((75,1660),'Thăng Long mà không giữ nổi?',font=fit('Thăng Long mà không giữ nổi?',LORA,930,56),fill=YEL)
    add_logo(im); d.text((75,1810),'Người Gác Sử',font=font(LORA,44),fill=YEL)
    im.convert('RGB').save(out,quality=93)
if __name__=='__main__':
    s=sys.argv[1]; o='assets/bia/NM5/'
    ngang(s,o+'NM5_dai_thumbnail.jpg'); ngang(s,o+'NM5_dai_thumbnail_fb.jpg'); doc(s,o+'NM5_thumbnail_tiktok.jpg')
