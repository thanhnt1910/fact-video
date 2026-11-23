# Bản dài tm22: Đinh Bộ Lĩnh và Hoa Lư, năm 944–968 (lời kể bản 6, chủ kênh duyệt 23/11).
# Điểm nhấn: Hoa Lư, thung lũng bốn bề núi đá (mở ở cảnh 1, nhắc ở 8 và 15, khép ở 34). Chi tiết khép vòng: Đinh Liễn trên ngọn sào.
# Quy ước màu (hình ảnh, không phải khẳng định lịch sử): quân Đinh khăn đỏ; quân nhà Ngô mũ trụ, áo xanh lục, khiên lục; quân sứ quân khác khăn tím.
# Nhân vật có tên vẽ dáng riêng (t22n_*): Đinh Bộ Lĩnh giáp sẫm, khăn đỏ thẫm, đai vàng; hai vua Ngô áo bào lục/chàm; Trần Lãm áo nâu, râu trắng.
# Nơi chưa rõ vị trí (hai thôn Đường, Nguyễn ở Thái Bình xưa; Ô Man) không đặt lên bản đồ (thuy-mac.md mục 4.6).
import math,re,json,os
import numpy as np
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from engine import ragged,asc
from fx_tran import arrows,dust,sparks,fall
from tran_fx import clash
import tran_fx
tran_fx.MAU.update({'dinh':(.69,.16,.11),'ngo':(.24,.35,.27),'sq':(.33,.2,.4),'dan':(.4,.34,.26)})   # chỉ trong tiến trình tm22: 'ngo' là quân nhà Ngô (xanh lục)
from dai_tm2 import big,lb
V=K.setup('tm22',{3:4.0})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
FREEZE=bool(os.environ.get('KIEM_TINH'))
NANG=True   # màu nước, gió (thuy-mac.md mục 4.3c)
DOC=False
GS=1.45
NGOC=(.18,.32,.24)    # màu chữ phe nhà Ngô
SQC=(.33,.20,.40)     # màu chữ sứ quân khác
GOLDC=(.79,.64,.35)
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
    put(cv,c,'t22_far',960+(seed%7-3)*60,g-120,ay=1,k=.35,o=far)
    put(cv,c,'t22_mid',960-(seed%5-2)*40,g+30,ay=1,k=.62,o=midv)
    suong(cv,c,t,g-260,mist,seed)
def truoc(cv,c,t,o=1,l=True,r=True):
    if l: put(cv,c,'t22_frontL',-120,1120,ax=0,ay=1,k=1.3,s=.85,r=.8*math.sin(t*.6),o=o)
    if r: put(cv,c,'t22_frontR',2040,1120,ax=1,ay=1,k=1.3,s=.8,r=1.2*math.sin(t*.7+1),o=o)
QUAN=('t22n_dblvua','t22n_ngoquyen','t22n_tamkha','t22n_xvan','t22n_xngap','t22n_tranlam')
def hinh(name,t,flip,ph=0.0):
    if NANG and not FREEZE and name in QUAN:
        import mau21;im=mau21.gio(A(name),t,ph);return np.ascontiguousarray(im[:,::-1]) if flip else im
    return Af(name) if flip else name
def di(cv,c,name,x0,y0,x1,y1,t,a,b,s=1.0,o=.97,bob=4,f=5,ph=0,k=1.0,r=0,lac=1.2,lat=False):
    if y0>700 and k==1.0: s*=GS;bob*=GS
    u=inn(t,a,max(b-a,.1));x=x0+(x1-x0)*u;y=y0+(y1-y0)*u-abs(math.sin(t*f+ph))*bob*(1 if 0<u<1 else .3)
    put(cv,c,hinh(name,t,lat,ph+x0*.01),x,y,s=s,o=o,k=k,r=r+lac*math.sin(t*f*.5+ph),ay=1,scale_px=asc(name))
    return x,y
def nv(cv,c,name,x,y,t,s=.7,r=0,o=1.0,flip=False):
    th=(1+.007*math.sin(t*1.7+x)) if NANG and name in QUAN else 1.0
    put(cv,c,hinh(name,t,flip,x*.01),x,y-2*math.sin(t*1.6+x),s=(s*GS if y>700 else s)*th,ay=1,o=o,r=r+.6*math.sin(t*1.1+x),scale_px=asc(name))
def smoke(cv,c,x,y,t,s=1.0):
    for k in range(2): put(cv,c,'t12_spr_khoi',x+20*math.sin(t*.7+k),y-((t*40+k*120)%240),s=s,o=.5*(1-((t*40+k*120)%240)/240))
def flick(cv,c,x,y,t,s=1.0):
    put(cv,c,'t12_spr_lua',x+6*math.sin(t*7),y,s=min(s,.38)*(1+.08*math.sin(t*9)),o=.5+.3*math.sin(t*5)**2)
def dem(cv,o=.3):
    if not FREEZE: ink_wash(cv,o,col=np.array((.1,.1,.18),np.float32))
_NZ=None
def nz():
    global _NZ
    if _NZ is None:
        rg=np.random.default_rng(22);a=rg.random((34,60)).astype(np.float32)
        from PIL import Image as _I
        _NZ=np.asarray(_I.fromarray((a*255).astype(np.uint8)).resize((W,H),_I.BICUBIC),np.float32)/255
    return _NZ
_YY,_XX=np.mgrid[0:H,0:W].astype(np.float32)
def loang(cx,cy,r,soft=40):
    d=np.sqrt((_XX-cx)**2+(_YY-cy)**2)+(nz()-.5)*r*.35
    return np.clip((r-d)/soft,0,1)[...,None]
def mau(cv,dem=False,bd=False):
    if NANG and not FREEZE:
        import mau21
        if bd: mau21.to_mau_bd(cv)
        else: mau21.to_mau(cv,dem=dem)
def bui(cv,t):
    if NANG and not FREEZE:
        import mau21;mau21.bui(cv,t)
def cuon(cv,x,y,t,tieu,chu,col=None,o=1.0,s=.62,sz=46,u=1.0,glow=0.0):
    put(cv,C0,'t22_cuon',x,y,s=s,o=o,r=.5*math.sin(t*.7+x))
    if FREEZE: return
    if glow>0: put_screen(cv,band(int(500*s/.62),int(620*s/.62),GOLDC,.25*glow,40),x,y,o)
    put_screen(cv,text(tieu,28,INK,700),x,y-170*s/.62,o)
    for k,ln in enumerate(chu.split('|')): put_screen(cv,wipe(text(ln,sz,col if col is not None else RED,700),u,0,.25,seed=int(x)+k),x,y-40+k*(sz+16),o)
def o_dem(cv,x,y,n,tong,nhan,t,o=1.0,cot=None,gap=70):
    cot=cot or tong;rows=(tong+cot-1)//cot
    put_screen(cv,band(gap*cot+80,110+rows*gap,PAPER,.88,18),x,y+(rows-1)*gap/2,o)
    put_screen(cv,text(nhan,30,INK,700),x,y-52,o)
    for k in range(tong):
        xx=x-(cot-1)*gap/2+(k%cot)*gap;yy=y+18+(k//cot)*gap;on=k<n
        put_screen(cv,band(int(gap*.77),int(gap*.77),RED if on else INK,.85 if on else .2,4),xx,yy,o)
def pulse(cv,c,x,y,t,col=RED):
    for k in range(2):
        u=((t*.6+k*.5)%1.0);dot(cv,c,x,y,o=.6*(1-u),col=col,r=int(8+40*u))
def panel(cv,t,t0,dong,x=1450,y=300,w=540,col=INK,b=None):
    if FREEZE or t<t0: return
    u=inn(t,t0,.4)*(1-(inn(t,b,.4) if b else 0))
    h=40+sum(d[1]+18 for d in dong)
    put_screen(cv,band(w,h,PAPER,.88,16),x,y,u)
    yy=y-h/2+30
    for d in dong:
        put_screen(cv,text(d[0],d[1],d[2] if len(d)>2 else col,700),x,yy+d[1]/2,u);yy+=d[1]+18
def gach(cv,c,x,y,t,t0,w=180):
    """tên bị gạch đỏ: cái chết (không vẽ máu)"""
    if t>t0: stroke(cv,c,[(x-w/2,y+6),(x+w/2,y-10)],inn(t,t0,.5),wid=8,col=RED,o=.9,head=False)
# ---- bản đồ (map.png của mapink.py: kinh độ 103,5–114, tâm vĩ độ 21,35)
_KX=520*math.cos(math.radians(23));_x0=1.5*_KX;_w=10.5*_KX;_sc=2880/_w;_y0=(24.8-21.35)*520-_w*9/32
def wpt(lon,lat): return ((lon-102.0)*_KX-_x0)*_sc/1.5,((24.8-lat)*520-_y0)*_sc/1.5
PT={k:wpt(*v) for k,v in {'hoalu':(105.91,20.25),'coloa':(105.87,21.11),'bachdang':(106.80,20.85),'phongchau':(105.43,21.30),'duonglam':(105.47,21.15),
    'dodong':(105.77,20.87),'bohai':(106.33,20.45),'dangchau':(106.05,20.72)}.items()}
def mapbg2(cv,c,u=1.0,o=1.0):
    im=A('map')
    if u<1: im=wipe(im,u,0,.25,seed=4)
    put(cv,c,im,960,540,o=o,scale_px=1.5)
def mcam(t,keys):
    if FREEZE: t=keys[0][0]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z);return cam(cx,cy,z)
