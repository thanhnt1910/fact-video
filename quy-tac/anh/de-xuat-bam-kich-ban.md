# Đề xuất: ảnh bám theo kịch bản (DRAFT 01/11/2026, CHỜ CHỦ KÊNH DUYỆT)

Tài liệu này KHÔNG sửa và không ghi đè `master-style.md`, `period-ly-tong.md`, `khoi-prompt.json`, `quy-trinh-anh.md`, `quyet-dinh.json` hay bộ kiểm. Mọi điểm dưới đây chỉ có hiệu lực sau khi chủ kênh duyệt từng điểm và được cập nhật trực tiếp vào tài liệu tương ứng.

Lý do (chủ kênh, 01/11/2026): ảnh không cần dựa quá nặng vào tài liệu sử ghi; ảnh phải bám theo kịch bản (lời kể). Thực tế: L04, L32, L33 đã vẽ hai lần đều hỏng vì cổng đếm người, voi và đồ hiện đại, không phải vì sai sử.

## Các điểm đề xuất
| # | Quy tắc hiện hành | Đề xuất | File phải sửa sau khi duyệt |
|---|---|---|---|
| 1 | Nội dung cảnh phải khớp tài liệu thời kỳ (Period Bible) và bằng chứng A/B/C | Nguồn chính của cảnh là lời kể trong đoạn: ai, làm gì, ở đâu, cảm xúc. Period Bible chỉ để tránh sai thời quá rõ (đồ hiện đại, cờ sao vàng, mũ cối, chữ), không để chặn cảnh | `quy-trinh-anh.md`, `period-ly-tong.md` (mục phạm vi) |
| 2 | Chi tiết mang khẳng định lịch sử (trang phục, thuyền, lũy, kiến trúc) là MUST_VERIFY | Mặc định AUTO nếu lời kể có nhắc; chỉ MUST_VERIFY khi ảnh là bằng chứng (bản đồ có tên, số liệu in trên hình). Trang phục, công trình vẽ theo mô tả kiểu \"minh họa\" | `quy-trinh-anh.md`, `quyet-dinh.json` |
| 3 | Bảy bản đồ M1–M7 bị chặn đến khi VERIFIED | Cho vẽ bản đồ minh họa theo lời kể, không chữ, ghi \"minh họa\" ở mô tả video; bản đồ có tên địa danh hoặc ranh giới chỉ dùng khi đã có nguồn | `quy-trinh-anh.md`, `kiem_scene_planner.py` (sau khi duyệt) |
| 4 | Đếm người, ngựa, voi theo Scene Planner là chặn | Số lượng do lời kể quyết định (\"năm con voi\" thì ảnh phải gần năm). Sai số cho phép với đám đông (nhiều hơn năm người): cộng trừ hai. Voi và nhân vật có tên: đủ đúng. Lệch trong sai số chỉ ghi cảnh báo | `quy-trinh-anh.md`, `khoi-prompt.json` |
| 5 | Giữ nguyên | Không chữ, không đồ hiện đại, không máu, một lần vẽ cộng ba lần vẽ lại rồi MANUAL_REVIEW, ảnh tham chiếu chỉ khi có trong danh sách được duyệt | không đổi |

## Prompt đề xuất cho lần vẽ thứ ba (chờ duyệt, chưa vẽ)
Lý do chung: giữ đúng ý lời kể, đổi bố cục để dễ đếm và bỏ yếu tố khiến máy thêm đồ hiện đại. Nếu duyệt thì cập nhật `scene-planner.json` (phiên bản, `prompt_sha256`) theo quy trình.

- **L04 (một vị tướng già xem bản đồ):** đổi nền thành \"a plain bare timber hall with thatched roof and packed earth floor covered by a woven mat; a single small clay oil dish holding a tiny flame; the general sits at a low wooden table with a hand-drawn rolled paper map without text; no glass, no metal fixtures, no wall sockets, no windows with panes, no lamps with shades\". Giữ mô tả ông (râu đen pha bạc, mặt nghiêng).
- **L32 (sứ đoàn dắt năm con voi):** \"wide shot of a dirt road, exactly five elephants walking left to right in single file with a clear gap between each elephant, one attendant on foot at the head of each elephant, one envoy in front; empty background\". Cảnh rộng, không chồng voi lên nhau.
- **L33 (dân bị bắt đem về):** giảm số để dễ đếm nhưng vẫn đúng ý lời kể \"bắt người đem về\": sáu dân thường (hai hàng, mỗi hàng ba), hai lính Tống không vũ khí đi cùng, hai lính Đại Việt cầm giáo ở cuối hàng, tổng mười người, góc rộng. (Đổi số từ mười bốn xuống mười: cần duyệt, vì AC22 đã duyệt bốn lính Tống.)

## Việc cần chủ kênh quyết
| # | Việc | Đề xuất |
|---|---|---|
| 1 | Duyệt từng điểm 1–4 trong bảng trên | Duyệt cả bốn; tôi mới cập nhật tài liệu APPROVED và bộ kiểm, rồi chạy `test_kiem_anh.py` và `so_sanh_baseline.py` |
| 2 | Duyệt prompt lần ba cho L04, L32, L33 | Duyệt, rồi tôi cập nhật Scene Planner và chạy workflow vẽ |
