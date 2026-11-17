# Bản dài tm3: Trận Như Nguyệt 1077 (giọng Charon gốc, không cân giọng)
import sys,os,subprocess,json,math
import dai
from dai import cam,cpath,to8,stage,PAP,W,H,XM,NM
from canh import *
from dai_tm2 import big,tagfall,strike,lb,dongho,scene_bg,ground
GD=os.environ.get('GIONG','/tmp/pc/assets/thu_giong_hai/charon')
J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm3_full.json'))
TX={i+1:d['text'] for i,d in enumerate(J)};NN={i+1:d['n'] for i,d in enumerate(J)}
def dur(i):
    f=f'{GD}/{NN[i]}.mp3'
    if os.path.exists(f):
        return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    return len(TX[i].split())/3.1+.2
GAP={6:4.0,12:2.6,19:2.6,28:2.6,35:2.6}
T={};E={};t=0.5
for n in TX:
    t+=GAP.get(n,0);T[n]=t;d=dur(n);E[n]=t+d;t+=d+.45
TOTAL=t+4.5
def mid(n,f): return T[n]+(E[n]-T[n])*f
CARDS={12:'Lần thứ nhất · Ngoài biển',19:'Lần thứ hai · Trên sông',28:'Lần thứ ba · Trong trại',35:'Vì sao dừng lại'}
P=PTS
def lan(cv,t,t0,k,t1=None):
    """biểu tượng góc: dòng sông + ba vạch, lần chặn thứ k"""
    t1=t1 or t0+5.0
    if not (t0-.1<t<t1+.6): return
    o=fio(t,t0,t1,.5);x,y=W-330,250;c0=cam(960,540,1)
    put_screen(cv,band(420,200,PAPER,.78,24),x,y+10,o)
    stroke(cv,c0,[(x-170,y-40),(x-90,y-55),(x,y-38),(x+90,y-52),(x+170,y-40)],1,wid=6,head=False,o=o*.8)
    for i in range(3):
        X=x-80+i*80;on=i<k-1 or (i==k-1 and t>t0+.6)
        stroke(cv,c0,[(X,y-10),(X,y+60)],1,wid=9,col=RED if on else INK,head=False,o=o*(1 if on else .25))
    put_screen(cv,text(f'LẦN {k}',40,RED,700,glow=3),x,y+110,o*inn(t,t0+.6,.4))
def night(cv,o):
    if o<=0: return
    cv*=1-.55*o;cv+=np.float32([.05,.06,.09])*o
def banks(cv,c,t,wl=640,luy=1.0,north=True,mist=.6):
    """bờ bắc (phải) - sông - bờ nam có lũy (trái), nhìn ngang"""
    put(cv,c,'far',960,760,ay=1,k=.35,o=.45)
    put(cv,c,'mist',700,640,s=2.6,o=mist,k=.45)
    Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=PAP[Ys:]
    put(cv,c,'water',960,wl-24,ay=0)
    for i,yy in enumerate([wl+8,wl+90,wl+210]):
        put(cv,c,'wave',960-((t*(18+i*9))%200)+(i*77),yy,ay=.5,o=.4-.1*i)
    if luy>0: put(cv,c,'luy',-320,wl+30,ax=0,ay=1,s=.45,o=.8*luy)
# ---------------- chương 1: hook
def S_h1(cv,t):
    a,b=0,E[2]
    c=cam(*cpath(t,[(0,(820,560,1.15)),(T[2],(900,560,1.05)),(mid(2,.5),(1250,540,1.0)),(b+.3,(1300,540,1.0))]))
    wl=620
    banks(cv,c,t,wl,luy=.9)
    if t<1.4:
        u=eo(t/1.3);put_screen(cv,A('blot'),W/2,H/2,(1-u)*.85,s=1.9*(1+u*.9))
    put(cv,c,wipe(A('cau_phao'),inn(t,.2,1.4),0,.2,seed=3),1000,wl+150,ay=1,s=.62)
    for i in range(9):
        st=1.0+i*.45;u=cl((t-st)/4.5)
        if t>st: put(cv,c,Af('fig_giap_giao'),lerp(1600,520,u),wl+60-8*abs(math.sin(t*6+i)),ay=1,s=.32,o=inn(t,st,.3))
    lb(cv,c,'bờ nam',300,330,t,1.5,T[2],sz=36)
    big(cv,'MỘT CÂY CẦU PHAO',t,.25,E[1]+.2,INK,170,84,seed=3)
    if t>T[2]-.3:
        for r in range(3):
            for i in range(9): put(cv,c,'fig_giap_giao',1500+i*95+r*40,wl-40-r*36,ay=1,s=.34-.04*r,o=inn(t,T[2]+(r*9+i)*.03,.4)*(.9-.2*r))
        lb(cv,c,'mười vạn quân',1900,330,t,T[2]+.4,E[2]+.3,col=RED,sz=40)
        stroke(cv,c,[(1000,300),(500,300)],inn(t,mid(2,.55),1.0),wid=6,col=INK,o=.85)
        lb(cv,c,'kinh thành · vài chục cây số',760,270,t,mid(2,.6),E[2]+.3,sz=34)
