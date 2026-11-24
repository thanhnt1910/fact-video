# dai_tm23: Bình Lệ Nguyên 1257–1258 (lời kể bản 7, giọng Charon lần 3). Tập đầu tiên dùng nhân vật múa rối có khớp (rig.py, mảnh t23n_r_*), ngựa có khớp, voi, thuyền.
# Hình ảnh lặp lại: đoàn thuyền (mở đầu, rút lui, Thiên Mạc, Đông Bộ Đầu, kết) và tấm ván thuyền che tên.
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
V=K.setup('tm23',{7:4.0})
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
    put(cv,c,'t23_far',960+seed*60,g-120,ay=1,k=.35,o=far)
    put(cv,c,'t23_mid',960-sd*40,g+30,ay=1,k=.62,o=midv)
    suong(cv,c,t,g-260,mist,seed)
def truoc(cv,c,t,o=1):
    put(cv,c,'t23_frontL',-120,1120,ax=0,ay=1,k=1.3,s=.85,r=1.2*math.sin(t*.8),o=o)
    put(cv,c,'t23_frontR',2040,1120,ax=1,ay=1,k=1.3,s=.8,r=1.2*math.sin(t*.7+1),o=o)
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
        rg=np.random.default_rng(23);a=rg.random((34,60)).astype(np.float32)
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
VIETC=(.20,.31,.43);MONGC=(.42,.33,.24);GOLDC=(.79,.64,.35)
# ---------- nền ----------
def nen(cv,c,t,kieu='dong',g=900,seed=0,mist=.45):
    sd=(seed*37)%7-3
    put(cv,c,'t23_far' if kieu!='nui' else 't23_nui',960+sd*50,g-120,ay=1,k=.35,o=.85)
    if kieu=='song':
        put(cv,c,'t23_mid',960-sd*40,g-170,ay=1,k=.5,o=.6)
        put(cv,c,'t23_song',960,g-270,ay=0,k=.8,s=1.0,o=.95)
    else: put(cv,c,'t23_mid',960-sd*40,g+30,ay=1,k=.62,o=.8)
    suong(cv,c,t,g-260,mist,seed)
def song(cv,c,t,y=620,o=.95):
    put(cv,c,'t23_song',960,y,ay=0,k=.85,o=o)
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
    put(cv,C0,'t23_cuon',x,y,s=s,o=o)
    if FREEZE: return
    put_screen(cv,text(tieu,28,INK,700),x,y-170*s/.62,o)
    for k,ln in enumerate(chu.split('|')): put_screen(cv,wipe(text(ln,sz,col if col is not None else RED,700),u,0,.25,seed=int(x)+k),x,y-20+k*(sz+16),o)
def nhan(cv,txt,x,y,t,t0,t1,col=None,sz=40,w=None):
    if FREEZE or not(t0<t<t1): return
    u=inn(t,t0,.35)*(1-inn(t,t1-.35,.35));tx=text(txt,sz,col if col is not None else INK,700)
    put_screen(cv,band(w or tx.shape[1]+50,tx.shape[0]+26,PAPER,.86,18),x,y,u);put_screen(cv,tx,x,y,u)
# =================== các cảnh ===================
G=[(1,3),(4,5),(6,6),(7,7),(8,9),(10,11),(12,13),(14,15),(16,17),(18,20),(21,22),(23,23),(24,25),(26,27),(28,29),(30,31),(32,32),(33,33),(34,36),(37,38),(39,39),(40,41),(42,43),(44,45),(46,47),(48,49),(50,50),(51,53),(54,55),(56,56),(57,57)]
def AB(i): a,b=G[i-1];return T[a]-.3,E[b]+.3
# 1: mở đầu, trận rút, Lê Phụ Trần một mình một ngựa
def S_1(cv,t):
    a,b=0,E[3]+.3;q=T[3]
    c=kc(t,[(a,(900,560,1.05)),(q,(820,540,1.18)),(b,(760,520,1.3))])
    nen(cv,c,t,seed=1,mist=.55)
    for i,key in enumerate(['lv1','lv3','lv2','lv1']): dib(cv,c,key,560-i*120,-300-i*160,905+(i%2)*14,t,a+.2+i*.15,b,s=.55,vk=['giao','dao','no','giao'][i],ph=i,chay=1.2)
    for i,key in enumerate(['lm2','lm3','lm2']): dib(cv,c,key,2300+i*160,1450+i*150,905+(i%2)*12,t,a,b,s=.58,vk=['daocong','moc','daocong'][i],ph=i)
    ngua(cv,c,'nau','lm1',2600,1700,900,t,a+.4,b,s=.6,vk='cung')
    ngua(cv,c,'trang','lpt',600,1050,900,t,a+.3,q+1.5,s=.66,vk='giao',flip=False)
    ten(cv,c,t,a,b,[(1700,600),(1900,620)],[(500,840),(900,860)],n=12,h=160)
    truoc(cv,c,t)
    if not FREEZE and t>q+.2: ink_wash(cv,.18*inn(t,q,1))
