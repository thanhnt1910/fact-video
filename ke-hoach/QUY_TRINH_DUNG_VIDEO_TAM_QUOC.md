# Quy trình dựng video dài Tam Quốc (kênh Người Gác Sử)

Soạn 03/11/2026 từ CLAUDE.md, các file kế hoạch trên nhánh `tq9-anh` (Chu Du, Điêu Thuyền) và mã nguồn trong repo. Ví dụ gần nhất: video "Chu Du có thật sự bị Gia Cát Lượng chọc tức đến chết" (mã `CD`, 76 câu + 9 ảnh phần hai, 24 clip Veo).

Tóm tắt một dòng: **kịch bản (có kiểm nguồn) → chủ kênh duyệt → kế hoạch ảnh và Veo → vẽ ảnh + kiểm → chủ kênh tạo clip Veo → đọc giọng + kiểm → dựng → kiểm video → gửi Telegram.**

Quy tắc chung: workflow (vẽ, giọng, dựng) chỉ chạy khi chủ kênh yêu cầu, và chỉ chạy đúng video được yêu cầu.

---

## Bước 1. Viết kịch bản và tự kiểm nguồn

- File: `ke-hoach/<tên-video>-kich-ban.md`. Mỗi câu có nhãn độ chắc ([SỬ], [CG], [GT]) và mục "Trạng thái kiểm chứng", "Chi tiết đã bỏ khỏi lời kể".
- Lời kể là một mạch chuyện liền, theo nguyên nhân – kết quả. Không chen "tiểu thuyết kể thế này, sử chép thế kia", không tên sách, không chú giải.
- Câu ngắn, từ đời thường; năm viết bằng chữ ("năm một trăm chín mươi sáu"); họ tên đủ mỗi lần nhắc; bỏ từ Hán Việt cổ; không dùng địa danh dễ nhầm như "Hà Nội".
- Độ dài: video dài tối thiểu 10 phút (sàn). Kịch bản chuẩn 20–22 phút ≈ 3.600–3.960 chữ. Thiếu thì gộp thêm hồi có nguồn, không độn.
- **Tự kiểm TRƯỚC khi gửi chủ kênh (quy định 03/11):** tra từng tên, năm, con số, lời trích bằng nguồn gốc (Wikisource, ctext…), ít nhất hai nguồn độc lập cho số liệu quan trọng. Không gửi bản còn nhãn [SỬ*] hay mục "phải kiểm". Bản gửi nêu rõ: bao nhiêu câu đã kiểm nguyên văn, bao nhiêu hạ nhãn hoặc bỏ, câu nào còn tranh cãi.
- Cho kiểu video "tiểu thuyết và chính sử": được sáng tạo ở cách kể (mở bằng cảnh gây tò mò có thật trong video), không đổi sự kiện, kết cục, nguyên nhân.
- Chủ kênh duyệt kịch bản rồi mới chuyển sang `scripts/<MÃ>.json`.

## Bước 2. Chuyển sang `scripts/<MÃ>.json`

- Trường `long.chapters[].beats[]`: mỗi beat một câu lời kể (`text`), kèm `anh_file` (ảnh 2D vẽ sẵn, ví dụ `assets/anh_2d/<MÃ>/001.jpg`) và `clip_file` nếu có clip Veo.
- Các trường chính: `title`, `title_card`, `thumb_title`, `description`, `voice` (Sadaltager), `giong_them` (chỉ dẫn sắc thái), `chuyen_canh` (`fade` cho video 2D), `bia`, `binh_luan`, `sources`, `nguon_link`.
- Mỗi ảnh chỉ dùng một lần trong video dài (khóa ảnh = số câu). Câu đọc quá dài so với clip thì có ảnh phần hai (mã = 100 + số câu).
- Đẩy file này lên `main` có thể tự kích hoạt `render.yml` (trigger `scripts/**`). Chỉ đẩy khi chủ kênh cho dựng.

## Bước 3. Kế hoạch ảnh và Veo

File `ke-hoach/<tên>-veo.md` (hoặc `...-anh-va-veo.md`). Đầu file nêu: tổng ảnh, số clip Veo (≥ 20), số cảnh hoạt hình nhẹ, số ảnh tĩnh.

