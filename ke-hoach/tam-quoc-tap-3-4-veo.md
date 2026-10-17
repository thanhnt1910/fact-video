# Tam Quốc tập 3+4 (video gộp ~22 phút) — Kế hoạch 40 clip Veo (ảnh → video)

Trạng thái: KẾ HOẠCH. Danh sách cảnh dưới đây là dự kiến theo nội dung ảnh; chỉ chốt sau khi ảnh tập 3 (Cloudflare/Kaggle) và ảnh tập 4 đã được duyệt xong, vì mỗi clip phải bắt đầu đúng từ ảnh cuối cùng.

## 1. Con số

| Mục | Giá trị |
|---|---|
| Số clip | 40 = 20 của tập 3 + 20 của tập 4 |
| Độ dài mỗi clip | 6 giây (cảnh rộng, ít người có thể 8 giây) |
| Tổng thời lượng Veo | khoảng 240–280 giây, tức khoảng 18–20% video |
| Nhịp | khoảng 1 clip mỗi 33 giây, rải đều cả video, không dồn vào một đoạn |
| Chi phí qua API (Veo 3.1 Lite, 720p, 0,05 USD/giây) | 40 × 6 s = 240 s ≈ 12 USD cho một lần; tính cả làm lại cảnh tay khoảng 30 USD (bản Fast gấp đôi; không dùng bản thường) |
| Nếu làm tay trong Google Flow | trừ vào hạn mức credit của tài khoản, không tốn tiền API |

## 2. Chọn cảnh nào làm clip (đã sửa theo yêu cầu chủ kênh: ưu tiên cảnh chính theo cốt truyện)

Tiêu chí chọn là tầm quan trọng của cảnh trong câu chuyện, không phải độ an toàn. Cảnh có tương tác tay vẫn làm khi đó là khoảnh khắc chính (trao ấn, nhận khăn, từ chối, thề báo thù, cầm kích, tin dữ...). Bản kế hoạch đầu loại các cảnh này vì Veo dễ làm méo tay, đó là sai thứ tự ưu tiên; nay xử lý rủi ro bằng cách làm kỹ, không bằng cách bỏ cảnh.

Cách làm cho cảnh có tương tác tay:
- Prompt mô tả đúng MỘT hành động nhỏ, chậm, rõ chủ thể ("he slowly lowers the box into the other man's hands"), kèm câu giữ nguyên số người, số tay, số vật.
- Máy quay gần như đứng yên hoặc đẩy chậm, để Veo chỉ phải động một chỗ.
- Mỗi cảnh chính tạo tối đa 3 lần với 3 mô tả hơi khác nhau, chọn bản tốt nhất. Chỉ khi cả 3 hỏng mới dùng ảnh tĩnh với hiệu ứng máy quay, hoặc thay bằng cảnh toàn cảnh cùng đoạn lời kể.
- Chi phí tính theo mức này: tối đa 40 clip × 6 giây × 2,5 lần thử trung bình ≈ 600 giây ≈ 30 USD (Lite). Veo Fast gấp đôi.

Cảnh chỉ có phong cảnh, khói, lửa, đoàn quân xa (an toàn) dùng làm cảnh dự phòng và cảnh nối, không chiếm chỗ cảnh chính.

Mỗi ảnh chỉ làm một clip và mỗi ảnh chỉ xuất hiện một lần trong video, nên không có clip trùng.

## 3. Tiền tố dán vào MỌI prompt

`Animate this exact 2D ligne claire illustration. Keep the same drawing style, flat colours, outlines and exactly the same characters, faces, clothes, weapons and number of people, arms and hands. No new people, no new objects, no text, no letters, no camera cut, no zoom into faces, silent, no music, no speech. Motion:`

## 4. Tập 3 — 20 clip cảnh chính (ảnh `assets/anh_2d/TQ3/NNN.jpg`, theo thứ tự cốt truyện)

