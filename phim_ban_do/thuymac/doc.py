# Bản dọc 9:16 (60–80 giây, chưa có giọng)
import sys,subprocess
from canh import *
W,H=1080,1920;V=True
PAP=A('paper_v')[...,:3].copy()
J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/bd1d_full.json'))
TX={i+1:d['text'] for i,d in enumerate(J)}
T={};E={};t=0.3
for n in range(1,len(J)+1):
    T[n]=t;d=len(TX[n].split())/3.1+.55;E[n]=t+d-.35;t+=d
TOTAL=t+3.5
Z=H/1080
def cam(cx,cy,z,sx=0,sy=0): return Cam(cx,cy,z,W,H,sx,sy)
def cpath(t,keys):
    if t<=keys[0][0]: return keys[0][1]
    for (a,ka),(b,kb) in zip(keys,keys[1:]):
        if t<=b: u=ease((t-a)/max(b-a,1e-6));return tuple(lerp(x,y,u) for x,y in zip(ka,kb))
    return keys[-1][1]
HOOK_V='Ai chặn nổi đoàn thuyền này?';END_V='Vì sao quân Nam Hán kéo sang?'
LOW=895
def wl_of(t): return 640+(LOW-640)*inn(t,T[6]+2.6,2.4)
BX0=[840,930,1010,1130,1250,1350]
def lane(i): return [0,1,2,0,1,2][i]
def ctime(i): return E[7]+5 if i==0 else T[7]+.4+[0,.8,.3,1.3,1.0,1.7][i]
def fleet(t):
    wl=wl_of(t);out=[]
    for i in range(6):
        ln=lane(i)
        xs=[(0,1500+i*150),(T[3],1100+i*120),(T[6],1250+i*120),(E[6]-.8,BX0[i])]
        x=xs[0][1]
        for (a,va),(b,vb) in zip(xs,xs[1:]):
            if a<=t<=b: x=lerp(va,vb,ease((t-a)/(b-a)));break
            if t>b: x=vb
        keel=wl+14+ln*45
        if ZONE[0]<x<ZONE[1]: keel=min(keel,LANE_TIP[ln]+12)
        s=.6+ln*.13;r=math.sin(t*1.5+i)*1.4;o=1;y=keel
        tc=ctime(i)
        if t>tc:
            v=t-tc;r+=(-1 if i%2 else 1)*min(78,60*v*v+25*v);y+=110*v*v;o=cl(1-(v-.7)/1.3)
        out.append(dict(x=x,y=y,s=s,r=r,o=o,flip=True,ln=ln))
    out.sort(key=lambda b:b['ln']);return out
def viet(t):
    out=[];wl=wl_of(t)
    if T[5]+3.4<t<T[6]+2:  # khiêu chiến rồi giả thua
        u1=cl((t-T[5]-3.4)/1.6);u2=cl((t-T[5]-5.2)/2.2)
        for i in range(3):
            x=lerp(500-i*80,1050-i*70,ease(u1));fl=False
            if u2>0: x=lerp(1050-i*70,350-i*80,ease(u2));fl=True
            out.append(dict(x=x,y=wl+50+(i%2)*40,s=.62,flip=fl))
    if t>T[7]-.2:
        u=ease((t-T[7]+.2)/2.5)
        for i in range(4):
            out.append(dict(x=lerp(300-i*60,720+i*60,u),y=wl+70+(i%3)*34,s=.65))
            out.append(dict(x=lerp(1700+i*60,1450-i*50,u),y=wl+60+(i%3)*34,s=.65,flip=True))
    return out
def splash(t):
    def f(cv,c):
        for i in range(6):
            tc=ctime(i)
            if tc+.3<t<tc+1.9:
                v=(t-tc-.3)/1.6;put(cv,c,'splash',BX0[i],LANE_TIP[lane(i)]+60,s=.9+1.1*v,o=(1-v)*.95,ay=.95)
    return f
