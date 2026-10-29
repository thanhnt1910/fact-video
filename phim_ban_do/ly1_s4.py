"""Cảnh động chương 5–8 (dòng 57–86)."""
import base64
from ly1_anim import *
from ly1_s1 import throne_back,throne_front,mv,NIGHT_DEF
from ly1_s2 import drape,WHITE
from ly1_s3 import SKY_DEF,palace,courtyard,soldiers,room_bg
import ly1_svg as SV
@functools.lru_cache(maxsize=200)
def _dr64(phq,size=420):
    im=SV.dragon_png(phq,size);b=io.BytesIO();im.save(b,'PNG');return base64.b64encode(b.getvalue()).decode()
def dragon_img(x,y,t,w=300,rot=0.0,op=1.0,spd=6.0):
    phq=int(t*spd)%63;h=w*520/440
    return f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot:.1f})" opacity="{op:.2f}"><image x="{-w/2:.0f}" y="{-h*.25:.0f}" width="{w:.0f}" height="{h:.0f}" href="data:image/png;base64,{_dr64(phq)}"/></g>'
def wall_seg(x0,x1,ytop,ybot,col='#b99a64'):
    return f'<rect x="{x0}" y="{ytop}" width="{x1-x0}" height="{ybot-ytop}" fill="{col}" stroke="{OUT}" stroke-width="3"/>'+''.join(f'<path d="M{x0},{y} H{x1}" stroke="#8a7452" stroke-width="2"/>' for y in range(int(ytop)+30,int(ybot),30))
@scene('dap_thanh')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skyday)"/>'+hill([(-400,520),(300,470),(900,510),(1500,460),(2000,510)],'#8fb88a')
    bg+='<rect x="-400" y="560" width="2400" height="700" fill="#b8c88a"/><path d="M-400,820 Q500,780 1000,840 T2000,820 L2000,1100 L-400,1100Z" fill="#4a86c0"/>'
    bg+='<path d="M200,640 L1400,640" stroke="#a89468" stroke-width="40"/>'
    def fg(t,u,ms):
        o=clouds(t,110,3,'#fff',.85,9,3)+birds(t,200,4,3,40)
        h=lerp(0,230,sstep(t,.5,ms[-1]-1.0))
        o+=wall_seg(380,1220,700-h,700)
        if h>20: o+=''.join(f'<rect x="{x}" y="{700-h-22}" width="36" height="24" fill="#b99a64" stroke="{OUT}" stroke-width="3"/>' for x in range(380,1220,76))
        # giàn giáo và thợ khiêng gạch
        o+=f'<g stroke="{OUT}" stroke-width="4"><path d="M300,700 L300,430 M360,700 L360,430 M300,500 H360 M300,580 H360" fill="none" stroke="#7a5a32"/></g>'
        for i in range(6):
            k=((t*.12)+i/6)%1;x=1380-k*980
            o+=P(x,780,1.0,t,'walk',p=i,robe='#8a7a62',hat='bun',face=-1 if True else 1,hands='hold')
            o+=f'<rect x="{x-16:.0f}" y="{680:.0f}" width="34" height="22" fill="#c9a26a" stroke="{OUT}" stroke-width="2"/>'
        for i in range(5):
            k=((t*.1)+i/5)%1;x=380+k*840
            o+=P(x,700-h*(.2),.8,t,'walk',p=i+2,robe='#7a6a52',hat='bun',hands='hold') if h>30 else ''
        o+=P(1230,850,1.5,t,'talk',robe='#4a525c',hat='helm',armor=True,trim='#b22a2a',face=-1)
        o+=flag(1330,330,t,150,86,'#b22a2a',380,1)
        return o
    return bg,fg,lambda u,t:(lerp(760,860,u),560,1.25)
