import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 25 (sóng thần): biển xanh thẫm, các vạch sóng mờ chạy ngang.
// Dấu ấn riêng: ở mép trái một vòng gợn sóng loang rộng rồi tan, lặp mãi.
export const StBackground: React.FC = () => {
  const f = useCurrentFrame();
  const T = 90;
  const t = (f % T) / T;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="stG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#17354a" />
          <stop offset="1" stopColor="#0b1822" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#stG)" />
      {Array.from({length: 12}).map((_, i) => {
        const y = 120 + i * 150;
        const ph = f * 0.04 + i;
        let d = `M 0 ${y}`;
        for (let x = 0; x <= 1080; x += 60) d += ` L ${x} ${y + 10 * Math.sin(x * 0.012 + ph)}`;
        return <path key={i} d={d} fill="none" stroke="#7fc2d6" strokeWidth={3} opacity={0.09} />;
      })}
      <circle cx={70} cy={560} r={8 + 70 * t} fill="none" stroke="#9fd8e8" strokeWidth={3} opacity={0.5 * (1 - t)} />
      <circle cx={70} cy={560} r={4 + 40 * t} fill="none" stroke="#9fd8e8" strokeWidth={2} opacity={0.4 * (1 - t)} />
      <circle cx={70} cy={560} r={4} fill="#9fd8e8" opacity={0.5} />
    </svg>
  );
};
