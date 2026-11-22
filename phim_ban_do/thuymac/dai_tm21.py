# Bản dài tm21: Ba đời họ Khúc, năm 905–930 (lời kể bản 2). Điểm nhấn: chiếc tiết việt (cờ tiết, búa việt) đổi tay qua ba đời.
# Nhân vật chính KHÔNG dùng dáng lính: t21n_thuadu / hao / thuamy là người mặc áo bào dài, mũ khác nhau, cầm tiết (quan21 trong assets.html).
# Tranh nền không vẽ người; mọi người là sprite đặt chỗ riêng để không chồng nhau. Mỗi lúc chỉ một nhãn ở dải trên (y=150),
# bảng chữ phụ đặt ở khối phải (x≈1450, y 260–420), không đè nhãn tên góc trái và không đè người.
import math,re,json,os
import numpy as np
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from engine import ragged,asc
from fx_tran import arrows,dust,sparks,fall
from tran_fx import clash
from dai_tm2 import big,lb
V=K.setup('tm21',{3:4.0})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
FREEZE=bool(os.environ.get('KIEM_TINH'))
NANG=bool(os.environ.get('NANG'))   # bản thử màu và chuyển động (chờ duyệt)
DOC=False   # bản dọc: tắt các bảng chữ đặt ngang ở mép khung
GS=1.45
DUONGC=(.17,.29,.45)
GOLDC=(.79,.64,.35)
NAU=np.array((.55,.42,.27),np.float32)
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
def suong(cv,c,t,y=560,o=.5,seed=0):
    if FREEZE: return
    for i,(sp,k,yy,s) in enumerate([(22,.5,y-120,2.2),(34,1.1,y+120,2.6)]):
        x=(300+seed*400+i*900+t*sp)%2800-400;put(cv,c,'mist',x,yy,s=s,o=o*(.8 if i else 1),k=k)
def ngoai(cv,c,t,g=900,far=.9,midv=.85,mist=.5,seed=0):
    put(cv,c,'t21_far',960+(seed%7-3)*60,g-120,ay=1,k=.35,o=far)   # lớp xa rộng 3000 px: lệch tối đa 180 px để mép lớp không lọt vào khung
    put(cv,c,'t21_mid',960-(seed%5-2)*40,g+30,ay=1,k=.62,o=midv)
    suong(cv,c,t,g-260,mist,seed)
def truoc(cv,c,t,o=1):
    put(cv,c,'t21_frontL',-120,1120,ax=0,ay=1,k=1.3,s=.85,r=1.2*math.sin(t*.8),o=o)
    put(cv,c,'t21_frontR',2040,1120,ax=1,ay=1,k=1.3,s=.8,r=1.2*math.sin(t*.7+1),o=o)
QUAN=('t21n_thuadu','t21n_hao','t21n_hao2','t21n_thuamy','t21n_thuamy2','t21n_luuan','t21n_luunham','t21n_tangcon','t21n_sulu','t21n_lytien')
def hinh(name,t,flip,ph=0.0):
    """nhân vật chính (áo bào): tà áo và tua cờ tiết bay theo gió khi bật NANG"""
    if NANG and not FREEZE and name in QUAN:
        import mau21;im=mau21.gio(A(name),t,ph);return np.ascontiguousarray(im[:,::-1]) if flip else im
    return Af(name) if flip else name
def di(cv,c,name,x0,y0,x1,y1,t,a,b,s=1.0,o=.97,bob=4,f=5,ph=0,k=1.0,r=0,lac=1.2,lat=False):
    if y0>700 and k==1.0: s*=GS;bob*=GS
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;y=y0+(y1-y0)*u-abs(math.sin(t*f+ph))*bob*(1 if 0<u<1 else .3)
    put(cv,c,hinh(name,t,lat,ph+x0*.01),x,y,s=s,o=o,k=k,r=r+lac*math.sin(t*f*.5+ph),ay=1,scale_px=asc(name))
    return x,y
def nv(cv,c,name,x,y,t,s=.7,r=0,o=1.0,flip=False):
    th=(1+.007*math.sin(t*1.7+x)) if NANG and name in QUAN else 1.0   # thở nhẹ
    put(cv,c,hinh(name,t,flip,x*.01),x,y-2*math.sin(t*1.6+x),s=(s*GS if y>700 else s)*th,ay=1,o=o,r=r+.6*math.sin(t*1.1+x),scale_px=asc(name))
def flick(cv,c,x,y,t,s=1.0):
    put(cv,c,'t12_spr_lua',x+6*math.sin(t*7),y,s=min(s,.38)*(1+.08*math.sin(t*9)),o=.5+.3*math.sin(t*5)**2)
def smoke(cv,c,x,y,t,s=1.0):
    for k in range(2): put(cv,c,'t12_spr_khoi',x+20*math.sin(t*.7+k),y-((t*40+k*120)%240),s=s,o=.5*(1-((t*40+k*120)%240)/240))
def duoc_lua(cv,c,pts,t):
    for i,(x,y) in enumerate(pts): flick(cv,c,x,y,t+i*.7,.28)
def dem(cv,o=.3):
    if not FREEZE: ink_wash(cv,o,col=np.array((.1,.1,.18),np.float32))
_NZ=None
def nz():
    global _NZ
    if _NZ is None:
        rg=np.random.default_rng(20);a=rg.random((34,60)).astype(np.float32)
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
def mau(cv,dem=False,bd=False):
    if NANG and not FREEZE:
        import mau21
        if bd: mau21.to_mau_bd(cv)
        else: mau21.to_mau(cv,dem=dem)
def bui(cv,t):
    if NANG and not FREEZE:
        import mau21;mau21.bui(cv,t)
def tiet(cv,x,y,t,rot=0.0,s=.5,o=1.0):
    """hình ảnh lặp lại: chiếc tiết (cờ tiết) của chức tiết độ sứ"""
    put(cv,C0,'t21_tiet',x,y,s=s,o=o,r=rot+1.5*math.sin(t*1.3))
def cuon(cv,x,y,t,tieu,chu,col=None,o=1.0,s=.62,sz=46,u=1.0,gach=0.0,glow=0.0):
    put(cv,C0,'t21_cuon',x,y,s=s,o=o,r=.5*math.sin(t*.7+x))
    if FREEZE: return
    if glow>0: put_screen(cv,band(int(500*s/.62),int(620*s/.62),GOLDC,.25*glow,40),x,y,o)
    put_screen(cv,text(tieu,28,INK,700),x,y-170*s/.62,o)
    for k,ln in enumerate(chu.split('|')): put_screen(cv,wipe(text(ln,sz,col if col is not None else RED,700),u,0,.25,seed=int(x)+k),x,y-40+k*(sz+16),o)
    if gach>0: stroke(cv,C0,[(x-150*s/.62,y+10),(x+150*s/.62,y-20)],gach,wid=10,col=RED,o=.9*o,head=False)
