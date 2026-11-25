# dai_tm27: Bạch Đằng 1288 (lời dọa của Ô Mã Nhi, Chiêu Lăng, sông Bạch Đằng), giọng Charon đọc lại lần 2 (25/11); kiểu hình mới: nền phong cảnh FLUX không người + người vẽ bằng mã. Nhân vật múa rối riêng tập (t26n_r_*), có nét mặt sợ, giận, reo (headS/G/V)
# và tư thế cảm xúc (rig.so, hoang, reo, quat, xung, nga). Mỗi đoạn chia 2–3 góc máy theo từng câu lời kể.
import math,re,json,os
import numpy as np
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from engine import ragged
from fx_tran import arrows,dust,sparks,fall
from tran_fx import clash
from dai_tm2 import big,lb
P=PTS
V=K.setup('tm27',{5:4.0})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
FREEZE=bool(os.environ.get('KIEM_TINH'))
GS=1.45
HAN=(.17,.29,.45)
GOLD=np.array((.79,.64,.35),np.float32)
_SC={}
for _n,_t in TX.items():
    _s=[x for x in re.split(r'(?<=[.!?])\s+',_t) if x.strip()];_w=[len(x.split()) for x in _s];_tot=sum(_w);_c=[0]
    for _k in _w: _c.append(_c[-1]+_k/_tot)
    _SC[_n]=_c
def sb(n,k): return T[n]+(E[n]-T[n])*_SC[n][min(k,len(_SC[n])-1)]
def kc(t,keys,sh=0):
    if FREEZE: t=keys[0][0];sh=0
    cx,cy,z=cpath(t,keys);return cam(cx,cy,z,sh,sh)
def mcam(t,keys):
    if FREEZE: t=keys[0][0]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z);return cam(cx,cy,z)
C0=cam(960,540,1.0)
def suong(cv,c,t,y=560,o=.5,seed=0):
    if FREEZE: return
    for i,(sp,k,yy,s) in enumerate([(22,.5,y-120,2.2),(34,1.1,y+120,2.6)]):
        x=(300+seed*400+i*900+t*sp)%2800-400;put(cv,c,'mist',x,yy,s=s,o=o*(.8 if i else 1),k=k)
def ngoai(cv,c,t,g=900,far=.9,midv=.85,mist=.5,seed=0):
    put(cv,c,'t26_far',960+seed*60,g-120,ay=1,k=.35,o=far)
    put(cv,c,'t26_mid',960-seed*40,g+30,ay=1,k=.62,o=midv)
    suong(cv,c,t,g-260,mist,seed)
def truoc(cv,c,t,o=1):
    put(cv,c,'t26_frontL',-120,1120,ax=0,ay=1,k=1.3,s=.85,r=1.2*math.sin(t*.8),o=o)
    put(cv,c,'t26_frontR',2040,1120,ax=1,ay=1,k=1.3,s=.8,r=1.2*math.sin(t*.7+1),o=o)
def di(cv,c,name,x0,y0,x1,y1,t,a,b,s=1.0,o=.97,bob=4,f=5,ph=0,k=1.0,r=0,lac=1.2,lat=False):
    if y0>700 and k==1.0: s*=GS;bob*=GS
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;y=y0+(y1-y0)*u-abs(math.sin(t*f+ph))*bob*(1 if 0<u<1 else .3)
    put(cv,c,Af(name) if lat else name,x,y,s=s,o=o,k=k,r=r+lac*math.sin(t*f*.5+ph),ay=1,scale_px=1.5)
    return x,y
def flick(cv,c,x,y,t,s=1.0):
    put(cv,c,'t12_spr_lua',x+6*math.sin(t*7),y,s=min(s,.38)*(1+.08*math.sin(t*9)),o=.5+.3*math.sin(t*5)**2)
def smoke(cv,c,x,y,t,s=1.0):
    for k in range(2): put(cv,c,'t12_spr_khoi',x+20*math.sin(t*.7+k),y-((t*40+k*120)%240),s=s,o=.5*(1-((t*40+k*120)%240)/240))
def co_bay(cv,c,name,x,y,t,s=1.0,ph=0,lat=False):
    put(cv,c,Af(name) if lat else name,x,y,s=s,ay=1,r=2.5*math.sin(t*2.2+ph),scale_px=1.5)
# ---- mặt nạ mực, vòng tiếng gọi
_NZ=None
def nz():
    global _NZ
    if _NZ is None:
        rg=np.random.default_rng(27);a=rg.random((34,60)).astype(np.float32)
        from PIL import Image as _I
        _NZ=np.asarray(_I.fromarray((a*255).astype(np.uint8)).resize((W,H),_I.BICUBIC),np.float32)/255
    return _NZ
_YY,_XX=np.mgrid[0:H,0:W].astype(np.float32)
def loang(cx,cy,r,soft=40):
    d=np.sqrt((_XX-cx)**2+(_YY-cy)**2)+(nz()-.5)*r*.35
    return np.clip((r-d)/soft,0,1)[...,None]
_RG=ragged(H,7)[:,None]
def quet(u,band=.12):
    x=_XX/W+(_RG-.5)*.16
    return np.clip((u*(1+band*2)-band-x)/band,0,1)[...,None]
def vong(cv,x,y,t,t0,n=3,per=1.4,rmax=520,o=.55,col=None,flat=.55):
    """vòng tiếng gọi lan ra từ mặt trống (hình ảnh lặp lại), tọa độ màn hình"""
    if FREEZE or t<t0: return
    col=np.array(col if col is not None else RED,np.float32)
    x0,x1=int(max(0,x-rmax-20)),int(min(W,x+rmax+20));y0,y1=int(max(0,y-rmax*flat-20)),int(min(H,y+rmax*flat+20))
    if x1<=x0 or y1<=y0: return
    d=np.sqrt((_XX[y0:y1,x0:x1]-x)**2+((_YY[y0:y1,x0:x1]-y)/flat)**2)
    m=np.zeros_like(d)
    for k in range(n):
        u=((t-t0)/per+k/n)%1.0;r=20+u*rmax
        m=np.maximum(m,np.clip(1-np.abs(d-r)/7,0,1)*(1-u)*o)
    m=m[...,None];cv[y0:y1,x0:x1]=cv[y0:y1,x0:x1]*(1-m)+col*m
import rig
from engine import asc
import rig
from engine import asc
VIETC=(.20,.31,.43);MONGC=(.42,.33,.24);GOLDC=(.79,.64,.35)
# ---------- nền ----------
def nen(cv,c,t,kieu='dong',g=900,seed=0,mist=.45):
    sd=(seed*37)%7-3
    put(cv,c,'t26_far',960+sd*50,g-120,ay=1,k=.35,o=.85)
    if kieu=='song':
        put(cv,c,'t26_mid',960-sd*40,g-170,ay=1,k=.5,o=.6)
        put(cv,c,'t26_song',960,g-270,ay=0,k=.8,s=1.0,o=.95)
    else: put(cv,c,'t26_mid',960-sd*40,g+30,ay=1,k=.62,o=.8)
    suong(cv,c,t,g-260,mist,seed)
def song(cv,c,t,y=620,o=.95):
    put(cv,c,'t26_song',960,y,ay=0,k=.85,o=o)
# ---------- người, ngựa, thuyền ----------
def ss(y,s): return s*GS if y>700 else s
def nguoi(cv,c,key,x,y,t,s=.62,vk=None,flip=False,PP=None,o=1.0,ph=0):
    rig.ve23(cv,c,key,x,y,ss(y,s),PP or rig.dung(t+ph),flip=flip,vk=vk,o=o)
def dib(cv,c,key,x0,x1,y,t,a,b,s=.62,vk=None,flip=None,ph=0,o=1.0,buoc=60,chay=1.0,sua=None):
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;mv=1.0 if 0<u<1 else 0.0
    S_=ss(y,s);pha=abs(x-x0)/(buoc*rig.SC*S_)*math.pi+ph
    PP=rig.tron(rig.dung(t+ph),rig.walk(pha,chay),mv)
    if sua: sua(PP,t)
    rig.ve23(cv,c,key,x,y,S_,PP,flip=(x1<x0) if flip is None else flip,vk=vk,o=o)
    return x
def ngua(cv,c,mau,key,x0,x1,y,t,a,b,s=.62,vk=None,flip=None,ph=0,o=1.0,sua=None):
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;mv=1.0 if 0<u<1 else 0.15
    S_=ss(y,s);pha=abs(x-x0)/(70*rig.SC*S_)*math.pi+ph+t*(0 if mv==1 else 1.5)
    PP=rig.ngoi(t+ph)
    if sua: sua(PP,t)
    rig.ngua(cv,c,mau,x,y,S_,pha,mv,flip=(x1<x0) if flip is None else flip,o=o,nguoi=key,P=PP,vk=vk,t=t)
    return x
def thuyen(cv,c,x,y,t,s=.6,lon=False,flip=False,ngoi=(),o=1.0,ph=0):
    """thuyền dập dềnh; ngoi=[(key,dx,vk)] người ngồi trên mạn"""
    if y>=880: y-=140
    S_=ss(y+140,s);bob=3*math.sin(t*1.3+ph+x*.01);r=.8*math.sin(t*.9+ph)
    name='t23n_thuyenlon' if lon else 't23n_thuyen'
    for key,dx,vk in ngoi:
        f=-1 if flip else 1
        PP=rig.ngoi(t+dx*.01);PP.update(thF=-80,thB=-76,knF=84,knB=82)
        if vk=='cheo': PP.update(arF=-10+25*math.sin(t*2+dx),faF=-40,arB=10+25*math.sin(t*2+dx),faB=-40);vk=None
        elif vk=='so': PP.update(arF=-120+3*math.sin(t*23),faF=-70,arB=-100,faB=-80,lean=-10,mat='S');vk=None
        elif vk=='quat': PP.update(arF=-88+4*math.sin(t*4),faF=-4,lean=6,mat='G');vk=None
        elif vk=='reo': PP.update(arF=-160+8*math.sin(t*6),faF=-5,arB=-140,faB=-10,mat='V');vk=None
        rig.ve23(cv,c,key,0,0,S_,PP,flip=flip,vk=vk,o=o,hip=c_pt(x+f*dx*S_,y-46*S_+bob))
    put(cv,c,Af(name) if flip else name,x,y+bob,s=S_,r=r,ay=.8,o=o,scale_px=3)
