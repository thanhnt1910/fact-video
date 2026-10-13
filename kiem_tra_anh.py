"""
KIỂM TRA ẢNH TRƯỚC KHI DỰNG (chạy sau khi tải / vẽ ảnh, trước khi đọc giọng và dựng khung hình).

1. Kỹ thuật (miễn phí): ảnh quá nhỏ, mờ nhòe, vỡ khối JPEG, ảnh gần như một màu, tỉ lệ quá dẹt.
2. Gemini (Flash-Lite, rẻ): ảnh có đúng nội dung lời kể và đúng thời kỳ không; ảnh mô phỏng AI có
   lỗi giải phẫu (tay, mặt), chữ lạ, vật dụng sai thời, watermark; ảnh có nội dung nhạy cảm không.

  check(items, sid, kind, log)   items: [{"src", "texts": [...], "ai": bool, "label": ""}]
  -> {"src": [vấn đề...]} ; ghi logs/anh_<mã>_<kind>_kiemtra.txt và lưới ảnh .jpg đánh số
"""
import json
import os
from pathlib import Path
from urllib.parse import unquote, urlparse

import numpy as np

ROOT = Path(__file__).resolve().parent
STORY = ""   # tên câu chuyện (long_video gán trước khi kiểm tra) để Gemini hiểu ngữ cảnh
LOGS = ROOT / "logs"


def _path(src):
    s = str(src)
    return unquote(urlparse(s).path) if s.startswith("file:") else s


def tech(path, kind):
    """Lỗi kỹ thuật của 1 ảnh. kind: "dai" (khung 16:9) hoặc "ngan" (khung dọc)."""
    import cv2
    from PIL import Image
    out = []
    try:
        im = Image.open(path)
        w, h = im.size
        g = np.asarray(im.convert("L"), np.float32)
    except Exception as e:
        return [("loi", f"không mở được ảnh: {e}")]
    short = min(w, h)
    if short < 540:
        out.append(("loi", f"ảnh quá nhỏ ({w}x{h}), phóng to sẽ vỡ"))
    elif short < 700:
        out.append(("canh_bao", f"ảnh hơi nhỏ ({w}x{h})"))
    if max(w, h) / max(1, short) > 3.2:
        out.append(("canh_bao", f"ảnh quá dẹt ({w}x{h}), dễ bị cắt mất nội dung"))
    # độ nét: phương sai Laplace trên bản thu về 1000 px (để so sánh được giữa các cỡ ảnh)
    k = 1000 / max(w, h)
    small = cv2.resize(g, (max(1, int(w * k)), max(1, int(h * k))), interpolation=cv2.INTER_AREA)
    sharp = float(cv2.Laplacian(small, cv2.CV_32F).var())
    if sharp < 25:
        out.append(("loi", f"ảnh rất mờ / nhòe (độ nét {sharp:.0f})"))
    elif sharp < 60:
        out.append(("canh_bao", f"ảnh hơi mờ (độ nét {sharp:.0f})"))
    # vỡ khối JPEG: chênh lệch ở ranh giới khối 8 px so với trong khối
    if w >= 64 and h >= 64:
        dx = np.abs(np.diff(g, axis=1))
        edge = dx[:, 7::8].mean()
        inner = np.delete(dx, np.s_[7::8], axis=1).mean()
        if inner > 0 and edge / inner > 1.6 and edge > 4:
            out.append(("canh_bao", f"ảnh có dấu hiệu vỡ khối JPEG (tỉ lệ {edge / inner:.1f})"))
    if float(g.std()) < 10:
        out.append(("loi", "ảnh gần như một màu (có thể tải lỗi)"))
    return out


