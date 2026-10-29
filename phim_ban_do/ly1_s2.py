"""Cảnh động chương 2 (dòng 13–26): những năm cuối nhà Tiền Lê."""
from ly1_anim import *
from ly1_s1 import throne_back,throne_front,mv,NIGHT_DEF
WHITE='#efe9dc'
def coffin(x,y,k=1.0):
    return (f'<g transform="translate({x},{y}) scale({k})" stroke="{OUT}" stroke-width="3"><rect x="-150" y="-70" width="300" height="70" rx="10" fill="#5a3a20"/><rect x="-150" y="-78" width="300" height="20" rx="8" fill="#d9a441"/>'
            f'<rect x="-120" y="-60" width="240" height="8" fill="#f2c94c" opacity=".8"/><rect x="-170" y="-10" width="340" height="24" fill="{WHITE}"/></g>')
def drape(x,w=90,h=520,col=WHITE): return f'<path d="M{x-w/2},-40 H{x+w/2} V{h} Q{x+w/4},{h-30} {x},{h} Q{x-w/4},{h+30} {x-w/2},{h}Z" fill="{col}" stroke="#bbb4a4" stroke-width="3" opacity=".95"/>'
@scene('hall_tang')
def _():
    bg=hall(dark=.35)+''.join(drape(x) for x in (180,360,1240,1420))+f'<rect y="690" width="1600" height="210" fill="url(#floor)" opacity=".0"/>'
    bg+=coffin(800,700,1.5)
    def fg(t,u,ms):
        o=''
        o+=lamp_a(560,690,t,1.5)+lamp_a(1040,690,t,1.5,1.7)+smoke(800,560,t,6,'#ddd',150,.25,9,22,.45)
        for i,x in enumerate((520,640,960,1080)): o+=P(x,880,1.15,t,'still',robe=WHITE,trim='#cfc8b8',hat='bun',pose='bow',ang=24+10*math.sin(t*.9+i),hands='sleeve')
        k=sstep(t,ms[1],ms[1]+1.2)
        # ba hoàng tử đứng đầu quan tài; sang dòng 2 họ quay đi và cãi
        for i,(x0,x1,rb) in enumerate([(700,360,'#6a3a5a'),(800,800,'#2e4a6a'),(900,1240,'#3a5a3a')]):
            x=lerp(x0,x1,k)
            o+=P(x,830,1.25,t,'talk' if k>.5 else 'idle',p=i*2,robe=rb,trim='#e8c36a',hat='crown' if i==1 else 'cap',hands='sleeve',face=1 if i<2 else -1)
        o+=fade(.25*k,'#400808')
        return o
    return bg,fg,lambda u,t:(800,650,lerp(1.45,1.65,u))
@scene('tranh_ngoi')
def _():
    bg=hall(dark=.45)+throne_back(800,620,k=1.4)+''.join(drape(x,70,420,'#7a1c14') for x in (150,1450))
    bg+=throne_front(800,620,k=1.4)
    def fg(t,u,ms):
        o=''
        o+=dust(t,500,1100,200,620,30,3,'#ffe9a0',.5)
        o+=torch(380,560,t,1.3)+torch(1220,560,t,1.3,2)
        # hai phe đi tới đi lui
        for i in range(4): o+=P(330+i*70+14*math.sin(t*1.1+i),780-i*10,1.0-i*.04,t,'talk',p=i,robe='#2e4a6a',trim='#9ab8e0',hat='cap',hands='sleeve')
        for i in range(4): o+=P(1270-i*70+14*math.sin(t*1.1+i+2),780-i*10,1.0-i*.04,t,'talk',p=i+1,robe='#7a3a2a',trim='#e8a070',hat='cap',hands='sleeve',face=-1)
        # tám vầng trăng lần lượt hiện: tám tháng không có vua
        for i in range(8):
            a=sstep(t,ms[1]*.0+0.3+i*(ms[-1]*.7)/8,0.3+i*(ms[-1]*.7)/8+.6)
            x=360+i*125
            o+=f'<g opacity="{a:.2f}"><circle cx="{x}" cy="90" r="26" fill="#f6f0cf" stroke="{OUT}" stroke-width="2"/><circle cx="{x+9}" cy="86" r="22" fill="#33324e" opacity=".85"/></g>'
        return o
    return bg,fg,lambda u,t:(800,450,1.15+.05*math.sin(u*3.1))
