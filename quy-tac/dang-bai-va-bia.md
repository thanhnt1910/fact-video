# Bài đăng, ảnh bìa, giao video

> Mục ảnh bìa gộp từ ba mục cũ, chủ kênh duyệt 18/11/2026 (`ke-hoach/ban-nhap-bia-gop-18-11.md`); bản gốc ba mục: `archive/quy-dinh-da-thay-the.md`. Bài Facebook và giao video chuyển nguyên văn từ CLAUDE.md.

## Bài đăng Facebook (và mọi bài viết đăng mạng): văn phong rõ ràng, mạch lạc, dễ hiểu (chủ kênh yêu cầu 20/10/2026, áp dụng mọi bài post sau)

Người đọc lướt điện thoại, không biết trước chuyện. Bài phải đọc một lần là hiểu.
- **Câu ngắn, một ý một câu** (khoảng 20 từ trở xuống). Đoạn 2–4 câu, cách nhau một dòng trống. Không dồn nhiều số liệu và tên riêng vào một câu.
- **Có đầu có đuôi:** mở bằng điều gây tò mò (1–2 câu) → kể theo thứ tự thời gian hoặc nguyên nhân – kết quả → chốt bằng ý chính và một câu hỏi đơn giản cho người xem. Chia bằng các mục ngắn, có tiêu đề rõ (kèm một emoji), mỗi mục trả lời một câu hỏi ("Hai người là ai?", "Chuyện gì xảy ra hôm đó?", "Vì sao ít người tin?").
- **Từ đời thường.** Thuật ngữ, tên tổ chức nước ngoài, đơn vị lạ phải giải thích ngay bằng tiếng Việt dễ hiểu. Đổi sang đơn vị Việt Nam (mét, ki-lô-mét), không để feet, dặm. Tên tiếng Anh chỉ ghi khi cần, đặt sau cách gọi tiếng Việt. Không chép nguyên câu dịch máy từ tài liệu.
- **Mốc thời gian dạng danh sách ngắn** (mỗi dòng: ngày – chuyện gì xảy ra). Danh sách tối đa 5 dòng.
- **Dẫn chứng gọn trong bài:** nói thẳng "Theo ...", mỗi ý chính một nguồn ngắn. Danh sách nguồn dài và link để ở bình luận, không nhét vào bài.
- **Phân biệt rõ điều chắc chắn và giai thoại:** điều có tài liệu thì kể thẳng; điều còn tranh cãi thì nói "theo lời kể" hoặc "đến nay chưa rõ".
- **Tránh:** câu lồng nhiều ngoặc đơn, chữ viết tắt không giải thích, lặp ý, văn sách giáo khoa, giọng quảng cáo.
- **Tự đọc lại trước khi giao:** thử đọc như người chưa biết chuyện, đọc một lần có hiểu không? Câu nào phải đọc hai lần thì viết lại. Mẫu chuẩn: `telegram/sl21_bai_facebook.txt`.

## Giao video: mỗi video dựng xong phải gửi Telegram kèm tiêu đề và hashtag (chủ kênh yêu cầu 28/10/2026, áp dụng mọi video từ nay)
- Mỗi video dựng xong (ngắn hay dài, mọi series) phải gửi vào Telegram của chủ kênh, KHÔNG chỉ báo đường dẫn file. Tin nhắn gồm: file video (hoặc link tải nếu quá dung lượng), **tiêu đề đề xuất** (một dòng, gọn, gây tò mò, đúng nội dung) và **hashtag** (khoảng 5–8 thẻ: tên kênh, chủ đề, nhân vật hoặc địa danh, thời đại; không hashtag sai chủ đề hay câu khách).
- Gửi kèm ảnh bìa nếu đã có. Tiêu đề và hashtag viết theo văn phong rõ ràng của bài Facebook ở trên; tiêu đề không đoán sai sự thật, không giật tít sai lệch.
- Chỉ gửi sau khi đã qua bước kiểm (`kiem_video.py`, `review.py` không có ❌). Video chưa đạt thì không gửi, báo chủ kênh lỗi nào.
- Cách gửi: workflow `gui-file-telegram.yml` (ghi đường dẫn vào `ke-hoach/thu-giong-hai/gui_tg.txt`) hoặc `tg_text.py` cho phần chữ. Chỉ chạy khi chủ kênh đã yêu cầu dựng video đó (xem mục Git: workflow chỉ chạy khi được yêu cầu). Gửi xong phải xác nhận tin đã tới, không giả định.
- Với video dựng trong phiên làm việc này (không qua workflow): gửi file trực tiếp cho chủ kênh trong cuộc trò chuyện, kèm tiêu đề và hashtag trong cùng tin nhắn.

