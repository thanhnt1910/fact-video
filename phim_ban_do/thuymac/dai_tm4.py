# Bản dài tm4: Đông Bộ Đầu 1258 (giọng Charon gốc, không cân giọng)
import sys,os,subprocess,json,math
import dai
from dai import cam,cpath,to8,stage,PAP,W,H,XM,NM
from canh import *
from fx_tran import arrows,dust,sparks,fall
from dai_tm2 import big,tagfall,strike,lb,dongho,scene_bg,ground
from dai_tm3 import night,banks
GD=os.environ.get('GIONG','/tmp/pc/assets/thu_giong_hai/charon')
J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm4_full.json'))
TX={i+1:d['text'] for i,d in enumerate(J)};NN={i+1:d['n'] for i,d in enumerate(J)}
def dur(i):
    f=f'{GD}/{NN[i]}.mp3'
    if os.path.exists(f):
        return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    return len(TX[i].split())/3.1+.2
GAP={6:4.0,11:2.6,20:2.6,24:2.6,29:2.6}
T={};E={};t=0.5
for n in TX:
    t+=GAP.get(n,0);T[n]=t;d=dur(n);E[n]=t+d;t+=d+.45
TOTAL=t+4.5
def mid(n,f): return T[n]+(E[n]-T[n])*f
CARDS={11:'Bình Lệ Nguyên',20:'Kinh thành trống',24:'Mười hai ngày sau',29:'Đường rút'}
P=PTS
def riv(cv,c,t,wl=620,mist=.6,dark=0.0):
    put(cv,c,'far',960,760,ay=1,k=.35,o=.45)
    put(cv,c,'mist',900,640,s=2.8,o=mist,k=.45)
    Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=PAP[Ys:]
    put(cv,c,'water',960,wl-24,ay=0)
    for i,yy in enumerate([wl+8,wl+90,wl+210]):
        put(cv,c,'wave',960-((t*(18+i*9))%200)+(i*77),yy,ay=.5,o=.4-.1*i)
def boatbob(t,i=0): return math.sin(t*1.3+i)*1.2
# ---------------- chương 1
def S_h1(cv,t):
    c=cam(*cpath(t,[(0,(960,560,1.12)),(T[2]-.3,(960,560,1.0))]))
    riv(cv,c,t,640,.7)
    if t<1.4:
        u=eo(t/1.3);put_screen(cv,A('blot'),W/2,H/2,(1-u)*.85,s=1.9*(1+u*.9))
    put(cv,c,'lau_thuyen',960,700,ay=.86,s=.55,r=boatbob(t))
    for i in range(4): put(cv,c,'smallboat2',300+i*130+(i%2)*40,720+(i%2)*30,s=.5,ax=.5,ay=.86,scale_px=1.5)
    night(cv,.35)
    big(cv,'KINH THÀNH SẮP MẤT',t,.25,E[1]+.2,RED,190,84,seed=1)
def S_h2(cv,t):
    a,b=T[2],E[2]
    c=cam(960+8*(t-a),540,1.0)
    put(cv,c,'man_thuyen',960,1080,ay=1,s=1.0)
    u=inn(t,a+.6,2.2)
    for k,(x0,dx) in enumerate([(560,330),(1030,330)]):
        uk=cl(u*2-k)
        if uk>0:
            pts=[(x0+dx*j/10,560+50*math.sin(j*1.3+k)) for j in range(11)]
            pts=pts[:max(2,int(len(pts)*uk))]
            stroke(cv,c,pts,1,wid=18,head=False,col=np.float32([.62,.58,.5]),o=.55)
    lb(cv,c,'sang nhà Tống',960,110,t,mid(2,.45),b+.3,col=RED,sz=56)
def S_h3(cv,t):
    a,b=T[3],E[3]
    c=cam(*cpath(t,[(a-.3,(960,560,1.05)),(b+.3,(960,540,1.12))]))
    riv(cv,c,t,640,.7)
    put(cv,c,'lau_thuyen',960,700,ay=.86,s=.55,r=boatbob(t))
    night(cv,.35)
    big(cv,'ĐẦU THẦN CHƯA RƠI XUỐNG ĐẤT',t,mid(3,.3),b+.3,RED,190,70,seed=3)
