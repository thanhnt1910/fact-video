# Hướng dẫn cho Claude khi làm việc trong repo này

Repo của kênh "Người Gác Sử": video dọc 60–80 giây và video dài YouTube 16:9, kể chuyện có thật trong lịch sử.

Quy tắc được tách theo series để mỗi phiên làm việc chỉ cần đọc phần liên quan. Nội dung các quy tắc giữ nguyên như khi chủ kênh đặt; chỉ đổi nơi chứa.

## Cách dùng: đọc file nào trước khi làm

Quy tắc chung luôn có hiệu lực (nhập tự động ngay dưới). Trước khi làm việc với một series, PHẢI dùng Read đọc file riêng của series đó, vì CLAUDE.md không tự nạp chúng.

| Đang làm | Đọc file |
|---|---|
| Mọi việc (kịch bản, bài đăng, bìa, git, workflow) | `quy-tac/chung.md` (đã nhập bên dưới) |
| Tam Quốc theo chính sử (video ảnh 2D, Veo) | `quy-tac/tam-quoc.md` |
| Video dạng bản đồ động (dựng, giọng Puck, kiểm video) | `quy-tac/video-ban-do.md` |
| Lịch sử Việt Nam (Đinh Bộ Lĩnh, Lê Hoàn, Lý Công Uẩn, Tây Sơn...) | `quy-tac/su-viet.md` + `quy-tac/video-ban-do.md` |
| Lịch sử thế giới (Hán Sở, Hannibal, Mông Cổ...) | `quy-tac/lich-su-the-gioi.md` + `quy-tac/video-ban-do.md` |
| Tên đường: nhân vật gắn với tên đường (tiểu sử, không giới hạn năm) | `quy-tac/ten-duong.md` + `quy-tac/video-ban-do.md` |
| Vẽ ảnh minh họa bằng FLUX (Cloudflare klein, Kaggle) | `quy-tac/anh/master-style.md` + Period Bible của thời kỳ (`quy-tac/anh/period-<tên>.md`, hiện có `period-ly-tong.md` APPROVED) + `quy-tac/anh/khoi-prompt.json` + `quy-tac/anh/quy-trinh-anh.md` (lưu `detail_tags`, duyệt Scene Planner, phiên bản; kiểm bằng `phim_ban_do/kiem_scene_planner.py`) |
| Quyết định tái sử dụng, hồ sơ nhân vật, Period Bible bổ sung (kiến trúc 4 tầng, DRAFT 01/11/2026) | `quy-tac/anh/quyet-dinh.json` (Decision Registry) + `quy-tac/anh/nhan-vat/<tên>.json` + `quy-tac/anh/period-ly-tong-bo-sung.md` (xem mục "Kiến trúc 4 tầng cho ảnh" bên dưới) |

Series mới: tạo file `quy-tac/<series>.md`, ghi nó vào bảng trên, đừng thêm quy tắc riêng series vào `chung.md`. Quy tắc nào áp cho mọi series thì mới vào `chung.md`.

## Tài liệu khác
- Cách viết kịch bản chi tiết: `PROMPT_KICH_BAN.md`, danh sách điều kiểm: `review_checklist.md`.
- Kế hoạch, kịch bản từng video: thư mục `ke-hoach/`.

@quy-tac/chung.md

## Giọng đọc: luôn dùng Sadaltager (chủ kênh chốt 29/10/2026, áp dụng mọi video từ nay)
- Mọi video (dài và ngắn, mọi series) đọc bằng giọng Gemini **Sadaltager**: workflow `thu-giong-hai.yml` với `-f voices=Sadaltager`. Không đổi sang Puck hay giọng khác nếu chủ kênh chưa yêu cầu.
- Cả video chỉ một giọng, một mô hình, cùng `cum.txt` (xem mục "Giọng đọc đồng đều"). Video ly1 dựng thử bằng Puck cũ chỉ là bản xem trước hình ảnh; bản giao phải đọc lại bằng Sadaltager.
- Kịch bản mới (lt1 và sau) ghi sẵn trong mục "Việc cần chủ kênh quyết" rằng giọng là Sadaltager.

## Nhân vật chibi: vẽ KHÔNG LoRA (chủ kênh đổi lại 29/10/2026 sau khi xem ảnh thật, áp dụng khi làm video kiểu chibi)

