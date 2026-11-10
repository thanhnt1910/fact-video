import {FPS} from '../lib/theme';
import {timeline} from './content';

// Hiệu ứng âm thanh thưa: mỗi nhịp một tiếng mở, nhịp dài thêm một tiếng nhấn.
export type Ev = {t: number; k: string; pan?: number; v?: number; d?: number};

export function sfxEvents(): {events: Ev[]; total: number} {
  const tl = timeline();
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
