# Tam Quốc tập 1 — Prompt tạo clip chuyển động (Google Flow / Veo, ảnh → video)

Cách dùng trong Flow: chọn "Frames to Video" (ảnh → video), tải ảnh `assets/anh_2d/TQ1/NNN.jpg` làm khung đầu, dán prompt bên dưới, tỉ lệ 16:9, 8 giây (hoặc ngắn nhất có thể), tắt âm thanh nếu có tùy chọn. Mỗi ảnh chỉ làm một clip; video dùng lại clip cho các lần ảnh xuất hiện.

Tiền tố dán vào MỌI prompt (giữ nguyên nét vẽ và nhân vật):
`Animate this exact 2D ligne claire illustration. Keep the same drawing style, flat colours, outlines and exactly the same characters, faces, clothes and number of people. No new people, no new objects, no text, no letters, no camera cut, no zoom into faces, silent, no music, no speech. Motion:`

Quy tắc giữ ảnh khỏi biến dạng:
- Chỉ chuyển động máy quay chậm (đẩy vào, trượt ngang) và môi trường (gió, cờ, khói, nước, lửa, mây, lá, bụi). Nhân vật chỉ thở nhẹ, áo bay theo gió.
- Không để nhân vật làm động tác tay (cầm, trao, nắm, chào). Các ảnh đó để ảnh tĩnh.
- Xem từng clip: nếu có thêm người, thêm tay, mặt méo hoặc đổi râu/áo thì bỏ clip và dùng lại ảnh tĩnh.

## Nhóm A — làm trước (an toàn, 14 clip)
| Ảnh | Cảnh | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|
| 001 | Cột gỗ trống, mặt trời lặn | Slow push-in toward the bare pole, the dim sun sinks slightly, dust and thin mist drift across the flat plain, grass sways in the wind. |
| 003 | Giày cỏ và chiếu trước nhà tranh | Static camera with a very slow drift to the right, the thatched roof straw and grass tremble in a light breeze, soft dust floats in the morning light. |
| 006 | Cung điện Hán | Slow upward tilt along the palace roof, light clouds drift behind the roof, banners stay plain and flutter softly, no people appear. |
| 011 | Bản đồ ba mươi sáu cờ | Slow top-down push-in on the map, the small yellow flags flutter gently as if in wind, subtle paper grain shimmer. Map shape stays fixed. |
| 015 | Huyện nhỏ, Lưu Bị đi trên đường | Slow forward drift down the road, mist moves between the houses, flags sway, the walking man keeps walking at a calm pace without changing. |
| 022 | Cây dâu lớn | Slow push-in toward the great tree, leaves rustle, golden light shifts slowly through the branches. |
| 031 | Cây đào, khoảng trống | Slow drift past the tree, a few petals and blossoms fall and float in the breeze, soft light shifts. |
| 037 | Hàng dài quân Hoàng Cân ở xa | Slow lateral drift along the column, the yellow banners ripple in the wind, dust rises from the marching feet. |
| 040 | Lưu Bị trước chiến trường khói | Slow push-in, thick smoke clouds drift and roll across the battlefield behind him, embers glow, his clothes move slightly in the wind. |
| 043 | Tướng đứng trước doanh trại | Slow push-in, banners flutter in the camp behind, tent canvas ripples, dust drifts. |
| 044 | Đốc bưu đến cổng huyện | The cart moves slowly forward a short distance, the horse walks calmly, banners flutter, dust rises from the wheels. |
| 046 | Lưu Bị bước ra cổng, nhìn từ sau | Static camera slowly pulling back, he walks away along the road, banners flutter, dawn light brightens gradually. |
| 005 | Lưu Bị đi trên đường sương, nhìn từ sau | Slow push-in behind him, mist rolls across the hills, grass moves in the wind, he keeps walking. |
| 029 | Ba người ngủ chung giường | Static top-down camera, the lamp flame flickers softly changing the warm light, their chests rise and fall very slightly with breathing. Nobody wakes, nobody moves their arms. |

## Nhóm B — nếu còn lượt (chuyển động nhẹ, cần soi kỹ)
| Ảnh | Prompt |
|---|---|
| 002 | Slow lateral tracking along the five marching men, they walk at a steady pace, dust kicks up, grass sways. Exactly five men throughout. |
| 004 | Very slow push-in, his clothes sway slightly in the breeze, dust blows at his feet. He stays standing with arms behind his back. |
| 008 | Slow push-in, a faint heat shimmer over the cracked ground, dust blows, the man stays still looking down. |
| 009 | Very slow push-in on his calm face, the cloth ends of his headband flutter slightly. No hand movement. |
| 012 | Very slow push-in, dawn light brightens gradually, the spear stays upright. |
| 013 | Slow push-in, the torch flame flickers and lights his face unevenly, night clouds drift outside the window. |
| 016 | Static camera, incense smoke curls up slowly, his clothes move slightly in a breeze. |
| 018 | Slow lateral drift, a light breeze moves his sleeves, he stays still. |
| 019 | Very slow push-in, light breathing only. |
| 020 | Slow push-in on the objects, warm light moves slowly across the table, dust specks float. |
| 024 | Slow push-in, leaves rustle on both trees, the boy looks up and breathes slightly. |
| 025 | Slow push-in, the blurred background flags flutter, light shifts. |
| 026 | Slow push-in on the three men, dawn light brightens, their clothes move in a light breeze. All three remain standing still. |
| 027 | Slow push-in, a flag flutters in the background and dust blows on the road. |
| 028 | Slow push-in, torchlight flickers across their faces, they stay motionless. |
| 030 | Very slow push-in, light breeze in their sleeves, nothing else moves. |
| 032 | Slow forward dolly along the road, autumn leaves swirl and fall, the three men keep walking at the same pace. |
| 033 | Slow push-in, the lamp light flickers on their faces, they stay seated and still. |
| 035 | Slow push-in on the three men, the faint figures behind them stay still, dust drifts. |
| 038 | Slow push-in, the tent canvas moves in the wind, the scroll in his hand stays still. |
| 039 | Static camera, the oil lamp flame flickers, his chest rises and falls slightly with weak breathing. No limb moves. |
| 042 | Slow push-in, the view through the window shows light clouds moving, leaves rustling, his figure stays still. |

## Nhóm C — KHÔNG làm clip (giữ ảnh tĩnh, có tương tác tay hoặc nhiều chi tiết dễ biến dạng)
007, 010, 014, 017, 021, 023, 034, 036, 041, 045.

## Ghi chú
- Ảnh 018: tay chưa dài quá gối như sử chép; có thể bỏ khỏi clip.
- Veo xuất 720p/24 fps thì dựng lại 1080p/30 fps, thêm cùng hạt phim và bộ lọc màu như ảnh tĩnh.
- Khi có clip, đặt đường dẫn `clip_file` vào cảnh tương ứng trong `scripts/TQ1.json` (cùng cách ST3: `assets/clips_2d/TQ1/NNN.mp4`).
- Làm thử 3 clip (001, 037, 044) trước để xem chất lượng rồi mới làm tiếp.
