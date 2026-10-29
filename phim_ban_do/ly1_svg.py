"""Hình vector (SVG -> PNG bằng cairosvg) cho video Lý Công Uẩn: rồng vàng, tranh Hoa Lư, tranh Đại La."""
import math, io, functools
import cairosvg
from PIL import Image
def _png(svg,w,h):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=w,output_height=h))).convert('RGBA')
def _spine(ph,N=56,L=360):
    P=[]
    for i in range(N):
        p=i/(N-1); y=p*L; x=math.sin(p*7.5-ph)*(10+80*p)+p*p*20; P.append((x,y,p))
    return P
def _offs(P,side):
    out=[]
    for i,(x,y,p) in enumerate(P):
        a=P[min(i+1,len(P)-1)];b=P[max(i-1,0)]; dx,dy=a[0]-b[0],a[1]-b[1]; n=math.hypot(dx,dy) or 1
        w=(30-24*p)+2; out.append((x+side*(-dy/n)*w, y+side*(dx/n)*w))
    return out
@functools.lru_cache(maxsize=400)
def dragon_png(phq,size=520):
    ph=phq/10.0; P=_spine(ph); l=_offs(P,1); r=_offs(P,-1)
    body='M'+' L'.join('%.1f,%.1f'%q for q in l)+' L'+' L'.join('%.1f,%.1f'%q for q in reversed(r))+' Z'
    spikes=''.join('<path d="M%.1f,%.1f l-11,-5 l5,-11 z" fill="#ffe27a" stroke="#8a5208" stroke-width="1.2"/>'%(l[i][0],l[i][1]) for i in range(3,len(P)-6,3))
    scales=''.join('<path d="M%.1f,%.1f q%.1f,7 %.1f,0" fill="none" stroke="#c98a14" stroke-width="2" opacity=".7"/>'%(P[i][0]-9,P[i][1],9,18) for i in range(2,len(P)-4,2))
    belly=' '.join('%.1f,%.1f'%(P[i][0],P[i][1]) for i in range(1,len(P)-3))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-210 -130 440 520">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#f6c33c"/><stop offset=".5" stop-color="#ffd966"/><stop offset="1" stop-color="#d9981a"/></linearGradient>
<radialGradient id="h"><stop offset="0" stop-color="#fff2b0"/><stop offset="1" stop-color="#f0b429"/></radialGradient>
<filter id="gl"><feGaussianBlur stdDeviation="9"/></filter></defs>
<path d="{body}" fill="#ffd34a" opacity=".55" filter="url(#gl)"/>
<path d="{body}" fill="url(#g)" stroke="#8a5208" stroke-width="3.5" stroke-linejoin="round"/>
{scales}{spikes}
<polyline points="{belly}" fill="none" stroke="#fff0b8" stroke-width="5" stroke-linecap="round" opacity=".7"/>
<g transform="translate(0,-4) rotate(-8)">
 <path d="M-20,-14 C-52,-26 -78,-60 -70,-100 M-46,-34 C-62,-44 -86,-40 -100,-56 M-34,-22 C-48,-24 -66,-14 -84,-20" fill="none" stroke="#b9770e" stroke-width="9" stroke-linecap="round"/>
 <path d="M-20,-14 C-52,-26 -78,-60 -70,-100 M-46,-34 C-62,-44 -86,-40 -100,-56 M-34,-22 C-48,-24 -66,-14 -84,-20" fill="none" stroke="#ffe27a" stroke-width="4.5" stroke-linecap="round"/>
 <path d="M-36,-24 C-52,-8 -50,22 -30,34 C-44,44 -34,62 -14,56 C-40,30 -40,-4 -24,-18Z" fill="#ff9d2e" stroke="#8a5208" stroke-width="2.5"/>
 <path d="M-30,-8 C-34,-40 0,-52 34,-40 C62,-32 88,-22 112,-12 C120,-6 118,2 108,6 L50,14 C56,30 24,44 -2,36 C-24,30 -32,10 -30,-8Z" fill="url(#h)" stroke="#8a5208" stroke-width="3.5" stroke-linejoin="round"/>
 <path d="M108,8 C86,20 58,26 34,30 C60,46 98,40 118,22Z" fill="#f0b429" stroke="#8a5208" stroke-width="3" stroke-linejoin="round"/>
 <path d="M64,15 l6,10 l6,-10 M86,12 l5,9 l5,-10" fill="#fff" stroke="#8a5208" stroke-width="1.5"/>
 <circle cx="116" cy="-6" r="3" fill="#8a5208"/>
 <path d="M18,-34 C28,-52 44,-58 56,-52" fill="none" stroke="#8a5208" stroke-width="5" stroke-linecap="round"/>
 <path d="M14,-18 L40,-26 L36,-6 L16,-2Z" fill="#fffbe6" stroke="#8a5208" stroke-width="2.5"/>
 <ellipse cx="28" cy="-14" rx="9" ry="9" fill="#e23b1e"/><circle cx="28" cy="-14" r="4.5" fill="#1a0c02"/><circle cx="30" cy="-17" r="2" fill="#fff"/>
 <path d="M112,-6 C140,-26 176,-16 196,-38 M112,6 C146,24 176,12 200,34" fill="none" stroke="#fff0b8" stroke-width="3.5" stroke-linecap="round"/>
