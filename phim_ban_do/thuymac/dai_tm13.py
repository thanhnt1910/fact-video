# Bản dài tm13: Hai Bà Trưng, Lãng Bạc và Cấm Khê. Dựng lại 20/11/2026 theo quy tắc "độ chi tiết ngang video Ngô Quyền":
# cảnh ghép nhiều lớp (núi xa, đồng giữa, vật chính, cây tiền cảnh, sương hai tầng), ít nhất ba vật chuyển động riêng khớp câu,
# hình nhỏ vẽ riêng (t13_spr_*), cảnh trọng tâm: trận Lãng Bạc (đoạn 9) và nấu trống đồng (đoạn 13).
# Quy ước màu: quân hai bà đỏ son, quân nhà Hán xanh chàm đội mũ trụ, suốt video.
import math,re,json,os
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from fx_tran import arrows,dust,sparks,fall
from tran_fx import clash
from dai_tm2 import big,lb
V=K.setup('tm13',{4:4.0})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
P=PTS
FREEZE=bool(os.environ.get('KIEM_TINH'))
GS=1.45
HAN=(.17,.29,.45)
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
def trong(cv,c,t,o=.85): put(cv,c,'t13_inback',960,540,k=.5,o=o)
def trong_truoc(cv,c,t):
    put(cv,c,'t13_inL',-60,1100,ax=0,ay=1,k=1.3,s=.72,r=.4*math.sin(t*.6),o=.9)
    put(cv,c,'t13_inR',1980,1100,ax=1,ay=1,k=1.3,s=.72,r=.4*math.sin(t*.6+2),o=.9)
def di(cv,c,name,x0,y0,x1,y1,t,a,b,s=1.0,o=.97,bob=4,f=5,ph=0,k=1.0,r=0,lac=1.2,lat=False):
    if y0>700 and k==1.0: s*=GS;bob*=GS
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;y=y0+(y1-y0)*u-abs(math.sin(t*f+ph))*bob*(1 if 0<u<1 else .3)
    put(cv,c,Af(name) if lat else name,x,y,s=s,o=o,k=k,r=r+lac*math.sin(t*f*.5+ph),ay=1,scale_px=1.5)
    return x,y
def flick(cv,c,x,y,t,s=1.0):
    put(cv,c,'t12_spr_lua',x+6*math.sin(t*7),y,s=min(s,.38)*(1+.08*math.sin(t*9)),o=.5+.3*math.sin(t*5)**2)
def smoke(cv,c,x,y,t,s=1.0):
    for k in range(2): put(cv,c,'t12_spr_khoi',x+20*math.sin(t*.7+k),y-((t*40+k*120)%240),s=s,o=.5*(1-((t*40+k*120)%240)/240))
def pulse(cv,c,x,y,t,col=RED):
    for k in range(2):
        u=((t*.6+k*.5)%1.0);dot(cv,c,x,y,o=.6*(1-u),col=col,r=int(8+40*u))
def co_bay(cv,c,name,x,y,t,s=1.0,ph=0,lat=False):
    put(cv,c,Af(name) if lat else name,x,y,s=s,ay=1,r=2.5*math.sin(t*2.2+ph),scale_px=1.5)
def viet(cv,c,pts,t,a,d,wid=5,col=INK,o=.7):
    stroke(cv,c,pts,inn(t,a,d),wid=wid,col=col,o=o,head=False)
