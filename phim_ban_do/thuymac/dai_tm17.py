# Bản dài tm17: Lý Bí, ba lần bị đánh, khung bí ẩn cái chết (bản 3). Dựng theo chuẩn chi tiết 20/11 và các cách dựng mới:
# hình ảnh lặp lại (khí độc xanh xám: mở đầu, Hợp Phố, cuối), mở đầu giọt mực loang, chuyển cảnh bằng mực, chia đôi hai cuộn sử,
# lặng nhịp trước câu nhấn. Quy ước màu: quân Lý Bí đỏ son, quân nhà Lương xanh chàm đội mũ trụ; khí độc xanh xám chỉ dùng cho khí độc.
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
C0=None
V=K.setup('tm17',{4:4.0})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
FREEZE=bool(os.environ.get('KIEM_TINH'))
GS=1.45
DOCC=np.array((.37,.42,.30),np.float32)
_SC={}
for _n,_t in TX.items():
    _s=[x for x in re.split(r'(?<=[.!?])\s+',_t) if x.strip()];_w=[len(x.split()) for x in _s];_tot=sum(_w);_c=[0]
    for _k in _w: _c.append(_c[-1]+_k/_tot)
    _SC[_n]=_c
def sb(n,k): return T[n]+(E[n]-T[n])*_SC[n][min(k,len(_SC[n])-1)]
def kc(t,keys,sh=0):
    if FREEZE: t=keys[0][0];sh=0
    cx,cy,z=cpath(t,keys);return cam(cx,cy,z,sh,sh)
C0=cam(960,540,1.0)
def mcam(t,keys):
    if FREEZE: t=keys[0][0]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z);return cam(cx,cy,z)
def suong(cv,c,t,y=560,o=.5,seed=0):
    if FREEZE: return
    for i,(sp,k,yy,s) in enumerate([(22,.5,y-120,2.2),(34,1.1,y+120,2.6)]):
        x=(300+seed*400+i*900+t*sp)%2800-400;put(cv,c,'mist',x,yy,s=s,o=o*(.8 if i else 1),k=k)
def ngoai(cv,c,t,g=900,far=.9,midv=.85,mist=.5,seed=0):
    put(cv,c,'t17_far',960+seed*60,g-120,ay=1,k=.35,o=far)
    put(cv,c,'t17_mid',960-seed*40,g+40,ay=1,k=.62,o=midv)
    suong(cv,c,t,g-260,mist,seed)
def truoc(cv,c,t,o=1):
    put(cv,c,'t17_frontL',-120,1120,ax=0,ay=1,k=1.3,s=.85,r=1.2*math.sin(t*.8),o=o)
    put(cv,c,'t17_frontR',2040,1120,ax=1,ay=1,k=1.3,s=.8,r=1.2*math.sin(t*.7+1),o=o)
def di(cv,c,name,x0,y0,x1,y1,t,a,b,s=1.0,o=.97,bob=4,f=5,ph=0,k=1.0,r=0,lac=1.2):
    if y0>700 and k==1.0: s*=GS;bob*=GS
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;y=y0+(y1-y0)*u-abs(math.sin(t*f+ph))*bob*(1 if 0<u<1 else .3)
    put(cv,c,name,x,y,s=s,o=o,k=k,r=r+lac*math.sin(t*f*.5+ph),ay=1)
    return x,y
def flick(cv,c,x,y,t,s=1.0):
    put(cv,c,'t12_spr_lua',x+6*math.sin(t*7),y,s=min(s,.38)*(1+.08*math.sin(t*9)),o=.5+.3*math.sin(t*5)**2)
# ---- hình ảnh lặp lại: khí độc (xanh xám, cuộn chậm, mỗi đám một nhịp)
def khidoc(cv,c,t,x0,y0,dx,n=3,s=1.0,o=.8,sp=30,k=1.0,seed=0):
    for i in range(n):
        ph=seed*1.7+i*2.1
        x=x0+i*dx*.45+((t*sp+i*170)%(abs(dx)+400))*(1 if dx>=0 else -1)
        put(cv,c,'t17_spr_doc',x,y0-i*30+12*math.sin(t*.6+ph),s=s*(1+.08*math.sin(t*.4+ph)),o=o*(.75+.25*math.sin(t*.5+ph)),r=4*math.sin(t*.3+ph),k=k)
# ---- mặt nạ mực
_NZ=None
def nz():
    global _NZ
    if _NZ is None:
        rg=np.random.default_rng(17);a=rg.random((34,60)).astype(np.float32)
        from PIL import Image as _I
        _NZ=np.asarray(_I.fromarray((a*255).astype(np.uint8)).resize((W,H),_I.BICUBIC),np.float32)/255
    return _NZ
_YY,_XX=np.mgrid[0:H,0:W].astype(np.float32)
def loang(cx,cy,r,soft=40):
    d=np.sqrt((_XX-cx)**2+(_YY-cy)**2)+ (nz()-.5)*r*.35
    return np.clip((r-d)/soft,0,1)[...,None]
_RG=ragged(H,7)[:,None]
def quet(u,band=.12):
    x=_XX/W+(_RG-.5)*.16
    return np.clip((u*(1+band*2)-band-x)/band,0,1)[...,None]
