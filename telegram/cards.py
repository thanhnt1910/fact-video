import sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'.')
import noi_dung as n
D='/usr/share/fonts/truetype/dejavu/'
def F(name,sz): return ImageFont.truetype(D+name,sz)
W,H=1280,720
BG=(20,24,32); GOLD=(217,180,91); RED=(196,84,72); TEAL=(74,163,160); INK=(236,232,222); DIM=(150,156,168)
def wrap(d,text,font,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
def card(k):
    c=n.CARD[k]
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,8],fill=GOLD); d.rectangle([0,H-8,W,H],fill=GOLD)
    d.text((60,36),f"TAM QUỐC THEO CHÍNH SỬ  ·  TẬP {k}",font=F('DejaVuSans-Bold.ttf',26),fill=GOLD)
    y=84
    for line in c['tieu_de']:
        d.text((60,y),line,font=F('DejaVuSerif-Bold.ttf',62),fill=INK); y+=76
    d.text((60,y+2),c['phu'],font=F('DejaVuSerif-Bold.ttf',34),fill=GOLD)
    top=326; colw=(W-60*2-40)//2
    for i,(lab,col,items,colr) in enumerate([("TIỂU THUYẾT KỂ",RED,c['tt'],RED),("CHÍNH SỬ CHÉP",TEAL,c['su'],TEAL)]):
        x=60+i*(colw+40)
        d.rounded_rectangle([x,top,x+colw,H-70],radius=14,fill=(30,36,48),outline=colr,width=2)
        d.rectangle([x,top,x+colw,top+46],fill=colr)
        d.text((x+22,top+8),lab,font=F('DejaVuSans-Bold.ttf',26),fill=(20,24,32))
        yy=top+66
        for it in items:
            lines=wrap(d,it,F('DejaVuSans.ttf',25),colw-70)
            d.ellipse([x+22,yy+10,x+32,yy+20],fill=colr)
            for ln in lines:
                d.text((x+46,yy),ln,font=F('DejaVuSans.ttf',25),fill=INK); yy+=33
            yy+=14
    d.text((60,H-52),"Người Gác Sử  ·  Tam quốc chí, Hậu Hán thư, Tư trị thông giám, chú của Bùi Tùng Chi",font=F('DejaVuSans.ttf',18),fill=DIM)
    im.save(f'./tap{k}.png')
for k in (1,2,3,4,5): card(k)
