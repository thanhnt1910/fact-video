# Hướng dẫn cho Claude khi làm việc trong repo này

Repo của kênh "Người Gác Sử": video dọc 60–80 giây và video dài YouTube 16:9, kể chuyện có thật trong lịch sử.

## Quy định thời lượng (chủ kênh đặt ngày 15/10/2026, áp dụng cho mọi video từ nay)

- Mọi VIDEO DÀI phải dài TỐI THIỂU 10 PHÚT. Đây là mức sàn.
- Lời đọc ít nhất khoảng 1.900 tiếng (giọng Gemini đọc khoảng 3 tiếng/giây), khoảng 70–90 beat, 8–10 chương.
- Thiếu chữ thì thêm chi tiết có nguồn, không độn câu, không lặp ý, không bịa. Chi tiết không chắc thì nói rõ là còn tranh cãi.
- Sau khi dựng, đo thời lượng thật; dưới 10 phút thì bổ sung kịch bản, không đăng.
- Video dọc vẫn 60–80 giây. Quy định này chỉ áp cho video dài.
- Chi tiết đầy đủ: mục "VIDEO DÀI" trong `PROMPT_KICH_BAN.md`.
- `review.py` đã áp mức sàn này: video dài dưới 10 phút báo ⚠️ (vẫn được gửi), dưới 6 phút báo ❌ (không được gửi Telegram).

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

## Series Tam Quốc (chính sử)

- Mỗi tập viết kịch bản ở `ke-hoach/tam-quoc-tap-N-kich-ban.md` (có nhãn độ chắc từng câu và mục "Trạng thái kiểm chứng"), chủ kênh duyệt, rồi mới chuyển sang `scripts/TQN.json`.

## Phân nhóm cảnh khi làm ảnh và clip (chủ kênh chốt ngày 15/10/2026, áp dụng mọi tập, tự kiểm không chờ nhắc)

Khi soạn file `ke-hoach/tam-quoc-tap-N-anh-va-veo.md` (hoặc tương đương), phân mỗi ảnh vào đúng một nhóm:

- **Nhóm A — Veo (Google Flow, ảnh → video), TỐI THIỂU 20 CLIP MỖI TẬP VIDEO DÀI:** chỉ các **cảnh chính có người di chuyển nhiều** (hành quân, hàng quân, dàn trận, đám đông, người bước đi). Mỗi clip kèm tiền tố và prompt chuyển động; làm thử 3 clip trước. Nếu chưa đủ 20 cảnh có người di chuyển, chọn thêm cảnh người bước đi hoặc đội hình, không độn cảnh vắng người.
- **Nhóm B — tool dựng có sẵn (`anim_nhe.py`, không dùng AI):** cảnh vật, đồ vật, cảnh vắng người; chỉ cây cỏ, cờ, nước, lửa, khói, đèn, sương chuyển động nhẹ. Ghi phần chuyển động của từng ảnh; cần `ke-hoach/nhan-vat/<MÃ>_nhe.json` (khung chọn tay khi đã có ảnh).
- **Còn lại — ảnh tĩnh:** người đứng yên hoặc có tương tác tay; không làm clip.
- Không đưa cảnh vắng người vào Veo; không đưa cảnh người di chuyển nhiều vào `anim_nhe.py`.
- Không máu, không cảnh chém/giết (xem `review_checklist.md`). Ngựa được vẽ bình thường khi lời kể có (chủ kênh bỏ quy tắc cấm ngựa ngày 16/10/2026); chỉ soi ngựa có méo chân, thừa chân, yên cương sai thời.
- Đầu file phải nêu số lượng: tổng ảnh, số clip Veo (≥ 20), số cảnh hoạt hình nhẹ, số ảnh tĩnh.
- Tập 2 đã dựng theo cách cũ (có nhóm B Veo cảnh người nhẹ); không sửa. Mẫu mới: `ke-hoach/tam-quoc-tap-3-anh-va-veo.md`.

## Vẽ ảnh: tự kiểm và tự vẽ lại (chủ kênh yêu cầu ngày 15/10/2026, áp dụng mọi tập)

Ảnh AI hay lỗi (thừa tay, thừa người, giống trẻ con, lệch nhân vật, chữ lạ, ngựa méo/thừa chân, sai thời). Không giao ảnh chưa kiểm cho chủ kênh.

- Lệnh chuẩn: `python ve_kiem_anh.py <MÃ>` (hoặc workflow GitHub "Vẽ ảnh 2D hàng loạt", đã chạy lệnh này khi để trống ô "lam_lai"). Quy trình: vẽ ảnh còn thiếu → kiểm → cất ảnh lỗi vào `assets/anh_2d/<MÃ>/_loi/` → vẽ lại với hạt giống mới → kiểm lại; tối đa 3 vòng (`vong=N`).
- Ba lớp kiểm: (1) kỹ thuật (nhỏ, mờ, một màu, vỡ khối); (2) trùng ảnh (mỗi ảnh một lần); (3) Gemini xem từng ảnh qua `kiem_tra_2d.py` (số người, trẻ con, giải phẫu, lệch nhân vật, chữ lạ, sai thời, lạc đề so với lời kể; riêng Tam Quốc thêm: cờ/vật có chữ hoặc biểu tượng, có máu hay cảnh giết).
- Quy ước riêng loạt nằm ở `SERIES` trong `kiem_tra_2d.py` (khóa là tiền tố mã). Loạt mới thì thêm mục ở đó. Mỗi mã cần `ke-hoach/nhan-vat/<MÃ>_anh.json` (có `nv`, `text` là lời kể của ảnh) và `ke-hoach/nhan-vat/<MÃ>.json` (mô tả nhân vật).
- Chỉ kiểm ảnh đã có: `python ve_kiem_anh.py <MÃ> chi_kiem=1`. Báo cáo: `logs/kiem_2d/<MÃ>_tong_hop.txt`.
- Không có khóa Gemini thì lớp 3 không chạy và báo "chưa kiểm bằng AI" (không tính là đạt, thoát mã 2). Khi giao ảnh, nói rõ ảnh nào còn lỗi sau vòng cuối và ảnh nào chưa qua AI.
- Mọi tập mới: sau khi vẽ ảnh phải đọc báo cáo tổng hợp trước khi chuyển sang làm clip Veo hoặc dựng.

