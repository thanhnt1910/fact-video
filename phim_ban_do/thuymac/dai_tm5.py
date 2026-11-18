# Bản dài tm5: Hàm Tử, Chương Dương, Tây Kết 1285 (bộ tranh riêng t5_*, giọng Charon gốc)
import math
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title,rain
from canh import *
from fx_tran import arrows,dust,sparks,fall
from dai_tm2 import big,tagfall,strike,lb
from dai_tm3 import night
V=K.setup('tm5',{6:4.0,11:2.6,18:2.6,21:2.6,26:2.6,29:2.6})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
P=PTS
CARDS={11:'Giặc tràn sang',18:'Bến thứ nhất',21:'Bến thứ hai',26:'Bến thứ ba',29:'Đường rút'}
def bob(t,i=0): return math.sin(t*1.3+i)*1.2
def mistbg(cv,c,o=.6,y=760):
    put(cv,c,'far',960,y,ay=1,k=.35,o=.4);put(cv,c,'mist',900,y-140,s=2.8,o=o,k=.45)
def water(cv,c,t,wl):
    Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=PAP[Ys:]
    put(cv,c,'water',960,wl-24,ay=0)
    for i,yy in enumerate([wl+8,wl+90,wl+210]): put(cv,c,'wave',960-((t*(18+i*9))%200)+(i*77),yy,ay=.5,o=.4-.1*i)
# ---------------- mở đầu
def S_1(cv,t):
    c=cam(*cpath(t,[(0,(960,560,1.15)),(E[1]+.3,(960,540,1.0))]))
    mistbg(cv,c,.8)
    if t<1.4: u=eo(t/1.3);put_screen(cv,A('blot'),W/2,H/2,(1-u)*.85,s=1.9*(1+u*.9))
    put(cv,c,'t5_khay',960,860,ay=1,s=1.5)
    if t>.8: put(cv,c,'redblot',960,520,s=.5,o=.6*inn(t,.8,.6))
    big(cv,'CHỊU HÀNG ĐỂ LÀM VƯƠNG?',t,.25,E[1]+.3,RED,170,80,seed=1)
def S_2(cv,t):
    a,b=T[2],E[2]
    c=cam(960,560,1.0+.03*(t-a))
    mistbg(cv,c,.7)
    u=inn(t,a+.3,1.2)
    put(cv,c,'fig_giap',lerp(880,640,u),860,ay=1,s=1.9)
    put(cv,c,Af('fig_quan_dung'),lerp(1040,1280,u),860,ay=1,s=2.0)
    stroke(cv,c,[(960,180),(965,860)],inn(t,a+.6,1.0),wid=6,head=False,o=.8)
    lb(cv,c,'cùng họ Trần',960,150,t,a+.3,mid(2,.5),sz=40)
    big(cv,'HAI CÁCH TRẢ LỜI',t,mid(2,.45),b+.3,INK,160,70,seed=2)
def S_3(cv,t):
    a,b=T[3],E[3];td=mid(3,.78)
    c=cam(*cpath(t,[(a-.3,(960,600,1.0)),(b+.3,(960,620,1.12))]))
    mistbg(cv,c,.5)
    put(cv,c,'t5_troi',960,870,ay=1,s=1.55,o=1-.6*inn(t,td,1.0))
    tagfall(cv,c,960,500,'Trần Bình Trọng',t,a+.3,fall=td+.2,sz=44,col=INK)
    big(cv,'THÀ LÀM QUỶ NƯỚC NAM',t,a+.8,mid(3,.6),RED,170,70,seed=3)
    big(cv,'CHỨ KHÔNG THÈM LÀM VƯƠNG ĐẤT BẮC',t,mid(3,.3),mid(3,.7),INK,250,46,seed=4)
    if t>td: put(cv,c,'redblot',960,700,s=1.5*eo(cl((t-td)/1.4)),o=.6)
