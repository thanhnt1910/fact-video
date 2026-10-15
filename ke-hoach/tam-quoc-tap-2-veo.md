# Tam Quốc tập 2 — Prompt tạo clip chuyển động (Google Flow / Veo, ảnh → video)

Cách dùng: chọn "Frames to Video" (ảnh → video), tải ảnh `assets/anh_2d/TQ2/NNN.jpg` làm khung đầu, dán **tiền tố** rồi dán prompt chuyển động của ảnh đó, tỉ lệ 16:9, 8 giây (hoặc ngắn nhất có thể), tắt âm thanh nếu có tùy chọn. Mỗi ảnh chỉ làm một clip.

Khác tập 1: **ưu tiên cảnh quân đội, đánh trận và cảnh có người**, làm cảnh vật sau cùng. Kênh kể chuyện người và chiến sự nên clip phải có người, có hàng quân, có cờ và bụi chuyển động.

## Tiền tố dán vào MỌI prompt

`Animate this exact 2D ligne claire illustration. Keep the same drawing style, flat colours, outlines, and exactly the same characters, faces, armour, clothes and weapons. Keep exactly the same people in the foreground. Han dynasty soldiers on foot only, no horses, no modern objects, no new foreground people, no text, no letters, no camera cut, no zoom into faces, silent, no music, no speech. Motion:`

## Quy tắc để khỏi biến dạng (đặc biệt với đám đông)

- Người ở tiền cảnh: chỉ thở, đổi trọng tâm nhẹ, bước đi đều, áo và khăn bay theo gió. Không bắt họ làm động tác tay phức tạp (rót, trao, viết, cầm đồ nhỏ).
- Hàng quân ở hậu cảnh: cho chuyển động tập thể rất đơn giản, đồng loạt: bước tiến vài bước, giáo nghiêng cùng một nhịp, cờ bay, bụi bốc lên. Không cho từng người làm việc riêng.
- Đánh trận: chỉ dùng cảnh hai bên đối mặt, tiến lên, dàn trận, rút lui. **Không đòi cảnh chém nhau cận cảnh** (AI hay vẽ sai tay, vũ khí, dính người vào nhau). Sức nặng của trận đánh nằm ở khói, bụi, cờ, tiếng quân và nhịp cắt dựng.
- Không máu, không thương tích, không cảnh giết người (đúng `review_checklist.md`).
- Xem từng clip: nếu có thêm người ở tiền cảnh, thêm tay, mặt méo, vũ khí đổi hình hoặc ngựa xuất hiện thì bỏ clip và dùng lại ảnh tĩnh.
- Veo xuất 720p/24 fps thì dựng lại 1080p/30 fps, thêm cùng hạt phim và bộ lọc màu như ảnh tĩnh. Đặt đường dẫn clip vào cảnh tương ứng trong `scripts/TQ2.json` theo cách của TQ1 (`assets/clips_2d/TQ2/NNN.mp4`).
- Làm thử 3 clip (052, 064, 081) trước để xem chất lượng rồi mới làm tiếp.

## Nhóm A — quân đội và đánh trận (làm trước, 16 clip)

