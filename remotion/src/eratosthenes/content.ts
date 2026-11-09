import {FPS} from '../lib/theme';
import {beatSeconds} from '../thales/content';
import ledaDur from './leda_dur.json';

// Video khoa học số 1 (dọc 1080x1920, tiếng Việt, bản duyệt trước): Eratosthenes đo Trái Đất bằng một cây gậy.
// Nguồn đã kiểm: xem remotion/scripts/eratosthenes.md

export type SceneId = 'hook' | 'problem' | 'clue' | 'idea' | 'calc' | 'compare' | 'modern' | 'outro';
export const END_E = 3.5;

export const TEXT_E: Record<SceneId, string[]> = {
  hook: [
    'Một cây gậy mà đo được cả Trái Đất?',
    'Hơn hai nghìn năm trước, chưa có vệ tinh. Vậy mà Eratosthenes đã làm được.',
  ],
  problem: ['Không ai đi vòng quanh Trái Đất được, nên không thể đo thẳng.'],
  clue: [
    'Người ta kể: ở Syene, trưa ngày dài nhất năm, nắng rọi thẳng xuống đáy giếng.',
    'Cùng lúc ở Alexandria, cột dựng thẳng vẫn có bóng, nghiêng một phần năm mươi vòng tròn.',
  ],
  idea: [
    'Nắng chiếu song song, nên hai nơi khác nhau chỉ vì mặt đất cong.',
    'Góc cái bóng chính là góc giữa hai thành phố, nhìn từ tâm Trái Đất.',
  ],
  calc: [
    'Người đếm bước cho biết hai thành phố cách nhau khoảng năm nghìn stadia.',
    'Một phần năm mươi vòng, nên cả Trái Đất dài gấp năm mươi lần: hai trăm năm mươi nghìn stadia.',
  ],
  compare: [
    'Mỗi stadion khoảng một trăm năm mươi bảy mét rưỡi, vậy là gần bốn mươi nghìn cây số.',
    'Số đo ngày nay chỉ nhỉnh hơn một chút: lệch chưa tới hai phần trăm.',
  ],
  modern: [
    'Hơn hai nghìn năm sau, người Pháp làm tương tự: đo từ Dunkerque tới Barcelona, suy ra cả đường từ Bắc Cực tới xích đạo.',
    'Một phần mười triệu đường ấy là mét đầu tiên.',
  ],
  outro: ['Một cây gậy, một cái bóng và phép tính. Đó là cách chúng ta biết.'],
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
  conv: '250 000 stadia × 157,5 m',
  conv2: '≈ 39 375 km',
  barE: 'Eratosthenes (1 stadion ≈ 157,5 m)',
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
};

export type Beat = {text: string; start: number; dur: number};
export type SceneTl = {id: SceneId; start: number; dur: number; beats: Beat[]; bs: number[]};
const ORDER: SceneId[] = ['hook', 'problem', 'clue', 'idea', 'calc', 'compare', 'modern', 'outro'];

export function timeline(): {scenes: SceneTl[]; total: number; beats: Beat[]} {
  let f = 0;
  let voiceIdx = 0;
  const all: Beat[] = [];
  const scenes: SceneTl[] = ORDER.map((id) => {
    const texts = id === 'outro' ? [...TEXT_E[id], ''] : TEXT_E[id];
    const beats: Beat[] = texts.map((text) => {
      // Có giọng đọc thật (Leda): nhịp = thời lượng giọng + 0,5 s, không ngắn hơn 93% ước tính để hoạt cảnh kịp chạy
      let sec = text ? beatSeconds('vi', text) : END_E;
      if (text && ledaDur[voiceIdx] !== undefined) sec = Math.max(ledaDur[voiceIdx] + 0.5, sec * 0.93);
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