def S_4(cv,t):
    a,b=T[4],E[4]
    c=cam(*cpath(t,[(a-.3,(900,560,1.0)),(b+.3,(1100,560,1.08))]))
    put(cv,c,'t5_traitk',1500,640,ay=.5,s=.7,o=.55)
    put(cv,c,'mist',700,640,s=2.4,o=.6,k=.45)
    for i in range(6):
        x=lerp(300-i*110,1000-i*110,inn(t,a+.2,b-a));im='fig_quan_dung' if i==0 else 'fig_quan'
        put(cv,c,im,x,830+(i%2)*8,ay=1,s=1.5 if i==0 else 1.2,o=inn(t,a+i*.15,.4))
    tagfall(cv,c,lerp(300,1000,inn(t,a+.2,b-a)),330,'Trần Ích Tắc',t,a+.3,sz=42,col=INK)
    lb(cv,c,'em trai Thượng hoàng',lerp(300,1000,inn(t,a+.2,b-a)),400,t,a+.6,mid(4,.5),sz=30)
    if t>mid(4,.6):
        seal(cv,'s1285',1500,280,mid(4,.6),t,s=.8,r=-4)
        lb(cv,c,'An Nam quốc vương',1500,470,t,mid(4,.75),b+.3,col=RED,sz=44)
def S_5(cv,t):
    a,b=T[5],E[5]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'t5_hamtu',960,560,ay=.5,s=.75,o=.55)
    for k,(x,nm) in enumerate([(480,'Hàm Tử'),(960,'Chương Dương'),(1440,'Tây Kết')]):
        tk=a+.6+k*.5;o=inn(t,tk,.4)*(1-inn(t,mid(5,.6),.4))
        put_screen(cv,A('blot'),x,480,o*.9,s=.22)
        put_screen(cv,text(str(k+1),64,PAPER,700),x,480,o)
        put_screen(cv,text(nm,40,INK,700,glow=3),x,610,o)
    if t>mid(5,.55): put(cv,c,'t5_ao',960,560,s=1.0,o=inn(t,mid(5,.55),.8))
    big(cv,'LỰA CHỌN NÀO SẼ THẮNG?',t,a+.3,mid(5,.55),RED,170,70,seed=5)
    big(cv,'MỘT CHIẾC ÁO CỦA NHÀ VUA',t,mid(5,.65),b+.3,INK,170,60,seed=6)
# ---------------- bản đồ
def S_map(cv,t):
    keys=[(T[6]-.5,(700,560,1.0)),(E[6],(700,560,1.0)),(T[8]-.5,(560,620,1.0)),(E[8],(560,640,1.0)),(T[12]-.5,(460,760,1.6)),(E[12],(460,760,1.6)),(T[17]-.5,(460,720,2.2)),(E[17],(450,690,2.6))]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z)
    c=cam(cx,cy,z)
    mapbg(cv,c,u=inn(t,T[6]-1.0,1.4))
    tl,cha,ls,th,na,tk=[P[k] for k in ['thanglong','chiemthanh','langson2','thanhhoa','nghean','tayket']]
    sz=30 if z<2 else 24
    dot(cv,c,*tl,o=1);tag(cv,c,tl[0]+12,tl[1]+30,'Thăng Long',dy=0,sz=sz)
    tag(cv,c,520,820,'ĐẠI VIỆT',o=.7,sz=44,dy=0,col=np.float32([.25,.22,.18]))
    if t<T[7]:
        tag(cv,c,cha[0]+80,840,'CHIÊM THÀNH',o=inn(t,T[6]+.3,.5),dy=0,sz=36)
        stroke(cv,c,[(600,120),ls,tl,th,(cha[0]-40,cha[1]-20)],inn(t,mid(6,.4),E[6]-mid(6,.4)),wid=7,col=RED,dash=12)
        lb(cv,c,'đòi mượn đường',780,260,t,mid(6,.45),E[6]+.3,col=RED,sz=34)
    elif t<T[9]:
        stroke(cv,c,[(640,120),ls,(500,520)],inn(t,T[8]+.2,1.6),wid=8,col=RED)
        lb(cv,c,'Thoát Hoan',720,330,t,T[8]+.3,E[8]+.3,col=RED,sz=34)
        dot(cv,c,cha[0]-30,850,o=inn(t,mid(8,.5),.4),col=RED);lb(cv,c,'Toa Đô ở Chiêm Thành',cha[0]+150,820,t,mid(8,.5),E[8]+.3,col=RED,sz=34)
    elif t<T[13]:
        stroke(cv,c,[ls,(500,520),tl],inn(t,T[12]+.2,1.4),wid=8,col=RED)
        stroke(cv,c,[(na[0],na[1]+40),na,th,(th[0]+10,th[1]-60)],inn(t,mid(12,.45),1.6),wid=8,col=RED)
        lb(cv,c,'Nghệ An',na[0]+80,na[1]-10,t,mid(12,.5),E[12]+.3,sz=sz);lb(cv,c,'Thanh Hóa',th[0]+90,th[1],t,mid(12,.55),E[12]+.3,sz=sz)
        lb(cv,c,'kẹp từ hai đầu',300,700,t,mid(12,.7),E[12]+.3,col=RED,sz=34)
    else:
        dot(cv,c,*th,o=1,col=RED)
        stroke(cv,c,[th,(th[0]+10,th[1]-80),(tk[0]-10,tk[1]+40),tk],inn(t,T[17]+.2,E[17]-T[17]-.4),wid=7,col=RED)
        lb(cv,c,'Toa Đô ngược lên',th[0]+130,th[1]-120,t,T[17]+.3,E[17]+.3,col=RED,sz=26)
        lb(cv,c,'Thoát Hoan',tl[0]-80,tl[1]-40,t,mid(17,.3),E[17]+.3,col=RED,sz=26)
        lb(cv,c,'sông Hồng',tl[0]+70,tl[1]+80,t,mid(17,.4),E[17]+.3,sz=22)
