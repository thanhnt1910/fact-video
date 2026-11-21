import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 27 (đường chân trời): bầu trời hoàng hôn tối, mặt biển phẳng ở đáy, tương phản thấp.
// Dấu ấn riêng: ở mép trái một chấm tròn (con mắt) trượt lên xuống và vạch một đường chân trời mảnh ở độ cao của nó, lặp mãi.
export const CtBackground: React.FC = () => {
  const f = useCurrentFrame();
  const T = 160;
  const t = (f % T) / T;
  const y = 560 + 360 * (0.5 - 0.5 * Math.cos(t * Math.PI * 2));
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="ctG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#1b2033" />
          <stop offset="0.55" stopColor="#2c2a3c" />
          <stop offset="1" stopColor="#14181f" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#ctG)" />
      <rect x={0} y={1500} width={1080} height={420} fill="#101722" opacity={0.7} />
      <line x1={0} y1={1500} x2={1080} y2={1500} stroke="#e8c77a" strokeWidth={3} opacity={0.12} />
      {[0, 1, 2, 3].map((i) => (
        <line key={i} x1={200 + i * 230} y1={1560 + i * 30} x2={330 + i * 230} y2={1560 + i * 30} stroke="#6fa0c8" strokeWidth={3} opacity={0.1} />
      ))}
      <line x1={40} y1={540} x2={40} y2={940} stroke="#c8b08a" strokeWidth={3} opacity={0.15} />
      <line x1={40} y1={y} x2={120} y2={y} stroke="#e8c77a" strokeWidth={3} opacity={0.22} />
      <circle cx={40} cy={y} r={11} fill="#e8c77a" opacity={0.35} />
    </svg>
  );
};
