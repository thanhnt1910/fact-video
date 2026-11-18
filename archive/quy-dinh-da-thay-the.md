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

## 18/11/2026 22:36: gộp ba mục ảnh bìa của `dang-bai-va-bia.md`
Chủ kênh duyệt bản gộp: bìa chính 16:9 (1920×1080); bỏ vùng an toàn y 70–1560 và thông số riêng cho ảnh dọc; mẫu HAN1 và XK (khung dọc) thành tham khảo. Ba mục cũ giữ nguyên văn dưới đây; không còn áp dụng.

> ## Ảnh bìa video: luôn có logo kênh, đặt giống video bản đồ (chủ kênh yêu cầu 24/10/2026, áp dụng mọi bìa sau)
> - Mọi ảnh bìa (YouTube, Facebook, TikTok) phải có logo cây đèn `assets/logo/nguoi-gac-su.png`, đặt **giống logo trong video bản đồ** (`mapfilm3.py`): vuông 130 px, độ đậm 0,8, góc trên bên phải, cách mép phải 44 px và mép trên 34 px (khổ 1920 rộng; khổ dọc 1080 dùng cùng cỡ và vị trí). Không phóng to, không đổ bóng, không bỏ.
> - Không để chữ hay hình đè lên logo; khung hình bản đồ lấy làm nền phải cắt bỏ khung HUD (hộp năm, chú giải, la bàn, phụ đề) rồi mới đặt chữ.
> - Mẫu và mã nguồn: `assets/bia/NQ1/tao_bia.py` (chạy `python assets/bia/NQ1/tao_bia.py <khung.jpg>`; sửa chữ và vùng cắt cho video mới). Kiểm bằng cách xem ảnh bìa ở cỡ lớn trước khi giao.
>
> ## Ảnh bìa dọc 1080×1920: mẫu đã duyệt, dùng cho mọi video cùng bố cục (chủ kênh duyệt 06/11/2026, từ tập 1 "Chín quận")
> Mẫu ảnh: `assets/bia/HAN1/bia_v3.png`. Mã tạo: `python assets/bia/tao_bia_mau.py <cau_hinh.json> [ra.png]`; cấu hình mẫu `assets/bia/HAN1/bia.json` (chạy lại cho ra đúng ảnh đã duyệt, sai khác 0). Tập mới: sao chép `bia.json` sang `assets/bia/<MÃ>/`, đổi chữ, danh sách điểm (kinh, vĩ), `lon0`, `scale`, `oy`.
> - **Bố cục:** bản đồ địa hình phủ kín khung (`map_relief.jpg`), chấm điểm phát sáng ở nửa trên; thẻ đỏ viền vàng góc trái trên (mốc năm); thẻ trắng nghiêng (triều đại hoặc bên chính); tiêu đề hai dòng giữa ảnh (dòng 1 trắng ngà, dòng 2 vàng, dòng 2 là câu hỏi gây tò mò); thẻ tên loạt và số tập; chân trang thương hiệu "NGƯỜI GÁC SỬ" + khẩu hiệu "LỊCH SỬ THEO CHÍNH SỬ". Logo cây đèn góc trên phải đúng quy tắc logo ở mục "Ảnh bìa video".
> - **Chữ chính nằm trong y 70–1560.** Vùng đáy Facebook/TikTok che; chân trang chỉ là thương hiệu. Không để đáy ảnh đen trơn: bản đồ mờ dần sang xanh biển đậm cùng chân trang.
> - **Tiêu đề chữ Việt phải đọc được ở cỡ điện thoại:** phông Oswald 700 cỡ khoảng 206 px; viền ngoài là LỚP RIÊNG phía sau chữ (không dùng `-webkit-text-stroke` trên chữ chính vì ăn mất dấu); khung chữ có padding trên 50 px dưới 60 px để không cắt dấu dưới (Ạ, Ị); hai dòng cách nhau đủ để dấu mũ dòng dưới không chạm dòng trên. Phông Be Vietnam Pro Black quá nhỏ dấu, Anton dính dấu: không dùng cho tiêu đề.
> - **Tự kiểm trước khi giao:** xem ảnh cắt vùng tiêu đề ở cỡ lớn và bản thu 270×480; mọi dấu phải thấy rõ (dấu chấm dưới Ạ, mũ trên Â/Ô, huyền, sắc). Không giao khi chưa kiểm.
> - Phông (OFL) ở `assets/bia/fonts/`. Mẫu cũ `assets/bia/HAN1/tao_bia.py` (nền khung video) giữ để tham khảo, không dùng cho bố cục mới.
>
> ## Ảnh bìa video: đúng cốt truyện và cuốn hút (chủ kênh chốt 10/11/2026, từ bìa #15 Cầu Long Biên bị làm chân dung Eiffel; áp dụng mọi bìa từ nay)
> Bổ sung cho mục "Ảnh bìa video", "Ảnh bìa dọc 1080×1920". Mỗi video chỉ MỘT bìa, không làm nhiều bản cho chủ kênh chọn.
> - **Hình phải đúng cốt truyện video đang nói.** Ảnh chính của bìa là chủ thể của video (cầu Long Biên thì ảnh cây cầu, trống đồng thì ảnh trống). KHÔNG đặt chân dung nhân vật làm ảnh bìa khi chủ thể là vật hoặc công trình, KHÔNG có ngoại lệ ("không thêm ngoại lệ", chủ kênh 10/11/2026). Tên người nhắc trên bìa đi vào chữ, không đi vào hình. Chân dung chỉ dùng khi video kể về chính người đó.
> - **Chọn ảnh:** trước khi làm bìa xem mọi ảnh ứng viên cạnh nhau. Chọn ảnh toàn cảnh, rõ hình dáng đặc trưng, sáng, không bị che quá một phần ba; người lạ nhìn 1 giây phải đoán được chủ đề. Tránh ảnh cận chi tiết (biển tên, đinh tán), ảnh mờ, ảnh có logo kho ảnh. Ảnh chi tiết chỉ dùng khi chính chi tiết đó là điểm gây tò mò.
> - **Bìa phải cuốn hút, gây tò mò, không chỉ minh họa.** Mỗi bìa có MỘT điểm gây tò mò nhìn thấy ngay trên hình: khoanh đỏ vào đúng chỗ của câu hỏi chính kèm dấu "?" (trường `hook=dict(cx, cy, r, q)` trong `assets/bia/XK/tao_bia.py`, tọa độ theo khung 1080×1920), hoặc mũi tên, dấu X đỏ, hình đối lập. Chữ dòng 1 nêu chủ thể, dòng 2 là câu hỏi hoặc điều lạ nhất của video (tối đa 4 chữ mỗi dòng, 2 dòng). Dòng chữ phải khớp điều video sẽ chứng minh; không giật tít sai sự thật. Ảnh được tăng nhẹ tương phản và màu (đã đặt sẵn trong `tao_bia.py`) để nổi hơn trên nền tối.
> - **Khai báo `chu_the`** (vật trong ảnh) trong mục cấu hình bìa; chỉ giao khi `chu_the` khớp tên video. Thẻ tên nhỏ trên ảnh (như "CẦU LONG BIÊN") phải đúng vật trong ảnh.
> - **Bố cục và logo giữ nguyên mẫu đã duyệt** (logo cây đèn, số tập, chữ trong y 70–1560, đáy chỉ thương hiệu). Vòng khoanh và dấu "?" không che chủ thể và không đè logo, thẻ năm, thẻ tên.
> - **Kiểm trước khi giao (bắt buộc):** mở bìa ở cỡ lớn, tự hỏi "chưa biết video, nhìn ảnh này đoán chuyện gì?"; đoán sai hoặc không đoán được thì đổi ảnh. So hình, chữ với tên video và câu 1 kịch bản; kiểm dấu tiếng Việt ở cỡ 270×480. Khi giao ghi một dòng: ảnh dùng (tác giả, giấy phép) và vì sao chọn.

