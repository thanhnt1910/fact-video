# PERIOD BIBLE – Đại Việt nhà Lý và Trung Hoa nhà Tống (v1.2 DRAFT, 01/11/2026)

**Trạng thái: DRAFT (đã sửa theo quyết định phục dựng thận trọng của chủ kênh và bổ sung quy tắc truy vết; chờ chủ kênh xác nhận quy chuẩn cuối).** Chưa APPROVED. Chưa lập Scene Planner, chưa vẽ lại ảnh nào theo bản này.

## A. Nhận diện
- Thời kỳ: 1075–1077 (chiến tranh Lý–Tống), tham chiếu thêm 1069–1105 (đời Lý Thường Kiệt).
- Phe 1: Đại Việt, nhà Lý (Thăng Long, sông Như Nguyệt). Phe 2: Bắc Tống (Quảng Tây, Quế Châu, Ung, Khâm, Liêm châu).

## B. Ba mức bằng chứng và nhãn trong prompt (chủ kênh chốt 01/11/2026)
| Mức | Nghĩa | Nhãn gắn vào chi tiết | Cách dùng |
|---|---|---|---|
| **A** | Bằng chứng khảo cổ trực tiếp | (không cần nhãn) | Dùng thẳng |
| **B** | Tư liệu lịch sử hoặc bằng chứng gián tiếp | `cautious_reconstruction` | Phục dựng thận trọng, không nêu kiểu dáng, màu, cấu tạo cụ thể khi chưa có tư liệu |
| **C** | Lựa chọn nghệ thuật | `artistic_choice` | Không trình bày như sự thật lịch sử |

**Quy tắc nhãn:**
- Mọi chi tiết chưa được xác nhận (B hoặc C) phải mang MỘT trong hai nhãn; không có "không nhãn". Chi tiết ghi "A/B" trong bảng (giáp vảy, mũ sắt, vũ khí Tống) coi là `cautious_reconstruction`, trừ khi chủ kênh xác nhận mức A.
- Không tự suy diễn: xem Master Style mục 7.
- Mỗi cảnh trong Scene Planner có trường `detail_tags` liệt kê từng chi tiết chưa được xác nhận kèm nhãn, ví dụ `[{"item":"khăn quấn đầu","tag":"artistic_choice"},{"item":"giáp sắt và da","tag":"cautious_reconstruction"}]`. Nhãn nằm trong dữ liệu cảnh (và trong ghi chú gửi chủ kênh duyệt), không dán vào câu prompt vì FLUX không hiểu nhãn.
- Chi tiết mang nhãn KHÔNG được tự biến thành đặc điểm cố định của cả đội quân. Mỗi cảnh chọn theo nhóm người (xem mục C), đổi giữa các cảnh khi hợp lý.
- Chi tiết nào chưa có trong bảng thì không tự thêm; phải hỏi chủ kênh hoặc dùng thiết kế trung tính và gắn `artistic_choice`.

## C. Đại Việt nhà Lý

