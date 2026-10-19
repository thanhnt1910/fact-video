import json,math,os
from PIL import Image,ImageDraw,ImageFont
W,H,FPS=1920,1080,24
FONT=os.environ.get('FONT','/tmp/wt/assets/fonts/Lora-Variable.ttf')
def font(sz,bold=True):
    f=ImageFont.truetype(FONT,int(sz))
    try: f.set_variation_by_name('Bold' if bold else 'Regular')
    except Exception: pass
    return f
ease=lambda x:0.5-0.5*math.cos(math.pi*min(1,max(0,x)))
clamp=lambda x:min(1,max(0,x))
SCRIPT=os.environ.get('SCRIPT','/home/claude/fact-video/ke-hoach/thu-giong-hai/tq45_hai.json')
HAI=json.load(open(SCRIPT))
texts={b['n']:b['text'] for b in HAI}
chap={b['n']:b['chuong'] for b in HAI}
FIRST,LAST=min(texts),max(texts)
def dur(t): return max(3.2,len(t.split())/3.4+0.5)
D={n:dur(t) for n,t in texts.items()}
VDIR=os.environ.get('VOICE_DIR','')
if VDIR and os.path.exists(VDIR+'/thoi_luong.json'):
    _d=json.load(open(VDIR+'/thoi_luong.json'));D={n:(_d[str(n)]+0.45 if str(n) in _d else D[n]) for n in texts}
T={};t=0.5
for n in range(FIRST,LAST+1): T[n]=t;t+=D[n]
TOTAL=t+1.5
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
def chip_layer(chapter,year):
    _g=ImageDraw.Draw(Image.new('RGBA',(10,10)));wd=int(max(420,_g.textlength(chapter,font=font(40 if not year else 26))+70))
    im=Image.new('RGBA',(wd,120),(0,0,0,0));g=ImageDraw.Draw(im)
    g.rounded_rectangle((0,0,wd,120),16,fill=(16,10,6,205))
    if year:
        g.text((26,12),str(year),font=font(60),fill=(246,206,102,255));g.text((190,34),'sau Công nguyên',font=font(28,False),fill=(230,220,195,255))
        g.text((26,80),chapter,font=font(26,False),fill=(215,200,170,255))
    else:
        g.text((26,34),chapter,font=font(40),fill=(246,206,102,255))
    return im
def comp(base,layer,pos=(0,0),a=1.0):
    if a<=0: return base
    L=layer if a>=1 else Image.merge('RGBA',(*layer.split()[:3],layer.split()[3].point(lambda v:int(v*a))))
    base.paste(L,pos,L);return base
def beat_of(t):
    for n in range(FIRST,LAST+1):
        if T[n]<=t<T[n]+D[n]: return n
    return FIRST if t<T[FIRST] else LAST
if __name__=='__main__': print('tổng',round(TOTAL,1),'s',round(TOTAL/60,1),'phút')
