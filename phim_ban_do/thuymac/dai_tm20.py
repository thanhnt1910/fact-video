# Bản dài tm20: Dương Thanh, năm 819–820 (bản 1). Điểm nhấn: hai cái kết (sử nhà Đường và Toàn thư chép khác nhau).
# Hình người kiểu mới (t20n_*, nguoi18). Hình ảnh lặp lại: ngọn giáo quay đầu (chuyện quay lưng: đoạn 1, 12, 17, 23, 29)
# và hai cuộn sử (đoạn 2, 11, 26, 30, 33). Mở đầu giọt mực; bộ đếm ngày vây (15), bốn ngày (18), bảy nghìn người hàng (24).
import math,re,json,os
import numpy as np
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from engine import ragged,asc
from fx_tran import arrows,dust,sparks,fall
from tran_fx import clash
from dai_tm2 import big,lb
V=K.setup('tm20',{4:4.0})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
FREEZE=bool(os.environ.get('KIEM_TINH'))
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
    put(cv,c,'t20_far',960+seed*60,g-120,ay=1,k=.35,o=far)
    put(cv,c,'t20_mid',960-seed*40,g+30,ay=1,k=.62,o=midv)
    suong(cv,c,t,g-260,mist,seed)
def truoc(cv,c,t,o=1):
    put(cv,c,'t20_frontL',-120,1120,ax=0,ay=1,k=1.3,s=.85,r=1.2*math.sin(t*.8),o=o)
    put(cv,c,'t20_frontR',2040,1120,ax=1,ay=1,k=1.3,s=.8,r=1.2*math.sin(t*.7+1),o=o)
def di(cv,c,name,x0,y0,x1,y1,t,a,b,s=1.0,o=.97,bob=4,f=5,ph=0,k=1.0,r=0,lac=1.2,lat=False):
    if y0>700 and k==1.0: s*=GS;bob*=GS
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;y=y0+(y1-y0)*u-abs(math.sin(t*f+ph))*bob*(1 if 0<u<1 else .3)
    put(cv,c,Af(name) if lat else name,x,y,s=s,o=o,k=k,r=r+lac*math.sin(t*f*.5+ph),ay=1,scale_px=asc(name))
    return x,y
def nv(cv,c,name,x,y,t,s=.7,r=0,o=1.0,flip=False):
    put(cv,c,Af(name) if flip else name,x,y-2*math.sin(t*1.6+x),s=s*GS if y>700 else s,ay=1,o=o,r=r+.6*math.sin(t*1.1+x),scale_px=asc(name))
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
def giao(cv,x,y,t,rot=0.0,s=.5,o=1.0):
    """hình ảnh lặp lại: ngọn giáo, rot=180 là đã quay đầu"""
    put(cv,C0,'t20_giao',x,y,s=s,o=o,r=rot+1.5*math.sin(t*1.3))
def cuon(cv,x,y,t,tieu,chu,col=None,o=1.0,s=.62,sz=46,u=1.0,gach=0.0,glow=0.0):
    put(cv,C0,'t20_cuon',x,y,s=s,o=o,r=.5*math.sin(t*.7+x))
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
PT=json.load(open('/tmp/gen/bd/a/map_trung_pts.json'))
def mapbg(cv,c,u=1.0,o=1.0):
    im=A('map_trung')
    if u<1: im=wipe(im,u,0,.25,seed=4)
    put(cv,c,im,960,540,o=o,scale_px=1.5)
def mcam(t,keys):
    if FREEZE: t=keys[0][0]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z);return cam(cx,cy,z)

# ---- 1: giọt mực loang thành con đường đêm; quân đi rồi quay đầu (cảnh trọng tâm mở đầu)
def demquay(cv,t,a,b):
    q=sb(1,1)
    c=kc(t,[(a,(1300,560,1.08)),(q,(1100,560,1.0)),(b,(800,560,1.06))])
    ngoai(cv,c,t,g=880,seed=1,mist=.35,far=.6,midv=.6)
    put(cv,c,'t20x_dem',960,560,s=1.0)
    ra=q+.2
    for r in range(4):
        x0=700-r*220;y=880+r*16
        if t<ra: di(cv,c,'t20n_1ta',x0,y,x0+500,y,t,a,ra,s=.6,bob=5,f=6+r*.4,ph=r)
        else: di(cv,c,'t20n_1ta',x0+500,y,x0-300,y,t,ra+r*.15,b+1,s=.6,bob=5,f=6.4+r*.4,ph=r,lat=True)
    if t<ra: di(cv,c,'t20n_thanh',900,885,1300,885,t,a,ra,s=.74,bob=4,f=5)
    else: di(cv,c,'t20n_thanh',1300,885,700,885,t,ra,b+1,s=.74,bob=4,f=5.2,lat=True)
    duoc_lua(cv,c,[(1000,690),(1300,690),(1600,690)],t)
    truoc(cv,c,t)
    dem(cv,.32)
    return c
def S_1(cv,t):
    a,b=0,E[1]+.3;td=.95;q=sb(1,1)
    sc=PAP.copy();demquay(sc,t,a,b)
    if FREEZE: cv[:]=sc;return
    if t<td:
        y=-40+(540+40)*(t/td)**2
        m=loang(960,y,22,6);cv[:]=cv*(1-m)+np.array(INK,np.float32)*m
    else:
        u=inn(t,td,1.6);r=30+u*1300
        m=loang(960,540,r,60);rim=np.clip(loang(960,540,r,60)-loang(960,540,r-70,60),0,1)
        cv[:]=cv*(1-m)+sc*m;cv[:]=cv*(1-rim*.75)+np.array(INK,np.float32)*rim*.75
    giao(cv,1650,380,t,rot=180*inn(t,q,1.0),s=.42,o=inn(t,1.6,.5))
    big(cv,'QUAY QUÂN GIỮA ĐÊM',t,q,b,RED,180,92,seed=1)
