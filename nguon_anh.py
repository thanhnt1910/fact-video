"""
BẰNG CHỨNG BẢN QUYỀN HÌNH ẢNH (kế hoạch, mục "✅ Cam kết bản quyền hình ảnh").

Mỗi lần dựng, trước khi vẽ khung hình:
- Gom mọi ảnh trong kịch bản (video ngắn, video dài, bài ảnh).
- Ảnh Wikimedia Commons: hỏi API lấy giấy phép, tác giả, ngày chụp NGAY LÚC TẢI và lưu nguyên văn (bằng chứng,
  vì trang nguồn có thể đổi sau này). Ảnh nguồn khác: lưu nhãn giấy phép ghi ở nguồn.
- Chỉ chấp nhận Public Domain / CC0 (các nhãn PD-...). Có ảnh không hợp lệ -> KHÔNG dựng (RuntimeError).
- Ảnh chụp "Public domain" sau năm 1950 không phải của chính phủ Mỹ -> cảnh báo (luật Việt Nam bảo hộ ảnh 75 năm).
- Tranh AI: lưu prompt, model, ngày tạo.
Ghi: logs/nguon_anh_<mã>.json và sổ tổng logs/so_anh.csv (mỗi ảnh một dòng, tra cứu khi có khiếu nại).
"""
import csv
import datetime as dt
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"
API = "https://commons.wikimedia.org/w/api.php"
UA = "NguoiGacSuVideo/1.0 (https://github.com/thanhnt1910/fact-video; educational history videos)"
OK = re.compile(r"(public domain|^pd\b|^pd-|\bpd-|cc0|cc-zero|no known restrictions|no restrictions)", re.I)
BAD = re.compile(r"\bcc[- ]?by\b|by-sa|by-nc|gfdl|all rights reserved", re.I)
US_GOV = re.compile(r"\b(u\.?s\.?|united states|us army|us navy|navy|army|air force|marine|nasa|noaa|national archives|"
                    r"department|government|library of congress|federal)\b", re.I)
AI_MODEL = "@cf/black-forest-labs/flux-1-schnell (Cloudflare Workers AI)"


def _strip(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h or "")).strip()


def commons_title(spec):
    """Tên trang File:... trên Commons từ credit hoặc đường dẫn ảnh."""
    m = re.search(r"commons\.wikimedia\.org/wiki/(File:\S+)\)\s*$", spec.get("credit", "") or "") or \
        re.search(r"commons\.wikimedia\.org/wiki/(File:[^)\s]+)", spec.get("credit", "") or "")
    if m:
        return urllib.parse.unquote(m.group(1)).replace("_", " ")
    u = spec.get("url", "") or ""
    m = re.search(r"upload\.wikimedia\.org/wikipedia/commons/(?:thumb/)?\w/\w\w/([^/?]+)", u)
    if m:
        return "File:" + urllib.parse.unquote(m.group(1)).replace("_", " ")
    return None


def gather(script):
    out = []
    for i, b in enumerate((script.get("ngan") or {}).get("beats", [])):
        for j, im in enumerate(b.get("images", [])):
            out.append((f"ngắn · cảnh {i + 1} ảnh {j + 1}", im))
    for ci, ch in enumerate((script.get("long") or {}).get("chapters", [])):
        for bi, b in enumerate(ch.get("beats", [])):
            if b.get("image"):
                out.append((f"dài · chương {ci} đoạn {bi + 1}", b["image"]))
            elif b.get("mo_phong"):
                out.append((f"dài · chương {ci} đoạn {bi + 1}", {"mo_phong": b["mo_phong"]}))
    for si, sc in enumerate(script.get("scenes", [])):
        if isinstance(sc.get("image"), dict):
            out.append((f"bài ảnh · cảnh {si + 1}", sc["image"]))
    return out


def _api(titles):
    res = {}
    for k in range(0, len(titles), 40):
        part = titles[k:k + 40]
        q = {"action": "query", "titles": "|".join(part), "prop": "imageinfo", "iiprop": "url|extmetadata|timestamp",
             "iiextmetadatafilter": "LicenseShortName|License|UsageTerms|Copyrighted|Artist|Credit|DateTimeOriginal|"
                                    "ImageDescription|Restrictions|AttributionRequired",
             "format": "json", "formatversion": 2, "redirects": 1}
        url = API + "?" + urllib.parse.urlencode(q)
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=40) as r:
                    data = json.loads(r.read().decode("utf-8"))
                break
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(2 + 3 * attempt)
        norm = {n["to"]: n["from"] for n in (data.get("query", {}).get("normalized") or [])}
        for p in data.get("query", {}).get("pages", []):
            ii = (p.get("imageinfo") or [{}])[0]
            md = {k2: _strip(v.get("value", "")) for k2, v in (ii.get("extmetadata") or {}).items()}
            res[norm.get(p["title"], p["title"])] = {"trang": ii.get("descriptionurl", ""), "missing": p.get("missing", False),
                                                     "metadata": md}
            res[p["title"]] = res[norm.get(p["title"], p["title"])]
        time.sleep(0.5)
    return res


def _year(*texts):
    for t in texts:
        m = re.search(r"\b(1[6-9]\d\d|20\d\d)\b", t or "")
        if m:
            return int(m.group(1))
    return None


