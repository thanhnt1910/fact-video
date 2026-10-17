# Tam Quốc tập 3+4 (video gộp ~22 phút) — Kế hoạch 40 clip Veo (ảnh → video)

Trạng thái: KẾ HOẠCH. Danh sách cảnh dưới đây là dự kiến theo nội dung ảnh; chỉ chốt sau khi ảnh tập 3 (Cloudflare/Kaggle) và ảnh tập 4 đã được duyệt xong, vì mỗi clip phải bắt đầu đúng từ ảnh cuối cùng.

## 1. Con số

| Mục | Giá trị |
|---|---|
| Số clip | 40 = 20 của tập 3 + 20 của tập 4 |
| Độ dài mỗi clip | 6 giây (cảnh rộng, ít người có thể 8 giây) |
| Tổng thời lượng Veo | khoảng 240–280 giây, tức khoảng 18–20% video |
| Nhịp | khoảng 1 clip mỗi 33 giây, rải đều cả video, không dồn vào một đoạn |
| Chi phí qua API (Veo 3.1 Lite, 720p, 0,05 USD/giây) | 40 × 6 s = 240 s ≈ 12 USD (bản Fast 0,10 USD/giây ≈ 24 USD; không dùng bản thường) |
| Nếu làm tay trong Google Flow | trừ vào hạn mức credit của tài khoản, không tốn tiền API |

## 2. Chọn cảnh nào làm clip

Rút từ bài học của tập 1 (`tam-quoc-tap-1-veo.md`):
- Chỉ chọn cảnh có chuyển động của máy quay và môi trường (khói, lửa, cờ, nước, mây, bụi, đoàn quân đi xa). Nhân vật chỉ thở nhẹ, áo bay theo gió.
- Không làm clip cho cảnh có tay tương tác (trao, nhận, chắp tay, nắm, chỉ), cảnh cận mặt, cảnh 3 người trở lên đứng sát nhau, cảnh có bộ ba Lưu–Quan–Trương đứng cạnh nhau (dễ đổi mặt, thừa tay).
- Mỗi ảnh chỉ làm một clip, và mỗi ảnh trong video chỉ xuất hiện một lần nên không có clip trùng.
- Chọn dư 6 cảnh dự phòng cho mỗi tập, để clip hỏng thì thay bằng cảnh dự phòng thay vì bỏ trống nhịp.

## 3. Tiền tố dán vào MỌI prompt

`Animate this exact 2D ligne claire illustration. Keep the same drawing style, flat colours, outlines and exactly the same characters, faces, clothes and number of people. No new people, no new objects, no text, no letters, no camera cut, no zoom into faces, silent, no music, no speech. Motion:`

## 4. Tập 3 — 20 clip (ảnh `assets/anh_2d/TQ3/NNN.jpg`)

