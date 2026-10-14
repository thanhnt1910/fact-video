"""
Tạo kịch bản video dài ST3 (toàn tranh 2D) và danh sách câu mô tả ảnh cho máy vẽ.

  python ke-hoach/nhan-vat/tao_ST3.py
Ra: scripts/ST3.json (kịch bản) và ke-hoach/nhan-vat/ST3_anh.json (mỗi ảnh một câu mô tả đầy đủ).
Mỗi lời kể (beat) = 1 ảnh. Nhân vật luôn dùng ĐÚNG đoạn mô tả cố định trong ST3.json để giữ giống nhau.
Ảnh vẽ xong nằm ở assets/anh_2d/ST3/<số>.jpg; khi có ảnh, beat được gắn trường "anh_file".
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CFG = json.loads((ROOT / "ke-hoach" / "nhan-vat" / "ST3v2.json").read_text(encoding="utf-8"))
NV = CFG["nhan_vat"]
STYLE = CFG["phong_cach"]
SAFE = ("medium to wide shot, simple natural poses, every person has exactly two arms, two hands and two legs with "
        "natural adult proportions, serious weathered adult faces, no extra limbs, no deformed faces, no text, no letters, no watermark. "
        "All ships, boats and objects are realistic with no faces, eyes or smiles. Any people are adult men with beards "
        "in heavy winter clothes, never children, never women")
ONLY = ("only these people appear in the picture and nobody else, no crowd, no extra men, no background figures")
SO_NGUOI = {**{f"{i:03d}": 6 for i in range(70, 76)}}   # hành trình James Caird: đúng 6 người
CLIPS = {"001", "002", "026", "036", "052", "070", "075", "089", "096", "100"}   # ảnh đã có clip chuyển động Veo (giữ nguyên ảnh cũ)
NOT_PERSON = ("ship", "boat", "tug", "dogs", "shelter")

S, W, H, M, C, B, E = "shackleton", "worsley", "hurley", "macklin", "crean", "blackborow", "endurance"
WILD, MCN, PAR, CAIRD, YEL, HUT, DOGS = "wild", "mcnish", "pardo", "caird", "yelcho", "hut", "dogs"


def b(text, nv, canh, label=None):
    return {"text": text, "nv": nv, "canh": canh, "label": label}


MO_DAU = [
    b("Hai mươi tám người đàn ông mắc kẹt giữa biển băng Nam Cực, cách nơi có người ở hàng nghìn cây số.", [],
      "very wide aerial view of a tiny group of men and a few small tents on a vast drifting ice floe in a grey frozen sea, the men look very small"),
    b("Con tàu của họ vừa bị băng nghiền nát. Họ không thể gửi tín hiệu cầu cứu, và không ai trên thế giới biết họ ở đâu.", [E],
      "the ship Endurance trapped and tilting in the ice pack at night, masts leaning, blocks of ice piled against the hull, cold moonlight"),
    b("Hy vọng duy nhất là một chiếc xuồng gỗ nhỏ, và một người đàn ông tên là Ernest Shackleton.", [S],
      "Shackleton standing on the ice facing the horizon at sunrise, a small wooden lifeboat on a sled beside him, golden light over white ice"),
    b("Hai năm sau ngày lên đường, ông quay lại. Và cả hai mươi tám người… đều còn sống.", [S],
      "Shackleton on the deck of a small ship looking toward a distant snowy shore, calm hopeful expression, pale blue sky"),
    b("Đây là chuyến thám hiểm Endurance, một trong những chuyện sinh tồn nổi tiếng nhất lịch sử.", [E],
      "the ship Endurance sailing under full sail across open grey-blue Antarctic water, mountains of ice on the horizon, bright morning"),
]

CHUONG = []

CHUONG.append(("Giấc mơ vượt Nam Cực", [
    b("Năm một nghìn chín trăm mười bốn, nhà thám hiểm Ernest Shackleton mơ một kỳ tích chưa ai làm: đi bộ xuyên lục địa Nam Cực.", [S],
      "Shackleton at a wooden desk in a cosy old London office with a large map of Antarctica pinned behind him, warm lamp light", "Luân Đôn · 1914"),
    b("Cực Nam đã có người tới. Ông muốn đi xa hơn: băng qua cả lục địa, khoảng hai nghìn chín trăm cây số.", [S],
      "close-ish view of a big hand-drawn map of the Antarctic continent with a dotted route crossing it from one sea to the other, no text on the map"),
    b("Con tàu mang tên Endurance, nghĩa là sức chịu đựng, lấy từ khẩu hiệu của gia đình ông: bằng kiên trì, ta chiến thắng.", [E],
      "the wooden ship Endurance moored at a stone harbour wall, flags fluttering, small crowd of onlookers far away on the quay"),
    b("Tháng tám, chiến tranh thế giới bùng nổ. Shackleton xin dâng cả con tàu cho nước Anh. Bộ Hải quân chỉ đáp một chữ: Tiến hành.", [S],
      "Shackleton reading a short telegram in a naval office with a window showing warships in a harbour, serious thoughtful expression"),
    b("Ngày tám tháng tám, Endurance rời cảng Plymouth, hướng về đầu kia của thế giới.", [E],
      "Endurance leaving the English harbour at Plymouth, crowds waving from the shore, seagulls, clear sky", "Plymouth · 8/8/1914"),
    b("Thuyền trưởng là Frank Worsley, người New Zealand, nổi tiếng về tài định hướng trên biển.", [W],
      "Worsley standing at the ship's wooden wheel on the bridge, looking at the horizon, brass compass nearby"),
    b("Tom Crean, thủy thủ người Ireland, đã hai lần đi thám hiểm Nam Cực trước đó.", [C],
      "Crean coiling a thick rope on the ship's deck with a warm smile, sea behind him"),
    b("Frank Hurley, nhiếp ảnh gia người Úc, mang theo máy ảnh và hàng trăm tấm kính để chụp lại mọi thứ.", [H],
      "Hurley standing on the ship's deck beside a wooden camera on a tripod and a box of glass plates, sea wind in his curly hair"),
    b("Bác sĩ Alexander Macklin lo sức khỏe cho cả đoàn trên suốt chuyến đi.", [M],
      "Macklin sitting at a small table in the ship's medical cabin, shelves of bottles behind him, lantern light"),
    b("Cùng đi còn có sáu mươi chín chú chó kéo xe, và cậu thanh niên mười tám tuổi Perce Blackborow, trốn lên tàu ở Buenos Aires.", [B, DOGS],
      "young Blackborow peeking out from behind wooden crates on the deck among a team of husky sled dogs, shy smile"),
    b("Ngày năm tháng mười hai, Endurance rời đảo South Georgia, bến cuối cùng có người. Bốn trăm chín mươi bảy ngày sau họ mới lại thấy đất liền.", [E],
      "Endurance sailing away from a rugged snowy island with a small whaling station on the shore, evening orange light", "South Georgia · 5/12/1914"),
]))

CHUONG.append(("Băng khép lại", [
    b("Hai ngày sau, tàu gặp băng trôi. Năm đó lớp băng dày bất thường, và con tàu phải len từng chút một.", [E],
      "Endurance pushing through a narrow dark channel between large white ice floes, steam from the funnel", "Biển Weddell · 12/1914"),
    b("Suốt sáu tuần, họ lách qua những tảng băng. Chỉ còn khoảng một ngày đi biển là tới đất liền.", [W, E],
      "Worsley at the bow of the ship pointing ahead through a maze of ice floes, low sun, long blue shadows"),
    b("Rồi ngày mười tám tháng giêng năm một nghìn chín trăm mười lăm, băng khép lại. Endurance không thể nhúc nhích.", [E],
      "Endurance completely surrounded by flat white ice stretching in every direction, perfectly still and silent, pale pink sky"),
    b("Shackleton hy vọng băng sẽ vỡ trong vài tuần. Họ chờ. Rồi mùa đông Nam Cực kéo đến.", [S],
      "Shackleton standing alone on the deck at dusk with folded arms, watching the frozen sea, frost on the rigging"),
    b("Từ đầu tháng năm, Mặt Trời biến mất suốt bốn tháng. Chỉ còn bóng tối và tiếng băng rạn nứt.", [E],
      "Endurance frozen in the ice under a deep blue starry polar night, warm lantern light glowing in the cabin windows"),
    b("Để giữ tinh thần, Shackleton bắt mọi người làm việc đều đặn: tập chó, dọn tàu, thay phiên canh gác.", [S, C, DOGS],
      "Crean walking a team of husky dogs on the ice beside the frozen ship while Shackleton watches with a nod, blue twilight"),
    b("Buổi tối, họ hát, chơi nhạc, thậm chí tổ chức đua chó trên băng.", [H, M],
      "cosy ship's common room with men in sweaters sitting around a wooden table laughing, one holding a banjo, warm lamplight"),
    b("Ngày hai mươi hai tháng sáu, giữa mùa đông, họ tổ chức một bữa tiệc với nhạc và những bài phát biểu.", [S, W, C, H],
      "a long wooden table in the ship's mess with a feast, candles, paper decorations, four men laughing and raising cups"),
    b("Hurley chụp ảnh con tàu giữa đêm tối bằng ánh sáng chớp. Nhờ ông, chúng ta còn nhìn thấy những ngày ấy.", [H, E],
      "Hurley beside a camera on a tripod at night on the ice, a bright flash lighting up the frozen ship behind him"),
    b("Nhưng băng không đứng yên. Tháng chín, áp lực băng nâng thân tàu lên rồi đặt nó nghiêng xuống.", [E],
      "Endurance lifted and tilted on its side by pressure ridges of broken ice, masts leaning, dramatic cold light"),
    b("Gỗ kêu răng rắc suốt đêm. Cả đoàn nghe rõ con tàu đang bị bóp nghẹt.", [W, C],
      "Worsley and Crean standing on the tilted deck at night, listening, lantern in hand, cracked planks beneath them"),
    b("Shackleton ra lệnh chuẩn bị xuồng và lương thực, phòng khi phải bỏ tàu.", [S, C],
      "men loading sacks of supplies and sledges next to three lifeboats on the ship's deck at dawn, Shackleton directing"),
]))

CHUONG.append(("Con tàu hấp hối", [
    b("Ngày hai mươi bảy tháng mười, băng ép mạnh đến mức thân tàu vỡ toác, nước tràn vào. Năm giờ chiều, Shackleton ra lệnh bỏ tàu.", [S, E],
      "Shackleton standing on the ice pointing away from the crushed, sinking ship in the background, men leaving, red dusk sky", "Biển Weddell · 27/10/1915"),
    b("Hai mươi tám người rời tàu, mang theo ba xuồng cứu sinh, ít lương thực và đàn chó kéo xe.", [DOGS],
      "a long line of tiny men and dog teams hauling a lifeboat on a sled across a white ice plain, seen from far away"),
    b("Mỗi người chỉ được mang rất ít đồ. Thứ gì không cần để sống sót đều bị bỏ lại trên băng.", [S, B],
      "a small pile of abandoned belongings on the ice, a trunk, books and tools, while Shackleton and Blackborow walk away carrying light packs"),
    b("Hurley có khoảng bốn trăm tấm kính chụp ảnh. Ông chọn giữ lại khoảng một trăm hai mươi tấm.", [H, S],
      "inside a canvas tent by lantern light Hurley sorting a box of glass photographic plates while Shackleton sits beside him"),
    b("Những tấm ảnh ấy, giữ lại hơn một thế kỷ, là lý do ta nhìn thấy hành trình này.", [H],
      "Hurley carrying a wooden box of precious plates close to his chest across the ice, a small sled beside him, soft blue light"),
    b("Họ thử kéo xuồng qua băng về phía đất liền, nhưng sau ba ngày chỉ nhích được vài cây số.", [S, C, W],
      "three men pulling a heavy lifeboat on a sledge over bumpy ice with ropes across their shoulders, grey overcast sky"),
    b("Băng gồ ghề, tuyết mềm đến đầu gối. Họ quay lại và dựng trại trên một tảng băng, đặt tên là Ocean Camp.", [],
      "a small camp of tents and lifeboats on a flat ice floe with a few men moving about, the dark wreck far in the distance", "Ocean Camp · 11/1915"),
    b("Từ trại, họ nhìn con tàu của mình chìm dần. Cột buồm đổ xuống băng.", [E],
      "Endurance half buried in ice with its main mast falling, seen from far across the ice, subdued light"),
    b("Ngày hai mươi mốt tháng mười một, Endurance chìm hẳn. Shackleton nói khẽ: Nó đi rồi, các chàng trai.", [S, W],
      "Shackleton and Worsley standing side by side on the ice in silhouette, watching the ship slip beneath the ice at sunset", "Ocean Camp · 21/11/1915"),
    b("Họ đứng lặng nhìn nhau. Từ giờ, sinh tồn là việc duy nhất phải làm.", [S, C, M],
      "Shackleton, Crean and Macklin standing in silence on the ice staring at the dark hole where the ship vanished, cold light"),
    b("Shackleton có một mục tiêu mới, đơn giản hơn nhiều: đưa cả hai mươi tám người về nhà.", [S],
      "Shackleton alone on a snow ridge looking toward the far horizon with a determined expression, rays of sun through clouds"),
    b("Ông hiểu rằng giữ được tinh thần cả đoàn quan trọng không kém giữ được lương thực.", [S, B],
      "Shackleton sitting beside the young Blackborow by a small campfire, kindly talking, other men resting in the background"),
]))

CHUONG.append(("Năm tháng trên băng trôi", [
    b("Tháng mười hai, họ thử kéo xuồng đi thêm lần nữa, nhưng chỉ nhích được khoảng hai cây số mỗi ngày.", [C, W],
      "Crean and Worsley hauling a sledge with a lifeboat over uneven snow, tiny figures behind them, hazy light", "Biển Weddell · 12/1915"),
    b("Ngày hai mươi chín tháng mười hai, Shackleton cho dừng lại, dựng trại mới và gọi nó là Patience Camp, trại Kiên Nhẫn.", [S],
      "Shackleton standing in front of a new camp of tents with lifeboats turned over, calm decisive pose, pale morning", "Patience Camp · 29/12/1915"),
    b("Tảng băng trôi chầm chậm theo dòng nước, mang cả đoàn đi như một chiếc bè khổng lồ.", [],
      "a large flat ice floe with a small camp of tents drifting on a grey sea, seen from a distance, soft overcast light"),
    b("Họ sống trong lều vải mỏng, ngủ trong túi ngủ lông thú, bên cạnh một cái bếp dầu nhỏ.", [M, B],
      "inside a canvas tent two men lying in fur sleeping bags beside a small glowing stove, warm orange light, frost on the walls"),
    b("Thức ăn là thịt hải cẩu và chim cánh cụt, nấu bằng chính mỡ của chúng.", [C, H],
      "Crean and Hurley beside a smoky fire pot on the ice cooking in a metal pot, penguins waddling in the far distance"),
    b("Tháng ba, lương thực cạn dần. Shackleton đau lòng ra lệnh giết số chó còn lại.", [S, DOGS],
      "Shackleton standing alone looking away toward a grey sunset with a few sled dogs sitting quietly at his side, sad mood"),
    b("Ai trong đoàn cũng buồn. Những chú chó đã gắn bó với họ suốt cả hành trình.", [B, DOGS],
      "young Blackborow sitting on a crate beside a husky dog, resting a hand on its back, soft gentle light"),
    b("Rồi băng bắt đầu nứt. Ngày ba mươi mốt tháng ba, tảng băng tách đôi ngay dưới trại.", [],
      "a dark crack splitting the ice floe between tents on one side and lifeboats on the other, small men running toward the boats"),
    b("Họ chạy ra giành lại ba chiếc xuồng kịp lúc. Mất xuồng, họ sẽ không còn đường sống.", [C, W],
      "Crean and Worsley dragging a lifeboat away from the edge of the cracking ice, urgency, spray of snow"),
    b("Ngày bảy tháng tư, họ thấy một đỉnh núi nhô lên ở chân trời. Đó là đảo Elephant.", [S, H],
      "Shackleton and Hurley standing at the edge of the floe pointing at dark rocky peaks rising on the horizon, hopeful mood", "Biển Weddell · 7/4/1916"),
    b("Nhưng dòng băng đang kéo họ đi qua. Nếu bỏ lỡ hòn đảo ấy, phía trước chỉ còn biển mở mênh mông.", [],
      "the dark rocky island seen far away across open water, a small ice floe with tents drifting past it, tense mood"),
    b("Ngày chín tháng tư, băng vỡ thành những luồng nước đen. Ba chiếc xuồng được hạ xuống biển.", [],
      "three small lifeboats being launched onto a dark channel of water between big ice floes, men climbing aboard, cold dawn"),
]))

CHUONG.append(("Bảy ngày trên biển", [
    b("Ba chiếc xuồng mang tên James Caird, Dudley Docker và Stancomb Wills, chở hai mươi tám người rời tảng băng.", [CAIRD],
      "three small lifeboats packed with bundled men rowing in a line across grey water among icebergs, seen from a distance"),
    b("Họ chèo qua nước lạnh buốt, né những tảng băng lớn hơn cả ngôi nhà.", [W, C],
      "Worsley steering and Crean rowing in an open boat past a huge towering iceberg, tiny in comparison"),
    b("Đêm đến, họ dạt vào một tảng băng để ngủ. Có đêm, băng vỡ ngay dưới chân.", [],
      "small tents and boats on a floe at night under stars, a crack opening in the ice near a tent, calm blue night"),
    b("Sóng đánh liên tục, nước biển đóng băng trên áo quần. Nhiều người khát khô vì không có nước ngọt.", [M, B],
      "Macklin and Blackborow huddled in an open boat with ice on their coats as waves splash, exhausted but together"),
    b("Bác sĩ Macklin đi từ xuồng này sang xuồng khác, lo cho những người yếu nhất.", [M],
      "Macklin kneeling in a boat tending to a weak man wrapped in a blanket, spray around them"),
    b("Sau bảy ngày, họ thấy bờ đảo Elephant. Bốn trăm chín mươi bảy ngày họ chưa đặt chân lên đất liền.", [],
      "three boats approaching a rugged black rocky coast with glaciers behind it, grey dawn, seabirds", "Đảo Elephant · 4/1916"),
    b("Nhiều người kiệt sức đến mức khó đứng vững khi chạm bờ sỏi.", [C, B],
      "Crean helping Blackborow step out of a boat onto a shingle beach, both unsteady and smiling tiredly"),
    b("Nhưng đảo Elephant là bãi đá hoang vắng, bão tuyết quanh năm, không có ai ở.", [],
      "a bleak narrow shingle beach below steep ice cliffs with a few small tents, heavy wind blowing snow"),
    b("Bãi biển hẹp, thủy triều lên là cuốn trôi chỗ cắm trại. Họ phải dời sang một mũi đất khác.", [W, C],
      "Worsley and Crean carrying supplies along a rocky shore past a sandspit while waves wash near the tents", "Cape Wild · 17/4/1916"),
    b("Ở đó, họ dựng chỗ trú bằng hai chiếc xuồng lật úp trên những bức tường đá.", [HUT, M],
      "the shelter made of two upturned lifeboats on stone walls with smoke rising from a chimney, Macklin standing outside"),
    b("Họ nhìn nhau và hiểu: không ai biết họ ở đây, và mùa đông Nam Cực sắp đến lần nữa.", [S, WILD],
      "Shackleton and Wild standing in front of the shelter looking out at a darkening stormy sea, thoughtful"),
    b("Shackleton nhận ra: muốn cả đoàn sống, phải có người đi tìm sự giúp đỡ.", [S],
      "Shackleton looking out to the vast empty sea at sunset with a hard decided expression, gulls in the sky"),
]))

CHUONG.append(("Chuyến đi bằng xuồng gỗ", [
    b("Trạm săn cá voi gần nhất ở đảo South Georgia, cách đó khoảng tám trăm hải lý, hơn một nghìn bốn trăm cây số.", [],
      "a hand-drawn ocean map showing a tiny island and a far distant island with a dotted line of stormy sea between them, no text"),
    b("Phương tiện duy nhất là chiếc James Caird, dài chưa tới bảy mét, vượt vùng biển dữ nhất thế giới.", [CAIRD],
      "the small wooden boat James Caird resting on the shingle beach, tiny against the huge grey sea behind it"),
    b("Thợ mộc Harry McNish gia cố con thuyền bằng ván và vải bạt, dựng thêm mái che.", [MCN, CAIRD],
      "McNish on the beach fixing a canvas deck over the small boat with wooden planks and tools around him"),
    b("Ngày hai mươi bốn tháng tư, Shackleton cùng năm người lên đường: Worsley, Crean, McNish, McCarthy và Vincent.", [S, W, C, MCN],
      "Shackleton, Worsley, Crean and McNish standing beside the loaded small boat ready to launch, wet shingle, cold morning", "Đảo Elephant · 24/4/1916"),
    b("Hai mươi hai người ở lại dưới sự chỉ huy của Frank Wild, đứng nhìn chiếc xuồng nhỏ biến mất trên sóng.", [WILD],
      "Wild and a group of men waving on a rocky beach as a tiny boat sails away toward a stormy horizon, seen from behind"),
    b("Trên biển, sóng cao như những ngọn đồi. Có lần, một con sóng khổng lồ suýt lật cả chiếc xuồng.", [CAIRD],
      "the tiny boat on the crest of an enormous dark green wave about to break, men clinging on, dramatic sky"),
    b("Nước biển đóng băng trên thuyền, nặng thêm từng giờ. Họ phải đập băng liên tục để thuyền không lật.", [C, S],
      "Crean chipping thick ice off the boat's canvas deck with a small axe while Shackleton holds the tiller, spray flying"),
    b("Quần áo ướt sũng không bao giờ khô. Họ ngủ co ro trong túi ngủ ướt, thay phiên nhau canh lái.", [W, MCN],
      "Worsley and McNish curled up under the canvas deck beside a tiny lantern, damp blankets, cramped little space"),
    b("Worsley chỉ ngắm được Mặt Trời vài lần trong cả chuyến đi, trên chiếc thuyền chòng chành.", [W],
      "Worsley kneeling and bracing in the boat holding a brass sextant up toward a break in the clouds, waves around"),
    b("Chỉ cần một sai lệch nhỏ, họ sẽ đi lướt qua đảo và lạc ra Đại Tây Dương mênh mông.", [W],
      "Worsley staring at a small notebook with calculations in the boat, serious worried face, grey sky"),
    b("Ngày tám tháng năm, họ thấy đảo South Georgia. Nhưng một cơn bão dữ đẩy họ ra xa, suýt ném thuyền vào vách đá.", [CAIRD],
      "the small boat tossed by white-capped waves near a dark cliff coast with a jagged island rising behind, storm clouds"),
    b("Ngày mười tháng năm, sau hơn hai tuần trên biển, James Caird cập vào vịnh King Haakon.", [S, W, C],
      "the boat landing in a sheltered cove with tall snowy mountains behind, three men stepping onto the shore, calm clearing sky", "South Georgia · 10/5/1916"),
    b("Họ uống nước ngọt từ một dòng suối, ăn thịt chim con, và lần đầu tiên sau nhiều ngày, được ngủ yên.", [C, W],
      "Crean and Worsley sitting by a small fire in a rocky cave beside the beach, a stream nearby, warm glow"),
    b("Nhưng họ đã đến sai phía. Trạm săn cá voi ở bờ bên kia, và giữa hai bên là những dãy núi chưa ai từng vượt qua.", [S],
      "Shackleton looking up at jagged snow-capped mountain ridges blocking the way inland, tiny figure under huge peaks"),
]))

CHUONG.append(("Ba người vượt núi", [
    b("Ba người còn khỏe nhất quyết định đi bộ: Shackleton, Worsley và Crean. Ba người còn lại ở lại với con thuyền.", [S, W, C],
      "Shackleton, Worsley and Crean standing together at the foot of a snowy slope, packs on their backs, three companions in a row"),
    b("Họ chỉ mang một sợi dây dài khoảng mười lăm mét, một chiếc rìu thợ mộc, một bếp nhỏ và thức ăn cho ba ngày.", [C, W],
      "a close view of a coil of rope, a small axe, a camp stove and a bag of food laid out on a rock, Crean and Worsley beside them"),
    b("Để bám băng, họ vặn những chiếc đinh vít lấy từ chính con thuyền vào đế giày.", [MCN, S],
      "McNish screwing metal screws into the sole of a leather boot with a tool while Shackleton holds the boot, workshop-like cave"),
    b("Họ xuất phát lúc ba giờ sáng dưới ánh trăng, ngày mười chín tháng năm.", [S, W, C],
      "three silhouetted men climbing a moonlit snowfield in a line, long shadows, bright full moon, deep blue sky", "South Georgia · 19/5/1916"),
    b("Có lúc họ leo lên một đỉnh, chỉ để thấy phía bên kia là vách đá, và phải leo ngược xuống.", [S, C],
      "Shackleton and Crean at a ridge top looking down a sheer cliff, heavy fog below, disappointed but resolute"),
    b("Sương mù dày kéo đến, trời tối dần. Họ không dám dừng, vì ngủ quên trên tuyết là chết.", [W, C],
      "Worsley and Crean trudging through deep snow in thick fog at dusk, roped together, tired faces"),
    b("Để đi nhanh, họ ngồi lên cuộn dây và trượt xuống một sườn núi dốc trong bóng tối, không biết bên dưới là gì.", [S, W, C],
      "three men sitting one behind the other on a rope coil sliding down a steep snowy slope in the dark, snow spraying"),
    b("Họ dừng lại an toàn dưới chân dốc, cười phá lên trong tuyết.", [S, C],
      "Shackleton and Crean at the bottom of the slope laughing in the snow, relieved, stars above"),
    b("Sau ba mươi sáu giờ không nghỉ, họ nghe tiếng còi báo giờ làm việc từ trạm săn cá voi Stromness.", [S, W, C],
      "three exhausted men standing on a hill at dawn hearing a faint whistle, a small whaling station with chimneys in the valley below", "Stromness · 20/5/1916"),
    b("Quần áo rách tả tơi, mặt lem khói dầu, râu tóc bù xù. Người trong trạm không nhận ra họ.", [S, W],
      "Shackleton and Worsley at the door of a wooden whaling station building, ragged clothes, sooty faces, a surprised station worker in the doorway"),
    b("Hai mươi hai dặm đường núi, khoảng ba mươi lăm cây số, đi qua vùng đất chưa từng có bản đồ.", [],
      "a wide shot of a mountain range with a thin line of tiny footprints crossing snowy peaks and a glacier, golden morning light"),
]))

CHUONG.append(("Không ai bị bỏ lại", [
    b("Ngay hôm đó, một tàu săn cá voi được cử đi đón ba người còn lại ở bờ bên kia.", [],
      "a small whaling steamer leaving the harbour of Stromness toward the open sea, smoke from the funnel, mountains behind", "Stromness · 20/5/1916"),
    b("Nhưng vẫn còn hai mươi hai người trên đảo Elephant. Shackleton lập tức lên đường cứu họ.", [S],
      "Shackleton on the quay of the whaling station looking at a steamer ready to depart, determined, winter light"),
    b("Lần thứ nhất, tàu Southern Sky bị băng chặn lại, còn cách đảo khoảng một trăm sáu mươi cây số.", [E],
      "a small steamer stopped at the edge of a wall of pack ice with Shackleton at the rail looking out in frustration"),
    b("Lần thứ hai và thứ ba, một tàu từ Uruguay và một tàu buồm thuê ở Chile cũng phải quay về vì băng và bão.", [],
      "a small schooner tossed on rough seas turning around in front of a big stormy sky with ice in the distance"),
    b("Ba lần thất bại, hơn ba tháng trôi qua. Shackleton vẫn không bỏ cuộc.", [S],
      "Shackleton at a window of an office in a southern port city looking out at ships in the harbour, determined, tired"),
    b("Lần thứ tư, ông mượn chiếc tàu nhỏ Yelcho của hải quân Chile, do thuyền trưởng Luis Pardo chỉ huy.", [S, PAR, YEL],
      "Shackleton shaking hands with Captain Pardo on the quay in front of the small grey tug Yelcho, flags above, warm light"),
    b("Ngày ba mươi tháng tám, sương mù tan ra. Yelcho nhìn thấy bờ đảo Elephant.", [YEL],
      "the small steamer Yelcho emerging from fog with the dark island and glaciers ahead, sun breaking through", "Đảo Elephant · 30/8/1916"),
    b("Trên bờ, hai mươi hai người chạy ra vẫy tay. Họ đã sống bốn tháng rưỡi dưới hai chiếc xuồng lật úp, không ai chết.", [WILD, M, B],
      "Wild, Macklin and Blackborow waving on the beach beside the shelter of upturned boats with other men behind them, joyful"),
    b("Theo lời kể lại, Shackleton đếm từng bóng người trên bờ, và thấy đủ cả.", [S, PAR],
      "Shackleton and Captain Pardo at the ship's rail looking toward the beach with a row of figures waving, Shackleton counting"),
    b("Hai mươi tám người của Endurance đều trở về. Không ai bị bỏ lại.", [S, W, C, H],
      "Shackleton, Worsley, Crean and Hurley standing side by side on the Yelcho's deck smiling with relief, sunlit sea behind them"),
    b("Năm hai nghìn không trăm hai mươi hai, các nhà thám hiểm tìm thấy xác Endurance ở độ sâu hơn ba nghìn mét dưới đáy biển Weddell.", [E],
      "the wreck of Endurance resting on a dark sandy seabed lit by a soft glow, a small research submarine drone with lights nearby", "Biển Weddell · 2022"),
    b("Con tàu nằm thẳng đứng, gần như nguyên vẹn, chỉ cách vị trí Worsley ghi lại chừng bốn dặm.", [E],
      "Endurance sitting upright on the seabed with masts and rails intact, fine silt and small sea creatures, quiet mystery"),
    b("Shackleton không vượt được lục địa Nam Cực. Nhưng ông làm được điều quan trọng hơn: đưa mọi người trở về.", [S],
      "Shackleton standing on a hill at golden sunset with his coat blowing, a long line of crew small behind him heading home"),
    b("Sử thật… lạ hơn cả truyện.", [E],
      "Endurance sailing at dawn on a calm glittering sea, a golden path of light, hopeful and warm, cinematic wide shot"),
]))

# ---------------------------------------------------------------- ghép thành kịch bản
beats_all = []
chapters_json = []
mo_dau_beats = []
n = 0


CANH_MOI = {
    "011": "a single man only, Captain Worsley alone at the ship's wooden wheel on the bridge, looking at the horizon, nobody else on deck, one person in the whole picture",
    "059": "Crean, a tall adult sailor, helping the young adult Blackborow (a slim 18-year-old man, clearly a young man not a boy) step out of a rowing boat onto a shingle beach, both tired",
    "065": "a wide empty seascape of dark stormy waves with one tiny rocky island on the left and another tiny rocky island far away on the right, a thin dotted line crossing the water between them, empty sea, absolutely no people, no figures, no ships",
    "071": "inside a small open wooden whaleboat in a rough grey sea, Crean chipping thick ice off the canvas deck with a small axe while Shackleton holds the tiller, spray flying, only the boat and open sea around, no other ships",
    "073": "Worsley alone kneeling in a small open wooden whaleboat holding a brass sextant up toward a break in the clouds, big waves all around, open empty ocean, no other ships, one person only",
    "074": "Worsley alone sitting in a small open wooden whaleboat staring at a small notebook with calculations, serious worried face, grey sky, open empty ocean, no other ships, one person only",
    "101": "underwater view of the wooden ship Endurance sitting upright on a dark seabed with masts and rails intact, fine silt and small fish drifting, quiet mystery, empty seabed, no people, no divers, no figures at all",
}


def add(bt, store):
    global n
    n += 1
    if f"{n:03d}" in CANH_MOI:
        bt = {**bt, "canh": CANH_MOI[f"{n:03d}"]}
    nvs = [x for x in bt["nv"]]
    parts = [bt["canh"]]
    desc = [NV[x] for x in nvs]
    if desc:
        parts.append("Characters (keep exactly this look): " + "; ".join(desc))
        npers = sum(1 for x in nvs if not any(w in NV[x].lower() for w in NOT_PERSON))
        if npers:
            parts.append(f"exactly {npers} named character{'s' if npers > 1 else ''}, each drawn only once, no duplicates or twins, " + ONLY)
    k0 = f"{n:03d}"
    if k0 in SO_NGUOI:
        parts.append(f"exactly {SO_NGUOI[k0]} men in total, no more, no crowd")
    elif not any(not any(w in NV[x].lower() for w in NOT_PERSON) for x in nvs):
        parts.append("no people unless the scene explicitly needs a few small distant figures")
    parts.append(STYLE)
    parts.append(SAFE)
    prompt = ". ".join(parts)
    key = f"{n:03d}"
    beat = {"text": bt["text"], "ai": prompt, "anh_file": f"assets/anh_2d/ST3/{key}.jpg"}
    if bt.get("label"):
        beat["label"] = bt["label"]
    if key in CLIPS:
        beat["clip_file"] = f"assets/clips_2d/ST3/{key}.mp4"
    store.append(beat)
    beats_all.append({"key": key, "prompt": prompt, "nv": nvs})


for bt in MO_DAU:
    add(bt, mo_dau_beats)
chapters_json.append({"beats": mo_dau_beats})
for title, bs in CHUONG:
    store = []
    for bt in bs:
        add(bt, store)
    chapters_json.append({"title": title, "beats": store})

words = sum(len(x["text"].split()) for ch in chapters_json for x in ch["beats"])

script = {
    "id": "ST3",
    "topic": "sinh-ton",
    "title": "28 người mắc kẹt ở Nam Cực và tất cả đều sống sót",
    "caption": "Con tàu bị băng nghiền nát, 28 người mắc kẹt giữa Nam Cực… và không ai bị bỏ lại 🧊",
    "hashtags": ["nguoigacsu", "sinhton", "lichsu", "chuyencothat", "shackleton", "endurance"],
    "sources": [
        "PBS NOVA – Shackleton's Antarctic Adventure: Timeline of the Endurance expedition",
        "Endurance22 – Endurance is found (2022)",
        "Burke Museum – Shackleton's Endurance expedition",
        "Royal Geographical Society – Shackleton Endurance expedition timeline",
    ],
    "nguon_link": [
        {"ten": "PBS NOVA, dòng thời gian chuyến thám hiểm Endurance", "url": "https://www.pbs.org/wgbh/nova/shackletonexped/1914/timeline.html", "ngon_ngu": "tiếng Anh"},
        {"ten": "Endurance22, thông báo tìm thấy xác tàu Endurance (2022)", "url": "https://endurance22.org/endurance-is-found", "ngon_ngu": "tiếng Anh"},
        {"ten": "Bảo tàng Burke, chuyến thám hiểm Endurance của Shackleton", "url": "https://burkemuseum.org/static/endurance/expedition2.html", "ngon_ngu": "tiếng Anh"},
    ],
    "music": "none",
    "pronounce": {"Yelcho": "Yeltcho", "Blackborow": "Blackbarrow", "Stromness": "Stromness"},
    "long": {
        "title": "Vì sao 28 người mắc kẹt ở Nam Cực đều sống sót? | Chuyến thám hiểm Endurance",
        "title_card": "Endurance: **28 người** giữa băng Nam Cực",
        "description": "Năm 1915, con tàu Endurance của Ernest Shackleton bị băng nghiền nát giữa biển Weddell. Hai mươi tám người mắc kẹt trên băng trôi, không điện đài, không ai biết họ ở đâu. Một chiếc xuồng gỗ nhỏ, một cuộc vượt núi chưa từng có bản đồ… và cái kết khiến cả thế giới kinh ngạc.",
        "voice": "Sadaltager",
        "music": "none",
        "chapters": chapters_json,
    },
    "binh_luan": {
        "dai": {
            "ghim": "Theo bạn, quyết định nào của Shackleton khó nhất: bỏ tàu, bỏ lại đàn chó, hay một mình cầm lái chiếc xuồng nhỏ đi tìm cứu viện? Bình luận cho mình biết nhé.",
            "phu": ["Một chi tiết mình chưa kịp kể: để bám băng, họ vặn đinh vít lấy từ chính con thuyền vào đế giày. Đôi khi sống sót là nhờ những thứ nhỏ nhất."],
        }
    },
}

(ROOT / "scripts" / "ST3.json").write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
(ROOT / "ke-hoach" / "nhan-vat" / "ST3_anh.json").write_text(json.dumps(beats_all, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{n} ảnh, {len(chapters_json)} chương (kể cả mở đầu), {words} chữ ≈ {words / 3 / 60:.1f} phút")
