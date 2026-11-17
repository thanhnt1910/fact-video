# Bản dài tm2: Lê Hoàn phá Tống 981 (giọng Charon gốc, không cân giọng)
import sys,os,subprocess,json,math
import dai
from dai import cam,cpath,to8,stage,PAP,W,H,XM,NM
from canh import *
GD=os.environ.get('GIONG','/tmp/pc/assets/thu_giong_hai/charon')
J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm2_full.json'))
TX={i+1:d['text'] for i,d in enumerate(J)};NN={i+1:d['n'] for i,d in enumerate(J)}
def dur(i):
    f=f'{GD}/{NN[i]}.mp3'
    if os.path.exists(f):
        return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    return len(TX[i].split())/3.1+.2
GAP={5:4.0,16:2.6,25:2.6,33:2.6,44:2.6}
T={};E={};t=0.5
for n in TX:
    t+=GAP.get(n,0);T[n]=t;d=dur(n);E[n]=t+d;t+=d+.45
TOTAL=t+4.5
def mid(n,f): return T[n]+(E[n]-T[n])*f
CARDS={16:'Lần thứ nhất · Một ông vua cầm quân',25:'Lần thứ hai · Cọc trên sông Bạch Đằng',33:'Lần thứ ba · Hàng giả ở Chi Lăng',44:'Sau trận đánh'}
P=PTS
# ---------------- tiện ích
def big(cv,s,t,a,b,col=INK,y=200,sz=80,seed=1):
    if a-.1<t<b+.6:
        hd=text(s,sz,col,700,glow=6);put_screen(cv,wipe(hd,inn(t,a,.7),0,.3,seed=seed),W/2,y,1-inn(t,b,.45))
def tagfall(cv,c,x,y,s,t,a,fall=None,col=RED,sz=40,b=None):
    """nhãn tên hiện ở a; nếu có fall thì rơi xuống và mờ dần"""
    if t<a: return
    o=inn(t,a,.4);dy=0;r=0
    if fall is not None and t>fall:
        v=t-fall;dy=160*v*v;o*=cl(1-v/1.1)
    if b is not None: o*=1-inn(t,b,.4)
    if o<=.01: return
    X,Y=c.p(x,y);put_screen(cv,text(s,sz,col,700,glow=3),X,Y+dy,o,r=r)
def strike(cv,c,x,y,w,t,a,o=1):
    stroke(cv,c,[(x-w/2,y+4),(x+w/2,y-6)],inn(t,a,.4),wid=6,col=RED,head=False,o=o)
def lb(cv,c,s,x,y,t,a,b,col=INK,sz=38):
    tag(cv,c,x,y,s,o=fio(t,a,b),dy=0,sz=sz,col=col)
BR=A('canh_kho');_hw=BR.shape[1]//2
BRL=np.ascontiguousarray(BR[:,:_hw]);BRR=np.ascontiguousarray(BR[:,_hw:])
def branch(cv,x,y,s,ang,o=1.0,hands=0.0,shake=0.0,t=0):
    """cành khô trên màn hình, cong ở giữa một góc ang (độ); hands: độ đậm hai bàn tay"""
    if o<=.01: return
    j=math.sin(t*41)*shake;a=ang+j
    put_screen(cv,BRL,x,y,o,ax=1,ay=.5,s=s/1.5,r=a)
    put_screen(cv,BRR,x,y,o,ax=0,ay=.5,s=s/1.5,r=-a)
    if hands>.01:
        L=BR.shape[1]/1.5*s*.47;rr=math.radians(a)
        lx,ly=x-L*math.cos(rr),y-L*math.sin(rr);rx,ry=x+L*math.cos(rr),y-L*math.sin(rr)
        put_screen(cv,A('tay'),lx,ly,o*hands,ax=290/420,ay=.5,s=s*.9/1.5,r=a)
        put_screen(cv,Af('tay'),rx,ry,o*hands,ax=1-290/420,ay=.5,s=s*.9/1.5,r=-a)
        return (lx,ly),(rx,ry)
def lan(cv,t,t0,k,t1=None):
    """biểu tượng góc: cành khô + vạch đếm, lần thứ k"""
    t1=t1 or t0+5.5
    if not (t0-.1<t<t1+.6): return
    o=fio(t,t0,t1,.5);x,y=W-330,250
    put_screen(cv,band(420,190,PAPER,.75,24),x,y+10,o)
    branch(cv,x,y-20,.3,0,o)
    for i in range(3):
        X=x-80+i*80;on=i<k-1 or (i==k-1 and t>t0+.6)
        m=np.zeros((1,1))
        stroke(cv,cam(960,540,1),[(X-8,y+30),(X+8,y+80)],1 if on else 1,wid=7,col=RED if on else INK,head=False,o=o*(1 if on else .25))
    put_screen(cv,text(f'LẦN {k}',40,RED,700,glow=3),x,y+125,o*inn(t,t0+.6,.4))
def ground(cv,c,y=900,o=.3): put(cv,c,'water',960,y,ay=0,o=o)
def scene_bg(cv,c,far=.5,mist=.7,gy=900):
    stage(cv,c,0,far=far,mist=mist,ground=gy)
# ---------------- chương 1
def S_hook(cv,t):
    c=cam(960,540,1.0+.03*t)
    put(cv,c,'far',960,880,ay=1,k=.3,o=.35);put(cv,c,'mist',960,700,s=3.0,o=.8)
    if t<1.4:
        u=eo(t/1.3);put_screen(cv,A('blot'),W/2,H/2,(1-u)*.85,s=1.9*(1+u*.9))
    big(cv,'DỄ NHƯ BẺ CÀNH KHÔ?',t,.25,E[1]+.3,INK,200,84,seed=3)
    ang=8*inn(t,.8,E[1]-1)+6*inn(t,T[2],mid(2,.5)-T[2])
    gone=mid(2,.72)
    sh=1.2*fio(t,T[2],gone+.5)
    zx=1+.25*inn(t,T[2],E[2]-T[2])
    hs=1-inn(t,gone+.2,1.2)
    r=branch(cv,W/2,H/2+40,1.05*zx,ang,1,hands=hs,shake=sh,t=t)
    if t>gone and r:
        u=inn(t,gone,.6);put_screen(cv,A('redblot'),r[1][0]+40,r[1][1],.85*u,s=.9*(.4+.6*u))
        put_screen(cv,A('redblot'),r[0][0]-40,r[0][1],.55*u,s=.6*(.4+.6*u))