def c_pt(x,y): return (x,y)
def voi(cv,c,x,y,t,s=.6,flip=False,o=1.0,ph=0):
    S_=ss(y,s);put(cv,c,Af('t23n_voi') if flip else 't23n_voi',x,y-3*abs(math.sin(t*1.1+ph))*S_,s=S_,ay=1,r=.6*math.sin(t*.9+ph),o=o,scale_px=3)
def co(cv,c,name,x,y,t,s=.5,ph=0,flip=False):
    put(cv,c,Af(name) if flip else name,x,y,s=ss(y,s),ay=1,r=2.2*math.sin(t*2+ph))
def ten(cv,c,t,a,b,src,dst,n=8,h=120,seed=23,col=None):
    arrows(cv,c,t,a,b,src,dst,n=n,h=h,per=1.0,seed=seed,col=col if col is not None else MONGC)
def cuon(cv,x,y,t,tieu,chu,col=None,o=1.0,s=.62,sz=46,u=1.0,nm='t26n_cuon'):
    put(cv,C0,nm,x,y,s=s*2,o=o)
    if FREEZE: return
    put_screen(cv,text(tieu,28,INK,700),x,y-170*s/.62,o)
    for k,ln in enumerate(chu.split('|')): put_screen(cv,wipe(text(ln,sz,col if col is not None else RED,700),u,0,.25,seed=int(x)+k),x,y-20+k*(sz+16),o)
def nhan(cv,txt,x,y,t,t0,t1,col=None,sz=40,w=None):
    if FREEZE or not(t0<t<t1): return
    u=inn(t,t0,.35)*(1-inn(t,t1-.35,.35));tx=text(txt,sz,col if col is not None else INK,700)
    put_screen(cv,band(w or tx.shape[1]+50,tx.shape[0]+26,PAPER,.86,18),x,y,u);put_screen(cv,tx,x,y,u)
for _k in ['tkd','tkd2','tts6','tnt6','hdv6','ts6','lh6','tvh','thn6','omn6','v6','v7','v8','m7','m8','m9','d6a','d6b','d6c']: rig.PRE[_k]='t26n_r_'
for _k in ['dh7','ptp','tlc','tqn','v9','v10','v11']: rig.PRE[_k]='t27n_r_'
def gio(PP,t_): PP.update(arF=-150+6*math.sin(t_*2),faF=-10)
# ---------- bản đồ và sơ đồ trận (sửa 25/11 theo góp ý chủ kênh) ----------
PTM=json.load(open('/tmp/gen/bd/a/map_pts.json'))
def mcam(t,keys):
    if FREEZE: t=keys[0][0]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z);return cam(cx,cy,z)
def bando(cv,c,t,a):
    im=A('map')
    if not FREEZE and t<a+1: im=wipe(im,inn(t,a-.2,1.0),0,.25,seed=4)
    put(cv,c,im,960,540,scale_px=1.5)
def diem(cv,c,nm,p,t,t0,col=INK,sz=36,dx=22,dy=-6):
    if t<t0: return
    o=inn(t,t0,.3);dot(cv,c,*p,o=o,col=col,r=7)
    X,Y=c.p(*p);tx=text(nm,sz,col,700,glow=3)
    put_screen(cv,tx,X+dx+(tx.shape[1]/2 if dx>=0 else -tx.shape[1]/2),Y+dy,o)
def duong(cv,c,pts,t,t0,dur,col,wid=9):
    if FREEZE: return stroke(cv,c,pts,1,wid=wid,col=col,o=.85,head=True)
    stroke(cv,c,pts,inn(t,t0,dur),wid=wid,col=col,o=.85,head=True)
def theo(pts,u):
    L=[math.dist(pts[i],pts[i+1]) for i in range(len(pts)-1)];tot=sum(L);d=u*tot
    for i,l in enumerate(L):
        if d<=l or i==len(L)-1:
            v=min(d/l,1) if l else 0;return pts[i][0]+(pts[i+1][0]-pts[i][0])*v,pts[i][1]+(pts[i+1][1]-pts[i][1])*v
        d-=l
def cotheo(cv,c,name,pts,t,t0,dur,s=.14,ph=0,o=1.0):
    """lá cờ đi theo đường tiến quân (dấu hiệu một đạo quân trên bản đồ)"""
    u=inn(t,t0,dur);x,y=theo(pts,u)
    put(cv,c,name,x,y,s=s,ay=1,r=2*math.sin(t*3+ph),o=o)
def khoi(cv,c,x,y,w,h,col,o=.9):
    put(cv,c,band(w,h,col,o,6),x,y)
def pulse(cv,c,x,y,t,col=RED):
    for k in range(2):
        u=((t*.6+k*.5)%1.0);dot(cv,c,x,y,o=.6*(1-u),col=col,r=int(8+40*u))

# ---------- hiệu ứng cảm xúc tm25 ----------
def run(cv,c,x,y,s=1.0,t=0,o=1.0):
    """vạch run quanh đầu người đang sợ"""
    for k in range(3):
        a=-0.6+k*.6;r=60*s;put(cv,c,band(int(18*s)+2,3,INK,.6*o,1),x+math.cos(a)*r,y-math.sin(a)*r+2*math.sin(t*30+k),r=math.degrees(a))
def roi(cv,c,name,x0,y0,t,t0,dx=120,s=.6,quay=1):
    """vũ khí rơi khỏi tay: văng ra rồi rơi xuống đất"""
    if t<t0: return
    u=min(1,(t-t0)/.7);x=x0+dx*u;y=y0-120*s*math.sin(u*math.pi)+260*s*u*u
    put(cv,c,name,x,y,s=s,r=quay*(30+300*u),scale_px=3)
def bui(cv,c,x,y,t,t0,n=4,s=.35):
    if t<t0: return
    for k in range(n): dust(cv,c,x+k*60+40*(t-t0),y-10*k,o=.35*max(0,1-(t-t0)/3),s=s*(1+.4*(t-t0)))
def mat(P,m):
    P=dict(P);P['mat']=m;return P
def tronm(p,q,u,m=None):
    pp={k:v for k,v in p.items() if k!='mat'};qq={k:v for k,v in q.items() if k!='mat'}
    r=rig.tron(pp,qq,u)
    if m: r['mat']=m
    elif u>.5 and 'mat' in q: r['mat']=q['mat']
    elif 'mat' in p: r['mat']=p['mat']
    return r
from fx_tran import dust

# ---------- kiểu hình mới tm27: nền tranh thủy mặc (FLUX, không người) ----------
def tranh(cv,name,t,a,b,p0,p1,o=1.0):
    """vẽ nền tranh khổ 1024: p=(cx,cy,zoom) theo pixel ảnh; zoom 1 = ảnh rộng vừa khung 1920"""
    u=inn(t,a,max(.1,b-a));cx=lerp(p0[0],p1[0],u);cy=lerp(p0[1],p1[1],u);z=lerp(p0[2],p1[2],u)*1.875
    hw,hh=960/z,540/z;cx=min(max(cx,hw),1024-hw);cy=min(max(cy,hh),1024-hh)
    global _CC
    _CC=Cam(cx,cy,z,W,H);_CC.yy=(cx,cy,z);put(cv,_CC,'t27n_bg_'+name,0,0,s=3,ax=0,ay=0,o=o)
    for j in range(2): put(cv,_CC,band(900,70,PAPER,.18,40),300+j*520+40*math.sin(t*.2+j),380+j*40,k=.6)
    return lambda ix,iy:(960+(ix-cx)*z,540+(iy-cy)*z,z/1.875)
C0S=None
def ngua_da(cv,mp,t,bun=0):
    """hai ngựa đá đứng chầu trên bệ trước lăng (bản mo_a)"""
    global C0S
    if C0S is None: C0S=Cam(960,540,1.0,W,H)
    for ix,iy,fl in [(166,560,False),(884,571,True)]:
        X,Y,k=mp(ix,iy)
        rig.ngua(cv,C0S,'den',X,Y,.26*k,0,chay=0.0,flip=fl,o=.92)
        if bun and not FREEZE:
            for j in range(4): put_screen(cv,band(int(22*k),int(12*k),INK,.55*bun,4),X+(-40+j*26)*k*(-1 if fl else 1),Y-14*k)
_CC=None
def tong(cv,k=.5):
    """đưa người, thuyền về tông mực của tranh: bớt màu; thêm lớp sương gần (thị sai)"""
    global _CC
    if _CC is not None:
        for j in range(3): put(cv,_CC,band(700,60,PAPER,.16,40),_CC.yy[0]-420+j*420,_CC.yy[1]+250/_CC.yy[2]+j*6,k=1.4)
        _CC=None
    if FREEZE: return
    lum=cv.mean(2,keepdims=True);tone=INK+lum*(PAPER-INK);cv[:]=cv*(1-k)+tone*k
def suong2(cv,t,y,o=.45,sp=30,seed=0):
    for k in range(2): put_screen(cv,band(1900,100,PAPER,o,50),((t*sp+k*1100+seed*300)%3000)-500,y+k*80)
def ngd(cv,c,key,x,y,t,s,P,flip=False,vk=None,o=1.0):
    rig.ve23(cv,c,key,x,y,ss(y,s),P,flip=flip,vk=vk,o=o)
