# Bản dài tm7: Tốt Động, Chúc Động 1426 (bộ tranh riêng t7_*)
import math
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from fx_tran import arrows,dust,sparks,fall
from dai_tm2 import big,tagfall,strike,lb
from dai_tm3 import night
V=K.setup('tm7',{5:4.0,8:2.6,11:2.6,15:2.6,19:2.6,22:2.6})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
P=PTS
CARDS={8:'Ba đường quân',11:'Mấy tên do thám',15:'Im lặng',19:'Phục binh',22:'Thành Đông Quan'}
def field(cv,c,o=1.0,y=520,s=.75): put(cv,c,'t7_ruong',1400,y,ay=.5,s=s,o=o)
def S_1(cv,t):
    c=cam(*cpath(t,[(0,(960,560,1.15)),(E[1]+.3,(960,540,1.0))]))
    if t<1.4: u=eo(t/1.3);put_screen(cv,A('blot'),W/2,H/2,(1-u)*.85,s=1.9*(1+u*.9))
    put(cv,c,'mist',960,560,s=3.2,o=.7);put(cv,c,'t7_sung',960,500,s=1.4)
    big(cv,'BIẾT TRƯỚC ÁM HIỆU CỦA GIẶC?',t,.25,E[1]+.3,RED,170,72,seed=1)
def S_2(cv,t):
    a,b=T[2],E[2]
    c=cam(*cpath(t,[(a-.3,(1400,560,1.25)),(b+.3,(1400,540,1.1))]))
    field(cv,c)
    big(cv,'HỌ NẰM IM',t,mid(2,.2),b+.3,INK,200,80,seed=2)
    lb(cv,c,'giữa một vùng ruộng lầy',1400,430,t,mid(2,.5),b+.3,sz=36)
def S_3(cv,t):
    a,b=T[3],E[3]
    c=cam(*cpath(t,[(a-.3,(1400,560,1.1)),(b+.3,(1300,580,1.2))]))
    field(cv,c,.8)
    put(cv,c,'t7_minh',lerp(2100,1500,inn(t,a,b-a)),660,ay=1,s=.6)
    lb(cv,c,'mấy vạn quân nhà Minh',1500,330,t,a+.3,mid(3,.5),col=RED,sz=40)
    big(cv,'TỐT ĐỘNG · CHÚC ĐỘNG',t,mid(3,.45),b+.3,INK,170,64,seed=3)
def S_4(cv,t):
    a,b=T[4],E[4]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'t7_dothaam',560,640,s=.6,o=inn(t,mid(4,.45),.5))
    put(cv,c,'t7_sung',1400,600,s=.75,o=inn(t,mid(4,.75),.5))
    lb(cv,c,'mấy tên do thám bị bắt',560,380,t,mid(4,.45),b+.3,sz=36)
    lb(cv,c,'một tiếng súng hiệu',1400,380,t,mid(4,.75),b+.3,col=RED,sz=36)
    big(cv,'VÌ SAO IM LẶNG LẠI THẮNG?',t,a+.2,mid(4,.45),RED,170,64,seed=4)
