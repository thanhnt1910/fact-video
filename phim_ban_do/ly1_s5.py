"""Cảnh động chương 9–12 (dòng 93–134)."""
from ly1_anim import *
from ly1_anim import _get
from ly1_s1 import throne_back,throne_front,mv,NIGHT_DEF
from ly1_s2 import drape,WHITE,coffin
from ly1_s3 import SKY_DEF,palace,courtyard,soldiers,room_bg
from ly1_s4 import dragon_img,wall_seg,castle
def gate(x,y,s=1.0,open_=0.0,col='#8f2d22',dark='#1a1410'):
    """cổng thành: open_ 0..1 (hai cánh mở ra)"""
    w=160*s;h=220*s
    o=f'<g stroke="{OUT}" stroke-width="4"><rect x="{x-w*1.5}" y="{y-h*1.3}" width="{w*3}" height="{h*1.3}" fill="#b99a64"/><rect x="{x-w/2}" y="{y-h}" width="{w}" height="{h}" fill="{dark}"/>'
    lw=w/2*(1-open_*.85)
    o+=f'<rect x="{x-w/2}" y="{y-h}" width="{lw}" height="{h}" fill="{col}"/><rect x="{x+w/2-lw}" y="{y-h}" width="{lw}" height="{h}" fill="{col}"/>'
    o+=f'<path d="M{x-w*1.7},{y-h*1.3} Q{x},{y-h*1.9} {x+w*1.7},{y-h*1.3} L{x+w*1.5},{y-h*1.2} L{x-w*1.5},{y-h*1.2}Z" fill="#a8261c"/></g>'
    return o
@scene('bao_bien')
def _():
    bg='<rect x="-400" y="-300" width="2400" height="1700" fill="#1a2238"/><g fill="#3a4262" opacity=".8"><ellipse cx="300" cy="120" rx="320" ry="80"/><ellipse cx="900" cy="80" rx="380" ry="90"/><ellipse cx="1400" cy="170" rx="300" ry="80"/></g>'
    def fg(t,u,ms):
        calm=sstep(t,ms[3]+.2,ms[3]+3.0);st=1-calm
        sky=int(26+110*calm)
        o=f'<rect x="-400" y="-300" width="2400" height="1100" fill="rgb({sky},{sky+14},{sky+50})" opacity="{.55+.45*calm:.2f}"/>'
        o+=clouds(t,120,5,'#4a5272' if calm<.5 else '#e8eef8',.85,22*st+4,3,1.4)
        if calm>0: o+=beam(1000,0,60,420,900,'#fff3c0',.25*calm,8)+beam(700,0,50,380,900,'#fff3c0',.18*calm,-6)
        o+=wave_band(560,t,28*st+6,'#24476e',-300,1900,.012,2.0*st+.8,1200)+wave_band(660,t,32*st+7,'#1d3a5e',-300,1900,.011,2.3*st+.9,1200,1.1)
        rk=1+st*2.2
        bt=boat(800,700+10*math.sin(t*2),t*rk,2.0,sail=True,sailc='#d9c8a0')
        o+=bt
        kneel=calm<.5
        o+=P(780,690,1.0,t,'idle',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='hold')
        for i,x in enumerate((650,900,980)): o+=P(x,700,.9,t,'idle',p=i,robe='#4a525c',hat='helm',armor=True,trim='#b22a2a',pose='kneelbow' if st>.5 else 'stand',ang=30*st)
        o+=f'<path d="M740,560 q-10,-40 6,-80 q-8,-30 8,-60" fill="none" stroke="#e8e8e8" stroke-width="8" stroke-linecap="round" opacity=".55"/><circle cx="733" cy="568" r="5" fill="#ff9d2e"/>'
        o+=wave_band(780,t,24*st+5,'#173050',-300,1900,.013,2.5*st+.8,1200,2.0)+wave_band(880,t,30*st+6,'#10253f',-300,1900,.012,2.8*st+.9,1200,3.0)
        if st>.05: o+=rain(t,int(120*st),-200,1800,-60,960,.4,.55*st,5,1200,46)
        fl=max(0.0,math.sin(t*2.1)**24)*st+max(0.0,math.sin(t*3.7+1)**30)*st*.7
        if fl>.02: o+=f'<path d="M1000,-60 L930,200 L1000,190 L900,420 L1080,170 L1010,180 Z" fill="#fff6b0" opacity="{min(1,fl*1.5):.2f}"/>'+fade(.5*fl,'#ffffff')
        return o
    return bg,fg,lambda u,t:(lerp(780,820,u),540,lerp(1.1,1.35,ease(u)))
