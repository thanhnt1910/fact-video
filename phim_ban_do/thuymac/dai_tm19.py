# Bản dài tm19: Phùng Hưng, năm 791 (bản 1). Khung: người được gọi là cha mẹ (Bố Cái Đại Vương).
# Hình người kiểu mới (t19n_*, nguoi18, độ phân giải gấp ba). Hình ảnh lặp lại: tấm biển gỗ Bố Cái (đoạn 1, 3, 17, 25) và cổng làng Đường Lâm (4, 10, 24, 25).
# Mở đầu giọt mực; quét mực khi vây phủ; chia đôi cuộn sử (2, 15, 22); bộ đếm làng theo ông (6), vòng lửa vây phủ (11); dấu năm 722 → 791 (13).
import math,re,json,os
import numpy as np
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from engine import ragged,asc
from fx_tran import arrows,dust,sparks,fall
from tran_fx import clash
from dai_tm2 import big,lb
P=PTS
V=K.setup('tm19',{4:4.0})
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
    put(cv,c,'t19_far',960+seed*60,g-120,ay=1,k=.35,o=far)
    put(cv,c,'t19_mid',960-seed*40,g+30,ay=1,k=.62,o=midv)
    suong(cv,c,t,g-260,mist,seed)
def truoc(cv,c,t,o=1):
    put(cv,c,'t19_frontL',-120,1120,ax=0,ay=1,k=1.3,s=.85,r=1.2*math.sin(t*.8),o=o)
    put(cv,c,'t19_frontR',2040,1120,ax=1,ay=1,k=1.3,s=.8,r=1.2*math.sin(t*.7+1),o=o)
def di(cv,c,name,x0,y0,x1,y1,t,a,b,s=1.0,o=.97,bob=4,f=5,ph=0,k=1.0,r=0,lac=1.2,lat=False):
    if y0>700 and k==1.0: s*=GS;bob*=GS
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;y=y0+(y1-y0)*u-abs(math.sin(t*f+ph))*bob*(1 if 0<u<1 else .3)
    put(cv,c,Af(name) if lat else name,x,y,s=s,o=o,k=k,r=r+lac*math.sin(t*f*.5+ph),ay=1,scale_px=asc(name))
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
        rg=np.random.default_rng(19);a=rg.random((34,60)).astype(np.float32)
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
DUONGC=(.17,.29,.45)
GOLDC=(.79,.64,.35)
def nv(cv,c,name,x,y,t,s=.7,r=0,o=1.0,flip=False):
    """nhân vật đứng, thở nhẹ"""
    put(cv,c,Af(name) if flip else name,x,y-2*math.sin(t*1.6+x),s=s*GS if y>700 else s,ay=1,o=o,r=r+.6*math.sin(t*1.1+x),scale_px=asc(name))
def bien(cv,x,y,t,chu='',u=1.0,o=1.0,s=.9,phu=''):
    """hình ảnh lặp lại: tấm biển gỗ thờ Bố Cái"""
    put(cv,C0,'t19_bien',x,y,s=s,o=o,r=.4*math.sin(t*.6))
    if FREEZE: return
    if chu: put_screen(cv,wipe(text(chu,int(84*s/.9*min(1,9/max(len(chu),1))),GOLDC,700),u,0,.25,seed=19),x,y-6,o)
    if phu: put_screen(cv,text(phu,int(34*s/.9),RED,700),x,y+int(140*s/.9),o*u)
def cuon(cv,x,y,t,tieu,chu,col=None,o=1.0,s=.62,sz=48,u=1.0,gach=0.0):
    put(cv,C0,'t19_cuon',x,y,s=s,o=o,r=.5*math.sin(t*.7+x))
    if FREEZE: return
    put_screen(cv,text(tieu,28,INK,700),x,y-170*s/.62,o)
    for k,ln in enumerate(chu.split('|')): put_screen(cv,wipe(text(ln,sz,col if col is not None else RED,700),u,0,.25,seed=int(x)+k),x,y-20+k*(sz+16),o)
    if gach>0: stroke(cv,C0,[(x-150*s/.62,y+10),(x+150*s/.62,y-20)],gach,wid=10,col=RED,o=.9*o,head=False)