def S_map(cv,t):
    keys=[(T[5]-.5,(520,660,1.5)),(E[5],(500,700,1.5)),(T[6]-.5,(500,760,1.4)),(E[6],(480,780,1.4)),(T[7]-.5,(440,620,3.0)),(E[7],(440,620,3.0)),(T[22]-.5,(460,760,1.5)),(E[22],(460,700,1.6))]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z)
    c=cam(cx,cy,z)
    mapbg(cv,c,u=inn(t,T[5]-1.0,1.4))
    tl,th,na,td,ls=[P[k] for k in ['thanglong','thanhhoa','nghean','totdong','langson2']]
    sz=28 if z<2 else 22
    dot(cv,c,*tl,o=1);tag(cv,c,tl[0]+12,tl[1]+26,'Đông Quan',dy=0,sz=sz)
    if t<T[6]:
        seal(cv,'s1407',380,260,T[5]+.2,t,s=.7,r=-4)
        stroke(cv,c,[(640,120),ls,(500,520),tl],inn(t,T[5]+.3,1.6),wid=8,col=RED)
        dot(cv,c,th[0]-20,th[1]-20,o=inn(t,mid(5,.55),.4),col=INK);lb(cv,c,'Lê Lợi · Lam Sơn',th[0]-120,th[1]-50,t,mid(5,.55),E[5]+.3,sz=sz)
        seal(cv,'s1418',th[0]+180,th[1]-90,mid(5,.6),t,s=.5,r=4)
    elif t<T[8]:
        if t<T[7]:
            stroke(cv,c,[(th[0]-20,th[1]-20),(na[0]+10,na[1]-60),(na[0],na[1]+20)],inn(t,mid(6,.4),1.6),wid=10,col=INK,o=.7)
            lb(cv,c,'làm chủ từ Nghệ An trở vào',na[0]+220,na[1]-120,t,mid(6,.5),E[6]+.3,sz=sz)
        else:
            stroke(cv,c,[(td[0]-30,td[1]+30),(tl[0]-6,tl[1]+10)],inn(t,T[7]+.2,1.2),wid=5,col=INK)
            lb(cv,c,'Lý Triện, Đỗ Bí',td[0]-20,td[1]+60,t,T[7]+.3,E[7]+.3,sz=sz)
            stroke(cv,c,[(tl[0]+40,tl[1]-80),(tl[0]+6,tl[1]-6)],inn(t,mid(7,.5),1),wid=5,col=RED)
            lb(cv,c,'Vương Thông, năm vạn quân',tl[0]+60,tl[1]-100,t,mid(7,.55),E[7]+.3,col=RED,sz=sz)
    else:
        stroke(cv,c,[(na[0],na[1]),(th[0]-10,th[1]-40),(tl[0]-10,tl[1]+60)],inn(t,T[22]+.2,2),wid=9,col=INK)
        lb(cv,c,'Lê Lợi kéo đại quân ra bắc',th[0]+190,th[1]-60,t,T[22]+.3,E[22]+.3,sz=sz)
        if t>mid(22,.55):
            for k in range(10):
                a_=k/10*6.28;dot(cv,c,tl[0]+30*math.cos(a_),tl[1]+30*math.sin(a_),o=inn(t,mid(22,.55)+k*.05,.3),r=5)
def S_6(cv,t):
    a,b=T[6],E[6]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(b+.3,(1200,520,1.08))]))
    put(cv,c,'t7_lamson',1400,480,ay=.5,s=.75)
    put(cv,c,'mist',1300,700,s=3.5,o=.85)
    for i in range(6): put(cv,c,Af('fig_giap_giao'),lerp(1800,1300,inn(t,a,b-a))+i*80,760,ay=1,s=.55,o=.9)
    lb(cv,c,'nhiều lần bị vây, phải rút lên núi',1300,260,t,a+.3,mid(6,.5),sz=38)
def S_8(cv,t):
    a,b=T[8],E[8]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.05)),(b+.3,(1400,560,1.12))]))
    put(cv,c,'t7_dongquan',1400,420,ay=.5,s=.75)
    for k,x0 in enumerate([1080,1400,1720]):
        u=inn(t,a+.4+k*.3,b-a-.6)
        put(cv,c,'t7_minh',x0+(x0-1400)*u*.9,620+u*200,ay=1,s=.28+.08*u,o=inn(t,a+.4+k*.3,.3))
    lb(cv,c,'chia ba đường',1400,260,t,a+.3,b+.3,col=RED,sz=44)