# 2: câu hỏi, cận Lê Phụ Trần
def S_2(cv,t):
    a,b=AB(2);q=T[5]
    c=kc(t,[(a,(1000,520,1.3)),(b,(1000,540,1.15))])
    nen(cv,c,t,seed=2,mist=.6)
    ngua(cv,c,'trang','lpt',960,960,900,t,a,b,s=.7,vk='giao')
    for i in range(3): dib(cv,c,['lv1','lv2','lv3'][i],1300+i*120,2200+i*120,905,t,a+i*.3,b,s=.55,vk=['giao','no','dao'][i],ph=i)
    dib(cv,c,'lm2',-300,250,905,t,a,b,s=.56,vk='daocong')
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3)
    nhan(cv,'nhụt chí?',700,330,t,a+.5,q-.1,RED,48);nhan(cv,'hay đã nhìn thấy điều người khác chưa thấy?',960,330,t,q+.1,b,INK,40)
# 3: đoàn thuyền, mười hai ngày
def S_3(cv,t):
    a,b=AB(3)
    c=kc(t,[(a,(700,560,1.05)),(b,(1100,540,1.0))])
    nen(cv,c,t,'song',seed=3)
    for i in range(4): thuyen(cv,c,300+i*420+60*inn(t,a,b-a),780+(i%2)*40,t,s=.5,lon=(i==2),ngoi=[('lv1',-60,'cheo'),('lv2',40,'cheo')] if i!=2 else [],ph=i)
    truoc(cv,c,t)
    seal(cv,'s12ngay',1560,260,a+.6,t,s=.8,r=4)
# 4: mốc năm, tiêu đề
def S_4(cv,t):
    a,b=AB(4)
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,540,1.06))])
    nen(cv,c,t,seed=4)
    for i in range(3): dib(cv,c,'dan' if i!=1 else 'quan1',-300-i*200,600+i*200,905,t,a+i*.4,b,s=.5,ph=i)
    truoc(cv,c,t)
    seal(cv,'s1257',1560,300,T[7]+.5,t,s=.8,r=4)
# 5: đế quốc Mông Cổ, Đại Lý
def S_5(cv,t):
    a,b=AB(5);q=T[9]
    c=kc(t,[(a,(1300,540,1.05)),(b,(800,560,1.0))])
    nen(cv,c,t,'nui',seed=5)
    for i in range(4): ngua(cv,c,['nau','den','nau','den'][i],'lm1',2400+i*260,200+i*260,900+(i%2)*16,t,a+i*.2,b,s=.5,vk='cung',ph=i)
    co(cv,c,'t23_spr_co',1500,880,t,s=.6)
    truoc(cv,c,t)
    nhan(cv,'đế quốc Mông Cổ',960,180,t,a+.4,q-.2,MONGC,46);nhan(cv,'Đại Lý (Vân Nam) · sát biên giới Đại Việt',960,180,t,q+.1,b,INK,40)
# 6: Ngột Lương Hợp Thai sai sứ; im lặng
def S_6(cv,t):
    a,b=AB(6);q=T[11]
    c=kc(t,[(a,(700,560,1.1)),(q,(1100,560,1.0)),(b,(1400,560,1.08))])
    nen(cv,c,t,seed=6)
    nguoi(cv,c,'nlh',520,905,t,s=.62,vk='daocong')
    ngua(cv,c,'nau','lm3',700,1450,900,t,a+.6,q,s=.5)
    for i in range(2): dib(cv,c,'lv1',1950+i*120,1800+i*120,905,t,q,b,s=.5,vk='giao',ph=i,flip=True)
    co(cv,c,'t23_spr_co',420,880,t,s=.55)
    truoc(cv,c,t)
    nhan(cv,'Ngột Lương Hợp Thai sai sứ đòi nhà Trần đầu hàng',960,170,t,a+.4,q-.2,MONGC,38);nhan(cv,'không trả lời',1450,330,t,q+.2,b,RED,48)
