# Chu Du có thật sự bị Gia Cát Lượng chọc tức đến chết: clip Veo (24 clip), căn theo thời lượng câu

Soạn 03/11/2026. **Tổng ảnh: 85 (76 ảnh chính + 9 ảnh phần hai). Số clip Veo: 24 (≥ 20). Ảnh tĩnh: 61.** Chưa có nhóm B hoạt hình nhẹ (chưa phân loại cảnh vắng).

## Quy tắc căn câu và clip (chủ kênh yêu cầu 03/11/2026)
1. Mỗi clip Veo dài **8 giây**. Câu lời kể đọc **dài hơn 8 giây thì clip hết mà câu chưa hết** (lỗi lệch như TQ10 câu 28). Cách xử lý: vẽ **thêm một ảnh phần hai** (mã = 100 + số câu, ví dụ 101 là phần hai của câu 1) vẽ nội dung nửa sau của câu; dựng: clip 8 giây rồi ảnh phần hai cho đến hết câu.
2. Ngưỡng: lệch ≤ 1,0 giây thì giữ khung cuối clip; 1,0 đến 1,5 giây giữ khung cuối hoặc làm chậm clip; **trên 1,5 giây phải có ảnh phần hai**. Câu ngắn hơn 8 giây thì cắt clip theo thời lượng câu, nên prompt đặt hành động chính ở các giây đầu.
3. **Thời lượng câu đang là ƯỚC TÍNH** theo 2,7 chữ mỗi giây (giọng Sadaltager hồ sơ C chậm hơn 3 chữ mỗi giây của quy tắc chung). **Sau khi đọc giọng xong phải tính lại bằng thời lượng thật** (`thoi_luong.json`); câu nào lệch khác dự kiến thì thêm hoặc bỏ ảnh phần hai và cập nhật bảng này.
4. Chọn clip theo tầm quan trọng của cốt truyện (cảnh chính, có chuyển động), theo `CLAUDE.md` mục "Veo cho tập gộp". Clip chỉ cần một hành động nhỏ, chậm.

**Tiền tố cho cảnh thời Hán (dán vào mọi prompt, không nêu tên người):**
`Animate this exact 2D ligne claire illustration. Keep the same drawing style, flat colours, outlines, and exactly the same characters, faces, clothes and objects. Keep exactly the same people in the foreground. Han dynasty clothing only, no modern objects, no new foreground people, no text, no letters, no camera cut, no zoom into faces, silent, no music, no speech. Motion:`

**Tiền tố cho cảnh phố Tống (câu 056, 060, 062):**
`Animate this exact 2D ligne claire illustration. Keep the same drawing style, flat colours, outlines, and exactly the same characters, faces, clothes and objects. Keep exactly the same people in the foreground. Song dynasty clothing only, no modern objects, no new foreground people, no text, no letters, no camera cut, no zoom into faces, silent, no music, no speech. Motion:`

Cách làm clip: Google Flow, "Frames to Video", khung đầu `assets/anh_2d/CDCF/NNN.jpg`, 16:9, 8 giây, tắt âm. Làm thử 3 clip trước (005, 025, 043). Lưu `assets/clips_2d/CD/E4_NNN.mp4`.

## Nhóm A — Veo (24 clip)

