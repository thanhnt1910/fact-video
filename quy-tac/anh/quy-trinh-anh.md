# QUY TRÌNH ẢNH – lưu `detail_tags`, kiểm duyệt Scene Planner, quản lý phiên bản (v1.3 APPROVED, 01/11/2026)

Áp dụng cho mọi video dùng ảnh FLUX. Chưa có Scene Planner nào được lập theo quy trình này.

## 1. Nơi lưu và truy vết `detail_tags`
Mọi thứ lưu trong repo (không dùng Worker, D1, R2):
- `ke-hoach/anh/<mã video>/scene-planner.json`: kế hoạch cảnh (một cảnh = một phần tử).
- `ke-hoach/anh/<mã video>/anh.json`: sổ ảnh (một lần vẽ = một bản ghi, không xóa).
- Ảnh nằm ở `assets/anh_sinh/<mã video>/<scene_id>_p<prompt_version>_s<seed>.jpg`, không ghi đè.

**Cảnh trong `scene-planner.json` có các trường bắt buộc:**
```
scene_id, segment_ids, scene_type,
expected_people, expected_horses,            # BẮT BUỘC, số nguyên (0 nếu không có)
main_characters = ["tên hoặc mô tả nhân vật chính"],   # BẮT BUỘC
positions = "vị trí chủ thể và các nhóm trong khung hình",   # BẮT BUỘC
groups = [ {"name":..., "count":N, "horses":H, "mounted":M, "position":"tiền cảnh trái|trung cảnh|...", "role":..., "faction":"viet|song|dan"} ],
            # BẮT BUỘC. Tổng count = expected_people; tổng horses = expected_horses; mounted = horses (mỗi kỵ binh một ngựa), mounted ≤ count
composition (tiền cảnh, trung cảnh, hậu cảnh), camera, lighting,
blocks_used  = ["VN_DAU","VN_GIAP", ...]            # mọi khối đã ghép
detail_tags  = [ {"item":"khăn quấn đầu", "block":"VN_DAU", "tag":"artistic_choice", "evidence_level":"C",
                  "who":"nhóm tiền cảnh", "bible_ref":"period-ly-tong#C Mũ"}, ... ]
# tag: historical_evidence (A) | cautious_reconstruction (B) | artistic_choice (C); evidence_level giữ mức gốc, không đổi, không gộp
free_text_details = []                               # chi tiết KHÔNG có trong khối; phải rỗng, hoặc có tag và chủ kênh duyệt
image_prompt, prompt_sha256, prompt_version, prompt_chars,
reference_images = [ {"id":..., "purpose":"face_only|costume_only|style_only"} ],
bible_versions = {"master":"1.1","period":"1.2","khoi_prompt":"1.2"},
plan_status, reuse_group
```
**Truy ngược một chi tiết trong ảnh:** ảnh → bản ghi trong `anh.json` (`scene_id`, `prompt_version`) → cảnh trong planner → `detail_tags` → `block` trong `khoi-prompt.json` → `bible_ref` trong Period Bible → mức bằng chứng và nguồn. `bible_versions` cho biết ảnh vẽ theo phiên bản quy chuẩn nào.

**Kiểm bằng máy:** `python phim_ban_do/kiem_scene_planner.py <mã video>` kiểm: đủ trường; mọi `block` có thật và nhãn và `evidence_level` không nhẹ hơn của khối trong `khoi-prompt.json`; `groups` đủ trường, tổng `count` bằng `expected_people`, tổng `horses` bằng `expected_horses`, `mounted` bằng `horses`, prompt có đúng "EXACTLY N horses" với N khớp (cảnh không ngựa thì prompt không được nhắc ngựa hoặc kỵ binh); `bible_ref` phải giải được tới một mục và hạng mục có thật trong Bible; `detail_tags` không nhắc khối ngoài `blocks_used`; ảnh tham chiếu phải có trong danh sách chủ kênh duyệt; có `main_characters` và `positions`; không có từ cấm khi cảnh không có khối cho phép (nón, mũ lưỡi trai, cờ, bao tải, đèn lồng...); prompt chứa nguyên văn khối STYLE và ANATOMY; số người, số ngựa khớp chữ trong prompt; độ dài prompt (klein tối đa 1.800 ký tự); `bible_versions` khớp phiên bản hiện hành; `free_text_details` rỗng.

