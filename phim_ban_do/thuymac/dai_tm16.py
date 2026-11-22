# Bản dài tm16 (bản 2): Bà Triệu, khung "câu nói nổi tiếng không có trong bộ sử nào". Dựng 20/11/2026 theo chuẩn chi tiết và các cách dựng mới:
# hình ảnh lặp lại = dải giấy chép câu nói của dân gian (mở đầu, đoạn 16, 18, 19) đối lại con voi và áo vàng (việc sử chép thật);
# mở đầu giọt mực loang; quét mực từ yên sang loạn (đoạn 8); hai trang sử chia màn hình; ba ô trống ở đoạn 12.
# mỗi cảnh ghép nhiều lớp (núi xa, đồi giữa, vật chính, cây tiền cảnh, sương hai tầng), ít nhất ba vật chuyển động riêng
# khớp từng câu lời đọc, hình nhỏ vẽ riêng cho tập (t16_spr_*), hai cảnh trọng tâm: ra hàng (đoạn 10) và voi ra trận (đoạn 13).
# Quy ước màu (quy ước hình ảnh): quân Cửu Chân và quân Bà Triệu đỏ son, quân nhà Ngô xanh chàm đội mũ trụ; Bà Triệu áo vàng (Giao Chỉ chí).
import math,re,json,os
import numpy as np
from engine import ragged
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from fx_tran import arrows,dust,sparks,fall
from tran_fx import clash
from dai_tm2 import big,lb
V=K.setup('tm16',{4:4.0})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
P=PTS
FREEZE=bool(os.environ.get('KIEM_TINH'))
GS,DY=1.45,-15
NGO=(.17,.29,.45)
_SC={}
for _n,_t in TX.items():
    _s=[x for x in re.split(r'(?<=[.!?])\s+',_t) if x.strip()];_w=[len(x.split()) for x in _s];_tot=sum(_w);_c=[0]
    for _k in _w: _c.append(_c[-1]+_k/_tot)
    _SC[_n]=_c
def sb(n,k): return T[n]+(E[n]-T[n])*_SC[n][min(k,len(_SC[n])-1)]
def kc(t,keys):
    if FREEZE: t=keys[0][0]
    cx,cy,z=cpath(t,keys);return cam(cx,cy,z)
def mcam(t,keys):
    if FREEZE: t=keys[0][0]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z);return cam(cx,cy,z)
# ---------- lớp nền
def suong(cv,c,t,y=560,o=.5,seed=0):
    if FREEZE: return
    for i,(sp,k,yy,s) in enumerate([(22,.5,y-120,2.2),(34,1.1,y+120,2.6)]):
        x=(300+seed*400+i*900+t*sp)%2800-400;put(cv,c,'mist',x,yy,s=s,o=o*(.8 if i else 1),k=k)
def ngoai(cv,c,t,g=900,far=.9,midv=.85,front=1,mist=.5,seed=0):
    put(cv,c,'t16_far',960+seed*60,g-120,ay=1,k=.35,o=far)
    put(cv,c,'t16_mid',960-seed*40,g+30,ay=1,k=.62,o=midv)
    suong(cv,c,t,g-260,mist,seed)
def truoc(cv,c,t,front=1,y=1120):
    if not front: return
    put(cv,c,'t16_frontL',-120,y,ax=0,ay=1,k=1.3,s=.85,r=1.2*math.sin(t*.8),o=front)
    put(cv,c,'t16_frontR',2040,y,ax=1,ay=1,k=1.3,s=.8,r=1.2*math.sin(t*.7+1),o=front)
def trong(cv,c,t,o=.85):
    put(cv,c,'t16_inback',960,540,k=.5,o=o)
def trong_truoc(cv,c,t):
    put(cv,c,'t16_inL',-60,1100,ax=0,ay=1,k=1.3,s=.72,r=.4*math.sin(t*.6))
    put(cv,c,'t16_inR',1980,1100,ax=1,ay=1,k=1.3,s=.72,r=.4*math.sin(t*.6+2))
def di(cv,c,name,x0,y0,x1,y1,t,a,b,s=1.0,o=.97,bob=4,f=5,ph=0,k=1.0,r=0,lac=1.2):
    """vật đi có nhịp riêng: nhún theo bước (bob, f), lắc nhẹ (lac độ), tốc độ dồn đều theo ease"""
    if y0>700 and k==1.0: s*=GS;y0+=DY;y1+=DY;bob*=GS
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;y=y0+(y1-y0)*u-abs(math.sin(t*f+ph))*bob*(1 if 0<u<1 else .3)
    put(cv,c,name,x,y,s=s,o=o,k=k,r=r+lac*math.sin(t*f*.5+ph),ay=1)
    return x,y
def flick(cv,c,x,y,t,s=1.0):
    put(cv,c,'t12_spr_lua',x+6*math.sin(t*7),y,s=min(s,.38)*(1+.08*math.sin(t*9)),o=.5+.3*math.sin(t*5)**2)
