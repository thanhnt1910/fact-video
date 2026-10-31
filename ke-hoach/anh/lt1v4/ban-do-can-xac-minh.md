# Bản đồ M1–M7: dữ liệu địa lý cần xác minh (lt1v4)

Quy tắc: Không tự đặt tọa độ hay đường biên. Không tạo bản đồ chỉ dựa trên suy đoán. Ba loại thông tin tách riêng: DIA_LY (dữ kiện địa lý), DUONG_QUAN_SU (đường tiến quân/rút lui), DIEN_GIAI (diễn giải lịch sử). Mục chỉ được vẽ (duoc_ve=true) khi trang_thai=VERIFIED và có nguon_xac_minh; toa_do chỉ điền khi VERIFIED. Cột co_so_kich_ban chỉ cho biết kịch bản nhắc tới điều gì, KHÔNG phải nguồn địa lý.

33 mục, tất cả NEEDS_REVIEW; chưa có tọa độ, chưa có đường biên; bản đồ bị chặn (`BLOCKED_NEEDS_REVIEW`).

## CHUNG (dùng cho cả bảy bản đồ)

| Mã | Loại | Nội dung | Cơ sở kịch bản | Cần xác minh | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|
| CHUNG-01 | DIA_LY | Bản đồ nền (bờ biển, sông, địa hình) dùng cho cả bảy bản đồ | - | dữ liệu nền có giấy phép rõ; ghi rõ là bản đồ HIỆN ĐẠI hay bản dựng lịch sử; không dùng bờ biển hiện đại như thể là bờ biển thế kỷ 11 nếu khác nhau | chưa có | NEEDS_REVIEW |
| CHUNG-02 | DIA_LY | Cách gọi địa danh: tên cổ (thời Lý–Tống) và tên hiện đại | - | bảng đối chiếu tên cổ – tên nay có nguồn; chỗ chưa chắc chỉ ghi tên cổ, không gắn tên nay | chưa có | NEEDS_REVIEW |
| CHUNG-03 | DIEN_GIAI | Quy ước nét vẽ: mũi tên quân đội có nhãn "minh họa" nếu tuyến không có sử liệu | - | chủ kênh duyệt quy ước ghi chú | chưa có | NEEDS_REVIEW |

## M1 (đoạn [11])

| Mã | Loại | Nội dung | Cơ sở kịch bản | Cần xác minh | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|
| M1-01 | DIA_LY | Quế Châu: vị trí | đoạn 11 | vị trí thành/châu thời Tống, nguồn địa lý có thể kiểm | chưa có | NEEDS_REVIEW |
| M1-02 | DIA_LY | Đường biên giới Đại Việt – Tống thời điểm 1075 (kịch bản chỉ nói Quế Châu "sát biên giới") | đoạn 11 | nguồn về biên giới; không tự vẽ đường biên | chưa có | NEEDS_REVIEW |
| M1-03 | DUONG_QUAN_SU | Thẩm Khởi và Lưu Di được phái tới vùng Quế Châu: kịch bản KHÔNG nói họ đi từ đâu | đoạn 11 | nếu không có nguồn về điểm xuất phát thì chỉ ghi nhãn tại Quế Châu, không vẽ mũi tên đường đi | chưa có | NEEDS_REVIEW |
| M1-04 | DIEN_GIAI | Ý "nhà Tống chuẩn bị đánh Đại Việt" (lời Vương An Thạch trong kịch bản) | đoạn 11 | chỉ là diễn giải/lời kể; không thể hiện bằng ký hiệu địa lý như dữ kiện | chưa có | NEEDS_REVIEW |

## M2 (đoạn [19])

