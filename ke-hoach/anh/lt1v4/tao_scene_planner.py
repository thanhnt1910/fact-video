"""Tạo ke-hoach/anh/lt1v4/scene-planner.json từ kịch bản lt1v4 (68 đoạn) và khối prompt. Không vẽ ảnh, không gọi mạng.
python ke-hoach/anh/lt1v4/tao_scene_planner.py"""
import hashlib, json, os, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, f'{R}/phim_ban_do')
import anh_quy_tac as Q
KP = json.load(open(f'{R}/quy-tac/anh/khoi-prompt.json', encoding='utf-8'))
CUR = Q.phien_ban_hien_hanh()
T = lambda b: KP[b]['text']
DAU = KP['VN_DAU']['chon_mot']; CHAN = KP['VN_CHAN']['chon_mot']
NHAN = {'VN_AO_VAI': 'quần áo lính vải thô', 'VN_GIAP': 'giáp sắt và da (chỉ một phần lính)', 'VN_DAU': 'đầu lính (búi tóc / khăn quấn)', 'VN_CHAN': 'giày dép lính',
        'VN_VU_KHI': 'giáo gỗ đầu sắt', 'VN_TUONG': 'tướng và sĩ quan Đại Việt', 'VN_TUONG_LY_THUONG_KIET': 'Lý Thường Kiệt (người lớn tuổi, râu bạc)',
        'SONG_BO_BINH_NANG': 'bộ binh nặng Tống', 'SONG_CUNG_NO': 'cung nỏ thủ Tống', 'SONG_BO_BINH_NHE': 'bộ binh nhẹ Tống', 'SONG_SI_QUAN': 'sĩ quan Tống',
        'THANH_SONG': 'thành Tống (tường đá xám, lầu cổng gỗ)', 'DOC_DAT': 'dốc đất đắp áp tường', 'VAC_DAT': 'vác đất bằng giỏ', 'DEN': 'đèn dầu đất nung trên bàn thấp',
        'NHA_DAN': 'nhà gỗ đơn giản, sàn chiếu', 'KIEN_TRUC_CUNG': 'cung điện gỗ mái ngói, đấu củng'}