PROMPT = """Bạn kiểm tra ảnh minh họa cho video kể chuyện lịch sử có thật "Người Gác Sử" (chuyện {sid}{story}).
Ảnh này sẽ hiện trên màn hình trong lúc giọng đọc kể những câu sau:
{texts}
{kind_note}
{title_note}
Chỉ dựa vào chính những câu lời kể ở trên để đánh giá, không suy đoán câu chuyện khác.\nHãy soi ảnh và chỉ báo vấn đề có thật:
- Ảnh SAI rõ ràng so với lời kể: sai người (lời kể nói về nhân vật A mà ảnh là người khác được giới thiệu như A),
  sai nơi, sai sự việc, sai thời kỳ (ví dụ vật dụng hiện đại trong cảnh năm 1945), hoặc dễ khiến người xem hiểu sai sự thật.
  Ảnh BỐI CẢNH là chấp nhận được, KHÔNG phải lỗi: phong cảnh nơi xảy ra chuyện, bản đồ, hiện vật hoặc vật dụng cùng loại
  (súng, truyền đơn, tàu...), ảnh tư liệu cùng thời kỳ minh họa không khí chung. Với loại này chỉ báo "canh_bao" nếu thật sự lạc đề.
- Ảnh vỡ, mờ, nhòe, bị cắt mất chủ thể, có viền đen/trắng thừa, có chữ hoặc watermark, logo của trang web.
- Nội dung nhạy cảm: thi thể, máu me, bạo lực rõ, biểu tượng phát xít.
{ai_note}
TRẢ LỜI JSON: {{"van_de": [{{"muc": "loi" hoặc "canh_bao", "mo_ta": "…", "sua": "…"}}], "tom_tat": "một câu"}}
KHÔNG báo lỗi tỉ lệ khung hình (ảnh vuông, dọc...): ảnh sẽ được tự động cắt cho vừa màn hình.
Câu chuyện có thể kéo dài nhiều chục năm: đồ vật, ảnh thuộc bất kỳ năm nào trong khoảng thời gian lời kể nói tới
(ví dụ chiếc đài thập niên 1950-1960 khi lời kể nói về những năm lẩn trốn sau chiến tranh) là ĐÚNG thời kỳ.
"loi" = không nên dùng ảnh này. Ảnh tư liệu cũ thì mờ, ngả màu, có hạt là BÌNH THƯỜNG, không phải lỗi.
Không có vấn đề thì "van_de": []."""

AI_NOTE = """Đây là ẢNH MÔ PHỎNG do AI tạo (không phải ảnh thật). Soi kỹ thêm:
- Lỗi giải phẫu: tay thừa/thiếu ngón, tay chân dị dạng, mặt méo, người dính vào nhau.
- Chữ viết lạ hoặc vô nghĩa trên biển, giấy, quần áo; quân phục, vũ khí, xe cộ sai thời kỳ hoặc sai quốc gia.
- Có khuôn mặt nhìn rõ của nhân vật lịch sử có thật (không được: chỉ vẽ người quay lưng, ở xa, trong bóng tối)."""


def ai_check(path, texts, is_ai, sid, kind, title=""):
    import review
    from PIL import Image
    small = Path(path).with_suffix(".kt.jpg")
    im = Image.open(path).convert("RGB")
    im.thumbnail((1024, 1024))
    im.save(small, quality=88)
    title_note = f"Tên / nguồn của ảnh: {title}" if title else ""
    prompt = PROMPT.format(sid=sid, story=(f": {STORY}" if STORY else ""), texts="\n".join(f"- {t}" for t in texts[:8]), title_note=title_note,
                           kind_note="(video dài, khung ngang 16:9)" if kind == "dai" else "(video ngắn, khung dọc)",
                           ai_note=AI_NOTE if is_ai else "Đây là ảnh tư liệu thật (ảnh chụp, tranh cổ, bản đồ).")
    old = review.STAGE
    review.STAGE = "precheck"
    try:
        r = review.ask([{"text": prompt}, review.img_part(small)], f"anh_{sid}_{kind}",
                       ROOT / "output" / sid / "_review", review.hashlib.sha1(small.read_bytes()).hexdigest())
    finally:
        review.STAGE = old
    return [(("loi" if str(v.get("muc", "")).lower().startswith("loi") else "canh_bao"),
             str(v.get("mo_ta", "")).strip() + (f" → {v.get('sua')}" if v.get("sua") else ""))
            for v in r.get("van_de", []) if isinstance(v, dict) and v.get("mo_ta")]


