import {FPS} from '../lib/theme';
import {SceneTl3, timeline3} from './content';

// Danh sách hiệu ứng âm thanh, tính từ cùng mốc thời gian với hình (xem scenes.tsx).
// t: giây; pan: -1 (trái) .. 1 (phải); v: âm lượng 0..1.
export type Ev = {t: number; k: string; pan?: number; v?: number; d?: number};

const panOf = (x: number) => Math.max(-0.9, Math.min(0.9, (x / 1920) * 2 - 1));
const lerp = (a: number, b: number, k: number) => a + (b - a) * k;
const eio = (x: number) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);

export function sfxEvents(): {events: Ev[]; total: number} {
  const tl = timeline3();
  const ev: Ev[] = [];
  const S = (id: string) => tl.scenes.find((s) => s.id === id) as SceneTl3;
  const T = (s: SceneTl3, bi: number | null, off: number) => (s.start + (bi === null ? 0 : s.bs[bi])) / FPS + off;
  const add = (t: number, k: string, pan = 0, v = 1, d = 0) => ev.push({t, k, pan, v, d});
  // bước chân người: từ t0 đến t1, mỗi `gap` giây, x chạy từ xa tới xb
  const steps = (t0: number, t1: number, gap: number, xa: number, xb: number, v = 0.9, k = 'step', ease = false) => {
    for (let t = t0; t < t1; t += gap) {
      const p = (t - t0) / (t1 - t0);
      add(t, k, panOf(lerp(xa, xb, ease ? eio(p) : p)), v);
    }
  };

  // ---- 1. Mở đầu
  const h = S('hook');
  add(T(h, null, 0.0), 'whoosh', 0, 0.5);
  add(T(h, null, 0.4), 'scratch', 0, 0.7, 4.2);
  const camels = [0, 330, 700];
  camels.forEach((off, i) => {
    const t0 = Math.max(0, (2150 + off - 1950) / 170);
    const t1 = (2150 + off + 80) / 170;
    for (let t = t0; t < Math.min(t1, h.dur / FPS); t += 0.52) add(t + i * 0.13, 'hoof', panOf(2150 + off - 170 * t), 0.5);
    for (let t = t0 + 0.7 + i * 0.5; t < Math.min(t1, h.dur / FPS); t += 1.9) add(t, 'bell', panOf(2150 + off - 170 * t), 0.35);
  });
  steps(T(h, 1, -5.0), T(h, 1, -1.4), 0.308, 1900, 1520, 0.8);
  add(T(h, null, 5.2), 'shimmer', 0, 0.5);
  add(T(h, 2, 0.2), 'pop', 0.5, 0.9);
  add(T(h, 2, 1.2), 'question', 0.5, 0.8);

  // ---- 2. Dụng cụ thời đó
  const tools = S('tools');
  add(T(tools, 0, 0.8), 'water', 0, 0.9, 5.6);
  add(T(tools, 1, 0.2), 'rope', -0.3, 0.8);
  const w0 = T(tools, 1, 0.8);
  const w1 = T(tools, 1, 6.6);
  steps(w0, w1, 0.5, 336, 946, 0.6, 'step', true);
  for (let k = 360; k < 930; k += 36) {
    const frac = (k + 14 - 336) / (946 - 336);
    // tìm thời điểm eio(p) = frac
    let lo = 0;
    let hi = 1;
    for (let i = 0; i < 24; i++) {
      const mid = (lo + hi) / 2;
      if (eio(mid) < frac) lo = mid;
      else hi = mid;
    }
    add(w0 + lo * (w1 - w0), 'tick', panOf(k), 0.35);
  }
  add(T(tools, 1, 6.8), 'pop', -0.2, 0.9);
  add(T(tools, 1, 8.0), 'success', 0.1, 0.55);
  add(T(tools, 2, 0.4), 'question', -0.6, 0.9);

  // ---- 3. Seked
  const sk = S('seked');
  add(T(sk, 0, 1.0), 'pop', 0.4, 0.8);
  add(T(sk, 0, 3.0), 'pop', 0.4, 0.8);
  add(T(sk, 1, 2.0), 'pop', 0.6, 0.8);
  add(T(sk, 1, 3.2), 'success', 0.6, 0.55);
  add(T(sk, 2, 1.0), 'pop', 0.1, 0.8);
  add(T(sk, 2, 5.0), 'bad', 0.1, 0.7);
  add(T(sk, 3, 5.0), 'question', 0.5, 0.8);

  // ---- 5. Ý tưởng
  const id = S('idea');
  add(T(id, 0, 1.4), 'pop', 0.3, 0.8);
  add(T(id, 0, 1.9), 'bad', 0.3, 0.6);
  add(T(id, 0, 3.0), 'pop', 0.4, 0.8);
  add(T(id, 0, 3.5), 'bad', 0.4, 0.6);
  add(T(id, 0, 4.6), 'pop', 0.6, 0.8);
  add(T(id, 0, 5.1), 'success', 0.6, 0.5);
  add(T(id, 1, 1.0), 'chime', 0.5, 1.0);
  add(T(id, 1, 1.0), 'whooshUp', 0.5, 0.5);
  add(T(id, 1, 2.6), 'shimmer', -0.5, 0.6);
  add(T(id, 2, 0.8), 'swing', -0.2, 0.9, 2.8);
  add(T(id, 2, 3.4), 'thud', -0.1, 0.9);
  add(T(id, 2, 3.6), 'success', 0, 0.8);
  add(T(id, 2, 3.8), 'whoosh', -0.3, 0.5);

  // ---- 6. Mặt Trời và cái bóng
  const su = S('sun');
  add(T(su, null, 0.2), 'shimmer', -0.5, 0.6);
  add(T(su, 1, 0.2), 'whoosh', 0, 0.6);
  add(T(su, 1, 1.2), 'whoosh', 0.3, 0.5);
  add(T(su, 1, 3.2), 'pop', 0.7, 0.8);
  add(T(su, 2, 0.4), 'whooshUp', -0.4, 0.7, 5);
  for (let t = T(su, 2, 0.4); t < T(su, 3, -0.4); t += 0.3) add(t, 'tick', -0.8, 0.4);
  add(T(su, 3, 0.4), 'pop', 0.6, 0.8);
  add(T(su, 3, 0.8), 'pop', 0.6, 0.7);
  add(T(su, 3, 2.4), 'chime', 0.3, 0.8);

  // ---- 7. Lúc bóng bằng người
  const eq = S('equal');
  add(T(eq, 1, 0.2), 'pop', 0.1, 0.8);
  add(T(eq, 1, 0.3), 'pop', 0.7, 0.8);
  add(T(eq, 1, 1.8), 'pop', -0.6, 0.8);
  add(T(eq, 1, 3.6), 'chime', 0.2, 0.8);
  steps(T(eq, 2, 0.4), T(eq, 2, 5.4), 0.308, 1520, 1020, 0.8);

  // ---- 8. Nửa cạnh đáy
  const hf = S('half');
  steps(T(hf, null, 0.2), T(hf, null, 1.4), 0.308, 1020, 938, 0.8);
  add(T(hf, null, 1.2), 'whoosh', 0.1, 0.5);
  add(T(hf, 0, 1.8), 'whooshUp', -0.3, 0.6);
  add(T(hf, 0, 3.0), 'pop', -0.7, 0.8);
  add(T(hf, 1, -0.2), 'pop', 0.4, 0.9);
  add(T(hf, 1, 1.4), 'whoosh', 0.3, 0.6);
  add(T(hf, 2, 0.2), 'pop', -0.3, 0.8);
  add(T(hf, 2, 1.4), 'pop', 0, 0.8);
  add(T(hf, 2, 2.6), 'chime', 0.3, 0.8);

  // ---- 9. Mẹo cây gậy
  const st = S('stick');
  add(T(st, null, 0.4), 'whooshDown', 0, 0.6, 3);
  steps(T(st, 1, 0.3), T(st, 1, 3.0), 0.308, 938, 1210, 0.8);
  add(T(st, 1, 3.0), 'thud', 0.2, 0.9);
  add(T(st, 1, 3.0), 'wood', 0.2, 0.9);
  add(T(st, 1, 3.5), 'whoosh', 0.3, 0.5);
  steps(T(st, 1, 3.9), T(st, 1, 7.2), 0.308, 1210, 1520, 0.8);
  add(T(st, 2, 0.3), 'whoosh', 0, 0.6);
  add(T(st, 2, 0.5), 'whoosh', 0.3, 0.5);
  add(T(st, 2, 2.2), 'pop', 0.4, 0.8);
  add(T(st, 2, 2.4), 'pop', 0.6, 0.8);
  add(T(st, 2, 2.8), 'chime', 0.2, 0.7);
  add(T(st, 3, 0.1), 'whoosh', -0.2, 0.4);
  add(T(st, 3, 1.6), 'zoom', 0, 0.9, 3.4);
  add(T(st, 3, 5.0), 'lock', 0, 0.9);
  add(T(st, 3, 4.6), 'chime', 0, 0.8);
  for (let i = 0; i < 4; i++) add(T(st, 4, 1.0 + i * 0.25), 'pop', -0.4 + i * 0.3, 0.7);
  add(T(st, 4, 2.8), 'success', 0.1, 0.8);

  // ---- 10. Con số
  const nu = S('numbers');
  add(T(nu, null, 0.6), 'pop', 0.3, 0.8);
  add(T(nu, null, 1.4), 'pop', 0.3, 0.8);
  add(T(nu, 1, 0.4), 'pop', 0.2, 0.8);
  add(T(nu, 2, 0.4), 'pop', -0.2, 0.8);
  add(T(nu, 2, 2.6), 'pop', 0.2, 0.8);
  add(T(nu, 2, 4.8), 'success', 0.1, 0.9);
  add(T(nu, 2, 5.0), 'pop', -0.7, 0.8);
  add(T(nu, 3, 0.4), 'pop', 0.3, 0.7);

  // ---- 11. Ngày nay
  const mo = S('modern');
  add(T(mo, null, 0.0), 'whoosh', 0, 0.7);
  add(T(mo, null, 0.2), 'pop', -0.7, 0.8);
  add(T(mo, 1, 0.2), 'pop', -0.1, 0.8);
  add(T(mo, 1, 0.8), 'servo', -0.3, 0.8, 2.6);
  add(T(mo, 1, 3.2), 'whoosh', 0.2, 0.6);
  add(T(mo, 1, 3.6), 'pop', -0.2, 0.8);
  add(T(mo, 2, 0.2), 'pop', 0.4, 0.8);
  add(T(mo, 2, 1.4), 'chime', 0, 0.8);

  // ---- 12. Everest
  const ev2 = S('everest');
  add(T(ev2, 0, 0.6), 'servo', -0.7, 0.7, 2.6);
  add(T(ev2, 0, 3.0), 'pop', 0, 0.8);
  for (let i = 0; i < 3; i++) add(T(ev2, 1, 0.6 + i), 'pop', -0.8 + i * 0.1, 0.7);
  add(T(ev2, 1, 3.8), 'pop', -0.8, 0.7);
  add(T(ev2, 2, 0.8), 'chime', 0, 0.8);
  add(T(ev2, 3, 0.8), 'success', 0, 0.8);

  // ---- 13. Đời thường
  const ed = S('everyday');
  add(T(ed, null, 0.2), 'whooshUp', -0.5, 0.5);
  add(T(ed, null, 0.2), 'shimmer', -0.8, 0.5);
  add(T(ed, 0, 2.0), 'whoosh', 0, 0.5);
  add(T(ed, 0, 3.6), 'whoosh', 0.2, 0.5);
  add(T(ed, 0, 4.8), 'pop', -0.3, 0.8);
  add(T(ed, 0, 6.0), 'chime', 0.2, 0.8);
  add(T(ed, 1, 1.0), 'zoom', 0, 0.9, 4.2);
  add(T(ed, 1, 5.2), 'lock', 0, 0.8);
  add(T(ed, 2, 0.6), 'chime', 0, 0.9);

  // ---- 14. Kết
  const ou = S('outro');
  [0, 330, 700].forEach((off, i) => {
    for (let t = 0; t < ou.dur / FPS; t += 0.52) {
      const x = -250 + 190 * t - off;
      if (x > -100 && x < 2000) add(T(ou, null, t) + i * 0.13, 'hoof', panOf(x), 0.45);
    }
    for (let t = 0.8 + i * 0.6; t < ou.dur / FPS; t += 1.9) {
      const x = -250 + 190 * t - off;
      if (x > -100 && x < 2000) add(T(ou, null, t), 'bell', panOf(x), 0.3);
    }
  });
  steps(T(ou, null, 0.4), T(ou, null, 4.4), 0.308, 1520, 1380, 0.7);
  const endStart = T(ou, ou.bs.length - 1, 0);
  add(endStart, 'whoosh', 0, 0.6);
  add(endStart + 0.5, 'success', 0, 0.9);
  add(endStart + 0.9, 'chime', 0, 0.9);

  ev.sort((a, b) => a.t - b.t);
  return {events: ev, total: tl.total / FPS};
}
