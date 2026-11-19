# Âm thanh tm16 (khớp cảnh dai_tm16.py)
from amchung import *
from sfx import _guard
import dai_tm16 as D
V=D.V;T,E,mid=V.T,V.E,V.mid;sb=D.sb
M=Mix(V.TOTAL,30)
wind(M,.2,V.TOTAL-.5,.12)
CH=[(0,T[4],'cang',.9),(T[4],T[8],'bi',.8),(T[8],T[12],'mo',.9),(T[12],T[15],'cang',1.0),(T[15],V.TOTAL-1,'trang',.8)]
for a,b,md,v in CH: music(M,a,b,md,v)
drop(M,.15,.8)
murm=_guard(lambda m,t0,d,g=.1: m.add((lp(m.nz(int(d*SR)),600)*.3).astype(np.float32),t0,g))
t0=T[4]-3.6;whoosh(M,t0-.4,1.0,.4);gong(M,t0+.1,.55);stamp(M,t0+1.1,.6)
drum(M,mid(2,.6),.5);shouts(M,mid(2,.7),1.2,.3)
brush(M,mid(3,.5),1.0,.3);march(M,T[5],sb(5,1),.25);gong(M,sb(5,1)+.3,.4)
brush(M,mid(6,.5),1.2,.3);brush(M,mid(7,.5),1.0,.3)
drum(M,T[8],.6);shouts(M,mid(8,.2),2.0,.35)
murm(M,T[10],E[10]-T[10],.15);murm(M,T[11],E[11]-T[11],.1)
gong(M,T[12]+.3,.5);drum(M,T[13],.6);shouts(M,mid(13,.3),2.0,.4);stamp(M,mid(13,.6),.5)
drum(M,T[14],.5);shouts(M,mid(14,.1),1.6,.3);gong(M,sb(14,1)+.3,.4)
gong(M,mid(15,.5),.4);gong(M,mid(16,.1),.4);brush(M,mid(18,.5),1.0,.3);gong(M,mid(22,.1),.4)
finish(M,V,'/tmp/gen/bd/out/am_tm16.wav')
