# CHANGELOG quy chuẩn ảnh

## 01/11/2026, DUYỆT (APPROVED) theo chỉ thị của chủ kênh sau kiểm cuối
Điều kiện bắt buộc (5 phép kiểm, 44 trường hợp thử qua `python phim_ban_do/test_kiem_anh.py`) đều đạt.
| Tài liệu | Phiên bản APPROVED | Ngày duyệt | Thay đổi so với bản chủ kênh đã xem |
|---|---|---|---|
| `master-style.md` | **v1.3** | 01/11/2026 | Thêm: ảnh tham chiếu chỉ lấy từ `tham-chieu-duoc-duyet.json` |
| `period-ly-tong.md` | **v1.3** | 01/11/2026 | Không đổi nội dung, chỉ đổi trạng thái |
| `khoi-prompt.json` | **v1.3** | 01/11/2026 | Không đổi nội dung, chỉ đổi trạng thái |
| `quy-trinh-anh.md` | **v1.2** | 01/11/2026 | Thêm: `horses` và `mounted` trong `groups`, `dem_thu_cong` và `ke_hoach` tách riêng, danh sách tham chiếu duyệt, chặn vẽ quá lượt bằng mã |
Mã mới hoặc sửa: `phim_ban_do/anh_quy_tac.py` (mới), `phim_ban_do/kiem_scene_planner.py` (viết lại), `phim_ban_do/test_kiem_anh.py` (mới), `cf_ve_lt1t2.py` (chặn ảnh tham chiếu chưa duyệt), `ke-hoach/anh/lt1v4/tham-chieu-duoc-duyet.json` (mới, rỗng), `ke-hoach/anh/lt1v4/anh.json` (thêm trường), `assets/anh_chibi/*/KHONG_DUNG_LAM_THAM_CHIEU.md` (6 thư mục).
Việc KHÔNG làm theo chỉ thị: chưa lập Scene Planner 68 đoạn, chưa tạo hay vẽ lại ảnh, chưa đọc giọng. Chờ chủ kênh xác nhận bước tiếp theo.

## 01/11/2026, đợt 2 (theo yêu cầu chủ kênh; DRAFT, chưa APPROVED)
- `master-style.md` v1.1 → **v1.2-DRAFT**: ba mức bằng chứng giữ riêng (A `historical_evidence`, B `cautious_reconstruction`, C `artistic_choice`); thêm trạng thái ảnh `MANUAL_REVIEW`; giới hạn vẽ lại (3 lần tự động rồi `MANUAL_REVIEW`, không đổi lịch sử hay tiêu chuẩn để ép PASS); kiểm số người và ngựa bằng người; ảnh vẽ trước Bible hiện hành không dùng làm căn cứ.
- `period-ly-tong.md` v1.2 → **v1.3-DRAFT**: bỏ việc gộp A/B. Các dòng "A/B" (giáp vảy, mũ sắt, vũ khí Tống) ghi **B** vì chưa kiểm được nguồn khảo cổ trực tiếp; dốc đất: sự kiện theo sử liệu, hình ảnh B; chỉ kiến trúc cung điện giữ **A**.
- `khoi-prompt.json` v1.2 → **v1.3-DRAFT**: `tag` đổi thành `historical_evidence` / `cautious_reconstruction` / `artistic_choice` / `style_rule`; thêm `evidence_level` gốc (A/B/C) cho từng khối; `DOC_DAT` từ A thành B.
- `quy-trinh-anh.md` v1.0 → **v1.1-DRAFT**: Scene Planner bắt buộc khai `expected_people`, `expected_horses`, `main_characters`, `positions`, `groups` (tổng `count` = `expected_people`); `detail_tags` có `evidence_level`; giới hạn vẽ lại và `MANUAL_REVIEW`; `dem_thu_cong`.
- `kiem_scene_planner.py`: kiểm `groups`, `main_characters`, `positions`, `evidence_level` không bị đổi, nhãn mới.
- `CLAUDE.md`: thêm mục "Ảnh Lý Thường Kiệt v4" (chuyển sang tranh bán hiện thực FLUX.2 klein, chỉ áp dụng cho lt1 v4); đánh dấu DEPRECATED (giữ nguyên nội dung, không xóa) mục chibi lt1 và mục ảnh phẳng lt1.
- Kaggle: hủy lượt vẽ 6 ảnh thử bằng prompt cũ (run 41221199148); không dùng kết quả cũ làm căn cứ.

## 01/11/2026 (đề xuất, chờ chủ kênh duyệt, chưa APPROVED)
- `master-style.md` v1.0 → **v1.1-DRAFT**: sửa định nghĩa mức C theo nhãn; thêm mục 7 "không tự suy diễn"; thêm mục kiểm thứ 8 (chi tiết ngoài `detail_tags`); viết lại mục ảnh tham chiếu klein (cách gọi, nguy cơ sao chép bố cục, quy tắc dùng); ghi 19901 không còn hợp lệ làm tham chiếu.
- `period-ly-tong.md` v1.0 → v1.1 (phục dựng thận trọng theo quyết định chủ kênh) → **v1.2-DRAFT** (không có "không nhãn", gộp A/B thành `cautious_reconstruction`, bảng ánh xạ dòng sang khối).
- `khoi-prompt.json` v1.0 → v1.1 → **v1.2-DRAFT**: thêm `bible_ref` cho mọi khối, chuẩn hóa `tag` (chỉ A, cautious_reconstruction, artistic_choice), thêm nguyên tắc.
- `quy-trinh-anh.md` **v1.0-DRAFT** (mới): lưu và truy vết `detail_tags`, kiểm duyệt Scene Planner, quản lý phiên bản.
- Thêm `phim_ban_do/kiem_scene_planner.py` và sổ ảnh `ke-hoach/anh/lt1v4/anh.json` (ghi 24 ảnh thử cũ, đều `STALE`).
