# Thử quy trình mới trên tm11 (Dương Đình Nghệ, Đại La 931), 18/11/2026

**Trạng thái:** kết quả thử, chưa sửa kịch bản. `tm11_full.json` và `viet_tm11.py` giữ nguyên. Sửa kịch bản phải qua cổng C (toàn văn + bảng đổi); bảng đổi đề xuất ở mục 4.

Cách thử: đi lại bốn bước ở CLAUDE.md §3 trên kịch bản đã có (26 đoạn, 636 chữ, khoảng 3,5 phút): bộ kiểm, đối chiếu nguồn lần hai, đọc theo `giong-van.md` bản gộp, câu tự rà tầng 3 trong `bien-tap.md`.

## 1. Bộ kiểm
| Bộ kiểm | Kết quả | Đọc |
|---|---|---|
| `kiem_kich_ban` | 0 ❌, 5 ⚠️ (đoạn 186006 nhiều dấu phẩy; 186009, 186023, 186025, 186026 dài 31–32 chữ) | Đúng giới hạn kỹ thuật, không vượt 32 |
| `kiem_khung` | 0 ❌, 0 ⚠️ | Khung đủ, câu đếm "Thứ đầu tiên / Thứ hai" khớp lời hứa |
| `kiem_mach_ke` | 0 ❌, 3 ⚠️ (16% đoạn mở bằng từ nối; hai đoạn 4 tên riêng) | Gợi ý, không phải lỗi |
| `kiem_mo_dau` | ⚠️ 7 tên riêng mới trong 25 giây đầu | Đã chấp nhận ở bản gửi duyệt cũ |
| `kiem_giong_van` | 0 ❌, 0 ⚠️ | |

Công cụ không bắt được bốn vấn đề ở mục 2 và 3: đúng như thiết kế (tầng 1 là cổng của người và Claude, không phải của công cụ).

## 2. Kiểm tầng 1: nguồn (tra lại ngày 18/11, ngoài Wikipedia)
Nguồn dùng: giaoduc.net.vn ("Nhìn lại trận chiến trên sông Bạch Đằng năm 938"), hoduongvietnam.com.vn ("Dương Đình Nghệ với việc giải phóng thành Đại La năm 931"; bài dẫn Toàn thư, Việt giám thông khảo luận). Bản gửi duyệt cũ ghi các chi tiết mới "đều theo Wikipedia", mà quy tắc `nghien-cuu-su-lieu.md` không coi Wikipedia là nguồn chính.

| Chi tiết trong lời kể | Đoạn | Nguồn thứ hai | Kết luận |
|---|---|---|---|
| Dương Đình Nghệ là tướng cũ họ Khúc, ở Ái Châu | 3, 11 | hoduongvietnam: "một tướng cũ của họ Khúc" | Đã kiểm hai nguồn |
| Ba nghìn người con nuôi (giả tử) | 4, 12, 15, 20, 26 | hoduongvietnam: "nuôi 3.000 giả tử" | Đã kiểm |
| Năm 931 thắng, tự xưng Tiết độ sứ | 15, 23 | giaoduc, hoduongvietnam | Đã kiểm |
| Sáu năm sau (937) Kiều Công Tiễn giết ông | 24 | giaoduc | Đã kiểm |
| Ngô Quyền là con rể | 3, 25, 26 | giaoduc | Đã kiểm |
| Lý Tiến bỏ thành chạy | 18 | hoduongvietnam: "bỏ thành chạy trốn" | Đã kiểm phần "bỏ thành chạy"; phần "bỏ cả lính, cùng các quan, chạy về nước" **chưa kiểm** |
| Lập trường đấu vật, luyện võ lâu dài | 13 | không nguồn nào nhắc | **Chưa kiểm** (chỉ Wikipedia) |
| Trình Bảo đến sau, vây ngược Đại La; Dương Đình Nghệ từ trong thành đánh ra | 19–21 | không nguồn nào nhắc cách diễn biến này | **Chưa kiểm** (chỉ Wikipedia) |
| "Từ đời cha của người vừa bị bắt" (Khúc Hạo) | 23 | hoduongvietnam chỉ nói "tướng cũ của họ Khúc" | **Chưa kiểm**; bỏ |
| Tên tướng Nam Hán: Trình Bảo | 19–22 | hoduongvietnam: "Trình Bảo (hoặc Trần Bảo)"; giaoduc: "Trần Bảo" | **Điểm lệch giữa nguồn** (xem dưới) |

