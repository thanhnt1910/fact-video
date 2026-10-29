"""Hiệu ứng thêm cho video Lý Công Uẩn: vệt đường đi (sóng nước, bụi ngựa), rồng vàng Thăng Long, thẻ so sánh Hoa Lư – Đại La."""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W,H=1920,1080
FONT=os.environ.get('FONT','')
def _f(sz,bold=False):
    try:
        f=ImageFont.truetype(FONT,sz)
        try: f.set_variation_by_axes([700 if bold else 500])
        except Exception: pass
        return f
    except Exception: return ImageFont.load_default()
def clamp(x): return max(0.0,min(1.0,x))
def ease(x): x=clamp(x); return x*x*(3-2*x)
GOLD=(236,186,52)
# (tên đội, kiểu vệt)
TRAILS={'Thuyền vua ra Đại La':'ripple','Đoàn vua về Cổ Pháp':'dust'}
def trail(lay,t,v,groups,pp):
    d=ImageDraw.Draw(lay,'RGBA')
    for g in groups:
        kind=TRAILS.get(g.name.strip())
        if not kind: continue
        a,b=g.show[0],g.show[1]
        if not(a<=t<=b+3.0): continue
        te=min(t,b); n=int((te-a)/0.12)+1; pts=[]
        for i in range(max(0,n-130),n):
            tt=min(te,a+i*0.12); lo,la,_=pp(g.keys,tt); x,y=v.sc(lo,la); pts.append((tt,x,y))
        fade=1.0-clamp((t-b)/3.0)
        # đường nét đứt vàng
        for i in range(len(pts)-1):
            if i%2: continue
            age=t-pts[i][0]; al=int(220*fade*max(0.25,1-age/16.0))
            d.line([pts[i][1:],pts[i+1][1:]],fill=GOLD+(al,),width=6)
        for (tt,x,y) in pts[::3]:
            age=t-tt
            if age<0: continue
            if kind=='ripple':
                r=10+age*26; al=int(150*fade*clamp(1-age/3.2))
                if al>4: d.ellipse((x-r,y-r*0.45,x+r,y+r*0.45),outline=(255,255,255,al),width=2)
            else:
                r=6+age*14; al=int(130*fade*clamp(1-age/2.4)); rr=random.Random(int(tt*100))
                if al>4: d.ellipse((x-r+rr.uniform(-6,6),y-r*0.8-age*8,x+r+rr.uniform(-6,6),y+r*0.1-age*8),fill=(196,168,120,al))
def dragon(lay,t,v,t0,loc,dur=6.0):
    if not(t0<=t<=t0+dur): return
    x0,y0=v.sc(*loc); u=(t-t0)/dur; fi=ease(u/0.15)*(1-ease((u-0.82)/0.18)); A=int(255*fi)
    import ly1_svg as SV
    rise=ease(u)*260; hx=x0+math.sin(u*5)*14; hy=y0-40-rise
    sz=int(360+60*ease(u)); dr=SV.dragon_png(int(u*70)%62*1+int(u*40),sz) if False else SV.dragon_png(int(u*110)%63,sz)
    if A<255: dr=dr.copy(); dr.putalpha(dr.split()[3].point(lambda q:int(q*A/255)))
    gl=dr.filter(ImageFilter.GaussianBlur(16)); gl.putalpha(gl.split()[3].point(lambda q:int(q*0.7)))
    px=int(hx-0.40*sz); py=int(hy-0.22*sz*520/440)
    lay.alpha_composite(gl,(px,py)) if 0<=px<W-gl.width and 0<=py<H-gl.height else None
    lay.alpha_composite(dr,(px,py)) if 0<=px<W-dr.width and 0<=py<H-dr.height else None
    if 0.12<u<0.88:
        f=_f(28); tx='theo sử cũ: rồng vàng hiện lên'; dd=ImageDraw.Draw(lay,'RGBA'); tw=dd.textlength(tx,font=f)
        k=ease((u-0.12)/0.1)*(1-ease((u-0.8)/0.08)); ox=int(x0-tw/2); oy=int(y0+70)
        ox=max(60,min(W-60-int(tw),ox))
        dd.rounded_rectangle((ox-16,oy-6,ox+tw+16,oy+44),12,fill=(28,20,12,int(215*k)),outline=(246,238,214,int(230*k)),width=2)
        dd.text((ox,oy),tx,font=f,fill=(250,244,226,int(255*k)))
