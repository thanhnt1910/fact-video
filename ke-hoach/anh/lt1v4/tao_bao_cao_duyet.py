"""Sinh các bảng cho chủ kênh duyệt từ scene-planner.json: scene-planner-review.md, chi-tiet-artistic-choice.(json|md), ban-do-can-xac-minh.md."""
import json, os
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f'{D}/../../..')
P = json.load(open(f'{D}/scene-planner.json', encoding='utf-8')); SC = P['scenes']
T = [x['text'] for x in json.load(open(f'{R}/{P["script"]}', encoding='utf-8'))]
W = lambda g: len(T[g - 1].split())
img = [s for s in SC if s.get('render') != 'vector_map']; maps = [s for s in SC if s.get('render') == 'vector_map']
# ---- chi tiết nghệ thuật
ac = []
for s in img:
    for f in s['free_text_details']:
        ac.append(dict(id=f['id'], scene_id=s['scene_id'], segment_ids=s['segment_ids'], item=f['item'], tag=f['tag'], evidence_level=f['evidence_level'], reason=f['reason'], approval_scope='visual_only',
                       noi_luu_de_xuat=f.get('noi_luu_de_xuat'), noi_luu_chi_tiet=f.get('noi_luu_chi_tiet'), decision_mode=f.get('decision_mode', 'OWNER_APPROVAL'), quyet_dinh=f.get('quyet_dinh'), tinh_chat='quy_uoc_hinh_anh', la_du_kien_lich_su=False, owner_decision='PENDING', owner_approved=False, approved_by=None, approved_date=None, evidence_level_after_approval=f['evidence_level']))
