# Bản dài tm8: Chi Lăng, Xương Giang 1427 (bộ tranh riêng t8_*)
import math
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from fx_tran import arrows,dust,sparks,fall
from dai_tm2 import big,tagfall,strike,lb
from dai_tm3 import night
V=K.setup('tm8',{5:4.0,9:2.6,12:2.6,17:2.6,22:2.6})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
P=PTS
CARDS={9:'Đánh rồi lui',12:'Ải Chi Lăng',17:'Xương Giang',22:'Con dấu'}
def S_1(cv,t):
    c=cam(*cpath(t,[(0,(1300,560,1.25)),(E[1]+.3,(1400,540,1.1))]))
    if t<1.4: u=eo(t/1.3);put_screen(cv,A('blot'),W/2,H/2,(1-u)*.85,s=1.9*(1+u*.9))
    put(cv,c,'t8_duoi',1400+lerp(0,-80,cl(t/E[1])),560,ay=.5,s=.75)
    big(cv,'CÓ NÊN ĐUỔI THEO?',t,.25,E[1]+.3,RED,170,80,seed=1)
def S_2(cv,t):
    a,b=T[2],E[2]
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(b+.3,(960,560,1.08))]))
    put(cv,c,'mist',960,640,s=3,o=.6);put(cv,c,'far',960,760,ay=1,k=.35,o=.4)
    for r in range(3): put(cv,c,'t7_minh',1500+r*120,700+r*30,ay=1,s=.45+.05*r,o=.5+.2*r)
    put(cv,c,'t8_lieuthang',760,820,ay=1,s=1.0)
    tagfall(cv,c,760,400,'Liễu Thăng',t,a+.3,sz=48,col=RED)
    lb(cv,c,'mười vạn quân',1500,330,t,mid(2,.4),b+.3,col=RED,sz=40)
def S_3(cv,t):
    a,b=T[3],E[3]
    c=cam(*cpath(t,[(a-.3,(1400,560,1.0)),(b+.3,(1400,560,1.12))]))
    put(cv,c,'t8_mayen',1400,500,ay=.5,s=.75)
    for i in range(8):
        x=lerp(2300,1500,inn(t,a+.2+i*.05,b-a-1))+i*40
        put(cv,c,Af('ky_mong'),x,830+(i%2)*10,ay=1,s=.32,o=1-inn(t,mid(3,.75),.8))
    lb(cv,c,'núi Mã Yên',1400,200,t,a+.3,b+.3,sz=40)
    big(cv,'KHÔNG BAO GIỜ TRỞ RA',t,mid(3,.7),b+.3,RED,300,64,seed=3)
def S_4(cv,t):
    a,b=T[4],E[4]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'t8_mayen',500,600,s=.35,o=inn(t,mid(4,.6),.5));put(cv,c,'t8_dau',1400,620,s=.55,o=inn(t,mid(4,.8),.5))
    lb(cv,c,'một ngọn núi',500,420,t,mid(4,.6),b+.3,sz=38);lb(cv,c,'một con dấu',1400,420,t,mid(4,.8),b+.3,col=RED,sz=38)
    big(cv,'MƯỜI LĂM VẠN QUÂN CỨU VIỆN',t,a+.2,mid(4,.55),RED,170,60,seed=4)
