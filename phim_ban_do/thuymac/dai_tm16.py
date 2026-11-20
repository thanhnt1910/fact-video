# Bản dài tm16: Bà Triệu, Cửu Chân năm 248. Dựng lại 20/11/2026 theo quy tắc "độ chi tiết ngang video Ngô Quyền":
# mỗi cảnh ghép nhiều lớp (núi xa, đồi giữa, vật chính, cây tiền cảnh, sương hai tầng), ít nhất ba vật chuyển động riêng
# khớp từng câu lời đọc, hình nhỏ vẽ riêng cho tập (t16_spr_*), hai cảnh trọng tâm: ra hàng (đoạn 10) và voi ra trận (đoạn 13).
# Quy ước màu (quy ước hình ảnh): quân Cửu Chân và quân Bà Triệu đỏ son, quân nhà Ngô xanh chàm đội mũ trụ; Bà Triệu áo vàng (Giao Chỉ chí).
import math,re,json,os
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
# ---------- 1 hook: bên phải các gia đình ra hàng đi về, bên trái voi của Bà Triệu nổi lên
def S_1(cv,t):
    a,b=0,E[1]+.3;s1=sb(1,1) if len(_SC[1])>2 else 2.9
    c=kc(t,[(a,(1200,560,1.12)),(2.6,(1150,560,1.06)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=1)
    put(cv,c,'t16x_voi1',960,560,s=1.0,o=.6)
    for i in range(4): di(cv,c,'t16_spr_dan' if i%2 else 't16_spr_dan2',1000+i*230,880+i*14,1900+i*230,860+i*14,t,a-1,b+2,s=.7-.04*i,bob=3,f=4.6+i*.3,ph=i)
    for i in range(3): di(cv,c,'t16_spr_cc',-700+i*120,900+i*30,200+i*140,900+i*30,t,1.8+i*.25,b,s=.62+.05*i,bob=5,f=6+i,ph=i*1.3)
    voi(cv,c,-500,920,560,920,t,1.6,b,s=.95)
    flock(cv,c,t,.6)
    truoc(cv,c,t)
    big(cv,'HƠN BA VẠN NHÀ RA HÀNG',t,.25,2.9,RED,150,76,seed=1)
    big(cv,'MỘT PHỤ NỮ CƯỠI VOI NỔI LÊN',t,3.0,b,INK,150,70,seed=2)
# 2 trụ sở quận huyện bị đánh
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3;q=sb(2,1);h=sb(2,1)+(E[2]-sb(2,1))*.5
    c=kc(t,[(a,(960,540,1.0)),(q,(1000,560,1.08)),(b,(1100,600,1.16))])
    ngoai(cv,c,t,g=870,seed=2)
    put(cv,c,'t16x_trusoo',960,560,s=1.1)
    for i in range(3): di(cv,c,'t16_spr_ngo1',640+i*140,845,620+i*140,845,t,a,b,s=.55,bob=1.5,f=1.2+i*.4,ph=i,lac=.6)
    for i in range(3): di(cv,c,'t16_spr_cc',2300+i*160,880+i*20,1500+i*120,880+i*20,t,a+i*.4,h+.5,s=.62,bob=5,f=6.4+i*.5,ph=i)
    smoke(cv,c,960,380,t,1.0)
    if t>q-.5: clash(cv,c,t,h,b,'ngo','cc',xm=960,y=790,s=0.9,push=-1,seed=3,pre='t16_spr_')
    if t>h: 
        for x in (720,1180): flick(cv,c,x,420,t,s=1.3*inn(t,h,1.5));smoke(cv,c,x,360,t,s=1.2)
    truoc(cv,c,t)
    seal(cv,'s248',1560,330,a+.6,t,s=.8,r=4)
    lb(cv,c,'năm 248, Cửu Chân (Thanh Hóa)',960,170,t,a+.4,q-.2,col=RED,sz=44)
    lb(cv,c,'quân nhà Ngô',560,300,t,h,b,col=NGO,sz=32);lb(cv,c,'người theo bà',1400,300,t,h,b,col=RED,sz=32)
# 3 sử nhà Ngô đếm số nhà, không chép tên
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3;q1,q2=sb(3,1),sb(3,2)
    c=kc(t,[(a,(960,560,1.0)),(b,(900,600,1.14))])
    trong(cv,c,t,.6)
    put(cv,c,'t16x_so',960,560,s=1.1)
    for i in range(4): di(cv,c,'t16_spr_dan' if i%2 else 't16_spr_dan2',-300-i*260,880,520-i*170,880,t,a,q1,s=.72,bob=3,f=4.4+i*.4,ph=i)
    for j in range(5): viet(cv,c,[(760+j*80,612),(760+j*80,632)],t,a+.8+j*.7,.5,wid=4,o=.8)
    put(cv,c,'t16_spr_quan',1180,655,s=.75,ay=1,r=1.5*math.sin(t*3))
    smoke(cv,c,1350,560,t,.8)
    trong_truoc(cv,c,t)
    lb(cv,c,'ghi kỹ số nhà ra hàng',960,160,t,a+.4,q1-.1,col=INK,sz=40)
    lb(cv,c,'không chép tên bà',960,160,t,q1+.1,q2-.1,col=RED,sz=44)
# 4 bản đồ: Giao Châu chia ba quận, nước Ngô
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3
    dl,th,ng=P['daila'],P['thanhhoa'],P['nghean']
    c=mcam(t,[(a-.3,(700,620,1.35)),(a+4,(760,740,1.1)),(b,(860,700,1.0))])
    mapbg(cv,c,u=inn(t,a-.4,1.2))
    for nm,p in (('Giao Chỉ',dl),('Cửu Chân',th),('Nhật Nam',ng)):
        dot(cv,c,*p,o=inn(t,a+.6,.4));tag(cv,c,p[0]+22,p[1]-6,nm,dy=0,sz=26)
    pulse(cv,c,*th,t)
    stroke(cv,c,[(dl[0]+500,dl[1]-300),(dl[0]+200,dl[1]-120),dl],inn(t,a+.5,3),wid=8,col=NGO)
    q=sb(4,1)
    di(cv,c,'t16_spr_thuyen',dl[0]+700,dl[1]-80,dl[0]+380,dl[1]+60,t,q,b,s=.32,bob=3,f=2,lac=2)
    di(cv,c,'t16_spr_ngua',dl[0]+360,dl[1]-260,dl[0]+80,dl[1]-40,t,a+.5,a+4,s=.25,bob=2,f=7)
    di(cv,c,'t16_spr_ngo',dl[0]+520,dl[1]-200,dl[0]+160,dl[1]+10,t,q+.5,b,s=.18,bob=1,f=6)
    lb(cv,c,'Giao Châu thuộc quyền nhà Ngô',960,170,t,a+.3,q-.2,col=INK,sz=38)
    lb(cv,c,'nhà Ngô sai Lữ Đại sang',960,170,t,q+.2,b,col=NGO,sz=40)
# 5 Lữ Đại hứa tha rồi chém Sĩ Huy
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3;q=sb(5,1)
    c=kc(t,[(a,(960,560,1.0)),(q,(960,560,1.08)),(b,(900,520,1.2))])
    ngoai(cv,c,t,g=880,seed=3)
    put(cv,c,'t16x_luudai',960,560,s=1.1)
    di(cv,c,'t16_spr_ngo',-500,880,140,880,t,a,q,s=.62,bob=3,f=5)
    di(cv,c,'t16_spr_ngo',2400,890,1780,890,t,a+.4,q,s=.6,bob=3,f=5.4,ph=1)
    for i in range(3): di(cv,c,'t16_spr_quy',760+i*150,900,760+i*150,912,t,a+1+i*.5,q,s=.55,bob=0,lac=.8,ph=i)
    if t>q+.6:
        v=inn(t,q+.6,1.8);put(cv,c,'redblot',960,760,s=.8+1.0*v,o=.38*v,r=18*v);ink_wash(cv,.22*v)
    truoc(cv,c,t)
    lb(cv,c,'Sĩ Huy chống lại',960,170,t,a+.4,q-.2,col=INK,sz=40)
    lb(cv,c,'hứa tha, rồi chém',960,170,t,q+.2,b,col=RED,sz=48)
# 6 Ngô Sĩ Liên bàn về chữ tín
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3;q=sb(6,1)
    c=kc(t,[(a,(960,540,1.0)),(b,(1000,560,1.12))])
    trong(cv,c,t,.7)
    put(cv,c,'t16x_sulien',960,560,s=1.1)
    for j in range(6): viet(cv,c,[(800+j*44,500),(800+j*44,540)],t,a+.5+j*.6,.45,wid=4,o=.85)
    flick(cv,c,1180,500,t,.8);smoke(cv,c,1180,440,t,.7)
    put(cv,c,'t16_spr_quan',990,620,s=.0001,o=0)
    di(cv,c,'t16_spr_khach',-500,920,200,920,t,q,b,s=.55,bob=2,f=4)
    trong_truoc(cv,c,t)
    lb(cv,c,'Ngô Sĩ Liên, sử gia đời Lê',960,160,t,a+.4,q-.2,col=INK,sz=42)
    lb(cv,c,'một lời hứa đã bị phá',960,160,t,q+.2,b,col=RED,sz=44)
# 7 thư dâng vua Ngô
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3;q=sb(7,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,520,1.14))])
    trong(cv,c,t,.6)
    put(cv,c,'t16x_thu',960,560,s=1.1)
    x,y=di(cv,c,'t16_spr_quan',600,840,880,780,t,a+.3,q,s=.8,bob=2,f=3)
    if t>q: 
        u=inn(t,q,1.2);put(cv,c,'t16_spr_quan',960,700-30*u,s=.0001,o=0)
        viet(cv,c,[(860,700),(1060,700)],t,q,1.0,wid=6,col=RED,o=.8)
    smoke(cv,c,700,620,t,.8);smoke(cv,c,1220,620,t+1.3,.8)
    for i in range(2): di(cv,c,'t16_spr_1ngo',380+i*1160,860,380+i*1160,860,t,a,b,s=.6,bob=1,f=1.3,ph=i,lac=.5)
    trong_truoc(cv,c,t)
    lb(cv,c,'giao nhầm người, lại sinh chuyện',960,160,t,q+.2,b,col=RED,sz=40)
