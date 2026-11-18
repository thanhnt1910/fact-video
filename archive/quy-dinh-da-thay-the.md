# Quy định đã bị thay thế bằng quyết định 18/11/2026

> Sàn 10 phút và câu kết 'tập sau' mặc định đã bỏ; xem quy-tac/dung-mach-truyen.md. Nguồn: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`. Chuyển ngày 18/11/2026.

## Quy định thời lượng (chủ kênh đặt ngày 15/10/2026, áp dụng cho mọi video từ nay)

- Mọi VIDEO DÀI phải dài TỐI THIỂU 10 PHÚT. Đây là mức sàn.
- Lời đọc ít nhất khoảng 1.900 tiếng (giọng Gemini đọc khoảng 3 tiếng/giây), khoảng 70–90 beat, 8–10 chương.
- Thiếu chữ thì thêm chi tiết có nguồn, không độn câu, không lặp ý, không bịa. Chi tiết không chắc thì nói rõ là còn tranh cãi.
- Sau khi dựng, đo thời lượng thật; dưới 10 phút thì bổ sung kịch bản, không đăng.
- Video dọc vẫn 60–80 giây. Quy định này chỉ áp cho video dài.
- Chi tiết đầy đủ: mục "VIDEO DÀI" trong `PROMPT_KICH_BAN.md`.
- `review.py` đã áp mức sàn này: video dài dưới 10 phút báo ⚠️ (vẫn được gửi), dưới 6 phút báo ❌ (không được gửi Telegram).

## Câu kết mời xem tập sau (chủ kênh yêu cầu 06/11/2026, áp dụng loạt "Chuyện cai trị ngàn năm" và mọi video có số tập)
- Sau câu hỏi mở cuối cùng, thêm đúng một đoạn ngắn: "Hẹn bạn ở tập tiếp theo." (khoảng 2 giây, đoạn riêng, không gộp vào câu hỏi). Câu hỏi vẫn là câu gây tò mò mạnh nhất, câu mời chỉ đặt sau nó.
- Cố định một câu cho cả loạt, không đổi chữ giữa các tập. Tập 2 (44016) và tập 3 (45019) đã có.
- Đọc riêng đoạn này (`cum.txt` = 1, giọng Orus, file nhỏ chỉ chứa đoạn mới), ghép vào bản giọng gốc không chỉnh âm thanh, nhận dạng lại, rồi dựng. Cảnh cuối của trang dựng kéo dài đến hết video nên không cần thêm cảnh.
- Tập 1 đã giao trước quy tắc này; thêm vào khi chủ kênh yêu cầu.

## Quyết định 18/11/2026 (chủ kênh, tối): nhập quy tắc từ nhánh khác và câu kết

- **Không nhập nguyên xi `chung.md` của nhánh `lh6-dung-thu`.** Chỉ chuyển mục phù hợp với nguyên tắc cốt lõi 18/11 và không xung đột quy tắc đã duyệt. Không nhập quy tắc cũ chỉ vì nó có ở nhánh khác. Mục "Diễn giải của người kể" (duyệt 01/11) giữ trong `quy-tac/giong-van.md`.
- **Giữ lời bàn của sử gia có ghi rõ tên** khi lời bàn giúp giải thích hoặc làm sáng tỏ câu chuyện. KHÔNG áp dụng quy tắc "bỏ hết lời bình của sử gia" (27/10, nhánh khác).
- **Phân biệt rõ lời sử gia được trích dẫn với diễn giải của người kể.** Không biến lời bàn thành sự thật đã xác minh khi nguồn chỉ là quan điểm của người viết sử.
- **Không mặc định câu kết phải có lời cảm ơn.** Câu cuối khép câu chuyện tự nhiên, có ý nghĩa; lời cảm ơn chỉ dùng khi hợp với cách kết của video. (Dòng "Đoạn cuối gồm một câu tóm gọn và lời cảm ơn" ở mục 10 của `nguyen-tac-cot-loi.md` và kiểm ❌ "thiếu lời cảm ơn chuẩn" ở `kiem_khung.py` trái quyết định này; chờ chủ kênh duyệt bản sửa, xem `ke-hoach/kiem-khung-bang-chi-tiet-18-11.md`.)
- `kiem_khung.py`: chưa duyệt hạ đồng loạt 12 mục ❌; cần xem bảng chi tiết từng mục.
- Giai đoạn 2 theo trình tự: đối chiếu → bản gộp dự thảo → chủ kênh duyệt → mới thay file gốc.