def S_h3(cv,t):
    a,b=T[3],E[4]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(960,540,1.08))]))
    wl=620;banks(cv,c,t,wl,luy=.9,mist=.8)
    put(cv,c,'cau_phao',960,wl+150,ay=1,s=.62,o=.35)
    big(cv,'KHÔNG QUA NỔI',t,a+.2,E[3]+.2,RED,200,90,seed=4)
    if t>T[4]-.1:
        big(cv,'Chuyện gì đã xảy ra?',t,T[4]+.1,mid(4,.45),INK,170,64,seed=5)
        big(cv,'Vì sao người đang thắng lại đề nghị thôi đánh?',t,mid(4,.45),E[4]+.3,INK,170,54,seed=6)
def S_map(cv,t):
    keys=[(T[5]-.5,(620,560,1.6)),(E[5],(560,600,2.2)),(T[6]-.5,(760,460,1.15)),(E[6],(780,440,1.1)),
          (T[11]-.5,(720,500,1.05)),(E[11],(720,500,1.05)),(T[12]-.5,(620,560,1.5)),(E[12],(640,560,1.5)),
          (T[15]-.5,(560,500,1.6)),(E[15],(520,540,1.8)),(T[16]-.3,(480,580,2.6)),(E[16],(470,590,2.8)),
          (T[36]-.5,(640,460,1.2)),(E[36],(640,460,1.2)),(T[38]-.5,(900,420,1.0)),(E[38],(900,420,1.0)),(T[40]-.5,(520,420,1.6)),(E[40],(520,420,1.6))]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z)
    c=cam(cx,cy,z)
    mapbg(cv,c,u=inn(t,T[5]-1.0,1.4))
    tl,nn,tc,ls,uc,kc,lc,qn,dk=[P[k] for k in ['thanglong','nhunguyet','thicau','langson','ungchau','khamchau','liemchau','quangnguyen','dongkenh']]
    dot(cv,c,*tl,o=1);tag(cv,c,tl[0]-10,tl[1]+46,'Thăng Long',dy=0,sz=30 if z<2 else 22)
    tag(cv,c,300,720,'ĐẠI VIỆT',o=.8,sz=44,dy=0,col=np.float32([.25,.22,.18]))
    tag(cv,c,1150,150,'NHÀ TỐNG',o=.8,sz=44,dy=0,col=RED)
    if t<T[6]:  # đoạn 5
        dot(cv,c,*nn,o=1,col=RED);tag(cv,c,nn[0]+10,nn[1]-12,'sông Như Nguyệt',o=inn(t,T[5]+.3,.5),dy=0,sz=24,col=RED)
    elif t<T[11]:  # đoạn 6: quân Đại Việt đánh trước
        for k,(tg,pt) in enumerate([('Ung Châu',uc),('Khâm Châu',kc),('Liêm Châu',lc)]):
            stroke(cv,c,[(620,520),(760,460) if k==0 else (820,560),pt],inn(t,mid(6,.3)+k*.4,2.0),wid=7,col=INK,o=.9)
            dot(cv,c,*pt,o=inn(t,mid(6,.3),.4),col=RED);tag(cv,c,*pt,tg,o=inn(t,mid(6,.3),.4),dy=-22,col=RED,sz=30)
    elif t<T[12]:  # đoạn 11: chỗ yếu
        stroke(cv,c,[uc,(760,330),(660,400),ls,nn],1,wid=7,col=RED,o=.9)
        stroke(cv,c,[(1350,560),(1000,600),dk,(560,600),nn],inn(t,T[11]+.2,2.0),wid=6,col=RED,o=.8,dash=16)
        dot(cv,c,*nn,o=1,col=RED);tag(cv,c,nn[0]+10,nn[1]-12,'Như Nguyệt',dy=0,sz=26,col=RED)
        lb(cv,c,'nếu đoàn thuyền không tới?',900,700,t,mid(11,.4),E[11]+.3,col=RED,sz=36)
    elif t<T[15]:  # đoạn 12
        stroke(cv,c,[(1350,560),(1000,600),dk],1,wid=6,col=RED,o=.8,dash=16)
        stroke(cv,c,[tl,(560,640),(660,620),dk],inn(t,T[12]+.4,2.0),wid=8,col=INK,o=.9)
        tag(cv,c,dk[0],dk[1]+60,'vùng biển Đông Kênh',o=inn(t,T[12]+.5,.5),dy=0,sz=30)
        tag(cv,c,640,560,'Lý Kế Nguyên',o=inn(t,mid(12,.5),.5),dy=0,sz=30)
    elif t<T[17]:  # đoạn 15-16
        seal(cv,'s1077',W-300,300,T[15]+.2,t,s=.8,o=1-inn(t,E[15],.4))
        dot(cv,c,*ls,o=1);tag(cv,c,*ls,'Lạng Sơn',dy=-22,sz=30)
        stroke(cv,c,[(620,330),ls,(520,520),nn],inn(t,T[15]+.4,E[15]-T[15]-.4),wid=8,col=RED)
        if t>T[16]-.3:
            dot(cv,c,*nn,o=1,col=RED);tag(cv,c,nn[0]+18,nn[1]-12,'sông Như Nguyệt',dy=0,sz=30,col=RED)
            stroke(cv,c,[nn,tl],inn(t,mid(16,.4),1.0),wid=3,head=False,col=INK,dash=6,o=.85)
            tag(cv,c,(nn[0]+tl[0])/2-30,(nn[1]+tl[1])/2,'vài chục cây số',o=inn(t,mid(16,.5),.5),dy=0,sz=30)
    elif t<T[38]:  # đoạn 36: rút quân, giữ Quảng Nguyên
        stroke(cv,c,[nn,(520,520),ls,(620,330),uc],inn(t,T[36]+.2,2.5),wid=7,col=RED,o=.9)
        dot(cv,c,*qn,o=inn(t,mid(36,.5),.4),col=RED,r=12);tag(cv,c,*qn,'châu Quảng Nguyên',o=inn(t,mid(36,.5),.4),dy=-26,col=RED,sz=32)
        lb(cv,c,'nhà Tống giữ lại',qn[0],qn[1]+70,t,mid(36,.6),E[36]+.3,col=RED,sz=30)
    elif t<T[40]:  # đoạn 38
        put_screen(cv,band(1920,420,RED,.10,80),W/2,200,inn(t,T[38],.6))
        big(cv,'NHÀ TỐNG RẤT LỚN',t,T[38]+.2,E[38]+.2,RED,300,70,seed=38)
    else:  # đoạn 40
        dot(cv,c,*qn,o=1,col=INK,r=12);tag(cv,c,*qn,'châu Quảng Nguyên',dy=-26,sz=32)
        lb(cv,c,'trả lại Đại Việt · năm 1079',qn[0],qn[1]+70,t,mid(40,.5),E[40]+.3,sz=30)
