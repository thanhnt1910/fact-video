# Tạo ảnh bìa Lý Công Uẩn (có logo kênh, logo cũ). Dùng: python assets/bia/LY1/tao_bia.py
# Nền: khung sạch (không phụ đề, không logo) của cảnh phục kích cửa Quảng Phúc, lưu ở assets/bia/LY1/nen_phuc_kich.jpg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='assets/fonts/'
BLK=F+'BeVietnamPro-BlackItalic.ttf'; EXB=F+'BeVietnamPro-ExtraBoldItalic.ttf'; LORA=F+'Lora-Variable.ttf'
WHITE=(255,250,235); YEL=(255,205,60); RED=(200,30,30)
logo=Image.open('assets/logo/nguoi-gac-su-cu.png').convert('RGBA')
NEN='assets/bia/LY1/nen_phuc_kich.jpg'          # cho bìa dọc
NEN_NGANG='assets/bia/LY1/nen_ngang.jpg'        # cho bìa ngang (hoàng tử lệch phải để chừa chỗ chữ)
def font(p,s): return ImageFont.truetype(p,s)
def fit(t,p,maxw,s):
    while font(p,s).getlength(t)>maxw: s-=2
    return font(p,s)
def shadow_text(im,xy,t,f,fill,off=6):
    d=ImageDraw.Draw(im); d.text((xy[0]+off,xy[1]+off),t,font=f,fill=(30,10,0)); d.text(xy,t,font=f,fill=fill)
def add_logo(im,size=130):
    # Giống logo video bản đồ: 130 px, độ đậm 0,8, góc trên phải, lề phải 44 px, cách mép trên 34 px
    l=logo.resize((size,size),Image.LANCZOS); l.putalpha(l.split()[3].point(lambda v:int(v*0.8)))
    im.alpha_composite(l,(im.size[0]-44-size,34))
def ngang(out):
    im=Image.open(NEN_NGANG).convert('RGB').resize((1920,1080),Image.LANCZOS).convert('RGBA')
    g=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(g)
    for x in range(820): d.line([(x,0),(x,1080)],fill=(12,8,20,int(245*(1-x/820)**1.0)))
    for y in range(300): d.line([(0,1080-y),(1920,1080-y)],fill=(10,6,12,int(190*(1-y/300))))
    im.alpha_composite(g)
    d=ImageDraw.Draw(im)
    d.polygon([(70,70),(600,62),(592,142),(62,150)],fill=RED)
    d.text((92,84),'ĐẠI CỒ VIỆT 1028',font=font(EXB,48),fill=WHITE)
    shadow_text(im,(66,200),'CỬA',font(BLK,140),WHITE)
    shadow_text(im,(66,375),'QUẢNG PHÚC',fit('QUẢNG PHÚC',BLK,660,140),YEL)
    shadow_text(im,(66,545),'ÂM MƯU',font(BLK,130),WHITE)
    d=ImageDraw.Draw(im)
    t='Vì sao Lý Công Uẩn dời đô?'
    d.text((72,830),t,font=fit(t,LORA,640,60),fill=WHITE)
    add_logo(im)
    d.line([(76,985),(156,985)],fill=YEL,width=4); d.text((176,958),'Người Gác Sử',font=font(LORA,44),fill=YEL)
    im.convert('RGB').save(out,quality=93)
def doc(out):
    src=Image.open(NEN).convert('RGB')
    bg=src.resize((3413,1920)).crop((1050,0,2130,1920)).filter(ImageFilter.GaussianBlur(26))
    im=bg.convert('RGBA'); im.alpha_composite(Image.new('RGBA',im.size,(12,8,20,150)))
    fg=src.resize((1080,608),Image.LANCZOS); im.alpha_composite(fg.convert('RGBA'),(0,860))
    d=ImageDraw.Draw(im)
    d.polygon([(70,170),(640,162),(632,242),(62,250)],fill=RED)
    d.text((92,182),'ĐẠI CỒ VIỆT 1028',font=font(EXB,50),fill=WHITE)
    shadow_text(im,(66,290),'CỬA',font(BLK,190),WHITE)
    shadow_text(im,(66,490),'QUẢNG PHÚC',fit('QUẢNG PHÚC',BLK,940,170),YEL)
    shadow_text(im,(66,680),'ÂM MƯU',font(BLK,150),WHITE)
    d=ImageDraw.Draw(im)
    d.text((72,1540),'Vì sao Lý Công Uẩn',font=font(LORA,66),fill=WHITE)
    d.text((72,1625),'dời đô?',font=font(LORA,66),fill=YEL)
    add_logo(im)
    d.line([(76,1800),(156,1800)],fill=YEL,width=4); d.text((176,1773),'Người Gác Sử',font=font(LORA,46),fill=YEL)
    im.convert('RGB').save(out,quality=93)
if __name__=='__main__':
    o='assets/bia/LY1/'
    ngang(o+'LY1_ngang.jpg'); doc(o+'LY1_doc.jpg')