def hs(cv,o=1.0):
    """bản đồ có biển phía đông: Hoàng Sa, Trường Sa nằm ngoài khung (vĩ độ dưới 18), ghi thẻ ở mép phải (quy-tac/kiem-tra-lich-su.md)"""
    for k,s in enumerate(('Quần đảo Hoàng Sa (Việt Nam) ở phía đông nam','Trường Sa (Việt Nam) ở phía nam')):
        tx=text(s,24,RED,700);w=tx.shape[1]+50;xc=1880-w/2;y=790+k*54
        put_screen(cv,band(w,48,PAPER,.88,12),xc,y,o);put_screen(cv,tx,xc,y,o)
def mlb(cv,c,s,key,dx,dy,t,a,b,col=INK,sz=34):
    x,y=PT[key];lb(cv,c,s,x+dx,y+dy,t,a,b,col=col,sz=sz)

# ===== 1: giọt mực loang thành thung lũng; quân nhà Ngô kéo đến, rồi lùi; bóng kinh đô hiện ra
def mo(cv,t,a,b):
    q=sb(1,1);q2=sb(1,2)
    c=kc(t,[(a,(960,560,1.12)),(q,(1100,560,1.04)),(b,(1180,540,1.0))])
    ngoai(cv,c,t,g=880,seed=1,mist=.5,far=.75,midv=.55)
    put(cv,c,'t22x_hoalu',960,560,s=1.0)
    if t>q2-.3: put(cv,c,'t22x_kinh',960,560,s=1.0,o=.85*inn(t,q2-.3,1.6))
    mau(cv)
    u=inn(t,q,q2-q);back=inn(t,q+(q2-q)*.62,(q2-q)*.38)
    for i in range(3):
        x0=2500+i*260;xs=1500+i*200
        x=x0+(xs-x0)*u-(xs-x0)*.0+(x0-xs)*back*.9
        di(cv,c,'t22n_ngo',x,890+i*6,x,890+i*6,t,a,b,s=.5,bob=3,f=4+i*.3,ph=i,lat=back<.05)
    if q<t<q2: dust(cv,c,1650,880,o=.25,s=.4)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    return c
def S_1(cv,t):
    a,b=0,E[1]+.3;td=.95;q=sb(1,1);q2=sb(1,2)
    sc=PAP.copy();mo(sc,t,a,b)
    if FREEZE: cv[:]=sc;return
    if t<td:
        y=-40+(540+40)*(t/td)**2
        m=loang(960,y,22,6);cv[:]=cv*(1-m)+np.array(INK,np.float32)*m
    else:
        u=inn(t,td,1.6);r=30+u*1300
        m=loang(960,540,r,60);rim=np.clip(loang(960,540,r,60)-loang(960,540,r-70,60),0,1)
        cv[:]=cv*(1-m)+sc*m;cv[:]=cv*(1-rim*.75)+np.array(INK,np.float32)*rim*.75
    big(cv,'BỐN BỀ LÀ NÚI ĐÁ',t,1.6,q-.15,INK,180,76,seed=1)
    big(cv,'HAI VUA KHÔNG HẠ NỔI',t,q+.1,q2-.15,RED,180,76,seed=2)
    big(cv,'RỒI THÀNH KINH ĐÔ',t,q2+.1,b,INK,180,76,seed=3)
# ===== 2: người đứng trên đỉnh đá giữa sương; hai câu hỏi
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3;q=sb(2,1)
    c=kc(t,[(a,(820,560,1.08)),(b,(1000,540,1.0))])
    ngoai(cv,c,t,g=880,seed=2,mist=.7,far=.85,midv=.7)
    put(cv,c,'t22_frontL',1560,980,ax=.5,ay=1,k=.85,s=1.15,o=.9)
    mau(cv)
    nv(cv,c,'t22n_dbl',1020,885,t,s=.5,o=.9*inn(t,a+.6,.8))   # đứng trên mặt đất cạnh chân núi (cùng lớp k=1), không đặt trên đỉnh lớp núi trôi khác tốc độ
    for i in range(3): put(cv,c,'mist',(400+i*700+t*(30+i*8))%2600-300,620+i*60,s=2.4,o=.45,k=.9)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t,l=False)
    if not FREEZE: ink_wash(cv,.18)
    if not FREEZE:
        put_screen(cv,text('người giữ thung lũng ấy là ai?',46,INK,700),520,300,inn(t,a+.5,.4))
        put_screen(cv,text('vì sao nơi ấy thành kinh đô?',46,RED,700),520,390,inn(t,q,.4))
# ===== 3: bản đồ: Hoa Lư; sông Bạch Đằng
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3;q=sb(3,1)
    hx,hy=PT['hoalu'];bx,by=PT['bachdang']
    c=mcam(t,[(a,(hx+60,hy-80,2.0)),(q,(hx+160,hy-120,1.9)),(b,(bx-40,by-20,1.85))])
    mapbg2(cv,c,u=inn(t,a-.2,1.0))
    mau(cv,bd=True)
    pulse(cv,c,hx,hy,t,col=RED);dot(cv,c,hx,hy,col=RED,r=10)
    mlb(cv,c,'Hoa Lư','hoalu',0,-30,t,a+.4,b,col=RED)
    if t>q:
        dot(cv,c,bx,by,col=INK,r=8);mlb(cv,c,'sông Bạch Đằng','bachdang',30,-28,t,q+.2,b,sz=30)
        for i in range(3):
            u=((t*.12+i/3)%1.0);put(cv,c,'t22n_thuyen',bx+80-90*u,by+40+i*18,s=.07,scale_px=3,o=.8*(1-u),r=3*math.sin(t*3+i))
        stroke(cv,c,[(bx+120,by+90),(bx+40,by+40),(bx-10,by+6)],inn(t,q+.3,1.0),wid=5,col=RED,o=.8)
    for i in range(2):
        u=((t*.08+i*.5)%1.0);put(cv,c,'t22n_thuyen',hx+40+60*u,hy+30+i*14,s=.05,scale_px=3,o=.7,r=2*math.sin(t*2+i))
    put(cv,c,'mist',(hx-200+t*12)%600+hx-300,hy-40,s=.5,o=.25)
    flock(cv,c,t,.35,y0=420)
    hs(cv,o=inn(t,a+.3,.5))
    lb(cv,C0,'Hoa Lư: nay thuộc tỉnh Ninh Bình',960,200,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'Ngô Quyền thắng quân Nam Hán, giành quyền tự chủ',960,200,t,q+.2,b,col=RED,sz=38)
# ===== 4: điện một ngai: Ngô Quyền mất, Dương Tam Kha chiếm ngôi, Ngô Xương Ngập bỏ trốn
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3;q=sb(4,1);q2=sb(4,2);q3=sb(4,3)
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,540,1.07))])
    put(cv,c,'t22_far',960,760,ay=1,k=.35,o=.35)
    put(cv,c,'t22x_sanh1',960,610,s=.85)
    suong(cv,c,t,700,.3,4)
    mau(cv)
    nv(cv,c,'t22n_ngoquyen',960,885,t,s=.7,o=1-inn(t,q-.6,.8))
    gach(cv,c,960,470,t,q-.5,160)
    if t>q-.2: di(cv,c,'t22n_tamkha',2200,885,1250,885,t,q-.2,q2-.2,s=.68,bob=3,f=3.6,lat=True)
    if t>q3-.3: di(cv,c,'t22n_xngap',620,885,-300,885,t,q3-.3,b,s=.64,bob=5,f=6,lat=True)
    for i in range(2): smoke(cv,c,500+i*900,640,t+i,.4)
    bui(cv,t)
    truoc(cv,c,t,o=.9)
    lb(cv,c,'Ngô Quyền',960,500,t,a+.3,q-.2,col=RED,sz=34)
    lb(cv,c,'Dương Tam Kha: anh vợ Ngô Quyền',1300,500,t,q+.1,q3-.1,col=SQC,sz=32)
    lb(cv,c,'Ngô Xương Ngập: con trưởng',480,500,t,q3,b,col=NGOC,sz=32)
    lb(cv,C0,'Ngô Quyền xưng vương, vài năm sau qua đời',960,200,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'người thân cận trong nhà chiếm ngôi',960,200,t,q+.1,b,col=RED,sz=40)
