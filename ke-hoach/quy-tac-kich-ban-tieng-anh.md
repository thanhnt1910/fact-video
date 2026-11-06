# Quy tắc kiểm chứng và viết kịch bản kênh tiếng Anh (History Mysteries Daily)

Chủ kênh yêu cầu ghi chi tiết ngày 04/11/2026, rút ra từ lần tự đánh giá kịch bản Roanoke (RN1): bản đầu có 5 lỗi mà lần soát đầu không bắt được. Áp dụng cho mọi kịch bản tiếng Anh sau. Cùng đọc với mục "Kịch bản phải tự kiểm trước khi gửi chủ kênh" trong `CLAUDE.md`.

## A. Kiểm chứng (tự làm trước khi gửi, không đẩy cho chủ kênh)
1. **Đối chiếu từng câu với văn bản gốc, không chỉ với Wikipedia.** Chuyện có tài liệu gốc (Hakluyt, biên niên sử, thư từ…) phải mở và đọc đúng đoạn của cảnh chính, rồi so từng câu của lời kể với văn bản. Nhãn SỬ chỉ dùng khi đã làm vậy (ghi tên nguồn và đường dẫn).
2. **Rà sự kiện bị bỏ sót.** Đọc nguyên đoạn nguồn quanh mỗi cảnh then chốt, liệt kê MỌI biến cố (người chết, bão, tai nạn, tranh cãi), rồi quyết định đưa vào hay bỏ. Biến cố nào giải thích nguyên nhân – kết quả của cảnh sau thì phải đưa vào. (RN1 sót: thuyền Spicer lật, bảy người chết, ngày 17/8/1590.)
3. **Câu phủ định tuyệt đối cần nguồn thứ hai.** "Nothing more was heard", "never seen again", "no one ever" chỉ được viết khi hai nguồn độc lập cùng nói; còn lại dùng "no confirmed sighting", "is not known to have". (RN1 sai ở câu mười lăm người của Grenville: có nguồn nói tìm thấy xương.)
4. **Chi tiết chỉ có một nguồn** (nhất là chỉ Wikipedia): gắn nhãn TC và mở câu bằng "According to …", hoặc bỏ khỏi lời kể.
5. **Con số dao động** (số người, số quân, số tàu): lời kể dùng "more than", "about", "most counts"; ghi dải số trong mục kiểm chứng. **Tiêu đề, ảnh bìa, mô tả KHÔNG ghi con số chính xác khi nguồn không thống nhất**; dùng "100+", "More than 100". Các câu trong cùng video không được lệch nhau (quét mọi số trong json trước khi gửi).
6. **Cấm mốc thời gian tương đối** ("a few years ago", "recently", "today") trong lời kể: ghi năm cụ thể. Video đăng nhiều năm sau, chữ "recently" sẽ sai.
7. **Từ chắc chắn ("certain", "proves", "always", "never")** chỉ cho điều có tài liệu. Giả thuyết dùng "may", "suggests", "unproven".
8. **Không suy diễn tâm trạng hay cách hành động** mà nguồn không nói ("calmly", "hoped", "feared"). Lời thoại và nội tâm không bịa.
9. Sau khi sửa: ghi vào mục "Sửa ngày …" của file kịch bản (câu nào, vì sao, nguồn nào). Bản gửi nêu rõ số câu đã đối chiếu nguyên văn, số câu hạ nhãn hoặc bỏ.

## B. Viết cho giọng đọc tiếng Anh
- Năm viết thành chữ ("fifteen eighty-seven"), số ngày thành chữ ("August eighteenth"). Từ khó đọc (CROATOAN) có hướng dẫn phát âm trong STYLE của `en_video.py`.
- Mỗi câu một ý, một hoặc hai câu mỗi beat. Chương 7–10 beat; tổng 70–90 beat; 1.800–2.100 từ (khoảng 13–14 phút).
- Mở bằng cảnh gây tò mò là sự kiện có thật của chính video; kết bằng phân tách "chắc chắn / giả thuyết / bịa" và câu hỏi bình luận.
- Đơn vị Mỹ (dặm, feet) giữ nguyên trong lời đọc; bản Việt ghi thêm quy đổi.

## C. Quy trình sửa kịch bản đã có giọng
- Sửa lời đọc thì sửa đồng thời: `<tên>.json`, `vi.json`, `<tên>_song_ngu.md`, `<tên>_kich_ban.md` (bảng + mục "Sửa"), mô tả YouTube, ảnh bìa (nếu có số hoặc tên bị đổi).
- Thêm hoặc bớt một beat làm lệch cách chia cụm 8 beat theo chương, nên các cụm phía sau đổi chữ và phải đọc lại giọng. Báo chủ kênh số cụm phải đọc lại và hỏi trước khi chạy (tốn hạn mức Gemini). Hết mọi khóa thì dừng, không đợi.
- Chỉ chạy workflow khi chủ kênh yêu cầu; push chỉ chứa file kịch bản/tài liệu thì để `[skip ci]` trong tiêu đề commit.

