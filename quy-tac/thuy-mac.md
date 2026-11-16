# Series trận đánh thủy mặc (bản dài 16:9 + bản dọc 9:16)

Quy tắc riêng cho series video trận đánh vẽ kiểu tranh thủy mặc (mực trên giấy). Rút ra từ bản thử Bạch Đằng 938 (`bd1`, `bd2`), chủ kênh góp ý ngày 16/11/2026. Mọi quy tắc trong `chung.md` và `su-viet.md` vẫn áp dụng. Chỗ nào file này khác hai file kia thì đó là ngoại lệ đã được chủ kênh duyệt riêng cho series này.

Mẫu: kịch bản `ke-hoach/thu-giong-hai/bd2_full.json` và `ke-hoach/bd2-bach-dang-thuy-mac-gui-duyet.md`; mã dựng ở `phim_ban_do/thuymac/`.

## 1. Phạm vi và định dạng
- Mỗi video kể trọn một trận đánh trong sử Việt, trước năm 1858. Các tập xếp theo thứ tự thời gian, nhưng mỗi tập phải tự đứng được và không có "tập sau".
- Mỗi trận có hai bản:
  - Bản dài 16:9, khoảng 5–8 phút (1.000–1.300 chữ). Độ dài do nội dung quyết định, không độn chữ.
  - Bản dọc 9:16, 60–80 giây (8–10 đoạn), cắt từ phần trận đánh, kết bằng lời mời xem bản đầy đủ.
- Không cần làm nhanh. Mỗi video phải đủ chi tiết cả lời kể lẫn hình (chủ kênh 16/11/2026).

## 2. Giọng đọc
- Gemini **Charon**, hồ sơ C (`STYLE_C` trong `thu_giong_hai_cum.py`), `cum.txt` = 16. Chủ kênh chọn ngày 16/11/2026 sau khi nghe thử Iapetus, Puck, Charon; lý do là Sadaltager quá trầm, cần giọng to và rõ.
- Cả video một giọng, một hồ sơ. Sau khi đọc phải nhận dạng giọng từng đoạn và đạt 100% ở `kiem_giong.py` rồi mới dựng.

## 3. Kịch bản

### 3.1 Khung "câu hỏi + N thứ"
1. **Đoạn 1: một hoặc hai câu hỏi.** Hỏi thẳng vào nghịch lý của trận đánh, ví dụ bên yếu hơn vì sao thắng, hay chủ tướng địch vì sao không trở về.
   - Không năm, không tên riêng.
   - Tối đa 25 chữ (giới hạn của `kiem_mach_ke.py`).
   - Được để hai câu hỏi liền nhau: đây là ngoại lệ chủ kênh duyệt cho series này.
2. **Đoạn 2:** nói nơi chốn, không có năm (`kiem_mo_dau.py` báo lỗi nếu có năm).
3. **Đoạn 3–4:** giới thiệu hai phe bằng chi tiết có trong sử. Mỗi đoạn tối đa 4 tên riêng.
4. **Đoạn 5: lời hứa "N thứ".**
   - Bên thắng có N thứ (2–4) mà đối thủ không có.
   - Chưa nói tên các thứ ấy, chỉ gợi thứ cuối cùng (ví dụ "nằm ngay dưới mặt nước").
   - Không lộ kế sách.
5. **Thân bài:** mỗi chương mở ra đúng một thứ, gọi tên theo thứ tự ("Đây là thứ đầu tiên...", "thứ thứ hai...").
   - Chương trước đó là bối cảnh và nguyên nhân, viết gọn.
   - Cuối mỗi chương có một câu móc: một chuyện sắp xảy ra, hoặc một câu hỏi ở bước ngoặt lớn.
6. **Cao trào:** trận đánh, kể theo từng nhịp hành động. Thứ cuối cùng hiện ra đúng ở khoảnh khắc quyết định.
7. **Kết:**
   - Kết quả thực tế của trận.
   - Hậu quả ngay sau trận.
   - Tối đa một câu nối với trận về sau trên cùng nơi chốn, nếu có.
   - Một đoạn trả lời câu hỏi mở đầu, gọi lại đủ N thứ, không kể lại diễn biến.
   - Câu kết quay lại hình ảnh mở đầu, rồi lời cảm ơn (tối đa 32 chữ).
- "N thứ" là **diễn giải của người kể**. Mỗi thứ phải dựng từ sự việc có nguồn, đủ năm điều kiện diễn giải trong `chung.md`, và không được nói đó là nguyên nhân duy nhất. Ghi rõ trong "Ghi chú độ chắc".
- Không dùng lại một khuôn câu hỏi mở đầu đã dùng ở tập trước. Sau mỗi tập, thêm khuôn đã dùng vào mục "Khuôn mở đầu đã dùng" của `chung.md`.

