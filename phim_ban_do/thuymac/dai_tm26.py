# dai_tm26: Thuyền lương ở Vân Đồn (1287–1288), lời kể bản 2, giọng Charon (25/11). Nhân vật múa rối riêng tập (t26n_r_*), có nét mặt sợ, giận, reo (headS/G/V)
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
V=K.setup('tm26',{5:4.0})
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
        rg=np.random.default_rng(26);a=rg.random((34,60)).astype(np.float32)
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
def ngd(cv,c,key,x,y,t,s,P,flip=False,vk=None,o=1.0):
    rig.ve23(cv,c,key,x,y,ss(y,s),P,flip=flip,vk=vk,o=o)
def chay(cv,c,key,x0,x1,y,t,a,b,s,ham,flip=None,vk=None,ph=0,buoc=60,o=1.0):
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;S_=ss(y,s);pha=abs(x-x0)/(buoc*rig.SC*S_)*math.pi+ph
    P=ham(pha,t) if 0<u<1 else rig.dung(t+ph)
    rig.ve23(cv,c,key,x,y,S_,P,flip=(x1<x0) if flip is None else flip,vk=vk,o=o);return x
VA=['v6','v7','v8'];MA=['m7','m8','m9']
def quy(P):
    P=dict(P);P.update(thF=-90,knF=90,thB=0,knB=90,lean=10,arF=-60,faF=-40,arB=-50,faB=-40);return P
def lay(P,t_=0):
    P=dict(P);P.update(lean=14+3*math.sin(t_),arF=-40,faF=-50,arB=-30,faB=-50);return P
def ngam(P):
    """đưa tay lên trán nhìn xa"""
    P=dict(P);P.update(arF=-150,faF=-110,head=-4);return P
def bien(cv,c,t,seed=0,mist=.5,dao=True,y=560,bo=False):
    sd=(seed*37)%7-3
    put(cv,c,'t26_bien',960+sd*60,y+140,ay=1,k=.35,o=.9)
    put(cv,c,'t26_song',960+sd*30,y+40,ay=0,k=.8,s=1.0,o=.95)
    suong(cv,c,t,y-160,mist,seed)
    if bo:
        put(cv,c,band(4200,300,(.80,.74,.62),.97,40),960,1040,k=1.0)
        put(cv,c,'t26_mid',960-sd*40,1000,ay=1,k=1.0,s=1.0,o=.35)
def daotruoc(cv,c,t,o=.95,sd=0):
    put(cv,c,'t26_dao',960+((sd*53)%5-2)*120,1100,ay=1,k=1.25,s=1.0,o=o)
def thuyenluong(cv,c,x,y,t,s=.6,flip=False,ngoi=(),o=1.0,ph=0,day=1.0):
    """thuyền lương: thuyền lớn chở bao gạo"""
    if y>=880: y-=140
    S_=ss(y+140,s);bob=2*math.sin(t*1.0+ph+x*.01)
    thuyen(cv,c,x,y+140 if y+140>=880 else y,t,s=s,lon=True,flip=flip,ngoi=ngoi,o=o,ph=ph)
    if day>0: put(cv,c,'t26n_bao',x+(-40 if not flip else 40)*S_,y-30*S_+bob,s=S_*.55*day,ay=1,o=o)
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
TIEN='t26n_r_'
# 1: hook: đoàn thuyền lương giữa biển
def S_1(cv,t):
    a,b=0,E[1]+.3
    c=kc(t,[(a,(900,640,1.3)),(b,(1100,620,1.15))])
    bien(cv,c,t,seed=1,mist=.6)
    for i in range(3): thuyenluong(cv,c,200+i*520+260*inn(t,a,b-a+2),780+(i%2)*30,t,s=.5,ngoi=[(MA[i],-170,None)],ph=i)
    for i in range(3): put(cv,c,'t26_spr_coN',280+i*520+260*inn(t,a,b-a+2),690+(i%2)*30,s=.32,ay=1,r=2*math.sin(t*2+i))
    daotruoc(cv,c,t,sd=1)
    if not FREEZE: ink_wash(cv,.22)
    nhan(cv,'chở lương theo · vẫn phải rút vì thiếu lương',960,170,t,sb(1,0)+2.4,b,RED,40)
# 2: hai lần trước thiếu lương; lần này chở theo đường biển
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3;q=sb(2,1)
    if t<q:
        c=kc(t,[(a,(1100,640,1.15)),(q,(900,640,1.25))])
        nen(cv,c,t,seed=2,mist=.6)
        def met(PP,t_): PP.update(lean=18,arF=-20,faF=-30,arB=10,faB=-20,mat='S')
        for i in range(6):
            x=1350+i*170-420*inn(t,a,q-a+2);P=rig.walk(t*2.2+i,.6);met(P,t)
            ngd(cv,c,MA[i%3],x,905+(i%2)*12,t,.56,P,flip=True)
        truoc(cv,c,t)
        nhan(cv,'hai lần trước · càng đánh sâu càng thiếu lương',960,170,t,a+.4,q,INK,40)
    else:
        c=kc(t,[(q,(800,640,1.1)),(b,(1000,620,1.0))])
        bien(cv,c,t,seed=3)
        for i in range(4): thuyenluong(cv,c,-200+i*420+700*inn(t,q,b-q+3),790+(i%2)*25,t,s=.44,ngoi=[(MA[i%3],-170,None)],ph=i)
        for i in range(4): put(cv,c,'t26_spr_coN',-130+i*420+700*inn(t,q,b-q+3),700+(i%2)*25,s=.28,ay=1,r=2*math.sin(t*2+i))
        daotruoc(cv,c,t,sd=2)
        nhan(cv,'lần thứ ba · lương đi theo bằng đường biển',960,170,t,q+.2,b,MONGC,40)
# 3: đạo quân ngóng thuyền lương
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.4
    c=kc(t,[(a,(700,620,1.1)),(b,(620,660,1.35))])
    bien(cv,c,t,seed=4,mist=.7,bo=True)
    put(cv,c,'t26n_trai',300,860,ay=1,s=.45,k=.85,o=.8)
    for i in range(5):
        P=ngam(rig.dung(t+i));P['mat']='S' if t>b-2 else ''
        ngd(cv,c,MA[i%3],260+i*150,905+(i%2)*10,t,.58,P)
    co(cv,c,'t26_spr_coN',180,870,t,s=.5)
    if not FREEZE: ink_wash(cv,.18+.15*inn(t,b-2.5,2))
# 4: câu hỏi
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.8
    c=kc(t,[(a,(960,600,1.0)),(b,(1000,640,1.2))])
    bien(cv,c,t,seed=5,mist=.8)
    for i in range(5): put(cv,c,'t26n_gao',400+i*260+45*(t-a),860+10*math.sin(t*1.3+i),s=.3,r=25*math.sin(t*.9+i)+i*40,o=.85)
    thuyen(cv,c,1600-60*(t-a),800,t,s=.4,flip=True,ngoi=[('v8',30,'cheo')],o=.6)
    daotruoc(cv,c,t,sd=3)
    if not FREEZE: ink_wash(cv,.3)
    nhan(cv,'ai đã chặn đoàn thuyền lương?',960,260,t,a+.3,b,RED,50)
# 5: bản đồ: quân Nguyên sang lần thứ ba
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3
    vk,ls,kc_,lc=tuple(PTM['vankiep']),tuple(PTM['langson']),tuple(PTM['khamchau']),tuple(PTM['laocai'])
    c=mcam(t,[(a,(560,560,1.25)),(b,(600,560,1.3))])
    bando(cv,c,t,a)
    diem(cv,c,'Vạn Kiếp',vk,t,a+.2,MONGC,dx=-24,dy=-24)
    bac=[(640,300),ls,(560,520),vk];tay=[lc,(250,466),(330,540),(430,600)];bi=[kc_,(860,470),(760,560),tuple(PTM['vandon'])]
    for i,ps in enumerate([bac,tay,bi]):
        duong(cv,c,ps,t,a+.4+i*.4,b-a-1.4,MONGC,6)
        for j in range(3): cotheo(cv,c,'t23n_thuyen' if i==2 else 't26_spr_coN',ps,t,a+.4+i*.4+j*.4,b-a-1.0,s=.14 if i==2 else .2,ph=i+j)
    nhan(cv,'Mông Cổ · người Hán phương nam · Vân Nam · Hải Nam',960,150,t,a+.6,b,MONGC,36)