# ===== 5: cổng triều: Ngô Xương Văn quay quân lật Dương Tam Kha; đón anh về; hai vua
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3;q=sb(5,1);q2=sb(5,2);q3=sb(5,3);q4=sb(5,4)
    c=kc(t,[(a,(760,560,1.06)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=5,mist=.4,far=.5,midv=.5)
    put(cv,c,'t22x_trieu',960,560,s=1.0)
    mau(cv)
    x,_=di(cv,c,'t22n_xvan',-300,885,820,885,t,a+.2,q,s=.66,bob=4,f=5)
    di(cv,c,'t22n_ngo',-900,890,300,890,t,a+.2,q,s=.5,bob=4,f=5.6,ph=1)
    di(cv,c,'t22n_ngo',-1500,900,-200,900,t,a+.4,q,s=.48,bob=4,f=5.9,ph=2)
    di(cv,c,'t22n_tamkha',1400,885,2500,885,t,q,q2,s=.64,bob=2,f=2.6,o=.6)
    if t>q2: di(cv,c,'t22n_xngap',-300,885,520,885,t,q2,q3,s=.64,bob=3,f=3.8)
    seal(cv,'s951',1650,330,q3+.2,t,s=.75,r=4)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'Ngô Xương Văn: con thứ',960,200,t,a+.3,q-.2,col=NGOC,sz=42)
    lb(cv,C0,'không giết, chỉ giáng chức',960,200,t,q+.1,q2-.2,col=INK,sz=42)
    lb(cv,C0,'đón anh về cùng lo việc nước',960,200,t,q2+.1,q3-.2,col=NGOC,sz=42)
    if t>q3:
        lb(cv,c,'Thiên Sách Vương (anh)',520,330,t,q3+.1,b,col=NGOC,sz=32);lb(cv,c,'Nam Tấn Vương (em)',x,330,t,q3+.3,b,col=NGOC,sz=32)
# ===== 6: điện hai ngai: một bên sáng, một bên mờ
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3;q=sb(6,1);q2=sb(6,2)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.08))])
    put(cv,c,'t22_far',960,760,ay=1,k=.35,o=.3)
    put(cv,c,'t22x_sanh2',960,610,s=.85)
    suong(cv,c,t,700,.25,6)
    mau(cv)
    g=inn(t,q,1.2)
    if not FREEZE:
        X,Y=c.p(706,560);put_screen(cv,band(300,460,GOLDC,.26*g*(.7+.3*math.sin(t*3)),60),X,Y,1)
    nv(cv,c,'t22n_xngap',560,885,t,s=.72*(1+.06*g))
    nv(cv,c,'t22n_xvan',1360,885,t,s=.7*(1-.08*g),o=1-.45*g,flip=True)
    for i in range(2): smoke(cv,c,960+i*30,700,t+i,.35)
    bui(cv,t)
    truoc(cv,c,t,o=.9)
    lb(cv,C0,'hai anh em không thể cùng chia quyền lâu',960,200,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'Thiên Sách Vương nắm hết việc lớn',960,200,t,q+.1,q2-.2,col=NGOC,sz=42)
    lb(cv,C0,'cùng mang danh vua, quyền không ngang nhau',960,200,t,q2+.1,b,col=RED,sz=40)
# ===== 7: Hoa Lư: Đinh Bộ Lĩnh đứng giữa núi đá, quân khăn đỏ
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3;q=sb(7,1);q2=sb(7,2)
    c=kc(t,[(a,(1150,560,1.08)),(b,(900,560,1.0))])
    ngoai(cv,c,t,g=880,seed=7,mist=.5)
    put(cv,c,'t22_frontL',300,1000,ax=.5,ay=1,k=.8,s=1.1,o=.95)
    put(cv,c,'t22_frontL',1750,1010,ax=.5,ay=1,k=.8,s=1.05,o=.95)
    mau(cv)
    nv(cv,c,'t22n_dbl',960,885,t,s=.72,o=inn(t,q-.3,.6))
    di(cv,c,'t22n_dinh',-700,890,520,890,t,q,q2+1.5,s=.5,bob=3,f=4.4)
    di(cv,c,'t22n_dinh',2600,890,1420,890,t,q+.3,q2+1.8,s=.48,bob=3,f=4.7,ph=1,lat=True)
    smoke(cv,c,1500,640,t,.4)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t,l=False)
    lb(cv,C0,'ở Hoa Lư, một người không chịu cúi đầu',960,200,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'Đinh Bộ Lĩnh',960,200,t,q,q2-.2,col=RED,sz=48)
    lb(cv,C0,'giữ riêng một vùng, không nghe lệnh triều đình',960,200,t,q2+.1,b,col=INK,sz=38)
# ===== 8 (cảnh trọng tâm 1): Hoa Lư nhìn từ trên: vòng núi đá vẽ dần; mũi tên từ ngoài dừng ở vách
def S_8(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1);q2=sb(8,2)
    c=kc(t,[(a,(960,500,1.18)),(q,(960,520,1.06)),(b,(960,540,1.0))])
    put(cv,c,'t22_far',960,330,ay=1,k=.35,o=.25)
    im=A('t22x_tren');u=inn(t,a,max(q-a,.5))
    put(cv,c,wipe(im,u,0,.25,seed=8) if u<1 and not FREEZE else im,960,540,s=1.0)
    mau(cv,bd=True)
    for i in range(4):
        k=(t*.5+i*.25)%1.0;ang=i*1.6+.3
        x0=960+math.cos(ang)*900;y0=520+math.sin(ang)*560;x1=960+math.cos(ang)*620;y1=520+math.sin(ang)*360
        if t>q2-.2: stroke(cv,c,[(x0,y0),(x0+(x1-x0)*min(1,k*1.4),y0+(y1-y0)*min(1,k*1.4))],1,wid=5,col=NGOC,o=.75*(1-max(0,k-.7)/.3))
    if t>q: pulse(cv,c,960,500,t,col=RED)
    for i in range(3): put(cv,c,'mist',(200+i*800+t*25)%2400-200,300+i*220,s=2.0,o=.3,k=.9)
    put(cv,c,'mist',(t*40)%2600-300,980,s=3.0,o=.35,k=1.25)
    flock(cv,c,t,.4,y0=200)
    lb(cv,C0,'bốn bề núi đá dựng đứng',960,200,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'bên trong: khoảng đất tương đối bằng phẳng',960,200,t,q+.1,q2-.2,col=INK,sz=40)
    lb(cv,C0,'quân bên ngoài rất khó đánh vào',960,200,t,q2+.1,b,col=RED,sz=42)
