# Series trận đánh thủy mặc (bản dài 16:9 + bản dọc 9:16)

> **Từ 18/11/2026, phần kịch bản của file này đứng dưới `quy-tac/nguyen-tac-cot-loi.md`** (mức ưu tiên cao nhất). Chỗ nào mâu thuẫn thì theo nguyên tắc cốt lõi. Khung nhịp, câu đếm và lời hứa "N lần / N thứ", hình ảnh xuyên suốt, câu hỏi xuyên suốt nay là công cụ tham khảo, chỉ dùng khi hợp với câu chuyện. Quy trình viết là bốn bước của nguyên tắc cốt lõi: tìm câu chuyện, dựng mạch truyện (gửi duyệt), viết lời kể, biên tập.

Quy tắc riêng cho series video trận đánh vẽ kiểu tranh thủy mặc (mực trên giấy). Rút ra từ bản thử Bạch Đằng 938 (`bd1`, `bd2`), chủ kênh góp ý ngày 16/11/2026. Mọi quy tắc chung trong `CLAUDE.md` và các file `quy-tac/` vẫn áp dụng. Chỗ nào file này khác thì đó là ngoại lệ đã được chủ kênh duyệt riêng cho series này.

Mẫu: kịch bản `ke-hoach/thu-giong-hai/bd2_full.json` và `ke-hoach/bd2-bach-dang-thuy-mac-gui-duyet.md`; mã dựng ở `phim_ban_do/thuymac/`. Mẫu lời kể kiểu nói chuyện và bố cục dựng: tập 2 Lê Hoàn phá Tống (`tm2_full.json`, `ke-hoach/tm2-le-hoan-pha-tong-981-gui-duyet.md`, `ke-hoach/tm2-le-hoan-pha-tong-981-bo-cuc-dung.md`, mã `dai_tm2.py`, `amthanh_tm2.py`). Cập nhật 17/11/2026 sau tập 2 và tập 3: các mục 3.1, 3.4, 4.6, 5 và 6 tổng hợp góp ý của chủ kênh trong hai tập này.

## 1. Phạm vi và định dạng
- Mỗi video kể trọn một trận đánh trong sử Việt. Không giới hạn mốc năm (chủ kênh bỏ giới hạn "trước năm 1858" ngày 18/11/2026; các trận chống Pháp như Nhật Tảo 1861, Cầu Giấy 1873 thuộc series). Các tập xếp theo thứ tự thời gian, nhưng mỗi tập phải tự đứng được và không có "tập sau". Ngoại lệ (chủ kênh 25/11/2026): khi một tập kể tiếp chuyện của tập liền trước (ví dụ tm27 sau tm26), được thêm một đoạn ngắn sau hook nhắc "video trước của kênh" để dẫn người xem sang đó; tập vẫn phải tự hiểu được, và vẫn không hứa "tập sau".
- Mỗi trận có hai bản:
  - Bản dài 16:9, khoảng 5–8 phút (1.000–1.300 chữ). Độ dài do nội dung quyết định, không độn chữ.
  - Bản dọc 9:16, 60–80 giây (8–10 đoạn), cắt từ phần trận đánh, kết bằng lời mời xem bản đầy đủ.
- Không cần làm nhanh. Mỗi video phải đủ chi tiết cả lời kể lẫn hình (chủ kênh 16/11/2026).

## 2. Giọng đọc
- Gemini **Charon**, hồ sơ C (`STYLE_C` trong `thu_giong_hai_cum.py`), **đọc từng câu** (`cum.txt` = 1; script `docgiong1*.sh`). Không đọc theo cụm 16 câu nữa. Chủ kênh chọn ngày 16/11/2026 sau khi nghe thử Iapetus, Puck, Charon; lý do là Sadaltager quá trầm, cần giọng to và rõ.
- **Giọng tươi, cao trào rõ (chủ kênh duyệt bản demo tm6 ngày 18/11/2026):** khi đọc cả video, `thu_giong_hai_cum.py` thêm chỉ dẫn theo nhịp khung: cả bài giữ năng lượng sáng, tỉnh như đoạn mở đầu, không trầm buồn ngủ; các đoạn trận, cao trào (nhịp `cao_trao`, `lan*`, `buoc_ngoat`, `the_nguy`) to và mạnh hơn; chỉ `diem_thap`, `lang` được chậm, nhẹ hơn. `style_them.txt` thêm yêu cầu đọc đủ từng câu. Khi trộn, nhạc và hiệu ứng nằm thấp dưới giọng (mức nhạc 0,2 so với giọng, giảm nhạc 70% khi có lời).
- **Bài trên 780 chữ chia đôi** ở ranh giới chương gần giữa nhất: đọc cả tm5 (901 chữ) một lần, Gemini bỏ sót câu hai lần. Sau mỗi lần đọc luôn nhận dạng giọng (`asr_<mã>ca`) để kiểm đủ chữ trước khi giao.
- **Độ to, độ rõ (chủ kênh nhắc 18/11/2026):** file giọng cả video vẫn giữ nguyên bản Gemini, nhưng khi trộn âm phải qua `audio_fx.VOICE_CHAIN` (lọc kiểu radio, nén nhẹ) như các tập tm2–tm4, nếu không giọng nhỏ hơn khoảng 4,5 dB (tm6: −17 LUFS so với tm4 −12,5 LUFS). Cả video một file nên chuỗi lọc không làm lệch giữa các câu. Đã làm trong `amchung.voice_mix`; mức đích khoảng −12 đến −13,5 LUFS.
- **Cả video một lần gọi (17/11/2026, thay cách đọc theo chương):** `doc_chuong.txt` = `ca`. Đọc theo chương vẫn lệch cao độ giữa các chương (tm5: 105–144 Hz); đọc cả video một lần (tm6, 230 giây) cao độ chỉ 111–122 Hz. File `c<số đoạn đầu>.mp3` giữ nguyên, khi dựng chỉ chia ở ranh giới chương theo mốc nhận dạng (`asr_<mã>ca.json`) để chèn thẻ chương. Nhận dạng cả file để kiểm đủ chữ: tm10 lần đầu bị cụt câu cảm ơn cuối nên đã đọc lại.
- **Đọc theo chương (chủ kênh chọn 17/11/2026, thay cách đọc từng câu):** đọc từng câu làm mỗi đoạn một giọng (đo tm5: cao độ 104–139 Hz, tốc độ 3,0–4,0 chữ/giây giữa các câu). Từ tm5 trở đi, `ke-hoach/thu-giong-hai/doc_chuong.txt` = 1: mỗi chương (trường `chuong` trong `<mã>_full.json`) đọc trong một lần gọi, lưu nguyên một file `c<số đoạn đầu>.mp3` (danh sách đoạn ở `chuong_<mã>.json`), không cắt câu, không qua bộ lọc âm. Mốc từng đoạn trong file lấy từ nhận dạng giọng (`khung_dung.align`), dùng cho phụ đề và cảnh. tm5, tm6 đọc lại theo cách này.
- Cả video một giọng, một hồ sơ. Sau khi đọc phải nhận dạng giọng từng đoạn và đạt 100% ở `kiem_giong.py` rồi mới dựng.
- **Không cân giọng (chủ kênh nhắc lại 16/11/2026):** dùng nguyên file gốc Gemini trong `assets/thu_giong_hai/charon/`.
  - KHÔNG chạy `chuan_hoa_giong.py`, không `atempo`, không `loudnorm` từng câu, không cắt lặng, không nén hay giới hạn biên độ giọng. Giọng gốc không lỗi âm điệu; qua cân giọng thì bị lỗi.
  - Khi trộn, chỉ chỉnh mức hiệu ứng và nhạc cho nằm dưới giọng; giọng giữ nguyên.
  - Nhận dạng giọng chạy trên bản sao y nguyên file gốc (chép sang `<mã>_chuan/` mà không xử lý gì, vì workflow nhận dạng đọc thư mục đó).
- **Không tự đọc lại vì tốn hạn mức Gemini.** Chỉ đọc lại những câu nhận dạng sai thật (thiếu chữ, đọc sai năm, sai tên), và phải báo chủ kênh trước khi đọc lại.
  - Lỗi do máy nhận dạng có gợi ý thì kiểm lại bằng bản không gợi ý (`asr_<mã>_ngoai.json`), không đọc lại.
  - Máy nhận dạng hay nghe sai dấu hoặc tên ("ông tưởng" thành "ông Tường", "ông quan" thành "ông Quang" ở tm2). Nếu bản không gợi ý đủ chữ thì không đọc lại, nhưng báo chủ kênh đúng câu ấy để nghe kiểm.
  - Đọc từng câu riêng ngay từ lần đầu, để không phải cắt cụm (cắt cụm 16 câu từng bị lệch câu ở bd2).

## 3. Kịch bản

### 3.1 Khung hook bốn đoạn + "N lần" (cập nhật 17/11/2026 theo tập 2, tập 3) *(tham khảo từ 18/11/2026, xem `nguyen-tac-cot-loi.md`)*
Cả mục này là gợi ý cách mở đầu và dàn bài. Không ép câu chuyện vào bốn đoạn hook hay lời hứa "N lần" nếu làm câu chuyện gượng.
**Ưu tiên số một:** mở ngay vào khoảnh khắc nguy nhất của chính trận đánh (ví dụ cầu phao vừa bắc xong, giặc tràn qua), kể như đang xảy ra, rồi lùi lại bằng một câu tương phản. Sự việc ấy phải có thật và được kể lại đầy đủ ở chương của nó. Ở tm3, chủ kênh chê hai bản hook mở bằng nghịch lý và mối nguy chung chung là "quá hiền". Các bước 1–4 dưới đây áp dụng khi không có khoảnh khắc như vậy, hoặc để dựng phần còn lại của hook.