# 7: điều quân lên biên giới; Lê Phụ Trần
def S_7(cv,t):
    a,b=AB(7);q=T[13]
    c=kc(t,[(a,(1200,560,1.05)),(b,(800,540,1.12))])
    nen(cv,c,t,seed=7)
    for i in range(5): dib(cv,c,['lv1','lv2','lv3','lv1','lv2'][i],2300+i*170,700+i*170,905+(i%2)*12,t,a+i*.2,q+1,s=.52,vk=['giao','no','dao','giao','no'][i],ph=i)
    nguoi(cv,c,'ttt',300,905,t,s=.62,vk='dao')
    if t>q-.5: ngua(cv,c,'trang','lpt',-300,600,900,t,q-.3,q+2,s=.64,vk='giao')
    co(cv,c,'t23_spr_coV',180,880,t,s=.5)
    truoc(cv,c,t)
    nhan(cv,'Trần Thái Tông · quân lên giữ biên giới',960,170,t,a+.3,q-.2,VIETC,38)
# 8: quân Mông Cổ tới Bình Lệ Nguyên; vua đem quân ra chặn
def S_8(cv,t):
    a,b=AB(8);q=T[15]
    c=kc(t,[(a,(1300,560,1.0)),(b,(900,560,1.1))])
    nen(cv,c,t,seed=8)
    for i in range(4): ngua(cv,c,['nau','den','den','nau'][i],'lm1',2500+i*200,1250+i*190,895+(i%2)*14,t,a+i*.2,q,s=.52,vk='cung',ph=i)
    for i in range(3): dib(cv,c,['lv1','lv3','lv1'][i],-400-i*150,350+i*150,905,t,q,b,s=.55,vk=['giao','dao','giao'][i],ph=i)
    nguoi(cv,c,'ttt',560,905,t,s=.62,vk='dao') if t>q else None
    truoc(cv,c,t)
    nhan(cv,'Bình Lệ Nguyên, vùng Vĩnh Phúc bây giờ',960,170,t,a+.3,q-.2,INK,40)
# 9: hàng voi bên sông; cuộn sử nhà Nguyên
def S_9(cv,t):
    a,b=AB(9);q=T[17]
    c=kc(t,[(a,(900,560,1.05)),(b,(1000,540,1.0))])
    nen(cv,c,t,'song',seed=9)
    for i in range(3): voi(cv,c,420+i*420,870,t,s=.55,ph=i)
    for i in range(4): dib(cv,c,['lv1','lv2','lv1','lv3'][i],-200+i*120,300+i*430,925,t,a+i*.2,b,s=.5,vk=['giao','no','giao','dao'][i],ph=i)
    truoc(cv,c,t)
    if not FREEZE and t>q: ink_wash(cv,.35*inn(t,q,.5));cuon(cv,960,470,t,'SỬ NHÀ NGUYÊN','voi chiến|rất đông quân bộ',col=MONGC,u=inn(t,q+.2,.8))
# 10: ba cánh vượt sông, cái bẫy cướp thuyền
def S_10(cv,t):
    a,b=AB(10);q=T[19];r=T[20]
    c=kc(t,[(a,(960,540,1.0)),(b,(800,560,1.12))])
    nen(cv,c,t,'song',seed=10)
    for i in range(3): thuyen(cv,c,300+i*300,790,t,s=.5,ph=i)
    for i in range(3):
        y=640+i*70;dib(cv,c,['lm2','lm3','lm2'][i],2400,1300-i*80,y,t,a+.3+i*.5,q+1,s=.42,vk=['daocong','moc','daocong'][i],ph=i)
        if not FREEZE: stroke(cv,c,[(2000,y-60),(1400-i*80,y-60)],inn(t,a+.3+i*.5,1.2),wid=7,col=MONGC,o=.75,head=True)
    nguoi(cv,c,'nlh',1700,600,t,s=.42,vk='daocong',flip=True)
    truoc(cv,c,t)
    nhan(cv,'Ngột Lương Hợp Thai chia quân làm ba cánh',960,160,t,a+.3,q-.2,MONGC,40)
    if not FREEZE and t>q: put_screen(cv,band(560,110,PAPER,.88,18),560,330,inn(t,q,.3));put_screen(cv,text('cánh đi đầu: cướp thuyền',42,RED,700),560,330,inn(t,q,.3))
    nhan(cv,'mất thuyền = hết đường',1400,330,t,r,b,RED,44)
