"""Cảnh động chương 3–4 (dòng 27–55)."""
from ly1_anim import *
from ly1_s1 import throne_back,throne_front,mv,NIGHT_DEF
from ly1_s2 import drape,WHITE
SKY_DEF='<defs><linearGradient id="skym" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd9a0"/><stop offset=".5" stop-color="#f7e9c8"/><stop offset="1" stop-color="#a8cfe8"/></linearGradient><linearGradient id="skyday" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fb0e8"/><stop offset="1" stop-color="#e6f0f4"/></linearGradient><linearGradient id="skydusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3a78"/><stop offset=".6" stop-color="#d9708a"/><stop offset="1" stop-color="#ffc47a"/></linearGradient></defs>'
def palace(x,y,w=520,h=230,roof='#a8261c',wall='#e0c088'):
    o=f'<g stroke="{OUT}" stroke-width="3" stroke-linejoin="round"><rect x="{x-w/2}" y="{y-h}" width="{w}" height="{h}" fill="{wall}"/>'
    for i in range(6):
        cx=x-w/2+w*(i+.5)/6;o+=f'<rect x="{cx-9}" y="{y-h}" width="18" height="{h}" fill="#8f2d22"/>'
    o+=f'<rect x="{x-60}" y="{y-h*.62}" width="120" height="{h*.62}" fill="#3a2210"/>'
    o+=f'<path d="M{x-w/2-40},{y-h} Q{x},{y-h-100} {x+w/2+40},{y-h} L{x+w/2+20},{y-h+24} L{x-w/2-20},{y-h+24}Z" fill="{roof}"/><path d="M{x-w/2+30},{y-h-34} Q{x},{y-h-150} {x+w/2-30},{y-h-34} L{x+w/2-50},{y-h-12} L{x-w/2+50},{y-h-12}Z" fill="#c33a2a"/></g>'
    return o
def courtyard(sky='skyday',pal=True,fence=True):
    bg=SKY_DEF+f'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#{sky})"/>'
    bg+=hill([(-400,430),(300,380),(800,420),(1300,370),(2000,420)],'#7fa37a')
    if pal: bg+=palace(800,520,560,240)
    bg+='<rect x="-400" y="520" width="2400" height="700" fill="#cdb98c"/><path d="M-400,640 L2000,640" stroke="#a89468" stroke-width="3"/><path d="M-400,760 L2000,760" stroke="#a89468" stroke-width="3"/>'
    for i in range(-4,12): bg+=f'<path d="M{i*200},520 L{i*300-400},1200" stroke="#a89468" stroke-width="2" opacity=".6"/>'
    bg+='<g stroke="#2a1608" stroke-width="3"><rect x="640" y="520" width="320" height="26" fill="#b8942a"/><rect x="600" y="546" width="400" height="26" fill="#a8842a"/></g>'
    return bg
def soldiers(n,x0,x1,y,s,t,colr,seed=1,face=1,spear=True,hat='helm',mode='idle'):
    o='';r=random.Random(seed)
    for i in range(n):
        x=x0+(x1-x0)*i/max(1,n-1)+r.uniform(-6,6)
        o+=P(x,y+r.uniform(-4,4),s,t,mode,p=r.uniform(0,6),robe=colr,hat=hat,armor=True,trim='#b22a2a',face=face)
        if spear: o+=f'<rect x="{x+22*s*face:.0f}" y="{y-290*s:.0f}" width="5" height="{290*s:.0f}" fill="#5a3a20"/><path d="M{x+20*s*face:.0f},{y-290*s:.0f} l5,-26 l5,26z" fill="#cfd4da" stroke="{OUT}" stroke-width="1.5"/>'
    return o