def S_9(cv,t):
    a,b=T[9],E[10];tc=mid(10,.2)
    sh=fio(t,tc,mid(10,.7))
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(T[10],(1000,580,1.08)),(b+.3,(900,600,1.12))]),sx=4*math.sin(t*23)*sh,sy=3*math.sin(t*19)*sh)
    put(cv,c,'t7_cau',960,520,s=1.0)
    for i in range(6):
        x=lerp(1400,700,inn(t,a+.2,2.5))+i*70;x=lerp(x,x+500,inn(t,mid(9,.55),2))
        put(cv,c,Af('fig_giap_giao') if t<mid(9,.55) else 'fig_giap_giao',x,700+(i%2)*12,ay=1,s=.42)
    lb(cv,c,'cầu Tam La',960,260,t,a+.3,mid(9,.5),sz=40)
    if t>mid(9,.6): put(cv,c,'t7_chong',1500,720,ay=1,s=.55,o=inn(t,mid(9,.6),.5));lb(cv,c,'hàng rào chông tre',1500,330,t,mid(9,.65),E[9]+.3,col=RED,sz=36)
    if t>T[10]-.2:
        put(cv,c,'t7_chong',1500,720,ay=1,s=.55)
        for i in range(2):
            x=lerp(1300,700,inn(t,tc+i*.3,2.5))+i*220
            put(cv,c,Af('voi'),x,760,ay=1,s=.55,r=math.sin(t*6+i)*4)
            dust(cv,c,x+180,740,o=.35)
        lb(cv,c,'voi chiến quay đầu chạy loạn',960,260,t,T[10]+.2,mid(10,.6),col=RED,sz=40)
        big(cv,'SẮP BỊ NGHIỀN NÁT?',t,mid(10,.6),b+.3,RED,170,64,seed=10)
def S_11(cv,t):
    a,b=T[11],E[11]
    c=cam(*cpath(t,[(a-.3,(1300,560,1.0)),(b+.3,(1100,580,1.06))]))
    field(cv,c,.6)
    for i in range(2): put(cv,c,'voi',lerp(-200,600,inn(t,a,b-a))+i*260,760,ay=1,s=.55)
    for i in range(8): put(cv,c,'fig_giap_giao',lerp(-500,300,inn(t,a,b-a))+i*70,770,ay=1,s=.42)
    tagfall(cv,c,700,420,'Đinh Lễ, Nguyễn Xí',t,a+.3,sz=40,col=INK)
    lb(cv,c,'ba nghìn quân, hai con voi',700,500,t,mid(11,.4),b+.3,sz=32)
    lb(cv,c,'vẫn ít hơn giặc nhiều lần',1500,300,t,mid(11,.6),b+.3,col=RED,sz=36)
def S_12(cv,t):
    a,b=T[12],E[12]
    c=cam(*cpath(t,[(a-.3,(960,540,1.0)),(b+.3,(960,560,1.1))]))
    put(cv,c,'t7_tra',960,520,s=.95)
    lb(cv,c,'bắt được do thám của giặc',960,260,t,a+.3,mid(12,.5),sz=40)
    lb(cv,c,'kế hoạch lộ ra hết',960,260,t,mid(12,.55),b+.3,col=RED,sz=44)
def S_13(cv,t):
    a,b=T[13],E[13]
    c=cam(960,560,1.0)
    put_screen(cv,band(1500,760,PAPER,.6,40),W/2,520)
    stroke(cv,c,[(300,640),(1600,640)],1,wid=14,head=False,col=np.float32([.35,.32,.28]),o=.5)
    lb(cv,c,'sông',300,600,t,a,b+.3,sz=28)
    stroke(cv,c,[(1500,300),(1000,560),(700,700)],inn(t,a+.3,2),wid=10,col=RED)
    lb(cv,c,'quân chính vượt sông đánh thẳng',1300,260,t,a+.4,b+.3,col=RED,sz=34)
    stroke(cv,c,[(1500,300),(1700,520),(1300,820),(800,800)],inn(t,mid(13,.5),2),wid=8,col=RED,dash=14)
    lb(cv,c,'một cánh lén vòng ra sau',1500,850,t,mid(13,.55),b+.3,col=RED,sz=34)
    put(cv,c,'fig_giap_giao',700,740,ay=1,s=.6)