def S_h4(cv,t):
    a,b=T[4],E[5]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(T[5],(960,560,1.0)),(b+.4,(960,520,1.06))]))
    riv(cv,c,t,700,.6)
    put(cv,c,'lau_thuyen',960,780,ay=.86,s=.75,r=boatbob(t),o=.5)
    for i,(nm,im,x) in enumerate([('Trần Thái Tông','fig_giap',960),('Trần Nhật Hiệu','fig_quan_dung',620),('Trần Thủ Độ',Af('fig_quan_dung'),1300)]):
        put(cv,c,im,x,700,ay=1,s=1.0,o=inn(t,a+.2+i*.6,.4)*(1-.6*inn(t,T[5],.6)))
        tagfall(cv,c,x,320,nm,t,a+.3+i*.7,sz=40,col=INK,b=T[5])
    if t>T[5]-.2:
        for i in range(8):
            u=cl((t-T[5]-i*.15)/4)
            put(cv,c,Af('ky_mong'),lerp(2100+i*90,1300+i*90,u),560-(i%2)*20,ay=1,s=.4,o=inn(t,T[5]+i*.15,.4))
        lb(cv,c,'quân Mông Cổ',1500,330,t,T[5]+.3,mid(5,.45),col=RED,sz=44)
        big(cv,'Lời hứa thật, hay lời trấn an?',t,mid(5,.45),E[5]+.3,INK,190,60,seed=5)
def S_title(cv,t):
    t0=T[6]-3.6
    u=inn(t,t0-.3,.8);put_screen(cv,A('blot'),W/2,H/2,u*.97*(1-inn(t,t0+3.2,.6)),s=1.5+.1*(t-t0),r=4*(t-t0))
    tt=text('ĐÔNG BỘ ĐẦU',96,PAPER,700);put_screen(cv,wipe(tt,inn(t,t0+.2,.8),0,.3,seed=3),W/2,H/2-30,1-inn(t,t0+3.2,.5))
    seal(cv,'s1257',W/2+420,H/2+110,t0+1.1,t,s=.75,o=1-inn(t,t0+3.2,.5),r=4)