## Prompt Veo: không nêu tên riêng người nổi tiếng (chủ kênh ghi nhận ngày 15/10/2026)

- Prompt gửi Veo / Google Flow **không được chứa tên riêng của người thật nổi tiếng** (nhân vật lịch sử như Lưu Bị, Tôn Kiên, Liu Bei, Sun Jian…): vi phạm chính sách của Veo, clip bị từ chối (ví dụ ảnh 027 tập 2). Ảnh khung đầu đã mang sẵn khuôn mặt, prompt chỉ mô tả chung: "the foreground man", "the officer", "the two men", "the leader".
- Áp dụng cho tiền tố và cả cột prompt chuyển động. Cột "Cảnh" tham khảo viết tiếng Việt, ghi rõ "KHÔNG dán vào Veo".
- Tên riêng chỉ được dùng ở prompt VẼ ẢNH (Flux/Kaggle), không dùng ở prompt Veo.
- Trước khi giao file prompt Veo luôn chạy: `python kiem_prompt_veo.py <file.md>`; phải báo ĐẠT (mã 0). Loạt mới thì thêm tên vào danh sách `TEN` trong `kiem_prompt_veo.py`.

## Lỗi ảnh hay gặp: tự soi bằng mắt ở kích thước lớn (chủ kênh nhắc ngày 16/10/2026)

- Bản thu nhỏ KHÔNG đủ để kiểm. Sau mỗi đợt vẽ phải xem ảnh ở cỡ lớn (tối đa 6 ảnh một tấm) và soi: thừa/thiếu tay ngón, hai người giống hệt nhau, vật hiện đại (đèn điện, bóng đèn, chao đèn, đèn lồng kính, cửa sổ kính, ổ cắm/công tắc, khung tranh, sách đóng gáy, cốc có quai), vật sai cấu tạo (vòi ấm ngược), vật lơ lửng (quạ không có chỗ đậu), ngựa méo hoặc thừa chân, viền khung quanh ảnh.
- Prompt vẽ ảnh KHÔNG dùng chữ "lamp/lantern/book/cup" trơn: AI sẽ vẽ đồ hiện đại. Dùng "Han bronze oil dish (shallow open bowl, tiny flame, no glass, no lampshade)", "bamboo slips", "two-eared bronze wine cup", hoặc bỏ hẳn đèn; đã thêm câu cấm vật hiện đại vào cuối mọi prompt TQ3.
- Tay cầm vật (kiếm, gậy, thẻ lệnh) hay sinh thừa tay: để "hai tay giấu trong tay áo", vật cắm trên giá hoặc treo ở thắt lưng.
- Cảnh đứng hai người phải ghi rõ hai khuôn mặt khác nhau; cảnh hai đạo quân thì vẽ lính nhỏ ở xa, không đặt hai người lớn đối xứng ở tiền cảnh.
- `kiem_tra_2d.py` đã thêm các trường: đèn/vật hiện đại, hai người giống hệt, vật sai cấu tạo, viền khung. Gemini không thay thế mắt người; ảnh chưa qua AI vẫn phải tự soi.


---

# Quy ước vẽ ảnh và kịch bản: series Tam Quốc theo chính sử

File này do chủ kênh yêu cầu (17/10) để ghi các quy tắc vẽ ảnh và viết kịch bản, các phiên Claude sau phải đọc và theo.

## Quy tắc vẽ ảnh (áp dụng từ tập 4 trở đi)

1. **Tranh phải phục vụ cốt truyện.** Mỗi ảnh vẽ đúng điều lời kể đang nói: binh lính, đám đông, kỵ binh, doanh trại, thành quách, hội đồng, đoàn người đi đường... Không được thay cảnh có người bằng vật thể trống hoặc chân dung đơn giản.
2. **KHÔNG giới hạn số người trong khung** và **KHÔNG ép khung nửa người**. Chọn cỡ cảnh (toàn cảnh, trung cảnh, cận cảnh, góc thấp, từ trên cao) theo điều cần kể. Trước đây có quy tắc "nửa người, tối đa hai người, giấu tay còn lại": đã bỏ hẳn, không dùng lại.
3. **Ảnh nào cũng phải có nền chi tiết** hợp cảnh (kiến trúc, cảnh quan, lều trại, cờ, đồi núi), không để nền trơn một màu, kể cả chân dung.
4. **Đúng thời Hán** (Đông Hán, thế kỷ 2): đường đất, đèn dầu đất nung, thẻ tre cuộn buộc dây, chiếu và giường thấp, cửa sổ chấn song gỗ không kính, giày vải hoặc dép rơm, kiến trúc gạch bùn mái ngói xám. Cấm vật hiện đại: đường nhựa, cột điện, nến, sách đóng gáy, giấy, ghế tựa, giường khung gỗ, kính, tay nắm cửa, mũ lưỡi trai, đèn đường, bảng hiệu; cũng tránh kiến trúc Hàn, Nhật, châu Âu. Đoạn cấm này (biến `ANTI`) phải nằm trong mọi prompt (xem `ke-hoach/nhan-vat/tao_TQ4.py`).
5. **Không có chữ** trên ảnh, cờ và biển để trơn một màu, không biểu tượng.
6. **Không vẽ cảnh máu me hoặc người bị giết.** Cảnh chiến tranh vẽ bằng hai bên đối mặt, hàng quân tiến, khói lửa, thành bị vây, dân chạy nạn; kết quả bi thảm chỉ gợi bằng đường vắng, xe đổ, khói. Lính ở xa hoặc nhìn từ sau thì mặt đơn giản.
7. **Trang phục đổi theo mốc cốt truyện, mẫu nhân vật giữ nguyên.** Mã trang phục từng tập nằm trong `ke-hoach/nhan-vat/TQn_trang_phuc.json` (tập 4: `TQ4_trang_phuc.json`). Trang phục của mọi nhân vật, kể cả Lưu Bị, được đổi theo tập đang kể, miễn nhận ra nhân vật.
8. **Tuổi nhân vật đúng theo sổ sách**, tính từ năm sinh trong sử theo năm đang kể (Lưu Bị sinh 161, Tào Tháo 155...). Người sử không ghi năm sinh thì ghi khoảng tuổi chung. Năm sinh nhớ từ trí nhớ thì ghi "cần kiểm".
9. **Vũ khí theo Tam Quốc diễn nghĩa** (xem bảng vũ khí ở kịch bản tập 3): Lưu Bị song kiếm, Quan Vũ thanh long yển nguyệt đao, Trương Phi xà mâu, Lữ Bố phương thiên họa kích. Không có quy tắc "không ngựa": vẽ ngựa bình thường.
    **Cập nhật 17/10 (chủ kênh duyệt, áp dụng mọi tập):** Quan Vũ cầm đao lưỡi cong rộng, cổ đồng chạm rồng, cán nâu hai đai vàng; Trương Phi cầm xà mâu cán nâu thẳng, mũi bạc hình lá dài thẳng có hoa văn rắn (ảnh tham chiếu `ke-hoach/nhan-vat/refs/guandao.jpg`, `xamau.jpg`, vẽ đơn giản, không vẽ giá đỡ). **Mỗi người chỉ MỘT kiếm** (kể cả Lưu Bị, không song kiếm), không bao giờ hai kiếm, không kiếm chéo nhau.