def sheet(items, res, out):
    from PIL import Image, ImageDraw, ImageFont
    tw, th, cols = 320, 180, 6
    rows = (len(items) + cols - 1) // cols
    S = Image.new("RGB", (cols * (tw + 6), max(1, rows) * (th + 6)), (16, 16, 16))
    d = ImageDraw.Draw(S)
    try:
        f = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
    except Exception:
        f = ImageFont.load_default()
    for k, it in enumerate(items):
        try:
            im = Image.open(_path(it["src"])).convert("RGB")
            im.thumbnail((tw, th))
        except Exception:
            im = Image.new("RGB", (tw, th), (80, 0, 0))
        x, y = (k % cols) * (tw + 6), (k // cols) * (th + 6)
        S.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
        lv = [m for m, _ in res.get(it["src"], [])]
        col = (220, 40, 40) if "loi" in lv else (230, 170, 30) if lv else (40, 170, 70)
        d.rectangle([x, y, x + tw - 1, y + th - 1], outline=col, width=4)
        d.rectangle([x, y, x + 64, y + 24], fill=(0, 0, 0))
        d.text((x + 4, y + 3), f"{k + 1}{' AI' if it.get('ai') else ''}", fill=(255, 220, 120), font=f)
    S.save(out, quality=82)


def check(items, sid, kind, log=print, use_ai=True):
    """Kiểm tra mọi ảnh (mỗi ảnh 1 lần). Trả về {src: [(muc, mo_ta)]}."""
    res = {}
    use_ai = use_ai and __import__("gemini_keys").has_key()
    for k, it in enumerate(items):
        p = _path(it["src"])
        issues = tech(p, kind)
        if it.get("allow_soft"):   # ảnh tư liệu duy nhất (vd tranh gốc của con tàu): mờ chỉ là cảnh báo
            issues = [("canh_bao" if "mờ" in m_ else lv, m_) for lv, m_ in issues]
        if use_ai and not any(m == "loi" for m, _ in issues):
            try:
                issues += ai_check(p, it.get("texts", []), it.get("ai"), sid, kind, it.get("title", ""))
            except Exception as e:
                issues.append(("canh_bao", f"chưa nhờ Gemini soi được: {str(e)[:120]}"))
        res[it["src"]] = issues
    LOGS.mkdir(exist_ok=True)
    lines = [f"KIỂM TRA ẢNH {sid} · {'video dài' if kind == 'dai' else 'video ngắn'} · {len(items)} ảnh "
             f"(số thứ tự khớp lưới ảnh anh_{sid}_{kind}_kiemtra.jpg; viền đỏ = lỗi, vàng = nên xem)"]
    for k, it in enumerate(items):
        iss = res[it["src"]]
        mark = "❌" if any(m == "loi" for m, _ in iss) else "⚠️" if iss else "✅"
        lines.append(f"{mark} {k + 1}{' (ảnh mô phỏng AI)' if it.get('ai') else ''} · {it.get('label') or ''} "
                     f"{Path(p := _path(it['src'])).name}")
        for m, t in iss:
            lines.append(f"     {'❌' if m == 'loi' else '⚠️'} {t}")
    (LOGS / f"anh_{sid}_{kind}_kiemtra.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        sheet(items, res, LOGS / f"anh_{sid}_{kind}_kiemtra.jpg")
    except Exception as e:
        log(f"     (không tạo được lưới ảnh: {e})")
    n_err = sum(1 for v in res.values() if any(m == "loi" for m, _ in v))
    log(f"  🔍 Kiểm tra {len(items)} ảnh: {n_err} ảnh lỗi, "
        f"{sum(1 for v in res.values() if v and not any(m == 'loi' for m, _ in v))} ảnh cần xem")
    return res


if __name__ == "__main__":
    import sys
    its = [{"src": a, "texts": [], "ai": False} for a in sys.argv[1:]]
    print(json.dumps(check(its, "THU", "dai", use_ai=False), ensure_ascii=False, indent=1))
