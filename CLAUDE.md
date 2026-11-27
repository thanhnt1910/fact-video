# Hướng dẫn cho Claude khi làm việc trong repo này

Nhánh `claude/bi-an-lich-su`: hướng mới của kênh "Người Gác Sử", lịch sử bí ẩn thế giới, không làm đề tài Việt Nam. Các quy tắc, kế hoạch và kịch bản cũ đã gỡ khỏi nhánh này, vẫn còn ở nhánh `claude/cach-ho-cai-tri-tap-1`.

## Vai trò
- Claude giúp chủ kênh (StrawMan, ở Việt Nam, viết và trả lời bằng tiếng Việt) chọn đề tài, nghiên cứu nguồn, viết lời kể, dựng và kiểm video.
- Chủ kênh không đọc được nguồn tiếng Anh, nên mọi dữ kiện phải đi kèm bảng nguồn nói rõ nguồn nào chép gì.

## Định hướng
- Mỗi tập là một hồ sơ: bắt đầu bằng một câu hỏi cụ thể, lần theo chứng cứ, đối chiếu giả thuyết, kết bằng điều đã biết chắc và phần còn bỏ ngỏ.
- Mỗi tập có nhãn mức độ chắc chắn (cao, vừa, thấp, chưa rõ).
- Không khẳng định một bí ẩn chưa được giải nếu nghiên cứu đã có lời giải đáng kể. Không dùng "sự thật bị che giấu", "cấm kỵ" khi không có bằng chứng. Không biến khoảng trống tư liệu thành bằng chứng cho giả thuyết kỳ bí.
- Không bịa lời thoại, nội tâm, nhân vật. Không dùng video của kênh khác làm nguồn chính. Ảnh AI chỉ là minh họa, không trình bày như tư liệu thật.
- Dữ kiện cứng (năm, tên, số, địa danh) phải có ít nhất hai nguồn độc lập hoặc được nói rõ là chỉ có một nguồn. Không tra được thì bỏ khỏi lời kể.

## Quy trình
Chủ kênh duyệt ở bốn cổng, chưa qua cổng thì không sang bước sau: A chủ đề, B mạch truyện và bảng nguồn, C lời kể, D video. Không đọc giọng, không dựng, không chạy workflow khi chưa được duyệt.

## Git
- Commit với `user.email noreply@anthropic.com`, `user.name Claude`.
- Không đẩy `main` khi chưa được yêu cầu.
- Workflow chỉ chạy khi chủ kênh yêu cầu và chỉ đúng video được yêu cầu.

## Quy tắc chi tiết
`quy-tac/kich-ban-va-dung.md` (bản nháp chờ chủ kênh duyệt): chọn đề tài, phiếu hồ sơ, cấu trúc tập, câu chữ, bảng chấm kịch bản, dựng hình, giọng, đo lường. Mục 11 của file đó liệt kê các điều còn chờ chủ kênh chốt.
