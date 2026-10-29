"""8 cảnh vector 16:9 cho video Lý Công Uẩn (SVG -> PNG). Không chữ, không máu."""
import io, math, random, cairosvg
from PIL import Image
VB='viewBox="0 0 1600 900"'
def png(svg,w=1600,h=900):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=w,output_height=h))).convert('RGB')
SKIN='#e8c39a'; OUT='#2a1608'
def person(x,y,s=1.0,robe='#7a3030',trim='#e8c36a',hat='cap',pose='stand',face=1,hands='sleeve',armor=False,skin=SKIN,hair='#1c1208'):
    """x,y = giữa hai bàn chân. s=1 cao ~230px."""
    o=f'<g transform="translate({x},{y}) scale({s*face},{s})" stroke="{OUT}" stroke-width="2.5" stroke-linejoin="round">'
    if pose=='lie':
        o=f'<g transform="translate({x},{y}) scale({s*face},{s}) rotate(-90) translate(0,-8)" stroke="{OUT}" stroke-width="2.5" stroke-linejoin="round">'
    ang={'bow':32,'kneelbow':52}.get(pose,0)
    if pose=='kneel' or pose=='kneelbow': o+='<g transform="scale(1,.72)">'
    # váy (phần dưới, đứng yên)
    if armor: o+=f'<path d="M-30,0 L-27,-60 L27,-60 L30,0Z" fill="#4a525c"/><path d="M-30,-26 L30,-26 L33,0 L-33,0Z" fill="#3c434c"/>'
    else: o+=f'<path d="M-30,0 L-26,-60 L26,-60 L30,0 Z" fill="{robe}"/><path d="M-27,-6 L27,-6 L30,0 L-30,0Z" fill="{trim}"/>'
    o+=f'<g transform="rotate({ang} 0 -60)">'
    # thân trên
    if armor: o+=f'<path d="M-27,-60 L-25,-105 Q0,-125 25,-105 L27,-60Z" fill="#7d8896"/><g stroke="#3c434c" stroke-width="2"><path d="M-22,-90 H22 M-22,-76 H22"/></g><rect x="-27" y="-66" width="54" height="9" fill="{robe}"/>'
    else: o+=f'<path d="M-26,-60 L-24,-105 Q0,-125 24,-105 L26,-60Z" fill="{robe}"/>'
    # tay áo rộng
    if hands=='sleeve': o+=f'<path d="M-24,-100 Q-52,-66 -30,-52 L16,-60 L18,-82 Z" fill="{robe}"/><path d="M24,-100 Q52,-66 30,-52 L-16,-60 L-18,-82Z" fill="{robe}" opacity=".95"/><ellipse cx="0" cy="-58" rx="11" ry="7" fill="{skin}"/>'
    elif hands=='up': o+=f'<path d="M-24,-100 Q-60,-120 -44,-150 L-30,-146 Q-40,-124 -14,-96Z" fill="{robe}"/><path d="M24,-100 Q60,-120 44,-150 L30,-146 Q40,-124 14,-96Z" fill="{robe}"/>'
    elif hands=='hold': o+=f'<path d="M-24,-100 Q-56,-78 -34,-60 L12,-70 L14,-92Z" fill="{robe}"/><path d="M24,-100 Q40,-80 22,-64 L-10,-66 L-8,-88Z" fill="{robe}"/><ellipse cx="-6" cy="-66" rx="10" ry="7" fill="{skin}"/>'
    # đầu
    o+=f'<rect x="-6" y="-128" width="12" height="14" fill="{skin}"/><ellipse cx="0" cy="-142" rx="19" ry="22" fill="{skin}"/>'
    o+=f'<circle cx="7" cy="-142" r="2" fill="{OUT}" stroke="none"/><path d="M2,-130 q6,3 12,0" fill="none" stroke="#8a4a3a" stroke-width="2"/>'
    if hat=='cap': o+=f'<path d="M-21,-148 Q0,-182 21,-148 L18,-156 Q0,-170 -18,-156Z" fill="{hair}"/><rect x="-24" y="-156" width="48" height="8" rx="3" fill="#2a2a30"/><rect x="-14" y="-176" width="28" height="22" rx="3" fill="#2a2a30"/>'
    elif hat=='crown': o+=f'<path d="M-24,-152 L-24,-188 L-10,-170 L0,-196 L10,-170 L24,-188 L24,-152Z" fill="#f2c94c"/><rect x="-24" y="-158" width="48" height="8" fill="#d4a017"/>'
    elif hat=='helm': o+=f'<path d="M-22,-148 Q0,-196 22,-148 Z" fill="#7d8896"/><rect x="-24" y="-152" width="48" height="8" fill="#4a525c"/><path d="M0,-172 L0,-198" stroke="#b22a2a" stroke-width="7" stroke-linecap="round"/>'
    elif hat=='hood': o+=f'<path d="M-24,-146 Q0,-190 24,-146 L24,-136 L-24,-136Z" fill="#555"/>'
    else: o+=f'<path d="M-20,-150 Q0,-184 20,-150 Q0,-160 -20,-150Z" fill="{hair}"/><circle cx="0" cy="-176" r="9" fill="{hair}"/>'
    o+='</g>'
    if pose in('kneel','kneelbow'): o+='</g>'
    return o+'</g>'
