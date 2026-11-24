# Nhân vật múa rối ghép mảnh (thử 24/11/2026). Mảnh vẽ ở assets.html (rigpart), tên t19n_r_<key>_<mảnh>.
# Góc tính bằng độ, quy ước giống engine.put: góc dương xoay đoạn chĩa xuống sang phía sau (về -x khi nhìn sang phải).
import math
from engine import put
from canh import Af
SC=1.1
PIV={'legU':(.5,14/90),'legL':(30/80,14/90),'armU':(.5,14/70),'armL':(.5,14/70),'torso':(.5,150/220),'head':(.5,110/130),'dao':(.5,140/170),'giao':(.5,250/330)}
def rot(v,a):
    c,s_=math.cos(math.radians(a)),math.sin(math.radians(a));return (v[0]*c-v[1]*s_,v[0]*s_+v[1]*c)
def seg(j,a,L): d=rot((0,L),a);return (j[0]+d[0],j[1]+d[1])
def walk(ph,amp=1.0):
    sp,cp=math.sin(ph),math.cos(ph)
    return dict(thF=-20*sp*amp,thB=20*sp*amp,knF=36*max(0,cp)*amp+4,knB=36*max(0,-cp)*amp+4,
                arF=20*sp*amp,faF=-22,arB=-20*sp*amp,faB=-22,lean=3*amp,head=1.5*math.sin(2*ph))
def dung(t):
    b=math.sin(t*1.7)
    return dict(thF=-7,thB=7,knF=4,knB=4,arF=6+2*b,faF=-22,arB=-6-2*b,faB=-20,lean=.8*b,head=1.2*math.sin(t*1.1))
def tron(p,q,u):
    return {k:p[k]+(q[k]-p[k])*u for k in p}
def ve(cv,c,key,x,ground,s,P,flip=False,vk=None,o=1.0):
    """vẽ một người: x là vị trí hông, ground là mặt đất; P là tư thế (dict góc)"""
    f=-1 if flip else 1;k=SC*s
    def W(v): return (x+f*v[0]*k,yh+v[1]*k)
    # chiều cao hông để bàn chân thấp nhất chạm đất
    def chan(hx,th,kn):
        kj=seg((hx,0),th,52);return kj,seg(kj,th+kn,55)
    feet=[chan(-8,P['thB'],P['knB'])[1][1],chan(8,P['thF'],P['knF'])[1][1]]
    yh=ground-max(feet)*k
    def part(name,j,a):
        ax,ay=PIV[name.split('_')[-1]]
        if flip: put(cv,c,Af(name),*W(j),s=s,r=-a,o=o,ax=1-ax,ay=ay)
        else: put(cv,c,name,*W(j),s=s,r=a,o=o,ax=ax,ay=ay)
    n=lambda p:f't19n_r_{key}_{p}'
    for hx,th,kn in ((-8,P['thB'],P['knB']),(8,P['thF'],P['knF'])):
        kj=seg((hx,0),th,52);part(n('legU'),(hx,0),th);part(n('legL'),kj,th+kn)
    sB=rot((-6,-78),P['lean']);sF=rot((10,-78),P['lean']);nk=rot((0,-94),P['lean'])
    eB=seg(sB,P['arB'],30);part(n('armU'),sB,P['arB']);part(n('armL'),eB,P['arB']+P['faB'])
    part(n('torso'),(0,0),P['lean']);part(n('head'),nk,P['lean']+P['head'])
    eF=seg(sF,P['arF'],30);aF=P['arF']+P['faF'];hand=seg(eF,aF,30)
    if vk:
        g=P.get('giuong',0);r0=10+.4*(aF+22)
        part(f't19n_r_{key}_{vk}',hand,r0+g*(aF+165-r0) if vk=='dao' else aF+55)
    part(n('armU'),sF,P['arF']);part(n('armL'),eF,aF)
class Nguoi:
    """người đi theo quãng đường: bước chân khớp với quãng đi, không trượt"""
    def __init__(s,key,s_,vk=None,buoc=118): s.key,s.s,s.vk,s.buoc=key,s_,vk,buoc
    def ve(s,cv,c,x,ground,t,dang_di,flip=False,P=None,o=1.0):
        if P is None:
            ph=abs(x)/(s.buoc*SC*s.s)*math.pi
            P=tron(dung(t),walk(ph),dang_di)
        ve(cv,c,s.key,x,ground,s.s,P,flip,s.vk,o)
