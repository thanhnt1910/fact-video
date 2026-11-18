# Bản dài tm9: Rạch Gầm, Xoài Mút 1785 (bộ tranh riêng t9_*, bản đồ phương Nam)
import math,json
import khung_dung as K
from khung_dung import cam,cpath,PAP,W,H,title
from canh import *
from fx_tran import arrows,dust,sparks,fall
from dai_tm2 import big,tagfall,strike,lb
from dai_tm3 import night
V=K.setup('tm9',{5:4.0,9:2.6,13:2.6,17:2.6,22:2.6})
T,E,mid,TX=V.T,V.E,V.mid,V.TX
PN=json.load(open('/tmp/gen/bd/a/map_nam_pts.json'))
CARDS={9:'Quân Xiêm sang',13:'Nguyễn Huệ vào nam',17:'Khúc sông',22:'Người cầu cứu'}
def bob(t,i=0): return math.sin(t*1.3+i)*1.2
def mapnam(cv,c,u=1.0):
    """sơ đồ vị trí (không vẽ bờ biển vì không có dữ liệu bờ biển phương Nam): điểm đặt đúng kinh vĩ độ"""
    put(cv,c,'mist',960,540,s=5,o=.35*u)
    put_screen(cv,text('sơ đồ vị trí',26,INK,600),150,1000-0,.5*u) if False else None
def water(cv,c,t,wl,o=1):
    Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=PAP[Ys:]
    put(cv,c,'water',960,wl-24,ay=0,o=o)
    for i,yy in enumerate([wl+8,wl+90,wl+210]): put(cv,c,'wave',960-((t*(18+i*9))%200)+(i*77),yy,ay=.5,o=.4-.1*i)
def S_1(cv,t):
    c=cam(*cpath(t,[(0,(960,520,1.12)),(E[1]+.3,(960,540,1.0))]))
    if t<1.4: u=eo(t/1.3);put_screen(cv,A('blot'),W/2,H/2,(1-u)*.85,s=1.9*(1+u*.9))
    put(cv,c,'t9_cau',960,560,s=.95)
    big(cv,'MỜI QUÂN NƯỚC KHÁC VÀO?',t,.25,E[1]+.3,RED,110,72,seed=1)
def S_2(cv,t):
    a,b=T[2],E[2]
    c=cam(*cpath(t,[(a-.3,(700,600,1.2)),(b+.3,(800,560,1.1))]))
    put(cv,c,'t9_cau',960,500,s=.95)
    tagfall(cv,c,560,420,'Nguyễn Ánh',t,a+.3,sz=44,col=INK)
    lb(cv,c,'sang nước Xiêm xin quân',800,330,t,mid(2,.5),b+.3,col=RED,sz=40)
def S_3(cv,t):
    a,b=T[3],E[3]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(b+.3,(1400,560,1.1))]))
    if t<mid(3,.4): put(cv,c,'t9_hamdoi',1400,460,ay=.5,s=.75)
    else:
        put(cv,c,'t9_xac',1400,460,ay=.5,s=.75,o=inn(t,mid(3,.4),.6))
        lb(cv,c,'sông Tiền',1400,250,t,mid(3,.45),b+.3,sz=40)
    lb(cv,c,'mấy vạn quân nước Xiêm',1400,250,t,a+.3,mid(3,.4),col=RED,sz=40)
def S_4(cv,t):
    a,b=T[4],E[4]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'t9_lang',520,600,s=.35,o=inn(t,mid(4,.55),.5));put(cv,c,'t9_khucsong',1420,600,s=.35,o=inn(t,mid(4,.8),.5))
    lb(cv,c,'những gì quân Xiêm làm',520,420,t,mid(4,.55),b+.3,sz=34);lb(cv,c,'một khúc sông chọn sẵn',1420,420,t,mid(4,.8),b+.3,col=RED,sz=34)
    big(cv,'LỜI CẦU CỨU KẾT THÚC RA SAO?',t,a+.2,mid(4,.55),RED,170,60,seed=4)
