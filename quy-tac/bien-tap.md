# Biên tập và gửi duyệt

> Chuyển nguyên văn từ CLAUDE.md. Nguồn: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`. Chuyển ngày 18/11/2026.

## Kịch bản phải kiểm đầy đủ TRƯỚC khi gửi chủ kênh duyệt (chủ kênh yêu cầu 07/11/2026, áp dụng mọi kịch bản)
- Không bao giờ đưa kịch bản còn chi tiết "cần kiểm" cho chủ kênh. Mọi năm, tên, số, địa danh phải tra xong (mỗi dữ kiện ít nhất hai nguồn, hoặc nói đúng mức một nguồn) rồi mới gửi duyệt. Chi tiết không kiểm được thì BỎ khỏi lời kể, không để treo và không hỏi chủ kênh kiểm hộ.
- Gửi kèm bảng nguồn đã đọc, điểm lệch giữa nguồn, và chi tiết đã bỏ. Chủ kênh duyệt nội dung, không duyệt thay việc kiểm dữ kiện.
- **Mỗi lần sửa kịch bản (dù một chữ) phải gửi lại toàn văn bản mới cho chủ kênh duyệt, kèm bảng "đoạn nào đổi, trước và sau, vì sao" (chủ kênh yêu cầu 07/11/2026).** Chưa được duyệt lại thì không đọc giọng, không dựng.

## Kịch bản gửi duyệt: cấm đẩy việc kiểm nguồn cho chủ kênh, có công cụ chặn (chủ kênh nhắc 11/11/2026, sau khi bản 7 kịch bản còn hai chi tiết chưa tra mà hỏi lại chủ kênh)
- Gặp chi tiết cứng không tra được hai nguồn hoặc bản gốc không mở được: BỎ khỏi lời kể ngay, ghi vào "Chi tiết đã bỏ". Không giữ lại rồi hỏi "anh muốn tôi tra không". Hỏi như vậy là vi phạm mục "Kịch bản phải kiểm đầy đủ TRƯỚC khi gửi chủ kênh duyệt".
- Một nguồn thứ cấp (báo, trang tổng hợp) chỉ đủ cho điều nó tự khẳng định; không dùng nó để gắn tên sách gốc hay tên người (Toàn thư, Vũ trung tùy bút, Dư địa chí...) vào lời kể nếu chưa mở được bản gốc hoặc bản dịch có số quyển.
- Trước khi gửi duyệt luôn chạy: `python phim_ban_do/kiem_gui_duyet.py <file gửi duyệt>`; phải ĐẠT (mã 0). Công cụ báo ❌ khi bản gửi còn cụm đẩy việc kiểm cho chủ kênh, thiếu mục nguồn, lệch nguồn, chi tiết đã bỏ, hook hoặc toàn văn, hoặc dưới 2 nguồn mỗi kịch bản.
- Mỗi dữ kiện cứng đếm theo nguồn ĐỘC LẬP: hai bài báo chép lại nhau là một nguồn.

## Câu hỏi tự rà về chất lượng (tầng 3, gợi ý cho người đọc, không phải lỗi; chủ kênh duyệt 18/11/2026)
Công cụ không trả lời được các câu này; Claude và chủ kênh đọc và quyết. Kịch bản không mắc lỗi nào chưa chắc đã hay.
- Hook đã đủ hấp dẫn chưa?
- Có chi tiết lịch sử đáng nhớ không?
- Nhịp kể có giữ chân người xem không?
- Kết thúc có tạo được dư âm không?
- Có thể rút gọn mà không mất thông tin không?