## Ảnh bìa video

Mỗi video một bìa (không làm nhiều bản cho chủ kênh chọn). Bìa phải khiến người lạ muốn xem, nhưng điều bìa hứa phải là điều video kể đúng. Mục B1–B3 và B5 là quy tắc chung; B4 là mẫu riêng của từng series, không bắt buộc cho series khác. Thiết kế theo video dài: chủ thể lớn, bố cục rõ, ít chữ, nhận ra được khi thu nhỏ.

### B1. Đúng nội dung (quy tắc chung, ưu tiên cao nhất của bìa)
- **Hình là chủ thể của video** (cầu Long Biên thì ảnh cây cầu, trống đồng thì ảnh trống). Không dùng chân dung nhân vật làm ảnh bìa khi chủ thể là vật hoặc công trình, không có ngoại lệ (chủ kênh 10/11/2026). Tên người nhắc trên bìa đi vào chữ, không đi vào hình. Chân dung chỉ dùng khi video kể về chính người đó.
- **Chữ trên bìa khớp điều video chứng minh được.** Không giật tít sai sự thật; khoanh, mũi tên, dấu "?" chỉ vào điều video thật sự kể, không ngụ ý điều video không nói.
- **Không để người xem hiểu sai thời đại.** Ảnh hiện đại, tranh vẽ về sau hay ảnh dựng không đặt kèm mốc năm theo kiểu như ảnh đương thời.
- **Một điểm gây tò mò** (điều lạ nhất của video), nhìn thấy ngay trên hình hoặc ở dòng chữ; không dồn khoanh, mũi tên và câu hỏi cùng lúc.
- Tiêu đề bìa phải thống nhất với tiêu đề đăng và câu mở đầu kịch bản về nội dung được hứa hẹn. Có thể diễn đạt ngắn gọn, hấp dẫn hơn nhưng không được tạo ra một câu chuyện khác với nội dung video.
- Khi giao ghi nguồn hoặc đường dẫn ảnh, tác giả và giấy phép sử dụng (nếu có), cùng lý do chọn ảnh.

### B2. Chữ và bố cục dễ đọc (quy tắc chung)
- Thiết kế ảnh bìa theo tỷ lệ 16:9, kích thước chuẩn 1920×1080.
- Tiêu đề tối đa hai dòng, ngắn gọn, ưu tiên khoảng 3–6 từ nếu phù hợp.
- Chủ thể chính phải nhận ra ngay khi ảnh thu nhỏ.
- Chữ có tương phản rõ với nền, dấu tiếng Việt đầy đủ, không bị cắt hoặc chạm vào nhau (dấu chấm dưới Ạ, Ị; mũ trên Â, Ô; huyền, sắc). Kỹ thuật gợi ý: viền chữ là lớp riêng phía sau chữ, không dùng `-webkit-text-stroke` trên chữ chính; padding đủ để không cắt dấu dưới; hai dòng cách nhau đủ để dấu dòng dưới không chạm dòng trên.
- Ngoài tiêu đề chỉ giữ logo, thẻ mốc năm hoặc thương hiệu khi thực sự cần thiết.
- Không nhồi số liệu, đoạn mô tả hoặc nhiều điểm gây chú ý cùng lúc.
- Phông và cỡ chữ là gợi ý, chọn theo kích thước chủ thể; thử Oswald 700 (OFL, ở `assets/bia/fonts/`) cỡ đủ lớn để đọc ở kích thước thu nhỏ. Be Vietnam Pro Black quá nhỏ dấu, Anton dính dấu: không dùng cho tiêu đề (kinh nghiệm từ bìa dọc, cần thử lại ở khung ngang).