## D. Ảnh: trộn ảnh tư liệu với tranh AI (chủ kênh chọn 04/11/2026, Cloudflare thay vì Kaggle)
- Cảnh làm bằng chứng (bản đồ, tranh khắc, ảnh khảo cổ, chân dung có thật) giữ ảnh tư liệu. Cảnh không có ảnh thời đó hoặc chỉ có ảnh hiện đại (bãi biển, khói, dấu chân, cây) vẽ bằng AI: khai báo trong `anh_ai.json` (ô → prompt), chạy `ve_anh_cf_en.py` (workflow `ve-anh-en.yml`, kích hoạt bằng `ke-hoach/<chủ đề>/ve_chay.txt`; `lam_lai=S01,S18` để vẽ lại).
- Tranh AI phải giữ phong cách sơn dầu, tối, bí ẩn; KHÔNG vẽ mặt người nhận ra được (người quay lưng, ở xa); không chữ. Cảnh vắng người ghi "completely empty, absolutely no people"; cảnh một người ghi "exactly ONE man only".
- Soi từng ảnh ở cỡ lớn trước khi dựng. Lỗi đã gặp: tháp đá / lâu đài châu Âu mọc vào cảnh lẽ ra là hàng rào gỗ (thay bằng "long wall of tall rough tree trunks"), nhà kiểu Anh có ống khói thay cho nhà thổ dân (thay bằng "dome-shaped houses made of bent saplings covered with bark mats"), núi ở vùng bờ biển phẳng (ghi "flat horizon, no mountains"), bóng ngựa mọc ở cảnh trống (ghi "no animals").
- Bắt buộc khai báo nhãn AI của YouTube và ghi vào mô tả: tranh AI không phải ảnh chụp sự kiện thật.
- Cloudflare: FLUX.1 schnell (`cheap=True`, khoảng 80 neurons mỗi ảnh) đủ cho phong cách này; hết mọi tài khoản thì dừng ngay.

## E. Bản đồ đánh dấu vị trí (chủ kênh yêu cầu 04/11/2026, áp dụng mọi video từ AN1)
- Câu nào nhắc tới một địa điểm (đảo, thành phố, nơi hạ cánh, kho lương, hướng đi) thì cảnh của câu đó là **bản đồ động**: máy quay phóng vào đúng chỗ, điểm đánh dấu đỏ có vòng sáng lan ra, nhãn tên mờ dần vào; hướng đi và hướng trôi vẽ bằng mũi tên chạy dần (nét đứt cho dự định hoặc dòng trôi).
- Khai báo trong `ke-hoach/<chủ đề>/ban_do.json`: mỗi cảnh `Mxx` có `khi` (đầu câu lời kể gắn bản đồ), `from`/`to` (tâm và bề ngang khung, km), `markers`, `arrows`, `lat_line`. Script dựng kịch bản tự gắn trường `map` vào câu; `en_video.py dung` dựng cảnh bản đồ bằng `ban_do_en.py` thay cho ảnh của câu đó.
- **Tọa độ phải có nguồn** (Wikipedia, GeoNames, bài nghiên cứu) và ghi ở trường `_nguon_toa_do`. Không vẽ lộ trình chính xác khi nguồn chỉ cho biết hướng: khi đó chỉ vẽ mũi tên chỉ hướng, không nối các điểm đoán.
- Nhãn trên bản đồ bằng tiếng Anh, ngắn, khớp lời kể (ngày tháng viết số được vì là chữ trên màn hình, không phải lời đọc).
- Điểm đánh dấu và nhãn không nằm trong 190 px dưới cùng (vùng phụ đề); tâm khung đặt ở 44% chiều cao. Trước khi dựng, xuất khung cuối từng cảnh để soi: `python ban_do_en.py anh ke-hoach/<chủ đề>/ban_do.json Mxx out.jpg`; thử nhanh vài cảnh có chuyển động: `python ban_do_en.py demo ke-hoach/<chủ đề>/ban_do.json Mxx,Myy out.mp4`.
- Dữ liệu bờ biển: Natural Earth 1:10m (phạm vi công cộng) đã cắt sẵn ở `assets/ban_do/bac_cuc_10m.json` (vùng từ 44 độ bắc trở lên). Video ở vùng khác thì cắt thêm từ bản Natural Earth trên GitHub (`nvkelso/natural-earth-vector`).

## F. Giọng đọc gốc (chủ kênh yêu cầu 07/11/2026, áp dụng kênh tiếng Anh từ AN1)
- Giọng Orus lấy nguyên bản Gemini trả về: không cân âm lượng (`loudnorm`), không chỉnh tốc độ (`atempo`). Bật bằng `"giong_goc": true` trong `<chủ đề>.json`. Quy tắc "chuẩn hóa ở bước âm thanh" trong CLAUDE.md không áp cho kênh này.

## G. Xem lại toàn bộ video sau khi dựng (chủ kênh yêu cầu 07/11/2026, áp dụng mọi video tiếng Anh)
- Dựng xong phải xem lại TOÀN BỘ video trước khi giao, không chỉ vài khung mẫu:
  1. Lặp chữ: nhận dạng lại giọng trong video (ASR) và đối chiếu từng câu với lời đọc; đầu câu đọc lại đuôi câu trước, cuối câu lẫn đầu câu sau, từ lặp liền nhau, thừa/mất chữ đều phải đọc lại câu đó. Nghe lại các chỗ nối câu nghi ngờ.
  2. Hình ảnh: trích khung hình dày (mỗi 2–3 giây và mọi chỗ đổi cảnh), xem ở cỡ lớn từng khung: chữ lạ, vật hiện đại, thừa tay/người, khung đen/đứng hình, nhãn bản đồ đè phụ đề hoặc đè nhau, ảnh không khớp lời kể.
  3. Ghi kết quả (số câu kiểm, lỗi tìm thấy, đã sửa gì) vào bản gửi chủ kênh. Có lỗi thì sửa và dựng lại, không giao.