def chay(cv,c,key,x0,x1,y,t,a,b,s,ham,flip=None,vk=None,ph=0,buoc=60,o=1.0):
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;S_=ss(y,s);pha=abs(x-x0)/(buoc*rig.SC*S_)*math.pi+ph
    P=ham(pha,t) if 0<u<1 else rig.dung(t+ph)
    rig.ve23(cv,c,key,x,y,S_,P,flip=(x1<x0) if flip is None else flip,vk=vk,o=o);return x
VA=['v8','v9','v10'];MA=['m7','m8','m9']
def quy(P):
    P=dict(P);P.update(thF=-90,knF=90,thB=0,knB=90,lean=10,arF=-60,faF=-40,arB=-50,faB=-40);return P
def lay(P,t_=0):
    P=dict(P);P.update(lean=14+3*math.sin(t_),arF=-40,faF=-50,arB=-30,faB=-50);return P
def ngam(P):
    """đưa tay lên trán nhìn xa"""
    P=dict(P);P.update(arF=-150,faF=-110,head=-4);return P
def song_nuoc(cv,x,y,t,t0,col=None,n=3,o=.6):
    """vòng nước bắn lên khi bao gạo rơi"""
    if FREEZE or t<t0: return
    for k in range(n):
        u=min(1,(t-t0)/1.2-k*.15)
        if u<=0: continue
        put_screen(cv,band(int(40+200*u),int(10+26*u),INK,o*(1-u),6),x,y)
def gao_roi(cv,c,x0,y0,t,t0,dx=80,s=.5,yday=920):
    if t<t0: return
    u=min(1,(t-t0)/.9);x=x0+dx*u;y=y0-60*math.sin(u*math.pi)+(yday-y0)*u*u
    if u<1: put(cv,c,'t26n_gao',x,y,s=s,r=200*u)
    else:
        X,Y=c.p(x,yday);song_nuoc(cv,X,Y,t,t0+.9)
def soi(cv,c,x,y,t,s=1.0):
    """vạch tỏa quanh mặt người đang giận, quát"""
    if FREEZE: return
    for k in range(3):
        a=0.3+k*.5;r=70*s+6*math.sin(t*12+k);put(cv,c,band(int(20*s)+2,4,RED,.6,1),x+math.cos(a)*r,y-math.sin(a)*r,r=-math.degrees(a))

# ---------- tm27: người kiểu nhìn từ sau, ngựa nghiêng, cọc, thuyền nghiêng ----------
LINHSAU='abc'
def linhsau(cv,c,i,x,y,s,t,o=1.0):
    put(cv,c,f't27n_linhsau_{LINHSAU[i%3]}_{int(t*3.2+i*.5)%2}',x,y,s=s,ay=1,o=o)
def chim(cv,c,t,x0,y0,n=4,sp=40,seed=0):
    for i in range(n):
        x=x0+((t*sp+i*90+seed*50)%900);y=y0+i*18+6*math.sin(t*3+i)
        put(cv,c,'t12_spr_chim',x,y,s=.12+.02*(i%2),r=8*math.sin(t*6+i))
RC=np.random.default_rng(8)
COC=[(int(260+i*60+RC.normal(0,10)),int(690+RC.normal(0,10)+(i%3)*12),RC.uniform(-18,18),RC.uniform(.8,1.05)) for i in range(24)]
def coc(cv,c,t,wl,lo=0,hi=99):
    """cọc gỗ nhọn: chỉ phần trên mặt nước wl mới thấy"""
    if FREEZE: return
    for k,(x,yb,ang,h) in enumerate(COC):
        if not lo<=k<hi: continue
        top=yb-120*h;X0,Y0=c.p(x,yb);X1,Y1=c.p(x+math.sin(math.radians(ang))*120*h,top);Yw=c.p(0,wl)[1]
        if Y1>Yw-2: continue
        col=tuple(float(v) for v in INK+.05);w=max(3,int(8*c.z*h));Yb=min(Y0,Yw+4)
        dx_,dy_=X1-X0,Y1-Yb;L_=math.hypot(dx_,dy_)+1e-6;nx,ny=-dy_/L_,dx_/L_;tx,ty=X1+dx_/L_*w*2.2,Y1+dy_/L_*w*2.2
        cv2.fillPoly(cv,[np.int32([[X0+nx*w,Yb+ny*w],[X1+nx*w*.8,Y1+ny*w*.8],[tx,ty],[X1-nx*w*.8,Y1-ny*w*.8],[X0-nx*w,Yb-ny*w]])],col,cv2.LINE_AA)
        cv2.ellipse(cv,(int(X0),int(Yw+3)),(int(w*1.6),3),0,0,360,tuple(float(v) for v in INK*.5+PAPER*.5),1,cv2.LINE_AA)
import cv2
def tthuyen(cv,c,x,y,t,s,lon,flip,ngoi,nghieng=0,o=1.0,ph=0):
    """thuyền có thể nghiêng khi mắc cọc; ngoi=[(key,dx,kiểu)]"""
    bob=0 if nghieng else 3*math.sin(t*1.3+ph);r=nghieng+.8*math.sin(t*.9+ph)
    f=-1 if flip else 1;name='t23n_thuyenlon' if lon else 't23n_thuyen'
    for key,dx,vk in ngoi:
        PP=rig.ngoi(t+dx*.01);PP.update(thF=-80,thB=-76,knF=84,knB=82)
        if vk=='cheo': PP.update(arF=-10+25*math.sin(t*4+dx),faF=-40,arB=10+25*math.sin(t*4+dx),faB=-40,mat='G');vk=None
        elif vk=='so': PP.update(arF=-120+3*math.sin(t*23),faF=-70,arB=-100,faB=-80,lean=-10,mat='S');vk=None
        elif vk=='dam': PP.update(arF=-60+40*math.sin(t*6+dx),faF=-10,lean=14,mat='G');vk='giao'
        elif vk=='quat': PP.update(arF=-88+4*math.sin(t*4),faF=-4,lean=6,mat='G');vk=None
        elif vk=='reo': PP.update(arF=-160+8*math.sin(t*6),faF=-5,arB=-140,faB=-10,mat='V');vk='giao'
        elif vk=='trong': PP.update(arF=-100+50*abs(math.sin(t*7)),faF=-20,arB=-100+50*abs(math.sin(t*7+1.5)),faB=-20,mat='G');vk=None
        rr=math.radians(r);hx=x+f*dx*s*math.cos(rr);hy=y-46*s+bob+f*dx*s*math.sin(rr)
        rig.ve23(cv,c,key,0,0,s,PP,flip=flip,vk=vk,o=o,hip=(hx,hy))
    put(cv,c,Af(name) if flip else name,x,y+bob,s=s,r=r,ay=.8,o=o,scale_px=3)
def tenbay(cv,c,t,src,dst,n,seed):
    if FREEZE: return
    r=np.random.default_rng(seed)
    for i in range(n):
        ph=((t*.9+r.random())%1.0);a=(src[0]+r.normal(0,40),src[1]+r.normal(0,20));b=(dst[0]+r.normal(0,80),dst[1]+r.normal(0,30))
        P=lambda q:(lerp(a[0],b[0],q),lerp(a[1],b[1],q)-math.sin(q*math.pi)*160)
        X,Y=c.p(*P(ph));X2,Y2=c.p(*P(max(0,ph-.04)))
        cv2.line(cv,(int(X2),int(Y2)),(int(X),int(Y)),tuple(float(v) for v in INK),2,cv2.LINE_AA)
def rnuoc(cv,c,key,x0,y0,t,t0,dx,wl,s=.34):
    if t<t0: return
    u=(t-t0)/1.0
    if u<1: rig.ve23(cv,c,key,x0+dx*u,y0+(wl-y0)*u*u-50*math.sin(u*math.pi),s,rig.so(t,1.3),flip=dx<0)
    elif not FREEZE:
        X,Y=c.p(x0+dx,wl+6);k=min(1,(u-1)*1.4)
        if k<1: cv2.ellipse(cv,(int(X),int(Y)),(int(16+60*k),int(4+9*k)),0,0,360,tuple(float(v) for v in INK*(1-k)+PAPER*k),2,cv2.LINE_AA)
def sp(t,a,b,p0,p1): return p0 if FREEZE else tuple(lerp(p0[i],p1[i],inn(t,a,max(.1,b-a))) for i in range(3))
def tieude(cv,t,t0,t1,s1,s2=None,col=None):
    nhan(cv,s1,960,150,t,t0,t1,col if col is not None else INK,40)
# 1: lời dọa giữa biển động
def S_1(cv,t):
    a,b=0,E[1]+.3;q=sb(1,1)
    tranh(cv,'bien_b',t,a,b,(512,560,1.0),(560,600,1.15))
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,560,1.12))])
    for i in range(2): tthuyen(cv,c,260+i*300+40*math.sin(t*.4+i),640+i*20,t,.34,True,False,[(MA[i],-60,None)],ph=i,o=.7)
    tthuyen(cv,c,1080,780,t,.78,True,False,[('omn6',-90,'quat' if t>q-.5 else None),('m7',80,'dam'),('m8',170,None)],ph=2)
    tong(cv,.42);suong2(cv,t,640,.35,40)
    if t>q: soi(cv,c,1010,520,t,.8)
    nhan(cv,'ngươi chạy lên trời, ta theo lên trời',960,170,t,q,b,RED,44)
# 2: lời dọa chép trong thư nhà Trần
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3;q=sb(2,1)
    c=kc(t,[(a,(960,620,1.05)),(b,(1000,600,1.15))])
    nen(cv,c,t,seed=2,mist=.5)
    put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9,o=.6)
    ngd(cv,c,'omn6',1450,905,t,.72,rig.quat(t)|{'mat':'G'},flip=True)
    for i in range(2): ngd(cv,c,MA[i],1650+i*130,905,t,.6,rig.dung(t+i),flip=True,vk='giao')
    truoc(cv,c,t);tong(cv,.3)
    cuon(cv,700,470,t,'THƯ NHÀ TRẦN','kể tội|Ô Mã Nhi',col=RED,s=.78,sz=42,u=inn(t,a+.4,1.8),nm='t26n_cuon2')
    nhan(cv,'Ô Mã Nhi · tướng chỉ huy thủy quân nhà Nguyên',960,1000-900,t,q,b,INK,36)
