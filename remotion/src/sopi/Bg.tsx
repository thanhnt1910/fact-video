import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 18 (số pi): giấy kẻ ô cổ màu xanh đá đậm với vài đường tròn rất mờ.
// Dấu ấn riêng: một đa giác nhỏ ở mép trái tăng dần số cạnh 6 → 12 → 24 → 48 rồi quay lại hình sáu cạnh, lặp lại mỗi 5 giây.
const poly = (cx: number, cy: number, r: number, n: number) =>
  Array.from({length: n}, (_, i) => `${cx + r * Math.cos((i / n) * 2 * Math.PI - Math.PI / 2)},${cy + r * Math.sin((i / n) * 2 * Math.PI - Math.PI / 2)}`).join(' ');
export const SpBackground: React.FC = () => {
  const f = useCurrentFrame();
  const step = Math.floor((f % 150) / 38);
  const n = [6, 12, 24, 48][Math.min(3, step)];
  const t = (f % 150) % 38;
  const o = Math.min(1, t / 8) * 0.85;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <radialGradient id="spG" cx="0.5" cy="0.4" r="0.8">
          <stop offset="0" stopColor="#1f2c3c" />
          <stop offset="1" stopColor="#0f1722" />
        </radialGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#spG)" />
      {Array.from({length: 14}).map((_, i) => (
        <line key={'v' + i} x1={i * 80} y1={0} x2={i * 80} y2={1920} stroke="#8fb4d6" strokeWidth={2} opacity={0.05} />
      ))}
      {Array.from({length: 25}).map((_, i) => (
        <line key={'h' + i} x1={0} y1={i * 80} x2={1080} y2={i * 80} stroke="#8fb4d6" strokeWidth={2} opacity={0.05} />
      ))}
      {[260, 420, 600].map((r, i) => (
        <circle key={i} cx={540} cy={960} r={r} fill="none" stroke="#8fb4d6" strokeWidth={2} opacity={0.07} />
      ))}
      <circle cx={62} cy={470} r={30} fill="none" stroke="#8fb4d6" strokeWidth={2} opacity={0.3} />
      <polygon points={poly(62, 470, 30, n)} fill="none" stroke="#f2c14e" strokeWidth={4} strokeLinejoin="round" opacity={o} />
    </svg>
  );
};
