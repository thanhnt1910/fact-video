# Phim bản đồ (kiểu mới, giọng hài)
Bản thử chương Hạ Bì (tập gộp 4+5, câu 128–143). Các file còn đường dẫn /tmp/proto, /tmp/wt: khi dùng cho tập khác phải đổi.
- world.py: dựng bản đồ nền từ Natural Earth (ne_land.json, ne_lakes.json tải từ raw.githubusercontent.com).
- build.py: chữ, phụ đề, thẻ nhân vật, mốc thời gian (đọc ke-hoach/thu-giong-hai/*.json và VOICE_DIR/thoi_luong.json).
- mapfilm.py: dựng khung hình (camera, quân, huy hiệu thua, đêm, lửa), ghi mv.mp4.
- audio.py: tiếng động tổng hợp + ghép giọng đọc có hạ tiếng nền khi đọc.
Giọng: `python thu_giong_hai.py <json> Puck <thư mục>` (workflow thu-giong-hai.yml, chạy bằng push vào chay.txt).

## Hiệu ứng phụ (FX) và bản quyền âm thanh
- Danh sách `FX=[(t0,t1,loại,điểm_bắn,điểm_trúng)]` trong file nội dung tập (`tq45_content.py`):
  - `catapult`: máy bắn đá (đá bay theo đường cong, bụi và vòng xung kích khi rơi; có thật ở Quan Độ năm hai trăm).
  - `firearrows`: loạt tên lửa bay theo đường cong.
  - `horn`: kèn lệnh, vòng sóng lan ra.
- Thời Tam Quốc chưa có thuốc súng: KHÔNG dùng "pháo nổ/đại bác". Thứ gần nhất có thật là máy bắn đá.
- Mọi âm thanh (vó ngựa, bước chân, binh khí, cung, trống, kèn, máy bắn đá, lửa...) do `audio2.py` tự tổng hợp bằng code: không dùng mẫu thu sẵn nên không dính bản quyền. Giọng đọc là Gemini TTS (Puck).