def dot_dem(cv,x,y,n,tong,cot=8,col=RED,o=1.0,gap=46,r=15):
    for k in range(tong): dot(cv,C0,x+(k%cot)*gap,y+(k//cot)*gap,o=o*(.95 if k<n else .25),col=col if k<n else INK,r=r)
def pulse(cv,c,x,y,t,col=RED):
    for k in range(2):
        u=((t*.6+k*.5)%1.0);dot(cv,c,x,y,o=.6*(1-u),col=col,r=int(8+40*u))
def o_dem(cv,x,y,n,tong,nhan,t,o=1.0):
    """bộ đếm ô triện: n ô đã đóng"""
    put_screen(cv,band(70*tong+80,170,PAPER,.88,18),x,y,o)
    put_screen(cv,text(nhan,30,INK,700),x,y-52,o)
    for k in range(tong):
        xx=x-(tong-1)*35+k*70;on=k<n
        put_screen(cv,band(54,54,RED if on else INK,.85 if on else .2,4),xx,y+18,o)
PT=json.load(open('/tmp/gen/bd/a/map21_pts.json'))
def mapbg(cv,c,u=1.0,o=1.0):
    im=A('map21')
    if u<1: im=wipe(im,u,0,.25,seed=4)
    put(cv,c,im,960,540,o=o,scale_px=1.5)
def mcam(t,keys):
    if FREEZE: t=keys[0][0]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z);return cam(cx,cy,z)

NAMHANC=(.36,.16,.30)
MX0,MY0=480,880   # dải chữ của cảnh bản đồ: góc dưới trái trên đất liền, không đè nhãn Hoàng Sa, thẻ Trường Sa, phụ đề
LUONGC=(.45,.33,.12)
def hs(cv,c,o=1.0):
    """Hoàng Sa trên mọi khung bản đồ có biển phía đông (quy-tac/kiem-tra-lich-su.md); thẻ Trường Sa ở mép dưới phải"""
    pts=[(112.33,16.95),(112.6,16.83),(111.6,16.52),(111.75,16.45),(111.5,16.58)]
    import mapink21_xy as MX
    for lon,lat in pts:
        x,y=MX.xy(lon,lat);dot(cv,c,x,y,o=.9*o,col=INK,r=4)
    x,y=MX.xy(112.0,16.95);tag(cv,c,x,y-6,'Quần đảo Hoàng Sa (Việt Nam)',o=o,sz=26,col=RED)
    tx=text('Trường Sa (Việt Nam) ở phía nam',24,RED,700);xc=1860-tx.shape[1]/2-40
    put_screen(cv,band(tx.shape[1]+90,50,PAPER,.88,12),xc+20,872,o);put_screen(cv,tx,xc,872,o)
    stroke(cv,C0,[(xc+tx.shape[1]/2+30,860),(xc+tx.shape[1]/2+30,890)],o,wid=4,col=RED,o=o)
def mlb(cv,c,s,key,dx,dy,t,a,b,col=INK,sz=34):
    x,y=PT[key];lb(cv,c,s,x+dx,y+dy,t,a,b,col=col,sz=sz)
def panel(cv,t,t0,dong,x=1450,y=300,w=540,col=INK,b=None):
    """bảng chữ ở khối phải; dong=[(chữ, cỡ, màu)]"""
    if FREEZE or t<t0: return
    u=inn(t,t0,.4)*(1-(inn(t,b,.4) if b else 0))
    h=40+sum(d[1]+18 for d in dong)
    put_screen(cv,band(w,h,PAPER,.88,16),x,y,u)
    yy=y-h/2+30
    for d in dong:
        put_screen(cv,text(d[0],d[1],d[2] if len(d)>2 else col,700),x,yy+d[1]/2,u);yy+=d[1]+18
# ---- 1: chiếc tiết rơi như giọt mực; ba đời bước qua; lá cờ từ phương xa, người láng giềng nổi giận
def mo(cv,t,a,b):
    q=sb(1,1)
    c=kc(t,[(a,(900,560,1.08)),(q,(1000,560,1.0)),(b,(1150,560,1.05))])
    ngoai(cv,c,t,g=880,seed=1,mist=.45,far=.7,midv=.6)
    put(cv,c,'t21x_mo',960,560,s=1.0)
    mau(cv)
    for i,(nm,x1) in enumerate((('t21n_thuadu',230),('t21n_hao',530),('t21n_thuamy',830))):   # cùng tốc độ, cách nhau 300 px: không chồng nhau
        di(cv,c,nm,x1-1150,885,x1,885,t,a+.6,q,s=.66,bob=3,f=3.4+i*.2,ph=i)
    if t>q-.2: nv(cv,c,'t21n_luunham',1200,885,t,s=.7,flip=True,o=inn(t,q-.2,.6))
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    return c
def S_1(cv,t):
    a,b=0,E[1]+.3;td=.95;q=sb(1,1)
    sc=PAP.copy();mo(sc,t,a,b)
    if FREEZE: cv[:]=sc;return
    if t<td:
        y=-40+(540+40)*(t/td)**2
        m=loang(960,y,22,6);cv[:]=cv*(1-m)+np.array(INK,np.float32)*m
    else:
        u=inn(t,td,1.6);r=30+u*1300
        m=loang(960,540,r,60);rim=np.clip(loang(960,540,r,60)-loang(960,540,r-70,60),0,1)
        cv[:]=cv*(1-m)+sc*m;cv[:]=cv*(1-rim*.75)+np.array(INK,np.float32)*rim*.75
    big(cv,'BA ĐỜI, KHÔNG MỘT TRẬN LỚN',t,1.7,q-.2,INK,180,76,seed=1)
    big(cv,'MỘT LÁ CỜ XIN TỪ PHƯƠNG XA',t,q+.2,b,RED,180,76,seed=2)
# ---- 2: ba câu hỏi
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3;L=E[2]-T[2]
    c=kc(t,[(a,(800,560,1.06)),(b,(1000,560,1.0))])
    ngoai(cv,c,t,g=880,seed=2,mist=.6,far=.6,midv=.6)
    put(cv,c,'t21x_dau',960,560,s=1.0)
    mau(cv)
    smoke(cv,c,1500,600,t,.4)
    di(cv,c,'t21n_dan',-300,890,350,890,t,a,b,s=.55,bob=2,f=3)
    di(cv,c,'t21n_dan2',2300,890,1900,890,t,a,b,s=.55,bob=2,f=3.4,lat=True)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.22)
    if not FREEZE and not DOC:
        for k,(tt,t0) in enumerate((('lá cờ ấy là gì?',a+.4),('vì sao phải xin?',T[2]+L*.3),('vì sao xin được rồi lại mất đất?',T[2]+L*.55))):
            put_screen(cv,text(tt,44,RED if k==2 else INK,700),1300,300+k*90,inn(t,t0,.4))
