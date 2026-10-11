"""
Tự tìm ảnh hợp lệ (không vi phạm bản quyền) cho từng cảnh.

Trong kịch bản, mỗi cảnh có thể có:
  "image": {"query": "octopus underwater"}                     # tự tìm (từ khóa tiếng Anh cho kết quả tốt hơn)
  "image": {"query": "Gobekli Tepe pillar", "source": "wikimedia"}
  "image": {"url": "https://...jpg", "credit": "Tên tác giả, CC0"}   # chỉ định thẳng

Nguồn và giấy phép được nhận:
  - Openverse  : CC0, Public Domain Mark, CC BY (ghi nguồn)       — không cần mã
  - Wikimedia  : Public domain, CC0, CC BY (ghi nguồn)             — không cần mã
  - NASA       : ảnh của NASA (public domain)                      — không cần mã
  - Met Museum : hiện vật isPublicDomain = CC0                     — không cần mã
  - Pixabay    : Giấy phép Pixabay (dùng thương mại, không cần ghi) — cần PIXABAY_API_KEY
Luôn LOẠI: CC BY-SA (ràng buộc chia sẻ tương tự), NC (cấm thương mại), ND (cấm chỉnh sửa).
"""
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = "NguoiGacSuVideo/1.0 (https://github.com/thanhnt1910/fact-video; educational history videos)"
MIN_SHORT_SIDE = 700

TOPIC_SOURCES = {
    "co-dai": ["met", "wikimedia", "openverse"],
    "lich-su": ["wikimedia", "met", "openverse"],
    "vu-tru": ["nasa", "wikimedia", "openverse"],
    "tam-tri": ["openverse", "wikimedia"],
    "su-la": ["wikimedia", "met", "openverse"],
    "bi-an": ["wikimedia", "openverse", "met"],
    "sinh-ton": ["wikimedia", "openverse"],
    "phi-vu": ["wikimedia", "met", "openverse"],
    "than-thoai": ["met", "wikimedia", "openverse"],
    "default": ["pixabay", "openverse", "wikimedia"],
}


def _get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _strip_html(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


# ------------------------------------------------------------------ các nguồn
def search_openverse(q):
    url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({
        "q": q, "license": "cc0,pdm,by", "page_size": 20, "mature": "false", "category": "photograph"})
    out = []
    for r in _get(url).get("results", []):
        lic = (r.get("license") or "").lower()
        if lic not in ("cc0", "pdm", "by"):
            continue
        src = (r.get("source") or "") + " " + (r.get("creator") or "")
        if re.search(r"biodiversity|biodivlibrary|internet archive book|bhl", src, re.I):
            continue
        w, h = r.get("width") or 0, r.get("height") or 0
        if w and h and min(w, h) < MIN_SHORT_SIDE:
            continue
        credit = (f"\"{r.get('title') or 'Ảnh'}\" – {r.get('creator') or 'không rõ'}, "
                  f"{'CC0' if lic == 'cc0' else 'Public Domain' if lic == 'pdm' else 'CC BY ' + (r.get('license_version') or '')}"
                  f" ({r.get('foreign_landing_url') or r.get('url')})")
        text = " ".join([r.get("title") or ""] + [t.get("name", "") for t in (r.get("tags") or [])])
        out.append({"url": r.get("url"), "thumb": r.get("thumbnail"), "w": w, "h": h, "credit": credit,
                    "needs_credit": lic == "by", "text": text})
    return out


def search_wikimedia(q):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"filetype:bitmap {q}", "gsrlimit": 20, "prop": "imageinfo",
        "iiprop": "url|size|extmetadata|mime", "iiurlwidth": 1600})
    # (thumburl 1600px dùng làm ảnh chính, cũng đủ nhỏ để duyệt)
    pages = sorted((_get(url).get("query", {}).get("pages", {}) or {}).values(), key=lambda p: p.get("index", 99))
    out = []
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata", {})
        lic = (meta.get("LicenseShortName", {}).get("value") or "").strip()
        low = lic.lower()
        ok = ("public domain" in low or low.startswith("pd") or low == "cc0"
              or (low.startswith("cc by") and "sa" not in low and "nc" not in low and "nd" not in low))
        if not ok or ii.get("mime") not in ("image/jpeg", "image/png"):
            continue
        w, h = ii.get("width") or 0, ii.get("height") or 0
        if min(w, h) < MIN_SHORT_SIDE:
            continue
        artist = _strip_html(meta.get("Artist", {}).get("value")) or "không rõ"
        credit = f"\"{p.get('title', '').replace('File:', '')}\" – {artist}, {lic} ({ii.get('descriptionurl')})"
        desc = _strip_html(meta.get("ImageDescription", {}).get("value"))[:300]
        out.append({"url": ii.get("thumburl") or ii.get("url"), "w": w, "h": h, "credit": credit,
                    "needs_credit": low.startswith("cc by"), "text": p.get("title", "") + " " + desc})
    return out