# ---------------- bản đồ
def S_map(cv,t):
    keys=[(T[6]-.5,(400,420,1.4)),(E[6],(420,440,1.4)),(T[10]-.5,(340,440,1.5)),(E[10],(380,480,1.6)),(T[11]-.5,(420,560,2.4)),(E[11],(420,570,2.6)),
          (T[14]-.5,(440,600,2.4)),(E[14],(440,610,2.4)),(T[26]-.5,(440,620,2.8)),(E[26],(440,620,2.8)),(T[33]-.5,(520,440,1.1)),(E[33],(520,440,1.1))]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z)
    c=cam(cx,cy,z)
    mapbg(cv,c,u=inn(t,T[6]-1.0,1.4))
    tl,bl,lc,qh,tm,pt=[P[k] for k in ['thanglong','binhle','laocai','quyhoa','thienmac','phutho']]
    sz=30 if z<2 else 26
    dot(cv,c,*tl,o=1);tag(cv,c,tl[0]+12,tl[1]+30,'Thăng Long',dy=0,sz=sz)
    tag(cv,c,520,820,'ĐẠI VIỆT',o=.8,sz=44,dy=0,col=np.float32([.25,.22,.18]))
    if t<T[7]:   # đoạn 6: Đại Lý / Vân Nam
        tag(cv,c,lc[0]+90,lc[1]-120,'VÂN NAM',o=inn(t,T[6]+.2,.5),dy=0,sz=44,col=RED)
        stroke(cv,c,[(lc[0]-40,lc[1]-200),(lc[0],lc[1]-60)],inn(t,mid(6,.4),1.0),wid=8,col=RED)
        lb(cv,c,'quân Mông Cổ vừa chiếm Đại Lý',lc[0]+200,lc[1]-210,t,mid(6,.45),E[6]+.3,col=RED,sz=30)
    elif t<T[12]:  # đoạn 10-11
        stroke(cv,c,[(lc[0]-20,lc[1]-60),lc,qh,pt,bl],inn(t,T[10]+.3,E[10]-T[10]),wid=8,col=RED)
        tag(cv,c,(lc[0]+qh[0])/2+60,(lc[1]+qh[1])/2,'sông Thao',o=inn(t,mid(10,.5),.5),dy=0,sz=sz)
        if t>T[11]-.3:
            dot(cv,c,*bl,o=1,col=RED);tag(cv,c,bl[0]-10,bl[1]-26,'Bình Lệ Nguyên',dy=0,sz=sz,col=RED)
            stroke(cv,c,[bl,tl],inn(t,mid(11,.5),1.0),wid=3,head=False,dash=6,o=.85)
            tag(cv,c,(bl[0]+tl[0])/2+10,(bl[1]+tl[1])/2-24,'chừng ba mươi cây số',o=inn(t,mid(11,.6),.5),dy=0,sz=sz)
    elif t<T[15]:  # đoạn 14
        dot(cv,c,*bl,o=1,col=RED);tag(cv,c,bl[0]-10,bl[1]-26,'Bình Lệ Nguyên',dy=0,sz=sz,col=RED)
        stroke(cv,c,[bl,(bl[0]+20,bl[1]+30),tl,(tl[0]+12,tl[1]+20),tm],inn(t,T[14]+.3,E[14]-T[14]),wid=5,col=INK,dash=10)
        dot(cv,c,*tm,o=inn(t,mid(14,.6),.4));tag(cv,c,tm[0]+14,tm[1]+26,'sông Thiên Mạc',o=inn(t,mid(14,.6),.4),dy=0,sz=sz)
    elif t<T[27]:  # đoạn 26
        dot(cv,c,*tm,o=1);tag(cv,c,tm[0]+14,tm[1]+26,'sông Thiên Mạc',dy=0,sz=sz)
        stroke(cv,c,[tm,(tm[0]-6,tm[1]-20),tl],inn(t,T[26]+.2,E[26]-T[26]-.3),wid=6,col=INK)
        tag(cv,c,tl[0]+14,tl[1]-26,'bến Đông Bộ Đầu',o=inn(t,mid(26,.3),.4),dy=0,sz=sz,col=RED)
    else:  # đoạn 33
        for k,(lbl,yy) in enumerate([('năm 1285',380),('năm 1288',470)]):
            stroke(cv,c,[(1100,200+k*60),(800,yy),tl],inn(t,mid(33,.45)+k*.6,1.6),wid=6,col=RED,o=.6,dash=14)
            tag(cv,c,1000,240+k*80,lbl,o=inn(t,mid(33,.5)+k*.6,.4),dy=0,sz=30,col=RED)
        lb(cv,c,'lần thứ nhất',tl[0]-60,tl[1]+130,t,T[33]+.2,E[33]+.3,sz=30)
# ---------------- chương 2
def S_7(cv,t):
    a,b=T[7],E[8]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(1000,580,1.1))]))
    put(cv,c,'cong_cung',960,880,ay=1,s=1.0)
    x=lerp(1700,1150,inn(t,a+.2,3))
    put(cv,c,Af('fig_quan_dung'),x,820,ay=1,s=.85)
    tagfall(cv,c,x,420,'sứ Mông Cổ',t,a+.6,sz=42)
    lb(cv,c,'đòi nhà Trần chịu hàng',x,530,t,mid(7,.55),T[8],col=RED,sz=32)
    seal(cv,'s1257',300,260,a+.2,t,s=1.0,r=-4)
    if t>T[8]-.2:
        for i in range(4): put(cv,c,'fig_giap_giao',x-260+i*160+(80 if i>1 else 0),820,ay=1,s=.75,o=inn(t,T[8]+i*.2,.4))
        lb(cv,c,'giữ sứ giả lại',x,530,t,T[8]+.3,b+.3,sz=34)
        big(cv,'CHỌN ĐÁNH',t,mid(8,.55),b+.3,RED,170,80,seed=8)
def S_9(cv,t):
    a,b=T[9],E[9]
    c=cam(960+20*(t-a),560,1.0)
    scene_bg(cv,c,.5,.6,820);ground(cv,c,830,.25)
    for r in range(2): put(cv,c,'army',500+r*620,800-r*30,ay=1,s=.6-.08*r,o=.95-.2*r)
    put(cv,c,'fig_giap',1500,800,ay=1,s=1.0,o=inn(t,mid(9,.4),.5))
    tagfall(cv,c,1500,440,'Trần Quốc Tuấn',t,mid(9,.4),sz=40,col=INK)
    lb(cv,c,'sau này là Hưng Đạo Đại Vương',1500,520,t,mid(9,.65),b+.3,sz=30)
    lb(cv,c,'giữ biên giới',700,300,t,a+.3,b+.3,sz=40)
