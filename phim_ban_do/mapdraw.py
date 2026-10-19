import math,random,json,numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from build2 import font,W,H,FPS
def shade(c,k): return tuple(int(max(0,min(255,x*k))) for x in c)
# ---------------- vẽ biểu tượng (trên canvas 2x)
def soldier(d,x,y,s,col,face,bob,alpha=255):
    y-=abs(math.sin(bob))*s*0.18
    ink=(30,22,16,alpha);skin=(232,196,150,alpha);c=col+(alpha,)
    d.line([(x+face*s*0.55,y-s*1.7),(x+face*s*0.55,y+s*0.45)],fill=(110,80,50,alpha),width=max(2,int(s*0.12)))
    d.polygon([(x+face*s*0.55,y-s*2.0),(x+face*s*0.4,y-s*1.65),(x+face*s*0.7,y-s*1.65)],fill=(200,205,210,alpha))
    d.polygon([(x-s*0.5,y+s*0.55),(x+s*0.5,y+s*0.55),(x+s*0.38,y-s*0.5),(x-s*0.38,y-s*0.5)],fill=c,outline=ink)
    d.ellipse((x-s*0.28,y-s*1.05,x+s*0.28,y-s*0.5),fill=skin,outline=ink)
    d.pieslice((x-s*0.34,y-s*1.25,x+s*0.34,y-s*0.55),180,360,fill=(70,70,78,alpha),outline=ink)
    d.ellipse((x-face*s*0.55-s*0.28,y-s*0.2,x-face*s*0.55+s*0.28,y+s*0.36),fill=shade(col,0.7)+(alpha,),outline=ink)
def horse(d,x,y,s,col,face,bob,alpha=255):
    y-=abs(math.sin(bob))*s*0.3;ink=(30,22,16,alpha);hc=(116,78,48,alpha)
    gal=math.sin(bob*1.0)
    for lx,ph in((-0.7,0),(-0.35,1.6),(0.35,3.1),(0.7,4.6)):
        a=math.sin(bob*1.0+ph)*0.5
        d.line([(x+face*lx*s*1.2,y+s*0.45),(x+face*(lx+a*0.5)*s*1.2,y+s*1.25)],fill=ink,width=max(2,int(s*0.14)))
    d.ellipse((x-s*1.1,y-s*0.3,x+s*1.1,y+s*0.65),fill=hc,outline=ink)
    d.polygon([(x+face*s*0.8,y-s*0.2),(x+face*s*1.35,y-s*0.9),(x+face*s*1.65,y-s*0.7),(x+face*s*1.05,y+s*0.1)],fill=hc,outline=ink)
    d.line([(x-face*s*1.1,y),(x-face*s*1.6,y+s*0.5+gal*s*0.1)],fill=ink,width=max(2,int(s*0.16)))
    d.polygon([(x-s*0.35,y-s*0.3),(x+s*0.35,y-s*0.3),(x+s*0.28,y-s*1.0),(x-s*0.28,y-s*1.0)],fill=col+(alpha,),outline=ink)
    d.ellipse((x-s*0.24,y-s*1.5,x+s*0.24,y-s*0.95),fill=(232,196,150,alpha),outline=ink)
    d.pieslice((x-s*0.3,y-s*1.65,x+s*0.3,y-s*1.0),180,360,fill=(70,70,78,alpha),outline=ink)
    d.line([(x+face*s*0.4,y-s*2.1),(x+face*s*0.4,y-s*0.3)],fill=(110,80,50,alpha),width=max(2,int(s*0.1)))
def flag(d,x,y,s,col,txt=None,fn=None):
    d.line([(x,y),(x,y-s*3.2)],fill=(70,50,30,255),width=max(3,int(s*0.18)))
    d.polygon([(x,y-s*3.2),(x+s*1.9,y-s*2.85),(x+s*1.6,y-s*2.35),(x+s*1.9,y-s*1.9),(x,y-s*2.2)],fill=col+(255,),outline=(25,18,12,255))