# ===== 9: đường từ Hoa Lư về triều: Đinh Liễn theo người đưa tin
def S_9(cv,t):
    a,b=T[9]-.3,E[9]+.3;q=sb(9,1);q2=sb(9,2)
    c=kc(t,[(a,(1150,560,1.04)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=9,mist=.45,far=1.0,midv=.8)
    put(cv,c,'t22_frontL',1950,1000,ax=.5,ay=1,k=.8,s=1.0,o=.9)
    mau(cv)
    if t<q: di(cv,c,'t22n_1ngo',-200,890,520,890,t,a,q,s=.52,bob=3,f=4.6)
    nv(cv,c,'t22n_dbl',1600,885,t,s=.66,o=inn(t,q-.4,.5))
    if t>q: di(cv,c,'t22n_lien',1450,885,300,885,t,q+.2,b,s=.6,bob=3,f=4,lat=True)
    if t>q: di(cv,c,'t22n_su',1250,885,100,885,t,q+.2,b,s=.6,bob=3,f=4.2,ph=1,lat=True)
    seal(cv,'s951',1650,330,q2+.2,t,s=.75,r=4)
    smoke(cv,c,1750,640,t,.4)
    di(cv,c,'t22n_dan2',300,720,700,720,t,a,b,s=.32,bob=2,f=3,k=.75,o=.7)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t,r=False)
    lb(cv,C0,'hai vua nhà Ngô định đem quân đến đánh',960,200,t,a+.3,q-.2,col=NGOC,sz=40)
    lb(cv,C0,'Đinh Liễn, con trai Đinh Bộ Lĩnh, vào triều làm con tin',960,200,t,q+.1,q2-.1,col=RED,sz=36)
    lb(cv,C0,'khoảng năm 951',960,200,t,q2+.1,b,col=INK,sz=42)
# ===== 10: trong triều: hai vua trách, giữ Đinh Liễn lại; quân lên đường
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3;q=sb(10,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(900,540,1.07))])
    put(cv,c,'t22_far',960,760,ay=1,k=.35,o=.3)
    put(cv,c,'t22x_ngai0',960,610,s=.85)
    suong(cv,c,t,700,.25,10)
    mau(cv)
    nv(cv,c,'t22n_xngap',700,885,t,s=.68)
    nv(cv,c,'t22n_xvan',1230,885,t,s=.66,flip=True)
    di(cv,c,'t22n_lien',1700,885,1480,885,t,a+.2,a+1.6,s=.56,bob=2,f=3,lat=True,r=-6*inn(t,a+1.6,.5))
    if t>q:
        di(cv,c,'t22n_1ngo',2300,890,1650,890,t,q,q+1.4,s=.5,bob=3,f=4.4,lat=True)
        di(cv,c,'t22n_ngo',-900,895,2600,895,t,q+.6,b+3,s=.46,bob=3,f=5)
    bui(cv,t)
    truoc(cv,c,t,o=.9)
    lb(cv,C0,'hai vua trách Đinh Bộ Lĩnh không tự mình vào triều',960,200,t,a+.3,q-.2,col=NGOC,sz=38)
    lb(cv,C0,'giữ Đinh Liễn lại, mang theo khi kéo quân',960,200,t,q+.1,b,col=RED,sz=40)
# ===== 11: khe núi: quân Ngô đánh, bị đẩy lùi; đếm ngày
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,540,1.06))],sh=1.5)
    ngoai(cv,c,t,g=880,seed=11,mist=.4,far=.6,midv=.5)
    put(cv,c,'t22x_khe',960,560,s=1.0)
    mau(cv)
    L=b-a;ph=((t-a)/max(L,.1))
    clash(cv,c,t,a+.2,b,'ngo','dinh',xm=1180,y=790,s=.5,push=-1,seed=11,pre='t22n_')
    for k in range(2): dust(cv,c,950+k*120,880,o=.3,s=.4)
    if not FREEZE:
        n=min(30,int(30*ph)+1)
        for k in range(n): stroke(cv,C0,[(1460+(k%10)*34,300+(k//10)*44),(1460+(k%10)*34,330+(k//10)*44)],1,wid=5,col=INK,o=.75,head=False)
        put_screen(cv,text('hơn một tháng',34,RED,700),1610,250,inn(t,a+.4,.4))
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'đánh hơn một tháng, vẫn không hạ được Hoa Lư',960,200,t,a+.3,b,col=NGOC,sz=40)
# ===== 12 (cảnh trọng tâm 2): ngọn sào dựng lên trước trại; người đưa tin chạy về phía núi
def S_12(cv,t):
    a,b=T[12]-.3,E[12]+.3;q=sb(12,1)
    c=kc(t,[(a,(900,560,1.04)),(b,(1100,540,1.0))])
    ngoai(cv,c,t,g=880,seed=12,mist=.35,far=.55,midv=.45)
    put(cv,c,'t22x_trai',960,560,s=1.0)
    mau(cv,dem=True)
    u=inn(t,a+.4,1.6);ang=-(1-u)*70
    put(cv,c,'t22_sao',1000,900,s=.8,ax=.5,ay=1,r=ang+1.2*math.sin(t*1.5),scale_px=1.5)
    nv(cv,c,'t22n_xngap',720,885,t,s=.62)
    nv(cv,c,'t22n_xvan',1260,885,t,s=.6,flip=True)
    if t>q: di(cv,c,'t22n_su',1350,885,2400,885,t,q,b+1,s=.56,bob=5,f=7)
    for i in range(3): smoke(cv,c,350+i*240,600,t+i,.35)
    flock(cv,c,t,.4)
    bui(cv,t)
    truoc(cv,c,t)
    dem(cv,.22)
    lb(cv,C0,'họ treo Đinh Liễn lên ngọn sào',960,200,t,a+.3,q-.2,col=RED,sz=42)
    lb(cv,C0,'không chịu hàng thì con trai sẽ bị giết',960,200,t,q+.1,b,col=NGOC,sz=40)
# ===== 13: Đinh Bộ Lĩnh nổi giận; hàng tay nỏ giương lên
def S_13(cv,t):
    a,b=T[13]-.3,E[13]+.3;q=sb(13,1);q2=sb(13,2)
    c=kc(t,[(a,(700,560,1.1)),(q2,(900,560,1.02)),(b,(1150,540,1.0))])
    ngoai(cv,c,t,g=880,seed=13,mist=.35,far=.7,midv=.5)
    put(cv,c,'t22_frontL',320,1040,ax=.5,ay=1,k=.85,s=1.25,o=.95)
    mau(cv)
    nv(cv,c,'t22n_dbl2' if t>q else 't22n_dbl',620,885,t,s=.74)
    if t>q2-.2:
        for i in range(3): di(cv,c,'t22n_nohang',300+i*80,890+i*8,820+i*80,890+i*8,t,q2-.2+i*.2,q2+.8+i*.2,s=.42,bob=2,f=3.4+i*.2,ph=i)
    put(cv,c,'t22_saoxa',1820,640,s=.42,ax=.5,ay=1,k=.7,r=2.5*math.sin(t*1.5),scale_px=1.5,o=.8)
    di(cv,c,'t22n_dinh',1300,720,800,720,t,a,b,s=.3,bob=2,f=3.2,k=.75,lat=True,o=.7)
    smoke(cv,c,1500,620,t,.35);smoke(cv,c,1150,640,t+1.3,.3)
    di(cv,c,'t22n_1dinh',1200,890,900,890,t,a,b,s=.46,bob=2,f=3.4,lat=True)
    if t>q2: dust(cv,c,1000,880,o=.2,s=.35)
    bui(cv,t)
    truoc(cv,c,t,l=False)
    if not FREEZE: ink_wash(cv,.16*inn(t,q,.6))
    lb(cv,C0,'Đinh Bộ Lĩnh nổi giận',960,200,t,a+.3,q-.2,col=RED,sz=44)
    lb(cv,C0,'người làm việc lớn đâu có xót con',960,200,t,q+.1,q2-.2,col=INK,sz=40)
    lb(cv,C0,'sai hơn mười người cầm nỏ',960,200,t,q2+.1,b,col=RED,sz=42)
# ===== 14: hai vua kinh sợ, rút quân
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3;q=sb(14,1);q2=sb(14,2)
    c=kc(t,[(a,(1000,560,1.06)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=14,mist=.45,far=.8,midv=.6)
    put(cv,c,'t22x_rut',960,560,s=1.0)
    mau(cv)
    nv(cv,c,'t22n_xngap',820,885,t,s=.64,r=-4*inn(t,a+.3,.4),flip=True)
    nv(cv,c,'t22n_xvan',1100,885,t,s=.62,r=-5*inn(t,a+.4,.4),flip=True)
    if t>q2-.3:
        di(cv,c,'t22n_ngo',900,890,-900,890,t,q2-.3,b+1.5,s=.5,bob=3,f=4.6,lat=True)
        di(cv,c,'t22n_ngo',1500,900,-300,900,t,q2,b+1.8,s=.48,bob=3,f=4.9,ph=1,lat=True)
    put(cv,c,'t22_saodo',1650,900,s=.55,ax=.5,ay=1,r=-6*inn(t,q2,1.2),o=.85*(1-inn(t,b-.6,.5)),scale_px=1.5)
    di(cv,c,'t22n_1ngo',2300,895,1500,895,t,a,b,s=.46,bob=3,f=3.6,lat=True)
    smoke(cv,c,350,640,t,.35);smoke(cv,c,2000,640,t+1,.35)
    if t>q2: dust(cv,c,700,880,o=.25,s=.4)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'hai vua nhà Ngô kinh sợ',960,200,t,a+.3,q-.2,col=NGOC,sz=44)
    lb(cv,C0,'treo con người ấy cũng chẳng ích gì',960,200,t,q+.1,q2-.2,col=INK,sz=40)
    lb(cv,C0,'không giết Đinh Liễn, rút quân về',960,200,t,q2+.1,b,col=RED,sz=42)
# ===== 15: ngọn sào trống giữa sương núi; dấu hỏi
def S_15(cv,t):
    a,b=T[15]-.3,E[15]+.3;q=sb(15,1);q2=sb(15,2)
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,520,1.12))])
    ngoai(cv,c,t,g=880,seed=15,mist=.8,far=1.0,midv=.75)
    put(cv,c,'t22_saotrong',960,900,s=.85,ax=.5,ay=1,r=1.5*math.sin(t*.9),scale_px=1.5,o=.9)
    mau(cv)
    for i in range(4): put(cv,c,'mist',(200+i*600+t*(26+i*6))%2600-300,520+i*70,s=2.6,o=.5,k=.95)
    di(cv,c,'t22n_dan',1500,700,1150,700,t,a,b,s=.32,bob=2,f=3,k=.75,lat=True,o=.6)
    di(cv,c,'t22n_dan2',300,705,620,705,t,a+.5,b,s=.3,bob=2,f=3.3,k=.75,o=.55)
    flock(cv,c,t,.4)
    bui(cv,t)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.2)
    lb(cv,C0,'vì sao ông nói và làm như vậy? không ai biết chắc',960,200,t,a+.3,q-.2,col=INK,sz=38)
    lb(cv,C0,'chỉ biết: hai vua phải rút khỏi Hoa Lư',960,200,t,q+.1,q2-.2,col=RED,sz=40)
    lb(cv,C0,'người con trên ngọn sào sẽ còn xuất hiện',960,200,t,q2+.1,b,col=INK,sz=40)
