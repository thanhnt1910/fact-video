# dai_tm28: Chế Bồng Nga và chiếc thuyền sơn xanh (1371–1390), giọng Charon (26/11). Chủ kênh 26/11: thủy mặc 100% bằng code (không FLUX, không Veo), thêm hiệu ứng; người vẽ bằng mã. Nhân vật múa rối riêng tập (t26n_r_*), có nét mặt sợ, giận, reo (headS/G/V)
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
V=K.setup('tm28',{5:3.5})
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
for _k in ['cbn','lng','blk','mbm','c1','c2','c3','dt','dl','dtb','nt','nmh','tkc','lql','nd','ngv']: rig.PRE[_k]='t28n_r_'
def gio(PP,t_): PP.update(arF=-150+6*math.sin(t_*2),faF=-10)
# ---------- bản đồ và sơ đồ trận (sửa 25/11 theo góp ý chủ kênh) ----------
PTM=json.load(open('/tmp/gen/bd/a/map28_pts.json'))
def mcam(t,keys):
    if FREEZE: t=keys[0][0]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z);return cam(cx,cy,z)
def bando(cv,c,t,a):
    im=A('map28')
    if not FREEZE and t<a+1: im=wipe(im,inn(t,a-.2,1.0),0,.25,seed=4)
    put(cv,c,im,960,540,scale_px=1.5)
    if not FREEZE and t>a+.6:
        for k_,nm_ in (('hoangsa','quần đảo Hoàng Sa'),('truongsa','quần đảo Trường Sa')):
            if k_ in PTM:
                X_,Y_=c.p(*PTM[k_]);tx_=text(nm_,max(18,int(15*c.z)),INK,700,glow=3);put_screen(cv,tx_,X_,Y_+18*c.z+tx_.shape[0]/2,inn(t,a+.6,.6)*.9)
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

# ---------- tm28: thủy mặc 100% bằng code (chủ kênh 26/11) ----------
import cv2
VA=['v8','v9','v10','v11'];CA=['c1','c2','c3']
def chim(cv,c,t,x0,y0,n=4,sp=40,seed=0):
    for i in range(n):
        x=x0+((t*sp+i*90+seed*50)%900);y=y0+i*18+6*math.sin(t*3+i)
        put(cv,c,'t12_spr_chim',x,y,s=.12+.02*(i%2),r=8*math.sin(t*6+i))
def tthuyen(cv,c,x,y,t,s,lon,flip,ngoi,nghieng=0,o=1.0,ph=0,name=None):
    """thuyền (lon=True: chiến thuyền lớn; name='t28n_thuyenxanh' cho thuyền vua); ngoi=[(key,dx,kiểu)]"""
    bob=0 if nghieng else 3*math.sin(t*1.3+ph);r=nghieng+.8*math.sin(t*.9+ph)
    f=-1 if flip else 1;name=name or ('t23n_thuyenlon' if lon else 't23n_thuyen')
    for key,dx,vk in ngoi:
        PP=rig.ngoi(t+dx*.01);PP.update(thF=-80,thB=-76,knF=84,knB=82);dung_=False
        if vk=='cheo': PP.update(arF=-10+25*math.sin(t*4+dx),faF=-40,arB=10+25*math.sin(t*4+dx),faB=-40,mat='G');vk=None
        elif vk=='so': PP.update(arF=-120+3*math.sin(t*23),faF=-70,arB=-100,faB=-80,lean=-10,mat='S');vk=None
        elif vk=='khoc': PP.update(arF=-100,faF=-120,arB=-90,faB=-120,lean=24,head=18,mat='S');vk=None
        elif vk=='dung': PP=rig.dung(t+dx);PP['mat']='G';dung_=True;vk=None
        elif vk=='giao': PP=rig.dung(t+dx);dung_=True
        rr=math.radians(r);hx=x+f*dx*s*math.cos(rr);hy=y-46*s+bob+f*dx*s*math.sin(rr)
        if dung_: rig.ve23(cv,c,key,hx,y+bob+14*s+f*dx*s*math.sin(rr),s*1.05,PP,flip=flip,vk=vk,o=o)
        else: rig.ve23(cv,c,key,0,0,s,PP,flip=flip,vk=vk,o=o,hip=(hx,hy))
    put(cv,c,Af(name) if flip else name,x,y+bob,s=s,r=r,ay=.8,o=o,scale_px=3)
def tenbay(cv,c,t,src,dst,n,seed):
    if FREEZE: return
    r=np.random.default_rng(seed)
    for i in range(n):
        ph=((t*.9+r.random())%1.0);a=(src[0]+r.normal(0,40),src[1]+r.normal(0,20));b=(dst[0]+r.normal(0,80),dst[1]+r.normal(0,30))
        P_=lambda q:(lerp(a[0],b[0],q),lerp(a[1],b[1],q)-math.sin(q*math.pi)*160)
        X,Y=c.p(*P_(ph));X2,Y2=c.p(*P_(max(0,ph-.04)))
        cv2.line(cv,(int(X2),int(Y2)),(int(X),int(Y)),tuple(float(v) for v in INK),2,cv2.LINE_AA)
def dem(cv,k=.55):
    """đêm: mực đậm phủ, giữ giấy ở trăng"""
    if FREEZE: return
    cv[:]=cv*(1-k)+(INK*.85+PAPER*.15)*k
def trang(cv,c,x,y,t):
    put(cv,c,band(150,150,PAPER,.95,75),x,y);put(cv,c,band(260,260,PAPER,.25,130),x,y)
def mua(cv,t,o=.5,seed=0):
    """mưa bão: vệt chéo trên màn hình"""
    if FREEZE: return
    r=np.random.default_rng(seed);ov=cv.copy()
    for i in range(140):
        x=(r.random()*2200+t*900*(1+r.random()*.3))%2200-140;y=(r.random()*1300+t*1300)%1300-110
        cv2.line(ov,(int(x),int(y)),(int(x-26),int(y+70)),tuple(float(v) for v in INK*.7+PAPER*.3),2,cv2.LINE_AA)
    cv[:]=cv*(1-o)+ov*o
def chop(cv,t,t0,o=.6):
    """tia chớp: lóe sáng giấy"""
    if FREEZE or not(t0<t<t0+.35): return
    u=1-(t-t0)/.35;cv[:]=cv*(1-o*u)+PAPER*(o*u)
def lua(cv,c,x,y,t,s=1.0,n=3,seed=0):
    for k in range(min(n,2)): put(cv,c,'t24_lua',x+(k-.5)*120*s+8*math.sin(t*6+k+seed),y,s=.45*s*(1+.06*math.sin(t*9+k)),ay=1,o=.75+.2*math.sin(t*5+k))
    smoke(cv,c,x,y-160*s,t+seed,s=s*.9)
def no(cv,c,x,y,t,t0,s=1.0):
    """phát hỏa súng: chớp lửa, vòng khói bung ra rồi tan"""
    if t<t0 or FREEZE: return
    u=t-t0
    if u<.25: put(cv,c,band(int(140*s),int(80*s),(1,.82,.45),.9*(1-u/.25),40),x,y)
    for k in range(4):
        uu=min(1,u/2.2);put(cv,c,'t12_spr_khoi',x+60*k*s*uu,y-40*s*uu*(k%2),s=.5*s*(.6+uu),o=.55*(1-uu))
def manh(cv,c,x,y,t,t0,n=8,seed=0,s=1.0):
    """mảnh ván văng ra"""
    if t<t0 or FREEZE: return
    r=np.random.default_rng(seed);u=t-t0
    for i in range(n):
        vx,vy=r.normal(0,260),-r.uniform(150,380);X,Y=c.p(x+vx*u*s,y+(vy*u+500*u*u)*s)
        if u<1.4: cv2.line(cv,(int(X),int(Y)),(int(X+14*math.cos(u*9+i)),int(Y+14*math.sin(u*9+i))),tuple(float(v) for v in INK*.9+(.4,.3,.2)),4,cv2.LINE_AA)
def song_toi(cv,c,y,t,o=.9):
    put(cv,c,'t26_song',960,y,ay=0,k=.8,s=1.0,o=o)
def ao_dan_ba(cv,c,x,y,s,t,u):
    """áo dài đàn bà màu hồng nhạt choàng lên vai tướng"""
    if u<=0 or FREEZE: return
    X,Y=c.p(x,y);k=s*1.875
    pts=np.int32([[X-46*k,Y-190*k],[X+40*k,Y-190*k],[X+60*k,Y-20*k],[X-64*k,Y-20*k]])
    ov=cv.copy();cv2.fillPoly(ov,[pts],(0.86,0.72,0.74),cv2.LINE_AA);cv2.polylines(ov,[pts],True,tuple(float(v) for v in INK),3,cv2.LINE_AA)
    cv[:]=cv*(1-.8*u)+ov*(.8*u)
