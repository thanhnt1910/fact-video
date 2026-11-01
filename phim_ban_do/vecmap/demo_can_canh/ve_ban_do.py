import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path('/home/claude/fact-video/phim_ban_do/vecmap'); name,t0,n=sys.argv[1],float(sys.argv[2]),int(sys.argv[3])
out=Path('/tmp/demo')/name; out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(args=["--allow-file-access-from-files"]); pg=b.new_page(viewport={"width":1920,"height":1080})
    pg.goto((HERE/"film.html").as_uri()+"?spec=spec_demo.js&geo=geo_nhe.js"); pg.evaluate("window.ready")
    for i in range(n):
        pg.evaluate(f"T({t0+i/24})"); pg.screenshot(path=str(out/f"{i:04d}.jpg"),type="jpeg",quality=90)
    b.close()
print('done',name)