# 11: trận đánh; vua xông vào làn tên; quân bị dồn
def S_11(cv,t):
    a,b=AB(11);q=T[22]
    hit=a+.8;sh=(4*math.sin(t*37)*(1-inn(t,hit+.3,.6))) if hit<t<hit+.9 and not FREEZE else 0
    c=kc(t,[(a,(1000,540,1.1)),(b,(800,560,1.0))],sh)
    nen(cv,c,t,seed=11)
    dib(cv,c,'ttt',500,800,905,t,a+.2,q,s=.64,vk='dao')
    for i in range(3): dib(cv,c,['lv1','lv3','lv2'][i],300-i*140,420-i*140,905+(i%2)*14,t,a,q,s=.55,vk=['giao','dao','no'][i],ph=i)
    if t>q:
        for i in range(3): dib(cv,c,['lv1','lv3','lv2'][i],420-i*140,-200-i*140,905+(i%2)*14,t,q,b,s=.55,vk=['giao','dao','no'][i],ph=i)
    for i in range(4): dib(cv,c,['lm2','lm3','lm2','lm3'][i],2200+i*150,1200+i*150,905,t,a,b,s=.56,vk=['daocong','moc','daocong','moc'][i],ph=i)
    ten(cv,c,t,a,b,[(1600,600),(1800,620)],[(400,840),(900,860)],n=14,h=150)
    truoc(cv,c,t)
    nhan(cv,'thế trận nghiêng về phía quân Mông Cổ',960,170,t,q+.2,b,MONGC,40)
# 12: chỉ còn Lê Phụ Trần
def S_12(cv,t):
    a,b=AB(12)
    c=kc(t,[(a,(960,540,1.2)),(b,(1000,520,1.35))])
    nen(cv,c,t,seed=12,mist=.7)
    ngua(cv,c,'trang','lpt',700,1150,900,t,a,b,s=.66,vk='giao')
    for i in range(4): dib(cv,c,['lm2','lm3','lm2','lm3'][i],[300,1600,1800,150][i],[500,1400,1700,350][i],905+(i%2)*12,t,a,b,s=.56,vk=['daocong','moc','daocong','moc'][i],ph=i,flip=[False,True,True,False][i])
    ten(cv,c,t,a,b,[(1700,560),(200,560)],[(1000,820),(900,830)],n=10,h=140)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.2)
    nhan(cv,'Lê Phụ Trần',960,170,t,a+.3,b,RED,52)
# 13: lời can, dốc vốn một ván
def S_13(cv,t):
    a,b=AB(13);q=T[25]
    c=kc(t,[(a,(960,560,1.12)),(b,(960,540,1.05))])
    nen(cv,c,t,seed=13,mist=.6)
    nguoi(cv,c,'ttt',820,905,t,s=.64,vk='dao')
    nguoi(cv,c,'lv3',560,905,t,s=.6,vk='dao',ph=1)
    def can(PP,t_): PP.update(arF=-60+8*math.sin(t_*2),faF=-30)
    dib(cv,c,'lpt',1500,1100,905,t,a+.2,a+2,s=.64,sua=can,flip=True)
    for i in range(2): dib(cv,c,'lv1',-300-i*200,250+i*100,905,t,a,b,s=.52,vk='giao',ph=i)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.25)
    nhan(cv,'đánh như vậy là dốc hết vốn vào một ván',960,170,t,a+.6,q-.2,RED,40);nhan(cv,'thua thì mất cả vua lẫn đạo quân',960,170,t,q+.2,b,INK,40)
# 14: rút xuống thuyền; tấm ván thuyền che tên
def S_14(cv,t):
    a,b=AB(14);q=T[27]
    c=kc(t,[(a,(800,560,1.0)),(q,(900,560,1.12)),(b,(860,540,1.22))])
    nen(cv,c,t,'song',seed=14)
    for i in range(2): thuyen(cv,c,300+i*360-200*inn(t,q,b-q),930,t,s=.5,ngoi=[('lv1',-60,'cheo'),('lv2',40,'cheo')],ph=i)
    thuyen(cv,c,1000-150*inn(t,q,b-q),930,t,s=.55,ngoi=[('ttt',-30,None),('lv1',60,'cheo')],ph=3)
    def che(PP,t_): PP.update(arF=-120,faF=-20,giuong=0)
    dib(cv,c,'lpt',1450,1150,905,t,q,b,s=.62,vk='van',sua=che,flip=True) if t>q else dib(cv,c,'lv1',1450,1150,905,t,a,q,s=.55,vk='giao')
    for i in range(3): dib(cv,c,['lm2','lm3','lm2'][i],2300+i*140,1650+i*140,905,t,a,b,s=.55,vk=['daocong','moc','daocong'][i],ph=i)
    ten(cv,c,t,q,b,[(1800,560),(1950,580)],[(1100,700),(1200,720)],n=12,h=120)
    truoc(cv,c,t)
    nhan(cv,'rút về sông Lô',960,170,t,a+.3,q-.2,VIETC,44)
