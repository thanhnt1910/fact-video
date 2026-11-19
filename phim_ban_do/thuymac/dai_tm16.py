# Bản dài tm16: Bà Triệu, Cửu Chân năm 248 (bộ tranh riêng t16_*, mỗi tranh một cảnh, cảnh nào cũng chuyển động)
# Quy ước màu (quy ước hình ảnh): Việt đỏ son, nhà Ngô xanh chàm; Bà Triệu áo vàng theo Giao Chỉ chí. Một phe một màu suốt video.
import math,re,json,os
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from fx_tran import arrows,dust,sparks,fall
from tran_fx import clash
from dai_tm2 import big,tagfall,strike,lb
V=K.setup('tm16',{4:4.0})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
P=PTS
FREEZE=bool(os.environ.get('KIEM_TINH'))
NGO=(.17,.29,.45)
_SC={}
for _n,_t in TX.items():
    _s=[x for x in re.split(r'(?<=[.!?])\s+',_t) if x.strip()];_w=[len(x.split()) for x in _s];_tot=sum(_w);_c=[0]
    for _k in _w: _c.append(_c[-1]+_k/_tot)
    _SC[_n]=_c
def sb(n,k): return T[n]+(E[n]-T[n])*_SC[n][k]
def mcam(t,keys):
    if FREEZE: t=keys[0][0]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z);return cam(cx,cy,z)
MOV={}
def mv(cv,c,name,x0,y0,x1,y1,t,a,b,s=1.0,o=.95,bob=0):
    u=cl((t-a)/max(b-a,.1));put(cv,c,name,x0+(x1-x0)*u,y0+(y1-y0)*u+bob*math.sin(t*2.3),s=s,o=o)
def flick(cv,c,x,y,t,s=1.0):
    put(cv,c,'t12_spr_lua',x+6*math.sin(t*7),y,s=s*(1+.08*math.sin(t*9)),o=.6+.3*math.sin(t*5)**2)
def smoke(cv,c,x,y,t,s=1.0):
    for k in range(2): put(cv,c,'t12_spr_khoi',x+20*math.sin(t*.7+k),y-((t*40+k*120)%240),s=s,o=.5*(1-((t*40+k*120)%240)/240))
def paint_(cv,t,a,b,name,x=960,y=560,s=1.15,dx=0,dy=0,z0=1.0,z1=1.1,mist=.28):
    if FREEZE: dx=dy=0;z1=z0;mist=0
    u=cl((t-a)/max(b-a,.1));c=cam(960+dx*(u-.5),540+dy*(u-.5),z0+(z1-z0)*u)
    put(cv,c,name,x,y,s=s)
    if mist: put(cv,c,'mist',200+u*1500,y+170,s=.9,o=mist);put(cv,c,'mist',1700-u*1400,y-130,s=.7,o=mist*.7)
    return c
def paint(cv,t,a,b,name,**kw):
    c=paint_(cv,t,a,b,name,**kw)
    if name in MOV: MOV[name](cv,c,t,a,b)
    return c
def pulse(cv,c,x,y,t,col=RED):
    for k in range(2):
        u=((t*.6+k*.5)%1.0);dot(cv,c,x,y,o=.6*(1-u),col=col,r=int(8+40*u))
def voi(cv,c,x0,y0,x1,y1,t,a,b,s=.8,o=.97,k=0):
    u=cl((t-a)/max(b-a,.1));put(cv,c,'t16_spr_voi_k' if k else 't16_spr_voi',x0+(x1-x0)*u,y0+(y1-y0)*u+5*math.sin(t*2.6),s=s,o=o)
# 1 hook
def S_1(cv,t):
    a,b=0,E[1]+.3
    c=paint(cv,t,a,b,'t16_voi1',s=1.0,y=560,dx=-300,z0=1.1,z1=1.0,mist=.2)
    flock(cv,c,t,.6)
    big(cv,'HƠN BA VẠN NHÀ RA HÀNG',t,.25,2.9,RED,150,76,seed=1)
    big(cv,'MỘT PHỤ NỮ CƯỠI VOI NỔI LÊN',t,3.0,b,INK,150,70,seed=2)
