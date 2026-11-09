"""Tạo avatar (1080x1080) và ảnh bìa Facebook (1640x624) cho page "Người Giải Mã".
Chạy: python assets/page-nguoi-giai-ma/tao_page.py   (cần playwright + chromium)"""
import pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
FONTS = HERE.parent.parent / "remotion" / "public"
BG1, BG2, CREAM, AMBER, DEEP = "#2b1e15", "#130c08", "#f4e9d0", "#f2b35a", "#e8913a"
BE_VI = "U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB"
LATIN = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122"
FONT_CSS = f"""
@font-face{{font-family:'BeVN';font-weight:800;src:url(file://{FONTS}/be-vietnam-pro-vietnamese-800-normal.woff2);unicode-range:{BE_VI};}}
@font-face{{font-family:'BeVN';font-weight:800;src:url(file://{FONTS}/be-vietnam-pro-latin-800-normal.woff2);unicode-range:{LATIN};}}
@font-face{{font-family:'Lora';font-style:italic;font-weight:400 700;src:url(file://{FONTS}/Lora-Italic.ttf);}}
body{{margin:0;background:{BG2}}}
"""

def hero(x, y, s, shadow_len=0):
    """Người que đội mũ cầm gậy, chân tại (x, y)."""
    sk = 5 / s
    return f'''<g transform="translate({x} {y}) scale({s})" stroke="{CREAM}" stroke-width="{sk}" stroke-linecap="round" stroke-linejoin="round" fill="none">
  <circle cx="0" cy="-69" r="11" fill="{BG2}"/>
  <path d="M -11 -80 Q -11 -98 0 -98 Q 11 -98 11 -80 Z" fill="{DEEP}" stroke="{DEEP}"/>
  <line x1="-18" y1="-80" x2="18" y2="-80" stroke="{DEEP}" stroke-width="{sk*1.2}"/>
  <line x1="0" y1="-58" x2="0" y2="-26"/><line x1="0" y1="-26" x2="-10" y2="0"/><line x1="0" y1="-26" x2="10" y2="0"/>
  <line x1="0" y1="-48" x2="-17" y2="-32"/><line x1="0" y1="-48" x2="22" y2="-40"/>
  <line x1="24" y1="0" x2="24" y2="-92" stroke="{AMBER}" stroke-width="{sk*1.2}"/>
</g>'''

def sun(x, y, r):
    rays = "".join(f'<line x1="{x+1.5*r*__import__("math").cos(a*0.5236):.1f}" y1="{y+1.5*r*__import__("math").sin(a*0.5236):.1f}" x2="{x+2.0*r*__import__("math").cos(a*0.5236):.1f}" y2="{y+2.0*r*__import__("math").sin(a*0.5236):.1f}"/>' for a in range(12))
    return f'<circle cx="{x}" cy="{y}" r="{r*3}" fill="url(#glow)"/><circle cx="{x}" cy="{y}" r="{r}" fill="{AMBER}"/><g stroke="{AMBER}" stroke-width="{r*0.22}" stroke-linecap="round">{rays}</g>'

DEFS = f'''<defs>
<radialGradient id="bg" cx="50%" cy="40%" r="80%"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></radialGradient>
<radialGradient id="globe" cx="38%" cy="32%" r="80%"><stop offset="0" stop-color="#3f7a80"/><stop offset="1" stop-color="#10272b"/></radialGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{AMBER}" stop-opacity=".45"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="80" height="80" patternUnits="userSpaceOnUse"><path d="M80 0L0 0L0 80" fill="none" stroke="{CREAM}" stroke-width="1.5" opacity=".07"/></pattern>
</defs>'''

def globe_lines(cx, cy, r):
    out = f'<g fill="none" stroke="{CREAM}" stroke-width="3" opacity=".22">'
    out += f'<ellipse cx="{cx}" cy="{cy}" rx="{r*.35}" ry="{r}"/><ellipse cx="{cx}" cy="{cy}" rx="{r*.7}" ry="{r}"/><line x1="{cx}" y1="{cy-r}" x2="{cx}" y2="{cy+r}"/>'
    for k in (-.55, 0, .55):
        dy = r * k; rx = (r*r - dy*dy) ** .5
        out += f'<ellipse cx="{cx}" cy="{cy+dy}" rx="{rx}" ry="{rx*.16}"/>'
    return out + '</g>'

