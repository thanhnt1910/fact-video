import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 7 (kính hiển vi): xưởng vải Delft ấm màu nâu, hạt bụi bay trong chùm nắng.
// Dấu ấn riêng: một vòng tròn thấu kính trượt nhẹ, bên trong các chấm nhỏ bơi lượn.
const W = 1080;
const H = 1920;

export const KhBackground: React.FC = () => {
  const f = useCurrentFrame();
  const cx = 540 + Math.sin(f * 0.012) * 260;
  const cy = 820 + Math.cos(f * 0.009) * 120;
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="khBg" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#4a3626" />
          <stop offset="0.55" stopColor="#32241a" />
          <stop offset="1" stopColor="#1a120d" />
        </linearGradient>
        <clipPath id="khLens"><circle cx={cx} cy={cy} r={170} /></clipPath>
      </defs>
      <rect width={W} height={H} fill="url(#khBg)" />
      <polygon points="780,0 1080,0 1080,700 420,1500" fill="#f4d28a" opacity={0.05} />
      {Array.from({length: 30}, (_, i) => (
        <circle key={i} cx={((i * 353) % 1060) + 10 + Math.sin(f * 0.02 + i) * 16} cy={((i * 571 + f * (0.3 + (i % 5) * 0.12)) % 1900) + 10} r={1.8 + (i % 3)} fill="#f4d28a" opacity={0.12 + 0.12 * Math.abs(Math.sin(f * 0.05 + i))} />
      ))}
      {Array.from({length: 7}, (_, i) => (
        <line key={i} x1={0} y1={260 + i * 260} x2={W} y2={260 + i * 260} stroke="#8a6a48" strokeWidth={2} opacity={0.08} />
      ))}
      <circle cx={cx} cy={cy} r={170} fill="#f4d28a" opacity={0.05} />
      <circle cx={cx} cy={cy} r={170} fill="none" stroke="#e0b97a" strokeWidth={4} opacity={0.14} />
      <g clipPath="url(#khLens)">
        {Array.from({length: 14}, (_, i) => (
          <circle key={i} cx={cx + Math.sin(f * (0.03 + (i % 4) * 0.01) + i * 2) * 120} cy={cy + Math.cos(f * (0.025 + (i % 3) * 0.012) + i) * 120} r={5 + (i % 3) * 2} fill="#bfe3c0" opacity={0.16} />
        ))}
      </g>
    </svg>
  );
};