# 2
def S_2(cv,t):
    a,b=T[2]-.3,E[2]+.3
    c=paint(cv,t,a,b,'t16_trusoo',s=1.15,z0=1.0,z1=1.1,mist=.2)
    seal(cv,'s248',1560,330,a+.6,t,s=.8,r=4)
    lb(cv,c,'năm 248, Cửu Chân (Thanh Hóa)',960,170,t,a+.4,sb(2,1)-.2,col=RED,sz=44)
    lb(cv,c,'nhà Ngô vừa dẹp yên bằng lời hứa khoan dung',960,170,t,sb(2,1)+.2,sb(2,1)+(E[2]-sb(2,1))*.5,col=INK,sz=38)
    lb(cv,c,'người phụ nữ ấy đánh vào trụ sở quận huyện',960,170,t,sb(2,1)+(E[2]-sb(2,1))*.5+.2,b,col=RED,sz=40)
    lb(cv,c,'quân nhà Ngô',500,300,t,a+1,b,col=NGO,sz=32);lb(cv,c,'người theo bà',1500,300,t,a+1,b,col=RED,sz=32)
# 3
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3
    c=paint(cv,t,a,b,'t16_so',s=1.15,z0=1.0,z1=1.12,mist=.15)
    lb(cv,c,'sử nhà Ngô đếm kỹ số nhà ra hàng',960,160,t,a+.4,sb(3,1)-(sb(3,1)-a)*.45-.1,col=INK,sz=40)
    lb(cv,c,'nhưng không chép tên bà',960,160,t,sb(3,1)-(sb(3,1)-a)*.45,sb(3,1)-.1,col=RED,sz=42)
    lb(cv,c,'vì sao bà không ra hàng?',960,160,t,sb(3,1)+.1,sb(3,2)-.1,col=RED,sz=42)
    lb(cv,c,'vì sao phần lớn do đời sau kể lại?',960,160,t,sb(3,2)+.1,b,col=INK,sz=40)
# 4 bản đồ (hai câu)
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3
    dl,th,ng=P['daila'],P['thanhhoa'],P['nghean']
    c=mcam(t,[(a-.3,(700,620,1.35)),(a+4,(760,740,1.1)),(b,(860,700,1.0))])
    mapbg(cv,c,u=inn(t,a-.4,1.2))
    for nm,p in (('Giao Chỉ',dl),('Cửu Chân',th),('Nhật Nam',ng)):
        dot(cv,c,*p,o=inn(t,a+.6,.4));tag(cv,c,p[0]+22,p[1]-6,nm,dy=0,sz=26)
    pulse(cv,c,*th,t)
    stroke(cv,c,[(dl[0]+500,dl[1]-300),(dl[0]+200,dl[1]-120),dl],inn(t,a+.5,3),wid=8,col=NGO)
    lb(cv,c,'Trung Hoa chia ba nước; Giao Châu thuộc nước Ngô',960,170,t,a+.3,sb(4,1)-.2,col=INK,sz=38)
    lb(cv,c,'Sĩ Nhiếp cai quản mấy chục năm',960,170,t,sb(4,1)+.2,sb(4,1)+(b-sb(4,1))*.5,col=INK,sz=40)
    lb(cv,c,'nhà Ngô sai Lữ Đại sang nắm vùng đất này',960,170,t,sb(4,1)+(b-sb(4,1))*.5+.2,b,col=RED,sz=38)
# 5
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3
    c=paint(cv,t,a,b,'t16_luudai',s=1.15,z0=1.0,z1=1.12,mist=.2)
    lb(cv,c,'Sĩ Huy không nghe lệnh, đem quân chống lại',960,170,t,a+.4,sb(5,1)-.2,col=INK,sz=40)
    lb(cv,c,'Lữ Đại hứa tha, rồi chém Sĩ Huy',960,170,t,sb(5,1)+.2,b,col=RED,sz=44)