def S_hai(cv,t):
    a,b=T[3]-.3,E[3]+.3
    c=cam(*cpath(t,[(a,(960,560,1.0)),(b,(990,560,1.08))]))
    scene_bg(cv,c,.45,.6,820);ground(cv,c,830,.25)
    put(cv,c,'fig_quan_dung',620,840,ay=1,s=2.0)
    fo=1-inn(t,mid(3,.78),.9)
    put(cv,c,'fig_giap',1300,840,ay=1,s=1.9,o=fo)
    tagfall(cv,c,620,230,'Lư Đa Tốn',t,T[3]+.3,sz=50)
    lb(cv,c,'quan lớn nhà Tống',620,330,t,T[3]+.6,b,sz=32)
    tagfall(cv,c,1300,230,'Hầu Nhân Bảo',t,mid(3,.45),fall=mid(3,.8),sz=50)
    lb(cv,c,'người dẫn quân sang',1300,330,t,mid(3,.5),mid(3,.8),sz=32)
    if t>mid(3,.78):
        u=inn(t,mid(3,.78),.8);put(cv,c,'redblot',1300,760,s=1.1*(.3+.7*u),o=.8*u)
def S_bavach(cv,t):
    a=T[4]-.3
    c=cam(960,540,1.0)
    put(cv,c,'mist',960,640,s=3.0,o=.8)
    branch(cv,W/2,H/2-10,1.0,0,1,t=t)
    for i in range(3):
        X=W/2-160+i*160;stroke(cv,c,[(X-10,700),(X+10,790)],inn(t,mid(4,.62)+i*.35,.3),wid=9,col=INK,head=False,o=.3)
    big(cv,'Vì sao nhà Tống trả giá đắt?',t,T[4]+.2,mid(4,.55),INK,210,64,seed=9)
def S_title(cv,t):
    t0=T[5]-3.6
    u=inn(t,t0-.3,.8);put_screen(cv,A('blot'),W/2,H/2,u*.97*(1-inn(t,t0+3.2,.6)),s=1.5+.1*(t-t0),r=4*(t-t0))
    tt=text('LÊ HOÀN PHÁ TỐNG',96,PAPER,700);put_screen(cv,wipe(tt,inn(t,t0+.2,.8),0,.3,seed=3),W/2,H/2-30,1-inn(t,t0+3.2,.5))
    seal(cv,'s981',W/2+470,H/2+110,t0+1.1,t,s=.75,o=1-inn(t,t0+3.2,.5),r=4)
# ---------------- chương 2
def S_979(cv,t):
    a,b=T[5],E[5]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(900,580,1.15))]))
    put(cv,c,'hall',960,860,ay=1,s=1.0)
    x=lerp(1240,1040,inn(t,mid(5,.45),1.4))
    put(cv,c,'fig_satthu',x,865,ay=1,s=1.15,o=inn(t,mid(5,.4),.6))
    seal(cv,'s979',300,260,a+.2,t,s=1.0,r=-4)
    tagfall(cv,c,1560,330,'Đinh Tiên Hoàng',t,mid(5,.5),fall=mid(5,.85),sz=44,col=INK)
    tagfall(cv,c,1560,400,'Đinh Liễn',t,mid(5,.58),fall=mid(5,.9),sz=44,col=INK)
    if t>mid(5,.85):
        u=inn(t,mid(5,.85),.8);put(cv,c,'redblot',820,760,s=.9*u,o=.7*u)
def S_trieu(cv,t,a,b,keys,le=True,army=False,txt=None):
    c=cam(*cpath(t,keys))
    put(cv,c,'trieu_hoalu',960,1000,ay=1,s=1.0)
    if le: put(cv,c,'fig_giap',760,980,ay=1,s=1.0)
    return c
def S_6(cv,t):
    a,b=T[6],E[6]
    c=S_trieu(cv,t,a,b,[(a-.4,(960,560,1.55)),(mid(6,.4),(930,600,1.5)),(mid(6,.6),(800,760,1.3)),(b+.3,(800,760,1.3))])
    lb(cv,c,'Đinh Toàn · sáu tuổi',960,400,t,a+.3,mid(6,.5),sz=34)
    tagfall(cv,c,760,800,'Lê Hoàn',t,mid(6,.5),sz=42,col=INK)
    lb(cv,c,'người cầm mười đạo quân',960,1000,t,mid(6,.75),b+.3,sz=30)
def S_7(cv,t):
    a,b=T[7],E[7]
    c=cam(960+12*(t-a),560,1.0)
    put(cv,c,'far',960,820,ay=1,k=.4,o=.45)
    put(cv,c,'water',1440,560,ay=0,o=.6)
    put(cv,c,'army',480,800,ay=1,s=.6,o=inn(t,mid(7,.3),.6))
    for i in range(3):
        x=lerp(2100+i*160,1300+i*170,eo(cl((t-mid(7,.5))/4)))
        put(cv,c,Af('bigboat'),x,640+i*55,ay=.9,s=.55+i*.07,r=math.sin(t*1.5+i))
    stroke(cv,c,[(960,120),(975,980)],inn(t,a,.6),wid=7,head=False,o=.85)
    lb(cv,c,'nổi lên chống Lê Hoàn',480,520,t,mid(7,.3),b+.3,sz=34)
    lb(cv,c,'Chiêm Thành',1450,520,t,mid(7,.55),b+.3,sz=40,col=RED)
