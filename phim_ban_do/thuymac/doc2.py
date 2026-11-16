# Bản dọc v2 (kịch bản bd2d, giọng Charon)
import sys,os,subprocess,json
import doc
from doc import *
GD='/tmp/pc/assets/thu_giong_hai/charon'
J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/bd2d_full.json'))
doc.TX.clear();doc.TX.update({i+1:d['text'] for i,d in enumerate(J)})
def dur(n):
    f=f"{GD}/{J[n-1]['n']}.mp3"
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout) if os.path.exists(f) else len(J[n-1]['text'].split())/3.1
t=0.3
for n in range(1,10):
    doc.T[n]=t;d=dur(n);doc.E[n]=t+d;t+=d+.4
doc.TOTAL=t+3.5;T,E=doc.T,doc.E
doc.SHOTS[:]=[(0,T[4]-.3,doc.S_river),(T[4]-.3,T[5]+3.2,doc.S_cross),(T[5]+3.2,T[8]-.3,doc.S_river),(T[8]-.3,T[9]-.3,doc.S_end8),(T[9]-.3,doc.TOTAL+1,doc.S_end9)]
TOTAL=doc.TOTAL;doc.HOOK_V='Vì sao bên yếu hơn lại thắng?';doc.END_V='Vì sao phải ra tay trước?'
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='soi':
        for x in sys.argv[2:]:
            tt=float(x[1:]) if x[0]=='t' else T[int(x.split('+')[0])]+float(x.split('+')[1]) if '+' in x else T[int(x)]+1.5
            Image.fromarray(to8(doc.frame(tt))).save(f'/tmp/gen/bd/out/s_{x}.jpg',quality=85)
        print('TOTAL',round(TOTAL,1),{k:round(v,1) for k,v in T.items()})
    else:
        out,i0,i1,fps=sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
        ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        for i in range(i0,i1): ff.stdin.write(to8(doc.frame(i/fps)).tobytes())
        ff.stdin.close();ff.wait()
