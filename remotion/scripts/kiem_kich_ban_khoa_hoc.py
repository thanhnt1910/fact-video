#!/usr/bin/env python3
"""Kiểm kịch bản video khoa học (kênh Người Giải Mã) theo quy tắc chủ kênh đã chốt.

Dùng: python3 remotion/scripts/kiem_kich_ban_khoa_hoc.py ke-hoach/khoa-hoc-video-N-...-kich-ban.md
Mã thoát 0 = không có ❌. Có ❌ thì không gửi kịch bản cho chủ kênh, sửa rồi chạy lại.
Công cụ kiểm phần máy kiểm được; phần nguồn gốc và độ dễ hiểu vẫn phải tự soát (xem skill viet-kich-ban-khoa-hoc).
"""
import re
import sys

WPS = 3.7          # chữ mỗi giây của giọng Leda (đo trên video 2 và 3: 3,68–3,71)
PAD = 0.5          # mỗi câu thêm 0,5 giây, tối thiểu 2,4 giây (content.ts)
BAD_PHRASES = [
    (r"sức hút", "dùng 'lực hút', không dùng 'sức hút'"),
    (r"tập sau|video sau|xem tiếp|video tiếp|kỳ sau|phần sau", "không có 'tập sau' hay lời dẫn sang video khác"),
    (r"video trước|ở video|tập trước|như đã kể", "mỗi video trọn gói, không nhắc video khác"),
    (r"đăng ký kênh|nhớ bấm|like và|chia sẻ video", "không kêu gọi bấm nút trong lời kể"),
]
ABSTRACT = ["độ cong", "bản chất", "khái niệm", "trừu tượng", "về mặt lý thuyết", "mô hình toán", "phương trình vi phân"]
FORBID_FILE = [r"\[SỬ\*\]", r"phải kiểm", r"TBD", r"chưa kiểm", r"CHƯA ĐỐI CHIẾU"]


# ---- Quy tắc mở đầu (chủ kênh, 10/11/2026, từ phân tích dữ liệu một kênh) ----
OPEN_WIN = 25.0     # giây đầu: tối đa MỘT mốc năm hoặc tên sách
SRC_WIN = 30.0      # nguồn sử chỉ được xuất hiện sau giây này
MAX_NAMES = 2       # ngưỡng tên riêng trong cửa sổ đầu (giả định của Claude, chủ kênh chưa nêu số)
YEAR_RE = re.compile(r"(?<![\d.,])(1\d{3}|20\d{2})(?![\d,.]?\d)(?!\s\d{3})|\b\d{1,4}\s*(?:TCN|SCN)\b")
CITE_RE = re.compile(r"\b(theo\s+(?:sách|chép|ghi|lời|nguồn|tài liệu|sử)|sách\s+\w+|sử\s+(?:chép|ghi|sách)|ghi\s+(?:lại|chép)|chép\s+rằng|nguồn\s+(?:tin|sử|tài)|tài\s+liệu|biên\s+niên|nhà\s+sử|sử\s+gia|bài\s+báo|công\s+bố|bản\s+dịch|nguyên\s+văn)\b", re.I)
COMMON = ["Mặt Trời", "Trái Đất", "Mặt Trăng", "Việt Nam", "Đan Mạch", "Anh", "Pháp", "Mộc", "Kim", "Hỏa", "Thủy", "Thổ"]
TURN_RE = re.compile(r"\b(nhưng|vậy mà|thế mà|hóa ra|bất ngờ|không ngờ|điều lạ|vì sao|làm sao|bằng cách nào|câu hỏi|lời giải|bí mật|bí quyết|chỉ cần|sẽ thấy|sắp|cho đến|cho tới|mà là|không phải)\b", re.I)


def proper_names(cap):
    plain = cap.replace("*", "")
    for w in COMMON:
        plain = plain.replace(w, " ")
    names, cur = [], []
    # tách theo câu nhỏ để bỏ chữ hoa đầu câu
    for part in re.split(r"(?<=[.?!:])\s+|^", plain):
        toks = part.split()
        for k, t in enumerate(toks):
            t2 = t.strip(",.;:?!()\"'")
            if k > 0 and t2[:1].isupper() and not t2.isupper():
                cur.append(t2)
            else:
                if cur:
                    names.append(" ".join(cur))
                    cur = []
        if cur:
            names.append(" ".join(cur))
            cur = []
    return names


