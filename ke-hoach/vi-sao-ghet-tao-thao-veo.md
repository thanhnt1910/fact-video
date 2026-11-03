# Vì sao cả ngàn năm người ta ghét Tào Tháo? — Clip Veo (nhóm A, 24 clip)

Soạn 03/11/2026 sau khi xem cả 74 ảnh ở cỡ lớn. **Tổng ảnh: 74. Số clip Veo: 24 (≥ 20). Số cảnh hoạt hình nhẹ: 16. Số ảnh tĩnh: 34.**
Chọn theo tầm quan trọng của câu chuyện (mở đầu, lúc bước ngoặt, câu hỏi cuối), mỗi clip có diễn biến rõ ràng theo mốc thời gian (0-3 giây, 3-6 giây, 6-8 giây) hoặc chuỗi hành động cụ thể: người làm gì, phản ứng ra sao, máy quay đi thế nào, kèm chuyển động phụ (gió, khói, nước, vạt áo, ánh sáng) để cảnh sống động mà ảnh không bị vẽ lại. Có 21 clip dự phòng cho trường hợp Veo vẽ lại khung đầu hoặc mọc thêm tay.
Lưu clip ở `assets/clips_2d/TQ10/NNN.mp4` (NNN = số câu = số ảnh), kèm `danh_sach.json`. Chủ kênh tạo clip trong Google Flow.

## Nhóm A — Veo (24 clip)

Chọn "Frames to Video", tải ảnh `assets/anh_2d/TQ10/NNN.jpg` làm khung đầu, 16:9, 8 giây, tắt âm nếu có. Dán tiền tố rồi dán prompt. Mỗi ảnh một clip. **Làm thử 3 clip trước: 003 (đám trẻ reo hò), 029 (người đi), 065 (gió biển)**, thấy ổn mới làm các clip còn lại. Cột `rủi ro` trong `ke-hoach/veo/TQ10_clips.json` cho biết clip nào hay lỗi (tay, ngựa, đám đông).

**Tiền tố dán vào MỌI prompt:**

`Animate this exact 2D ligne claire illustration. Keep the same drawing style, flat colours, outlines, and exactly the same characters, faces, clothes and objects. Keep exactly the same people in the foreground. Han dynasty clothing only, no modern objects, no new foreground people, no text, no letters, no camera cut, no zoom into faces, silent, no music, no speech. Motion:`

**Quy tắc về tên:** prompt Veo TUYỆT ĐỐI không nêu tên riêng của người thật nổi tiếng, chỉ mô tả hình dáng. Kiểm bằng `python kiem_prompt_veo.py ke-hoach/vi-sao-ghet-tao-thao-veo.md`.

**Quy tắc chuyển động:** người bước đều, áo và khăn bay theo gió; ngựa đi bước thường; không cảnh chém, không máu. Clip nào mọc thêm người, thêm tay, mặt méo, ngựa méo hoặc thừa chân, ảnh đổi nét vẽ thì bỏ, dùng ảnh tĩnh. Veo xuất 720p thì dựng lại 1080p/30 fps.