10. Mỗi ảnh chỉ dùng một lần trong video dài (khóa ảnh = số câu lời kể).
11. **Kiếm đeo ở hông hoặc sau lưng luôn nằm trọn trong bao kiếm** (chỉ thấy chuôi và bao). Chỉ vẽ lưỡi kiếm trần khi người đó đang cầm kiếm trong tay. Mỗi người tối đa một kiếm.
12. **Trong một tranh không có hai người giống hệt nhau**: mỗi người một khuôn mặt, tuổi, tóc râu và màu áo riêng; không nhân bản, không cặp sinh đôi, kể cả quân lính và đám đông.
13. **Cảnh nhiều nhân vật chính (Lưu Bị, Quan Vũ, Trương Phi chung khung):** vẽ nhiều bản (hạt giống khác nhau, khóa biến thể = số bản x 1000 + số cảnh, file `TQnV_anh.json`) rồi chọn bản đúng nhất.
14. **Gửi ảnh cho chủ kênh từng ảnh một**, đặt tên theo số câu, sau khi cả đợt vẽ xong; không gửi ảnh ghép nhiều ảnh.

## Quy tắc viết kịch bản

- Lời kể là một câu chuyện liền mạch, kể như kể chuyện, không trình bày nguồn. Không nhắc tên sách, chú giải; độ chắc từng câu nằm ở nhãn trong ngoặc vuông, không nằm trong lời kể.
- Video dài tối thiểu 10 phút (khoảng 3 chữ mỗi giây). Quy cách đầy đủ: `PROMPT_KICH_BAN.md`, `review_checklist.md`.
- Tài liệu kịch bản, lộ trình và quy ước trang phục lưu trong Project "Tam Quốc" (`claude/tam-quoc-*.md`).

## Quy trình vẽ ảnh một tập

1. Tạo `tao_TQn.py` theo khuôn `tao_TQ4.py` (cảnh, nhân vật, mã trang phục) rồi chạy ra `TQn.json` và `TQn_anh.json`.
2. Chạy workflow `ve-anh-2d.yml` (tham số `ma=TQn`; `lam_lai` là danh sách số ảnh cần vẽ lại, `dot` đổi hạt giống). Ảnh ra ở `assets/anh_2d/TQn/`.
3. Soi từng ảnh ở độ phân giải lớn (không soi ảnh thu nhỏ) và vẽ lại ảnh lỗi trước khi gửi chủ kênh.

## Cập nhật 18/10/2026: tập gộp 4+5 (mã TQ45, 177 cảnh), các quy tắc bổ sung

15. **Vũ khí theo ảnh mẫu.** Cảnh có Quan Vũ hoặc Trương Phi thêm ảnh mẫu vũ khí làm ảnh tham chiếu (`refs/guandao.jpg`, `refs/xamau.jpg`); cảnh ba huynh đệ thêm cả `refs/trio.jpg` và câu "chỉ có đúng hai vũ khí: Quan Vũ đao lưỡi cong, Trương Phi mâu mũi lá, Lưu Bị tay không". Cảnh đứng thì vũ khí dựng thẳng, chuôi đặt trên đất; cảnh ngủ hoặc ngồi trong lều thì không có vũ khí. Cán đao và mâu dài hơn người cầm, phải thấy trọn lưỡi.
16. **Mô hình hay đổi chéo vũ khí giữa Quan Vũ và Trương Phi**: cảnh ba huynh đệ luôn vẽ 2–3 bản (đổi `dot`), soi rồi chọn bản đúng nhất.
17. **Cảnh chỉ một người**: viết "exactly ONE man only ... no second figure, no crowd". Chữ "alone" quá yếu, mô hình vẫn vẽ thêm người.
18. **Prompt vẽ ảnh**: không cắt cụt mô tả trang phục (từng cắt mất ", wearing" nên Trương Phi cởi trần). Dùng hậu tố Hán ngắn, nói điều cần có thay vì danh sách cấm dài; thứ tự: cảnh, nhân vật, hướng dẫn ảnh tham chiếu, hậu tố; cố giữ dưới khoảng 2.000 ký tự. Lưu Bị và Tào Tháo thêm ", empty hands, no weapon" (nếu không mô hình vẽ kiếm trần). Cảnh vật trống thêm "completely empty, absolutely no people". Thêm "single full-frame picture, no panels, no border" để khỏi ra ảnh hai khung. Chỉ dùng tối đa 2 ảnh chân dung tham chiếu (cảnh ba huynh đệ dùng trio + 2 ảnh vũ khí).
19. **Quy trình Kaggle**: workflow `ve-anh-2d.yml` có tham số `hau_to` (ảnh ra `assets/anh_2d/<mã><hậu tố>`), chỉ một kernel, KHÔNG chạy song song, khoảng 40 phút cho 53 ảnh. Workflow đọc prompt đã commit trên nhánh nên phải push trước khi chạy. Cloudflare Workers AI hết hạn mức sớm và ảnh kém: không dùng. Gemini kiểm ảnh chậm và hay bị giới hạn: soi bằng mắt ở cỡ lớn là chính.
20. **Mẫu Lữ Bố** là người trẻ bên phải ảnh chủ kênh gửi (`refs/lubo_cd.jpg`; bản cũ `lubo_cd_cu.jpg`).
21. **Ảnh chủ kênh tự sửa và gửi lại** thường không ghi số: so khung hình với bộ ảnh (tương quan độ xám thu nhỏ) để khớp số cảnh, đưa về 1344×768, thay vào `TQ45_V2` (giữ tên cũ), commit. Ảnh chủ kênh sửa có thể có biểu tượng ngôi sao nhỏ ở góc: hỏi có cần che không.
22. **Gộp tập**: tập 4+5 thành một video dài (mã `TQ45`), kịch bản `ke-hoach/tam-quoc-tap-4-5-gop-van-xuoi.md`, ảnh chính thức `assets/anh_2d/TQ45_V2/NNN.jpg` (177 ảnh, một ảnh mỗi câu). Việc đánh lại số tập sau khi gộp chưa chốt, không sửa tài liệu tập 5, 6 của chủ kênh.