# 1: giọt mực rơi, loang thành động Khuất Lão; câu hỏi lớn
def canh_dong(cv,t,a,b,push=True,keys=None):
    c=kc(t,keys or [(a,(960,560,1.0)),(b,(960,600,1.18 if push else 1.05))])
    ngoai(cv,c,t,g=900,seed=1,mist=.4)
    put(cv,c,'t17x_dong',960,560,s=1.0)
    flick(cv,c,1010,820,t,.9)
    khidoc(cv,c,t,600,640,700,n=3,s=1.1,o=.7,sp=22,seed=1)
    put(cv,c,'t17_spr_lb',965,870,s=.7,ay=1,o=.75+.15*math.sin(t*1.1)**2)
    truoc(cv,c,t)
    return c
def S_1(cv,t):
    a,b=0,E[1]+.3;td=.95
    sc=PAP.copy();canh_dong(sc,t,a,b)
    if FREEZE: cv[:]=sc;return
    if t<td:
        y=-40+(540+40)*(t/td)**2
        m=loang(960,y,22,6);cv[:]=cv*(1-m)+np.array(INK,np.float32)*m
    else:
        u=inn(t,td,1.6);r=30+u*1300
        m=loang(960,540,r,60);rim=np.clip(loang(960,540,r,60)-loang(960,540,r-70,60),0,1)
        cv[:]=cv*(1-m)+sc*m;cv[:]=cv*(1-rim*.75)+np.array(INK,np.float32)*rim*.75
        if t<td+.25:
            for k in range(7):
                ang=k*.9;dd=40+260*inn(t,td,.25)
                put(cv,cam(960,540,1),'t12_spr_khoi',960+math.cos(ang)*dd,540+math.sin(ang)*dd*.6,s=.15,o=.0)
    big(cv,'LÝ NAM ĐẾ CHẾT THẾ NÀO?',t,1.6,b,RED,150,80,seed=1)
# 2: hai cuộn sử chia đôi màn hình
_L=['ốm nhiều ngày','vì khí độc núi rừng','mất trong động Khuất Lão']
_R=['người trong động','chém ông','gửi đầu về kinh đô nhà Lương']
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3;q=sb(2,1)
    canh_dong(cv,t,a-5,b,push=False);ink_wash(cv,.55)
    c=cam(960,540,1.0)
    actL=1-inn(t,q-.1,.4)*.55;actR=.45+.55*inn(t,q-.1,.4)
    for x,act,tt,lines,ta,tb,col in ((540,actL,'SỬ TA',_L,a+.3,q,INK),(1380,actR,'SỬ PHƯƠNG BẮC',_R,q,E[2],INK)):
        put(cv,c,'t17_cuon',x,500,s=.95,o=.35+.65*act,r=.6*math.sin(t*.7+x))
        put_screen(cv,text(tt,40,RED,700),x,200,act)
        for k,ln in enumerate(lines):
            t0=ta+(tb-ta)*k/len(lines)
            if t>t0: put_screen(cv,wipe(text(ln,36,col,600),inn(t,t0,.7),0,.25,seed=k+int(x)),x,330+k*90,act)
    if not FREEZE:
        khidoc(cv,c,t,250,700,500,n=2,s=.7,o=.6*actL,sp=26,seed=2)
        if t>q+1.2:
            stroke(cv,c,[(1200,700),(1580,600)],inn(t,q+1.2,.35),wid=10,col=RED,o=.8*actR,head=False)
    else:
        put(cv,c,'t17_spr_doc',300+40*math.sin(t),700,s=.7,o=.5);put(cv,c,'t17_spr_doc',600+30*math.sin(t*.8),720,s=.6,o=.5);put(cv,c,'t17_cuon',540,500,s=.62,r=2*math.sin(t*2))
# 3: thứ đã khép đời ông cũng là thứ từng cứu ông (lóe về Hợp Phố) → quét mực sang viên quan nhỏ
def hopphoso(cv,t,a,b):
    c=kc(t,[(a,(900,560,1.04)),(b,(1100,560,1.1))])
    ngoai(cv,c,t,g=900,seed=3,mist=.3,far=.7,midv=.7)
    khidoc(cv,c,t,-600,600,900,n=3,s=1.6,o=.7,sp=70,seed=3,k=.8)
    di(cv,c,'t17_spr_luong',-300,830,900,830,t,a-1,b+2,s=.75,bob=3,f=5)
    di(cv,c,'t17_spr_luong',-800,880,500,880,t,a-1,b+2,s=.82,bob=3,f=5.4,ph=1)
    for k in range(5):
        t0=a+1.0+k*.6
        if t0<t<t0+2.4: fall(cv,c,'t17_spr_1luong',200+k*130,870,t,t0,s=1.15,dirn=1)
    khidoc(cv,c,t,-500,820,900,n=2,s=1.3,o=.45,sp=90,seed=5)
    truoc(cv,c,t,.9)
    ink_wash(cv,.12,col=DOCC)
def quannho(cv,t,a,b):
    c=kc(t,[(a,(960,560,1.08)),(b,(960,540,1.0))])
    ngoai(cv,c,t,g=880,seed=4,mist=.4)
    put(cv,c,'t17x_quan',960,560,s=1.1)
    for j in range(4): stroke(cv,c,[(760+j*90,575),(800+j*90,575)],inn(t,a+.4+j*.6,.4),wid=4,col=INK,o=.8,head=False)
    di(cv,c,'t17_spr_1luong',2300,860,1700,860,t,a,b,s=.62,bob=3,f=4.5)
    truoc(cv,c,t)
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3;q=sb(3,1)
    if t<q-.6 or FREEZE: hopphoso(cv,t,a,q+1)
    else:
        A_=PAP.copy();hopphoso(A_,t,a,q+1);B_=PAP.copy();quannho(B_,t,q-.6,b+4)
        m=quet(inn(t,q-.6,1.1));cv[:]=A_*(1-m)+B_*m
    lb(cv,cam(960,540,1),'mấy năm trước, Hợp Phố',960,170,t,a+.5,q-.5,col=INK,sz=40)