# 1 hook: Tô Định bỏ chạy
def S_1(cv,t):
    a,b=0,E[1]+.3
    c=kc(t,[(a,(700,560,1.12)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=1)
    put(cv,c,'t13x_chay',960,560,s=1.05,o=.55)
    di(cv,c,'t13_spr_dinh',500,850,1700,840,t,a,b+1,s=.9,bob=8,f=9,lac=2)
    for i in range(3): di(cv,c,'t13_spr_1han',300-i*120,860+i*14,1400-i*140,860+i*14,t,a+.2+i*.2,b+1,s=.62,bob=6,f=8+i,ph=i)
    for i in range(3): di(cv,c,'t13_spr_trungco' if i==1 else 't13_spr_1trung',-500-i*150,880+i*16,700-i*170,880+i*16,t,a+.6+i*.3,b+1,s=.62,bob=6,f=7.5+i*.5,ph=i+2,lat=i!=1)
    for i in range(5): dust(cv,c,lerp(500,1700,inn(t,a,b+1))-160-i*60,860+(i%2)*10,o=.25,s=.3+.05*i)
    flock(cv,c,t,.6)
    truoc(cv,c,t)
    big(cv,'THÁI THÚ BỎ CHẠY',t,.25,3.2,RED,150,84,seed=1)
    big(cv,'VÌ HAI NGƯỜI PHỤ NỮ',t,3.3,b,INK,150,84,seed=2)
# 2a Tô Định và luật nhà Hán
def S_2a(cv,t):
    a,b=T[2]-.3,sb(2,1)
    c=kc(t,[(a,(960,540,1.0)),(b,(1020,560,1.12))])
    ngoai(cv,c,t,g=870,seed=2)
    put(cv,c,'t13x_phu',960,560,s=1.1)
    di(cv,c,'t13_spr_han',-600,880,200,880,t,a,b,s=.6,bob=3,f=5)
    di(cv,c,'t13_spr_trai',2300,890,1500,890,t,a+.5,b,s=.62,bob=2,f=3.2)
    di(cv,c,'t13_spr_1han',2600,880,1800,880,t,a+.5,b,s=.62,bob=3,f=4.5,ph=1,lat=True)
    smoke(cv,c,1300,600,t,.9)
    truoc(cv,c,t)
    lb(cv,c,'Tô Định, thái thú quận Giao Chỉ',960,170,t,a+.6,b-.3,col=RED,sz=42)
    lb(cv,c,'nhà Hán cai trị hơn 140 năm',960,225,t,b-4.5,b-.3,col=INK,sz=34)
# 2b bản đồ: các quận hưởng ứng
def S_2b(cv,t):
    a,b=sb(2,1),E[2]+.3
    dl,th,ng,lc=P['daila'],P['thanhhoa'],P['nghean'],P['liemchau']
    c=mcam(t,[(a-.3,(520,640,1.5)),(a+3,(700,760,1.0)),(b,(900,640,.95))])
    mapbg(cv,c,u=inn(t,a-.4,1.2))
    dot(cv,c,*dl);tag(cv,c,dl[0]+24,dl[1]-6,'Mê Linh',dy=0,sz=26);pulse(cv,c,*dl,t)
    lb(cv,c,'Trưng Trắc và Trưng Nhị',dl[0]+300,dl[1]-90,t,a+.2,sb(2,2)-.2,col=RED,sz=32)
    for nm,p,t0 in (('Cửu Chân',th,sb(2,2)+.6),('Nhật Nam',ng,sb(2,2)+1.5),('Hợp Phố',lc,sb(2,2)+2.4)):
        if t>t0:
            dot(cv,c,*p,o=inn(t,t0,.3));tag(cv,c,p[0]+22,p[1]-6,nm,dy=0,sz=26);stroke(cv,c,[dl,p],inn(t,t0,1.2),wid=5,col=RED,o=.8)
            u=inn(t,t0,1.4);put(cv,c,'t13_spr_trungco',dl[0]+(p[0]-dl[0])*u,dl[1]+(p[1]-dl[1])*u,s=.22,ay=1,r=3*math.sin(t*3+t0))
    put(cv,c,'t13_spr_haiba',dl[0]-10,dl[1]-6,s=.3,ay=1,r=1.5*math.sin(t*1.6),o=inn(t,a,.6))
    u=inn(t,a,b-a);put(cv,c,'t13_spr_dinh',dl[0]+40+520*u,dl[1]-20-260*u,s=.22,ay=1,r=2*math.sin(t*7))
    put(cv,c,'t13_spr_han',dl[0]+10+420*u,dl[1]+10-200*u,s=.16,ay=1,r=1.5*math.sin(t*6))
    put(cv,c,'t13_spr_trung',dl[0]-60+120*u,dl[1]+40+20*math.sin(t),s=.16,ay=1)
    if t>sb(2,2)+3:
        n65=int(65*inn(t,sb(2,2)+3,2.5));rg=np.random.default_rng(2)
        for i in range(n65):
            p=(dl[0]+60+rg.random()*900,dl[1]-120+rg.random()*400-(i%3)*10);dot(cv,c,p[0],p[1],o=.8,col=RED,r=6)
        lb(cv,c,'sáu mươi lăm thành đáp lại',1100,260,t,sb(2,2)+3.2,b,col=RED,sz=42)
# 3 ba năm sau, tắt
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3
    c=kc(t,[(a,(960,540,1.02)),(b,(960,560,1.14))])
    ngoai(cv,c,t,g=880,seed=3,mist=.7)
    put(cv,c,'t13x_tat',960,560,s=1.1)
    put(cv,c,'t13_spr_trong',950,850,s=1.0+.03*math.sin(t*.8),ay=1,r=4*math.sin(t*.6),scale_px=1.5)
    co_bay(cv,c,'t13_spr_trungco',600,860,t,1.0)
    di(cv,c,'t13_spr_dan',700,880,-400,880,t,a,b,s=.6,bob=3,f=4,lat=True)
    smoke(cv,c,1350,700,t,1.0)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    lb(cv,c,'ba năm sau',960,170,t,a+.4,sb(3,1)-.2,col=RED,sz=48)
    lb(cv,c,'vì sao không giữ nổi?',960,170,t,sb(3,1)+.2,b,col=INK,sz=46)
    seal(cv,'s43',1500,330,sb(3,1)-1.5,t,s=.8,r=4)
# 4 Mê Linh, Chu Diên, Thi Sách bị giết
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3;q1,q2=sb(4,1),sb(4,2)
    c=kc(t,[(a,(860,560,1.0)),(q1,(960,560,1.06)),(b,(1060,560,1.12))])
    ngoai(cv,c,t,g=880,seed=4)
    put(cv,c,'t13x_lang',960,560,s=1.1)
    di(cv,c,'t13_spr_dan',-300,880,500,880,t,a,q1,s=.6,bob=3,f=4.5)
    if t>q1-.3:
        di(cv,c,'t13_spr_trai',2300,890,1300,890,t,q1,q2,s=.62,bob=2,f=3)
        di(cv,c,'t13_spr_han',2700,880,1700,880,t,q1,q2+1,s=.58,bob=3,f=5,lat=True)
    if t>q2-.3: di(cv,c,'t13_spr_haiba',500,880,760,880,t,q2,b,s=.65,bob=1,f=2)
    truoc(cv,c,t)
    lb(cv,c,'Mê Linh, nhà Trưng Trắc',700,200,t,a+.5,q1-.2,col=INK,sz=38)
    lb(cv,c,'Chu Diên, nhà Thi Sách',1380,200,t,a+3.6,q1-.2,col=INK,sz=38)
    lb(cv,c,'luật nhà Hán trói buộc dân, Thi Sách bị giết',960,170,t,q1+.2,q2-.2,col=RED,sz=40)
    lb(cv,c,'Trưng Trắc tìm cách trả thù',960,170,t,q2+.1,b,col=RED,sz=44)
# 5 nổi dậy năm 40
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3;q=sb(5,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,520,1.15))])
    ngoai(cv,c,t,g=900,seed=5)
    put(cv,c,'t13x_hoi',960,560,s=1.05)
    for i in range(3):
        di(cv,c,'t13_spr_trung',-900+i*120,880+i*26,-200+i*140,880+i*26,t,a+i*.3,q,s=.55,bob=5,f=6+i*.5,ph=i,lat=True)
        di(cv,c,'t13_spr_trung',2800+i*120,880+i*26,2100+i*120,880+i*26,t,a+.2+i*.3,q,s=.55,bob=5,f=6.3+i*.5,ph=i+3)
    co_bay(cv,c,'t13_spr_trungco',1300,880,t,1.0,1)
    if t>q+2: di(cv,c,'t13_spr_dinh',1100,640,2400,600,t,q+2,b,s=.45,bob=5,f=9,k=.7)
    truoc(cv,c,t)
    seal(cv,'s40',1500,300,a+.3,t,s=.8,r=-4)
    lb(cv,c,'mùa xuân năm bốn mươi',960,160,t,a+.5,q-.2,col=RED,sz=44)
    lb(cv,c,'chiếm trụ sở của quan nhà Hán',960,160,t,q+.2,q+4,col=INK,sz=40)
    lb(cv,c,'Tô Định chạy về Nam Hải',960,160,t,q+4.2,b,col=RED,sz=42)