def city_icon(d,x,y,s,gold=False,owner=None,open_=0):
    ink=(40,28,18,255);wall=(188,170,140,255)
    d.rectangle((x-s*1.2,y-s*0.6,x+s*1.2,y+s*0.9),fill=wall,outline=ink,width=max(2,int(s*0.1)))
    for i in range(5):
        cx=x-s*1.2+i*s*0.6
        d.rectangle((cx,y-s*0.9,cx+s*0.36,y-s*0.6),fill=wall,outline=ink)
    d.polygon([(x-s*0.8,y-s*0.9),(x,y-s*1.8),(x+s*0.8,y-s*0.9)],fill=(120,70,50,255),outline=ink)
    gw=s*0.38;ghh=s*0.6
    d.rectangle((x-gw,y+s*0.9-ghh,x+gw,y+s*0.9),fill=(40,28,20,255) if not open_ else (210,160,60,255),outline=ink)
    if open_:
        d.polygon([(x-gw,y+s*0.9-ghh),(x-gw-s*0.4,y+s*0.8),(x-gw,y+s*0.9)],fill=(100,70,40,255),outline=ink)
        d.polygon([(x+gw,y+s*0.9-ghh),(x+gw+s*0.4,y+s*0.8),(x+gw,y+s*0.9)],fill=(100,70,40,255),outline=ink)
def fire(d,x,y,s,t,seed):
    r=random.Random(seed)
    for i in range(9):
        ph=t*7+r.uniform(0,6);fx=x+r.uniform(-1,1)*s*0.7;h=s*(1.2+0.6*math.sin(ph))
        w=s*0.5
        d.polygon([(fx-w,y),(fx-w*0.3,y-h*0.7),(fx,y-h),(fx+w*0.4,y-h*0.6),(fx+w,y)],fill=(240,110,30,200))
        d.polygon([(fx-w*0.5,y),(fx,y-h*0.7),(fx+w*0.5,y)],fill=(255,205,70,230))
    for i in range(5):
        u=((t*0.8+i*0.2)%1);d.ellipse((x-s*0.4+i*s*0.2,y-s*2-u*s*3,x+s*0.4+i*s*0.2,y-s*1.4-u*s*3),fill=(60,55,55,int(110*(1-u))))
def scroll(d,x,y,s):
    d.rectangle((x-s,y-s*0.6,x+s,y+s*0.6),fill=(240,228,196,255),outline=(70,50,30,255),width=max(2,int(s*0.15)))
    d.line([(x-s*0.6,y-s*0.2),(x+s*0.6,y-s*0.2)],fill=(110,90,60,255),width=max(1,int(s*0.1)))
    d.line([(x-s*0.6,y+s*0.15),(x+s*0.3,y+s*0.15)],fill=(110,90,60,255),width=max(1,int(s*0.1)))
    d.ellipse((x+s*0.6,y-s*0.3,x+s*1.2,y+s*0.3),fill=(176,48,40,255))
def tag(d,x,y,txt,col,size,fn=None):
    f=fn or font(size);b=d.textbbox((0,0),txt,font=f);w=b[2]-b[0];h=b[3]-b[1];p=size*0.28
    d.rounded_rectangle((x-w/2-p,y,x+w/2+p,y+h+p*1.6),size*0.25,fill=(246,238,214,235),outline=col+(255,),width=max(2,int(size*0.09)))
    d.text((x-w/2,y+p*0.3-b[1]*0+0),txt,font=f,fill=col+(255,))

