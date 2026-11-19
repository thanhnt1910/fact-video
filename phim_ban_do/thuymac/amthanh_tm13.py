# Âm thanh tm13 (khớp cảnh dai_tm13.py)
from amchung import *
from sfx import _guard
import dai_tm13 as D
V=D.V;T,E,mid=V.T,V.E,V.mid;sb=D.sb
M=Mix(V.TOTAL,30)
wind(M,.2,V.TOTAL-.5,.12)
CH=[(0,T[3],'cang',1.0),(T[3],T[4]-3,'bi',.8),(T[4],T[7],'mo',.9),(T[7],T[11],'cang',1.0),(T[11],T[13],'bi',.9),(T[13],V.TOTAL-1,'trang',.8)]
for a,b,md,v in CH: music(M,a,b,md,v)
drop(M,.15,.8)
murm=_guard(lambda m,t0,d,g=.1: m.add((lp(m.nz(int(d*SR)),600)*.3).astype(np.float32),t0,g))
t0=T[4]-3.6;whoosh(M,t0-.4,1.0,.4);gong(M,t0+.1,.55);stamp(M,t0+1.1,.6)
brush(M,mid(1,.5),1.0,.3);brush(M,mid(2,.6),1.2,.3);drum(M,mid(5,.5),.6);shouts(M,mid(5,.6),1.5,.35)
murm(M,T[6],E[6]-T[6],.15);gong(M,mid(7,.5),.4)
march(M,T[8],sb(8,1),.3);oars(M,sb(8,1),sb(8,2),.3,.8)
wave_bed(M,sb(8,1),sb(8,2),.2)
drum(M,T[9],.6);shouts(M,mid(9,.2),2.0,.4);stamp(M,sb(9,1)+.3,.6);gong(M,sb(9,3),.5)
murm(M,T[10],E[10]-T[10],.12);gong(M,mid(11,.9),.5)
gong(M,mid(12,.1),.4);stamp(M,mid(13,.3),.5);drum(M,mid(13,.6),.4);gong(M,mid(14,.9),.4)
finish(M,V,'/tmp/gen/bd/out/am_tm13.wav')
