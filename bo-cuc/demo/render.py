import sys,subprocess,os,numpy as np,wave
from playwright.sync_api import sync_playwright
FPS=24;DUR=16.0
def music(path):
    sr=44100;n=int(sr*DUR);t=np.arange(n)/sr;y=np.zeros(n)
    sw=np.clip(t/8,0,1)**1.5
    y+=0.25*np.sin(2*np.pi*55*t)*sw+0.15*np.sin(2*np.pi*82.5*t)*sw+0.08*np.sin(2*np.pi*110*t)*sw*(1+0.3*np.sin(2*np.pi*.25*t))
    beat=60/134
    for k in range(int(DUR/beat)):
        tb=k*beat
        if tb<2 or 8<=tb<8.6: continue
        amp=0.9 if tb<8 and tb>=2 else 0.0
        amp=min(1,0.25+tb/8) if tb<8 else 0.9
        i=int(tb*sr);m=min(int(.35*sr),n-i);tt=np.arange(m)/sr
        y[i:i+m]+=amp*0.6*np.sin(2*np.pi*(50+80*np.exp(-tt*25))*tt)*np.exp(-tt*9)
    # flip silence then hit
    f0,f1=int(8*sr),int(8.6*sr);y[f0:f1]*=0
    i=f1;m=int(1.2*sr);tt=np.arange(m)/sr;y[i:i+m]+=0.9*np.sin(2*np.pi*(45+120*np.exp(-tt*12))*tt)*np.exp(-tt*3)
    # stamp hit
    i=int(12.6*sr);m=int(.8*sr);tt=np.arange(m)/sr;y[i:i+m]+=0.9*np.sin(2*np.pi*(40+100*np.exp(-tt*20))*tt)*np.exp(-tt*5)
    y[int(15.2*sr):]*=np.linspace(1,0,n-int(15.2*sr))
    y=y/np.max(np.abs(y))*0.8
    with wave.open(path,'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((y*32767).astype('<i2').tobytes())
def render(mode):
    d=f'/tmp/fr_{mode}';os.makedirs(d,exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch();pg=b.new_page(viewport={'width':720,'height':1280});pg.goto('file://'+os.path.abspath('page.html'))
        for i in range(int(FPS*DUR)):
            pg.evaluate(f'draw({i/FPS},"{mode}")');pg.screenshot(path=f'{d}/{i:04d}.png',clip={'x':0,'y':0,'width':720,'height':1280})
        b.close()
    music('/tmp/music.wav')
    out=f'demo_{mode}.mp4'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{d}/%04d.png','-i','/tmp/music.wav','-c:v','libx264','-pix_fmt','yuv420p','-preset','veryfast','-crf','20','-c:a','aac','-shortest',out],check=True)
for m in sys.argv[1:]: render(m)
print('xong')
