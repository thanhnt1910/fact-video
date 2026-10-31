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
| Vẽ ảnh minh họa bằng FLUX (Cloudflare klein, Kaggle) | `quy-tac/anh/master-style.md` + Period Bible của thời kỳ (`quy-tac/anh/period-<tên>.md`, hiện có `period-ly-tong.md` DRAFT) + `quy-tac/anh/khoi-prompt.json` + `quy-tac/anh/quy-trinh-anh.md` (lưu `detail_tags`, duyệt Scene Planner, phiên bản; kiểm bằng `phim_ban_do/kiem_scene_planner.py`) |

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
- Dự án Lý Thường Kiệt v4 (`ke-hoach/thu-giong-hai/lt1v4_full.json`) chuyển hẳn sang phong cách **tranh bán hiện thực** theo Master Style, vẽ bằng **FLUX.2 klein trên Cloudflare Workers AI** (khóa API miễn phí, không Worker/D1/R2). Quy chuẩn nằm ở `quy-tac/anh/` (xem bảng đầu file): `master-style.md`, `period-ly-tong.md`, `khoi-prompt.json`, `quy-trinh-anh.md`. Các tài liệu này đang **DRAFT**, chờ chủ kênh duyệt, chưa APPROVED.
- Ba mức bằng chứng giữ riêng: A `historical_evidence`, B `cautious_reconstruction`, C `artistic_choice`.
- **Chưa áp dụng cho dự án khác.** Series khác (Tam Quốc, Nguyên Mông, Hồ Quý Ly...) giữ quy tắc ảnh riêng của series đó cho tới khi chủ kênh duyệt riêng việc áp dụng.
- Hai mục dưới đây (chibi lt1 và ảnh phẳng lt1) được giữ nguyên làm lịch sử, KHÔNG xóa, và **DEPRECATED cho lt1 v4**.

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
