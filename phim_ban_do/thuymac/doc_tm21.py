# Bản dọc tm21 (1080×1920, khoảng 64 giây): cắt từ bản dài, không đọc giọng mới.
# Đoạn 1–2 (lá cờ xin từ phương xa, ba câu hỏi), 10 (tiết việt là gì), 22–24 (xin tiết nhà Lương, Nam Hán nổi giận, bị bắt), 26 (về đúng Quảng Châu),
# rồi màn mời xem bản đầy đủ. Cảnh bản đồ (đoạn 22) không cắt dải mà thu nhỏ nguyên khung, để Hoàng Sa và thẻ Trường Sa vẫn nằm trong hình.
import sys,math,subprocess,numpy as np,cv2,os
os.environ.setdefault('NANG','1')
import dai_tm21 as D
from engine import text,band,put_screen,caption,blend,inn
from canh import RED,INK,PAPER
D.NOCAP=True;D.DOC=True;D.V2.NHAN={}
_no=lambda *a,**k:None
D.big=_no;D.panel=_no
_lb=D.lb
D.lb=_no   # nhãn ngang của bản dài bị cắt khi lấy dải dọc: bản dọc dùng chữ lớn riêng (cảnh bản đồ vẫn giữ nhãn Hoàng Sa, Trường Sa vẽ bằng hs())
T,E,sb=D.T,D.E,D.sb
SEG=[(T[1]-.3,E[2]+.4),(T[10]-.3,E[10]+.3),(T[22]-.3,E[24]+.4),(T[26]-.3,E[26]+.15)]
MAP=(T[22]-.3,T[23]-.3)
END=3.8
VT=[];acc=0
for a,b in SEG: VT.append((acc,a,b));acc+=b-a
TOTAL=acc+END
def src(tv):
    for v0,a,b in VT:
        if tv<v0+(b-a): return a+(tv-v0)
    return SEG[-1][1]-.05
CX=[(0,560),(sb(1,1)-.4,560),(sb(1,1)+.6,1050),(T[2]-.3,1250),(T[10]-.3,900),(T[23]-.3,460),(sb(23,2),460),(sb(23,2)+1.2,1420),(T[24]-.3,960),(sb(24,1)+.3,900),(E[24]+.4,1500),(T[26]-.3,300),(E[26]+.15,1350),(999,960)]
def cx_of(t):
    for (a,x0),(b,x1) in zip(CX,CX[1:]):
        if t<=b: u=min(1,max(0,(t-a)/max(b-a,1e-6)));u=u*u*(3-2*u);return x0+(x1-x0)*u
    return 960
HEAD=[(T[1]-.3,T[2]-.2,'BA ĐỜI, KHÔNG MỘT TRẬN LỚN'),(T[2]-.2,T[2]+(E[2]-T[2])*.3,'LÁ CỜ ẤY LÀ GÌ?'),(T[2]+(E[2]-T[2])*.3,T[2]+(E[2]-T[2])*.55,'VÌ SAO PHẢI XIN?'),(T[2]+(E[2]-T[2])*.55,E[2]+.4,'XIN ĐƯỢC RỒI, VÌ SAO MẤT ĐẤT?'),(T[10]-.3,E[10]+.3,'TIẾT VIỆT: DẤU HIỆU CAI QUẢN'),
      (T[22]-.3,T[23]-.3,'XIN LÁ CỜ CỦA NƠI XA'),(T[23]-.3,T[24]-.3,'CHUỐC GIẬN NGƯỜI Ở GẦN'),(T[24]-.3,E[24]+.4,'NAM HÁN ĐEM QUÂN SANG'),(T[26]-.3,E[26]+.15,'NGƯỜI SỨ THÀNH NGƯỜI BỊ BẮT')]
NAME={22:('Khúc Thừa Mỹ','đời thứ ba họ Khúc'),23:('Lưu Nham','vua Nam Hán')}
def cap_at(t):
    for n,hs in D.SENT.items():
        for k,h in enumerate(hs):
            a=sb(n,k) if len(hs)>1 else T[n];b=sb(n,k+1) if len(hs)>1 else E[n]
            if a<t<b: return h,inn(t,a,.12)*(1-inn(t,b-.12,.12))
    return None,0
WV,HV=1080,1920;CW=int(1080*1080/1920)
PAPV=None
def vframe(tv):
    if tv>=acc:
        t=SEG[-1][1]-.05;base=vframe_src(t,tv)
        u=inn(tv,acc,.8);base[:]=base*(1-.8*u)+np.array(PAPER,np.float32)*.8*u
        put_screen(base,text('Xem bản đầy đủ',72,RED,700,glow=6),WV/2,1150,u)
        put_screen(base,text('trên kênh Người Gác Sử',56,INK,700),WV/2,1250,u)
        put_screen(base,text('Ba đời họ Khúc, năm 905–930',44,INK,600),WV/2,1340,inn(tv,acc+.5,.8))
        return base
    return vframe_src(src(tv),tv)
def vframe_src(t,tv):
    fr=D.frame(t);fr=fr.astype(np.float32)/255 if fr.dtype==np.uint8 else fr.astype(np.float32)
    if MAP[0]<t<MAP[1]:
        global PAPV
        if PAPV is None: PAPV=np.ascontiguousarray(cv2.resize(D.PAP,(WV,HV)))
        cv=PAPV.copy();sm=cv2.resize(fr,(WV,int(WV*1080/1920)),interpolation=cv2.INTER_AREA);y0=(HV-sm.shape[0])//2
        cv[y0:y0+sm.shape[0]]=sm
    else:
        cx=cx_of(t)
        if t>T[26]-.3:   # bám theo xe tù (dai_tm21.S_26)
            a=T[26]-.3;b=E[26]+.3;c=D.kc(t,[(a,(800,560,1.04)),(b,(1150,560,1.0))]);cx=c.p(-200+1440*inn(t,a+.2,b-a-.4)+100,890)[0]
        x0=int(round(cx-CW/2));x0=max(0,min(1920-CW,x0))
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
FPS=30
if __name__=='__main__':
    out,f0,f1=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
    if out=='soi':
        from PIL import Image
        ims=[Image.fromarray((np.clip(vframe(float(x)),0,1)*255).astype(np.uint8)).resize((360,640)) for x in sys.argv[4:]]
        sh=Image.new('RGB',(360*len(ims),640));[sh.paste(im,(i*360,0)) for i,im in enumerate(ims)];sh.save('/tmp/gen/doc21.jpg');print(TOTAL);sys.exit()
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{WV}x{HV}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    for i in range(f0,f1):
        cv=vframe(i/FPS);p.stdin.write((np.clip(cv,0,1)*255+.5).astype(np.uint8).tobytes())
    p.stdin.close();p.wait()
