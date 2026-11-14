"""Lời đọc Tập 1 «Quốc Tử Giám Thăng Long» (series Lịch sử đại học Việt Nam).
Mỗi đoạn 15–32 tiếng, tối đa 2 câu, năm và số viết bằng chữ, không ngoặc, ngoặc kép, gạch, hai chấm, chữ số.
Chạy: python3 loi_doc.py  ->  loi_doc.json  [{n, canh, text}]
Nguồn từng ý: xem kịch bản «Kịch bản Phần 1 – Tập 1: Quốc Tử Giám Thăng Long» (mục Kiểm chứng và nguồn)."""
import json, os, re

C = []          # (cảnh, lời)
def S(canh, *lines):
    for t in lines: C.append((canh, t))

# ===== 1. MỞ ĐẦU =====
S('mo_dem',
  'Giữa lòng Hà Nội hôm nay có một ngôi trường đã chín trăm năm mươi tuổi.',
  'Đó là trường đại học đầu tiên của người Việt.')
S('mo_canh',
  'Nơi đây từng dạy các hoàng tử, rồi mở cửa cho con nhà thường dân học giỏi.',
  'Nơi đây còn lưu tên hơn một nghìn ba trăm vị tiến sĩ, khắc trên những tấm bia đá.')
S('mo_hoi',
  'Vậy trường đại học đầu tiên ấy đã ra đời như thế nào, và vì sao nó tồn tại gần một nghìn năm?')
S('mo_tieu_de', 'Lịch sử đại học Việt Nam. Tập một. Quốc Tử Giám Thăng Long.')

# ===== 2. BỐI CẢNH =====
S('bc_ban_do',
  'Năm một nghìn không trăm mười, nhà Lý dời đô về Thăng Long, bên bờ sông Hồng.',
  'Một vương triều mới, một kinh thành mới, và một câu hỏi cũ.',
  'Lấy đâu ra người có học để giúp vua trị nước?')
S('bc_truoc_ly',
  'Trong gần một thế kỷ trước đó, các triều Ngô, Đinh, Tiền Lê phải lo chống giặc ngoại xâm.',
  'Việc võ được coi trọng hơn việc văn, và nhà nước chưa có trường học riêng.')
S('bc_chua',
  'Trước đó, người Việt học chữ chủ yếu ở nhà chùa và ở các trường tư trong dân gian.',
  'Các nhà sư vừa tu hành, vừa dạy chữ, vừa là người giúp việc cho triều đình.')
S('bc_lang',
  'Ở làng quê, vài ông đồ mở lớp nhỏ ngay trong nhà mình.',
  'Học trò ngồi trên chiếu, chép chữ Hán, đọc sách thánh hiền.')
S('bc_trieu',
  'Nhưng một quốc gia muốn vững mạnh cần nhiều quan lại hiểu kinh sử, hiểu luật lệ.',
  'Họ còn phải viết được văn thư để giao thiệp với các nước láng giềng.',
  'Thuở ấy, triều đình chọn người chủ yếu bằng cách để quan lại tiến cử người tài.',
  'Ai tiến cử sai người thì phải chịu tội nặng trước triều đình.',
  'Nhà Lý bắt đầu xây một con đường mới.',
  'Dựng miếu thờ bậc thầy, mở khoa thi chọn người tài, và lập trường học của nhà nước.')

# ===== 3. HÌNH THÀNH =====
S('ht_van_mieu',
  'Năm một nghìn không trăm bảy mươi, vua Lý Thánh Tông cho dựng Văn Miếu ở phía nam kinh thành.',
  'Trong miếu tạc tượng Chu Công, Khổng Tử cùng các bậc tiên nho, tiên hiền.',
  'Hai dãy nhà hai bên thờ bảy mươi hai học trò giỏi nhất của Khổng Tử.',
  'Đây chưa phải là trường học, mà là một lời tuyên bố.',
  'Triều đình tôn trọng chữ nghĩa và đạo làm thầy.')
S('ht_khoa_thi',
  'Năm một nghìn không trăm bảy mươi lăm, vua Lý Nhân Tông mở khoa thi Nho học đầu tiên.',
  'Khoa thi ấy gọi là Minh kinh bác học, nghĩa là chọn người hiểu sáng kinh sách và học rộng.',
  'Người đỗ đầu là Lê Văn Thịnh, một người con của vùng Kinh Bắc.',
  'Từ đây bắt đầu nền khoa cử kéo dài gần tám trăm năm mươi năm.')