def S_map(cv,t):
    keys=[(T[8]-.5,(560,560,1.35)),(E[8],(700,440,1.2)),(T[13]-.5,(720,520,1.05)),(E[13],(720,540,1.0)),
          (T[25]-.5,(640,540,1.3)),(E[25],(640,540,1.25)),(T[33]-.5,(560,520,1.6)),(E[33],(560,520,1.6)),(T[38]-.5,(520,640,1.5)),(E[38],(520,600,1.45))]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z)
    c=cam(cx,cy,z)
    mapbg(cv,c,u=inn(t,T[8]-1.0,1.4))
    hl,uc,ls,cli,bd,tk,hm=P['hoalu'],P['ungchau'],P['langson'],P['chilang'],P['bachdang'],P['tayket'],P['haimon']
    dot(cv,c,*hl,o=1);tag(cv,c,*hl,'Hoa Lư',dy=-22)
    tag(cv,c,250,860,'ĐẠI CỒ VIỆT',o=.8,sz=44,dy=0,col=np.float32([.25,.22,.18]))
    tag(cv,c,1150,150,'NHÀ TỐNG',o=.8,sz=44,dy=0,col=RED)
    dot(cv,c,*uc,o=inn(t,T[8]+.5,.4),col=RED);tag(cv,c,*uc,'Ung Châu',o=inn(t,T[8]+.6,.4),dy=-22,col=RED)
    if t<T[13]:
        stroke(cv,c,[hl,(500,620),(620,450),(760,330),uc],inn(t,T[8]+.8,mid(8,.5)-T[8]),wid=5,dash=14,head=True,col=INK,o=.8)
        tag(cv,c,uc[0]+190,uc[1]+40,'Hầu Nhân Bảo',o=inn(t,mid(8,.55),.5),dy=0,col=RED,sz=36)
    elif t<T[25]:
        for k,pts in enumerate([[(880,150),(760,330),(640,420)],[(700,120),(620,300),(560,400)],[(1250,330),(1100,460),(860,560),(720,600)],[(1500,500),(1200,640),(900,680)]]):
            stroke(cv,c,pts,inn(t,T[13]+.3+k*.6,2.2),wid=7,col=RED,o=.9)
        lb(cv,c,'đường bộ',600,330,t,T[13]+1.5,E[13]+.5,col=RED,sz=32);lb(cv,c,'đường thủy',1150,720,t,T[13]+2.5,E[13]+.5,col=RED,sz=32)
    elif t<T[33]:
        seal(cv,'s981',W-280,300,T[25]+.2,t,s=.8,o=1-inn(t,E[25],.4))
        dot(cv,c,*ls,o=inn(t,T[25]+1,.4));tag(cv,c,*ls,'Lạng Sơn',o=inn(t,T[25]+1,.4),dy=-22)
        dot(cv,c,*bd,o=inn(t,mid(25,.55),.4));tag(cv,c,bd[0]+60,bd[1]+40,'sông Bạch Đằng',o=inn(t,mid(25,.55),.4),dy=0)
        stroke(cv,c,[uc,(760,330),(660,400),ls],inn(t,mid(25,.3),2.4),wid=7,col=RED)
        tag(cv,c,740,300,'Hầu Nhân Bảo',o=inn(t,mid(25,.35),.5),dy=0,col=RED,sz=34)
        stroke(cv,c,[(1300,560),hm,(900,560),(720,620),bd],inn(t,mid(25,.55),2.4),wid=7,col=RED)
        tag(cv,c,950,600,'Lưu Trừng',o=inn(t,mid(25,.65),.5),dy=0,col=RED,sz=34)
    elif t<T[38]:
        dot(cv,c,*ls,o=1);tag(cv,c,*ls,'Lạng Sơn',dy=-22)
        stroke(cv,c,[(700,330),(640,400),ls,cli],inn(t,T[33]+.4,E[33]-T[33]-.8),wid=8,col=RED)
        dot(cv,c,*cli,o=inn(t,mid(33,.6),.4),col=RED);tag(cv,c,cli[0]-40,cli[1]+50,'Chi Lăng',o=inn(t,mid(33,.6),.4),dy=0,col=RED,sz=40)
    else:
        dot(cv,c,*tk,o=.55,col=RED);tag(cv,c,tk[0]+80,tk[1]+10,'Tây Kết',o=inn(t,T[38]+.3,.4),dy=0,col=RED)
        stroke(cv,c,[tk,(500,560),(560,480),(640,380),(720,300)],inn(t,mid(38,.35),2.6),wid=7,col=RED)
        tag(cv,c,700,520,'Trần Khâm Tộ rút về',o=inn(t,mid(38,.4),.5),dy=0,col=RED,sz=34)
def S_9(cv,t):
    a,b=T[9],E[9]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'mist',960,600,s=3,o=.7)
    fly=mid(9,.78)
    if t<fly+.2:
        im=wipe(A('cuon_thu'),inn(t,a+.1,1.2),0,.2,seed=5)
        put(cv,c,im,960,560,s=1.15,o=1-inn(t,fly,.3))
    seal(cv,'s980',300,260,a+.2,t,s=1.0,r=-4)
    seal(cv,'s980',700,720,mid(9,.4),t,s=.55,r=6,o=1-inn(t,fly,.3))
    if t>fly:
        u=eo(cl((t-fly)/1.6));put_screen(cv,A('thu_cuon'),lerp(960,1700,u),lerp(560,120,u),1-inn(t,fly+1.3,.4),s=lerp(1.0,.5,u)/1.5,r=-20*u)
    lb(cv,c,'nước Việt đang loạn, xin đánh ngay',960,880,t,mid(9,.35),fly,sz=36)
def S_tong(cv,t):
    a=T[10]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(mid(10,.4),(780,640,1.3)),(T[11],(780,640,1.3)),(T[12],(960,580,1.0)),(E[12]+.4,(960,560,1.08))]))
    put(cv,c,'court',960,900,ay=1,s=1.0,o=.85)
    x=lerp(620,760,inn(t,a+.3,1.5))
    put(cv,c,'fig_quan_dung',x,900,ay=1,s=1.25)
    tagfall(cv,c,x,590,'Lư Đa Tốn',t,a+.5,sz=40,b=T[12])
    if t>T[12]:
        u=eo(cl((t-mid(12,.3))/1.6));put(cv,c,tint(A('thu_cuon'),RED),lerp(900,960,u),lerp(500,740,u),s=.8,o=inn(t,mid(12,.3),.3))
        lb(cv,c,'lệnh đánh nước Việt',960,330,t,mid(12,.45),E[12]+.4,col=RED,sz=40)
    # đoạn 11: cắt nhanh về cành khô
    f0,f1=T[11]+.2,E[11]-.2
    if f0-.3<t<f1+.3:
        o=fio(t,f0,f1,.3);flash=PAP.copy();put(flash,c,'mist',960,640,s=3,o=.7)
        branch(flash,W/2,H/2+60,1.0,6+4*inn(t,f0,2),1,hands=1,t=t)
        big(flash,'KHÔNG TỐN MỘT MŨI TÊN',t,f0+.3,f1,RED,200,74,seed=11)
        cv*=1-o;cv+=flash*o
