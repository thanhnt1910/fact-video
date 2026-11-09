"""Tìm và tải ảnh tư liệu từ Wikimedia Commons (chạy trên GitHub, máy làm việc không vào được Commons).
python tai_anh_commons.py assets/xk1
- tim.json : {"danh_muc": ["Category:..."], "tim": ["từ khóa"]} -> ghi ung_vien.json (tên, đường dẫn ảnh, tác giả, giấy phép, kích thước)
- chon.json: {"khoa": {"title": "File:...", "slot": "S1", "so": 1}} -> tải ảnh <khoa>.jpg và ghi nguon.json (kèm ghi công)
"""
import json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
UA = {"User-Agent": "NguoiGacSu/1.0 (https://github.com/thanhnt1910/fact-video; noreply@anthropic.com)"}
API = "https://commons.wikimedia.org/w/api.php"
def api(**p):
    p["format"] = "json"
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(p), headers=UA)
    for t in range(3):
        try:
            return json.loads(urllib.request.urlopen(req, timeout=60).read())
        except Exception as e:
            print("lỗi api", t, e); time.sleep(4 * (t + 1))
    return {}
def clean(s): return re.sub(r"<[^>]+>", "", s or "").strip()
def info(pages):
    out = []
    for pg in pages.values():
        ii = (pg.get("imageinfo") or [{}])[0]; md = ii.get("extmetadata", {})
        out.append({"title": pg.get("title"), "url": ii.get("thumburl") or ii.get("url"), "w": ii.get("width"), "h": ii.get("height"),
                    "tac_gia": clean(md.get("Artist", {}).get("value")), "giay_phep": md.get("LicenseShortName", {}).get("value"),
                    "mo_ta": clean(md.get("ImageDescription", {}).get("value"))[:160]})
    return out
d = Path(sys.argv[1])
if (d / "tim.json").exists():
    q = json.loads((d / "tim.json").read_text(encoding="utf-8")); res = []
    IP = dict(prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=1920)
    for c in q.get("danh_muc", []):
        r = api(action="query", generator="categorymembers", gcmtitle=c, gcmtype="file", gcmlimit=60, **IP)
        res += info(r.get("query", {}).get("pages", {}))
    for s in q.get("tim", []):
        r = api(action="query", generator="search", gsrsearch=s, gsrnamespace=6, gsrlimit=20, **IP)
        res += info(r.get("query", {}).get("pages", {}))
    seen = set(); uniq = []
    for x in res:
        if x["title"] not in seen: seen.add(x["title"]); uniq.append(x)
    (d / "ung_vien.json").write_text(json.dumps(uniq, ensure_ascii=False, indent=1), encoding="utf-8"); print("ứng viên:", len(uniq))
if (d / "chon.json").exists():
    ch = json.loads((d / "chon.json").read_text(encoding="utf-8")); nguon = {}
    for k, v in ch.items():
        r = api(action="query", titles=v["title"], prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=1920)
        got = info(r.get("query", {}).get("pages", {}))
        if not got or not got[0]["url"]: print("không thấy", k, v["title"]); continue
        g = got[0]; out = d / f"{k}.jpg"
        if not (out.exists() and out.stat().st_size > 5000):
            for t in range(3):
                try:
                    out.write_bytes(urllib.request.urlopen(urllib.request.Request(g["url"], headers=UA), timeout=90).read()); print("ok", k, out.stat().st_size); break
                except Exception as e:
                    print("lỗi tải", k, t, e); time.sleep(5 * (t + 1))
        page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(g["title"].replace(" ", "_"), safe=":(),_")
        nguon[k] = {"slot": v.get("slot"), "so": v.get("so"), "url": g["url"],
                    "credit": f"\"{g['title'][5:]}\" – {g['tac_gia'] or 'không rõ tác giả'}, {g['giay_phep'] or 'không rõ giấy phép'} ({page})"}
    (d / "nguon.json").write_text(json.dumps(nguon, ensure_ascii=False, indent=1), encoding="utf-8")