# 6: bản đồ: chiến thuyền đi trước, thuyền lương theo sau; mọi đường biển qua Vân Đồn
def S_6(cv,t):
    a,b=T[6]-.3,E[7]+.3;q=sb(6,1);r=T[7]
    vk,vd,bd,kc_=tuple(PTM['vankiep']),tuple(PTM['vandon']),tuple(PTM['bachdang']),tuple(PTM['khamchau'])
    c=mcam(t,[(a,(720,540,1.7)),(r,(700,560,1.9)),(b,(660,600,2.3))])
    bando(cv,c,t,a)
    diem(cv,c,'Vạn Kiếp',vk,t,a,MONGC,dx=-24,dy=-24)
    ps=[kc_,(860,470),(780,560),vd,(650,630),bd,(560,610),vk]
    duong(cv,c,ps,t,a+.3,b-a-1.5,MONGC,5)
    for j in range(3): cotheo(cv,c,'t23n_thuyen',ps,t,a+.3+j*.25,(b-a)*.75,s=.11,ph=j)
    if t>q:
        ps2=[(1243,689),(1000,640),(850,610),vd,(650,630),bd,(560,610),vk]
        duong(cv,c,ps2,t,q,b-q-.5,(.55,.45,.3),4)
        for j in range(3): cotheo(cv,c,'t23n_thuyenlon',ps2,t,q+j*.3,(b-q)*1.6,s=.1,ph=j)
        nhan(cv,'thuyền lương của Trương Văn Hổ theo sau',960,150,t,q+.2,r-.1,MONGC,38)
    else: nhan(cv,'thủy quân Ô Mã Nhi đi trước',960,150,t,a+.4,q,MONGC,38)
    if t>r:
        diem(cv,c,'Vân Đồn',vd,t,r,RED,dx=24,dy=-16);diem(cv,c,'sông Bạch Đằng',bd,t,r+.6,INK,dx=24,dy=26);pulse(cv,c,*vd,t)
        nhan(cv,'đường biển nào cũng phải qua Vân Đồn',960,150,t,r+.2,b,RED,40)
# 7: người giữ cửa ngõ
def S_7(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1)
    c=kc(t,[(a,(1150,650,1.15)),(q,(1250,620,1.45)),(b,(1250,600,1.55))])
    bien(cv,c,t,seed=7,mist=.5,bo=True)
    co(cv,c,'t26_spr_coV',1460,880,t,s=.6)
    ngd(cv,c,'tkd',1300,905,t,.74,rig.dung(t),flip=True,vk='dao')
    for i in range(3): ngd(cv,c,VA[i],1550+i*130,905+(i%2)*10,t,.6,rig.dung(t+i),flip=True,vk='giao')
    for i in range(2): thuyen(cv,c,400+i*360+30*math.sin(t*.3+i),800+i*20,t,s=.42,ngoi=[('v8',-40,'cheo')],ph=i)
    daotruoc(cv,c,t,sd=4)
    if t>q and not FREEZE: ink_wash(cv,.3*inn(t,q,1.5))
    nhan(cv,'Nhân Huệ Vương Trần Khánh Dư',1250,250,t,a+.5,q,VIETC,40)
    nhan(cv,'con đường tới Vân Đồn · một chuyện rất lạ',960,170,t,q+.3,b,RED,40)
# 8: đánh úp giặc; thượng hoàng khen, nhận làm con nuôi
def S_8(cv,t):
    a,b=T[9]-.3,E[9]+.3;q=sb(9,1)
    if t<q:
        hit=a+1.8;sh=(5*math.sin(t*37)*(1-inn(t,hit+.3,.6))) if hit<t<hit+.9 and not FREEZE else 0
        c=kc(t,[(a,(800,660,1.3)),(q,(1000,640,1.15))],sh)
        nen(cv,c,t,seed=8,mist=.6)
        chay(cv,c,'tkd',150,1000,905,t,a+.1,q,.7,lambda ph,tt:rig.xung(ph),vk='dao')
        for i in range(3): chay(cv,c,VA[i],-60-i*150,800-i*150,905+(i%2)*10,t,a+.3+i*.1,q,.6,lambda ph,tt:rig.xung(ph),ph=i,vk='giao')
        for i in range(4):
            u=inn(t,hit+i*.12,.4);x0=1250+i*150
            if u<.5: ngd(cv,c,MA[i%3],x0,905+(i%2)*10,t,.6,tronm(rig.dung(t+i),rig.so(t+i,1.2),u*2),flip=True,vk='daocong')
            else: chay(cv,c,MA[i%3],x0,x0+900,905+(i%2)*10,t,hit+.5,q+1,.6,lambda ph,tt:rig.hoang(ph,tt),ph=i)
            if u>.5: roi(cv,c,'t23n_r_w_daocong',x0,905-120,t,hit+.4+i*.12,dx=-80,s=.5)
        truoc(cv,c,t)
        nhan(cv,'nhân lúc giặc sơ hở mà đánh úp',960,170,t,a+.4,q,VIETC,40)
    else:
        c=kc(t,[(q,(960,640,1.15)),(b,(960,620,1.3))])
        nen(cv,c,t,seed=6,mist=.3)
        put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9)
        ngd(cv,c,'tts6',760,905,t,.72,rig.reo(t)|{'arB':10,'faB':-40})
        ngd(cv,c,'tkd',1200,905,t,.68,lay(rig.dung(t),t),flip=True)
        for i in range(3): ngd(cv,c,'lh6',1450+i*130,905,t,.6,rig.dung(t+i),flip=True,vk='giao')
        nhan(cv,'Thượng hoàng Trần Thánh Tông nhận làm con nuôi',960,170,t,q+.2,b,VIETC,38)
# 9: Phiêu Kỵ đại tướng quân; rồi tự đánh mất tất cả
def S_9(cv,t):
    a,b=T[10]-.3,E[10]+.3;q=sb(10,1)
    c=kc(t,[(a,(960,660,1.2)),(q,(980,640,1.4)),(b,(1000,620,1.6))])
    nen(cv,c,t,seed=9,mist=.4)
    for i in range(4): co(cv,c,'t26_spr_coV',500+i*300,880,t,s=.55,ph=i)
    m='S' if t>q+.5 else ''
    ngd(cv,c,'tkd',980,905,t,.8,(rig.quat(t) if t<q else rig.dung(t))|{'mat':m},vk='dao')
    for i in range(3): ngd(cv,c,VA[i],620-i*140,905+(i%2)*10,t,.6,lay(rig.dung(t+i),t+i))
    for i in range(3): ngd(cv,c,VA[i],1320+i*140,905+(i%2)*10,t,.6,lay(rig.dung(t+i),t+i),flip=True)
    truoc(cv,c,t)
    if t>q and not FREEZE: ink_wash(cv,.4*inn(t,q,1.5))
    nhan(cv,'Phiêu Kỵ đại tướng quân',960,170,t,a+.4,q,VIETC,44)
# 10: công chúa Thiên Thụy
def S_10(cv,t):
    a,b=T[11]-.3,E[11]+.3
    c=kc(t,[(a,(900,640,1.1)),(b,(1050,640,1.3))])
    nen(cv,c,t,seed=6,mist=.3)
    put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9)
    def rinh(PP,t_): PP.update(lean=16,arF=-40,faF=-40,arB=-20,faB=-30)
    dib(cv,c,'tkd',300,900,905,t,a,b-1,s=.66,sua=rinh,chay=.5,buoc=30)
    for i in range(2): ngd(cv,c,'lh6',1500+i*160,905,t,.6,rig.dung(t+i),flip=True,vk='giao')
    if not FREEZE: ink_wash(cv,.42)
    truoc(cv,c,t)
    nhan(cv,'công chúa Thiên Thụy · đã được gả cho Hưng Vũ Vương',960,170,t,a+.5,b,INK,38)
