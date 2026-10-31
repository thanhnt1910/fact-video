# Scene Planner lt1v4 — bảng chủ kênh duyệt (PLAN_OWNER_REVIEW)

Bible: master 1.3, period 1.3, khoi-prompt 1.3. 42 cảnh = 35 ảnh FLUX + 7 bản đồ vector. Phủ đủ đoạn 1–68. Chưa vẽ ảnh, chưa đọc giọng. Ảnh tham chiếu: không có (danh sách duyệt rỗng).

| Cảnh | Đoạn | Loại | Người/Ngựa | Nhân vật chính | Nhóm (vị trí) | Rủi ro | Chi tiết chờ duyệt (C/B ngoài khối) |
|---|---|---|---|---|---|---|---|
| L01 | [1, 26] | fortress | 6/0 | thành Ung Châu | lính Tống trên đầu tường ×6 (trung cảnh, rải đều trên đầu tường) | Low | - |
| L02 | [2, 27] | portrait | 3/0 | Tô Giám (không có chân dung; tạo hình nghệ thuật) | sĩ quan Tống (tri châu Tô Giám, tạo hình nghệ thuật) ×1 (tiền cảnh trái, nhìn từ phía sau); lính Tống ×2 (trung cảnh, sau sĩ quan vài bước) | Low | - |
| L03 | [3, 66] | army | 16/0 | đoàn quân Đại Việt | lính Đại Việt tiền cảnh ×3 (tiền cảnh); lính Đại Việt trung cảnh ×7 (trung cảnh); lính Đại Việt hậu cảnh ×6 (hậu cảnh, nhỏ) | Medium | - |
| L04 | [4, 5, 60] | command_room | 1/0 | Lý Thường Kiệt | Lý Thường Kiệt (tạo hình nghệ thuật) ×1 (giữa khung, nhìn từ phía sau và hơi nghiêng) | Medium | bản đồ cuộn không chữ |
| L05 | [6] | architecture | 3/0 | kinh thành Thăng Long | người hầu trong cung ×3 (tiền cảnh dưới, nhỏ) | Low | người hầu trong cung mặc áo dài thô, đầu trần |
| L06 | [7] | small_group | 8/0 | Lý Thường Kiệt thời trung niên (chưa có Character Reference) | quan Đại Việt (Lý Thường Kiệt thời trẻ hơn, tạo hình nghệ thuật) ×1 (giữa đường); tùy tùng ×3 (sau quan); dân làng ×4 (bên phải, làm ruộng) | Low | dân làng mặc áo thô, đầu trần hoặc khăn quấn; quan ở độ tuổi trung niên |
| L07 | [8, 63] | army | 12/0 | đạo quân tiên phong | lính Đại Việt tiên phong tiền cảnh ×4 (tiền cảnh); lính Đại Việt phía sau ×8 (trung cảnh) | Medium | - |
| L08 | [9, 17, 18] | small_group | 3/0 | Lý Thường Kiệt | Lý Thường Kiệt (tạo hình nghệ thuật) ×1 (tiền cảnh, nhìn từ phía sau); lính Đại Việt ×2 (sau tướng vài bước) | Low | - |
| L09 | [10] | object_detail | 0/0 | không có người | (không có người) ×0 (-) | Low | bàn gỗ, giấy cuộn, nghiên mực và bút lông |
| M1 | [11] | bản đồ SVG | - | - | Vị trí Quế Châu sát biên giới, hai mũi tên cử Thẩm Khởi và Lưu Di từ phía Tống tới. Chỉ dựa trên kịch bản. | - | cần dữ liệu địa lý |
| L10 | [12, 22, 23] | small_group | 8/0 | xưởng đóng thuyền của quân Tống | lính Tống ở xưởng thuyền ×8 (tiền cảnh 4, gần thân thuyền 4) | Medium | thân thuyền gỗ đang đóng trên giá đỡ |
| L11 | [13, 50, 51] | command_room | 4/0 | Lý Thường Kiệt | Lý Thường Kiệt (tạo hình nghệ thuật) ×1 (đầu bàn phía xa, ba phần tư); sĩ quan Đại Việt ×3 (hai bên và đầu bàn gần) | Medium | bản đồ cuộn không chữ |
| L12 | [14] | army | 14/0 | Lý Thường Kiệt, Tông Đản | tướng Đại Việt (Lý Thường Kiệt) ×1 (tiền cảnh trái, từ phía sau); tướng Đại Việt (Tông Đản, tạo hình nghệ thuật) ×1 (tiền cảnh phải, từ phía sau); lính Đại Việt ×12 (trung cảnh, hai hàng sáu người) | Medium | Tông Đản trẻ hơn Lý Thường Kiệt, râu đen ngắn |
| L13 | [15, 16] | small_group | 6/0 | nông dân nhà Tống | nông dân Tống ×3 (tiền cảnh); nông dân Tống ×3 (trung cảnh) | Low | nông dân Tống áo thô, đầu trần hoặc khăn quấn |
| M2 | [19] | bản đồ SVG | - | - | Hai đạo thủy bộ: đạo thủy (Lý Thường Kiệt) đi dọc biển tới Khâm Châu và Liêm Châu; đạo bộ (Tông Đản) đi thẳng tới Ung Châu. Không ghi số quân trên bản đồ (kịch bản có nói hơn mười vạn người, cần nêu nguồn). | - | cần dữ liệu địa lý |
| L14 | [20] | small_group | 8/0 | đạo thủy Đại Việt | lính Đại Việt xuống thuyền, thuyền trái ×4 (trung cảnh trái, lội ra bờ); lính Đại Việt, thuyền phải ×4 (trung cảnh phải) | Medium | thuyền gỗ lòng nông |
| L15 | [21] | army | 14/0 | đạo bộ Tông Đản | lính Đại Việt tiền cảnh ×3 (tiền cảnh); lính Đại Việt giữa ×6 (trung cảnh); lính Đại Việt sau ×5 (hậu cảnh) | Medium | - |
| L16 | [24] | army | 12/0 | Trương Thủ Tiết (không có chân dung) | sĩ quan Tống (Trương Thủ Tiết, tạo hình nghệ thuật) ×1 (tiền cảnh, dẫn đầu); bộ binh nặng Tống ×5 (trung cảnh); cung nỏ thủ Tống ×6 (hậu cảnh) | Medium | - |
| L17 | [25] | battlefield | 16/0 | phục kích ở ải Côn Lôn | lính Tống trên đường ×8 (đường dưới thung lũng); lính Đại Việt sườn trái ×4 (sườn dốc trên trái, nấp sau đá); lính Đại Việt sườn phải ×4 (sườn dốc trên phải) | High | - |
| L18 | [28, 65] | fortress | 11/0 | quân vây thành Đại Việt | lính Đại Việt vác đất ×8 (trên dốc đất); lính Tống giữ thành ×3 (trên đầu tường) | Medium | - |
| L19 | [29] | architecture | 0/0 | sân trong thành Ung Châu | (không có người) ×0 (-) | Low | sân đá trong thành, cửa gỗ khép hờ |
| L20 | [30] | landscape | 0/0 | bãi đất trước tường thành | (không có người) ×0 (-) | Low | - |
| L21 | [31] | small_group | 14/0 | người dân bị bắt | người dân Tống bị đưa về ×6 (giữa đường, xếp một hàng); lính Đại Việt dẫn đầu ×4 (phía trước hàng dân); lính Đại Việt đi sau ×4 (phía sau hàng dân) | Medium | dân Tống áo thô, đầu trần hoặc khăn quấn |
| M3 | [32, 33] | bản đồ SVG | - | - | Ung Châu nằm sâu trong lãnh thổ nhà Tống, đường rút về biên giới và về Đại Việt, hai vùng ven biển Khâm và Liêm. Minh họa lý do "không ở lại giữ thành": đường rút dài, có thể bị bao vây. | - | cần dữ liệu địa lý |
| L22 | [34] | army | 12/0 | Quách Quỳ (không có chân dung) | chỉ huy Tống (Quách Quỳ, tạo hình nghệ thuật) ×1 (tiền cảnh, nhìn từ phía sau); bộ binh nặng Tống ×6 (trung cảnh trước, một hàng); cung nỏ thủ Tống ×5 (trung cảnh sau, một hàng) | Medium | - |
| M4 | [35] | bản đồ SVG | - | - | Ba mũi áp lực lên Đại Việt: từ phía bắc (nhà Tống), phía nam (Chiêm Thành) và phía tây nam (Chân Lạp). Chỉ dựa trên kịch bản. | - | cần dữ liệu địa lý |
| L23 | [36] | army | 14/0 | đại quân Tống | sĩ quan Tống ×1 (tiền cảnh, dẫn đầu); bộ binh nặng Tống ×7 (trung cảnh); cung nỏ thủ Tống ×6 (hậu cảnh) | Medium | - |
| L24 | [37, 67] | small_group | 3/0 | Lý Thường Kiệt | Lý Thường Kiệt (tạo hình nghệ thuật) ×1 (tiền cảnh, nhìn từ phía sau); sĩ quan Đại Việt ×2 (hai bên, sau một bước) | Low | - |
| M5 | [38, 39] | bản đồ SVG | - | - | Sông Như Nguyệt (sông Cầu) nằm trên đường từ phía bắc về Thăng Long; vị trí khúc sông và khoảng cách tới kinh thành. Cần dữ liệu địa lý đã kiểm. | - | cần dữ liệu địa lý |
| L25 | [40, 66] | landscape | 10/0 | phòng tuyến bờ nam | lính Đại Việt giữ phòng tuyến ×10 (rải dọc bờ nam) | Medium | lũy đất cắm cọc gỗ dọc bờ nam |
| L26 | [41, 42, 43] | army | 13/0 | quân Tống nhìn phòng tuyến | lính Tống bờ bắc ×5 (tiền cảnh, nhìn từ phía sau); lính Đại Việt bờ nam ×8 (hậu cảnh, nhỏ, sau lũy) | Medium | lũy đất cắm cọc gỗ dọc bờ nam |
| L27 | [44] | battlefield | 16/0 | trận vượt sông | lính Tống lội sông ×8 (trung cảnh, lội qua dòng nông); lính Đại Việt sau lũy ×8 (hậu cảnh, sau lũy bờ nam) | High | lũy đất cắm cọc gỗ dọc bờ nam |
| L28 | [45, 48, 68] | small_group | 5/0 | quân sĩ nghe bài thơ | lính Đại Việt ×5 (trước đền, nhóm lỏng) | Low | đền nhỏ bên sông mái ngói xám, đèn dầu bên trong |
| L29 | [46, 47] | object_detail | 0/0 | cửa đền | (không có người) ×0 (-) | Low | cửa đền gỗ chạm khắc đơn giản, đèn dầu đất nung |
| L30 | [49] | small_group | 8/0 | doanh trại quân Tống | lính Tống ngồi nghỉ, nhóm trái ×4 (trung cảnh trái); lính Tống ngồi nghỉ, nhóm phải ×4 (trung cảnh phải) | Low | lều vải đơn giản của quân Tống |
| L31 | [52] | army | 12/0 | quân Tống rút lui | lính Tống tiền cảnh ×3 (tiền cảnh, từ phía sau); lính Tống phía sau ×9 (trung cảnh và hậu cảnh) | Medium | - |
| M6 | [53, 57, 59] | bản đồ SVG | - | - | Các châu Quảng Nguyên, Tư Lang, Tô Mậu (quân Tống giữ lại); Quảng Nguyên đổi tên Thuận Châu (1079); trại Vĩnh Bình và sáu huyện, ba động được trả (1084). Cần dữ liệu địa lý đã kiểm. | - | cần dữ liệu địa lý |
| L32 | [54, 55, 56] | small_group | 6/0 | Đào Tống Nguyên (không có chân dung) | sứ giả Đại Việt (Đào Tống Nguyên, tạo hình nghệ thuật) ×1 (dẫn đầu đoàn); người dắt voi ×5 (mỗi người cạnh một con voi) | High | - |
| L33 | [58] | small_group | 12/0 | người dân và binh lính được trao trả | người dân Tống được trả về ×10 (giữa đường, hai hàng năm người); lính Đại Việt đi cùng ×2 (cuối hàng) | Medium | dân và binh lính Tống được trả: áo thô, đầu trần hoặc khăn quấn |
| M7 | [61] | bản đồ SVG | - | - | Diễn Châu (nơi Lý Giác dấy binh năm 1103). Chỉ dựa trên kịch bản. | - | cần dữ liệu địa lý |
| L34 | [62] | army | 14/0 | Lý Thường Kiệt | Lý Thường Kiệt (tạo hình nghệ thuật) ×1 (tiền cảnh, từ phía sau); lính Đại Việt ×13 (sau tướng, ba nhóm) | Medium | - |
| L35 | [64] | command_room | 0/0 | sảnh vắng | (không có người) ×0 (-) | Low | bản đồ cuộn không chữ |

## Điểm cần anh quyết
- Nhân vật Lý Thường Kiệt cần Character Reference (cảnh L04, L08, L11, L12, L24, L34); chưa có ảnh nào được duyệt.
- Voi (L32, đoạn 54–56): chưa có khối giải phẫu voi và bộ kiểm chưa đếm voi; em đề xuất câu giải phẫu voi, cần anh duyệt.
- 7 bản đồ vector cần dữ liệu địa lý đã kiểm.
- Cảnh rủi ro cao: L17 (phục kích), L27 (vượt sông), L32 (voi).
- Ảnh giữ lâu (đoạn liền nhau dùng chung một ảnh, ~18–30 s): L04 (4–5), L08 (17–18), L10 (22–23), L11 (50–51), L13 (15–16), L26 (41–43), L29 (46–47), L32 (54–56): cần hiệu ứng chuyển động hoặc thêm ảnh.
- 20 chi tiết ngoài khối (đạo cụ, trang phục dân, thuyền, lũy cọc, đền, lều…) gắn artistic_choice, owner_approved=false; PLAN_APPROVED chỉ khi anh duyệt.
- Số người trong ảnh chỉ minh họa, không phải số quân trong sử; không vẽ cờ, máu, thi thể.