def S_title(cv,t):
    t0=T[6]-3.6
    u=inn(t,t0-.3,.8);put_screen(cv,A('blot'),W/2,H/2,u*.97*(1-inn(t,t0+3.2,.6)),s=1.5+.1*(t-t0),r=4*(t-t0))
    tt=text('TRẬN NHƯ NGUYỆT',96,PAPER,700);put_screen(cv,wipe(tt,inn(t,t0+.2,.8),0,.3,seed=3),W/2,H/2-30,1-inn(t,t0+3.2,.5))
    seal(cv,'s1077',W/2+440,H/2+110,t0+1.1,t,s=.75,o=1-inn(t,t0+3.2,.5),r=4)
# ---------------- chương 2
def S_7(cv,t):
    a,b=T[7],E[7]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(900,560,1.12))]))
    put(cv,c,'far',960,760,ay=1,k=.4,o=.45)
    put(cv,c,'citadel',960,720,ay=1,s=.8)
    ground(cv,c,720,.25)
    for i in range(10): put(cv,c,'fig_giap_giao',260+i*150,820+(i%2)*20,ay=1,s=.5,o=inn(t,a+.3+i*.06,.3))
    seal(cv,'s1075',300,260,a+.2,t,s=1.0,r=-4)
    tag(cv,c,960,300,'Ung Châu',o=inn(t,a+.3,.5),dy=0,col=RED,sz=48)
    lb(cv,c,'vây hơn bốn mươi ngày',960,380,t,mid(7,.55),b+.3,sz=36)
    if t>mid(7,.75):
        for k in range(3): put(cv,c,'redblot',760+k*200,640,s=.7,o=.6*inn(t,mid(7,.75)+k*.2,.6))