@scene('chua_xay')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skyday)"/>'+hill([(-400,520),(300,470),(900,510),(1500,460),(2000,510)],'#8fb88a')+'<rect x="-400" y="640" width="2400" height="600" fill="#b8c88a"/><rect x="-400" y="780" width="2400" height="500" fill="#c9b27a"/>'
    def fg(t,u,ms):
        n=ms[-1];g=sstep(t,.3,n*.6)
        o=clouds(t,100,3,'#fff',.85,9,3)+birds(t,190,4,2,40)
        h=0;w=130
        for i in range(4):
            a=sstep(g,i*.22,i*.22+.3)
            o+=f'<g opacity="{a:.2f}" transform="translate(0,{(1-a)*-50:.0f})" stroke="{OUT}" stroke-width="3" stroke-linejoin="round"><rect x="{600-w*.6}" y="{720-h-70}" width="{w*1.2}" height="70" fill="#a8452c"/><path d="M{600-w},{720-h-62} Q600,{720-h-112} {600+w},{720-h-62} L{600+w*.8},{720-h-52} L{600-w*.8},{720-h-52}Z" fill="#5a3a2a"/></g>'
            h+=84;w*=.78
        o+=f'<path d="M290,720 V300 H450" stroke="#7a5a32" stroke-width="10" fill="none"/>'
        # chuông treo lắc
        sw=14*math.sin(t*1.6)*(.4+.6*sstep(t,n*.3,n*.5))
        o+=f'<g transform="translate(1180,260)"><rect x="-150" y="-20" width="300" height="20" fill="#5a3a20" stroke="{OUT}" stroke-width="3"/><g transform="rotate({sw:.1f} 0 0)"><path d="M0,0 V30" stroke="{OUT}" stroke-width="5"/><path d="M-60,160 Q-70,60 0,30 Q70,60 60,160Z" fill="#c9a24a" stroke="{OUT}" stroke-width="4"/><rect x="-66" y="156" width="132" height="14" rx="6" fill="#a8842a" stroke="{OUT}" stroke-width="3"/></g></g>'
        o+=f'<rect x="1020" y="260" width="12" height="470" fill="#5a3a20"/><rect x="1330" y="260" width="12" height="470" fill="#5a3a20"/>'
        for i in range(9):
            k=((t*.07)+i/9)%1;x=-100+k*2000
            o+=P(x,880,1.15,t,'walk',p=i,robe='#d98a2a',trim='#f2c94c',hat='bald',hands='sleeve')
        o+=smoke(900,740,t,6,'#e8e8e8',160,.25,9,22,.55)
        return o
    return bg,fg,lambda u,t:(lerp(700,980,ease(u)),560,lerp(1.1,1.25,u))
@scene('tang_cam_moc')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skydusk)"/>'+hill([(-400,560),(300,510),(900,550),(1500,500),(2000,550)],'#3a3050')+'<rect x="-400" y="700" width="2400" height="500" fill="#4a5a3a"/>'
    bg+='<path d="M560,800 Q800,640 1040,800Z" fill="#6a5a3a" stroke="#2a1608" stroke-width="4"/>'
    def fg(t,u,ms):
        o=stars(t,26,4,280)+dust(t,100,1500,450,900,26,5,'#f4f08a',.8)
        o+=smoke(800,670,t,5,'#ddd',150,.3,9,20,.5)+f'<rect x="794" y="680" width="12" height="60" fill="#5a3a20"/>'+flame(800,676,t,.4)
        for x,c in [(250,'#fff'),(1350,'#fff')]: o+=flag(x,380,t,120,70,c,330,x*.01,trim='#ddd')
        o+=P(800,880,1.1,t,'still',robe='#f2c94c',trim='#fff2a8',hat='crown',pose='bow',ang=22+14*math.sin(t*.8),hands='sleeve',face=1)
        for i,x in enumerate((540,620,980,1060)): o+=P(x,860,1.0,t,'still',p=i,robe=WHITE,hat='bun',pose='bow',ang=24+8*math.sin(t*.8+i),hands='sleeve',face=1 if x<800 else -1)
        return o
    return bg,fg,lambda u,t:(800,620,lerp(1.2,1.5,u))