# 11: đánh đòn ở Hồ Tây
def S_11(cv,t):
    a,b=T[12]-.3,E[12]+.3;q=sb(12,1) if len(_SC[12])>2 else (a+b)/2
    c=kc(t,[(a,(800,640,1.15)),(q,(1000,660,1.3)),(b,(1100,680,1.45))])
    nen(cv,c,t,'song',seed=11,mist=.5)
    ngd(cv,c,'tnt6',520,905,t,.72,rig.quat(t))
    ngd(cv,c,'tkd',1100,905,t,.64,quy(rig.dung(t))|{'mat':'S','head':8})
    for i in range(2):
        P=rig.dung(t+i);sw=math.sin(t*5+i*2);P.update(arF=-150+60*max(0,sw),faF=-10)
        ngd(cv,c,'lh6',920+i*370,905,t,.64,P,flip=bool(i),vk='gay')
    if t>q and not FREEZE: run(cv,c,1100,700,.8,t)
    truoc(cv,c,t)
    nhan(cv,'Hồ Tây · đánh đòn nhưng dặn đừng đánh đến chết',960,170,t,a+.4,b,RED,38)
# 12: tước hết, về Chí Linh bán than
def S_12(cv,t):
    a,b=T[13]-.3,E[13]+.3;q=sb(13,1)
    if t<q:
        c=kc(t,[(a,(960,640,1.2)),(q,(1100,650,1.3))])
        nen(cv,c,t,seed=12,mist=.7)
        def cui(PP,t_): PP.update(lean=10,head=10,mat='S')
        dib(cv,c,'tkd2',500,1300,905,t,a,q+1,s=.66,sua=cui,chay=.6)
        put(cv,c,'t26n_ao',300,880,s=1.0,ay=1,o=.7,r=-8)
        if not FREEZE: ink_wash(cv,.35)
        nhan(cv,'tước hết quan tước và tài sản',960,170,t,a+.3,q,RED,42)
    else:
        c=kc(t,[(q,(900,640,1.1)),(b,(1100,640,1.2))])
        nen(cv,c,t,seed=13,mist=.5)
        def ganh(PP,t_): PP.update(lean=14,arF=-160,faF=0,arB=-150,faB=0)
        x=dib(cv,c,'tkd2',300,1300,905,t,q,b+2,s=.66,sua=ganh,chay=.6,buoc=40)
        put(cv,c,'t26n_than',x,905-250*.66*1.45,s=.25,ay=1,r=2*math.sin(t*3))
        for i in range(2): ngd(cv,c,'d6c',1500+i*170,905,t,.6,rig.dung(t+i),flip=True)
        truoc(cv,c,t)
        nhan(cv,'về Chí Linh · sống bằng nghề bán than',960,170,t,q+.2,b,INK,42)
# 13: bến Bình Than
def S_13(cv,t):
    a,b=T[14]-.3,E[14]+.3;q=sb(14,1)
    c=kc(t,[(a,(700,640,1.1)),(q,(1000,660,1.2)),(b,(1100,690,1.35))])
    nen(cv,c,t,'song',seed=14,mist=.5)
    thuyen(cv,c,520,800,t,s=.6,lon=True,ngoi=[('tnt6',-260,None),('lh6',-160,None),('lh6',140,'cheo')])
    if t>q-1:
        x=1900-700*inn(t,q-1,b-q+2)
        thuyen(cv,c,x,830,t,s=.52,flip=True,ngoi=[('tkd2',40,'cheo')],ph=2)
        put(cv,c,Af('t26n_than'),x-110,812,s=.15,ay=1)
    truoc(cv,c,t)
    nhan(cv,'năm 1282 · bến Bình Than',960,170,t,a+.3,q,INK,44)
    nhan(cv,'người lái đội nón lá, mặc áo ngắn',960,170,t,q+.3,b,INK,40)
# 14: vua nhận ra, sai thuyền nhỏ đuổi theo
def S_14(cv,t):
    a,b=T[15]-.3,E[15]+.3;q=sb(15,1)
    if t<q:
        c=kc(t,[(a,(760,600,1.45)),(q,(720,600,1.6))])
        nen(cv,c,t,'song',seed=15,mist=.4)
        thuyen(cv,c,1250,800,t,s=.6,lon=True,ngoi=[])
        ngd(cv,c,'tnt6',700,905,t,.76,rig.quat(t)|{'mat':''})
        for i in range(2): ngd(cv,c,'lh6',420-i*150,905,t,.62,rig.dung(t+i),vk='giao')
        truoc(cv,c,t)
        nhan(cv,'người kia chẳng phải Nhân Huệ Vương?',960,170,t,a+.4,q,RED,40)
    else:
        c=kc(t,[(q,(900,640,1.1)),(b,(1200,650,1.15))])
        nen(cv,c,t,'song',seed=16,mist=.5)
        x=1800-200*inn(t,q,b-q+2);thuyen(cv,c,x,830,t,s=.5,flip=True,ngoi=[('tkd2',40,'cheo')],ph=2)
        put(cv,c,Af('t26n_than'),x-110,812,s=.15,ay=1)
        thuyen(cv,c,200+900*inn(t,q,b-q+1),860,t,s=.46,ngoi=[('lh6',-40,'cheo'),('lh6',50,'cheo')],ph=1)
        truoc(cv,c,t)
        nhan(cv,'một chiếc thuyền nhỏ được sai đuổi theo',960,170,t,q+.2,b,INK,40)
# 15: lính gọi; Khánh Dư đáp
def S_15(cv,t):
    a,b=T[16]-.3,E[16]+.3;q=sb(16,1)
    if t<q:
        c=kc(t,[(a,(760,620,1.5)),(q,(800,620,1.6))])
        nen(cv,c,t,'song',seed=17,mist=.4)
        thuyen(cv,c,700,830,t,s=.6,ngoi=[('lh6',-40,None),('lh6',60,'cheo')],ph=1)
        if not FREEZE: vong(cv,*c.p(640,640),t,a+.2,n=3,per=1.2,rmax=300,o=.4,col=INK)
    else:
        c=kc(t,[(q,(1200,620,1.6)),(b,(1230,610,1.75))])
        nen(cv,c,t,'song',seed=18,mist=.4)
        thuyen(cv,c,1250,830,t,s=.6,flip=True,ngoi=[('tkd2',40,None)],ph=2)
        put(cv,c,Af('t26n_than'),1140,812,s=.17,ay=1)
        if not FREEZE: soi(cv,c,1230,610,t,.7)
        nhan(cv,'lão là người buôn bán',960,170,t,q+.3,b,INK,42)
# 16: vua nhận ra cách trả lời; sai người hầu gọi lần nữa
def S_16(cv,t):
    a,b=T[17]-.3,E[17]+.3;q=sb(17,1)
    c=kc(t,[(a,(700,600,1.45)),(q,(900,640,1.15)),(b,(1100,650,1.1))])
    nen(cv,c,t,'song',seed=19,mist=.4)
    thuyen(cv,c,600,800,t,s=.64,lon=True,ngoi=[('tnt6',-140,None)])
    if t<q: nhan(cv,'đúng là Nhân Huệ rồi',960,170,t,a+.4,q,VIETC,44)
    else:
        thuyen(cv,c,900+600*inn(t,q,b-q),860,t,s=.46,ngoi=[('lh6',-40,'cheo'),('lh6',50,'cheo')],ph=1)
        nhan(cv,'người thường chẳng ai dám trả lời như thế',960,170,t,q+.1,b,INK,38)
    truoc(cv,c,t)
# 17: gặp vua, tha tội
def S_17(cv,t):
    a,b=T[18]-.3,E[18]+.3;q=sb(18,1)
    c=kc(t,[(a,(960,640,1.15)),(q,(900,620,1.4)),(b,(860,620,1.5))])
    nen(cv,c,t,'song',seed=20,mist=.4)
    ngd(cv,c,'tnt6',700,905,t,.74,(rig.dung(t)|{'arF':-60,'faF':-30}) if t<q else rig.quat(t)|{'mat':''})
    for i in range(2): ngd(cv,c,'lh6',420-i*150,905,t,.62,rig.dung(t+i),vk='giao')
    ngd(cv,c,'tkd2',1080,905,t,.7,lay(rig.dung(t),t) if t<q+2 else quy(rig.dung(t)),flip=True)
    truoc(cv,c,t)
    nhan(cv,'vẫn áo ngắn, nón lá',960,170,t,a+.4,q,INK,42);nhan(cv,'nam nhi mà đến nỗi này · tha tội',960,170,t,q+.3,b,VIETC,40)