# 8 năm 248, Cửu Chân chiếm thành
def S_8(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1)
    c=kc(t,[(a,(1100,560,1.08)),(b,(860,560,1.0))])
    ngoai(cv,c,t,g=860,seed=4)
    put(cv,c,'t16x_chiemthanh',960,560,s=1.0)
    clash(cv,c,t,a+.6,q+1,'ngo','cc',xm=1000,y=720,s=0.96,push=-1,seed=5,pre='t16_spr_')
    for x in (1300,760): flick(cv,c,x,360,t,s=1.1);smoke(cv,c,x,300,t,1.3)
    if t>q: di(cv,c,'t16_spr_ngua',1500,860,2400,840,t,q,b,s=.6,bob=6,f=8)
    truoc(cv,c,t)
    lb(cv,c,'người Cửu Chân đánh chiếm các thành',960,170,t,a+.4,q-.2,col=RED,sz=40)
    lb(cv,c,'quân nhà Ngô',480,300,t,a+.6,q,col=NGO,sz=32);lb(cv,c,'người Cửu Chân',1460,300,t,a+.6,q,col=RED,sz=32)
# 9 Lục Dận đi thuyền sang
def S_9(cv,t):
    a,b=T[9]-.3,E[9]+.3;q=sb(9,1)
    c=kc(t,[(a,(1200,560,1.1)),(b,(800,560,1.0))])
    put(cv,c,'t16_far',960,560,ay=1,k=.35,o=.8)
    river(cv,c,t,PAP,wl=600,stakes=False,cliffs=False,reeds=1,mist=.8,ridge_o=.0,
          boats=[dict(name='t16_spr_thuyenlon',x=lerp(-200+i*330,900+i*330,inn(t,a-.3,b-a)),y=640+i*60+math.sin(t*1.8+i)*6,s=.55+.12*i,r=math.sin(t*1.4+i)*2.5) for i in range(3)])
    for i in range(2): di(cv,c,'t16_spr_thuyen',2100-i*400,560+i*20,1500-i*400,560+i*20,t,a,b,s=.4,bob=4,f=1.6,ph=i,k=.7,lac=3)
    flock(cv,c,t,.6)
    lb(cv,c,'Lục Dận, quan đứng đầu Giao Châu',960,170,t,a+.4,q-.2,col=NGO,sz=42)
    lb(cv,c,'hứa khoan dung với ai ra hàng',960,170,t,q+.2,b,col=INK,sz=40)