# ===== 16: Thiên Sách Vương mất; chỉ còn Nam Tấn Vương
def S_16(cv,t):
    a,b=T[16]-.3,E[16]+.3;q=sb(16,1)
    c=kc(t,[(a,(960,540,1.06)),(b,(980,560,1.0))])
    put(cv,c,'t22_far',960,780,ay=1,k=.35,o=.4)
    put(cv,c,'t22_mid',960,920,ay=1,k=.6,o=.3)
    put(cv,c,'t22_ngai',960,860,s=1.0,ay=1)
    suong(cv,c,t,700,.35,16)
    mau(cv)
    nv(cv,c,'t22n_xngap',640,885,t,s=.66,o=1-inn(t,a+.6,1.2))
    if t<q: gach(cv,c,640,360,t,a+.8,200)
    nv(cv,c,'t22n_xvan',1260,885,t,s=.66,o=inn(t,q-.2,.8),flip=True)
    for i in range(2): flick(cv,c,420+i*1080,620,t+i,.3)
    for i in range(2): smoke(cv,c,420+i*1080,560,t+i,.3)
    bui(cv,t)
    truoc(cv,c,t,o=.85)
    lb(cv,c,'Thiên Sách Vương Ngô Xương Ngập',640,330,t,a+.3,q,col=NGOC,sz=30)
    lb(cv,c,'Nam Tấn Vương Ngô Xương Văn',1260,330,t,q,b,col=NGOC,sz=30)
    lb(cv,C0,'ít năm sau, Thiên Sách Vương qua đời',960,200,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'chỉ còn một vua',960,200,t,q+.1,b,col=NGOC,sz=44)
# ===== 17: năm 965: thuyền cập bến hai thôn, phục binh nỏ; Nam Tấn Vương trúng tên
def S_17(cv,t):
    a,b=T[17]-.3,E[17]+.3;q=sb(17,1);q2=sb(17,2)
    c=kc(t,[(a,(700,560,1.06)),(b,(1000,560,1.0))],sh=1.2 if q<t<q2+1 else 0)
    ngoai(cv,c,t,g=880,seed=17,mist=.4)
    put(cv,c,'t22x_lang',960,560,s=1.0)
    mau(cv)
    u=inn(t,a+.2,q-a)
    for i in range(3): put(cv,c,'t22n_thuyen',-200+760*u+i*170,820+i*16,s=.6,scale_px=3,r=2*math.sin(t*2+i))
    if t>q-.3: nv(cv,c,'t22n_xvan',700,860,t,s=.56,r=-60*inn(t,q2,.8),o=1-.4*inn(t,q2+.6,1))
    if t>q: put(cv,c,Af('t22n_phuc'),1480,850,s=.5,ax=.5,ay=1,scale_px=3,o=inn(t,q,.4),r=.8*math.sin(t*5))
    if q<t<q2+1 and not FREEZE:
        for i in range(5):
            k=((t*1.3+i*.2)%1.0);x0,y0=1300,760;x1,y1=760,700
            xs=x0+(x1-x0)*k;ys=y0+(y1-y0)*k-120*math.sin(k*math.pi)
            put(cv,c,'arrow',xs,ys,s=.6,r=180+20*math.cos(k*math.pi),scale_px=1.5,o=.9)
    gach(cv,c,700,420,t,q2+.2,200)
    seal(cv,'s965',1650,330,a+.5,t,s=.8,r=4)
    bui(cv,t)
    truoc(cv,c,t,l=False)
    lb(cv,c,'Nam Tấn Vương',700,420,t,a+.5,b,col=NGOC,sz=32)
    lb(cv,C0,'hai thôn Đường, Nguyễn ở Thái Bình xưa (chưa rõ nay ở đâu)',960,200,t,a+.3,q-.2,col=INK,sz=34)
    lb(cv,C0,'vừa lên bờ, gặp phục binh cầm nỏ',960,200,t,q+.1,q2-.2,col=RED,sz=42)
    lb(cv,C0,'Ngô Xương Văn bị bắn chết',960,200,t,q2+.1,b,col=RED,sz=44)
# ===== 18: mười lăm năm trước, cũng hai thôn ấy; cuộn lời bàn Ngô Sĩ Liên
def S_18(cv,t):
    a,b=T[18]-.3,E[18]+.3;q=sb(18,1);q2=sb(18,2);q3=sb(18,3)
    c=kc(t,[(a,(1150,560,1.04)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=18,mist=.45,far=.6,midv=.5)
    put(cv,c,'t22x_langcu',960,560,s=1.0)
    mau(cv)
    if not FREEZE: ink_wash(cv,.18,col=np.array((.45,.36,.22),np.float32))
    if t<q3:
        x,_=di(cv,c,'t22n_xvan',-200,885,900,885,t,a+.2,q2,s=.62,bob=3,f=4.4,lat=(t>q2))
        di(cv,c,'t22n_ngo',-900,890,300,890,t,a+.2,q2,s=.48,bob=3,f=4.8,ph=1,lat=(t>q2))
    if q2<t<q3: di(cv,c,'t22n_ngo',300,890,-900,890,t,q2,q3,s=.48,bob=3,f=5.2,lat=True)
    smoke(cv,c,520,560,t,.35);smoke(cv,c,820,560,t+1,.3)
    if t>q3-.3: cuon(cv,1450,500,t,'LỜI BÀN NGÔ SĨ LIÊN','ham việc đánh dẹp',col=RED,s=.55,sz=44,u=inn(t,q3,.8),o=inn(t,q3-.3,.4))
    flock(cv,c,t,.4)
    bui(cv,t)
    truoc(cv,c,t,o=.9)
    lb(cv,C0,'hai thôn ấy, mười lăm năm trước',960,200,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'Dương Tam Kha sai Ngô Xương Văn đến đánh',960,200,t,q+.1,q2-.2,col=SQC,sz=40)
    lb(cv,C0,'giữa đường, ông quay quân lật Dương Tam Kha',960,200,t,q2+.1,q3-.2,col=NGOC,sz=40)
# ===== 19: Đinh Liễn trở về Hoa Lư lúc trời sáng
def S_19(cv,t):
    a,b=T[19]-.3,E[19]+.3;q=sb(19,1)
    c=kc(t,[(a,(800,560,1.06)),(b,(1100,560,1.0))])
    put(cv,c,'t22_far',960,760,ay=1,k=.35,o=.6)
    put(cv,c,'t22x_hoalu2',960,560,s=1.0)
    suong(cv,c,t,620,.5,19)
    mau(cv)
    di(cv,c,'t22n_lien',-200,885,1000,885,t,a+.2,b,s=.62,bob=3,f=4)
    nv(cv,c,'t22n_dbl',1500,885,t,s=.66,flip=True,o=inn(t,a+1,.6))
    di(cv,c,'t22n_dan',2300,890,1800,890,t,a,b,s=.5,bob=2,f=3,lat=True)
    smoke(cv,c,1200,620,t,.35);smoke(cv,c,700,620,t+1,.3)
    put(cv,c,'sun',700,300,s=.45,o=.45*inn(t,a,1.5),k=.3)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'cũng năm 965, Đinh Liễn trở về Hoa Lư',960,200,t,a+.3,q-.2,col=RED,sz=40)
    lb(cv,C0,'những năm trước đó ông ở đâu, không ai rõ',960,200,t,q+.1,b,col=INK,sz=40)
# ===== 20: ngai trống; khói các vùng bốc lên; sứ quân nổi lên
def S_20(cv,t):
    a,b=T[20]-.3,E[20]+.3;q=sb(20,1);q2=sb(20,2)
    c=kc(t,[(a,(960,560,1.08)),(b,(960,540,1.0))])
    ngoai(cv,c,t,g=880,seed=20,mist=.35,far=.6,midv=.5)
    put(cv,c,'t22x_khoi',960,560,s=1.0)
    mau(cv)
    for i in range(6):
        t0=q+i*(q2-q)/6
        if t>t0: smoke(cv,c,250+i*300,560+(i%2)*30,t+i,.5*inn(t,t0,.6));flick(cv,c,250+i*300,600+(i%2)*30,t+i,.25)
    di(cv,c,'t22n_sq',-700,890,500,890,t,q,b+1,s=.46,bob=3,f=4.4)
    di(cv,c,'t22n_1ngo',2400,890,1500,890,t,q+.4,b+1,s=.48,bob=3,f=4.8,lat=True)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'nhà Ngô không còn vua',960,200,t,a+.3,q-.2,col=NGOC,sz=44)
    lb(cv,C0,'người có quân riêng ở các nơi nổi lên',960,200,t,q+.1,q2-.2,col=RED,sz=40)
    lb(cv,C0,'sứ quân: người cầm quân giữ riêng một vùng',960,200,t,q2+.1,b,col=SQC,sz=40)
