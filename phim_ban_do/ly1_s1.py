"""Cảnh động chương 1–2 (dòng 2–26)."""
from ly1_anim import *
import ly1_anim as A
from ly1_scenes import lamp as _lampS
NIGHT_DEF='<defs><linearGradient id="skyn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1030"/><stop offset="1" stop-color="#2c3a68"/></linearGradient><linearGradient id="skyd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fb8e8"/><stop offset="1" stop-color="#f4e6c0"/></linearGradient></defs>'
def mv(t,t0,t1,x0,x1): return lerp(x0,x1,sstep(t,t0,t1))
def throne_back(x,y,gold='#d9a441',k=1.0):
    return (f'<g transform="translate({x},{y}) scale({k}) translate({-x},{-y})" stroke="{OUT}" stroke-width="3"><rect x="{x-110}" y="{y-330}" width="220" height="330" rx="18" fill="#8f2d22"/><rect x="{x-90}" y="{y-310}" width="180" height="290" rx="12" fill="#a8261c"/>'
            f'<circle cx="{x}" cy="{y-230}" r="40" fill="{gold}"/><path d="M{x-120},{y-330} Q{x},{y-380} {x+120},{y-330}Z" fill="{gold}"/></g>')
def throne_front(x,y,gold='#d9a441',k=1.0):
    return (f'<g transform="translate({x},{y}) scale({k}) translate({-x},{-y})" stroke="{OUT}" stroke-width="3"><rect x="{x-100}" y="{y-96}" width="200" height="96" rx="8" fill="#b8942a"/><rect x="{x-112}" y="{y-110}" width="224" height="24" rx="8" fill="{gold}"/>'
            f'<rect x="{x-120}" y="{y-12}" width="240" height="22" fill="#6a1a12"/></g>')
@scene('co_phap_dem')
def _():
    bg=NIGHT_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skyn)"/>'
    bg+='<circle cx="1230" cy="150" r="58" fill="#f6f0cf"/><circle cx="1212" cy="140" r="52" fill="#fffbe0" opacity=".5"/>'
    bg+=hill([(-400,560),(100,470),(420,520),(760,450),(1100,500),(1500,440),(2000,520)],'#1a2a3e')
    bg+=hill([(-400,660),(200,600),(560,640),(980,590),(1400,640),(2000,600)],'#223a4a',1100)
    bg+='<rect x="-400" y="700" width="2400" height="500" fill="#2e4630"/><path d="M-400,760 Q400,730 800,770 T2000,760 L2000,800 L-400,800Z" fill="#3a5a3a"/>'
    bg+='<path d="M600,900 Q760,800 840,730" fill="none" stroke="#6a5a3a" stroke-width="46" stroke-linecap="round" opacity=".75"/>'
    for x,y,s in [(220,760,.95),(470,720,.7),(1130,730,.75),(1330,780,1.0),(1560,740,.8)]: bg+=house(x,y,s,roof='#4a3a28',wall='#6a5a48')
    bg+=house(820,740,1.25,roof='#5a4228',wall='#8a7452')
    for x,y,s in [(60,790,1.2),(980,800,1.1),(1440,820,1.3)]: bg+=tree(x,y,s,0,x,leaf='#274a30',trunk='#3a2a1c')
    def fg(t,u,ms):
        o=stars(t,50,3,300)
        for x,y,s,p in [(220,760,.95,0),(470,720,.7,1),(1130,730,.75,2),(1330,780,1.0,3),(1560,740,.8,4)]:
            o+=f'<circle cx="{x}" cy="{y-36*s}" r="{36*s}" fill="url(#fl)" opacity=".55"/><rect x="{x-14*s}" y="{y-58*s}" width="{28*s}" height="{26*s}" fill="#ffd27a" opacity="{.75+.2*math.sin(t*7+p):.2f}"/>'
        o+=glow(820,700,150,t,0,op=.8)+f'<rect x="{820-18}" y="{740-84}" width="36" height="40" fill="#ffe28a" opacity="{.8+.15*math.sin(t*6):.2f}"/>'
        # vương miện vàng mờ bay lên (chuyện mai sau)
        a=sstep(t,ms[1]*0+0.4,ms[1]+1.0)*(1-sstep(t,ms[2]-0.2,ms[2]+1.2))
        if a>0:
            cy=500-60*seg(t,0.4,ms[2]+1.0)
            o+=f'<g transform="translate(820,{cy:.0f}) scale(1.6)" opacity="{a*.75:.2f}" stroke="#fff3a8" stroke-width="2"><path d="M-30,10 L-30,-26 L-14,-8 L0,-34 L14,-8 L30,-26 L30,10Z" fill="#f2c94c"/><rect x="-30" y="6" width="60" height="10" fill="#d4a017"/></g>'
            o+=sparks(t,820,cy,16,5,90)
        # đom đóm
        o+=dust(t,100,1500,420,820,26,9,'#f4f08a',.8)
        o+=smoke(1330,690,t,5,'#9aa6b8',110,.25,8,10,.35)
        return o
    return bg,fg,lambda u,t:(820-60*(1-u),500,1.0+.22*u)
