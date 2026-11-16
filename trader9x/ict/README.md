# Bộ mẫu Trader9x Masterclass (tập MACD, cấu trúc 2 phần)

| File | Việc |
| --- | --- |
| `data.py` | Giá ngày XAU/USD thật (`ALL`, MetalCharts, chỉ ngày giao dịch) → nến H4, tính chỉ báo, in vị trí tín hiệu (`python data.py`). |
| `render.py` | Dựng hình: `frame(t)`; cảnh `intro, card1, p1, card2, p2, check, outro`. Phần 2 khai báo bằng `TERMS`, `P2` (mốc thuật ngữ / câu ứng dụng), `NB_P2` (số nến hiện), `VS_P2` (camera), `CAPS` (phụ đề). Xem thử: `python render.py still 27.6 46.6 ...` → `stills.jpg`. |
| `voice_tl.py` | `PLAN`: gắn từng đoạn giọng vào mốc của cảnh; giãn thời lượng theo giọng thật; `info / audio / render`. |
| `nhac.py` | Nhạc nền lo-fi tự tạo. |
| `dung.sh` | Ghép tất cả: giọng → dựng 2 nửa song song → nhạc → trộn âm thanh. |

Giọng: kịch bản `trader9x/<mã>_cau.json` (giọng Iapetus), ghi tên file vào `trader9x/chay.txt`, đẩy lên nhánh `trader9x-giong` → workflow "Trader9x đọc giọng". Kiểm: ghi tên giọng vào `trader9x/asr.txt` → workflow "Trader9x nhận dạng giọng".

Tập mới: chép thư mục này thành `trader9x/<chỉ báo>/`, thay phần tính chỉ báo trong `data.py`, panel chỉ báo trong `render.py` (`draw_macd`), `TERMS/P2/CAPS`, `PLAN` trong `voice_tl.py`.
