# Bìa v2 Lê Hoàn: hai chân dung đối mặt (Lê Hoàn và vua Tống), chữ lớn, có logo kênh. Chạy từ gốc repo: python assets/bia/LH6/tao_bia_v2.py <khung.jpg>
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
F='assets/fonts/'
BLK=F+'BeVietnamPro-BlackItalic.ttf'; EXB=F+'BeVietnamPro-ExtraBoldItalic.ttf'; LORA=F+'Lora-Variable.ttf'
WHITE=(255,250,235); YEL=(255,205,60); RED=(205,30,30)
logo=Image.open('assets/logo/nguoi-gac-su.png').convert('RGBA')
def font(p,s): return ImageFont.truetype(p,s)
def fit(t,p,maxw,s):
    while font(p,s).getlength(t)>maxw: s-=2
    return font(p,s)
def st(im,xy,t,f,fill,off=7):
    d=ImageDraw.Draw(im); d.text((xy[0]+off,xy[1]+off),t,font=f,fill=(30,8,0))
    d.text(xy,t,font=f,fill=fill,stroke_width=2,stroke_fill=(30,8,0))
def add_logo(im,size=130):
    l=logo.resize((size,size),Image.LANCZOS); a=l.split()[3].point(lambda v:int(v*0.8)); l.putalpha(a)
    im.alpha_composite(l,(im.size[0]-44-size,34))
def portrait(name,size,ring):
    p=Image.open(f'assets/icon_nhan_vat/{name}.jpg').convert('RGB')
    p=ImageEnhance.Contrast(p).enhance(1.12).resize((size,size),Image.LANCZOS).convert('RGBA')
    m=Image.new('L',(size*3,size*3),0); ImageDraw.Draw(m).ellipse((0,0,size*3-1,size*3-1),fill=255)
    p.putalpha(m.resize((size,size),Image.LANCZOS))
    pad=22; out=Image.new('RGBA',(size+2*pad,size+2*pad),(0,0,0,0)); d=ImageDraw.Draw(out)
    d.ellipse((0,0,size+2*pad-1,size+2*pad-1),fill=ring)
    d.ellipse((10,10,size+2*pad-11,size+2*pad-11),fill=(20,10,5,255))
    out.alpha_composite(p,(pad,pad)); return out
def glow(im,cx,cy,r,col):
    g=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(g).ellipse((cx-r,cy-r,cx+r,cy+r),fill=col)
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(r//3)))
def ngang(src,out):
    bg=Image.open(src).convert('RGB').crop((500,170,1460,710)).resize((1920,1080),Image.LANCZOS).filter(ImageFilter.GaussianBlur(9))
    bg=ImageEnhance.Brightness(bg).enhance(0.45); im=bg.convert('RGBA')
    im.alpha_composite(Image.new('RGBA',im.size,(110,12,12,95)))
    glow(im,1330,600,520,(255,170,40,120))
    d=ImageDraw.Draw(im)
    d.polygon([(80,70),(600,62),(592,140),(72,146)],fill=RED)
    d.text((100,80),'LÊ HOÀN 980–990',font=font(EXB,50),fill=WHITE)
    st(im,(70,190),'4 LẦN',fit('4 LẦN',BLK,800,250),YEL,9)
    st(im,(75,470),'LỪA',font(BLK,190),WHITE,8)
    st(im,(75,660),'VUA TỐNG',fit('VUA TỐNG',BLK,770,170),WHITE,8)
    d=ImageDraw.Draw(im)
    d.text((85,880),'Không cần thắng trận nào?',font=fit('Không cần thắng trận nào?',LORA,780,52),fill=WHITE)
    d.line([(85,1000),(165,1000)],fill=YEL,width=4); d.text((185,973),'Người Gác Sử',font=font(LORA,44),fill=YEL)
    lh=portrait('lehoan',500,(255,205,60,255)); vt=portrait('vuatong',500,(205,30,30,255))
    im.alpha_composite(lh,(880,300)); im.alpha_composite(vt,(1360,300))
    d=ImageDraw.Draw(im); cx,cy=1370,820
    d.ellipse((cx-62,cy-62,cx+62,cy+62),fill=RED,outline=WHITE,width=6)
    f=font(BLK,64); w=f.getlength('VS'); d.text((cx-w/2,cy-48),'VS',font=f,fill=WHITE)
    add_logo(im); im.convert('RGB').save(out,quality=93)
def doc(src,out):
    bg=Image.open(src).convert('RGB').resize((3413,1920)).crop((1100,0,2180,1920)).filter(ImageFilter.GaussianBlur(20))
    bg=ImageEnhance.Brightness(bg).enhance(0.45); im=bg.convert('RGBA')
    im.alpha_composite(Image.new('RGBA',im.size,(110,12,12,95))); glow(im,540,1100,560,(255,170,40,110))
    d=ImageDraw.Draw(im)
    d.polygon([(70,190),(600,182),(592,262),(62,268)],fill=RED); d.text((92,200),'LÊ HOÀN 980–990',font=font(EXB,50),fill=WHITE)
    st(im,(65,300),'4 LẦN',fit('4 LẦN',BLK,940,300),YEL,10)
    st(im,(70,620),'LỪA VUA TỐNG',fit('LỪA VUA TỐNG',BLK,940,150),WHITE,8)
    lh=portrait('lehoan',420,(255,205,60,255)); vt=portrait('vuatong',420,(205,30,30,255))
    im.alpha_composite(lh,(60,860)); im.alpha_composite(vt,(560,860))
    d=ImageDraw.Draw(im); cx,cy=540,1200
    d.ellipse((cx-55,cy-55,cx+55,cy+55),fill=RED,outline=WHITE,width=6)
    f=font(BLK,56); w=f.getlength('VS'); d.text((cx-w/2,cy-42),'VS',font=f,fill=WHITE)
    d.text((75,1470),'Không cần thắng',font=font(LORA,64),fill=WHITE); d.text((75,1550),'trận nào?',font=font(LORA,64),fill=YEL)
    add_logo(im); d.text((75,1810),'Người Gác Sử',font=font(LORA,44),fill=YEL)
    im.convert('RGB').save(out,quality=93)
if __name__=='__main__':
    s=sys.argv[1]; o='assets/bia/LH6/'
    ngang(s,o+'LH6_v2_dai.jpg'); doc(s,o+'LH6_v2_tiktok.jpg')