def smoke(cv,c,x,y,t,s=1.0):
    for k in range(2): put(cv,c,'t12_spr_khoi',x+20*math.sin(t*.7+k),y-((t*40+k*120)%240),s=s,o=.5*(1-((t*40+k*120)%240)/240))
def pulse(cv,c,x,y,t,col=RED):
    for k in range(2):
        u=((t*.6+k*.5)%1.0);dot(cv,c,x,y,o=.6*(1-u),col=col,r=int(8+40*u))
def co_bay(cv,c,name,x,y,t,s=1.0,ph=0):
    put(cv,c,name,x,y,s=s,ay=1,r=2.5*math.sin(t*2.2+ph))
def viet(cv,c,pts,t,a,d,wid=5,col=INK,o=.7):
    stroke(cv,c,pts,inn(t,a,d),wid=wid,col=col,o=o,head=False)
def voi(cv,c,x0,y0,x1,y1,t,a,b,s=.8,o=.97,k=0):
    u=inn(t,a,max(b-a,.1));nm=('t16_spr_voi_k' if k else 't16_spr_voi')+('l' if x1<x0 else '')
    nm={'t16_spr_voi_kl':'t16_spr_voi_kl','t16_spr_voil':'t16_spr_voi_l'}.get(nm,nm)
    put(cv,c,nm,x0+(x1-x0)*u,y0+(y1-y0)*u-50-abs(math.sin(t*3.1))*6,s=s*1.25,o=o,r=1.5*math.sin(t*1.55),ay=1) if True else None
    return x0+(x1-x0)*u

_NZ=None
def nz():
    global _NZ
    if _NZ is None:
        rg=np.random.default_rng(16);a=rg.random((34,60)).astype(np.float32)
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
C0=cam(960,540,1.0)
CAU='"cưỡi cơn gió mạnh, đạp luồng sóng dữ"'
def cau_noi(cv,x,y,o=1.0,u=1.0,sz=40,mo=0.0,t=0,trai=0):
    """hình ảnh lặp lại: dải giấy chép câu nói của dân gian; mo>0 thì chữ nhòe dần như khói"""
    if FREEZE or o<=0: return
    yy=y+trai*(-30*mo)+4*math.sin(t*1.1)
    put_screen(cv,band(1180,96,PAPER,.82,26),x,yy,o*(1-.6*mo))
    put_screen(cv,wipe(text(CAU,sz,RED,700),u,0,.25,seed=16),x,yy-2,o*(1-.85*mo))
    if mo>0: put(cv,C0,'mist',x+60*math.sin(t*.7),yy,s=1.5,o=.5*mo)
# ---------- 1: giọt mực loang thành cánh đồng, voi đi tới; câu hỏi lớn
def S_1(cv,t):
    a,b=0,E[1]+.3;td=.95
    sc=PAP.copy()
    c=kc(t,[(a,(1150,560,1.08)),(b,(950,560,1.0))])
    ngoai(sc,c,t,g=880,seed=1)
    put(sc,c,'t16x_voi1',960,560,s=1.0,o=.6)
    voi(sc,c,-500,920,520,920,t,.6,b,s=.95)
    for i in range(2): di(sc,c,'t16_spr_cc',-800+i*140,900+i*30,100+i*140,900+i*30,t,1.0+i*.3,b,s=.6,bob=5,f=6+i,ph=i)
    di(sc,c,'t16_spr_dan',1500,880,2300,860,t,a,b+2,s=.65,bob=3,f=4.4)
    flock(sc,c,t,.6)
    truoc(sc,c,t)
    if FREEZE: cv[:]=sc;return
    if t<td:
        y=-40+(540+40)*(t/td)**2
        m=loang(960,y,22,6);cv[:]=cv*(1-m)+np.array(INK,np.float32)*m
    else:
        u=inn(t,td,1.6);r=30+u*1300
        m=loang(960,540,r,60);rim=np.clip(loang(960,540,r,60)-loang(960,540,r-70,60),0,1)
        cv[:]=cv*(1-m)+sc*m;cv[:]=cv*(1-rim*.75)+np.array(INK,np.float32)*rim*.75
    big(cv,'CÂU NÓI KHÔNG CÓ TRONG SỬ',t,1.6,b,RED,120,80,seed=1)
# ---------- 2: hai trang: dân gian kể / Toàn thư, Cương mục không ghi
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3;q=sb(2,1)
    c=kc(t,[(a,(960,560,1.06)),(b,(960,540,1.0))])
    trong(cv,c,t,.5)
    put(cv,c,'t16x_haicot',960,560,s=1.0)
    di(cv,c,'t16_spr_khach',-500,940,180,940,t,a,b,s=.45,bob=2,f=4)
    di(cv,c,'t16_spr_quan',2400,860,1720,860,t,q-.4,b,s=.7,bob=2,f=3.2)
    smoke(cv,c,960,640,t,.7)
    trong_truoc(cv,c,t)
    if not FREEZE:
        put_screen(cv,text('DÂN GIAN KỂ',34,RED,700),560,330,inn(t,a+.3,.4))
        for k,ln in enumerate(['cưỡi cơn gió mạnh,','đạp luồng sóng dữ']):
            put_screen(cv,wipe(text(ln,40,RED,700),inn(t,a+.5+k*.8,.9),0,.25,seed=k),560,450+k*70,1)
        o=inn(t,q-.1,.4)
        put_screen(cv,text('TOÀN THƯ · CƯƠNG MỤC',32,INK,700),1300,330,o)
        if t>q+.6: put_screen(cv,wipe(text('không ghi',52,INK,700),inn(t,q+.6,.6),0,.25,seed=5),1300,500,1)
    lb(cv,C0,'câu nói nhiều người thuộc lòng',960,150,t,a+.3,q-.2,col=INK,sz=40)