@scene('ben_song')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skyday)"/>'+hill([(-400,500),(400,450),(1000,490),(2000,450)],'#9cc29a')
    bg+='<rect x="-400" y="500" width="2400" height="700" fill="#b8d88a"/>'
    bg+='<path d="M-400,720 Q500,660 1000,720 T2000,700 L2000,1100 L-400,1100Z" fill="#4a86c0"/><path d="M-400,720 Q500,660 1000,720 T2000,700 L2000,740 Q1000,760 -400,740Z" fill="#a89468"/>'
    for x,y,s in [(220,660,.8),(420,650,.8),(1250,660,.9),(1460,650,.8)]: bg+=house(x,y,s)
    bg+=palace(800,640,360,150,'#8a2a1c')
    bg+='<g stroke="#4a2c18" stroke-width="3"><rect x="560" y="740" width="480" height="20" fill="#7a5a32"/><rect x="580" y="760" width="12" height="40" fill="#5a3a20"/><rect x="1000" y="760" width="12" height="40" fill="#5a3a20"/></g>'
    def fg(t,u,ms):
        o=clouds(t,100,3,'#fff',.85,9,2)+birds(t,200,5,2,40)
        o+=wave_band(900,t,6,'#3a76b0',-300,1900,.02,1.4,1100)
        for i,(x,y,s,p) in enumerate([(300,850,1.2,0),(780,940,1.4,1),(1300,880,1.1,2),(1520,960,1.0,3)]): o+=boat(((x+t*25*(1 if i%2==0 else -1))%2000)-200,y,t,s,p)
        for i in range(8):
            k=((t*.09)+i/8)%1;x=560+k*480
            o+=P(x,740,.9,t,'walk',p=i,robe=['#8a5a3a','#3a5a3a','#6a3a5a'][i%3],hat='bun',hands='hold')
        for i in range(5):
            x=1080+i*60;o+=P(x,760,.9,t,'idle',p=i,robe=['#2e4a6a','#6a3a5a','#3a5a3a'][i%3],hat='cap',face=-1)
        return o
    return bg,fg,lambda u,t:(lerp(800,900,u),620,lerp(1.4,1.15,ease(u)))
@scene('soan_chieu')
def _():
    bg='<rect width="1600" height="900" fill="#241a14"/><rect y="640" width="1600" height="260" fill="#3a2a1c"/><rect x="520" y="200" width="560" height="320" fill="#33261c" stroke="#1a100a" stroke-width="6"/>'
    bg+='<g stroke="#2a1608" stroke-width="4"><rect x="340" y="600" width="920" height="40" rx="6" fill="#6a4228"/><rect x="380" y="640" width="30" height="120" fill="#4a2c18"/><rect x="1190" y="640" width="30" height="120" fill="#4a2c18"/></g>'
    bg+='<g stroke="#2a1608" stroke-width="4"><path d="M330,372 Q800,350 1270,372 L1270,600 Q800,620 330,600Z" fill="#f1e2b4"/><rect x="296" y="352" width="44" height="270" rx="20" fill="#c9a26a"/><rect x="1260" y="352" width="44" height="270" rx="20" fill="#c9a26a"/></g>'
    rnd=random.Random(9)
    for c in range(8):
        x=360+c*115;bg+=f'<g stroke="#3a2a1c" stroke-width="4" stroke-linecap="round" opacity=".5">'+''.join(f'<path d="M{x},{385+r*28} h{rnd.randint(50,86)}"/>' for r in range(8))+'</g>'
    def fg(t,u,ms):
        o=glow(800,480,520,t,0,op=.5)
        # chữ hiện dần (vệt mực) theo thời gian
        n=ms[-1];prog=sstep(t,.5,n-1)
        rnd=random.Random(5)
        for c in range(8):
            x=360+c*115
            for r in range(8):
                f=(c*8+r)/64
                if f<prog: o+=f'<path d="M{x},{385+r*28} h{rnd.randint(50,86)}" stroke="#1a0e06" stroke-width="5" stroke-linecap="round" opacity=".85"/>'
        # bút lông
        bx=420+prog*800;by=400+((prog*8)%1)*210
        o+=f'<g transform="translate({bx:.0f},{by:.0f}) rotate(-24)"><rect x="-6" y="-120" width="12" height="130" rx="5" fill="#7a4a22" stroke="{OUT}" stroke-width="3"/><path d="M-8,10 l8,26 l8,-26z" fill="#1a0e06"/></g>'
        o+=P(800,920,1.25,t,'still',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='hold',pose='stand')
        o+=lamp_a(500,330,t,1.9)+lamp_a(1100,330,t,1.5,2)+dust(t,300,1300,100,600,22,3,'#ffe9a0',.5)
        return o
    return bg,fg,lambda u,t:(800,560,lerp(1.15,1.45,ease(u)))