Phân nhóm mỗi ảnh vào đúng một nhóm:
- **A — Veo (ảnh → video):** cảnh chính quan trọng với cốt truyện, có chuyển động rõ (hành quân, đám đông, người bước đi, hành động nhỏ chậm). Tối thiểu 20 clip mỗi video dài.
- **B — `anim_nhe.py`:** cảnh vật, vắng người; chỉ cờ, nước, lửa, khói chuyển động nhẹ. Cần `ke-hoach/nhan-vat/<MÃ>_nhe.json`.
- **Còn lại — ảnh tĩnh.**
- Không máu, không cảnh chém giết.

Căn clip với câu đọc (quy tắc 03/11): clip dài 8 giây. Lệch ≤ 1,0 s giữ khung cuối; 1,0–1,5 s giữ khung cuối hoặc làm chậm; trên 1,5 s phải có ảnh phần hai. Thời lượng câu lúc này chỉ là ước tính (khoảng 2,7 chữ/giây), **tính lại bằng thời lượng thật sau khi đọc giọng**.

Ba loại ảnh ghi vào kế hoạch từng câu: (a) cảnh người, (b) cảnh vật có nghĩa, (c) minh họa ẩn dụ (khoảng 15–25% ở video kiểu tiểu thuyết và chính sử). Câu giải thích, câu hỏi, so sánh nguồn không vẽ tả thực mà dùng hình minh họa sáng tạo (ví dụ dấu hỏi chấm vàng phát sáng). Cột "Ý của ảnh" do chủ kênh duyệt trước khi vẽ.

Prompt Veo:
- **Không nêu tên riêng người thật**, chỉ tả chung ("the man at the bow", "the old general"). Cột "Cảnh" tiếng Việt ghi rõ "KHÔNG dán vào Veo".
- Dán tiền tố giữ phong cách (cảnh Hán / cảnh Tống), rồi prompt chuyển động chia theo giây (0–3 s, 3–6 s, 6–8 s).
- Trước khi giao: `python kiem_prompt_veo.py ke-hoach/<file>.md` phải báo ĐẠT.

## Bước 4. Vẽ ảnh và kiểm

Sinh script prompt: `ke-hoach/nhan-vat/tao_<MÃ>.py` → ra `<MÃ>.json` (nhân vật) và `<MÃ>_anh.json` (từng ảnh: `nv`, `text`, prompt).

Quy tắc prompt (xem `ke-hoach/quy-tac-ve-anh-giam-loi.md`):
- Tả điều cần có, không dựa vào câu cấm ("no text" hay bị vẽ đúng thứ cấm). Dùng bảng thay vật dễ lỗi: đèn → đĩa dầu đồng; ghế tựa → chiếu và bục thấp; cờ → "plain blank cloth banner"; cuộn tre, sách, biển → không đặt vào cảnh.
- Cảnh một người: "exactly ONE man only". Cảnh vật trống: "completely empty, absolutely no people". Thêm "single full-frame picture, full-bleed, no panels".
- Đúng thời Hán (hoặc Tống với cảnh người kể chuyện phố). Màu sáng, tươi; trang phục lụa thêu đẹp, mỗi nhân vật một màu áo riêng.
- Ảnh Veo khung đầu cần Veo nhận 16:9; ảnh vẽ khổ 1920×1088 trên Kaggle.

Quy trình vẽ:
1. **Vẽ thử 10 cảnh đại diện** trước, soi, sửa prompt chung, rồi mới vẽ phần còn lại.
2. Vẽ dư khoảng 10% ở loại cảnh hay hỏng; ảnh quan trọng và ẩn dụ vẽ 2 bản.
3. **Đẩy prompt lên nhánh TRƯỚC khi chạy workflow**, xác nhận `git ls-remote` khớp `HEAD`.
4. Chạy workflow `ve-anh-2d.yml` (tham số `ma`, `lam_lai`, `dot`, `vong`, `hau_to`; chỉ một kernel, không chạy song song) hoặc lệnh `python ve_kiem_anh.py <MÃ>`. Tối đa 3 vòng vẽ lại.
5. Script vẽ không được báo "ĐẠT" khi không vẽ ảnh mới: kiểm số ảnh thật sự mới (ngày giờ file hoặc log "đã vẽ N ảnh").