# ---------- 3: sử cũ chỉ vài dòng
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3;q=sb(3,1)
    c=kc(t,[(a,(960,520,1.12)),(b,(960,560,1.0))])
    trong(cv,c,t,.6)
    put(cv,c,'t16x_sulien',960,560,s=1.1)
    for j in range(3): viet(cv,c,[(800+j*60,500),(800+j*60,540)],t,a+.6+j*.7,.45,wid=4,o=.85)
    di(cv,c,'t16_spr_khach',-500,920,200,920,t,a,b,s=.55,bob=2,f=4)
    di(cv,c,'t16_spr_quan',2300,860,1650,860,t,a+.5,b,s=.7,bob=2,f=3)
    di(cv,c,'t16_spr_khach',1900,930,1350,930,t,a+.3,b,s=.42,bob=2,f=3.4,ph=2)
    flick(cv,c,1180,500,t,.8);smoke(cv,c,1180,440,t,.7)
    trong_truoc(cv,c,t)
    lb(cv,C0,'sử cũ chép về bà: vài dòng',960,160,t,a+.4,q-.2,col=INK,sz=44)
    lb(cv,C0,'một việc khác hẳn mọi người quanh mình',960,160,t,q+.2,b,col=RED,sz=40)
# ---------- 4: bản đồ: năm 248, Cửu Chân; Giao Châu dưới nhà Ngô
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3;q=sb(4,1)
    dl,th,ng=P['daila'],P['thanhhoa'],P['nghean']
    c=mcam(t,[(a-.3,(700,760,1.35)),(q,(760,740,1.1)),(b,(860,700,1.0))])
    mapbg(cv,c,u=inn(t,a-.4,1.2))
    for nm,p,t0 in (('Cửu Chân',th,a+.4),('Giao Chỉ',dl,q),('Nhật Nam',ng,q+.4)):
        if t>t0: dot(cv,c,*p,o=inn(t,t0,.4));tag(cv,c,p[0]+22,p[1]-6,nm,dy=0,sz=26)
    pulse(cv,c,*th,t)
    if t>q: stroke(cv,c,[(dl[0]+500,dl[1]-300),(dl[0]+200,dl[1]-120),dl],inn(t,q,2.5),wid=8,col=NGO)
    di(cv,c,'t16_spr_ngua',dl[0]+360,dl[1]-260,dl[0]+80,dl[1]-40,t,q,b,s=.25,bob=2,f=7)
    di(cv,c,'t16_spr_ngo',dl[0]+520,dl[1]-200,dl[0]+160,dl[1]+10,t,q+.5,b,s=.18,bob=1,f=6)
    for i in range(3): di(cv,c,'t16_spr_1cc',th[0]-60+i*40,th[1]+30,th[0]-40+i*40,th[1]+30,t,a,b,s=.14,bob=2,f=5+i,ph=i)
    seal(cv,'s248',1560,330,a+.6,t,s=.8,r=4)
    lb(cv,C0,'Cửu Chân, nay là Thanh Hóa: rối loạn',960,170,t,a+.3,q-.2,col=RED,sz=40)
    lb(cv,C0,'Giao Châu dưới sự cai trị của nhà Ngô',960,170,t,q+.2,b,col=NGO,sz=40)
# ---------- 5: Lữ Đại hứa tha rồi chém Sĩ Huy
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3;q=sb(5,1)
    c=kc(t,[(a,(960,560,1.0)),(q,(960,560,1.08)),(b,(900,520,1.2))])
    ngoai(cv,c,t,g=880,seed=3)
    put(cv,c,'t16x_luudai',960,560,s=1.1)
    di(cv,c,'t16_spr_ngo',-500,880,140,880,t,a,q,s=.62,bob=3,f=5)
    di(cv,c,'t16_spr_ngo',2400,890,1780,890,t,a+.4,q,s=.6,bob=3,f=5.4,ph=1)
    for i in range(3): di(cv,c,'t16_spr_quy',760+i*150,900,760+i*150,912,t,q+.4+i*.5,b,s=.55,bob=0,lac=.8,ph=i)
    if t>sb(5,1)+(b-q)*.6:
        t0=q+(b-q)*.6;v=inn(t,t0,1.6);put(cv,c,'redblot',960,760,s=.8+1.0*v,o=.38*v,r=18*v);ink_wash(cv,.22*v)
    truoc(cv,c,t)
    lb(cv,C0,'lời hứa của nhà Ngô đáng giá thế nào?',960,170,t,a+.4,q-.2,col=INK,sz=40)
    lb(cv,C0,'Lữ Đại hứa tha Sĩ Huy, rồi chém',960,170,t,q+.2,b,col=RED,sz=44)
