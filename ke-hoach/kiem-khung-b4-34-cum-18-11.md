# B4: 34 cụm trong danh sách `CAM` của `kiem_khung.py`, chờ chủ kênh phân loại (18/11/2026)

**Trạng thái: ĐÃ PHÂN LOẠI VÀ ĐÃ ÁP DỤNG (18/11/2026, 22:11, chủ kênh duyệt đề xuất "làm đi").** N1 (❌): có thể thấy, điều đáng chú ý, quân thuyền. Tạm ❌ chờ xem cách dùng: câu trả lời nằm ở. N2 ⚠️ chỉ khi một kịch bản dùng từ 3 lần trở lên: không chỉ, bài học, phía bên kia, dấy binh. 26 cụm còn lại N2 ⚠️ mỗi lần gặp. Không cụm nào bị Bỏ. Danh sách vẫn đủ 34 cụm.

Cách kiểm hiện tại: tìm cụm trong câu (không phân biệt hoa thường, khớp chuỗi con) trong mọi đoạn; thấy là báo ❌ ở đoạn đó. Không xét ngữ cảnh.

Số liệu: quét 234 file `*_full.json` hiện có. "Lần" là số đoạn chứa cụm, "file" là số kịch bản chứa cụm. Cột "ví dụ" là một đoạn thật.

Cột "gợi ý ban đầu": **N1** = giữ ❌ (cụm sáo, dịch sát, chủ kênh đã chê); **N2** = hạ ⚠️ (có thể đúng ngữ cảnh). Chỉ đánh dấu cho 10 cụm chủ kênh đã nêu tên trong quyết định; 24 cụm còn lại để trống, chủ kênh chọn.