Kiểm ảnh, theo thứ tự:
1. Lọc tự động: kỹ thuật (nhỏ, mờ, một màu), viền khung, chữ (OCR), ảnh trùng.
2. Gemini xem từng ảnh (`kiem_tra_2d.py`; chỉ là phụ, có thể bị giới hạn lượt).
3. **Soi mắt ở cỡ lớn** (tối đa 6 ảnh một tấm, không soi bản thu nhỏ): thừa/thiếu tay ngón, hai người giống hệt, vật hiện đại, vật sai cấu tạo, ngựa méo hoặc thừa chân, viền khung, chữ lạ, vũ khí bị đổi chéo.
4. Ảnh lỗi cất vào `assets/anh_2d/<MÃ>/_loi/`, vẽ lại. Báo cáo: `logs/kiem_2d/<MÃ>_tong_hop.txt`. Phải đọc báo cáo trước khi chuyển sang clip hoặc dựng.
5. Gửi chủ kênh từng ảnh một (đặt tên theo số câu) sau khi cả đợt vẽ xong, không gửi ảnh ghép.

## Bước 5. Clip Veo (chủ kênh làm)

- Chủ kênh tạo clip trong Google Flow ("Frames to Video"): khung đầu là ảnh gốc, 16:9, 8 giây, tắt âm. Làm thử 3 clip trước.
- Veo có thể hết hạn mức giữa chừng; clip nhận được lưu vào `assets/clips_2d/<MÃ>/E4_NNN.mp4` kèm `danh_sach.json`.
- Kiểm: so khung đầu clip với ảnh nguồn (tương quan từ 0,9 trở lên). Veo tự vẽ lại khung đầu thì bỏ clip (để `_bo_qua/`), cảnh đó dùng ảnh tĩnh. Tiêu đề file chủ kênh đặt có thể sai, chỉ tin khung hình.
- Khi dựng, clip được cắt bỏ chữ Veo ở góc (crop 95%), phóng lên 1080p, bỏ tiếng gốc, 24 fps.
- **Chờ chủ kênh báo đủ clip rồi mới dựng**; cảnh thiếu clip dùng ảnh tĩnh với hiệu ứng máy quay.

## Bước 6. Giọng đọc

- Giọng Gemini Sadaltager, chỉ dẫn sắc thái theo loại chương (`am_thanh.sac_thai`) cộng `giong_them` trong kịch bản; từ điển phát âm `tu_dien_phat_am.json`. Hồ sơ đọc của Chu Du chậm hơn chuẩn (khoảng 2,7 chữ/giây).
- Đọc thử vài câu bằng `doc_mau_tq9.py` (mẫu cho mã khác) để chủ kênh nghe trước.
- **Trước khi đọc:** nếu dùng đường phim bản đồ thì chạy `python phim_ban_do/kiem_kich_ban.py <tên>` (0 ❌).
- Hạn mức Gemini: cần tối thiểu 10 khóa; mỗi lần chỉ đọc đoạn còn thiếu, không xóa giọng đã đọc tốt (bộ nhớ đệm `assets/tts_cache`). Hết hạn mức thì dừng và báo chủ kênh, không đợi quá 15 phút.
- Đọc cả video theo một cách (cùng mô hình, cùng kiểu cụm) để nhịp và âm lượng đồng đều; chỉ đọc lại riêng các đoạn lỗi (tối đa 3 lần mỗi đoạn, vẫn lỗi thì đổi chữ nhẹ).
- Chuẩn hóa: `loudnorm=I=-16:TP=-1.5:LRA=11` từng đoạn; đoạn lệch tốc độ quá 5% chỉnh bằng `atempo` trong khoảng 0,90–1,10; cập nhật `thoi_luong.json` rồi mới tính phụ đề.
- Kiểm giọng: `python phim_ban_do/kiem_giong.py <tên> [--nguong 0.9] [--xoa]`, phải sạch trước khi dựng. Nhận dạng giọng chạy bằng workflow `phude-asr.yml` sau khi giọng đã chốt.
- **Sau khi có giọng thật:** tính lại bảng căn thời lượng câu – clip, thêm hoặc bỏ ảnh phần hai cho câu còn lệch.

## Bước 7. Dựng video