def _panel_hoa_lu(d,x0,x1,y0,y1):
    d.rectangle((x0,y0,x1,y1),fill=(70,76,92)); 
    for i,(b,h,c) in enumerate([(0,0.62,(54,60,76)),(60,0.8,(44,50,66)),(150,0.55,(58,64,80)),(260,0.9,(40,46,62)),(380,0.7,(52,58,74)),(520,0.85,(42,48,64)),(660,0.6,(56,62,78))]):
        bx=x0+b*(x1-x0)/870; w=(x1-x0)*0.34; top=y1-(y1-y0)*h
        d.polygon([(bx-w/2,y1),(bx-w*0.15,top+30),(bx,top),(bx+w*0.2,top+50),(bx+w/2,y1)],fill=c)
    cx=(x0+x1)/2; cy=y1-90
    d.rectangle((cx-70,cy,cx+70,cy+60),fill=(150,126,92),outline=(60,40,20),width=3)
    d.polygon([(cx-84,cy),(cx,cy-46),(cx+84,cy)],fill=(110,70,50),outline=(60,40,20))
def _panel_dai_la(d,x0,x1,y0,y1):
    d.rectangle((x0,y0,x1,y1),fill=(168,206,236))
    d.rectangle((x0,y1-(y1-y0)*0.45,x1,y1),fill=(126,176,96))
    pts=[(x0+i*(x1-x0)/12,y1-(y1-y0)*0.18+math.sin(i*0.9)*26) for i in range(13)]
    d.line(pts,fill=(70,128,190),width=44); d.line(pts,fill=(120,170,220),width=30)
    cx=(x0+x1)/2; cy=y1-(y1-y0)*0.40
    d.rectangle((cx-150,cy,cx+150,cy+70),fill=(206,170,110),outline=(110,70,40),width=3)
    for k in (-110,0,110):
        d.rectangle((cx+k-26,cy-34,cx+k+26,cy),fill=(190,150,100),outline=(110,70,40),width=2)
        d.polygon([(cx+k-34,cy-34),(cx+k,cy-66),(cx+k+34,cy-34)],fill=(160,60,40),outline=(110,70,40))
def compare(lay,t,t0,t1):
    if not(t0<=t<=t1): return
    k=min(clamp((t-t0)/0.5),clamp((t1-t)/0.4)); k=ease(k)
    card=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(card,'RGBA')
    d.rectangle((0,0,W,H),fill=(14,12,10,150))
    for (x0,x1,ttl,sub,fn) in [(110,930,'HOA LƯ','núi đá bao quanh, chật hẹp, khó mở rộng',_panel_hoa_lu),(990,1810,'ĐẠI LA','rồng cuộn hổ ngồi, rộng mà bằng phẳng',_panel_dai_la)]:
        y0,y1=250,810
        import ly1_svg as SV
        pan=(SV.hoa_lu_png() if ttl=='HOA LƯ' else SV.dai_la_png()).resize((x1-x0,y1-y0))
        card.paste(pan,(x0,y0),pan); d.rectangle((x0,y0,x1,y1),outline=(250,244,226,255),width=6)
        f=_f(64,True); tw=d.textlength(ttl,font=f); d.text(((x0+x1)/2-tw/2,172),ttl,font=f,fill=(250,222,120,255),stroke_width=3,stroke_fill=(30,20,10,255))
        f2=_f(34); tw=d.textlength(sub,font=f2)
        if tw>x1-x0-20: f2=_f(30); tw=d.textlength(sub,font=f2)
        d.rounded_rectangle(((x0+x1)/2-tw/2-16,826,(x0+x1)/2+tw/2+16,880),12,fill=(28,20,12,230),outline=(246,238,214,230),width=2)
        d.text(((x0+x1)/2-tw/2,832),sub,font=f2,fill=(250,244,226,255))
    # dịch vào từ hai bên
    off=int((1-k)*140); lay.alpha_composite(card.crop((0,0,W,H)),(0,off)) if False else None
    a=card.split()[3].point(lambda q:int(q*k)); card.putalpha(a); lay.alpha_composite(card,(0,off))