def dot_dem(cv,x,y,n,tong,cot=8,col=RED,o=1.0,gap=46,r=15):
    for k in range(tong): dot(cv,C0,x+(k%cot)*gap,y+(k//cot)*gap,o=o*(.95 if k<n else .25),col=col if k<n else INK,r=r)
def pulse(cv,c,x,y,t,col=RED):
    for k in range(2):
        u=((t*.6+k*.5)%1.0);dot(cv,c,x,y,o=.6*(1-u),col=col,r=int(8+40*u))
# ---- 1: giọt mực loang thành đền thờ; tấm biển chưa có chữ
def den(cv,t,a,b):
    c=kc(t,[(a,(960,600,1.0)),(b,(960,520,1.14))])
    ngoai(cv,c,t,g=880,seed=1,mist=.4)
    put(cv,c,'t19x_den',960,560,s=1.1)
    di(cv,c,'t19n_dan',-200,890,520,890,t,a+.3,b+2,s=.62,bob=2,f=3.2)
    di(cv,c,'t19n_dan2',2300,890,1450,890,t,a,b+2,s=.6,bob=2,f=3.4,lat=True)
    for i in range(3): smoke(cv,c,930+i*20,520,t+i,.7)
    truoc(cv,c,t)
    return c
def S_1(cv,t):
    a,b=0,E[1]+.3;td=.95
    sc=PAP.copy();den(sc,t,a,b)
    if FREEZE: cv[:]=sc;return
    if t<td:
        y=-40+(540+40)*(t/td)**2
        m=loang(960,y,22,6);cv[:]=cv*(1-m)+np.array(INK,np.float32)*m
    else:
        u=inn(t,td,1.6);r=30+u*1300
        m=loang(960,540,r,60);rim=np.clip(loang(960,540,r,60)-loang(960,540,r-70,60),0,1)
        cv[:]=cv*(1-m)+sc*m;cv[:]=cv*(1-rim*.75)+np.array(INK,np.float32)*rim*.75
    q=sb(1,1)
    bien(cv,960,250,t,'? ?',u=inn(t,1.8,.6),s=.7)
    big(cv,'GỌI ÔNG LÀ CHA MẸ',t,q,b,RED,620,96,seed=1)
# ---- 2: đánh tới tận phủ thành; sử nhà Đường không ghi tên (chia đôi)
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3;q=sb(2,1)
    c=kc(t,[(a,(960,420,1.2)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=900,seed=2)
    put(cv,c,'t19x_phu',960,520,s=.95)
    for r in range(2): di(cv,c,'t19n_ta',-900-r*250,880+r*30,450-r*200,880+r*30,t,a+r*.3,b+1,s=.62,bob=5,f=6.4+r*.4,ph=r)
    di(cv,c,'t19n_1duong',1400,880,2400,860,t,a+.5,b+1,s=.65,bob=6,f=8,lac=2)
    truoc(cv,c,t)
    if not FREEZE and t>q-.2:
        ink_wash(cv,.4*inn(t,q-.2,.5))
        cuon(cv,1400,500,t,'SỬ NHÀ ĐƯỜNG','? ? ?',col=DUONGC,s=.6,sz=60,u=inn(t,q,.6))
    lb(cv,C0,'đánh tới tận nơi quan nhà Đường đóng',960,150,t,a+.3,q-.2,col=RED,sz=42)
# ---- 3: câu hỏi (tấm biển, cận cảnh)
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3
    c=kc(t,[(a,(960,560,1.0)),(b,(1060,560,1.1))])
    ngoai(cv,c,t,g=880,seed=3,mist=.6,far=.6,midv=.6)
    di(cv,c,'t19n_dan',-300,890,320,890,t,a,b,s=.6,bob=2,f=3)
    di(cv,c,'t19n_dan2',2300,890,1700,890,t,a,b,s=.58,bob=2,f=3.4,lat=True)
    di(cv,c,'t19n_an',2600,890,2000,890,t,a+.3,b,s=.58,bob=2,f=3.2,lat=True)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.35)
    bien(cv,960,470,t,'? ?',s=1.0,u=1)
# ---- 4: làng Đường Lâm (cổng làng, hình ảnh lặp lại)
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3;q=sb(4,1)
    c=kc(t,[(a,(1300,560,1.08)),(b,(950,560,1.0))])
    ngoai(cv,c,t,g=880,seed=4)
    put(cv,c,'t19x_duonglam',960,560,s=1.0)
    di(cv,c,'t19n_dan',-300,890,600,890,t,a,b+1,s=.6,bob=2,f=3.2)
    di(cv,c,'t19n_dan2',2300,890,1500,890,t,a+.4,b+1,s=.58,bob=2,f=3.4,lat=True)
    di(cv,c,'t19n_trau',2600,890,1800,890,t,a,b+3,s=.5,bob=2,f=2.4,lat=True,lac=.6)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    lb(cv,C0,'làng Đường Lâm, Sơn Tây ngày nay',960,170,t,a+.3,q-.2,col=RED,sz=44)
    lb(cv,C0,'nước ta dưới sự cai trị của nhà Đường',960,170,t,q+.2,b,col=INK,sz=42)
# ---- 5: Phùng Hưng, sức khỏe, vật trâu
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3;q=sb(5,1)
    c=kc(t,[(a,(960,560,1.0)),(q,(900,560,1.12)),(b,(860,540,1.2))])
    ngoai(cv,c,t,g=880,seed=5)
    put(cv,c,'t19x_trau',960,560,s=1.1,o=.6)
    u=inn(t,q,1.2)
    put(cv,c,'t19n_trau',760-30*u,880,s=.95*GS,ay=1,r=-4*u+1.5*math.sin(t*3),scale_px=3)
    nv(cv,c,'t19n_ph2',1060,885,t,s=.78)
    di(cv,c,'t19n_dan',2300,890,1500,890,t,a,b,s=.55,bob=2,f=3.2,lat=True)
    di(cv,c,'t19n_dan2',-400,890,300,890,t,a+.4,b,s=.55,bob=2,f=3.4)
    truoc(cv,c,t)
    lb(cv,C0,'Phùng Hưng',960,170,t,a+.3,q-.2,col=RED,sz=52)
    lb(cv,C0,'sử cũ chép: vật được trâu, đánh được hổ',960,170,t,q+.2,b,col=INK,sz=40)
# ---- 6: thời loạn, thu phục các làng (bộ đếm làng)
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3;q=sb(6,1)
    c=kc(t,[(a,(1300,560,1.05)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=6,mist=.6)
    put(cv,c,'t19x_loan',960,560,s=1.0)
    nv(cv,c,'t19n_ph',900,885,t,s=.72);nv(cv,c,'t19n_hai',1060,885,t,s=.68)
    for i in range(3): di(cv,c,'t19n_dan' if i%2 else 't19n_dan2',-600-i*220,890,400+i*150,890,t,q+i*.4,b+1,s=.55,bob=2,f=3.4+i*.3,ph=i)
    for x in (300,1700): smoke(cv,c,x,560,t,1.1)
    truoc(cv,c,t)
    if not FREEZE and t>q:
        n=int(12*inn(t,q,b-q-.4));put_screen(cv,band(470,190,PAPER,.88,20),1500,330,inn(t,q,.3))
        dot_dem(cv,1360,320,n,12,cot=6,gap=56,r=17);put_screen(cv,text(f'{n} làng theo về',38,RED,700),1500,260,inn(t,q,.3))
    lb(cv,C0,'xứ ta có loạn',960,170,t,a+.3,q-.2,col=INK,sz=46)
    lb(cv,C0,'cùng em là Phùng Hãi',960,170,t,q+.2,b,col=RED,sz=44)
# ---- 7: Đô Quân
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3;q=sb(7,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,520,1.15))])
    ngoai(cv,c,t,g=880,seed=7)
    put(cv,c,'t19x_doquan',960,560,s=1.1)
    for i in range(3): di(cv,c,'t19n_ta',-900-i*200,885+i*20,-200+i*220,885+i*20,t,a+i*.4,b,s=.55,bob=4,f=5.4+i*.3,ph=i)
    di(cv,c,'t19n_dan',2300,890,1500,890,t,a+.3,b,s=.55,bob=2,f=3.2,lat=True)
    truoc(cv,c,t)
    if not FREEZE: put_screen(cv,band(420,120,PAPER,.88,20),1500,330,inn(t,a+.6,.4));put_screen(cv,text('ĐÔ QUÂN',58,RED,700),1500,315,inn(t,a+.6,.4));put_screen(cv,text('người đứng đầu cả vùng',28,INK,700),1500,365,inn(t,a+1.2,.4))
    lb(cv,C0,'một vùng tự giữ lấy mình, ngay gần quan nhà Đường',960,170,t,q+.2,b,col=INK,sz=38)
# ---- 8: Cao Chính Bình thu thuế nặng
def S_8(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1)
    c=kc(t,[(a,(960,520,1.15)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=8,far=.5,midv=.5)
    put(cv,c,'t19x_thue',960,630,s=1.1)
    nv(cv,c,'t19n_cao',960,885,t,s=.72)
    for i in range(3): di(cv,c,'t19n_dan' if i%2 else 't19n_dan2',-500-i*200,890,300+i*130,890,t,a+i*.4,b,s=.55,bob=3,f=3+i*.2,ph=i)
    di(cv,c,'t19n_1duong',2300,885,1500,885,t,a,b,s=.6,bob=2,f=3.2,lat=True)
    truoc(cv,c,t)
    lb(cv,C0,'người đứng đầu bộ máy cai trị',960,230,t,a+.3,q-.2,col=DUONGC,sz=40)
    lb(cv,C0,'bắt dân nộp thuế rất nặng',960,150,t,q+.2,b,col=RED,sz=44)
# ---- 9: đánh mãi không thắng (quét mực sang trận)
def danhmai(cv,t,a,b):
    hit=a+1.2;sh=(4*math.sin(t*37)*(1-inn(t,hit+.3,.6))) if hit<t<hit+.9 and not FREEZE else 0
    c=kc(t,[(a,(800,500,1.05)),(b,(1000,540,1.0))],sh)
    ngoai(cv,c,t,g=900,seed=9)
    put(cv,c,'t19x_danhmai',960,520,s=.95)
    for r in range(2): di(cv,c,'t19n_ta',-700-r*250,880+r*30,500-r*200,880+r*30,t,a+r*.3,b,s=.6,bob=5,f=6.4+r*.4,ph=r)
    nv(cv,c,'t19n_ph',700,885,t,s=.74)
    arrows(cv,c,t,a+.3,b,[(1500,420),(1600,430)],[(600,800),(800,820)],n=8,h=120,per=1.0,seed=9,col=DUONGC)
    truoc(cv,c,t)
def S_9(cv,t):
    a,b=T[9]-.3,E[9]+.3;q=sb(9,1)
    if t<a+1.0 and not FREEZE:
        A_=PAP.copy();S_8(A_,t);B_=PAP.copy();danhmai(B_,t,a,b)
        m=quet(inn(t,a-.1,1.0));cv[:]=A_*(1-m)+B_*m
    else: danhmai(cv,t,a,b)
    lb(cv,C0,'đánh mãi không thắng',960,170,t,a+.6,q-.2,col=RED,sz=46)
    lb(cv,C0,'thứ giúp ông thắng: kế của một người cùng làng',960,170,t,q+.2,b,col=INK,sz=40)
# ---- 10: Đỗ Anh Hàn bày kế (đêm, cổng làng)
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3;q=sb(10,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(900,540,1.12))])
    ngoai(cv,c,t,g=880,seed=10,far=.5,midv=.5,mist=.4)
    put(cv,c,'t19x_ke',960,560,s=1.1)
    nv(cv,c,'t19n_han',800,885,t,s=.72);nv(cv,c,'t19n_ph',1080,885,t,s=.74,flip=True)
    flick(cv,c,940,880,t,.6)
    di(cv,c,'t19n_1ta',2300,890,1600,890,t,a,b,s=.6,bob=3,f=4,lat=True)
    di(cv,c,'t19n_dan',-400,890,300,890,t,a+.3,b,s=.55,bob=2,f=3.2)
    truoc(cv,c,t)
    if not FREEZE:
        ink_wash(cv,.25,col=np.array((.15,.15,.25),np.float32))
        if t>q:
            u=inn(t,q,1.6)
            for k in range(10):
                ang=k/10*math.pi*2;x=1460+math.cos(ang)*150;y=340+math.sin(ang)*90
                if k/10<u: dot(cv,C0,x,y,col=RED,r=12)
            put_screen(cv,text('vây kín',40,RED,700),1460,340,u)
# ---- 11: tháng tư 791, vây phủ thành (vòng lửa)
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3;q=sb(11,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1100,520,1.12))])
    put(cv,c,'t19_far',960,560,ay=1,k=.35,o=.6)
    put(cv,c,'t19x_vay',960,560,s=1.0)
    for r in range(3): di(cv,c,'t19n_ta',-800-r*240,880+r*24,300-r*180,880+r*24,t,a+r*.3,b+1,s=.55,bob=4,f=5.4+r*.3,ph=r)
    for k in range(6): flick(cv,c,300+k*300,780,t+k,.5)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.2,col=np.array((.15,.12,.2),np.float32))
    seal(cv,'s791',1560,330,q+.4,t,s=.8,r=4)
    lb(cv,C0,'sử không ghi kế ấy cụ thể ra sao',960,150,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'tháng tư năm 791: phủ thành bị vây',960,150,t,q+.2,b,col=RED,sz=44)