# 6 cả dân Giao Chỉ bị trói buộc
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3;q=sb(6,1)
    c=kc(t,[(a,(1300,560,1.06)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=6)
    put(cv,c,'t13x_troi',960,560,s=1.1)
    di(cv,c,'t13_spr_trai',-200,890,700,890,t,a,b,s=.6,bob=2,f=3)
    di(cv,c,'t13_spr_trai',-900,900,0,900,t,a+1,b,s=.55,bob=2,f=3.3,ph=1)
    di(cv,c,'t13_spr_1han',-60,880,840,880,t,a,b,s=.62,bob=3,f=4.5)
    if t>q:
        for i in range(8): stroke(cv,c,[(420+i*150,760),(500+i*150,770)],inn(t,q+.3+i*.3,.6),wid=5,col=RED,o=.7,head=False)
    truoc(cv,c,t)
    lb(cv,c,'tưởng là một mối thù riêng',960,170,t,a+.3,q-.2,col=INK,sz=44)
    lb(cv,c,'nhưng dân Giao Chỉ cùng bị trói buộc',960,170,t,q+.2,b,col=RED,sz=42)
# 7 Lạc Dương
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3;q=sb(7,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,520,1.12))])
    trong(cv,c,t,.65)
    put(cv,c,'t13x_trieu',960,560,s=1.1)
    di(cv,c,'t13_spr_quan',500,860,880,830,t,a+.3,q,s=.62,bob=2,f=3)
    for i in range(3): put(cv,c,'t13_spr_quan',1250+i*90,870,s=.55*GS,ay=1,r=8+6*math.sin(t*1.2+i),scale_px=1.5)
    if t>q: di(cv,c,'t13_spr_mavien',-300,880,400,880,t,q,b,s=.55,bob=4,f=6)
    smoke(cv,c,760,620,t,.8);smoke(cv,c,1160,620,t+1.3,.8)
    trong_truoc(cv,c,t)
    lb(cv,c,'Lạc Dương, kinh đô nhà Hán',960,170,t,a+.4,q-.2,col=INK,sz=42)
    seal(cv,'s42',1500,320,q+1.5,t,s=.8,r=4)
    lb(cv,c,'năm bốn mươi hai: cử Mã Viện',960,170,t,q+.2,b,col=RED,sz=42)
