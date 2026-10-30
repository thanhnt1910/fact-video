"""Dựng thử 1 đoạn video (6 giây) từ ảnh có tay, chân rõ: python phim_ban_do/phang/thu_video_tc.py [số cảnh] -> assets/clips_phang/lt1_tc/N.mp4"""
import sys, pathlib, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import flat
flat.LIMBS = True
import dong_lt1 as D
D.OUT = D.ROOT / 'assets' / 'clips_phang' / 'lt1_tc'
from playwright.sync_api import sync_playwright
ns = [int(a) for a in sys.argv[1:]] or [19015]
tmp = pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 1080})
    for n in ns:
        D.render_one(pg, n, tmp); print('xong', n)
    br.close()
