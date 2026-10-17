"""
Bình luận của chủ kênh (kế hoạch, mục "💬 Bình luận của chủ kênh").

Kịch bản ghi sẵn ở trường "binh_luan":
  "binh_luan": {
    "ngan": {"ghim": "bình luận để ghim", "phu": ["bình luận phụ 1", "bình luận phụ 2"]},
    "dai":  {"ghim": "...", "phu": ["..."]}
  }
Thiếu thì máy tự soạn bản đơn giản từ dữ liệu có sẵn trong kịch bản (không gọi AI, không bịa chi tiết mới).

Nguồn có link (trường "nguon_link" ở cấp kịch bản) -> thêm 1 bình luận "📚 Nguồn tham khảo" kèm link:
  "nguon_link": [{"ten": "Nghiên cứu lở tuyết (Gaume & Puzrin, 2021)", "url": "https://...", "ngon_ngu": "tiếng Anh"}]
Máy kiểm tra từng link mở được (HTTP < 400) trước khi đưa vào; link hỏng / rút gọn / không phải https bị bỏ.

Trả về các dòng văn bản, mỗi bình luận là một mục "════ … ════" riêng để tg_text.py gửi thành khối copy được.
"""
import urllib.parse
import urllib.request

RUT_GON = ("bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "buff.ly", "cutt.ly", "shorturl.at", "rebrand.ly")
_CHECKED = {}

HUONG_DAN = ("Đăng bình luận ghim trong 5–15 phút đầu rồi ghim lại; bình luận phụ đăng sau 15–30 phút "
             "(hoặc gộp làm một). Trả lời bình luận người xem trong 1–2 giờ đầu. "
             "Không dùng tài khoản phụ / clone để bình luận.")


def _sources(script, n=2):
    names = []
    for s in script.get("sources", [])[:n]:
        s = str(s).split(":")[0].strip()          # bỏ phần ghi chú sau dấu ":"
        if s:
            names.append(s)
    return names


def _fallback(script, part):
    """Bản máy tự soạn: giải thích ngắn nội dung video từ dữ liệu có sẵn, không đặt câu hỏi."""
    if part == "dai":
        L = script.get("long", {})
        ghim = (L.get("description") or script.get("caption", "")).strip()
    else:
        ghim = (script.get("caption") or "").strip()
    phu = []
    src = _sources(script)
    if src:
        phu.append("📚 Nguồn tham khảo: " + "; ".join(src) + ".")
    return {"ghim": ghim, "phu": phu}


def comments(script, part):
    """part: 'ngan' hoặc 'dai'. Trả về (dict, có_sẵn_trong_kịch_bản)."""
    bl = (script.get("binh_luan") or {}).get(part) or {}
    if bl.get("ghim"):
        return {"ghim": bl["ghim"].strip(), "phu": [p.strip() for p in bl.get("phu", []) if p and p.strip()]}, True
    return _fallback(script, part), False


def _link_ok(url):
    """Link dùng được: https, không phải link rút gọn, mở được (HTTP < 400). Lưu kết quả để không kiểm tra lại."""
    if url in _CHECKED:
        return _CHECKED[url]
    ok, why = True, ""
    u = urllib.parse.urlparse(url or "")
    host = (u.netloc or "").lower().removeprefix("www.")
    if u.scheme != "https" or not host:
        ok, why = False, "không phải link https"
    elif host in RUT_GON:
        ok, why = False, "link rút gọn"
    else:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (fact-video link check)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                ok = r.status < 400
                why = "" if ok else f"HTTP {r.status}"
        except Exception as e:
            code = getattr(e, "code", None)
            # một số trang chặn máy kiểm tra (403/429) dù người xem vẫn mở được: vẫn giữ nhưng ghi chú
            if code in (403, 429):
                ok, why = True, f"HTTP {code}: trang chặn máy kiểm tra, nên tự bấm thử"
            else:
                ok, why = False, f"không mở được ({code or type(e).__name__})"
    _CHECKED[url] = (ok, why)
    return ok, why


def source_links(script):
    """Trả về (danh sách nguồn dùng được [(tên, url, ngôn ngữ, ghi chú)], danh sách bị bỏ [(tên, url, lý do)])."""
    good, bad = [], []
    for x in script.get("nguon_link") or []:
        ten, url = (x.get("ten") or "").strip(), (x.get("url") or "").strip()
        if not ten or not url:
            continue
        ok, why = _link_ok(url)
        (good if ok else bad).append((ten, url, x.get("ngon_ngu", ""), why) if ok else (ten, url, why))
    return good[:3], bad


def link_comment(script):
    good, bad = source_links(script)
    if not good:
        return None, bad
    langs = {g[2] for g in good if g[2]}
    head = "📚 Nguồn tham khảo" + (f" ({', '.join(sorted(langs))})" if langs else "") + ":"
    body = [head] + [f"• {t}: {u}" for t, u, _, _ in good]
    return "\n".join(body), bad


def lines(script, part):
    c, given = comments(script, part)
    out = ["", "════ BÌNH LUẬN GHIM CỦA CHỦ KÊNH (đăng ngay, rồi ghim) ════", c["ghim"]]
    for k, p in enumerate(c["phu"][:2], 1):
        out += ["", f"════ BÌNH LUẬN PHỤ {k} (đăng sau 15–30 phút) ════", p]
    lc, bad = link_comment(script)
    if lc:
        out += ["", "════ BÌNH LUẬN NGUỒN THAM KHẢO CÓ LINK (Facebook / YouTube; không ghim, đăng sau 15–30 phút) ════", lc]
    out += ["", "════ CÁCH ĐĂNG BÌNH LUẬN (không đăng) ════", HUONG_DAN,
            "Link chỉ để trong bình luận, không để trong caption. TikTok không bấm được link trong bình luận: chỉ ghi tên nguồn."]
    for t, u, why in bad:
        out.append(f"⚠️ Đã bỏ link nguồn \"{t}\" ({u}): {why}")
    if lc:
        for t, u, _, why in source_links(script)[0]:
            if why:
                out.append(f"ℹ️ {t}: {why}")
    if not given:
        out.append("Kịch bản chưa có trường \"binh_luan\" nên đây là bản máy tự soạn đơn giản; nên sửa cho hay hơn trước khi đăng.")
    return out
