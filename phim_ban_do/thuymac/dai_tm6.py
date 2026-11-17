# Bản dài tm6: Bạch Đằng 1288 (bộ tranh riêng t6_*, giọng Charon gốc)
import math
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from fx_tran import arrows,dust,sparks,fall
from dai_tm2 import big,tagfall,strike,lb
from dai_tm3 import night
V=K.setup('tm6',{5:4.0,8:2.6,14:2.6,19:2.6,25:2.6})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
P=PTS
CARDS={8:'Vân Đồn',14:'Kinh thành không lương',19:'Sông Bạch Đằng',25:'Đường về'}
def bob(t,i=0): return math.sin(t*1.3+i)*1.2
def sea(cv,c,t,wl,o=1.0):
    Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=PAP[Ys:]
    put(cv,c,'water',960,wl-24,ay=0,o=o)
    for i,yy in enumerate([wl+8,wl+90,wl+210]): put(cv,c,'wave',960-((t*(22+i*9))%200)+(i*77),yy,ay=.5,o=.45-.1*i)
def S_1(cv,t):
    c=cam(*cpath(t,[(0,(960,520,1.12)),(E[1]+.3,(960,540,1.0))]))
    if t<1.4: u=eo(t/1.3);put_screen(cv,A('blot'),W/2,H/2,(1-u)*.85,s=1.9*(1+u*.9))
    put(cv,c,'t6_hoi',960,470,s=.95)
    big(cv,'NĂM NAY ĐÁNH GIẶC NHÀN?',t,.25,E[1]+.3,RED,260,76,seed=1)
def S_2(cv,t):
    a,b=T[2],E[2]
    c=cam(*cpath(t,[(a-.3,(900,600,1.15)),(b+.3,(960,560,1.0))]))
    put(cv,c,'mist',1300,600,s=3,o=.6);put(cv,c,'t6_tuong',760,560,s=1.0)
    tagfall(cv,c,1400,330,'Trần Quốc Tuấn',t,a+.4,sz=48,col=INK)
    lb(cv,c,'Hưng Đạo Đại Vương',1400,410,t,a+.8,b+.3,sz=34)
    lb(cv,c,'hai lần đánh lui quân nhà Nguyên',1400,470,t,mid(2,.55),b+.3,col=RED,sz=32)
def S_3(cv,t):
    a,b=T[3],E[3]
    c=cam(960,560,1.0)
    panels=[('t6_benvang','kinh thành bỏ trống'),('t6_lang','lăng vua bị đào phá'),('t6_hamdoi','hạm đội trên sông')]
    for k,(nm,lbl) in enumerate(panels):
        tk=a+.2+k*(b-a)/3.2;o=inn(t,tk,.5)
        cx=320+k*640
        sub=PAP.copy();cc=cam(960,560,1.0);put(sub,cc,nm,960,540,s=.75 if k!=1 else .95)
        m=np.zeros((H,W,1),np.float32);m[:,int(cx-310):int(cx+310)]=o
        shift=int((960-cx));sub=np.roll(sub,-shift,axis=1)
        cv[:]=cv*(1-m)+sub*m
        put_screen(cv,text(lbl,32,RED if k==1 else INK,700,glow=3),cx,250,o)
    for k in (1,2): stroke(cv,c,[(k*640,180),(k*640+6,860)],inn(t,a+.2+k*(b-a)/3.2,.5),wid=5,head=False,o=.7)
def S_4(cv,t):
    a,b=T[4],E[4]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'t6_songcu',1450,600,s=.42,o=.8)
    put(cv,c,'t6_thuyenluong',480,600,s=.38,o=inn(t,mid(4,.5),.6))
    lb(cv,c,'một đoàn thuyền lương',500,380,t,mid(4,.5),b+.3,sz=36)
    lb(cv,c,'một con sông cũ',1300,380,t,mid(4,.7),b+.3,sz=36)
    big(cv,'LỜI TRẤN AN, HAY ĐÃ NHÌN THẤY ĐIỀU GÌ?',t,a+.2,mid(4,.5),RED,170,54,seed=4)
