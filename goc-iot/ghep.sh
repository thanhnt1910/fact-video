#!/bin/bash
# dùng: ghep.sh N  (dựng video có tiếng)
N=$1
S=/tmp/claude-0/-home-claude/632dedbd-7f81-5ca7-9478-f00ed7d0f34f/scratchpad/video1
G=/home/claude/fact-video/goc-iot/giong
cd $S; mkdir -p aud final
python3 - $N <<'PY'
import json,subprocess,sys,statistics
n=sys.argv[1]
G='/home/claude/fact-video/goc-iot/giong'
d=json.load(open(G+'/thoi-luong.json'))
allw=[v['tu_moi_giay'] for v in d.values()]
target=statistics.median(allw)
tl={}
for k,v in d.items():
    if not k.startswith(f'v{n}_'): continue
    r=max(0.92,min(1.08,target/v['tu_moi_giay']))
    out=f'aud/{k}.wav'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{G}/{k}.wav','-af',f'atempo={r:.4f},loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100','-ac','1',out],check=True)
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out]))
    tl[k]=dict(v,giay=round(dur,3))
json.dump(tl,open(f'aud/tl{n}.json','w'),ensure_ascii=False)
print('target wps',target)
PY
TLFILE=$S/aud/tl$N.json node render4.cjs $N ff$N full > ff$N.log 2>&1 || exit 1
python3 - $N <<'PY'
import json,subprocess,sys
n=sys.argv[1]
tl=json.load(open(f'aud/tl{n}.json'))
files=[]
for k in sorted(tl, key=lambda x:int(x.split('_s')[1])):
    dur=tl[k]['giay']+0.7
    o=f'aud/p_{k}.wav'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'aud/{k}.wav','-af',f'adelay=250,apad=whole_dur={dur:.3f}','-t',f'{dur:.3f}','-ar','44100','-ac','1',o],check=True)
    files.append(o)
open(f'aud/list{n}.txt','w').write(''.join(f"file '{f.split('/')[-1]}'\n" for f in files))
PY
(cd aud && ffmpeg -y -loglevel error -f concat -safe 0 -i list$N.txt -c copy full$N.wav)
ffmpeg -y -loglevel error -framerate 24 -i ff$N/f%05d.png -i aud/full$N.wav -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -b:a 128k -shortest final/video-$N.mp4 && rm -rf ff$N && echo ok $N >> final/done.txt
