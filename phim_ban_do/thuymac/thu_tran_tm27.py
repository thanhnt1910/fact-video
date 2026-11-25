# Thử cảnh đánh nhau kiểu mới: sông Bạch Đằng lúc thủy triều rút, thuyền quân Nguyên mắc cọc, thuyền Đại Việt lao ra đánh.
# Nền cửa sông lúc triều xuống vẽ bằng FLUX (không người, không thuyền), xóa chữ và dấu giả; cọc, nước, thuyền, người, tên bay vẽ bằng mã.
import sys,math,numpy as np,cv2
sys.path.insert(0,'/tmp/gen/bd');sys.path.insert(0,'/tmp/gen/tm27')
from engine import *
from khung_dung import PAP
from canh import Af
import rig
for _k in ['omn6','m7','m8','m9','v6','v7','v8','hdv6']: rig.PRE[_k]='t26n_r_'
from thu_but2 import nen
W,H=1920,1080;FPS=24;DUR=12.0
BG=nen('/tmp/pc/assets/anh_2d/NBTM27_cf/song_a.jpg',[(40,50,115,270),(925,925,995,995)])
SC=1.875;BGS=cv2.resize(BG,None,fx=SC,fy=SC,interpolation=cv2.INTER_CUBIC)
bl=cv2.GaussianBlur(BGS,(0,0),2.0);BGS=np.clip(BGS*1.6-bl*.6,0,1)
BG4=np.dstack([BGS,np.ones(BGS.shape[:2],np.float32)])
WL=1250   # mực nước (toạ độ thế giới) lúc triều đầy
def nuoc(t): return WL+70*inn(t,1.0,6.0)          # thủy triều rút: mặt nước hạ dần
R=np.random.default_rng(8)
COC=[(int(330+i*56+R.normal(0,12)),int(1430+R.normal(0,14)+(i%3)*18),R.uniform(-18,18),R.uniform(1.0,1.25)) for i in range(26)]
def coc(cv,c,t):
    """cọc gỗ nhọn: lộ dần khi nước rút; vẽ bằng nét mực"""
    wl=nuoc(t)
    for x,yb,ang,h in COC:
        top=yb-150*h;vis=max(0,min(1,(wl-top)/-1)) if False else 1
        X0,Y0=c.p(x,yb);X1,Y1=c.p(x+math.sin(math.radians(ang))*150*h,top)
        Xw,Yw=c.p(0,wl)
        if Y1>Yw-2: continue      # còn chìm
        col=tuple(float(v) for v in INK+.05)
        w=max(3,int(9*c.z*h));Yb=min(Y0,Yw+4)
        dx_,dy_=X1-X0,Y1-Yb;L_=math.hypot(dx_,dy_)+1e-6;nx,ny=-dy_/L_,dx_/L_
        tipx,tipy=X1+dx_/L_*w*2.2,Y1+dy_/L_*w*2.2
        poly=np.int32([[X0+nx*w,Yb+ny*w],[X1+nx*w*.8,Y1+ny*w*.8],[tipx,tipy],[X1-nx*w*.8,Y1-ny*w*.8],[X0-nx*w,Yb-ny*w]])
        cv2.fillPoly(cv,[poly],col,cv2.LINE_AA)
        cv2.ellipse(cv,(int(X0),int(Yw+3)),(int(w*1.6),3),0,0,360,tuple(float(v) for v in INK*0+INK*.5+PAPER*.5),1,cv2.LINE_AA)
WASH=None
def song_nuoc(cv,c,t):
    """mặt sông: dải mực loang nhạt, vệt sóng chạy ngang"""
    global WASH
    if WASH is None:
        from thu_but import fbm,premul
        h,w=360,2600;yy=np.linspace(0,1,h)[:,None]
        a=(np.exp(-((yy-.35)/.35)**2)*.26*(.6+.8*fbm(h,w,77,90))).astype(np.float32)
        WASH=premul(np.clip(a,0,.4))
    wl=nuoc(t)
    put(cv,c,WASH,960,wl-40,ay=0,scale_px=1)
    for k in range(9):
        y=wl+20+k*38;x=((t*(30+k*7)+k*370)%2400)-200
        put(cv,c,band(300+k*20,5,INK,.18,3),x,y)
