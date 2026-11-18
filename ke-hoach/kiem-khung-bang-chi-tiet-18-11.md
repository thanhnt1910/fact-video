# `kiem_khung.py`: bảng chi tiết từng mục để chủ kênh duyệt (18/11/2026)

**Trạng thái: ĐÃ DUYỆT VÀ ĐÃ SỬA (18/11/2026 tối).** Chủ kênh duyệt hạ cả 12 mục ⚠️ (mục 8 giữ cảnh báo, không mặc định cắt); B1, B2 giữ ❌; B3 bỏ hẳn; B5 sửa logic; hai thay đổi ở mục C duyệt; bảy mục ở mục D giữ nguyên, không revert. B4 chờ phân loại từng cụm (`kiem-khung-b4-34-cum-18-11.md`). Phần dưới giữ nguyên làm bản ghi.

Nguyên tắc dùng để đánh giá (của chủ kênh): công cụ kỹ thuật không được loại một kịch bản tốt chỉ vì nó không theo khuôn kể chuyện cứng; lỗi lịch sử, lỗi logic và lỗi kỹ thuật thật vẫn phải kiểm nghiêm túc.

## Hạ từ ❌ xuống ⚠️ sẽ thay đổi gì (chung cho mọi mục)
- Dòng báo vẫn in ra, đổi tiền tố thành ⚠️ và chuyển từ danh sách `loi` sang `canh`.
- Mã thoát (`return 1 if loi else 0`) chỉ còn 1 khi còn ❌ thật; kịch bản chỉ có ⚠️ thì thoát 0.
- `phim_ban_do/thuymac/tao_gui_duyet2.py` gọi `kiem_khung` và chép dòng tổng "-> N ❌, M ⚠️" vào hồ sơ gửi duyệt; số ❌ giảm, ⚠️ tăng. Chưa kiểm cách script ấy dùng mã thoát (chỉ đọc dòng tổng).
- Chủ kênh vẫn thấy từng dòng cảnh báo trong hồ sơ, nên không mất thông tin; chỉ không bị chặn "chưa nên gửi duyệt".

## A. 12 mục đề nghị hạ

| # | Dòng | Đang kiểm gì | Vì sao không còn phù hợp (bằng chứng) | Nếu hạ ⚠️ | Đề xuất |
|---|---|---|---|---|---|
| 1 | 37 | Tên nhịp ngoài danh sách 12 nhịp của khung (`nhịp lạ`) | Mạch truyện mới không bắt buộc đặt tên nhịp theo khung cũ; kịch bản dựng theo sự kiện sẽ luôn có nhịp "lạ" | Báo ⚠️ "nhịp lạ", không chặn | Hạ |
| 2 | 38–39 | Nhịp đứng sai thứ tự khung (ví dụ chi tiết con người trước cao trào) | Thứ tự do nguyên nhân – kết quả quyết định, không do khung | Báo ⚠️ sai thứ tự | Hạ |
| 3 | 40–41 | Thiếu một trong 13 nhịp bắt buộc | Chính chỗ này ép tập nào cũng có "Nhìn lúc ấy… tưởng như…" (nhịp điểm thấp bắt buộc); câu chuyện không có điểm thấp vẫn đúng và hay | Báo ⚠️ thiếu nhịp | Hạ |
| 4 | 44 | Khối cao trào (lặng, cao trào, chi tiết con người) bị cắt ngang | Cấu trúc khung thuần túy | ⚠️ | Hạ |
| 5 | 53–54 | Nhịp "một đoạn" (hook1–4, điểm thấp, lặng, chi tiết con người) có hơn một đoạn | Ép mỗi ý chỉ một đoạn, kể cả khi ý cần hai đoạn để hiểu | ⚠️ | Hạ |
| 6 | 59–60 | Số câu đếm khác số lời hứa N | Ép đủ câu đếm sinh ra "Thứ đầu tiên là… Thứ hai là…" (tm11–tm15) | ⚠️ | Hạ |
| 7 | 61 | Chưa khai báo hình ảnh xuyên suốt | Nguyên tắc cốt lõi đã hạ hình ảnh xuyên suốt xuống tham khảo | ⚠️ | Hạ |
| 8 | 69, 84–85 | Phần sau cao trào hơn 5 đoạn | tm14: luật này buộc cắt cảnh xử chém và gộp ba việc vào một đoạn; độ dài phần kết do câu chuyện quyết định | ⚠️ | Hạ |
| 9 | 78–79 | Lời đọc chưa viết đủ các nhịp của khung | Khung là tham khảo | ⚠️ | Hạ |
| 10 | 89–92 | Hình ảnh xuyên suốt không ở hook, không ở câu kết, hoặc dưới 3 lần | Ép gài chữ cho đủ số lần (tm14: phải có chữ "cỏ" ở hook) | ⚠️ | Hạ |
| 11 | 93–101 | Đoạn cuối của hook4, bước ngoặt, mỗi "lần" phải nhắc lại câu hỏi xuyên suốt (`soi_chi`) | Sinh đoạn giảng giải chỉ để có chữ "ghe" cuối nhịp (tm14 bản 2, đoạn 17) | ⚠️ | Hạ |
| 12 | 104–106 | Thân bài thiếu câu đếm đã khai báo | Câu đếm là tham khảo | ⚠️ | Hạ |