# ---- 12: Cao Chính Bình lo sợ mà chết; vào phủ thành (cảnh trọng tâm)
def S_12(cv,t):
    a,b=T[12]-.3,E[12]+.3;q=sb(12,1)
    if t<q-.3 or FREEZE:
        c=kc(t,[(a,(960,520,1.2)),(q,(960,540,1.28))])
        ngoai(cv,c,t,g=880,seed=12,far=.5,midv=.5,mist=.7)
        nv(cv,c,'t19n_cao',960,885,t,s=.85,r=-3*inn(t,a+.5,2))
        di(cv,c,'t19n_1duong',300,885,-200,885,t,a,q,s=.62,bob=4,f=6,lat=True)
        di(cv,c,'t19n_1duong',1600,885,2300,885,t,a+.3,q,s=.62,bob=4,f=6)
        di(cv,c,'t19n_duong',1300,890,2400,890,t,a+.6,q,s=.5,bob=4,f=6.4,ph=1)
        truoc(cv,c,t)
        if not FREEZE: ink_wash(cv,.35*inn(t,a,1.5))
    else:
        c=kc(t,[(q-.3,(1100,560,1.08)),(b,(1000,540,1.0))])
        ngoai(cv,c,t,g=880,seed=13)
        put(cv,c,'t19x_vaophu',960,520,s=.95)
        for r in range(2): di(cv,c,'t19n_ta',-700-r*240,885+r*24,700-r*160,885+r*24,t,q-.3+r*.3,b+1,s=.6,bob=4,f=5.6+r*.3,ph=r)
        di(cv,c,'t19n_ph2',-200,885,820,885,t,q-.3,b,s=.76,bob=4,f=5)
        di(cv,c,'t19n_dan',2300,890,1600,890,t,q,b,s=.55,bob=2,f=3.2,lat=True)
        truoc(cv,c,t)
        if not FREEZE: ink_wash(cv,.1,col=np.array((.7,.45,.15),np.float32))
    lb(cv,C0,'Cao Chính Bình lo sợ quá mà chết',960,170,t,a+.3,q-.3,col=DUONGC,sz=44)
    lb(cv,C0,'Phùng Hưng vào ở trong phủ thành',960,170,t,q+.2,b,col=RED,sz=44)
