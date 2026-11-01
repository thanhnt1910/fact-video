import numpy as np, math, subprocess, os
from PIL import Image, ImageDraw, ImageFont
R='/home/claude/fact-video/'
W,H=1920,1080
F=lambda s: ImageFont.truetype(R+'assets/fonts/Lora-Variable.ttf',s)
logo=Image.open(R+'assets/logo/nguoi-gac-su.png').convert('RGBA').resize((130,130))
a=logo.split()[3].point(lambda v:int(v*.8)); logo.putalpha(a)
SEG=[('A','19047','Ung Châu, đầu năm 1076','Cận cảnh · minh họa','Quân Đại Việt chồng bao đất thành bậc thang, trèo lên mặt thành',(0.5,0.55)),
     ('B','19060','Sông Như Nguyệt, đầu năm 1077','Cận cảnh · minh họa','Hàng rào tre dọc bờ nam, cọc cắm dưới lòng sông',(0.5,0.6)),
     ('C','19077','Vùng Quảng Nguyên, năm 1078','Cận cảnh · minh họa','Sứ đoàn dắt voi sang biếu nhà Tống, xin lại đất',(0.45,0.6))]
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); D=np.sqrt((xx-960)**2+(yy-432)**2)
ease=lambda u:u*u*(3-2*u)
def chip(im,txt,sub=None,y=900):
    d=ImageDraw.Draw(im,'RGBA'); f=F(54); w=int(d.textlength(txt,font=f))+70
    d.rounded_rectangle((46,y,46+w,y+(150 if sub else 100)),14,fill=(36,26,14,225))
    d.rectangle((46,y,54,y+(150 if sub else 100)),fill=(201,116,42,255))
    d.text((80,y+16),txt,font=f,fill=(241,231,203,255))
    if sub: d.text((80,y+86),sub,font=F(34),fill=(214,170,110,255))
n=0; os.makedirs('out',exist_ok=True)
for s,(m,ill,mapcap,tag,cap,fx) in enumerate(SEG):
    I=Image.open(R+f'assets/anh_phang/lt1/{ill}.jpg').convert('RGB')
    for i in range(209):
        mf=Image.open(f'{m}/{min(i,119):04d}.jpg').convert('RGB')
        if i<113:
            u=ease(min(1,max(0,(i-84)/29)))
            fr=mf.copy()
            if u>0:
                r=u*1250; sc=1.0
                big=I.copy()
                mask=(D<r).astype(np.float32)
                arr=np.asarray(fr,np.float32); b=np.asarray(big,np.float32)
                arr=arr*(1-mask[...,None])+b*mask[...,None]
                fr=Image.fromarray(arr.astype(np.uint8))
                ring=((D>r-5)&(D<r+5)&(D>0)).astype(np.float32)[...,None]*0.9
                arr=np.asarray(fr,np.float32); arr=arr*(1-ring)+np.array([110,70,30],np.float32)*ring
                fr=Image.fromarray(arr.astype(np.uint8))
            if i<100: chip(fr,mapcap)
        else:
            k=(i-113)/96; z=1.0+0.16*ease(k)
            cw,ch=W/z,H/z; cx=fx[0]*W; cy=fx[1]*H
            x0=min(max(cx-cw/2,0),W-cw); y0=min(max(cy-ch/2,0),H-ch)
            fr=I.resize((W,H),Image.LANCZOS,box=(x0,y0,x0+cw,y0+ch))
            if k>0.08: chip(fr,cap,tag)
        fr=fr.convert('RGBA'); fr.alpha_composite(logo,(W-44-130,34)); fr=fr.convert('RGB')
        fade=min(1,i/8) if s==0 else min(1,i/8)
        if i>=200: fade=(208-i)/8
        if fade<1: fr=Image.eval(fr,lambda v:int(v*max(0,fade)))
        fr.save(f'out/{n:05d}.jpg',quality=92); n+=1
print(n)
