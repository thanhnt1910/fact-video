# Scene Planner lt1v4 — bảng chủ kênh duyệt (PLAN_OWNER_REVIEW, bản 2)

Bible: master 1.3, period 1.3, khoi-prompt 1.3. 42 cảnh = 35 ảnh FLUX + 7 bản đồ vector. Phủ đủ đoạn 1–68. Rủi ro: Thấp 14, Vừa 18, Cao 3. Chưa vẽ ảnh, chưa gọi API, chưa đọc giọng.

| Cảnh | Đoạn | Loại | Người/Ngựa/Voi | Nhân vật chính | Nhóm (vị trí) | Rủi ro | Chi tiết nghệ thuật chờ duyệt |
|---|---|---|---|---|---|---|---|
| L01 | [1, 34] | fortress | 6/0/0 | thành Ung Châu | lính Tống trên đầu tường ×6 (trung cảnh, rải đều trên đầu tường) | Low | - |
| L02 | [2, 35, 36] | portrait | 3/0/0 | Tô Giám (không có chân dung; tạo hình nghệ thuật) | sĩ quan Tống (tri châu Tô Giám, tạo hình nghệ thuật) ×1 (tiền cảnh trái, nhìn từ phía sau); lính Tống ×2 (trung cảnh, sau sĩ quan vài bước) | Low | - |
| L03 | [3, 87] | army | 16/0/0 | đoàn quân Đại Việt | lính Đại Việt tiền cảnh ×3 (tiền cảnh); lính Đại Việt trung cảnh ×7 (trung cảnh); lính Đại Việt hậu cảnh ×6 (hậu cảnh, nhỏ) | Medium | - |
| L04 | [4, 5, 78] | command_room | 1/0/0 | Lý Thường Kiệt | Lý Thường Kiệt (tạo hình nghệ thuật) ×1 (giữa khung, nhìn từ phía sau và hơi nghiêng) | Medium | AC01, AC23 |
| L05 | [6] | architecture | 3/0/0 | kinh thành Thăng Long | người hầu trong cung ×3 (tiền cảnh dưới, nhỏ) | Low | AC02 |
| L06 | [7] | small_group | 8/0/0 | Lý Thường Kiệt thời trung niên (chưa có Character Reference) | quan Đại Việt (Lý Thường Kiệt thời trẻ hơn, tạo hình nghệ thuật) ×1 (giữa đường); tùy tùng ×3 (sau quan); dân làng ×4 (bên phải, làm ruộng) | Low | AC03, AC04 |
| L07 | [8, 9, 82, 83] | army | 12/0/0 | đạo quân tiên phong | lính Đại Việt tiên phong tiền cảnh ×4 (tiền cảnh); lính Đại Việt phía sau ×8 (trung cảnh) | Medium | - |
| L08 | [10, 11, 22, 23, 24] | small_group | 3/0/0 | Lý Thường Kiệt | Lý Thường Kiệt (tạo hình nghệ thuật) ×1 (tiền cảnh, nhìn từ phía sau); lính Đại Việt ×2 (sau tướng vài bước) | Low | - |
| L09 | [12, 13] | object_detail | 0/0/0 | không có người | (không có người) ×0 (-) | Low | AC05 |
| M1 | [14, 15] | bản đồ SVG | - | - | 4 mục địa lý NEEDS_REVIEW (xem ban-do-can-xac-minh.md) | - | - |
| L10 | [16, 29, 30, 31] | small_group | 8/0/0 | xưởng đóng thuyền của quân Tống | lính Tống ở xưởng thuyền ×8 (tiền cảnh 4, gần thân thuyền 4) | Medium | AC06 |
| L11 | [17, 65, 66, 67] | command_room | 4/0/0 | Lý Thường Kiệt | Lý Thường Kiệt (tạo hình nghệ thuật) ×1 (đầu bàn phía xa, ba phần tư); sĩ quan Đại Việt ×3 (hai bên và đầu bàn gần) | Medium | AC07, AC24 |
| L12 | [18] | army | 14/0/0 | Lý Thường Kiệt, Tông Đản | tướng Đại Việt (Lý Thường Kiệt) ×1 (tiền cảnh trái, từ phía sau); tướng Đại Việt (Tông Đản, tạo hình nghệ thuật) ×1 (tiền cảnh phải, từ phía sau); lính Đại Việt ×12 (trung cảnh, hai hàng sáu người) | Medium | AC08 |
| L13 | [19, 20, 21] | small_group | 6/0/0 | nông dân nhà Tống | nông dân Tống ×3 (tiền cảnh); nông dân Tống ×3 (trung cảnh) | Low | AC09 |
| M2 | [25, 26] | bản đồ SVG | - | - | 7 mục địa lý NEEDS_REVIEW (xem ban-do-can-xac-minh.md) | - | - |
| L14 | [27] | small_group | 8/0/0 | đạo thủy Đại Việt | lính Đại Việt xuống thuyền, thuyền trái ×4 (trung cảnh trái, lội ra bờ); lính Đại Việt, thuyền phải ×4 (trung cảnh phải) | Medium | AC10 |
| L15 | [28] | army | 14/0/0 | đạo bộ Tông Đản | lính Đại Việt tiền cảnh ×3 (tiền cảnh); lính Đại Việt giữa ×6 (trung cảnh); lính Đại Việt sau ×5 (hậu cảnh) | Medium | - |
| L16 | [32] | army | 12/0/0 | Trương Thủ Tiết (không có chân dung) | sĩ quan Tống (Trương Thủ Tiết, tạo hình nghệ thuật) ×1 (tiền cảnh, dẫn đầu); bộ binh nặng Tống ×5 (trung cảnh); cung nỏ thủ Tống ×6 (hậu cảnh) | Medium | - |
| L17 | [33] | battlefield | 16/0/0 | phục kích ở ải Côn Lôn | lính Tống trên đường ×8 (đường dưới thung lũng); lính Đại Việt sườn trái ×4 (sườn dốc trên trái, nấp sau đá); lính Đại Việt sườn phải ×4 (sườn dốc trên phải) | High | - |
| L18 | [37, 86] | fortress | 11/0/0 | quân vây thành Đại Việt | lính Đại Việt vác đất ×8 (trên dốc đất); lính Tống giữ thành ×3 (trên đầu tường) | Medium | - |
| L19 | [38] | architecture | 0/0/0 | sân trong thành Ung Châu | (không có người) ×0 (-) | Low | AC11 |
| L20 | [39, 40] | landscape | 0/0/0 | bãi đất trước tường thành | (không có người) ×0 (-) | Low | - |
| L21 | [41] | small_group | 14/0/0 | người dân bị bắt | người dân Tống bị đưa về ×6 (giữa đường, xếp một hàng); lính Đại Việt dẫn đầu ×4 (phía trước hàng dân); lính Đại Việt đi sau ×4 (phía sau hàng dân) | Medium | AC12 |
| M3 | [42, 43, 44] | bản đồ SVG | - | - | 3 mục địa lý NEEDS_REVIEW (xem ban-do-can-xac-minh.md) | - | - |
| L22 | [45] | army | 12/0/0 | Quách Quỳ (không có chân dung) | chỉ huy Tống (Quách Quỳ, tạo hình nghệ thuật) ×1 (tiền cảnh, nhìn từ phía sau); bộ binh nặng Tống ×6 (trung cảnh trước, một hàng); cung nỏ thủ Tống ×5 (trung cảnh sau, một hàng) | Medium | - |
| M4 | [46] | bản đồ SVG | - | - | 3 mục địa lý NEEDS_REVIEW (xem ban-do-can-xac-minh.md) | - | - |
| L23 | [47] | army | 14/0/0 | đại quân Tống | sĩ quan Tống ×1 (tiền cảnh, dẫn đầu); bộ binh nặng Tống ×7 (trung cảnh); cung nỏ thủ Tống ×6 (hậu cảnh) | Medium | - |
| L24 | [48, 88] | small_group | 3/0/0 | Lý Thường Kiệt | Lý Thường Kiệt (tạo hình nghệ thuật) ×1 (tiền cảnh, nhìn từ phía sau); sĩ quan Đại Việt ×2 (hai bên, sau một bước) | Low | - |
| M5 | [49, 50, 51] | bản đồ SVG | - | - | 5 mục địa lý NEEDS_REVIEW (xem ban-do-can-xac-minh.md) | - | - |
| L25 | [52, 87] | landscape | 10/0/0 | phòng tuyến bờ nam | lính Đại Việt giữ phòng tuyến ×10 (rải dọc bờ nam) | Medium | AC13 |
| L26 | [53, 54, 55, 56] | army | 13/0/0 | quân Tống nhìn phòng tuyến | lính Tống bờ bắc ×5 (tiền cảnh, nhìn từ phía sau); lính Đại Việt bờ nam ×8 (hậu cảnh, nhỏ, sau lũy) | Medium | AC14 |
| L27 | [57] | battlefield | 16/0/0 | trận vượt sông | lính Tống lội sông ×8 (trung cảnh, lội qua dòng nông); lính Đại Việt sau lũy ×8 (hậu cảnh, sau lũy bờ nam) | High | AC15 |
| L28 | [58, 59, 62, 63, 89, 90] | small_group | 5/0/0 | quân sĩ nghe bài thơ | lính Đại Việt ×5 (trước đền, nhóm lỏng) | Low | AC16 |
| L29 | [60, 61] | object_detail | 0/0/0 | cửa đền | (không có người) ×0 (-) | Low | AC17 |
| L30 | [64] | small_group | 8/0/0 | doanh trại quân Tống | lính Tống ngồi nghỉ, nhóm trái ×4 (trung cảnh trái); lính Tống ngồi nghỉ, nhóm phải ×4 (trung cảnh phải) | Low | AC18 |
| L31 | [68] | army | 12/0/0 | quân Tống rút lui | lính Tống tiền cảnh ×3 (tiền cảnh, từ phía sau); lính Tống phía sau ×9 (trung cảnh và hậu cảnh) | Medium | - |
| M6 | [69, 75, 77] | bản đồ SVG | - | - | 6 mục địa lý NEEDS_REVIEW (xem ban-do-can-xac-minh.md) | - | - |
| L32 | [70, 71, 72, 73, 74] | small_group | 6/0/5 | Đào Tống Nguyên (không có chân dung) | sứ giả Đại Việt (Đào Tống Nguyên, tạo hình nghệ thuật) ×1 (dẫn đầu đoàn); người dắt voi (mỗi người một con) ×5 (mỗi người cạnh đầu con voi của mình) | High | AC19 |
| L33 | [76] | small_group | 14/0/0 | dân và binh lính nhà Tống được trao trả | người dân Tống được trả về ×8 (giữa đường, hai hàng bốn người); lính Tống được trả về (không vũ khí) ×4 (sau hàng dân, một hàng dọc); lính Đại Việt đi cùng ×2 (cuối hàng) | Medium | AC20, AC22 |
| M7 | [79] | bản đồ SVG | - | - | 2 mục địa lý NEEDS_REVIEW (xem ban-do-can-xac-minh.md) | - | - |
| L34 | [80, 81] | army | 14/0/0 | Lý Thường Kiệt | Lý Thường Kiệt (tạo hình nghệ thuật) ×1 (tiền cảnh, từ phía sau); lính Đại Việt ×13 (sau tướng, ba nhóm) | Medium | - |
| L35 | [84, 85] | command_room | 0/0/0 | sảnh vắng | (không có người) ×0 (-) | Low | AC21 |

