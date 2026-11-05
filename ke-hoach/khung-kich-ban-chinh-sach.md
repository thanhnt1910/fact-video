# Khung kịch bản series "Cách họ cai trị" (chốt 05/11/2026)

Dùng cho MỌI tập của series chính sách cai trị phương Bắc thời đô hộ. Viết kịch bản mới thì làm đúng khung này, không sáng tác cấu trúc khác.

Lý do có khung: bản demo 29 đoạn (chiếu 1407 đến trận Bô Cô) bị chủ kênh xem xong "chưa hiểu video nói về gì". Lỗi: nhồi nhiều việc, thiếu một ý chính, quá nhiều tên, kết bằng trận đánh, cảnh phụ chỉ liệt kê.

## 1. Một tập = một chính sách = một ý chính

- Mỗi tập chỉ trả lời MỘT câu hỏi, viết trước kịch bản bằng một dòng: "Tập này cho người xem hiểu: ___".
- Người xem xem xong phải nhắc lại được ý ấy trong một câu (ví dụ: "Nhà Minh bắt người giỏi về Kim Lăng rồi cho làm quan cho mình; ai không muốn thì phải trốn").
- Việc nào không phục vụ ý chính thì bỏ, dù có trong Toàn thư. Chuyện bỏ để dành cho tập khác.
- Chỉ nói chính sách và hệ quả với dân. Không kể trận đánh, không kết bằng trận đánh hay cái chết của tướng.
- Mỗi tập trọn gói, không "tập sau", không dẫn sang chủ đề khác.

## 2. Giới hạn cho dễ hiểu

| Mục | Mức |
|---|---|
| Thời lượng | 60–120 giây, nhắm khoảng 90 giây |
| Lời đọc | 200–400 chữ, 8–16 đoạn, mỗi đoạn 20–28 chữ (tối đa 32), một hoặc hai câu |
| Tên người mới | Tối đa 3 (ghi đủ họ tên lần đầu). Người chỉ xuất hiện một câu thì gọi theo vai ("viên quan nhà Minh") |
| Số liệu | Tối đa 2 con số cả tập, số nào cũng phải có cảnh phụ minh họa |
| Địa danh | Tối đa 3, mỗi nơi đều hiện trên bản đồ |
| Chính sách / sự kiện | Một chính sách chính. Tối đa 2 ví dụ cụ thể làm chứng |
| Từ khó | Giải thích ngay trong câu, không dùng từ Hán Việt cổ nếu có từ dễ hiểu hơn |

## 3. Bộ khung năm phần

Thứ tự cố định. Cột "đoạn" là số đoạn gợi ý cho tập 12 đoạn.

| Phần | Việc phải làm | Đoạn |
|---|---|---|
| A. Mở | Bắt đầu từ đầu câu chuyện, ngắn, rõ: nhà Minh vừa làm xong gì, người dân đang ở đâu. Câu đầu tối đa 15 chữ, không ngày tháng, không tên lạ. Không dựng cảnh gây tò mò tách khỏi mạch. Câu hỏi của tập nêu ở đoạn 2 hoặc 3, sau khi chuyện đã bắt đầu | 2–3 |
| B. Họ làm gì | Chính sách là gì, ra lệnh thế nào, ai thực hiện. Mỗi đoạn có nguyên nhân hoặc hệ quả, đoạn nào cũng dẫn sang đoạn kế | 3–4 |
| C. Một việc cụ thể | Một ví dụ có người, có nơi, có chi tiết khiến người xem hình dung được (ví dụ cụ thể đã có nguồn, không bịa lời thoại, nội tâm) | 2–3 |
| D. Dân ra sao | Hệ quả với dân thường: mất gì, phải làm gì, né bằng cách nào | 2 |
| E. Kết | Một câu chốt ý chính, nói thẳng điều người xem cần nhớ. Kết bằng kết cục của chính chuyện. Không tóm tắt lại cả tập, không lời bàn của sử gia, không so với thời nay | 1 |