### 3.2 Chất liệu làm video cuốn hút (vẫn đúng sử)
- **Ưu tiên chi tiết có trong sử mà ít người biết:**
  - Lời can bị gạt đi (ví dụ Tiêu Ích can vua Nam Hán).
  - Lời chủ tướng bàn với các tướng, kể gián tiếp theo sử, không đặt thành lời thoại.
  - Tước hiệu phong sẵn, số liệu sử chép ("chết đuối quá nửa").
- **Mọi chi tiết loại này phải đối chiếu bản dịch chính sử trước khi đọc giọng.** Không đối chiếu được thì ghi rõ nguồn khác ("sử Trung Quốc chép") hoặc bỏ.
- **Một hình ảnh xuyên suốt** lấy từ chính sử liệu (ví dụ tước Giao Vương), gieo ở mở đầu, nhắc ở cao trào, khép ở câu kết.
- **Nhịp kể:** câu ngắn khi hành động, câu dài hơn khi giải thích. Gọi đúng tên phe theo thời (năm 938 là "quân của Ngô Quyền", chưa phải "quân Đại Việt"). Không nói tắt ("thủy triều rút xuống", không "nước rút").
- **Hài:** chỉ nhắm vào tình huống hoặc phía xâm lược, không đùa anh hùng dân tộc (`su-viet.md`).

### 3.3 Hồ sơ gửi duyệt
- File `ke-hoach/<mã>-<tên>-gui-duyet.md` gồm các phần sau:
  - Kịch bản đủ, chia chương, ghi phần trăm thời lượng mỗi chương.
  - 3 phương án hook.
  - Ghi chú độ chắc: nguồn, chỗ các nguồn chép khác nhau, các đoạn diễn giải.
  - Ghi chú kỹ thuật kể chuyện.
  - Tỷ lệ thời điểm biến cố chính.
  - Kết quả ba bộ kiểm.
- `kiem_kich_ban.py`, `kiem_mach_ke.py`, `kiem_mo_dau.py` phải đều 0 ❌. Cảnh báo nào được chấp nhận thì ghi lý do.
- Kịch bản được chủ kênh duyệt rồi mới đọc giọng.

## 4. Hình: tranh thủy mặc
### 4.1 Phong cách
- **Màu:** giấy `#ece2cb` có vân và vết loang; mực `#15130f` với ba mức đậm nhạt; đỏ triện `#a3261c`.
- **Màu đỏ chỉ dùng cho:**
  - triện (năm, tước hiệu);
  - nhãn và đường đi của phe địch;
  - mặt trời;
  - nét gạch tên.
- **Chữ:** Lora, có rung nhẹ cho giống nét cọ.
- **Nhân vật** là bóng mực, không vẽ chi tiết khuôn mặt. Trang phục chung chung theo thời: khăn, mũ quan có hai cánh, mũ trụ, giáo, khiên.
- **Những thứ không vẽ:** cờ có chữ, chữ Hán, vật thời hiện đại.
- **Không có máu.** Cái chết được thể hiện bằng mực đỏ loang, triện rơi hoặc vỡ, thuyền lật chìm.
- **Logo** đặt góc trên bên phải, cỡ 130 px, độ đậm 0,8, như mọi video của kênh.

### 4.2 Bản đồ để chỉ chỗ, tranh để kể việc (chủ kênh nhắc 16/11/2026)
- Bản đồ mực vẽ từ đường bờ biển và sông thật (`mapink.py` dùng `world7.jpg`). Chỉ dùng bản đồ khi lời kể nói về vị trí hoặc đường đi. **Không để quá hai đoạn liền nhau chỉ có bản đồ.**
- **Đoạn nào kể một sự việc thì phải có tranh riêng.** Bộ tranh đã có trong `assets.html`:

  | Sự việc | Tranh |
  |---|---|
  | Giết người | sảnh phủ, người ngồi, người cầm kiếm bước ra |
  | Hành quân | hàng quân |
  | Sai sứ | người khiêng hòm |
  | Triều đình địch | ngai, lọng, quan cúi chào |
  | Đánh thành | tường thành, lầu, quân áp sát |
  | Xuất quân | đoàn thuyền rời cảng |
  | Bàn kế | chủ tướng bên án thư, các tướng hai bên |
  | Kinh đô | thành, nhà |

  Tập mới cần sự việc chưa có tranh thì vẽ thêm tranh vào `assets.html`, không dùng bản đồ thay.
- **Mỗi đoạn có ít nhất một chuyển động**, khoảng 3–6 giây có một thay đổi. Các kiểu chuyển động: máy quay trôi hoặc đẩy, quân và thuyền di chuyển, nét cọ vẽ dần, triện đóng xuống, nhãn tên hiện ra.

### 4.3 Cảnh trận
- **Cảnh nhiều lớp có thị sai** (lớp xa trôi chậm hơn lớp gần), xếp từ sau ra trước:
  1. núi xa;
  2. sương;
  3. núi gần;
  4. mặt nước có sóng;
  5. cọc hoặc vật cản;
  6. thuyền theo ba hàng xa gần;
  7. vách đá tiền cảnh;
  8. lau sậy ở mép dưới khung hình.