# 15: sử nhà Nguyên; Triệt Triệt Đô đánh ngay
def S_15(cv,t):
    a,b=AB(15);q=T[29]
    c=kc(t,[(a,(1100,540,1.05)),(b,(900,560,1.12))])
    nen(cv,c,t,'song',seed=15)
    thuyen(cv,c,500,790,t,s=.5,ph=1);thuyen(cv,c,900,795,t,s=.5,ph=2)
    dib(cv,c,'ttd',2000,1300,905,t,q-.2,b,s=.62,vk='daocong',chay=1.3)
    for i in range(3): dib(cv,c,['lm2','lm3','lm2'][i],2250+i*150,1500+i*150,905,t,q,b,s=.55,vk=['daocong','moc','daocong'][i],ph=i,chay=1.3)
    for i in range(2): dib(cv,c,'lv1',300+i*120,-200+i*120,905,t,q+.6,b,s=.52,vk='giao',ph=i,chay=1.2)
    truoc(cv,c,t)
    if not FREEZE and t<q+.3: ink_wash(cv,.35);cuon(cv,960,470,t,'SỬ NHÀ NGUYÊN','Triệt Triệt Đô|trái lệnh',col=MONGC,u=inn(t,a+.6,.8))
    nhan(cv,'Triệt Triệt Đô · đánh ngay, không chờ cướp thuyền',960,170,t,q+.2,b,MONGC,38)
# 16: thoát bằng thuyền; Ngột Lương Hợp Thai nổi giận
def S_16(cv,t):
    a,b=AB(16);q=T[31]
    c=kc(t,[(a,(900,560,1.0)),(b,(1300,560,1.1))])
    nen(cv,c,t,'song',seed=16)
    for i in range(3): thuyen(cv,c,600+i*330-500*inn(t,a,q-a),930+(i%2)*10,t,s=.5,ngoi=[('lv1',-60,'cheo'),('lv3',40,'cheo')],ph=i)
    if t>q-.3:
        def gian(PP,t_): PP.update(arF=-100+20*math.sin(t_*4),faF=-20)
        dib(cv,c,'nlh',1900,1600,905,t,q-.3,q+1.2,s=.62,vk='daocong',sua=gian,flip=True)
        ten_o=1-inn(t,q+1.5,1.5)
        nguoi(cv,c,'ttd',1250,905,t,s=.6,o=max(.05,ten_o))
        dib(cv,c,'lm2',2300,1900,905,t,q,b,s=.55,vk='daocong',flip=True)
    truoc(cv,c,t)
    nhan(cv,'tuy thua to vẫn kịp xuống thuyền mà thoát',960,170,t,a+.3,q-.2,VIETC,38);nhan(cv,'Triệt Triệt Đô sợ tội, uống thuốc độc',960,170,t,q+.2,b,MONGC,38)
# 17: hai bộ sử cùng chép còn thuyền
def S_17(cv,t):
    a,b=AB(17)
    c=kc(t,[(a,(960,560,1.04)),(b,(960,560,1.0))])
    nen(cv,c,t,'song',seed=17,mist=.6)
    for i in range(3): thuyen(cv,c,200+i*500+40*math.sin(t*.3+i),810,t,s=.45,ngoi=[('lv1',-50,'cheo')],ph=i)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3)
    cuon(cv,560,470,t,'SỬ NƯỚC TA','rút được|còn thuyền',col=VIETC,s=.6,sz=44)
    cuon(cv,1360,470,t,'SỬ NHÀ NGUYÊN','xuống thuyền|mà thoát',col=MONGC,s=.6,sz=44,u=inn(t,a+.6,.8))
# 18: bỏ trống Thăng Long
def S_18(cv,t):
    a,b=AB(18)
    c=kc(t,[(a,(1200,540,1.05)),(b,(900,560,1.0))])
    nen(cv,c,t,seed=18)
    put(cv,c,'t23_thanh',1350,880,ay=1,s=.62,k=.85)
    for i in range(3): ngua(cv,c,['nau','den','nau'][i],'lm1',2500+i*200,1400+i*160,900+(i%2)*12,t,a+i*.3,b,s=.5,vk='cung',ph=i)
    for i in range(2): thuyen(cv,c,500-i*300-300*inn(t,a,b-a),960,t,s=.45,ngoi=[('lv1',-50,'cheo')],ph=i)
    co(cv,c,'t23_spr_co',1600,860,t,s=.5)
    for i in range(2): smoke(cv,c,1200+i*300,560,t+i,.9)
    truoc(cv,c,t)
    nhan(cv,'vua lui xuống sông Thiên Mạc · bỏ trống Thăng Long',960,170,t,a+.3,b,INK,38)