def castle(x,y,s=1.0,col='#cfae78'):
    return f'<g transform="translate({x},{y}) scale({s})" stroke="{OUT}" stroke-width="3" stroke-linejoin="round"><rect x="-50" y="-80" width="100" height="80" fill="{col}"/><path d="M-62,-80 L0,-130 L62,-80Z" fill="#a8261c"/><rect x="-12" y="-44" width="24" height="44" fill="#3a2210"/></g>'
@scene('doi_do_xua')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="#e8d9b4"/><rect x="40" y="60" width="1520" height="780" fill="#f2e6c4" stroke="#8a7452" stroke-width="8" rx="20"/>'
    bg+='<path d="M60,700 Q400,640 800,700 T1540,680" fill="none" stroke="#8fb8d8" stroke-width="40" opacity=".7"/>'
    pts=[(220,640),(480,420),(760,560),(1020,360),(1300,520),(1480,300)]
    def fg(t,u,ms):
        o=''
        n=ms[-1];m=len(pts)
        prog=sstep(t,.4,n-1.2)*(m-1)
        d='M'+' L'.join(f'{x},{y}' for x,y in pts)
        o+=f'<path d="{d}" fill="none" stroke="#a8261c" stroke-width="7" stroke-dasharray="22 16" stroke-dashoffset="{-t*30:.0f}" opacity=".8"/>'
        for i,(x,y) in enumerate(pts):
            a=sstep(prog,i-.4,i+.1);o+=f'<g opacity="{a:.2f}" transform="translate(0,{(1-a)*-30:.0f})">'+castle(x,y,1.5,'#cfae78' if i<5 else '#9ab8d8')+'</g>'
        i0=min(int(prog),m-2);f=prog-i0;cx=lerp(pts[i0][0],pts[i0+1][0],f);cy=lerp(pts[i0][1],pts[i0+1][1],f)
        o+=f'<g transform="translate({cx:.0f},{cy-10+3*math.sin(t*8):.0f})" stroke="{OUT}" stroke-width="3"><rect x="-26" y="-30" width="52" height="30" rx="6" fill="#7a4a22"/><circle cx="-14" cy="4" r="10" fill="#4a2c18"/><circle cx="14" cy="4" r="10" fill="#4a2c18"/></g>'
        o+=P(cx-70,pts[i0][1]+90 if False else cy+60,.7,t,'walk',robe='#8a5a3a',hat='bun')
        return o
    return bg,fg,lambda u,t:(800,450,1.0+.12*u)
@scene('nen_ngan')
def _():
    bg=hall(dark=.55)
    def fg(t,u,ms):
        o='';n=ms[-1]
        for i,(x,rate) in enumerate([(560,1.0),(1040,.55)]):
            h=max(14,lerp(260,14,seg(t,.3,n*rate)))
            o+=f'<rect x="{x-24}" y="{780-h}" width="48" height="{h}" rx="6" fill="#efe9dc" stroke="{OUT}" stroke-width="3"/>'
            if h>14.5: o+=glow(x,780-h-20,120,t,i,op=.8)+flame(x,780-h,t,1.3,i)
            else: o+=smoke(x,740,t,5,'#aaa',150,.5,8,18,.5)
            o+=''.join(f'<ellipse cx="{x-24+((k*37)%48)}" cy="{780-h+ (k*17+t*20)%max(h,1):.0f}" rx="4" ry="8" fill="#efe9dc" opacity=".7"/>' for k in range(2))
        o+=P(800,900,1.0,t,'idle',robe='#2e4a9a',hat='crown',hands='sleeve',face=1) if False else ''
        return o
    return bg,fg,lambda u,t:(800,560,lerp(1.3,1.5,u))
