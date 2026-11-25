# dai_tm25: Ba bến sông (1285), lời kể bản 1, giọng Charon (25/11). Nhân vật múa rối riêng tập (t25n_r_*), có nét mặt sợ, giận, reo (headS/G/V)
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
V=K.setup('tm25',{5:4.0})
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
    put(cv,c,'t25_far',960+seed*60,g-120,ay=1,k=.35,o=far)
    put(cv,c,'t25_mid',960-seed*40,g+30,ay=1,k=.62,o=midv)
    suong(cv,c,t,g-260,mist,seed)
def truoc(cv,c,t,o=1):
    put(cv,c,'t25_frontL',-120,1120,ax=0,ay=1,k=1.3,s=.85,r=1.2*math.sin(t*.8),o=o)
    put(cv,c,'t25_frontR',2040,1120,ax=1,ay=1,k=1.3,s=.8,r=1.2*math.sin(t*.7+1),o=o)
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
        rg=np.random.default_rng(25);a=rg.random((34,60)).astype(np.float32)
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
    put(cv,c,'t25_far',960+sd*50,g-120,ay=1,k=.35,o=.85)
    if kieu=='song':
        put(cv,c,'t25_mid',960-sd*40,g-170,ay=1,k=.5,o=.6)
        put(cv,c,'t25_song',960,g-270,ay=0,k=.8,s=1.0,o=.95)
    else: put(cv,c,'t25_mid',960-sd*40,g+30,ay=1,k=.62,o=.8)
    suong(cv,c,t,g-260,mist,seed)
def song(cv,c,t,y=620,o=.95):
    put(cv,c,'t25_song',960,y,ay=0,k=.85,o=o)
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
        rig.ve23(cv,c,key,0,0,S_,PP,flip=flip,vk=vk,o=o,hip=c_pt(x+f*dx*S_,y-46*S_+bob))
    put(cv,c,Af(name) if flip else name,x,y+bob,s=S_,r=r,ay=.8,o=o,scale_px=3)
def c_pt(x,y): return (x,y)
def voi(cv,c,x,y,t,s=.6,flip=False,o=1.0,ph=0):
    S_=ss(y,s);put(cv,c,Af('t23n_voi') if flip else 't23n_voi',x,y-3*abs(math.sin(t*1.1+ph))*S_,s=S_,ay=1,r=.6*math.sin(t*.9+ph),o=o,scale_px=3)
def co(cv,c,name,x,y,t,s=.5,ph=0,flip=False):
    put(cv,c,Af(name) if flip else name,x,y,s=ss(y,s),ay=1,r=2.2*math.sin(t*2+ph))
def ten(cv,c,t,a,b,src,dst,n=8,h=120,seed=23,col=None):
    arrows(cv,c,t,a,b,src,dst,n=n,h=h,per=1.0,seed=seed,col=col if col is not None else MONGC)
def cuon(cv,x,y,t,tieu,chu,col=None,o=1.0,s=.62,sz=46,u=1.0):
    put(cv,C0,'t25_cuon',x,y,s=s,o=o)
    if FREEZE: return
    put_screen(cv,text(tieu,28,INK,700),x,y-170*s/.62,o)
    for k,ln in enumerate(chu.split('|')): put_screen(cv,wipe(text(ln,sz,col if col is not None else RED,700),u,0,.25,seed=int(x)+k),x,y-20+k*(sz+16),o)
def nhan(cv,txt,x,y,t,t0,t1,col=None,sz=40,w=None):
    if FREEZE or not(t0<t<t1): return
    u=inn(t,t0,.35)*(1-inn(t,t1-.35,.35));tx=text(txt,sz,col if col is not None else INK,700)
    put_screen(cv,band(w or tx.shape[1]+50,tx.shape[0]+26,PAPER,.86,18),x,y,u);put_screen(cv,tx,x,y,u)
for _k in ['qk','nd','tq','st1','st2','qt','hd','hc','tnt5','tts5','hdv5','tdo5','omn5','thn5','lh','lq','v4','v5','db1','db2','m4','m5','m6']: rig.PRE[_k]='t25n_r_'
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
def ngd(cv,c,key,x,y,t,s,P,flip=False,vk=None,o=1.0):
    rig.ve23(cv,c,key,x,y,ss(y,s),P,flip=flip,vk=vk,o=o)
def chay(cv,c,key,x0,x1,y,t,a,b,s,ham,flip=None,vk=None,ph=0,buoc=60,o=1.0):
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;S_=ss(y,s);pha=abs(x-x0)/(buoc*rig.SC*S_)*math.pi+ph
    P=ham(pha,t) if 0<u<1 else rig.dung(t+ph)
    rig.ve23(cv,c,key,x,y,S_,P,flip=(x1<x0) if flip is None else flip,vk=vk,o=o);return x
# A: đoạn 11, toán quân lạ trong hàng quân Trần Nhật Duật
def S_A(cv,t):
    a=T[11]-.3;q=sb(11,1);b=E[11]+.5
    if t<q:
        c=kc(t,[(a,(700,560,1.0)),(q,(1100,560,1.12))])
        nen(cv,c,t,'song',seed=11)
        co(cv,c,'t25_spr_coV',300,820,t,s=.45);co(cv,c,'t25_spr_coV',1700,820,t,s=.45,ph=1)
        for r,y in enumerate([800,850,905]):
            for i in range(7):
                k=['v4','v5','v4'][(i+r)%3];x=120+i*270+r*60
                if 3<=i<=4 and r==2: continue
                ngd(cv,c,k,x,y,t+i+r,.42+r*.06,rig.dung(t+i+r),vk=['giao','giao','no'][(i+r)%3])
        for i,k in enumerate(['st1','st2','tq']):
            P=rig.tron(rig.dung(t+i),rig.walk((t-a)*4+i,1.0),1.0 if a+.8<t<a+3 else 0)
            x=930+i*130+min(max(t-a-.8,0),2.2)*60
            ngd(cv,c,k,x,905+(i%2)*10,t,.58,P,vk='cung')
        truoc(cv,c,t)
    else:
        c=kc(t,[(q,(1050,700,1.45)),(b,(1100,690,1.6))])
        nen(cv,c,t,'song',seed=12,mist=.4)
        ngd(cv,c,'nd',700,905,t,.66,rig.quat(t),vk='cung')
        for i,k in enumerate(['st1','tq','st2','st1']):
            P=rig.dung(t+i);u=inn(t,q+.3+i*.25,.6);P.update(arF=-90*u+6,faF=-10*u-22,arB=-80*u,faB=-60*u-20)
            ngd(cv,c,k,1000+i*150,905+(i%2)*12,t,.62,P,vk='cung')
        co(cv,c,'t25_spr_coT',1650,860,t,s=.5)
        truoc(cv,c,t)
        nhan(cv,'người Tống mặc áo Tống, cầm cung tên',1150,200,t,q+.4,b,INK,40)
        nhan(cv,'Chiêu Văn Vương Trần Nhật Duật',560,330,t,q+.8,b,VIETC,36)
# B: đoạn 12, thượng hoàng sai người dặn khắp các quân
def S_B(cv,t):
    a=T[12]-.4;b=E[12]+.5;q=sb(12,1) if len(_SC[12])>2 else (a+b)/2
    c=kc(t,[(a,(700,540,1.15)),(b,(1200,560,1.0))])
    nen(cv,c,t,'song',seed=13)
    thuyen(cv,c,560,800,t,s=.62,lon=True,ngoi=[('tts5',-300,None),('v4',-220,None)])
    def bao(pha,t_): P=rig.walk(pha,1.4);P.update(arF=-100+20*math.sin(t_*5),faF=-20,lean=10);return P
    for i in range(2): chay(cv,c,['v5','db1'][i],500+i*80,2200,905+i*14,t,a+1.2+i*.5,b,.56,bao,ph=i)
    for i in range(5):
        x=900+i*260;look=inn(t,a+2+i*.6,.5)
        P=rig.dung(t+i);P['head']=-12*look
        ngd(cv,c,['v4','v5','st1','v4','st2'][i],x,905,t,.54,P,flip=look>.5,vk=['giao','giao','cung','no','cung'][i])
    truoc(cv,c,t)
    nhan(cv,'Thượng hoàng Trần Thánh Tông',560,330,t,a+.4,a+3.5,VIETC,36)
    nhan(cv,'đó là quân của Chiêu Văn Vương, nhận cho kỹ',960,170,t,a+3,b,INK,40)
