# Bản dài 16:9 (chưa có giọng): thời gian mỗi đoạn ước theo số chữ
import sys,subprocess
from canh import *
W,H=1920,1080;V=False
PAP=A('paper_h')[...,:3].copy()
J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/bd1_full.json'))
TX={i+1:d['text'] for i,d in enumerate(J)}
GAP={5:3.6,14:2.3,21:2.3,26:2.3,37:2.3}
T={};E={};t=0.4
for n in range(1,len(J)+1):
    t+=GAP.get(n,0);T[n]=t;d=len(TX[n].split())/3.1+.55;E[n]=t+d-.35;t+=d
TOTAL=t+5.0
CARDS={14:'Ngô Quyền bàn kế',21:'Dòng sông có thủy triều',26:'Trận Bạch Đằng',37:'Sau trận đánh'}
P=PTS
def cam(cx,cy,z,sx=0,sy=0): return Cam(cx,cy,z,W,H,sx,sy)
def cpath(t,keys):
    """keys: [(thời điểm,(cx,cy,z))] nội suy mượt"""
    if t<=keys[0][0]: return keys[0][1]
    for (a,ka),(b,kb) in zip(keys,keys[1:]):
        if t<=b: u=ease((t-a)/max(b-a,1e-6));return tuple(lerp(x,y,u) for x,y in zip(ka,kb))
    return keys[-1][1]
# ---------------- thuyền
def fleet_hook(t):
    out=[]
    for i in range(6):
        u=cl((t+1.5-i*.4)/17);x=lerp(2050+i*170,980+i*150+(i%2)*60,1-(1-u)**1.7)
        out.append(dict(x=x,y=640+16+(i%3)*30+math.sin(t*1.9+i)*4,s=.62+(i%3)*.1,r=math.sin(t*1.5+i)*1.4,flip=True))
    return out
# ---------------- cảnh
def S_hook(cv,t):
    kc=cpath(t,[(0,(1250,560,1.18)),(T[2],(1250,560,1.18)),(T[2]+2.5,(1560,610,1.75)),(T[3],(1520,610,1.7)),(T[3]+2.4,(560,640,1.3)),(T[4],(600,650,1.3)),(T[4]+3,(800,900,1.9))])
    c=cam(*kc)
    viet=[dict(x=300+i*90,y=740+i*28,s=.55,flip=False,o=inn(t,T[3]+.5,1.2)) for i in range(3)]
    dk=.35*inn(t,T[4]+.5,2.5)
    river(cv,c,t,PAP,wl=640,boats=fleet_hook(t),viet=viet,under=.0,mist=1,dark=dk,cr=False,sun=.9,birds=1)
    if t<4.6 and HOOKHEAD:
        hd=text('Ai chặn nổi đoàn thuyền này?',80,INK,700,glow=6);put_screen(cv,wipe(hd,inn(t,.3,.9),0,.3,seed=21),W/2,230,1-inn(t,3.9,.6))
    # giọt mực mở đầu
    if t<1.4:
        u=eo(t/1.3);put_screen(cv,A('blot'),W/2,H/2,(1-u)*.85,s=1.9*(1+u*.9))
    seal(cv,'sgiao',W-300,330,T[2]+2.2,t,s=1.0,o=fio(t,0,T[3]+1.2,.5))
def S_title(cv,t,t0):
    u=inn(t,t0-.3,.8);put_screen(cv,A('blot'),W/2,H/2,u*.97*(1-inn(t,t0+3.1,.6)),s=1.5+.1*(t-t0),r=4*(t-t0))
    tt=text('TRẬN BẠCH ĐẰNG',96,PAPER,700);put_screen(cv,wipe(tt,inn(t,t0+.2,.8),0,.3,seed=3),W/2,H/2-30,1-inn(t,t0+3.1,.5))
    seal(cv,'stitle',W/2+460,H/2+110,t0+1.1,t,s=.75,o=1-inn(t,t0+3.1,.5),r=4)
