import {FPS} from '../lib/theme';
import {beatSeconds} from '../thales/content';

// Video 1 bản 3 (tiếng Việt, duyệt trước): vì sao người xưa không đo được, rồi cách của Thales, rồi ngày nay.
// Nguồn: xem remotion/scripts/thales.md

export type SceneId = 'hook' | 'tools' | 'seked' | 'idea' | 'sun' | 'equal' | 'half' | 'stick' | 'numbers' | 'modern' | 'everest' | 'everyday' | 'outro';
export const END3 = 3.5;

export const TEXT3: Record<SceneId, string[]> = {
  hook: [
    'Theo các tác giả cổ đại, Thales là một nhà tư tưởng Hy Lạp sống cách đây khoảng 2.600 năm, và từng đến Ai Cập.',
    'Ông đứng trước Đại Kim Tự Tháp và tự hỏi: nó cao bao nhiêu?',
    'Nghe thì dễ. Nhưng hãy thử nghĩ xem, với dụng cụ của thời đó, bạn sẽ đo bằng cách nào?',
  ],
  tools: [
    'Người Ai Cập thời đó rất giỏi đo đất. Mỗi lần sông Nin dâng nước làm mất ranh giới ruộng, họ lại căng dây để đo lại.',
    'Những người đo đất ấy được gọi là người căng dây. Chỉ cần một sợi dây dài, họ đo được cạnh đáy kim tự tháp: khoảng hai trăm ba mươi mét.',
    'Đo ngang trên mặt đất thì dễ. Còn đo thẳng lên trời thì sao?',
  ],
  seked: [
    'Người Ai Cập còn có một cách khác, ghi trong giấy cói Rhind. Họ mô tả độ dốc của kim tự tháp bằng một tỉ lệ gọi là seked: lên cao một khuỷu tay thì mặt dốc lùi vào bao nhiêu bàn tay.',
    'Biết cạnh đáy và tỉ lệ ấy, họ tính được chiều cao. Với Đại Kim Tự Tháp, một nửa cạnh đáy chia năm rưỡi rồi nhân bảy cho ra khoảng một trăm bốn mươi bảy mét.',
    'Nhưng cách này dành cho lúc thiết kế, khi đã biết trước kích thước định xây. Các ghi chép còn lại không cho biết họ đo độ dốc của một tháp đã xây xong bằng cách nào.',
    'Theo suy luận của chúng ta, muốn đo độ dốc phải đặt dụng cụ lên mặt tháp, mà mặt tháp khi đó ốp đá vôi trắng nhẵn. Thales hỏi: có cách đo chiều cao mà không cần bản thiết kế và không cần leo lên không?',
  ],
  idea: [
    'Vấn đề là gì? Tỉ lệ độ dốc cần có sẵn bản thiết kế. Dây chỉ đo được mặt đất. Còn chiều cao thì nằm thẳng đứng.',
    'Vậy nếu biến chiều cao thành thứ nằm trên mặt đất thì sao? Có một thứ làm được điều đó: cái bóng.',
    'Các ghi chép cổ kể rằng Thales đã dùng đúng cái bóng để đo kim tự tháp. Chiều cao như nằm xuống đất.',
  ],
  sun: [
    'Thales chỉ có một dụng cụ: Mặt Trời.',
    'Bạn biết điều này từ chính cái bóng của mình. Khi Mặt Trời còn thấp, bóng của bạn rất dài.',
    'Khi Mặt Trời lên cao hơn, bóng ngắn lại. Bóng thay đổi vì góc của ánh nắng thay đổi.',
    'Và có một lúc trong ngày, bóng của bạn dài đúng bằng chiều cao của bạn.',
  ],
  equal: [
    'Chuyện xưa kể rằng Thales chờ đúng lúc đó.',
    'Vì sao? Vì Mặt Trời chiếu vào ông và vào kim tự tháp theo cùng một góc. Nên bóng của kim tự tháp cũng dài bằng chiều cao của nó.',
    'Vậy ông chỉ cần đo bóng của kim tự tháp trên mặt đất. Độ dài đó chính là chiều cao.',
  ],
  half: [
    'Nhưng có một điểm vướng. Bóng bắt đầu từ mép kim tự tháp, còn chiều cao nằm phía trên tâm của nó.',
    'Nhìn từ trên xuống, tâm cách mép đúng nửa cạnh đáy.',
    'Vì vậy chiều cao bằng phần bóng ta đo được, cộng thêm nửa cạnh đáy.',
  ],
  stick: [
    'Nhưng nếu Mặt Trời không bao giờ cho ta khoảnh khắc hoàn hảo đó thì sao?',
    'Plutarch kể về một mẹo khác: cắm một cây gậy thẳng đứng ngay đầu bóng của kim tự tháp.',
    'Ánh nắng đến theo các tia song song, nên nó nghiêng cùng một góc trên cây gậy và trên kim tự tháp.',
    'Như vậy ta có hai tam giác cùng hình dạng, một nhỏ, một khổng lồ. Phóng to tam giác nhỏ lên, nó khớp đúng với tam giác lớn.',
    'Nên các cạnh có cùng tỉ lệ: kim tự tháp cao hơn cây gậy bao nhiêu lần thì bóng của nó dài hơn bóng cây gậy bấy nhiêu lần.',
  ],
  numbers: [
    'Thử với số liệu ví dụ. Một cây gậy dài hai mét đổ bóng dài ba mét.',
    'Vậy cứ hai mét chiều cao thì đi kèm ba mét bóng.',
    'Bóng của kim tự tháp, tính từ tâm đáy, đo được 220 mét. Lấy 220 nhân hai rồi chia ba: khoảng 147 mét.',
    'Đại Kim Tự Tháp khi xây xong cao khoảng 146,6 mét. Nay lớp đá ốp ngoài đã mất, chỉ còn 138,5 mét.',
  ],
  modern: [
    'Hơn hai nghìn năm sau, người ta vẫn dùng đúng ý tưởng ấy, chỉ là chính xác hơn nhiều.',
    'Người đo đạc đặt máy đo góc trên ba chân, đo một đoạn nằm ngang trên đất, rồi đo góc nhìn lên đỉnh tòa nhà.',
    'Từ đoạn ngang và góc đó, họ tính ra chiều cao mà không cần leo lên.',
  ],
  everest: [
    'Năm một nghìn tám trăm năm mươi sáu, Cục Khảo sát Ấn Độ công bố độ cao đỉnh Everest. Họ đo góc từ những trạm cách đỉnh khoảng một trăm bảy mươi cây số.',
    'Lúc đó chưa ai leo lên tới đỉnh. Họ chỉ dùng góc đo được, nối từ một đoạn đường chuẩn trên đồng bằng thành cả một chuỗi tam giác.',
    'Kết quả khi đó là khoảng tám nghìn tám trăm bốn mươi mét.',
    'Năm hai nghìn không trăm hai mươi, Trung Quốc và Nepal cùng công bố số đo mới: tám nghìn tám trăm bốn mươi tám phẩy tám mươi sáu mét.',
  ],
  everyday: [
    'Cách của Thales còn dùng được ngay trong đời thường. Muốn biết một cái cây cao bao nhiêu, bạn chỉ cần một cây gậy và một buổi nắng.',
    'Bản đồ, mô hình thu nhỏ và bản vẽ của kiến trúc sư cũng dựa trên điều đó: cùng hình dạng, chỉ khác kích thước, nên các cạnh luôn giữ một tỉ lệ.',
    'Ý tưởng này cho ta thấy: muốn đo thứ ta không với tới, hãy biến nó thành thứ ta đo được.',
  ],
  outro: [
    'Không leo trèo. Không dây thừng. Chỉ có ánh nắng, một cây gậy và phép tỉ lệ.',
    'Thales có thật sự làm vậy không? Chưa thể chắc. Nhưng cách đo này đúng với bất kỳ ai, ở bất kỳ đâu, ngay hôm nay. Đó là cách chúng ta biết.',
  ],
};

