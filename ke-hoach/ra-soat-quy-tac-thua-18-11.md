# Rà soát quy tắc thừa trên nhánh `claude/cach-ho-cai-tri-tap-1` (18/11/2026)

**Trạng thái: CHỜ CHỦ KÊNH DUYỆT. Chưa xóa, chưa sửa quy tắc nào.**

Phạm vi đã đọc: `CLAUDE.md` (583 dòng, 61 mục `##`, ~124 KB), `quy-tac/nguyen-tac-cot-loi.md`, `quy-tac/thuy-mac.md` (296 dòng), `thuy-mac-khung.md`, `thuy-mac-giong-van.md`, `thuy-mac-mau.md`, `PROMPT_KICH_BAN.md` (199 dòng), `review_checklist.md`, `ke-hoach/ra-soat-kiem-khung-18-11.md`. Chưa đọc kỹ từng dòng của `PROMPT_KICH_BAN.md` mục 20–170 và 5 bộ kiểm `kiem_*.py` (xem mục E).

Nhận xét chung: CLAUDE.md phình vì mỗi lần chủ kênh sửa thì thêm một mục mới, ít khi gỡ mục cũ. Hậu quả là cùng một việc có 2–4 mục nói khác nhau, và phiên Claude mới phải đọc ~124 KB mới biết quy tắc nào còn sống.

## A. Đã bị bỏ nhưng vẫn nằm nguyên văn (xóa hẳn được)

| Vị trí | Nội dung | Ghi chú |
|---|---|---|
| dòng 109–110 (mục Tam Quốc kể liền mạch) | Hai gạch "năm viết bằng chữ", "từ Hán Việt cổ không đưa vào" | Đã gạch **[ĐÃ BỎ 05/11]** ngay tại chỗ, còn nguyên chữ cũ |
| mục "Làm kịch bản bằng ngôn ngữ tự nhiên" (dòng 290–301) | Gạch "không nhắc tên sách", gạch "tránh câu khuôn máy" | Cùng đánh dấu ĐÃ BỎ. Các gạch còn lại của mục (không mở câu cùng kiểu, nhịp dài ngắn, không giải nghĩa từ điển) vẫn sống, nên chỉ xóa 2 gạch |
| mục "Nới quy tắc viết kịch bản" (dòng 334–342) | Chính mục này | Là bản ghi "bỏ gì", nên khi các mục gốc đã xóa sạch thì mục này chỉ còn là lịch sử. Giữ 1 dòng "đã bỏ: cấm nhắc sách, cấm chữ số, cấm ngoặc kép, cấm từ cổ, giới hạn 15 chữ" |
| dòng 246 và 561 liên quan | "(giới hạn 15 chữ đã bỏ 05/11)" chú thích cạnh quy tắc | Xóa phần chú thích, giữ câu |
| mục "Series lịch sử Việt Nam" dòng 203 | "Giới hạn thời gian: ĐÃ BỎ" | Gộp thành một dòng ở nguyên tắc cốt lõi (đã có trong `thuy-mac.md` mục 1) |
| dòng 510 | "bỏ giới hạn 1858" | Lịch sử của lộ trình, không phải quy tắc |
| dòng 227 | "Video Ngô Quyền đã giao chưa áp dụng bước này" | Ghi chú tiến độ, không phải quy tắc |
| dòng 331 | "tập 1 hiện dài hơn (khoảng 100 giây)" | Ghi chú tiến độ |

## B. Quy tắc của loạt đã dừng hoặc đã thay hướng (đề nghị chuyển sang `ke-hoach/luu-tru-quy-tac/`, không xóa)

Đây là phần lớn nhất. Khoảng một nửa CLAUDE.md thuộc nhóm này, và chỉ có tác dụng nếu chủ kênh quay lại loạt đó.