# 6
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3
    c=paint(cv,t,a,b,'t16_sulien',s=1.15,z0=1.0,z1=1.1,mist=0)
    lb(cv,c,'Ngô Sĩ Liên, sử gia đời Lê',960,160,t,a+.4,sb(6,1)-.2,col=INK,sz=42)
    lb(cv,c,'một lời hứa của nhà Ngô đã bị phá',960,160,t,sb(6,1)+.2,b,col=RED,sz=42)
# 7
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3
    c=paint(cv,t,a,b,'t16_thu',s=1.15,z0=1.0,z1=1.12,mist=0)
    lb(cv,c,'mấy năm sau, một quan nhà Ngô dâng thư',960,160,t,a+.4,sb(7,1)-.2,col=INK,sz=40)
    lb(cv,c,'giao nhầm người thì sẽ lại sinh chuyện',960,160,t,sb(7,1)+.2,b,col=RED,sz=40)
# 8
def S_8(cv,t):
    a,b=T[8]-.3,E[8]+.3
    c=paint(cv,t,a,b,'t16_chiemthanh',s=1.0,y=560,dx=-300,z0=1.05,z1=1.0,mist=.2)
    lb(cv,c,'người Cửu Chân nổi lên đánh chiếm các thành',960,170,t,a+.4,sb(8,1)-.2,col=RED,sz=40)
    lb(cv,c,'cả Giao Châu rối ren, nhà Ngô cử người mới sang',960,170,t,sb(8,1)+.2,b,col=INK,sz=38)
    lb(cv,c,'quân nhà Ngô',420,300,t,a+.6,b,col=NGO,sz=32);lb(cv,c,'người Cửu Chân',1500,300,t,a+.6,b,col=RED,sz=32)
# 9
def S_9(cv,t):
    a,b=T[9]-.3,E[9]+.3
    c=paint(cv,t,a,b,'t16_lucdan',s=1.0,y=560,dx=-500,z0=1.1,z1=1.0,mist=.3)
    lb(cv,c,'Lục Dận, quan đứng đầu Giao Châu',960,170,t,a+.4,sb(9,1)-.2,col=NGO,sz=42)
    lb(cv,c,'hứa khoan dung và giữ chữ tín với ai ra hàng',960,170,t,sb(9,1)+.2,b,col=INK,sz=40)
# 10
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3
    c=paint(cv,t,a,b,'t16_rahang',s=1.15,dx=-200,z0=1.0,z1=1.12,mist=.15)
    lb(cv,c,'lời kêu gọi có tác dụng',960,160,t,a+.4,sb(10,1)-.2,col=INK,sz=42)
    n=int(30000*inn(t,sb(10,1),2.2));
    if t>sb(10,1)-.1:
        im=text('Toàn thư: hơn '+f'{n:,}'.replace(',','.')+' nhà ra hàng',46,RED,700);put_screen(cv,im,W/2,170,inn(t,sb(10,1)-.1,.4)*(1-inn(t,sb(10,2)+.1,.4)))
    if t>sb(10,2)-.1:
        im=text('sử nhà Ngô: hơn 100 thủ lĩnh, hơn 50.000 nhà quy phục',40,INK,700);put_screen(cv,im,W/2,170,inn(t,sb(10,2)-.1,.4))
# 11
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3
    c=paint(cv,t,a,b,'t16_bovukhi',s=1.0,y=560,dx=-400,z0=1.05,z1=1.0,mist=.2)
    lb(cv,c,'khác thời Lữ Đại: dùng lời hứa trước khi dùng quân',960,170,t,a+.4,sb(11,1)-.2,col=INK,sz=38)
    lb(cv,c,'sử không chép họ nghĩ gì, chỉ biết phần lớn nhận lời',960,170,t,sb(11,1)+.2,b,col=RED,sz=38)
