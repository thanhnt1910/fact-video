import subprocess,numpy as np,sys
def load(p):
    a=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
    return np.frombuffer(a,np.int16).astype(np.float32)/32768
def f0(x,sr=16000):
    fs=[];n=640
    for i in range(0,len(x)-n,n):
        s=x[i:i+n]
        if np.sqrt((s**2).mean())<.03: continue
        s=s-s.mean();c=np.correlate(s,s,'full')[n-1:];lo,hi=sr//300,sr//60;k=lo+np.argmax(c[lo:hi])
        if c[k]>.4*c[0]: fs.append(sr/k)
    return np.array(fs)
for p in sys.argv[1:]:
    x=load(p);F=f0(x);fr=np.sqrt(np.convolve(x**2,np.ones(1600)/1600,'valid')[::400])
    print(p.split('/')[-1],f'{len(x)/16000:.1f}s',f'cao độ {np.median(F):.0f} Hz, dao động {np.percentile(F,90)-np.percentile(F,10):.0f}',f'lặng {(fr<.01).mean()*100:.0f}%')
