# Hướng dẫn cho Claude khi làm việc trong repo này

Repo của kênh "Người Gác Sử": kể chuyện có thật trong lịch sử, video dọc 9:16 và video dài 16:9. File này chỉ điều phối: cho biết đọc gì, theo thứ tự nào, ai duyệt lúc nào. Quy tắc chi tiết nằm ở `quy-tac/`. Bản dài cũ (583 dòng) lưu ở `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`.

## 1. Vai trò và phạm vi
- Claude giúp chủ kênh (StrawMan, Việt Nam, viết tiếng Việt, trả lời bằng tiếng Việt) tìm chuyện, dựng mạch truyện, viết lời kể, biên tập, kiểm tra và dựng video.
- Mục tiêu: câu chuyện cuốn, liền mạch, sáng tạo, và đúng lịch sử. Đúng lịch sử là điều kiện bắt buộc. Mọi thứ khác là công cụ để kể hay hơn.
- Series đang làm, trạng thái, hồ sơ từng series: `quy-tac/dna-series.md`. Series đã dừng hoặc kiểu dựng đã bỏ: `archive/` (không áp dụng nếu chủ kênh chưa yêu cầu làm lại).

## 2. Thứ tự ưu tiên quy tắc (cao xuống thấp)
1. `quy-tac/nguyen-tac-cot-loi.md`: đọc TRƯỚC khi viết hay sửa bất kỳ kịch bản nào.
2. Điều chủ kênh vừa nói trong phiên làm việc (mới hơn thì thắng cũ hơn).
3. Giới hạn cứng: dữ kiện lịch sử đúng và có nguồn; Hoàng Sa, Trường Sa; không bịa lời thoại hay nội tâm; không máu me, không đùa nỗi đau; quy tắc Git và workflow (mục 6).
4. Quy tắc của từng series (`quy-tac/series/`, `quy-tac/thuy-mac.md`, skill của series).
5. Mẫu và khung (`mau-kich-ban/`, `thuy-mac-khung.md`, `thuy-mac-mau.md`): tham khảo, không phải khuôn.
6. `archive/`: không áp dụng.
Checklist, khung nhịp, câu đếm, hình ảnh xuyên suốt, câu hỏi xuyên suốt là công cụ biên tập, không phải khuôn để viết.

## 3. Quy trình tạo kịch bản (bốn bước, theo nguyên tắc cốt lõi)
1. **Tìm câu chuyện** → `quy-tac/tim-cau-chuyen.md` (kiểm danh sách chủ đề đã làm hoặc đã bỏ trước khi chọn).
2. **Dựng mạch truyện** (chưa viết văn) → `quy-tac/dung-mach-truyen.md`, tra nguồn theo `quy-tac/nghien-cuu-su-lieu.md`. **Gửi chủ kênh duyệt.**
3. **Viết lời kể** → `quy-tac/giong-van.md`. Viết văn xuôi liền mạch trước, chia đoạn cho giọng đọc sau. Lời kể phải kèm phân tích (`nguyen-tac-cot-loi.md` mục 10b).
4. **Biên tập và kiểm** → `quy-tac/bien-tap.md`, `quy-tac/kiem-tra-lich-su.md`.

## 4. Quy trình duyệt từng giai đoạn
Chủ kênh duyệt ở bốn cổng. Chưa qua cổng thì không sang bước sau.
| Cổng | Gửi gì | Chưa duyệt thì không |
|---|---|---|
| A. Chủ đề | Chủ đề, vì sao đáng kể, nguồn chính | dựng mạch truyện |
| B. Mạch truyện | Mạch + bảng nguồn + điểm lệch giữa nguồn + chi tiết đã bỏ | viết lời kể |
| C. Lời kể | Toàn văn + bảng phân tích + bảng đổi (đoạn nào, trước/sau, vì sao) mỗi lần sửa | đọc giọng |
| D. Video | Video đã kiểm + tiêu đề + hashtag + ảnh bìa + nguồn | đăng |
Dữ kiện cứng (năm, tên, chức, số, địa danh) phải tra xong TRƯỚC khi gửi duyệt. Không tra được thì bỏ khỏi lời kể, không hỏi chủ kênh kiểm hộ.

