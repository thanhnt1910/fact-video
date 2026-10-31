# PERIOD BIBLE BỔ SUNG – Đại Việt nhà Lý và nhà Tống (0.1-DRAFT, 01/11/2026)

**Trạng thái: DRAFT, chờ chủ kênh duyệt.** File này KHÔNG sửa `period-ly-tong.md` (v1.3 APPROVED). Chỉ sau khi chủ kênh duyệt mới gộp thành phiên bản mới của Bible, giữ lịch sử phiên bản.

## A. Phạm vi niên đại của Bible hiện tại (v1.3)
- Phạm vi áp dụng đã xác định: **1075–1077** (chiến tranh Lý–Tống), phe Đại Việt nhà Lý và Bắc Tống (Quảng Tây).
- **1069–1105** chỉ là "tham chiếu thêm" (mục A của v1.3), KHÔNG được coi là đã kiểm. Nội dung ngoài 1075–1077 chưa xác nhận.
- Bible này KHÔNG mặc định áp dụng cho toàn bộ thời Lý, thế kỷ XII hay thời kỳ khác (Trần, Lê...).
- Khi dự án vượt phạm vi: AI đánh dấu `NEEDS_EXTENDED_RESEARCH`, không tự kế thừa chi tiết chưa xác nhận.
- Nguồn đã dùng ở v1.3: mục J của `period-ly-tong.md`. Bản bổ sung này chưa rà lại nguồn từng hàng; hàng nào chưa có nguồn gắn thời điểm thì chỉ áp dụng 1075–1077.

## B. Trạng thái kiểm chứng các hàng hiện có (đề xuất, không đổi nội dung v1.3)
| Nhóm hàng (v1.3) | Mức | Phạm vi niên đại | Trạng thái kiểm chứng |
|---|---|---|---|
| Kiến trúc cung điện (mục C) | A | 1075–1077 | Theo nguồn khảo cổ ở mục J; phạm vi rộng hơn chưa kiểm |
| Giáp sắt và da, vũ khí Đại Việt, giáp Tống, mũ sắt Tống, thành trì Tống, dốc đất | B | 1075–1077 | Gián tiếp (mục J), không có hiện vật trực tiếp đã kiểm |
| Quần áo, mũ, giày, nón lá, cờ, thuyền chiến, tướng lĩnh, Lý Thường Kiệt, màu quân phục Tống | C | 1075–1077 | KHÔNG có bằng chứng; quy ước hình ảnh |

## C. Ba hàng quy ước hình ảnh mới (mức C)
Ghi chú bắt buộc cho mọi hàng dưới đây: **"Quy ước hình ảnh đã được chủ kênh duyệt để tái sử dụng về mặt hình ảnh. Đây KHÔNG phải dữ kiện lịch sử đã xác minh; không dùng làm căn cứ khi viết lời đọc, mô tả video hoặc bình luận ghim."** (`tinh_chat = quy_uoc_hinh_anh`, `la_du_kien_lich_su = false`, `approval_scope = visual_only`).

| Hàng | Hướng thể hiện | evidence_level | Phạm vi | Trạng thái kiểm chứng | decision_mode | Chi tiết gốc (kế hoạch lt1v4) |
|---|---|---|---|---|---|---|
| **Dân thường và người hầu Đại Việt** | Áo vải thô, dài hoặc ngắn tùy việc, màu đất trầm; đầu trần hoặc khăn quấn; không hoa văn | C `artistic_choice` | Đại Việt, 1075–1077 | NEEDS_REVIEW: không có bằng chứng | OWNER_APPROVAL | AC02 (L05 người hầu), AC03 (L06 dân làng) |
| **Dân thường nhà Tống** | Áo vải thô màu đất hoặc xám, đầu trần hoặc khăn quấn; không hoa văn, không lụa sang | C `artistic_choice` | Bắc Tống (Quảng Tây), 1075–1077 | NEEDS_REVIEW: không có bằng chứng | OWNER_APPROVAL | AC09 (L13), AC12 (L21), AC20 (L33) |
| **Lều vải đơn giản của quân Tống** | Lều hoặc mái che bằng vải thô, không cờ, không họa tiết | C `artistic_choice` | Bắc Tống, 1075–1077 | NEEDS_REVIEW: không có bằng chứng | OWNER_APPROVAL | AC18 (L30) |

Hạn chế: không thêm chi tiết nào ngoài bảng; hàng chưa duyệt không được AUTO.

### Về hàng "dân thường nhà Tống" và cảnh L33 (đối chiếu theo yêu cầu chủ kênh)
- Kịch bản đoạn 58 nói trao trả **"dân và binh lính"** bị bắt ở Ung, Khâm, Liêm.
- Cảnh L33 hiện chỉ vẽ **10 người dân Tống** và **2 lính Đại Việt đi hộ tống** (lính Đại Việt dùng các khối Đại Việt đã có). **Không có binh lính Tống trong cảnh L33.**
- Vì cảnh chỉ có dân thường Tống nên AC20 gộp vào hàng "Dân thường nhà Tống". Nhãn của AC20 trong kế hoạch được sửa cho đúng ("dân Tống được trao trả").
- Câu hỏi mở cho chủ kênh: có muốn thể hiện cả binh lính Tống được trao trả không? Nếu có, phải thêm hàng riêng **"Binh lính nhà Tống được trao trả"** (C, OWNER_APPROVAL, chi tiết tù binh/quân phục chưa có căn cứ) và sửa Scene Planner; hiện KHÔNG tạo hàng này vì chưa có cảnh dùng.

## D. Cách xử lý khi dự án nằm ngoài phạm vi
| Tình huống | Chế độ |
|---|---|
| Thời kỳ mới chưa có Period Bible | `MUST_VERIFY` cho trang phục, giáp, vũ khí, kiến trúc, phương tiện, địa danh. Không kế thừa Bible Lý–Tống |
| Có Bible nhưng chi tiết chưa nằm trong đó, và là quy ước hình ảnh không mang khẳng định lịch sử (ví dụ bản đồ cuộn) | `OWNER_APPROVAL` |
| Chi tiết mang khẳng định lịch sử (thuyền, lũy, trang phục, kiến trúc) Bible chưa phủ | `MUST_VERIFY`; không tự chuyển thành C để né xác minh |
Chi tiết của từng quyết định (DQ-001 đến DQ-004) nằm trong `quyet-dinh.json`.

## E. Những điều AI không được tự ý thêm
Như v1.3 (mục B, C, D), cộng: không dùng hàng C ở đây làm căn cứ lịch sử; không áp cho thời kỳ ngoài 1075–1077.