# ---- 2: hai cái kết (hai cuộn sử, chưa có chữ)
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.08))])
    ngoai(cv,c,t,g=880,seed=2,mist=.6,far=.6,midv=.6)
    di(cv,c,'t20n_dan',-300,890,300,890,t,a,b,s=.55,bob=2,f=3)
    di(cv,c,'t20n_dan2',2300,890,1700,890,t,a,b,s=.55,bob=2,f=3.4,lat=True)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3)
    cuon(cv,620,470,t,'SỬ NHÀ ĐƯỜNG','? ? ?',col=DUONGC,s=.6,sz=58,u=inn(t,a+.6,.6))
    cuon(cv,1300,470,t,'SỬ NƯỚC TA','? ? ?',col=RED,s=.6,sz=58,u=inn(t,a+1.4,.6))
    if not FREEZE: put_screen(cv,text('hai cái kết',44,INK,700),960,170,inn(t,a+2,.5))
# ---- 3: câu hỏi: người đứng trên đồi nhìn phủ thành
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3
    c=kc(t,[(a,(700,560,1.12)),(b,(1000,560,1.0))])
    ngoai(cv,c,t,g=880,seed=3,mist=.6,far=.6,midv=.5)
    put(cv,c,'t20x_doi',960,560,s=1.0)
    for i in range(3): flick(cv,c,1640+i*60,560,t+i,.25)
    flock(cv,c,t,.5)
    di(cv,c,'t20n_1duong',2200,885,1600,885,t,a,b,s=.55,bob=3,f=4,lat=True)
    truoc(cv,c,t)
    dem(cv,.25)
    if not FREEZE:
        for k,(tt,t0) in enumerate((('ông là ai?',a+.4),('vì sao quay quân?',sb(3,0)+(E[3]-T[3])*.35),('kết thúc thế nào?',sb(3,0)+(E[3]-T[3])*.7))):
            put_screen(cv,text(tt,46,RED if k==2 else INK,700),1400,230+k*80,inn(t,t0,.4))
# ---- 4: bản đồ An Nam dưới nhà Đường (đầu thế kỷ chín)
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3;q=sb(4,1)
    c=mcam(t,[(a,(900,560,1.0)),(b,(800,420,1.25))])
    mapbg(cv,c,u=inn(t,a-.2,1.0))
    x,y=PT['daila'];pulse(cv,c,x,y,t,col=DUONGC);dot(cv,c,x,y,col=DUONGC,r=12)
    lb(cv,c,'phủ thành nhà Đường',x+60,y-40,t,q,b,col=DUONGC,sz=36)
    u=inn(t,q,b-q-.6)
    if not FREEZE: stroke(cv,c,[(x-40,y-180),(x,y-30)],u,wid=8,col=DUONGC,o=.8)
    flock(cv,c,t,.4,y0=700)
    lb(cv,C0,'đầu thế kỷ thứ chín',960,150,t,a+.3,q-.2,col=INK,sz=46)
    lb(cv,C0,'đất An Nam, nhà Đường cai trị',960,150,t,q+.2,b,col=DUONGC,sz=44)