# 19: thuyền nhỏ; Trần Nhật Hiệu viết hai chữ "nhập Tống"
def S_19(cv,t):
    a,b=AB(19);q=T[35];r=T[36]
    c=kc(t,[(a,(900,560,1.05)),(q,(1100,540,1.25)),(b,(1050,540,1.18))])
    nen(cv,c,t,'song',seed=19,mist=.65)
    thuyen(cv,c,700+250*inn(t,a,q-a-.5),940,t,s=.55,ngoi=[('ttt',-20,None),('lv1',70,'cheo')])
    thuyen(cv,c,1350,805,t,s=.55,ngoi=[('tnh',-40,None)],flip=True,ph=2)
    thuyen(cv,c,300,820,t,s=.45,ngoi=[('lv2',0,'cheo')],ph=4)
    truoc(cv,c,t)
    if not FREEZE and t>q+.5:
        tx=text('nhập Tống',62,(.3,.36,.42),700);put_screen(cv,wipe(tx,inn(t,q+.8,1.6),0,.3,seed=34),1250,600,.85*(1-inn(t,b-.8,.6)))
    nhan(cv,'Trần Nhật Hiệu · em vua, nắm việc quân',960,170,t,a+.4,q,INK,38);nhan(cv,'chạy sang nước Tống',960,170,t,r,b,RED,44)
# 20: Trần Thủ Độ
def S_20(cv,t):
    a,b=AB(20);q=T[38]
    c=kc(t,[(a,(800,560,1.05)),(b,(1000,540,1.2))])
    nen(cv,c,t,'song',seed=20,mist=.6)
    thuyen(cv,c,500+300*inn(t,a,q-a),940,t,s=.55,ngoi=[('ttt',-20,None),('lv1',70,'cheo')])
    thuyen(cv,c,1350,805,t,s=.58,ngoi=[('tth',-30,None)],flip=True,ph=2)
    thuyen(cv,c,1900-100*inn(t,a,b-a),965,t,s=.45,ngoi=[('lv3',0,'cheo')],ph=4,flip=True)
    truoc(cv,c,t)
    if not FREEZE and t>q:
        ink_wash(cv,.3*inn(t,q,.5))
        big(cv,'ĐẦU THẦN CHƯA RƠI XUỐNG ĐẤT',t,q+.1,b,RED,330,64,seed=38)
    nhan(cv,'Trần Thủ Độ · người đứng đầu triều đình',960,170,t,a+.4,q-.2,INK,38)
# 21: Ngô Sĩ Liên
def S_21(cv,t):
    a,b=AB(21)
    c=kc(t,[(a,(960,560,1.0)),(b,(1040,540,1.06))])
    nen(cv,c,t,'song',seed=21,mist=.6)
    for i in range(3): thuyen(cv,c,300+i*600+30*math.sin(t*.4+i),815,t,s=.42,ngoi=[('lv1',0,'cheo')],ph=i)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3)
    cuon(cv,960,470,t,'NGÔ SĨ LIÊN, HƠN 200 NĂM SAU','khiếp sợ|không có kế chống giữ',col=INK,s=.65,sz=44)
# 22: đạo quân vẫn còn
def S_22(cv,t):
    a,b=AB(22);q=T[41]
    c=kc(t,[(a,(1100,540,1.15)),(b,(900,560,1.0))])
    nen(cv,c,t,'song',seed=22)
    for i in range(5): thuyen(cv,c,150+i*380,760+(i%2)*45,t,s=.46,lon=(i==2),ngoi=[('lv1',-50,'cheo'),('lv3',40,'cheo')] if i!=2 else [],ph=i)
    truoc(cv,c,t)
    if not FREEZE and t>q:
        n=int(40*inn(t,q,b-q-.5));put_screen(cv,band(440,100,PAPER,.88,16),1500,300,inn(t,q,.3));put_screen(cv,text('đạo quân vẫn còn',42,RED,700),1500,300,inn(t,q,.3))
    nhan(cv,'kinh thành đã mất · đoàn thuyền vẫn còn',960,170,t,a+.3,q-.2,VIETC,40)
# 23: ngày 24 tháng Chạp, ngược sông; vua và thái tử
def S_23(cv,t):
    a,b=AB(23);q=T[43]
    c=kc(t,[(a,(700,560,1.0)),(b,(1100,540,1.12))])
    nen(cv,c,t,'song',seed=23)
    x0=300+600*inn(t,a,b-a)
    thuyen(cv,c,x0+300,765,t,s=.62,lon=True,ngoi=[('ttt',-300,'dao'),('tho',-225,None)])
    for i in range(3): thuyen(cv,c,x0-200-i*330,810+(i%2)*14,t,s=.46,ngoi=[('lv1',-50,'cheo'),('lv2',40,'cheo')],ph=i)
    co(cv,c,'t23_spr_coV',x0+560,700,t,s=.4)
    truoc(cv,c,t)
    seal(cv,'s12ngay',1580,260,a+.5,t,s=.75,r=4)
    nhan(cv,'thái tử Trần Hoảng, mười bảy tuổi',960,170,t,q+.2,b,VIETC,40)