## 18/11/2026 23:15: bỏ mục "Khung 6 câu hỏi để xây kịch bản, rồi chia đoạn" khỏi `dung-mach-truyen.md`
Chủ kênh quyết bỏ. Lý do: mâu thuẫn với `giong-van.md` mục 1 (viết văn xuôi liền mạch trước, chia đoạn sau) và với nguyên tắc cốt lõi mục 4–6: câu "mỗi đoạn chỉ giải quyết MỘT ý chính", "mỗi ý trong khung thành một đoạn 20–30 chữ" kéo người viết viết thẳng thành đoạn, mỗi đoạn một nhiệm vụ (phát hiện khi thử tm11 mới, 18/11). Việc đã làm thay: cổng B (mạch + bảng nguồn từng dữ kiện) và cổng C (bản văn xuôi rồi mới chia đoạn). Bản gốc giữ nguyên văn dưới đây.

> ## Khung 6 câu hỏi để xây kịch bản, rồi chia đoạn (chủ kênh yêu cầu 06/11/2026, áp dụng mọi kịch bản từ nay)
> Trước khi viết lời kể, trả lời đủ 6 câu hỏi dưới đây cho chủ đề của video; sau đó mới chia thành các đoạn nội dung. **Mỗi đoạn chỉ giải quyết MỘT ý chính** (một câu hỏi, hoặc một phần của một câu hỏi).
>
> | # | Câu hỏi | Nội dung cần có |
> |---|---------|-----------------|
> | 1 | Chuyện gì xảy ra? | Sự kiện lịch sử trung tâm, nói gọn một hai câu |
> | 2 | Xảy ra khi nào, ở đâu? | Niên đại, địa danh (kèm vị trí ngày nay nếu giúp người nghe hình dung) |
> | 3 | Vì sao xảy ra? | Nguyên nhân trực tiếp và nguyên nhân sâu xa |
> | 4 | Ai tham gia? | Nhân vật, thế lực, vai trò của từng bên |
> | 5 | Kết quả thế nào? | Thắng bại, thay đổi sau sự kiện |
> | 6 | Có ý nghĩa gì? | Tác động và đánh giá lịch sử |
>
> Cách áp dụng:
> - **Bước 1, lập khung:** ghi ra 6 câu trả lời (mỗi câu vài ý, kèm nguồn) vào đầu file kịch bản, mục "Khung 6 câu hỏi". Câu nào chưa có nguồn thì nói rõ "còn tranh cãi" hoặc bỏ, không bịa cho đủ.
> - **Bước 2, chia đoạn:** mỗi ý trong khung thành một đoạn (20–30 chữ, tối đa 32, tối đa 2 câu). Đoạn nào chứa hai ý thì tách; ý nào cần nhiều câu thì thành nhiều đoạn liên tiếp, mỗi đoạn một ý nhỏ.
> - **Bước 3, sắp thứ tự:** mở bằng điểm gây tò mò lấy từ câu 1 hoặc 5 (đúng quy tắc "cảnh mở đầu là sự kiện có thật"), rồi đi theo thứ tự thời gian và nguyên nhân – kết quả: 2 → 3 → 4 → diễn biến (1) → 5 → 6. Có thể đảo thứ tự TRÌNH BÀY ở phần mở, không đảo quan hệ nguyên nhân – kết quả.
> - **Câu 6 (ý nghĩa, đánh giá):** chỉ dùng lời của sử gia có tên (Lê Văn Hưu, Ngô Sĩ Liên, hoặc tác giả bộ sử đã chốt làm nguồn). Lời đánh giá của kênh không đặt vào lời kể; muốn giữ thì để ở mô tả hoặc bình luận ghim. Không thêm câu "điều này cho thấy…" do kênh tự rút ra (xem các điểm đã gặp ở tập 2, 3).
> - **Tự kiểm trước khi đọc giọng:** lập bảng đoạn → câu hỏi (1–6) nó trả lời. Đoạn nào không thuộc câu hỏi nào thì bỏ hoặc gộp; câu hỏi nào không có đoạn nào thì bổ sung hoặc ghi lý do bỏ. Ghi bảng này vào mục "Ghi chú độ chắc" để chủ kênh duyệt.
> - **Video dọc ngắn:** vẫn dùng khung, nhưng chỉ chọn câu 1, 2 và một trong 3 hoặc 5 làm trục; các câu còn lại nằm ở phần mô tả hoặc ở video khác trong loạt.
> - Khung này bổ sung, không thay thế các quy tắc về nguồn, giọng kể, bố cục cuốn hút, họ tên đủ và đoạn ngắn cho giọng đọc ở các mục trên.