1. **Đoạn 1: ưu tiên một câu hỏi (chủ kênh 17/11/2026), hoặc một câu kể bằng lời thường như kể chuyện miệng cho bạn bè.** Xem `thuy-mac-khung.md`, hook 1.
   - Mẫu chủ kênh đưa: "có một người nói chiếm nước Việt dễ như bẻ một cành khô, nhưng người đó không biết rằng không phải cành khô nào cũng dễ bẻ như tưởng tượng".
   - Nội dung là một câu nói có thật trong sử, hoặc một nghịch lý của trận đánh ("đang thắng mà lại đề nghị thôi đánh").
   - Không năm cụ thể (bộ kiểm báo lỗi). Cần mốc thời gian thì viết "Hơn một nghìn năm trước". Không tên riêng. Tối đa 25 chữ.
   - Kiểu hai câu hỏi liền nhau (Bạch Đằng) vẫn được dùng, nhưng không lặp lại khuôn đã dùng.
2. **Đoạn 2: lật lại câu ở đoạn 1** bằng một hình ảnh ví hoặc một sự thật ngược ("không phải cành khô nào cũng dễ bẻ", "Ông không thua").
3. **Đoạn 3: tên người, tên nơi, và hệ quả nói mạnh.** Viết "đã phải trả giá bằng chính mạng mình", không viết "không trở về nữa" (chủ kênh chê "nói hiền quá"). Tối đa 4 tên riêng.
4. **Đoạn 4 (tham khảo): câu hỏi "vì sao" và lời hứa "N lần" hoặc "N thứ"** (2–4), chỉ khi câu chuyện thật sự có các lần hoặc các thứ để đếm. Có thể gọi tên vắn tắt ("ngoài biển, trên sông, trong trại"), nhưng không lộ cách đánh.
   - Không dùng "Vì sao...? Muốn trả lời, ta phải bắt đầu từ..." (cấm, xem `giong-van.md`).
   - Không lặp "Câu trả lời nằm ở..." của tập trước.
5. **Thân bài:** mỗi chương mở ra một lần hoặc một thứ, có thể có câu đếm (tham khảo, không bắt buộc) ("Đó là lần thứ nhất cành khô không gãy").
   - Chương bối cảnh viết gọn. Trận nào đã có video riêng của kênh thì rút còn vài đoạn (tm3 rút trận Ung Châu còn ba đoạn).
   - Cuối chương có câu móc: việc sắp xảy ra, hoặc một câu hỏi ở bước ngoặt lớn.
6. **Cao trào:** kể chậm lại ngay trước khoảnh khắc quyết định ("Nếu đó là thật..."), rồi kể dồn sau đó.
7. **Kết:**
   - Kết quả thực tế, hậu quả ngay sau trận.
   - Một đoạn trả lời câu hỏi ở đoạn 4, gọi lại đủ N lần.
   - Câu kết khép câu chuyện tự nhiên, có thể quay lại hình ảnh mở đầu. Lời cảm ơn chỉ dùng khi hợp cách kết, không bắt buộc (`nguyen-tac-cot-loi.md` mục 10, 18/11/2026).
- "N lần / N thứ" là **diễn giải của người kể**. Mỗi lần phải dựng từ sự việc có nguồn, đủ năm điều kiện diễn giải trong `giong-van.md`, và không được nói đó là nguyên nhân duy nhất. Ghi rõ trong "Ghi chú độ chắc".
- Không dùng lại khuôn mở đầu đã dùng. Sau mỗi tập, thêm khuôn vào mục "Khuôn mở đầu đã dùng của series" ở cuối file này.

### 3.2 Chất liệu làm video cuốn hút (vẫn đúng sử)
- **Ưu tiên chi tiết có trong sử mà ít người biết:**
  - Lời can bị gạt đi (ví dụ Tiêu Ích can vua Nam Hán).
  - Lời chủ tướng bàn với các tướng, kể gián tiếp theo sử, không đặt thành lời thoại.
  - Tước hiệu phong sẵn, số liệu sử chép ("chết đuối quá nửa").
- **Mọi chi tiết loại này phải đối chiếu bản dịch chính sử trước khi đọc giọng.** Không đối chiếu được thì ghi rõ nguồn khác ("sử Trung Quốc chép") hoặc bỏ.
- **Một hình ảnh xuyên suốt (tham khảo)** lấy từ chính sử liệu (ví dụ tước Giao Vương), gieo ở mở đầu, nhắc ở cao trào, khép ở câu kết. Chỉ dùng khi sử liệu có sẵn một hình ảnh như vậy; không gài chữ cho đủ số lần.
- **Nhịp kể:** câu ngắn khi hành động, câu dài hơn khi giải thích. Gọi đúng tên phe theo thời (năm 938 là "quân của Ngô Quyền", chưa phải "quân Đại Việt"). Không nói tắt ("thủy triều rút xuống", không "nước rút").
- **Hài:** chỉ nhắm vào tình huống hoặc phía xâm lược, không đùa anh hùng dân tộc (`dna-series.md`).

### 3.3b Người chưa biết sử cũng phải hiểu (chủ kênh nhận xét tm5–tm10, 18/11/2026)
Một số tập mơ hồ với người không nhớ sử. Mỗi video phải tự đứng được, không dựa vào tập trước hay kiến thức sách giáo khoa.
- **Trước khi vào trận (trong khoảng 90 giây đầu) phải trả lời đủ ba câu:** ai đánh ai; vì sao họ đánh nhau; chuyện xảy ra lúc nào, ở đâu (kèm một mốc người nghe quen, ví dụ "hơn bảy trăm năm trước", "vùng Lạng Sơn bây giờ").
- **Không dựa vào tập trước.** Câu như "Ba năm trước, quân nhà Nguyên đã tháo chạy" (tm6) hay "Vương Thông thua ở Tốt Động" (tm8) phải kèm một câu tóm chuyện trước đó.
- **Mỗi tên người lần đầu nhắc phải có một cụm cho biết là ai và thuộc phe nào**: "Thoát Hoan, con trai hoàng đế nhà Nguyên"; "Lê Chiêu Thống, vị vua cuối cùng của nhà Lê". Mỗi phe chỉ gọi tên tối đa ba người; người phụ gọi bằng vai trò ("một viên tướng nhà Minh"). tm7 có tới chín tên người, quá nhiều.
- **Phe phái rối thì có một đoạn "ai đứng về phía ai"** trước khi kể diễn biến (tm9: chúa Nguyễn, nhà Tây Sơn, nước Xiêm; tm10: nhà Lê, nhà Tây Sơn, nhà Thanh). Màn hình hiện thẻ tên phe.
- **Không dùng tên gọi chỉ dân học sử biết** mà không giải thích: Bắc Hà, Đông Quan, Thượng hoàng, Chiêm Thành, Gia Định… lần đầu phải kèm nghĩa ("Đông Quan, tức Hà Nội ngày nay").
- **Kế sách phải giải thích cơ chế bằng lời thường trước khi đánh** (vì sao cọc chỉ lộ ra khi thủy triều rút; vì sao ván phủ rơm ướt cản được tên lửa).
- **Sửa video đã làm bằng đoạn chèn (18/11/2026):** đoạn bối cảnh đặt ở `ke-hoach/thu-giong-hai/<mã>chen_full.json` (trường `sau_doan`; đoạn nào cần sửa câu cho khỏi lệch thì thêm trường `thay` = số đoạn cũ và đọc lại cùng lần gọi). Thẻ tên trận đứng trước phần bối cảnh. Phải ghép thử câu trước, câu sau để tránh kể hai lần hoặc sai mốc (tm9: câu cũ "Mấy năm trước đó" phải thay). `V.NHAN` trong mã dựng hiện nhãn giới thiệu người, đất ở góc trên bên trái.
- **Kiểm trước khi giao:** đọc lại như người chưa học sử; ghi vào "Ghi chú độ chắc" bảng ba câu hỏi (ai, vì sao, lúc nào ở đâu) với số đoạn trả lời, và danh sách tên người kèm cụm giới thiệu.

