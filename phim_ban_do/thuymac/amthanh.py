import sys
from sfx import *
which=sys.argv[1]
if which=='dai':
    import dai as V;T,E=V.T,V.E;M=Mix(V.TOTAL)
    # nền
    for a,b in [(0,V.T[5]-.4),(V.T[17]-.3,V.T[21]-1),(V.T[26]-.6,V.T[35]-.3),(V.T[36]-.3,V.T[37]),(V.T[43]-.3,V.T[45])]: wave_bed(M,a,b,.35)
    wind(M,0,V.TOTAL,.12)
    gulls(M,0,T[4],.15);gulls(M,T[36],T[37],.15);gulls(M,T[45],V.TOTAL,.12)
    drop(M,0.05,.9);oars(M,1,T[4],.18,1.3,.4)
    # thẻ tựa, thẻ chương
    tt=T[5]-3.3;thump(M,tt,.9);gong(M,tt+.3,.7);brush(M,tt+.2,.9,.4)
    for n in V.CARDS: whoosh(M,T[n]-2.4,1.0,.4);gong(M,T[n]-1.9,.45);brush(M,T[n]-2.0,.7,.35)
    # triện
    for ts in [T[2]+2.2,T[5]+.6,T[7]+.3,T[9]+.2,T[37]+.6,T[42]+2.5,T[45]+1.6,T[34]+.4,T[5]-3.3+1.1]: stamp(M,ts,.7)
    # nét cọ trên bản đồ
    for ts in [T[5]-1,T[7]+.6,T[9]+1,T[10]+.4,T[12]+.6,T[12]+2.4,T[14]+1.3,T[15],T[35]+1.6,T[39]-.3,T[40]-.2,T[42]+.3]: brush(M,ts,1.0,.32,M.rng.uniform(-.4,.4))
    # bàn kế
    for k in range(3): brush(M,T[18]+1.6+2*k,.6,.3)
    brush(M,T[19]+2.6,.8,.35);drum(M,T[19]+2.6,.5)
    # mặt cắt: thủy triều, đóng cọc
    tide(M,T[22],2.2,.45,True);tide(M,T[22]+3.6,3.8,.45,False)
    for i,xx in enumerate(range(480,1460,44)): stake_hit(M,T[23]+1.2+i*.09+.45,.5)
    tide(M,T[24],2.4,.45,True);oars(M,T[25],E[25],.25,.7)
    # trận đánh
    war_drums(M,T[26],T[31],.28,.9);oars(M,T[26],E[29],.22,.9,.3)
    horn(M,T[28]+.2,1.8,.4);oars(M,T[28],T[28]+6.5,.3,.55,-.4)
    tide(M,T[30]+.2,E[32]-T[30],.6,False)
    horn(M,T[31]-.2,2.2,.55);war_drums(M,T[31],E[34],.6,.5);shouts(M,T[31],E[32]-T[31]+1,.5)
    volley(M,T[31]+.4,E[31]+1,16,.35);volley(M,T[32],E[32],10,.3);clangs(M,T[31]+1,E[33],3,.3)
    for i in range(6): woodcrack(M,V.capt_time(i)+.1,.7,(V.BX0[i]-1100)/900)
    stamp(M,E[34]-1.2,.3);whoosh(M,E[34]-1.1,1.0,.3)
    oars(M,T[35]+1.6,E[35],.2,1.1)
    # sau trận
    gong(M,T[37]+.6,.5);lap(M,T[36],T[37],.2);lap(M,T[43],T[45],.2);creak(M,T[43]+1,1.6,.25)
    # nhạc
    for a,b,md,v in [(0,T[5]-.4,'cang',.9),(T[5]-.4,T[14]-2,'mo',.8),(T[14]-2,T[21]-2,'binh',.8),(T[21]-2,T[26]-2,'mo',.8),(T[26]-2,T[31],'cang',.9),
                     (T[31],T[35]-.3,'loan',.7),(T[35]-.3,T[37]-2,'bi',.8),(T[37]-2,V.TOTAL-1,'trang',.9)]: music(M,a,b,md,v)
    write(M,'/tmp/gen/bd/out/am_dai.wav',V.TOTAL)
else:
    import doc as V;T,E=V.T,V.E;M=Mix(V.TOTAL,9)
    wave_bed(M,0,T[4]-.3,.35);wave_bed(M,T[5]+3,T[8],.35);wind(M,0,V.TOTAL,.12);gulls(M,0,T[4],.15)
    drop(M,.05,.9);oars(M,1,T[4],.18,1.3,.4)
    stamp(M,T[2]+2.0,.75);brush(M,.3,.9,.35)
    for i in range(23): stake_hit(M,T[4]+1.0+i*.11+.45,.5)
    brush(M,T[4]+1.6,.8,.3);tide(M,T[5]+.1,2.0,.45,True);brush(M,T[5]+.8,.8,.3)
    horn(M,T[5]+3.4,1.6,.4);oars(M,T[5]+3.4,T[6]+2,.28,.55,-.3);war_drums(M,T[5]+3,T[7],.3,.8)
    tide(M,T[6]+2.6,2.6,.6,False);brush(M,T[6]+2.8,.8,.3)
    horn(M,T[7]-.3,2,.5);war_drums(M,T[7],E[7],.6,.45);shouts(M,T[7],E[7]-T[7],.5);volley(M,T[7],E[7]-1,12,.35);clangs(M,T[7]+.5,E[7],3,.3)
    for i in range(6): woodcrack(M,V.ctime(i)+.1,.7,(V.BX0[i]-1100)/900)
    stamp(M,E[7]-2.6,.6);whoosh(M,E[7]-1.0,1.0,.3)
    stamp(M,T[8]+.3,.7);gong(M,T[8]+.3,.45);brush(M,T[8]+1.4,1.0,.3)
    stamp(M,T[9]+1.4,.7);gong(M,T[9]+3.2,.5);brush(M,T[9]+3.2,.8,.35)
    for a,b,md,v in [(0,T[4]-.3,'cang',.9),(T[4]-.3,T[5]+3,'mo',.8),(T[5]+3,T[7],'cang',.9),(T[7],T[8]-.3,'loan',.7),(T[8]-.3,V.TOTAL-1,'trang',.9)]: music(M,a,b,md,v)
    write(M,'/tmp/gen/bd/out/am_doc.wav',V.TOTAL)
print('ok')