| Ảnh | Câu | Cảnh (chỉ để tra, KHÔNG dán vào Veo) | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|---|
| 001 | 1 | Con phố thành thị thời Tống buổi sáng, người đi lại, quán có mái vải, một xe kéo | Camera glides forward down the middle of the street. A shopkeeper at the left stall sweeps his arm to wave a passer-by over, two men at the roadside table clink cups and laugh, the cart puller leans into his load and the cart rolls on, the awnings snap in a gust and the crowd in the far background thickens and flows toward the camera. |
| 002 | 2 | Người kể chuyện áo nâu đứng trên bục gỗ, sáu đứa trẻ ngồi quanh | 0-3s: the storyteller strikes a pose, one arm thrust high, then swings it down in a sweeping arc as if a hero fell. 3-6s: the children gasp together, lean forward and shuffle closer on their knees, heads snapping toward his hand. 6-8s: he lowers his voice with a hush gesture and the children freeze wide-eyed. Sleeves swing the whole time; camera pushes in on the group. |
| 003 | 3 | Lũ trẻ ngồi thành hàng, đứa khóc, đứa giơ nắm tay reo hò | 0-3s: the two children with tears sniff, rub their eyes with both sleeves and slump. 3-6s: the others explode into cheers, fists pumping up and down, mouths wide open, heads thrown back, topknots bouncing, dust puffing from the ground. 6-8s: the crying ones look sideways at the cheering ones and pout. Camera shakes lightly with the excitement. |
| 012 | 12 | Người trẻ áo xanh đậm đối mặt ông già tóc râu bạc trong sân | 0-3s: the elder sizes the young man up, eyes moving slowly from his face to his belt and back, stroking nothing, shoulders still. 3-6s: he leans a little closer and speaks a short sentence, mouth moving, then gives a firm nod. 6-8s: the young man's frown breaks into a pleased grin, chest lifting. Camera drifts sideways between them; sleeves and sashes sway, dry leaves skitter across the paving. |
| 014 | 14 | Người viết sử ngồi trước bàn thấp trong sân, cầm bút | 0-3s: the scholar dips his brush and draws one long downward stroke along the scroll. 3-6s: he lifts the brush, glances up at the sky as if recalling a fact, then bends and writes quickly. 6-8s: he sets the brush down and straightens his back with a deep breath. Camera drifts right across the courtyard; grass sways, a breeze flutters his sleeve. |
| 021 | 21 | Dân chạy loạn đi dọc kênh, xe bò chở đồ, khói ở làng xa | The line of villagers trudges forward with real weight: ox carts lurch and wheels turn, a mother shifts a bundle from one shoulder to the other, an old man leans on a staff, a child looks back over his shoulder. Camera tracks sideways at walking speed; grey smoke columns bend in the wind and the canal water ripples. |
| 023 | 23 | Người đàn ông cao áo đen đứng cạnh cậu bé ngồi bên bàn | 0-3s: the tall man leans forward on the table, planting his palm, and fixes the child with a hard stare. 3-6s: the child shrinks a little, eyes darting up to him, small fingers curling on the table edge. 6-8s: the man straightens up and glances away toward the window while the child keeps watching him. Camera creeps in; light slides across the wall. |
| 027 | 27 | Người áo đen đưa chiếc mũ đen cao cho người áo xám đang đưa tay đón | 0-3s: the man in black lifts the tall hat in both hands and holds it out with ceremony. 3-6s: the man in grey hesitates, then reaches out and takes hold of the cord. 6-8s: the man in black releases it with a firm nod and steps back a half pace. Camera pushes in on the hat between them; sleeves sway, wind tugs the sashes. |
| 028 | 28 | Người chèo thuyền trên sông, buồm trắng, thuyền khác ở xa | The boatman rows with two strong strokes, the boat surges forward and the white sails belly out; ripples fan out behind the hull, spray glitters, a far boat crosses the frame, mist rolls over the water and a bird sweeps past. Camera tracks alongside the boat at its speed. |
| 029 | 29 | Người áo xám đi giữa con hẻm lát đá | The man strides toward the camera with a confident, brisk walk, arms swinging, sash and trouser hems whipping; he glances left at a doorway, then back ahead. Camera dollies backward in front of him at his speed; long shadows slide along the paving and a leaf tumbles across the path. |
| 034 | 34 | Người râu ngắn viết ban đêm bên đĩa dầu có ngọn lửa nhỏ, cạnh một bọc vải | 0-3s: the writer jots short quick strokes, brush moving left to right, then pauses to think, eyes lifting to the flame. 3-6s: the oil-dish flame flares and shrinks in a draught, warm light pulsing across his face and the bundle. 6-8s: he rubs his tired eyes with one hand and resumes writing. Stars twinkle; the camera inches in. |
| 036 | 36 | Người áo dài đi khuất dần trên con đường đất ướt, nhà đổ ở xa | The man walks away from the camera with a heavy, slow-footed stride, shoulders sagging, robe hem swinging; he steps through a puddle and rings spread, pauses for one beat to glance at the ruined building in the haze, then walks on. Mist rolls between the rooftops. Camera follows behind at his pace. |
| 038 | 38 | Người lữ khách đeo bó thẻ tre sau lưng đi giữa phố núi lúc chạng vạng | The traveller strides toward the camera with a steady, determined walk, the bundle on his back bouncing slightly with each step, sandals kicking up dust, sleeves swaying; he adjusts the strap with one hand and keeps going. Dusk mist rolls down from the mountains behind him. Camera backs away smoothly. |
| 045 | 45 | Người áo đen đi trên lối giữa dãy nhà, hai đứa trẻ đi hai bên | The man and the two children walk toward the camera in step; the child on the left tugs his sleeve and points to the sky, the man bends his head to listen and nods, the child on the right skips one step ahead. Bamboo and pine boughs sway, a bird flies across, camera tracks sideways with them. |
| 048 | 48 | Người béo cười, áo nâu, đứng bên lan can cầu, kênh và hoàng hôn | 0-3s: the smiling man leans on the railing and takes a deep breath of the evening air, chest rising. 3-6s: he lifts one hand to stroke his moustache and gives a pleased nod toward the sunset. 6-8s: he laughs softly, shoulders shaking. Golden light ripples on the canal, his broad sleeve and sash stir in the breeze; camera drifts gently left. |
| 050 | 50 | Ông già áo nâu đi ngược lưng về phía xa dọc bờ kênh | The old man walks away from the camera with the small deliberate steps of age, one hand resting behind his back, robe swinging; he pauses a beat and tilts his head toward the water, then walks on. Canal water ripples, tree leaves flutter, shifting light slides along the stone embankment. Camera follows behind. |
| 051 | 51 | Hai cậu bé áo xám chĩa gậy vào nhau (đấu giả), một cậu áo vàng nâu bên trái cầm gậy lao tới, bốn đứa nhỏ đứng xem bên phải | The two boys in grey clash their wooden sticks in a mock duel with no contact on their bodies: stick taps stick, the left boy lunges and the right boy skips back, then they swap sides and circle each other, scowling playfully. The boy at the far left stamps forward with his stick raised, and the four small onlookers on the right flinch, gasp and bounce on their toes. Dust puffs at their feet; camera drifts sideways. |
| 052 | 52 | Người kể chuyện dang hai tay trước quán gỗ sáng đèn | 0-3s: the storyteller throws both arms wide, chest out, mouth open in a bellow. 3-6s: he sweeps both arms in with a dramatic flourish, then crouches slightly and leans toward the audience as if sharing a secret. 6-8s: he straightens up and spreads one hand to the side. Long sleeves swing, warm light flickers through the lattice windows; camera pushes in. |
| 055 | 55 | Người viết ngồi bên bàn thấp, cuộn thẻ, hộp gỗ, cửa sổ chấn song | 0-3s: the writer draws the brush down the scroll in smooth strokes, pauses and tilts his head, thinking. 3-6s: he glances up toward the window, then writes a line quickly. 6-8s: he lifts the finished line to look at it and gives a small satisfied exhale. Window light shifts across the mat; a breeze moves his sleeve; camera drifts right. |
| 062 | 62 | Người cưỡi ngựa nâu sẫm đi trên con đường làng | The rider urges the dark horse forward at a steady walk; its hooves land in clear four-beat rhythm, head bobbing, mane and tail swaying; the rider sits upright, scanning left and right along the lane, his sleeves fluttering. Dust rises at the hooves, mist rolls along the walls. Camera tracks sideways at the horse's pace. |
| 064 | 64 | Ông già râu bạc cười, giơ cây gậy nhỏ, nắng sớm phía sau | 0-3s: the laughing old man raises the small stick high. 3-6s: he brings it down with a flourish, as if sealing a punchline, then spreads his other hand to the side and grins. 6-8s: he leans in, whispering conspiratorially. Sleeves swing, sunrise glows behind him, dust motes float in the beams; camera pushes in. |
| 065 | 65 | Người áo choàng đen đứng trên bãi biển, sóng vỗ | Strong sea wind: the man's dark cloak and sleeves snap behind him; waves surge in and break around his feet in white foam; he turns his head slowly from the sea to the horizon and squares his shoulders. Clouds race across the sky, spray drifts through the air. Camera pushes in, trembling slightly in the wind. |
| 073 | 73 | Người áo đen đứng chính diện giữa ngõ, nhìn thẳng | The man stands firm facing the camera: he draws a deep breath, his chest rising, blinks once, then fixes the viewer with a steady direct gaze; his sleeves and sash stir in a gust and cloud shadows sweep across the walls behind him. Camera creeps in by a hair. |
| 074 | 74 | Sáu đứa trẻ ngồi hàng dưới gốc cây lớn | 0-3s: the six children under the tree glance at each other, whispering, one nudges her neighbour. 3-6s: they turn their heads toward the camera one after another with big questioning eyes, a boy tilts his head. 6-8s: they all hold still, waiting for an answer, one child swings her feet. Leaves rustle, dappled light flickers across them; camera drifts closer. |