def S_14(cv,t):
    a,b=T[14],E[14]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'mist',960,700,s=3,o=.7)
    dongho(cv,c,960,560,1.0,t,lvl=.9,low=.15)
    for k in range(3):
        stroke(cv,c,[(1500,300+k*150),(1260,330+k*130)],inn(t,a+.6+k*.3,.6),wid=6,col=RED,o=.85)
    lb(cv,c,'mọi cánh quân',1560,250,t,mid(14,.3),b+.3,col=RED,sz=34)
    lb(cv,c,'cùng một lúc',600,300,t,mid(14,.6),b+.3,col=INK,sz=46)
def dongho(cv,c,x,y,s,t,lvl=.9,low=.1,drip=True):
    """đồng hồ nước: lvl mức bình trên, low mức bình dưới (0..1)"""
    put(cv,c,'dong_ho',x,y,s=s)
    X0,Y0=c.p(x-260*s,y-390*s);z=c.z*s
    def fill(x0,x1,ytop,ybot,u):
        if u<=0: return
        yy=ybot-(ybot-ytop)*u
        a0,b0=int(X0+x0*z),int(X0+x1*z);c0,d0=int(Y0+yy*z),int(Y0+ybot*z)
        a0,b0=max(0,a0),min(W,b0);c0,d0=max(0,c0),min(H,d0)
        if b0>a0 and d0>c0: cv[c0:d0,a0:b0]=cv[c0:d0,a0:b0]*.62+INK*.38
    fill(156,364,80,306,lvl);fill(156,364,424,726,low)
    if drip and lvl>0:
        ph=(t*1.6)%1;yy=Y0+(350+ph*(726-(726-424)*low-350))*z
        Xd=X0+300*z;m=np.zeros((1,1))
        stroke(cv,cam(960,540,1),[(Xd,yy),(Xd,yy+10*z)],1,wid=6,head=False,o=.8)
def S_15(cv,t):
    a,b=T[15],E[15]
    c=S_trieu(cv,t,a,b,[(a-.4,(960,620,1.1)),(b+.4,(960,560,1.75))],le=False)
    big(cv,'AI SẼ CẦM QUÂN?',t,mid(15,.55),b+.5,RED,150,84,seed=15)
# ---------------- chương 3
def S_16(cv,t):
    a,b=T[16],E[16]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(1120,600,1.18))]))
    put(cv,c,'council',960,960,ay=1,s=1.0)
    lb(cv,c,'Thái hậu giao cho Lê Hoàn chọn người',760,300,t,a+.3,mid(16,.5),sz=34)
    put(cv,c,'fig_giap',1290,975,ay=1,s=.85,o=inn(t,mid(16,.45),.5))
    tagfall(cv,c,1290,560,'Phạm Cự Lạng',t,mid(16,.5),sz=40,col=INK)
    lb(cv,c,'Đại tướng quân',1290,620,t,mid(16,.62),b+.3,sz=32,col=RED)
GEN=[(0,1),(1,0),(2,1),(3,0),(4,1),(5,0)]
def S_vao(cv,t):
    a,b=T[17],E[18]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(mid(17,.3),(960,560,1.0)),(T[18],(1050,600,1.1)),(b+.4,(1100,620,1.15))]))
    put(cv,c,'cong_cung',960,880,ay=1,s=1.0)
    go=mid(17,.28)
    for i,(k,sp) in enumerate(GEN):
        st=go+i*.35;u=eo(cl((t-st)/3.2))
        x=lerp(690,1050+i*120-(0 if i<3 else 240),u);y=lerp(680,800+(i%2)*30,u);s=lerp(.45,1.0,u)
        if t>st: put(cv,c,'fig_giap_giao' if sp else 'fig_giap',x,y,ay=1,s=s,o=inn(t,st,.4),r=math.sin(t*9+i)*1.5*(1-u))
    if t>T[18]-.5:
        put(cv,c,'fig_giap',1250,840,ay=1,s=1.05,o=inn(t,T[18]-.5,.6))
        tagfall(cv,c,1250,520,'Lê Hoàn',t,T[18],sz=40,col=INK)
    lb(cv,c,'mặc nguyên áo trận',1100,300,t,mid(17,.5),T[18],sz=36)
def S_19(cv,t):
    a,b=T[19],E[19]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(960,520,1.08))]))
    put(cv,c,'trieu_hoalu',960,900,ay=1,s=1.0,o=.35)
    put(cv,c,'fig_giap',960,880,ay=1,s=1.55)
    dy=lerp(-520,0,eo(cl((t-mid(19,.32))/1.6)))
    if t>mid(19,.3): put(cv,c,'ao_vua',960+2,650+dy,s=.95,o=inn(t,mid(19,.3),.3))
    for i in range(2):
        put(cv,c,'dam_dong',960+(i*60),1080+i*20-abs(math.sin(t*5+i))*14*inn(t,a,.5),ay=1,s=.8-i*.05,o=.85-i*.25,k=1.15)
    lan(cv,t,mid(19,.62),1,E[19]+1.0)
def S_20(cv,t):
    a,b=T[20],E[20]
    c=cam(960,560,1.0+.01*(t-a))
    put(cv,c,'mist',960,700,s=3,o=.6)
    stroke(cv,c,[(960,140),(970,940)],inn(t,a,.5),wid=6,head=False,o=.7)
    put(cv,c,'fig_be',480,720,ay=1,s=1.9,o=1-.5*inn(t,mid(20,.55),.6))
    strike(cv,c,480,560,300,t,mid(20,.55))
    lb(cv,c,'ông vua sáu tuổi',480,280,t,mid(20,.4),b+.3,sz=34)
    put(cv,c,'fig_giap',1440,760,ay=1,s=1.2,o=inn(t,mid(20,.55),.5))
    for r in range(2):
        for i in range(5): put(cv,c,'fig_giap_giao',1200+i*110+r*50,880+r*20,ay=1,s=.42,o=inn(t,mid(20,.7)+i*.06,.3)*.85)
    lb(cv,c,'người từng cầm mười đạo quân',1440,280,t,mid(20,.6),b+.3,sz=34)
    big(cv,'Chỉ trong một buổi',t,a+.2,mid(20,.4),INK,160,56,seed=20)