def apply_map(out,t,v,groups,pp,C):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); trail(lay,t,v,groups,pp)
    t_d=C.at(75,'Thăng Long'); dragon(lay,t,v,t_d,C.DL)
    return Image.alpha_composite(out,lay)
def apply_top(out,t,C):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); compare(lay,t,*C.COMPARE)
    return Image.alpha_composite(out,lay)

# ===================== DỜI ĐÔ: mũi tên chỉ đường chạy, đoàn thuyền và dân đi theo =====================
def _poly_len(P):
    L=[0.0]
    for i in range(1,len(P)): L.append(L[-1]+math.hypot(P[i][0]-P[i-1][0],P[i][1]-P[i-1][1]))
    return L
def _at(P,L,s):
    s=max(0.0,min(L[-1],s))
    for i in range(1,len(P)):
        if s<=L[i]:
            f=(s-L[i-1])/max(L[i]-L[i-1],1e-6); x=P[i-1][0]+(P[i][0]-P[i-1][0])*f; y=P[i-1][1]+(P[i][1]-P[i-1][1])*f
            a=math.atan2(P[i][1]-P[i-1][1],P[i][0]-P[i-1][0]); return x,y,a
    return P[-1][0],P[-1][1],0.0
def _smooth(P,n=10):
    out=[]
    for i in range(len(P)-1):
        a,b=P[i],P[i+1]
        for k in range(n): f=k/n; out.append((a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f))
    out.append(P[-1]); return out
def _boat(d,x,y,a,S,bob,col):
    c,s=math.cos(a),math.sin(a)
    def T(px,py): return (x+(px*c-py*s)*S, y+bob+(px*s+py*c)*S)
    d.polygon([T(-16,2),T(18,2),T(12,9),T(-12,9)],fill=(122,74,40,255),outline=(50,28,10,255))
    d.line([T(0,2),T(0,-24)],fill=(50,28,10,255),width=int(2*S)+1)
    d.polygon([T(2,-23),T(16,-8),T(2,-4)],fill=(238,226,190,255),outline=(60,40,20,255))
    d.polygon([T(-2,-23),T(-12,-12),T(-2,-6)],fill=col+(255,),outline=(60,40,20,255))
def _walker(d,x,y,S,ph,robe,helm=False):
    bob=abs(math.sin(ph))*3*S; y=y-bob
    d.ellipse((x-6*S,y+8*S,x+6*S,y+11*S),fill=(0,0,0,70))
    d.polygon([(x-6*S,y+8*S),(x-4.5*S,y-8*S),(x+4.5*S,y-8*S),(x+6*S,y+8*S)],fill=robe+(255,),outline=(40,24,10,255))
    d.ellipse((x-4.5*S,y-17*S,x+4.5*S,y-8*S),fill=(232,195,154,255),outline=(40,24,10,255))
    d.polygon([(x-5*S,y-14*S),(x,y-22*S),(x+5*S,y-14*S)],fill=((110,120,132) if helm else (30,30,36))+(255,))
    k=math.sin(ph)*3.5*S; d.line([(x-2*S,y+8*S),(x-2*S+k,y+13*S)],fill=(40,24,10,255),width=int(2*S)+1); d.line([(x+2*S,y+8*S),(x+2*S-k,y+13*S)],fill=(40,24,10,255),width=int(2*S)+1)