def S_map(cv,t):
    keys=[(T[5]-.5,(470,600,2.4)),(E[5],(470,600,2.4)),(T[6]-.5,(400,520,1.2)),(E[6],(400,520,1.2)),(T[11]-.5,(420,520,1.2)),(E[11],(440,560,1.3))]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z)
    c=cam(cx,cy,z)
    mapbg(cv,c,u=inn(t,T[5]-1.0,1.4))
    tl,ls,lc,td=[P[k] for k in ['thanglong','langson2','laocai','totdong']]
    sz=24 if z>2 else 28
    dot(cv,c,*tl,o=1);tag(cv,c,tl[0]+12,tl[1]+26,'Đông Quan',dy=0,sz=sz)
    if t<T[6]:
        seal(cv,'s1426',300,250,T[5]+.2,t,s=.6,r=-4)
        stroke(cv,c,[(td[0],td[1]+20),(tl[0]-8,tl[1]+4)],inn(t,T[5]+.3,1.0),wid=4,col=RED)
        lb(cv,c,'Vương Thông thua ở Tốt Động',td[0]-20,td[1]+50,t,T[5]+.3,mid(5,.6),col=RED,sz=sz)
        for k in range(12): a_=k/12*6.28;dot(cv,c,tl[0]+24*math.cos(a_),tl[1]+24*math.sin(a_),o=inn(t,mid(5,.55)+k*.05,.3),r=4)
    else:
        u1=inn(t,T[6]+.3,2);u2=inn(t,mid(6,.55),2)
        lc2=(lc[0]-60,lc[1]-200)
        on=t<T[7] or t>T[11]-.5
        if on:
            seal(cv,'s1427',1500,260,T[6]+.2,t,s=.6,r=-4)
            stroke(cv,c,[(640,120),ls,(520,500),(tl[0]+10,tl[1]-10)],u1,wid=9,col=RED);lb(cv,c,'Liễu Thăng · mười vạn',760,320,t,T[6]+.4,E[11]+.3,col=RED,sz=sz)
            stroke(cv,c,[lc2,lc,(260,460),(tl[0]-10,tl[1]-10)],u2,wid=7,col=RED,dash=12);lb(cv,c,'Mộc Thạnh · năm vạn',220,300,t,mid(6,.6),E[11]+.3,col=RED,sz=sz)
        if t>T[11]-.5: big(cv,'ĐÔNG QUAN VẪN CHƯA HẠ',t,mid(11,.3),E[11]+.3,INK,170,56,seed=11)
def S_7(cv,t):
    a,b=T[7],E[8]
    c=cam(*cpath(t,[(a-.3,(960,540,1.0)),(T[8],(960,560,1.06)),(b+.3,(960,560,1.12))]))
    put(cv,c,'t8_lele',960,500,s=.9)
    tagfall(cv,c,950,330,'Lê Lợi',t,a+.3,sz=44,col=INK)
    lb(cv,c,'các tướng muốn đánh thành ngay',960,110,t,a+.4,mid(7,.5),sz=36)
    big(cv,'KHÔNG ĐÁNH THÀNH',t,mid(7,.5),E[7]+.3,RED,110,70,seed=7)
    lb(cv,c,'giữ sức, chờ quân cứu viện',960,110,t,T[8]+.2,b+.3,sz=38)
def S_9(cv,t):
    a,b=T[9],E[10]
    c=cam(*cpath(t,[(a-.3,(1000,560,1.1)),(T[10],(1400,560,1.15)),(b+.3,(1700,560,1.2))]))
    put(cv,c,'t8_duoi',1400,520,ay=.5,s=.75)
    lb(cv,c,'Trần Lựu đánh vài trận rồi lui',900,250,t,a+.3,E[9]+.3,sz=38)
    arrows(cv,c,t,a+.6,E[9],[(1300+k*80,440) for k in range(4)],[(820+k*60,480) for k in range(4)],n=8,h=60,per=1,seed=9)
    lb(cv,c,'càng tin mình mạnh, càng đuổi gấp',1600,250,t,T[10]+.2,b+.3,col=RED,sz=38)
def S_12(cv,t):
    a,b=T[12],E[13]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(T[13],(1400,560,1.08)),(b+.3,(1400,580,1.15))]))
    put(cv,c,'t8_chilang',1400,460,ay=.5,s=.75)
    lb(cv,c,'ải Chi Lăng',1400,170,t,a+.3,E[12]+.3,col=RED,sz=48)
    lb(cv,c,'phục sẵn trên núi',700,330,t,mid(12,.6),E[12]+.3,sz=34)
    if t>T[13]-.2:
        for i in range(9):
            x=lerp(2400,1500,inn(t,T[13]+i*.08,b-T[13]))+i*50
            put(cv,c,Af('ky_mong'),x,740+(i%2)*10,ay=1,s=.32)
        put(cv,c,Af('t8_lieuthang'),lerp(2350,1450,inn(t,T[13],b-T[13])),740,ay=1,s=.4)
        lb(cv,c,'hơn một trăm kỵ binh vượt lên trước',1400,250,t,T[13]+.2,b+.3,sz=36)
