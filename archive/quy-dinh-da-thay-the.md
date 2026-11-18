# Quy định đã bị thay thế bằng quyết định 18/11/2026

> Sàn 10 phút và câu kết 'tập sau' mặc định đã bỏ; xem quy-tac/dung-mach-truyen.md. Nguồn: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`. Chuyển ngày 18/11/2026.

## Quy định thời lượng (chủ kênh đặt ngày 15/10/2026, áp dụng cho mọi video từ nay)

- Mọi VIDEO DÀI phải dài TỐI THIỂU 10 PHÚT. Đây là mức sàn.
- Lời đọc ít nhất khoảng 1.900 tiếng (giọng Gemini đọc khoảng 3 tiếng/giây), khoảng 70–90 beat, 8–10 chương.
- Thiếu chữ thì thêm chi tiết có nguồn, không độn câu, không lặp ý, không bịa. Chi tiết không chắc thì nói rõ là còn tranh cãi.
- Sau khi dựng, đo thời lượng thật; dưới 10 phút thì bổ sung kịch bản, không đăng.
- Video dọc vẫn 60–80 giây. Quy định này chỉ áp cho video dài.
- Chi tiết đầy đủ: mục "VIDEO DÀI" trong `PROMPT_KICH_BAN.md`.
- `review.py` đã áp mức sàn này: video dài dưới 10 phút báo ⚠️ (vẫn được gửi), dưới 6 phút báo ❌ (không được gửi Telegram).

## Câu kết mời xem tập sau (chủ kênh yêu cầu 06/11/2026, áp dụng loạt "Chuyện cai trị ngàn năm" và mọi video có số tập)
- Sau câu hỏi mở cuối cùng, thêm đúng một đoạn ngắn: "Hẹn bạn ở tập tiếp theo." (khoảng 2 giây, đoạn riêng, không gộp vào câu hỏi). Câu hỏi vẫn là câu gây tò mò mạnh nhất, câu mời chỉ đặt sau nó.
- Cố định một câu cho cả loạt, không đổi chữ giữa các tập. Tập 2 (44016) và tập 3 (45019) đã có.
- Đọc riêng đoạn này (`cum.txt` = 1, giọng Orus, file nhỏ chỉ chứa đoạn mới), ghép vào bản giọng gốc không chỉnh âm thanh, nhận dạng lại, rồi dựng. Cảnh cuối của trang dựng kéo dài đến hết video nên không cần thêm cảnh.
- Tập 1 đã giao trước quy tắc này; thêm vào khi chủ kênh yêu cầu.

## Quyết định 18/11/2026 (chủ kênh, tối): nhập quy tắc từ nhánh khác và câu kết

- **Không nhập nguyên xi `chung.md` của nhánh `lh6-dung-thu`.** Chỉ chuyển mục phù hợp với nguyên tắc cốt lõi 18/11 và không xung đột quy tắc đã duyệt. Không nhập quy tắc cũ chỉ vì nó có ở nhánh khác. Mục "Diễn giải của người kể" (duyệt 01/11) giữ trong `quy-tac/giong-van.md`.
- **Giữ lời bàn của sử gia có ghi rõ tên** khi lời bàn giúp giải thích hoặc làm sáng tỏ câu chuyện. KHÔNG áp dụng quy tắc "bỏ hết lời bình của sử gia" (27/10, nhánh khác).
- **Phân biệt rõ lời sử gia được trích dẫn với diễn giải của người kể.** Không biến lời bàn thành sự thật đã xác minh khi nguồn chỉ là quan điểm của người viết sử.
- **Không mặc định câu kết phải có lời cảm ơn.** Câu cuối khép câu chuyện tự nhiên, có ý nghĩa; lời cảm ơn chỉ dùng khi hợp với cách kết của video. (Dòng "Đoạn cuối gồm một câu tóm gọn và lời cảm ơn" ở mục 10 của `nguyen-tac-cot-loi.md` và kiểm ❌ "thiếu lời cảm ơn chuẩn" ở `kiem_khung.py` trái quyết định này; chờ chủ kênh duyệt bản sửa, xem `ke-hoach/kiem-khung-bang-chi-tiet-18-11.md`.)
- `kiem_khung.py`: chưa duyệt hạ đồng loạt 12 mục ❌; cần xem bảng chi tiết từng mục.
- Giai đoạn 2 theo trình tự: đối chiếu → bản gộp dự thảo → chủ kênh duyệt → mới thay file gốc.

## `kiem_khung.py` sửa 18/11/2026 tối (chủ kênh duyệt)
- Hạ 12 mục cấu trúc từ ❌ xuống ⚠️, giữ nội dung cảnh báo. Mục "phần sau cao trào hơn 5 đoạn" giữ cảnh báo; khi gặp thì đánh giá đoạn kết có cần thiết không, không mặc định cắt.
- Giữ ❌: nhịp chưa ghi sự việc, nhịp chưa ghi nguồn, câu sáo trong `CAM` (34 cụm, chờ phân loại từng cụm, danh sách không đổi).
- Bỏ hẳn kiểm "thiếu lời cảm ơn chuẩn".
- Nói tắt tên phe: bỏ ❌ hàng loạt; chỉ ⚠️ lần đầu khi phe chưa được giới thiệu.
- Thiếu `<mã>_khung.json` hoặc thiếu `n_hua`, `dem`, `hinh_anh`, `soi_chi`: bỏ qua kiểm tương ứng, in dòng ℹ️.
- Bảy mục đã hạ ở `kiem_mo_dau`, `kiem_mach_ke`, `kiem_giong_van`: giữ nguyên, không revert. `kiem_kich_ban.py` giữ giới hạn cứng 32 chữ, 2 câu.
- Thử nghiệm: tm5, tm7, tm9, tm14 (có khung), `bd1`, `dbl1` (không có khung, cấu trúc khác khung cũ), thêm hai khung thử nghiệm đã xóa. tm14: 3 ❌ → 0 ❌ (3 ⚠️).

## 18/11/2026 22:11: mục 10 của nguyên tắc cốt lõi, 34 cụm `CAM`, bản gộp giong-van
- Mục 10 của `nguyen-tac-cot-loi.md` đổi: bỏ "đoạn cuối gồm một câu tóm gọn và lời cảm ơn"; thay bằng "đoạn cuối khép lại câu chuyện tự nhiên, có ý nghĩa; lời cảm ơn chỉ dùng khi hợp với cách kết".
- 34 cụm `CAM` trong `kiem_khung.py`: N2 (⚠️) làm mặc định. N1 ❌: có thể thấy, điều đáng chú ý, quân thuyền. Tạm ❌: câu trả lời nằm ở. Cụm thông dụng (không chỉ, bài học, phía bên kia, dấy binh) chỉ ⚠️ khi một kịch bản dùng từ 3 lần. Công cụ chỉ nêu lý do và gợi ý, không tự sửa câu.
- Phân tầng đánh giá: tầng 1 (sử, niên đại, nguồn) là cổng duyệt của người, công cụ chỉ kiểm có ghi sự việc và nguồn; tầng 2 công cụ bắt dấu hiệu bề mặt, Claude đọc và nêu lý do, đề xuất; tầng 3 là câu hỏi tự rà cho người đọc.
- Dự thảo gộp `giong-van` bổ sung 3 ý (không nghị luận/giáo khoa; không câu hỏi tu từ liên tục; không lặp để kéo dài).
- Thử nghiệm bản chốt `kiem_khung.py`: tm5 (viết tốt), lt1v6 (nhiều cụm bị chê), tm15 (mới nhất). Xem báo cáo trong tin nhắn cùng ngày.

## 18/11/2026 22:25: gộp sáu mục văn phong của `giong-van.md`
Chủ kênh duyệt bản gộp (7 nhóm). Sáu mục cũ giữ nguyên văn dưới đây để tra cứu; không còn áp dụng. Phần "Khung hồ sơ vụ án" chuyển sang `quy-tac/series/sengoku.md`.

> ## Làm kịch bản bằng ngôn ngữ tự nhiên, không giống văn máy (chủ kênh yêu cầu 25/10/2026, áp dụng mọi kịch bản từ nay)
> Người nghe và người đánh giá nhận ra "kịch bản AI" qua cấu trúc lặp, giọng sách giáo khoa và nhắc nguồn liên tục. Viết như người kể chuyện cho bạn bè nghe.
> - **Lời kể không nhắc tên sách và không có câu dẫn nguồn.** Bỏ "Đại Việt sử ký toàn thư chép…", "Sử chép", "Sử ghi", "Sử còn", "Theo sử cũ"; nguồn đưa vào mô tả và bình luận ghim. Chỗ chưa rõ vẫn nói thẳng bằng chữ đời thường ("ta không thể nói chắc", "chuyện này chưa rõ", "người ta kể rằng, nhưng đó là truyền thuyết"). **[ĐÃ BỎ 05/11/2026, xem mục "Nới quy tắc viết kịch bản"]**
> - **Lời bàn vẫn giữ tên sử gia** (Lê Văn Hưu, Ngô Sĩ Liên): đó là ý kiến của người có tên, không phải kết luận của kênh.
> - **Không mở câu cùng một kiểu.** Đếm ba kiểu hay lặp: "Sử…", "Năm…", "Ông…". Mỗi kiểu không quá khoảng 1/10 số câu; đổi bằng chủ ngữ khác, bắt đầu từ hành động, hoặc nối hai câu bằng "nhưng", "rồi", "vì vậy". Không mở hai đoạn liên tiếp bằng cùng một chữ.
> - **Nhịp câu có dài có ngắn.** Xen câu thật ngắn (dưới 8 chữ, nhấn ý: "Không ai chịu nghe lệnh ai.") với câu 20–28 chữ; không để cả đoạn toàn câu cùng độ dài.
> - **Không giải nghĩa kiểu từ điển.** Gộp lời giải vào chính câu ("Hùng trưởng là người mạnh nhất một vùng") thay vì thêm câu "X nghĩa là Y" hay "tức là". Hạn chế cụm "tức", "nghĩa là" (không quá khoảng 5 lần cả video).
> - **Tránh câu khuôn máy:** "Điều đáng chú ý là", "Có thể thấy", "Không chỉ… mà còn", "Đây là một…", liệt kê ba ý đều đặn, câu kết tổng kết sách vở sau mỗi chương. Cuối chương kết bằng việc sắp xảy ra hoặc một câu hỏi, không tóm tắt lại điều vừa kể. **[ĐÃ BỎ 05/11/2026, xem mục "Nới quy tắc viết kịch bản"]**
> - **Dùng chi tiết cụ thể có nguồn thay cho lời khen chung chung** ("ông đánh đâu thắng đó, nên người đời gọi là Vạn Thắng Vương" thay vì "ông là người tài giỏi").
> - **Vẫn giữ mọi quy tắc cũ:** đủ họ tên, năm viết bằng chữ, không nói tắt, không bịa lời thoại, đoạn ngắn 20–30 chữ cho giọng đọc, không câu nào cần đọc hai lần mới hiểu.
> - **Cách làm:** viết xong bản chính xác về sử rồi mới "tự nhiên hóa" (đổi chữ, nhịp, câu mở), không đổi sự kiện, năm, tên, số. Đo bằng `python phim_ban_do/kiem_kich_ban.py <tên>` (0 ❌) và đếm các kiểu câu mở, câu ngắn, "tức/nghĩa là". Làm bản so sánh trước/sau cho chủ kênh duyệt (trang artifact hoặc bảng trong kịch bản) trước khi đọc giọng, vì sửa kịch bản sau khi đọc giọng tốn hạn mức Gemini.
> - Mẫu: `ke-hoach/dinh-bo-linh-kich-ban.md` (bản tự nhiên, 86 đoạn, 2.103 chữ).
>
> ## Câu chữ sáng tạo trong kịch bản (chủ kênh cho phép 11/11/2026 23:09, áp dụng mọi kịch bản mới, nhất là video "Vĩ nhân")
> Sáng tạo ở CÂU CHỮ, không ở SỰ KIỆN. Giữ nghiêm quy tắc "chỉ chuyện có thật, có nguồn" nhưng được kể bằng giọng có hồn.
> - **Được thêm (là lời của người kể):** so sánh và ẩn dụ gần gũi ("nhà đông như cái chợ", "mê như điếu đổ"); cường điệu rõ là cách nói; câu hỏi tự hỏi tự đáp ("Lý do hả? Nhà hết tiền."); câu cảm thán ngắn ("Không!"); nhịp đảo (câu rất ngắn sau câu dài); từ đời thường, khẩu ngữ nhẹ; đối lập ("cậu bé bỏ học năm 10 tuổi, giờ nằm trên tờ tiền lớn nhất"); lời bình hóm hỉnh về tình huống; đặt biệt danh hợp lý cho một sự việc (không cho người thật).
> - **Không được:** gán cho nhân vật một câu nói, suy nghĩ hay cảm xúc không có trong tài liệu (lời bình của người kể phải rõ là của người kể, ví dụ "Ai cũng nghĩ: con nít biết gì mà viết" là lời người kể về thái độ chung, không đặt vào miệng một người cụ thể); thêm hoặc đổi sự kiện, số, năm, tên để câu hay hơn; cường điệu làm sai số liệu ("hàng triệu" khi sử ghi vài nghìn); so sánh đời thường làm lệch bản chất (so sánh số đo chỉ khi phép so đúng).
> - **Mật độ:** khoảng 1 điểm sáng tạo mỗi 3–4 đoạn, mỗi điểm ngắn. Không dồn dập, không câu nào cố gắng quá lộ ra là "ép hài". Hai đoạn liền không cùng một kiểu (hai so sánh liền nhau, hai câu hỏi tự đáp liền nhau).
> - **Giữ quy tắc đùa:** chỉ đùa về tình huống và chi tiết đời thường; không đùa nỗi đau, cái chết, không chê nhân vật; không đùa anh hùng dân tộc Việt Nam; không đùa phía bị hại.
> - **Gửi duyệt:** thêm mục "Câu chữ sáng tạo" liệt kê từng câu, đoạn nào, kiểu gì (so sánh, tự hỏi tự đáp, cường điệu, bình luận), và xác nhận từng câu không thêm dữ kiện, không gán lời hay nội tâm. Chủ kênh duyệt lời chứ không duyệt thay việc kiểm dữ kiện.
> - Vẫn chạy `kiem_kich_ban`, `kiem_mo_dau`, `kiem_mach_ke`, `kiem_gui_duyet`. Đoạn ngắn cho giọng đọc, họ tên đủ, mỗi đoạn một ý lớn vẫn giữ.
>
> ## Viết kịch bản: văn xuôi liền mạch trước, chia đoạn sau (chủ kênh duyệt 12/11/2026, rút từ bản Lâm Đồng `tn11` chủ kênh tự viết; áp dụng mọi kịch bản; khi trùng hoặc mâu thuẫn với mục cũ về câu khuôn, độ dài, mục này ưu tiên)
> Bài học: kịch bản Claude viết thẳng vào khuôn bộ kiểm (mỗi đoạn một mẩu dữ kiện, ≤32 chữ) thành ra chuỗi mốc rời, khó nghe; bản chủ kênh viết văn xuôi trước rồi chia đoạn thì liền mạch, dễ hiểu hơn hẳn. Mẫu: toàn văn bản 4 trong `ke-hoach/tn11-lam-dong-gui-duyet.md`.
> - **Thứ tự làm bắt buộc:** (1) viết cả câu chuyện thành văn xuôi liền mạch như kể cho người chưa biết gì; (2) đối chiếu từng dữ kiện với nguồn, sửa chỗ sai; (3) sau cùng mới chia đoạn cho vừa `kiem_kich_ban.py` (tối đa 32 chữ, 2 câu). Không viết thẳng thành từng đoạn ngắn.
> - **Có xương sống trước khi viết:** nói được câu chuyện trong một câu theo dạng khung (ví dụ "hai tỉnh, rồi hai câu chuyện đi song song, rồi gặp nhau năm 1976"). Thân bài đi theo khung ấy, không đi theo thứ tự mốc của nguồn.
> - **Câu dẫn đường và câu chốt ý được dùng, không tính là câu khuôn:** câu báo bước ngoặt ("Rồi vùng đất này rẽ thành hai câu chuyện."), câu nối ("Trong khi đó", "Vì thế", "Từ đây"), câu chốt sau đoạn phức tạp ("Đà Lạt và Lâm Đồng cứ thế ở hai tỉnh khác nhau."). Điều kiện: giúp người nghe biết mình đang ở đâu trong câu chuyện, không lặp nguyên điều vừa kể, không là lời khen hay kết luận sáo. Câu khuôn bị cấm vẫn là câu không mang thông tin hay hướng đi ("Có thể thấy", "Không chỉ… mà còn", tóm tắt cuối mỗi chương).
> - **Độ dài do mạch truyện quyết định:** không cắt câu giải thích, câu chuyển ý để kịp thời lượng các tập trước. Nếu dễ nghe buộc phải dài hơn khoảng 20% so với các tập cùng loạt, ghi rõ trong bản gửi duyệt và đề xuất đoạn có thể bỏ; chủ kênh quyết.
> - **Ưu tiên hiểu trước, bất ngờ sau:** câu tạo bất ngờ ("Lạ ở chỗ…") chỉ dùng khi người nghe đã nắm được chuyện đang xảy ra.
> - **Kiểm dữ kiện vẫn nghiêm như cũ, kể cả với bản chủ kênh viết:** câu dễ nghe không được thay dữ kiện đúng (bản `tn11` chủ kênh viết có hai chỗ sai về tỉnh Tuyên Đức và Đà Lạt, đã sửa theo tài liệu lưu trữ). Khi sửa bản chủ kênh, giữ nguyên câu chữ và mạch, chỉ đổi chỗ sai dữ kiện hoặc vượt giới hạn bộ kiểm, liệt kê từng chỗ sửa kèm nguồn.
> - **Tự rà trước khi gửi:** đọc liền một mạch từ đầu đến cuối; chỗ nào người nghe phải tự nối hai mốc lại với nhau, chỗ nào một tên mới xuất hiện mà chưa được giới thiệu, thì thêm câu dẫn hoặc câu giới thiệu.
>
> ## Viết lịch sử rõ ràng, đầy đủ, không nói tắt (chủ kênh yêu cầu 23/10/2026, áp dụng mọi kịch bản)
>
> - Lịch sử phải ghi rõ ràng, chi tiết. KHÔNG viết tắt kiểu rút gọn danh từ: nói đủ "thuyền chiến của quân Nguyên" (không "thuyền Nguyên"), "hạm đội của quân Nguyên", "lãnh thổ của nhà Nguyên", "thủy triều lên" / "thủy triều rút xuống" (không "triều lên", "nước rút"), "quân Đại Việt" hoặc tên người chỉ huy (không "người Việt" chung chung khi đang nói về người đánh trận).
> - Khi nói về hiện tượng (thủy triều, mùa mưa, bão), nói luôn hệ quả ngay trong câu để người nghe một lần là hiểu.
> - Khi nhắc một trận đánh, nêu tên người chỉ huy (đủ họ tên) ngay lần đầu, kể cả ở đoạn mở đầu ngắn.
> - Trước khi giao kịch bản, tự rà các cụm danh từ ghép rút gọn ("thuyền X", "đất X", "quân X" khi X là tên nước hoặc triều đại) và viết lại cho rõ.
>
> ## Series Sengoku "Ba người, một thiên hạ" và mọi video sử nước ngoài: viết cho người chưa biết gì (chủ kênh yêu cầu 16/11/2026, áp dụng mọi kịch bản từ nay)
> Bài học: bản 10 và bản 11 đầu có câu tóm tắt quá chặt từ nguồn tiếng Anh ("hai phe quan lớn tranh quyền trong nhà tướng quân", "nhà gác bạc Ginkaku-ji") làm người nghe không hiểu tranh cái gì, nhà gì. Chủ kênh phải tự phát hiện.
> - **Mỗi câu phải trả lời được "ai làm gì, với ai, vì sao".** Không tóm tắt chặt kiểu dịch sát. Gặp câu nguồn ngắn gọn thì mở rộng thành chuyện: ai, chuyện gì, kết quả.
> - **Thuật ngữ, tên tổ chức, địa danh lạ phải giải thích ngay trong câu hoặc câu liền sau** (Gác Bạc là biệt thự nghỉ dưỡng của tướng quân, sau thành chùa; nhà Mori là một đối thủ ở xa; Kantō ở phía đông nước Nhật). Tên mới lần đầu xuất hiện phải có vai trò đi kèm.
> - **Không dùng chữ dịch sát gây hiểu sai** ("quan lớn" thay cho lãnh chúa, "chân xách dép, vị trí thấp nhất"). Dùng đúng vai trò thật và nói rõ vật tranh chấp (tranh chuyện nối ngôi, không "tranh quyền" chung chung).
> - **Kiểm nội bộ trước khi gửi duyệt:** mọi mốc năm, tên, quan hệ phải khớp giữa các đoạn (ví dụ không đoạn nói "chỉ biết chắc từ 1570" mà đoạn khác nói "1557 vào nhà Oda"); chi tiết nhắc lại phải báo "như đã kể".
> - **Không lời nhận định không nguồn và không cực cấp không nguồn** ("mạnh nhất", "nhiều lý do nhất"). Chi tiết chỉ nói đúng điều nguồn nói.
> - **Rà từng câu theo 5 điểm** (ghi kết quả vào bản gửi duyệt): (1) chủ ngữ rõ; (2) ai-với-ai rõ; (3) từ lạ đã giải thích; (4) mốc khớp các đoạn khác; (5) cực cấp và nhận định có nguồn. Đọc như người chưa biết chuyện: câu nào phải đọc hai lần thì viết lại.
> - **Câu nào nghi tóm tắt chặt thì tra lại nguồn gốc trước khi sửa**, không đoán chữ. Ghi nguồn đã đọc vào bản gửi.
> - **Mỗi câu nối câu trước bằng quan hệ nguyên nhân – kết quả hoặc đối lập, không xếp liệt kê (chủ kênh nhắc 16/11/2026).** Dùng "nên", "nhưng rồi", "thế là", "vì vậy" để người nghe thấy chuyện đi đâu. Không viết kiểu "A. Sau đó B. Và C." khi giữa A, B, C có quan hệ nhân quả. Dùng "dòng họ", "phe" cho đúng vai, không "cả nhà".
> - **Thứ tự giải thích: nền trước, hình ảnh sau (chủ kênh nhắc 16/11/2026).** Ví von, ví dụ, câu đùa chỉ đặt SAU khi người nghe đã biết đủ để thấy nó đúng. Không đưa ví von rồi mới quay lại giải thích khái niệm: người nghe hụt nhịp. Thứ tự chuẩn: (1) ai/cái gì, (2) chuyện gì xảy ra, (3) ví von làm điểm nhấn, (4) nguyên nhân hoặc bước tiếp. Khi rà, kiểm từng ví von: đoạn liền trước đã đủ để người nghe hiểu ví von này chưa; đoạn liền sau có quay lại giải thích khái niệm mà ví von đáng ra phải đứng sau không.
> - **Mỗi lần sửa gửi lại toàn bản kèm bảng trước/sau và lý do** (đã có ở mục kiểm kịch bản).
>
> ## Nới quy tắc viết kịch bản (chủ kênh yêu cầu 05/11/2026, thay các điều cũ cùng nội dung)
> Chủ kênh thấy các quy tắc dưới đây quá cứng và yêu cầu bỏ hết. Từ nay KHÔNG áp dụng:
> - Cấm nhắc tên sách hoặc câu dẫn nguồn trong lời kể ("Theo Đại Việt sử ký toàn thư", "sử sách ghi lại", "theo lời chép trong sử" được phép khi cần).
> - Cấm chữ số trong lời đọc (có thể viết "110" hoặc "111"; năm không bắt buộc viết bằng chữ).
> - Cấm ngoặc kép, ngoặc đơn, gạch, hai chấm trong lời đọc (có thể trích lời bằng ngoặc kép).
> - Cấm từ Hán Việt cổ và câu khuôn ("hà khắc", "chiêu dụ", "tiến cử", "sưu thuế", "thái thú", "Câu chuyện cho thấy"…); từ cổ không bắt buộc giải thích ngay.
> - Giới hạn câu đầu tiên tối đa 15 chữ.
> `kiem_kich_ban.py` chỉ còn nhắc (⚠️) về ký tự giọng đọc dễ đọc sai, không chặn (❌) và không kiểm từ cổ.
> Vẫn giữ: đoạn ngắn cho giọng đọc (khoảng 20–30 chữ, tối đa 32, tối đa 2 câu), họ tên đủ, không bịa lời thoại hay nội tâm, độ chính xác dữ kiện theo nguồn (năm, chức, số liệu phải đối chiếu), quy tắc nguồn mục 9, bố cục cuốn hút và các quy tắc khác không nêu ở đây. Chữ số và ngoặc kép có thể khiến giọng Gemini đọc sai: kiểm giọng bằng nhận dạng như thường lệ.
>