# ---- 3: bản đồ: An Nam cuối thế kỷ chín, nhà Đường đã suy
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3;q=sb(3,1)
    c=mcam(t,[(a,(960,540,1.0)),(b,(900,560,1.04))])
    mapbg(cv,c,u=inn(t,a-.2,1.0))
    mau(cv,bd=True)
    hs(cv,c,o=inn(t,a+.3,.5))
    x,y=PT['daila'];pulse(cv,c,x,y,t,col=DUONGC);dot(cv,c,x,y,col=DUONGC,r=12)
    mlb(cv,c,'đất An Nam','daila',0,-40,t,a+.4,b,col=DUONGC)
    xq,yq=PT['quangchau'];dot(cv,c,xq,yq,col=INK,r=9);mlb(cv,c,'Quảng Châu','quangchau',150,70,t,a+.6,b,col=NAMHANC,sz=30)
    for i in range(3):
        u=((t*.07+i/3)%1.0) if not FREEZE else i/3
        put(cv,c,'t21n_1tang',x+30+i*50,y-30-260*u,s=.13,ay=1,scale_px=3,r=3*math.sin(t*6+i),o=.9*(1-u))
    for i in range(2):
        u=((t*.04+i/2)%1.0);put(cv,c,'t21n_thuyen',760+i*240+300*u,620+110*i,s=.2,scale_px=3,r=2*math.sin(t*2+i))
    flock(cv,c,t,.4,y0=650)
    lb(cv,C0,'cuối thế kỷ thứ chín',MX0,MY0,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'nhà Đường cai trị, nhưng đã suy',MX0,MY0,t,q+.2,b,col=DUONGC,sz=38)
# ---- 4: năm 880, quân trong phủ thành nổi loạn, Tăng Cổn bỏ thành chạy
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3;q=sb(4,1);q2=sb(4,2)
    c=kc(t,[(a,(800,560,1.06)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=4,mist=.35,far=.5,midv=.5)
    put(cv,c,'t21x_phudem',960,560,s=1.0)
    mau(cv,dem=True)
    for i in range(3):
        x,y=di(cv,c,'t21n_1tang',-500-i*200,890,140+i*190,890,t,a+i*.3,q,s=.56,bob=4,f=5.6+i*.3,ph=i)
        flick(cv,c,x+40,y-300,t+i,.3)
    x,_=di(cv,c,'t21n_tangcon',1150,885,2400,885,t,q,q2,s=.68,bob=5,f=6)
    if t>q-.1: di(cv,c,'t21n_1tang',1450,890,2700,890,t,q,q2,s=.55,bob=5,f=6.4,ph=2)
    for i in range(3):
        if t>q2+.1: di(cv,c,'t21n_1tang',1250-i*240,890,2600-i*240,890,t,q2+.1,b+2.5,s=.52,bob=3,f=4.4+i*.3,ph=i,o=.97*inn(t,q2+.1+i*.25,.4))
    smoke(cv,c,1050,520,t,.6)
    bui(cv,t)
    truoc(cv,c,t)
    dem(cv,.3)
    seal(cv,'s880',1650,330,a+.5,t,s=.8,r=4)
    lb(cv,C0,'năm 880: quân lính trong phủ thành nổi loạn',960,200,t,a+.3,q-.2,col=RED,sz=40)
    lb(cv,C0,'Tăng Cổn bỏ thành mà chạy',960,200,t,q+.1,q2-.2,col=DUONGC,sz=42)
    lb(cv,C0,'quân vùng biên cũng thường tự ý bỏ về',960,200,t,q2+.1,b,col=INK,sz=40)
# ---- 5: năm 905, viên quan đứng đầu An Nam bị triều Đường rút về
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3;q=sb(5,1)
    c=kc(t,[(a,(700,560,1.08)),(b,(1000,560,1.0))])
    ngoai(cv,c,t,g=880,seed=5,mist=.5,far=.5,midv=.5)
    put(cv,c,'t21x_ben',960,560,s=1.0)
    mau(cv)
    smoke(cv,c,1750,560,t,.4)
    u=inn(t,a+.4,q-a)
    if t<a+.4+(q-a)*.5: di(cv,c,'t21n_sulu',-150,780,520,780,t,a+.2,a+.4+(q-a)*.5,s=.52,bob=3,f=4,k=1.0)
    put(cv,c,'t21n_thuyen',640+1100*inn(t,a+.4+(q-a)*.5,b-a),800-40*inn(t,a+.4+(q-a)*.5,b-a),s=.62-.2*inn(t,a+.4+(q-a)*.5,b-a),scale_px=3,r=2*math.sin(t*2))
    di(cv,c,'t21n_dan',-300,890,300,890,t,a,b,s=.52,bob=2,f=3)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    seal(cv,'s905',1650,330,a+.5,t,s=.8,r=4)
    lb(cv,C0,'hai mươi lăm năm sau, năm 905',960,200,t,a+.3,q-.2,col=RED,sz=42)
    panel(cv,t,q+.1,[('sử chép',28,INK),('ngu đần, không có tài năng gì',36,DUONGC)],x=1450,y=520)
    lb(cv,C0,'bị chính triều Đường rút về',960,200,t,q+.1,b,col=DUONGC,sz=40)
# ---- 6: phủ thành trống
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3;q=sb(6,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.1))])
    ngoai(cv,c,t,g=880,seed=6,far=.4,midv=.4,mist=.4)
    put(cv,c,'t21x_phutrong',960,610,s=.85)
    mau(cv)
    di(cv,c,'t21n_tangcon',700,885,-300,885,t,a+.2,q,s=.66,bob=3,f=4,o=.45,lat=True)
    di(cv,c,'t21n_sulu',1250,885,2300,885,t,a+.4,q,s=.66,bob=3,f=4.2,o=.45)
    for k in range(3): dust(cv,c,500+k*450+60*math.sin(t*.8+k),860,o=.25+.1*math.sin(t*1.5+k),s=.4)
    smoke(cv,c,960,700,t,.45)
    bui(cv,t)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.2)
    lb(cv,C0,'người bỏ chạy, người bị rút về',960,200,t,a+.3,q-.2,col=DUONGC,sz=42)
    lb(cv,C0,'phủ thành gần như không còn ai đủ sức giữ',960,200,t,q+.1,b,col=RED,sz=40)
# ---- 7: Hồng Châu, Khúc Thừa Dụ được dân suy tôn
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3;q=sb(7,1)
    c=kc(t,[(a,(1200,560,1.06)),(b,(900,560,1.0))])
    ngoai(cv,c,t,g=880,seed=7)
    put(cv,c,'t21x_hongchau',960,560,s=1.0)
    mau(cv)
    for i in range(2): smoke(cv,c,1500+i*300,560,t+i,.45)
    nv(cv,c,'t21n_thuadu',760,885,t,s=.7)
    di(cv,c,'t21n_dan',-300,890,420,890,t,q,q+2.2,s=.55,bob=2,f=3.2,o=1)
    di(cv,c,'t21n_dan2',2300,890,1110,890,t,q+.3,q+2.6,s=.55,bob=2,f=3.4,lat=True)
    di(cv,c,'t21n_dan',2600,890,1420,890,t,q+.7,q+3.0,s=.52,bob=2,f=3.6,ph=1,lat=True)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'Hồng Châu: vùng Hải Dương ngày nay',960,200,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'Cương mục: tính khoan hòa, hay thương người',960,200,t,q+.1,b,col=RED,sz=40)