# 3: bị giải tới trước lăng
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3
    mp=tranh(cv,'mo_a',t,a,b,(512,560,1.0),(512,600,1.18));ngua_da(cv,mp,t)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,600,1.12))])
    x=dib(cv,c,'omn6',820,960,960,t,a,b,s=.5,sua=lambda PP,t_:PP.update(lean=12,head=10,arF=10,faF=-80,arB=0,faB=-80,mat='S'),chay=.4,buoc=36)
    for i,dx in enumerate([-170,150]): dib(cv,c,VA[i],820+dx,960+dx,975,t,a,b,s=.52,vk='giao',chay=.4,buoc=36,ph=i)
    chim(cv,c,t,200,220,4,30)
    tong(cv,.5);suong2(cv,t,760,.35,25)
# 4: câu hỏi
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.6
    tranh(cv,'song_hoa',t,a,b,(512,520,1.0),(540,540,1.1))
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.05))])
    for i in range(3): tthuyen(cv,c,500+i*360+60*(t-a),640+i*14,t,.26,False,i%2==1,[('v8',-30,'cheo')],ph=i,o=.6)
    chim(cv,c,t,300,260,5,45,1)
    tong(cv,.5);suong2(cv,t,560,.5,35)
    nhan(cv,'chuyện gì đã xảy ra?',960,260,t,a+.2,b,RED,50)
# 5: bản đồ: quân Nguyên thiếu lương, thuyền lương bị chặn ở Vân Đồn
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3
    vk,vd,tl=tuple(PTM['vankiep']),tuple(PTM['vandon']),tuple(PTM['thanglong'])
    c=mcam(t,[(a,(620,580,1.6)),(b,(640,600,1.9))])
    bando(cv,c,t,a)
    diem(cv,c,'Thăng Long',tl,t,a+.2,MONGC,dx=-26,dy=-18);diem(cv,c,'Vạn Kiếp',vk,t,a+.4,MONGC,dx=24,dy=-20)
    for j,p in enumerate([tl,vk]):
        for k in range(3): put(cv,c,'t27_spr_coN',p[0]-14+k*14,p[1]+4+2*math.sin(t*3+k+j),s=.08,ay=1)
    ps=[(1000,640),(860,615),vd];duong(cv,c,ps,t,a+.6,1.5,(.5,.4,.3),4)
    for j in range(3): cotheo(cv,c,'t23n_thuyenlon',ps,t,a+.6+j*.3,b-a,s=.09,ph=j)
    if t>a+2.2:
        diem(cv,c,'Vân Đồn',vd,t,a+2.2,RED,dx=24,dy=-16);pulse(cv,c,*vd,t)
        put(cv,c,band(46,7,RED,.9,1),vd[0],vd[1]+18,r=40);put(cv,c,band(46,7,RED,.9,1),vd[0],vd[1]+18,r=-40)
    nhan(cv,'đầu năm 1288 · quân Nguyên bắt đầu thiếu lương',960,150,t,a+.3,b,MONGC,38)
# 6: dẫn sang video trước
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3
    tranh(cv,'bien_a',t,a,b,(512,560,1.0),(520,580,1.1))
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.06))])
    for i in range(4): put(cv,c,'t26n_gao',420+i*300+30*math.sin(t*.6+i),700+i*18+6*math.sin(t+i),s=.22,r=30*i+15*math.sin(t*.5+i),o=.85)
    tthuyen(cv,c,1350+40*math.sin(t*.3),640,t,.4,False,True,[('tkd',20,None),('v8',-50,'cheo')])
    tong(cv,.45)
    if not FREEZE:
        u=inn(t,a+.4,.6)*(1-inn(t,b-.5,.4));put_screen(cv,band(900,150,PAPER,.88*u,30),960,300)
        put_screen(cv,text('VIDEO TRƯỚC',34,INK,700),960,262,u);put_screen(cv,text('Thuyền lương ở Vân Đồn',54,RED,700),960,318,u)
# 7: Thăng Long bỏ trống
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3;q=sb(7,1)
    c=kc(t,[(a,(900,620,1.1)),(q,(1000,640,1.2)),(b,(1100,650,1.3))])
    nen(cv,c,t,seed=7,mist=.6)
    put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9)
    x=dib(cv,c,'thn6',300,900,905,t,a,q+1,s=.7,vk='dao',sua=lambda PP,t_:PP.update(mat='S' if t_>q+.6 else ''))
    for i in range(4): dib(cv,c,MA[i%3],60-i*150,640-i*130,905+(i%2)*10,t,a+.2,q+1.2,s=.6,vk='giao',ph=i)
    for i in range(3): put(cv,c,'t12_spr_chim',1200+i*80+((t*60)%300),300-i*20,s=.12)
    truoc(cv,c,t);tong(cv,.35)
    nhan(cv,'Thăng Long · cung điện vắng tanh',960,170,t,q,b,INK,42)
# 8: đuổi tới cửa biển Thiên Trường
def S_8(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1)
    tranh(cv,'bien_a',t,a,b,(470,560,1.0),(560,600,1.15))
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,560,1.1))])
    tthuyen(cv,c,700,700,t,.62,True,False,[('thn6',-60,None),('m7',90,None)],ph=1)
    if t>q:
        P=ngam(rig.dung(t));P['mat']='G'
    for i in range(3): tthuyen(cv,c,260-i*160+40*(t-a),640+i*10,t,.3,True,False,[(MA[i],-40,None)],ph=i,o=.7)
    tong(cv,.42);suong2(cv,t,600,.3,50)
    nhan(cv,'cửa biển Thiên Trường',960,170,t,a+.3,q,INK,44);nhan(cv,'chỉ còn sóng biển mênh mông',960,170,t,q+.2,b,INK,40)
# 9: lùng sục tìm thóc gạo
def S_9(cv,t):
    a,b=T[9]-.3,E[9]+.3
    mp=tranh(cv,'dong_b',t,a,b,(560,640,1.0),(580,660,1.12))
    c=kc(t,[(a,(960,540,1.0)),(b,(960,540,1.0))])
    ps=[mp(*p)[:2] for p in [(540,1020),(520,850),(560,700),(640,620),(710,560),(745,500)]];k=mp(0,0)[2]
    for i in range(14):
        u=((i/14)+(t-a)*.03)%1.0;x,y=theo(ps,u);s=lerp(.75,.08,u**.6)*k
        linhsau(cv,c,i,x+(i%2-.5)*50*s,y,s,t,o=lerp(1,.6,u))
    tong(cv,.5);suong2(cv,t,560,.35,30)
    nhan(cv,'kho lương trống rỗng · lùng sục khắp các làng',960,170,t,a+.3,b,MONGC,38)
# 10: thủy quân lùng ven biển; thư kể tội
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3;q=sb(10,1)
    tranh(cv,'song_b',t,a,b,(512,560,1.0),(470,580,1.12))
    c=kc(t,[(a,(960,560,1.0)),(b,(940,560,1.08))])
    for i in range(3): tthuyen(cv,c,1500-i*330-80*(t-a),560+i*30,t,.42+.04*i,True,True,[(MA[i],-90,'dam'),('omn6' if i==1 else MA[(i+1)%3],60,'quat' if i==1 else None)],ph=i)
    for i in range(3): chay(cv,c,'d6c' if i%2 else 'd6a',300+i*120,-200+i*80,940+(i%2)*15,t,q-.5+i*.2,b+1,.55,lambda ph,tt:rig.hoang(ph,tt,1.0),ph=i)
    tong(cv,.45)
    nhan(cv,'thư nhà Trần kể tội · giết và bắt dân ven biển',960,150,t,q+.1,b,RED,38)
# 11: bản đồ: Ô Mã Nhi đánh vào phủ Long Hưng
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3
    lh,vk,bd=tuple(PTM['longhung']),tuple(PTM['vankiep']),tuple(PTM['bachdang'])
    c=mcam(t,[(a,(560,660,2.2)),(b,(540,690,2.6))])
    bando(cv,c,t,a)
    ps=[bd,(590,690),(560,715),lh];duong(cv,c,ps,t,a+.3,b-a-1.2,MONGC,4)
    for j in range(3): cotheo(cv,c,'t23n_thuyen',ps,t,a+.3+j*.25,b-a-.6,s=.11,ph=j)
    if t>a+2: diem(cv,c,'phủ Long Hưng',lh,t,a+2,RED,dx=24,dy=12);pulse(cv,c,*lh,t)
    nhan(cv,'tháng giêng · quê gốc của họ Trần',960,150,t,a+.4,b,INK,40)
# 12: Chiêu Lăng, ngựa đá đứng chầu
def S_12(cv,t):
    a,b=T[12]-.3,E[12]+.3;q=sb(12,1)
    mp=tranh(cv,'mo_a',t,a,b,(512,500,1.0),(300,560,1.6) if t>q else (512,520,1.08));ngua_da(cv,mp,t)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.04))])
    chim(cv,c,t,250,200,5,25,2)
    for k in range(3): put(cv,c,band(220,60,PAPER,.35,30),300+((t*30+k*400)%1400),420+k*50)
    tong(cv,.3)
    nhan(cv,'Chiêu Lăng · lăng vua Trần Thái Tông',960,170,t,a+.3,q,INK,42);nhan(cv,'những con ngựa đá đứng chầu',960,170,t,q+.2,b,INK,40)