def S_map(cv,t):
    keys=[(T[5]-.5,(1300,500,1.0)),(E[5],(1300,500,1.0)),(T[7]-.5,(900,560,1.0)),(E[8],(900,560,1.0)),(T[9]-.5,(1100,800,1.8)),(E[9],(1150,800,1.8))]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z)
    c=cam(cx,cy,z)
    mapnam(cv,c,u=inn(t,T[5]-1.0,1.4))
    gd,qn,bk,pq,rg,to,sd,mt=[PN[k] for k in ['giadinh','quynhon','bangkok','phuquoc','rachgia','traon','sadec','manthit']]
    sz=26 if z<1.5 else 22
    dot(cv,c,*gd,o=1);tag(cv,c,gd[0]+16,gd[1]-20,'Gia Định',dy=0,sz=sz)
    if t<T[7]:
        dot(cv,c,*qn,o=1);tag(cv,c,qn[0]-30,qn[1]-24,'Quy Nhơn · Tây Sơn',dy=0,sz=sz)
        stroke(cv,c,[qn,(qn[0]-150,qn[1]+300),(gd[0]+40,gd[1]-20)],inn(t,T[5]+.4,2),wid=8,col=INK)
        lb(cv,c,'nhiều lần đánh vào Gia Định',qn[0]-200,qn[1]+200,t,mid(5,.5),E[5]+.3,sz=sz)
        if t>T[6]-.2:
            stroke(cv,c,[gd,(gd[0]-200,gd[1]+100),pq],inn(t,T[6]+.3,2),wid=6,col=RED,dash=10);lb(cv,c,'Nguyễn Ánh chạy ra đảo',pq[0]+40,pq[1]-60,t,mid(6,.4),E[6]+.3,col=RED,sz=sz)
    elif t<T[10]:
        dot(cv,c,*bk,o=1,col=RED);tag(cv,c,bk[0]+10,bk[1]-26,'nước Xiêm',dy=0,sz=sz,col=RED)
        seal(cv,'s1784',400,260,T[7]+.2,t,s=.6,r=-4)
        stroke(cv,c,[pq,(bk[0]+100,bk[1]+60),bk],inn(t,T[7]+.4,1.6),wid=5,col=INK,dash=10)
        if t>T[8]-.2:
            stroke(cv,c,[bk,(bk[0]+120,bk[1]+300),(rg[0]-60,rg[1]),rg],inn(t,T[8]+.2,2),wid=9,col=RED)
            lb(cv,c,'hai vạn thủy binh, ba trăm chiến thuyền',bk[0]+260,bk[1]+170,t,T[8]+.3,E[9]+.3,col=RED,sz=sz)
            lb(cv,c,'ba vạn quân bộ',bk[0]+260,bk[1]+220,t,mid(8,.5),E[9]+.3,col=RED,sz=sz)
        if t>T[9]-.2:
            for k,(p,nm) in enumerate([(rg,'Rạch Giá'),(to,'Trà Ôn'),(sd,'Sa Đéc'),(mt,'Mân Thít')]):
                dot(cv,c,*p,o=inn(t,T[9]+.3+k*.5,.3),col=RED);tag(cv,c,p[0]+10,p[1]+22,nm,o=inn(t,T[9]+.3+k*.5,.3),dy=0,sz=sz,col=RED)
def S_5(cv,t):
    a,b=T[5],E[5]
    c=cam(*cpath(t,[(a-.3,(1100,520,1.0)),(b+.3,(1500,540,1.06))]))
    put(cv,c,'t9_quynhon',1400,460,ay=.5,s=.75)
    for i in range(10): put(cv,c,Af('fig_giap_giao'),lerp(1500,2300,inn(t,a+.3+i*.1,b-a))+i*60,760+(i%2)*10,ay=1,s=.4)
    tagfall(cv,c,1300,650,'Nguyễn Nhạc · Nguyễn Huệ · Nguyễn Lữ',t,a+.4,sz=34,col=INK)
    lb(cv,c,'nhiều lần đánh vào Gia Định',1500,180,t,mid(5,.5),b+.3,col=RED,sz=40)
def S_7(cv,t):
    a,b=T[7],E[7]
    c=cam(*cpath(t,[(a-.3,(1100,560,1.1)),(b+.3,(1200,540,1.0))]))
    put(cv,c,'t9_cau',960,500,s=.95)
    seal(cv,'s1784',1650,250,a+.3,t,s=.7,r=-4)
    lb(cv,c,'vua Xiêm nhận lời',1200,130,t,mid(7,.35),b+.3,col=RED,sz=40)
    tagfall(cv,c,1500,620,'Chiêu Tăng, Chiêu Sương',t,mid(7,.6),sz=36,col=RED)
