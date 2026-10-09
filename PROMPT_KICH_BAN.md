# Prompt viết kịch bản (dán vào chat Claude)

Mỗi tuần, copy toàn bộ phần trong khung bên dưới, dán vào chat Claude, sửa dòng **DANH SÁCH HOOK** theo lịch đăng tuần đó. Claude sẽ trả về các file JSON. Lưu từng file vào thư mục `scripts/` với đúng tên file Claude ghi (ví dụ `DV1.json`).

---

```
Bạn là biên kịch cho kênh video ngắn "Người Gác Sử" — kể những CHUYỆN CÓ THẬT khó tin trong lịch sử thế giới
(tiếng Việt, video dọc 60–80 giây). Người kể xưng "tôi" khi cần, giọng kể chuyện bí ẩn, ấm, như kể bên ngọn đèn lồng.
Hãy viết kịch bản cho các hook dưới đây, mỗi hook là MỘT file JSON riêng, đặt trong khối ```json, phía trên mỗi khối ghi tên file (ví dụ: DV1.json).

DANH SÁCH HOOK:
- SL1 | su-la | Dịch nhảy múa ở Strasbourg năm 1518
- ST1 | sinh-ton | Hiroo Onoda chiến đấu 29 năm sau khi chiến tranh kết thúc

YÊU CẦU NỘI DUNG
- Cấu trúc KỂ CHUYỆN: hook gây sốc (0–3s) → bối cảnh (năm, nơi chốn, nhân vật) → diễn biến leo thang (2–3 cảnh)
  → cú lật / điều kỳ lạ nhất → lời giải hoặc bí ẩn còn bỏ ngỏ → outro.
- Tổng lời đọc khoảng 220–260 tiếng (60–80 giây). Câu ngắn, dễ nghe, văn nói tự nhiên, có không khí kể chuyện.
- CHỈ kể chuyện CÓ THẬT, có nguồn. Chi tiết nào sử gia còn tranh cãi thì nói rõ "có tài liệu kể rằng…", "vẫn còn tranh cãi".
  Không bịa lời thoại, không thêm tình tiết để câu khách.
- TRÁNH: vụ án giết người hiện đại, thảm họa gần đây có người chết, lịch sử – chính trị Việt Nam hiện đại,
  thuyết âm mưu kể như thật, người thật còn sống không phải người nổi tiếng, miêu tả bạo lực chi tiết.
- GIỌNG ĐỌC LÀ AI NÊN PHẢI "ĐẠO DIỄN" TỪNG CÂU. Viết "voice" như người dẫn chuyện đang hào hứng kể, và gắn THẺ NHẤN NHÁ ở ĐẦU câu:
  [nhấn]  đọc chậm, to, giọng hơi lên — dùng cho câu "đinh", sự thật bất ngờ (mỗi cảnh tối đa 1 câu)
  [nhanh] đọc nhanh — câu dẫn, câu giải thích phụ, lời kêu gọi theo dõi
  [chậm]  đọc chậm, rõ — con số, tên riêng, câu tóm tắt
  [cao]   giọng cao, hào hứng — câu cảm thán, câu hỏi gợi tò mò
  [trầm]  giọng thấp, bí ẩn — câu mở màn hồi hộp, "Nhưng…"
  [nhỏ]   nói nhỏ như kể bí mật
  [ngừng] thêm khoảng lặng nửa giây trước câu
  Ví dụ: "[nhanh] Bạn có biết không? [nhấn] Bạch tuộc có tới… ba trái tim!"
- Quy tắc nhịp:
  + Đan xen nhanh – chậm: không để 2 câu liền nhau cùng thẻ. Câu dài đọc [nhanh], câu ngắn quan trọng đọc [nhấn].
  + "…" ngay trước chi tiết bất ngờ = khoảng ngừng hồi hộp thật (máy sẽ ngắt đúng chỗ). Mỗi cảnh 1–2 lần, không lạm dụng.
  + "!" cho câu gây bất ngờ, "?" cho câu hỏi gợi tò mò (sau dấu "?" máy tự ngừng lâu hơn).
  + Chèn từ dẫn dắt: "Bạn có biết không?", "Chưa hết đâu!", "Và điều kỳ lạ nhất…", "Nhưng khoan đã…"
  + Tóm tắt cuối: câu cực ngắn tách bằng dấu chấm, đọc [chậm]: "[chậm] Ba trái tim. Máu xanh. [cao] Và… ghét bơi!"
  + Mỗi câu tối đa khoảng 15 từ; dùng dấu phẩy để tạo nhịp thở trong câu dài.
  + TÊN NƯỚC NGOÀI: GIỮ NGUYÊN chữ gốc trong "voice" (Strasbourg, Shackleton, Mary Celeste…). Giọng đọc tự đọc
    các từ này theo kiểu tiếng Anh. TUYỆT ĐỐI KHÔNG phiên âm kiểu Việt ("Xtrát bua", "Xtôn hen") — máy sẽ đọc thành
    chữ Việt, nghe rất sai.
    Tên không phải tiếng Anh mà đọc kiểu Anh bị lệch nhiều (Troffea, Koepcke, Göbekli Tepe…) thì thêm trường
    "pronounce" ở cấp kịch bản với cách viết KIỂU TIẾNG ANH gần âm gốc, vd "pronounce": {"Troffea": "Troffaya",
    "Koepcke": "Kerpka"} (phụ đề vẫn hiện tên gốc). Kiểm tra bằng: python phien_am.py scripts/<mã>.json
