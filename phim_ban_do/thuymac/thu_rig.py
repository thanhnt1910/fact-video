# Đoạn thử 10 giây: cùng cảnh, bản hiện tại (hình liền khối trượt) rồi bản múa rối (ghép mảnh có khớp).
import sys,math,subprocess,numpy as np
import dai_tm19 as D
from engine import put,text,put_screen,inn,band
from canh import Af,INK,RED,PAPER
import rig
T0=9.0
def nen(cv,t):
    c=D.kc(t,[(0,(900,560,1.0)),(T0,(1000,540,1.06))])
    D.ngoai(cv,c,t,g=880,seed=4);put(cv,c,'t19x_duonglam',960,560,s=1.0,o=.55)
    return c
def pos(t,x0,x1,a,b):
    u=min(1,max(0,(t-a)/(b-a)));u2=u*u*(3-2*u);return x0+(x1-x0)*u2,(0<u<1)
LINH=[(-260,560,.2,5.6),(-480,380,.4,5.8),(-700,200,.6,6.0)]
def cu(cv,t):
    c=nen(cv,t)
    for i,(x0,x1,a,b) in enumerate(LINH): D.di(cv,c,'t19n_1ta',x0,885+i*6,x1,885+i*6,t,a,b,s=.6,bob=4,f=6,ph=i)
    if t<5.6: D.di(cv,c,'t19n_ph',80,885,860,885,t,.0,5.0,s=.74,bob=4,f=5.5)
    else: put(cv,c,'t19n_ph2' if t>6.0 else 't19n_ph',860,885-2*math.sin(t*1.6),s=.74*D.GS,ay=1,scale_px=3)
    D.truoc(cv,c,t)
PH=rig.Nguoi('ph',1.15,'dao',buoc=60);TA=rig.Nguoi('ta',.83,'giao',buoc=60)
def moi(cv,t):
    c=nen(cv,t)
    for i,(x0,x1,a,b) in enumerate(LINH):
        x,dd=pos(t,x0,x1,a,b)
        ph=abs(x-x0)/(60*rig.SC*.83)*math.pi+i
        P=rig.tron(rig.dung(t+i),rig.walk(ph),1.0 if dd else 0)
        P['faF']=-55;P['arF']=8+3*math.sin(ph)
        rig.ve(cv,c,'ta',x,885+i*6,.83,P,vk='giao')
    x,dd=pos(t,80,860,0,5.0)
    ph=abs(x-80)/(60*rig.SC*1.15)*math.pi
    P=rig.tron(rig.dung(t),rig.walk(ph),1.0 if dd else 0)
    u=inn(t,5.8,1.0)
    if u>0: P['arF']=P['arF']+(-135-P['arF'])*u;P['faF']=P['faF']+(-25-P['faF'])*u;P['lean']+=2*u;P['head']-=6*u;P['giuong']=u
    rig.ve(cv,c,'ph',x,885,1.15,P,vk='dao')
    D.truoc(cv,c,t)
def frame(t):
    cv=D.PAP.copy()
    if t<T0: cu(cv,t);lab='HIỆN TẠI: hình liền khối trượt'
    else: moi(cv,t-T0);lab='MÚA RỐI: tay chân có khớp'
    put_screen(cv,band(760,90,PAPER,.88,20),960,120);put_screen(cv,text(lab,44,RED,700),960,118)
    return cv
if __name__=='__main__':
    out=sys.argv[1];N=int(2*T0*24)
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    for i in range(N):
        fr=frame(i/24);fr=fr if fr.dtype==np.uint8 else (np.clip(fr,0,1)*255+.5).astype(np.uint8)
        p.stdin.write(fr.tobytes())
    p.stdin.close();p.wait()