# ---- 8: tự xưng tiết độ sứ, xin nhà Đường công nhận; năm 906 được thăng thêm chức
def S_8(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,540,1.08))])
    ngoai(cv,c,t,g=880,seed=8,far=.4,midv=.4,mist=.35)
    put(cv,c,'t21x_sanh',960,610,s=.85)
    mau(cv)
    nv(cv,c,'t21n_thuadu',560,885,t,s=.7)
    if t<q: di(cv,c,'t21n_sulu',900,885,2300,885,t,a+.6,q-.2,s=.64,bob=3,f=4)
    else: di(cv,c,'t21n_sulu',2300,885,1560,885,t,q+.2,q+2.4,s=.64,bob=3,f=4,lat=True)
    di(cv,c,'t21n_1ta',-300,890,200,890,t,a,b,s=.5,bob=2,f=3)
    smoke(cv,c,960,640,t,.4)
    bui(cv,t)
    truoc(cv,c,t)
    seal(cv,'s906',1840,330,q+.6,t,s=.75,r=4)
    lb(cv,C0,'tự xưng tiết độ sứ: chức đứng đầu cả vùng',960,200,t,a+.3,sb(8,1)-(sb(8,1)-T[8])*.45,col=RED,sz=38)
    lb(cv,C0,'rồi xin nhà Đường công nhận',960,200,t,sb(8,1)-(sb(8,1)-T[8])*.4,q-.1,col=DUONGC,sz=42)
    lb(cv,C0,'đầu năm 906, nhà Đường thăng thêm một chức',960,200,t,q+.1,b,col=DUONGC,sz=38)
