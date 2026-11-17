# Khung kịch bản cố định của series thủy mặc (chủ kênh duyệt 17/11/2026)

> **Bài mẫu:** `quy-tac/thuy-mac-mau.md` (tm5 bản 9, chủ kênh duyệt 17/11/2026). Viết tập mới thì đặt từng nhịp cạnh bài mẫu để so.


Mọi tập đều viết theo một khung nhịp giống nhau, để điểm nhấn luôn nằm ở cùng chỗ và chủ kênh không phải duyệt lại bố cục mỗi lần. Khung này đứng trên các quy tắc lời kể ở `quy-tac/thuy-mac.md` mục 3. Hai file không mâu thuẫn: khung quyết định đoạn nào làm gì, mục 3 quyết định viết câu thế nào.

## 1. Khung nhịp

| Nhịp (mã) | Số đoạn | Mốc | Nhiệm vụ |
|---|---|---|---|
| Hook 1 (`hook1`) | 1 | 0% | **Ưu tiên một câu hỏi** (chủ kênh 17/11/2026: mở bằng câu hỏi thu hút hơn), có thể hỏi thẳng người nghe ("Nếu kẻ thù hứa cho bạn làm vương, chỉ cần bạn chịu hàng, bạn sẽ trả lời thế nào?"); không năm, không tên, tối đa 25 chữ; câu hỏi dẫn thẳng vào khoảnh khắc nguy nhất hoặc câu nói có thật ở hook 2 |
| Hook 2 (`hook2`) | 1 | | Lật lại câu 1 |
| Hook 3 (`hook3`) | 1 | | Tên người, tên nơi, hệ quả nói mạnh; tối đa 4 tên |
| Hook 4 (`hook4`) | 1 | ≤8% | Câu hỏi kèm lời hứa "N lần / N điều" (N = 2–4) |
| Gốc rễ (`goc_re`) | 3–5 | đến ~20% | Chuỗi nguyên nhân; đoạn sau là hệ quả của đoạn trước |
| Thế nguy (`the_nguy`) | 2–5 | | Giặc thắng dần |
| Điểm thấp nhất (`diem_thap`) | đúng 1 | ~35–40% | Lúc phe ta nguy nhất, kể bằng sự việc có nguồn |
| Bước ngoặt (`buoc_ngoat`) | 1–4 | ≤50% | Điều gì đổi chiều, có nguồn |
| Lần / trận (`lan1`, `lan2`…) | 1–5 mỗi lần | | Mỗi lần có bốn nhịp: thế nguy, chi tiết có nguồn, bước ngoặt, hệ quả đẩy sang lần sau. Lần sau lớn hơn lần trước |
| Đoạn lặng (`lang`) | đúng 1 nhịp | | Kể chậm ngay trước khoảnh khắc quyết định, có căn cứ ("Thủy triều vẫn đang lên…") |
| Cao trào (`cao_trao`) | 2–4 | 55–85% | Kể dồn |
| Chi tiết con người (`chi_tiet_nguoi`) | đúng 1 | | Một lời nói hoặc hành động có thật của một người, nằm trong khối cao trào |
| Dồn cuối (`don_cuoi`) | 1–3 | | Cuộc đuổi, cảnh tháo chạy, hoặc hệ quả gấp nhất |
| Kết (`ket`) | 1–2 | cuối | Trả lời câu hỏi ở hook; câu cuối quay về hình ảnh mở đầu và lời cảm ơn, tối đa 32 chữ |

- Ba nhịp `lang`, `cao_trao`, `chi_tiet_nguoi` là một khối liền nhau, thứ tự bên trong tự do.
- Phần sau khối cao trào (`don_cuoi` + `ket`) tối đa 5 đoạn.
- Tổng 24–42 đoạn.

