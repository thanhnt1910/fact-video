# Bản dài tm12: Triệu Quang Phục, đầm Dạ Trạch (bộ tranh riêng t12_*, mỗi tranh một cảnh, cảnh nào cũng chuyển động)
import math,re,json,os
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from fx_tran import arrows,dust,sparks,fall
from dai_tm2 import big,tagfall,strike,lb
V=K.setup('tm12',{})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
P=PTS
_SC={}
for _n,_t in TX.items():
    _s=[x for x in re.split(r'(?<=[.!?])\s+',_t) if x.strip()];_w=[len(x.split()) for x in _s];_tot=sum(_w);_c=[0]
    for _k in _w: _c.append(_c[-1]+_k/_tot)
    _SC[_n]=_c
def sb(n,k): return T[n]+(E[n]-T[n])*_SC[n][k]
def mcam(t,keys):
    if os.environ.get('KIEM_TINH'): t=keys[0][0]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z);return cam(cx,cy,z)
import os
FREEZE=bool(os.environ.get('KIEM_TINH'))
MOV={}
def mv(cv,c,name,x0,y0,x1,y1,t,a,b,s=1.0,o=.95,bob=0):
    u=cl((t-a)/max(b-a,.1));put(cv,c,name,x0+(x1-x0)*u,y0+(y1-y0)*u+bob*math.sin(t*2.3),s=s,o=o)
def flick(cv,c,x,y,t,s=1.0):
    put(cv,c,'t12_spr_lua',x+6*math.sin(t*7),y,s=s*(1+.08*math.sin(t*9)),o=.6+.3*math.sin(t*5)**2)
def smoke(cv,c,x,y,t,s=1.0):
    for k in range(2): put(cv,c,'t12_spr_khoi',x+20*math.sin(t*.7+k),y-((t*40+k*120)%240),s=s,o=.5*(1-((t*40+k*120)%240)/240))
def paint_(cv,t,a,b,name,x=960,y=560,s=1.15,dx=0,dy=0,z0=1.0,z1=1.1,mist=.28,sun=None):
    if FREEZE: dx=dy=0;z1=z0;mist=0
    """tranh một lần: máy quay đẩy vào và trôi ngang, sương trôi, chim bay"""
    u=cl((t-a)/max(b-a,.1));c=cam(960+dx*(u-.5),540+dy*(u-.5),z0+(z1-z0)*u)
    put(cv,c,name,x,y,s=s)
    if mist: put(cv,c,'mist',200+u*1500,y+170,s=.9,o=mist);put(cv,c,'mist',1700-u*1400,y-130,s=.7,o=mist*.7)
    if sun: put(cv,c,'sun',sun[0]+u*sun[1],sun[2],o=.45,k=.2)
    return c

LB=(429.7,603.6);CD=(452,643);GN=(402,574);PT=(329,540);DN=(494,808);QC=P['quangchau']
def paint(cv,t,a,b,name,**kw):
    c=paint_(cv,t,a,b,name,**kw)
    if name in MOV: MOV[name](cv,c,t,a,b)
    return c

def pulse(cv,c,x,y,t,col=RED):
    for k in range(2):
        u=((t*.6+k*.5)%1.0);dot(cv,c,x,y,o=.6*(1-u),col=col,r=int(8+40*u))
def boat(cv,c,t,x0,x1,y,a,b,s=1.0,o=.95):
    u=cl((t-a)/max(b-a,.1));put(cv,c,'t12_spr_thuyen',x0+(x1-x0)*u,y+4*math.sin(t*2),s=s,o=o)
def SC(name,n,k0,k1,**kw):
    def f(cv,t,_n=n,_k0=k0,_k1=k1):
        a=sb(_n,_k0)-(.3 if _k0==0 else 0);b=sb(_n,_k1)+(.3 if _k1==len(_SC[_n])-1 else 0)
        return paint(cv,t,a,b,name,**kw),a,b
    return f
