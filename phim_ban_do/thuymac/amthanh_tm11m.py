# Âm thanh tm11m (khớp cảnh dai_tm11m.py)
from amchung import *
from sfx import _guard
import dai_tm11m as D
V=D.V;T,E,mid=V.T,V.E,V.mid
M=Mix(V.TOTAL,30)
wind(M,.2,V.TOTAL-.5,.12)
CH=[(0,T[2]-4,'cang',1.0),(T[2],T[6]-2.4,'mo',.9),(T[6],E[8],'cang',.9),(T[9],E[10],'bi',.8),
    (T[11],E[12],'cang',1.0),(T[13],E[14],'trang',.9)]
for a,b,md,v in CH: music(M,a,b,md,v)
drop(M,.15,.8)
murm=_guard(lambda m,t0,d,g=.1: m.add((lp(m.nz(int(d*SR)),600)*.3).astype(np.float32),t0,g))
murm(M,.3,E[1],.15)
t0=T[2]-3.6;whoosh(M,t0-.4,1.0,.4);gong(M,t0+.1,.55);stamp(M,t0+1.1,.6)
brush(M,mid(2,.5),1.2,.3);brush(M,mid(4,.55),1,.3);march(M,T[5],E[5],.25)
for n in D.CARDS: whoosh(M,T[n]-2.6,1.0,.4);gong(M,T[n]-2.1,.45);brush(M,T[n]-2.2,.7,.35)
march(M,T[7],E[7],.3);drum(M,mid(7,.6),.5)
shouts(M,mid(8,.6),2.0,.4);drum(M,mid(8,.6),.6);stamp(M,mid(8,.8),.5)
gong(M,mid(9,.4),.35);murm(M,T[10],E[10]-T[10],.15)
gong(M,mid(11,.45),.6);drum(M,mid(11,.5),.5);stamp(M,mid(12,.5),.5)
wave_bed(M,T[13],E[13],.3);oars(M,T[13],E[13],.3,.8)
drum(M,mid(13,.6),.5);gong(M,mid(14,.5),.4)
finish(M,V,'/tmp/gen/bd/out/am_tm11m.wav')