ANAT, STY = T('ANATOMY'), T('STYLE')
G = lambda name, n, pos, role, fac, h=0, e=0: dict(name=name, count=n, position=pos, role=role, faction=fac, horses=h, mounted=h, elephants=e)
FT = lambda item, tag, why: dict(item=item, tag=tag, evidence_level='B' if tag == 'cautious_reconstruction' else 'C', reason=why, owner_approved=False)
C, B_ = 'artistic_choice', 'cautious_reconstruction'
VNS = ['VN_AO_VAI', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI']
sc = []
def S(sid, segs, typ, groups, chars, pos, comp, cam, light, blocks, layout, dau=None, chan=None, scenery='', extra='', ft=(), risk='Medium', reuse=None, note='', ltk=False, elephants=0, pairs=None, tim=''):
    parts = [layout]
    for b in blocks:
        if b == 'VN_DAU': parts.append(dau)
        elif b == 'VN_CHAN': parts.append(chan)
        else: parts.append(T(b))
    if scenery: parts.append(scenery)
    if extra: parts.append(extra)
    people = sum(g['count'] for g in groups)
    if people: parts.append(ANAT)
    parts.append(STY)
    prompt = ' '.join(x.strip().rstrip('.') + '.' if not x.strip().endswith('.') else x.strip() for x in parts)
    tags = [dict(item=NHAN[b], block=b, tag=KP[b]['tag'], evidence_level=KP[b]['evidence_level'], who=(groups[0]['name'] if groups else ''), bible_ref=KP[b]['bible_ref']) for b in blocks if b in KP and KP[b]['tag'] != 'style_rule']
    d = dict(scene_id=sid, segment_ids=segs, scene_type=typ, expected_people=people, expected_horses=0, expected_elephants=elephants, main_characters=chars, positions=pos,
             groups=groups, composition=comp, camera=cam, lighting=light, scenery=scenery, blocks_used=[b for b in blocks], detail_tags=tags, free_text_details=list(ft),
             image_prompt=prompt, prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(), prompt_version='p1', prompt_chars=len(prompt), bible_versions=dict(CUR),
             needs_character_reference=ltk, **({'elephant_pairs': pairs} if pairs else {}), risk=risk, reuse_group=reuse or sid, reference_images=[], plan_status='PLAN_CHECKED', ghi_chu=note, timing_note=tim)
    sc.append(d)
MAPD = json.load(open(f'{R}/ke-hoach/anh/lt1v4/ban-do-can-xac-minh.json', encoding='utf-8'))['items']
def M(sid, segs, note):
    its = [x['id'] for x in MAPD if x['map'] == sid]
    sc.append(dict(scene_id=sid, segment_ids=segs, scene_type='map', render='vector_map', map_note=note, map_data_ref=f'ke-hoach/anh/lt1v4/ban-do-can-xac-minh.json#{sid}', map_items=its,
                   map_status='BLOCKED_NEEDS_REVIEW', plan_status='PLAN_CHECKED', reuse_group=sid,
                   ghi_chu='Bản đồ SVG/GeoJSON của kênh (không dùng FLUX). KHÔNG dựng cho tới khi các mục dữ liệu địa lý liên quan được xác minh; không có tọa độ hay đường biên trong planner.'))
NG = [G('(không có người)', 0, '-', '-', '-')]
# ---------------- Mở đầu
S('L01', [1, 26], 'fortress', [G('lính Tống trên đầu tường', 6, 'trung cảnh, rải đều trên đầu tường', 'canh giữ', 'song')], ['thành Ung Châu'], 'tường thành giữa khung; tiền cảnh là đồng bằng trống',
  dict(fore='đồng bằng trống', mid='tường thành và lầu cổng, sáu lính nhỏ trên đầu tường', back='trời xám'), 'wide establishing, hơi cao', 'ánh sáng xám, trời âm u',
  ['THANH_SONG', 'SONG_BO_BINH_NANG'], 'Wide establishing shot from outside across an empty plain, the city wall fills the middle of the frame; six tiny Song soldiers stand spaced apart along the top of the wall, nobody on the plain in the foreground',
  scenery='Flat open plain under a grey overcast sky', risk='Low', reuse='ung-chau-wall', note='Đoạn 1: không vẽ cái chết hay lửa (kịch bản v4 không nói). Đoạn 26 dùng lại: thành đứng một mình.', tim='Đoạn 1 và đoạn 26 cách xa nhau, không liền.')
S('L02', [2, 27], 'portrait', [G('sĩ quan Tống (tri châu Tô Giám, tạo hình nghệ thuật)', 1, 'tiền cảnh trái, nhìn từ phía sau', 'chỉ huy giữ thành', 'song'), G('lính Tống', 2, 'trung cảnh, sau sĩ quan vài bước', 'hộ vệ', 'song')],
  ['Tô Giám (không có chân dung; tạo hình nghệ thuật)'], 'sĩ quan đứng trên đầu tường, lưng quay về máy, hai lính phía sau', dict(fore='sĩ quan nhìn từ phía sau', mid='hai lính', back='đồng bằng ngoài thành'),
  'medium shot, nhìn từ sau vai', 'ánh sáng xám lạnh', ['THANH_SONG', 'SONG_SI_QUAN', 'SONG_BO_BINH_NANG'],
  'Medium shot: one Song officer stands on top of the city wall seen from behind and slightly from the side, looking out over the plain; two Song soldiers stand a few steps behind him',
  scenery='Plain beyond the wall under a grey sky', risk='Low', reuse='to-giam', note='Đoạn 2 chưa nêu tên; đoạn 27 nêu tên Tô Giám. Tạo hình sĩ quan là phục dựng, không phải chân dung.', ltk=False, tim='Hai đoạn cách xa nhau.')
S('L03', [3, 66], 'army', [G('lính Đại Việt tiền cảnh', 3, 'tiền cảnh', 'hành quân', 'viet'), G('lính Đại Việt trung cảnh', 7, 'trung cảnh', 'hành quân', 'viet'), G('lính Đại Việt hậu cảnh', 6, 'hậu cảnh, nhỏ', 'hành quân', 'viet')],
  ['đoàn quân Đại Việt'], 'ba hàng lính đi về cùng một hướng (bắc) trên đường đất', dict(fore='3 lính', mid='7 lính', back='6 lính nhỏ'), 'wide shot, hơi cao', 'ánh sáng buổi sáng mát', VNS[:1] + ['VN_GIAP'] + VNS[1:],
  'Wide shot, slightly elevated: sixteen Vietnamese soldiers march in three rows along a dirt road through hills, all walking in the same direction. Three soldiers in the foreground, seven in the middle, six small in the background, clearly spaced apart',
  dau=DAU[0], chan=CHAN[0], scenery='Green hills, dry dirt road', risk='Medium', reuse='vn-vuot-bien-gioi', note='Số lính trong ảnh chỉ minh họa, không phải số quân trong sử (kịch bản nói hơn mười vạn người). Không cờ.', tim='Đoạn 66 dùng lại: nửa đầu đoạn.')
S('L04', [4, 5, 60], 'command_room', [G('Lý Thường Kiệt (tạo hình nghệ thuật)', 1, 'giữa khung, nhìn từ phía sau và hơi nghiêng', 'đứng nhìn bản đồ', 'viet')], ['Lý Thường Kiệt'], 'một người đứng bên bàn thấp, mặt quay đi một phần',
  dict(fore='nhân vật từ phía sau', mid='bàn thấp, bản đồ, đèn dầu', back='tường và cột gỗ'), 'medium shot, từ phía sau và hơi nghiêng', 'ánh sáng ấm yếu từ đèn dầu', ['VN_TUONG_LY_THUONG_KIET', 'VN_TUONG', 'DEN', 'NHA_DAN'],
  'Medium shot from behind and slightly from the side: one general stands at a table looking down at an unrolled map with no writing on it, his face partly turned away, a plain timber hall around him',
  ft=[FT('bản đồ cuộn không chữ', C, 'đạo cụ không có trong Bible')], risk='Medium', reuse='ltk-hall', ltk=True, note='Cần Character Reference Lý Thường Kiệt trước khi vẽ loạt nhân vật này. Dùng cho đoạn 4, 5 và 60.', tim='Đoạn 4 và 5 liền nhau (khoảng 19 giây một ảnh): cần hiệu ứng chuyển động.')
S('L05', [6], 'architecture', [G('người hầu trong cung', 3, 'tiền cảnh dưới, nhỏ', 'đi qua sân', 'viet')], ['kinh thành Thăng Long'], 'sân cung điện, ba người nhỏ đi ngang cuối khung', dict(fore='sân lát', mid='cung điện gỗ mái ngói', back='mái và trời'),
  'wide establishing shot', 'ánh sáng buổi sáng mềm', ['KIEN_TRUC_CUNG'], 'Wide establishing shot of a palace courtyard in Thăng Long, three small attendants walk across the courtyard near the bottom of the frame',
  scenery='Open paved courtyard, soft morning haze', ft=[FT('người hầu trong cung mặc áo dài thô, đầu trần', C, 'trang phục người hầu không có trong Bible')], risk='Low', reuse='thang-long', note='Không vẽ vua. Mô tả "khôi ngô" của kịch bản không thể hiện bằng ảnh này.')
S('L06', [7], 'small_group', [G('quan Đại Việt (Lý Thường Kiệt thời trẻ hơn, tạo hình nghệ thuật)', 1, 'giữa đường', 'đi tuần', 'viet'), G('tùy tùng', 3, 'sau quan', 'đi theo', 'viet'), G('dân làng', 4, 'bên phải, làm ruộng', 'làm đồng', 'dan')],
  ['Lý Thường Kiệt thời trung niên (chưa có Character Reference)'], 'một quan đi giữa đường đất cạnh ruộng, ba người theo sau, bốn dân làng bên phải',
  dict(fore='quan và tùy tùng', mid='ruộng lúa', back='làng xa'), 'wide shot', 'ánh sáng ban ngày dịu', ['VN_TUONG', 'VN_AO_VAI', 'VN_DAU', 'VN_CHAN'],
  'Wide shot: one Vietnamese official walks along a dirt road beside rice fields, followed by three attendants; four villagers work in the field on the right side',
  dau=DAU[1], chan=CHAN[0], scenery='Rice fields, a village in the distance', ft=[FT('dân làng mặc áo thô, đầu trần hoặc khăn quấn', C, 'trang phục dân không có trong Bible'), FT('quan ở độ tuổi trung niên', C, 'Bible chỉ mô tả Lý Thường Kiệt lớn tuổi, râu bạc')],
  risk='Low', ltk=False, note='Không vẽ "cờ tiết" (chưa có tư liệu về hình dạng và màu).')
S('L07', [8, 63], 'army', [G('lính Đại Việt tiên phong tiền cảnh', 4, 'tiền cảnh', 'tiến quân', 'viet'), G('lính Đại Việt phía sau', 8, 'trung cảnh', 'tiến quân', 'viet')], ['đạo quân tiên phong'], 'hai hàng lính tiến về phía nam dọc bờ sông',
  dict(fore='4 lính', mid='8 lính', back='đồng bằng nhiệt đới'), 'wide shot', 'ánh nắng rõ, bóng đổ', ['VN_AO_VAI', 'VN_GIAP', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI'],
  'Wide shot: twelve Vietnamese soldiers advance south in two rows along a river bank among palm trees; four soldiers in the foreground, eight behind them, clearly spaced apart',
  dau=DAU[1], chan=CHAN[1], scenery='Tropical lowland, palm trees, calm river', risk='Medium', reuse='chiem-thanh', note='Dùng cho đoạn 8 (1069) và đoạn 63 (chiến dịch Chiêm Thành lần cuối). Địa hình nhiệt đới là suy luận từ hướng nam.', tim='Hai lần dùng cách xa nhau.')
S('L08', [9, 17, 18], 'small_group', [G('Lý Thường Kiệt (tạo hình nghệ thuật)', 1, 'tiền cảnh, nhìn từ phía sau', 'nhìn về phía bắc', 'viet'), G('lính Đại Việt', 2, 'sau tướng vài bước', 'hộ vệ', 'viet')],
  ['Lý Thường Kiệt'], 'tướng đứng trên đồi đá nhìn núi phía bắc, hai lính sau lưng', dict(fore='tướng và hai lính', mid='sườn đồi', back='núi xanh xám chồng lớp'), 'medium wide shot từ phía sau', 'ánh sáng lạnh, có sương',
  ['VN_TUONG_LY_THUONG_KIET', 'VN_TUONG', 'VN_AO_VAI', 'VN_GIAP', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI'],
  'Medium wide shot from behind: one general stands on a rocky hill looking north across distant mountains, two soldiers stand a few steps behind him',
  dau=DAU[2], chan=CHAN[2], scenery='Rocky hill in the foreground, layered blue-grey mountains in the distance, cold light', risk='Low', reuse='ltk-nhin-bac', ltk=True,
  note='Dùng cho 9, 17, 18 (đoạn 17 và 18 là câu hỏi và suy nghĩ về danh nghĩa tiến quân).', tim='Đoạn 17 và 18 liền nhau, khoảng 23 giây: cần hiệu ứng chuyển động.')
# ---------------- Chờ hay đánh
S('L09', [10], 'object_detail', NG, ['không có người'], 'bàn gỗ sẫm với giấy cuộn, nghiên mực, bút lông, ánh sáng cửa sổ', dict(fore='mặt bàn', mid='giấy cuộn', back='mờ'), 'close view', 'ánh sáng cửa sổ mềm', [],
  'Close view of a dark wooden desk with paper scrolls, an ink stone and a brush, soft window light, no people',
  ft=[FT('bàn gỗ, giấy cuộn, nghiên mực và bút lông', C, 'đạo cụ triều đình Tống không có trong Bible; không vẽ Vương An Thạch vì chưa có tạo hình quan văn Tống')], risk='Low', reuse='tong-trieu-dinh', note='Cảnh thay cho Vương An Thạch và chính sách cải cách: không vẽ nhân vật.')
M('M1', [11], 'Vị trí Quế Châu sát biên giới, hai mũi tên cử Thẩm Khởi và Lưu Di từ phía Tống tới. Chỉ dựa trên kịch bản.')
S('L10', [12, 22, 23], 'small_group', [G('lính Tống ở xưởng thuyền', 8, 'tiền cảnh 4, gần thân thuyền 4', 'khuân gỗ', 'song')], ['xưởng đóng thuyền của quân Tống'], 'bờ sông, hai thân thuyền gỗ trên giá, tám lính khuân ván',
  dict(fore='4 lính khuân ván', mid='2 thân thuyền trên giá', back='dòng sông'), 'wide shot', 'ánh sáng ban ngày', ['SONG_BO_BINH_NHE'],
  'Wide shot of a riverside yard: eight Song soldiers carry timber planks toward two unfinished wooden boat hulls resting on wooden supports; four soldiers in the foreground, four near the hulls',
  scenery='River bank, muddy ground', ft=[FT('thân thuyền gỗ đang đóng trên giá đỡ', C, 'chưa có tư liệu kiểu thuyền Tống ở Quế Châu')], risk='Medium', reuse='quang-tay-chuan-bi',
  note='Dùng cho 12 (đóng thuyền, luyện thủy quân), 22 và 23 (nhà Tống chuẩn bị lực lượng ở khu vực sát biên giới). Không vẽ cờ.', tim='Đoạn 22 và 23 liền nhau, khoảng 19 giây.')
S('L11', [13, 50, 51], 'command_room', [G('Lý Thường Kiệt (tạo hình nghệ thuật)', 1, 'đầu bàn phía xa, ba phần tư', 'quyết định', 'viet'), G('sĩ quan Đại Việt', 3, 'hai bên và đầu bàn gần', 'bàn bạc', 'viet')],
  ['Lý Thường Kiệt'], 'bốn người quanh bàn thấp có bản đồ', dict(fore='sĩ quan đầu bàn gần', mid='bàn, bản đồ, đèn dầu', back='cột gỗ'), 'medium shot, ba phần tư', 'ánh sáng ấm từ đèn dầu',
  ['VN_TUONG_LY_THUONG_KIET', 'VN_TUONG', 'DEN', 'NHA_DAN'], 'Medium shot, three-quarter view: four men stand around a low wooden table with an unrolled map with no writing on it, one elderly general at the far end and three officers, one on each side and one at the near end, all looking at the map',
  ft=[FT('bản đồ cuộn không chữ', C, 'đạo cụ không có trong Bible')], risk='Medium', reuse='ltk-hoi-dong', ltk=True, note='Dùng cho 13 (chờ hay đánh), 50 và 51 (nghị hòa). Không vẽ nhà vua (không có tạo hình trong Bible).', tim='Đoạn 50 và 51 liền nhau, khoảng 19 giây.')
S('L12', [14], 'army', [G('tướng Đại Việt (Lý Thường Kiệt)', 1, 'tiền cảnh trái, từ phía sau', 'chỉ huy', 'viet'), G('tướng Đại Việt (Tông Đản, tạo hình nghệ thuật)', 1, 'tiền cảnh phải, từ phía sau', 'chỉ huy', 'viet'), G('lính Đại Việt', 12, 'trung cảnh, hai hàng sáu người', 'đứng chờ lệnh', 'viet')],
  ['Lý Thường Kiệt', 'Tông Đản'], 'hai tướng đứng cạnh nhau, quay lưng, đối diện hai hàng lính', dict(fore='hai tướng', mid='12 lính hai hàng', back='sân đất nện'), 'medium wide shot từ phía sau', 'ánh sáng buổi sáng',
  ['VN_TUONG_LY_THUONG_KIET', 'VN_TUONG', 'VN_AO_VAI', 'VN_GIAP', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI'],
  'Medium wide shot from behind: two Vietnamese generals stand side by side in the foreground, the left one elderly with a grey beard and the right one younger, facing twelve Vietnamese soldiers standing in two neat rows of six in a courtyard',
  dau=DAU[0], chan=CHAN[1], scenery='Packed earth courtyard, soft morning light', ft=[FT('Tông Đản trẻ hơn Lý Thường Kiệt, râu đen ngắn', C, 'không có tư liệu về diện mạo Tông Đản')], risk='Medium', reuse='xuat-quan', ltk=True,
  note='Không vẽ cờ xuất quân (chưa có tư liệu).')
S('L13', [15, 16], 'small_group', [G('nông dân Tống', 3, 'tiền cảnh', 'gặt lúa', 'dan'), G('nông dân Tống', 3, 'trung cảnh', 'bó lúa', 'dan')], ['nông dân nhà Tống'], 'ruộng lúa chín, sáu người chia hai nhóm ba', dict(fore='3 người gặt', mid='3 người bó lúa', back='đồi thấp'),
  'wide shot', 'ánh sáng chiều vàng nhạt', [], 'Wide shot of a rice field at harvest: six Song farmers cut and bundle ripe golden rice, three in the foreground and three further back, clearly spaced apart',
  scenery='Open fields and low hills', ft=[FT('nông dân Tống áo thô, đầu trần hoặc khăn quấn', C, 'trang phục dân Tống không có trong Bible')], risk='Low', reuse='thanh-mieu',
  note='Minh họa chính sách thanh miêu (vay khi lúa còn non, trả khi gặt). Không vẽ quan thu nợ.', tim='Đoạn 15 và 16 liền nhau, khoảng 20 giây.')
# ---------------- Đánh vào đâu
M('M2', [19], 'Hai đạo thủy bộ: đạo thủy (Lý Thường Kiệt) đi dọc biển tới Khâm Châu và Liêm Châu; đạo bộ (Tông Đản) đi thẳng tới Ung Châu. Không ghi số quân trên bản đồ (kịch bản có nói hơn mười vạn người, cần nêu nguồn).')
S('L14', [20], 'small_group', [G('lính Đại Việt xuống thuyền, thuyền trái', 4, 'trung cảnh trái, lội ra bờ', 'đổ bộ', 'viet'), G('lính Đại Việt, thuyền phải', 4, 'trung cảnh phải', 'đổ bộ', 'viet')], ['đạo thủy Đại Việt'], 'hai thuyền gỗ tấp bờ cát, mỗi thuyền bốn lính lội lên bờ', dict(fore='bãi cát', mid='hai thuyền và tám lính', back='biển'),
  'wide shot', 'ánh sáng ven biển', ['VN_AO_VAI', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI'], 'Wide shot of a sandy coast: two wooden boats are pulled onto the shore, eight Vietnamese soldiers wade out of them onto the beach, four near each boat',
  dau=DAU[1], chan=CHAN[1], scenery='Sandy beach, shallow surf, grey sea', ft=[FT('thuyền gỗ lòng nông', C, 'chưa có tư liệu kiểu thuyền chiến nhà Lý')], risk='Medium', reuse='dao-thuy',
  note='Không vẽ cảnh bắt dân (đoạn 20 nói bắt tù binh), chỉ vẽ đổ bộ.')
S('L15', [21], 'army', [G('lính Đại Việt tiền cảnh', 3, 'tiền cảnh', 'hành quân', 'viet'), G('lính Đại Việt giữa', 6, 'trung cảnh', 'hành quân', 'viet'), G('lính Đại Việt sau', 5, 'hậu cảnh', 'hành quân', 'viet')], ['đạo bộ Tông Đản'], 'cột quân đi về phía thành ở xa', dict(fore='3 lính', mid='6 lính', back='5 lính, thành nhỏ ở xa'),
  'wide shot', 'ánh sáng ban ngày', ['VN_AO_VAI', 'VN_GIAP', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI', 'THANH_SONG'],
  'Wide shot: fourteen Vietnamese soldiers march in a column along a road toward a walled city seen small in the far distance; three soldiers in the foreground, six in the middle, five behind, clearly spaced apart',
  dau=DAU[2], chan=CHAN[0], scenery='Open road across low fields', risk='Medium', reuse='dao-bo')
S('L16', [24], 'army', [G('sĩ quan Tống (Trương Thủ Tiết, tạo hình nghệ thuật)', 1, 'tiền cảnh, dẫn đầu', 'chỉ huy', 'song'), G('bộ binh nặng Tống', 5, 'trung cảnh', 'hành quân', 'song'), G('cung nỏ thủ Tống', 6, 'hậu cảnh', 'hành quân', 'song')],
  ['Trương Thủ Tiết (không có chân dung)'], 'cột quân Tống đi trên đường núi: sĩ quan dẫn đầu, năm bộ binh nặng, sáu nỏ thủ', dict(fore='sĩ quan', mid='5 bộ binh nặng', back='6 nỏ thủ'), 'wide shot', 'ánh sáng xám',
  ['SONG_SI_QUAN', 'SONG_BO_BINH_NANG', 'SONG_CUNG_NO'], 'Wide shot: twelve Song soldiers march in a column along a mountain road; one officer leads at the front of the frame, five heavy infantry with round shields and spears follow in the middle, six crossbowmen walk at the rear, clearly spaced apart',
  scenery='Mountain road between steep hills', risk='Medium', reuse='vien-binh-tong', note='Không cờ Tống. Binh chủng chọn theo Bible (nặng + nỏ).')
S('L17', [25], 'battlefield', [G('lính Tống trên đường', 8, 'đường dưới thung lũng', 'đi qua ải', 'song'), G('lính Đại Việt sườn trái', 4, 'sườn dốc trên trái, nấp sau đá', 'phục kích', 'viet'), G('lính Đại Việt sườn phải', 4, 'sườn dốc trên phải', 'phục kích', 'viet')], ['phục kích ở ải Côn Lôn'], 'đường hẹp dưới thung lũng, hai sườn dốc phía trên',
  dict(fore='sườn dốc và đá', mid='cột quân Tống', back='đèo'), 'wide shot, góc cao', 'ánh sáng chiều xuyên khe núi', ['SONG_BO_BINH_NANG', 'VN_AO_VAI', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI'],
  'Wide shot from a high angle of a narrow mountain pass: eight Song soldiers walk in a short column on the road below, and on the steep slopes above, eight Vietnamese soldiers stand hidden among rocks and bushes, four on each side',
  dau=DAU[0], chan=CHAN[2], scenery='Narrow pass between steep rocky slopes', risk='High', reuse='phuc-kich', note='Không vẽ cảnh giết Trương Thủ Tiết hay máu. Chỉ vẽ khoảnh khắc phục kích. Rủi ro cao vì hai phe ở cùng khung.')
S('L18', [28, 65], 'fortress', [G('lính Đại Việt vác đất', 8, 'trên dốc đất', 'vác giỏ đất lên dốc', 'viet'), G('lính Tống giữ thành', 3, 'trên đầu tường', 'canh giữ', 'song')], ['quân vây thành Đại Việt'], 'dốc đất lớn áp tường, tám lính leo dốc, ba lính Tống trên tường', dict(fore='dốc đất', mid='tám lính vác giỏ', back='tường thành'), 'wide shot', 'ánh sáng ban ngày',
  ['VN_AO_VAI', 'VN_DAU', 'VN_CHAN', 'THANH_SONG', 'DOC_DAT', 'VAC_DAT', 'SONG_BO_BINH_NANG'],
  'Wide shot: against a tall grey stone city wall, eight Vietnamese soldiers climb the earth mound carrying baskets of soil, three Song defenders stand on the top of the wall',
  dau=DAU[1], chan=CHAN[1], risk='Medium', reuse='doc-dat', note='Dốc đất: sự kiện theo kịch bản (sử liệu), hình dạng là phục dựng (B). Không vũ khí công thành khác.', tim='Đoạn 65 dùng lại: hai trận cách nhau một năm.')
S('L19', [29], 'architecture', NG, ['sân trong thành Ung Châu'], 'sân đá trống, cửa gỗ khép hờ, không người', dict(fore='sân đá', mid='cửa gỗ', back='tường thành'), 'medium wide shot', 'ánh sáng xám âm u',
  ['THANH_SONG'], 'Quiet empty stone courtyard inside the walls of a Song city, the tall grey stone wall rising behind, wooden doors half open, no people',
  ft=[FT('sân đá trong thành, cửa gỗ khép hờ', C, 'không có tư liệu về bố cục bên trong thành Ung Châu')], risk='Low', reuse='ung-chau-trong', note='Không vẽ cái chết của Tô Giám và người thân (kịch bản v4 đoạn 29).')
S('L20', [30], 'landscape', NG, ['bãi đất trước tường thành'], 'dốc đất bên tường, đất xung quanh vắng, không người', dict(fore='đất trống', mid='dốc đất', back='tường thành trong sương'), 'wide shot', 'bình minh, sương mỏng',
  ['THANH_SONG', 'DOC_DAT'], 'Wide shot at dawn: the ground around the huge earth mound beside the grey stone city wall is empty and quiet, mist over the fields, no people',
  risk='Low', reuse='doc-dat-vang', note='Không vẽ thi thể. Số "hơn năm vạn tám nghìn người" (kịch bản nói là từ sử liệu được nhắc) nên hiện bằng chữ trên màn hình kèm nguồn, không bằng hình.')
S('L21', [31], 'small_group', [G('người dân Tống bị đưa về', 6, 'giữa đường, xếp một hàng', 'đi bộ', 'dan'), G('lính Đại Việt dẫn đầu', 4, 'phía trước hàng dân', 'đi trước', 'viet'), G('lính Đại Việt đi sau', 4, 'phía sau hàng dân', 'đi sau', 'viet')],
  ['người dân bị bắt'], 'đường rời thành: bốn lính đi trước, sáu dân ở giữa, bốn lính đi sau', dict(fore='bốn lính dẫn đầu', mid='sáu dân', back='tường thành xa'), 'wide shot', 'ánh sáng chiều',
  ['VN_AO_VAI', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI'], 'Wide shot: on a road leading away from a Song city, six Song civilians walk in a line in the middle, four Vietnamese soldiers walk ahead of them and four behind, all heading the same direction away from the wall',
  dau=DAU[2], chan=CHAN[0], scenery='Dirt road across fields, the city wall small behind', ft=[FT('dân Tống áo thô, đầu trần hoặc khăn quấn', C, 'trang phục dân Tống không có trong Bible')], risk='Medium', reuse='rut-quan', note='Không dùng xiềng xích, roi, bạo lực (kịch bản không nói).')
M('M3', [32, 33], 'Ung Châu nằm sâu trong lãnh thổ nhà Tống, đường rút về biên giới và về Đại Việt, hai vùng ven biển Khâm và Liêm. Minh họa lý do "không ở lại giữ thành": đường rút dài, có thể bị bao vây.')
# ---------------- Giữ sông
S('L22', [34], 'army', [G('chỉ huy Tống (Quách Quỳ, tạo hình nghệ thuật)', 1, 'tiền cảnh, nhìn từ phía sau', 'chỉ huy', 'song'), G('bộ binh nặng Tống', 6, 'trung cảnh trước, một hàng', 'đứng chờ', 'song'), G('cung nỏ thủ Tống', 5, 'trung cảnh sau, một hàng', 'đứng chờ', 'song')],
  ['Quách Quỳ (không có chân dung)'], 'chỉ huy trên gò cao nhìn xuống hai hàng quân', dict(fore='chỉ huy', mid='6 bộ binh nặng, 5 nỏ thủ', back='đồng bằng'), 'wide shot từ gò thấp', 'ánh sáng nghiêm, trời trong',
  ['SONG_SI_QUAN', 'SONG_BO_BINH_NANG', 'SONG_CUNG_NO'], 'Wide shot from a low hill: one Song commander stands in the foreground seen from behind, looking down at an assembled army of twelve Song soldiers: six heavy infantry in one row and five crossbowmen in a row behind them, clearly spaced apart',
  scenery='Open plain, clear sky', risk='Medium', reuse='quach-quy', note='"Đạo quân lớn" của kịch bản chỉ được gợi bằng 11 lính; không vẽ cờ.')
M('M4', [35], 'Ba mũi áp lực lên Đại Việt: từ phía bắc (nhà Tống), phía nam (Chiêm Thành) và phía tây nam (Chân Lạp). Chỉ dựa trên kịch bản.')
S('L23', [36], 'army', [G('sĩ quan Tống', 1, 'tiền cảnh, dẫn đầu', 'dẫn quân', 'song'), G('bộ binh nặng Tống', 7, 'trung cảnh', 'hành quân', 'song'), G('cung nỏ thủ Tống', 6, 'hậu cảnh', 'hành quân', 'song')],
  ['đại quân Tống'], 'cột quân Tống tiến về phía nam trên đường đất', dict(fore='sĩ quan', mid='7 bộ binh nặng', back='6 nỏ thủ'), 'wide shot', 'ánh sáng xám lạnh cuối năm',
  ['SONG_SI_QUAN', 'SONG_BO_BINH_NANG', 'SONG_CUNG_NO'], 'Wide shot: fourteen Song soldiers march south in a column along a dirt road: one officer at the front, seven heavy infantry with round shields and spears in the middle, six crossbowmen behind them, clearly spaced apart',
  scenery='Dry fields and low hills, cold grey light', risk='Medium', reuse='tong-tien-quan')
S('L24', [37, 67], 'small_group', [G('Lý Thường Kiệt (tạo hình nghệ thuật)', 1, 'tiền cảnh, nhìn từ phía sau', 'nhìn ra sông', 'viet'), G('sĩ quan Đại Việt', 2, 'hai bên, sau một bước', 'đứng bên', 'viet')],
  ['Lý Thường Kiệt'], 'ba người đứng trên bờ nam nhìn qua sông', dict(fore='ba người nhìn từ phía sau', mid='dòng sông rộng', back='bờ bắc mờ'), 'wide shot từ phía sau', 'hoàng hôn',
  ['VN_TUONG_LY_THUONG_KIET', 'VN_TUONG'], 'Wide shot from behind at dusk: a wide river, on the south bank one elderly general with a grey beard stands looking across the water, two Vietnamese officers stand beside him; the far bank is barely visible',
  scenery='Wide calm river, flat banks, low evening light', risk='Low', reuse='ltk-song', ltk=True, note='Đoạn 37 (chọn sông Như Nguyệt) và 67 (hai nước cờ, kết).', tim='Hai đoạn cách xa nhau.')
M('M5', [38, 39], 'Sông Như Nguyệt (sông Cầu) nằm trên đường từ phía bắc về Thăng Long; vị trí khúc sông và khoảng cách tới kinh thành. Cần dữ liệu địa lý đã kiểm.')
S('L25', [40, 66], 'landscape', [G('lính Đại Việt giữ phòng tuyến', 10, 'rải dọc bờ nam', 'đứng canh', 'viet')], ['phòng tuyến bờ nam'], 'hàng lũy đất cắm cọc dọc bờ, mười lính rải đều', dict(fore='lũy cọc ở bờ gần', mid='mười lính', back='dòng sông và bờ bắc xa'), 'wide shot qua sông', 'ánh sáng sớm',
  ['VN_AO_VAI', 'VN_GIAP', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI'], 'Wide shot across a river: along the near south bank runs a long defensive line, an earth rampart with wooden stakes, with ten Vietnamese soldiers standing spaced along it facing the far bank',
  dau=DAU[2], chan=CHAN[0], scenery='Wide river, flat banks, early light', ft=[FT('lũy đất cắm cọc gỗ dọc bờ nam', C, 'kịch bản chỉ nói "phòng tuyến kiên cố"; kiểu lũy chưa có tư liệu đã kiểm')], risk='Medium', reuse='phong-tuyen',
  note='Đoạn 40 nói "theo những ghi chép và truyền lại về sau". Đoạn 66 dùng lại: nửa sau đoạn.')
S('L26', [41, 42, 43], 'army', [G('lính Tống bờ bắc', 5, 'tiền cảnh, nhìn từ phía sau', 'nhìn sang bờ nam', 'song'), G('lính Đại Việt bờ nam', 8, 'hậu cảnh, nhỏ, sau lũy', 'giữ lũy', 'viet')], ['quân Tống nhìn phòng tuyến'], 'năm lính Tống đứng bờ bắc, bờ nam xa có hàng lũy và tám lính nhỏ', dict(fore='5 lính Tống', mid='dòng sông', back='lũy và 8 lính nhỏ'), 'wide shot từ phía sau lính Tống', 'ánh sáng buổi sáng',
  ['SONG_BO_BINH_NANG', 'VN_AO_VAI', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI'], 'Wide shot from behind: five Song soldiers stand on the north bank in the foreground looking across a wide river, and on the far south bank a long earth rampart with wooden stakes and eight small Vietnamese soldiers behind it',
  dau=DAU[1], chan=CHAN[0], scenery='Wide river, flat banks', ft=[FT('lũy đất cắm cọc gỗ dọc bờ nam', C, 'như cảnh L25')], risk='Medium', reuse='bo-bac', tim='Ba đoạn liền nhau (41 đến 43), khoảng 30 giây một ảnh: cần hiệu ứng chuyển động hoặc đổi sang L25.')
S('L27', [44], 'battlefield', [G('lính Tống lội sông', 8, 'trung cảnh, lội qua dòng nông', 'vượt sông', 'song'), G('lính Đại Việt sau lũy', 8, 'hậu cảnh, sau lũy bờ nam', 'giữ lũy', 'viet')], ['trận vượt sông'], 'tám lính Tống lội nước tiến về bờ nam; tám lính Đại Việt đứng sau lũy', dict(fore='mặt nước', mid='8 lính Tống', back='lũy và 8 lính Đại Việt'), 'wide shot', 'ánh sáng ban ngày',
  ['SONG_BO_BINH_NANG', 'VN_AO_VAI', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI'], 'Wide shot: eight Song soldiers wade into a shallow river carrying round shields toward the far bank, spread across the frame; on the far bank eight Vietnamese soldiers stand behind an earth rampart with wooden stakes, spears held upright',
  dau=DAU[0], chan=CHAN[2], scenery='Shallow river, flat banks', ft=[FT('lũy đất cắm cọc gỗ dọc bờ nam', C, 'như cảnh L25')], risk='High', reuse='vuot-song', note='Rủi ro cao: hai phe trong một khung, nhiều người trong nước. Không vẽ cung tên (chưa có khối vũ khí cung).')
S('L28', [45, 48, 68], 'small_group', [G('lính Đại Việt', 5, 'trước đền, nhóm lỏng', 'đứng lặng nhìn về đền', 'viet')], ['quân sĩ nghe bài thơ'], 'đền nhỏ bên sông phải khung, năm lính đứng trước', dict(fore='bờ sông', mid='năm lính và đền', back='sương trên sông, rặng tre'), 'wide shot', 'đêm có trăng nhạt, sương',
  ['VN_AO_VAI', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI'], 'Wide shot at night under a pale moon, mist over the river: a small wooden riverside shrine with a grey tiled roof stands on the right, lit by a clay oil lamp inside; five Vietnamese soldiers stand quietly in a loose group in front of it, looking toward the shrine',
  dau=DAU[0], chan=CHAN[1], scenery='Wide river at night, mist, bamboo and hills in the distance', ft=[FT('đền nhỏ bên sông mái ngói xám, đèn dầu bên trong', C, 'kiến trúc đền thờ Trương Hống, Trương Hát chưa có tư liệu hình dạng')], risk='Low', reuse='den-ben-song',
  note='Đoạn 45 và 48 theo truyền thuyết. Không vẽ người đọc thơ hay thần linh. Đoạn 68 dùng lại để khép.', tim='Dùng ba lần cách xa nhau.')
S('L29', [46, 47], 'object_detail', NG, ['cửa đền'], 'cửa gỗ chạm khắc của đền nhỏ, ánh đèn dầu, sương phía sau, không người', dict(fore='bậc thềm', mid='cửa gỗ', back='sương'), 'close view', 'ánh sáng ấm yếu từ đèn dầu, đêm',
  [], 'Close view of the wooden doorway of a small riverside shrine at night, soft light from a clay oil lamp, mist behind, no people',
  ft=[FT('cửa đền gỗ chạm khắc đơn giản, đèn dầu đất nung', C, 'không có tư liệu hình dạng đền')], risk='Low', reuse='den-chi-tiet', note='Bài thơ nên hiện bằng chữ trên màn hình (không vẽ chữ trong ảnh).', tim='Đoạn 46 và 47 liền nhau, khoảng 18 giây.')
S('L30', [49], 'small_group', [G('lính Tống ngồi nghỉ, nhóm trái', 4, 'trung cảnh trái', 'ngồi cúi đầu', 'song'), G('lính Tống ngồi nghỉ, nhóm phải', 4, 'trung cảnh phải', 'ngồi cúi đầu', 'song')], ['doanh trại quân Tống'], 'tám lính ngồi dưới đất chia hai nhóm bốn, cạnh lều vải đơn giản', dict(fore='đất ẩm', mid='hai nhóm lính', back='lều vải, sương'), 'wide shot', 'sương ẩm, ánh sáng xám',
  ['SONG_BO_BINH_NHE'], 'Wide shot of a damp riverside camp in humid mist: eight Song soldiers sit on the ground in two groups of four near simple cloth shelters, heads bowed, spears laid on the ground beside them',
  scenery='Wet ground, humid mist, river in the distance', ft=[FT('lều vải đơn giản của quân Tống', C, 'không có tư liệu')], risk='Low', reuse='doanh-trai-tong', note='Bệnh tật thể hiện bằng dáng ngồi, không vẽ thi thể hay người hấp hối.')
S('L31', [52], 'army', [G('lính Tống tiền cảnh', 3, 'tiền cảnh, từ phía sau', 'rút lui', 'song'), G('lính Tống phía sau', 9, 'trung cảnh và hậu cảnh', 'rút lui', 'song')], ['quân Tống rút lui'], 'cột quân đi về phía bắc, quay lưng về máy', dict(fore='3 lính', mid='9 lính', back='đường dài'), 'wide shot từ phía sau', 'ánh sáng xám chiều',
  ['SONG_BO_BINH_NANG'], 'Wide shot from behind: twelve Song soldiers walk away north in a column along a road, three in the foreground and nine behind them, clearly spaced apart',
  scenery='Dirt road across low fields, grey late-afternoon light', risk='Medium', reuse='tong-rut', note='Đoạn 52 nói Quảng Nguyên rơi vào tay nhà Tống: dùng bản đồ M6.')
M('M6', [53, 57, 59], 'Các châu Quảng Nguyên, Tư Lang, Tô Mậu (quân Tống giữ lại); Quảng Nguyên đổi tên Thuận Châu (1079); trại Vĩnh Bình và sáu huyện, ba động được trả (1084). Cần dữ liệu địa lý đã kiểm.')
PR = [dict(handler=f'người dắt {k}', elephant=f'voi {k}', quan_he='đi bên cạnh đầu con voi này, một tay dắt') for k in range(1, 6)]
S('L32', [54, 55, 56], 'small_group', [G('sứ giả Đại Việt (Đào Tống Nguyên, tạo hình nghệ thuật)', 1, 'dẫn đầu đoàn', 'đi đầu', 'viet'), G('người dắt voi (mỗi người một con)', 5, 'mỗi người cạnh đầu con voi của mình', 'dắt voi', 'viet', 0, 5)],
  ['Đào Tống Nguyên (không có chân dung)'], 'sứ giả đi đầu, năm con voi theo hàng một, mỗi con một người dắt riêng', dict(fore='sứ giả', mid='5 con voi và 5 người dắt', back='đường đồng bằng'), 'wide shot từ bên cạnh', 'ánh sáng ban ngày',
  ['VN_TUONG', 'VN_AO_VAI', 'VN_DAU', 'VN_CHAN'], 'Wide shot from the side: one Vietnamese envoy walks at the front of a procession along a dirt road, followed by EXACTLY five elephants in single file. Each elephant is led by one attendant on foot at its head: five attendants and five elephants in total, one attendant per elephant',
  dau=DAU[1], chan=CHAN[1], extra='Each elephant has one head, one trunk and four legs, clearly separated from the others', scenery='Dirt road across open land', elephants=5, pairs=PR,
  ft=[FT('giải phẫu voi: mỗi con một đầu, một vòi, bốn chân, tách rời nhau (câu mô tả đề xuất; khoi-prompt chưa có khối voi)', C, 'chưa có khối voi trong khoi-prompt.json; không thêm ngà vì chưa có căn cứ')],
  risk='High', reuse='su-bo-voi', note='Chỉ theo dõi voi (expected_elephants); chưa mở rộng loài khác. Số voi trong ảnh phải được người đếm, ghi riêng ở dem_thu_cong.voi.', tim='Ba đoạn liền nhau (54 đến 56), khoảng 30 giây: xem motion_plan.')
S('L33', [58], 'small_group', [G('người dân Tống được trả về', 10, 'giữa đường, hai hàng năm người', 'đi về phía bắc', 'dan'), G('lính Đại Việt đi cùng', 2, 'cuối hàng', 'hộ tống', 'viet')], ['người dân và binh lính được trao trả'], 'hai hàng dân đi về phía bắc, hai lính Đại Việt đi cuối', dict(fore='hàng dân', mid='đường đất', back='đồng bằng'), 'wide shot', 'ánh sáng ban ngày dịu',
  ['VN_AO_VAI', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI'], 'Wide shot: ten Song civilians walk north in two loose lines of five along a dirt road, accompanied by two Vietnamese soldiers walking at the rear',
  dau=DAU[0], chan=CHAN[0], scenery='Dirt road across open land', ft=[FT('dân và binh lính Tống được trả: áo thô, đầu trần hoặc khăn quấn', C, 'trang phục không có trong Bible')], risk='Medium', reuse='tra-nguoi')
M('M7', [61], 'Diễn Châu (nơi Lý Giác dấy binh năm 1103). Chỉ dựa trên kịch bản.')
S('L34', [62], 'army', [G('Lý Thường Kiệt (tạo hình nghệ thuật)', 1, 'tiền cảnh, từ phía sau', 'dẫn quân', 'viet'), G('lính Đại Việt', 13, 'sau tướng, ba nhóm', 'hành quân', 'viet')], ['Lý Thường Kiệt'], 'tướng đi đầu, mười ba lính theo sau trên đường ven biển', dict(fore='tướng', mid='lính', back='bờ biển'), 'wide shot từ phía sau', 'ánh sáng ban ngày',
  ['VN_TUONG_LY_THUONG_KIET', 'VN_TUONG', 'VN_AO_VAI', 'VN_GIAP', 'VN_DAU', 'VN_CHAN', 'VN_VU_KHI'], 'Wide shot from behind: one elderly general with a grey beard leads fourteen soldiers in total along a coastal road, he walks alone at the front and thirteen Vietnamese soldiers follow in three groups',
  dau=DAU[2], chan=CHAN[2], scenery='Coastal road, sea on one side', risk='Medium', reuse='dep-loan', ltk=True, note='Số lính chỉ minh họa. Không vẽ cờ.')
S('L35', [64], 'command_room', NG, ['sảnh vắng'], 'sảnh gỗ vắng lúc bình minh, bàn thấp có bản đồ cuộn và đèn dầu đang cháy, không người', dict(fore='bàn thấp', mid='bản đồ và đèn', back='cột gỗ'), 'medium shot', 'ánh sáng bình minh qua cửa, ấm yếu từ đèn dầu',
  ['DEN', 'NHA_DAN'], 'Medium shot of an empty plain timber hall at dawn: a low wooden table with a rolled map with no writing on it and a clay oil lamp burning, nobody in the hall',
  ft=[FT('bản đồ cuộn không chữ', C, 'đạo cụ không có trong Bible')], risk='Low', reuse='sanh-vang', note='Thay cho cảnh mất: không vẽ tang lễ hay mộ (kịch bản không nói, Bible không có).')
MOTION = {
 'L04': 'Đoạn 4: zoom chậm vào bản đồ trên bàn (cắt cận bàn). Đoạn 5: pan nhẹ sang nhân vật khi tên Lý Thường Kiệt được nhắc. Một ảnh, ~19 giây.',
 'L13': 'Đoạn 15: khung rộng, zoom chậm vào nhóm gặt lúa phía trước. Đoạn 16: pan sang nhóm bó lúa phía sau. Một ảnh, ~20 giây.',
 'L08': 'Đoạn 17: khung rộng, zoom chậm vào lưng tướng. Đoạn 18: pan lên dãy núi phía bắc (cắt cận núi). Một ảnh, ~23 giây; dùng lại cho đoạn 9 thì đổi hướng pan.',
 'L10': 'Đoạn 22: khung rộng xưởng thuyền. Đoạn 23: zoom vào hai thân thuyền. Một ảnh, ~19 giây.',
 'L26': 'Ba đoạn ~29 giây. Đoạn 41: khung rộng từ lưng lính Tống. Đoạn 42: zoom chậm vào hàng lũy bờ nam. Đoạn 43: pan xuống mặt nước và lính Tống chuẩn bị lội. Một ảnh, ba lần cắt cận; nếu chủ kênh thấy đơn điệu thì đề xuất dùng L25 (cùng phòng tuyến) cho đoạn 43.',
 'L29': 'Đoạn 46 và 47 (~18 giây): zoom rất chậm vào cửa đền, đèn dầu sáng dần. Một ảnh.',
 'L11': 'Đoạn 50: khung ba phần tư. Đoạn 51: zoom vào bản đồ trên bàn. Một ảnh, ~19 giây.',
 'L32': 'Ba đoạn ~31 giây. Đoạn 54: khung rộng cả đoàn (đếm được năm voi). Đoạn 55: pan dọc theo hàng voi. Đoạn 56: zoom vào sứ giả đi đầu. Một ảnh, ba lần cắt cận. Chỉ thêm ảnh thứ hai (cận cảnh sứ giả) nếu cắt cận từ ảnh gốc bị mờ.',
 'M3': 'Bản đồ động: hai đoạn ~21 giây; hiện địa danh theo từng câu (đoạn 32: câu hỏi; đoạn 33: lập luận), không thêm ảnh.',
 'M5': 'Bản đồ động ~18 giây: đoạn 38 hiện sông, đoạn 39 hiện Thăng Long và hướng tiến; không thêm ảnh.'}
for x in sc:
    if x['scene_id'] in MOTION: x['motion_plan'] = MOTION[x['scene_id']]
CUTS = {'66': [dict(thu_tu=1, scene='L03', cau='Một lần, ông đưa quân vượt biên giới, đánh vào đất địch.', tu_ngu_bat_dau='Một lần', so_chu=len('Một lần, ông đưa quân vượt biên giới, đánh vào đất địch.'.split()), thoi_gian_uoc_tinh='khoảng 0–4 giây của đoạn', ly_do='câu này nói về cuộc tiến quân sang đất Tống: cảnh quân Đại Việt hành quân lên phía bắc'),
               dict(thu_tu=2, scene='L25', cau='Một lần khác, ông dựng phòng tuyến bên sông, bảo vệ từng tấc đất quê hương.', tu_ngu_bat_dau='Một lần khác', so_chu=len('Một lần khác, ông dựng phòng tuyến bên sông, bảo vệ từng tấc đất quê hương.'.split()), thoi_gian_uoc_tinh='khoảng 4–9 giây của đoạn', ly_do='câu này nói về phòng tuyến bên sông: cảnh lũy đất dọc bờ nam')]}
n_ft = 0
for x in sc:
    for f in x.get('free_text_details', []):
        n_ft += 1; f['id'] = f'AC{n_ft:02d}'; f['approval_scope'] = 'visual_only'
# --- kiểm bao phủ 68 đoạn
cov = {}
for s in sc:
    for g in s['segment_ids']: cov.setdefault(g, []).append(s['scene_id'])
miss = [i for i in range(1, 69) if i not in cov]
assert not miss, f'đoạn chưa có cảnh: {miss}'
for x in sc: x['plan_status'] = 'PLAN_OWNER_REVIEW'   # đã qua bộ kiểm, đang chờ chủ kênh duyệt (không tự chuyển PLAN_APPROVED)
json.dump(dict(project='lt1v4', plan_version='2', plan_status='PLAN_OWNER_REVIEW', bible_versions=dict(CUR), script='ke-hoach/thu-giong-hai/lt1v4_full.json', segment_cuts=CUTS, scenes=sc), open(f'{R}/ke-hoach/anh/lt1v4/scene-planner.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(sc), 'cảnh,', sum(1 for s in sc if s.get('render') == 'vector_map'), 'bản đồ;', 'đoạn nhiều cảnh:', {k: v for k, v in cov.items() if len(v) > 1})
