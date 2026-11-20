# Bản dài tm13 (bản 5): Hai Bà Trưng, khung trống đồng → ngựa mẫu. Dựng theo chuẩn chi tiết 20/11 và các cách dựng mới:
# hình ảnh lặp lại = trống đồng và vòng tiếng gọi lan ra (mở đầu, khởi nghĩa, 65 thành, Lê Văn Hưu, kết); mở đầu giọt mực loang;
# quét mực khi chuyển từ yên sang chiến; ba cuộn sử chia màn hình; cận cảnh mặt trống; trống hóa ngựa ở đoạn 19.
# Quy ước màu: quân hai bà đỏ son, quân nhà Hán xanh chàm đội mũ trụ.
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
V=K.setup('tm13',{4:4.0})
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
    put(cv,c,'t13_far',960+seed*60,g-120,ay=1,k=.35,o=far)
    put(cv,c,'t13_mid',960-seed*40,g+30,ay=1,k=.62,o=midv)
    suong(cv,c,t,g-260,mist,seed)
def truoc(cv,c,t,o=1):
    put(cv,c,'t13_frontL',-120,1120,ax=0,ay=1,k=1.3,s=.85,r=1.2*math.sin(t*.8),o=o)
    put(cv,c,'t13_frontR',2040,1120,ax=1,ay=1,k=1.3,s=.8,r=1.2*math.sin(t*.7+1),o=o)
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
        rg=np.random.default_rng(13);a=rg.random((34,60)).astype(np.float32)
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
def trong(cv,c,x,y,t,s=1.0,o=1.0,k=1.0):
    put(cv,c,'t13_spr_trong',x,y,s=s*(1+.02*math.sin(t*1.3)),ay=1,o=o,k=k,scale_px=1.5)
# ---- 1: giọt mực rơi, loang thành con ngựa đồng
def S_1(cv,t):
    a,b=0,E[1]+.3;td=.95
    sc=PAP.copy()
    c=kc(t,[(a,(960,600,1.0)),(b,(960,560,1.14))])
    ngoai(sc,c,t,g=900,seed=1,mist=.4)
    put(sc,c,'t13x_ngua',960,560,s=1.1)
    for i in range(3): di(sc,c,'t13_spr_quan',-200-i*160,880,500+i*120,880,t,a+.3+i*.3,b+2,s=.55,bob=2,f=3.4,ph=i)
    di(sc,c,'t13_spr_1han',2200,880,1500,880,t,a,b+2,s=.6,bob=2,f=3.2,lat=True)
    put(sc,c,'mist',960+40*math.sin(t*.5),700,s=2.2,o=.35,k=1.1)
    truoc(sc,c,t)
    if FREEZE: cv[:]=sc;return
    if t<td:
        y=-40+(540+40)*(t/td)**2
        m=loang(960,y,22,6);cv[:]=cv*(1-m)+np.array(INK,np.float32)*m
    else:
        u=inn(t,td,1.6);r=30+u*1300
        m=loang(960,540,r,60);rim=np.clip(loang(960,540,r,60)-loang(960,540,r-70,60),0,1)
        cv[:]=cv*(1-m)+sc*m;cv[:]=cv*(1-rim*.75)+np.array(INK,np.float32)*rim*.75
    big(cv,'CON NGỰA ĐÚC TỪ TRỐNG ĐỒNG',t,1.6,b,RED,110,80,seed=1)
# ---- 2: Mã Viện nấu trống, đúc ngựa (lóe nhanh, chưa kể chi tiết)
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3;q=sb(2,1)
    c=kc(t,[(a,(900,560,1.0)),(b,(1100,520,1.16))])
    ngoai(cv,c,t,g=880,seed=2,mist=.3,far=.7,midv=.7)
    di(cv,c,'t13_spr_mavien',-200,870,420,870,t,a,q,s=.75,bob=4,f=6)
    for k in range(6): flick(cv,c,840+k*60,870-abs(k-2.5)*8,t+k,1.0)
    put(cv,c,'mist',960,800,s=1.4,o=.25+.1*math.sin(t*3),k=1.0)
    smoke(cv,c,920,700,t,1.4);smoke(cv,c,1010,680,t+1.3,1.2)
    for i in range(3):
        t0=q+.2+i*1.1;u=inn(t,t0,1.8)
        if t>t0: trong(cv,c,lerp(1700,960,u),lerp(880,820,u)-120*math.sin(math.pi*u),t,s=.7*(1-.5*inn(t,t0+1.6,.6)),o=1-inn(t,t0+1.7,.4))
    di(cv,c,'t13_spr_han',2600,880,1500,880,t,a,b,s=.55,bob=3,f=5,lat=True)
    if t>sb(2,2)-.8:
        put(cv,c,'t13_spr_ngua',960,860,s=.9*GS*inn(t,sb(2,2)-.8,1.2),ay=1,o=inn(t,sb(2,2)-.8,1.0),scale_px=1.5)
    truoc(cv,c,t)
    lb(cv,C0,'Mã Viện, tướng nhà Hán',960,170,t,a+.3,q-.2,col=INK,sz=44)
    lb(cv,C0,'nấu trống đồng, đúc thành ngựa',960,170,t,q+.2,b,col=RED,sz=44)