def thuyen(cv,c,x,y,t,s,lon,flip,ngoi,nghieng=0,o=1.0,ph=0):
    bob=0 if nghieng else 3*math.sin(t*1.3+ph);r=nghieng+.8*math.sin(t*.9+ph)
    f=-1 if flip else 1;name='t23n_thuyenlon' if lon else 't23n_thuyen'
    for key,dx,vk in ngoi:
        PP=rig.ngoi(t+dx*.01);PP.update(thF=-80,thB=-76,knF=84,knB=82)
        if vk=='cheo': PP.update(arF=-10+25*math.sin(t*4+dx),faF=-40,arB=10+25*math.sin(t*4+dx),faB=-40,mat='G');vk=None
        elif vk=='so': PP.update(arF=-120+3*math.sin(t*23),faF=-70,arB=-100,faB=-80,lean=-10,mat='S');vk=None
        elif vk=='dam': PP.update(arF=-60+40*math.sin(t*6+dx),faF=-10,lean=14,mat='G');vk='giao'
        rr=math.radians(r);hx=x+f*dx*s*math.cos(rr);hy=y-46*s+bob+f*dx*s*math.sin(rr)
        rig.ve23(cv,c,key,0,0,s,PP,flip=flip,vk=vk,o=o,hip=(hx,hy))
    put(cv,c,Af(name) if flip else name,x,y+bob,s=s,r=r,ay=.8,o=o,scale_px=3)
def ten(cv,c,t,src,dst,n,seed,col):
    r=np.random.default_rng(seed)
    for i in range(n):
        ph=((t*.9+r.random())%1.0);a=src[0]+r.normal(0,40),src[1]+r.normal(0,20);b=dst[0]+r.normal(0,80),dst[1]+r.normal(0,30)
        x=lerp(a[0],b[0],ph);y=lerp(a[1],b[1],ph)-math.sin(ph*math.pi)*220
        x2=lerp(a[0],b[0],ph-.04);y2=lerp(a[1],b[1],ph-.04)-math.sin((ph-.04)*math.pi)*220
        X,Y=c.p(x,y);X2,Y2=c.p(x2,y2)
        cv2.line(cv,(int(X2),int(Y2)),(int(X),int(Y)),tuple(float(v) for v in col),2,cv2.LINE_AA)
def roi(cv,c,key,x0,y0,t,t0,dx):
    """người rơi xuống nước, có vòng nước bắn"""
    if t<t0: return
    u=(t-t0)/1.1
    if u<1:
        P=rig.so(t,1.3);rig.ve23(cv,c,key,x0+dx*u,y0+120*u*u-60*math.sin(u*math.pi),.36,P,flip=dx<0)
    else:
        X,Y=c.p(x0+dx,nuoc(t)+8);k=min(1,(u-1)*1.5)
        if k<1: cv2.ellipse(cv,(int(X),int(Y)),(int(20+70*k),int(5+10*k)),0,0,360,tuple(float(v) for v in INK*(1-k)+PAPER*k),2,cv2.LINE_AA)
