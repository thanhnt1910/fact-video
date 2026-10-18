# Tam Quốc tập gộp 4+5 — Kế hoạch 40 clip Veo (ảnh → video)
Trạng thái: BẢN NHÁP chờ chủ kênh duyệt. Ảnh nguồn lấy từ `assets/anh_2d/TQ45_V2/` (sau khi thay các ảnh sửa lại ở `TQ45_R1`; clip chỉ làm khi ảnh đã chốt). Không có clip tập 3 vì tập 3 đã dựng xong.
Cập nhật 18/10: clip E4_067 bị bỏ vì Veo tự vẽ lại khung đầu, cảnh 067 dùng ảnh tĩnh; còn 39 clip.

## 1. Con số
| Mục | Giá trị |
|---|---|
| Số clip | 40 trên 177 ảnh |
| Mỗi clip | 6 giây, 16:9, 720p, tắt tiếng |
| Tổng thời lượng Veo | 240 giây, khoảng 18% video 22 phút |
| Nhịp | cứ khoảng 4 ảnh có một clip, rải đều từ chương Mở đầu tới Lời kết |
| Chi phí API Veo 3.1 Lite (0,05 USD/giây) | 240 giây ≈ 12 USD một lần; làm lại tới 3 lần cho cảnh có tay ≈ 25–30 USD (Fast gấp đôi, không dùng bản thường) |
| Làm tay trong Google Flow | trừ credit tài khoản, không tốn tiền API |
Rủi ro: tay 13 clip, đám đông 10 clip, an toàn 8 clip, ngựa 9 clip.
## 2. Nguyên tắc chọn
- Chọn cảnh chính theo cốt truyện (trao ấn, từ chối, nhận ấn, thú nhận, đóng cổng, rót rượu, giương cung, đón thiên tử, hai lần cứu người, mất Hạ Bì...), kể cả cảnh có tay; xử lý rủi ro bằng cách làm kỹ.
- Cảnh có tay: một hành động nhỏ, chậm, một chủ thể, máy quay gần như đứng yên; tạo tối đa 3 bản (`_a`, `_b`, `_c`) với mô tả hơi khác, chọn bản tốt nhất; cả 3 hỏng thì giữ ảnh tĩnh với hiệu ứng máy quay.
- Cảnh ba huynh đệ (020, 177): chỉ gió, lửa, hơi thở, không cử động tay để vũ khí không đổi hình.
- Cảnh có chiến tranh: không ai bị đánh trúng, không máu.
- Mỗi ảnh một clip, mỗi ảnh một lần trong video.
## 3. Tiền tố dán vào MỌI prompt

