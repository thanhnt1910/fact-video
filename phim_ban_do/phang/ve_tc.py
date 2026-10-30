"""Vẽ toàn bộ 64 ảnh với tay, chân rõ (flat.LIMBS) vào thư mục thử: python phim_ban_do/phang/ve_tc.py [số cảnh ...] -> assets/anh_phang/lt1_tc/all/N.jpg"""
import sys, pathlib, io
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import flat, chitiet
flat.LIMBS = True
canh = chitiet.canh
from playwright.sync_api import sync_playwright
from PIL import Image
OUT = pathlib.Path(__file__).resolve().parents[2] / 'assets' / 'anh_phang' / 'lt1_tc' / 'all'
OUT.mkdir(parents=True, exist_ok=True)
want = [int(a) for a in sys.argv[1:]] or sorted(set(canh.SC) | set(chitiet.SCN))
tmp = OUT / '_t.svg'; err = []
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 1080})
    for n in want:
        try: s = (chitiet.SCN.get(n) or canh.SC[n])()
        except Exception as e: err.append((n, repr(e))); continue
        tmp.write_text(s, encoding='utf-8'); pg.goto(tmp.as_uri())
        Image.open(io.BytesIO(pg.screenshot())).convert('RGB').save(OUT / f'{n}.jpg', quality=90)
    br.close()
tmp.unlink(); print('xong', len(want) - len(err), 'lỗi', err)