# 8a Mã Viện tiến quân qua núi
def S_8a(cv,t):
    a,b=T[8]-.3,sb(8,1)
    c=kc(t,[(a,(1200,540,1.1)),(b,(860,560,1.0))])
    ngoai(cv,c,t,g=860,seed=7,mist=.7)
    put(cv,c,'t13x_vien',960,540,s=1.0,o=.8)
    for r in range(3): di(cv,c,'t13_spr_han',-800-r*260,850+r*30,600-r*180,850+r*30,t,a+r*.3,b+1,s=.5+.05*r,bob=3,f=5+r*.4,ph=r)
    di(cv,c,'t13_spr_mavien',-200,860,900,860,t,a,b+1,s=.62,bob=5,f=6)
    truoc(cv,c,t)
    lb(cv,c,'Mã Viện, Phục Ba tướng quân',960,170,t,a+.4,b-.2,col=RED,sz=44)
# 8b thuyền lương theo bờ biển
def S_8b(cv,t):
    a,b=sb(8,1),sb(8,2)
    c=kc(t,[(a,(1200,560,1.1)),(b,(800,560,1.0))])
    put(cv,c,'t13_far',960,560,ay=1,k=.35,o=.8)
    river(cv,c,t,PAP,wl=600,stakes=False,cliffs=False,reeds=1,mist=.8,ridge_o=0,
          boats=[dict(name='t13_spr_thuyen',x=lerp(-300+i*380,800+i*380,inn(t,a-.3,b-a+1)),y=650+i*55+math.sin(t*1.8+i)*6,s=.75+.12*i,r=math.sin(t*1.4+i)*2.5) for i in range(4)])
    flock(cv,c,t,.6)
    lb(cv,c,'thuyền chở lương theo bờ biển',960,170,t,a+.3,b-.2,col=INK,sz=42)