| Ảnh | Câu | Chữ | Giây (ước) | Căn thời lượng | Cảnh (chỉ để tra, KHÔNG dán vào Veo) | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|---|---|---|---|
| 001 | 1 | 29 | 10.7 | lệch 2.7 s → ảnh phần hai 101 | Zhou Yu đứng ở mũi chiến thuyền lúc hoàng hôn | 0-3s: the man at the bow stands tall as the wind lifts his sleeves and the sails behind him ripple. 3-6s: he turns his head slowly toward the burned wreck and the drifting smoke on the water. 6-8s: he lowers his gaze, calm, as the boat rocks gently. |
| 005 | 5 | 14 | 5.2 | đủ | Zhou Yu loạng choạng, hai sĩ quan đỡ | 0-3s: the man staggers a step backward with a pained face, head tilting back. 3-6s: the two officers hurry in and catch him under the arms. 6-8s: they hold him upright as he sags. |
| 011 | 11 | 25 | 9.3 | hơi lệch, giữ khung cuối | Mở cổng dinh, mời vào | 0-3s: the man in teal pushes the big wooden gate open with both hands. 3-6s: he sweeps one sleeve out to invite the young guest in and the guest bows. 6-8s: the guest steps forward across the threshold. |
| 012 | 12 | 23 | 8.5 | đủ | Chu Du trẻ bước ra cổng, bạn trải chiếu | 0-3s: the young man walks out through the gate with a light easy stride, sleeves swaying, a small cloth bundle in hand. 3-6s: behind him in the courtyard the other man cheerfully unrolls a sleeping mat. 6-8s: the young man glances back with a smile and keeps walking. |
| 015 | 15 | 25 | 9.3 | hơi lệch, giữ khung cuối | Đạo quân phương bắc hành quân mùa đông | The vast column of soldiers marches steadily toward the camera across the frozen north bank, blank banners swaying, breath puffing in the cold, a few snow flurries drifting; steady marching rhythm. |
| 016 | 16 | 26 | 9.6 | lệch 1.6 s → ảnh phần hai 116 | Người trên đài cao giơ tay tuyên bố | 0-3s: the commander on the tall platform raises one arm high, sleeve whipping in the wind. 3-6s: he sweeps the arm across the horizon and the tiny soldiers below ripple and cheer. 6-8s: banners snap in the wind. |
| 020 | 20 | 23 | 8.5 | đủ | Cưỡi ngựa dẫn đoàn quân dọc sông | The rider leads the long column along the river road at a steady walk, hooves landing in clear four-beat rhythm, soldiers marching behind, banners swaying, sunlight glinting on the river. |
| 021 | 21 | 34 | 12.6 | lệch 4.6 s → ảnh phần hai 121 | Hai hạm đội lớn nhỏ trên sông | The camera drifts slowly along the river: the huge fleet on the right rocks on the water, oars rising and falling and sails fluttering; the small fleet on the left sails ahead and the tiny figure on the nearest deck stands calm. |
| 022 | 22 | 24 | 8.9 | đủ | Lão tướng chỉ về hạm đội địch | 0-3s: the old general on the deck points steadily toward the enemy fleet, his sleeve fluttering. 3-6s: sailors behind him move about the deck and the ship rocks gently in the dusk light. 6-8s: he lowers his arm and nods slowly. |
| 023 | 23 | 22 | 8.1 | đủ | Thủy thủ chất củi rơm lên thuyền nhỏ | The sailors on the quay hurry back and forth piling dry brushwood and straw onto the small boats, pouring oil from clay jars and passing bundles hand to hand; the boats bob on the water. |
| 024 | 24 | 32 | 11.9 | lệch 3.9 s → ảnh phần hai 124 | Thuyền nhỏ lao qua sông, buồm căng gió | The line of small boats surges across the river with sails fully swollen, spray flying from the bows; the flame on the lead boat grows and flickers, flags streaming in the wind. |
| 025 | 25 | 23 | 8.5 | đủ | Hạm đội địch cháy trong đêm | The burning fleet: tall flames rise and flicker, black smoke rolls upward, burning masts lean, sparks drift into the sky and reflections ripple on the water; tiny sailors run along the decks. |
| 026 | 26 | 9 | 3.3 | đủ | Tàn quân lê bước qua bãi lau lúc đêm | The defeated soldiers trudge slowly forward through the reeds at night, heads down, the reeds swaying around them. |
| 027 | 27 | 31 | 11.5 | lệch 3.5 s → ảnh phần hai 127 | Chỉ huy trên đài tướng, ba sĩ quan quỳ nhận lệnh | 0-3s: the man on the command tower stretches one arm out firmly to give an order. 3-6s: the three officers below bow and rise with joined hands. 6-8s: one officer turns and hurries away while the man lowers his arm. |
| 032 | 32 | 19 | 7.0 | đủ | Tướng gượng dậy, đi giữa hai dãy lều | 0-3s: the man pushes himself up from his seat. 3-6s: he walks slowly between the two rows of tents with one hand pressed to his side, tent cloth fluttering. 6-8s: soldiers glance at him as he passes. |
| 033 | 33 | 13 | 4.8 | đủ | Viên tướng bên kia sông quay ngựa | The rider on the far bank wheels his horse around and raises one hand to signal, dust kicking up from the hooves; the horse turns in clear steps. |
| 043 | 43 | 30 | 11.1 | lệch 3.1 s → ảnh phần hai 143 | Đạo quân hành quân về phía tây qua hẻm núi | The army column marches west through the mountain pass, the two riders at the front looking ahead, horses walking in clear four-beat rhythm, soldiers striding steadily, blank banners swaying, a little mist drifting. |
| 045 | 45 | 15 | 5.6 | đủ | Cổng thành: sĩ quan chất xe, quân xếp hàng | The officers load the wagons beside the city gate and the soldiers form lines, a banner sways in the morning light, a wagon wheel turns slowly. |
| 046 | 46 | 15 | 5.6 | đủ | Thuyền có mái che lướt trên sông sương | The covered boat glides slowly along the misty water with its curtains swaying, the officer at the stern stands with bowed head, the soldiers march along the bank; soft ripples spread. |
| 056 | 56 | 19 | 7.0 | đủ | Người kể chuyện diễn cảnh ôm ngực ngã (phố Tống) | PRE_S + 0-3s: the standing storyteller presses a hand to his chest with a pained face and sways. 3-6s: the crowd gasps and covers their mouths, a few step back. 6-8s: the storyteller steadies himself and lifts his other hand to the crowd. |
| 058 | 58 | 29 | 10.7 | lệch 2.7 s → ảnh phần hai 158 | Quân trên boong reo mừng chiến thắng | The soldiers on the deck cheer and raise their arms again and again, the man in the foreground turns his head slowly with a proud look; smoke drifts behind and flags sway. |
| 060 | 60 | 21 | 7.8 | đủ | Người kể chuyện giơ hai con rối (phố Tống) | PRE_S + 0-3s: the storyteller raises the white puppet higher into the light. 3-6s: the small green puppet bows lower, the puppet strings swing. 6-8s: the audience watches wide-eyed and one child leans forward. |
| 062 | 62 | 31 | 11.5 | lệch 3.5 s → ảnh phần hai 162 | Người diễn ngã trên bục (phố Tống) | PRE_S + 0-3s: the performer in teal sways and drops to his knees. 3-6s: he falls slowly onto his side on the platform. 6-8s: the other performer stands calm with his arms in his sleeves while the audience murmurs. |
| 074 | 74 | 33 | 12.2 | lệch 4.2 s → ảnh phần hai 174 | Ngựa không người ở bờ sông lúc rạng sáng | The riderless horse stands at the river edge, mane and saddle tassel swaying in the breeze, mist drifting over the water; the horse lowers its head and breathes out; the tiny officers far behind bow. |