# ---- 13: gần bảy mươi năm sau Mai Thúc Loan (hai dấu năm)
def S_13(cv,t):
    a,b=T[13]-.3,E[13]+.3
    c=kc(t,[(a,(960,560,1.0)),(b,(1060,540,1.08))])
    ngoai(cv,c,t,g=880,seed=14,mist=.5)
    nv(cv,c,'t19n_ph',1300,885,t,s=.78)
    for r in range(2): di(cv,c,'t19n_ta',-600-r*200,885+r*24,500-r*160,885+r*24,t,a+r*.3,b+1,s=.55,bob=4,f=5.4,ph=r)
    di(cv,c,'t19n_dan',2300,890,1700,890,t,a,b,s=.55,bob=2,f=3.2,lat=True)
    truoc(cv,c,t)
    if not FREEZE:
        ink_wash(cv,.25)
        seal(cv,'s722b',600,330,a+.3,t,s=.9,r=-4);put_screen(cv,text('Mai Thúc Loan',32,INK,700),600,430,inn(t,a+.4,.4))
        u=inn(t,a+1.0,1.6);stroke(cv,C0,[(720,330),(1180,330)],u,wid=6,col=RED,o=.8)
        seal(cv,'s791',1320,330,a+2.2,t,s=.9,r=4);put_screen(cv,text('Phùng Hưng',32,RED,700),1320,430,inn(t,a+2.3,.4))
        put_screen(cv,text('gần bảy mươi năm',34,INK,700),950,290,u)