def gach(cv,c,x0,y0,x1,y1,t,t0,n=6,seed=0):
    """gạch ngói ném vào"""
    if t<t0 or FREEZE: return
    r=np.random.default_rng(seed)
    for i in range(n):
        ph=((t-t0)*.8+r.random())%1.0;a=(x0+r.normal(0,120),y0);b=(x1+r.normal(0,40),y1+r.normal(0,30))
        X,Y=c.p(lerp(a[0],b[0],ph),lerp(a[1],b[1],ph)-math.sin(ph*math.pi)*140)
        cv2.rectangle(cv,(int(X-6),int(Y-4)),(int(X+6),int(Y+4)),tuple(float(v) for v in INK*.8+(.35,.2,.15)),-1)
def vang(cv,c,x,y,n=14,seed=0,o=1.0):
    r=np.random.default_rng(seed)
    for i in range(n): put(cv,c,band(18,12,GOLD,.95*o,4),x+r.normal(0,40),y+r.normal(0,12))
def nuocvo(cv,c,x,y,t,t0,s=1.0):
    """đập vỡ: khối nước tràn ra"""
    if t<t0 or FREEZE: return
    u=min(1,(t-t0)/1.6);X,Y=c.p(x,y)
    for k in range(6):
        cv2.ellipse(cv,(int(X+k*90*u*s),int(Y+20*k*u)),(int(80*s+200*u*s),int(18*s+20*u*s)),0,180,360,tuple(float(v) for v in INK*.5+PAPER*.5),3,cv2.LINE_AA)
def bui2(cv,c,x,y,t,n=5,s=.5,o=.5):
    for k in range(n): put(cv,c,'t12_spr_khoi',x+k*70*s-n*35*s+12*math.sin(t*2+k),y-8*k%3,s=s,o=o*(.6+.4*math.sin(t*1.3+k)))
def chuyen(cv,t,t0,dur=.7):
    """chuyển cảnh: mực loang từ giữa (đầu cảnh)"""
    if FREEZE or not(t0<t<t0+dur): return
    u=(t-t0)/dur;m=loang(960,540,2200*u,120)
    cv[:]=cv*m+(PAPER*.9+INK*.1)*(1-m)
GOLD=np.array((.79,.64,.35),np.float32)
# ================= CẢNH =================
# 1: hơn một trăm chiến thuyền, một chiếc sơn xanh
def S_1(cv,t):
    a,b=0,E[1]+.3
    c=kc(t,[(a,(960,560,1.25)),(b,(1000,600,1.05))])
    nen(cv,c,t,'song',seed=1,mist=.55);song_toi(cv,c,620,t)
    for i in range(14):
        x=-100+(i%7)*330+((i*53)%90);y=600+(i//7)*70+((i*37)%30)
        tthuyen(cv,c,x+30*(t-a),y,t,.22+.05*(i//7),True,False,[],ph=i,o=.55+.2*(i//7))
    tthuyen(cv,c,1000+30*(t-a),760,t,.42,True,False,[('cbn',-230,'dung')],name='t28n_thuyenxanh',ph=3)
    suong(cv,c,t,640,.4,1)
    nhan(cv,'một chiếc thuyền sơn xanh',960,160,t,a+.8,b,RED,46)
# 2: người hầu chạy sang, chỉ tay
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3;q=sb(2,1)
    c=kc(t,[(a,(900,580,1.0)),(q,(1000,600,1.15)),(b,(1100,600,1.2))])
    nen(cv,c,t,'song',seed=2,mist=.4);song_toi(cv,c,640,t)
    tthuyen(cv,c,1550,700,t,.3,True,False,[],name='t28n_thuyenxanh')
    for i in range(3): tthuyen(cv,c,1250+i*250,650+i*12,t,.2,True,False,[],ph=i,o=.6)
    for i in range(4): ngd(cv,c,VA[i],300+i*120,900+(i%2)*12,t,.56,rig.dung(t+i)|({'mat':'S'} if t>q else {}),vk='giao')
    x=chay(cv,c,'blk',-150,800,920,t,a,q-.2,.56,lambda ph,tt:rig.hoang(ph,tt,1.1))
    if t>q-.2:
        P=rig.dung(t);P.update(arF=-92+3*math.sin(t*5),faF=-2,lean=6,mat='S');ngd(cv,c,'blk',800,920,t,.56,P)
    suong(cv,c,t,700,.3,2)
# 3: Chế Bồng Nga trên thuyền
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3;q=sb(3,1)
    c=kc(t,[(a,(1000,560,1.35)),(q,(960,560,1.15)),(b,(900,560,1.0))])
    nen(cv,c,t,'song',seed=3,mist=.4);song_toi(cv,c,620,t)
    for i in range(4): tthuyen(cv,c,200+i*420,690+(i%2)*20,t,.3,True,False,[(CA[i%3],-120,'giao'),(CA[(i+1)%3],60,'giao')],ph=i,o=.75)
    tthuyen(cv,c,1050,860,t,.62,True,False,[('c1',-320,'giao'),('cbn',-230,'dung'),('c2',220,'giao')],name='t28n_thuyenxanh')
    nhan(cv,'Chế Bồng Nga · vua nước Chiêm Thành',960,150,t,a+.4,q,INK,40)
    nhan(cv,'nhiều lần đánh vào tận Thăng Long',960,150,t,q+.2,b,RED,40)
# 4: câu hỏi
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.6
    c=kc(t,[(a,(900,600,1.6)),(b,(960,600,1.75))])
    nen(cv,c,t,'song',seed=4,mist=.6);song_toi(cv,c,640,t)
    tthuyen(cv,c,1400,720,t,.35,True,False,[],name='t28n_thuyenxanh')
    P=rig.dung(t);P.update(arF=-92,faF=-2,lean=6,mat='S');ngd(cv,c,'blk',700,930,t,.7,P)
    nhan(cv,'người hầu ấy là ai?',960,250,t,a+.3,b,RED,52)
# 5: bản đồ: Đại Việt và Chiêm Thành
def S_5(cv,t):
    a,b=T[5]-3.6,E[5]+.3
    tl,db=tuple(PTM['thanglong']),tuple(PTM['doban'])
    c=mcam(t,[(a,(960,540,1.0)),(b,(960,540,1.04))])
    bando(cv,c,t,a)
    diem(cv,c,'Thăng Long',tl,t,T[5]+.3,VIETC,dx=24,dy=-10);diem(cv,c,'Đồ Bàn',db,t,T[5]+1.2,RED,dx=-130,dy=-10)
    if t>T[5]+1.2: pulse(cv,c,*db,t)
    if not FREEZE:
        X,Y=c.p(*tl);put_screen(cv,text('ĐẠI VIỆT',46,VIETC,700,glow=4),X-60,Y+120,inn(t,T[5]+.3,.6))
        X,Y=c.p(*db);put_screen(cv,text('CHIÊM THÀNH',46,RED,700,glow=4),X-260,Y-130,inn(t,T[5]+1.2,.6))
    nhan(cv,'hơn sáu trăm năm trước',960,110,t,T[5],b,INK,38)
# 6: năm 1371, theo biển vào cửa Đại An, lên Thăng Long
def S_6(cv,t):
    a,b=T[6]-.3,E[7]+.3;q=T[7]
    tl,da,db=tuple(PTM['thanglong']),tuple(PTM['daian']),tuple(PTM['doban'])
    c=mcam(t,[(a,(960,560,1.0)),(q,(tl[0]+60,tl[1]+120,2.2)),(b,(tl[0]+40,tl[1]+80,2.4))])
    bando(cv,c,t,a-1)
    ps=[db,(db[0]+80,db[1]-260),(da[0]+160,da[1]+60),da,tl];duong(cv,c,ps,t,a+.2,2.6,RED,5)
    for j in range(4): cotheo(cv,c,'t23n_thuyen',ps,t,a+.2+j*.25,3.2,s=.06,ph=j)
    diem(cv,c,'cửa Đại An',da,t,a+1.8,INK,dx=24,dy=10);diem(cv,c,'Thăng Long',tl,t,a+2.6,RED,dx=24,dy=-12)
    if t>a+2.8: pulse(cv,c,*tl,t)
    nhan(cv,'năm 1371',960,110,t,a+.2,q,RED,42)
    if t>q: nhan(cv,'vua nhà Trần lánh sang Đông Ngàn',960,110,t,q,b,INK,38)
# 8: kinh thành cháy
def S_8(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1)
    sh=2*math.sin(t*30) if not FREEZE else 0
    c=kc(t,[(a,(960,620,1.05)),(b,(1020,620,1.2))],sh)
    nen(cv,c,t,seed=8,mist=.2)
    put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9)
    for x,y in [(620,560),(960,520),(1300,560)]: lua(cv,c,x,y,t,1.0,3,x*.01)
    for i in range(5): chay(cv,c,CA[i%3],-200+i*160,2100+i*60,950+(i%2)*14,t,a+i*.3,b,.52,lambda ph,tt:rig.hoang(ph,tt,1.2),vk='giao' if i%2 else None,ph=i)
    if t>q:
        for k in range(4): flick(cv,c,700+k*160,990,t+k,s=.5)
    truoc(cv,c,t)
    nhan(cv,'sách vở, sổ sách cháy thành tro',960,150,t,q,b,RED,40)
# 9: mẹ Dương Nhật Lễ xúi giục
def S_9(cv,t):
    a,b=T[9]-.3,E[9]+.3
    c=kc(t,[(a,(960,560,1.0)),(b,(980,560,1.05))])
    nen(cv,c,t,seed=9,mist=.5)
    put(cv,c,'t28n_doban',960,980,ay=1,s=.95,k=.7,o=.55)
    cuon(cv,960,460,t,'THEO SỬ CŨ','mẹ Dương Nhật Lễ|xúi giục báo thù',col=RED,s=.7,sz=40,u=inn(t,a+.4,1.6),nm='t26n_cuon2')
# 10: biên giới bỏ trống
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3;q=sb(10,1)
    c=kc(t,[(a,(960,600,1.1)),(b,(1100,600,1.0))])
    nen(cv,c,t,seed=10,mist=.6)
    put(cv,c,'t23_thanh',960,980,ay=1,s=.8,k=.85,o=.9)
    chim(cv,c,t,300,320,5,30,1)
    for i in range(6): put(cv,c,'t26n_vai',300+i*280,975,s=.4,o=.5,r=10*math.sin(i))
    truoc(cv,c,t)
    nhan(cv,'thái bình đã lâu · không ai lo phòng giữ',960,150,t,q-.6,b,INK,40)
# 11: lời Ngô Sĩ Liên
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.04))])
    nen(cv,c,t,seed=11,mist=.5)
    cuon(cv,960,470,t,'SỬ GIA NGÔ SĨ LIÊN','mối lo đời đời|mà bỏ bê việc giữ nước',col=RED,s=.72,sz=38,u=inn(t,a+.4,2.0),nm='t26n_cuon2')