| Mã | Loại | Nội dung | Cơ sở kịch bản | Cần xác minh | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|
| M2-01 | DIA_LY | Khâm Châu và Liêm Châu: vị trí (kịch bản: hai vùng ven biển của nhà Tống) | đoạn 20 | vị trí hai châu thời Tống và đối chiếu với tên nay | chưa có | NEEDS_REVIEW |
| M2-02 | DIA_LY | Ung Châu: vị trí | đoạn 19-21 | vị trí thành thời Tống | chưa có | NEEDS_REVIEW |
| M2-03 | DIA_LY | Điểm xuất phát của đạo thủy và đạo bộ (kịch bản không nêu) | đoạn 19 | nguồn sử về nơi tập kết; nếu không có thì không vẽ điểm xuất phát | chưa có | NEEDS_REVIEW |
| M2-04 | DUONG_QUAN_SU | Đường đi của đạo thủy (Lý Thường Kiệt) tới Khâm Châu, Liêm Châu | đoạn 19-20 | kịch bản chỉ nói đạo thủy tiến công hai châu; tuyến biển cụ thể cần nguồn, nếu không chỉ vẽ mũi tên ước lệ có nhãn "minh họa" | chưa có | NEEDS_REVIEW |
| M2-05 | DUONG_QUAN_SU | Đường đi của đạo bộ (Tông Đản) tới Ung Châu | đoạn 19, 21 | tuyến bộ cụ thể cần nguồn; kịch bản không nêu | chưa có | NEEDS_REVIEW |
| M2-06 | DIEN_GIAI | Phân công chỉ huy: Lý Thường Kiệt – đạo thủy, Tông Đản – đạo bộ (lời kể trong kịch bản) | đoạn 19 | đối chiếu nguồn sử; nhãn chỉ huy chỉ ghi khi đã đối chiếu | chưa có | NEEDS_REVIEW |
| M2-07 | DIEN_GIAI | Số quân "hơn mười vạn người" | đoạn 19 | số liệu phải có nguồn; không ghi lên bản đồ nếu chưa đối chiếu | chưa có | NEEDS_REVIEW |

## M3 (đoạn [32, 33])

| Mã | Loại | Nội dung | Cơ sở kịch bản | Cần xác minh | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|
| M3-01 | DIA_LY | Ung Châu: vị trí và khoảng cách tới biên giới | đoạn 32-33 | khoảng cách tính trên dữ liệu đã xác minh, không ước lượng bằng mắt | chưa có | NEEDS_REVIEW |
| M3-02 | DUONG_QUAN_SU | Đường rút về nước của quân Đại Việt (kịch bản chỉ nói "mất đường rút về nước") | đoạn 33 | tuyến rút cụ thể không có trong kịch bản; không vẽ nếu chưa có nguồn | chưa có | NEEDS_REVIEW |
| M3-03 | DIEN_GIAI | Lý do không ở lại giữ thành: "có thể bị bao vây và mất đường rút" (diễn giải trong lời đọc) | đoạn 33 | là lập luận trong kịch bản; không vẽ vòng vây hay mũi tên bao vây như sự kiện đã xảy ra | chưa có | NEEDS_REVIEW |

## M4 (đoạn [35])

| Mã | Loại | Nội dung | Cơ sở kịch bản | Cần xác minh | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|
| M4-01 | DIA_LY | Phạm vi (lãnh thổ) Đại Việt, nhà Tống, Chiêm Thành, Chân Lạp khoảng 1075 | đoạn 35 | nguồn về ranh giới các nước; không tự vẽ đường biên | chưa có | NEEDS_REVIEW |
| M4-02 | DIA_LY | Vị trí tương đối của Chiêm Thành và Chân Lạp so với Đại Việt (phía nam? tây nam?) | đoạn 35 | kịch bản không nêu hướng; phải có nguồn trước khi đặt nhãn | chưa có | NEEDS_REVIEW |
| M4-03 | DIEN_GIAI | Ý "tạo sức ép từ nhiều phía" và việc nhà Tống liên kết hai nước | đoạn 35 | diễn giải; mũi tên áp lực chỉ là ký hiệu minh họa có nhãn, không phải đường hành quân | chưa có | NEEDS_REVIEW |

## M5 (đoạn [38, 39])