# ---------------- chương 3
def S_12(cv,t):
    a,b=T[12],E[13];tc=mid(12,.55)
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(T[13],(900,560,1.05)),(b+.4,(820,580,1.15))]),
          sx=5*math.sin(t*23)*fio(t,tc,E[13]),sy=4*math.sin(t*19)*fio(t,tc,E[13]))
    scene_bg(cv,c,.5,.7,820);ground(cv,c,830,.3)
    fade13=1-.75*inn(t,T[13]-.2,.6)
    for i in range(3): put(cv,c,'voi',420+i*230,820,ay=1,s=.55,o=inn(t,a+.3+i*.2,.4)*fade13)
    inf=[(140,840),(250,850),(960,840),(1060,850),(1160,840),(360,840),(1250,850)]
    for i,(x,y) in enumerate(inf):
        if i in (2,4,5) and t>tc+.4+i*.25: fall(cv,c,'fig_giap_giao',x,y,t,tc+.4+i*.25,s=.5,dirn=-1)
        else: put(cv,c,'fig_giap_giao',x,y,ay=1,s=.5,o=inn(t,a+.2,.4)*fade13)
    tagfall(cv,c,480,420,'Trần Thái Tông',t,a+.4,sz=36,col=INK,b=T[13])
    rid=[]
    for i in range(10):
        st=a+.6+i*.18;u=eo(cl((t-st)/3.0))
        x=lerp(2200+i*60,1280+(i%5)*130,u);y=800+(i%2)*30;rid.append((x,y))
        if u<.98: dust(cv,c,x+150,y-10,o=.3*inn(t,st,.3)*(1-u))
        if i in (1,6) and t>tc+.8+i*.1: fall(cv,c,Af('ky_mong'),x,y,t,tc+.8+i*.1,s=.55,dirn=1)
        else: put(cv,c,Af('ky_mong'),x,y,ay=1,s=.55,o=inn(t,st,.3))
    lb(cv,c,'kỵ binh Mông Cổ',1500,300,t,a+.8,T[13],col=RED,sz=36)
    # hai bên bắn tên: quân Đại Việt bắn ra trước, quân Mông Cổ bắn trả dày dần
    arrows(cv,c,t,a+.7,tc+1.0,[(x+20,y-60) for x,y in inf],[(1450+k*120,740) for k in range(5)],n=10,h=110,per=1.1,seed=12)
    arrows(cv,c,t,a+1.4,b-.6,[(x-40,y-120) for x,y in rid],[(x,y-40) for x,y in inf]+[(500+k*200,760) for k in range(3)],n=16,h=90,per=.95,seed=13)
    sparks(cv,c,t,[(1150+k*110,730-(k%2)*30) for k in range(4)],tc,E[12]+.5,seed=12)
    if t>mid(12,.6):
        for k in range(3): put(cv,c,'redblot',600+k*240,760,s=.6,o=.5*inn(t,mid(12,.6)+k*.2,.6))
    if t>T[13]-.2:
        put(cv,c,'ky_si',lerp(700,960,inn(t,T[13],2)),840,ay=1,s=1.0)
        tagfall(cv,c,lerp(700,960,inn(t,T[13],2)),420,'Lê Phụ Trần',t,T[13]+.2,sz=40,col=INK)
        lb(cv,c,'một mình một ngựa',760,300,t,T[13]+.4,b+.3,sz=38)
def S_15(cv,t):
    a,b=T[15],E[15]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(900,560,1.1))]))
    put(cv,c,'far',960,720,ay=1,k=.4,o=.45)
    put(cv,c,'citadel',900,720,ay=1,s=.8);ground(cv,c,720,.25)
    lb(cv,c,'kinh thành bị bỏ trống',900,250,t,a+.3,mid(15,.5),sz=40)
    if t>mid(15,.45):
        for i in range(9):
            u=cl((t-mid(15,.45)-i*.15)/3.5)
            put(cv,c,Af('ky_mong'),lerp(2000+i*80,1000+i*80,u),820+(i%2)*20,ay=1,s=.5,o=inn(t,mid(15,.45)+i*.15,.3))
        lb(cv,c,'quân Mông Cổ chiếm thành',900,250,t,mid(15,.55),b+.3,col=RED,sz=40)
