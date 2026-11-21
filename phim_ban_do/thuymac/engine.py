# Bộ ghép khung hình thủy mặc: tài sản RGBA (vẽ sẵn) + camera + hiệu ứng, xuất thẳng ra ffmpeg
import numpy as np,cv2,math,json,os
from PIL import Image,ImageDraw,ImageFont,ImageFilter
D='/tmp/gen/bd/a/'
INK=np.float32([21,19,15])/255;PAPER=np.float32([236,226,203])/255;RED=np.float32([163,38,28])/255
SC={'paper_h':1,'paper_v':1,'mist':1,'blot':1}
_A={}
def A(name):
    if name not in _A:
        a=np.asarray(Image.open(D+name+'.png').convert('RGBA'),np.float32)/255
        a[...,:3]*=a[...,3:4];_A[name]=a
    return _A[name]
import re as _re
def asc(name): return 3 if _re.match(r't\d+n_',name) else SC.get(name,1.5)  # hình người kiểu mới (tNNn_) xuất ở độ phân giải gấp ba
PTS=json.load(open(D+'map_pts.json'))
cl=lambda x:max(0.,min(1.,x))
def ease(x):
    x=cl(x);return 2*x*x if x<.5 else 1-(-2*x+2)**2/2
def eo(x): x=cl(x);return 1-(1-x)**3
def inn(t,a,d): return ease((t-a)/d) if d>0 else float(t>=a)
def fio(t,a,b,f=.4): return inn(t,a,f)*(1-inn(t,b-f,f))
lerp=lambda a,b,u:a+(b-a)*u
class Cam:
    def __init__(s,cx,cy,z,W,H,sx=0,sy=0): s.cx,s.cy,s.z,s.W,s.H,s.sx,s.sy=cx,cy,z,W,H,sx,sy
    def p(s,x,y): return ((x-s.cx)*s.z+s.W/2+s.sx,(y-s.cy)*s.z+s.H/2+s.sy)
    def par(s,k,ox=0,oy=0):  # camera thị sai: lớp xa trôi chậm hơn
        return Cam(lerp(960,s.cx,k)+ox,lerp(540,s.cy,k)+oy,1+(s.z-1)*k if s.z>=1 else s.z,s.W,s.H,s.sx,s.sy) if False else Cam(960+(s.cx-960)*k+ox,540+(s.cy-540)*k+oy,s.z,s.W,s.H,s.sx,s.sy)
def blend(cv,img,bx,by,o):
    H,W=cv.shape[:2];h,w=img.shape[:2]
    x0,y0=max(0,bx),max(0,by);x1,y1=min(W,bx+w),min(H,by+h)
    if x1<=x0 or y1<=y0 or o<=0.003: return
    s=img[y0-by:y1-by,x0-bx:x1-bx];r=cv[y0:y1,x0:x1]
    a=s[...,3:4]*o;r*=1-a;r+=s[...,:3]*o
def tint(img,col):
    o=img.copy();o[...,:3]=img[...,3:4]*col;return o
