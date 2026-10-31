# CHANGELOG quy chuẩn ảnh

## 01/11/2026, chủ kênh duyệt năm mục (quy trình ảnh v1.3, DQ-001..005, râu S2, L33, danh sách bản đồ)
- **Duyệt mục 5 của `quy-trinh-anh.md`:** nâng quy trình v1.2 → **v1.3 APPROVED**. Năm quy tắc QK-VOI, QK-BANDO, QK-DOAN, QK-GIULAU, QK-DUYET-NT chuyển PROPOSED → **APPROVED, chặn** (hết Cách B). QK-HOSO không thuộc mục 5 nên vẫn PROPOSED (cảnh báo). Retry, MANUAL_REVIEW, owner_unlock không đổi.
- **Duyệt DQ-001..DQ-004** (APPROVED, vẫn C, `visual_only`, OWNER_APPROVAL, chưa AUTO) và **21 chi tiết AC01–AC21** (vẫn C, không thành dữ kiện lịch sử).
- **Thêm DQ-005:** râu Lý Thường Kiệt giai đoạn S2 (1075–1077) = **đen pha bạc** (phương án B2), C, `visual_only`, phạm vi CHARACTER (`nhan_vat` + `giai_doan`). S1, S3, S4 và Tông Đản vẫn UNDECIDED. L04 và L11 (cảnh thấy mặt) thay khối `VN_TUONG_LY_THUONG_KIET` (cụm "grey beard" trong khối APPROVED, KHÔNG sửa) bằng câu râu đen pha bạc trong prompt (AC23, AC24).
- **L33:** thêm 4 lính Tống được trao trả, không vũ khí (chủ kênh trả lời "Có"): 8 dân + 4 lính Tống + 2 lính Đại Việt = 14 người. Chi tiết AC22 CHƯA duyệt. Bible bổ sung có hàng riêng.
- **Bản đồ:** chủ kênh duyệt danh sách 33 mục cần xác minh làm kế hoạch; mọi mục vẫn NEEDS_REVIEW, chưa nguồn, chưa tọa độ; 7 bản đồ vẫn bị chặn.
- Bộ kiểm: phạm vi CHARACTER trong `dq_hop_le` và `kiem_registry`. Test 120/120. So sánh baseline: `baseline_kiem/so_sanh_sau_duyet_2026-11-01.txt`; SHA mới của quy-trinh-anh.md ở `baseline_kiem/sau_duyet_2026-11-01.json` (baseline b0/b1 giữ nguyên).
- Không đổi: `master-style.md` v1.3, `period-ly-tong.md` v1.3, `khoi-prompt.json` v1.3, `bible_versions` lt1v4 (1.3). Planner vẫn PLAN_OWNER_REVIEW; danh sách ảnh tham chiếu được duyệt vẫn rỗng.

## 01/11/2026, triển khai kiến trúc 4 tầng (DRAFT, theo chủ kênh duyệt phương án; KHÔNG đổi tài liệu APPROVED)
- Mới (DRAFT): `quyet-dinh.json` (Decision Registry 0.1: DQ-001 đến DQ-004 đều PROPOSED/C/OWNER_APPROVAL; nguyên tắc NT-01..06 do chủ kênh duyệt; trạng thái các quy tắc kiểm QK-*), `nhan-vat/ly-thuong-kiet.json`, `nhan-vat/tong-dan.json` (nhiều giai đoạn, râu UNDECIDED, ảnh tham chiếu đã duyệt: rỗng), `period-ly-tong-bo-sung.md` (phạm vi niên đại 1075–1077, 3 hàng quy ước hình ảnh C: dân thường Đại Việt, dân thường nhà Tống, lều vải quân Tống).
- Bộ kiểm `kiem_scene_planner.py`: 26 quy tắc thêm sau ngày duyệt (voi, bản đồ, đoạn, giữ lâu, duyệt nghệ thuật) chuyển sang CẢNH BÁO (Cách B) cho tới khi duyệt mục 5 của `quy-trinh-anh.md`; thêm `kiem_registry`, kiểm phạm vi và AUTO, cổng `cong_san_xuat` (`--cong`). Retry, MANUAL_REVIEW, owner_unlock và quy tắc cũ không đổi.
- Test 107 phép (44 gốc + 26 quy tắc mới đã chỉnh sang cảnh báo + 37 phép cho cổng, phạm vi, AUTO, registry, hồ sơ nhân vật, tài liệu APPROVED). So sánh trước/sau: `phim_ban_do/baseline_kiem/so_sanh_sau_khi_sua.txt`.
- Scene Planner lt1v4 (vẫn PLAN_OWNER_REVIEW, bible_versions 1.3): thêm `quyet_dinh_ap_dung`, `nien_dai_canh`, `decision_mode`; nhãn AC20 (L33) sửa thành "dân Tống được trao trả" vì cảnh chỉ vẽ dân.
- Baseline chỉ đọc: `phim_ban_do/baseline_kiem/` và hai tag git riêng.

## 01/11/2026, bổ sung theo yêu cầu chủ kênh sau khi xem Scene Planner (CHỜ DUYỆT, không đổi số phiên bản APPROVED)
- `quy-trinh-anh.md`: thêm mục 5 (kiểm voi, dữ liệu bản đồ, `segment_cuts`, `motion_plan`, duyệt chi tiết nghệ thuật chỉ ở phạm vi hình ảnh).
- `kiem_scene_planner.py`, `test_kiem_anh.py` (70 phép kiểm): voi, bản đồ, đoạn nhiều cảnh, cảnh giữ lâu, duyệt chi tiết nghệ thuật.

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