### 3.4 Lời kể kiểu nói chuyện, giữ độ gay cấn tới cuối (chủ kênh góp ý tập 2, 17/11/2026)
- **Được thêm câu chữ miêu tả, miễn bản chất đúng sử (chủ kênh 24/11/2026, tm23; ưu tiên hơn các câu cũ cấm "thêm hình ảnh"):** không cứng nhắc chép đúng từng chữ của sử. Được viết "xông pha giữa vòng vây quân địch" cho "ra vào trận giặc", "vó ngựa quét qua nhiều nước", "nóng vội" cho "trái lệnh đánh ngay"; được thêm câu chuyển, câu tương phản, câu cảm. Vẫn cấm: thêm hay đổi sự việc, đổi kết cục, nguyên nhân, người thắng thua; bịa lời thoại như lời có thật; số liệu không nguồn; từ lạc thời. Viết một mạch theo giọng kể trước (mẫu: đoạn mở đầu tm23 bản 6), rồi mới chia đoạn và chạy bộ kiểm; không viết câu cụt để qua bộ kiểm.
- **Từ ngữ chiến trận (chủ kênh nhắc 24/11/2026, tm23):** quân ở thế thua thì "rút", "phải rút dần", "bị dồn ép", không "lùi"; không nói "quân ... yếu dần" (nghe như sức khỏe), nói thế trận nghiêng về phía nào. Không gọi quân mình là "chúng", không gọi người là "thứ". Chữ "ông" đứng một mình cũng phải rà: tướng bên xâm lược gọi thẳng tên, kể cả khi bộ kiểm chỉ bắt "ông ta". Không thêm suy đoán về chiến thuật mà sử không chép (tm23 bản 3 từng có "không đánh thẳng vào hàng voi"). Không dùng "nao núng", "cực thịnh" (chủ kênh 24/11). Cảnh có hỏi đáp giữa nhân vật thì kể thành cảnh liền mạch (ai đến, hỏi gì, phản ứng ra sao, chuyển sang người kế tiếp), không xếp từng câu hỏi đáp thành danh sách. Trận thời chưa có súng (trước thời Hồ, cuối thế kỷ XIV) không dùng "tên đạn", "súng", "đạn", kể cả khi bản dịch sử dùng thành ngữ "xông pha tên đạn": viết "mũi tên", "làn tên", "đá, tên".
- **Gọi thẳng tên quan, tướng bên xâm lược (chủ kênh yêu cầu 22/11/2026):** không gọi họ là "ông", "ông ta". Nhắc lại thì dùng đúng tên ("Cao Chính Bình bắt dân nộp thuế", "Triệu Xương sai người") hoặc chức kèm tên; tránh lặp tên quá dày thì đổi câu cho chủ ngữ là việc làm của họ. "Ông" chỉ dùng cho người bên ta, sử gia, người kể chuyện. `kiem_khung.py` báo lỗi khi thấy "ông ta"; chữ "ông" trơn vẫn phải tự rà xem trỏ vào ai. Ví dụ đã sửa: tm16 đoạn 6 (Lục Dận), tm18 đoạn 15 (Dương Tư Húc), tm19 đoạn 8 (Cao Chính Bình) và 19 (Triệu Xương).
- **Viết như kể miệng.** Câu ngắn, từ thường ngày ("nóng ruột", "chắc ăn", "ai biết công cho"). Tham khảo cách sách giáo khoa kể thẳng sự việc. Không viết giọng dịch nguyên từ sách sử.
- **Không nhắc nguồn liên tục trong lời đọc.** Không lặp "sử nhà Tống chép", "sử nước ta chép". Cả video tối đa một hai lần "theo sử cũ", và chỉ ở chỗ cần phân biệt. Chỗ các nguồn chép khác nhau thì để ở "Ghi chú độ chắc".
- **Dùng đúng từ:**
  - "người lên ngôi là...", không "ngai vàng rơi vào tay" (nghe như cướp ngôi);
  - "được phong làm Đại tướng quân", không "được đặt làm";
  - "lấy áo vua khoác lên người", không "áo long cổn, tức là...";
  - "nổi lên", không "dấy binh".
- **Không dùng đại từ chỉ phe mơ hồ** ("bên này", "phía bên kia"). Gọi đúng tên: "nước Việt", "quân Đại Việt", "quân nhà Tống".
- **Hai câu cạnh nhau phải chung một mạch.** Câu sau nối nguyên nhân, kết quả hoặc đối lập với câu trước. Ví dụ bị chê: câu Ngô Quyền cắm cọc năm xưa đặt cạnh câu Lê Hoàn ra chặn giặc mà không có chữ nối; sửa thành "Cách đánh ấy không phải mới."
- **Không câu nghe như văn máy,** ví dụ "Dù sử không nối chúng với nhau, phía ... đã có thêm thời gian".
- **Động cơ phải có nguồn và nói cụ thể.** Ví dụ: "Hai ông quan cùng nói chắc thắng, và vua Tống quyết chớp lấy thời cơ ấy". Không viết trơn "vua Tống nghe theo".
- **Giữ độ gay cấn tới cuối video** (chủ kênh: "càng về sau càng đơn điệu"):
  - mỗi chương có lúc tưởng như phe xâm lược sắp thắng, rồi bị lật lại ("trận đầu trên sông, quân nhà Tống lại thắng... tưởng như lời Lư Đa Tốn sắp thành sự thật. Vậy mà...");
  - câu ngắn mở bước ngoặt ("Mọi việc tưởng đã xong.");
  - kể chậm trước cao trào, kể dồn sau cao trào;
  - các câu này là lời người kể, không gán ý nghĩ cho nhân vật.
- **Những dấu hiệu "văn máy" phải bỏ** (chủ kênh chê ở tm3 bản 2):
  - câu đúc kết chung chung chen giữa mạch kể ("Một đạo quân đông như thế ăn rất nhiều lương", "Phía Đại Việt cũng phải trả giá");
  - câu khen hay câu bài học ở cuối ("làm hòa lúc đang mạnh mà không phải cúi đầu");
  - lặp nguyên khuôn câu đếm ("Đó là lần thứ N quân nhà Tống bị chặn" ba lần): mỗi lần đếm phải nói một cách khác;
  - mở diễn giải bằng "Có thể hiểu vì sao...": nên nói thẳng bằng lời thường ("Sử không chép ông đã nghĩ gì. Nhưng...");
  - một đoạn truyền thuyết đứng riêng, chen ngang mạch trận đánh: phải gắn vào một khoảng lặng của trận, rồi trở lại bằng câu nối.
- **Không bỏ mắt xích nguyên nhân** (chủ kênh chê tm5, 17/11/2026: từ "cho mượn đường là mở cửa cho giặc" nhảy ngay sang "hỏi các bô lão nên đánh hay hòa"). Giữa hai việc phải có đủ việc nối: nhà Trần từ chối, rồi nhà Nguyên lấy cớ đem quân, rồi quân giặc kéo tới biên giới, rồi mới đến lúc vua hỏi các bô lão. Trước khi giao, đọc từng cặp đoạn kề nhau và tự hỏi: vì sao việc sau xảy ra? Câu trả lời có nằm ngay trong đoạn trước không? Không có thì thêm việc còn thiếu (phải có nguồn), không chỉ thêm chữ nối.
- **Người, nơi lần đầu nhắc phải có lý do có mặt** ("Người giữ Gia Định là Nguyễn Ánh, cháu các chúa Nguyễn cũ"; "Quy Nhơn, nơi nhà Tây Sơn đóng đô"). Không dùng "lại" khi trong video chưa có lần trước.
- **Tập có nhiều trận: mỗi trận phải đẩy cao hơn trận trước, không kể nối đuôi** (chủ kênh chê tm5 bản 2, 17/11/2026: "càng về sau càng giảm cao trào… mang tính liệt kê"):
  - mỗi trận có bốn nhịp: thế nguy trước trận; một chi tiết cụ thể có nguồn (ví dụ quân Triệu Trung mặc áo Tống); bước ngoặt; hệ quả đẩy sang trận sau ("Trận đầu đã thắng. Nhưng kinh thành vẫn trong tay giặc…");
  - mức nguy và mục tiêu tăng dần (chặn một cánh quân, rồi lấy lại kinh thành, rồi diệt đạo quân mạnh nhất);
  - chọn một trận làm cao trào và kể chậm lại ("Nhưng trận lớn nhất vẫn còn ở phía trước…"). Các trận khác kể gọn hơn, nhưng không được chỉ còn một câu "đánh tan giặc ở X";
  - nếu có nhiều lần sụp đổ thì mỗi lần một kiểu khác (phục kích chớp nhoáng; vây cho đói; sụp đổ không cần đánh);
  - sau cao trào chỉ còn một đợt dồn cuối (cuộc đuổi, cảnh tháo chạy), rồi kết. Phần đuôi sau trận chính tối đa 3–4 đoạn;
  - không xếp các việc phụ thành danh sách ở cuối (bài thơ, hòm thư, đại cáo, trận đánh mấy năm sau).
- **Kể chậm ngay trước cao trào bằng một đoạn "lặng"** có căn cứ, ví dụ "Thủy triều vẫn đang lên…", "Hai bờ vẫn im, cù lao vẫn im…". Không thêm chi tiết bịa (thời tiết, tiếng động, cảm xúc) chỉ để tạo không khí.
- **Không dịch sát chữ từ bản dịch Toàn thư** (chủ kênh, tm4): "do Trần Quốc Tuấn coi chung" (chữ "tiết chế"), "núng thế", "sắm sửa khí giới". Gặp chữ như vậy thì kể bằng việc làm cụ thể: "do Trần Quốc Tuấn chỉ huy", "yếu thế dần". Người nổi tiếng thì kèm cái tên người nghe quen ("Ông chính là Hưng Đạo Đại Vương sau này").
- **Có một sợi chỉ nối mạch:** mỗi đoạn mở bằng hệ quả của đoạn trước. Ví dụ ở tm3: kế hoạch có chỗ yếu, rồi bị đánh đúng vào chỗ yếu, rồi đoàn thuyền không tới, rồi phải tự bắc cầu, rồi không qua được, rồi đứng chờ, đói và bệnh, rồi bị đánh vào trại.
- **Hình ảnh xuyên suốt (tham khảo)** có thể lấy từ một câu nói có thật ("dễ như bẻ cành khô"). Hình ảnh ấy gieo ở hook, hiện lại ở mỗi lần đếm, rồi khép ở câu kết.

