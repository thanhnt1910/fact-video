# Bản dài tm13: Hai Bà Trưng, Lãng Bạc và Cấm Khê (bộ tranh riêng t13_*, mỗi tranh một cảnh, cảnh nào cũng chuyển động)
import math,re,json,os
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from fx_tran import arrows,dust,sparks,fall
from tran_fx import clash
from dai_tm2 import big,tagfall,strike,lb
V=K.setup('tm13',{4:4.0})
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
def paint(cv,t,a,b,name,**kw):
    c=paint_(cv,t,a,b,name,**kw)
    if name in MOV: MOV[name](cv,c,t,a,b)
    return c

def pulse(cv,c,x,y,t,col=RED):
    for k in range(2):
        u=((t*.6+k*.5)%1.0);dot(cv,c,x,y,o=.6*(1-u),col=col,r=int(8+40*u))
# 1
def S_1(cv,t):
    a,b=0,E[1]+.3
    c=paint(cv,t,a,b,'t13_chay',s=1.12,dx=-360,z0=1.12,z1=1.0,mist=.2)
    for i in range(6): dust(cv,c,1000-i*60-(t*260)%200,880+(i%2)*20,o=.28,s=.3+.04*i)
    flock(cv,c,t,.6)
    big(cv,'THÁI THÚ BỎ CHẠY',t,.25,3.2,RED,150,84,seed=1)
    big(cv,'VÌ HAI NGƯỜI PHỤ NỮ',t,3.3,b,INK,150,84,seed=2)
# 2a
def S_2a(cv,t):
    a,b=T[2]-.3,sb(2,1)
    c=paint(cv,t,a,b,'t13_phu',s=1.15,z0=1.0,z1=1.12,dx=120)
    lb(cv,c,'Tô Định, thái thú quận Giao Chỉ',960,170,t,a+.6,b-.3,col=RED,sz=42)
    lb(cv,c,'nhà Hán cai trị hơn 140 năm',960,225,t,b-4.5,b-.3,col=INK,sz=34)
# 2b bản đồ
def S_2b(cv,t):
    a,b=sb(2,1),E[2]+.3
    dl,th,ng,lc=P['daila'],P['thanhhoa'],P['nghean'],P['liemchau']
    c=mcam(t,[(a-.3,(520,640,1.5)),(a+3,(700,760,1.0)),(b,(900,640,.95))])
    mapbg(cv,c,u=inn(t,a-.4,1.2))
    dot(cv,c,*dl);tag(cv,c,dl[0]+24,dl[1]-6,'Mê Linh',dy=0,sz=26);pulse(cv,c,*dl,t)
    lb(cv,c,'Trưng Trắc và Trưng Nhị',dl[0]+300,dl[1]-90,t,a+.2,sb(2,2)-.2,col=RED,sz=32)
    k=0
    for nm,p,t0 in (('Cửu Chân',th,sb(2,2)+.6),('Nhật Nam',ng,sb(2,2)+1.5),('Hợp Phố',lc,sb(2,2)+2.4)):
        if t>t0: dot(cv,c,*p,o=inn(t,t0,.3));tag(cv,c,p[0]+22,p[1]-6,nm,dy=0,sz=26);stroke(cv,c,[dl,p],inn(t,t0,1.2),wid=5,col=RED,o=.8)
    if t>sb(2,2)+3:
        n65=int(65*inn(t,sb(2,2)+3,2.5));rg=np.random.default_rng(2)
        for i in range(n65):
            p=(dl[0]+60+rg.random()*900,dl[1]-120+rg.random()*400-(i%3)*10);dot(cv,c,p[0],p[1],o=.8,col=RED,r=6)
        lb(cv,c,'sáu mươi lăm thành đáp lại',1100,260,t,sb(2,2)+3.2,b,col=RED,sz=42)
# 3
def S_3(cv,t):
    a,b=T[3]-.3,E[3]+.3
    c=paint(cv,t,a,b,'t13_tat',s=1.15,z0=1.02,z1=1.14)
    lb(cv,c,'ba năm sau',960,170,t,a+.4,sb(3,1)-.2,col=RED,sz=48)
    lb(cv,c,'vì sao không giữ nổi?',960,170,t,sb(3,1)+.2,b,col=INK,sz=46)
    seal(cv,'s43',1500,330,sb(3,1)-1.5,t,s=.8,r=4)
