# Loạt 'Bí mật biểu tượng' và 'Vĩ nhân' (phần dựng hình và kịch bản vĩ nhân)

> Phần viết kịch bản nằm trong skill viet-kich-ban-bi-mat-bieu-tuong. Nguồn: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`. Chuyển ngày 18/11/2026.

## Phong cách video dọc "BÍ MẬT BIỂU TƯỢNG" mới: giọng Leda và hiệu ứng (chủ kênh duyệt 07/11/2026, từ #07; áp dụng mọi video dọc loạt này, đã dựng lại #01–#06, #08)
Mẫu: `phim_ban_do/doc9x16/trang_vn7b.html` (#07, bản `out/vn7l_doc.mp4`). Chủ kênh đã gửi video của kênh khác làm mẫu về độ đa dạng (hiệu ứng, âm thanh, giọng); ta học KỸ THUẬT, không sao chép nhận diện.
- **Giọng:** Gemini **Leda** (nữ trẻ), lời dặn phong cách ở `ke-hoach/thu-giong-hai/style_nu_tre_sang.txt` (cao độ khoảng 230 Hz; lời dặn mặc định `STYLE_C` ghi "male narrator" nên Zephyr/Leda vẫn ra giọng trầm, phải dùng lời dặn này). Cách đọc: sao chép thành `style_thu.txt` (tệp này ghi đè lời dặn của mọi lượt đọc; XÓA ngay sau khi đọc xong), `cum.txt` = số đoạn của cả video (một lượt gọi, cùng một giọng), `giong.txt` = `Leda`. Giọng gốc, KHÔNG chỉnh âm thanh. Mã video có hậu tố `l` (vd `vn7l`): `ke-hoach/thu-giong-hai/vn7l_full.json`, giọng ở `assets/thu_giong_hai/vn7l_chuan/` (chép từ `leda/`), nhận dạng ở `phim_ban_do/asr_vn7l.json`.
- **Kiểm sau nhận dạng:** `python phim_ban_do/kiem_giong.py <mãl> --nguong 0.95` và `python phim_ban_do/kiem_cat.py <mãl> [--sua]` (chữ dính cuối, lời tràn sang đoạn sau; `--sua` nối lại ranh giới rồi nhận dạng lại hai đoạn). Đạt cả hai mới dựng.
- **Nền:** giấy dó nâu vàng (sợi giấy) xen nền nâu đen, hoa văn mặt trống đồng mờ; đổi theo cảnh bằng hiệu ứng trượt. KHÔNG dùng nền giấy báo kẻ dòng với chữ tên báo, KHÔNG dùng tờ lịch (nhận diện của video khác).
- **Mốc năm/thế kỷ:** bia đá vòm viền vàng đồng ở góc trên (cạnh logo), lật khi đổi mốc.
- **Hình phẳng:** người bóng đen viền trắng (mũ, xẻng, tay giơ), tem đóng, thẻ giấy xé, danh sách có ô tick, bong bóng thoại, đèn rọi, trục thời gian; ảnh tư liệu thật chỉ ở cảnh chính. Mỗi cảnh một kiểu, không lặp một mẫu.
- **Phụ đề:** cụm 2–3 chữ, chữ trắng viền tối cỡ 68, tên riêng và số nằm trên nền vàng đồng bo góc (chữ đen), bật lên nhẹ.
- **Âm thanh nhấn (`sfx.py` loại `boom`):** sóng 45→35 Hz lên 50 ms tắt khoảng 300 ms, thêm thân 90–140 Hz cho loa điện thoại, tiếng giấy quét 0,25 s báo trước và tiếng tách đúng lúc đập. Khoảng 10 cú mạnh mỗi video (thẻ tên, mốc năm, tem, ảnh chính, câu hỏi cuối) và cú nhẹ cho thẻ nhỏ. `dung_9x16.py` cho boom đi đường riêng, KHÔNG bị giọng đọc hạ (nếu qua sidechain gần như không nghe thấy); mức `volume=0.55`, độ to bản trộn khoảng -14 LUFS. Cú mạnh làm khung cảnh rung khoảng 0,4 giây (`HB` trong trang).
- **Trước khi giao:** xem khung hình lớn quanh chỗ chuyển cảnh, đo boom nổi lên so với nền (script đo trong lịch sử phiên), gửi kèm tiêu đề, hashtag, nguồn và ghi công ảnh CC BY.

## Bộ cảnh minh họa mới cho video dọc "Bí mật biểu tượng" (chủ kênh yêu cầu 08/11/2026: mỗi ảnh một lần, cảnh không có ảnh thì vẽ minh họa phẳng)
- Mã: `phim_ban_do/doc9x16/tao_trang_moi.py <N>` ghép `canh_vnN.js` (cảnh viết tay) với `_moi_cc.js`, `_moi_map.js` thành `trang_vnNn.html`. Đã làm #03, #04, #05, #06, #08; #01, #02, #07 không làm lại.
- Mỗi ảnh chỉ một cảnh; cảnh thiếu ảnh dùng hình phẳng (bóng người, trục thời gian, bộ đếm, hoạt hình). Ảnh không đúng vật được nhắc phải ghi "ảnh minh họa".
- Nội dung chính nằm trên y 1290; HUD trên cùng đến y 190; khối nền (nước, đất) không kéo xuống quá y 1290 để khỏi che phụ đề.
- Xem khung lớn mọi cảnh trước khi dựng (`bash sheet.sh <trang> <tag> <giây>…`).

## Độ dài video dọc "Bí mật biểu tượng": không cố định 60–80 giây (chủ kênh yêu cầu 08/11/2026)
- Loạt này không giới hạn 60–80 giây. Độ dài theo lượng thông tin cần thiết: đủ ý, đủ tên, năm, ý nghĩa thì dài bao nhiêu cũng được; không cắt bớt đoạn để cho vừa mức cũ.
- Vẫn giữ đoạn ngắn cho giọng đọc, bố cục cuốn hút (mở nhanh, mỗi 60–90 giây có một "móc" mới) và không độn câu, không lặp ý.

## Mỗi video một dấu ấn riêng: nền, hiệu ứng, phong cách hình (chủ kênh yêu cầu 10/11/2026, áp dụng mọi video loạt Bí mật biểu tượng từ #15)
Nền mặc định chỉ có hai màu (nâu đen và giấy vàng) với họa tiết trống đồng dùng chung nên mọi video trông giống nhau. Từ nay mỗi video phải có bộ nhận diện riêng theo chủ đề của nó.
- **Nền riêng:** chọn chất liệu và bảng màu theo chủ đề (cầu thép: xanh thép + lưới bản vẽ kỹ thuật + đinh tán; trống đồng: đồng; chữ quốc ngữ: giấy cổ, v.v.). Cả hai nền (tối và sáng) đều đổi, không dùng lại họa tiết trống đồng ở video không liên quan đến trống đồng.
- **Một hiệu ứng nền chuyển động đặc trưng** chạy suốt video, nhẹ, không che chữ và nằm dưới vùng phụ đề (y > 1500) hoặc ở mép khung (cầu Long Biên: giàn thép trôi chậm dưới đáy). Cài qua `window.THEME_UPD = t => {...}` trong file `canh_xkN.js` (`tao_trang_moi.py` gọi hàm này mỗi khung); đổi nền bằng cách sửa `DARKG`, `PAPG`, `DR1`, `DR2` ngay đầu file cảnh (mẫu: `canh_xk7.js`, khối "Dấu ấn riêng").
- **Một kiểu cảnh đặc trưng** dùng cho chủ đề (đếm số, trục thời gian, vật dụng vẽ phẳng của chính chủ đề), không dùng lại nguyên bộ cảnh của video trước.
- Khung hình soi ở cỡ lớn phải cho thấy nền mới ở cả cảnh tối lẫn cảnh sáng; chữ vẫn đọc rõ trên nền mới. Giữ nguyên các quy tắc cũ (logo, nội dung chính trên y 1290, phụ đề).
- Ghi dấu ấn đã chọn vào mô tả giao video (một dòng) để các video sau không lặp lại.

## Dựng cảnh có chuyển động và màu có nghĩa (chủ kênh duyệt 10/11/2026 từ bản v2 của #15 Cầu Long Biên; áp dụng mọi video dọc loạt "Bí mật biểu tượng" từ #16, video đã làm giữ nguyên)
Mẫu: `phim_ban_do/doc9x16/canh_xk7.js` (hàm `PH`, `strip2`, `CK`, `shw`); video `out/xk7l_v2_doc.mp4`.
- **Cảnh ảnh phải zoom tới ĐÚNG chi tiết đang nói**, không chỉ phóng nhẹ cả khung. Khai báo cho mỗi cảnh ảnh `F={fx,fy,z,w:[từ,giây dự phòng],r,mark:'x'|'ok',m:[từ,giây dự phòng]}` (tọa độ chi tiết theo phần trăm ảnh, zoom, từ khóa kích hoạt zoom, bán kính vòng khoanh, dấu ✗/✓ và từ khóa của nó). Vòng khoanh vẽ chạy tới chi tiết ngay khi từ khóa vang lên; sau khi zoom xong vẫn trôi chậm tiếp.
- **Chọn tọa độ chi tiết bằng mắt:** xem ảnh có lưới 10×10 (chia ảnh thành lưới đánh số) rồi chọn; không đặt vòng sát mép ảnh (vòng tràn ra ngoài khung ảnh).
- **Dấu ✗ đóng lên điều sai hoặc bị bác, ✓ lên điều đúng**, đúng lúc lời kể nói tới ("nhưng không trúng", "do Eiffel thiết kế?" → ✗; "hãng thắng thầu", "biển kim loại" → ✓).
- **Màu có nghĩa, mỗi video tối đa 3–4 màu:** đỏ `#d8372d` = điều sai, thiếu, bị bác, nguy hiểm; vàng đồng `#e0a63c` = điều đúng, có thật; xanh thép `#7fa6c4` = nền và mốc đầu; kem = trung tính. Dải chữ dùng `strip2(chữ,'bad'|'ok'|'base',cỡ,seed)`. Không dùng cam, xanh lá hay xanh dương lẻ.
- **Không có khoảng hình đứng yên từ 2 giây trở lên:** dải chữ rung nhẹ (`shw`), thẻ ảnh lắc nhẹ, nền có hiệu ứng chuyển động riêng. Tự đo sau khi dựng: lấy khung 4 hình/giây, độ lệch trung bình giữa hai khung liền nhau dưới 0,35 kéo dài từ 2 giây là đoạn đứng yên; phải bằng 0 đoạn (v2: 0; bản cũ: 2).
- **Cảnh vẽ phẳng** vẫn phải có vật chuyển động theo lời (đếm số, đường nối, vật rơi, tháp xoay); không để chỉ một icon đứng yên.
- Cách làm: `python phim_ban_do/doc9x16/tao_trang_moi.py <mã>` rồi dựng với `--trang trang_<mã>n.html`; soi khung lớn từng cảnh trước khi giao (vòng khoanh có nằm đúng chi tiết, dấu ✗/✓ không đè chữ).
- **Chưa biết hiệu quả giữ chân:** đây là thay đổi hình thức, chưa có số liệu. Theo dõi thời gian xem trung bình Facebook của #16 trở đi so với mốc #15 bản cũ trước khi coi là luật cứng.