def S_14(cv,t):
    a,b=T[14],E[15];tc=T[14]+.3
    sh=fio(t,tc,E[14])
    c=cam(*cpath(t,[(a-.3,(1400,600,1.15)),(T[15],(1400,600,1.2)),(b+.3,(1400,580,1.1))]),sx=5*math.sin(t*23)*sh,sy=4*math.sin(t*19)*sh)
    put(cv,c,'t8_mayen',1400,480,ay=.5,s=.75)
    rid=[]
    for i in range(9):
        x=1350+i*55;y=740+(i%2)*10;rid.append((x,y))
        tf=tc+.5+i*.25
        if i%3!=1 and t>tf: fall(cv,c,Af('ky_mong'),x,y,t,tf,s=.32,dirn=1)
        else: put(cv,c,Af('ky_mong'),x,y,ay=1,s=.32)
    td=mid(14,.5)
    if t<td: put(cv,c,Af('t8_lieuthang'),1300,740,ay=1,s=.4)
    else: fall(cv,c,Af('t8_lieuthang'),1300,740,t,td,s=.4,dirn=1)
    for side in (-1,1):
        for i in range(7):
            x=(700+i*60) if side<0 else (2100-i*60);put(cv,c,'fig_giap_giao' if side<0 else Af('fig_giap_giao'),lerp(x+side*300,x,inn(t,tc,1)),720+(i%2)*14,ay=1,s=.38,o=inn(t,tc,.4))
    arrows(cv,c,t,tc,E[14]+.4,[(800+k*60,620) for k in range(4)]+[(2000-k*60,620) for k in range(4)],[(x,y-40) for x,y in rid],n=18,h=110,per=.9,seed=14)
    tagfall(cv,c,1300,440,'Liễu Thăng',t,a+.1,fall=td+.2,sz=44,col=RED)
    if t>td+.6 and t<T[15]+.4: put(cv,c,'redblot',1300,700,s=.7*eo(cl((t-td)/1.2)),o=.5)
    if t>T[15]-.2:
        seal(cv,'s1427',1700,300,T[15]+.2,t,s=.7,r=-4)
        big(cv,'THỨ ĐẦU TIÊN: NGỌN NÚI',t,T[15]+.2,b+.3,RED,170,60,seed=15)
def S_16(cv,t):
    a,b=T[16],E[16]
    c=cam(*cpath(t,[(a-.3,(1600,560,1.1)),(b+.3,(1300,560,1.1))]))
    put(cv,c,'t8_duong',1400,480,ay=.5,s=.75)
    for i in range(3): put(cv,c,'t7_minh',lerp(2200,1500,inn(t,a,b-a))+i*300,700+(i%2)*20,ay=1,s=.35,o=.85)
    arrows(cv,c,t,a+.3,b,[(900+k*120,500) for k in range(5)],[(1500+k*150,660) for k in range(5)],n=12,h=60,per=.9,seed=16)
    tagfall(cv,c,1200,250,'Lương Minh tử trận',t,a+.3,fall=mid(16,.45),sz=40,col=RED)
    tagfall(cv,c,1700,250,'Lý Khánh tự tử',t,mid(16,.5),fall=b-.2,sz=40,col=RED)