def S_21(cv,t):
    a,b=T[21],E[21]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'trieu_hoalu',960,1000,ay=1,s=1.0,o=.4)
    u=eo(cl((t-a)/1.4));put_screen(cv,tint(A('thu_cuon'),RED),lerp(1900,960,u),lerp(80,420,u),inn(t,a,.3)*(1-inn(t,mid(21,.3),.3)),s=.6)
    if t>mid(21,.28):
        put(cv,c,wipe(A('cuon_thu'),inn(t,mid(21,.28),1.0),0,.2,seed=8),960,520,s=.95)
        put(cv,c,'tay',1200,320,s=2.2,r=90,o=.25*inn(t,mid(21,.5),1.0)*(1+.1*math.sin(t*3)))
    lb(cv,c,'nước Việt chỉ như ngón tay của nhà Tống',960,900,t,mid(21,.5),b+.3,col=RED,sz=38)
def S_22(cv,t):
    a,b=T[22],E[22]
    c=cam(960+15*(t-a),560,1.0)
    scene_bg(cv,c,.45,.6,900);ground(cv,c,900,.25)
    x=lerp(300,900,cl((t-a)/(b-a+.5)))
    put(cv,c,'porters',x,905,ay=1,s=1.0)
    put(cv,c,'thu_cuon',x+380,520,s=.55,o=inn(t,mid(22,.4),.4))
    lb(cv,c,'thư ký tên Đinh Toàn',x+380,450,t,mid(22,.45),b+.3,sz=32)
    lb(cv,c,'xin phong chức như cha',1300,300,t,mid(22,.65),b+.3,sz=36)
def S_23(cv,t):
    a,b=T[23],E[23]
    c=cam(960,560,1.0)
    put(cv,c,'court',960,1010,ay=1,s=1.05,o=.35)
    for i,(x,t0) in enumerate([(560,mid(23,.3)),(1360,mid(23,.62))]):
        put(cv,c,wipe(tint(A('cuon_thu'),INK*.0+np.float32([.30,.10,.07])) if False else A('cuon_thu'),inn(t,t0,.8),0,.2,seed=i+2),x,540,s=.75)
        if i==0:
            put(cv,c,'fig_be',x-40,610,ay=1,s=.8,o=inn(t,t0+.6,.4));put(cv,c,'fig_giap',x+90,640,ay=1,s=.45,o=inn(t,t0+.8,.4))
            lb(cv,c,'Đinh Toàn làm vua, Lê Hoàn làm phó',x,800,t,t0+.5,b+.3,sz=30,col=RED)
        else:
            k=cl((t-t0-.6)/3)
            put(cv,c,'fig_quan_dung',x-60+60*k,640,ay=1,s=.45,o=inn(t,t0+.6,.4));put(cv,c,'fig_be',x+20+60*k,640,ay=1,s=.45,o=inn(t,t0+.6,.4))
            lb(cv,c,'hoặc mẹ con sang nhà Tống',x,800,t,t0+.5,b+.3,sz=30,col=RED)
        seal(cv,'s980',int(x+150),700,t0+.9,t,s=.4,r=8)
def S_24(cv,t):
    a,b=T[24],E[24]
    c=cam(960,560,1.0)
    put(cv,c,'court',960,1010,ay=1,s=1.05,o=.35*(1-inn(t,mid(24,.4),.8)))
    burn=inn(t,a+.4,2.0)
    for i,x in enumerate([560,1360]):
        im=wipe(A('cuon_thu'),1-burn,1,.25,seed=i+30)
        put(cv,c,im,x,540,s=.75)
        if 0<burn<1:
            yb=540-195+390*(1-burn)
            stroke(cv,c,[(x-330,yb),(x+330,yb+8)],1,wid=10,col=RED,head=False,o=.5)
    if t>mid(24,.5):
        u=eo(cl((t-mid(24,.5))/.5));put(cv,c,'fig_giap_giao',960,lerp(-200,900,u),ay=1,s=1.4)
        if u>=1: put(cv,c,'splash',960,920,s=.6,o=.6*(1-inn(t,mid(24,.5)+.6,1.2)))
# ---------------- chương 4: trận trên sông
def S_26(cv,t):
    a,b=T[26],E[26];sw=mid(26,.42)
    if t<sw+.3:
        c=cam(*cpath(t,[(a-.4,(1000,640,1.15)),(sw+.3,(900,660,1.25))]))
        viet=[dict(x=lerp(500,800,cl((t-a)/5))+i*190,y=690+i*30,s=1.0,o=1) for i in range(3)]
        river(cv,c,t,PAP,wl=640,viet=viet,under=.04,mist=.5)
        tag(cv,c,lerp(500,800,cl((t-a)/5)),570,'Lê Hoàn',o=fio(t,a+.3,sw),dy=0,sz=38)
    else:
        c=cam(960,560,1.02)
        wl=470
        y0=int(c.p(0,wl)[1]);cv[y0:]=cv[y0:]*(1-.18)+INK*.18
        for i in range(2): put(cv,c,'wave',960-((t*20+i*70)%200),wl+i*16,o=.7-.3*i)
        put(cv,c,'riverbed',960,980,ay=1,s=1)
        for i,xx in enumerate(range(520,1420,52)):
            by=dai.bedy(xx)+30;td=sw+.6+i*.12
            if t<td-.5: continue
            u=eo((t-td+.5)/.5);top=by-272;y=lerp(top-300,top,u)
            im=rowclip(A('stake'),(wl-y)*1.5/.85,below=.22,soft=4) if wl>y else A('stake')
            put(cv,c,im,xx+(i%2)*6,y,s=.85,ax=.5,ay=0,scale_px=1.5)
        tag(cv,c,960,260,'đóng cọc xuống lòng sông',o=inn(t,sw+.8,.5),dy=0,sz=42)
