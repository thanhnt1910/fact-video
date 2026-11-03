# Quy trình dựng video Góc IoT (từ ý tưởng đến Telegram)

Tài liệu này mô tả đúng cách đang làm video "Điều gì xảy ra nếu…" của kênh Góc IoT (nhân vật Bóng, video dọc 1080×1920). Mỗi bước ghi rõ: làm gì, file nào, chạy lệnh gì, kiểm cái gì.

Cập nhật: 3/11/2026. Nhánh làm việc: `goc-iot-video-1-6`.

---

## 1. Nhìn tổng thể

```
Chọn chủ đề → Kiểm chứng nguồn → Duyệt chủ đề với chủ kênh
      ↓
Viết kịch bản 9 cảnh  (kich-ban.json + mo-ta.json)
      ↓
Đọc giọng bằng Gemini  (GitHub Actions, tao_giong.py)  →  giong/vN_sK.wav
      ↓
Vẽ cảnh minh họa chuyển động  (minh_hoa.cjs + dung_hinh.cjs)
      ↓
Xem thử khung hình ở cỡ lớn  →  sửa bố cục
      ↓
Dựng video  (ghep_giong.py: giọng + hình + tiếng động)  →  video-N-giong.mp4
      ↓
Làm ảnh bìa  (tao_bia.cjs)  →  bia/bia-N.jpg
      ↓
Đẩy lên nhánh + đổi gui-telegram.txt  →  workflow gửi video + bìa vào Telegram
      ↓
Gửi file cho chủ kênh xem, ghi chú còn gì cần nghe lại
```

Nguyên tắc chạy: chủ kênh duyệt chủ đề trước, chỉ chạy workflow khi chủ kênh yêu cầu, mỗi video xong là gửi Telegram ngay.

---

## 2. Bản đồ file

| File | Vai trò |
|---|---|
| `goc-iot/kich-ban.json` | Kịch bản: giọng đọc, bảng phát âm, danh sách video và 9 câu lời kể của mỗi video |
| `goc-iot/mo-ta.json` | Tiêu đề, mô tả có nguồn, hashtag của từng video (dùng làm chú thích Telegram) |
| `goc-iot/tao_giong.py` | Đọc từng cảnh bằng Gemini, ghi `giong/vN_sK.wav` và `giong/thoi-luong.json` |
| `goc-iot/giong/` | File giọng đọc từng cảnh và bảng thời lượng |
| `goc-iot/dung_hinh.cjs` | Bộ dựng hình: vẽ từng khung (SVG → PNG), Bóng, phụ đề, bố cục, danh sách tiếng động |
| `goc-iot/minh_hoa.cjs` | Các cảnh minh họa chuyển động riêng cho từng video |
| `goc-iot/ghep_giong.py` | Ghép giọng + hình + tiếng động thành mp4 |
| `goc-iot/sfx_video.py`, `audio_fx.py` | Tiếng động tự tổng hợp (không dính bản quyền) |
| `goc-iot/tao_bia.cjs` | Tạo ảnh bìa từ một khung hình |
| `goc-iot/video/` | Video chờ gửi Telegram (chỉ để video cần gửi) |
| `goc-iot/bia/` | Ảnh bìa `bia-<số>.jpg` |
| `goc-iot/chay-giong.txt` | Đổi nội dung file này và đẩy lên → chạy workflow đọc giọng |
| `goc-iot/gui-telegram.txt` | Đổi nội dung file này và đẩy lên → chạy workflow gửi Telegram |
| `.github/workflows/goc-iot-giong.yml` | Workflow đọc giọng |
| `.github/workflows/goc-iot-telegram.yml` | Workflow gửi video + bìa vào Telegram |

---

## 3. Từng bước chi tiết

### Bước 1. Chọn chủ đề và kiểm chứng

