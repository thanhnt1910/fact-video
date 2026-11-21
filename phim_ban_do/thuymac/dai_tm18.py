# Bản dài tm18: Mai Thúc Loan, năm 722 (bản 1.2). Khung: hai cách gọi một con người (vua Đen / tướng giặc → châu dân).
# Cách dựng mới: mở đầu giọt mực loang; hình ảnh lặp lại = cuộn sử có hai chữ (tướng giặc ở đoạn 2, 3, 19, đổi thành châu dân ở đoạn 25);
# chia đôi màn hình (đoạn 2, 8, 12, 18); bộ đếm (32 châu, 10 vạn, 12 trên 32); con đường cũ của Mã Viện (nối tm13); quét mực khi quân Đường xuất hiện.
# Quy ước màu: quân Mai Thúc Loan đỏ son, quân nhà Đường xanh chàm đội mũ trụ; chuyện dân gian phủ màu nâu nhạt và khung nét đứt.
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
V=K.setup('tm18',{4:4.0})
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
    put(cv,c,'t18_far',960+seed*60,g-120,ay=1,k=.35,o=far)
    put(cv,c,'t18_mid',960-seed*40,g+30,ay=1,k=.62,o=midv)
    suong(cv,c,t,g-260,mist,seed)
def truoc(cv,c,t,o=1):
    put(cv,c,'t18_frontL',-120,1120,ax=0,ay=1,k=1.3,s=.85,r=1.2*math.sin(t*.8),o=o)
    put(cv,c,'t18_frontR',2040,1120,ax=1,ay=1,k=1.3,s=.8,r=1.2*math.sin(t*.7+1),o=o)
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
        rg=np.random.default_rng(18);a=rg.random((34,60)).astype(np.float32)
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
NAU=np.array((.55,.42,.27),np.float32)
PT=json.load(open('/tmp/gen/bd/a/map_trung_pts.json'))
def mapbg_trung(cv,cam,u=1.0,o=1.0):
    im=A('map_trung')
    if u<1: im=wipe(im,u,0,.25,seed=4)
    put(cv,cam,im,960,540,o=o,scale_px=1.5)
def cuon(cv,x,y,t,tieu,chu,col=None,o=1.0,s=.62,sz=60,u=1.0,gach=0.0,thay=None,uthay=0.0):
    """hình ảnh lặp lại: cuộn sử có hai chữ; gach>0 thì gạch chéo, thay = hai chữ mới viết đè"""
    put(cv,C0,'t18_cuon',x,y,s=s,o=o,r=.5*math.sin(t*.7+x))
    if FREEZE: return
    put_screen(cv,text(tieu,30,INK,700),x,y-170*s/.62,o)
    put_screen(cv,wipe(text(chu,sz,col if col is not None else RED,700),u,0,.25,seed=int(x)),x,y,o*(1-.6*uthay))
    if gach>0: stroke(cv,C0,[(x-150*s/.62,y+10),(x+150*s/.62,y-20)],gach,wid=10,col=RED,o=.9*o,head=False)
    if thay and uthay>0: put_screen(cv,wipe(text(thay,sz+6,INK,700),uthay,0,.25,seed=7),x,y+110*s/.62,o)
def dangian(cv,o):
    """chuyện dân gian: phủ nâu nhạt và khung nét đứt"""
    if FREEZE or o<=0: return
    ink_wash(cv,.18*o,col=NAU)
    for k in range(18):
        x0=60+k*100;stroke(cv,C0,[(x0,60),(x0+60,60)],1,wid=5,col=NAU,o=.8*o,head=False);stroke(cv,C0,[(x0,1020),(x0+60,1020)],1,wid=5,col=NAU,o=.8*o,head=False)
    put_screen(cv,band(330,70,PAPER,.85,14),300,130,o);put_screen(cv,text('dân gian kể',36,(.45,.3,.15),700),300,128,o)
