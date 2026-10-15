# Tam Quốc tập 3 — Ảnh cần vẽ, clip Veo, hoạt hình nhẹ

Soạn từ `tam-quoc-tap-3-kich-ban.md` (kịch bản chờ chủ kênh duyệt). Sửa kịch bản thì rà lại danh sách theo số câu. Số ảnh = số câu − 1 từ câu 4 trở đi (câu 3 dùng lại ảnh 002).

## Quy ước phân nhóm (chủ kênh chốt, áp dụng mọi tập; ghi ở `CLAUDE.md`)

- **Nhóm A — Veo:** chỉ các cảnh chính có **người di chuyển nhiều** (hành quân, hàng quân, dàn trận, đám đông, người bước đi). Làm bằng Google Flow / Veo, ảnh → video.
- **Nhóm B — tool dựng đang có (`anim_nhe.py`, không dùng AI):** cảnh vật, đồ vật, cảnh vắng người; chỉ cây cỏ, cờ, nước, lửa, khói, đèn, sương chuyển động nhẹ.
- **Còn lại — ảnh tĩnh:** cảnh người đứng yên hoặc có tương tác tay; dùng chuyển máy chậm sẵn của tool dựng, không làm clip.

## Cần bao nhiêu

- **Ảnh tĩnh: 85 ảnh** (mỗi lời kể một ảnh, mỗi ảnh dùng một lần). Video ngắn dùng lại 9 ảnh, không vẽ thêm. Lưu `assets/anh_2d/TQ3/001.jpg` … `085.jpg`.
- **Veo (nhóm A): 12 clip**, lưu `assets/clips_2d/TQ3/NNN.mp4`.
- **Hoạt hình nhẹ (nhóm B): 19 cảnh**, chạy `python anim_nhe.py TQ3 <số ảnh,…>` sau khi có ảnh; cần tạo `ke-hoach/nhan-vat/TQ3_nhe.json` (khung vùng chuyển động chọn tay khi đã có ảnh, như `TQ2_nhe.json`).
- **Giữ ảnh tĩnh:** 54 ảnh.
- **Ảnh bìa:** tạm hoãn.

## Cách vẽ ảnh

- `ke-hoach/tam-quoc-tap-3-prompt-anh.txt`: 85 prompt đầy đủ, dán nguyên (đã gồm nhân vật và phong cách). `ke-hoach/nhan-vat/TQ3_anh.json`: cùng nội dung cho pipeline.
- Tuổi nhân vật theo năm 190: Lưu Bị 29, Quan Vũ 31, Trương Phi 28, Tôn Kiên khoảng 35 (tập 2 ghi 45, theo sử ông sinh 155, mất 192 lúc 37 tuổi; đã vẽ rồi thì dùng ảnh cũ làm tham chiếu mặt).
- Nhân vật mới cần khóa mặt trước (vẽ một ảnh rồi làm tham chiếu): Tôn Kiên, Lữ Bố, Hồ Chẩn, Viên Thuật, Đinh Nguyên, Vương Doãn, Hàn Phức, Tổ Mậu.
- Cảnh nhạy cảm xử lý bằng cảnh vắng người hoặc nhìn từ sau: giết Thiếu đế (ảnh 014), chém Hoa Hùng (037, 039), đốt Lạc Dương (043), đào lăng (044), Tôn Kiên chết (055 đến 057), Lữ Bố giết Đổng Trác (075, 076). Không máu, không cảnh chém, không vẽ ngựa cận cảnh.

## Nhóm A — Veo (12 clip, người di chuyển nhiều)

Chọn "Frames to Video", tải ảnh làm khung đầu, 16:9, 8 giây hoặc ngắn nhất, tắt âm nếu có. Dán tiền tố rồi dán prompt. Mỗi ảnh một clip. Làm thử 3 clip (ảnh 026, 062, 036) trước.

**Tiền tố dán vào MỌI prompt:**

`Animate this exact 2D ligne claire illustration. Keep the same drawing style, flat colours, outlines, and exactly the same characters, faces, armour, clothes and weapons. Keep exactly the same people in the foreground. Han dynasty soldiers on foot only, no horses, no modern objects, no new foreground people, no text, no letters, no camera cut, no zoom into faces, silent, no music, no speech. Motion:`

**Quy tắc:** người tiền cảnh chỉ thở, đổi trọng tâm, bước đi đều, áo khăn bay theo gió; hàng quân chuyển động tập thể đơn giản (tiến vài bước, giáo nghiêng cùng nhịp, cờ bay, bụi); không cảnh chém nhau, không máu; clip nào mọc thêm người, thêm tay, mặt méo, vũ khí đổi hình, xuất hiện ngựa thì bỏ, dùng ảnh tĩnh. Veo xuất 720p thì dựng lại 1080p/30 fps cùng hạt phim.