def lop(c,t):
    """lớp thuyền, người, cọc, tên (vẽ trên nền đen và trắng để lấy độ trong rồi xử lý cho hợp tranh)"""
    A0=np.zeros((H,W,3),np.float32);A1=np.ones((H,W,3),np.float32)
    def draw(cv):
        wl=nuoc(t);tilt=inn(t,3.5,2.5)
        # hàng xa: thuyền Nguyên nhỏ, nhạt
        for i,x in enumerate([760,1240]):
            thuyen(cv,c,x+40*inn(t,0,3.5)*(1-tilt),wl-40+10*tilt,t,.42,True,True,[('m8',-100,'so' if t>5 else None),('m9',80,None)],nghieng=tilt*[7,-9][i],ph=i+3,o=.75)
        # hàng giữa: ba thuyền lớn, đang đuổi rồi mắc cọc, nghiêng
        for i,(x,ph,dy) in enumerate([(520,0,20),(1000,1.3,70),(1480,2.1,0)]):
            xx=x+60*inn(t,0,3.5)*(1-tilt)
            ng=[('omn6' if i==1 else 'm8',-110,'so' if t>5 else None),('m7',40,'so' if t>4.5 else 'dam'),('m9',130,'so' if t>5.5 else None)]
            thuyen(cv,c,xx,wl+dy+16*tilt,t,.6,True,True,ng,nghieng=tilt*[10,-13,8][i],ph=ph)
        coc(cv,c,t)
        # thuyền nhỏ Đại Việt lao ra từ hai bên, ở tiền cảnh
        for i in range(6):
            st=4.0+i*.3;u=inn(t,st,4.0)
            j=i//2;x=lerp(-300-j*120,330+j*300,u) if i%2==0 else lerp(2250+j*120,1640-j*290,u)
            thuyen(cv,c,x,wl+170+j*55,t,.5+j*.05,False,i%2==1,[('v8',-50,'cheo'),(['v6','v7','v8'][i%3],40,'dam')],ph=i)
        if t>4.5:
            ten(cv,c,t,(400,wl+90),(1000,wl-60),10,3,INK)
            ten(cv,c,t,(1650,wl+100),(1150,wl-50),8,4,INK)
        for k,(x,t0,dx) in enumerate([(1010,6.3,90),(560,7.1,-80),(1440,7.8,70),(1050,9.0,-60)]):
            roi(cv,c,['m7','m8','m9','m7'][k],x,wl-90,t,t0,dx)
    draw(A0);draw(A1)
    a=np.clip(1-(A1-A0).mean(2),0,1);col=np.where(a[...,None]>1e-3,A0/np.maximum(a[...,None],1e-3),0)
    lum=col.mean(2,keepdims=True);tone=INK+lum*(PAPER-INK);col=col*.38+tone*.62
    col=cv2.GaussianBlur(col,(0,0),.6);a=cv2.GaussianBlur(a,(0,0),.6)
    return col,a
def frame(t):
    sh=4*math.sin(t*40)*(1-inn(t,5.0,.8)) if 4.2<t<5.8 else 0
    c=Cam(960+40*inn(t,0,DUR)+sh,lerp(1210,1260,inn(t,0,DUR)),lerp(1.0,1.14,inn(t,0,DUR)),W,H)
    cv=PAP.copy();put(cv,c,BG4,0,0,ax=0,ay=0,scale_px=1)
    song_nuoc(cv,c,t)
    col,a=lop(c,t);cv[:]=cv*(1-a[...,None])+col*a[...,None]
    for k in range(2): put(cv,c,band(2200,80,PAPER,.35,50),((t*35+k*1200)%3000)-300,1080+k*90,k=.8)
    if t>.6: put_screen(cv,text('sông Bạch Đằng · thủy triều rút',48,INK,700),360,120,inn(t,.6,.8)*(1-inn(t,4.0,.6)))
    return cv
if __name__=='__main__':
    import subprocess
    if sys.argv[1]=='soi':
        from PIL import Image
        ims=[Image.fromarray((np.clip(frame(float(x)),0,1)*255).astype('uint8')).resize((960,540)) for x in sys.argv[2:]]
        s=Image.new('RGB',(960*2,540*((len(ims)+1)//2)))
        for i,im in enumerate(ims): s.paste(im,((i%2)*960,(i//2)*540))
        s.save('/dev/shm/thu.jpg')
    else:
        p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',sys.argv[1]],stdin=subprocess.PIPE)
        for f in range(int(DUR*FPS)): p.stdin.write((np.clip(frame(f/FPS),0,1)*255).astype(np.uint8).tobytes())
        p.stdin.close();p.wait()