def S_8(cv,t):
    a,b=T[8],E[8]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(980,580,1.1))]))
    put(cv,c,'court',960,850,ay=1,s=1.0,o=.8)
    put(cv,c,'fig_giap',700,850,ay=1,s=1.05,o=inn(t,mid(8,.35),.5))
    put(cv,c,Af('fig_giap'),1240,850,ay=1,s=1.0,o=inn(t,mid(8,.6),.5))
    tagfall(cv,c,700,520,'Quách Quỳ',t,mid(8,.4),sz=42)
    lb(cv,c,'chủ tướng',700,600,t,mid(8,.45),b+.3,sz=30,col=RED)
    tagfall(cv,c,1240,520,'Triệu Tiết',t,mid(8,.62),sz=42)
    lb(cv,c,'phó tướng',1240,600,t,mid(8,.65),b+.3,sz=30,col=RED)
    big(cv,'TRẢ ĐŨA',t,a+.2,mid(8,.35),RED,160,70,seed=8)
def S_9(cv,t):
    a,b=T[9],E[9]
    c=cam(960+25*(t-a),560,1.0)
    scene_bg(cv,c,.45,.6,820);ground(cv,c,830,.25)
    for r in range(3): put(cv,c,'army',300+r*520-((t-a)*30),800-r*30,ay=1,s=.6-.08*r,o=.95-.2*r)
    put(cv,c,'porters',1500-((t-a)*20),860,ay=1,s=.9,o=inn(t,mid(9,.45),.5))
    lb(cv,c,'khoảng mười vạn quân',700,300,t,a+.4,b+.3,col=RED,sz=40)
    lb(cv,c,'dân phu gánh lương',1500,420,t,mid(9,.5),b+.3,sz=34)
def S_10(cv,t):
    a,b=T[10],E[10]
    c=cam(960+15*(t-a),620,1.1)
    boats=[dict(x=lerp(2000+i*200,1100+i*200,eo(cl((t-a+.3)/5))),y=720+(i%2)*40,s=.6,r=math.sin(t*1.4+i)*1.5,flip=True) for i in range(5)]
    river(cv,c,t,PAP,wl=660,boats=boats,stakes=False,mist=.25,cliffs=False)
    lb(cv,c,'đoàn thuyền chở quân và lương',1100,420,t,a+.4,b+.3,col=RED,sz=38)
# ---------------- chương 3
def S_13(cv,t):
    a,b=T[13],E[14]
    c=cam(*cpath(t,[(a-.4,(1050,640,1.2)),(mid(13,.6),(1000,660,1.28)),(T[14],(1050,650,1.1)),(b+.4,(1000,620,1.05))]),sx=4*math.sin(t*23)*fio(t,a,E[13]),sy=3*math.sin(t*19)*fio(t,a,E[13]))
    wl=640
    boats=[]
    for i in range(5):
        x=lerp(1900+i*150,1150+i*150,eo(cl((t-a+.5)/4)))
        if t>mid(13,.55): x+=lerp(0,800,inn(t,mid(13,.55),3))
        boats.append(dict(x=x,y=wl+14+(i%3)*40,s=.55+(i%3)*.1,r=math.sin(t*1.5+i)*1.4,flip=t<mid(13,.5)))
    viet=[dict(x=lerp(300,700,inn(t,a,3))+i*150,y=wl+40+i*28,s=.65,o=1) for i in range(4)]
    river(cv,c,t,PAP,wl=wl,boats=boats,viet=viet,stakes=False,mist=.3,cliffs=False)
    if t<E[13]:
        for k in range(14):
            ph=((t*.9+k*.29)%1);vi=viet[k%4];bo=boats[(k*2)%5]
            x0,y0=vi['x']+40,vi['y']-60;x1,y1=bo['x']-(k%3-1)*40,bo['y']-80
            hgt=60+(k%3)*20
            def P_(u): return lerp(x0,x1,u),lerp(y0,y1,u)-hgt*4*u*(1-u)
            xa,ya=P_(ph);xb,yb=P_(max(0,ph-.06))
            stroke(cv,c,[(xb,yb),(xa,ya)],1,wid=3,head=True,o=.8*fio(t,a+.4,E[13])*cl((ph-.12)*8)*cl((1-ph)*10))
    lb(cv,c,'thủy quân Đại Việt',600,420,t,a+.3,mid(13,.5),sz=36)
    lb(cv,c,'đoàn thuyền nhà Tống bị chặn',1300,420,t,mid(13,.55),E[13]+.3,col=RED,sz=36)
    lan(cv,t,T[14]+.2,1,mid(14,.6))
    if t>mid(14,.5):
        o=inn(t,mid(14,.5),.5);land=PAP.copy();c2=cam(960+20*(t-mid(14,.5)),560,1.0)
        scene_bg(land,c2,.45,.6,820);ground(land,c2,830,.25)
        for r in range(2): put(land,c2,'army',lerp(1500,900,cl((t-mid(14,.5))/5))+r*500,800-r*30,ay=1,s=.6-.08*r,o=.95-.2*r)
        lb(land,c2,'trên đất liền, Quách Quỳ vẫn tiến quân',960,300,t,mid(14,.55),b+.3,col=RED,sz=38)
        cv*=1-o;cv+=land*o