# 24: Đông Bộ Đầu
def S_24(cv,t):
    a,b=AB(24);q=T[45]
    hit=q+.3;sh=(5*math.sin(t*37)*(1-inn(t,hit+.3,.6))) if hit<t<hit+.9 and not FREEZE else 0
    c=kc(t,[(a,(1000,540,1.0)),(b,(1200,560,1.1))],sh)
    nen(cv,c,t,'song',seed=24)
    put(cv,c,'t23_trai',1500,700,ay=1,s=.45,k=.85,o=.9);co(cv,c,'t23_spr_co',1750,690,t,s=.45)
    for i in range(2): thuyen(cv,c,200+i*360+500*inn(t,a,q-a),930+(i%2)*14,t,s=.5,lon=(i==0),ngoi=[('lv1',-50,'cheo'),('lv3',40,'dao')] if i else [('ttt',-300,'dao')],ph=i)
    if t>q:
        for i in range(4): dib(cv,c,['lm2','lm3','lm2','lm3'][i],1300+i*130,2400+i*130,905,t,q+.3+i*.1,b,s=.55,vk=['daocong','moc','daocong','moc'][i],ph=i,chay=1.3)
        for i in range(2): dib(cv,c,['lv1','lv3'][i],900+i*120,1500+i*120,905,t,q+.2,b,s=.55,vk=['giao','dao'][i],ph=i,chay=1.2)
    truoc(cv,c,t)
    nhan(cv,'Đông Bộ Đầu · gần cầu Long Biên bây giờ',960,170,t,a+.3,q-.2,INK,40);nhan(cv,'quân Mông Cổ bị phá tan',960,170,t,q+.2,b,RED,44)
# 25: rút về Vân Nam; Hà Bổng đánh úp; giặc Phật
def S_25(cv,t):
    a,b=AB(25);q=T[47]
    c=kc(t,[(a,(900,560,1.05)),(b,(1200,560,1.0))])
    nen(cv,c,t,'nui',seed=25)
    for i in range(3): ngua(cv,c,['nau','den','nau'][i],'lm1',400+i*200,2200+i*200,900+(i%2)*14,t,a+i*.2,b,s=.48,vk='cung',ph=i)
    for i in range(3): dib(cv,c,['dan','lv1','dan'][i],-300-i*150,700-i*150,905,t,a+.8+i*.2,b,s=.5,vk=[None,'giao',None][i],ph=i)
    truoc(cv,c,t)
    nhan(cv,'trại Quy Hóa · Hà Bổng đánh úp',960,170,t,a+.3,q-.2,VIETC,40);nhan(cv,'người bấy giờ gọi là "giặc Phật"',960,170,t,q+.2,b,INK,40)
# 26: hai cái kết
def S_26(cv,t):
    a,b=AB(26)
    c=kc(t,[(a,(960,560,1.04)),(b,(960,560,1.0))])
    nen(cv,c,t,'song',seed=26,mist=.6)
    for i in range(3): thuyen(cv,c,300+i*600+30*math.sin(t*.4+i),815,t,s=.42,ngoi=[('lv1',0,'cheo')],ph=i)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3)
    cuon(cv,560,470,t,'SỬ NƯỚC TA','đánh tan ở|Đông Bộ Đầu',col=VIETC,s=.6,sz=44)
    cuon(cv,1360,470,t,'SỬ NHÀ NGUYÊN','vua Trần|xin quy phục',col=MONGC,s=.6,sz=44,u=inn(t,a+.8,.8))
# 27: Tết, trăm quan vào chầu
def S_27(cv,t):
    a,b=AB(27)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,540,1.12))])
    put(cv,c,'t23_cung',960,1000,ay=1,s=.9,k=.9)
    nguoi(cv,c,'ttt',960,720,t,s=.7,vk=None)
    for i in range(4): dib(cv,c,['quan1','tth','quan1','quan1'][i],-200-i*200,560-i*130,905,t,a+i*.3,b,s=.55,ph=i)
    for i in range(3): dib(cv,c,'quan1',2200+i*200,1380+i*130,905,t,a+i*.3,b,s=.55,ph=i+4)
    truoc(cv,c,t)
    nhan(cv,'Tết năm 1258 · trăm quan vào chầu',960,170,t,a+.3,b,INK,40)