# ---- 3: trống là quyền của thủ lĩnh; cận mặt trống; câu hỏi
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3;q=sb(3,1)
    c=kc(t,[(a,(960,600,1.0)),(q,(960,520,1.22)),(b,(960,500,1.3))])
    ngoai(cv,c,t,g=900,seed=3,mist=.4)
    put(cv,c,'t13x_trongto',960,540,s=1.0)
    for i in range(2): di(cv,c,'t13_spr_1trung',-200-i*200,880,250+i*130,880,t,a+i*.4,b,s=.6,bob=2,f=3.2,ph=i)
    di(cv,c,'t13_spr_dan',2300,890,1500,890,t,a,b,s=.55,bob=2,f=3.6,lat=True)
    truoc(cv,c,t)
    if not FREEZE and t>q-.4:
        o=inn(t,q-.4,1.0)
        ink_wash(cv,.45*o)
        put(cv,C0,'t13_spr_matrong',960,470,s=.85+.04*inn(t,q,b-q),o=o,r=3*(t-q))
        vong(cv,960,470,t,q,n=3,per=1.6,rmax=600,o=.5*o,flat=1.0)
    lb(cv,C0,'trống đồng: quyền của thủ lĩnh Lạc Việt',960,170,t,a+.4,q-.3,col=INK,sz=42)
    lb(cv,C0,'vì sao được cả vùng đáp lại, rồi tắt?',960,170,t,q+.2,b,col=RED,sz=44)
# ---- 4: Trưng Trắc ở Mê Linh, chồng là Thi Sách
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3;q=sb(4,1)
    c=kc(t,[(a,(760,560,1.1)),(b,(1160,560,1.02))])
    ngoai(cv,c,t,g=880,seed=4)
    put(cv,c,'t13x_lang',960,560,s=1.1)
    put(cv,c,'t13_spr_haiba',820,880,s=.62*GS,ay=1,r=1.2*math.sin(t*1.3),scale_px=1.5)
    di(cv,c,'t13_spr_dan',-300,890,500,890,t,a,b,s=.55,bob=3,f=4)
    if t>q-.3: di(cv,c,'t13_spr_1trung',2300,880,1250,880,t,q-.3,b,s=.6,bob=3,f=4.2,lat=True)
    smoke(cv,c,1420,650,t,1.0)
    trong(cv,c,600,885,t,s=.55)
    truoc(cv,c,t)
    lb(cv,C0,'Trưng Trắc, con gái Lạc tướng Mê Linh',960,170,t,a+.4,q-.2,col=RED,sz=42)
    lb(cv,C0,'chồng là Thi Sách, người Chu Diên',960,170,t,q+.2,b,col=INK,sz=42)
