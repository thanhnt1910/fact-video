import {FPS} from '../lib/theme';
import {beatSeconds} from '../thales/content';

// Bộ dựng chung cho các video khoa học 8–12: mỗi câu đọc là một "khung" (Panel), nhóm câu thành cảnh.
export type Beat = {text: string; start: number; dur: number};
export type SceneTl = {first: number; start: number; dur: number; beats: Beat[]; bs: number[]};
export type Tl = {scenes: SceneTl[]; total: number; beats: Beat[]};

export const END_C = 3.5;

export function buildTimeline(texts: string[], sizes: number[], ledaDur: number[]): Tl {
  let f = 0;
  let idx = 0;
  const all: Beat[] = [];
  const scenes: SceneTl[] = sizes.map((n, si) => {
    const tx = texts.slice(idx, idx + n);
    const first = idx;
    const list = si === sizes.length - 1 ? [...tx, ''] : tx;
    const beats: Beat[] = list.map((text, j) => {
      let sec = text ? beatSeconds('vi', text) : END_C;
      const d = ledaDur[first + j];
      if (text && d !== undefined) sec = Math.max(d + 0.5, 2.4);
      const dur = Math.round(sec * FPS);
      const b = {text, start: f, dur};
      f += dur;
      all.push(b);
      return b;
    });
    idx += n;
    const start = beats[0].start;
    return {first, start, dur: f - start, beats, bs: beats.map((b) => b.start - start)};
  });
  return {scenes, total: f, beats: all};
}


// Hiệu ứng âm thanh thưa: mỗi nhịp một tiếng mở, nhịp dài thêm một tiếng nhấn.
export type Ev = {t: number; k: string; pan?: number; v?: number; d?: number};
export function sfxFor(tl: Tl): {events: Ev[]; total: number} {
  const ev: Ev[] = [];
  const open = ['pop', 'whoosh', 'tick', 'swing', 'pop', 'whooshDown'];
  tl.scenes.forEach((s, si) => {
    s.beats.forEach((b, bi) => {
      const t0 = (s.start + s.bs[bi]) / FPS;
      if (!b.text) { ev.push({t: t0 + 0.3, k: 'shimmer', pan: 0, v: 0.6, d: 0}); return; }
      ev.push({t: t0 + 0.9, k: open[(si + bi) % open.length], pan: 0, v: 0.45, d: 0});
      if (b.dur / FPS > 6) ev.push({t: t0 + b.dur / FPS - 2.2, k: /\d/.test(b.text) ? 'chime' : 'tick', pan: 0, v: 0.5, d: 0});
    });
  });
  ev.push({t: 0.8, k: 'chime', pan: 0, v: 0.5, d: 0});
  return {events: ev.sort((a, b) => a.t - b.t), total: tl.total / FPS};
}
