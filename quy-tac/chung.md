# Quy tắc chung (mọi series, mọi video)

Áp dụng cho mọi video và mọi bài đăng của kênh, bất kể series. Quy tắc riêng từng series nằm ở các file cùng thư mục (xem bảng trong `CLAUDE.md`).

## Quy định thời lượng: bỏ mức sàn 10 phút (chủ kênh đổi ngày 30/10/2026, thay quy định 15/10/2026)

- Video dài KHÔNG còn mức sàn 10 phút. Độ dài do nội dung kịch bản quyết định: kể xong câu chuyện thì dừng, không độn câu, không lặp ý, không kéo dài để đủ giờ. Chuyện gọn thì 6–8 phút là đủ; chuyện nhiều tầng thì dài hơn.
- Vẫn phải đủ ý và đủ chi tiết có nguồn để người xem hiểu trọn câu chuyện; thiếu ý quan trọng thì bổ sung, nhưng không bổ sung chỉ để đạt số phút.
- Ưu tiên giữ chân người xem: bố cục theo mục "Bố cục video cuốn hút" bên dưới (hook, xung đột sớm, móc mỗi 60–90 giây).
- Video dọc vẫn 60–80 giây.
- `review.py` (video dài): ngoài khoảng 5–20 phút báo ⚠️ (vẫn được gửi), dưới 3 phút hoặc trên 32 phút báo ❌ (không được gửi Telegram).
- Các nơi cũ còn nhắc "tối thiểu 10 phút", "1.900 tiếng", "70–90 beat" (ví dụ `PROMPT_KICH_BAN.md`, kịch bản cũ) coi như đã bỏ.

## Quy tắc nội dung

- Chỉ chuyện có thật, có nguồn; lời kể có thể cuốn nhưng không được làm sai lệch sự kiện, không bịa lời thoại hay nội tâm.
- Quy tắc viết kịch bản và danh sách điều kiểm: `PROMPT_KICH_BAN.md`, `review_checklist.md`.
- Bình luận ghim Facebook/YouTube (trường `binh_luan`), áp dụng từ tập 3 trở đi; tập 1, 2 và các video đã đăng trước đó giữ nguyên bản cũ: giải thích ngắn nội dung video, KHÔNG đặt câu hỏi hay câu hỏi chọn đáp án (chủ kênh yêu cầu 17/10/2026).

## Bài đăng Facebook (và mọi bài viết đăng mạng): văn phong rõ ràng, mạch lạc, dễ hiểu (chủ kênh yêu cầu 20/10/2026, áp dụng mọi bài post sau)

Người đọc lướt điện thoại, không biết trước chuyện. Bài phải đọc một lần là hiểu.
- **Câu ngắn, một ý một câu** (khoảng 20 từ trở xuống). Đoạn 2–4 câu, cách nhau một dòng trống. Không dồn nhiều số liệu và tên riêng vào một câu.
- **Có đầu có đuôi:** mở bằng điều gây tò mò (1–2 câu) → kể theo thứ tự thời gian hoặc nguyên nhân – kết quả → chốt bằng ý chính và một câu hỏi đơn giản cho người xem. Chia bằng các mục ngắn, có tiêu đề rõ (kèm một emoji), mỗi mục trả lời một câu hỏi ("Hai người là ai?", "Chuyện gì xảy ra hôm đó?", "Vì sao ít người tin?").
- **Từ đời thường.** Thuật ngữ, tên tổ chức nước ngoài, đơn vị lạ phải giải thích ngay bằng tiếng Việt dễ hiểu. Đổi sang đơn vị Việt Nam (mét, ki-lô-mét), không để feet, dặm. Tên tiếng Anh chỉ ghi khi cần, đặt sau cách gọi tiếng Việt. Không chép nguyên câu dịch máy từ tài liệu.
- **Mốc thời gian dạng danh sách ngắn** (mỗi dòng: ngày – chuyện gì xảy ra). Danh sách tối đa 5 dòng.
- **Dẫn chứng gọn trong bài:** nói thẳng "Theo ...", mỗi ý chính một nguồn ngắn. Danh sách nguồn dài và link để ở bình luận, không nhét vào bài.
- **Phân biệt rõ điều chắc chắn và giai thoại:** điều có tài liệu thì kể thẳng; điều còn tranh cãi thì nói "theo lời kể" hoặc "đến nay chưa rõ".
- **Tránh:** câu lồng nhiều ngoặc đơn, chữ viết tắt không giải thích, lặp ý, văn sách giáo khoa, giọng quảng cáo.
- **Tự đọc lại trước khi giao:** thử đọc như người chưa biết chuyện, đọc một lần có hiểu không? Câu nào phải đọc hai lần thì viết lại. Mẫu chuẩn: `telegram/sl21_bai_facebook.txt`.