def emblem(d,x,y,r,kind,col):
    ink=(30,22,16,255);d.ellipse((x-r,y-r,x+r,y+r),fill=col+(255,),outline=ink,width=max(2,int(r*0.14)))
    w=(250,244,226,255)
    if kind=='sun':
        d.ellipse((x-r*0.38,y-r*0.38,x+r*0.38,y+r*0.38),fill=w)
        for k in range(8):
            a=k*math.pi/4;d.line([(x+math.cos(a)*r*0.55,y+math.sin(a)*r*0.55),(x+math.cos(a)*r*0.8,y+math.sin(a)*r*0.8)],fill=w,width=max(2,int(r*0.12)))
    elif kind=='dia': d.polygon([(x,y-r*0.7),(x+r*0.55,y),(x,y+r*0.7),(x-r*0.55,y)],fill=w)
    elif kind=='tri': d.polygon([(x,y-r*0.7),(x+r*0.65,y+r*0.5),(x-r*0.65,y+r*0.5)],fill=w)
    elif kind=='moon':
        d.ellipse((x-r*0.6,y-r*0.6,x+r*0.6,y+r*0.6),fill=w);d.ellipse((x-r*0.25,y-r*0.7,x+r*0.9,y+r*0.5),fill=col+(255,))
    else: d.rectangle((x-r*0.5,y-r*0.5,x+r*0.5,y+r*0.5),fill=w)
def skull(d,x,y,r):
    ink=(25,18,14,255);w=(246,240,226,255)
    d.ellipse((x-r*0.62,y-r*0.7,x+r*0.62,y+r*0.35),fill=w,outline=ink,width=max(2,int(r*0.09)))
    d.rectangle((x-r*0.34,y+r*0.15,x+r*0.34,y+r*0.62),fill=w,outline=ink,width=max(2,int(r*0.09)))
    for sx in(-1,1): d.ellipse((x+sx*r*0.32-r*0.2,y-r*0.3,x+sx*r*0.32+r*0.2,y+r*0.1),fill=ink)
    d.polygon([(x,y+r*0.02),(x-r*0.1,y+r*0.2),(x+r*0.1,y+r*0.2)],fill=ink)
    for k in(-0.17,0,0.17): d.line([(x+k*r*1.0,y+r*0.4),(x+k*r*1.0,y+r*0.62)],fill=ink,width=max(1,int(r*0.06)))
def whiteflag(d,x,y,r):
    ink=(25,18,14,255)
    d.line([(x-r*0.45,y+r*0.8),(x-r*0.45,y-r*0.85)],fill=(90,66,40,255),width=max(3,int(r*0.14)))
    d.polygon([(x-r*0.45,y-r*0.85),(x+r*0.75,y-r*0.6),(x+r*0.5,y-r*0.3),(x+r*0.75,y),(x-r*0.45,y-r*0.15)],fill=(250,248,240,255),outline=ink)
def badge(d,x,y,r,kind,u):
    r=r*(0.4+0.6*min(1,u*1.0))*(1+0.18*math.sin(min(1,u)*math.pi))
    d.ellipse((x-r,y-r,x+r,y+r),fill=(120,30,26,255) if kind=='skull' else (70,70,78,255),outline=(246,238,214,255),width=max(3,int(r*0.12)))
    (skull if kind=='skull' else whiteflag)(d,x,y,r*0.8)
def tag2(d,x,y,g,col,size,fr,defeated,tt):
    f=font(size);txt=g.name;b=d.textbbox((0,0),txt,font=f);w=b[2]-b[0];h=b[3]-b[1];p=size*0.28
    er=size*0.62;tw=w+er*2+p*2.4;x0=x-tw/2
    cc=(120,120,126) if defeated else col
    d.rounded_rectangle((x0,y,x0+tw,y+h+p*1.6+size*0.3),size*0.25,fill=(246,238,214,235) if not defeated else (222,218,208,235),outline=cc+(255,),width=max(2,int(size*0.09)))
    emblem(d,x0+p+er,y+(h+p*1.6)/2,er,g.emb,cc)
    d.text((x0+p*1.6+er*2,y+p*0.3),txt,font=f,fill=cc+(255,))
    by=y+h+p*1.6+size*0.05;bx0=x0+p;bx1=x0+tw-p
    d.rectangle((bx0,by,bx1,by+size*0.16),fill=(190,180,160,255))
    d.rectangle((bx0,by,bx0+(bx1-bx0)*fr,by+size*0.16),fill=(200,60,50,255) if fr<0.5 else cc+(255,))
    return tw