# ---- 9: không một trận đánh; quyền từ chỗ trống và lòng người; cái danh vẫn phải xin
def S_9(cv,t):
    a,b=T[9]-.3,E[9]+.3;q=sb(9,1);q2=sb(9,2)
    c=kc(t,[(a,(800,560,1.04)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=9,mist=.55)
    put(cv,c,'t21x_dong',960,560,s=1.0)
    mau(cv)
    di(cv,c,'t21n_dan',100,890,700,890,t,a,b,s=.52,bob=2,f=3)
    di(cv,c,'t21n_dan2',1900,890,1300,890,t,a+.4,b,s=.52,bob=2,f=3.3,lat=True)
    smoke(cv,c,360,600,t,.4)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    panel(cv,t,q2+.2,[('cái danh để cai quản',30,INK),('phải xin nhà Đường ban',36,DUONGC)],x=1450,y=330)
    lb(cv,C0,'sử không chép một trận đánh nào',960,200,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'quyền đến từ chỗ trống ở phủ thành và lòng người',960,200,t,q+.1,q2-.2,col=RED,sz=38)
    lb(cv,C0,'nhưng cái danh thì vẫn phải xin nhà Đường ban',960,200,t,q2+.1,b,col=DUONGC,sz=38)
# ---- 10: cận cảnh tiết việt (hình ảnh lặp lại)
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3;q=sb(10,1)
    c=kc(t,[(a,(960,560,1.0)),(q,(900,560,1.08)),(b,(860,560,1.14))])
    put(cv,c,'t21_far',960,760,ay=1,k=.35,o=.35)
    put(cv,c,'t21x_bay',960,560,s=1.0)
    for i in range(2): smoke(cv,c,420+i*1100,820,t+i,.5)
    suong(cv,c,t,620,.3,10)
    mau(cv)
    if not FREEZE:
        ink_wash(cv,.1)
        X,Y=c.p(778,600)
        if t>q: put_screen(cv,band(150,360,GOLDC,.22*(.6+.4*math.sin(t*4)),40),X,Y,inn(t,q,.5))
        if not DOC:
            put_screen(cv,text('cờ tiết',40,RED,700),X-200,Y-40,inn(t,a+.6,.4))
            X2,Y2=c.p(1112,560);put_screen(cv,text('búa việt',40,INK,700),X2+200,Y2-40,inn(t,a+1.4,.4))
    lb(cv,C0,'tiết việt: dấu hiệu của quyền cai quản',960,200,t,a+.3,q-.2,col=INK,sz=42)
    big(cv,'HÃY NHỚ LÁ CỜ NÀY',t,q+.1,b,RED,170,70,seed=10)
# ---- 11: năm 907, Khúc Thừa Dụ mất; nhà Đường mất, nhà Lương lên thay
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3;q=sb(11,1)
    c=kc(t,[(a,(960,540,1.08)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=11,far=.4,midv=.4,mist=.4)
    put(cv,c,'t21x_tang',960,610,s=.85)
    mau(cv)
    nv(cv,c,'t21n_hao2',1340,885,t,s=.68,r=-5,flip=True)
    nv(cv,c,'t21n_dan',420,890,t,s=.52,r=-10);nv(cv,c,'t21n_dan2',640,890,t,s=.5,r=-12)
    smoke(cv,c,960,640,t,.5);smoke(cv,c,900,660,t+1.3,.4)
    bui(cv,t)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.18)
    seal(cv,'s907',1840,330,a+.5,t,s=.75,r=4)
    lb(cv,C0,'năm 907, Khúc Thừa Dụ mất',960,200,t,a+.3,q-.2,col=INK,sz=44)
    if not FREEZE and t>q:
        put_screen(cv,text('nhà Đường mất',42,DUONGC,700),730,140,inn(t,q+.1,.4))
        stroke(cv,C0,[(590,132),(870,124)],inn(t,q+.6,.4),wid=6,col=RED,o=.85,head=False)
        stroke(cv,C0,[(905,132),(985,132)],inn(t,q+.8,.3),wid=6,col=INK,o=.85)
        put_screen(cv,text('nhà Lương lên thay',42,LUONGC,700),1200,140,inn(t,q+.9,.4))
# ---- 12: nhà Lương cho Khúc Hạo làm tiết độ sứ (trao tiết)
def S_12(cv,t):
    a,b=T[12]-.3,E[12]+.3;th=T[12]+(E[12]-T[12])*.6
    c=kc(t,[(a,(900,560,1.05)),(b,(1000,560,1.0))])
    ngoai(cv,c,t,g=880,seed=12)
    put(cv,c,'t21x_san',960,560,s=1.0)
    mau(cv)
    x,y=di(cv,c,'t21n_sulu',-200,885,860,885,t,a+.2,th-.3,s=.64,bob=3,f=4)
    if t<th: nv(cv,c,'t21n_hao2',1300,885,t,s=.7,flip=True)
    else: nv(cv,c,'t21n_hao',1300,885,t,s=.7,flip=True)
    di(cv,c,'t21n_1ta',-500,890,480,890,t,a+.5,th,s=.52,bob=3,f=4)
    di(cv,c,'t21n_dan',2400,890,1950,890,t,a,b,s=.5,bob=2,f=3,lat=True)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    if not FREEZE and t<th+.4:
        X,Y=c.p(x+110,y-200) if t<th-.3 else c.p(860+110+(1300-60-970)*inn(t,th-.3,.6),685)
        tiet(cv,X,Y,t,s=.3,o=1-inn(t,th+.1,.3))
    lb(cv,C0,'nhà Lương cho Khúc Hạo làm tiết độ sứ',960,200,t,a+.3,b,col=LUONGC,sz=40)
# ---- 13: bản đồ: cùng năm, Lưu Ẩn ở Quảng Châu kiêm luôn chức ấy
def S_13(cv,t):
    a,b=T[13]-.3,E[13]+.3;L=E[13]-T[13]
    c=mcam(t,[(a,(960,540,1.0)),(b,(960,540,1.03))])
    mapbg(cv,c)
    mau(cv,bd=True)
    hs(cv,c)
    xd,yd=PT['daila'];xq,yq=PT['quangchau']
    pulse(cv,c,xd,yd,t);dot(cv,c,xd,yd,col=RED,r=11);dot(cv,c,xq,yq,col=NAMHANC,r=11)
    if t>T[13]+L*.35: pulse(cv,c,xq,yq,t,col=NAMHANC)
    put(cv,c,'t21n_hao',460,372+2*math.sin(t*1.6),s=.34,ay=1,scale_px=3)
    put(cv,c,'t21n_luuan',1180,252+2*math.sin(t*1.7),s=.34,ay=1,o=inn(t,T[13]+L*.25,.5),scale_px=3)
    mlb(cv,c,'Khúc Hạo · phủ thành','daila',60,130,t,a+.2,b,col=RED,sz=30)
    mlb(cv,c,'Quảng Châu','quangchau',150,70,t,a+.2,b,col=NAMHANC,sz=30)
    lb(cv,c,'Lưu Ẩn',1030,200,t,T[13]+L*.3,b,col=NAMHANC,sz=30)
    if not FREEZE:
        u=inn(t,T[13]+L*.4,L*.45);stroke(cv,c,[(1250,275),(900,300),(xd+60,yd+5)],u,wid=6,col=NAMHANC,o=.8,dash=1)
    for i in range(2):
        u=((t*.04+i/2)%1.0);put(cv,c,'t21n_thuyen',780+i*260+280*u,620+110*i,s=.2,scale_px=3,r=2*math.sin(t*2+i))
    u=((t*.05)%1.0);put(cv,c,'t21n_thuyen',1300+300*u,420,s=.2,scale_px=3,r=2*math.sin(t*2.3))
    lb(cv,C0,'cùng năm: Lưu Ẩn kiêm chức ấy',MX0,MY0,t,a+.3,b,col=NAMHANC,sz=38)
# ---- 14: hai bên mưu đồ lẫn nhau (hai thành hai bờ sông)
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3;L=E[14]-T[14]
    c=kc(t,[(a,(960,560,1.04)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=14,mist=.5)
    put(cv,c,'t21x_doi',960,560,s=1.0)
    mau(cv)
    smoke(cv,c,60,600,t,.4);smoke(cv,c,1860,600,t+1.5,.4)
    nv(cv,c,'t21n_hao',430,885,t,s=.68)
    nv(cv,c,'t21n_luuan',1500,885,t,s=.68,flip=True)
    flock(cv,c,t,.4)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,c,'giữ phủ thành',430,330,t,a+.5,b,col=RED,sz=30)
    lb(cv,c,'giữ Quảng Châu',1500,330,t,a+.5,b,col=NAMHANC,sz=30)
    if not FREEZE:
        stroke(cv,C0,[(620,520),(960,470),(1300,520)],inn(t,T[14]+L*.45,.8),wid=6,col=RED,o=.8,dash=1)
        stroke(cv,C0,[(1300,580),(960,630),(620,580)],inn(t,T[14]+L*.6,.8),wid=6,col=NAMHANC,o=.8,dash=1)
    lb(cv,C0,'Toàn thư: hai bên có ý mưu đồ lẫn nhau',960,200,t,a+.3,b,col=INK,sz=40)
# ---- 15: một chức, hai người
def S_15(cv,t):
    a,b=T[15]-.3,E[15]+.3;q=sb(15,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.08))])
    ngoai(cv,c,t,g=880,seed=15,mist=.6,far=.7,midv=.7)
    mau(cv)
    nv(cv,c,'t21n_hao',560,885,t,s=.7)
    nv(cv,c,'t21n_luuan',1360,885,t,s=.7,flip=True)
    smoke(cv,c,960,600,t,.4)
    di(cv,c,'t21n_dan',2300,890,1800,890,t,a,b,s=.5,bob=2,f=3,lat=True)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    if not FREEZE:
        ink_wash(cv,.15)
        for k,(x,col) in enumerate(((560,RED),(1360,NAMHANC))):
            X,Y=c.p(x,560);put_screen(cv,band(200,420,col,.14*(.6+.4*math.sin(t*3+k)),60),X,Y,inn(t,a+.5+k*.6,.5))
    big(cv,'MỘT CHỨC · HAI NGƯỜI',t,a+.3,q-.1,RED,180,72,seed=15)
    lb(cv,C0,'nay có thêm một người láng giềng cùng nắm',960,200,t,q+.1,b,col=NAMHANC,sz=40)
# ---- 16: đổi hương thành giáp, đặt người thu thuế
def S_16(cv,t):
    a,b=T[16]-.3,E[16]+.3;q=sb(16,1)
    c=kc(t,[(a,(1100,560,1.05)),(b,(900,560,1.0))])
    ngoai(cv,c,t,g=880,seed=16)
    put(cv,c,'t21x_giap',960,560,s=1.0)
    mau(cv)
    nv(cv,c,'t21n_giap',540,890,t,s=.54)
    nv(cv,c,'t21n_giap',1340,890,t,s=.54,flip=True)
    di(cv,c,'t21n_dan',-300,890,280,890,t,q,q+2.4,s=.52,bob=2,f=3.2)
    di(cv,c,'t21n_dan2',2300,890,1600,890,t,q+.4,q+2.8,s=.52,bob=2,f=3.4,lat=True)
    for i in range(2): smoke(cv,c,700+i*900,560,t+i,.4)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'Cương mục: Khúc Hạo đổi các hương thành giáp',960,200,t,a+.3,q-.2,col=INK,sz=38)
    lb(cv,C0,'mỗi giáp: một quản giáp, một phó tri giáp',960,200,t,q+.1,b,col=RED,sz=40)