## Git và quy ước commit (chủ kênh yêu cầu, mọi series)
- Mọi commit dùng `user.email noreply@anthropic.com`, `user.name Claude`. Commit tự động của workflow (`actions@users.noreply.github.com`) bị GitHub gắn "Unverified": đợi hết run đang chạy rồi `git rebase --exec "git commit --amend --no-edit --reset-author -q" <SHA>^` và `git push --force-with-lease=<nhánh>:<SHA từ git ls-remote>`.
- Cảnh báo "commit chưa đẩy" của stop hook thường do tracking ref cũ: chạy `git update-ref refs/remotes/origin/<nhánh> $(git ls-remote origin <nhánh> | cut -f1)` rồi đếm lại.
- **Workflow chỉ chạy khi chủ kênh yêu cầu, và chỉ chạy đúng video được yêu cầu** (chủ kênh nhắc 21/10/2026). Không tự kích hoạt dựng, nhận dạng giọng hay vẽ ảnh. Workflow dựng/nhận dạng chạy khi có push thay đổi file kích hoạt, và push viết lại lịch sử (rebase đặt lại tác giả) làm GitHub coi mọi file là đã đổi nên chạy cả tập 1, 2, Nguyên Mông: khi buộc phải viết lại lịch sử thì commit cuối phải có `[skip ci]` trong tiêu đề.
- Không đẩy lên `main` trừ khi chủ kênh yêu cầu; riêng CLAUDE.md này chủ kênh yêu cầu gộp vào `main` (18/10/2026) để các phiên khác dùng.

## Viết lịch sử rõ ràng, đầy đủ, không nói tắt (chủ kênh yêu cầu 23/10/2026, áp dụng mọi kịch bản)

- Lịch sử phải ghi rõ ràng, chi tiết. KHÔNG viết tắt kiểu rút gọn danh từ: nói đủ "thuyền chiến của quân Nguyên" (không "thuyền Nguyên"), "hạm đội của quân Nguyên", "lãnh thổ của nhà Nguyên", "thủy triều lên" / "thủy triều rút xuống" (không "triều lên", "nước rút"), "quân Đại Việt" hoặc tên người chỉ huy (không "người Việt" chung chung khi đang nói về người đánh trận).
- Khi nói về hiện tượng (thủy triều, mùa mưa, bão), nói luôn hệ quả ngay trong câu để người nghe một lần là hiểu.
- Khi nhắc một trận đánh, nêu tên người chỉ huy (đủ họ tên) ngay lần đầu, kể cả ở đoạn mở đầu ngắn.
- Trước khi giao kịch bản, tự rà các cụm danh từ ghép rút gọn ("thuyền X", "đất X", "quân X" khi X là tên nước hoặc triều đại) và viết lại cho rõ.