def S_16(cv,t):
    a,b=T[16],E[18]
    if T[17]-.1<t<T[18]-.1:  # mạn thuyền
        c=cam(960+8*(t-T[17]),540,1.0)
        put(cv,c,'man_thuyen',960,1080,ay=1,s=1.0)
        u=inn(t,mid(17,.45),2.2)
        for k,(x0,dx) in enumerate([(560,330),(1030,330)]):
            uk=cl(u*2-k)
            if uk>0:
                pts=[(x0+dx*j/10,560+50*math.sin(j*1.3+k)) for j in range(11)];pts=pts[:max(2,int(len(pts)*uk))]
                stroke(cv,c,pts,1,wid=18,head=False,col=np.float32([.62,.58,.5]),o=.55)
        tagfall(cv,c,960,170,'Trần Nhật Hiệu',t,T[17]+.2,sz=44,col=INK)
        lb(cv,c,'sang nhà Tống',960,320,t,mid(17,.6),T[18],col=RED,sz=48)
        return
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(E[16],(960,560,1.1)),(T[18],(1100,560,1.15)),(b+.4,(1150,540,1.2))]))
    riv(cv,c,t,700,.6)
    put(cv,c,'lau_thuyen',960,780,ay=.86,s=.75,r=boatbob(t),o=.6)
    night(cv,.3)
    lb(cv,c,'sông Thiên Mạc',960,280,t,a+.3,E[16]+.2,sz=40)
    if t>T[18]-.2:
        put(cv,c,Af('fig_quan_dung'),1250,700,ay=1,s=1.0)
        tagfall(cv,c,1250,320,'Trần Thủ Độ',t,T[18]+.1,sz=42,col=INK)
        lb(cv,c,'người đứng đầu triều đình',1250,400,t,T[18]+.3,mid(18,.5),sz=30)
        big(cv,'ĐẦU THẦN CHƯA RƠI XUỐNG ĐẤT',t,mid(18,.5),b+.3,RED,170,64,seed=18)
def S_19(cv,t):
    a,b=T[19],E[19]
    c=cam(960,560,1.0+.02*(t-a))
    riv(cv,c,t,700,.8)
    put(cv,c,'citadel',1300,640,ay=1,s=.5,o=.5)
    night(cv,.35)
    big(cv,'LẤY GÌ ĐỂ GIỮ LỜI HỨA?',t,mid(19,.4),b+.4,RED,190,70,seed=19)
# ---------------- chương 4
def S_20(cv,t):
    a,b=T[20],E[20]
    c=cam(960+10*(t-a),600,1.05)
    riv(cv,c,t,640,.4)
    put(cv,c,'lau_thuyen',900,720,ay=.86,s=.6,r=boatbob(t))
    for i in range(10): put(cv,c,'smallboat2',200+i*170+(i%2)*40,700+(i%3)*40,s=.5,ax=.5,ay=.86,scale_px=1.5,o=inn(t,a+.2+i*.08,.3))
    lb(cv,c,'chưa mất quân',900,300,t,a+.3,b+.3,sz=44)
def S_21(cv,t):
    a,b=T[21],E[22]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(T[22],(1000,580,1.1)),(b+.4,(1050,600,1.15))]))
    put(cv,c,'far',960,720,ay=1,k=.4,o=.45)
    put(cv,c,'citadel',900,720,ay=1,s=.8);ground(cv,c,720,.25)
    put(cv,c,'trai',1300,860,ay=1,s=.55,o=.95)
    for k in range(3): put(cv,c,'redblot',700+k*220,560,s=.6,o=.45*inn(t,a+.6+k*.3,.6))
    lb(cv,c,'gần như không còn ai',900,250,t,a+.3,mid(21,.55),sz=40)
    lb(cv,c,'không có lương thực',900,250,t,mid(21,.6),T[22],col=RED,sz=40)
    if t>T[22]-.2:
        for i in range(5): put(cv,c,'nguoi_om',1000+i*130,880+(i%2)*14,ay=1,s=.55,o=inn(t,T[22]+i*.3,.6))
        lb(cv,c,'nhiều người ốm',1250,330,t,T[22]+.3,b+.3,col=RED,sz=38)
