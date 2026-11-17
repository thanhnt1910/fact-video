# Tạo hồ sơ gửi duyệt tm5–tm9 (mục 3.3 quy-tac/thuy-mac.md). Chạy trong /tmp/pc.
import json,subprocess,re
H='Các hook theo khung bốn đoạn ở mục 3.1: (1) câu kể thường, không năm, không tên; (2) lật lại câu 1; (3) tên người, tên nơi, hệ quả nói mạnh; (4) câu hỏi kèm lời hứa N lần.'
M={
'tm5':dict(file='tm5-ham-tu-chuong-duong-tay-ket-1285',ten='Hàm Tử, Chương Dương, Tây Kết 1285',
 kieu='Số phận nhân vật, mở vào lúc nguy nhất của cuộc chiến: Trần Bình Trọng bị bắt khi kinh thành đã mất. Lời hứa: "ba trận trên ba bến sông".',
 bien='Trận phản công đầu tiên (Hàm Tử) bắt đầu ở chương 5, đoạn 19, mốc 47%. Vượt mục tiêu 2 điểm vì chương 3 phải kể đủ lúc nhà Trần xuống thấp nhất: rút khỏi kinh thành, Trần Bình Trọng hy sinh, Trần Ích Tắc và Trần Kiện ra hàng. Cao trào là trận Tây Kết (mốc 68%). Đợt dồn cuối là cảnh Thoát Hoan tháo chạy (mốc 85%).',
 cao=['Bản 2 bị chê vì kể ba trận như liệt kê. Bản 3 sửa theo cách sau: mỗi trận có bốn nhịp, gồm thế nguy trước trận, một chi tiết cụ thể có nguồn, bước ngoặt, và hệ quả đẩy sang trận sau.','Hàm Tử (đoạn 19–22): chi tiết quân Triệu Trung mặc áo Tống. Kết bằng "trận đầu đã thắng, nhưng kinh thành vẫn trong tay Thoát Hoan, Toa Đô vẫn đang trên đường lên".','Chương Dương (đoạn 23–26): mục tiêu lớn hơn là lấy lại kinh thành. Chi tiết Trần Quốc Toản với lá cờ sáu chữ.','Tây Kết (đoạn 27–32) là cao trào và được kể chậm lại: "trận lớn nhất vẫn còn ở phía trước"; đạo quân Toa Đô đánh từ Chiêm Thành ra, thua một trận vẫn còn đông; hai vua tự cầm quân; Toa Đô chết; lời vua than.','Sau cao trào là đợt dồn cuối chứ không phải phần liệt kê: Thoát Hoan còn một mình, chạy qua đúng chỗ Trần Quốc Tuấn chờ, Lý Hằng chết, cảnh ống đồng.','Phần sau cao trào chỉ còn 3 đoạn. Đã bỏ bài thơ của Trần Quang Khải.'],
 hook=['(Đang dùng) Một vị tướng bị bắt, được hứa làm vương, chỉ đáp một câu; lật lại bằng câu "thà làm quỷ nước Nam"; rồi hứa kể ba trận trên ba bến sông.','Mở vào lúc Thoát Hoan chui ống đồng cho lính khiêng chạy; lật lại: nửa năm trước ông đang thắng; hứa kể ba trận đã lật thế cờ.','Mở vào lúc vua Trần Nhân Tông cởi áo mình liệm đầu tướng giặc Toa Đô; lật lại: mấy tháng trước Toa Đô còn kẹp nước ta từ phía nam.'],
 dem='"Bến sông đầu tiên là Hàm Tử" (đoạn 19), "Ở Chương Dương, bến sông thứ hai" (đoạn 25), "Đó là bến sông thứ ba" (đoạn 32).',
 xuyen='Câu "quỷ nước Nam, vương đất Bắc" gieo ở hook, nhắc lại ở đoạn 12, khép ở câu kết.',
 lat='Chương 3: nhà Trần xuống thấp nhất (đoạn 14). Chương 4: hai cánh quân giặc đang tiến lại gần nhau. Chương 6: kinh thành vẫn trong tay giặc. Chương 7: Toa Đô vẫn còn đông.',
 dien=['Đoạn 14: "Đó là lúc nhà Trần xuống thấp nhất" là nhận định của người kể, gom từ các việc có nguồn ở đoạn 10–13.','Đoạn 18: "Vì thế, những trận phản công đều diễn ra trên các bến của sông Hồng". Chữ "vì thế" nối với việc giặc đóng quân dọc sông Hồng (đoạn 17). Câu này không nói nhà Trần đã tính toán như vậy.','Đoạn 32: "Gọng kìm phía nam đã gãy" là hình ảnh của người kể, dựa trên việc Toa Đô chết và quân tan.'],
 chac=['Câu nói của Trần Bình Trọng; nơi bị bắt là bãi Đà Mạc, sông Thiên Mạc: Toàn thư.','Hội nghị Diên Hồng; chữ "Sát Thát": Toàn thư.','Trần Ích Tắc là em trai Thượng hoàng (không viết "em ruột"). Trần Kiện ra hàng: Toàn thư.','Hai vua đi thuyền lánh ra vùng biển Thanh Hóa: Toàn thư.','Quân của Triệu Trung mặc áo Tống ở Hàm Tử: Toàn thư, chỉ một nguồn.','Trần Quang Khải ở Chương Dương, có Trần Quốc Toản và Phạm Ngũ Lão đi cùng: Toàn thư. Lá cờ "phá cường địch, báo hoàng ân" Toàn thư chép ở mục năm 1282. Tuổi của Quốc Toản chỉ suy ra từ năm sinh mà các sách ghi khác nhau, nên lời đọc nói "chưa tới hai mươi tuổi". CẦN chủ kênh duyệt chi tiết này.','Toa Đô đánh ở Chiêm Thành từ năm 1283: sử nhà Nguyên.','Tây Kết tháng Năm, Toa Đô bị chém, Ô Mã Nhi chạy ra biển, lời vua than và việc cởi áo liệm: Toàn thư. CẦN đối chiếu câu chữ.','Ở Vạn Kiếp: Lý Hằng trúng tên độc chết khi che phía sau cho Thoát Hoan; Thoát Hoan chui ống đồng: Toàn thư.','Nóng, mưa, dịch bệnh: Nguyên sử. Lời đọc không nhắc tên nguồn này.'],
 nguon='Hai lần: đoạn 31 ("Theo sử cũ") và đoạn 35 ("theo lời kể trong sử cũ").',
 han='"Truy tặng" đổi thành "phong tước vương cho ông sau khi mất"; "áo ngự" đổi thành "áo mình". "Thượng hoàng" và "Thượng tướng" có giải thích. Sáu chữ trên lá cờ giữ nguyên vì là chữ có thật.',
 canh='"Hook trên 20 chữ": đoạn 1 có 22 chữ, dưới giới hạn 25. Đoạn có 4 tên riêng: tên đã giới thiệu từ trước. "Nhiều hơn 3 dấu phẩy": sẽ nghe lại khi đọc giọng.'),
'tm6':dict(file='tm6-bach-dang-1288',ten='Bạch Đằng 1288',
 kieu='Trận chiến, mở vào khoảnh khắc nguy nhất: hạm đội giặc đuổi theo mấy thuyền nhỏ. Hook không nói ra cọc và thủy triều. Lời hứa: "hai điều".',
 bien='Vân Đồn (mất thuyền lương) bắt đầu ở mốc 30%. Quyết định rút qua Bạch Đằng ở mốc 46%. Trận Bạch Đằng ở mốc 63%. Mất lương là biến cố chính thứ nhất; trận Bạch Đằng là hệ quả của nó nên phải đứng sau.',
 cao=['Kể chậm trước cao trào: thêm đoạn 24 "Thủy triều vẫn đang lên… đoàn chiến thuyền giặc vẫn đuổi theo". Sau đó là "Mọi việc tưởng như vẫn trong tay quân giặc", rồi thủy triều rút xuống.','Bỏ phần đuôi liệt kê sau cao trào: Hốt Tất Liệt định đánh lần nữa, hòm thư bị đốt (2 đoạn). Sau trận chỉ còn 3 đoạn: Thoát Hoan chạy, giải nghĩa câu "đánh giặc nhàn", câu kết.'],
 hook=['(Đang dùng) Hạm đội giặc đuổi mấy thuyền nhỏ; lật lại: thuyền nhỏ đang dẫn đường; Ô Mã Nhi sắp mất hạm đội; hứa "hai điều".','Nghịch lý: vua hỏi tình hình, tướng giỏi nhất đáp "năm nay đánh giặc nhàn" trong khi kinh thành sắp mất lần nữa.','Lời thề của Trần Quốc Tuấn trên sông Hóa trước trận.'],
 dem='"Thuyền lương mất, đó là điều đầu tiên…" (đoạn 13), "Điều thứ hai lộ ra từ đây" (đoạn 19), đoạn 29 gọi lại cả hai.',
 xuyen='Mấy thuyền nhỏ chạy trước hạm đội: gieo ở đoạn 1–2, hiện lại ở đoạn 23, khép ở câu kết. Câu "đánh giặc nhàn": gieo ở đoạn 6, khép ở đoạn 29.',
 lat='Chương 3: Trần Khánh Dư thua trận đầu, "tưởng như đường biển đã mở". Chương 4: kinh thành lại bị bỏ trống. Chương 5: "Mọi việc tưởng như vẫn trong tay quân giặc".',
 dien=['Đoạn 7: "Câu ấy nghe như để vua yên lòng" là cách hiểu của người kể.','Cách gọi "hai điều" là diễn giải của người kể, dựng từ việc có nguồn; không nói đó là nguyên nhân duy nhất.','Đoạn 29: giải nghĩa câu "đánh giặc nhàn" là cách hiểu của người kể; Toàn thư không chép lời giải thích của ông.'],
 chac=['Câu "năm nay đánh giặc nhàn": Toàn thư (năm 1287). CẦN đối chiếu câu chữ.','Ô Mã Nhi đi trước, thuyền lương Trương Văn Hổ đi sau; Trần Khánh Dư thua lúc đầu rồi chặn được thuyền lương ở Vân Đồn: Toàn thư.','Ô Mã Nhi phá Chiêu Lăng: Toàn thư.','Cọc phủ cỏ, đánh nhử, thủy triều rút xuống, ngày mồng tám tháng Ba: Toàn thư. Lời thề trên sông Hóa: Toàn thư.','Bắt Ô Mã Nhi, Phàn Tiếp, Tích Lệ Cơ; hơn bốn trăm thuyền: Toàn thư.','Quân Nguyên không sang đánh Đại Việt lần nào nữa: sự thật lịch sử.'],
 nguon='Một lần, ở đoạn 27 ("Theo sử cũ").',
 han='"Khiêu chiến" đổi thành "ra đánh nhử".',
 canh='"Hook trên 20 chữ": dưới giới hạn 25. Ký tự hai chấm dùng khi dẫn lời nói có thật.'),
'tm7':dict(file='tm7-tot-dong-chuc-dong-1426',ten='Tốt Động, Chúc Động 1426',
 kieu='Trận chiến, mở vào giữa trận: mấy vạn quân chờ một tiếng súng hiệu không nổ. Lời hứa: "hai điều" (do thám, ruộng lầy).',
 bien='Vương Thông kéo quân ra đánh bắt đầu ở mốc 31%. Trận phục kích chính ở mốc 68%. Phần do thám và ám hiệu phải kể trước thì trận phục kích mới có nghĩa.',
 cao=['Kể chậm trước cao trào: thêm đoạn 23 "Đội quân đông đảo ấy dàn dài ra giữa ruộng lầy… chung quanh vẫn không có một tiếng động nào", rồi mới đến lúc phục binh đổ ra.','Bỏ đuôi liệt kê: đoạn khí giới bỏ lại đầy đồng và đoạn Bình Ngô đại cáo. Sau trận còn 4 đoạn: Lê Lợi vây Đông Quan, Vương Thông bị nhốt trong thành, gọi lại hai điều, câu kết.'],
 hook=['(Đang dùng) Mấy vạn quân chờ tiếng súng hiệu; súng không nổ; hai quan lớn nhà Minh trả giá bằng mạng mình; hứa "hai điều".','Nghịch lý: đội quân sang để giữ đất, cuối cùng phải chạy vào thành Đông Quan mà trốn.','Câu hỏi: mấy tên do thám bị bắt đã đổi kết cục của trận đánh nhiều vạn người.'],
 dem='"Đó là lần đầu vùng ruộng lầy giúp nghĩa quân" (đoạn 12), "Mấy tên do thám là điều đầu tiên…" (đoạn 19), "Điều thứ hai là ruộng lầy" (đoạn 20).',
 xuyen='Tiếng súng hiệu: gieo ở hook, nói rõ ở đoạn 18, khép ở câu kết.',
 lat='Chương 3: voi giẫm chông chạy loạn, "tưởng như quân nhà Minh sắp thắng". Chương 4: quân Lam Sơn vẫn ít hơn nhiều lần.',
 dien=['Cách gọi "hai điều" là diễn giải của người kể.','Đoạn 15: "Đánh thẳng mặt thì khó lòng thắng nổi" là nhận định của người kể, dựa vào chênh lệch quân số.','Đoạn 23: hình ảnh đội quân dàn dài, không một tiếng động là lời người kể, dựa vào việc nghĩa quân giữ im lặng và quân Minh đi tắt.'],
 chac=['Diễn biến (Ninh Kiều, cầu Tam La, hàng rào chông, Đinh Lễ và Nguyễn Xí tiếp viện, do thám khai ám hiệu, giữ im lặng, đi tắt vào chỗ phục): Toàn thư Quyển X, mới tra qua bản tóm tắt thứ cấp. CẦN đối chiếu nguyên văn.','Quân số: sử ta ghi tổng mười vạn, sử nhà Minh ghi năm vạn tư. Lời đọc nói "nhiều vạn người".','Thương vong: sử ta và sử nhà Minh ghi khác nhau; lời đọc nêu cả hai ở đoạn 26.','Trần Hiệp, Lý Lượng chết: Bình Ngô đại cáo, Toàn thư.'],
 nguon='Một lần, ở đoạn 26 (so sánh sử ta với sử nhà Minh).',
 han='Không còn từ khó.',
 canh='"Hook trên 20 chữ": dưới giới hạn 25. Đoạn có 4 tên riêng: tên đã giới thiệu.'),
'tm8':dict(file='tm8-chi-lang-xuong-giang-1427',ten='Chi Lăng, Xương Giang 1427',
 kieu='Trận chiến, mở vào khoảnh khắc nguy nhất: mười vạn quân tràn qua cửa ải, đuổi theo một toán quân nhỏ. Lời hứa: "ba lần sụp đổ".',
 bien='Liễu Thăng bắt đầu bị nhử ở mốc 34%. Liễu Thăng chết ở khoảng 45%. Đạt mục tiêu.',
 cao=['Ba lần sụp đổ được kể theo ba kiểu khác nhau để tránh liệt kê: Mã Yên là trận phục kích chớp nhoáng; Xương Giang là vây cho đói dần rồi mới đánh; Mộc Thạnh sụp đổ mà không cần đánh trận lớn, chỉ vì thư và con dấu.','Xương Giang được kể chậm lại: tới nơi mới biết thành đã mất; đóng trại giữa đồng trống; "Nghĩa quân chưa đánh ngay"; đến tháng Mười mới đánh vào.','Bỏ đoạn Bình Ngô đại cáo ở phần đuôi. Sau lần sụp đổ thứ ba còn 3 đoạn.'],
 hook=['(Đang dùng) Mười vạn quân đuổi một toán quân cứ đánh rồi lùi; lật lại: toán quân ấy đang kéo giặc vào thung lũng; Liễu Thăng trả giá bằng mạng mình; hứa "ba lần sụp đổ".','Câu hỏi bí ẩn: năm vạn quân của Mộc Thạnh bỏ chạy vì mấy lá thư và con dấu của một người vừa chết.','Sự kiện bất ngờ: mười lăm vạn quân cứu viện sụp đổ trong chưa đầy một tháng.'],
 dem='"Đó là lần sụp đổ thứ nhất" (đoạn 15), "Xương Giang là lần sụp đổ thứ hai" (đoạn 22), "và đó là lần sụp đổ thứ ba" (đoạn 26).',
 xuyen='Toán quân cứ đánh rồi lùi: gieo ở hook, hiện lại ở đoạn 10, khép ở câu kết.',
 lat='Chương 4: mất chủ tướng mà quân Minh "vẫn còn rất đông, vẫn cố tiến". Chương 5: năm vạn quân Mộc Thạnh "chưa đánh trận lớn nào".',
 dien=['Cách gọi "ba lần sụp đổ" là diễn giải của người kể, dựng từ ba việc có nguồn.','Đoạn 25: việc Mộc Thạnh biết đạo quân kia đã tan được kể theo sử cũ (đoạn 24 có ghi "Theo sử cũ").'],
 chac=['Liễu Thăng mười vạn quân, hai vạn ngựa; Mộc Thạnh năm vạn quân: Toàn thư.','Lê Lợi không cho đánh thành, chờ đánh quân cứu viện, nhắm trước vào Liễu Thăng: Toàn thư. CẦN đối chiếu.','Các mốc ngày Mã Yên, Lương Minh, Lý Khánh: Bình Ngô đại cáo, Toàn thư.','Hơn một trăm kỵ binh vượt lên trước: Toàn thư. CẦN đối chiếu câu chữ.','Thành Xương Giang bị nghĩa quân hạ trước khi viện binh tới; vây rồi đánh vào tháng Mười; bắt Thôi Tụ, Hoàng Phúc: Toàn thư.','Đưa thư từ, con dấu của Liễu Thăng cho Mộc Thạnh xem: theo Việt Nam sử lược. CẦN kiểm với Toàn thư trước khi đọc giọng.','Hội thề Đông Quan, cấp thuyền và ngựa cho quân Minh về nước: Toàn thư.'],
 nguon='Một lần, ở đoạn 24 ("Theo sử cũ").',
 han='"Ấn tín" đổi thành "con dấu"; "giảng hòa" đổi thành "xin thôi đánh để được rút về nước". Bỏ chữ "Thượng thư".',
 canh='Đoạn 5 có 5 tên riêng: cần để người xem mới hiểu bối cảnh.'),
'tm9':dict(file='tm9-rach-gam-xoai-mut-1785',ten='Rạch Gầm, Xoài Mút 1785',
 kieu='Trận chiến, mở vào lúc đoàn thuyền giặc xuôi sông, chưa biết khúc sông phía trước đã được chọn sẵn. Lời hứa: "hai điều".',
 bien='Đặt bẫy bắt đầu ở mốc 41%. Trận đánh ở mốc 59%. Video ngắn; phần lời cầu viện không bỏ được vì đó là "điều thứ nhất".',
 cao=['Kể chậm trước cao trào: thêm đoạn 17 "Trên sông, đoàn thuyền vẫn yên ổn. Hai bờ vẫn im, cù lao vẫn im, chưa một phát súng nào nổ".','Bỏ đoạn Ngọc Hồi, Đống Đa ở phần đuôi. Sau trận còn 3 đoạn.'],
 hook=['(Đang dùng) Mấy trăm chiến thuyền xuôi sông; hai bờ im lặng; quân Xiêm sắp mất gần hết chiến thuyền; hứa "hai điều".','Sự kiện bất ngờ: năm vạn quân sang, vài nghìn người chạy bộ về.','Nghịch lý: người mời quân Xiêm vào lại là một người nước ta.'],
 dem='"Đó là điều thứ nhất" (đoạn 6), "Đó là điều thứ hai" (đoạn 12), "Lời cầu cứu năm trước đã kết thúc như vậy" (đoạn 22).',
 xuyen='Đoàn chiến thuyền xuôi sông Tiền: gieo ở hook, hiện lại ở đoạn 15–17, khép ở câu kết.',
 lat='Chương 2: "Gia Định tưởng như sắp về tay Nguyễn Ánh". Chương 4: "đoàn thuyền vẫn yên ổn".',
 dien=['Đoạn 9: "Gia Định tưởng như sắp về tay Nguyễn Ánh" là nhận định của người kể.','Cách gọi "hai điều" là diễn giải của người kể.'],
 chac=['Quân số Xiêm: sử nhà Nguyễn (Đại Nam thực lục) và các sách sau.','Ngày đánh: sách ghi đêm mười chín rạng sáng hai mươi tháng Một năm 1785. CẦN chủ kênh chọn mốc.','Khúc sông, cù lao Thới Sơn, thuyền giấu trong rạch, súng đại bác hai bờ: các nghiên cứu hiện đại.','Vài nghìn người chạy bộ qua Chân Lạp về nước: các nghiên cứu hiện đại.','Câu "sợ Tây Sơn như sợ cọp": sử nhà Nguyễn. CẦN đối chiếu.'],
 nguon='Hai lần: đoạn 7 và đoạn 23 ("Theo sử nhà Nguyễn").',
 han='"Đại bản doanh" đổi thành "đóng quân chính".',
 canh='Đoạn có 4–5 tên đất miền Tây: cần để hình dung đường tiến quân; bản đồ sẽ hiện tên.'),
}
def run(c,k): return subprocess.run(['python3',f'phim_ban_do/{c}.py',k],capture_output=True,text=True).stdout
for k,m in M.items():
    J=json.load(open(f'ke-hoach/thu-giong-hai/{k}_full.json'));w=sum(len(d['text'].split()) for d in J)
    acc=0;pc={}
    for d in J: pc.setdefault(d['chuong'],acc/w);acc+=len(d['text'].split())
    o=[f'# {k}: {m["ten"]} (gửi duyệt)','',f'{len(J)} đoạn, {w} chữ, khoảng {w/3.1/60:.1f} phút. Giọng đọc dự kiến: Charon, hồ sơ C, đọc từng câu. Chưa đọc giọng.','','## Kịch bản']
    ch=None
    for i,d in enumerate(J):
        if d['chuong']!=ch: ch=d['chuong'];o+=['',f'### Chương {ch} (bắt đầu ở mốc {pc[ch]:.0%})','']
        o.append(f'{i+1}. {d["text"]}')
    o+=['','## Ba phương án hook','',H,'']+[f'{i+1}. {h}' for i,h in enumerate(m['hook'])]
    o+=['','## Thời điểm biến cố chính','',m['bien'],'','## Cao trào: đã sửa lối kể liệt kê thế nào','']+[f'- {x}' for x in m['cao']]
    o+=['','## Ghi chú kỹ thuật kể chuyện','',f'- Kiểu mở đầu: {m["kieu"]}',f'- Câu đếm: {m["dem"]}',f'- Hình ảnh xuyên suốt: {m["xuyen"]}',f'- Chỗ tưởng như giặc sắp thắng: {m["lat"]}',f'- Số lần nhắc nguồn trong lời đọc: {m["nguon"]}',f'- Từ Hán Việt: {m["han"]}','- Câu kết: quay lại hình ảnh mở đầu, cộng lời cảm ơn, không quá 32 chữ.','','**Các đoạn diễn giải của người kể** (đủ năm điều kiện ở `chung.md`)','']+[f'- {x}' for x in m['dien']]
    o+=['','## Ghi chú độ chắc','']+[f'- {x}' for x in m['chac']]
    kq=[]
    for c in ('kiem_kich_ban','kiem_mach_ke','kiem_mo_dau'):
        r=run(c,k);last=[l for l in r.strip().splitlines() if re.search(r'lỗi ❌|->|mở đầu gọn|❌ ',l)][-1:]
        kq.append(f'- `{c}.py`: {last[0].strip() if last else "?"}')
    o+=['','## Kết quả ba bộ kiểm','']+kq+['',f'Cảnh báo được chấp nhận: {m["canh"]}','']
    open(f'ke-hoach/{m["file"]}-gui-duyet.md','w').write('\n'.join(o));print(k,'ok')