def col(x,w=46,top=120,bot=700): return f'<rect x="{x}" y="{top}" width="{w}" height="{bot-top}" fill="#8f2d22" stroke="#3a120c" stroke-width="3"/><rect x="{x-8}" y="{bot-16}" width="{w+16}" height="16" fill="#5b4a3a"/><rect x="{x-8}" y="{top}" width="{w+16}" height="14" fill="#c9a24a"/>'
def lamp(x,y,s=1,glow=True):
    g=f'<circle cx="{x}" cy="{y-18*s}" r="{70*s}" fill="url(#fl)"/>' if glow else ''
    return g+f'<g transform="translate({x},{y}) scale({s})" stroke="{OUT}" stroke-width="2"><path d="M-24,0 Q0,16 24,0 L18,-10 L-18,-10Z" fill="#a8742e"/><path d="M-4,-10 q-8,-22 4,-34 q12,12 4,34Z" fill="#ffb938" stroke="#d96a12"/><path d="M-2,-12 q-3,-12 2,-20 q5,8 2,20Z" fill="#fff3a8" stroke="none"/></g>'
DEFS='''<defs>
<radialGradient id="fl"><stop offset="0" stop-color="#ffcf70" stop-opacity=".75"/><stop offset="1" stop-color="#ffcf70" stop-opacity="0"/></radialGradient>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6d5a49"/><stop offset="1" stop-color="#8b7358"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6e5238"/><stop offset="1" stop-color="#3f2c1c"/></linearGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
</defs>'''
def wrap(inner,extra='',ext=False):
    if not ext: return f'<svg xmlns="http://www.w3.org/2000/svg" {VB}>{DEFS}{inner}<rect width="1600" height="900" fill="url(#vig)"/>{extra}</svg>'
    inner=(inner.replace('<rect width="1600" height="900" fill=','<rect x="-400" y="-300" width="2400" height="1700" fill=')
      .replace('<rect y="690" width="1600" height="210"','<rect x="-400" y="690" width="2400" height="500"')
      .replace('<rect y="640" width="1600" height="260"','<rect x="-400" y="640" width="2400" height="500"')
      .replace('<rect y="0" width="1600" height="300"','<rect x="-400" y="-300" width="2400" height="600"')
      .replace('<rect y="330" width="1600" height="570"','<rect x="-400" y="330" width="2400" height="900"')
      .replace('M0,300 Q800,250 1600,300 L1600,330 L0,330Z','M-400,300 Q800,250 2000,300 L2000,330 L-400,330Z'))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-200 0 2000 1125">{DEFS}{inner}<rect x="-400" y="-300" width="2400" height="1700" fill="url(#vig)"/>{extra}</svg>'

def hall(wall='url(#wall)',floor='url(#floor)',dark=0):
    s=f'<rect width="1600" height="900" fill="{wall}"/><rect y="690" width="1600" height="210" fill="{floor}"/>'
    s+=''.join(col(x) for x in (90,430,1130,1470))
    s+='<rect x="520" y="170" width="560" height="400" fill="#4a3322" stroke="#2a1608" stroke-width="4"/>'
    s+=''.join(f'<line x1="{520+i*70}" y1="170" x2="{520+i*70}" y2="570" stroke="#2a1608" stroke-width="3"/>' for i in range(1,8))
    s+=''.join(f'<line x1="520" y1="{170+i*80}" x2="1080" y2="{170+i*80}" stroke="#2a1608" stroke-width="3"/>' for i in range(1,5))
    s+='<rect x="520" y="170" width="560" height="400" fill="#f4c97a" opacity=".12"/>'
    if dark: s+=f'<rect width="1600" height="900" fill="#0b0a18" opacity="{dark}"/>'
    return s
def couch(x,y,w=420,lying=True):
    s=f'<g stroke="{OUT}" stroke-width="3"><rect x="{x}" y="{y}" width="{w}" height="48" rx="8" fill="#7a2c26"/><rect x="{x-10}" y="{y+48}" width="{w+20}" height="26" fill="#4a1c16"/><rect x="{x+20}" y="{y+74}" width="22" height="44" fill="#4a1c16"/><rect x="{x+w-42}" y="{y+74}" width="22" height="44" fill="#4a1c16"/><rect x="{x+10}" y="{y-26}" width="90" height="30" rx="14" fill="#d9a441"/></g>'
    return s
def sc1():  # Lê Long Đĩnh nằm nghe việc, Lý Công Uẩn đứng cạnh
    s=hall()
    s+='<path d="M980,150 L1500,150 L1500,260 Q1240,230 980,260Z" fill="#a8261c" stroke="#3a0e08" stroke-width="3"/><rect x="990" y="260" width="14" height="440" fill="#6a1a12"/><rect x="1486" y="260" width="14" height="440" fill="#6a1a12"/>'
    s+=couch(1020,560,420)
    s+=person(1250,570,1.0,robe='#d9a441',trim='#f6e08a',hat='crown',pose='lie',face=1,hands='sleeve')
    s+=person(600,740,1.35,robe='#4a525c',hat='helm',armor=True,trim='#b22a2a',hands='sleeve')
    s+=person(880,740,1.1,robe='#2e4a6a',hat='cap',hands='sleeve')
    s+=lamp(800,690,1.4)+lamp(1480,640,1.0)
    s+='<g opacity=".85"><circle cx="1180" cy="440" r="3" fill="#fff"/></g>'
    return wrap(s,ext=True)
def sc2():  # ôm xác vua khóc, quan bỏ chạy
    s=hall(dark=.28)
    s+=couch(560,590,480)
    s+=person(800,600,1.0,robe='#d9a441',trim='#f6e08a',hat='crown',pose='lie',face=1,hands='sleeve')
    s+='<path d="M560,560 L1040,560 L1040,596 L560,596Z" fill="#e8e0d0" opacity=".9" stroke="#3a2a1a" stroke-width="2"/>'
    s+=person(520,760,1.45,robe='#4a525c',hat='helm',armor=True,pose='kneelbow',hands='hold')
    s+='<path d="M470,690 q-6,26 4,44" fill="none" stroke="#9ad2f0" stroke-width="5" stroke-linecap="round"/>'
    for i,(x,yb,sz) in enumerate([(1230,780,.8),(1330,800,.85),(1420,790,.75),(1500,820,.9),(1290,720,.55)]):
        s+=person(x,yb,sz,robe=['#2e4a6a','#6a3a5a','#3a5a3a','#5a4a2a','#6a4a2a'][i],hat='cap',pose='bow' if i%2 else 'stand',face=1,hands='up')
    s+=''.join(f'<path d="M{1180-i*34},{820-i*18} h-46" stroke="#fff" stroke-width="4" opacity=".4" stroke-linecap="round"/>' for i in range(3))
    s+=lamp(300,690,1.2)
    return wrap(s,ext=True)
def sc3():  # Đào Cam Mộc thì thầm
    s=hall(dark=.45)
    s+='<rect x="120" y="150" width="320" height="380" fill="#1a1f3a" stroke="#2a1608" stroke-width="6"/>'+''.join(f'<line x1="{120+i*80}" y1="150" x2="{120+i*80}" y2="530" stroke="#2a1608" stroke-width="5"/>' for i in range(1,4))+'<circle cx="360" cy="230" r="26" fill="#f3efd0"/><g fill="#fff" opacity=".7"><circle cx="190" cy="210" r="2"/><circle cx="300" cy="300" r="2"/></g>'
    s+=lamp(1100,700,1.4)
    s+=person(760,770,1.4,robe='#4a525c',hat='helm',armor=True,hands='sleeve')
    s+=person(930,770,1.25,robe='#6a3a5a',hat='cap',pose='bow',face=-1,hands='sleeve')
    s+='<g fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".7"><path d="M850,500 q16,-6 26,6"/><path d="M846,520 q22,-6 36,10"/></g>'
    s+='<g opacity=".55"><circle cx="1010" cy="486" r="5" fill="#fff"/><circle cx="1030" cy="470" r="3" fill="#fff"/></g>'
    return wrap(s,ext=True)
def sc4():  # lên ngôi, trăm quan lạy rạp
    s='<rect width="1600" height="900" fill="#7a6048"/><rect y="0" width="1600" height="300" fill="#a8261c"/><path d="M0,300 Q800,250 1600,300 L1600,330 L0,330Z" fill="#c9a24a"/>'
    s+='<rect y="330" width="1600" height="570" fill="#8a7050"/>'
    s+=''.join(col(x,44,60,560) for x in (150,420,1110,1380))
    s+='<g stroke="#3a120c" stroke-width="3"><rect x="520" y="330" width="560" height="40" fill="#b8942a"/><rect x="480" y="370" width="640" height="40" fill="#a8842a"/><rect x="440" y="410" width="720" height="40" fill="#987422"/></g>'
    s+='<path d="M700,330 q100,-40 200,0" fill="none" stroke="#f2c94c" stroke-width="4"/>'
    s+='<g stroke="#3a120c" stroke-width="3"><rect x="740" y="250" width="120" height="86" rx="6" fill="#d9a441"/><rect x="720" y="130" width="160" height="130" rx="14" fill="#e8b84a"/><circle cx="800" cy="170" r="28" fill="#f2c94c"/></g>'
    s+=person(800,332,1.05,robe='#f2c94c',trim='#fff2a8',hat='crown',hands='sleeve')
    s+='<g opacity=".4" fill="#fff"><path d="M780,160 l20,-24 l20,24z"/></g>'
    rows=[(480,.95,9),(560,1.05,10),(650,1.15,11),(760,1.3,12)]
    colors=['#2e4a6a','#6a3a5a','#3a5a3a','#5a3a2a','#4a4a7a','#7a3a2a']
    rnd=random.Random(4)
    for ri,(y,sz,n) in enumerate(rows):
        for i in range(n):
            x=210+i*(1180/(n-1)) if n>1 else 800
            if 640<x<960 and ri<2: continue
            s+=person(x+rnd.uniform(-8,8),y+(ri*0),sz*0.75,robe=colors[(i+ri)%6],hat='cap' if i%2 else 'none',pose='bow' if ri%2 else 'kneelbow',hands='up')
    s+=lamp(560,430,0.9,False)
    return wrap(s,ext=True)
def sc5():  # bản chiếu dời đô
    s='<rect width="1600" height="900" fill="#241a14"/><rect y="640" width="1600" height="260" fill="#3a2a1c"/>'
    s+='<circle cx="800" cy="460" r="520" fill="url(#fl)" opacity=".8"/>'
    s+='<g stroke="#2a1608" stroke-width="4"><rect x="340" y="600" width="920" height="40" rx="6" fill="#6a4228"/><rect x="380" y="640" width="30" height="120" fill="#4a2c18"/><rect x="1190" y="640" width="30" height="120" fill="#4a2c18"/></g>'
    s+='<g stroke="#2a1608" stroke-width="4"><path d="M330,372 Q800,350 1270,372 L1270,600 Q800,620 330,600Z" fill="#f1e2b4"/><rect x="296" y="352" width="44" height="270" rx="20" fill="#c9a26a"/><rect x="1260" y="352" width="44" height="270" rx="20" fill="#c9a26a"/><circle cx="318" cy="340" r="14" fill="#8a1c1c"/><circle cx="318" cy="634" r="14" fill="#8a1c1c"/><circle cx="1282" cy="340" r="14" fill="#8a1c1c"/><circle cx="1282" cy="634" r="14" fill="#8a1c1c"/></g><path d="M330,372 Q800,350 1270,372 L1270,400 Q800,380 330,400Z" fill="#000" opacity=".12"/>'
    for i in range(7): s+=f'<g stroke="#4a3220" stroke-width="5" stroke-linecap="round" opacity=".75"><path d="M{360+i*20},392 v190" opacity="0"/></g>'
    rnd=random.Random(9)
    for c in range(8):
        x=360+c*115
        s+=f'<g stroke="#3a2a1c" stroke-width="4" stroke-linecap="round" opacity=".7">'+''.join(f'<path d="M{x},{385+r*28} h{rnd.randint(50,86)}"/>' for r in range(8))+'</g>'
    s+='<g stroke="#2a1608" stroke-width="3"><rect x="1100" y="520" width="16" height="130" rx="6" transform="rotate(-24 1100 520)" fill="#7a4a22"/><path d="M1068,636 l-8,26 l22,-12z" fill="#2a1608"/></g>'
    s+='<g><rect x="1180" y="540" width="110" height="60" rx="6" fill="#4a4a50" stroke="#2a1608" stroke-width="3"/><rect x="1196" y="556" width="78" height="14" fill="#1a1a1a"/></g>'
    s+=lamp(520,330,1.9)+lamp(1100,330,1.5)
    s+=person(800,860,1.5,robe='#f2c94c',trim='#fff2a8',hat='crown',pose='bow',hands='sleeve') if False else ''
    s+='<g opacity=".5" fill="#fff"><circle cx="520" cy="250" r="3"/><circle cx="1110" cy="262" r="2"/><circle cx="480" cy="230" r="2"/></g>'
    return wrap(s)
def sc6():  # thành Thăng Long nhìn từ trên cao
    s='<rect width="1600" height="900" fill="#8fc062"/><g transform="translate(800,420) scale(.8) translate(-800,-450)"><rect x="-400" y="-300" width="2400" height="1500" fill="#9bc86a"/><path d="M0,700 Q300,640 600,720 T1600,680 L1600,900 L0,900Z" fill="#8bb85a"/>'
    s+='<path d="M-40,560 Q200,540 420,600 T900,780 T1700,860 L1700,930 L900,860 T420,700 Q200,640 -40,640Z" fill="#4a86c0" opacity=".9"/>'
    s+='<g stroke="#3a2210" stroke-width="4"><rect x="300" y="110" width="1000" height="700" fill="#4a86c0"/><rect x="330" y="140" width="940" height="640" fill="#cfae78"/><rect x="354" y="164" width="892" height="592" fill="#b99a64"/></g>'
    def gate(x,y,w,h,n): return f'<g stroke="#3a1008" stroke-width="3"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#a8452c"/><rect x="{x+8}" y="{y+8}" width="{w-16}" height="{h-16}" fill="#d9a441"/><path d="M{x-10},{y} L{x+w/2},{y-26} L{x+w+10},{y}Z" fill="#8c2a1c"/></g>'
    s+=gate(770,130,60,40,1)+gate(770,750,60,40,2)+gate(334,420,40,60,3)+gate(1226,420,40,60,4)
    def hallb(x,y,w,h): return f'<g stroke="#3a1008" stroke-width="3"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e0c088"/><path d="M{x-14},{y} Q{x+w/2},{y-44} {x+w+14},{y} L{x+w+6},{y+14} L{x-6},{y+14}Z" fill="#a8261c"/><path d="M{x-6},{y-16} Q{x+w/2},{y-62} {x+w+6},{y-16} L{x+w},{y-6} L{x},{y-6}Z" fill="#c33a2a"/></g>'
    s+=hallb(690,420,220,90)+hallb(500,430,120,70)+hallb(980,430,120,70)+hallb(700,250,200,80)+hallb(700,560,110,60)+hallb(850,560,110,60)
    s+='<path d="M800,170 V250 M800,330 V420 M800,510 V560 M800,620 V750 M600,465 H690 M910,465 H980" stroke="#8a6a3a" stroke-width="18" stroke-linecap="round" opacity=".7"/>'
    s+='<g fill="#4c8a3a" stroke="#2f5a24" stroke-width="2">'+''.join(f'<ellipse cx="{x}" cy="{y}" rx="26" ry="18"/>' for x,y in [(420,220),(1180,220),(420,700),(1180,700),(560,640),(1040,630)])+'</g>'
    s+='<g><path d="M1430,330 q60,-24 120,0 l-20,40 h-80z" fill="#8a5a2c" stroke="#3a2210" stroke-width="3"/><rect x="1488" y="290" width="4" height="50" fill="#3a2210"/><path d="M1492,292 l30,10 l-30,10z" fill="#2f8f4a"/></g>'
    s+='</g>'
    return wrap(s)
def sc7():  # biển Biện Sơn dông tố, vua khấn
    s='<rect width="1600" height="900" fill="#1a2238"/><path d="M0,0 H1600 V420 Q1200,330 800,400 Q400,470 0,380Z" fill="#2a3150"/><g fill="#3a4262" opacity=".8"><ellipse cx="300" cy="120" rx="320" ry="80"/><ellipse cx="900" cy="80" rx="380" ry="90"/><ellipse cx="1400" cy="170" rx="300" ry="80"/></g>'
    s+='<path d="M1000,60 L930,260 L1000,250 L900,470 L1080,220 L1010,230 Z" fill="#fff6b0" stroke="#f2d84a" stroke-width="4"/><circle cx="960" cy="300" r="200" fill="#fff6b0" opacity=".12"/>'
    waves=''
    for i,(y,c) in enumerate([(430,'#24476e'),(520,'#1d3a5e'),(620,'#173050'),(740,'#10253f')]):
        waves+=f'<path d="M0,{y} '+' '.join(f'Q{x+100},{y-60-(i%2)*20} {x+200},{y}' for x in range(0,1600,200))+f' L1600,900 L0,900Z" fill="{c}"/>'
    s+=waves
    s+='<g stroke="#e8f2ff" stroke-width="5" stroke-linecap="round" fill="none" opacity=".7">'+''.join(f'<path d="M{x},{y} q30,-30 70,-6"/>' for x,y in [(160,520),(520,610),(1240,560),(1360,700),(260,760),(880,730)])+'</g>'
    s+='<g stroke="#2a1608" stroke-width="4" stroke-linejoin="round"><path d="M560,640 Q800,720 1060,640 L1020,700 Q800,760 600,700Z" fill="#7a4a2a"/><rect x="798" y="330" width="8" height="310" fill="#3a2210"/><path d="M806,350 Q960,400 970,560 L806,590Z" fill="#d9c8a0"/><path d="M798,380 Q690,420 690,560 L798,570Z" fill="#c9b890"/><rect x="590" y="620" width="440" height="14" fill="#5a3a20"/></g>'
    s+=person(760,630,.8,robe='#f2c94c',trim='#fff2a8',hat='crown',hands='hold')
    s+=person(880,630,.62,robe='#4a525c',hat='helm',armor=True,hands='sleeve')
    s+='<path d="M740,540 q-10,-40 6,-80 q-8,-30 8,-60" fill="none" stroke="#e8e8e8" stroke-width="8" stroke-linecap="round" opacity=".55"/><circle cx="732" cy="548" r="5" fill="#ff9d2e"/>'
    return wrap(s)
def sc8():  # nhật thực trên điện Long An
    s='<rect width="1600" height="900" fill="#27304e"/><circle cx="800" cy="260" r="330" fill="#5a4a7a" opacity=".35"/><circle cx="800" cy="260" r="220" fill="#8a7aa8" opacity=".35"/>'
    s+=''.join(f'<path d="M800,260 L{800+math.cos(a)*300:.0f},{260+math.sin(a)*300:.0f}" stroke="#ffe9a0" stroke-width="{3+(i%3)*2}" opacity=".55" stroke-linecap="round"/>' for i,a in enumerate([k*math.pi/9 for k in range(18)]))
    s+='<circle cx="800" cy="260" r="124" fill="none" stroke="#fff3c0" stroke-width="10" opacity=".9"/><circle cx="800" cy="260" r="118" fill="#0a0a14"/><path d="M690,200 A124,124 0 0 1 870,150" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".9"/>'
    s+='<g fill="#fff" opacity=".8"><circle cx="200" cy="120" r="3"/><circle cx="1380" cy="180" r="3"/><circle cx="420" cy="300" r="2"/><circle cx="1180" cy="90" r="2"/><circle cx="560" cy="80" r="2"/></g>'
    s+='<rect y="640" width="1600" height="260" fill="#201a2a"/>'
    s+='<g stroke="#0e0a14" stroke-width="4"><rect x="460" y="500" width="680" height="150" fill="#3a2a3a"/><path d="M400,500 Q800,380 1200,500 L1170,530 Q800,430 430,530Z" fill="#2a1e30"/><path d="M500,430 Q800,320 1100,430 L1070,456 Q800,370 530,456Z" fill="#33243a"/><rect x="760" y="560" width="80" height="90" fill="#150f1a"/></g>'
    s+=''.join(f'<rect x="{x}" y="520" width="26" height="120" fill="#5a2a2a" stroke="#0e0a14" stroke-width="3"/>' for x in (520,610,970,1060))
    s+=lamp(800,780,1.6)
    s+=''.join(person(x,860,.7,robe='#3a3a5a',hat='cap',pose='bow',hands='up') for x in (500,640,960,1100))
    return wrap(s,ext=True)
SC={1:sc1,2:sc2,3:sc3,4:sc4,5:sc5,6:sc6,7:sc7,8:sc8}
NAME={1:'ngoc-trieu',2:'om-xac-vua',3:'thi-tham',4:'len-ngoi',5:'chieu-doi-do',6:'thanh-thang-long',7:'bien-bien-son',8:'nhat-thuc'}
if __name__=='__main__':
    import sys
    for k in ([int(a) for a in sys.argv[1:]] or list(SC)):
        png(SC[k]()).save(f'/tmp/proto/ly1_sc{k}_{NAME[k]}.png'); print('ok',k)
