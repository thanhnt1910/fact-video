"""Cảnh vector CHUYỂN ĐỘNG cho video Lý Công Uẩn (ly1).
Mỗi cảnh = nền tĩnh (SVG -> ảnh, lưu đệm) + lớp động vẽ lại MỖI KHUNG theo thời gian t (người, lửa, cờ, sóng, mưa...).
Máy quay trượt/phóng trong thế giới 1600x900 (lề thêm 200 px mỗi phía). Không chữ, không máu."""
import io, math, random, functools
import cairosvg
from PIL import Image
import ly1_scenes as S
from ly1_scenes import person as _person, hall, col, couch, DEFS, OUT
VB=(-200,-112.5,2000,1125)   # vùng thế giới có nền
BGW=2800                     # độ rộng ảnh nền (px)
def clamp(x,a=0.0,b=1.0): return max(a,min(b,x))
def ease(x): x=clamp(x); return x*x*(3-2*x)
def lerp(a,b,x): return a+(b-a)*x
def seg(t,a,b): return clamp((t-a)/max(b-a,1e-6))
def sstep(t,a,b): return ease(seg(t,a,b))
def ph(ms,i,t):
    """tiến độ 0..1 trong dòng thứ i (0 = dòng đầu của cảnh)"""
    i=max(0,min(i,len(ms)-2));return seg(t,ms[i],ms[i+1])
# ---------------------------------------------------------------- người
PGAIN=1.3
def P(x,y,s=1.0,t=0.0,mode='idle',p=0.0,**kw):
    """mode: idle | walk | bow(ang=) | cheer | talk | still. x,y = giữa hai bàn chân."""
    dy=0;rot=0;kw=dict(kw);s=s*PGAIN
    if mode=='idle': dy=-1.6*s*abs(math.sin(t*1.5+p));rot=1.0*math.sin(t*1.1+p)
    elif mode=='walk': dy=-6*s*abs(math.sin(t*5.2+p));rot=3.2*math.sin(t*5.2+p)
    elif mode=='run': dy=-10*s*abs(math.sin(t*8+p));rot=5*math.sin(t*8+p)
    elif mode=='cheer':
        dy=-7*s*abs(math.sin(t*4+p));kw['hands']='up' if math.sin(t*4+p)>-0.2 else 'sleeve'
    elif mode=='talk':
        dy=-1.2*s*abs(math.sin(t*3+p));rot=2.0*math.sin(t*2.6+p)
        kw['hands']='hold' if math.sin(t*2.2+p)>0.2 else kw.get('hands','sleeve')
    f=kw.get('face',1)
    g=f'<g transform="translate({x:.1f},{y+dy:.1f}) rotate({rot*f:.2f})">'
    return g+_person(0,0,s,**kw)+'</g>'
def row(n,x0,x1,y,s,t,mode='idle',cols=None,hat='cap',seed=1,jit=8,**kw):
    r=random.Random(seed);cols=cols or ['#2e4a6a','#6a3a5a','#3a5a3a','#5a3a2a','#4a4a7a','#7a3a2a']
    o=''
    for i in range(n):
        x=x0+(x1-x0)*(i/(n-1) if n>1 else .5)+r.uniform(-jit,jit)
        o+=P(x,y+r.uniform(-4,4),s*r.uniform(.94,1.06),t,mode,p=r.uniform(0,6),robe=cols[(i+seed)%len(cols)],hat=hat,**kw)
    return o
# ---------------------------------------------------------------- hiệu ứng động
def flame(x,y,t,s=1.0,p=0.0):
    a=1+.14*math.sin(t*13+p)+.07*math.sin(t*7.3+p*2);b=1+.10*math.sin(t*11+p*1.7)
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s*b:.3f},{s*a:.3f})" stroke="none"><path d="M-9,0 q-12,-26 4,-44 q4,12 12,16 q10,-14 -2,-34 q26,18 14,44 q-4,14 -14,18Z" fill="#ffb938"/>'
            f'<path d="M-4,0 q-6,-16 2,-28 q10,10 4,28Z" fill="#fff3a8"/></g>')
