"""Ảnh bìa video khoa học (1080x1920) có tiêu đề. Chạy: python tao_bia_video.py  -> bia-anhsang.png"""
import importlib.util, pathlib, math
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
src = (HERE / "tao_page.py").read_text(encoding="utf-8").split("# ---------- Avatar")[0]
ns = {"__file__": str(HERE / "tao_page.py")}
exec(src, ns)
DEFS, hero, sun, globe_lines, FONT_CSS = ns["DEFS"], ns["hero"], ns["sun"], ns["globe_lines"], ns["FONT_CSS"]
CREAM, AMBER, DEEP, BG2 = ns["CREAM"], ns["AMBER"], ns["DEEP"], ns["BG2"]
cx, cy, R = 540, 1210, 320
logo = (HERE / "avatar.png").as_uri()
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}
<rect width="1080" height="1920" fill="url(#bg)"/><rect width="1080" height="1920" fill="url(#grid)"/>
<circle cx="{cx}" cy="1230" r="300" fill="#c98f5e" stroke="{CREAM}" stroke-width="5"/>
<g stroke="#7b4e2f" stroke-width="28" opacity=".55" stroke-linecap="round"><line x1="{cx-245}" y1="1135" x2="{cx+245}" y2="1135"/><line x1="{cx-290}" y1="1230" x2="{cx+290}" y2="1230"/><line x1="{cx-235}" y1="1325" x2="{cx+235}" y2="1325"/></g>
<circle cx="{cx}" cy="1230" r="430" fill="none" stroke="{CREAM}" stroke-width="3" stroke-dasharray="8 16" opacity=".5"/>
<circle cx="{cx+300}" cy="930" r="32" fill="{CREAM}" stroke="{AMBER}" stroke-width="6"/>
<circle cx="170" cy="760" r="64" fill="{AMBER}" stroke="{CREAM}" stroke-width="5"/>
<circle cx="170" cy="760" r="118" fill="{AMBER}" opacity=".18"/>
<g stroke="{AMBER}" stroke-width="7" stroke-dasharray="6 22" stroke-linecap="round" opacity=".9"><line x1="250" y1="790" x2="{cx+260}" y2="915"/></g>
{hero(900, 800, 2.2)}
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
<div class="tag" style="top:240px">Rømer · năm 1676</div>
<div class="t" style="top:330px;font-size:82px;line-height:1.12">Đo ánh sáng<br><span style="color:{AMBER}">bằng một mặt trăng</span></div>
<div class="tag" style="top:1680px;font-size:50px;color:{CREAM}">Nó nhanh cỡ nào?</div>
</body></html>'''
(HERE / "_bia.html").write_text(html, encoding="utf-8")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    pg.goto((HERE / "_bia.html").as_uri()); pg.wait_for_timeout(800)
    pg.screenshot(path=str(HERE / "bia-anhsang.png")); b.close()
(HERE / "_bia.html").unlink()