# 13: quân Nguyên đào bới Chiêu Lăng
def S_13(cv,t):
    a,b=T[13]-.3,E[13]+.3;q=sb(13,1)
    mp=tranh(cv,'mo_a',t,a,b,(512,560,1.25),(512,560,1.4));ngua_da(cv,mp,t)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,600,1.1))])
    for i in range(5):
        x=520+i*210;P=rig.dung(t+i);sw=math.sin(t*5+i*1.7);P.update(arF=-150+80*max(0,sw),faF=-10,lean=20*max(0,sw),mat='G')
        ngd(cv,c,MA[i%3],x,940+(i%2)*14,t,.5,P,flip=i%2==1,vk='gay')
        if not FREEZE and sw>.8: bui(cv,c,x+(-40 if i%2 else 40),950,t,t-.1,n=2,s=.3)
    tong(cv,.45)
    nhan(cv,'đào mà vẫn không phạm được tới quan tài',960,170,t,q,b,RED,40)
# 14: bản đồ: rút về hai ngả
def S_14(cv,t):
    a,b=T[14]-.3,E[15]+.3;q=T[15]
    vk,bd,ls,tl=tuple(PTM['vankiep']),tuple(PTM['bachdang']),tuple(PTM['langson']),tuple(PTM['thanglong'])
    c=mcam(t,[(a,(600,560,2.0)),(b,(590,520,2.1))])
    bando(cv,c,t,a)
    diem(cv,c,'Vạn Kiếp',vk,t,a,MONGC,dx=-24,dy=-20)
    s1=[vk,(560,610),bd,(680,660)];duong(cv,c,s1,t,a+.4,2.4,MONGC,5)
    for j in range(4): cotheo(cv,c,'t23n_thuyen',s1,t,a+.4+j*.25,q-a,s=.11,ph=j)
    nhan(cv,'Ô Mã Nhi, Phàn Tiếp · thủy quân về trước theo đường sông',960,150,t,a+.3,q,MONGC,36)
    if t>q:
        s2=[tl,vk,(560,520),ls];duong(cv,c,s2,t,q,2.4,MONGC,5)
        for j in range(4): cotheo(cv,c,'t27_spr_coN',s2,t,q+j*.3,b-q,s=.16,ph=j)
        diem(cv,c,'Lạng Sơn',ls,t,q+.8,MONGC,dx=24,dy=-10)
        nhan(cv,'Thoát Hoan · đại quân theo đường bộ',960,150,t,q+.2,b,MONGC,38)
# 15: sông Bạch Đằng, nơi Ngô Quyền thắng năm 938
def S_15(cv,t):
    a,b=T[16]-.3,E[16]+.3;q=sb(16,1)
    vk,bd=tuple(PTM['vankiep']),tuple(PTM['bachdang'])
    c=mcam(t,[(a,(580,620,2.6)),(b,(600,630,3.0))])
    bando(cv,c,t,a)
    s1=[vk,(560,610),bd,(660,660)];duong(cv,c,s1,t,a+.3,2.0,MONGC,4)
    for j in range(3): cotheo(cv,c,'t23n_thuyen',s1,t,a+.3+j*.25,b-a,s=.1,ph=j)
    diem(cv,c,'sông Bạch Đằng',bd,t,a+1.0,RED,dx=24,dy=24);pulse(cv,c,*bd,t)
    nhan(cv,'năm 938 · Ngô Quyền nhấn chìm thủy quân Nam Hán',960,150,t,q+.1,b,VIETC,38)
# 16: Hưng Đạo Vương cho đóng cọc
def S_16(cv,t):
    a,b=T[17]-.3,E[17]+.3;q=sb(17,1)
    tranh(cv,'song_b',t,a,b,(512,600,1.05),(540,640,1.15))
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,580,1.1))])
    wl=640
    for i in range(5):
        x=360+i*170;P=rig.dung(t+i);sw=abs(math.sin(t*4+i*1.3));P.update(arF=-160+70*sw,faF=-10,arB=-150+70*sw,faB=-10,lean=8*sw,mat='G')
        ngd(cv,c,VA[i%3],x,820,t,.48,P,flip=i%2==1,vk='gay')
    coc(cv,c,t,760,0,14)
    ngd(cv,c,'hdv6',1450,860,t,.6,rig.quat(t)|{'mat':''},flip=True,vk='dao')
    co(cv,c,'t27_spr_coV',1600,840,t,s=.5)
    tong(cv,.4)
    nhan(cv,'Hưng Đạo Vương Trần Quốc Tuấn',960,170,t,a+.3,q,VIETC,42);nhan(cv,'đóng cọc gỗ · lấy cỏ phủ kín đầu cọc',960,170,t,q+.2,b,INK,40)
# 17: sơ đồ vì sao lại là cọc (thủy triều lên, rút)
def S_17(cv,t):
    a,b=T[18]-.3,E[21]+.3;q=T[20]
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.04))])
    nen(cv,c,t,'song',seed=17,mist=.2)
    put(cv,c,band(2200,700,PAPER,.9,30),960,600)
    hi,lo=430,610
    wl=hi if t<q else lerp(hi,lo,inn(t,q,2.5))
    if not FREEZE:
        X0,Yw=c.p(0,wl);_,Yb=c.p(0,860)
        ov=cv.copy();cv2.rectangle(ov,(0,int(Yw)),(1920,int(Yb)),tuple(float(v) for v in INK*.35+PAPER*.65),-1);cv[:]=cv*.45+ov*.55
        cv2.rectangle(cv,(0,int(Yb)),(1920,1080),tuple(float(v) for v in INK*.6+PAPER*.4),-1)
        for k in range(6): cv2.line(cv,(int(((t*80+k*330)%2200)-200),int(Yw+8)),(int(((t*80+k*330)%2200)-60),int(Yw+8)),tuple(float(v) for v in INK*.7+PAPER*.3),2,cv2.LINE_AA)
    for i in range(9):
        x=520+i*110;X0,Y0=c.p(x,860);X1,Y1=c.p(x,640)
        if not FREEZE: cv2.fillPoly(cv,[np.int32([[X0-12,Y0],[X0+12,Y0],[X1+6,Y1+20],[X1,Y1-10],[X1-6,Y1+20]])],tuple(float(v) for v in INK),cv2.LINE_AA)
    bx=lerp(200,900,inn(t,a+.5,q-a-1)) if t<q else 900;by=wl-10+(0 if t<q else 0)
    stuck=t>q+2.0
    tthuyen(cv,c,bx+(0 if not stuck else 0),min(by,640) if stuck else by,t,.6,True,True,[('m8',-60,'so' if stuck else None),('m7',60,'so' if stuck else None)],nghieng=12*inn(t,q+1.8,1.2))
    nhan(cv,'thủy triều dâng · nước che kín bãi cọc',960,150,t,a+.3,q,INK,40)
    nhan(cv,'thủy triều rút · đầu cọc nhô lên',960,150,t,q+.2,b,RED,40)
    if t>sb(21,0) and not FREEZE: put_screen(cv,text('như con thú sa vào bẫy',44,RED,700),960,980,inn(t,sb(21,0),.6))
# 18: mai phục hai bên bờ
def S_18(cv,t):
    a,b=T[22]-.3,E[22]+.3;q=sb(22,1)
    tranh(cv,'song_b',t,a,b,(300,700,1.25),(420,700,1.3))
    c=kc(t,[(a,(960,560,1.0)),(b,(980,560,1.06))])
    for i in range(4):
        P=rig.dung(t+i);P.update(lean=18,head=6,mat='G',thF=-40,knF=60,thB=-20,knB=50)
        ngd(cv,c,VA[i%3],300+i*200,900+(i%2)*20,t,.55,P,vk='giao')
    for i in range(3): tthuyen(cv,c,1300+i*200,780+i*20,t,.4,False,True,[('v9',-30,None),('v10',40,None)],ph=i)
    tong(cv,.45);suong2(cv,t,700,.35,20)
    nhan(cv,'quân Đại Việt mai phục dọc hai bên bờ',960,170,t,q-.5,b,VIETC,40)
# 19: Hưng Đạo Vương qua sông Hóa
def S_19(cv,t):
    a,b=T[23]-.3,E[23]+.3;q=sb(23,1)
    tranh(cv,'song_hoa',t,a,b,(512,600,1.0),(500,620,1.12))
    c=kc(t,[(a,(960,560,1.0)),(b,(900,580,1.1))])
    for i in range(6): dib(cv,c,VA[i%3],-200-i*120,300+i*110,900+(i%2)*14,t,a,q,s=.5,vk='giao',ph=i)
    for i in range(3): co(cv,c,'t27_spr_coV',150+i*240,880,t,s=.45,ph=i)
    P=rig.quat(t) if t>q else rig.dung(t);P['mat']='G' if t>q else ''
    ngd(cv,c,'hdv6',1250,900,t,.62,P,vk='dao')
    tong(cv,.4);suong2(cv,t,620,.35,25)
    nhan(cv,'sông Hóa',960,170,t,a+.3,q,INK,44)
# 20: lời thề
def S_20(cv,t):
    a,b=T[24]-.3,E[25]+.3;q=T[25]
    tranh(cv,'song_hoa',t,a,b,(620,640,1.3),(640,650,1.45))
    c=kc(t,[(a,(1150,620,1.45)),(q,(1100,620,1.55)),(b,(900,640,1.1))])
    ngd(cv,c,'hdv6',1250,900,t,.66,rig.quat(t)|{'mat':'G','arF':-95},vk='dao')
    soi(cv,c,1250,700,t,.8)
    for i in range(6): ngd(cv,c,VA[i%3],500+i*110,920+(i%2)*14,t,.5,(rig.reo(t+i) if t>q else rig.dung(t+i)),vk='giao')
    tong(cv,.38)
    nhan(cv,'không phá tan được giặc Nguyên thì không trở về con sông này nữa',960,160,t,a+.4,q+.4,RED,36)
