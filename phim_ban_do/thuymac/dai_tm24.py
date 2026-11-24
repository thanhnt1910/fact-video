# dai_tm24: Hai chữ trên cánh tay (1284–1285), lời kể bản 5, giọng Charon lần 3. Nhân vật múa rối riêng tập (t24n_r_*).
# Hình ảnh lặp lại: cánh tay có hai chữ Sát Thát (t24n_canhtay) ở mở đầu, lúc quân Nguyên phát hiện, lúc Đỗ Khắc Chung giơ tay, và kết.
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
V=K.setup('tm24',{6:4.0})
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
    put(cv,c,'t24_far',960+seed*60,g-120,ay=1,k=.35,o=far)
    put(cv,c,'t24_mid',960-seed*40,g+30,ay=1,k=.62,o=midv)
    suong(cv,c,t,g-260,mist,seed)
def truoc(cv,c,t,o=1):
    put(cv,c,'t24_frontL',-120,1120,ax=0,ay=1,k=1.3,s=.85,r=1.2*math.sin(t*.8),o=o)
    put(cv,c,'t24_frontR',2040,1120,ax=1,ay=1,k=1.3,s=.8,r=1.2*math.sin(t*.7+1),o=o)
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
        rg=np.random.default_rng(24);a=rg.random((34,60)).astype(np.float32)
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
    put(cv,c,'t24_far',960+sd*50,g-120,ay=1,k=.35,o=.85)
    if kieu=='song':
        put(cv,c,'t24_mid',960-sd*40,g-170,ay=1,k=.5,o=.6)
        put(cv,c,'t24_song',960,g-270,ay=0,k=.8,s=1.0,o=.95)
    else: put(cv,c,'t24_mid',960-sd*40,g+30,ay=1,k=.62,o=.8)
    suong(cv,c,t,g-260,mist,seed)
def song(cv,c,t,y=620,o=.95):
    put(cv,c,'t24_song',960,y,ay=0,k=.85,o=o)
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
    put(cv,C0,'t24_cuon',x,y,s=s,o=o)
    if FREEZE: return
    put_screen(cv,text(tieu,28,INK,700),x,y-170*s/.62,o)
    for k,ln in enumerate(chu.split('|')): put_screen(cv,wipe(text(ln,sz,col if col is not None else RED,700),u,0,.25,seed=int(x)+k),x,y-20+k*(sz+16),o)
def nhan(cv,txt,x,y,t,t0,t1,col=None,sz=40,w=None):
    if FREEZE or not(t0<t<t1): return
    u=inn(t,t0,.35)*(1-inn(t,t1-.35,.35));tx=text(txt,sz,col if col is not None else INK,700)
    put_screen(cv,band(w or tx.shape[1]+50,tx.shape[0]+26,PAPER,.86,18),x,y,u);put_screen(cv,tx,x,y,u)
for _k in ['dkc','hdv','tnt','tts','tbt','iat','tkn','yk','dtg','tlai','bl1','bl2','omn','tdo','thn','v1','v2','v3','m1','m2','m3','q24']: rig.PRE[_k]='t24n_r_'
def tay(cv,x,y,t,t0,t1,s=.62,o=1.0):
    """cánh tay có hai chữ Sát Thát (hình ảnh lặp lại), hiện như tranh chèn giữa màn hình"""
    if FREEZE: return put(cv,C0,'t24n_canhtay',x,y,s=s,o=o)
    if not(t0<t<t1): return
    u=inn(t,t0,.6)*(1-inn(t,t1-.5,.5));put(cv,C0,'t24n_canhtay',x+30*(t-t0),y,s=s*(1+.03*(t-t0)),o=u*o)
def gio(PP,t_): PP.update(arF=-150+6*math.sin(t_*2),faF=-10)
# =================== các cảnh ===================
G=[(1,1),(2,2),(3,3),(4,5),(6,7),(8,9),(10,11),(12,13),(14,15),(16,17),(18,19),(20,22),(23,24),(25,26),(27,28),(29,30),(31,32),(33,34),(35,36),(37,39),(40,42),(43,45),(46,46),(47,48),(49,50),(51,51),(52,53),(54,55),(56,58),(59,59),(60,60),(61,62),(63,63),(64,64),(65,65),(66,67)]
def AB(i): a,b=G[i-1];return T[a]-.3,E[b]+.3
def bat(PP,t_): PP.update(arF=-70,faF=-60,arB=40,faB=-30,lean=10)
def troi(PP,t_): PP.update(arF=20,faF=-80,arB=20,faB=-80,lean=12)
def ngoiq(PP,t_): PP.update(thF=-80,thB=-76,knF=84,knB=82)
# 1: quân giặc kéo tay áo người lính bị bắt
def S_1(cv,t):
    a,b=0,E[1]+.3
    c=kc(t,[(a,(1000,560,1.2)),(b,(980,540,1.35))])
    nen(cv,c,t,seed=1,mist=.6)
    nguoi(cv,c,'v2',900,905,t,s=.64,PP=rig.dung(t)|{'arF':30,'faF':-60,'lean':14})
    dib(cv,c,'m2',1300,1060,905,t,a,a+2,s=.64,vk=None,sua=bat,flip=True)
    dib(cv,c,'m1',1700,1350,905,t,a+.4,b,s=.62,vk='daocong',flip=True)
    dib(cv,c,'m3',300,600,905,t,a,b,s=.6,vk='moc')
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.2)
# 2: cận cánh tay, Sát Thát
def S_2(cv,t):
    a,b=AB(2);q=sb(2,1)
    c=kc(t,[(a,(960,560,1.05)),(b,(960,540,1.0))])
    nen(cv,c,t,seed=2,mist=.7)
    for i in range(4): dib(cv,c,['v1','v3','v2','v1'][i],300+i*380,320+i*380,905,t,a,b,s=.58,sua=troi,ph=i)
    for i in range(3): dib(cv,c,['m1','m2','m3'][i],500+i*420,560+i*420,905,t,a,b,s=.6,vk=['daocong','moc','daocong'][i],ph=i,flip=True)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.45*inn(t,a,.6))
    tay(cv,960,430,t,a+.1,b,s=.85)
    nhan(cv,'Sát Thát = giết giặc Thát Đát',960,760,t,a+.8,q-.1,RED,46)
    nhan(cv,'rất nhiều người bị giết',960,760,t,q+.1,b,INK,44)
