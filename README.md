# 🏮 Bộ tạo video "Người Gác Sử"

Tự động biến **kịch bản JSON** thành **video dọc 1080×1920** có hình động, giọng đọc AI tiếng Việt, phụ đề, nhạc nền, kèm ảnh bìa và caption để đăng Facebook Reels, TikTok, YouTube Shorts.

---

## 1. Cài đặt (chỉ làm 1 lần)

1. **Cài Python 3.10 trở lên** tại https://www.python.org/downloads/
   Khi cài, **nhớ tick ô "Add python.exe to PATH"**.
2. Giải nén thư mục này ra ổ đĩa, ví dụ `D:\fact-video`.
3. Bấm đúp **`cai-dat.bat`** và chờ chạy xong (tải thư viện và trình duyệt Chromium, khoảng 150 MB).

Không cần cài ffmpeg riêng, bộ công cụ tự tải kèm.

---

## 2. Quy trình mỗi tuần

| Bước | Việc làm | Thời gian |
|---|---|---|
| 1 | Mở `PROMPT_KICH_BAN.md`, copy prompt, sửa danh sách hook theo lịch đăng tuần sau, dán vào chat Claude | 2 phút |
| 2 | Lưu từng JSON Claude trả về thành file trong thư mục `scripts\` (ví dụ `scripts\DV1.json`) | 3 phút |
| 3 | **Duyệt kịch bản**: đọc lời thoại, kiểm tra nguồn trong `sources` | 2–5 phút/video |
| 4 | Bấm đúp **`kiem-tra.bat`** để kiểm tra các file có hợp lệ không | 10 giây |
| 5 | Bấm đúp **`tao-video.bat`** → tự dựng **tất cả** video chưa làm | 2–4 phút/video |
| 6 | Xem lại video trong `output\<mã>\`, đăng kèm caption | 1–2 phút/video |

**Mẹo:** muốn xem nhanh 1 video trước khi dựng bản đẹp, **kéo thả file `.json` vào `xem-truoc.bat`**. Bản xem trước nhỏ hơn, dựng nhanh gấp khoảng 3 lần.

**Quy định thời lượng (chủ kênh đặt ngày 15/10/2026):** mọi **video dài YouTube phải dài tối thiểu 10 phút**, tức lời đọc từ khoảng **1.900 tiếng** trở lên (giọng Gemini đọc khoảng 3 tiếng/giây). Video dọc vẫn 60–80 giây. Quy định đầy đủ nằm ở mục "VIDEO DÀI" trong `PROMPT_KICH_BAN.md`. Bước tự kiểm tra `review.py` đã đặt mức sàn này: video dài dưới 10 phút bị báo ⚠️ (nên xem lại, vẫn được gửi), dưới 6 phút bị báo ❌ (không được gửi).

---

## 3. Kết quả trong `output\<mã>\`

| File | Dùng để |
|---|---|
| `DV1.mp4` | Video để đăng |
| `DV1_thumbnail.jpg` | Ảnh bìa (YouTube Shorts cho phép chọn) |
| `DV1_caption.txt` | Tiêu đề, caption, hashtag, và nguồn kiểm chứng để bạn lưu |
| `_work\` | File tạm (giọng đọc, dòng thời gian). Có thể xóa |

Video đã có thì lần sau sẽ bị **bỏ qua**. Muốn dựng lại sau khi sửa kịch bản:
```
python make_video.py scripts\DV1.json --force
```
Giọng đọc được lưu đệm: chỉ câu nào sửa mới phải đọc lại.

---

## 4. Tùy chỉnh trong `config.json`

| Mục | Ý nghĩa |
|---|---|
| `channel`, `catchphrase`, `follow` | Tên kênh, câu chốt, lời kêu gọi theo dõi |
| `subtitles` | `false` = không chạy phụ đề lời đọc (chữ trên hình đã đủ ý) |
| `style` | `"story"` = phong cách kể chuyện: chữ có chân, chuyển cảnh tan mờ, hạt phim, ánh đèn lồng, bộ âm lật trang / chuông đồng / nền không khí (`sfx.ambience`) |
| `pronounce` (trong kịch bản) | Cách viết kiểu tiếng Anh cho tên khó đọc; kiểm tra bằng `python phien_am.py scripts/<mã>.json` |
| `voice` | `vi-VN-HoaiMyNeural` (nữ) hoặc `vi-VN-NamMinhNeural` (nam) |
| `voice_rate` | Tốc độ đọc, ví dụ `+5%`, `+10%`, `-5%` |
| `tts_delay` | Số giây giãn cách giữa các câu đọc (máy chủ Microsoft chặn nếu gửi dồn dập). Mặc định 6 |
| `fps` | 30 là chuẩn. Giảm xuống 24 để dựng nhanh hơn |
| `music_file`, `music_volume` | Nhạc nền và âm lượng (0.08–0.15 là vừa) |
| `transition_sfx` | Âm "vút" khi chuyển cảnh: `true` / `false` |
| `subtitle_on_hook` | Có hiện phụ đề ở cảnh hook không (hook đã có chữ to nên mặc định tắt) |
| `topics` | Màu nền, màu nhấn, icon, tên của từng chủ đề |

### Nhạc nền
Đặt file nhạc vào `assets\music\nhac-nen.mp3`. Không có file thì video chỉ có giọng đọc.
**Chỉ dùng nhạc miễn phí bản quyền**, ví dụ YouTube Audio Library (studio.youtube.com → Thư viện âm thanh). Nhạc có bản quyền sẽ khiến video bị tắt tiếng hoặc mất quyền kiếm tiền.

---

## 5. Lệnh đầy đủ

```
python make_video.py scripts                  # dựng tất cả video chưa làm
python make_video.py scripts\DV1.json         # dựng 1 video
python make_video.py scripts\DV1.json --preview   # bản xem trước 540x960
python make_video.py scripts --check          # chỉ kiểm tra kịch bản
python make_video.py scripts\DV1.json --force # dựng lại
python make_video.py scripts\DV1.json --no-tts    # không cần mạng, thay giọng bằng khoảng lặng
```

---

## 6. Lỗi thường gặp

| Lỗi | Cách xử lý |
|---|---|
| `'python' is not recognized` | Cài lại Python và tick "Add python.exe to PATH" |
| `Không tạo được giọng đọc` | Kiểm tra mạng (Edge TTS cần internet), chạy lại. Câu đã đọc xong sẽ không phải đọc lại |
| `Executable doesn't exist ... chromium` | Chạy lại `cai-dat.bat` |
| `JSON sai cú pháp` | Thường do thiếu dấu phẩy hoặc có dòng `//`. Nhờ Claude sửa lại file đó |
| Emoji hiện ô vuông | Emoji quá mới mà Windows chưa có. Đổi sang emoji phổ biến hơn trong kịch bản |
| Giọng đọc sai số | Trong `voice`, viết số bằng chữ: "ba trái tim", "tám phút hai mươi giây" |