## 2. Kiểm duyệt Scene Planner trước khi tạo ảnh
Trạng thái kế hoạch (`plan_status`): `PLAN_DRAFT` → `PLAN_CHECKED` → `PLAN_OWNER_REVIEW` → `PLAN_APPROVED`. Không vẽ ảnh khi chưa `PLAN_APPROVED`.
1. **PLAN_DRAFT:** Claude lập kế hoạch từ kịch bản đã chốt. Nhóm các đoạn cùng cảnh để dùng lại ảnh (`reuse_group`). Cảnh nhiều hơn 3 hành động hoặc hơn 30 người thì đề xuất tách ảnh.
2. **PLAN_CHECKED:** chạy `kiem_scene_planner.py` (0 lỗi) và tự rà theo 6 câu: đúng nội dung kịch bản? Có tự thêm sự kiện, nhân vật, số quân không có trong kịch bản? Mỗi chi tiết mức B/C đã có nhãn? Có cảnh nào dùng cùng một chi tiết nhãn C cho cả đội quân qua nhiều cảnh? Số người, ngựa khả thi cho FLUX? Cảnh bản đồ có chuyển sang bản đồ vector?
3. **PLAN_OWNER_REVIEW:** gửi chủ kênh một bảng: scene_id, các đoạn, loại cảnh, số người và ngựa, nhân vật chính, các nhóm (tên, số người, vị trí), mô tả bố cục một dòng, **danh sách chi tiết `artistic_choice` và `cautious_reconstruction` của cảnh**, ảnh tham chiếu dự kiến, rủi ro (Low, Medium, High). Chủ kênh duyệt hoặc sửa từng cảnh.
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
- **Trạng thái ảnh:** `PASS`, `REVIEW`, `REGENERATE`, `MANUAL_REVIEW`, `SUPERSEDED`, `STALE`. `STALE` = ảnh vẽ theo phiên bản Bible hoặc khối nay đã đổi; không tự vẽ lại, chủ kênh quyết định giữ hay vẽ lại.
- **Khi Bible đổi:** chạy lại kiểm để liệt kê ảnh `STALE` (ảnh có `blocks_used` chứa khối đã đổi) và gửi chủ kênh danh sách. Không tự động vẽ lại ảnh nào.
- **Ảnh tham chiếu:** chỉ ảnh `PASS`, không `STALE`, mới được dùng (Master Style mục 8).
- **Giới hạn vẽ lại:** lần vẽ đầu (`attempt` 1) cộng tối đa 3 lần vẽ lại tự động (`attempt` ≤ 4). Vẫn không đạt thì đặt `status` = `MANUAL_REVIEW` và dừng tự động. **Không đổi nội dung lịch sử, nhãn bằng chứng hay tiêu chuẩn hình ảnh để ép cảnh đạt PASS.** Cách xử lý được phép: sửa cách viết bố cục, số lượng, góc máy trong phạm vi Bible, hoặc đề xuất chia ảnh; mọi thay đổi khác do chủ kênh quyết.
- **Kiểm số người, số ngựa:** do người đếm bằng mắt. Số THỰC TẾ ghi riêng ở `dem_thu_cong` = {"nguoi":N,"ngua":N,"nguoi_dem":"...","ngay":"..."}; số DỰ KIẾN là bản chụp `ke_hoach` = {"nguoi":N,"ngua":N} lấy từ Scene Planner lúc vẽ. Hai trường luôn tách riêng, không ghi đè nhau và không ghi đè `expected_people`, `expected_horses` của planner. Ảnh PASS bắt buộc có cả hai và hai bên phải khớp; lệch thì chỉ được REVIEW hoặc REGENERATE. Chưa xây hệ thống đếm tự động.
- **Ảnh tham chiếu được duyệt:** chỉ ảnh có trong `ke-hoach/anh/<mã>/tham-chieu-duoc-duyet.json` (do CHỦ KÊH duyệt, kèm `duyet_boi`, `ngay`), có bản ghi `PASS` và `bible_versions` khớp phiên bản hiện hành. Danh sách này hiện RỖNG. Ảnh cũ (19901 đến 19906 và 24 ảnh thử) là `STALE`, thư mục chứa chúng có file `KHONG_DUNG_LAM_THAM_CHIEU.md`, và `kiem_scene_planner.py` cùng `cf_ve_lt1t2.py` từ chối chúng.
- **Chặn vẽ quá lượt bằng mã:** script vẽ hàng loạt phải gọi `python phim_ban_do/anh_quy_tac.py <mã> <scene_id>` (hoặc `anh_quy_tac.quyet_dinh_ve`) trước mỗi lần vẽ; mã thoát 0 mới được vẽ, 3 là phải chuyển `MANUAL_REVIEW`, và `kiem_scene_planner.py` báo lỗi nếu sổ ảnh vượt lượt.
- **Ảnh vẽ trước quy chuẩn hiện hành** (ảnh thử 31/10, lượt Kaggle cũ) là `STALE`, không dùng làm căn cứ duyệt ảnh tham chiếu hay đánh giá chất lượng theo quy chuẩn mới.

