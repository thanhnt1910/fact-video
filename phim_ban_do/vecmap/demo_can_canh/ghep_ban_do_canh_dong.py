import numpy as np, os
from PIL import Image, ImageDraw, ImageFont
W,H=1920,1080
F=lambda s: ImageFont.truetype('/home/claude/fact-video/assets/fonts/Lora-Variable.ttf',s)
logo=Image.open('/home/claude/fact-video/assets/logo/nguoi-gac-su.png').convert('RGBA').resize((130,130)); logo.putalpha(logo.split()[3].point(lambda v:int(v*.8)))
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); D=np.sqrt((xx-960)**2+(yy-432)**2)
ease=lambda u:u*u*(3-2*u)
SEG=[('A','/tmp/uc/f','Ung Châu, đầu năm 1076'),('B','/tmp/nn/f','Sông Như Nguyệt, đầu năm 1077')]
def chip(im,txt):
    d=ImageDraw.Draw(im,'RGBA'); f=F(54); w=int(d.textlength(txt,font=f))+70
    d.rounded_rectangle((46,900,46+w,1000),14,fill=(36,26,14,225)); d.rectangle((46,900,54,1000),fill=(201,116,42,255)); d.text((80,916),txt,font=f,fill=(241,231,203,255))
os.makedirs('out2',exist_ok=True); n=0
for si,(m,sd,cap) in enumerate(SEG):
    tot=113+235
    for i in range(tot):
        mf=Image.open(f'{m}/{min(i,119):04d}.jpg').convert('RGB')
        if i<84: fr=mf.copy(); chip(fr,cap)
        elif i<113:
            u=ease((i-84)/29); r=u*1300
            sc=Image.open(f'{sd}/{i-84:04d}.png').convert('RGB')
            mk=(D<r).astype(np.float32)[...,None]
            a=np.asarray(mf,np.float32)*(1-mk)+np.asarray(sc,np.float32)*mk
            ring=((D>r-5)&(D<r+5)&(D>0)).astype(np.float32)[...,None]*.9
            a=a*(1-ring)+np.array([110,70,30],np.float32)*ring
            fr=Image.fromarray(a.astype(np.uint8))
            if i<100: chip(fr,cap)
        else:
            fr=Image.open(f'{sd}/{i-84:04d}.png').convert('RGB')
        if i<113 and i<84:
            fr=fr.convert('RGBA'); fr.alpha_composite(logo,(W-174,34)); fr=fr.convert('RGB')
        k=1.0
        if i<8: k=i/8
        if i>=tot-8: k=(tot-1-i)/8
        if k<1: fr=Image.eval(fr,lambda v:int(v*max(0,k)))
        fr.save(f'out2/{n:05d}.jpg',quality=92); n+=1
print(n)