# ---- 5: Lý Tượng Cổ thu thuế, dân nộp
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3;q=sb(5,1)
    c=kc(t,[(a,(960,520,1.15)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=5,far=.5,midv=.5)
    put(cv,c,'t20x_phu',960,630,s=1.1)
    for i in range(3): di(cv,c,'t20n_dan' if i%2 else 't20n_dan2',-500-i*200,890,250+i*130,890,t,a+i*.4,b,s=.55,bob=3,f=3+i*.2,ph=i)
    di(cv,c,'t20n_1duong',2300,885,1500,885,t,q,b,s=.6,bob=2,f=3.2,lat=True)
    for i in range(2): flick(cv,c,700+i*520,600,t+i,.3)
    truoc(cv,c,t)
    lb(cv,C0,'người trong họ nhà vua Đường',960,230,t,a+.3,q-.2,col=DUONGC,sz=40)
    lb(cv,C0,'tham lam, tàn bạo, cai trị hà khắc',960,150,t,q+.2,b,col=RED,sz=44)
# ---- 6: Hoan Châu, Dương Thanh
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3;q=sb(6,1)
    c=kc(t,[(a,(1300,560,1.06)),(b,(900,560,1.0))])
    ngoai(cv,c,t,g=880,seed=6)
    put(cv,c,'t20x_hoan',960,560,s=1.0)
    for i in range(2):
        put(cv,c,'t12_spr_khoi',1640+i*240,520-((t*30+i*100)%200),s=.5,o=.3)
    nv(cv,c,'t20n_thanh',1000,885,t,s=.76)
    di(cv,c,'t20n_dan',-400,890,500,890,t,a,b+1,s=.55,bob=2,f=3.2)
    di(cv,c,'t20n_1ta',2300,890,1500,890,t,a+.3,b+1,s=.58,bob=3,f=4,lat=True)
    truoc(cv,c,t)
    lb(cv,C0,'dòng họ nhiều đời làm tù trưởng',960,170,t,a+.3,q-.2,col=INK,sz=44)
    lb(cv,C0,'thứ sử Hoan Châu: Nghệ An, Hà Tĩnh ngày nay',960,170,t,q+.2,b,col=RED,sz=40)
# ---- 7: bản đồ: gọi từ Hoan Châu về phủ thành
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3;q=sb(7,1)
    c=mcam(t,[(a,(760,560,1.25)),(b,(760,420,1.25))])
    mapbg(cv,c)
    xh,yh=PT['hoanchau'];xd,yd=PT['daila']
    pulse(cv,c,xh,yh,t);dot(cv,c,xh,yh,col=RED,r=12);dot(cv,c,xd,yd,col=DUONGC,r=12)
    lb(cv,c,'Hoan Châu',xh+110,yh,t,a+.2,b,col=RED,sz=38)
    lb(cv,c,'phủ thành',xd+100,yd,t,a+.2,b,col=DUONGC,sz=38)
    u=inn(t,q,b-q-.4)
    if not FREEZE:
        pts=[(xh,yh-20),(xh+30,(yh+yd)/2),(xd,yd+24)];stroke(cv,c,pts,u,wid=7,col=RED,o=.85,dash=1)
        if u>0:
            k=min(int(u*2),1);px=pts[k][0]+(pts[k+1][0]-pts[k][0])*(u*2-k);py=pts[k][1]+(pts[k+1][1]-pts[k][1])*(u*2-k)
            put(cv,c,'t20n_thanh',px,py+10,s=.32,ay=1,scale_px=3,r=2*math.sin(t*6))
    lb(cv,C0,'sử nhà Đường: Lý Tượng Cổ ghét thế lực của ông',960,150,t,a+.3,q-.2,col=DUONGC,sz=38)
    lb(cv,C0,'gọi về làm nha tướng, ở ngay trong phủ',960,150,t,q+.2,b,col=INK,sz=42)
# ---- 8: trong phủ, đứng dưới trướng người dè chừng mình
def S_8(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1);q2=sb(8,2)
    c=kc(t,[(a,(960,560,1.0)),(q,(1200,560,1.1)),(b,(1300,540,1.18))])
    ngoai(cv,c,t,g=880,seed=8,far=.4,midv=.4,mist=.4)
    put(cv,c,'t20x_trong',960,560,s=1.1)
    for i in range(2): di(cv,c,'t20n_1duong',300+i*1200,885,600+i*1200,885,t,a+i*.5,b,s=.55,bob=2,f=2.6,ph=i,lat=bool(i))
    flick(cv,c,700,600,t,.35);flick(cv,c,1200,600,t+1,.35)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.18)
    if not FREEZE and t>q:
        u=inn(t,q,.6);put_screen(cv,band(520,140,PAPER,.88,18),560,330,u)
        put_screen(cv,text('thứ sử một châu',34,INK,700),560,300,u);stroke(cv,C0,[(430,300),(690,296)],inn(t,q+.6,.5),wid=6,col=RED,o=.85,head=False)
        put_screen(cv,text('→ tướng dưới quyền',38,RED,700),560,355,inn(t,q+.9,.4))
    lb(cv,C0,'sử nhà Đường chép: uất ức, không vui',960,150,t,q2+.1,b,col=INK,sz=40)
# ---- 9: Hoàng Động nổi lên ở phía bắc
def S_9(cv,t):
    a,b=T[9]-.3,E[9]+.3;q=sb(9,1)
    c=kc(t,[(a,(1300,560,1.05)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=9,mist=.6)
    put(cv,c,'t20x_hoangdong',960,560,s=1.0)
    for x in (500,1200,1900): smoke(cv,c,x,520,t+x,1.0)
    for i in range(3): di(cv,c,'t20n_man',-500-i*220,890,300+i*180,890,t,a+i*.3,b+1,s=.56,bob=4,f=5.4+i*.3,ph=i)
    di(cv,c,'t20n_man5',2400,880,1500,880,t,q,b+1,s=.75,bob=3,f=4.8,lat=True)
    truoc(cv,c,t)
    lb(cv,C0,'phía bắc: người Man ở Hoàng Động nổi lên',960,150,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'các động họ Hoàng, nhiều năm chống nhà Đường',960,150,t,q+.2,b,col=INK,sz=38)
# ---- 10: hai viên quan xin đánh; chiếu vua Đường
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3;q=sb(10,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,520,1.12))])
    ngoai(cv,c,t,g=880,seed=10,far=.5,midv=.5)
    put(cv,c,'t20x_chieu',960,560,s=1.08)
    di(cv,c,'t20n_su',2300,885,1300,885,t,q,b,s=.62,bob=3,f=4,lat=True)
    for i in range(2): nv(cv,c,'t20n_uoc',700+i*160,885,t,s=.6,r=-6*inn(t,a+.5+i*.3,.6))
    truoc(cv,c,t)
    if not FREEZE and t>q:
        u=inn(t,q+.3,.8);put(cv,C0,'t19_cuon',1500,420,s=.32*u+.01,o=u)
        put_screen(cv,text('CHIẾU',40,RED,700),1500,420,u)
    lb(cv,C0,'hai viên quan vùng Quảng Tây muốn lập công',960,150,t,a+.3,q-.2,col=DUONGC,sz=40)
    lb(cv,C0,'vua Đường xuống chiếu: Lý Tượng Cổ cũng phải đem quân',960,150,t,q+.2,b,col=INK,sz=36)
# ---- 11: giao quân cho Dương Thanh; hai sách ghi số quân khác nhau
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3;q=sb(11,1)
    c=kc(t,[(a,(1300,560,1.12)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=11)
    put(cv,c,'t20x_giao',960,560,s=1.0)
    for r in range(3): di(cv,c,'t20n_ta',-900-r*260,880+r*24,-100-r*200,880+r*24,t,a+r*.3,b+1,s=.55,bob=4,f=5.6+r*.3,ph=r)
    for i in range(2): put(cv,c,'t12_spr_khoi',1880+i*80,420-((t*30+i*120)%200),s=.35,o=.25)
    truoc(cv,c,t)
    if not FREEZE and t>q:
        cuon(cv,620,470,t,'CỰU ĐƯỜNG THƯ','2.000|quân',col=INK,s=.44,sz=52,u=inn(t,q+.2,.6))
        cuon(cv,1300,470,t,'TƯ TRỊ THÔNG GIÁM','3.000|quân',col=INK,s=.44,sz=52,u=inn(t,q+1.0,.6))
    lb(cv,C0,'Lý Tượng Cổ giao việc ấy cho Dương Thanh',960,150,t,a+.3,q-.2,col=INK,sz=42)
# ---- 12: cận cảnh lệnh bài, ngọn giáo đổi tay
def S_12(cv,t):
    a,b=T[12]-.3,E[12]+.3
    c=kc(t,[(a,(960,560,1.0)),(b,(980,540,1.12))])
    put(cv,c,'t20_far',960,760,ay=1,k=.35,o=.4)
    put(cv,c,'t20x_lenh',960,600,s=1.0)
    for i in range(2): flick(cv,c,300+i*1300,420,t+i,.4)
    suong(cv,c,t,560,.35,12)
    if not FREEZE:
        ink_wash(cv,.12)
        u=inn(t,a+.5,1.6);giao(cv,600+700*u,430,t,rot=-35+35*u,s=.38)
        put_screen(cv,text('người bị dè chừng',36,DUONGC,700),560,230,inn(t,a+.3,.4))
        put_screen(cv,text('được trao cả một đạo quân',40,RED,700),1360,230,inn(t,a+1.6,.4))
# ---- 13: ba người bàn kín bên đống lửa
def S_13(cv,t):
    a,b=T[13]-.3,E[13]+.3;q=sb(13,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(940,540,1.16))])
    ngoai(cv,c,t,g=880,seed=13,far=.5,midv=.5,mist=.4)
    put(cv,c,'t20x_ban',960,560,s=1.1)
    flick(cv,c,960,880,t,.7);smoke(cv,c,960,700,t,.6)
    di(cv,c,'t20n_1ta',2300,890,1700,890,t,a,b,s=.58,bob=3,f=4,lat=True)
    di(cv,c,'t20n_1ta',-300,890,250,890,t,a+.4,b,s=.58,bob=3,f=4.2)
    truoc(cv,c,t)
    dem(cv,.3)
    if not FREEZE:
        for k,(nm,x,t0) in enumerate((('Dương Thanh',560,a+.3),('Dương Chí Liệt · con trai',1180,a+1.2),('Đỗ Sĩ Giao · người thân tín',1180,a+2.0))):
            put_screen(cv,band(440,64,PAPER,.88,14),x,250+(k>0)*(k-1)*70,inn(t,t0,.4));put_screen(cv,text(nm,32,RED if k==0 else INK,700),x,248+(k>0)*(k-1)*70,inn(t,t0,.4))
    lb(cv,C0,'không đi đánh Hoàng Động nữa',960,150,t,q+.2,b,col=RED,sz=42)