def S_map(cv,t):
    keys=[(T[5]-.5,(560,520,1.3)),(E[5],(560,520,1.3)),(T[17]-.5,(560,560,1.4)),(E[17],(560,560,1.4))]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z)
    c=cam(cx,cy,z)
    mapbg(cv,c,u=inn(t,T[5]-1.0,1.4))
    tl,ls,vd,bd=[P[k] for k in ['thanglong','langson2','vandon','bachdang']]
    dot(cv,c,*tl,o=1);tag(cv,c,tl[0]+12,tl[1]+30,'Thăng Long',dy=0,sz=28)
    if t<T[6]:
        seal(cv,'s1287',360,260,T[5]+.3,t,s=.7,r=-4)
        stroke(cv,c,[(640,150),ls,(500,520),tl],inn(t,mid(5,.4),2),wid=8,col=RED)
        lb(cv,c,'Thoát Hoan',720,330,t,mid(5,.45),E[5]+.3,col=RED,sz=30)
        stroke(cv,c,[(1100,500),(900,560),vd],inn(t,mid(5,.6),1.8),wid=7,col=RED,dash=10)
        lb(cv,c,'đường biển',980,470,t,mid(5,.65),E[5]+.3,col=RED,sz=28)
    else:
        stroke(cv,c,[tl,(500,520),ls,(640,150)],inn(t,T[17]+.2,2),wid=7,col=RED,dash=12)
        lb(cv,c,'quân bộ: đường Lạng Sơn',760,300,t,T[17]+.3,E[17]+.3,col=RED,sz=26)
        stroke(cv,c,[tl,(500,620),bd,(700,650)],inn(t,mid(17,.4),2),wid=7,col=RED)
        lb(cv,c,'chiến thuyền: sông Bạch Đằng',700,700,t,mid(17,.45),E[17]+.3,col=RED,sz=26)
def S_6(cv,t):
    a,b=T[6],E[7]
    c=cam(*cpath(t,[(a-.3,(1200,560,1.0)),(T[7],(900,560,1.0)),(b+.3,(700,580,1.2))]))
    sea(cv,c,t,620)
    put(cv,c,'t6_hamdoi',lerp(1500,1700,inn(t,a,b-a)),520,s=.65)
    lb(cv,c,'Ô Mã Nhi đi trước',1500,250,t,a+.3,mid(6,.5),col=RED,sz=36)
    put(cv,c,'t6_thuyenluong',lerp(300,450,inn(t,a,b-a)),700,s=.6,o=inn(t,mid(6,.45),.6))
    lb(cv,c,'thuyền lương của Trương Văn Hổ',500,500,t,mid(6,.5),E[6]+.3,sz=34)
    if t>T[7]-.2:
        lb(cv,c,'đi chậm',560,500,t,T[7]+.2,mid(7,.5),sz=34)
        big(cv,'THỨ QUÝ NHẤT CỦA CẢ ĐẠO QUÂN',t,mid(7,.45),b+.3,RED,150,52,seed=7)