def S_map(cv,t):
    keys=[(T[5],(520,640,1.65)),(T[7]+1,(520,640,1.65)),(T[8],(480,700,1.5)),(T[9]+1.5,(520,680,1.45)),(T[10],(960,520,1.0)),(T[11],(1300,380,1.2)),(T[12],(1150,470,1.05)),(T[13],(960,540,1.0)),
          (T[14],(560,640,1.7)),(T[15]+.5,(560,640,1.7)),(T[16],(900,640,1.15)),(T[17],(760,640,1.4))]
    cx,cy,z=cpath(t,keys);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z)
    c=cam(cx,cy,z)
    mapbg(cv,c,u=inn(t,T[5]-1.0,1.6))
    dl,ac,qc,hm,bd=P['daila'],P['aichau'],P['quangchau'],P['haimon'],P['bachdang']
    # vùng
    tag(cv,c,330,760,'GIAO CHÂU',o=fio(t,T[5]+.6,T[10]+1),sz=44,dy=0,col=np.float32([.25,.22,.18]))
    dot(cv,c,*dl,o=inn(t,T[5]+.8,.4));tag(cv,c,*dl,'Đại La',o=inn(t,T[5]+.9,.4)*(1-inn(t,T[10],.5)*.0),dy=-22)
    if t>T[6]-.2:
        u=inn(t,T[6],.7);put(cv,c,'redblot',dl[0],dl[1],s=.25+.35*u,o=.75*u*(1-inn(t,T[8],1.0)*.6))
    tag(cv,c,dl[0]+120,dl[1]-70,'Dương Đình Nghệ',o=fio(t,T[6]+.3,T[8]+.3),dy=0)
    tag(cv,c,dl[0]-40,dl[1]+70,'Kiều Công Tiễn',o=fio(t,T[6]+1.6,T[10]+.2)+fio(t,T[14],T[16]),dy=0)
    if t>T[14]+1.2:  # gạch tên
        stroke(cv,c,[(dl[0]-150,dl[1]+60),(dl[0]+70,dl[1]+56)],inn(t,T[14]+1.3,.5),wid=5,col=RED,o=1-inn(t,T[16]-.4,.4),head=False)
    stroke(cv,c,[dl,(520,520),(600,430),(700,370)],inn(t,T[7]+.6,1.4),wid=6,o=1-inn(t,T[8]+.5,.6))
    dot(cv,c,*ac,o=inn(t,T[8]+.2,.4));tag(cv,c,*ac,'Ngô Quyền',sub='Ái Châu',o=fio(t,T[8]+.3,T[10]+.5),dy=-22)
    stroke(cv,c,[ac,(395,780),(400,700),(422,630)],inn(t,T[9]+1.0,1.6),wid=7,o=1-inn(t,T[13],.6))
    # sứ sang Nam Hán
    env=[dl,(650,500),(950,360),(1300,250),qc]
    stroke(cv,c,env,inn(t,T[10]+.4,2.4),wid=4,dash=14,head=False,o=1-inn(t,T[12],.6))
    dot(cv,c,*qc,o=inn(t,T[10]+2,.4));tag(cv,c,qc[0]-10,qc[1]+50,'Quảng Châu',o=inn(t,T[10]+2.1,.4)*(1-inn(t,T[14]-1,.5)),dy=0)
    tag(cv,c,1420,300,'NAM HÁN',o=fio(t,T[10]+2.3,T[14]-.5),sz=50,dy=0,col=np.float32([.25,.22,.18]))
    tag(cv,c,qc[0]-70,qc[1]+130,'Lưu Cung',sub='vua Nam Hán',o=fio(t,T[11]+1,T[13]+.5),dy=0)
    # Hải Môn và đường thủy
    stroke(cv,c,[qc,(1600,290),(1350,400),hm],inn(t,T[12]+2.4,1.6),wid=5,col=RED,dash=12,o=1-inn(t,T[14]-.4,.5))
    dot(cv,c,*hm,o=inn(t,T[12]+3.6,.4),col=RED);tag(cv,c,*hm,'Hải Môn',o=fio(t,T[12]+3.6,T[14]-.4),dy=-22,col=RED)
    sea=[(1800,330),(1640,520),(1430,640),(1350,735),(1300,772),(1190,775),(1060,725),(860,672),(700,650),bd]
    up=inn(t,T[12]+.6,2.2)*.42+inn(t,T[15],5.0)*.58
    stroke(cv,c,sea,up,wid=8,o=1)
    tag(cv,c,1560,600,'Lưu Hoằng Tháo',o=fio(t,T[12]+1.4,T[14]-.4),dy=0)
    # thuyền nhỏ chạy trên đường biển
    if t>T[12]+.6:
        seg=np.float32(sea);L=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(seg,axis=0),axis=1))])
        for j in range(3):
            d=L[-1]*max(0,up-.05*j)
            x=np.interp(d,L,seg[:,0]);y=np.interp(d,L,seg[:,1])
            put(cv,c,Af('bigboat2'),x+16*j,y-4-8*j,s=.2,o=.9,ay=.9,scale_px=1.5)
    dot(cv,c,*bd,o=inn(t,T[15]+3,.4));tag(cv,c,*bd,'Cửa sông Bạch Đằng',o=inn(t,T[15]+3.1,.5),dy=-22)
    seal(cv,'s937',W-270,300,T[5]+.6,t,s=.8,o=1-inn(t,T[7],.4))
    seal(cv,'s931',W-270,300,T[7]+.3,t,s=.8,o=1-inn(t,T[8]+.5,.4))
    seal(cv,'s938',W-270,300,T[9]+.2,t,s=.8,o=1-inn(t,T[10]+.8,.4))

# ---------- tranh minh họa cho chương 2–3
def stage(cv,c,t,far=.5,mist=.8,ground=880):
    put(cv,c,'far',960,ground-60,ay=1,k=.4,o=far)
    put(cv,c,'mist',500,ground-160,s=2.6,o=mist,k=.5);put(cv,c,'mist',1400,ground-220,s=2.2,o=mist*.8,k=.5)
def gnd(cv,c,y=900,o=.25):
    put(cv,c,'water',960,y,ay=0,o=o)
