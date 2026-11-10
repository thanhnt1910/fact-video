import {FPS} from '../lib/theme';
import {SceneTl, SceneId, timeline} from './content';

// Hiệu ứng âm thanh thưa cho video 4 (kinh độ). t: giây; pan -1..1; v: âm lượng.
export type Ev = {t: number; k: string; pan?: number; v?: number; d?: number};

export function sfxEvents(): {events: Ev[]; total: number} {
  const tl = timeline();
  const ev: Ev[] = [];
  const S = (id: SceneId) => tl.scenes.find((s) => s.id === id) as SceneTl;
  const T = (s: SceneTl, bi: number, off: number) => (s.start + s.bs[bi]) / FPS + off;
  const add = (t: number, k: string, pan = 0, v = 0.5) => ev.push({t, k, pan, v, d: 0});

  const h = S('hook');
  add(T(h, 0, 0.8), 'chime', 0, 0.5);
  add(T(h, 0, 3.0), 'question', 0.3, 0.6);
  add(T(h, 1, 1.0), 'pop', 0, 0.5);
  add(T(h, 2, 1.0), 'whoosh', 0, 0.4);
  add(T(h, 2, 3.2), 'question', 0.3, 0.6);

  const g = S('globe');
  add(T(g, 0, 1.0), 'pop', 0, 0.5);
  add(T(g, 1, 1.0), 'whoosh', 0, 0.4);
  add(T(g, 1, 2.6), 'tick', 0, 0.5);
  add(T(g, 1, 4.6), 'chime', 0, 0.5);
  add(T(g, 2, 1.0), 'tick', 0, 0.5);
  add(T(g, 2, 3.0), 'tick', 0, 0.5);
  add(T(g, 2, 5.4), 'chime', 0, 0.5);
  add(T(g, 3, 1.0), 'swing', 0, 0.5);
  add(T(g, 3, 3.0), 'chime', 0, 0.5);

  const w = S('wreck');
  add(T(w, 0, 0.8), 'whooshDown', 0, 0.4);
  add(T(w, 1, 1.0), 'tick', 0, 0.5);
  add(T(w, 1, 3.4), 'bad', 0, 0.5);
  add(T(w, 2, 2.6), 'thud', 0, 0.6);

  const c = S('clock');
  add(T(c, 0, 1.0), 'swing', 0, 0.5);
  add(T(c, 0, 3.2), 'bad', 0, 0.5);
  add(T(c, 1, 1.0), 'chime', 0, 0.5);
  add(T(c, 1, 3.0), 'tick', 0, 0.5);
  add(T(c, 2, 1.0), 'pop', 0, 0.5);

  const r = S('harrison');
  add(T(r, 0, 0.8), 'pop', 0, 0.5);
  add(T(r, 0, 2.4), 'pop', 0, 0.5);
  add(T(r, 1, 1.0), 'whoosh', 0, 0.4);
  add(T(r, 2, 1.0), 'tick', 0, 0.5);
  add(T(r, 2, 3.4), 'success', 0, 0.5);

  const e = S('error');
  add(T(e, 0, 1.0), 'tick', 0, 0.5);
  add(T(e, 0, 3.2), 'chime', 0, 0.5);
  add(T(e, 1, 1.0), 'pop', 0, 0.5);
  add(T(e, 1, 3.4), 'success', 0, 0.5);
  add(T(e, 2, 1.0), 'bad', 0, 0.5);
  add(T(e, 2, 3.6), 'chime', 0, 0.5);

  const n = S('now');
  add(T(n, 0, 1.0), 'whoosh', 0, 0.4);
  add(T(n, 0, 3.0), 'tick', 0, 0.5);
  add(T(n, 1, 1.0), 'pop', 0, 0.5);
  add(T(n, 1, 4.0), 'chime', 0, 0.5);
  add(T(n, 2, 2.0), 'success', 0, 0.5);
  add(T(n, 3, 0.3), 'shimmer', 0, 0.6);

  return {events: ev.sort((a, b) => a.t - b.t), total: tl.total / FPS};
}
