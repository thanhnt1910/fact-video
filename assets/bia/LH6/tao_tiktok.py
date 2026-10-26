# Clip dọc ~66 giây Lê Hoàn bốn lần đánh lừa nhà Tống, dựng từ các đoạn bản đồ đã kết xuất riêng.
# Dùng: python assets/bia/LH6/tao_tiktok.py <thư mục chứa seg0..seg4.mp4/.wav và segs.txt> <ra.mp4>
import sys,os,json,subprocess,textwrap
from PIL import Image,ImageDraw,ImageFont
SD,OUT=sys.argv[1],sys.argv[2]; W='/tmp/lh6_tt'; os.makedirs(W,exist_ok=True)
F='assets/fonts/';BLK=F+'BeVietnamPro-BlackItalic.ttf';EXB=F+'BeVietnamPro-ExtraBoldItalic.ttf';LORA=F+'Lora-Variable.ttf'
WHITE=(255,250,235);YEL=(255,205,60);RED=(200,30,30)
fo=lambda p,s:ImageFont.truetype(p,s)
sys.path.insert(0,'phim_ban_do');import build2 as b
SEGROWS=[l.split() for l in open(SD+'/segs.txt') if l.strip() and l.split()[0].isdigit()]
BEATS=[(1,2),(46,47),(55,56),(79,79),(88,89)]
OUTRO=5.4;off=0;subs=[];segs=[]
for k,(r,(a_,b_)) in enumerate(zip(SEGROWS,BEATS)):
    s=float(r[1]);e=float(r[2]);segs.append((k,e-s,off))
    for n in range(17000+a_,17000+b_+1):
        for rr in b.PH.get(str(n),[]):
            subs.append((off+b.T[n]+rr[1]-s,off+b.T[n]+rr[2]-s+0.05,rr[0]))
    off+=e-s
body=off;total=body+OUTRO
print('thân',round(body,1),'tổng',round(total,1),'cụm phụ đề',len(subs))
NS=len(segs)
# 1) từng đoạn dọc: nền mờ + khung bản đồ 1080x675 ở giữa
for k,d,o in segs:
    V=f'{SD}/seg{k}.mp4';A=f'{SD}/seg{k}.wav'
    fc=("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.3[bg];"
        "[b]crop=1700:956:0:0,scale=1080:608[fg];[bg][fg]overlay=0:640,fps=24[v];"
        f"[1:a]afade=t=in:d=0.12,afade=t=out:st={d-0.15:.2f}:d=0.15,aresample=44100[a]")
    ex=[]
    if k==0:   # 4,2 giây đầu của video là thẻ tiêu đề ngang: thay bằng khung bản đồ sạch (giọng đọc vẫn chạy)
        subprocess.run(['ffmpeg','-y','-v','error','-i',SD+'/clean.jpg','-vf','crop=1700:956:0:0,scale=1080:608',f'{W}/fg0.png'],check=True)
        ex=['-i',f'{W}/fg0.png'];fc=fc.replace('[bg][fg]overlay=0:640,fps=24[v]',"[bg][fg]overlay=0:640[t];[t][2:v]overlay=0:640:enable='between(t,0,3.9)',fps=24[v]")
    subprocess.run(['ffmpeg','-y','-v','error','-i',V,'-i',A]+ex+['-filter_complex',fc,'-map','[v]','-map','[a]','-t',f'{d:.3f}','-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',f'{W}/s{k}.mp4'],check=True)
# 2) đoạn kết: khung bản đồ mờ + thẻ
bg=Image.open(SD+'/clean.jpg').convert('RGB').resize((3413,1920)).crop((1000,0,2080,1920)).filter(__import__('PIL.ImageFilter',fromlist=['x']).GaussianBlur(30))
bg=Image.blend(bg,Image.new('RGB',bg.size,(15,10,5)),0.55);bg.save(f'{W}/outro.jpg')
subprocess.run(['ffmpeg','-y','-v','error','-loop','1','-t',str(OUTRO),'-i',f'{W}/outro.jpg','-f','lavfi','-t',str(OUTRO),'-i','anullsrc=r=44100:cl=mono','-vf','fps=24','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-shortest',f'{W}/s{NS}.mp4'],check=True)
open(f'{W}/l.txt','w').write(''.join(f"file '{W}/s{i}.mp4'\n" for i in range(NS+1)))
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
d.polygon([(70,150),(520,142),(512,214),(62,220)],fill=RED);d.text((92,158),'LÊ HOÀN · 980–990',font=fo(EXB,46),fill=WHITE)
sh(d,(70,235),'BỐN LẦN',fit('BỐN LẦN',BLK,940,150),WHITE,7);sh(d,(70,385),'ĐÁNH LỪA',fit('ĐÁNH LỪA',BLK,940,150),YEL,7);sh(d,(70,525),'NHÀ TỐNG',fit('NHÀ TỐNG',BLK,940,100),WHITE,7)
d.text((75,1815),'Người Gác Sử',font=fo(LORA,44),fill=YEL);add_logo(H);H.save(f'{W}/head.png')
O=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(O);add_logo(O)
t1='Xem đủ câu chuyện';t2='trong video 14 phút'
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