| Hạng mục | Hướng thể hiện | Mức / nhãn | Căn cứ | Hạn chế |
|---|---|---|---|---|
| Kiến trúc cung điện | Nhà gỗ, mái ngói, hệ đấu củng | **A** | Khai quật Hoàng thành Thăng Long (53 nền móng, 18 Hoàng Diệu và khu Quốc hội) | Dạng mái cụ thể, bố cục: còn đang nghiên cứu |
| Nhà dân, trướng quân | Nhà gỗ đơn giản, mái ngói xám hoặc tranh, sàn chiếu | C `artistic_choice` | Suy từ kiến trúc cung đình, không có tư liệu riêng | Không chạm trổ cầu kỳ |
| Giáp lính Đại Việt | Giáp làm từ sắt và da. **Không mặc định cả đội quân mặc giáp**: một phần lính (nhóm tiền cảnh, tiền quân) mặc giáp, phần còn lại áo vải thô | **B** `cautious_reconstruction` | Wikipedia "Vietnamese armour": thời trung đại chỉ còn văn bản và tranh, hiện vật rất hiếm, không có chi tiết riêng thời Lý | **Không khẳng định kiểu dáng, màu sắc, cấu tạo giáp.** Khi vẽ phải chọn một dạng nhìn được, dạng đó là `artistic_choice` và không đồng nhất giữa các cảnh |
| Quần áo lính | Áo vải thô tay hẹp, màu đất trầm, quần ngắn hoặc dài | C `artistic_choice` | Thiết kế trung tính | Không quân phục xanh, không phụ kiện hiện đại |
| Mũ / đầu lính bộ binh | Ưu tiên khăn quấn đầu, búi tóc, hoặc không đội mũ. **Không dùng nón lá hình chóp làm trang bị mặc định** | C `artistic_choice` | Không có tư liệu xác nhận mũ lính thời Lý | Không mũ lưỡi trai, không mũ sắt kiểu Tống cho lính Đại Việt |
| Nón lá | Chỉ cho dân phu khi bối cảnh thật cần (ví dụ vác đất, tải lương) | C `artistic_choice` | **Chưa có bằng chứng xác nhận kiểu dáng phổ biến thời Lý** | Không dùng cho binh lính, ghi nhãn mỗi lần dùng |
| Tướng lĩnh | Tạo hình khác lính: áo dài rộng hơn, vai giáp hoặc đai lưng, khăn hoặc búi tóc cao gọn | C `artistic_choice` | Thiết kế phân biệt cấp bậc, không phải tư liệu | **Không dùng mũ quan của triều đại muộn hơn** (mũ cánh chuồn Lê–Nguyễn, mũ Tống cho quan Việt) |
| Giày dép | Tùy nhân vật và cảnh: có nhóm đi giày hoặc dép, có nhóm chân đất. **Không mặc định toàn quân chân đất** | C `artistic_choice` | Không có tư liệu thời Lý | Không giày hiện đại, không ủng quân đội |
| Vũ khí | Giáo gỗ đầu sắt, cung, nỏ | B `cautious_reconstruction` | Sử và sách giáo khoa nói quân đội nhà Lý có bộ binh, thủy binh, cung nỏ | Không thêm vũ khí lạ, không kiếm cong |
| Cờ hiệu Đại Việt | **Mặc định KHÔNG vẽ cờ.** Cần cờ thì chỉ cờ vải trơn không chữ, không họa tiết, không sao, màu không cố định | C `artistic_choice` | **Chưa có tư liệu xác nhận màu, họa tiết, biểu tượng cờ Đại Việt** | Không mặc định màu nâu đỏ. Không cờ đỏ sao vàng |
| Thuyền chiến | Thuyền gỗ lòng nông, buồm cói | C `artistic_choice` | Sử chép có thủy quân, không rõ kiểu thuyền | Giữ đơn giản |
| Lý Thường Kiệt | Người lớn tuổi, dáng cứng cỏi; tạo hình chi tiết chờ chủ kênh duyệt Character Reference | C `artistic_choice` | Không có chân dung đương thời đáng tin | Phải có Character Reference được duyệt trước khi vẽ nhiều cảnh |

## D. Trung Hoa nhà Tống