- **Không viết câu cụt kiểu biên niên (chủ kênh nhắc 19/11/2026, tm12).** Không chép nhịp từng vế của Toàn thư, không nối các việc chỉ bằng dấu phẩy, không kết câu bằng động từ trơ ("tan vỡ", "thua liền"). Quy tắc và ví dụ ở `quy-tac/thuy-mac-giong-van.md` mục 5; kiểm bằng `phim_ban_do/kiem_cau_cut.py` (0 ❌).
- **Đại từ phải chỉ đúng người, con số phải cùng một phạm vi (chủ kênh nhắc 18/11/2026, tm14).** Chữ "ông" đứng sau đoạn vừa nhắc một người khác (ví dụ viên chỉ huy phe kia) thì phải gọi lại đủ tên. Hai con số về cùng một nhóm (50 người của một toán, 150 người của cả trận) phải nói rõ mỗi số đếm cái gì. Khi rà, đánh dấu từng chữ "ông", "họ", "toán" và hỏi nó trỏ vào ai.
- **Việc nào kể ra cũng phải có kết quả, và đúng logic trước sau (chủ kênh nhắc 18/11/2026, tm14).** Đã bắt được người thì không còn "dụ hàng"; kể "họ mua chuộc" thì phải nói ông nhận hay không trước khi dẫn câu trả lời. Đọc lại từng cặp đoạn: hành động ở đoạn trước đã có kết quả chưa, và việc sau có còn hợp lý với việc trước không.
- **Mốc thời gian không dựa vào tập khác (chủ kênh nhắc 18/11/2026, tm11).** Mỗi tập xem riêng, nên không viết kiểu "bảy năm trước Bạch Đằng": người xem dễ hiểu là bảy năm trước ngày nay. Mốc tương đối chỉ dùng khi mốc gốc đã nói rõ trong chính tập đó ("sáu năm sau" sau khi đã nêu năm chín trăm ba mươi mốt); ngày tháng của trận chính phải kèm năm.
- **Không dịch thô từ chữ Hán của sử cũ (chủ kênh nhắc 20/11/2026, tm18).** Các chữ như "dấy dân", "mộ quân", "giữ lấy châu", "xưng đế", "hào trưởng", "xuất chúng", "tính kế", "thổi phồng thế giặc để lấy công", "việc thành thì…, không thành thì…" là dịch từng chữ của Toàn thư, Đường thư. Kể lại bằng lời thường: "người của ba mươi hai châu đứng lên theo ông", "gọi được mười vạn người", "chiếm lấy Hoan Châu", "tự lên làm vua", "người có thế lực trong vùng", "nói quân ta đông lên để được thưởng". Lời bàn của sử gia cũng kể lại ý, không dịch câu. Các chữ này đã thêm vào `CAM` trong `kiem_khung.py`.

### 3.3 Hồ sơ gửi duyệt
- **Từ 18/11/2026: trước khi viết lời, gửi mạch truyện theo bước 2 của `quy-tac/nguyen-tac-cot-loi.md` (sự kiện, nguyên nhân, lựa chọn, bước ngoặt, kết quả; chưa viết văn). Chủ kênh duyệt mạch truyện rồi mới viết lời.** Bảng khung theo `quy-tac/thuy-mac-khung.md` (từ 17/11/2026) nay là tham khảo, chỉ lập khi hữu ích.
- File `ke-hoach/<mã>-<tên>-gui-duyet.md` gồm các phần sau:
  - Kịch bản đủ, chia chương, ghi phần trăm thời lượng mỗi chương.
  - 3 phương án hook.
  - Ghi chú độ chắc: nguồn, chỗ các nguồn chép khác nhau, các đoạn diễn giải.
  - Ghi chú kỹ thuật kể chuyện.
  - Tỷ lệ thời điểm biến cố chính.
  - Kết quả ba bộ kiểm.
- `kiem_kich_ban.py`, `kiem_mach_ke.py`, `kiem_mo_dau.py` phải đều 0 ❌. Cảnh báo nào được chấp nhận thì ghi lý do.
- Kịch bản được chủ kênh duyệt rồi mới đọc giọng.
- **Sau kịch bản, gửi bố cục dựng** `ke-hoach/<mã>-<tên>-bo-cuc-dung.md` (chủ kênh yêu cầu ở tập 2):
  - từng đoạn có cảnh, chuyển động, chữ trên màn hình và âm thanh;
  - danh sách tranh mới cần vẽ;
  - ghi chú độ chắc của phần hình (vị trí chưa rõ, cách thể hiện cái chết).

## 4. Hình: tranh thủy mặc
### 4.1 Phong cách
- **Màu:** giấy `#ece2cb` có vân và vết loang; mực `#15130f` với ba mức đậm nhạt; đỏ triện `#a3261c`.
- **Màu đỏ chỉ dùng cho:**
  - triện (năm, tước hiệu);
  - nhãn và đường đi của phe địch;
  - mặt trời;
  - nét gạch tên.
- **Chữ:** Lora, có rung nhẹ cho giống nét cọ.
- **Nhân vật** là bóng mực, không vẽ chi tiết khuôn mặt. Trang phục chung chung theo thời: khăn, mũ quan có hai cánh, mũ trụ, giáo, khiên.
- **Những thứ không vẽ:** cờ có chữ, chữ Hán, vật thời hiện đại.
- **Không có máu.** Cái chết được thể hiện bằng mực đỏ loang, triện rơi hoặc vỡ, thuyền lật chìm.
- **Logo** đặt góc trên bên phải, cỡ 130 px, độ đậm 0,8, như mọi video của kênh.

### 4.2 Bản đồ để chỉ chỗ, tranh để kể việc (chủ kênh nhắc 16/11/2026)
- Bản đồ mực vẽ từ đường bờ biển và sông thật (`mapink.py` dùng `world7.jpg`). Chỉ dùng bản đồ khi lời kể nói về vị trí hoặc đường đi. **Không để quá hai đoạn liền nhau chỉ có bản đồ.**
- **Đoạn kể dàn trận, chia cánh quân, tiến quân, rút quân phải có bản đồ hoặc sơ đồ (chủ kênh yêu cầu 25/11/2026, sau khi xem tm23):** cảnh người đứng, ngựa chạy không cho người xem hiểu "ba cánh vượt sông", "voi hàng đầu, quân bộ phía sau", "lui xuống sông Thiên Mạc". Đường đi của quân dùng bản đồ mực (`map`, điểm mốc `map_pts.json`, cờ đạo quân chạy theo đường); thế trận một trận đánh dùng sơ đồ nhìn từ trên xuống (mẫu `t23n_sodo`: sông chắn ngang, khối quân hai màu, nhãn từng cánh). Khi rà video, đọc từng đoạn lời kể và hỏi: người xem có hình dung được vị trí và hướng đi không? Không thì đổi sang bản đồ.
- **Dựng theo từng câu, có cảm xúc (chủ kênh yêu cầu 25/11/2026, từ tm25; đã áp dụng lại cho tm23, tm24):** mỗi câu lời kể có một góc máy riêng (toàn, trung, cận), không để một cảnh ôm 2–3 đoạn mà người chỉ đứng hoặc đi. Nhân vật múa rối có nét mặt (`mat`: `S` sợ, `G` giận hoặc quát, `V` reo; mảnh `head` + `S/G/V`) và tư thế cảm xúc trong `rig.py` (`so`, `hoang`, `reo`, `quat`, `xung`, `nga`). Cảnh quân giặc thua phải thấy được: mặt sợ, ngả người lùi, vũ khí văng khỏi tay, cờ đổ, bụi, máy quay rung. Nét mặt chỉ đọc được ở cảnh cận, nên lúc quan trọng (đối mặt, quát, sợ) dùng cận. Mẫu: `dai_tm25.py` (đoạn Hàm Tử, cảnh S_A–S_D).
- **Nghe lại giọng ở mọi chỗ ASR lệch chữ** (tm23: giọng chèn thừa "Ngay lúc ấy có người" của câu sau vào trước "giữa hàng quân", chủ kênh phát hiện). Chèn thừa ngắn thì cắt khỏi tệp giọng ở khoảng lặng hai đầu (đo năng lượng âm), dời mốc chữ sau chỗ cắt trong `asr_<mã>ca.json` rồi dựng lại; không cần đọc lại cả bài.
- **Đoạn nào kể một sự việc thì phải có tranh riêng.** Bộ tranh đã có trong `assets.html`:

  | Sự việc | Tranh |
  |---|---|
  | Giết người | sảnh phủ, người ngồi, người cầm kiếm bước ra |
  | Hành quân | hàng quân |
  | Sai sứ | người khiêng hòm |
  | Triều đình địch | ngai, lọng, quan cúi chào |
  | Đánh thành | tường thành, lầu, quân áp sát |
  | Xuất quân | đoàn thuyền rời cảng |
  | Bàn kế | chủ tướng bên án thư, các tướng hai bên |
  | Kinh đô | thành, nhà |

  Tập mới cần sự việc chưa có tranh thì vẽ thêm tranh vào `assets.html`, không dùng bản đồ thay.