- Kết quả thử nằm ở `logs/chibi/tong_hop.jpg` (hàng trên: không LoRA; hàng giữa: LoRA Muapi). Chủ kênh chọn hàng trên vì đẹp và rõ nét hơn: LoRA Muapi (độ mạnh 1,0 và 0,6) làm mặt tròn như bánh, mắt chấm, màu nhợt, các nhân vật giống nhau.
- **Kiểu được chọn:** FLUX.1 schnell (GGUF Q8), KHÔNG nạp LoRA; kiểu vẽ chỉ nằm trong câu lệnh, câu mở đầu prompt `A vibrant chibi-style illustration`. Vẽ trên Kaggle (GPU miễn phí), không dùng Gemini (để dành hạn mức cho giọng đọc). Trong `*_chibi.json` đặt `"lora": 0.0` cho mọi cảnh (mã `kaggle_chibi_ve.py` tự bỏ qua bước nạp LoRA).
- **Không dùng:** `Muapi/chibi-characters-flux-dev` (ảnh xấu như trên); `LoliOverflow/chibi` (LoRA của Stable Diffusion, không nạp được vào FLUX).
- Mã thử: `kaggle_chibi_thu.py`, workflow `chibi-thu.yml`; mã vẽ hàng loạt: `kaggle_chibi_ve.py`, workflow `chibi-ve.yml` (đẩy `ke-hoach/chibi/chay_<mã>.txt`).
- Mỗi cảnh vẫn phải mô tả riêng từng người (tuổi, râu tóc, màu áo) và soi bằng mắt ở cỡ lớn. Các quy tắc ảnh của series (không chữ, không máu, đúng thời, không hai người giống hệt, soi ảnh cỡ lớn) vẫn áp dụng.

## Ảnh Lý Thường Kiệt v4: tranh bán hiện thực bằng FLUX.2 klein (chủ kênh chuyển hẳn 01/11/2026; CHỈ áp dụng cho dự án lt1 v4)
- Dự án Lý Thường Kiệt v4 (`ke-hoach/thu-giong-hai/lt1v4_full.json`) chuyển hẳn sang phong cách **tranh bán hiện thực** theo Master Style, vẽ bằng **FLUX.2 klein trên Cloudflare Workers AI** (khóa API miễn phí, không Worker/D1/R2). Quy chuẩn nằm ở `quy-tac/anh/` (xem bảng đầu file): `master-style.md`, `period-ly-tong.md`, `khoi-prompt.json`, `quy-trinh-anh.md`. Các tài liệu này đã **APPROVED** ngày 01/11/2026 (master-style v1.3, period-ly-tong v1.3, khoi-prompt v1.3, quy-trinh-anh v1.2; xem `quy-tac/anh/CHANGELOG.md`). Chưa lập Scene Planner, chưa vẽ ảnh; chỉ ảnh có trong `tham-chieu-duoc-duyet.json` mới làm tham chiếu.
- Ba mức bằng chứng giữ riêng: A `historical_evidence`, B `cautious_reconstruction`, C `artistic_choice`.
- **Chưa áp dụng cho dự án khác.** Series khác (Tam Quốc, Nguyên Mông, Hồ Quý Ly...) giữ quy tắc ảnh riêng của series đó cho tới khi chủ kênh duyệt riêng việc áp dụng.
- Hai mục dưới đây (chibi lt1 và ảnh phẳng lt1) được giữ nguyên làm lịch sử, KHÔNG xóa, và **DEPRECATED cho lt1 v4**.