# 3: viên quan nhỏ giơ cánh tay trước tướng giặc
def S_3(cv,t):
    a,b=AB(3)
    c=kc(t,[(a,(1100,560,1.05)),(b,(1000,540,1.2))])
    nen(cv,c,t,seed=3)
    put(cv,c,'t24n_trai',1100,860,ay=1,s=.5,k=.85,o=.9)
    co(cv,c,'t24_spr_colon',1650,880,t,s=.55)
    nguoi(cv,c,'omn',1350,905,t,s=.66,vk='daocong',flip=True)
    for i in range(2): nguoi(cv,c,['m2','m1'][i],1560+i*150,905,t,s=.6,vk=['moc','cung'][i],flip=True,ph=i)
    def g3(PP,t_): PP.update(arF=-150*inn(t_,a+2,1)+20,faF=-10)
    dib(cv,c,'dkc',500,900,905,t,a,a+2.4,s=.64,sua=g3)
    truoc(cv,c,t)
# 4: Đỗ Khắc Chung đi khỏi; tướng giặc quay sang các tướng; câu hỏi
def S_4(cv,t):
    a,b=AB(4);q=T[5]
    c=kc(t,[(a,(1000,560,1.1)),(b,(1200,540,1.2))])
    nen(cv,c,t,seed=4)
    put(cv,c,'t24n_trai',900,860,ay=1,s=.52,k=.85,o=.85)
    dib(cv,c,'dkc',900,-200,905,t,a,a+4,s=.62)
    def quay(PP,t_): PP.update(arF=-50+10*math.sin(t_*2),faF=-50)
    nguoi(cv,c,'omn',1350,905,t,s=.66,vk='daocong',flip=t>a+2.5,PP=None)
    for i in range(3): nguoi(cv,c,['m1','m2','m3'][i],1550+i*140,905,t,s=.6,vk=['cung','moc','daocong'][i],flip=True,ph=i)
    truoc(cv,c,t)
    if not FREEZE and t>q: ink_wash(cv,.3*inn(t,q,.6))
    nhan(cv,'vì sao biết là chết mà vẫn xăm?',960,250,t,q+.1,sb(5,1),RED,46)
    nhan(cv,'tướng giặc đã thấy gì?',960,250,t,sb(5,1)+.1,b,INK,46)
# 5: duyệt binh Đông Bộ Đầu
def S_5(cv,t):
    a,b=AB(5);q=T[7]
    c=kc(t,[(a,(800,560,1.0)),(b,(1100,540,1.1))])
    nen(cv,c,t,'song',seed=5)
    for i in range(3): thuyen(cv,c,300+i*500,780,t,s=.46,ngoi=[('v1',-50,'cheo'),('v2',40,'cheo')],ph=i)
    nguoi(cv,c,'hdv',380,905,t,s=.66,vk='dao')
    for i in range(6): dib(cv,c,['v1','v2','v3'][i%3],2200+i*150,800+i*150,905+(i%2)*12,t,a+i*.15,q+1,s=.55,vk=['giao','no','dao'][i%3],ph=i)
    truoc(cv,c,t)
    seal(cv,'s1284',1580,280,a+.6,t,s=.8,r=4)
    nhan(cv,'Hưng Đạo Vương Trần Quốc Tuấn duyệt binh',960,170,t,a+.3,q-.2,VIETC,40);nhan(cv,'chia quân giữ bến Bình Than',960,170,t,sb(7,1),b,VIETC,40)
# 6: sứ về báo tin; Thoát Hoan
def S_6(cv,t):
    a,b=AB(6);q=T[9]
    c=kc(t,[(a,(900,560,1.05)),(q,(1200,560,1.0)),(b,(1300,540,1.08))])
    nen(cv,c,t,seed=6)
    if t<q+.5:
        ngua(cv,c,'den','q24',-300,700,900,t,a,a+3,s=.56)
        nguoi(cv,c,'tnt',1000,905,t,s=.64,flip=True)
    else:
        ngua(cv,c,'den','thn',2000,1300,900,t,q,b,s=.6,vk='cung',flip=True)
        for i in range(4): ngua(cv,c,['nau','den','nau','den'][i],'m1',2200+i*220,1500+i*200,900+(i%2)*14,t,q+.2+i*.2,b,s=.52,vk='cung',ph=i,flip=True)
    truoc(cv,c,t)
    nhan(cv,'sứ giả từ phương Bắc về báo tin',960,170,t,a+.3,sb(8,1),INK,40);nhan(cv,'hoàng tử Thoát Hoan đem đại quân sang',960,170,t,sb(8,1)+.1,q-.1,MONGC,40)
    nhan(cv,'cái cớ: mượn đường đánh Chiêm Thành',960,170,t,q+.1,b,MONGC,40)