def S_tam(cv,t):
    c=kc(t,[(T[4]-.3,(960,560,1.0)),(V.TOTAL,(960,560,1.05))]);quannho(cv,t,T[4]-.3,V.TOTAL)

# ---- bộ đếm ba lần bị đánh (góc trên bên trái)
from PIL import Image as _Im, ImageDraw as _ID
_BOX={}
def _box(kq):
    if kq in _BOX: return _BOX[kq]
    im=_Im.new('RGBA',(96,96),(0,0,0,0));d=_ID.Draw(im)
    if kq: d.rectangle([4,4,92,92],fill=(176,40,28,235))
    d.rectangle([4,4,92,92],outline=(43,38,32,230),width=5)
    a=np.asarray(im,np.float32)/255;a[...,:3]*=a[...,3:4]
    if kq:
        tx=text(kq,26,PAPER,700,rough=False)
    _BOX[kq]=a;return a
DEM=lambda:[(sb(16,1),'GIỮ'),(sb(20,1),'THẮNG'),(sb(25,1),'MẤT')]
def dem(cv,t):
    if FREEZE or t<T[11]-.3 or t>E[29]+.5: return
    o=inn(t,T[11]-.3,.6)
    for i,(ts,kq) in enumerate(DEM()):
        x,y=70+i*112,64
        blend(cv,_box(None),x,y,o*.9)
        if t>ts:
            u=inn(t,ts,.35);sz=int(96*(1.6-.6*u))
            im=_box(kq);put_screen(cv,text(kq,24,PAPER,700),x+48,y+48,o*u) if False else None
            blend(cv,im,x,y,o*u);put_screen(cv,text(kq,22,PAPER,700),x+48,y+50,o*u)
        put_screen(cv,text(f'lần {i+1}',22,INK,600),x+48,y+118,o*.9)
# ---- các cảnh 4–29
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3;q=sb(4,1)
    c=kc(t,[(a,(1200,560,1.1)),(b,(900,560,1.0))])
    ngoai(cv,c,t,g=880,seed=5)
    put(cv,c,'t17x_trai',960,560,s=1.05)
    for i in range(3): di(cv,c,'t17_spr_1luong',300+i*150,860,700+i*150,860,t,a+i*.4,b,s=.62,bob=3,f=4+i*.6,ph=i)
    di(cv,c,'t17_spr_1viet',-200,880,500,880,t,q,b,s=.62,bob=3,f=4.2)
    truoc(cv,c,t)
    lb(cv,C0,'Lý Bí, quan coi việc quân ở Cửu Đức',960,170,t,a+.4,q-.2,col=RED,sz=40)
    lb(cv,C0,'có tài, không chỗ dùng tài',960,170,t,q+.2,b,col=INK,sz=42)
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3;q=sb(5,1)
    c=kc(t,[(a,(700,560,1.1)),(b,(1300,560,1.05))])
    ngoai(cv,c,t,g=880,seed=6,far=.7)
    put(cv,c,'t17x_deo',960,560,s=1.0)
    for i in range(3): di(cv,c,'t17_spr_dicu',-400-i*300,860+i*20,1400-i*260,840+i*20,t,a,b+2,s=.75,bob=3,f=4.4+i*.3,ph=i)
    # bảy đời: bảy ô triện nhỏ đóng lần lượt
    if not FREEZE:
        for k in range(7):
            tk=q+.2+k*.45
            if t>tk: dot(cv,cam(960,540,1),620+k*110,260,o=inn(t,tk,.25),col=RED,r=int(18*(1.5-.5*inn(t,tk,.25))))
    truoc(cv,c,t)
    lb(cv,C0,'tổ tiên là người phương bắc',960,170,t,a+.4,q-.2,col=INK,sz=42)
    lb(cv,C0,'bảy đời, thành người phương nam',960,170,t,q+.2,b,col=RED,sz=42)
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3;q=sb(6,1)
    c=kc(t,[(a,(960,540,1.0)),(b,(1000,560,1.12))])
    ngoai(cv,c,t,g=880,seed=7)
    put(cv,c,'t17x_tieutu',960,560,s=1.1)
    for i in range(3): di(cv,c,'t17_spr_dicu',2300+i*200,880,1500+i*160,880,t,a+i*.5,q+1,s=.55,bob=2,f=3.6,ph=i)
    if t>q: di(cv,c,'t17_spr_cuacai',1500,800,900,700,t,q,b,s=.5,bob=6,f=6,k=1.0)
    di(cv,c,'t17_spr_1luong',1250,860,1350,860,t,a,b,s=.62,bob=2,f=1.4)
    truoc(cv,c,t)
    lb(cv,C0,'Giao Châu dưới sự cai trị của nhà Lương',960,170,t,a+.4,q-.2,col=INK,sz=40)
    lb(cv,C0,'Tiêu Tư, cháu vua Lương: hà khắc',960,170,t,q+.2,b,col=RED,sz=42)
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3;q=sb(7,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,520,1.15))])
    ngoai(cv,c,t,g=880,seed=8,far=.5,midv=.5)
    put(cv,c,'t17x_kinhdo',960,560,s=1.1)
    x,y=di(cv,c,'t17_spr_dicu',-200,880,620,880,t,a,q,s=.6,bob=3,f=4)
    if t>q: put_screen(cv,text('họ Tinh? chưa ai làm nên chuyện',36,RED,600),960,240,inn(t,q,.4))
    for i in range(2): di(cv,c,'t17_spr_1luong',1400+i*300,860,1700-i*300,860,t,a+i,b,s=.62,bob=3,f=3.4+i,ph=i)
    di(cv,c,'t17_spr_dicu',2400,890,1700,890,t,a+.5,b,s=.5,bob=2,f=3.2)
    truoc(cv,c,t)
    lb(cv,C0,'Tinh Thiều lên kinh đô nhà Lương',960,170,t,a+.4,q-.2,col=INK,sz=42)
