import sys, io, math, subprocess
sys.path.insert(0, 'nhan_vat_ma')
import cairosvg, numpy as np
from PIL import Image
from puppet import *
W,H,FPS,N=600,800,24,96
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
  '-c:v','libx264','-pix_fmt','yuv420p',sys.argv[1]],stdin=subprocess.PIPE)
for i in range(N):
    t=i/FPS
    if t<1.5: pose=pose_walk(t*2*math.pi*1.2); face=FACES["bình thản"]
    elif t<2.5: pose=pose_point(); face=FACES["giận"]
    else: pose=pose_bow() if int(t*2)%2==0 else pose_cheer(); face=FACES["tinh nghịch"]
    svg=render_svg(NOBUNAGA,pose,face,bg="#f3e9d2")
    im=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=W))).convert("RGB")
    p.stdin.write(np.asarray(im).tobytes())
p.stdin.close(); p.wait()