# ---- 14: ít lâu sau thì mất
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3;q=sb(14,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.1))])
    ngoai(cv,c,t,g=880,seed=15,far=.5,midv=.5,mist=.6)
    put(cv,c,'t19x_mat',960,630,s=1.1)
    for i in range(2): di(cv,c,'t19n_dan' if i else 't19n_dan2',-400-i*200,890,250+i*150,890,t,a+i*.4,b,s=.55,bob=2,f=2.6,ph=i)
    di(cv,c,'t19n_1ta',2300,890,1700,890,t,a,b,s=.58,bob=2,f=2.8,lat=True)
    nv(cv,c,'t19n_an',1450,885,t,s=.62,flip=True)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3*inn(t,a,1.2))
    lb(cv,C0,'nhưng ông không giữ được lâu',960,150,t,a+.3,q-.2,col=INK,sz=44)
    lb(cv,C0,'Toàn thư, Cương mục: vào phủ thành chưa bao lâu thì mất',960,150,t,q+.2,b,col=RED,sz=36)
# ---- 15: hai cách ghi (chia đôi cuộn sử)
def S_15(cv,t):
    a,b=T[15]-.3,E[15]+.3;q=sb(15,1)
    c=kc(t,[(a,(960,560,1.04)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=16,mist=.5,far=.6,midv=.6)
    di(cv,c,'t19n_han',-300,885,260,885,t,a,b,s=.6,bob=1,f=2)
    di(cv,c,'t19n_dan',2300,890,1700,890,t,a,b,s=.55,bob=2,f=3.2,lat=True)
    di(cv,c,'t19n_dan2',2600,890,2000,890,t,a+.5,b,s=.52,bob=2,f=3.4,lat=True)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3)
    cuon(cv,560,500,t,'TOÀN THƯ · CƯƠNG MỤC','ít lâu sau|thì mất',col=INK,s=.6,sz=46)
    cuon(cv,1360,500,t,'VIỆT ĐIỆN U LINH','nắm quyền|bảy năm',s=.6,sz=46,u=inn(t,a+.6,.8))
    lb(cv,C0,'đến nay hai cách ghi chưa được làm rõ',960,860,t,q+.2,b,col=INK,sz=36)
# ---- 16: lập Phùng An; danh hiệu Bố Cái Đại Vương
def S_16(cv,t):
    a,b=T[16]-.3,E[16]+.3;q=sb(16,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,520,1.14))])
    ngoai(cv,c,t,g=880,seed=17)
    put(cv,c,'t19x_lap',960,560,s=1.1)
    nv(cv,c,'t19n_an',960,885,t,s=.72)
    for i in range(3): di(cv,c,'t19n_ta',-900-i*200,885+i*20,-200+i*220,885+i*20,t,a+i*.4,b,s=.5,bob=3,f=4.6,ph=i)
    di(cv,c,'t19n_dan',2300,890,1500,890,t,a,b,s=.55,bob=2,f=3.2,lat=True)
    truoc(cv,c,t)
    lb(cv,C0,'mọi người lập con ông là Phùng An',960,150,t,a+.3,q-.2,col=INK,sz=44)
    if not FREEZE and t>q: bien(cv,960,330,t,'BỐ CÁI ĐẠI VƯƠNG',u=inn(t,q+.2,1.0),s=.75,o=inn(t,q,.4))