# 10 CẢNH TRỌNG TÂM: ra hàng
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3;q1,q2=sb(10,1),sb(10,2)
    c=kc(t,[(a,(1300,560,1.12)),(q1,(1100,560,1.04)),(q2,(900,560,1.0)),(b,(760,520,1.06))])
    ngoai(cv,c,t,g=880,seed=5)
    put(cv,c,'t16x_rahang',960,560,s=1.1)
    # dòng người từ đồi xuống, ba làn, mỗi làn một nhịp; tới bàn thì đặt vũ khí xuống đống rồi quay về
    n=int(10+12*inn(t,q1,b-q1))
    for i in range(n):
        ln=i%3;t0=a+i*.45;yv=830+ln*40;sc=.5+ln*.08
        if t<t0: continue
        u=(t-t0)/5.0
        if u<1: di(cv,c,['t16_spr_dan','t16_spr_dan2','t16_spr_dan'][ln],-200+ln*80,yv,1080-ln*40,yv,t,t0,t0+5,s=sc,bob=3,f=4.5+ln*.5,ph=i)
        elif u<1.25: put(cv,c,'t16_spr_quy',1150-ln*40,yv+DY,s=sc*.9*GS,ay=1,r=2*math.sin(t*2+i))
    pile=inn(t,a+2,b-a-2)
    for j in range(int(1+pile*6)): put(cv,c,'t16_spr_dau',1060+j*44,860-pile*10*(j%2),s=.6+pile*.35,ay=1,o=.9)
    co_bay(cv,c,'t16_spr_ngo1',1640,860,t,1.0);co_bay(cv,c,'t16_spr_ngo1',1780,875,t,1.0,1)
    truoc(cv,c,t)
    lb(cv,c,'lời kêu gọi có tác dụng',960,160,t,a+.4,q1-.2,col=INK,sz=42)
    if t>q1-.1:
        nn=int(30000*inn(t,q1,2.2));im=text('Toàn thư: hơn '+f'{nn:,}'.replace(',','.')+' nhà ra hàng',46,RED,700)
        put_screen(cv,im,W/2,170,inn(t,q1-.1,.4)*(1-inn(t,q2-.5,.35)))
    if t>q2-.1:
        put_screen(cv,text('sử nhà Ngô: hơn 100 thủ lĩnh, hơn 50.000 nhà',42,INK,700),W/2,170,inn(t,q2,.4))