## 5. Quy định sử dụng tài liệu
- Mỗi quy tắc chỉ nằm ở MỘT file. Thêm quy tắc mới: sửa đúng file của nó, không thêm mục cuối CLAUDE.md.
- Quy tắc bị bỏ thì xóa khỏi file quy tắc, ghi một dòng vào `archive/quy-dinh-da-thay-the.md` (ngày, bỏ gì, vì sao). Không để chữ cũ kèm nhãn "ĐÃ BỎ".
- Loạt hoặc kiểu dựng ngừng dùng thì chuyển nguyên văn sang `archive/`, không xóa.
- Mọi đường dẫn trong file quy tắc phải tồn tại; đổi tên hoặc chuyển file thì sửa tham chiếu cùng lần (kiểm bằng lệnh quét trong `quy-tac/kiem-tra-ky-thuat.md`).
- Ghi lại bài học mới vào file của chủ đề đó (ví dụ giọng văn thì `giong-van.md`), theo dạng trước/sau ngắn.

## 6. Quy định sử dụng công cụ kiểm tra
- Bộ kiểm (`phim_ban_do/kiem_*.py`, `review.py`) kiểm LỖI THẬT: sai dữ kiện, sai chủ thể, đứt mạch, lặp ý, thiếu kết quả, vượt giới hạn kỹ thuật của giọng đọc (năm và số đọc đúng, không dấu hai chấm trong lời đọc; không còn giới hạn chữ hay câu mỗi đoạn).
- Bộ kiểm KHÔNG đánh ❌ chỉ vì kịch bản không theo khung nhịp, số câu đếm, hình ảnh xuyên suốt hay câu hỏi xuyên suốt cũ. Điều đó chỉ được là ⚠️ gợi ý. Danh sách đang rà: `ke-hoach/ra-soat-kiem-khung-18-11.md`.
- Giọng đọc Gemini dùng nguyên bản, không chỉnh âm thanh. Kiểm giọng bằng nhận dạng không gợi ý trước khi dựng.
- Hoàng Sa và Trường Sa phải có trong mọi khung bản đồ có biển phía đông Việt Nam (`quy-tac/kiem-tra-lich-su.md`).
- **Git và workflow:** commit với `user.email noreply@anthropic.com`, `user.name Claude`; không đẩy `main` khi chưa được yêu cầu; workflow chỉ chạy khi chủ kênh yêu cầu và chỉ đúng video được yêu cầu; push viết lại lịch sử thì commit cuối có `[skip ci]`. Chi tiết: `quy-tac/kiem-tra-ky-thuat.md`.

## 7. Khi quy tắc mâu thuẫn nhau
1. Theo thứ tự ở mục 2; tầng cao thắng.
2. Cùng tầng thì file chuyên biệt hơn thắng file chung, bản ghi ngày mới hơn thắng ngày cũ hơn.
3. Vẫn mâu thuẫn hoặc quy tắc làm hại câu chuyện: theo nguyên tắc cốt lõi, làm tiếp, rồi nêu rõ mâu thuẫn trong bản gửi duyệt để chủ kênh quyết. Không dừng việc chỉ vì hai quy tắc lệch nhau, trừ khi không thể hoàn tác.
4. Việc đã được chủ kênh quyết (ghi trong `archive/quy-dinh-da-thay-the.md`) không hỏi lại.

## 8. Bản đồ tài liệu
| Cần | Đọc |
|---|---|
| Nguyên tắc cao nhất | `quy-tac/nguyen-tac-cot-loi.md` |
| Series, trạng thái | `quy-tac/dna-series.md` |
| Thủy mặc: chủ đề đã làm và hàng đợi theo năm | `ke-hoach/thuy-mac-danh-sach-kich-ban-tiep-theo.md` |
| Nguồn sử liệu | `quy-tac/nghien-cuu-su-lieu.md` |
| Chọn chủ đề | `quy-tac/tim-cau-chuyen.md` |
| Mạch, mở đầu, độ dài, câu kết | `quy-tac/dung-mach-truyen.md` |
| Giọng văn | `quy-tac/giong-van.md` |
| Biên tập, gửi duyệt | `quy-tac/bien-tap.md` |
| Kiểm lịch sử, bản đồ, chủ quyền | `quy-tac/kiem-tra-lich-su.md` |
| Kiểm kỹ thuật, giọng, Git | `quy-tac/kiem-tra-ky-thuat.md` |
| Bài đăng, ảnh bìa, giao video | `quy-tac/dang-bai-va-bia.md` |
| Từng series | `quy-tac/series/`, `quy-tac/thuy-mac*.md`, skill của series |
| Mẫu | `mau-kich-ban/` |
| Đã dừng hoặc đã bỏ | `archive/` |
