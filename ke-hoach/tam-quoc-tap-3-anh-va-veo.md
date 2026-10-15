# Tam Quốc tập 3 — Ảnh cần vẽ và prompt Veo

Soạn từ `tam-quoc-tap-3-kich-ban.md` (bản kịch bản chờ chủ kênh duyệt). Nếu sửa kịch bản, danh sách này phải rà lại theo số câu.

## Cần bao nhiêu

- **Ảnh tĩnh: 85 ảnh** cho video dài (86 lời kể, mỗi lời một ảnh, câu 3 dùng lại ảnh câu 2). Mỗi ảnh chỉ dùng một lần. Video ngắn 9 câu dùng lại 9 ảnh trong số này, không cần vẽ thêm.
- **Clip Veo: 32 clip** (ảnh → video), chia hai nhóm bên dưới. Làm tối thiểu nhóm A (cảnh quân, cảnh vật, an toàn nhất); nhóm B làm thêm nếu còn lượt. Ảnh nào không làm clip thì dùng ảnh tĩnh có chuyển máy nhẹ như các tập trước.
- **Ảnh bìa:** tạm hoãn theo yêu cầu.
- Mọi ảnh ở tỉ lệ 16:9, lưu `assets/anh_2d/TQ3/001.jpg` … `085.jpg`; clip lưu `assets/clips_2d/TQ3/NNN.mp4`.

## Cách vẽ ảnh

- File `ke-hoach/tam-quoc-tap-3-prompt-anh.txt` có **85 prompt đầy đủ, dán nguyên** (đã gồm mô tả nhân vật và phong cách). File `ke-hoach/nhan-vat/TQ3_anh.json` là cùng nội dung cho pipeline (cùng định dạng `TQ2_anh.json`).
- Công thức mỗi prompt: `cảnh` + `Characters (keep exactly this look): …` + phong cách ligne claire + hậu tố chống lỗi (tay, thừa người, chữ). Giống hệt tập 1–2 để cùng một nét vẽ.
- Tuổi nhân vật đã chỉnh theo năm 190: Lưu Bị 29, Quan Vũ 31, Trương Phi 28, Tôn Kiên khoảng 35 (tập 2 ghi 45 là chưa đúng với sử: ông sinh 155, mất 192 khi 37 tuổi; nếu bạn vẽ tập 2 xong rồi thì giữ mặt cũ, chỉ cần nét râu và tuổi tương đối).
- Nhân vật mới cần khóa mặt (vẽ ảnh đầu của họ trước rồi đính kèm làm tham chiếu): **Tôn Kiên, Lữ Bố, Hồ Chẩn, Viên Thuật, Đinh Nguyên, Vương Doãn, Hàn Phức, Tổ Mậu**.
- Cảnh nhạy cảm đã xử lý bằng cảnh vắng người hoặc nhìn từ sau: giết Thiếu đế (ảnh 013), chém Hoa Hùng (ảnh 037, 039), đốt Lạc Dương (ảnh 043), đào lăng (ảnh 044), Tôn Kiên chết (ảnh 055 đến 057), Lữ Bố giết Đổng Trác (ảnh 075, 076). Không có máu, không cảnh chém.
- Không vẽ ngựa ở ảnh cận cảnh (AI hay lỗi); kỵ binh chỉ để ngoài khung hoặc bụi xa.

## Danh sách 85 ảnh

Số ảnh khác số câu từ câu 4 trở đi (câu 3 dùng lại ảnh 002): ảnh = câu − 1.

