import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path('/home/claude/fact-video/phim_ban_do/vecmap'); out=Path(sys.argv[1]); a,b=int(sys.argv[2]),int(sys.argv[3]); out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    br=p.chromium.launch(args=["--allow-file-access-from-files"]); pg=br.new_page(viewport={"width":1920,"height":1080})
    pg.goto((HERE/"film_cc.html").as_uri()+"?spec=spec_cc.js&geo=geo_nhe.js"); pg.evaluate("window.ready")
    for i in range(a,b):
        pg.evaluate(f"T({i/24})"); pg.screenshot(path=str(out/f"{i:04d}.jpg"),type="jpeg",quality=90)
    br.close()