# 12
def S_12(cv,t):
    a,b=T[12]-.3,E[12]+.3
    c=paint(cv,t,a,b,'t16_noilen',s=1.15,z0=1.0,z1=1.14,mist=.2)
    lb(cv,c,'cả vùng vừa yên, một phụ nữ họ Triệu nổi lên',960,160,t,a+.4,sb(12,1)-.2,col=RED,sz=40)
    lb(cv,c,'Cương mục: tập hợp người theo mình, đánh phá trụ sở',960,160,t,sb(12,1)+.2,b,col=INK,sz=38)
    pulse(cv,c,960,470,t)
# 13
def S_13(cv,t):
    a,b=T[13]-.3,E[13]+.3
    c=paint(cv,t,a,b,'t16_voi2',s=1.0,y=560,dx=-300,z0=1.05,z1=1.0,mist=.15)
    lb(cv,c,'Toàn thư: bà cưỡi voi ra trận',960,160,t,a+.4,sb(13,1)-.2,col=RED,sz=44)
    lb(cv,c,'Giao Chỉ chí: cô gái chưa chồng, áo vải vàng',960,160,t,sb(13,1)+.2,b,col=INK,sz=40)
    lb(cv,c,'quân nhà Ngô',470,330,t,a+.6,b,col=NGO,sz=32);lb(cv,c,'quân của bà',1450,330,t,a+.6,b,col=RED,sz=32)
# 14
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3
    c=paint(cv,t,a,b,'t16_dep',s=1.0,y=560,dx=300,z0=1.0,z1=1.08,mist=.35)
    lb(cv,c,'Lục Dận đem quân dẹp được bà',960,160,t,a+.4,sb(14,1)-.2,col=NGO,sz=44)
    lb(cv,c,'sử không chép nơi nào, bao lâu, bà mất ra sao',960,160,t,sb(14,1)+.2,b,col=INK,sz=38)
# 15
def S_15(cv,t):
    a,b=T[15]-.3,E[15]+.3
    c=paint(cv,t,a,b,'t16_thutu',s=1.15,dx=-120,z0=1.0,z1=1.1,mist=.2)
    lb(cv,c,'thứ tự các việc mới là chỗ khác thường',960,160,t,a+.4,sb(15,1)-.2,col=INK,sz=40)
    lb(cv,c,'người khác bỏ vũ khí, bà đứng lên',960,160,t,sb(15,1)+.2,sb(15,2)-.2,col=RED,sz=42)
    lb(cv,c,'sử không chép vì sao bà chọn khác',960,160,t,sb(15,2)+.2,b,col=INK,sz=40)
# 16
def S_16(cv,t):
    a,b=T[16]-.3,E[16]+.3
    c=paint(cv,t,a,b,'t16_den',s=1.15,z0=1.0,z1=1.12,mist=.15)
    lb(cv,c,'sau khi chết, bà thành thần',960,160,t,a+.4,sb(16,1)-.2,col=RED,sz=44)
    lb(cv,c,'đền ở xã Phú Điền, nay thuộc vùng Hậu Lộc, Thanh Hóa',960,160,t,sb(16,1)+.2,b,col=INK,sz=38)
# 17
def S_17(cv,t):
    a,b=T[17]-.3,E[17]+.3
    c=paint(cv,t,a,b,'t16_sunguyen',s=1.15,z0=1.0,z1=1.12,mist=0)
    lb(cv,c,'sử triều Nguyễn: chỉ đứng sau Hai Bà Trưng',960,160,t,a+.4,b,col=RED,sz=42)
# 18
def S_18(cv,t):
    a,b=T[18]-.3,E[18]+.3
    c=paint(cv,t,a,b,'t16_sachtong',s=1.15,z0=1.0,z1=1.12,mist=0)
    lb(cv,c,'những điều quen thuộc từ đâu mà có?',960,160,t,a+.4,sb(18,1)-.2,col=RED,sz=42)
    lb(cv,c,'sách địa lý đời Tống, hơn 700 năm sau khi bà mất',960,160,t,sb(18,1)+.2,b,col=INK,sz=38)
