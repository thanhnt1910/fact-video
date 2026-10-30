"""Vẽ toàn bộ ảnh phẳng lt1: python phim_ban_do/phang/ve.py [số cảnh ...]  -> ke-hoach/phang/lt1_svg/N.svg và assets/anh_phang/lt1/N.jpg"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import canh
from playwright.sync_api import sync_playwright
from PIL import Image
import io
ROOT = pathlib.Path(__file__).resolve().parents[2]
SV = ROOT / 'ke-hoach' / 'phang' / 'lt1_svg'; IM = ROOT / 'assets' / 'anh_phang' / 'lt1'
SV.mkdir(parents=True, exist_ok=True); IM.mkdir(parents=True, exist_ok=True)
want = [int(a) for a in sys.argv[1:]] or sorted(canh.SC)
err = []
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 1080})
    for n in want:
        try:
            s = canh.SC[n]()
        except Exception as e:
            err.append((n, repr(e))); continue
        (SV / f'{n}.svg').write_text(s, encoding='utf-8')
        pg.goto((SV / f'{n}.svg').as_uri()); 
        Image.open(io.BytesIO(pg.screenshot())).convert('RGB').save(IM / f'{n}.jpg', quality=92)
    br.close()
print('xong', len(want) - len(err), 'ảnh; lỗi:', err)