# 4
def S_4(cv,t):
    a,b=T[4]-.3,E[4]+.3
    c=paint(cv,t,a,b,'t13_lang',s=1.15,dx=-200,z0=1.0,z1=1.1,mist=.3)
    lb(cv,c,'Mê Linh, nhà Trưng Trắc',700,200,t,a+.5,sb(4,1)-.2,col=INK,sz=38)
    lb(cv,c,'Chu Diên, nhà Thi Sách',1380,200,t,a+3.6,sb(4,1)-.2,col=INK,sz=38)
    lb(cv,c,'luật nhà Hán trói buộc dân, Thi Sách bị giết',960,170,t,sb(4,1)+.2,sb(4,2)-.2,col=RED,sz=40)
    if t>sb(4,1)+1: stroke(cv,c,[(300,780),(900,740),(1600,780)],inn(t,sb(4,1)+1,3),wid=7,col=RED,o=.8)
    lb(cv,c,'Trưng Trắc tìm cách trả thù',960,170,t,sb(4,2)+.1,b,col=RED,sz=44)
# 5
def S_5(cv,t):
    a,b=T[5]-.3,E[5]+.3
    c=paint(cv,t,a,b,'t13_hoi',s=1.1,z0=1.0,z1=1.15,dy=-40,mist=.2)
    seal(cv,'s40',1500,300,a+.3,t,s=.8,r=-4)
    lb(cv,c,'mùa xuân năm bốn mươi',960,160,t,a+.5,sb(5,1)-.2,col=RED,sz=44)
    lb(cv,c,'chiếm trụ sở của quan nhà Hán',960,160,t,sb(5,1)+.2,sb(5,1)+4,col=INK,sz=40)
    if t>sb(5,1)+4: lb(cv,c,'Tô Định chạy về Nam Hải',960,160,t,sb(5,1)+4.2,b,col=RED,sz=42)
# 6
def S_6(cv,t):
    a,b=T[6]-.3,E[6]+.3
    c=paint(cv,t,a,b,'t13_troi',s=1.15,dx=-420,z0=1.05,z1=1.0)
    lb(cv,c,'tưởng là một mối thù riêng',960,170,t,a+.3,sb(6,1)-.2,col=INK,sz=44)
    lb(cv,c,'nhưng dân Giao Chỉ cùng bị trói buộc',960,170,t,sb(6,1)+.2,b,col=RED,sz=42)
    if t>sb(6,1): 
        for i in range(8): stroke(cv,c,[(420+i*150,820),(500+i*150,830)],inn(t,sb(6,1)+.3+i*.3,.6),wid=5,col=RED,o=.7)
# 7
def S_7(cv,t):
    a,b=T[7]-.3,E[7]+.3
    c=paint(cv,t,a,b,'t13_trieu',s=1.15,dx=160,z0=1.0,z1=1.12)
    lb(cv,c,'Lạc Dương, kinh đô nhà Hán',960,170,t,a+.4,sb(7,1)-.2,col=INK,sz=42)
    seal(cv,'s42',1500,320,sb(7,1)+1.5,t,s=.8,r=4)
    lb(cv,c,'năm bốn mươi hai: cử Mã Viện',960,170,t,sb(7,1)+.2,b,col=RED,sz=42)
# 8a,b
def S_8a(cv,t):
    a,b=T[8]-.3,sb(8,1)
    c=paint(cv,t,a,b,'t13_vien',s=1.0,y=540,dx=-260,z0=1.0,z1=1.14,mist=.35)
    lb(cv,c,'Mã Viện, Phục Ba tướng quân',960,170,t,a+.4,b-.2,col=RED,sz=44)
def S_8b(cv,t):
    a,b=sb(8,1),sb(8,2)
    c=paint(cv,t,a,b,'t13_thuyenluong',s=1.0,y=560,dx=-500,z0=1.1,z1=1.0,mist=.3)
    lb(cv,c,'thuyền chở lương theo bờ biển',960,170,t,a+.3,b-.2,col=INK,sz=42)