def room_bg():
    bg='<rect width="1600" height="900" fill="#5a4636"/><rect y="690" width="1600" height="210" fill="url(#floor)"/>'
    bg+='<rect x="120" y="140" width="320" height="380" fill="#1a1f3a" stroke="#2a1608" stroke-width="8"/>'+''.join(f'<line x1="{120+i*80}" y1="140" x2="{120+i*80}" y2="520" stroke="#2a1608" stroke-width="5"/>' for i in range(1,4))+'<circle cx="340" cy="230" r="28" fill="#f3efd0"/>'
    bg+='<rect x="1100" y="160" width="360" height="40" fill="#4a2c18"/><rect x="1100" y="300" width="360" height="40" fill="#4a2c18"/><rect x="1100" y="440" width="360" height="40" fill="#4a2c18"/>'
    for i in range(9): bg+=f'<rect x="{1120+i*38}" y="{205+(i%2)*4}" width="26" height="90" rx="4" fill="#cfae78" stroke="{OUT}" stroke-width="2"/>'
    for i in range(9): bg+=f'<rect x="{1120+i*38}" y="{345+(i%3)*3}" width="26" height="90" rx="4" fill="#bca068" stroke="{OUT}" stroke-width="2"/>'
    bg+='<rect x="620" y="640" width="360" height="26" rx="6" fill="#6a4228" stroke="#2a1608" stroke-width="3"/>'
    return bg
@scene('hai_doi_quan')
def _():
    bg=courtyard('skym')+'<rect x="720" y="470" width="160" height="56" fill="#f2c94c" opacity=".5"/>'
    def fg(t,u,ms):
        o=glow(800,430,260,t,0,op=.8)
        for i,x in enumerate((220,380,1220,1380)): o+=flag(x,200,t,150,86,['#2e5aa0','#2e5aa0','#2f8f4a','#2f8f4a'][i],300,i)
        for r_,y in enumerate((700,790,880)):
            o+=soldiers(5,120+r_*40,520+r_*30,y,1.15,t,'#4a6aa0',seed=r_+1)
            o+=soldiers(5,1080-r_*30,1480-r_*40,y,1.15,t,'#3a8a5a',seed=r_+7,face=-1)
        o+=P(560,640,1.5,t,'talk',robe='#2e4a9a',hat='helm',armor=True,trim='#e8c36a')+P(1040,640,1.5,t,'talk',p=2,robe='#2f7f4a',hat='helm',armor=True,trim='#e8c36a',face=-1)
        return o
    return bg,fg,lambda u,t:(lerp(640,960,ease(u)),520,1.12)
@scene('dao_cam_moc')
def _():
    bg=room_bg()
    def fg(t,u,ms):
        o=lamp_a(800,640,t,1.5)+stars(t,10,2,0)
        o+=P(560,830,1.35,t,'idle',robe='#4a525c',hat='helm',armor=True,trim='#b22a2a',hands='sleeve')
        a=sstep(t,.2,1.5)
        o+=P(lerp(1400,1000,a),830,1.2,t,'walk' if a<1 else 'talk',robe='#6a3a5a',hat='cap',pose='bow',ang=12*(1-a)+14,face=-1,hands='sleeve')
        if a>=1:
            for i in range(3):
                u2=((t*.7)+i/3)%1;o+=f'<path d="M{930-u2*140:.0f},{560+i*14} q-18,-8 -34,0" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity="{.7*(1-u2):.2f}"/>'
        return o
    return bg,fg,lambda u,t:(lerp(780,860,u),600,1.55)
@scene('gia_mang')
def _():
    bg=room_bg()
    def fg(t,u,ms):
        o=lamp_a(800,640,t,1.5)
        calm=sstep(t,ms[2]-.2,ms[2]+1.2)
        o+=P(560,830,1.4,t,'talk' if calm<.5 else 'idle',p=0,robe='#4a525c',hat='helm',armor=True,trim='#b22a2a',hands='up' if (t<ms[1] and int(t*2)%2==0) else 'sleeve')
        o+=P(1030,830,1.2,t,'idle' if t<ms[1] else 'talk',p=2,robe='#6a3a5a',hat='cap',face=-1,hands='sleeve')
        o+=fade(.35*(1-calm)*sstep(t,0,.8),'#701010')
        return o
    return bg,fg,lambda u,t:(800,620,lerp(1.5,1.75,u))
