"""Hiệu ứng nâng cấp thủy mặc: mực loang động, hạt khói tro, người ghép từ mảnh (bộ xương viết bằng code)."""
import math,numpy as np,cv2
from engine import *
INKC=np.array([.17,.15,.12],np.float32)
_NZ={};_GR={}
def _nz(h,w,seed):
    k=(h,w,seed)
    if k not in _NZ:
        rg=np.random.default_rng(seed);n=rg.standard_normal((2,h//36+3,w//36+3)).astype(np.float32)
        _NZ[k]=np.stack([cv2.resize(n[i],(w,h),interpolation=cv2.INTER_CUBIC) for i in range(2)])
    return _NZ[k]
def mucloang(name,t,amp=2.4,seed=1,bleed=.55,rate=1.5):
    """tranh với nét mực rung nhẹ theo thời gian và quầng mực thấm quanh nét"""
    a=A(name);h,w=a.shape[:2]
    n1,n2=_nz(h,w,seed),_nz(h,w,seed+7)
    ph=t*rate;f1,f2=math.sin(ph),math.cos(ph)
    dx=amp*(n1[0]*f1+n2[0]*f2);dy=amp*(n1[1]*f1+n2[1]*f2)
    if (h,w) not in _GR: _GR[(h,w)]=np.meshgrid(np.arange(w,dtype=np.float32),np.arange(h,dtype=np.float32))
    gx,gy=_GR[(h,w)]
    o=cv2.remap(a,gx+dx,gy+dy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
    if bleed>0:
        al=o[...,3];halo=cv2.GaussianBlur(al,(0,0),5)
        ex=np.clip(halo-al,0,1)*bleed*.35
        o=o+ex[...,None]*np.concatenate([INKC,[1.]]).astype(np.float32)
    return o
def tro(cv,c,t,a,b,pts,n=14,seed=3,o=.55):
    """tro tàn bay lên từ các điểm, lắc theo gió"""
    if not a-.2<t<b+.5: return
    rg=np.random.default_rng(seed)
    for k in range(n):
        x0,y0=pts[k%len(pts)];ph=rg.random();sp=40+rg.random()*50;sw=rg.random()*6.28
        f=((t-a)*.35+ph)%1
        x=x0+rg.uniform(-40,40)+math.sin(t*1.6+sw)*28+f*60;y=y0-f*sp*4.2
        put(cv,c,'blot',x,y,s=.010+.008*rg.random(),o=min(1,o*1.6)*math.sin(math.pi*f)*inn(t,a,.5)*(1-inn(t,b,.5)))
def suong(cv,c,t,y,o=.16,n=5,sp=18):
    for i in range(n): put(cv,c,'mist',(t*sp*(1+i*.3)+i*520)%2800-400,y+(i%2)*30,s=1.2,o=o)
# ---- người ghép mảnh: tọa độ chân (x,y); mọi khớp quay quanh điểm treo
def _end(x,y,L,r): return (x-L*math.sin(math.radians(r)),y+L*math.cos(math.radians(r)))
def linh(cv,c,x,y,t,s=.4,ph=0.,face=1,mode='march',o=1.0):
    """mode: march (đi, giáo vác), run (chạy), thrust (đứng đâm giáo). (x,y) là chân; face=1 quay phải, -1 quay trái"""
    f=face;sp={'march':6.5,'run':10.5,'thrust':0}[mode];amp={'march':26,'run':42,'thrust':0}[mode]
    w=math.sin(t*sp+ph) if sp else 0
    hip=(x,y-148*s+(abs(math.sin(t*sp+ph))*4*s if sp else 0))
    for side in (1,-1):
        a1=side*w*amp*f
        a2=a1+max(0,-side*w)*(45 if sp else 0)*f
        if mode=='thrust': a1=a2=side*9*f
        kx,ky=_end(hip[0],hip[1],75*s,a1)
        put(cv,c,'rg_dui',hip[0],hip[1],s=s,r=a1,ay=0,o=o)
        put(cv,c,'rg_chan',kx,ky,s=s,r=a2,ay=0,o=o)
    lean=(7 if mode=='run' else 2)*f;sl,cl_=math.sin(math.radians(lean)),math.cos(math.radians(lean))
    put(cv,c,'rg_than',hip[0],hip[1],s=s,r=-lean,ay=1,o=o)
    put(cv,c,'rg_dau',hip[0]+100*s*sl,hip[1]-100*s*cl_+4*s,s=s,r=-lean*.5,ay=.9,o=o)
    sh=(hip[0]+92*s*sl,hip[1]-92*s*cl_)
    put(cv,c,'rg_tay',sh[0]-6*s*f,sh[1],s=s,r=(-w*amp*.9 if sp else 8)*f,ay=0,o=o)
    if mode=='thrust': d=.5+.5*math.sin(t*5+ph);ar=-(55+20*d)*f;gr=(78-8*d)*f;push=26*s*d*f
    else: ar=-(35+8*w)*f;gr=(18+4*w)*f;push=0
    hx,hy=_end(sh[0]+6*s*f,sh[1],62*s,ar)
    put(cv,c,'rg_tay',sh[0]+6*s*f,sh[1],s=s,r=ar,ay=0,o=o)
    put(cv,c,'rg_giao',hx+push,hy,s=s,r=gr,ay=.78,o=o)
