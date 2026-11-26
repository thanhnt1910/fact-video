# Làm sạch và cắt khung 16:9 cho tranh FLUX tm28: bỏ dấu đỏ và chữ giả, cắt dải giữa 1024x576, phóng 1920x1080.
# python3 lam_anh_tm28.py [mã...]  -> /tmp/gen/tm28/anh/<mã>.jpg ; DY={mã:dịch dọc} khi chủ thể lệch.
import cv2,numpy as np,glob,os,sys
from pathlib import Path
OUT=Path('/dev/shm/tm28/anh');OUT.mkdir(parents=True,exist_ok=True)
DY={}
def sach(im):
    """chỉ xóa dấu đỏ nhỏ, gần vuông (con dấu giả); giữ áo đỏ, cờ, tường gạch"""
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV);h,s,v=cv2.split(hsv);H,W=h.shape
    red=(((h<12)|(h>165))&(s>90)&(v>60)).astype(np.uint8)
    n,lab,st,_=cv2.connectedComponentsWithStats(cv2.dilate(red,np.ones((5,5),np.uint8)))
    m=np.zeros_like(red)
    for i in range(1,n):
        x,y,w,hh,a=st[i]
        if a<H*W*.003 and .5<w/max(hh,1)<2.2 and (x<W*.15 or x>W*.85 or y<H*.15 or y>H*.85): m[lab==i]=255
    m=cv2.dilate(m,np.ones((9,9),np.uint8))
    return cv2.inpaint(im,m,7,cv2.INPAINT_TELEA) if m.any() else im
def chu(im):
    """chữ giả: nét tối mảnh dồn thành cột ở hai mép trái phải"""
    g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);H,W=g.shape;m=np.zeros_like(g)
    for x0,x1 in [(0,int(W*.16)),(int(W*.84),W)]:
        z=g[:,x0:x1];dark=(z<110).astype(np.uint8)
        bg=cv2.medianBlur(z,31);thin=((bg.astype(int)-z)>45).astype(np.uint8)&dark
        n,lab,st,_=cv2.connectedComponentsWithStats(thin)
        for i in range(1,n):
            x,y,w,h,a=st[i]
            if 6<w<70 and 6<h<70 and a<1800: m[y:y+h,x0+x:x0+x+w]=255
    m=cv2.dilate(m,np.ones((7,7),np.uint8))
    return cv2.inpaint(im,m,7,cv2.INPAINT_TELEA) if m.any() else im
def lam(src):
    k=Path(src).stem.split('_')[-1];im=sach(cv2.imread(src))   # chữ giả nằm ở dải trên, dưới nên bị cắt bỏ khi lấy khung 16:9
    H,W=im.shape[:2];ch=int(W*9/16);y0=int(np.clip((H-ch)//2+DY.get(k,0),0,H-ch))
    im=cv2.resize(im[y0:y0+ch],(1920,1080),interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(str(OUT/f'{k}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,90])
if __name__=='__main__':
    ks=sys.argv[1:]
    for f in sorted(glob.glob('/dev/shm/tm28/src/NBTM28[ABC]_cf_*.jpg')):
        if not ks or Path(f).stem in ks: lam(f)