### Veo cho tập gộp (chủ kênh duyệt 18/10/2026, điều chỉnh nhóm phân loại ở trên)
- Chủ kênh chọn cảnh Veo theo tầm quan trọng của cốt truyện, kể cả cảnh có tương tác tay (trao ấn, rót rượu, giương cung); chỉ cần một hành động nhỏ, chậm. Kế hoạch: `ke-hoach/tam-quoc-tap-4-5-veo.md`, dữ liệu: `ke-hoach/veo/TQ45_clips.json` (40 clip, mỗi ảnh một clip, giá trị `rui_ro`: tay, ngựa, đám đông, an toàn).
- Prompt Veo chỉ mô tả theo hình dáng ("người cao gầy áo chàm", "người thấp mặc giáp đen", "người già râu trắng"), không có tên người nào, kể cả tên phụ như Thái Sử Từ, Mi Trúc, Trần Đăng. Luôn chạy `python kiem_prompt_veo.py ke-hoach/tam-quoc-tap-4-5-veo.md` và quét cả `TQ45_clips.json`.
- Chủ kênh tự tạo clip trong Google Flow rồi gửi; Veo có thể hết hạn mức giữa chừng. Clip dài 8–10 giây (không phải 6). Lưu vào `assets/clips_2d/<mã>/E4_NNN.mp4` kèm `danh_sach.json`; số cảnh xác định bằng cách so khung hình đầu clip với ảnh nguồn (tương quan từ 0,9 trở lên).
- Veo hay tự vẽ lại khung đầu: khung đầu không khớp ảnh gốc thì bỏ clip, cảnh đó dùng ảnh tĩnh (đã xảy ra với cảnh 067; clip để ở `_bo_qua/`). Tiêu đề file video chủ kênh đặt có thể sai nội dung, chỉ tin khung hình.
- **Chờ chủ kênh báo đủ clip rồi mới dựng video dài**; cảnh nào thiếu clip thì dùng ảnh tĩnh với hiệu ứng máy quay.

### Git
- Mọi commit dùng `user.email noreply@anthropic.com`, `user.name Claude`. Commit tự động của workflow (`actions@users.noreply.github.com`) bị GitHub gắn "Unverified": đợi hết run đang chạy rồi `git rebase --exec "git commit --amend --no-edit --reset-author -q" <SHA>^` và `git push --force-with-lease=<nhánh>:<SHA từ git ls-remote>`.
- Cảnh báo "commit chưa đẩy" của stop hook thường do tracking ref cũ: chạy `git update-ref refs/remotes/origin/<nhánh> $(git ls-remote origin <nhánh> | cut -f1)` rồi đếm lại.
- **Workflow chỉ chạy khi chủ kênh yêu cầu, và chỉ chạy đúng video được yêu cầu** (chủ kênh nhắc 21/10/2026). Không tự kích hoạt dựng, nhận dạng giọng hay vẽ ảnh. Workflow dựng/nhận dạng chạy khi có push thay đổi file kích hoạt, và push viết lại lịch sử (rebase đặt lại tác giả) làm GitHub coi mọi file là đã đổi nên chạy cả tập 1, 2, Nguyên Mông: khi buộc phải viết lại lịch sử thì commit cuối phải có `[skip ci]` trong tiêu đề.
- Không đẩy lên `main` trừ khi chủ kênh yêu cầu; riêng CLAUDE.md này chủ kênh yêu cầu gộp vào `main` (18/10/2026) để các phiên khác dùng.

## Viết kịch bản Tam Quốc: kể liền mạch, 20–22 phút (chủ kênh yêu cầu 18/10/2026, áp dụng từ tập 5)

- Lời kể là một câu chuyện liền, theo nguyên nhân – kết quả. KHÔNG chen so sánh "tiểu thuyết / sử chép", "theo một lời kể", tên sách, chú giải. Độ chắc chỉ nằm ở ghi chú.
- Chi tiết nghi vấn (cần kiểm) bỏ khỏi lời kể, ghi vào mục "Chi tiết đã bỏ khỏi lời kể".
- Video dài 20–22 phút ≈ 3.600–3.960 chữ; thiếu thì gộp thêm hồi có nguồn, không độn.
- Cuối tập: sự kiện sắp tới + câu hỏi "vì sao" + "Tập sau sẽ kể tiếp." (không dùng câu so sánh nguồn.)
- Video ngắn cũng kể liền. Chi tiết: `claude/tam-quoc-quy-tac-viet-kich-ban.md` trong Project "Tam Quốc". Tập 5 là mẫu: `claude/tam-quoc-tap-6-7-gop-van-xuoi.md`.
- Năm trong lời kể viết đầy đủ bằng chữ: 196 = "năm một trăm chín mươi sáu" (không rút gọn "một chín sáu").
- Từ Hán Việt cổ (xa giá, đông thiên, tiết việt, thượng thư, đồn điền, đại xá, bêu...) không đưa vào lời kể; dùng chữ dễ hiểu hoặc giải thích ngay trong câu. Mỗi câu hiểu được khi nghe một lần.
- Tên nhân vật luôn ghi đủ họ tên trong lời kể (Tào Tháo, không "Tháo"; Tào Hồng, không "Hồng"); chi tiết ở quy tắc 11 trong `claude/tam-quoc-quy-tac-viet-kich-ban.md`.
- Viết như kể chuyện cho người nghe một lần (câu ngắn, từ đời thường, nêu nguyên nhân); không dùng địa danh dễ nhầm như "Hà Nội" (viết "vùng phía bắc sông Hoàng Hà"). Chi tiết: quy tắc 12–13.