@scene('thang_long_hung')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skyday)"/>'+hill([(-400,520),(300,470),(900,510),(1500,460),(2000,510)],'#9cc29a')+'<rect x="-400" y="540" width="2400" height="700" fill="#b8d88a"/>'
    bg+='<path d="M-400,820 Q500,760 1000,830 T2000,800 L2000,1100 L-400,1100Z" fill="#4a86c0"/>'
    for x,y,s in [(120,640,.7),(300,650,.8),(500,640,.7),(1100,650,.8),(1300,640,.7),(1480,650,.8),(1640,640,.7)]: bg+=house(x,y,s)
    bg+=palace(800,650,420,170,'#8a2a1c')+pagoda(1000,640,.7,3)+pagoda(560,640,.6,2)
    bg+='<path d="M-400,700 L2000,700" stroke="#a89468" stroke-width="50" opacity=".6"/>'
    def fg(t,u,ms):
        o=clouds(t,110,4,'#fff',.85,9,3)+birds(t,230,6,3,45)
        for x,y in [(120,590),(500,590),(1300,590)]: o+=smoke(x,y,t,5,'#aaa',90,.25,8,10,.4)
        o+=flag(640,330,t,110,64,'#2f8f4a',200,0)+flag(980,330,t,110,64,'#2f8f4a',200,2)
        for i in range(14):
            k=((t*.06)+i/14)%1;x=-100+k*1900*(1 if i%2==0 else -1)+(1700 if i%2 else 0)
            o+=P(x,720+(i%3)*28,.7,t,'walk',p=i,robe=['#8a5a3a','#3a5a3a','#6a3a5a','#2e4a6a'][i%4],hat='bun' if i%2 else 'cap',face=1 if i%2==0 else -1)
        for i,(x,y,s) in enumerate([(300,900,1.2),(700,940,1.4),(1200,890,1.1),(1500,960,1.0)]): o+=boat(((x+t*(30 if i%2==0 else -30))%2100)-250,y,t,s,i)
        return o
    return bg,fg,lambda u,t:(lerp(500,1100,ease(u)),560,1.25)
@scene('thai_tu')
def _():
    bg=courtyard('skyday')
    def fg(t,u,ms):
        o=clouds(t,100,3,'#fff',.85,9,3)
        for i,x in enumerate((200,420,1180,1400)): o+=flag(x,180,t,150,86,'#2f8f4a',320,i)
        a=sstep(t,.2,ms[-1]*.6)
        for r_,y in enumerate((760,840,920)):
            for i in range(5):
                x=lerp(-150-i*90,330+i*110-r_*30,a)
                o+=P(x,y,1.15,t,'walk' if a<1 else 'idle',p=i+r_,robe='#3a8a5a',hat='helm',armor=True,trim='#b22a2a')
        o+=P(lerp(1500,1000,a),780,1.6,t,'talk' if a>.99 else 'walk',robe='#2f7f4a',trim='#f2c94c',hat='helm',armor=True,face=-1,hands='sleeve')
        return o
    return bg,fg,lambda u,t:(800,560,1.2)
@scene('vua_om')
def _():
    bg=hall(dark=.4)+'<path d="M980,150 L1500,150 L1500,260 Q1240,230 980,260Z" fill="#a8261c" stroke="#3a0e08" stroke-width="3"/><rect x="990" y="260" width="14" height="440" fill="#6a1a12"/><rect x="1486" y="260" width="14" height="440" fill="#6a1a12"/>'+couch(1020,560,420)
    def fg(t,u,ms):
        o=P(1250,570,1.0,t,'still',robe='#d9a441',trim='#f6e08a',hat='crown',pose='lie',hands='sleeve')
        o+=P(900,800,1.2,t,'still',robe='#2e4a6a',hat='cap',pose='kneelbow',ang=36,hands='hold')+P(1500,800,1.1,t,'still',p=1,robe='#6a3a5a',hat='bun',pose='kneelbow',ang=36,face=-1)
        o+=P(660,800,1.3,t,'idle',robe='#2f7f4a',trim='#f2c94c',hat='crown',hands='hold')
        o+=lamp_a(820,700,t,1.4)+lamp_a(1400,640,t,1.0,2)
        return o
    return bg,fg,lambda u,t:(lerp(900,1100,ease(u)),520,1.3)
