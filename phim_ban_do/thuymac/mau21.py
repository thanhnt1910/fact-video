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
# ---- nền tô màu: tính sẵn các lớp không đổi theo khung
_CACHE={}
def _nen(hor,dem):
    k=(hor,dem)
    if k not in _CACHE:
        tren=(_Y<hor).astype(np.float32);mem=np.clip((_Y-hor+.05)/.1,0,1)
        troi=TROI_TREN*(1-_Y/hor)*tren+TROI_DUOI*np.clip(_Y/hor,0,1)*tren+DAT_SANG*(1-tren)
        if dem: troi=troi*np.float32([.62,.64,.82])
        tint=NUI*(1-mem)+DAT*mem
        if dem: tint=tint*np.float32([.7,.72,.95])
        v=np.clip((np.abs(_X)**3*.6+np.abs(_Y-.5)**3*1.6),0,1)
        _CACHE[k]=(np.broadcast_to(troi,(1080,1920,3)).astype(np.float32),np.broadcast_to(tint,(1080,1920,3)).astype(np.float32),np.broadcast_to(v,(1080,1920,1)).astype(np.float32))
    return _CACHE[k]
def to_mau(cv,hor=.6,o=1.0,dem=False):
    troi,tint,v=_nen(hor,dem)
    L=cv.mean(2,keepdims=True)
    wp=np.clip((L-.80)/.08,0,1)*o;wm=np.clip(1-np.abs(L-.62)/.22,0,1)*(.7*o)
    out=cv+wp*(troi*(L/.88)-cv)
    out+=wm*(tint*(L/.62)-out)
    out+=v*.35*o*(np.float32([.45,.32,.2])-out)
    np.clip(out,0,1,out=cv)
BIEN=np.float32([.40,.52,.60]);GIAY_BD=np.float32([.93,.86,.70])
def to_mau_bd(cv,o=1.0):
    """bản đồ: biển và núi xanh chàm nhạt, đất màu giấy ấm"""
    _,_,v=_nen(.6,False)
    L=cv.mean(2,keepdims=True)
    wp=np.clip((L-.80)/.08,0,1)*o;wm=np.clip(1-np.abs(L-.6)/.25,0,1)*(.6*o)
    out=cv+wp*(GIAY_BD*(L/.88)-cv)
    out+=wm*(BIEN*(L/.6)-out)
    out+=v*.3*o*(np.float32([.45,.32,.2])-out)
    np.clip(out,0,1,out=cv)
# ---- tà áo và tua cờ bay theo gió (uốn hình, không lắc cả hình)
import cv2
_G={}
def gio(img,t,ph=0.0,tua=True):
    h,w=img.shape[:2]
    if (h,w) not in _G:
        yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
        robe=np.clip((yy/h-.42)/.58,0,1)**1.5
        tm=((xx>w*.6)&(yy<h*.45)).astype(np.float32);tm=cv2.GaussianBlur(tm,(0,0),6)*(1-np.clip(yy/(h*.45),0,1))
        _G[(h,w)]=(xx,yy,robe,tm)
    xx,yy,robe,tm=_G[(h,w)]
    dx=robe*(w*.018)*np.sin(t*2.1+yy/h*7+ph)
    if tua: dx=dx+tm*(w*.03)*np.sin(t*3.2+yy/h*14+ph)
    return cv2.remap(img,xx-dx.astype(np.float32),yy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=0)
