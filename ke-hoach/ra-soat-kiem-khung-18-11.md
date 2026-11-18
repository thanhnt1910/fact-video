# Rà soát `phim_ban_do/kiem_khung.py` theo nguyên tắc cốt lõi (18/11/2026)

Chưa sửa file. Chờ chủ kênh duyệt danh sách này.

## A. Đề nghị hạ ❌ xuống ⚠️ (quy tắc cấu trúc nay là tham khảo)

| # | Vị trí | Điều kiện đang báo ❌ | Lý do hạ |
|---|---|---|---|
| 1 | dòng 37 (`kiem_thu_tu`), khung và lời đọc | Nhịp có tên ngoài danh sách khung (`nhịp lạ`) | Khung nhịp là tham khảo; mạch truyện mới không phải dùng đúng tên nhịp cũ |
| 2 | dòng 38–39 | Nhịp đứng sai thứ tự khung (ví dụ chi tiết con người trước cao trào) | Thứ tự do mạch truyện quyết định, không do khung |
| 3 | dòng 40–41 | Thiếu một trong 13 nhịp bắt buộc (hook1–hook4, gốc rễ, thế nguy, điểm thấp, bước ngoặt, lặng, cao trào, chi tiết con người, dồn cuối, kết) | Đây chính là chỗ ép câu chuyện vào khuôn: tập nào cũng có "Nhìn lúc ấy… tưởng như…" vì nhịp điểm thấp bắt buộc |
| 4 | dòng 44 | Khối cao trào (lặng, cao trào, chi tiết con người) bị cắt ngang | Cấu trúc khung |
| 5 | dòng 53–54 | Các nhịp "một đoạn" (hook1–4, điểm thấp, lặng, chi tiết con người) có hơn một đoạn | Cấu trúc khung |
| 6 | dòng 59–60 | Số câu đếm khác số lời hứa N (`dem` ≠ `n_hua`) | Câu đếm nay là tham khảo; ép đủ câu đếm sinh ra "Thứ đầu tiên là… Thứ hai là…" (tm11–tm15) |
| 7 | dòng 61 | Chưa khai báo hình ảnh xuyên suốt | Hình ảnh xuyên suốt nay là tham khảo |
| 8 | dòng 69 và 84–85 | Phần sau cao trào hơn 5 đoạn | Ở tm14, luật này buộc cắt ngày bị xử chém và gộp ba việc vào một đoạn; độ dài phần kết do câu chuyện quyết định |
| 9 | dòng 78–79 | Lời đọc chưa viết đủ các nhịp của khung | Khung là tham khảo |
| 10 | dòng 89–92 | Hình ảnh xuyên suốt không có ở hook, không có ở câu kết, hoặc xuất hiện dưới 3 lần | Ép gài chữ cho đủ số lần (ví dụ phải có chữ "cỏ" trong hook tm14) |
| 11 | dòng 93–101 | Đoạn cuối của hook4, bước ngoặt và mỗi "lần" không nhắc lại câu hỏi xuyên suốt (`soi_chi`) | Sinh ra đoạn giảng giải chỉ để có chữ "ghe" ở cuối nhịp (tm14 bản 2, đoạn 17) |
| 12 | dòng 104–106 | Thân bài thiếu câu đếm đã khai báo | Câu đếm là tham khảo |

Đề nghị thêm, cùng một đợt sửa:
- Khi không có file `<mã>_khung.json` (quy trình mới không bắt buộc lập khung), bộ kiểm không được dừng vì lỗi đọc file. Nó bỏ qua phần khung và chỉ chạy các kiểm ở mục B.
- Khi khung không khai báo `n_hua`, `dem`, `hinh_anh`, `soi_chi` thì bỏ qua các kiểm 6, 7, 10, 11, 12, không cảnh báo.
- Ba cảnh báo ⚠️ cũ giữ nguyên ⚠️: số đoạn ngoài 24–42 (dòng 66), bước ngoặt sau mốc 50% (dòng 67), cao trào ngoài mốc 55–85% (dòng 68, 86).

## B. Đề nghị giữ nguyên ❌

| # | Vị trí | Điều kiện | Lý do giữ |
|---|---|---|---|
| 1 | dòng 55–56 | Nhịp trong khung (hoặc mạch truyện) chưa ghi sự việc | Mạch truyện phải dựng bằng sự việc |
| 2 | dòng 57–58 | Nhịp chưa ghi nguồn | Đúng sử là điều kiện bắt buộc |
| 3 | dòng 107–108 | Đoạn cuối thiếu lời cảm ơn chuẩn | Giới hạn kỹ thuật và quy tắc chung (`chung.md`, mục "Câu kết cuối video") |
| 4 | dòng 112–114 (`CAM`) | Câu sáo, từ dịch sát, từ chủ kênh đã chê | Đúng tinh thần văn phong tự nhiên của nguyên tắc cốt lõi |
| 5 | dòng 115–116 (`TAT`) | Nói tắt "quân Nguyên", "quân Minh"… | Quy tắc chung "quân nhà X" |

## C. Các bộ kiểm khác (ngoài phạm vi yêu cầu, chỉ ghi để chủ kênh biết)
- `kiem_kich_ban.py`: 32 chữ, 2 câu mỗi đoạn, câu cụt, mệnh đề chen, nói tắt. Là giới hạn kỹ thuật, giữ.
- `kiem_mo_dau.py`, `kiem_mach_ke.py`, `kiem_giong_van.py`: có một số kiểm mang tính công thức (số tên riêng trong 25 giây đầu, hai đoạn liền nhau cùng chữ mở đầu, độ lệch nhịp câu). Nếu chủ kênh muốn, sẽ rà riêng theo cùng cách.