| # | Cụm | Lần | File | Gợi ý ban đầu | Ví dụ thật | Chủ kênh chọn (N1/N2/Bỏ) |
|---|---|---|---|---|---|---|
| 1 | bước ngoặt quan trọng | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 2 | chi tiết đặc biệt | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 3 | nổi tiếng nhất | 2 | 2 |  | `hs1` đoạn 7177: "Chuyện nổi tiếng nhất là ở chợ. Một tên côn đồ chặn ông lại: to cao, hay đeo kiếm, nhưng thật ra nhát. Có gan " | N2 ⚠️ mỗi lần gặp |
| 4 | không thể quên | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 5 | quyết liệt | 2 | 1 | N2 | `lt1v6` đoạn 32043: "Cuộc vây hãm kéo dài. Quân phòng thủ chống trả quyết liệt, trong khi quân Đại Việt phải tìm cách phá vỡ hệ thố" | N2 ⚠️ mỗi lần gặp |
| 6 | mạnh mẽ | 1 | 1 | N2 | `lt1v6` đoạn 32074: "Dù câu chuyện được lưu truyền dưới hình thức nào, Nam quốc sơn hà đã trở thành biểu tượng mạnh mẽ về ý thức độ" | N2 ⚠️ mỗi lần gặp |
| 7 | rơi vào tay | 8 | 8 |  | `dbl1` đoạn 10084: "Đinh Toàn lên nối ngôi khi mới sáu tuổi. Quyền hành rơi vào tay Lê Hoàn, người giữ chức Thập đạo tướng quân." | N2 ⚠️ mỗi lần gặp |
| 8 | thất thủ | 4 | 4 | N2 | `v1` đoạn 1023: "Trong vài tháng, các quận huyện thất thủ, quan chức bỏ chạy. Cả triều đình hoảng, vì lần đầu thấy dân chúng có" | N2 ⚠️ mỗi lần gặp |
| 9 | điều đáng chú ý | 3 | 3 | N1 | `han2v6` đoạn 49018: "Điều đáng chú ý là người dân không chỉ lập đền thờ ông khi còn sống, mà nhiều gia đình sinh con trai còn đặt t" | N1 ❌ |
| 10 | có thể thấy | 2 | 2 | N1 | `hbt` đoạn 9110: "Có thể thấy họ không coi đây là một chuyến đi dạo." | N1 ❌ |
| 11 | không chỉ | 39 | 26 |  | `bm7` đoạn 116001: "Bạn có biết, ba mươi sáu phố phường của Hà Nội xưa kể về những nhóm thợ? Không chỉ về những con phố." | N2 ⚠️, chỉ khi dùng ≥3 lần/kịch bản |
| 12 | bảo toàn lực lượng | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 13 | được tổ chức | 2 | 2 |  | `han1` đoạn 41002: "Năm một trăm mười trước Công nguyên, nhà Hán thôn tính nước Nam Việt của họ Triệu. Sau đó, vùng đất này được t" | N2 ⚠️ mỗi lần gặp |
| 14 | câu trả lời nằm ở | 8 | 7 | N1 | `bd2` đoạn 173002: "Câu trả lời nằm ở cửa sông Bạch Đằng, nơi hai bên sắp gặp nhau trong một trận đánh quyết định." | Tạm ❌ (chờ xem cách dùng) |
| 15 | muốn trả lời | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 16 | coi chung | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 17 | núng thế | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 18 | sắm sửa | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 19 | dấy binh | 8 | 8 |  | `lh1` đoạn 11011: "Họ dấy binh, chia hai đường thủy bộ tiến về kinh đô để giết Lê Hoàn. Nhưng họ không đánh nổi." | N2 ⚠️, chỉ khi dùng ≥3 lần/kịch bản |
| 20 | đặt làm | 2 | 2 |  | `tn32` đoạn 160003: "Tên Tuyên Quang đã có từ rất sớm. Dưới thời vua Trần Hiến Tông, vùng này được đặt làm trấn Tuyên Quang." | N2 ⚠️ mỗi lần gặp |
| 21 | bên này | 2 | 1 |  | `tm2` đoạn 176015: "Còn bên này biên giới, giặc sắp tới mà vua mới sáu tuổi. Vậy ai sẽ cầm quân ra trận?" | N2 ⚠️ mỗi lần gặp |
| 22 | phía bên kia | 10 | 8 |  | `bd1` đoạn 170003: "Ở phía bên kia, Ngô Quyền có ít chiến thuyền hơn hẳn, và chính ông cũng biết rõ điều đó." | N2 ⚠️, chỉ khi dùng ≥3 lần/kịch bản |
| 23 | có thể hiểu vì sao | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 24 | kinh hoàng | 2 | 2 |  | `v2` đoạn 2060: "Quân Tào thắng lớn với quân ít. Tôn Quyền và cả đạo quân Ngô kinh hoàng trước sức một người, không ai dám chặn" | N2 ⚠️ mỗi lần gặp |
| 25 | khủng khiếp | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 26 | chấn động | 4 | 2 |  | `v2` đoạn 2089: "Quân Quan Vũ vây Phàn Thành. Cả thiên hạ chấn động. Có nơi ở phía bắc, người dân đã nổi dậy hưởng ứng ông. Tào" | N2 ⚠️ mỗi lần gặp |
| 27 | định mệnh | 1 | 1 | N2 | `ly1` đoạn 18004: "Vì cớ gì ngài lại quyết định rũ bỏ kinh đô cũ kiên cố, để dời ra vùng đất mới và dựng lên cánh cửa định mệnh n" | N2 ⚠️ mỗi lần gặp |
| 28 | không ai ngờ | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 29 | giữ trọn | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 30 | bài học | 14 | 7 | N2 | `ly1` đoạn 18053: "Hoàng đế chiêm nghiệm bài học từ hai triều đại đi trước." | N2 ⚠️, chỉ khi dùng ≥3 lần/kịch bản |
| 31 | tinh thần quân giặc | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 32 | cục diện | 0 | 0 | N2 | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 33 | trong khi chờ | 0 | 0 |  | (không có trong kịch bản nào) | N2 ⚠️ mỗi lần gặp |
| 34 | quân thuyền | 1 | 1 | N1 | `bd2` đoạn 173014: "Lưu Cung không nghe. Ông phong con trai làm Giao Vương và giao cho cầm quân thuyền sang trước." | N1 ❌ |

Ghi chú:
- "không chỉ" xuất hiện 39 lần trong 26 kịch bản, nhiều khả năng đa số là cách nói bình thường ("không chỉ A mà còn B"). Nên xem kỹ cụm này đầu tiên: nếu giữ ❌ thì phần lớn kịch bản cũ sẽ bị báo.
- "bài học" (14 lần/7 file), "phía bên kia" (10/8), "rơi vào tay" (8/8), "dấy binh" (8/8) cũng xuất hiện nhiều: cần anh quyết đây là từ đã chê thật hay chỉ chê một số cách dùng.
- 15 cụm chưa xuất hiện ở kịch bản nào: nếu chủ kênh chưa từng chê cụ thể, có thể giữ nguyên vì không tốn gì.
- Nếu cụm chuyển N2, nó vẫn in ra ở dạng ⚠️ cùng câu cảnh báo, không bị xóa.