## Chạy workflow và Git: bài học từ Hai Bà Trưng và Ngô Quyền (chủ kênh yêu cầu 24/10/2026)
- Job lỗi vì treo bước "Cài đặt" (apt/pip): dùng `gh run rerun <id> --failed` (chỉ chạy lại job lỗi, sau khi run đã kết thúc), KHÔNG hủy cả run. Ghép video dùng workflow riêng không `apt-get update` (`ghep-hbt.yml`, đổi tên cho từng video).
- Dựng video dài chia 16 đoạn song song, có thử lại bước cài đặt. Không chạy nhận dạng, giọng hay dựng khi chủ kênh chưa yêu cầu.
- **Bước cài đặt dùng chung** `.github/actions/cai-dat` (chủ kênh yêu cầu 24/10/2026): ffmpeg chỉ cài khi thiếu, không `apt-get update`, gói pip có cache, mỗi lần tối đa 150–200 giây và thử lại 3 lần. Workflow mới dùng `- uses: ./.github/actions/cai-dat` với `pip: "gói1 gói2"` ngay sau checkout và setup-python, không viết lại bước cài tay.

## Ảnh bìa video: luôn có logo kênh, đặt giống video bản đồ (chủ kênh yêu cầu 24/10/2026, áp dụng mọi bìa sau)
- Mọi ảnh bìa (YouTube, Facebook, TikTok) phải có logo cây đèn `assets/logo/nguoi-gac-su.png`, đặt **giống logo trong video bản đồ** (`mapfilm3.py`): vuông 130 px, độ đậm 0,8, góc trên bên phải, cách mép phải 44 px và mép trên 34 px (khổ 1920 rộng; khổ dọc 1080 dùng cùng cỡ và vị trí). Không phóng to, không đổ bóng, không bỏ.
- Không để chữ hay hình đè lên logo; khung hình bản đồ lấy làm nền phải cắt bỏ khung HUD (hộp năm, chú giải, la bàn, phụ đề) rồi mới đặt chữ.
- Mẫu và mã nguồn: `assets/bia/NQ1/tao_bia.py` (chạy `python assets/bia/NQ1/tao_bia.py <khung.jpg>`; sửa chữ và vùng cắt cho video mới). Kiểm bằng cách xem ảnh bìa ở cỡ lớn trước khi giao.

## Sáng tạo cho đỡ nhàm, nhưng không đổi cốt truyện chính (chủ kênh yêu cầu 24/10/2026, áp dụng mọi video từ nay)
Sử chép khô dễ làm video nhàm. Được phép sáng tạo ở CÁCH KỂ, không được sáng tạo ở NỘI DUNG sử.
- **Được:** mở đầu bằng một cảnh gây tò mò rồi mới kể từ đầu; đảo thứ tự TRÌNH BÀY (nhưng phần thân vẫn đi đúng thứ tự thời gian và nguyên nhân – kết quả); rút gọn chương khô (danh sách chức quan, số quân, chế độ) còn các việc lớn; dồn chất liệu có nguồn vào cảnh xung đột; dùng bản đồ động, hiệu ứng, nhịp đổi cảnh, khung đùa nhẹ về tình huống hoặc quân xâm lược; câu hỏi gợi mở dẫn vào chương.
- **Không được:** đổi, thêm hay bỏ sự kiện chính; đổi kết cục, người thắng thua, nguyên nhân; bịa lời thoại, nội tâm, nhân vật; kể truyền thuyết như sự thật; đảo ngược quan hệ nguyên nhân – kết quả; dùng lời "kết luận" của mình thay cho lời sử (lời bàn phải là của sử gia có tên, ví dụ Lê Văn Hưu, Ngô Sĩ Liên).
- **Cảnh mở đầu gây tò mò phải là sự kiện có thật trong chính video**, sẽ được kể đầy đủ ở chương của nó (không dựng cảnh mở đầu riêng không có trong sử). Phần sáng tạo phải ghi trong kịch bản, mục "Ghi chú độ chắc", để chủ kênh duyệt.
- Mỗi video vẫn trọn gói một chủ đề, không nối sang video khác (chủ kênh 24/10/2026): không có "tập sau", chỉ kết bằng kết cục của chính câu chuyện.
- Video sử Việt vẫn tuân thủ mục "Series lịch sử Việt Nam": hài chỉ nhắm vào tình huống và quân xâm lược, không đùa anh hùng dân tộc.
- Mẫu: `ke-hoach/dinh-bo-linh-kich-ban.md` (mở đầu bằng cảnh Đinh Liễn bị treo trên sào, chương lập triều đình rút gọn).

