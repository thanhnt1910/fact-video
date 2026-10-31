"""Vẽ khung hình video lt1v3. python ve_film.py still <đoạn|giây>... | khung <từ> <đến> <thư mục>  (24 khung/giây)"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FPS = 24
import os
SPJS = os.environ.get("SPEC_JS", "spec.js")
SP = json.load(open(HERE / os.environ.get("SFX_JSON", "sfx.json")))


def main():
    mode = sys.argv[1]
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        msgs = []
        pg.on("pageerror", lambda e: msgs.append(str(e)[:200]))
        pg.goto((HERE / "film.html").as_uri() + "?spec=" + SPJS + "&geo=" + os.environ.get("GEO_JS", "geo_nhe.js"))
        pg.evaluate("window.ready")
        if mode == "still":
            out = HERE / "ra" / "film"
            out.mkdir(parents=True, exist_ok=True)
            for a in sys.argv[2:]:
                t = SP["starts"][a[1:]] + 2.5 if a.startswith("d") else float(a)
                pg.evaluate(f"T({t})")
                pg.screenshot(path=str(out / f"{a}.jpg"), type="jpeg", quality=88)
                print("ok", a, round(t, 1), flush=True)
        else:
            a, c, d = int(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4])
            d.mkdir(parents=True, exist_ok=True)
            for i in range(a, c):
                pg.evaluate(f"T({i / FPS})")
                pg.screenshot(path=str(d / f"{i:05d}.jpg"), type="jpeg", quality=88)
        if msgs:
            print("LỖI JS:", msgs[:3])
        b.close()


main()