@scene('the_dat')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skyday)"/>'
    bg+=hill([(-400,520),(300,470),(700,510),(1000,430),(1400,500),(2000,450)],'#8fb88a')
    bg+='<rect x="-400" y="560" width="2400" height="700" fill="#b8d88a"/>'
    bg+='<path d="M-400,760 Q200,640 500,720 T1000,700 T1500,780 T2000,720 L2000,830 Q1500,860 1200,800 T700,800 T200,760 L-400,860Z" fill="#4a86c0"/>'
    bg+=karst(1400,600,380,300,'#a07a52','#c09a70')
    bg+=palace(700,640,300,120,'#8a2a1c')
    def fg(t,u,ms):
        o=clouds(t,110,3,'#fff',.85,9,3)+birds(t,200,5,3,40)
        a=sstep(t,.8,3.0)
        o+=dragon_img(560,420-30*math.sin(t*.8),t,330,rot=18,op=.9*a,spd=5)
        # hổ ngồi: bóng cam trên đồi
        o+=f'<g transform="translate(1400,430)" stroke="{OUT}" stroke-width="3" opacity="{a:.2f}"><path d="M-70,60 Q-80,-20 -30,-50 Q-10,-80 20,-50 Q70,-30 60,60Z" fill="#e8943a"/><path d="M-20,-10 q10,18 20,0 M10,0 q10,18 20,0" fill="none" stroke="#3a1c08" stroke-width="5"/><circle cx="0" cy="-34" r="6" fill="#fff"/></g>'
        return o
    return bg,fg,lambda u,t:(lerp(700,860,u),520,1.15)
@scene('hoi_quan')
def _():
    bg=hall(dark=.1)+throne_back(800,560,k=1.4)
    def fg(t,u,ms):
        o=P(800,560,1.4,t,'talk',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='hold')+throne_front(800,560,k=1.4)
        bw=sstep(t,ms[1],ms[1]+1.0)*(1-sstep(t,ms[2]-.2,ms[2]+.6))
        for i in range(4):
            for sd in (-1,1):
                x=800+sd*(220+i*110);o+=P(x,820+(i%2)*40,1.1,t,'still',robe=['#2e4a6a','#6a3a5a','#3a5a3a','#5a3a2a'][i],hat='cap',pose='bow',ang=8+34*bw,hands='sleeve',face=-sd)
        if t>ms[2]: o+=sparks(t,800,330,12,2,160)+glow(800,420,260,t,0,op=.4*sstep(t,ms[2],ms[2]+1))
        o+=lamp_a(300,700,t,1.4)+lamp_a(1300,700,t,1.4,2)
        return o
    return bg,fg,lambda u,t:(800,470,lerp(1.2,1.4,ease(u)))
@scene('rong_vang')
def _():
    bg=SKY_DEF+'<rect x="-400" y="-300" width="2400" height="1700" fill="url(#skydusk)"/>'+hill([(-400,600),(300,540),(900,590),(1500,530),(2000,590)],'#3a3050')
    bg+='<rect x="-400" y="720" width="2400" height="500" fill="#2a2438"/><path d="M-400,800 Q500,760 1000,810 T2000,790 L2000,1100 L-400,1100Z" fill="#3a5a8a"/>'
    bg+=wall_seg(420,1180,560,740,'#9a8660')+''.join(f'<rect x="{x}" y="538" width="36" height="24" fill="#9a8660" stroke="{OUT}" stroke-width="3"/>' for x in range(420,1180,76))+palace(800,560,260,120,'#7a2a1c','#b09468')
    def fg(t,u,ms):
        o=stars(t,30,5,300)
        o+=boat(520,830,t,1.1,sail=True)+f'<g stroke="{OUT}" stroke-width="3">'+P(520,810,.6,t,'idle',robe='#c9a441',hat='crown')+'</g>'
        o+=f'<path d="M-400,820 Q500,800 1000,830" stroke="#fff" stroke-width="2" opacity=".2" fill="none"/>'
        k=ms[1] if len(ms)>2 else ms[-1]*.35
        rise=sstep(t,.8,ms[-1]*.65)
        y=lerp(840,260,rise);x=lerp(1050,900,rise)
        o+=glow(x,y,260,t,0,op=.6*rise)+dragon_img(x,y,t,lerp(200,480,rise),rot=lerp(0,-4,rise)+3*math.sin(t*1.2),op=sstep(t,.5,1.5),spd=6)
        o+=sparks(t,x,y,20,4,260)
        o+=wave_band(860,t,6,'#2e4a7a',-300,1900,.018,1.3,1200)
        return o
    return bg,fg,lambda u,t:(lerp(800,860,u),520,lerp(1.2,1.0,ease(u)))
