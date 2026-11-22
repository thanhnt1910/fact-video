# Thử nâng cấp màu và chuyển động cho thủy mặc (tm21, chờ chủ kênh duyệt): tô màu nước lên lớp nền theo độ sáng và độ cao,
# viền giấy loang màu, bụi mực và lá bay. Chỉ tác động lớp nền (gọi trước khi vẽ người), người giữ màu riêng.
import numpy as np,math

_Y=np.linspace(0,1,1080,dtype=np.float32)[:,None,None]
_X=np.linspace(-1,1,1920,dtype=np.float32)[None,:,None]
TROI_TREN=np.float32([.95,.83,.64]);TROI_DUOI=np.float32([.94,.90,.80])
NUI=np.float32([.42,.52,.62]);DAT=np.float32([.55,.62,.42]);DAT_SANG=np.float32([.86,.82,.66])
def to_mau(cv,hor=.6,o=1.0,dem=False):
    L=cv.mean(2,keepdims=True)
    wp=np.clip((L-.80)/.08,0,1)                 # giấy, trời
    wm=np.clip(1-np.abs(L-.62)/.22,0,1)          # núi, cây nhạt, mặt đất xám
    tren=(_Y<hor).astype(np.float32);mem=np.clip((_Y-hor+.05)/.1,0,1)
    troi=TROI_TREN*(1-_Y/hor)[...,]*tren+TROI_DUOI*(np.clip(_Y/hor,0,1))*tren+DAT_SANG*(1-tren)
    if dem: troi=troi*np.float32([.55,.58,.78])
    out=cv*(1-wp*o)+troi*L/0.88*wp*o
    tint=NUI*(1-mem)+DAT*mem
    out=out*(1-wm*.7*o)+(tint*(L/.62))*wm*.7*o
    v=np.clip((np.abs(_X)**3*.6+np.abs(_Y-.5)**3*1.6),0,1)   # viền giấy loang nâu
    out=out*(1-v*.35*o)+np.float32([.45,.32,.2])*v*.35*o
    cv[:]=np.clip(out,0,1)
_RG=np.random.default_rng(21);_P=_RG.random((26,5)).astype(np.float32)
def _splat(cv,x,y,rx,ry,ang,col,o):
    R=int(max(rx,ry)*3)+2;x0,y0=int(x)-R,int(y)-R;x1,y1=x0+2*R,y0+2*R
    if x1<0 or y1<0 or x0>=cv.shape[1] or y0>=cv.shape[0]: return
    yy,xx=np.mgrid[y0:y1,x0:x1].astype(np.float32);ca,sa=math.cos(ang),math.sin(ang)
    u=((xx-x)*ca+(yy-y)*sa)/rx;v=(-(xx-x)*sa+(yy-y)*ca)/ry
    m=np.exp(-(u*u+v*v)*1.6)[...,None]*o
    a0,b0=max(0,y0),max(0,x0);a1,b1=min(cv.shape[0],y1),min(cv.shape[1],x1)
    mm=m[a0-y0:a1-y0,b0-x0:b1-x0];cv[a0:a1,b0:b1]=cv[a0:a1,b0:b1]*(1-mm)+col*mm
def bui(cv,t,o=1.0):
    """lá và bụi mực bay chéo qua khung, lá xoay khi bay"""
    for i,(x0,y0,sp,sz,kind) in enumerate(_P):
        u=(t*(.025+.04*sp)+x0)%1.0
        x=-80+2080*u;y=(y0*820+90*math.sin(t*.8+i*1.3)+u*240)%960
        if kind>.55:   # lá: đỏ son hoặc vàng đất, dẹt, xoay
            col=np.float32([.66,.24,.12]) if kind>.8 else np.float32([.78,.58,.22])
            _splat(cv,x,y,7+6*sz,2.5+1.5*sz,t*(1.5+sp)+i,col,o*.8)
        else:          # bụi mực
            _splat(cv,x,y,2+2.5*sz,2+2.5*sz,0,np.float32([.1,.09,.08]),o*(.25+.3*sp))