**Điểm lệch cần ghi vào bản gửi duyệt:**
- Tên: Trình Bảo hay Trần Bảo. Bản cũ đã sửa "Trần" thành "Trình" theo Toàn thư và Tư trị thông giám; hai bài báo ngày nay không thống nhất. Đề xuất: giữ "Trình Bảo" (theo sử gốc đã chọn) và ghi rõ lệch trong bảng nguồn.
- Ngô Quyền: giaoduc ghi quân của Dương Đình Nghệ **và Ngô Quyền** đuổi Lý Tiến, giết Bảo năm 931. Lời kể hiện tại (theo góp ý chủ kênh 18/11) không để Ngô Quyền ở trận này. Hai nguồn không mâu thuẫn trực tiếp (lời kể chỉ không nhắc), nhưng đoạn 186026 "cha vợ Ngô Quyền và ba nghìn người con nuôi đuổi giặc" đừng thành câu bị hiểu là Ngô Quyền vắng mặt.

## 3. Đọc theo `giong-van.md` (bản gộp) và tầng 3
| Điểm | Đoạn | Nhận xét |
|---|---|---|
| Chủ ngữ rõ (nhóm 4) | 23 | "Người tướng từng phục vụ họ Khúc…" đứng ngay sau đoạn Trình Bảo bị chém, chủ ngữ không có tên: người nghe có thể hiểu là Trình Bảo hay người khác |
| Diễn giải của người kể (nhóm 5/6) | 26 | "Bạch Đằng có gốc từ Đại La năm ấy" là cách nhìn của người kể nhưng câu viết như khẳng định; bản gửi duyệt cũ ghi "nói rõ là cách nhìn" mà câu không có dấu hiệu đó ("có thể nói", "nhìn lại") |
| Nêu nguồn (nhóm 6) | 13 | "Theo sử cũ" mơ hồ: nguồn nào? Nếu chi tiết chưa kiểm được thì không nên gắn "sử cũ" |
| Kết (nguyên tắc cốt lõi mục 10) | 26 | Kết bằng câu diễn giải rồi "Cảm ơn bạn đã lắng nghe": lời cảm ơn được phép, không bắt buộc; quyết định của chủ kênh (giữ hay bỏ) |
| Hook, chi tiết đáng nhớ, nhịp, rút gọn (tầng 3) | | Hook "người ta thường chỉ nhớ Ngô Quyền" ổn; chi tiết đáng nhớ (ba nghìn con nuôi) là thật và có nguồn; độ dài 3,5 phút hợp nội dung; không phát hiện đoạn lặp để độn thời lượng |

## 4. Bảng đổi đề xuất (chưa áp dụng, chờ chủ kênh duyệt)
| Đoạn | Trước | Sau | Vì sao |
|---|---|---|---|
| 186013 | "Theo sử cũ, ông lập trường đấu vật để họ vật nhau, luyện võ nghệ và tập cách đánh trận suốt một thời gian dài." | "Ông cho họ luyện võ nghệ và tập đánh trận suốt một thời gian dài." (bỏ chi tiết trường đấu vật và "theo sử cũ") | Chỉ một nguồn; quy tắc: không kiểm được hai nguồn thì bỏ; phần "luyện tập" là suy ra hợp lý, nhưng cần nguồn: nếu cũng không kiểm được thì bỏ cả câu |
| 186018 | "Viện binh chưa tới, Lý Tiến đã bỏ cả lính, cùng các quan chạy về nước. Đại La lần đầu được lấy lại." | "Viện binh chưa tới, Lý Tiến đã bỏ thành chạy trốn. Đại La lần đầu được lấy lại." | Hai nguồn chỉ xác nhận "bỏ thành chạy trốn" |
| 186019–186021 | Trình Bảo tới, vây ngược; Dương Đình Nghệ đánh ra | Cần một nguồn thứ hai trước; chưa có thì rút gọn thành một câu nguồn xác nhận: "Viện binh Nam Hán của Trình Bảo kéo tới, Dương Đình Nghệ đánh tan, Trình Bảo chết tại trận." | hoduongvietnam xác nhận Trình Bảo chết tại trận; diễn biến vây ngược chưa kiểm |
| 186023 | "Người tướng từng phục vụ họ Khúc từ đời cha của người vừa bị bắt, nay tự xưng Tiết độ sứ, chức đứng đầu cả vùng mà họ Khúc từng giữ." | "Dương Đình Nghệ, người từng là tướng cũ của họ Khúc, nay tự xưng Tiết độ sứ, chức đứng đầu cả vùng mà họ Khúc từng giữ." | Có tên chủ ngữ; bỏ "từ đời cha" chưa kiểm |
| 186026 | "Bạch Đằng có gốc từ Đại La năm ấy, nơi cha vợ Ngô Quyền và ba nghìn người con nuôi đuổi giặc. Cảm ơn bạn đã lắng nghe câu chuyện này." | "Nhìn lại, có thể nói trận Bạch Đằng khởi đầu từ Đại La năm ấy, nơi cha vợ Ngô Quyền và ba nghìn người con nuôi đuổi giặc." (lời cảm ơn: chủ kênh chọn giữ hay bỏ) | Thêm dấu hiệu diễn giải; lời cảm ơn không bắt buộc |