@scene('doi_ngoi')
def _():
    bg=hall(dark=.2)+throne_back(800,640,k=1.4)
    def fg(t,u,ms):
        o=''
        sw=sstep(t,ms[-1]*.45,ms[-1]*.45+.5)
        o+=P(800,640,1.4,t,'idle',robe='#c9a441' if sw<.5 else '#8f2d22',trim='#f6e08a',hat='crown',hands='sleeve')+throne_front(800,640,k=1.4)
        for i in range(5):
            xx=lerp(1560,1130+i*70,sstep(t,ms[-1]*.45,ms[-1]*.45+1.5)) if sw>0 else 1700
            if sw>0: o+=P(xx,800-i*10,1.0,t,'walk' if xx>1300+i*70 else 'idle',p=i,robe='#7a1c14',trim='#e8a070',hat='helm',armor=True,face=-1,hands='sleeve')
        o+=P(450,800,1.0,t,'idle',robe='#2e4a6a',hat='cap')+P(560,790,.9,t,'idle',p=2,robe='#4a4a7a',hat='cap')
        o+=lamp_a(520,700,t,1.4)+lamp_a(1100,700,t,1.4,3)
        o+=fade(.8*math.exp(-((t-ms[-1]*.45)/.25)**2),'#fff6d0')
        return o
    return bg,fg,lambda u,t:(800,520,lerp(1.3,1.55,ease(u)))
@scene('om_xac')
def _():
    bg=hall(dark=.4)+couch(560,590,480)+'<path d="M560,560 L1040,560 L1040,596 L560,596Z" fill="#e8e0d0" opacity=".9" stroke="#3a2a1a" stroke-width="2"/>'
    def fg(t,u,ms):
        o=''
        o+=P(800,600,1.0,t,'still',robe='#c9a441',trim='#f6e08a',hat='crown',pose='lie',hands='sleeve')
        n=ms[-1]
        # công uẩn quỳ khóc (vai rung)
        o+=P(520,790,1.5,t,'still',robe='#4a525c',hat='helm',armor=True,trim='#b22a2a',pose='kneelbow',ang=48+3*math.sin(t*9),hands='hold')
        o+=f'<path d="M470,720 q-6,30 4,50" fill="none" stroke="#9ad2f0" stroke-width="5" stroke-linecap="round" opacity="{.5+.4*math.sin(t*3):.2f}"/>'
        # quan bỏ chạy
        for i,(x0,yy,rb) in enumerate([(1000,800,'#2e4a6a'),(1100,820,'#6a3a5a'),(1200,790,'#3a5a3a'),(1300,830,'#5a4a2a'),(1400,800,'#7a3a2a')]):
            x=x0+max(0,t-0.3-i*.25)*230
            if x<1900: o+=P(x,yy,1.1,t,'run',p=i,robe=rb,hat='cap',hands='up',face=-1 if False else 1)
        # sang dòng 2: Lê Long Đĩnh bước vào, dòng 3: trao ấn
        a=sstep(t,ms[1]+.2,ms[1]+3.0)
        if t>ms[1]:
            x=lerp(1750,1100,a);o+=P(x,820,1.45,t,'walk' if a<1 else 'talk',robe='#8f2d22',trim='#f6e08a',hat='crown',face=-1,hands='sleeve')
            for i in range(3): o+=P(x+110+i*70,850-i*8,1.1,t,'walk' if a<1 else 'idle',p=i,robe='#4a525c',hat='helm',armor=True,face=-1)
        if t>ms[2]:
            o+=f'<g transform="translate({lerp(1000,640,sstep(t,ms[2],ms[2]+1.6)):.0f},{700-40*math.sin(sstep(t,ms[2],ms[2]+1.6)*3.14):.0f})"><rect x="-26" y="-20" width="52" height="40" rx="6" fill="#d9a441" stroke="{OUT}" stroke-width="3"/><rect x="-14" y="-32" width="28" height="16" rx="4" fill="#f2c94c" stroke="{OUT}" stroke-width="3"/></g>'+sparks(t,640,690,8,1,60)
        o+=lamp_a(300,690,t,1.3)
        return o
    return bg,fg,lambda u,t:(lerp(780,860,ease(u)),520,lerp(1.5,1.3,ease(u)))