1. **Tam Quốc: ảnh, Veo, tập gộp** (dòng 39–152): "Phân nhóm cảnh A/B/ảnh tĩnh", "Prompt Veo không nêu tên", "Lỗi ảnh hay gặp", "Quy tắc vẽ ảnh 1–14", "Cập nhật 18/10 tập gộp 4+5 (quy tắc 15–22)", "Veo cho tập gộp", "Quy trình vẽ ảnh một tập", "Git" kèm nhánh. Khoảng 110 dòng. Nhắc kiểu "tự kiểm bằng `ve_kiem_anh.py`", "ảnh Kaggle", "Cloudflare không dùng". Tam Quốc đã chuyển hướng sang bản đồ rồi sang Sengoku, và chủ kênh đã nói không làm Veo thủ công.
2. **Hán Sở tranh hùng** (dòng 201 và rải rác): đã DỪNG 23/10, chỉ còn nhắc ở các mẫu như `hs1_content.py`.
3. **Video bản đồ 16:9** (4 mục: dòng 154 chữ trong khung, 160 bố cục gọn mắt, 274 mặt nhân vật, 284 tiếng nền): ~45 dòng, dựa trên `mapfilm3.py`. Chủ kênh đã bỏ kiểu bản đồ 16:9 (mục dòng 321: "đã bỏ các kiểu: bản đồ 16:9, …") nhưng 4 mục này vẫn để như đang áp dụng "mọi tập".
4. **Series Việt Nam kiểu Puck/Đinh Bộ Lĩnh** (dòng 184–197, 258–268, 310–318): quy trình giọng Puck cum 8 → cum 16 → cắt lại cụm → chuẩn hóa → cân âm sắc. Cả ba cách đã bị mục dòng 364 ("dùng nguyên giọng gốc, KHÔNG chỉnh") thay thế.
5. **"Chuyện cai trị ngàn năm" 9:16 bản đồ phủ kín** (dòng 320–332, 372–390, 412–436): vẫn còn hiệu lực nếu loạt này tiếp tục, nhưng phần "bài học tập 2 dựng lại" chỉ là danh sách lỗi một lần.
6. **Loạt "Bí mật biểu tượng" và "Vĩ nhân"** (dòng 447–544): đã có skill `viet-kich-ban-bi-mat-bieu-tuong` làm nguồn chính (chính CLAUDE.md dòng 504 và skill đều nói thế). Phần kịch bản trong CLAUDE.md trùng với skill, nên chỉ giữ trong skill. Phần dựng hình (nền, boom, dấu ấn) giữ ở một tệp riêng.
7. **Series "Tên tỉnh thành"** (dòng 545–549) và **hook "lật lại" thử nghiệm** (dòng 485–492): thử nghiệm đang chờ số liệu; số liệu Metricool hôm nay cho thấy hook "lật lại" chưa chứng minh được. Đề nghị xếp vào "đang thử nghiệm", không phải luật.

## C. Trùng lặp (gộp lại thành một)

| Chủ đề | Các mục đang nói | Đề nghị |
|---|---|---|
| Chuẩn hóa/cân giọng | dòng 219 (loudnorm + atempo), 258–264 (cắt cụm + chuẩn hóa), 310–318 (cân âm sắc), **364 (cấm mọi chỉnh sửa)** | Chỉ giữ mục 364. Ba mục kia bị thay thế hoàn toàn nên **tự mâu thuẫn** (một mục bắt `loudnorm`, một mục cấm `loudnorm`) |
| Đọc cụm | dòng 188 (cum=8), 260 (cum=16), 364 (cum=15), 8 ở dòng 184 | Giữ một con số, ghi "tùy hạn mức, cùng một lượt cho cả video" |
| Ảnh bìa | dòng 230 (logo, khung bản đồ), 252 (bìa 4 chữ), 372 (bìa dọc 1080×1920 mẫu HAN1), 476 (bìa đúng cốt truyện + hook) | Gộp thành một mục "Ảnh bìa": logo, ≤4 chữ, đúng chủ thể, hook đỏ, kiểm chữ dấu |
| Bố cục mở đầu | dòng 244 (24/10 3 giây/3 phút), dòng 485 (hook lật lại), skill Bí mật biểu tượng (Bước 3b, 25 giây đầu), `nguyen-tac-cot-loi.md` | Giữ nguyên nguyên tắc cốt lõi + một mục ngắn "mở đầu"; các số "tối đa 40 giây", "1 phút 30", "45%" chuyển thành gợi ý |
| Câu mở/nhịp câu | dòng 290–301 (tự nhiên), 536–544 (câu chữ sáng tạo), 550–559 (văn xuôi trước), `thuy-mac-giong-van.md` | Một mục "Văn phong" |
| Chạy workflow/Git | dòng 214–217, 138–150 (Git), 270–272 (429), 560–563 | Một mục "Workflow và Git" |
| Gửi duyệt | dòng 438–441 (kiểm đầy đủ), 515–519 (cấm đẩy việc kiểm), 565 (rà 5 điểm) | Một mục "Gửi duyệt" |
| Hoàng Sa/Trường Sa | CLAUDE.md dòng 432, `review_checklist.md` dòng 38, skill | Giữ ở một nơi (CLAUDE.md), `review_checklist.md` chỉ trỏ tới |
| Độ dài | dòng 10–18 (10 phút, 1.900 chữ), 3 (60–80 giây), 253, 331, 464, `PROMPT_KICH_BAN.md` 9, 19, 103–128 | Một mục "Độ dài" (xem D2) |
| "Khung 6 câu hỏi" (dòng 391), "Mạch kể" (504), "bốn bước" (nguyên tắc cốt lõi) | Ba cách dựng kịch bản | Giữ bốn bước của nguyên tắc cốt lõi; 6 câu hỏi chỉ là danh sách kiểm đủ ý (skill đã hạ như vậy) |