| Ảnh | Câu | Cảnh | Clip Veo |
|---|---|---|---|
| 001 | 1 | waist-up of Liu Bei, Guan Yu and Zhang Fei standing side by side on a dusty road before a mountain pass gate in morning mist,… |  |
| 002 | 2 (+3) | waist-up of Guan Yu holding a steaming pottery wine cup in one hand, calm stern face, exactly one man, his far arm hidden… |  |
| 003 | 4 | an open bamboo-slip scroll on a wooden table beside an oil lamp, warm light, an empty quiet scene of objects only |  |
| 004 | 5 | wide view of a mountain pass gate tower between two cliffs in grey mist, no banners, no people, an empty quiet landscape |  |
| 005 | 6 | a scholar seen from behind writing on bamboo slips by lamp light at a window, exactly one man, simple room |  |
| 006 | 7 | waist-up of Dong Zhuo standing in a palace hall, looking toward the far soldiers outside, heavy menacing face, exactly one… |  |
| 007 | 8 | waist-up of Ding Yuan in a barracks courtyard holding a wooden command tally, stern face, exactly one man, his far arm hidden |  |
| 008 | 9 | Lu Bu seen from behind standing in a dark doorway at night, tall, spear upright in his hand, exactly one man, no face visible,… |  |
| 009 | 10 | ranks of capital guard soldiers standing in a stone courtyard at dawn, spears upright, seen from behind one foreground… |  |
| 010 | 11 | waist-up of Dong Zhuo seated on a heavy chair with Lu Bu standing beside him, both facing the viewer, exactly two men, hands… |  |
| 011 | 12 | waist-up of Yuan Shao in a palace hall holding a sheathed sword horizontally at his side in one hand, about to turn away,… |  |
| 012 | 13 | waist-up of Yuan Shao standing at the gate of a northern walled city at dawn, calm determined face, exactly one man, his far… |  |
| 013 | 14 | an empty palace hall with heavy hanging curtains, one oil lamp burning, an empty low couch, no people, quiet sorrowful mood |  |
| 014 | 15 | waist-up of Dong Zhuo on palace steps in a rich dark-red court robe with a sword at his belt, wearing shoes on the steps,… |  |
| 015 | 16 | rows of empty court cushions and a lone empty throne in a hall, cold morning light, no people |  |
| 016 | 17 | waist-up of Yuan Shao standing on a wooden platform with plain coloured banners behind him, proud face, exactly one man, his… | có |
| 017 | 18 | rows of idle soldiers sitting around cold cooking pots in a hillside camp, seen from behind one seated officer, no one fighting | có |
| 018 | 19 | waist-up of Sun Jian with a red cloth headband, strong determined face looking toward the north, exactly one man, his far arm… | có |
| 019 | 20 | a small river boat on the Qiantang river with a seventeen-year-old youth standing at the bow and his father seated beside him,… | có |
| 020 | 21 | the youth Sun Jian on a riverbank with a short sword in one hand, his other arm outstretched pointing east, bundles of loot on… |  |
| 021 | 22 | Sun Jian seen from behind on a hilltop looking down at a wide river valley at dawn, exactly one man, no face visible |  |
| 022 | 23 | waist-up of Yuan Shu at a city gate with a bundle on his shoulder looking back anxiously, exactly one man, his far arm hidden |  |
| 023 | 24 | waist-up of Sun Jian and Yuan Shu facing each other inside a camp tent, exactly two men, hands hidden |  |
| 024 | 25 | waist-up of Sun Jian standing in front of a plain solid-colour banner that is not his own, serious face, exactly one man, his… |  |
| 025 | 26 | waist-up of Dong Zhuo reading a scroll with a thoughtful sneer, lamp light, exactly one man, his far arm hidden |  |
| 026 | 27 | wide view of Han foot soldiers scattered on a dusty plain with enemy ranks approaching from the far side, dust clouds, plain… | có |
| 027 | 28 | a small knot of about ten men pushing through a thin line of soldiers in a thick dust cloud, wide shot, no horses, no faces… | có |
| 028 | 29 | waist-up of Sun Jian and Zu Mao, exactly two men, Sun Jian holding out a red cloth headband toward Zu Mao, dust and smoke… |  |
| 029 | 30 | a dusty narrow dirt shortcut leading into hills in the foreground, a distant dust cloud of pursuers on the plain, no people | có |
| 030 | 31 | a charred wooden post in a field of graves with a red cloth hung on top, tall grass, dusk light, no people | có |
| 031 | 32 | waist-up of Sun Jian sitting on a rock, tired and sweaty, his red headband gone, exactly one man, his far arm hidden |  |
| 032 | 33 | soldiers forming ranks again on a field at dusk, a tall red banner at the front, seen from behind, no horses, no one fighting | có |
| 033 | 34 | waist-up of Hu Zhen and Lu Bu side by side in a command tent, Hu Zhen worried in front and Lu Bu behind him looking sideways,… |  |
| 034 | 35 | waist-up of Hu Zhen alone in a command tent, worried face, lamp light, exactly one man, his far arm hidden |  |
| 035 | 36 | waist-up of Lu Bu in front of a small walled town, one arm raised pointing outward, exactly one man, his far arm hidden |  |
| 036 | 37 | a column of soldiers breaking ranks and stumbling on a road, dust, banners tilting, wide shot, no horses, no faces in close-up | có |
| 037 | 38 | Sun Jian seen from behind standing on a mound with a spear upright, in front of him only dust and plain red banners, exactly… | có |
| 038 | 39 | a pottery wine pot and a cup on a plain table, no steam, cold and still, empty quiet scene of objects only |  |
| 039 | 40 | a lone distant figure with a plain helmet standing small on a hill wall in mist, no face visible, exactly one tiny person |  |
| 040 | 41 | waist-up of Guan Yu standing calmly far from any battle, green robe, stern face, exactly one man, his far arm hidden |  |
| 041 | 42 | a closed bound book lying on a table beside an oil lamp, no text on the cover, empty quiet scene of objects only |  |
| 042 | 43 | a fortified pass gate between cliffs in mist, a long wall across the gorge, no banners, no people | có |
| 043 | 44 | a large city seen from far at night with its palaces burning, flames and black smoke, no people | có |
| 044 | 45 | a hillside tomb gate with stone doors standing open, dark inside with faint torch light, no people | có |
| 045 | 46 | Luoyang's city wall and gate tower at sunrise, whole and peaceful, tiny distant people on the road, soft golden light | có |
| 046 | 47 | waist-up of Sun Jian standing among burnt palace ruins with a broken column behind him, serious face, exactly one man, his far… |  |
| 047 | 48 | a stone well in a ruined courtyard with a rope and a hanging lantern, a soldier looking down into it seen from behind, exactly… | có |
| 048 | 49 | an imperial square jade seal with a dragon-shaped knob on a silk cloth on a table, no carved text, empty quiet scene of… |  |
| 049 | 50 | waist-up of Yuan Shu sitting in a large carved chair, calculating look, exactly one man, his far arm hidden |  |
| 050 | 51 | waist-up of Yuan Shu and a plain grey-robed adviser whispering, exactly two men, hands hidden |  |
| 051 | 52 | an empty army granary with only a few sacks left on the floor, grey light, no people |  |
| 052 | 53 | Sun Jian crouched drawing a line on the bare ground with a stick, Yuan Shu standing over him, torch-lit night, exactly two men |  |
| 053 | 54 | a coalition hillside camp with banners of many plain colours, two commanders standing apart with their backs to each other,… | có |
| 054 | 55 | a red plain banner planted in the ground at the edge of a ruined city wall at dusk, no people | có |
| 055 | 56 | Mount Xian in mist at dawn, an empty winding mountain road, no people | có |
| 056 | 57 | waist-up of Sun Jian with a calm serious face in soft light, exactly one man, his far arm hidden |  |
| 057 | 58 | a small lone figure walking on a steep forest path seen from far, no face, mist between the trees, exactly one tiny person |  |
| 058 | 59 | the great river of the south at sunrise with one small boat, calm water, soft golden light, no faces | có |
| 059 | 60 | tents being taken down and loaded on carts in a coalition camp, soldiers packing, no horses, seen from far | có |
| 060 | 61 | waist-up of Yuan Shao and Han Fu presenting a rolled scroll to each other, exactly two men, hands hidden below the frame |  |
| 061 | 62 | waist-up of Han Fu looking afraid, pale face, exactly one man, his far arm hidden |  |
| 062 | 63 | a stone bridge over a river with two armies on opposite banks, blue banners on the left bank and red on the right, wide shot,… | có |
| 063 | 64 | waist-up of Gongsun Zan and Liu Bei side by side in a northern landscape, old classmates, exactly two men, hands hidden |  |
| 064 | 65 | waist-up of Liu Bei with Guan Yu standing behind him, exactly two men, calm, hands hidden |  |
| 065 | 66 | waist-up of Liu Bei at a table with a rolled scroll in a small town office at Pingyuan, serious face, exactly one man, his far… |  |
| 066 | 67 | a huge stone fortress with towers and a long wall on a plain, tiny gates, no people | có |
| 067 | 68 | rows of enormous granaries stacked with sacks inside a fortress, empty of people | có |
| 068 | 69 | waist-up of Dong Zhuo in front with Lu Bu behind him looking sideways, tense, exactly two men, hands hidden |  |
| 069 | 70 | a long halberd lying on a carpet floor in a lamp-lit hall, nobody, empty quiet scene of objects only |  |
| 070 | 71 | waist-up of Lu Bu in a dark corridor at night looking over his shoulder, anxious, exactly one man, his far arm hidden |  |
| 071 | 72 | a young maidservant seen from behind carrying a small oil lamp along a palace corridor at night, exactly one woman | có |
| 072 | 73 | waist-up of Wang Yun and Lu Bu at a low table at night, exactly two men, hands hidden, lamp light |  |
| 073 | 74 | palace gate guards in plain uniforms lined up at a gate, seen from behind, torch light, nobody fighting | có |
| 074 | 75 | the great hall of a palace with tall columns and a long stair, empty, morning light through the doors, no people | có |
| 075 | 76 | Lu Bu seen from behind standing in an empty hall, exactly one man, no face visible, light from the doors |  |
| 076 | 77 | an empty heavy chair with a dark fur-trimmed robe draped over it, rays of light, no people |  |
| 077 | 78 | waist-up of Sun Jian in profile with raised chin at dawn, exactly one man, his far arm hidden |  |
| 078 | 79 | waist-up of Hu Zhen in front with Lu Bu behind him looking away in resentment, exactly two men, hands hidden |  |
| 079 | 80 | a long wall across a gorge with a gate tower at evening, wide shot, no people | có |
| 080 | 81 | waist-up of Guan Yu and Zhang Fei standing watch at a tent door at night with torches, exactly two men, spears upright | có |
| 081 | 82 | two blank wooden name tablets lying side by side on a table in lamp light, empty quiet scene of objects only |  |
| 082 | 83 | a quiet dawn battlefield with fallen plain banners and stones, thin smoke, no people | có |
| 083 | 84 | burnt ruins of a palace at dawn with thin smoke and one crow, no people | có |
| 084 | 85 | waist-up of Liu Bei on a small town wall at dusk looking east, serious face, exactly one man, his far arm hidden |  |
| 085 | 86 | a long road leading east between fields toward a distant misty walled city at dawn, no people | có |