# 7: hội nghị Diên Hồng
def S_7(cv,t):
    a,b=AB(7);q=T[11]
    c=kc(t,[(a,(960,600,1.0)),(b,(960,560,1.1))])
    put(cv,c,'t24_dien',960,1010,ay=1,s=.78,k=.9)
    nguoi(cv,c,'tts',960,850,t,s=.6)
    def ho(PP,t_): 
        if t_>q: PP.update(arF=-150+8*math.sin(t_*5),faF=-10)
    for i in range(7):
        x0=-300-i*120 if i<4 else 2300+(i-4)*130;x1=300+i*140 if i<4 else 1550+(i-4)*140
        dib(cv,c,['bl1','bl2','bl1','bl2','bl2','bl1','bl2'][i],x0,x1,905+(i%2)*14,t,a+i*.2,q-.3,s=.56,ph=i,sua=ho,flip=(i>=4))
    truoc(cv,c,t)
    nhan(cv,'thềm điện Diên Hồng',960,170,t,a+.3,q-.2,INK,42)
    if not FREEZE and t>q: big(cv,'ĐÁNH!',t,q+.1,b,RED,300,96,seed=11)
# 8: các ải biên giới; vua đi thuyền nhẹ
def S_8(cv,t):
    a,b=AB(8);q=T[13]
    c=kc(t,[(a,(1100,540,1.0)),(b,(900,560,1.08))])
    put(cv,c,'t24_ai',960,900,ay=1,s=.75,k=.6,o=.9)
    for i in range(4): ngua(cv,c,['nau','den','nau','den'][i],'m1',2400+i*200,1100+i*170,900+(i%2)*14,t,a+i*.2,q,s=.52,vk='cung',ph=i,flip=True)
    for i in range(4): dib(cv,c,['v1','v3','v2','v1'][i],1000-i*130,-300-i*150,905,t,a+.8,b,s=.55,vk=['giao','dao','no','giao'][i],ph=i,chay=1.2)
    ten(cv,c,t,a,q,[(1900,560),(2000,600)],[(800,840),(1100,860)],n=10,h=140)
    truoc(cv,c,t)
    nhan(cv,'ngày 26 tháng chạp · ải Chi Lăng',960,170,t,a+.3,q-.2,INK,40);nhan(cv,'rút về bến Vạn Kiếp',960,170,t,q+.1,b,VIETC,42)
# 9: vua chưa ăn cơm sáng; Trần Lai
def S_9(cv,t):
    a,b=AB(9);q=sb(14,1)
    c=kc(t,[(a,(900,560,1.05)),(b,(1000,540,1.18))])
    nen(cv,c,t,'song',seed=9,mist=.6)
    thuyen(cv,c,900,800,t,s=.6,ngoi=[('tnt',-30,None),('v1',80,'cheo')])
    thuyen(cv,c,1450,820,t,s=.5,ngoi=[('tlai',0,None)],flip=True,ph=2)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.25+.1*inn(t,a,2))
    nhan(cv,'Trần Lai · một người lính',960,170,t,q+.1,T[15]-.1,VIETC,40);nhan(cv,'được ban một chức nhỏ ở Bạch Đằng',960,170,t,T[15]+.1,b,INK,40)
# 10: Hưng Đạo Vương rút theo chân núi; Dã Tượng
def S_10(cv,t):
    a,b=AB(10);q=T[17]
    c=kc(t,[(a,(900,560,1.05)),(b,(1100,540,1.15))])
    put(cv,c,'t24_far',960,780,ay=1,k=.35,o=.85);put(cv,c,'t24_mid',900,930,ay=1,k=.62,o=.85)
    dib(cv,c,'hdv',-200,900,905,t,a,b,s=.64,vk='dao')
    dib(cv,c,'dtg',-400,700,905,t,a,b,s=.66,ph=1)
    truoc(cv,c,t)
    nhan(cv,'Dã Tượng · voi rừng',800,250,t,q+.1,b,INK,42);nhan(cv,'Yết Kiêu · một loài chó săn',1250,330,t,sb(17,1)-1.5,b,INK,42)
# 11: Yết Kiêu giữ thuyền ở Bãi Tân
def S_11(cv,t):
    a,b=AB(11);q=T[19]
    c=kc(t,[(a,(1200,560,1.1)),(q,(1000,560,1.0)),(b,(800,560,1.1))])
    nen(cv,c,t,'song',seed=11,mist=.55)
    thuyen(cv,c,1300,800,t,s=.6,ngoi=[('yk',-20,'cheo')])
    if t>q-.5:
        nguoi(cv,c,'hdv',400,905,t,s=.64,vk='dao')
        def noi(PP,t_): PP.update(arF=-50+15*math.sin(t_*3),faF=-40)
        nguoi(cv,c,'dtg',620,905,t,s=.66,flip=True,PP=rig.dung(t)|{'arF':-50+15*math.sin(t*3),'faF':-40})
    truoc(cv,c,t)
    nhan(cv,'Yết Kiêu giữ thuyền ở Bãi Tân',960,170,t,a+.3,q-.2,VIETC,42)
    nhan(cv,'chưa thấy Đại Vương thì không rời thuyền',960,170,t,q+.2,b,INK,40)