Lưu ý: mục 5 và 8 không chỉ là "khuôn kể chuyện". Mục 8 (phần sau cao trào quá dài) cũng bảo vệ người xem khỏi phần kết lê thê. Nếu hạ thì phần đó chỉ còn ⚠️; chủ kênh quyết có chấp nhận rủi ro đó không.

## B. Mục giữ ❌ hoặc cần chủ kênh quyết lại

| # | Dòng | Đang kiểm gì | Đề xuất |
|---|---|---|---|
| B1 | 55–56 | Nhịp chưa ghi sự việc | Giữ ❌ (mạch truyện phải dựng bằng sự việc) |
| B2 | 57–58 | Nhịp chưa ghi nguồn | Giữ ❌ (đúng sử là điều kiện bắt buộc) |
| **B3** | 107–108 | **Đoạn cuối thiếu đúng câu "Cảm ơn bạn đã lắng nghe câu chuyện này."** | **Trái quyết định 18/11 tối (không mặc định lời cảm ơn). Đề nghị BỎ kiểm này (hoặc ⚠️ nhắc nhẹ), không giữ ❌.** |
| B4 | 112–114 (`CAM`) | Câu sáo, từ dịch sát, từ chủ kênh đã chê, báo ❌ | Danh sách 34 cụm. Một số là từ lịch sử bình thường nếu dùng đúng chỗ: "cục diện", "bài học", "thất thủ", "định mệnh", "quyết liệt", "mạnh mẽ". Đề xuất: giữ ❌ cho cụm chủ kênh đã chê rõ ràng (ví dụ "có thể thấy", "điều đáng chú ý", "câu trả lời nằm ở", "muốn trả lời", "quân thuyền"), hạ ⚠️ cho cụm có thể đúng ngữ cảnh. Cần chủ kênh đánh dấu cụm nào thuộc nhóm nào |
| B5 | 115–116 (`TAT`) | Nói tắt "quân Nguyên", "quân Minh"… | Giữ ❌ (rõ ràng, sửa nhanh, không ảnh hưởng mạch) |

## C. Hai thay đổi cùng đợt (không đổi mức ❌/⚠️ của quy tắc nào)
1. Thiếu file `<mã>_khung.json` thì bỏ qua phần khung, chỉ chạy kiểm câu chữ (`CAM`, `TAT`) và kiểm B1–B2 nếu có sự việc. Hiện bộ kiểm dừng vì lỗi đọc file.
2. Khung không khai báo `n_hua`, `dem`, `hinh_anh`, `soi_chi` thì bỏ qua các kiểm 6, 7, 10, 11, 12, không báo gì.

## D. Việc mình đã làm trước khi có bảng này (cần anh biết)
Ở lượt trước, theo bước "rà bộ kiểm" trong kế hoạch của anh, mình đã hạ 7 mục ❌ → ⚠️ ở ba bộ kiểm KHÁC, trước khi lập bảng chi tiết cho chúng:
| Bộ kiểm | Mục đã hạ | Lý do |
|---|---|---|
| `kiem_mo_dau.py` | 25 giây đầu có từ 2 mốc năm/trích nguồn trở lên | Công thức hook của loạt Bí mật biểu tượng, không phải lỗi thật |
| `kiem_mo_dau.py` | Đoạn 2 có năm hoặc trích nguồn | Như trên |
| `kiem_mach_ke.py` | Hook quá dài (>25 chữ) hoặc có năm | Khung hook |
| `kiem_mach_ke.py` | Hai đoạn liền nhau cùng chữ mở đầu | Đếm số, văn phong |
| `kiem_giong_van.py` | Cụm lặp quá số lần | Đếm số, văn phong |
| `kiem_giong_van.py` | Động từ tóm lược quá 3 lần | Đếm số, văn phong |
| `kiem_giong_van.py` | Khối cao trào thiếu câu ngắn dưới 8 chữ | Khung |

Không đụng `kiem_kich_ban.py` (đúng quy định 01/11: giữ 32 chữ, 2 câu). Nếu anh không đồng ý bất kỳ mục nào ở bảng trên, mình hoàn lại đúng mục đó bằng `git revert` hoặc sửa tay; commit chứa thay đổi là `f4dac5e5`.

## E. Cần chủ kênh trả lời
Với từng dòng trong bảng A: **Hạ / Giữ ❌ / Bỏ hẳn**. Với B3: bỏ hay ⚠️. Với B4: danh sách cụm giữ ❌.