| Ảnh | Cảnh (theo lời kể) | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|
| 018 | Lưu Bị ra trận ở Hạ Bì, hai bên giáo chĩa vào nhau | Slow push-in. The two foreground men hold their stance and breathe, the rows of spearmen behind them sway and shift their spears together, dust and smoke drift across the field from left to right. |
| 021 | Giặc kéo vào cổng huyện, quân huyện rút lui | Slow lateral drift to the right. Dust and smoke roll through the broken gate, the rear ranks surge forward a few steps in unison, spear tips tilt together, the two foreground men stay in place. |
| 025 | Hai đạo quân đối mặt trên đồng bằng | Slow forward dolly down the empty lane between the two armies, red banners on the left and blue banners on the right flutter strongly, spear tips sway in unison, dust rises along the lane. |
| 052 | Quân biên cương của Đổng Trác kéo vào cổng Lạc Dương | Static camera with a slow push-in. The long ranks march forward a few steps in step, tall dark-red banners ripple in the wind, dust rises from their boots, the foreground soldier stands still and breathes. |
| 056 | Doanh trại liên quân trên sườn đồi | Slow lateral drift along the ridge, the many coloured banners flap in the wind, tent canvas ripples, the formation stays in ranks, the officer in the foreground breathes slightly. |
| 059 | Viên Thiệu được tôn làm minh chủ | Slow push-in toward the platform, the ranks behind stand firm while their spear tips and banners sway in the wind, the two men on the platform stay almost still and breathe. |
| 061 | Quân dàn trước cửa ải Hổ Lao | Slow push-in toward the pass gate through mist, the mist drifts between the cliffs, the banners flutter, the ranks of soldiers lift their spears slightly together, the foreground soldier stays still seen from behind. |
| 064 | Tôn Kiên dẫn quân tiến lên | Slow tracking shot, the leader strides forward at a steady pace, the ranks behind advance with him in step, the tall red banner flutters, dust is kicked up. Same leader, same spear, no new fighters. |
| 065 | Đoàn người rời Lạc Dương đang cháy | Static camera with a slow upward tilt toward the burning city, flames flicker and black smoke rolls across the sky, embers float, the crowd stands still while cloth and banners move in the wind. |
| 066 | Liên quân ngồi chờ, không ai tiến | Slow push-in, thin smoke curls up from the cold cooking pots, the rows of idle soldiers shift their weight slightly, banners flutter, the foreground man stays seated and breathes. |
| 067 | Quân Tôn Kiên hành quân lên bắc | Slow tracking shot walking backwards in front of the column, the soldiers march forward at a steady pace in step, spears upright, the red banner at the head flutters, dust rises from the road. |
| 075 | Đoàn quân tiến về cửa ải lúc hoàng hôn | Slow forward drift behind the foreground soldier, the column marches ahead toward the mountain pass, banners flutter, dust glows orange in the setting sun, clouds drift slowly. |
| 079 | Nhiều đạo quân tụ về hai bờ sông | Slow descending crane move over the valley, columns of tiny soldiers move forward and converge along the river, morning mist drifts, banners flutter, the two foreground commanders stay still. |
| 081 | Quân của Tào Tháo thua trận, rút lui bên sông | Slow tracking shot alongside the two foreground soldiers as they walk wearily, the long retreating line behind them trudges forward, the torn blue banners flutter, dust drifts, evening light dims slowly. |
| 016 | Lưu Bị xin ghi tên đi lính | Slow push-in, the long line of waiting men shuffles forward by a small step, banners and cloth flutter, the seated officer and Liu Bei stay almost still. |
| 027 | Lưu Bị nhậm chức, dân huyện đón | Slow push-in, the lines of townspeople and officials hold their bows, the river in the background glides slowly, clouds drift, Liu Bei stands still and breathes. |

## Nhóm B — cảnh có người, chuyển động nhẹ (làm sau nhóm A, cần soi kỹ)

| Ảnh | Cảnh | Prompt |
|---|---|---|
| 003 | Lưu Bị rời cổng huyện trong đêm, nhìn từ sau | Slow push-in behind him as he walks away along the moonlit road, cloth bundle swaying, clouds drift across the moon. |
| 014 | Bóng người đi một mình trên đường | Slow lateral drift, the small figure keeps walking at a steady pace, moonlight shifts on the road, grass sways. |
| 019 | Lưu Bị rời gian sảnh trống | Static camera, grey light shifts slowly through the window, he stands in the doorway and breathes slightly, dust floats in the light. |
| 031 | Quan Vũ, Trương Phi đứng canh lều | Very slow push-in, torch flames flicker and change the light on their faces, the spears stay upright, they breathe and do not move their arms. |
| 033 | Quan Vũ, Trương Phi bên đống lửa | Slow push-in, the campfire flames dance and light their faces unevenly, sparks rise, they stay seated and still. |
| 040 | Ba người ăn chung một nồi | Static camera, steam curls up from the pot, the small lamp flame flickers softly, the three men breathe and stay seated. |
| 041 | Ba bóng người đi về phía hoàng hôn | Slow forward dolly behind the three men as they walk side by side, dust rises at their feet, the sunset glow brightens slowly. |
| 050 | Hai thiếu niên bên bờ sông đêm | Static camera with a slow push-in from behind, reeds sway, moonlight shimmers on the water, the two boys stand still and breathe. |
| 057 | Tào Tháo nhìn lại trên đường đêm | Slow push-in, a light wind moves his sleeves, clouds drift across the night sky, he stays still. |
| 058 | Tào Tháo trước hàng giáo | Slow push-in, the planted spears stay still, dust and wind move his sleeves slightly, he stays still. |
| 048 | Hoạn quan nấp ở hành lang cung | Slow push-in down the corridor, torch flames flicker and long shadows shift, the small figure far down the corridor keeps walking away, the eunuch stays still. |
| 051 | Đổng Trác đứng giữa doanh | Very slow push-in, his cloak moves in a light wind, dust drifts behind him, he stays still. |
| 053 | Đổng Trác và vị vua trẻ | Very slow push-in, light flickers across the room, the two men stay still and breathe. |
| 062 | Lưu Bị nhìn về ải Hổ Lao | Slow push-in behind him, mist drifts across the valley toward the far pass, his clothes move slightly in the wind. |

