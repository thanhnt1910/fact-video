#!/usr/bin/env python3
"""Chặn bản gửi duyệt còn việc kiểm nguồn bị đẩy sang chủ kênh.
Dùng: python phim_ban_do/kiem_gui_duyet.py <file.md> [...]
Mọi dữ kiện cứng phải tra xong (hai nguồn) hoặc BỎ khỏi lời kể trước khi gửi.
Có cụm đẩy việc kiểm cho chủ kênh, hoặc bảng nguồn thiếu, thì thoát mã 1."""
import re, sys
BAN = [r"chưa đối chiếu", r"cần kiểm", r"không tra được.*(nếu anh|anh muốn)",
       r"nếu anh muốn.*(tra|kiểm)", r"anh muốn tôi.*(tra|kiểm)", r"tôi sẽ tra", r"kiểm hộ", r"chờ anh kiểm", r"TBD"]
CAN = ["### Nguồn đã đọc", "### Điểm lệch giữa các nguồn", "### Chi tiết đã bỏ", "### 3 phương án hook", "### Toàn văn lời kể"]
bad = 0
for p in sys.argv[1:]:
    t = open(p, encoding="utf-8").read()
    for i, line in enumerate(t.splitlines(), 1):
        for b in BAN:
            if re.search(b, line, re.I):
                print(f"❌ {p}:{i}: đẩy việc kiểm cho chủ kênh ({b}): {line[:90]}"); bad += 1; break
    parts = t.split("\n## ")
    for blk in parts[1:]:
        ten = blk.splitlines()[0]
        for c in CAN:
            if c not in blk:
                print(f"❌ {p}: '{ten[:40]}' thiếu mục {c}"); bad += 1
        m = re.search(r"### Nguồn đã đọc\n(.*?)\n###", blk, re.S)
        n = len([l for l in (m.group(1).splitlines() if m else []) if l.startswith("- ")])
        if n < 2:
            print(f"❌ {p}: '{ten[:40]}' dưới 2 nguồn"); bad += 1
print("ĐẠT" if not bad else f"{bad} lỗi ❌: sửa hoặc bỏ chi tiết, KHÔNG gửi")
sys.exit(1 if bad else 0)