# 19
def S_19(cv,t):
    a,b=T[19]-.3,E[19]+.3
    c=paint(cv,t,a,b,'t16_hoangduong',s=1.15,z0=1.0,z1=1.12,mist=0)
    lb(cv,c,'mỗi sách ghi một kiểu: chuyện hoang đường',960,120,t,a+.4,b,col=RED,sz=42)
# 20
def S_20(cv,t):
    a,b=T[20]-.3,E[20]+.3
    c=paint(cv,t,a,b,'t16_haicot',s=1.15,z0=1.0,z1=1.1,mist=0)
    lb(cv,c,'Toàn thư, Cương mục',620,215,t,a+.3,b,col=INK,sz=34);lb(cv,c,'người đời sau kể thêm',1360,215,t,a+.3,b,col=RED,sz=34)
    lb(cv,c,'tên Triệu Thị Trinh, núi Tùng, hai mươi ba tuổi: không có',960,100,t,a+.6,sb(20,1)-.2,col=INK,sz=36)
    lb(cv,c,'câu nói cưỡi cơn gió mạnh: dân gian kể thêm',960,100,t,sb(20,1)+.2,b,col=RED,sz=38)
# 21
def S_21(cv,t):
    a,b=T[21]-.3,E[21]+.3
    c=paint(cv,t,a,b,'t16_ke',s=1.15,z0=1.0,z1=1.12,mist=0)
    lb(cv,c,'có thể hiểu vì sao lại như vậy',960,160,t,a+.4,sb(21,1)-.2,col=INK,sz=42)
    lb(cv,c,'người đời sau kể tiếp phần sử còn bỏ trống',960,160,t,sb(21,1)+.2,sb(21,2)-.2,col=RED,sz=40)
    lb(cv,c,'điều sử chép thì vẫn chắc chắn',960,160,t,sb(21,2)+.2,b,col=INK,sz=42)
# 22
def S_22(cv,t):
    a=T[22]-.3
    c=paint(cv,t,a,E[22]+4,'t16_cuoi',s=1.0,y=560,dx=-300,z0=1.05,z1=1.0,mist=.3)
    flock(cv,c,t,.5)
    tx=text('Bà Triệu, năm 248',54,INK,700);put_screen(cv,wipe(tx,inn(t,a+.8,1.4),0,.3,seed=13),W/2,170)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,245,inn(t,E[22]+.6,1))
