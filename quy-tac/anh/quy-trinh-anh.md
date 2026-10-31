# QUY TRÌNH ẢNH – lưu `detail_tags`, kiểm duyệt Scene Planner, quản lý phiên bản (v1.0 DRAFT, 01/11/2026)

Áp dụng cho mọi video dùng ảnh FLUX. Trạng thái DRAFT: chờ chủ kênh duyệt. Chưa có Scene Planner nào được lập theo quy trình này.

## 1. Nơi lưu và truy vết `detail_tags`
Mọi thứ lưu trong repo (không dùng Worker, D1, R2):
- `ke-hoach/anh/<mã video>/scene-planner.json`: kế hoạch cảnh (một cảnh = một phần tử).
- `ke-hoach/anh/<mã video>/anh.json`: sổ ảnh (một lần vẽ = một bản ghi, không xóa).
- Ảnh nằm ở `assets/anh_sinh/<mã video>/<scene_id>_p<prompt_version>_s<seed>.jpg`, không ghi đè.

**Cảnh trong `scene-planner.json` có các trường bắt buộc:**
```
scene_id, segment_ids, scene_type, expected_people, expected_horses,
composition (tiền cảnh, trung cảnh, hậu cảnh), camera, lighting,
blocks_used  = ["VN_DAU","VN_GIAP", ...]            # mọi khối đã ghép
detail_tags  = [ {"item":"khăn quấn đầu", "block":"VN_DAU", "tag":"artistic_choice",
                  "who":"nhóm tiền cảnh", "bible_ref":"period-ly-tong#C Mũ"}, ... ]
free_text_details = []                               # chi tiết KHÔNG có trong khối; phải rỗng, hoặc có tag và chủ kênh duyệt
image_prompt, prompt_sha256, prompt_version, prompt_chars,
reference_images = [ {"id":..., "purpose":"face_only|costume_only|style_only"} ],
bible_versions = {"master":"1.1","period":"1.2","khoi_prompt":"1.2"},
plan_status, reuse_group
```
**Truy ngược một chi tiết trong ảnh:** ảnh → bản ghi trong `anh.json` (`scene_id`, `prompt_version`) → cảnh trong planner → `detail_tags` → `block` trong `khoi-prompt.json` → `bible_ref` trong Period Bible → mức bằng chứng và nguồn. `bible_versions` cho biết ảnh vẽ theo phiên bản quy chuẩn nào.

**Kiểm bằng máy:** `python phim_ban_do/kiem_scene_planner.py <mã video>` kiểm: đủ trường; mọi `block` có thật và nhãn không nhẹ hơn nhãn trong `khoi-prompt.json`; không có từ cấm khi cảnh không có khối cho phép (nón, mũ lưỡi trai, cờ, bao tải, đèn lồng...); prompt chứa nguyên văn khối STYLE và ANATOMY; số người, số ngựa khớp chữ trong prompt; độ dài prompt (klein tối đa 1.800 ký tự); `bible_versions` khớp phiên bản hiện hành; `free_text_details` rỗng.

## 2. Kiểm duyệt Scene Planner trước khi tạo ảnh
Trạng thái kế hoạch (`plan_status`): `PLAN_DRAFT` → `PLAN_CHECKED` → `PLAN_OWNER_REVIEW` → `PLAN_APPROVED`. Không vẽ ảnh khi chưa `PLAN_APPROVED`.
1. **PLAN_DRAFT:** Claude lập kế hoạch từ kịch bản đã chốt. Nhóm các đoạn cùng cảnh để dùng lại ảnh (`reuse_group`). Cảnh nhiều hơn 3 hành động hoặc hơn 30 người thì đề xuất tách ảnh.
2. **PLAN_CHECKED:** chạy `kiem_scene_planner.py` (0 lỗi) và tự rà theo 6 câu: đúng nội dung kịch bản? Có tự thêm sự kiện, nhân vật, số quân không có trong kịch bản? Mỗi chi tiết mức B/C đã có nhãn? Có cảnh nào dùng cùng một chi tiết nhãn C cho cả đội quân qua nhiều cảnh? Số người, ngựa khả thi cho FLUX? Cảnh bản đồ có chuyển sang bản đồ vector?
3. **PLAN_OWNER_REVIEW:** gửi chủ kênh một bảng: scene_id, các đoạn, loại cảnh, số người và ngựa, mô tả bố cục một dòng, **danh sách chi tiết `artistic_choice` và `cautious_reconstruction` của cảnh**, ảnh tham chiếu dự kiến, rủi ro (Low, Medium, High). Chủ kênh duyệt hoặc sửa từng cảnh.
4. **PLAN_APPROVED:** khóa kế hoạch (ghi phiên bản). Sửa sau khi khóa phải tăng `plan_version` và chỉ cảnh bị sửa được vẽ lại.
5. **Vẽ thử trước:** 6 đến 10 cảnh đại diện (đông người, ngựa, thành, nội thất, đêm). Chấm 8 mục kiểm (Master Style mục 6). Chỉ khi thử đạt mới vẽ hàng loạt.
6. **Vẽ hàng loạt:** chia đợt theo hạn mức Cloudflare, mỗi đợt lưu và đẩy ngay.