# 12–13: Chế Bồng Nga rèn quân
def S_12(cv,t):
    a,b=T[12]-.3,E[13]+.3;q=T[13]
    c=kc(t,[(a,(1200,580,1.25)),(q,(960,580,1.0)),(b,(900,580,1.05))])
    nen(cv,c,t,seed=12,mist=.35)
    put(cv,c,'t28n_doban',960,900,ay=1,s=.85,k=.6,o=.6)
    voi(cv,c,1700,930,t,.55,flip=True);voi(cv,c,1880,940,t,.5,flip=True,ph=1)
    for i in range(12):
        r_=i//6;x=250+(i%6)*170+r_*60;y=930+r_*40
        P=rig.reo(t+i*.2) if (t>q and int(t*1.2+i)%2==0) else rig.dung(t+i);ngd(cv,c,CA[i%3],x,y,t,.5,P,vk='giao')
    ngd(cv,c,'cbn',1360,900,t,.6,rig.quat(t)|{'mat':'G'},flip=True)
    ngd(cv,c,'lng',1480,905,t,.56,rig.dung(t),flip=True,vk='giao')
    truoc(cv,c,t)
    nhan(cv,'Chế Bồng Nga và tướng La Ngai rèn quân',960,150,t,a+.3,q,INK,38)
    nhan(cv,'nỗi lo lớn nhất ở phương nam',960,150,t,q+.2,b,RED,40)
# 14: Đỗ Tử Bình giữ Hóa Châu
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3;q=sb(14,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(1000,620,1.15))])
    nen(cv,c,t,seed=14,mist=.4)
    put(cv,c,'t26n_trai',960,930,ay=1,s=.9,k=.8)
    for i in range(5): ngd(cv,c,VA[i%4],420+i*140,935+(i%2)*10,t,.52,rig.dung(t+i),vk='giao')
    ngd(cv,c,'dtb',1250,930,t,.62,rig.dung(t)|{'mat':'G'},flip=True)
    nhan(cv,'Đỗ Tử Bình · trấn giữ Hóa Châu',960,150,t,q-.5,b,INK,40)
# 15–16: mười mâm vàng
def S_15(cv,t):
    a,b=T[15]-.3,E[16]+.3;q=T[16]
    c=kc(t,[(a,(900,600,1.0)),(q,(1150,640,1.35)),(b,(1200,650,1.55))])
    nen(cv,c,t,seed=15,mist=.35)
    put(cv,c,'t26n_trai',960,930,ay=1,s=.9,k=.8,o=.8)
    for i in range(5):
        x=dib(cv,c,'mbm' if i==0 else CA[i%3],-200-i*170,700-i*150,940,t,a,q,s=.52,ph=i,sua=lambda PP,t_:PP.update(arF=-170,faF=-10,arB=-170,faB=-10))
        put(cv,c,'t23_mam',x+8,940-200*.52*1.45,s=.42,o=.95);vang(cv,c,x+8,940-215*.52*1.45,14,i)
    ngd(cv,c,'dtb',1250,930,t,.62,rig.dung(t)|{'mat':'G','lean':12} ,flip=True)
    if t>q:
        put(cv,c,'t23_mam',1130,930,s=.6);vang(cv,c,1130,905,24,9)
        soi(cv,c,1130,900,t,.8)
    nhan(cv,'mười mâm vàng dâng vua nhà Trần',960,150,t,a+.3,q,INK,40)
    nhan(cv,'nhưng chúng không bao giờ về tới kinh thành',960,150,t,sb(16,1),b,RED,38)
# 17: nói dối
def S_17(cv,t):
    a,b=T[17]-.3,E[17]+.3;q=sb(17,1)
    c=kc(t,[(a,(1150,640,1.3)),(b,(960,600,1.0))])
    nen(cv,c,t,seed=17,mist=.4)
    put(cv,c,'t26n_trai',960,930,ay=1,s=.9,k=.8,o=.6)
    ngd(cv,c,'dtb',1150,930,t,.64,rig.dung(t)|{'mat':'G','arF':-60,'faF':-60},flip=True)
    cuon(cv,640,450,t,'TÂU VỀ TRIỀU','Chế Bồng Nga|ngạo mạn vô lễ',col=RED,s=.62,sz=38,u=inn(t,a+.5,1.6),nm='t26n_cuon2')
# 18: vua nổi giận
def S_18(cv,t):
    a,b=T[18]-.3,E[18]+.3;q=sb(18,1)
    sh=3*math.sin(t*40) if q<t<q+.4 and not FREEZE else 0
    c=kc(t,[(a,(960,620,1.0)),(q,(1100,600,1.3)),(b,(1100,600,1.35))],sh)
    nen(cv,c,t,seed=18,mist=.2)
    put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9)
    for i in range(4): ngd(cv,c,'dtb' if i==0 else 'lql' if i==1 else 'nd',500+i*150,945,t,.5,lay(rig.dung(t),t+i))
    P=rig.quat(t) if t>q else rig.dung(t);P['mat']='G' if t>q else '';ngd(cv,c,'dt',1150,930,t,.62,P,flip=True,vk='dao' if t>q else None)
    nhan(cv,'vua Trần Duệ Tông quyết tự mình cầm quân',960,150,t,q,b,RED,38)
# 19–20: lời can, treo mũ
def S_19(cv,t):
    a,b=T[19]-.3,E[20]+.3;q=T[20]
    c=kc(t,[(a,(1000,620,1.25)),(q,(960,600,1.0)),(b,(800,600,1.0))])
    nen(cv,c,t,seed=19,mist=.3)
    put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9,o=.8 if t<q else .5)
    if t<q+.3:
        ngd(cv,c,'ngv',800,950,t,.56,lay(rig.dung(t),t))
        ngd(cv,c,'dt',1250,930,t,.6,rig.dung(t)|{'mat':'G'},flip=True)
    else:
        dib(cv,c,'ngv',700,-300,950,t,q+.3,b,s=.56,sua=lambda PP,t_:PP.update(head=12,lean=8))
        put(cv,c,'t26n_non',820,955,s=.3)
    nhan(cv,'ba lần can · cả ba lần vua gạt đi',960,150,t,a+.3,q,INK,40)
    nhan(cv,'treo mũ từ quan',960,150,t,q+.2,b,RED,42)