def S_1(cv,t):
    a,b=0,E[1]+.3;c=paint(cv,t,a,b,'t12_hai',s=1.0,y=560,x=1200,dx=-250,z0=1.05,z1=1.0,mist=.25)
    boat(cv,c,t,1500,1250,620,a,b,s=.6)
    big(cv,'HAI NGƯỜI, MỘT CÁI ĐẦM',t,.25,b,RED,140,80,seed=1)
def S_2a(cv,t):
    c,a,b=SC('t12_vua',2,0,1,s=1.15,z0=1.0,z1=1.12)(cv,t)
    lb(cv,c,'Trần Bá Tiên, tướng nhà Lương',960,160,t,a+.3,b-1.6,col=INK,sz=42)
    lb(cv,c,'về sau lên làm hoàng đế',960,160,t,b-1.5,b,col=RED,sz=44)
def S_2b(cv,t):
    c,a,b=SC('t12_bien',2,1,3,s=1.0,y=540,dx=-400,z0=1.05,z1=1.0)(cv,t)
    lb(cv,c,'Triệu Quang Phục',960,160,t,a+.2,sb(2,2),col=RED,sz=48)
    lb(cv,c,'chết ở một cửa biển',960,160,t,sb(2,2)+.2,b,col=INK,sz=44)
def S_3(cv,t):
    c,a,b=SC('t12_bun',3,0,2,s=1.15,z0=1.0,z1=1.18,dy=-60)(cv,t)
    lb(cv,c,'trụ được bằng cách nào?',960,160,t,a+.4,sb(3,1),col=INK,sz=46)
    lb(cv,c,'vì sao vẫn mất tất cả?',960,160,t,sb(3,1)+.2,b,col=RED,sz=46)
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3
    c=mcam(t,[(a,(700,500,1.0)),(a+3,(470,620,1.9)),(b,(440,610,2.2))]);mapbg(cv,c,u=inn(t,a-.3,1.2))
    if t>a+1: put(cv,c,'t12_spr_nuoc',0,0,o=0)
    dot(cv,c,*LB);tag(cv,c,LB[0]+16,LB[1]-6,'Long Biên',dy=0,sz=28)
    dot(cv,c,*CD,o=inn(t,a+3,.4));tag(cv,c,CD[0]+16,CD[1]+4,'Chu Diên',dy=0,sz=28)
    lb(cv,c,'đồng bằng sông Hồng dưới quyền nhà Lương',960,170,t,a+.3,sb(4,1),col=INK,sz=40)
    lb(cv,c,'Lý Bí đứng lên',960,170,t,sb(4,1)+.2,b,col=RED,sz=48)
    seal(cv,'s541',1500,330,sb(4,1)+1,t,s=.8,r=4)
    pulse(cv,c,*LB,t)
    stroke(cv,c,[LB,(700,450),(1100,300),QC],inn(t,sb(4,1),max(b-sb(4,1)-.5,1)),wid=4,col=INK,o=.7)
def S_5a(cv,t):
    c,a,b=SC('t12_vanxuan',5,0,2,s=1.15,dx=150,z0=1.0,z1=1.1)(cv,t)
    lb(cv,c,'Lý Nam Đế, nước Vạn Xuân',960,150,t,a+.3,b,col=RED,sz=46)
def S_5b(cv,t):
    c,a,b=SC('t12_luongsang',5,2,4,s=1.0,y=560,dx=500,z0=1.0,z1=1.08)(cv,t)
    lb(cv,c,'cha con Triệu Quang Phục, đất Chu Diên',960,160,t,a+.2,sb(5,3),col=INK,sz=40)
    lb(cv,c,'nhà Lương sai Trần Bá Tiên sang đánh',960,160,t,sb(5,3)+.2,b,col=RED,sz=42)
def S_6a(cv,t):
    c,a,b=SC('t12_thua',6,0,2,s=1.0,y=560,dx=-400,z0=1.0,z1=1.1)(cv,t)
    lb(cv,c,'Chu Diên, cửa sông Tô Lịch',960,170,t,sb(6,1)+.2,b,col=INK,sz=42)
    dust(cv,c,800+(t*80)%300,760,o=.3,s=.4)