| Ảnh | Cảnh chính | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|
| 001 | Ba anh em vây đánh Lữ Bố trước ải Hổ Lao | The camera slowly pushes in; the three riders on the left advance a few steps while Lu Bu on the right turns his horse and lifts his halberd; dust and banners blow. No one is struck. |
| 005 | Đổng Trác tiến vào Lạc Dương | The column slowly rides forward toward the camera, Dong Zhuo's horse walks at a calm pace, townspeople at both sides lean back, banners flutter. |
| 008 | Đổng Trác nhận Lữ Bố làm con nuôi | Dong Zhuo slowly lowers one hand onto the shoulder of the kneeling Lu Bu, who bows his head; officials stand still; lamp flames flicker. |
| 010 | Viên Thiệu cúi chào rồi bỏ đi | Dong Zhuo slowly raises one hand and points; Yuan Shao keeps the sheathed sword across his chest and bows deeply, then straightens; lamp flames flicker. |
| 012 | Đổng Trác bước lên thềm, mang giày, đeo kiếm | Dong Zhuo walks slowly up the stone steps, the officials on both sides bow deeper, guards stay still, his robe sways. |
| 014 | Hội minh các lộ chư hầu | Slow push-in on the platform, the lords turn their heads toward Yuan Shao, banners ripple, soldiers behind shift slightly, dust drifts. |
| 020 | Viên Thuật trao thư cho Tôn Kiên | Yuan Shu slowly holds out the sealed document and Sun Jian takes it with a bow; lamp flames flicker; officials stay still. |
| 024 | Tôn Kiên phá vòng vây | The camera tracks sideways, Sun Jian's horse gallops forward through the gap, dust trails, his red headband flutters; the enemy riders stay in the ring. |
| 025 | Tôn Kiên trao khăn đỏ cho Tổ Mậu | Sun Jian slowly takes off the red headband and hands it to Zu Mao, who takes it with both hands; dust swirls around the riders. |
| 026 | Tổ Mậu đặt khăn lên cột cháy | Zu Mao slowly places the red cloth on the scorched post, smoke curls, embers glow, grass sways in the wind. |
| 031 | Đêm quân Đổng Trác hỗn loạn | Slow push-in, riders turn their horses in confusion, torches flicker and sway, dust swirls. No one new enters. |
| 036 | Lạc Dương bị đốt, đoàn dời đô | Slow upward tilt, thick smoke columns rise and roll across the sky, embers drift, the caravan moves slowly forward. |
| 038 | Lính vớt ấn từ giếng, Tôn Kiên nhận | The soldier slowly hands the red-cloth bundle to Sun Jian, who receives it with both hands; torch flames flicker; ash drifts. |
| 039 | Viên Thuật nhìn ấn ngọc | Slow push-in on the jade seal on the table, its soft glow pulses gently; Yuan Shu leans slightly forward; officials whisper and turn their heads. |
| 043 | Tôn Kiên một mình lên dốc, cung thủ ẩn nấp | Slow push-in, evening mist drifts in the valley, the rider climbs the path slowly, the hidden archers stay still. |
| 047 | Lưu Ngu lắc đầu từ chối | Old Liu Yu slowly shakes his head with both palms raised; Yuan Shao and Han Fu stay standing; lamp flames flicker. |
| 049 | Hai đạo quân đối mặt, Công Tôn Toản trên ngựa trắng | Slow lateral drift, the white horse steps in place, banners flutter, dust drifts between the armies, the ranks stay in place. |
| 054 | Đổng Trác phóng kích về phía Lữ Bố | Dong Zhuo slowly raises the long-handled halberd over his shoulder; Lu Bu stands frozen and turns his head away; officials freeze. No one is hit. |
| 056 | Vương Doãn mật bàn với Lữ Bố | Slow push-in, Wang Yun speaks and lowers his head closer, the others lean in, the lamp flame flickers on their faces. |
| 057 | Cổng cung Vị Ương lúc rạng sáng | Slow push-in, grey dawn light brightens, the guards' tassels sway, the ox cart waits, mist drifts across the stone road. |