# 21: mười hai vạn quân lên đường
def S_21(cv,t):
    a,b=T[21]-.3,E[21]+.3
    c=kc(t,[(a,(960,600,1.0)),(b,(1100,620,1.12))])
    nen(cv,c,t,seed=21,mist=.3)
    put(cv,c,'t23_thanh',500,980,ay=1,s=.7,k=.8,o=.8)
    for i in range(18):
        r_=i%3;x=dib(cv,c,VA[i%4],-500+(i//3)*330,500+(i//3)*330,910+r_*35,t,a,b,s=.46+r_*.04,vk='giao',ph=i,buoc=55)
        if i%6==0: co(cv,c,'t26_spr_coV',x+30,910+r_*35,t,s=.42,ph=i)
    bui2(cv,c,1100,980,t,8,.6,.35)
    truoc(cv,c,t)
    nhan(cv,'tháng 12 năm 1376 · mười hai vạn quân',960,150,t,a+.3,b,VIETC,40)
# 22: thủy quân vượt biển, vua dẫn quân bộ
def S_22(cv,t):
    a,b=T[22]-.3,E[22]+.3;q=sb(22,1)
    c=kc(t,[(a,(960,580,1.0)),(b,(1040,590,1.08))])
    nen(cv,c,t,'song',seed=22,mist=.35);song_toi(cv,c,560,t)
    for i in range(5): tthuyen(cv,c,100+i*380+40*(t-a),640+(i%2)*20,t,.3,True,False,[(VA[i%4],-60,'cheo')],ph=i,o=.8)
    ngua(cv,c,'nau','dt',200,1100,960,t,a,b+3,s=.6)
    for i in range(5): dib(cv,c,VA[i%4],-100-i*130,800-i*130,975,t,a,b+3,s=.5,vk='giao',ph=i)
    nhan(cv,'luyện quân một tháng ở cửa Nhật Lệ',960,150,t,q,b,INK,40)
# 23: Lê Quý Ly chở lương
def S_23(cv,t):
    a,b=T[23]-.3,E[23]+.3
    tl,nl=tuple(PTM['thanglong']),tuple(PTM['nhatle'])
    c=mcam(t,[(a,(tl[0]+120,(tl[1]+nl[1])/2,1.6)),(b,(nl[0]+80,nl[1],1.9))])
    bando(cv,c,t,a)
    ps=[tl,(tl[0]+60,tl[1]+160),(nl[0]-20,nl[1]-160),nl];duong(cv,c,ps,t,a,1.6,VIETC,5)
    for j in range(4): cotheo(cv,c,'t26_spr_coV',ps,t,a+j*.25,b-a,s=.1,ph=j)
    diem(cv,c,'cửa Nhật Lệ',nl,t,a+1,VIETC,dx=24)
    nhan(cv,'Lê Quý Ly lo việc chở lương',960,150,t,a+.3,b,INK,40)
# 24: đến cửa Thi Nại, thấy Đồ Bàn
def S_24(cv,t):
    a,b=T[24]-.3,E[24]+.3;q=sb(24,1)
    if t<q:
        db,ti=tuple(PTM['doban']),tuple(PTM['thinai'])
        c=mcam(t,[(a,(db[0]-200,db[1]-260,1.3)),(q,(db[0],db[1],2.6))])
        bando(cv,c,t,a);diem(cv,c,'cửa Thi Nại',ti,t,a+.4,VIETC,dx=24,dy=14);diem(cv,c,'Đồ Bàn',db,t,a+.8,RED,dx=-120,dy=-14);pulse(cv,c,*db,t)
        nhan(cv,'tháng giêng năm 1377',960,110,t,a+.2,q,RED,40)
    else:
        c=kc(t,[(q,(960,560,1.3)),(b,(960,580,1.0))])
        nen(cv,c,t,seed=24,mist=.55);put(cv,c,'t28n_doban',960,900,ay=1,s=.85,k=.6)
        put(cv,c,'t26n_trai',700,1000,ay=1,s=.8,k=.9,o=.9);truoc(cv,c,t)
        nhan(cv,'Đồ Bàn · kinh đô Chiêm Thành',960,150,t,q+.2,b,RED,40)
# 25–26: lời hàng giả
def S_25(cv,t):
    a,b=T[25]-.3,E[26]+.3;q=T[26]
    c=kc(t,[(a,(960,600,1.0)),(q,(1100,640,1.3)),(b,(1100,640,1.38))])
    nen(cv,c,t,seed=25,mist=.4)
    if t<q:
        put(cv,c,'t28n_doban',960,900,ay=1,s=.85,k=.6)
        for i in range(6): ngd(cv,c,CA[i%3],250+i*110,920+(i%2)*10,t,.46,rig.dung(t+i),vk='giao')
        dib(cv,c,'mbm',900,1700,935,t,a+1,q,s=.5)
    else:
        put(cv,c,'t26n_trai',960,930,ay=1,s=.9,k=.8)
        ngd(cv,c,'mbm',950,945,t,.56,quy(rig.so(t,.4)))
        P=rig.dung(t);P.update(lean=10,mat='G');ngd(cv,c,'dt',1280,930,t,.62,P,flip=True)
        for i in range(2): ngd(cv,c,VA[i],1450+i*110,935,t,.52,rig.dung(t+i),flip=True,vk='giao')
    nhan(cv,'Chế Bồng Nga không giữ thành',960,150,t,a+.3,q,INK,40)
    nhan(cv,'"đã bỏ trốn · chỉ còn tòa thành trống"',960,150,t,q+.2,b,RED,38)
# 27: một cái bẫy
def S_27(cv,t):
    a,b=T[27]-.3,E[27]+.3;q=sb(27,1)
    c=kc(t,[(a,(960,760,1.6)),(b,(960,740,2.1))])
    nen(cv,c,t,seed=27,mist=.6);put(cv,c,'t28n_doban',960,900,ay=1,s=.85,k=.6)
    dem(cv,.25+.15*inn(t,a,b-a))
    nhan(cv,'một cái bẫy giăng sẵn trước cửa thành',960,150,t,a+.3,q,RED,40)
    nhan(cv,'người nghi ngờ lại không phải nhà vua',960,150,t,q+.2,b,INK,40)
# 28: vua áo đen, ngựa màu bùn
def S_28(cv,t):
    a,b=T[28]-.3,E[28]+.3;q=sb(28,1)
    c=kc(t,[(a,(1050,600,1.4)),(q,(960,600,1.05)),(b,(960,600,1.0))])
    nen(cv,c,t,seed=28,mist=.35)
    for i in range(8): ngd(cv,c,VA[i%4],200+i*120,915+(i%2)*14,t,.48,rig.dung(t+i),vk='giao')
    ngua(cv,c,'nau','dt',1050,1050,960,t,a,b,s=.66,vk='dao' if t>q else None,sua=lambda PP,t_:PP.update(arF=-160,faF=-5) if t_>q else None)
    ngua(cv,c,'trang','ngv',1450,1450,950,t,a,b,s=.56)
    nhan(cv,'áo đen · ngựa lông đen trắng như màu bùn',960,150,t,a+.3,q,INK,38)
    nhan(cv,'lệnh tiến quân gấp',960,150,t,q+.2,b,RED,44)
# 29–31: Đỗ Lễ can, bị mắng, mặc áo đàn bà
def S_29(cv,t):
    a,b=T[29]-.3,E[31]+.3;q=T[30];r=T[31]
    sh=3*math.sin(t*40) if q<t<q+.5 and not FREEZE else 0
    c=kc(t,[(a,(900,620,1.3)),(q,(1100,600,1.2)),(r,(800,640,1.45)),(b,(800,640,1.55))],sh)
    nen(cv,c,t,seed=29,mist=.35)
    for i in range(6): ngd(cv,c,VA[i%4],200+i*110,915,t,.46,rig.dung(t+i)|({'mat':'S'} if t>r else {}),vk='giao')
    P=lay(rig.dung(t),t) if t<q else (quy(rig.so(t,.3)) if t>r else rig.dung(t)|{'mat':'S','head':14})
    ngd(cv,c,'dl',820,950,t,.6,P)
    ao_dan_ba(cv,c,820,950,.6,t,inn(t,r+.4,1.2))
    P=rig.quat(t) if t>q else rig.dung(t);P['mat']='G' if t>q else ''
    ngua(cv,c,'nau','dt',1250,1250,960,t,a,b,s=.66,flip=True,sua=lambda PP,t_:PP.update(arF=-92,faF=-4,mat='G') if t_>q else None)
    nhan(cv,'đại tướng Đỗ Lễ xin hỏi cho rõ thật giả',960,150,t,a+.3,q,INK,38)
    nhan(cv,'vua gạt phắt đi',960,150,t,q+.2,r,RED,42)
    nhan(cv,'"hạng đàn bà"',960,150,t,r+.2,b,RED,48)
# 32–33: hàng quân như xâu cá, đứt quãng
def S_32(cv,t):
    a,b=T[32]-.3,E[33]+.3;q=T[33]
    c=kc(t,[(a,(960,600,1.0)),(b,(1300,600,1.0))])
    nen(cv,c,t,seed=32,mist=.35)
    for i in range(24):
        gap=420*inn(t,q,b-q) if i<10 else 0
        dib(cv,c,VA[i%4],1700-i*95+gap,3100-i*95+gap,920+(i%2)*14,t,a,b+6,s=.44,vk='giao',ph=i,buoc=55)
    truoc(cv,c,t)
    nhan(cv,'nối gót nhau như một xâu cá',960,150,t,a+.3,q,INK,40)
    nhan(cv,'một khoảng trống chết người',960,150,t,q+.4,b,RED,42)
# 34: phục binh xông ra
def S_34(cv,t):
    a,b=T[34]-.3,E[34]+.3;q=sb(34,1)
    sh=4*math.sin(t*37) if not FREEZE and t>a+.6 else 0
    c=kc(t,[(a,(960,600,1.05)),(b,(980,600,1.15))],sh)
    nen(cv,c,t,seed=34,mist=.25)
    for i in range(6): ngd(cv,c,VA[i%4],700+i*90,930+(i%2)*10,t,.48,rig.so(t+i,1.0),vk='giao')
    for i in range(7):
        P=rig.xung(t*6+i);P['mat']='G';x0=-300-i*90 if i%2 else 2200+i*90
        chay(cv,c,CA[i%3],x0,(560 if i%2 else 1500)+((i*37)%80),930+(i%3)*12,t,a+.2+i*.12,a+1.8+i*.12,.5,lambda ph,tt:rig.xung(ph*1.3),vk='giao',ph=i)
    tenbay(cv,c,t,(200,700),(900,880),7,3);tenbay(cv,c,t,(1750,700),(1000,880),7,4)
    bui2(cv,c,960,980,t,9,.7,.5)
    nhan(cv,'quân Chiêm Thành bất ngờ xông ra',960,150,t,a+.3,b,RED,42)
# 35: tan vỡ trước giờ trưa
def S_35(cv,t):
    a,b=T[35]-.3,E[35]+.3
    c=kc(t,[(a,(960,600,1.1)),(b,(960,600,1.0))],2*math.sin(t*31) if not FREEZE else 0)
    nen(cv,c,t,seed=35,mist=.3)
    for i in range(7): chay(cv,c,VA[i%4],1300+i*60,-300+i*40,930+(i%2)*14,t,a+i*.15,b+1,.5,lambda ph,tt:rig.hoang(ph,tt,1.2),ph=i)
    for k in range(4): roi(cv,c,'t23n_r_w_giao',700+k*200,820,t,a+.5+k*.4,dx=100,s=.4)
    for x in (500,1100,1500): smoke(cv,c,x,850,t+x*.01,s=.9)
    nhan(cv,'đội hình vỡ tan giữa đất Chiêm Thành',960,150,t,a+.3,b,RED,40)
# 36: vua ngã xuống
def S_36(cv,t):
    a,b=T[36]-.3,E[36]+.6
    c=kc(t,[(a,(960,640,1.5)),(b,(960,620,1.1))])
    nen(cv,c,t,seed=36,mist=.45)
    ngd(cv,c,'dt',900,960,t,.62,rig.nga(inn(t,a+.6,1.6))|{'mat':'S'})
    ngua(cv,c,'nau',None,1300,1300,965,t,a,b,s=.62,flip=True)
    for k in range(5): roi(cv,c,'t23n_r_w_giao',600+k*180,960,t,a-10,dx=0,s=.4)
    bui2(cv,c,960,990,t,6,.6,.3*(1-inn(t,a,b-a)))
    nhan(cv,'vua Trần Duệ Tông ngã xuống',960,150,t,a+.6,b,RED,42)
# 37: Đỗ Lễ chết, Ngự Câu vương bị bắt
def S_37(cv,t):
    a,b=T[37]-.3,E[37]+.3;q=sb(37,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(1000,600,1.05))])
    nen(cv,c,t,seed=37,mist=.4)
    if t<q: ngd(cv,c,'dl',700,975,t,.58,rig.nga(1.0));ao_dan_ba(cv,c,700,975,.58,t,.6)
    x=dib(cv,c,'ngv',1500,600,950,t,q-.3,b+1,s=.56,flip=True,sua=lambda PP,t_:PP.update(lean=12,head=10,arF=10,faF=-80,arB=0,faB=-80,mat='S'),chay=.4)
    for i,dx in enumerate([-160,150]): dib(cv,c,CA[i],1500+dx,600+dx,960,t,q-.3,b+1,s=.52,vk='giao',chay=.4,ph=i,flip=True)
    nhan(cv,'Ngự Câu vương bị bắt sống',960,150,t,q,b,INK,40)
