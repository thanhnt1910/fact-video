"""Ảnh bìa video khoa học (1080x1920) có tiêu đề. Chạy: python tao_bia_video.py  -> bia-eratosthenes.png"""
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
{sun(870, 800, 46)}
<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#globe)" stroke="{CREAM}" stroke-width="5"/>
{globe_lines(cx, cy, R)}
<g stroke="{AMBER}" stroke-width="6" stroke-dasharray="14 12" opacity=".85">
 <line x1="860" y1="860" x2="{cx+60}" y2="{cy-R-70}"/><line x1="900" y1="870" x2="{cx+130}" y2="{cy-R-45}"/></g>
{hero(cx-40, cy-R+14, 2.5)}
<ellipse cx="{cx+60}" cy="{cy-R+16}" rx="50" ry="8" fill="{BG2}" opacity=".6"/>
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
<div class="tag" style="top:240px">Eratosthenes · khoảng 240 TCN</div>
<div class="t" style="top:330px;font-size:104px;line-height:1.12">Đo Trái Đất<br><span style="color:{AMBER}">bằng một cây gậy</span></div>
<div class="tag" style="top:1680px;font-size:50px;color:{CREAM}">Không cần đi hết một vòng</div>
</body></html>'''
(HERE / "_bia.html").write_text(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    pg.goto((HERE / "_bia.html").as_uri()); pg.wait_for_timeout(800)
    pg.screenshot(path=str(HERE / "bia-eratosthenes.png")); b.close()
(HERE / "_bia.html").unlink()