## Kiến trúc 4 tầng cho ảnh (chủ kênh duyệt triển khai 01/11/2026; cập nhật sau khi duyệt năm mục cùng ngày)
- **Cập nhật 01/11/2026:** chủ kênh duyệt mục 5 `quy-trinh-anh.md` (nay v1.3 APPROVED; QK-VOI/BANDO/DOAN/GIULAU/DUYET-NT chặn; QK-HOSO còn PROPOSED), DQ-001..004 (APPROVED, vẫn C/visual_only/OWNER_APPROVAL), DQ-005 (râu Lý Thường Kiệt S2 đen pha bạc, C, chỉ S2), 21 chi tiết AC01–AC21; L33 vẽ thêm 4 lính Tống không vũ khí (AC22 CHƯA duyệt); danh sách 33 mục bản đồ được duyệt làm kế hoạch nhưng CHƯA xác minh nên 7 bản đồ vẫn bị chặn. Câu "Cách B" bên dưới là lịch sử; từ nay các quy tắc trên chặn. Các ý còn lại của mục này vẫn đúng.
- **Tầng:** GLOBAL_RULES (`master-style.md`, `quy-trinh-anh.md`, `khoi-prompt.json`, đã APPROVED) → PERIOD_BIBLE (`period-ly-tong.md` APPROVED v1.3 + `period-ly-tong-bo-sung.md` DRAFT; phạm vi niên đại chỉ 1075–1077, KHÔNG mặc định cho cả thời Lý, thế kỷ XII hay thời kỳ khác) → CHARACTER_PROFILE (`quy-tac/anh/nhan-vat/`, nhiều giai đoạn) → PROJECT (`ke-hoach/anh/<mã>/`). Mọi quyết định tái sử dụng nằm ở `quy-tac/anh/quyet-dinh.json`; chỉ lưu quyết định có giá trị tái sử dụng, không lưu lựa chọn nhỏ từng cảnh.
- **Ba trường độc lập mỗi chi tiết:** `evidence_level` (A/B/C = căn cứ lịch sử), `decision_mode` (`AUTO` / `OWNER_APPROVAL` / `MUST_VERIFY` = ai được quyết), `pham_vi` (dùng lại ở đâu). Mục C được chủ kênh duyệt chỉ dùng lại về mặt HÌNH ẢNH (`approval_scope = visual_only`), vẫn là C, `la_du_kien_lich_su = false`; KHÔNG dùng làm căn cứ khi viết lời đọc, mô tả video hay bình luận ghim.
- **AUTO** chỉ khi có quyết định `APPROVED` còn hiệu lực đúng phạm vi và phiên bản; không có thì coi là `OWNER_APPROVAL`. Quyết định `PROPOSED` không bao giờ AUTO. Nhân vật chính và nhân vật có tên theo kịch bản; số người, ngựa, voi theo Scene Planner; bố cục, góc máy, ánh sáng AI tự quyết.
- **Ngoài phạm vi:** không kế thừa quyết định PERIOD sang thời kỳ khác. Thời kỳ chưa có Bible hoặc chi tiết mang khẳng định lịch sử (trang phục, thuyền, lũy, kiến trúc, địa danh, bản đồ, số lượng) → `MUST_VERIFY`, không chuyển thành C để né xác minh; quy ước hình ảnh thuần túy ngoài phạm vi → `OWNER_APPROVAL`.
- **Cổng trước khi vẽ:** cảnh chỉ vào sản xuất khi Scene Planner `PLAN_APPROVED`, không còn quyết định cần duyệt mà chưa duyệt, không còn `MUST_VERIFY` chưa `VERIFIED` kèm nguồn, không có lỗi từ quy tắc cũ đã APPROVED. Kiểm bằng `python phim_ban_do/kiem_scene_planner.py lt1v4 --cong all`. Cảnh báo ở giai đoạn soạn thảo KHÔNG phải giấy phép bỏ qua.
- **Cách B:** các quy tắc kiểm thêm sau ngày duyệt (voi, bản đồ, đoạn nhiều cảnh, giữ lâu, duyệt nghệ thuật; xem `quy_tac_kiem` trong registry, trạng thái PROPOSED) chỉ cảnh báo cho tới khi chủ kênh duyệt mục 5 của `quy-trinh-anh.md`. Các quy tắc cũ đã APPROVED (retry, MANUAL_REVIEW, owner_unlock, đếm người/ngựa, evidence_level bất biến, ảnh tham chiếu phải duyệt) vẫn chặn như cũ.
- **Baseline chỉ đọc** ở `phim_ban_do/baseline_kiem/` (tag git `baseline-kiem-b0-2026-11-01`, `baseline-kiem-b1-2026-11-01`). So sánh trước/sau: `python phim_ban_do/so_sanh_baseline.py`; bộ test: `python phim_ban_do/test_kiem_anh.py`.
- Màu râu Lý Thường Kiệt: `UNDECIDED` (C, OWNER_APPROVAL), chưa khóa; chỉ hỏi chủ kênh khi một cảnh cần thấy mặt.

