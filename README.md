# 🎬 Bộ tạo video "Hóa Ra Là Vậy"

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