# 38–39: Đỗ Tử Bình đứng ngoài, Lê Quý Ly bỏ về
def S_38(cv,t):
    a,b=T[38]-.3,E[39]+.3;q=T[39]
    c=kc(t,[(a,(960,600,1.0)),(b,(1000,600,1.05))])
    nen(cv,c,t,seed=38,mist=.35)
    for x in (1300,1600,1800): smoke(cv,c,x,700,t+x*.01,s=1.1)
    if t<q:
        ngua(cv,c,'nau','dtb',700,700,960,t,a,b,s=.6)
        for i in range(5): ngd(cv,c,VA[i%4],300+i*90,930,t,.46,rig.dung(t+i),vk='giao')
        nhan(cv,'Đỗ Tử Bình không đến cứu',960,150,t,a+.3,q,RED,42)
    else:
        put(cv,c,'t26n_bao',1100,950,s=.5);ngua(cv,c,'nau','lql',1200,-300,960,t,q,b+1,s=.56,flip=True)
        nhan(cv,'Lê Quý Ly nghe tin vua mất · bỏ về nước',960,150,t,q+.2,b,INK,38)
# 40–41: xe tù, ném gạch ngói
def S_40(cv,t):
    a,b=T[40]-.3,E[41]+.3;q=T[41]
    c=kc(t,[(a,(960,600,1.05)),(b,(1000,610,1.15))])
    nen(cv,c,t,seed=40,mist=.35)
    x=lerp(1500,700,inn(t,a,q-a))
    ngd(cv,c,'dtb',x,930,t,.58,quy(rig.so(t,.5)))
    if not FREEZE:
        X,Y=c.p(x,930);k=.58*1.875
        for j in range(6): cv2.line(cv,(int(X-70*k+j*28*k),int(Y-260*k)),(int(X-70*k+j*28*k),int(Y)),tuple(float(v) for v in INK),3,cv2.LINE_AA)
        cv2.rectangle(cv,(int(X-80*k),int(Y-265*k)),(int(X+80*k),int(Y)),tuple(float(v) for v in INK),4,cv2.LINE_AA)
    for i in range(6): ngd(cv,c,'dan',250+i*150 if i<3 else 1250+i*120,960,t,.52,rig.reo(t+i)|{'mat':'V'})
    gach(cv,c,400,880,x,800,t,a+.5,6,1);gach(cv,c,1500,880,x,800,t,a+.8,6,2)
    nhan(cv,'phủ Thiên Trường · dân ném gạch ngói mà chửi',960,150,t,a+.3,q,INK,38)
    nhan(cv,'cuộc chiến chưa dừng lại ở Đồ Bàn',960,150,t,sb(41,1),b,RED,40)
# 42: bão ở cửa Đại An
def S_42(cv,t):
    a,b=T[42]-.3,E[42]+.3;q=sb(42,1)
    sh=3*math.sin(t*23) if not FREEZE else 0
    c=kc(t,[(a,(960,580,1.0)),(b,(1000,600,1.1))],sh)
    nen(cv,c,t,'song',seed=42,mist=.6);song_toi(cv,c,580,t)
    for i in range(4):
        ng=12*math.sin(t*1.7+i) if t>q else 0
        tthuyen(cv,c,250+i*440,680+(i%2)*40,t,.36,True,False,[(CA[i%3],-80,'so')],nghieng=ng,ph=i)
    dem(cv,.35);mua(cv,t,.55);chop(cv,t,q+.3);chop(cv,t,q+1.9)
    nhan(cv,'lần nữa tiến thẳng vào kinh thành',960,150,t,a+.3,q,INK,40)
    nhan(cv,'gặp bão ở cửa Đại An · chết đuối rất nhiều',960,150,t,q+.2,b,RED,38)
# 43–44: viên quan không chịu lạy
def S_43(cv,t):
    a,b=T[43]-.3,E[44]+.3;q=T[44]
    c=kc(t,[(a,(960,620,1.0)),(q,(980,620,1.3)),(b,(980,600,1.45))])
    nen(cv,c,t,seed=43,mist=.3);put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9,o=.7)
    for x,y in [(560,560),(1350,560)]: lua(cv,c,x,y,t,.9,3,x*.01)
    P=rig.dung(t);P.update(mat='G',head=-6);ngd(cv,c,'dtb' if False else 'nd',980,945,t,.6,P)
    for i,(x,fl) in enumerate([(720,False),(820,False),(1140,True),(1240,True)]):
        PP=rig.dung(t+i);PP.update(arF=-60,faF=-10,lean=10);ngd(cv,c,CA[i%3],x,950,t,.54,PP,flip=fl,vk='giao')
    nhan(cv,'quân Chiêm Thành ép phải quỳ lạy',960,150,t,a+.3,q,INK,40)
    nhan(cv,'"ta là quan của nước lớn"',960,150,t,q+.2,b,RED,44)