Quy ước viết lời:
- Kể như kể chuyện cho bạn nghe một lần là hiểu. Mỗi sự kiện có nguyên nhân và hệ quả, mỗi câu nối sang câu sau. Tránh liệt kê sự việc.
- Lời kể không nhắc tên sách, không "sử chép". Nguồn ghi ở mô tả và bình luận ghim.
- Một sự việc chọn một nguồn đáng tin nhất, không kể "sách này nói thế, sách kia nói khác". Chỗ chưa rõ thì bỏ khỏi lời kể.
- Không đùa cợt, không hài về nạn nhân; không bịa cảm xúc. Không có máu me hay cảnh giết (nói gián tiếp: bóng, dấu vết, hậu quả).
- Không mở các đoạn liền nhau bằng cùng một chữ; xen câu rất ngắn (dưới 8 chữ) để nhấn ý. Hạn chế "tức là", "nghĩa là".
- Họ tên đủ, năm viết bằng chữ trong lời đọc, không nói tắt ("thuyền chiến của quân Nguyên", không "thuyền Nguyên").
- Giữ nguyên quy tắc kiểm trong `phim_ban_do/kiem_kich_ban.py` (0 lỗi trước khi đọc giọng).

## 4. Cảnh phụ: mỗi đoạn một cảnh, không để video đơn giản

Phản hồi 05/11/2026: bản demo "khá đơn giản". Quy tắc dưới đây bắt buộc.

- **Mỗi đoạn có một cảnh riêng, đổi cảnh ít nhất mỗi 4–6 giây.** Không để một khung đứng yên cả đoạn dài.
- **Ít nhất một nửa số đoạn là cảnh vẽ hoạt hình** (người, vật, đoàn người, ruộng, thuyền, sổ sách chuyển động), không phải thẻ chữ. Thẻ chữ chỉ dùng để tóm số liệu hoặc so sánh.
- **Mỗi cảnh phải có chuyển động có nghĩa** (người đi, vật di chuyển, nét vẽ hiện dần, mũi tên chỉ hướng). Không chỉ làm mờ hiện lên.
- **Không dùng cùng một loại cảnh quá hai đoạn liên tiếp.** Thư viện loại cảnh:
  1. bản đồ zoom tới nơi xảy ra việc, có đường đi của người hoặc lệnh;
  2. đoàn người đi trên đường (bị áp giải, di chuyển, chạy nạn);
  3. văn bản: cuộn chiếu, bảng yết, sổ hộ, hiện chữ từng dòng;
  4. cảnh nơi chốn: chợ, ruộng, bãi muối, bến thuyền, cổng thành, vẽ phẳng nhiều lớp có người;
  5. so sánh trước/sau (cái của dân trước, sau chính sách);
  6. biểu đồ số đơn giản (một con số lớn, một thanh đo, một phép chia);
  7. đồng hồ hoặc dòng thời gian, tối đa 4 mốc;
  8. chân dung vai trò (kiểu `face_sprite`, không vẽ mặt thật) kèm tên và chức, chỉ khi người ấy xuất hiện lần đầu.
- **Lớp nền mỗi cảnh luôn có chi tiết** (đồi, nhà, cờ, sương, ánh sáng); bản đồ làm nền chung nhưng cảnh phụ che bản đồ ở nửa trên nên phải đẹp, không để trống.
- **Màu và không khí theo từng phần của khung:** A trầm, ấm; B lạnh, gọn; C sáng rõ vào chi tiết; D ấm xám, nặng; E sáng dần.
- **Chữ trên màn hình rất ít:** tối đa một lớp chữ lớn mỗi lúc; thẻ số tối đa 2 cái cả tập; không đặt thẻ chữ lên cảnh đang chuyển động chính.
- **Bản đồ phải đúng chủ quyền** (không vẽ đường biên, nguồn tô màu chỉ minh họa). Bản đồ chỉ dùng khi việc gắn với địa điểm.
- **Logo cây đèn của kênh** ở góc trên phải, đúng cỡ của video bản đồ. Phụ đề nằm cao hơn vùng dưới của Facebook Reels (tránh chồng tên kênh và tiêu đề).
- Mỗi tập có bảng cảnh phụ kèm theo kịch bản (xem mục 6) để chủ kênh duyệt trước khi dựng.

