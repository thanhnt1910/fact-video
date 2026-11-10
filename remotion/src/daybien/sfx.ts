import {FPS} from '../lib/theme';
import {SceneTl, SceneId, timeline} from './content';

// Hiệu ứng âm thanh thưa cho video 5 (đáy biển). t: giây.
export type Ev = {t: number; k: string; pan?: number; v?: number; d?: number};

export function sfxEvents(): {events: Ev[]; total: number} {
  const tl = timeline();
  const ev: Ev[] = [];
  const S = (id: SceneId) => tl.scenes.find((s) => s.id === id) as SceneTl;
  const T = (s: SceneTl, bi: number, off: number) => (s.start + s.bs[bi]) / FPS + off;
  const add = (t: number, k: string, pan = 0, v = 0.5) => ev.push({t, k, pan, v, d: 0});

  const h = S('hook');
  add(T(h, 0, 0.8), 'chime', 0, 0.5);
  add(T(h, 0, 3.0), 'pop', 0, 0.5);
  add(T(h, 1, 1.0), 'whoosh', 0, 0.4);
  add(T(h, 1, 4.0), 'question', 0.3, 0.6);
  add(T(h, 2, 1.0), 'pop', 0, 0.5);

  const c = S('cu');
  add(T(c, 0, 1.0), 'whooshDown', 0, 0.4);
  add(T(c, 0, 3.0), 'tick', 0, 0.5);
  add(T(c, 1, 1.0), 'swing', 0, 0.5);
  add(T(c, 1, 4.0), 'bad', 0, 0.5);
  add(T(c, 2, 1.0), 'tick', 0, 0.5);
  add(T(c, 2, 3.4), 'chime', 0, 0.5);

  const r = S('chal');
  add(T(r, 0, 1.0), 'pop', 0, 0.5);
  add(T(r, 1, 1.0), 'tick', 0, 0.5);
  add(T(r, 1, 3.4), 'chime', 0, 0.5);
  add(T(r, 2, 1.0), 'whooshDown', 0, 0.4);
  add(T(r, 2, 3.4), 'success', 0, 0.5);

  const v = S('vang');
  add(T(v, 0, 0.8), 'chime', 0, 0.5);
  add(T(v, 0, 2.4), 'whoosh', 0, 0.4);
  add(T(v, 1, 1.0), 'pop', 0, 0.5);
  add(T(v, 1, 4.0), 'tick', 0, 0.5);
  add(T(v, 2, 1.0), 'pop', 0, 0.5);
  add(T(v, 2, 3.6), 'chime', 0, 0.5);
  add(T(v, 3, 0.8), 'tick', 0, 0.5);
  add(T(v, 3, 1.6), 'tick', 0, 0.5);
  add(T(v, 3, 2.4), 'chime', 0, 0.5);
  add(T(v, 4, 0.8), 'tick', 0, 0.5);
  add(T(v, 4, 2.4), 'tick', 0, 0.5);
  add(T(v, 4, 4.4), 'success', 0, 0.5);
  add(T(v, 5, 1.0), 'whoosh', 0, 0.4);

  const m = S('meteor');
  add(T(m, 0, 1.0), 'pop', 0, 0.5);
  add(T(m, 1, 1.0), 'swing', 0, 0.5);
  add(T(m, 1, 4.0), 'chime', 0, 0.5);
  add(T(m, 2, 1.0), 'whoosh', 0, 0.4);
  add(T(m, 2, 3.4), 'success', 0, 0.5);

  const n = S('nay');
  add(T(n, 0, 1.0), 'whoosh', 0, 0.4);
  add(T(n, 0, 3.0), 'chime', 0, 0.5);
  add(T(n, 1, 1.0), 'pop', 0, 0.5);
  add(T(n, 1, 4.0), 'chime', 0, 0.5);
  add(T(n, 2, 1.0), 'tick', 0, 0.5);
  add(T(n, 2, 3.4), 'chime', 0, 0.5);
  add(T(n, 3, 1.0), 'swing', 0, 0.5);
  add(T(n, 3, 4.0), 'chime', 0, 0.5);
  add(T(n, 4, 1.0), 'pop', 0, 0.5);
  add(T(n, 4, 3.4), 'success', 0, 0.5);
  add(T(n, 5, 0.3), 'shimmer', 0, 0.6);

  return {events: ev.sort((a, b) => a.t - b.t), total: tl.total / FPS};
}