| Mã | Loại | Nội dung | Cơ sở kịch bản | Cần xác minh | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|
| M5-01 | DIA_LY | Sông Như Nguyệt: đoạn sông cụ thể nơi đặt phòng tuyến (kịch bản chỉ nói "khúc sông này") | đoạn 38-40 | xác định đoạn sông có nguồn; tên cổ – tên nay | chưa có | NEEDS_REVIEW |
| M5-02 | DIA_LY | Thăng Long (thời Lý): vị trí | đoạn 39 | vị trí kinh thành thời Lý | chưa có | NEEDS_REVIEW |
| M5-03 | DIA_LY | Bờ bắc và bờ nam của đoạn sông (bờ nam là phía Đại Việt giữ) | đoạn 40-41 | hướng chảy và bờ theo dữ liệu đã xác minh | chưa có | NEEDS_REVIEW |
| M5-04 | DUONG_QUAN_SU | Đường quân Tống tiến về kinh thành qua khúc sông (kịch bản: "nằm trên đường tiến về kinh thành") | đoạn 39-40 | tuyến bộ từ biên giới đến sông cần nguồn | chưa có | NEEDS_REVIEW |
| M5-05 | DIEN_GIAI | Phòng tuyến dọc bờ nam: vị trí và hình dạng (kịch bản: "theo những ghi chép và truyền lại về sau") | đoạn 40 | vị trí cụ thể chưa có; không vẽ phòng tuyến thành đường cụ thể trên bản đồ | chưa có | NEEDS_REVIEW |

## M6 (đoạn [53, 57, 59])

| Mã | Loại | Nội dung | Cơ sở kịch bản | Cần xác minh | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|
| M6-01 | DIA_LY | Quảng Nguyên, Tư Lang, Tô Mậu: vị trí các châu | đoạn 52-53 | vị trí và tên nay có nguồn | chưa có | NEEDS_REVIEW |
| M6-02 | DIA_LY | Thuận Châu (tên mới của Quảng Nguyên từ năm một nghìn không trăm bảy mươi chín): vị trí | đoạn 57 | vị trí; xác nhận cùng vùng đất với Quảng Nguyên | chưa có | NEEDS_REVIEW |
| M6-03 | DIA_LY | Trại Vĩnh Bình (nơi đàm phán năm một nghìn không trăm tám mươi tư): vị trí | đoạn 59 | vị trí có nguồn | chưa có | NEEDS_REVIEW |
| M6-04 | DIA_LY | Sáu huyện và ba động được trả lại (kịch bản không nêu tên) | đoạn 59 | tên và vị trí từng nơi; nếu chưa có thì KHÔNG đánh dấu, chỉ ghi chữ trên màn hình | chưa có | NEEDS_REVIEW |
| M6-05 | DIA_LY | Ranh giới trước và sau khi trả đất | đoạn 53, 57, 59 | nguồn về ranh giới; không tự vẽ đường biên | chưa có | NEEDS_REVIEW |
| M6-06 | DIEN_GIAI | Trình tự trả đất theo năm (một nghìn không trăm bảy mươi chín, một nghìn không trăm tám mươi tư) | đoạn 57, 59 | mốc năm đối chiếu nguồn; thể hiện bằng nhãn năm, không bằng đường biên | chưa có | NEEDS_REVIEW |

## M7 (đoạn [61])

| Mã | Loại | Nội dung | Cơ sở kịch bản | Cần xác minh | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|
| M7-01 | DIA_LY | Diễn Châu: vị trí | đoạn 61 | vị trí châu thời Lý và tên nay | chưa có | NEEDS_REVIEW |
| M7-02 | DIEN_GIAI | Lý Giác dấy binh năm một nghìn một trăm linh ba (sự kiện trong kịch bản) | đoạn 61 | chỉ đặt nhãn sự kiện tại Diễn Châu nếu vị trí đã xác minh; không vẽ đường hành quân | chưa có | NEEDS_REVIEW |