- **Mỗi đoạn có ít nhất một chuyển động**, khoảng 3–6 giây có một thay đổi. Các kiểu chuyển động: máy quay trôi hoặc đẩy, quân và thuyền di chuyển, nét cọ vẽ dần, triện đóng xuống, nhãn tên hiện ra.

- **Trong cùng một video, không cảnh nào trùng cảnh khác, và cảnh nào cũng phải có chuyển động (chủ kênh yêu cầu 19/11/2026, áp dụng mọi video thủy mặc từ nay).**
  - **Không trùng:** mỗi tranh chỉ dùng một lần trong video; hai đoạn khác nhau không dùng cùng một tranh, cùng một bố cục hoặc cùng một bản đồ giữ nguyên vùng. Hai đoạn kề nhau cùng nói về một việc thì vẽ hai góc khác (toàn cảnh rồi cận cảnh một vật), không giữ nguyên một tranh để kéo dài. Bản đồ chỉ dùng cho đoạn nói về vị trí, đường đi, mỗi vùng một lần; đoạn kể người, việc dùng tranh vẽ riêng.
  - **Có chuyển động:** không có cảnh tĩnh, kể cả cảnh bản đồ và cảnh tranh có một vật đứng yên. Mỗi cảnh có ít nhất camera trôi hoặc đẩy, cộng thêm ít nhất một thứ trong tranh tự đổi (khói, sương, nước, lửa, quân đi, nét cọ vẽ dần, nhãn hiện ra). Chuyển động phải liên quan nội dung lời đọc ở đoạn ấy; không dùng một hiệu ứng chung cho mọi cảnh.
  - **Kiểm bằng khung hình thật, không chỉ nhìn danh sách cảnh:** (1) với mỗi cảnh, trích khung ở đầu, giữa, cuối và so hai khung cách nhau ba giây: khung giống hệt thì cảnh tĩnh, phải sửa; (2) so khung giữa của mọi cảnh với nhau: hai cảnh giống nhau (cùng nền, cùng vật chính, cùng bố cục) thì phải vẽ lại một cảnh; (3) ghép các khung lên tờ để soi ở cỡ lớn. Trước khi giao nêu cho chủ kênh số cảnh, số tranh khác nhau, và danh sách cảnh còn chưa đạt thay vì tuyên bố đã xong. Mã kiểm: `phim_ban_do/thuymac/kiem_canh.py`. **Chuyển động phải là chuyển động thật trong tranh (chủ kênh nhắc 19/11/2026, tm13 bị chê "toàn cảnh tĩnh"):** máy quay trôi, sương trôi, chữ và triện hiện ra KHÔNG được tính. Mỗi cảnh phải có ít nhất một vật chuyển động gắn với lời kể (người, ngựa, thuyền đi; nước dâng; khói, lửa; nét vẽ hoặc đường tiến quân hiện dần; trên bản đồ có điểm nhấp nháy và đường đi chạy suốt cảnh). `kiem_canh.py` chạy với máy quay đứng yên, tắt sương, chữ, triện, phụ đề; cảnh nào dưới 0,3% điểm ảnh đổi là ❌ TĨNH, tranh dùng cho hơn một cảnh là ❌.

- **Độ chi tiết phải ngang video Ngô Quyền (chủ kênh nhắc 20/11/2026: tm12, tm13, tm16 "quá đơn giản, ít chi tiết"; dựng lại tm13, tm16).** Nguyên nhân đã rút ra: mỗi cảnh chỉ một tấm tranh phẳng; chuyển động chỉ là một hai hình nhỏ đi ngang để qua bộ kiểm; hình nhỏ dùng lại giữa các tập; tranh vẽ sơ sài; chữ lặp lại lời kể thay cho hình. Từ nay mỗi cảnh phải:
  - **Ghép nhiều lớp có chiều sâu:** ít nhất ba lớp vẽ riêng (xa, giữa, gần hoặc vật chính) đặt bằng `put(...,k=)` để trôi khác tốc độ, cộng sương; không dựng cảnh bằng một tấm tranh phẳng duy nhất. Mẫu: `dai.py` (`S_citadel`, `S_council`, `S_battle`, hàm `river`).
  - **Chuyển động kể chuyện, khớp từng câu:** việc gì lời kể nói tới thì việc ấy xảy ra trên hình đúng lúc câu ấy được đọc (dùng mốc câu `sb(n,k)`); mỗi cảnh có ít nhất ba vật chuyển động riêng, mỗi vật có đường đi, nhịp, độ chòng chành riêng (không chạy thẳng đều). Một con chim bay ngang không tính là chuyển động kể chuyện.
  - **Mỗi tập có một hai cảnh trọng tâm dựng riêng** như trận Bạch Đằng (nước triều, cọc, từng thuyền một kịch bản): chọn sự việc đắt nhất của tập và viết hẳn một hàm dựng cho nó, dài cỡ 40–80 dòng.
  - **Hình nhỏ vẽ riêng cho từng tập** (tên `tNN_spr_*`); chỉ được dùng lại hình nhỏ của tập khác cho vật trang trí nền (chim, khói), không cho người, quân, thuyền, voi, ngựa.
  - **Tranh vẽ kỹ:** mỗi tranh chính có tiền cảnh, trung cảnh, hậu cảnh, có chi tiết riêng của câu chuyện (đồ vật, kiến trúc, địa hình); không vẽ vật chính bằng vài hình chữ nhật. Soi từng tranh ở cỡ lớn trước khi dựng.
  - **Chữ đi kèm hình, không thay hình:** chữ trên màn hình chỉ để nêu tên, số, mốc hoặc một ý ngắn hiện đúng lúc giọng nói tới, kèm nét cọ hoặc vật chuyển động; không đặt một dòng chữ tóm lời kể lên một cảnh không có gì xảy ra.
  - **Kiểm:** `kiem_canh.py` (bản 20/11) báo thêm số lớp, số vật chuyển động riêng và hình nhỏ mượn tập khác; cảnh dưới chuẩn là ❌. Trước khi giao, gửi tờ ghép khung giữa của mọi cảnh để chủ kênh so với video Ngô Quyền.
- **Cảnh đánh nhau phải thấy đánh nhau, hai quân phải phân biệt được (chủ kênh nhắc 19/11/2026, tm12 và tm13).** Không dàn lính thành hàng đi qua đi lại. Mỗi cảnh trận: hai quân đứng hai phía nhìn vào nhau, lao vào giáp trận, có tia chớp và bụi ở chỗ giáp nhau, người ngã (không máu), tên bắn từ phía bắn sang phía bị bắn; bên thua bị đẩy lùi đúng như lời kể. Dùng `phim_ban_do/thuymac/tran_fx.py` (`clash`). Màu áo và cờ (quy ước hình ảnh, không phải khẳng định lịch sử): quân Việt đỏ son, quân phương Bắc (Hán, Lương, Tống, Nguyên, Minh, Thanh...) xanh chàm và đội mũ trụ, phe Việt thứ hai trong cùng video vàng đất. Cảnh đầu mỗi trận có nhãn tên hai quân. Một phe giữ một màu suốt cả video, kể cả đám đông, người bỏ đi, người ra hàng, người bị đuổi (tm13 bị chê: quân hai bà lúc đen lúc xanh lúc đỏ); trước khi giao, soi mọi cảnh có người và đối chiếu màu với phe trong lời kể. Hiệu ứng trận chỉ bắt đầu khi lời kể nói tới trận đánh.
- **Nhãn nhịp điều khiển giọng đọc (chủ kênh hỏi 19/11/2026).** Trường `nhip` bắt đầu bằng `cao_trao`, `lan`, `buoc_ngoat`, `the_nguy` làm Gemini đọc to và nhanh hơn. Chỉ gắn cho đoạn trận đánh hoặc lúc quyết định; đoạn phân tích, lời bàn dùng `don_cuoi` hoặc `goc_re`. Năm trong lời đọc ghi thêm bằng chữ số ở trường `tts` (tm12: "năm năm trăm năm mươi bảy" từng bị đọc thành 555); sau khi đọc phải đối chiếu mọi con số trong bản nhận dạng với kịch bản.
- **Mỗi video một bộ cảnh riêng (chủ kênh yêu cầu 17/11/2026).** Tranh kể việc, cảnh trận, cảnh mở đầu, cảnh kết phải vẽ mới cho từng video: khác bố cục, khác địa hình, khác đội hình, khác vật đặc trưng của trận ấy. Không lấy lại tranh của tập trước, kể cả khi hai trận giống nhau (ví dụ tm6 Bạch Đằng 1288 không dùng lại cảnh cọc của tập Ngô Quyền).
  - **Được dùng chung:** nền bản đồ mực (`mapink.py`, đường bờ biển và sông thật, chỉ đổi vùng, mũi tên, nhãn); khung thẻ tựa, vệt chuyển chương, màn kết, phụ đề, logo; mã hiệu ứng (`fx_tran.py`: tên bay, bụi, tia lửa, người ngã) và thư viện âm thanh, nhưng phải đặt vào cảnh mới.
  - **Phong cách giữ nguyên:** tranh thủy mặc theo mục 4.1 (giấy, mực ba mức, đỏ triện, bóng mực, không máu).
  - Trước khi dựng, lập danh sách cảnh của tập và đối chiếu với các tập đã dựng; cảnh nào trùng bố cục thì vẽ lại.