---

## 7. Cấu trúc thư mục

```
fact-video/
├─ make_video.py          bộ dựng chính
├─ config.json            cấu hình kênh, giọng, màu chủ đề
├─ PROMPT_KICH_BAN.md     prompt để nhờ Claude viết kịch bản
├─ templates/scene.html   mẫu hình động các loại cảnh
├─ assets/fonts/          phông Be Vietnam Pro (giấy phép OFL)
├─ assets/music/          đặt nhạc nền vào đây
├─ scripts/               kịch bản JSON (có sẵn 2 mẫu: DV1, CD-F1)
└─ output/                video đầu ra
```

---

## 8. Chạy trên GitHub (không cần bật máy ở nhà)

Mỗi khi có kịch bản mới hoặc kịch bản bị sửa trong thư mục `scripts/`, GitHub Actions tự dựng video bằng giọng VieNeu, rồi gửi video kèm caption và ảnh bìa về Telegram.

**Cài đặt một lần:**
1. Telegram: nhắn **@BotFather**, gõ `/newbot`, đặt tên, rồi nhận **mã bot** (dạng `123456:ABC...`). Mở bot vừa tạo, bấm **Start** và gửi 1 tin nhắn bất kỳ.
2. GitHub repo, mục **Settings → Secrets and variables → Actions → New repository secret**:
   - `TELEGRAM_BOT_TOKEN` = mã bot
3. Tab **Actions**, chọn **Lấy mã chat Telegram**, bấm **Run workflow**. Mở log để thấy dòng `MÃ CHAT: ...`.
4. Thêm secret thứ hai: `TELEGRAM_CHAT_ID` = số đó.

**Dùng hằng ngày:**
- Nhờ Claude viết kịch bản và đẩy lên `scripts/`. GitHub sẽ tự dựng, khoảng 5–10 phút sau video về Telegram.
- Muốn dựng lại một video: tab **Actions → Dựng video → Run workflow**, ô "only" điền mã, ví dụ `DV1`.
- Video cũng được lưu trong mục *Artifacts* của lần chạy, giữ trong 7 ngày.
- Danh sách video đã dựng nằm trong `rendered.json`. Xóa một dòng trong file đó để dựng lại video tương ứng.