def S_8c(cv,t):
    a,b=sb(8,2),E[8]+.3
    c=cam(960,540,1.0+.04*cl((t-a)/(b-a)))
    mapbg(cv,c,u=1)
    dl=P['daila'];dot(cv,c,*dl);tag(cv,c,dl[0]+24,dl[1]-6,'Mê Linh',dy=0,sz=28)
    lb(cv,c,'sử không ghi quân hai bà đông bao nhiêu',960,200,t,a+.3,b,col=RED,sz=42)
    stroke(cv,c,[(1500,300),(900,420),dl],inn(t,a+.5,max(b-a-1,1)),wid=8,col=INK);pulse(cv,c,*dl,t)
# 9
def S_9a(cv,t):
    a,b=T[9]-.3,sb(9,1)
    c=paint(cv,t,a,b,'t13_langbac',s=1.0,y=560,dx=-380,z0=1.0,z1=1.15,mist=.15)
    lb(cv,c,'Lãng Bạc',960,170,t,a+.3,b-.2,col=RED,sz=52)
    lb(cv,c,'sách cũ: Hồ Tây; nay: vùng núi Tiên Du',960,235,t,a+2.2,b-.2,col=INK,sz=32)
    lb(cv,c,'quân nhà Hán',450,300,t,a+.6,b,col=(.17,.29,.45),sz=36)
    lb(cv,c,'quân hai bà',1500,300,t,a+.6,b,col=RED,sz=36)
def S_9b(cv,t):
    a,b=sb(9,1),E[9]+.3
    c=paint(cv,t,a,b,'t13_hang',s=1.15,dx=250,z0=1.0,z1=1.12,mist=.2)
    lb(cv,c,'Mã Viện thắng lớn',960,160,t,a+.3,sb(9,2)-.2,col=RED,sz=46)
    lb(cv,c,'quân nhà Hán',1500,330,t,a+.5,b,col=(.17,.29,.45),sz=32);lb(cv,c,'quân hai bà ra hàng',600,330,t,a+.5,b,col=RED,sz=32)
    lb(cv,c,'hàng nghìn người ngã xuống, hơn mười nghìn người hàng',960,160,t,sb(9,2)+.2,sb(9,3)-.2,col=INK,sz=38)
    lb(cv,c,'hai bà lui về Cấm Khê',960,160,t,sb(9,3)+.1,b,col=RED,sz=44)
# 10
def S_10(cv,t):
    a,b=T[10]-.3,E[10]+.3
    c=paint(cv,t,a,b,'t13_roi',s=1.0,y=560,dx=-500,z0=1.1,z1=1.0)
    lb(cv,c,'nhiều người bỏ đi',960,170,t,a+.5,b,col=RED,sz=46)
    lb(cv,c,'theo lời kể của Toàn thư',960,230,t,a+2,b,col=INK,sz=34)
# 11
def S_11(cv,t):
    a,b=T[11]-.3,E[11]+.3
    c=paint(cv,t,a,b,'t13_camkhe',s=1.0,y=540,dx=300,z0=1.0,z1=1.2,mist=.4)
    lb(cv,c,'Cấm Khê, chưa rõ ở đâu',960,170,t,a+.3,sb(11,1)-.2,col=INK,sz=44)
    lb(cv,c,'quân hai bà',1120,430,t,a+.6,b,col=RED,sz=32);lb(cv,c,'quân Mã Viện',700,560,t,a+.6,b,col=(.17,.29,.45),sz=32)
    lb(cv,c,'Mã Viện đuổi theo, đánh nhiều trận',960,170,t,sb(11,1)+.2,sb(11,2)-.2,col=RED,sz=40)
    seal(cv,'s43',1500,300,sb(11,2)-.2,t,s=.8,r=4)
    lb(cv,c,'năm bốn mươi ba: bị cô lập, thất bại',960,170,t,sb(11,2)+.2,b,col=RED,sz=40)
