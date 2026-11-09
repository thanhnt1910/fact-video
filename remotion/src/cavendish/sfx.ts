import {FPS} from '../lib/theme';
import {SceneTl, SceneId, timeline} from './content';

// Hiệu ứng âm thanh thưa cho video Cavendish. t: giây; pan -1..1; v: âm lượng.
export type Ev = {t: number; k: string; pan?: number; v?: number; d?: number};

export function sfxEvents(): {events: Ev[]; total: number} {
  const tl = timeline();
  const ev: Ev[] = [];
  const S = (id: SceneId) => tl.scenes.find((s) => s.id === id) as SceneTl;
  const T = (s: SceneTl, bi: number | null, off: number) => (s.start + (bi === null ? 0 : s.bs[bi])) / FPS + off;
  const add = (t: number, k: string, pan = 0, v = 1) => ev.push({t, k, pan, v, d: 0});

  const h = S('hook');
  add(T(h, null, 0.2), 'whoosh', 0, 0.45);
  add(T(h, 0, 2.6), 'chime', 0, 0.5);
  add(T(h, 1, 1.0), 'question', 0.3, 0.6);
  add(T(h, 1, 2.0), 'bad', -0.4, 0.5);

  const m = S('mount');
  add(T(m, 0, 0.9), 'pop', 0, 0.5);
  add(T(m, 1, 0.8), 'tick', -0.3, 0.5);
  add(T(m, 2, 1.8), 'swing', -0.2, 0.5);
  add(T(m, 3, 0.7), 'pop', 0, 0.5);
  add(T(m, 4, 0.9), 'question', 0.3, 0.6);
  add(T(m, 5, 0.8), 'whoosh', 0, 0.4);
  add(T(m, 5, 3.4), 'thud', 0, 0.5);

  const i = S('idea');
  add(T(i, 0, 1.2), 'whooshDown', 0, 0.4);
  add(T(i, 0, 2.2), 'pop', 0.3, 0.5);
  add(T(i, 1, 0.6), 'pop', -0.3, 0.5);
  add(T(i, 2, 1.4), 'chime', 0.3, 0.6);

  const d = S('device');
  add(T(d, 0, 0.5), 'pop', 0, 0.5);
  add(T(d, 1, 0.5), 'whoosh', 0, 0.4);
  add(T(d, 2, 1.2), 'swing', 0, 0.5);
  add(T(d, 3, 1.0), 'tick', 0, 0.5);
  add(T(d, 4, 0.9), 'whoosh', 0, 0.4);
  add(T(d, 5, 1.0), 'thud', 0, 0.5);
  add(T(d, 5, 2.4), 'pop', 0.4, 0.5);
  add(T(d, 6, 2.0), 'swing', 0, 0.5);
  for (let t = 3.6; t < 5.0; t += 0.25) add(T(d, 6, t), 'tick', -0.4, 0.3);

  const k = S('calc');
  add(T(k, 0, 1.0), 'pop', 0, 0.5);
  add(T(k, 0, 3.4), 'tick', 0.3, 0.5);
  for (let n = 0; n < 3; n++) add(T(k, 1, 0.6 + n * 1.2), 'tick', 0, 0.5);
  add(T(k, 1, 4.6), 'chime', 0, 0.5);
  add(T(k, 2, 1.0), 'swing', 0, 0.5);
  add(T(k, 2, 3.2), 'thud', 0, 0.5);
  add(T(k, 3, 2.0), 'question', 0, 0.6);
  add(T(k, 4, 1.0), 'whoosh', 0, 0.4);
  add(T(k, 4, 4.2), 'success', 0, 0.6);

  const e = S('outro');
  add(T(e, 0, 0.3), 'whooshDown', 0, 0.4);
  add(T(e, 0, 3.0), 'success', 0, 0.5);
  add(T(e, 1, 0.3), 'shimmer', 0, 0.6);

  return {events: ev.sort((a, b) => a.t - b.t), total: tl.total / FPS};
}
