# Quy tắc vẽ ảnh để giảm lỗi và rút ngắn thời gian (chủ kênh yêu cầu 03/11/2026, áp dụng mọi video từ nay)

Mục tiêu: ít vòng vẽ lại, không vẽ lại cả tập, không giao ảnh chưa kiểm. Bổ sung cho mục "Vẽ ảnh: tự kiểm và tự vẽ lại" và "Lỗi ảnh hay gặp" trong CLAUDE.md.

## A. Viết prompt: tả điều cần có, bỏ vật dễ sinh lỗi
1. **Câu cấm gần như vô tác dụng** ("no text", "no border", "no chair"): mô hình hay vẽ đúng thứ bị cấm. Muốn không có vật nào thì KHÔNG nhắc vật đó, đổi sang cách tả khác hoặc bỏ cảnh phụ.
2. **Bảng vật dễ lỗi và cách thay** (thêm dòng mới khi gặp lỗi mới, đây là nguồn duy nhất để bộ tạo prompt dùng):
   | Dễ lỗi | Lỗi gặp | Thay bằng |
   |---|---|---|
   | Cuộn tre, sách, giấy, hộp, rương có hoa văn, biển, bia | Sinh chữ lạ | Không đặt vào cảnh; nếu cần chỉ để xa, nhỏ, hoặc đặt "bàn trống" |
   | Ghế tựa, giường khung gỗ, bàn cao | Đồ hiện đại / kiểu Hàn | Chiếu trải đất, bục thấp, đệm đỏ trên bục, bàn thấp trơn |
   | Đèn, đèn lồng, đèn đứng | Đèn thủy tinh, đèn đường | "Han bronze oil dish (shallow open bowl, tiny flame)" hoặc bỏ đèn |
   | Cửa sổ | Kính, khung hiện đại | "wooden lattice window, no glass" hoặc không tả cửa sổ |
   | Giáp lính | Giáp tấm bạc kiểu Tây, chữ trên giáp | "dark leather lamellar armour, plain surfaces"; lính nhỏ ở xa |
   | Cờ, biểu ngữ | Chữ, biểu tượng | "plain blank cloth banner" |
   | Tay cầm vật | Thừa tay | Tay giấu trong tay áo, vật cắm giá hoặc đeo hông |
   | Nhiều người cạnh nhau | Hai người giống hệt | Ghi từng người một đặc điểm khác nhau |
   | Cảnh một người | Mọc thêm người | "exactly ONE man only ... no second figure, no crowd" |
   | Cảnh vật trống | Mọc người | "completely empty, absolutely no people" |
3. **Viền khung:** luôn thêm "single full-frame picture, full-bleed, no panels". Cảnh trong phòng hay ra viền đen nhất: ưu tiên cảnh ngoài trời hoặc góc rộng.
4. Prompt ≤ 2.000 ký tự; thứ tự: cảnh, nhân vật, ảnh tham chiếu, hậu tố Hán ngắn.

## B. Quy trình vẽ: vẽ thử rồi mới vẽ cả tập
1. **Vẽ thử 10 cảnh đại diện trước** (phòng trong, ngoài trời, đông người, vũ khí, cảnh trống, đêm). Soi xong, sửa prompt chung hoặc bảng ở mục A, mới vẽ phần còn lại.
2. **Vẽ dư khoảng 10%** vào các cảnh thuộc loại hay hỏng (phòng có bàn, cảnh có giáp, cảnh đông người) để thay ngay khi có ảnh lỗi, không chờ thêm một vòng chạy.
3. **Cảnh quan trọng vẽ 2 bản** (đổi `dot`), chọn bản tốt.
4. **Script vẽ không được bỏ qua ảnh có sẵn mà báo "ĐẠT":** muốn vẽ đè phải xóa ảnh cũ (cất sang `_loi/`) hoặc dùng `lam_lai`. Sau mỗi lần chạy phải kiểm số ảnh thật sự mới được vẽ (ngày giờ file, hoặc log "đã vẽ N ảnh"), không tin dòng "ĐẠT".
5. Xóa ảnh lỗi trước khi đẩy lệnh vẽ lại, đẩy prompt mới lên nhánh TRƯỚC khi chạy workflow, và xác nhận `git ls-remote` khớp `HEAD` (một lần đã chạy với prompt cũ vì đẩy lỗi).
6. Lỗi cả loạt thì sửa prompt chung, không vẽ lại từng ảnh một.