## D. Mâu thuẫn với nguyên tắc cốt lõi hoặc với nhau (cần chủ kênh quyết)

1. **Giọng nguyên bản và cân giọng**: xem C, mâu thuẫn trực tiếp. Đề nghị theo mục 364.
2. **Độ dài tối thiểu 10 phút/1.900 chữ** (dòng 10–18, `PROMPT_KICH_BAN.md`, `review.py`: ❌ dưới 6 phút) so với nguyên tắc cốt lõi (chất lượng kể chuyện trên mọi quy tắc khác) và `thuy-mac` hiện nay (tập tm ngắn). Câu hỏi cho chủ kênh: sàn 10 phút còn là ràng buộc, hay chỉ còn là mức tham khảo cho video dài YouTube?
3. **"Tập sau sẽ kể tiếp"/"Hẹn bạn ở tập tiếp theo"** (dòng 142–152, 380–384) so với "mỗi video trọn gói, không có tập sau" (dòng 240, `thuy-mac.md` mục 1). Hai loạt khác nhau, nhưng CLAUDE.md không nói rõ luật nào cho loạt nào.
4. **Câu hỏi gây tò mò và "câu hỏi xuyên suốt"** (dòng 244–256, `thuy-mac-khung.md`) đã hạ xuống tham khảo trong thuy-mac, nhưng CLAUDE.md vẫn nói "bố cục... áp dụng mọi video từ nay" với số cứng (40 giây, 45%, 60–90 giây một móc).
5. **"Chỉ chuyện có thật, không bịa nội tâm"** (dòng 21) với "người kể được diễn giải" (nguyên tắc cốt lõi mục 7). Hai điều hợp nhau nếu hiểu "diễn giải của người kể" khác "nội tâm gán cho nhân vật", nên cần một câu phân biệt ở một chỗ duy nhất.
6. **Cloudflare**: dòng 124 "Cloudflare Workers AI hết hạn mức sớm, ảnh kém: không dùng" nhưng hôm nay chủ kênh bảo "vẽ ảnh dùng CF" và workflow `cf-thuy-mac.yml` đang sống. Sửa dòng 124 thành mô tả đúng (dùng được cho thủy mặc, dừng ở 429).
7. **Veo**: CLAUDE.md có ~12 gạch về Veo (tối thiểu 20 clip, nhóm A, không tên riêng...) trong khi chủ kênh nói "không muốn thủ công". Các gạch đó chỉ nên còn ở lưu trữ Tam Quốc.
8. **Câu chốt sổ**: `review_checklist.md` dòng 11 bắt video ngắn kết bằng câu "Sử thật… lạ hơn cả truyện" và không giới thiệu chuyện tiếp theo. Còn nguyên tắc cốt lõi mục "đoạn cuối = tóm tắt + cảm ơn". Chọn một.
9. **Tham chiếu tệp hỏng**: đã kiểm 10 đường dẫn mẫu, 9 còn, **1 thiếu: `ke-hoach/tam-quoc-tap-4-5-veo.md`** (CLAUDE.md dòng ~133–136 trỏ tới). `claude/tam-quoc-*.md` nằm trong Project chứ không ở repo. Chưa kiểm hết mọi đường dẫn trong CLAUDE.md (xem E). Các tệp `quy-tac/chung.md`, `su-viet.md`, `ky-thuat-ke-chuyen.md` **không có** trong thư mục `quy-tac/` (chỉ 5 tệp), nên nếu ở đâu đó trỏ tới thì đó là tham chiếu hỏng.

## E. Việc chưa làm trong lượt rà này (nói rõ để khỏi hiểu lầm)