# ---------------- khung hình
FONTCACHE={}
def F(sz):
    k=int(sz)
    if k not in FONTCACHE: FONTCACHE[k]=font(k)
    return FONTCACHE[k]
def deco(d,v,K,z,ik,DECO):
    if z<2.0: return
    n=0
    for lo,la,k,r in DECO:
        if k=='none': continue
        x,y=v.sc(lo,la,K)
        if not(0<x<W*K and 0<y<H*K): continue
        s=ik*(0.55+0.4*r)
        if k=='tree':
            d.line([(x,y),(x,y+s*0.5)],fill=(80,56,34,200),width=max(2,int(s*0.12)))
            d.polygon([(x,y-s*1.1),(x+s*0.55,y+s*0.1),(x-s*0.55,y+s*0.1)],fill=(92,128,70,210),outline=(40,70,40,220))
            d.polygon([(x,y-s*0.5),(x+s*0.7,y+s*0.45),(x-s*0.7,y+s*0.45)],fill=(104,142,78,215),outline=(40,70,40,220))
        else:
            d.arc((x-s*0.9,y-s*0.3,x,y+s*0.5),200,340,fill=(250,250,245,170),width=max(2,int(s*0.1)))
            d.arc((x,y-s*0.3,x+s*0.9,y+s*0.5),200,340,fill=(250,250,245,170),width=max(2,int(s*0.1)))
def compass(d,x,y,r):
    ink=(60,44,28,255);cr=(246,238,214,255)
    d.ellipse((x-r*1.15,y-r*1.15,x+r*1.15,y+r*1.15),fill=(246,238,214,170),outline=ink,width=3)
    for k,(dx,dy) in enumerate(((0,-1),(1,0),(0,1),(-1,0))):
        px,py=-dy,dx
        d.polygon([(x+dx*r,y+dy*r),(x+px*r*0.22,y+py*r*0.22),(x,y),],fill=ink if k==0 else (150,120,80,255))
        d.polygon([(x+dx*r,y+dy*r),(x-px*r*0.22,y-py*r*0.22),(x,y)],fill=(180,150,100,255),outline=ink)
    d.text((x,y-r*1.45),'B',font=font(int(r*0.7)),fill=ink,anchor='mm')
def scalebar(d,x,y,w):
    ink=(60,44,28,255)
    for i in range(4): d.rectangle((x+i*w/4,y,x+(i+1)*w/4,y+10),fill=ink if i%2==0 else (246,238,214,255),outline=ink)
    d.text((x,y+14),'0',font=font(20),fill=ink);d.text((x+w,y+14),'≈ 100 dặm',font=font(20),fill=ink,anchor='ra')
def paper():
    r=np.random.default_rng(5);g=r.normal(0,1,(H//2,W//2)).astype(np.float32)
    g=np.asarray(Image.fromarray(np.clip(g*40+128,0,255).astype(np.uint8)).resize((W,H),Image.BICUBIC),np.float32)
    a=np.clip((g-128)*0.25,-14,14)
    rgba=np.zeros((H,W,4),np.uint8);rgba[...,0]=np.where(a>0,255,60);rgba[...,1]=np.where(a>0,250,40);rgba[...,2]=np.where(a>0,240,20);rgba[...,3]=np.abs(a)*1.0
    im=Image.fromarray(rgba,'RGBA');dd=ImageDraw.Draw(im)
    dd.rectangle((14,14,W-15,H-15),outline=(60,44,28,200),width=4);dd.rectangle((26,26,W-27,H-27),outline=(60,44,28,120),width=2)
    for cx,cy in((14,14),(W-15,14),(14,H-15),(W-15,H-15)):
        dd.ellipse((cx-14,cy-14,cx+14,cy+14),fill=(150,110,60,230),outline=(60,44,28,255),width=3)
    return im

