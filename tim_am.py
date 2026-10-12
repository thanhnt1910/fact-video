"""
TÌM NHẠC NỀN / TIẾNG ĐỘNG KHÔNG BẢN QUYỀN trên Wikimedia Commons (chỉ nhận Public Domain hoặc CC0).

  python tim_am.py ke-hoach/am/nhac.json

File yêu cầu:  {"id": "nhac", "slots": [{"slot": "M1", "mo_ta": "...", "queries": ["Gymnopedie", ...]}]}
Kết quả: logs/am_tim/<id>.json — mỗi ứng viên: tên file, trang nguồn, giấy phép (chụp từ API), tác giả,
độ dài, link tải (bản mp3 chuyển mã của Commons nếu file gốc là ogg/flac/wav).
Kế hoạch (mục Bản quyền): nhạc cổ điển chỉ dùng BẢN THU có nhãn PD/CC0 (vd Musopen); không dùng CC BY.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "logs" / "am_tim"
API = "https://commons.wikimedia.org/w/api.php"
UA = "NguoiGacSuVideo/1.0 (https://github.com/thanhnt1910/fact-video; educational history videos)"
OK_LICENSE = re.compile(r"^(public domain|pd\b|pd-|cc0|cc-zero|no restrictions)", re.I)


def api(params):
    params = dict(params, format="json", formatversion=2)
    url = API + "?" + urllib.parse.urlencode(params)
    for k in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if k == 3:
                raise
            time.sleep(2 + 3 * k)


def strip(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def search(q, limit=25):
    r = api({"action": "query", "generator": "search", "gsrsearch": f"{q} filetype:audio", "gsrnamespace": 6,
             "gsrlimit": limit, "prop": "imageinfo", "iiprop": "url|extmetadata|mediatype|mime|size",
             "iiextmetadatafilter": "LicenseShortName|License|Artist|Credit|ImageDescription|DateTimeOriginal|UsageTerms"})
    out = []
    for p in (r.get("query") or {}).get("pages", []):
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata") or {}
        lic = strip((md.get("LicenseShortName") or {}).get("value", ""))
        if not OK_LICENSE.search(lic):
            continue
        url = ii.get("url", "")
        mp3 = url
        if not url.lower().endswith(".mp3"):
            # bản chuyển mã mp3 của Commons: /transcoded/<a>/<ab>/<File>/<File>.mp3
            m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons)/(\w)/(\w\w)/(.+)$", url)
            if m:
                mp3 = f"{m.group(1)}/transcoded/{m.group(2)}/{m.group(3)}/{m.group(4)}/{m.group(4)}.mp3"
        out.append({"title": p["title"], "page": ii.get("descriptionurl", ""), "license": lic,
                    "license_raw": {k: strip(v.get("value", "")) for k, v in md.items()},
                    "artist": strip((md.get("Artist") or {}).get("value", ""))[:120],
                    "desc": strip((md.get("ImageDescription") or {}).get("value", ""))[:200],
                    "duration": ii.get("duration") or p.get("duration"), "size": ii.get("size"),
                    "url": url, "mp3": mp3, "mime": ii.get("mime")})
    return out


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    res = []
    for s in spec["slots"]:
        seen, cands = set(), []
        for q in s["queries"]:
            try:
                found = search(q)
            except Exception as e:
                print(f"  ⚠️  {s['slot']} \"{q}\": {e}")
                found = []
            for c in found:
                if c["title"] not in seen:
                    seen.add(c["title"])
                    cands.append(dict(c, query=q))
            time.sleep(0.5)
        print(f"{s['slot']} ({s.get('mo_ta', '')}): {len(cands)} ứng viên PD/CC0", flush=True)
        res.append({"slot": s["slot"], "mo_ta": s.get("mo_ta"), "candidates": cands[:20]})
    (OUT / f"{spec['id']}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
