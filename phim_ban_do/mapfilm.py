import json,math,sys,random,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
sys.argv_backup=sys.argv; sys.argv=['x','none']
import build as B
sys.argv=sys.argv_backup
from world import RW,RH,wp
W,H,FPS=1920,1080,30
T,D,TOTAL,texts=B.T,B.D,B.TOTAL,B.texts
font=B.font
ease=B.ease;clamp=B.clamp
WORLD=Image.open('/tmp/proto/world.png').convert('RGB')
PYR=[WORLD]
for i in range(1,4): PYR.append(PYR[-1].resize((RW>>i,RH>>i),Image.LANCZOS))
S0=W/RW
# ---------------- máy quay
def kf(t,lon,lat,z): 
    x,y=wp(lon,lat);return (t,x,y,z)
CAMK=[kf(0,117.2,34.3,1.0),kf(T[128]+1.5,116.2,34.2,1.5),kf(T[128]+D[128]-0.5,117.4,33.9,1.9),
 kf(T[129]+1.0,117.7,33.0,2.4),kf(T[129]+6,118.5,33.2,3.4),
 kf(T[130],118.4,33.8,2.2),kf(T[130]+5,117.95,34.3,4.6),
 kf(T[131]+3,118.1,33.9,2.8),kf(T[132],117.5,34.5,3.0),kf(T[132]+5,117.95,34.3,4.6),
 kf(T[133],118.3,33.6,2.8),kf(T[133]+4,118.47,33.1,3.0),
 kf(T[134],117.95,34.3,5.5),kf(T[137],117.95,34.3,6.5),kf(T[138],117.8,34.35,5.0),kf(T[139]+6,117.95,34.3,4.0),
 kf(T[140],117.95,34.3,3.0),kf(T[141],118.0,34.0,2.2),kf(T[142],117.8,33.6,1.9),kf(T[143]+1,117.4,34.0,1.35),kf(TOTAL,117.2,34.3,1.2)]
def cam(t):
    for i in range(len(CAMK)-1):
        a,b=CAMK[i],CAMK[i+1]
        if t<=b[0] or i==len(CAMK)-2:
            u=ease((t-a[0])/max(1e-6,b[0]-a[0]))
            z=math.exp(math.log(a[3])+(math.log(b[3])-math.log(a[3]))*u)
            return a[1]+(b[1]-a[1])*u,a[2]+(b[2]-a[2])*u,z
    return CAMK[-1][1:]
class View:
    def __init__(s,t):
        s.cx,s.cy,s.z=cam(t);s.z=max(s.z,RW and (RW*H/W)/RH*1.01);s.bw=RW/s.z;s.bh=s.bw*H/W
        s.x0=min(max(s.cx-s.bw/2,0),RW-s.bw);s.y0=min(max(s.cy-s.bh*0.40,0),RH-s.bh)
    def sc(s,lon,lat,k=1):
        x,y=wp(lon,lat);return ((x-s.x0)/s.bw*W*k,(y-s.y0)/s.bh*H*k)
    @property
    def mpp(s): return W/s.bw   # px màn hình / px thế giới
def base_frame(v):
    lvl=0
    while lvl<3 and v.mpp*(2**(lvl+1))<=1.0: lvl+=1
    im=PYR[lvl];f=2**lvl
    return im.resize((W,H),Image.BICUBIC,box=(max(0,v.x0/f),max(0,v.y0/f),min(im.width,(v.x0+v.bw)/f),min(im.height,(v.y0+v.bh)/f)))
# ---------------- dữ liệu
CITY={'Hứa':(113.83,34.03),'Tiểu Bái':(116.93,34.73),'Thọ Xuân':(116.78,32.6),'Hạ Bì':(117.95,34.3),'Hu Di':(118.52,33.0),'Hoài Âm':(119.02,33.58),'Hải Tây':(119.3,33.85)}
COL={'luu':(52,142,86),'tao':(54,96,176),'vien':(190,52,42),'lu':(46,38,58),'dan':(205,160,40),'xam':(120,120,120)}
def lerp(a,b,u): return a+(b-a)*u
def path_pos(keys,t):
    # keys: [(t,lon,lat)]
    if t<=keys[0][0]: return keys[0][1],keys[0][2],0.0
    for i in range(len(keys)-1):
        a,b=keys[i],keys[i+1]
        if t<=b[0]:
            u=ease((t-a[0])/(b[0]-a[0])) if b[0]>a[0] else 1
            moving=(a[1],a[2])!=(b[1],b[2])
            return lerp(a[1],b[1],u),lerp(a[2],b[2],u),(1.0 if moving and 0<u<1 else 0.0)
    return keys[-1][1],keys[-1][2],0.0
