# So sánh giọng: B (hồ sơ cũ) và C (hồ sơ cố định mới)

Mỗi lần gồm 2 cụm tạo ở 2 request độc lập. f0 = cao độ trung vị (Hz), wps = chữ/giây, rms = mức (dB), cen = trọng tâm phổ (Hz, độ sáng).

| Lần | model | dự phòng | f0 cụm1 | f0 cụm2 | lệch f0 | wps 1 | wps 2 | rms 1 | rms 2 | sáng 1 | sáng 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B1 | gemini-3.8-flash-tts | False | 145.5 | 139.1 | 6.3 | 4.81 | 4.78 | -15.6 | -15.3 | 2609 | 3052 |
| B2 | gemini-3.8-flash-tts | False | 132.2 | 135.6 | 3.4 | 5.04 | 4.89 | -15.5 | -15.9 | 2563 | 3342 |
| B3 | gemini-3.8-flash-tts | False | 142.9 | 134.5 | 8.4 | 5.08 | 5.02 | -15.4 | -16.4 | 2647 | 3084 |
| C1 | gemini-3.8-flash-tts | False | 110.3 | 115.1 | 4.8 | 4.97 | 5.19 | -16.1 | -16.0 | 2773 | 2747 |
| C2 | gemini-3.8-flash-tts | False | 119.4 | 131.1 | 11.7 | 5.19 | 5.10 | -16.1 | -15.4 | 2631 | 2977 |
| C3 | gemini-3.8-flash-tts | False | 112.7 | 115.1 | 2.4 | 4.94 | 4.67 | -15.9 | -16.7 | 2872 | 3301 |

## Tóm tắt theo hồ sơ (3 lần tạo)

- **B**: f0 trung bình 138.3 Hz, độ lệch chuẩn 4.7; tốc độ 4.94 chữ/giây, độ lệch chuẩn 0.12; độ sáng độ lệch chuẩn 292 Hz; lệch cao độ giữa hai cụm nối tiếp trung bình 6.0 Hz
- **C**: f0 trung bình 117.3 Hz, độ lệch chuẩn 6.8; tốc độ 5.01 chữ/giây, độ lệch chuẩn 0.18; độ sáng độ lệch chuẩn 215 Hz; lệch cao độ giữa hai cụm nối tiếp trung bình 6.3 Hz

Độ lệch chuẩn càng nhỏ thì giọng càng ổn định giữa các lần và giữa các cụm. Số đo chỉ là chỉ báo; quyết định cuối cần nghe các file nghe_B*.mp3 và nghe_C*.mp3.