@scene('nhat_thuc')
def _():
    bg='<rect x="-400" y="-300" width="2400" height="1700" fill="#27304e"/><rect y="640" width="1600" height="260" fill="#201a2a"/>'
    bg+='<g stroke="#0e0a14" stroke-width="4"><rect x="460" y="500" width="680" height="150" fill="#3a2a3a"/><path d="M400,500 Q800,380 1200,500 L1170,530 Q800,430 430,530Z" fill="#2a1e30"/><path d="M500,430 Q800,320 1100,430 L1070,456 Q800,370 530,456Z" fill="#33243a"/><rect x="760" y="560" width="80" height="90" fill="#150f1a"/></g>'
    bg+=''.join(f'<rect x="{x}" y="520" width="26" height="120" fill="#5a2a2a" stroke="#0e0a14" stroke-width="3"/>' for x in (520,610,970,1060))
    def fg(t,u,ms):
        n=ms[-1];c=sstep(t,.4,n-1.5)   # 0 = chưa che, 1 = che hết
        dark=c
        o=f'<rect x="-400" y="-300" width="2400" height="1100" fill="#0a0a1c" opacity="{.75*dark:.2f}"/>'
        o+=stars(t,40,6,330) if False else f'<g opacity="{dark:.2f}">'+stars(t,40,6,330)+'</g>'
        sx,sy=800,260
        o+=f'<circle cx="{sx}" cy="{sy}" r="{300+60*dark}" fill="#5a4a7a" opacity="{.25+.25*dark:.2f}"/>'
        for i in range(18):
            a=i*math.pi/9;o+=f'<path d="M{sx},{sy} L{sx+math.cos(a)*(250+60*dark):.0f},{sy+math.sin(a)*(250+60*dark):.0f}" stroke="#ffe9a0" stroke-width="{3+(i%3)*2}" opacity="{.25+.45*dark:.2f}" stroke-linecap="round"/>'
        o+=f'<circle cx="{sx}" cy="{sy}" r="124" fill="#fff3c0"/>'
        mx=lerp(sx+260,sx,c)
        o+=f'<circle cx="{mx:.0f}" cy="{sy}" r="120" fill="#0a0a14"/>'
        o+=f'<circle cx="{sx}" cy="{sy}" r="{128+8*dark}" fill="none" stroke="#fff3c0" stroke-width="6" opacity="{.4*dark:.2f}"/>'
        o+=lamp_a(800,780,t,1.6)
        for i,x in enumerate((420,560,1040,1180)): o+=P(x,880,1.0,t,'still',p=i,robe='#3a3a5a',hat='cap',pose='bow',ang=8+20*dark,hands='up' if dark>.5 else 'sleeve')
        return o
    return bg,fg,lambda u,t:(800,400,lerp(1.05,1.3,ease(u)))
@scene('tang_le')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skydusk)"/>'+hill([(-400,540),(300,490),(900,530),(1500,480),(2000,530)],'#3a3050')+'<rect x="-400" y="700" width="2400" height="500" fill="#4a5a3a"/><path d="M-400,860 Q800,800 2000,870" stroke="#7a6a4a" stroke-width="60" fill="none"/>'
    def fg(t,u,ms):
        o=stars(t,26,4,260)+dust(t,0,1600,500,900,20,3,'#f4f08a',.7)
        x0=mv(t,0,ms[-1],350,1650)
        for i in range(10):
            x=x0-i*130
            o+=P(x,860,1.1,t,'walk',p=i*.5,robe=WHITE,hat='bun',hands='hold',face=1)
            if i%3==0: o+=flag(x+40,400,t,80,50,WHITE,300,i,trim='#ddd')
        # kiệu quan tài
        cx=x0-420
        o+=f'<g transform="translate({cx:.0f},760)" stroke="{OUT}" stroke-width="3"><rect x="-150" y="-70" width="300" height="60" rx="8" fill="#5a3a20"/><rect x="-150" y="-80" width="300" height="16" fill="#d9a441"/><rect x="-190" y="-30" width="380" height="8" fill="#3a2210"/></g>'
        for i in range(8): o+=P(cx-140+i*40,860,1.0,t,'walk',p=i,robe=WHITE,hat='bun',face=1)
        return o
    return bg,fg,lambda u,t:(800,620,1.2)