- Workflow `render.yml`: chạy khi đẩy `scripts/**` lên `main`, hoặc chạy tay (`workflow_dispatch`) với ô `only` = mã video (ví dụ `CD:dai`), `send` (có gửi Telegram ngay không), `bo_qua_kiemtra`, `hau_to` (bản thử, ví dụ `-thu`), `gui_lai`.
- Trình tự trong `ci_render.py` → `long_video.py` → `long_render.py`: kiểm kịch bản và ảnh trước khi dựng → nạp ảnh 2D vẽ sẵn (`anh_file`) → ghép clip Veo vào đầu cảnh → đọc giọng (bộ nhớ đệm) → chuyển cảnh `fade` → ghép âm thanh và nhạc → xuất `output/<mã>/<mã>_dai.mp4` cùng ảnh bìa, mô tả YouTube.
- Lỗi giọng Gemini hết lượt thì dừng, lần chạy sau (7h17 sáng giờ Việt Nam hằng ngày) làm tiếp.
- Đường dựng khác: phim bản đồ (`phim_ban_do/`, workflow `dung-v1.yml`, `dung-v2.yml`, `dung-quan-do.yml`), dựng chia 16 đoạn song song, bước cài dùng chung `.github/actions/cai-dat`. Job treo bước cài thì `gh run rerun <id> --failed`, không hủy cả run.
- Sau khi dựng **đo thời lượng thật**: dưới 10 phút phải bổ sung kịch bản, không đăng.

## Bước 8. Kiểm video trước khi giao

- `python phim_ban_do/kiem_video.py <tên> --tts <file> --video <mp4>` (với phim bản đồ); báo cáo `logs/kiem_video/<tên>.md`. Có ❌ thì không giao.
- `review.py`: dưới 10 phút báo ⚠️ (vẫn gửi), dưới 6 phút báo ❌ (không gửi Telegram).
- Tự xem khung hình mẫu ở cỡ lớn (đầu, giữa, cảnh đông nhất, câu cuối) và nghe lại chỗ nối giữa các câu đã sửa.
- Với video bản đồ: mọi chữ nằm gọn trong khung 1920×1080 (lề ≥ 60 px), ít banner khi đánh nhau, không đùa anh hùng dân tộc.

## Bước 9. Ảnh bìa, mô tả, gửi Telegram

- Ảnh bìa luôn có logo cây đèn `assets/logo/nguoi-gac-su.png` (vuông 130 px, độ đậm 0,8, góc trên phải, cách mép phải 44 px, mép trên 34 px). Mẫu `assets/bia/NQ1/tao_bia.py`. Xem bìa ở cỡ lớn trước khi giao.
- Mô tả và bình luận ghim: ghi nguồn rõ; bình luận ghim là giải thích ngắn (từ tập 3 trở đi theo quy định hiện hành của CLAUDE.md), không câu hỏi chọn đáp án.
- Gửi: `send.yml` (có ô `hau_to` cho bản thử); video sang Telegram sau khi chủ kênh duyệt. Sổ video đã gửi nằm trong repo, mỗi video chỉ gửi một lần trừ khi `gui_lai`.
- Bài Facebook: câu ngắn, mở bằng điều gây tò mò, mốc thời gian tối đa 5 dòng, nguồn dài để ở bình luận; mẫu `telegram/sl21_bai_facebook.txt`.

---

## Danh sách việc cho một video mới (rút gọn)

1. Kịch bản đã tự kiểm nguồn, chủ kênh duyệt
2. `scripts/<MÃ>.json`
3. Kế hoạch ảnh + Veo, `kiem_prompt_veo.py` ĐẠT
4. Vẽ thử 10 cảnh → vẽ cả bộ → kiểm → soi mắt → gửi ảnh từng tấm
5. Chủ kênh tạo clip Veo, kiểm khung đầu
6. Đọc giọng → `kiem_giong.py` sạch → chuẩn hóa → tính lại căn clip
7. Dựng (`render.yml`), đo thời lượng ≥ 10 phút
8. Kiểm video, bìa có logo, mô tả có nguồn
9. Gửi Telegram

## Phần tôi chưa kiểm chứng được

- Không lấy được toàn bộ nhánh `tq9-anh` về máy (kho nặng), nên chưa đọc mã dựng mới nhất trên nhánh đó. Đường dựng ở Bước 7 lấy từ `main`; nhánh `tq9-anh` còn có `doc_mau_tq9.py`, `xuat_giong_tq9.py` chưa gộp vào `main`.
- Chưa thấy file ghi rõ video Chu Du/Điêu Thuyền dùng `render.yml` hay đường phim bản đồ để dựng cuối; hai đường đều được mô tả ở trên. Nếu bạn đang dùng đường khác, cho tôi biết để tôi sửa.
