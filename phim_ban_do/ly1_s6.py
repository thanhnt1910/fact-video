"""Cảnh dời đô: thuyền chân thực hơn (mũi cong, mui, chèo, người ngồi) và đoàn người di chuyển."""
from ly1_anim import *
from ly1_s3 import SKY_DEF,palace
from ly1_s4 import wall_seg
import ly1_scenes as _S
_P=_S.person
def boat2(x,y,t,s=1.0,p=0.0,face=1,king=False,rowers=2,flagc='#c0392b',moving=1.0,col1='#8a5a30',col2='#6a4220'):
    """Thuyền gỗ nhìn ngang. (x,y) = giữa thân ở mực nước. moving: 0..1 độ mạnh của chèo."""
    rk=2.2*math.sin(t*1.3+p);dy=2.2*math.sin(t*1.8+p)
    g=f'<g transform="translate({x:.1f},{y+dy:.1f}) rotate({rk:.2f}) scale({s*face},{s})" stroke-linejoin="round" stroke-linecap="round">'
    # chèo (sau thân thuyền, phía xa)
    sw=0.5+0.35*math.sin(t*2.4+p)
    rx=[-95,-20,60,115][:max(rowers,0)] if rowers<=4 else [-95,-20,60,115]
    rx=[-90,70,-10,115][:rowers]
    # mui thuyền (vua) hoặc mái che dân
    if king:
        g+=(f'<g stroke="{OUT}" stroke-width="3"><path d="M-62,-30 V-112 M52,-30 V-112" stroke="#5a3a1c" stroke-width="7" fill="none"/>'
            f'<path d="M-84,-108 Q-4,-176 78,-108 L68,-96 Q-4,-146 -74,-96Z" fill="#b3261e"/><path d="M-84,-108 Q-4,-176 78,-108" stroke="#e8c36a" stroke-width="5" fill="none"/>'
            + ''.join(f'<path d="M{xx},{-100+abs(xx+4)*-0.0 } v14" stroke="#e8c36a" stroke-width="3"/>' for xx in range(-70,74,18))+'</g>')
    # người ngồi / chèo (vẽ trước phần mạn trước để bị che nửa thân)
    ppl=''
    if king:
        ppl+=_P(-4,-14,0.5*PGAIN,robe='#f2c94c',trim='#fff2a8',hat='crown',hands='hold',pose='kneel')
    for i,px in enumerate(rx):
        lean=16*math.sin(t*2.4+p+i*.4)*moving
        ppl+=_P(px,-12,0.4*PGAIN,robe=['#6a8a5a','#7a5a3a','#5a6a8a','#8a5a5a'][(i+int(p*3))%4],hat='cap' if i%2==0 else 'bun',hands='hold',ang=lean-6,face=1 if i%2==0 else -1)
    # chèo
    oars=''
    for i,px in enumerate(rx):
        a=sw+i*.15;hx=px;hy=-44
        ex=px-110*math.sin(a);ey=-30+88*math.cos(a)
        bx=ex-18*math.sin(a);by=ey+18*math.cos(a)
        oars+=(f'<path d="M{px+22*math.sin(a):.1f},{hy-14*math.cos(a):.1f} L{bx:.1f},{by:.1f}" stroke="#4a2c14" stroke-width="6" fill="none"/>'
               f'<path d="M{ex:.1f},{ey:.1f} L{bx:.1f},{by:.1f}" stroke="{OUT}" stroke-width="3" fill="none"/>'
               f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="7" ry="18" transform="rotate({-a*57:.0f} {bx:.1f} {by:.1f})" fill="#6a4220" stroke="{OUT}" stroke-width="2.5"/>')
    # thân thuyền: mũi và đuôi cong vút, mạn trước phủ nửa người
    hull_back=f'<path d="M-150,-52 Q-140,-12 -96,8 L84,8 Q140,-10 156,-62 Q150,-30 120,-26 L-110,-26 Q-140,-26 -150,-52Z" fill="{col2}" stroke="{OUT}" stroke-width="3.5"/>'
    hull_front=(f'<path d="M-150,-52 Q-136,-14 -96,10 L84,10 Q140,-8 156,-62 Q144,-34 112,-30 L-104,-30 Q-138,-30 -150,-52Z" fill="{col1}" stroke="{OUT}" stroke-width="3.5"/>'
                f'<path d="M-120,-28 Q-100,2 -60,6 M-60,-28 V6 M0,-28 V8 M60,-28 V6 M110,-28 Q100,0 70,6" stroke="{col2}" stroke-width="2.5" fill="none"/>'
                f'<path d="M-146,-48 Q-100,-36 0,-34 Q100,-36 152,-58" stroke="#e8c36a" stroke-width="4" fill="none"/>'
                f'<path d="M156,-62 q10,-14 4,-30" stroke="{OUT}" stroke-width="4" fill="none"/>')
    # cờ nhỏ ở mũi thuyền
    fl=''
    if king:
        wv=6*math.sin(t*5+p)
        fl=(f'<path d="M-134,-52 V-140" stroke="#3a2210" stroke-width="5"/><path d="M-134,-138 q{22+wv:.0f},-6 {44+wv*1.4:.0f},{4+wv*.4:.0f} q{-14-wv*.5:.0f},10 {-44-wv*1.4:.0f},{16:.0f}Z" fill="{flagc}" stroke="{OUT}" stroke-width="2.5"/>')
    return g+hull_back+oars+ppl+hull_front+fl+'</g>'
def ripples(x,y,t,w=380,n=3,p=0.0):
    o=''
    for i in range(n):
        k=((t*.5)+i/n+p)%1;r=w*(.42+.5*k)
        o+=f'<ellipse cx="{x:.0f}" cy="{y+6:.0f}" rx="{r:.0f}" ry="{r*.09:.0f}" fill="none" stroke="#fff" stroke-width="2.2" opacity="{.38*(1-k):.2f}"/>'
    return o
def _bg_dusk():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skydusk)"/>'
    bg+=hill([(-400,600),(300,540),(900,590),(1500,530),(2000,590)],'#3a3050')
    bg+=karst(1450,600,330,250,'#3c3454','#4a4264')+karst(1750,610,280,200,'#3c3454','#4a4264')+karst(1180,610,200,130,'#443c5c','#524a6c')
    bg+='<rect x="-400" y="720" width="2400" height="500" fill="#2a2438"/><path d="M-400,800 Q500,760 1000,810 T2000,790 L2000,1100 L-400,1100Z" fill="#3a5a8a"/>'
    bg+=wall_seg(420,1180,560,740,'#9a8660')+''.join(f'<rect x="{x}" y="538" width="36" height="24" fill="#9a8660" stroke="{OUT}" stroke-width="3"/>' for x in range(420,1180,76))+palace(800,560,260,120,'#7a2a1c','#b09468')
    return bg