## Video bản đồ: mọi chữ trên màn hình phải nằm gọn trong khung (chủ kênh yêu cầu 20/10/2026, áp dụng mọi tập)

- Không chữ nào được dài quá khung 1920×1080: thẻ hài, tiêu đề, thẻ nhân vật, thẻ câu nói, nhãn, phụ đề đều phải tự xuống dòng hoặc thu nhỏ chữ khi quá rộng (chừa lề tối thiểu 60 px mỗi bên). Hàm vẽ chữ mới phải có sẵn bước đo độ rộng (`textlength`) và xuống dòng; không vẽ một dòng dài cố định.
- Trước khi dựng bản đầy đủ: chạy kiểm độ rộng cho mọi lớp chữ của nội dung (hộp bao `getchannel('A').getbbox()` phải nằm trong 60–1860 px) và xem ít nhất một khung của câu dài nhất mỗi loại.
- Khi sửa phụ đề: dùng `phude_tinh.py` (mốc theo đoạn có tiếng), không đặt mốc cố định.

## Video bản đồ: bố cục gọn mắt, không che nhau (chủ kênh chốt 22/10/2026, từ demo Hán Sở Hồng Môn yến, áp dụng mọi tập)

- **Không dùng khung trích lời (`QUOTES`) ở dưới màn hình:** nó đè lên phụ đề, mà phụ đề đã hiện đúng câu ấy. Lời nhân vật chỉ nằm trong phụ đề.
- **Khung đùa (`JOKES`) chỉ khoảng hai khung mỗi chương, mỗi khung hiện tối đa 3 giây** (`J(n,icon,text,off,dur=3.0)`). Không đặt khung đùa lên câu vốn đã là câu đùa, và không lặp nguyên văn câu đang đọc.
- **Không đặt thẻ tiêu đề hay thẻ kết lên lúc đang đọc câu cuối:** thẻ chữ lớn che bản đồ. Thẻ mở đầu chỉ ở giây đầu; kết video bằng mờ dần, không thêm thẻ "HẾT".
- **Nhãn và quân không đè lên tên thành:** dùng `soff` (dịch cả quân lẫn nhãn theo điểm ảnh) để đặt cụm quân lệch khỏi biểu tượng thành và nhãn tên thành; quân đứng yên dùng `spread` nhỏ (0,45–0,6); nhóm hai bên đóng gần nhau không để chồng lên nhau. Quân chạy về nơi có quân đứng yên thì dùng cùng `soff` để nhập vào đúng chỗ.
- **Ít banner chữ, nhất là lúc đánh nhau (chủ kênh yêu cầu 22/10/2026):** banner chữ che cảnh đánh nhau làm rối mắt. Ghi chú nổi (`NT`) tối đa khoảng 4 cái mỗi chương, mỗi cái hiện tối đa 3,5 giây, chỉ giữ ý quan trọng (mốc, con số, bước ngoặt); bỏ ghi chú nhắc lại điều phụ đề đã nói. Thẻ số (`NU`) chỉ ở mốc lớn (mở đầu, đổi năm quan trọng). Khung đùa vẫn tối đa hai khung mỗi chương. **Cảnh đánh nhau, giao tranh, vây thành thì khai báo `Q(câu đầu, câu cuối)` trong file nội dung:** bộ dựng tự ẩn ghi chú nổi, khung đùa và thẻ số trong các khoảng đó (và trong mọi khoảng `BATT`); chỉ còn phụ đề và nhãn quân.
- **Mỗi lúc chỉ một lớp chữ lớn:** thẻ nhân vật, ghi chú, khung đùa và thẻ số không hiện cùng lúc ở cùng vùng (giữ các thời điểm không chồng nhau, `dur` ngắn, bị cắt ở `E(n,-0.1)`).
- **Luôn xem khung hình thật ở cỡ lớn** (`python3 mapfilm3.py still <giây>...`) ở đầu, giữa, lúc nhiều quân nhất và câu cuối trước khi đẩy lệnh dựng; bản thu nhỏ không đủ.
- **Giọng đọc cụm nhiều câu hay cắt lệch** (chữ cuối câu này lẫn sang đầu câu sau). Nếu `kiem_video.py` báo ❌ "thừa/mất chữ" ở nhiều câu liền nhau thì đọc lại từng câu: xóa các câu ấy khỏi `thoi_luong.json` và mp3, đặt `ke-hoach/thu-giong-hai/cum.txt` là `1`, đẩy `chay.txt`, rồi chạy lại nhận dạng giọng (`asr.txt`) và `phude_tinh.py`.
- **Mẫu:** `phim_ban_do/hs1_content.py` (demo Hồng Môn yến, kiểm 0 lỗi).

## Kiểm video trước khi giao (công cụ `phim_ban_do/kiem_video.py`, chủ kênh yêu cầu 21/10/2026)

- Sau khi chốt giọng và dựng, chạy: `python phim_ban_do/kiem_video.py <tên> --tts <các file tts> --video <mp4>` (cần `asr_<tên>_final.json` mới, chạy `phude-asr.yml` SAU khi file giọng đã chốt; công cụ báo "nhận dạng CŨ" nếu lệch với file giọng).
- Công cụ kiểm: chữ thừa/mất/lặp ở đầu và cuối mỗi câu, năm đọc sai, từ hay sai (kỵ), phụ đề trễ/sớm/trống, ô năm góc trái so với lời kể, cảnh gắn vào câu quá dài, giọng trong video lệch khỏi cảnh, im lặng dài, hình đen/đứng, độ dài. Báo cáo: `logs/kiem_video/<tên>.md`. Có ❌ thì không giao video.

