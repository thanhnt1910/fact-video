"""Ảnh bìa video khoa học (1080x1920) có tiêu đề. Chạy: python tao_bia_video.py  -> bia-cavendish.png"""
import importlib.util, pathlib, math
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
src = (HERE / "tao_page.py").read_text().split("# ---------- Avatar")[0]
ns = {"__file__": str(HERE / "tao_page.py")}
exec(src, ns)
DEFS, hero, sun, globe_lines, FONT_CSS = ns["DEFS"], ns["hero"], ns["sun"], ns["globe_lines"], ns["FONT_CSS"]
CREAM, AMBER, DEEP, BG2 = ns["CREAM"], ns["AMBER"], ns["DEEP"], ns["BG2"]
cx, cy, R = 540, 1210, 320
logo = (HERE / "avatar.png").as_uri()
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}
<rect width="1080" height="1920" fill="url(#bg)"/><rect width="1080" height="1920" fill="url(#grid)"/>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#globe)" stroke="{CREAM}" stroke-width="5"/>
{globe_lines(cx, cy, R)}
<text x="{cx}" y="{cy+40}" text-anchor="middle" font-family="BeVN" font-weight="800" font-size="150" fill="{CREAM}" opacity=".9">?</text>
<text x="{cx}" y="{cy+110}" text-anchor="middle" font-family="BeVN" font-weight="800" font-size="44" fill="{AMBER}">tấn</text>
<line x1="{cx}" y1="580" x2="{cx}" y2="640" stroke="{CREAM}" stroke-width="5"/>
<line x1="{cx-230}" y1="640" x2="{cx+230}" y2="640" stroke="{AMBER}" stroke-width="14" stroke-linecap="round"/>
<circle cx="{cx-230}" cy="700" r="62" fill="#8e98a3" stroke="{CREAM}" stroke-width="5"/>
<circle cx="{cx+230}" cy="700" r="62" fill="#8e98a3" stroke="{CREAM}" stroke-width="5"/>
<line x1="{cx-230}" y1="700" x2="{cx-230}" y2="698" stroke="{CREAM}"/>
{hero(cx-50, cy-R+40, 2.2)}
</svg>'''
html = f'''<html><head><style>{FONT_CSS}
body{{width:1080px;height:1920px;position:relative;overflow:hidden}}
svg{{position:absolute;left:0;top:0}}
.t{{position:absolute;left:60px;width:960px;text-align:center;font-family:BeVN;font-weight:800;color:{CREAM};text-shadow:0 6px 0 #130c08,0 0 30px #130c08}}
.tag{{position:absolute;left:60px;width:960px;text-align:center;font-family:Lora;font-style:italic;font-size:44px;color:{AMBER}}}
.brand{{position:absolute;right:160px;top:68px;font-family:BeVN;font-weight:800;font-size:38px;color:{CREAM}}}
img{{position:absolute;right:48px;top:40px;width:96px;height:96px;border-radius:48px;border:3px solid {AMBER}}}
</style></head><body>{svg}
<img src="{logo}"><div class="brand">Người <span style="color:{AMBER}">Giải Mã</span></div>
<div class="tag" style="top:240px">Henry Cavendish · năm 1797</div>
<div class="t" style="top:330px;font-size:100px;line-height:1.12">Cân cả Trái Đất<br><span style="color:{AMBER}">bằng hai quả chì</span></div>
<div class="tag" style="top:1680px;font-size:50px;color:{CREAM}">Nó nặng bao nhiêu?</div>
</body></html>'''
(HERE / "_bia.html").write_text(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    pg.goto((HERE / "_bia.html").as_uri()); pg.wait_for_timeout(800)
    pg.screenshot(path=str(HERE / "bia-cavendish.png")); b.close()
(HERE / "_bia.html").unlink()