`Animate this exact 2D ligne claire illustration. Keep the same drawing style, flat colours, outlines and exactly the same characters, faces, clothes, weapons and number of people, arms and hands. No new people, no new objects, no text, no letters, no camera cut, no zoom into faces, silent, no music, no speech. Motion:`
## 4. 40 clip
| Clip | Ảnh | Chương | Cảnh chính | Rủi ro | Prompt chuyển động (dán sau tiền tố) |
|---|---|---|---|---|---|
| E4_001 | 001 | Mở đầu | Đào Khiêm đưa hộp ấn cho Lưu Bị, Lưu Bị giơ tay từ chối | tay | The elderly white-bearded man slowly holds the lacquered box a little further toward the tall slender man in the dark robe, who slowly shakes his head and keeps both palms raised; the kneeling officials stay still; lamp flames flicker. |
| E4_002 | 002 | Mở đầu | Lưu Bị từ chối trên bậc đá, cả châu quỳ van xin | đám đông | Slow push-in; the man standing on the steps bows his head and straightens, the crowd below stays kneeling and a few heads sway slightly; morning light shifts on the rooftops. |
| E4_016 | 016 | Tướng nhỏ ở Bình Nguyên | Người khách thú nhận không dám giết Lưu Bị | an toàn | Slow push-in; the kneeling masked man bows his head lower, the tall slender man in the dark robe turns his face slightly toward him with a surprised look; lamp flame flickers. |
| E4_020 | 020 | Tướng nhỏ ở Bình Nguyên | Ba anh em ngủ chung giường trong lều | an toàn | Almost static; the three sleepers breathe slowly with the blankets rising a little, the lamp flame flickers and the tent canvas moves gently in the night air. Nobody wakes or moves their arms. |
| E4_022 | 022 | Lời cầu cứu đầu tiên | Thái Sử Từ phi ngựa tới Bình Nguyên cầu viện | ngựa | The dusty rider slowly steps down from the tired horse, which lowers its head and breathes; the guards hurry a few steps toward him; dust settles; thin smoke drifts on the horizon. |
| E4_027 | 027 | Lời cầu cứu đầu tiên | Quân cứu viện kéo đến, giặc nhổ trại chạy | đám đông | The column marches slowly away from the camera along the road behind the red banner, dust rises, the distant tents are struck and the besiegers retreat; the soldiers keep their number and formation. |
| E4_030 | 030 | Món nợ của Tào Tháo | Tào Tháo trong trướng, tay đặt lên chuôi kiếm | tay | Slow push-in; the short man in dark armour keeps his hand on the sword hilt and slowly turns his head toward the officers, who stand still; lamp flames flicker. |
| E4_036 | 036 | Món nợ của Tào Tháo | Tào Tháo dẫn quân đánh Từ Châu | ngựa | The camera tracks sideways; the horse of the rider in dark armour at the head of the long army walks forward, banners ripple, dust drifts up from the road. |
| E4_040 | 040 | Lời cầu cứu thứ hai | Sứ giả trao thư khẩn cho Điền Giai | tay | The courier slowly holds out the rolled letter and the commander takes it with one hand; the officers lean in slightly; banners flutter in the grey morning. |
| E4_042 | 042 | Lời cầu cứu thứ hai | Doanh trại nhỏ của Lưu Bị, dân đói nhận lương | đám đông | Slow push-in; the tall slender man walks slowly between the people, the hungry peasants shuffle forward in line, camp fire smoke rises, horses stand calmly. |
| E4_048 | 048 | Lời cầu cứu thứ hai | Lưu Bị nhận ấn thứ sử Dự Châu ở Tiểu Bái | tay | The official slowly holds out the small seal on its cord and the tall slender man bows his head and takes it with both hands; the assembled soldiers stand still; banners flutter. |
| E4_055 | 055 | Kẻ chạy khỏi Trường An | Lữ Bố rút khỏi Trường An khi quân địch tràn vào | ngựa | The armoured rider turns his horse and rides slowly away along the wall, his small band follows, smoke drifts across the sky; the enemy soldiers far away keep pouring through the gate. |
| E4_056 | 056 | Kẻ chạy khỏi Trường An | Lữ Bố cùng vài trăm kỵ ra Vũ Quan | ngựa | Slow tracking from the side; the riders walk through the pass toward the distant gate, lowered banners hang, dust rises, evening light dims. |
| E4_057 | 057 | Kẻ chạy khỏi Trường An | Viên Thuật quay mặt từ chối Lữ Bố | tay | The seated nobleman slowly turns his head away and raises one hand in refusal; the tall armoured man standing before him stiffens and lowers his eyes; lamp flames flicker; officials stay still. |
| E4_062 | 062 | Con ngựa Xích Thố | Lữ Bố xông trận phá quân Trương Yên | ngựa | The camera pushes in a little; the red horse and the small band of riders charge forward, the enemy horsemen scatter, dust clouds billow, banners snap in the wind. No one is struck. |
| E4_066 | 066 | Con ngựa Xích Thố | Trướng đêm với chiếc giường rối, quân xông vào | an toàn | Slow push-in; torchlight flickers across the canvas, the shadows of soldiers move along the wall, the lamp flame flickers; nobody enters the frame. |
| E4_067 (BỎ, dùng ảnh tĩnh) | 067 | Con ngựa Xích Thố | Sáng ra Viên Thiệu cho đóng cửa thành | tay | The soldiers slowly push the two gate leaves shut and lower the bar; the man in the road keeps standing with a grim face; dawn light brightens. |
| E4_072 | 072 | Bạn cũ của Tào Tháo | Tào Tháo và Trương Mạc nhìn nhau rơi lệ | an toàn | Almost static; slow push-in; the two bearded men stay facing each other, the one in grey slowly lowers his gaze, lamp flames flicker. |
| E4_076 | 076 | Bạn cũ của Tào Tháo | Lữ Bố được đón vào Duyện Châu | đám đông | Slow push-in; the dusty armoured man walks slowly forward between the lines of people, the two officials bow, the crowd shifts slightly, banners flutter. |
| E4_084 | 084 | Lời trăn trối | Mi Trúc dẫn người cả châu ra đón, Lưu Bị không dám nhận | tay | The delegation bows lower; the tall slender man slowly shakes his head with both hands raised; the soldiers stand still; dust drifts in the light. |
| E4_085 | 085 | Những người khuyên | Trần Đăng khuyên Lưu Bị nhận Từ Châu | tay | The man in the hall slowly moves his raised hand as he speaks, the tall slender man listens and gives a small nod; the elders behind stay still; lamp flames flicker. |
| E4_089 | 089 | Những người khuyên | Lưu Bị chắp tay nhận Từ Châu trước cổng thành | đám đông | The tall slender man bows slightly with joined hands and straightens, the people around him bow and a few raise their arms; banners flutter in the dawn light. |
| E4_096 | 096 | Ba lần nhường, hay | Lưu Bị nghe Trần Đăng và Khổng Dung bàn | tay | Slow push-in; the seated man keeps his hand at his chin and slowly nods, the two advisers lean slightly toward him; lamp flames flicker. |
| E4_106 | 106 | Món quà có độc | Tào Tháo trên đồi nhìn về Từ Châu | an toàn | Slow push-in from behind; the man on the hilltop keeps his arm pointing, a cold wind moves his cloak and the banners, the evening light dims. |
| E4_114 | 114 | Kết cục ở Duyện Châu | Tào Tháo phi ngựa qua lửa | ngựa | The camera tracks sideways; the horse gallops through the corridor of flames, the rider's cloak flies, smoke and dust billow. No injury. |
| E4_118 | 118 | Kết cục ở Duyện Châu | Quân Tào Tháo vây Ung Khâu | đám đông | Slow crane-like push-in; smoke rises from the hill fortress, banners ripple, the soldiers around the walls stand in their ranks. |
| E4_120 | 120 | Kết cục ở Duyện Châu | Lữ Bố thua, cùng kỵ binh phi về phía đông | ngựa | Slow tracking behind the riders; the red horse leads at a trot, dust rises, lowered banners flutter, the first sunlight brightens the distant walls. |
| E4_124 | 124 | Người cho nương nhờ | Lữ Bố mời Lưu Bị ngồi trên giường của vợ, vợ rót rượu | tay | The woman slowly tilts the clay jar and pours wine into the cup, the smiling armoured man gestures slightly with one hand, the tall slender man sits still; lamp flames flicker. |
| E4_132 | 132 | Hạ Bì | Lữ Bố đưa kỵ binh tới cổng Hạ Bì trong đêm | ngựa | The camera pushes in slowly; the cavalry advance at a walk, the gate slowly opens, torches flicker on the gate-tower, the leading rider keeps his halberd upright. |
| E4_133 | 133 | Hạ Bì | Lưu Bị rút quân về Hải Tây | đám đông | Slow tracking along the river bank; the weary column walks forward with lowered banners, mist drifts over the water; the number of soldiers stays the same. |
| E4_138 | 138 | Hạ Bì | Quân Lữ Bố tới chân thành, cổng mở toang | đám đông | The long column advances slowly along the road toward the camera, the gates swing fully open, dust rises, banners flutter in the dawn wind. No one is struck. |
| E4_139 | 139 | Hạ Bì | Lữ Bố ngồi trên cổng, kỵ binh phóng lửa | ngựa | Slow tilt up; the three riders gallop through the gate with torches, flames and smoke rise behind the wall, banners snap, the armoured man stays seated on the tower. No one is struck. |
| E4_146 | 146 | Cầu hòa và Tiểu Bái | Lưu Bị đứng ngoài cổng Tiểu Bái nhìn về Hạ Bì | an toàn | Slow push-in from behind; the man at the gate stays standing and slowly lowers his head, the wind moves his sleeves and the banner far away, dusk light dims. |
| E4_152 | 152 | Bắn kích viên môn | Kỷ Linh dẫn ba vạn quân tiến đánh Tiểu Bái | đám đông | The camera cranes up slowly; the vast army advances across the plain toward the small town, banners ripple, dust rises in long clouds. |
| E4_159 | 159 | Bắn kích viên môn | Lữ Bố giương cung bắn kích | tay | The armoured archer slowly draws the bow a little further and holds still, the generals watch with amazed faces and lean slightly; banners flutter. He does not release the arrow. |
| E4_164 | 164 | Chạy sang Tào | Tào Tháo đón Lưu Bị ở cổng trại | tay | The two men slowly bow with joined hands and straighten; the lined-up soldiers stay still; lamp flames flicker; the grain carts creak slightly forward. |
| E4_166 | 166 | Chạy sang Tào | Tào Tháo lắc đầu, không giết Lưu Bị | an toàn | Slow push-in; the seated man slowly shakes his head once, his hand stays on the table; the lamp flame flickers; the tent wall sways slightly. |
| E4_174 | 174 | Lời kết | Tào Tháo đón thiên tử về phía đông | đám đông | Slow tracking; the procession moves forward along the road, the cart rolls slowly, the man in the dark cap walks beside it, banners flutter in the dawn light, dust rises. |
| E4_176 | 176 | Lời kết | Tào Tháo và Lưu Bị ngồi đối diện uống rượu | tay | Slow push-in; the two seated men slowly raise their cups a little and nod politely; lamp flames flicker; the officials along the wall stay still. |
| E4_177 | 177 | Lời kết | Ba anh em nhìn về kinh đô sáng rực lúc chiều tà | an toàn | Slow push-in from behind; the three men stay standing, banners ripple strongly in the wind, their sleeves and robes sway, the glow of the far city flickers. They do not move their arms. |