# ---- 14: quay về giữa đêm, đánh úp phủ thành (cảnh trọng tâm)
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3;q=sb(14,1)
    if t<a+1.0 and not FREEZE:
        A_=PAP.copy();S_13(A_,t);B_=PAP.copy();demhanh(B_,t,a,b)
        m=quet(inn(t,a-.1,1.0));cv[:]=A_*(1-m)+B_*m
    else: demhanh(cv,t,a,b)
    lb(cv,C0,'quay về giữa đêm, đánh úp phủ thành',960,150,t,q+.1,b,col=RED,sz=44)
def demhanh(cv,t,a,b):
    c=kc(t,[(a,(1400,560,1.05)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=14,mist=.3,far=.5,midv=.5)
    put(cv,c,'t20x_demhanh',960,560,s=1.0)
    for r in range(3): di(cv,c,'t20n_ta',2400+r*260,880+r*20,700+r*200,880+r*20,t,a+r*.25,b+.5,s=.58,bob=5,f=6.4+r*.3,ph=r,lat=True)
    di(cv,c,'t20n_thanh2',2000,885,500,885,t,a,b,s=.74,bob=5,f=6,lat=True)
    duoc_lua(cv,c,[(900,690),(1200,690),(1500,690),(1800,690)],t)
    if not FREEZE:
        u=inn(t,a+.4,b-a-.6);stroke(cv,c,[(1900,760),(1200,740),(500,700)],u,wid=9,col=RED,o=.8)
    truoc(cv,c,t)
    dem(cv,.36)
# ---- 15: mấy ngày sau thành mới vỡ (bộ đếm ngày), tháng mười năm 819
def S_15(cv,t):
    a,b=T[15]-.3,E[15]+.3;q=sb(15,1);q2=sb(15,2)
    c=kc(t,[(a,(960,520,1.12)),(b,(960,560,1.0))],3*math.sin(t*30)*(q<t<q2) if not FREEZE else 0)
    ngoai(cv,c,t,g=900,seed=15)
    put(cv,c,'t20x_vay',960,560,s=1.0)
    clash(cv,c,t,a+.2,b,'ta','duong',xm=1000,y=880,s=.62,push=1,seed=15,pre='t20n_')
    for k in range(4): flick(cv,c,600+k*300,560,t+k,.35 if t>q else .0001)
    truoc(cv,c,t)
    if not FREEZE:
        n=min(4,int((t-a)/((q-a)/4+.01))+1) if t<q+.4 else 4
        o_dem(cv,1500,300,n,4,'ngày vây',t,inn(t,a+.3,.4))
    seal(cv,'s819',400,300,q2+.2,t,s=.8,r=-4)
    lb(cv,C0,'thành không mất ngay trong đêm ấy',960,150,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'mùa đông, tháng mười năm 819',960,150,t,q2+.1,b,col=RED,sz=44)
# ---- 16: Lý Tượng Cổ bị giết; sảnh phủ đổ (nhãn tên rơi, mực đỏ loang)
def S_16(cv,t):
    a,b=T[16]-.3,E[16]+.3;q=sb(16,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,540,1.1))])
    ngoai(cv,c,t,g=880,seed=16,far=.5,midv=.5,mist=.7)
    put(cv,c,'t20x_sanh',960,560,s=1.08)
    for i in range(3): smoke(cv,c,500+i*450,500,t+i,1.0)
    for i in range(2): di(cv,c,'t20n_1ta',-300-i*200,890,350+i*150,890,t,a+i*.3,b,s=.58,bob=3,f=4,ph=i)
    truoc(cv,c,t)
    if not FREEZE:
        ink_wash(cv,.22)
        u=inn(t,a+.6,1.2);put_screen(cv,text('LÝ TƯỢNG CỔ',58,DUONGC,700),960+30*u,300+380*u**2,1-.7*inn(t,a+1.6,.6),r=20*u)
        if t>a+1.2: put_screen(cv,band(int(500*inn(t,a+1.2,1.5)),int(260*inn(t,a+1.2,1.5)),RED,.35,60),960,650,1)
        if t>q: put_screen(cv,band(500,90,PAPER,.88,16),1500,300,inn(t,q,.4));put_screen(cv,text('hơn 1.000 người',44,RED,700),1500,298,inn(t,q,.4));put_screen(cv,text('theo sử nhà Đường',26,INK,700),1500,345,inn(t,q,.4))
# ---- 17: ngọn giáo quay đầu: đạo quân được giao quay về đánh người giao
def S_17(cv,t):
    a,b=T[17]-.3,E[17]+.3;q=sb(17,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,520,1.12))])
    ngoai(cv,c,t,g=880,seed=17)
    put(cv,c,'t20x_cotdo',960,560,s=1.0)
    for x in (840,1560): put(cv,c,'t12_spr_khoi',x,400-((t*30)%160),s=.4,o=.25)
    for i in range(3): di(cv,c,'t20n_ta',-900-i*200,885+i*20,-100+i*240,885+i*20,t,a+i*.4,b,s=.52,bob=3,f=4.6,ph=i)
    truoc(cv,c,t)
    if not FREEZE:
        giao(cv,1600,430,t,rot=180*inn(t,q,1.2),s=.5)
        put_screen(cv,text('đạo quân Lý Tượng Cổ giao',36,DUONGC,700),560,250,inn(t,a+.3,.4))
    lb(cv,C0,'quay lưng với chính người giữ mình',960,180,t,q+.2,b,col=RED,sz=44)
