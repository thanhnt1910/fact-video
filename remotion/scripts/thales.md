# Video 1: How Thales Measured a Pyramid / Thales đo kim tự tháp như thế nào

Lời kể nằm trong `src/thales/content.ts` (EN và VI, từng beat).

## Nguồn đã kiểm
- Diogenes Laërtius, Lives, 1.27 (dẫn Hieronymus): Thales đo kim tự tháp bằng bóng, lúc bóng người bằng chiều cao người.
- Plutarch, Banquet of the Seven Sages 147: cây gậy đặt ở đầu bóng, hai tam giác đồng dạng. Không nêu tên vua, nên lời kể không nhắc Amasis.
- MacTutor: Thales khoảng 624–547 TCN; các bản kể viết rất lâu sau, nên lời kể dùng "các tác giả cổ đại kể".
- Đại Kim Tự Tháp: cao 146,6 m lúc xây (khoảng 2600 TCN), nay 138,5 m, cạnh đáy 230,3 m.

## Ghi chú độ chắc
- Số trong ví dụ (gậy 2 m, bóng 3 m, 220 m, ≈147 m) chỉ để minh họa.
- Bước cộng nửa cạnh đáy là cách giải thích hình học của kênh, không phải lời nguồn cổ.
- Video chưa có giọng đọc: thời lượng beat được ước tính, sẽ thay bằng giọng thật (từng câu) sau.

## Bản 2 (sinh động hơn, `Thales2EN` / `Thales2VI`, mã trong `src/thales2/`)
- Lời kể: `src/thales2/content.ts`. Mạch: mở đầu có lạc đà và Thales → Mặt Trời lên cao làm bóng ngắn dần (đồng hồ, cung góc) → lúc bóng bằng người → vướng mắc nửa cạnh đáy (mây suy nghĩ nhìn từ trên xuống) → mẹo cây gậy (tia song song, tam giác nhỏ phóng to khớp tam giác lớn) → con số → kết.
- Hình minh họa không đúng tỉ lệ (gậy và người vẽ to hơn thật); video có ghi "(not to scale)".
- Lạc đà, người cưỡi và cảnh Thales đi lại chỉ là hình minh họa, không phải chi tiết từ nguồn cổ.
- Chi tiết "Thales chờ đúng lúc bóng bằng người" theo Diogenes Laërtius 1.27; "cắm gậy ở đầu bóng, hai tam giác" theo Plutarch 147.

## Bản 3 (`Thales3`, tiếng Việt, mã trong `src/thales3/`)
Mạch: người xưa thử đo (dây đo đất, thang, tháp người, leo trơn + dây chỉ đo đường dốc) → ý tưởng bóng → cách Thales → ngày nay (máy đo góc, Everest, đo cây, mô hình thu nhỏ).
Âm thanh: `src/thales3/sfx.ts` (danh sách sự kiện theo mốc thời gian) → `scripts/dump_sfx.ts` → `scripts/sfx_thales.py` (tổng hợp bằng numpy, không dùng mẫu có bản quyền) → ghép bằng ffmpeg.

## Nguồn đã kiểm cho bản 3
- Người căng dây Ai Cập (harpedonaptae): Democritus qua Clement, Strom. i.15.69; Herodotus 2.109 (đo lại ruộng sau khi sông Nin dâng nước, "nguồn gốc của hình học") — dẫn lại trong Heath, From Thales to Euclid.
- Đại Kim Tự Tháp: cao 146,6 m, cạnh đáy 230,3 m, dốc 51°50'40", ốp đá vôi Tura trắng nhẵn (Wikipedia, mục Great Pyramid of Giza).
- Đường dốc ≈ 186 m: tự tính từ hai số trên (căn của 146,6² + 115,15²). Số "khoảng 86 người" = 146,6 chia 1,7 (minh họa, giả định người cao 1,7 m).
- Everest: Great Trigonometrical Survey, góc đo từ trạm cách đỉnh khoảng 160–190 km, nối từ đường chuẩn 1802; Waugh công bố 3/1856 ≈ 29.002 feet (≈ 8.840 m) (explorersweb.com/the-five-men-who-measured-mount-everest). Số chính thức 8.848,86 m do Trung Quốc và Nepal công bố 12/2020 (Britannica).
- Đo cây bằng bóng, bản đồ/mô hình theo tỉ lệ: kiến thức chung về tam giác đồng dạng, không gắn nguồn riêng.
- Cảnh người leo trượt, tháp người, lạc đà là hình minh họa, không phải chi tiết từ nguồn cổ.
