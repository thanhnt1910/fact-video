# Bản dài tm10: Ngọc Hồi, Đống Đa 1789 (bộ tranh riêng t10_*)
import math
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from fx_tran import arrows,dust,sparks,fall
from dai_tm2 import big,tagfall,strike,lb
from dai_tm3 import night
V=K.setup('tm10',{5:4.0,8:2.6,11:2.6,14:2.6,16:2.6,22:2.6})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
P=PTS
CARDS={8:'Quân Thanh trong thành',11:'Lời hẹn',14:'Đường ra bắc',16:'Ngọc Hồi',22:'Cầu phao'}
def S_1(cv,t):
    c=cam(*cpath(t,[(0,(960,560,1.12)),(E[1]+.3,(960,540,1.0))]))
    if t<1.4: u=eo(t/1.3);put_screen(cv,A('blot'),W/2,H/2,(1-u)*.85,s=1.9*(1+u*.9))
    put(cv,c,'t10_tet',960,520,s=.95)
    big(cv,'HẸN TRƯỚC NGÀY ĂN MỪNG?',t,.25,E[1]+.3,RED,150,76,seed=1)
def S_2(cv,t):
    a,b=T[2],E[2]
    c=cam(*cpath(t,[(a-.3,(900,580,1.1)),(b+.3,(960,560,1.0))]))
    put(cv,c,'mist',1300,600,s=3,o=.6);put(cv,c,'far',960,760,ay=1,k=.35,o=.4)
    put(cv,c,'t10_qt',700,860,ay=1,s=.85)
    tagfall(cv,c,1350,330,'Quang Trung Nguyễn Huệ',t,a+.4,sz=44,col=INK)
    lb(cv,c,'hẹn mồng bảy tháng Giêng',1350,490,t,mid(2,.55),b+.3,col=RED,sz=40)
def S_3(cv,t):
    a,b=T[3],E[3]
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(b+.3,(960,560,1.08))]))
    put(cv,c,'t10_dinh',1400,460,ay=.5,s=.75,o=.8)
    put(cv,c,'t10_thanh',960,760,ay=1,s=.75)
    lb(cv,c,'hai mươi chín vạn, theo sử ta',960,250,t,a+.3,mid(3,.55),col=RED,sz=40)
    big(cv,'VÀO THÀNH TRƯỚC HẸN HAI NGÀY',t,mid(3,.6),b+.3,INK,170,58,seed=3)
def S_4(cv,t):
    a,b=T[4],E[4]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'t10_tet',500,600,s=.4,o=inn(t,mid(4,.55),.5));put(cv,c,'t10_van',1420,620,s=.5,o=inn(t,mid(4,.8),.5))
    lb(cv,c,'một cái Tết ăn trước',500,420,t,mid(4,.55),b+.3,sz=36);lb(cv,c,'những tấm ván phủ rơm ướt',1420,420,t,mid(4,.8),b+.3,col=RED,sz=36)
    big(cv,'VÌ SAO ĐẾN SỚM?',t,a+.2,mid(4,.55),RED,170,70,seed=4)
def S_map(cv,t):
    keys=[(T[6]-.5,(560,520,1.3)),(E[6],(500,560,1.3)),(T[13]-.5,(520,860,.9)),(E[13],(500,760,1.2)),(T[14]-.5,(440,680,3.0)),(E[14],(440,660,3.0))]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z)
    c=cam(cx,cy,z)
    mapbg(cv,c,u=inn(t,T[6]-1.0,1.4))
    tl,ls,td,gk,hh,nh,px,na=[P[k] for k in ['thanglong','langson2','tamdiep','gianKhau','hahoi','ngochoi','phuxuan','nghean']]
    sz=26 if z<2 else 20
    dot(cv,c,*tl,o=1);tag(cv,c,tl[0]+14,tl[1]-20,'Thăng Long',dy=0,sz=sz)
    if t<T[7]:
        seal(cv,'s1788',1500,260,T[6]+.2,t,s=.6,r=-4)
        stroke(cv,c,[(660,120),ls,(520,500),tl],inn(t,mid(6,.4),2),wid=9,col=RED);lb(cv,c,'Tôn Sĩ Nghị',740,320,t,mid(6,.4),E[6]+.3,col=RED,sz=sz)
    elif t<T[14]:
        dot(cv,c,*px,o=1);tag(cv,c,px[0]+20,px[1]-24,'Phú Xuân',dy=0,sz=sz)
        stroke(cv,c,[px,(620,1300),na,(430,900),td],inn(t,T[13]-.3,2.5),wid=9,col=INK)
        dot(cv,c,*td,o=1);tag(cv,c,td[0]+40,td[1],'Tam Điệp',dy=0,sz=sz)
    else:
        for p,nm in [(gk,'Gián Khẩu'),(hh,'Hà Hồi'),(nh,'Ngọc Hồi')]: dot(cv,c,*p,o=1,r=6);tag(cv,c,p[0]+30,p[1],nm,dy=0,sz=sz)
        stroke(cv,c,[td,gk,hh],inn(t,T[14]+.2,E[14]-T[14]),wid=5,col=INK)
