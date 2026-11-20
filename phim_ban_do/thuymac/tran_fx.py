# Hiệu ứng giao chiến cho cảnh thủy mặc (chủ kênh 19/11/2026: cảnh đánh nhau phải thấy đánh nhau, hai quân khác màu)
import math,random
from engine import put,inn,cl
from fx_tran import arrows,dust,sparks,fall
BACC=(.17,.29,.45);LYCC=(.69,.5,.13);VIETC=(.69,.16,.11)
MAU={'bac':BACC,'viet':VIETC,'ly':LYCC,'ngo':BACC,'cc':VIETC,'han':BACC,'trung':VIETC}
def clash(cv,c,t,a,b,L,R,xm=960,y=860,s=.9,push=0,seed=1,ten=True,thua=None,pre='t12_spr_'):
    """Hai hàng quân L (bên trái) và R (bên phải) lao vào nhau rồi giáp trận ở xm.
    push=+1: bên trái đẩy bên phải lùi dần; -1 ngược lại. thua: bên bị ngã nhiều ('L'/'R'), mặc định bên bị đẩy."""
    if t<a-.2: return
    u=inn(t,a,1.4);d=(1-u)*520
    sh=push*cl((t-a-1.4)/max(b-a-1.4,.1))*260+14*math.sin(t*3.3)
    xc=xm+sh;w=370*s
    put(cv,c,f'{pre}{L}',xc-w-d,y,s=s,o=.97);put(cv,c,f'{pre}{R}',xc+w+d,y,s=s,o=.97)
    put(cv,c,f'{pre}{L}',xc-w-d-260*s,y+40,s=s*.85,o=.85);put(cv,c,f'{pre}{R}',xc+w+d+260*s,y+40,s=s*.85,o=.85)
    if u>.9:
        pts=[(xc+(-30+60*k/4),y-120*s-30*math.sin(k*1.7)) for k in range(5)]
        sparks(cv,c,t,pts,a+1.3,b+.3,seed=seed)
        for k in range(3): dust(cv,c,xc-80+k*80,y-40,o=.25+.1*math.sin(t*2+k),s=.35)
        thua=thua or ('R' if push>0 else 'L' if push<0 else None)
        R0=random.Random(seed)
        for k in range(int((b-a)/1.1)+1):
            t0=a+1.6+k*1.1
            if t0<t<t0+1.8:
                side=thua or ('L' if k%2 else 'R')
                img=pre+'1'+(R if side=='R' else L);dx=(1 if side=='R' else -1)
                fall(cv,c,img,xc+dx*(40+R0.random()*120),y,t,t0,s=s*.9,dirn=dx)
    if ten:
        arrows(cv,c,t,a+.3,b,[(xc-w-d-300,y-260),(xc-w-d-200,y-250)],[(xc+w*.6+d,y-90),(xc+w+d,y-80)],n=7,h=110,per=1.1,seed=seed,col=MAU[L])
        arrows(cv,c,t,a+.8,b,[(xc+w+d+300,y-260),(xc+w+d+200,y-250)],[(xc-w*.6-d,y-90),(xc-w-d,y-80)],n=5,h=110,per=1.2,seed=seed+9,col=MAU[R])