# C: đoạn 13, quân Nguyên kinh hãi; tưởng nhà Tống sang giúp
def S_C(cv,t):
    a=T[13]-.3;q=sb(13,1);b=E[13]+.2
    if t<q:
        sh=3*math.sin(t*41)*inn(t,a+1.5,.6) if not FREEZE else 0
        c=kc(t,[(a,(960,660,1.3)),(q,(980,690,1.7))],sh)
        nen(cv,c,t,'song',seed=14,mist=.5)
        for i in range(4):
            x=1500+i*170;P=rig.dung(t+i);P['arF']=-140;P['faF']=-10
            ngd(cv,c,['st1','tq','st2','st1'][i],x,700,t,.36,P,vk='cung',flip=True,o=.75)
        co(cv,c,'t25_spr_coT',2150,680,t,s=.35)
        for i,k in enumerate(['m4','m5','lh','m6']):
            u=inn(t,a+1.0+i*.25,.7);x=640+i*190-70*inn(t,a+1.2+i*.25,1.6)
            P=tronm(rig.dung(t+i),rig.so(t+i,1.3),u,'S' if u>.3 else None)
            ngd(cv,c,k,x,905+(i%2)*10,t,.66,P,vk=None if u>.3 else ['daocong','moc','daocong','moc'][i])
            if 0<t-(a+1.0+i*.25)<1.2: roi(cv,c,['t23n_r_w_daocong','t23n_r_w_moc'][i%2],x+30,780,t,a+1.0+i*.25,dx=60,s=.4)
            if u<.3: pass
            else: run(cv,c,x+10,905-150*.66*rig.SC*1.0,s=.7,t=t)
        truoc(cv,c,t)
        if not FREEZE: ink_wash(cv,.18*inn(t,a+1,1))
        nhan(cv,'quân Nguyên kinh hãi',960,170,t,a+1.4,q,MONGC,44)
    else:
        c=kc(t,[(q,(900,700,1.5)),(b,(940,690,1.62))])
        nen(cv,c,t,'song',seed=15,mist=.6)
        g=inn(t,q+.3,1.4)
        for i in range(9):
            P=rig.dung(t+i);P['arF']=-150;P['faF']=-10
            ngd(cv,c,['st1','st2','tq'][i%3],1100+i*130,760+(i%3)*26,t,.5,P,vk='cung',flip=True,o=.38*g)
        for i in range(3): co(cv,c,'t25_spr_coT',1250+i*380,720,t,s=.45*g+.01,ph=i)
        def chi(t_):
            P=rig.quat(t_);P['mat']='S';return P
        ngd(cv,c,'m4',700,905,t,.7,chi(t),vk=None)
        ngd(cv,c,'m5',520,905,t,.68,rig.so(t,.8),flip=False)
        run(cv,c,530,905-150*.68*rig.SC,s=.8,t=t)
        truoc(cv,c,t)
        nhan(cv,'tưởng nhà Tống đã sang giúp',960,170,t,q+.3,b,RED,44)
# D: đoạn 14, quân Nguyên bỏ chạy; nhà Tống đã mất
def S_D(cv,t):
    a=T[14]-.2;q=sb(14,1);b=E[14]+.6
    if t<q+1.2:
        sh=4*math.sin(t*37)*(1-inn(t,a+.6,1.2)) if not FREEZE and t>a+.2 else 0
        c=kc(t,[(a,(900,640,1.15)),(q+1.2,(1250,620,1.0))],sh)
        nen(cv,c,t,seed=16)
        for i,k in enumerate(['m4','m5','lh','m6','m4','m5']):
            x0=500+i*220;t0=a+.15*i
            x=chay(cv,c,k,x0,x0+1500,905+(i%3)*12,t,t0,t0+3.2,.6,lambda ph,tt:rig.hoang(ph,tt),ph=i,buoc=55)
            roi(cv,c,['t23n_r_w_daocong','t23n_r_w_moc'][i%2],x0+20,905-110*.6*rig.SC,t,t0+.1,dx=-140,s=.6*GS if 905>700 else .6)
        put(cv,c,'t25_spr_coN',1250+200*inn(t,a,.6),880,s=.55,ay=1,r=-75*inn(t,a+.4,.9))
        bui(cv,c,800,900,t,a+.3,n=6)
        for i,k in enumerate(['v4','st1','v5','tq','st2']):
            x0=-100-i*200;chay(cv,c,k,x0,x0+1500,905+(i%2)*12,t,a+.6+i*.15,b,.6,lambda ph,tt:rig.xung(ph),ph=i,vk=['giao','cung','giao','cung','cung'][i])
        truoc(cv,c,t)
        nhan(cv,'quân Nguyên bỏ chạy',960,170,t,a+.3,q,RED,48)
    else:
        c=kc(t,[(q+1.2,(960,560,1.05)),(b,(960,540,1.12))])
        nen(cv,c,t,seed=17,mist=.7)
        put(cv,c,'t25_spr_coT',900,905,s=.8,ay=1,r=-80,o=.7)
        for i in range(3): ngd(cv,c,VA[i] if 'VA' in globals() else 'v4',300+i*200+300*inn(t,q+1.2,b-q),905,t,.5,rig.walk(t*3+i,.7),o=.6)
        for i in range(3): dust(cv,c,800+i*120,880,o=.25,s=.5+.05*math.sin(t+i))
        truoc(cv,c,t)
        if not FREEZE: ink_wash(cv,.3)
        nhan(cv,'nhà Tống đã mất năm 1279',960,330,t,q+1.3,b,INK,46)
for _k in ['hvv','tgh']: rig.PRE[_k]='t25n_r_'
VA=['v4','v5','v4'];MA=['m4','m5','m6']
def hang(cv,c,t,y0,n,x0,dx,keys,vk,s=.5,flip=False,ph=0,o=1.0,P=None):
    for i in range(n):
        k=keys[i%len(keys)];x=x0+i*dx
        ngd(cv,c,k,x,y0,t,s,(P(t+i+ph) if P else rig.dung(t+i+ph)),flip=flip,vk=vk[i%len(vk)],o=o)
def ongdong(cv,c,x,y,t,s=.5,flip=False,ph=0):
    """hai lính khiêng ống đồng chạy"""
    for j,dx in enumerate((-150,150)):
        P=rig.hoang(t*6+j+ph,t,1.0);P['arF']=-160;P['faF']=0;P['arB']=-150;P['faB']=0
        ngd(cv,c,['m5','m6'][j],x+dx*s/.5*(1 if not flip else -1),y,t,s,P,flip=flip)
    put(cv,c,Af('t25n_ongdong') if flip else 't25n_ongdong',x,y-205*s/.5+4*math.sin(t*12),s=s*.9,r=1.5*math.sin(t*12))
# 1: hook: ống đồng trên đường núi lúc chạng vạng
def S_1(cv,t):
    a,b=0,E[1]+.3
    c=kc(t,[(a,(1150,640,1.35)),(b,(950,620,1.2))])
    nen(cv,c,t,seed=1,mist=.6)
    ongdong(cv,c,1500-450*inn(t,a,b-a+1),905,t,s=.6)
    for i in range(2): chay(cv,c,['lq','m4'][i],1700+i*160,1250+i*160,905,t,a,b+1,.58,lambda ph,tt:rig.hoang(ph,tt,1.1),ph=i,flip=True,vk=['daocong',None][i])
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.28)
# 2: Thoát Hoan, con Hốt Tất Liệt
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3
    c=kc(t,[(a,(960,620,1.25)),(b,(980,580,1.05))])
    nen(cv,c,t,seed=2)
    put(cv,c,'t25n_trai',960,860,ay=1,s=.5,k=.85,o=.85)
    ngd(cv,c,'thn5',960,905,t,.72,rig.quat(t)|{'mat':''})
    for i in range(4): co(cv,c,'t25_spr_coN',560+i*270,880,t,s=.5,ph=i)
    hang(cv,c,t,905,4,380,160,MA,['daocong','moc'],s=.56,ph=1)
    hang(cv,c,t,905,3,1250,170,MA,['cung','moc'],s=.56,flip=True,ph=3)
    truoc(cv,c,t)
    nhan(cv,'Thoát Hoan · con trai hoàng đế nhà Nguyên',960,170,t,a+.6,b,MONGC,40)