def S_23(cv,t):
    a,b=T[23],E[23]
    c=cam(960,560,1.0)
    left=PAP.copy();cL=cam(900,560,1.15)
    put(left,cL,'citadel',900,720,ay=1,s=.8);ground(left,cL,720,.25)
    put(left,cL,'trai',1300,860,ay=1,s=.55)
    right=PAP.copy();cR=cam(960,600,1.0)
    riv(right,cR,t,640,.4);put(right,cR,'lau_thuyen',960,720,ay=.86,s=.6,r=boatbob(t))
    m=np.zeros((H,W,1),np.float32);m[:,W//2:]=1
    cv[:]=left*(1-m)+right*m
    stroke(cv,c,[(960,80),(970,1000)],1,wid=7,head=False,o=.85)
    lb(cv,c,'kẻ chiếm thành bị kẹt',480,250,t,a+.3,b+.3,col=RED,sz=36)
    lb(cv,c,'triều đình chờ lúc ra tay',1440,250,t,mid(23,.5),b+.3,sz=36)
# ---------------- chương 5
def S_24(cv,t):
    a,b=T[24],E[25]
    c=cam(*cpath(t,[(a-.4,(960,600,1.05)),(b+.4,(1100,600,1.1))]))
    riv(cv,c,t,640,.4)
    x=lerp(600,1300,cl((t-a)/(b-a+1)))
    for i in range(10): put(cv,c,'smallboat2',x-700+i*120,700+(i%3)*40,s=.5,ax=.5,ay=.86,scale_px=1.5)
    put(cv,c,'lau_thuyen',x,720,ay=.86,s=.6,r=boatbob(t))
    big(cv,'MƯỜI HAI NGÀY SAU',t,a+.2,E[24]+.2,RED,190,84,seed=24)
    if t>T[25]-.2:
        tagfall(cv,c,x-260,430,'Trần Thái Tông',t,T[25]+.2,sz=36,col=INK)
        tagfall(cv,c,x+300,430,'thái tử Trần Hoảng · mười bảy tuổi',t,mid(25,.3),sz=32,col=INK)
        lb(cv,c,'ngược sông lên kinh thành',x,300,t,mid(25,.6),b+.3,sz=36)
def S_27(cv,t):
    a,b=T[27],E[28]
    c=cam(*cpath(t,[(a-.4,(1000,580,1.1)),(T[28],(960,560,1.0)),(b+.4,(900,560,1.05))]),
          sx=5*math.sin(t*23)*fio(t,a,E[27]),sy=4*math.sin(t*19)*fio(t,a,E[27]))
    wl=700
    put(cv,c,'far',960,640,ay=1,k=.35,o=.45)
    put(cv,c,'citadel',1450,560,ay=1,s=.45,o=.8)
    Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=PAP[Ys:]
    put(cv,c,'water',960,wl-24,ay=0)
    put(cv,c,'trai',1400,wl-20,ay=1,s=.45)
    for i in range(6):
        xx=1150+i*110
        if t>T[28]: xx-=lerp(0,900,inn(t,T[28]+i*.1,3))
        if i in (0,2,4) and t>mid(27,.4)+i*.2: fall(cv,c,'ky_mong',xx,wl-20,t,mid(27,.4)+i*.2,s=.45,dirn=1);continue
        put(cv,c,Af('ky_mong') if t>T[28] else 'ky_mong',xx,wl-20,ay=1,s=.45,o=1-.5*inn(t,T[28]+1.5,2))
    xb=lerp(200,700,inn(t,a,2.0))
    put(cv,c,'lau_thuyen',xb,wl+80,ay=.86,s=.55,r=boatbob(t))
    for i in range(5): put(cv,c,'smallboat2',xb+250+i*90,wl+60+(i%2)*30,s=.45,ax=.5,ay=.86,scale_px=1.5)
    if t<E[27]:
        for k in range(14):
            ph=((t*.9+k*.29)%1);x0,y0=xb+200+(k%5)*60,wl-20;x1,y1=1150+(k%6)*110,wl-60
            def P_(u): return lerp(x0,x1,u),lerp(y0,y1,u)-70*4*u*(1-u)
            xa,ya=P_(ph);xb2,yb2=P_(max(0,ph-.06))
            stroke(cv,c,[(xb2,yb2),(xa,ya)],1,wid=4,head=True,o=.9*fio(t,a+.3,E[27])*cl((ph-.12)*8)*cl((1-ph)*10))
        for k in range(3): put(cv,c,'redblot',1200+k*160,wl-60,s=.6,o=.55*inn(t,mid(27,.5)+k*.25,.6))
        arrows(cv,c,t,a+.8,mid(27,.6),[(1200+k*110,wl-90) for k in range(5)],[(xb+k*80,wl+10) for k in range(5)],n=6,h=60,per=1.0,seed=27)
        for i in range(6):
            st=a+1.2+i*.25;u=inn(t,st,1.6);x=lerp(xb+300+i*40,1050+i*70,u)
            put(cv,c,'fig_giap_giao',x,wl-5+(i%2)*12,ay=1,s=.36,o=inn(t,st,.3))
        sparks(cv,c,t,[(1120+k*130,wl-50) for k in range(4)],mid(27,.35),E[27],seed=27)
    lb(cv,c,'bến Đông Bộ Đầu',1300,300,t,a+.2,mid(27,.6),sz=40,col=RED)
    lb(cv,c,'kinh thành được lấy lại',1000,300,t,T[28]+.3,b+.3,sz=40)
# ---------------- chương 6
def S_29(cv,t):
    a,b=T[29],E[30]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(960,540,1.06))]),sx=4*math.sin(t*23)*fio(t,mid(29,.5),E[29]))
    put(cv,c,'far',960,700,ay=1,k=.35,o=.55);put(cv,c,'mist',700,560,s=2.4,o=.7,k=.45)
    put(cv,c,'mid',960,820,ay=1,k=.6,o=.8);put(cv,c,'duong_nui',960,1000,ay=1,s=1.0)
    amb=inn(t,mid(29,.45),.6)
    for i in range(7):
        x=[160,260,360,1520,1640,1760,1860][i];y=[480,440,500,470,430,490,450][i]
        put(cv,c,'fig_giap_giao',x,y+lerp(0,120,inn(t,mid(29,.55),1.2)),ay=1,s=.38,o=.08+.92*amb)
    put(cv,c,'cliffL',-160,1200,ax=0,ay=1,k=1.15);put(cv,c,'cliffR',2080,1150,ax=1,ay=1,k=1.15)
    rid=[]
    for i in range(8):
        u=cl((t-a-i*.12)/(b-a));x=lerp(1800,200,u)+i*70;y=830+(i%2)*20;rid.append((x,y))
        dust(cv,c,x+140,y-10,o=.25)
        tf=mid(29,.62)+i*.3
        if i in (2,5,7) and t>tf: fall(cv,c,Af('ky_mong'),x,y,t,tf,s=.55,dirn=1)
        else: put(cv,c,Af('ky_mong'),x,y,ay=1,s=.55)
    src=[(x,y+lerp(0,120,inn(t,mid(29,.55),1.2))-60) for x,y in zip([160,260,360,1520,1640,1760,1860],[480,440,500,470,430,490,450])]
    arrows(cv,c,t,mid(29,.5),E[29]+.3,src,[(x,y-60) for x,y in rid],n=14,h=40,per=.9,seed=29)
    sparks(cv,c,t,[(700,780),(1100,790)],mid(29,.7),E[29],seed=29)
    tagfall(cv,c,1640,330,'Hà Bổng',t,mid(29,.5),sz=40,col=INK,b=T[30])
    lb(cv,c,'trại Quy Hóa',960,230,t,a+.3,T[30],sz=44)
    if t>T[30]-.2: big(cv,'GIẶC PHẬT',t,mid(30,.6),b+.3,RED,200,96,seed=30)