### 4.3 Cảnh trận
- **Cảnh nhiều lớp có thị sai** (lớp xa trôi chậm hơn lớp gần), xếp từ sau ra trước:
  1. núi xa;
  2. sương;
  3. núi gần;
  4. mặt nước có sóng;
  5. cọc hoặc vật cản;
  6. thuyền theo ba hàng xa gần;
  7. vách đá tiền cảnh;
  8. lau sậy ở mép dưới khung hình.
- **Thông tin kế sách** (cọc, thủy triều, phục binh) chỉ hiện ở đúng chương của nó, để giữ bí mật của hook. Trước đó, cọc dưới nước để mờ hẳn.
- **Thủy triều có thước đo** ở góc màn hình. Cọc nhô lên theo đúng mực nước. Thuyền mắc cọc thì treo lại trên cọc rồi nghiêng, lật, chìm, kèm nước bắn.
- **Đoạn giao chiến** có tên bay, máy quay rung nhẹ, quân hai bên áp vào.
- **Mặt cắt lòng sông** dùng để giải thích kế sách: thủy triều lên xuống, cọc được đóng xuống đáy.

### 4.3b Hiệu ứng mực chung và quân (chủ kênh duyệt 19/11/2026, từ tm11m)
- **Áp cho mọi tranh nền** (ảnh rộng từ 1200 px trở lên): nét mực rung và quầng mực thấm (`hieu_ung.mucloang`), sương trôi nhẹ phía dưới (`suong`, rất mờ để không làm nhạt cảnh), tro hoặc bụi mực bay lên từ lửa (`tro`, gắn trong `flame`). Mẫu cài: đoạn "hiệu ứng mực chung" trong `dai_tm11m.py`.
- **Quân giữ nguyên bản tĩnh** (`fig_*` bóng đen, chỉ nhún hoặc di chuyển cả khối). KHÔNG dùng người ghép mảnh `hieu_ung.linh`: thử ở tm11m thấy cứng như người que, tỉ lệ dễ cao kều, không đáng công. Muốn cận cảnh nhân vật sống động thì vẽ riêng từng nhân vật.
- Dựng chậm hơn khoảng 0,8 giây mỗi khung; kiểm mờ sương trên khung thật trước khi dựng cả video.

### 4.3c Màu nước, gió, 30 khung/giây (chủ kênh chọn 22/11/2026 sau bản thử tm21)
- Tô màu nước lên lớp nền sau khi vẽ tranh, trước khi vẽ người (`mau21.to_mau`): trời vàng nhạt, núi xanh chàm, đất xanh ngọc, viền giấy loang nâu; cảnh đêm ngả xanh tím; bản đồ dùng `to_mau_bd` (biển xanh chàm, đất màu giấy). Người giữ màu riêng.
- Lá đỏ, vàng và bụi mực bay chéo qua khung (`mau21.bui`). Tà áo và tua cờ tiết của nhân vật chính bay theo gió bằng uốn hình (`mau21.gio`), nhân vật chính thở nhẹ. Lính vẫn tĩnh theo 4.3b.
- Dựng 30 khung/giây.
- Nhân vật chính và người có tên vẽ dáng riêng (áo bào dài, mũ, vật cầm tay riêng: `quan21`), không phóng to dáng lính rồi đổi màu (chủ kênh nhắc 22/11/2026).
- Chống chồng hình: `lb` vẽ chữ cao hơn tọa độ truyền vào khoảng 65 px, nên dải nhãn trên đặt y=200 (không đè dòng tên góc trái ở y≈64). Bảng chữ phụ đặt ở khối phải. Người đứng cách nhau đủ rộng: tâm cách nhau ít nhất bằng nửa bề ngang hai hình cộng lại. Người đi cùng lúc thì cùng tốc độ. Lớp núi xa và gần chỉ lệch tối đa ±180 px (công thức cũ `seed*60` làm mép lớp lọt vào khung ở các cảnh số lớn).

### 4.4 Mở đầu, chuyển chương, kết
- **Giây 0:** đã có hình và chữ lớn trên màn hình (câu hỏi của hook). Không mở bằng logo hay đoạn giới thiệu.
- **Thẻ tựa** sau hook: vệt mực loang, tên trận và triện năm.
- **Chuyển chương:** vệt mực loang có tên chương. Trong cùng một chương, các cảnh chuyển nhau bằng vệt quét có mép rách.
- **Phụ đề** hiện toàn văn ở dưới khung hình, trên nền giấy mờ.
- **Màn kết:** câu kết viết tay, triện tên trận, tên kênh.

### 4.5 Bản dọc
- Khung 1080×1920. Máy quay đặt cỡ khoảng 1,78 lần để tranh ngang phủ kín chiều cao khung.
- Chữ lớn ở phía trên, phụ đề ở khoảng y = 1650.
- Dùng lại cảnh trận và mặt cắt lòng sông. Cảnh cuối là "Xem bản đầy đủ trên kênh Người Gác Sử".

### 4.6 Những lỗi hình đã gặp, phải soi trước khi giao (tập 2, 17/11/2026)
- **Hướng đi:** người, ngựa, thuyền phải quay mặt theo hướng di chuyển. Đi sang trái thì dùng ảnh lật (`Af(...)`). Ở tm2, ngựa của Hầu Nhân Bảo từng đi giật lùi.
- **Tên bắn:**
  - tên phải bay ra từ người hoặc thuyền đang bắn, theo đường cong thấp, rơi xuống chỗ đối phương;
  - mũi tên quay theo hướng bay;
  - không vẽ tên lơ lửng giữa trời, lệch khỏi thuyền.
- **Cảnh giao chiến phải có hành động, không chỉ rung khung (chủ kênh nhắc 17/11/2026, sau tập 4):**
  - mỗi cảnh đánh nhau có mưa tên của bên đang bắn (bay theo vòng cung tới đối phương, chạm thì có vệt mực nhỏ);
  - có chỗ giáp nhau thì vẽ tia va chạm nhấp nháy; vài người hoặc ngựa ngã (nghiêng rồi nhạt đi, không máu);
  - kỵ binh phi có bụi vó ngựa;
  - âm thanh khớp hình: tiếng tên bay (`volley`) đúng lúc tên bay, tiếng binh khí (`clangs`), tiếng hô, tiếng ngã (`thump`);
  - rung khung chỉ là phần phụ. Hàm dùng chung ở `phim_ban_do/thuymac/fx_tran.py` (`arrows`, `sparks`, `fall`, `dust`).
- **Vùng phụ đề:** nhân vật chính, đoàn quân và nhãn tên phải nằm trên dải phụ đề (khoảng y ≤ 880 trên khung cao 1080). Nhãn không đè lên nhau hay lên người.
- **Nơi chưa rõ vị trí** (Hoa Bộ) thì không đặt lên bản đồ: dùng tranh có chữ tên nơi. Nơi chỉ có vị trí ước đoán (Tây Kết) thì dùng chấm mờ và ghi trong ghi chú.
- **Biểu tượng đếm ở góc** khi lời đọc nói "lần thứ N". Biểu tượng là hình ảnh xuyên suốt cộng vạch đỏ, kèm chữ "LẦN N".
- **Cái chết** thể hiện bằng nhãn tên rơi, nét đỏ gạch tên, mực đỏ loang. Không vẽ cảnh chém.
- **Tranh mới đã có ở tập 2** (`assets.html`):
  - cành khô, nắm tay;
  - điện Hoa Lư có vua nhỏ và rèm;
  - cổng cung;
  - tướng mặc giáp, tướng cầm giáo, quan nhà Tống đứng;
  - người quỳ hàng;
  - ngựa có người cưỡi (tướng, quan);
  - áo vua;
  - đám quân giơ giáo;
  - cuộn thư mở và cuộn thư cuộn;
  - đồng hồ nước;
  - trại quân;
  - đường núi;
  - khu chợ.
- **Mỗi lần vẽ tranh mới**, ghép tất cả lên một tờ để soi ở cỡ lớn trước khi đưa vào cảnh. Sau khi dựng, trích khung ở mọi cảnh có chuyển động hoặc giao chiến.

## 5. Âm thanh
- **Tất cả tự tổng hợp** bằng `sfx.py`, không dùng bản ghi có bản quyền.
- **Âm nền:** sóng, gió nhẹ, hải âu, nước vỗ mạn thuyền.
- **Âm theo hình:**

  | Hình | Âm |
  |---|---|
  | Giọt mực mở đầu | tiếng giọt rơi |
  | Thẻ tựa, thẻ chương | cồng |
  | Triện đóng xuống | tiếng đóng triện |
  | Nét vẽ đường đi | tiếng cọ quét |
  | Đóng cọc | tiếng gỗ |
  | Thủy triều lên, xuống | tiếng nước dâng, rút |
  | Hành quân | bước chân, trống |
  | Giao chiến | mái chèo, tù và, trống dồn, tên bay, binh khí va nhau, tiếng hô |
  | Thuyền lật | gỗ gãy kèm nước bắn |
  | Ngựa | vó ngựa |
  | Trại quân | lửa trại |
  | Đồng hồ nước, chờ đợi | giọt nước |
  | Hình ảnh xuyên suốt bị bẻ, căng | tiếng gỗ căng |
  | Triều đình, đám đông | tiếng xì xào, tiếng hô (không lời) |

