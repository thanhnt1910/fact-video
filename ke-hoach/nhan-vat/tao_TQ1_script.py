"""Tạo scripts/TQ1.json (video dài 8-10 phút + video ngắn) từ danh sách lời kể và ảnh assets/anh_2d/TQ1/NNN.jpg."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CH = [
 ("Mở đầu", [
  ("Hơn một nghìn tám trăm năm trước, khắp Trung Hoa vang lên một câu khẩu hiệu: Trời xanh đã chết, trời vàng sẽ lên.", "001"),
  ("Chỉ ít lâu sau, hàng chục vạn người quấn khăn vàng nổi dậy, và nhà Hán bắt đầu sụp đổ.", "002"),
  ("Giữa cơn loạn ấy, ở một huyện nhỏ, có một người đàn ông nghèo bán giày cỏ, dệt chiếu để sống.", "003"),
  ("Ông chưa có binh, chưa có tiền, chưa có chức. Vậy mà người ta nhớ tên ông suốt cả nghìn năm: Lưu Bị.", "004"),
  ("Đây là Tam Quốc theo chính sử. Không có phép thuật, không có lời thề vườn đào. Chỉ có những con người thật.", "005"),
  ("Câu chuyện này dựa vào bộ Tam quốc chí do Trần Thọ biên soạn, cùng phần chú giải của Bùi Tùng Chi.", "042"),
  ("Còn bộ tiểu thuyết quen thuộc của La Quán Trung chỉ được viết ra hơn một nghìn năm sau. Nhiều cảnh nổi tiếng trong đó không có trong sử.", "020"),
  ("Câu hỏi của tập này rất đơn giản: một người không binh, không tiền, đã bắt đầu từ đâu?", "005"),
 ]),
 ("Nhà Hán trước ngày loạn", [
  ("Năm một trăm tám mươi bốn, nhà Hán đã tồn tại gần bốn trăm năm, và mục ruỗng từ bên trong.", "006"),
  ("Nhà Hán do Lưu Bang lập ra. Sau một thời gian bị Vương Mãng cướp ngôi, một người họ Lưu khác dựng lại triều đại, và sử gọi đó là Đông Hán.", "006"),
  ("Hoàng đế Linh đế bán cả chức quan để lấy tiền, hoạn quan nắm quyền trong triều.", "007"),
  ("Đó là một triều đình mà người có tài chưa chắc được dùng, còn người có tiền thì mua được chức.", "007"),
  ("Người bỏ tiền mua chức sẽ phải tìm cách lấy lại vốn. Và người phải trả giá cuối cùng thường là dân thường.", "014"),
  ("Nhiều năm liền thiên tai và dịch bệnh kéo đến, nông dân đói khổ, mất ruộng, mất cả nhà cửa.", "008"),
  ("Người đứng lên thu phục lòng dân là một đạo sĩ tên Trương Giác, ở Cự Lộc.", "009"),
  ("Ông lập Thái Bình đạo, chữa bệnh bằng bùa nước và sám hối, có hàng chục vạn tín đồ khắp tám châu.", "010"),
  ("Với nhiều người nghèo, không có thầy thuốc, đó có thể là hy vọng duy nhất họ còn.", "010"),
  ("Ông chia tín đồ thành ba mươi sáu phương, như ba mươi sáu đạo quân.", "011"),
  ("Phương lớn có hơn một vạn người, phương nhỏ chừng sáu bảy nghìn. Mỗi phương có một người đứng đầu.", "037"),
  ("Họ hẹn nhau khởi sự năm Giáp Tý, tức năm một trăm tám mươi bốn, và quấn khăn vàng trên đầu.", "012"),
  ("Khẩu hiệu của họ nói rõ: năm Giáp Tý, thiên hạ đại cát. Họ tin rằng trời đất sắp đổi chủ.", "011"),
  ("Nhưng kế hoạch bị lộ. Một người trong đạo là Đường Chu đã đi tố giác, nên Trương Giác phải khởi sự sớm hơn dự định.", "013"),
  ("Triều đình hoảng loạn, ra lệnh cho các châu quận dấy nghĩa binh.", "014"),
  ("Lửa loạn lan nhanh khắp tám châu, và nhiều quan địa phương hoảng sợ bỏ trốn.", "002"),
 ]),
 ("Người bán giày cỏ", [
  ("Ở huyện Trác, quận Trác, lúc ấy có một thanh niên tên là Lưu Bị.", "015"),
  ("Ông tự nhận là con cháu Trung Sơn Tĩnh vương Lưu Thắng, con của vua Cảnh đế nhà Hán.", "016"),
  ("Họ Lưu là họ của hoàng đế. Nhưng qua nhiều đời, dòng dõi ấy đã xa, và không còn mang lại cho ông đặc quyền nào.", "016"),
  ("Cha ông mất sớm, hai mẹ con sống bằng nghề bán giày, dệt chiếu.", "017"),
  ("Người mẹ ấy là chỗ dựa của ông qua những năm nghèo khó.", "017"),
  ("Sử chép ông cao bảy thước năm tấc, khoảng một mét bảy mươi ba, tay dài quá gối, quay đầu có thể thấy tai mình.", "004"),
  ("Tay dài quá gối là một chi tiết lạ. Người đời sau thường coi đó là dấu hiệu của một người khác thường.", "018"),
  ("Ông ít nói, giỏi hạ mình, vui buồn không để lộ ra mặt.", "019"),
  ("Ông không thích đọc sách. Ông thích chó ngựa, âm nhạc, và áo quần đẹp.", "020"),
  ("Năm mười lăm tuổi, ông đi học với Lư Thực, cùng một người bạn học là Công Tôn Toản.", "042"),
  ("Người thầy ấy, Lư Thực, sau này chính là một trong những tướng được triều đình giao đánh Hoàng Cân.", "038"),
  ("Điều ông giỏi nhất là kết bạn: ông thích giao du với hào kiệt, và nhiều người trẻ muốn đi theo ông.", "021"),
  ("Hồi nhỏ, nhà ông có một cây dâu rất lớn, từ xa nhìn như chiếc lọng xe.", "022"),
  ("Ông từng chỉ cây dâu mà nói: sau này ta sẽ ngồi xe có lọng như thế. Người chú nghe thấy, quát: đừng nói bậy, cả họ ta sẽ bị giết.", "023"),
  ("Một đứa trẻ nghèo nói câu ấy giữa thời nhà Hán còn nguyên vẹn là một lời đại nghịch. Nhưng ông vẫn nhớ nó.", "024"),
  ("Câu nói ấy được Tam quốc chí chép lại, và cho thấy ông mang tham vọng từ rất sớm.", "024"),
 ]),
 ("Hai người đi cùng", [
  ("Khi loạn Hoàng Cân nổ ra, Lưu Bị bắt đầu tập hợp người ở quê nhà.", "025"),
  ("Hai người đàn ông theo ông ngay từ những ngày ấy: Quan Vũ và Trương Phi.", "026"),
  ("Ba người đến từ ba hoàn cảnh khác nhau: một người nghèo mà có chí, một người chạy loạn từ xa tới, một người sinh ra ở quê nhà.", "026"),
  ("Quan Vũ vốn người Hà Đông, chạy tới quận Trác lánh nạn. Trương Phi là người quận Trác.", "027"),
  ("Sử chỉ ghi rất ngắn: hai người làm hộ vệ cho Lưu Bị.", "028"),
  ("Lưu Bị đối xử với họ ngủ chung giường, ân nghĩa như anh em.", "029"),
  ("Trong thời loạn, chung một chiếc giường nghĩa là tin nhau đến mức dám nhắm mắt ngủ trước mặt nhau.", "029"),
  ("Quan Vũ lớn hơn Trương Phi vài tuổi, nên Trương Phi coi Quan Vũ như anh.", "030"),
  ("Không có tế trời đất, không có lời thề sinh tử. Trong Tam quốc chí không có một chữ nào về vườn đào.", "031"),
  ("Tình nghĩa ấy không đến từ một buổi lễ. Nó đến từ nhiều năm dài đi bên nhau.", "032"),
  ("Nhưng ba người còn thiếu một thứ: tiền để nuôi quân.", "033"),
  ("Sử chép hai thương nhân buôn ngựa giàu có, Trương Thế Bình và Tô Song, đã cho Lưu Bị nhiều tiền, vì thấy ông khác thường.", "034"),
  ("Hai thương nhân ấy không phải quan lại. Họ nhìn người bằng con mắt của người làm ăn: ai đáng để đặt cược.", "034"),
  ("Lưu Bị không có binh lực, nhưng ông có thứ khác: khả năng khiến người ta muốn đi cùng mình.", "021"),
  ("Có tiền, ông tập hợp được một nhóm quân nhỏ.", "035"),
  ("Đó chưa phải một đội quân lớn. Nhưng với một người từng không có gì, nó là bước đầu tiên.", "035"),
 ]),
 ("Ra trận", [
  ("Ông đem quân theo hiệu úy Trâu Tĩnh, đi đánh giặc Hoàng Cân.", "036"),
  ("Trâu Tĩnh là một hiệu úy của triều đình. Đi theo ông ta là cách nhanh nhất để một nhóm quân nhỏ có được danh phận.", "025"),
  ("Hoàng Cân không phải một toán cướp. Họ là cả một đạo quân tín ngưỡng, hàng chục vạn người.", "037"),
  ("Triều đình phái các đạo quân lớn do Lư Thực, Hoàng Phủ Tung và Chu Tuấn chỉ huy.", "038"),
  ("Lư Thực đánh ở phía bắc, còn Hoàng Phủ Tung và Chu Tuấn đánh ở phía nam.", "043"),
  ("Trong vòng một năm, đạo quân khăn vàng bị đánh tan ở nhiều mặt. Trương Giác bệnh mất giữa chừng.", "039"),
  ("Cuộc chiến kéo dài nhiều tháng, và đây mới chỉ là trận đầu tiên của một thời đại loạn lạc.", "012"),
  ("Sau khi ông chết, quan tài bị mở ra, và đầu ông bị đưa về kinh đô.", "039"),
  ("Công trạng của Lưu Bị trong sử chỉ có một câu: đánh giặc Hoàng Cân, có công.", "040"),
  ("Ông không phải một vị tướng nổi tiếng. Ông chỉ là một người có công trong vô số người ra trận.", "040"),
  ("Phần thưởng lại rất nhỏ: chức huyện úy ở huyện An Hỉ.", "041"),
  ("Một huyện úy không có đại quân, không có quyền lớn. Đó chỉ là một chức nhỏ trong bộ máy nhà Hán.", "015"),
  ("Sau bao tháng đánh trận, người con cháu hoàng tộc vẫn chỉ là một viên quan nhỏ nơi xa.", "041"),
 ]),
 ("Hậu quả và tập sau", [
  ("Dập xong Hoàng Cân, nhiều tướng lĩnh và quan châu quận giờ có quân riêng, và triều đình không còn đủ sức quản họ.", "043"),
  ("Từ đây, nhiều người hiểu rằng ai nắm quân trong tay, người đó nắm số phận.", "036"),
  ("Nhưng Lưu Bị, người từng bị chú quát vì một câu nói về chiếc xe lọng, giờ chỉ ngồi ở một vị trí nhỏ bé.", "023"),
  ("Còn Lưu Bị ngồi ở An Hỉ, và một ngày nọ, một viên đốc bưu đến huyện.", "044"),
  ("Sử chép rất rõ điều ông làm với người ấy: chính tay ông trói viên đốc bưu lại và đánh.", "045"),
  ("Và điều đó khác hẳn chuyện bạn từng nghe.", "045"),
  ("Trong tiểu thuyết, người đánh đốc bưu là Trương Phi. Còn trong sử, đó là chính Lưu Bị.", "044"),
  ("Vì sao một viên huyện úy lại dám làm vậy, và chuyện gì xảy ra sau đó? Tập sau sẽ kể tiếp.", "046"),
 ]),
]
GIONG = ("HEROIC EPIC DELIVERY: a powerful, resonant, commanding male narrator with the gravitas of a historical epic; "
         "strong, confident, ringing voice with rising energy at turning points and names of heroes; firm emphasis, "
         "slightly driving pace, solemn pride when speaking of the Han dynasty and its heroes; not shouting, no theatrical overacting, "
         "still clear Northern Vietnamese diction.")
NGAN = [
 ("hook", "Hơn một nghìn tám trăm năm trước, hàng chục vạn người quấn khăn vàng nổi dậy, và nhà Hán bắt đầu sụp đổ.", ("002", "001")),
 ("boi_canh", "Giữa cơn loạn ấy, có một người bán giày cỏ, dệt chiếu ở huyện Trác. Ông tên là Lưu Bị.", ("003", "004")),
 ("boi_canh", "Ông tự nhận là con cháu một vị vương nhà Hán, nhưng dòng dõi ấy đã xa, và không mang lại cho ông đặc quyền nào.", ("016", "017")),
 ("boi_canh", "Sử chép ông cao bảy thước năm tấc, tay dài quá gối, quay đầu có thể thấy tai mình.", ("019", "016")),
 ("leo_thang", "Hồi nhỏ, ông chỉ cây dâu trước nhà mà nói: sau này ta sẽ ngồi xe có lọng. Người chú quát: đừng nói bậy, cả họ sẽ bị giết.", ("023", "022")),
 ("leo_thang", "Khi Hoàng Cân nổi lên, ông tập hợp người ở quê. Hai người đàn ông đi theo ông: Quan Vũ và Trương Phi.", ("026", "027")),
 ("leo_thang", "Sử chỉ ghi: ba người ngủ chung giường, ân nghĩa như anh em. Trong Tam quốc chí không có lời thề vườn đào.", ("029", "031")),
 ("leo_thang", "Hoàng Cân không phải một toán cướp. Họ là cả một đạo quân tín ngưỡng, hàng chục vạn người.", ("037", "012")),
 ("cu_lat", "Ông theo quân triều đình đánh Hoàng Cân, và lập công.", ("036", "040")),
 ("cu_lat", "Phần thưởng chỉ là chức huyện úy nhỏ ở An Hỉ.", ("041", "042")),
 ("vong_lap", "Rồi một viên đốc bưu đến huyện. Trong tiểu thuyết, người đánh ông ta là Trương Phi. Nhưng trong sử, đó là chính Lưu Bị. Sử thật… lạ hơn cả truyện.", ("044", "045")),
]

CLIPS = {"001","003","005","006","011","015","022","031","037","040","043","044","046"}

def img(k):
    return f"assets/anh_2d/TQ1/{k}.jpg"

# ảnh mới (047-076) gán cho các câu trước đây phải dùng chung ảnh; khóa = số thứ tự câu (từ 0)
NEW_IMG = {7:"047",9:"048",11:"049",16:"050",20:"051",22:"052",23:"053",26:"054",28:"055",29:"056",32:"057",33:"058",39:"059",
           46:"060",52:"061",53:"062",55:"063",57:"064",58:"065",59:"066",62:"067",63:"068",65:"069",67:"070",68:"071",
           69:"072",70:"073",71:"074",74:"075",75:"076"}
_n = 0
_CH3 = []
for _title, _bs in CH:
    _nb = []
    for _t, _k in _bs:
        _nb.append((_t, NEW_IMG.get(_n, _k))); _n += 1
    _CH3.append((_title, _nb))
CH = _CH3

# KHÔNG LẶP ẢNH: mỗi ảnh chỉ xuất hiện đúng một lần. Câu nào trùng ảnh đã dùng (không liền kề) thì giữ ảnh của câu liền trước
# (cảnh kéo dài, máy quay lướt chậm), clip chuyển động chỉ gắn ở lần đầu.
_seen, _prev = set(), None
_CH2 = []
for _title, _bs in CH:
    _nb = []
    _prev0 = _prev
    for _t, _k in _bs:
        if _k in _seen and _k != _prev:
            _k = _prev
        _seen.add(_k); _prev = _k
        _nb.append((_t, _k))
    _CH2.append((_title, _nb))
CH = _CH2

chapters = []
cnt = Counter()
def _split(beats, mx=7):
    n = -(-len(beats) // mx)
    sz = -(-len(beats) // n)
    return [beats[i:i + sz] for i in range(0, len(beats), sz)]

for title, beats0 in CH:
  for beats in _split(beats0):
    chapters.append({"beats": [dict({"text": t, "ai": "ancient Han China scene, 2D ligne claire", "anh_file": img(k)}, **({"clip_file": f"assets/clips_2d/TQ1/{k}.mp4"} if k in CLIPS else {})) for t, k in beats]})
    for t, k in beats:
        cnt[k] += 1
assert all(v <= 1 for v in {k: 0 for k in cnt}.values())
assert len({k for k in cnt}) == len(set(k for _, bs in CH for _, k in bs))
for k in cnt:
    assert (ROOT / img(k)).exists(), k
words = sum(len(t.split()) for _, bs in CH for t, _ in bs)
nb = sum(len(bs) for _, bs in CH)
print(f"dài: {nb} cảnh, {words} chữ, ước tính {words*0.343/60:.1f} phút")

ngan_beats = [{"loai_canh": lc, "text": t, "images": [{"anh_file": img(a)}, {"anh_file": img(b)}]} for lc, t, (a, b) in NGAN]
script = {
 "id": "TQ1",
 "topic": "lich-su",
 "title": "Lưu Bị bán giày cỏ: chính sử kể gì về khởi đầu của ông?",
 "caption": "Người bán giày cỏ, không binh không tiền, đã bắt đầu thế nào trong loạn Hoàng Cân? Tam Quốc theo chính sử, không có vườn đào 🏯",
 "hashtags": ["nguoigacsu", "tamquoc", "luubi", "lichsu", "hoangcan", "chinhsu"],
 "sources": [
  "Trần Thọ, Tam quốc chí, Thục thư, Tiên chủ truyện; Quan Vũ truyện; Trương Phi truyện (nguyên văn và bản dịch hiện đại)",
  "Hậu Hán thư (Linh đế kỷ, Hoàng Phủ Tung truyện) — đối chiếu qua nguồn thứ cấp về khởi nghĩa Hoàng Cân",
  "Wikipedia tiếng Quảng Đông, mục Khởi nghĩa Hoàng Cân",
  "The Scholars, bản dịch tiếng Anh Tiên chủ truyện",
 ],
 "nguon_link": [
  {"ten": "Nguyên văn Quan Vũ, Trương Phi truyện (Tam quốc chí), arteducation.com.tw", "url": "https://www.arteducation.com.tw/", "ngon_ngu": "tiếng Trung"},
  {"ten": "Bản dịch hiện đại Tiên chủ truyện, sanguozhi.5000yan.com", "url": "https://sanguozhi.5000yan.com/", "ngon_ngu": "tiếng Trung"},
  {"ten": "Khởi nghĩa Hoàng Cân, Wikipedia tiếng Quảng Đông", "url": "https://zh-yue.wikipedia.org/", "ngon_ngu": "tiếng Quảng Đông"},
  {"ten": "Bản dịch tiếng Anh Tiên chủ truyện, the-scholars.com", "url": "https://the-scholars.com/", "ngon_ngu": "tiếng Anh"},
 ],
 "music": "none",
 "giong_them": GIONG,
 "pronounce": {},
 "long": {
  "chuyen_canh": "fade",
  "title": "Lưu Bị bán giày cỏ: chính sử kể gì về khởi đầu của ông? | Tam Quốc theo chính sử, tập 1",
  "title_card": "Tam Quốc chính sử: **Lưu Bị** khởi đầu",
  "description": "Năm 184, hàng chục vạn người quấn khăn vàng nổi dậy, nhà Hán bắt đầu sụp đổ. Giữa lúc ấy, một người bán giày cỏ ở huyện Trác tập hợp được hai người bạn và một nhóm quân nhỏ. Tập 1 của series Tam Quốc theo chính sử: không phép thuật, không vườn đào, chỉ những gì Tam quốc chí và Hậu Hán thư chép lại.",
  "voice": "Sadaltager",
  "music": "none",
  "bia": {"anh": img("026"), "nen": img("031"), "huy_hieu": "TAM QUỐC CHÍNH SỬ · TẬP 1", "dong1": "KHÔNG CÓ", "dong2": "VƯỜN ĐÀO", "gach": True,
          "dong3": "Lưu Bị <b>thật sự</b> khởi đầu thế nào?"},
  "chapters": chapters,
 },
 "binh_luan": {
  "dai": {"ghim": "Tập này mình bám theo Tam quốc chí nên một số cảnh quen thuộc trong tiểu thuyết, như vườn đào, không có trong video. Hình ảnh nhân vật là tranh minh họa, vì sử không tả ngoại hình ngoài chiều cao, tay dài và tai lớn của Lưu Bị.", "phu": []},
  "ngan": {"ghim": "Về cảnh vườn đào kết nghĩa: Tam quốc chí chỉ chép Lưu Bị, Quan Vũ, Trương Phi ngủ chung giường, ân nghĩa như anh em. Lời thề vườn đào là do tiểu thuyết thêm vào 🏯", "phu": []},
 },
 "ngan": {
  "hook_text": "Lưu Bị: người bán giày cỏ\n**không hề thề vườn đào**",
  "hooks": ["Sử chép Lưu Bị không hề thề vườn đào. Vậy ba người họ gắn bó với nhau thế nào?"],
  "caption": "Người bán giày cỏ, không binh không tiền, đã bắt đầu thế nào trong loạn Hoàng Cân? Tam Quốc theo chính sử, không có vườn đào 🏯 Bạn có biết chuyện này chưa?",
  "beats": ngan_beats,
  "anh_bia": img("026"),
 },
}
script["scenes"] = [{"type": "hook" if i == 0 else "text", "text": b["text"], "voice": b["text"]} for i, b in enumerate(ngan_beats)]
(ROOT / "scripts" / "TQ1.json").write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok")