# ---- 18: tin về triều Đường; bốn ngày
def S_18(cv,t):
    a,b=T[18]-.3,E[18]+.3;q=sb(18,1)
    c=kc(t,[(a,(700,560,1.05)),(b,(1300,520,1.05))])
    ngoai(cv,c,t,g=880,seed=18,mist=.5)
    put(cv,c,'t20x_tin',960,560,s=1.0)
    u=inn(t,a,b-a);put(cv,c,'t20n_ngua',300+1500*u,860-260*u,s=.62,ay=1,scale_px=3,r=-6+2*math.sin(t*14))
    for k in range(3): dust(cv,c,300+1500*u-100-k*60,860-260*u+10,o=.3,s=.3)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    if not FREEZE and t>q:
        n=min(4,int((t-q)/max((b-q-.6)/4,.3))+1);o_dem(cv,1450,300,n,4,'bốn ngày',t,inn(t,q,.4))
    lb(cv,C0,'tin về tới triều Đường',960,150,t,a+.3,q-.2,col=DUONGC,sz=44)
# ---- 19: triều Đường quyết định: cử Quế Trọng Vũ, tha tội, phong thứ sử Quỳnh Châu
def S_19(cv,t):
    a,b=T[19]-.3,E[19]+.3;q=sb(19,1)
    c=kc(t,[(a,(960,500,1.1)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=19,far=.4,midv=.4)
    put(cv,c,'t20x_trieu',960,560,s=1.0)
    di(cv,c,'t20n_vu',300,885,820,885,t,q,b,s=.72,bob=2,f=2.8)
    for i in range(2): nv(cv,c,'t20n_su',1350+i*140,885,t,s=.6,flip=True,r=-5*inn(t,a+.4+i*.3,.6))
    flick(cv,c,960,600,t,.3)
    truoc(cv,c,t)
    if not FREEZE and t>q:
        for k,(tt,t0) in enumerate((('tha tội',q+.8),('phong thứ sử Quỳnh Châu',q+1.8))):
            u=inn(t,t0,.4);put_screen(cv,band(460,70,PAPER,.9,14),1500,280+k*84,u);put_screen(cv,text(tt,34,RED,700),1500,278+k*84,u)
    lb(cv,C0,'nhà Đường không sai quân sang đánh ngay',960,150,t,a+.3,q-.2,col=INK,sz=42)
# ---- 20: bản đồ: Quỳnh Châu (đảo Hải Nam) cách Hoan Châu một vùng biển
def S_20(cv,t):
    a,b=T[20]-.3,E[20]+.3;q=sb(20,1);q2=sb(20,2)
    c=mcam(t,[(a,(1100,500,1.0)),(b,(1100,470,1.12))])
    mapbg(cv,c)
    xq,yq=PT['quynhchau'];xh,yh=PT['hoanchau']
    pulse(cv,c,xq,yq,t);dot(cv,c,xq,yq,col=RED,r=12);dot(cv,c,xh,yh,col=RED,r=12)
    lb(cv,c,'Quỳnh Châu',xq,yq-60,t,a+.3,b,col=RED,sz=40);lb(cv,c,'đảo Hải Nam ngày nay',xq,yq+60,t,a+.8,b,col=INK,sz=30)
    lb(cv,c,'Hoan Châu',xh+120,yh,t,a+.3,b,col=RED,sz=38)
    if not FREEZE:
        u=inn(t,q,1.6);stroke(cv,c,[(xh+20,yh-10),((xh+xq)/2,(yh+yq)/2-80),(xq-30,yq+10)],u,wid=6,col=INK,o=.7,dash=1)
        for k in range(5):
            wx=(xh+xq)/2-200+k*100+20*math.sin(t*1.5+k);wy=(yh+yq)/2+60+8*math.sin(t*2+k)
            stroke(cv,c,[(wx-30,wy),(wx,wy-10),(wx+30,wy)],1,wid=3,col=INK,o=.4,head=False)
    lb(cv,C0,'sử không chép nhà Đường tính toán gì',960,150,t,q+.2,q2,col=INK,sz=40)
    lb(cv,C0,'được tha, nhưng phải rời xa đất của mình',960,150,t,q2+.1,b,col=RED,sz=42)
# ---- 21: không nhận; chặn ở biên giới, năm 820
def S_21(cv,t):
    a,b=T[21]-.3,E[21]+.3;q=sb(21,1);q2=sb(21,2)
    c=kc(t,[(a,(960,560,1.0)),(b,(1060,520,1.12))])
    ngoai(cv,c,t,g=880,seed=21,mist=.5)
    put(cv,c,'t20x_ai',960,560,s=1.0)
    di(cv,c,'t20n_vu',2300,885,1500,885,t,q,q2+.5,s=.66,bob=3,f=3.6,lat=True)
    for i in range(3): di(cv,c,'t20n_1duong',2600+i*160,885,1700+i*160,885,t,q+.2*i,q2+.5,s=.58,bob=3,f=4.2,ph=i,lat=True)
    for i in range(2): di(cv,c,'t20n_1ta',-300-i*200,885,600+i*120,885,t,a+i*.3,q,s=.6,bob=3,f=4,ph=i)
    truoc(cv,c,t)
    if not FREEZE:
        put_screen(cv,text('không nhận',50,RED,700),960,190,inn(t,a+.3,.4)*(1-inn(t,q-.2,.3)))
        if t>q2: u=inn(t,q2,.5);stroke(cv,C0,[(1250,700),(1250,860)],u,wid=12,col=RED,o=.9,head=False);put_screen(cv,text('không cho vào',44,RED,700),1250,620,u)
    seal(cv,'s820',400,300,q+.2,t,s=.8,r=-4)
# ---- 22: Quế Trọng Vũ sai người thuyết phục từng tù trưởng
def S_22(cv,t):
    a,b=T[22]-.3,E[22]+.3
    c=kc(t,[(a,(1300,560,1.08)),(b,(950,560,1.0))])
    ngoai(cv,c,t,g=880,seed=22)
    put(cv,c,'t20x_du',960,560,s=1.0)
    di(cv,c,'t20n_su',2300,885,1500,885,t,a,a+2.5,s=.62,bob=3,f=4,lat=True)
    di(cv,c,'t20n_tt',-300,885,500,885,t,a+.6,b,s=.62,bob=2,f=3)
    for i in range(2): smoke(cv,c,600+i*1300,520,t+i,.7)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    if not FREEZE:
        n=int(6*inn(t,a+1,b-a-1.4));put_screen(cv,band(420,150,PAPER,.88,18),1500,300,inn(t,a+.8,.4))
        dot_dem(cv,1360,320,n,6,cot=6,gap=56,col=DUONGC,r=17);put_screen(cv,text('từng tù trưởng',34,INK,700),1500,260,inn(t,a+.8,.4))
    lb(cv,C0,'không đánh thẳng, mà sai người đi thuyết phục',960,150,t,a+.3,b,col=DUONGC,sz=40)
# ---- 23: hình phạt tàn khốc; người dưới quyền quay lưng (lời phía đối địch)
def S_23(cv,t):
    a,b=T[23]-.3,E[23]+.3;q=sb(23,1)
    c=kc(t,[(a,(900,560,1.1)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=23,far=.5,midv=.5,mist=.6)
    put(cv,c,'t20x_trai',960,560,s=1.0)
    for i in range(4): di(cv,c,'t20n_1ta' if i%2 else 't20n_dan',800+i*120,890+i*6,2500+i*150,890+i*6,t,a+.8+i*.6,b+2,s=.55,bob=3,f=3.6+i*.3,ph=i)
    flick(cv,c,600,880,t,.5)
    truoc(cv,c,t)
    if not FREEZE:
        ink_wash(cv,.2)
        giao(cv,1650,420,t,rot=180*inn(t,a+1.0,1.2),s=.4,o=.9)
        put_screen(cv,band(540,80,PAPER,.9,14),560,250,inn(t,a+.2,.4));put_screen(cv,text('lời của sử nhà Đường',36,DUONGC,700),560,248,inn(t,a+.2,.4))
    lb(cv,C0,'dần quay lưng với ông',960,180,t,a+1.4,q,col=RED,sz=44)
    lb(cv,C0,'cần nhớ: đây là lời của phía đối địch',960,180,t,q+.1,b,col=INK,sz=40)
# ---- 24: hơn bảy nghìn quân ra hàng
def S_24(cv,t):
    a,b=T[24]-.3,E[24]+.3
    c=kc(t,[(a,(700,560,1.08)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=24,mist=.5)
    put(cv,c,'t20x_hang',960,560,s=1.0)
    for i in range(4): di(cv,c,'t20n_dan' if i%2 else 't20n_1ta',-600-i*240,890+(i%2)*10,600+i*160,890+(i%2)*10,t,a+i*.35,b+1,s=.55,bob=3,f=3.6+i*.25,ph=i)
    for x in (1700,2050): put(cv,c,'t12_spr_khoi',x,480-((t*30+x)%180),s=.35,o=.25)
    truoc(cv,c,t)
    if not FREEZE:
        n=int(7000*inn(t,a+.6,b-a-1.2));put_screen(cv,band(480,110,PAPER,.88,16),1450,280,inn(t,a+.4,.4))
        put_screen(cv,text(f'{n:,}'.replace(',','.')+' quân' if n<7000 else 'hơn 7.000 quân',48,DUONGC,700),1450,278,inn(t,a+.4,.4))
    lb(cv,C0,'người ra hàng Quế Trọng Vũ cứ nối nhau',960,150,t,a+.3,b,col=INK,sz=42)
# ---- 25: bị chê chậm; người được cử thay chết trên đường
def S_25(cv,t):
    a,b=T[25]-.3,E[25]+.3;q=sb(25,1)
    c=kc(t,[(a,(960,520,1.0)),(b,(1100,520,1.1))])
    ngoai(cv,c,t,g=880,seed=25,far=.4,midv=.0,mist=.6)
    put(cv,c,'t20x_bien',960,560,s=1.0,r=1.2*math.sin(t*.9))
    for k in range(6):
        x=((t*60+k*330)%2200)-100;stroke(cv,c,[(x-40,820+k*8),(x,810+k*8),(x+40,820+k*8)],1,wid=3,col=INK,o=.35,head=False)
    flock(cv,c,t,.5)
    if not FREEZE:
        put_screen(cv,band(520,150,PAPER,.88,18),560,300,inn(t,a+.3,.4))
        put_screen(cv,text('Quế Trọng Vũ',40,DUONGC,700),560,270,inn(t,a+.3,.4));stroke(cv,C0,[(430,262),(690,280)],inn(t,a+1.2,.5),wid=6,col=RED,o=.85,head=False)
        put_screen(cv,text('bị giáng chức',32,RED,700),560,335,inn(t,a+1.4,.4))
        if t>q: u=inn(t,q+.4,1.0);put_screen(cv,text('người thay',38,DUONGC,700),1450,250+330*u**2,1-.7*inn(t,q+1.2,.6),r=25*u)
    lb(cv,C0,'chưa tới nơi đã chết trên đường',960,150,t,q+.2,b,col=INK,sz=42)
# ---- 26: hãy nhớ: hai cuộn sử rẽ hai ngả
def S_26(cv,t):
    a,b=T[26]-.3,E[26]+.3;q=sb(26,1)
    c=kc(t,[(a,(960,560,1.06)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=26,mist=.7,far=.5,midv=.5)
    di(cv,c,'t20n_dan',-300,890,260,890,t,a,b,s=.55,bob=2,f=3)
    di(cv,c,'t20n_1ta',2300,890,1700,890,t,a,b,s=.55,bob=2,f=3.4,lat=True)
    flock(cv,c,t,.4)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.32)
    u=inn(t,q,1.4)
    cuon(cv,960-360*u,470,t,'SỬ NHÀ ĐƯỜNG','',s=.6)
    cuon(cv,960+360*u,470,t,'TOÀN THƯ','',s=.6)
    if not FREEZE:
        put_screen(cv,text('HÃY NHỚ',60,RED,700),960,170,inn(t,a+.2,.4))
        if u>.3: stroke(cv,C0,[(960,780),(960-300*u,860)],u,wid=6,col=DUONGC,o=.8);stroke(cv,C0,[(960,780),(960+300*u,860)],u,wid=6,col=RED,o=.8)
# ---- 27: theo sử nhà Đường: tướng sĩ mở cửa thành, Dương Thanh bị bắt (cảnh trọng tâm)
def S_27(cv,t):
    a,b=T[27]-.3,E[27]+.3;q=sb(27,1)
    c=kc(t,[(a,(1100,500,1.15)),(q,(1100,540,1.05)),(b,(1000,560,1.0))])
    ngoai(cv,c,t,g=880,seed=27,far=.5,midv=.5)
    put(cv,c,'t20x_mocua',960,520,s=.95)
    for r in range(3): di(cv,c,'t20n_duong',2600+r*240,885+r*22,1250+r*200,885+r*22,t,a+.4+r*.3,q+1.4,s=.58,bob=4,f=5.6+r*.3,ph=r,lat=True)
    if t<q+.5: nv(cv,c,'t20n_thanh',700,885,t,s=.74)
    else: put(cv,c,'t20n_thanh',700,885,s=.74*GS,ay=1,r=-20*inn(t,q+.5,.8),o=1-.5*inn(t,q+.9,.8),scale_px=3)
    di(cv,c,'t20n_1duong',1100,885,820,885,t,q,q+1,s=.6,bob=4,f=6,lat=True)
    truoc(cv,c,t)
    if not FREEZE:
        put_screen(cv,band(420,70,PAPER,.88,14),360,250,inn(t,a+.2,.4));put_screen(cv,text('theo sử nhà Đường',32,DUONGC,700),360,248,inn(t,a+.2,.4))
        if t>q+.6: u=inn(t,q+.6,.6);put_screen(cv,text('DƯƠNG THANH',54,INK,700),1420,320,1);stroke(cv,C0,[(1250,330),(1590,305)],u,wid=9,col=RED,o=.9,head=False)
    seal(cv,'s820',1660,180,a+.4,t,s=.7,r=4)
    lb(cv,C0,'chính tướng sĩ trong thành mở cửa',960,150,t,a+.3,q-.2,col=INK,sz=42)
# ---- 28: Chí Trinh bị giết; Chí Liệt, Đỗ Sĩ Giao rút về Tạc Khê rồi ra hàng
def S_28(cv,t):
    a,b=T[28]-.3,E[28]+.3;q=sb(28,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,520,1.12))])
    ngoai(cv,c,t,g=880,seed=28,mist=.6)
    put(cv,c,'t20x_khe',960,560,s=1.0)
    for i in range(2): di(cv,c,'t20n_1ta',-300-i*200,890,700+i*140,890,t,q+i*.3,q+3,s=.56,bob=4,f=5+i*.3,ph=i)
    di(cv,c,'t20n_liet',-200,885,860,885,t,q,q+3,s=.62,bob=4,f=5)
    di(cv,c,'t20n_giao',-500,885,700,885,t,q+.2,q+3.2,s=.6,bob=4,f=5.2)
    smoke(cv,c,1200,500,t,.8)
    truoc(cv,c,t)
    if not FREEZE:
        u=inn(t,a+.3,.6);put_screen(cv,text('Dương Chí Trinh',44,INK,700),560,260,1-.7*inn(t,a+1.4,.6));stroke(cv,C0,[(400,270),(720,250)],inn(t,a+.9,.5),wid=7,col=RED,o=.85,head=False)
        if t>q: put_screen(cv,band(400,70,PAPER,.88,14),1500,250,inn(t,q,.4));put_screen(cv,text('Tạc Khê, Trường Châu',32,RED,700),1500,248,inn(t,q,.4))
        if t>E[28]-2.2: put_screen(cv,text('rồi ra hàng',42,DUONGC,700),1500,330,inn(t,E[28]-2.2,.4))
# ---- 29: vòng tròn: hai lần quay lưng
def S_29(cv,t):
    a,b=T[29]-.3,E[29]+.3;q=sb(29,1);q2=sb(29,2)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.06))])
    ngoai(cv,c,t,g=880,seed=29,mist=.6,far=.6,midv=.6)
    di(cv,c,'t20n_1ta',-300,890,300,890,t,a,b,s=.55,bob=2,f=3)
    di(cv,c,'t20n_1duong',2300,890,1700,890,t,a,b,s=.55,bob=2,f=3.4,lat=True)
    truoc(cv,c,t)
    if not FREEZE:
        ink_wash(cv,.3)
        u=inn(t,a+.3,b-a-1);n=48;pts=[(960+300*math.cos(-math.pi/2+2*math.pi*k/n),470+240*math.sin(-math.pi/2+2*math.pi*k/n)) for k in range(n+1)]
        stroke(cv,C0,pts,u,wid=10,col=INK,o=.8,head=False)
        giao(cv,960,240,t,rot=180*inn(t,q,1.0),s=.32)
        giao(cv,960,700,t,rot=180*inn(t,q2,1.0),s=.32)
        put_screen(cv,text('819: quay lưng với người trao quân',34,RED,700),1500,300,inn(t,q,.4))
        put_screen(cv,text('820: người trong thành quay lưng với ông',34,DUONGC,700),1460,660,inn(t,q2,.4))
        put_screen(cv,text('nếu theo sử nhà Đường',34,INK,700),420,470,inn(t,a+.3,.4))
