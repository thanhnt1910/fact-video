import {FPS} from '../lib/theme';
import {SceneTl, SceneId, timeline} from './content';

// Hiệu ứng âm thanh thưa, bám các chuyển động chính. t: giây; pan -1..1; v: âm lượng.
export type Ev = {t: number; k: string; pan?: number; v?: number; d?: number};

export function sfxEvents(): {events: Ev[]; total: number} {
  const tl = timeline();
  const ev: Ev[] = [];
  const S = (id: SceneId) => tl.scenes.find((s) => s.id === id) as SceneTl;
  const T = (s: SceneTl, bi: number | null, off: number) => (s.start + (bi === null ? 0 : s.bs[bi])) / FPS + off;
  const add = (t: number, k: string, pan = 0, v = 1) => ev.push({t, k, pan, v, d: 0});

  const h = S('hook');
  add(T(h, null, 0.2), 'whoosh', 0, 0.45);
  add(T(h, 0, 1.0), 'question', 0.3, 0.6);
  add(T(h, 1, 1.1), 'bad', -0.4, 0.5);
  add(T(h, 1, 2.0), 'bad', 0.4, 0.5);
  add(T(h, 1, 3.4), 'chime', 0.5, 0.6);

  const p = S('problem');
  for (let t = 0.8; t < 3.4; t += 0.55) add(T(p, null, t), 'step', 0.5, 0.4);
  add(T(p, null, 4.4), 'question', 0.4, 0.6);

  const c = S('clue');
  add(T(c, 0, 2.0), 'pop', 0, 0.6);
  add(T(c, 1, 0.8), 'shimmer', 0.3, 0.5);
  add(T(c, 2, 0.6), 'whoosh', 0, 0.4);
  add(T(c, 2, 2.6), 'tick', 0, 0.5);
  add(T(c, 3, 2.4), 'question', 0.3, 0.6);

  const o = S('orange');
  add(T(o, 0, 0.5), 'pop', 0, 0.6);
  add(T(o, 0, 3.4), 'tick', 0, 0.5);
  add(T(o, 1, 1.4), 'swing', 0, 0.5);
  add(T(o, 2, 0.5), 'whooshDown', 0, 0.4);
  add(T(o, 3, 0.4), 'whooshUp', 0, 0.4);
  add(T(o, 3, 3.0), 'chime', 0, 0.6);

  const k = S('calc');
  add(T(k, 0, 1.6), 'tick', 0, 0.5);
  add(T(k, 1, 1.4), 'pop', 0, 0.5);
  add(T(k, 2, 1.0), 'tick', 0, 0.5);
  for (let t = 1.0; t < 3.0; t += 0.4) add(T(k, 3, t), 'step', 0, 0.35);
  add(T(k, 4, 3.6), 'success', 0, 0.6);

  const m = S('compare');
  add(T(m, 0, 0.8), 'whoosh', 0, 0.4);
  add(T(m, 0, 3.2), 'thud', 0, 0.5);
  add(T(m, 0, 5.0), 'chime', -0.5, 0.5);
  add(T(m, 1, 1.0), 'lock', 0, 0.5);

  const d = S('modern');
  add(T(d, 0, 0.8), 'pop', 0, 0.5);
  add(T(d, 1, 0.8), 'whoosh', 0, 0.4);
  add(T(d, 1, 3.4), 'tick', 0.3, 0.5);
  add(T(d, 2, 0.8), 'chime', 0, 0.6);

  const e = S('outro');
  add(T(e, 0, 0.3), 'whooshDown', 0, 0.4);
  add(T(e, 0, 4.0), 'success', 0, 0.6);
  add(T(e, 1, 0.3), 'shimmer', 0, 0.6);

  return {events: ev.sort((a, b) => a.t - b.t), total: tl.total / FPS};
}