# ---------- 6: Lục Dận sang, gửi lời kêu gọi
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3;q=sb(6,1)
    c=kc(t,[(a,(1200,560,1.1)),(b,(800,560,1.0))])
    put(cv,c,'t16_far',960,560,ay=1,k=.35,o=.8)
    river(cv,c,t,PAP,wl=600,stakes=False,cliffs=False,reeds=1,mist=.8,ridge_o=.0,
          boats=[dict(name='t16_spr_thuyenlon',x=lerp(-200+i*330,900+i*330,inn(t,a-.3,b-a)),y=640+i*60+math.sin(t*1.8+i)*6,s=.55+.12*i,r=math.sin(t*1.4+i)*2.5) for i in range(3)])
    put(cv,c,'t16x_lucdan',960,600,s=1.0,o=.55)
    for i in range(2): di(cv,c,'t16_spr_thuyen',2100-i*400,560+i*20,1500-i*400,560+i*20,t,a,b,s=.4,bob=4,f=1.6,ph=i,k=.7,lac=3)
    if not FREEZE and t>q:
        for k in range(5):
            u=inn(t,q+k*.35,1.6)
            put_screen(cv,band(150,60,PAPER,.85,10),lerp(980,250+k*360,u),lerp(560,300,u),u*(1-inn(t,b-.6,.5)))
    flock(cv,c,t,.6)
    lb(cv,C0,'nhà Ngô cử Lục Dận sang',960,170,t,a+.4,q-.2,col=NGO,sz=44)
    lb(cv,C0,'hứa khoan dung, giữ chữ tín',960,170,t,q+.2,b,col=INK,sz=42)
# ---------- 7: CẢNH TRỌNG TÂM: ra hàng (bộ đếm số nhà)
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3;q1,q2=sb(7,1),sb(7,1)+(E[7]-sb(7,1))*.55
    c=kc(t,[(a,(1300,560,1.12)),(q1,(1100,560,1.04)),(q2,(900,560,1.0)),(b,(760,520,1.06))])
    ngoai(cv,c,t,g=880,seed=5)
    put(cv,c,'t16x_rahang',960,560,s=1.1)
    n=int(10+12*inn(t,q1,b-q1))
    for i in range(n):
        ln=i%3;t0=a+i*.4;yv=830+ln*40;sc=.5+ln*.08
        if t<t0: continue
        u=(t-t0)/5.0
        if u<1: di(cv,c,['t16_spr_dan','t16_spr_dan2','t16_spr_dan'][ln],-200+ln*80,yv,1080-ln*40,yv,t,t0,t0+5,s=sc,bob=3,f=4.5+ln*.5,ph=i)
        elif u<1.25: put(cv,c,'t16_spr_quy',1150-ln*40,yv+DY,s=sc*.9*GS,ay=1,r=2*math.sin(t*2+i))
    pile=inn(t,a+2,b-a-2)
    for j in range(int(1+pile*6)): put(cv,c,'t16_spr_dau',1060+j*44,860-pile*10*(j%2),s=.6+pile*.35,ay=1,o=.9)
    co_bay(cv,c,'t16_spr_ngo1',1640,860,t,1.0);co_bay(cv,c,'t16_spr_ngo1',1780,875,t,1.0,1)
    truoc(cv,c,t)
    lb(cv,C0,'và phần lớn đã nhận lời',960,160,t,a+.4,q1-.2,col=INK,sz=42)
    if not FREEZE and t>q1-.1:
        nn=int(30000*inn(t,q1,2.2));put_screen(cv,text('Toàn thư: hơn '+f'{nn:,}'.replace(',','.')+' nhà ra hàng',46,RED,700),W/2,170,inn(t,q1-.1,.4)*(1-inn(t,q2-.5,.35)))
    if not FREEZE and t>q2-.1:
        put_screen(cv,text('sử nhà Ngô: hơn 50.000 nhà, hơn 100 thủ lĩnh',42,INK,700),W/2,170,inn(t,q2,.4))