# 12: đến Bãi Tân, lên thuyền, kỵ binh đuổi không kịp
def S_12(cv,t):
    a,b=AB(12);q=T[21];r=T[22]
    c=kc(t,[(a,(800,560,1.05)),(q,(900,540,1.15)),(b,(1100,560,1.0))])
    nen(cv,c,t,'song',seed=12,mist=.6)
    xb=900 if t<r else 900-700*inn(t,r,b-r)
    thuyen(cv,c,xb,800,t,s=.6,ngoi=([('yk',60,'cheo')]+([('hdv',-40,'dao')] if t>q-.5 else [])))
    if t<q: dib(cv,c,'hdv',-200,700,905,t,a,q-.5,s=.64,vk='dao')
    if t>r:
        for i in range(3): ngua(cv,c,['nau','den','nau'][i],'m1',2400+i*200,1300+i*180,900+(i%2)*14,t,r+.2+i*.2,b,s=.52,vk='cung',ph=i,flip=True)
    truoc(cv,c,t)
    nhan(cv,'chim hồng hộc bay cao nhờ sáu chiếc lông cánh lớn',960,170,t,q+.2,r-.1,INK,38)
    nhan(cv,'kỵ binh giặc đuổi không kịp',960,170,t,r+.8,b,VIETC,42)
# 13: Ô Mã Nhi đánh Vạn Kiếp; tràn vào Gia Lâm
def S_13(cv,t):
    a,b=AB(13);q=T[24]
    hit=a+1.0;sh=(4*math.sin(t*37)*(1-inn(t,hit+.3,.6))) if hit<t<hit+.9 and not FREEZE else 0
    c=kc(t,[(a,(1200,540,1.05)),(b,(800,560,1.0))],sh)
    nen(cv,c,t,seed=13)
    dib(cv,c,'omn',2200,1300,905,t,a,q,s=.66,vk='daocong',flip=True)
    for i in range(5): dib(cv,c,['m2','m3','m1','m2','m3'][i],2400+i*150,1400+i*150-300*inn(t,q,b-q),905+(i%2)*12,t,a+.2+i*.15,b,s=.56,vk=['moc','daocong','cung','moc','daocong'][i],ph=i,flip=True)
    for i in range(3): dib(cv,c,['v1','v2','v3'][i],900-i*140,-300-i*140,905,t,a+.8,q+1,s=.55,vk=['giao','no','dao'][i],ph=i,chay=1.2)
    truoc(cv,c,t)
    seal(cv,'s1285',1580,280,a+.6,t,s=.8,r=4)
    nhan(cv,'Ô Mã Nhi đánh Vạn Kiếp, núi Phả Lại',960,170,t,a+.3,q-.2,MONGC,40);nhan(cv,'Gia Lâm · Vũ Ninh · Đông Ngàn',960,170,t,q+.1,b,INK,42)
# 14: phát hiện hai chữ Sát Thát
def S_14(cv,t):
    a,b=AB(14);q=T[26]
    c=kc(t,[(a,(1000,560,1.15)),(b,(960,540,1.05))])
    nen(cv,c,t,seed=14,mist=.6)
    for i in range(3): nguoi(cv,c,['v1','v2','v3'][i],600+i*260,905,t,s=.6,PP=rig.dung(t+i)|{'arF':30,'faF':-60,'lean':14})
    for i in range(3): dib(cv,c,['m2','m1','m3'][i],1800+i*130,820+i*260+80,905,t,a+i*.3,a+2.5,s=.62,sua=bat,flip=True,ph=i)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.35*inn(t,q-.5,.8))
    tay(cv,960,430,t,a+2.2,q+.4,s=.55)
    nhan(cv,'không thể giấu, không thể xóa',960,250,t,q+.3,b,RED,44)
# 15: cờ lớn ở Đông Bộ Đầu; vua tìm người dò tình hình
def S_15(cv,t):
    a,b=AB(15);q=T[28]
    c=kc(t,[(a,(1200,540,1.0)),(q,(1100,560,1.05)),(b,(700,560,1.12))])
    nen(cv,c,t,'song',seed=15)
    put(cv,c,'t24n_trai',1500,700,ay=1,s=.45,k=.85,o=.9)
    co(cv,c,'t24_spr_colon',1250,720,t,s=.5)
    for i in range(3): dib(cv,c,['m1','m2','m3'][i],1900+i*160,1350+i*160,640,t,a+i*.3,b,s=.4,vk=['cung','moc','daocong'][i],ph=i,flip=True)
    if t>q-.3:
        nguoi(cv,c,'tnt',500,905,t,s=.64)
        for i in range(3): nguoi(cv,c,'q24',700+i*130,905,t,s=.6,flip=True,ph=i,PP=rig.dung(t+i)|{'lean':8})
    truoc(cv,c,t)
    nhan(cv,'bến Đông Bộ Đầu · trong tay quân giặc',960,170,t,a+.3,q-.2,MONGC,40)
# 16: Đỗ Khắc Chung xin đi
def S_16(cv,t):
    a,b=AB(16);q=T[30]
    c=kc(t,[(a,(900,560,1.1)),(b,(1000,540,1.2))])
    nen(cv,c,t,seed=16,mist=.5)
    nguoi(cv,c,'tnt',1250,905,t,s=.66,flip=True)
    for i in range(2): nguoi(cv,c,'q24',300+i*140,905,t,s=.6,ph=i)
    def lay(PP,t_): PP.update(lean=10+4*math.sin(t_),arF=-40,faF=-40,arB=-30,faB=-40)
    dib(cv,c,'dkc',500,980,905,t,a+.3,a+2.6,s=.64,sua=lay)
    truoc(cv,c,t)
    nhan(cv,'Đỗ Khắc Chung · một viên quan nhỏ',960,170,t,a+.4,q-.2,VIETC,40)
    nhan(cv,'ngựa quý giữa đám ngựa kéo xe muối',960,170,t,q+.1,b,INK,40)