def S_5(cv,t):
    a,b=T[5],E[5]
    c=cam(*cpath(t,[(a-.3,(1200,560,1.0)),(b+.3,(1500,560,1.06))]))
    put(cv,c,'t10_cong',1400,460,ay=.5,s=.75);night(cv,.35)
    for i in range(6): put(cv,c,'fig_quan',lerp(1400,2200,inn(t,a+i*.15,b-a))+i*60,760,ay=1,s=.6)
    tagfall(cv,c,1500,830,'Lê Chiêu Thống bỏ Thăng Long',t,a+.3,sz=36,col=INK)
    lb(cv,c,'mẹ và vợ con sang nhà Thanh xin quân',1400,200,t,mid(5,.55),b+.3,col=RED,sz=38)
def S_7(cv,t):
    a,b=T[7],E[7]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(b+.3,(1400,540,1.08))]))
    put(cv,c,'t10_tamdiep',1400,460,ay=.5,s=.75)
    for i in range(10): put(cv,c,'fig_giap_giao',lerp(900,1400,inn(t,a+i*.1,b-a))+i*30,700+(i%2)*8,ay=1,s=.32)
    tagfall(cv,c,1400,110,'Ngô Văn Sở',t,a+.3,sz=40,col=INK)
    lb(cv,c,'theo kế Ngô Thì Nhậm, rút về Tam Điệp',1400,290,t,mid(7,.4),b+.3,sz=34)
def S_8(cv,t):
    a,b=T[8],E[9]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(T[9],(960,540,1.0)),(b+.3,(960,560,1.08))]))
    if t<T[9]-.1:
        put(cv,c,'t10_dinh',1400,460,ay=.5,s=.75)
        seal(cv,'s1788',1750,300,mid(8,.55),t,s=.7,r=-4)
        lb(cv,c,'An Nam quốc vương',1400,180,t,mid(8,.55),E[8]+.3,col=RED,sz=44)
        lb(cv,c,'gần như không mất một trận nào',1400,180,t,a+.3,mid(8,.5),sz=38)
    else:
        put(cv,c,'t10_chau',960,500,s=.9)
        lb(cv,c,'việc gì cũng chờ lệnh',960,130,t,mid(9,.4),b+.3,col=RED,sz=40)
def S_10(cv,t):
    a,b=T[10],E[10]
    c=cam(960,560,1.0+.03*(t-a))
    put(cv,c,'t10_tamdiep',960,460,ay=.5,s=.7);night(cv,.4)
    big(cv,'CHUYỆN KHÔNG TƯỞNG?',t,mid(10,.5),b+.3,RED,170,72,seed=10)
def S_11(cv,t):
    a,b=T[11],E[11]
    c=cam(*cpath(t,[(a-.3,(960,520,1.0)),(b+.3,(960,540,1.1))]))
    put(cv,c,'t10_dan',960,480,s=.95)
    lb(cv,c,'Phú Xuân',960,120,t,a+.3,mid(11,.4),sz=40)
    big(cv,'QUANG TRUNG',t,mid(11,.45),b+.3,RED,150,80,seed=11)