# 3: bản đồ: Thoát Hoan giữ Thăng Long, hai gọng kìm
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3
    tl,th,ls=tuple(PTM['thanglong']),tuple(PTM['thanhhoa']),tuple(PTM['langson'])
    c=mcam(t,[(a,(520,640,1.4)),(b,(500,680,1.3))])
    bando(cv,c,t,a)
    for i in range(3): put(cv,c,'t25_spr_coN',tl[0]-12+i*12,tl[1]+2*math.sin(t*3+i),s=.12,ay=1)
    diem(cv,c,'Thăng Long',tl,t,a+.2,MONGC,dx=24,dy=24)
    bac=[(620,330),ls,(470,560),tl];nam=[(400,1075),th,(436,700),tl]
    duong(cv,c,bac,t,a+.5,b-a-1.2,MONGC,7);duong(cv,c,nam,t,a+.8,b-a-1.2,MONGC,7)
    for i,ps in enumerate([bac,nam]):
        for j in range(2): cotheo(cv,c,'t25_spr_coN',ps,t,a+.5+i*.3+j*.4,b-a-.8,s=.22,ph=i+j)
    pulse(cv,c,*tl,t)
    nhan(cv,'nhà Trần bị kẹp giữa hai gọng kìm',960,150,t,a+1.5,b,RED,40)
# 4: câu hỏi: từ kinh thành đến ống đồng
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+1.0;q=a+(b-a)*.5
    c=kc(t,[(a,(900,600,1.1)),(b,(1100,600,1.25))])
    nen(cv,c,t,seed=4,mist=.5)
    o1=1-inn(t,q-.5,1.0);o2=inn(t,q-.5,1.0)
    if o1>.02:
        put(cv,c,'t25n_trai',960,860,ay=1,s=.5,k=.85,o=.85*o1)
        ngd(cv,c,'thn5',900,905,t,.7,rig.quat(t)|{'mat':''},o=o1)
        hang(cv,c,t,905,3,1200,150,MA,['moc','daocong'],s=.55,o=o1,flip=True)
    if o2>.02:
        ongdong(cv,c,1300-200*inn(t,q,b-q),905,t,s=.6)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.25)
    nhan(cv,'chuyện gì đã xảy ra?',960,250,t,q,b,RED,48)
# 5: bản đồ: Toa Đô ra Thanh Hóa; hai vua vượt biển vào Thanh Hóa
def S_5(cv,t):
    a,b=T[5]-.3,E[6]+.3;q=T[6]
    tl,th,na=tuple(PTM['thanglong']),tuple(PTM['thanhhoa']),tuple(PTM['nghean'])
    c=mcam(t,[(a,(520,800,1.4)),(q,(540,760,1.45)),(b,(560,720,1.4))])
    bando(cv,c,t,a)
    diem(cv,c,'Thăng Long',tl,t,a,MONGC,dx=24,dy=24);diem(cv,c,'Thanh Hóa',th,t,a+.8,INK,dx=24,dy=-10)
    for i in range(3): put(cv,c,'t25_spr_coN',tl[0]-12+i*12,tl[1]+2*math.sin(t*3+i),s=.12,ay=1)
    nam=[(400,1075),na,th];duong(cv,c,nam,t,a+.3,q-a-1,MONGC,7)
    for i in range(3): cotheo(cv,c,'t25_spr_coN',nam,t,a+.3+i*.3,q-a-.6,s=.13,ph=i)
    if t>q:
        bien=[(600,650),(640,720),(560,800),(470,850),th]
        duong(cv,c,bien,t,q,b-q-.6,VIETC,6)
        for i in range(2): cotheo(cv,c,'t23n_thuyen',bien,t,q+i*.4,b-q-.3,s=.09,ph=i)
    nhan(cv,'Toa Đô từ Chiêm Thành đánh ra Thanh Hóa',960,150,t,a+.3,q-.1,MONGC,38);nhan(cv,'hai vua vượt biển vào Thanh Hóa',960,150,t,q+.1,b,VIETC,40)
# 6: chỗ yếu: đường lương xa
def S_6(cv,t):
    a,b=T[7]-.3,E[7]+.3;q=sb(7,1)
    c=kc(t,[(a,(1100,620,1.1)),(b,(800,620,1.2))])
    nen(cv,c,t,seed=6,mist=.6)
    def met(PP,t_): PP.update(lean=18,arF=-160,faF=0,arB=-150,faB=0,mat='S')
    for i in range(6):
        k=MA[i%3];x0=2000+i*190;x=x0-500*inn(t,a,b-a+3)
        P=rig.walk((t*2.2+i),.6);met(P,t)
        ngd(cv,c,k,x,905+(i%2)*12,t,.56,P,flip=True)
        put(cv,c,'t25n_hop',x,905-235*.56*rig.SC/2.2,s=.22,r=3*math.sin(t*2+i))
    truoc(cv,c,t)
    nhan(cv,'lương chở qua hàng vạn dặm',960,170,t,q,b,INK,42)
# 7: vua tính kế; đánh trở lại
def S_7(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1)
    if t<q:
        c=kc(t,[(a,(960,700,1.4)),(q,(1000,690,1.55))])
        nen(cv,c,t,seed=7,mist=.45)
        ngd(cv,c,'tnt5',820,905,t,.7,rig.quat(t)|{'mat':''})
        for i,k in enumerate(['qk','nd','hdv5']): ngd(cv,c,k,1120+i*150,905,t,.64,rig.dung(t+i),flip=True,vk=[None,'cung','dao'][i])
        truoc(cv,c,t)
        nhan(cv,'lấy sức nhàn mà chống sức mệt',960,170,t,a+.6,q,RED,42)
    else:
        c=kc(t,[(q,(800,620,1.1)),(b,(1100,600,1.0))])
        nen(cv,c,t,seed=8)
        for i in range(7):
            k=VA[i%3];x0=-100-i*150
            chay(cv,c,k,x0,x0+1500,905+(i%2)*12,t,q+i*.12,b+3,.56,lambda ph,tt:rig.xung(ph),ph=i,vk=['giao','no','giao'][i%3])
        for i in range(2): put(cv,c,'t25_spr_coV',-200+i*300+1400*inn(t,q,b-q+2),880,s=.5,ay=1,r=2*math.sin(t*3+i))
        truoc(cv,c,t)
        nhan(cv,'tháng tư · nhà Trần đánh trở lại',960,170,t,q+.2,b,VIETC,42)
# 8: bản đồ: Tây Kết, Hàm Tử
def S_8(cv,t):
    a,b=T[9]-.3,E[10]+.3;q=T[10]
    tk,ht,tl=tuple(PTM['tayket']),tuple(PTM['hamtu']),tuple(PTM['thanglong'])
    c=mcam(t,[(a,(470,660,2.4)),(b,(460,650,2.6))])
    bando(cv,c,t,a)
    diem(cv,c,'Thăng Long',tl,t,a,MONGC,dx=-24,dy=-20)
    diem(cv,c,'bến Tây Kết',tk,t,a+.6,RED,dx=24,dy=6)
    for i in range(3): put(cv,c,'t25_spr_coN',tk[0]-6+i*8,tk[1]-2+2*math.sin(t*3+i),s=.07,ay=1)
    d1=[(420,700),(440,670),(tk[0]-4,tk[1]+2)];duong(cv,c,d1,t,a+.4,q-a-.6,VIETC,4)
    for i in range(2): cotheo(cv,c,'t25_spr_coV',d1,t,a+.4+i*.3,q-a-.3,s=.07,ph=i)
    if t>q:
        diem(cv,c,'cửa ải Hàm Tử',ht,t,q,RED,dx=24,dy=24)
        d2=[(490,690),(470,660),(ht[0]+4,ht[1]+2)];duong(cv,c,d2,t,q,b-q-.4,VIETC,4)
        for i in range(2): cotheo(cv,c,'t25_spr_coV',d2,t,q+i*.3,b-q-.2,s=.07,ph=i+2)
        pulse(cv,c,*ht,t)
    nhan(cv,'Chiêu Thành Vương · Trần Quốc Toản · Nguyễn Khoái',960,150,t,a+.3,q-.1,VIETC,36)
