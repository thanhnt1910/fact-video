# Tam Quốc tập 3 — Ảnh cần vẽ, clip Veo, hoạt hình nhẹ

Soạn từ `tam-quoc-tap-3-kich-ban.md` (kịch bản chờ chủ kênh duyệt). Sửa kịch bản thì rà lại danh sách theo số câu. Số ảnh = số câu − 1 từ câu 4 trở đi (câu 3 dùng lại ảnh 002).

## Quy ước phân nhóm (chủ kênh chốt, áp dụng mọi tập; ghi ở `CLAUDE.md`)

- **Nhóm A — Veo (mỗi tập tối thiểu 20 clip):** chỉ các cảnh chính có **người di chuyển nhiều** (hành quân, hàng quân, dàn trận, đám đông, người bước đi). Làm bằng Google Flow / Veo, ảnh → video.
- **Nhóm B — tool dựng đang có (`anim_nhe.py`, không dùng AI):** cảnh vật, đồ vật, cảnh vắng người; chỉ cây cỏ, cờ, nước, lửa, khói, đèn, sương chuyển động nhẹ.
- **Còn lại — ảnh tĩnh:** cảnh người đứng yên hoặc có tương tác tay; dùng chuyển máy chậm sẵn của tool dựng, không làm clip.

## Cần bao nhiêu

- **Ảnh tĩnh: 85 ảnh** (mỗi lời kể một ảnh, mỗi ảnh dùng một lần). Video ngắn dùng lại 9 ảnh, không vẽ thêm. Lưu `assets/anh_2d/TQ3/001.jpg` … `085.jpg`.
- **Veo (nhóm A): 20 clip**, lưu `assets/clips_2d/TQ3/NNN.mp4`.
- **Hoạt hình nhẹ (nhóm B): 18 cảnh**, chạy `python anim_nhe.py TQ3 <số ảnh,…>` sau khi có ảnh; cần tạo `ke-hoach/nhan-vat/TQ3_nhe.json` (khung vùng chuyển động chọn tay khi đã có ảnh, như `TQ2_nhe.json`).
- **Giữ ảnh tĩnh:** 47 ảnh (ảnh 055 chuyển từ nhóm B sang vì có người cưỡi ngựa nhỏ).
- **Ảnh bìa:** tạm hoãn.

## Cách vẽ ảnh

- `ke-hoach/tam-quoc-tap-3-prompt-anh.txt`: 85 prompt đầy đủ, dán nguyên (đã gồm nhân vật và phong cách). `ke-hoach/nhan-vat/TQ3_anh.json`: cùng nội dung cho pipeline.
- Tuổi nhân vật theo năm 190: Lưu Bị 29, Quan Vũ 31, Trương Phi 28, Tôn Kiên khoảng 35 (tập 2 ghi 45, theo sử ông sinh 155, mất 192 lúc 37 tuổi; đã vẽ rồi thì dùng ảnh cũ làm tham chiếu mặt).
- Nhân vật mới cần khóa mặt trước (vẽ một ảnh rồi làm tham chiếu): Tôn Kiên, Lữ Bố, Hồ Chẩn, Viên Thuật, Đinh Nguyên, Vương Doãn, Hàn Phức, Tổ Mậu.
- Cảnh nhạy cảm xử lý bằng cảnh vắng người hoặc nhìn từ sau: giết Thiếu đế (ảnh 014), chém Hoa Hùng (037, 039), đốt Lạc Dương (043), đào lăng (044), Tôn Kiên chết (055 đến 057), Lữ Bố giết Đổng Trác (075, 076). Không máu, không cảnh chém. Ngựa được vẽ bình thường.

## Nhóm A — Veo (20 clip, người di chuyển nhiều)

Chọn "Frames to Video", tải ảnh làm khung đầu, 16:9, 8 giây hoặc ngắn nhất, tắt âm nếu có. Dán tiền tố rồi dán prompt. Mỗi ảnh một clip. Làm thử 3 clip (ảnh 026, 062, 036) trước.

**Tiền tố dán vào MỌI prompt:**

`Animate this exact 2D ligne claire illustration. Keep the same drawing style, flat colours, outlines, and exactly the same characters, faces, armour, clothes and weapons. Keep exactly the same people in the foreground. Han dynasty soldiers on foot only, no horses, no modern objects, no new foreground people, no text, no letters, no camera cut, no zoom into faces, silent, no music, no speech. Motion:`