def bob(t,k=0,a=4,f=6): return abs(math.sin(t*f+k))*-a
def S_hall(cv,t):
    a,b=T[6],E[6];u=cl((t-a)/(b-a))
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(900,580,1.18))]))
    put(cv,c,'hall',960,900,ay=1,s=1.0)
    put(cv,c,'fig_quan',780,762,ay=1,s=1.7,scale_px=1.5)
    sx=lerp(1260,1050,inn(t,a+2.2,1.6));put(cv,c,'fig_satthu',sx,762,ay=1,s=1.7,o=inn(t,a+2.0,1.0)*.95,scale_px=1.5)
    tag(cv,c,760,440,'Dương Đình Nghệ',o=fio(t,a+.4,b+.4),dy=0)
    tag(cv,c,1080,380,'Kiều Công Tiễn',o=fio(t,a+2.8,b+.4),dy=0,col=RED)
    if t>a+4.0:
        v=inn(t,a+4.0,1.6);put(cv,c,'redblot',820,700,s=1.2+2.8*v,o=.55*v,r=20*v)
        ink_wash(cv,.35*v)
def S_931(cv,t):
    a,b=T[7],E[7]
    c=cam(*cpath(t,[(a-.4,(960,540,1.0)),(b+.4,(1060,560,1.06))]))
    stage(cv,c,t,far=.6);gnd(cv,c,880,.3)
    x=lerp(350,820,inn(t,a,b-a));put(cv,c,'army',x,920+bob(t,0,3,5),ay=1,s=1.0,o=inn(t,a-.3,.6))
    x2=lerp(1550,2250,inn(t,a+1.0,b-a-1));put(cv,c,Af('army'),x2,790+bob(t,1,3,7),ay=1,s=.55,o=.75*(1-inn(t,b-2,1.5)),scale_px=1.5)
    tag(cv,c,x,640,'quân Dương Đình Nghệ',o=fio(t,a+.8,b+.3),dy=0)
    tag(cv,c,min(x2,1600),600,'quân Nam Hán rút chạy',o=fio(t,a+1.8,b+.3),dy=0,col=RED)
    seal(cv,'s931',W-270,300,a+.3,t,s=.8,o=1-inn(t,b,.4))
def S_aichau(cv,t):
    a,b=T[8],E[8]
    c=cam(*cpath(t,[(a-.4,(900,520,1.0)),(b+.4,(820,500,1.15))]))
    put(cv,c,'far',960,760,ay=1,k=.4,o=.7);put(cv,c,'mid',700,980,ay=1,k=.7,o=.9,s=1.0)
    put(cv,c,'mist',1300,700,s=2.6,o=.8,k=.6)
    put(cv,c,'cliffL',560,1120,ax=0,ay=1,s=.7)
    put(cv,c,'fig_tuong',697,530,ay=1,s=1.2,scale_px=1.5,o=inn(t,a,.8))
    put(cv,c,'army',1250,880,ay=1,s=.65,o=inn(t,a+1.0,1.0)*.9)
    tag(cv,c,697,250,'Ngô Quyền',sub='con rể Dương Đình Nghệ',o=fio(t,a+.5,b+.4),dy=0,sz=40)
    tag(cv,c,1250,700,'Ái Châu (Thanh Hóa)',o=fio(t,a+3.5,b+.4),dy=0)
def S_porters(cv,t):
    a,b=T[10],E[10]
    c=cam(*cpath(t,[(a-.4,(900,540,1.0)),(b+.4,(1100,560,1.08))]))
    stage(cv,c,t,far=.6);gnd(cv,c,880,.3)
    stroke(cv,c,[(-200,925),(2200,910)],1,wid=5,head=False,o=.5)
    x=lerp(300,1150,inn(t,a-.3,b-a+.5));put(cv,c,'porters',x,922+bob(t,0,4,5),ay=1,s=1.5)
    tag(cv,c,x+480,560,'sứ của Kiều Công Tiễn',o=fio(t,a+.5,b+.4),dy=0)
    tag(cv,c,1550,420,'sang Nam Hán →',o=fio(t,a+2.5,b+.4),dy=0,col=RED)
def S_court(cv,t):
    a,b=T[11],E[11]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(a+3,(960,520,1.12)),(b+.4,(900,520,1.2))]))
    put(cv,c,'court',960,1010,ay=1,s=1.05)
    tag(cv,c,1530,300,'Lưu Cung',sub='vua Nam Hán',o=fio(t,a+.6,b+.4),dy=0,sz=40)
    if t>a+3.5:
        stroke(cv,c,[(1110,500),(1170,390),(820,320),(320,350),(80,420)],inn(t,a+3.6,1.8),wid=10,col=RED,o=.85*(1-inn(t,b,.4)))
        tag(cv,c,260,310,'đất Việt',o=fio(t,a+4.6,b+.4),dy=0,col=RED,sz=38)