def search_nasa(q):
    url = "https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"q": q, "media_type": "image"})
    out = []
    for it in _get(url).get("collection", {}).get("items", [])[:20]:
        d = (it.get("data") or [{}])[0]
        nid = d.get("nasa_id")
        if not nid:
            continue
        img = f"https://images-assets.nasa.gov/image/{urllib.parse.quote(nid)}/{urllib.parse.quote(nid)}~large.jpg"
        out.append({"url": img, "thumb": img.replace("~large", "~small"), "w": 0, "h": 0,
                    "credit": f"\"{d.get('title', nid)}\" – NASA ({d.get('center', '')})", "text": d.get("title", "") + " " + d.get("description", "")[:300],
                    "needs_credit": False})
    return out


def search_met(q):
    url = "https://collectionapi.metmuseum.org/public/collection/v1/search?" + urllib.parse.urlencode(
        {"hasImages": "true", "q": q})
    ids = (_get(url).get("objectIDs") or [])[:12]
    out = []
    for oid in ids:
        try:
            o = _get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}")
        except Exception:
            continue
        if not o.get("isPublicDomain") or not o.get("primaryImage"):
            continue
        out.append({"url": o["primaryImage"], "thumb": o.get("primaryImageSmall"), "w": 0, "h": 0,
                    "text": " ".join(str(o.get(k, "")) for k in ("title", "objectName", "culture", "period")),
                    "credit": f"\"{o.get('title', '')}\" – The Metropolitan Museum of Art, CC0 ({o.get('objectURL', '')})",
                    "needs_credit": False})
        if len(out) >= 5:
            break
    return out


def search_pixabay(q):
    key = os.environ.get("PIXABAY_API_KEY", "").strip()
    if not key:
        return []
    url = "https://pixabay.com/api/?" + urllib.parse.urlencode({
        "key": key, "q": q[:100], "image_type": "photo", "safesearch": "true", "per_page": 20})
    out = []
    for h in _get(url).get("hits", []):
        if min(h.get("imageWidth", 0), h.get("imageHeight", 0)) < MIN_SHORT_SIDE:
            continue
        out.append({"url": h.get("largeImageURL"), "thumb": h.get("webformatURL"), "text": h.get("tags", ""),
                    "w": h.get("imageWidth"), "h": h.get("imageHeight"),
                    "credit": f"Pixabay – {h.get('user', '')} ({h.get('pageURL', '')})", "needs_credit": False})
    return out


SOURCES = {"openverse": search_openverse, "wikimedia": search_wikimedia, "nasa": search_nasa,
           "met": search_met, "pixabay": search_pixabay}


# ------------------------------------------------------------------ tải ảnh
def _download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read()
    if len(data) < 15000:
        raise ValueError("ảnh quá nhỏ hoặc lỗi")
    dest.write_bytes(data)
    return dest


def _norm_txt(t):
    import unicodedata
    t = unicodedata.normalize("NFD", t or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t)


def _relevant(c, subject):
    """Ảnh phải nhắc tới chủ thể chính (từ đầu tiên của từ khóa, hoặc trường 'subject')."""
    if not subject or "text" not in c:
        return True
    words = [w for w in _norm_txt(subject).split() if len(w) >= 3]
    hay = " " + _norm_txt(c["text"]) + " "
    return all((" " + w) in hay for w in words) if words else True