Dự phòng cảnh nối tập 3: 013, 015, 019, 037, 044, 045, 052, 062, 063, 064.

## 5. Tập 4 — 20 clip cảnh chính (ảnh `assets/anh_2d/TQ4/NNN.jpg`, theo bảng ánh xạ cảnh–ảnh)

| Ảnh | Cảnh chính | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|
| 001 | Đào Khiêm dâng hộp ấn cho Lưu Bị | Tao Qian slowly holds the lacquered seal box forward with both hands; Liu Bei slowly raises his hands in refusal; lamp flames flicker. |
| 002 | Lưu Bị từ chối trên thềm | Liu Bei slowly shakes his head with both hands raised; the crowd below murmurs and sways; banners flutter. |
| 008 | Sứ Công Tôn Toản trao thư bổ nhiệm | The envoy slowly extends the rolled slip toward Liu Bei, who takes it with both hands; officials stand still; light shifts. |
| 015 | Thái Sử Từ xuống ngựa trước cổng Bình Nguyên | The horse stops and blows, Taishi Ci slowly swings off and steps forward holding the small scroll; dust settles. |
| 017 | Thái Sử Từ cúi chào Lưu Bị | Taishi Ci bows deeply and straightens; Liu Bei presses one hand to his chest; Guan Yu and Zhang Fei stay still; lamp flames flicker. |
| 021 | Khổng Dung mỉm cười đọc thẻ tre | Kong Rong slowly lowers the bamboo scroll and smiles; the man before him bows slightly; lamp light flickers. |
| 026 | Sứ giả quỳ báo tin dữ cho Tào Tháo | The messenger bows his head lower; Cao Cao's fist slowly tightens and he turns his face away; officers stay still; lamp flames flicker. |
| 027 | Tào Tháo giơ nắm tay thề báo thù | Cao Cao slowly raises his fist before the army; the rows of soldiers lift their spears slightly; banners ripple; dust drifts. |
| 030 | Quân Tào trước thành đang cháy | Slow push-in, thick smoke rolls over the towers, flames flicker, banners flap, the ranks stay in place. |
| 038 | Đào Khiêm ra cổng đón Lưu Bị | Slow push-in, Tao Qian steps forward with a welcoming hand while Liu Bei's column enters the gate; townsfolk wave; banners flutter. |
| 041 | Trao ấn đồng cho Lưu Bị ở Tiểu Bái | The official slowly hands the small bronze seal to Liu Bei, who receives it with both hands; the assembled soldiers stand still; banners flutter. |
| 044 | Lữ Bố vào cửa Duyện Châu | Seen from behind, Lu Bu rides slowly through the gate; Zhang Miao and Chen Gong bow; soldiers on the wall wave their spears; dust drifts. |
| 047 | Đào Khiêm lúc hấp hối | Very slow push-in, the old man breathes weakly, the lamp flame flickers, a curtain moves in the draft. No limb moves much. |
| 049 | Đào Khiêm thì thầm di ngôn cho Mi Trúc | Mi Zhu bends slightly closer to listen; Tao Qian's lips move weakly; the dim lamp flickers; a curtain sways. |
| 052 | Lưu Bị từ chối, dân và quan quỳ van | Liu Bei slowly shakes his head with both hands raised; the kneeling delegation bows lower; soldiers stand still; dust drifts. |
| 053 | Trần Đăng khuyên Lưu Bị | Chen Deng speaks with one hand raised and slowly lowers it; the elders listen and nod; lamp flames flicker. |
| 057 | Lưu Bị chắp tay nhận Từ Châu | Liu Bei slowly bows with his hands joined; the crowd before the gate cheers and raises their arms slightly; banners flutter. |
| 060 | Mi Trúc mở rương tiền cho Lưu Bị | Mi Zhu slowly lifts the lid of the chest of bronze coins; Liu Bei looks down; servants carry silk past; light shifts. |
| 076 | Tào Tháo trước ngôi mộ lúc rạng sáng | Slow push-in, incense smoke curls, grey dawn brightens, a cold wind moves his cloak; he stays standing; the soldiers far behind stay kneeling. |
| 084 | Lữ Bố rách áo, quân mệt trên đường dài | Slow tracking behind the riders, the torn cloak flutters, dust rises, the horses walk wearily. |