def S_6b(cv,t):
    c,a,b=SC('t12_thanh',6,2,3,s=1.15,z0=1.0,z1=1.15)(cv,t)
    lb(cv,c,'thành Gia Ninh bị vây',960,150,t,a+.2,b,col=RED,sz=46)
    for i in range(5): dust(cv,c,700+i*120,560-((t*60+i*40)%200),o=.25,s=.35)
def S_6c(cv,t):
    a,b=sb(6,3),E[6]+.3
    c=mcam(t,[(a,(500,560,2.4)),(b,(380,550,2.6))]);mapbg(cv,c)
    dot(cv,c,*GN);tag(cv,c,GN[0]-110,GN[1]-6,'Gia Ninh',dy=0,sz=26)
    stroke(cv,c,[GN,(370,555),PT],inn(t,a+.3,2.5),wid=4,col=RED,o=.85)
    dot(cv,c,*PT,o=inn(t,a+2.5,.3));tag(cv,c,PT[0]-100,PT[1]-6,'Phú Thọ',dy=0,sz=26)
    pulse(cv,c,*GN,t)
def S_7(cv,t):
    c,a,b=SC('t12_dientriet',7,0,4,s=1.0,y=540,dx=-300,z0=1.0,z1=1.12,mist=.2)(cv,t)
    seal(cv,'s546',1500,300,a+.5,t,s=.8,r=4)
    lb(cv,c,'hồ Điển Triệt, hai vạn quân',960,160,t,a+.4,sb(7,2),col=INK,sz=42)
    if t>sb(7,2): put(cv,c,'t12_spr_nuoc',960,880-260*inn(t,sb(7,2),3.0),s=1.0,o=.8)
    lb(cv,c,'đêm ấy nước sông dâng cao bảy thước',960,160,t,sb(7,2)+.2,b,col=RED,sz=42)
def S_8a(cv,t):
    c,a,b=SC('t12_bachon',8,0,2,s=1.1,z0=1.0,z1=1.08,mist=0)(cv,t)
    for i,w in enumerate(['khúc sông','tòa thành','mặt hồ']): lb(cv,c,w,330+i*620,140,t,a+1.5+i*1.2,b,col=RED,sz=38)
def S_8b(cv,t):
    c,a,b=SC('t12_lvh',8,2,3,s=1.15,dx=-120,z0=1.0,z1=1.1,mist=0)(cv,t)
    lb(cv,c,'Lê Văn Hưu, nhà viết sử đời Trần',960,170,t,a+.3,b,col=INK,sz=42)
def S_9(cv,t):
    c,a,b=SC('t12_nui',9,0,1,s=1.15,z0=1.0,z1=1.15,mist=.4)(cv,t)
    lb(cv,c,'động Khuất Lão',960,150,t,a+.3,a+4,col=INK,sz=44)
    lb(cv,c,'giao việc đánh giặc cho Triệu Quang Phục',960,150,t,a+4.2,b,col=RED,sz=40)
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3
    c=mcam(t,[(a,(440,620,1.6)),(b,(452,640,3.0))]);mapbg(cv,c)
    seal(cv,'s547',1500,330,a+.6,t,s=.8,r=4)
    dot(cv,c,*LB,o=.6);tag(cv,c,LB[0]+12,LB[1]-6,'Long Biên',dy=0,sz=24)
    stroke(cv,c,[LB,CD],inn(t,a+.5,b-a-1),wid=4,col=RED,o=.8);pulse(cv,c,*CD,t);pulse(cv,c,*LB,t+.7,col=INK)
    mv(cv,c,'t12_spr_thuyen',LB[0]-10,LB[1]+10,CD[0]-10,CD[1]+10,t,a,b,s=.12)
    if t>sb(10,1): dot(cv,c,*CD,col=RED,r=9);tag(cv,c,CD[0]+14,CD[1]+4,'đầm Dạ Trạch',dy=0,sz=28)
    lb(cv,c,'không giữ thành, không bày trận',960,170,t,a+.3,sb(10,1),col=INK,sz=42)
    lb(cv,c,'vùng Khoái Châu, Hưng Yên bây giờ',960,170,t,sb(10,1)+.2,b,col=RED,sz=42)