json.dump(dict(project='lt1v4', quy_tac=['Chấp thuận chỉ có nghĩa chủ kênh đồng ý về mặt HÌNH ẢNH (visual_only).', 'evidence_level giữ nguyên C sau khi chấp thuận; không bao giờ thành dữ kiện lịch sử (A) hay phục dựng thận trọng (B).', 'Khi vẽ, không được viết chi tiết này như sự thật trong mô tả, bình luận hay lời đọc.'], items=ac), open(f'{D}/chi-tiet-artistic-choice.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# Chi tiết ngoài khối prompt — chủ kênh duyệt (lt1v4)', '', f'{len(ac)} mục. Tất cả `artistic_choice`, `evidence_level = C`, phạm vi duyệt `visual_only`. Duyệt xong vẫn là C: không thành dữ kiện lịch sử. Cột "Nơi lưu đề xuất" chỉ là đề xuất (DRAFT); chưa mục nào được AUTO.', '',
     '| Mã | Cảnh | Đoạn | Chi tiết | Nơi lưu đề xuất | decision_mode | Lý do | Quyết định |', '|---|---|---|---|---|---|---|---|']
for x in ac: L.append(f'| {x["id"]} | {x["scene_id"]} | {x["segment_ids"]} | {x["item"]} | {x["noi_luu_de_xuat"]}: {x["noi_luu_chi_tiet"]} | {x["decision_mode"]} | {x["reason"]} | PENDING (đồng ý / sửa / bỏ) |')
by = {}
for x in ac: by.setdefault(x['item'].split(' (')[0], []).append(x['id'])
L += ['', '## Mục lặp lại (duyệt một lần cho cả nhóm nếu anh muốn)', ''] + [f'- {k}: {", ".join(v)}' for k, v in by.items() if len(v) > 1]
open(f'{D}/chi-tiet-artistic-choice.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
# ---- bản đồ
MD = json.load(open(f'{D}/ban-do-can-xac-minh.json', encoding='utf-8'))
L = ['# Bản đồ M1–M7: dữ liệu địa lý cần xác minh (lt1v4)', '', 'Quy tắc: ' + ' '.join(MD['quy_tac']), '', f'{len(MD["items"])} mục, tất cả NEEDS_REVIEW; chưa có tọa độ, chưa có đường biên; bản đồ bị chặn (`BLOCKED_NEEDS_REVIEW`).', '']
for m in ['CHUNG'] + [f'M{k}' for k in range(1, 8)]:
    sc = next((s for s in maps if s['scene_id'] == m), None)
    L += [f'## {m}' + (f' (đoạn {sc["segment_ids"]})' if sc else ' (dùng cho cả bảy bản đồ)'), '', '| Mã | Loại | Nội dung | Cơ sở kịch bản | Cần xác minh | Nguồn | Trạng thái |', '|---|---|---|---|---|---|---|']
    for x in MD['items']:
        if x['map'] == m: L.append(f'| {x["id"]} | {x["loai"]} | {x["noi_dung"]} | {x["co_so_kich_ban"]} | {x["can_xac_minh"]} | chưa có | {x["trang_thai"]} |')
    L.append('')
open(f'{D}/ban-do-can-xac-minh.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
# ---- bảng duyệt chính
cnt = lambda k: sum(1 for s in img if s['risk'] == k)
R_ = ['# Scene Planner lt1v4 — bảng chủ kênh duyệt (PLAN_OWNER_REVIEW, bản 2)', '',
      f'Bible: master 1.3, period 1.3, khoi-prompt 1.3. {len(SC)} cảnh = {len(img)} ảnh FLUX + {len(maps)} bản đồ vector. Phủ đủ đoạn 1–68. Rủi ro: Thấp {cnt("Low")}, Vừa {cnt("Medium")}, Cao {cnt("High")}. Chưa vẽ ảnh, chưa gọi API, chưa đọc giọng.', '',
      '| Cảnh | Đoạn | Loại | Người/Ngựa/Voi | Nhân vật chính | Nhóm (vị trí) | Rủi ro | Chi tiết nghệ thuật chờ duyệt |', '|---|---|---|---|---|---|---|---|']
for s in SC:
    if s.get('render') == 'vector_map':
        R_.append(f'| {s["scene_id"]} | {s["segment_ids"]} | bản đồ SVG | - | - | {len(s["map_items"])} mục địa lý NEEDS_REVIEW (xem ban-do-can-xac-minh.md) | - | - |'); continue
    g = '; '.join(f'{x["name"]} ×{x["count"]} ({x["position"]})' for x in s['groups'])
    R_.append(f'| {s["scene_id"]} | {s["segment_ids"]} | {s["scene_type"]} | {s["expected_people"]}/{s["expected_horses"]}/{s["expected_elephants"]} | {", ".join(s["main_characters"])} | {g} | {s["risk"]} | {", ".join(f["id"] for f in s["free_text_details"]) or "-"} |')
# thời lượng giữ
m = {}
for s in SC:
    for g in s['segment_ids']: m.setdefault(g, []).append(s['scene_id'])
runs = []
for g in range(1, 69):
    k = tuple(m[g])
    if runs and runs[-1][0] == k: runs[-1][1].append(g)
    else: runs.append((k, [g]))
R_ += ['', '## Nhân vật có tên: hồ sơ, giai đoạn, thấy mặt', '', '| Cảnh | Hồ sơ / giai đoạn | Thấy mặt | Cần quyết râu trước khi vẽ |', '|---|---|---|---|']
for s_ in img:
    if s_.get('ho_so_nhan_vat'): R_.append(f'| {s_["scene_id"]} | ' + '; '.join(f'{h["ma"]} {",".join(h["giai_doan"])}' for h in s_['ho_so_nhan_vat']) + f' | {"có" if s_["thay_mat"] else "không (nhìn từ phía sau)"} | {"CÓ (râu UNDECIDED)" if s_["thay_mat"] else "chưa cần"} |')
R_ += ['', '## Đoạn 66 (hai cảnh L03 rồi L25)', '']
for c in P['segment_cuts']['66']: R_.append(f'{c["thu_tu"]}. **{c["scene"]}** — "{c["cau"]}" ({c["so_chu"]} chữ, {c["thoi_gian_uoc_tinh"]}). {c["ly_do"]}.')
R_ += ['', 'Chủ ý dùng hai cảnh: đoạn 66 gồm hai câu có hai ý đối nhau (vượt biên giới đánh trước / dựng phòng tuyến giữ sông), mỗi câu khoảng 4–5 giây. Cắt đúng ở dấu chấm sau "đất địch", không đổi lời đọc. Phương án khác: dùng L25 cho cả đoạn (bỏ L03 ở đoạn này), nhưng khi đó câu đầu hiện cảnh bờ sông không khớp lời. Em đề xuất giữ hai cảnh.', '',
       '## Ảnh/bản đồ giữ lâu (từ 18 giây) và cách xử lý', '', '| Cảnh | Đoạn | Giữ (giây) | Xử lý |', '|---|---|---|---|']
for k, gs in runs:
    sec = sum(W(g) for g in gs) / 3
    if sec >= 18 and len(k) == 1:
        s = next(x for x in SC if x['scene_id'] == k[0]); R_.append(f'| {k[0]} | {gs[0]}–{gs[-1]} | {sec:.0f} | {s.get("motion_plan", "(thiếu)")} |')
R_ += ['', 'Không đề xuất thêm ảnh mới ở bước này. Chỉ L32 có điều kiện: thêm một ảnh cận sứ giả nếu cắt cận từ ảnh gốc bị mờ.', '',
       '## L32 — kiểm soát voi', '', '- `expected_elephants` = 5; năm cặp (người dắt k ↔ voi k) trong `elephant_pairs`; prompt có "EXACTLY five elephants" và "one attendant per elephant".',
       '- Sổ ảnh: `dem_thu_cong.voi` (số người đếm) tách riêng khỏi `ke_hoach.voi`; PASS chỉ khi hai số khớp. Chỉ theo dõi voi, chưa mở rộng loài khác.', '- Câu giải phẫu voi chưa có trong `khoi-prompt.json` nên nằm ở chi tiết nghệ thuật (mã trong `chi-tiet-artistic-choice.md`), cần anh duyệt; em bỏ "ngà" vì chưa có căn cứ.', '',
       '## Còn tồn tại', '', '- Character Reference Lý Thường Kiệt (L04, L08, L11, L12, L24, L34) chưa duyệt; danh sách ảnh tham chiếu được duyệt rỗng.', '- 33 mục địa lý bản đồ NEEDS_REVIEW.', f'- {len(ac)} chi tiết nghệ thuật chờ anh duyệt.', '- Cảnh rủi ro cao: L17, L27, L32.',
       '- Kịch bản v4 còn 31 ❌ / 13 ⚠️ của `kiem_kich_ban.py` (anh giữ nguyên lời đọc).']
open(f'{D}/scene-planner-review.md', 'w', encoding='utf-8').write('\n'.join(R_) + '\n')
print(len(ac), 'chi tiết nghệ thuật;', len(SC), 'cảnh')