def S_8(cv,t):
    a,b=T[8],E[8]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(b+.3,(1300,540,1.08))]))
    put(cv,c,'t9_hamdoi',lerp(1500,1300,inn(t,a,b-a)),480,ay=.5,s=.75)
    lb(cv,c,'hai vạn thủy binh, ba trăm chiến thuyền',1400,170,t,a+.3,b+.3,col=RED,sz=40)
    lb(cv,c,'thêm ba vạn quân bộ',1400,240,t,mid(8,.6),b+.3,sz=36)
def S_9(cv,t):
    a,b=T[9],E[9]
    c=cam(*cpath(t,[(a-.3,(1600,520,1.0)),(b+.3,(1200,540,1.0))]))
    put(cv,c,'t9_lang',1400,480,ay=.5,s=.75,o=.8)
    for k,(x,nm) in enumerate([(700,'Rạch Giá'),(1150,'Trà Ôn'),(1600,'Sa Đéc'),(2050,'Mân Thít')]):
        tk=a+.4+k*(b-a-.8)/4;dot(cv,c,x,300,o=inn(t,tk,.3),col=RED,r=12);tag(cv,c,x,250,nm,o=inn(t,tk,.3),dy=0,sz=36,col=RED)
    lb(cv,c,'cả một dải miền Tây',1400,150,t,mid(9,.7),b+.3,sz=40)
def S_6(cv,t):
    a,b=T[6],E[6]
    c=cam(*cpath(t,[(a-.3,(1400,560,1.1)),(b+.3,(1400,560,1.0))]))
    put(cv,c,'t9_dao',1400,500,ay=.5,s=.75)
    tagfall(cv,c,1400,330,'Nguyễn Ánh',t,a+.3,sz=40,col=INK)
    lb(cv,c,'trốn ra các đảo ngoài biển',1400,200,t,mid(6,.55),b+.3,col=RED,sz=40)
def S_10(cv,t):
    a,b=T[10],E[10]
    c=cam(*cpath(t,[(a-.3,(1500,520,1.0)),(b+.3,(1300,540,1.08))]))
    put(cv,c,'t9_hamdoi',1400,480,ay=.5,s=.75)
    lb(cv,c,'tưởng như đã chọn đúng',1400,200,t,mid(10,.5),b+.3,col=RED,sz=40)
def S_11(cv,t):
    a,b=T[11],E[12]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(T[12],(1400,540,1.08)),(b+.3,(1300,560,1.15))]))
    put(cv,c,'t9_lang',1400,480,ay=.5,s=.75)
    for i in range(6): put(cv,c,Af('fig_giap_giao'),lerp(1900,1200,inn(t,a,b-a))+i*90,700+(i%2)*10,ay=1,s=.42,o=.85)
    lb(cv,c,'cướp phá',1400,200,t,a+.3,mid(11,.5),col=RED,sz=44)
    lb(cv,c,'sử nhà Nguyễn cũng chép: dân rất oán',1400,200,t,mid(11,.55),E[11]+.3,sz=38)
    if t>T[12]-.2: big(cv,'THỨ ĐẦU TIÊN',t,T[12]+.1,b+.3,RED,170,70,seed=12)
def S_13(cv,t):
    a,b=T[13],E[13]
    c=cam(*cpath(t,[(a-.3,(1300,520,1.0)),(b+.3,(1500,540,1.08))]))
    put(cv,c,'t9_quynhon',1400,460,ay=.5,s=.75)
    lb(cv,c,'Quy Nhơn',1400,170,t,a+.3,mid(13,.5),sz=44)
    tagfall(cv,c,1300,630,'Nguyễn Huệ',t,mid(13,.55),sz=44,col=RED)
    lb(cv,c,'đem quân vào nam',1300,700,t,mid(13,.6),b+.3,sz=34)