# 11 bỏ vũ khí, về làng
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3;q=sb(11,1)
    c=kc(t,[(a,(900,560,1.04)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=860,seed=6)
    put(cv,c,'t16x_bovukhi',960,560,s=1.0)
    for i in range(5): di(cv,c,'t16_spr_dan' if i%2 else 't16_spr_dan2',600+i*90,850+(i%2)*30,1900+i*120,820+(i%2)*30,t,a+i*.8,b+2,s=.62,bob=3,f=4.6+i*.2,ph=i)
    for x in (2100,2480): smoke(cv,c,x,560,t,1.0)
    put(cv,c,'t16_spr_dau',700,860,s=.8+.3*inn(t,a,b-a),ay=1)
    truoc(cv,c,t)
    lb(cv,c,'lời hứa đi trước, quân đi sau',960,170,t,a+.4,q-.2,col=INK,sz=40)
    lb(cv,c,'phần lớn nhận lời',960,170,t,q+.2,b,col=RED,sz=44)
# 12 người phụ nữ họ Triệu nổi lên
def S_12(cv,t):
    a,b=T[12]-.3,E[12]+.3;q=sb(12,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,520,1.16))])
    ngoai(cv,c,t,g=880,seed=7)
    put(cv,c,'t16x_noilen',960,560,s=1.1)
    for i in range(3):
        di(cv,c,'t16_spr_cc',-900+i*100,890+i*24,-80+i*120,890+i*24,t,q-1+i*.4,b,s=.55+.04*i,bob=5,f=6+i*.5,ph=i)
        di(cv,c,'t16_spr_1cc',2400+i*90,880+i*24,1500+i*80,880+i*24,t,q-.5+i*.3,b,s=.6,bob=5,f=6.3+i*.4,ph=i+3)
    truoc(cv,c,t)
    lb(cv,c,'một người phụ nữ họ Triệu',960,160,t,a+.4,q-.2,col=RED,sz=44)
    lb(cv,c,'tập hợp người, đánh phá trụ sở',960,160,t,q+.2,b,col=INK,sz=40)