def S_12(cv,t):
    a,b=T[12],E[13]
    c=cam(*cpath(t,[(a-.3,(960,520,1.0)),(T[13],(960,540,1.06)),(b+.3,(900,560,1.12))]))
    if t<T[13]-.1:
        put(cv,c,'t10_tet',960,500,s=.95)
        lb(cv,c,'Tam Điệp: ăn Tết trước',960,130,t,a+.3,mid(12,.6),sz=40)
        big(cv,'HẸN MỒNG BẢY',t,mid(12,.65),E[12]+.3,RED,150,80,seed=12)
    else:
        put(cv,c,'far',960,640,ay=1,k=.35,o=.4)
        Ys=int(c.p(0,620)[1]);cv[Ys:]=PAP[Ys:];put(cv,c,'water',960,596,ay=0)
        for i in range(8): put(cv,c,'smallboat2',lerp(-200,900,inn(t,T[13]+i*.2,b-T[13]))+i*120,700+(i%3)*30,s=.5,ax=.5,ay=.86)
        night(cv,.45)
        big(cv,'THỨ ĐẦU TIÊN: CÁI TẾT ĂN SỚM',t,T[13]+.2,mid(13,.5),RED,150,56,seed=13)
        lb(cv,c,'đêm ba mươi, vượt sông Gián Khẩu',960,230,t,mid(13,.5),b+.3,sz=40)
def S_14(cv,t):
    a,b=T[14],E[15];tc=mid(14,.6)
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(b+.3,(1400,540,1.1))]))
    put(cv,c,'t10_hahoi',1400,460,ay=.5,s=.75);night(cv,.35*(1-inn(t,T[15],1)))
    lb(cv,c,'đồn Hà Hồi, đêm mồng ba Tết',1400,170,t,a+.3,mid(14,.55),sz=40)
    if t>tc: big(cv,'ĐỒNG LOẠT HÔ VANG',t,tc,E[14]+.3,RED,170,64,seed=14)
    if t>T[15]-.2:
        lb(cv,c,'quân trong đồn xin hàng',1400,170,t,T[15]+.2,mid(15,.55),col=RED,sz=40)
        lb(cv,c,'chỉ còn đồn Ngọc Hồi chắn lối',1400,170,t,mid(15,.6),b+.3,sz=40)
def S_16(cv,t):
    a,b=T[16],E[17]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(T[17],(1400,540,1.05)),(b+.3,(1300,560,1.1))]))
    put(cv,c,'t10_ngochoi',1400,460,ay=.5,s=.75)
    lb(cv,c,'lũy cao, súng lớn',1400,160,t,a+.3,E[16]+.3,col=RED,sz=40)
    if t>T[17]-.2:
        put(cv,c,'t10_van',lerp(500,800,inn(t,T[17],b-T[17])),760,ay=1,s=.5,o=inn(t,T[17],.5))
        big(cv,'THỨ HAI: NHỮNG TẤM VÁN',t,T[17]+.1,b+.3,RED,160,60,seed=17)
def S_18(cv,t):
    a,b=T[18],E[19];tc=T[19]
    sh=fio(t,tc,E[19])
    c=cam(*cpath(t,[(a-.3,(1300,560,1.05)),(T[19],(1400,560,1.1)),(b+.3,(1400,560,1.15))]),sx=5*math.sin(t*23)*sh,sy=4*math.sin(t*19)*sh)
    put(cv,c,'t10_ngochoi',1400,460,ay=.5,s=.75)
    xv=lerp(700,1200,inn(t,a,T[19]-a))
    if t<tc+.3: put(cv,c,'t10_van',xv,760,ay=1,s=.5)
    arrows(cv,c,t,a+.3,tc+.2,[(900+k*150,380) for k in range(5)],[(xv-250+k*120,640) for k in range(5)],n=16,h=50,per=.8,seed=18)
    for k in range(3): put(cv,c,'redblot',1000+k*200,350,s=.3,o=.6*fio(t,a+.4+k*.4,a+1+k*.4)) if t<tc else None
    lb(cv,c,'rạng sáng mồng năm Tết',1400,160,t,a+.2,mid(18,.5),sz=40)
    lb(cv,c,'súng và tên rơi xuống rơm ướt',1400,160,t,mid(18,.55),E[18]+.3,col=RED,sz=40)
    if t>tc-.2:
        for i in range(10):
            st=tc+.1+i*.08;u=inn(t,st,1.6);put(cv,c,'fig_giap_giao',lerp(1000+i*40,1500+i*60,u),620+(i%2)*20,ay=1,s=.4,o=inn(t,st,.3))
        for i in range(8):
            tf=mid(19,.4)+i*.2;x=1500+i*90
            if i%2==0 and t>tf: fall(cv,c,Af('t10_thanh') if False else 'fig_quan',x,600,t,tf,s=.5,dirn=1)
            else: put(cv,c,'fig_quan',lerp(x,x+600,inn(t,mid(19,.5),2)),600,ay=1,s=.5)
        sparks(cv,c,t,[(1300+k*120,520) for k in range(4)],tc+.3,E[19],seed=19)
        big(cv,'ĐỒN NGỌC HỒI VỠ',t,mid(19,.35),b+.3,RED,160,72,seed=19)
