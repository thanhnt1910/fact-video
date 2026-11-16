import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 20 (một năm dài bao nhiêu ngày): bầu trời hoàng hôn xám tím có vạch quỹ đạo Mặt Trời rất mờ.
// Dấu ấn riêng: một chấm vàng nhỏ ở mép trái đi một vòng quanh mỗi 3 giây; cứ bốn vòng thì lần thứ tư có thêm một đoạn nhỏ (ngày nhuận).
export const NdBackground: React.FC = () => {
  const f = useCurrentFrame();
  const lap = Math.floor(f / 90) % 4;
  const t = (f % 90) / 90;
  const a = t * 2 * Math.PI - Math.PI / 2;
  const extra = lap === 3 ? Math.min(1, t * 4) : 0;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="ndG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#2b2542" />
          <stop offset="1" stopColor="#120f24" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#ndG)" />
      {[320, 520, 760].map((r, i) => (
        <path key={i} d={`M ${540 - r} 1100 A ${r} ${r * 0.8} 0 0 1 ${540 + r} 1100`} fill="none" stroke="#c9b6ea" strokeWidth={2} opacity={0.08} />
      ))}
      <line x1={0} y1={1100} x2={1080} y2={1100} stroke="#c9b6ea" strokeWidth={2} opacity={0.06} />
      <circle cx={62} cy={470} r={26} fill="none" stroke="#c9b6ea" strokeWidth={2} opacity={0.3} />
      <circle cx={62 + 26 * Math.cos(a)} cy={470 + 26 * Math.sin(a)} r={7} fill="#f2c14e" opacity={0.9} />
      {extra > 0 && <rect x={54} y={430} width={16} height={8 * extra} fill="#f2c14e" opacity={0.9} />}
    </svg>
  );
};