---

## 9. Nhấn nhá giọng đọc và hiệu ứng âm thanh

**Thẻ nhấn nhá** đặt ở đầu câu trong `voice`: `[nhấn]` `[nhanh]` `[chậm]` `[cao]` `[trầm]` `[nhỏ]` `[ngừng]`.
Dấu `…` giữa câu sẽ tạo khoảng ngừng hồi hộp thật. Chi tiết xem `PROMPT_KICH_BAN.md`.

**Cách đọc tên nước ngoài:** thêm `"pronounce": {"Göbekli Tepe": "Gơ bếch li Tê pê"}` vào kịch bản.

**Trong `config.json`:**
| Mục | Ý nghĩa |
|---|---|
| `sfx.enabled`, `sfx.volume` | Bật/tắt và độ to hiệu ứng âm thanh |
| `voice_fx` | Xử lý giọng cho rõ, dày như radio |
| `loudness_lufs` | Âm lượng chuẩn (-14 hợp TikTok/YouTube/Facebook) |
| `auto_prosody` | Tự nhấn câu mở đầu và câu cảm thán khi không có thẻ |
| `pauses` | Độ dài các khoảng ngừng (giây) |

**Thay hiệu ứng bằng âm của bạn:** đặt file WAV 16-bit vào `assets/sfx/` với tên
`transition.wav`, `pop.wav`, `tick.wav`, `chime.wav`, `impact.wav`, `reveal.wav`, `outro.wav`.

**Nhạc nền** (`assets/music/nhac-nen.mp3`) sẽ tự hạ nhỏ khi có giọng đọc và to lên lúc ngừng.

---

## 10. Ảnh minh họa tự động

Thêm `"image": {"query": "octopus underwater"}` vào cảnh. Khi dựng, công cụ tự tìm ảnh **chỉ có giấy phép mở** (CC0, Public Domain, CC BY) từ Openverse, Wikimedia Commons, NASA, Bảo tàng Met (và Pixabay nếu có secret `PIXABAY_API_KEY`). Ảnh CC BY-SA, NC, ND bị loại.
- Chỉ định nguồn: `"source": "wikimedia" | "met" | "nasa" | "openverse" | "pixabay"`
- Chỉ định ảnh cụ thể: `"image": {"url": "https://...", "credit": "Tác giả, giấy phép"}`
- Thông tin nguồn ảnh được ghi trong file caption. Ảnh CC BY thì dán dòng ghi nguồn vào mô tả video.
- Tắt ảnh: `"images": false` trong `config.json`.

---

## 11. Ảnh chuyển động (parallax 3D và lớp hạt)

Ảnh tĩnh được làm cho "sống" bằng hai lớp, áp dụng cho cả video ngắn và video dài (`motion.py`):

- **Parallax 2.5D:** máy ước lượng độ sâu của ảnh (mô hình Depth Anything V2 Small, chạy CPU, tải 1 lần khoảng 100 MB). Khi máy quay lướt hoặc đẩy vào, vật ở gần dịch nhiều hơn vật ở xa, ảnh trông như cảnh 3D. Bản đồ độ sâu được lưu đệm trong `assets/ai_cache/depth`.
- **Lớp hạt:** `dust` (bụi bay, mặc định), `embers` (tàn lửa), `rain` (mưa), `snow` (tuyết), `mist` (sương). Máy tự chọn theo mô tả ảnh và lời kể ("jungle, misty" → sương; "storm" → mưa). Muốn chọn tay, ghi vào cảnh hoặc đoạn video dài: `"fx": "rain"`, `"fx": "snow+dust"`, hoặc `"fx": "none"`.

- **Ánh sáng và máy quay** (tự chọn theo nội dung, ghi tay được trong `"fx"`): `rays` (tia nắng xuyên rừng), `lightning` (chớp khi có bão), `flicker` (ánh lửa hắt chập chờn), `shake` (rung máy khi có nổ, pháo kích).
- **Đổi tiêu điểm:** ảnh có độ sâu sẽ mờ nhẹ phần xa hoặc gần, cảnh chẵn kéo nét từ xa vào chủ thể.
- **Chuyển cảnh "lao vào ảnh":** cảnh cũ phóng nhanh tới, cảnh mới thu từ to về, kèm vệt sáng ấm quét ngang.