@scene('chua_don')
def _():
    bg=NIGHT_DEF.replace('skyn','sk')+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skyd)"/>'
    bg+=hill([(-400,520),(200,430),(520,500),(900,420),(1300,490),(1700,430),(2100,500)],'#7fa37a')
    bg+=hill([(-400,600),(300,560),(700,600),(1200,550),(2100,600)],'#8cba6a',1100)
    bg+='<rect x="-400" y="720" width="2400" height="500" fill="#98c46a"/><path d="M-400,790 Q500,760 1000,800 T2000,790 L2000,860 L-400,860Z" fill="#a98c5a"/>'
    bg+=pagoda(1290,720,1.25)
    bg+='<g stroke="#2a1608" stroke-width="3"><rect x="1120" y="700" width="30" height="100" fill="#8f2d22"/><rect x="1430" y="700" width="30" height="100" fill="#8f2d22"/><path d="M1100,704 Q1290,640 1480,704 L1470,722 Q1290,670 1110,722Z" fill="#5a3a2a"/></g>'
    for x,y,s in [(120,790,1.5),(520,770,1.2),(900,780,1.4)]: bg+=tree(x,y,s,0,x)
    def fg(t,u,ms):
        o=clouds(t,110,4,'#fff',.9,10,3)+birds(t,230,4,2,40)
        for x,y,s in [(120,790,1.5),(520,770,1.2),(900,780,1.4)]: o+=tree(x,y,s,t,x*.01,leaf='#4c8a3a')
        x=mv(t,0.3,ms[-1]-1.2,150,1020);mode='walk' if t>0.3 and t<ms[-1]-1.2 else 'idle'
        o+=P(x+90,790,.55,t,mode,p=1.2,robe='#c7a95e',trim='#e8d9a0',hat='bun',hands='sleeve')
        o+=P(x,800,.95,t,mode,p=0,robe='#7a5a3a',trim='#d9c18a',hat='bun',hands='sleeve')
        # sư đứng chờ ở cổng
        o+=P(1290,790,.9,t,'idle',robe='#d98a2a',trim='#f2c94c',hat='bald',hands='sleeve',face=-1)
        return o
    return bg,fg,lambda u,t:(lerp(560,1060,ease(u)),500,1.2)
@scene('chua_luc_to')
def _():
    bg='<rect x="-400" y="-300" width="2400" height="1700" fill="#bcd6c0"/>'+hill([(-400,430),(300,360),(700,420),(1100,350),(1600,410),(2100,370)],'#7fa37a')
    bg+='<rect x="-400" y="700" width="2400" height="500" fill="#b99a64"/>'
    bg+=pagoda(800,720,1.6,4)
    bg+='<g stroke="#2a1608" stroke-width="3"><rect x="1210" y="650" width="120" height="110" rx="10" fill="#6a5a48"/><rect x="1196" y="636" width="148" height="22" fill="#8a7a62"/></g>'
    for x,y,s in [(130,800,1.7),(1500,810,1.6)]: bg+=tree(x,y,s,0,x)
    def fg(t,u,ms):
        o=clouds(t,100,3,'#fff',.8,8,5)+birds(t,200,3,4,50)
        for x,y,s in [(130,800,1.7),(1500,810,1.6)]: o+=tree(x,y,s,t,x*.02)
        o+=smoke(1270,640,t,7,'#e8e8e8',200,.3,10,32,.6)+glow(1270,690,50,t,0,op=.5)+flame(1270,700,t,.35)
        d=0.9
        # dòng 0: cậu bé cúi chào; dòng 1: thầy nói; dòng 2: cậu đứng thẳng nhìn xa
        bow=34*math.sin(clamp(seg(t,0.4,ms[1]*0.6)*3.14159)) if t<ms[1] else 0
        o+=P(560,800,0.7,t,'still',robe='#4a6a9a',trim='#cfe0f0',hat='bun',pose='bow',ang=bow,hands='sleeve')if t<ms[1] else P(560,800,0.7,t,'idle',robe='#4a6a9a',trim='#cfe0f0',hat='bun',hands='sleeve',face=1 if t<ms[2] else -1)
        o+=P(780,795,1.0,t,'talk' if ms[1]<t<ms[2] else 'idle',robe='#d98a2a',trim='#f2c94c',hat='bald',hands='sleeve',face=-1)
        if ms[1]+0.8<t<ms[2]+0.6:
            a=sstep(t,ms[1]+0.8,ms[1]+1.8)*(1-sstep(t,ms[2]-0.4,ms[2]+0.6))
            o+=f'<g opacity="{a:.2f}">'+sparks(t,560,640,18,3,120)+f'<circle cx="560" cy="650" r="90" fill="url(#fl)"/></g>'
        return o
    return bg,fg,lambda u,t:(lerp(900,660,ease(u)),560,lerp(1.1,1.5,ease(u)))
@scene('trieu_dinh')
def _():
    bg=hall(dark=.2)+throne_back(1080,640,k=1.3)
    bg+='<path d="M200,120 Q300,300 260,520 L120,520 Q160,300 100,120Z" fill="#7a1c14" opacity=".9"/><path d="M1400,120 Q1300,300 1340,520 L1480,520 Q1440,300 1500,120Z" fill="#7a1c14" opacity=".9"/>'
    def fg(t,u,ms):
        o=''
        o+=P(1080,640,1.0,t,'talk',robe='#d9a441',trim='#f6e08a',hat='crown',hands='sleeve')+throne_front(1080,640,k=1.3)
        o+=P(760,800,1.0,t,'idle',robe='#4a525c',hat='helm',armor=True,trim='#b22a2a',hands='sleeve')
        o+=P(1400,790,.8,t,'idle',robe='#2e4a6a',hat='cap',face=-1)
        o+=lamp_a(560,700,t,1.4)+lamp_a(1500,690,t,1.1,2)
        o+=dust(t,300,1300,150,700,24,2,'#ffe9a0',.5)
        o+=fade(0.38*sstep(t,ms[2],ms[3]),'#300808')
        return o
    return bg,fg,lambda u,t:(lerp(900,780,ease(u)),460,lerp(1.0,1.5,ease(u)))