# 12
def S_12a(cv,t):
    a,b=T[12]-.3,sb(12,4)
    c=paint(cv,t,a,b,'t13_sach',s=1.15,dx=-120,z0=1.0,z1=1.1,mist=0)
    lb(cv,c,'sách kể khác nhau',960,150,t,a+.3,sb(12,1)-.2,col=RED,sz=46)
    lb(cv,c,'Hậu Hán thư: bị chém, đầu gửi về Lạc Dương',960,150,t,sb(12,1)+.2,sb(12,2)-.2,col=INK,sz=38)
    lb(cv,c,'Toàn thư: chỉ ghi hai bà thua trận',960,150,t,sb(12,2)+.2,sb(12,3)-.2,col=INK,sz=38)
def S_12b(cv,t):
    a,b=sb(12,3),E[12]+.3
    c=paint(cv,t,a,b,'t13_hat',s=1.0,y=540,dx=-300,z0=1.05,z1=1.0)
    lb(cv,c,'sông Hát, đền Hát Môn: chuyện dân gian giữ lại',960,170,t,a+.3,sb(12,4)-.2,col=INK,sz=40)
    lb(cv,c,'cách kể nào cũng không thay được cách kể khác',960,170,t,sb(12,4)+.2,b,col=RED,sz=40)
# 13
def S_13a(cv,t):
    a,b=T[13]-.3,sb(13,1)+0.01*0+ (E[13]-T[13])*.45+T[13]-T[13]
    b=T[13]+(E[13]-T[13])*.5
    c=paint(cv,t,a,b,'t13_lo',s=1.15,dx=-100,z0=1.0,z1=1.14,mist=.15)
    lb(cv,c,'nấu chảy trống đồng',960,160,t,a+.4,b-.2,col=RED,sz=48)
    lb(cv,c,'biểu tượng quyền của thủ lĩnh người bản địa',960,220,t,a+2.5,b-.2,col=INK,sz=34)
    for i in range(10): dust(cv,c,760+(i%3)*40,520-((t*70+i*60)%320),o=.3,s=.25)
def S_13b(cv,t):
    a=T[13]+(E[13]-T[13])*.5;b=E[13]+.3
    c=paint(cv,t,a,b,'t13_ngua',s=1.15,dx=200,z0=1.1,z1=1.0,mist=.2)
    lb(cv,c,'đúc thành tượng ngựa, dâng vua năm bốn mươi bốn',960,160,t,a+.3,b-3,col=INK,sz=38)
    seal(cv,'s44',1500,320,a+.8,t,s=.8,r=4)
    lb(cv,c,'quân Mã Viện chết gần một nửa vì hơi độc và dịch bệnh',960,160,t,b-3,b,col=RED,sz=36)
# 14
def S_14(cv,t):
    a,b=T[14]-.3,E[14]+.3
    c=paint(cv,t,a,b,'t13_thanh65',s=1.0,y=560,dx=-500,z0=1.05,z1=1.0,mist=.25)
    lb(cv,c,'sử không đưa ra một lý do duy nhất',960,170,t,sb(14,1)+.2,sb(14,2)-.2,col=INK,sz=42)
    lb(cv,c,'một đạo quân có thuyền chở lương theo bờ biển',960,170,t,sb(14,2)+.2,sb(14,3)-.2,col=RED,sz=38)
    lb(cv,c,'Lê Văn Hưu: sáu mươi lăm thành chỉ vì một tiếng gọi',960,170,t,sb(14,3)+.2,b,col=INK,sz=36)
    if t>sb(14,3): 
        for i in range(10): dot(cv,c,300+i*150,420-(i%2)*30,o=inn(t,sb(14,3)+i*.25,.3),col=RED,r=6)
# 15
def S_15(cv,t):
    a=T[15]-.3
    c=paint(cv,t,a,E[15]+4,'t13_cuoi',s=1.15,z0=1.0,z1=1.1,mist=.3)
    flock(cv,c,t,.5)
    tx=text('Hai Bà Trưng, năm 40 đến 43',54,INK,700);put_screen(cv,wipe(tx,inn(t,a+.8,1.4),0,.3,seed=13),W/2,170)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,245,inn(t,E[15]+.6,1))