## [DEPRECATED cho lt1 v4, 01/11/2026] Ảnh chibi Lý Thường Kiệt: lỗi thời đại và cách tránh (chủ kênh phát hiện 30/10/2026)
> DEPRECATED (chủ kênh 01/11/2026): các quy định áo giáp da nâu, nón tre, chân đất, cờ nâu đỏ "plain brown-red triangular cloth pennants" bên dưới KHÔNG còn dùng cho lt1 v4. Thay bằng `quy-tac/anh/period-ly-tong.md` (khăn quấn hoặc búi tóc, nón lá chỉ cho dân phu, giáp chỉ một phần lính, giày dép tùy nhóm, mặc định không vẽ cờ). Nội dung cũ giữ để tra lịch sử, không áp dụng cho dự án khác nếu chưa duyệt.
- Lần vẽ đầu (lt1) có khoảng 34/64 ảnh sai: cờ sao vàng, lính mũ cối và súng, đường nhựa, cột điện, tàu hơi nước, bàn ghế, nến, đèn lồng giấy, chữ Hán trên cờ. Nguyên nhân: prompt chỉ ghi "plain red flags" và không có mốc thời Lý; bỏ LoRA nên mô hình trôi về kiểu phổ biến.
- Không dùng chữ "flag" / "red flag": viết "plain brown-red triangular cloth pennants". Mọi prompt (kể cả cảnh vắng người) phải có mốc "ancient Vietnam, Ly dynasty 11th century, grey tiled roofs and thatched houses" (hoặc Tống) và mô tả lính: áo giáp da nâu, nón tre, chân đất, giáo. Không dùng "chair, table, candle, lantern, ship" trơn: viết "woven mat, low wooden table, clay oil dish, wooden war boat with woven sails". Mã `ke-hoach/chibi/tao_lt1_chibi.py` đã gắn sẵn ERA_VN/ERA_SONG.
- Sau mỗi đợt vẽ phải xem ảnh cỡ lớn (6 ảnh một tấm) và soi cờ, quân phục, đồ vật hiện đại trước khi báo xong.

## [DEPRECATED cho lt1 v4, 01/11/2026] Ảnh phẳng (vector) thay chibi cho video Lý Thường Kiệt (chủ kênh chọn 30/10/2026)
> DEPRECATED (chủ kênh 01/11/2026): quy chuẩn ảnh phẳng/vector của lt1 (mã `phim_ban_do/phang/`, 64 cảnh) không dùng cho lt1 v4, vì v4 chuyển sang tranh bán hiện thực FLUX.2 klein. Mã và ảnh cũ giữ nguyên, không xóa. Quy tắc "ảnh vẽ phải chi tiết" ở cuối mục này chỉ còn áp dụng cho các ảnh phẳng ở dự án khác nếu có.
- Chibi vẽ bằng FLUX không giữ được nhân vật đồng nhất, hay ra phong cách Hàn/Trung và sai thời → video lt1 dùng ảnh phẳng vẽ bằng code: nhân vật mặt đơn giản, nền nhiều lớp. Mã: `phim_ban_do/phang/` (`flat.py` thư viện, `canh.py` 64 cảnh, `ve.py` chạy ra ảnh).
- Chạy: `python phim_ban_do/phang/ve.py [số cảnh ...]` → `ke-hoach/phang/lt1_svg/N.svg` (từng lớp có `<g id>` để làm chuyển động) và `assets/anh_phang/lt1/N.jpg` (1920×1080).
- Số người trong cảnh do mã quyết định, không thừa tay thừa người; mỗi người một tông da, râu, màu áo. Trang phục Việt: áo giao lĩnh tay hẹp, nón lá/khăn quấn; quan Tống: mũ hai cánh. Sửa nhân vật ở `CAST` trong `canh.py`.
- Soi ảnh ở cỡ lớn sau khi sửa; chibi (`ke-hoach/chibi/`) không dùng cho lt1 nữa.
- **Ảnh vẽ phải chi tiết (chủ kênh yêu cầu 30/10/2026, áp dụng mọi ảnh phẳng từ nay):** luôn vẽ ở mức chi tiết cao (`flat.DETAIL = True`; `ve.py` đã bật sẵn qua `chitiet.py`): mắt và mí, nếp áo, hoa văn, giáp vảy, nền nhiều lớp, đồ vật có viền rõ. Không giao ảnh nhân vật đơn giản trơn. Cảnh nào cần thêm chi tiết riêng (sàn, bình phong, ván thuyền) thì viết bản riêng trong `chitiet.py` (`SCN`). Sau khi vẽ vẫn soi ảnh cỡ lớn và sửa lỗi trước khi báo xong.