| Ảnh | Câu | Cảnh | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|---|
| 017 | 18 | rows of idle soldiers sitting around cold cooking pots in a hillside camp, seen from behind one seated… | Slow push-in, thin smoke curls up from the cooking pots, the seated soldiers shift their weight slightly, banners flutter, the foreground man stays seated and breathes. |
| 019 | 20 | a small river boat on the Qiantang river with a seventeen-year-old youth standing at the bow and his… | Slow lateral drift along the river, the boat rocks very slightly, ripples spread on the water, mist drifts, the two people stay in place. |
| 026 | 27 | wide view of Han foot soldiers scattered on a dusty plain with enemy ranks approaching from the far side,… | Slow lateral drift to the right, dust rolls across the field, the distant enemy ranks advance a few steps in unison, spear tips tilt together, banners flutter. |
| 027 | 28 | a small knot of about ten men pushing through a thin line of soldiers in a thick dust cloud, wide shot, no… | Slow push-in, thick dust swirls, the small group presses forward together through the thin line, spears sway, nobody comes forward into the foreground. |
| 029 | 30 | a dusty narrow dirt shortcut leading into hills in the foreground, a distant dust cloud of pursuers on the… | Static camera with a slow push-in, the dust cloud on the plain drifts and rolls, grass sways at the roadside, clouds drift. |
| 032 | 33 | soldiers forming ranks again on a field at dusk, a tall red banner at the front, seen from behind, no… | Slow push-in, the ranks stand firm while spear tips and the tall red banner sway in the wind, dust glows orange in the dusk light. |
| 036 | 37 | a column of soldiers breaking ranks and stumbling on a road, dust, banners tilting, wide shot, no horses,… | Slow tracking shot along the column, the soldiers stumble and bunch up in unison, dust rises, banners tilt and flutter. |
| 037 | 38 | Sun Jian seen from behind standing on a mound with a spear upright, in front of him only dust and plain… | Slow push-in behind him, dust and smoke drift across the field in front, the banners flutter, he stays still and breathes. |
| 059 | 60 | tents being taken down and loaded on carts in a coalition camp, soldiers packing, no horses, seen from far | Slow lateral drift along the camp, canvas ripples, the soldiers move boxes onto the carts at the same slow pace, banners flutter, dust drifts. |
| 062 | 63 | a stone bridge over a river with two armies on opposite banks, blue banners on the left bank and red on… | Slow descending crane move over the river, the two armies hold their ranks on the banks, banners flutter, spear tips sway, morning mist drifts. |
| 071 | 72 | a young maidservant seen from behind carrying a small oil lamp along a palace corridor at night, exactly… | Slow push-in behind her, the lamp flame flickers and shadows shift on the walls, she walks forward at a steady pace. |
| 073 | 74 | palace gate guards in plain uniforms lined up at a gate, seen from behind, torch light, nobody fighting | Slow push-in, the torch flames flicker, the guards stand still and breathe, banners ripple. |

## Nhóm B — hoạt hình nhẹ bằng tool dựng (`anim_nhe.py`, không dùng AI)

Không dùng Veo hay Kaggle (video AI giật, dễ biến dạng). Chạy `python anim_nhe.py TQ3 <số ảnh,…>`; vùng chuyển động xác định theo màu (cỏ, lá, nước, lửa) và khung chọn tay trong `TQ3_nhe.json`.

| Ảnh | Câu | Phần chuyển động |
|---|---|---|
| 003 | 4 | ngọn đèn dầu, ánh sáng chớp nhẹ |
| 004 | 5 | sương trôi giữa vách núi, bụi cây |
| 014 | 15 | ngọn đèn dầu, rèm khẽ lay |
| 030 | 31 | lá cờ đỏ trên cột cháy, cỏ cao, khói mỏng |
| 041 | 42 | ngọn đèn dầu |
| 042 | 43 | sương mù ở cửa ải |
| 043 | 44 | lửa và khói đen từ thành cháy |
| 044 | 45 | ánh đuốc trong cổng lăng, bụi, lá |
| 045 | 46 | cờ trên tháp cổng, ánh sáng bình minh |
| 054 | 55 | lá cờ đỏ, khói bụi, mây |
| 055 | 56 | sương trên núi, cây thông |
| 058 | 59 | mặt sông, thuyền nhỏ, sương |
| 066 | 67 | cờ trên các tháp, bụi đường |
| 074 | 75 | ánh sáng qua cửa điện, bụi lơ lửng |
| 079 | 80 | sương dọc tường thành lúc chiều tối |
| 081 | 82 | ngọn đèn dầu |
| 082 | 83 | khói mỏng, vải cờ rơi lay nhẹ, sương |
| 083 | 84 | khói mỏng, con quạ, tro bay |
| 085 | 86 | cỏ ven đường, sương, nắng lên |

## Giữ ảnh tĩnh (54 ảnh)

Ảnh: 001, 002, 005, 006, 007, 008, 009, 010, 011, 012, 013, 015, 016, 018, 020, 021, 022, 023, 024, 025, 028, 031, 033, 034, 035, 038, 039, 040, 046, 047, 048, 049, 050, 051, 052, 053, 056, 057, 060, 061, 063, 064, 065, 067, 068, 069, 070, 072, 075, 076, 077, 078, 080, 084.

Đây là cảnh người đứng yên hoặc có tay cầm vật; không làm clip để khỏi biến dạng.

