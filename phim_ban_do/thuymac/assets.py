import os,sys,json
from playwright.sync_api import sync_playwright
H='file://'+os.path.abspath('/tmp/gen/bd/assets.html')
SIZES={'paper_h':(1920,1080,1),'paper_v':(1080,1920,1),'far':(2800,560,1.5),'mid':(2800,620,1.5),'cliffL':(720,900,1.5),'cliffR':(620,760,1.5),'mist':(1000,300,1),
'water':(2800,800,1.5),'wave':(2600,50,1.5),'stake':(46,320,1.5),'bigboat':(430,310,1.5),'smallboat':(250,120,1.5),'blot':(1200,1200,1),'redblot':(400,400,1.5),
'splash':(420,260,1.5),'arrow':(160,16,1.5),'wreck':(260,80,1.5),'coloa':(1500,1000,1.5),'riverbed':(1700,520,1.5),'gauge':(140,640,1.5),'bigboat2':(430,340,1.5),'smallboat2':(270,140,1.5),'sun':(320,320,1.5),'reeds':(1000,300,1.5),'council':(1500,700,1.5),'coloa2':(1500,1000,1.5),'hall':(1500,860,1.5),'fig_quan':(160,200,1.5),'fig_satthu':(200,320,1.5),'fig_tuong':(200,330,1.5),'army':(1700,300,1.5),'porters':(1000,320,1.5),'court':(1700,900,1.5),'citadel':(1900,620,1.5)}
SEALS={'s937':(['937'],170,130,62),'s931':(['931'],170,130,62),'s938':(['938'],170,130,62),'s939':(['939'],170,130,62),'s944':(['944'],170,130,62),'s1288':(['1288'],200,130,58),
'sgiao':(['GIAO','VƯƠNG'],210,200,44),'stitle':(['BẠCH','ĐẰNG','938'],210,250,44)}
only=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch()
    for sc in (1,1.5):
        pg=b.new_page(device_scale_factor=sc,viewport={'width':800,'height':600});pg.goto(H);pg.wait_for_timeout(500)
        for k,(w,h,s) in SIZES.items():
            if s!=sc or (only and k not in only): continue
            pg.set_viewport_size({'width':w,'height':h});pg.evaluate(f'A.{k}()');pg.wait_for_timeout(150)
            pg.locator('#S').screenshot(path=f'/tmp/gen/bd/a/{k}.png',omit_background=True,type='png')
        if sc==1.5:
            for k,(L,w,h,fs) in SEALS.items():
                if only and k not in only: continue
                pg.set_viewport_size({'width':w+40,'height':h+40});pg.evaluate(f'sealDraw({json.dumps(L)},{w},{h},{fs})');pg.wait_for_timeout(150)
                pg.locator('#S').screenshot(path=f'/tmp/gen/bd/a/{k}.png',omit_background=True,type='png')
    b.close()
print('xong')