# ---------------- chương 2
def S_7(cv,t):
    a,b=T[7],E[7]
    c=cam(*cpath(t,[(a-.3,(1400,560,1.5)),(b+.3,(1400,560,1.35))]))
    put(cv,c,'t5_ai',1400,500,ay=.5,s=.65)
    x=lerp(1950,1650,inn(t,a+.2,2.5))
    put(cv,c,Af('ky_mong'),x,730,ay=1,s=.55)
    tagfall(cv,c,x,540,'sứ nhà Nguyên',t,a+.4,sz=34,col=RED)
    lb(cv,c,'mượn đường thì dễ, trả đường mới khó',1400,330,t,a+.6,mid(7,.55),sz=40)
    big(cv,'TỪ CHỐI',t,mid(7,.5),b+.3,RED,200,90,seed=7)
def S_9(cv,t):
    a,b=T[9],E[9]
    c=cam(*cpath(t,[(a-.3,(960,500,1.05)),(b+.3,(960,560,1.18))]))
    put(cv,c,'t5_dien',960,500,s=.9)
    lb(cv,c,'điện Diên Hồng',960,90,t,a+.3,mid(9,.5),sz=42)
    tagfall(cv,c,960,250,'Thượng hoàng Trần Thánh Tông',t,a+.5,sz=30,col=INK,b=mid(9,.6))
    lb(cv,c,'hòa hay đánh?',960,90,t,mid(9,.5),mid(9,.75),col=RED,sz=44)
    big(cv,'ĐÁNH!',t,mid(9,.75),b+.4,RED,420,140,seed=9)
def S_10(cv,t):
    a,b=T[10],E[10]
    c=cam(*cpath(t,[(a-.3,(900,560,1.2)),(b+.3,(980,560,1.05))]))
    put(cv,c,'t5_canhtay',900,600,s=1.0)
    lb(cv,c,'Sát Thát',780,700,t,a+.8,b+.3,col=RED,sz=64)
    lb(cv,c,'giết giặc Mông Cổ',780,300,t,mid(10,.6),b+.3,sz=40)
