import sys,textwrap,subprocess,json
from sfx import *
which=sys.argv[1]
def voice_mix(M,T,files,duck=.55):
    v=np.zeros(M.N,np.float32)
    for t0,f in zip(T,files):
        raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
        a=np.frombuffer(raw,np.float32);i=int(t0*SR);j=min(M.N,i+len(a));v[i:j]+=a[:j-i]
    env_=np.convolve(np.abs(v),np.ones(4000)/4000,'same');d=1-duck*np.clip(env_*12,0,1)
    return v,d.astype(np.float32)
def write_mix(M,v,d,path):
    L,R=M.L*d,M.R*d
    f=int(.6*SR)
    for x in (L,R): x[:f]*=np.linspace(0,1,f);x[-f:]*=np.linspace(1,0,f)
    L=lp(L,11000);R=lp(R,11000)
    st=np.stack([L,R],1);q=np.percentile(np.abs(st),99.7);st=st/max(q,1e-6)*.32   # hiệu ứng nhỏ hơn giọng
    vv=v/max(np.max(np.abs(v)),1e-6)*.8
    out=np.clip(st+vv[:,None],-1,1);out=np.tanh(out*1.1)/np.tanh(1.1)*.95
    import wave
    with wave.open(path,'wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes())
if which=='dai':
    import dai2,dai as V
    src=open('/tmp/gen/bd/amthanh.py').read()
    a=src.index("if which=='dai':")+len("if which=='dai':\n");b=src.index("    write(M,'/tmp/gen/bd/out/am_dai.wav',V.TOTAL)")
    blk=textwrap.dedent(src[a:b]).replace("import dai as V;T,E=V.T,V.E;M=Mix(V.TOTAL)","T,E=V.T,V.E;M=Mix(V.TOTAL)")
    blk=blk.replace("music(M,a,b,md,v)","music(M,min(a,V.TOTAL-2),min(b,V.TOTAL-1),md,v) if a<V.TOTAL-3 else None")
    g={'V':V,'np':np,'math':math};exec("from sfx import *\n"+blk,g);M=g['M'];T2=dai2.T2;E2=dai2.E2
    for n in dai2.CARDS2: whoosh(M,T2[n]-2.6,1.0,.4);gong(M,T2[n]-2.1,.45);brush(M,T2[n]-2.2,.7,.35)
    brush(M,.3,.8,.3);brush(M,dai2.mid(1,.58),.8,.3)
    from sfx import wind as _w
    n_=int((dai2.E2[12]-dai2.T2[12])*SR);M.add(hp(lp(M.nz(n_),6000),1200)*fadeio(n_,.8,.8)*.6,dai2.T2[12]+.8,.5)
    gong(M,T2[11]+.2,.3)
    kw=dai2.mid(44,.25)
    for i in range(3): stamp(M,kw+i*(E2[44]-kw)/3.2,.55)
    stamp(M,T2[40]+.3,.6);brush(M,T2[40]+1.0,1.2,.3)
    ns=sorted(dai2.TX2);files=[f"{dai2.GD}/{dai2.NN[n]}.mp3" for n in ns]
    v,d=voice_mix(M,[T2[n] for n in ns],files)
    write_mix(M,v,d,'/tmp/gen/bd/out/am_dai2.wav')
else:
    import doc2,doc as V
    src=open('/tmp/gen/bd/amthanh.py').read()
    a=src.index("    import doc as V;");b=src.index("    write(M,'/tmp/gen/bd/out/am_doc.wav',V.TOTAL)")
    blk=textwrap.dedent(src[a:b]).replace("import doc as V;T,E=V.T,V.E;M=Mix(V.TOTAL,9)","T,E=V.T,V.E;M=Mix(V.TOTAL,9)")
    g={'V':V,'np':np,'math':math};exec("from sfx import *\n"+blk,g);M=g['M']
    files=[f"{doc2.GD}/{d['n']}.mp3" for d in doc2.J]
    v,d=voice_mix(M,[V.T[n] for n in range(1,10)],files)
    write_mix(M,v,d,'/tmp/gen/bd/out/am_doc2.wav')
print('ok')
