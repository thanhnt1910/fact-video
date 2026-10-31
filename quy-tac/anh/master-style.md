# MASTER STYLE – hệ thống hình ảnh tư liệu lịch sử (v1.3 APPROVED, 01/11/2026)

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
- Ba mức bằng chứng giữ riêng, không gộp: A `historical_evidence`, B `cautious_reconstruction`, C `artistic_choice` định nghĩa trong Period Bible mục B. Chi tiết mức B và C phải mang nhãn trong `detail_tags` của cảnh; chi tiết mức C không được trình bày như sự thật lịch sử và không thành đặc điểm cố định của cả đội quân.
- Không trộn trang phục giữa các triều đại. Không đồ hiện đại.

## 5. Cách viết "điều cấm" cho FLUX
Klein và schnell trên Cloudflare KHÔNG có ô negative prompt, và câu "no X" đôi khi làm model nhớ tới X. Vì vậy: ưu tiên mô tả điều CẦN có ("brown leather armor, bare heads, topknot") thay vì liệt kê điều cấm. Chỉ giữ "no text, no modern items" trong khối giải phẫu. Danh sách cấm đầy đủ (chibi, cartoon, anime, giáp fantasy, tỷ lệ siêu nhân, thiết bị quân sự hiện đại, vật liệu nhựa, giải phẫu méo, thừa chi, khuôn mặt nhân đôi, đồ vật lơ lửng, vũ khí vô lý, phụ kiện hiện đại, chữ, logo) dùng làm TIÊU CHÍ KIỂM ẢNH, không dán vào prompt.

## 6. Kiểm ảnh (8 mục, mỗi ảnh phải báo)
1. Đúng bối cảnh lịch sử? 2. Đúng quân phục từng phe? 3. Có đồ hiện đại? 4. Có tự thêm cờ hoặc đạo cụ? 5. Đúng số người, số ngựa? 6. Lỗi tay chân, ngựa, cơ thể? 7. Đúng phong cách tranh bán hiện thực? 8. Mọi chi tiết nhìn thấy có nằm trong `detail_tags` của cảnh không (mũ, giáp, giày, cờ, đạo cụ)?
Trạng thái: PASS / REVIEW / REGENERATE / MANUAL_REVIEW. Không báo PASS chỉ vì ảnh đẹp. Chỉ vẽ lại ảnh REGENERATE (hạn mức Cloudflare miễn phí có hạn).
**Giới hạn vẽ lại:** tối đa 3 lần vẽ lại tự động sau lần vẽ đầu. Vẫn không đạt thì chuyển `MANUAL_REVIEW` cho chủ kênh. **Không được đổi nội dung lịch sử, nhãn bằng chứng hoặc tiêu chuẩn hình ảnh để ép cảnh đạt PASS**; chỉ được sửa cách viết bố cục, số lượng, góc máy trong phạm vi Bible.
**Kiểm số người và ngựa:** do người đếm bằng mắt (chưa có hệ thống đếm tự động); kết quả ghi vào bản ghi ảnh.
**Ảnh vẽ trước khi có Bible hiện hành** (ví dụ các ảnh thử 31/10 và các lượt Kaggle cũ) không được dùng làm căn cứ duyệt ảnh tham chiếu hay đánh giá chất lượng theo quy chuẩn mới.