def S_17(cv,t):
    a,b=T[17],E[18]
    c=cam(*cpath(t,[(a-.3,(900,520,1.1)),(T[18],(1600,560,1.08)),(b+.3,(1700,560,1.15))]))
    put(cv,c,'t8_xuonggiang',1400,460,ay=.5,s=.75)
    if t<T[18]-.1:
        for r in range(2): put(cv,c,'t7_minh',lerp(2200,1500,inn(t,a,E[17]-a))+r*200,700+r*30,ay=1,s=.35,o=.85)
        tagfall(cv,c,1600,290,'Thôi Tụ, Hoàng Phúc',t,a+.3,sz=38,col=RED)
        lb(cv,c,'thành đã bị hạ từ trước',900,170,t,mid(17,.6),E[17]+.3,col=RED,sz=40)
    else:
        lb(cv,c,'đóng trại giữa đồng trống',1700,170,t,T[18]+.2,mid(18,.5),sz=40)
        u=inn(t,mid(18,.5),2)
        for k in range(16):
            a_=k/16*6.28;dot(cv,c,1820+520*math.cos(a_)*u+0*(1-u),470+120*math.sin(a_)*u,o=u,r=7)
        lb(cv,c,'vây kín bốn mặt, cắt đường lấy lương',1700,170,t,mid(18,.55),b+.3,col=RED,sz=38)
def S_19(cv,t):
    a,b=T[19],E[21];tc=T[19]+.3
    sh=fio(t,tc,mid(19,.6))
    c=cam(*cpath(t,[(a-.3,(1800,560,1.15)),(T[20],(1700,560,1.2)),(b+.3,(1700,560,1.12))]),sx=4*math.sin(t*23)*sh,sy=3*math.sin(t*19)*sh)
    put(cv,c,'t8_xuonggiang',1400,460,ay=.5,s=.75)
    if t<T[20]-.1:
        arrows(cv,c,t,tc,E[19],[(1300+k*80,560) for k in range(4)]+[(2400-k*80,560) for k in range(4)],[(1600+k*100,500) for k in range(6)],n=18,h=90,per=.9,seed=19)
        sparks(cv,c,t,[(1650+k*120,500) for k in range(4)],tc+.3,E[19],seed=19)
        for k in range(4): put(cv,c,'redblot',1600+k*150,500,s=.5,o=.45*inn(t,tc+.6+k*.3,.6))
        big(cv,'DOANH TRẠI VỠ',t,tc,E[19]+.3,RED,170,72,seed=19)
    else:
        put(cv,c,'t8_tha',1700,640,s=.6)
        lb(cv,c,'Hoàng Phúc từng làm quan ở nước ta nhiều năm',1700,250,t,T[20]+.2,E[20]+.3,sz=34)
        if t>T[21]-.2: big(cv,'MƯỜI VẠN QUÂN ẤY KHÔNG CÒN NỮA',t,T[21]+.1,b+.3,RED,170,56,seed=21)
def S_22(cv,t):
    a,b=T[22],E[23]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(T[23],(1400,540,1.08)),(b+.3,(1300,560,1.1))]))
    put(cv,c,'t8_lehoa',1400,480,ay=.5,s=.75)
    lb(cv,c,'Mộc Thạnh ở Lê Hoa',1400,170,t,a+.3,mid(22,.5),sz=40)
    put(cv,c,'ky_si',lerp(400,1100,inn(t,mid(22,.4),2.5)),760,ay=1,s=.45)
    put(cv,c,'t8_dau',lerp(400,1100,inn(t,mid(22,.4),2.5)),560,s=.25,o=inn(t,mid(22,.45),.4)*(1-inn(t,T[23],.5)))
    if t>T[23]-.2:
        put_screen(cv,A('t8_dau'),W/2,420,inn(t,T[23],.4)*(1-inn(t,mid(23,.5),.4)),s=.55)
        big(cv,'THỨ HAI: CON DẤU',t,T[23]+.1,mid(23,.5),RED,170,64,seed=23)
        for i in range(8):
            x=lerp(1100,2300,inn(t,mid(23,.4)+i*.1,5))+i*60
            put(cv,c,Af('ky_mong'),x,850+(i%2)*10,ay=1,s=.38,o=inn(t,mid(23,.4),.3))
        lb(cv,c,'Mộc Thạnh bỏ chạy về nước',1500,170,t,mid(23,.55),b+.3,col=RED,sz=40)
def S_24(cv,t):
    a,b=T[24],E[24]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(b+.3,(1300,540,1.08))]))
    put(cv,c,'t8_ve',1400,460,ay=.5,s=.75)
    lb(cv,c,'Vương Thông xin thôi đánh',1400,170,t,a+.3,mid(24,.5),sz=40)
    lb(cv,c,'cấp cả thuyền và ngựa',1400,170,t,mid(24,.55),b+.3,col=RED,sz=40)
