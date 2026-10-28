# Series "Tên đường": nhân vật gắn với tên đường (chủ kênh chốt 28/10/2026)

Chuyển hướng sau video Lý Công Uẩn (dạng dọc, đèn cầm thước): tạm dừng video lịch sử theo dòng thời gian, làm series giới thiệu nhân vật có tên đặt cho đường phố.

## Nội dung: chỉ tiểu sử đơn giản
- Mỗi video một nhân vật, nói **nguồn gốc** (quê quán, gia đình, xuất thân), **năm sinh, năm mất**, và **các công danh** (chức vụ, khoa bảng, công trạng, tác phẩm, trận đánh tiêu biểu) theo thứ tự thời gian.
- Chỉ dữ kiện có sử sách ghi và được thống nhất. Năm sinh, năm mất còn tranh cãi thì nói rõ "theo sử chép" hoặc "đến nay chưa rõ".
- Không bịa lời thoại, nội tâm, chi tiết đời tư. Không kể truyền thuyết như sự thật; truyền thuyết chỉ nhắc ngắn kèm ghi rõ là truyền thuyết.
- Mỗi nhân vật nêu một dòng "vì sao có đường mang tên ông/bà" khi có thông tin chắc chắn (không đoán).

## Không giới hạn về năm
- **Bỏ mốc "dừng trước 1858"** cho series này: nhân vật thuộc mọi thời kỳ, kể cả thế kỷ 19, 20, nếu có tên đường.
- Với nhân vật hoạt động sau 1858 (và mọi nhân vật liên quan chính trị): chỉ kể dữ kiện đã được ghi nhận (sinh, mất, chức vụ, tổ chức đã tham gia, trận đánh hoặc tác phẩm tiêu biểu). Không bình luận, đánh giá chính trị, không so sánh với thời nay, không nói về pháp luật hay thời cuộc đương thời.
- Giữ nguyên các quy tắc chung khác: tôn trọng, không đùa cợt nhân vật (khung đùa không nhắm vào nhân vật), vẫn phải đúng pháp luật Việt Nam.

## Nguồn
- Nhân vật cổ: Đại Việt sử ký toàn thư, Khâm định Việt sử thông giám cương mục, Đại Nam thực lục, Đại Nam liệt truyện.
- Nhân vật cận hiện đại: sách và tư liệu đã xuất bản (tiểu sử chính thức, từ điển nhân vật lịch sử, tư liệu lưu trữ có nguồn), đối chiếu ít nhất hai nguồn cho năm sinh, năm mất và chức vụ.
- Ghi nguồn trong phần mô tả video và bình luận ghim, như các series khác.

## Cách làm video
- Ngắn gọn: khoảng 60–120 giây, mỗi video một nhân vật. Cấu trúc: tên đường, nhân vật là ai, quê và xuất thân, năm sinh, các chức danh và công trạng theo thứ tự thời gian, năm mất, chốt bằng một câu về nơi đặt tên đường (nếu chắc).
- Dùng bộ dựng dọc đang có (`phim_ban_do/doc2.py`): đèn cầm thước, thẻ minh họa, giọng Puck, phụ đề chạy chữ. **Mỗi cảnh chỉ dùng một lần** trong một video; thẻ chân dung dùng tranh nhân vật trong `assets/icon_nhan_vat/` hoặc vẽ đơn giản bằng code, không dùng ảnh thật có bản quyền.
- Quy trình giọng và kiểm video như `quy-tac/video-ban-do.md` (kịch bản kiểm bằng `kiem_kich_ban.py`, đọc, nhận dạng, `kiem_giong.py` trước khi dựng).
- Kịch bản mỗi nhân vật ở `ke-hoach/ten-duong-<tên>.md`, có nhãn độ chắc từng dữ kiện và mục "Nguồn", chủ kênh duyệt trước khi đọc giọng.