# ---- 17: bố là cha, cái là mẹ (tấm biển, cận cảnh)
def S_17(cv,t):
    a,b=T[17]-.3,E[17]+.3;q=sb(17,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.06))])
    ngoai(cv,c,t,g=880,seed=18,mist=.5,far=.5,midv=.5)
    di(cv,c,'t19n_dan',-300,890,300,890,t,a,b,s=.6,bob=2,f=3)
    di(cv,c,'t19n_dan2',2300,890,1700,890,t,a,b,s=.58,bob=2,f=3.4,lat=True)
    di(cv,c,'t19n_an',2600,890,2000,890,t,a+.3,b,s=.58,bob=2,f=3.2,lat=True)
    for i in range(3): smoke(cv,c,960+i*30,800,t+i,.7)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.35)
    bien(cv,960,420,t,'BỐ CÁI',s=1.0)
    if not FREEZE:
        put_screen(cv,text('bố = cha',46,RED,700),760,640,inn(t,a+.6,.4));put_screen(cv,text('cái = mẹ',46,RED,700),1160,640,inn(t,a+1.4,.4))
        if t>q: put_screen(cv,band(760,80,PAPER,.9,14),960,760,inn(t,q,.4));put_screen(cv,text('vị vua được coi như cha mẹ',40,INK,700),960,758,inn(t,q,.4))