# ---- 5: hơn 140 năm nhà Hán cai trị, thái thú Tô Định
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3;q=sb(5,1)
    c=kc(t,[(a,(960,520,1.15)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=5,far=.6,midv=.6)
    put(cv,c,'t13x_phu',960,630,s=1.1)
    for i in range(3): di(cv,c,'t13_spr_1han',1500+i*140,880,1550+i*140,880,t,a,b,s=.6,bob=1.5,f=1.6,ph=i,lat=True,lac=.6)
    di(cv,c,'t13_spr_trai',-500,890,500,890,t,q,b+1,s=.6,bob=2,f=3)
    di(cv,c,'t13_spr_dan',2300,890,1700,890,t,a,q+1,s=.5,bob=2,f=3.2,lat=True)
    truoc(cv,c,t)
    if not FREEZE:
        n=int(140*inn(t,a+.4,2.4));put_screen(cv,text(f'{n} năm',64,RED,700),1500,300,inn(t,a+.3,.4)*(1-inn(t,q-.4,.4)))
    lb(cv,C0,'nhà Hán cai trị đồng bằng sông Hồng',960,170,t,a+.4,q-.2,col=INK,sz=40)
    lb(cv,C0,'thái thú Tô Định: luật nhà Hán trói buộc dân',960,170,t,q+.2,b,col=RED,sz=40)
# ---- 6: Thi Sách bị giết (tối lại, lặng)
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3;q=sb(6,1)
    c=kc(t,[(a,(1100,560,1.0)),(b,(1300,580,1.14))])
    ngoai(cv,c,t,g=880,seed=6,mist=.6)
    put(cv,c,'t13x_troi',960,560,s=1.1)
    for i in range(2): di(cv,c,'t13_spr_1han',-200-i*180,880,500+i*120,880,t,a,b,s=.6,bob=2,f=3.4,ph=i)
    di(cv,c,'t13_spr_dan',2300,890,1700,890,t,a,b,s=.5,bob=2,f=2.6,lat=True)
    if not FREEZE: ink_wash(cv,.25*inn(t,a+.5,1.5))
    if t>q:
        put(cv,c,'t13_spr_haiba',1550,880,s=.6*GS,ay=1,o=inn(t,q,.8),r=1.2*math.sin(t*1.1),scale_px=1.5)
    truoc(cv,c,t)
    lb(cv,C0,'Tô Định giết Thi Sách',960,170,t,a+.4,q-.2,col=RED,sz=46)
    lb(cv,C0,'sử chỉ chép: bà tìm cách trả thù',960,170,t,q+.2,b,col=INK,sz=42)
# ---- 7: mùa xuân năm 40, nổi dậy; Tô Định chạy (quét mực từ tối sang lửa)
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3;q=sb(7,1)
    hit=a+1.0;sh=(4*math.sin(t*37)*(1-inn(t,hit+.3,.6))) if hit<t<hit+.9 else 0
    c=kc(t,[(a,(800,560,1.04)),(b,(1250,560,1.12))],sh)
    ngoai(cv,c,t,g=880,seed=7)
    put(cv,c,'t13x_chay',960,560,s=1.1)
    for r in range(2): di(cv,c,'t13_spr_trung',-900-r*250,870+r*24,600-r*200,870+r*24,t,a+r*.3,b+1,s=.55,bob=5,f=6.4+r*.4,ph=r)
    co_bay(cv,c,'t13_spr_trungco',lerp(-100,700,inn(t,a,b-a)),880,t,1.0)
    if t>q: di(cv,c,'t13_spr_dinh',1300,880,2500,850,t,q,b+.5,s=.6,bob=6,f=9,lac=2)
    vong(cv,*c.p(520,840),t,a+.4,n=2,per=1.2,rmax=420,o=.35)
    truoc(cv,c,t)
    seal(cv,'s40',1560,320,a+.6,t,s=.8,r=4)
    lb(cv,C0,'mùa xuân năm 40: Trưng Trắc, Trưng Nhị',960,170,t,a+.3,q-.2,col=RED,sz=42)
    lb(cv,C0,'Tô Định bỏ cả quận, chạy về Nam Hải',960,170,t,q+.2,b,col=INK,sz=42)
# ---- 8: tiếng gọi lan ra: sáu mươi lăm thành (bản đồ, vòng trống lan)
def S_8(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1)
    dl,th,ng,lc=P['daila'],P['thanhhoa'],P['nghean'],P['liemchau']
    c=mcam(t,[(a,(700,700,1.25)),(q,(820,800,1.0)),(b,(900,760,.95))])
    mapbg(cv,c,u=inn(t,a-.2,1.0))
    dot(cv,c,*dl);tag(cv,c,dl[0]+24,dl[1]-6,'Mê Linh',dy=0,sz=26)
    put(cv,c,'t13_spr_trong',dl[0],dl[1]+10,s=.35,ay=1,scale_px=1.5)
    for nm,p,t0 in (('Cửu Chân',th,a+1.2),('Nhật Nam',ng,a+2.0),('Hợp Phố',lc,a+2.8)):
        if t>t0:
            dot(cv,c,*p,o=inn(t,t0,.3));tag(cv,c,p[0]+22,p[1]-6,nm,dy=0,sz=26);stroke(cv,c,[dl,p],inn(t,t0,1.0),wid=5,col=RED,o=.8)
            u=inn(t,t0,1.4);put(cv,c,'t13_spr_trungco',dl[0]+(p[0]-dl[0])*u,dl[1]+(p[1]-dl[1])*u,s=.22,ay=1,r=3*math.sin(t*3+t0))
    put(cv,c,'t13_spr_haiba',dl[0]-40,dl[1]-6,s=.3,ay=1,r=1.5*math.sin(t*1.6))
    if t>q:
        n65=int(65*inn(t,q,2.6));rg=np.random.default_rng(2)
        for i in range(65):
            p=(dl[0]+rg.random()*700-250,dl[1]-80+rg.random()*600)
            if i<n65: dot(cv,c,p[0],p[1],o=.85,col=RED,r=7)
        if not FREEZE: put_screen(cv,text(f'{n65} thành',70,RED,700),1500,300,inn(t,q,.4))
    lb(cv,C0,'Cửu Chân, Nhật Nam, Hợp Phố hưởng ứng',960,150,t,a+.6,q-.2,col=INK,sz=40)
def S_8v(cv,t):
    S_8(cv,t)
    if not FREEZE:
        dl=P['daila'];a=T[8]-.3;q=sb(8,1)
        c=mcam(t,[(a,(700,700,1.25)),(q,(820,800,1.0)),(E[8]+.3,(900,760,.95))])
        x,y=c.p(*dl)
        vong(cv,x,y,t,a+.3,n=3,per=1.5,rmax=700,o=.45,flat=.8)
# ---- 9: Trưng Trắc xưng vua ở Mê Linh
def S_9(cv,t):
    a,b=T[9]-.3,E[9]+.3;q=sb(9,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,520,1.15))])
    ngoai(cv,c,t,g=880,seed=9,far=.6,midv=.6)
    put(cv,c,'t13x_trieu',960,630,s=1.1)
    for i in range(3): di(cv,c,'t13_spr_1trung',-300-i*160,880,350+i*120,880,t,a+i*.4,q+1,s=.6,bob=2,f=3,ph=i)
    for i in range(2): di(cv,c,'t13_spr_dan',2300+i*200,890,1550+i*140,890,t,a+i*.5,b,s=.5,bob=2,f=3,ph=i,lat=True)
    trong(cv,c,1350,885,t,s=.6)
    vong(cv,*c.p(1350,800),t,q,n=2,per=1.6,rmax=380,o=.3)
    truoc(cv,c,t)
    lb(cv,C0,'Trưng Trắc làm vua, đóng đô ở Mê Linh',960,170,t,a+.4,q-.2,col=RED,sz=42)
    lb(cv,C0,'sau hơn 140 năm, một người của mình làm vua',960,170,t,q+.2,b,col=INK,sz=40)
