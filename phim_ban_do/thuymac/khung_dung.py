# Phần chung của mã dựng tm5–tm10: thời gian theo giọng gốc, ghép cảnh, logo, phụ đề, chạy soi/render
import sys,os,subprocess,json,math
from dai import cam,cpath,to8,PAP,W,H,XM,NM
from canh import *
GD=os.environ.get('GIONG','/tmp/pc/assets/thu_giong_hai/charon')
class V: pass
import re as _re,difflib as _dl
def _nm(w): return _re.sub(r'[^\w]','',w.lower())
def align_pause(texts,f):
    """chưa có nhận dạng: chọn khoảng lặng gần vị trí ước theo số chữ nhất làm ranh giới đoạn"""
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout
    x=np.frombuffer(raw,np.float32);hop=160;fr=x[:len(x)//hop*hop].reshape(-1,hop);e=np.sqrt((fr**2).mean(1))
    thr=max(e.max()*.03,np.percentile(e,20)*1.5);sil=e<thr
    runs=[];i=0;n=len(sil)
    while i<n:
        if sil[i]:
            j=i
            while j<n and sil[j]: j+=1
            if (j-i)*hop/16000>=.25: runs.append((i*hop/16000,j*hop/16000))
            i=j
        else: i+=1
    fd=len(x)/16000;w=[len(t.split()) for t in texts];tot=sum(w);N=len(texts)
    sp_start=runs[0][1] if runs and runs[0][0]<.05 else 0;sp_end=runs[-1][0] if runs and runs[-1][1]>fd-.05 else fd
    C=[r for r in runs if r[0]>sp_start+.5 and r[1]<sp_end-.5]
    if len(C)<N-1:
        acc=np.cumsum([0]+w)/tot;b=[sp_start+(sp_end-sp_start)*a for a in acc];return list(zip(b[:-1],b[1:]))
    rate=(sp_end-sp_start-sum(r[1]-r[0] for r in C)*.4)/tot
    pts=[(sp_start,sp_start)]+C+[(sp_end,sp_end)];M=len(pts)
    INF=1e18;dp=[[INF]*M for _ in range(N+1)];bk=[[-1]*M for _ in range(N+1)];dp[0][0]=0
    for k in range(1,N+1):
        for j in range(1,M):
            if k==N and j!=M-1: continue
            if k<N and j==M-1: continue
            bonus=-.8*min(1.0,pts[j][1]-pts[j][0]) if k<N else 0
            for i2 in range(j):
                if dp[k-1][i2]>=INF: continue
                d=pts[j][0]-pts[i2][1];e=(d-w[k-1]*rate)/max(1.0,w[k-1]*rate)
                c=dp[k-1][i2]+e*e*10+bonus
                if c<dp[k][j]: dp[k][j]=c;bk[k][j]=i2
    idx=[M-1];k=N
    while k>0: idx.append(bk[k][idx[-1]]);k-=1
    idx=idx[::-1];return [(pts[idx[k]][1],pts[idx[k+1]][0]) for k in range(N)]
_AU={}
def cut_point(f,e_prev,s_next):
    """điểm cắt giữa hai đoạn: giữa khoảng lặng dài nhất trong vùng [hết đoạn trước − 0,8 ; đầu đoạn sau + 0,3]"""
    if f not in _AU:
        raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout
        x=np.frombuffer(raw,np.float32);fr=x[:len(x)//320*320].reshape(-1,320);_AU[f]=np.sqrt((fr**2).mean(1))
    e=_AU[f];thr=max(e.max()*.02,np.percentile(e,15)*1.3)
    i0=max(0,int((min(e_prev,s_next)-.8)*50));i1=min(len(e),int((max(e_prev,s_next)+.3)*50))
    best=None;i=i0
    while i<i1:
        if e[i]<thr:
            j=i
            while j<i1 and e[j]<thr: j+=1
            if best is None or j-i>best[1]-best[0]: best=(i,j)
            i=j
        else: i+=1
    if best is None: return (e_prev+s_next)/2
    return (best[0]+best[1])/2/50
def align(texts,words,fd,f=None):
    """mốc (bắt đầu, kết thúc) của từng đoạn trong file chương: khớp chữ kịch bản với chữ nhận dạng"""
    if not words and f: return align_pause(texts,f)
    sw=[];lab=[]
    for i,tx in enumerate(texts):
        for w in tx.split(): sw.append(_nm(w));lab.append(i)
    aw=[_nm(w[0]) for w in words]
    st=[None]*len(texts);en=[None]*len(texts)
    for blk in _dl.SequenceMatcher(None,sw,aw,autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            i=lab[blk.a+k];w=words[blk.b+k]
            if st[i] is None: st[i]=w[1]
            en[i]=w[2]
    n=len(texts);tot=sum(len(t.split()) for t in texts);acc=0
    for i in range(n):   # đoạn không khớp được thì nội suy theo số chữ
        if st[i] is None: st[i]=fd*acc/tot
        acc+=len(texts[i].split())
        if en[i] is None: en[i]=fd*acc/tot
    for i in range(1,n): st[i]=max(st[i],en[i-1]-.05)
    return list(zip(st,en))
def setup(ma,gaps,tail=4.5):
    J=json.load(open(f'/tmp/pc/ke-hoach/thu-giong-hai/{ma}_full.json'))
    v=V();v.TX={i+1:d['text'] for i,d in enumerate(J)};v.NN={i+1:d['n'] for i,d in enumerate(J)}
    def dur(i):
        f=f'{GD}/{v.NN[i]}.mp3'
        if os.path.exists(f):
            return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
        return len(v.TX[i].split())/3.1+.2
    v.T={};v.E={};t=.5;v.CH=None
    gm=f'{GD}/chuong_{ma}_full.json';asr=f'/tmp/pc/phim_ban_do/asr_{ma}ca.json'
    cf=f'/tmp/pc/ke-hoach/thu-giong-hai/{ma}chen_full.json'
    if os.path.exists(gm) and os.path.exists(cf) and os.path.exists(f'{GD}/chuong_{ma}chen_full.json'):
        # có đoạn chèn bối cảnh (và đoạn thay): ghép theo thứ tự khóa; đoạn chèn có khóa lẻ (4.1, 4.2…), đoạn thay giữ khóa cũ
        C=json.load(open(cf));A_={}
        for nm_ in (asr,f'/tmp/pc/phim_ban_do/asr_{ma}chenca.json'):
            if os.path.exists(nm_) and not os.environ.get('KHOP_LANG'): A_.update(json.load(open(nm_)))
        inv={n:i for i,n in v.NN.items()};thay={c['thay']:c for c in C if c.get('thay')}
        k0=C[0]['sau_doan'];key={};txt={}
        for j,c in enumerate([c for c in C if not c.get('thay')]): key[c['n']]=round(k0+.1*(j+1),2);txt[c['n']]=c['text']
        for c in C:
            if c.get('thay'): key[c['n']]=inv[c['thay']];txt[c['n']]=c['text']
        for n,i in inv.items():
            if n not in thay: key[n]=i;txt[n]=v.TX[i]
        v.TX={key[n]:txt[n] for n in key};v.NN={key[n]:n for n in key}
        G={**json.load(open(gm)),**json.load(open(f'{GD}/chuong_{ma}chen_full.json'))}
        seg={}
        for stem,ns in G.items():
            f=f'{GD}/{stem}.mp3';fd=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
            tx=[txt.get(n) or json.load(open(f'/tmp/pc/ke-hoach/thu-giong-hai/{ma}_full.json'))[inv[n]-1]['text'] for n in ns]
            sp=align(tx,A_.get(stem,[]),fd,f)
            for j,n in enumerate(ns): seg[n]=(f,j,sp,fd,ns)
        order=sorted(key,key=lambda n:key[n]);v.CH=[];runs=[]
        gaps=dict(gaps);k1=round(k0+.1,2);gaps[k1]=gaps.pop(k0+1,1.0);v.TTL_KEY=k1   # thẻ tên trận đứng trước phần bối cảnh
        for n in order:
            f,j,sp,fd,ns=seg[n];g=gaps.get(key[n],0)
            if runs and runs[-1]['f']==f and runs[-1]['j'][-1]==j-1 and g==0: runs[-1]['j'].append(j);runs[-1]['n'].append(n)
            else: runs.append({'f':f,'j':[j],'n':[n],'g':g,'sp':sp,'fd':fd})
        for r in runs:
            f,sp,fd,J0,J1=r['f'],r['sp'],r['fd'],r['j'][0],r['j'][-1]
            a0=0 if J0==0 else max(sp[J0-1][1]+.02,sp[J0][0]-.18)
            b0=fd if J1==len(sp)-1 else min(sp[J1][1]+.3,sp[J1+1][0]-.02)
            ca=0 if J0==0 else cut_point(f,sp[J0-1][1],sp[J0][0]);cb=fd if J1==len(sp)-1 else cut_point(f,sp[J1][1],sp[J1+1][0])
            t+=r['g'];off=t-a0
            for j,n in zip(r['j'],r['n']): v.T[key[n]]=off+sp[j][0];v.E[key[n]]=off+sp[j][1]
            v.CH.append((t-(a0-ca),f,ca,cb));t+=b0-a0+.5
    elif os.path.exists(gm):   # giọng đọc theo chương / cả video: mốc đoạn lấy từ nhận dạng, chia đoạn âm ở ranh giới chương
        G=json.load(open(gm));A_=json.load(open(asr)) if os.path.exists(asr) and not os.environ.get('KHOP_LANG') else {};v.CH=[];inv={n:i for i,n in v.NN.items()}
        for stem,ns in sorted(G.items(),key=lambda kv:kv[1][0]):
            f=f'{GD}/{stem}.mp3';fd=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
            sp=align([v.TX[inv[n]] for n in ns],A_.get(stem,[]),fd,f)
            runs=[[0]]
            for j in range(1,len(ns)):
                if gaps.get(inv[ns[j]],0)>0: runs.append([j])
                else: runs[-1].append(j)
            cuts=[cut_point(f,sp[run[0]-1][1],sp[run[0]][0]) for run in runs[1:]]   # cắt ở giữa khoảng lặng thật, không theo mốc chữ (mốc chữ hay trễ, làm mất tiếng đầu câu)
            for r,run in enumerate(runs):
                a0=0 if r==0 else max(sp[run[0]-1][1]+.02,sp[run[0]][0]-.18)
                b0=fd if r==len(runs)-1 else min(sp[run[-1]][1]+.3,sp[run[-1]+1][0]-.02)
                t+=gaps.get(inv[ns[run[0]]],0);off=t-a0
                for j in run: v.T[inv[ns[j]]]=off+sp[j][0];v.E[inv[ns[j]]]=off+sp[j][1]
                ca=0 if r==0 else cuts[r-1];cb=fd if r==len(runs)-1 else cuts[r]
                v.CH.append((t-(a0-ca),f,ca,cb));t+=b0-a0+.5
    else:
        for n in v.TX:
            t+=gaps.get(n,0);v.T[n]=t;d=dur(n);v.E[n]=t+d;t+=d+.45
    v.TOTAL=t+tail;v.N=len(v.TX)
    v.TTL=v.T[v.TTL_KEY] if getattr(v,'TTL_KEY',None) else None
    v.mid=lambda n,f:v.T[n]+(v.E[n]-v.T[n])*f
    return v
_LOGO=[None]
def compose(v,SH,t,overlay=None,cards={}):
    act=[s for s in SH if s[0]-.35<=t<s[1]+.35]
    def one(fn):
        cv=PAP.copy();fn(cv,t);return cv
    if len(act)==1: cv=one(act[0][2])
    else:
        a,b=act[0],act[1];u=cl((t-(b[0]-.35))/.7)
        m=np.clip((u*1.7-.35-XM*.35-NM*.35)/.3,0,1)[...,None];cv=one(a[2])*(1-m)+one(b[2])*m
    if overlay: overlay(cv,t)
    for n,s in cards.items(): card(cv,t,v.T[n]-2.2,s,PAP)
    for n,lst in getattr(v,'NHAN',{}).items():   # nhãn giới thiệu nhân vật, địa danh (người chưa biết sử vẫn hiểu)
        if n in v.T and v.T[n]-.2<t<v.E[n]+.6:
            o=inn(t,v.T[n]-.2,.4)*(1-inn(t,v.E[n]+.2,.4))
            for k,lab in enumerate(lst if isinstance(lst,list) else [lst]):
                im=text(lab,30,INK,600,glow=4);put_screen(cv,im,60+im.shape[1]/2,64+k*46,o)
    for n in v.TX:
        if v.T[n]-.25<t<v.E[n]+.35: caption(cv,v.TX[n],inn(t,v.T[n]-.25,.25)*(1-inn(t,v.E[n]+.1,.25)),False)
    if _LOGO[0] is None:
        lg=np.asarray(Image.open(D+'nguoi-gac-su.png').convert('RGBA').resize((130,130),Image.LANCZOS),np.float32)/255;lg[...,:3]*=lg[...,3:4];_LOGO[0]=lg
    blend(cv,_LOGO[0],W-44-130,34,.8)
    return cv
def main(v,frame):
    mode=sys.argv[1]
    if mode=='soi':
        out=[]
        for x in sys.argv[2:]:
            if x[0]=='t': tt=float(x[1:])
            elif '+' in x: tt=v.T[int(x.split('+')[0])]+float(x.split('+')[1])
            elif '@' in x: tt=v.mid(int(x.split('@')[0]),float(x.split('@')[1]))
            else: tt=v.mid(int(x),.6)
            out.append((x,to8(frame(tt))))
        cols=3;h,w=H//3,W//3;rows=(len(out)+cols-1)//cols
        sh=Image.new('RGB',(w*cols,(h+30)*rows),(255,255,255));dr=ImageDraw.Draw(sh)
        for i,(x,im) in enumerate(out):
            sh.paste(Image.fromarray(im).resize((w,h)),((i%cols)*w,(i//cols)*(h+30)+30));dr.text(((i%cols)*w+8,(i//cols)*(h+30)+6),x,fill=(0,0,0))
        sh.save(os.environ.get('SOI','/tmp/gen/soi.jpg'),quality=82);print('TOTAL',round(v.TOTAL,1))
    else:
        out,i0,i1,fps=sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
        ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        for i in range(i0,i1): ff.stdin.write(to8(frame(i/fps)).tobytes())
        ff.stdin.close();ff.wait()
def title(cv,t,t0,name,sealname,ss=.75):
    u=inn(t,t0-.3,.8);put_screen(cv,A('blot'),W/2,H/2,u*.97*(1-inn(t,t0+3.2,.6)),s=1.5+.1*(t-t0),r=4*(t-t0))
    tt=text(name,96,PAPER,700);put_screen(cv,wipe(tt,inn(t,t0+.2,.8),0,.3,seed=3),W/2,H/2-30,1-inn(t,t0+3.2,.5))
    seal(cv,sealname,W/2+460,H/2+110,t0+1.1,t,s=ss,o=1-inn(t,t0+3.2,.5),r=4)
def rain(cv,t,o=.5,n=140,seed=3):
    if o<=0: return
    rg=np.random.default_rng(seed);xs=rg.random(n)*2200-100;ys=rg.random(n);sp=.8+rg.random(n)*.6
    c=cam(960,540,1.0)
    for x,y,s in zip(xs,ys,sp):
        yy=((y+t*s)%1.2)*1200-100;stroke(cv,c,[(x,yy),(x-18,yy+70)],1,wid=2,head=False,o=.35*o)