@scene('xay_dien')
def _():
    bg=courtyard('skyday',False)+'<rect x="500" y="540" width="600" height="30" fill="#b8942a" stroke="#2a1608" stroke-width="3"/>'
    def fg(t,u,ms):
        n=ms[-1];g=sstep(t,.4,n*.8)
        o=clouds(t,100,3,'#fff',.8,8,4)+birds(t,180,4,2,40)
        # cung điện dựng lên: cột trước, mái hạ xuống
        for i in range(7):
            cx=520+i*(560/6);hh=lerp(0,240,sstep(g,i*.06,i*.06+.35))
            o+=f'<rect x="{cx-11}" y="{540-hh}" width="22" height="{hh}" fill="#8f2d22" stroke="{OUT}" stroke-width="2.5"/>'
        wall_h=lerp(0,230,sstep(g,.4,.7))
        o+=f'<rect x="530" y="{540-wall_h}" width="540" height="{wall_h}" fill="#e0c088" opacity=".9"/>'
        roof=sstep(g,.65,1.0);ry=lerp(-60,0,roof)
        o+=f'<g transform="translate(0,{(1-roof)*-300:.0f})" opacity="{min(1,roof*3):.2f}"><path d="M450,{300+ry} Q800,{180+ry} 1150,{300+ry} L1130,{330+ry} L470,{330+ry}Z" fill="#a8261c" stroke="{OUT}" stroke-width="3"/><path d="M530,{262+ry} Q800,{150+ry} 1070,{262+ry} L1050,{286+ry} L550,{286+ry}Z" fill="#c33a2a" stroke="{OUT}" stroke-width="3"/></g>'
        # cần trục / dây kéo và thợ
        o+=f'<path d="M300,540 L300,200 L700,200" fill="none" stroke="#5a3a20" stroke-width="12"/><path d="M700,200 L{700+(1-roof)*100:.0f},{300-(1-roof)*100:.0f}" stroke="#3a2a1c" stroke-width="4"/>'
        for i in range(6):
            k=((t*.1)+i/6)%1;x=1300-k*900
            o+=P(x,820+(i%2)*40,1.05,t,'walk',p=i,robe='#8a7a62',hat='bun',hands='hold',face=-1)
        for i in range(3): o+=P(560+i*220,600,.8,t,'talk',p=i,robe='#6a5a48',hat='bun',hands='hold')
        o+=P(1300,860,1.4,t,'talk',robe='#2e4a6a',hat='cap',hands='hold',face=-1)
        o+=sparks(t,800,540,8,6,120,'#d9c8a0') if g<.95 else ''
        return o
    return bg,fg,lambda u,t:(lerp(760,840,u),560,1.2)