# 8c bản đồ: hai đường tiến quân
def S_8c(cv,t):
    a,b=sb(8,2),E[8]+.3
    c=kc(t,[(a,(960,540,1.0)),(b,(960,540,1.04))])
    mapbg(cv,c,u=1)
    dl=P['daila'];dot(cv,c,*dl);tag(cv,c,dl[0]+24,dl[1]-6,'Mê Linh',dy=0,sz=28)
    stroke(cv,c,[(1500,300),(900,420),dl],inn(t,a+.5,max(b-a-1,1)),wid=8,col=HAN);pulse(cv,c,*dl,t)
    u=inn(t,a+.5,max(b-a-1,1))
    put(cv,c,'t13_spr_mavien',lerp(1500,dl[0],u),lerp(300,dl[1],u),s=.22,ay=1,r=2*math.sin(t*6))
    put(cv,c,'t13_spr_thuyen',lerp(1700,dl[0]+200,u),lerp(620,dl[1]+120,u)+4*math.sin(t*2),s=.22,ay=1)
    put(cv,c,'t13_spr_haiba',dl[0]-10,dl[1]-6,s=.28,ay=1,r=1.5*math.sin(t*1.7))
    lb(cv,c,'sử không ghi quân hai bà đông bao nhiêu',960,200,t,a+.3,b,col=RED,sz=42)
# 9a CẢNH TRỌNG TÂM: trận Lãng Bạc
def S_9a(cv,t):
    a,b=T[9]-.3,sb(9,1)
    hit=a+2.4
    sh=(6*math.sin(t*37)*(1-inn(t,hit+.4,.8))) if hit<t<hit+1.2 else 0
    c=kc(t,[(a,(760,560,1.08)),(hit,(960,580,1.04)),(b,(1120,560,1.1))],sh)
    put(cv,c,'t13_far',960,700,ay=1,k=.35,o=.9)
    river(cv,c,t,PAP,wl=640,stakes=False,cliffs=False,reeds=0,mist=.5,ridge_o=.6)
    put(cv,c,'t13x_langbac',960,560,s=1.0,o=.55)
    # nỏ nhà Hán bắn trước khi giáp trận
    arrows(cv,c,t,a+.2,hit+.6,[(260,700),(380,690)],[(1300,820),(1500,840)],n=10,h=120,per=.9,seed=4,col=HAN)
    arrows(cv,c,t,a+.8,b,[(1600,720),(1700,700)],[(500,820),(650,840)],n=6,h=120,per=1.1,seed=8,col=(.69,.16,.11))
    clash(cv,c,t,hit-1.4,b+2,'han','trung',xm=980,y=800,s=.92,push=1,seed=9,pre='t13_spr_',ten=False)
    di(cv,c,'t13_spr_mavien',-200,860,240,860,t,a,hit,s=.72,bob=4,f=6)
    co_bay(cv,c,'t13_spr_trungco',1600-inn(t,hit,b-hit)*140,880,t,1.1,lat=True)
    if t>hit:
        for k in range(5): put(cv,c,'mist',980+k*90-60,800-20*k,s=.4+.12*k,o=.3*(1-inn(t,hit+3,2)))
    truoc(cv,c,t)
    lb(cv,c,'Lãng Bạc',960,170,t,a+.3,b-.2,col=RED,sz=52)
    lb(cv,c,'sách cũ: Hồ Tây; nay: vùng núi Tiên Du',960,235,t,a+2.2,b-.2,col=INK,sz=32)
    lb(cv,c,'quân nhà Hán',450,300,t,a+.6,b,col=HAN,sz=36)
    lb(cv,c,'quân hai bà',1500,300,t,a+.6,b,col=RED,sz=36)
