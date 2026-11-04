# Quy tắc kiểm chứng và viết kịch bản kênh tiếng Anh (History Mysteries Daily)

Chủ kênh yêu cầu ghi chi tiết ngày 04/11/2026, rút ra từ lần tự đánh giá kịch bản Roanoke (RN1): bản đầu có 5 lỗi mà lần soát đầu không bắt được. Áp dụng cho mọi kịch bản tiếng Anh sau. Cùng đọc với mục "Kịch bản phải tự kiểm trước khi gửi chủ kênh" trong `CLAUDE.md`.

## A. Kiểm chứng (tự làm trước khi gửi, không đẩy cho chủ kênh)
1. **Đối chiếu từng câu với văn bản gốc, không chỉ với Wikipedia.** Chuyện có tài liệu gốc (Hakluyt, biên niên sử, thư từ…) phải mở và đọc đúng đoạn của cảnh chính, rồi so từng câu của lời kể với văn bản. Nhãn SỬ chỉ dùng khi đã làm vậy (ghi tên nguồn và đường dẫn).
2. **Rà sự kiện bị bỏ sót.** Đọc nguyên đoạn nguồn quanh mỗi cảnh then chốt, liệt kê MỌI biến cố (người chết, bão, tai nạn, tranh cãi), rồi quyết định đưa vào hay bỏ. Biến cố nào giải thích nguyên nhân – kết quả của cảnh sau thì phải đưa vào. (RN1 sót: thuyền Spicer lật, bảy người chết, ngày 17/8/1590.)
3. **Câu phủ định tuyệt đối cần nguồn thứ hai.** "Nothing more was heard", "never seen again", "no one ever" chỉ được viết khi hai nguồn độc lập cùng nói; còn lại dùng "no confirmed sighting", "is not known to have". (RN1 sai ở câu mười lăm người của Grenville: có nguồn nói tìm thấy xương.)
4. **Chi tiết chỉ có một nguồn** (nhất là chỉ Wikipedia): gắn nhãn TC và mở câu bằng "According to …", hoặc bỏ khỏi lời kể.
5. **Con số dao động** (số người, số quân, số tàu): lời kể dùng "more than", "about", "most counts"; ghi dải số trong mục kiểm chứng. **Tiêu đề, ảnh bìa, mô tả KHÔNG ghi con số chính xác khi nguồn không thống nhất**; dùng "100+", "More than 100". Các câu trong cùng video không được lệch nhau (quét mọi số trong json trước khi gửi).
6. **Cấm mốc thời gian tương đối** ("a few years ago", "recently", "today") trong lời kể: ghi năm cụ thể. Video đăng nhiều năm sau, chữ "recently" sẽ sai.
7. **Từ chắc chắn ("certain", "proves", "always", "never")** chỉ cho điều có tài liệu. Giả thuyết dùng "may", "suggests", "unproven".
8. **Không suy diễn tâm trạng hay cách hành động** mà nguồn không nói ("calmly", "hoped", "feared"). Lời thoại và nội tâm không bịa.
9. Sau khi sửa: ghi vào mục "Sửa ngày …" của file kịch bản (câu nào, vì sao, nguồn nào). Bản gửi nêu rõ số câu đã đối chiếu nguyên văn, số câu hạ nhãn hoặc bỏ.

## B. Viết cho giọng đọc tiếng Anh
- Năm viết thành chữ ("fifteen eighty-seven"), số ngày thành chữ ("August eighteenth"). Từ khó đọc (CROATOAN) có hướng dẫn phát âm trong STYLE của `en_video.py`.
- Mỗi câu một ý, một hoặc hai câu mỗi beat. Chương 7–10 beat; tổng 70–90 beat; 1.800–2.100 từ (khoảng 13–14 phút).
- Mở bằng cảnh gây tò mò là sự kiện có thật của chính video; kết bằng phân tách "chắc chắn / giả thuyết / bịa" và câu hỏi bình luận.
- Đơn vị Mỹ (dặm, feet) giữ nguyên trong lời đọc; bản Việt ghi thêm quy đổi.

## C. Quy trình sửa kịch bản đã có giọng
- Sửa lời đọc thì sửa đồng thời: `<tên>.json`, `vi.json`, `<tên>_song_ngu.md`, `<tên>_kich_ban.md` (bảng + mục "Sửa"), mô tả YouTube, ảnh bìa (nếu có số hoặc tên bị đổi).
- Thêm hoặc bớt một beat làm lệch cách chia cụm 8 beat theo chương, nên các cụm phía sau đổi chữ và phải đọc lại giọng. Báo chủ kênh số cụm phải đọc lại và hỏi trước khi chạy (tốn hạn mức Gemini). Hết mọi khóa thì dừng, không đợi.
- Chỉ chạy workflow khi chủ kênh yêu cầu; push chỉ chứa file kịch bản/tài liệu thì để `[skip ci]` trong tiêu đề commit.