@scene('dao_hao')
def _():
    bg=courtyard('skyday',False)+wall_seg(-300,1900,360,560,'#b99a64')
    def fg(t,u,ms):
        n=ms[-1];w=sstep(t,.5,n-.8)
        o=clouds(t,100,3,'#fff',.8,8,5)
        o+=f'<path d="M-300,760 H{-300+w*2200:.0f} V900 H-300Z" fill="#4a86c0"/><path d="M-300,760 H1900 V900 H-300Z" fill="#6a5a3a" opacity="{1-w*0:.2f}" style="display:none"/>'
        o+=f'<path d="M-300,740 H1900 V780 H-300Z" fill="#6a5a3a"/>'
        for i in range(9):
            k=((t*.12)+i/9)%1;x=-100+k*2000
            o+=P(x,780+(i%3)*50,1.0,t,'walk',p=i,robe='#8a7a62',hat='bun',hands='hold',face=1)
        o+=f'<path d="M-300,{790} H{-300+w*2200:.0f}" stroke="#a8d4f0" stroke-width="3" opacity=".7" stroke-dasharray="12 10" stroke-dashoffset="{-t*40:.0f}"/>'
        o+=flag(300,200,t,150,86,'#2f8f4a',300,0)+flag(1300,200,t,150,86,'#2f8f4a',300,1.5)
        o+=P(900,720,1.2,t,'talk',robe='#2e4a6a',hat='cap',hands='hold')
        return o
    return bg,fg,lambda u,t:(lerp(500,1100,ease(u)),560,1.15)
@scene('bon_cua')
def _():
    # nhìn từ trên cao toàn thành, bốn cửa sáng lên lần lượt, cửa tây (Quảng Phúc) nhấp nháy cuối
    bg='<rect x="-400" y="-300" width="2400" height="1700" fill="#9bc86a"/><path d="M-400,700 Q300,640 800,720 T2000,680 L2000,1100 L-400,1100Z" fill="#8bb85a"/>'
    bg+='<path d="M-400,560 Q200,540 420,600 T900,780 T2000,860 L2000,930 L900,860 T420,700 Q200,640 -400,640Z" fill="#4a86c0" opacity=".9"/>'
    bg+='<g stroke="#3a2210" stroke-width="4"><rect x="300" y="110" width="1000" height="700" fill="#4a86c0"/><rect x="330" y="140" width="940" height="640" fill="#cfae78"/><rect x="354" y="164" width="892" height="592" fill="#b99a64"/></g>'
    def hallb(x,y,w,h): return f'<g stroke="#3a1008" stroke-width="3"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e0c088"/><path d="M{x-14},{y} Q{x+w/2},{y-44} {x+w+14},{y} L{x+w+6},{y+14} L{x-6},{y+14}Z" fill="#a8261c"/><path d="M{x-6},{y-16} Q{x+w/2},{y-62} {x+w+6},{y-16} L{x+w},{y-6} L{x},{y-6}Z" fill="#c33a2a"/></g>'
    bg+=hallb(690,420,220,90)+hallb(500,430,120,70)+hallb(980,430,120,70)+hallb(700,250,200,80)+hallb(700,560,110,60)+hallb(850,560,110,60)
    bg+='<path d="M800,170 V250 M800,330 V420 M800,510 V560 M800,620 V750 M600,465 H690 M910,465 H980" stroke="#8a6a3a" stroke-width="18" stroke-linecap="round" opacity=".7"/>'
    bg+='<g fill="#4c8a3a" stroke="#2f5a24" stroke-width="2">'+''.join(f'<ellipse cx="{x}" cy="{y}" rx="26" ry="18"/>' for x,y in [(420,220),(1180,220),(420,700),(1180,700),(560,640),(1040,630)])+'</g>'
    gates=[(800,148,'đông'),(800,772,'nam'),(346,448,'tây'),(1254,448,'bắc')]
    def fg(t,u,ms):
        o='';n=ms[-1]
        for i,(x,y,nm) in enumerate(gates):
            a=sstep(t,.6+i*(n*.55)/4,1.4+i*(n*.55)/4)
            pulse=.5+.5*math.sin(t*5) if (i==2 and t>n*.6) else 1
            o+=f'<circle cx="{x}" cy="{y}" r="{60+30*a*pulse}" fill="url(#fl)" opacity="{a*.9:.2f}"/><rect x="{x-24}" y="{y-20}" width="48" height="40" rx="6" fill="#ffcf4a" stroke="{OUT}" stroke-width="3" opacity="{a:.2f}"/>'
        for i in range(10):
            k=((t*.05)+i/10)%1;o+=P(800+(-1)**i*(60+k*0)+0,170+k*580,.45,t,'walk',p=i,robe=['#8a5a3a','#3a5a3a','#6a3a5a'][i%3],hat='bun')
        o+=boat(1450,330,t,.5)
        return o
    return bg,fg,lambda u,t:(lerp(800,560,ease(u)),470,lerp(1.05,1.45,ease(u)))