Nếu chủ kênh duyệt, sửa trong `phim_ban_do/thuymac/viet_tm11.py` (nguồn sinh `tm11_full.json`), chạy lại bộ kiểm, gửi lại toàn văn cổng C. Giọng đọc chưa chạy nên không phải đọc lại.

## 5. Điều thử này cho thấy về quy trình
1. **Bộ kiểm 0 ❌ nhưng kịch bản vẫn có chỗ chưa đủ nguồn.** Tầng 1 phải do Claude tra lại và ghi bảng; công cụ chỉ kiểm có ghi nguồn. Việc tra lại lần này tìm ra bốn chi tiết chưa có nguồn thứ hai và hai chỗ lệch giữa nguồn.
2. **Bản gửi duyệt cũ ghi "theo Wikipedia" cho chi tiết chủ kênh yêu cầu thêm.** Cần quy tắc rõ: chi tiết do chủ kênh yêu cầu thêm vẫn phải qua hai nguồn; không có thì báo lại chủ kênh thay vì thêm vào lời kể. Đề xuất ghi vào `bien-tap.md` (một dòng).
3. **Ba file series thủy mặc còn chữ "rồi lời cảm ơn" cũ** (`thuy-mac.md`, `thuy-mac-khung.md`, `thuy-mac-mau.md`), trái nguyên tắc cốt lõi mục 10. Đã sửa ba dòng thành "tùy chọn, không bắt buộc" trong lần thử này. Mười kịch bản thủy mặc cũ trong `viet_tm*.py` vẫn kết bằng lời cảm ơn; chưa động vào.
4. **Bản gộp `giong-van` dùng được:** các điểm bắt được (chủ ngữ rõ, diễn giải có dấu hiệu, nêu nguồn đúng chỗ) đều có trong bản gộp. Không phát hiện quy tắc nào gượng hay mâu thuẫn với kịch bản đang viết.

## 6. Đính chính (18/11/2026, sau khi tra thêm sáu nguồn để dựng tm11 mới)
Bảng ở mục 2 và mục 4 của file này dựa trên hai bài báo; sau khi tra thêm, hai nhận xét của tôi phải sửa:
- **"Từ đời cha của người vừa bị bắt" (đoạn 186023) là có nguồn**, không phải "chưa kiểm": Toàn thư (qua N1 và N5) ghi Dương Đình Nghệ là tướng của Khúc Hạo, cha của Khúc Thừa Mỹ. Không cần bỏ.
- **"Lập trường đấu vật" (186013) và "Trình Bảo vây ngược, Dương Đình Nghệ đánh ra" (186019–186021):** vây thành rồi bị đánh ra và bị giết tại trận có hai nguồn (N5, N6); trường đấu vật chỉ có N5 (qua Việt sử tiêu án) nên vẫn chỉ một nguồn.
- **Lỗi lớn hơn:** bản cũ nêu năm 930 như chắc và ghi "923 chỉ là cách tính năm cai trị"; theo N1, Toàn thư ghi 923 là năm bắt Khúc Thừa Mỹ. Đây là điểm lệch giữa nguồn mà bản cũ che đi (đoạn 186008, 186009).
- **Tên tướng:** bản cũ ghi đã sửa thành "Trình Bảo" theo Toàn thư; N5 dẫn Toàn thư lại ghi "Trần Bảo".
Bảng đổi ở mục 4 của file này vì thế lạc hậu; thay bằng mạch mới `ke-hoach/tm11-moi-mach-truyen-18-11.md`.