# ---- 30: Toàn thư chép khác: nhà Đường đánh không thắng
def S_30(cv,t):
    a,b=T[30]-.3,E[30]+.3;q=sb(30,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1100,560,1.06))])
    ngoai(cv,c,t,g=880,seed=30)
    put(cv,c,'t20x_toanthu',960,560,s=1.0)
    clash(cv,c,t,q,b,'ta','duong',xm=1100,y=880,s=.6,push=1,seed=30,pre='t20n_')
    truoc(cv,c,t)
    if not FREEZE and t<q+.3:
        ink_wash(cv,.3*(1-inn(t,q-.3,.5)))
        cuon(cv,960,470,t,'TOÀN THƯ','chép khác',col=RED,s=.62,sz=52,u=inn(t,a+.4,.6),glow=1,o=1-inn(t,q-.3,.5))
    lb(cv,C0,'Toàn thư: nhà Đường sai quân sang đánh mà không thắng',960,150,t,q+.2,b,col=RED,sz=36)
# ---- 31: vào sống giữa người Man Lạo, tiếp tục đánh phá phủ thành
def S_31(cv,t):
    a,b=T[31]-.3,E[31]+.3;q=sb(31,1)
    c=kc(t,[(a,(1300,560,1.06)),(b,(900,560,1.0))])
    ngoai(cv,c,t,g=880,seed=31,mist=.7)
    put(cv,c,'t20x_manlao',960,560,s=1.0)
    for x in (700,1400): smoke(cv,c,x,480,t+x,.8)
    for i in range(3): di(cv,c,'t20n_man',2300+i*200,890,1500+i*150,890,t,a+i*.3,b,s=.55,bob=3,f=4+i*.3,ph=i,lat=True)
    di(cv,c,'t20n_1ta',-300,890,450,890,t,a,b,s=.56,bob=3,f=4)
    truoc(cv,c,t)
    if not FREEZE and t>q:
        u=inn(t,q,.5);put_screen(cv,band(520,110,PAPER,.88,16),1450,300,u)
        put_screen(cv,text('Lý Nguyên Gia',38,DUONGC,700),1450,282,u);put_screen(cv,text('đánh không được, dụ không xong',28,INK,700),1450,325,u)
    lb(cv,C0,'theo Toàn thư: vào sống giữa người Man Lạo',960,150,t,a+.3,q-.2,col=RED,sz=40)