# 45–46: men chân núi, voi phục sẵn
def S_45(cv,t):
    a,b=T[45]-.3,E[46]+.3;q=T[46]
    sh=4*math.sin(t*33) if not FREEZE and t>q else 0
    c=kc(t,[(a,(960,600,1.0)),(q,(960,600,1.0)),(b,(1050,610,1.15))],sh)
    nen(cv,c,t,seed=45,mist=.5)
    if t<q:
        for i in range(12): dib(cv,c,CA[i%3],1300-i*110,2600-i*110,930+(i%2)*10,t,a,q+6,s=.44,vk='giao',ph=i)
        voi(cv,c,lerp(-500,1500,inn(t,a,q+6-a)),940,t,.5)
    else:
        for i in range(3): voi(cv,c,lerp(-400-i*300,900+i*250,inn(t,q,1.8)),950+i*15,t,.62+i*.04,ph=i)
        for i in range(6): chay(cv,c,VA[i%4],1100+i*80,2300,940+(i%2)*12,t,q+.3+i*.1,b+1,.5,lambda ph,tt:rig.hoang(ph,tt,1.2),ph=i)
        bui2(cv,c,700,980,t,9,.75,.55)
    truoc(cv,c,t)
    nhan(cv,'năm 1383 · men theo chân núi',960,150,t,a+.3,q,INK,40)
    nhan(cv,'quân voi phục sẵn ào ra',960,150,t,q+.2,b,RED,42)
# 47–49: Nguyễn Mộng Hoa kéo thuyền vua
def S_47(cv,t):
    a,b=T[47]-.3,E[49]+.3;q=T[48];r=T[49]
    c=kc(t,[(a,(960,600,1.0)),(q,(1050,640,1.4)),(r,(1000,640,1.3)),(b,(800,600,1.0))])
    nen(cv,c,t,'song',seed=47,mist=.45);song_toi(cv,c,640,t)
    bx=lerp(1050,1700,inn(t,r,b-r))
    tthuyen(cv,c,bx,880,t,.8,False,False,[('nt',-60,None),('v10',110,'cheo')])
    if t<q: x=chay(cv,c,'nmh',300,850,960,t,a+.8,q,.56,lambda ph,tt:rig.hoang(ph,tt,1.0))
    elif t<r+.6:
        P=rig.dung(t);P.update(arF=-70,faF=-10,arB=-60,faB=-10,lean=22,mat='S');ngd(cv,c,'nmh',870,960,t,.56,P);song_nuoc(cv,870,940,t,q,n=2) if False else None
    else:
        P=rig.dung(t);P.update(head=12);ngd(cv,c,'nmh',870,960,t,.56,P)
    if not FREEZE and t>q:
        X,Y=c.p(870,900);k=.56*1.875
        ov=cv.copy();cv2.rectangle(ov,(int(X-90*k),int(Y-20*k)),(int(X+90*k),int(Y+60*k)),tuple(float(v) for v in INK*.35+PAPER*.65),-1);cv[:]=cv*.55+ov*.45
    nhan(cv,'thượng hoàng Trần Nghệ Tông lên thuyền lánh',960,150,t,a+.3,q,INK,38)
    nhan(cv,'người học trò Nguyễn Mộng Hoa níu thuyền vua',960,150,t,q+.2,r,RED,38)
    nhan(cv,'con thuyền vẫn rời bến',960,150,t,r+.2,b,INK,42)
# 50: lời Ngô Sĩ Liên
def S_50(cv,t):
    a,b=T[50]-.3,E[50]+.3
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.04))])
    nen(cv,c,t,'song',seed=50,mist=.5);song_toi(cv,c,640,t,o=.5)
    cuon(cv,960,470,t,'SỬ GIA NGÔ SĨ LIÊN','người học trò còn biết giữ vua|kẻ ăn lộc thật đáng khinh',col=RED,s=.72,sz=34,u=inn(t,a+.4,2.0),nm='t26n_cuon2')
# 51–53: Thanh Hóa, đập vỡ, voi ào ra
def S_51(cv,t):
    a,b=T[51]-.3,E[53]+.3;q=T[52];r=T[53]
    sh=4*math.sin(t*35) if not FREEZE and q+.6<t<r else 0
    c=kc(t,[(a,(960,600,1.0)),(q,(960,600,1.05)),(r,(1000,610,1.15)),(b,(1000,610,1.2))],sh)
    nen(cv,c,t,'song',seed=51,mist=.4);song_toi(cv,c,660,t)
    if t<q:
        ngua(cv,c,'nau','lql',300,1000,960,t,a,q,s=.6)
        for i in range(8): dib(cv,c,VA[i%4],-200-i*110,800-i*110,950+(i%2)*10,t,a,q+2,s=.48,vk='giao',ph=i)
        nhan(cv,'năm 1389 · Lê Quý Ly đem quân ra Thanh Hóa',960,150,t,a+.3,q,INK,38)
    else:
        put(cv,c,'t28n_dap',600,920,ay=1,s=.8,o=1-inn(t,q+.5,.6)*.6)
        nuocvo(cv,c,600,850,t,q+.5,1.2)
        for i in range(3): voi(cv,c,lerp(-300-i*250,900+i*230,inn(t,q+.9,1.8)),955+i*14,t,.6,ph=i)
        for i in range(6): chay(cv,c,VA[i%4],1000+i*90,2300,945,t,q+1.2+i*.1,b+1,.5,lambda ph,tt:rig.hoang(ph,tt,1.2),ph=i)
        bui2(cv,c,600,980,t,8,.7,.5)
        nhan(cv,'đập nước bị phá · voi trận ào ra như núi đổ',960,150,t,q+.2,r,RED,38)
        if t>r: ngua(cv,c,'nau','lql',900,-400,960,t,r+.3,b,s=.58,flip=True)
        nhan(cv,'bảy mươi tướng nhà Trần ngã xuống',960,150,t,r+.2,b,RED,40)
# 54: tìm người khác
def S_54(cv,t):
    a,b=T[54]-.3,E[54]+.3
    c=kc(t,[(a,(960,620,1.0)),(b,(1050,640,1.2))])
    nen(cv,c,t,seed=54,mist=.2);put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9);dem(cv,.25)
    ngd(cv,c,'nt',1050,940,t,.6,rig.ngoi(t)|{'head':10,'mat':'S'})
    nhan(cv,'ai sẽ chặn được Chế Bồng Nga?',960,150,t,a+.3,b,RED,42)
# 55–56: Trần Khát Chân nhận lệnh, cùng khóc
def S_55(cv,t):
    a,b=T[55]-.3,E[56]+.3;q=T[56]
    c=kc(t,[(a,(960,620,1.0)),(q,(980,620,1.35)),(b,(980,620,1.45))])
    nen(cv,c,t,seed=55,mist=.3);put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9,o=.8)
    P=rig.dung(t);P.update(arF=-80,faF=-6,mat='S' if t>q else '');ngd(cv,c,'nt',1150,935,t,.6,P,flip=True)
    if t<q+1.5: ngd(cv,c,'tkc',850,950,t,.6,quy(rig.so(t,.3)) if t>q else lay(rig.dung(t),t))
    else: dib(cv,c,'tkc',850,-300,950,t,q+1.5,b+1,s=.6,vk='dao')
    if t>q and not FREEZE:
        for (x,y) in [(880,760),(1150,745)]:
            X,Y=c.p(x,y);yy=int(Y+((t*60)%30));cv2.line(cv,(int(X),yy),(int(X),yy+8),(0.55,0.62,0.7),2,cv2.LINE_AA)
    nhan(cv,'Trần Khát Chân · dòng dõi Trần Bình Trọng',960,150,t,a+.3,q,VIETC,38)
    nhan(cv,'thượng hoàng cũng khóc',960,150,t,q+.2,b,RED,42)
# 57–58: không đánh, lui về Hải Triều
def S_57(cv,t):
    a,b=T[57]-.3,E[58]+.3;q=T[58]
    if t<q:
        c=kc(t,[(a,(960,600,1.0)),(q,(1100,600,1.15))])
        nen(cv,c,t,'song',seed=57,mist=.45);song_toi(cv,c,640,t)
        put(cv,c,'t26n_trai',1500,760,ay=1,s=.5,k=.7,o=.6)
        ngd(cv,c,'tkc',700,950,t,.62,rig.dung(t)|{'mat':'G'})
        for i in range(4): ngd(cv,c,VA[i],400-i*90,950,t,.5,rig.dung(t+i),vk='giao')
        nhan(cv,'Hoàng Giang · ông lại cho quân rút về',960,150,t,a+.3,q,INK,40)
    else:
        hg,ht=tuple(PTM['hoanggiang']),tuple(PTM['haitrieu'])
        c=mcam(t,[(q,(ht[0],ht[1],3.2)),(b,(ht[0],ht[1],3.6))])
        bando(cv,c,t,q-1);duong(cv,c,[hg,ht],t,q+.3,1.0,VIETC,4)
        diem(cv,c,'sông Hải Triều',ht,t,q+.8,VIETC,dx=24,dy=-10);pulse(cv,c,*ht,t)
        nhan(cv,'vì sao lại rút?',960,110,t,q,sb(58,1),RED,44)
        nhan(cv,'xem thế đất · không đánh được',960,110,t,sb(58,1),b,INK,40)