## 7. Nguyên tắc KHÔNG TỰ SUY DIỄN chi tiết lịch sử (bắt buộc, chủ kênh 01/11/2026)
1. Mỗi chi tiết nhìn thấy trong ảnh (mũ, giáp, giày, cờ, vũ khí, kiến trúc, đồ vật, ánh sáng) phải truy được tới một khối trong `khoi-prompt.json` hoặc một dòng trong Period Bible. Không truy được thì không đưa vào prompt.
2. Chi tiết chưa có trong Bible: không tự thêm. Dùng thiết kế trung tính và gắn `artistic_choice`, hoặc hỏi chủ kênh trước.
3. Kịch bản không nói thì không thêm (số quân, binh chủng, vũ khí, phe thắng thua, thời tiết có ý nghĩa).
4. Mọi chi tiết chưa được xác nhận phải được phân loại đúng một trong hai nhãn `cautious_reconstruction` (B) hoặc `artistic_choice` (C), không để "không nhãn". Chi tiết có bằng chứng trực tiếp mang `historical_evidence` (A). Mỗi chi tiết giữ nguyên mức gốc (`evidence_level`), không gộp và không tự nâng mức: chưa xác nhận được A thì ghi B.
5. Model có thể tự thêm chi tiết mà prompt không yêu cầu (cờ, mũ, chữ). Chi tiết nhìn thấy trong ảnh mà không có trong `detail_tags` thì ảnh bị REVIEW (hoặc REGENERATE nếu là đồ sai thời).
6. Nhãn không bao giờ biến một chi tiết thành "đặc điểm cố định của đội quân": mỗi cảnh chọn theo nhóm người, thay đổi giữa các cảnh khi hợp lý.
7. Ảnh đẹp không phải bằng chứng. Không báo PASS chỉ vì ảnh đẹp.

## 8. Ảnh tham chiếu của FLUX.2 klein (Cloudflare)
**Cách gọi (đã dùng thực tế 01/11/2026):** gửi multipart với các trường `input_image_0`, `input_image_1`; ảnh tham chiếu thu nhỏ cạnh dài tối đa 768 px; đã thử tối đa 2 ảnh. Đây là quan sát thực nghiệm, chưa đối chiếu tài liệu chính thức của Cloudflare.

**Nguy cơ sao chép bố cục (đã quan sát):** ảnh tham chiếu giữ được quân phục và nét vẽ nhưng klein cũng chép luôn bố cục. Với 3/3 cảnh ngoài trời rộng có hàng người (19902, 19903, 19904 lần 1, tham chiếu 19901 là cảnh hành quân), cả ba ra bố cục "hàng lính hành quân" giống ảnh tham chiếu và bỏ yêu cầu riêng của cảnh (3 kỵ binh, hai bờ sông, dốc đất). Với 2/2 cảnh khác loại hẳn (nội thất 19905, đêm bên sông 19906) bố cục theo prompt. Mẫu nhỏ, chưa kết luận chắc.

**Quy tắc sử dụng:**
1. Mặc định KHÔNG dùng ảnh tham chiếu. Chỉ dùng khi cần giữ khuôn mặt nhân vật (sau khi có Character Reference được duyệt) hoặc trang phục lặp lại ở nhiều cảnh.
2. Trước khi dùng cho một loại cảnh mới, vẽ thử hai bản (có và không có tham chiếu) và so bố cục. Ghi kết quả vào sổ ảnh.
3. Mỗi lần dùng phải khai rõ mục đích: `face_only`, `costume_only` hoặc `style_only`, và viết trong prompt bố cục mới bằng chữ viết hoa (số người, vị trí, hành động). Không dùng ảnh tham chiếu có bố cục gần với cảnh đích.
4. Chỉ dùng ảnh tham chiếu đã duyệt VÀ còn hợp lệ với phiên bản Bible hiện hành. Ảnh tạo theo phiên bản cũ (trạng thái STALE) hoặc ảnh lỗi không được làm tham chiếu.
5. Tối đa 2 ảnh tham chiếu mỗi lần. Ghi mã ảnh tham chiếu, mục đích và phiên bản vào bản ghi ảnh.
6. Chỉ ảnh có trong `ke-hoach/anh/<mã>/tham-chieu-duoc-duyet.json` (chủ kênh duyệt) mới được dùng; bộ kiểm và script vẽ chặn ảnh khác bằng mã.
7. **Ảnh 19901 KHÔNG còn là ảnh tham chiếu hợp lệ**: nó PASS theo Bible v1.0 nhưng vi phạm v1.1 (cả đội đội nón lá, giáp da nâu, cờ nâu đỏ). Chưa có ảnh tham chiếu nào được duyệt theo v1.1.

Trạng thái bản này: **APPROVED** (v1.3, 01/11/2026, theo chỉ thị của chủ kênh sau kiểm cuối). Lịch sử phiên bản ở `quy-tac/anh/CHANGELOG.md`.