## Prompt Veo (Google Flow, ảnh → video)

Chọn "Frames to Video", tải ảnh `TQ3/NNN.jpg` làm khung đầu, 16:9, 8 giây (hoặc ngắn nhất), tắt âm nếu có tùy chọn. Dán **tiền tố** rồi dán prompt của ảnh. Mỗi ảnh một clip.

**Tiền tố dán vào MỌI prompt:**

`Animate this exact 2D ligne claire illustration. Keep the same drawing style, flat colours, outlines, and exactly the same characters, faces, armour, clothes and weapons. Keep exactly the same people in the foreground. Han dynasty soldiers on foot only, no horses, no modern objects, no new foreground people, no text, no letters, no camera cut, no zoom into faces, silent, no music, no speech. Motion:`

**Quy tắc (giữ như tập 2):** người tiền cảnh chỉ thở, đổi trọng tâm, áo và khăn bay theo gió; hàng quân hậu cảnh chỉ chuyển động tập thể đơn giản (tiến vài bước, giáo nghiêng cùng nhịp, cờ bay, bụi); không đòi cảnh chém nhau; không máu, không cảnh giết người; clip nào mọc thêm người, thêm tay, mặt méo, vũ khí đổi hình hoặc xuất hiện ngựa thì bỏ và dùng ảnh tĩnh. Làm thử 3 clip (ảnh 043, 062, 053) trước để xem chất lượng rồi mới làm tiếp. Veo xuất 720p thì dựng lại 1080p/30 fps cùng hạt phim như ảnh tĩnh.