def S_harbor(cv,t):
    a,b=T[13],T[14]-1.6
    c=cam(*cpath(t,[(a-.4,(1100,560,1.0)),(b+.4,(1000,600,1.1))]))
    bs=[]
    for i in range(9):
        ln=i%3;x=lerp(1700+i*130,700+i*120,inn(t,a-1+i*.2,b-a+1))
        bs.append(dict(x=x,y=660+ln*45+math.sin(t*1.8+i)*4,s=.5+ln*.13,r=math.sin(t*1.4+i)*1.5,flip=True,ln=ln))
    bs.sort(key=lambda q:q['ln'])
    river(cv,c,t,PAP,wl=640,boats=bs,cliffs=False,mist=1.2,dark=.12,stakes=False)
def S_citadel(cv,t):
    a,b=T[14],E[14]
    sh=3*math.sin(t*31) if a+2<t<b else 0
    c=cam(*cpath(t,[(a-1.2,(960,520,1.0)),(b+.4,(1000,560,1.1))]),sh,sh)
    put(cv,c,'far',960,560,ay=1,k=.4,o=.5)
    put(cv,c,'citadel',1100,900,ay=1,s=.95)
    for k in range(3): put(cv,c,'mist',700+k*400,400+20*math.sin(t+k),s=1.8,o=.35+.3*inn(t,a+2,2),k=.8)
    x=lerp(-500,500,inn(t,a-.6,3.5));put(cv,c,'army',x,1000+bob(t,0,3,6),ay=1,s=1.0)
    x2=lerp(-900,150,inn(t,a+.4,3.5));put(cv,c,'army',x2,1060+bob(t,1,3,6),ay=1,s=1.1)
    tag(cv,c,1100,250,'thành Đại La',o=fio(t,a+.3,a+3.2),dy=0,sz=40)
    if t>a+3.2:
        tx=text('Kiều Công Tiễn',46,INK,700,glow=5);X,Y=c.p(1100,180);put_screen(cv,tx,X,Y,fio(t,a+3.2,b+.4))
        stroke(cv,Cam(W/2,H/2,1,W,H),[(X-190,Y-12),(X+190,Y-16)],inn(t,a+3.8,.5),wid=6,col=RED,head=False,o=1-inn(t,b,.4))
def S_sea(cv,t):
    a,b=T[15],E[15]
    c=cam(*cpath(t,[(a-.4,(1000,560,1.05)),(b+.4,(900,600,1.12))]))
    bs=[dict(x=lerp(1500+i*140,900+i*130,inn(t,a-.4,b-a+.8)),y=650+(i%3)*45+math.sin(t*2+i)*7,s=.5+(i%3)*.13,r=math.sin(t*1.7+i)*3,flip=True,ln=i%3) for i in range(7)]
    bs.sort(key=lambda q:q['ln'])
    river(cv,c,t,PAP,wl=640,boats=bs,cliffs=False,mist=1.0,stakes=False,ridge_o=.35)
    tag(cv,c,1200,380,'vẫn tiến về cửa sông Bạch Đằng',o=fio(t,a+2.5,b+.4),dy=0)
def S_council(cv,t):
    c=cam(*cpath(t,[(T[17]-.6,(960,560,1.0)),(T[20],(960,600,1.08))]))
    put(cv,c,'far',960,700,ay=1,k=.4,o=.55);put(cv,c,'mist',600,620,s=2.5,o=.8,k=.5);put(cv,c,'mist',1400,560,s=2.2,o=.7,k=.5)
    put(cv,c,wipe(A('council'),inn(t,T[17]-.4,1.4),0,.25,seed=6),960,920,ay=1,s=.95,scale_px=1.5)
    tag(cv,c,960,505,'Ngô Quyền',o=fio(t,T[17]+1.2,T[18]+.5),dy=0,sz=34)
    items=[(T[18]+1.6,'trẻ dại'),(T[18]+3.6,'từ xa tới, đã mỏi mệt'),(T[18]+5.6,'mất người làm nội ứng')]
    o_all=1-inn(t,T[20]-.4,.5)
    for i,(t0,s) in enumerate(items):
        tx=text(s,48,INK,700,glow=5);put_screen(cv,wipe(tx,inn(t,t0,.6),0,.3,seed=i+2),[450,960,1450][i],170,o_all*(1-inn(t,T[19]+2.5,.5)*.55))
    tx=text('nhưng: hơn hẳn về chiến thuyền',58,RED,700,glow=5);put_screen(cv,wipe(tx,inn(t,T[19]+2.6,.7),0,.3,seed=9),W/2,240,o_all)
def S_q(cv,t):
    c=cam(*cpath(t,[(T[20]-.5,(1100,560,1.25)),(E[20]+1,(1180,600,1.5))]))
    b=[dict(x=lerp(1700,1250,cl((t-T[20]+.5)/4)),y=656,s=1.5,flip=True,r=math.sin(t*1.4))]
    river(cv,c,t,PAP,wl=640,boats=b,under=0,mist=1.6,dark=.08)
def S_mapBD(cv,t):
    c=cam(*cpath(t,[(T[21]-1,(700,620,1.2)),(T[21]+2.5,(620,630,2.2))]))
    mapbg(cv,c);bd=P['bachdang']
    dot(cv,c,*bd,o=1);tag(cv,c,*bd,'Sông Bạch Đằng',o=inn(t,T[21]+.5,.5),dy=-24)
    tag(cv,c,bd[0]+60,bd[1]-90,'Quảng Ninh',o=inn(t,T[21]+2.6,.5)*.75,dy=0,sz=26)
    tag(cv,c,bd[0]-70,bd[1]+40,'Hải Phòng',o=inn(t,T[21]+2.9,.5)*.75,dy=0,sz=26)