def S_8(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1)
    c=kc(t,[(a,(960,420,1.3)),(q,(960,480,1.15)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=900,seed=9)
    put(cv,c,'t17x_cong',960,540,s=1.0)
    if t<q+.4: di(cv,c,'t17_spr_1viet',760,860,1160,860,t,a,q,s=.55,bob=2,f=2.4,lac=.8)
    else: di(cv,c,'t17_spr_1viet',1160,860,-300,880,t,q+.4,b,s=.6,bob=4,f=5)
    di(cv,c,'t17_spr_dicu',-400,890,500,890,t,a,b,s=.5,bob=2,f=3.6)
    di(cv,c,'t17_spr_1luong',1700,860,1300,860,t,a,b,s=.55,bob=2,f=3)
    di(cv,c,'t17_spr_dicu',2400,890,1600,890,t,a,b,s=.5,bob=2,f=3.5)
    truoc(cv,c,t)
    lb(cv,C0,'việc được giao: canh một cổng thành',960,170,t,a+.6,q-.2,col=RED,sz=42)
    lb(cv,C0,'Tinh Thiều bỏ về, tìm đến Lý Bí',960,170,t,q+.2,b,col=INK,sz=42)
def S_9(cv,t):
    a,b=T[9]-.3,E[9]+.3;q=sb(9,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,520,1.12))])
    ngoai(cv,c,t,g=880,seed=10)
    put(cv,c,'t17x_hoi',960,560,s=1.1)
    for i in range(3):
        di(cv,c,'t17_spr_viet',2600+i*150,880+i*24,1500+i*150,880+i*24,t,a+i*.5,b,s=.5,bob=4,f=5.5+i*.4,ph=i)
        di(cv,c,'t17_spr_vietr',-900-i*150,880+i*24,-100+i*150,880+i*24,t,q+i*.5,b,s=.5,bob=4,f=5.8+i*.4,ph=i+2)
    truoc(cv,c,t)
    lb(cv,C0,'Triệu Túc, người đứng đầu vùng Chu Diên',960,170,t,a+.4,q-.2,col=RED,sz=40)
    lb(cv,C0,'người nhiều châu lần lượt theo về',960,170,t,q+.2,b,col=INK,sz=40)
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3;q=sb(10,1)
    c=kc(t,[(a,(960,560,1.0)),(q,(1300,640,1.4)),(b,(960,560,1.05))])
    ngoai(cv,c,t,g=900,seed=11)
    put(cv,c,'t17x_longbien',960,520,s=.95)
    for i in range(2): di(cv,c,'t17_spr_vietr',-900-i*200,880+i*30,500-i*200,880+i*30,t,a,b,s=.55,bob=5,f=6+i*.5,ph=i)
    if t>q-.2:
        put(cv,c,'t17_spr_cuacai',1300,700,s=.6+.04*math.sin(t*3),ay=1,r=4*math.sin(t*2))
        di(cv,c,'t17_spr_ngua',1250,880,2500,840,t,q+1.2,b+1,s=.62,bob=7,f=9,lac=2)
    truoc(cv,c,t)
    seal(cv,'s541',1560,320,a+.4,t,s=.8,r=4) if False else None
    lb(cv,C0,'năm 541, nổi dậy',960,170,t,a+.3,q-.2,col=RED,sz=46)
    lb(cv,C0,'Tiêu Tư đút lót để chạy về Quảng Châu',960,170,t,q+.2,b,col=INK,sz=40)
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3;q=sb(11,1)
    c=kc(t,[(a,(960,420,1.2)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=900,seed=12)
    put(cv,c,'t17x_thanhco',960,540,s=1.0)
    u=inn(t,a+.5,2.0)
    put(cv,c,'t17_spr_1luong',760,300+120*u,s=.55,ay=1,o=1-u,r=-30*u)
    co=put(cv,c,'t17_spr_vietr',960,320,s=.25,ay=1,o=0)
    put_screen(cv,text('',10,INK),0,0,0)
    di(cv,c,'t17_spr_1viet',1200,330,1200,330,t,a,b,s=.45,bob=1,f=2,k=1.0,lac=3)
    for i in range(2): di(cv,c,'t17_spr_vietr',-700-i*200,880+i*24,400-i*180,880+i*24,t,a,b,s=.55,bob=4,f=5.5,ph=i)
    truoc(cv,c,t)
    lb(cv,C0,'Long Biên đổi chủ, gần như không đổ máu',960,170,t,a+.4,q-.2,col=RED,sz=40)
    lb(cv,C0,'nhà Lương sẽ quay lại: ba lần',960,170,t,q+.2,b,col=INK,sz=42)
def S_12(cv,t):
    a,b=T[12]-.3,E[12]+.3
    c=kc(t,[(a,(1200,560,1.05)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=13)
    put(cv,c,'t17x_luongtrai',960,560,s=1.0)
    for r in range(3): di(cv,c,'t17_spr_luong',-800-r*240,860+r*28,700-r*200,860+r*28,t,a+r*.3,b+1,s=.5+.04*r,bob=3,f=5+r*.4,ph=r)
    truoc(cv,c,t)
    lb(cv,C0,'lần thứ nhất: Tôn Quýnh, Lư Tử Hùng',960,170,t,a+.4,b,col=RED,sz=42)
def S_13(cv,t):
    a,b=T[13]-.3,E[13]+.3;q=sb(13,1)
    c=kc(t,[(a,(960,560,1.0)),(q,(960,520,1.25)),(b,(960,540,1.3))])
    ngoai(cv,c,t,g=880,seed=14,mist=.3)
    khidoc(cv,c,t,-300,760,900,n=3,s=1.2,o=.35+.4*inn(t,a+1,3),sp=18,seed=7)
    put(cv,c,'t17_spr_cuon',960,520,s=.8,o=.95,r=.8*math.sin(t*.8))
    put_screen(cv,text('LỆNH',44,RED,700),960,230,inn(t,a+.6,.4)) if not FREEZE else None
    if t>q: put_screen(cv,wipe(text('đi ngay',72,RED,700),inn(t,q+.2,.6),0,.25,seed=3),960,470,1) if not FREEZE else None
    for i in range(2): di(cv,c,'t17_spr_1luong',600+i*700,860,640+i*700,860,t,a,b,s=.6,bob=1.5,f=1.5,ph=i,lac=.8)
    truoc(cv,c,t)
    lb(cv,C0,'mùa xuân, mùa khí độc bốc lên',960,150,t,a+.4,q-.2,col=INK,sz=42) if False else None
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3;q=sb(14,1)
    c=kc(t,[(a,(700,560,1.05)),(b,(1200,560,1.12))])
    ngoai(cv,c,t,g=900,seed=15,mist=.2,far=.7,midv=.7)
    khidoc(cv,c,t,-400,620,900,n=3,s=1.7,o=.65,sp=50,seed=8,k=.8)
    for r in range(2): di(cv,c,'t17_spr_luong',-500-r*400,850+r*40,1100-r*300,850+r*40,t,a-1,q+1.5,s=.75+.06*r,bob=3,f=5+r*.5,ph=r)
    for k in range(7):
        t0=q-.8+k*.5
        if t0<t<t0+2.6: fall(cv,c,'t17_spr_1luong',380+k*120,880,t,t0,s=1.1,dirn=1)
    if t>q+1.4:
        for i in range(3): di(cv,c,'t17_spr_1luong',1100+i*80,870,-300+i*200,870,t,q+1.4+i*.3,b,s=.62,bob=6,f=8,ph=i,r=0) if False else put(cv,c,Af('t17_spr_1luong'),lerp(1100+i*80,-200+i*200,inn(t,q+1.4+i*.3,b-q-1.4)),870-abs(math.sin(t*8+i))*10,s=.62*GS,ay=1,scale_px=1.5)
    khidoc(cv,c,t,-500,860,900,n=2,s=1.4,o=.5,sp=80,seed=9)
    truoc(cv,c,t)
    if not FREEZE and t>q-.6:
        for k in range(10):
            dead=k<7 and t>q-.6+k*.35
            put(cv,cam(960,540,1),'t17_spr_1luong',560+k*90,330,s=.55,ay=1,o=.95 if not dead else .25,r=0 if not dead else 80)
    lb(cv,C0,'Hợp Phố',960,160,t,a+.3,q-.8,col=RED,sz=48)
    lb(cv,C0,'mười người, sáu bảy người chết vì bệnh',960,320,t,q-.4,b,col=INK,sz=36)
def S_15(cv,t):
    a,b=T[15]-.3,E[15]+.3;q=sb(15,1)
    c=kc(t,[(a,(960,540,1.0)),(b,(960,540,1.06))])
    ngoai(cv,c,t,g=880,seed=16,mist=.6,far=.6,midv=.6);ink_wash(cv,.35)
    c2=cam(960,540,1.0)
    for x,tt,ln,act,col in ((540,'NHIỀU BÀI VIẾT NGÀY NAY','mai phục, đánh tan',1-inn(t,q,.4)*.5,INK),(1380,'SỬ CŨ CẢ HAI BÊN','tan vì bệnh',.5+.5*inn(t,q,.4),RED)):
        put(cv,c2,'t17_spr_cuon',x,560,s=.78,o=.35+.65*act,r=.6*math.sin(t*.7+x))
        if not FREEZE: put_screen(cv,text(tt,30,RED,700),x,330,act);put_screen(cv,text(ln,40,col,700),x,480,act)
    if t>q+.4: stroke(cv,c2,[(380,490),(700,470)],inn(t,q+.4,.4),wid=8,col=RED,o=.8,head=False)
    khidoc(cv,c2,t,900,760,500,n=2,s=.9,o=.55,sp=24,seed=10)
    di(cv,c2,'t17_spr_1luong',-200,900,700,900,t,q,b+2,s=.5,bob=4,f=6,o=.6)
    di(cv,c2,'t17_spr_1luong',2100,900,1300,900,t,a,b,s=.5,bob=4,f=6.4,o=.6)
    lb(cv,C0,'không có trận đánh nào ở Hợp Phố',960,190,t,a+.3,q-.1,col=RED,sz=42)
def S_16(cv,t):
    a,b=T[16]-.3,E[16]+.3;q=sb(16,1)
    c=kc(t,[(a,(700,560,1.0)),(b,(1300,560,1.08))])
    ngoai(cv,c,t,g=880,seed=17,mist=.2)
    khidoc(cv,c,t,-200,700,1000,n=4,s=1.5,o=.7,sp=40,seed=11)
    di(cv,c,'t17_spr_1viet',1400,880,1420,880,t,a,b,s=.62,bob=1,f=1.2,lac=.5)
    truoc(cv,c,t)
    lb(cv,C0,'hãy nhớ thứ khí độc ấy',960,170,t,a+.4,b,col=DOCC if False else INK,sz=46)
def S_17(cv,t):
    a,b=T[17]-.3,E[17]+.3;q=sb(17,1)
    c=kc(t,[(a,(960,540,1.0)),(b,(960,560,1.12))])
    ngoai(cv,c,t,g=880,seed=18,far=.5,midv=.5)
    put(cv,c,'t17x_luongdien',960,560,s=1.1)
    put(cv,c,'t17_spr_quy2',960,880,s=.9,ay=1,r=1.5*math.sin(t*1.5))
    for i in range(2): di(cv,c,'t17_spr_1luong',200+i*1300,860,600+i*900,860,t,a+i*.5,b,s=.62,bob=3,f=3.5,ph=i)
    put(cv,c,'t17_spr_cuon',1300,520,s=.35,o=inn(t,q,.5),r=3*math.sin(t*1.5))
    if t>q: stroke(cv,c,[(800,300),(1120,300)],inn(t,q+.3,.6),wid=10,col=RED,o=.8,head=False)
    truoc(cv,c,t)
    lb(cv,C0,'Tiêu Tư đổ tội: thông đồng với Lý Bí',960,170,t,a+.4,q-.2,col=INK,sz=40)
    lb(cv,C0,'hai tướng bị bắt phải chết',960,170,t,q+.2,b,col=RED,sz=44)
def S_18(cv,t):
    a,b=T[18]-.3,E[18]+.3;q=sb(18,1)
    c=kc(t,[(a,(1100,560,1.05)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=19)
    put(cv,c,'t17x_quangchau',960,520,s=.9)
    clash(cv,c,t,a+.3,q+1,'luong','noiloan',xm=1000,y=760,s=.92,push=1,seed=12,pre='t17_spr_')
    if t>q-.5: di(cv,c,'t17_spr_tbt',-300,880,500,880,t,q-.5,b,s=.62,bob=5,f=6)
    truoc(cv,c,t)
    lb(cv,C0,'nổi loạn ở Quảng Châu',1350,300,t,a+.4,q,col=(.69,.5,.13),sz=34)
    lb(cv,C0,'Trần Bá Tiên dẹp được',960,170,t,q+.2,b,col=INK,sz=44)
def S_19(cv,t):
    a,b=T[19]-.3,E[19]+.3
    dl,th,ng=P['daila'],P['thanhhoa'],P['nghean']
    c=mcam(t,[(a,(800,800,1.1)),(b,(900,760,1.0))])
    mapbg(cv,c,u=1)
    for nm,p in (('Long Biên',dl),('Cửu Đức',(ng[0]-30,ng[1]-60)),('Nhật Nam',ng)):
        dot(cv,c,*p);tag(cv,c,p[0]+22,p[1]-6,nm,dy=0,sz=26)
    u=inn(t,a,b-a)
    stroke(cv,c,[(ng[0]+200,ng[1]+300),ng],u,wid=8,col=(.31,.24,.39))
    put(cv,c,'t17_spr_lamap',lerp(ng[0]+240,ng[0]+40,u),lerp(ng[1]+330,ng[1]+40,u),s=.45,ay=1,r=2*math.sin(t*5))
    put(cv,c,'t17_spr_vietr',lerp(dl[0],ng[0]-40,inn(t,a,b-a)),lerp(dl[1],ng[1]-70,inn(t,a,b-a)),s=.42,ay=1,r=2*math.sin(t*6))
    for k in range(2):
        uu=((t*.6+k*.5)%1.0);dot(cv,c,ng[0],ng[1],o=.6*(1-uu),col=(.31,.24,.39),r=int(10+50*uu))
    put(cv,c,'t17_spr_1lamap',ng[0]+300-200*u,ng[1]+380-300*u,s=.42,ay=1,r=3*math.sin(t*5))
    lb(cv,C0,'lần thứ hai: Lâm Ấp đánh từ phía nam',960,170,t,a+.3,b,col=RED,sz=40)
def S_20(cv,t):
    a,b=T[20]-.3,E[20]+.3;q=sb(20,1)
    hit=a+1.6;sh=(5*math.sin(t*37)*(1-inn(t,hit+.4,.8))) if hit<t<hit+1.2 else 0
    c=kc(t,[(a,(900,560,1.04)),(b,(1100,560,1.1))],sh)
    ngoai(cv,c,t,g=880,seed=20)
    arrows(cv,c,t,a+.2,hit+.6,[(300,700),(380,690)],[(1300,800),(1450,820)],n=6,h=110,per=1.0,seed=5,col=(.31,.24,.39))
    clash(cv,c,t,hit-1,b+1,'lamap','viet',xm=950,y=780,s=.95,push=-1,seed=13,pre='t17_spr_')
    co=put(cv,c,'t17_spr_vietr',1650,880,s=.0001,o=0)
    truoc(cv,c,t)
    lb(cv,C0,'Phạm Tu',1450,300,t,a+.4,q,col=RED,sz=40);lb(cv,C0,'quân Lâm Ấp',460,300,t,a+.4,q,col=(.31,.24,.39),sz=36)
    lb(cv,C0,'thắng ở Cửu Đức, do chính người của ông đánh',960,170,t,q+.2,b,col=RED,sz=38)
def S_21(cv,t):
    a,b=T[21]-.3,E[21]+.3;q=sb(21,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,480,1.15))])
    ngoai(cv,c,t,g=880,seed=21,mist=.3)
    put(cv,c,'t17x_dien',960,560,s=1.1)
    if not FREEZE:
        for i in range(14):
            x=(i*157+t*40)%2100-100;y=(i*83+t*60)%900
            dot(cv,cam(960,540,1),x,y,o=.45,col=(.85,.55,.5),r=6+(i%3)*2)
    for i in range(3): di(cv,c,'t17_spr_vietr',-600-i*200,880+i*20,300-i*120,880+i*20,t,a+i*.3,b,s=.5,bob=3,f=4.5,ph=i)
    di(cv,c,'t17_spr_viet',2500,880,1700,880,t,a,b,s=.5,bob=3,f=4.6)
    ink_wash(cv,.06*inn(t,a,2),col=np.array((.85,.66,.25),np.float32)) if not FREEZE else None
    truoc(cv,c,t)
    if t>q and not FREEZE: put_screen(cv,wipe(text('VẠN XUÂN',110,RED,700,glow=6),inn(t,q,1.2),0,.3,seed=21),W/2,230)
    lb(cv,C0,'năm 544, Lý Nam Đế, niên hiệu Thiên Đức',960,140,t,a+.3,q-.2,col=RED,sz=40)
def S_22(cv,t):
    a,b=T[22]-.3,E[22]+.3;q=sb(22,1)
    c=kc(t,[(a,(960,520,1.1)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=22,far=.5,midv=.5)
    if t<q+.3 and not FREEZE:
        put(cv,c,'t17x_trieu',960,560,s=1.1)
    else:
        put(cv,c,'t17x_trieu',960,560,s=1.1)
        put(cv,cam(960,540,1),'t17_spr_congnho',360,300,s=.35,o=.6*(1-inn(t,q+1.5,1)))
    for i in range(2): di(cv,c,'t17_spr_1viet',-300-i*200,880,600+i*120,880,t,a+i*.4,b,s=.6,bob=2,f=3.6,ph=i)
    di(cv,c,'t17_spr_1viet',2300,880,1500,880,t,a+.3,b,s=.6,bob=2,f=3.4)
    truoc(cv,c,t)
    lb(cv,C0,'Triệu Túc: chức rất cao trong triều',960,170,t,a+.4,q-.2,col=INK,sz=40)
    lb(cv,C0,'người từng canh cổng thành, nay là quan lớn',960,170,t,q+.2,b,col=RED,sz=40)
def S_23(cv,t):
    a,b=T[23]-.3,E[23]+.3;q=sb(23,1)
    c=kc(t,[(a,(1200,560,1.08)),(b,(800,560,1.0))])
    put(cv,c,'t17_far',960,600,ay=1,k=.35,o=.8)
    river(cv,c,t,PAP,wl=620,stakes=False,cliffs=False,reeds=1,mist=.6,ridge_o=.4,
          boats=[dict(name='t17_spr_thuyen',x=lerp(-300+i*360,900+i*360,inn(t,a-.3,b-a+1)),y=660+i*50+math.sin(t*1.7+i)*6,s=.7+.1*i,r=math.sin(t*1.3+i)*2.5) for i in range(4)])
    if t>q: di(cv,c,'t17_spr_tbt',-300,820,600,820,t,q,b,s=.6,bob=5,f=6,k=1.0)
    lb(cv,C0,'lần thứ ba, năm 545',960,170,t,a+.3,q-.2,col=RED,sz=46)
    lb(cv,C0,'người đi đầu: Trần Bá Tiên',960,170,t,q+.2,b,col=INK,sz=42)
def S_24(cv,t):
    a,b=T[24]-.3,E[24]+.3;q=sb(24,1)
    hit=a+1.2;sh=(5*math.sin(t*37)*(1-inn(t,hit+.4,.8))) if hit<t<hit+1.2 else 0
    c=kc(t,[(a,(1000,560,1.05)),(b,(1300,560,1.1))],sh)
    ngoai(cv,c,t,g=880,seed=23,mist=.6)
    arrows(cv,c,t,a,hit+.6,[(300,700),(380,690)],[(1300,800),(1450,820)],n=8,h=110,per=.9,seed=6,col=(.17,.29,.45))
    clash(cv,c,t,hit-1,b+1,'luong','viet',xm=1000,y=780,s=.95,push=1,seed=14,pre='t17_spr_')
    for k in range(int((b-hit)/1.1)+1):
        t0=hit+.4+k*1.1
        if t0<t<t0+1.8: fall(cv,c,'t17_spr_1viet',1250+k*60,880,t,t0,s=.9,dirn=1)
    truoc(cv,c,t)
    lb(cv,C0,'Chu Diên, cửa sông Tô Lịch',960,170,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'ba vạn quân',1450,300,t,a+.4,q,col=RED,sz=34);lb(cv,C0,'quân nhà Lương',460,300,t,a+.4,q,col=(.17,.29,.45),sz=34)
    lb(cv,C0,'lui về giữ thành Gia Ninh',960,170,t,q+.2,b,col=RED,sz=42)
def S_25(cv,t):
    a,b=T[25]-.3,E[25]+.3;q=sb(25,1)
    c=kc(t,[(a,(800,600,1.0)),(b,(1300,420,1.12))])
    ngoai(cv,c,t,g=880,seed=24,mist=.8,far=.7)
    put(cv,c,'t17x_nui',960,560,s=1.0)
    for i in range(3): di(cv,c,'t17_spr_vietr',-400-i*250,900-i*10,900+i*200,700-i*60,t,a+i*.3,b,s=.5-.05*i,bob=3,f=4.2+i*.3,ph=i)
    if t>q: put(cv,c,'t17_spr_tqp',1350,640,s=.75,ay=1,o=inn(t,q,.6),r=1.2*math.sin(t*1.4))
    truoc(cv,c,t)
    lb(cv,C0,'mất Gia Ninh, rút lên động Khuất Lão',960,170,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'giao Triệu Quang Phục việc giữ nước',960,170,t,q+.2,b,col=RED,sz=40)
def S_26(cv,t):
    a,b=T[26]-.3,E[26]+.3;q=sb(26,1)
    c=canh_dong(cv,t,a,b+3,keys=[(a,(980,760,1.55)),(b+3,(980,780,1.7))])
    khidoc(cv,c,t,-400,640,900,n=4,s=1.6,o=.8,sp=34,seed=12)
    ink_wash(cv,.18*inn(t,q,2.5))
    lb(cv,C0,'khí độc quay lại',960,170,t,a+.4,q-.2,col=INK,sz=44)
    lb(cv,C0,'theo sử ta: ốm nhiều ngày, mất năm 548',960,170,t,q+.2,b,col=RED,sz=40)
def S_27(cv,t):
    a,b=T[27]-.3,E[27]+.3
    canh_dong(cv,t,a-8,b,push=False);ink_wash(cv,.6)
    c=cam(960,540,1.0)
    for x,tt,lines,act in ((540,'SỬ TA',_L,.75),(1380,'SỬ PHƯƠNG BẮC',_R,.75)):
        put(cv,c,'t17_spr_cuon',x,500,s=.95,o=.9,r=.6*math.sin(t*.7+x))
        if not FREEZE:
            put_screen(cv,text(tt,40,RED,700),x,200,act)
            for k,ln in enumerate(lines): put_screen(cv,text(ln,36,INK,600),x,330+k*90,act)
    if not FREEZE: put_screen(cv,text('?',160,RED,700),960,500,inn(t,a+1.5,.6)*(.8+.2*math.sin(t*2)))
    khidoc(cv,c,t,200,780,700,n=2,s=.8,o=.5,sp=20,seed=13)
    lb(cv,C0,'hai cách chép, chưa có gì để phân xử',960,120,t,a+.6,b,col=INK,sz=40)
def S_28(cv,t):
    a,b=T[28]-.3,E[28]+.3
    c=kc(t,[(a,(1300,560,1.08)),(b,(800,560,1.0))])
    put(cv,c,'t17_far',960,620,ay=1,k=.35,o=.7)
    river(cv,c,t,PAP,wl=640,stakes=False,cliffs=False,reeds=1,mist=.8,ridge_o=.3)
    put(cv,c,'t17x_dam',960,520,s=1.0,o=.9)
    for i in range(3): di(cv,c,'t17_spr_tqp',300+i*400,820+i*20,600+i*420,800+i*20,t,a+i*.4,b,s=.5,bob=3,f=2.5,ph=i,k=1.0) if i==0 else di(cv,c,'t17_spr_vietr',-400-i*200,840+i*20,300+i*200,840+i*20,t,a+i*.4,b,s=.5,bob=3,f=4,ph=i)
    lb(cv,C0,'nước không mất theo ông',960,170,t,a+.3,b,col=RED,sz=46)
def S_29(cv,t):
    a=T[29]-.3;b=E[29]+4
    c=kc(t,[(a,(900,560,1.06)),(b,(1100,520,1.0))])
    ngoai(cv,c,t,g=880,seed=25,mist=.6)
    put(cv,c,'t17x_cuoi',960,560,s=1.0)
    khidoc(cv,c,t,200,620,900,n=3,s=1.4,o=.5*(1-inn(t,a+2,b-a-2)),sp=30,seed=14,k=.8)
    for i in range(2): di(cv,c,'t17_spr_vietr',-400-i*200,880+i*20,800-i*200,880+i*20,t,a+i*.4,b,s=.5,bob=3,f=4,ph=i)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    tx=text('Lý Nam Đế, 541–548',54,INK,700);put_screen(cv,wipe(tx,inn(t,a+.8,1.4),0,.3,seed=13),W/2,170)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,245,inn(t,E[29]+.6,1))
if FREEZE:
    lb=lambda *a,**k:None
    big=lambda *a,**k:None
    flock=lambda *a,**k:None
    seal=lambda *a,**k:None
S=lambda n:T[n]-.3
SH=[(0,S(2),S_1)]+[(S(n),S(n+1),globals()[f'S_{n}']) for n in range(2,29)]+[(S(29),V.TOTAL+1,S_29)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm17_full.json'))
SENT={}
for _i,_d in enumerate(_J):
    _hs=[x for x in re.split(r'(?<=[.!?])\s+',_d['hien']) if x.strip()]
    SENT[_i+1]=_hs if len(_hs)==len(_SC[_i+1])-1 else [_d['hien']]
def caps(cv,t):
    for n,hs in SENT.items():
        for k,h in enumerate(hs):
            a=sb(n,k) if len(hs)>1 else T[n];b=sb(n,k+1) if len(hs)>1 else E[n]
            if a-.2<t<b+.05: caption(cv,h,inn(t,a-.15,.15)*(1-inn(t,b-.15,.15)),False)
def ov(cv,t):
    if FREEZE: return
    dem(cv,t)
    caps(cv,t)
V.NHAN={}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