def S_27(cv,t):
    a,b=T[27],E[27]
    c=cam(*cpath(t,[(a-.4,(1000,660,1.2)),(b+.4,(1000,640,1.1))]))
    old=fio(t,a+.2,mid(27,.92),.6)
    boats=[dict(x=900+i*170,y=840+(i%2)*30,s=.62,r=(25 if i%2 else -30)*old,o=1,flip=True) for i in range(4)]
    river(cv,c,t,PAP,wl=880 if old>.5 else 700,boats=boats if old>.3 else [],under=1,mist=1.1)
    if old>0:
        cv*=1-.35*old;cv+=PAPER*.35*old
    seal(cv,'s938',300,260,a+.3,t,s=1.0,r=-4,o=1-inn(t,mid(27,.9),.4))
    tag(cv,c,1000,500,'Ngô Quyền · 43 năm trước',o=fio(t,mid(27,.3),mid(27,.9)),dy=0,sz=40)
def S_tran(cv,t):
    a,b=T[28],E[29]
    c=cam(*cpath(t,[(a-.4,(1050,640,1.2)),(mid(28,.6),(1000,660,1.28)),(T[29],(1050,650,1.15)),(b+.4,(1000,650,1.1))]),sx=4*math.sin(t*23)*fio(t,a,mid(28,.8)),sy=3*math.sin(t*19)*fio(t,a,mid(28,.8)))
    wl=lerp(640,840,inn(t,T[29],2.5))
    boats=[]
    for i in range(5):
        x=lerp(1900+i*150,1050+i*150,eo(cl((t-a+.5)/5)))
        if t>mid(29,.45): x+=lerp(0,700,inn(t,mid(29,.45),2.5))
        boats.append(dict(x=x,y=wl+14+(i%3)*40,s=.55+(i%3)*.1,r=math.sin(t*1.5+i)*1.4,flip=t<mid(29,.4)))
    vx=lambda i:lerp(900,300,inn(t,mid(28,.2),2.5))+i*150
    viet=[]
    for i in range(4):
        cap=i<2 and t>mid(28,.55)
        viet.append(dict(x=vx(i) if not cap else lerp(vx(i),1000+i*120,inn(t,mid(28,.55),1.8)),y=wl+40+i*28,s=.6,flip=cap,o=1))
    river(cv,c,t,PAP,wl=wl,boats=boats,viet=viet,under=.04 if t<T[29] else lerp(.04,1,inn(t,T[29],2)),mist=.9)
    if t<E[28]:
        # tên bắn từ chiến thuyền nhà Tống (phải) sang thuyền Đại Cồ Việt (trái), bay theo đường cong
        for k in range(16):
            ph=((t*.9+k*.29)%1);bo=boats[k%5];vi=viet[(k*3)%4]
            x0,y0=bo['x']-60*bo['s'],bo['y']-170*bo['s'];x1,y1=vi['x']+(k%3-1)*30,vi['y']-40
            hgt=60+(k%3)*20
            def P_(u): return lerp(x0,x1,u),lerp(y0,y1,u)-hgt*4*u*(1-u)
            xa,ya=P_(ph);xb,yb=P_(max(0,ph-.06))
            stroke(cv,c,[(xb,yb),(xa,ya)],1,wid=3,head=True,o=.8*fio(t,a+.4,E[28])*cl((ph-.12)*8)*cl((1-ph)*10))
    lb(cv,c,'hai trăm chiến thuyền',1000,420,t,mid(28,.5),mid(28,.9),col=RED,sz=40)
    put(cv,c,'gauge',1810,980,ay=1,s=.7,o=inn(t,T[29],.5))
    if t>T[29]: stroke(cv,c,[(1760,wl),(1790,wl)],1,wid=5,col=RED,head=True)
    if T[28]+3<t<E[28]+.5: lan_cong(cv,t,mid(28,.7),E[28]+.3)
    lan(cv,t,mid(29,.6),2,E[29]+1.0)
def lan_cong(cv,t,a,b):
    o=fio(t,a,b,.4);x,y=W-330,250
    if o<=.01: return
    put_screen(cv,band(420,160,PAPER,.7,24),x,y,o);branch(cv,x,y,.3,lerp(0,16,inn(t,a,1.2)),o,shake=1.5,t=t)
def S_trai(cv,t):
    a,b=T[30],E[31]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(T[31],(1000,580,1.08)),(b+.4,(1000,580,1.12))]))
    # mặt trời đi qua trời: gợi chờ lâu
    if t>T[31]:
        u=cl((t-T[31])/(E[31]-T[31]));ang=math.pi*(1-u)
        put(cv,c,'sun',960+700*math.cos(ang),620-380*math.sin(ang),s=.55,o=.7,k=.3)
    put(cv,c,'far',960,760,ay=1,k=.4,o=.4)
    put(cv,c,'trai',960,890,ay=1,s=1.0)
    tag(cv,c,960,190,'Hoa Bộ',o=inn(t,a+.3,.5),dy=0,sz=56,col=RED)
    tagfall(cv,c,700,400,'Tôn Toàn Hưng',t,mid(30,.45),sz=40)
    lb(cv,c,'chờ quân thủy tới rồi mới đi',700,480,t,mid(30,.6),T[31],sz=30)
    if t>T[31]:
        for k in range(3):
            st=T[31]+.2+k*(E[31]-T[31])/3.4;u=cl((t-st)/1.6)
            if 0<u<1: put(cv,c,'ky_si',lerp(-200,700,u),840,ay=1,s=.75)
            if 0<u<1.3: lb(cv,c,'Hầu Nhân Bảo giục',700,560,t,st+.4,st+1.5,col=RED,sz=30)
        dongho(cv,cam(960,540,1),1690,470,.36,t,lvl=lerp(.8,0,inn(t,T[31]+.5,E[31]-T[31]-1)),low=lerp(.2,.9,inn(t,T[31]+.5,E[31]-T[31]-1)),drip=True)
def S_32(cv,t):
    a,b=T[32],E[32]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(1250,600,1.55))]))
    put(cv,c,'far',960,820,ay=1,k=.4,o=.5);put(cv,c,'mist',700,700,s=2.6,o=.7)
    put(cv,c,'cliffR',1950,1150,ax=1,ay=1,s=1.0)
    put(cv,c,Af('fig_giap'),1330,520,ay=1,s=.8)
    big(cv,'LIỆU CÓ CHỊU CHỜ?',t,mid(32,.45),b+.4,RED,180,76,seed=32)