## 3. Quản lý phiên bản
**Số phiên bản:** `MAJOR.MINOR-TRẠNG THÁI`. Trạng thái: DRAFT, REVIEWED, APPROVED. Chỉ chủ kênh được chuyển lên APPROVED. Mọi thay đổi ghi vào `quy-tac/anh/CHANGELOG.md` (ngày, file, thay đổi, lý do).
- **Master Style:** đổi khối STYLE hoặc ANATOMY là MAJOR (mọi ảnh cũ thành STALE). Đổi quy tắc khác là MINOR.
- **Period Bible:** đổi nội dung lịch sử hoặc nhãn là MINOR (ảnh dùng khối bị đổi thành STALE); đổi cách trình bày thì không tăng số.
- **khoi-prompt.json:** đổi chữ trong một khối là MINOR; chỉ ảnh dùng khối đó bị ảnh hưởng (tra bằng `blocks_used`).
- **Prompt:** mỗi cảnh có `prompt_version` (p1, p2, ...). Mỗi lần sửa chữ trong prompt là một phiên bản mới, lưu `prompt_sha256` của chuỗi gửi đi.
- **Ảnh:** mỗi lần vẽ là một bản ghi mới trong `anh.json`: `image_id`, `scene_id`, `prompt_version`, `prompt_sha256`, `bible_versions`, `model`, `seed`, `width`, `height`, `reference_images`, `file`, `file_sha256`, `attempt`, `status`, `review` (kết quả 8 mục kiểm, lỗi, ngày), `superseded_by`. Không xóa và không ghi đè ảnh cũ; ảnh bị thay chuyển `status` thành `SUPERSEDED`.
- **Trạng thái ảnh:** `PASS`, `REVIEW`, `REGENERATE`, `SUPERSEDED`, `STALE`. `STALE` = ảnh vẽ theo phiên bản Bible hoặc khối nay đã đổi; không tự vẽ lại, chủ kênh quyết định giữ hay vẽ lại.
- **Khi Bible đổi:** chạy lại kiểm để liệt kê ảnh `STALE` (ảnh có `blocks_used` chứa khối đã đổi) và gửi chủ kênh danh sách. Không tự động vẽ lại ảnh nào.
- **Ảnh tham chiếu:** chỉ ảnh `PASS`, không `STALE`, mới được dùng (Master Style mục 8).
- **Ngân sách vẽ:** mỗi cảnh tối đa 3 lần vẽ lại tự động (`attempt` ≤ 3); sau đó báo chủ kênh sửa prompt hoặc chia ảnh.

## 4. Việc còn mở
- Chưa có quy tắc riêng cho cảnh dùng chung ảnh nhiều đoạn (thời lượng tối đa một ảnh giữ trên màn hình; hiệu ứng chuyển động). Theo quy tắc kênh, không giữ một cảnh tĩnh quá lâu: sẽ cần làm chuyển động hoặc đổi ảnh.
- Chưa có Character Reference được duyệt cho Lý Thường Kiệt.
- Chưa có kiểm tự động số người và ngựa trong ảnh (hiện soi bằng mắt).