- Dạng chủ đề: "Điều gì xảy ra nếu…" hoặc "Bạn có biết…". Mở bằng câu hỏi, trả lời bằng cơ chế, kết bằng việc làm được ngay.
- Phải neo vào một sự việc có thật, có nguồn (thông cáo cơ quan quản lý, bài báo công nghệ, bài nghiên cứu). Đọc nguồn gốc, ghi lại số liệu và ngày tháng.
- Chỗ nào nguồn không thống nhất (ví dụ khoảng cách khác nhau giữa hai bài) thì chọn số có nguồn chính thức hơn, hoặc nói rõ "theo…" trong lời kể.
- Chỗ chưa kiểm được thì bỏ khỏi lời kể.
- **Gửi chủ đề cho chủ kênh duyệt trước khi viết và chạy gì.** Danh sách đề xuất kèm: câu sai, sự việc có thật, nguồn đã đọc, chỗ cần kiểm thêm.

### Bước 2. Viết kịch bản (`kich-ban.json`)

Mỗi video có đúng **9 cảnh**:

| Cảnh | Nội dung |
|---|---|
| 1 | Câu hỏi mở "Điều gì xảy ra nếu…?" (Bóng lớn ở giữa) |
| 2 | **Câu trả lời sai** mà nhiều người dễ nghĩ ("Bạn có thể nghĩ…") |
| 3 | **Sửa lại cho đúng** ("Không phải vậy…"), giải thích cơ chế |
| 4–7 | Sự việc có thật, theo thứ tự thời gian hoặc nguyên nhân – kết quả |
| 8 | "Bạn làm được gì?" với ba việc cụ thể |
| 9 | Câu hỏi cho người xem + "Bình luận cho Bóng biết nhé!" |

Quy tắc viết lời kể (vì lời được đọc lên và người nghe chỉ nghe một lần):
- Câu ngắn, từ đời thường. Mỗi cảnh khoảng 14–33 chữ.
- Số và năm viết bằng chữ: "năm hai nghìn không trăm mười bảy", "hai phẩy hai triệu đô la".
- Đơn vị Việt Nam (ki-lô-mét), không để dặm.
- Tên tổ chức nước ngoài giải thích ngay.
- **Mỗi video chỉ MỘT chỗ "sai rồi đúng"** (cảnh 2 và 3). Không thêm chỗ thứ hai.
- Phần nghi vấn nói "theo…" hoặc "có vẻ", không khẳng định.
- Chuyện còn tranh cãi hoặc là truyền thuyết thì không đưa vào.

Bảng phát âm: trường `phat_am` trong `kich-ban.json` đổi chữ viết sang chữ đọc, ví dụ `"TV": "ti vi"`, `"Strava": "Xtra-va"`, `"Jeep": "Díp"`. Tên nước ngoài, từ viết tắt, tên riêng đều phải thêm vào đây trước khi đọc giọng. Chỉ ảnh hưởng giọng, không đổi chữ trên màn hình.

Mô tả và hashtag: thêm mục trong `mo-ta.json` với `id`, `tieu_de`, `mo_ta` (tóm tắt sự việc, việc làm được, **dòng "Nguồn:"**, câu hỏi cuối), `hashtag`.

### Bước 3. Đọc giọng (GitHub Actions)

Lệnh kích hoạt:
1. Đặt biến `GOC_IOT_VIDEOS` trong `.github/workflows/goc-iot-giong.yml` thành danh sách video cần đọc, ví dụ `"12 13 14"`.
2. Đổi nội dung `goc-iot/chay-giong.txt`, commit và đẩy lên nhánh.

Việc workflow làm (`tao_giong.py`):
- Đọc từng cảnh một bằng Gemini (giọng "Puck", phong cách Bóng: vui, tinh nghịch, chậm và nhẹ khi nói về rủi ro).
- Đổi số, năm thành chữ và áp bảng phát âm trước khi gửi cho giọng đọc.
- Đo tốc độ đọc (từ/giây). Chấp nhận 1,8–3,6 từ/giây, ngoài khoảng này thì đọc lại, tối đa 3 lần, giữ lần gần mức bình thường nhất.
- Cảnh nào đã có file giọng và chữ không đổi thì bỏ qua. Sửa lời một cảnh thì chỉ cảnh đó đọc lại, nên **chỉnh kịch bản xong mới đẩy `chay-giong.txt`**.
- Ghi `goc-iot/giong/vN_sK.wav`, `thoi-luong.json` và log `goc-iot/logs/giong.txt`; bot tự commit "giọng đọc … [skip ci]".