def dot_dem(cv,x,y,n,tong,cot=8,col=RED,o=1.0,sz=34,gap=46):
    for k in range(tong):
        xx=x+(k%cot)*gap;yy=y+(k//cot)*gap;on=k<n
        dot(cv,C0,xx,yy,o=o*(.95 if on else .25),col=col if on else INK,r=int(sz*.45))
def canh_lang(cv,t,a,b,keys=None):
    c=kc(t,keys or [(a,(960,600,1.0)),(b,(960,560,1.12))])
    ngoai(cv,c,t,g=880,seed=1,mist=.4)
    put(cv,c,'t18x_lang',960,560,s=1.0)
    di(cv,c,'t18_spr_mtl',-200,880,560,880,t,a+.4,b+1,s=.62,bob=3,f=3.4)
    di(cv,c,'t18_spr_dan',2300,890,1500,890,t,a,b+2,s=.55,bob=2,f=3.6,lat=True)
    di(cv,c,'t18_spr_phu',2600,885,1800,885,t,a+.6,b+2,s=.6,bob=3,f=4,lat=True)
    truoc(cv,c,t)
    return c
# ---- 1: giọt mực loang thành làng ven biển Hoan Châu
def S_1(cv,t):
    a,b=0,E[1]+.3;td=.95
    sc=PAP.copy();canh_lang(sc,t,a,b)
    if FREEZE: cv[:]=sc;return
    if t<td:
        y=-40+(540+40)*(t/td)**2
        m=loang(960,y,22,6);cv[:]=cv*(1-m)+np.array(INK,np.float32)*m
    else:
        u=inn(t,td,1.6);r=30+u*1300
        m=loang(960,540,r,60);rim=np.clip(loang(960,540,r,60)-loang(960,540,r-70,60),0,1)
        cv[:]=cv*(1-m)+sc*m;cv[:]=cv*(1-rim*.75)+np.array(INK,np.float32)*rim*.75
    big(cv,'VUA ĐEN HAY TƯỚNG GIẶC?',t,1.6,b,RED,120,80,seed=1)
# ---- 2: hai cuộn sử chia đôi màn hình
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3;q=sb(2,1)
    canh_lang(cv,t,a-6,b+3);ink_wash(cv,.5)
    cuon(cv,560,560,t,'NGƯỜI CÙNG QUÊ','vua Đen',col=INK,u=inn(t,a+.2,.8))
    cuon(cv,1360,560,t,'BỘ SỬ NHÀ LÊ','tướng giặc',u=inn(t,a+1.2,.8))
    if not FREEZE and t>q: put_screen(cv,band(760,80,PAPER,.9,14),960,200,inn(t,q,.4));put_screen(cv,text('gần 300 năm sau, có người viết lại',38,RED,700),960,198,inn(t,q,.4))
    lb(cv,C0,'cùng một người: Mai Thúc Loan',960,120,t,a+.4,q-.2,col=INK,sz=40)
# ---- 3: câu hỏi: hai chữ nào thay vào?
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3
    c=kc(t,[(a,(960,560,1.0)),(b,(1060,560,1.1))])
    ngoai(cv,c,t,g=880,seed=3,mist=.6,far=.6,midv=.6)
    di(cv,c,'t18_spr_suga',-300,880,300,880,t,a,b,s=.6,bob=1,f=1.5,lac=.4)
    di(cv,c,'t18_spr_dan',2300,890,1700,890,t,a,b,s=.5,bob=2,f=3.4,lat=True)
    di(cv,c,'t18_spr_phu',2600,885,1900,885,t,a,b,s=.5,bob=3,f=4,lat=True)
    truoc(cv,c,t)
    cuon(cv,1060,540,t,'BỘ SỬ NHÀ LÊ','tướng giặc',s=.7,sz=64,gach=inn(t,a+.6,.6))
    if not FREEZE: put_screen(cv,text('? ?',90,RED,700),1060,700,inn(t,a+1.2,.5)*(.85+.15*math.sin(t*3)))
# ---- 4: bản đồ: nước ta dưới nhà Đường, chia thành châu; Hoan Châu
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3;q=sb(4,1)
    dl,ng,th=PT['daila'],PT['hoanchau'],PT['aichau']
    c=mcam(t,[(a,(820,400,1.2)),(q,(800,480,1.1)),(b,(780,600,1.25))])
    mapbg_trung(cv,c,u=inn(t,a-.2,1.0))
    for nm,p,t0 in (('nơi đóng của quan nhà Đường',dl,a+.6),('Ái Châu',th,a+1.2),('Hoan Châu',ng,q)):
        if t>t0: dot(cv,c,*p,o=inn(t,t0,.3),col=RED if nm=='Hoan Châu' else INK);tag(cv,c,p[0]+22,p[1]-6,nm,dy=0,sz=26)
    if t>q: pulse(cv,c,*ng,t);stroke(cv,c,[dl,th,ng],inn(t,q,1.5),wid=4,col=INK,o=.5,head=False)
    di(cv,c,'t18_spr_1duong',dl[0]+40,dl[1]+10,dl[0]+80,dl[1]+10,t,a,b,s=.18,bob=1,f=3,k=1.01)
    di(cv,c,'t18_spr_mtl',ng[0]-30,ng[1]+20,ng[0]+10,ng[1]+20,t,q,b,s=.2,bob=1,f=3,k=1.01)
    for i in range(2): di(cv,c,'t18_spr_1duong',dl[0]-120+i*60,dl[1]+60,dl[0]+40+i*60,dl[1]+120,t,a+i*.5,b,s=.15,bob=1,f=4,ph=i,k=1.01)
    di(cv,c,'t18_spr_phu',th[0]+80,th[1]-40,ng[0]+60,ng[1]-30,t,a,b,s=.16,bob=1,f=4,k=1.01)
    lb(cv,C0,'nước ta dưới sự cai trị của nhà Đường',960,150,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'Hoan Châu: Nghệ An, Hà Tĩnh bây giờ',960,150,t,q+.2,b,col=RED,sz=40)
def pulse(cv,c,x,y,t,col=RED):
    for k in range(2):
        u=((t*.6+k*.5)%1.0);dot(cv,c,x,y,o=.6*(1-u),col=col,r=int(8+40*u))
# ---- 5: làng Mai Phụ, nước da rất đen
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3;q=sb(5,1)
    c=kc(t,[(a,(800,600,1.05)),(q,(900,560,1.2)),(b,(940,520,1.35))])
    put(cv,c,'t18_far',960,560,ay=1,k=.35,o=.8)
    river(cv,c,t,PAP,wl=640,stakes=False,cliffs=False,reeds=1,mist=.6,ridge_o=.3)
    put(cv,c,'t18_mid',960,700,ay=1,k=.62,o=.7)
    di(cv,c,'t18_spr_mtl',300,880,940,880,t,a,q+.6,s=.75,bob=3,f=3.2)
    di(cv,c,'t18_spr_dan',-400,890,300,890,t,a,b,s=.5,bob=2,f=3.4)
    di(cv,c,'t18_spr_phu',2200,885,1500,885,t,a+.4,b,s=.55,bob=3,f=4,lat=True)
    truoc(cv,c,t)
    lb(cv,C0,'làng Mai Phụ, Hà Tĩnh',960,170,t,a+.3,q-.2,col=INK,sz=44)
    lb(cv,C0,'sử chỉ ghi: nước da rất đen',960,170,t,q+.2,b,col=RED,sz=44)
# ---- 6: người trong vùng gọi ông là vua Đen
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3;q=sb(6,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,520,1.16))])
    ngoai(cv,c,t,g=880,seed=6)
    put(cv,c,'t18x_dancu',960,560,s=1.1)
    for i in range(3): di(cv,c,'t18_spr_dan',-400-i*260,890,250+i*120,890,t,a+i*.4,b,s=.5,bob=2,f=3.4+i*.3,ph=i)
    di(cv,c,'t18_spr_phu',2300,885,1600,885,t,a+.3,b,s=.55,bob=3,f=4,lat=True)
    truoc(cv,c,t)
    if not FREEZE: put_screen(cv,band(420,120,PAPER,.88,20),1500,330,inn(t,a+.6,.4));put_screen(cv,text('HẮC ĐẾ',60,INK,700),1500,315,inn(t,a+.6,.4));put_screen(cv,text('vua Đen',34,RED,700),1500,365,inn(t,a+1.2,.4))
    lb(cv,C0,'người Hoan Châu đặt tên, không vua nào ban',960,170,t,q+.2,b,col=RED,sz=40)