# 9b thắng lớn, ra hàng, lui về Cấm Khê
def S_9b(cv,t):
    a,b=sb(9,1),E[9]+.3;q2,q3=sb(9,2),sb(9,3)
    c=kc(t,[(a,(1000,560,1.0)),(b,(1100,560,1.12))])
    ngoai(cv,c,t,g=880,seed=8,mist=.7)
    put(cv,c,'t13x_hang',960,560,s=1.1)
    di(cv,c,'t13_spr_han',2500,880,1500,880,t,a,b,s=.6,bob=3,f=5,lat=True)
    di(cv,c,'t13_spr_trai',300,900,900,900,t,a+.5,q3,s=.6,bob=2,f=3)
    for k in range(int((q3-a)/1.3)+1):
        t0=a+.4+k*1.3
        if t0<t<t0+1.8: fall(cv,c,'t13_spr_1trung',600+k*70,880,t,t0,s=.9,dirn=1)
    if t>q3-.3: di(cv,c,'t13_spr_trung',900,890,-300,870,t,q3,b+1,s=.55,bob=5,f=6.5)
    truoc(cv,c,t)
    lb(cv,c,'Mã Viện thắng lớn',960,160,t,a+.3,q2-.2,col=RED,sz=46)
    lb(cv,c,'hàng nghìn người ngã xuống, hơn mười nghìn người hàng',960,160,t,q2+.2,q3-.2,col=INK,sz=38)
    lb(cv,c,'hai bà lui về Cấm Khê',960,160,t,q3+.1,b,col=RED,sz=44)
