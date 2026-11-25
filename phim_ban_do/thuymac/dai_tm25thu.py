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
# =================== các cảnh (đoạn làm thử: Hàm Tử, đoạn 11–14) ===================
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
        for i in range(3): dust(cv,c,800+i*120,880,o=.25,s=.5+.05*math.sin(t+i))
        truoc(cv,c,t)
        if not FREEZE: ink_wash(cv,.3)
        nhan(cv,'nhà Tống đã mất năm 1279',960,330,t,q+1.3,b,INK,46)
G_THU=[(T[11]-.3,'A'),(T[12]-.4,'B'),(T[13]-.3,'C'),(T[14]-.2,'D')]
SH=[(G_THU[i][0],G_THU[i+1][0] if i<3 else E[14]+.6,globals()['S_'+G_THU[i][1]]) for i in range(4)]
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
    if not NOCAP: caps(cv,t)
V.NHAN={}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
