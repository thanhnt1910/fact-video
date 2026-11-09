import {FPS} from '../lib/theme';
import {SceneTl, SceneId, timeline} from './content';

// Hiệu ứng âm thanh thưa, bám các chuyển động chính. t: giây; pan -1..1; v: âm lượng.
export type Ev = {t: number; k: string; pan?: number; v?: number; d?: number};

export function sfxEvents(): {events: Ev[]; total: number} {
  const tl = timeline();
  const ev: Ev[] = [];
  const S = (id: SceneId) => tl.scenes.find((s) => s.id === id) as SceneTl;
  const T = (s: SceneTl, bi: number | null, off: number) => (s.start + (bi === null ? 0 : s.bs[bi])) / FPS + off;
  const add = (t: number, k: string, pan = 0, v = 1, d = 0) => ev.push({t, k, pan, v, d});

  const h = S('hook');
  add(T(h, null, 0.1), 'whoosh', 0, 0.5);
  add(T(h, 0, 1.8), 'bad', -0.6, 0.5);
  add(T(h, 1, 0.3), 'pop', 0, 0.8);

  const p = S('problem');
  add(T(p, null, 0.2), 'question', 0, 0.7);
  for (let t = 1.0; t < 3.6; t += 0.55) add(T(p, null, t), 'step', 0.5, 0.45);

  const c = S('clue');
  add(T(c, 0, 1.0), 'shimmer', 0.3, 0.5);
  add(T(c, 1, 0.4), 'whoosh', 0, 0.4);
  add(T(c, 1, 2.0), 'tick', 0, 0.5);

  const i = S('idea');
  add(T(i, 0, 0.5), 'whooshUp', 0, 0.4);
  add(T(i, 0, 2.2), 'swing', 0, 0.5);
  add(T(i, 1, 0.6), 'chime', 0, 0.6);

  const k = S('calc');
  for (let t = 0.6; t < 3.0; t += 0.42) add(T(k, 0, t), 'step', -0.2, 0.4);
  add(T(k, 0, 3.4), 'pop', 0, 0.7);
  add(T(k, 1, 0.5), 'tick', 0, 0.5);
  add(T(k, 1, 3.4), 'success', 0, 0.6);

  const m = S('compare');
  add(T(m, 0, 0.5), 'whoosh', 0, 0.4);
  add(T(m, 0, 2.6), 'thud', 0, 0.5);
  add(T(m, 1, 0.5), 'whoosh', 0, 0.4);
  add(T(m, 1, 1.6), 'lock', 0, 0.5);

  const d = S('modern');
  add(T(d, 0, 0.6), 'whoosh', 0, 0.4);
  add(T(d, 0, 3.0), 'tick', 0.3, 0.5);
  add(T(d, 1, 0.8), 'chime', 0, 0.6);

  const o = S('outro');
  add(T(o, 0, 0.3), 'whooshDown', 0, 0.4);
  add(T(o, 0, 4.0), 'success', 0, 0.6);
  add(T(o, 1, 0.3), 'shimmer', 0, 0.6);

  return {events: ev.sort((a, b) => a.t - b.t), total: tl.total / FPS};
}