def S_11a(cv,t):
    c,a,b=SC('t12_dam',11,0,1,s=1.0,y=540,dx=-500,z0=1.0,z1=1.1,mist=.4)(cv,t)
def S_11b(cv,t):
    c,a,b=SC('t12_docmoc',11,1,4,s=1.15,dx=200,z0=1.0,z1=1.1)(cv,t)
    lb(cv,c,'thuyền độc mộc',960,160,t,sb(11,2)-.3,sb(11,3),col=RED,sz=46)
    lb(cv,c,'không thuộc đường thì lạc',960,160,t,sb(11,3)+.2,b,col=INK,sz=42)
def S_12(cv,t):
    c,a,b=SC('t12_bokhuat',12,0,2,s=1.0,y=550,dx=400,z0=1.0,z1=1.1,mist=.3)(cv,t)
    lb(cv,c,'không chỗ dàn trận, không đường cho ngựa',960,160,t,sb(12,1)+.2,b,col=RED,sz=40)
def S_13a(cv,t):
    c,a,b=SC('t12_ngay',13,0,1,s=1.0,y=540,dx=-300,z0=1.0,z1=1.06,mist=.2)(cv,t)
    lb(cv,c,'ban ngày tắt hết khói bếp',960,160,t,a+.3,b,col=INK,sz=44)
def S_13b(cv,t):
    c,a,b=SC('t12_dem',13,1,3,s=1.0,y=540,dx=400,z0=1.0,z1=1.12,mist=0)(cv,t)
    for i in range(3): boat(cv,c,t,200+i*250,900+i*250,820+i*20,a,b,s=.5)
    lb(cv,c,'đêm xuống, đánh úp trại giặc',960,160,t,a+.3,b,col=RED,sz=44)
def S_14(cv,t):
    c,a,b=SC('t12_luong',14,0,4,s=1.15,dx=-200,z0=1.0,z1=1.12,mist=.15)(cv,t)
    lb(cv,c,'thế hai bên đổi chỗ',960,150,t,a+.3,sb(14,2),col=RED,sz=46)
    lb(cv,c,'nuôi quân bằng lương của giặc',960,150,t,sb(14,2)+.2,sb(14,3),col=INK,sz=42)
    seal(cv,'sdtv',960,330,sb(14,3)+.5,t,s=.9,r=-3)
def S_15(cv,t):
    c,a,b=SC('t12_sachhai',15,0,2,s=1.1,z0=1.0,z1=1.08,mist=0)(cv,t)
    lb(cv,c,'sử Trung Hoa không ghi tên ông',960,120,t,a+.3,sb(15,1),col=RED,sz=42)
    lb(cv,c,'sử nước ta chép lại nhiều thế kỷ sau',960,120,t,sb(15,1)+.2,b,col=INK,sz=40)
def S_16(cv,t):
    c,a,b=SC('t12_mat',16,0,2,s=1.15,z0=1.0,z1=1.1,mist=.45)(cv,t)
    seal(cv,'s548',1500,300,a+.5,t,s=.8,r=4)
    lb(cv,c,'Toàn thư: chết vì bệnh',960,150,t,sb(16,1)+.2,sb(16,1)+4,col=INK,sz=42)
    lb(cv,c,'sử Trung Hoa: bị giết',960,150,t,sb(16,1)+4.2,b,col=RED,sz=42)
def S_17(cv,t):
    c,a,b=SC('t12_haivua',17,0,3,s=1.0,y=540,dx=-600,z0=1.0,z1=1.04,mist=.25)(cv,t)
    lb(cv,c,'Triệu Việt Vương',960,160,t,a+.3,sb(17,1),col=RED,sz=46)
    lb(cv,c,'hai vị vua',960,160,t,sb(17,2)+.2,b,col=INK,sz=46)
def S_18(cv,t):
    c,a,b=SC('t12_vay',18,0,3,s=1.1,z0=1.12,z1=1.0,mist=.2)(cv,t)
    seal(cv,'s550',1500,300,a+.5,t,s=.8,r=4)
    lb(cv,c,'chặn đường lương, vây thật lâu',960,140,t,sb(18,1),b,col=RED,sz=44)