def S_17(cv,t):
    a,b=T[17],E[17]
    c=cam(*cpath(t,[(a-.4,(900,560,1.0)),(b+.4,(760,600,1.15))]))
    wl=700
    put(cv,c,'far',960,760,ay=1,k=.35,o=.45);put(cv,c,'mist',1200,640,s=2.6,o=.6,k=.45)
    Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=PAP[Ys:];put(cv,c,'water',960,wl-24,ay=0)
    put(cv,c,'luy',960,wl+120,ay=1,s=1.0)
    for i in range(6): put(cv,c,'fig_giap_giao',380+i*220,wl-40,ay=1,s=.55,o=inn(t,mid(17,.5)+i*.08,.4))
    put(cv,c,'fig_giap',300,wl-50,ay=1,s=.85,o=inn(t,mid(17,.3),.4))
    tagfall(cv,c,300,wl-370,'Lý Thường Kiệt',t,mid(17,.32),sz=38,col=INK)
    lb(cv,c,'lũy đất · hàng rào · giữ bến sông',1100,300,t,mid(17,.4),b+.3,sz=36)
def S_18(cv,t):
    a,b=T[18],E[18]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(960,540,1.06))]))
    wl=620;banks(cv,c,t,wl,luy=1.0)
    for r in range(2):
        for i in range(8): put(cv,c,'fig_giap_giao',1300+i*80+r*40,wl-40-r*30,ay=1,s=.34-.04*r,o=.85-.2*r)
    put(cv,c,Af('fig_giap'),1240,wl-30,ay=1,s=.55)
    tagfall(cv,c,1240,wl-260,'Quách Quỳ',t,a+.3,sz=36)
    lb(cv,c,'bờ bắc',1500,300,t,a+.3,b+.3,col=RED,sz=34);lb(cv,c,'bờ nam',350,300,t,a+.3,b+.3,sz=34)
    big(cv,'QUA SÔNG BẰNG CÁCH NÀO?',t,mid(18,.55),b+.4,RED,170,66,seed=18)
# ---------------- chương 4
def S_19(cv,t):
    a,b=T[19],E[19]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(1000,580,1.08))]))
    put(cv,c,'far',960,760,ay=1,k=.4,o=.4)
    put(cv,c,'trai',960,890,ay=1,s=1.0)
    tag(cv,c,500,220,'khúc sông Thị Cầu · Quách Quỳ',o=inn(t,a+.4,.5),dy=0,sz=32,col=RED)
    tag(cv,c,1420,220,'bến Như Nguyệt · Triệu Tiết',o=inn(t,a+1.2,.5),dy=0,sz=32,col=RED)
    dongho(cv,cam(960,540,1),1700,350,.32,t,lvl=lerp(.9,.15,inn(t,mid(19,.4),E[19]-mid(19,.4))),low=lerp(.1,.85,inn(t,mid(19,.4),E[19]-mid(19,.4))))
    lb(cv,c,'chờ đoàn thuyền',1700,560,t,mid(19,.4),b+.3,sz=30)
