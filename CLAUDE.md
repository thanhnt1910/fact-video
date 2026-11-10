# Hướng dẫn cho Claude trong repo này (nhánh `khoa-hoc`, kênh Người Giải Mã)

Nhánh này làm video khoa học dọc 9:16 (1080×1920) tiếng Việt cho trang "Người Giải Mã", dựng bằng Remotion, giọng Leda.
Quy tắc của kênh lịch sử Người Gác Sử (Tam Quốc, sử Việt, video bản đồ, vẽ ảnh, Veo, bài Facebook) nằm ở `quy-tac/nguoi-gac-su.md`: chỉ đọc khi làm kênh đó.

## Cách làm việc với chủ kênh
- Chủ kênh làm trên điện thoại: không bao giờ bảo chủ kênh chạy lệnh hay git; Claude tự làm hết.
- Chủ kênh chỉ duyệt câu văn của kịch bản. Chủ đề, nền, hình, mũ nhân vật, ví dụ minh họa: Claude tự quyết và nói ngắn gọn đã chọn gì; không đẩy việc quyết định hay việc kiểm tra sang chủ kênh.
- Workflow (đọc giọng, dựng, vẽ ảnh) chỉ chạy khi chủ kênh yêu cầu, và chỉ chạy đúng video được yêu cầu.
- Khi video xong phải giao đủ: video, file SRT, ảnh bìa, tiêu đề, mô tả có nguồn, hashtag không dấu.

## Kịch bản (chi tiết: skill `viet-kich-ban-khoa-hoc`, ý tưởng: `ke-hoach/khoa-hoc-y-tuong-video.md`)
- Chỉ nói điều có thật, có nguồn. Claude tự tra nguồn gốc từng tên, năm, con số trước khi gửi; số liệu quan trọng đối chiếu hai nguồn. Điều không kiểm được thì bỏ khỏi lời kể. Giai thoại phải nói rõ là giai thoại.
- Liền mạch: một mạch nguyên nhân – kết quả, mỗi câu nối sang câu sau, câu kết quay lại câu hỏi mở đầu.
- Gần gũi, dễ hiểu: câu ngắn (khoảng 22 chữ trở xuống), một ý một câu, từ đời thường; thuật ngữ giải thích ngay trong câu. Viết đủ, không nói tắt.
- Giải thích bằng ví dụ: mỗi ý khó đi kèm một ví dụ hoặc phép so sánh với vật quen (muỗng canh, hạt cát, sân bóng). Có công thức thật, tính từng bước bằng số cụ thể; mỗi câu chỉ một phép tính, số dài thì lời đọc làm tròn và số đầy đủ hiện trên màn hình.
- Độ dài tùy chủ đề: đủ để giải thích rõ, không độn, không cắt mất bước giải thích.
- Mở đầu: câu hỏi gây tò mò trong 3 câu đầu; 25 giây đầu tối đa một mốc năm và hai tên riêng; nguồn chỉ nhắc sau giây 30.
- Mỗi video trọn gói: không "tập sau", không nhắc video khác, không kêu gọi bấm nút.
- Trước khi gửi: `python3 remotion/scripts/kiem_kich_ban_khoa_hoc.py <file.md>` phải ĐẠT; mỗi ⚠️ phải sửa hoặc nêu lý do giữ.

## Giọng đọc
- Giọng Leda (Gemini), đọc TỪNG CÂU (mỗi câu một lần gọi), dùng giọng gốc: không chỉnh tốc độ, không chỉnh cao độ.
- File câu đọc: `ke-hoach/giong-video-khoa-hoc-<tên>.json`; chạy `gemini-demo.yml` (`voices=Leda`, `video=<tên>`), kết quả ở `demo/<tên>/leda/NN.wav`.
- Mỗi lần chỉ chạy MỘT video (hai lượt chạy song song đẩy đè nhau, mất kết quả). Gặp 429 thì chạy lại: chỉ đọc câu còn thiếu.

## Hình và dựng
- Mỗi video có nền riêng theo chủ đề (`remotion/src/<tên>/Bg.tsx`) và một dấu ấn riêng lặp lại xuyên video; nền tương phản thấp, không át chữ.
- Nhân vật người que đội mũ phải chuyển động (đi lại, giơ tay), không đứng im.
- Vùng an toàn: tiêu đề y 200–340, hình y 440–1260, phụ đề từ y 1330, x 90–990; logo góc trên phải. Không chữ nào tràn khung hay đè nhau.
- Phụ đề viết gần nguyên văn lời đọc (chỉ đổi số sang chữ số), để chữ khớp tiếng.
- Trước khi dựng bản đầy đủ: chụp khung hình từng nhịp (`node scripts/stills.mjs`) và soi ở cỡ lớn.
- Thứ tự: giọng → thời lượng (`leda_dur.json`) → phụ đề (`scripts/tao_phu_de.py`) → tiếng động → dựng → trộn (`scripts/mix_<tên>.py`) → SRT, bìa, mô tả. Mẫu: `remotion/src/vuongmien/`.
- Ảnh bìa luôn có logo kênh ở góc trên phải; không chữ hay hình đè lên logo; xem bìa ở cỡ lớn trước khi giao.

## Git
- Chỉ làm trên nhánh `khoa-hoc`; không đẩy lên `main` trừ khi chủ kênh yêu cầu.
- Mọi commit: `user.name Claude`, `user.email noreply@anthropic.com`, tiêu đề có `[skip ci]`.
- Commit tự động của workflow (tác giả `actions@...`) bị gắn "Unverified": đợi không còn run nào chạy rồi đặt lại tác giả (`git rebase --exec "git commit --amend --no-edit --reset-author -q" <SHA>^`) và đẩy bằng `--force-with-lease`.
- Cảnh báo "commit chưa đẩy" thường do tracking ref cũ: `git update-ref refs/remotes/origin/khoa-hoc $(git ls-remote origin khoa-hoc | cut -f1)`.
