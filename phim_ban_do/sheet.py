import sys,time
beats=[int(x) for x in sys.argv[2:]];name=sys.argv[1]
sys.argv=['x','none']
import mapfilm2 as M
from build2 import T,D
from PIL import Image
ts=[T[n]+D[n]*0.6 for n in beats]
cols=3;rows=(len(ts)+cols-1)//cols
sh=Image.new('RGB',(1920,360*rows))
for i,t in enumerate(ts):
    sh.paste(M.frame(t).resize((640,360)),((i%cols)*640,(i//cols)*360))
sh.save(f'/tmp/proto/{name}.jpg',quality=88)