def glow(x,y,r,t,p=0.0,col='fl',op=1.0):
    k=1+.07*math.sin(t*9+p)
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*k:.1f}" fill="url(#{col})" opacity="{op:.2f}"/>'
def lamp_a(x,y,t,s=1.0,p=0.0,gl=True):
    o=glow(x,y-20*s,75*s,t,p) if gl else ''
    o+=f'<g transform="translate({x},{y}) scale({s})" stroke="{OUT}" stroke-width="2"><path d="M-24,0 Q0,16 24,0 L18,-10 L-18,-10Z" fill="#a8742e"/></g>'
    return o+flame(x,y-10*s,t,s*.55,p)
def torch(x,y,t,s=1.0,p=0.0,h=70):
    return (f'<g transform="translate({x},{y})"><rect x="{-4*s}" y="0" width="{8*s}" height="{h*s}" rx="3" fill="#5a3a20" stroke="{OUT}" stroke-width="2"/></g>'
            +glow(x,y-14*s,60*s,t,p,op=.8)+flame(x,y+4*s,t,s*.9,p))
def flag(x,y,t,w=130,h=74,colr='#8f2d22',pole=260,p=0.0,amp=9,trim='#e8c36a'):
    pts_t=[];pts_b=[]
    for i in range(9):
        u=i/8;dy=amp*u*math.sin(u*4.2-t*4.5+p)
        pts_t.append((x+4+u*w,y+dy));pts_b.append((x+4+u*w,y+h+dy*1.1))
    d='M'+' L'.join(f'{a:.1f},{b:.1f}' for a,b in pts_t)+' L'+' L'.join(f'{a:.1f},{b:.1f}' for a,b in reversed(pts_b))+'Z'
    return (f'<rect x="{x-3}" y="{y-14}" width="7" height="{pole}" rx="3" fill="#5a3a20" stroke="{OUT}" stroke-width="2"/><circle cx="{x}" cy="{y-18}" r="7" fill="{trim}" stroke="{OUT}" stroke-width="2"/>'
            f'<path d="{d}" fill="{colr}" stroke="{OUT}" stroke-width="2.5" stroke-linejoin="round"/>')
def smoke(x,y,t,n=7,colr='#d9d4cc',h=170,spd=.35,r0=9,drift=26,op=.55):
    o=''
    for i in range(n):
        u=((t*spd)+i/n)%1.0
        o+=f'<circle cx="{x+math.sin(u*5+i)*drift*u:.1f}" cy="{y-u*h:.1f}" r="{r0+u*r0*2.2:.1f}" fill="{colr}" opacity="{op*(1-u)*min(1,u*6):.2f}"/>'
    return o
def cloud(x,y,s=1.0,colr='#fff',op=.9):
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s})" fill="{colr}" opacity="{op}"><ellipse cx="0" cy="0" rx="120" ry="34"/><ellipse cx="-60" cy="-22" rx="70" ry="32"/><ellipse cx="40" cy="-30" rx="80" ry="36"/></g>'
def clouds(t,y,n=4,colr='#fff',op=.85,spd=14,seed=3,s=1.0):
    r=random.Random(seed);o=''
    for i in range(n):
        x0=r.uniform(-300,1900);o+=cloud((x0+t*spd*r.uniform(.6,1.4))%2300-300,y+r.uniform(-50,60),s*r.uniform(.7,1.3),colr,op)
    return o
def stars(t,n=40,seed=7,y1=330,x0=-150,x1=1750):
    r=random.Random(seed);o=''
    for i in range(n):
        o+=f'<circle cx="{r.uniform(x0,x1):.0f}" cy="{r.uniform(-60,y1):.0f}" r="{r.uniform(1.2,3):.1f}" fill="#fff" opacity="{.35+.6*abs(math.sin(t*r.uniform(.8,2.4)+r.uniform(0,6))):.2f}"/>'
    return o