# 13 CẢNH TRỌNG TÂM: Bà Triệu cưỡi voi ra trận
def S_13(cv,t):
    a,b=T[13]-.3,E[13]+.3;q=sb(13,1)
    hit=a+3.0
    sh=(6*math.sin(t*37)*(1-inn(t,hit+.4,.8))) if hit<t<hit+1.2 and not FREEZE else 0
    keys=[(a,(1300,600,1.0)),(hit,(1050,600,1.04)),(q,(1150,560,1.08)),(b,(1300,470,1.3))]
    if FREEZE: keys=[(a,(1050,600,1.0))]
    cx,cy,z=cpath(t,keys) if not FREEZE else (1050,600,1.0);c=cam(cx,cy,z,sh,sh)
    ngoai(cv,c,t,g=880,seed=8,mist=.35)
    put(cv,c,'t16x_voi2',960,560,s=1.0,o=.7)
    # hàng quân nhà Ngô bên trái: dựng giáo, bắn tên, rồi bị dồn lùi
    lui=inn(t,hit,b-hit)*240
    for r in range(3):
        put(cv,c,'t16_spr_ngo',260-r*170-lui,850+r*30,s=.95+.06*r,ay=1,r=(2 if t>hit else 0)*math.sin(t*9+r))
    arrows(cv,c,t,a+.4,hit+1,[(300,700),(420,690)],[(1150,780),(1300,800)],n=8,h=90,per=1.0,seed=3,col=NGO)
    # voi lao từ phải sang trái, bụi cuộn sau chân
    xv=voi(cv,c,2200,900,820,880,t,a,hit+.3,s=1.0)
    if t>hit-1:
        for k in range(4): put(cv,c,'mist',xv+240+k*120,840-20*k,s=.5+.15*k+.2*inn(t,hit,1),o=.35*(1-inn(t,hit+3,2)),k=1.0)
    # quân của bà chạy theo ba hàng, mỗi hàng nhịp khác
    for r in range(3):
        di(cv,c,'t16_spr_cc',2500+r*200,900+r*34,980+r*160-lui*.3,900+r*34,t,a+.5+r*.35,hit+1.2+r*.3,s=.6+.05*r,bob=6,f=7+r,ph=r)
    co_bay(cv,c,'t16_spr_ccco',xv+160,860,t,1.2)
    if t>hit:
        sparks(cv,c,t,[(660+k*40,700-20*math.sin(k)) for k in range(5)],hit,b,seed=8)
        for k in range(int((b-hit)/1.2)+1):
            t0=hit+.3+k*1.2
            if t0<t<t0+1.8: fall(cv,c,'t16_spr_1ngo',560-k*30,860,t,t0,s=.95,dirn=-1)
    truoc(cv,c,t)
    lb(cv,c,'Toàn thư: bà cưỡi voi ra trận',960,160,t,a+.4,q-.2,col=RED,sz=44)
    lb(cv,c,'Giao Chỉ chí: áo vải vàng',960,160,t,q+.2,b,col=INK,sz=40)
    lb(cv,c,'quân nhà Ngô',380,330,t,a+.6,q,col=NGO,sz=32);lb(cv,c,'quân của bà',1500,330,t,a+.6,q,col=RED,sz=32)