def S_8(cv,t):
    a,b=T[8],E[9];tc=mid(8,.55)
    sh=fio(t,tc,E[8])
    c=cam(*cpath(t,[(a-.3,(1400,560,1.0)),(E[8],(1300,560,1.08)),(b+.3,(1100,560,1.12))]),sx=4*math.sin(t*23)*sh)
    sea(cv,c,t,640)
    put(cv,c,'t6_vandon',1400,420,ay=.5,s=.75)
    for i in range(5):
        x=lerp(2400,1200,inn(t,a,b-a))+i*230
        put(cv,c,'t6_chienthuyen',x,720+(i%2)*40,s=.5,ax=.5,ay=.85,r=bob(t,i))
    for i in range(5):
        x=lerp(900,500,inn(t,tc,3))+i*110
        put(cv,c,Af('smallboat2'),x,760+(i%2)*30,s=.55,ax=.5,ay=.86,r=bob(t,i),o=1-.5*inn(t,T[9],1))
    if a<t<E[8]+.5:
        arrows(cv,c,t,tc-.6,E[8],[(1300+k*200,600) for k in range(4)],[(600+k*110,720) for k in range(4)],n=10,h=70,per=.9,seed=8)
    tagfall(cv,c,700,520,'Trần Khánh Dư',t,a+.5,sz=36,col=INK,b=T[9])
    lb(cv,c,'vùng biển Vân Đồn',1300,140,t,a+.3,mid(8,.5),sz=40)
    lb(cv,c,'đánh không lại',800,430,t,mid(8,.6),E[8]+.3,col=RED,sz=36)
    lb(cv,c,'giặc lọt vào trong',1300,200,t,T[9]+.2,mid(9,.45),col=RED,sz=38)
    if t>mid(9,.45):
        put_screen(cv,band(1400,520,PAPER,.9,40),W/2,500,inn(t,mid(9,.45),.4))
        put_screen(cv,A('t6_bat'),W/2,560,inn(t,mid(9,.5),.5),s=.5)
        put_screen(cv,text('bị bắt về kinh xét tội',40,RED,700,glow=3),W/2,300,inn(t,mid(9,.6),.4))
def S_10(cv,t):
    a,b=T[10],E[10]
    c=cam(960,560,1.0+.03*(t-a))
    sea(cv,c,t,600,.8);put(cv,c,'t6_vandon',960,440,ay=.5,s=.6,o=.5);night(cv,.4)
    big(cv,'MỘT LỜI NÓI QUÁ?',t,mid(10,.4),b+.3,RED,220,72,seed=10)
def S_11(cv,t):
    a,b=T[11],E[13];tc=T[12]
    sh=fio(t,tc,E[12])
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(T[12],(900,560,1.05)),(b+.3,(860,580,1.12))]),sx=4*math.sin(t*23)*sh,sy=3*math.sin(t*19)*sh)
    sea(cv,c,t,620);put(cv,c,'t6_vandon',1300,420,ay=.5,s=.7,o=.6)
    sink=inn(t,mid(12,.3),3)
    put(cv,c,'t6_thuyenluong',lerp(1500,1000,inn(t,a,T[12]-a)),700+60*sink,s=.6,r=6*sink,o=1-.6*sink)
    for i in range(6):
        x=lerp(200,700,inn(t,mid(11,.5),3))+i*100
        put(cv,c,'smallboat2',x,760+(i%3)*25,s=.55,ax=.5,ay=.86,r=bob(t,i))
    tagfall(cv,c,500,520,'Trần Khánh Dư',t,a+.3,sz=36,col=INK,b=T[12])
    lb(cv,c,'xin hoãn ít ngày để lập công',600,200,t,a+.4,mid(11,.5),sz=36)
    lb(cv,c,'thuyền lương mới tới',1300,200,t,mid(11,.55),E[11]+.3,col=RED,sz=36)
    if t>tc-.2:
        arrows(cv,c,t,tc,mid(12,.6),[(400+k*90,700) for k in range(5)],[(950+k*120,640) for k in range(5)],n=14,h=90,per=.9,seed=11)
        for k in range(5): put(cv,c,'splash',950+k*120,740,s=.5,o=.6*fio(t,tc+.4+k*.25,tc+1.6+k*.25))
        big(cv,'KHÔNG ĐỂ LỌT',t,tc+.1,mid(12,.5),RED,170,80,seed=12)
    if t>T[13]-.2:
        seal(cv,'s1288',1500,330,T[13]+.2,t,s=.8,r=-4)
        big(cv,'THỨ ĐẦU TIÊN: THUYỀN LƯƠNG ĐÃ MẤT',t,T[13]+.3,b+.3,RED,170,56,seed=13)
