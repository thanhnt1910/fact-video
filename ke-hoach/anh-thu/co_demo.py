import sys,math
sys.path.insert(0,'/tmp/lh/phim_ban_do')
from PIL import Image,ImageDraw
import mapdraw as M
INK=(30,22,16,255)
def cloth(d,x,y,w,h,col,t,tail=0,band=True,seed=0,wind=1.0):
    """cờ vải: nhiều lát dọc lượn sóng, bóng sáng tối theo nếp, viền, tua; tail=1: đuôi nheo"""
    n=28;top=[];bot=[]
    for i in range(n+1):
        u=i/n;amp=h*0.10*u*wind
        dy=math.sin(t*5-u*7+seed)*amp
        dx=u*w*(1-0.06*math.sin(t*5-u*7+seed))
        top.append((x+dx,y+dy));bot.append((x+dx,y+h*(1-0.0)+dy*1.0))
    if tail:
        # đuôi nheo: cạnh dưới cuối bị khoét hình chữ V
        bot[-1]=(bot[-1][0]-w*0.0,bot[-1][1]);
        mid=((top[-1][0]+bot[-1][0])/2-w*0.22,(top[-1][1]+bot[-1][1])/2)
    # thân
    for i in range(n):
        u=i/n;sh=0.78+0.28*math.sin(t*5-u*7+seed+1.2)
        c=tuple(int(max(0,min(255,v*sh))) for v in col)+(255,)
        d.polygon([top[i],top[i+1],bot[i+1],bot[i]],fill=c)
    if band:
        for i in range(n):
            u=i/n;sh=0.8+0.25*math.sin(t*5-u*7+seed+1.2)
            for (a,b) in ((0.0,0.14),(0.86,1.0)):
                p=[(top[i][0],top[i][1]+h*a),(top[i+1][0],top[i+1][1]+h*a),(top[i+1][0],top[i+1][1]+h*b),(top[i][0],top[i][1]+h*b)]
                d.polygon(p,fill=(int(235*sh),int(200*sh),int(90*sh),255))
    if tail:
        e=top[-1];f=bot[-1]
        d.polygon([e,(e[0]-w*0.22,(e[1]+f[1])/2),f,(f[0]+w*0.0,f[1]),(e[0]+w*0.0,e[1])],fill=(238,228,200,255))  # mask by bg later
    d.line(top,fill=INK,width=3);d.line(bot,fill=INK,width=3)
    d.line([top[0],bot[0]],fill=INK,width=3);
    if not tail:d.line([top[-1],bot[-1]],fill=INK,width=3)
    # tua rua
    for k in range(9):
        q=k/8;px=top[-1][0]+0;py=top[-1][1]+(bot[-1][1]-top[-1][1])*q
        d.line([(px,py),(px+w*0.05,py+math.sin(t*9+k)*h*0.02)],fill=(235,200,90,255),width=3)
def pole(d,x,y,H,top=True):
    d.line([(x,y),(x,y-H)],fill=(86,58,34,255),width=10)
    d.ellipse((x-9,y-H-12,x+9,y-H+6),fill=(224,176,62,255),outline=INK,width=2)
    d.polygon([(x-5,y-H-10),(x,y-H-34),(x+5,y-H-10)],fill=(224,176,62,255),outline=INK)
def old_flag(d,x,y,s,col):
    M.flag(d,x,y,s,col)
def lenh(d,x,y,s,col,t):
    pole(d,x,y,s*3.4)
    cloth(d,x+5,y-s*3.2,s*1.9,s*1.25,col,t,band=True)
def phuong(d,x,y,s,col,t):  # cờ phướn dài thẳng đứng
    d.line([(x-s*0.9,y-s*4.0),(x+s*0.9,y-s*4.0)],fill=(86,58,34,255),width=8)
    d.line([(x,y),(x,y-s*4.0)],fill=(86,58,34,255),width=10)
    n=20
    for i in range(n):
        u=i/n;dx=math.sin(t*4-u*5)*s*0.12*u
        sh=0.8+0.25*math.sin(t*4-u*5+1)
        c=tuple(int(v*sh) for v in col)+(255,)
        y0=y-s*3.95+u*s*3.2;y1=y-s*3.95+(u+1/n)*s*3.2
        d.polygon([(x-s*0.55+dx,y0),(x+s*0.55+dx,y0),(x+s*0.55+dx,y1),(x-s*0.55+dx,y1)],fill=c)
    # đuôi răng cưa
    yb=y-s*0.75;dx=math.sin(t*4-5)*s*0.12
    for k in range(3):
        a=x-s*0.55+dx+k*s*0.37
        d.polygon([(a,yb),(a+s*0.37,yb),(a+s*0.185,yb+s*0.5)],fill=tuple(int(v*0.85) for v in col)+(255,),outline=INK)
    d.rectangle((x-s*0.55,y-s*3.95,x+s*0.55,y-s*3.95+s*3.2),outline=INK,width=3)
    for yy in (y-s*3.55,y-s*1.2):d.line([(x-s*0.55,yy),(x+s*0.55,yy)],fill=(235,200,90,255),width=6)
def long(d,x,y,s):  # lọng vàng
    d.line([(x,y),(x,y-s*3.4)],fill=(86,58,34,255),width=8)
    d.pieslice((x-s*1.8,y-s*4.6,x+s*1.8,y-s*2.0),180,360,fill=(226,176,56,255),outline=INK,width=3)
    for k in range(-4,5):
        xx=x+k*s*0.4;d.line([(xx,y-s*3.3),(xx,y-s*2.9)],fill=(180,52,42,255),width=5)
    for k in range(-5,6):
        xx=x+k*s*0.33;d.ellipse((xx-4,y-s*3.3-4,xx+4,y-s*3.3+4),fill=(180,52,42,255))
def dung(d,x,y,s,col,t):  # lính cầm cờ
    M.soldier(d,x,y,s,col,1,t*3)
    pole(d,x+s*0.7,y+s*0.3,s*3.0)
    cloth(d,x+s*0.7+4,y+s*0.3-s*2.9,s*1.3,s*0.85,col,t,band=False,wind=1.0)
def make(t,fn):
    W,H=1800,900;im=Image.new('RGBA',(W,H),(236,224,190,255));d=ImageDraw.Draw(im)
    f=M.font(34)
    def lab(x,s): d.text((x,830),s,font=f,fill=(40,30,20,255),anchor='mm')
    G=(52,142,86);R=(188,52,42)
    old_flag(d,150,720,100,G);lab(150,'Hiện tại')
    lenh(d,420,720,100,G,t);lab(420,'Cờ vải lượn sóng')
    phuong(d,720,720,100,R,t);lab(720,'Cờ phướn')
    long(d,1000,720,100);lab(1000,'Lọng vàng')
    dung(d,1330,720,70,G,t);dung(d,1480,720,70,G,t+0.5);dung(d,1630,720,70,G,t+1.0);lab(1480,'Quân cầm cờ')
    im.convert('RGB').save(fn)
make(0.35,'/tmp/ly/demo/co_demo.png')
