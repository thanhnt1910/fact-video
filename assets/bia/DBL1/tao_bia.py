# Ảnh bìa Đinh Bộ Lĩnh (có logo kênh, đặt giống video bản đồ). Dùng: python assets/bia/DBL1/tao_bia.py <khung_giay_4.jpg>
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='assets/fonts/'
BLK=F+'BeVietnamPro-BlackItalic.ttf'; EXB=F+'BeVietnamPro-ExtraBoldItalic.ttf'; LORA=F+'Lora-Variable.ttf'
WHITE=(255,250,235); YEL=(255,205,60); RED=(200,30,30)
logo=Image.open('assets/logo/nguoi-gac-su.png').convert('RGBA')
def font(p,s): return ImageFont.truetype(p,s)
def shadow_text(im,xy,t,f,fill,off=6):
    d=ImageDraw.Draw(im); d.text((xy[0]+off,xy[1]+off),t,font=f,fill=(40,15,0)); d.text(xy,t,font=f,fill=fill)
def add_logo(im,size=130):
    l=logo.resize((size,size),Image.LANCZOS); a=l.split()[3].point(lambda v:int(v*0.8)); l.putalpha(a)
    im.alpha_composite(l,(im.size[0]-44-size,34))
def fit(t,p,maxw,s):
    while font(p,s).getlength(t)>maxw: s-=2
    return font(p,s)
def ngang(src,out):
    fr=Image.open(src).convert('RGB').crop((150,168,1110,708)).resize((1920,1080),Image.LANCZOS)
    im=fr.convert('RGBA')
    g=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(g)
    for x in range(1000): d.line([(x,0),(x,1080)],fill=(20,12,5,int(240*(1-x/1000)**1.05)))
    g2=Image.new('RGBA',im.size,(0,0,0,0)); d2=ImageDraw.Draw(g2)
    for y in range(280): d2.line([(0,1080-y),(1920,1080-y)],fill=(15,10,5,int(210*(1-y/280))))
    im.alpha_composite(g2); im.alpha_composite(g)
    d=ImageDraw.Draw(im)
    d.polygon([(80,70),(560,62),(552,140),(72,146)],fill=RED)
    d.text((100,80),'ĐINH BỘ LĨNH',font=font(EXB,50),fill=WHITE)
    shadow_text(im,(75,210),'CON BỊ',font(BLK,170),WHITE,8)
    shadow_text(im,(75,410),'TREO',font(BLK,170),YEL,8)
    shadow_text(im,(75,610),'TRÊN SÀO',font(BLK,150),YEL,8)
    d=ImageDraw.Draw(im)
    t='Người cha chọn điều gì?'
    d.text((85,830),t,font=fit(t,LORA,820,56),fill=WHITE)
    add_logo(im)
    d.line([(85,985),(165,985)],fill=YEL,width=4); d.text((185,958),'Người Gác Sử',font=font(LORA,44),fill=YEL)
    im.convert('RGB').save(out,quality=93)
def doc(src,out):
    fr=Image.open(src).convert('RGB').crop((150,165,1110,765)).resize((1080,675),Image.LANCZOS)
    im=Image.new('RGBA',(1080,1920),(25,16,8,255))
    bg=Image.open(src).convert('RGB').resize((3413,1920)).crop((1000,0,2080,1920)).filter(ImageFilter.GaussianBlur(28))
    im.paste(bg.convert('RGBA'),(0,0)); im.alpha_composite(Image.new('RGBA',im.size,(15,10,5,150)))
    im.alpha_composite(fr.convert('RGBA'),(0,880))
    d=ImageDraw.Draw(im)
    d.polygon([(70,150),(520,142),(512,214),(62,220)],fill=RED)
    d.text((92,158),'ĐINH BỘ LĨNH',font=font(EXB,46),fill=WHITE)
    shadow_text(im,(70,250),'CON BỊ TREO',fit('CON BỊ TREO',BLK,940,170),WHITE,7)
    shadow_text(im,(70,450),'TRÊN SÀO',fit('TRÊN SÀO',BLK,940,190),YEL,7)
    d=ImageDraw.Draw(im)
    d.text((75,1625),'Người cha chọn',font=font(LORA,60),fill=WHITE); d.text((75,1705),'điều gì?',font=font(LORA,60),fill=YEL)
    add_logo(im); d.text((75,1815),'Người Gác Sử',font=font(LORA,44),fill=YEL)
    im.convert('RGB').save(out,quality=93)
if __name__=='__main__':
    s=sys.argv[1]; o='assets/bia/DBL1/'
    ngang(s,o+'DBL1_dai_thumbnail.jpg'); ngang(s,o+'DBL1_dai_thumbnail_fb.jpg'); doc(s,o+'DBL1_thumbnail_tiktok.jpg')