## Bố cục video cuốn hút: giữ người lạ trong 3 giây đầu và 3 phút đầu (chủ kênh yêu cầu 24/10/2026, áp dụng mọi video từ nay; rút từ số liệu bài Ngô Quyền)
Số liệu video Ngô Quyền (12 phút 57 giây, Facebook): 559 lượt xem, chỉ 21% xem đủ 3 giây, 4% xem quá 1 phút, thời gian xem trung bình 51 giây, 81% người xem chưa theo dõi kênh. Người lạ bỏ đi ngay từ đầu; ai ở lại thì xem khá lâu. Vì vậy bố cục phải thắng ở phần mở đầu.
- **Giây 0–3:** có hình hoặc cảnh gây tò mò và một dòng chữ lớn (video hay tự phát không tiếng). Câu đầu tiên tối đa 15 chữ, không ngày tháng, không tên nước hay tên người lạ. Mẫu tốt: cảnh người cha nhìn con bị treo trên sào (Đinh Bộ Lĩnh).
- **Mở đầu tối đa 40 giây, không lộ đáp án.** Chỉ đặt câu hỏi, chưa nói cách giải (Ngô Quyền đã nói "thủy triều lên rồi sẽ rút" ngay đoạn 4 nên người xem thấy không cần xem tiếp). Không đặt câu giới thiệu nguồn hay lời rào đón ở đoạn đầu; nguồn để ở mô tả và bình luận ghim, hoặc một câu ngắn sau phút đầu.
- **Nhân vật chính và xung đột chính xuất hiện trước 1 phút 30 giây.** Phần bối cảnh trước đó tối đa 2 phút, chỉ giữ điều người nghe cần để hiểu xung đột; mỗi chương dẫn nhập tối đa 4 tên riêng mới. Danh sách tên, chức quan, số quân thì rút gọn hoặc đưa vào bản đồ và chữ trên màn hình.
- **Điểm hấp dẫn nhất (kế sách, trận đánh, bước ngoặt) phải bắt đầu trước 45% thời lượng video**, không để sau phút thứ 8 của video 13 phút.
- **Mỗi 60–90 giây có một "móc" mới:** một câu hỏi, một bước ngoặt, một cảnh hay hình mới. Cuối mỗi chương nêu việc sắp xảy ra hoặc câu hỏi dẫn sang chương sau.
- **Đổi giọng theo chương:** căng ở xung đột và trận đánh, trầm ở mất mát, sáng ở thắng lợi; không để cả video một tone (video Ngô Quyền cả 119 đoạn đều tone "calm").
- **Ảnh bìa:** một người hoặc một cảnh cụ thể, tối đa 4 chữ lớn, có logo kênh. Câu trên ảnh bìa là câu hỏi hoặc điều gây tò mò, không đặt tên chương.
- **Mỗi video dài có kèm một video dọc 60–80 giây** cắt từ cảnh gây tò mò nhất, kết bằng lời mời xem bản đầy đủ. Đây là đường chính kéo người lạ vào kênh.
- **Ghi chú tranh cãi, so sánh nguồn không nằm trong lời kể** mà ở mô tả và bình luận ghim (khớp mục "Viết kịch bản Tam Quốc: kể liền mạch" trong `tam-quoc.md`).
- **Tự kiểm trước khi đọc giọng:** in bảng thời điểm bắt đầu từng chương (tính theo số chữ chia 3 mỗi giây) và kiểm các điểm trên. Ghi kết quả vào mục "Ghi chú độ chắc" của kịch bản để chủ kênh duyệt.
- **Sau khi đăng, ghi lại số liệu (chủ kênh gửi ảnh Insights hoặc kết nối Metricool):** tỷ lệ xem đủ 3 giây, thời gian xem trung bình, tỷ lệ giữ chân ở 1 phút và ở giữa video. Mức tham chiếu của kênh hiện tại là 21% xem đủ 3 giây và 51 giây xem trung bình (Ngô Quyền); đặt mục tiêu cao hơn mức này ở video sau rồi chỉnh theo số liệu.