# 21: thủy triều lên, Ô Mã Nhi vào sông
def S_21(cv,t):
    a,b=T[26]-.3,E[27]+.3;q=T[27]
    tranh(cv,'bd_trieu',t,a,b,(560,500,1.0),(500,520,1.1))
    c=kc(t,[(a,(960,540,1.0)),(b,(940,540,1.06))])
    for i,(x,y,s) in enumerate([(1500,640,.5),(1150,670,.56),(1800,700,.6),(820,620,.42)]):
        tthuyen(cv,c,x-240*inn(t,a,b-a),y,t,s,True,True,[(MA[i%3],-90,None),('omn6' if i==1 else MA[(i+1)%3],60,'quat' if i==1 else None)],ph=i)
    tong(cv,.42);suong2(cv,t,560,.3,35)
    nhan(cv,'ngày mồng tám tháng ba năm Mậu Tý',960,170,t,a+.3,q,INK,40);nhan(cv,'thủy triều lên cao · bãi cọc chìm dưới làn nước',960,170,t,q+.2,b,INK,38)
# 22: khiêu chiến rồi giả thua
def S_22(cv,t):
    a,b=T[28]-.3,E[29]+.3;q=T[29]
    sh=4*math.sin(t*40) if a+1.5<t<a+2.1 and not FREEZE else 0
    tranh(cv,'bd_trieu',t,a,b,(500,560,1.15),(470,560,1.2))
    c=kc(t,[(a,(960,560,1.0)),(b,(900,560,1.05))],sh)
    for i,(x,y) in enumerate([(1350,640),(1650,690)]): tthuyen(cv,c,x,y,t,.56,True,True,[(MA[i],-90,'dam'),(MA[i+1],60,'dam')],ph=i)
    back=inn(t,q,b-q)
    for i in range(3):
        x=lerp(-200+i*120,900+i*90,inn(t,a,1.6))-900*back;fl=back>0
        tthuyen(cv,c,x,760+i*30,t,.46,False,fl,[('v9',-40,'cheo'),(VA[i%3],40,'dam' if not fl else None)],ph=i)
    if a+1.4<t<q: tenbay(cv,c,t,(1300,600),(800,700),7,2);tenbay(cv,c,t,(700,740),(1350,620),6,3)
    tong(cv,.42)
    nhan(cv,'toán thuyền Đại Việt khiêu chiến',960,170,t,a+.3,q,VIETC,40);nhan(cv,'rồi quay thuyền bỏ chạy',960,170,t,q+.2,b,INK,42)
# 23: Ô Mã Nhi đuổi theo, hiểm họa dưới mặt nước
def S_23(cv,t):
    a,b=T[30]-.3,E[31]+.3;q=T[31]
    tranh(cv,'bd_trieu',t,a,b,(620,540,1.1),(380,560,1.2))
    c=kc(t,[(a,(1150,560,1.2)),(q,(960,560,1.0)),(b,(900,560,1.0))])
    for i,(x,y,s) in enumerate([(1500,650,.62),(1850,700,.66),(1200,620,.5)]):
        tthuyen(cv,c,x-700*inn(t,a,b-a),y,t,s,True,True,[('omn6' if i==0 else MA[i],-90,'quat' if i==0 else None),(MA[(i+1)%3],60,'dam')],ph=i)
    for i in range(2): tthuyen(cv,c,500-500*inn(t,a,b-a)-i*200,760+i*20,t,.42,False,True,[('v9',-40,'cheo')],ph=i)
    if t>q and not FREEZE:
        ov=cv.copy()
        for k in range(14): X,Y=c.p(300+k*90,770+(k%3)*10);cv2.line(ov,(int(X),int(Y+40)),(int(X+4),int(Y)),tuple(float(v) for v in INK),8,cv2.LINE_AA)
        u=.22*inn(t,q,1);cv[:]=cv*(1-u)+ov*u
    tong(cv,.42)
    nhan(cv,'hiểm họa vẫn nằm im dưới mặt nước',960,170,t,q+.2,b,RED,40)
# 24: thủy triều rút, cọc nhô lên
def S_24(cv,t):
    a,b=T[32]-.3,E[33]+.3;q=T[33]
    tranh(cv,'song_a',t,a,b,(512,600,1.0),(512,630,1.08))
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.08))])
    wl=lerp(560,640,inn(t,a+.5,b-a-1))
    for i,(x,ph,dy) in enumerate([(520,0,20),(1000,1.3,60),(1440,2.1,0)]):
        tthuyen(cv,c,x+40*(1-inn(t,a,2)),wl+dy-30,t,.5,True,True,[('omn6' if i==1 else 'm8',-110,None),('m7',40,None)],ph=ph,nghieng=6*inn(t,q,2)*[1,-1,1][i])
    coc(cv,c,t,wl)
    tong(cv,.45)
    nhan(cv,'thủy triều rút · mặt sông hạ thấp',960,170,t,a+.3,q,INK,40);nhan(cv,'cái bẫy bắt đầu phát huy tác dụng',960,170,t,q+.2,b,RED,40)
def tran_lon(cv,c,t,a,tilt,dong,wl):
    for i,(x,ph,dy) in enumerate([(520,0,20),(1000,1.3,60),(1440,2.1,0)]):
        ng=[('omn6' if i==1 else 'm8',-110,'so' if tilt>.3 else 'quat'),('m7',40,'so' if tilt>.5 else 'dam'),('m9',130,'so' if tilt>.6 else None)]
        tthuyen(cv,c,x,wl+dy-30+14*tilt,t,.5,True,True,ng,ph=ph,nghieng=tilt*[10,-13,8][i])
    coc(cv,c,t,wl)
    for i in range(int(6*dong)):
        j=i//2;u=inn(t,a+i*.2,2.5)
        x=lerp(-300-j*120,330+j*300,u) if i%2==0 else lerp(2250+j*120,1640-j*290,u)
        tthuyen(cv,c,x,wl+120+j*50,t,.44+j*.04,False,i%2==1,[('v9',-50,'cheo'),(VA[i%3],40,'dam')],ph=i)
# 25: quân Đại Việt đồng loạt đổ ra, trống trận
def S_25(cv,t):
    a,b=T[34]-.3,E[35]+.3;q=T[35]
    sh=3*math.sin(t*37) if not FREEZE and int(t*2.2)%2==0 else 0
    tranh(cv,'song_a',t,a,b,(512,630,1.08),(512,640,1.15))
    c=kc(t,[(a,(960,560,1.0)),(b,(980,570,1.08))],sh)
    tran_lon(cv,c,t,a,.25*inn(t,q,2),1.0,640)
    tthuyen(cv,c,260,880,t,.5,False,False,[('v10',-40,'trong'),('v9',50,'reo')])
    tenbay(cv,c,t,(400,700),(1000,580),9,3);tenbay(cv,c,t,(1650,720),(1150,590),7,4)
    tong(cv,.4)
    nhan(cv,'tiếng trống trận vang dậy hai bên bờ',960,170,t,a+.3,q,VIETC,40);nhan(cv,'đường rút đã bị những hàng cọc chắn ngang',960,170,t,q+.2,b,RED,38)
# 26: mắc cọc, hỗn loạn, rơi xuống nước
def S_26(cv,t):
    a,b=T[36]-.3,E[38]+.3;q=T[37];r=T[38]
    tranh(cv,'song_a',t,a,b,(512,640,1.15),(560,650,1.3))
    c=kc(t,[(a,(960,580,1.05)),(q,(1000,600,1.2)),(b,(960,580,1.1))])
    tilt=.4+.6*inn(t,a,3)
    tran_lon(cv,c,t,a-3,tilt,1.0,640)
    for k,(x,t0,dx) in enumerate([(1000,q+.2,90),(520,q+1.0,-80),(1440,q+1.8,70),(1050,r+.2,-60),(560,r+1,60)]):
        rnuoc(cv,c,['m7','m8','m9','m7','m8'][k],x,560,t,t0,dx,640)
    tenbay(cv,c,t,(400,720),(1000,590),7,5)
    tong(cv,.4)
    nhan(cv,'trước mặt là quân Đại Việt · phía sau là bãi cọc',960,170,t,a+.3,q,INK,38);nhan(cv,'chết đuối rất nhiều',960,170,t,q+.3,r,RED,42);nhan(cv,'bị chính dòng sông dồn vào đường cùng',960,170,t,r+.2,b,RED,40)
# 27: chập tối, hơn bốn trăm thuyền
def S_27(cv,t):
    a,b=T[39]-.3,E[40]+.3;q=T[40]
    tranh(cv,'bd_chieu',t,a,b,(512,560,1.0),(512,580,1.12))
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.06))])
    for i,(x,y,r) in enumerate([(500,690,14),(900,710,-18),(1350,680,10),(1700,720,-8)]):
        tthuyen(cv,c,x,y,t,.4,True,True,[],nghieng=r,o=.85)
    for i in range(4): tthuyen(cv,c,300+i*400+40*(t-a),800+(i%2)*30,t,.4,False,False,[('v9',-40,'cheo'),(VA[i%3],40,'reo')],ph=i)
    for i in range(4): put(cv,c,'t27_spr_coV',380+i*400+40*(t-a),760+(i%2)*30,s=.22,ay=1,r=3*math.sin(t*2+i))
    tong(cv,.5);chim(cv,c,t,300,260,5,30,3)
    nhan(cv,'đánh tới chập tối · bắt hơn bốn trăm thuyền',960,170,t,a+.4,q,VIETC,40);nhan(cv,'Bạch Đằng · nơi chôn vùi tham vọng xâm lược',960,170,t,q+.2,b,RED,38)