def check_opening(sents, errs, warns):
    """Báo cáo 25 giây đầu: số mốc năm, tên riêng, cụm trích nguồn; câu nào dồn quá nhiều."""
    t = 0.0
    rows = []
    for n, doc, cap in sents:
        words = len(doc.split())
        dur = max(words / WPS + PAD, 2.4)
        rows.append((n, t, dur, cap))
        t += dur
    print("\n25 giây đầu (ước tính theo tốc độ giọng):")
    total_years, total_names = [], []
    for n, st, dur, cap in rows:
        if st >= SRC_WIN:
            break
        plain = cap.replace("*", "")
        years = [m.group(0) for m in YEAR_RE.finditer(plain)]
        names = proper_names(cap)
        cites = [m.group(0) for m in CITE_RE.finditer(plain)]
        in_open = st < OPEN_WIN
        tag = "" if in_open else " (giây 25–30)"
        print(f"  câu {n:>2} @{st:4.1f}s{tag}: năm={years or '-'} tên={names or '-'} trích nguồn={cites or '-'}")
        if in_open:
            total_years += years
            total_names += names
            if len(years) + len(names) >= 3:
                warns.append(f"Câu {n} (giây {st:.0f}): dồn {len(years)} mốc năm và {len(names)} tên riêng trong một câu; tách hoặc bỏ bớt")
        if cites:
            errs.append(f"Câu {n} (giây {st:.0f}): có cụm trích nguồn {cites} trước giây {SRC_WIN:.0f}; để nguồn sử sau giây {SRC_WIN:.0f} (và nhãn nguồn nằm ở ghi chú, không nằm trong lời kể)")
    if len(total_years) > 1:
        errs.append(f"{OPEN_WIN:.0f} giây đầu có {len(total_years)} mốc năm {total_years}: chỉ được tối đa MỘT mốc năm hoặc tên sách")
    if len(set(total_names)) > MAX_NAMES:
        warns.append(f"{OPEN_WIN:.0f} giây đầu có {len(set(total_names))} tên riêng {sorted(set(total_names))} (ngưỡng đề xuất {MAX_NAMES}); người nghe chưa nhớ nổi")
    # bước ngoặt / lời hứa ngay sau hook (câu 2–4)
    early = [(n, doc + " " + cap) for n, doc, cap in sents[1:4]]
    if early and not any(TURN_RE.search(txt) for _, txt in early):
        warns.append("Ngay sau hook (câu 2–4) chưa thấy bước ngoặt hoặc lời hứa (nhưng / vậy mà / hóa ra / vì sao / không phải ... mà là ...): dễ rơi vào bối cảnh khô")