# ---- 17: sơ đồ: Khúc Hạo đặt người thu thuế ở từng giáp
def S_17(cv,t):
    a,b=T[17]-.3,E[17]+.3;q=sb(17,1)
    c=kc(t,[(a,(960,540,1.0)),(b,(960,540,1.04))])
    put(cv,c,'t21_far',960,980,ay=1,k=.4,o=.35)
    suong(cv,c,t,700,.4,17)
    mau(cv)
    if not FREEZE: ink_wash(cv,.08)
    put(cv,c,'t21n_hao',960,470+2*math.sin(t*1.6),s=.44,ay=1,scale_px=3)
    for k,x in enumerate((520,960,1400)):
        u=inn(t,a+.6+k*.3,.6)
        if not FREEZE: stroke(cv,c,[(960,490),(x,700)],u,wid=5,col=RED,o=.8)
        put(cv,c,'t21n_giap',x,880+2*math.sin(t*1.5+k),s=.4,ay=1,o=u,scale_px=3)
        if u>.9:
            v=((t*.35+k*.33)%1.0);put(cv,c,'t21_cuon',x+(960-x)*v,700-210*v,s=.06,o=.9*math.sin(math.pi*v),r=8*math.sin(t*2+k))
    lb(cv,c,'Khúc Hạo',960,250,t,a+.3,b,col=RED,sz=34)
    lb(cv,C0,'người thu thuế do Khúc Hạo đặt, ở ngay từng giáp',960,200,t,a+.3,q-.2,col=INK,sz=38)
    panel(cv,t,q+.1,[('bộ máy cai quản riêng',36,RED),('chức danh vẫn của phương bắc',30,DUONGC)],x=1500,y=330,w=560)
# ---- 18: năm 917, Lưu Nham lập nước Nam Hán
def S_18(cv,t):
    a,b=T[18]-.3,E[18]+.3;q=sb(18,1)
    c=kc(t,[(a,(960,520,1.1)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=18,far=.4,midv=.4,mist=.35)
    put(cv,c,'t21x_namhan',960,610,s=.85)
    mau(cv)
    nv(cv,c,'t21n_luunham',960,885,t,s=.7)
    nv(cv,c,'t21n_1duong',460,890,t,s=.54);nv(cv,c,'t21n_1duong',1460,890,t,s=.54,flip=True)
    smoke(cv,c,700,640,t,.4);smoke(cv,c,1220,640,t+1,.4)
    bui(cv,t)
    truoc(cv,c,t)
    seal(cv,'s917',1840,330,a+.5,t,s=.75,r=4)
    lb(cv,C0,'năm 917, ở Quảng Châu, Lưu Nham lập nước',960,200,t,a+.3,q-.2,col=NAMHANC,sz=40)
    lb(cv,C0,'sử gọi là Nam Hán: vùng Quảng Đông ngày nay',960,200,t,q+.1,b,col=NAMHANC,sz=38)
# ---- 19: Khúc Thừa Mỹ sang Quảng Châu làm sứ
def S_19(cv,t):
    a,b=T[19]-.3,E[19]+.3;q=sb(19,1)
    c=kc(t,[(a,(800,560,1.05)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=19,mist=.5,far=.4,midv=.3)
    put(cv,c,'t21x_bien',960,560,s=1.0)
    mau(cv)
    u=inn(t,a,b-a);bx=200+900*u;by=790+6*math.sin(t*1.4)
    put(cv,c,'t21n_thuamy2',bx-20,by+14,s=.5,ay=1,scale_px=3)
    put(cv,c,'t21n_thuyen',bx,by,s=1.0,ay=.75,scale_px=3,r=2*math.sin(t*1.4))
    put(cv,c,'t21n_thuyen',bx-520,by+30,s=.6,ay=.75,scale_px=3,r=2*math.sin(t*1.5+1))
    flock(cv,c,t,.5)
    lb(cv,C0,'Khúc Thừa Mỹ sang Quảng Châu làm sứ',960,200,t,a+.3,q-.2,col=RED,sz=40)
    panel(cv,t,q+.1,[('sử chép mục đích',28,INK),('thăm dò thực hư nước Nam Hán',36,NAMHANC)],x=1450,y=330)
# ---- 20: hãy nhớ người sứ ấy và thành Quảng Châu (hình ảnh lặp lại: cổng thành)
def S_20(cv,t):
    a,b=T[20]-.3,E[20]+.3
    c=kc(t,[(a,(900,560,1.0)),(b,(1000,540,1.1))])
    ngoai(cv,c,t,g=880,seed=20,mist=.5)
    put(cv,c,'t21_cong',1260,885,ay=1,s=1.0)
    mau(cv)
    smoke(cv,c,1700,560,t,.4)
    nv(cv,c,'t21n_thuamy2',480,885,t,s=.7)
    di(cv,c,'t21n_1duong',2300,890,1860,890,t,a,b,s=.52,bob=2,f=3,lat=True)
    flock(cv,c,t,.4)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,c,'người sứ',480,330,t,a+.6,b,col=RED,sz=32)
    lb(cv,c,'thành Quảng Châu',1260,300,t,a+1.0,b,col=NAMHANC,sz=32)
    big(cv,'HÃY NHỚ',t,a+.2,b,RED,150,70,seed=20)
# ---- 21: Khúc Hạo mất, Khúc Thừa Mỹ lên thay; năm mất mỗi sách một khác
def S_21(cv,t):
    a,b=T[21]-.3,E[21]+.3;q=sb(21,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(980,540,1.06))])
    ngoai(cv,c,t,g=880,seed=21,mist=.6,far=.6,midv=.6)
    mau(cv)
    if t<a+1.7: nv(cv,c,'t21n_hao2',420,885,t,s=.68,o=1-inn(t,a+.6,1.0))
    di(cv,c,'t21n_thuamy2',-300,885,420,885,t,a+1.4,q-.2,s=.7,bob=3,f=3.6)
    smoke(cv,c,800,620,t,.4)
    di(cv,c,'t21n_dan',2300,890,1900,890,t,a,b,s=.5,bob=2,f=3,lat=True)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.22)
    lb(cv,C0,'Khúc Hạo mất, Khúc Thừa Mỹ lên thay',960,200,t,a+.3,b,col=RED,sz=40)
    if not FREEZE and t>q:
        cuon(cv,1120,470,t,'SÁCH NÀY','năm ?',col=INK,s=.42,sz=50,u=inn(t,q+.2,.6))
        cuon(cv,1580,470,t,'SÁCH KHÁC','năm ?',col=INK,s=.42,sz=50,u=inn(t,q+.8,.6))
