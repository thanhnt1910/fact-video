# Clip dọc 80 giây Đinh Bộ Lĩnh từ video đầy đủ. Dùng: python assets/bia/DBL1/tao_tiktok.py <dbl1_video.mp4> <ra.mp4>
import sys,os,json,subprocess,textwrap
from PIL import Image,ImageDraw,ImageFont
V,OUT=sys.argv[1],sys.argv[2]; W='/tmp/dbl1_tt'; os.makedirs(W,exist_ok=True)
F='assets/fonts/';BLK=F+'BeVietnamPro-BlackItalic.ttf';EXB=F+'BeVietnamPro-ExtraBoldItalic.ttf';LORA=F+'Lora-Variable.ttf'
WHITE=(255,250,235);YEL=(255,205,60);RED=(200,30,30)
fo=lambda p,s:ImageFont.truetype(p,s)
PH=json.load(open('phim_ban_do/phude_dbl1.json'))
T={10001:0.5,10002:9.83,10005:24.92}
import importlib;os.environ.setdefault('SCRIPT','ke-hoach/thu-giong-hai/dbl1_full.json');os.environ.setdefault('VOICE_DIR','assets/thu_giong_hai/dbl1_chuan');os.environ.setdefault('WORLD','phim_ban_do/world7.jpg');os.environ['PHUDE']='phim_ban_do/phude_dbl1.json';os.environ['CONTENT']='dbl1_content'
sys.path.insert(0,'phim_ban_do');import build2 as b
SEG=[(0.4,b.T[10002]+b.D[10002],[10001,10002]),(b.T[10005],b.T[10005]+b.D[10005],[10005]),(b.T[10038],b.T[10043]+b.D[10043],[10038,10039,10040,10041,10042,10043])]
OUTRO=6.0;off=0;subs=[];segs=[]
for k,(s,e,ps) in enumerate(SEG):
    segs.append((s,e-s,off))
    for n in ps:
        for r in b.PH.get(str(n),[]):
            a=off+b.T[n]+r[1]-s; z=off+b.T[n]+r[2]-s+0.05
            subs.append((a,z,r[0]))
    off+=e-s
body=off;total=body+OUTRO
print('thân',round(body,1),'tổng',round(total,1),'cụm phụ đề',len(subs))
# 1) từng đoạn dọc
for k,(s,d,o) in enumerate(segs):
    fc=("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.3[bg];"
        "[b]crop=1440:900:0:0,scale=1080:675[fg];[bg][fg]overlay=0:640,fps=24[v];"
        f"[0:a]afade=t=in:d=0.12,afade=t=out:st={d-0.15:.2f}:d=0.15,aresample=44100[a]")
    ex=[]
    if k==0:   # 3,8 giây đầu của video là thẻ tiêu đề: thay bằng khung bản đồ sạch (giọng đọc vẫn chạy)
        subprocess.run(['ffmpeg','-y','-v','error','-ss','4.3','-i',V,'-frames:v','1','-vf','crop=1440:900:0:0,scale=1080:675',f'{W}/fg0.png'],check=True)
        ex=['-i',f'{W}/fg0.png'];fc=fc.replace('[bg][fg]overlay=0:640,fps=24[v]',"[bg][fg]overlay=0:640[t];[t][1:v]overlay=0:640:enable='between(t,0,3.8)',fps=24[v]")
    subprocess.run(['ffmpeg','-y','-v','error','-ss',f'{s:.3f}','-t',f'{d:.3f}','-i',V]+ex+['-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',f'{W}/s{k}.mp4'],check=True)
