import sys,os
SPECJS=os.environ.get("SPECJS","spec_cc.js")
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path('/home/claude/fact-video/phim_ban_do/vecmap'); out=Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=True)
ts=[float(x) for x in sys.argv[2:]]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--allow-file-access-from-files"]); pg=b.new_page(viewport={"width":1920,"height":1080})
    pg.on("console",lambda m:print("console:",m.text)); pg.on("pageerror",lambda e:print("ERR",e))
    pg.goto((HERE/"film_cc.html").as_uri()+"?spec="+SPECJS+"&geo=geo_nhe.js"); pg.evaluate("window.ready")
    for t in ts:
        pg.evaluate(f"T({t})"); pg.screenshot(path=str(out/f"t{t:05.2f}.jpg"),type="jpeg",quality=88)
    b.close()