## 5. Quy trình, theo đúng thứ tự

1. Chủ kênh chọn tập (chính sách) từ dàn ý `ke-hoach/chinh-sach-cai-tri-series-dan-y.md`.
2. Đọc nguyên văn nguồn (Toàn thư, hoặc sách khác với tập mùa Hán, Ngô, Đường); ghi số dòng. Mỗi tập chỉ dùng chi tiết đã đọc nguyên văn.
3. Viết "ý chính một dòng", bảng bố cục năm phần và bảng cảnh phụ.
4. Viết kịch bản theo khung. Tự kiểm: người chưa biết chuyện đọc một lần có hiểu không; có đủ A–E không; giới hạn mục 2.
5. Chạy `python phim_ban_do/kiem_kich_ban.py <tên>` đến khi 0 lỗi.
6. Gửi chủ kênh duyệt (gửi lại file sau mỗi lần sửa). Chưa duyệt thì chưa đọc giọng, vì sửa sau khi đọc tốn hạn mức Gemini.
7. Giọng Gemini Orus, đọc từng câu (`cum=1`), cùng một mô hình cho cả tập; khóa hết hạn mức thì dừng và báo.
8. Sau khi đọc: nhận dạng, `kiem_giong.py`, cân âm lượng và nhịp; đoạn lệch tự phát hiện bằng công cụ, không nhờ chủ kênh nghe. Không thêm vang, nén hay đổi cao độ.
9. Dựng, xem khung hình cỡ lớn, chạy `kiem_video.py` (0 ❌), rồi mới giao.
10. Workflow chỉ chạy khi chủ kênh yêu cầu đúng tập đó.

## 6. Mẫu trình bày một tập (điền khi viết kịch bản)

```
Tập N: <tên>
Ý chính một dòng: ...
Nguồn đã đọc nguyên văn: <sách, quyển, dòng>
Tên mới: (tối đa 3) ...   Số liệu: (tối đa 2) ...   Địa danh: (tối đa 3) ...

| Đoạn | Phần | Lời đọc (20–28 chữ) | Cảnh phụ (loại, chuyển động) | Nguồn |
|---|---|---|---|---|
| 1 | A | ... | ... | dòng ... |
...
Kiểm: ý chính / A–E đủ / giới hạn / kiem_kich_ban 0 lỗi / số chữ, ước thời lượng
Chi tiết đã bỏ (để dành tập khác): ...
```

Ước thời lượng: số chữ chia 3,3 (giọng Orus khoảng 3,3–3,6 chữ mỗi giây), cộng khoảng 1 giây mỗi đoạn cho quãng nghỉ.

## 7. Giao video

- Tiêu đề một dòng, gọn, gây tò mò, đúng sự thật. Hashtag 5–8 thẻ, viết không dấu (ví dụ #NguoiGacSu #CachHoCaiTri #NhaMinh #LichSuVietNam).
- Nguồn ghi ở mô tả và bình luận ghim; bình luận ghim theo quy định chung của kênh.
- Nói rõ điều gì đã kiểm, điều gì chưa.

## 8. Các tập gợi ý để làm lại bằng khung này

| Tập | Ý chính một dòng | Nguồn đã đọc |
|---|---|---|
| Lùng người tài | Nhà Minh bắt người giỏi về Kim Lăng rồi cho làm quan cho mình; ai không chịu thì phải ẩn đi | Toàn thư dòng 16222–16230, 16790–16810 |
| Biến nước thành quận huyện | Chỉ qua một tờ chiếu, nước thành các dòng trong sổ: phủ, châu, huyện, hộ | Toàn thư dòng 16118–16122, 16174–16175 |
| Muối và ruộng | Dân bị kiểm đến từng bát muối, từng mẫu ruộng | Toàn thư dòng 16795–16806 |
| Sổ hộ | Nhà nước biết từng hộ để thu thuế và bắt phu | Toàn thư dòng 16763–16780, 16991–16999 |

Mỗi tập vẫn phải đọc lại đúng đoạn nguồn trước khi viết lời.