# 13: người Tống chạy sang, Trần Nhật Duật thu nhận
def S_13(cv,t):
    a,b=T[15]-.3,E[15]+.3;q=sb(15,1)
    c=kc(t,[(a,(900,640,1.2)),(b,(1000,620,1.1))])
    nen(cv,c,t,'song',seed=13,mist=.55)
    if t<q:
        if not FREEZE: ink_wash(cv,.2)
        nhan(cv,'toán quân ấy từ đâu ra?',960,250,t,a+.3,q,RED,46)
    for i in range(2): thuyen(cv,c,1700-500*inn(t,q-.5,3),800+i*30,t,s=.5,flip=True,ngoi=[('st1',-40,None),('st2',40,None)],ph=i)
    ngd(cv,c,'nd',700,905,t,.66,rig.dung(t)|({'arF':-60,'faF':-40} if t>q+2 else {}))
    for i in range(2): ngd(cv,c,VA[i],450-i*140,905,t,.58,rig.dung(t+i),vk='giao')
    truoc(cv,c,t)
    nhan(cv,'nhà Tống mất · người Tống chạy sang nước ta',960,170,t,q+.2,b,INK,38)
# 14: Triệu Trung; công Nhật Duật nhiều hơn cả
def S_14(cv,t):
    a,b=T[16]-.3,E[16]+.3;q=sb(16,1)
    c=kc(t,[(a,(960,700,1.45)),(b,(960,680,1.25))])
    nen(cv,c,t,seed=14,mist=.45)
    ngd(cv,c,'nd',1150,905,t,.7,rig.dung(t),flip=True,vk='cung')
    def lay(PP,t_): PP.update(lean=14+3*math.sin(t_),arF=-40,faF=-50,arB=-30,faB=-50)
    dib(cv,c,'tq',500,880,905,t,a,a+2,s=.68,sua=lay)
    for i in range(3): ngd(cv,c,['st1','st2','st1'][i],300+i*120,905,t,.6,rig.dung(t+i),vk='cung')
    truoc(cv,c,t)
    nhan(cv,'Triệu Trung · tướng riêng của Trần Nhật Duật',960,170,t,a+.4,q-.1,VIETC,38);nhan(cv,'công đánh quân Nguyên nhiều hơn cả',960,170,t,q+.1,b,RED,40)
# 15: bản đồ: thắng ở Trường Yên; Toa Đô từ Thanh Hóa kéo ra
def S_15(cv,t):
    a,b=T[17]-.3,E[18]+.3;q=T[18]
    ty,th=tuple(PTM['hoalu']),tuple(PTM['thanhhoa'])
    c=mcam(t,[(a,(450,760,2.0)),(b,(450,740,1.8))])
    bando(cv,c,t,a)
    diem(cv,c,'phủ Trường Yên (Ninh Bình)',ty,t,a+.2,VIETC,dx=24,dy=-10)
    for i in range(2): put(cv,c,'t25_spr_coV',ty[0]-8+i*12,ty[1]+2*math.sin(t*3+i),s=.1,ay=1)
    pulse(cv,c,*ty,t,VIETC)
    if t>q:
        diem(cv,c,'Thanh Hóa',th,t,q,INK,dx=24,dy=10)
        len_=[th,(430,800),(424,760)];duong(cv,c,len_,t,q+.3,b-q-.6,MONGC,6)
        for i in range(3): cotheo(cv,c,'t25_spr_coN',len_,t,q+.3+i*.3,b-q-.3,s=.1,ph=i)
    nhan(cv,'ngày mồng ba tháng năm · thắng ở Trường Yên',960,150,t,a+.3,q-.1,VIETC,38);nhan(cv,'Toa Đô từ Thanh Hóa kéo ra',960,150,t,q+.1,b,MONGC,40)
# 16: người trốn về báo tin trong đêm
def S_16(cv,t):
    a,b=T[19]-.3,E[20]+.3;q=T[20]
    c=kc(t,[(a,(900,640,1.1)),(q,(1000,660,1.3)),(b,(1050,690,1.45))])
    nen(cv,c,t,seed=16,mist=.7)
    if not FREEZE: ink_wash(cv,.35)
    put(cv,c,'t25n_trai',1500,860,ay=1,s=.45,k=.85,o=.85)
    if t<q:
        chay(cv,c,'db1',-200,900,905,t,a+.3,b,.6,lambda ph,tt:rig.hoang(ph,tt,1.2)|{'mat':''},ph=0)
    else:
        def quy(PP,t_): PP.update(thF=-90,knF=90,thB=0,knB=90,lean=10,arF=-60,faF=-40,arB=-50,faB=-40)
        P=rig.dung(t);quy(P,t);ngd(cv,c,'db1',900,905,t,.62,P)
    ngd(cv,c,'tnt5',1250,905,t,.66,rig.dung(t),flip=True);ngd(cv,c,'tts5',1420,905,t,.64,rig.dung(t+1),flip=True)
    truoc(cv,c,t)
    nhan(cv,'đạo quân chính của Thoát Hoan đã gặp chuyện lớn',960,170,t,a+.3,q-.1,INK,38)
    nhan(cv,'ngày mồng mười · một tin vui',960,170,t,q+.1,b,VIETC,42)
# 17: Chương Dương: Trần Quang Khải dẫn quân và dân binh xông trận
def S_17(cv,t):
    a,b=T[21]-.3,E[22]+.3;q=T[22]
    hit=a+2.2;sh=(5*math.sin(t*37)*(1-inn(t,hit+.3,.6))) if hit<t<hit+.9 and not FREEZE else 0
    if t<q:
        c=kc(t,[(a,(800,690,1.4)),(q,(1000,650,1.15))],sh)
        nen(cv,c,t,'song',seed=17)
        chay(cv,c,'qk',200,1100,905,t,a+.2,q+1,.7,lambda ph,tt:rig.xung(ph),vk='dao')
        chay(cv,c,'qt',-100,850,905,t,a+.6,q+1,.62,lambda ph,tt:rig.xung(ph),vk='giao')
        put(cv,c,'t25_spr_coV',-100+950*inn(t,a+.6,q+.4-a),870,s=.5,ay=1,r=3*math.sin(t*4))
        for i in range(4):
            x0=1250+i*150;u=inn(t,hit+i*.15,.5)
            P=tronm(rig.dung(t+i),rig.so(t+i,1.2),u)
            ngd(cv,c,MA[i%3],x0+300*inn(t,hit+.4+i*.1,2),905+(i%2)*10,t,.6,P,flip=True,vk=None if u>.5 else 'daocong')
        truoc(cv,c,t)
        nhan(cv,'Thượng tướng Trần Quang Khải · bến Chương Dương',960,170,t,a+.3,q-.1,VIETC,38)
    else:
        c=kc(t,[(q,(1000,620,1.05)),(b,(1150,600,1.0))],sh)
        nen(cv,c,t,seed=18)
        for i in range(8):
            k=['db1','db2','v4','db1','v5','db2','qt','db1'][i];x0=-300-i*150
            P=lambda ph,tt,i=i:rig.xung(ph) if i%3 else rig.walk(ph,1.3)|{'arF':-160,'faF':0,'mat':'V'}
            chay(cv,c,k,x0,x0+1600,905+(i%2)*12,t,q+i*.1,b+1,.54,P,ph=i,vk=['giao','dao','giao','no','giao','dao','giao','dao'][i])
        bui(cv,c,700,900,t,q+.5,n=5)
        truoc(cv,c,t)
        nhan(cv,'dân binh các lộ',960,170,t,q+.3,b,VIETC,44)