## Nhân vật có tên: hồ sơ, giai đoạn, thấy mặt

| Cảnh | Hồ sơ / giai đoạn | Thấy mặt | Cần quyết râu trước khi vẽ |
|---|---|---|---|
| L04 | ly-thuong-kiet S2 | có | CÓ (râu UNDECIDED) |
| L08 | ly-thuong-kiet S1,S2 | không (nhìn từ phía sau) | chưa cần |
| L11 | ly-thuong-kiet S2 | có | CÓ (râu UNDECIDED) |
| L12 | ly-thuong-kiet S2; tong-dan S1 | không (nhìn từ phía sau) | chưa cần |
| L24 | ly-thuong-kiet S2 | không (nhìn từ phía sau) | chưa cần |
| L34 | ly-thuong-kiet S4 | không (nhìn từ phía sau) | chưa cần |

## Đoạn 87 của bản tách 90 đoạn (đoạn 66 của bản 68 đoạn; hai cảnh L03 rồi L25)

1. **L03** — "Một lần, ông đưa quân vượt biên giới, đánh vào đất địch." (12 chữ, khoảng 0–4 giây của đoạn). câu này nói về cuộc tiến quân sang đất Tống: cảnh quân Đại Việt hành quân lên phía bắc.
2. **L25** — "Một lần khác, ông dựng phòng tuyến bên sông, bảo vệ từng tấc đất quê hương." (16 chữ, khoảng 4–9 giây của đoạn). câu này nói về phòng tuyến bên sông: cảnh lũy đất dọc bờ nam.