def S_14(cv,t):
    a,b=T[14],E[14]
    c=cam(*cpath(t,[(a-.3,(1300,520,1.1)),(b+.3,(900,520,1.1))]))
    put(cv,c,'t6_benvang',1300,480,ay=.5,s=.75)
    lb(cv,c,'kinh thành bỏ trống',1600,150,t,a+.3,mid(14,.5),sz=38)
    lb(cv,c,'ngồi chờ thuyền lương',900,150,t,mid(14,.5),b+.3,col=RED,sz=40)
def S_15(cv,t):
    a,b=T[15],E[16]
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(T[16],(960,560,1.08)),(b+.3,(960,560,1.0))]))
    if t<T[16]-.1:
        put(cv,c,'t6_lang',960,520,s=1.0)
        tagfall(cv,c,960,170,'Ô Mã Nhi',t,mid(15,.45),sz=44,col=RED)
        lb(cv,c,'lăng vua Trần Thái Tông ở Long Hưng',960,330,t,mid(15,.55),E[15]+.3,sz=34)
        if t>mid(15,.6):
            for k in range(3): put(cv,c,'redblot',800+k*160,600,s=.5,o=.4*inn(t,mid(15,.6)+k*.3,.6))
    else:
        put(cv,c,'sun',1500,320,o=.6,k=.2);put(cv,c,'far',960,760,ay=1,k=.35,o=.45)
        ground(cv,c,760,.25) if False else None
        for i in range(10):
            x=lerp(1600,700,cl((t-T[16]-i*.2)/(b-T[16])))+i*90
            put(cv,c,Af('fig_giap_giao'),x,830+(i%2)*10,ay=1,s=.62,r=math.sin(t*3+i)*3)
        lb(cv,c,'càng đói, càng mệt',960,200,t,T[16]+.3,mid(16,.55),sz=40)
        big(cv,'RÚT VỀ',t,mid(16,.6),b+.3,RED,200,90,seed=16)
def S_18(cv,t):
    a,b=T[18],E[18]
    c=cam(*cpath(t,[(a-.3,(1400,500,1.0)),(b+.3,(1400,520,1.08))]))
    put(cv,c,'t6_songcu',1400,460,ay=.5,s=.7)
    sea(cv,c,t,700,.6)
    ghost=fio(t,mid(18,.35),b+.2)*.35
    for i in range(4): put(cv,c,'bigboat2',1000+i*280,760,s=.45,ax=.5,ay=.88,o=ghost)
    seal(cv,'s938',1000,280,mid(18,.3),t,s=.8,r=-4)
    seal(cv,'s1288',1800,280,a+.3,t,s=.8,r=4)
    lb(cv,c,'Ngô Quyền',1000,400,t,mid(18,.45),b+.3,sz=36)
    big(cv,'THỨ HAI: CON SÔNG CŨ',t,a+.3,mid(18,.4),RED,140,60,seed=18)
def S_19(cv,t):
    a,b=T[19],E[19]
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(b+.3,(1000,600,1.1))]))
    put(cv,c,'far',960,640,ay=1,k=.35,o=.4)
    put(cv,c,'t6_dongcoc',960,560,s=1.0)
    wl=lerp(760,560,inn(t,mid(19,.6),2.5))
    Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=cv[Ys:]*.55+PAP[Ys:]*.45
    put(cv,c,'water',960,wl-24,ay=0,o=.8)
    put(cv,c,'gauge',1780,520,s=.6,o=.85)
    lb(cv,c,'đóng cọc, phủ cỏ',700,270,t,a+.3,mid(19,.55),sz=40)
    lb(cv,c,'thủy triều lên che kín',700,270,t,mid(19,.6),b+.3,col=RED,sz=40)