def dode(out,t,v,C,pp=None):
    t0=C.R(72,-0.2); t1=C.E(72,0.3)
    if not(t0-0.6<=t<=t1+1.2): return out
    Q=[(C.H[0]+0.02,C.H[1]+0.05),(106.10,20.80),(105.95,20.93),(105.88,21.00)]
    P=_smooth([v.sc(lo,la)[:2] for lo,la in Q],12); L=_poly_len(P)
    S2_=2; lay=Image.new('RGBA',(W*S2_,H*S2_),(0,0,0,0)); d=ImageDraw.Draw(lay,'RGBA')
    P2=[(x*S2_,y*S2_) for x,y in P]; L2=[l*S2_ for l in L]
    u=clamp((t-t0-0.5)/max(t1-t0-3.0,1.0)); u=0.85*u+0.15*ease(u); head=u*L2[-1]; fade=ease((t-(t0-0.6))/0.6)*(1-ease((t-t1)/1.2))
    A=int(255*fade); sc=S2_*1.0
    # vệt đứt vàng đã đi qua
    n=int(head/24)
    for i in range(0,n,2):
        x1,y1,_=_at(P2,L2,i*24); x2,y2,_=_at(P2,L2,min(head,i*24+14)); d.line([(x1,y1),(x2,y2)],fill=GOLD+(int(190*fade),),width=int(6*sc))
    # mũi tên chạy dọc đường (phía trước đoàn): chevron trôi về Đại La
    off=(t*90*S2_)%(70*S2_); s=head+30*S2_+off-70*S2_
    while s<L2[-1]-10*S2_:
        if s>head:
            x,y,a=_at(P2,L2,s); al=int(A*max(0,min(1,1-(s-head)/(260*S2_)))*0.95)
            c,sn=math.cos(a),math.sin(a); w=24*sc
            pts=[(x+c*w-sn*w,y+sn*w+c*w),(x+c*w*1.6,y+sn*w*1.6),(x+c*w+sn*w,y+sn*w-c*w),(x+c*w*0.6+sn*w*0.6,y+sn*w*0.6-c*w*0.6),(x+c*w*0.9,y+sn*w*0.9),(x+c*w*0.6-sn*w*0.6,y+sn*w*0.6+c*w*0.6)]
            d.polygon(pts,fill=(255,214,90,al),outline=(150,96,10,al))
        s+=70*S2_
    # đích Đại La: vòng sáng nhấp nháy
    ex,ey=P2[-1]; pul=0.5+0.5*math.sin(t*4)
    for r,al in ((40,150),(62,90)): d.ellipse((ex-r*sc*(0.8+0.2*pul),ey-r*sc*(0.8+0.2*pul),ex+r*sc*(0.8+0.2*pul),ey+r*sc*(0.8+0.2*pul)),outline=GOLD+(int(al*fade),),width=int(4*sc))
    # quân và dân đi bộ ven bờ (lệch 34px về một phía), đoàn thuyền trên sông
    for k in range(12):
        s=max(0.0,head-(40+k*46)*S2_)
        x,y,a=_at(P2,L2,s); nx,ny=-math.sin(a),math.cos(a); side=1 if k%2 else -1
        _walker(d,x+nx*(34+(k%3)*8)*sc*side,y+ny*(34+(k%3)*8)*sc*side,sc*1.7,t*7+k*1.3,[(150,60,50),(60,90,140),(60,120,70),(150,110,50),(110,70,130)][k%5],helm=(k%4==0))
    for k in range(5):
        s=max(0.0,head-(8+k*72)*S2_)
        x,y,a=_at(P2,L2,s); _boat(d,x,y,a*0.6,sc*1.7,math.sin(t*3+k)*3*sc,[(190,40,40),(40,120,70),(200,160,40)][k%3])
    lay=lay.resize((W,H),Image.LANCZOS)
    return Image.alpha_composite(out,lay)