@scene('khe_man')
def _():
    bg=hall(dark=.25)+'<g stroke="#2a1608" stroke-width="3"><rect x="600" y="620" width="520" height="30" rx="8" fill="#6a4228"/><rect x="640" y="650" width="26" height="120" fill="#4a2c18"/><rect x="1054" y="650" width="26" height="120" fill="#4a2c18"/><ellipse cx="860" cy="612" rx="120" ry="18" fill="#d8d0c0"/></g>'
    bg+='<path d="M-100,200 Q200,260 400,160 Q520,100 640,200" fill="none" stroke="#4a2c18" stroke-width="12"/>'
    def fg(t,u,ms):
        o=''
        for i,(x,y) in enumerate([(780,590),(850,584),(920,590)]):
            o+=f'<g transform="translate({x},{y})"><path d="M0,-22 L6,-8 L22,-8 L9,2 L14,18 L0,9 L-14,18 L-9,2 L-22,-8 L-6,-8Z" fill="#f2d23a" stroke="{OUT}" stroke-width="2.5"/></g>'
        o+=P(1100,700,1.45,t,'talk',robe='#8f2d22',trim='#f6e08a',hat='crown',face=-1,hands='sleeve')
        o+=P(500,820,1.2,t,'idle',robe='#4a525c',hat='helm',armor=True,trim='#b22a2a')
        # hạt mận hiện lên, sáng chớp
        a=sstep(t,ms[1],ms[1]+1.0)*(1-sstep(t,ms[-1]-1.5,ms[-1]-.5))
        if a>0:
            o+=f'<g opacity="{a:.2f}"><circle cx="850" cy="470" r="70" fill="url(#fl)"/><circle cx="850" cy="470" r="30" fill="#8a4a9a" stroke="{OUT}" stroke-width="3"/><ellipse cx="850" cy="470" rx="9" ry="14" fill="#d9c8a0"/></g>'+sparks(t,850,470,10,2,70,'#e8c0ff')
        # cánh hoa mận bay
        for i in range(14):
            x=(i*131+t*30)%1900-150;y=((i*97+t*50)%1100)-100
            o+=f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="7" ry="4" fill="#fff" opacity=".55" transform="rotate({i*40+t*60:.0f} {x:.0f} {y:.0f})"/>'
        o+=lamp_a(300,690,t,1.3)+lamp_a(1480,640,t,1.1,2)
        return o
    return bg,fg,lambda u,t:(lerp(900,860,u),520,lerp(1.35,1.7,ease(u)))
@scene('lung_giet')
def _():
    bg=NIGHT_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skyn)"/><circle cx="260" cy="130" r="60" fill="#f6f0cf"/>'
    bg+='<rect x="-400" y="680" width="2400" height="500" fill="#2a2a34"/><path d="M-400,700 L2000,700" stroke="#1a1a22" stroke-width="6"/>'
    for x in (50,420,800,1180,1560): bg+=house(x,690,1.7,roof='#2e2a28',wall='#4a4238')
    def fg(t,u,ms):
        o=stars(t,40,8,300)
        for i,x in enumerate((50,420,800,1180,1560)):
            on=math.sin(t*.5+i*1.9)>.2
            o+=f'<rect x="{x-24}" y="{690-110}" width="48" height="44" fill="#ffd27a" opacity="{.8 if on else .08}"/>'
        for i in range(5):
            x=mv(t,0.0,ms[-1],-250-i*130,1900-i*130)
            o+=P(x,860,1.2,t,'walk',p=i,robe='#2a2a34',trim='#555',hat='helm',armor=True,face=1,hands='sleeve')
            o+=torch(x+95,690,t,1.4,i,90)
        return o
    return bg,fg,lambda u,t:(lerp(600,1000,u),600,1.35)
