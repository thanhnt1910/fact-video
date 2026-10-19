# Phim bản đồ (kiểu mới, giọng hài)
Bản thử chương Hạ Bì (tập gộp 4+5, câu 128–143). Các file còn đường dẫn /tmp/proto, /tmp/wt: khi dùng cho tập khác phải đổi.
- world.py: dựng bản đồ nền từ Natural Earth (ne_land.json, ne_lakes.json tải từ raw.githubusercontent.com).
- build.py: chữ, phụ đề, thẻ nhân vật, mốc thời gian (đọc ke-hoach/thu-giong-hai/*.json và VOICE_DIR/thoi_luong.json).
- mapfilm.py: dựng khung hình (camera, quân, huy hiệu thua, đêm, lửa), ghi mv.mp4.
- audio.py: tiếng động tổng hợp + ghép giọng đọc có hạ tiếng nền khi đọc.
Giọng: `python thu_giong_hai.py <json> Puck <thư mục>` (workflow thu-giong-hai.yml, chạy bằng push vào chay.txt).
