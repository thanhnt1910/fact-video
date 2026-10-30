"""Bản thử vẽ tay, chân rõ ràng (4 cảnh mẫu): python phim_ban_do/phang/thu_tay_chan.py -> assets/anh_phang/lt1_tc/N_cu.jpg, N_moi.jpg"""
import sys, pathlib, io
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import flat, chitiet            # chitiet bật DETAIL
canh = chitiet.canh
from playwright.sync_api import sync_playwright
from PIL import Image
OUT = pathlib.Path(__file__).resolve().parents[2] / 'assets' / 'anh_phang' / 'lt1_tc'
OUT.mkdir(parents=True, exist_ok=True)
want = [int(a) for a in sys.argv[1:]] or [19033, 19036, 19061, 19015]
tmp = OUT / '_t.svg'
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 1080})
    for n in want:
        for tag, on in (('cu', False), ('moi', True)):
            flat.LIMBS = on
            s = (chitiet.SCN.get(n) or canh.SC[n])()
            tmp.write_text(s, encoding='utf-8'); pg.goto(tmp.as_uri())
            Image.open(io.BytesIO(pg.screenshot())).convert('RGB').save(OUT / f'{n}_{tag}.jpg', quality=92)
    br.close()
tmp.unlink(); print('xong', want)