S('ht_qtg',
  'Một năm sau, năm một nghìn không trăm bảy mươi sáu, Quốc Tử Giám được lập ngay phía sau Văn Miếu.',
  'Lúc đầu, đây là nơi học của các hoàng tử, con cái nhà vua.',
  'Về sau, trường mở cửa cho cả những học trò giỏi trong nước.')
S('ht_toan_canh',
  'Văn Miếu thờ bậc thầy, Quốc Tử Giám dạy người học.',
  'Hai công trình đứng cạnh nhau, và trường đại học đầu tiên của người Việt đã ra đời.',
  'Ngày nay, khu di tích rộng hơn năm mươi tư nghìn mét vuông, chia thành năm lớp sân nối tiếp nhau.',
  'Từ cổng vào là khu Nhập đạo, rồi Thành đạt, vườn bia tiến sĩ, khu Đại Thành, và cuối cùng là khu Thái Học.')
S('ht_1086',
  'Năm một nghìn không trăm tám mươi sáu, nhà Lý mở thêm khoa thi chọn người giỏi văn học.',
  'Người đỗ đầu là Mạc Hiển Tích, sau làm đến chức thượng thư, tức là đứng đầu một bộ trong triều.')

# ===== 4. ĐỜI SỐNG HỌC TẬP =====
S('hs_buoi_hoc',
  'Một buổi sáng ở Quốc Tử Giám bắt đầu từ rất sớm.',
  'Giám sinh, tức là học trò của trường, xếp hàng vào giảng đường.',
  'Thầy ngồi trên bục cao, học trò ngồi chiếu, sách mở trước mặt.')
S('hs_hoc_gi',
  'Việc học dựa trên kinh điển Nho giáo, gồm Tứ thư, Ngũ kinh, sử sách và lễ nghĩa.',
  'Nhưng mục đích không chỉ là thuộc sách.',
  'Người học phải có cả học vấn lẫn phẩm hạnh, để sau này giúp nước, giúp dân.')
S('hs_tran',
  'Đến đời nhà Trần, năm một nghìn hai trăm năm mươi ba, trường được đổi tên thành Quốc học viện.',
  'Vua Trần Thái Tông xuống chiếu cho nho sĩ trong cả nước đến đây học Tứ thư, Ngũ kinh.',
  'Con em thường dân học giỏi cũng được vào học.',
  'Ngôi trường của hoàng tộc dần trở thành ngôi trường của cả nước.')
S('hs_tam_khoi',
  'Năm một nghìn hai trăm bốn mươi bảy, triều Trần lần đầu đặt ba bậc đỗ cao nhất.',
  'Đó là trạng nguyên, bảng nhãn và thám hoa.')
S('hs_kinh_trai',
  'Năm một nghìn hai trăm năm mươi sáu, vua Trần Thái Tông còn lấy hai trạng nguyên cùng một khoa.',
  'Một người cho kinh đô và miền bắc, gọi là kinh trạng nguyên.',
  'Một người cho vùng từ Thanh Hóa trở vào, gọi là trại trạng nguyên, để khuyến khích việc học ở nơi xa.')
S('hs_thi',
  'Muốn đỗ đại khoa, sĩ tử phải qua ba kỳ thi.',
  'Thi Hương ở các vùng, thi Hội ở kinh đô, và thi Đình ngay trước sân điện nhà vua.')
S('hs_truong_thi',
  'Ở trường thi Hương, hàng nghìn sĩ tử mang theo lều, chõng và nghiên bút.',
  'Mỗi người tự dựng một chiếc lều nhỏ, ngồi làm bài từ sáng đến tối.')
S('hs_so_lieu',
  'Từ khoa thi đầu tiên năm một nghìn không trăm bảy mươi lăm đến khoa cuối cùng năm một nghìn chín trăm mười chín.',
  'Các triều đại đã mở một trăm tám mươi ba khoa thi, lấy đỗ hai nghìn tám trăm chín mươi tám tiến sĩ.',
  'Trung bình mỗi năm chưa đến bốn người.')
S('hs_vinh_quy',
  'Người đỗ đạt được vua ban áo mũ, rồi về quê trong nghi lễ vinh quy bái tổ.',
  'Cả làng ra đón, cờ lọng rợp đường, để mừng người con mang vinh dự về cho quê hương.')