### Không để giọng đọc lặp câu (chủ kênh yêu cầu 22/10/2026, từ demo Hồng Môn yến bị lặp câu 6009 và 6023)

- Lỗi hay gặp: giọng đọc cụm nhiều câu một lần rồi cắt, nên **đuôi câu trước bị đọc lại ở đầu câu sau** (6009 mở đầu bằng "Hạng Vũ nghe theo" của câu 6008) hoặc **đầu câu sau lẫn vào cuối câu này** (6023). Người nghe thấy một câu bị nhắc hai lần.
- `kiem_video.py` kiểm các dạng lặp sau, tất cả là ❌ (không giao video): thừa chữ ở đầu hoặc cuối câu (tính theo khối khớp đầu/cuối, không bỏ sót khi chữ thừa dính chữ lệch); đầu câu đọc lại 3–6 chữ cuối câu trước; cuối câu đọc lẫn 3–6 chữ đầu câu sau; một vế của câu bị đọc từ hai lần; giọng nhiều hơn kịch bản từ 4 chữ; lặp cụm 2–3 chữ liền nhau.
- **Báo cáo 0 lỗi chưa đủ:** sau khi dựng, mở `logs/kiem_video/<tên>.md` và nghe lại ít nhất chỗ nối giữa các câu đã sửa; câu nào ASR dài hơn kịch bản thì nghe lại.
- Cách sửa giống mục bố cục: xóa các câu lỗi khỏi `thoi_luong.json` và mp3, `cum.txt` = `1`, đẩy `chay.txt` (chỉ khi chủ kênh cho chạy), chạy lại nhận dạng và `phude_tinh.py`, rồi kiểm lại đến khi sạch. Chỉ sửa giọng thì phải dựng lại video.

## Quy trình giọng đọc: kiểm TRƯỚC khi dựng (chủ kênh yêu cầu 23/10/2026, từ bản Hai Bà Trưng bị 30 lỗi giọng và dựng lại hai lần)

Thứ tự bắt buộc, không đảo: **đọc từng đoạn → nhận dạng → `kiem_giong.py` → (đọc lại) → mới dựng.** Không dựng video (45 phút mỗi lần) khi chưa kiểm giọng.
- **Đọc cụm 8 đoạn ngắn rồi cắt, `cum.txt` = `8` (chủ kênh chốt 24/10/2026, thay quy tắc `cum=1` ngày 23/10).** Lý do: Gemini giới hạn số lượt gọi mỗi khóa (khoảng 4 lượt mỗi khóa rồi báo 429 và không hồi lại trong cả 15 phút), mà đọc từng đoạn cần 119 lượt cho 119 đoạn nên hết hạn mức sau 20 đoạn. Cụm 8 đoạn chỉ cần khoảng 15 lượt. Để cắt không lệch chữ thì mỗi đoạn phải ngắn (xem dưới), và vẫn phải nhận dạng + `kiem_giong.py` trước khi dựng; đoạn nào lỗi thì đọc lại riêng (đặt `cum=1` cho lượt đọc lại đó).
- **Trước khi đọc giọng luôn chạy `python phim_ban_do/kiem_kich_ban.py <tên>`** (0 ❌): đoạn tối đa 32 chữ (nên 20–30), tối đa 2 câu, không ngoặc/ngoặc kép/gạch/hai chấm/chữ số, không nói tắt, họ tên đủ, không mệnh đề chen giữa chủ ngữ và vị ngữ. Kịch bản viết cho giọng đọc ngay từ đầu, không sửa sau khi đã đọc.
- **Giữ hạn mức Gemini:** mỗi lần chạy giọng chỉ đọc đoạn còn thiếu, không xóa giọng đã đọc tốt. Tối thiểu 10 khóa trong `GEMINI_API_KEY` … `GEMINI_API_KEY_10`, từ các dự án Google khác nhau. Đầu log in bảng "tên secret → đuôi khóa" và chi tiết lỗi 429 (theo phút hay theo ngày). Khóa báo 401 (tài khoản dịch vụ bị xóa) thì mã tự bỏ qua; phải thay khóa đó. Nếu mọi khóa hết lượt thì dừng, báo chủ kênh, không đợi hơn 15 phút.
- **Đoạn lời ngắn:** mỗi đoạn khoảng 20–30 chữ, một hoặc hai câu. Đoạn dài 45–56 chữ hay bị Gemini bỏ câu đầu hoặc đọc lệch.
- **Nhận dạng chạy SAU khi giọng đã chốt** (workflow `phude-asr.yml`, không chạy song song với dựng). `phude_asr.py` đã nhớ mã nội dung file giọng: giọng đổi thì đoạn đó tự nhận dạng lại. Nếu thấy báo cáo "nhận dạng CŨ", xóa đoạn đó trong `asr_<tên>.json`.
- **Kiểm từng đoạn:** `python phim_ban_do/kiem_giong.py <tên> [--nguong 0.9] [--xoa]`. Đoạn nào khớp dưới 90% hoặc chưa có nhận dạng thì in ra; với `--xoa` thì xóa đoạn đó (giọng, hash, nhận dạng) để đẩy `chay.txt` đọc lại. Lặp đến khi sạch.
- **Đọc lại tối đa 3 lần mỗi đoạn.** Nếu vẫn bị bỏ câu hoặc đọc sai (đã gặp: "Vậy là nước Nam Việt, tồn tại gần một trăm năm, đã mất." bị đọc thành "ổn ạ"), đổi chữ nhẹ ở câu đó trong cả `<tên>_full.json` và file kịch bản `.md`, rồi đọc lại.
- Sau khi `kiem_giong.py` sạch mới tính phụ đề (`phude_tinh.py`), xem khung hình mẫu ở cỡ lớn, dựng, rồi chạy `kiem_video.py`. Có ❌ thì không giao.
- Dựng nên chia 16 đoạn song song nếu cần nhanh; chỉ đổi vài đoạn giọng thì cân nhắc chỉ dựng lại đoạn bị ảnh hưởng.
- Chi tiết dân gian (ví dụ voi chiến của Hai Bà Trưng) không có trong sử cũ chỉ được vẽ kèm ghi chú trên màn hình "theo truyền thuyết dân gian"; không đưa vào lời kể như sự kiện chắc chắn.