# 18: quân Nguyên tan ở Chương Dương và kinh thành; Thoát Hoan chạy qua sông
def S_18(cv,t):
    a,b=T[23]-.3,E[23]+.3;q=sb(23,1)
    c=kc(t,[(a,(900,640,1.15)),(b,(1300,600,1.05))])
    nen(cv,c,t,'song',seed=19)
    put(cv,c,'t25_lua',600,880,ay=1,s=.5,o=.85*(.9+.1*math.sin(t*7)))
    for i in range(2): smoke(cv,c,520+i*160,560,t+i,1.0)
    put(cv,c,'t25_spr_coN',900,860,s=.5,ay=1,r=-80*inn(t,a+.6,.9))
    for i in range(5):
        x0=600+i*170;t0=a+.2+i*.15
        x=chay(cv,c,MA[i%3],x0,x0+1300,905+(i%2)*12,t,t0,t0+3.5,.56,lambda ph,tt:rig.hoang(ph,tt),ph=i)
        roi(cv,c,['t23n_r_w_daocong','t23n_r_w_moc'][i%2],x0+20,800,t,t0+.1,dx=-120,s=.5)
    if t>q-.5:
        thuyen(cv,c,1400+500*inn(t,q-.5,b-q+.5),800,t,s=.55,ngoi=[('thn5',-30,None),('m4',60,'cheo')])
    bui(cv,c,800,900,t,a+.3,n=5)
    truoc(cv,c,t)
    nhan(cv,'quân Nguyên tan vỡ ở Chương Dương và ở kinh thành',960,170,t,a+.3,q-.1,RED,38);nhan(cv,'Thoát Hoan rút chạy qua sông Hồng',960,170,t,q+.1,b,MONGC,40)
# 19: bản đồ: Thoát Hoan rút lên bắc, Toa Đô vẫn đang tới
def S_19(cv,t):
    a,b=T[24]-.3,E[24]+.3
    tl,th,ls=tuple(PTM['thanglong']),tuple(PTM['thanhhoa']),tuple(PTM['langson'])
    c=mcam(t,[(a,(500,620,1.35)),(b,(500,640,1.3))])
    bando(cv,c,t,a)
    diem(cv,c,'Thăng Long',tl,t,a,VIETC,dx=24,dy=24)
    rut=[tl,(470,540),ls,(620,330)];duong(cv,c,rut,t,a+.3,b-a-1.4,MONGC,6)
    for i in range(3): cotheo(cv,c,'t25_spr_coN',rut,t,a+.3+i*.3,b-a-.9,s=.22,ph=i)
    pulse(cv,c,*tl,t,VIETC)
    toi=[th,(430,800),(436,700)];duong(cv,c,toi,t,a+1.4,b-a-2,MONGC,6)
    for i in range(2): cotheo(cv,c,'t25_spr_coN',toi,t,a+1.4+i*.3,b-a-1.6,s=.22,ph=i+3)
    nhan(cv,'Thoát Hoan rút lên phía bắc',600,300,t,a+.6,b,MONGC,38);nhan(cv,'Toa Đô vẫn đang đi tới',1300,800,t,a+2,b,MONGC,38)
# 20: Hà Đặc ở Phù Ninh, lên núi Trĩ Sơn
def S_20(cv,t):
    a,b=T[25]-.3,E[26]+.3;q=T[26]
    c=kc(t,[(a,(1000,600,1.0)),(b,(800,560,1.15))])
    nen(cv,c,t,seed=20)
    for i in range(6):
        k=['hd','db1','db2','hc','db1','db2'][i];x0=1300+i*130
        chay(cv,c,k,x0,x0-900,905-i*6,t,a+.3+i*.2,b,.56,lambda ph,tt:rig.walk(ph,1.0)|{'lean':10},ph=i,vk=['giao','giao',None,'giao',None,'giao'][i])
    for i in range(3): chay(cv,c,MA[i],2400+i*150,1900+i*150,905,t,q,b,.5,lambda ph,tt:rig.walk(ph,1.0),ph=i,vk='daocong')
    truoc(cv,c,t)
    nhan(cv,'Hà Đặc · người đứng đầu huyện Phù Ninh',960,170,t,a+1.5,q-.1,VIETC,38);nhan(cv,'lên núi Trĩ Sơn để giữ',960,170,t,q+.1,b,VIETC,40)
# 21: hình người bằng tre, dẫn ra dẫn vào lúc chiều tối
def S_21(cv,t):
    a,b=T[27]-.3,E[27]+.3
    c=kc(t,[(a,(960,560,1.0)),(b,(900,620,1.2))])
    nen(cv,c,t,seed=21,mist=.6)
    if not FREEZE: ink_wash(cv,.3)
    for i in range(4):
        x=300+i*360+80*math.sin(t*.5+i);put(cv,c,'t25n_hinhnhan',x,700,s=.42,ay=1,r=2*math.sin(t+i))
        ngd(cv,c,['db1','db2','hc','db1'][i],x-60,700,t,.36,rig.walk(t*3+i,.8))
    for i in range(3): ngd(cv,c,MA[i],1300+i*170,905,t,.6,tronm(rig.dung(t+i),rig.so(t+i,.8),inn(t,a+1.5+i*.3,.8)),flip=False)
    truoc(cv,c,t)
    nhan(cv,'hình người bằng tre, mặc áo',960,170,t,a+.6,b,INK,42)
# 22: cây to bị tên lớn xuyên qua
def S_22(cv,t):
    a,b=T[28]-.3,E[28]+.3
    c=kc(t,[(a,(700,560,1.3)),(b,(900,600,1.1))])
    nen(cv,c,t,seed=22,mist=.5)
    put(cv,c,'t25_cay',700,900,ay=1,s=.6)
    for i in range(2):
        u=inn(t,a+1+i*.4,.8);P=tronm(rig.dung(t+i),rig.so(t+i,1.1),u);
        if u<.5: P.update(arF=-100,faF=-30)
        ngd(cv,c,MA[i],1150+i*190,905,t,.66,P,flip=True)
        if u>.5: run(cv,c,1150+i*190,905-150*.66*rig.SC,s=.8,t=t)
    truoc(cv,c,t)
    nhan(cv,'tên xuyên qua cả thân cây?',960,170,t,a+1.5,b,RED,44)
# 23: quân Hà Đặc xông ra, bắc cầu phao
def S_23(cv,t):
    a,b=T[29]-.3,E[29]+.3;q=sb(29,1)
    c=kc(t,[(a,(900,620,1.1)),(b,(1250,620,1.0))])
    nen(cv,c,t,'song' if t>q else 'dong',seed=23)
    for i in range(6):
        k=['hd','db1','db2','hc','db1','db2'][i];x0=-200-i*170
        chay(cv,c,k,x0,x0+1700,905+(i%2)*12,t,a+.3+i*.1,b,.56,lambda ph,tt:rig.xung(ph),ph=i,vk=['giao','giao','dao','giao','dao','giao'][i])
    for i in range(4):
        x0=900+i*160;chay(cv,c,MA[i%3],x0,x0+1300,905,t,a+.2+i*.1,a+3.5,.56,lambda ph,tt:rig.hoang(ph,tt),ph=i)
    if t>q:
        for i in range(6): put(cv,c,'t23n_thuyen',900+i*110,830+2*math.sin(t*2+i),s=.22*GS,ay=.8,r=90 if False else 0,o=inn(t,q+i*.15,.4))
    truoc(cv,c,t)
    nhan(cv,'bắc cầu phao qua sông',960,170,t,q+.2,b,VIETC,42)