@scene('canh_vua')
def _():
    bg=hall(dark=.3)+throne_back(1080,640,k=1.3)
    def fg(t,u,ms):
        o=P(1080,640,1.3,t,'talk',robe='#8f2d22',trim='#f6e08a',hat='crown',hands='sleeve',face=-1)+throne_front(1080,640,k=1.3)
        o+=P(780,820,1.4,t,'idle',robe='#4a525c',hat='helm',armor=True,trim='#b22a2a')
        o+=lamp_a(560,700,t,1.4)+lamp_a(1500,690,t,1.1,2)
        o+=dust(t,300,1300,150,700,20,6,'#ffe9a0',.5)
        return o
    return bg,fg,lambda u,t:(lerp(1000,900,u),520,lerp(1.5,1.8,u))
@scene('nghe_viec')
def _():
    bg=hall(dark=.3)+'<path d="M980,150 L1500,150 L1500,260 Q1240,230 980,260Z" fill="#a8261c" stroke="#3a0e08" stroke-width="3"/><rect x="990" y="260" width="14" height="440" fill="#6a1a12"/><rect x="1486" y="260" width="14" height="440" fill="#6a1a12"/>'+couch(1020,560,420)
    def fg(t,u,ms):
        o=P(1250,570,1.0,t,'still',robe='#8f2d22',trim='#f6e08a',hat='crown',pose='lie',hands='sleeve')
        o+=P(780,790,1.45,t,'idle',robe='#4a525c',hat='helm',armor=True,trim='#b22a2a',face=1)
        for i in range(3):
            a=sstep(t,.3+i*2.2,1.8+i*2.2);x=lerp(-250,540-i*150,a)
            mode='walk' if a<1 else 'talk'
            o+=P(x,820-i*8,1.1,t,mode,p=i,robe=['#2e4a6a','#6a3a5a','#3a5a3a'][i],hat='cap',hands='hold')
        o+=lamp_a(900,690,t,1.4)+lamp_a(1480,640,t,1.0,2)
        return o
    return bg,fg,lambda u,t:(lerp(780,1000,ease(u)),520,1.5)
@scene('vua_mat')
def _():
    bg=hall(dark=.55)+couch(560,590,480)+'<rect x="560" y="540" width="480" height="64" rx="12" fill="#efe9dc" stroke="#bbb4a4" stroke-width="3"/>'
    bg+=''.join(drape(x,70,430,WHITE) for x in (200,1400))
    def fg(t,u,ms):
        o=lamp_a(480,620,t,1.3)+lamp_a(1120,620,t,1.3,2)+smoke(800,540,t,6,'#ddd',140,.25,9,20,.45)
        for i,x in enumerate((360,500,1100,1240,1380)): o+=P(x,870,1.2,t,'still',robe=WHITE,trim='#cfc8b8',hat='bun',pose='bow',ang=20+8*math.sin(t*.8+i),hands='sleeve')
        return o
    return bg,fg,lambda u,t:(800,600,lerp(1.4,1.7,u))
@scene('vua_nho')
def _():
    bg=hall(dark=.2)+throne_back(800,640,k=1.4)
    def fg(t,u,ms):
        o=P(800,640,.95,t,'idle',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='sleeve')+throne_front(800,640,k=1.4)
        for i,(x,rb) in enumerate([(420,'#2e4a6a'),(540,'#6a3a5a'),(1060,'#3a5a3a'),(1180,'#5a3a2a')]):
            o+=P(x,800,1.0,t,'talk',p=i*1.3,robe=rb,hat='cap',face=1 if x<800 else -1,hands='sleeve')
        o+=lamp_a(300,700,t,1.4)+lamp_a(1320,700,t,1.4,2)
        return o
    return bg,fg,lambda u,t:(800,580,lerp(1.4,1.8,u))