def S_20(cv,t):
    a,b=T[20],E[20]
    c=cam(*cpath(t,[(a-.3,(900,560,1.05)),(b+.3,(860,560,1.15))]))
    put(cv,c,'mist',1300,600,s=3,o=.6)
    sea(cv,c,t,760,.6)
    put(cv,c,'t6_tuong',760,560,s=1.0)
    lb(cv,c,'không phá xong giặc Nguyên',1400,300,t,mid(20,.25),b+.3,sz=40)
    lb(cv,c,'thì không về đến sông này nữa',1400,370,t,mid(20,.5),b+.3,col=RED,sz=40)
def S_21(cv,t):
    a,b=T[21],E[21]
    c=cam(*cpath(t,[(a-.3,(1300,560,1.0)),(b+.3,(900,560,1.0))]))
    put(cv,c,'t6_songcu',1100,460,ay=.5,s=.7,o=.8);sea(cv,c,t,640)
    put(cv,c,'t6_hamdoi',lerp(2100,1300,inn(t,a,b-a)),560,s=.55)
    for i in range(4):
        x=lerp(1300,500,inn(t,mid(21,.4),b-mid(21,.4)))+i*110
        put(cv,c,Af('smallboat2'),x,780+(i%2)*20,s=.5,ax=.5,ay=.86,r=bob(t,i))
    lb(cv,c,'ngày mồng tám tháng Ba',1100,150,t,a+.3,mid(21,.5),sz=40)
    lb(cv,c,'giả thua chạy',700,560,t,mid(21,.5),b+.3,col=RED,sz=36)
COC=[(500+i*90+((i*37)%30),0) for i in range(14)]
def S_22(cv,t):
    a,b=T[22],E[24];tc=T[23]
    sh=fio(t,T[22],mid(23,.6))
    c=cam(*cpath(t,[(a-.3,(1000,580,1.0)),(T[23],(1000,600,1.05)),(T[24],(1000,600,1.12)),(b+.3,(1000,600,1.15))]),sx=5*math.sin(t*23)*sh,sy=4*math.sin(t*19)*sh)
    put(cv,c,'t6_songcu',1000,440,ay=.5,s=.7,o=.7)
    wl=lerp(700,800,inn(t,a,2.5))
    Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=PAP[Ys:]
    stk=A('stake')
    for i,(x,_) in enumerate(COC): put(cv,c,stk,x,wl-90-(i%3)*12,s=.9,ay=0,o=inn(t,a+.2,1.0))
    put(cv,c,'water',960,wl-24,ay=0,o=.8)
    for i in range(5):
        x=520+i*240;tilt=inn(t,a+.6+i*.3,1.5)*(8 if i%2 else -10)
        sk=inn(t,T[24]+i*.4,3)
        put(cv,c,'t6_chienthuyen',x,wl-10+60*sk,s=.55,ax=.5,ay=.85,r=tilt+sk*14,o=1-.5*sk)
    put(cv,c,'gauge',1780,520,s=.6,o=.85)
    lb(cv,c,'thủy triều rút',1000,250,t,a+.2,E[22]+.3,col=RED,sz=44)
    if t>tc-.2:
        for i in range(6):
            x=lerp(-100,350,inn(t,tc+i*.15,2))+i*60;put(cv,c,'smallboat2',x,wl+40+(i%2)*20,s=.45,ax=.5,ay=.86,r=bob(t,i))
            x2=lerp(2100,1650,inn(t,tc+i*.15,2))-i*60;put(cv,c,Af('smallboat2'),x2,wl+40+(i%2)*20,s=.45,ax=.5,ay=.86,r=bob(t,i))
        arrows(cv,c,t,tc+.2,E[23],[(300+k*60,wl-40) for k in range(4)]+[(1650-k*60,wl-40) for k in range(4)],[(520+k*240,wl-80) for k in range(5)],n=18,h=110,per=.9,seed=22)
        sparks(cv,c,t,[(600+k*230,wl-60) for k in range(4)],tc+.6,E[23],seed=22)
        lb(cv,c,'hơn bốn trăm chiếc bị bắt',1000,250,t,mid(23,.6),E[23]+.3,col=RED,sz=40)
    if t>T[24]-.2:
        put(cv,c,'t5_troi',1000,wl-20,ay=1,s=.6,o=inn(t,T[24],.6))
        tagfall(cv,c,1000,wl-260,'Ô Mã Nhi bị bắt sống',t,T[24]+.2,sz=40,col=RED)
        lb(cv,c,'người đã đào phá lăng vua Trần',1000,250,t,T[24]+.3,b+.3,sz=36)