# ---- 22: bản đồ: sứ sang kinh đô nhà Lương xin tiết việt; vua Nam Hán nổi giận
def S_22(cv,t):
    a,b=T[22]-.3,E[22]+.3;q=sb(22,1);q2=sb(22,2)
    c=mcam(t,[(a,(960,520,1.12)),(b,(960,520,1.15))])
    mapbg(cv,c)
    mau(cv,bd=True)
    hs(cv,c)
    for i in range(2):
        u=((t*.045+i/2)%1.0);put(cv,c,'t21n_thuyen',820+i*300+260*u,560+120*i,s=.2,scale_px=3,r=2*math.sin(t*2+i))
    xd,yd=PT['daila'];xq,yq=PT['quangchau']
    dot(cv,c,xd,yd,col=RED,r=11);dot(cv,c,xq,yq,col=NAMHANC,r=11)
    mlb(cv,c,'phủ thành','daila',60,130,t,a+.2,b,col=RED,sz=30)
    mlb(cv,c,'Quảng Châu','quangchau',150,70,t,a+.2,b,col=NAMHANC,sz=30)
    path=[(xd+10,yd-20),(820,180),(900,-40)]
    if not FREEZE:
        stroke(cv,c,path,inn(t,a+.4,q-a-.6),wid=7,col=LUONGC,o=.85,dash=1)
        put_screen(cv,text('kinh đô nhà Lương, ở tận phía bắc',30,LUONGC,700),420,44,inn(t,a+.8,.4))
    if t<q: u=inn(t,a+.4,q-a-.6) if not FREEZE else .4;k=min(int(u*2),1);px=path[k][0]+(path[k+1][0]-path[k][0])*(u*2-k);py=path[k][1]+(path[k+1][1]-path[k][1])*(u*2-k)
    else: u=inn(t,q,q2-q) if not FREEZE else .5;px=900+(xd+10-900)*u;py=-40+(yd-20+40)*u
    put(cv,c,'t21n_sulu',px,py+10,s=.26,ay=1,scale_px=3,r=2*math.sin(t*6))
    if t>q and not FREEZE:
        X,Y=c.p(px+50,py-40);tiet(cv,X,Y,t,s=.16)
    if t>q2-.2:
        pulse(cv,c,xq,yq,t,col=NAMHANC)
        put(cv,c,'t21n_luunham',1180,252+2*math.sin(t*1.7),s=.34,ay=1,o=inn(t,q2-.2,.5),scale_px=3)
        lb(cv,c,'vua Nam Hán nổi giận',960,220,t,q2,b,col=NAMHANC,sz=30)
    lb(cv,C0,'xin nhà Lương ban tiết việt',MX0,MY0,t,a+.3,q-.2,col=LUONGC,sz=38)
    lb(cv,C0,'nhà Lương trao cho',MX0,MY0,t,q+.1,q2-.2,col=LUONGC,sz=40)
    lb(cv,C0,'Toàn thư: vua Nam Hán nổi giận',MX0,MY0,t,q2+.1,b,col=NAMHANC,sz=38)
# ---- 23: nơi xa và người ở gần
def S_23(cv,t):
    a,b=T[23]-.3,E[23]+.3;q=sb(23,1);q2=sb(23,2)
    c=kc(t,[(a,(900,560,1.06)),(b,(1000,560,1.0))])
    ngoai(cv,c,t,g=880,seed=23,mist=.45)
    put(cv,c,'t21x_xagan',960,560,s=1.0)
    mau(cv)
    smoke(cv,c,1820,560,t,.4)
    nv(cv,c,'t21n_thuamy',380,885,t,s=.7)
    if t>a+.8: nv(cv,c,'t21n_luunham',1420,885,t,s=.7,flip=True,o=inn(t,a+.8,.5))
    for i in range(2): di(cv,c,'t21n_1duong',2300+i*200,890,1700+i*200,890,t,a+.6+i*.3,b,s=.5,bob=2,f=3.2+i*.3,lat=True)
    flock(cv,c,t,.4,y0=200)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,c,'nơi xa: nhà Lương',800,470,t,a+.4,b,col=LUONGC,sz=30)
    lb(cv,c,'ngay sát bên: Nam Hán',1420,330,t,a+1.0,b,col=NAMHANC,sz=30)
    lb(cv,C0,'sử không chép Khúc Thừa Mỹ tính toán gì',960,200,t,q+.1,q2-.2,col=INK,sz=38)
    if not FREEZE and not DOC:
        put_screen(cv,band(760,70,PAPER,.88,14),960,150,inn(t,q2+.1,.4))
        put_screen(cv,text('xin lá cờ nơi xa, chuốc cơn giận người ở gần',36,RED,700),960,150,inn(t,q2+.1,.4))
# ---- 24: Nam Hán đem quân sang đánh, bắt Khúc Thừa Mỹ
def S_24(cv,t):
    a,b=T[24]-.3,E[24]+.3;q=sb(24,1)
    c=kc(t,[(a,(960,520,1.1)),(b,(960,560,1.0))],3*math.sin(t*30)*(a+1.4<t<q) if not FREEZE else 0)
    ngoai(cv,c,t,g=900,seed=24)
    put(cv,c,'t21x_tran',960,560,s=1.0)
    mau(cv)
    if t<q+.3: clash(cv,c,t,a+.2,q+.3,'ta','duong',xm=960,y=770,s=.62,push=-1,seed=24,pre='t21n_')
    else:
        x0=500;u=inn(t,q+.3,b-q)
        for k,(nm,dx,ss) in enumerate((('t21n_1duong',0,.52),('t21n_thuamy2',240,.66),('t21n_1duong',480,.52))):
            di(cv,c,nm,x0+dx,888,x0+dx+1300,888,t,q+.3,b+1.5,s=ss,bob=3,f=4+k*.2,ph=k)
    for i in range(2): smoke(cv,c,800+i*400,520,t+i,.5)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'vua Nam Hán sai tướng đem quân sang đánh',960,200,t,a+.3,q-.2,col=NAMHANC,sz=40)
    lb(cv,C0,'Khúc Thừa Mỹ bị bắt, đưa về Quảng Châu',960,200,t,q+.1,b,col=RED,sz=40)
# ---- 25: năm 923 hay 930
def S_25(cv,t):
    a,b=T[25]-.3,E[25]+.3;q=sb(25,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.06))])
    ngoai(cv,c,t,g=880,seed=25,mist=.6,far=.5,midv=.5)
    mau(cv)
    di(cv,c,'t21n_dan',-300,890,300,890,t,a,b,s=.52,bob=2,f=3)
    di(cv,c,'t21n_dan2',2300,890,1700,890,t,a,b,s=.52,bob=2,f=3.4,lat=True)
    smoke(cv,c,960,640,t,.4)
    bui(cv,t)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.28)
    lb(cv,C0,'năm nào? các sách chép khác nhau',960,200,t,a+.3,q-.2,col=INK,sz=40)
    cuon(cv,620,480,t,'TOÀN THƯ · CƯƠNG MỤC','923',col=RED,s=.58,sz=64,u=inn(t,q+.1,.6),glow=inn(t,q,.4)*(1-inn(t,q+(E[25]-q)*.5,.4)))
    cuon(cv,1300,480,t,'TƯ TRỊ THÔNG GIÁM','930',col=NAMHANC,s=.58,sz=64,u=inn(t,q+(E[25]-q)*.5,.6),glow=inn(t,q+(E[25]-q)*.5,.4))
# ---- 26: đưa về đúng Quảng Châu, lần này là người bị bắt
def S_26(cv,t):
    a,b=T[26]-.3,E[26]+.3
    c=kc(t,[(a,(800,560,1.04)),(b,(1150,560,1.0))])
    ngoai(cv,c,t,g=880,seed=26,mist=.45)
    put(cv,c,'t21x_vecong',960,560,s=1.0)
    mau(cv)
    u=inn(t,a+.2,b-a-.4);x=-200+1440*u
    o=1-inn(t,b-.9,.6)
    put(cv,c,'t21n_thuamy2',x-10,860+2*math.sin(t*5),s=.56,ay=1,scale_px=3,o=o)
    put(cv,c,'t21n_xetu',x,890,s=.92,ay=1,scale_px=3,r=1.5*math.sin(t*9),o=o)
    put(cv,c,'t21n_ngua',x+400,890,s=.82,ay=1,scale_px=3,r=2*math.sin(t*10),o=o)
    di(cv,c,'t21n_1duong',-560,890,880,890,t,a+.2,b-.2,s=.5,bob=4,f=6)
    for k in range(2): dust(cv,c,x-60+k*80,880,o=.25,s=.3)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,c,'thành Quảng Châu',1460,470,t,a+.4,b,col=NAMHANC,sz=32)
    lb(cv,C0,'từng sang làm sứ, nay là người bị bắt',960,200,t,a+.3,b,col=RED,sz=40)