# 17: hỏi tội; chó nhà cắn người lạ
def S_17(cv,t):
    a,b=AB(17);q=T[32]
    c=kc(t,[(a,(1000,560,1.05)),(b,(1000,540,1.15))])
    nen(cv,c,t,seed=17,mist=.4)
    put(cv,c,'t24n_trai',960,820,ay=1,s=.58,k=.85,o=.8)
    def chi(PP,t_): PP.update(arF=-90+10*math.sin(t_*3),faF=-10)
    nguoi(cv,c,'omn',1250,905,t,s=.68,vk='daocong',flip=True,PP=rig.dung(t)|({'arF':-90+10*math.sin(t*3),'faF':-10} if t<q else {}))
    for i in range(2): nguoi(cv,c,['m2','m3'][i],1480+i*150,905,t,s=.6,vk=['moc','daocong'][i],flip=True,ph=i)
    dib(cv,c,'dkc',300,760,905,t,a,a+2.2,s=.64)
    truoc(cv,c,t)
    nhan(cv,'vua nước ngươi vô lễ',960,170,t,a+.6,q-.2,MONGC,44);nhan(cv,'chó nhà cắn người lạ, đâu phải tại chủ',960,170,t,q+.1,b,VIETC,40)
# 18: giơ cánh tay
def S_18(cv,t):
    a,b=AB(18);q=T[34]
    c=kc(t,[(a,(960,560,1.15)),(b,(900,540,1.3))])
    nen(cv,c,t,seed=18,mist=.4)
    put(cv,c,'t24n_trai',960,820,ay=1,s=.58,k=.85,o=.8)
    nguoi(cv,c,'omn',1200,905,t,s=.68,vk='daocong',flip=True)
    def g18(PP,t_): PP.update(arF=-150*inn(t_,a+.6,.8)+20*(1-inn(t_,a+.6,.8)),faF=-10)
    dib(cv,c,'dkc',760,760,905,t,a,b,s=.64,sua=g18)
    truoc(cv,c,t)
    if not FREEZE and t>q: ink_wash(cv,.35*inn(t,q,.5))
    tay(cv,960,430,t,q,b,s=.6)
# 19: dọa nạt và câu đáp
def S_19(cv,t):
    a,b=AB(19);q=T[36]
    c=kc(t,[(a,(1150,540,1.15)),(q,(800,560,1.15)),(b,(960,560,1.05))])
    nen(cv,c,t,seed=19,mist=.4)
    put(cv,c,'t24n_trai',960,820,ay=1,s=.58,k=.85,o=.8)
    def doa(PP,t_): PP.update(arF=-120+30*math.sin(t_*4),faF=-30,lean=6)
    nguoi(cv,c,'omn',1150,905,t,s=.68,vk='daocong',flip=True,PP=rig.dung(t)|({'arF':-120+30*math.sin(t*4),'faF':-30,'lean':6} if t<q else {}))
    nguoi(cv,c,'dkc',760,905,t,s=.64)
    for i in range(2): nguoi(cv,c,['m1','m2'][i],1420+i*150,905,t,s=.6,vk=['cung','moc'][i],flip=True,ph=i)
    truoc(cv,c,t)
    nhan(cv,'bọ ngựa giơ càng cản bánh xe',960,170,t,a+.5,q-.2,MONGC,42);nhan(cv,'thú cùng đường còn cắn lại',960,170,t,q+.1,b,VIETC,42)
# 20: nước nó còn có người giỏi
def S_20(cv,t):
    a,b=AB(20);q=T[38];r=T[39]
    c=kc(t,[(a,(900,560,1.05)),(b,(1300,540,1.15))])
    nen(cv,c,t,seed=20)
    put(cv,c,'t24n_trai',1200,820,ay=1,s=.55,k=.85,o=.8)
    dib(cv,c,'dkc',800,-300,905,t,a,a+4,s=.62)
    nguoi(cv,c,'omn',1300,905,t,s=.68,vk='daocong',flip=False)
    for i in range(3): nguoi(cv,c,['m1','m2','m3'][i],1520+i*140,905,t,s=.6,vk=['cung','moc','daocong'][i],flip=True,ph=i)
    if t>r: ngua(cv,c,'nau','m1',1500,-300,900,t,sb(39,1),b,s=.52,vk='cung')
    truoc(cv,c,t)
    nhan(cv,'lời lẽ tự nhiên, không nhục mệnh vua',960,170,t,q+.1,r-.1,INK,40)
    if not FREEZE and t>r: big(cv,'NƯỚC NÓ CÒN CÓ NGƯỜI GIỎI',t,r+.1,sb(39,1)+.3,RED,320,60,seed=39)
# 21: Trần Kiện đầu hàng, bị bắn ở trại Ma Lục
def S_21(cv,t):
    a,b=AB(21);q=T[41];r=T[42]
    c=kc(t,[(a,(1000,560,1.05)),(r,(1100,560,1.05)),(b,(1200,540,1.1))])
    nen(cv,c,t,seed=21)
    if t<r:
        dib(cv,c,'tkn',300,1100,905,t,q,r,s=.64)
        for i in range(3): dib(cv,c,['v1','v2','v3'][i],100-i*150,900-i*150,905,t,q+.2,r,s=.55,ph=i)
        for i in range(2): nguoi(cv,c,['m1','m2'][i],1500+i*150,905,t,s=.6,vk=['cung','moc'][i],flip=True,ph=i)
        if t<q: dib(cv,c,'dkc',800,-300,905,t,a,q,s=.6)
    else:
        ngua(cv,c,'den','tkn',300,1300,900,t,r,b,s=.56,o=1-.6*inn(t,sb(42,1),.8))
        for i in range(2): ngua(cv,c,'nau','m1',100-i*200,1100-i*200,900,t,r,b,s=.52,vk='cung',ph=i)
        ten(cv,c,t,sb(42,1)-.6,b,[(1900,620),(1850,560)],[(1150,760),(1250,780)],n=6,h=80,col=VIETC)
    truoc(cv,c,t)
    nhan(cv,'không phải ai cũng chọn như Đỗ Khắc Chung',960,170,t,a+.3,q-.2,INK,40)
    nhan(cv,'Trần Kiện đem quân đầu hàng',960,170,t,q+.1,r-.1,MONGC,42);nhan(cv,'trại Ma Lục · Nguyễn Địa Lô bắn chết Trần Kiện',960,170,t,r+.1,b,VIETC,38)