def record(script, log=print, strict=True):
    """Ghi bằng chứng giấy phép cho mọi ảnh; strict: có ảnh không hợp lệ thì dừng dựng."""
    sid = script["id"]
    items = gather(script)
    today = dt.date.today().isoformat()
    titles = sorted({t for _, im in items if not im.get("mo_phong") and (t := commons_title(im))})
    try:
        api = _api(titles) if titles else {}
        api_err = None
    except Exception as e:
        api, api_err = {}, str(e)[:200]
    rows, errs, warns = [], [], []
    seen = {}
    for usage, im in items:
        if im.get("mo_phong"):
            key = "AI:" + im["mo_phong"]
            if key in seen:
                seen[key]["dung_o"].append(usage)
                continue
            r = {"loai": "tranh AI", "prompt": im["mo_phong"], "model": AI_MODEL, "ngay_tao": today,
                 "giay_phep": "ảnh do kênh tạo bằng AI từ mô tả chữ (model cho phép dùng thương mại)", "dung_o": [usage]}
            seen[key] = r
            rows.append(r)
            continue
        key = im.get("url", "")
        if key in seen:
            seen[key]["dung_o"].append(usage)
            continue
        title = commons_title(im)
        credit = im.get("credit", "")
        r = {"loai": "ảnh tư liệu", "url": key, "credit": credit, "ngay_tai": today, "dung_o": [usage]}
        if title and title in api and not api[title]["missing"]:
            md = api[title]["metadata"]
            lic = md.get("LicenseShortName", "")
            r.update({"ten_file": title, "trang_nguon": api[title]["trang"], "giay_phep": lic,
                      "tac_gia": md.get("Artist", "")[:200], "ngay_chup": md.get("DateTimeOriginal", "")[:80],
                      "ban_chup_giay_phep": {k2: md.get(k2, "") for k2 in ("LicenseShortName", "License", "UsageTerms",
                                                                            "Copyrighted", "Restrictions",
                                                                            "AttributionRequired", "Credit")},
                      "nguon_giay_phep": "Wikimedia Commons API (extmetadata) lúc dựng"})
        else:
            m = re.search(r",\s*([^,()]+?)\s*\(https?://.*\)\s*$", credit)
            lic = m.group(1).strip() if m else ""
            r.update({"ten_file": title or Path(urllib.parse.urlparse(key).path).name, "giay_phep": lic,
                      "nguon_giay_phep": ("nhãn ghi ở nguồn (không có API)" if not title else
                                          f"nhãn ghi ở nguồn (API Commons lỗi: {api_err})" if api_err else
                                          "nhãn ghi ở nguồn (không tìm thấy trang Commons)")})
        lic = r.get("giay_phep", "")
        if not lic or BAD.search(lic) or not OK.search(lic):
            errs.append(f"{r['ten_file']}: giấy phép '{lic or 'không rõ'}' không phải Public Domain/CC0")
            r["hop_le"] = False
        else:
            r["hop_le"] = True
            year = _year(r.get("ngay_chup", ""), r.get("ten_file", ""), credit)
            r["nam"] = year
            if "cc0" not in lic.lower() and year and year > 1950 and not US_GOV.search(r.get("tac_gia", "") + " " + credit):
                warns.append(f"{r['ten_file']}: ảnh năm {year}, nhãn '{lic}' — ở Việt Nam ảnh chụp chỉ hết bản quyền nếu "
                             f"công bố từ 1950 trở về trước; cần xem lại")
        seen[key] = r
        rows.append(r)
    LOGS.mkdir(exist_ok=True)
    (LOGS / f"nguon_anh_{sid}.json").write_text(json.dumps(
        {"ma": sid, "cap_nhat": dt.datetime.now().isoformat(timespec="seconds"), "anh": rows,
         "loi": errs, "canh_bao": warns}, ensure_ascii=False, indent=1), encoding="utf-8")
    _update_book(sid, rows)
    n_ai = sum(1 for r in rows if r["loai"] == "tranh AI")
    log(f"  ⚖️  Bằng chứng bản quyền: {len(rows) - n_ai} ảnh tư liệu + {n_ai} tranh AI → logs/nguon_anh_{sid}.json"
        + (f" · ⚠️ {len(warns)} cần xem" if warns else ""))
    for w in warns:
        log(f"     ⚠️  {w}")
    if errs:
        for e in errs:
            log(f"     ❌ {e}")
        if strict:
            raise RuntimeError("ảnh không rõ giấy phép / không phải PD-CC0: " + "; ".join(errs[:5]))
    return rows, errs, warns


def _update_book(sid, rows):
    f = LOGS / "so_anh.csv"
    cols = ["ma", "loai", "ten_file", "trang_nguon", "giay_phep", "tac_gia", "nam", "ngay_tai", "dung_o", "prompt"]
    old = []
    if f.exists():
        with f.open(encoding="utf-8", newline="") as fh:
            old = [r for r in csv.DictReader(fh) if r.get("ma") != sid]
    new = [{"ma": sid, "loai": r["loai"], "ten_file": r.get("ten_file", ""),
            "trang_nguon": r.get("trang_nguon", r.get("url", "")), "giay_phep": r.get("giay_phep", ""),
            "tac_gia": r.get("tac_gia", ""), "nam": r.get("nam") or "", "ngay_tai": r.get("ngay_tai", r.get("ngay_tao", "")),
            "dung_o": " | ".join(r["dung_o"]), "prompt": r.get("prompt", "")} for r in rows]
    with f.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in old + new:
            w.writerow({k: r.get(k, "") for k in cols})


if __name__ == "__main__":
    import sys
    for a in sys.argv[1:]:
        record(json.loads(Path(a).read_text(encoding="utf-8")), strict=False)