# 14 Lục Dận dẹp được bà
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3;q=sb(14,1)
    c=kc(t,[(a,(900,560,1.0)),(b,(1150,560,1.08))])
    ngoai(cv,c,t,g=880,seed=9,mist=.8)
    put(cv,c,'t16x_dep',960,560,s=1.0)
    clash(cv,c,t,a+.4,q,'ngo','cc',xm=900,y=780,s=0.93,push=1,seed=9,pre='t16_spr_')
    if t>q:
        for i in range(3): di(cv,c,'t16_spr_ngo',300+i*200,860+i*30,1100+i*260,860+i*30,t,q,b,s=.6,bob=3,f=5+i*.4,ph=i)
        u=inn(t,q,2.5);put(cv,c,'t16_spr_ccco',1500,870,s=1.2,ay=1,r=-70*u,o=1-.7*u)
    truoc(cv,c,t)
    lb(cv,c,'Lục Dận dẹp được bà',960,160,t,a+.4,q-.2,col=NGO,sz=44)
    lb(cv,c,'sử không chép bà mất ra sao',960,160,t,q+.2,b,col=INK,sz=40)
# 15 thứ tự các việc: người ra hàng đi một chiều, bà đi chiều ngược lại
def S_15(cv,t):
    a,b=T[15]-.3,E[15]+.3;q1,q2=sb(15,1),sb(15,2)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.1))])
    ngoai(cv,c,t,g=880,seed=10)
    put(cv,c,'t16x_thutu',960,560,s=1.1)
    for i in range(4): di(cv,c,'t16_spr_dan' if i%2 else 't16_spr_dan2',900-i*60,850+i*20,-500-i*200,850+i*20,t,a+i*.5,b,s=.62,bob=3,f=4.4+i*.3,ph=i)
    voi(cv,c,2300,880,1300,880,t,q1,b,s=.85)
    di(cv,c,'t16_spr_cc',2700,900,1700,900,t,q1+.4,b,s=.55,bob=5,f=6.5)
    truoc(cv,c,t)
    lb(cv,c,'người khác bỏ vũ khí',600,250,t,a+.4,b,col=INK,sz=36)
    lb(cv,c,'bà đứng lên',1450,250,t,q1+.2,b,col=RED,sz=40)
    lb(cv,c,'sử không chép vì sao',960,160,t,q2+.2,b,col=INK,sz=40)