# 59–60: Nguyên Diệu sang hàng; hai bên chờ nhau
def S_59(cv,t):
    a,b=T[59]-.3,E[60]+.3;q=T[60]
    c=kc(t,[(a,(960,600,1.0)),(q,(960,580,1.0)),(b,(1000,580,1.08))])
    nen(cv,c,t,'song',seed=59,mist=.4);song_toi(cv,c,640,t)
    if t<q:
        dib(cv,c,'nd',300,1300,950,t,a,q,s=.58)
        for i in range(4): dib(cv,c,VA[i],100-i*110,1100-i*110,960,t,a,q,s=.5,vk='giao',ph=i)
        for i in range(3): ngd(cv,c,CA[i],1550+i*100,950,t,.52,rig.dung(t+i),flip=True,vk='giao')
        nhan(cv,'Nguyên Diệu đem quân sang hàng Chế Bồng Nga',960,150,t,a+.3,q,RED,38)
    else:
        put(cv,c,'t26n_trai',450,760,ay=1,s=.45,k=.7,o=.7);put(cv,c,'t26n_trai',1500,760,ay=1,s=.45,k=.7,o=.7)
        for x in (420,620,1420,1620): smoke(cv,c,x,700,t+x*.01,s=.6)
        put(cv,c,'t28n_rao',960,1000,ay=1,s=.65,k=1.1,o=.9)
        nhan(cv,'hai bên chờ nhau qua những ngày cuối năm',960,150,t,q+.2,b,INK,38)
# 61–63: hơn một trăm chiến thuyền, thuyền xanh
def S_61(cv,t):
    a,b=T[61]-.3,E[63]+.3;q=T[62];r=T[63]
    c=kc(t,[(a,(960,560,1.0)),(q,(1100,600,1.35)),(r,(960,580,1.0)),(b,(960,580,1.05))])
    nen(cv,c,t,'song',seed=61,mist=.45);song_toi(cv,c,600,t)
    for i in range(16):
        x=-200+(i%8)*300+((i*41)%80)+50*(t-a);y=620+(i//8)*80+((i*29)%30)
        tthuyen(cv,c,x,y,t,.18+.06*(i//8),True,False,[],ph=i,o=.5+.25*(i//8))
    tthuyen(cv,c,1100+40*(t-a),800,t,.5,True,False,[('c1',-320,'giao'),('cbn',-230,'dung'),('nd',230,'dung')],name='t28n_thuyenxanh',ph=2)
    if t>r: put(cv,c,'t28n_rao',960,1080,ay=1,s=.8,k=1.2)
    nhan(cv,'23 tháng giêng năm 1390',960,150,t,a+.3,q,RED,40)
    nhan(cv,'Chế Bồng Nga tận mắt dò xem thế trận',960,150,t,q+.2,r,INK,38)
    nhan(cv,'các thuyền chưa kịp tụ lại thành hàng',960,150,t,r+.2,b,INK,38)
# 64–66: Ba Lậu Kê chạy sang, chỉ tay
def S_64(cv,t):
    a,b=T[64]-.3,E[66]+.3;q=T[65];r=T[66]
    c=kc(t,[(a,(960,600,1.0)),(q,(900,630,1.35)),(r,(1100,600,1.1)),(b,(1300,600,1.2))])
    nen(cv,c,t,'song',seed=64,mist=.4);song_toi(cv,c,640,t)
    tthuyen(cv,c,1600,720,t,.32,True,False,[],name='t28n_thuyenxanh')
    for i in range(4): tthuyen(cv,c,1150+i*280,660+(i%2)*14,t,.2,True,False,[],ph=i,o=.6)
    if t<q: chay(cv,c,'blk',2100,850,940,t,a,q,.56,lambda ph,tt:rig.hoang(ph,tt,1.1))
    elif t<r: ngd(cv,c,'blk',800,950,t,.56,quy(rig.so(t,.9)))
    else:
        P=rig.dung(t);P.update(arF=-90+3*math.sin(t*4),faF=-2,lean=6,mat='S');ngd(cv,c,'blk',800,945,t,.56,P)
    P=rig.dung(t);P.update(mat='G' if t>r else '');ngd(cv,c,'tkc',620,945,t,.62,P)
    for i in range(2): ngd(cv,c,VA[i],420-i*100,950,t,.52,rig.dung(t+i),vk='giao')
    nhan(cv,'Ba Lậu Kê · người hầu của Chế Bồng Nga',960,150,t,a+.3,q,INK,38)
    nhan(cv,'sợ bị giết nên bỏ chủ',960,150,t,q+.2,r,RED,42)
    nhan(cv,'đó là thuyền của vua',960,150,t,r+.2,b,RED,46)
# 67: lời ấy thật hay giả? (ký ức Đồ Bàn)
def S_67(cv,t):
    a,b=T[67]-.3,E[67]+.3;q=sb(67,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(980,600,1.05))])
    nen(cv,c,t,seed=67,mist=.6)
    if t>q:
        put(cv,c,'t26n_trai',960,930,ay=1,s=.9,k=.8,o=.35)
        ngd(cv,c,'mbm',900,945,t,.56,quy(rig.so(t,.4)),o=.4);ngd(cv,c,'dt',1230,930,t,.6,rig.dung(t),flip=True,o=.4)
    nhan(cv,'lời ấy thật hay giả?',960,250,t,a+.2,q+.4,RED,52)
    nhan(cv,'mười ba năm trước ở Đồ Bàn',960,150,t,q+.2,b,INK,40)
# 68–70: hỏa súng
SUNG=[(500,0.0),(640,.25),(780,.5),(920,.15),(1060,.4)]
def S_68(cv,t):
    a,b=T[68]-.3,E[70]+.3;q=T[69];r=T[70]
    sh=6*math.sin(t*41)*(1-inn(t,q,.6)) if not FREEZE and q<t<q+.8 else 0
    if t<r:
        c=kc(t,[(a,(960,600,1.25)),(q,(960,600,1.0)),(r,(1100,600,1.05))],sh)
        nen(cv,c,t,'song',seed=68,mist=.4);song_toi(cv,c,640,t)
        tthuyen(cv,c,1650,720,t,.3,True,False,[],name='t28n_thuyenxanh')
        P=rig.quat(t) if t>a+1 else rig.dung(t);P['mat']='G';P.update(arF=-160,faF=-4) if t>q-.6 else None
        ngd(cv,c,'tkc',300,950,t,.64,P,vk='dao')
        for x,d in SUNG:
            PP=rig.dung(t);PP.update(arF=-75,faF=-15,arB=-60,faB=-20,lean=10,mat='G');ngd(cv,c,VA[int(x)%4],x,955,t,.52,PP,vk='sung')
            no(cv,c,x+80,760,t,q+d*.4,1.0)
        put(cv,c,'t28n_rao',960,1080,ay=1,s=.8,k=1.15)
        nhan(cv,'Trần Khát Chân không để lỡ một khắc',960,150,t,a+.3,q,VIETC,38)
        nhan(cv,'hỏa súng đồng loạt gầm lên',960,150,t,q+.2,r,RED,42)
    else:
        c=kc(t,[(r,(1000,620,1.3)),(b,(1000,640,1.45))],3*math.sin(t*30) if not FREEZE and t<r+.6 else 0)
        nen(cv,c,t,'song',seed=70,mist=.3);song_toi(cv,c,640,t)
        tthuyen(cv,c,1000,820,t,.62,True,False,[('c1',-320,'so'),('cbn',-230,'so' if t<r+.8 else 'khoc'),('nd',230,'so')],name='t28n_thuyenxanh',nghieng=8*inn(t,r,1))
        manh(cv,c,1000,760,t,r+.1,10,7);no(cv,c,1000,740,t,r,1.4)
        for x in (600,1400): smoke(cv,c,x,700,t,s=1.1)
        nhan(cv,'Chế Bồng Nga gục xuống trên chiếc thuyền của mình',960,150,t,r+.6,b,RED,36)
# 71–73: kêu khóc, Nguyên Diệu, đoàn thuyền tan vỡ
def S_71(cv,t):
    a,b=T[71]-.3,E[73]+.3;q=T[72];r=T[73]
    c=kc(t,[(a,(1000,640,1.4)),(q,(960,600,1.0)),(r,(960,580,1.0)),(b,(900,580,1.0))])
    nen(cv,c,t,'song',seed=71,mist=.4);song_toi(cv,c,620,t)
    if t<q:
        tthuyen(cv,c,1000,820,t,.62,True,False,[('c1',-320,'khoc'),('c2',-250,'khoc'),('c3',230,'khoc')],name='t28n_thuyenxanh',nghieng=8)
        smoke(cv,c,700,650,t,s=1.0)
        nhan(cv,'trên thuyền vang lên tiếng kêu khóc',960,150,t,a+.3,q,INK,40)
    elif t<r:
        x=chay(cv,c,'nd',400,1100,940,t,q,r,.56,lambda ph,tt:rig.hoang(ph,tt,1.1))
        for i in range(2): chay(cv,c,VA[i],1800+i*100,1250+i*80,945,t,q+.4,r-.6,.54,lambda ph,tt:rig.xung(ph*1.3),flip=True,vk='giao',ph=i)
        nhan(cv,'Nguyên Diệu cắt đầu Chế Bồng Nga chạy sang',960,150,t,q+.2,sb(72,1),INK,38)
        nhan(cv,'lính Long Tiệp giết luôn Nguyên Diệu',960,150,t,sb(72,1)+.2,r,RED,38)
    else:
        for i in range(10):
            dx=(-1 if i%2 else 1)*300*inn(t,r,b-r)
            tthuyen(cv,c,150+i*190+dx,640+(i%3)*40,t,.24,True,i%2==1,[(CA[i%3],-60,'so')],ph=i,nghieng=6*math.sin(i))
        for x in (500,1300): smoke(cv,c,x,640,t,s=1.0)
        nhan(cv,'cả đoàn thuyền tan vỡ',960,150,t,r+.2,b,RED,44)
# 74–77: canh ba ở Bình Than
def S_74(cv,t):
    a,b=T[74]-.3,E[77]+.3;q=T[75];r=T[76];s_=T[77]
    if t<q:
        c=kc(t,[(a,(960,600,1.0)),(q,(1000,600,1.06))])
        nen(cv,c,t,'song',seed=74,mist=.3);song_toi(cv,c,620,t);dem(cv,.6);trang(cv,c,1400,300,t)
        tthuyen(cv,c,lerp(400,1300,inn(t,a,q-a)),800,t,.4,False,False,[('v10',-40,'cheo'),('v9',50,None)])
        put(cv,c,'t24_hom',lerp(400,1300,inn(t,a,q-a))+10,760,s=.18)
        nhan(cv,'đầu Chế Bồng Nga trong một chiếc hòm',960,150,t,a+.3,q,INK,38)
    elif t<s_:
        c=kc(t,[(q,(960,620,1.3)),(r,(960,620,1.0)),(s_,(960,620,1.05))],2*math.sin(t*40) if not FREEZE and q<t<q+.4 else 0)
        nen(cv,c,t,seed=75,mist=.2);put(cv,c,'t26n_trai',960,930,ay=1,s=.9,k=.8);dem(cv,.55)
        lua(cv,c,520,880,t,.5,1);lua(cv,c,1420,880,t,.5,1)
        if t<r: ngd(cv,c,'nt',960,945,t,.62,rig.so(t,1.0))
        else:
            ngd(cv,c,'nt',960,945,t,.62,rig.reo(t)|{'mat':'V'})
            for i in range(6): ngd(cv,c,'lql' if i==0 else 'dtb' if i==1 else 'nd' if i==2 else VA[i%4],400+i*110 if i<3 else 1300+i*80,955,t,.52,rig.reo(t+i)|{'mat':'V'},flip=i>=3)
        nhan(cv,'canh ba · thượng hoàng giật mình tỉnh dậy',960,150,t,q+.2,r,INK,38)
        nhan(cv,'các quan hô muôn năm',960,150,t,r+.2,s_,VIETC,42)
    else:
        c=kc(t,[(s_,(960,600,1.0)),(b,(1000,600,1.1))])
        nen(cv,c,t,'song',seed=77,mist=.3);song_toi(cv,c,620,t);dem(cv,.5);trang(cv,c,1300,300,t)
        ngd(cv,c,'nt',800,950,t,.64,rig.dung(t))
        nhan(cv,'"như vua nhà Hán thấy đầu Hạng Vũ"',960,150,t,s_+.2,b,INK,38)
# 78–80: La Ngai rút về
def S_78(cv,t):
    a,b=T[78]-.3,E[80]+.3;q=T[79];r=T[80]
    if t<q:
        c=kc(t,[(a,(960,600,1.0)),(q,(1000,600,1.1))])
        nen(cv,c,t,'song',seed=78,mist=.3);song_toi(cv,c,660,t)
        lua(cv,c,960,880,t,1.3,4);dem(cv,.25)
        for i in range(8): ngd(cv,c,CA[i%3] if i else 'lng',560+i*110 if i<4 else 1100+i*80,950,t,.5,rig.dung(t+i)|{'head':12})
        nhan(cv,'La Ngai hỏa táng thi hài Chế Bồng Nga',960,150,t,a+.3,q,INK,38)
    elif t<r:
        c=kc(t,[(q,(960,600,1.0)),(r,(1050,600,1.08))])
        nen(cv,c,t,seed=79,mist=.4)
        vx=lerp(900,2100,inn(t,q,r-q+2));voi(cv,c,vx,950,t,.6,flip=False)
        for k in range(3): vang(cv,c,vx-150-k*170,960,10,k,o=1.0)
        for i in range(5): ngd(cv,c,VA[i%4],600-i*120,955,t,.5,lay(rig.dung(t+i),t+i) if t>q+.8 else rig.dung(t+i))
        nhan(cv,'rải tiền bạc trên đường rút',960,150,t,q+.2,r,RED,40)
    else:
        c=kc(t,[(r,(960,600,1.0)),(b,(980,600,1.05))])
        nen(cv,c,t,seed=80,mist=.4);put(cv,c,'t28n_doban',960,920,ay=1,s=.85,k=.6)
        ngd(cv,c,'lng',800,950,t,.6,rig.quat(t)|{'mat':'G'})
        for i in range(2): dib(cv,c,CA[i],1300+i*100,2300,960,t,r+.5,b+2,s=.5,ph=i)
        nhan(cv,'La Ngai tự lên làm vua',960,150,t,r+.2,b,INK,40)
# 81: gần hai mươi năm
def S_81(cv,t):
    a,b=T[81]-.3,E[81]+.3
    tl=tuple(PTM['thanglong'])
    c=mcam(t,[(a,(tl[0],tl[1]+100,1.6)),(b,(960,540,1.0))])
    bando(cv,c,t,a)
    for k in range(3): smoke(cv,c,tl[0]+k*12,tl[1]-20,t+k,s=.4)
    pulse(cv,c,*tl,t)
    nhan(cv,'gần hai mươi năm khói lửa',960,110,t,a+.3,b,RED,42)
# 82: kết
def S_82(cv,t):
    a=T[82]-.3;b=E[82]+4
    c=kc(t,[(a,(960,600,1.0)),(b,(1000,600,1.08))])
    nen(cv,c,t,'song',seed=82,mist=.5);song_toi(cv,c,640,t)
    tthuyen(cv,c,1100-40*(t-a),780,t,.42,True,False,[],name='t28n_thuyenxanh',nghieng=4)
    chim(cv,c,t,300,240,5,25,8);dem(cv,.15)
    if not FREEZE: put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,150,inn(t,E[82]+.6,1))