| Ảnh | Cảnh | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|
| 001 | Ải Hổ Lao, bộ tứ Lữ Bố và ba anh em | Slow push-in toward the pass, dust and banners blow, horses stay in place and only breathe, no one changes position. |
| 013 | Đại điện trống lúc chiều tà | Static camera, the oil lamp flame flickers softly, long shadows creep slowly across the floor, dust floats in the light. No people appear. |
| 015 | Doanh trại liên quân buổi tối | Slow lateral drift along the camp, cooking fires flicker, smoke rises, banners sway, soldiers stay seated. |
| 016 | Tôn Kiên dẫn quân hành quân | Slow tracking along the marching column, dust rises from the feet, banners flutter, the column keeps a steady pace. |
| 019 | Tôn Kiên trên đồi nhìn về Lạc Dương | Slow push-in from behind, strong wind moves his cloak and the banners, grass ripples, clouds drift over the distant walls. |
| 024 | Tôn Kiên phá vòng vây trên ngựa | Camera tracks sideways, the horse gallops forward, dust trails behind, banners snap in the wind. Same number of riders. |
| 026 | Tổ Mậu bên cột cháy dở lúc chiều tối | Static camera, smoke curls from the scorched post, embers glow, grass sways, his clothes move slightly in the wind. |
| 028 | Tôn Kiên tập hợp lại quân lúc bình minh | Slow push-in, dawn light brightens, red banners ripple, mist drifts across the hill, the spears stay upright. |
| 031 | Đêm quân Đổng Trác hỗn loạn | Slow push-in, torch flames flicker, dust swirls, the horses shuffle, no one new enters. |
| 036 | Lạc Dương cháy, đoàn xe dời đô | Slow upward tilt, thick smoke columns rise and roll across the sky, embers drift, the caravan moves slowly forward. |
| 037 | Tôn Kiên đi qua phế tích cung điện | Slow forward drift through the ruins, ash and dust drift, thin smoke rises from charred beams, the men walk calmly. |
| 043 | Tôn Kiên một mình lên dốc, cung thủ ẩn nấp | Slow push-in, evening mist drifts in the valley, leaves rustle, the rider climbs the path slowly. The hidden archers stay still. |
| 044 | Con ngựa không người và dải khăn đỏ | Static camera, the riderless horse breathes and flicks its tail, the red cloth flutters, light fades slowly. |
| 045 | Sông Trường Giang phía nam | Slow forward glide over the river, the sailing boats drift gently, water glitters, clouds move, birds cross the sky. |
| 048 | Công Tôn Toản dẫn kỵ binh lông thú | Slow lateral tracking along the cavalry column, dust rises, horses trot steadily, banners flutter. Same number of riders. |
| 052 | Bồi đắp ổ Mi Ổ | Slow push-in on the huge fortress walls, dust rises from the workers, ropes sway, clouds drift. |
| 057 | Cổng cung Vị Ương lúc rạng sáng | Static camera with a very slow push-in, grey dawn light brightens, a light breeze moves the guards' tassels, mist drifts across the stone road. |
| 062 | Lưu Bị một mình trên tường đất Bình Nguyên | Slow push-in from behind, the dusk sky glows, smoke drifts, his robe moves in the wind. He stays standing still. |
| 063 | Lưu Bị cưỡi ngựa trên đường phía đông | Slow tracking, the riders move steadily along the road, dust rises, clouds drift over the hills, the messenger rides closer at the far end. |
| 064 | Cổng thành cũ lúc mặt trời mọc | Slow push-in, the sun rises behind misty hills, birds fly across the sky, the mist moves along the empty road. No people appear. |

Dự phòng tập 3: 035 (ải Hổ Lao vắng), 061 (đồng sương), 042 (lửa trại các quân), 011 (Viên Thiệu ra cửa đông), 046 (liên quân rút), 003 (ải và phòng sử).

## 5. Tập 4 — 20 clip (ảnh `assets/anh_2d/TQ4/NNN.jpg`, theo bảng ánh xạ cảnh–ảnh)