# ---------------- chương 5: Chi Lăng
def S_chilang(cv,t):
    a,b=T[34],E[37]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(T[35],(900,600,1.1)),(mid(35,.6),(820,640,1.3)),(T[36],(820,620,1.25)),(mid(36,.4),(960,560,1.0)),(T[37],(960,560,1.0)),(b+.4,(960,540,1.05))]),
          sx=5*math.sin(t*25)*fio(t,mid(36,.05),mid(36,.6)),sy=4*math.sin(t*21)*fio(t,mid(36,.05),mid(36,.6)))
    put(cv,c,'far',960,700,ay=1,k=.35,o=.55)
    put(cv,c,'mist',700,560,s=2.4,o=.7,k=.45)
    put(cv,c,'mid',960,820,ay=1,k=.6,o=.8)
    put(cv,c,'duong_nui',960,1000,ay=1,s=1.0)
    amb=inn(t,mid(36,.05),.5)
    for i in range(7):
        x=[160,260,360,1520,1640,1760,1860][i];y=[480,440,500,470,430,490,450][i]
        dy=lerp(0,120,inn(t,mid(36,.15),1.2))
        put(cv,c,'fig_giap_giao',x,y+dy,ay=1,s=.38,o=.08+.92*amb,k=1.0)
    put(cv,c,'cliffL',-160,1200,ax=0,ay=1,k=1.15)
    put(cv,c,'cliffR',2080,1150,ax=1,ay=1,k=1.15)
    # quân nhà Tống tiến vào
    ax_=lerp(1900,1250,eo(cl((t-a)/5)))
    put(cv,c,'army',ax_+560,820,ay=1,s=.6,o=1-inn(t,mid(36,.5),1))
    hx=lerp(1700,1050,eo(cl((t-a)/5)))
    if t>T[35]: hx=lerp(1050,860,inn(t,mid(35,.4),2))
    put(cv,c,Af('ky_si_quan'),hx,830,ay=1,s=.85,o=1-inn(t,mid(36,.7),.8))
    tagfall(cv,c,hx,560,'Hầu Nhân Bảo',t,a+.6,fall=mid(36,.75),sz=40)
    lb(cv,c,'sông Chi Lăng',960,230,t,a+.3,T[35],sz=46)
    # toán quân xin hàng
    if t>T[35]:
        for i in range(3):
            put(cv,c,'fig_quy',520+i*110,830,ay=1,s=.75,o=inn(t,T[35]+.2+i*.2,.5)*(1-inn(t,mid(36,.6),.6)))
    if T[35]+2<t<E[35]+.4: lan_cong(cv,t,mid(35,.55),E[35]+.2)
    if t>mid(36,.6):
        u=inn(t,mid(36,.6),.7);put(cv,c,'redblot',hx,780,s=1.3*u,o=.85*u)
    if T[36]-.1<t<mid(36,.62): ink_wash(cv,.0)
    if T[37]-.3<t:
        o=inn(t,T[37]-.3,.8);put(cv,c,'mist',960,640,s=4,o=.9*o)
        branch(cv,W/2,H/2-40,.95,0,o,t=t)
        lan(cv,t,mid(37,.5),3,E[37]+1.0)
def S_39(cv,t):
    a,b=T[39],E[39]
    c=cam(960+40*(t-a),560,1.05)
    put(cv,c,'far',960,720,ay=1,k=.35,o=.5);put(cv,c,'mid',960,860,ay=1,k=.6,o=.6)
    put(cv,c,'duong_nui',960,1000,ay=1,s=1.0)
    x=lerp(700,1500,cl((t-a)/(b-a)))
    put(cv,c,'army',x+300,830,ay=1,s=.55)
    lb(cv,c,'quân nhà Tống',x+300,640,t,a+.2,mid(39,.5),col=RED,sz=34)
    if t>mid(39,.2):
        x2=lerp(-200,1100,cl((t-mid(39,.2))/(b-mid(39,.2))))
        put(cv,c,'ky_si',x2,850,ay=1,s=.8);put(cv,c,'army',x2-560,850,ay=1,s=.5)
        lb(cv,c,'Lê Hoàn',x2,580,t,mid(39,.3),b+.3,sz=34)
    if t>mid(39,.6):
        for k in range(3): put(cv,c,'redblot',900+k*260,860,s=.6,o=.55*inn(t,mid(39,.6)+k*.3,.6))
        lb(cv,c,'chết quá nửa',1200,330,t,mid(39,.65),b+.3,col=RED,sz=44)
def S_40(cv,t):
    a,b=T[40],E[40]
    c=cam(960-20*(t-a),560,1.0)
    put(cv,c,'citadel',760,700,ay=1,s=.75,o=.85)
    ground(cv,c,760,.25)
    x=lerp(1700,1150,cl((t-a)/(b-a+.6)))
    put(cv,c,'fig_giap_giao',x-200,860,ay=1,s=.85)
    for i,nm in enumerate(['Quách Quân Biện','Triệu Phụng Huân']):
        xx=x+i*170;put(cv,c,'fig_giap',xx,860,ay=1,s=.85,r=6)
        tagfall(cv,c,xx,520-i*60,nm,t,a+.4+i*.6,sz=34)
    stroke(cv,c,[(x-180,740),(x,745),(x+170,745)],1,wid=3,head=False,o=.8)
    put(cv,c,'fig_giap_giao',x+360,860,ay=1,s=.85)
    lb(cv,c,'Hoa Lư',760,330,t,mid(40,.5),b+.3,sz=44)
def S_tongphat(cv,t):
    a,b=T[41],E[43]
    if t<T[43]-.2:
        c=cam(960,560,1.0+.02*(t-a))
        put(cv,c,'court',960,1010,ay=1,s=1.05,o=.75)
        tx=text('KHÔNG TỐN MỘT MŨI TÊN',72,RED,700,glow=6);put_screen(cv,tx,W/2,190,fio(t,a+.2,T[42]))
        strike(cv,c,960,190,800,t,mid(41,.3),o=1-inn(t,T[42]-.4,.4))
        lb(cv,c,'rút hết quân về',960,340,t,mid(41,.55),T[42],sz=40)
        for i,nm in enumerate(['Lưu Trừng','Vương Soạn']):
            st=T[42]+i*(E[42]-T[42])*.5
            tagfall(cv,c,620+i*680,420,nm,t,st,fall=st+1.4,sz=48)
            strike(cv,c,620+i*680,400,320,t,st+.6,o=1-inn(t,st+1.4,.6))
            seal(cv,'s981',int(620+i*680),560,st+.7,t,s=.5,fall=st+1.4)
    else:
        c=cam(*cpath(t,[(T[43]-.4,(960,560,1.0)),(b+.4,(960,600,1.12))]))
        put(cv,c,'cho',960,1000,ay=1,s=1.0)
        tagfall(cv,c,960,420,'Tôn Toàn Hưng',t,T[43]+.2,fall=mid(43,.8),sz=48)
        strike(cv,c,960,400,380,t,mid(43,.55),o=1-inn(t,mid(43,.8),.6))