# 28: Đỗ Hành bắt sống Ô Mã Nhi
def S_28(cv,t):
    a,b=T[41]-.3,E[41]+.3;q=sb(41,1) if len(_SC[41])>2 else a+(b-a)*.5
    c=kc(t,[(a,(900,600,1.3)),(b,(960,620,1.45))])
    nen(cv,c,t,seed=28,mist=.4)
    tthuyen(cv,c,1350,760,t,.5,True,True,[],nghieng=8,o=.85)
    ngd(cv,c,'dh7',820,960,t,.62,rig.quat(t)|{'mat':'G','arF':-70},vk='dao')
    ngd(cv,c,'omn6',1050,960,t,.6,quy(rig.so(t,1.0)))
    ngd(cv,c,'tlc',1230,960,t,.58,quy(rig.so(t+.5,1.0)))
    for i in range(2): ngd(cv,c,VA[i],600-i*120,970,t,.56,rig.dung(t+i)|{'mat':'V'},vk='giao')
    tong(cv,.3)
    nhan(cv,'Đỗ Hành bắt sống Ô Mã Nhi và Tích Lệ Cơ',960,170,t,a+.3,b,VIETC,40)
# 29: lên thuyền ngự cùng ngồi nói chuyện
def S_29(cv,t):
    a,b=T[42]-.3,E[42]+.3;q=sb(42,1)
    c=kc(t,[(a,(960,600,1.2)),(q,(1000,620,1.45)),(b,(1000,620,1.55))])
    nen(cv,c,t,seed=29,mist=.4)
    tthuyen(cv,c,1000,820,t,.72,True,False,[('tts6',-120,None),('omn6',60,None)])
    for i in range(2): ngd(cv,c,'lh6',460-i*130,1000,t,.56,rig.dung(t+i),vk='giao')
    tong(cv,.28)
    nhan(cv,'thượng hoàng cho lên thuyền ngự, cùng ngồi nói chuyện',960,170,t,a+.3,q,INK,38)
    nhan(cv,'người từng dọa đuổi vua lên trời xuống nước',960,170,t,q+.2,b,RED,38)
# 30: Phàn Tiếp bị bắt, đoàn chiến thuyền tan tác
def S_30(cv,t):
    a,b=T[43]-.3,E[43]+.3
    tranh(cv,'bd_chieu',t,a,b,(600,600,1.2),(640,610,1.3))
    c=kc(t,[(a,(960,560,1.0)),(b,(980,560,1.05))])
    for i,(x,y,r) in enumerate([(700,720,20),(1200,700,-24)]): tthuyen(cv,c,x,y,t,.45,True,True,[],nghieng=r,o=.8)
    for i in range(3): put(cv,c,'t27_spr_coN',500+i*420+20*math.sin(t+i),760+10*math.sin(t*1.3+i),s=.25,ay=1,r=70+10*math.sin(t+i),o=.8)
    tthuyen(cv,c,1000+30*(t-a),850,t,.5,False,False,[('ptp',-30,'so'),('v10',50,None)])
    tong(cv,.45)
    nhan(cv,'Phàn Tiếp cũng bị bắt · đoàn chiến thuyền tan tác',960,170,t,a+.3,b,INK,38)
# 31: ngả đường bộ: Thoát Hoan rút qua núi
def S_31(cv,t):
    a,b=T[44]-.3,E[44]+.3;q=sb(44,1)
    mp=tranh(cv,'deo_a',t,a,b,(420,700,1.0),(380,720,1.12))
    c=kc(t,[(a,(960,540,1.0)),(b,(960,540,1.0))])
    pts=[mp(*p)[:2] for p in [(360,1060),(300,960),(250,860),(232,790),(250,745)]];k=mp(0,0)[2]
    for i in range(16):
        u=((i/16)+(t-a)*.03)%1.0;x,y=theo(pts,u);s=lerp(.7,.1,u**.6)*k
        linhsau(cv,c,i,x+(i%2-.5)*50*s,y,s,t,o=lerp(1,.6,u))
    X,Y,_=mp(640,900)
    ngua(cv,c,'nau','thn6',X+500,X,Y,t,a,b,s=.5*k,flip=True)
    tong(cv,.45)
    nhan(cv,'ải Nội Bàng · quân Đại Việt chờ sẵn hai bên vách núi',960,150,t,q,b,RED,38)
# 32: ải Nội Bàng, Trương Quân chặn phía sau
def S_32(cv,t):
    a,b=T[45]-.3,E[45]+.3;q=sb(45,1) if len(_SC[45])>2 else a+(b-a)*.5
    sh=3*math.sin(t*41) if not FREEZE and int(t*3)%3==0 else 0
    tranh(cv,'deo_d',t,a,b,(512,620,1.0),(512,660,1.12))
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.08))],sh)
    tenbay(cv,c,t,(200,420),(900,860),9,7);tenbay(cv,c,t,(1750,400),(1100,860),9,8)
    for i in range(4):
        P=rig.xung(t*6+i);P['mat']='G';ngd(cv,c,MA[i%3] if i else 'tqn',820+i*90,900+(i%2)*14,t,.46,P,flip=True,vk='daocong' if i else 'dao')
    for i in range(3): chay(cv,c,MA[i],900+i*80,1500+i*80,930,t,a+.3+i*.3,b,.44,lambda ph,tt:rig.hoang(ph,tt,1.1),ph=i)
    tong(cv,.42)
    nhan(cv,'Trương Quân dẫn ba nghìn quân tinh nhuệ chặn phía sau',960,150,t,a+.3,b,MONGC,36)
# 33: thám báo hớt hải về báo tin
def S_33(cv,t):
    a,b=T[46]-.3,E[46]+.3;q=sb(46,1)
    tranh(cv,'rung_a',t,a,b,(512,640,1.05),(512,600,1.15))
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,580,1.12))])
    chay(cv,c,'m9',-100,1050,930,t,a,q,.5,lambda ph,tt:rig.hoang(ph,tt,1.2))
    ngua(cv,c,'nau','thn6',1400,1350,930,t,a,b,s=.6,flip=True,sua=lambda PP,t_:PP.update(mat='S' if t_>q else ''))
    for i in range(3): ngd(cv,c,MA[i],1650+i*100,930,t,.48,rig.dung(t+i)|({'mat':'S'} if t>q else {}),flip=True,vk='giao')
    tong(cv,.42)
    nhan(cv,'hơn ba mươi vạn quân · nối dài hơn trăm dặm',960,150,t,q,b,RED,38)
# 34: bản đồ: đường tắt về Tư Minh
def S_34(cv,t):
    a,b=T[47]-.3,E[47]+.3
    ls=tuple(PTM['langson']);tm=(650,330);lc=(632,420)
    c=mcam(t,[(a,(600,440,2.2)),(b,(620,410,2.5))])
    bando(cv,c,t,a)
    diem(cv,c,'Lạng Sơn',ls,t,a,INK,dx=-24,dy=14)
    big_=[(540,520),ls,(600,380),tm];duong(cv,c,big_,t,a,.3,(.5,.5,.5),3)
    put(cv,c,band(46,7,RED,.9,1),600,400,r=40);put(cv,c,band(46,7,RED,.9,1),600,400,r=-40)
    tat=[(540,520),(570,470),lc,(655,380),tm];duong(cv,c,tat,t,a+.6,b-a-1.2,MONGC,4)
    for j in range(3): cotheo(cv,c,'t27_spr_coN',tat,t,a+.6+j*.3,b-a-.4,s=.14,ph=j)
    diem(cv,c,'Lộc Châu',lc,t,a+1.5,MONGC,dx=24,dy=0);diem(cv,c,'Tư Minh',tm,t,b-2,MONGC,dx=24,dy=-10)
    nhan(cv,'bỏ đường lớn · len lỏi theo đường tắt qua Đan Kỷ, Lộc Châu',960,150,t,a+.3,b,MONGC,34)
# 35: cả hai ngả đều có quân chờ
def S_35(cv,t):
    a,b=T[48]-.3,E[48]+.3
    vk,bd,ls=tuple(PTM['vankiep']),tuple(PTM['bachdang']),tuple(PTM['langson'])
    c=mcam(t,[(a,(600,540,1.8)),(b,(600,540,1.9))])
    bando(cv,c,t,a)
    duong(cv,c,[vk,(560,610),bd],t,a,.3,MONGC,4);duong(cv,c,[vk,(560,520),ls],t,a,.3,MONGC,4)
    for p,t0 in [(bd,a+.6),((580,480),a+1.4)]:
        if t>t0:
            put(cv,c,band(52,8,RED,.95,1),p[0],p[1],r=40);put(cv,c,band(52,8,RED,.95,1),p[0],p[1],r=-40);pulse(cv,c,*p,t)
    for j in range(3): cotheo(cv,c,'t27_spr_coV',[(640,700),bd],t,a+j*.3,b-a,s=.14,ph=j)
    nhan(cv,'đường sông hay đường bộ · đều có quân Đại Việt chờ sẵn',960,150,t,a+.3,b,VIETC,36)
# 36: hai vua về phủ Long Hưng, giải tù binh theo
def S_36(cv,t):
    a,b=T[49]-.3,E[49]+.3;q=sb(49,1)
    tranh(cv,'dong_b',t,a,b,(560,640,1.15),(520,660,1.2))
    c=kc(t,[(a,(960,560,1.0)),(b,(900,570,1.05))])
    for i in range(3): co(cv,c,'t27_spr_coV',1700-i*120-300*inn(t,a,b-a),880,t,s=.45,ph=i)
    ngua(cv,c,'nau','tts6',1900,1150,940,t,a,b,s=.56,flip=True)
    ngua(cv,c,'den','tnt6',2200,1450,960,t,a+.3,b,s=.56,flip=True)
    if t>q-1:
        for i,k in enumerate(['omn6','ptp','tlc']): dib(cv,c,k,2300+i*150,1700+i*150,960,t,q-1,b+1,s=.5,flip=True,sua=lambda PP,t_:PP.update(lean=12,head=10,arF=10,faF=-80,arB=0,faB=-80,mat='S'),chay=.4)
    tong(cv,.35)
    nhan(cv,'ngày mười bảy tháng ba · về phủ Long Hưng',960,170,t,a+.3,q,VIETC,40);nhan(cv,'Ô Mã Nhi · Phàn Tiếp · Tích Lệ Cơ bị giải theo',960,170,t,q+.2,b,INK,38)