def S_14(cv,t):
    a,b=T[14],E[16]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(T[15],(1400,540,1.05)),(T[16],(1400,560,1.1)),(b+.3,(1400,560,1.12))]))
    put(cv,c,'t9_khucsong',1400,480,ay=.5,s=.75)
    lb(cv,c,'không đánh thẳng',1400,180,t,a+.3,E[14]+.3,sz=40)
    if t>T[15]-.2:
        lb(cv,c,'rạch Gầm',800,250,t,T[15]+.2,b+.3,col=RED,sz=36);lb(cv,c,'rạch Xoài Mút',2000,250,t,T[15]+.5,b+.3,col=RED,sz=36)
        lb(cv,c,'cù lao Thới Sơn',1400,380,t,mid(15,.5),b+.3,sz=32)
    if t>T[16]-.2:
        for k,(x,y) in enumerate([(700,300),(1200,300),(1700,300),(2100,300),(900,630),(1600,630)]):
            put(cv,c,'t9_daibac' if x<1400 else Af('t9_daibac'),x,y,ay=1,s=.22,o=inn(t,T[16]+k*.2,.4))
        big(cv,'THỨ HAI: KHÚC SÔNG',t,mid(16,.6),b+.3,RED,170,64,seed=16)
def S_17(cv,t):
    a,b=T[17],E[18]
    c=cam(*cpath(t,[(a-.3,(1600,520,1.0)),(T[18],(1400,540,1.05)),(b+.3,(1400,540,1.08))]))
    put(cv,c,'t9_khucsong',1400,480,ay=.5,s=.75)
    x=lerp(2800,1300,inn(t,a,b-a))
    put(cv,c,'t9_hamdoi',x,480,ay=.5,s=.42)
    lb(cv,c,'đoàn chiến thuyền nước Xiêm',1400,170,t,a+.3,E[17]+.3,col=RED,sz=38)
    big(cv,'HAI BỜ VẪN IM',t,T[18]+.3,b+.3,INK,170,70,seed=18)
def S_19(cv,t):
    a,b=T[19],E[21];tc=T[19]+.2
    sh=fio(t,tc,E[20])
    c=cam(*cpath(t,[(a-.3,(1400,540,1.08)),(T[20],(1400,560,1.15)),(b+.3,(1300,560,1.1))]),sx=5*math.sin(t*23)*sh,sy=4*math.sin(t*19)*sh)
    put(cv,c,'t9_khucsong',1400,480,ay=.5,s=.75)
    if t<T[21]-.2:
        sk=inn(t,T[20],3)
        put(cv,c,'t9_hamdoi',1300,480+60*sk,ay=.5,s=.42,r=5*sk,o=1-.6*sk)
        for k,(x0,y0) in enumerate([(500,520),(2300,520),(500,440),(2300,440)]):
            x=lerp(x0,1300+(k%2*2-1)*500,inn(t,tc+k*.15,2));put(cv,c,'smallboat2' if x0<1400 else Af('smallboat2'),x,y0+20,s=.45,ax=.5,ay=.86,r=bob(t,k))
        for k,(x,y) in enumerate([(700,300),(1200,300),(1700,300),(2100,300),(900,630),(1600,630)]):
            put(cv,c,'t9_daibac' if x<1400 else Af('t9_daibac'),x,y,ay=1,s=.22)
            if t>tc+.3: put(cv,c,'redblot',x+(60 if x<1400 else -60),y-50,s=.25,o=.6*fio(t,tc+.3+k*.25,tc+.9+k*.25))
        arrows(cv,c,t,tc+.2,E[20],[(700,280),(1200,280),(1700,280),(2100,280),(900,610),(1600,610)],[(1100+k*100,470) for k in range(5)],n=12,h=60,per=.7,seed=19)
        for k in range(5): put(cv,c,'splash',1050+k*120,520,s=.4,o=.55*fio(t,tc+.6+k*.3,tc+1.6+k*.3))
        lb(cv,c,'chặn cả đầu lẫn đuôi',1400,170,t,tc,E[19]+.3,col=RED,sz=40)
        big(cv,'KHÔNG CÒN LỐI THOÁT',t,T[20]+.1,E[20]+.3,RED,170,70,seed=20)
    else:
        put(cv,c,'t9_rung',1400,500,ay=.5,s=.75)
        for i in range(8): put(cv,c,Af('fig_giap_giao'),lerp(900,1900,inn(t,T[21]+i*.15,4))+i*50,760+(i%2)*10,ay=1,s=.45)
        lb(cv,c,'Chiêu Tăng, Chiêu Sương chạy bộ qua Chân Lạp',1400,170,t,T[21]+.2,b+.3,sz=36)