| Ảnh | Cảnh | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|
| 004 | Cổng thành Từ Châu bên sông, thuyền lương | Slow push-in toward the gate, boats rock gently at the quay, water ripples, flags sway, soft morning light shifts. |
| 005 | Hai ngả đường nhìn từ đồi cao | Slow aerial drift over the plain, two small columns advance along the roads, dust trails, clouds move. |
| 009 | Hai đạo quân đối mặt qua sông | Slow lateral drift, the river flows, banners flutter, dust drifts between the two armies, the ranks stay in place. |
| 014 | Nhà tranh ban đêm, ánh đèn qua cửa sổ | Static camera, the lamplight flickers in the window, night clouds drift, grass moves in the wind. No people appear. |
| 024 | Đoàn xe gia quyến trên đường núi Lang Gia | Slow tracking beside the convoy, the ox carts roll steadily, mist drifts between the peaks, dust rises. |
| 025 | Đêm sương, đoàn xe dừng, đuốc trên sườn núi | Static camera with slow push-in, thick mist rolls across the road, distant torch lights flicker on the ridge, the carts stay still. |
| 029 | Thành bên sông, bến thuyền đông đúc | Slow push-in on the quay, boats rock, porters keep moving slowly, flags flutter, water glitters. |
| 030 | Quân Tào Tháo trước thành đang cháy | Slow push-in, thick smoke rolls over the towers, flames flicker, banners flap in the wind, the ranks stay in place. |
| 032 | Phố vắng, xe đổ, khói còn lại | Slow forward drift down the empty street, thin smoke and dust drift, a torn cloth flutters. No people appear. |
| 042 | Thành nhỏ lúc chiều tối | Slow push-in, evening clouds move, smoke rises from roofs, banners sway, soldiers stay in place. |
| 054 | Thọ Xuân, thành cao ở phương nam | Slow upward tilt along the city wall and gate tower, clouds drift, the plain banner flutters. |
| 065 | Duyện Châu dưới cờ đỏ của Lữ Bố | Slow push-in, the red banner ripples, dust rises as the cavalry rides out of the gate, evening light shifts. |
| 069 | Lưu Bị dẫn quân lúc hoàng hôn vàng | Slow tracking from the side, the riders move steadily, golden light glows, dust rises, grass ripples. Same number of riders. |
| 072 | Ba lữ khách đi trên con đường đồi dài | Slow aerial drift behind the walkers, they keep walking at a calm pace along the winding road, clouds drift over the hills. |
| 076 | Tào Tháo một mình trước ngôi mộ lúc rạng sáng | Static camera with slow push-in, incense smoke curls up, grey dawn light brightens, a cold wind moves his cloak. He stays standing still. |
| 077 | Tháp cổng thành trên ruộng lúa | Slow push-in, rice leaves ripple in the wind, grey clouds roll, the banner flaps, guards stay still. |
| 080 | Bốn con đường gặp nhau ở cổng thành | Slow downward tilt to the crossroads, small groups of riders slowly advance along the roads, dust rises, dusk darkens gradually. |
| 084 | Lữ Bố từ phía sau, áo rách, quân mệt | Slow tracking behind the riders, the torn cloak flutters, dust rises, the horses walk wearily. Same number of riders. |
| 085 | Đêm mưa, toán kỵ đuốc tới cổng thành | Static camera with slow push-in, heavy rain falls, torch flames flicker, puddles ripple, horses shuffle slightly. |
| 086 | Bàn đêm với cuộn thẻ tre và đèn | Static camera, the oil lamp flame flickers, warm light moves across the table, night clouds drift outside the lattice window. No people appear. |

Dự phòng tập 4: 058 (suối chảy vào sông), 075 (thành sông, thuyền), 019 (đoàn lính hành quân), 045 (nhìn quân Tào rút), 046 (đoàn quân trên đường đá), 031 (đoàn dân phu).

Lưu ý: bảng ánh xạ cảnh–ảnh tập 4 (65 cảnh dùng 65 ảnh trong 86 ảnh) đang tạm; nếu một ảnh ở trên không nằm trong 65 ảnh được dùng thì thay bằng cảnh dự phòng.

## 6. Cách làm (hai hướng, chọn một)

A. Tự động qua API (khuyến nghị, rẻ và lặp lại được): viết `veo_lo.py` đọc `ke-hoach/veo/TQ34_clips.json` (tập, ảnh, prompt), mỗi ảnh gọi Veo 3.1 Lite 6 giây 16:9 720p, bỏ tiếng, lưu `assets/clips_2d/TQ34/E3_NNN.mp4`, `E4_NNN.mp4`, bỏ qua clip đã có, ghi chi phí bằng `chi_phi.py`. Chạy bằng workflow bấm tay (như `veo-thu.yml`), chia 4 đợt 10 clip để dễ kiểm.
B. Làm tay trong Google Flow ("Frames to Video"): tải ảnh làm khung đầu, dán tiền tố + prompt, 16:9, tắt âm thanh; tải về đặt vào cùng thư mục và tên như trên.

Thứ tự: làm thử 3 clip (tập 3: 036; tập 4: 004; tập 3: 019) để đánh giá chất lượng và tính hợp lý của prompt, rồi mới làm 37 clip còn lại.

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