# ---- 7: dân gian kể chuyện gánh vải (phủ nâu, khung nét đứt)
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3;q=sb(7,1)
    c=kc(t,[(a,(1300,560,1.05)),(b,(900,560,1.0))])
    ngoai(cv,c,t,g=880,seed=7,mist=.5,far=.7,midv=.6)
    put(cv,c,'t18x_ganhvai',960,560,s=1.0)
    for i in range(5): di(cv,c,'t18_spr_phu',2600+i*220,880-(i%2)*14,600+i*260,880-(i%2)*14,t,a-1+i*.5,b+3,s=.6,bob=4,f=4+i*.2,ph=i,lat=True)
    truoc(cv,c,t)
    dangian(cv,inn(t,q-.3,.6))
    lb(cv,C0,'sử cũ không nói vì sao ông đứng lên',960,250,t,a+.3,q-.4,col=INK,sz=40)
# ---- 8: chuyện ấy chỉ là dân gian (chia đôi: sử nhà Đường / Phan Huy Lê)
def S_8(cv,t):
    a,b=T[8]-.3,E[8]+.3;q=sb(8,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(960,560,1.05))])
    ngoai(cv,c,t,g=880,seed=8,mist=.6)
    for i in range(3): di(cv,c,'t18_spr_phu',1900+i*240,885,800+i*240,885,t,a+i*.4,b+2,s=.55,bob=3,f=4,ph=i,lat=True,o=.6)
    di(cv,c,'t18_spr_dan',-300,890,400,890,t,a,b,s=.5,bob=2,f=3.4)
    truoc(cv,c,t)
    dangian(cv,1-inn(t,a+.2,.8))
    if not FREEZE:
        ink_wash(cv,.3)
        for x,tt,ln,t0 in ((560,'SỬ NHÀ ĐƯỜNG','không ghi lệ nộp vải',a+.4),(1360,'NHÀ SỬ HỌC PHAN HUY LÊ','cảnh nộp của, đi làm không công',q)):
            if t>t0:
                u=inn(t,t0,.4);put_screen(cv,band(680,200,PAPER,.9,20),x,450,u)
                put_screen(cv,text(tt,30,RED,700),x,400,u);put_screen(cv,wipe(text(ln,36,INK,700),inn(t,t0+.2,.7),0,.25,seed=int(x)),x,470,1)
# ---- 9: mùa thu năm 722, chiếm Hoan Châu, tự lên làm vua (ánh thu)
def S_9(cv,t):
    a,b=T[9]-.3,E[9]+.3;q=sb(9,1)
    c=kc(t,[(a,(960,600,1.0)),(b,(960,520,1.16))])
    ngoai(cv,c,t,g=880,seed=9)
    put(cv,c,'t18x_xungde',960,560,s=1.1)
    for i in range(3): di(cv,c,'t18_spr_ta',-900-i*200,880+i*24,-150+i*200,880+i*24,t,a+i*.4,b,s=.5,bob=4,f=5.4+i*.3,ph=i)
    di(cv,c,'t18_spr_coda',2300,880,1450,880,t,a+.3,b,s=.6,bob=4,f=5,lat=True)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.1,col=np.array((.75,.5,.2),np.float32))
    seal(cv,'s722',1560,330,a+.6,t,s=.8,r=4)
    lb(cv,C0,'mùa thu năm 722',960,170,t,a+.3,q-.2,col=INK,sz=46)
    lb(cv,C0,'chiếm lấy Hoan Châu, tự lên làm vua',960,170,t,q+.2,b,col=RED,sz=44)
