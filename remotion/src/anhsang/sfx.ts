import {FPS} from '../lib/theme';
import {SceneTl, SceneId, timeline} from './content';

// Hiệu ứng âm thanh thưa cho video tốc độ ánh sáng. t: giây; pan -1..1; v: âm lượng.
export type Ev = {t: number; k: string; pan?: number; v?: number; d?: number};

export function sfxEvents(): {events: Ev[]; total: number} {
  const tl = timeline();
  const ev: Ev[] = [];
  const S = (id: SceneId) => tl.scenes.find((s) => s.id === id) as SceneTl;
  const T = (s: SceneTl, bi: number | null, off: number) => (s.start + (bi === null ? 0 : s.bs[bi])) / FPS + off;
  const add = (t: number, k: string, pan = 0, v = 1) => ev.push({t, k, pan, v, d: 0});

  const h = S('hook');
  add(T(h, 0, 1.5), 'whooshDown', 0, 0.5);
  add(T(h, 0, 4.4), 'chime', 0, 0.5);
  add(T(h, 1, 1.2), 'tick', -0.3, 0.6);
  add(T(h, 1, 3.2), 'pop', 0, 0.5);
  add(T(h, 2, 1.0), 'whoosh', 0, 0.4);
  add(T(h, 2, 3.0), 'question', 0.3, 0.6);

  const l = S('lantern');
  add(T(l, 0, 0.8), 'pop', 0, 0.5);
  add(T(l, 1, 1.0), 'pop', -0.3, 0.5);
  add(T(l, 2, 0.6), 'tick', -0.4, 0.5);
  add(T(l, 2, 1.7), 'tick', 0.4, 0.5);
  add(T(l, 3, 1.0), 'bad', 0, 0.5);
  add(T(l, 4, 1.2), 'swing', 0, 0.5);

  const i = S('io');
  add(T(i, 0, 1.0), 'pop', 0, 0.5);
  add(T(i, 1, 1.0), 'tick', 0, 0.5);
  for (let n = 0; n < 2; n++) add(T(i, 2, 1.0 + n * 2.1), 'tick', 0.3, 0.5);
  add(T(i, 3, 3.2), 'swing', 0, 0.5);
  add(T(i, 4, 2.0), 'thud', 0, 0.5);
  add(T(i, 5, 1.8), 'pop', 0, 0.5);
  add(T(i, 6, 2.2), 'whoosh', 0, 0.4);
  add(T(i, 7, 2.0), 'chime', 0, 0.6);

  const r = S('romer');
  add(T(r, 0, 2.0), 'thud', 0, 0.5);
  add(T(r, 1, 1.4), 'bad', 0, 0.5);
  add(T(r, 2, 2.0), 'chime', 0, 0.5);

  const d = S('divide');
  add(T(d, 0, 1.0), 'pop', 0, 0.5);
  add(T(d, 1, 1.0), 'tick', 0, 0.5);
  add(T(d, 2, 1.0), 'chime', 0, 0.5);
  add(T(d, 3, 1.0), 'whoosh', 0, 0.4);
  add(T(d, 4, 0.8), 'swing', 0, 0.5);

  const w = S('wheel');
  add(T(w, 0, 0.6), 'pop', 0, 0.5);
  add(T(w, 1, 1.0), 'tick', 0, 0.5);
  add(T(w, 2, 2.0), 'tick', 0, 0.5);
  add(T(w, 3, 1.0), 'swing', 0, 0.5);
  add(T(w, 3, 2.6), 'bad', 0, 0.5);
  add(T(w, 4, 1.0), 'whoosh', 0, 0.4);
  add(T(w, 5, 1.0), 'pop', 0, 0.5);
  add(T(w, 6, 3.0), 'chime', 0, 0.6);

  const e = S('outro');
  add(T(e, 0, 0.8), 'chime', 0, 0.6);
  add(T(e, 1, 1.0), 'whoosh', 0, 0.4);
  add(T(e, 2, 1.5), 'success', 0, 0.5);
  add(T(e, 3, 0.3), 'shimmer', 0, 0.6);

  return {events: ev.sort((a, b) => a.t - b.t), total: tl.total / FPS};
}
