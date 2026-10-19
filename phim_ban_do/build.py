import json,math,re,subprocess,sys,wave
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
W,H,FPS=1920,1080,30
WT='/tmp/wt'
FONT=WT+'/assets/fonts/Lora-Variable.ttf'
def font(sz,bold=True):
    f=ImageFont.truetype(FONT,sz)
    try: f.set_variation_by_name('Bold' if bold else 'Regular')
    except Exception: pass
    return f
d=json.load(open('/tmp/TQ45_long_moi.json'))
beats=[b['text'] for c in d['long']['chapters'] for b in c['beats']]
FIRST,LAST=128,143
import os
HAI=json.load(open('/home/claude/fact-video/ke-hoach/thu-giong-hai/habi.json'))
texts={b['n']:b['text'] for b in HAI}
def dur(t): return max(3.2,len(t.split())/2.7+0.7)
D={n:dur(t) for n,t in texts.items()}
VDIR=os.environ.get('VOICE_DIR','')
if VDIR and os.path.exists(VDIR+'/thoi_luong.json'):
    _d=json.load(open(VDIR+'/thoi_luong.json'));D={n:_d[str(n)]+0.45 for n in texts}
# thời điểm bắt đầu mỗi câu
T={};t=0.5
for n in range(FIRST,LAST+1): T[n]=t;t+=D[n]
TOTAL=t+1.0
print('tổng',round(TOTAL,1),'giây')
ease=lambda x:0.5-0.5*math.cos(math.pi*min(1,max(0,x)))
clamp=lambda x:min(1,max(0,x))

# ---------- chuyển động máy quay: (zoom0,zoom1,cx0,cy0,cx1,cy1) cx,cy là tâm khung (0..1)
CAM={
128:(1.00,1.18,.5,.5,.50,.42),   # tiến vào cảnh trao chức
131:(1.05,1.05,.30,.5,.70,.5),    # lướt qua hai người
132:(1.0,1.2,.35,.55,.30,.48),   # theo con ngựa
133:(1.15,1.0,.5,.5,.5,.5),      # kéo xa: bên bờ sông
134:(1.0,1.18,.65,.5,.70,.45),   # tiến vào người mặc áo trắng
135:(1.18,1.0,.45,.5,.55,.5),    # kéo xa khỏi lá thư
136:(1.0,1.15,.55,.5,.62,.45),
137:(1.0,1.0,.40,.5,.62,.5),     # lướt qua đám lính cầm đuốc
138:(1.0,1.22,.35,.55,.32,.40),  # tiến vào tướng cầm kích
139:(1.0,1.18,.55,.55,.55,.45),
140:(1.0,1.2,.35,.55,.35,.42),
141:(1.22,1.0,.5,.55,.5,.5),     # kéo xa: sân vắng, mất thành
142:(1.0,1.12,.5,.5,.5,.5),
143:(1.0,1.2,.5,.55,.52,.60),    # tiến vào cổng thành
128.5:None}
CAM[129]=(1.0,1.1,.5,.5,.5,.5)
CAM[130]=(1.0,1.15,.35,.55,.30,.5)
def cam(n,u):
    z0,z1,x0,y0,x1,y1=CAM[n]; e=ease(u)
    z=z0+(z1-z0)*e;cx=x0+(x1-x0)*e;cy=y0+(y1-y0)*e
    return z,cx,cy
IMG={n:Image.open(f'{WT}/assets/anh_2d/TQ45_V2/{n:03d}.jpg').convert('RGB').resize((1920,1080),Image.LANCZOS) for n in range(FIRST,LAST+1)}
def img_frame(n,u):
    z,cx,cy=cam(n,u); w=1920/z;h=1080/z
    x0=min(max(cx*1920-w/2,0),1920-w);y0=min(max(cy*1080-h/2,0),1080-h)
    return IMG[n].resize((W,H),Image.BICUBIC,box=(x0,y0,x0+w,y0+h))