@scene('den_sang')
def _():
    bg=courtyard('skym')
    def fg(t,u,ms):
        o=birds(t,180,5,3,50)+clouds(t,120,3,'#fff',.7,8,2)
        o+=flag(260,250,t,150,86,'#2e5aa0',280,0)+flag(1340,250,t,150,86,'#2e5aa0',280,2)
        x=mv(t,.2,ms[-1]-.8,-200,760)
        o+=P(x,900,1.5,t,'walk' if x<740 else 'idle',robe='#6a3a5a',hat='cap',hands='sleeve')
        o+=soldiers(3,420,520,800,1.2,t,'#4a6aa0')+soldiers(3,1080,1180,800,1.2,t,'#4a6aa0',face=-1,seed=4)
        return o
    return bg,fg,lambda u,t:(800,560,1.4)
@scene('hop_quan')
def _():
    bg=hall(dark=.2)
    def fg(t,u,ms):
        o=''
        o+=lamp_a(300,700,t,1.4)+lamp_a(1320,700,t,1.4,2)
        up=sstep(t,ms[-1]-3.2,ms[-1]-2.4)
        for i,(x,y,rb,f) in enumerate([(520,820,'#2e4a6a',1),(640,800,'#4a4a7a',1),(960,800,'#3a5a3a',-1),(1080,820,'#5a3a2a',-1),(580,900,'#7a3a2a',1),(1020,900,'#6a3a5a',-1)]):
            o+=P(x,y,1.2,t,'cheer' if up>.5 else 'talk',p=i*1.7,robe=rb,hat='cap',face=f,hands='sleeve')
        o+=P(800,860,1.35,t,'talk',p=1,robe='#6a3a5a',trim='#e8c36a',hat='cap',hands='sleeve')
        return o
    return bg,fg,lambda u,t:(800,600,lerp(1.4,1.65,u))
@scene('len_ngoi')
def _():
    bg=hall(dark=.05)+throne_back(800,500,k=1.5)+'<g stroke="#3a120c" stroke-width="3"><rect x="520" y="500" width="560" height="40" fill="#b8942a"/><rect x="460" y="540" width="680" height="40" fill="#a8842a"/><rect x="400" y="580" width="800" height="40" fill="#987422"/></g>'
    def fg(t,u,ms):
        o='';sit=sstep(t,ms[1]-.5,ms[1]+.5)
        walk=sstep(t,.4,ms[1]-1.0)
        if sit<.5:
            o+=P(lerp(800,800,walk),lerp(900,500,walk),lerp(1.4,1.0,walk),t,'walk' if walk<1 else 'idle',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='sleeve')
        else: o+=P(800,500,1.5,t,'idle',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='sleeve')+throne_front(800,500,k=1.5)
        o+=glow(800,330,200,t,0,op=.5*sit)
        for r_,(y,sz) in enumerate([(720,1.0),(800,1.1),(880,1.2)]):
            for i in range(4):
                for sd in (-1,1):
                    x=800+sd*(230+i*120)
                    ang=40+30*math.sin(t*2.2+i*.8+r_)*(1 if t>ms[1] else .3)
                    o+=P(x,y,sz,t,'still',robe=['#2e4a6a','#6a3a5a','#3a5a3a','#5a3a2a'][(i+r_)%4],hat='cap',pose='bow',ang=ang if t>ms[1] else 8,hands='up' if t>ms[1]+1 else 'sleeve')
        o+=flag(300,160,t,150,86,'#2f8f4a',300,0)+flag(1300,160,t,150,86,'#2f8f4a',300,2)
        if sit>.5: o+=sparks(t,800,330,14,3,180)
        return o
    return bg,fg,lambda u,t:(800,540,lerp(1.15,1.4,ease(u)))
@scene('co_doi')
def _():
    bg=courtyard('skym',True)
    def fg(t,u,ms):
        o=birds(t,160,6,4,40)
        a=sstep(t,0.6,ms[-1]-.8)
        o+=flag(500,lerp(150,560,a),t,170,96,'#2e5aa0',480,0)+flag(1100,lerp(560,150,a),t,170,96,'#2f8f4a',480,1.2,trim='#f2c94c')
        for i in range(8): o+=P(260+i*160,860-(i%2)*30,1.3,t,'idle',p=i,robe=['#2e4a6a','#6a3a5a','#3a5a3a','#5a3a2a'][i%4],hat='cap',pose='bow',ang=10)
        return o
    return bg,fg,lambda u,t:(800,520,1.2+.15*u)