Việc cần kiểm sau khi giọng xong:
- Đọc cuối log: dòng "Cảnh tốc độ lạ (cần nghe lại)" liệt kê cảnh đọc quá nhanh hoặc quá chậm, phải nghe lại các cảnh đó.
- Giọng bị bỏ câu hoặc đọc sai thì đổi chữ nhẹ ở câu đó rồi đọc lại.

Giới hạn đã gặp:
- Gemini giới hạn số lượt gọi mỗi khóa. Khi báo `429` ở mọi khóa thì hết lượt, phải đợi hồi hạn mức hoặc đổi nguồn giọng. Không đợi quá lâu trong workflow.
- **Cloudflare Workers AI không dùng được cho tiếng Việt.** Đã thử 29/10/2026: MeloTTS chỉ hỗ trợ `en, es, fr, jp, kr, zh`, tiếng Việt báo lỗi "Unsupported language 'vi'". Kết quả thử: `goc-iot/logs/cf_tts.txt`.
- Các hướng thay thế đang chờ chủ kênh chọn: giọng Microsoft (edge-tts), đợi Gemini hồi hạn mức, hoặc Google Cloud Text-to-Speech.

### Bước 4. Vẽ cảnh minh họa

Bộ dựng (`dung_hinh.cjs`) vẽ mỗi khung hình bằng SVG rồi đổi sang PNG (1080×1920, 24 khung/giây).

Mỗi video là một danh sách cảnh trong `DEFS` (cuối file `dung_hinh.cjs`):

```js
12: [Q('Điều gì xảy ra nếu', 'TV thông minh ghi lại bạn xem gì?'),
     ...MH.v12.map((x) => D(x)),
     E],
```

- `Q(...)`: cảnh mở đầu có tiêu đề, Bóng lớn ở giữa.
- `D(...)`: cảnh minh họa riêng, định nghĩa trong `minh_hoa.cjs` (7 cảnh cho cảnh 2–8).
- `E`: cảnh kết, Bóng lớn.

Mỗi cảnh minh họa trong `minh_hoa.cjs` có dạng:

```js
{
  w: [['tv', 'TV'], ['xem', 'xem']],        // từ neo theo THỨ TỰ lời kể
  point: [['tv', 540, 700]],                // chỗ Bóng chỉ tay tới
  draw(l, t) { ... }                        // l = giây trong cảnh, t.tv = giây từ neo xuất hiện
}
```

- **Từ neo** quyết định hình nào hiện đúng lúc người dẫn nhắc tới từ đó. Phải xếp đúng thứ tự trong câu, không thì báo lỗi "không thấy từ …". Từ neo ngắn dễ khớp nhầm đầu từ khác (ví dụ `ba` khớp `bay`), nên chọn từ dài và độc nhất.
- Các hàm dựng sẵn: `pop` (hiện ra có nảy), `myth` (bong bóng câu sai, bị gạch đỏ kèm nhãn SAI khi lời kể sửa), `tag` (nhãn viên thuốc), `cal` (tờ lịch), `check`/`cross` (dấu đúng/sai), `toggle` (công tắc), `panel`, `photo`…
- Phải có chuyển động thật: sóng lan, gói dữ liệu chạy, bộ đếm tăng, thanh tiến độ, công tắc gạt. Không để chỉ là icon đứng yên.

Bố cục cố định:
- Nội dung chính nằm giữa khung hình (khoảng y từ 430 đến 1100).
- Bóng nhỏ ở góc dưới, **đổi bên theo từng cảnh**, chỉ tay vào mục đang nói.
- Phụ đề ở dưới, từng chữ hiện đúng lúc được đọc tới.
- Nội dung không đè lên vùng Bóng và phụ đề.

Xem thử trước khi dựng thật (chưa cần giọng thật):

```bash
# thời lượng giả theo số chữ, rồi vẽ khung hình ở các giây chỉ định
TLFILE=<file thời lượng giả>.json AT=8,15,24 node goc-iot/dung_hinh.cjs <số video> <thư mục> at
```