- **Nhạc nền:** đàn gảy âm ngũ cung trên nền âm trầm, đổi không khí theo chương:

  | Chương | Không khí |
  |---|---|
  | Mở đầu | căng |
  | Bối cảnh | mờ |
  | Bàn kế | bình |
  | Giao chiến | loạn |
  | Mất mát | buồn |
  | Kết | sáng |

- **Mức âm:** bản chưa có giọng khoảng −16 LUFS. Khi có giọng:
  - giọng giữ nguyên mức gốc của Gemini, không chuẩn hóa về −16 LUFS (mục 2);
  - hiệu ứng và nhạc đặt theo giọng (khoảng 0,3 lần độ lớn trung bình của giọng), chỉ cắt đỉnh của hiệu ứng trong phần trống còn lại, không đụng vào mẫu giọng;
  - hiệu ứng tự giảm khi đang đọc;
  - giữ rõ trống và tù và ở các bước ngoặt;
  - không dùng tiếng xẹt hay mưa rè (chủ kênh từng phàn nàn "nhiều tiếng xẹt xẹt").

## 6. Quy trình mỗi tập
1. Nghiên cứu: lập khung sự kiện, đối chiếu Toàn thư và Cương mục, ghi các chỗ nguồn chép khác nhau.
2. Viết kịch bản theo bốn bước của `nguyen-tac-cot-loi.md` (mạch truyện gửi duyệt trước), rồi biên tập, chạy các bộ kiểm, gửi duyệt kèm 3 phương án hook.
3. Chủ kênh duyệt, rồi Claude đối chiếu lại các chi tiết ít người biết với bản dịch chính sử. Lên bố cục dựng (mục 3.3) gửi duyệt.
4. Đọc giọng Charon (workflow `thu-giong-hai.yml`, chỉ chạy khi chủ kênh yêu cầu), nhận dạng giọng từng đoạn, đạt 100% ở `kiem_giong.py`.
5. Vẽ thêm tranh cho các sự việc mới (`assets.py`). Soi từng tranh ở cỡ lớn.
6. Gắn cảnh theo thời gian thật của giọng: thay thời lượng ước theo số chữ bằng `thoi_luong.json`. Soi tờ ghép khung (`sheet.py`) cho mọi cảnh trước khi dựng cả video.
7. Dựng bản dài và bản dọc bằng `dai_<mã>.py` và `doc_<mã>.py` (24 khung/giây, chia hai tiến trình), trộn âm bằng `amthanh_<mã>.py`, ghép bằng ffmpeg. Thời lượng mỗi đoạn đọc thẳng từ file mp3 gốc (ffprobe).
8. Xem lại video đã dựng: trích khung ở các điểm chuyển cảnh và đoạn cao trào.
9. Làm ảnh bìa có logo, theo `dang-bai-va-bia.md`.
10. Giao cho chủ kênh. Sau khi đăng, ghi số liệu giữ chân người xem.

## 7. Ghi chú kỹ thuật cho Claude
- **So giọng với tập trước trước khi dựng (chủ kênh nhắc 21/11/2026, tm19):** cùng giọng Charon, cùng mô hình và câu chỉ dẫn, Gemini vẫn có lần đọc trầm, chậm, phẳng. Sau mỗi lần đọc, ngoài nhận dạng giọng để kiểm đủ chữ, chạy `python3 phim_ban_do/thuymac/do_giong.py <mp3 tập trước> <mp3 mới>` (cao độ, độ lên xuống, khoảng lặng). Lệch rõ (cao độ thấp hơn từ 4 Hz hoặc độ lên xuống thấp hơn khoảng 10%) thì báo chủ kênh trước khi dựng. Kiểm riêng từng năm trong lời đọc: lần đọc 2 của tm19 đọc "791" thành "779". **Giờ đọc:** chiều 21/11 (16–19 giờ) đọc 9 lần đều trầm, cả kịch bản tm18 đọc lại cũng trầm; sáng sớm và tối muộn (22–8 giờ) các lần đều đạt. Ưu tiên đọc giọng vào khung này; năm dễ đọc nhầm thì ghi bằng chữ trong trường đọc.
- **Nhân vật chính khác hẳn lính (chủ kênh nhắc 21/11/2026, tm19):** không dùng cùng màu khăn, áo, đai của lính cho nhân vật có tên rồi chỉ vẽ to hơn. Nhân vật chính đổi ít nhất hai thứ trong khăn, áo, đai hoặc thêm giáp (tm19: Phùng Hưng giáp sẫm, khăn đen, đai vàng; lính khăn đỏ, áo vải sáng). Tranh đã có sẵn một nhân vật thì cảnh đó không thêm hình rời cùng nhân vật (tm19 cảnh Triệu Xương từng có hai Triệu Xương). Người đi trên bờ không đi ngang qua thuyền vẽ trong tranh.
- **Biển, cuộn sử có chữ đè lên thì không xoay, không lắc**, vì chữ đặt riêng sẽ lệch khỏi biển.
- **Nhánh làm việc dùng sparse checkout.** Khi thêm file mới (kịch bản, giọng, mã), chạy `git sparse-checkout add '<đường dẫn>'` cho đúng mẫu đường dẫn. Nếu không, lần `sparse-checkout add` sau sẽ xóa các file ấy khỏi thư mục làm việc. Ở tm2, `tm2_full.json` từng biến mất vì lỗi này.
- **Cách dựng cho hấp dẫn (chủ kênh chốt 20/11/2026 sau bản thử mở đầu tm17; áp dụng mọi video từ nay, mẫu `dai_tm17.py`):**
  1. **Hình ảnh lặp lại theo điểm nhấn:** chọn một hình gắn với điểm nhấn của nhân vật chính (tm17: khí độc xanh xám `t17_spr_doc`, hàm `khidoc`) và chỉ cho nó xuất hiện ở các lúc lời kể nhắc tới (mở đầu, giữa, cuối), để người xem tự nối. Màu của hình này không dùng cho việc khác.
  2. **Mở đầu như phim:** 1–2 giây đầu là giọt mực rơi trên nền giấy rồi loang ra thành cảnh (hàm `loang`), chữ lớn câu hỏi hook hiện cùng câu đầu, có tiếng giọt rơi và cồng. Không mở bằng logo hay tên kênh.
  3. **Chuyển cảnh bằng mực ở các bước ngoặt:** nét quét có mép rách (`quet`), cuộn giấy mở, triện đóng; không cắt cứng ở chỗ đổi thời gian hoặc đổi nơi.
  4. **Bộ đếm khi câu chuyện có các lần lặp** (ba lần bị đánh, bốn cái giả…): góc màn hình có các ô triện, mỗi lần xong thì đóng dấu ghi kết quả.
  5. **Chia đôi màn hình khi các nguồn chép khác nhau:** hai cuộn sử cạnh nhau, cuộn đang được đọc sáng lên, chữ viết dần theo câu đọc.
  6. **Cận cảnh đồ vật** 2–3 giây ở chi tiết đắt (của đút lót, cổng thành, tờ lệnh) để đổi nhịp.
  7. **Lặng nhịp và âm thanh theo câu:** nhạc lặng ngay trước câu nhấn, tiếng cọ khi quét cảnh, trống khi trận, chỉ còn gió khi khí độc tràn.
  8. **Ánh sáng, mùa theo chương:** đổi tông màu theo tâm trạng (sáng khi lập nước, tối ẩm ở cảnh mất mát), chỉ dùng mùa, giờ có trong sử hoặc là bối cảnh chung không khẳng định sự kiện.
  - Tất cả là cách thể hiện, không thêm sự việc. Trước khi dựng cả video, dựng thử phần hook (đến hết đoạn mở) gửi chủ kênh xem.