# 22: Trần Bình Trọng
def S_22(cv,t):
    a,b=AB(22);q=T[44];r=T[45]
    hit=a+1;sh=(4*math.sin(t*37)*(1-inn(t,hit+.3,.6))) if hit<t<hit+.9 and not FREEZE else 0
    c=kc(t,[(a,(1000,540,1.05)),(q,(960,560,1.15)),(b,(960,540,1.25))],sh)
    nen(cv,c,t,seed=22,mist=.5)
    if t<q:
        dib(cv,c,'tbt',400,800,905,t,a,q,s=.64,vk='giao')
        for i in range(4): dib(cv,c,['m2','m3','m1','m2'][i],2000+i*140,1050+i*140,905,t,a,q,s=.58,vk=['moc','daocong','cung','moc'][i],ph=i,flip=True)
    else:
        nguoi(cv,c,'tbt',900,905,t,s=.66,PP=rig.dung(t)|{'arF':20,'faF':-70,'arB':20,'faB':-70})
        for i in range(2): nguoi(cv,c,['m1','m2'][i],1250+i*150,905,t,s=.6,vk=['cung','moc'][i],flip=True,ph=i)
        nguoi(cv,c,'thn',600,905,t,s=.64,PP=rig.dung(t)|{'arF':-60+10*math.sin(t*2),'faF':-40})
    truoc(cv,c,t)
    nhan(cv,'Trần Bình Trọng · bãi Đà Mạc',960,170,t,a+.3,q-.2,VIETC,42);nhan(cv,'không ăn, không trả lời',960,170,t,q+.1,r-.1,INK,42)
    if not FREEZE and t>r: big(cv,'THÀ LÀM MA NƯỚC NAM',t,sb(45,1)-1.8,b,RED,320,62,seed=45)
# 23: hai vua đi thuyền nhỏ; thuyền ngự đi hướng khác
def S_23(cv,t):
    a,b=AB(23)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.08))])
    nen(cv,c,t,'song',seed=23,mist=.65)
    thuyen(cv,c,700-500*inn(t,a+1,b-a),820,t,s=.5,ngoi=[('tts',-50,None),('tnt',20,None),('v1',90,'cheo')])
    thuyen(cv,c,1300+500*inn(t,a+1,b-a),780,t,s=.6,lon=True,flip=True,ph=2)
    truoc(cv,c,t)
    nhan(cv,'thuyền ngự đi hướng khác để đánh lừa quân giặc',960,170,t,sb(46,1),b,INK,38)
# 24: mối nghi; lời dặn của Yên Sinh Vương
def S_24(cv,t):
    a,b=AB(24);q=T[48]
    c=kc(t,[(a,(1000,560,1.1)),(b,(960,540,1.0))])
    nen(cv,c,t,seed=24,mist=.6)
    nguoi(cv,c,'hdv',960,905,t,s=.66,vk='gays')
    for i in range(4): nguoi(cv,c,'q24',[400,560,1350,1500][i],905,t,s=.6,flip=(i>=2),ph=i)
    truoc(cv,c,t)
    if not FREEZE and t>q:
        ink_wash(cv,.4*inn(t,q,.5));cuon(cv,960,470,t,'LỜI DẶN CỦA YÊN SINH VƯƠNG','giành lấy thiên hạ',col=RED,u=inn(t,q+.3,.8))
        nhan(cv,'Hưng Đạo Vương không cho là phải',960,800,t,sb(48,1),b,VIETC,40)
    nhan(cv,'nhiều người nghi ngại Hưng Đạo Vương',960,170,t,a+.3,q-.2,INK,40)
# 25: lời can của hai người đầy tớ
def S_25(cv,t):
    a,b=AB(25);q=T[50]
    c=kc(t,[(a,(960,560,1.1)),(b,(960,540,1.2))])
    nen(cv,c,t,seed=25,mist=.5)
    nguoi(cv,c,'hdv',1150,905,t,s=.66,flip=True,PP=rig.dung(t)|({'arF':-30,'faF':-90} if t>q+1 else {}))
    def lay(PP,t_): PP.update(lean=14+3*math.sin(t_),arF=-40,faF=-50,arB=-30,faB=-50)
    for i,k in enumerate(['yk','dtg']): dib(cv,c,k,400+i*160,700+i*160,905,t,a+.3,a+2,s=.64,sua=lay,ph=i)
    truoc(cv,c,t)
    nhan(cv,'giàu sang một thời, tiếng xấu nghìn năm',960,170,t,a+.6,q-.2,INK,40);nhan(cv,'thà chết già làm đầy tớ',960,170,t,q+.1,b,VIETC,44)