# ---- 18: dân thờ ông hơn một nghìn năm
def S_18(cv,t):
    a,b=T[18]-.3,E[18]+.3
    c=kc(t,[(a,(960,500,1.06)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=19)
    put(cv,c,'t19x_thocung',960,560,s=1.0)
    for i in range(3): smoke(cv,c,1150+i*30,520,t+i,.7)
    for i in range(3): di(cv,c,'t19n_dan' if i%2 else 't19n_dan2',-400-i*300,890+i*14,500+i*90,890+i*14,t,a+i*.6,b,s=.5,bob=2,f=3.4+i*.3,ph=i)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    if not FREEZE:
        n=int(1200*inn(t,a+.5,b-a-1));put_screen(cv,band(440,100,PAPER,.88,16),1500,300,inn(t,a+.4,.4));put_screen(cv,text(f'{n} năm' if n<1000 else 'hơn 1.000 năm',42,RED,700),1500,300,inn(t,a+.4,.4))
    lb(cv,C0,'con ông đặt, người dân giữ lại',960,150,t,a+.3,b,col=INK,sz=42)
# ---- 19: nhà Đường cử Triệu Xương, sai người đến thuyết phục
def S_19(cv,t):
    a,b=T[19]-.3,E[19]+.3;q=sb(19,1)
    c=kc(t,[(a,(1200,560,1.05)),(b,(900,560,1.0))])
    ngoai(cv,c,t,g=880,seed=20,mist=.5)
    put(cv,c,'t19x_trieuxuong',960,560,s=1.0)
    di(cv,c,'t19n_xuong',2300,885,1450,885,t,a,q+1,s=.72,bob=2,f=3,lat=True)
    for i in range(2): di(cv,c,'t19n_1duong',2600+i*180,885,1700+i*150,885,t,a+i*.3,q+1,s=.6,bob=3,f=4,ph=i,lat=True)
    if t>q: di(cv,c,'t19n_dan2',1300,890,400,890,t,q,b+1,s=.55,bob=3,f=4.4,lat=True)
    truoc(cv,c,t)
    lb(cv,C0,'nhà Đường không đem quân sang đánh',960,150,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'sai người đến thuyết phục Phùng An',960,230,t,q+.2,b,col=DUONGC,sz=40)
# ---- 20: Phùng An ra hàng
def S_20(cv,t):
    a,b=T[20]-.3,E[20]+.3;q=sb(20,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1060,540,1.1))])
    ngoai(cv,c,t,g=880,seed=21,mist=.6)
    put(cv,c,'t19x_hang',960,560,s=1.0)
    di(cv,c,'t19n_an',300,885,760,885,t,a,b,s=.7,bob=2,f=2.6)
    for i in range(2): di(cv,c,'t19n_1ta',-300-i*200,885,400+i*120,885,t,a+i*.4,b,s=.58,bob=2,f=2.8,ph=i)
    nv(cv,c,'t19n_xuong',1450,885,t,s=.72,flip=True)
    di(cv,c,'t19n_duong',2600,885,2000,885,t,a,b,s=.55,bob=2,f=3,lat=True)
    truoc(cv,c,t)
    seal(cv,'s791',1560,330,q+.3,t,s=.8,r=4)
    lb(cv,C0,'Phùng An đem quân ra hàng',960,150,t,a+.3,b,col=RED,sz=46)
# ---- 21: sử không nói vì sao (chia đôi hai việc)
def S_21(cv,t):
    a,b=T[21]-.3,E[21]+.3;q=sb(21,1)
    c=kc(t,[(a,(960,560,1.04)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=22,mist=.6)
    di(cv,c,'t19n_an',-300,885,300,885,t,a,b,s=.62,bob=2,f=2.6)
    di(cv,c,'t19n_xuong',2300,885,1650,885,t,a,b,s=.62,bob=2,f=2.8,lat=True)
    di(cv,c,'t19n_dan',-600,890,0,890,t,a+.4,b,s=.55,bob=2,f=3.2)
    truoc(cv,c,t)
    if not FREEZE:
        ink_wash(cv,.3)
        put_screen(cv,text('vì sao ra hàng? sử không nói',40,RED,700),960,200,inn(t,a+.3,.4))
        for x,tt,t0 in ((620,'người cha vừa mất',q),(1300,'nhà Đường chọn thuyết phục',q+.9)):
            if t>t0: u=inn(t,t0,.4);put_screen(cv,band(560,100,PAPER,.9,16),x,420,u);put_screen(cv,text(tt,36,INK,700),x,418,u)
# ---- 22: sử nhà Đường chỉ ghi Đỗ Anh Hàn (cuộn sử)
def S_22(cv,t):
    a,b=T[22]-.3,E[22]+.3;q=sb(22,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1060,540,1.08))])
    ngoai(cv,c,t,g=880,seed=23,mist=.5,far=.6,midv=.6)
    di(cv,c,'t19n_1duong',2300,885,1650,885,t,a,b,s=.6,bob=2,f=3,lat=True)
    di(cv,c,'t19n_han',-300,885,320,885,t,q,b,s=.6,bob=2,f=3)
    di(cv,c,'t19n_dan',-600,890,0,890,t,a,b,s=.55,bob=2,f=3.2)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3)
    cuon(cv,1060,480,t,'SỬ NHÀ ĐƯỜNG','Phùng Hưng',col=INK,s=.7,sz=52,gach=inn(t,a+.8,.6))
    if not FREEZE and t>q: put_screen(cv,wipe(text('Đỗ Anh Hàn',58,DUONGC,700),inn(t,q,.7),0,.25,seed=22),1060,620,1)