def _crop(path, box):
    """Cắt 1 vùng của ảnh: box = [trái, trên, phải, dưới] theo tỉ lệ 0..1 (dùng cho ảnh ghép nhiều ô)."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    w, h = im.size
    l, t, r, b = box
    im.crop((int(l * w), int(t * h), int(r * w), int(b * h))).save(path, quality=95)


def _score(c, used):
    if c["url"] in used:
        return -1
    w, h = c.get("w") or 0, c.get("h") or 0
    s = 1.0
    if w and h:
        s += min(h / w, 1.6) * 0.4          # ưu tiên ảnh dọc / vuông cho video dọc
        s += min(min(w, h) / 1500, 1) * 0.3  # ưu tiên ảnh nét
    if not c.get("needs_credit"):
        s += 0.1
    return s


def license_ok(credit):
    """Chỉ nhận ảnh hết bản quyền / CC0 / CC BY (không SA, NC, ND). Ghi nguồn phải nêu rõ giấy phép."""
    low = (credit or "").lower()
    if any(x in low for x in ("by-sa", "by sa", "share alike", "sharealike", "-nc", " nc ", "noncommercial",
                              "-nd", " nd ", "noderiv", "all rights reserved", "fair use")):
        return False
    return any(x in low for x in ("public domain", "cc0", "pdm", "no restrictions", "cc by", "cc-by"))


def fetch_scene_images(script, work, log=print):
    """Gắn 'image_src' (đường dẫn file) vào các cảnh có 'image'. Trả về danh sách ghi nguồn."""
    img_dir = Path(work) / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    topic = script.get("topic", "")
    credits, used = [], set()
    for i, sc in enumerate(script["scenes"]):
        spec = sc.get("image")
        if not spec:
            continue
        if isinstance(spec, str):
            spec = {"query": spec}
        dest = img_dir / f"scene_{i:02d}.jpg"
        meta = img_dir / f"scene_{i:02d}.json"
        key = json.dumps(spec, ensure_ascii=False, sort_keys=True)
        if dest.exists() and meta.exists():
            m = json.loads(meta.read_text(encoding="utf-8"))
            if m.get("key") == key:
                sc["image_src"] = dest.resolve().as_uri()
                credits.append(m["credit"])
                used.add(m.get("url"))
                continue
        cands = []
        if spec.get("url"):
            credit = spec.get("credit", "")
            if not license_ok(credit) and not spec.get("url", "").startswith("file:"):
                log(f"     ⛔ cảnh {i + 1}: bỏ ảnh vì giấy phép không rõ hoặc không cho phép dùng: {credit[:120]}")
                continue
            cands = [{"url": spec["url"], "credit": credit or spec["url"], "w": 0, "h": 0}]
        else:
            srcs = [spec["source"]] if spec.get("source") else TOPIC_SOURCES.get(topic, TOPIC_SOURCES["default"])
            for src in srcs:
                try:
                    found = SOURCES[src](spec["query"])
                except Exception as e:
                    log(f"     ⚠️  {src}: {e}")
                    found = []
                if found:
                    cands = found
                    log(f"     🔎 cảnh {i + 1}: {len(found)} ảnh từ {src}")
                    break
                time.sleep(0.5)
        subject = spec.get("subject") or (spec.get("query", "").split() or [""])[0]
        if not spec.get("url"):
            rel = [c for c in cands if _relevant(c, subject)]
            if len(rel) < len(cands):
                log(f"     🧹 bỏ {len(cands) - len(rel)} ảnh không đúng chủ thể \"{subject}\"")
            cands = rel
        # ảnh chỉ định sẵn (url) được dùng lại nhiều lần, ví dụ cắt các ô khác nhau từ 1 ảnh ghép
        cands = sorted([c for c in cands if spec.get("url") or _score(c, used) > 0], key=lambda c: -_score(c, used))
        ok = False
        for c in cands[:5]:
            try:
                _download(c["url"], dest)
                if spec.get("crop"):
                    _crop(dest, spec["crop"])
                meta.write_text(json.dumps({"key": key, "credit": c["credit"], "url": c["url"]},
                                           ensure_ascii=False), encoding="utf-8")
                sc["image_src"] = dest.resolve().as_uri()
                credits.append(c["credit"])
                used.add(c["url"])
                ok = True
                break
            except Exception as e:
                log(f"     ⚠️  tải ảnh lỗi: {e}")
        if not ok:
            log(f"     ℹ️  cảnh {i + 1}: không tìm được ảnh phù hợp cho \"{spec.get('query', spec.get('url'))}\" — dùng đồ họa")
    return credits


# ======================================================================= duyệt ảnh ứng viên
def collect_candidates(script, per_scene=8, log=print):
    """Tìm ứng viên cho mọi cảnh có 'image' (kể cả cảnh đã chọn url) để người/Claude duyệt."""
    topic = script.get("topic", "")
    result = []
    for i, sc in enumerate(script["scenes"]):
        spec = sc.get("image")
        if not spec:
            continue
        if isinstance(spec, str):
            spec = {"query": spec}
        q = spec.get("query")
        if not q:
            continue
        srcs = [spec["source"]] if spec.get("source") else TOPIC_SOURCES.get(topic, TOPIC_SOURCES["default"])
        cands = []
        for src in srcs:
            try:
                found = SOURCES[src](q)
            except Exception as e:
                log(f"  ⚠️  {src}: {e}")
                found = []
            subject = spec.get("subject") or (q.split() or [""])[0]
            found = [dict(c, source=src) for c in found if _relevant(c, subject)]
            cands += found
            if len(cands) >= per_scene:
                break
        result.append({"scene": i, "query": q, "candidates": cands[:per_scene]})
    return result


def make_contact_sheet(entries, work, out_jpg, out_json):
    from PIL import Image, ImageDraw, ImageFont
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    tw, th, pad, head = 240, 320, 8, 46
    rows = []
    for e in entries:
        ims = []
        for k, c in enumerate(e["candidates"]):
            p = work / f"c{e['scene']}_{k}.jpg"
            try:
                _download(c.get("thumb") or c["url"], p)
                im = Image.open(p).convert("RGB")
                im.thumbnail((tw * 3, th * 3))
                r = max(tw / im.width, th / im.height)
                im = im.resize((max(tw, int(im.width * r)), max(th, int(im.height * r))))
                l, t = (im.width - tw) // 2, (im.height - th) // 2
                ims.append(im.crop((l, t, l + tw, t + th)))
            except Exception:
                ims.append(Image.new("RGB", (tw, th), (60, 0, 0)))
        rows.append((e, ims))
    W = pad + 8 * (tw + pad)
    H = sum(head + th + pad for _ in rows) + pad
    sheet = Image.new("RGB", (W, max(H, 100)), (20, 20, 24))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
        small = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
    except Exception:
        font = small = ImageFont.load_default()
    y = pad
    for e, ims in rows:
        d.text((pad, y + 10), f"Canh {e['scene'] + 1}: \"{e['query']}\"", fill=(255, 220, 120), font=font)
        y += head
        for k, im in enumerate(ims):
            x = pad + k * (tw + pad)
            sheet.paste(im, (x, y))
            d.rectangle([x, y, x + 40, y + 38], fill=(0, 0, 0))
            d.text((x + 10, y + 4), str(k), fill=(255, 255, 255), font=small)
        y += th + pad
    sheet.save(out_jpg, quality=85)
    Path(out_json).write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    import sys
    ROOTP = Path(__file__).resolve().parent
    ids = [x.strip() for x in (sys.argv[1] if len(sys.argv) > 1 else "").split(",") if x.strip()]
    (ROOTP / "logs").mkdir(exist_ok=True)
    for f in sorted((ROOTP / "scripts").glob("*.json")):
        sc = json.loads(f.read_text(encoding="utf-8"))
        if ids and sc.get("id") not in ids:
            continue
        print(f"== {sc['id']} ==", flush=True)
        ent = collect_candidates(sc)
        make_contact_sheet(ent, ROOTP / "output" / "_cand" / sc["id"],
                           ROOTP / "logs" / f"cand_{sc['id']}.jpg", ROOTP / "logs" / f"cand_{sc['id']}.json")
        print(f"   {sum(len(e['candidates']) for e in ent)} ứng viên", flush=True)
