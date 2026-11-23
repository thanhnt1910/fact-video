# Bản dọc tm22 (1080×1920, khoảng 66 giây): cắt từ bản dài, không đọc giọng mới.
# Đoạn 1–2 (thung lũng hai vua không hạ nổi, hai câu hỏi), 11–14 (đánh hơn một tháng, ngọn sào, tay nỏ, hai vua rút quân),
# 34 (thung lũng thành kinh đô), rồi màn mời xem bản đầy đủ. Không có cảnh bản đồ nên không cần thẻ Hoàng Sa, Trường Sa.
import sys,math,subprocess,numpy as np,cv2,os
import dai_tm22 as D
from engine import text,band,put_screen,caption,blend,inn
from canh import RED,INK,PAPER
D.NOCAP=True;D.DOC=True;D.V2.NHAN={}
_no=lambda *a,**k:None
D.big=_no;D.panel=_no;D.lb=_no;D.o_dem=_no
T,E,sb=D.T,D.E,D.sb
SEG=[(T[1]-.3,E[2]+.4),(T[11]-.3,E[14]+.4),(T[34]-.3,E[34]+.15)]
END=3.8
VT=[];acc=0
for a,b in SEG: VT.append((acc,a,b));acc+=b-a
TOTAL=acc+END
def src(tv):
    for v0,a,b in VT:
        if tv<v0+(b-a): return a+(tv-v0)
    return SEG[-1][1]-.05
CX=[(0,1100),(sb(1,1),1250),(sb(1,2),1150),(T[2]-.3,1500),(T[11]-.3,1150),(T[12]-.3,960),(sb(12,1),1000),(T[13]-.3,620),(sb(13,2),760),(T[14]-.3,960),(sb(14,2),800),(T[34]-.3,1150),(E[34]+.15,1250),(999,1200)]
def cx_of(t):
    for (a,x0),(b,x1) in zip(CX,CX[1:]):
        if t<=b: u=min(1,max(0,(t-a)/max(b-a,1e-6)));u=u*u*(3-2*u);return x0+(x1-x0)*u
    return 960
L2=E[2]-T[2]
HEAD=[(T[1]-.3,sb(1,1),'BỐN BỀ LÀ NÚI ĐÁ'),(sb(1,1),sb(1,2),'HAI VUA KHÔNG HẠ NỔI'),(sb(1,2),T[2]-.2,'RỒI THÀNH KINH ĐÔ'),
      (T[2]-.2,sb(2,1),'NGƯỜI GIỮ LÀ AI?'),(sb(2,1),E[2]+.4,'VÌ SAO THÀNH KINH ĐÔ?'),
      (T[11]-.3,T[12]-.3,'HƠN MỘT THÁNG KHÔNG HẠ ĐƯỢC'),(T[12]-.3,T[13]-.3,'NGỌN SÀO TRƯỚC TRẠI'),(T[13]-.3,T[14]-.3,'NGƯỜI CHA KHÔNG HÀNG'),(T[14]-.3,E[14]+.4,'HAI VUA RÚT QUÂN'),
      (T[34]-.3,E[34]+.15,'THUNG LŨNG THÀNH KINH ĐÔ')]
NAME={12:('Đinh Liễn','con trai Đinh Bộ Lĩnh'),13:('Đinh Bộ Lĩnh','người giữ Hoa Lư')}
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
        put_screen(base,text('Đinh Bộ Lĩnh và Hoa Lư, năm 944–968',42,INK,600),WV/2,1340,inn(tv,acc+.5,.8))
        logo(base)
        return base
    return vframe_src(src(tv),tv)
def vframe_src(t,tv):
    fr=D.frame(t);fr=fr.astype(np.float32)/255 if fr.dtype==np.uint8 else fr.astype(np.float32)
    cx=cx_of(t);x0=int(round(cx-CW/2));x0=max(0,min(1740-CW,x0))   # không lấy vùng logo của bản dài (x 1746–1876); logo bản dọc đặt riêng
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
    logo(cv)
    return cv
_LG=[None]
def logo(cv):
    if _LG[0] is None:
        from PIL import Image
        from canh import D as _D
        lg=np.asarray(Image.open(_D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4];_LG[0]=lg
    blend(cv,_LG[0],WV-44-130,34,.8)
FPS=30
if __name__=='__main__':
    out,f0,f1=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
    if out=='soi':
        from PIL import Image
        ims=[Image.fromarray((np.clip(vframe(float(x)),0,1)*255).astype(np.uint8)).resize((360,640)) for x in sys.argv[4:]]
        sh=Image.new('RGB',(360*len(ims),640));[sh.paste(im,(i*360,0)) for i,im in enumerate(ims)];sh.save('/tmp/claude-0/s/doc22.jpg');print(TOTAL);sys.exit()
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{WV}x{HV}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    for i in range(f0,f1):
        cv=vframe(i/FPS);p.stdin.write((np.clip(cv,0,1)*255+.5).astype(np.uint8).tobytes())
    p.stdin.close();p.wait()
