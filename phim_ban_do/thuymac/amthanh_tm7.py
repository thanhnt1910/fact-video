# Âm thanh tm7 (khớp cảnh dai_tm7.py)
from amchung import *
from sfx import _guard
import dai_tm7 as D
V=D.V;T,E,mid=V.T,V.E,V.mid
M=Mix(V.TOTAL,27)
wind(M,.2,V.TOTAL-.5,.12)
CH=[(0,T[5]-4,'cang',1.0),(T[5],T[8]-2.4,'mo',.9),(T[8],E[10],'loan',1.0),(T[11],E[14],'cang',.9),(T[15],E[18],'bi',.7),
    (T[19],E[21],'loan',1.0),(T[22],E[23],'cang',.8),(T[24],V.TOTAL-.5,'trang',.9)]
for a,b,md,v in CH: music(M,a,b,md,v)
drop(M,.15,.8);brush(M,.8,1.0,.3)
march(M,T[3],E[3],.3);brush(M,T[4]+.3,1,.3);stamp(M,mid(4,.75),.4)
t0=T[5]-3.6;whoosh(M,t0-.4,1.0,.4);gong(M,t0+.1,.55);stamp(M,t0+1.1,.6)
stamp(M,T[5]+.2,.5);stamp(M,mid(5,.6),.4);brush(M,mid(5,.3),1.5,.3)
for n in D.CARDS: whoosh(M,T[n]-2.6,1.0,.4);gong(M,T[n]-2.1,.45);brush(M,T[n]-2.2,.7,.35)
march(M,T[8],E[8],.35);steps(M,T[9],E[9],.3,.4)
battle(M,mid(10,.2),E[10],.9,8);hooves(M,mid(10,.2),2.5,.4)
march(M,T[11],E[11],.3)
fire=None
murm=_guard(lambda m,t0,d,g=.1: m.add((lp(m.nz(int(d*SR)),600)*.3).astype(np.float32),t0,g))
murm(M,T[12],E[12]-T[12],.15)
brush(M,T[13]+.3,2,.35);brush(M,mid(13,.5),2,.35)
cannon(M,T[14]+.5,.5)
# im lặng: chỉ gió nhẹ đoạn 15–18
steps(M,T[17],E[18],.15,.6)
horn(M,T[19]+.2,1.5,.5);battle(M,T[19]+.3,E[20],1.2,22)
for k in range(4): splash(M,mid(19,.6)+k*.3,.4)
thump(M,mid(21,.6)+.3,.5);thump(M,mid(21,.65)+.3,.5)
march(M,T[22],E[22],.35);war_drums(M,mid(22,.5),E[22],.3,.7)
gong(M,mid(23,.5),.45)
gong(M,mid(24,.5),.5)
finish(M,V,'/tmp/gen/bd/out/am_tm7.wav')