# 24: Hà Đặc tử trận; Hà Chương lấy cờ giặc
def S_24(cv,t):
    a,b=T[30]-.3,E[30]+.3;q=sb(30,1)
    if t<q:
        c=kc(t,[(a,(900,700,1.4)),(q,(900,700,1.55))])
        nen(cv,c,t,seed=24,mist=.6)
        ngd(cv,c,'hd',900,905,t,.7,rig.nga(inn(t,a+.6,1.6)),vk=None)
        roi(cv,c,'t23n_r_w_giao',900,800,t,a+.6,dx=180,s=.5)
        truoc(cv,c,t)
        if not FREEZE: ink_wash(cv,.35*inn(t,a+.8,1))
        nhan(cv,'Hà Đặc tử trận',960,170,t,a+.8,q,INK,44)
    else:
        c=kc(t,[(q,(1000,620,1.1)),(b,(800,640,1.2))])
        nen(cv,c,t,seed=25,mist=.55)
        if not FREEZE: ink_wash(cv,.25)
        put(cv,c,'t25n_trai',1200,860,ay=1,s=.45,k=.85,o=.8)
        x=chay(cv,c,'hc',1300,200,905,t,q+.6,b+1,.6,lambda ph,tt:rig.hoang(ph,tt,1.1)|{'mat':''},flip=True)
        put(cv,c,'t25_spr_coN',x+30,905-120*.6*rig.SC*.6,s=.4,ay=1,r=-20)
        truoc(cv,c,t)
        nhan(cv,'Hà Chương lấy trộm cờ và áo của giặc',960,170,t,q+.2,b,VIETC,40)
# 25: giả làm quân giặc mà phá trại
def S_25(cv,t):
    a,b=T[31]-.3,E[31]+.3;q=sb(31,1)
    c=kc(t,[(a,(800,620,1.1)),(b,(1250,620,1.05))])
    nen(cv,c,t,seed=26)
    put(cv,c,'t25n_trai',1500,860,ay=1,s=.5,k=.85,o=.9)
    for i in range(5):
        k=['hc','db1','db2','db1','db2'][i];x0=-200-i*150;mode=t>q+.5
        f=(lambda ph,tt:rig.xung(ph)) if mode else (lambda ph,tt:rig.walk(ph,.9))
        x=chay(cv,c,k,x0,x0+1600,905+(i%2)*10,t,a+.3+i*.1,b+1,.56,f,ph=i,vk='giao' if mode else None)
        if i==0: put(cv,c,'t25_spr_coN',x+20,905-90*.56*rig.SC*.6,s=.42,ay=1,r=3*math.sin(t*3))
    for i in range(3):
        u=inn(t,q+.6+i*.2,.6);P=tronm(rig.dung(t+i)|{'arF':-130,'faF':-20},rig.so(t+i,1.2),u)
        ngd(cv,c,MA[i],1450+i*150,905,t,.56,P,flip=True)
    truoc(cv,c,t)
    nhan(cv,'giả làm quân giặc',960,170,t,a+.6,q,INK,44);nhan(cv,'trại giặc bị đánh phá',960,170,t,q+.4,b,RED,44)
# 26: bản đồ: Toa Đô, Ô Mã Nhi vào sông Thiên Mạc; Thoát Hoan đã bỏ kinh thành
def S_26(cv,t):
    a,b=T[32]-.3,E[33]+.3;q=T[33]
    tl,tm=tuple(PTM['thanglong']),tuple(PTM['thienmac'])
    c=mcam(t,[(a,(560,680,1.9)),(b,(500,640,2.0))])
    bando(cv,c,t,a)
    vao=[(720,760),(600,700),(500,670),tm,(436,615)];duong(cv,c,vao,t,a+.3,b-a-1.6,MONGC,5)
    for i in range(3): cotheo(cv,c,'t25_spr_coN',vao,t,a+.3+i*.3,b-a-1.2,s=.09,ph=i)
    diem(cv,c,'sông Thiên Mạc',tm,t,a+.8,INK,dx=24,dy=24);diem(cv,c,'Thăng Long',tl,t,a,INK,dx=-24,dy=-20)
    if t>q:
        rut=[tl,(460,560),(500,480)];duong(cv,c,rut,t,q,b-q-.4,MONGC,5)
        cotheo(cv,c,'t25_spr_coN',rut,t,q,b-q,s=.09,ph=5)
        nhan(cv,'Thoát Hoan đã bỏ kinh thành',960,150,t,sb(33,1),b,RED,40)
    nhan(cv,'Toa Đô, Ô Mã Nhi muốn hội quân với Thoát Hoan',960,150,t,a+.3,q-.1,MONGC,38)
# 27: bến Đại Mang; Trương Hiển ra hàng
def S_27(cv,t):
    a,b=T[34]-.3,E[34]+.3;q=sb(34,1)
    c=kc(t,[(a,(800,620,1.05)),(b,(1050,680,1.3))])
    nen(cv,c,t,'song',seed=27)
    for i in range(3): thuyen(cv,c,300+i*420+200*inn(t,a,q-a),800+(i%2)*25,t,s=.5,lon=(i==1),ngoi=[('tnt5',-300,None),('tts5',-230,None)] if i==1 else [('v4',-50,'cheo'),('v5',40,'cheo')],ph=i)
    if t>q:
        def quy(PP,t_): PP.update(thF=-90,knF=90,thB=0,knB=90,lean=14,arF=-60,faF=-40,arB=-50,faB=-40)
        P=rig.dung(t);quy(P,t);dib(cv,c,'tgh',1600,1300,905,t,q,q+1.5,s=.62,flip=True) if t<q+1.5 else ngd(cv,c,'tgh',1300,905,t,.62,P,flip=True)
    truoc(cv,c,t)
    nhan(cv,'bến Đại Mang',960,170,t,a+.3,q-.1,VIETC,42);nhan(cv,'Trương Hiển · tổng quản quân Nguyên ra hàng',960,170,t,q+.1,b,MONGC,38)
# 28: Tây Kết: Toa Đô bị chém
def S_28(cv,t):
    a,b=T[35]-.3,E[36]+.3;q=T[36]
    hit=a+1.5;sh=(5*math.sin(t*37)*(1-inn(t,hit+.3,.6))) if hit<t<hit+.9 and not FREEZE else 0
    if t<q:
        c=kc(t,[(a,(900,640,1.1)),(q,(1050,680,1.35))],sh)
        nen(cv,c,t,'song',seed=28)
        for i in range(5):
            k=['v4','qt','v5','db1','v4'][i];x0=-200-i*160
            chay(cv,c,k,x0,x0+1200,905+(i%2)*12,t,a+.2+i*.1,q,.56,lambda ph,tt:rig.xung(ph),ph=i,vk=['giao','giao','dao','giao','dao'][i])
        ngd(cv,c,'tdo5',1250,905,t,.66,rig.nga(inn(t,hit,1.6)) if t>hit else rig.quat(t),flip=True,vk=None if t>hit else 'daocong')
        if t>hit: roi(cv,c,'t23n_r_w_daocong',1250,780,t,hit,dx=160,s=.55)
        put(cv,c,'t25_spr_coN',1500,880,s=.5,ay=1,r=-80*inn(t,hit+.3,.9))
        for i in range(3):
            x0=1450+i*160;chay(cv,c,MA[i],x0,x0+900,905,t,hit+.2+i*.1,q,.56,lambda ph,tt:rig.hoang(ph,tt),ph=i)
        truoc(cv,c,t)
        nhan(cv,'Tây Kết · chém đầu nguyên soái Toa Đô',960,170,t,hit+.4,q,RED,40)
    else:
        c=kc(t,[(q,(960,560,1.05)),(b,(960,540,1.12))])
        nen(cv,c,t,'song',seed=29,mist=.7)
        put(cv,c,'t25_spr_coN',960,860,s=.6,ay=1,r=-85,o=.75)
        for i in range(3): dust(cv,c,860+i*100,850,o=.25,s=.5+.05*math.sin(t+i))
        truoc(cv,c,t)
        if not FREEZE: ink_wash(cv,.3)
        nhan(cv,'hẹn ba năm san phẳng nước ta',960,330,t,q+.2,b,INK,44)
