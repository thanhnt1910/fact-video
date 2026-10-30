# Ảnh phẳng lt1: việc cần sửa và quyết định (ghi 30/10/2026)

Chủ kênh chọn kiểu ảnh phẳng (vector) thay chibi/FLUX. Mã nguồn: `phim_ban_do/phang/`. Ảnh: `assets/anh_phang/lt1/` (64 ảnh, bản thường), `assets/anh_phang/lt1_ct/` (4 ảnh mẫu chi tiết cao).

## Đã có
- `flat.py` (thư viện nhân vật, nền), `canh.py` (64 cảnh 19002–19096), `ve.py` (vẽ ảnh).
- `chitiet.py`: mức chi tiết cao (bật `flat.DETAIL=True`): mắt, mí, nếp áo, hoa văn, giáp vảy, nền nhiều lớp. Mới có 4 ảnh mẫu (19054, 19066, 19071, 19085), chưa áp cho 64 ảnh.
- `dong.py`, `dongthat.py`: demo chuyển động theo lớp (cờ, nước, máy quay, chèo, quân bước). `nguoi_nghieng.py`: cách A, nhân vật nhìn nghiêng tay chân tách rời (đi bộ, chèo bằng tính toán từng khung).
- Dựng demo: chụp từng khung bằng Playwright, khoảng 1 giây mỗi khung; video 10 phút phải dựng song song trên workflow.

## Lỗi còn lại trong 64 ảnh bản thường
- 19002: bao tải trông như quầng sáng sau mũ.
- 19016: cổ áo bắt chéo trên vua trông như chữ X đỏ.
- 19015: đường bao kiếm còn thô.
- 19038: góc nhìn từ trên cao còn đơn giản.
- 19043: lính bên phải xếp chồng thành một cột.
- 19048: khói là các vòng tròn chồng nhau, hơi máy móc.
- 19064: dải cực quang chưa đối chiếu với lời kể, chưa chắc đúng ngữ cảnh.
- 19092: người đứng chồng lên ngai ở giữa.
- 19047, 19068: đã sửa (bỏ bao tải trên đầu, dời người ngồi) nhưng chưa xem lại.

## Lỗi trong 4 ảnh chi tiết cao
- 19054: mũ cánh ngang của hai quan đứng gần nhau chạm nhau; ánh đèn dầu đè lên hai quan hai bên.
- 19085: bụi cỏ trên nền đất giống mầm cây.
- 19066: vệt bụi hình elip hơi lộ liễu.
- 19071: thuyền đã vẽ lại (mũi đuôi cong, ván ghép, mái chèo); chủ kênh chưa xác nhận dáng thuyền.

## Chuyển động: các điểm chủ kênh chê và việc cần làm
- Chuyển động theo lớp (bản 1, 2) bị chê "giả": người chỉ nhún lên xuống. Chủ kênh muốn người di chuyển, mái chèo chèo thật, nước chuyển động.
- Chọn cách A: nhân vật nhìn nghiêng tay chân tách rời. Việc còn lại:
  - Mặt nhìn nghiêng còn đơn giản (mũi nhọn, miệng chưa đẹp).
  - Bước chân hơi dài, lính trông như đi nhanh; cần chỉnh biên độ và nhịp.
  - Tay lính chưa nắm cán giáo (giáo đứng cạnh người); tay chèo đã nắm cán.
  - Chưa có bản nhìn nghiêng cho quan Tống, vua (mũ miện), áo dài, ngựa, voi.
  - Chưa làm cảnh chạy, cưỡi ngựa, cưỡi voi, đánh nhau.
- Cảnh đứng yên giữ nhân vật đối diện; cảnh có di chuyển dùng nhân vật nhìn nghiêng. Chủ kênh chưa chọn cảnh nào làm chuyển động trước.

## Chờ chủ kênh quyết
- Áp mức chi tiết cao cho cả 64 ảnh hay không (chờ duyệt dáng thuyền và mức chi tiết).
- Cảnh nào trong 64 cảnh làm chuyển động trước.
- Dựng video đủ độ dài cần chạy workflow; chỉ chạy khi chủ kênh yêu cầu.

## Đã sửa 30/10/2026 (phiên tiếp theo), cần chủ kênh xem lại
- 19002 (bao tải đặt ở ngực, không còn như quầng sáng), 19016 (cổ áo giao lĩnh dạng chữ V, áp cho mọi nhân vật), 19015 (bao kiếm có viền rõ), 19038 (thêm ruộng và bờ sông), 19043 (quân Tống rải dọc thung lũng, không xếp cột), 19048 (khói thành cột liền), 19064 (nét sáng vàng nhạt thay dải cực quang xanh tím), 19092 (người dời xuống dưới bậc ngai).
- 19047, 19068 đã xem lại: ổn. Chưa sửa: 4 ảnh chi tiết cao (19054, 19066, 19071, 19085), chuyển động, dựng video.