# 18: ban áo, bàn việc nước, Phó đô tướng quân
def S_18(cv,t):
    a,b=T[19]-.3,E[19]+.3;q=a+(b-a)*.45
    c=kc(t,[(a,(960,640,1.15)),(b,(960,620,1.05))])
    nen(cv,c,t,seed=6,mist=.3)
    put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9)
    ngd(cv,c,'tnt6',560,905,t,.72,rig.dung(t)|{'arF':-70,'faF':-30})
    if t<q:
        u=inn(t,a+.4,1.4);put(cv,c,'t26n_ao',700+400*u,720+60*math.sin(u*math.pi)*-1,s=.9,r=-10+10*u)
        ngd(cv,c,'tkd2',1150,905,t,.7,lay(rig.dung(t),t),flip=True)
    else:
        ngd(cv,c,'tkd',1150,905,t,.72,rig.dung(t)|{'mat':'V'},flip=True,vk='dao')
        for i,k in enumerate(['hdv6','ts6']): ngd(cv,c,k,1400+i*170,905,t,.66,rig.dung(t+i),flip=True)
        truoc(cv,c,t)
    nhan(cv,'Phó đô tướng quân',960,170,t,q+.3,b,VIETC,44)
# 19: Vân Đồn, cảng buôn; dân theo kiểu khách phương Bắc
def S_19(cv,t):
    a,b=T[20]-.3,E[21]+.3;q=T[21]
    c=kc(t,[(a,(800,680,1.3)),(q,(1000,700,1.4)),(b,(1150,700,1.45))])
    bien(cv,c,t,seed=21,mist=.4,y=520)
    put(cv,c,'t26n_cang',960,930,ay=1,s=1.9,k=.9)
    for i in range(5): dib(cv,c,['d6a','d6b','d6a','d6b','d6c'][i],200+i*300,500+i*300+150*(1 if i%2 else -1),905+(i%2)*12,t,a+i*.3,b,s=.56,ph=i,chay=.6)
    for i in range(2): put(cv,c,'t26n_bao',600+i*700,905,s=.12,ay=1)
    nhan(cv,'Vân Đồn · cảng buôn giữa các đảo',960,170,t,a+.4,q,INK,42);nhan(cv,'ăn mặc giống khách buôn phương Bắc',960,170,t,q+.2,b,INK,40)
# 20: lệnh đội nón Ma Lôi
def S_20(cv,t):
    a,b=T[22]-.3,E[22]+.3
    c=kc(t,[(a,(900,640,1.3)),(b,(1100,640,1.15))])
    nen(cv,c,t,seed=22,mist=.4)
    ngd(cv,c,'tkd',520,905,t,.74,rig.quat(t),vk='dao')
    for i in range(6):
        u=inn(t,a+1+i*.3,.6);k=['v6','v7'][i%2] if u>.5 else 'v8'
        ngd(cv,c,k,820+i*170,905+(i%2)*12,t,.6,rig.dung(t+i),flip=True,vk='giao')
    co(cv,c,'t26_spr_coV',380,880,t,s=.55)
    truoc(cv,c,t)
    nhan(cv,'nón Ma Lôi · để khỏi lẫn với quân Nguyên',960,170,t,a+.6,b,VIETC,40)
# 21: thuyền nón của người nhà
def S_21(cv,t):
    a,b=T[23]-.3,E[23]+.3;q=sb(23,1)
    c=kc(t,[(a,(960,680,1.3)),(q,(800,690,1.4)),(b,(760,700,1.55))])
    bien(cv,c,t,seed=23,mist=.6,y=520)
    put(cv,c,'t26n_cang',960,930,ay=1,s=1.9,k=.9)
    x=200+500*inn(t,a,q-a+1)
    thuyen(cv,c,x,830,t,s=.6,lon=True,ngoi=[('d6c',-200,'cheo')])
    put(cv,c,'t26n_non',x+40,830-140-30,s=.4,ay=1)
    if t>q:
        ngd(cv,c,'d6a',x+380,905,t,.6,lay(rig.dung(t),t),flip=True)
        if not FREEZE: ink_wash(cv,.3*inn(t,q,1))
    nhan(cv,'lý do nghe rất hợp lẽ',960,170,t,a+.3,q,INK,42);nhan(cv,'một thuyền nón Ma Lôi của người nhà',960,170,t,q+.2,b,RED,40)
# 22: dân tranh mua; giá lên một tấm vải
def S_22(cv,t):
    a,b=T[24]-.3,E[24]+.3;q=sb(24,1)
    c=kc(t,[(a,(960,640,1.1)),(q,(960,620,1.3)),(b,(960,600,1.4))])
    nen(cv,c,t,seed=24,mist=.4)
    put(cv,c,'t26n_non',960,905,s=.5,ay=1)
    for i in range(7):
        x=420+i*170+(0 if i<3 else 120);fl=i>=4
        P=rig.dung(t+i);P.update(arF=-110+20*math.sin(t*6+i),faF=-20,lean=12)
        ngd(cv,c,['d6a','d6b','d6c'][i%3],x+20*math.sin(t*2+i),905+(i%2)*10,t,.56,P,flip=fl)
    if t>q and not FREEZE:
        u=inn(t,q+.3,.8);put(cv,c,'t26n_vai',1380,620,s=.4*u,o=u)
        put_screen(cv,text('lúc đầu chưa tới 1 tiền',46,INK,700),560,330,1-inn(t,q+.8,.5))
        put_screen(cv,text('sau lên tới 1 tấm vải',52,RED,700),1350,330,inn(t,q+.8,.5))
    truoc(cv,c,t)
    nhan(cv,'dân tranh nhau đi mua nón',960,170,t,a+.3,q,INK,42)
# 23: sử chê tham; vua tiếc tài
def S_23(cv,t):
    a,b=T[25]-.3,E[25]+.3;q=sb(25,1)
    c=kc(t,[(a,(960,620,1.05)),(b,(960,600,1.12))])
    nen(cv,c,t,seed=25,mist=.6)
    if t<q:
        ngd(cv,c,'tkd',1450,905,t,.66,rig.dung(t),flip=True)
        cuon(cv,760,470,t,'SỬ CŨ CHÉP','tham lam|nơi ông trấn giữ|người ta cũng ghét',col=RED,s=.8,sz=38,u=inn(t,a+.5,2.2),nm='t26n_cuon2')
    else:
        ngd(cv,c,'tnt6',760,905,t,.72,rig.dung(t)|{'head':10,'arF':-40,'faF':-60})
        ngd(cv,c,'tkd',1200,905,t,.7,rig.dung(t),flip=True,vk='dao')
        nhan(cv,'vua Trần Nhân Tông tiếc ông có tài làm tướng',960,170,t,q+.2,b,VIETC,38)
    truoc(cv,c,t)
# 24: Hưng Đạo Vương giao việc giữ vùng biển
def S_24(cv,t):
    a,b=T[26]-.3,E[26]+.3
    c=kc(t,[(a,(960,660,1.2)),(b,(980,640,1.35))])
    bien(cv,c,t,seed=26,mist=.5,bo=True)
    ngd(cv,c,'hdv6',760,905,t,.74,rig.dung(t)|{'arF':-80,'faF':-10})
    ngd(cv,c,'tkd',1160,905,t,.72,lay(rig.dung(t),t),flip=True,vk='dao')
    for i in range(4): ngd(cv,c,VA[i%2],1400+i*130,905+(i%2)*10,t,.58,rig.dung(t+i),flip=True,vk='giao')
    co(cv,c,'t26_spr_coV',560,880,t,s=.55)
    daotruoc(cv,c,t,sd=5)
    nhan(cv,'Hưng Đạo Vương giao việc giữ vùng biển đông bắc',960,170,t,a+.4,b,VIETC,38)