Mở ảnh `at_<giây>.png` **ở cỡ lớn** (không xem ảnh thu nhỏ). Soi: chữ bị đè, nhãn chồng nhau, nhãn lòi ra mép, đồ vật lơ lửng sai chỗ, số đếm đúng khi đã chạy hết.

### Bước 5. Dựng video

Cần giọng đã xong ở bước 3.

```bash
python3 goc-iot/ghep_giong.py <số video> <thư mục làm việc>
```

`ghep_giong.py` làm lần lượt:
1. **Chuẩn hóa giọng từng cảnh.** Chỉnh tốc độ về mức trung vị của cả video (chỉ trong khoảng 0,93–1,07 lần, giữ nguyên cao độ), rồi chuẩn âm lượng -16 LUFS. Nhờ vậy giọng đều nhau giữa các cảnh.
2. **Tính giờ từng chữ cho phụ đề.** Dò chỗ nghỉ thật của giọng, chia câu theo chỗ nghỉ, trong câu chia theo độ dài chữ. Kết quả cho phụ đề hiện sát giọng.
3. **Ghép giọng.** Mỗi cảnh trễ 0,25 giây ở đầu và đệm thêm 0,7 giây ở cuối. Độ dài mỗi cảnh trong hình = thời lượng giọng thật + 0,7 giây.
4. **Dựng hình theo thời lượng thật.** Gọi `dung_hinh.cjs` ở chế độ `full` để xuất từng khung PNG.
5. **Nén hình.** `ffmpeg`, `libx264`, `-preset veryfast`, `-crf 20`, 24 khung/giây.
6. **Tiếng động.** Bộ dựng ghi danh sách hiệu ứng theo mốc (`events.json`), `audio_fx` tự tổng hợp âm, rồi trộn nhỏ hơn giọng (âm lượng mặc định 0,35).
7. **Trộn** giọng + tiếng động, giới hạn đỉnh, ghép vào hình, âm thanh AAC 160 kb/s.
8. **Xuất** `video-<số>-giong.mp4`, xóa các khung PNG tạm.

Cần kiểm sau khi dựng:
- Đo độ dài (khoảng 70–90 giây) và âm lượng (-16 LUFS).
- Xem các khung ở đầu, giữa, cảnh có nhiều hình nhất và cảnh cuối.
- Cảnh nào giọng bị đánh dấu "tốc độ lạ" thì nghe lại.

### Bước 6. Làm ảnh bìa

Mỗi video phải có thêm ảnh bìa dọc 1080×1920.

```bash
# 1. lấy khung cảnh mở đầu có Bóng lớn (khoảng giây 3,5)
TLFILE=goc-iot/giong/thoi-luong.json AT=3.5 node goc-iot/dung_hinh.cjs <số> <thư mục> at

# 2. đặt thanh chữ gây tò mò và nhãn "Góc IoT"
node goc-iot/tao_bia.cjs <thư mục>/at_3.5.png goc-iot/bia/bia-<số>.jpg "<dòng gây tò mò>" "<dòng phụ>"
```

Xem ảnh bìa ở cỡ lớn rồi mới giao. Bìa video 11 là mẫu: `goc-iot/bia/bia-11.jpg`.

### Bước 7. Gửi Telegram

1. Đặt video: `goc-iot/video/video-<số>-<tên>.mp4`. **Chỉ để trong thư mục này video cần gửi.** Xóa file video cũ (`git rm`) để workflow không gửi lại.
2. Đặt bìa: `goc-iot/bia/bia-<số>.jpg`.
3. Đảm bảo `mo-ta.json` có mục cho video này.
4. Đổi nội dung `goc-iot/gui-telegram.txt`, commit và đẩy lên nhánh.

Workflow `goc-iot-telegram.yml` gửi mỗi video trong `goc-iot/video/` kèm chú thích: tiêu đề, mô tả có nguồn, hashtag. Ngay sau đó gửi ảnh bìa `bia-<số>` tương ứng.

Sau cùng gửi file cho chủ kênh xem trong cuộc trò chuyện, nói ngắn: video là gì, đã thay đổi gì, còn chỗ nào chưa kiểm.

### Bước 8. Git