class Group:
    def __init__(s,name,col,n,keys,kind='inf',alive=None,show=(0,1e9),seed=1,label=True,spread=1.0,soff=(0,0),defeat=None,emb='circle'):
        s.soff=soff;s.defeat=defeat;s.emb=emb
        s.name,s.col,s.n,s.keys,s.kind=name,col,n,keys,kind
        s.alive=alive or [(0,1.0)];s.show=show;s.label=label
        r=random.Random(seed);s.off=[(r.uniform(-1,1),r.uniform(-1,1)) for _ in range(n)];s.spread=spread
        s.phase=[r.uniform(0,6.28) for _ in range(n)]
    def frac(s,t):
        a=s.alive
        if t<=a[0][0]: return a[0][1]
        for i in range(len(a)-1):
            if t<=a[i+1][0]: return lerp(a[i][1],a[i+1][1],(t-a[i][0])/(a[i+1][0]-a[i][0]))
        return a[-1][1]
    def color(s,t):
        c=s.col
        if callable(c): return c(t)
        return c
GROUPS=[]
def G(*a,**k): g=Group(*a,**k);GROUPS.append(g);return g
t128,t129,t130,t131,t132,t133,t134,t135,t136,t137,t138,t139,t140,t141,t143=[T[i] for i in (128,129,130,131,132,133,134,135,136,137,138,139,140,141,143)]
HB=CITY['Hạ Bì'];HU=CITY['Hu Di'];TX=CITY['Thọ Xuân'];HST=CITY['Hứa'];TB=CITY['Tiểu Bái'];HT=CITY['Hải Tây']
def near(p,dx,dy): return (p[0]+dx,p[1]+dy)
# Tào Tháo ở Hứa
G('Tào Tháo',COL['tao'],10,[(0,*near(HST,0.0,-0.12))],seed=2,emb='dia')
# Lưu Bị: ở Hạ Bì rồi ra Hu Di (câu 129), sau đó rút về Hải Tây (câu 133)
LB_KEYS=[(0,*near(HB,-0.12,-0.1)),(t128+5,*near(HB,-0.12,-0.1)),(t129+3.0,118.47,33.04),(t139+4.0,118.47,33.04),(t141+4.0,*near(HT,-0.1,-0.12))]
LB_ALIVE=[(0,1),(t129+4.5,1),(t129+10,0.78),(t141,0.78)]
G('Lưu Bị',COL['luu'],16,LB_KEYS,alive=LB_ALIVE,seed=3,defeat=(t139+4.0,'lose'),emb='sun')
# Viên Thuật
VT_KEYS=[(0,*TX),(t129+0.3,*TX),(t129+4.2,118.47,32.90),(t136,118.47,32.90)]
G('Viên Thuật',COL['vien'],26,VT_KEYS,alive=[(0,1),(t129+4.5,1),(t129+10,0.82)],seed=4,spread=1.2,emb='tri')
# Trương Phi giữ Hạ Bì
TP_KEYS=[(0,*near(HB,-0.03,0.04)),(t139+0.5,*near(HB,-0.03,0.04)),(t139+6,118.2,33.9)]
G('Trương Phi',COL['luu'],8,TP_KEYS,alive=[(0,1),(t139,1),(t139+3.5,0.3)],show=(t131-0.3,1e9),seed=5,spread=0.6,soff=(-200,80),defeat=(t139+3.5,'lose'),emb='sun')
# Tào Báo trong thành
def tb_col(t): return COL['luu']
G('Tào Báo',(200,150,40),8,[(0,*near(HB,0.03,-0.03))],alive=[(0,1),(t137+1.5,1),(t137+5,0)],show=(t130-0.5,1e9),seed=6,spread=0.6,soff=(170,60),defeat=(t137+4.5,'skull'),emb='dia')
# Lữ Bố
LU_KEYS=[(0,117.15,34.62),(t132+0.5,117.15,34.62),(t132+4.0,117.85,34.38),(t132+8.0,117.85,34.38),(t138+0.0,117.15,34.62),(t138+6.0,117.82,34.36),(t139+2,117.95,34.31)]
G('Lữ Bố',COL['lu'],14,LU_KEYS,kind='cav',show=(t132-0.3,1e9),seed=7,spread=1.0,emb='moon')
# quân Đan Dương mở cổng
G('quân Đan Dương',COL['dan'],10,[(0,117.78,34.36),(t138+4.0,117.78,34.36)],show=(t138+0.5,t139+4),seed=8,spread=0.7,soff=(-120,190),emb='sq')
# trinh sát / thư
LETTERS=[('chiếu của Tào Tháo',[(t128+3.0,*HST),(t128+8.5,*near(HB,-0.12,-0.02))],(236,224,190)),
         ('thư Viên Thuật',[(t136+0.2,*TX),(t136+3.6,117.15,34.62)],(236,224,190)),
         ('tin của Hứa Đam',[(t135+3.0,*HB),(t135+7.0,117.2,34.58)],(236,224,190))]