# ---------------- chương 3
def S_11(cv,t):
    a,b=T[11],E[11];tc=mid(11,.5)
    c=cam(*cpath(t,[(a-.3,(1350,600,1.45)),(b+.3,(1250,620,1.6))]),sx=4*math.sin(t*23)*fio(t,tc,b),sy=3*math.sin(t*19)*fio(t,tc,b))
    put(cv,c,'t5_ai',1400,500,ay=.5,s=.65)
    inf=[(700+i*90,760+(i%2)*12) for i in range(5)]
    for i,(x,y) in enumerate(inf):
        if i in (1,3) and t>tc+.3+i*.3: fall(cv,c,'fig_giap_giao',x,y,t,tc+.3+i*.3,s=.42,dirn=-1)
        else: put(cv,c,'fig_giap_giao',x,y,ay=1,s=.42,o=1-.5*inn(t,mid(11,.8),.8))
    rid=[]
    for i in range(12):
        st=a+.2+i*.2;u=eo(cl((t-st)/3));x=lerp(1500,1000+(i%5)*110,u);y=780+(i%3)*14;rid.append((x,y))
        if u<.98: dust(cv,c,x+120,y-10,o=.3*(1-u))
        put(cv,c,Af('ky_mong'),x,y,ay=1,s=.45,o=inn(t,st,.3))
    arrows(cv,c,t,tc-.6,b,[(x-30,y-100) for x,y in rid[:6]],[(x,y-40) for x,y in inf],n=12,h=80,per=.9,seed=11)
    sparks(cv,c,t,[(980+k*60,720) for k in range(3)],tc,b,seed=11)
    tagfall(cv,c,850,500,'Trần Quốc Tuấn',t,mid(11,.55),sz=30,col=INK)
    lb(cv,c,'Hưng Đạo Đại Vương',850,545,t,mid(11,.6),b+.3,sz=28)
    lb(cv,c,'chặn không nổi',1300,330,t,mid(11,.7),b+.3,col=RED,sz=44)