Chủ ý dùng hai cảnh: đoạn này gồm hai câu có hai ý đối nhau (vượt biên giới đánh trước / dựng phòng tuyến giữ sông), mỗi câu khoảng 4–5 giây. Cắt đúng ở dấu chấm sau "đất địch", không đổi lời đọc. Phương án khác: dùng L25 cho cả đoạn (bỏ L03 ở đoạn này), nhưng khi đó câu đầu hiện cảnh bờ sông không khớp lời. Em đề xuất giữ hai cảnh.

## Ảnh/bản đồ giữ lâu (từ 18 giây) và cách xử lý

| Cảnh | Đoạn | Giữ (giây) | Xử lý |
|---|---|---|---|
| L04 | 4–5 | 19 | Đoạn 4: zoom chậm vào bản đồ trên bàn (cắt cận bàn). Đoạn 5: pan nhẹ sang nhân vật khi tên Lý Thường Kiệt được nhắc. Một ảnh, ~19 giây. |
| L13 | 19–21 | 20 | Đoạn 15: khung rộng, zoom chậm vào nhóm gặt lúa phía trước. Đoạn 16: pan sang nhóm bó lúa phía sau. Một ảnh, ~20 giây. |
| L08 | 22–24 | 23 | Đoạn 17: khung rộng, zoom chậm vào lưng tướng. Đoạn 18: pan lên dãy núi phía bắc (cắt cận núi). Một ảnh, ~23 giây; dùng lại cho đoạn 9 thì đổi hướng pan. |
| L10 | 29–31 | 19 | Đoạn 22: khung rộng xưởng thuyền. Đoạn 23: zoom vào hai thân thuyền. Một ảnh, ~19 giây. |
| M3 | 42–44 | 21 | Bản đồ động: hai đoạn ~21 giây; hiện địa danh theo từng câu (đoạn 32: câu hỏi; đoạn 33: lập luận), không thêm ảnh. |
| M5 | 49–51 | 18 | Bản đồ động ~18 giây: đoạn 38 hiện sông, đoạn 39 hiện Thăng Long và hướng tiến; không thêm ảnh. |
| L26 | 53–56 | 29 | Ba đoạn ~29 giây. Đoạn 41: khung rộng từ lưng lính Tống. Đoạn 42: zoom chậm vào hàng lũy bờ nam. Đoạn 43: pan xuống mặt nước và lính Tống chuẩn bị lội. Một ảnh, ba lần cắt cận; nếu chủ kênh thấy đơn điệu thì đề xuất dùng L25 (cùng phòng tuyến) cho đoạn 43. |
| L29 | 60–61 | 18 | Đoạn 46 và 47 (~18 giây): zoom rất chậm vào cửa đền, đèn dầu sáng dần. Một ảnh. |
| L11 | 65–67 | 19 | Đoạn 50: khung ba phần tư. Đoạn 51: zoom vào bản đồ trên bàn. Một ảnh, ~19 giây. |