def warp(cv,img,M,o=1.0):
    h,w=img.shape[:2];H,W=cv.shape[:2]
    c=np.float32([[0,0,1],[w,0,1],[0,h,1],[w,h,1]])@np.float32(M).T
    bx,by=int(math.floor(max(0,c[:,0].min()))),int(math.floor(max(0,c[:,1].min())))
    ex,ey=int(math.ceil(min(W,c[:,0].max()))),int(math.ceil(min(H,c[:,1].max())))
    if ex-bx<1 or ey-by<1: return
    M2=np.float32(M).copy();M2[0,2]-=bx;M2[1,2]-=by
    out=cv2.warpAffine(img,M2,(ex-bx,ey-by),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
    blend(cv,out,bx,by,o)
def put(cv,cam,img,x,y,s=1.0,r=0.0,o=1.0,ax=.5,ay=.5,k=1.0,scale_px=1.5,screen=False):
    """đặt ảnh: (x,y) tọa độ thế giới của điểm neo; s: tỉ lệ; r: độ xoay; k: hệ số thị sai"""
    if o<=0.003: return
    if isinstance(img,str): scale_px=asc(img);img=A(img)
    h,w=img.shape[:2]
    if screen: z=1.0;X,Y=x,y
    else:
        cm=cam.par(k) if k!=1 else cam;z=cm.z;X,Y=cm.p(x,y)
    f=s*z/scale_px;ca,sa=math.cos(math.radians(r))*f,math.sin(math.radians(r))*f
    axp,ayp=ax*w,ay*h
    M=[[ca,-sa,X-(ca*axp-sa*ayp)],[sa,ca,Y-(sa*axp+ca*ayp)]]
    warp(cv,img,M,o)
_noise={}
def ragged(n,seed):
    if (n,seed) not in _noise:
        rg=np.random.default_rng(seed);v=rg.random(n//8+3).astype(np.float32)
        _noise[(n,seed)]=cv2.resize(v[None,:],(n,1),interpolation=cv2.INTER_CUBIC)[0]
    return _noise[(n,seed)]
def wipe(img,u,axis=0,band=.18,seed=1,rev=False):
    if u>=1: return img
    h,w=img.shape[:2]
    if axis==0:
        xn=np.linspace(0,1,w,dtype=np.float32)[None,:];nz=ragged(h,seed)[:,None]
    else:
        xn=np.linspace(0,1,h,dtype=np.float32)[:,None];nz=ragged(w,seed)[None,:]
    if rev: xn=1-xn
    m=np.clip((u*(1+band)-xn-band*nz)/band*1.0,0,1)
    return img*m[...,None]
def rowclip(img,ycut,below=.06,soft=6):
    """giữ phần trên dòng ycut (theo pixel ảnh), phần dưới mờ đi (cọc dưới nước)"""
    h=img.shape[0];yy=np.arange(h,dtype=np.float32)
    dep=np.clip(yy-ycut,0,None)
    m=below*np.exp(-dep/90)+(1-below*np.exp(-dep/90))*np.clip((ycut-yy)/soft,0,1)
    return img*m[:,None,None]
# ---------- chữ
FONT='/tmp/gen/bd/a/Lora-Variable.ttf'
_F={};_T={}
def font(sz,wg=600):
    k=(sz,wg)
    if k not in _F:
        f=ImageFont.truetype(FONT,sz)
        try: f.set_variation_by_axes([wg])
        except Exception: pass
        _F[k]=f
    return _F[k]
def wrap(s,f,maxw):
    words=s.split();lines=[];cur=''
    for wd in words:
        t=(cur+' '+wd).strip()
        if f.getlength(t)<=maxw or not cur: cur=t
        else: lines.append(cur);cur=wd
    if cur: lines.append(cur)
    return lines
def balance(s,f,maxw):
    L=wrap(s,f,maxw)
    if len(L)==2:  # cân hai dòng
        words=s.split();best=None
        for i in range(1,len(words)):
            a,b=' '.join(words[:i]),' '.join(words[i:]);m=max(f.getlength(a),f.getlength(b))
            if m<=maxw and (best is None or m<best[0]): best=(m,[a,b])
        if best: L=best[1]
    return L
def text(s,sz,col=INK,wg=600,maxw=10000,lh=1.28,align='center',rough=True,glow=0):
    k=(s,sz,tuple(np.round(col,3)),wg,maxw,lh,align,rough,glow)
    if k in _T: return _T[k]
    f=font(sz,wg);L=balance(s,f,maxw) if maxw<10000 else s.split('\n')
    W=int(max(f.getlength(x) for x in L))+40+glow*4;Hh=int(sz*lh*len(L)+sz*.6)+20+glow*4
    im=Image.new('L',(W,Hh),0);d=ImageDraw.Draw(im)
    for i,x in enumerate(L):
        lw=f.getlength(x);xx=(W-lw)/2 if align=='center' else 20+glow*2
        d.text((xx,10+glow*2+i*sz*lh),x,font=f,fill=255)
    a=np.asarray(im,np.float32)/255
    if rough:
        rg=np.random.default_rng(len(s));h,w=a.shape
        dx=cv2.GaussianBlur(rg.random((h,w)).astype(np.float32),(0,0),2)-.5;dy=cv2.GaussianBlur(rg.random((h,w)).astype(np.float32),(0,0),2)-.5
        mx,my=np.meshgrid(np.arange(w,dtype=np.float32),np.arange(h,dtype=np.float32))
        a=cv2.remap(a,mx+dx*max(2,sz/22),my+dy*max(2,sz/22),cv2.INTER_LINEAR)
        a=cv2.GaussianBlur(a,(0,0),.6)
    out=np.zeros(a.shape+(4,),np.float32);out[...,3]=a;out[...,:3]=a[...,None]*col
    if glow:
        g=cv2.GaussianBlur(cv2.dilate(a,np.ones((5,5),np.uint8)),(0,0),glow)*.85
        base=np.zeros_like(out);base[...,3]=g;base[...,:3]=g[...,None]*PAPER
        a2=out[...,3:4];out=out+base*(1-a2)
    _T[k]=out;return out
def band(w,h,col=PAPER,a=.8,soft=24):
    k=('band',w,h,a,soft,tuple(col))
    if k not in _T:
        im=np.zeros((h+soft*4,w+soft*4),np.float32);cv2.rectangle(im,(soft*2,soft*2),(soft*2+w,soft*2+h),1,-1)
        im=cv2.GaussianBlur(im,(0,0),soft)*a
        o=np.zeros(im.shape+(4,),np.float32);o[...,3]=im;o[...,:3]=im[...,None]*col;_T[k]=o
    return _T[k]
def put_screen(cv,img,x,y,o=1,ax=.5,ay=.5,s=1.0,r=0.0):
    if s==1 and r==0:
        h,w=img.shape[:2];blend(cv,img,int(round(x-ax*w)),int(round(y-ay*h)),o)
    else: put(cv,None,img,x,y,s=s,r=r,o=o,ax=ax,ay=ay,scale_px=1,screen=True)
def caption(cv,s,o,V):
    if o<=0.01: return
    if V: sz,maxw,y=50,940,1650
    else: sz,maxw,y=44,1480,968
    t=text(s,sz,INK,620,maxw,lh=1.3)
    h,w=t.shape[:2];b=band(w-10,h-20,PAPER,.78,26)
    put_screen(cv,b,cv.shape[1]/2,y,o);put_screen(cv,t,cv.shape[1]/2,y,o)
# ---------- nét cọ: đường đi, mũi tên (tọa độ thế giới)
def stroke(cv,cam,pts,prog=1.0,wid=6,col=INK,o=1.0,dash=0,head=True,seed=3):
    if prog<=0 or o<=0: return
    P=np.float32([cam.p(x,y) for x,y in pts])
    seg=np.linalg.norm(np.diff(P,axis=0),axis=1);L=seg.sum();cut=L*cl(prog);acc=0;Q=[P[0]]
    for i,sl in enumerate(seg):
        if acc+sl>=cut: Q.append(P[i]+(P[i+1]-P[i])*((cut-acc)/max(sl,1e-6)));break
        acc+=sl;Q.append(P[i+1])
    Q=np.float32(Q);H,W=cv.shape[:2]
    x0,y0=np.floor(Q.min(0)-wid*6).astype(int);x1,y1=np.ceil(Q.max(0)+wid*6).astype(int)
    x0,y0=max(0,x0),max(0,y0);x1,y1=min(W,x1),min(H,y1)
    if x1<=x0 or y1<=y0: return
    m=np.zeros((y1-y0,x1-x0),np.uint8);q=((Q-[x0,y0])*16).astype(np.int32)
    w=max(1,int(wid*cam.z**.5))
    if dash:
        d=0;on=True;cs=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))])
        L2=cs[-1];s0=0
        while s0<L2:
            s1=min(L2,s0+dash);
            a=np.interp(s0,cs,np.arange(len(Q)));b=np.interp(s1,cs,np.arange(len(Q)))
            def at(fi):
                i=min(int(fi),len(Q)-2);fr=fi-i;return Q[i]+(Q[i+1]-Q[i])*fr
            pa,pb=(at(a)-[x0,y0])*16,(at(b)-[x0,y0])*16
            cv2.line(m,tuple(pa.astype(int)),tuple(pb.astype(int)),255,w,cv2.LINE_AA,shift=4)
            s0+=dash*1.8
    else:
        cv2.polylines(m,[q],False,255,w,cv2.LINE_AA,shift=4)
    if head and prog>.15 and len(Q)>1:
        e=Q[-1];dvec=Q[-1]-Q[max(0,len(Q)-3)];n=np.linalg.norm(dvec)
        if n>1:
            dvec/=n;pp=np.float32([-dvec[1],dvec[0]]);hl=w*3.4
            tri=np.float32([e+dvec*hl*.5,e-dvec*hl+pp*hl*.6,e-dvec*hl*.6,e-dvec*hl-pp*hl*.6])
            cv2.fillPoly(m,[((tri-[x0,y0])*16).astype(np.int32)],255,cv2.LINE_AA,shift=4)
    a=cv2.GaussianBlur(m.astype(np.float32)/255,(0,0),.8)*o
    r=cv[y0:y1,x0:x1];r*=1-a[...,None];r+=a[...,None]*col