### B3. Logo và chuẩn thương hiệu (khung ngang 1920×1080)
- Mọi bìa có logo cây đèn `assets/logo/nguoi-gac-su.png`, đặt giống logo trong video: vuông 130 px, độ đậm 0,8, góc trên bên phải, cách mép phải 44 px và mép trên 34 px. Không phóng to, không đổ bóng, không bỏ.
- Không để chữ hay hình đè lên logo. Nếu lấy khung hình bản đồ làm nền thì cắt bỏ khung HUD (hộp năm, chú giải, la bàn, phụ đề) trước khi đặt chữ.
- Bản 1920×1080 là bản bìa chính. Nếu cần dùng trên nền tảng hoặc định dạng có tỷ lệ khác, phải kiểm tra và thiết kế lại bố cục cho phù hợp; không mặc định cắt ảnh ngang là đủ.
- Số đo logo (130 px, 44/34 px) là cho khung ngang 1920×1080; nhìn trực quan trên bìa thực tế trước khi chốt.

### B4. Mẫu riêng của từng series (tham khảo; mẫu dọc chưa dùng cho bìa ngang)
- **Video bản đồ 16:9** (`assets/bia/NQ1/tao_bia.py`, `python assets/bia/NQ1/tao_bia.py <khung.jpg>`): mẫu duy nhất đã ở khung 1920×1080 (script cũng xuất bản dọc cho TikTok). Dùng làm điểm xuất phát cho bìa ngang; sửa chữ và vùng cắt cho video mới. Cần rà lại theo B1–B3 trước khi dùng (có phù hợp, có nhồi chữ không).
- **Chuyện cai trị ngàn năm** (tạm dừng): mẫu `assets/bia/HAN1/bia_v3.png` và `assets/bia/tao_bia_mau.py` là KHUNG DỌC 1080×1920, không dùng cho bìa ngang. Giữ làm tham khảo ý tưởng (thẻ mốc năm, thẻ triều đại, tiêu đề hai dòng, chân trang thương hiệu); khi series chạy lại thì làm mẫu ngang mới.
- **Bí mật biểu tượng** (`assets/bia/XK/tao_bia.py`): mẫu dọc 1080×1920, vòng khoanh đỏ kèm "?" (`hook=dict(cx, cy, r, q)`), khai báo `chu_the` khớp tên video. Chưa có mẫu ngang; ý "một điểm gây tò mò, khoanh đúng chỗ video kể" là phong cách của loạt, không phải khuôn của series khác.
- Series khác (thủy mặc, Sengoku, Tên tỉnh thành…): tự thiết kế theo B1–B3 ở 1920×1080, không bắt chước mẫu của series khác; có mẫu riêng thì ghi vào đây khi chủ kênh duyệt.

### B5. Chọn ảnh và kiểm trước khi giao
- **Chọn ảnh:** xem mọi ảnh ứng viên cạnh nhau. Ưu tiên ảnh toàn cảnh, rõ hình dáng đặc trưng, sáng, không bị che quá một phần ba; chủ thể lớn trong khung ngang. Tránh ảnh cận chi tiết (biển tên, đinh tán), ảnh mờ, ảnh có logo kho ảnh; ảnh chi tiết chỉ dùng khi chính chi tiết đó là điểm gây tò mò.
- **Kiểm (bắt buộc):** (1) mở bìa 1920×1080 ở cỡ lớn, tự hỏi "chưa biết video, nhìn ảnh này đoán chuyện gì?"; đoán sai hoặc không đoán được thì đổi ảnh; (2) thu nhỏ về cỡ hiển thị gợi ý của YouTube (khoảng 320×180) và kiểm chủ thể vẫn nhận ra, chữ vẫn đọc được, dấu tiếng Việt còn rõ; (3) so hình và chữ với tên video, tiêu đề đăng và câu 1 kịch bản (phải thống nhất, xem B1); (4) ghi nguồn hoặc đường dẫn ảnh, tác giả, giấy phép và lý do chọn. 320×180 chỉ là cỡ kiểm tra thu nhỏ, không phải cỡ xuất ảnh. Không giao khi chưa kiểm.