def rain(t,n=90,x0=-200,x1=1800,y0=-60,y1=960,slant=.35,op=.5,seed=5,spd=900,L=40,colr='#cfe4ff'):
    r=random.Random(seed);o=''
    for i in range(n):
        x=r.uniform(x0,x1);v=spd*r.uniform(.8,1.2);ph_=r.uniform(0,1)
        yy=y0+((t*v/(y1-y0)+ph_)%1.0)*(y1-y0);xx=x-slant*(yy-y0)*0.0+slant*(yy-y0)
        o+=f'<path d="M{xx:.0f},{yy:.0f} l{-slant*L:.0f},{L}" stroke="{colr}" stroke-width="2" opacity="{op}" stroke-linecap="round"/>'
    return o
def wave_band(y,t,amp,colr,x0=-300,x1=1900,k=.012,spd=1.6,bottom=1200,p=0.0):
    pts=[];x=x0
    while x<=x1:
        pts.append(f'{x},{y+amp*math.sin(x*k-t*spd+p)+amp*.4*math.sin(x*k*2.3-t*spd*1.3):.1f}');x+=40
    return f'<path d="M{x0},{bottom} L'+' L'.join(pts)+f' L{x1},{bottom}Z" fill="{colr}"/>'
def birds(t,y=150,n=5,seed=2,spd=60,colr='#2a2a30'):
    r=random.Random(seed);o=''
    for i in range(n):
        x=(r.uniform(-200,1800)+t*spd*r.uniform(.8,1.2))%2100-250;yy=y+r.uniform(-60,60)+10*math.sin(t*.8+i)
        f=math.sin(t*9+i*1.7)*10
        o+=f'<path d="M{x-16:.0f},{yy+f:.0f} Q{x-8:.0f},{yy-6:.0f} {x:.0f},{yy:.0f} Q{x+8:.0f},{yy-6:.0f} {x+16:.0f},{yy+f:.0f}" fill="none" stroke="{colr}" stroke-width="3" stroke-linecap="round"/>'
    return o
def boat(x,y,t,s=1.0,p=0.0,sail=True,face=1,colr='#7a4a2a',sailc='#d9c8a0'):
    rk=3.2*math.sin(t*1.3+p);dy=2.5*math.sin(t*1.8+p)
    o=f'<g transform="translate({x:.1f},{y+dy:.1f}) rotate({rk:.2f}) scale({s*face},{s})" stroke="{OUT}" stroke-width="3" stroke-linejoin="round">'
    o+=f'<path d="M-90,0 Q0,60 90,0 L70,-14 L-70,-14Z" fill="{colr}"/><rect x="-70" y="-18" width="140" height="8" fill="#5a3a20"/>'
    if sail: o+=f'<rect x="-3" y="-120" width="6" height="108" fill="#3a2210"/><path d="M4,-116 Q60,-80 62,-30 L4,-24Z" fill="{sailc}"/><path d="M-4,-106 Q-44,-76 -44,-30 L-4,-26Z" fill="#c9b890"/>'
    return o+'</g>'
def house(x,y,s=1.0,roof='#7a5a32',wall='#b89868',win=False,t=0,p=0):
    o=f'<g transform="translate({x},{y}) scale({s})" stroke="{OUT}" stroke-width="3" stroke-linejoin="round"><rect x="-70" y="-90" width="140" height="90" fill="{wall}"/><path d="M-100,-86 L0,-170 L100,-86 L72,-86 L0,-136 L-72,-86Z" fill="{roof}"/><path d="M-100,-86 L0,-170 L100,-86Z" fill="{roof}"/><rect x="-22" y="-62" width="44" height="62" fill="#4a3220"/></g>'
    if win: o+=glow(x,y-30*s,60*s,t,p,op=.7)
    return o
