import json,sys
# Trận đánh thủy mặc tập 5: Hàm Tử, Chương Dương, Tây Kết 1285 (mã tm5)
S=[
(1,"Một vị tướng bị bắt giữa trận. Kẻ thù không giết, mà đem chức vương ra dụ ông đầu hàng."),
(1,"Ông đáp lại: ta thà làm quỷ nước Nam, chứ không thèm làm vương đất Bắc. Và ông bị giết ngay sau câu nói ấy."),
(1,"Lúc đó kinh thành đã mất, nhà vua phải lui về phía nam, quân giặc đang thắng ở khắp nơi."),
(1,"Người tướng ấy là Trần Bình Trọng. Kẻ thù trước mặt ông là quân nhà Nguyên, kéo sang từ phương bắc."),
(1,"Tướng giỏi đã chết, người trong họ vua lại có kẻ ra hàng. Vậy chỉ vài tháng sau, nhà Trần lấy đâu ra sức để lật ngược cả cuộc chiến?"),
(2,"Mọi chuyện bắt đầu từ một lời đòi. Năm một nghìn hai trăm tám mươi tư, nhà Nguyên đòi mượn đường qua Đại Việt để đánh nước Chiêm Thành ở phía nam."),
(2,"Cho mượn đường thì chẳng khác gì mở cửa cho giặc vào nhà. Nhà Trần từ chối, và biết chắc chiến tranh sẽ tới."),
(2,"Thượng hoàng Trần Thánh Tông, vua cha đã nhường ngôi cho con, mời các bô lão về điện Diên Hồng, hỏi nên hòa hay nên đánh. Các cụ đều đáp: đánh."),
(2,"Trong quân, binh lính tự thích lên cánh tay hai chữ Sát Thát, nghĩa là giết giặc Mông Cổ."),
(2,"Cuối năm ấy, Thoát Hoan, con trai hoàng đế Hốt Tất Liệt, dẫn đại quân tràn qua biên giới phía bắc. Phía nam, tướng Toa Đô chờ sẵn ở Chiêm Thành."),
(3,"Trần Quốc Tuấn, tức Hưng Đạo Đại Vương, đem quân chặn ở biên giới nhưng không giữ nổi. Ông phải lui về Vạn Kiếp, rồi lui tiếp."),
(3,"Thế là kinh thành Thăng Long lại bị bỏ trống. Đầu năm sau, quân nhà Nguyên vào thành, triều đình thì lui dần về phía nam."),
(3,"Từ phía nam, Toa Đô cũng kéo quân ra đánh Nghệ An, Thanh Hóa. Hai gọng kìm từ hai đầu đất nước đang khép lại."),
(3,"Chính lúc ấy, Trần Bình Trọng cầm quân chặn giặc ở bãi Đà Mạc, bên sông Thiên Mạc. Ông thua trận và bị bắt sống."),
(3,"Tướng giặc dụ ông làm vương đất Bắc. Câu trả lời của ông là câu đã kể ở đầu, và ông chết vì câu trả lời ấy."),
(3,"Cái chết ấy chưa phải tin xấu nhất. Em ruột của Thượng hoàng là Trần Ích Tắc đã dẫn cả nhà sang hàng quân nhà Nguyên."),
(3,"Ở Thanh Hóa, tướng Trần Kiện cũng ra hàng Toa Đô. Nhìn từ phía giặc, nhà Trần lúc ấy như sắp sụp đổ."),
(3,"Vậy tại sao chỉ ít tháng sau, chính quân nhà Nguyên mới là bên phải bỏ chạy?"),
(4,"Thật ra quân nhà Nguyên chiếm được kinh thành, nhưng không bắt được triều đình và không lấy được bao nhiêu lương thực."),
(4,"Rồi mùa hè tới, trời nóng, mưa nhiều, quân lính sinh bệnh. Chính sử nhà Nguyên về sau cũng chép lại nỗi khổ ấy."),
(4,"Trong lúc ấy, Toa Đô từ phía nam kéo lên để hợp quân với Thoát Hoan. Quân hai cánh đóng dọc sông Hồng, ở phía nam kinh thành."),
(4,"Nhưng sông Hồng lại là nơi quân thuyền Đại Việt quen thuộc nhất. Tháng Tư, Trần Nhật Duật đánh vào cửa Hàm Tử trên sông Hồng và thắng trận."),
(4,"Trong quân của Trần Nhật Duật có một toán người nhà Tống sang nương nhờ, do Triệu Trung cầm đầu. Họ ra trận vẫn mặc áo quần kiểu Tống."),
(4,"Vì thế, quân giặc trông thấy thì hoảng, tưởng nhà Tống sang đánh giúp Đại Việt, nên vỡ chạy."),
(4,"Gần như cùng lúc, Thượng tướng Trần Quang Khải đánh tan giặc ở bến Chương Dương. Thắng xong, ông dẫn quân tiến thẳng về Thăng Long."),
(4,"Quân nhà Nguyên giữ kinh thành không nổi, phải bỏ thành rút qua sông. Kinh thành vì thế lại về tay nhà Trần."),
(5,"Lúc ấy Toa Đô vẫn còn đóng quân ở vùng Tây Kết, bên sông Hồng, phía nam kinh thành."),
(5,"Tháng Năm, hai vua Trần đem quân tới đánh. Quân giặc tan vỡ ở Tây Kết, và chính Toa Đô bị chém đầu ngay trong trận."),
(5,"Đầu Toa Đô được đem về dâng vua. Theo sử cũ, vua Trần Nhân Tông nhìn rồi than: làm bề tôi nên như người này, rồi cởi áo ngự sai đem liệm."),
(6,"Mất Toa Đô, Thoát Hoan chỉ còn cách rút về phương bắc. Nhưng đường về lại đi ngang Vạn Kiếp, nơi Trần Quốc Tuấn đang chờ."),
(6,"Quả nhiên, ở đó quân nhà Nguyên bị đánh tơi tả. Tướng Lý Hằng trúng tên độc mà chết, tướng Lý Quán cũng chết trên đường chạy."),
(6,"Còn Thoát Hoan, con trai hoàng đế nhà Nguyên, theo lời kể trong sử cũ, phải chui vào một cái ống đồng cho quân lính khiêng chạy về nước."),
(6,"Tháng Sáu, hai vua trở về kinh thành Thăng Long. Từ lúc giặc tràn sang đến khi chúng rút hết, chỉ khoảng nửa năm."),
(6,"Trên đường về, Trần Quang Khải làm một bài thơ ngắn, nhắc chuyện cướp giáo giặc ở Chương Dương và bắt quân thù ở Hàm Tử."),
(6,"Trần Bình Trọng thì đã chết từ đầu cuộc chiến. Vì thế, vua thương xót mà truy tặng ông tước vương."),
(6,"Mất kinh thành, mất tướng giỏi, có cả người ra hàng giặc, nhà Trần vẫn đứng dậy đánh đuổi quân Nguyên. Cảm ơn bạn đã lắng nghe câu chuyện này."),
]
json.dump([{'n':180001+i,'chuong':c,'tone':'story','text':t,'hien':t} for i,(c,t) in enumerate(S)],open('/tmp/pc/ke-hoach/thu-giong-hai/tm5_full.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
tot=sum(len(t.split()) for c,t in S);acc=0;seen=set()
print(len(S),'đoạn',tot,'chữ ~',round(tot/3.1/60,1),'phút')
for i,(c,t) in enumerate(S):
    if c not in seen: seen.add(c);print('chương',c,'đoạn',i+1,f'{acc/tot:.0%}')
    acc+=len(t.split())