S('hs_khac_bia',
  'Năm một nghìn bốn trăm tám mươi tư, vua Lê Thánh Tông cho khắc tên người đỗ tiến sĩ lên bia đá.',
  'Việc khắc bia bắt đầu từ khoa thi năm một nghìn bốn trăm bốn mươi hai.')
S('hs_nguyen_khi',
  'Trên tấm bia đầu tiên có một câu được nhắc đến nhiều nhất trong lịch sử giáo dục Việt Nam.',
  'Hiền tài là nguyên khí quốc gia.',
  'Nguyên khí vững thì thế nước mạnh, nguyên khí kém thì thế nước yếu.')
S('hs_vuon_bia',
  'Những tấm bia đều dẹt, trán cong hình vòm, đặt trên lưng những con rùa đá to, chắc khỏe.',
  'Ngày nay còn lại tám mươi hai bia, ghi danh một nghìn ba trăm linh bảy vị tiến sĩ qua tám mươi hai khoa thi.')

# ===== 5. NHÂN VẬT =====
S('nv_le_van_thinh',
  'Người đỗ đầu khoa thi đầu tiên, Lê Văn Thịnh, xuất thân từ một gia đình nông dân.',
  'Ông nổi tiếng chăm học, thường đọc sách đến khuya bên ngọn đèn dầu.',
  'Sau khi đỗ, Lê Văn Thịnh trở thành thầy dạy của vua Lý Nhân Tông, rồi làm đến chức thái sư.',
  'Người đời sau gọi ông là trạng nguyên khai khoa, dù khi ấy triều đình chưa đặt ra danh hiệu trạng nguyên.')
S('nv_chu_van_an_truong',
  'Thời Trần, có một người thầy được hậu thế kính trọng bậc nhất, đó là Chu Văn An.',
  'Chu Văn An mở trường dạy học ở quê, học trò kéo đến hàng nghìn người.',
  'Nhiều học trò của ông đỗ cao, làm quan to, mà gặp thầy vẫn giữ lễ học trò.',
  'Ông viết sách Tứ thư thuyết ước, giảng giải bốn bộ sách gốc của Nho học.')
S('nv_chu_van_an_qtg',
  'Vua Trần Minh Tông mời Chu Văn An về làm tư nghiệp Quốc Tử Giám, tức là người đứng đầu nhà trường.',
  'Ông dạy cả thái tử, người sau này lên ngôi vua.')
S('nv_that_tram',
  'Đến đời vua Trần Dụ Tông, gian thần lộng hành, triều chính rối ren.',
  'Chu Văn An dâng Thất trảm sớ, tức là tờ sớ xin chém bảy kẻ nịnh thần.',
  'Nhà vua không nghe.')
S('nv_ve_nui',
  'Chu Văn An trả lại mũ áo, về núi Phượng Hoàng ở Chí Linh, dạy học và viết sách đến cuối đời.',
  'Khi ông mất, năm một nghìn ba trăm bảy mươi, triều đình cho thờ ông ở Văn Miếu, bên cạnh Khổng Tử.',
  'Nhà sử học Phan Huy Chú về sau khen ông có học vấn thuần khiết, khí tiết cao thượng.',
  'Theo lời Phan Huy Chú, trong giới nhà nho nước Việt, trước sau không ai sánh được Chu Văn An.')
S('nv_ten_bia',
  'Trên những tấm bia đá, ta còn đọc được tên Ngô Sĩ Liên, người viết bộ sử lớn của nước nhà.',
  'Có Lương Thế Vinh, người giỏi toán. Có Lê Quý Đôn, nhà bác học. Có Ngô Thì Nhậm, nhà văn và nhà chính trị.',
  'Mỗi tấm bia là một khoa thi. Mỗi cái tên là một đời người đi qua cánh cửa của ngôi trường này.')

# ===== 6. BIẾN CỐ VÀ ĐỔI THAY =====
S('bd_le_trung_hung',
  'Thời Lê trung hưng, năm một nghìn bảy trăm sáu mươi hai, Quốc Tử Giám được sửa sang lại.',
  'Năm một nghìn bảy trăm tám mươi lăm, trường đổi tên thành nhà Thái Học.',
  'Ngôi trường còn giữ một chiếc chuông lớn gọi là chuông Bích Ung, đúc năm một nghìn bảy trăm sáu mươi tám.')
