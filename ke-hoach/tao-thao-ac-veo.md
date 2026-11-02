# Tào Tháo thật sự ác đến mức nào, theo chính sử? — Clip Veo (nhóm A, 20 clip)

Soạn 02/11/2026 từ `TQ9_plan.json` (cảnh đánh dấu V) sau khi soi từng ảnh. Lấy 20 cảnh có người di chuyển nhiều. Bỏ 045 và 082 (hai người đứng yên, ít chuyển động) và 171 (ảnh đang vẽ lại, chưa phải hàng quân đi qua cổng; đạt thì thêm làm clip thứ 21).
Lưu clip ở `assets/clips_2d/TQ9/NNN.mp4` (NNN = số câu = số ảnh), kèm `danh_sach.json`. Chủ kênh tạo clip trong Google Flow.

## Nhóm A — Veo (20 clip)

Chọn "Frames to Video", tải ảnh `assets/anh_2d/TQ9/NNN.jpg` làm khung đầu, 16:9, 8 giây hoặc ngắn nhất, tắt âm nếu có. Dán tiền tố rồi dán prompt. Mỗi ảnh một clip. **Làm thử 3 clip trước: 042, 167, 073** (ba kiểu chuyển động: đám đông tiến lên, người chạy, ngựa kéo xe), thấy ổn mới làm 17 clip còn lại.

**Tiền tố dán vào MỌI prompt:**

`Animate this exact 2D ligne claire illustration. Keep the same drawing style, flat colours, outlines, and exactly the same characters, faces, clothes and objects. Keep exactly the same people in the foreground. Han dynasty clothing only, no modern objects, no new foreground people, no text, no letters, no camera cut, no zoom into faces, silent, no music, no speech. Motion:`

**Quy tắc về tên:** prompt Veo TUYỆT ĐỐI không nêu tên riêng của người thật nổi tiếng. Chỉ mô tả chung ("the foreground man", "the officer"). Kiểm bằng `python kiem_prompt_veo.py ke-hoach/tao-thao-ac-veo.md`.

**Quy tắc chuyển động:** người tiền cảnh bước đều, áo khăn bay theo gió; hàng quân chuyển động tập thể đơn giản; ngựa đi bước thường, chân theo nhịp tự nhiên; không cảnh chém, không máu. Clip nào mọc thêm người, thêm tay, mặt méo, ngựa méo hoặc thừa chân, ảnh đổi nét vẽ thì bỏ, dùng ảnh tĩnh. Veo xuất 720p thì dựng lại 1080p/30 fps.