def tag(cv,cam,x,y,s,sub=None,o=1,dy=-34,V=False,col=INK,sz=None):
    """nhãn tên gắn vào điểm trên bản đồ"""
    if o<=0.01: return
    X,Y=cam.p(x,y);sz=sz or (40 if V else 34)
    t=text(s,sz,col,700,glow=3);put_screen(cv,t,X,Y+dy,o,ay=1)
    if sub:
        t2=text(sub,int(sz*.72),INK,500,glow=3);put_screen(cv,t2,X,Y+(14 if dy<0 else dy+sz*.5),o,ay=0)
def dot(cv,cam,x,y,o=1,col=INK,r=9):
    if o<=0.01: return
    X,Y=cam.p(x,y);H,W=cv.shape[:2];R=int(r*2.5)
    x0,y0=int(X)-R,int(Y)-R
    m=np.zeros((2*R,2*R),np.float32);cv2.circle(m,(R,R),r,1,-1,cv2.LINE_AA);cv2.circle(m,(R,R),int(r*1.9),1,3,cv2.LINE_AA)
    img=np.zeros((2*R,2*R,4),np.float32);img[...,3]=m;img[...,:3]=m[...,None]*col
    blend(cv,img,x0,y0,o)
def ink_wash(cv,o,col=INK):
    if o>0.003: cv*= (1-o);cv+=o*col