@scene('mai_phuc')
def _():
    bg=NIGHT_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skyn)"/><circle cx="1350" cy="120" r="50" fill="#f6f0cf"/>'
    bg+=palace(420,720,560,240,'#7a2a1c','#a89068')+'<rect x="-400" y="720" width="2400" height="500" fill="#3a3a44"/>'
    bg+=gate(1150,720,1.2,0)+'<rect x="900" y="560" width="120" height="160" fill="#b99a64" stroke="#2a1608" stroke-width="4"/>'
    def fg(t,u,ms):
        o=stars(t,30,7,300)
        for x in (200,400,600): o+=flag(x,420,t,90,56,WHITE,300,x*.01,trim='#ddd')
        o+=torch(960,640,t,1.3,0)+torch(1340,640,t,1.3,2)
        # lính mai phục lấp ló sau tường
        for i in range(9):
            x=780+i*60;a=sstep(t,ms[1]-.5,ms[1]+1.5)
            yy=560+(1-a)*60
            o+=f'<g transform="translate({x},{yy:.0f})"><path d="M-16,40 Q-16,0 0,-6 Q16,0 16,40Z" fill="#c4742c" stroke="{OUT}" stroke-width="2"/><ellipse cx="0" cy="-20" rx="13" ry="14" fill="#7d8896" stroke="{OUT}" stroke-width="2"/></g>'
            o+=f'<rect x="{x+10}" y="{yy-70:.0f}" width="4" height="90" fill="#5a3a20"/><path d="M{x+8},{yy-70:.0f} l4,-20 l4,20z" fill="#cfd4da" stroke="{OUT}" stroke-width="1.5"/>'
        # ba vị vương
        b=sstep(t,ms[2]-.2,ms[2]+1.2)
        for i,(x,rb) in enumerate([(1010,'#c4742c'),(1090,'#d98a3a'),(1170,'#a8523a')]):
            o+=P(x,820,1.2,t,'talk',p=i*2,robe=rb,trim='#f2c94c',hat='crown',hands='hold',face=-1 if i==0 else 1)
        return o
    return bg,fg,lambda u,t:(lerp(500,1050,ease(seg(u,.1,.7))),600,lerp(1.1,1.7,ease(seg(u,.5,1))))
@scene('thai_tu_vao')
def _():
    bg=courtyard('skyday')+gate(300,560,1.0,1.0)
    def fg(t,u,ms):
        n=ms[-1]
        o=clouds(t,100,3,'#fff',.85,9,3)
        a=sstep(t,.3,ms[1]*.9)
        o+=P(lerp(-200,700,a),860,1.5,t,'walk' if a<1 else 'idle',robe='#2f7f4a',trim='#f2c94c',hat='crown',hands='sleeve')
        for i in range(4): o+=P(lerp(-340,520-i*100,a),880-(i%2)*14,1.2,t,'walk' if a<1 else 'idle',p=i,robe='#4a525c',hat='helm',armor=True,trim='#b22a2a')
        # phát hiện, ra lệnh: quay đầu, giơ tay; cổng đóng
        cl=sstep(t,ms[1]+.5,ms[1]+3.0)
        o+=f'<g stroke="{OUT}" stroke-width="4"><rect x="{300-80+0}" y="{560-220}" width="{80*cl*1.0+1}" height="220" fill="#8f2d22"/><rect x="{300+80-80*cl}" y="{560-220}" width="{80*cl+1}" height="220" fill="#8f2d22"/></g>' if False else ''
        o+=P(1100,860,1.3,t,'idle',robe='#c4742c',hat='helm',armor=True,face=-1)
        return o
    return bg,fg,lambda u,t:(lerp(700,800,u),560,1.2)