# ---------- 8: vừa yên → quét mực → bà nổi dậy, đánh trụ sở
def yen(cv,t,a,b):
    c=kc(t,[(a,(900,560,1.04)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=860,seed=6)
    put(cv,c,'t16x_bovukhi',960,560,s=1.0)
    for i in range(4): di(cv,c,'t16_spr_dan' if i%2 else 't16_spr_dan2',600+i*90,850+(i%2)*30,1900+i*120,820+(i%2)*30,t,a+i*.6,b+2,s=.62,bob=3,f=4.6+i*.2,ph=i)
    for x in (2100,2480): smoke(cv,c,x,560,t,1.0)
    truoc(cv,c,t)
def danh(cv,t,a,b):
    c=kc(t,[(a,(960,540,1.0)),(b,(1100,600,1.16))])
    ngoai(cv,c,t,g=870,seed=2)
    put(cv,c,'t16x_trusoo',960,560,s=1.1)
    for i in range(3): di(cv,c,'t16_spr_ngo1',640+i*140,845,620+i*140,845,t,a,b,s=.55,bob=1.5,f=1.2+i*.4,ph=i,lac=.6)
    for i in range(3): di(cv,c,'t16_spr_cc',2300+i*160,880+i*20,1500+i*120,880+i*20,t,a+i*.3,a+2,s=.62,bob=5,f=6.4+i*.5,ph=i)
    if t>a+1.5: clash(cv,c,t,a+1.5,b+1,'ngo','cc',xm=960,y=790,s=0.9,push=-1,seed=3,pre='t16_spr_')
    if t>a+2.5:
        for x in (720,1180): flick(cv,c,x,420,t,s=1.3*inn(t,a+2.5,1.5));smoke(cv,c,x,360,t,s=1.2)
    truoc(cv,c,t)
def S_8(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1)
    if FREEZE or t<q-.6: yen(cv,t,a,q+1)
    elif t<q+.6:
        A_=PAP.copy();yen(A_,t,a,q+1);B_=PAP.copy();danh(B_,t,q-.6,b)
        m=quet(inn(t,q-.6,1.1));cv[:]=A_*(1-m)+B_*m
    else: danh(cv,t,q-.6,b)
    lb(cv,C0,'cả vùng vừa yên trở lại',960,170,t,a+.4,q-.5,col=INK,sz=42)
    lb(cv,C0,'một người phụ nữ họ Triệu ở Cửu Chân',960,170,t,q+.4,b,col=RED,sz=40)
def S_8b(cv,t): danh(cv,t,sb(8,1)-.6,E[8]+.3)
# ---------- 9: thứ tự: người ra hàng đi một chiều, voi của bà đi chiều ngược lại
def S_9(cv,t):
    a,b=T[9]-.3,E[9]+.3;q=sb(9,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.1))])
    ngoai(cv,c,t,g=880,seed=10)
    put(cv,c,'t16x_thutu',960,560,s=1.1)
    for i in range(4): di(cv,c,'t16_spr_dan' if i%2 else 't16_spr_dan2',900-i*60,850+i*20,-500-i*200,850+i*20,t,a+i*.5,b,s=.62,bob=3,f=4.4+i*.3,ph=i)
    voi(cv,c,2300,880,1300,880,t,q,b,s=.85)
    di(cv,c,'t16_spr_cc',2700,900,1700,900,t,q+.4,b,s=.55,bob=5,f=6.5)
    truoc(cv,c,t)
    lb(cv,C0,'mọi người bỏ vũ khí xuống',560,250,t,a+.4,b,col=INK,sz=36)
    lb(cv,C0,'bà đứng lên',1450,250,t,q+.2,b,col=RED,sz=40)
    lb(cv,C0,'thứ tự ấy mới là điều đáng nói',960,160,t,a+.3,b,col=RED,sz=42)
# ---------- 10: sử không chép vì sao; bà đã chọn khác (cận cảnh)
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3;q=sb(10,1)
    c=kc(t,[(a,(960,600,1.0)),(q,(900,520,1.18)),(b,(880,500,1.26))])
    ngoai(cv,c,t,g=880,seed=7)
    put(cv,c,'t16x_noilen',960,560,s=1.1)
    for i in range(3):
        di(cv,c,'t16_spr_cc',-900+i*100,890+i*24,-80+i*120,890+i*24,t,q-1+i*.4,b,s=.55+.04*i,bob=5,f=6+i*.5,ph=i)
        di(cv,c,'t16_spr_1cc',2400+i*90,880+i*24,1500+i*80,880+i*24,t,q-.5+i*.3,b,s=.6,bob=5,f=6.3+i*.4,ph=i+3)
    truoc(cv,c,t)
    lb(cv,C0,'sử không chép vì sao',960,160,t,a+.4,q-.2,col=INK,sz=44)
    lb(cv,C0,'chỉ biết chắc: bà đã chọn khác',960,160,t,q+.2,b,col=RED,sz=44)