_BX=[330,425,520,685,850,1015,1180,1275,1370];_BY=[230,290,318,336,340,336,330,295,230]
def bedy(x): return 460+float(np.interp(x-110,_BX,_BY))
def S_cross(cv,t):
    """mặt cắt lòng sông: thủy triều lên xuống, cọc, thuyền"""
    c=cam(*cpath(t,[(T[22]-.6,(960,560,1.0)),(E[25],(960,560,1.04))]))
    # mực nước theo lời kể
    hi,lo=430,640
    k=[(T[22],lo),(T[22]+2.2,hi),(T[22]+3.6,hi),(E[22]-.4,lo),(T[24],lo),(T[24]+2.2,hi),(E[25],hi)]
    wl=k[0][1]
    for (a,va),(b,vb) in zip(k,k[1:]):
        if a<=t<=b: wl=lerp(va,vb,ease((t-a)/max(b-a,1e-6)));break
        if t>b: wl=vb
    # nước
    y0=int(c.p(0,wl)[1]);cv[y0:]=cv[y0:]*(1-.18)+INK*.18
    for i in range(2):
        put(cv,c,'wave',960-((t*20+i*70)%200),wl+i*16,o=.7-.3*i)
    put(cv,c,'riverbed',960,980,ay=1,s=1)
    # cọc đóng xuống lòng sông (chân cọc cắm vào đáy)
    for i,xx in enumerate(range(480,1460,44)):
        by=bedy(xx)+30
        td=T[23]+1.2+i*.09
        if t<td-.5: continue
        u=eo((t-td+.5)/.5);top=by-272;y=lerp(top-300,top,u)
        im=rowclip(A('stake'),(wl-y)*1.5/.85,below=.22,soft=4) if wl>y else A('stake')
        put(cv,c,im,xx+(i%2)*6,y,s=.85,ax=.5,ay=0,scale_px=1.5)
    # thước đo
    put(cv,c,'gauge',1790,960,ay=1,s=.95)
    gy=wl;stroke(cv,c,[(1730,gy),(1772,gy)],1,wid=6,col=RED,head=True)
    tag(cv,c,1640,hi-30,'thủy triều lên',o=fio(t,T[22]+.4,E[22]-1.6),dy=0,sz=30)
    tag(cv,c,1610,lo+40,'thủy triều rút xuống',o=fio(t,E[22]-2.2,T[23]+1),dy=0,sz=30)
    tag(cv,c,960,250,'cọc vạt nhọn, bịt sắt',o=fio(t,T[23]+2.6,T[24]+.4),dy=0,sz=40)
    # thuyền trên mặt nước khi nước che kín cọc
    if t>T[24]+1.5:
        bx=lerp(1500,950,cl((t-T[24]-1.5)/(E[25]-T[24]-1.5)))
        put(cv,c,Af('bigboat2'),bx,wl+12,s=.8,o=inn(t,T[24]+1.5,.6),ay=.9,r=math.sin(t*1.6),scale_px=1.5)
    if t>T[25]:
        sx=lerp(1150,700,cl((t-T[25])/3.5))
        put(cv,c,Af('smallboat2'),sx,wl+10,s=.6,o=inn(t,T[25],.5),ay=.82,scale_px=1.5)
        stroke(cv,c,[(1000,lo),(1500,lo)],inn(t,T[25]+2.5,.8),wid=3,dash=10,head=False,col=RED,o=.9)
        tag(cv,c,1250,lo-8,'khi thủy triều rút',o=inn(t,T[25]+3,.5),dy=0,sz=28,col=RED)
# ------------- trận đánh
LOW=895
def wl_battle(t):
    return 640+(LOW-640)*inn(t,T[30]+.2,(E[32]-T[30]))
def lane_of(i): return [0,1,2,0,1,2][i]
def capt_time(i): return E[33]+2 if i==0 else T[32]+.3+[0,.9,.4,1.5,1.2,2.0][i]
BX0=[840,930,1010,1130,1250,1350]
def battle_boats(t):
    wl=wl_battle(t);out=[]
    for i in range(6):
        ln=lane_of(i)
        xs=[(T[26]-1,1950+i*170),(E[27],1500+i*130),(T[29],1420+i*120),(E[29],BX0[i])]
        x=xs[0][1]
        for (a,va),(b,vb) in zip(xs,xs[1:]):
            if a<=t<=b: x=lerp(va,vb,ease((t-a)/(b-a)));break
            if t>b: x=vb
        keel=wl+14+ln*45
        if ZONE[0]<x<ZONE[1]: keel=min(keel,LANE_TIP[ln]+12)
        s=.6+ln*.13;r=math.sin(t*1.5+i)*1.4;o=1;y=keel
        tc=capt_time(i)
        if t>tc:
            v=t-tc;r+=(-1 if i%2 else 1)*min(78,60*v*v+25*v);y+=110*v*v;o=cl(1-(v-.7)/1.3)
        out.append(dict(x=x,y=y,s=s,r=r,o=o,flip=True,ln=ln))
    out.sort(key=lambda b:b['ln'])
    return out