def S_cau(cv,t):
    a,b=T[20],E[22]
    c=cam(*cpath(t,[(a-.4,(1050,560,1.05)),(T[21],(900,580,1.1)),(mid(21,.6),(600,600,1.25)),(T[22],(700,580,1.1)),(b+.4,(900,560,1.0))]),
          sx=4*math.sin(t*23)*fio(t,T[22],mid(22,.7)),sy=3*math.sin(t*19)*fio(t,T[22],mid(22,.7)))
    wl=620;banks(cv,c,t,wl,luy=1.0)
    put(cv,c,wipe(A('cau_phao'),inn(t,a+.3,2.4),0,.2,seed=3),1000,wl+150,ay=1,s=.62)
    if t>T[20]+2: lb(cv,c,'cầu phao',1300,330,t,T[20]+2,T[21]+.5,sz=40,col=RED)
    # toán quân vượt sang
    for i in range(10):
        st=T[21]+i*.3;u=cl((t-st)/4.0)
        if t<st: continue
        x=lerp(1600,300+(i%4)*60,u)
        if t>T[22]: x=lerp(x,1500,inn(t,T[22]+.3+i*.08,2.4))
        o=inn(t,st,.3)*(1-(.6 if t>mid(22,.5) and i%3==0 else 0))
        put(cv,c,Af('fig_giap_giao') if t<T[22]+.3 else 'fig_giap_giao',x,wl+60-6*abs(math.sin(t*6+i)) if x>450 else wl-20,ay=1,s=.34,o=o)
    if T[21]<t<E[21]+.3:
        stroke(cv,c,[(500,wl+40),(250,wl-30)],inn(t,mid(21,.3),1.0),wid=9,col=RED,o=.9)
        big(cv,'Phòng tuyến bị chọc thủng?',t,mid(21,.5),E[21]+.2,RED,170,60,seed=21)
    if t>T[22]-.2:
        for i in range(8):
            st=T[22]+.1+i*.12;u=eo(cl((t-st)/1.4))
            put(cv,c,'fig_giap_giao',lerp(-100,350+i*50,u),wl-10,ay=1,s=.4,o=inn(t,st,.3))
        tagfall(cv,c,150,wl-330,'Lý Thường Kiệt',t,T[22]+.2,sz=36,col=INK)
        if t>mid(22,.5):
            for k in range(3): put(cv,c,'redblot',600+k*250,wl+60,s=.6,o=.55*inn(t,mid(22,.5)+k*.25,.6))
        lb(cv,c,'hơn một nghìn người chết',1000,300,t,mid(22,.65),b+.3,col=RED,sz=38)
def S_23(cv,t):
    a,b=T[23],E[23]
    c=cam(*cpath(t,[(a-.4,(960,580,1.1)),(b+.4,(900,560,1.0))]))
    wl=620;banks(cv,c,t,wl,luy=1.0)
    for i in range(2):
        x=lerp(1500+i*200,900+i*200,inn(t,a+.2,3));
        if t>mid(23,.5): x+=lerp(0,700,inn(t,mid(23,.5),2.5))
        put(cv,c,'be',x,wl+70+i*40,ay=.85,s=.42,r=math.sin(t*2+i)*2)
    for k in range(10):
        ph=((t*.9+k*.31)%1);x0,y0=420+(k%4)*50,wl-120;x1,y1=1000+(k%3)*120,wl+30
        def P_(u): return lerp(x0,x1,u),lerp(y0,y1,u)-80*4*u*(1-u)
        xa,ya=P_(ph);xb,yb=P_(max(0,ph-.06))
        stroke(cv,c,[(xb,yb),(xa,ya)],1,wid=3,head=True,o=.8*fio(t,a+.3,mid(23,.6))*cl((ph-.12)*8)*cl((1-ph)*10))
    lb(cv,c,'thử vượt sông bằng bè',1200,330,t,a+.3,mid(23,.55),col=RED,sz=36)
    lan(cv,t,mid(23,.6),2,E[23]+1.0)
def S_24(cv,t):
    a,b=T[24],E[24]
    c=cam(*cpath(t,[(a-.4,(960,540,1.0)),(b+.4,(960,540,1.04))]))
    wl=620;banks(cv,c,t,wl,luy=1.0,mist=.9)
    for i in range(6): put(cv,c,'fig_giap_giao',140+i*60,wl-20,ay=1,s=.34,o=.85)
    put(cv,c,'trai',1500,wl-10,ay=1,s=.4,o=.9)
    lb(cv,c,'nhìn nhau qua một dòng nước',960,300,t,mid(24,.5),b+.3,sz=38)