# 37: lễ dâng thắng trận ở Chiêu Lăng
def S_37(cv,t):
    a,b=T[50]-.3,E[50]+.3;q=sb(50,1)
    mp=tranh(cv,'mo_a',t,a,b,(512,560,1.15),(512,600,1.3));ngua_da(cv,mp,t,1)
    c=kc(t,[(a,(960,560,1.0)),(q,(960,600,1.1)),(b,(1050,620,1.25))])
    ngd(cv,c,'tts6',600,920,t,.56,lay(rig.dung(t),t));ngd(cv,c,'tnt6',760,920,t,.56,lay(rig.dung(t),t+1))
    for i,k in enumerate(['omn6','ptp','tlc']): ngd(cv,c,k,1100+i*140,940,t,.5,quy(rig.so(t+i,.6)))
    for i in range(3): ngd(cv,c,VA[i],1550+i*110,930,t,.5,rig.dung(t+i),flip=True,vk='giao')
    if not FREEZE: smoke(cv,c,680,860,t,.5)
    tong(cv,.4)
    nhan(cv,'lễ dâng thắng trận ở Chiêu Lăng',960,170,t,a+.3,q,VIETC,42);nhan(cv,'kẻ phá lăng bị giải tới trước mặt',960,170,t,q+.2,b,RED,40)
# 38: chân ngựa đá lấm bùn
def S_38(cv,t):
    a,b=T[51]-.3,E[51]+.3;q=sb(51,1)
    tranh(cv,'ngua_da',t,a,b,(512,420,1.0),(500,700,1.35))
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.0))])
    for i in range(5):
        x=300+i*330+20*math.sin(t+i);y=900+((t*40+i*60)%140)
        put(cv,c,band(18,10,INK,.5,4),x,y)
    chim(cv,c,t,1300,220,3,25,4)
    tong(cv,.3)
    nhan(cv,'chân những con ngựa đá đều lấm bùn',960,170,t,q-.3,b,RED,42)
# 39: như thể ngựa đá cũng đã ra trận
def S_39(cv,t):
    a,b=T[52]-.3,E[52]+.3;q=sb(52,1)
    mp=tranh(cv,'mo_a',t,a,b,(300,560,1.4),(512,560,1.15));ngua_da(cv,mp,t,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.03))])
    if t<q+.5:
        for i in range(3): ngua(cv,c,['nau','den','nau'][i],None,-300-i*260,2200,820+i*40,t,a+.2+i*.25,q+.6,s=.5,o=.28)
    tong(cv,.4)
    nhan(cv,'như thể ngựa đá cũng đã ra trận',960,170,t,a+.3,q,INK,42)
    if t>q: ngd(cv,c,'tts6',960,940,t,.55,rig.dung(t)|{'arF':-60,'faF':-40})
    nhan(cv,'trong lễ bái yết, nhà vua làm thơ',960,170,t,q+.2,b,INK,40)
# 40: câu thơ
def S_40(cv,t):
    a,b=T[53]-.3,E[53]+.3;q=sb(53,1)
    mp=tranh(cv,'mo_a',t,a,b,(512,520,1.0),(512,540,1.05),o=.5);ngua_da(cv,mp,t)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.02))])
    chim(cv,c,t,200,200,4,25,5)
    for k in range(3): put(cv,c,band(260,60,PAPER,.4,30),300+((t*30+k*500)%1500),420+k*60)
    tong(cv,.3)
    cuon(cv,760,470,t,'THƠ NHÀ VUA','xã tắc lưỡng hồi|lao thạch mã',col=RED,s=.78,sz=40,u=inn(t,a+.4,2.0),nm='t26n_cuon2')
    if t>q and not FREEZE: put_screen(cv,text('đất nước hai lần gặp nạn,\nđến ngựa đá cũng phải nhọc nhằn',38,INK,700),1440,470,inn(t,q,.6))
# 41: đưa Ô Mã Nhi về nước
def S_41(cv,t):
    a,b=T[54]-.3,E[54]+.3;q=sb(54,1)
    tranh(cv,'song_b',t,a,b,(560,600,1.05),(520,620,1.12))
    c=kc(t,[(a,(960,560,1.0)),(b,(980,560,1.06))])
    tthuyen(cv,c,900+200*inn(t,q,b-q),700,t,.55,True,False,[('omn6',-80,None),('lh6',60,None),('v10',150,'cheo')])
    chim(cv,c,t,300,240,4,30,6)
    tong(cv,.42)
    nhan(cv,'tháng hai năm 1289 · đưa Ô Mã Nhi về nước',960,170,t,q-.4,b,INK,40)
# 42: giữa đêm, thuyền bị đục, chìm dần
def S_42(cv,t):
    a,b=T[55]-.3,E[55]+.3;q=sb(55,1) if len(_SC[55])>2 else a+(b-a)*.45
    tranh(cv,'dem_bien',t,a,b,(512,480,1.0),(560,500,1.12))
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.06))])
    u=inn(t,a+2,b-a-2.5)
    if not FREEZE: cv[:]=cv*(1-.0)
    tthuyen(cv,c,900,700+70*u,t,.55,True,False,[('omn6',-80,'so' if u>.1 else None),('m8',60,'so' if u>.2 else None)],nghieng=14*u,o=1-.6*u)
    if not FREEZE:
        X,Y=c.p(900,700);ov=cv.copy();cv2.rectangle(ov,(0,int(Y+20)),(1920,1080),tuple(float(v) for v in INK*.9+PAPER*.1),-1);cv[:]=cv*.35+ov*.65
        for k in range(4):
            kk=((t*1.2+k*.25)%1.0);cv2.ellipse(cv,(int(X+(k-1.5)*60),int(Y+20)),(int(20+90*kk),int(5+10*kk)),0,0,360,tuple(float(v) for v in PAPER*.7*(1-kk)+INK*kk),2,cv2.LINE_AA)
    tong(cv,.5)
    nhan(cv,'giữa đêm · thuyền bị đục thủng rồi chìm dần',960,170,t,a+.3,b,INK,40)
# 43: quân Nguyên không còn sang nữa
def S_43(cv,t):
    a,b=T[56]-.3,E[56]+.3
    tranh(cv,'song_a',t,a,b,(512,560,1.0),(512,580,1.06))
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.04))])
    coc(cv,c,t,600)
    for i in range(2): tthuyen(cv,c,300+i*900+50*(t-a),720+i*20,t,.36,False,i==1,[('v11',-30,'cheo')],ph=i)
    chim(cv,c,t,200,260,6,35,7)
    tong(cv,.45)
    nhan(cv,'quân Nguyên không còn sang đánh Đại Việt',960,170,t,a+.3,b,VIETC,40)
# 44: kết
def S_44(cv,t):
    a=T[57]-.3;b=E[57]+4
    tranh(cv,'bd_chieu',t,a,b,(512,520,1.0),(512,560,1.12))
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.05))])
    coc(cv,c,t,700,4,20)
    tthuyen(cv,c,1300-60*(t-a),760,t,.4,False,True,[('v11',-30,'cheo')])
    chim(cv,c,t,400,240,5,25,8)
    tong(cv,.5)
    if not FREEZE: put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,150,inn(t,E[57]+.6,1))
# ---------- ráp cảnh ----------
SC_LIST=[(0,S_1),(T[2]-.3,S_2),(T[3]-.3,S_3),(T[4]-.3,S_4),(T[5]-.3,S_5),(T[6]-.3,S_6),(T[7]-.3,S_7),(T[8]-.3,S_8),(T[9]-.3,S_9),(T[10]-.3,S_10),
 (T[11]-.3,S_11),(T[12]-.3,S_12),(T[13]-.3,S_13),(T[14]-.3,S_14),(T[16]-.3,S_15),(T[17]-.3,S_16),(T[18]-.3,S_17),(T[22]-.3,S_18),(T[23]-.3,S_19),(T[24]-.3,S_20),
 (T[26]-.3,S_21),(T[28]-.3,S_22),(T[30]-.3,S_23),(T[32]-.3,S_24),(T[34]-.3,S_25),(T[36]-.3,S_26),(T[39]-.3,S_27),(T[41]-.3,S_28),(T[42]-.3,S_29),(T[43]-.3,S_30),
 (T[44]-.3,S_31),(T[45]-.3,S_32),(T[46]-.3,S_33),(T[47]-.3,S_34),(T[48]-.3,S_35),(T[49]-.3,S_36),(T[50]-.3,S_37),(T[51]-.3,S_38),(T[52]-.3,S_39),(T[53]-.3,S_40),
 (T[54]-.3,S_41),(T[55]-.3,S_42),(T[56]-.3,S_43),(T[57]-.3,S_44)]
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
SH=[(SC_LIST[i][0],SC_LIST[i+1][0] if i<len(SC_LIST)-1 else V.TOTAL+1,SC_LIST[i][1]) for i in range(len(SC_LIST))]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm27_full.json'))
SENT={}
for _i,_d in enumerate(_J):
    _hs=[x for x in re.split(r'(?<=[.!?])\s+',_d.get('hien',_d['text'])) if x.strip()]
    SENT[_i+1]=_hs if len(_hs)==len(_SC[_i+1])-1 else [_d.get('hien',_d['text'])]
def caps(cv,t):
    for n,hs in SENT.items():
        for k,h in enumerate(hs):
            a=sb(n,k) if len(hs)>1 else T[n];b=sb(n,k+1) if len(hs)>1 else E[n]
            if a<t<b: caption(cv,h,inn(t,a,.12)*(1-inn(t,b-.12,.12)),False)
NOCAP=False
def ov(cv,t):
    if FREEZE: return
    TT=T[5]
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'BẠCH ĐẰNG 1288','stitle27',.55)
    if not NOCAP: caps(cv,t)
V.NHAN={}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