# 25: bản đồ: Ô Mã Nhi tới cửa An Bang
def S_25(cv,t):
    a,b=T[27]-.3,E[27]+.3
    vd,kc_=tuple(PTM['vandon']),tuple(PTM['khamchau']);ab=(675,628)
    c=mcam(t,[(a,(760,520,2.0)),(b,(720,580,2.4))])
    bando(cv,c,t,a)
    diem(cv,c,'Vân Đồn',vd,t,a,RED,dx=24,dy=-16)
    ps=[kc_,(880,470),(800,540),(740,590),ab]
    duong(cv,c,ps,t,a+.3,b-a-1,MONGC,5)
    for j in range(4): cotheo(cv,c,'t23n_thuyen',ps,t,a+.3+j*.25,b-a-.6,s=.1,ph=j)
    if t>b-2.2: diem(cv,c,'cửa An Bang',ab,t,b-2.2,MONGC,dx=-24,dy=24);pulse(cv,c,*ab,t)
    nhan(cv,'tháng mười một · thủy quân Ô Mã Nhi kéo vào',960,150,t,a+.3,b,MONGC,38)
# 26: trận đầu ở Vân Đồn: Đại Việt thua
def S_26(cv,t):
    a,b=T[28]-.3,E[28]+.3;q=sb(28,1)
    c=kc(t,[(a,(900,640,1.1)),(q,(1000,650,1.2)),(b,(1100,660,1.3))])
    bien(cv,c,t,seed=28,mist=.4)
    for i in range(3):
        x=1500+i*200-300*inn(t,a,b-a)
        thuyen(cv,c,x,780+(i%2)*30,t,s=.5,lon=True,flip=True,ngoi=[(('omn6' if i==1 else MA[i]),60,None),(MA[(i+1)%3],-120,'daocong')],ph=i)
        put(cv,c,Af('t26_spr_coN'),x+120,690+(i%2)*30,s=.3,ay=1,r=2*math.sin(t*2+i))
    for i in range(4):
        u=inn(t,q+i*.35,1.2);x=300+i*190-120*u
        thuyen(cv,c,x,830+(i%2)*20+30*u,t,s=.42,ngoi=[('v8',-30,'cheo' if u<.3 else None)],ph=i,o=1-.5*u)
    if not FREEZE:
        ten(cv,c,t,a+.6,b,[(1300,700),(1500,720),(1700,690)],[(300,820),(500,840),(700,830)],n=10,h=140)
        for i in range(3):
            if t>q+i*.5: smoke(cv,c,260+i*240,800,t,.6)
    daotruoc(cv,c,t,sd=6)
    nhan(cv,'sử nhà Nguyên · hơn 400 thuyền Đại Việt vẫn thua',960,170,t,q+.1,b,MONGC,38)
# 27: bản đồ: đoàn chiến thuyền vượt qua, lên Vạn Kiếp
def S_27(cv,t):
    a,b=T[29]-.3,E[29]+.3
    vk,vd,bd=tuple(PTM['vankiep']),tuple(PTM['vandon']),tuple(PTM['bachdang']);ab=(675,628)
    c=mcam(t,[(a,(660,600,2.4)),(b,(600,600,2.6))])
    bando(cv,c,t,a)
    diem(cv,c,'Vân Đồn',vd,t,a,RED,dx=24,dy=-16);diem(cv,c,'Vạn Kiếp',vk,t,a+.3,MONGC,dx=-24,dy=-20)
    ps=[ab,bd,(560,610),vk]
    duong(cv,c,ps,t,a+.3,b-a-1,MONGC,4)
    for j in range(5): cotheo(cv,c,'t23n_thuyen',ps,t,a+.3+j*.3,b-a-.4,s=.13,ph=j)
    pulse(cv,c,*vd,t)
    put(cv,c,band(40,6,RED,.8,1),vd[0],vd[1]+14,r=40);put(cv,c,band(40,6,RED,.8,1),vd[0],vd[1]+14,r=-40)
    nhan(cv,'Trần Khánh Dư không chặn nổi',960,150,t,a+.3,b,RED,40)
# 28: Vạn Kiếp, chờ thuyền lương
def S_28(cv,t):
    a,b=T[30]-.3,E[30]+.3
    c=kc(t,[(a,(960,640,1.15)),(b,(800,640,1.3))])
    nen(cv,c,t,'song',seed=30,mist=.5)
    put(cv,c,'t26n_trai',960,860,ay=1,s=.5,k=.85,o=.85)
    ngd(cv,c,'thn6',700,905,t,.74,ngam(rig.dung(t)))
    ngd(cv,c,'omn6',880,905,t,.7,rig.dung(t+1))
    for i in range(5): ngd(cv,c,MA[i%3],1100+i*150,905+(i%2)*10,t,.58,rig.dung(t+i),vk=['daocong','moc'][i%2])
    for i in range(3): co(cv,c,'t26_spr_coN',500+i*600,880,t,s=.5,ph=i)
    truoc(cv,c,t)
    nhan(cv,'Thoát Hoan · Ô Mã Nhi · Vạn Kiếp · chờ thuyền lương',960,170,t,a+.4,b,MONGC,36)
# 29: sứ giả đem xiềng tới bắt
def S_29(cv,t):
    a,b=T[31]-.3,E[31]+.3;q=sb(31,1)
    c=kc(t,[(a,(900,640,1.1)),(q,(1000,650,1.2)),(b,(1100,660,1.4))])
    bien(cv,c,t,seed=31,mist=.5,bo=True)
    x=dib(cv,c,'ts6',-100,700,905,t,a,q+1.5,s=.66)
    for i in range(2):
        xl=dib(cv,c,'lh6',-300-i*150,520-i*150,905,t,a,q+1.5,s=.6,ph=i,sua=lambda PP,t_:PP.update(arF=-70,faF=-20))
        if i==0 and t>q-1: put(cv,c,'t26n_xieng',xl+95,905-118,s=.26,r=8*math.sin(t*3))
    ngd(cv,c,'tkd',1250,905,t,.7,rig.dung(t)|{'head':8},flip=True)
    for i in range(3): ngd(cv,c,VA[i],1480+i*120,905,t,.56,rig.dung(t+i)|{'mat':'S'},flip=True)
    daotruoc(cv,c,t,sd=7)
    nhan(cv,'tin thua trận về tới triều',960,170,t,a+.3,q,INK,42);nhan(cv,'đem xiềng tới bắt giải về kinh',960,170,t,q+.2,b,RED,40)
# 30: xin khất hai ba ngày
def S_30(cv,t):
    a,b=T[32]-.3,E[33]+.3;q=T[33]
    c=kc(t,[(a,(1100,620,1.5)),(q,(1050,620,1.6)),(b,(960,640,1.3))])
    bien(cv,c,t,seed=32,mist=.5,bo=True)
    ngd(cv,c,'ts6',760,905,t,.7,rig.dung(t)|({'head':6} if t>b-1.5 else {}))
    ngd(cv,c,'lh6',500,905,t,.64,rig.dung(t)|{'arF':-70,'faF':-20});put(cv,c,'t26n_xieng',590,905-125,s=.28,r=4*math.sin(t*2))
    ngd(cv,c,'tkd',1150,905,t,.72,(quy(rig.dung(t)) if t<q else rig.dung(t)|{'arF':-90,'faF':-20,'mat':'G'}),flip=True)
    daotruoc(cv,c,t,sd=8)
    nhan(cv,'thua trận thì chịu tội · không dám trốn chết',960,170,t,a+.4,q,INK,40)
    nhan(cv,'xin khất hai ba ngày để lập công',960,170,t,q+.2,b,RED,42)
# 31: vì sao xin chờ? đoàn thuyền chở lương tất theo sau
def S_31(cv,t):
    a,b=T[34]-.3,E[34]+.3;q=sb(34,1)
    c=kc(t,[(a,(1200,600,1.5)),(q,(1100,620,1.4)),(b,(800,640,1.15))])
    bien(cv,c,t,seed=34,mist=.6,bo=True)
    ngd(cv,c,'tkd',1300,905,t,.74,ngam(rig.dung(t)),flip=True)
    if t>q:
        for i in range(3): thuyenluong(cv,c,200+i*300+80*inn(t,q,b-q),770,t,s=.34,o=.55*inn(t,q,1),ph=i)
    daotruoc(cv,c,t,sd=9)
    if t<q and not FREEZE: ink_wash(cv,.25)
    nhan(cv,'vì sao ông xin chờ thêm?',960,250,t,a+.2,q,RED,48)
    nhan(cv,'chiến thuyền đã qua · thuyền lương tất theo sau',960,170,t,q+.2,b,INK,40)