def S_14(cv,t):
    a,b=T[14],E[14]
    c=cam(960,560,1.0+.04*(t-a))
    put(cv,c,'mist',960,560,s=3.2,o=.5);put(cv,c,'t7_sung',960,600,s=1.3)
    if t>a+.5:
        for k in range(3):
            r=(t-a-.5-k*.5)%1.6
            stroke(cv,c,[(1170+r*300*math.cos(q/8*6.28),370+r*200*math.sin(q/8*6.28)) for q in range(9)],1,wid=3,head=False,o=.5*(1-r/1.6)) if r>0 else None
    big(cv,'ÁM HIỆU LÀ TIẾNG SÚNG',t,a+.3,mid(14,.5),RED,160,70,seed=14)
    big(cv,'THỨ ĐẦU TIÊN',t,mid(14,.55),b+.3,INK,160,70,seed=15)
def S_15(cv,t):
    a,b=T[15],E[16]
    c=cam(*cpath(t,[(a-.3,(1400,560,1.0)),(T[16],(1400,600,1.1)),(b+.3,(1500,620,1.2))]))
    field(cv,c,.7,480)
    put(cv,c,'t7_phuc',1400,720,ay=.5,s=.7,o=inn(t,T[16]-.3,.8))
    big(cv,'KHÔNG MỘT TIẾNG ĐỘNG',t,a+.3,E[15]+.3,INK,170,70,seed=16)
    lb(cv,c,'Tốt Động',600,360,t,T[16]+.2,b+.3,col=RED,sz=40);lb(cv,c,'Chúc Động',2200,360,t,T[16]+.4,b+.3,col=RED,sz=40)
    big(cv,'THỨ HAI: SỰ IM LẶNG',t,mid(16,.6),b+.3,RED,170,64,seed=17)
def S_17(cv,t):
    a,b=T[17],E[18]
    c=cam(*cpath(t,[(a-.3,(1600,560,1.05)),(T[18],(1400,580,1.1)),(b+.3,(1200,600,1.15))]))
    field(cv,c,.9)
    for r in range(3):
        x=lerp(2400,1100+r*150,inn(t,a+r*.3,b-a))
        put(cv,c,'t7_minh',x,640+r*60,ay=1,s=.45-.04*r,o=.95-.2*r)
    lb(cv,c,'không nghe súng nổ',1500,260,t,a+.3,mid(17,.5),sz=38)
    lb(cv,c,'đi tắt cho nhanh',1500,260,t,mid(17,.55),E[17]+.3,col=RED,sz=40)
    lb(cv,c,'chung quanh vẫn im phăng phắc',1300,260,t,mid(18,.4),b+.3,sz=38)
