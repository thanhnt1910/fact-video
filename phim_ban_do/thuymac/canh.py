# Các cảnh dùng chung cho bản dài và bản dọc
from engine import *
_FL={}
def Af(name):
    if name not in _FL: _FL[name]=np.ascontiguousarray(A(name)[:,::-1])
    return _FL[name]
rg=np.random.default_rng(5)
STAKES=[]
LANE_TIP=[795,830,865]
for row,ty in enumerate(LANE_TIP):
    x=740+row*14
    while x<1440:
        STAKES.append((x+rg.random()*10,ty+rg.random()*14,0.8+row*.12+rg.random()*.12,(rg.random()-.5)*9));x+=48+rg.random()*16
STAKES.sort(key=lambda s:s[1])
ZONE=(740,1440)
MIST=[(rg.random()*2400-200,560+rg.random()*160,0.8+rg.random()*.8,8+rg.random()*14) for _ in range(6)]
def river(cv,cam,t,PAP,sun=0,birds=0,reeds=1,wl=640,boats=(),viet=(),under=.04,stakes=True,fx=(),mist=1.0,cliffs=True,dark=0.0,ridge_o=1.0,far_dx=0,front=(),clx=-120,cr=True):
    if sun: put(cv,cam,'sun',1560,430,s=1.0,o=sun,k=.15)
    if birds: flock(cv,cam,t,birds)
    put(cv,cam,'far',960+far_dx,760,ay=1,k=.35,o=ridge_o)
    for i,(mx,my,ms,sp) in enumerate(MIST[:3]):
        x=(mx+t*sp)%2600-300;put(cv,cam,'mist',x,my-80,s=ms*1.4,o=.75*mist,k=.45)
    put(cv,cam,'mid',960+far_dx*.6,900,ay=1,k=.6,o=ridge_o)
    # nước: phục hồi giấy dưới mực nước, rồi phủ lớp mực loang
    Ys=int(max(0,min(cv.shape[0],cam.p(0,wl)[1])))
    cv[Ys:]=PAP[Ys:]
    put(cv,cam,'water',960,wl-24,ay=0,s=1.0)
    if stakes:
        im=A('stake')
        for x,ty,s,r in STAKES:
            cut=(wl-ty)*1.5/s
            put(cv,cam,rowclip(im,cut,below=under,soft=5),x,ty,s=s,r=r,ax=.5,ay=0,scale_px=1.5)
    for i,yy in enumerate([wl+8,wl+90,wl+210]):
        put(cv,cam,'wave',960-((t*(18+i*9))%200)+(i*77),yy,ay=.5,o=.4-.1*i,s=1.0)
    for b in boats:
        nm=b.get('name','bigboat2')
        im=Af(nm) if b.get('flip') else A(nm)
        put(cv,cam,im,b['x'],b['y'],s=b.get('s',1),r=b.get('r',0),o=b.get('o',1),ax=.5,ay=b.get('ay',.88 if nm=='bigboat2' else .9),scale_px=1.5)
    for b in viet:
        im=Af('smallboat2') if b.get('flip') else A('smallboat2')
        put(cv,cam,im,b['x'],b['y']+math.sin(t*2.3+b['x']*.01)*3,s=b.get('s',1)*.95,r=b.get('r',0)+math.sin(t*1.9+b['x'])*1.5,o=b.get('o',1),ax=.5,ay=.86,scale_px=1.5)
    put(cv,cam,'wave',960-((t*30)%200),wl+18,ay=.5,o=.5,s=1.0)
    for f in fx: f(cv,cam)
    if cliffs:
        put(cv,cam,'cliffL',clx,1200,ax=0,ay=1,k=1.25)
        if cr: put(cv,cam,'cliffR',2420,1150,ax=1,ay=1,k=1.25)
    for i,(mx,my,ms,sp) in enumerate(MIST[3:]):
        x=(mx-t*sp*1.3)%2800-400;put(cv,cam,'mist',x,my+60,s=ms*1.8,o=.6*mist,k=1.1)
    if reeds:
        H_,W_=cv.shape[:2];rs=.42 if W_>H_ else .4
        put(cv,None,wipe(A('reeds'),1,0) if False else A('reeds'),-40,H_+10,ax=0,ay=1,s=rs,r=math.sin(t*.9)*1.5,o=.9*reeds,scale_px=1,screen=True)
        put(cv,None,Af('reeds'),W_+40,H_+10,ax=1,ay=1,s=rs*.9,r=math.sin(t*.8+1)*1.5,o=.9*reeds,scale_px=1,screen=True)
    for f in front: f(cv,cam)
    if dark>0: ink_wash(cv,dark)
def mapbg(cv,cam,u=1.0,o=1.0):
    im=A('map')
    if u<1: im=wipe(im,u,0,.25,seed=4)
    put(cv,cam,im,960,540,o=o,scale_px=1.5)
def seal(cv,name,x,y,t0,t,s=1.0,o=1.0,r=-5,fall=None):
    """triện đỏ đóng xuống: phóng to rồi chạm giấy"""
    if t<t0: return
    u=cl((t-t0)/.28);sc=lerp(1.7,1.0,eo(u));oo=cl((t-t0)/.12)*o
    dx=dy=0;rr=r
    if fall is not None and t>fall:
        v=t-fall;dy=220*v*v;rr=r+40*v;oo*=cl(1-v/1.2)
    put_screen(cv,A(name),x+dx,y+dy,oo,s=s*sc/1.5,r=rr)
def card(cv,t,t0,title,PAP,V=False):
    """thẻ chương: giọt mực loang giữa màn hình, chữ màu giấy"""
    a,b=t0-.45,t0+2.35
    if t<a or t>b+.6: return
    H,W=cv.shape[:2]
    gr=eo((t-a)/.7);fade=1-inn(t,b-.2,.8)
    sc=(1.25 if not V else 1.05)*gr
    put_screen(cv,A('blot'),W/2,H/2,fade*.96,s=sc*(1+.05*(t-a)),r=8*(t-a))
    tx=text(title,58 if not V else 64,PAPER,700,maxw=760 if V else 1100)
    u=inn(t,t0,.6);put_screen(cv,wipe(tx,u,0,.3,seed=7),W/2,H/2,fade*u)

def flock(cv,cam,t,o=1.0,n=6,y0=260,sp=38,seed=3):
    r=np.random.default_rng(seed)
    for i in range(n):
        x=(r.random()*2400+t*sp*(0.8+r.random()*.4))%2600-300;y=y0+r.random()*120+math.sin(t*.7+i)*10
        f=math.sin(t*7+i*1.7);w=16+r.random()*8
        stroke(cv,cam.par(.5),[(x-w,y-6*f-4),(x,y+2),(x+w,y-6*f-4)],1,wid=3,head=False,o=.75*o)