# ---- 10: năm 42, Mã Viện, Phục Ba tướng quân (quét mực từ triều đình sang quân Hán)
def vien(cv,t,a,b):
    c=kc(t,[(a,(1200,560,1.05)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=10,mist=.4)
    put(cv,c,'t13x_vien',960,540,s=1.0)
    for r in range(3): di(cv,c,'t13_spr_han',2600+r*260,860+r*28,1300+r*240,860+r*28,t,a+r*.3,b+1,s=.5+.04*r,bob=3,f=5+r*.4,ph=r,lat=True)
    di(cv,c,'t13_spr_mavien',2300,870,1500,870,t,a+.3,b,s=.7,bob=4,f=6,lat=True)
    truoc(cv,c,t)
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3;q=sb(10,1)
    if t<a+1.0 and not FREEZE:
        A_=PAP.copy();S_9(A_,t);B_=PAP.copy();vien(B_,t,a,b)
        m=quet(inn(t,a-.1,1.0));cv[:]=A_*(1-m)+B_*m
    else: vien(cv,t,a,b)
    seal(cv,'s42',1560,330,a+.8,t,s=.8,r=4)
    lb(cv,C0,'năm 42, vua Hán sai Mã Viện sang',960,170,t,a+.6,q-.2,col=INK,sz=42)
    lb(cv,C0,'Phục Ba tướng quân: vị tướng dẹp sóng',960,170,t,q+.2,b,col=RED,sz=42)
# ---- 11: quân bộ qua núi rừng, thuyền lương theo bờ biển
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3;q=sb(11,1)
    c=kc(t,[(a,(900,500,1.1)),(q,(900,560,1.0)),(b,(1100,600,1.08))])
    put(cv,c,'t13_far',960,520,ay=1,k=.35,o=.8)
    river(cv,c,t,PAP,wl=660,stakes=False,cliffs=False,reeds=1,mist=.5,ridge_o=.4,
          boats=[dict(name='t13_spr_thuyen',x=lerp(2200+i*380,700+i*380,inn(t,a,b-a+2)),y=700+i*36+math.sin(t*1.6+i)*6,s=.62+.06*i,r=math.sin(t*1.2+i)*2.5) for i in range(3)])
    put(cv,c,'t13x_thuyenluong',960,600,s=1.0,o=.7)
    for r in range(2): di(cv,c,'t13_spr_han',2400+r*300,520+r*20,600+r*250,520+r*20,t,a+r*.4,b+2,s=.42,bob=3,f=5+r*.5,ph=r,k=.62,lat=True)
    truoc(cv,c,t)
    lb(cv,C0,'quân bộ qua núi rừng hiểm trở',960,170,t,a+.4,q-.2,col=INK,sz=42)
    lb(cv,C0,'thuyền chở lương theo sau: không phải vội',960,170,t,q+.2,b,col=RED,sz=42)
# ---- 12: Lãng Bạc (cảnh trọng tâm)
def S_12(cv,t):
    a,b=T[12]-.3,E[12]+.3;q=sb(12,1)
    hit=a+1.6
    sh=(6*math.sin(t*37)*(1-inn(t,hit+.4,.8))) if hit<t<hit+1.2 else 0
    c=kc(t,[(a,(760,560,1.08)),(hit,(960,580,1.04)),(b,(1120,560,1.1))],sh)
    put(cv,c,'t13_far',960,700,ay=1,k=.35,o=.9)
    river(cv,c,t,PAP,wl=640,stakes=False,cliffs=False,reeds=0,mist=.5,ridge_o=.6)
    put(cv,c,'t13x_langbac',960,560,s=1.0,o=.55)
    arrows(cv,c,t,a+.2,hit+.6,[(260,700),(380,690)],[(1300,820),(1500,840)],n=10,h=120,per=.9,seed=4,col=HAN)
    arrows(cv,c,t,a+.8,b,[(1600,720),(1700,700)],[(500,820),(650,840)],n=6,h=120,per=1.1,seed=8,col=(.69,.16,.11))
    clash(cv,c,t,hit-1.4,b+2,'han','trung',xm=980,y=800,s=.92,push=1,seed=9,pre='t13_spr_',ten=False)
    di(cv,c,'t13_spr_mavien',-200,860,240,860,t,a,hit,s=.72,bob=4,f=6)
    co_bay(cv,c,'t13_spr_trungco',1600-inn(t,hit,b-hit)*140,880,t,1.1,lat=True)
    if t>hit:
        for k in range(5): put(cv,c,'mist',980+k*90-60,800-20*k,s=.4+.12*k,o=.3*(1-inn(t,hit+3,2)))
    truoc(cv,c,t)
    lb(cv,C0,'Lãng Bạc',960,170,t,a+.3,q-.2,col=RED,sz=52)
    lb(cv,C0,'sách cũ: Hồ Tây · người nay: vùng Tiên Du',960,170,t,q+.2,b,col=INK,sz=36)
    lb(cv,C0,'quân nhà Hán',450,300,t,a+.6,b,col=HAN,sz=36)
    lb(cv,C0,'quân hai bà',1500,300,t,a+.6,b,col=RED,sz=36)
# ---- 13: Mã Viện thắng lớn
def S_13(cv,t):
    a,b=T[13]-.3,E[13]+.3;q=sb(13,1)
    c=kc(t,[(a,(1000,560,1.0)),(b,(1100,560,1.12))])
    ngoai(cv,c,t,g=880,seed=13,mist=.7)
    put(cv,c,'t13x_hang',960,560,s=1.1)
    di(cv,c,'t13_spr_han',2500,880,1500,880,t,a,b,s=.6,bob=3,f=5,lat=True)
    di(cv,c,'t13_spr_trai',300,900,900,900,t,q,b,s=.6,bob=2,f=3)
    di(cv,c,'t13_spr_han',2900,900,1800,900,t,a+.4,b,s=.55,bob=3,f=5.4,ph=1,lat=True)
    di(cv,c,'t13_spr_mavien',2400,870,1650,870,t,a,q+1,s=.62,bob=4,f=6,lat=True)
    for k in range(int((q-a)/1.0)+1):
        t0=a+.3+k*1.0
        if t0<t<t0+1.8: fall(cv,c,'t13_spr_1trung',600+k*80,880,t,t0,s=.9,dirn=1)
    truoc(cv,c,t)
    lb(cv,C0,'Mã Viện thắng lớn',960,170,t,a+.3,q-.2,col=RED,sz=48)
    lb(cv,C0,'hàng nghìn người ngã xuống, hơn mười nghìn người hàng',960,170,t,q+.2,b,col=INK,sz=36)
# ---- 14: nhiều người bỏ đi (cận cảnh hai bà ở lại)
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3;q=sb(14,1)
    c=kc(t,[(a,(1200,560,1.1)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=14)
    put(cv,c,'t13x_roi',960,560,s=1.0)
    for i in range(4): di(cv,c,'t13_spr_1trung',900+i*80,880+(i%2)*20,-400+i*500,860+(i%2)*20,t,q+i*.5,b+1,s=.62,bob=4,f=5+i*.4,ph=i,lat=i%2==0)
    di(cv,c,'t13_spr_dan',1100,890,2400,870,t,q+.3,b,s=.6,bob=3,f=4.4)
    if not FREEZE: ink_wash(cv,.15*inn(t,q,1.2))
    truoc(cv,c,t)
    lb(cv,C0,'Toàn thư: một chi tiết cay đắng',960,170,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'"người đứng đầu là phụ nữ thì không thể thắng"',960,170,t,q+.2,b,col=RED,sz=38)
# ---- 15: Cấm Khê, năm 43
def S_15(cv,t):
    a,b=T[15]-.3,E[15]+.3;q=sb(15,1)
    c=kc(t,[(a,(700,540,1.05)),(b,(1300,540,1.0))])
    ngoai(cv,c,t,g=880,seed=15,mist=.8)
    put(cv,c,'t13x_camkhe',960,540,s=1.0,o=.85)
    di(cv,c,'t13_spr_trung',-200,880,700,880,t,a,b,s=.5,bob=4,f=5.4)
    if t>q-.3: di(cv,c,'t13_spr_han',-1000,880,300,880,t,q-.3,b+1,s=.55,bob=4,f=6)
    co_bay(cv,c,'t13_spr_trungco',lerp(300,900,inn(t,a,b-a)),880,t,1.0)
    truoc(cv,c,t)
    seal(cv,'s43',1560,330,q+.6,t,s=.8,r=4)
    lb(cv,C0,'Cấm Khê: đến nay chưa ai chỉ chắc ở đâu',960,170,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'năm 43: bị cô lập, thua trận',960,170,t,q+.2,b,col=RED,sz=44)
# ---- 16: ba cách chép (ba cuộn sử)
_C3=[(470,'SỬ PHÍA NHÀ HÁN','bị chém'),(960,'SỬ TRIỀU NGUYỄN','bị bắt'),(1450,'DÂN GIAN','gieo mình sông Hát')]
def S_16(cv,t):
    a,b=T[16]-.3,E[16]+.3;q=sb(16,1)
    c=kc(t,[(a,(960,560,1.04)),(b,(960,540,1.0))])
    ngoai(cv,c,t,g=880,seed=16,mist=.5,far=.6,midv=.5)
    put(cv,c,'t13x_hat',960,600,s=1.0,o=.5)
    put(cv,c,'t13x_sach',960,560,s=1.0)
    for i in range(2): di(cv,c,'t13_spr_dan',-300-i*200,900,300+i*200,900,t,a+i*.3,b,s=.45,bob=2,f=3,ph=i,o=.7)
    di(cv,c,'t13_spr_1han',2300,880,1550,880,t,a,b,s=.55,bob=2,f=3.4,lat=True)
    di(cv,c,'t13_spr_1trung',-200,880,620,880,t,q,b,s=.55,bob=2,f=3.2)
    truoc(cv,c,t,.8)
    if not FREEZE:
        for k,(x,tt,ln) in enumerate(_C3):
            t0=q+k*((b-q)/3.2)
            if t>t0:
                u=inn(t,t0,.5)
                put_screen(cv,band(330,130,PAPER,.85,20),x,470,u)
                put_screen(cv,text(tt,26,RED,700),x,440,u);put_screen(cv,wipe(text(ln,32,INK,700),inn(t,t0+.2,.6),0,.25,seed=k),x,490,1)
    lb(cv,C0,'hai bà mất thế nào: mỗi sách chép một kiểu',960,140,t,a+.3,b,col=INK,sz=40)
# ---- 17: thu trống, nấu chảy (cảnh trọng tâm)
def S_17(cv,t):
    a,b=T[17]-.3,E[17]+.3;q=sb(17,1)
    c=kc(t,[(a,(1100,560,1.0)),(b,(860,540,1.18))])
    ngoai(cv,c,t,g=880,seed=17,far=.6,midv=.6,mist=.3)
    put(cv,c,'t13x_lo',960,560,s=1.1)
    for i in range(4):
        t0=a+.6+i*1.3;u=inn(t,t0,2.2)
        if t>t0: trong(cv,c,lerp(1900,980,u),lerp(880,640,u*u)+(0 if u<1 else 40*inn(t,t0+2.2,1.2)),t,s=.75,o=1-inn(t,t0+2.4,1.0))
    di(cv,c,'t13_spr_han',2600,880,1500,880,t,a,b,s=.55,bob=3,f=5,lat=True)
    for k in range(3): flick(cv,c,840+k*40,500,t+k,1.0)
    smoke(cv,c,840,380,t,1.4);smoke(cv,c,900,360,t+1,1.2)
    for i in range(8): dust(cv,c,760+(i%3)*40,520-((t*70+i*60)%320),o=.3,s=.25)
    if not FREEZE and t>q: ink_wash(cv,.12*inn(t,q,1),col=np.array((.55,.2,.1),np.float32))
    truoc(cv,c,t)
    lb(cv,C0,'sử nhà Hán chép rất rõ',960,170,t,a+.3,q-.2,col=INK,sz=44)
    lb(cv,C0,'thu trống đồng của người Lạc Việt, nấu chảy',960,170,t,q+.2,b,col=RED,sz=42)
# ---- 18: ngựa mẫu, mùa thu năm 44 dâng vua
def S_18(cv,t):
    a,b=T[18]-.3,E[18]+.3;q=sb(18,1)
    c=kc(t,[(a,(960,520,1.15)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=18,far=.5,midv=.5,mist=.3)
    put(cv,c,'t13x_dangvua',960,630,s=1.1)
    di(cv,c,'t13_spr_mavien',-300,880,520,880,t,q,b,s=.6,bob=3,f=5)
    for r in range(2): di(cv,c,'t13_spr_1han',-600-r*200,880,250-r*140,880,t,q+r*.3,b,s=.6,bob=2,f=3.6,ph=r)
    for i in range(2): di(cv,c,'t13_spr_quan',2300+i*200,880,1700+i*140,880,t,a+i*.4,b,s=.55,bob=2,f=3,ph=i,lat=True)
    if not FREEZE: vong(cv,960,560,t,a+.4,n=2,per=2.0,rmax=300,o=.25,col=GOLD,flat=.5)
    truoc(cv,c,t)
    seal(cv,'s44',1560,330,q+.4,t,s=.8,r=4)
    lb(cv,C0,'đồng ấy đúc thành một con ngựa mẫu',960,170,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'mùa thu năm 44, mang về kinh đô dâng vua',960,170,t,q+.2,b,col=RED,sz=42)
# ---- 19: trống hóa ngựa (cận cảnh, chia đôi trước/sau)
def S_19(cv,t):
    a,b=T[19]-.3,E[19]+.3;q=sb(19,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.08))])
    ngoai(cv,c,t,g=880,seed=19,mist=.6)
    put(cv,c,'t13x_tat',960,560,s=1.1)
    co_bay(cv,c,'t13_spr_trungco',600,880,t,1.0)
    di(cv,c,'t13_spr_dan',700,890,-400,890,t,a,b,s=.55,bob=3,f=4,lat=True)
    di(cv,c,'t13_spr_1han',2300,880,1600,880,t,q,b,s=.6,bob=3,f=4.2,lat=True)
    truoc(cv,c,t)
    if not FREEZE:
        u=inn(t,q,1.6);ink_wash(cv,.4)
        put(cv,C0,'t13_spr_matrong',960,470,s=.7,o=1-u,r=4*t)
        put(cv,C0,'t13_spr_ngua',960,640,s=1.5,ay=1,o=u,scale_px=1.5)
        vong(cv,960,470,t,a+.3,n=3,per=1.6,rmax=420,o=.4*(1-u),flat=1.0)
    lb(cv,C0,'trống: quyền của các Lạc tướng, như cha Trưng Trắc',960,150,t,a+.3,q-.2,col=INK,sz=38)
    lb(cv,C0,'nấu thành ngựa dâng vua: ai đã thắng',960,150,t,q+.2,b,col=RED,sz=42)
# ---- 20: chiến thắng không rẻ: mười người, bốn năm người chết
def S_20(cv,t):
    a,b=T[20]-.3,E[20]+.3;q=sb(20,1)
    c=kc(t,[(a,(700,560,1.05)),(b,(1200,560,1.1))])
    ngoai(cv,c,t,g=900,seed=20,mist=.2,far=.7,midv=.7)
    for k in range(4): put(cv,c,'mist',(t*40+k*600)%2600-300,620+k*50,s=2.0,o=.45,k=.9)
    for r in range(2): di(cv,c,'t13_spr_han',-500-r*400,850+r*40,1000-r*300,850+r*40,t,a-1,q+1,s=.7+.06*r,bob=3,f=4.6+r*.5,ph=r)
    for k in range(6):
        t0=q-.4+k*.5
        if t0<t<t0+2.6: fall(cv,c,'t13_spr_1han',420+k*130,880,t,t0,s=1.0,dirn=1)
    truoc(cv,c,t)
    if not FREEZE and t>q-.6:
        for k in range(10):
            dead=k<5 and t>q-.4+k*.4
            put(cv,C0,'t13_spr_1han',560+k*90,330,s=.5,ay=1,o=.95 if not dead else .25,r=0 if not dead else 80,scale_px=1.5)
    lb(cv,C0,'chiến thắng ấy không rẻ',960,160,t,a+.3,q-.6,col=RED,sz=46)
    lb(cv,C0,'mười người, bốn năm người chết vì khí độc, dịch bệnh',960,400,t,q-.4,b,col=INK,sz=34)
# ---- 21: vì sao không giữ nổi
def S_21(cv,t):
    a,b=T[21]-.3,E[21]+.3;q=sb(21,1)
    c=kc(t,[(a,(1200,560,1.05)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=21,mist=.6)
    put(cv,c,'t13x_thanh65',960,560,s=1.0,o=.85)
    if t>q-.3: di(cv,c,'t13_spr_thuyen',2300,700,1300,690,t,q,b,s=.55,bob=3,f=1.8,k=.8,lac=2)
    di(cv,c,'t13_spr_1trung',600,880,-300,880,t,q,b,s=.6,bob=4,f=5,lat=True)
    di(cv,c,'t13_spr_1trung',900,880,-100,880,t,q+.8,b,s=.6,bob=4,f=5.4,lat=True)
    co_bay(cv,c,'t13_spr_trungco',1400,880,t,1.0)
    truoc(cv,c,t)
    lb(cv,C0,'65 thành đáp lại, vẫn không giữ nổi: vì sao?',960,170,t,a+.3,q-.2,col=RED,sz=42)
    lb(cv,C0,'sử ghi: thuyền lương theo sau · những người bỏ đi',960,170,t,q+.2,b,col=INK,sz=38)
# ---- 22: Lê Văn Hưu nhìn ở phía khác (vòng tiếng gọi trở lại)
def S_22(cv,t):
    a,b=T[22]-.3,E[22]+.3;q=sb(22,1)
    c=kc(t,[(a,(960,520,1.12)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=22,mist=.4)
    put(cv,c,'t13x_hoi',960,560,s=1.05)
    for i in range(3): di(cv,c,'t13_spr_trung',-900-i*200,880+i*20,-100+i*250,880+i*20,t,q+i*.4,b+1,s=.5,bob=4,f=5.4+i*.3,ph=i)
    trong(cv,c,960,890,t,s=.6)
    vong(cv,*c.p(960,800),t,q,n=3,per=1.4,rmax=620,o=.4)
    truoc(cv,c,t)
    lb(cv,C0,'sử gia Lê Văn Hưu',960,170,t,a+.3,q-.2,col=INK,sz=46)
    if not FREEZE and t>q:
        put_screen(cv,band(1400,150,PAPER,.8,30),960,215,inn(t,q,.4))
        put_screen(cv,wipe(text('một tiếng gọi, sáu mươi lăm thành đáp lại',44,RED,700),inn(t,q+.2,1.2),0,.25,seed=22),960,190,1)
        put_screen(cv,text('người nước ta không có cớ tự coi thường mình',32,INK,600),960,250,inn(t,q+1.8,.6))
# ---- 23: kết
def S_23(cv,t):
    a=T[23]-.3;b=E[23]+4;q=sb(23,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,520,1.1))])
    ngoai(cv,c,t,g=880,seed=23,mist=.6)
    put(cv,c,'t13x_cuoi',960,560,s=1.1)
    di(cv,c,'t13_spr_dan',-300,890,700,890,t,a,b,s=.55,bob=3,f=4)
    di(cv,c,'t13_spr_1trung',2300,880,1500,880,t,a+.5,b,s=.55,bob=2,f=3,lat=True)
    trong(cv,c,600,890,t,s=.55)
    vong(cv,*c.p(600,820),t,a+.5,n=3,per=1.8,rmax=900,o=.3)
    smoke(cv,c,1600,640,t,1.0)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    if not FREEZE:
        tx=text('Hai Bà Trưng, năm 40 đến 43',54,INK,700);put_screen(cv,wipe(tx,inn(t,a+.8,1.4),0,.3,seed=13),W/2,170)
        put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,245,inn(t,E[23]+.6,1))
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
    flock=lambda *a,**k:None
S=lambda n:T[n]-.3
_FN={1:S_1,8:S_8v}
SH=[(0 if n==1 else S(n),S(n+1) if n<23 else V.TOTAL+1,_FN.get(n) or globals()[f'S_{n}']) for n in range(1,24)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm13_full.json'))
SENT={}
for _i,_d in enumerate(_J):
    _hs=[x for x in re.split(r'(?<=[.!?])\s+',_d['hien']) if x.strip()]
    SENT[_i+1]=_hs if len(_hs)==len(_SC[_i+1])-1 else [_d['hien']]
def caps(cv,t):
    for n,hs in SENT.items():
        for k,h in enumerate(hs):
            a=sb(n,k) if len(hs)>1 else T[n];b=sb(n,k+1) if len(hs)>1 else E[n]
            if a<t<b: caption(cv,h,inn(t,a,.12)*(1-inn(t,b-.12,.12)),False)
def ov(cv,t):
    if FREEZE: return
    TT=T[4]
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'MÊ LINH','stitle13b',.55)
    caps(cv,t)
V.NHAN={2:'Mã Viện – tướng nhà Hán'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
