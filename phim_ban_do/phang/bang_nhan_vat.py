"""Bảng nhân vật xin duyệt: python phim_ban_do/phang/bang_nhan_vat.py -> /tmp/bnv.png"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from chitiet import *   # noqa
import flat; flat.DETAIL = True
from flat import sh
from nguoi_nghieng import side_fig
from playwright.sync_api import sync_playwright
items = [
 ('A. Lính Đại Việt', '#7a5a3a', dict(hat='khan', seed=61, pants='#3a2a1a', armor=None, sash='#a8452f', spear='#a8452f'), 'khăn quấn, áo vải nâu, giáo'),
 ('B. Lính Đại Việt mặc giáp', '#6e4f30', dict(hat='khan', seed=62, pants='#3a2a1a', armor='#5a4028', sash='#a8452f', spear='#a8452f'), 'một phần lính mặc giáp da + sắt'),
 ('C. Dân phu vác đất', '#8a6a44', dict(hat='cone', seed=63, pants='#4a3a24', armor=None, sash='#8a6a44'), 'nón lá chỉ cho dân phu'),
 ('D. Lính Tống bộ binh', '#3a4a6a', dict(hat='songhelm', seed=64, pants='#26304a', armor='#566070', sash='#2e4a80', spear='#2e4a80'), 'mũ sắt chỏm nhọn, giáp vảy, tấm che gáy'),
 ('E. Tướng Tống', '#34445f', dict(hat='songtuong', seed=65, pants='#26304a', armor='#6a7280', sash='#2e4a80', spear='#2e4a80', beard='black'), 'mũ sắt có chùm lông xanh'),
 ('F. Lý Thường Kiệt, phương án 1', '#7a2f26', dict(hat='khantuong', seed=66, pants='#2a1c18', armor='#4a3a2a', sash='#d8b04a', beard='black'), 'khăn đỏ + búi tóc cài trâm, giáp vảy, vai giáp, áo choàng'),
 ('G. Lý Thường Kiệt, phương án 2', '#7a2f26', dict(hat='mugiap_vn', seed=66, pants='#2a1c18', armor='#4a3a2a', sash='#d8b04a', beard='black'), 'mũ giáp riêng kiểu búp sen, giáp vảy, vai giáp'),
]
L = ['<rect width="1920" height="1080" fill="#d9cfb4"/><rect y="860" width="1920" height="220" fill="#8a7a5a"/>']
for i, (name, col, kw, note) in enumerate(items):
    x = 140 + i * 270
    L.append(side_fig(f'p{i}', x, 740, 1.55, col, flip=1, **kw).replace('class="sf"', 'class="sf stat"'))
    import textwrap
    for j, ln in enumerate(textwrap.wrap(name, 17)):
        L.append(f'<text x="{x}" y="{925+j*28}" text-anchor="middle" font-size="24" font-weight="700" fill="#2a1d10" font-family="Lora">{ln}</text>')
    for j, ln in enumerate(textwrap.wrap(note, 24)):
        L.append(f'<text x="{x}" y="{998+j*24}" text-anchor="middle" font-size="19" fill="#3a2a18" font-family="Lora">{ln}</text>')
svg_ = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">{"".join(L)}</svg>'
p = pathlib.Path('/tmp/bnv.svg'); p.write_text(svg_, encoding='utf-8')
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 1080}); pg.goto(p.as_uri()); pg.screenshot(path='/tmp/bnv.png'); br.close()