def splashes(t):
    def f(cv,c):
        for i in range(6):
            tc=capt_time(i)
            if tc+.3<t<tc+1.9:
                v=(t-tc-.3)/1.6;x=BX0[i];put(cv,c,'splash',x,LANE_TIP[lane_of(i)]+60,s=.9+1.1*v,o=(1-v)*.95,ay=.95)
    return f
def arrows(t,t0,t1,n=26,seed=1):
    def f(cv,c):
        if not (t0<t<t1+1.5): return
        r=np.random.default_rng(seed)
        for j in range(n):
            ts=t0+r.random()*(t1-t0);fl=1.1+r.random()*.4
            if not ts<t<ts+fl: continue
            u=(t-ts)/fl;side=j%2
            sx,sy=(150+r.random()*250,760+r.random()*80) if side==0 else (1850-r.random()*200,780+r.random()*60)
            ex,ey=900+r.random()*500,700+r.random()*60
            x=lerp(sx,ex,u);y=lerp(sy,ey,u)-260*u*(1-u)
            dx=ex-sx;dy=(ey-sy)-260*(1-2*u)
            ang=math.degrees(math.atan2(dy,dx))
            put(cv,c,'arrow',x,y,s=.8,r=ang,o=.9)
    return f
def viet_battle(t):
    out=[]
    for i in range(4):  # khiêu chiến rồi giả thua
        x0=-260-i*90;x1=820-i*100
        if t<T[28]: continue
        u1=cl((t-T[28])/3.0);u2=cl((t-T[28]-3.4)/3.2)
        x=lerp(x0,x1,ease(u1));fl=False
        if u2>0: x=lerp(x1,x0-200,ease(u2));fl=True
        out.append(dict(x=x,y=wl_battle(t)+50+(i%2)*40,s=.6,flip=fl))
    if t>T[31]-.3:  # tung quân ra đánh từ hai bên
        u=ease((t-T[31]+.3)/3.5)
        for i in range(5):
            out.append(dict(x=lerp(-200-i*80,560+i*60,u),y=wl_battle(t)+70+(i%3)*34,s=.6+(i%3)*.08))
            out.append(dict(x=lerp(2150+i*80,1560-i*50,u),y=wl_battle(t)+60+(i%3)*34,s=.6+(i%3)*.08,flip=True))
    if t>T[34]:  # vây thuyền chủ tướng
        u=ease((t-T[34])/3)
        for i in range(3): out.append(dict(x=lerp(480,700+i*90,u),y=wl_battle(t)+70+i*22,s=.62))
    return out
def S_battle(cv,t):
    keys=[(T[26]-1,(1200,560,1.0)),(E[27],(1300,620,1.08)),(T[28],(900,640,1.08)),(E[29],(1080,680,1.12)),(T[30]+.5,(1100,760,1.32)),(E[30],(1100,780,1.32)),(T[31],(1000,740,1.12)),
          (T[32],(1100,790,1.25)),(T[33],(960,680,1.0)),(T[34],(860,800,1.3)),(E[34],(840,800,1.35))]
    cx,cy,z=cpath(t,keys)
    sh=0
    if T[31]<t<E[32]: sh=5*math.sin(t*37)*(1-cl((t-T[31])/(E[32]-T[31])))
    c=cam(cx,cy,z,sh,sh*.6)
    wl=wl_battle(t)
    under=.06*inn(t,T[29],2)
    river(cv,c,t,PAP,wl=wl,clx=-330,boats=battle_boats(t),viet=viet_battle(t),under=under,fx=[splashes(t),arrows(t,T[31]+.4,E[31]+1,30,1),arrows(t,T[32],E[32],20,2)])
    # thước thủy triều nhỏ góc trái
    if T[29]+1<t<E[32]+2:
        o=fio(t,T[29]+1,E[32]+2,.5);gx,gy=W-110,600
        put_screen(cv,A('gauge'),gx,gy,o*.9,s=.45)
        yy=gy-140+280*(wl-640)/(LOW-640)
        stroke(cv,Cam(960,540,1,W,H),[(gx-70,yy),(gx-24,yy)],1,wid=5,col=RED,o=o)
        put_screen(cv,text('thủy triều',26,INK,700,glow=3),gx,gy+170,o)
    seal(cv,'sgiao',W-300,330,T[34]+.4,t,s=1.0,fall=E[34]-1.2)
def S_retreat(cv,t):
    cx,cy,z=cpath(t,[(T[35]-.6,(1300,400,1.25)),(E[35],(1400,330,1.3))]);cx=min(max(cx,960/z),1920-960/z);cy=min(max(cy,540/z),1080-540/z);c=cam(cx,cy,z)
    mapbg(cv,c);hm,qc=P['haimon'],P['quangchau']
    dot(cv,c,*hm,col=RED);tag(cv,c,*hm,'Hải Môn',col=RED,dy=-22)
    tag(cv,c,hm[0]-150,hm[1]+110,'Lưu Cung',sub='rút quân về',o=inn(t,T[35]+1.2,.5),dy=0)
    stroke(cv,c,[hm,(1350,380),(1600,280),qc],inn(t,T[35]+1.6,2.2),wid=6,col=RED,dash=12)
    dot(cv,c,*qc);tag(cv,c,qc[0]-10,qc[1]+50,'Quảng Châu',dy=0)