# ---------- 11: CẢNH TRỌNG TÂM: cưỡi voi ra trận, áo vải vàng
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3;q=sb(11,1)
    hit=a+3.0
    sh=(6*math.sin(t*37)*(1-inn(t,hit+.4,.8))) if hit<t<hit+1.2 and not FREEZE else 0
    keys=[(a,(1300,600,1.0)),(hit,(1050,600,1.04)),(q,(1150,560,1.08)),(b,(1300,470,1.3))]
    cx,cy,z=cpath(t,keys) if not FREEZE else (1050,600,1.0);c=cam(cx,cy,z,sh,sh)
    ngoai(cv,c,t,g=880,seed=8,mist=.35)
    put(cv,c,'t16x_voi2',960,560,s=1.0,o=.7)
    lui=inn(t,hit,b-hit)*240
    for r in range(3): put(cv,c,'t16_spr_ngo',260-r*170-lui,850+r*30,s=.95+.06*r,ay=1,r=(2 if t>hit else 0)*math.sin(t*9+r))
    arrows(cv,c,t,a+.4,hit+1,[(300,700),(420,690)],[(1150,780),(1300,800)],n=8,h=90,per=1.0,seed=3,col=NGO)
    xv=voi(cv,c,2200,900,820,880,t,a,hit+.3,s=1.0)
    if t>hit-1:
        for k in range(4): put(cv,c,'mist',xv+240+k*120,840-20*k,s=.5+.15*k+.2*inn(t,hit,1),o=.35*(1-inn(t,hit+3,2)),k=1.0)
    for r in range(3): di(cv,c,'t16_spr_cc',2500+r*200,900+r*34,980+r*160-lui*.3,900+r*34,t,a+.5+r*.35,hit+1.2+r*.3,s=.6+.05*r,bob=6,f=7+r,ph=r)
    co_bay(cv,c,'t16_spr_ccco',xv+160,860,t,1.2)
    if t>hit:
        sparks(cv,c,t,[(660+k*40,700-20*math.sin(k)) for k in range(5)],hit,b,seed=8)
        for k in range(int((b-hit)/1.2)+1):
            t0=hit+.3+k*1.2
            if t0<t<t0+1.8: fall(cv,c,'t16_spr_1ngo',560-k*30,860,t,t0,s=.95,dirn=-1)
    truoc(cv,c,t)
    lb(cv,C0,'Toàn thư: bà cưỡi voi ra trận',960,160,t,a+.4,q-.2,col=RED,sz=44)
    lb(cv,C0,'sách cũ: áo vải vàng, ngồi trên lưng voi',960,160,t,q+.2,b,col=INK,sz=40)
    lb(cv,C0,'quân nhà Ngô',380,330,t,a+.6,q,col=NGO,sz=32);lb(cv,C0,'quân của bà',1500,330,t,a+.6,q,col=RED,sz=32)
# ---------- 12: ba ô trống: tên trận, số quân, ngày tháng
def S_12(cv,t):
    a,b=T[12]-.3,E[12]+.3;q=sb(12,1)
    c=kc(t,[(a,(1100,560,1.08)),(b,(860,560,1.0))])
    ngoai(cv,c,t,g=860,seed=4)
    put(cv,c,'t16x_chiemthanh',960,560,s=1.0)
    for x in (1300,760): flick(cv,c,x,360,t,s=1.0);smoke(cv,c,x,300,t,1.2)
    for i in range(3): di(cv,c,'t16_spr_1cc',-300-i*160,880,500+i*140,880,t,a+i*.3,b,s=.6,bob=4,f=5.6+i*.4,ph=i)
    di(cv,c,'t16_spr_ngo',2400,880,1700,880,t,a,b,s=.6,bob=3,f=5,ph=1)
    truoc(cv,c,t)
    if not FREEZE:
        ink_wash(cv,.3*inn(t,q-.3,.8))
        for k,nm in enumerate(['tên trận','số quân','ngày tháng']):
            t0=q+.2+k*((b-q-.6)/3);x=560+k*400
            if t>t0:
                u=inn(t,t0,.35)
                put_screen(cv,band(300,170,PAPER,.9,16),x,520,u)
                put_screen(cv,text(nm,32,INK,700),x,470,u);put_screen(cv,text('?',80,RED,700),x,550,u*(.85+.15*math.sin(t*3+k)))
    lb(cv,C0,'gần như tất cả những gì sử chép',960,170,t,a+.4,q-.2,col=INK,sz=42)
    lb(cv,C0,'sử không ghi',960,330,t,q+.1,b,col=RED,sz=40)
# ---------- 13: Lục Dận dẹp được bà
def S_13(cv,t):
    a,b=T[13]-.3,E[13]+.3;q=sb(13,1)
    c=kc(t,[(a,(900,560,1.0)),(b,(1150,560,1.08))])
    ngoai(cv,c,t,g=880,seed=9,mist=.8)
    put(cv,c,'t16x_dep',960,560,s=1.0)
    clash(cv,c,t,a+.4,q,'ngo','cc',xm=900,y=780,s=0.93,push=1,seed=9,pre='t16_spr_')
    if t>q:
        for i in range(3): di(cv,c,'t16_spr_ngo',300+i*200,860+i*30,1100+i*260,860+i*30,t,q,b,s=.6,bob=3,f=5+i*.4,ph=i)
        u=inn(t,q,2.5);put(cv,c,'t16_spr_ccco',1500,870,s=1.2,ay=1,r=-70*u,o=1-.7*u)
    truoc(cv,c,t)
    lb(cv,C0,'Lục Dận đem quân dẹp được bà',960,160,t,a+.4,q-.2,col=NGO,sz=44)
    lb(cv,C0,'bà mất thế nào: sử không chép',960,160,t,q+.2,b,col=INK,sz=42)
