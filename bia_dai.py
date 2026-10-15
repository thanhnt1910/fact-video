"""Ảnh bìa video dài thiết kế riêng cho từng tập: scripts/<mã>.json -> long.bia
  {"anh": "assets/anh_2d/TQ1/026.jpg", "nen": "assets/anh_2d/TQ1/031.jpg", "huy_hieu": "TAM QUỐC CHÍNH SỬ · TẬP 1",
   "dong1": "KHÔNG CÓ", "dong2": "VƯỜN ĐÀO", "gach": true, "dong3": "Lưu Bị <b>thật sự</b> khởi đầu thế nào?"}
Dùng:  python bia_dai.py TQ1   -> assets/bia/TQ1/TQ1_dai_thumbnail.jpg (YouTube) và TQ1_dai_thumbnail_fb.jpg (Facebook, chữ giữa).
Dựng video / gửi Telegram ưu tiên dùng hai ảnh này nếu có."""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent


def main():
    sid = sys.argv[1]
    script = json.loads((ROOT / "scripts" / f"{sid}.json").read_text(encoding="utf-8"))
    b = script["long"]["bia"]
    cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    out = ROOT / "assets" / "bia" / sid
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch()
        page = br.new_page(viewport={"width": 1920, "height": 1080})
        for mode, name in (("", f"{sid}_dai_thumbnail.jpg"), ("center", f"{sid}_dai_thumbnail_fb.jpg")):
            page.goto((ROOT / "templates" / "bia.html").as_uri())
            o = {"nen": (ROOT / b["nen"]).as_uri(), "anh": (ROOT / b["anh"]).as_uri(), "huy_hieu": b["huy_hieu"],
                 "dong1": b["dong1"], "dong2": b["dong2"], "gach": b.get("gach", False), "dong3": b["dong3"],
                 "kenh": cfg.get("channel", ""), "mode": mode}
            page.evaluate("o => window.setup(o)", o)
            page.wait_for_timeout(400)
            page.screenshot(path=str(out / name), type="jpeg", quality=93)
            print("ok", out / name)
        br.close()


if __name__ == "__main__":
    main()