## Nhóm B — hoạt hình nhẹ bằng `anim_nhe.py` (16 cảnh, không dùng AI)

Cảnh vắng người; cần `ke-hoach/nhan-vat/TQ10_nhe.json` (khung chọn tay khi đã có ảnh).

| Ảnh | Chuyển động nhẹ |
|---|---|
| 006 | sương trôi dọc phố, đèn cửa sổ nhấp nháy rất nhẹ |
| 009 | trăng sáng, mây trôi chậm, lá cây rung |
| 011 | lúa và cỏ bên đường đung đưa, mây chiều trôi |
| 019 | mặt nước hai bên con đường gợn sóng |
| 020 | khói bốc lên từ xa, cỏ rung, mây trôi |
| 024 | bụi và sương bay dọc con đường vắng |
| 031 | cỏ đồng rung, mây trôi, cờ nhỏ trên thành xa |
| 032 | hai ngọn lửa trong chậu đồng nhảy nhẹ |
| 042 | khói bếp từ các mái nhà bay lên, nước kênh gợn |
| 047 | khói bay trên bờ sông, mặt nước gợn |
| 058 | sương và bụi trôi trên đường, cỏ rung |
| 061 | lửa bếp nhảy, hơi nước bốc lên từ nồi, con lợn dậm chân nhẹ |
| 063 | sương trôi, lá khô bay qua dấu chân |
| 066 | sóng biển vỗ, mặt trời sáng lên dần |
| 071 | ngọn lửa trên sân khấu nhảy, tấm màn đỏ lay |
| 072 | khói đen cuộn chậm bên bờ mương, sương trôi |

## Còn lại — ảnh tĩnh (34 ảnh)

004, 005, 007, 008, 010, 013, 015, 016, 017, 018, 022, 025, 026, 030, 033, 035, 037, 039, 040, 041, 043, 044, 046, 049, 053, 054, 056, 057, 059, 060, 067, 068, 069, 070