def main(path):
    txt = open(path, encoding="utf-8").read()
    lines = txt.splitlines()
    errs, warns = [], []
    sents = []
    i = 0
    while i < len(lines):
        m = re.match(r"^(\d+)\.\s*Đọc:\s*(.+)$", lines[i])
        if m:
            n, doc = int(m.group(1)), m.group(2).strip()
            cap = ""
            if i + 1 < len(lines):
                m2 = re.match(r"^\s*Phụ đề:\s*(.+)$", lines[i + 1])
                if m2:
                    cap = m2.group(1).strip()
            sents.append((n, doc, cap))
        i += 1

    if not sents:
        errs.append("Không tìm thấy câu nào theo mẫu '1. Đọc: ...' kèm dòng 'Phụ đề: ...'")
    # đánh số liên tục
    for k, (n, _, _) in enumerate(sents, 1):
        if n != k:
            errs.append(f"Câu số {n} không liên tục (mong đợi {k})")
            break

    total = 0.0
    for n, doc, cap in sents:
        words = len(doc.split())
        total += max(words / WPS + PAD, 2.4)
        if not cap:
            errs.append(f"Câu {n}: thiếu dòng Phụ đề")
        if re.search(r"\d", doc):
            errs.append(f"Câu {n}: dòng Đọc còn chữ số (giọng phải đọc thành chữ)")
        if re.search(r"[%°÷×≈=/]", doc):
            errs.append(f"Câu {n}: dòng Đọc còn ký hiệu (%, °, ÷, ×, ≈, =, /); viết thành chữ")
        if "*" in doc:
            errs.append(f"Câu {n}: dòng Đọc không được có dấu * (chỉ Phụ đề mới tô màu)")
        if re.search(r"[A-Z]{2,}", doc):
            warns.append(f"Câu {n}: dòng Đọc có chữ viết tắt in hoa, cần phiên âm (ví dụ GPS = gi-pi-ét)")
        if re.search(r"[fjwzFJWZøØ]", doc):
            warns.append(f"Câu {n}: dòng Đọc có chữ nước ngoài chưa phiên âm (f, j, w, z, ø)")
        if words > 38:
            warns.append(f"Câu {n}: dòng Đọc dài {words} chữ, nên tách (giọng dễ đọc lệch, người nghe khó theo)")
        for pat, why in BAD_PHRASES:
            if re.search(pat, doc + " " + cap, re.I):
                errs.append(f"Câu {n}: {why}")
        for a in ABSTRACT:
            if a in (doc + cap).lower():
                warns.append(f"Câu {n}: từ trừu tượng '{a}', thay bằng hình ảnh đời thường")
        # phụ đề
        if cap:
            stars = cap.count("*")
            if stars % 2 or stars == 0:
                errs.append(f"Câu {n}: Phụ đề thiếu hoặc lệch dấu *...* (từ khóa phải tô màu)")
            plain = cap.replace("*", "")
            if re.search(r"\b(mươi|chục)\b", plain) or re.search(r"(?<!phần )\btrăm\b", plain):
                errs.append(f"Câu {n}: Phụ đề viết số bằng chữ (mươi/trăm/chục), phải là chữ số")
            tmp = re.sub(r"phần (nghìn|triệu|tỉ)", "", plain)
            if re.search(r"\b(nghìn|triệu|tỉ)\b", tmp) and not re.search(r"\d\s*(nghìn|triệu|tỉ)", tmp):
                warns.append(f"Câu {n}: Phụ đề có 'nghìn/triệu/tỉ' không đi cùng chữ số")

    # công thức thật
    if sents and not any(re.search(r"[÷×]|\d\s*=\s*\d|=\s*\*?\d", cap) for _, _, cap in sents):
        errs.append("Không có công thức thật trong Phụ đề (÷, ×, =): video phải có phép tính ra kết quả")

    # hook
    if sents:
        n, doc, _ = sents[0]
        if len(doc.split()) > 38:
            warns.append("Câu 1 (hook) quá dài; hook phải ngắn và gây tò mò ngay")
        if "?" not in " ".join(d for _, d, _ in sents[:3]):
            warns.append("Ba câu đầu không có câu hỏi gợi tò mò; hook nên có câu hỏi hoặc điều đáng ngạc nhiên")

    # cấu trúc file
    for need in ["Trạng thái kiểm chứng", "Chi tiết đã bỏ", "Cần chủ kênh duyệt"]:
        if need not in txt:
            errs.append(f"Thiếu mục '{need}'")
    for pat in FORBID_FILE:
        if re.search(pat, txt):
            errs.append(f"File còn dấu hiệu chưa kiểm nguồn: /{pat}/ (quy tắc 03/11/2026)")
    if not re.search(r"\[(SỬ|CG)\]", txt):
        errs.append("Mục Trạng thái kiểm chứng không có nhãn [SỬ] hoặc [CG] nào: chưa kiểm nguồn")
    # nhãn trong lời kể
    for n, doc, cap in sents:
        if re.search(r"\[(SỬ|CG|TÍNH|MH)", doc + cap):
            errs.append(f"Câu {n}: nhãn độ chắc nằm trong lời kể, phải để ở ghi chú")

    if sents:
        check_opening(sents, errs, warns)

    dur = total
    mm, ss = int(dur // 60), int(dur % 60)
    print(f"{len(sents)} câu, ước tính {mm} phút {ss} giây (giọng Leda {WPS} chữ/giây)")
    if dur > 210:
        warns.append(f"Ước tính {mm}:{ss:02d} dài; video 2 là 2:50, video 3 là 4:30 bị chê dài. Nên cắt bớt")
    for w in warns:
        print("⚠️ ", w)
    for e in errs:
        print("❌", e)
    print("KẾT QUẢ:", "ĐẠT" if not errs else f"CHƯA ĐẠT ({len(errs)} lỗi)")
    return 0 if not errs else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