## C. Lọc tự động trước khi soi mắt (bắt lỗi đo được, rẻ, không dùng Gemini)
- **Viền khung:** dải 8–12 px ở bốn mép gần một màu tối/đen khác hẳn bên trong → loại.
- **Chữ:** chạy OCR (tesseract) vùng giữa ảnh; có ký tự chữ cái hoặc CJK với độ tin cậy cao → loại.
- **Ảnh trùng hoặc gần trùng** với ảnh khác trong cùng video (đã có trong `ve_kiem_anh.py`).
- Bản nào qua lọc mới đưa vào soi mắt ở cỡ lớn (tối đa 6 ảnh một tấm).
- Soi mắt vẫn bắt buộc cho lỗi tay thừa, người giống hệt, vật hiện đại, ngựa méo; Gemini chỉ là phụ.

## D. Ghi lại để lần sau khỏi lặp
- Mỗi đợt vẽ: ghi số ảnh vẽ, số ảnh lỗi theo loại (chữ, viền, hiện đại, thừa người...) vào `logs/kiem_2d/<MÃ>_tong_hop.txt`.
- Lỗi mới chưa có trong bảng ở mục A thì thêm dòng vào bảng ngay trong cùng phiên.
- Khi soạn kế hoạch ảnh cho video mới, ưu tiên cảnh có người, ngoài trời, góc rộng; hạn chế cảnh phòng trống chỉ có bàn và vật. Ngoại lệ là ảnh minh họa ẩn dụ ở mục E: ảnh vật có chủ ý, không bị hạn chế này.

## Kịch bản phải tự kiểm trước khi gửi chủ kênh (chủ kênh yêu cầu 03/11/2026, áp dụng mọi kịch bản từ nay)
- Không gửi kịch bản còn mục "phải kiểm nguyên văn" hoặc câu gắn nhãn [SỬ*] (chưa đọc nguyên văn). Trước khi gửi, Claude tự tra từng chi tiết có tên, năm, con số, lời trích và câu nói của nhân vật bằng nguồn gốc (WebSearch/WebFetch, nguyên văn chữ Hán trên Wikisource/ctext/zh.wikisource, sách dẫn lại), rồi ghi kết quả vào mục "Trạng thái kiểm chứng".
- Chỉ dùng nhãn [SỬ] khi đã đọc nguyên văn nguồn gốc và nêu được tên sách, quyển, hoặc đường dẫn. Không tìm được nguyên văn thì hạ nhãn xuống [CG]/[GT], hoặc bỏ chi tiết khỏi lời kể và ghi vào "Chi tiết đã bỏ"; không để nhãn [SỬ*] hay danh sách "phải kiểm" tồn tại trong bản gửi.
- Bản gửi chủ kênh phải nêu rõ: bao nhiêu câu đã kiểm nguyên văn, bao nhiêu đã hạ nhãn hoặc bỏ, và câu nào còn tranh cãi. Không đẩy việc kiểm cho chủ kênh hay để sang bước đọc giọng.
- Không gán nhãn "đã kiểm" cho điều chỉ nhớ từ trí nhớ hoặc từ một bài tổng hợp. Đối chiếu ít nhất hai nguồn độc lập cho số liệu và lời trích quan trọng.

## Màu sáng và trang phục đẹp (chủ kênh yêu cầu 03/11/2026, áp dụng mọi ảnh từ nay)
- Ảnh phải **sáng, màu tươi, sạch**: ánh sáng ban ngày trong, màu bão hòa vừa phải. KHÔNG xám xịt, tối, đục (không dùng "muted", "grey-blue calm", "dim"). Cảnh đêm vẫn rực: lửa cam sáng trên nền xanh đêm trong.
- **Trang phục đẹp, giàu chi tiết:** áo lụa có viền thêu hoa văn, chỉ vàng, đai ngọc, mũ có trâm ngọc, giáp da bóng có đinh đồng. Mỗi nhân vật một màu áo riêng, rõ ràng (Chu Du xanh lục thẫm, Tôn Sách đỏ thắm, Tôn Quyền tím, Gia Cát Lượng trắng viền xanh trời, Tào Tháo đen viền đỏ). Dân thường mặc áo nhiều màu (xanh, vàng đất, xanh lá, nâu đỏ), không toàn xám.
- Không để nhân vật quyền quý trông như nông dân: vua chúa, tướng lĩnh, quan văn mặc lụa; cung điện có cột son, trần vẽ, rèm lụa; ngai thật bằng vàng, đặt trong điện.
- Vẫn giữ mọi quy tắc cấm: không chữ, không viền, không kính, không ghế tựa, không vật hiện đại.
- Mã nguồn mẫu: `ke-hoach/nhan-vat/tao_CD.py` (biến `HAN`, `SONG`, `W`, `C`, `F`, `NV`); các bộ sau dùng theo.