def S_end(cv,t):
    a=T[25]
    c=cam(960,560,1.0+.015*(t-a))
    put(cv,c,'t8_chilang',960,460,ay=.5,s=.7);put(cv,c,'sun',1600,360,o=.45,k=.2);flock(cv,c,t,.6)
    tx=text('Đánh rồi lùi, kéo người đuổi theo vào Chi Lăng',56,INK,700);put_screen(cv,wipe(tx,inn(t,a+.3,1.2),0,.3,seed=13),W/2,230)
    seal(cv,'stitle8',W/2,430,mid(25,.5),t,s=.55,r=3)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,H-80,inn(t,E[25]+.5,1))
S=lambda n:T[n]-.3
SH=[(0,S(2),S_1),(S(2),S(3),S_2),(S(3),S(4),S_3),(S(4),S(5),S_4),(S(5),S(7),S_map),(S(7),S(9),S_7),(S(9),S(11),S_9),(S(11),S(12),S_map),
 (S(12),S(14),S_12),(S(14),S(16),S_14),(S(16),S(17),S_16),(S(17),S(19),S_17),(S(19),S(22),S_19),(S(22),S(24),S_22),(S(24),S(25),S_24),(S(25),V.TOTAL+1,S_end)]
def ov(cv,t):
    TT=V.TTL or T[5]
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'CHI LĂNG · XƯƠNG GIANG','stitle8',.55)
V.NHAN={2: 'Liễu Thăng – tướng nhà Minh', 6: 'Mộc Thạnh – tướng nhà Minh', 9: 'Trần Lựu – tướng Lam Sơn', 12: 'Chi Lăng – Lạng Sơn ngày nay', 16: 'Lương Minh, Lý Khánh – tướng, quan nhà Minh', 17: ['Thôi Tụ, Hoàng Phúc – tướng, quan nhà Minh', 'Xương Giang – Bắc Giang ngày nay']}
def S_chen(cv,t):
    ks=sorted(k for k in V.T if 4<k<5);a,b=V.T[ks[0]],V.E[ks[-1]]
    cx,cy,z=cpath(t,[(a-.3,(600,600,1.3)),(b+.3,(560,620,1.5))]);c=cam(min(max(cx,960/z),1920-960/z),min(max(cy,540/z),1080-540/z),z)
    mapbg(cv,c,u=1)
    tl,th=P['thanglong'],P['thanhhoa']
    lb(cv,c,'gần sáu trăm năm trước',900,640,t,a+.3,b+.3,sz=30)
    lb(cv,c,'nhà Minh cai trị nước ta hai mươi năm',900,690,t,mid(ks[0],.5),b+.3,col=RED,sz=30)
    if t>V.T[ks[-1]]-.2:
        dot(cv,c,*th,o=1);tag(cv,c,th[0]+60,th[1],'Thanh Hóa',dy=0,sz=24)
        stroke(cv,c,[th,(th[0]-10,th[1]-90),(tl[0]-6,tl[1]+30)],inn(t,V.T[ks[-1]]+.2,2),wid=9,col=INK)
        lb(cv,c,'nghĩa quân Lam Sơn · Lê Lợi',th[0]+160,th[1]-70,t,V.T[ks[-1]]+.2,b+.3,sz=26)
        dot(cv,c,*tl,o=1,col=RED);tag(cv,c,tl[0]+20,tl[1]-26,'Đông Quan – Hà Nội ngày nay',o=inn(t,mid(ks[-1],.6),.4),dy=0,sz=24,col=RED)

def _chen_sh():
    if V.TTL:
        i=[k for k,s in enumerate(SH) if s[2] is S_4][0];a0,b0,fn=SH[i];k1=min(k for k in V.T if 4<k<5)
        SH[i]=(a0,V.T[k1]-.3,fn);SH.insert(i+1,(V.T[k1]-.3,b0,S_chen))
_chen_sh()
def frame(t): return K.compose(V,SH,t,ov,CARDS)
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