# ---- 10: bắt tay Lâm Ấp, Chân Lạp; ba mươi hai châu (bản đồ, bộ đếm)
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3;q=sb(10,1)
    ng=PT['hoanchau']
    c=mcam(t,[(a,(780,640,1.3)),(b,(820,700,1.05))])
    mapbg_trung(cv,c,u=inn(t,a-.2,1.0))
    dot(cv,c,*ng,col=RED);tag(cv,c,ng[0]+22,ng[1]-6,'Hoan Châu',dy=0,sz=26);pulse(cv,c,*ng,t)
    for nm,p,t0 in (('Lâm Ấp',(PT['lamap'][0],880),a+.6),('Chân Lạp',(PT['chanlap'][0]+60,880),a+1.6)):
        if t>t0: tag(cv,c,p[0]+20,p[1]-6,nm,dy=0,sz=26);stroke(cv,c,[p,ng],inn(t,t0,1.2),wid=5,col=RED,o=.7)
        u=inn(t,t0,1.4);put(cv,c,'t18_spr_coda',p[0]+(ng[0]-p[0])*u,p[1]+(ng[1]-p[1])*u,s=.2,ay=1,o=inn(t,t0,.3),r=3*math.sin(t*3+t0))
    di(cv,c,'t18_spr_mtl',ng[0]-30,ng[1]+20,ng[0]+10,ng[1]+20,t,a,b,s=.2,bob=1,f=3,k=1.01)
    if not FREEZE and t>q:
        n=int(32*inn(t,q,2.4));put_screen(cv,band(440,260,PAPER,.85,20),1400,410,inn(t,q,.3));dot_dem(cv,1240,350,n,32,cot=8)
        put_screen(cv,text(f'{n} châu',56,RED,700),1400,290,inn(t,q,.3))
    lb(cv,C0,'Lâm Ấp: miền Trung · Chân Lạp: Campuchia bây giờ',960,140,t,a+.6,q-.2,col=INK,sz=36)
    lb(cv,C0,'sử nhà Đường: ba mươi hai châu theo ông',960,140,t,q+.2,b,col=RED,sz=38)