## Kịch bản "Vĩ nhân": kể đời một con người có thật (chủ kênh yêu cầu 11/11/2026, rút từ video mẫu Benjamin Franklin của kênh khác; áp dụng video kể đời người từ nay)
Video mẫu hay vì là một hành trình từ dưới lên, giọng như bạn kể chuyện, kết quay về hook. Học KỸ THUẬT, không sao chép lời hay nhận diện. Quy tắc này dùng cho video về người; video về vật, công trình vẫn theo mục "Kịch bản Bí mật biểu tượng: xương sống là MẠCH KỂ".
- **Chỉ nhân vật thế giới (chủ kênh chốt 11/11/2026 23:06).** Nhân vật Việt Nam không thuộc hướng "Vĩ nhân"; chuyện người Việt vẫn kể theo các loạt sử Việt và mục "Series lịch sử Việt Nam".
- **Chọn người:** người có đường đi đối lập (nghèo thành giàu, bị coi thường thành được nhớ, thất bại thành thành tựu) và có một vật quen thuộc để mở hook (tờ tiền, tên phố, công trình mang tên ông). Phải đủ nguồn độc lập.
- **Hook (đoạn 1):** từ vật quen thuộc, nêu điều lạ về người trên đó, tối đa khoảng 20 chữ, không năm. Tên người xuất hiện trong 10 giây đầu. Ví dụ kiểu: "Người trên tờ 100 đô chưa từng làm tổng thống ngày nào."
- **Cung kể (mỗi đoạn một ý, nối bằng nguyên nhân – kết quả):** hook → xuất thân → 3–4 mốc đi lên, mỗi mốc là một bước ngoặt (khó khăn, quyết định, hậu quả) → thành tựu lớn → kết. Trục là đường đi của con người, không phải danh sách thành tích.
- **Chuyện nhỏ đời thường có nguồn:** chèn 1–2 chi tiết đáng yêu hoặc tinh nghịch có tài liệu (thư, hồi ký, báo thời đó) để người xem quý nhân vật. Tên tài liệu ghi trong mục nguồn, không bịa lời thoại hay nội tâm.
- **Số neo:** mỗi mốc một con số hoặc một tuổi (tối đa một số mỗi đoạn), hiện bằng con dấu hoặc thẻ chữ ngắn. Phải đúng nguồn.
- **Kết quay về hook:** câu cuối đóng vòng ("cậu bé bỏ học năm 10 tuổi ngày nào, giờ nằm trên tờ tiền…"). Video tự chứa đủ, không treo câu hỏi bỏ ngỏ, không "tập sau".
- **Giọng:** văn nói đời thường, câu ngắn (khoảng 12–14 chữ trở xuống), có thể thêm câu hỏi tự hỏi tự đáp ("Lý do hả? Nhà hết tiền."). Được đùa vào tình huống và chi tiết đời thường; không chê bai nhân vật, không đùa nỗi đau, không đùa anh hùng dân tộc Việt Nam. Vẫn đủ họ tên, không nói tắt, đoạn ngắn cho giọng đọc (20–30 chữ, tối đa 32).
- **Hình:** mỗi câu một hình riêng, con dấu chữ ngắn (tối đa 3 chữ: "HẾT TIỀN", "KHÔNG!"), nền tối cho căng thẳng và bước ngoặt, nền sáng cho phần kể thường. Ảnh tư liệu (chân dung tranh, trang báo, chữ ký) chỉ dùng ảnh công cộng hoặc có giấy phép, ghi công; ảnh không đúng vật phải ghi "ảnh minh họa".
- **Kiểm nguồn nặng tay hơn vì giai thoại nhiều:** tự truyện hoặc hồi ký của chính nhân vật chỉ tính là MỘT nguồn, phải có tiểu sử học thuật hoặc lưu trữ đối chiếu. Giai thoại nổi tiếng nhưng nghi vấn (ví dụ thả diều hứng sét, quả táo của Newton) thì bỏ hoặc nói rõ "theo lời kể". Chi tiết bỏ ghi vào "Chi tiết đã bỏ".
- **Độ dài:** theo cung kể, thường khoảng 70–110 giây (20–30 đoạn); không cắt bớt mốc để cho ngắn, không độn.
- **Gửi duyệt:** ngoài bảng nguồn, thêm bảng "mốc → bước ngoặt → số neo → hình" và ghi rõ hook lật gì, chuyện nhỏ nào, câu kết đóng vòng thế nào. Chạy `kiem_kich_ban`, `kiem_mo_dau`, `kiem_mach_ke`, `kiem_gui_duyet` trước khi gửi. Ghi chủ đề vào `ke-hoach/bi-mat-bieu-tuong-danh-sach-chu-de.md` (không trùng, không chủ đề đã bỏ).