Dự phòng cảnh nối tập 4: 004, 005, 009, 014, 024, 025, 029, 032, 042, 054, 065, 069, 072, 077, 080, 085, 086.

Lưu ý: bảng ánh xạ cảnh–ảnh tập 4 (65 cảnh dùng 65 ảnh trong 86 ảnh) đang tạm; nếu một ảnh ở trên không nằm trong 65 ảnh được dùng thì thay bằng cảnh chính cùng đoạn lời kể.

## 6. Cách làm (hai hướng, chọn một)

A. Tự động qua API (khuyến nghị, rẻ và lặp lại được): viết `veo_lo.py` đọc `ke-hoach/veo/TQ34_clips.json` (tập, ảnh, prompt), mỗi ảnh gọi Veo 3.1 Lite 6 giây, cho phép 1–3 lần thử với mô tả khác nhau và lưu từng bản (`_a`, `_b`, `_c`) để chọn 16:9 720p, bỏ tiếng, lưu `assets/clips_2d/TQ34/E3_NNN.mp4`, `E4_NNN.mp4`, bỏ qua clip đã có, ghi chi phí bằng `chi_phi.py`. Chạy bằng workflow bấm tay (như `veo-thu.yml`), chia 4 đợt 10 clip để dễ kiểm.
B. Làm tay trong Google Flow ("Frames to Video"): tải ảnh làm khung đầu, dán tiền tố + prompt, 16:9, tắt âm thanh; tải về đặt vào cùng thư mục và tên như trên.

Thứ tự: làm thử 3 clip cảnh chính có tay (tập 3: 025; tập 4: 001; tập 3: 036 làm đối chứng cảnh khói) để đánh giá chất lượng và tính hợp lý của prompt, rồi mới làm 37 clip còn lại.

## 7. Kiểm từng clip (bắt buộc)

Bỏ clip và dùng lại ảnh tĩnh (hoặc thay bằng cảnh dự phòng) nếu có một trong các lỗi: thêm người hoặc thêm vật, thừa tay chân, mặt méo, đổi râu hoặc áo, ngựa đi ngược hoặc thừa chân, chữ xuất hiện, kiến trúc biến thành Hàn hay Nhật, cảnh nhảy cắt, hình xấu đi ở các khung cuối. Mỗi clip xem ở 3 điểm: khung đầu, giữa, cuối.

## 8. Ghép vào video

- Clip đặt ở đầu cảnh, hết clip giữ khung cuối đến hết lời kể của cảnh đó (bộ dựng `long_video.py` đã hỗ trợ trường `clip_file` trong `beats`, tự cắt chữ Veo ở góc, phóng lên 1080p, bỏ tiếng, 24 fps).
- Thêm `clip_file` vào các `beats` tương ứng trong `scripts/TQ34.json` khi dựng bản gộp.
- Dựng lại màu, hạt phim giống ảnh tĩnh để clip và ảnh liền mạch.
- Khi dựng bản xem thử, chưa cần clip; chỉ chèn clip ở bản chính thức sau khi qua bước kiểm ở mục 7.

## 9. Việc phải xong trước khi chạy Veo

1. Duyệt xong ảnh tập 3 (kết quả Cloudflare đợt `_s`, `_t`, `_u`, `_v` và đợt Kaggle `TQ3_KG`).
2. Vẽ lại và duyệt xong ảnh tập 4 (các ảnh lỗi) và chốt bảng ánh xạ 65 cảnh – 65 ảnh.
3. Chốt danh sách 40 clip từ mục 4 và mục 5, sinh `TQ34_clips.json` tự động từ bảng.
4. Chốt hướng làm (A hoặc B) và hạn mức chi phí.
