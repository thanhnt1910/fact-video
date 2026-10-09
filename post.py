"""
Bài đăng Facebook dạng ẢNH + BÀI VIẾT kể chuyện (đi kèm mỗi video).

Kịch bản có thêm mục "post":
  "post": {
    "hook": "Câu mở đầu (hiện trước chữ 'Xem thêm')",
    "paragraphs": ["đoạn 1", "đoạn 2", ...],
    "ending": "Câu hỏi mở cuối bài",
    "hashtags": ["nguoigacsu", ...],                      (không có thì dùng hashtags của video)
    "slides": [
      {"kind": "cover", "scene": 0, "kicker": "Chuyện có thật · 1518", "title": "…"},
      {"scene": 1, "tag": "07/1518", "text": "…"},
      {"kind": "end", "scene": 5, "text": "…"}
    ]
  }

Kết quả trong output/<mã>/:  <mã>_post_1.jpg … (ảnh 1080×1350) và <mã>_post.txt (bài viết dán thẳng).
Chạy riêng (không dựng video):  python post.py scripts/SL1.json
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _scene_credit(work, i):
    meta = Path(work) / "img" / f"scene_{i:02d}.json"
    if meta.exists():
        return json.loads(meta.read_text(encoding="utf-8")).get("credit")
    return None


def post_text(script, cfg, credits):
    p = script["post"]
    tags = p.get("hashtags") or script.get("hashtags") or []
    lines = [p["hook"], ""]
    for para in p.get("paragraphs", []):
        lines += [para, ""]
    lines += [f"{cfg.get('catchphrase', '')} 🏮", ""]
    if p.get("ending"):
        lines += [p["ending"], ""]
    lines.append(" ".join("#" + t.lstrip("#") for t in tags))
    import make_video as mv
    short = mv._short_credits(credits)
    if short:
        lines += ["", "📷 Ảnh: " + "; ".join(short) + " · nguồn Wikimedia Commons"]
    return "\n".join(lines).replace("**", "") + "\n"


def render_post(script, cfg, work, out_dir, log=print):
    """Dựng ảnh bài đăng + file bài viết. Ảnh nền lấy từ ảnh các cảnh đã tải."""
    from playwright.sync_api import sync_playwright
    p = script.get("post")
    if not p:
        return []
    slides = p.get("slides") or []
    theme = cfg["topics"][script["topic"]]
    out = []
    used_credits = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        page.goto((ROOT / "templates" / "post.html").as_uri())
        for k, s in enumerate(slides):
            img = None
            si = s.get("scene")
            if si is not None and 0 <= si < len(script["scenes"]):
                img = script["scenes"][si].get("image_src")
                c = _scene_credit(work, si)
                if c and c not in used_credits:
                    used_credits.append(c)
            data = {"slide": s, "image": img, "focus": s.get("focus"), "index": k + 1, "total": len(slides),
                    "theme": theme, "channel": cfg.get("channel", ""), "catchphrase": cfg.get("catchphrase", "")}
            page.evaluate("d => window.show(d)", data)
            page.wait_for_timeout(150)
            f = out_dir / f"{script['id']}_post_{k + 1}.jpg"
            page.screenshot(path=str(f), type="jpeg", quality=92)
            out.append(f)
        browser.close()
    (out_dir / f"{script['id']}_post.txt").write_text(post_text(script, cfg, used_credits), encoding="utf-8")
    log(f"  🖼️  Bài đăng ảnh: {len(out)} ảnh + bài viết ({script['id']}_post.txt)")
    return out


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    import make_video as mv
    import images
    cfg = mv.load_config()
    for arg in sys.argv[1:]:
        script = json.loads(Path(arg).read_text(encoding="utf-8"))
        out_dir = ROOT / "output" / script["id"]
        work = out_dir / "_work"
        work.mkdir(parents=True, exist_ok=True)
        images.fetch_scene_images(script, work, print)
        render_post(script, cfg, work, out_dir)


if __name__ == "__main__":
    main()
