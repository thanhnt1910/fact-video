# Prompt viết kịch bản (dán vào chat Claude)

Mỗi tuần, copy toàn bộ phần trong khung bên dưới, dán vào chat Claude, sửa dòng **DANH SÁCH HOOK** theo lịch đăng tuần đó. Claude sẽ trả về các file JSON. Lưu từng file vào thư mục `scripts/` với đúng tên file Claude ghi (ví dụ `DV1.json`).

---

```
Bạn là biên kịch cho kênh video ngắn "Hóa Ra Là Vậy" (sự thật thú vị, tiếng Việt, video dọc 40–60 giây).
Hãy viết kịch bản cho các hook dưới đây, mỗi hook là MỘT file JSON riêng, đặt trong khối ```json, phía trên mỗi khối ghi tên file (ví dụ: DV1.json).

DANH SÁCH HOOK:
- DV1 | dong-vat | Bạch tuộc có tới 3 trái tim
- CD-A1 | co-dai | Kim tự tháp không phải do nô lệ xây

YÊU CẦU NỘI DUNG
- Cấu trúc: hook (0–3s) → làm rõ điều khó tin → giải thích (2–3 cảnh) → chi tiết bồi → outro.
- Tổng lời đọc khoảng 110–150 từ (40–60 giây). Câu ngắn, dễ nghe, văn nói tự nhiên.
- GIỌNG ĐỌC PHẢI CÓ ĐIỂM NHẤN, viết "voice" như người dẫn chuyện đang hào hứng kể:
  + Dùng "…" ngay trước chi tiết bất ngờ để tạo khoảng ngừng hồi hộp: "Bạch tuộc có tới… ba trái tim!"
  + Dùng "!" cho câu gây bất ngờ, "?" cho câu hỏi gợi tò mò: "Vậy tại sao… lại cần tới ba?"
  + Chèn từ dẫn dắt cảm xúc: "Bạn có biết không?", "Chưa hết đâu!", "Và điều kỳ lạ nhất:", "Nhưng khoan đã…"
  + Tóm tắt cuối dùng câu cực ngắn, tách bằng dấu chấm: "Ba trái tim. Máu xanh. Và… ghét bơi!"
  + Mỗi câu tối đa khoảng 15 từ.
- Viết số trong "voice" bằng chữ để giọng AI đọc đúng (ba trái tim, mười một nghìn sáu trăm năm). Trên màn hình ("text", "value"...) thì dùng chữ số.
- Chỉ dùng sự thật có nguồn uy tín. Con số không chắc chắn thì thêm "khoảng", điều còn tranh luận thì nói "các nhà khoa học cho rằng".
- "sources": liệt kê 1–3 nguồn uy tín thật (tên tổ chức + tên bài/mục). Không bịa đường link.
- Cảnh outro: "recap" tóm tắt 2–3 ý, "next" là câu hook của tập sau (nếu biết), voice kết thúc bằng câu "Hóa ra là vậy!".
- Emoji dùng emoji phổ biến từ trước 2020 (tránh emoji mới như 🫧 🫀 🪸 — Windows sẽ hiện ô vuông).
- Bọc chữ cần tô màu nổi bật bằng **hai dấu sao**.

ĐỊNH DẠNG JSON
{
  "id": "DV1",                      // mã hook, không dấu
  "topic": "dong-vat",              // dong-vat | con-nguoi | thien-nhien | vu-tru | thuc-vat | lich-su | co-dai
  "title": "Bạch tuộc có tới 3 trái tim",
  "caption": "Caption đăng mạng xã hội, 1–2 câu, có emoji",
  "hashtags": ["sựthậtthúvị", "hóaralàvậy", "..."],
  "sources": ["...", "..."],
  "scenes": [ ...các cảnh... ]
}

CÁC LOẠI CẢNH (mỗi cảnh BẮT BUỘC có "type" và "voice")
1. hook      : { "type":"hook", "icon":"🐙", "text":"Bạch tuộc có tới **3 trái tim**", "voice":"..." }   (cảnh đầu tiên)
2. compare   : { "type":"compare", "title":"...", "left":{"icon":"🧍","label":"Con người","value":"1 tim"}, "right":{"icon":"🐙","label":"Bạch tuộc","value":"3 tim"}, "winner":"right", "voice":"..." }
3. explain   : { "type":"explain", "icon":"❤️", "title":"...", "bullets":[{"icon":"💧","text":"..."},{"icon":"🫧","text":"..."}], "voice":"..." }   (tối đa 3 bullet, mỗi bullet ≤ 8 từ)
4. number    : { "type":"number", "pre":"...", "value":"11.600", "unit":"năm", "caption":"...", "voice":"..." }
5. timeline  : { "type":"timeline", "title":"...", "items":[{"year":"~2.560 TCN","label":"🔺 Kim tự tháp"}], "voice":"..." }   (tối đa 4 mốc)
6. text      : { "type":"text", "icon":"🤯", "text":"câu khẳng định ngắn", "sub":"câu phụ", "voice":"..." }
7. outro     : { "type":"outro", "recap":"ý 1 · ý 2 · ý 3", "next":"hook tập sau", "voice":"... Hóa ra là vậy! ..." }   (cảnh cuối)

JSON phải hợp lệ: không có dòng chú thích //, không có dấu phẩy thừa.
Mỗi video 5–7 cảnh. Chữ trên màn hình phải ngắn gọn (text ≤ 10 từ), phần chi tiết để trong voice.
```

---

## Mã chủ đề

| Chủ đề | topic |
|---|---|
| 🐾 Động vật | `dong-vat` |
| 🧠 Con người & Cơ thể | `con-nguoi` |
| 🌍 Thiên nhiên & Trái Đất | `thien-nhien` |
| 🪐 Vũ trụ | `vu-tru` |
| 🍌 Thực vật & Đồ ăn | `thuc-vat` |
| 🏛️ Lịch sử | `lich-su` |
| 🏺 Thế giới cổ đại | `co-dai` |

Mã hook có dấu trong kế hoạch (ĐV1, CĐ-A1…) thì đổi sang không dấu khi đặt `id`: ĐV1 → `DV1`, CĐ-A1 → `CD-A1`, NG1, TN1, VT1, TA1, LS1 giữ nguyên.
