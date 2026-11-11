import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 11 (nhiệt kế): tường phòng thí nghiệm xanh lá nhạt tối, vạch chia mờ chạy dọc hai bên.
// Dấu ấn riêng: một cột chất lỏng đỏ nhỏ ở mép trái dâng lên rồi hạ xuống, mỗi nhịp 3 giây.
export const NkBackground: React.FC = () => {
  const f = useCurrentFrame();
  const p = 0.5 - 0.5 * Math.cos(((f % 180) / 180) * Math.PI * 2);
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="labG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#1f3a3a" />
          <stop offset="1" stopColor="#12262a" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#labG)" />
      {Array.from({length: 24}, (_, i) => (
        <g key={i} opacity={0.08}>
          <line x1={0} y1={90 + i * 80} x2={i % 5 ? 28 : 54} y2={90 + i * 80} stroke="#bfe8d8" strokeWidth={3} />
          <line x1={1080} y1={90 + i * 80} x2={1080 - (i % 5 ? 28 : 54)} y2={90 + i * 80} stroke="#bfe8d8" strokeWidth={3} />
        </g>
      ))}
      <rect x={64} y={420} width={16} height={560} rx={8} fill="#0d1c20" stroke="#bfe8d8" strokeWidth={2} opacity={0.35} />
      <rect x={66} y={420 + 556 * (1 - p)} width={12} height={556 * p + 4} rx={6} fill="#e0613b" opacity={0.6} />
      <circle cx={72} cy={996} r={22} fill="#e0613b" opacity={0.6} />
    </svg>
  );
};