**Quy tắc về tên: prompt Veo TUYỆT ĐỐI không nêu tên riêng của người thật nổi tiếng (nhân vật lịch sử), vì vi phạm chính sách của Veo và clip bị từ chối.** Chỉ mô tả chung ("the foreground man", "the officer", "the two men"); ảnh khung đầu đã mang sẵn khuôn mặt. Kiểm bằng `python kiem_prompt_veo.py ke-hoach/tam-quoc-tap-3-anh-va-veo.md`.

**Quy tắc:** người tiền cảnh chỉ thở, đổi trọng tâm, bước đi đều, áo khăn bay theo gió; hàng quân chuyển động tập thể đơn giản (tiến vài bước, giáo nghiêng cùng nhịp, cờ bay, bụi); không cảnh chém nhau, không máu; clip nào mọc thêm người, thêm tay, mặt méo, vũ khí đổi hình, ngựa méo chân hoặc thừa chân thì bỏ, dùng ảnh tĩnh. Veo xuất 720p thì dựng lại 1080p/30 fps cùng hạt phim.

| Ảnh | Câu | Cảnh (chỉ để tra, KHÔNG dán vào Veo) | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|---|
| 008 | 9 | Một tướng cao lớn nhìn từ sau, cầm giáo, bước qua cửa trong đêm | Slow push-in behind him as he steps forward through the doorway into the corridor at a steady pace, the torch flames flicker and shadows shift, his cloak sways. No face visible. |
| 009 | 10 | Hàng lính gác kinh đô đứng trong sân lúc bình minh, một sĩ quan nhìn từ sau | Slow push-in behind the foreground officer, the ranks of guards stand firm and their spear tips sway slightly in unison, plain banners flutter, dawn light brightens, dust drifts across the courtyard. |
| 016 | 17 | Một thủ lĩnh đứng trên đài gỗ, cờ trơn nhiều màu phía sau | Very slow push-in toward the platform, the plain banners behind him ripple in the wind, he stands still and breathes, dust drifts in the background. |
| 017 | 18 | Hàng lính ngồi quanh nồi nguội trong trại sườn đồi, một sĩ quan ngồi nhìn từ sau | Slow push-in, thin smoke curls up from the cooking pots, the seated soldiers shift their weight slightly, banners flutter, the foreground man stays seated and breathes. |
| 018 | 19 | Một tướng đội khăn đỏ nhìn về phía bắc, đồi núi phía sau | Very slow push-in, his red headband and sleeves move in the wind, mist drifts over the hills behind, he stands still and breathes. |
| 019 | 20 | Thuyền nhỏ trên sông với một thiếu niên đứng đầu thuyền và người cha ngồi cạnh | Slow lateral drift along the river, the boat rocks very slightly, ripples spread on the water, mist drifts, the two people stay in place. |
| 021 | 22 | Một tướng nhìn từ sau trên đỉnh đồi, nhìn xuống thung lũng sông lúc bình minh | Slow push-in behind him as he strides a few steps along the hilltop, his cloak and headband stream in the wind, mist rolls through the valley below. No face visible. |
| 022 | 23 | Một quan văn đeo bọc vải trên vai, rời cổng thành | Slow lateral tracking as he walks out through the city gate at a steady pace with the bundle on his shoulder, the gate flags flutter, dust rises at his feet. |
| 026 | 27 | Lính bộ binh tản trên đồng bụi, quân địch tiến lại từ xa | Slow lateral drift to the right, dust rolls across the field, the distant enemy ranks advance a few steps in unison, spear tips tilt together, banners flutter. |
| 027 | 28 | Một nhóm khoảng mười người xông qua hàng lính mỏng trong bụi mù | Slow push-in, thick dust swirls, the small group presses forward together through the thin line, spears sway, nobody comes forward into the foreground. |
| 029 | 30 | Con đường tắt đầy bụi dẫn vào đồi, đám bụi quân truy đuổi ở xa | Static camera with a slow push-in, the dust cloud on the plain drifts and rolls, grass sways at the roadside, clouds drift. |
| 032 | 33 | Hàng quân dàn lại lúc hoàng hôn, cờ đỏ cao ở đầu hàng, nhìn từ sau | Slow push-in, the ranks stand firm while spear tips and the tall red banner sway in the wind, dust glows orange in the dusk light. |
| 036 | 37 | Đoàn quân vỡ hàng, vấp ngã trên đường, bụi mù, cờ nghiêng | Slow tracking shot along the column, the soldiers stumble and bunch up in unison, dust rises, banners tilt and flutter. |
| 037 | 38 | Một tướng nhìn từ sau đứng trên gò, giáo dựng, phía trước chỉ có bụi và cờ đỏ | Slow push-in behind him, dust and smoke drift across the field in front, the banners flutter, he stays still and breathes. |
| 053 | 54 | Trại liên quân trên sườn đồi, nhiều cờ trơn nhiều màu, hai chỉ huy đứng quay lưng nhau | Slow lateral drift along the ridge, the many coloured banners flap in the wind, tent canvas ripples, the two men stay still. |
| 059 | 60 | Trại quân dỡ lều, xếp lên xe, lính thu dọn, nhìn từ xa | Slow lateral drift along the camp, canvas ripples, the soldiers move boxes onto the carts at the same slow pace, banners flutter, dust drifts. |
| 062 | 63 | Cầu đá bắc qua sông, hai đạo quân đứng hai bờ, cờ xanh bên trái, cờ đỏ bên phải | Slow descending crane move over the river, the two armies hold their ranks on the banks, banners flutter, spear tips sway, morning mist drifts. |
| 071 | 72 | Một thị nữ nhìn từ sau, cầm đèn dầu đi dọc hành lang cung điện ban đêm | Slow push-in behind her, the lamp flame flickers and shadows shift on the walls, she walks forward at a steady pace. |
| 073 | 74 | Lính gác cổng cung đứng thành hàng, nhìn từ sau, ánh đuốc | Slow push-in, the torch flames flicker, the guards stand still and breathe, banners ripple. |
| 080 | 81 | Hai người cao lớn canh cửa lều ban đêm, cầm đuốc, giáo dựng | Very slow push-in, torch flames flicker and change the light on their faces, the spears stay upright, they breathe and do not move their arms. |

