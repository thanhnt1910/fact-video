# Bóng mực thủy mặc vẽ bằng code: mỗi người/thuyền là một khối bóng liền, mép loang như mực thấm giấy, mực lan ra dần.
import numpy as np,cv2,sys,subprocess
W,H,FPS,SS=960,540,24,3
def fbm(h,w,seed,octs=4):
    r=np.random.default_rng(seed);o=np.zeros((h,w),np.float32);a=1;tot=0
    for k in range(octs):
        s=max(2,64>>k);n=r.random((max(2,h//s),max(2,w//s))).astype(np.float32)
        o+=a*cv2.resize(n,(w,h),interpolation=cv2.INTER_CUBIC);tot+=a;a*=.5
    return o/tot
def giay():
    n=fbm(H,W,3,5);base=np.array([.93,.895,.81],np.float32);g=base*(0.94+0.09*n[...,None])
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32);v=((xx-W/2)/(W*.75))**2+((yy-H/2)/(H*.8))**2
    return np.clip(g*(1-.16*v[...,None]),0,1)
def ss(x): x=np.clip(x,0,1);return x*x*(3-2*x)
def cm(p,n=14):
    p=np.array(p,np.float32);q=np.vstack([p[-1],p,p[0],p[1]]);o=[]
    for i in range(1,len(q)-2):
        for u in np.linspace(0,1,n,endpoint=False):
            a,b,c,d=q[i-1],q[i],q[i+1],q[i+2];o.append(.5*((2*b)+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u**3))
    return np.array(o)
class L:
    """một khối mực: shapes là danh sách ('poly',pts)|('ell',cx,cy,rx,ry)|('line',p,q,w) toạ độ điểm ảnh khung 960x540"""
    def __init__(s,shapes,t0,d,col=0,dens=1.,seed=0,wash=False,dirn=0):
        s.t0,s.d,s.col,s.seed,s.dirn=t0,d,col,seed,dirn
        xs=[];ys=[]
        for sh in shapes:
            if sh[0]=='poly': xs+=list(sh[1][:,0]);ys+=list(sh[1][:,1])
            elif sh[0]=='ell': xs+=[sh[1]-sh[3],sh[1]+sh[3]];ys+=[sh[2]-sh[4],sh[2]+sh[4]]
            else: xs+=[sh[1][0],sh[2][0]];ys+=[sh[1][1],sh[2][1]]
        pad=14;s.x0=max(0,int(min(xs))-pad);s.x1=min(W,int(max(xs))+pad);s.y0=max(0,int(min(ys))-pad);s.y1=min(H,int(max(ys))+pad)
        w,h=s.x1-s.x0,s.y1-s.y0;m=np.zeros((h*SS,w*SS),np.uint8)
        P=lambda p:((np.asarray(p)-[s.x0,s.y0])*SS).astype(np.int32)
        for sh in shapes:
            if sh[0]=='poly': cv2.fillPoly(m,[P(sh[1])],255)
            elif sh[0]=='ell': cv2.ellipse(m,tuple(P((sh[1],sh[2]))),(int(sh[3]*SS),int(sh[4]*SS)),0,0,360,255,-1)
            else: cv2.line(m,tuple(P(sh[1])),tuple(P(sh[2])),255,max(1,int(sh[3]*SS)))
        m=cv2.resize(m,(w,h),interpolation=cv2.INTER_AREA).astype(np.float32)/255
        r=np.random.default_rng(seed);dx=(fbm(h,w,seed+1,3)-.5)*3.2;dy=(fbm(h,w,seed+2,3)-.5)*3.2
        gx,gy=np.meshgrid(np.arange(w,dtype=np.float32),np.arange(h,dtype=np.float32))
        m=cv2.remap(m,gx+dx,gy+dy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
        bl=cv2.GaussianBlur(m,(0,0),1.1);edge=fbm(h,w,seed+3,4)
        core=ss((bl-.28-.32*edge)/.22)
        halo=cv2.GaussianBlur(m,(0,0),3.2)*.20*(.5+edge)   # mực loang quanh mép
        dark=(.80+.20*fbm(h,w,seed+4,3))
        s.mask=np.clip(core*dark*dens+halo*(1-core),0,1)
        if wash: s.mask=cv2.GaussianBlur(m,(0,0),wash)*dens*(.7+.5*fbm(h,w,seed+5,3))
        kx=(gx/max(1,w-1)) if dirn==0 else (gy/max(1,h-1))
        s.key=np.clip(.75*kx+.25*fbm(h,w,seed+6,3),0,1.2)
    def get(s,t):
        p=(t-s.t0)/s.d
        if p<=0: return None
        a=ss((p*1.35-s.key)/.22) if p<1 else 1.
        return s.mask*a
def close(pts,n=10): return ('poly',cm(pts,n))
# ---- hình mẫu
def nguoi(x,y,h,t0,d,hat=0,lean=0,spear=False,arm=0,seed=0):
    r=np.random.default_rng(seed);f=lambda p:np.array([x+lean*(-p[1])*.5*h+p[0]*h*(1+r.normal(0,.03)),y+p[1]*h])
    body=[(-.09,-.77),(0,-.795),(.09,-.77),(.115,-.5),(.15,-.1),(.0,-.065),(-.15,-.1),(-.115,-.5)]
    sh=[close([f(p) for p in body]),('ell',*f((0,-.865)),.046*h,.052*h),('ell',*f((-.06,-.03)),.045*h,.02*h),('ell',*f((.07,-.03)),.045*h,.02*h)]
    sh[1]=('ell',f((0,-.865))[0],f((0,-.865))[1],.046*h,.052*h);sh[2]=('ell',f((-.06,-.03))[0],f((-.06,-.03))[1],.05*h,.02*h);sh[3]=('ell',f((.07,-.03))[0],f((.07,-.03))[1],.05*h,.02*h)
    if hat==1: sh.append(('poly',np.array([f((-.13,-.885)),f((0,-1.0)),f((.13,-.885)),f((0,-.9))])))
    if hat==2: sh.append(('ell',f((0,-.925))[0],f((0,-.925))[1],.075*h,.02*h)); sh.append(('poly',np.array([f((-.04,-.925)),f((-.045,-.99)),f((.045,-.99)),f((.04,-.925))])))
    if arm: 
        a=f((0,-.74));b=f((arm*.2,-.78));c=f((arm*.38,-.8));sh+= [('line',a,b,.05*h),('line',b,c,.04*h)]
    if spear:
        a=f((.17,-.5));b=f((.2,-1.02));sh.append(('line',a,b,max(1.5,.012*h)));t=f((.205,-1.1))
        sh.append(('poly',np.array([f((.19,-1.02)),t,f((.22,-1.02))])))
    return L(sh,t0,d,seed=seed)
def thuyen(x,y,w,t0,d,col=0,seed=0):
    hull=[(-.5,-.07),(-.3,.05),(.0,.07),(.3,.05),(.52,-.09),(.46,-.01),(.3,.0),(-.3,.0),(-.44,-.01)]
    f=lambda p:np.array([x+p[0]*w,y+p[1]*w])
    sh=[close([f(p) for p in hull]),close([f(p) for p in [(-.14,-.01),(-.14,-.11),(.14,-.11),(.14,-.01)]]),
        ('poly',np.array([f((-.2,-.11)),f((-.1,-.17)),f((.1,-.17)),f((.2,-.11)),f((.14,-.115)),f((-.14,-.115))])),('line',f((.3,-.04)),f((.3,-.42)),max(1.5,.012*w)),
        close([f(p) for p in [(.31,-.4),(.47,-.22),(.31,-.08)]])]
    l=L(sh,t0,d,col=col,seed=seed);return l
def nui(pts,t0,d,dens,seed):
    p=np.array(pts,np.float32);top=cm(p,18);poly=np.vstack([top,[[top[-1][0],420],[top[0][0],420]]])
    return L([('poly',poly)],t0,d,seed=seed,wash=5,dens=dens*1.3)
def thong(x,y,h,t0,d,seed):
    sh=[('line',np.array([x,y]),np.array([x+3,y-h]),max(1.8,h*.035))]
    for i,fr in enumerate((.35,.55,.75,.93)):
        ww=h*(.32-.06*i);yy=y-h*fr;sh.append(close([(x-ww,yy+h*.07),(x,yy-h*.05),(x+ww,yy+h*.07),(x,yy+h*.02)]))
    return L(sh,t0,d,seed=seed,dens=.9)
def can(x,y,h,t0,d,seed): return L([('line',np.array([x+(i-1)*7,y]),np.array([x+(i-1)*11+3,y-h*(.7+.15*i)]),1.6) for i in range(3)],t0,d,seed=seed,dens=.6)
def canh():
    Z=[nui([(0,300),(150,230),(300,285),(420,255),(560,300),(560,340),(0,340)],.2,3,.36,1),nui([(520,310),(720,215),(930,290),(960,300),(960,340),(520,340)],.8,3,.30,2)]
    for i,(x,y,h) in enumerate([(70,345,100),(150,350,72),(790,343,105),(880,348,78),(330,347,52)]): Z.append(thong(x,y,h,2.0+i*.35,1.3,i*3))
    for i,x in enumerate((120,240,640,860)): Z.append(can(x,376,44,3.5+i*.4,1.2,60+i))
    Z.append(L([('poly',np.array([[0,378],[960,376],[960,381],[0,383]]))],1.5,4,seed=40,dens=.35))
    Z.append(nguoi(420,478,112,5.0,2.4,lean=-.22,arm=1,seed=11))
    for i,x in enumerate((640,740,830)): Z.append(thuyen(x,402,100,6+i*.6,2.0,seed=20+i))
    for i,(x,h,hat) in enumerate([(120,128,1),(215,136,2),(310,130,1),(405,140,0),(500,132,1)]): Z.append(nguoi(x,510,h,10+i*.7,2.0,hat=hat,spear=True,seed=100+i*7))
    Z.append(thuyen(760,405,300,15.5,5,col=1,seed=50))
    return Z
def render(out,secs=24,audio=None):
    paper=giay();Z=canh();teal=np.array([.20,.52,.45],np.float32)
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-']+(['-i',audio,'-map','0:v','-map','1:a','-c:a','aac','-shortest'] if audio else [])+['-c:v','libx264','-pix_fmt','yuv420p','-crf','20',out],stdin=subprocess.PIPE)
    for f in range(secs*FPS):
        t=f/FPS;ink=np.zeros((H,W),np.float32);gr=np.zeros((H,W),np.float32)
        for z in Z:
            m=z.get(t)
            if m is None: continue
            T=gr if z.col else ink;R=T[z.y0:z.y1,z.x0:z.x1];np.maximum(R,m,out=R)
        im=paper*(1-ink[...,None]*np.array([.93,.94,.95],np.float32))
        im=im*(1-gr[...,None])+gr[...,None]*teal*(.97-.2*fbm(H,W,9,2)[...,None])
        p.stdin.write((np.clip(im,0,1)*255).astype(np.uint8).tobytes())
    p.stdin.close();p.wait()
if __name__=='__main__': render(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 24,sys.argv[3] if len(sys.argv)>3 else None)