@scene('tha_toi')
def _():
    bg=courtyard('skyday',False)+'<g stroke="#2a1608" stroke-width="4"><rect x="560" y="300" width="480" height="300" fill="#8a7a62"/><rect x="700" y="400" width="200" height="200" fill="#1a1410"/></g>'
    def fg(t,u,ms):
        o='';a=sstep(t,.2,1.2)
        o+=f'<g stroke="{OUT}" stroke-width="4"><rect x="{700-120*a}" y="400" width="{100}" height="200" fill="#4a2c18"/><rect x="{800+120*a+0}" y="400" width="100" height="200" fill="#4a2c18"/></g>'
        for i in range(5):
            x=mv(t,1.0+i*.5,ms[-1]-.8,800,1300+i*110)
            o+=P(x,780+i*10,1.25,t,'walk' if t>1.0+i*.5 else 'idle',p=i,robe=['#8a7a62','#6a5a48','#7a6a52'][i%3],hat='bun',face=1,hands='sleeve') if t>1.0+i*.5 else ''
        o+=P(1000,800,1.4,t,'talk',robe='#4a525c',hat='helm',armor=True,trim='#b22a2a')
        o+=birds(t,200,6,5,70)
        return o
    return bg,fg,lambda u,t:(lerp(800,1000,u),540,1.4)
@scene('lap_thai_tu')
def _():
    bg=hall(dark=.05)+throne_back(800,640,k=1.5)
    def fg(t,u,ms):
        o=P(800,640,1.5,t,'talk',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='sleeve')+throne_front(800,640,k=1.5)
        a=sstep(t,.4,1.8)
        o+=P(lerp(1300,900,a),850,1.1,t,'walk' if a<1 else 'still',robe='#2f8f4a',trim='#e8c36a',hat='crown',pose='bow',ang=10+26*sstep(t,2,3.4) if a>=1 else 0,hands='sleeve',face=-1)
        o+=lamp_a(400,700,t,1.4)+lamp_a(1200,700,t,1.4,2)
        return o
    return bg,fg,lambda u,t:(850,520,lerp(1.25,1.45,u))
@scene('phong_thuong')
def _():
    bg=courtyard('skym',True)
    def fg(t,u,ms):
        o=flag(300,200,t,150,86,'#2f8f4a',300,0)+flag(1300,200,t,150,86,'#2f8f4a',300,2)+birds(t,150,4,2,40)
        # dòng 0: cô dâu (công chúa) và Đào Cam Mộc đứng cạnh nhau; dòng 1: quỳ nhận chức; dòng 2: đứng dậy giữa các quan
        o+=P(800,700,1.4,t,'still',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='sleeve',face=-1) if False else ''
        o+=P(1000,760,1.5,t,'talk',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='sleeve',face=-1)
        k=ph(ms,1,t)
        if t<ms[1]:
            o+=P(560,820,1.4,t,'idle',robe='#6a3a5a',trim='#e8c36a',hat='cap',hands='sleeve')+P(440,830,1.3,t,'idle',p=2,robe='#d96a8a',trim='#fff0a8',hat='bun',hands='sleeve')
            o+=sparks(t,500,700,10,2,120,'#ff9ab0')
        else:
            kneel=sstep(t,ms[1],ms[1]+1.2)*(1-sstep(t,ms[2]-.6,ms[2]+.4))
            o+=P(660,830,1.45,t,'still',robe='#6a3a5a',trim='#e8c36a',hat='cap',pose='kneelbow' if kneel>.5 else 'stand',ang=40*kneel,hands='sleeve')
            if t>ms[1]+.8: o+=f'<g transform="translate({lerp(940,720,sstep(t,ms[1]+.8,ms[1]+2.2)):.0f},{690:.0f})"><rect x="-26" y="-14" width="52" height="30" rx="6" fill="#d9a441" stroke="{OUT}" stroke-width="3"/></g>'
        for i in range(5):
            o+=P(220+i*60,900-(i%2)*20,1.2,t,'cheer' if t>ms[2] else 'idle',p=i,robe=['#2e4a6a','#3a5a3a','#5a3a2a'][i%3],hat='cap')
        return o
    return bg,fg,lambda u,t:(780,520,1.25)
