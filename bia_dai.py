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


def main_moi(sid, script, b, cfg):
    """Kiểu bìa mới (templates/bia2.html): ảnh nền vẽ riêng cho tập, chữ dựng bằng mã.
    long.bia: anh_rong, anh_doc (ảnh nền đã chọn trong assets/anh_2d/<mã>BIA/), huy_hieu, dong1, dong2, gach, dong3."""
    out = ROOT / "assets" / "bia" / sid
    out.mkdir(parents=True, exist_ok=True)
    sb = script.get("ngan", {}).get("bia") or b
    jobs = [((1920, 1080), "w", b["anh_rong"], b, f"{sid}_dai_thumbnail.jpg"),
            ((1920, 1080), "c", b["anh_rong"], b, f"{sid}_dai_thumbnail_fb.jpg"),
            ((1080, 1920), "v", b["anh_doc"], sb, f"{sid}_thumbnail.jpg")]
    with sync_playwright() as p:
        br = p.chromium.launch()
        for (w, h), mode, anh, t, name in jobs:
            page = br.new_page(viewport={"width": w, "height": h})
            page.goto((ROOT / "templates" / "bia2.html").as_uri())
            o = {"anh": (ROOT / anh).as_uri(), "huy_hieu": t["huy_hieu"], "dong1": t["dong1"], "dong2": t["dong2"],
                 "gach": t.get("gach", False), "dong3": t["dong3"], "kenh": cfg.get("channel", ""), "mode": mode,
                 "vi_tri": t.get("vi_tri_doc" if mode == "v" else "vi_tri_rong") or t.get("vi_tri")}
            page.evaluate("o => window.setup(o)", o)
            page.wait_for_timeout(500)
            page.screenshot(path=str(out / name), type="jpeg", quality=93)
            print("ok", out / name)
        br.close()


def main():
    sid = sys.argv[1]
    script = json.loads((ROOT / "scripts" / f"{sid}.json").read_text(encoding="utf-8"))
    b = script["long"]["bia"]
    cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    if b.get("anh_rong"):
        return main_moi(sid, script, b, cfg)
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
        # ảnh bìa video ngắn (dọc 9:16)
        page = br.new_page(viewport={"width": 1080, "height": 1920})
        sb = script.get("ngan", {}).get("bia") or b
        page.goto((ROOT / "templates" / "bia.html").as_uri())
        o = {"nen": (ROOT / sb["nen"]).as_uri(), "anh": (ROOT / sb["anh"]).as_uri(), "huy_hieu": sb["huy_hieu"],
             "dong1": sb["dong1"], "dong2": sb["dong2"], "gach": sb.get("gach", False), "dong3": sb["dong3"],
             "kenh": cfg.get("channel", ""), "mode": "v"}
        page.evaluate("o => window.setup(o)", o)
        page.wait_for_timeout(400)
        page.screenshot(path=str(out / f"{sid}_thumbnail.jpg"), type="jpeg", quality=93)
        print("ok", out / f"{sid}_thumbnail.jpg")
        br.close()


if __name__ == "__main__":
    main()