# 32: gom tàn quân, nằm chờ
def S_32(cv,t):
    a,b=T[35]-.3,E[35]+.3
    c=kc(t,[(a,(900,640,1.1)),(b,(1050,660,1.25))])
    bien(cv,c,t,seed=35,mist=.6,bo=True)
    ngd(cv,c,'tkd',1300,905,t,.72,rig.quat(t)|{'mat':'G','arF':-60},flip=True,vk='dao')
    def que(PP,t_): PP.update(lean=14,head=8,arB=20,faB=-60)
    for i in range(5): dib(cv,c,VA[i%3],-100-i*170,600+i*110,905+(i%2)*12,t,a+i*.3,b-1,s=.58,ph=i,sua=que,chay=.5,buoc=36)
    for i in range(3): thuyen(cv,c,1550+i*120,820+i*18,t,s=.36,ngoi=[('v8',0,None)],ph=i,o=.85)
    daotruoc(cv,c,t,sd=10)
    if not FREEZE: ink_wash(cv,.18)
    nhan(cv,'gom lính còn sót lại · nằm chờ ở vùng biển Vân Đồn',960,170,t,a+.4,b,VIETC,38)
# 33: sơ đồ: chiến thuyền đã lên Vạn Kiếp, thuyền lương nặng và chậm
def S_33(cv,t):
    a,b=T[36]-.3,E[36]+.3
    vk,vd=tuple(PTM['vankiep']),tuple(PTM['vandon'])
    c=mcam(t,[(a,(700,600,2.0)),(b,(720,600,2.1))])
    bando(cv,c,t,a)
    diem(cv,c,'Vạn Kiếp',vk,t,a,MONGC,dx=-24,dy=-20);diem(cv,c,'Vân Đồn',vd,t,a+.2,RED,dx=24,dy=-16)
    for i in range(4): put(cv,c,'t23n_thuyen',vk[0]-30+i*18,vk[1]+16+2*math.sin(t*3+i),s=.09)
    ps=[(1000,640),(900,625),(820,612)];x,y=theo(ps,inn(t,a+.3,b-a+6))
    for i in range(3): put(cv,c,'t23n_thuyenlon',x+i*34,y+(i%2)*14+2*math.sin(t*2+i),s=.1)
    for i in range(2): put(cv,c,'t26_spr_coV',vd[0]+10+i*12,vd[1]+6+2*math.sin(t*3+i),s=.06,ay=1)
    pulse(cv,c,*vd,t)
    nhan(cv,'chiến thuyền đã lên Vạn Kiếp',960,150,t,a+.3,(a+b)/2,MONGC,40);nhan(cv,'thuyền lương chở đầy gạo · nặng và chậm',960,150,t,(a+b)/2,b,INK,40)
# 34: Đồn Sơn: ba mươi thuyền Đại Việt lao ra
def S_34(cv,t):
    a,b=T[37]-.3,E[37]+.3;q=sb(37,1)
    c=kc(t,[(a,(1200,640,1.2)),(q,(1000,650,1.1)),(b,(900,660,1.15))])
    bien(cv,c,t,seed=37,mist=.5)
    for i in range(3): thuyenluong(cv,c,1450+i*300-500*inn(t,a,b-a+2),770+(i%2)*30,t,s=.48,flip=True,ngoi=[(('tvh' if i==0 else MA[i]),150,None)],ph=i)
    if t>q:
        for i in range(5):
            x=-200-i*120+900*inn(t,q+i*.12,b-q+.5)
            thuyen(cv,c,x,840+(i%2)*25,t,s=.4,ngoi=[('v8',-40,'cheo'),(VA[i%2],40,'giao')],ph=i)
    daotruoc(cv,c,t,sd=11)
    nhan(cv,'tháng chạp · đoàn thuyền lương tới Đồn Sơn',960,170,t,a+.3,q,MONGC,40)
    nhan(cv,'sử nhà Nguyên · ba mươi thuyền Đại Việt lao ra',960,170,t,q+.2,b,VIETC,38)
# 35: giằng co
def S_35(cv,t):
    a,b=T[38]-.3,E[38]+.3;q=sb(38,1)
    hit=a+1.0;sh=(4*math.sin(t*37)) if hit<t<hit+.6 and not FREEZE else 0
    c=kc(t,[(a,(960,640,1.2)),(b,(960,620,1.3))],sh)
    bien(cv,c,t,seed=38,mist=.4)
    for i in range(2): thuyenluong(cv,c,1250+i*330,770+i*30,t,s=.5,flip=True,ngoi=[(MA[i],170,'daocong'),(MA[i+1],-170,'quat')],ph=i)
    for i in range(3): thuyen(cv,c,380+i*230,840+(i%2)*25,t,s=.42,ngoi=[('v8',-40,None),(VA[i%2],40,'giao')],ph=i)
    if not FREEZE:
        ten(cv,c,t,a+.3,b,[(1200,700),(1500,730)],[(380,830),(600,850),(820,830)],n=6,h=120)
        ten(cv,c,t,a+.6,b,[(400,820),(620,840),(850,820)],[(1250,720),(1550,740)],n=6,h=120,col=VIETC,seed=5)
    nhan(cv,'Trương Văn Hổ cho quân đánh trả',960,170,t,a+.3,q,MONGC,40);nhan(cv,'hai bên giằng co',960,170,t,q+.2,b,INK,44)
# 36: biển Lục Thủy: thuyền Đại Việt mỗi lúc một đông
def S_36(cv,t):
    a,b=T[39]-.3,E[39]+.3;q=sb(39,1)
    c=kc(t,[(a,(1000,640,1.15)),(b,(960,620,1.0))])
    bien(cv,c,t,seed=39,mist=.4)
    for i in range(3):
        P=[(MA[i],150,'so' if t>q+1 else None)];thuyenluong(cv,c,1000+i*300,770+(i%2)*25,t,s=.46,flip=True,ngoi=P,ph=i)
    n=int(2+8*inn(t,q,b-q)) if not FREEZE else 6
    for i in range(n):
        side=i%2;x=(-100-i*60+500*inn(t,q+i*.2,2)) if side==0 else (2050+i*60-450*inn(t,q+i*.2,2))
        thuyen(cv,c,x,840+(i%3)*18,t,s=.36,flip=bool(side),ngoi=[('v8',-30,'cheo')],ph=i)
    daotruoc(cv,c,t,sd=12)
    nhan(cv,'biển Lục Thủy',960,170,t,a+.3,q,INK,44);nhan(cv,'thuyền Đại Việt kéo tới mỗi lúc một đông',960,170,t,q+.2,b,VIETC,38)
# 37: Trương Văn Hổ đổ gạo xuống biển, chạy về Hải Nam
def S_37(cv,t):
    a,b=T[40]-.3,E[41]+.3;q=T[41]
    if t<q:
        c=kc(t,[(a,(1100,600,1.7)),(q,(1100,610,1.85))])
        bien(cv,c,t,seed=40,mist=.4)
        thuyenluong(cv,c,1150,780,t,s=.6,flip=True,ngoi=[('tvh',170,'so'),('m8',100,'so')],ph=1)
        for i in range(3): thuyen(cv,c,300+i*250+60*math.sin(t*.5+i),850+(i%2)*20,t,s=.36,ngoi=[('v8',-30,'cheo')],ph=i)
        nhan(cv,'không đánh nổi · thuyền quá nặng',960,170,t,a+.3,q,MONGC,40)
    else:
        c=kc(t,[(q,(1000,640,1.2)),(b,(1100,630,1.1))])
        bien(cv,c,t,seed=41,mist=.4)
        for i in range(3):
            x=900+i*330+700*inn(t,q+2.5,b-q)
            thuyenluong(cv,c,x,770+(i%2)*25,t,s=.5,ngoi=[(('tvh' if i==0 else MA[i]),-170,'quat' if i==0 else 'so')],ph=i,day=1-.7*inn(t,q+.5+i*.3,2.2))
            for j in range(3): gao_roi(cv,c,x-60,640,t,q+.4+i*.3+j*.55,dx=-140-j*30,s=.3,yday=880)
        nhan(cv,'đổ gạo xuống biển · chạy về đảo Hải Nam',960,170,t,q+.3,b,RED,40)