## Nhóm B — hoạt hình nhẹ bằng tool dựng (`anim_nhe.py`, không dùng AI)

Không dùng Veo hay Kaggle (video AI giật, dễ biến dạng). Chạy `python anim_nhe.py TQ3 <số ảnh,…>`; vùng chuyển động xác định theo màu (cỏ, lá, nước, lửa) và khung chọn tay trong `TQ3_nhe.json`.

| Ảnh | Câu | Phần chuyển động |
|---|---|---|
| 003 | 4 | ngọn đèn dầu, ánh sáng chớp nhẹ |
| 004 | 5 | sương trôi giữa vách núi, bụi cây |
| 013 | 14 | ngọn đèn đồng, rèm khẽ lay |
| 030 | 31 | lá cờ đỏ trên cột cháy, cỏ cao, khói mỏng |
| 041 | 42 | ngọn đèn dầu |
| 042 | 43 | sương mù ở cửa ải |
| 043 | 44 | lửa và khói đen từ thành cháy |
| 044 | 45 | ánh đuốc trong cổng lăng, bụi, lá |
| 045 | 46 | cờ trên tháp cổng, ánh sáng bình minh |
| 054 | 55 | lá cờ đỏ, khói bụi, mây |
| 058 | 59 | mặt sông, thuyền nhỏ, sương |
| 066 | 67 | cờ trên các tháp, bụi đường |
| 074 | 75 | ánh sáng qua cửa điện, bụi lơ lửng |
| 079 | 80 | sương dọc tường thành lúc chiều tối |
| 081 | 82 | ngọn đèn dầu |
| 082 | 83 | khói mỏng, vải cờ rơi lay nhẹ, sương |
| 083 | 84 | khói mỏng, con quạ, tro bay |
| 085 | 86 | cỏ ven đường, sương, nắng lên |

## Giữ ảnh tĩnh (47 ảnh)

Ảnh: 001, 002, 005, 006, 007, 010, 011, 012, 014, 015, 020, 023, 024, 025, 028, 031, 033, 034, 035, 038, 039, 040, 046, 047, 048, 049, 050, 051, 052, 055, 056, 057, 060, 061, 063, 064, 065, 067, 068, 069, 070, 072, 075, 076, 077, 078, 084.

Đây là cảnh người đứng yên hoặc có tay cầm vật; không làm clip để khỏi biến dạng.
