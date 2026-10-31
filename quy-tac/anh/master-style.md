# MASTER STYLE – hệ thống hình ảnh tư liệu lịch sử (v1.0 DRAFT, 01/11/2026)

Dùng chung cho mọi video của kênh. Không đổi theo video. Đổi bản phải tăng version và có chủ kênh đồng ý.

## 1. Khối kiểu vẽ CỐ ĐỊNH (chép nguyên vào cuối mọi prompt, không sửa chữ)
`Cinematic historical illustration, semi-realistic traditional historical painting, epic documentary look, natural dramatic lighting, atmospheric depth, subtle painterly texture, 16:9.`

Lý do giữ cố định: lần thử 31/10 cho thấy khóa nguyên chữ kiểu vẽ giữ được một ngôn ngữ hội họa xuyên suốt. Bảng màu KHÔNG nằm trong khối này mà do Period Bible quyết định (quân phục, kiến trúc), ánh sáng và thời tiết theo cảnh.

## 2. Khối giải phẫu (thêm vào mọi cảnh có người nhìn rõ)
`Every person has one head, two arms, two legs, natural anatomy, clear separate silhouettes, no overlapping limbs, no fused bodies, no text.`
Cảnh có ngựa thêm: `EXACTLY N horses with N riders, each rider upright on exactly one horse, each horse four natural legs, clearly separated from the others.`

## 3. Quy tắc bố cục
- Một chủ thể, một hành động chính mỗi cảnh. Nêu số người và số ngựa ngay đầu prompt, rồi vị trí các nhóm.
- Tiền cảnh 1–3 người chi tiết; trung cảnh nhóm 3–5 người; hậu cảnh nhỏ, ít chi tiết.
- Mô tả bố cục bằng chữ viết HOA ở chỗ model hay làm sai (EXACTLY, LEFT bank only, RIGHT bank only).
- Bản đồ, địa danh, đường biên: không dùng FLUX (dùng bản đồ vector của kênh).

## 4. Quy tắc lịch sử (bắt buộc)
- Không dùng phong cách chung để thay độ chính xác. Trang phục, kiến trúc, vũ khí, cờ lấy từ Period Bible, chi tiết nào chưa có trong đó thì không tự thêm.
- Chi tiết mức C (không đủ bằng chứng) chỉ dùng dạng trung tính và phải ghi "phục dựng nghệ thuật" trong ghi chú cảnh, không khẳng định là sự thật.
- Không trộn trang phục giữa các triều đại. Không đồ hiện đại.

## 5. Cách viết "điều cấm" cho FLUX
Klein và schnell trên Cloudflare KHÔNG có ô negative prompt, và câu "no X" đôi khi làm model nhớ tới X. Vì vậy: ưu tiên mô tả điều CẦN có ("brown leather armor, bare heads, topknot") thay vì liệt kê điều cấm. Chỉ giữ "no text, no modern items" trong khối giải phẫu. Danh sách cấm đầy đủ (chibi, cartoon, anime, giáp fantasy, tỷ lệ siêu nhân, thiết bị quân sự hiện đại, vật liệu nhựa, giải phẫu méo, thừa chi, khuôn mặt nhân đôi, đồ vật lơ lửng, vũ khí vô lý, phụ kiện hiện đại, chữ, logo) dùng làm TIÊU CHÍ KIỂM ẢNH, không dán vào prompt.

## 6. Kiểm ảnh (7 mục, mỗi ảnh phải báo)
1. Đúng bối cảnh lịch sử? 2. Đúng quân phục từng phe? 3. Có đồ hiện đại? 4. Có tự thêm cờ hoặc đạo cụ? 5. Đúng số người, số ngựa? 6. Lỗi tay chân, ngựa, cơ thể? 7. Đúng phong cách tranh bán hiện thực?
Trạng thái: PASS / REVIEW / REGENERATE. Không báo PASS chỉ vì ảnh đẹp. Chỉ vẽ lại ảnh REGENERATE (hạn mức Cloudflare miễn phí có hạn).

## 7. Ảnh tham chiếu (klein nhận `input_image_N`)
Thử 01/11/2026: ảnh tham chiếu giữ được quân phục và nét vẽ nhưng CHÉP LUÔN bố cục. Dùng cho cảnh khác bố cục thì phải ghi mạnh bố cục mới, hoặc không dùng tham chiếu. Không dùng ảnh lỗi làm tham chiếu. Ảnh tham chiếu đã duyệt: 19901 (quân Đại Việt hành quân, PASS).

Trạng thái bản này: DRAFT, chờ chủ kênh duyệt.
