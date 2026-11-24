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
        if flip: put(cv,c,Af(name),*W(j),s=s,r=-a,o=o,ax=1-ax,ay=ay,scale_px=3)
        else: put(cv,c,name,*W(j),s=s,r=a,o=o,ax=ax,ay=ay,scale_px=3)
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

PRE={}  # tiền tố mảnh theo nhân vật: tm24 trở đi đăng ký PRE[key]='t24n_r_'
# ===== tm23: nhân vật theo bảng P23 (tên t23n_r_<key>_<mảnh>), vũ khí dùng chung t23n_r_w_<loại>, ngựa có khớp =====
def ve23(cv,c,key,x,ground,s,P,flip=False,vk=None,o=1.0,hip=None):
    """như ve() nhưng tên mảnh tm23; hip=(x,y) đặt hông cố định (người cưỡi ngựa), khi đó bỏ qua mặt đất"""
    f=-1 if flip else 1;k=SC*s
    def chan(hx,th,kn):
        kj=seg((hx,0),th,52);return kj,seg(kj,th+kn,55)
    if hip is None:
        feet=[chan(-8,P['thB'],P['knB'])[1][1],chan(8,P['thF'],P['knF'])[1][1]];yh=ground-max(feet)*k;xh=x
    else: xh,yh=hip
    def W(v): return (xh+f*v[0]*k,yh+v[1]*k)
    def part(name,j,a,pv):
        ax,ay=PIV[pv]
        if flip: put(cv,c,Af(name),*W(j),s=s,r=-a,o=o,ax=1-ax,ay=ay,scale_px=3)
        else: put(cv,c,name,*W(j),s=s,r=a,o=o,ax=ax,ay=ay,scale_px=3)
    n=lambda p:f'{PRE.get(key,"t23n_r_")}{key}_{p}'
    for hx,th,kn in ((-8,P['thB'],P['knB']),(8,P['thF'],P['knF'])):
        kj=seg((hx,0),th,52);part(n('legU'),(hx,0),th,'legU');part(n('legL'),kj,th+kn,'legL')
    sB=rot((-6,-78),P['lean']);sF=rot((10,-78),P['lean']);nk=rot((0,-94),P['lean'])
    eB=seg(sB,P['arB'],30);part(n('armU'),sB,P['arB'],'armU');aB=P['arB']+P['faB'];part(n('armL'),eB,aB,'armL')
    if P.get('vkB'): part(f"t23n_r_w_{P['vkB']}",seg(eB,aB,30),aB+P.get('vkBr',0),P['vkB'])
    part(n('torso'),(0,0),P['lean'],'torso');part(n('head'),nk,P['lean']+P['head'],'head23')
    eF=seg(sF,P['arF'],30);aF=P['arF']+P['faF'];hand=seg(eF,aF,30)
    if vk:
        g=P.get('giuong',0);r0=10+.4*(aF+22)
        r={'dao':r0+g*(aF+165-r0),'daocong':r0+g*(aF+165-r0),'giao':aF+55,'moc':aF+55,'cung':aF+90,'no':aF+90,'van':aF+90,'gay':aF+30,'gays':aF+30}[vk]+P.get('vkr',0)
        part(f't23n_r_w_{vk}',hand,r,vk)
    part(n('armU'),sF,P['arF'],'armU');part(n('armL'),eF,aF,'armL')
PIV.update({'gay':(.5,250/330),'gays':(.5,250/330),'head23':(.5,125/150),'daocong':(.5,140/170),'cung':(.5,110/220),'no':(45/150 if False else .5,45/90),'van':(.5,60/120),'moc':(.5,250/340)})
def ngoi(t):
    """tư thế ngồi trên ngựa/thuyền"""
    b=math.sin(t*1.7)
    return dict(thF=-70,thB=-62,knF=72,knB=70,arF=-20+2*b,faF=-30,arB=-10,faB=-30,lean=2+.8*b,head=1.2*math.sin(t*1.1))
def ngua(cv,c,mau,x,ground,s,ph,chay=1.0,flip=False,o=1.0,nguoi=None,P=None,vk=None,t=0):
    """ngựa có khớp; ph là pha bước; chay 0 đứng, 1 phi. nguoi=key người cưỡi"""
    f=-1 if flip else 1;k=SC*s
    bob=4*math.sin(2*ph)*chay
    yb=ground-(10+106)*k+bob*k
    def W(v): return (x+f*v[0]*k,yb+v[1]*k)
    def part(name,j,a,ax,ay):
        if flip: put(cv,c,Af(name),*W(j),s=s,r=-a,o=o,ax=1-ax,ay=ay,scale_px=3)
        else: put(cv,c,name,*W(j),s=s,r=a,o=o,ax=ax,ay=ay,scale_px=3)
    A=32*chay
    legs=[(50,10,A*math.sin(ph+math.pi)),(-58,10,-A*math.sin(ph+.6+math.pi))]
    for lx,ly,a in legs: part(f't23n_ngua_{mau}_chanS',(lx,ly),a,.5,12/140)
    part(f't23n_ngua_{mau}_than',(0,0),-1.5*math.sin(2*ph)*chay,180/380,150/280)
    if nguoi:
        PP=P or ngoi(t)
        ve23(cv,c,nguoi,0,0,s,PP,flip=flip,vk=vk,o=o,hip=W((-4,-56)))
    for lx,ly,a in [(64,10,A*math.sin(ph)),(-46,10,-A*math.sin(ph+.6))]: part(f't23n_ngua_{mau}_chan',(lx,ly),a,.5,12/140)
