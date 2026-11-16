# Bản dài v2 (kịch bản bd2, giọng Charon). Dùng lại cảnh của dai.py, đổi số đoạn cũ sang thời điểm mới.
import sys,os,subprocess,json,math
import dai
from dai import *
GD=os.environ.get('GIONG','/tmp/pc/assets/thu_giong_hai/bd2_chuan')
J2=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/bd2_full.json'))
TX2={i+1:d['text'] for i,d in enumerate(J2)};NN={i+1:d['n'] for i,d in enumerate(J2)}
def dur(i):
    f=f'{GD}/{NN[i]}.mp3'
    if os.path.exists(f):
        return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    return len(TX2[i].split())/3.1+.2
GAP2={6:3.8,17:2.6,23:2.6,30:2.6,40:2.6}
T2={};E2={};t=0.5
for n in TX2:
    t+=GAP2.get(n,0);T2[n]=t;d=dur(n);E2[n]=t+d;t+=d+.45
TOT2=t+4.5
mid=lambda n,f: T2[n]+(E2[n]-T2[n])*f
MAP={1:(T2[1],E2[1]),2:(T2[3],E2[3]),3:(T2[4],E2[4]),4:(T2[5],E2[5]),5:(T2[6],E2[6]),6:(T2[7],E2[7]),7:(T2[8],E2[8]),8:(T2[9],E2[9]),
 9:(T2[10],mid(10,.45)),10:(mid(10,.45),E2[10]),11:(T2[11],E2[11]),12:(T2[14],E2[15]),13:(T2[16],E2[16]),14:(T2[17],E2[17]),15:(T2[18],E2[18]),
 17:(T2[19],E2[19]),18:(T2[20],E2[20]),19:(T2[21],E2[21]),20:(T2[22],E2[22]),21:(T2[23],E2[23]),22:(T2[24],E2[25]),23:(T2[26],E2[26]),24:(T2[27],E2[27]),
 25:(T2[28],E2[29]),26:(T2[30],E2[30]),27:(T2[31],E2[31]),28:(T2[32],E2[32]),29:(T2[33],E2[33]),30:(T2[34],E2[34]),31:(T2[35],E2[35]),32:(T2[36],E2[36]),
 33:(T2[37],E2[37]),34:(T2[38],E2[38]),35:(T2[39],E2[39]),37:(T2[40],E2[40]),38:(T2[41],E2[41]),40:(T2[42],E2[42]),42:(T2[43],E2[43]),45:(T2[45],E2[45])}
for k in range(1,46):
    a,b=MAP.get(k,(1e6,1e6+1));dai.T[k]=a;dai.E[k]=b
dai.T[16]=dai.E[15]+.5;dai.E[16]=dai.T[16]+1   # không còn cảnh map đoạn 16 cũ
dai.TOTAL=TOT2;dai.CARDS={};dai.HOOKHEAD=False
T,E=dai.T,dai.E
CARDS2={17:'Thứ nhất · Ra tay trước',23:'Thứ hai · Hiểu dòng sông',30:'Thứ ba · Đúng giờ con nước',40:'Sau trận đánh'}
# ---- cảnh mới
def S_tieuich(cv,t):
    a,b=T2[12],E2[13]
    c=cam(*cpath(t,[(a-.4,(960,560,1.0)),(b+.4,(760,600,1.18))]))
    put(cv,c,'court',960,1010,ay=1,s=1.05,o=.75)
    put(cv,c,'fig_quan',660,1030,ay=1,s=2.1,scale_px=1.5)
    tag(cv,c,660,640,'Tiêu Ích',sub='quan Nam Hán',o=fio(t,a+.4,b+.3),dy=0,sz=40)
    # mưa dầm
    if t<E2[12]+.8:
        r=np.random.default_rng(int(t*24)%997);o=.5*fio(t,a+1.0,E2[12]+.8,.6)
        for j in range(70):
            x=r.random()*2200-100;y=r.random()*1080;stroke(cv,c,[(x,y),(x-14,y+46)],1,wid=2,head=False,o=o)
        tag(cv,c,1400,330,'mưa dầm nhiều tuần',o=fio(t,a+1.6,E2[12]+.5),dy=0,sz=34)
        tag(cv,c,1400,400,'đường biển xa và hiểm',o=fio(t,a+2.4,E2[12]+.5),dy=0,sz=34)
    else:
        tag(cv,c,1350,330,'Ngô Quyền là người mưu lược',o=fio(t,T2[13]+.3,b+.3),dy=0,sz=36,col=RED)
        tag(cv,c,1350,400,'quân lớn nên đi chậm',o=fio(t,T2[13]+2.2,b+.3),dy=0,sz=34)
def S_hook2(cv,t):
    dai.S_hook(cv,t)
    for (s,a,b) in [('Vì sao bên yếu hơn lại thắng?',.3,mid(1,.55)),('Vì sao hoàng tử không trở về?',mid(1,.58),E2[1]+.6)]:
        if a-.1<t<b+.6:
            hd=text(s,78,INK if 'yếu' in s else RED,700,glow=6);put_screen(cv,wipe(hd,inn(t,a,.7),0,.3,seed=len(s)),W/2,230,1-inn(t,b,.4))