- Mọi commit dùng `user.email noreply@anthropic.com`, `user.name Claude`, và kèm dòng đồng tác giả theo hướng dẫn của phiên.
- Đẩy lên nhánh `goc-iot-video-1-6`, không đẩy lên `main` khi chủ kênh chưa yêu cầu.
- Trước khi đẩy: `git pull --rebase -q origin goc-iot-video-1-6` vì bot cũng commit lên nhánh.
- Commit tự động của workflow bị GitHub gắn "Unverified" (thiếu chữ ký của bot). Việc này không ảnh hưởng video. Không sửa lịch sử bằng đẩy ép, vì có thể kích hoạt lại workflow.

---

## 4. Danh sách kiểm trước khi gửi

- [ ] Chủ đề đã được chủ kênh duyệt, nguồn đã đọc, số liệu khớp nguồn.
- [ ] Mỗi video 9 cảnh, đúng một chỗ "sai rồi đúng".
- [ ] Số và năm viết bằng chữ, không dặm, tên nước ngoài đã vào `phat_am`.
- [ ] `mo-ta.json` có tiêu đề, mô tả có dòng "Nguồn:", hashtag.
- [ ] Giọng đọc xong, đã nghe lại các cảnh "tốc độ lạ".
- [ ] Mỗi cảnh có chuyển động thật, không chỉ icon đứng yên.
- [ ] Đã xem khung hình cỡ lớn: không chữ đè nhau, không đè Bóng và phụ đề.
- [ ] Độ dài 70–90 giây, âm lượng khoảng -16 LUFS.
- [ ] Có ảnh bìa, đã xem cỡ lớn.
- [ ] Thư mục `goc-iot/video/` chỉ có video cần gửi, `gui-telegram.txt` đã đổi.
- [ ] Đã gửi file cho chủ kênh.

---

## 5. Lỗi hay gặp

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| Lỗi "không thấy từ …" khi vẽ | Từ neo không có trong câu, hoặc sai thứ tự | Sửa `w` cho đúng thứ tự trong lời kể |
| Hình hiện sai lúc | Từ neo khớp nhầm đầu của từ khác | Dùng từ neo dài, độc nhất |
| Phụ đề lệch giọng | Dùng thời lượng giả thay vì giọng thật | Dựng bằng `ghep_giong.py` sau khi giọng chốt |
| Giọng đọc chậm hoặc nhanh bất thường | Gemini đọc lệch | Xem dòng "tốc độ lạ" trong log, đọc lại cảnh đó |
| Mọi khóa Gemini báo 429 | Hết hạn mức | Đợi hồi, hoặc chọn nguồn giọng khác (xem bước 3) |
| Workflow Telegram gửi lại video cũ | Video cũ còn trong `goc-iot/video/` | `git rm` các file cũ trước khi đẩy |
| Nhãn chồng nhau, lòi mép | Vị trí trong `draw()` | Xem khung hình cỡ lớn, dời nhãn |
| Cảnh đọc lại tốn hạn mức | Sửa lời sau khi đã đọc | Chốt kịch bản trước khi đẩy `chay-giong.txt` |

---

## 6. Tình trạng hiện tại (3/11/2026)

| Video | Chủ đề | Trạng thái |
|---|---|---|
| 8, 9, 10 | Máy chủ đám mây sập; camera bị chiếm; pin sạc sai | Đã gửi, dùng bố cục cũ (hàng icon), chưa có ảnh bìa |
| 11 | Robot hút bụi chụp ảnh | Đã gửi cùng ảnh bìa, là mẫu cho định dạng mới |
| 12 | TV thông minh ghi lại bạn xem gì (Vizio, FTC 2017) | Kịch bản và cảnh minh họa xong, **chờ giọng đọc** |
| 13 | Đồng hồ chạy bộ lộ đường chạy (Strava, 2017–2018) | Kịch bản và cảnh minh họa xong, **chờ giọng đọc** |
| 14 | Xe bị điều khiển từ xa (Jeep Cherokee, 2015) | Kịch bản và cảnh minh họa xong, **chờ giọng đọc** |

Việc tiếp theo: chủ kênh chọn nguồn giọng thay thế (hoặc đợi Gemini hồi hạn mức) → đọc giọng 12–14 → dựng → làm bìa → gửi Telegram từng video.
