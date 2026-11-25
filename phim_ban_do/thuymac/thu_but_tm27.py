# Thử kiểu tranh bút lông (cách 1, chủ kênh 25/11): Thoát Hoan dẫn quân rút qua ải Nội Bàng.
# Nền vẽ bằng nét bút khô sinh bằng mã (không dùng AI): núi mực đậm quệt chéo, đồi xa loang, đường núi uốn khúc;
# đoàn quân đi theo chiều sâu (gần to, xa nhỏ thành nét chấm), tướng cưỡi ngựa nhìn từ phía sau ở tiền cảnh.
import sys,math,numpy as np,cv2
sys.path.insert(0,'/tmp/gen/bd')
from engine import *
from khung_dung import cam,PAP
import rig
for _k in ['thn6','m7','m8','m9']: rig.PRE[_k]='t26n_r_'
W,H=1920,1080;FPS=24;DUR=10.0
rg=np.random.default_rng(27)
def premul(alpha,col=INK):
    a=np.clip(alpha,0,1).astype(np.float32);o=np.zeros(a.shape+(4,),np.float32);o[...,:3]=a[...,None]*col;o[...,3]=a;return o
def noise(h,w,sc,seed):
    r=np.random.default_rng(seed).random((max(2,h//sc),max(2,w//sc))).astype(np.float32)
    return cv2.resize(r,(w,h),interpolation=cv2.INTER_CUBIC)
def stroke(L,pts,w0,w1,ink=.9,dry=.5,seed=0,n=None):
    """nét bút lông: dải rộng gồm nhiều sợi lông liền nét, đậm nhạt khác nhau; cuối nét mực cạn thì sợi đứt, tạo vệt bút khô"""
    r=np.random.default_rng(seed);pts=np.float32(pts)
    d=np.r_[0,np.cumsum(np.hypot(*np.diff(pts,axis=0).T))];m=max(8,int(d[-1]/5))
    u=np.linspace(0,d[-1],m);P=np.c_[np.interp(u,d,pts[:,0]),np.interp(u,d,pts[:,1])]
    if len(pts)>2: P=cv2.GaussianBlur(P.reshape(-1,1,2),(1,9),0).reshape(-1,2)
    T=np.gradient(P,axis=0);T/=np.hypot(*T.T)[:,None]+1e-6;N=np.c_[-T[:,1],T[:,0]]
    W=max(w0,w1);n=n or max(10,int(W/2.2));th=max(1,int(round(W/n*1.7)))
    for j in range(n):
        o=(j/(n-1)-.5)
        wv=np.linspace(w0,w1,m)*(1+.12*np.sin(np.linspace(0,5,m)+j*.3))
        Q=P+N*(o*wv)[:,None]+r.normal(0,.5,(m,2))
        ink_j=ink*(.45+.55*r.random())
        d0=r.uniform(.45,.95)-abs(o)*.5   # sợi ở mép cạn mực sớm hơn
        st=r.random()*.06*(abs(o)>.3)
        for k in range(m-1):
            uu=k/(m-1)
            if uu<st: continue
            if uu>d0 and r.random()<dry*min(1,(uu-d0)*4): continue
            cv2.line(L,(int(Q[k,0]),int(Q[k,1])),(int(Q[k+1,0]),int(Q[k+1,1])),float(ink_j),th,cv2.LINE_AA)
    return L
def fbm(h,w,seed,base=200,oct=5):
    o=np.zeros((h,w),np.float32);amp=1;tot=0
    for k in range(oct):
        o+=amp*noise(h,w,max(2,base>>k),seed+k);tot+=amp;amp*=.55
    return o/tot
def streak(h,w,ang,ln,seed):
    """vân bút: nhiễu bị kéo dài theo hướng nét bút"""
    n=np.random.default_rng(seed).random((h,w)).astype(np.float32)
    k=np.zeros((ln,ln),np.float32);c=ln//2
    cv2.line(k,(int(c-math.cos(ang)*c),int(c-math.sin(ang)*c)),(int(c+math.cos(ang)*c),int(c+math.sin(ang)*c)),1,1);k/=k.sum()
    v=cv2.filter2D(n,-1,k);v=(v-v.mean())/(v.std()+1e-6);return v
def vung(h,w,cx,cy,rx,ry,ang):
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32);ca,sa=math.cos(ang),math.sin(ang)
    X=(xx-cx)*ca+(yy-cy)*sa;Y=-(xx-cx)*sa+(yy-cy)*ca;return 1-np.sqrt((X/rx)**2+(Y/ry)**2)
def lop_nui(w,h):
    """khối núi mực kiểu tranh: hình loang theo nhiễu, mép rách; vân bút khô kéo chéo; phần dưới có vệt dọc như vách đá"""
    ang=-.32
    reg=np.maximum(vung(h,w,1720,440,760,170,ang),vung(h,w,1980,620,330,260,.2)*.9)
    f=fbm(h,w,11,260)
    m=reg+ (f-.5)*.9
    a=np.clip((m-.02)*5,0,1)
    st=streak(h,w,ang,121,5);st2=streak(h,w,1.45,151,6)
    lower=np.clip((np.mgrid[0:h,0:w][0]-520)/260,0,1).astype(np.float32)
    s=st*(1-lower)+st2*lower
    core=np.clip((m-.25)*3,0,1)
    a=a*np.clip(.62+.38*s,0,1)*(1-core)+core*np.clip(.9+.1*s,0,1)
    edge=np.clip(1-a*1.6,0,1)*(a>0)
    a=np.where((s<-.55)&(np.clip(m,0,1)<.35),a*.15,a)          # vệt trắng bút khô ở mép
    a=np.clip(a*(.85+.3*fbm(h,w,21,40,3)),0,1)
    R=np.random.default_rng(3)
    for i in range(70):
        x,y=int(1000+R.random()*1350),int(200+R.random()*850)
        if reg[min(h-1,y),min(w-1,x)]>-.4: cv2.circle(a,(x,y),int(1+R.random()*4),float(.35+R.random()*.5),-1,cv2.LINE_AA)
    a=cv2.GaussianBlur(a,(0,0),1.1)
    return premul(a*.96)
def lop_xa(w,h):
    L=np.zeros((h,w),np.float32)
    for k,(y,a) in enumerate([(330,.34),(390,.24),(290,.16)]):
        xs=np.arange(w);yy=y+40*np.sin(xs/260+k)+25*np.sin(xs/97+2*k)+18*noise(1,w,60,k+9)[0]*3
        for x in range(0,w,2): L[int(yy[x]):int(yy[x])+90+k*30,x:x+2]=np.maximum(L[int(yy[x]):int(yy[x])+90+k*30,x:x+2],a)
    L=cv2.GaussianBlur(L,(0,0),9)*(.7+.5*noise(h,w,80,4))
    return premul(np.clip(L,0,1))
DUONG=[(1010,1250),(900,1020),(720,880),(520,770),(430,650),(560,545),(860,480),(1180,430),(1500,380),(1780,345)]
def duong_pt(u):
    P=np.float32(DUONG);d=np.r_[0,np.cumsum(np.hypot(*np.diff(P,axis=0).T))];s=u*d[-1]
    x=np.interp(s,d,P[:,0]);y=np.interp(s,d,P[:,1]);s2=min(d[-1],s+5);x2=np.interp(s2,d,P[:,0]);y2=np.interp(s2,d,P[:,1])
    return x,y,x2-x
def lop_duong(w,h):
    L=np.zeros((h,w),np.float32)
    for side in (-1,1):
        pts=[];
        for u in np.linspace(0,1,40):
            x,y,_=duong_pt(u);wd=lerp(230,8,u**.6);pts.append((x+side*wd*.5,y+ (8 if side>0 else 0)))
        stroke(L,pts,22,3,.55,.6,seed=300+side)
    st=streak(h,w,-.08,151,41);f=fbm(h,w,42,160)
    for cx,cy,rx,ry,al in [(300,1180,520,40,.35),(1500,1230,700,45,.3),(700,1290,600,35,.25),(2000,1120,400,30,.2)]:
        r_=np.clip(vung(h,w,cx,cy,rx,ry,-.05)*2+(f-.5)*.8,0,1)
        L=np.maximum(L,r_*np.clip(.5+.5*st,0,1)*al)
    return premul(np.clip(cv2.GaussianBlur(L,(0,0),.7),0,1))
print('vẽ nền...',file=sys.stderr)
NUI=lop_nui(2400,1300);XA=lop_xa(2400,900);DG=lop_duong(2400,1350)
def linh_xa(cv,c,x,y,s,t,i):
    """người ở rất xa: một nét mực dọc, chấm đầu và cây giáo; càng xa càng nhạt"""
    X,Y=c.p(x,y);z=c.z*s/.1
    hh=max(4.,30*z);bob=abs(math.sin(t*4+i))*1.5*z
    col=tuple(float(v) for v in INK+(PAPER-INK)*min(.6,.15/max(s,.03)*.12))
    cv2.line(cv,(int(X),int(Y-bob)),(int(X+1),int(Y-hh*.75-bob)),col,max(1,int(hh*.22)),cv2.LINE_AA)
    cv2.circle(cv,(int(X+1),int(Y-hh*.88-bob)),max(1,int(hh*.12)),col,-1,cv2.LINE_AA)
    cv2.line(cv,(int(X+hh*.2),int(Y-bob)),(int(X+hh*.35),int(Y-hh*1.5-bob)),col,max(1,int(hh*.05)),cv2.LINE_AA)
def frame(t):
    cv=PAP.copy()
    c=Cam(960+60*inn(t,0,DUR),560-20*inn(t,0,DUR),1.0+.12*inn(t,0,DUR),W,H)
    put(cv,c,XA,1150,300,ay=0,k=.3,scale_px=1,o=.9)
    # sương xa
    for k in range(3):
        put(cv,c,band(1600,90,PAPER,.55,40),600+((t*25+k*700)%2600)-400,420+k*60,k=.5)
    put(cv,c,DG,1200,675,k=1.0,scale_px=1)
    # đoàn quân theo chiều sâu
    n=46
    for i in range(n):
        u=((i/n)+t*.010)%1.0;u=.10+.9*u
        x,y,dx=duong_pt(u);s=.56*(1-u)**1.5+.025
        if s<.11: linh_xa(cv,c,x,y,s,t,i);continue
        P=rig.walk(t*2.0+i*.7,.55);P['mat']=''
        rig.ve23(cv,c,['m7','m8','m9'][i%3],x+(i%2)*6*s,y,s,P,flip=dx<0,vk='giao' if i%3 else 'moc',o=lerp(1,.5,(u-.1)/.6))
    put(cv,c,NUI,1200,650,k=1.0,scale_px=1)
    for k in range(2):
        put(cv,c,band(2000,70,PAPER,.45,40),((t*40+k*900)%2600)-300,700+k*90,k=1.1)
    # tướng cưỡi ngựa nhìn từ sau
    u=inn(t,0,DUR);ph=int(t*2.4)%2
    put(cv,c,'t27n_kysau_b' if ph else 't27n_kysau_a',1380-70*u,1190-50*u+5*math.sin(t*4.8),s=1.55-.15*u,ay=1,k=1.25)
    if t>1.2: put_screen(cv,text('ải Nội Bàng',54,INK,700),260,140,inn(t,1.2,.8)) if 'put_screen' in globals() else None
    return cv
if __name__=='__main__':
    import subprocess
    if sys.argv[1]=='soi':
        from PIL import Image
        ims=[Image.fromarray((np.clip(frame(float(x)),0,1)*255).astype('uint8')).resize((640,360)) for x in sys.argv[2:]]
        s=Image.new('RGB',(640*2,360*((len(ims)+1)//2)))
        for i,im in enumerate(ims): s.paste(im,((i%2)*640,(i//2)*360))
        s.save('/dev/shm/thu.jpg')
    else:
        out=sys.argv[1]
        p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        for f in range(int(DUR*FPS)): p.stdin.write((np.clip(frame(f/FPS),0,1)*255).astype(np.uint8).tobytes())
        p.stdin.close();p.wait()
