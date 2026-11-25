# Bản dọc tm27 (1080×1920, khoảng 76 giây): cắt từ bản dài, không đọc giọng mới.
# Đoạn 1–4 (hook lời dọa của Ô Mã Nhi), 33–38 (thủy triều rút, thuyền mắc cọc, quân Đại Việt đổ ra), rồi màn mời xem bản đầy đủ.
# Hình lấy từ dai_tm27.frame (tắt phụ đề, nhãn ngang), cắt dải 608 px.
import sys,math,subprocess,numpy as np,cv2
import dai_tm27 as D
from engine import text,band,put_screen,caption,blend,inn
from canh import RED,INK,PAPER
D.NOCAP=True;D.V2.NHAN={}
_nolb=lambda *a,**k:None
D.lb=_nolb;D.big=_nolb;D.nhan=_nolb
T,E,sb=D.T,D.E,D.sb
SEG=[(T[1]-.3,E[4]+.5),(T[33]-.3,E[38]+.4)]
END=3.8
VT=[];acc=0
for a,b in SEG: VT.append((acc,a,b));acc+=b-a
TOTAL=acc+END
def src(tv):
    for v0,a,b in VT:
        if tv<v0+(b-a): return a+(tv-v0)
    return SEG[-1][1]-.05
# tâm cắt theo thời gian nguồn (x trên khung 1920)
CX=[(0,1080),(T[2],1080),(T[2]+.5,760),(T[3],960),(T[4],960),(T[33],1000),(T[34],900),(T[35],1000),(T[36],1000),(T[37],1050),(T[38],1000),(999,1000)]
def cx_of(t):
    for (a,x0),(b,x1) in zip(CX,CX[1:]):
        if t<=b: u=min(1,max(0,(t-a)/max(b-a,1e-6)));u=u*u*(3-2*u);return x0+(x1-x0)*u
    return 960
HEAD=[(T[1]-.3,T[3],'DỌA ĐUỔI VUA LÊN TRỜI'),(T[3],E[4]+.4,'RỒI BỊ GIẢI TỚI TRƯỚC LĂNG?'),(T[33]-.3,E[38]+.4,'BÃI CỌC SÔNG BẠCH ĐẰNG')]
NAME={2:('Ô Mã Nhi','tướng thủy quân nhà Nguyên')}
def cap_at(t):
    for n,hs in D.SENT.items():
        for k,h in enumerate(hs):
            a=sb(n,k) if len(hs)>1 else T[n];b=sb(n,k+1) if len(hs)>1 else E[n]
            if a<t<b: return h,inn(t,a,.12)*(1-inn(t,b-.12,.12))
    return None,0
WV,HV=1080,1920;CW=int(1080*1080/1920)
def vframe(tv):
    if tv>=acc:
        t=SEG[-1][1]-.05;base=vframe_src(t,tv)
        u=inn(tv,acc,.8);base[:]=base*(1-.8*u)+np.array(PAPER,np.float32)*.8*u
        put_screen(base,text('Xem bản đầy đủ',72,RED,700,glow=6),WV/2,1150,u)
        put_screen(base,text('trên kênh Người Gác Sử',56,INK,700),WV/2,1250,u)
        put_screen(base,text('Bạch Đằng 1288',40,INK,600),WV/2,1340,inn(tv,acc+.5,.8))
        return base
    return vframe_src(src(tv),tv)
def vframe_src(t,tv):
    fr=D.frame(t);fr=fr.astype(np.float32)/255 if fr.dtype==np.uint8 else fr.astype(np.float32)
    x0=int(round(cx_of(t)-CW/2));x0=max(0,min(1920-CW,x0))
    cv=np.ascontiguousarray(cv2.resize(fr[:,x0:x0+CW],(WV,HV),interpolation=cv2.INTER_CUBIC))
    for a,b,h in HEAD:
        if a<t<b:
            o=inn(t,a+.1,.4)*(1-inn(t,b-.4,.4));tx=text(h,64,RED,700,maxw=980,glow=6)
            put_screen(cv,band(tx.shape[1]-20,tx.shape[0]-10,PAPER,.85,30),WV/2,300,o);put_screen(cv,tx,WV/2,300,o)
    for n,(nm,ph) in NAME.items():
        if T[n]<t<E[n]:
            o=inn(t,T[n]+.2,.4)*(1-inn(t,E[n]-.4,.4))
            put_screen(cv,band(620,110,PAPER,.85,20),WV/2,470,o)
            put_screen(cv,text(nm,46,RED,700),WV/2,450,o);put_screen(cv,text(ph,30,INK,600),WV/2,500,o)
    h,o=cap_at(t)
    if h: caption(cv,h,o,True)
    return cv
if __name__=='__main__':
    out,f0,f1=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{WV}x{HV}','-r','24','-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    for i in range(f0,f1):
        cv=vframe(i/24);p.stdin.write((np.clip(cv,0,1)*255+.5).astype(np.uint8).tobytes())
    p.stdin.close();p.wait()