# 29: Ô Mã Nhi trốn ra biển; bắt năm vạn quân
def S_29(cv,t):
    a,b=T[37]-.3,E[38]+.3;q=T[38]
    if t<q:
        c=kc(t,[(a,(900,560,1.0)),(q,(1200,560,1.1))])
        nen(cv,c,t,'song',seed=30,mist=.7)
        if not FREEZE: ink_wash(cv,.4)
        thuyen(cv,c,600+900*inn(t,a,q-a),790,t,s=.5,ngoi=[('omn5',-20,None),('m4',60,'cheo')])
        for i in range(3): thuyen(cv,c,-200-i*300+700*inn(t,a+1,q-a),830,t,s=.46,ngoi=[('v4',-40,'cheo'),('v5',40,'giao')],ph=i)
        truoc(cv,c,t)
        nhan(cv,'Ô Mã Nhi chỉ còn một chiếc thuyền',960,170,t,sb(37,1),q,MONGC,40)
    else:
        c=kc(t,[(q,(960,640,1.1)),(b,(960,600,1.0))])
        nen(cv,c,t,seed=31)
        def quy(PP,t_): PP.update(thF=-90,knF=90,thB=0,knB=90,lean=14,arF=30,faF=-70,arB=20,faB=-70,mat='S')
        for r,y in enumerate([820,860,905]):
            for i in range(8):
                P=rig.dung(t+i+r);quy(P,t);ngd(cv,c,MA[(i+r)%3],200+i*210+r*60,y,t,.44+r*.06,P,flip=True)
        for i in range(3): dib(cv,c,VA[i],1700+i*130,1500+i*130,905,t,q,b,s=.58,vk='giao',flip=True,ph=i)
        truoc(cv,c,t)
        nhan(cv,'hơn năm vạn quân Nguyên bị bắt (theo sử nước ta)',960,170,t,q+.2,b,INK,38)
# 30: cái hộp và chiếc áo
def S_30(cv,t):
    a,b=T[39]-.3,E[40]+.3;q=sb(39,1);r=T[40]
    c=kc(t,[(a,(960,700,1.3)),(r,(960,700,1.45)),(b,(960,680,1.3))])
    nen(cv,c,t,seed=32,mist=.45)
    sad=t>q
    ngd(cv,c,'tnt5',1150,905,t,.7,rig.dung(t)|({'head':8,'lean':4} if sad and t<r else {})|({'arF':-70,'faF':-40} if t>r else {}),flip=True)
    if t<r:
        dib(cv,c,'v4',300,760,905,t,a,a+2,s=.62,sua=lambda PP,t_: PP.update(arF=-70,faF=-60,arB=-70,faB=-60))
        put(cv,c,'t25n_hop',min(760,300+460*inn(t,a,2))+60,905-110*.62*rig.SC*.5,s=.3)
    else:
        put(cv,c,'t25_quan',800,905,ay=1,s=.45)
        u=inn(t,r+.5,1.5);put(cv,c,'t25_ao',800+200*(1-u),905-80-60*(1-u),s=.4,o=u,r=-15*(1-u))
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.18)
    nhan(cv,'người làm tôi phải nên như thế này',960,170,t,q+.3,r-.1,RED,42)
    nhan(cv,'vua cởi áo ngự, sai liệm chôn Toa Đô',960,170,t,r+.2,b,INK,40)
# 31: tẩm dầu để răn; lời Ngô Sĩ Liên
def S_31(cv,t):
    a,b=T[41]-.3,E[42]+.3;q=T[42]
    c=kc(t,[(a,(960,640,1.15)),(b,(960,560,1.0))])
    nen(cv,c,t,seed=33,mist=.6)
    put(cv,c,'t25n_hop',960,905,ay=1,s=.5)
    for i in range(2): ngd(cv,c,VA[i],760+i*400,905,t,.62,rig.dung(t+i),flip=(i==1),vk='giao')
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3*inn(t,a,.6)+.15*inn(t,q,.5))
    nhan(cv,'mượn đường vào cướp nước ta suốt ba năm',960,170,t,a+.6,q-.1,RED,40)
    if t>q: cuon(cv,960,470,t,'NGÔ SĨ LIÊN, GẦN 200 NĂM SAU','lời của|bậc đế vương',col=INK,u=inn(t,q+.3,.8))
# 32: Vạn Kiếp: quân Nguyên chết đuối
def S_32(cv,t):
    a,b=T[43]-.3,E[44]+.3;q=T[44]
    hit=q+1;sh=(5*math.sin(t*37)*(1-inn(t,hit+.3,.6))) if hit<t<hit+.9 and not FREEZE else 0
    c=kc(t,[(a,(900,620,1.05)),(q,(1000,640,1.15)),(b,(1100,620,1.05))],sh)
    nen(cv,c,t,'song',seed=34)
    if t<q:
        thuyen(cv,c,600+600*inn(t,a,q-a),800,t,s=.55,ngoi=[('thn5',-30,None),('lh',40,'daocong')])
    else:
        chay(cv,c,'hdv5',-200,700,905,t,q,b,.68,lambda ph,tt:rig.xung(ph),vk='dao')
        for i in range(4): chay(cv,c,VA[i%3],-400-i*150,500-i*150+300,905,t,q+.2+i*.1,b,.56,lambda ph,tt:rig.xung(ph),ph=i,vk='giao')
        for i in range(5):
            x=1000+i*170;u=inn(t,hit+i*.15,.9)
            P=tronm(rig.dung(t+i),rig.so(t+i,1.4),.8);ngd(cv,c,MA[i%3],x,905+60*u,t,.56,P,flip=True,o=1-.85*u)
            if u>0: dust(cv,c,x,880,o=.4*(1-u)+.1,s=.3+.3*u)
    truoc(cv,c,t)
    nhan(cv,'Thoát Hoan đang chạy ngược lên phía bắc',960,170,t,a+.3,q-.1,MONGC,40);nhan(cv,'Vạn Kiếp · quân Nguyên chết đuối rất nhiều',960,170,t,q+.3,b,RED,40)
# 33: Lý Hằng trúng tên độc
def S_33(cv,t):
    a,b=T[45]-.3,E[45]+.3;q=sb(45,1)
    c=kc(t,[(a,(1000,620,1.05)),(b,(1100,660,1.25))])
    nen(cv,c,t,seed=35)
    ngua(cv,c,'den','thn5',300,1500,900,t,a,b,s=.58)
    if t<q+.6: ngua(cv,c,'nau','lh',100,1300,900,t,a,q+.6,s=.6,vk='daocong')
    else:
        ngd(cv,c,'lh',1240,905,t,.6,rig.nga(inn(t,q+.6,1.4)))
    ten(cv,c,t,q-.4,q+.7,[(200,760),(250,740)],[(1150,820),(1180,830)],n=3,h=40,col=VIETC)
    truoc(cv,c,t)
    nhan(cv,'Lý Hằng · trúng tên tẩm thuốc độc',960,170,t,q+.6,b,MONGC,40)
# 34: Lý Quán giấu Thoát Hoan vào ống đồng
def S_34(cv,t):
    a,b=T[46]-.3,E[47]+.3;q=sb(46,1);r=T[47]
    if t<r:
        c=kc(t,[(a,(960,700,1.3)),(r,(960,700,1.5))])
        nen(cv,c,t,seed=36,mist=.5)
        put(cv,c,'t25n_ongdong',1050,860,s=.55)
        ngd(cv,c,'lq',650,905,t,.68,rig.quat(t),vk=None)
        u=inn(t,q+.3,1.6)
        ngd(cv,c,'thn5',900+150*u,905-60*u,t,.6,rig.so(t,.6),o=1-.95*inn(t,q+1.4,.5))
        truoc(cv,c,t)
        nhan(cv,'Lý Quán thu nhặt năm vạn quân còn lại',960,170,t,a+.3,q-.1,MONGC,40)
    else:
        c=kc(t,[(r,(1100,640,1.3)),(b,(900,620,1.15))])
        nen(cv,c,t,seed=37,mist=.6)
        ongdong(cv,c,1500-700*inn(t,r,b-r+1),905,t,s=.6)
        for i in range(4): chay(cv,c,MA[i%3],1900+i*160,1100+i*160,905,t,r,b+1,.55,lambda ph,tt:rig.hoang(ph,tt),ph=i,flip=True)
        truoc(cv,c,t)
        if not FREEZE: ink_wash(cv,.2)
        nhan(cv,'cái ống đồng ở đầu câu chuyện',960,170,t,r+.2,b,RED,44)