Chỉnh trong `config.json`:
```
"motion": { "parallax": true, "parallax_strength": 1.0, "fx": true, "fx_strength": 1.0,
            "dof": 0.6, "transition": "zoom", "light": true }
```
`dof` 0 = tắt đổi tiêu điểm; `transition` `"fade"` = tan mờ như cũ; `light` false = tắt tia nắng, chớp, lửa hắt, rung máy.
`parallax_strength` 0.5 = nhẹ hơn, 1.5 = mạnh hơn. Đặt `false` để tắt. Lỗi mô hình hay WebGL thì cảnh đó tự quay về chuyển động cũ, video không hỏng.
Ghi chú: dựng chậm hơn khoảng 2–3 lần (video ngắn khoảng 1,8 lần, video dài khoảng 3 lần).

**Dựng thử không ghi đè bản cũ:** chạy workflow "Dựng video" với ô *Hậu tố* = `-thu`, kết quả nằm ở Releases tag `video-<mã>-thu`.

## 12. Tiết kiệm chi phí Gemini

- **Kiểm tra kịch bản trước khi dựng:** Gemini đọc chữ kịch bản (rẻ, có lưu đệm). Có lỗi nội dung thì máy **không dựng**, báo lỗi về Telegram để bạn sửa. Chắc chắn không phải lỗi thì chạy workflow "Dựng video" với ô *Bỏ qua kiểm tra* = `yes`.
- **Chỉ gửi cả video cho Gemini xem lại khi lời kể hoặc giọng đọc thay đổi.** Dựng lại vì sửa ảnh thì chỉ soi từng khung hình. Muốn luôn xem lại cả video: đặt biến `REVIEW_VIDEO=always`.
- **Bước tự kiểm tra dùng Flash-Lite** (rẻ nhất), không dùng được thì tự lùi về Flash.
- **Chi phí ước tính mỗi lần dựng** được gửi kèm báo cáo Telegram và lưu ở `logs/chiphi_<mã>.txt`. Số chính xác xem ở Google Cloud Billing → Reports → Group by SKU.

## 9. Tự kiểm tra trước khi gửi (`review.py`)

Sau khi dựng, máy tự soi lại từng sản phẩm rồi gửi **báo cáo kiểm tra** về Telegram:

| Bước | Soi gì | Công cụ |
|---|---|---|
| Kỹ thuật | Thời lượng, kích thước, có tiếng, màn hình đen, hình đứng im, mất giọng, độ to | ffmpeg (miễn phí) |
| Kịch bản | Đối chiếu mục "Kiểm chứng" trong kế hoạch, số liệu khớp nhau, chính tả, nội dung cấm | Gemini đọc chữ |
| Xem và nghe | Giọng đọc đúng từng câu (tên, số, dấu), hình đúng lời, chữ trên màn hình, chủ thể bị cắt | Gemini xem video |
| Khung hình | Lỗi tranh AI (tay chân dị dạng, chữ méo, sai thời đại), watermark, ảnh nhạy cảm | Gemini xem ảnh rõ nét |
| Bài ảnh | Chữ trên ảnh, chính tả bài viết, ảnh hợp câu chữ | Gemini xem ảnh |
| Đồng bộ (video dài) | Đoạn đọc nhanh/chậm bất thường, dấu hiệu ảnh đổi lệch lời | tính toán |

Kết luận: **✅ Đạt** · **⚠️ Nên xem lại** · **❌ Có lỗi**. Bản bị **❌** sẽ **không được gửi** khi chạy "Gửi Telegram"
(muốn vẫn gửi thì đặt ô *Vẫn gửi* = `yes`). Báo cáo nằm ở `logs/kiemtra_<mã>_ngan.txt`, `logs/kiemtra_<mã>_dai.txt` và trên Releases.

- **Kiểm tra lại video đã có:** Actions → *Tự kiểm tra lại video đã dựng* → nhập mã (ví dụ `SL2` hoặc `SL2:dai`).
- **Dạy máy soi thêm:** gặp lỗi mà máy bỏ sót thì thêm một dòng vào `review_checklist.md` đúng mục. Lần sau máy kiểm tra cả điều đó.
- **Chạy trên máy nhà:** `python review.py SL2` (cần `GEMINI_API_KEY`), hoặc `python review.py SL2 --no-ai` chỉ kiểm tra kỹ thuật.
- Chi phí: chỉ gọi Gemini Flash để **đọc** video và ảnh (không vẽ), khoảng vài trăm đồng mỗi chuyện. Kết quả được lưu đệm nên chạy lại cùng một video không tốn thêm.
