import json,wave,subprocess,numpy as np
c=json.load(open('/home/claude/fact-video/trader9x/vang55_cau.json'))
V='/home/claude/fact-video/assets/trader9x/VANG55/Iapetus/'
sr=44100;t=0.35;parts=[];times=[];prev=None
for s in c['doan']:
    f=V+s['id']+'.wav'
    if s['id']=='d3':
        subprocess.run(['ffmpeg','-y','-v','error','-i',f,'-af','atempo=0.9','-ar','44100','-ac','1','d3.wav'],check=True);f='d3.wav'
    w=wave.open(f);a=np.frombuffer(w.readframes(w.getnframes()),np.int16)
    if prev and prev[0]!=s['id'][0]: t+=0.45
    times.append({'id':s['id'],'start':round(t+0.08,3),'dur':round(len(a)/sr,3)})
    parts.append((int((t+0.08)*sr),a)); t+=len(a)/sr+0.22; prev=s['id']
N=int((t+1.6)*sr);out=np.zeros(N,np.int32)
for p,a in parts: out[p:p+len(a)]+=a
wave_out=wave.open('voice.wav','wb');wave_out.setnchannels(1);wave_out.setsampwidth(2);wave_out.setframerate(sr)
wave_out.writeframes(np.clip(out,-32768,32767).astype('<i2').tobytes())
json.dump(times,open('times.json','w'),indent=0)
print('tổng',t+1.6)