# 16 thành thần, đền Phú Điền
def S_16(cv,t):
    a,b=T[16]-.3,E[16]+.3;q=sb(16,1)
    c=kc(t,[(a,(960,500,1.06)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=11)
    put(cv,c,'t16x_den',960,560,s=1.1)
    for i in range(3): smoke(cv,c,900+i*60,610,t+i,.8)
    for i in range(3): di(cv,c,'t16_spr_khach',-400-i*300,900+i*20,500+i*80,900+i*20,t,a+i*.6,b,s=.45,bob=2,f=3.6+i*.3,ph=i)
    flock(cv,c,t,.6)
    truoc(cv,c,t)
    lb(cv,c,'bà được thờ làm thần',960,160,t,a+.4,q-.2,col=RED,sz=44)
    lb(cv,c,'đền ở Phú Điền, nay vùng Hậu Lộc',960,160,t,q+.2,b,col=INK,sz=40)
# 17 Cương mục
def S_17(cv,t):
    a,b=T[17]-.3,E[17]+.3
    c=kc(t,[(a,(1000,560,1.0)),(b,(900,540,1.12))])
    trong(cv,c,t,.6)
    put(cv,c,'t16x_sunguyen',960,560,s=1.1)
    for j in range(7): viet(cv,c,[(800+j*50,548),(800+j*50,556)],t,a+.4+j*.5,.4,wid=4,o=.8)
    di(cv,c,'t16_spr_quan',2100,760,1400,760,t,a,b,s=.7,bob=2,f=3)
    smoke(cv,c,960,640,t,.8)
    trong_truoc(cv,c,t)
    lb(cv,c,'chỉ đứng sau Hai Bà Trưng',960,160,t,a+.4,b,col=RED,sz=44)
# 18 sách địa lý đời Tống
def S_18(cv,t):
    a,b=T[18]-.3,E[18]+.3;q=sb(18,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,540,1.12))])
    trong(cv,c,t,.6)
    put(cv,c,'t16x_sachtong',960,560,s=1.1)
    for j in range(6): viet(cv,c,[(1400,250+j*44),(1500,250+j*44)],t,q+j*.5,.4,wid=4,o=.7)
    flick(cv,c,760,560,t,.7);smoke(cv,c,760,500,t,.6)
    di(cv,c,'t16_spr_khach',-500,920,300,920,t,a,q,s=.45,bob=2,f=4)
    trong_truoc(cv,c,t)
    lb(cv,c,'những điều quen thuộc từ đâu?',960,160,t,a+.4,q-.2,col=RED,sz=42)
    lb(cv,c,'sách đời Tống, hơn 700 năm sau',960,160,t,q+.2,b,col=INK,sz=40)
# 19 chuyện hoang đường
def S_19(cv,t):
    a,b=T[19]-.3,E[19]+.3
    c=kc(t,[(a,(960,540,1.0)),(b,(960,520,1.1))])
    trong(cv,c,t,.5)
    put(cv,c,'t16x_hoangduong',960,560,s=1.1)
    for i in range(4):
        u=inn(t,a+i*1.1,1.6);put(cv,c,'blot',600+i*240,320+(i%2)*170,s=(.25+.3*u)*(1+.12*math.sin(t*1.3+i)),o=.18*u*(1-inn(t,b-1,1)),r=30*u+8*math.sin(t*.9+i))
    for i in range(3): viet(cv,c,[(520+i*300,300+i*40),(760+i*300,420+i*40)],t,a+1+i*1.2,.6,wid=8,col=RED,o=.65)
    di(cv,c,'t16_spr_quan',-300,860,300,860,t,a,b,s=.7,bob=2,f=3)
    di(cv,c,'t16_spr_khach',2300,900,1500,900,t,a+.5,b,s=.45,bob=2,f=3.7)
    smoke(cv,c,1500,600,t,.8)
    trong_truoc(cv,c,t)
    lb(cv,c,'mỗi sách ghi một kiểu',960,120,t,a+.4,b,col=RED,sz=42)