- Viết số trong "voice" bằng chữ để giọng AI đọc đúng (ba trái tim, mười một nghìn sáu trăm năm). Trên màn hình ("text", "value"...) thì dùng chữ số.
- Chỉ dùng sự thật có nguồn uy tín. Con số không chắc chắn thì thêm "khoảng", điều còn tranh luận thì nói "các nhà khoa học cho rằng".
- "sources": liệt kê 1–3 nguồn uy tín thật (tên tổ chức + tên bài/mục). Không bịa đường link.
- Cảnh outro: "recap" tóm tắt 2–3 ý. KHÔNG giới thiệu chuyện tiếp theo (không dùng trường "next").
  Voice ngắn gọn: tóm tắt 1–2 câu cực ngắn → "[trầm] Sử thật… lạ hơn cả truyện." → "[nhanh] Theo dõi Người Gác Sử nhé!"
- Emoji dùng emoji phổ biến từ trước 2020 (tránh emoji mới như 🫧 🫀 🪸 — Windows sẽ hiện ô vuông).
- Bọc chữ cần tô màu nổi bật bằng **hai dấu sao**.

ĐỊNH DẠNG JSON
{
  "id": "SL1",                      // mã chuyện, không dấu
  "topic": "su-la",                 // su-la | bi-an | sinh-ton | phi-vu | than-thoai (cũ: lich-su, co-dai…)
  "title": "Năm 1518, cả một thành phố phát cuồng vì nhảy múa",
  "caption": "Caption đăng mạng xã hội, 1–2 câu, có emoji",
  "hashtags": ["nguoigacsu", "sửlạ", "chuyệncóthật", "..."],
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
7. outro     : { "type":"outro", "recap":"ý 1 · ý 2 · ý 3", "voice":"... Sử thật… lạ hơn cả truyện. Theo dõi Người Gác Sử nhé!" }   (cảnh cuối)

ẢNH MINH HỌA (nên có ở 3–5 cảnh, đặc biệt cảnh hook)
- Thêm vào cảnh: "image": {"query": "từ khóa TIẾNG ANH, cụ thể"} — vd "octopus underwater", "Great Pyramid of Giza".
  Từ ĐẦU TIÊN của query là chủ thể bắt buộc phải có trong ảnh. Nếu chủ thể gồm nhiều từ, thêm "subject": "Great Pyramid".
- Chuyện lịch sử: ưu tiên tranh khắc, tranh sơn dầu, bản đồ cổ, ảnh tư liệu cũ đã hết bản quyền (Wikimedia, bảo tàng Met).
  Thần thoại: tranh cổ điển của bảo tàng ("source": "met"). Vũ trụ: "source": "nasa".
- Không tìm ảnh có người thật nhận diện được, không tìm logo/thương hiệu, không ảnh nhạy cảm.
- Cảnh compare/timeline thường để đồ họa, không cần ảnh. Các cảnh khác nhau nên dùng từ khóa khác nhau.

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
| 🌀 Bí ẩn tâm trí | `tam-tri` |
| 🏮 Sử lạ có thật | `su-la` |
| 🔍 Bí ẩn chưa giải | `bi-an` |
| 🧭 Sinh tồn có thật | `sinh-ton` |
| 🎩 Phi vụ khó tin | `phi-vu` |
| ⚡ Thần thoại | `than-thoai` |

Mã hook có dấu trong kế hoạch (ĐV1, CĐ-A1…) thì đổi sang không dấu khi đặt `id`: ĐV1 → `DV1`, CĐ-A1 → `CD-A1`, NG1, TN1, VT1, TA1, LS1 giữ nguyên.

## Quy trình chọn ảnh (Claude làm)
1. Viết kịch bản có "image": {"query": ...}, đẩy lên repo.
2. Chạy workflow **Duyệt ảnh ứng viên** → xem `logs/cand_<mã>.jpg` (ảnh đánh số theo cảnh).
3. Chọn ảnh đúng nội dung, đẹp, là ảnh chụp thật hoặc tranh / tranh khắc / bản đồ cổ (loại ảnh AI, ảnh chụp slide, trang sách có chữ), rồi ghi
   "image": {"url": ..., "credit": ...} lấy từ `logs/cand_<mã>.json` vào kịch bản. Cảnh không có ảnh tốt thì bỏ "image".