# ===== 21: bản đồ các vùng sứ quân
def S_21(cv,t):
    a,b=T[21]-.3,E[21]+.3;q=sb(21,1)
    hx,hy=PT['hoalu'];px,py=PT['phongchau'];bx,by=PT['bohai']
    c=mcam(t,[(a,(px+60,py+40,2.3)),(q,(hx+150,hy-80,1.9)),(b,(bx-40,by-60,1.9))])
    mapbg2(cv,c,u=inn(t,a-.2,1.0))
    mau(cv,bd=True)
    L=E[21]-T[21]
    for k,(key,lab,col,f,dx,dy) in enumerate((('phongchau','Phong Châu',SQC,.0,-40,-24),('duonglam','Đường Lâm',SQC,.18,-70,40),('dodong','Đỗ Động Giang',SQC,.36,90,10),('bohai','Bố Hải Khẩu: Trần Lãm',RED,.62,40,-26))):
        t0=T[21]+L*f
        if t>t0:
            x,y=PT[key];dot(cv,c,x,y,col=col,r=7);pulse(cv,c,x,y,t,col=col)
            mlb(cv,c,lab,key,dx,dy,t,t0,b,col=col,sz=22)
    dot(cv,c,hx,hy,col=RED,r=9);mlb(cv,c,'Hoa Lư','hoalu',0,30,t,a+.3,b,col=RED,sz=26)
    for k,key in enumerate(('phongchau','duonglam','dodong','bohai','hoalu')):
        x,y=PT[key];put(cv,c,'t12_spr_khoi',x+4*math.sin(t+k),y-10-((t*12+k*9)%30),s=.06,o=.5)
    flock(cv,c,t,.35,y0=420)
    hs(cv,o=inn(t,a+.3,.5))
    lb(cv,C0,'mỗi vùng một người giữ',960,200,t,a+.3,b,col=SQC,sz=40)
# ===== 22: mười hai ô triện; đất xé thành từng mảnh
def S_22(cv,t):
    a,b=T[22]-.3,E[22]+.3;q=sb(22,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.06))])
    ngoai(cv,c,t,g=880,seed=22,mist=.4,far=.8,midv=.7)
    mau(cv)
    if not FREEZE:
        sp=inn(t,q,1.6)
        for k in range(12):
            ang=k/12*2*math.pi;dx=math.cos(ang)*120*sp;dy=math.sin(ang)*60*sp
            x,y=c.p(560+(k%6)*160+dx,640+(k//6)*120+dy)
            put_screen(cv,band(140,100,(.78,.70,.55),.92,4),x,y,inn(t,a+.2,.4),r=8*sp*math.sin(k))
            stroke(cv,C0,[(x-60,y-40),(x+60,y+40)],sp,wid=3,col=INK,o=.35,head=False)
    di(cv,c,'t22n_sq',-600,890,400,890,t,a,b,s=.44,bob=3,f=4)
    di(cv,c,'t22n_sq',2500,895,1600,895,t,a+.3,b,s=.42,bob=3,f=4.3,lat=True)
    for i in range(3): smoke(cv,c,500+i*480,580,t+i,.4)
    bui(cv,t)
    truoc(cv,c,t)
    if not FREEZE: o_dem(cv,1480,300,min(12,int(12*inn(t,a+.3,max(q-a-.3,.5)))+(1 if t>a+.3 else 0)),12,'mười hai sứ quân',t,cot=6,gap=56)
    lb(cv,C0,'mười hai người, mười hai vùng',760,200,t,a+.3,q-.2,col=SQC,sz=42)
    lb(cv,C0,'đất nước bị xé ra thành từng mảnh',760,200,t,q+.1,b,col=RED,sz=42)
# ===== 23: hai cuộn sử: Toàn thư và Cương mục chép khác nhau
def S_23(cv,t):
    a,b=T[23]-.3,E[23]+.3;q=sb(23,1);q2=sb(23,2);q3=sb(23,3);q4=sb(23,4)
    c=kc(t,[(a,(960,560,1.04)),(b,(960,540,1.0))])
    ngoai(cv,c,t,g=880,seed=23,mist=.5,far=.5,midv=.4)
    mau(cv)
    for i in range(2): smoke(cv,c,300+i*1300,700,t+i,.35)
    flock(cv,c,t,.35)
    bui(cv,t)
    if not FREEZE: ink_wash(cv,.22)
    cuon(cv,620,500,t,'TOÀN THƯ','sau khi nhà Ngô|mất vua',col=NGOC,s=.58,sz=40,u=inn(t,q,.8),glow=inn(t,q,.4)*(1-inn(t,q2,.4)))
    cuon(cv,1300,500,t,'CƯƠNG MỤC','nổi lên trước sau,|không cùng lúc',col=RED,s=.58,sz=40,u=inn(t,q2,.8),glow=inn(t,q2,.4)*(1-inn(t,q3,.4)))
    if t>q3: pulse(cv,C0,1300,820,t,col=RED)
    lb(cv,C0,'các bộ sử không chép giống nhau',960,200,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'Đinh Bộ Lĩnh đã giữ Hoa Lư từ trước',960,200,t,q3+.1,q4-.2,col=RED,sz=40)
    lb(cv,C0,'ông gây dựng lực lượng thế nào?',960,200,t,q4+.1,b,col=INK,sz=42)
# ===== 24: năm 967: cha con Đinh Bộ Lĩnh đến cửa biển Bố Hải
def S_24(cv,t):
    a,b=T[24]-.3,E[24]+.3;q=sb(24,1)
    c=kc(t,[(a,(1150,560,1.04)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=24,mist=.4,far=.5,midv=.5)
    put(cv,c,'t22x_cuahai',960,560,s=1.0)
    mau(cv)
    di(cv,c,'t22n_dbl',2300,885,1300,885,t,a+.2,b,s=.64,bob=3,f=4,lat=True)
    di(cv,c,'t22n_lien',2500,885,1500,885,t,a+.2,b,s=.58,bob=3,f=4.3,ph=1,lat=True)
    nv(cv,c,'t22n_tranlam',700,885,t,s=.66,o=inn(t,q-.2,.6))
    for i in range(2): put(cv,c,'t22n_thuyen',1700+i*260+40*math.sin(t*.5+i),800+i*30,s=.45,scale_px=3,r=2*math.sin(t*2+i))
    seal(cv,'s967',1650,330,a+.5,t,s=.8,r=4)
    bui(cv,t)
    truoc(cv,c,t,l=False)
    lb(cv,c,'Trần Lãm',700,330,t,q,b,col=RED,sz=34)
    lb(cv,C0,'năm 967, hai cha con đến nương nhờ Trần Lãm',960,200,t,a+.3,q-.2,col=RED,sz=40)
    lb(cv,C0,'người hiền đức, không có con trai nối nghiệp',960,200,t,q+.1,b,col=INK,sz=40)
# ===== 25: Trần Lãm nhận làm con nuôi, giao quân
def S_25(cv,t):
    a,b=T[25]-.3,E[25]+.3;q=sb(25,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1000,540,1.07))])
    put(cv,c,'t22_far',960,760,ay=1,k=.35,o=.3)
    put(cv,c,'t22x_dinhtran',960,610,s=.85)
    suong(cv,c,t,700,.25,25)
    mau(cv)
    nv(cv,c,'t22n_tranlam',700,885,t,s=.68)
    nv(cv,c,'t22n_dbl',1180,885,t,s=.68,flip=True,r=-8*inn(t,a+.8,.5)*(1-inn(t,q-.2,.5)))
    if t>q-.3: di(cv,c,'t22n_dinh',2600,890,1500,890,t,q-.3,b,s=.48,bob=3,f=4.4,lat=True)
    di(cv,c,'t22n_1dinh',300,890,520,890,t,a,b,s=.48,bob=2,f=3)
    for i in range(2): smoke(cv,c,400+i*1100,600,t+i,.3)
    if not FREEZE:
        X,Y=c.p(940,560);u=inn(t,a+1.2,1.0)
        put_screen(cv,band(54,40,RED,.85,6),X-150+260*u*(1-inn(t,q,.5))+0,Y-40*math.sin(u*math.pi),inn(t,a+1,.3)*(1-inn(t,b-.4,.4)))
    bui(cv,t)
    truoc(cv,c,t,o=.9)
    lb(cv,C0,'nhận làm con nuôi, giao cho cầm quân',960,200,t,a+.3,q-.2,col=RED,sz=40)
    lb(cv,C0,'có thêm cả quân của Trần Lãm',960,200,t,q+.1,b,col=INK,sz=42)
# ===== 26: giáp trận với các sứ quân khác; Phạm Bạch Hổ xin hàng
def S_26(cv,t):
    a,b=T[26]-.3,E[26]+.3;q=sb(26,1)
    c=kc(t,[(a,(900,560,1.06)),(b,(1050,560,1.0))],sh=1.5 if t<q else 0)
    ngoai(cv,c,t,g=880,seed=26,mist=.35,far=.6,midv=.5)
    put(cv,c,'t22x_dong',960,560,s=1.0)
    mau(cv)
    u=inn(t,a+.2,q-a)
    x,_=di(cv,c,'t22n_dbl',-200,885,700,885,t,a+.2,q,s=.66,bob=5,f=6)
    di(cv,c,'t22n_dinh',-800,890,520,890,t,a+.2,q,s=.5,bob=4,f=6.4,ph=1)
    clash(cv,c,t,a+.6,q+.3,'dinh','sq',xm=1150,y=840,s=.52,push=1,seed=26,pre='t22n_')
    if t>q: di(cv,c,'t22n_bachho',2200,885,1350,885,t,q,q+(b-q)*.7,s=.64,bob=2,f=3,lat=True,r=-10*inn(t,q+(b-q)*.7,.4))
    for k in range(2): dust(cv,c,850+k*150,880,o=.3*(1-inn(t,q,.5)),s=.4)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'đánh các người cầm quân khác, trận nào cũng thắng',960,200,t,a+.3,q-.2,col=RED,sz=38)
    lb(cv,C0,'Phạm Bạch Hổ ở Đằng Châu tự đến xin hàng',960,200,t,q+.1,b,col=SQC,sz=40)