def S_19(cv,t):
    a,b=T[19],E[21];tc=T[19]+.3
    sh=fio(t,tc,E[20])
    c=cam(*cpath(t,[(a-.3,(1400,560,1.1)),(T[20],(1300,600,1.12)),(b+.3,(1200,600,1.15))]),sx=5*math.sin(t*23)*sh,sy=4*math.sin(t*19)*sh)
    field(cv,c,.9)
    for r in range(3):
        x=1300+r*150+lerp(0,-250,inn(t,tc,3))
        put(cv,c,'t7_minh',x,640+r*60,ay=1,s=.45-.04*r,o=(.95-.2*r)*(1-.5*inn(t,T[20],2)))
    for side in (-1,1):
        for i in range(9):
            st=tc+i*.1;u=inn(t,st,1.8)
            x=lerp(500,1000,u)-i*45 if side<0 else lerp(2300,1800,u)+i*45
            put(cv,c,'fig_giap_giao' if side<0 else Af('fig_giap_giao'),x,700+(i%2)*14,ay=1,s=.45,o=inn(t,st,.3))
    arrows(cv,c,t,tc,E[20],[(800+k*60,640) for k in range(4)]+[(2000-k*60,640) for k in range(4)],[(1300+k*100,560) for k in range(6)],n=18,h=110,per=.9,seed=19)
    sparks(cv,c,t,[(1250+k*140,580) for k in range(4)],tc+.4,E[20],seed=19)
    for k in range(4): put(cv,c,'splash',1100+k*200,700,s=.45,o=.5*fio(t,mid(19,.6)+k*.3,mid(19,.6)+k*.3+1.2))
    lb(cv,c,'phục binh ập ra',1400,260,t,tc,mid(19,.5),col=RED,sz=44)
    lb(cv,c,'dồn chạy về phía sông',1400,260,t,mid(19,.55),E[19]+.3,sz=40)
    if t>T[20]-.2:
        lb(cv,c,'sử ta: mấy vạn chết và bị bắt',1100,230,t,T[20]+.2,E[20]+.3,col=RED,sz=34)
        lb(cv,c,'sử nhà Minh: hai, ba vạn chết',1700,300,t,mid(20,.5),E[20]+.3,sz=34)
    if t>T[21]-.2:
        tagfall(cv,c,1200,330,'Trần Hiệp',t,T[21]+.2,fall=mid(21,.6),sz=40,col=RED)
        tagfall(cv,c,1600,330,'Lý Lượng',t,T[21]+.4,fall=mid(21,.65),sz=40,col=RED)
        lb(cv,c,'Vương Thông bị thương, chạy về Đông Quan',1400,200,t,mid(21,.5),b+.3,sz=34)
def S_23(cv,t):
    a,b=T[23],E[23]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(b+.3,(1400,500,1.12))]))
    put(cv,c,'t7_dongquan',1400,420,ay=.5,s=.75)
    for i in range(14):
        x=500+i*130;put(cv,c,'fig_giap_giao',x,700+(i%2)*10,ay=1,s=.35,o=inn(t,a+.2+i*.05,.3))
    night(cv,.3)
    lb(cv,c,'sang để giữ đất',1400,260,t,a+.3,mid(23,.5),sz=40)
    big(cv,'BỊ NHỐT TRONG THÀNH MÌNH GIỮ',t,mid(23,.5),b+.3,RED,170,60,seed=23)
def S_end(cv,t):
    a=T[24]
    c=cam(960,560,1.0+.015*(t-a))
    field(cv,c,.7,480);put(cv,c,'sun',1600,360,o=.45,k=.2);flock(cv,c,t,.6)
    put(cv,c,'t7_sungbun',960,640,s=.9)
    tx=text('Tiếng súng hiệu không bao giờ nổ',62,INK,700);put_screen(cv,wipe(tx,inn(t,a+.3,1.2),0,.3,seed=13),W/2,230)
    seal(cv,'stitle7',W/2,430,mid(24,.5),t,s=.55,r=3)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,H-80,inn(t,E[24]+.5,1))
S=lambda n:T[n]-.3
SH=[(0,S(2),S_1),(S(2),S(3),S_2),(S(3),S(4),S_3),(S(4),S(5),S_4),(S(5),S(6),S_map),(S(6),S(7),S_6),(S(7),S(8),S_map),(S(8),S(9),S_8),
 (S(9),S(11),S_9),(S(11),S(12),S_11),(S(12),S(13),S_12),(S(13),S(14),S_13),(S(14),S(15),S_14),(S(15),S(17),S_15),(S(17),S(19),S_17),
 (S(19),S(22),S_19),(S(22),S(23),S_map),(S(23),S(24),S_23),(S(24),V.TOTAL+1,S_end)]
def ov(cv,t):
    if T[5]-4.2<t<T[5]+.2: title(cv,t,T[5]-3.6,'TỐT ĐỘNG · CHÚC ĐỘNG','stitle7',.55)
def frame(t): return K.compose(V,SH,t,ov,CARDS)
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