@scene('thai_tu_tang')
def _():
    bg=hall(dark=.35)+''.join(drape(x) for x in (180,360,1240,1420))+coffin(800,700,1.5)
    def fg(t,u,ms):
        o=lamp_a(560,690,t,1.5)+lamp_a(1040,690,t,1.5,1.7)+smoke(800,560,t,6,'#ddd',150,.25,9,22,.45)
        o+=P(800,880,1.4,t,'talk' if t>ms[1] else 'idle',robe=WHITE,trim='#cfc8b8',hat='crown',hands='hold' if t>ms[1] else 'sleeve')
        step=sstep(t,ms[1]+.4,ms[1]+2.0)
        for i,x in enumerate((420,540,1060,1180)): o+=P(x,860-8*step*(i%2),1.15,t,'still',p=i,robe=['#2e4a6a','#6a3a5a','#3a5a3a','#5a3a2a'][i],hat='cap',pose='bow',ang=12+16*step,hands='sleeve',face=1 if x<800 else -1)
        return o
    return bg,fg,lambda u,t:(800,640,lerp(1.4,1.7,u))
@scene('mo_cua')
def _():
    bg=courtyard('skyday')+'<rect x="-400" y="520" width="2400" height="30" fill="#8a7452"/>'
    def fg(t,u,ms):
        n=ms[-1];op=sstep(t,n*.5,n*.5+1.8)
        o=gate(1200,640,1.1,op)
        bow=1 if t<n*.5 else 0
        for i,x in enumerate((520,640,760,880)): o+=P(x,860,1.2,t,'still',p=i,robe=['#6a3a5a','#2e4a6a','#3a5a3a','#5a3a2a'][i],hat='cap',pose='bow',ang=(32*max(0,math.sin(t*3)) if t<n*.5 else 0),hands='sleeve')
        if op>.5:
            for i in range(8):
                x=mv(t,n*.5+.6+i*.15,n*.5+2.8+i*.15,1000,1700+i*60) if t>n*.5+.6+i*.15 else None
                if x is not None: o+=P(x,840+(i%3)*20,1.15,t,'run',p=i,robe='#3a8a5a',hat='helm',armor=True,trim='#b22a2a',face=1)
        return o
    return bg,fg,lambda u,t:(lerp(760,1000,ease(u)),560,1.2)
@scene('giao_chien')
def _():
    bg=courtyard('skym',False)+gate(1300,600,1.0,1.0)
    def fg(t,u,ms):
        n=ms[-1];ret=sstep(t,ms[2],ms[2]+3.5)
        o=dust(t,300,1500,500,900,30,3,'#d9c8a0',.5)
        for r_,y in enumerate((740,820,900)):
            for i in range(5):
                gx=700+i*60+(r_%2)*30+6*math.sin(t*3+i)*(1-ret)
                o+=P(gx-lerp(0,900,ret)*0+0,y,1.1,t,'idle',p=i,robe='#3a8a5a',hat='helm',armor=True,trim='#b22a2a',face=1) if False else ''
        # phe hoàng cung (xanh) xông ra, phe nổi loạn (cam) chống rồi tháo chạy sang trái
        for r_,y in enumerate((740,820,900)):
            for i in range(5):
                xg=lerp(1150,620,sstep(t,.2,ms[1]))+i*58-r_*20
                xo=lerp(560,520,sstep(t,.2,ms[1]))+i*-58+r_*20-lerp(0,900,ret)
                o+=P(xg,y,1.1,t,'run' if t<ms[1] else 'idle',p=i+r_,robe='#3a8a5a',hat='helm',armor=True,trim='#b22a2a',face=-1)
                o+=P(xo,y,1.1,t,'run' if ret>0 else 'idle',p=i+r_+3,robe='#c4742c',hat='helm',armor=True,trim='#7a2a1c',face=1 if ret==0 else -1)
        # Lê Phụng Hiểu rút gươm xông ra
        ph_=sstep(t,ms[1]+.2,ms[1]+2.4)
        px=lerp(1250,420,ph_)
        o+=P(px,860,1.6,t,'run' if ph_<1 else 'idle',robe='#2f7f4a',trim='#f2c94c',hat='helm',armor=True,hands='up',face=-1)
        o+=f'<g transform="translate({px-60:.0f},{540:.0f}) rotate(-35)"><rect x="-4" y="-120" width="8" height="130" fill="#e8ecf0" stroke="{OUT}" stroke-width="2"/><rect x="-14" y="6" width="28" height="8" fill="#7a5a32" stroke="{OUT}" stroke-width="2"/></g>'
        o+=sparks(t,(560+1150)/2,700,10,2,200,'#fff3c0') if ret==0 else ''
        return o
    return bg,fg,lambda u,t:(lerp(900,700,ease(u)),580,1.2)