def arrows(t,t0,t1,n=18,seed=1):
    def f(cv,c):
        r=np.random.default_rng(seed)
        for j in range(n):
            ts=t0+r.random()*(t1-t0);fl=1.0+r.random()*.4
            if not ts<t<ts+fl: continue
            u=(t-ts)/fl;side=j%2
            sx,sy=(500+r.random()*200,860) if side==0 else (1500-r.random()*150,860)
            ex,ey=900+r.random()*350,760+r.random()*60
            x=lerp(sx,ex,u);y=lerp(sy,ey,u)-200*u*(1-u)
            ang=math.degrees(math.atan2((ey-sy)-200*(1-2*u),ex-sx));put(cv,c,'arrow',x,y,s=.9,r=ang,o=.9)
    return f
def headline(cv,s,t,a,b,y=330,sz=78,col=INK):
    if t<a-.1 or t>b+.6: return
    hd=text(s,sz,col,700,maxw=940,glow=6);put_screen(cv,wipe(hd,inn(t,a,.8),0,.3,seed=len(s)),W/2,y,1-inn(t,b,.5))
def S_river(cv,t):
    keys=[(0,(1500,560,Z)),(T[2],(1400,560,Z)),(T[2]+2.2,(1250,600,Z*1.25)),(T[3],(1100,600,Z*1.2)),(T[3]+2,(560,620,Z*1.05)),(E[3],(560,620,Z*1.05))]
    if t>T[5]: keys=[(T[5]+2.6,(850,600,Z)),(T[6],(1000,620,Z)),(T[6]+2.4,(1080,700,Z*1.1)),(E[6],(1080,720,Z*1.1)),(T[7],(1000,700,Z)),(E[7],(1050,720,Z*1.05))]
    cx,cy,z=cpath(t,keys);sh=6*math.sin(t*37)*(1-cl((t-T[7])/(E[7]-T[7]))) if T[7]<t<E[7] else 0
    c=cam(cx,cy,z,sh,sh*.6)
    vb=[dict(x=380+i*90,y=740+i*30,s=.6,o=inn(t,T[3]+.8,1.2)) for i in range(3)] if t<T[4] else viet(t)
    river(cv,c,t,PAP,sun=.8*(t<T[4]),birds=1*(t<T[4]),wl=wl_of(t),boats=fleet(t),viet=vb,under=.06*inn(t,T[6],1.5) if t>T[5] else 0,clx=-330,cr=t>T[5],
          fx=[splash(t),arrows(t,T[7],E[7]-1)],dark=.25*inn(t,T[3]+3,1.5)*(t<T[4]))
    if t<4.4: headline(cv,HOOK_V,t,.3,3.8)
    if t<T[4]: seal(cv,'sgiao',W/2,470,T[2]+2.0,t,s=1.15,o=1-inn(t,T[3]+1.0,.5))
    if T[5]<t: 
        if T[6]+1.5<t<E[7]:
            o=fio(t,T[6]+1.5,E[7],.5);gx,gy=W-110,700
            put_screen(cv,A('gauge'),gx,gy,o*.9,s=.45)
            yy=gy-140+280*(wl_of(t)-640)/(LOW-640)
            stroke(cv,Cam(W/2,H/2,1,W,H),[(gx-70,yy),(gx-24,yy)],1,wid=5,col=RED,o=o)
            put_screen(cv,text('thủy triều',30,INK,700,glow=3),gx,gy+175,o)
        headline(cv,'Thủy triều rút xuống',t,T[6]+2.8,E[6],y=330,col=RED)
        seal(cv,'sgiao',W/2,470,E[7]-2.6,t,s=1.15,fall=E[7]-1.0)
