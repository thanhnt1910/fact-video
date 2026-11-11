import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 14 (tuổi Trái Đất): các tầng đất đá nâu nhiều lớp, tương phản thấp.
// Dấu ấn riêng: một chấm vàng nhỏ ở mép trái, cứ 2 giây lại hóa xám như một nguyên tử phân rã rồi lặp lại.
export const TdBackground: React.FC = () => {
  const f = useCurrentFrame();
  const t = f % 60;
  const k = Math.min(1, Math.max(0, (t - 40) / 14));
  const col = k < 0.5 ? '#f2c14e' : '#8d8a84';
  const layers = [
    ['#3b2c20', 1480, 0.5],
    ['#4a3626', 1560, 0.45],
    ['#2f2319', 1640, 0.6],
    ['#54402c', 1720, 0.4],
    ['#33261b', 1800, 0.6],
  ] as const;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="tdG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#2a2018" />
          <stop offset="1" stopColor="#140e0a" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#tdG)" />
      {layers.map(([c, y, o], i) => (
        <path key={i} d={`M 0 ${y} Q 270 ${y - 28 + i * 6} 540 ${y} T 1080 ${y - 10} L 1080 1920 L 0 1920 Z`} fill={c} opacity={o} />
      ))}
      {[[140, 1560], [420, 1620], [760, 1700], [980, 1580], [300, 1790], [880, 1850]].map(([x, y], i) => (
        <ellipse key={i} cx={x} cy={y} rx={22} ry={11} fill="#6b5036" opacity={0.3} />
      ))}
      <g opacity={0.8}>
        <circle cx={62} cy={430} r={11} fill={col} />
        <circle cx={62} cy={430} r={17} fill="none" stroke={col} strokeWidth={2} opacity={0.5} />
      </g>
    </svg>
  );
};