def S_20(cv,t):
    a,b=T[20],E[20]
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(b+.3,(960,560,1.08))]))
    put(cv,c,'t10_go',960,500,s=1.0)
    lb(cv,c,'Khương Thượng',960,160,t,a+.3,mid(20,.4),sz=40)
    tagfall(cv,c,960,330,'Đô đốc Long',t,a+.4,sz=40,col=INK,b=mid(20,.5))
    tagfall(cv,c,960,330,'Sầm Nghi Đống',t,mid(20,.55),fall=b-.4,sz=44,col=RED)
def S_21(cv,t):
    a,b=T[21],E[21]
    c=cam(*cpath(t,[(a-.3,(1300,540,1.0)),(b+.3,(1700,540,1.05))]))
    put(cv,c,'t10_cong',1400,460,ay=.5,s=.75,o=.8)
    x=lerp(1200,2300,inn(t,mid(21,.4),b-mid(21,.4)));put(cv,c,Af('ky_si'),x,760,ay=1,s=.6);dust(cv,c,x-150,740,o=.4)
    tagfall(cv,c,x,640,'Tôn Sĩ Nghị',t,a+.3,sz=40,col=RED)
    lb(cv,c,'ngựa không kịp đóng yên, người không kịp mặc giáp',1400,170,t,mid(21,.3),b+.3,sz=34)
def S_22(cv,t):
    a,b=T[22],E[23]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(T[23],(1400,540,1.06)),(b+.3,(960,560,1.0))]))
    if t<T[23]-.1:
        put(cv,c,'t10_cauphao',1400,460,ay=.5,s=.75)
        for i in range(8): put(cv,c,'fig_quan',1000+i*90,430,ay=1,s=.3,o=1-inn(t,mid(22,.5)+i*.1,.6))
        for k in range(5): put(cv,c,'splash',1300+k*90,520,s=.4,o=.6*fio(t,mid(22,.5)+k*.25,mid(22,.5)+1.2+k*.25))
        lb(cv,c,'cầu đứt',1400,180,t,mid(22,.45),E[22]+.3,col=RED,sz=44)
    else:
        put(cv,c,'t10_bk',960,500,s=.95)
        tagfall(cv,c,960,560,'Lê Chiêu Thống',t,T[23]+.3,sz=40,col=INK)
        lb(cv,c,'chỉ được một chức quan nhỏ',960,640,t,mid(23,.5),b+.3,col=RED,sz=38)
def S_end(cv,t):
    a=T[24]
    c=cam(960,560,1.0+.015*(t-a))
    put(cv,c,'t10_cong',960,460,ay=.5,s=.7);put(cv,c,'sun',1600,300,o=.5,k=.2);flock(cv,c,t,.6)
    tx=text('Trưa mồng năm, sớm hơn ngày hẹn hai ngày',58,INK,700);put_screen(cv,wipe(tx,inn(t,a+.3,1.2),0,.3,seed=13),W/2,220)
    seal(cv,'stitle10',W/2,400,mid(24,.5),t,s=.55,r=3)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,H-80,inn(t,E[24]+.5,1))
S=lambda n:T[n]-.3
SH=[(0,S(2),S_1),(S(2),S(3),S_2),(S(3),S(4),S_3),(S(4),S(5),S_4),(S(5),S(6),S_5),(S(6),S(7),S_map),(S(7),S(8),S_7),(S(8),S(10),S_8),(S(10),S(11),S_10),
 (S(11),S(12),S_11),(S(12),S(14),S_12),(S(14),S(16),S_14),(S(16),S(18),S_16),(S(18),S(20),S_18),(S(20),S(21),S_20),(S(21),S(22),S_21),(S(22),S(24),S_22),(S(24),V.TOTAL+1,S_end)]
def ov(cv,t):
    if T[5]-4.2<t<T[5]+.2: title(cv,t,T[5]-3.6,'NGỌC HỒI · ĐỐNG ĐA','stitle10',.55)
def frame(t): return K.compose(V,SH,t,ov,CARDS)
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