Không đề xuất thêm ảnh mới ở bước này. Chỉ L32 có điều kiện: thêm một ảnh cận sứ giả nếu cắt cận từ ảnh gốc bị mờ.

## L32 — kiểm soát voi

- `expected_elephants` = 5; năm cặp (người dắt k ↔ voi k) trong `elephant_pairs`; prompt có "EXACTLY five elephants" và "one attendant per elephant".
- Sổ ảnh: `dem_thu_cong.voi` (số người đếm) tách riêng khỏi `ke_hoach.voi`; PASS chỉ khi hai số khớp. Chỉ theo dõi voi, chưa mở rộng loài khác.
- Câu giải phẫu voi chưa có trong `khoi-prompt.json` nên nằm ở chi tiết nghệ thuật (mã trong `chi-tiet-artistic-choice.md`), cần anh duyệt; em bỏ "ngà" vì chưa có căn cứ.

## Còn tồn tại

- Character Reference Lý Thường Kiệt (L04, L08, L11, L12, L24, L34) chưa duyệt; danh sách ảnh tham chiếu được duyệt rỗng.
- 33 mục địa lý bản đồ NEEDS_REVIEW.
- 24 chi tiết nghệ thuật chờ anh duyệt.
- Cảnh rủi ro cao: L17, L27, L32.
- Kịch bản v4 còn 31 ❌ / 13 ⚠️ của `kiem_kich_ban.py` (anh giữ nguyên lời đọc).