# 38: hai bộ sử
def S_38(cv,t):
    a,b=T[42]-.3,E[43]+.3;q=T[43]
    c=kc(t,[(a,(960,620,1.05)),(b,(960,600,1.12))])
    bien(cv,c,t,seed=42,mist=.6)
    for i in range(3): thuyenluong(cv,c,-200+i*700+120*(t-a),760,t,s=.3,o=.5,ph=i)
    cuon(cv,560,460,t,'SỬ NHÀ NGUYÊN','đổ gạo|xuống biển',col=MONGC,s=.66,sz=40,u=inn(t,a+.4,1.6),nm='t26n_cuon2')
    cuon(cv,1360,460,t,'TOÀN THƯ','bắt được|lương thực|khí giới',col=RED,s=.66,sz=40,u=inn(t,sb(42,1)+.2,1.6))
    if t>q and not FREEZE:
        u=inn(t,sb(43,1),.6);put_screen(cv,band(1300,90,PAPER,.9*u,18),960,960);put_screen(cv,text('lương không tới được Vạn Kiếp',48,RED,700),960,960,u)
# 39: bản đồ: các đoàn thuyền lương khác gặp nạn
def S_39(cv,t):
    a,b=T[44]-.3,E[44]+.3;q=sb(44,1)
    hn=(1230,820);cp=(860,930);lz=tuple(PTM['leizhou'])
    c=mcam(t,[(a,(1000,700,1.2)),(b,(950,760,1.15))])
    bando(cv,c,t,a)
    diem(cv,c,'đảo Hải Nam',hn,t,a+.3,INK,dx=24,dy=20);diem(cv,c,'về phía Chăm Pa',cp,t,q,INK,dx=24,dy=-20)
    p1=[(1400,500),(1330,640),(1260,760),hn];p2=[(1300,560),(1100,700),(900,880),cp]
    for i,ps in enumerate([p1,p2]):
        st=a+.4 if i==0 else q
        duong(cv,c,ps,t,st,b-st-.6,(.45,.4,.35),4)
        for j in range(3): cotheo(cv,c,'t23n_thuyenlon',ps,t,st+j*.4,b-st-.3+j*.4,s=.1,ph=i+j)
    if not FREEZE:
        for k in range(5):
            x=1150+((t*90+k*170)%500);put(cv,c,band(90,4,INK,.4,1),x,520+k*60,r=-25)
    nhan(cv,'gặp gió trôi dạt · sang Hải Nam · tới Chăm Pa',960,150,t,a+.4,b,INK,38)
# 40: tù binh; ngựa chạy về triều báo tin
def S_40(cv,t):
    a,b=T[45]-.3,E[45]+.3;q=sb(45,1)
    if t<q:
        c=kc(t,[(a,(960,640,1.15)),(q,(1000,640,1.25))])
        bien(cv,c,t,seed=45,mist=.5,bo=True)
        for i in range(5):
            P=rig.walk(t*2+i,.5);P.update(lean=12,head=10,arF=10,faF=-80,arB=0,faB=-80,mat='S')
            ngd(cv,c,MA[i%3],600+i*150+60*inn(t,a,q-a),905+(i%2)*10,t,.56,P)
        for i in range(2): ngd(cv,c,VA[i],380-i*140,905,t,.6,rig.dung(t+i)|{'mat':'V'},vk='giao')
        ngd(cv,c,'tkd',1500,905,t,.7,rig.reo(t),flip=True,vk='dao')
        daotruoc(cv,c,t,sd=13)
        nhan(cv,'bắt được rất nhiều tù binh',960,170,t,a+.3,q,VIETC,42)
    else:
        c=kc(t,[(q,(900,640,1.1)),(b,(1100,640,1.05))])
        nen(cv,c,t,seed=46,mist=.5)
        ngua(cv,c,'nau','lh6',-200,2000,905,t,q,b+.5,s=.62)
        if not FREEZE: bui(cv,c,-300+2200*inn(t,q,b-q+.5),905,t,q+.2,n=3)
        truoc(cv,c,t)
        nhan(cv,'ngay hôm ấy · ngựa chạy về triều báo tin',960,170,t,q+.2,b,INK,40)
# 41: thượng hoàng bỏ qua tội
def S_41(cv,t):
    a,b=T[46]-.3,E[46]+.3;q=sb(46,1)
    c=kc(t,[(a,(960,640,1.15)),(b,(960,630,1.3))])
    nen(cv,c,t,seed=6,mist=.3)
    put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9)
    ngd(cv,c,'tts6',720,905,t,(.72),rig.reo(t) if t<q else rig.dung(t)|{'arF':-70,'faF':-20,'mat':'V'})
    ngd(cv,c,'tkd',1180,905,t,.7,quy(rig.dung(t)) if t>q else lay(rig.dung(t),t),flip=True)
    roi(cv,c,'t26n_xieng',1180,780,t,q+.3,dx=120,s=.3)
    for i in range(3): ngd(cv,c,'lh6',1450+i*130,905,t,.6,rig.dung(t+i)|{'mat':'V'},flip=True,vk='giao')
    truoc(cv,c,t)
    nhan(cv,'tin thắng trận về tới triều',960,170,t,a+.3,q,VIETC,42);nhan(cv,'tội thua trận · không xét đến nữa',960,170,t,q+.2,b,VIETC,40)
# 42: lời thượng hoàng
def S_42(cv,t):
    a,b=T[47]-.3,E[47]+.3
    c=kc(t,[(a,(800,600,1.5)),(b,(820,600,1.65))])
    nen(cv,c,t,seed=6,mist=.3)
    put(cv,c,'t26n_dien',960,940,ay=1,s=1.24,k=.9)
    ngd(cv,c,'tts6',780,905,t,.76,rig.quat(t)|{'mat':''})
    for i in range(3): put(cv,c,'t26n_gao',1100+i*90,905,s=.3,ay=1)
    ngd(cv,c,'tkd',1450,905,t,.7,lay(rig.dung(t),t),flip=True)
    truoc(cv,c,t)
    nhan(cv,'quân Nguyên trông cậy cả vào lương thực, khí giới',960,170,t,a+.4,b,RED,38)
# 43: thả tù binh về báo tin
def S_43(cv,t):
    a,b=T[48]-.3,E[48]+.3
    c=kc(t,[(a,(800,640,1.1)),(b,(1100,640,1.15))])
    nen(cv,c,t,seed=48,mist=.6)
    put(cv,c,'t26n_trai',1700,860,ay=1,s=.4,k=.85,o=.8)
    for i in range(5): chay(cv,c,MA[i%3],300+i*130,1300+i*130,905+(i%2)*10,t,a+.5+i*.2,b+2,.55,lambda ph,tt:rig.hoang(ph,tt,1.0),ph=i)
    for i in range(3): ngd(cv,c,VA[i],250-i*130,905,t,.6,rig.dung(t+i),vk='giao')
    truoc(cv,c,t)
    nhan(cv,'thả tù binh về doanh trại quân Nguyên báo tin',960,170,t,a+.4,b,VIETC,38)
# 44: Thoát Hoan chờ mãi; sai Ô Mã Nhi ra biển đón
def S_44(cv,t):
    a,b=T[49]-.3,E[49]+.3;q=sb(49,1)
    c=kc(t,[(a,(900,620,1.3)),(q,(1000,640,1.2)),(b,(1100,650,1.1))])
    nen(cv,c,t,'song',seed=49,mist=.5)
    put(cv,c,'t26n_trai',960,860,ay=1,s=.5,k=.85,o=.85)
    ngd(cv,c,'thn6',720+40*math.sin(t*.8),905,t,.74,(ngam(rig.dung(t))|{'mat':'G'}) if t<q else rig.quat(t))
    if t>q: soi(cv,c,720,700,t,.7)
    ngd(cv,c,'omn6',1000,905,t,.7,lay(rig.dung(t),t),flip=True)
    for i in range(4): ngd(cv,c,MA[i%3],1250+i*150,905+(i%2)*10,t,.56,rig.dung(t+i)|{'mat':'S'},flip=True)
    truoc(cv,c,t)
    nhan(cv,'chờ mãi không thấy thuyền lương',960,170,t,a+.3,q,MONGC,40);nhan(cv,'sai Ô Mã Nhi ra biển đón',960,170,t,q+.2,b,MONGC,42)