### Nhóm A: cảnh quân, cảnh vật, đồ vật (25 clip, làm trước)

| Ảnh | Câu | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|
| 017 | 18 | Slow push-in, thin smoke curls up from the cooking pots, the seated soldiers shift their weight slightly, banners flutter, the foreground man stays seated and breathes. |
| 026 | 27 | Slow lateral drift to the right, dust rolls across the field, the distant enemy ranks advance a few steps in unison, spear tips tilt together, banners flutter. |
| 027 | 28 | Slow push-in, thick dust swirls, the small group presses forward together through the thin line, spears sway, nobody comes forward into the foreground. |
| 029 | 30 | Static camera with a slow push-in, the dust cloud on the plain drifts and rolls, grass sways at the roadside, clouds drift. |
| 030 | 31 | Static camera, the red cloth flutters on the post, tall grass sways, thin smoke drifts across the graves, dusk light dims slowly. |
| 032 | 33 | Slow push-in, the ranks stand firm while spear tips and the tall red banner sway in the wind, dust glows orange in the dusk light. |
| 036 | 37 | Slow tracking shot along the column, the soldiers stumble and bunch up in unison, dust rises, banners tilt and flutter. |
| 042 | 43 | Slow push-in toward the pass gate through mist, the mist drifts between the cliffs, nothing else moves. |
| 043 | 44 | Static camera with a slow upward tilt toward the burning city, flames flicker and black smoke rolls across the sky, embers float. |
| 044 | 45 | Static camera, torch light flickers inside the open gate, dust and leaves drift across the entrance. |
| 045 | 46 | Slow push-in toward the gate, golden light brightens, flags on the tower flutter, tiny people walk along the road. |
| 047 | 48 | Static camera, the lantern sways slightly, the rope moves, dust and ash drift, the soldier stays still. |
| 054 | 55 | Static camera, the red banner flutters in the wind, dust and ash drift past, clouds move slowly. |
| 055 | 56 | Slow push-in along the road, mist drifts between the pines, leaves tremble, nothing else moves. |
| 058 | 59 | Slow lateral drift along the water, the little boat rocks slightly, ripples glitter, mist drifts. |
| 059 | 60 | Slow lateral drift along the camp, canvas ripples, the soldiers move boxes onto the carts at the same slow pace, banners flutter, dust drifts. |
| 062 | 63 | Slow descending crane move over the river, the two armies hold their ranks on the banks, banners flutter, spear tips sway, morning mist drifts. |
| 066 | 67 | Slow push-in toward the fortress, banners on the towers flutter, dust rises from the road, clouds drift. |
| 067 | 68 | Slow tracking shot along the rows of sacks, dust floats in the light, nothing else moves. |
| 073 | 74 | Slow push-in, the torch flames flicker, the guards stand still and breathe, banners ripple. |
| 074 | 75 | Slow push-in up the hall, light shifts through the doors, dust floats, nothing else moves. |
| 079 | 80 | Slow lateral drift, the evening light dims, mist drifts along the wall, nothing else moves. |
| 082 | 83 | Static camera, thin smoke drifts, fallen banner cloth stirs in the breeze, mist moves slowly. |
| 083 | 84 | Static camera, thin smoke rises, the crow flaps once and settles, ash drifts. |
| 085 | 86 | Slow forward dolly along the road toward the distant city, mist drifts, grass sways, the sun brightens slowly. |

### Nhóm B: cảnh có người, chuyển động nhẹ (7 clip, làm sau, soi kỹ)

| Ảnh | Câu | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|
| 016 | 17 | Very slow push-in toward the platform, the plain banners behind him ripple in the wind, he stands still and breathes, dust drifts in the background. |
| 018 | 19 | Very slow push-in, his red headband and sleeves move in the wind, mist drifts over the hills behind, he stands still and breathes. |
| 019 | 20 | Slow lateral drift along the river, the boat rocks very slightly, ripples spread on the water, mist drifts, the two people stay in place. |
| 037 | 38 | Slow push-in behind him, dust and smoke drift across the field in front, the banners flutter, he stays still and breathes. |
| 053 | 54 | Slow lateral drift along the ridge, the many coloured banners flap in the wind, tent canvas ripples, the two men stay still. |
| 071 | 72 | Slow push-in behind her, the lamp flame flickers and shadows shift on the walls, she walks forward at a steady pace. |
| 080 | 81 | Very slow push-in, torch flames flicker and change the light on their faces, the spears stay upright, they breathe and do not move their arms. |