Dự phòng (cảnh nối, an toàn): 004, 005, 044, 105, 112, 143, 169, 171, 172, 175.
## 5. Cách làm (chọn một)
A. Qua API (khuyến nghị): viết `veo_lo.py` đọc `ke-hoach/veo/TQ45_clips.json`, gọi Veo 3.1 Lite 6 giây cho từng ảnh, tối đa 3 lần thử cho cảnh có tay, lưu `assets/clips_2d/TQ45/E4_NNN[_a|_b|_c].mp4`, bỏ qua clip đã có, ghi chi phí bằng `chi_phi.py`; chạy bằng workflow bấm tay chia 4 đợt 10 clip.
B. Làm tay trong Google Flow (Frames to Video): tải ảnh làm khung đầu, dán tiền tố + prompt, 16:9, tắt âm; đặt file đúng tên như trên.

Làm thử 3 clip đầu: E4_001 (tay), E4_062 (ngựa, đám đông), E4_020 (ba huynh đệ) để đánh giá trước khi làm 37 clip còn lại.
## 6. Kiểm từng clip
Bỏ clip nếu: thêm người hoặc vật, thừa tay chân, mặt méo, đổi râu hoặc áo, vũ khí đổi hình, ngựa đi ngược hoặc thừa chân, chữ xuất hiện, kiến trúc thành Hàn hoặc Nhật, cảnh nhảy cắt, hình xấu ở khung cuối. Xem ở 3 điểm: đầu, giữa, cuối.
## 7. Ghép vào video
Clip đặt ở đầu cảnh, hết clip giữ khung cuối đến hết lời kể (`long_video.py` hỗ trợ `clip_file` trong `beats`, tự cắt chữ Veo, phóng 1080p, bỏ tiếng, 24 fps). Thêm `clip_file` vào các beat tương ứng trong `scripts/TQ45.json`. Bản xem thử chưa cần clip.
## 8. Cần chủ kênh chọn
1. Làm qua API (≈ 12–30 USD) hay làm tay trong Google Flow?
2. Duyệt danh sách 40 cảnh, hoặc thêm bớt.