# ---- 32: năm 828, Hàn Ước bị đuổi chạy về Quảng Châu
def S_32(cv,t):
    a,b=T[32]-.3,E[32]+.3
    c=kc(t,[(a,(1300,560,1.05)),(b,(700,560,1.05))])
    ngoai(cv,c,t,g=880,seed=32,mist=.5)
    put(cv,c,'t20x_duoi',960,560,s=1.0)
    u=inn(t,a+.3,b-a);put(cv,c,Af('t20n_ngua'),1700-1400*u,880,s=.62,ay=1,scale_px=3,r=4*math.sin(t*14))
    for k in range(3): dust(cv,c,1700-1400*u+120+k*60,880,o=.3,s=.3)
    di(cv,c,'t20n_uoc',1900,885,600,885,t,a+.5,b,s=.62,bob=5,f=7,lat=True)
    for i in range(3): di(cv,c,'t20n_1ta',2500+i*180,885,1200+i*160,885,t,a+.9+i*.2,b+.5,s=.58,bob=5,f=6.6+i*.3,ph=i,lat=True)
    truoc(cv,c,t)
    seal(cv,'s828',1600,280,a+.6,t,s=.8,r=4)
    lb(cv,C0,'chín năm sau, năm 828',960,150,t,a+.3,b,col=RED,sz=44)
    lb(cv,C0,'Hàn Ước bị đuổi chạy về Quảng Châu',960,230,t,a+1.0,b,col=DUONGC,sz=38)
