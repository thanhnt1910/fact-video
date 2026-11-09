# Eratosthenes đo Trái Đất (video khoa học số 1, dọc 9:16, bản tiếng Việt duyệt trước)

Dựng: `remotion/src/eratosthenes/`. Âm thanh: `sfx.ts` + `scripts/dump_sfx_era.ts` + `scripts/sfx_thales.py`. Chưa có giọng đọc (thời lượng ước theo `beatSeconds`).

## Nguồn đã kiểm
- Cleomedes là nguồn duy nhất còn lại; sách của Eratosthenes đã mất. Vì vậy lời kể mở bằng "Người ta kể".
- Độ lệch bóng 7°12′ = 1/50 vòng; khoảng cách khoảng 5.000 stadia (do người đo bước đường, bematist); 5.000 × 50 = 250.000 stadia. Một số nguồn ghi con số của chính ông có thể là 252.000: chưa chốt.
- 1 stadion ≈ 157,5 m là một giả thiết trong nhiều giả thiết (Pliny nêu cách quy đổi); độ dài đúng còn tranh cãi. Kết quả ≈ 39.375 km so với ≈ 40.008 km (vòng qua hai cực): lệch khoảng 1,6%.
- Syene không nằm đúng chí tuyến và hai thành phố không nằm đúng một kinh tuyến: đã nói trên màn hình là "đơn giản hóa".
- Mét: 1/10.000.000 đường từ Bắc Cực tới xích đạo qua Paris; đo cung Dunkerque–Barcelona 1792–1798 (Delambre và Méchain), phần còn lại suy ra; chuẩn bạch kim 1799.

## Là minh họa, không phải tư liệu
Người que, quả địa cầu, góc vẽ to hơn thật (có chú thích trên hình), cảnh người đi vòng Trái Đất.

## Cần chủ kênh duyệt
Bản có giọng Leda (đọc từng câu, loudnorm -16 LUFS mỗi câu): nhịp mỗi câu = thời lượng giọng + 0,5 s, tổng 79,7 s. Không làm bản tiếng Anh cho video ngắn.


## Cập nhật bản dựng lại (22 câu, giọng Leda)
- Lời kể: `TEXT_E` trong `src/eratosthenes/content.ts` (22 câu đã duyệt: quả cam + hai que tăm, đèn pin, bánh 50 miếng).
- Độ dài thật khoảng 127 giây (không phải 85 giây): nhịp mỗi câu = thời lượng giọng Leda + 0,5 giây (`leda_dur.json`).
- Điều còn tranh cãi giữ trong lời kể: "người ta kể" (nguồn duy nhất là Cleomedes), độ dài stadion không chắc, 800 km x 50 làm tròn 40 000 km so với 39 375 km đổi theo cách phổ biến (lệch 1,6%).
- Dựng: SFX `scripts/dump_sfx_era.ts` -> `scripts/sfx_thales.py`; render `Eratosthenes`; ghép 22 file `demo/era/leda/NN.wav` (loudnorm -16, trễ 0,15 giây sau đầu câu), SFX nhỏ 0,5.