@scene('bao_tin')
def _():
    bg=hall(dark=.35)+''.join(drape(x) for x in (180,360,1240,1420))+coffin(800,700,1.5)
    def fg(t,u,ms):
        o=lamp_a(560,690,t,1.5)+lamp_a(1040,690,t,1.5,1.7)+smoke(800,560,t,6,'#ddd',150,.25,9,22,.45)
        a=sstep(t,.2,2.0)
        if t<ms[1]: o+=P(lerp(1400,820,a),880,1.5,t,'walk' if a<1 else 'still',robe='#4a5a3a',hat='helm',armor=True,trim='#b22a2a',pose='kneelbow' if a>=1 else 'stand',ang=48 if a>=1 else 0,face=-1 if a<1 else 1,hands='hold')
        else:
            b=sstep(t,ms[1]+.2,ms[1]+2.5)
            o+=P(lerp(820,1000,b),880,1.5,t,'walk' if 0<b<1 else 'idle',robe='#4a5a3a',hat='helm',armor=True,trim='#b22a2a',face=-1,pose='bow',ang=20*b if b>=1 else 0)
        o+=P(1160,880,1.4,t,'talk' if t>ms[1] else 'idle',robe=WHITE,trim='#cfc8b8',hat='crown',face=-1)
        for i,x in enumerate((420,540)): o+=P(x,860,1.15,t,'still',p=i,robe=['#2e4a6a','#6a3a5a'][i],hat='cap',pose='bow',ang=14)
        return o
    return bg,fg,lambda u,t:(900,640,lerp(1.4,1.6,u))
@scene('thai_tong_len_ngoi')
def _():
    bg=hall(dark=.05)+throne_back(800,500,k=1.5)+'<g stroke="#3a120c" stroke-width="3"><rect x="520" y="500" width="560" height="40" fill="#b8942a"/><rect x="460" y="540" width="680" height="40" fill="#a8842a"/><rect x="400" y="580" width="800" height="40" fill="#987422"/></g>'
    def fg(t,u,ms):
        o='';sit=sstep(t,.8,2.0)
        o+=P(lerp(800,800,sit),lerp(560,500,sit),1.5,t,'idle',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='sleeve')+(throne_front(800,500,k=1.5) if sit>.6 else '')
        o+=glow(800,330,230,t,0,op=.6*sit)+sparks(t,800,330,16,3,200)*(1 if sit>.5 else 0)
        for r_,(y,sz) in enumerate([(760,1.0),(840,1.1)]):
            for i in range(4):
                for sd in (-1,1):
                    x=800+sd*(220+i*120);o+=P(x,y,sz,t,'still',robe=['#2e4a6a','#6a3a5a','#3a5a3a','#5a3a2a'][(i+r_)%4],hat='cap',pose='bow',ang=18+22*max(0,math.sin(t*2+i)),hands='up' if t>ms[-1]*.5 else 'sleeve')
        o+=flag(300,160,t,150,86,'#2f8f4a',300,0)+flag(1300,160,t,150,86,'#2f8f4a',300,2)
        return o
    return bg,fg,lambda u,t:(800,470,lerp(1.15,1.35,ease(u)))
