import sys,subprocess
from PIL import Image
mod=sys.argv[1];args=sys.argv[2:]
subprocess.run(['python3',f'/tmp/gen/bd/{mod}.py','soi']+args,check=True)
V=mod=='doc'
cw,ch=(360,640) if V else (960,540);cols=5 if V else 3
rows=(len(args)+cols-1)//cols
sh=Image.new('RGB',(cw*cols,ch*rows),'white')
for i,x in enumerate(args):sh.paste(Image.open(f'/tmp/gen/bd/out/s_{x}.jpg').resize((cw,ch)),(cw*(i%cols),ch*(i//cols)))
if sh.width>1920: sh=sh.resize((1920,int(sh.height*1920/sh.width)))
sh.save('/tmp/gen/bd/out/sheet.jpg',quality=80)