## Làm kịch bản bằng ngôn ngữ tự nhiên, không giống văn máy (chủ kênh yêu cầu 25/10/2026, áp dụng mọi kịch bản từ nay)
Người nghe và người đánh giá nhận ra "kịch bản AI" qua cấu trúc lặp, giọng sách giáo khoa và nhắc nguồn liên tục. Viết như người kể chuyện cho bạn bè nghe.
- **Lời kể không nhắc tên sách và không có câu dẫn nguồn.** Bỏ "Đại Việt sử ký toàn thư chép…", "Sử chép", "Sử ghi", "Sử còn", "Theo sử cũ"; nguồn đưa vào mô tả và bình luận ghim. Chỗ chưa rõ vẫn nói thẳng bằng chữ đời thường ("ta không thể nói chắc", "chuyện này chưa rõ", "người ta kể rằng, nhưng đó là truyền thuyết").
- **Lời bàn vẫn giữ tên sử gia** (Lê Văn Hưu, Ngô Sĩ Liên): đó là ý kiến của người có tên, không phải kết luận của kênh.
- **Không mở câu cùng một kiểu.** Đếm ba kiểu hay lặp: "Sử…", "Năm…", "Ông…". Mỗi kiểu không quá khoảng 1/10 số câu; đổi bằng chủ ngữ khác, bắt đầu từ hành động, hoặc nối hai câu bằng "nhưng", "rồi", "vì vậy". Không mở hai đoạn liên tiếp bằng cùng một chữ.
- **Nhịp câu có dài có ngắn.** Xen câu thật ngắn (dưới 8 chữ, nhấn ý: "Không ai chịu nghe lệnh ai.") với câu 20–28 chữ; không để cả đoạn toàn câu cùng độ dài.
- **Không giải nghĩa kiểu từ điển.** Gộp lời giải vào chính câu ("Hùng trưởng là người mạnh nhất một vùng") thay vì thêm câu "X nghĩa là Y" hay "tức là". Hạn chế cụm "tức", "nghĩa là" (không quá khoảng 5 lần cả video).
- **Tránh câu khuôn máy:** "Điều đáng chú ý là", "Có thể thấy", "Không chỉ… mà còn", "Đây là một…", liệt kê ba ý đều đặn, câu kết tổng kết sách vở sau mỗi chương. Cuối chương kết bằng việc sắp xảy ra hoặc một câu hỏi, không tóm tắt lại điều vừa kể.
- **Dùng chi tiết cụ thể có nguồn thay cho lời khen chung chung** ("ông đánh đâu thắng đó, nên người đời gọi là Vạn Thắng Vương" thay vì "ông là người tài giỏi").
- **Vẫn giữ mọi quy tắc cũ:** đủ họ tên, năm viết bằng chữ, không nói tắt, không bịa lời thoại, đoạn ngắn 20–30 chữ cho giọng đọc, không câu nào cần đọc hai lần mới hiểu.
- **Cách làm:** viết xong bản chính xác về sử rồi mới "tự nhiên hóa" (đổi chữ, nhịp, câu mở), không đổi sự kiện, năm, tên, số. Đo bằng `python phim_ban_do/kiem_kich_ban.py <tên>` (0 ❌) và đếm các kiểu câu mở, câu ngắn, "tức/nghĩa là". Làm bản so sánh trước/sau cho chủ kênh duyệt (trang artifact hoặc bảng trong kịch bản) trước khi đọc giọng, vì sửa kịch bản sau khi đọc giọng tốn hạn mức Gemini.
- Mẫu: `ke-hoach/dinh-bo-linh-kich-ban.md` (bản tự nhiên, 86 đoạn, 2.103 chữ).