# 26: cây gậy bịt sắt
def S_26(cv,t):
    a,b=AB(26);q=sb(51,1)
    c=kc(t,[(a,(900,560,1.05)),(b,(1000,540,1.25))])
    nen(cv,c,t,seed=26)
    x=dib(cv,c,'hdv',300,1100,905,t,a,b,s=.66,vk='gays' if t<q+.4 else 'gay')
    dib(cv,c,'tnt',500,1300,905,t,a,b,s=.64)
    for i in range(3): nguoi(cv,c,'q24',[1500,1650,250][i],905,t,s=.6,flip=(i<2),ph=i)
    truoc(cv,c,t)
    nhan(cv,'rút đầu sắt vứt đi, chỉ chống gậy không',960,170,t,q+.3,b,VIETC,40)
# 27: Trần Ích Tắc hàng giặc
def S_27(cv,t):
    a,b=AB(27);q=T[53]
    c=kc(t,[(a,(900,560,1.05)),(b,(1200,540,1.12))])
    nen(cv,c,t,seed=27)
    put(cv,c,'t24n_trai',1500,820,ay=1,s=.5,k=.85,o=.75)
    dib(cv,c,'iat',100,1050,905,t,a,q,s=.64)
    for i in range(3): dib(cv,c,['dan','dan','q24'][i] if False else ['v2','q24','q24'][i],-100-i*150,850-i*150,905,t,a+.2,q,s=.55,ph=i)
    nguoi(cv,c,'thn',1400,905,t,s=.66,flip=True,PP=rig.dung(t)|({'arF':-80,'faF':-30} if t>q else {}))
    truoc(cv,c,t)
    nhan(cv,'Trần Ích Tắc · em ruột thượng hoàng',960,170,t,a+.3,q-.2,INK,40);nhan(cv,'An Nam quốc vương',960,170,t,q+.1,sb(53,1),MONGC,46)
    nhan(cv,'người chọn chết · người nhận tước vương từ tay giặc',960,170,t,sb(53,1)+.1,b,RED,36)
# 28: Toa Đô từ phía nam; hai gọng kìm
def S_28(cv,t):
    a,b=AB(28);q=T[55]
    c=kc(t,[(a,(960,540,1.0)),(b,(960,540,1.06))])
    if t<q:
        nen(cv,c,t,seed=28)
        ngua(cv,c,'nau','tdo',-300,900,900,t,a,q,s=.6,vk='moc')
        for i in range(4): ngua(cv,c,['den','nau','den','nau'][i],'m2',-500-i*220,700-i*200,900+(i%2)*14,t,a+.2+i*.2,q,s=.52,vk='moc',ph=i)
        truoc(cv,c,t)
        seal(cv,'shen3',1580,280,sb(54,1),t,s=.8,r=4)
    else:
        nen(cv,c,t,seed=29)
        for i in range(3): dib(cv,c,['v1','v2','v3'][i],860+i*110,880+i*110,905,t,q,b,s=.56,vk=['giao','no','dao'][i],ph=i)
        ngua(cv,c,'den','thn',-300,450,900,t,q,b-1,s=.58,vk='cung')
        for i in range(2): ngua(cv,c,'nau','m1',-500-i*200,250-i*150,900,t,q+.2,b-1,s=.5,vk='cung',ph=i)
        ngua(cv,c,'nau','tdo',2200,1500,900,t,q,b-1,s=.58,vk='moc',flip=True)
        for i in range(2): ngua(cv,c,'den','m2',2400+i*200,1700+i*150,900,t,q+.2,b-1,s=.5,vk='moc',ph=i,flip=True)
        truoc(cv,c,t)
        nhan(cv,'Thoát Hoan · phía bắc',450,300,t,q+.4,b,MONGC,40);nhan(cv,'Toa Đô · phía nam',1480,300,t,q+.6,b,MONGC,40)
        nhan(cv,'nhà Trần ở giữa',960,620,t,q+1.2,b,VIETC,40)
    nhan(cv,'Toa Đô · đánh ra vùng Nghệ An, Thanh Hóa',960,170,t,a+.3,q-.2,MONGC,40)
# 29: lấy nhàn chống mệt
def S_29(cv,t):
    a,b=AB(29);q=T[58]
    c=kc(t,[(a,(960,560,1.05)),(b,(960,540,1.12))])
    nen(cv,c,t,'song',seed=29,mist=.5)
    thuyen(cv,c,960,800,t,s=.62,lon=True,ngoi=[('tnt',-300,None),('hdv',-230,'dao')])
    for i in range(2): nguoi(cv,c,'q24',[350,500][i],905,t,s=.58,ph=i)
    truoc(cv,c,t)
    nhan(cv,'vì sao vẫn có thể thắng?',960,170,t,a+.3,T[57]-.1,RED,44)
    nhan(cv,'giặc đi xa · lương chở hàng vạn dặm',960,170,t,T[57]+.1,q-.1,INK,40)
    if not FREEZE and t>q: big(cv,'LẤY NHÀN CHỐNG MỆT',t,q+.1,b,RED,320,72,seed=58)
# 30: đường chở lương càng dài
def S_30(cv,t):
    a,b=AB(30)
    c=kc(t,[(a,(1100,560,1.0)),(b,(800,560,1.05))])
    nen(cv,c,t,seed=30,mist=.6)
    def met(PP,t_): PP.update(lean=16,arF=10,faF=-40)
    for i in range(6): dib(cv,c,['m3','m1','m2'][i%3],1700+i*170,300+i*170,905+(i%2)*12,t,a+i*.15,b+2,s=.55,ph=i,sua=met,chay=.6,buoc=40)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.2)
    nhan(cv,'càng tiến sâu, đường chở lương càng dài',960,170,t,a+.3,b,INK,40)
