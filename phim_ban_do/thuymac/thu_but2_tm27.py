# Thử kiểu tranh (bản 2, "dùng mọi công cụ"): nền phong cảnh thủy mặc KHÔNG người vẽ bằng FLUX (Cloudflare),
# xóa chữ và dấu triện giả, chuyển về tông giấy của series; người (lính nhìn từ sau, tướng cưỡi ngựa) vẽ bằng mã,
# xử lý lớp người cho hợp tranh: bớt màu, mờ nhẹ, nhạt dần theo khoảng cách. Máy quay lia từ đỉnh núi xuống đường đèo.
import sys,math,numpy as np,cv2
sys.path.insert(0,'/tmp/gen/bd')
from engine import *
from khung_dung import PAP
W,H=1920,1080;FPS=24;DUR=11.0
def nen(path,boxes):
    im=cv2.imread(path)
    m=np.zeros(im.shape[:2],np.uint8)
    for x0,y0,x1,y1 in boxes:
        sub=im[y0:y1,x0:x1].astype(np.int16);g=sub.mean(2)
        red=(sub[...,2]-sub[...,1])>40;dark=g<150
        m[y0:y1,x0:x1]=((red|dark)*255).astype(np.uint8)
    m=cv2.dilate(m,np.ones((9,9),np.uint8))
    im=cv2.inpaint(im,m,9,cv2.INPAINT_TELEA)
    L=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)
    p=np.percentile(L,97);v=np.clip(L/p,0,1)**1.15
    out=INK[None,None,:]+v[...,None]*(PAPER-INK)[None,None,:]
    return out.astype(np.float32)
BG=nen('/tmp/pc/assets/anh_2d/NBTM27_cf/deo_a.jpg',[(40,20,150,240),(920,935,1000,1005)])
SC=1.875;BGS=cv2.resize(BG,None,fx=SC,fy=SC,interpolation=cv2.INTER_CUBIC)
bl=cv2.GaussianBlur(BGS,(0,0),2.0);BGS=np.clip(BGS*1.6-bl*.6,0,1)   # làm nét lại sau khi phóng
gr=np.random.default_rng(5).normal(0,.018,BGS.shape[:2]).astype(np.float32);BGS=np.clip(BGS+gr[...,None]*.8,0,1)
BG4=np.dstack([BGS,np.ones(BGS.shape[:2],np.float32)])
# đường đèo trong ảnh gốc (toạ độ 1024) -> thế giới
ROAD=np.float32([(430,1040),(365,960),(305,885),(258,815),(232,775),(206,752)])*SC
def road(u):
    d=np.r_[0,np.cumsum(np.hypot(*np.diff(ROAD,axis=0).T))];s=u*d[-1]
    return float(np.interp(s,d,ROAD[:,0])),float(np.interp(s,d,ROAD[:,1]))
def cam_t(t):
    u=inn(t,.3,DUR-1.3)
    return Cam(lerp(960,900,u),lerp(820,1400,u),lerp(1.0,1.12,u),W,H)
def nguoi(c,t):
    """vẽ lớp người riêng (trên nền đen và nền trắng) để lấy độ trong, rồi xử lý cho hợp tranh"""
    A0=np.zeros((H,W,3),np.float32);A1=np.ones((H,W,3),np.float32)
    def draw(cv):
        n=34
        items=[]
        for i in range(n):
            u=((i/n)+t*.018)%1.0
            x,y=road(u);s=lerp(1.05,.12,u**.7)
            items.append((y,x,s,u,i))
        for y,x,s,u,i in sorted(items):
            k='abc'[i%3];ph=int(t*3.2+i*.5)%2
            put(cv,c,f't27n_linhsau_{k}_{ph}',x+(i%2-.5)*70*s,y,s=s,ay=1,o=lerp(1,.6,u))
        uu=inn(t,0,DUR);ph=int(t*2.4)%2
        put(cv,c,'t27n_kysau_b' if ph else 't27n_kysau_a',1330-110*uu,2030-60*uu+5*math.sin(t*4.8),s=1.8-.2*uu,ay=1)
    draw(A0);draw(A1)
    a=np.clip(1-(A1-A0).mean(2),0,1);col=np.where(a[...,None]>1e-3,A0/np.maximum(a[...,None],1e-3),0)
    lum=col.mean(2,keepdims=True);tone=INK+lum*(PAPER-INK)
    col=col*.45+tone*.55
    col=cv2.GaussianBlur(col,(0,0),.6);a=cv2.GaussianBlur(a,(0,0),.6)
    return col,a
def frame(t):
    c=cam_t(t);cv=PAP.copy()
    put(cv,c,BG4,0,0,ax=0,ay=0,scale_px=1)
    for k in range(3):
        put(cv,c,band(1700,110,PAPER,.5,50),((t*30+k*800)%2800)-200,1250+k*120,k=.9)
    col,a=nguoi(c,t)
    cv[:]=cv*(1-a[...,None])+col*a[...,None]
    for k in range(2):
        put(cv,c,band(2200,90,PAPER,.42,50),((t*45+k*1100)%3000)-300,1700+k*120,k=1.15)
    if t>1.5: put_screen(cv,text('ải Nội Bàng',54,INK,700),250,130,inn(t,1.5,.8))
    return cv
if __name__=='__main__':
    import subprocess
    if sys.argv[1]=='soi':
        from PIL import Image
        ims=[Image.fromarray((np.clip(frame(float(x)),0,1)*255).astype('uint8')).resize((960,540)) for x in sys.argv[2:]]
        s=Image.new('RGB',(960,540*len(ims)))
        for i,im in enumerate(ims): s.paste(im,(0,i*540))
        s.save('/dev/shm/thu.jpg')
    else:
        p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',sys.argv[1]],stdin=subprocess.PIPE)
        for f in range(int(DUR*FPS)): p.stdin.write((np.clip(frame(f/FPS),0,1)*255).astype(np.uint8).tobytes())
        p.stdin.close();p.wait()
