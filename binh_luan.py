"""
Bình luận của chủ kênh (kế hoạch, mục "💬 Bình luận của chủ kênh").

Kịch bản ghi sẵn ở trường "binh_luan":
  "binh_luan": {
    "ngan": {"ghim": "bình luận để ghim", "phu": ["bình luận phụ 1", "bình luận phụ 2"]},
    "dai":  {"ghim": "...", "phu": ["..."]}
  }
Thiếu thì máy tự soạn bản đơn giản từ dữ liệu có sẵn trong kịch bản (không gọi AI, không bịa chi tiết mới).

Trả về các dòng văn bản, mỗi bình luận là một mục "════ … ════" riêng để tg_text.py gửi thành khối copy được.
"""

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
    if part == "dai":
        L = script.get("long", {})
        ghim = (L.get("description") or script.get("caption", "")).strip()
        ghim = (ghim + "\n\n" if ghim else "") + "Theo bạn, chi tiết nào trong chuyện này khó tin nhất? Bình luận cho Người Gác Sử biết nhé 🏮"
    else:
        ghim = "Bạn đã từng nghe chuyện này chưa? Theo bạn chi tiết nào khó tin nhất? Bình luận cho Người Gác Sử biết nhé 🏮"
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


def lines(script, part):
    c, given = comments(script, part)
    out = ["", "════ BÌNH LUẬN GHIM CỦA CHỦ KÊNH (đăng ngay, rồi ghim) ════", c["ghim"]]
    for k, p in enumerate(c["phu"][:2], 1):
        out += ["", f"════ BÌNH LUẬN PHỤ {k} (đăng sau 15–30 phút) ════", p]
    out += ["", "════ CÁCH ĐĂNG BÌNH LUẬN (không đăng) ════", HUONG_DAN]
    if not given:
        out.append("Kịch bản chưa có trường \"binh_luan\" nên đây là bản máy tự soạn đơn giản; nên sửa cho hay hơn trước khi đăng.")
    return out