## Series lịch sử Việt Nam (Tây Sơn, Nguyên Mông...): quy tắc nội dung và giọng hài (chủ kênh chốt 23/10/2026, áp dụng mọi video sử Việt)

- **Hán Sở tranh hùng tập 1 đã DỪNG (23/10/2026)**, chuyển sang chủ đề Tây Sơn. Kịch bản, nội dung bản đồ và giọng đã đọc (7001–7058) giữ nguyên trong repo, không làm tiếp trừ khi chủ kênh yêu cầu.
- **Giọng hài chỉ nhắm vào tình huống và quân xâm lược** (tướng giặc chủ quan, lương thảo trục trặc, thua chạy...). **Không đùa cợt các anh hùng dân tộc** (Trần Hưng Đạo, Quang Trung – Nguyễn Huệ, Lê Lợi, Nguyễn Trãi, Ngô Quyền, Lý Thường Kiệt...): lời kể về họ nghiêm túc, trân trọng; khung đùa (`JOKES`), ghi chú, phụ đề không có câu giễu cợt, biệt danh hay so sánh bông đùa về họ. Khán giả Việt rất nhạy chuyện này, bình luận tiêu cực kéo cả video xuống. Khung đùa vẫn tối đa hai khung mỗi chương và chỉ rơi vào tình huống hoặc phía quân xâm lược.
- **Giới hạn thời gian: dừng trước năm 1858.** Không viết lịch sử cận đại và hiện đại (nhạy cảm chính trị, dễ bị báo cáo vi phạm). Không nói về pháp luật đương thời hay so sánh với thời nay.
- **Nguồn chính: Đại Việt sử ký toàn thư và Khâm định Việt sử thông giám cương mục** (lưu ý: Toàn thư chỉ chép đến 1675, không có thời Tây Sơn; thời Tây Sơn dựa Khâm định Việt sử, đối chiếu Đại Nam thực lục, Lê quý kỷ sự; Hoàng Lê nhất thống chí chỉ là nguồn phụ, xem `ke-hoach/tay-son-dan-y.md`). Ghi rõ nguồn trong phần mô tả video và bình luận, giống series "Tam Quốc theo chính sử". Chi tiết chỉ có ở tiểu thuyết, truyền thuyết hay sử liệu nước ngoài thì ghi rõ là lời kể hoặc còn tranh cãi, hoặc bỏ khỏi lời kể. Số quân, ngày tháng phải đối chiếu nguồn trước khi đọc giọng.
- Giữ quy tắc chung đã có: không bịa lời thoại, nội tâm; tên nhân vật ghi đủ; năm viết bằng chữ; từ cổ khó hiểu giải thích ngay; vẫn không phạm luật Việt Nam.

## Viết lịch sử rõ ràng, đầy đủ, không nói tắt (chủ kênh yêu cầu 23/10/2026, áp dụng mọi kịch bản)

- Lịch sử phải ghi rõ ràng, chi tiết. KHÔNG viết tắt kiểu rút gọn danh từ: nói đủ "thuyền chiến của quân Nguyên" (không "thuyền Nguyên"), "hạm đội của quân Nguyên", "lãnh thổ của nhà Nguyên", "thủy triều lên" / "thủy triều rút xuống" (không "triều lên", "nước rút"), "quân Đại Việt" hoặc tên người chỉ huy (không "người Việt" chung chung khi đang nói về người đánh trận).
- Khi nói về hiện tượng (thủy triều, mùa mưa, bão), nói luôn hệ quả ngay trong câu để người nghe một lần là hiểu.
- Khi nhắc một trận đánh, nêu tên người chỉ huy (đủ họ tên) ngay lần đầu, kể cả ở đoạn mở đầu ngắn.
- Trước khi giao kịch bản, tự rà các cụm danh từ ghép rút gọn ("thuyền X", "đất X", "quân X" khi X là tên nước hoặc triều đại) và viết lại cho rõ.

## Chạy workflow và Git: bài học từ Hai Bà Trưng và Ngô Quyền (chủ kênh yêu cầu 24/10/2026)
- Job lỗi vì treo bước "Cài đặt" (apt/pip): dùng `gh run rerun <id> --failed` (chỉ chạy lại job lỗi, sau khi run đã kết thúc), KHÔNG hủy cả run. Ghép video dùng workflow riêng không `apt-get update` (`ghep-hbt.yml`, đổi tên cho từng video).
- Dựng video dài chia 16 đoạn song song, có thử lại bước cài đặt. Không chạy nhận dạng, giọng hay dựng khi chủ kênh chưa yêu cầu.
- **Bước cài đặt dùng chung** `.github/actions/cai-dat` (chủ kênh yêu cầu 24/10/2026): ffmpeg chỉ cài khi thiếu, không `apt-get update`, gói pip có cache, mỗi lần tối đa 150–200 giây và thử lại 3 lần. Workflow mới dùng `- uses: ./.github/actions/cai-dat` với `pip: "gói1 gói2"` ngay sau checkout và setup-python, không viết lại bước cài tay.

