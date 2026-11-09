import {FPS} from '../lib/theme';
import {beatSeconds} from '../thales/content';
import ledaDur from './leda_dur.json';

// Video khoa học số 2 (dọc 1080x1920, tiếng Việt): Cân Trái Đất (Cavendish). Kịch bản và nguồn: ke-hoach/khoa-hoc-video-2-can-trai-dat-kich-ban.md
// Văn bản ở đây là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-cavendish.json.

export type SceneId = 'hook' | 'mount' | 'idea' | 'device' | 'calc' | 'outro';
export const END_C = 3.5;

export const TEXT_C: Record<SceneId, string[]> = {
  hook: [
    'Cân một quả táo thì dễ. Nhưng làm sao cân được cả Trái Đất?',
    'Không có chiếc cân nào đủ lớn, và cũng không ai nhấc nổi một hành tinh lên.',
  ],
  mount: [
    'Năm 1774, nhà thiên văn Nevil Maskelyne mang một sợi dây dọi lên chân núi Schiehallion ở Scotland.',
    'Dây dọi là sợi dây treo một quả nặng ở đầu, nên lúc nào cũng chỉ thẳng xuống đất.',
    'Ngọn núi đứng bên cạnh cũng hút quả nặng, nên sợi dây bị lệch đi một chút xíu.',
    'So lực hút của núi với lực hút của cả Trái Đất, người ta tính được Trái Đất nặng gấp ngọn núi bao nhiêu lần.',
    'Nhưng không ai biết bên trong núi là loại đá nào, nặng hay nhẹ, nên con số chỉ là ước chừng.',
    'Kết quả ra thấp hơn thật khoảng 1/5.',
  ],
  idea: [
    'Cách tốt hơn là mang ngọn núi vào trong phòng, bằng những quả chì mà mình cân được.',
    'Ý tưởng này của mục sư John Michell, nhưng ông mất trước khi kịp làm.',
    'Người làm tiếp là Henry Cavendish, một nhà khoa học nổi tiếng là sống ẩn dật, vào năm 1797.',
  ],
  device: [
    'Ông treo một thanh gỗ dài bằng sợi dây mảnh, 2 đầu thanh gắn 2 quả cầu chì nhỏ.',
    'Rồi ông đặt gần chúng 2 quả cầu chì lớn, mỗi quả nặng hơn 150 ki-lô-gam.',
    'Quả lớn kéo quả nhỏ về phía mình, làm thanh gỗ xoay đi một chút.',
    'Lực kéo ấy nhỏ hơn sức nặng của chính quả cầu nhỏ hàng chục triệu lần.',
    'Chỉ cần một luồng gió, hay một bên hộp ấm hơn bên kia, là thanh gỗ lắc theo gió chứ không theo quả chì.',
    'Vì vậy Cavendish nhốt cả thiết bị trong một căn nhà kín, và đứng bên ngoài nhìn qua kính thiên văn.',
    'Ông kéo dây để đổi chỗ quả cầu lớn sang bên kia, thanh gỗ lại xoay ngược lại, và ông ghi lại từng chút một.',
  ],
  calc: [
    'Cùng một quả cầu nhỏ, một bên bị Trái Đất kéo xuống đất, một bên bị quả chì kéo sang ngang.',
    'So hai lực ấy, biết quả chì nặng bao nhiêu, nằm cách bao xa, và Trái Đất to cỡ nào, là tính ra được Trái Đất nặng bao nhiêu.',
    'Kết quả: Trái Đất nặng gần 5,5 lần so với một khối nước cùng kích thước.',
    'Đá trên mặt đất nhẹ hơn thế nhiều, nên bên trong Trái Đất phải có thứ gì đó rất nặng.',
    'Nhân lên cho cả quả cầu, Trái Đất nặng khoảng 6 nghìn tỷ tỷ tấn, mà số đo ngày nay chỉ lệch chưa đến 1%.',
  ],
  outro: [
    'Chỉ với 2 quả chì, một sợi dây và rất nhiều kiên nhẫn, Cavendish đã cân được cả Trái Đất.',
  ],
};

export const LAB: Record<string, string> = {
  appleOk: 'quả táo: cân được',
  earthQ: 'Trái Đất: cân bằng gì?',
  noScale: 'không có cân nào đủ lớn',
  place: '1774 · núi Schiehallion, Scotland',
  maske: 'Maskelyne',
  plumb: 'dây dọi',
  straight: 'chỉ thẳng xuống đất',
  tilt: 'bị núi kéo lệch',
  notScale: '(độ lệch vẽ to hơn thật)',
  fMount: 'lực hút của núi',
  fEarth: 'lực hút của Trái Đất',
  ratio: 'so hai lực → Trái Đất nặng gấp núi bao nhiêu lần',
  rock: 'bên trong núi là đá gì?',
  densTitle: 'độ nặng trung bình của Trái Đất',
  densUnit: '(so với nước = 1)',
  barH: 'Maskelyne – Hutton, 1774',
  barNow: 'số đo ngày nay',
  lower: 'thấp hơn khoảng 1/5',
  mountain: 'ngọn núi',
  lead: 'quả chì: cân được',
  michell: 'John Michell, mục sư',
  michellEnd: 'mất trước khi kịp làm',
  cav: 'Henry Cavendish, 1797',
  cavTag: 'sống ẩn dật',
  topView: '(nhìn từ trên xuống)',
  rod: 'thanh gỗ dài',
  small: '2 quả cầu chì nhỏ',
  wire: 'sợi dây mảnh',
  big: '2 quả cầu chì lớn, hơn 150 kg',
  rotate: 'thanh xoay (vẽ to hơn thật)',
  weight: 'sức nặng quả nhỏ',
  pull: 'lực quả chì kéo',
  tiny: 'nhỏ hơn hàng chục triệu lần',
  wind: 'gió',
  warm: 'bên ấm hơn',
  shake: 'lắc theo gió, không theo quả chì',
  shed: 'căn nhà kín',
  tele: 'nhìn qua kính thiên văn',
  swap: 'đổi chỗ quả lớn',
  back: 'thanh xoay ngược lại',
  noteB: 'ghi lại',
  eFall: 'Trái Đất kéo xuống đất',
  eSide: 'quả chì kéo sang ngang',
  notRatio: '(không vẽ đúng tỉ lệ)',
  c1: 'quả chì nặng bao nhiêu',
  c2: 'nằm cách bao xa',
  c3: 'Trái Đất to cỡ nào',
  res: 'Trái Đất nặng bao nhiêu',
  water: '1 khối nước',
  earthSame: 'Trái Đất, cùng kích thước',
  times: 'gần 5,5 lần',
  crust: 'đá mặt đất ≈ 2,5–3',
  whole: 'cả Trái Đất ≈ 5,5',
  core: 'bên trong: thứ gì đó rất nặng',
  mass: '≈ 6 nghìn tỷ tỷ tấn',
  zeros: '(số 6 và 21 chữ số 0, tính ra tấn)',
  bCav: 'Cavendish: 5,48',
  bNow: 'ngày nay: 5,51',
  diff: 'lệch chưa đến 1%',
  page: 'Người Giải Mã',
  tag: 'Cân cả Trái Đất, chỉ bằng hai quả chì.',
};

export type Beat = {text: string; start: number; dur: number};
export type SceneTl = {id: SceneId; start: number; dur: number; beats: Beat[]; bs: number[]};
const ORDER: SceneId[] = ['hook', 'mount', 'idea', 'device', 'calc', 'outro'];

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