## 1b. Câu hỏi xuyên suốt (sợi chỉ) — chống kể liệt kê (chủ kênh chê tm5 bản 6, 17/11/2026)
- Mỗi tập có **một câu hỏi kịch tính** mà người nghe giữ trong đầu từ hook tới cao trào (tm5: "hai đầu gọng kìm có gặp được nhau không?"). Khai báo trong khung: `cau_hoi`, `soi_chi` (các cụm chữ của câu hỏi).
- Hook 4 đặt câu hỏi ấy. Đoạn cuối của **bước ngoặt** và của **mỗi lần/trận** phải nói câu hỏi đang nghiêng về phía nào ("Đầu gọng kìm phía nam bị đánh bật lại"; "Thế là hai đầu gọng kìm đã bị chặt rời"). `kiem_khung.py` báo ❌ nếu thiếu.
- Sự việc nào không làm câu hỏi nghiêng đi thì bỏ hoặc gộp vào một vế câu (tm5 bản 7 đã bỏ chữ Sát Thát, Trần Kiện, tước phong của Trần Bình Trọng). Đặt hai người, hai lựa chọn cạnh nhau thay vì kể từng người (Trần Bình Trọng chọn làm quỷ nước Nam, Trần Ích Tắc chọn hàng giặc).
- Tổng số sự việc trong một tập nên khoảng 15–18; mỗi đoạn hoặc thêm một sự việc, hoặc nói sự việc vừa kể làm câu hỏi nghiêng về đâu.

## 2. Năm điểm nhấn cố định (tập nào cũng phải có)
1. Câu nói có thật hoặc khoảnh khắc nguy nhất ở hook.
2. Điểm thấp nhất.
3. Đoạn lặng ngay trước cao trào.
4. Chi tiết con người trong cao trào.
5. Câu kết quay về hình ảnh mở đầu. Hình ảnh xuyên suốt xuất hiện ít nhất 3 lần (hook, giữa, câu kết).

Thêm vào đó: N câu đếm khớp lời hứa ở hook 4, mỗi câu nói một kiểu.

## 3. Quy trình hai bước
1. **Bảng khung** `ke-hoach/thu-giong-hai/<mã>_khung.json`: mỗi nhịp một dòng, gồm sự việc, nguồn và số đoạn dự kiến; khai báo `n_hua`, `loi_hua`, `dem` (các câu đếm) và `hinh_anh` (cụm chữ của hình ảnh xuyên suốt). Chạy `python phim_ban_do/kiem_khung.py <mã>` cho tới khi 0 ❌, rồi gửi chủ kênh duyệt. Bảng khung chỉ một trang, chưa viết văn.
2. **Lời đọc**: viết đúng theo bảng khung đã duyệt. Mỗi đoạn trong `<mã>_full.json` có trường `"nhip"`. Chạy bốn bộ kiểm: `kiem_kich_ban.py`, `kiem_mach_ke.py`, `kiem_mo_dau.py`, `kiem_khung.py`; tất cả phải 0 ❌. Sau đó mới gửi hồ sơ gửi duyệt (mục 3.3 `thuy-mac.md`).

## 4. Bộ kiểm `kiem_khung.py`
Bộ kiểm báo các lỗi sau:
- thiếu nhịp bắt buộc; sai thứ tự; nhịp chỉ được có một mà bị lặp; khối cao trào bị cắt ngang;
- nhịp chưa ghi nguồn; số câu đếm khác lời hứa;
- phần sau cao trào dài quá 5 đoạn; cao trào lệch khỏi mốc 55–85% (cảnh báo);
- hình ảnh xuyên suốt dưới 3 lần, không có ở hook, hoặc không có ở câu kết;
- thiếu câu đếm; thiếu lời cảm ơn chuẩn;
- câu sáo, văn máy hoặc từ đã bị chủ kênh chê (danh sách `CAM`, thêm vào mỗi khi bị chê);
- nói tắt tên phe ("quân Nguyên", "quân Minh", "quân Tây Sơn"…).