# gia quyến Lưu Bị bị bắt
FAM=[(t139+3.0,*HB),(t139+7.5,117.4,34.55)]
# vùng Từ Châu
XZ=[(116.55,35.1),(117.3,35.65),(118.4,35.45),(119.35,34.95),(119.45,34.1),(119.0,33.1),(118.3,32.85),(117.4,33.05),(116.7,33.6),(116.45,34.4)]
def owner_col(t):
    # xanh lá -> đen (câu 132 rồi rút lại) -> đen (câu 139)
    if t<t132+4.5: c=COL['luu'];a=0
    elif t<t134: c=COL['lu'];a=1
    elif t<t139+5: c=COL['luu'];a=0
    else: c=COL['lu'];a=1
    return a
OWN=[(0,0),(t139+4,0),(t139+6,1),(TOTAL,1)]
def own(t):
    if t<=OWN[0][0]: return OWN[0][1]
    for i in range(len(OWN)-1):
        if t<=OWN[i+1][0]: return lerp(OWN[i][1],OWN[i+1][1],ease((t-OWN[i][0])/(OWN[i+1][0]-OWN[i][0])))
    return OWN[-1][1]
NIGHT=[(0,0),(t134+2,0),(t135,0.62),(t140,0.62),(t141+2,0.0),(TOTAL,0)]
def night(t):
    if t<=NIGHT[0][0]: return NIGHT[0][1]
    for i in range(len(NIGHT)-1):
        if t<=NIGHT[i+1][0]: return lerp(NIGHT[i][1],NIGHT[i+1][1],ease((t-NIGHT[i][0])/(NIGHT[i+1][0]-NIGHT[i][0])))
    return NIGHT[-1][1]
# trận đánh: (t0,t1,tâm lon,lat,hướng)
BATT=[(t129+4.5,t129+10.5,118.47,32.97,'ngang'),(t137+1.5,t137+5.5,*near(HB,0,0),'ngang'),(t139+0.5,t139+4.5,*near(HB,0.01,0.0),'ngang')]
FIRES=[(t139+0.6,t139+14,0.00,0.02),(t139+1.2,t139+14,-0.05,-0.02),(t139+2.0,t139+14,0.04,-0.04),(t139+2.6,t140+3,-0.02,0.05)]
GATE=[(t132+3.3,1),(t132+8.0,0),(t134,0),(t137+6.5,1),(t140,1)]
def gate_open(t):
    v=0
    for tt,s in GATE:
        if t>=tt: v=s
    return v
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
SUBS=B.SUBS
CARDL=B.CARDL;CARDS=B.CARDS
DAYTXT=None
# ---- trang trí bản đồ: cây, sóng, khung giấy, la bàn
_r=random.Random(77);DECO=[]
_p=PYR[3]
for _ in range(2600):
    lo=_r.uniform(115.6,120.6);la=_r.uniform(32.0,35.9);x,y=wp(lo,la)
    px=_p.getpixel((min(_p.width-1,int(x/8)),min(_p.height-1,int(y/8))))
    water=px[2]>px[0]+10
    DECO.append((lo,la,'wave' if water else ('tree' if _r.random()<0.55 else 'none'),_r.random()))
