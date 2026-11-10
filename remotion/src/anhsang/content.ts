import {FPS} from '../lib/theme';
import {beatSeconds} from '../thales/content';
import ledaDur from './leda_dur.json';

// Video khoa học số 3 (dọc 1080x1920, tiếng Việt): Đo tốc độ ánh sáng. Kịch bản: ke-hoach/khoa-hoc-video-3-toc-do-anh-sang-kich-ban.md
// Văn bản ở đây là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-anhsang.json.

export type SceneId = 'hook' | 'lantern' | 'io' | 'romer' | 'divide' | 'wheel' | 'outro';
export const END_C = 3.5;

export const TEXT_C: Record<SceneId, string[]> = {
  hook: [
    "Nếu Mặt Trời tắt ngay bây giờ, bạn vẫn thấy nó sáng thêm hơn 8 phút nữa.",
    "Vì ánh sáng không đến tức thì, nó phải đi và mất thời gian. Nhưng nó nhanh đến mức bật đèn là sáng ngay.",
    "Người đầu tiên chứng minh điều ngược lại không dùng thước hay đồng hồ, mà dùng một mặt trăng của sao Mộc.",
  ],
  lantern: [
    "Năm 1638, nhà bác học Galileo mô tả trong sách một cách thử.",
    "Hai người, mỗi người cầm một đèn lồng, đứng cách nhau chưa đầy 2 ki-lô-mét.",
    "Người thứ nhất mở đèn. Người thứ hai vừa thấy thì mở đèn của mình. Người thứ nhất xem chờ bao lâu.",
    "Kết quả: Galileo không phân biệt được có độ trễ hay không. Ông viết: nếu không tức thì thì cũng nhanh vô cùng.",
    "Dễ hiểu thôi: ánh sáng chạy hết quãng đó chỉ trong 5 phần triệu giây, còn tay người chậm hơn hàng nghìn lần.",
  ],
  io: [
    "Muốn thấy độ trễ, phải cho ánh sáng đi xa hơn rất nhiều. Năm 1672, nhà thiên văn trẻ người Đan Mạch Ole Rømer đến làm việc ở Đài thiên văn Paris.",
    "Ở đó người ta theo dõi Io, một mặt trăng của sao Mộc. Cứ 42 tiếng rưỡi, Io quay trọn một vòng.",
    "Mỗi vòng, Io chui vào bóng sao Mộc rồi ló ra. Như một chiếc đồng hồ ngoài vũ trụ, mỗi lần ló ra là một nhịp.",
    "Rømer thấy điều lạ. Trái Đất đi xa sao Mộc, Io ló ra càng muộn. Trái Đất lại gần, Io ló ra sớm hơn.",
    "Mỗi vòng chỉ lệch chút xíu, không thấy được. Nhưng gộp 40 vòng lại thì độ lệch hiện rõ.",
    "Ông hiểu ra: Io vẫn quay đều. Chỉ là ánh sáng phải đi quãng đường dài hơn, nên tới muộn hơn.",
    "Giống thư gửi đều mỗi ngày: đường dài ra thì thư đến muộn dần, dù người gửi vẫn đúng giờ.",
    "Ngày 9/11/1676, Io ló ra muộn 10 phút so với bảng giờ tính từ tháng 8, như Rømer đã báo trước.",
  ],
  romer: [
    "Từ đó ông ước tính ánh sáng cần khoảng 22 phút để đi hết đường kính quỹ đạo Trái Đất.",
    "Không phải ai cũng tin. Giám đốc đài Cassini phản đối, vì hiện tượng không thấy ở các mặt trăng khác.",
    "Năm 1729, James Bradley dùng cách đo hoàn toàn khác và cũng thấy ánh sáng có tốc độ hữu hạn.",
  ],
  divide: [
    "Giờ chỉ còn một phép chia: tốc độ = quãng đường ÷ thời gian.",
    "Quãng đường: khoảng 300 triệu km. Thời gian: 22 phút, tức 1 320 giây.",
    "300 triệu ÷ 1 320 ≈ 227 nghìn ki-lô-mét mỗi giây.",
    "Hơi thấp, vì ánh sáng thực ra chỉ mất gần 17 phút. Với thời gian đúng, ra khoảng 300 nghìn km mỗi giây.",
    "Mỗi giây, ánh sáng chạy quanh Trái Đất 7 vòng rưỡi.",
  ],
  wheel: [
    "Năm 1849, nhà vật lý Pháp Hippolyte Fizeau đo ánh sáng ngay trên mặt đất, không cần nhờ bầu trời.",
    "Hai kính thiên văn cách nhau hơn 8,6 km, ở Suresnes và trên đồi Montmartre.",
    "Giữa đường ánh sáng là bánh xe 720 răng cưa. Ánh sáng chui qua khe, tới gương xa rồi dội về.",
    "Bánh xe quay nhanh dần. Đến một tốc độ, ánh sáng dội về gặp răng kế bên chắn lại, mắt không thấy gì.",
    "Quay nhanh gấp đôi, ánh sáng lại lọt qua khe kế bên. Lúc ấy 25 vòng mỗi giây, mỗi khe chuyển khe mất 55 phần triệu giây.",
    "Đó cũng là thời gian ánh sáng đi hơn 17 km, cả đi lẫn về.",
    "17 km ÷ 55 phần triệu giây ≈ 313 nghìn km mỗi giây, chỉ lệch 4,5% so với số đúng.",
  ],
  outro: [
    "Ngày nay, tốc độ ánh sáng là 299 792 458 mét mỗi giây, chính xác.",
    "Từ 1983, người ta lấy luôn tốc độ ấy làm chuẩn: 1 mét là quãng ánh sáng đi trong 1/299 792 458 giây.",
    "Từ 2 chiếc đèn lồng, một mặt trăng và một bánh xe, con người đã đo được ánh sáng chạy nhanh đến mức nào.",
  ],
};

export type Beat = {text: string; start: number; dur: number};
export type SceneTl = {id: SceneId; start: number; dur: number; beats: Beat[]; bs: number[]};
const ORDER: SceneId[] = ['hook', 'lantern', 'io', 'romer', 'divide', 'wheel', 'outro'];

export function timeline(): {scenes: SceneTl[]; total: number; beats: Beat[]} {
  let f = 0;
  let voiceIdx = 0;
  const all: Beat[] = [];
  const scenes: SceneTl[] = ORDER.map((id) => {
    const texts = id === 'outro' ? [...TEXT_C[id], ''] : TEXT_C[id];
    const beats: Beat[] = texts.map((text) => {
      let sec = text ? beatSeconds('vi', text) : END_C;
      const d = (ledaDur as number[])[voiceIdx];
      if (text && d !== undefined) sec = Math.max(d + 0.5, 2.4);
      if (text) voiceIdx++;
      const dur = Math.round(sec * FPS);
      const b = {text, start: f, dur};
      f += dur;
      all.push(b);
      return b;
    });
    const start = beats[0].start;
    return {id, start, dur: f - start, beats, bs: beats.map((b) => b.start - start)};
  });
  return {scenes, total: f, beats: all};
}