## Giọng đọc đồng đều trong một video (chủ kênh yêu cầu 24/10/2026, áp dụng mọi video từ nay)
Mỗi lượt gọi Gemini tạo giọng độc lập, nên nhịp nói và âm lượng khác nhau giữa các lượt (đo ở Ngô Quyền: đoạn đọc riêng nhanh hơn khoảng 8% và to hơn khoảng 0,9 dB so với đoạn đọc trong cụm 8). Người nghe thấy chỗ nối giữa hai kiểu đọc như "đổi người".
- **Đọc cả video theo một cách:** cùng một `cum.txt`, cùng một mô hình, cùng một đợt nếu còn đủ hạn mức. Chỉ đọc lại riêng (`cum=1`) những đoạn lỗi. Không để phần đầu video đọc kiểu khác phần sau.
- **Chuẩn hóa ở bước âm thanh, không tốn hạn mức Gemini, không đọc lại:** làm trên bản sao của từng đoạn (giữ nguyên mp3 gốc), trước `audio2.py` và trước khi tính `phude_tinh.py`.
  1. Âm lượng: `ffmpeg -i <đoạn> -af loudnorm=I=-16:TP=-1.5:LRA=11` cho từng đoạn, cùng một mức cho cả video.
  2. Tốc độ: tính số chữ trên giây của từng đoạn (số chữ lời đọc chia thời lượng); lấy trung vị của các đoạn đọc trong cụm làm chuẩn. Đoạn nào lệch quá 5% thì chỉnh bằng `atempo` (chỉ trong khoảng 0,90 đến 1,10, giữ nguyên cao độ), không chỉnh cắt chữ.
  3. Sau khi chỉnh tốc độ phải cập nhật `thoi_luong.json` (thời lượng mới) rồi mới tính phụ đề và dựng; nhận dạng giọng chạy trên bản đã chuẩn hóa.
- **Kiểm trước khi dựng:** in bảng theo nhóm đoạn (đọc riêng, đọc cụm, đọc lại): từ/giây trung bình và âm lượng trung bình; chênh giữa các nhóm phải dưới 5% tốc độ và dưới 0,5 dB. Không tự ý đổi giọng hoặc mô hình giữa chừng.
- Video Ngô Quyền đã giao (12 phút 57 giây) chưa áp dụng bước này; chỉ áp dụng cho video sau.


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

## Video Góc IoT: luôn có hiệu ứng, Bóng chuyển động đa dạng (chủ kênh yêu cầu 28/10/2026, áp dụng mọi video Góc IoT)
- Mọi video phải có hiệu ứng: ví dụ minh họa phải chuyển động (sóng lan, gói dữ liệu chạy, mã hóa biến đổi, thanh tiến độ...), biểu tượng nhún nhẹ, kèm tiếng động tự tổng hợp (`sfx_video.py`). Không để ví dụ chỉ là biểu tượng đứng yên.
- Nhân vật Bóng không chỉ đi ngang: phải có nhiều kiểu chuyển động (lên xuống, nhảy, xoay khi đổi cảnh, nghiêng, co giãn khi tiếp đất, bay lơ lửng) và đổi kiểu theo cảnh.
- Mỗi video có hoạt họa riêng theo ý từng cảnh, đăng ký trong `ANIMS` của `goc-iot/dung_hinh.cjs` (`G({ anim: 'tên', items: [...] })`).
- **Mỗi lần dựng xong MỘT video là gửi ngay vào Telegram kèm tiêu đề + hashtag (chủ kênh yêu cầu 28/10/2026), không đợi gom đủ lô, không đợi nhắc.** Thêm mục trong `goc-iot/mo-ta.json` (tiêu đề, mô tả có nguồn, hashtag) trước khi gửi. Cách gửi: đặt `goc-iot/video/video-<số>-<tên>.mp4`, đổi nội dung `goc-iot/gui-telegram.txt`, đẩy lên nhánh; chỉ để trong thư mục đó các video cần gửi.

### Định dạng video Góc IoT (chủ kênh chốt 28/10/2026, áp dụng mọi video Góc IoT sau)
- **Chủ đề tập trung dạng "Điều gì xảy ra nếu...", "Bạn có biết...".** Mở bằng câu hỏi, trả lời bằng cơ chế, neo vào sự việc có thật có nguồn, kết bằng việc làm được ngay.
- **Kịch bản "sai rồi đúng": mỗi video chỉ MỘT chỗ** nêu câu trả lời sai (điều nhiều người dễ nghĩ) rồi lời kể sửa lại cho đúng. Không quá một chỗ, vì nhiều chỗ làm video rối. Chọn ý quan trọng nhất; câu sửa phải dựa nguồn đã kiểm chứng. Trên màn hình: bong bóng câu sai, khi lời kể sửa thì gạch đỏ kèm nhãn SAI (`myth` trong `goc-iot/minh_hoa.cjs`). Mẫu: video 11, câu "Ảnh chỉ nằm trong máy?" (cảnh 2 và 3).
- **Cảnh minh họa chuyển động thật, không chỉ hàng icon** (chủ kênh 28/10/2026): mỗi ý một cảnh vẽ riêng trong `goc-iot/minh_hoa.cjs` (phòng nhìn từ trên xuống, ảnh bay, khung nhãn vẽ lên, bộ đếm, chuỗi chạy giữa các nút, công tắc gạt...). Hàng icon `G({items})` chỉ dùng cho cảnh phụ.
- **Bố cục:** nội dung chính nằm giữa khung hình; Bóng nhỏ ở góc dưới, đổi bên theo từng cảnh, chỉ tay về phía mục đang nói. Cảnh mở đầu và kết giữ Bóng lớn ở giữa.
- **Giọng đọc:** `tao_giong.py` chỉ bỏ qua cảnh có chữ trùng bản hiện tại; sửa lời cảnh nào thì cảnh đó tự đọc lại, nên chỉnh kịch bản xong mới đẩy `chay-giong.txt`.
- **Mỗi video phải có thêm ảnh bìa, gửi vào Telegram cùng video (chủ kênh yêu cầu 29/10/2026, áp dụng mọi video Góc IoT).** Ảnh bìa dọc 1080×1920: lấy khung cảnh mở đầu có Bóng lớn (`TLFILE=giong/thoi-luong.json AT=3.5 node dung_hinh.cjs <số> <thư mục> at`), rồi `node goc-iot/tao_bia.cjs <khung.png> goc-iot/bia/bia-<số>.jpg "<dòng gây tò mò>" "<dòng phụ>"` (thanh navy phía dưới + nhãn Góc IoT). Xem ảnh ở cỡ lớn trước khi giao. Workflow `goc-iot-telegram.yml` tự gửi `goc-iot/bia/bia-<số>.*` ngay sau video có cùng số; chỉ gửi bìa của video nằm trong `goc-iot/video/`. Bìa video 11 là mẫu.