# ---------- 14: thành thần, đền Phú Điền
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3;q=sb(14,1)
    c=kc(t,[(a,(960,500,1.06)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=11)
    put(cv,c,'t16x_den',960,560,s=1.1)
    for i in range(3): smoke(cv,c,900+i*60,610,t+i,.8)
    for i in range(3): di(cv,c,'t16_spr_khach',-400-i*300,900+i*20,500+i*80,900+i*20,t,a+i*.6,b,s=.45,bob=2,f=3.6+i*.3,ph=i)
    flock(cv,c,t,.6)
    truoc(cv,c,t)
    lb(cv,C0,'theo sách cũ: bà thành thần',960,160,t,a+.4,q-.2,col=RED,sz=44)
    lb(cv,C0,'đền ở Phú Điền, nay vùng Hậu Lộc, Thanh Hóa',960,160,t,q+.2,b,col=INK,sz=38)
# ---------- 15: sử gia triều Nguyễn
def S_15(cv,t):
    a,b=T[15]-.3,E[15]+.3
    c=kc(t,[(a,(1000,560,1.0)),(b,(900,540,1.12))])
    trong(cv,c,t,.6)
    put(cv,c,'t16x_sunguyen',960,560,s=1.1)
    for j in range(7): viet(cv,c,[(800+j*50,548),(800+j*50,556)],t,a+.4+j*.5,.4,wid=4,o=.8)
    di(cv,c,'t16_spr_quan',2100,760,1400,760,t,a,b,s=.7,bob=2,f=3)
    di(cv,c,'t16_spr_khach',-500,920,150,920,t,a+.5,b,s=.45,bob=2,f=3.8)
    smoke(cv,c,960,640,t,.8)
    trong_truoc(cv,c,t)
    lb(cv,C0,'sử gia triều Nguyễn: phụ nữ phương nam dũng cảm',960,160,t,a+.3,(a+b)/2,col=INK,sz=38)
    lb(cv,C0,'chỉ đứng sau Hai Bà Trưng',960,160,t,(a+b)/2+.2,b,col=RED,sz=44)
# ---------- 16: câu nói, tên, tuổi, núi Tùng từ đâu? (dải giấy trở lại, bốn mảnh)
_BON=['Triệu Thị Trinh','tuổi hai mươi ba','núi Tùng']
def S_16(cv,t):
    a,b=T[16]-.3,E[16]+.3;q=sb(16,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.08))])
    trong(cv,c,t,.5)
    put(cv,c,'t16x_thu',960,560,s=1.1)
    di(cv,c,'t16_spr_quan',-300,860,420,860,t,a,b,s=.7,bob=2,f=3)
    di(cv,c,'t16_spr_khach',2300,920,1550,920,t,a+.4,b,s=.45,bob=2,f=3.7)
    smoke(cv,c,960,600,t,.7)
    trong_truoc(cv,c,t)
    if not FREEZE:
        ink_wash(cv,.35*inn(t,a,.6))
        cau_noi(cv,960,250,o=inn(t,a+.2,.5),u=inn(t,a+.3,1.0),sz=40,t=t)
        for k,nm in enumerate(_BON):
            t0=a+1.6+k*.8
            if t>t0: u=inn(t,t0,.4);put_screen(cv,band(380,80,PAPER,.85,14),480+k*480,420,u);put_screen(cv,text(nm,34,RED,700),480+k*480,418,u)
        if t>q:
            u=inn(t,q,.5);put_screen(cv,band(760,90,PAPER,.92,14),960,600,u)
            put_screen(cv,wipe(text('Toàn thư, Cương mục: không ghi',40,INK,700),inn(t,q+.1,.8),0,.25,seed=7),960,598,1)
# ---------- 17: sách địa lý đời Tống, hơn 700 năm sau → hoang đường
def S_17(cv,t):
    a,b=T[17]-.3,E[17]+.3;q=sb(17,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,540,1.1))])
    trong(cv,c,t,.6)
    if t<q-.3 or FREEZE:
        put(cv,c,'t16x_sachtong',960,560,s=1.1)
        for j in range(6): viet(cv,c,[(1400,250+j*44),(1500,250+j*44)],t,a+.6+j*.5,.4,wid=4,o=.7)
    else:
        put(cv,c,'t16x_hoangduong',960,560,s=1.1,o=inn(t,q-.3,.6))
        for i in range(4):
            u=inn(t,q+i*.8,1.4);put(cv,c,'blot',600+i*240,320+(i%2)*170,s=(.25+.3*u)*(1+.12*math.sin(t*1.3+i)),o=.18*u,r=30*u+8*math.sin(t*.9+i))
        for i in range(2): viet(cv,c,[(520+i*400,300+i*60),(800+i*400,440+i*60)],t,q+1.5+i*1.0,.6,wid=8,col=RED,o=.65)
    di(cv,c,'t16_spr_khach',-500,920,300,920,t,a,b,s=.45,bob=2,f=4)
    di(cv,c,'t16_spr_quan',2300,860,1700,860,t,a+.3,b,s=.7,bob=2,f=3)
    di(cv,c,'t16_spr_dan',-400,930,500,930,t,a+.8,b,s=.42,bob=2,f=3.6)
    if t<q-.3 or FREEZE: flick(cv,c,760,560,t,.7);smoke(cv,c,760,500,t,.6)
    trong_truoc(cv,c,t)
    lb(cv,C0,'sách địa lý đời Tống: hơn 700 năm sau',960,160,t,a+.4,q-.2,col=INK,sz=40)
    lb(cv,C0,'sử gia triều Nguyễn chê: hoang đường',960,160,t,q+.2,b,col=RED,sz=42)