## E. Ảnh minh họa và ẩn dụ (chủ kênh yêu cầu 03/11/2026, áp dụng mọi video từ nay)
Quy tắc ở mục A đến D thiên về cảnh người làm việc, nên các đoạn kể ý trừu tượng (cân nhắc nguồn, hai mặt của một chuyện, lời đồn lan đi, nỗi đau, sự thật bị che) bị vẽ thành người đứng nói hoặc cảnh vắng chẳng có nghĩa. Từ nay mỗi kế hoạch ảnh phải phân loại từng câu và dành chỗ cho ẩn dụ.
1. **Ba loại ảnh, ghi vào kế hoạch ảnh từng câu:** (a) cảnh người: sự việc có người làm; (b) cảnh vật có nghĩa: nơi chốn, cảnh vật mang không khí; (c) minh họa ẩn dụ: vật hoặc cảnh tượng trưng cho một ý của lời kể.
2. **Khi nào dùng ẩn dụ:** câu nói về ý trừu tượng, lời nhận định, độ chắc của nguồn, kết quả không thể vẽ thành người (bệnh nặng, chết, danh tiếng, lời đồn), và các bước chuyển chương. Mục tiêu khoảng 15 đến 25 phần trăm số ảnh của một video kiểu "tiểu thuyết và chính sử", ít hơn ở video chiến trận.
3. **Mỗi ảnh ẩn dụ chỉ một ý, đọc ra ngay:** một vật chính ở giữa hoặc một cặp đối lập rõ (cán cân hai đĩa, hai con đường rẽ, một cây cầu gãy giữa dòng, bóng người lớn hơn người, bàn cờ với hai quân, ngọn đèn dầu trước gió, dòng sông chia đôi lửa và nước). Vật phải thuộc thời đó (đĩa dầu đồng, thẻ tre trơn, cầu gỗ, thuyền chiến Hán) và theo bảng ở mục A.
4. **Không ẩn dụ lẫn lộn với sự thật:** ảnh ẩn dụ không được trông như một sự kiện có thật. Không ghép vật không liên quan vào cùng khung (lỗi của ảnh 064 cũ: mũi tên, hạm đội cháy và chiếc giường đặt ngoài bờ không nói lên ý nào). Mỗi vật trong khung phải trả lời được "nó tượng trưng cho điều gì trong câu".
5. **Ghi nghĩa ẩn dụ trong kế hoạch ảnh:** cột "Ý của ảnh" một dòng (ví dụ "cán cân nghiêng về phía tiểu thuyết vì có nhiều người kể hơn người đọc sử"). Chủ kênh duyệt cột này trước khi vẽ.
6. **Vẽ 2 bản** cho ảnh ẩn dụ và soi xem người ngoài nhìn có hiểu không. Nếu phải giải thích mới hiểu thì đổi ẩn dụ.
7. **Vẫn giữ mọi quy tắc cấm:** không chữ, không viền, đồ đúng thời, màu sáng; ẩn dụ không dùng cờ có hình, bia, biển, thẻ có chữ.
8. **Ẩn dụ không thay thế cảnh người ở đoạn kể sự việc:** đoạn nào kể ai làm gì thì vẫn vẽ người đó, đúng quy tắc tóc búi, tay, số người.

### E2. Minh họa sáng tạo, không tả thực từng câu (chủ kênh yêu cầu 03/11/2026, 23:36)
- Câu giải thích, đặt câu hỏi, so sánh nguồn hay nêu ý trừu tượng **không vẽ tả thực lời kể**. Dùng hình minh họa sáng tạo nhưng vẫn đúng cốt truyện. Ví dụ cho sẵn: câu hỏi thì vẽ một người đang suy tư với một **dấu hỏi chấm vàng lớn phát sáng** lơ lửng trên đầu (dấu hỏi là biểu tượng, được phép, không tính là chữ).
- **Kho thủ pháp:** dấu hỏi chấm; cờ vây hai người (đi trước một bước); sa bàn có quân đất sét (số quân, kế hoạch); tòa nhà ba tầng (ba tầng tư liệu); móng đá của tòa nhà (chính văn); sân khấu rối và bóng rối (người kể chuyện); lấy mũ vàng từ rối này đặt sang rối kia (chuyển công trạng); dải sóng vàng từ đàn biến thành cờ trận (người nhạy nhạc biết đọc thế trận); cán cân; ba chiếc cồng đánh ba hồi (con số ba); bốn khung tranh tròn bay quanh nhân vật (tóm lại bốn việc); lụa trắng trống trơn (chưa từng có chuyện ấy); ngã ba đường (hai cách nhớ); tường treo tranh chân dung (người bạn nghĩ là ai).
- Không vẽ cảnh một người đứng một mình trừ khi người ấy đang làm điều có nghĩa (suy tư dưới dấu hỏi). Ưu tiên 2 đến 5 người có việc rõ ràng, hoặc vật minh họa có nghĩa.
- Cảnh kể sự việc (hành quân, đánh trận, gặp gỡ, khóc tang) vẫn vẽ đúng sự việc. Mỗi ảnh vẫn tuân thủ quy tắc tóc búi, hai tay, không chữ, màu sáng.
