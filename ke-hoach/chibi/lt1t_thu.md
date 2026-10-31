# Thử vẽ ảnh Lý Thường Kiệt theo bộ quy tắc prompt mới (mã `lt1t`)

Bộ quy tắc: bố cục trước chi tiết, chia nhóm người, một hành động chính, một Style Prompt cố định, giải phẫu người và ngựa, template A/B/C. FLUX.1 schnell không dùng negative prompt (không có hướng dẫn tương phản), nên các ràng buộc giải phẫu được ghi thẳng vào prompt. Prompt giữ dưới 256 token vì bộ mã hóa chữ cắt ở đó.

| Mã | Loại cảnh | Template | Người | Ngựa | Rủi ro |
|---|---|---|---|---|---|
| 19901 | Army Formation | Template A | 20 soldiers | 0 | Low |
| 19902 | Cavalry | Template B | 15 infantry + 3 riders | 3 | Medium |
| 19903 | Battlefield | Template C | about 24 soldiers, two armies | 0 | High |
| 19904 | Architecture | Template A | about 10 tiny figures | 0 | Low |
| 19905 | Small Group | Small group | 3 men | 0 | Medium |
| 19906 | Landscape | Landscape | 5 tiny figures | 0 | Low |

Chưa kiểm chứng: diện mạo Lý Thường Kiệt không có chân dung đáng tin, ảnh 19905 chỉ là một tướng già khái quát; trang phục Việt thời Lý dùng mô tả chung đã ghi ở `quy-tac` ảnh của series.