# ---------- 18: dân gian kể tiếp (khói bếp thành bốn mảnh giấy)
def S_18(cv,t):
    a,b=T[18]-.3,E[18]+.3;q=sb(18,1)
    c=kc(t,[(a,(960,540,1.0)),(b,(960,600,1.14))])
    ngoai(cv,c,t,g=860,far=.6,midv=.6,seed=12)
    put(cv,c,'t16x_ke',960,560,s=1.1)
    flick(cv,c,900,800,t,1.0);smoke(cv,c,900,720,t,1.0)
    for i in range(3): di(cv,c,'t16_spr_khach',-600-i*200,920,100+i*80,920,t,a+i*.8,q+1,s=.45,bob=2,f=3.5+i*.3,ph=i)
    put(cv,c,'t16_spr_ba',1250,560,s=.9,ay=1,o=.3*inn(t,q,1.5),r=2*math.sin(t))
    truoc(cv,c,t)
    if not FREEZE and t>q-.2:
        for k,nm in enumerate(['một cái tên','một tuổi','một ngọn núi']):
            t0=q+k*.8;u=inn(t,t0,1.6)
            if t>t0: put_screen(cv,band(300,70,PAPER,.85,12),lerp(960,520+k*440,u),lerp(700,420,u),u);put_screen(cv,text(nm,32,RED,700),lerp(960,520+k*440,u),lerp(698,418,u),u)
        t3=q+2.6
        if t>t3: cau_noi(cv,960,280,o=inn(t,t3,.5),u=inn(t,t3,1.0),sz=38,t=t)
    lb(cv,C0,'phần còn lại là của dân gian',960,160,t,a+.4,q-.2,col=INK,sz=44)
# ---------- 19: câu nói nhòe đi, việc bà làm thì rõ (chia đôi)
def S_19(cv,t):
    a,b=T[19]-.3,E[19]+.3;q=sb(19,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1100,560,1.08))])
    ngoai(cv,c,t,g=880,seed=14,mist=.4)
    voi(cv,c,1500,900,1250,900,t,a,b,s=.9)
    di(cv,c,'t16_spr_cc',2200,900,1700,900,t,a,b,s=.55,bob=5,f=6)
    co_bay(cv,c,'t16_spr_ccco',1460,860,t,1.1)
    di(cv,c,'t16_spr_khach',-300,920,400,920,t,a,b,s=.45,bob=2,f=3.6)
    truoc(cv,c,t)
    if not FREEZE:
        cau_noi(cv,620,330,o=1.0,u=1.0,sz=30,mo=inn(t,a+.4,q-a),t=t,trai=1)
        if t>q: put_screen(cv,band(560,90,PAPER,.9,14),1360,330,inn(t,q,.4));put_screen(cv,wipe(text('việc bà làm: sử chép thật',38,RED,700),inn(t,q+.1,.7),0,.25,seed=9),1360,328,1)
    lb(cv,C0,'câu nói ấy có thể bà chưa từng nói',960,160,t,a+.4,q-.2,col=INK,sz=42)
# ---------- 20: kết
def S_20(cv,t):
    a=T[20]-.3;b=E[20]+4
    c=kc(t,[(a,(900,560,1.06)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=13,mist=.6)
    put(cv,c,'t16x_cuoi',960,560,s=1.0)
    for i in range(3): di(cv,c,'t16_spr_dan' if i%2 else 't16_spr_dan2',1700+i*200,890+i*14,2500+i*200,870+i*14,t,a-1,b,s=.55,bob=3,f=4.4+i*.3,ph=i)
    voi(cv,c,100,890,1500,890,t,a,b,s=.85,k=1)
    for r in range(2): di(cv,c,'t16_spr_cc',-300-r*200,920+r*30,1100-r*200,920+r*30,t,a+.4+r*.4,b,s=.55,bob=5,f=6+r,ph=r)
    co_bay(cv,c,'t16_spr_ccco',lerp(260,1660,inn(t,a,b-a)),880,t,1.1)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    if not FREEZE:
        tx=text('Bà Triệu, năm 248',54,INK,700);put_screen(cv,wipe(tx,inn(t,a+.8,1.4),0,.3,seed=13),W/2,170)
        put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,245,inn(t,E[20]+.6,1))
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
    flock=lambda *a,**k:None
S=lambda n:T[n]-.3
SH=[(0 if n==1 else S(n),S(n+1) if n<20 else V.TOTAL+1,globals()[f'S_{n}']) for n in range(1,21)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm16_full.json'))
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
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'CỬU CHÂN · NĂM 248','stitle16',.55)
    caps(cv,t)
V.NHAN={5:'Lữ Đại – tướng nhà Ngô',6:'Lục Dận – quan nhà Ngô'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