def deco(d,v,K,z,ik):
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
PAPER=paper()
def frame(t):
    v=View(t);im=base_frame(v).convert('RGBA')
    K=2;ov=Image.new('RGBA',(W*K,H*K),(0,0,0,0));d=ImageDraw.Draw(ov)
    z=v.z;ik=min(2.0,max(0.85,z**0.38))*13.0*K/1.0*1.0   # cỡ biểu tượng
    deco(d,v,K,z,ik)
    # vùng Từ Châu
    a=own(t)
    fillc=tuple(int(lerp(COL['luu'][i],COL['lu'][i],a)) for i in range(3))
    pts=[v.sc(*p,K) for p in XZ]
    d.polygon(pts,fill=fillc+(30,),outline=None)
    for i in range(len(pts)):
        p,q=pts[i],pts[(i+1)%len(pts)];L=math.dist(p,q);n=max(2,int(L/(26*K)))
        for j in range(0,n,2):
            u0=j/n;u1=min(1,(j+1)/n);d.line([(lerp(p[0],q[0],u0),lerp(p[1],q[1],u0)),(lerp(p[0],q[0],u1),lerp(p[1],q[1],u1))],fill=fillc+(200,),width=int(5*K*0.6))
    cx_,cy_=v.sc(117.9,35.15,K);d.text((cx_,cy_),'TỪ CHÂU',font=F(34*K*min(1.6,z**0.3)/1.0*0.9),fill=fillc+(150,),anchor='mm')
    # dòng chữ địa danh lớn
    for nm,(lo,la),sz in(('SÔNG HOÀI',(115.2,32.62),30),('BIỂN ĐÔNG',(121.8,34.8),34)):
        x,y=v.sc(lo,la,K);d.text((x,y),nm,font=F(sz*K*min(1.7,z**0.3)),fill=(70,100,120,150),anchor='mm')
    # thành
    for nm,(lo,la) in CITY.items():
        x,y=v.sc(lo,la,K)
        if not(-200<x<W*K+200 and -200<y<H*K+200): continue
        if nm=='Hạ Bì': city_icon(d,x,y,ik*1.5,open_=gate_open(t))
        elif nm in('Hứa','Thọ Xuân'): city_icon(d,x,y,ik*1.25)
        else:
            d.ellipse((x-ik*0.5,y-ik*0.5,x+ik*0.5,y+ik*0.5),fill=(60,44,30,255),outline=(246,238,214,255),width=3)
        f=F(max(24,26*K*min(1.4,z**0.28)))
        d.text((x,y+ik*1.9),nm,font=f,fill=(40,28,18,255),anchor='mt',stroke_width=int(3*K*0.6),stroke_fill=(246,236,208,255))
    # vết di chuyển
    for g in GROUPS:
        if not(g.show[0]<=t<=g.show[1]): continue
        col=g.color(t);ks=g.keys
        pts=[]
        for i in range(len(ks)):
            if ks[i][0]<=t and (i==0 or (ks[i][1],ks[i][2])!=(ks[i-1][1],ks[i-1][2])): pts.append(v.sc(ks[i][1],ks[i][2],K))
        cur=path_pos(ks,t);pts.append(v.sc(cur[0],cur[1],K))
        for i in range(len(pts)-1):
            p,q=pts[i],pts[i+1];L=math.dist(p,q)
            if L<20: continue
            n=int(L/(22*K));
            for j in range(0,n,2):
                u0=j/n;u1=(j+1)/n;d.line([(lerp(p[0],q[0],u0),lerp(p[1],q[1],u0)),(lerp(p[0],q[0],u1),lerp(p[1],q[1],u1))],fill=col+(150,),width=int(6*K*0.55))
    # quân
    for g in GROUPS:
        if not(g.show[0]<=t<=g.show[1]): continue
        lon,lat,mv=path_pos(g.keys,t);x,y=v.sc(lon,lat,K);sf=1.0 if z<4 else 1.0;x+=g.soff[0]*K*sf;y+=g.soff[1]*K*sf
        if not(-300<x<W*K+300 and -300<y<H*K+300): continue
        col=g.color(t);fr=g.frac(t);s=ik*(1.0 if g.kind=='inf' else 0.9)
        ks=g.keys;face=1
        for i in range(len(ks)-1):
            if ks[i][0]<=t<=ks[i+1][0]: face=1 if ks[i+1][1]>=ks[i][1] else -1
        # tại trận: hai bên quay mặt vào nhau
        for (t0,t1,bl,bt,_) in BATT:
            if t0-1<=t<=t1+1 and g.name in('Lưu Bị','Viên Thuật','Trương Phi','Tào Báo','Lữ Bố'): 
                bx,by=v.sc(bl,bt,K);face=1 if bx>=x else -1
        spr=ik*(2.2 if g.kind=='inf' else 3.0)*g.spread
        for i in range(g.n):
            ox,oy=g.off[i];px=x+ox*spr*1.7;py=y+oy*spr*0.85
            dead=g.defeat is not None and t>=g.defeat[0]
            nfall=int(g.n*max(fr,0.5)) if dead else None
            alive=(i<nfall) if dead else (i/g.n)<fr
            if not alive: continue
            bob=t*(9 if mv else 0)+g.phase[i]
            jit=0
            for (t0,t1,bl,bt,_) in BATT:
                if t0<=t<=t1 and g.name in('Lưu Bị','Viên Thuật','Trương Phi','Tào Báo','Lữ Bố'):
                    bx,by=v.sc(bl,bt,K);px+=(bx-px)*0.0;jit=1;bob=t*14+g.phase[i];px+=math.sin(t*10+g.phase[i])*s*0.5*face
            if dead:
                gc=tuple(int(0.35*c+0.65*110) for c in col);py+=s*0.35
                (soldier if g.kind=='inf' else horse)(d,px,py,s*0.95,gc,face,0.0,alpha=190)
            else: (soldier if g.kind=='inf' else horse)(d,px,py,s,col,face,bob)
        # cờ, tên, phù hiệu, thanh quân số, huy hiệu thua
        dead=g.defeat is not None and t>=g.defeat[0]
        fcol=(120,120,126) if dead else col
        if dead: flag(d,x-spr*1.9,y-spr*0.1,s*0.7,fcol)
        else: flag(d,x-spr*1.9,y-spr*0.6,s*1.05,col)
        if g.label:
            tag2(d,x,y+spr*1.1,g,col,int(24*K*min(1.3,z**0.25)),(max(fr,0.0) if not dead else max(fr,0.0)),dead,t)
        if dead:
            u=(t-g.defeat[0])/0.8
            badge(d,x,y-spr*1.5-ik*1.2,ik*2.3,g.defeat[1],u)
            tg='BỊ DIỆT' if g.defeat[1]=='skull' else 'THUA TRẬN'
            ff=font(int(22*K*min(1.3,z**0.2)));bb=d.textbbox((0,0),tg,font=ff)
            d.rounded_rectangle((x-(bb[2]-bb[0])/2-14,y-spr*1.5+ik*1.3,x+(bb[2]-bb[0])/2+14,y-spr*1.5+ik*1.3+(bb[3]-bb[1])+16),10,fill=(110,30,26,235))
            d.text((x-(bb[2]-bb[0])/2,y-spr*1.5+ik*1.3+6-bb[1]*0),tg,font=ff,fill=(250,244,226,255))
    # trận: mũi tên, tia chớp binh khí
    for (t0,t1,bl,bt,_) in BATT:
        if t0<=t<=t1:
            bx,by=v.sc(bl,bt,K);rr=ik*3.2
            for i in range(14):
                ph=((t*1.6+i*0.37)%1);side=1 if i%2 else -1
                sx_=bx-side*rr*1.3;ex_=bx+side*rr*1.3;ay=by-rr*0.4+ (i%5-2)*ik*0.8
                px=lerp(sx_,ex_,ph);py=ay-math.sin(ph*math.pi)*rr*1.1
                nx=lerp(sx_,ex_,min(1,ph+0.04));ny=ay-math.sin(min(1,ph+0.04)*math.pi)*rr*1.1
                d.line([(px,py),(nx,ny)],fill=(50,36,24,230),width=int(3*K*0.6))
            for i in range(6):
                u=(t*3+i*0.31)%1;qx=bx+math.sin(i*2.1+t*5)*rr*0.5;qy=by+math.cos(i*1.7+t*4)*ik*1.2
                for kk in range(5):
                    ang=kk*1.26+i;d.line([(qx,qy),(qx+math.cos(ang)*ik*1.7*u,qy+math.sin(ang)*ik*1.7*u)],fill=(255,240,180,int(220*(1-u))),width=int(3*K*0.55))
    # bộ đếm ngày ở trận Hu Di
    if BATT[0][0]<=t<=BATT[0][1]+1.5:
        day=int(1+29*clamp((t-BATT[0][0])/(BATT[0][1]-BATT[0][0])))
        bx,by=v.sc(118.46,32.93,K)
        tag(d,bx,by-ik*12,f'NGÀY {day}',(120,40,30),int(40*K*min(1.3,z**0.2)))
    # lửa
    for i,(t0,t1,dx,dy) in enumerate(FIRES):
        if t0<=t<=t1:
            x,y=v.sc(HB[0]+dx,HB[1]+dy,K);fire(d,x,y,ik*1.5*min(1,(t-t0)/1.0+0.2),t,i)
    # thư và chiếu
    for nm,ks,c in LETTERS:
        if ks[0][0]<=t<=ks[-1][0]:
            u=ease((t-ks[0][0])/(ks[-1][0]-ks[0][0]));ax,ay=v.sc(ks[0][1],ks[0][2],K);bx,by=v.sc(ks[-1][1],ks[-1][2],K)
            ctl=(lerp(ax,bx,0.5),min(ay,by)-abs(bx-ax)*0.28-ik*6)
            def bez(u): return ((1-u)**2*ax+2*(1-u)*u*ctl[0]+u*u*bx,(1-u)**2*ay+2*(1-u)*u*ctl[1]+u*u*by)
            for j in range(0,int(u*40),2):
                p=bez(j/40);q=bez(min(1,(j+1)/40));d.line([p,q],fill=(120,90,50,200),width=int(5*K*0.6))
            px,py=bez(u);scroll(d,px,py,ik*1.1)
            tag(d,px,py-ik*3.8,nm,(110,70,30),int(20*K*min(1.3,z**0.2)))
    # gia quyến bị bắt
    if FAM[0][0]<=t<=FAM[1][0]+3:
        u=ease((t-FAM[0][0])/(FAM[1][0]-FAM[0][0]));lon=lerp(FAM[0][1],FAM[1][1],u);lat=lerp(FAM[0][2],FAM[1][2],u)
        x,y=v.sc(lon,lat,K)
        d.rounded_rectangle((x-ik*1.6,y-ik*0.9,x+ik*1.6,y+ik*0.9),ik*0.3,fill=(130,90,50,255),outline=(30,22,16,255))
        d.ellipse((x-ik*1.9,y+ik*0.5,x-ik*1.0,y+ik*1.4),fill=(40,30,20,255));d.ellipse((x+ik*1.0,y+ik*0.5,x+ik*1.9,y+ik*1.4),fill=(40,30,20,255))
        tag(d,x,y-ik*3.4,'vợ con Lưu Bị',COL['luu'],int(20*K*min(1.3,z**0.2)))
    # mũi tên gọng kìm ở câu 143
    if t>=t143+1.0:
        k=clamp((t-t143-1.0)/2.5);k=ease(k)
        for (a_,b_,c_,nm) in(((115.5,35.5),(117.6,34.62),COL['tao'],'Tào Tháo'),((116.8,32.7),(117.6,33.98),COL['vien'],'Viên Thuật')):
            ax,ay=v.sc(*a_,K);bx,by=v.sc(*b_,K);ex,ey=lerp(ax,bx,k),lerp(ay,by,k)
            d.line([(ax,ay),(ex,ey)],fill=c_+(255,),width=int(11*K*0.6))
            if k>0.95:
                ang=math.atan2(by-ay,bx-ax);L=ik*3
                d.polygon([(bx+math.cos(ang)*L*0.2,by+math.sin(ang)*L*0.2),(bx+math.cos(ang+2.5)*L,by+math.sin(ang+2.5)*L),(bx+math.cos(ang-2.5)*L,by+math.sin(ang-2.5)*L)],fill=c_+(255,))
            tag(d,lerp(ax,bx,0.5),lerp(ay,by,0.5)-ik*3,nm,c_,int(28*K*min(1.3,z**0.2)))
    ov=ov.resize((W,H),Image.LANCZOS)
    out=Image.alpha_composite(im,ov)
    # đêm
    n_=night(t)
    if n_>0.01:
        arr=np.asarray(out.convert('RGB'),np.float32)
        arr*=np.array([1-0.58*n_,1-0.5*n_,1-0.22*n_],np.float32)
        # ánh đuốc/lửa
        yy,xx=np.mgrid[0:H,0:W]
        glow=np.zeros((H,W),np.float32)
        srcs=[(HB[0]+dx,HB[1]+dy) for (t0,t1,dx,dy) in FIRES if t0<=t<=t1]
        if t>=t134 and t<=t140: srcs+= [(HB[0]+0.04,HB[1]+0.03),(HB[0]-0.04,HB[1]-0.03),(HB[0]+0.02,HB[1]-0.05)]
        for lo,la in srcs:
            x,y=v.sc(lo,la);r=80*min(2.2,z**0.5)
            glow+=np.exp(-(((xx-x)**2+(yy-y)**2)/(2*r*r)))*(0.8+0.2*math.sin(t*13+lo*50))*0.55
        arr+=glow[...,None]*np.array([110,64,18],np.float32)*n_
        out=Image.fromarray(np.clip(arr,0,255).astype(np.uint8)).convert('RGBA')
    # vignette nhẹ
    vg=VIGN
    out=Image.alpha_composite(out,vg);out=Image.alpha_composite(out,PAPER)
    hud=Image.new('RGBA',(W,H),(0,0,0,0));hd=ImageDraw.Draw(hud);compass(hd,W-110,120,46);scalebar(hd,W-290,205,170)
    out=Image.alpha_composite(out,hud)
    # HUD
    out=B.comp(out,B.YEARL[min(10,int(10*(t-T[128])/(TOTAL-T[128])))],(50,40),clamp((t-0.6)/0.6)*clamp((TOTAL-1.2-t)/0.5))
    for (cn,_,_,_,dl) in CARDS:
        if B.beat_of(t)==cn:
            s=T[cn]+dl;e=T[cn]+D[cn]-0.3
            if s<=t<=e:
                k=min(clamp((t-s)/0.5),clamp((e-t)/0.4));out=B.comp(out,CARDL[cn],(50-int((1-ease(k))*160),215),ease(k))
    for (cn,_,_,dl) in B.NUMS:
        if B.beat_of(t)==cn:
            s=T[cn]+dl;e=s+2.6
            if s<=t<=e:
                k=min(clamp((t-s)/0.25),clamp((e-t)/0.4));out=B.comp(out,B.NUML[cn],(0,0),ease(k))
    n=B.beat_of(t);lt=t-T[n];k=min(clamp(lt/0.35),clamp((D[n]-lt)/0.3))
    out=B.comp(out,SUBS[n],(0,0),ease(k) if lt>0.05 else 0)
    if t<0.5: out=Image.blend(Image.new('RGBA',(W,H),(8,5,3,255)),out,ease(t/0.5))
    if t>TOTAL-1.0: out=Image.blend(out,Image.new('RGBA',(W,H),(8,5,3,255)),ease((t-(TOTAL-1.0))/1.0))
    return out.convert('RGB')
yy,xx=np.mgrid[0:H,0:W]
vv=(((xx-W/2)/(W*0.62))**2+((yy-H/2)/(H*0.66))**2)
VIGN=Image.fromarray(np.stack([np.zeros((H,W),np.uint8)]*3+[(np.clip(vv-0.35,0,1)*120).astype(np.uint8)],-1),'RGBA')
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='still':
        for ts in sys.argv[2:]: frame(float(ts)).save(f'/tmp/proto/m_{ts}.jpg',quality=90)
        sys.exit()
    import multiprocessing as mp
    def work(i): return frame(i/FPS).tobytes()
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','/tmp/proto/mv.mp4'],stdin=subprocess.PIPE)
    N=int(TOTAL*FPS)
    with mp.Pool(2) as pool:
        for i,b in enumerate(pool.imap(work,range(N),chunksize=4)):
            p.stdin.write(b)
            if i%150==0: print(i,N,flush=True)
    p.stdin.close();p.wait()