def S_after(cv,t):
    c=cam(*cpath(t,[(T[36]-.6,(960,620,1.05)),(E[36]+1,(860,640,1.12))]))
    wr=[dict(name='wreck',x=600+i*170+t*6,y=896+(i%2)*20,s=.8,r=(i*23)%30-15,flip=i%2) for i in range(6)]
    river(cv,c,t,PAP,wl=880,boats=wr,under=1,mist=1.4,birds=1,sun=.5)
def S_king(cv,t):
    c=cam(*cpath(t,[(T[37]-1,(960,600,1.0)),(E[38],(960,560,1.05))]))
    put(cv,c,'far',960,820,ay=1,k=.4,o=.8);put(cv,c,'mist',700,700,s=2.5,o=.8);put(cv,c,'mist',1300,640,s=2.2,o=.8)
    seal(cv,'s939',W/2-520,H/2-40,T[37]+.6,t,s=1.15,r=-4)
    tx=text('Ngô Quyền xưng vương',76,INK,700);put_screen(cv,wipe(tx,inn(t,T[37]+1.2,.9),0,.3,seed=5),W/2+120,H/2-70)
    for i,s in enumerate(['Dương thị làm hoàng hậu','đặt chức quan, phép tắc triều đình']):
        tx=text(s,44,INK,600);put_screen(cv,wipe(tx,inn(t,T[38]+.6+i*2.4,.8),0,.3,seed=i+11),W/2+120,H/2+40+i*70)
def S_coloa(cv,t):
    c=cam(*cpath(t,[(T[39]-.8,(960,560,1.0)),(E[39]+1,(960,560,1.12))]))
    put(cv,c,'mist',500,300,s=2.2,o=.7)
    put(cv,c,wipe(A('coloa2'),inn(t,T[39]-.3,2.0),1,.25,seed=2),960,560,s=.9,scale_px=1.5)
    tag(cv,c,960,560,'Cổ Loa',sub='kinh đô',o=inn(t,T[39]+1.6,.5),dy=0,sz=58)
def S_line(cv,t):
    c=cam(*cpath(t,[(T[40]-.8,(900,540,1.0)),(T[41],(960,540,1.0)),(T[42],(1350,540,.95)),(E[42],(1420,540,.95))]))
    y=560
    stroke(cv,c,[(-300,y),(1100,y)],inn(t,T[40]-.2,2.2),wid=12,head=False)
    tag(cv,c,420,y+125,'hơn một nghìn năm phương Bắc đô hộ',o=inn(t,T[40]+1.2,.6),dy=0,sz=40)
    stroke(cv,c,[(1100,y),(1220,y)],inn(t,T[40]+2.6,.6),wid=12,col=RED,head=False)
    dot(cv,c,1100,y,o=inn(t,T[40]+2.4,.3),col=RED,r=12)
    tag(cv,c,1100,y+105,'938',o=inn(t,T[40]+2.5,.4),dy=0,sz=40,col=RED)
    dot(cv,c,1180,y,o=inn(t,T[41]+.6,.3),r=10);tag(cv,c,1340,y+125,'944 · Ngô Quyền mất',o=inn(t,T[41]+.7,.4),dy=0,sz=34)
    stroke(cv,c,[(1220,y),(2150,y)],inn(t,T[42]+.3,2.2),wid=4,dash=16,head=False)
    dot(cv,c,2150,y,o=inn(t,T[42]+2.4,.3),r=12,col=RED)
    seal(cv,'s1288',c.p(2150,0)[0],c.p(0,y+130)[1],T[42]+2.5,t,s=.8)
    # tranh nhỏ trên trục thời gian
    o1=inn(t,T[40]+2.8,.8)
    for k in range(6): put(cv,c,'stake',1040+k*24,y-150+(k%2)*8,s=.32,ay=0,o=o1)
    put(cv,c,Af('bigboat2'),1110,y-150,s=.38,r=35,o=o1*.9,scale_px=1.5)
    put(cv,c,'citadel',400,y-60,ay=1,s=.38,o=.45*inn(t,T[40]+.8,1.2))
    put(cv,c,'fig_tuong',1260,y-20,ay=1,s=.45,o=inn(t,T[41]+.8,.6)*.85,scale_px=1.5)
    o3=inn(t,T[42]+2.8,.8)
    for k in range(6): put(cv,c,'stake',2080+k*24,y-150+(k%2)*8,s=.32,ay=0,o=o3)
    for k in range(2): put(cv,c,Af('bigboat2'),2120+k*60,y-150,s=.34,r=-30+k*50,o=o3*.6,scale_px=1.5)
def ghosts(t):
    out=[]
    for i in range(5):
        x=860+i*120;out.append(dict(x=x,y=806+(i%3)*12,s=.6,r=(i%2*2-1)*(8+i*3),o=.42,flip=True))
    return out