def S_13(cv,t):
    a,b=T[13],E[13]
    c=cam(960,560,1.0)
    left=PAP.copy();cL=cam(960,560,1.0)
    put(left,cL,'t5_hamtu',900,520,s=.6,o=.7);put(left,cL,'mist',600,620,s=2,o=.5)
    td=a+1.4
    if t<td: put(left,cL,'fig_giap',520,820,ay=1,s=1.0)
    else: fall(left,cL,'fig_giap',520,820,t,td,s=1.0,dirn=-1)
    if t>td+.3: put(left,cL,'redblot',520,760,s=.8*eo(cl((t-td)/1.2)),o=.55)
    right=PAP.copy();cR=cam(960,560,1.0)
    water(right,cR,t,700);put(right,cR,'t5_traitk',1600,560,s=.45,o=.5)
    xb=lerp(900,1500,inn(t,mid(13,.5),b-mid(13,.5)))
    put(right,cR,'smallboat2',xb,760,s=.8,ax=.5,ay=.86,r=bob(t))
    m=np.zeros((H,W,1),np.float32);m[:,W//2:]=1
    cv[:]=left*(1-m)+right*m
    stroke(cv,c,[(960,80),(970,1000)],1,wid=7,head=False,o=.85)
    lb(cv,c,'Trần Bình Trọng ngã xuống',480,240,t,a+.3,b+.3,sz=34)
    lb(cv,c,'bãi Đà Mạc',480,300,t,a+.6,b+.3,sz=28)
    lb(cv,c,'Trần Ích Tắc sang hàng giặc',1440,240,t,mid(13,.5),b+.3,col=RED,sz=34)
def S_14(cv,t):
    a,b=T[14],E[14]
    c=cam(*cpath(t,[(a-.3,(960,540,1.0)),(b+.3,(900,560,1.1))]))
    put(cv,c,'t5_bien',960,540,s=1.0,r=bob(t,.4)*.3)
    lb(cv,c,'vùng biển Thanh Hóa',960,180,t,a+.3,mid(14,.5),sz=40)
    big(cv,'NGƯỜI CHỌN HÀNG ĐÃ ĐÚNG?',t,mid(14,.5),b+.3,RED,170,64,seed=14)
    night(cv,.15)
def S_15(cv,t):
    a,b=T[15],E[15]
    c=cam(*cpath(t,[(a-.3,(700,560,1.0)),(b+.3,(1500,540,1.0))]))
    put(cv,c,'t5_xeluong',1100,640,ay=.5,s=.75)
    lb(cv,c,'thành trống: vua đã đi, lương không có',900,200,t,a+.3,mid(15,.5),sz=38)
    lb(cv,c,'lương chở từ phương bắc, đường rất xa',1400,200,t,mid(15,.5),b+.3,col=RED,sz=38)
def S_16(cv,t):
    a,b=T[16],E[16]
    c=cam(960+10*(t-a),560,1.05)
    put(cv,c,'sun',1500,300,o=.5*(1-inn(t,mid(16,.4),.8)),k=.2)
    put(cv,c,'t5_mua',960,560,s=1.0)
    rain(cv,t,inn(t,mid(16,.35),.8))
    lb(cv,c,'nắng nóng, mưa dầm',960,170,t,a+.3,mid(16,.5),sz=40)
    lb(cv,c,'thiếu ăn, đổ bệnh',960,170,t,mid(16,.55),b+.3,col=RED,sz=40)
# ---------------- bến thứ nhất: Hàm Tử
def S_18(cv,t):
    a,b=T[18],E[20];tc=mid(20,.25)
    sh=fio(t,tc,E[20])
    c=cam(*cpath(t,[(a-.3,(960,620,1.25)),(T[19],(900,640,1.3)),(T[20],(1100,640,1.3)),(b+.3,(1200,640,1.35))]),sx=4*math.sin(t*23)*sh,sy=3*math.sin(t*19)*sh)
    put(cv,c,'t5_hamtu',960,400,ay=.5,s=.7)
    water(cv,c,t,700)
    # quân Nguyên từ phải tiến lên, quay đầu khi rối loạn
    turn=inn(t,mid(20,.45),1.2)
    for i in range(4):
        x=lerp(1900,1450,inn(t,a,3))+i*120+lerp(0,220,turn)
        put(cv,c,'bigboat2' if turn<.5 else Af('bigboat2'),x,740+(i%2)*40,s=.55,ax=.5,ay=.88,r=bob(t,i)+turn*4*(i%2-0.5))
    for i in range(6):
        x=lerp(-200,500,inn(t,a+.4,2.5))+i*110
        put(cv,c,'smallboat2',x,760+(i%3)*30,s=.55,ax=.5,ay=.86,r=bob(t,i))
    lb(cv,c,'Hàm Tử',960,140,t,a+.3,E[18]+.3,col=RED,sz=48)
    tagfall(cv,c,400,520,'Trần Nhật Duật',t,mid(18,.4),sz=36,col=INK,b=T[19])
    if t>T[19]-.2:
        put(cv,c,'t5_tong',520,575,s=.55,o=inn(t,T[19],.6))
        tagfall(cv,c,520,470,'Triệu Trung',t,T[19]+.2,sz=36,col=INK)
        lb(cv,c,'người nhà Tống không chịu hàng',600,220,t,mid(19,.4),E[19]+.3,sz=34)
    if t>T[20]-.2:
        lb(cv,c,'áo quần nước cũ',560,220,t,T[20]+.1,mid(20,.4),sz=36)
        arrows(cv,c,t,tc,b,[(400+k*100,700) for k in range(5)],[(1500+k*120,690) for k in range(5)],n=14,h=90,per=.9,seed=18)
        for k in range(4): put(cv,c,'splash',1500+k*140,760,s=.5,o=.6*fio(t,tc+k*.3,tc+k*.3+1.2))
        big(cv,'GIẶC VỠ CHẠY',t,mid(20,.6),b+.3,RED,170,70,seed=20)
# ---------------- bến thứ hai: Chương Dương
def S_21(cv,t):
    a,b=T[21],E[21]
    c=cam(*cpath(t,[(a-.3,(1500,520,1.0)),(b+.3,(1600,520,1.06))]))
    put(cv,c,'t5_chuongduong',1600,420,ay=.5,s=.75)
    water(cv,c,t,700)
    for i in range(6): put(cv,c,'smallboat2',lerp(600,1200,inn(t,a,b-a))+i*100,760+(i%2)*30,s=.55,ax=.5,ay=.86,r=bob(t,i))
    lb(cv,c,'Chương Dương',1600,140,t,a+.3,b+.3,col=RED,sz=48)
    tagfall(cv,c,1000,520,'Thượng tướng Trần Quang Khải',t,mid(21,.35),sz=32,col=INK)
    lb(cv,c,'một người rất trẻ',1300,600,t,mid(21,.75),b+.3,sz=34)
def S_22(cv,t):
    a,b=T[22],E[22]
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(b+.3,(1000,560,1.15))]))
    put(cv,c,'mist',960,600,s=3.4,o=.6)
    put(cv,c,'t5_qua',960,470,s=1.0,o=inn(t,mid(22,.5),.6))
    if t<mid(22,.55):
        put(cv,c,'t5_dien',960,500,s=.9,o=.5)
    lb(cv,c,'ba năm trước',960,140,t,a+.2,mid(22,.5),sz=40)
    tagfall(cv,c,960,220,'Trần Quốc Toản',t,a+.5,sz=40,col=INK)
    lb(cv,c,'bóp nát quả cam',960,220,t,mid(22,.65),b+.3,col=RED,sz=40)