# ===== 27: Trần Lãm mất; quân họ Ngô thua ở Ô Man
def S_27(cv,t):
    a,b=T[27]-.3,E[27]+.3;q=sb(27,1);q2=sb(27,2)
    c=kc(t,[(a,(900,560,1.04)),(b,(1150,560,1.0))])
    ngoai(cv,c,t,g=880,seed=27,mist=.4)
    put(cv,c,'t22x_oman',960,560,s=1.0)
    mau(cv)
    if t<q+.3: nv(cv,c,'t22n_tranlam',1500,885,t,s=.62,o=1-inn(t,a+.6,1.0),flip=True);gach(cv,c,1500,360,t,a+.7,160)
    if t>q:
        back=inn(t,q2,1.0)
        for i in range(2):
            x=-500+i*-300+1300*inn(t,q,q2-q)-1500*back
            di(cv,c,'t22n_ngo',x,890+i*8,x,890+i*8,t,a,b,s=.48,bob=4,f=5+i*.4,ph=i,lat=back>0)
        di(cv,c,'t22n_dan',2200,885,1200,885,t,q2-.6,q2+.6,s=.56,bob=4,f=6)
        di(cv,c,'t22n_dan2',2500,885,1450,885,t,q2-.4,q2+.8,s=.54,bob=4,f=6.3,lat=True)
        if q2-.2<t<q2+1.2: sparks(cv,c,t,[(1180+30*k,800-20*k) for k in range(3)],q2-.2,q2+1.2,seed=27)
    bui(cv,t)
    truoc(cv,c,t,r=False)
    lb(cv,c,'Trần Lãm',1500,330,t,a+.3,q,col=RED,sz=32)
    lb(cv,C0,'Trần Lãm qua đời',960,200,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'hơn năm trăm con em họ Ngô ở Đỗ Động Giang kéo đến',960,200,t,q+.1,q2-.2,col=NGOC,sz=36)
    lb(cv,C0,'vừa vào đất Ô Man, bị người trong làng đánh bại',960,200,t,q2+.1,b,col=RED,sz=38)
# ===== 28: tiến vào Đỗ Động Giang; các nơi xin hàng; nhà Ngô chấm dứt
def S_28(cv,t):
    a,b=T[28]-.3,E[28]+.3;q=sb(28,1)
    c=kc(t,[(a,(800,560,1.04)),(b,(1100,560,1.0))])
    ngoai(cv,c,t,g=880,seed=28,mist=.4)
    put(cv,c,'t22x_dodong',960,560,s=1.0)
    mau(cv)
    x,_=di(cv,c,'t22n_dbl',-200,885,900,885,t,a+.2,q,s=.66,bob=4,f=5)
    di(cv,c,'t22n_dinh',-900,890,500,890,t,a+.2,q,s=.5,bob=4,f=5.4,ph=1)
    di(cv,c,'t22n_dinh',-1500,900,-50,900,t,a+.4,q+.2,s=.48,bob=4,f=5.7,ph=2)
    for i in range(3): nv(cv,c,'t22n_dan' if i%2==0 else 't22n_dan2',1350+i*170,885,t,s=.54,r=-14*inn(t,q-.6+i*.15,.5),flip=True)
    smoke(cv,c,1700,600,t,.4)
    seal(cv,'s967',1650,330,q+.2,t,s=.75,r=4)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'tiến thẳng vào Đỗ Động Giang, các nơi xin hàng',960,200,t,a+.3,q-.2,col=RED,sz=38)
    lb(cv,C0,'nhà Ngô đến đây chấm dứt',960,200,t,q+.1,b,col=NGOC,sz=44)
# ===== 29: cuộn lời bàn Lê Văn Hưu: chỉ một câu; chỗ trống
def S_29(cv,t):
    a,b=T[29]-.3,E[29]+.3;q=sb(29,1)
    c=kc(t,[(a,(960,560,1.04)),(b,(960,540,1.0))])
    ngoai(cv,c,t,g=880,seed=29,mist=.5,far=.6,midv=.5)
    mau(cv)
    for i in range(2): smoke(cv,c,350+i*1200,680,t+i,.35)
    flock(cv,c,t,.35)
    bui(cv,t)
    if not FREEZE: ink_wash(cv,.2)
    cuon(cv,760,500,t,'LỜI BÀN LÊ VĂN HƯU','ra quân một lần,|mười hai sứ quân|đều phục',col=RED,s=.62,sz=34,u=inn(t,a+.6,1.0))
    if t>q and not FREEZE:
        for k in range(4):
            put_screen(cv,text('?',60,INK,700),1350+k*110,420+40*math.sin(t*1.5+k),inn(t,q+k*.4,.4)*.8)
    lb(cv,C0,'Lê Văn Hưu, sử gia thời nhà Trần',960,200,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'không trận nào được chép lại',960,200,t,q+.1,b,col=RED,sz=42)
# ===== 30: ba việc chắc chắn (bộ đếm ba ô)
def S_30(cv,t):
    a,b=T[30]-.3,E[30]+.3;q=sb(30,1);q2=sb(30,2);q3=sb(30,3);q4=sb(30,4)
    c=kc(t,[(a,(960,560,1.06)),(b,(960,540,1.0))])
    ngoai(cv,c,t,g=880,seed=30,mist=.4,far=.8,midv=.7)
    mau(cv)
    if t>q: nv(cv,c,'t22n_tranlam',380,885,t,s=.56,o=inn(t,q,.5))
    if t>q: nv(cv,c,'t22n_dbl',600,885,t,s=.56,flip=True,o=inn(t,q,.5))
    if t>q2: nv(cv,c,'t22n_bachho',960,885,t,s=.56,r=-10,flip=True,o=inn(t,q2,.5))
    if t>q3: di(cv,c,'t22n_ngo',1300,890,2400,890,t,q3,b+1,s=.46,bob=3,f=4.6)
    for i in range(2): smoke(cv,c,1500+i*250,620,t+i,.35)
    bui(cv,t)
    truoc(cv,c,t)
    if not FREEZE: o_dem(cv,1500,300,(t>q)+(t>q2)+(t>q3),3,'ba việc chắc chắn',t)
    lb(cv,C0,'những gì chắc chắn chỉ có ba việc',760,200,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'lớn mạnh từng bước, không nhờ một trận lớn',760,200,t,q4+.1,b,col=RED,sz=38)