# ---- 23: sử triều Nguyễn: vì đất xa
def S_23(cv,t):
    a,b=T[23]-.3,E[23]+.3;q=sb(23,1)
    c=kc(t,[(a,(960,520,1.12)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=24,far=.5,midv=.5)
    put(cv,c,'t19x_nguyen',960,630,s=1.1)
    di(cv,c,'t19n_dan',-300,890,350,890,t,a,b,s=.55,bob=2,f=3)
    di(cv,c,'t19n_dan2',2300,890,1650,890,t,a,b,s=.55,bob=2,f=3.4,lat=True)
    flick(cv,c,960,560,t,.5)
    truoc(cv,c,t)
    lb(cv,C0,'sử triều Nguyễn: vì đất xa, nhà Đường không rõ',960,150,t,a+.3,q-.2,col=INK,sz=38)
    lb(cv,C0,'tên Phùng Hưng còn trong sử nước ta',960,150,t,q+.2,b,col=RED,sz=42)
# ---- 24: làng Đường Lâm, đền thờ; Ngô Quyền (cổng làng trở lại)
def S_24(cv,t):
    a,b=T[24]-.3,E[24]+.3;q=sb(24,1)
    c=kc(t,[(a,(800,560,1.06)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=25)
    put(cv,c,'t19x_cong',960,560,s=1.0)
    for i in range(2): di(cv,c,'t19n_dan' if i else 't19n_dan2',-400-i*250,890,350+i*150,890,t,a+i*.4,b,s=.55,bob=2,f=3.2,ph=i)
    di(cv,c,'t19n_1ta',2300,890,1700,890,t,a,b,s=.58,bob=2,f=3,lat=True)
    for i in range(2): smoke(cv,c,1730+i*20,560,t+i,.6)
    truoc(cv,c,t)
    if not FREEZE and t>q:
        u=inn(t,q,.5);put_screen(cv,band(560,110,PAPER,.9,18),1450,330,u);put_screen(cv,text('NGÔ QUYỀN',52,RED,700),1450,315,u);put_screen(cv,text('cùng làng Đường Lâm',28,INK,700),1450,360,u)
    lb(cv,C0,'đền thờ ông vẫn còn ở làng Đường Lâm',960,150,t,a+.3,q-.2,col=INK,sz=42)
# ---- 25: kết (tấm biển, cổng làng)
def S_25(cv,t):
    a=T[25]-.3;b=E[25]+4
    c=kc(t,[(a,(900,560,1.06)),(b,(1100,520,1.0))])
    ngoai(cv,c,t,g=880,seed=26,mist=.6)
    put(cv,c,'t19x_cuoi',960,560,s=1.0)
    for i in range(3): di(cv,c,'t19n_dan' if i%2 else 't19n_dan2',-300-i*220,890+i*14,600+i*180,890+i*14,t,a+i*.4,b,s=.5,bob=2,f=3.4+i*.3,ph=i)
    di(cv,c,'t19n_1ta',2300,885,1700,885,t,a,b,s=.55,bob=3,f=4,lat=True)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    bien(cv,960,330,t,'BỐ CÁI',s=.6,o=inn(t,a+.4,.6),phu='cha · mẹ')
    if not FREEZE:
        tx=text('Phùng Hưng, năm 791',54,INK,700);put_screen(cv,wipe(tx,inn(t,a+1.2,1.4),0,.3,seed=13),W/2,150)
        put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,220,inn(t,E[25]+.6,1))
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
    flock=lambda *a,**k:None
S=lambda n:T[n]-.3
SH=[(0 if n==1 else S(n),S(n+1) if n<25 else V.TOTAL+1,globals()[f'S_{n}']) for n in range(1,26)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm19_full.json'))
SENT={}
for _i,_d in enumerate(_J):
    _hs=[x for x in re.split(r'(?<=[.!?])\s+',_d['hien']) if x.strip()]
    SENT[_i+1]=_hs if len(_hs)==len(_SC[_i+1])-1 else [_d['hien']]
def caps(cv,t):
    for n,hs in SENT.items():
        for k,h in enumerate(hs):
            a=sb(n,k) if len(hs)>1 else T[n];b=sb(n,k+1) if len(hs)>1 else E[n]
            if a<t<b: caption(cv,h,inn(t,a,.12)*(1-inn(t,b-.12,.12)),False)
NOCAP=False
def ov(cv,t):
    if FREEZE: return
    TT=T[4]
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'ĐƯỜNG LÂM','stitle19',.55)
    if not NOCAP: caps(cv,t)
V.NHAN={8:'Cao Chính Bình – quan đô hộ nhà Đường',10:'Đỗ Anh Hàn – người cùng làng',19:'Triệu Xương – quan nhà Đường'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