| Hạng mục | Hướng thể hiện | Mức / nhãn | Căn cứ | Hạn chế |
|---|---|---|---|---|
| Giáp vảy sắt | Giáp vảy sắt (lamellar). Bộ binh hạng nặng: loại "bộ nhân giáp" (bu renjia) nặng khoảng 30 kg | **A/B** `cautious_reconstruction` khi nêu chi tiết | *Võ kinh tổng yếu* (1044), tổng quan Song armor (dragonsarmory) | **Không áp dụng đồng nhất mọi binh chủng** (xem dưới) |
| Mũ sắt | Mũ sắt cổ, đỉnh tròn nhọn cho lính và tướng | **A/B** `cautious_reconstruction` | *Võ kinh tổng yếu* (mũ tướng có chùm lông), hiện vật phục dựng | Không mũ cánh chuồn cho lính |
| Phân theo binh chủng | Bộ binh nặng (giáp vảy nặng, khiên, giáo) / cung thủ và nỏ thủ (giáp nhẹ hơn khoảng 5 kg) / bộ binh nhẹ hoặc dân binh (áo thô, có thể mũ nỉ vành rộng) / sĩ quan, tướng (giáp khác, mũ có chùm lông). Mỗi cảnh chỉ định rõ binh chủng nào xuất hiện | B `cautious_reconstruction` | Tổng quan quân Tống (tác giả phục dựng hiện đại) | Không mặc cùng một bộ giáp cho cả đội; nếu kịch bản không nói binh chủng thì dùng bộ binh thường và ghi `artistic_choice` |
| Mũ nỉ vành rộng | Chỉ cho bộ binh nhẹ | B `cautious_reconstruction` | Một bài tổng quan hiện đại, không phải nguồn gốc | Dùng ít |
| Màu quân phục | Xám đậm, kim loại tối | C `artistic_choice` | Không nguồn xác định màu | Không thêm màu tươi |
| Cờ quân Tống | Không vẽ cờ | C | Chưa có chỉ định màu, biểu tượng | Không tự thêm |
| Vũ khí | Giáo, thương, khiên tròn, nỏ | A/B | *Võ kinh tổng yếu*: nỏ thần tý, khiên chắn | Không hỏa khí, không máy bắn đá nếu kịch bản không nói |
| Thành trì | Tường đá hoặc gạch xám cao, lầu cổng gỗ mái ngói cong | B `cautious_reconstruction` | Thành Trung Hoa thời Tống nói chung | **Ung Châu cụ thể: chưa xác nhận tường đất hay gạch** |
| Phòng thủ | Lính gác trên đầu tường, khói sau thành | B | Từ kịch bản | Không thêm thiết bị công phòng ngoài kịch bản |

## E. Công thành (theo kịch bản v4, đoạn 28)
Quân vây thành đắp đất thành dốc áp chân tường: **A theo kịch bản**. Hình ảnh: một khối đất lớn, bề mặt thô, liên tục từ mặt đất lên mép tường; lính vác giỏ đất. Không bao tải, không bậc thang đá. Cách vác bằng giỏ: C `artistic_choice`.

## F. Vật dụng và ánh sáng
- Ánh sáng trong trướng: đèn dầu đất nung đặt trên bàn, không treo gì trên trần. (C `artistic_choice`)
- Bàn gỗ thấp, chiếu; không đèn lồng kính, nến chân cao, bàn ghế kiểu hiện đại.

## G. Quyết định của chủ kênh (01/11/2026) và cách áp dụng
1. **Mũ lính Đại Việt:** khăn quấn đầu, búi tóc hoặc không mũ. Không nón lá làm mặc định. Nón lá chỉ cho dân phu, có nhãn `artistic_choice`. Tướng khác lính, không dùng mũ quan triều muộn. → mục C, dòng "Mũ", "Nón lá", "Tướng lĩnh".
2. **Giáp Đại Việt:** giữ sắt và da ở mức B. Không cả quân mặc giáp da nâu. Không khẳng định kiểu dáng, màu, cấu tạo. → mục C, dòng "Giáp lính".
3. **Giày dép:** không mặc định chân đất; tùy nhân vật. → mục C, dòng "Giày dép".
4. **Cờ hiệu:** không mặc định nâu đỏ; màu, họa tiết, biểu tượng chỉ khi có tư liệu, còn lại ghi thiết kế nghệ thuật. → mục C, dòng "Cờ hiệu". Cách xử lý của tôi: mặc định không vẽ cờ.
5. **Quân Tống:** giữ giáp vảy sắt và mũ sắt (A/B), không đồng nhất mọi binh chủng. → mục D, dòng "Phân theo binh chủng".
6. **Nhãn:** mọi chi tiết mức B/C đánh dấu `cautious_reconstruction` hoặc `artistic_choice` trong `detail_tags`, không thành đặc điểm cố định của cả quân.

