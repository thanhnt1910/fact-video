# Mẫu kịch bản kể sự kiện (tập 1 'Chín quận')

> Chuyển nguyên văn từ CLAUDE.md. Nguồn: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`. Chuyển ngày 18/11/2026.

## Mẫu kịch bản cho các video sau (chủ kênh chọn bản của mình làm ví dụ, 05/11/2026)
Mẫu: `ke-hoach/thu-giong-hai/han1_full.json` (tập 1 "Chín quận", bản chủ kênh viết). Các tập sau viết theo cùng kiểu:
- **Mở bằng câu hỏi "Bạn có biết, …?"** gắn tên vùng đất hoặc người, nói rõ ngay bối cảnh (ví dụ "vùng đất Nam Việt cũ").
- **Giọng kể trang trọng, liền mạch**, mỗi đoạn một ý lớn, các đoạn nối nhau bằng quan hệ nguyên nhân – kết quả hoặc đối lập ("Trong khi", "Chính sự…", "Nhưng liệu…").
- **Nêu nguồn ngay trong lời kể ở đoạn 3** ("Theo Đại Việt sử ký toàn thư, …") và có thể dùng "sử sách ghi lại", "theo lời chép trong sử" khi cần.
- **Năm viết bằng chữ trong trường `text` (để đọc giọng), kèm trường `hien` viết bằng số để làm phụ đề** (ví dụ `text`: "Năm một trăm mười trước Công nguyên", `hien`: "Năm 110 trước Công nguyên"). Phụ đề lấy `hien`, giọng đọc lấy `text`.
- **Trích lời dân bằng ngoặc kép**, giữ ý của nguồn, ghi rõ mức chắc chắn.
- **Câu tổng kết ở đoạn gần cuối** ("Câu chuyện cho thấy, cùng một bộ máy cai trị, …") rồi **câu hỏi mở đầu bằng "Nhưng liệu…" hoặc "Vậy vì sao…"** ở đoạn cuối.
- **Vẫn kiểm dữ kiện cứng** (năm, chức, số) theo mục 9; năm lấy theo Toàn thư (110 trước Công nguyên, không đổi sang 111).
- Mỗi đoạn tối đa 32 chữ để giọng không bỏ chữ; đoạn dài hơn thì chấp nhận khi chủ kênh đã duyệt nguyên văn (tập 1: 41007 và 41011 dài 37 chữ) và phải kiểm nhận dạng kỹ.

## Mẫu kịch bản mới nhất: bản chủ kênh viết cho tập 1 "Chín quận" (chủ kênh yêu cầu 06/11/2026: các kịch bản sau áp dụng cùng bố cục và câu văn)
Mẫu: `ke-hoach/thu-giong-hai/han1v4_full.json` (thay `han1_full.json` làm mẫu chính; kịch bản AI viết trước đó bị chủ kênh chê là "quá không logic").
- **Mở đầu (đoạn 1):** một câu hỏi "Bạn có biết, …?" nêu thẳng điều lớn nhất của cả video và phạm vi của nó (ví dụ "nhà Hán chia vùng đất này thành chín quận … từ Bắc Việt Nam ngày nay đến tận đảo Hải Nam"). Không đặt câu hỏi mà không cho biết điều gì.
- **Trình tự kể:** mốc thời gian có năm (đoạn 2) → nêu nguồn "Theo Đại Việt sử ký toàn thư, …" (đoạn 3) → cho biết mỗi phần nằm ở đâu theo địa danh ngày nay (đoạn 4: ba quận trên đất Việt Nam, bốn quận vùng Lĩnh Nam, hai quận trên đảo Hải Nam) → nguyên nhân và tổ chức cai quản → từng nhân vật theo đúng thứ tự thời gian → tổng kết bằng số năm → câu dẫn sang nhân vật tiếp theo.
- **Câu văn:** mỗi đoạn một ý, nối nhau bằng quan hệ nguyên nhân – kết quả ("Kinh đô nhà Hán ở rất xa, nên triều đình phải cử quan lại…"), giải thích chức vụ ngay trong câu ("Đứng đầu bộ là Thứ sử, bên dưới là các Thái thú cai quản từng quận"), ghi đủ họ tên lần đầu, nêu mốc năm cho từng bước. Không viết rời rạc kiểu liệt kê sự kiện không nối nhau.
- **Kết:** câu "Nhưng câu chuyện chưa dừng ở đó. Cũng trong thời kỳ này, …" giới thiệu nhân vật kế, rồi đúng một câu hỏi mở về điều người xem sẽ thấy ở tập sau ("Ông đã làm điều gì khiến …?").
- **Kiểm dữ kiện bằng nguồn gốc, không bỏ chi tiết khi chưa tra:** tra Toàn thư (bản chữ Hán tại zh.wikisource.org nếu truy cập được), Cương mục (bản dịch ở sites.google.com/hawaii.edu/viettexts, KĐVSTGCM quyển 2 có Thạch Đái, Đặng Nhượng, Tích Quang, Nhâm Diên), Hán thư và Hậu Hán thư. Chi tiết tra được thì giữ; chỉ sửa chữ khi nguồn nói khác (ví dụ bộ Giao Chỉ lập từ năm 110 trước Công nguyên chứ không phải 106).
- Đoạn dài 35–41 chữ của mẫu được chủ kênh duyệt nguyên văn, nhưng vẫn nên tách ở dấu câu cho giọng đọc (đoạn dài là nguyên nhân Gemini bỏ chữ).
