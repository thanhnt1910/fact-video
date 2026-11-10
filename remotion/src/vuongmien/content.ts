import {FPS} from '../lib/theme';
import {beatSeconds} from '../thales/content';
import ledaDur from './leda_dur.json';

// Video khoa học số 6 (dọc 1080x1920, tiếng Việt): Làm sao biết vương miện có pha bạc? Kịch bản: ke-hoach/khoa-hoc-video-6-vuong-mien-kich-ban.md
// Văn bản ở đây là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-vuongmien.json.

export type SceneId = 'hook' | 'can' | 'nuoc' | 'cong' | 'gal' | 'nay';
export const END_C = 3.5;

export const TEXT_C: Record<SceneId, string[]> = {
  hook: [
    "Vương miện vàng ròng hay có trộn bạc? Làm sao biết mà không phá nó?",
    "Theo giai thoại, lời giải đến ngay trong bồn tắm.",
    "Vì sao nước tràn lại cho biết vàng có bị pha bạc?",
  ],
  can: [
    "Vương miện nặng đúng số vàng đã đưa, nên cân không thấy gì.",
    "Lấy bớt vàng, thêm bạc cho đủ cân, thì cân không đổi.",
    "Bạc nhẹ hơn vàng: cùng cân nặng, bạc chiếm nhiều chỗ hơn.",
    "Đo xem nó chiếm bao nhiêu chỗ, so với vàng ròng cùng cân.",
  ],
  nuoc: [
    "Nhúng vào nước, vật chiếm bao nhiêu chỗ thì đẩy ra bấy nhiêu nước.",
    "Hai khối cùng cân: một vàng, một bạc, nhúng vào bình đầy nước.",
    "Tràn nhiều hơn khối vàng nghĩa là có bạc: thợ gian lận.",
  ],
  cong: [
    "Khối lượng riêng (g mỗi cm³): vàng 19,3, bạc 10,5.",
    "Thể tích = khối lượng ÷ khối lượng riêng.",
    "Ví dụ nặng 1 000 g, vàng ròng: 1 000 ÷ 19,3 ≈ 52 cm³.",
    "Giả sử 30% bạc: 700 ÷ 19,3 + 300 ÷ 10,5.",
    "≈ 65 cm³, lớn hơn 13 cm³.",
    "13 ml nước: chậu rộng 20 cm, nước chỉ chênh 0,4 mm.",
  ],
  gal: [
    "1586: Ga-li-lê gọi cách tràn nước là thô.",
    "Cân trong nước: vật nhẹ đi đúng bằng nước nó đẩy ra.",
    "Trong nước, nó nhẹ hơn khối vàng khoảng 13 g: cân thấy được.",
  ],
  nay: [
    "Kim hoàn cân trong không khí rồi trong nước để biết đó là chất gì.",
    "Tàu sắt vẫn nổi vì thân rỗng đẩy ra nước nặng bằng cả tàu.",
    "Chuyện bồn tắm chép lại sau 200 năm, nhưng ý khoa học vẫn đúng.",
  ],
};

export type Beat = {text: string; start: number; dur: number};
export type SceneTl = {id: SceneId; start: number; dur: number; beats: Beat[]; bs: number[]};
const ORDER: SceneId[] = ['hook', 'can', 'nuoc', 'cong', 'gal', 'nay'];

export function timeline(): {scenes: SceneTl[]; total: number; beats: Beat[]} {
  let f = 0;
  let voiceIdx = 0;
  const all: Beat[] = [];
  const scenes: SceneTl[] = ORDER.map((id) => {
    const texts = id === 'nay' ? [...TEXT_C[id], ''] : TEXT_C[id];
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
