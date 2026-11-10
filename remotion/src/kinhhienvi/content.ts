import {FPS} from '../lib/theme';
import {beatSeconds} from '../thales/content';
import ledaDur from './leda_dur.json';

// Video khoa học số 7 (dọc 1080x1920, tiếng Việt): Làm sao đếm được thứ mắt không thấy? Kịch bản: ke-hoach/khoa-hoc-video-7-kinh-hien-vi-kich-ban.md
// Văn bản ở đây là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-kinhhienvi.json.

export type SceneId = 'hook' | 'kinh' | 'lp' | 'nho' | 'giot' | 'nay';
export const END_C = 3.5;

export const TEXT_C: Record<SceneId, string[]> = {
  hook: [
    "Giọt nước có 1 triệu sinh vật. Làm sao đếm thứ không thấy?",
    "Người đếm là một người bán vải ở Hà Lan.",
    "Vì sao đo được? Ông dùng hạt cát.",
  ],
  kinh: [
    "Kính một thấu kính, phóng to tới 275 lần.",
    "Thấy chưa đủ: phải biết chúng to bao nhiêu.",
    "So với hạt cát, hạt kê, sợi tóc.",
  ],
  lp: [
    "Hạt cát dài gấp 12 lần con vật.",
    "Dài gấp 12 thì thể tích không gấp 12.",
    "12 × 12 × 12 = 1 728.",
    "Hạt cát lớn gấp 1 728 lần con vật.",
  ],
  nho: [
    "Loại dài bằng 1/4: 4 × 4 × 4 = 64.",
    "1 728 × 64 = 110 592 con trong một hạt cát.",
    "Loại dài bằng 1/10: nhân thêm 1 000, ra hơn 110 triệu con.",
    "100 hồng cầu dài bằng hạt cát: 100 × 100 × 100 = 1 triệu.",
  ],
  giot: [
    "1677, giọt nước: tính ra 2 730 000, báo 1 triệu.",
    "Hội Hoàng gia kiểm tra lại rồi mới công nhận.",
    "Ông giữ kín cách mài kính tốt nhất.",
    "Ước chừng bằng mắt, nhưng gần số đo hiện đại.",
  ],
  nay: [
    "Hồng cầu rộng khoảng 7 µm, tức 0,007 mm.",
    "100 × 7 µm = 0,7 mm: đúng cỡ hạt cát thô.",
    "1 ml máu có 4–6 tỉ hồng cầu.",
    "So với vật quen, rồi nhân lập phương.",
  ],
};

export type Beat = {text: string; start: number; dur: number};
export type SceneTl = {id: SceneId; start: number; dur: number; beats: Beat[]; bs: number[]};
const ORDER: SceneId[] = ['hook', 'kinh', 'lp', 'nho', 'giot', 'nay'];

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
