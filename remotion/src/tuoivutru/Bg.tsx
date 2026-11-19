import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 24 (tuổi vũ trụ): xanh tím sâu, vài thiên hà xoắn ốc mờ.
// Dấu ấn riêng: ở mép trái một chấm sáng (thiên hà) trôi dần ra xa rồi hiện lại, lặp mãi.
const Spiral: React.FC<{cx: number; cy: number; r: number; rot: number; o: number}> = ({cx, cy, r, rot, o}) => (
  <g transform={`translate(${cx} ${cy}) rotate(${rot})`} opacity={o} fill="none" stroke="#b9a6ff" strokeLinecap="round">
    <path d={`M 0 0 Q ${r * 0.5} ${-r * 0.7} ${r} 0`} strokeWidth={6} />
    <path d={`M 0 0 Q ${-r * 0.5} ${r * 0.7} ${-r} 0`} strokeWidth={6} />
    <circle r={r * 0.12} fill="#e8deff" stroke="none" />
  </g>
);
export const TvBackground: React.FC = () => {
  const f = useCurrentFrame();
  const T = 150;
  const t = (f % T) / T;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <radialGradient id="tvG" cx="0.5" cy="0.4" r="0.95">
          <stop offset="0" stopColor="#262a5c" />
          <stop offset="1" stopColor="#0d0f26" />
        </radialGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#tvG)" />
      {Array.from({length: 46}).map((_, i) => (
        <circle key={i} cx={(i * 211) % 1080} cy={(i * 367) % 1920} r={1.4 + (i % 3)} fill="#fff" opacity={0.1 + 0.07 * Math.sin(f * 0.05 + i)} />
      ))}
      <Spiral cx={820} cy={640} r={150} rot={20 + f * 0.1} o={0.1} />
      <Spiral cx={200} cy={1050} r={190} rot={-30 - f * 0.08} o={0.09} />
      <Spiral cx={860} cy={1500} r={120} rot={60 + f * 0.12} o={0.1} />
      <circle cx={46 + 120 * t * t} cy={440} r={9 * (1 - 0.5 * t)} fill="#f2c14e" opacity={0.95 * (1 - t)} />
      <line x1={46} y1={440} x2={46 + 120 * t * t} y2={440} stroke="#f2c14e" strokeWidth={2} strokeDasharray="6 8" opacity={0.3 * (1 - t)} />
      <circle cx={46} cy={440} r={4} fill="#f2c14e" opacity={0.5} />
    </svg>
  );
};