- Mới kiểm 10 đường dẫn mẫu, chưa đối chiếu toàn bộ tham chiếu trong CLAUDE.md với cây thư mục (mục D9).
- Chưa đọc từng dòng `PROMPT_KICH_BAN.md` 20–170 và `kiem_*.py`; phần kiểm khung đã có `ra-soat-kiem-khung-18-11.md`. Các bộ kiểm khác (`kiem_kich_ban`, `kiem_mo_dau`, `kiem_mach_ke`, `kiem_giong_van`) vẫn chặn ❌ theo luật cũ (ví dụ mở đầu, mạch kể, câu mở) trong khi nguyên tắc cốt lõi nói công cụ chỉ là công cụ biên tập. Cần rà tiếp giống mục B và C của tệp rà kiểm khung.

## F. Đề xuất hành động (xin duyệt từng nhóm)

1. **Xóa ngay (A)**: ~10 gạch/chú thích đã đánh dấu ĐÃ BỎ hoặc là ghi chú tiến độ. Rủi ro thấp.
2. **Chuyển sang lưu trữ (B1–B4)**: tạo `ke-hoach/luu-tru-quy-tac/{tam-quoc,ban-do-16x9,giong-puck}.md`, giữ nguyên chữ, CLAUDE.md chỉ để một dòng trỏ tới. Dự kiến CLAUDE.md giảm còn ~55% (khoảng 320 dòng).
3. **Gộp (C)**: viết lại thành 6–7 mục ngắn (Văn phong, Mở đầu, Giọng đọc, Ảnh bìa, Gửi duyệt, Workflow/Git, Độ dài). Cần chủ kênh xem bản gộp trước khi thay.
4. **Quyết (D2, D3, D8)**: ba câu hỏi chủ kênh trả lời được trong một dòng mỗi câu.
5. **Sửa dòng 124** (Cloudflare) ngay vì đang sai thực tế hôm nay.

Không nhóm nào được làm khi chưa có duyệt.

---

## G. Trạng thái thực hiện tái cấu trúc (cập nhật 18/11/2026 tối, theo kế hoạch chủ kênh)

**Chủ kênh đã quyết (18/11):** (1) bỏ sàn 10 phút, độ dài theo chất liệu; (2) bỏ câu kết "tập sau" mặc định; (3) chuyển Tam Quốc, Hán Sở, bản đồ 16:9, Puck sang lưu trữ, không xóa tài liệu tái sử dụng, không xóa file khi chưa kiểm hết đường dẫn.

**Đã làm (bước 1–5 và một phần bước 6):**
- Sao lưu: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md` (nguyên bản 583 dòng).
- Chuyển nguyên văn 60/61 mục bằng script (không gõ lại): bảng đích xem bên dưới. Mục 0 (nguyên tắc cốt lõi) ở lại CLAUDE.md.
- CLAUDE.md mới (~95 dòng): vai trò, thứ tự ưu tiên, quy trình bốn bước, bốn cổng duyệt, quy định tài liệu, công cụ kiểm, xử lý mâu thuẫn, bản đồ tài liệu.
- File mới: `quy-tac/dna-series.md`; phần "Độ dài và câu kết" trong `quy-tac/dung-mach-truyen.md`; phần "Git và workflow" và "Kiểm đường dẫn" trong `quy-tac/kiem-tra-ky-thuat.md`.
- Công cụ mới: `tools/kiem_lien_ket.py` (quét đường dẫn; hiện ĐẠT với CLAUDE.md, quy-tac/, mau-kich-ban/, PROMPT_KICH_BAN.md, review_checklist.md).
- Sửa 4 tham chiếu hỏng trong `nguyen-tac-cot-loi.md`, `thuy-mac.md`, `thuy-mac-giong-van.md` (trỏ tới `chung.md`, `su-viet.md`, `ky-thuat-ke-chuyen.md` vốn chỉ có ở nhánh khác). Chỉ sửa chỗ trỏ, không đổi nội dung quy tắc.
- Nhập từ nhánh `lh6-dung-thu` đúng một mục: "Diễn giải của người kể" (chủ kênh duyệt 01/11), vì nguyên tắc cốt lõi dựa vào nó. Đã vào cuối `quy-tac/giong-van.md`.
- `review.py`: thời lượng ngoài mức tham khảo chỉ còn ⚠️ (trước đây dưới 6 phút là ❌ chặn gửi).
- `PROMPT_KICH_BAN.md`: thêm ghi chú đầu file rằng sàn 10 phút và "tập sau" không còn bắt buộc; chưa viết lại thân file.
- Bộ kiểm hạ ❌ → ⚠️ vì chỉ là khung/đếm số: `kiem_mo_dau.py` (2 mục), `kiem_mach_ke.py` (2 mục), `kiem_giong_van.py` (3 mục). `kiem_kich_ban.py` giữ nguyên (chỉ chặn giới hạn kỹ thuật giọng đọc: >32 chữ, >2 câu, nói tắt, tên thiếu họ, mệnh đề chen).

**Bảng đích của 61 mục CLAUDE.md cũ (chỉ số theo thứ tự `##`, bắt đầu từ 0):**
| Đích | Mục |
|---|---|
| ở lại CLAUDE.md | 0 |
| `archive/tam-quoc.md` | 4–13 |
| `archive/video-ban-do-16-9.md` | 14, 15, 27, 28 |
| `archive/giong-doc-puck.md` | 17, 21, 25, 31, 44 |
| `archive/quy-dinh-da-thay-the.md` | 1 (sàn 10 phút), 38 (câu kết tập sau) |
| `quy-tac/nghien-cuu-su-lieu.md` | 2, 18 |
| `quy-tac/dung-mach-truyen.md` | 23, 24, 40, 50, 52 |
| `quy-tac/giong-van.md` | 19, 29, 33, 56, 58, 60 (+ mục diễn giải nhập từ nhánh khác) |
| `quy-tac/bien-tap.md` | 43, 54 |
| `quy-tac/kiem-tra-lich-su.md` | 39, 42 (bản đồ, Hoàng Sa, Trường Sa) |
| `quy-tac/kiem-tra-ky-thuat.md` | 16, 20, 26, 36, 41, 59 |
| `quy-tac/tim-cau-chuyen.md` | 53 |
| `quy-tac/dang-bai-va-bia.md` | 3, 22, 30, 37, 49 |
| `quy-tac/series/chuyen-cai-tri-ngan-nam.md` | 32 |
| `quy-tac/series/bi-mat-bieu-tuong.md` | 45, 46, 47, 48, 51, 55 |
| `quy-tac/series/ten-tinh-thanh.md` | 57 |
| `mau-kich-ban/su-kien.md` | 34, 35 |