def S_31(cv,t):
    a,b=T[31],E[31]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'mist',960,640,s=3.5,o=.8)
    put(cv,c,'fig_quan_dung',760,820,ay=1,s=1.4,o=.85)
    tagfall(cv,c,760,330,'Trần Nhật Hiệu',t,a+.3,sz=44,col=INK)
    put_screen(cv,band(640,240,PAPER,.8,30),1380,500,inn(t,mid(31,.45),.5))
    put_screen(cv,text('Ngô Sĩ Liên chê:',36,INK,700,glow=3),1380,440,inn(t,mid(31,.5),.4))
    put_screen(cv,text('nhút nhát, không đáng dùng',40,RED,700,glow=3),1380,520,inn(t,mid(31,.6),.4))
def S_32(cv,t):
    a,b=T[32],E[32]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(940,560,1.08))]))
    put(cv,c,'far',960,720,ay=1,k=.4,o=.45)
    put(cv,c,'citadel',900,720,ay=1,s=.8);ground(cv,c,720,.25)
    for i in range(10): put(cv,c,'fig_giap_giao',400+i*120,820+(i%2)*20,ay=1,s=.5,o=inn(t,a+.2+i*.06,.3))
    big(cv,'LỜI HỨA ĐÃ THÀNH SỰ THẬT',t,a+.3,b+.3,RED,190,70,seed=32)
