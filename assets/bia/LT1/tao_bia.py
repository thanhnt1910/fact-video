# Ảnh bìa video Lý Thường Kiệt (bản đồ vector). Chạy từ gốc repo: python assets/bia/LT1/tao_bia.py
# Nền: khung sạch (bỏ chữ năm, phụ đề) của cảnh vây Ung Châu, vẽ từ phim_ban_do/vecmap/film.html
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'assets/bia/LT1'
def nen():
    from playwright.sync_api import sync_playwright
    V=ROOT/'phim_ban_do/vecmap'
    with sync_playwright() as p:
        b=p.chromium.launch(args=["--allow-file-access-from-files"])
        pg=b.new_page(viewport={"width":1920,"height":1080})
        pg.goto((V/'film.html').as_uri()); pg.evaluate("window.ready"); pg.evaluate("T(4.5)")
        pg.evaluate("hud.querySelectorAll(':scope > g').forEach(e=>e.remove())")
        pg.screenshot(path=str(OUT/'nen_ungchau.jpg'),type='jpeg',quality=95); b.close()
F=ROOT/'assets/fonts/'
BLK=str(F/'BeVietnamPro-BlackItalic.ttf'); EXB=str(F/'BeVietnamPro-ExtraBoldItalic.ttf'); LORA=str(F/'Lora-Variable.ttf')
WHITE=(255,250,235); YEL=(255,205,60); RED=(200,30,30)
def font(p,s): return ImageFont.truetype(p,s)
def fit(t,p,maxw,s):
    while font(p,s).getlength(t)>maxw: s-=2
    return font(p,s)
def shadow(im,xy,t,f,fill,off=6):
    d=ImageDraw.Draw(im); d.text((xy[0]+off,xy[1]+off),t,font=f,fill=(30,10,0)); d.text(xy,t,font=f,fill=fill)
def add_logo(im,size=130):
    logo=Image.open(ROOT/'assets/logo/nguoi-gac-su-cu.png').convert('RGBA')
    l=logo.resize((size,size),Image.LANCZOS); l.putalpha(l.split()[3].point(lambda v:int(v*0.8)))
    im.alpha_composite(l,(im.size[0]-44-size,34))
def ngang(out):
    src=Image.open(OUT/'nen_ungchau.jpg').convert('RGB').crop((380,0,1540,1080))
    im=Image.new('RGBA',(1920,1080),(20,14,10,255)); im.alpha_composite(src.convert('RGBA'),(760,0))
    g=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(g)
    for x in range(1000): d.line([(x,0),(x,1080)],fill=(14,9,8,int(255*min(1,(1-x/1000)*1.6))))
    for y in range(260): d.line([(0,1080-y),(1920,1080-y)],fill=(10,6,6,int(150*(1-y/260))))
    im.alpha_composite(g); d=ImageDraw.Draw(im)
    d.polygon([(70,70),(640,62),(632,142),(62,150)],fill=RED)
    t='UNG CHÂU · NĂM 1075'; d.text((92,84),t,font=fit(t,EXB,520,48),fill=WHITE)
    shadow(im,(66,220),'ĐÁNH SANG',fit('ĐÁNH SANG',BLK,780,170),WHITE)
    shadow(im,(66,430),'ĐẤT TỐNG',fit('ĐẤT TỐNG',BLK,780,170),YEL)
    d=ImageDraw.Draw(im)
    for i,t2 in enumerate(['Một nước nhỏ vây thành của nước lớn.','Ai đã ra lệnh cho họ?']):
        d.text((72,700+i*74),t2,font=fit(t2,LORA,690,56),fill=WHITE)
    add_logo(im)
    d.line([(76,985),(156,985)],fill=YEL,width=4); d.text((176,958),'Người Gác Sử',font=font(LORA,44),fill=YEL)
    im.convert('RGB').save(out,quality=93)
if __name__=='__main__':
    if not (OUT/'nen_ungchau.jpg').exists() or 'nen' in sys.argv: nen()
    ngang(str(OUT/'LT1_ngang.jpg'))
