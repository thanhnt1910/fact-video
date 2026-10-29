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

## Ảnh chibi Lý Thường Kiệt: lỗi thời đại và cách tránh (chủ kênh phát hiện 30/10/2026)
- Lần vẽ đầu (lt1) có khoảng 34/64 ảnh sai: cờ sao vàng, lính mũ cối và súng, đường nhựa, cột điện, tàu hơi nước, bàn ghế, nến, đèn lồng giấy, chữ Hán trên cờ. Nguyên nhân: prompt chỉ ghi "plain red flags" và không có mốc thời Lý; bỏ LoRA nên mô hình trôi về kiểu phổ biến.
- Không dùng chữ "flag" / "red flag": viết "plain brown-red triangular cloth pennants". Mọi prompt (kể cả cảnh vắng người) phải có mốc "ancient Vietnam, Ly dynasty 11th century, grey tiled roofs and thatched houses" (hoặc Tống) và mô tả lính: áo giáp da nâu, nón tre, chân đất, giáo. Không dùng "chair, table, candle, lantern, ship" trơn: viết "woven mat, low wooden table, clay oil dish, wooden war boat with woven sails". Mã `ke-hoach/chibi/tao_lt1_chibi.py` đã gắn sẵn ERA_VN/ERA_SONG.
- Sau mỗi đợt vẽ phải xem ảnh cỡ lớn (6 ảnh một tấm) và soi cờ, quân phục, đồ vật hiện đại trước khi báo xong.