# 2) đoạn kết: khung cuối mờ + thẻ
last=subprocess.run(['ffmpeg','-y','-v','error','-ss','4','-i',V,'-frames:v','1',f'{W}/bg.jpg'],check=True)
bg=Image.open(f'{W}/bg.jpg').convert('RGB').resize((3413,1920)).crop((1000,0,2080,1920)).filter(__import__('PIL.ImageFilter',fromlist=['x']).GaussianBlur(30))
bg=Image.blend(bg,Image.new('RGB',bg.size,(15,10,5)),0.55);bg.save(f'{W}/outro.jpg')
subprocess.run(['ffmpeg','-y','-v','error','-loop','1','-t',str(OUTRO),'-i',f'{W}/outro.jpg','-f','lavfi','-t',str(OUTRO),'-i','anullsrc=r=44100:cl=mono','-vf','fps=24','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-shortest',f'{W}/s3.mp4'],check=True)
open(f'{W}/l.txt','w').write(''.join(f"file '{W}/s{i}.mp4'\n" for i in range(4)))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',f'{W}/l.txt','-c','copy',f'{W}/base.mp4'],check=True)
# 3) lớp chữ
logo=Image.open('assets/logo/nguoi-gac-su.png').convert('RGBA')
def add_logo(im):
    l=logo.resize((130,130),Image.LANCZOS);l.putalpha(l.split()[3].point(lambda v:int(v*0.8)));im.alpha_composite(l,(1080-44-130,34))
def sh(d,xy,t,f,fill,off=6): d.text((xy[0]+off,xy[1]+off),t,font=f,fill=(40,15,0));d.text(xy,t,font=f,fill=fill)
def fit(t,p,maxw,s):
    while fo(p,s).getlength(t)>maxw:s-=2
    return fo(p,s)
H=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(H)
d.polygon([(70,150),(520,142),(512,214),(62,220)],fill=RED);d.text((92,158),'ĐINH BỘ LĨNH',font=fo(EXB,46),fill=WHITE)
sh(d,(70,250),'CON BỊ TREO',fit('CON BỊ TREO',BLK,940,150),WHITE,7);sh(d,(70,420),'TRÊN SÀO',fit('TRÊN SÀO',BLK,940,170),YEL,7)
d.text((75,1815),'Người Gác Sử',font=fo(LORA,44),fill=YEL);add_logo(H);H.save(f'{W}/head.png')
O=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(O);add_logo(O)
t1='Xem đủ câu chuyện';t2='trong video 11 phút'
d.text((540-fo(LORA,64).getlength(t1)/2,720),t1,font=fo(LORA,64),fill=WHITE);d.text((540-fo(LORA,64).getlength(t2)/2,810),t2,font=fo(LORA,64),fill=YEL)
d.polygon([(190,950),(890,942),(884,1030),(184,1038)],fill=RED)
t3='YouTube · Facebook · Người Gác Sử';d.text((540-fit(t3,EXB,680,44).getlength(t3)/2,967),t3,font=fit(t3,EXB,680,44),fill=WHITE)
t4='Link ở bio';d.text((540-fo(LORA,52).getlength(t4)/2,1090),t4,font=fo(LORA,52),fill=YEL)
O.save(f'{W}/outro.png')
ins=['-i',f'{W}/base.mp4','-i',f'{W}/head.png','-i',f'{W}/outro.png'];fc='[0:v][1:v]overlay=0:0:enable=\'between(t,0,%.2f)\'[v0];[v0][2:v]overlay=0:0:enable=\'between(t,%.2f,%.2f)\'[v1]'%(body,body,total);last='v1'
for i,(a,z,t) in enumerate(subs):
    lines=textwrap.wrap(t,26) or [t];f=fo(LORA,66);h=len(lines)*92+40
    im=Image.new('RGBA',(1080,1920),(0,0,0,0));dd=ImageDraw.Draw(im);y0=1480
    w=max(f.getlength(l) for l in lines)+80;dd.rounded_rectangle([540-w/2,y0-10,540+w/2,y0+h-10],24,fill=(18,14,10,205))
    for j,l in enumerate(lines):dd.text((540-f.getlength(l)/2,y0+10+j*92),l,font=f,fill=WHITE)
    p=f'{W}/sub{i}.png';im.save(p);ins+=['-i',p]
    fc+=f";[{last}][{3+i}:v]overlay=0:0:enable='between(t,{a:.2f},{z:.2f})'[w{i}]";last=f'w{i}'
subprocess.run(['ffmpeg','-y','-v','error']+ins+['-filter_complex',fc,'-map',f'[{last}]','-map','0:a','-c:v','libx264','-crf','21','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',OUT],check=True)
print('xong',OUT)