## H. Danh sách thay đổi so với v1.0
- Bỏ "giáp da nâu" và "chân đất" khỏi mô tả mặc định của lính Đại Việt; giáp chỉ cho một phần lính.
- Bỏ nón lá khỏi lính; nón chỉ còn cho dân phu (có nhãn).
- Bỏ cờ tam giác nâu đỏ; mặc định không cờ.
- Nâng cấp mức: mũ, quần áo, chân, cờ chuyển sang C `artistic_choice`; giáp sắt và da và vũ khí giữ B; kiến trúc cung đình giữ A.
- Quân Tống: thêm cột phân binh chủng; thêm quy tắc không dùng một bộ giáp cho cả đội.
- Đổi định nghĩa mức A, B, C theo chủ kênh; thêm nhãn `cautious_reconstruction` và `artistic_choice`; thêm trường `detail_tags` cho Scene Planner.
- Mục "Chủ kênh quyết" đổi thành "Quyết định của chủ kênh" với 5 câu đã trả lời.

## I. Còn thiếu tư liệu (chưa tra hoặc không tìm thấy)
- Mũ, đầu, giày dép, quần áo của lính và dân phu thời Lý: chưa có tư liệu trực tiếp. Cần tra hiện vật, phù điêu, tượng chùa Lý (ví dụ phù điêu chùa Phật Tích, chùa Long Đọi) và tài liệu nghiên cứu y phục Việt Nam.
- Cờ hiệu, màu cờ quân Lý: chưa tìm thấy nguồn nào.
- Hình dáng giáp quân Lý: chưa có nguồn.
- Thuyền chiến thời Lý: chưa tra.
- Diện mạo Lý Thường Kiệt và tướng lĩnh (Tông Đản): không có chân dung đương thời.
- Ung Châu: kiểu tường thành, kích thước, cổng.
- Quân Tống tại Quảng Tây thời 1075–1077: binh chủng cụ thể (có dùng quân địa phương, dân binh miền núi?) chưa tra.
- Kiến trúc dân gian và trướng quân thời Lý: không có tư liệu riêng.

## J. Nguồn đã dùng
- [Vietnamese armour (Wikipedia)](https://en.wikipedia.org/wiki/Vietnamese_armour)
- [Song Dynasty military overview (Dragon's Armory)](https://dragonsarmory.blogspot.com/2024/08/song-dynasty-960-1279-military-overview.html)
- [Phỏng dựng kiến trúc cung điện thời Lý (Báo Văn hóa)](https://baovanhoa.vn/doi-song-van-hoa/phong-dung-kien-truc-cung-dien-thoi-ly-da-thuc-su-gan-voi-ngan-nam-lich-su-47638.html)


## K. Ghi chú phiên bản
- v1.0: bản đầu (01/11/2026).
- v1.1: phục dựng thận trọng theo quyết định chủ kênh (mục H).
- v1.2: thêm quy tắc "không có không nhãn", gộp A/B thành `cautious_reconstruction`, thêm liên kết truy vết sang `khoi-prompt.json` (mỗi dòng bảng ứng với một khối `block`). Không đổi nội dung lịch sử.
Bảng ánh xạ dòng bảng sang khối: Giáp lính → VN_GIAP; Quần áo lính → VN_AO_VAI; Mũ/đầu → VN_DAU; Nón lá → VN_NON_DAN_PHU; Tướng lĩnh → VN_TUONG; Giày dép → VN_CHAN; Vũ khí → VN_VU_KHI; Cờ Đại Việt → VN_CO; Lý Thường Kiệt → VN_TUONG_LY_THUONG_KIET; Kiến trúc cung điện → KIEN_TRUC_CUNG; Nhà dân → NHA_DAN; Giáp Tống theo binh chủng → SONG_BO_BINH_NANG, SONG_CUNG_NO, SONG_BO_BINH_NHE, SONG_SI_QUAN; Cờ Tống → SONG_CO; Thành trì → THANH_SONG; Dốc đất → DOC_DAT; Vác đất → VAC_DAT; Đèn → DEN.

Trạng thái: DRAFT v1.2. Chỉ chuyển APPROVED khi chủ kênh xác nhận.