## 4. Việc còn mở
- Chưa có quy tắc riêng cho cảnh dùng chung ảnh nhiều đoạn (thời lượng tối đa một ảnh giữ trên màn hình; hiệu ứng chuyển động). Theo quy tắc kênh, không giữ một cảnh tĩnh quá lâu: sẽ cần làm chuyển động hoặc đổi ảnh.
- Chưa có Character Reference được duyệt cho Lý Thường Kiệt.
- Kiểm số người và ngựa trong ảnh do người đếm (chủ kênh chưa yêu cầu hệ thống tự động).

## 5. Bổ sung 01/11/2026 theo yêu cầu chủ kênh (ĐÃ ĐƯỢC CHỦ KÊNH DUYỆT 01/11/2026; nâng quy trình lên v1.3)
- **Voi:** Scene Planner có `expected_elephants` (mặc định 0), mỗi nhóm có `elephants`, và `elephant_pairs` (mỗi người dắt gắn đúng một con voi, không trùng). Prompt có voi phải ghi "EXACTLY N elephants"; không có voi thì prompt không nhắc voi. Sổ ảnh: `dem_thu_cong.voi` (người đếm) tách khỏi `ke_hoach.voi`; ảnh PASS khi hai số khớp. Chỉ theo dõi voi, chưa mở rộng loài khác.
- **Bản đồ vector:** cảnh bản đồ phải có `map_data_ref`/`map_items` trỏ tới `ban-do-can-xac-minh.json`. Mỗi mục thuộc một loại tách riêng (`DIA_LY`, `DUONG_QUAN_SU`, `DIEN_GIAI`), mặc định `NEEDS_REVIEW`, không tọa độ, không đường biên. Chỉ mục `VERIFIED` kèm `nguon_xac_minh` mới được điền tọa độ hoặc vẽ. Còn mục NEEDS_REVIEW thì bản đồ `BLOCKED_NEEDS_REVIEW` và không PLAN_APPROVED.
- **Đoạn dùng nhiều cảnh:** phải có `segment_cuts` (thứ tự và câu cắt nằm đúng trong lời đọc). **Cảnh giữ từ 20 giây** phải có `motion_plan` (pan, zoom, cắt cận), chỉ thêm ảnh khi thật cần.
- **Chi tiết nghệ thuật:** duyệt `free_text_details` có `approved_by`, `approved_date`, phạm vi `visual_only`; `evidence_level` giữ C sau khi duyệt, không thành dữ kiện lịch sử.