def pagoda(x,y,s=1.0,tiers=3,colr='#a8452c',roof='#5a3a2a'):
    o=f'<g transform="translate({x},{y}) scale({s})" stroke="{OUT}" stroke-width="3" stroke-linejoin="round">'
    h=0;w=110
    for i in range(tiers):
        o+=f'<rect x="{-w*.6}" y="{-h-70}" width="{w*1.2}" height="70" fill="{colr}"/><path d="M{-w},{-h-62} Q0,{-h-112} {w},{-h-62} L{w*.8},{-h-52} L{-w*.8},{-h-52}Z" fill="{roof}"/>'
        h+=84;w*=.78
    return o+f'<path d="M0,{-h-52} v-40" stroke="{OUT}" stroke-width="5"/></g>'
def tree(x,y,s=1.0,t=0,p=0,leaf='#4c8a3a',trunk='#5a3a20'):
    sw=2.2*math.sin(t*1.2+p)
    return (f'<g transform="translate({x},{y}) scale({s})" stroke="{OUT}" stroke-width="2.5"><rect x="-9" y="-90" width="18" height="90" fill="{trunk}"/>'
            f'<g transform="rotate({sw:.2f} 0 -90)"><ellipse cx="0" cy="-130" rx="62" ry="52" fill="{leaf}"/><ellipse cx="-32" cy="-108" rx="38" ry="30" fill="{leaf}"/><ellipse cx="34" cy="-112" rx="40" ry="32" fill="#5a9a46"/></g></g>')
def hill(pts,colr,y0=900):
    return f'<path d="M{pts[0][0]},{y0} L'+' L'.join(f'{a},{b}' for a,b in pts)+f' L{pts[-1][0]},{y0}Z" fill="{colr}"/>'
def karst(x,y,w,h,colr='#6a7a6a',colr2='#8a9a88'):
    return (f'<path d="M{x-w/2},{y} Q{x-w*.42},{y-h*.7} {x-w*.16},{y-h*.92} Q{x},{y-h*1.06} {x+w*.14},{y-h*.9} Q{x+w*.4},{y-h*.66} {x+w/2},{y}Z" fill="{colr}" stroke="#2f3a30" stroke-width="3"/>'
            f'<path d="M{x-w*.1},{y-h*.9} Q{x+w*.12},{y-h*.5} {x+w*.3},{y-h*.1} L{x+w*.1},{y}Z" fill="{colr2}" opacity=".55"/>')
def sparks(t,x,y,n=14,seed=1,r=140,colr='#ffd26a',spd=.9):
    rr=random.Random(seed);o=''
    for i in range(n):
        u=((t*spd)+rr.uniform(0,1))%1.0;a=rr.uniform(0,6.28);d=u*r*rr.uniform(.4,1)
        o+=f'<circle cx="{x+math.cos(a)*d:.0f}" cy="{y+math.sin(a)*d*.8-u*30:.0f}" r="{3.5*(1-u):.1f}" fill="{colr}" opacity="{1-u:.2f}"/>'
    return o
def dust(t,x0,x1,y0,y1,n=22,seed=4,colr='#fff',op=.45):
    r=random.Random(seed);o=''
    for i in range(n):
        x=r.uniform(x0,x1)+14*math.sin(t*.6+i);y=y0+((r.uniform(0,1)+t*.03*r.uniform(.5,1.4))%1.0)*(y1-y0)
        o+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.5,4):.1f}" fill="{colr}" opacity="{op*abs(math.sin(t+i)):.2f}"/>'
    return o
def beam(x,y,w0,w1,h,colr='#fff3c0',op=.25,angle=0):
    return f'<path d="M{x-w0/2},{y} L{x+w0/2},{y} L{x+w1/2},{y+h} L{x-w1/2},{y+h}Z" fill="{colr}" opacity="{op}" transform="rotate({angle} {x} {y})"/>'