def S_22(cv,t):
    a,b=T[22],E[23]
    c=cam(*cpath(t,[(a-.3,(1400,520,1.0)),(T[23],(960,540,1.0)),(b+.3,(960,560,1.06))]))
    if t<T[23]-.1:
        put(cv,c,'t9_dao',1400,480,ay=.5,s=.75);night(cv,.35)
        tagfall(cv,c,1400,330,'Nguyễn Ánh',t,a+.3,sz=44,col=INK)
        lb(cv,c,'chạy về chính nước Xiêm',1400,200,t,mid(22,.5),E[22]+.3,col=RED,sz=40)
    else:
        put(cv,c,'t9_cau',960,500,s=.95)
        lb(cv,c,'sợ quân nhà Tây Sơn như sợ cọp',960,130,t,T[23]+.3,b+.3,col=RED,sz=40)
def S_end(cv,t):
    a=T[24]
    c=cam(960,560,1.0+.015*(t-a))
    put(cv,c,'t9_khucsong',960,480,ay=.5,s=.7);put(cv,c,'sun',1600,360,o=.45,k=.2);flock(cv,c,t,.6)
    tx=text('Khúc sông chọn sẵn',64,INK,700);put_screen(cv,wipe(tx,inn(t,a+.3,1.2),0,.3,seed=13),W/2,230)
    seal(cv,'stitle9',W/2,430,mid(24,.5),t,s=.55,r=3)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,H-80,inn(t,E[24]+.5,1))
S=lambda n:T[n]-.3
SH=[(0,S(2),S_1),(S(2),S(3),S_2),(S(3),S(4),S_3),(S(4),S(5),S_4),(S(5),S(6),S_5),(S(6),S(7),S_6),(S(7),S(8),S_7),(S(8),S(9),S_8),(S(9),S(10),S_9),(S(10),S(11),S_10),
 (S(11),S(13),S_11),(S(13),S(14),S_13),(S(14),S(17),S_14),(S(17),S(19),S_17),(S(19),S(22),S_19),(S(22),S(24),S_22),(S(24),V.TOTAL+1,S_end)]
def ov(cv,t):
    TT=V.TTL or T[5]
    if TT-4.2<t<TT+.2: title(cv,t,TT-3.6,'RẠCH GẦM · XOÀI MÚT','stitle9',.55)
V.NHAN={2: 'Nguyễn Ánh – người còn lại của họ Nguyễn', 3: 'nước Xiêm – Thái Lan ngày nay', 7: 'Chiêu Tăng, Chiêu Sương – tướng nước Xiêm', 13: 'Nguyễn Huệ – em Nguyễn Nhạc, chỉ huy quân Tây Sơn', 15: 'Rạch Gầm, Xoài Mút – Tiền Giang ngày nay'}
def S_chen(cv,t):
    ks=sorted(k for k in V.T if 4<k<5);a,b=V.T[ks[0]],V.E[ks[-1]]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'mist',960,560,s=5,o=.5)
    lb(cv,c,'hơn hai trăm năm trước',960,150,t,a+.3,b+.3,sz=36)
    cols=[(480,'CHÚA TRỊNH','phía bắc',INK),(1440,'CHÚA NGUYỄN','phía nam',INK)]
    for k,(x,nm,sub,col) in enumerate(cols):
        o=inn(t,mid(ks[0],.4)+k*.4,.5);put_screen(cv,text(nm,60,col,700,glow=4),x,420,o);put_screen(cv,text(sub,32,INK,600,glow=3),x,490,o)
    stroke(cv,c,[(960,330),(965,620)],inn(t,mid(ks[0],.5),.6),wid=6,head=False,o=.8)
    if t>V.T[ks[-1]]-.2:
        o=inn(t,V.T[ks[-1]]+.2,.5);put_screen(cv,text('NHÀ TÂY SƠN',60,RED,700,glow=4),1440,640,o);put_screen(cv,text('ba anh em ở Quy Nhơn nổi dậy',32,RED,600,glow=3),1440,710,o)
        stroke(cv,c,[(1440,600),(1440,520)],inn(t,mid(ks[-1],.5),.6),wid=8,col=RED)

def _chen_sh():
    if V.TTL:
        i=[k for k,s in enumerate(SH) if s[2] is S_4][0];a0,b0,fn=SH[i];k1=min(k for k in V.T if 4<k<5)
        SH[i]=(a0,V.T[k1]-.3,fn);SH.insert(i+1,(V.T[k1]-.3,b0,S_chen))
_chen_sh()
def frame(t): return K.compose(V,SH,t,ov,CARDS)
TOTAL=V.TOTAL
if __name__=='__main__': K.main(V,frame)