# ---------------- chương 6
def S_44(cv,t):
    a,b=T[44],E[44]
    c=cam(960+15*(t-a),560,1.0)
    scene_bg(cv,c,.45,.6,900);ground(cv,c,900,.25)
    x=lerp(300,1000,cl((t-a)/(b-a+.5)))
    put(cv,c,'porters',x,850,ay=1,s=1.0)
    for i in range(2): put(cv,c,'fig_giap',x+560+i*120,850,ay=1,s=.75)
    if t>mid(44,.55):
        u=eo(cl((t-mid(44,.55))/1.5));put(cv,c,tint(A('thu_cuon'),RED),lerp(2000,1450,u),400,s=.6)
        lb(cv,c,'nhà Tống phong chức',1450,330,t,mid(44,.65),b+.3,col=RED,sz=34)
    lb(cv,c,'trả tướng, làm hòa',700,300,t,a+.3,mid(44,.6),sz=38)
def leaves(cv,t,a,o=1):
    c=cam(960,540,1)
    rg_=np.random.default_rng(4)
    for k in range(16):
        x=W/2-380+k*50+rg_.random()*20;y=H/2-30+(rg_.random()-.5)*20;sg=1 if k%2 else -1
        u=inn(t,a+k*.12,.5)
        if u<=0: continue
        L=34*u
        stroke(cv,c,[(x,y),(x+L*.4,y+sg*L*.5),(x+L,y+sg*L*.6)],1,wid=5,head=False,o=o*.85)
def S_45(cv,t):
    a,b=T[45],E[45]
    c=cam(960,540,1.0)
    put(cv,c,'mist',960,640,s=3.5,o=.8)
    branch(cv,W/2,H/2,1.0,0,1,t=t)
    leaves(cv,t,mid(45,.62))
    big(cv,'Vì sao phải trả giá đắt?',t,a+.2,mid(45,.55),INK,200,64,seed=45)
def S_46(cv,t):
    a,b=T[46],E[46]
    c=cam(960,560,1.0)
    put(cv,c,'mist',960,640,s=3.5,o=.8)
    items=[('Một ông vua cầm quân','ao_vua',.42,mid(46,.05)),('Hàng cọc chặn sông','stake',1.0,mid(46,.35)),('Hàng giả ở Chi Lăng','fig_quy',.9,mid(46,.65))]
    for i,(s,im,sc,tt) in enumerate(items):
        x=W/2+(i-1)*560;o=inn(t,tt-.2,.5)
        put_screen(cv,band(480,420,PAPER,.85,30),x,520,o)
        if im=='stake':
            for k in range(5): put_screen(cv,A('stake'),x-120+k*60,560,o,ay=.5,s=.55/1.5,r=(k-2)*3)
        else: put_screen(cv,A(im),x,520,o,s=sc/1.5)
        put_screen(cv,text(s,40,INK,700,glow=3),x,770,o)
        stroke(cv,c,[(x-12,250),(x+12,320)],inn(t,tt,.3),wid=8,col=RED,head=False)
def S_end(cv,t):
    a=T[47]
    c=cam(960,560,1.0+.015*(t-a))
    put(cv,c,'sun',1640,230,o=.6,k=.2);flock(cv,c,t,.7);put(cv,c,'far',960,880,ay=1,k=.4,o=.5);put(cv,c,'mist',960,760,s=3,o=.9)
    branch(cv,W/2,H/2-150,.9,0,1,t=t)
    tx=text('Không phải cành khô nào cũng dễ bẻ',66,INK,700);put_screen(cv,wipe(tx,inn(t,a+.3,1.2),0,.3,seed=13),W/2,H/2+20)
    seal(cv,'stitle2',W/2,H/2+210,mid(47,.5),t,s=.62,r=3)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,H-80,inn(t,E[47]+.5,1))
SH=[(0,T[3]-.3,S_hook),(T[3]-.3,T[4]-.3,S_hai),(T[4]-.3,T[5]-.3,S_bavach),
 (T[5]-.3,T[6]-.3,S_979),(T[6]-.3,T[7]-.3,S_6),(T[7]-.3,T[8]-.3,S_7),(T[8]-.3,T[9]-.3,S_map),(T[9]-.3,T[10]-.3,S_9),(T[10]-.3,T[13]-.3,S_tong),
 (T[13]-.3,T[14]-.3,S_map),(T[14]-.3,T[15]-.3,S_14),(T[15]-.3,T[16]-.3,S_15),
 (T[16]-.3,T[17]-.3,S_16),(T[17]-.3,T[19]-.3,S_vao),(T[19]-.3,T[20]-.3,S_19),(T[20]-.3,T[21]-.3,S_20),(T[21]-.3,T[22]-.3,S_21),(T[22]-.3,T[23]-.3,S_22),(T[23]-.3,T[24]-.3,S_23),(T[24]-.3,T[25]-.3,S_24),
 (T[25]-.3,T[26]-.3,S_map),(T[26]-.3,T[27]-.3,S_26),(T[27]-.3,T[28]-.3,S_27),(T[28]-.3,T[30]-.3,S_tran),(T[30]-.3,T[32]-.3,S_trai),(T[32]-.3,T[33]-.3,S_32),
 (T[33]-.3,T[34]-.3,S_map),(T[34]-.3,T[38]-.3,S_chilang),(T[38]-.3,T[39]-.3,S_map),(T[39]-.3,T[40]-.3,S_39),(T[40]-.3,T[41]-.3,S_40),(T[41]-.3,T[44]-.3,S_tongphat),
 (T[44]-.3,T[45]-.3,S_44),(T[45]-.3,T[46]-.3,S_45),(T[46]-.3,T[47]-.3,S_46),(T[47]-.3,TOTAL+1,S_end)]
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
    if T[5]-4.2<t<T[5]+.2: S_title(cv,t)
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