S('bd_doi_do',
  'Năm một nghìn tám trăm linh hai, nhà Nguyễn đóng đô ở Phú Xuân, tức là Huế ngày nay.',
  'Một Quốc Tử Giám mới được lập ở kinh đô Huế.')
S('bd_hoai_duc',
  'Còn ở Thăng Long, ngôi trường cũ không còn là trường của cả nước.',
  'Năm một nghìn tám trăm linh năm, nơi đây trở thành học đường của phủ Hoài Đức.')
S('bd_khue_van',
  'Cũng năm ấy, Tổng trấn Bắc thành Nguyễn Văn Thành cho dựng Khuê Văn Các.',
  'Đó là một gác vuông tám mái, bốn mặt có cửa tròn như những vầng sáng.',
  'Ngôi gác ra đời khi trường đã lặng lẽ, nhưng nay lại là biểu tượng của cả Hà Nội.')
S('bd_gieng',
  'Trước Khuê Văn Các là giếng Thiên Quang hình vuông, tượng trưng cho đất.',
  'Bóng gác in xuống mặt giếng, như trời và đất soi vào nhau.')
S('bd_khoa_cuoi',
  'Năm một nghìn chín trăm mười chín, khoa thi Hội cuối cùng được tổ chức ở Huế.',
  'Nền khoa cử kéo dài hơn tám trăm bốn mươi năm chính thức khép lại.')
S('bd_chien_tranh',
  'Qua những năm tháng chiến tranh, nhiều công trình phía sau bị phá hủy, chỉ còn nền cũ.')
S('bd_trung_tu',
  'Năm một nghìn chín trăm linh sáu, người Pháp xếp hạng nơi đây là di tích.',
  'Năm một nghìn chín trăm sáu mươi hai, Văn Miếu Quốc Tử Giám được công nhận là di tích quốc gia.',
  'Năm một nghìn chín trăm chín mươi tư, những nhà che bia được dựng lại để bảo vệ bia khỏi mưa nắng.',
  'Cuối thế kỷ hai mươi, nhà Thái Học được xây lại trên nền Quốc Tử Giám xưa.')

# ===== 7. NGÀY NAY VÀ KẾT =====
S('kt_unesco',
  'Năm hai nghìn không trăm mười, tám mươi hai bia tiến sĩ được UNESCO công nhận là Di sản tư liệu thế giới.',
  'Ngày nay, Văn Miếu Quốc Tử Giám là di tích quốc gia đặc biệt.')
S('kt_ho_van',
  'Phía trước Văn Miếu là hồ Văn, xưa gọi là Thái Hồ, giữa hồ có gò Kim Châu.',
  'Trên gò có một ngôi lầu nhỏ để ngắm cảnh, bóng lầu in xuống mặt nước.')
S('kt_ngay_nay',
  'Sân nhà Thái Học vẫn đón các bạn nhỏ đến học về khoa cử và truyền thống hiếu học.',
  'Giống như ông cha họ đã đến đây, từ gần một nghìn năm trước.')
S('kt_cau_ket',
  'Ngôi trường đầu tiên không còn tiếng giảng bài.',
  'Nhưng ý nghĩ đã làm nên nó vẫn còn đó.',
  'Một đất nước muốn mạnh thì phải biết nuôi dưỡng người tài.')
S('kt_tap_sau',
  'Tập sau, một sĩ tử phải vượt qua những gì để được khắc tên lên đá?')

segs = [{'n': i + 1, 'canh': c, 'text': t} for i, (c, t) in enumerate(C)]
def tieng(t): return len(re.findall(r"[\wÀ-ỹ]+", t))
bad = [s for s in segs if re.search(r'[0-9()"“”:;\[\]]|\s-\s', s['text']) or tieng(s['text']) > 34]
if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loi_doc.json')
    json.dump(segs, open(out, 'w'), ensure_ascii=False, indent=1)
    tot = sum(tieng(s['text']) for s in segs)
    print(len(segs), 'đoạn,', tot, 'tiếng, ước tính', round(tot / 3 / 60, 1), 'phút; dài nhất', max(tieng(s['text']) for s in segs))
    for s in bad: print('LỖI', s['n'], tieng(s['text']), s['text'])
