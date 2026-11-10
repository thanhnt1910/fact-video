import json,subprocess,re,sys
S=sys.argv[1]
d=json.load(open('src/kinhdo/leda_dur.json'))
f=0;starts=[]
for x in d:
    starts.append(f/30);f+=round(max(x+.5,2.4)*30)
total=(f+round(3.5*30))/30
ins=[];fl=[]
n=len(d)
for i in range(n):
    p='../demo/kinhdo/leda/%02d.wav'%(i+1)
    r=subprocess.run(['ffmpeg','-nostats','-i',p,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
    I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',r)[-1])
    ins+=['-i',p]
    ms=int((starts[i]+.15)*1000)
    fl.append('[%d:a]volume=%.2fdB,adelay=%d|%d[a%d]'%(i+1,-16-I,ms,ms,i))
ins=['-i','out/kinhdo_silent.mp4']+ins+['-i',S+'/sfxk.wav']
fl.append('[%d:a]volume=0.5[sx]'%(n+1))
fl.append(''.join('[a%d]'%i for i in range(n))+'[sx]amix=inputs=%d:normalize=0:dropout_transition=0,alimiter=limit=0.9:level=disabled[m]'%(n+1))
cmd=['ffmpeg','-y']+ins+['-filter_complex',';'.join(fl),'-map','0:v','-map','[m]','-c:v','copy','-c:a','aac','-b:a','192k','-t','%.2f'%total,'out/kinhdo_vi_leda.mp4']
json.dump({'starts':starts,'total':total},open(S+'/starts_kd.json','w'))
subprocess.run(cmd,check=True,capture_output=True)
print(total)