# ---- 27: Lý Tiến làm thứ sử; lời vua Nam Hán
def S_27(cv,t):
    a,b=T[27]-.3,E[27]+.3;L=E[27]-T[27]
    c=kc(t,[(a,(900,560,1.04)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=27,far=.6,midv=.5,mist=.45)
    mau(cv)
    nv(cv,c,'t21n_luunham',420,885,t,s=.7)
    nv(cv,c,'t21n_lytien',850,885,t,s=.68,r=-6*inn(t,a+.6,.6),flip=True)
    di(cv,c,'t21n_1duong',2300,890,1900,890,t,a,b,s=.5,bob=2,f=3,lat=True)
    smoke(cv,c,1250,620,t,.4)
    flock(cv,c,t,.4)
    bui(cv,t)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.15)
    lb(cv,C0,'Lý Tiến làm thứ sử: quan đứng đầu một châu',960,200,t,a+.3,T[27]+L*.45,col=NAMHANC,sz=38)
    panel(cv,t,T[27]+L*.5,[('vua Nam Hán nói',28,INK),('dân Giao Chỉ hay làm loạn,',34,NAMHANC),('chỉ có thể ràng buộc mà thôi',34,NAMHANC)],x=1440,y=420,w=580)
# ---- 28: Dương Đình Nghệ lấy lại phủ thành năm 931
def S_28(cv,t):
    a,b=T[28]-.3,E[28]+.3;q=sb(28,1);q2=sb(28,2)
    c=kc(t,[(a,(800,560,1.04)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=28,mist=.5)
    put(cv,c,'t21x_aichau',960,560,s=1.0)
    mau(cv)
    x,_=di(cv,c,'t21n_nghe',-200,885,1300,885,t,a+.3,b+.5,s=.66,bob=4,f=5)
    di(cv,c,'t21n_ta',-900,885,600,885,t,a+.3,b+.5,s=.55,bob=4,f=5.6,ph=1)
    di(cv,c,'t21n_ta',-1500,900,0,900,t,a+.5,b+.5,s=.52,bob=4,f=5.9,ph=2)
    for k in range(3): dust(cv,c,x-500-k*200,890,o=.2,s=.3)
    flock(cv,c,t,.4)
    bui(cv,t)
    truoc(cv,c,t)
    seal(cv,'s931',1650,330,q2+.3,t,s=.8,r=4)
    lb(cv,C0,'nhưng họ Khúc vẫn còn người cũ',960,200,t,a+.3,q-.2,col=RED,sz=42)
    lb(cv,C0,'tướng của Khúc Hạo, người Ái Châu: Thanh Hóa ngày nay',960,200,t,q+.1,q2-.2,col=INK,sz=36)
    lb(cv,C0,'năm 931 đem quân lấy lại phủ thành',960,200,t,q2+.1,b,col=RED,sz=40)
# ---- 29: kết: chiếc tiết đặt xuống; năm 939 Ngô Quyền xưng vương
def S_29(cv,t):
    a=T[29]-.3;b=E[29]+4;q=sb(29,1);q2=sb(29,2);q3=sb(29,3)
    c=kc(t,[(a,(900,560,1.06)),(b,(1000,520,1.0))])
    ngoai(cv,c,t,g=880,seed=29,mist=.6)
    put(cv,c,'t21x_cuoi',960,560,s=1.0)
    mau(cv)
    for i,nm in enumerate(('t21n_thuadu','t21n_hao','t21n_thuamy')):
        nv(cv,c,nm,200+i*250,885,t,s=.6,o=(1-inn(t,q2-.4,1.2)*.6))
    di(cv,c,'t21n_dan',1950,890,1450,890,t,a,b,s=.5,bob=2,f=3.2,lat=True)
    di(cv,c,'t21n_dan2',2200,890,1730,890,t,a,b,s=.48,bob=2,f=3.4,lat=True)
    smoke(cv,c,1350,620,t,.4)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    seal(cv,'s939',1300,430,q2+.4,t,s=.8,r=4)
    lb(cv,C0,'ba đời họ Khúc giữ đất mà không cần trận lớn',960,200,t,a+.3,q-.2,col=RED,sz=38)
    lb(cv,C0,'nhưng lá cờ để giữ cái danh vẫn phải xin',960,200,t,q+.1,q2-.2,col=INK,sz=40)
    lb(cv,C0,'năm 939, Ngô Quyền xưng vương',960,200,t,q2+.1,q3-.1,col=RED,sz=42)
    if not FREEZE and t>q3:
        tx=text('Ba đời họ Khúc, năm 905–930',54,INK,700);put_screen(cv,wipe(tx,inn(t,q3,1.4),0,.3,seed=21),W/2,150)
        put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,220,inn(t,E[29]+.6,1))
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
    flock=lambda *a,**k:None
S=lambda n:T[n]-.3
NS=29
SH=[(0 if n==1 else S(n),S(n+1) if n<NS else V.TOTAL+1,globals()[f'S_{n}']) for n in range(1,NS+1)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm21_full.json'))
SENT={}
for _i,_d in enumerate(_J):
    _hs=[x for x in re.split(r'(?<=[.!?])\s+',_d['hien']) if x.strip()]
    SENT[_i+1]=_hs if len(_hs)==len(_SC[_i+1])-1 else [_d['hien']]
def caps(cv,t):
    for n,hs_ in SENT.items():
        for k,h in enumerate(hs_):
            a=sb(n,k) if len(hs_)>1 else T[n];b=sb(n,k+1) if len(hs_)>1 else E[n]
            if a<t<b: caption(cv,h,inn(t,a,.12)*(1-inn(t,b-.12,.12)),False)
NOCAP=False
def ov(cv,t):
    if FREEZE: return
    TT=T[3]
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'BA ĐỜI HỌ KHÚC','stitle21',.55)
    if not NOCAP: caps(cv,t)
V.NHAN={4:'Tăng Cổn – quan nhà Đường đứng đầu An Nam',7:'Khúc Thừa Dụ – họ Khúc ở Hồng Châu',12:'Khúc Hạo – con của Khúc Thừa Dụ',13:'Lưu Ẩn – người đang nắm Quảng Châu',18:'Lưu Nham – em Lưu Ẩn, vua Nam Hán',19:'Khúc Thừa Mỹ – con của Khúc Hạo',27:'Lý Tiến – thứ sử do Nam Hán đặt',28:'Dương Đình Nghệ – tướng của Khúc Hạo'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
