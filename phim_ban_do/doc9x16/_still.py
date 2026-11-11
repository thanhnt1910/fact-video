import sys,json
from playwright.sync_api import sync_playwright
from PIL import Image
page=sys.argv[1];out=sys.argv[2];ts=[float(x) for x in sys.argv[3:]]
with sync_playwright() as p:
    br=p.chromium.launch(args=['--allow-file-access-from-files']);pg=br.new_page(viewport={'width':1080,'height':1920})
    pg.on('pageerror',lambda e:print('LỖI TRANG',e));pg.on('console',lambda m:print('log',m.text) if m.type=='error' else None)
    pg.goto('file://'+page);pg.wait_for_timeout(800)
    ims=[]
    for t in ts:
        pg.evaluate(f'render({t})');pg.screenshot(path='/tmp/_f.png');ims.append(Image.open('/tmp/_f.png').convert('RGB').copy())
    W=540;sh=Image.new('RGB',(W*len(ims),960))
    for i,im in enumerate(ims):sh.paste(im.resize((W,960)),(i*W,0))
    sh.save(out,quality=88)
    br.close()