def S_23(cv,t):
    a,b=T[23],E[24];tc=T[24]
    sh=fio(t,tc,b)
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(E[23],(1100,560,1.05)),(b+.3,(1300,560,1.08))]),sx=4*math.sin(t*23)*sh,sy=3*math.sin(t*19)*sh)
    put(cv,c,'t5_chuongduong',1600,420,ay=.5,s=.75,o=.7)
    water(cv,c,t,720)
    put(cv,c,'t5_co',700,800,ay=1,s=.62,r=math.sin(t*1.2)*1.5)
    lb(cv,c,'hơn một nghìn người',700,170,t,a+.3,mid(23,.4),sz=36)
    big(cv,'PHÁ CƯỜNG ĐỊCH, BÁO HOÀNG ÂN',t,mid(23,.4),E[23]+.2,RED,170,56,seed=23)
    if t>tc-.2:
        for i in range(8):
            st=tc+i*.25;u=inn(t,st,2.6);x=lerp(1950+i*40,1400+i*90,u)
            if t>mid(24,.45):
                x=lerp(x,2300,inn(t,mid(24,.45)+i*.1,2.5));put(cv,c,Af('ky_mong'),x,740+(i%2)*20,ay=1,s=.42)
            else: put(cv,c,'ky_mong',x,740+(i%2)*20,ay=1,s=.42,o=inn(t,st,.3))
        for i in range(6):
            st=mid(24,.4)+i*.15;u=inn(t,st,3);put(cv,c,'fig_giap_giao',lerp(800+i*70,1700+i*70,u),760+(i%2)*14,ay=1,s=.4,o=inn(t,st,.3))
        arrows(cv,c,t,tc+.3,mid(24,.5),[(900+k*80,640) for k in range(4)],[(1450+k*90,700) for k in range(5)],n=12,h=90,per=.9,seed=24)
        lb(cv,c,'Thoát Hoan bỏ Thăng Long',1500,170,t,mid(24,.45),b+.3,col=RED,sz=40)
        big(cv,'KINH THÀNH VỀ LẠI',t,mid(24,.75),b+.3,INK,250,56,seed=24)
# ---------------- bến thứ ba: Tây Kết
def S_25(cv,t):
    a,b=T[25],E[25]
    c=cam(*cpath(t,[(a-.3,(960,640,1.35)),(b+.3,(960,620,1.25))]))
    mistbg(cv,c,.6,700)
    for r in range(3): put(cv,c,'army',960+(r-1)*80,800-r*40,ay=1,s=.8-.1*r,o=.95-.25*r)
    tagfall(cv,c,960,560,'Toa Đô',t,a+.3,sz=48,col=RED)
    lb(cv,c,'hai năm đánh ở Chiêm Thành',960,430,t,a+.6,mid(25,.5),sz=34)
    big(cv,'VẪN CÒN RẤT HUNG HÃN',t,mid(25,.6),b+.3,RED,170,64,seed=25)
    night(cv,.25)