def S_19(cv,t):
    c,a,b=SC('t12_kinhdo',19,0,3,s=1.15,z0=1.0,z1=1.12,mist=0)(cv,t)
    lb(cv,c,'Hầu Cảnh làm phản, chiếm kinh đô nhà Lương',960,140,t,sb(19,1),sb(19,2),col=RED,sz=40)
    lb(cv,c,'vua nhà Lương chết khi bị giam',960,140,t,sb(19,2)+.2,b,col=INK,sz=42)
    for i in range(6): dust(cv,c,600+i*150,300-((t*50+i*30)%220),o=.25,s=.4)
def S_20a(cv,t):
    c,a,b=SC('t12_ra',20,0,2,s=1.0,y=550,dx=600,z0=1.0,z1=1.06)(cv,t)
    lb(cv,c,'Trần Bá Tiên bị gọi về',960,150,t,a+.3,sb(20,1),col=INK,sz=44)
    lb(cv,c,'ra khỏi đầm',960,150,t,sb(20,1)+.2,b,col=RED,sz=48)
def S_20b(cv,t):
    c,a,b=SC('t12_longbien',20,2,3,s=1.15,z0=1.0,z1=1.12)(cv,t)
    lb(cv,c,'vào thành Long Biên',960,120,t,a+.3,b,col=RED,sz=46)
def S_21(cv,t):
    c,a,b=SC('t12_nuoc',21,0,3,s=1.15,dx=-150,z0=1.0,z1=1.08,mist=0)(cv,t)
    lb(cv,c,'nước lũ giúp quân Lương',700,170,t,sb(21,2),b,col=INK,sz=38)
    lb(cv,c,'cơn loạn giúp người trong đầm',1260,230,t,sb(21,2)+1.5,b,col=RED,sz=38)
def S_22(cv,t):
    c,a,b=SC('t12_lenngoi',22,0,3,s=1.0,y=560,dx=-300,z0=1.0,z1=1.1)(cv,t)
    seal(cv,'s557',1500,300,a+1,t,s=.8,r=4)
    lb(cv,c,'Trần Bá Tiên lên ngôi, lập nhà Trần của Trung Hoa',960,140,t,a+.3,b,col=RED,sz=38)
def S_23a(cv,t):
    c,a,b=SC('t12_phattu',23,0,2,s=1.0,y=550,dx=-500,z0=1.0,z1=1.08)(cv,t)
    lb(cv,c,'Lý Phật Tử, người họ Lý',960,150,t,sb(23,1),b,col=RED,sz=44)
def S_23b(cv,t):
    c,a,b=SC('t12_namtran',23,2,3,s=1.1,z0=1.0,z1=1.08,mist=0)(cv,t)
    lb(cv,c,'năm trận, không bên nào thắng',960,140,t,a+.3,b,col=INK,sz=44)
def S_24a(cv,t):
    c,a,b=SC('t12_hoa',24,0,3,s=1.0,y=540,dx=300,z0=1.0,z1=1.1)(cv,t)
    lb(cv,c,'bãi Quân Thần làm ranh giới',960,150,t,sb(24,2)-.5,b,col=RED,sz=42)
def S_24b(cv,t):
    c,a,b=SC('t12_cuoi',24,3,4,s=1.15,z0=1.0,z1=1.1)(cv,t)
    lb(cv,c,'Nhã Lang ở rể',960,130,t,a+.3,b,col=INK,sz=44)
def S_25(cv,t):
    c,a,b=SC('t12_hai_mat',25,0,4,s=1.1,z0=1.0,z1=1.1,mist=0)(cv,t)
    lb(cv,c,'vì họ Lý mà giữ nước',520,170,t,sb(25,1)-1,b,col=INK,sz=36)
    lb(cv,c,'vì họ Lý mà chia đất',1400,170,t,sb(25,1)+1.5,b,col=RED,sz=36)
def S_26a(cv,t):
    c,a,b=SC('t12_danhup',26,0,2,s=1.0,y=540,dx=500,z0=1.0,z1=1.1)(cv,t)
    seal(cv,'s571',1500,300,a+.5,t,s=.8,r=4)
    lb(cv,c,'Lý Phật Tử phá lời hòa ước',960,150,t,a+.3,b,col=RED,sz=44)