| Ảnh | Câu | Cảnh (chỉ để tra, KHÔNG dán vào Veo) | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|---|
| 018 | 18 | Người đàn ông râu bạc áo xanh đậm đi giữa phố đêm, hai người cầm đuốc đi hai bên | Slow push-in as the foreground man walks forward at a steady pace down the lane, the two torch bearers walk beside him, torch flames flicker and shadows shift, his sleeves and sash sway. |
| 030 | 30 | Một người cưỡi ngựa nâu trước tháp cổng thành lúc rạng sáng | Slow lateral tracking as the rider guides the horse forward at a calm walking pace, the horse's legs move in a natural regular walking gait, his sleeves and headband sway, dust rises at the hooves, clouds drift. |
| 037 | 37 | Một người cưỡi ngựa ban đêm, hai người đi bộ bên cạnh một xe gỗ | Slow lateral tracking as the horse and rider move forward at a calm walking pace, the two men walk beside the wooden cart, the cart wheels turn slowly, the horse's legs move in a natural regular gait, stars twinkle. |
| 040 | 40 | Một vị tướng giáp đứng trước hàng quân đang kéo về, cờ nhiều màu | Slow push-in, the long column of soldiers behind him marches forward in step, spear tips tilt together, the banners flutter, thin dust rises from the road, the foreground officer stands still and breathes. |
| 042 | 42 | Hàng quân khăn vàng tiến lên giữa phố, cờ vàng phía sau | Slow push-in as the rows of soldiers with yellow headbands march forward in step, the leading man swings a long wooden staff beside him as he walks, the yellow flags flutter, dust rolls across the road. |
| 044 | 44 | Đoàn người đi dọc bờ sông, có xe và giỏ đồ | Slow lateral tracking as the long line of people walks along the riverside road at a steady pace, the cart wheels turn slowly, their clothes sway, the river ripples, dust drifts. |
| 048 | 48 | Một ông già ngồi trên xe bò chở hàng, hai người đi bộ bên cạnh, khói ở xa | Slow lateral tracking as the ox pulls the cart forward at a walking pace, the old man sits swaying with the cart, the two men walk beside it, the cart wheels turn slowly, thin smoke drifts over the hills. |
| 050 | 50 | Hàng lính áo đen cầm giáo cờ trơn đi lúc hoàng hôn, khói đỏ phía sau | Slow lateral tracking as the line of soldiers marches forward in step, spears tilt together, the plain banners flutter, smoke drifts across the orange sunset sky, long shadows slide along the ground. |
| 052 | 52 | Đoàn quân nhìn từ sau, bóng đen cầm giáo, khói ở chân trời | Slow push-in behind the column as the soldiers march away from the camera in step, the spear tips sway in unison, the plain banners flutter, grey smoke rises and drifts on the horizon. |
| 056 | 56 | Đám đông đi trên phố khói, một người kéo xe | Slow push-in as the crowd walks toward the camera at a steady pace, the man pulls the small cart with its wheels turning slowly, smoke drifts in the background, their clothes sway. |
| 057 | 57 | Dân chạy loạn gánh rơm và bọc đồ đi dọc bờ sông, có người già và trẻ nhỏ | Slow lateral tracking as the refugees walk along the riverside road carrying their bundles, the children walk beside the adults, the bundles sway with each step, smoke drifts over the hills, the river ripples. |
| 061 | 61 | Vị tướng giáp dẫn lính vác bao, cờ trơn, trăng và khói | Slow push-in as the officer and the soldiers behind him march forward in step, the soldiers carry sacks that sway with each step, the plain banners flutter, smoke drifts across the moon. |
| 070 | 70 | Hai người đi giữa, một áo đen, một mặc giáp, hàng lính theo sau | Slow push-in as the two foreground men walk forward side by side at a steady pace, the loose line of soldiers behind them follows in step, the banners flutter, dust drifts. |
| 073 | 73 | Xe ngựa chở hai người ngồi, lính đi bộ hộ tống hai bên | Slow lateral tracking as the horse pulls the cart forward at a calm walking pace, the horse's legs move in a natural regular gait, the soldiers march beside it in step, the cart wheels turn slowly, spear tips tilt together, dust rises. |
| 078 | 78 | Người nông dân và một sĩ quan giáp đi bên ruộng, bò cày phía sau | Slow lateral tracking as the two foreground men walk along the field path side by side, the oxen pull the plough forward slowly in the field behind them, the green crop sways in the wind, the soldiers in the distance walk in line. |
| 113 | 113 | Một người áo nhạt đeo bọc nhỏ bị lính giáp áp giải đi trên phố đêm | Slow lateral tracking as the foreground man and the armored soldier walk forward side by side at a steady pace, the guards behind them follow in step, banners flutter, mist drifts along the street. |
| 126 | 126 | Một ông già râu bạc áo đen đi cùng lính giáp qua cổng, người xem hai bên | Slow push-in as the old man and the armored soldier walk forward together through the gateway at a steady pace, the onlookers at the sides shift slightly, banners flutter, light shifts across the courtyard. |
| 139 | 139 | Một người áo xanh đi tới, phía sau là bóng đen lính cầm giáo trong hành lang | Slow push-in as the foreground man walks forward along the corridor toward the camera, the black silhouettes of the soldiers behind him march in step, the spear tips sway together, the curtains sway, shadows lengthen on the floor. |
| 157 | 157 | Đoàn đưa tang: xe gỗ chở quan tài, người áo trắng đi hai bên, một sĩ quan giáp | Slow lateral tracking as the funeral procession walks forward at a slow steady pace, the wooden cart carries the coffin with its wheels turning slowly, the mourners in white walk beside it, the white banners flutter, mist drifts. |
| 167 | 167 | Dân chạy trong khói, gánh đồ, trẻ con và phụ nữ chạy theo | Slow lateral tracking as the villagers run along the road, the bundles of straw sway on their shoulders, the children run beside the adults, smoke drifts and rolls behind them, dust rises at their feet. |

### Bổ sung (tùy chọn, 02/11/2026): 3 cảnh thêm

Ngoài 20 cảnh trên (đã đủ mức sàn 20 clip). Cảnh 045 có cờ vẽ chữ ở góc phải: prompt không nhắc cờ bay để Veo không sinh thêm chữ.

| Ảnh | Câu | Cảnh (chỉ để tra, KHÔNG dán vào Veo) | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|---|
| 013 | 13 | Chàng trai cưỡi ngựa nâu phi nước kiệu trên bãi cỏ, chim ưng đậu trên cột | Slow lateral tracking as the rider guides the horse forward at a steady trot across the grass, the horse's legs move in a natural regular gait, his sleeves and topknot sway, dust rises at the hooves, the grass sways, the bird stays perched on the post. |
| 045 | 45 | Hai người đàn ông đứng trước hàng lính trong doanh trại | Slow push-in as the two foreground men stand and breathe, their robes and cloak sway gently in the wind, the rows of soldiers behind them shift and a few step forward in line, spear tips tilt together, dust drifts across the road. |
| 082 | 82 | Hai người đứng nhìn nhau qua con sông, hai hàng quân hai bờ | Slow push-in as the two foreground men stand still and look across the river, their sleeves sway in the wind, the long columns of soldiers on the far bank march slowly along the water's edge, spear tips tilt together, ripples run across the river, thin smoke drifts. |