# 35: Hưng Vũ Vương bắn Lý Quán ở Tư Minh
def S_35(cv,t):
    a,b=T[48]-.3,E[49]+.3;q=sb(48,1);r=T[49]
    c=kc(t,[(a,(900,620,1.1)),(r,(1100,620,1.05)),(b,(1300,600,1.0))])
    nen(cv,c,t,seed=38)
    if t<r:
        ngd(cv,c,'hvv',500,905,t,.66,rig.dung(t)|{'arF':-90,'faF':0,'arB':-80,'faB':-10,'mat':'G'},vk='cung')
        ten(cv,c,t,q-1,q,[(600,760),(620,750)],[(1300,800),(1320,810)],n=4,h=60,col=VIETC)
        ngd(cv,c,'lq',1300,905,t,.64,rig.nga(inn(t,q,1.4)) if t>q else rig.hoang(t*6,t),flip=False)
        ongdong(cv,c,1600+200*inn(t,a,r-a),905,t,s=.5)
        nhan(cv,'Hưng Vũ Vương · con trai Hưng Đạo Vương',960,170,t,a+.3,q-.1,VIETC,38);nhan(cv,'Tư Minh · Lý Quán bị bắn chết',960,170,t,q+.1,r,RED,40)
    else:
        ongdong(cv,c,1600+800*inn(t,r,b-r+1),905,t,s=.45)
        for i in range(3): chay(cv,c,MA[i],1500+i*160,2400+i*160,905,t,r,b+1,.5,lambda ph,tt:rig.hoang(ph,tt),ph=i)
        nhan(cv,'chuyện ống đồng chỉ thấy chép trong sử nước ta',960,170,t,sb(49,1),b,INK,38)
    truoc(cv,c,t)
# 36: bản đồ: cả hai cánh đã tan
def S_36(cv,t):
    a,b=T[50]-.3,E[50]+.3
    tl,th,ls,tk=tuple(PTM['thanglong']),tuple(PTM['thanhhoa']),tuple(PTM['langson']),tuple(PTM['tayket'])
    c=mcam(t,[(a,(500,640,1.3)),(b,(500,620,1.25))])
    bando(cv,c,t,a)
    diem(cv,c,'Thăng Long',tl,t,a,VIETC,dx=24,dy=24)
    rut=[tl,(470,540),ls,(640,300)];duong(cv,c,rut,t,a+.3,b-a-.8,MONGC,6);cotheo(cv,c,'t25_spr_coN',rut,t,a+.3,b-a-.4,s=.12)
    for i in range(3): put(cv,c,'t25_spr_coV',tl[0]-10+i*12,tl[1]+2*math.sin(t*3+i),s=.12,ay=1)
    diem(cv,c,'Tây Kết',tk,t,a+.8,RED,dx=24,dy=10);pulse(cv,c,*tk,t)
    nhan(cv,'cả hai cánh quân Nguyên đều tan',960,150,t,a+.6,b,RED,42)
# 37: hai vua về kinh; dân reo
def S_37(cv,t):
    a,b=T[51]-.3,E[51]+.3;q=sb(51,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(900,660,1.2))])
    nen(cv,c,t,seed=39)
    put(cv,c,'t23_thanh',960,880,ay=1,s=.55,k=.85,o=.9)
    for i,k in enumerate(['tnt5','tts5']): ngua(cv,c,['trang','nau'][i],k,-300-i*220,700-i*220,900,t,a,b,s=.56)
    for i in range(6): ngd(cv,c,['db1','db2','v4','db1','v5','db2'][i],1050+i*140,905+(i%2)*10,t,.52,rig.reo(t+i),flip=True)
    truoc(cv,c,t)
    nhan(cv,'ngày mồng sáu tháng sáu · hai vua về kinh',960,170,t,a+.3,q,VIETC,40);nhan(cv,'Thượng tướng Trần Quang Khải làm thơ',960,170,t,q+.1,b,INK,40)
# 38: bài thơ
def S_38(cv,t):
    a,b=T[52]-.3,E[53]+.3;q=T[53]
    c=kc(t,[(a,(960,620,1.05)),(b,(960,600,1.12))])
    nen(cv,c,t,'song',seed=40,mist=.6)
    ngd(cv,c,'qk',1500,905,t,.66,rig.dung(t)|{'arF':-50,'faF':-60},flip=True)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.25)
    if t<q: cuon(cv,760,470,t,'TRẦN QUANG KHẢI','Đoạt sáo Chương Dương độ|Cầm Hồ Hàm Tử quan',col=RED,s=.8,sz=34,u=inn(t,a+.6,2.4))
    else: cuon(cv,760,470,t,'TRẦN QUANG KHẢI','Thái bình tu trí lực|Vạn cổ thử giang san',col=RED,s=.8,sz=34,u=inn(t,q+.3,2.0))
# 39: kết
def S_39(cv,t):
    a=T[54]-.3;b=E[54]+4
    c=kc(t,[(a,(900,600,1.05)),(b,(1100,560,1.0))])
    nen(cv,c,t,'song',seed=41,mist=.65)
    for i in range(3): thuyen(cv,c,200+i*500+200*inn(t,a,b-a),800+(i%2)*25,t,s=.46,ngoi=[('v4',-50,'cheo'),('v5',40,'cheo')],ph=i)
    put(cv,c,'t25n_ongdong',1500,905,ay=1,s=.35,o=.5)
    truoc(cv,c,t)
    if not FREEZE: put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,150,inn(t,E[54]+.6,1))
# ---------- ráp cảnh ----------
SC_LIST=[(0,S_1),(T[2]-.3,S_2),(T[3]-.3,S_3),(T[4]-.3,S_4),(T[5]-.3,S_5),(T[7]-.3,S_6),(T[8]-.3,S_7),(T[9]-.3,S_8),
 (T[11]-.3,S_A),(T[12]-.4,S_B),(T[13]-.3,S_C),(T[14]-.2,S_D),(T[15]-.3,S_13),(T[16]-.3,S_14),(T[17]-.3,S_15),(T[19]-.3,S_16),
 (T[21]-.3,S_17),(T[23]-.3,S_18),(T[24]-.3,S_19),(T[25]-.3,S_20),(T[27]-.3,S_21),(T[28]-.3,S_22),(T[29]-.3,S_23),(T[30]-.3,S_24),
 (T[31]-.3,S_25),(T[32]-.3,S_26),(T[34]-.3,S_27),(T[35]-.3,S_28),(T[37]-.3,S_29),(T[39]-.3,S_30),(T[41]-.3,S_31),(T[43]-.3,S_32),
 (T[45]-.3,S_33),(T[46]-.3,S_34),(T[48]-.3,S_35),(T[50]-.3,S_36),(T[51]-.3,S_37),(T[52]-.3,S_38),(T[54]-.3,S_39)]
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
SH=[(SC_LIST[i][0],SC_LIST[i+1][0] if i<len(SC_LIST)-1 else V.TOTAL+1,SC_LIST[i][1]) for i in range(len(SC_LIST))]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm25_full.json'))
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
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'BA BẾN SÔNG','stitle25',.55)
    if not NOCAP: caps(cv,t)
V.NHAN={9:'Trần Quốc Toản – Hoài Văn hầu',21:'Trần Quang Khải – Thượng tướng',35:'Toa Đô – nguyên soái nhà Nguyên',44:'Trần Quốc Tuấn – Hưng Đạo Vương'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
