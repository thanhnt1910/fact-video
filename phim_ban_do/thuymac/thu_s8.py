"""Thử nâng cấp trên cảnh vây thành (đoạn 8) của tm11m: bản cũ và bản mới."""
import sys,math
import dai_tm11m as DM
from dai_tm11m import *
import dai_tm11m as DM
import hieu_ung as HU
def S_8n(cv,t):
    a,b=T[8],E[8];tc=sb(8,2)
    sh=fio(t,tc,tc+3.2)
    c=cam(*cpath(t,[(a-.3,(960,560,1.0)),(sb(8,1),(960,560,1.03)),(tc+3.0,(960,570,1.12))]),sx=4*math.sin(t*23)*sh,sy=3*math.sin(t*19)*sh)
    put(cv,c,HU.mucloang('t11_thanh',t,seed=3),960,470,s=.68)
    HU.suong(cv,c,t,700,.14)
    for i in range(9):   # quân vây ngoài tường: đi tới rồi đâm giáo
        for xx,fc in ((150+i*70,1),(1300+i*70+ (i%2)*12,-1)):
            ux=inn(t,a+.1+i*.07,.4)*(1-inn(t,tc+1.5,.8)*.8)
            mode='thrust' if t>sb(8,1) else 'march'
            xoff=(1-inn(t,a+.1+i*.07,1.6))*fc*-120 if mode=='march' else 0
            HU.linh(cv,c,xx+xoff,665+(i%3)*12,t,s=.42,ph=i*.9,face=fc,mode=mode,o=ux)
    lb(cv,c,'Trần Bảo vây chặt Đại La',960,170,t,a+.2,sb(8,1)-.1,col=RED,sz=42)
    big(cv,'NGƯỜI VÂY THÀNH, THÀNH NGƯỜI BỊ VÂY',t,sb(8,1)+.1,tc-.3,INK,150,58,seed=8)
    if t>tc-.2:
        for i in range(12):
            st=tc+i*.12;u=inn(t,st,1.5);fc=-1 if i%2 else 1
            xs=960+fc*lerp(0,150+i*45,u)
            HU.linh(cv,c,xs,655+(i%3)*10,t,s=.42,ph=i*.7,face=fc,mode='run' if u<.95 else 'thrust',o=inn(t,st,.2))
        sparks(cv,c,t,[(700,610),(820,620),(1100,610),(1220,620)],tc+.4,E[8],seed=8)
        HU.tro(cv,c,t,tc+.2,E[8],[(700,610),(820,620),(1100,610),(1220,620)],n=18)
        tagfall(cv,c,1180,330,'Trần Bảo',t,tc+.2,fall=E[8]-.9,sz=44,col=RED)
        lb(cv,c,'đánh ra từ trong thành',960,170,t,tc+.3,E[8]+.3,col=INK,sz=40)
    for x,rd in ((330,False),(2470,True)):
        fx,fy=tp(x,330,960,470,.68,2800,700);flag(cv,c,fx,fy-150,t,s=.8,red=rd,ph=x,pole=150)
def mk(fn):
    SH2=[(x,y,fn if f is DM.S_8 else f) for x,y,f in DM.SH]
    return lambda t: K.compose(DM.V2,SH2,t,DM.ov,DM.CARDS)
if __name__=='__main__':
    mode=sys.argv[1]
    fr=DM.frame if mode=='cu' else mk(S_8n)
    if sys.argv[2]=='soi':
        import os
        out=[]
        for x in sys.argv[3:]:
            tt=DM.V.mid(8,float(x));out.append((x,K.to8(fr(tt))))
        from PIL import Image
        w,h=640,360;sh_=Image.new('RGB',(w*3,h*((len(out)+2)//3)))
        for i,(x,im) in enumerate(out): sh_.paste(Image.fromarray(im).resize((w,h)),((i%3)*w,(i//3)*h))
        sh_.save('/tmp/gen/thu_soi.jpg')
    else:
        i0,i1=int((DM.T[8]-.3)*24),int((DM.E[8]+.5)*24);import subprocess
        ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',sys.argv[2]],stdin=subprocess.PIPE)
        for i in range(i0,i1): ff.stdin.write(K.to8(fr(i/24)).tobytes())
        ff.stdin.close();ff.wait()