MOV.update({
't16_voi1':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_viet',-100,720,500,720,t,a,b,s=.8),voi(cv,c,300,650,1500,650,t,a,b,s=.85),mv(cv,c,'t12_spr_chim',1700,180,500,140,t,a,b,s=1.0,o=.7)),
't16_trusoo':lambda cv,c,t,a,b:(clash(cv,c,t,a+1.0,b,'bac','viet',xm=960,y=800,s=.7,push=-1,seed=3),smoke(cv,c,1500,700,t)),
't16_so':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_dan',-100,800,700,800,t,a,b,s=.9),mv(cv,c,'t12_spr_chim',1700,170,400,140,t,a,b,s=1.0,o=.7)),
't16_luudai':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_bac',-200,800,300,800,t,a,b,s=.8),mv(cv,c,'t12_spr_bac',2100,800,1500,800,t,a,b,s=.8),smoke(cv,c,960,760,t)),
't16_sulien':lambda cv,c,t,a,b:(flick(cv,c,1360,760,t,s=.8),smoke(cv,c,1360,700,t,s=.8),[stroke(cv,c,[(700+i*180,880),(820+i*180,880)],inn(t,a+i*(b-a)/3,(b-a)/3),wid=6,col=RED,o=.6,head=False) for i in range(3)]),
't16_thu':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_nguoi',300,820,900,820,t,a,b,s=1.0),smoke(cv,c,1500,760,t),mv(cv,c,'t12_spr_chim',1700,120,400,100,t,a,b,s=1.0,o=.7)),
't16_chiemthanh':lambda cv,c,t,a,b:(clash(cv,c,t,a+.6,b,'bac','viet',xm=960,y=720,s=.8,push=-1,seed=5),flick(cv,c,1300,700,t,s=1.2),smoke(cv,c,1300,620,t,s=1.4)),
't16_lucdan':lambda cv,c,t,a,b:(mv(cv,c,'t16_spr_thuyenlon',100,790,1500,770,t,a,b,s=.9,bob=8),mv(cv,c,'t12_spr_nuoc',960,960,960,940,t,a,b,o=.4,bob=14)),
't16_rahang':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_dan',-100,800,1000,800,t,a,b,s=.9),mv(cv,c,'t12_spr_dan',-500,820,500,820,t,a,b,s=.8,o=.8)),
't16_bovukhi':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_dan',700,700,1900,700,t,a,b,s=.9),smoke(cv,c,2100,740,t,s=1.1),smoke(cv,c,2480,720,t+2,s=.9)),
't16_noilen':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_viet',-200,800,700,800,t,a,b,s=.9),mv(cv,c,'t12_spr_viet',2200,800,1300,800,t,a,b,s=.9)),
't16_voi2':lambda cv,c,t,a,b:(clash(cv,c,t,a+.5,b,'bac','viet',xm=760,y=720,s=.75,push=0,seed=7),voi(cv,c,2000,650,1250,650,t,a,b,s=.85)),
't16_dep':lambda cv,c,t,a,b:(clash(cv,c,t,a+.4,b,'viet','bac',xm=900,y=720,s=.75,push=-1,seed=9),mv(cv,c,'t12_spr_chim',1700,180,400,140,t,a,b,s=1.0,o=.7)),
't16_thutu':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_dan',900,800,-100,800,t,a,b,s=.9,o=.85),voi(cv,c,2200,735,1350,735,t,a,b,s=.8)),
't16_den':lambda cv,c,t,a,b:(smoke(cv,c,960,640,t,s=1.2),mv(cv,c,'t12_spr_dan',-100,830,700,830,t,a,b,s=.8),mv(cv,c,'t12_spr_chim',1700,200,400,160,t,a,b,s=1.0,o=.7)),
't16_sunguyen':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_chim',1700,200,300,140,t,a,b,s=1.0,o=.7),mv(cv,c,'t12_spr_nguoi',1900,820,1250,820,t,a,b,s=1.0),smoke(cv,c,980,640,t,s=.8),[stroke(cv,c,[(760+i*140,900),(860+i*140,900)],inn(t,a+i*(b-a)/3,(b-a)/3),wid=6,col=RED,o=.6,head=False) for i in range(3)]),
't16_sachtong':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_nguoi',200,820,1000,820,t,a,b,s=1.0),smoke(cv,c,1600,760,t,s=.9)),
't16_hoangduong':lambda cv,c,t,a,b:(smoke(cv,c,700,700,t,s=1.2),smoke(cv,c,1250,700,t+1.5,s=1.2),[stroke(cv,c,[(520+i*300,300+i*40),(740+i*300,420+i*40)],inn(t,a+i*(b-a)/4,(b-a)/4),wid=8,col=RED,o=.65,head=False) for i in range(3)]),
't16_haicot':lambda cv,c,t,a,b:(smoke(cv,c,1550,780,t,s=1.2),[stroke(cv,c,[(1020,330+i*130),(1620,330+i*130)],inn(t,a+i*(b-a)/4,(b-a)/4),wid=6,col=RED,o=.55,head=False) for i in range(3)]),
't16_ke':lambda cv,c,t,a,b:(flick(cv,c,960,800,t,s=1.0),smoke(cv,c,960,720,t,s=1.0),smoke(cv,c,1520,640,t+1,s=.8)),
't16_cuoi':lambda cv,c,t,a,b:(voi(cv,c,100,650,1700,650,t,a,E[22]+3,s=.85,k=1),mv(cv,c,'t12_spr_chim',1600,200,400,160,t,a,b,s=1.1,o=.8)),
})
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
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
            if a-.3<t<b+.35: caption(cv,h,inn(t,a-.25,.25)*(1-inn(t,b+.05,.25)),False)
if FREEZE:
    def caps(cv,t): pass
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