_BX=[330,425,520,685,850,1015,1180,1275,1370];_BY=[230,290,318,336,340,336,330,295,230]
def bedy(x): return 460+float(np.interp(x-110,_BX,_BY))
def S_cross(cv,t):
    c=cam(*cpath(t,[(T[4]-.5,(960,640,.72)),(E[5],(960,640,.76))]))
    hi,lo=430,640
    wl=lerp(lo,hi,inn(t,T[5]+.1,2.0))
    y0=int(c.p(0,wl)[1]);cv[y0:]=cv[y0:]*(1-.18)+INK*.18
    for i in range(2): put(cv,c,'wave',960-((t*20+i*70)%200),wl+i*16,o=.7-.3*i)
    put(cv,c,'riverbed',960,980,ay=1,s=1)
    for i,xx in enumerate(range(480,1460,44)):
        by=bedy(xx)+30;td=T[4]+1.0+i*.11
        if t<td-.5: continue
        u=eo((t-td+.5)/.5);top=by-272;y=lerp(top-300,top,u)
        im=rowclip(A('stake'),(wl-y)*1.5/.85,below=.22,soft=4) if wl>y else A('stake')
        put(cv,c,im,xx+(i%2)*6,y,s=.85,ax=.5,ay=0,scale_px=1.5)
    headline(cv,'Cọc vạt nhọn, bịt sắt',t,T[4]+1.6,T[5]+.6,y=420)
    headline(cv,'Thủy triều lên, nước che kín bãi cọc',t,T[5]+.8,E[5]+.5,y=420,sz=64)
    if t>T[5]+1.4:
        put(cv,c,Af('bigboat2'),lerp(1350,1000,cl((t-T[5]-1.4)/2.5)),wl+12,s=.8,o=inn(t,T[5]+1.4,.5),ay=.9,r=math.sin(t*1.6),scale_px=1.5)
def S_end8(cv,t):
    c=cam(960,560,.8)
    put(cv,c,'far',960,760,ay=1,k=.4,o=.6);put(cv,c,'mist',960,700,s=3,o=.9)
    seal(cv,'s939',W/2,420,T[8]+.3,t,s=1.2,r=-4)
    headline(cv,'Ngô Quyền xưng vương',t,T[8]+.8,E[8]+.3,y=620,sz=72)
    put(cv,c,wipe(A('coloa2'),inn(t,T[8]+1.4,1.8),1,.25,seed=2),960,700,s=.62,scale_px=1.5)
    if t>T[8]+2.5: put_screen(cv,text('Cổ Loa',60,INK,700,glow=4),W/2,1130,inn(t,T[8]+2.6,.5))
def S_end9(cv,t):
    c=cam(960,560,.8+.01*(t-T[9]))
    put(cv,c,'far',960,760,ay=1,k=.4,o=.5);put(cv,c,'mist',960,700,s=3,o=.9)
    headline(cv,END_V,t,T[9]+.3,TOTAL,y=470,sz=70)
    seal(cv,'stitle',W/2,860,T[9]+1.4,t,s=1.0,r=3)
    hd=text('Xem bản đầy đủ',84,RED,700,glow=6);put_screen(cv,wipe(hd,inn(t,T[9]+3.2,.8),0,.3,seed=4),W/2,1180)
    put_screen(cv,text('trên kênh Người Gác Sử',50,INK,600,glow=4),W/2,1285,inn(t,T[9]+3.8,.6))
SHOTS=[(0,T[4]-.3,S_river),(T[4]-.3,T[5]+3.2,S_cross),(T[5]+3.2,T[8]-.3,S_river),(T[8]-.3,T[9]-.3,S_end8),(T[9]-.3,TOTAL+1,S_end9)]
_r=np.random.default_rng(2);NM=cv2.resize(_r.random((10,6)).astype(np.float32),(W,H),interpolation=cv2.INTER_CUBIC)
NM=(NM-NM.min())/(NM.max()-NM.min());XM=np.linspace(0,1,H,dtype=np.float32)[:,None]*np.ones((1,W),np.float32)
LOGO=None
def frame(t):
    global LOGO
    act=[s for s in SHOTS if s[0]-.35<=t<s[1]+.35]
    def one(fn):
        cv=PAP.copy();fn(cv,t);return cv
    if len(act)==1: cv=one(act[0][2])
    else:
        a,b=act[0],act[1];u=cl((t-(b[0]-.35))/.7)
        m=np.clip((u*1.7-.35-XM*.35-NM*.35)/.3,0,1)[...,None]
        cv=one(a[2])*(1-m)+one(b[2])*m
    for n in TX:
        if T[n]-.3<t<E[n]+.5: caption(cv,TX[n],inn(t,T[n]-.25,.25)*(1-inn(t,E[n]+.15,.3)),V)
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
        print('TOTAL',round(TOTAL,1),{k:round(v,1) for k,v in T.items()})
    else:
        out,i0,i1,fps=sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
        ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        for i in range(i0,i1): ff.stdin.write(to8(frame(i/fps)).tobytes())
        ff.stdin.close();ff.wait()