def S_26b(cv,t):
    a,b=sb(26,2),sb(26,3)
    c=mcam(t,[(a,(440,650,2.0)),(b,(480,760,2.2))]);mapbg(cv,c)
    dot(cv,c,*LB,o=.6);tag(cv,c,LB[0]+12,LB[1]-6,'Long Biên',dy=0,sz=24)
    stroke(cv,c,[LB,(470,700),DN],inn(t,a+.3,3),wid=4,col=RED,o=.85)
    pulse(cv,c,*DN,t)
    dot(cv,c,*DN,o=inn(t,a+3,.3));tag(cv,c,DN[0]+14,DN[1]+4,'cửa biển Đại Nha',dy=0,sz=26)
def S_26c(cv,t):
    a,b=sb(26,3),E[26]+.3
    c=paint(cv,t,a,b,'t12_daina',s=1.0,y=540,dx=-300,z0=1.05,z1=1.0,mist=.3)
    lb(cv,c,'đền thờ ở cửa biển',960,150,t,a+.3,b,col=INK,sz=44)
def S_27(cv,t):
    c,a,b=SC('t12_mongrong',27,0,3,s=1.15,z0=1.0,z1=1.12,mist=.1)(cv,t)
    lb(cv,c,'truyền thuyết móng rồng',960,130,t,a+.3,sb(27,2),col=RED,sz=44)
    lb(cv,c,'Cương mục: chuyện hoang đường',960,130,t,sb(27,2)+.2,b,col=INK,sz=42)
def S_28(cv,t):
    c,a,b=SC('t12_trongnha',28,0,3,s=1.15,dx=-200,z0=1.0,z1=1.1)(cv,t)
    lb(cv,c,'Ngô Sĩ Liên chê Lý Phật Tử',960,130,t,sb(28,1)-.3,sb(28,2),col=INK,sz=42)
def S_29(cv,t):
    a=T[29]-.3;c=paint(cv,t,a,E[29]+4,'t12_ket',s=1.0,y=540,dx=-300,z0=1.05,z1=1.0,mist=.3)
    boat(cv,c,t,1400,1600,600,a,E[29]+4,s=.5,o=.6)
    tx=text('Triệu Quang Phục, Dạ Trạch Vương',54,INK,700);put_screen(cv,wipe(tx,inn(t,a+.8,1.4),0,.3,seed=12),W/2,170)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,600,inn(t,E[29]+.6,1))