def S_end(cv,t):
    a=T[34]
    c=cam(960,560,1.0+.015*(t-a))
    riv(cv,c,t,640,.9)
    put(cv,c,'lau_thuyen',1300,720,ay=.86,s=.45,r=boatbob(t),o=.85)
    put(cv,c,'sun',1700,560,o=.45,k=.2);flock(cv,c,t,.7)
    tx=text('Thua một trận, chưa thua cuộc chiến',62,INK,700);put_screen(cv,wipe(tx,inn(t,a+.3,1.2),0,.3,seed=13),W/2,250)
    seal(cv,'stitle4',W/2,470,mid(34,.5),t,s=.62,r=3)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,H-80,inn(t,E[34]+.5,1))
S=lambda n:T[n]-.3
SH=[(0,S(2),S_h1),(S(2),S(3),S_h2),(S(3),S(4),S_h3),(S(4),S(6),S_h4),(S(6),S(7),S_map),(S(7),S(9),S_7),(S(9),S(10),S_9),(S(10),S(12),S_map),
 (S(12),S(14),S_12),(S(14),S(15),S_map),(S(15),S(16),S_15),(S(16),S(19),S_16),(S(19),S(20),S_19),
 (S(20),S(21),S_20),(S(21),S(23),S_21),(S(23),S(24),S_23),(S(24),S(26),S_24),(S(26),S(27),S_map),(S(27),S(29),S_27),
 (S(29),S(31),S_29),(S(31),S(32),S_31),(S(32),S(33),S_32),(S(33),S(34),S_map),(S(34),TOTAL+1,S_end)]
LOGO=None
def frame(t):
    global LOGO
    act=[s for s in SH if s[0]-.35<=t<s[1]+.35]
    def one(fn):
        cv=PAP.copy();fn(cv,t);return cv
    if len(act)==1: cv=one(act[0][2])
    else:
        a,b=act[0],act[1];u=cl((t-(b[0]-.35))/.7)
        m=np.clip((u*1.7-.35-XM*.35-NM*.35)/.3,0,1)[...,None];cv=one(a[2])*(1-m)+one(b[2])*m
    if T[6]-4.2<t<T[6]+.2: S_title(cv,t)
    for n,s in CARDS.items(): card(cv,t,T[n]-2.2,s,PAP)
    for n in TX:
        if T[n]-.25<t<E[n]+.35: caption(cv,TX[n],inn(t,T[n]-.25,.25)*(1-inn(t,E[n]+.1,.25)),False)
    if LOGO is None:
        lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4];LOGO=lg
    blend(cv,LOGO,W-44-130,34,.8)
    return cv
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='soi':
        out=[]
        for x in sys.argv[2:]:
            if x[0]=='t': tt=float(x[1:])
            elif '+' in x: tt=T[int(x.split('+')[0])]+float(x.split('+')[1])
            elif '@' in x: tt=mid(int(x.split('@')[0]),float(x.split('@')[1]))
            else: tt=mid(int(x),.6)
            out.append((x,to8(frame(tt))))
        cols=3;h,w=H//3,W//3;rows=(len(out)+cols-1)//cols
        sh=Image.new('RGB',(w*cols,(h+30)*rows),(255,255,255));dr=ImageDraw.Draw(sh)
        for i,(x,im) in enumerate(out):
            sh.paste(Image.fromarray(im).resize((w,h)),((i%cols)*w,(i//cols)*(h+30)+30));dr.text(((i%cols)*w+8,(i//cols)*(h+30)+6),x,fill=(0,0,0))
        sh.save(os.environ.get('SOI','/tmp/gen/tm2v/soi.jpg'),quality=82);print('TOTAL',round(TOTAL,1))
    else:
        out,i0,i1,fps=sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
        ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        for i in range(i0,i1): ff.stdin.write(to8(frame(i/fps)).tobytes())
        ff.stdin.close();ff.wait()