export const LABELS3: Record<string, string> = {
  sekRise: '1 khuỷu tay = 7 bàn tay',
  sekRun: '5½ bàn tay',
  sekName: 'seked: độ dốc',
  sekCalc: '115 m ÷ 5½ × 7 ≈ 147 m',
  sekDesign: 'cần biết sẵn kích thước',
  infer: 'suy luận của chúng ta',
  sekHint: 'đặt dụng cụ lên mặt dốc?',
  title: 'Thales đo kim tự tháp như thế nào',
  halfBase: '½ cạnh đáy',
  measured: 'đo được',
  angle: 'góc',
  sameAngle: 'cùng một góc',
  sameShape: 'cùng hình dạng',
  ratio: 'bóng : cao = 3 : 2',
  built: 'xây xong: 146,6 m',
  today: 'hiện nay: 138,5 m',
  scale: '(không đúng tỉ lệ)',
  tag: 'Chúng ta biết điều đó bằng cách nào.',
  nowTag: 'NGÀY NAY',
  formula: 'đoạn ngang + góc nhìn → chiều cao',
  slope: '≈ 186 m',
  men: '≈ 86 người',
  ladderTag: 'thang: vài mét',
  base: '230 m',
  far: '≈ 170 km',
  ev1856: '1856: ≈ 8 840 m',
  ev2020: '2020: 8 848,86 m',
  model: 'mô hình',
  real: 'thật',
  height: 'cao?',
  tree: 'cây cao?',
  slopeName: 'đường dốc',
  baseLine: 'đoạn ngang',
  farLeft: 'còn rất xa',
  baseStd: 'đường chuẩn',
  tower: 'hơn tám mươi người',
};

export type Beat3 = {text: string; start: number; dur: number};
export type SceneTl3 = {id: SceneId; start: number; dur: number; beats: Beat3[]; bs: number[]};
const ORDER: SceneId[] = ['hook', 'tools', 'seked', 'idea', 'sun', 'equal', 'half', 'stick', 'numbers', 'modern', 'everest', 'everyday', 'outro'];

export function timeline3(): {scenes: SceneTl3[]; total: number; beats: Beat3[]} {
  let f = 0;
  const all: Beat3[] = [];
  const scenes: SceneTl3[] = ORDER.map((id) => {
    const texts = id === 'outro' ? [...TEXT3[id], ''] : TEXT3[id];
    const beats: Beat3[] = texts.map((text) => {
      const dur = Math.round((text ? beatSeconds('vi', text) : END3) * FPS);
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