MOV.update({
't12_hai':lambda cv,c,t,a,b:mv(cv,c,'t12_spr_chim',300,200,1500,140,t,a,b,s=.8,o=.7),
't12_vua':lambda cv,c,t,a,b:smoke(cv,c,700,620,t),
't12_bien':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_chim',1700,180,400,120,t,a,b,s=.8,o=.7),mv(cv,c,'t12_spr_nuoc',960,900,960,880,t,a,b,o=.5,bob=12)),
't12_bun':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_nuoc',960,1000,960,980,t,a,b,o=.45,bob=14),mv(cv,c,'t12_spr_chim',1600,160,300,220,t,a,b,s=.7,o=.6)),
't12_vanxuan':lambda cv,c,t,a,b:mv(cv,c,'t12_spr_dan',100,830,700,800,t,a,b,s=.9),
't12_luongsang':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_linh',-200,850,700,850,t,a,b,s=1.0),mv(cv,c,'t12_spr_ngua',300,760,1100,760,t,a,b,s=.9)),
't12_thua':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_linh',1500,840,900,840,t,a,b,s=.9),mv(cv,c,'t12_spr_dan',700,860,200,860,t,a,b,s=.8)),
't12_thanh':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_linh',1700,880,1300,860,t,a,b,s=.8),smoke(cv,c,960,520,t)),
't12_dientriet':lambda cv,c,t,a,b:mv(cv,c,'t12_spr_thuyen',1300,700,1450,700,t,a,b,s=.7,bob=8),
't12_bachon':lambda cv,c,t,a,b:[stroke(cv,c,[(150+i*620,300),(500+i*620,300)],inn(t,a+.5+i*1.2,1.0),wid=6,col=RED,o=.8) for i in range(3)],
't12_lvh':lambda cv,c,t,a,b:(smoke(cv,c,1600,640,t),smoke(cv,c,1450,640,t+2),mv(cv,c,'t12_spr_chim',1700,220,300,180,t,a,b,s=1.0,o=.7)),
't12_nui':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_nguoi',450,780,900,700,t,a,b,s=1.3),mv(cv,c,'t12_spr_chim',1700,200,400,160,t,a,b,s=.9,o=.7)),
't12_dam':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_thuyen',300,780,900,740,t,a,b,s=.6,bob=6),mv(cv,c,'t12_spr_chim',1700,150,600,120,t,a,b,s=.7,o=.6)),
't12_docmoc':lambda cv,c,t,a,b:mv(cv,c,'t12_spr_thuyen',1800,820,1350,800,t,a,b,s=.8,bob=6),
't12_bokhuat':lambda cv,c,t,a,b:mv(cv,c,'t12_spr_ngua',500+120*math.sin(t*.8),760,500+120*math.sin(t*.8),760,t,a,b,s=.9),
't12_ngay':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_chim',300,220,1600,160,t,a,b,s=1.1,o=.8),mv(cv,c,'t12_spr_chim',1700,320,700,260,t,a,b,s=.8,o=.7),mv(cv,c,'t12_spr_nuoc',960,960,960,940,t,a,b,o=.45,bob=14)),
't12_dem':lambda cv,c,t,a,b:[flick(cv,c,1350+i*230,640,t+i,s=.5) for i in range(3)],
't12_luong':lambda cv,c,t,a,b:mv(cv,c,'t12_spr_dan',1500,780,700,780,t,a,b,s=.9),
't12_sachhai':lambda cv,c,t,a,b:[stroke(cv,c,[(1150+i*45,240),(1150+i*45,600)],inn(t,a+.3+i*.4,.6),wid=5,col=INK,o=.7,head=False) for i in range(8)],
't12_mat':lambda cv,c,t,a,b:smoke(cv,c,960,700,t,s=1.2),
't12_haivua':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_chim',200,200,1700,180,t,a,b,s=1.1,o=.8),smoke(cv,c,1550,560,t),mv(cv,c,'t12_spr_nuoc',400,960,400,940,t,a,b,o=.45,bob=14)),
't12_vay':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_linh',200,860,1500,860,t,a,b,s=.9),mv(cv,c,'t12_spr_linh',1700,330,500,330,t,a,b,s=.6)),
't12_kinhdo':lambda cv,c,t,a,b:([flick(cv,c,640+i*200,360,t+i,s=.6) for i in range(4)],smoke(cv,c,960,300,t,s=1.3)),
't12_ra':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_thuyen',200,820,900,800,t,a,b,s=.6,bob=5),mv(cv,c,'t12_spr_linh',700,850,1400,850,t,a,b,s=.8)),
't12_longbien':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_linh',100,860,820,840,t,a,b,s=1.0),mv(cv,c,'t12_spr_chim',1600,160,500,140,t,a,b,s=.9,o=.7)),
't12_nuoc':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_nuoc',480,900,480,880,t,a,b,o=.5,bob=16),[flick(cv,c,1200+i*180,620,t+i,s=.6) for i in range(3)]),
't12_lenngoi':lambda cv,c,t,a,b:(smoke(cv,c,700,700,t),smoke(cv,c,1220,700,t+3)),
't12_phattu':lambda cv,c,t,a,b:mv(cv,c,'t12_spr_linh',300,560,800,760,t,a,b,s=.7),
't12_namtran':lambda cv,c,t,a,b:[dust(cv,c,190+i*380,560-((t*50+i*30)%150),o=.3,s=.35) for i in range(5)]+[stroke(cv,c,[(190+i*380-80,620),(190+i*380+80,620)],inn(t,a+.4+i*.8,.5),wid=6,col=RED,o=.7) for i in range(5)],
't12_hoa':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_thuyen',200,700,1000,700,t,a,b,s=.8,bob=6),mv(cv,c,'t12_spr_chim',1700,200,500,160,t,a,b,s=1.0,o=.8)),
't12_cuoi':lambda cv,c,t,a,b:mv(cv,c,'t12_spr_nguoi',300,800,700,780,t,a,b,s=.9),
't12_hai_mat':lambda cv,c,t,a,b:mv(cv,c,'t12_spr_nguoi',1700,780,1500,770,t,a,b,s=.9),
't12_danhup':lambda cv,c,t,a,b:([flick(cv,c,1200+i*200,520,t+i,s=.6) for i in range(3)],mv(cv,c,'t12_spr_linh',0,860,700,860,t,a,b,s=.9)),
't12_daina':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_chim',1700,160,500,120,t,a,b,s=.8,o=.7),mv(cv,c,'t12_spr_nuoc',960,880,960,860,t,a,b,o=.4,bob=12)),
't12_mongrong':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_lua',1300,640,950,320,t,a+2,b-2,s=.6,o=.8),smoke(cv,c,960,380,t)),
't12_trongnha':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_nguoi',1300,830,500,880,t,a,b,s=1.1),smoke(cv,c,1560,560,t)),
't12_ket':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_chim',1600,200,500,160,t,a,b,s=1.1,o=.8),mv(cv,c,'t12_spr_nuoc',960,960,960,940,t,a,b,o=.45,bob=14)),
})
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
S=lambda n:T[n]-.3
def X(n,k): return sb(n,k)
SH=[(0,S(2),S_1),(S(2),X(2,1),S_2a),(X(2,1),S(3),S_2b),(S(3),S(4),S_3),(S(4),S(5),S_4),(S(5),X(5,2),S_5a),(X(5,2),S(6),S_5b),
 (S(6),X(6,2),S_6a),(X(6,2),X(6,3),S_6b),(X(6,3),S(7),S_6c),(S(7),S(8),S_7),(S(8),X(8,2),S_8a),(X(8,2),S(9),S_8b),(S(9),S(10),S_9),(S(10),S(11),S_10),
 (S(11),X(11,1),S_11a),(X(11,1),S(12),S_11b),(S(12),S(13),S_12),(S(13),X(13,1),S_13a),(X(13,1),S(14),S_13b),(S(14),S(15),S_14),(S(15),S(16),S_15),(S(16),S(17),S_16),
 (S(17),S(18),S_17),(S(18),S(19),S_18),(S(19),S(20),S_19),(S(20),X(20,2),S_20a),(X(20,2),S(21),S_20b),(S(21),S(22),S_21),(S(22),S(23),S_22),
 (S(23),X(23,2),S_23a),(X(23,2),S(24),S_23b),(S(24),X(24,3),S_24a),(X(24,3),S(25),S_24b),(S(25),S(26),S_25),(S(26),X(26,2),S_26a),(X(26,2),X(26,3),S_26b),(X(26,3),S(27),S_26c),
 (S(27),S(28),S_27),(S(28),S(29),S_28),(S(29),V.TOTAL+1,S_29)]
_J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm12_full.json'))
SENT={}
for _i,_d in enumerate(_J):
    _hs=[x for x in re.split(r'(?<=[.!?])\s+',_d['hien']) if x.strip()]
    SENT[_i+1]=_hs if len(_hs)==len(_SC[_i+1])-1 else [_d['hien']]
def caps(cv,t):
    for n,hs in SENT.items():
        for k,h in enumerate(hs):
            a=sb(n,k) if len(hs)>1 else T[n];b=sb(n,k+1) if len(hs)>1 else E[n]
            if a-.3<t<b+.35: caption(cv,h,inn(t,a-.25,.25)*(1-inn(t,b+.05,.25)),False)
if FREEZE:
    def caps(cv,t): pass
def ov(cv,t):
    if FREEZE: return
    TT=T[4]
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'ĐẦM DẠ TRẠCH','stitle12',.55)
    caps(cv,t)
V.NHAN={}
class _V2: pass
V2=_V2();V2.__dict__.update(V.__dict__);V2.TX={}
def frame(t): return K.compose(V2,SH,t,ov,{})
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