- **Thông tin kế sách** (cọc, thủy triều, phục binh) chỉ hiện ở đúng chương của nó, để giữ bí mật của hook. Trước đó, cọc dưới nước để mờ hẳn.
- **Thủy triều có thước đo** ở góc màn hình. Cọc nhô lên theo đúng mực nước. Thuyền mắc cọc thì treo lại trên cọc rồi nghiêng, lật, chìm, kèm nước bắn.
- **Đoạn giao chiến** có tên bay, máy quay rung nhẹ, quân hai bên áp vào.
- **Mặt cắt lòng sông** dùng để giải thích kế sách: thủy triều lên xuống, cọc được đóng xuống đáy.

### 4.4 Mở đầu, chuyển chương, kết
- **Giây 0:** đã có hình và chữ lớn trên màn hình (câu hỏi của hook). Không mở bằng logo hay đoạn giới thiệu.
- **Thẻ tựa** sau hook: vệt mực loang, tên trận và triện năm.
- **Chuyển chương:** vệt mực loang có tên chương. Trong cùng một chương, các cảnh chuyển nhau bằng vệt quét có mép rách.
- **Phụ đề** hiện toàn văn ở dưới khung hình, trên nền giấy mờ.
- **Màn kết:** câu kết viết tay, triện tên trận, tên kênh.

### 4.5 Bản dọc
- Khung 1080×1920. Máy quay đặt cỡ khoảng 1,78 lần để tranh ngang phủ kín chiều cao khung.
- Chữ lớn ở phía trên, phụ đề ở khoảng y = 1650.
- Dùng lại cảnh trận và mặt cắt lòng sông. Cảnh cuối là "Xem bản đầy đủ trên kênh Người Gác Sử".

## 5. Âm thanh
- **Tất cả tự tổng hợp** bằng `sfx.py`, không dùng bản ghi có bản quyền.
- **Âm nền:** sóng, gió nhẹ, hải âu, nước vỗ mạn thuyền.
- **Âm theo hình:**

  | Hình | Âm |
  |---|---|
  | Giọt mực mở đầu | tiếng giọt rơi |
  | Thẻ tựa, thẻ chương | cồng |
  | Triện đóng xuống | tiếng đóng triện |
  | Nét vẽ đường đi | tiếng cọ quét |
  | Đóng cọc | tiếng gỗ |
  | Thủy triều lên, xuống | tiếng nước dâng, rút |
  | Hành quân | bước chân, trống |
  | Giao chiến | mái chèo, tù và, trống dồn, tên bay, binh khí va nhau, tiếng hô |
  | Thuyền lật | gỗ gãy kèm nước bắn |

- **Nhạc nền:** đàn gảy âm ngũ cung trên nền âm trầm, đổi không khí theo chương:

  | Chương | Không khí |
  |---|---|
  | Mở đầu | căng |
  | Bối cảnh | mờ |
  | Bàn kế | bình |
  | Giao chiến | loạn |
  | Mất mát | buồn |
  | Kết | sáng |

- **Mức âm:** bản chưa có giọng khoảng −16 LUFS. Khi có giọng:
  - giọng ở −16 LUFS;
  - hiệu ứng tự giảm khi đang đọc;
  - giữ rõ trống và tù và ở các bước ngoặt;
  - không dùng tiếng xẹt hay mưa rè (chủ kênh từng phàn nàn "nhiều tiếng xẹt xẹt").

## 6. Quy trình mỗi tập
1. Nghiên cứu: lập khung sự kiện, đối chiếu Toàn thư và Cương mục, ghi các chỗ nguồn chép khác nhau.
2. Viết kịch bản theo khung ở mục 3, chạy ba bộ kiểm, gửi duyệt kèm 3 phương án hook.
3. Chủ kênh duyệt, rồi Claude đối chiếu lại các chi tiết ít người biết với bản dịch chính sử.
4. Đọc giọng Charon (workflow `thu-giong-hai.yml`, chỉ chạy khi chủ kênh yêu cầu), nhận dạng giọng từng đoạn, đạt 100% ở `kiem_giong.py`.
5. Vẽ thêm tranh cho các sự việc mới (`assets.py`). Soi từng tranh ở cỡ lớn.
6. Gắn cảnh theo thời gian thật của giọng: thay thời lượng ước theo số chữ bằng `thoi_luong.json`. Soi tờ ghép khung (`sheet.py`) cho mọi cảnh trước khi dựng cả video.
7. Dựng bản dài và bản dọc bằng `dai.py` và `doc.py` (24 khung/giây, chia hai tiến trình), trộn âm bằng `amthanh.py`, ghép bằng ffmpeg.
8. Xem lại video đã dựng: trích khung ở các điểm chuyển cảnh và đoạn cao trào.
9. Làm ảnh bìa có logo, theo `chung.md`.
10. Giao cho chủ kênh. Sau khi đăng, ghi số liệu giữ chân người xem.