**Chưa làm, cần quyết hoặc làm tiếp (giai đoạn 2):**
1. **Gộp trùng trong từng file** (hiện các mục vẫn nằm nguyên văn cạnh nhau): `giong-van.md` (6 mục văn phong), `dang-bai-va-bia.md` (3 mục ảnh bìa), `kiem-tra-ky-thuat.md`, `dung-mach-truyen.md` (mở đầu 24/50). Cần viết lại thành bản ngắn rồi gửi chủ kênh xem trước khi thay.
2. **Chọn một giọng đọc hiện hành:** trong `kiem-tra-ky-thuat.md` mục "giọng gốc 06/11" là quy tắc sống; các mục giọng cũ đã ở `archive/giong-doc-puck.md`. Cần xác nhận mục 36 là duy nhất.
3. **G1. Hai nhánh có hai bộ quy tắc lệch nhau.** Nhánh `lh6-dung-thu`, `nm5-hq-tai`, `cd-dung`... có `quy-tac/chung.md` (218–227 dòng), `su-viet.md`, `ky-thuat-ke-chuyen.md`; nhánh này không có. Chúng ghi những điều trái với nhánh này, ví dụ: "bỏ sàn 10 phút" (30/10, khớp quyết định hôm nay), "bỏ hết lời bình của sử gia" (27/10, nhánh này vẫn cho giữ lời bàn có tên sử gia), "câu kết cuối: một câu tóm gọn và lời cảm ơn" (31/10), "rà 5 lần trước khi giao". Cần chủ kênh quyết: nhập mục nào vào nhánh này, mục nào bỏ. Mình chưa nhập.
4. **`kiem_khung.py`:** áp dụng bảng A của `ra-soat-kiem-khung-18-11.md` (12 mục ❌→⚠️). Quyết định hôm nay của chủ kênh khớp với bảng này, nhưng mình chưa sửa vì bảng ghi chờ duyệt từng mục.
5. **`PROMPT_KICH_BAN.md` và `review_checklist.md`:** còn nguyên nội dung cũ (hai sản phẩm video dọc/Facebook/dài, câu kết "Sử thật… lạ hơn cả truyện"). Cần quyết giữ làm quy trình riêng cho sản phẩm cũ hay gộp.
6. **Thử nghiệm bước 7:** chạy ba chủ đề lịch sử khác nhau qua quy trình mới (bốn bước, bốn cổng, bộ kiểm đã hạ) trước khi coi hệ thống cũ là hết hiệu lực. Chưa làm.
7. Xóa chỗ ĐÃ BỎ còn nguyên chữ ở trong các file đã chuyển (mục A của báo cáo này) sau khi chủ kênh duyệt gộp.