def S_den(cv,t):
    a,b=T[25],E[27]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(900,560,1.1))]))
    wl=700
    put(cv,c,tint(A('sun'),np.float32([.9,.88,.8])),1450,260,s=.7,o=.8,k=.2)
    put(cv,c,'far',960,760,ay=1,k=.35,o=.45);put(cv,c,'mist',960,620,s=3,o=.6)
    Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=PAP[Ys:];put(cv,c,'water',960,wl-24,ay=0)
    put(cv,c,'den',560,wl+10,ay=1,s=.7)
    night(cv,.55)
    for k in range(4):
        ph=((t*.2+k*.25)%1);put(cv,c,'mist',560+k*40,wl-300-ph*200,s=.6,o=.25*math.sin(ph*math.pi))
    if t>mid(25,.5):
        lines=['Sông núi nước Nam','vua Nam ở','sách trời đã định','kẻ xâm phạm sẽ chuốc thất bại']
        for i,l in enumerate(lines):
            st=T[26]+i*(E[26]-T[26])/4.2
            put_screen(cv,text(l,46,PAPER,700,glow=4),1420,330+i*80,fio(t,st,E[27],.5))
    lb(cv,c,'lời truyền',560,280,t,a+.4,T[26],col=PAPER,sz=40)
    if t>T[27]-.2: big(cv,'NAM QUỐC SƠN HÀ',t,T[27],E[27]+.3,RED,160,72,seed=27)
# ---------------- chương 5
def S_om(cv,t):
    a,b=T[28],E[29]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(T[29],(1000,600,1.12)),(b+.4,(1050,620,1.18))]))
    put(cv,c,'far',960,760,ay=1,k=.4,o=.4)
    put(cv,c,'trai',960,890,ay=1,s=1.0)
    if t>T[29]-.3:
        for i in range(6): put(cv,c,'nguoi_om',520+i*180,860+(i%2)*14,ay=1,s=.7,o=inn(t,T[29]+i*.3,.6))
        lb(cv,c,'lương cạn · bệnh tật',960,260,t,T[29]+.2,b+.3,col=RED,sz=40)
    lb(cv,c,'bị kẹt bên bờ bắc',960,260,t,a+.3,T[29]-.3,col=RED,sz=40)
def S_dem(cv,t):
    a,b=T[30],E[31]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(T[31],(1100,600,1.15)),(b+.4,(1150,600,1.2))]),
          sx=4*math.sin(t*23)*fio(t,T[31],mid(31,.7)),sy=3*math.sin(t*19)*fio(t,T[31],mid(31,.7)))
    wl=760
    put(cv,c,'far',960,700,ay=1,k=.35,o=.45)
    put(cv,c,'trai',1250,wl-10,ay=1,s=.75)
    Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=PAP[Ys:];put(cv,c,'water',960,wl-24,ay=0)
    viet=[dict(x=lerp(-100,700,inn(t,a+.2,3.0))+i*110,y=wl+60+i*20,s=.55,o=1) for i in range(3)]
    for b_ in viet: put(cv,c,'smallboat2',b_['x'],b_['y'],s=b_['s']*.95,ax=.5,ay=.86,scale_px=1.5)
    night(cv,.6)
    for b_ in viet: put(cv,c,'duoc',b_['x']+30,b_['y']-120,s=.6,o=1)
    if t>T[31]-.3:
        for i in range(7):
            st=T[31]+i*.15;u=eo(cl((t-st)/1.5))
            put(cv,c,'fig_giap_giao',lerp(700,900+i*90,u),wl-20,ay=1,s=.45,o=inn(t,st,.3))
            put(cv,c,'duoc',lerp(700,900+i*90,u)+30,wl-210,s=.45,o=inn(t,st,.3))
        for k in range(4): put(cv,c,'redblot',1050+k*170,wl-120,s=.8,o=.75*inn(t,mid(31,.3)+k*.25,.6))
        lb(cv,c,'đánh vào doanh trại',1150,300,t,T[31]+.3,b+.3,col=PAPER,sz=40)
    lan(cv,t,mid(31,.6),3,E[31]+1.0)
def S_32(cv,t):
    a,b=T[32],E[32]
    c=cam(960,560,1.0+.02*(t-a))
    put(cv,c,'mist',960,640,s=3.5,o=.8)
    for i,nm in enumerate(['Hoằng Chân','Chiêu Văn']):
        x=720+i*480;put(cv,c,'fig_giap',x,840,ay=1,s=1.1,o=.85-.4*inn(t,mid(32,.75),.8))
        tagfall(cv,c,x,420,nm,t,mid(32,.35)+i*.4,sz=46,col=INK)
    lb(cv,c,'hai hoàng tử nhà Lý',960,280,t,mid(32,.3),b+.3,sz=40)