def fade(op,colr='#000'):
    return f'<rect x="-400" y="-300" width="2400" height="1700" fill="{colr}" opacity="{clamp(op):.3f}"/>'
# ---------------------------------------------------------------- khung cảnh
def ext(inner):
    return (inner.replace('<rect width="1600" height="900" fill=','<rect x="-400" y="-300" width="2400" height="1700" fill=')
      .replace('<rect y="690" width="1600" height="210"','<rect x="-400" y="690" width="2400" height="500"')
      .replace('<rect y="640" width="1600" height="260"','<rect x="-400" y="640" width="2400" height="500"')
      .replace('<rect y="0" width="1600" height="300"','<rect x="-400" y="-300" width="2400" height="600"')
      .replace('<rect y="330" width="1600" height="570"','<rect x="-400" y="330" width="2400" height="900"')
      .replace('M0,300 Q800,250 1600,300 L1600,330 L0,330Z','M-400,300 Q800,250 2000,300 L2000,330 L-400,330Z'))
def svg_doc(inner,vb):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}">{DEFS}{inner}</svg>'
SCN={};_FACT={}
def scene(name):
    def deco(fn): _FACT[name]=fn;return fn
    return deco
def _get(name):
    if name not in SCN: SCN[name]=_FACT[name]()
    return SCN[name]
@functools.lru_cache(maxsize=3)
def _bg(name):
    bg,fg,cam=_get(name)
    svg=svg_doc(ext(bg),VB)
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=BGW,output_height=int(BGW*VB[3]/VB[2])))).convert('RGB')
_VIG={}
def _vig(W,H):
    if (W,H) not in _VIG:
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><defs><radialGradient id="v" cx=".5" cy=".5" r=".78"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient></defs><rect width="{W}" height="{H}" fill="url(#v)"/></svg>'
        _VIG[(W,H)]=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=W,output_height=H))).convert('RGBA')
    return _VIG[(W,H)]
def render(name,t,dur,W=1920,H=1080,ms=None):
    """khung ở thời điểm t (giây từ đầu cảnh). ms: mốc đầu mỗi dòng (giây, tính từ đầu cảnh) + hết cảnh."""
    bg,fg,cam=_get(name);u=clamp(t/max(dur,.01));ms=ms or [0,dur]
    cx,cy,z=cam(u,t)
    vw=1600/z;vh=900/z
    cx=max(VB[0]+vw/2,min(VB[0]+VB[2]-vw/2,cx));cy=max(VB[1]+vh/2,min(VB[1]+VB[3]-vh/2,cy))
    x0=cx-vw/2;y0=cy-vh/2
    B=_bg(name);k=B.width/VB[2]
    box=(int((x0-VB[0])*k),int((y0-VB[1])*k),int((x0-VB[0]+vw)*k),int((y0-VB[1]+vh)*k))
    im=B.crop(box).resize((W,H),Image.BILINEAR).convert('RGBA')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {vw:.2f} {vh:.2f}" width="{W}" height="{H}">{DEFS}{fg(t,u,ms)}</svg>'
    top=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=W,output_height=H))).convert('RGBA')
    im.alpha_composite(top);im.alpha_composite(_vig(W,H))
    return im.convert('RGB')
def sheet(name,dur=18.0,ms=None,us=(.08,.35,.62,.9),W=640,H=360,out=None):
    ims=[render(name,u*dur,dur,W,H,ms or [0,dur*.25,dur*.5,dur*.75,dur]) for u in us]
    cols=2;rows=(len(ims)+1)//2
    sh=Image.new('RGB',(W*cols,H*rows))
    for i,im in enumerate(ims): sh.paste(im,((i%cols)*W,(i//cols)*H))
    sh.save(out or f'/tmp/proto/an_{name}.jpg',quality=88);return out or f'/tmp/proto/an_{name}.jpg'