# 28: phần thưởng
def S_28(cv,t):
    a,b=AB(28);q=T[52];r=T[53]
    c=kc(t,[(a,(960,560,1.05)),(b,(960,540,1.14))])
    nen(cv,c,t,seed=28,mist=.4)
    put(cv,c,'t23_mam',1300,880,ay=1,s=.5,k=.95)
    nguoi(cv,c,'ttt',1150,905,t,s=.66,flip=True)
    def lay(PP,t_): PP.update(lean=8+4*math.sin(t_),arF=-40,faF=-40,arB=-30,faB=-40)
    dib(cv,c,'lpt',300,800,905,t,a,a+2.5,s=.64,sua=lay)
    for i in range(2): dib(cv,c,'quan1',2200+i*150,1600+i*130,905,t,a+.3+i*.3,b,s=.52,ph=i)
    truoc(cv,c,t)
    nhan(cv,'Ngự sử đại phu · một chức quan lớn',960,170,t,a+.3,q-.2,VIETC,40);nhan(cv,'"không có ông thì đâu có ngày hôm nay"',960,170,t,q+.1,r-.2,RED,40)
    nhan(cv,'công chúa Chiêu Thánh, tức Lý Chiêu Hoàng',960,170,t,r+.1,b,INK,40)
# 29: đi sứ, ba năm một lần
def S_29(cv,t):
    a,b=AB(29);q=T[55]
    c=kc(t,[(a,(800,560,1.0)),(b,(1200,560,1.08))])
    nen(cv,c,t,'nui',seed=29)
    if t<q: ngua(cv,c,'den','lm3',2300,1400,900,t,a,q,s=.5,flip=True)
    ngua(cv,c,'trang','lpt',150,1300,900,t,q-.6,b,s=.56)
    for i in range(2): dib(cv,c,'lv1',-100-i*150,1050-i*150,905,t,q-.6,b,s=.5,vk='giao',ph=i)
    truoc(cv,c,t)
    seal(cv,'s3nam',1560,280,q+1.0,t,s=.8,r=4)
    nhan(cv,'sứ nhà Nguyên đòi cống nộp mỗi năm',960,170,t,a+.3,q-.2,MONGC,40);nhan(cv,'Lê Phụ Trần đi sứ',960,170,t,q+.2,b,VIETC,44)
# 30: tấm ván và lời nói
def S_30(cv,t):
    a,b=AB(30)
    c=kc(t,[(a,(960,560,1.1)),(b,(960,540,1.0))])
    nen(cv,c,t,'song',seed=30,mist=.6)
    def che(PP,t_): PP.update(arF=-120,faF=-20)
    nguoi(cv,c,'lpt',700,905,t,s=.64,vk='van',PP=rig.dung(t)|{'arF':-120,'faF':-20},o=.45)
    def noi(PP,t_): PP.update(arF=-40+10*math.sin(t_*3),faF=-50)
    dib(cv,c,'lpt',1700,1300,905,t,a,a+2,s=.64,sua=noi,flip=True)
    dib(cv,c,'lv1',-200,300,905,t,a,b,s=.52,vk='giao')
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.2)
    nhan(cv,'giữ nước bằng lời nói',960,170,t,a+.4,b,RED,46)
# 31: kết
def S_31(cv,t):
    a=T[57]-.3;b=E[57]+4
    c=kc(t,[(a,(900,560,1.05)),(b,(1100,520,1.0))])
    nen(cv,c,t,'song',seed=31,mist=.65)
    x0=200+500*inn(t,a,b-a)
    thuyen(cv,c,x0+300,765,t,s=.6,lon=True,ngoi=[('lpt',-300,'giao')])
    for i in range(3): thuyen(cv,c,x0-200-i*330,815,t,s=.45,ngoi=[('lv1',-50,'cheo')],ph=i)
    truoc(cv,c,t)
    if not FREEZE:
        tx=text('Lê Phụ Trần và đoàn thuyền, năm 1257',50,INK,700);put_screen(cv,wipe(tx,inn(t,a+1.2,1.4),0,.3,seed=13),W/2,150)
        put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,220,inn(t,E[57]+.6,1))
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
S=lambda i:(T[G[i-1][0]]-.3)
SH=[(0 if i==1 else S(i),S(i+1) if i<len(G) else V.TOTAL+1,globals()[f'S_{i}']) for i in range(1,len(G)+1)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm23_full.json'))
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
    TT=T[7]
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'BÌNH LỆ NGUYÊN','stitle23',.55)
    if not NOCAP: caps(cv,t)
V.NHAN={10:'Ngột Lương Hợp Thai – tướng Mông Cổ',13:'Lê Phụ Trần – tướng nhà Trần',28:'Triệt Triệt Đô – tướng Mông Cổ'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
