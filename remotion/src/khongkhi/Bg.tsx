import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 16 (không khí nặng bao nhiêu): trời chiều xám xanh, vài lớp mây rất mờ trôi chậm.
// Dấu ấn riêng: một giọt thủy ngân bạc nhỏ ở mép trái nhấp nhô lên xuống, lặp lại.
export const KkBackground: React.FC = () => {
  const f = useCurrentFrame();
  const bob = Math.sin(f * 0.12) * 16;
  const clouds = [[180, 1500, 1.0], [700, 1600, 1.3], [420, 1760, 0.9], [960, 1450, 0.8]] as const;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="kkG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#1b2430" />
          <stop offset="1" stopColor="#10161e" />
        </linearGradient>
        <radialGradient id="kkD" cx="0.35" cy="0.35" r="0.7">
          <stop offset="0" stopColor="#ffffff" />
          <stop offset="0.5" stopColor="#c7ccd4" />
          <stop offset="1" stopColor="#7d8591" />
        </radialGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#kkG)" />
      {clouds.map(([x, y, s], i) => {
        const dx = ((x + f * 0.3 * (i % 2 ? 1 : 0.6)) % 1300) - 110;
        return (
          <g key={i} opacity={0.06} transform={`translate(${dx} ${y}) scale(${s})`} fill="#c9d6e6">
            <ellipse cx={0} cy={0} rx={110} ry={40} />
            <ellipse cx={60} cy={-30} rx={70} ry={45} />
            <ellipse cx={-60} cy={-20} rx={60} ry={35} />
          </g>
        );
      })}
      <path d={`M 62 ${414 + bob} q 14 22 0 32 q -14 -10 0 -32 z`} fill="url(#kkD)" opacity={0.9} />
      <ellipse cx={62} cy={472} rx={16} ry={4} fill="#7d8591" opacity={0.3 - bob * 0.008} />
    </svg>
  );
};