@scene('nhin_xa')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skydusk)"/>'
    bg+=hill([(-400,560),(300,500),(800,540),(1300,490),(2000,540)],'#4a3a5a')+hill([(-400,640),(400,600),(900,640),(2000,610)],'#3a2f4a',1100)
    bg+='<rect x="-400" y="760" width="2400" height="500" fill="#2a2030"/><rect x="-400" y="740" width="2400" height="40" fill="#4a3a3a"/>'
    for i in range(14): bg+=f'<rect x="{-300+i*150}" y="740" width="14" height="80" fill="#3a2a2a"/>'
    for x,y,s in [(200,640,.8),(600,650,.7),(1250,640,.9),(1500,650,.7)]: bg+=house(x,y,s,roof='#3a2a2a',wall='#5a4a48')
    def fg(t,u,ms):
        o=clouds(t,150,3,'#ffe0c0',.6,6,2)+birds(t,260,5,3,30)
        o+=P(800,800,1.15,t,'idle',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='sleeve',face=-1)
        for x in (200,600,1250,1500): o+=f'<rect x="{x-14}" y="{560}" width="28" height="26" fill="#ffd27a" opacity="{.7+.2*math.sin(t*5+x):.2f}"/>'
        o+=smoke(1250,520,t,5,'#aaa',90,.25,8,10,.4)
        return o
    return bg,fg,lambda u,t:(800,520,lerp(1.5,1.1,ease(u)))
# ---------------- Chương 4
@scene('hoa_lu')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skyday)"/>'
    for x,h in [(-100,420),(160,380),(1420,440),(1700,400),(1000,300),(300,300),(600,260)]: bg+=karst(x,640,300+h*.3,h)
    for x,h in [(80,500),(1500,520),(800,330)]: bg+=karst(x,720,380,h,'#5a6a5a','#7a8a78')
    bg+='<rect x="-400" y="650" width="2400" height="600" fill="#9ccf72"/><path d="M-400,780 Q600,740 1000,790 T2000,770 L2000,860 L-400,860Z" fill="#4a86c0"/>'
    bg+=palace(800,700,360,170,'#8a2a1c')
    def fg(t,u,ms):
        o=clouds(t,110,4,'#fff',.9,9,3)+birds(t,230,6,3,40)
        o+=f'<g opacity=".55">'+''.join(f'<ellipse cx="{(i*340+t*14)%2300-300:.0f}" cy="{600+(i%3)*40}" rx="200" ry="26" fill="#fff"/>' for i in range(7))+'</g>'
        o+=boat(260+60*math.sin(t*.2),800,t,.7)+boat(1260,820,t,.6,p=2)
        # giặc kéo tới cửa núi, quay đầu (dòng 2)
        a=sstep(t,ms[1]+.2,ms[1]+3.2);b=sstep(t,ms[1]+3.4,ms[1]+6.4)
        if t>ms[1]:
            for i in range(6): o+=P(lerp(-150,360,a)-lerp(0,500,b)-i*46,840,.8,t,'walk' if a<1 or b>0 else 'idle',p=i,robe='#7a2a2a',hat='helm',armor=True,face=1 if b==0 else -1)
        return o
    return bg,fg,lambda u,t:(lerp(700,900,u),520,lerp(1.15,1.35,u))