MOV.update({
't13_chay':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_viet',100,860,600,860,t,a,b,s=.9),mv(cv,c,'t12_spr_bac',1300,860,1900,860,t,a,b,s=.8),mv(cv,c,'t12_spr_chim',1600,180,500,140,t,a,b,s=1.0,o=.7)),
't13_phu':lambda cv,c,t,a,b:(smoke(cv,c,1300,700,t),mv(cv,c,'t12_spr_bac',1500,880,1000,880,t,a,b,s=.9)),
't13_tat':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_chim',300,200,1600,160,t,a,b,s=1.1,o=.8),smoke(cv,c,960,760,t)),
't13_lang':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_dan',300,880,1100,880,t,a,b,s=.9),mv(cv,c,'t12_spr_chim',1700,200,500,160,t,a,b,s=1.0,o=.7)),
't13_hoi':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_viet',-100,860,700,840,t,a,b,s=1.0),mv(cv,c,'t12_spr_viet',2000,860,1300,840,t,a,b,s=1.0)),
't13_troi':lambda cv,c,t,a,b:mv(cv,c,'t12_spr_dan',200,900,900,900,t,a,b,s=1.0),
't13_trieu':lambda cv,c,t,a,b:(smoke(cv,c,750,740,t),smoke(cv,c,1170,740,t+3)),
't13_vien':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_bac',-200,860,900,860,t,a,b,s=1.0),mv(cv,c,'t12_spr_ngua',100,780,1000,780,t,a,b,s=.9)),
't13_thuyenluong':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_thuyen',200,760,1100,740,t,a,b,s=.9,bob=8),mv(cv,c,'t12_spr_nuoc',960,960,960,940,t,a,b,o=.4,bob=14)),
't13_langbac':lambda cv,c,t,a,b:clash(cv,c,t,a+.4,b,'bac','viet',push=1,seed=9,y=740,s=.8),
't13_hang':lambda cv,c,t,a,b:mv(cv,c,'t12_spr_dan',200,880,900,880,t,a,b,s=.9),
't13_roi':lambda cv,c,t,a,b:mv(cv,c,'t12_spr_viet',900,860,1800,820,t,a,b,s=.8,o=.75),
't13_camkhe':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_bac',700,880,1300,700,t,a,b,s=.8),mv(cv,c,'t12_spr_chim',1700,200,400,160,t,a,b,s=1.0,o=.7)),
't13_hat':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_thuyen',300,820,900,800,t,a,b,s=.7,bob=6),mv(cv,c,'t12_spr_nuoc',960,980,960,960,t,a,b,o=.4,bob=14)),
't13_sach':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_chim',1700,110,300,90,t,a,b,s=1.0,o=.7),[stroke(cv,c,[(170+i*630,900),(500+i*630,900)],inn(t,a+i*(b-a)/3,(b-a)/3),wid=6,col=RED,o=.7,head=False) for i in range(3)]),
't13_lo':lambda cv,c,t,a,b:(flick(cv,c,840,560,t,s=1.0),smoke(cv,c,840,380,t,s=1.3)),
't13_ngua':lambda cv,c,t,a,b:(smoke(cv,c,500,760,t),mv(cv,c,'t12_spr_chim',1700,200,400,160,t,a,b,s=1.0,o=.7)),
't13_thanh65':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_chim',300,180,1600,140,t,a,b,s=1.1,o=.8),mv(cv,c,'t12_spr_dan',200,900,900,900,t,a,b,s=.9)),
't13_cuoi':lambda cv,c,t,a,b:(mv(cv,c,'t12_spr_chim',1600,200,400,160,t,a,b,s=1.1,o=.8),mv(cv,c,'t12_spr_nuoc',960,980,960,960,t,a,b,o=.45,bob=14)),
})
if FREEZE:
    lb=lambda *a,**k:None
    seal=lambda *a,**k:None
    big=lambda *a,**k:None
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
            if a-.3<t<b+.35: caption(cv,h,inn(t,a-.25,.25)*(1-inn(t,b+.05,.25)),False)
if FREEZE:
    def caps(cv,t): pass
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