# ---- 11: chiếm thành của viên quan đứng đầu bộ máy cai trị
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3
    c=kc(t,[(a,(960,420,1.2)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=900,seed=11)
    put(cv,c,'t18x_phuthanh',960,520,s=.95)
    for r in range(2): di(cv,c,'t18_spr_ta',-900-r*250,880+r*30,500-r*200,880+r*30,t,a+r*.3,b+1,s=.55,bob=5,f=6.4+r*.4,ph=r)
    di(cv,c,'t18_spr_1duong',1300,880,2400,860,t,a+1,b+1,s=.6,bob=6,f=8,lac=2)
    for x in (700,1220): smoke(cv,c,x,330,t,1.0)
    truoc(cv,c,t)
    lb(cv,C0,'theo sử nhà Đường: chiếm được thành của quan nhà Đường',960,170,t,a+.4,b,col=RED,sz=36)
# ---- 12: ba mươi vạn hay bốn mươi vạn (chia đôi, bộ đếm)
def S_12(cv,t):
    a,b=T[12]-.3,E[12]+.3;q=sb(12,1)
    c=kc(t,[(a,(1200,560,1.05)),(b,(760,560,1.0))])
    ngoai(cv,c,t,g=880,seed=12,mist=.4)
    put(cv,c,'t18x_quanta',960,620,s=1.0,o=.8)
    for r in range(2): di(cv,c,'t18_spr_ta',2600+r*200,890+r*28,1500+r*160,890+r*28,t,a+r*.3,b+1,s=.5,bob=4,f=5.6+r*.4,ph=r,lat=True)
    truoc(cv,c,t)
    if not FREEZE:
        for x,tt,n,t0,col in ((560,'BỘ SỬ NHÀ LÊ',300000,a+.4,INK),(1360,'SỬ NHÀ ĐƯỜNG',400000,q,RED)):
            if t>t0:
                u=inn(t,t0,.4);put_screen(cv,band(600,170,PAPER,.9,20),x,300,u)
                put_screen(cv,text(tt,30,RED,700),x,260,u);put_screen(cv,text(f'{int(n*inn(t,t0,1.6)):,}'.replace(',','.')+' quân',52,col,700),x,325,u)
# ---- 13: vua Đường sai Dương Tư Húc
def S_13(cv,t):
    a,b=T[13]-.3,E[13]+.3;q=sb(13,1)
    c=kc(t,[(a,(960,520,1.15)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=13,far=.5,midv=.5)
    put(cv,c,'t18x_trieuduong',960,630,s=1.1)
    di(cv,c,'t18_spr_quan',-300,880,420,880,t,a,q+1,s=.6,bob=2,f=3)
    for i in range(2): di(cv,c,'t18_spr_1duong',2300+i*180,880,1600+i*140,880,t,a+i*.4,b,s=.6,bob=2,f=3.4,ph=i,lat=True)
    if t>q: di(cv,c,'t18_spr_tuhuc',2400,880,1300,880,t,q,b+1,s=.62,bob=5,f=7,lat=True)
    truoc(cv,c,t)
    lb(cv,C0,'tin về tới kinh đô nhà Đường',960,150,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'Dương Tư Húc, thái giám đã ngoài sáu mươi',960,150,t,q+.2,b,col=DUONGC,sz=40)
# ---- 14: gọi được mười vạn người ở Lĩnh Nam (bộ đếm)
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3;q=sb(14,1)
    c=kc(t,[(a,(1300,560,1.05)),(b,(800,560,1.0))])
    ngoai(cv,c,t,g=880,seed=14)
    put(cv,c,'t18x_moquan',960,560,s=1.0)
    for r in range(3): di(cv,c,'t18_spr_duong',-900-r*260,870+r*28,500-r*200,870+r*28,t,a+r*.4,b+2,s=.5+.04*r,bob=3,f=5+r*.4,ph=r)
    truoc(cv,c,t)
    if not FREEZE:
        n=int(100000*inn(t,a+.6,b-a-1.2));put_screen(cv,band(520,110,PAPER,.88,18),1460,330,inn(t,a+.4,.4))
        put_screen(cv,text(f'{n:,}'.replace(',','.')+' người',50,DUONGC,700),1460,330,inn(t,a+.4,.4))
    lb(cv,C0,'Lĩnh Nam: Quảng Đông, Quảng Tây bây giờ',960,150,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'con cháu người đứng đầu các vùng ấy',960,150,t,q+.2,b,col=INK,sz=40)
# ---- 15: con đường cũ của Mã Viện (bản đồ; bóng Mã Viện đi trước, Dương Tư Húc theo sau)
DUONG_CU=None
def S_15(cv,t):
    a,b=T[15]-.3,E[15]+.3;q=sb(15,1)
    lc,dl,th,ng=PT['liemchau'],PT['daila'],PT['aichau'],PT['hoanchau']
    pts=[lc,dl,th,ng]
    c=mcam(t,[(a,(1000,300,1.15)),(b,(800,560,1.1))])
    mapbg_trung(cv,c,u=inn(t,a-.2,1.0))
    for nm,p in (('Lĩnh Nam',lc),('Hoan Châu',ng)): dot(cv,c,*p,col=RED if nm=='Hoan Châu' else INK);tag(cv,c,p[0]+22,p[1]-6,nm,dy=0,sz=26)
    def theo(u):
        seg=min(int(u*3),2);v=u*3-seg;p,q2=pts[seg],pts[seg+1];return p[0]+(q2[0]-p[0])*v,p[1]+(q2[1]-p[1])*v
    for k in range(30):
        u0=k/30;x0,y0=theo(u0);x1,y1=theo(u0+1/60)
        if k/30<inn(t,a+.2,2.4): stroke(cv,c,[(x0,y0),(x1,y1)],1,wid=5,col=INK,o=.5,head=False)
    u=inn(t,a+.2,2.6);x,y=theo(min(u,.999));put(cv,c,'t18_spr_mavien',x,y,s=.28,ay=1,o=.55*(1-inn(t,q,1)),r=2*math.sin(t*6))
    if t>q-.3:
        u=inn(t,q,b-q);x,y=theo(min(u,.999));put(cv,c,'t18_spr_tuhuc',x,y,s=.28,ay=1,r=2*math.sin(t*7))
        put(cv,c,'t18_spr_duong',x-60,y+30,s=.16,ay=1,r=1.5*math.sin(t*6))
    pulse(cv,c,*ng,t)
    di(cv,c,'t18_spr_mtl',ng[0]-20,ng[1]+20,ng[0]+20,ng[1]+20,t,a,b,s=.2,bob=1,f=3,k=1.01)
    for i in range(2): di(cv,c,'t18_spr_ta',ng[0]-80+i*60,ng[1]+60,ng[0]-40+i*60,ng[1]+60,t,a,b,s=.12,bob=1,f=4,ph=i,k=1.01)
    lb(cv,C0,'đường Mã Viện đã đi, gần bảy trăm năm trước',960,150,t,a+.4,q-.2,col=INK,sz=40)
    lb(cv,C0,'quân nhà Đường đi lại đúng con đường ấy',960,150,t,q+.2,b,col=DUONGC,sz=40)
# ---- 16: quân nhà Đường hiện ra trong sương (quét mực từ bản đồ)
def batngo(cv,t,a,b):
    c=kc(t,[(a,(960,600,1.0)),(b,(1000,560,1.12))])
    put(cv,c,'t18_far',960,560,ay=1,k=.35,o=.7)
    put(cv,c,'t18x_batngo',960,560,s=1.0)
    for r in range(3): di(cv,c,'t18_spr_duong',960+r*60,640+r*40,960-200+r*80,840+r*30,t,a+r*.5,b+1,s=.45+.08*r,bob=3,f=5+r*.4,ph=r,o=inn(t,a+r*.5,1.2))
    di(cv,c,'t18_spr_tuhuc',1000,600,1060,760,t,a,b,s=.5,bob=4,f=6,o=inn(t,a,1.0),k=1.01)
    for k in range(4): put(cv,c,'mist',700+k*220+40*math.sin(t*.5+k),640+k*30,s=1.8,o=.55*(1-inn(t,a+.5,b-a)),k=1.0)
    di(cv,c,'t18_spr_1ta',-200,880,500,880,t,a,b,s=.6,bob=4,f=5)
    truoc(cv,c,t)
    return c
def S_16(cv,t):
    a,b=T[16]-.3,E[16]+.3;q=sb(16,1)
    if t<a+1.0 and not FREEZE:
        A_=PAP.copy();S_15(A_,t);B_=PAP.copy();batngo(B_,t,a,b)
        m=quet(inn(t,a-.1,1.0));cv[:]=A_*(1-m)+B_*m
    else: batngo(cv,t,a,b)
    lb(cv,C0,'kéo đến lúc bên ta không ngờ tới',960,170,t,a+.6,q-.2,col=INK,sz=42)
    lb(cv,C0,'sững sờ, không kịp nghĩ cách chống đỡ',960,170,t,q+.2,b,col=RED,sz=42)
# ---- 17: thua lớn (cảnh trọng tâm), rồi gò xác (lặng, xám)
def tran(cv,t,a,b):
    hit=a+1.2;sh=(6*math.sin(t*37)*(1-inn(t,hit+.4,.8))) if hit<t<hit+1.2 else 0
    c=kc(t,[(a,(900,560,1.05)),(b,(1100,560,1.1))],sh)
    ngoai(cv,c,t,g=880,seed=17,mist=.4)
    arrows(cv,c,t,a,hit+.6,[(300,700),(380,690)],[(1300,800),(1450,820)],n=10,h=110,per=.9,seed=6,col=DUONGC)
    clash(cv,c,t,hit-1,b+1,'duong','ta',xm=1000,y=790,s=.95,push=1,seed=17,pre='t18_spr_',ten=False)
    di(cv,c,'t18_spr_tuhuc',-200,860,260,860,t,a,hit,s=.7,bob=4,f=6)
    truoc(cv,c,t)
def go(cv,t,a,b):
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.08))])
    ngoai(cv,c,t,g=880,seed=18,mist=.8,far=.6,midv=.6)
    put(cv,c,'t18x_go',960,560,s=1.1)
    for i in range(3): di(cv,c,'t18_spr_duong',800+i*200,880+i*24,2600+i*200,880+i*24,t,a+i*.4,b+2,s=.5,bob=3,f=5,ph=i)
    flock(cv,c,t,.7)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3)
