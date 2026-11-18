# Bài đăng, ảnh bìa, giao video

> Chuyển nguyên văn từ CLAUDE.md, chờ gộp (3 mục ảnh bìa trùng nhau). Nguồn: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`. Chuyển ngày 18/11/2026.

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

## Ảnh bìa video: luôn có logo kênh, đặt giống video bản đồ (chủ kênh yêu cầu 24/10/2026, áp dụng mọi bìa sau)
- Mọi ảnh bìa (YouTube, Facebook, TikTok) phải có logo cây đèn `assets/logo/nguoi-gac-su.png`, đặt **giống logo trong video bản đồ** (`mapfilm3.py`): vuông 130 px, độ đậm 0,8, góc trên bên phải, cách mép phải 44 px và mép trên 34 px (khổ 1920 rộng; khổ dọc 1080 dùng cùng cỡ và vị trí). Không phóng to, không đổ bóng, không bỏ.
- Không để chữ hay hình đè lên logo; khung hình bản đồ lấy làm nền phải cắt bỏ khung HUD (hộp năm, chú giải, la bàn, phụ đề) rồi mới đặt chữ.
- Mẫu và mã nguồn: `assets/bia/NQ1/tao_bia.py` (chạy `python assets/bia/NQ1/tao_bia.py <khung.jpg>`; sửa chữ và vùng cắt cho video mới). Kiểm bằng cách xem ảnh bìa ở cỡ lớn trước khi giao.

## Ảnh bìa dọc 1080×1920: mẫu đã duyệt, dùng cho mọi video cùng bố cục (chủ kênh duyệt 06/11/2026, từ tập 1 "Chín quận")
Mẫu ảnh: `assets/bia/HAN1/bia_v3.png`. Mã tạo: `python assets/bia/tao_bia_mau.py <cau_hinh.json> [ra.png]`; cấu hình mẫu `assets/bia/HAN1/bia.json` (chạy lại cho ra đúng ảnh đã duyệt, sai khác 0). Tập mới: sao chép `bia.json` sang `assets/bia/<MÃ>/`, đổi chữ, danh sách điểm (kinh, vĩ), `lon0`, `scale`, `oy`.
- **Bố cục:** bản đồ địa hình phủ kín khung (`map_relief.jpg`), chấm điểm phát sáng ở nửa trên; thẻ đỏ viền vàng góc trái trên (mốc năm); thẻ trắng nghiêng (triều đại hoặc bên chính); tiêu đề hai dòng giữa ảnh (dòng 1 trắng ngà, dòng 2 vàng, dòng 2 là câu hỏi gây tò mò); thẻ tên loạt và số tập; chân trang thương hiệu "NGƯỜI GÁC SỬ" + khẩu hiệu "LỊCH SỬ THEO CHÍNH SỬ". Logo cây đèn góc trên phải đúng quy tắc logo ở mục "Ảnh bìa video".
- **Chữ chính nằm trong y 70–1560.** Vùng đáy Facebook/TikTok che; chân trang chỉ là thương hiệu. Không để đáy ảnh đen trơn: bản đồ mờ dần sang xanh biển đậm cùng chân trang.
- **Tiêu đề chữ Việt phải đọc được ở cỡ điện thoại:** phông Oswald 700 cỡ khoảng 206 px; viền ngoài là LỚP RIÊNG phía sau chữ (không dùng `-webkit-text-stroke` trên chữ chính vì ăn mất dấu); khung chữ có padding trên 50 px dưới 60 px để không cắt dấu dưới (Ạ, Ị); hai dòng cách nhau đủ để dấu mũ dòng dưới không chạm dòng trên. Phông Be Vietnam Pro Black quá nhỏ dấu, Anton dính dấu: không dùng cho tiêu đề.
- **Tự kiểm trước khi giao:** xem ảnh cắt vùng tiêu đề ở cỡ lớn và bản thu 270×480; mọi dấu phải thấy rõ (dấu chấm dưới Ạ, mũ trên Â/Ô, huyền, sắc). Không giao khi chưa kiểm.
- Phông (OFL) ở `assets/bia/fonts/`. Mẫu cũ `assets/bia/HAN1/tao_bia.py` (nền khung video) giữ để tham khảo, không dùng cho bố cục mới.

## Ảnh bìa video: đúng cốt truyện và cuốn hút (chủ kênh chốt 10/11/2026, từ bìa #15 Cầu Long Biên bị làm chân dung Eiffel; áp dụng mọi bìa từ nay)
Bổ sung cho mục "Ảnh bìa video", "Ảnh bìa dọc 1080×1920". Mỗi video chỉ MỘT bìa, không làm nhiều bản cho chủ kênh chọn.
- **Hình phải đúng cốt truyện video đang nói.** Ảnh chính của bìa là chủ thể của video (cầu Long Biên thì ảnh cây cầu, trống đồng thì ảnh trống). KHÔNG đặt chân dung nhân vật làm ảnh bìa khi chủ thể là vật hoặc công trình, KHÔNG có ngoại lệ ("không thêm ngoại lệ", chủ kênh 10/11/2026). Tên người nhắc trên bìa đi vào chữ, không đi vào hình. Chân dung chỉ dùng khi video kể về chính người đó.
- **Chọn ảnh:** trước khi làm bìa xem mọi ảnh ứng viên cạnh nhau. Chọn ảnh toàn cảnh, rõ hình dáng đặc trưng, sáng, không bị che quá một phần ba; người lạ nhìn 1 giây phải đoán được chủ đề. Tránh ảnh cận chi tiết (biển tên, đinh tán), ảnh mờ, ảnh có logo kho ảnh. Ảnh chi tiết chỉ dùng khi chính chi tiết đó là điểm gây tò mò.
- **Bìa phải cuốn hút, gây tò mò, không chỉ minh họa.** Mỗi bìa có MỘT điểm gây tò mò nhìn thấy ngay trên hình: khoanh đỏ vào đúng chỗ của câu hỏi chính kèm dấu "?" (trường `hook=dict(cx, cy, r, q)` trong `assets/bia/XK/tao_bia.py`, tọa độ theo khung 1080×1920), hoặc mũi tên, dấu X đỏ, hình đối lập. Chữ dòng 1 nêu chủ thể, dòng 2 là câu hỏi hoặc điều lạ nhất của video (tối đa 4 chữ mỗi dòng, 2 dòng). Dòng chữ phải khớp điều video sẽ chứng minh; không giật tít sai sự thật. Ảnh được tăng nhẹ tương phản và màu (đã đặt sẵn trong `tao_bia.py`) để nổi hơn trên nền tối.
- **Khai báo `chu_the`** (vật trong ảnh) trong mục cấu hình bìa; chỉ giao khi `chu_the` khớp tên video. Thẻ tên nhỏ trên ảnh (như "CẦU LONG BIÊN") phải đúng vật trong ảnh.
- **Bố cục và logo giữ nguyên mẫu đã duyệt** (logo cây đèn, số tập, chữ trong y 70–1560, đáy chỉ thương hiệu). Vòng khoanh và dấu "?" không che chủ thể và không đè logo, thẻ năm, thẻ tên.
- **Kiểm trước khi giao (bắt buộc):** mở bìa ở cỡ lớn, tự hỏi "chưa biết video, nhìn ảnh này đoán chuyện gì?"; đoán sai hoặc không đoán được thì đổi ảnh. So hình, chữ với tên video và câu 1 kịch bản; kiểm dấu tiếng Việt ở cỡ 270×480. Khi giao ghi một dòng: ảnh dùng (tác giả, giấy phép) và vì sao chọn.