# ---------- bản đồ
LON0,LON1,LAT0,LAT1=114.6,121.0,31.9,35.4
KX=740/(LAT1-LAT0)  # px / độ vĩ
KXLON=KX*math.cos(math.radians(33.7))
MW=(LON1-LON0)*KXLON
OX=(W-MW)/2
def P(lon,lat): return (OX+(lon-LON0)*KXLON, 125+(LAT1-lat)*KX)
CITY={'Thọ Xuân':(116.78,32.6),'Hạ Bì':(117.95,34.3),'Hu Di':(118.52,33.0),'Hoài Âm':(119.02,33.58),'Tiểu Bái':(116.93,34.73)}
HUAI=[(114.6,32.45),(115.7,32.65),(116.8,32.95),(117.7,33.05),(118.3,33.3),(118.85,33.45),(119.3,33.5),(119.8,33.85),(120.25,34.2)]
SI=[(116.9,35.4),(117.3,35.0),(117.7,34.6),(117.95,34.3),(118.15,33.9),(118.3,33.3)]
COAST=[(119.35,35.4),(119.35,34.8),(119.7,34.4),(120.3,33.9),(120.6,33.2),(121.0,32.7),(121.0,31.9)]
def build_map_base():
    rng=np.random.default_rng(3)
    base=np.zeros((H,W,3),np.float32); base[:]=(222,203,160)
    yy,xx=np.mgrid[0:H,0:W]
    v=((xx-W/2)/(W*0.62))**2+((yy-H/2)/(H*0.7))**2
    base*= (1-0.38*np.clip(v,0,1.4))[...,None]
    base+= rng.normal(0,5,(H,W,1))
    im=Image.fromarray(np.clip(base,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    g=ImageDraw.Draw(im,'RGBA')
    # biển
    poly=[P(*p) for p in COAST]+[(W,125+(LAT1-31.9)*KX),(W,0),P(119.35,35.4)]
    g.polygon(poly,fill=(120,150,160,170))
    g.line([P(*p) for p in COAST],fill=(70,90,95,255),width=4,joint='curve')
    # sông
    g.line([P(*p) for p in HUAI],fill=(88,130,150,255),width=9,joint='curve')
    g.line([P(*p) for p in SI],fill=(88,130,150,255),width=6,joint='curve')
    # lưới
    for lon in np.arange(115,121.1,1): g.line([P(lon,LAT0),P(lon,LAT1)],fill=(90,70,40,40),width=1)
    for lat in np.arange(32,35.5,0.5): g.line([P(LON0,lat),P(LON1,lat)],fill=(90,70,40,40),width=1)
    fb=font(26);g.text(P(119.55,32.55),'HOÀI HÀ',font=fb,fill=(60,100,120,255)); 
    g.text(P(119.7,34.9),'BIỂN ĐÔNG',font=fb,fill=(235,245,250,230))
    g.text(P(117.05,34.95),'TỨ THỦY',font=font(20,False),fill=(60,100,120,255))
    return im
MAPBASE=build_map_base()
RED=(168,48,40);BLUE=(36,84,150);GOLD=(184,134,28);INK=(52,36,20)
def arrow(g,pts,u,col,w=10):
    # vẽ mũi tên mọc dần theo u
    seg=[math.dist(pts[i],pts[i+1]) for i in range(len(pts)-1)];tot=sum(seg);L=tot*u
    out=[pts[0]];acc=0
    for i,s in enumerate(seg):
        if acc+s<=L: out.append(pts[i+1]);acc+=s
        else:
            r=(L-acc)/s;out.append((pts[i][0]+(pts[i+1][0]-pts[i][0])*r,pts[i][1]+(pts[i+1][1]-pts[i][1])*r));break
    if len(out)>1:
        g.line(out,fill=col+(255,),width=w,joint='curve')
        if u>0.98:
            (x0,y0),(x1,y1)=out[-2],out[-1];a=math.atan2(y1-y0,x1-x0)
            tri=[(x1+math.cos(a)*26,y1+math.sin(a)*26),(x1+math.cos(a+2.5)*24,y1+math.sin(a+2.5)*24),(x1+math.cos(a-2.5)*24,y1+math.sin(a-2.5)*24)]
            g.polygon(tri,fill=col+(255,))
def label(g,xy,txt,col,size=34,anchor='l',alpha=1.0,sub=None):
    f=font(size);b=g.textbbox((0,0),txt,font=f);w=b[2]-b[0];h=b[3]-b[1]
    x,y=xy
    if anchor=='r': x-=w
    if anchor=='m': x-=w/2
    pad=10
    g.rounded_rectangle((x-pad,y-pad/2,x+w+pad,y+h+pad+(28 if sub else 0)),8,fill=(245,235,205,int(235*alpha)),outline=col+(int(255*alpha),),width=3)
    g.text((x,y-4),txt,font=f,fill=col+(int(255*alpha),))
    if sub: g.text((x,y+h+4),sub,font=font(22,False),fill=INK+(int(255*alpha),))
def dot(g,xy,col,pulse=0,r=14):
    x,y=xy
    if pulse: g.ellipse((x-r-pulse*22,y-r-pulse*22,x+r+pulse*22,y+r+pulse*22),outline=col+(int(200*(1-pulse)),),width=4)
    g.ellipse((x-r,y-r,x+r,y+r),fill=col+(255,),outline=(255,250,235,255),width=3)
def map_frame(t,phase):
    """phase 1: Viên Thuật → Hu Di, Lưu Bị cự địch; phase 2: Lữ Bố đánh úp Hạ Bì. t: giây trong khối"""
    im=MAPBASE.copy();g=ImageDraw.Draw(im,'RGBA')
    ft=font(54);title='SÁU THÁNG ĐẦU NĂM 196 · TỪ CHÂU'
    tw=g.textlength('TỪ CHÂU · NĂM 196',font=ft)
    g.text((W-60-tw,34),'TỪ CHÂU · NĂM 196',font=ft,fill=INK+(255,))
    g.text((W-60-250,98),'vị trí vẽ gần đúng',font=font(22,False),fill=INK+(200,))
    pul=(t*0.9)%1
    for name,(lo,la) in CITY.items():
        xy=P(lo,la); col=INK
        if name=='Hạ Bì': col=GOLD
        dot(g,xy,col,r=11)
        if name in('Hạ Bì','Thọ Xuân','Hu Di','Hoài Âm','Tiểu Bái'):
            off={'Hạ Bì':(24,-8),'Thọ Xuân':(-210,20),'Hu Di':(-112,6),'Hoài Âm':(22,-52),'Tiểu Bái':(-150,-14)}[name]
            g.text((xy[0]+off[0],xy[1]+off[1]),name,font=font(32),fill=INK+(255,))
    xT=P(*CITY['Thọ Xuân']);xH=P(*CITY['Hu Di']);xI=P(*CITY['Hoài Âm']);xB=P(*CITY['Hạ Bì'])
    if phase==1:
        u=ease((t-1.0)/2.4)
        if u>0:
            dot(g,xT,RED,pulse=pul,r=17)
            arrow(g,[xT,(P(117.6,32.75)),(P(118.2,32.95)),xH],u,RED)
            label(g,(xT[0]-20,xT[1]+44),'Viên Thuật',RED,36,alpha=clamp((t-1.0)/0.6),sub='đem quân từ Thọ Xuân')
        u2=ease((t-3.4)/1.0)
        if u2>0:
            mid=((xH[0]+xI[0])/2,(xH[1]+xI[1])/2)
            dot(g,xH,BLUE,pulse=pul,r=17);dot(g,xI,BLUE,r=13)
            g.line([xH,xI],fill=BLUE+(255,),width=8)
            label(g,(xH[0]+70,xH[1]+95),'Lưu Bị cự địch',BLUE,36,alpha=u2,sub='Hu Di – Hoài Âm · suốt một tháng')
        u3=ease((t-5.2)/1.0)
        if u3>0:
            dot(g,xB,GOLD,pulse=pul,r=17)
            label(g,(xB[0]+60,xB[1]+10),'Hạ Bì: phía sau',GOLD,34,alpha=u3,sub='Tào Báo giữ thành')
    else:
        dot(g,xB,GOLD,r=17);dot(g,xH,BLUE,r=13);dot(g,xI,BLUE,r=13)
        g.line([xH,xI],fill=BLUE+(180,),width=7)
        label(g,(xH[0]+40,xH[1]+30),'Lưu Bị ở xa',BLUE,30)
        u=ease((t-0.8)/2.2)
        a=P(115.75,35.25)
        arrow(g,[a,P(116.6,34.9),P(117.3,34.55),xB],u,(30,30,30),w=12)
        if u>0.3: label(g,(a[0]-330,a[1]+75),'Lữ Bố đánh úp',(30,30,30),38,alpha=clamp((u-0.3)/0.4))
        if u>0.95:
            ex=clamp((t-3.2)/0.6)
            dot(g,xB,RED,pulse=(t*1.4)%1,r=17)
            if ex>0: label(g,(xB[0]+60,xB[1]+10),'Tào Báo mở cổng',RED,34,alpha=ex)
    return im

# ---------- lớp phụ: phụ đề, thẻ, số, mốc năm
def wrap(txt,f,maxw,g):
    words=txt.split();lines=[];cur=''
    for w_ in words:
        tr=(cur+' '+w_).strip()
        if g.textlength(tr,font=f)<=maxw: cur=tr
        else: lines.append(cur);cur=w_
    lines.append(cur);return lines
def sub_layer(txt):
    im=Image.new('RGBA',(W,H),(0,0,0,0));g=ImageDraw.Draw(im);f=font(46,False)
    lines=wrap(txt,f,1560,g);lh=62;h=lh*len(lines)+30;y0=H-70-h
    g.rounded_rectangle((W/2-820,y0,W/2+820,y0+h),22,fill=(8,5,3,150))
    for i,l in enumerate(lines):
        w=g.textlength(l,font=f);x=W/2-w/2;y=y0+15+i*lh
        g.text((x+2,y+3),l,font=f,fill=(0,0,0,255));g.text((x,y),l,font=f,fill=(250,244,228,255))
    return im
def card_layer(name,role,col):
    im=Image.new('RGBA',(640,150),(0,0,0,0));g=ImageDraw.Draw(im)
    g.rounded_rectangle((0,0,640,150),16,fill=(16,10,6,225),outline=col+(255,),width=3)
    g.rectangle((0,0,16,150),fill=col+(255,))
    g.text((40,20),name,font=font(50),fill=(250,240,215,255))
    g.text((40,88),role,font=font(30,False),fill=(215,200,170,255))
    return im
def num_layer(big,small):
    im=Image.new('RGBA',(W,H),(0,0,0,0));g=ImageDraw.Draw(im);f=font(150);fs=font(44,False)
    w=g.textlength(big,font=f);x=W/2-w/2;y=250
    g.text((x+5,y+7),big,font=f,fill=(0,0,0,230));g.text((x,y),big,font=f,fill=(246,206,102,255))
    w2=g.textlength(small,font=fs);g.text((W/2-w2/2+2,y+190),small,font=fs,fill=(0,0,0,230));g.text((W/2-w2/2,y+188),small,font=fs,fill=(250,244,228,255))
    return im
def year_layer(yr,prog):
    im=Image.new('RGBA',(520,150),(0,0,0,0));g=ImageDraw.Draw(im)
    g.rounded_rectangle((0,0,520,150),16,fill=(16,10,6,205))
    g.text((26,10),f'{yr}',font=font(64),fill=(246,206,102,255));g.text((190,34),'sau Công nguyên',font=font(30,False),fill=(230,220,195,255))
    g.line((26,112,494,112),fill=(120,100,70,255),width=4)
    for i,y_ in enumerate(range(192,199)):
        x=26+i*(468/6);g.ellipse((x-5,107,x+5,117),fill=(160,135,90,255));g.text((x-18,120),str(y_)[-2:],font=font(18,False),fill=(190,175,145,255)) if False else None
    x=26+(yr-192+prog)*(468/6);g.ellipse((x-10,102,x+10,122),fill=(246,206,102,255))
    return im
SUBS={n:sub_layer(texts[n]) for n in texts}
def comp(base,layer,pos=(0,0),a=1.0):
    if a<=0: return base
    L=layer if a>=1 else Image.merge('RGBA',(*layer.split()[:3],layer.split()[3].point(lambda v:int(v*a))))
    base.paste(L,pos,L);return base
# --- lịch
MAPS=[(129,129,1),(132,132,2)]   # (câu đầu, câu cuối, giai đoạn)
mapspan={}
for a,b,ph in MAPS: mapspan[ph]=(T[a],T[b]+D[b])
CARDS=[ # (câu, tên, vai trò, màu, trễ)
 (130,'Tào Báo','tướng cũ của Đào Khiêm, giữ Hạ Bì',(176,60,50),0.8),
 (135,'Hứa Đam','một tướng của Lưu Bị',(60,100,170),0.8),
 (131,'Trương Phi','giữ Hạ Bì khi Lưu Bị đi xa',(60,100,170),0.5)]
CARDL={c[0]:card_layer(c[1],c[2],c[3]) for c in CARDS}
NUMS=[(141,'MỘT ĐÊM','Hạ Bì rơi vào tay Lữ Bố',0.6)]
NUML={n:num_layer(b,s) for n,b,s,_ in NUMS}
YEARL=[year_layer(196,p/10) for p in range(11)]
def beat_of(t):
    for n in range(FIRST,LAST+1):
        if T[n]<=t<T[n]+D[n]: return n
    return FIRST if t<T[FIRST] else LAST
def frame(t):
    n=beat_of(t);lt=t-T[n];u=lt/D[n]
    in_map=None
    for ph,(a,b) in mapspan.items():
        if a<=t<b: in_map=(ph,a)
    if in_map:
        ph,a_=in_map
        fr=map_frame(t-a_,ph)
        k=min(clamp((t-a_)/0.8),clamp((mapspan[ph][1]-t)/0.8))
        out=Image.blend(img_frame(n,u),fr,ease(k))
    else:
        out=img_frame(n,u)
    # chuyển cảnh mờ giữa các câu
    X=0.5
    if lt<X and n>FIRST and not in_map:
        out=Image.blend(img_frame(n-1,1.0),out,ease(lt/X))
    if t<0.5: out=Image.blend(Image.new('RGB',(W,H),(8,5,3)),out,ease(t/0.5))
    if t>TOTAL-1.0: out=Image.blend(out,Image.new('RGB',(W,H),(8,5,3)),ease((t-(TOTAL-1.0))/1.0))
    rgba=out.convert('RGBA')
    # mốc năm
    comp(rgba,YEARL[min(10,int(10*(t-T[FIRST])/(TOTAL-T[FIRST])))],(50,40),clamp((t-0.6)/0.6)*clamp((TOTAL-1.2-t)/0.5))
    # thẻ nhân vật
    for (cn,_,_,_,dl) in CARDS:
        if beat_of(t)==cn:
            s=T[cn]+dl;e=T[cn]+D[cn]-0.3;
            if s<=t<=e:
                k=min(clamp((t-s)/0.5),clamp((e-t)/0.4));x=50-int((1-ease(k))*160)
                comp(rgba,CARDL[cn],(x,215),ease(k))
    # chữ nhấn
    for (cn,_,_,dl) in NUMS:
        if n==cn:
            s=T[cn]+dl;e=s+2.6
            if s<=t<=e:
                k=min(clamp((t-s)/0.25),clamp((e-t)/0.4));sc=1+0.15*(1-ease(clamp((t-s)/0.25)))
                L=NUML[cn]
                if sc!=1: 
                    L2=L.resize((int(W*sc),int(H*sc)),Image.BICUBIC);rgba=comp(rgba,L2,(int((W-W*sc)/2),int((H-H*sc)/2)-(0)),ease(k))
                else: comp(rgba,L,(0,0),ease(k))
    # phụ đề
    if True:
        k=min(clamp(lt/0.35),clamp((D[n]-lt)/0.3))
        comp(rgba,SUBS[n],(0,0),ease(k) if lt>0.05 else 0)
    return rgba.convert('RGB')
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='still':
        for ts in sys.argv[2:]:
            frame(float(ts)).save(f'/tmp/proto/still_{ts}.jpg',quality=90)
        sys.exit()
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','/tmp/proto/v.mp4'],stdin=subprocess.PIPE)
    N=int(TOTAL*FPS)
    for i in range(N):
        p.stdin.write(frame(i/FPS).tobytes())
        if i%150==0: print(i,N,flush=True)
    p.stdin.close();p.wait()
    json.dump({'T':T,'D':D,'TOTAL':TOTAL},open('/tmp/proto/timeline.json','w'))