# 10 nhiều người bỏ đi
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3
    c=kc(t,[(a,(1200,560,1.1)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=9)
    put(cv,c,'t13x_roi',960,560,s=1.0)
    for i in range(4): di(cv,c,'t13_spr_1trung',900+i*80,880+(i%2)*20,-400+i*500,860+(i%2)*20,t,a+i*.5,b+1,s=.62,bob=4,f=5+i*.4,ph=i,lat=i%2==0)
    di(cv,c,'t13_spr_dan',1100,890,2400,870,t,a+.3,b,s=.6,bob=3,f=4.4)
    u=inn(t,a+1.5,2.5);put(cv,c,'t13_spr_trungco',1300,880,s=1.0*GS*.7,ay=1,r=-75*u,o=1-.5*u,scale_px=1.5)
    truoc(cv,c,t)
    lb(cv,c,'nhiều người bỏ đi',960,170,t,a+.5,b,col=RED,sz=46)
    lb(cv,c,'theo lời kể của Toàn thư',960,230,t,a+2,b,col=INK,sz=34)
# 11 Cấm Khê
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3;q1,q2=sb(11,1),sb(11,2)
    c=kc(t,[(a,(900,520,1.0)),(b,(1000,500,1.16))])
    ngoai(cv,c,t,g=860,seed=10,mist=1.0)
    put(cv,c,'t13x_camkhe',960,540,s=1.0,o=.85)
    di(cv,c,'t13_spr_han',-500,880,700,860,t,a,q2,s=.55,bob=3,f=5)
    di(cv,c,'t13_spr_trung',800,860,1700,800,t,a+.3,q2,s=.5,bob=4,f=6,lat=True)
    if t>q1: clash(cv,c,t,q1,b,'han','trung',xm=1250,y=770,s=.75,push=1,seed=11,pre='t13_spr_')
    truoc(cv,c,t)
    lb(cv,c,'Cấm Khê, chưa rõ ở đâu',960,170,t,a+.3,q1-.2,col=INK,sz=44)
    lb(cv,c,'quân hai bà',1300,330,t,a+.6,b,col=RED,sz=32);lb(cv,c,'quân Mã Viện',600,330,t,a+.6,b,col=HAN,sz=32)
    lb(cv,c,'Mã Viện đuổi theo, đánh nhiều trận',960,170,t,q1+.2,q2-.2,col=RED,sz=40)
    seal(cv,'s43',1500,300,q2-.2,t,s=.8,r=4)
    lb(cv,c,'năm bốn mươi ba: bị cô lập, thua trận',960,170,t,q2+.2,b,col=RED,sz=40)
# 12a sách kể khác nhau
def S_12a(cv,t):
    a,b=T[12]-.3,sb(12,3)
    c=kc(t,[(a,(960,540,1.0)),(b,(980,540,1.1))])
    trong(cv,c,t,.6)
    put(cv,c,'t13x_sach',960,560,s=1.1)
    for j in range(6): viet(cv,c,[(700+j*90,560),(700+j*90,600)],t,a+.5+j*.7,.5,wid=4,o=.8)
    di(cv,c,'t13_spr_quan',-300,860,420,860,t,a,b,s=.62,bob=2,f=3)
    di(cv,c,'t13_spr_quan',2300,860,1550,860,t,a+.8,b,s=.6,bob=2,f=3.3,lat=True)
    smoke(cv,c,960,640,t,.8)
    trong_truoc(cv,c,t)
    lb(cv,c,'sách kể khác nhau',960,150,t,a+.3,sb(12,1)-.2,col=RED,sz=46)
    lb(cv,c,'Hậu Hán thư: bị chém, đầu gửi về Lạc Dương',960,150,t,sb(12,1)+.2,sb(12,2)-.2,col=INK,sz=38)
    lb(cv,c,'Toàn thư: chỉ ghi hai bà thua trận',960,150,t,sb(12,2)+.2,b,col=INK,sz=38)
# 12b sông Hát, đền Hát Môn
def S_12b(cv,t):
    a,b=sb(12,3),E[12]+.3
    c=kc(t,[(a,(1100,560,1.06)),(b,(900,560,1.0))])
    put(cv,c,'t13_far',960,640,ay=1,k=.35,o=.8)
    river(cv,c,t,PAP,wl=640,stakes=False,cliffs=False,reeds=1,mist=.8,ridge_o=.4)
    put(cv,c,'t13x_hat',960,540,s=1.0,o=.8)
    di(cv,c,'t13_spr_thuyen',1700,700,1100,690,t,a,b,s=.5,bob=3,f=1.6,lac=2.5,k=.9)
    di(cv,c,'t13_spr_dan',-300,880,500,880,t,a,b,s=.55,bob=3,f=4)
    smoke(cv,c,1500,560,t,.9)
    put(cv,c,'t13_spr_haiba',700,620,s=.7,ay=1,o=.25+.15*math.sin(t*1.1)**2,k=.8)
    lb(cv,c,'sông Hát, đền Hát Môn: chuyện dân gian giữ lại',960,170,t,a+.3,sb(12,4)-.2,col=INK,sz=40)
    lb(cv,c,'cách kể nào cũng không thay được cách kể khác',960,170,t,sb(12,4)+.2,b,col=RED,sz=40)
# 13a CẢNH TRỌNG TÂM: nấu chảy trống đồng
def S_13a(cv,t):
    a=T[13]-.3;b=T[13]+(E[13]-T[13])*.5
    c=kc(t,[(a,(1100,560,1.0)),(b,(860,540,1.16))])
    ngoai(cv,c,t,g=880,seed=11,far=.6,midv=.6,mist=.3)
    put(cv,c,'t13x_lo',960,560,s=1.1)
    for i in range(3):
        t0=a+.3+i*1.4;u=inn(t,t0,2.4)
        if t>t0: put(cv,c,'t13_spr_trong',lerp(1900,980,u),lerp(870,640,u*u)+ (0 if u<1 else 40*inn(t,t0+2.4,1.5)),s=.75,ay=1,o=1-inn(t,t0+2.6,1.2),r=10*u,scale_px=1.5)
    di(cv,c,'t13_spr_han',2600,880,1500,880,t,a,b,s=.55,bob=3,f=5,lat=True)
    for k in range(3): flick(cv,c,840+k*40,500,t+k,1.0)
    smoke(cv,c,840,380,t,1.4);smoke(cv,c,900,360,t+1,1.2)
    for i in range(8): dust(cv,c,760+(i%3)*40,520-((t*70+i*60)%320),o=.3,s=.25)
    truoc(cv,c,t)
    lb(cv,c,'nấu chảy trống đồng',960,160,t,a+.4,b-.2,col=RED,sz=48)
    lb(cv,c,'biểu tượng quyền của thủ lĩnh người bản địa',960,220,t,a+2.5,b-.2,col=INK,sz=34)
# 13b tượng ngựa, quân Hán chết vì dịch
def S_13b(cv,t):
    a=T[13]+(E[13]-T[13])*.5;b=E[13]+.3;q=b-3
    c=kc(t,[(a,(900,560,1.08)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=12,mist=.9)
    put(cv,c,'t13x_ngua',960,560,s=1.1)
    di(cv,c,'t13_spr_ngua',-200,880,900,880,t,a,q,s=.7,bob=2,f=3,lac=1)
    di(cv,c,'t13_spr_han',-700,880,400,880,t,a,q,s=.55,bob=3,f=5)
    di(cv,c,'t13_spr_mavien',-400,880,600,880,t,a+.5,q,s=.6,bob=4,f=6)
    if t>q:
        for k in range(4):
            t0=q+.2+k*.6
            if t>t0: fall(cv,c,'t13_spr_1han',1200+k*120,880,t,t0,s=.9,dirn=1)
        for k in range(3): put(cv,c,'mist',1100+k*300+40*math.sin(t+k),760,s=1.2,o=.4)
    truoc(cv,c,t)
    lb(cv,c,'đúc thành tượng ngựa, dâng vua năm bốn mươi bốn',960,160,t,a+.3,q,col=INK,sz=38)
    seal(cv,'s44',1500,320,a+.8,t,s=.8,r=4)
    lb(cv,c,'quân Mã Viện chết gần một nửa vì hơi độc và dịch bệnh',960,160,t,q,b,col=RED,sz=36)
# 14 vì sao không giữ nổi
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3;q1,q2,q3=sb(14,1),sb(14,2),sb(14,3)
    c=kc(t,[(a,(1200,560,1.05)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=13,mist=.6)
    put(cv,c,'t13x_thanh65',960,560,s=1.0,o=.85)
    if q2-.3<t<q3+.5: di(cv,c,'t13_spr_thuyen',2300,700,1300,690,t,q2,q3,s=.55,bob=3,f=1.8,k=.8,lac=2)
    di(cv,c,'t13_spr_1trung',600,880,-300,880,t,q2,b,s=.6,bob=4,f=5,lat=True)
    co_bay(cv,c,'t13_spr_trungco',1400,880,t,1.0)
    if t>q3:
        for i in range(10): dot(cv,c,300+i*150,420-(i%2)*30,o=inn(t,q3+i*.25,.3),col=RED,r=6)
        di(cv,c,'t13_spr_trung',-600,890,300,890,t,q3,b,s=.55,bob=5,f=6.5,lat=True)
    truoc(cv,c,t)
    lb(cv,c,'sử không đưa ra một lý do duy nhất',960,170,t,q1+.2,q2-.2,col=INK,sz=42)
    lb(cv,c,'một đạo quân có thuyền chở lương theo bờ biển',960,170,t,q2+.2,q3-.2,col=RED,sz=38)
    lb(cv,c,'Lê Văn Hưu: sáu mươi lăm thành đáp lại một tiếng gọi',960,170,t,q3+.2,b,col=INK,sz=36)
# 15 kết
def S_15(cv,t):
    a=T[15]-.3;b=E[15]+4
    c=kc(t,[(a,(960,560,1.0)),(b,(960,520,1.1))])
    ngoai(cv,c,t,g=880,seed=14,mist=.6)
    put(cv,c,'t13x_cuoi',960,560,s=1.1)
    put(cv,c,'t13_spr_haiba',1300,880,s=.9*GS,ay=1,o=.55,r=1.5*math.sin(t*1.2),scale_px=1.5)
    di(cv,c,'t13_spr_dan',-300,890,700,890,t,a,b,s=.55,bob=3,f=4)
    smoke(cv,c,700,640,t,1.0)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    tx=text('Hai Bà Trưng, năm 40 đến 43',54,INK,700);put_screen(cv,wipe(tx,inn(t,a+.8,1.4),0,.3,seed=13),W/2,170)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,245,inn(t,E[15]+.6,1))
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
    flock=lambda *a,**k:None
S=lambda n:T[n]-.3
SH=[(0,S(2),S_1),(S(2),sb(2,1),S_2a),(sb(2,1),S(3),S_2b),(S(3),S(4),S_3),(S(4),S(5),S_4),(S(5),S(6),S_5),(S(6),S(7),S_6),(S(7),S(8),S_7),
 (S(8),sb(8,1),S_8a),(sb(8,1),sb(8,2),S_8b),(sb(8,2),S(9),S_8c),(S(9),sb(9,1),S_9a),(sb(9,1),S(10),S_9b),(S(10),S(11),S_10),(S(11),S(12),S_11),
 (S(12),sb(12,3),S_12a),(sb(12,3),S(13),S_12b),(S(13),T[13]+(E[13]-T[13])*.5,S_13a),(T[13]+(E[13]-T[13])*.5,S(14),S_13b),(S(14),S(15),S_14),(S(15),V.TOTAL+1,S_15)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm13_full.json'))
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
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'LÃNG BẠC · CẤM KHÊ','stitle13',.55)
    caps(cv,t)
V.NHAN={8:'Mã Viện – tướng nhà Hán'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