</g>
</svg>'''
    return _png(svg,size,int(size*520/440))
def _clouds(x,y,s=1,op=.9):
    return f'<g opacity="{op}" transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="0" rx="50" ry="16" fill="#fff"/><ellipse cx="-22" cy="-10" rx="26" ry="14" fill="#fff"/><ellipse cx="18" cy="-12" rx="30" ry="16" fill="#fff"/></g>'
@functools.lru_cache(maxsize=2)
def hoa_lu_png(w=820,h=560):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 560">
<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b97a8"/><stop offset=".6" stop-color="#c9ced0"/><stop offset="1" stop-color="#e5e3d6"/></linearGradient>
<linearGradient id="k1" x1="0" x2="1"><stop offset="0" stop-color="#4f5a63"/><stop offset=".6" stop-color="#6c7780"/><stop offset="1" stop-color="#3f484f"/></linearGradient>
<linearGradient id="k2" x1="0" x2="1"><stop offset="0" stop-color="#798792"/><stop offset="1" stop-color="#59656e"/></linearGradient></defs>
<rect width="820" height="560" fill="url(#s)"/>
<path d="M0,330 C60,250 110,230 150,290 C190,200 240,190 275,300 C330,230 380,250 410,320 C470,210 530,220 560,310 C620,240 690,230 740,300 C770,270 800,280 820,300 L820,560 L0,560Z" fill="url(#k2)" opacity=".75"/>
<path d="M-10,560 L-10,300 C20,170 60,110 90,150 C120,190 140,330 170,560Z" fill="url(#k1)"/>
<path d="M210,560 C230,330 250,140 290,70 C330,120 350,300 380,560Z" fill="url(#k1)"/>
<path d="M560,560 C590,320 620,170 660,90 C700,150 720,330 740,560Z" fill="url(#k1)"/>
<path d="M700,560 C730,400 770,250 830,200 L830,560Z" fill="url(#k1)"/>
<g fill="#5e8a4a" opacity=".85"><ellipse cx="80" cy="200" rx="26" ry="9"/><ellipse cx="290" cy="130" rx="18" ry="7"/><ellipse cx="660" cy="150" rx="20" ry="7"/></g>
<rect x="0" y="440" width="820" height="120" fill="#7fa266"/>
<path d="M0,500 C150,470 260,520 410,495 C560,470 690,520 820,490 L820,560 L0,560Z" fill="#6a9158"/>
<g stroke="#4a3220" stroke-width="3" stroke-linejoin="round"><rect x="360" y="420" width="110" height="52" fill="#b99a6a"/><path d="M345,424 L415,372 L485,424Z" fill="#8a4a30"/><rect x="402" y="440" width="26" height="32" fill="#4a3220"/></g>
<path d="M0,540 C120,520 200,552 330,534" fill="none" stroke="#6aa0cf" stroke-width="10" opacity=".8"/>
<g fill="#fff" opacity=".55"><ellipse cx="170" cy="380" rx="150" ry="14"/><ellipse cx="620" cy="410" rx="170" ry="12"/></g>
{_clouds(560,60,1.1,.7)}</svg>'''
    return _png(svg,w,h)
@functools.lru_cache(maxsize=2)
def dai_la_png(w=820,h=560):
    roof=lambda x,y,s=1:f'<g transform="translate({x},{y}) scale({s})" stroke="#5a3418" stroke-width="3" stroke-linejoin="round"><rect x="-44" y="-30" width="88" height="46" fill="#d9b982"/><path d="M-62,-30 Q0,-82 62,-30 Q0,-52 -62,-30Z" fill="#a8452c"/><path d="M-50,-52 Q0,-100 50,-52 Q0,-70 -50,-52Z" fill="#b95333"/><rect x="-10" y="-8" width="20" height="24" fill="#5a3418"/></g>'
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 560">
<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fb2e8"/><stop offset="1" stop-color="#e8f3fb"/></linearGradient>
<linearGradient id="r" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a9ad0"/><stop offset="1" stop-color="#3f78ac"/></linearGradient></defs>
<rect width="820" height="560" fill="url(#s)"/>
<circle cx="680" cy="90" r="36" fill="#fff3b0"/>
{_clouds(160,80,1.1)}{_clouds(470,130,.8,.8)}
<path d="M0,300 C100,270 200,285 300,292 C420,280 520,270 640,288 C720,280 780,285 820,290 L820,330 L0,330Z" fill="#8aa6b8" opacity=".55"/>
<rect x="0" y="320" width="820" height="240" fill="#8fc46d"/>
<path d="M0,360 C200,340 400,372 820,350 L820,560 L0,560Z" fill="#7bb85a"/>
<path d="M-20,470 C140,420 250,500 420,470 C580,440 690,420 840,460 L840,520 C690,480 580,500 420,525 C250,550 140,470 -20,525Z" fill="url(#r)"/>
<path d="M60,490 q40,-8 80,0 M300,500 q40,-8 80,0 M560,470 q40,-8 80,0" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/>
<rect x="190" y="380" width="440" height="60" fill="#c9a870" stroke="#5a3418" stroke-width="3"/>
<g stroke="#5a3418" stroke-width="2" opacity=".5">{''.join(f'<line x1="{x}" y1="380" x2="{x}" y2="440"/>' for x in range(230,630,40))}</g>
{roof(410,372,1.45)}{roof(290,382,.9)}{roof(530,382,.9)}
<g><rect x="408" y="236" width="3" height="40" fill="#5a3418"/><path d="M411,238 l34,10 l-34,10z" fill="#2f8f4a"/></g>
<g fill="#4c8a3a" stroke="#2f5a24" stroke-width="2"><ellipse cx="90" cy="410" rx="30" ry="22"/><ellipse cx="740" cy="405" rx="34" ry="24"/><ellipse cx="130" cy="430" rx="22" ry="16"/></g>
<g><path d="M560,500 q30,-34 70,0 z" fill="#8a5a2c" stroke="#4a2c12" stroke-width="3"/><rect x="594" y="466" width="3" height="34" fill="#4a2c12"/><path d="M597,468 l22,8 l-22,8z" fill="#2f8f4a"/></g></svg>'''
    return _png(svg,w,h)