def _convoy(t,xk,y,pw=1.0,moving=1.0,idle=False):
    """thuyền vua + 2 thuyền theo sau"""
    o=''
    o+=boat2(xk+690,y-12,t,.95,p=2.1,rowers=2,moving=moving,flagc='#2e7d4f')
    o+=boat2(xk+350,y+6,t,1.05,p=1.1,rowers=3,moving=moving,flagc='#d4a017')
    o+=boat2(xk,y+14,t,1.15,p=0.0,king=True,rowers=2,moving=moving)
    return o
def _walkers(t,u,n=8):
    o='';r=random.Random(11)
    cols=['#8a5a3a','#5a7a4a','#7a5a8a','#a06a3a','#4a6a8a','#8a4a4a']
    for i in range(n):
        x0=1150+i*150+r.uniform(-30,30);spd=360+r.uniform(-30,30)
        x=x0-(t*spd*.62)%1;x=x0-t*95-u*0
        y=752+r.uniform(-6,8);s=.32+.03*r.uniform(-1,1)
        if x<-300 or x>1900: continue
        o+=_P(x,y,s*PGAIN,robe=cols[i%6],hat='cap' if i%3 else 'bun',hands='hold',face=-1,ang=0) if False else P(x,y,s,t,'walk',p=i*1.7,robe=cols[i%6],hat='cap' if i%3 else 'bun',hands='hold',face=-1)
        if i%2==0: o+=f'<path d="M{x-26:.0f},{y-80*s*2.2:.0f} L{x+22:.0f},{y-60*s*2.2:.0f}" stroke="#4a2c14" stroke-width="4"/><ellipse cx="{x-26:.0f}" cy="{y-80*s*2.2+8:.0f}" rx="12" ry="9" fill="#a88a4a" stroke="{OUT}" stroke-width="2"/>'
    return o
@scene('doan_di')
def _():
    bg=_bg_dusk()
    def fg(t,u,ms):
        T=ms[-1]
        o=stars(t,26,5,300)
        o+=birds(t,180,4,3,38,'#2a2438')
        o+=_walkers(t,u)
        k=sstep(t,0.1,T-0.5);xk=lerp(1500,520,k);mv=1.0-0.8*sstep(t,T-1.6,T-0.3)
        for dx,yy in ((0,830),(350,836),(690,818)):
            o+=ripples(xk+dx,yy+12,t,260,3,dx*.001)
        o+=_convoy(t,xk,820,moving=mv)
        o+=wave_band(862,t,6,'#2e4a7a',-300,1900,.018,1.3,1200)
        o+=f'<path d="M-400,820 Q500,800 1000,830" stroke="#fff" stroke-width="2" opacity=".2" fill="none"/>'
        return o
    return bg,fg,lambda u,t:(lerp(1180,800,ease(u)),520,1.2)
@scene('rong_vang')
def _():
    bg=_bg_dusk()
    def fg(t,u,ms):
        o=stars(t,30,5,300)
        rise=sstep(t,.8,ms[-1]*.65)
        y=lerp(840,260,rise);x=lerp(1060,920,rise)
        from ly1_s4 import dragon_img
        o+=glow(x,y,260,t,0,op=.6*rise)+dragon_img(x,y,t,lerp(200,480,rise),rot=lerp(0,-4,rise)+3*math.sin(t*1.2),op=sstep(t,.5,1.5),spd=6)
        o+=sparks(t,x,y,20,4,260)
        o+=ripples(520,832,t,260,3)+ripples(870,838,t,260,3,.3)+ripples(1210,830,t,260,3,.6)
        o+=_convoy(t,520,820,moving=0.0)
        o+=wave_band(862,t,6,'#2e4a7a',-300,1900,.018,1.3,1200)
        return o
    return bg,fg,lambda u,t:(lerp(800,860,u),520,lerp(1.2,1.0,ease(u)))