def S_17(cv,t):
    a,b=T[17]-.3,E[17]+.3;q=sb(17,1)
    if t<q-.3 or FREEZE: tran(cv,t,a,q+1)
    else:
        A_=PAP.copy();tran(A_,t,a,q+1);B_=PAP.copy();go(B_,t,q-.3,b)
        u=inn(t,q-.3,1.0);cv[:]=A_*(1-u)+B_*u
    lb(cv,C0,'quân của ông thua lớn',960,170,t,a+.3,q-.4,col=RED,sz=46)
# ---- 18: ông mất thế nào: hai cách ghi (chia đôi)
def S_18(cv,t):
    a,b=T[18]-.3,E[18]+.3;q=sb(18,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1100,520,1.1))])
    ngoai(cv,c,t,g=880,seed=19,mist=.6)
    put(cv,c,'t18x_hungson',960,560,s=1.0,o=.85)
    di(cv,c,'t18_spr_mtl2',700,880,1000,760,t,q,b+2,s=.45,bob=2,f=3,o=.6)
    di(cv,c,'t18_spr_dan',-300,890,400,890,t,a,b,s=.5,bob=2,f=3.4)
    di(cv,c,'t18_spr_1duong',2300,880,1700,880,t,a,b,s=.55,bob=2,f=3.2,lat=True)
    truoc(cv,c,t)
    if not FREEZE:
        for x,tt,ln,t0 in ((560,'MỘT BỘ SỬ NHÀ ĐƯỜNG','bị bắt, bị chém tại trận',q),(1360,'MỘT BỘ SÁCH TRIỀU NGUYỄN','rút về núi Hùng Sơn',q+(b-q)*.45)):
            if t>t0:
                u=inn(t,t0,.4);put_screen(cv,band(640,170,PAPER,.9,20),x,330,u)
                put_screen(cv,text(tt,28,RED,700),x,290,u);put_screen(cv,wipe(text(ln,36,INK,700),inn(t,t0+.2,.7),0,.25,seed=int(x)),x,355,1)
    lb(cv,C0,'các sách ghi không giống nhau',960,150,t,a+.3,q-.2,col=INK,sz=42)
# ---- 19: bộ sử nhà Lê ghi tướng giặc (cuộn sử, đóng dấu)
def S_19(cv,t):
    a,b=T[19]-.3,E[19]+.3
    c=kc(t,[(a,(960,560,1.0)),(b,(800,560,1.12))])
    ngoai(cv,c,t,g=880,seed=20,far=.5,midv=.5)
    put(cv,c,'t18x_sule',960,630,s=1.1)
    di(cv,c,'t18_spr_quan',2300,880,1650,880,t,a,b,s=.55,bob=2,f=3,lat=True)
    di(cv,c,'t18_spr_dan',-400,890,250,890,t,a,b,s=.5,bob=2,f=3.4)
    flick(cv,c,1350,480,t,.6)
    truoc(cv,c,t)
    cuon(cv,1440,470,t,'BỘ SỬ NHÀ LÊ','tướng giặc',s=.5,sz=52,u=inn(t,a+.6,.8))
    lb(cv,C0,'chỉ ghi: nhà Đường đánh tan được',960,150,t,a+.3,b,col=INK,sz=40)