def S_33(cv,t):
    a,b=T[33],E[34]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(T[34],(960,560,1.0)),(b+.4,(760,560,1.3))]))
    if t<T[34]-.2:
        scene_bg(cv,c,.45,.6,820);ground(cv,c,830,.25)
        for r in range(3):
            for i in range(12):
                if (i*7+r*3)%2==0 and t>mid(33,.3): continue
                put(cv,c,'fig_giap_giao',300+i*110+r*40,800-r*30,ay=1,s=.4-.05*r,o=.9-.2*r)
        lb(cv,c,'mất quá nửa',960,280,t,mid(33,.3),mid(33,.7),col=RED,sz=44)
        lb(cv,c,'vẫn là một đạo quân lớn',960,280,t,mid(33,.72),E[33]+.3,col=RED,sz=44)
    else:
        wl=700
        put(cv,c,'far',960,760,ay=1,k=.35,o=.45);put(cv,c,'mist',1200,640,s=2.6,o=.6,k=.45)
        Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=PAP[Ys:];put(cv,c,'water',960,wl-24,ay=0)
        put(cv,c,'luy',960,wl+120,ay=1,s=1.0)
        put(cv,c,'fig_giap',760,wl-50,ay=1,s=.95)
        big(cv,'ĐÁNH TIẾP HAY DỪNG?',t,mid(34,.35),b+.4,RED,170,74,seed=34)
# ---------------- chương 6
def S_35(cv,t):
    a,b=T[35],E[35]
    c=cam(960+12*(t-a),620,1.05)
    wl=660
    viet=[dict(x=lerp(300,1100,cl((t-a)/(b-a+.5))),y=wl+40,s=.75,o=1)]
    river(cv,c,t,PAP,wl=wl,viet=viet,stakes=False,mist=.7,cliffs=False)
    put(cv,c,'thu_cuon',viet[0]['x'],wl-120,s=.45)
    put(cv,c,'trai',1600,wl-10,ay=1,s=.45,o=.9)
    lb(cv,c,'đề nghị thôi đánh, làm hòa',900,330,t,mid(35,.4),b+.3,sz=40)
def S_37(cv,t):
    a,b=T[37],E[37]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(800,560,1.25))]))
    wl=700
    put(cv,c,'far',960,760,ay=1,k=.35,o=.45);put(cv,c,'mist',1200,640,s=2.6,o=.7,k=.45)
    Ys=int(max(0,min(H,c.p(0,wl)[1])));cv[Ys:]=PAP[Ys:];put(cv,c,'water',960,wl-24,ay=0)
    put(cv,c,'luy',960,wl+120,ay=1,s=1.0);put(cv,c,'fig_giap',800,wl-50,ay=1,s=.95)
    big(cv,'Vì sao đang thắng mà dừng?',t,a+.2,b+.3,INK,170,62,seed=37)
def S_39(cv,t):
    a,b=T[39],E[39]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(960,600,1.1))]))
    put(cv,c,'cho',960,1000,ay=1,s=1.0,o=.9)
    lb(cv,c,'quân dân Đại Việt',960,300,t,a+.3,b+.3,sz=42)
def S_end(cv,t):
    a=T[41]
    c=cam(960,560,1.0+.015*(t-a))
    wl=640;banks(cv,c,t,wl,luy=1.0,mist=.9)
    put(cv,c,'sun',1480,380,o=.5,k=.2);flock(cv,c,t,.7)
    tx=text('Mười vạn quân không qua nổi một dòng sông',60,INK,700);put_screen(cv,wipe(tx,inn(t,a+.3,1.2),0,.3,seed=13),W/2,250)
    seal(cv,'stitle3',W/2,470,mid(41,.5),t,s=.62,r=3)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,H-80,inn(t,E[41]+.5,1))
S=lambda n:T[n]-.3
SH=[(0,S(3),S_h1),(S(3),S(5),S_h3),(S(5),S(7),S_map),(S(7),S(8),S_7),(S(8),S(9),S_8),(S(9),S(10),S_9),(S(10),S(11),S_10),(S(11),S(13),S_map),
 (S(13),S(15),S_13),(S(15),S(17),S_map),(S(17),S(18),S_17),(S(18),S(19),S_18),
 (S(19),S(20),S_19),(S(20),S(23),S_cau),(S(23),S(24),S_23),(S(24),S(25),S_24),(S(25),S(28),S_den),
 (S(28),S(30),S_om),(S(30),S(32),S_dem),(S(32),S(33),S_32),(S(33),S(35),S_33),
 (S(35),S(36),S_35),(S(36),S(37),S_map),(S(37),S(38),S_37),(S(38),S(39),S_map),(S(39),S(40),S_39),(S(40),S(41),S_map),(S(41),TOTAL+1,S_end)]
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