@scene('mien_thue')
def _():
    bg=courtyard('skyday',False)+'<g stroke="#2a1608" stroke-width="4"><rect x="560" y="440" width="480" height="130" fill="#e0c088"/><path d="M520,440 Q800,360 1080,440Z" fill="#a8261c"/></g>'
    def fg(t,u,ms):
        o=clouds(t,100,3,'#fff',.8,8,5)+birds(t,170,5,3,40)
        o+=P(800,600,1.35,t,'talk',robe='#6a3a5a',hat='cap',hands='hold')
        o+=f'<g transform="translate(790,500)"><rect x="-70" y="-6" width="140" height="44" rx="6" fill="#f1e2b4" stroke="{OUT}" stroke-width="3"/><rect x="-80" y="-12" width="16" height="56" rx="8" fill="#c9a26a" stroke="{OUT}" stroke-width="3"/><rect x="64" y="-12" width="16" height="56" rx="8" fill="#c9a26a" stroke="{OUT}" stroke-width="3"/></g>'
        n=ms[-1];cheer=sstep(t,n*.45,n*.5)
        for i in range(10):
            x=300+(i%5)*190+(60 if i>=5 else 0)
            y=840+(i//5)*50
            rb=['#8a7a62','#6a5a48','#7a6a52'][i%3]
            o+=P(x,y,1.1,t,'cheer' if cheer>.5 else 'idle',p=i,robe=rb,hat='bun' if i%2 else 'bald',face=1 if x<800 else -1)
        o+=sparks(t,800,620,16,2,260) if cheer>.5 else ''
        return o
    return bg,fg,lambda u,t:(800,620,lerp(1.25,1.4,u))
@scene('su_tong')
def _():
    bg=hall(dark=.1)+throne_back(1000,600,k=1.3)
    def fg(t,u,ms):
        o=P(1000,600,1.3,t,'talk',robe='#f2c94c',trim='#fff2a8',hat='crown',hands='hold')+throne_front(1000,600,k=1.3)
        a=sstep(t,.3,2.0)
        o+=P(lerp(-200,520,a),840,1.4,t,'walk' if a<1 else 'talk',robe='#a8261c',trim='#f2c94c',hat='cap',hands='hold',face=1)
        for i in range(3): o+=P(lerp(-400,360-i*100,a),870-i*10,1.1,t,'walk' if a<1 else 'idle',p=i,robe='#b8402c',hat='helm',armor=True,face=1)
        if a>=1: o+=f'<g transform="translate({lerp(640,860,sstep(t,ms[1]-1,ms[1]+1)):.0f},{690-30*math.sin(sstep(t,ms[1]-1,ms[1]+1)*3.14):.0f})"><rect x="-30" y="-20" width="60" height="40" rx="6" fill="#d9a441" stroke="{OUT}" stroke-width="3"/><rect x="-14" y="-32" width="28" height="16" rx="4" fill="#f2c94c" stroke="{OUT}" stroke-width="3"/></g>'
        for i in range(3): o+=P(1300+i*90,850,1.1,t,'idle',p=i,robe=['#2e4a6a','#3a5a3a','#5a3a2a'][i],hat='cap',face=-1)
        o+=flag(260,160,t,150,86,'#a8261c',320,0)+flag(1380,160,t,150,86,'#2f8f4a',320,1)
        o+=lamp_a(300,700,t,1.3)
        return o
    return bg,fg,lambda u,t:(820,580,lerp(1.2,1.4,u))
