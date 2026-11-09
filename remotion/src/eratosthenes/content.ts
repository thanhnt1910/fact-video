import {FPS} from '../lib/theme';
import {beatSeconds} from '../thales/content';
import ledaDur from './leda_dur.json';

// Video khoa học số 1 (dọc 1080x1920, tiếng Việt, bản duyệt trước): Eratosthenes đo Trái Đất bằng một cây gậy.
// Nguồn đã kiểm: xem remotion/scripts/eratosthenes.md

export type SceneId = 'hook' | 'problem' | 'clue' | 'orange' | 'calc' | 'compare' | 'modern' | 'outro';
export const END_E = 3.5;

// Kịch bản đã duyệt 09/11/2026 (viết lại thành một mạch, có ví dụ quả cam và cái bánh). Mỗi phần tử là một lượt đọc giọng.
export const TEXT_E: Record<SceneId, string[]> = {
  hook: [
    'Hơn hai nghìn năm trước, có một người đã tính ra Trái Đất to cỡ nào.',
    'Ông không có vệ tinh, không có máy bay. Ông chỉ có một cây gậy.',
  ],
  problem: ['Khó ở chỗ Trái Đất quá lớn. Không ai đi bộ hết một vòng để đo được.'],
  clue: [
    'Ông tên là Eratosthenes. Người ta kể ông nghe một chuyện lạ ở thành phố Syene.',
    'Mỗi năm có một trưa, nắng rọi thẳng xuống tận đáy giếng. Lúc đó Mặt Trời nằm ngay trên đầu, nên cột dựng đứng không có bóng.',
    'Cùng trưa hôm đó, ở thành phố Alexandria, cách Syene khoảng tám trăm cây số, cây gậy dựng đứng lại có bóng.',
    'Cùng một Mặt Trời, cùng một giờ. Chỗ này không có bóng, chỗ kia có bóng. Vì sao?',
  ],
  orange: [
    'Hãy nhìn một quả cam. Cắm hai cây tăm lên vỏ cam, rồi rọi đèn pin từ xa.',
    'Vỏ cam cong, nên hai cây tăm hướng về hai phía khác nhau, và bóng của chúng khác nhau.',
    'Nếu mặt đất phẳng như tờ giấy, hai cái bóng sẽ giống hệt nhau.',
    'Vậy cái bóng chính là bằng chứng: mặt đất cong. Hai nơi càng lệch hướng, bóng càng dài.',
  ],
  calc: [
    'Ông đo cái bóng, và tính ra hai thành phố lệch nhau đúng một phần năm mươi vòng.',
    'Giống như cắt cái bánh thành năm mươi miếng, hai thành phố cách nhau đúng một miếng.',
    'Người ta đã đếm bước chân và biết khoảng cách giữa hai thành phố khoảng tám trăm cây số.',
    'Một miếng là tám trăm cây số, thì cả cái bánh là năm mươi miếng như thế.',
    'Tám trăm nhân năm mươi, được khoảng bốn mươi nghìn cây số. Đó là chiều dài một vòng quanh Trái Đất.',
  ],
  compare: [
    'Ngày nay vệ tinh đo được hơn bốn mươi nghìn cây số. Ông chỉ lệch chưa tới hai phần trăm.',
    'Thời đó người ta đo bằng đơn vị khác nên đổi ra cây số còn tranh cãi, nhưng kết quả vẫn rất gần.',
  ],
  modern: [
    'Cách nghĩ ấy còn dùng đến nay.',
    'Người Pháp đo một đoạn từ Dunkerque tới Barcelona, rồi tính ra cả đường từ Bắc Cực tới xích đạo.',
    'Một phần mười triệu của đường ấy được lấy làm một mét.',
  ],
  outro: ['Một cây gậy, một cái bóng và một phép chia. Đó là cách chúng ta biết.'],
};

export const LAB: Record<string, string> = {
  year: 'khoảng 240 TCN',
  earthQ: 'Trái Đất to bao nhiêu?',
  noSat: 'chưa có vệ tinh',
  hero: 'Eratosthenes',
  stickTag: 'và một cây gậy',
  walk: 'đi bộ để đo?',
  illus: '(minh họa)',
  syene: 'Syene (nay là Aswan)',
  noon: 'trưa ngày dài nhất năm',
  noShadow: 'cột không có bóng',
  alex: 'Alexandria',
  sameTime: 'cùng lúc đó',
  ang: '7,2° = 1/50 vòng',
  notScale: '(góc vẽ to hơn thật cho dễ nhìn)',
  flat: 'nếu đất phẳng: Alexandria cũng không có bóng',
  curved: 'đất cong: hai nơi nghiêng khác nhau',
  sameAngle: 'cùng một góc α',
  stadia5: '≈ 5 000 stadia',
  counted: 'người đếm bước đo',
  stadiaDef: 'stadion: một đơn vị đo chiều dài thời xưa',
  part1: '1/50 vòng',
  total: '= 250 000 stadia',
  eq50: '5 000 × 50',
  source: 'theo Cleomedes, nguồn còn lại duy nhất',
  conv: '800 km × 50 (làm tròn)',
  conv2: '≈ 39 375 km',
  barE: 'Eratosthenes (đổi theo cách phổ biến)',
  barNow: 'Số đo ngày nay, vòng qua hai cực',
  diff: 'lệch khoảng 1,6%',
  unsure1: '1 stadion dài bao nhiêu chưa chắc chắn',
  unsure2: 'hai thành phố không thẳng hàng hoàn hảo',
  fr: 'Pháp, 1792–1798',
  dk: 'Dunkerque',
  bcn: 'Barcelona',
  pole: 'Bắc Cực',
  equator: 'Xích đạo',
  rest: 'phần còn lại: suy ra',
  meter1: '1 mét =',
  meter2: '1/10 000 000 đường này',
  tag: 'Chúng ta biết điều đó bằng cách nào.',
  page: 'Người Giải Mã',
  km800: '≈ 800 km',
  cam: '(ví dụ: quả cam, không phải Trái Đất thật)',
  tam: 'tăm',
  torch: 'đèn pin',
  paper: 'mặt phẳng như tờ giấy',
  same: 'hai bóng giống hệt nhau',
  differ: 'hai bóng khác nhau',
  proof: 'bóng khác nhau = mặt đất cong',
  slice1: '1 miếng = 1/50 vòng',
  cake: 'cả vòng = 50 miếng',
  mul: '800 km × 50',
  total2: '≈ 40 000 km',
  round: '(làm tròn)',
  planes: 'không vệ tinh, không máy bay',
  idea: 'Cách nghĩ ấy',
};

export type Beat = {text: string; start: number; dur: number};
export type SceneTl = {id: SceneId; start: number; dur: number; beats: Beat[]; bs: number[]};
const ORDER: SceneId[] = ['hook', 'problem', 'clue', 'orange', 'calc', 'compare', 'modern', 'outro'];

export function timeline(): {scenes: SceneTl[]; total: number; beats: Beat[]} {
  let f = 0;
  let voiceIdx = 0;
  const all: Beat[] = [];
  const scenes: SceneTl[] = ORDER.map((id) => {
    const texts = id === 'outro' ? [...TEXT_E[id], ''] : TEXT_E[id];
    const beats: Beat[] = texts.map((text) => {
      // Có giọng đọc thật (Leda): nhịp = thời lượng giọng + 0,5 s
      let sec = text ? beatSeconds('vi', text) : END_E;
      if (text && ledaDur[voiceIdx] !== undefined) sec = Math.max(ledaDur[voiceIdx] + 0.5, 2.4);
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