def S_coloa2(cv,t):
    a,b=T2[40],E2[40]
    c=cam(*cpath(t,[(a-.8,(960,560,1.0)),(b+.6,(960,560,1.1))]))
    put(cv,c,'mist',500,300,s=2.2,o=.7)
    put(cv,c,wipe(A('coloa2'),inn(t,a+1.0,2.0),1,.25,seed=2),960,600,s=.8,scale_px=1.5)
    seal(cv,'s939',300,260,a+.3,t,s=1.0,r=-4)
    tx=text('Ngô Quyền xưng vương',70,INK,700,glow=5);put_screen(cv,wipe(tx,inn(t,a+.8,.9),0,.3,seed=5),W/2+120,170)
    tag(cv,c,960,600,'Cổ Loa',sub='kinh đô',o=inn(t,mid(40,.6),.5),dy=0,sz=56)
def S_king2(cv,t):
    a,b=T2[41],E2[41]
    c=cam(*cpath(t,[(a-.6,(960,560,1.0)),(b+.4,(960,540,1.06))]))
    put(cv,c,'hall',960,980,ay=1,s=.95,o=.85)
    put(cv,c,'fig_tuong',960,820,ay=1,s=1.2,scale_px=1.5)
    for i,s in enumerate(['con gái Dương Đình Nghệ làm hoàng hậu','đặt chức quan, phép tắc triều đình']):
        tx=text(s,44,INK,600,glow=5);put_screen(cv,wipe(tx,inn(t,a+.5+i*2.4,.8),0,.3,seed=i+11),W/2,150+i*70)
THU=[('Ra tay trước','1'),('Hiểu dòng sông','2'),('Đúng giờ con nước','3')]
def S_ba(cv,t):
    a,b=T2[44],E2[44]
    c=cam(960,560,1.0+.02*(t-a))
    dai.river(cv,c,t,PAP,wl=880,under=1,mist=1.3,cliffs=False,reeds=.6)
    ink_wash(cv,.08)
    kw=mid(44,.25)
    for i,(s,k) in enumerate(THU):
        tt=kw+i*(E2[44]-kw)/3.2;x=W/2+(i-1)*560
        put_screen(cv,band(500,170,PAPER,.82,30),x,520,inn(t,tt-.2,.5))
        hd=text(s,60,INK,700,glow=4);put_screen(cv,wipe(hd,inn(t,tt,.6),0,.3,seed=i+3),x,540)
        tx=text(['Thứ nhất','Thứ hai','Thứ ba'][i],34,RED,700);put_screen(cv,tx,x,470,inn(t,tt,.5))
def S_map10(cv,t): dai.S_map(cv,t)
SH=[(0,T2[6]-.4,S_hook2),(T2[6]-.4,T2[7]-.3,dai.S_map),(T2[7]-.3,T2[8]-.3,dai.S_hall),(T2[8]-.3,T2[9]-.3,dai.S_931),(T2[9]-.3,T2[10]-.3,dai.S_aichau),
 (T2[10]-.3,mid(10,.45),dai.S_map),(mid(10,.45),T2[11]-.3,dai.S_porters),(T2[11]-.3,T2[12]-.3,dai.S_court),(T2[12]-.3,T2[14]-.3,S_tieuich),
 (T2[14]-.3,T2[16]-.3,dai.S_map),(T2[16]-.3,T2[17]-1.6,dai.S_harbor),(T2[17]-1.6,T2[18]-.3,dai.S_citadel),(T2[18]-.3,T2[19]-.3,dai.S_sea),
 (T2[19]-.3,T2[22]-.3,dai.S_council),(T2[22]-.3,T2[23]-1.0,dai.S_q),(T2[23]-1.0,T2[24]-.3,dai.S_mapBD),(T2[24]-.3,T2[30]-.6,dai.S_cross),
 (T2[30]-.6,T2[39]-.3,dai.S_battle),(T2[39]-.3,T2[40]-.6,dai.S_retreat),(T2[40]-.6,T2[41]-.3,S_coloa2),(T2[41]-.3,T2[42]-.3,S_king2),
 (T2[42]-.3,T2[44]-.3,dai.S_line),(T2[44]-.3,T2[45]-.3,S_ba),(T2[45]-.3,TOT2+1,dai.S_end)]
dai.SHOTS=SH
def frame(t):
    act=[s for s in SH if s[0]-.35<=t<s[1]+.35]
    def one(fn):
        cv=PAP.copy();fn(cv,t);return cv
    if len(act)==1: cv=one(act[0][2])
    else:
        a,b=act[0],act[1];u=cl((t-(b[0]-.35))/.7)
        m=np.clip((u*1.7-.35-dai.XM*.35-dai.NM*.35)/.3,0,1)[...,None];cv=one(a[2])*(1-m)+one(b[2])*m
    if T2[5]<t<T2[6]+.5: dai.S_title(cv,t,T2[6]-3.5)
    for n,s in CARDS2.items(): card(cv,t,T2[n]-2.2,s,PAP)
    for n in TX2:
        if T2[n]-.25<t<E2[n]+.35: caption(cv,TX2[n],inn(t,T2[n]-.25,.25)*(1-inn(t,E2[n]+.1,.25)),False)
    if dai.LOGO is None: dai.frame(0)
    blend(cv,dai.LOGO,W-44-130,34,.8)
    return cv
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='soi':
        for x in sys.argv[2:]:
            if x[0]=='t': tt=float(x[1:])
            elif '+' in x: tt=T2[int(x.split('+')[0])]+float(x.split('+')[1])
            else: tt=T2[int(x)]+1.5
            Image.fromarray(to8(frame(tt))).save(f'/tmp/gen/bd/out/s_{x}.jpg',quality=85)
        print('TOTAL',round(TOT2,1))
    else:
        out,i0,i1,fps=sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
        ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        for i in range(i0,i1): ff.stdin.write(to8(frame(i/fps)).tobytes())
        ff.stdin.close();ff.wait()