# 45: bản đồ: Ô Mã Nhi ra cửa An Bang, không thấy thuyền lương
def S_45(cv,t):
    a,b=T[50]-.3,E[51]+.3;q=T[51]
    vk,bd=tuple(PTM['vankiep']),tuple(PTM['bachdang']);ab=(675,628)
    c=mcam(t,[(a,(600,610,2.6)),(b,(640,620,2.4))])
    bando(cv,c,t,a)
    diem(cv,c,'Vạn Kiếp',vk,t,a,MONGC,dx=-24,dy=-20)
    di_=[vk,(560,610),bd,ab];duong(cv,c,di_,t,a+.3,q-a-.4,MONGC,4)
    for j in range(3): cotheo(cv,c,'t23n_thuyen',di_,t,a+.3+j*.2,q-a,s=.05,ph=j)
    if t>a+1.5:
        for i in range(8): put(cv,c,'t23n_thuyen',575+i*9,600+(i%3)*10+2*math.sin(t*3+i),s=.035,o=.8)
        nhan(cv,'sử nhà Nguyên · hơn một nghìn thuyền Đại Việt',960,150,t,a+1.5,q,VIETC,38)
    if t>q:
        diem(cv,c,'cửa An Bang',ab,t,q,RED,dx=24,dy=20);pulse(cv,c,*ab,t)
        ve=list(reversed(di_));duong(cv,c,ve,t,q+1.2,b-q-1.4,(.5,.4,.3),3)
        nhan(cv,'không thấy bóng một chiếc thuyền lương',960,150,t,q+.2,b,RED,40)
# 46: các tướng bàn rút
def S_46(cv,t):
    a,b=T[52]-.3,E[52]+.3
    c=kc(t,[(a,(960,620,1.2)),(b,(960,640,1.35))])
    nen(cv,c,t,seed=52,mist=.3)
    put(cv,c,'t26n_trai',960,860,ay=1,s=.5,k=.85,o=.8)
    ngd(cv,c,'thn6',960,905,t,.74,rig.dung(t)|{'head':6})
    for i,k in enumerate(['m9','m8','omn6']): ngd(cv,c,k,600-i*160,905,t,.66,rig.dung(t+i)|{'arF':-80+10*math.sin(t*3+i),'faF':-30,'mat':'S'})
    for i,k in enumerate(['m7','m9']): ngd(cv,c,k,1300+i*160,905,t,.66,rig.dung(t+i)|{'arF':-80,'faF':-30,'mat':'S'},flip=True)
    truoc(cv,c,t)
    nhan(cv,'không thành để giữ · không kho lương · thuyền lương không đến',960,170,t,a+.3,b,MONGC,36)
# 47: trời sắp nóng; rút quân
def S_47(cv,t):
    a,b=T[53]-.3,E[53]+.3;q=sb(53,1)
    c=kc(t,[(a,(960,600,1.1)),(b,(1100,620,1.0))])
    nen(cv,c,t,seed=53,mist=.2)
    put(cv,c,'t26_nang',1500,260,s=.6,o=.8*inn(t,a,1.5),k=.3)
    if t<q:
        for i in range(5):
            P=rig.dung(t+i);P.update(lean=14,head=10,arB=20,faB=-60,mat='S');ngd(cv,c,MA[i%3],500+i*220,905+(i%2)*10,t,.6,P)
        nhan(cv,'trời sắp vào mùa nóng',960,170,t,a+.3,q,INK,44)
    else:
        for i in range(7): chay(cv,c,MA[i%3],800+i*140,-300+i*140,905+(i%2)*10,t,q+i*.1,b+3,.56,lambda ph,tt:rig.hoang(ph,tt,.9),ph=i)
        for i in range(2): put(cv,c,Af('t26_spr_coN'),1200+i*300-1500*inn(t,q,b-q+3),880,s=.5,ay=1,r=3*math.sin(t*3+i))
        nhan(cv,'Thoát Hoan cho rút cả đạo quân',960,170,t,q+.2,b,MONGC,42)
    truoc(cv,c,t)
# 48: Toàn thư: Khánh Dư có phần công
def S_48(cv,t):
    a,b=T[54]-.3,E[54]+.3
    c=kc(t,[(a,(960,620,1.05)),(b,(960,600,1.12))])
    bien(cv,c,t,seed=54,mist=.6,bo=True)
    for i in range(3): thuyen(cv,c,1100+i*260+90*(t-a),800+(i%2)*20,t,s=.34,ngoi=[('v8',-30,'cheo')],ph=i)
    ngd(cv,c,'tkd',1500,905,t,.7,rig.dung(t)|{'mat':'V'},flip=True,vk='dao')
    cuon(cv,760,470,t,'TOÀN THƯ','không thảm như lần trước|Trần Khánh Dư|có phần công lao',col=RED,s=.8,sz=36,u=inn(t,a+.5,2.4))
# 49: kết
def S_49(cv,t):
    a=T[55]-.3;b=E[55]+4
    c=kc(t,[(a,(900,620,1.05)),(b,(1100,580,1.0))])
    bien(cv,c,t,seed=55,mist=.65,bo=True)
    ngd(cv,c,'tkd',1350,905,t,.66,ngam(rig.dung(t)),flip=True)
    for i in range(3): thuyen(cv,c,200+i*400+150*inn(t,a,b-a),820+(i%2)*25,t,s=.42,ngoi=[('v8',-40,'cheo'),(VA[i%2],40,None)],ph=i)
    for i in range(3): put(cv,c,'t26n_gao',500+i*260+20*math.sin(t*.6+i),880+5*math.sin(t+i),s=.22,r=40*i+10*math.sin(t*.4),o=.6)
    daotruoc(cv,c,t,sd=14)
    if not FREEZE: put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,150,inn(t,E[55]+.6,1))
# ---------- ráp cảnh ----------
SC_LIST=[(0,S_1),(T[2]-.3,S_2),(T[3]-.3,S_3),(T[4]-.3,S_4),(T[5]-.3,S_5),(T[6]-.3,S_6),(T[8]-.3,S_7),(T[9]-.3,S_8),(T[10]-.3,S_9),
 (T[11]-.3,S_10),(T[12]-.3,S_11),(T[13]-.3,S_12),(T[14]-.3,S_13),(T[15]-.3,S_14),(T[16]-.3,S_15),(T[17]-.3,S_16),(T[18]-.3,S_17),(T[19]-.3,S_18),
 (T[20]-.3,S_19),(T[22]-.3,S_20),(T[23]-.3,S_21),(T[24]-.3,S_22),(T[25]-.3,S_23),(T[26]-.3,S_24),(T[27]-.3,S_25),(T[28]-.3,S_26),(T[29]-.3,S_27),
 (T[30]-.3,S_28),(T[31]-.3,S_29),(T[32]-.3,S_30),(T[34]-.3,S_31),(T[35]-.3,S_32),(T[36]-.3,S_33),(T[37]-.3,S_34),(T[38]-.3,S_35),(T[39]-.3,S_36),
 (T[40]-.3,S_37),(T[42]-.3,S_38),(T[44]-.3,S_39),(T[45]-.3,S_40),(T[46]-.3,S_41),(T[47]-.3,S_42),(T[48]-.3,S_43),(T[49]-.3,S_44),(T[50]-.3,S_45),
 (T[52]-.3,S_46),(T[53]-.3,S_47),(T[54]-.3,S_48),(T[55]-.3,S_49)]
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
SH=[(SC_LIST[i][0],SC_LIST[i+1][0] if i<len(SC_LIST)-1 else V.TOTAL+1,SC_LIST[i][1]) for i in range(len(SC_LIST))]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm26_full.json'))
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
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'THUYỀN LƯƠNG VÂN ĐỒN','stitle26',.55)
    if not NOCAP: caps(cv,t)
V.NHAN={}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
