# Thử nét cọ thật: mỗi hình là các nét cọ (đầu đậm, cuối lướt khô, mực loang) chạy ra theo thời gian. Chỉ code, không dùng hình dựng sẵn.
import numpy as np,cv2,sys,subprocess,math
W,H,FPS=960,540,24
rg=np.random.default_rng(7)
def fbm(h,w,seed,octs=4):
    r=np.random.default_rng(seed);o=np.zeros((h,w),np.float32);a=1;tot=0
    for k in range(octs):
        s=max(2,64>>k);n=r.random((max(2,h//s),max(2,w//s))).astype(np.float32)
        o+=a*cv2.resize(n,(w,h),interpolation=cv2.INTER_CUBIC);tot+=a;a*=.5
    return o/tot
TEX=cv2.resize(np.random.default_rng(3).random((H//2,W//2)).astype(np.float32),(W,H),interpolation=cv2.INTER_CUBIC)
GR=cv2.GaussianBlur(np.random.default_rng(4).random((H,W)).astype(np.float32),(0,0),.8)
def giay():
    n=fbm(H,W,3,5);base=np.array([.93,.895,.81],np.float32)
    g=base*(0.94+0.09*n[...,None]);yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
    v=((xx-W/2)/(W*.75))**2+((yy-H/2)/(H*.8))**2;return np.clip(g*(1-.16*v[...,None]),0,1)
def smooth(p,n=60,jit=0,seed=0):
    p=np.array(p,np.float32)
    if jit: p=p+np.random.default_rng(seed).normal(0,jit,p.shape)
    if len(p)<3: t=np.linspace(0,1,n);return p[0]+(p[-1]-p[0])*t[:,None]
    t=np.linspace(0,1,len(p));tt=np.linspace(0,1,n)
    return np.stack([np.interp(tt,t,cv2.GaussianBlur(p[:,0:1],(1,3),0)[:,0] if False else p[:,0]) if False else np.interp(tt,t,p[:,0]),np.interp(tt,t,p[:,1])],1)
def catmull(p,n=80):
    p=np.array(p,np.float32);p=np.vstack([p[0],p,p[-1]]);out=[]
    for i in range(1,len(p)-2):
        for u in np.linspace(0,1,max(4,n//(len(p)-3)),endpoint=False):
            a,b,c,d=p[i-1],p[i],p[i+1],p[i+2]
            out.append(.5*((2*b)+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u**3))
    out.append(p[-2]);return np.array(out,np.float32)
class S:  # một nét cọ
    def __init__(s,pts,w0,w1=None,dens=1.,col=0,t0=0,t1=1,dry=.5,wet=1.,seed=0,belly=1.):
        s.pts=catmull(pts,max(40,int(sum(np.hypot(*(np.diff(np.array(pts),axis=0)).T))*1.2)));n=len(s.pts)
        w1=w0*.3 if w1 is None else w1;u=np.linspace(0,1,n)
        s.w=(w0+(w1-w0)*u)*(1+.35*belly*np.sin(np.pi*u))*(1+.15*np.sin(u*9+seed))
        s.w=np.maximum(s.w,.7);s.dens=dens;s.col=col;s.t0,s.t1=t0,t1;s.dry=dry;s.wet=wet;s.k=0;s.n=n;s.seed=seed
INK=np.zeros((2,H,W),np.float32);WASH=np.zeros((H,W),np.float32)
def stamp(L,x,y,r,v,soft=.6):
    x0,x1,y0,y1=int(x-r-1),int(x+r+2),int(y-r-1),int(y+r+2)
    if x1<=0 or y1<=0 or x0>=W or y0>=H: return
    x0c,y0c,x1c,y1c=max(x0,0),max(y0,0),min(x1,W),min(y1,H)
    yy,xx=np.mgrid[y0c:y1c,x0c:x1c];d=np.hypot(xx-x,yy-y)/max(r,.5)
    m=np.clip((1-d)/soft,0,1)*v;R=L[y0c:y1c,x0c:x1c];np.maximum(R,m,out=R)
def advance(s,p):
    kk=int(np.clip(p,0,1)*s.n)
    for i in range(s.k,kk):
        u=i/s.n;x,y=s.pts[i];r=max(.9,s.w[i]/2)
        tail=1-s.dry*smooth_step((u-.55)/.45)   # cuối nét lướt khô
        head=.78+.22*min(1,u*6)
        tx=TEX[int(np.clip(y,0,H-1)),int(np.clip(x,0,W-1))];gr=GR[int(np.clip(y,0,H-1)),int(np.clip(x,0,W-1))]
        v=s.dens*head*np.clip(tail*(.85+.4*tx)-s.dry*.45*(u>.6)*gr,0,1)
        stamp(INK[s.col],x,y,r,v)
        if s.wet>0 and i%2==0: stamp_w(x,y,r*2.4+2,.16*s.wet*s.dens)
    s.k=max(s.k,kk)
def smooth_step(x): x=min(max(x,0),1);return x*x*(3-2*x)
def stamp_w(x,y,r,v):
    stamp(WASH[None][0:1][0] if False else WASH_L,x,y,r,v,1.0)
WASH_L=WASH
def ease(x): x=min(max(x,0),1);return 2*x*x if x<.5 else 1-(-2*x+2)**2/2
# ---- hình vẽ bằng nét
def nguoi(x,y,h,t0,d,lean=0,hat=0,spear=False,arm=0,seed=0):
    L=[];r=np.random.default_rng(seed);j=lambda a:a+r.normal(0,h*.015)
    hd=h*.085;sh=y-h*.78;wb=y-h*.40
    L.append(S([(x+lean*.2,sh-hd*1.2),(x+lean*.2+j(0),sh-hd*.2)],hd*2.0,hd*1.8,1,0,t0,t0+d*.12,dry=.1,belly=.4,seed=seed))
    if hat==1: L.append(S([(x-hd*1.9+lean*.2,sh-hd*1.3),(x+lean*.2,sh-hd*3.0),(x+hd*1.9+lean*.2,sh-hd*1.3)],hd*.9,hd*.7,1,0,t0+d*.1,t0+d*.2,dry=.2,belly=.2,seed=seed))
    if hat==2: L.append(S([(x-hd*1.5+lean*.2,sh-hd*1.9),(x+hd*1.5+lean*.2,sh-hd*1.9)],hd*1.2,hd*.8,1,0,t0+d*.1,t0+d*.2,dry=.2,belly=.2,seed=seed))
    L.append(S([(x+lean*.2,sh),(x+j(0)+lean*.5,sh+h*.18),(x+j(0)+lean,wb),(x+lean*.4+j(0),y-h*.12)],h*.15,h*.20,1,0,t0+d*.15,t0+d*.45,dry=.25,seed=seed+1))
    L.append(S([(x+lean*.5,wb),(x-h*.06+lean*.2,y-h*.1),(x-h*.07,y)],h*.06,h*.04,1,0,t0+d*.45,t0+d*.6,dry=.2,belly=.3,seed=seed+2))
    L.append(S([(x+lean*.5,wb),(x+h*.07+lean*.3,y-h*.1),(x+h*.08+lean*.1,y)],h*.06,h*.04,1,0,t0+d*.5,t0+d*.65,dry=.2,belly=.3,seed=seed+3))
    if spear:
        L.append(S([(x+h*.16,sh+h*.18),(x+h*.2,sh+h*.02),(x+h*.2+h*.25,y-h*1.05)],h*.04,h*.03,1,0,t0+d*.62,t0+d*.9,dry=.15,belly=0,seed=seed+4))
        L.append(S([(x+h*.2+h*.25,y-h*1.05),(x+h*.2+h*.27,y-h*1.2)],h*.06,h*.01,1,0,t0+d*.9,t0+d,dry=0,belly=0,seed=seed+5))
    if arm:
        L.append(S([(x+lean*.3,sh+h*.07),(x+arm*h*.18,sh+h*.0),(x+arm*h*.38,sh-h*.02)],h*.07,h*.045,1,0,t0+d*.6,t0+d*.85,dry=.3,belly=.2,seed=seed+6))
    return L
def thuyen(x,y,w,t0,d,col=0,seed=0):
    L=[S([(x-w*.5,y-w*.05),(x-w*.3,y+w*.07),(x+w*.3,y+w*.07),(x+w*.52,y-w*.07)],w*.05,w*.025,.95,col,t0,t0+d*.4,dry=.3,seed=seed)]
    L.append(S([(x-w*.4,y+w*.0),(x-w*.2,y+w*.045),(x+w*.25,y+w*.045)],w*.035,w*.02,.9,col,t0+d*.3,t0+d*.5,dry=.4,seed=seed+1))
    L.append(S([(x-w*.18,y-w*.02),(x-w*.18,y-w*.2),(x+w*.12,y-w*.2),(x+w*.12,y-w*.02)],w*.03,w*.03,.95,col,t0+d*.45,t0+d*.75,dry=.3,belly=.2,seed=seed+2))
    L.append(S([(x-w*.24,y-w*.2),(x-w*.03,y-w*.3),(x+w*.18,y-w*.2)],w*.04,w*.03,.95,col,t0+d*.7,t0+d*.9,dry=.2,belly=.3,seed=seed+3))
    L.append(S([(x+w*.3,y-w*.03),(x+w*.3,y-w*.32)],w*.012,w*.01,.9,col,t0+d*.8,t0+d,dry=.1,belly=0,seed=seed+4))
    L.append(S([(x+w*.31,y-w*.3),(x+w*.46,y-w*.15),(x+w*.31,y-w*.03)],w*.02,w*.015,.5,col,t0+d*.85,t0+d,dry=.5,belly=0,seed=seed+5))
    return L
def nui(pts,t0,d,dens=.5,w=30,seed=0): return S(pts,w,w*.4,dens,0,t0,t0+d,dry=.8,wet=1.0,seed=seed)
def thong(x,y,h,t0,d,seed=0):
    L=[S([(x,y),(x+4,y-h*.5),(x,y-h)],h*.05,h*.03,.9,0,t0,t0+d*.4,dry=.3,belly=.2,seed=seed)]
    for i,f in enumerate((.35,.55,.75,.95)):
        ww=h*(.32-.06*i);yy=y-h*f
        L.append(S([(x-ww,yy+h*.05),(x,yy-h*.03),(x+ww,yy+h*.05)],h*.06,h*.035,.85,0,t0+d*(.3+i*.17),t0+d*(.45+i*.17),dry=.6,belly=.1,seed=seed+i))
    return L
def can(x,y,h,t0,d,seed=0):
    return [S([(x+(i-1)*7,y),(x+(i-1)*11+3,y-h*(.7+.15*i))],2,1,.55,0,t0+d*i*.25,t0+d*(.4+i*.25),dry=.7,belly=0,seed=seed+i) for i in range(3)]
def canh():
    L=[]
    L.append(nui([(0,300),(150,230),(300,285),(420,255),(560,300)],0.2,3,.40,38,1))
    L.append(nui([(520,310),(720,215),(930,290),(960,300)],0.8,3,.32,34,2))
    L.append(nui([(0,335),(200,310),(420,330),(700,305),(960,330)],1.4,3,.30,26,3))
    for i,(x,y,h) in enumerate([(70,340,95),(150,345,70),(790,338,100),(880,343,75),(330,342,50)]): L+=thong(x,y,h,2.0+i*.35,1.3,seed=i*3)
    L.append(S([(0,372),(240,366),(520,374),(800,367),(960,372)],4,2,.45,0,1.5,6,dry=.9,wet=.8,seed=40))
    for i,x in enumerate((120,240,640,860)): L+=can(x,372,44,3.5+i*.4,1.2,seed=60+i)
    L.append(S([(0,400),(300,395),(560,403),(960,398)],3,1.5,.3,0,4.5,8,dry=.9,wet=.6,seed=41))
    # A: một người chạy
    L+=nguoi(420,472,100,5.0,2.6,lean=-18,hat=0,arm=1,seed=11)
    for i,x in enumerate((640,740,830)): L+=thuyen(x,395,95,6+i*.6,2.2,seed=20+i)
    # B: hàng lính
    for i,(x,h,hat) in enumerate([(120,118,1),(215,126,2),(310,120,1),(405,130,0),(500,122,1)]): L+=nguoi(x,505,h,10+i*.7,2.2,hat=hat,spear=True,seed=100+i*7)
    # C: thuyền vua màu xanh
    L+=thuyen(760,400,300,15.5,5,col=1,seed=50)
    return L
STR=canh()
def render(out,secs=24,audio=None):
    paper=giay();p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-']+(['-i',audio,'-map','0:v','-map','1:a','-c:a','aac','-shortest'] if audio else [])+['-c:v','libx264','-pix_fmt','yuv420p','-crf','20',out],stdin=subprocess.PIPE)
    teal=np.array([.20,.52,.45],np.float32)
    for f in range(secs*FPS):
        t=f/FPS
        for s in STR:
            if t>s.t0: advance(s,(t-s.t0)/max(.01,s.t1-s.t0))
        ink=np.clip(INK[0],0,1);gr=INK[1]
        wash=cv2.GaussianBlur(np.clip(WASH_L,0,1),(0,0),5)
        a=np.clip(wash*.9*(.7+.6*TEX),0,.7)[...,None]
        im=paper*(1-a*np.array([.72,.72,.68],np.float32))
        im=im*(1-ink[...,None]*np.array([.93,.94,.95],np.float32))
        im=im*(1-gr[...,None])+gr[...,None]*teal*(.95-.2*TEX[...,None])
        p.stdin.write((np.clip(im,0,1)*255).astype(np.uint8).tobytes())
    p.stdin.close();p.wait()
if __name__=='__main__': render(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 24,sys.argv[3] if len(sys.argv)>3 else None)