## Câu không được cụt, đoạn phải liền mạch, hook phải giữ bí mật (chủ kênh yêu cầu 26/10/2026, từ kịch bản sáng tạo Lê Hoàn, áp dụng mọi kịch bản từ nay)
- **Không để câu cụt.** Câu phản ứng hay câu kết quả trơ trọi như "Vua Tống cho là phải.", "Tôn Toàn Hưng bị xử tử giữa chợ." phải gộp vào câu trước hoặc thêm chủ thể, lý do, bối cảnh ("Nghe xong, vua Tống thấy kế ấy hợp lý và cho chuẩn bị đưa quân sang."). Câu ngắn chỉ để nhấn có chủ ý hoặc là câu hỏi, và vẫn phải có người, việc, nơi chốn rõ ràng. Bộ kiểm `kiem_kich_ban.py` cảnh báo ⚠️ mọi đoạn dưới 12 chữ; đoạn nào bị cảnh báo thì phải gộp, sửa, hoặc xác nhận là câu hỏi hoặc câu nhấn.
- **Mỗi đoạn phải nối được với đoạn trước.** Không dùng "Đó", "họ", "ông" khi đoạn trước chưa có người hay việc ấy; không giới thiệu nhân vật mới rồi nhảy sang việc khác (giới thiệu "Hầu Nhân Bảo, một quan ở Ung Châu" xong mới kể lá thư). Người hay vật lần đầu nhắc phải có một cụm giới thiệu ("một quan khác tên Lư Đa Tốn").
- **Đừng thêm câu chỉ để nhắc lại điều đoạn sau sẽ nói** (ví dụ "Nhưng cả hai đường tiến quân ấy đều bị chặn lại" trước đoạn kể từng đường). Đoạn sau đã giải thích thì bỏ.
- **Nguyên nhân phải đúng tác nhân.** Việc do bão, do bệnh, do nội bộ thì ghi đúng như vậy; không để người nghe hiểu nhầm là nhân vật chính chiến thắng.
- **Hook đầu video phải giữ bí mật.** Mở bằng một cảnh thật, nêu câu hỏi và hứa trả lời ở cuối video, nhưng KHÔNG liệt kê sẵn các đáp án (ví dụ không kể ra cả bốn "cái giả" ngay từ đầu). Cuối video phải trả lời đúng câu hỏi đã hứa bằng sự việc có thật trong sử, không bằng lời kết luận của người kể. Cách nhấn như "điều đáng nói nhất" ghi vào "Ghi chú độ chắc" để chủ kênh duyệt.
- **Cảnh có người di chuyển hoặc mốc sự kiện nên gọi tên từng lần** ("Đây là cái giả thứ ba") để người nghe đếm theo và có lý do ở lại đến lần cuối.
- Mẫu: `ke-hoach/le-hoan-kich-ban-sang-tao.md` (mã `lh6`).