## Nhóm D — hoạt hình nhẹ, không dùng AI (`anim_nhe.py`, 16 cảnh, không trùng Nhóm A và B)

Cảnh chỉ có chuyển động nhỏ của cây cỏ, hoa, cờ, nước, lửa: **không dùng Veo hay Kaggle**, vì video AI bị giật và dễ biến dạng. `python anim_nhe.py TQ2 <số>` dịch chính các điểm ảnh của bức tranh theo một hàm sóng liên tục (1080p, 24 fps, 8 giây), người và vật cứng đứng yên. Cấu hình vùng chuyển động: `ke-hoach/nhan-vat/TQ2_nhe.json`.

| Ảnh | Phần chuyển động |
|---|---|
| 004 | cành cây trơ, cỏ ven đường |
| 006 | ngọn đèn dầu, ánh sáng chớp nhẹ |
| 009 | hai ngọn nến |
| 010 | tán cây, cỏ trước nhà |
| 012 | cỏ trên cánh đồng quanh cột mốc |
| 013 | hai ngọn đuốc |
| 015 | tán cây, cỏ bên đường |
| 022 | tán cây dâu, cỏ |
| 034 | hoa đào |
| 042 | lá cờ ở tháp cổng, cỏ |
| 047 | ngọn nến |
| 063 | hai lá cờ trên thành, cỏ |
| 071 | tán cây dâu, cỏ |
| 078 | tấm vải đen treo ở lều |
| 082 | mặt sông, cây bên bờ |
| 085 | ngọn nến |

Ảnh 016, 056, 065, 079 vốn cũng có cờ, lửa, nước nhưng thuộc Nhóm A (có người, có quân), nên giữ ở Nhóm A, không làm hoạt hình nhẹ.

## Nhóm C — KHÔNG làm clip (giữ ảnh tĩnh)

Có tương tác tay hoặc chi tiết nhỏ dễ biến dạng: 002, 008, 013, 015, 020, 023, 024, 026, 032, 037, 038, 045, 046, 070, 076, 077, 078, 085.
Cảnh vật, đồ vật (làm sau cùng nếu còn lượt): 001, 004, 005, 006, 007, 009, 010, 012, 022, 042, 047, 054, 055, 063, 068, 072, 073.

## Ghi chú

- Chọn clip nào làm trước theo thứ tự lời kể: mở đầu (003, 014, 019), Bình Nguyên (016, 018, 021, 025, 027), kinh đô và liên quân (048, 052, 056, 059, 061, 064–067, 079, 081), kết (075).
- Với các ảnh nhóm A, đoạn clip nên dài đủ cho 2 câu lời kể; nếu hết clip thì giữ khung cuối vài giây, như cách ST3 và TQ1.
- Ngựa: ảnh TQ2 hiện không vẽ ngựa (dễ sai chân, và thời Hán chưa có bàn đạp). Prompt Veo cũng không thêm ngựa. Nếu sau này cần kỵ binh (quân Lương Châu của Đổng Trác), nên vẽ từ xa và để Veo chỉ làm bụi, cờ.