@scene('bon_noi')
def _():
    bg=_get('bon_cua')[0]
    pts=[(346,448),(800,148),(800,470),(800,290)]  # cửa Quảng Phúc, cửa Tường Phù, điện Càn Nguyên, điện Long An (gần đúng trên sơ đồ)
    def fg(t,u,ms):
        o='';n=ms[-1]
        for i,(x,y) in enumerate([(800,148),(346,448),(800,500),(800,288)]):
            a=sstep(t,.6+i*(n*.7)/4,1.6+i*(n*.7)/4)
            pulse=.5+.5*math.sin(t*4)
            o+=f'<circle cx="{x}" cy="{y}" r="{70+30*pulse*a}" fill="url(#fl)" opacity="{a:.2f}"/><circle cx="{x}" cy="{y}" r="{28}" fill="none" stroke="#ffcf4a" stroke-width="6" opacity="{a:.2f}"/>'
        for i in range(12):
            k=((t*.05)+i/12)%1;o+=P(800+((-1)**i)*(50),170+k*580,.45,t,'walk',p=i,robe=['#8a5a3a','#3a5a3a','#6a3a5a'][i%3],hat='bun')
        return o
    return bg,fg,lambda u,t:(lerp(560,900,ease(u)),470,lerp(1.2,1.5,ease(u)))
@scene('cua_tay_chieu')
def _():
    bg=courtyard('skydusk',False)+gate(800,640,1.3,0)
    def fg(t,u,ms):
        o=stars(t,20,3,200)+birds(t,200,5,3,40)
        o+=soldiers(2,540,680,860,1.2,t,'#4a6aa0',2)+soldiers(2,920,1060,860,1.2,t,'#4a6aa0',3,face=-1)
        g=sstep(t,ms[1]+.3,ms[1]+2.0)
        o+=f'<g opacity="{.55*g:.2f}">'+glow(800,540,320,t,0,op=.9)+P(800,820,1.7,t,'idle',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='sleeve',face=1)+'</g>'
        o+=flag(300,260,t,150,86,'#2f8f4a',320,0)+flag(1300,260,t,150,86,'#2f8f4a',320,1)
        return o
    return bg,fg,lambda u,t:(800,560,lerp(1.1,1.4,ease(u)))
@scene('hoang_hon')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skydusk)"/>'+hill([(-400,580),(300,530),(900,570),(1500,520),(2000,570)],'#3a3050')+'<rect x="-400" y="660" width="2400" height="540" fill="#2a2438"/>'
    bg+='<path d="M-400,800 Q500,760 1000,810 T2000,790 L2000,1100 L-400,1100Z" fill="#7a5a7a"/><circle cx="800" cy="520" r="160" fill="#ffd9a0" opacity=".5"/>'
    for x,y,s in [(120,680,.7),(300,690,.8),(1300,680,.8),(1480,690,.7)]: bg+=house(x,y,s,roof='#3a2a3a',wall='#5a4a58')
    bg+=wall_seg(480,1120,600,700,'#7a6a5a')+palace(800,610,300,130,'#5a1c14','#8a7658')+pagoda(1180,690,.7,3,'#7a3a2c')+pagoda(420,690,.6,2,'#7a3a2c')
    def fg(t,u,ms):
        o=stars(t,30,5,260)+clouds(t,150,3,'#ffd0b0',.55,6,2)
        n=ms[-1]
        for x in (120,300,1300,1480): o+=f'<rect x="{x-12}" y="{630}" width="24" height="22" fill="#ffd27a" opacity="{.7+.2*math.sin(t*5+x):.2f}"/>'
        rise=sstep(t,.5,n-1.0)
        o+=dragon_img(lerp(800,860,rise),lerp(520,200,rise),t,lerp(220,420,rise),rot=lerp(0,-6,rise)+2*math.sin(t),op=.9*sstep(t,.3,1.5),spd=5)+glow(lerp(800,860,rise),lerp(520,200,rise),240,t,0,op=.5*rise)
        o+=sparks(t,860,260,18,4,260)
        o+=boat(520,880,t,1.1)+boat(1180,900,t,.9,p=2)
        return o
    return bg,fg,lambda u,t:(800,520,lerp(1.2,1.0,ease(u)))

def _vb():
    bg,fg,cam=_FACT_VM()
    return bg,fg,lambda u,t:(lerp(1100,900,ease(u)),600,lerp(1.5,1.2,ease(u)))
from ly1_anim import _FACT as _F
_FACT_VM=_F['vua_mat']
_F['vua_bang']=_vb
