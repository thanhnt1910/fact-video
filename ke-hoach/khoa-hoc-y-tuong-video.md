# Ý tưởng video khoa học dọc 9:16 (kênh Người Giải Mã, nhánh `khoa-hoc`)

Series: **"Người xưa đo bằng cách nào?"** Tiếng Việt, giọng Leda, người que đội mũ, dựng bằng Remotion.
Cập nhật 10/11/2026 (thay bản cũ viết cho kênh tiếng Anh, 60–75 giây).

## Mạch chung của mỗi video

Độ dài tùy chủ đề: đủ để người xem hiểu, không độn, không cắt mất bước giải thích. Mỗi video đi qua năm chặng, chặng sau trả lời câu hỏi mà chặng trước gợi ra:

| Chặng | Nội dung | Hình |
|---|---|---|
| 1. Câu hỏi | Một điều tưởng không thể đo, hỏi thẳng "làm sao biết?" | Vật cần đo, dấu hỏi, nhân vật ngước nhìn |
| 2. Cách cũ không đủ | Người xưa thử cách sẵn có và VÌ SAO nó không đủ | Nhân vật thử, thất bại |
| 3. Ý tưởng mới | Giải thích bằng một ví dụ nhìn thấy được, so với vật quen | Sơ đồ chuyển động |
| 4. Tính ra con số | Công thức thật, tính từng bước, mỗi câu một phép tính | Phép tính hiện từng bước |
| 5. Ngày nay | Ý đó đang dùng vào đâu, rồi quay lại câu hỏi mở đầu | Cảnh đời thường |

Cách giải thích cho dễ hiểu:
- Mỗi ý khó đi kèm một ví dụ hoặc phép so sánh với vật quen: "13 mi-li-lít, gần bằng một muỗng canh", "100 hồng cầu xếp hàng dài bằng một hạt cát".
- Nói bằng hình ảnh, không nói bằng thuật ngữ: "bóng của cây gậy lệch đi một chút" thay cho "góc lệch 1/50 vòng tròn". Thuật ngữ bắt buộc thì giải thích ngay trong câu.
- Số dài để hiện trên màn hình; lời đọc làm tròn ("hơn một trăm nghìn").
- Điều là giai thoại hoặc hình minh họa thì nói rõ.

## Đã làm

| Video | Chủ đề | Thư mục dựng |
|---|---|---|
| 1 | Eratosthenes đo Trái Đất bằng một cây gậy | `remotion/src/eratosthenes/` |
| 2 | Cân Trái Đất (Cavendish) | `remotion/src/cavendish/` |
| 3 | Đo tốc độ ánh sáng | `remotion/src/anhsang/` |
| 4 | Kinh độ và đồng hồ của Harrison | `remotion/src/kinhdo/` |
| 5 | Đáy biển sâu bao nhiêu (tiếng vang) | `remotion/src/daybien/` |
| 6 | Vương miện vàng hay bạc (Ác-si-mét) | `remotion/src/vuongmien/` |
| 7 | Đếm thứ nhỏ hơn mắt (kính hiển vi, hạt cát) | `remotion/src/kinhhienvi/` |

## Đã có kịch bản, chưa dựng

| Video | Chủ đề | Kịch bản |
|---|---|---|
| 8 | Ngôi sao xa bao nhiêu (thị sai, Bessel) | `ke-hoach/khoa-hoc-video-8-khoang-cach-sao-kich-ban.md` |
| 9 | Sấm chớp và tốc độ âm thanh | `ke-hoach/khoa-hoc-video-9-toc-do-am-thanh-kich-ban.md` |
| 10 | Mặt Trời xa hơn Mặt Trăng bao nhiêu lần (Aristarchus) | `ke-hoach/khoa-hoc-video-10-mat-troi-mat-trang-kich-ban.md` |
| 11 | Nhiệt kế, độ C và độ F | `ke-hoach/khoa-hoc-video-11-nhiet-ke-kich-ban.md` |
| 12 | Đồng hồ quả lắc (Galileo, Huygens) | `ke-hoach/khoa-hoc-video-12-dong-ho-qua-lac-kich-ban.md` |

## Chưa làm

Các mốc dưới đây mới là điều đã biết, chưa đối chiếu nguồn gốc. Khi viết kịch bản, Claude tự tra nguồn từng chi tiết trước khi gửi.

1. **Mặt Trời xa hơn Mặt Trăng bao nhiêu lần?** (Aristarchus). Cách làm đúng nhưng ra số sai: đo góc lúc Mặt Trăng sáng đúng một nửa, ra khoảng 18–20 lần, thật ra khoảng 390 lần vì góc quá khó đo. Ví dụ đời thường: chỉ lệch một chút khi ngắm là kết quả sai rất xa.
2. **Đo thời gian khi chưa có đồng hồ.** Đồng hồ nước, đồng hồ mặt trời hỏng khi đêm, mây, đông giá. Ý mới: quả lắc (Huygens, 1656), rồi thạch anh, rồi nguyên tử. Ngày nay: điện thoại biết giờ chính xác.
3. **Núi cao bao nhiêu khi chưa ai lên tới đỉnh?** Đo từ xa bằng góc ngắm và khoảng cách (Everest, 1856). Ví dụ: đo chiều cao cái cây bằng bóng của nó.
4. **Ngôi sao gần nhất xa bao nhiêu?** Đưa ngón tay ra trước mặt, nhắm từng mắt thì ngón tay "nhảy": người ta dùng đúng cách ấy với hai vị trí của Trái Đất cách nhau nửa năm (Bessel, 1838).
5. **Nóng bao nhiêu là "nóng"?** Trước khi có nhiệt kế, không ai so được hôm nay nóng hơn hôm qua bao nhiêu. Chất lỏng nở ra khi nóng, và chuyện chọn hai mốc nước đá, nước sôi.
6. **Âm thanh chạy nhanh bao nhiêu?** Thấy chớp trước, nghe sấm sau. Người xưa bắn đại bác ở xa, đếm thời gian từ lúc thấy lửa đến lúc nghe tiếng.
7. **Trái Đất bao nhiêu tuổi?** Từ đoán theo sách, theo độ mặn của biển, đến "đồng hồ" trong đá: chất phóng xạ tan dần đều đặn.

Thứ tự đề xuất: 4 (ví dụ ngón tay ai cũng thử được ngay), 6 (sấm chớp rất đời thường), rồi 1.

## Khi làm một video mới
- Kịch bản: theo skill `viet-kich-ban-khoa-hoc`, ghi vào `ke-hoach/khoa-hoc-video-N-<tên>-kich-ban.md`.
- Dựng: thêm `remotion/src/<tên>/` theo mẫu `remotion/src/vuongmien/` (content.ts, Bg.tsx, scenes.tsx, sfx.ts).
- Không đọc giọng, không dựng khi chủ kênh chưa yêu cầu.