# ---------- Avatar: kính lúp soi quả địa cầu, người que cầm gậy, bóng ngắn ----------
cx, cy, R = 500, 470, 290
AVATAR = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">{DEFS}
<rect width="1080" height="1080" fill="url(#bg)"/><rect width="1080" height="1080" fill="url(#grid)"/>
<g transform="translate(45 40)">
<clipPath id="lens"><circle cx="{cx}" cy="{cy}" r="{R-14}"/></clipPath>
<line x1="{cx+205}" y1="{cy+205}" x2="{cx+350}" y2="{cy+350}" stroke="{DEEP}" stroke-width="74" stroke-linecap="round"/>
<line x1="{cx+205}" y1="{cy+205}" x2="{cx+350}" y2="{cy+350}" stroke="{AMBER}" stroke-width="26" stroke-linecap="round" opacity=".55"/>
<circle cx="{cx}" cy="{cy}" r="{R-14}" fill="url(#globe)"/>
<g clip-path="url(#lens)">
 {globe_lines(cx, cy, R-14)}
 <path d="M {cx-300} {cy+250} Q {cx} {cy+170} {cx+300} {cy+250} L {cx+300} {cy+400} L {cx-300} {cy+400} Z" fill="{BG2}" opacity=".55"/>
 <path d="M {cx-300} {cy+250} Q {cx} {cy+170} {cx+300} {cy+250}" fill="none" stroke="{CREAM}" stroke-width="5" opacity=".8"/>
 {sun(cx-130, cy-120, 26)}
 <line x1="{cx-130}" y1="{cy-120}" x2="{cx-12+72}" y2="{cy+210-276}" stroke="{AMBER}" stroke-width="4" stroke-dasharray="14 12" opacity=".7"/>
 <line x1="{cx+60}" y1="{cy+207}" x2="{cx+190}" y2="{cy+212}" stroke="{DEEP}" stroke-width="16" stroke-linecap="round"/>
 {hero(cx-12, cy+207, 3.0)}
</g>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{AMBER}" stroke-width="30"/>
<circle cx="{cx}" cy="{cy}" r="{R-24}" fill="none" stroke="{CREAM}" stroke-width="3" opacity=".35"/>
</g></svg>'''

# ---------- Ảnh bìa Facebook 1640x624 ----------
COVER = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1640" height="624" viewBox="0 0 1640 624">{DEFS}
<rect width="1640" height="624" fill="url(#bg)"/><rect width="1640" height="624" fill="url(#grid)"/>
<rect x="18" y="18" width="1604" height="588" rx="10" fill="none" stroke="{CREAM}" stroke-width="2" opacity=".14"/>
<g opacity=".9">
 <line x1="1330" y1="470" x2="1610" y2="470" stroke="{CREAM}" stroke-width="3" opacity=".45"/>
 {sun(1380, 130, 22)}
 <line x1="1380" y1="130" x2="1520" y2="470" stroke="{AMBER}" stroke-width="3" stroke-dasharray="12 10" opacity=".5"/>
 <line x1="1544" y1="470" x2="1600" y2="470" stroke="{DEEP}" stroke-width="12" stroke-linecap="round"/>
 {hero(1520, 470, 2.3)}
</g>
<text x="520" y="290" font-family="BeVN" font-weight="800" font-size="96" fill="{CREAM}" stroke="{BG2}" stroke-width="7" paint-order="stroke">Người <tspan fill="{AMBER}">Giải Mã</tspan></text>
<line x1="524" y1="326" x2="1000" y2="326" stroke="{AMBER}" stroke-width="4" opacity=".7"/>
<text x="522" y="390" font-family="Lora" font-style="italic" font-weight="500" font-size="36" fill="{CREAM}">Mỗi điều ta biết đều từng có người đi tìm ra.</text>
</svg>'''

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, svg, w, h in (("avatar", AVATAR, 1080, 1080), ("bia-facebook", COVER, 1640, 624)):
        pg = b.new_page(viewport={"width": w, "height": h})
        f = HERE / f"_{name}.html"
        f.write_text(f"<style>{FONT_CSS}</style>{svg}", encoding="utf-8")
        pg.goto(f"file://{f}")
        pg.evaluate("document.fonts.load('800 40px BeVN','Người Giải Mã ờ ả ã')")
        pg.evaluate("document.fonts.load('italic 500 40px Lora','Mỗi điều')")
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(HERE / f"{name}.png"))
        pg.close()
    b.close()
for f in HERE.glob("_*.html"): f.unlink()
print("ok")
