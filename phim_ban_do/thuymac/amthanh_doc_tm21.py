# Âm thanh bản dọc tm21: cắt đúng các đoạn hình của doc_tm21 từ bản trộn âm của bản dài (giữ nguyên giọng, không xử lý giọng),
# mỗi chỗ nối có lớp mờ 80 ms; màn kết lấy tiếng cồng kết của bản dài.
import numpy as np,sys
from scipy.io import wavfile
import doc_tm21 as Dv
sr,x=wavfile.read(sys.argv[1] if len(sys.argv)>1 else '/tmp/gen/bd/out/am_tm21.wav');dt=x.dtype;x=x.astype(np.float32)
f=int(.08*sr);parts=[]
def cut(a,b):
    y=x[int(a*sr):int(b*sr)].copy();r=np.linspace(0,1,f)[:,None] if y.ndim>1 else np.linspace(0,1,f)
    y[:f]*=r;y[-f:]*=r[::-1];return y
for a,b in Dv.SEG: parts.append(cut(a,b))
e=Dv.E[29]+.1;parts.append(cut(e,e+Dv.END))
y=np.concatenate(parts);wavfile.write('/tmp/gen/bd/out/am_doc_tm21.wav',sr,y.astype(dt) if dt!=np.float32 else y);print(len(y)/sr,Dv.TOTAL)