# 31: quân nhà Trần đánh trở lại
def S_31(cv,t):
    a,b=AB(31)
    c=kc(t,[(a,(800,560,1.0)),(b,(1200,560,1.1))])
    nen(cv,c,t,'song',seed=31)
    for i in range(4): thuyen(cv,c,-200+i*330+700*inn(t,a,b-a),790+(i%2)*30,t,s=.48,ngoi=[('v1',-50,'cheo'),('v3',40,'giao')],ph=i)
    for i in range(4): dib(cv,c,['m1','m2','m3','m1'][i],1500+i*120,2500+i*120,905,t,a+.5+i*.1,b,s=.55,vk=['cung','moc','daocong','cung'][i],ph=i,chay=1.3)
    truoc(cv,c,t)
    nhan(cv,'mùa hè năm 1285 · quân Nguyên bỏ chạy',960,170,t,a+.3,b,VIETC,40)
# 32: ba năm sau; hòm thư xin hàng
def S_32(cv,t):
    a,b=AB(32);q=T[62]
    c=kc(t,[(a,(960,560,1.05)),(b,(960,540,1.15))])
    nen(cv,c,t,seed=32,mist=.55)
    if t<q:
        for i in range(4): dib(cv,c,['m1','m2','m3','m1'][i],500+i*130,2300+i*130,905,t,a+.3+i*.1,q+2,s=.55,ph=i,chay=1.3)
    else:
        put(cv,c,'t24_hom',960,760,s=.6,o=inn(t,q,.5))
        for i in range(2): nguoi(cv,c,['v1','v2'][i],[600,1320][i],905,t,s=.6,flip=(i==1),ph=i)
    truoc(cv,c,t)
    nhan(cv,'ba năm sau, quân Nguyên lại thua chạy',960,170,t,a+.3,q-.2,INK,40);nhan(cv,'một hòm thư xin hàng',960,170,t,q+.1,b,RED,44)
# 33: thượng hoàng sai đốt
def S_33(cv,t):
    a,b=AB(33)
    c=kc(t,[(a,(960,560,1.05)),(b,(960,540,1.12))])
    nen(cv,c,t,seed=33,mist=.4)
    put(cv,c,'t24_lua',960,900,ay=1,s=.55*(1+.02*math.sin(t*6)),o=.95)
    nguoi(cv,c,'tts',1400,905,t,s=.66,flip=True,PP=rig.dung(t)|{'arF':-70,'faF':-20})
    nguoi(cv,c,'v2',600,905,t,s=.58)
    for i in range(2): smoke(cv,c,900+i*120,520,t+i,1.0)
    truoc(cv,c,t)
    nhan(cv,'đốt hết đi, để người dao động được yên lòng',960,170,t,a+.3,b,INK,40)
# 34: đổi họ
def S_34(cv,t):
    a,b=AB(34);q=sb(64,1)
    c=kc(t,[(a,(960,560,1.04)),(b,(960,560,1.0))])
    nen(cv,c,t,seed=34,mist=.65)
    nguoi(cv,c,'tkn',500,905,t,s=.6,o=.5);nguoi(cv,c,'iat',1420,905,t,s=.6,o=.5,flip=True)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3)
    cuon(cv,560,470,t,'TRẦN KIỆN','đổi sang|họ Mai',col=RED,s=.6,sz=44)
    cuon(cv,1360,470,t,'TRẦN ÍCH TẮC','bị gọi là|Ả Trần',col=RED,s=.6,sz=44,u=inn(t,q,.8))
# 35: Trần Khắc Chung
def S_35(cv,t):
    a,b=AB(35)
    c=kc(t,[(a,(960,560,1.05)),(b,(960,540,1.15))])
    nen(cv,c,t,seed=35,mist=.4)
    nguoi(cv,c,'tnt',1250,905,t,s=.66,flip=True)
    def lay(PP,t_): PP.update(lean=10+4*math.sin(t_),arF=-40,faF=-40,arB=-30,faB=-40)
    dib(cv,c,'dkc',300,900,905,t,a,a+2.5,s=.64,sua=lay)
    for i in range(3): nguoi(cv,c,'q24',[1500,1650,1800][i],905,t,s=.58,flip=True,ph=i)
    truoc(cv,c,t)
    nhan(cv,'Đỗ Khắc Chung thành Trần Khắc Chung',960,170,t,sb(65,1)-.3,b,VIETC,46)
# 36: kết
def S_36(cv,t):
    a=T[66]-.3;b=E[67]+4;q=T[67]
    c=kc(t,[(a,(900,560,1.05)),(b,(1100,520,1.0))])
    nen(cv,c,t,'song',seed=36,mist=.6)
    for i in range(3): thuyen(cv,c,300+i*500+200*inn(t,a,b-a),800+(i%2)*25,t,s=.46,ngoi=[('v1',-50,'cheo'),('v2',40,'cheo')],ph=i)
    truoc(cv,c,t)
    tay(cv,960,430,t,q-.5,b+1,s=.55,o=.9)
    if not FREEZE:
        put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,150,inn(t,E[67]+.6,1))
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
S=lambda i:(T[G[i-1][0]]-.3)
SH=[(0 if i==1 else S(i),S(i+1) if i<len(G) else V.TOTAL+1,globals()[f'S_{i}']) for i in range(1,len(G)+1)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm24_full.json'))
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
    TT=T[6]
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'HAI CHỮ TRÊN CÁNH TAY','stitle24',.55)
    if not NOCAP: caps(cv,t)
V.NHAN={23:'Ô Mã Nhi – tướng nhà Nguyên',29:'Đỗ Khắc Chung – quan nhà Trần',6:'Trần Quốc Tuấn – Hưng Đạo Vương',54:'Toa Đô – tướng nhà Nguyên'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