# ---------- ráp cảnh ----------
_L=[(1,S_1),(2,S_2),(3,S_3),(4,S_4),(5,S_5),(6,S_6),(8,S_8),(9,S_9),(10,S_10),(11,S_11),(12,S_12),(14,S_14),(15,S_15),(17,S_17),(18,S_18),(19,S_19),(21,S_21),(22,S_22),(23,S_23),(24,S_24),
 (25,S_25),(27,S_27),(28,S_28),(29,S_29),(32,S_32),(34,S_34),(35,S_35),(36,S_36),(37,S_37),(38,S_38),(40,S_40),(42,S_42),(43,S_43),(45,S_45),(47,S_47),(50,S_50),(51,S_51),(54,S_54),(55,S_55),(57,S_57),
 (59,S_59),(61,S_61),(64,S_64),(67,S_67),(68,S_68),(71,S_71),(74,S_74),(78,S_78),(81,S_81),(82,S_82)]
SC_LIST=[(0 if n==1 else (T[5]-3.6 if n==5 else T[n]-.3),f) for n,f in _L]
_SC_FN={id(f):tt for tt,f in SC_LIST}
def _wrap(f,t0):
    def g(cv,t):
        f(cv,t);chuyen(cv,t,t0)
    return g
SC_LIST=[(tt,_wrap(f,tt)) for tt,f in SC_LIST]
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
SH=[(SC_LIST[i][0],SC_LIST[i+1][0] if i<len(SC_LIST)-1 else V.TOTAL+1,SC_LIST[i][1]) for i in range(len(SC_LIST))]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm28_full.json'))
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
    if TT-3.4<t<TT+.2: title(cv,t,TT-3.2,'CHIẾC THUYỀN SƠN XANH','stitle28',.55)
    if not NOCAP: caps(cv,t)
V.NHAN={}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