## Mở đầu mỗi video một kiểu khác, đoạn không cụt (chủ kênh yêu cầu 27/10/2026, từ Lý Công Uẩn)
- **Không lặp cầu nối mở đầu giữa các video.** Câu "Vì sao ...? Muốn trả lời, ta phải bắt đầu từ ..." đã dùng ở Lê Hoàn và nghe dập khuôn với video khác của kênh: cấm dùng lại. Mỗi video chọn một cách vào chuyện riêng; cách chuyển sang quá khứ bằng một câu tương phản hoặc một nơi chốn, không bằng câu hứa "để trả lời thì...".
- **Khuôn mở đầu đã dùng:** Đinh Bộ Lĩnh (cảnh Đinh Liễn bị treo trên sào); Lê Hoàn (bốn cái giả, câu hỏi rồi lùi về đầu truyện); Lý Công Uẩn (cảnh năm 1028 ở cánh cửa Quảng Phúc, thân bài gắn theo nơi chốn, kết quay lại cánh cửa); Nguyên Mông nm2 (Trần Khánh Dư bị xiềng xin khất hai ba ngày, kết trả lời "thứ ông chờ là thuyền lương"); Lý sang Trần lc1 (Lý Huệ Tông ngồi nhổ cỏ, Thủ Độ nói nhổ cỏ phải nhổ cả rễ, kết trả lời vì sao không ai phản đối). Video mới đọc danh sách này và chọn khuôn khác; thêm khuôn mới vào đây.
- **Không để đoạn lẻ ngắn, thiếu đầu thiếu đuôi.** Đoạn nào dưới 14 chữ phải gộp thành đoạn hai vế (câu sau nêu lý do hoặc hệ quả của câu trước), trừ câu hỏi. Mục tiêu 20–30 chữ mỗi đoạn, trung bình khoảng 26. Cảnh báo ⚠️ "ngắn" của `kiem_kich_ban.py` không phải để chấp nhận: gặp thì gộp, không giữ.

## Không dịch thô từ chữ Hán, câu văn liền mạch, có câu hỏi "vì sao" ở đoạn chính (chủ kênh yêu cầu 31/10/2026, áp dụng mọi kịch bản từ nay)
- **Không dùng từ Hán Việt dịch thô, người nghe không hiểu ngay.** Gặp từ cổ hoặc từ chữ Hán trong sử (ví dụ "cấm đình", "thiền vị", "xa giá", "đại xá", "phụ chính", "tôn thất", "thực ấp") thì đổi sang lời đời thường hoặc kể bằng việc làm cụ thể ("nhường ngôi", "vua bỏ kinh thành chạy đi", "tha tội cho cả nước", "người giúp vua điều hành việc nước", "người trong họ nhà vua"). Chức quan, tên đất, tên người thì giữ nguyên, nhưng lần đầu nhắc phải kèm một cụm giải thích ngắn gộp vào câu. Không chép nguyên câu dịch máy của bản Toàn thư.
- **Tự thử:** đọc to từng đoạn như kể cho người không học sử; chỗ nào khựng, chỗ nào phải đoán nghĩa thì viết lại. Soát thêm bằng cách tìm các từ Hán Việt hiếm trong bản nháp trước khi chạy `kiem_kich_ban.py`.
- **Câu văn liền mạch với nhau.** Mỗi câu phải trả lời "rồi sao?" hoặc "vì thế?" của câu trước, nối bằng nguyên nhân, thời gian hoặc đối lập ("vì thế", "nhưng", "đúng lúc ấy", "chưa đầy một tháng sau"). Không xếp các sự kiện rời nhau như danh sách. Cuối đoạn phải dẫn được sang đầu đoạn sau; đọc liền hai đoạn kề nhau phải thấy một mạch.
- **Có câu hỏi "vì sao", "tại sao" ở những đoạn chính.** Mỗi chương có bước ngoặt hoặc quyết định quan trọng nên có ít nhất một câu hỏi ngắn đặt đúng lúc người nghe đang thắc mắc ("Vì sao ông lại chọn đánh trước?", "Tại sao các quan chịu đứng ngoài chờ?"), rồi đoạn kế tiếp trả lời ngay bằng sự việc có thật. Mục tiêu khoảng 1 câu hỏi cho mỗi chương chính, không quá 2 câu hỏi liên tiếp, không hỏi rồi bỏ lửng. Câu hỏi ở hook vẫn theo quy tắc "hook giữ bí mật".
- **Không hỏi giả.** Câu hỏi phải có đáp án nằm trong sử của chính video; không hỏi để rồi trả lời bằng lời kết luận của người kể (xem mục "Sáng tạo cho đỡ nhàm").
- Ghi trong "Ghi chú độ chắc" của kịch bản: danh sách từ Hán Việt đã đổi và vị trí các câu hỏi "vì sao".