def S_26(cv,t):
    a,b=T[26],E[27];tc=T[27]
    sh=fio(t,tc,b)
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(E[26],(1400,520,1.05)),(b+.3,(1300,540,1.15))]),sx=5*math.sin(t*23)*sh,sy=4*math.sin(t*19)*sh)
    put(cv,c,'t5_traitk',1400,420,ay=.5,s=.75)
    water(cv,c,t,760)
    u=inn(t,a+.4,E[26]-a)
    for k in range(3):
        stroke(cv,c,[(200+k*40,820-k*30),(800,700-k*60),(1100+k*150,560-k*20)],u,wid=8,col=INK,o=.7)
        stroke(cv,c,[(2600-k*40,820-k*30),(2000,700-k*60),(1700-k*150,560-k*20)],u,wid=8,col=INK,o=.7)
    lb(cv,c,'Tây Kết',1400,140,t,a+.3,E[26]+.3,col=RED,sz=48)
    lb(cv,c,'hai vua Trần tự cầm quân',1400,210,t,mid(26,.4),E[26]+.3,sz=36)
    if t>tc-.2:
        arrows(cv,c,t,tc,b,[(700+k*100,700) for k in range(4)]+[(2000+k*100,700) for k in range(4)],[(1100+k*100,560) for k in range(7)],n=18,h=110,per=.9,seed=26)
        sparks(cv,c,t,[(1200+k*120,560) for k in range(4)],tc+.2,b,seed=26)
        for k in range(4): put(cv,c,'redblot',1100+k*180,560,s=.6,o=.5*inn(t,tc+.4+k*.3,.6))
        big(cv,'DOANH TRẠI VỠ',t,tc+.1,mid(27,.35),RED,170,80,seed=27)
        tagfall(cv,c,1400,330,'Toa Đô',t,tc+.3,fall=mid(27,.45),sz=44,col=RED)
        xb=lerp(1900,2700,inn(t,mid(27,.65),2.5))
        put(cv,c,Af('smallboat2'),xb,840,s=.55,ax=.5,ay=.86,r=bob(t))
        lb(cv,c,'Ô Mã Nhi chạy ra biển',xb,640,t,mid(27,.7),b+.3,col=RED,sz=30)
def S_28(cv,t):
    a,b=T[28],E[28]
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(b+.3,(960,580,1.12))]))
    mistbg(cv,c,.8,760)
    put(cv,c,'fig_tuong',700,840,ay=1,s=2.0)
    tagfall(cv,c,700,320,'vua Trần Nhân Tông',t,a+.3,sz=38,col=INK)
    y=lerp(380,640,inn(t,mid(28,.6),2.0))
    put(cv,c,'t5_ao',1250,y,s=.8,o=inn(t,mid(28,.55),.6))
    lb(cv,c,'làm bề tôi nên như người này',1100,180,t,mid(28,.25),mid(28,.6),sz=40)
    lb(cv,c,'cởi áo mình sai đem liệm',1100,180,t,mid(28,.62),b+.4,col=RED,sz=40)
# ---------------- đường rút
def S_29(cv,t):
    a,b=T[29],E[30];tc=T[30]
    sh=fio(t,tc,mid(30,.5))
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(b+.3,(1400,540,1.08))]),sx=4*math.sin(t*23)*sh)
    put(cv,c,'t5_vankiep',1400,460,ay=.5,s=.75)
    lb(cv,c,'Vạn Kiếp',1400,130,t,a+.3,E[29]+.3,col=RED,sz=48)
    for i in range(8):
        x=lerp(2300,800,cl((t-a-i*.15)/(b-a)))+i*80;y=720+(i%2)*14
        if i==3 and t>tc+.6: fall(cv,c,Af('ky_mong'),x,y,t,tc+.6,s=.45,dirn=1);continue
        put(cv,c,Af('ky_mong'),x,y,ay=1,s=.45)
    if t>tc-.3:
        arrows(cv,c,t,tc,mid(30,.5),[(700+k*90,560) for k in range(4)]+[(2100+k*90,560) for k in range(4)],[(1100+k*120,660) for k in range(6)],n=18,h=60,per=.85,seed=29)
        tagfall(cv,c,1400,300,'Lý Hằng trúng tên độc',t,tc+.6,sz=34,col=RED,b=mid(30,.5))
        u=inn(t,mid(30,.5),b-mid(30,.5));put(cv,c,Af('t5_ongdong'),lerp(1800,1100,u),740,ay=1,s=.6,o=inn(t,mid(30,.5),.4))
        lb(cv,c,'chui vào ống đồng',1400,300,t,mid(30,.55),b+.3,sz=38)
