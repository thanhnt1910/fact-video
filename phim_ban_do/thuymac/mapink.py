# Bản đồ mực từ world7.jpg (đường bờ biển, sông thật). Lớp mực RGBA, nền trong suốt.
import numpy as np,cv2,math
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
im=np.asarray(Image.open('/tmp/pc/phim_ban_do/world7.jpg').convert('RGB')).astype(np.float32)
LON0,LAT1,S=102.0,24.8,520;KX=S*math.cos(math.radians(23))
# khung: lon 104.3..114.3, 16:9
x0=(103.5-LON0)*KX;x1=(114.0-LON0)*KX;w=x1-x0;h=w*9/16;yc=(LAT1-21.35)*S;y0=yc-h/2
print('crop',x0,y0,w,h,'lat',LAT1-y0/S,LAT1-(y0+h)/S)
OW,OH=2880,1620
sc=OW/w
M=np.float32([[sc,0,-x0*sc],[0,sc,-y0*sc]])
c=cv2.warpAffine(im,M,(OW,OH),flags=cv2.INTER_AREA if sc<1 else cv2.INTER_LINEAR)
R,G,B=c[...,0],c[...,1],c[...,2]
blue=(B>R+12).astype(np.uint8)
sea=cv2.morphologyEx(blue,cv2.MORPH_OPEN,np.ones((9,9),np.uint8))
# giữ thành phần lớn = biển
n,lab,st,_=cv2.connectedComponentsWithStats(sea)
keep=np.zeros_like(sea)
for i in range(1,n):
    if st[i,4]>20000: keep[lab==i]=1
sea=keep
river=blue*(1-cv2.dilate(sea,np.ones((7,7),np.uint8)))
river=cv2.morphologyEx(river,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
lum=(R+G+B)/3
mount=((R<165)&(G<140)&(B<110)&(sea==0)).astype(np.uint8)
rng=np.random.default_rng(3)
def fbm(oct=5,base=4):
    out=np.zeros((OH,OW),np.float32);a=1;t=0
    for o in range(oct):
        nn=base*2**o;g=rng.random((int(nn*OH/OW)+2,nn+2)).astype(np.float32)
        out+=cv2.resize(g,(OW,OH),interpolation=cv2.INTER_CUBIC)*a;t+=a;a*=.5
    return out/t
N=fbm();N2=fbm(4,12)
# biển: mực loang đậm dần ra khơi, có vệt sóng ngang
dist=cv2.distanceTransform(sea,cv2.DIST_L2,5)
seaa=sea*(0.24+0.26*np.clip(dist/300,0,1)+0.18*(N-.5))
yy=np.arange(OH)[:,None];xx=np.arange(OW)[None,:]
lines=(np.sin(yy*0.07+N2*14+xx*0.0015)>0.965).astype(np.float32)*sea*np.clip(dist/60,0,1)*0.16*(N2>0.55)
lines=cv2.GaussianBlur(lines,(0,0),1.2)
# bờ biển: viền mực, có rung
edge=cv2.morphologyEx(sea,cv2.MORPH_GRADIENT,np.ones((3,3),np.uint8)).astype(np.float32)
edge=np.clip(cv2.GaussianBlur(cv2.dilate(edge,np.ones((2,2),np.uint8)),(0,0),1.1)*1.4,0,1)
inner=np.clip(1-dist/18,0,1)*sea*0.25   # quầng đậm sát bờ
rv=np.clip(cv2.GaussianBlur(river.astype(np.float32),(0,0),.9)*1.3,0,1)*0.6
# địa hình: vùng tối trên đất -> mực nhạt; tam giác núi -> nét mực
ref=cv2.GaussianBlur(lum,(0,0),60)
relief=np.clip((218-cv2.GaussianBlur(lum,(0,0),10))/55,0,1)*(1-sea)*0.30
mt=np.zeros((OH,OW),np.float32)
nm,lm,stm,cen=cv2.connectedComponentsWithStats(mount)
for i in range(1,nm):
    if stm[i,4]<4: continue
    ys,xs=np.nonzero(lm==i)
    k=max(1,int(stm[i,4]/90))
    for j in rng.choice(len(xs),size=min(k,len(xs)),replace=False):
        cx,cy=xs[j],ys[j];hh=12+rng.random()*16;ww=hh*1.5
        tmp=np.zeros((OH,OW),np.uint8)
        L=np.int32([[ (cx-ww/2+ww/2*u)*4,(cy+hh*.4-hh*(u**.8))*4] for u in np.linspace(0,1,7)])
        Rr=np.int32([[ (cx+ww/2*u)*4,(cy-hh*.6+hh*(u**1.2))*4] for u in np.linspace(0,1,7)])
        cv2.polylines(tmp,[L],False,255,3,cv2.LINE_AA,shift=2)
        cv2.polylines(tmp,[Rr],False,170,2,cv2.LINE_AA,shift=2)
        mt=np.maximum(mt,tmp.astype(np.float32)/255*0.75)
        sh=np.zeros((OH,OW),np.uint8)
        cv2.fillPoly(sh,[np.concatenate([L,Rr])],90,cv2.LINE_AA,shift=2)
        mt=np.maximum(mt,cv2.GaussianBlur(sh.astype(np.float32)/255,(0,0),2)*0.4)
A=np.clip(seaa+lines+edge*0.9+inner+rv+relief+mt,0,1)
# làm méo nhẹ cho giống nét cọ
dx=(cv2.GaussianBlur(rng.random((OH,OW)).astype(np.float32),(0,0),3)-.5)*14
dy=(cv2.GaussianBlur(rng.random((OH,OW)).astype(np.float32),(0,0),3)-.5)*14
mx,my=np.meshgrid(np.arange(OW,dtype=np.float32),np.arange(OH,dtype=np.float32))
A=cv2.remap(A.astype(np.float32),mx+dx,my+dy,cv2.INTER_LINEAR)
ink=np.array([21,19,15],np.uint8)
out=np.zeros((OH,OW,4),np.uint8);out[...,:3]=ink;out[...,3]=(A*255).astype(np.uint8)
Image.fromarray(out,'RGBA').save('/tmp/gen/bd/a/map.png')
# tọa độ thế giới (1920x1080) của các địa danh
def wpt(lon,lat): X=(lon-LON0)*KX;Y=(LAT1-lat)*S;return round((X-x0)*sc/1.5,1),round((Y-y0)*sc/1.5,1)
P={'daila':(105.85,21.03),'coloa':(105.87,21.11),'aichau':(105.78,19.80),'quangchau':(113.26,23.13),'haimon':(109.6,21.75),'bachdang':(106.80,20.85),'leizhou':(110.3,20.6)}
import json;json.dump({k:wpt(*v) for k,v in P.items()},open('/tmp/gen/bd/a/map_pts.json','w'),indent=1)
print({k:wpt(*v) for k,v in P.items()})
# xem thử trên giấy
pap=np.full((OH,OW,3),(236,226,203),np.float32);a=A[...,None]
Image.fromarray((pap*(1-a)+np.float32(ink)*a).astype(np.uint8)).resize((1440,810)).save('/tmp/gen/bd/map_xem.jpg')