- **Cách dựng cảnh nhiều lớp (từ 20/11/2026, mẫu `dai_tm16.py`, `dai_tm13.py`):** mỗi tập vẽ bộ lớp riêng `tNN_far` (núi xa, đặt `k=.35`), `tNN_mid` (đồng, làng, `k=.62`), `tNN_frontL/frontR` (cây tiền cảnh, `k=1.3`, đung đưa), cảnh trong nhà `tNN_inback` (`k=.5`) và `tNN_inL/inR`; sương hai tầng `k=.5` và `1.1`. Tranh vật chính vẽ bản tách nền `tNNx_<tên>` (gọi lại hàm tranh với cờ `NOBG=true`, bỏ `ridge`, `hills16`, `gnd16`) để đặt chồng lên các lớp. Người, quân, thuyền đi bằng hàm `di()` (nhún bước, lắc riêng từng vật, mốc theo câu `sb(n,k)`); lính vẽ bằng `sol16()` (bước chân, áo màu phe, vũ khí riêng); trận dùng `clash(..., pre='tNN_spr_')` với hình nhỏ của tập. Mặt đất của người khoảng y 830–900 để không bị phụ đề che. Phụ đề từng câu không chồng nhau (mờ vào và mờ ra trong khoảng của câu).
- `CLAUDE.md` đã được tái cấu trúc ngày 18/11/2026 (chỉ điều phối); quy tắc chung nằm ở `quy-tac/`. Sửa quy tắc chung: theo mục 5 của `CLAUDE.md`.
- **Bản đồ: điểm đang kể phải nằm giữa khung, không nằm trong dải phụ đề (chủ kênh nhắc 21/11/2026, tm18).** `map.png` chỉ phủ tới khoảng vĩ độ 18,2 nên Hoan Châu, Ái Châu phía nam bị dồn xuống mép dưới và bị phụ đề che. Câu chuyện ở miền Trung trở xuống thì dùng `map_trung.png` (kinh độ 101,2–113,2, tâm vĩ độ 18,9; tạo bằng `phim_ban_do/world8.py` rồi `phim_ban_do/thuymac/mapink_trung.py`, tọa độ ở `map_trung_pts.json`), phía nam xa hơn dùng `map_nam.png`. Khi đặt máy quay, tính vị trí màn hình của điểm chính ở đầu và cuối cảnh: y phải trong khoảng 150–850 (phụ đề chiếm từ khoảng 880 trở xuống), nhãn và mũi tên cũng không đặt dưới 880. Xem lại cảnh bản đồ ở ba thời điểm (đầu, giữa, cuối) trước khi dựng.
- **Hình người vẽ theo kiểu mới, rõ nét (chủ kênh chốt 21/11/2026, áp dụng từ tm18 và mọi tập sau).** Không dùng bóng đen đặc qua bộ lọc `ink` (bộ lọc ấy xô lệch nét khoảng 14 điểm ảnh, làm người nhòe và méo khi phóng to). Vẽ bằng hàm `nguoi18` trong `assets.html`:
  - Viền mực rõ, chân tay vẽ bằng `chi()` (nét mực bên dưới, màu bên trên); thân áo giao lĩnh dài tới gối, tô màu loang và có vạt bóng, nếp áo; mặt nhìn nghiêng có mắt, mũi, tai; khăn quấn hoặc mũ trụ rõ; thắt lưng có dải buông; vũ khí đúng tay cầm.
  - Bộ lọc nhẹ `inkf` (độ xô 2,2, không làm nhòe) chỉ làm sần mép nét.
  - Tên hình bắt đầu bằng `tNNn_` (ví dụ `t18n_ta`), xuất ở độ phân giải gấp ba (`SIZES` có hệ số 3); `engine.asc()` tự nhận tỉ lệ này. Đặt vào cảnh thì chỉnh `s` theo chiều cao thật của hình, không phóng hình cũ.
  - Mỗi phe một dấu hiệu nhìn là nhận ra: quân ta khăn đỏ, thắt lưng đỏ, áo nâu; quân phương bắc mũ trụ có tua, giáp vảy, áo xanh chàm, khiên. Nhân vật chính có dấu hiệu riêng (Mai Thúc Loan: da sạm, khăn đỏ, áo nâu sẫm, đao).
  - **Trang phục nhân vật có tên không được vẽ theo tưởng tượng gây hiểu sai:** không vẽ cởi trần, không vẽ áo bào vua hay giáp riêng nếu sử không chép. Chi tiết nào sử có ghi thì theo sử (Mai Thúc Loan da rất đen; Bà Triệu áo vàng); chi tiết không ghi thì dùng trang phục chung của người cùng thời, cùng phe.
  - Cảnh trận cần thêm các tư thế đi, đâm giáo, ngã và hình nhóm nhiều lính, vẽ cùng kiểu; không trộn người kiểu cũ và kiểu mới trong cùng một video.
  - Mẫu so sánh: `assets/thuymac/nguoi_moi_tm18.jpg`.
- **Nhân vật múa rối ghép mảnh có khớp (chủ kênh chốt 24/11/2026, áp dụng từ tập mới làm sau ngày này; tập đã dựng giữ nguyên).** Vẫn nét và màu của kiểu `nguoi18`, nhưng mỗi người tách thành mảnh (đầu, thân, cánh tay trên, cẳng tay, đùi, cẳng chân, vũ khí) nối ở cổ, vai, khuỷu, hông, gối; ghép và cử động bằng `phim_ban_do/thuymac/rig.py` (mảnh vẽ bằng `rigpart` trong `assets.html`, tên `tNNn_r_<người>_<mảnh>`). Đi thì bước chân theo quãng đường (không trượt), gối gập, tay vung ngược chân; đứng thì thở nhẹ; động tác (giơ gươm, chém, quỳ, ngã, chỉ tay) chuyển dần trong 0,5–1,5 giây, không thay hình. Không dùng hình liền khối trượt ngang cho người ở tiền cảnh. Mẫu: `thu_rig.py` (đoạn so sánh 18 giây).
  - **Mỗi tập, nhân vật chính khác hẳn nhân vật phụ (chủ kênh yêu cầu 24/11/2026):** khác ít nhất hai trong các thứ màu áo, khăn hoặc mũ, đai, giáp, vũ khí, râu; nhân vật phụ có tên cũng khác nhau và khác lính. Không vẽ hai người có tên giống nhau chỉ khác cỡ.
  - **Lính hai bên khác nhau cả trang phục lẫn vũ khí:** không chỉ đổi màu áo. Ví dụ quân ta khăn đỏ, áo vải, giáo dài, khiên mây hoặc không khiên; quân phương bắc mũ trụ có tua, giáp vảy, khiên tròn, đao hoặc kích. Mỗi phe nên có hai, ba kiểu lính (giáo, đao, cung) để hàng quân không giống hệt nhau. Trang phục, vũ khí theo thời kỳ của tập; chi tiết mang khẳng định lịch sử thì theo nguồn hoặc ghi rõ là lựa chọn hình ảnh.
  - Lập bảng nhân vật của tập (tên, vai, màu áo, khăn hoặc mũ, đai, vũ khí) trong hồ sơ gửi duyệt trước khi vẽ.
- **Kiểm trùng trước khi tra nguồn (24/11/2026):** trước khi đề xuất hay lập mạch truyện tập mới, tìm tên trận, tên người chính trong mọi `ke-hoach/thu-giong-hai/*_full.json` và `ke-hoach/*.md` (cả series khác). Nếu một tập đã có kể trận ấy (dù chỉ vài đoạn), báo chủ kênh trước. Lộ trình ghi "MỚI" có thể sai (Lê Hoàn 981 làm lại trùng tm2). Trùng với tập **đã đăng** thì không làm; trùng với tập chưa đăng (ví dụ tm4) thì báo rồi làm theo chủ kênh. Hỏi chủ kênh tập nào đã đăng nếu không chắc.

## 8. Khuôn mở đầu đã dùng của series
- **tm5–tm10 (bài mẫu tm5, 17/11/2026):** câu hỏi đặt thẳng cho người nghe về một lựa chọn: làm vương hay không (tm5), dám nói đánh giặc nhàn (tm6), biết trước ám hiệu (tm7), có đuổi theo (tm8), mời quân nước khác (tm9), hẹn trước ngày ăn mừng (tm10). Tập sau nên đổi kiểu mở đầu.
- **tm11–tm15 (chờ duyệt, 18/11/2026):** đổi khỏi kiểu "câu hỏi lựa chọn": tm11 sự thật bị hiểu nhầm (người ta chỉ nhớ Ngô Quyền), tm12 nghịch lý (đạo quân ban ngày không ai thấy), tm13 số phận nhân vật (không biết chắc hai bà mất thế nào), tm14 sự kiện bất ngờ (năm chiếc ghe áp sát tàu Pháp giữa trưa), tm15 trận chiến (Garnier bỏ thương thuyết, đuổi theo, pháo sa bùn).
- **Bạch Đằng 938** (`bd2`): hai câu hỏi liền nhau ("Làm sao đội quân yếu hơn về chiến thuyền lại đánh tan đoàn chiến thuyền lớn? Vì sao hoàng tử cầm quân không trở về?"), rồi "ba thứ".
- **Lê Hoàn phá Tống 981** (`tm2`): một câu nói có thật kể bằng lời thường ("có một người nói chiếm nước Việt dễ như bẻ một cành khô"), lật lại bằng hình ảnh ví ("không phải cành khô nào cũng dễ bẻ"), rồi "ba lần cành khô không gãy".
- **Như Nguyệt 1077** (`tm3`): mở giữa trận đánh ("Cầu phao vừa bắc xong, một toán quân giặc đã tràn sang bờ nam..."), dừng ở câu hỏi "có giữ nổi bờ nam không?", thêm nghịch lý "người đang thắng lại đề nghị thôi đánh", rồi lùi về một năm trước bằng câu tương phản. Bản 1 (chỉ có nghịch lý) và bản 2 (mối nguy cận kề) bị chủ kênh chê "quá hiền, chưa nổi bật trận đánh". Bài học: hook của series trận đánh nên mở ngay vào khoảnh khắc nguy nhất của chính trận đánh.
- **Đông Bộ Đầu 1258** (`tm4`): mở vào khoảnh khắc vua thua trận hỏi các quan trên thuyền; một người viết "sang nhà Tống", một người đáp "đầu thần chưa rơi xuống đất". Tên người nói ra ở đoạn 4. Câu hỏi để ngỏ: "lời hứa thật, hay chỉ là lời trấn an?".
- **Phùng Hưng 791** (`tm19`, 21/11/2026): mở bằng cách người dân gọi một nhân vật chưa nêu tên ("Người dân không gọi ông là vua. Họ gọi ông ... là cha mẹ"), câu hỏi "ông đã làm gì để được gọi là cha mẹ?", tấm biển gỗ để trống chữ làm hình ảnh lặp lại; đến đoạn 17 mới hiện "Bố Cái": bố là cha, cái là mẹ.