def S_1288(cv,t):
    c=cam(*cpath(t,[(T[43]-.8,(1100,700,1.25)),(E[44]+1,(1050,720,1.4))]))
    river(cv,c,t,PAP,wl=880,boats=ghosts(t),under=1,mist=1.3)
    tag(cv,c,1100,560,'năm 1288 · quân Nguyên',o=inn(t,T[43]+1,.6)*(1-inn(t,E[44],.5)),dy=0,sz=40)
def S_end(cv,t):
    c=cam(960,560,1.0+.02*(t-T[45]))
    put(cv,c,'sun',1500,330,o=.8,k=.2);flock(cv,c,t,.8);put(cv,c,'far',960,860,ay=1,k=.4,o=.55);put(cv,c,'mist',960,760,s=3,o=.9)
    tx=text('Hiểu dòng sông hơn đối thủ',78,INK,700);put_screen(cv,wipe(tx,inn(t,T[45]+.3,1.2),0,.3,seed=13),W/2,H/2-70)
    seal(cv,'stitle',W/2,H/2+150,T[45]+1.6,t,s=.7,r=3)
    put_screen(cv,text('Người Gác Sử',34,INK,600),W/2,H-120,inn(t,E[45]+.5,1))
SHOTS=[(0,T[5]-.4,S_hook),(T[5]-.4,T[6]-.3,S_map),(T[6]-.3,T[7]-.3,S_hall),(T[7]-.3,T[8]-.3,S_931),(T[8]-.3,T[9]-.3,S_aichau),(T[9]-.3,T[10]-.3,S_map),
       (T[10]-.3,T[11]-.3,S_porters),(T[11]-.3,T[12]-.3,S_court),(T[12]-.3,T[13]-.3,S_map),(T[13]-.3,T[14]-1.6,S_harbor),(T[14]-1.6,T[15]-.3,S_citadel),
       (T[15]-.3,T[16]-.3,S_sea),(T[16]-.3,T[17]-.3,S_map),(T[17]-.3,T[20]-.3,S_council),(T[20]-.3,T[21]-1.0,S_q),(T[21]-1.0,T[22]-.3,S_mapBD),(T[22]-.3,T[26]-.6,S_cross),
       (T[26]-.6,T[35]-.3,S_battle),(T[35]-.3,T[36]-.3,S_retreat),(T[36]-.3,T[37]-.6,S_after),(T[37]-.6,T[39]-.3,S_king),(T[39]-.3,T[40]-.3,S_coloa),(T[40]-.3,T[43]-.3,S_line),
       (T[43]-.3,T[45]-.3,S_1288),(T[45]-.3,TOTAL+1,S_end)]
LOGO=None
HOOKHEAD=True
_r=np.random.default_rng(2);NM=cv2.resize(_r.random((6,10)).astype(np.float32),(W,H),interpolation=cv2.INTER_CUBIC)
NM=(NM-NM.min())/(NM.max()-NM.min());XM=np.linspace(0,1,W,dtype=np.float32)[None,:]*np.ones((H,1),np.float32)
def frame(t):
    global LOGO
    act=[s for s in SHOTS if s[0]-.35<=t<s[1]+.35]
    def one(fn):
        cv=PAP.copy();fn(cv,t);return cv
    if len(act)==1: cv=one(act[0][2])
    else:
        a,b=act[0],act[1];cut=b[0];u=cl((t-(cut-.35))/.7)
        ca,cb=one(a[2]),one(b[2])
        m=np.clip((u*1.7-.35-XM*.35-NM*.35)/.3,0,1)[...,None]
        cv=ca*(1-m)+cb*m
    if 4.5<t-T[4]+0 and t<T[5]+3.5: pass
    if T[4]<t<T[5]+.5: S_title(cv,t,T[5]-3.3)
    for n,s in CARDS.items(): card(cv,t,T[n]-2.0,s,PAP)
    # phụ đề
    for n in TX:
        if T[n]-.3<t<E[n]+.5:
            caption(cv,TX[n],inn(t,T[n]-.25,.25)*(1-inn(t,E[n]+.15,.3)),V)
    if LOGO is None:
        lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4];LOGO=lg
    blend(cv,LOGO,W-44-130,34,.8)
    return cv
def to8(cv): return (np.clip(cv,0,1)*255+.5).astype(np.uint8)
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='soi':
        for x in sys.argv[2:]:
            if x[0]=='t': tt=float(x[1:])
            elif '+' in x: tt=T[int(x.split('+')[0])]+float(x.split('+')[1])
            elif '-' in x: tt=T[int(x.split('-')[0])]-float(x.split('-')[1])
            else: tt=T[int(x)]+1.5
            Image.fromarray(to8(frame(tt))).save(f'/tmp/gen/bd/out/s_{x}.jpg',quality=85)
        print('TOTAL',round(TOTAL,1))
    else:
        out,i0,i1,fps=sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
        ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        for i in range(i0,i1): ff.stdin.write(to8(frame(i/fps)).tobytes())
        ff.stdin.close();ff.wait()
