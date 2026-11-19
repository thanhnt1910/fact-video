# Âm thanh tm12 (khớp cảnh dai_tm12.py)
from amchung import *
from sfx import _guard
import dai_tm12 as D
V=D.V;T,E,mid=V.T,V.E,V.mid;sb=D.sb
M=Mix(V.TOTAL,30)
wind(M,.2,V.TOTAL-.5,.12)
CH=[(0,T[4]-3,'bi',.8),(T[4],T[7],'mo',.9),(T[7],T[9],'cang',1.0),(T[9],T[18],'mo',.85),(T[18],T[22],'cang',1.0),(T[22],T[26],'mo',.85),(T[26],T[28],'bi',.9),(T[28],V.TOTAL-1,'trang',.8)]
for a,b,md,v in CH: music(M,a,b,md,v)
drop(M,.15,.8)
t0=T[4]-3.6;whoosh(M,t0-.4,1.0,.4);gong(M,t0+.1,.55);stamp(M,t0+1.1,.6)
wave_bed(M,0,E[3],.15)
march(M,sb(5,2),E[5],.3);drum(M,T[6],.5);shouts(M,mid(6,.3),1.5,.3)
wave_bed(M,T[7],E[7],.25);drum(M,sb(7,3),.6);shouts(M,sb(7,3)+.3,2.0,.35)
wave_bed(M,T[11],E[13],.2);oars(M,sb(13,1),E[13],.3,.8)
gong(M,mid(16,.1),.4);gong(M,mid(18,.1),.4)
drum(M,T[20],.6);shouts(M,mid(20,.3),2.0,.4);stamp(M,sb(20,2)+.3,.5)
gong(M,mid(22,.2),.4);drum(M,sb(23,2),.5)
drum(M,T[26],.6);shouts(M,mid(26,.2),1.5,.35);wave_bed(M,sb(26,2),E[26],.3)
gong(M,mid(27,.1),.4);gong(M,E[29]-.5,.4)
finish(M,V,'/tmp/gen/bd/out/am_tm12.wav')