## Ảnh phần hai đã thêm (9 ảnh, đang vẽ)
| Mã | Phần hai của câu | Nội dung (ẩn dụ hoặc cảnh nối) |
|---|---|---|
| 101 | 1 | đĩa dầu đồng, ngọn lửa nhỏ lụi dần, ánh lửa hạm đội tắt dần ngoài cửa sổ (chết ở tuổi ba mươi sáu) |
| 116 | 16 | trại quân rộng với vô số lều và thuyền sát bờ (tám mươi vạn quân) |
| 121 | 21 | sa bàn: bên phải cả đàn quân đỏ nhỏ xíu, bên trái vài quân xanh (tám mươi vạn so với ba vạn) |
| 124 | 24 | thuyền lửa đâm vào hạm đội địch trong đêm |
| 127 | 27 | chiếu trống có chiếc khăn trắng gấp gọn trước đài chỉ huy (Gia Cát Lượng không có mặt) |
| 143 | 43 | sa bàn phía tây, con đường qua hẻm núi, một quân cờ ở lại giữ đất |
| 158 | 58 | người áo trắng đứng bậc cao hơn viên tướng áo xanh lục (cao hơn nhờ đặt cạnh người giỏi) |
| 162 | 62 | ba khối gỗ xếp hàng, khối thứ ba ngã (ba lần bị chọc, ba lần thua) |
| 174 | 74 | sa bàn dang dở: đường cờ chỉ cắm nửa chừng, cờ còn nằm trong khay (chưa kịp làm nốt kế hoạch) |

## Việc còn lại
1. Vẽ xong 9 ảnh phần hai và duyệt (ảnh ẩn dụ vẽ hai bản, xem người ngoài có hiểu không).
2. Chạy `python kiem_prompt_veo.py ke-hoach/chu-du-veo.md` (phải ĐẠT).
3. Chủ kênh tạo clip, gửi lại; nhận clip rồi kiểm khung đầu khớp ảnh gốc.
4. Đọc giọng, tính lại bảng căn thời lượng bằng thời lượng thật, bổ sung ảnh phần hai nếu còn câu lệch.