# ---- 33: hai cái kết đặt cạnh nhau
def S_33(cv,t):
    a,b=T[33]-.3,E[33]+.3;q=sb(33,1);q2=sb(33,2)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.06))])
    ngoai(cv,c,t,g=880,seed=33,mist=.6,far=.5,midv=.5)
    put(cv,c,'t20_far',960,980,ay=1,k=.5,o=.3)
    di(cv,c,'t20n_dan2',-300,890,300,890,t,a,b,s=.55,bob=2,f=3)
    di(cv,c,'t20n_dan',2300,890,1700,890,t,a,b,s=.55,bob=2,f=3.4,lat=True)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3)
    cuon(cv,600,470,t,'SỬ NHÀ ĐƯỜNG','820|bị chém',col=DUONGC,s=.6,sz=52,u=inn(t,a+.3,.6),glow=1-inn(t,q,.4))
    cuon(cv,1320,470,t,'TOÀN THƯ','828|còn đuổi|quan nhà Đường',col=RED,s=.6,sz=44,u=inn(t,q,.6),glow=inn(t,q,.4)*(1-inn(t,q2,.4)))
    if not FREEZE and t>q2: put_screen(cv,band(760,80,PAPER,.9,14),960,840,inn(t,q2,.4));put_screen(cv,text('đến nay chưa được phân xử',38,INK,700),960,838,inn(t,q2,.4))
# ---- 34: kết
def S_34(cv,t):
    a=T[34]-.3;b=E[34]+4;q=sb(34,1)
    c=kc(t,[(a,(900,560,1.06)),(b,(1100,520,1.0))])
    ngoai(cv,c,t,g=880,seed=34,mist=.6)
    put(cv,c,'t20x_cuoi',960,560,s=1.0)
    for i in range(3): di(cv,c,'t20n_dan' if i%2 else 't20n_dan2',-300-i*220,890+i*14,500+i*180,890+i*14,t,a+i*.4,b,s=.5,bob=2,f=3.4+i*.3,ph=i)
    di(cv,c,'t20n_1ta',2300,885,1700,885,t,a,b,s=.55,bob=3,f=4,lat=True)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    if not FREEZE:
        giao(cv,360,420,t,rot=180*inn(t,a+.6,1.2),s=.36,o=inn(t,a+.3,.5))
        cuon(cv,1560,430,t,'HAI BỘ SỬ','?',col=RED,s=.38,sz=60,o=inn(t,q,.5))
        tx=text('Dương Thanh, năm 819–820',54,INK,700);put_screen(cv,wipe(tx,inn(t,a+1.2,1.4),0,.3,seed=20),W/2,150)
        put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,220,inn(t,E[34]+.6,1))
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
    flock=lambda *a,**k:None
S=lambda n:T[n]-.3
SH=[(0 if n==1 else S(n),S(n+1) if n<34 else V.TOTAL+1,globals()[f'S_{n}']) for n in range(1,35)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm20_full.json'))
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
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'DƯƠNG THANH','stitle20',.55)
    if not NOCAP: caps(cv,t)
V.NHAN={5:'Lý Tượng Cổ – quan nhà Đường đứng đầu An Nam',6:'Dương Thanh – thứ sử Hoan Châu',19:'Quế Trọng Vũ – quan nhà Đường',31:'Lý Nguyên Gia – quan nhà Đường',32:'Hàn Ước – quan nhà Đường'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