# 20 hai cột: sử chép và đời sau kể thêm
def S_20(cv,t):
    a,b=T[20]-.3,E[20]+.3;q=sb(20,1)
    c=kc(t,[(a,(960,540,1.0)),(q,(700,540,1.12)),(b,(1300,540,1.12))])
    trong(cv,c,t,.5)
    put(cv,c,'t16x_haicot',960,560,s=1.1)
    for i in range(3): viet(cv,c,[(1020,330+i*130),(1620,330+i*130)],t,a+.8+i*1.2,.8,wid=6,col=RED,o=.6)
    put(cv,c,'t16_spr_ba',1360,620,s=.8,ay=1,o=.35+.25*math.sin(t*1.3)**2,r=2*math.sin(t))
    di(cv,c,'t16_spr_khach',-500,940,200,940,t,a,b,s=.45,bob=2,f=4)
    di(cv,c,'t16_spr_quan',2400,860,1700,860,t,a+.6,b,s=.7,bob=2,f=3.2)
    smoke(cv,c,960,640,t,.7)
    trong_truoc(cv,c,t)
    lb(cv,c,'Toàn thư, Cương mục',620,215,t,a+.3,b,col=INK,sz=34);lb(cv,c,'người đời sau kể thêm',1360,215,t,a+.3,b,col=RED,sz=34)
    lb(cv,c,'tên, tuổi, núi Tùng: không có',960,140,t,a+.6,q-.2,col=INK,sz=36)
    lb(cv,c,'câu nói nổi tiếng: dân gian kể',960,140,t,q+.2,b,col=RED,sz=38)
# 21 người đời sau kể tiếp
def S_21(cv,t):
    a,b=T[21]-.3,E[21]+.3;q1,q2=sb(21,1),sb(21,2)
    c=kc(t,[(a,(960,540,1.0)),(b,(960,600,1.14))])
    ngoai(cv,c,t,g=860,far=.6,midv=.6,seed=12)
    put(cv,c,'t16x_ke',960,560,s=1.1)
    flick(cv,c,900,800,t,1.0);smoke(cv,c,900,720,t,1.0)
    for i in range(3): di(cv,c,'t16_spr_khach',-600-i*200,920,100+i*80,920,t,a+i*.8,q1+1,s=.45,bob=2,f=3.5+i*.3,ph=i)
    put(cv,c,'t16_spr_ba',1200,560,s=.9,ay=1,o=.3*inn(t,q1,1.5)*(1-inn(t,q2,1)),r=2*math.sin(t))
    truoc(cv,c,t)
    lb(cv,c,'người đời sau kể tiếp phần sử bỏ trống',960,160,t,q1+.2,q2-.2,col=RED,sz=40)
    lb(cv,c,'điều sử chép thì vẫn chắc chắn',960,160,t,q2+.2,b,col=INK,sz=42)
# 22 kết
def S_22(cv,t):
    a=T[22]-.3;b=E[22]+4
    c=kc(t,[(a,(900,560,1.06)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=13,mist=.6)
    put(cv,c,'t16x_cuoi',960,560,s=1.0)
    voi(cv,c,100,890,1700,890,t,a,b,s=.85,k=1)
    for r in range(2): di(cv,c,'t16_spr_cc',-300-r*200,920+r*30,1300-r*200,920+r*30,t,a+.4+r*.4,b,s=.55,bob=5,f=6+r,ph=r)
    co_bay(cv,c,'t16_spr_ccco',lerp(260,1860,inn(t,a,b-a)),880,t,1.1)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    tx=text('Bà Triệu, năm 248',54,INK,700);put_screen(cv,wipe(tx,inn(t,a+.8,1.4),0,.3,seed=13),W/2,170)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,245,inn(t,E[22]+.6,1))
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
    flock=lambda *a,**k:None
S=lambda n:T[n]-.3
SH=[(0,S(2),S_1)]+[(S(n),S(n+1),globals()[f'S_{n}']) for n in range(2,22)]+[(S(22),V.TOTAL+1,S_22)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm16_full.json'))
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
    TT=T[4]
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'CỬU CHÂN · NĂM 248','stitle16',.55)
    caps(cv,t)
V.NHAN={5:'Lữ Đại – tướng nhà Ngô',9:'Lục Dận – quan nhà Ngô',12:'Bà Triệu – Cửu Chân'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