@scene('kinh_do_mo')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skyday)"/>'+hill([(-400,520),(300,460),(900,500),(1500,450),(2000,500)],'#a0c49a')
    bg+='<rect x="-400" y="520" width="2400" height="700" fill="#b8d88a"/>'
    for ang,(x2,y2) in enumerate([(-300,420),(1900,420),(-300,1100),(1900,1100)]): bg+=f'<path d="M800,640 L{x2},{y2} L{x2},{y2+40} Z" fill="#d9c18a" opacity=".9"/>'
    bg+='<ellipse cx="800" cy="650" rx="360" ry="130" fill="#cdb98c" stroke="#8a7452" stroke-width="4"/>'
    for x,y,s in [(650,640,.8),(940,650,.8),(800,600,.7)]: bg+=house(x,y,s)
    bg+=palace(800,640,260,120)
    bg+='<path d="M-400,880 Q500,820 1000,880 T2000,860 L2000,1100 L-400,1100Z" fill="#4a86c0"/>'
    def fg(t,u,ms):
        o=clouds(t,110,3,'#fff',.9,10,4)+birds(t,230,4,6,50)
        for i in range(4):
            for j,(dx,dy) in enumerate([(-1,-.45),(1,-.45),(-1,.9),(1,.9)]):
                k=((t*.07)+(i/4)+j*.13)%1;x=800+dx*k*1400;y=660+dy*k*400
                o+=P(x,y+20,.5+k*.5,t,'walk',p=i+j,robe=['#8a5a3a','#3a5a3a','#6a3a5a'][(i+j)%3],hat='bun' if i%2 else 'cap',face=1 if dx<0 else -1)
        o+=boat(500+(t*50)%1300-100,930,t,.9)+boat(1500-(t*40)%1400,980,t,.8,face=-1,p=1)
        o+=beam(800,-60,60,500,800,'#fff3c0',.12)
        return o
    return bg,fg,lambda u,t:(800,520,lerp(1.1,1.4,ease(u)))
@scene('hoa_lu_am')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="#7a8a90"/>'
    for x,h in [(100,600),(420,640),(1180,640),(1500,600),(800,520)]: bg+=karst(x,720,420,h,'#4a5a52','#6a7a72')
    bg+='<rect x="-400" y="720" width="2400" height="600" fill="#55703f"/>'+palace(800,760,320,140,'#6a2a1c','#b8a078')
    def fg(t,u,ms):
        o=f'<g opacity=".6">'+''.join(f'<ellipse cx="{(i*300+t*18)%2300-300:.0f}" cy="{420+(i%4)*70}" rx="260" ry="34" fill="#dfe6e8"/>' for i in range(8))+'</g>'
        o+=rain(t,70,-200,1800,-60,900,.12,.45,6,700,36,'#dfe9f0')
        for i in range(6):
            u2=((t*.6)+i/6)%1;x=380+i*170;o+=f'<ellipse cx="{x}" cy="{770+u2*30:.0f}" rx="{10+u2*34:.0f}" ry="{3+u2*8:.0f}" fill="none" stroke="#e8f2ff" stroke-width="2" opacity="{1-u2:.2f}"/>'
        o+=P(800,880,1.0,t,'idle',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='sleeve')
        o+=fade(.18,'#103018')
        return o
    return bg,fg,lambda u,t:(800,560,lerp(1.2,1.6,ease(u)))
@scene('chuoi_vua')
def _():
    bg=hall(dark=.45)
    def fg(t,u,ms):
        o='';n=ms[-1]
        names=[('#6a3a5a'),('#6a3a5a'),('#2e4a9a'),('#2e4a9a'),('#2e4a9a')]
        for i in range(5):
            a=sstep(t,.4+i*(n-2)/6,1.2+i*(n-2)/6);x=250+i*275
            o+=f'<g opacity="{a:.2f}" transform="translate({x},{560-30*(1-a)})"><rect x="-80" y="0" width="160" height="40" rx="8" fill="#6a4228" stroke="{OUT}" stroke-width="3"/><g transform="translate(0,-10) scale(2)"><path d="M-30,10 L-30,-26 L-14,-8 L0,-34 L14,-8 L30,-26 L30,10Z" fill="#f2c94c" stroke="{OUT}" stroke-width="2.5"/><rect x="-30" y="6" width="60" height="10" fill="#d4a017" stroke="{OUT}" stroke-width="2.5"/></g></g>'
            # nến cháy ngắn
            h=lerp(110,28,sstep(t,.4+i*(n-2)/6,n))
            o+=f'<rect x="{x-12}" y="{560+40}" width="24" height="{h}" fill="#efe9dc" stroke="{OUT}" stroke-width="2"/>'+flame(x,560+40,t,.55,i)+glow(x,560+30,50,t,i,op=.6*a)
        return o
    return bg,fg,lambda u,t:(800,540,lerp(1.0,1.2,u))