# ---- 20: bốn mươi vạn có thật không? (sử triều Nguyễn)
def S_20(cv,t):
    a,b=T[20]-.3,E[20]+.3;q=sb(20,1)
    c=kc(t,[(a,(960,520,1.12)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=21,far=.5,midv=.5)
    put(cv,c,'t18x_nguyen',960,630,s=1.1)
    di(cv,c,'t18_spr_quan',-300,880,380,880,t,a,b,s=.55,bob=2,f=3)
    di(cv,c,'t18_spr_dan',2300,890,1650,890,t,a,b,s=.5,bob=2,f=3.4,lat=True)
    truoc(cv,c,t)
    if not FREEZE:
        sh=6*math.sin(t*20)*inn(t,q,.5);put_screen(cv,band(560,130,PAPER,.9,20),960+sh,270,inn(t,a+.3,.4))
        put_screen(cv,text('400.000 quân ?',62,RED,700),960+sh,270,inn(t,a+.3,.4))
    lb(cv,C0,'những người viết sử triều Nguyễn không tin',960,140,t,q+.2,b,col=INK,sz=40)
# ---- 21: mười hai châu, không phải ba mươi hai (bộ đếm)
def S_21(cv,t):
    a,b=T[21]-.3,E[21]+.3;q=sb(21,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1100,560,1.08))])
    ngoai(cv,c,t,g=880,seed=22,mist=.6)
    for i in range(2): di(cv,c,'t18_spr_1duong',600+i*200,880,800+i*200,880,t,a,b,s=.6,bob=1.5,f=1.6,ph=i,lac=.6)
    di(cv,c,'t18_spr_quan',2300,880,1500,880,t,q,b,s=.55,bob=2,f=3,lat=True)
    di(cv,c,'t18_spr_dan',-400,890,200,890,t,a,b,s=.5,bob=2,f=3.4)
    truoc(cv,c,t)
    if not FREEZE:
        ink_wash(cv,.25)
        n=12 if t<q else 12;dot_dem(cv,620,300,n,32,cot=8,o=inn(t,a+.3,.5))
        put_screen(cv,text('12 châu thật',44,RED,700),790,240,inn(t,a+.6,.4))
        put_screen(cv,text('32 châu theo sử nhà Đường',34,INK,700),790,500,inn(t,a+1.2,.4))
        if t>q: put_screen(cv,band(700,90,PAPER,.9,14),1400,330,inn(t,q,.4));put_screen(cv,text('nói quân ta đông lên để được thưởng',34,DUONGC,700),1400,330,inn(t,q,.4))
    lb(cv,C0,'nhà Đường chỉ chia nước ta thành mười hai châu',960,150,t,a+.3,q-.2,col=INK,sz=40)
# ---- 22: điều chắc chắn: một người dám tự lên làm vua
def S_22(cv,t):
    a,b=T[22]-.3,E[22]+.3;q=sb(22,1)
    c=kc(t,[(a,(1300,560,1.05)),(q,(700,560,1.12)),(b,(800,540,1.18))])
    ngoai(cv,c,t,g=880,seed=23,mist=.4)
    put(cv,c,'t18x_doi',960,560,s=1.0)
    for r in range(3): di(cv,c,'t18_spr_duong',2700+r*260,880+r*28,1300+r*200,880+r*28,t,a+r*.4,b+2,s=.5+.04*r,bob=3,f=5+r*.4,ph=r,lat=True)
    di(cv,c,'t18_spr_coda',-200,880,300,880,t,a,b,s=.55,bob=3,f=4)
    truoc(cv,c,t)
    lb(cv,C0,'con số lớn là của người thắng?',960,150,t,a+.3,q-.2,col=INK,sz=42)
    lb(cv,C0,'chắc chắn: một người dám tự lên làm vua',960,150,t,q+.2,b,col=RED,sz=42)
