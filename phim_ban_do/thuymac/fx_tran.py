# Hiệu ứng cảnh giao chiến dùng chung: mưa tên theo vòng cung, bụi vó ngựa, tia va chạm, người ngã
import math,random
from canh import *
from engine import stroke
def _cl(x): return max(0.,min(1.,x))
def arrows(cv,c,t,a,b,src,dst,n=12,h=80,per=1.0,wid=4,o=.85,col=INK,seed=1,hits=True):
    """n mũi tên bay lặp vòng từ các điểm src tới dst, cung thấp cao h, hướng theo tiếp tuyến"""
    if t<a-.1 or t>b+per: return
    R=random.Random(seed)
    for k in range(n):
        x0,y0=src[k%len(src)];x1,y1=dst[(k*7+3)%len(dst)]
        x0+=R.uniform(-20,20);x1+=R.uniform(-40,40);off=R.random()
        ph=((t-a)/per+off)%1;st=a+(int((t-a)/per+off)-off)*per
        if st<a-1e-6 or st>b: continue
        def P(u): return lerp(x0,x1,u),lerp(y0,y1,u)-h*4*u*(1-u)
        xa,ya=P(ph);xb,yb=P(max(0,ph-.1))
        stroke(cv,c,[(xb,yb),(xa,ya)],1,wid=wid,head=True,col=col,o=o*_cl((ph-.05)*10)*_cl((1-ph)*12))
        if hits and ph>.9: put(cv,c,'blot',x1,y1,s=.10,o=.35*_cl((ph-.9)*10))
def dust(cv,c,x,y,o=.35,s=.4): put(cv,c,'mist',x,y,s=s,o=o)
def sparks(cv,c,t,pts,a,b,seed=5,col=INK):
    """tia chớp ngắn ở chỗ hai bên giáp nhau (nét mực xòe, nhấp nháy)"""
    if not a<t<b: return
    R=random.Random(seed)
    for k,(x,y) in enumerate(pts):
        f=(t*3.1+R.random())%1
        if f>.45: continue
        for j in range(4):
            ang=R.uniform(0,2*math.pi);L=R.uniform(18,34)*(1-f)
            stroke(cv,c,[(x,y),(x+L*math.cos(ang),y+L*math.sin(ang))],1,wid=2,head=False,col=col,o=.8*(1-f/.45))
def fall(cv,c,img,x,y,t,t0,s=.5,dirn=1,ay=1):
    """người hoặc ngựa ngã: nghiêng dần rồi nhạt đi (không máu)"""
    u=_cl((t-t0)/.7);put(cv,c,img,x+dirn*20*u,y,ay=ay,s=s,r=dirn*75*u,o=1-.85*_cl((t-t0-.6)/1.0))