# ===== 31: hai cha con cưỡi ngựa ra trận (sử nhà Tống)
def S_31(cv,t):
    a,b=T[31]-.3,E[31]+.3;q=sb(31,1)
    c=kc(t,[(a,(800,560,1.04)),(b,(1150,560,1.0))])
    ngoai(cv,c,t,g=880,seed=31,mist=.35,far=.9,midv=.8)
    mau(cv)
    u=inn(t,a+.2,b-a)
    put(cv,c,'t22n_ngua',-200+1400*u,900,s=.62,ay=1,scale_px=3,r=2*math.sin(t*9))
    put(cv,c,'t22n_ngua',-450+1400*u,910,s=.56,ay=1,scale_px=3,r=2*math.sin(t*9+1))
    di(cv,c,'t22n_dinh',-1100,890,300,890,t,a+.2,b,s=.48,bob=4,f=6)
    for k in range(3): dust(cv,c,-300+1400*u-k*120,890,o=.25,s=.35)
    flock(cv,c,t,.4)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'sử nhà Tống: hai cha con cùng đánh bại các đối thủ',960,200,t,a+.3,q-.2,col=INK,sz=38)
    lb(cv,C0,'người con trên ngọn sào nay ra trận cùng cha',960,200,t,q+.1,b,col=RED,sz=40)
# ===== 32: năm 968 lên ngôi hoàng đế, quốc hiệu Đại Cồ Việt
def S_32(cv,t):
    a,b=T[32]-.3,E[32]+.3
    c=kc(t,[(a,(960,600,1.0)),(b,(960,540,1.1))])
    put(cv,c,'t22_far',960,760,ay=1,k=.35,o=.3)
    put(cv,c,'t22x_dien',960,610,s=.85)
    suong(cv,c,t,700,.25,32)
    mau(cv)
    if not FREEZE:
        X,Y=c.p(960,520);put_screen(cv,band(360,520,GOLDC,.22*(.7+.3*math.sin(t*2.5)),70),X,Y,inn(t,a+.6,.8))
    nv(cv,c,'t22n_dblvua',960,885,t,s=.72)
    di(cv,c,'t22n_dinh',-700,890,300,890,t,a,b,s=.46,bob=2,f=3)
    di(cv,c,'t22n_dinh',2600,890,1620,890,t,a,b,s=.46,bob=2,f=3.2,lat=True)
    seal(cv,'s968',1650,330,a+.5,t,s=.8,r=4)
    for i in range(2): smoke(cv,c,500+i*900,620,t+i,.3)
    bui(cv,t)
    truoc(cv,c,t,o=.9)
    if not FREEZE:
        tx=text('ĐẠI CỒ VIỆT',74,RED,700,glow=5);put_screen(cv,wipe(tx,inn(t,a+(b-a)*.55,1.2),0,.3,seed=32),960,200)
# ===== 33: Đàm thôn chật, khó phòng giữ -> đắp thành, đào hào ở Hoa Lư
def S_33(cv,t):
    a,b=T[33]-.3,E[33]+.3;q=sb(33,1);q2=sb(33,2)
    c=kc(t,[(a,(1200,560,1.04)),(q,(1000,560,1.0)),(b,(960,540,1.05))])
    ngoai(cv,c,t,g=880,seed=33,mist=.4,far=.6,midv=.5)
    sw=inn(t,q-.4,1.0)
    put(cv,c,'t22x_damthon',960,560,s=1.0,o=1-sw)
    if sw>0:
        im=A('t22x_xay');put(cv,c,im,960,560,s=1.0,o=sw)
    mau(cv)
    if t<q: nv(cv,c,'t22n_dblvua',600,885,t,s=.62)
    if t>q2-.3:
        for i in range(3): di(cv,c,'t22n_dan' if i%2 else 't22n_dan2',300+i*500,885,520+i*500,885,t,q2,b,s=.5,bob=4,f=5+i*.3,ph=i)
        dust(cv,c,900,870,o=.3,s=.4);dust(cv,c,1400,870,o=.25,s=.4)
    bui(cv,t)
    truoc(cv,c,t)
    if not FREEZE and t<q+.5: stroke(cv,c,[(700,480),(1700,700)],inn(t,a+(q-a)*.6,.6),wid=10,col=RED,o=.8*(1-inn(t,q,.5)),head=False)
    lb(cv,C0,'Đàm thôn: đất chật hẹp, khó phòng giữ',960,200,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'ông vẫn đóng đô ở Hoa Lư',960,200,t,q+.1,q2-.2,col=RED,sz=44)
    lb(cv,C0,'đắp thành, đào hào, xây cung điện',960,200,t,q2+.1,b,col=INK,sz=42)
# ===== 34: kinh đô Hoa Lư giữa vòng núi đá (gọi lại cảnh mở đầu)
def S_34(cv,t):
    a,b=T[34]-.3,E[34]+.3;q=sb(34,1)
    c=kc(t,[(a,(1180,540,1.0)),(b,(1180,520,1.1))])
    ngoai(cv,c,t,g=880,seed=34,mist=.45,far=.75,midv=.55)
    put(cv,c,'t22x_kinh',960,560,s=1.0)
    mau(cv)
    for i in range(2): smoke(cv,c,1050+i*300,600,t+i,.3)
    di(cv,c,'t22n_dinh',300,890,900,890,t,a,b,s=.46,bob=2,f=3)
    di(cv,c,'t22n_dan',2300,890,1700,890,t,a,b,s=.48,bob=2,f=3.2,lat=True)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'Hoa Lư, nay thuộc tỉnh Ninh Bình',960,200,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'thung lũng che chở ông năm xưa, nay thành kinh đô',960,200,t,q+.1,b,col=RED,sz=38)
# ===== 35: kết: ngọn sào mờ dần thành kinh đô; tựa
def S_35(cv,t):
    a=T[35]-.3;b=E[35]+4;q=sb(35,1);q2=sb(35,2)
    c=kc(t,[(a,(900,560,1.06)),(b,(1000,520,1.0))])
    ngoai(cv,c,t,g=880,seed=35,mist=.6)
    put(cv,c,'t22x_cuoi',960,560,s=1.0)
    mau(cv)
    put(cv,c,'t22_saomo',560,900,s=.7,ax=.5,ay=1,o=.8*(1-inn(t,q,2.0)),r=1.2*math.sin(t),scale_px=1.5)
    di(cv,c,'t22n_dan',1950,890,1450,890,t,a,b,s=.5,bob=2,f=3.2,lat=True)
    di(cv,c,'t22n_dan2',2200,890,1730,890,t,a,b,s=.48,bob=2,f=3.4,lat=True)
    smoke(cv,c,1350,620,t,.4)
    flock(cv,c,t,.5)
    bui(cv,t)
    truoc(cv,c,t)
    lb(cv,C0,'một câu cho cả cuộc dẹp loạn',960,200,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'từ ngọn sào đến ngai vàng: hơn mười năm',960,200,t,q+.1,q2-.1,col=RED,sz=40)
    if not FREEZE and t>q2:
        tx=text('Đinh Bộ Lĩnh và Hoa Lư, năm 944–968',54,INK,700);put_screen(cv,wipe(tx,inn(t,q2,1.4),0,.3,seed=22),W/2,150)
        put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,220,inn(t,E[35]+.6,1))
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
    flock=lambda *a,**k:None
S=lambda n:T[n]-.3
NS=35
SH=[(0 if n==1 else S(n),S(n+1) if n<NS else V.TOTAL+1,globals()[f'S_{n}']) for n in range(1,NS+1)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm22_full.json'))
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
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'ĐINH BỘ LĨNH VÀ HOA LƯ','stitle22',.55)
    if not NOCAP: caps(cv,t)
V.NHAN={7:'Đinh Bộ Lĩnh – người giữ Hoa Lư',9:'Đinh Liễn – con trai Đinh Bộ Lĩnh',24:'Trần Lãm – sứ quân giữ Bố Hải Khẩu'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