def S_31(cv,t):
    a,b=T[31],E[31]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'t5_ngai',960,520,s=.85)
    tagfall(cv,c,960,330,'Trần Ích Tắc',t,a+.3,sz=42,col=INK)
    lb(cv,c,'An Nam quốc vương',960,400,t,a+.6,b+.3,col=RED,sz=40)
    big(cv,'CHƯA MỘT NGÀY ĐƯỢC LÀM VUA',t,mid(31,.55),b+.3,RED,170,56,seed=31)
def S_end(cv,t):
    a=T[32]
    c=cam(960,560,1.0+.015*(t-a))
    mistbg(cv,c,.9,760);put(cv,c,'sun',1600,520,o=.4,k=.2);flock(cv,c,t,.6)
    put(cv,c,'t5_ao',1400,620,s=.5,o=.85)
    put(cv,c,'fig_giap',520,820,ay=1,s=1.1,o=.8)
    tx=text('Thà làm quỷ nước Nam',64,INK,700);put_screen(cv,wipe(tx,inn(t,a+.3,1.2),0,.3,seed=13),W/2,240)
    seal(cv,'stitle5',W/2,450,mid(32,.5),t,s=.6,r=3)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,H-80,inn(t,E[32]+.5,1))
S=lambda n:T[n]-.3
SH=[(0,S(2),S_1),(S(2),S(3),S_2),(S(3),S(4),S_3),(S(4),S(5),S_4),(S(5),S(6),S_5),(S(6),S(7),S_map),(S(7),S(8),S_7),(S(8),S(9),S_map),(S(9),S(10),S_9),(S(10),S(11),S_10),
 (S(11),S(12),S_11),(S(12),S(13),S_map),(S(13),S(14),S_13),(S(14),S(15),S_14),(S(15),S(16),S_15),(S(16),S(17),S_16),(S(17),S(18),S_map),
 (S(18),S(21),S_18),(S(21),S(22),S_21),(S(22),S(23),S_22),(S(23),S(25),S_23),(S(25),S(26),S_25),(S(26),S(28),S_26),(S(28),S(29),S_28),
 (S(29),S(31),S_29),(S(31),S(32),S_31),(S(32),V.TOTAL+1,S_end)]
def ov(cv,t):
    if T[6]-4.2<t<T[6]+.2: title(cv,t,T[6]-3.6,'HÀM TỬ · TÂY KẾT','stitle5',.6)
V.NHAN={3: 'Trần Bình Trọng – tướng nhà Trần', 4: 'Trần Ích Tắc – em Thượng hoàng, sang hàng giặc', 8: ['Hốt Tất Liệt – hoàng đế nhà Nguyên', 'Thoát Hoan – con trai Hốt Tất Liệt', 'Toa Đô – tướng nhà Nguyên ở phía nam'], 9: 'Diên Hồng – nơi vua hỏi ý các bô lão', 11: 'Trần Quốc Tuấn – Hưng Đạo Đại Vương, tổng chỉ huy', 18: 'Trần Nhật Duật – tướng nhà Trần', 19: 'Triệu Trung – người nhà Tống chạy sang Đại Việt', 21: 'Trần Quang Khải – Thượng tướng nhà Trần', 22: 'Trần Quốc Toản – tướng trẻ nhà Trần', 27: 'Ô Mã Nhi – tướng thủy quân nhà Nguyên', 28: 'Trần Nhân Tông – vua Đại Việt'}
def frame(t): return K.compose(V,SH,t,ov,CARDS)
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