def S_25(cv,t):
    a,b=T[25],E[25]
    c=cam(*cpath(t,[(a-.3,(1500,520,1.0)),(b+.3,(1300,520,1.06))]))
    put(cv,c,'t6_bienmoc',1400,460,ay=.5,s=.7)
    for i in range(7):
        x=lerp(800,1900,cl((t-a-i*.2)/(b-a)))-i*70;y=700-lerp(0,60,cl((x-800)/1100))
        put(cv,c,'ky_mong',x,y,ay=1,s=.38)
    lb(cv,c,'Thoát Hoan chạy qua biên giới',1400,150,t,a+.3,mid(25,.55),col=RED,sz=40)
    big(cv,'KHÔNG BAO GIỜ SANG NỮA',t,mid(25,.6),b+.3,INK,150,60,seed=25)
def S_26(cv,t):
    a,b=T[26],E[26]
    c=cam(960,560,1.0)
    items=[('t6_benvang','đánh xa nhà',.5),('t6_thuyenluong','sống nhờ thuyền lương',.55),('t6_songcu','rút qua con sông chờ sẵn',.5)]
    for k,(nm,lbl,sc) in enumerate(items):
        tk=a+.3+k*(b-a)/3.3;o=inn(t,tk,.5);x=360+k*600
        put(cv,c,nm,x,560,s=sc,o=o);put_screen(cv,text(lbl,32,INK if k<2 else RED,700,glow=3),x,380,o)
    big(cv,'ĐÁNH GIẶC NHÀN LÀ THẾ',t,a+.2,b+.3,RED,170,64,seed=26)
def S_end(cv,t):
    a=T[27]
    c=cam(960,560,1.0+.015*(t-a))
    put(cv,c,'t6_songcu',960,460,ay=.5,s=.7);sea(cv,c,t,700,.6)
    stk=A('stake')
    for i,(x,_) in enumerate(COC[::2]): put(cv,c,stk,x+200,620,s=.7,ay=0,o=.6)
    put(cv,c,'sun',1600,420,o=.5,k=.2);flock(cv,c,t,.6)
    put(cv,c,'t6_tuong',400,600,s=.6,o=.85)
    tx=text('Năm nay đánh giặc nhàn',64,INK,700);put_screen(cv,wipe(tx,inn(t,a+.3,1.2),0,.3,seed=13),W/2,230)
    seal(cv,'stitle6',W/2,430,mid(27,.5),t,s=.6,r=3)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,H-80,inn(t,E[27]+.5,1))
S=lambda n:T[n]-.3
SH=[(0,S(2),S_1),(S(2),S(3),S_2),(S(3),S(4),S_3),(S(4),S(5),S_4),(S(5),S(6),S_map),(S(6),S(8),S_6),(S(8),S(10),S_8),(S(10),S(11),S_10),
 (S(11),S(14),S_11),(S(14),S(15),S_14),(S(15),S(17),S_15),(S(17),S(18),S_map),(S(18),S(19),S_18),(S(19),S(20),S_19),(S(20),S(21),S_20),
 (S(21),S(22),S_21),(S(22),S(25),S_22),(S(25),S(26),S_25),(S(26),S(27),S_26),(S(27),V.TOTAL+1,S_end)]
def ov(cv,t):
    if T[5]-4.2<t<T[5]+.2: title(cv,t,T[5]-3.6,'BẠCH ĐẰNG','stitle6',.6)
def frame(t): return K.compose(V,SH,t,ov,CARDS)
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