# ---- 23: Ngô Thì Sĩ, thế kỷ mười tám
def S_23(cv,t):
    a,b=T[23]-.3,E[23]+.3;q=sb(23,1)
    c=kc(t,[(a,(960,520,1.15)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=24,far=.4,midv=.4,mist=.3)
    put(cv,c,'t18x_ngothisi',960,630,s=1.1)
    flick(cv,c,1120,520,t,.7)
    di(cv,c,'t18_spr_dan',-400,890,250,890,t,a,b,s=.5,bob=2,f=3.4)
    di(cv,c,'t18_spr_quan',2300,880,1700,880,t,q,b,s=.55,bob=2,f=3,lat=True)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.2*inn(t,a,1))
    lb(cv,C0,'hai chữ tướng giặc nằm yên gần ba trăm năm',960,150,t,a+.3,q-.2,col=INK,sz=40)
    lb(cv,C0,'Ngô Thì Sĩ, sách Việt sử tiêu án',960,150,t,q+.2,b,col=RED,sz=42)
# ---- 24: ngang với Lý Bí, Triệu Quang Phục
def S_24(cv,t):
    a,b=T[24]-.3,E[24]+.3;q=sb(24,1)
    c=kc(t,[(a,(960,560,1.0)),(b,(1200,560,1.12))])
    ngoai(cv,c,t,g=880,seed=25,mist=.5)
    put(cv,c,'t18x_bacanh',960,560,s=1.0)
    for i in range(2): di(cv,c,'t18_spr_dan',-500-i*200,890,200+i*140,890,t,a+i*.4,b,s=.45,bob=2,f=3.4,ph=i)
    di(cv,c,'t18_spr_coda',2300,880,1750,880,t,q,b,s=.5,bob=3,f=4,lat=True)
    truoc(cv,c,t)
    if not FREEZE and t>q:
        for k,(nm,x) in enumerate((('Lý Bí',585),('Triệu Quang Phục',960),('Mai Thúc Loan',1335))):
            u=inn(t,q+k*.5,.4);put_screen(cv,band(300,60,PAPER,.88,12),x,820,u);put_screen(cv,text(nm,30,RED if k==2 else INK,700),x,818,u)
    lb(cv,C0,'giỏi hơn hẳn những người có thế lực trong vùng',960,150,t,a+.3,q-.2,col=INK,sz=38)
    lb(cv,C0,'ngang với họ, chỉ khác là việc không thành',960,150,t,q+.2,b,col=RED,sz=40)
# ---- 25: hình ảnh lặp lại khép lại: gạch tướng giặc, viết châu dân (cận cảnh, lặng trước nét cọ)
def S_25(cv,t):
    a,b=T[25]-.3,E[25]+.3
    c=kc(t,[(a,(960,560,1.0)),(b,(960,540,1.06))])
    ngoai(cv,c,t,g=880,seed=26,mist=.5,far=.5,midv=.5)
    di(cv,c,'t18_spr_suga',-300,880,280,880,t,a,b,s=.6,bob=1,f=1.5,lac=.4)
    di(cv,c,'t18_spr_dan',2300,890,1700,890,t,a,b,s=.5,bob=2,f=3.4,lat=True)
    truoc(cv,c,t)
    if not FREEZE: ink_wash(cv,.3)
    cuon(cv,1060,500,t,'VIỆT SỬ TIÊU ÁN','tướng giặc',s=.75,sz=66,gach=inn(t,a+.8,.6),thay='châu dân',uthay=inn(t,a+1.6,1.2))
    if not FREEZE: put_screen(cv,band(420,70,PAPER,.92,12),1500,640,inn(t,a+3.0,.6));put_screen(cv,text('người trong châu',36,RED,700),1500,638,inn(t,a+3.0,.6))
# ---- 26: đền thờ ở Sa Nam
def S_26(cv,t):
    a,b=T[26]-.3,E[26]+.3
    c=kc(t,[(a,(960,500,1.06)),(b,(960,560,1.0))])
    ngoai(cv,c,t,g=880,seed=27)
    put(cv,c,'t18x_den',960,560,s=1.0)
    for i in range(3): smoke(cv,c,1180+i*20,500,t+i,.7)
    for i in range(3): di(cv,c,'t18_spr_dan',-400-i*300,900+i*20,500+i*80,900+i*20,t,a+i*.6,b,s=.45,bob=2,f=3.6+i*.3,ph=i)
    flock(cv,c,t,.6)
    truoc(cv,c,t)
    lb(cv,C0,'Sa Nam, Nam Đàn: đền thờ vua Đen',960,160,t,a+.4,b,col=RED,sz=44)
# ---- 27: kết
def S_27(cv,t):
    a=T[27]-.3;b=E[27]+4;q=sb(27,1)
    c=kc(t,[(a,(900,560,1.06)),(b,(1100,520,1.0))])
    ngoai(cv,c,t,g=880,seed=28,mist=.6)
    put(cv,c,'t18x_cuoi',960,560,s=1.0)
    for i in range(3): di(cv,c,'t18_spr_dan' if i!=1 else 't18_spr_phu',-300-i*220,890+i*14,600+i*180,890+i*14,t,a+i*.4,b,s=.5,bob=3,f=4+i*.3,ph=i)
    di(cv,c,'t18_spr_coda',2300,880,1700,880,t,a,b,s=.5,bob=3,f=4,lat=True)
    flock(cv,c,t,.5)
    truoc(cv,c,t)
    if not FREEZE:
        tx=text('Mai Thúc Loan, năm 722',54,INK,700);put_screen(cv,wipe(tx,inn(t,a+.8,1.4),0,.3,seed=13),W/2,170)
        put_screen(cv,text('vua Đen · người trong châu',34,RED,700),W/2,240,inn(t,a+2.4,1))
        put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,300,inn(t,E[27]+.6,1))
DUONGC=(.17,.29,.45)
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
    flock=lambda *a,**k:None
S=lambda n:T[n]-.3
SH=[(0 if n==1 else S(n),S(n+1) if n<27 else V.TOTAL+1,globals()[f'S_{n}']) for n in range(1,28)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm18_full.json'))
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
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'HOAN CHÂU','stitle18',.55)
    caps(cv,t)
V.NHAN={13:'Dương Tư Húc – thái giám nhà Đường',23:'Ngô Thì Sĩ – nhà sử học thế kỷ 18'}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
