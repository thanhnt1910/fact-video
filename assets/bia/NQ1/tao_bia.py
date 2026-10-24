# Tạo ảnh bìa Ngô Quyền (có logo kênh). Dùng: python assets/bia/NQ1/tao_bia.py <khung.jpg>
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='assets/fonts/'
BLK=F+'BeVietnamPro-BlackItalic.ttf'; EXB=F+'BeVietnamPro-ExtraBoldItalic.ttf'; LORA=F+'Lora-Variable.ttf'
WHITE=(255,250,235); YEL=(255,205,60); RED=(200,30,30)
logo=Image.open('assets/logo/nguoi-gac-su.png').convert('RGBA')
def font(p,s): return ImageFont.truetype(p,s)
def shadow_text(im,xy,t,f,fill,off=5):
    d=ImageDraw.Draw(im); d.text((xy[0]+off,xy[1]+off),t,font=f,fill=(40,15,0)); d.text(xy,t,font=f,fill=fill)
def add_logo(im,size=130,xy=None):
    # Giống logo video bản đồ (mapfilm3.py): 130 px, độ đậm 0,8, góc trên phải, lề phải 44 px, cách mép trên 34 px
    l=logo.resize((size,size),Image.LANCZOS)
    a=l.split()[3].point(lambda v:int(v*0.8)); l.putalpha(a)
    im.alpha_composite(l,(im.size[0]-44-size,34))
def fit(t,p,maxw,s):
    while font(p,s).getlength(t)>maxw: s-=2
    return font(p,s)
def ngang(src,out,logo_sz=210):
    fr=Image.open(src).convert('RGB').crop((500,170,1460,710)).resize((1920,1080),Image.LANCZOS)
    # che chữ phụ đề đáy và hộp góc bằng lớp tối
    im=fr.convert('RGBA')
    g=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(g)
    for x in range(950):
        d.line([(x,0),(x,1080)],fill=(20,12,5,int(235*(1-x/950)**1.1)))
    g2=Image.new('RGBA',im.size,(0,0,0,0)); d2=ImageDraw.Draw(g2)
    for y in range(260):
        d2.line([(0,1080-y),(1920,1080-y)],fill=(15,10,5,int(200*(1-y/260))))
    im.alpha_composite(g2)
    im.alpha_composite(g)
    d=ImageDraw.Draw(im)
    d.polygon([(80,70),(560,62),(552,140),(72,146)],fill=RED)
    d.text((100,80),'BẠCH ĐẰNG 938',font=font(EXB,50),fill=WHITE)
    shadow_text(im,(75,200),'CỌC GỖ',font(BLK,150),WHITE,7)
    shadow_text(im,(75,380),'CHẶN',font(BLK,150),YEL,7)
    shadow_text(im,(75,560),'HẠM ĐỘI',font(BLK,130),YEL,7)
    d=ImageDraw.Draw(im)
    f=font(LORA,52); d.text((85,800),'Ngô Quyền dùng thủy triều thế nào?',font=fit('Ngô Quyền dùng thủy triều thế nào?',LORA,780,52),fill=WHITE)
    add_logo(im)
    d.line([(85,990),(165,990)],fill=YEL,width=4); d.text((185,963),'Người Gác Sử',font=font(LORA,44),fill=YEL)
    im.convert('RGB').save(out,quality=93)
def doc(src,out):
    fr=Image.open(src).convert('RGB').crop((500,170,1460,710))  # 960x540
    fr=fr.resize((1080,608),Image.LANCZOS)
    im=Image.new('RGBA',(1080,1920),(25,16,8,255))
    bg=Image.open(src).convert('RGB').resize((3413,1920)).crop((1100,0,2180,1920)).filter(ImageFilter.GaussianBlur(28))
    im.paste(bg.convert('RGBA'),(0,0)); dk=Image.new('RGBA',im.size,(15,10,5,150)); im.alpha_composite(dk)
    im.alpha_composite(fr.convert('RGBA'),(0,880))
    d=ImageDraw.Draw(im)
    d.polygon([(70,150),(520,142),(512,214),(62,220)],fill=RED)
    d.text((92,158),'BẠCH ĐẰNG 938',font=font(EXB,46),fill=WHITE)
    shadow_text(im,(70,250),'CỌC GỖ',font(BLK,190),WHITE,7)
    shadow_text(im,(70,440),'CHẶN HẠM ĐỘI',fit('CHẶN HẠM ĐỘI',BLK,940,150),YEL,7)
    d=ImageDraw.Draw(im)
    d.text((75,1625),'Ngô Quyền dùng thủy triều',font=font(LORA,56),fill=WHITE)
    d.text((75,1700),'thế nào?',font=font(LORA,56),fill=YEL)
    add_logo(im)
    d.text((75,1810),'Người Gác Sử',font=font(LORA,44),fill=YEL)
    im.convert('RGB').save(out,quality=93)
if __name__=='__main__':
    s=sys.argv[1]; o='assets/bia/NQ1/'
    ngang(s,o+'NQ1_dai_thumbnail.jpg'); ngang(s,o+'NQ1_dai_thumbnail_fb.jpg')
    doc(s,o+'NQ1_thumbnail_tiktok.jpg')
