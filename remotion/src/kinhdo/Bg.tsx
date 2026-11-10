import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../lib/theme';

// Nền riêng của video 4 (kinh độ): trời đêm trên biển, la bàn mờ, lưới kinh vĩ tuyến.
// Dấu ấn riêng: kim giây đồng hồ hàng hải quét quanh la bàn, nhích từng nhịp mỗi giây.
const W = 1080;
const H = 1920;
const CX = 540;
const CY = 760;

export const KdBackground: React.FC = () => {
  const f = useCurrentFrame();
  const tick = Math.floor(f / 30) * 6 + Math.min(1, (f % 30) / 4) * 6; // nhích 6 độ mỗi giây
  const rot = f * 0.04;
  const star = (i: number) => ({x: (i * 389) % 1040 + 20, y: (i * 617) % 900 + 120});
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="kdSky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#0d1722" />
          <stop offset="0.42" stopColor="#14222d" />
          <stop offset="0.62" stopColor="#1b3340" />
          <stop offset="1" stopColor="#0c1218" />
        </linearGradient>
        <radialGradient id="kdGlow" cx="0.5" cy="0.4" r="0.55">
          <stop offset="0" stopColor="#e9a84c" stopOpacity="0.16" />
          <stop offset="1" stopColor="#e9a84c" stopOpacity="0" />
        </radialGradient>
      </defs>
      <rect width={W} height={H} fill="url(#kdSky)" />
      <rect width={W} height={H} fill="url(#kdGlow)" />
      {Array.from({length: 40}, (_, i) => {
        const s = star(i);
        return <circle key={i} cx={s.x} cy={s.y} r={1.4 + (i % 3) * 0.7} fill={C.cream} opacity={0.15 + 0.2 * Math.abs(Math.sin(f * 0.04 + i))} />;
      })}
      {/* lưới kinh tuyến (cong) và vĩ tuyến */}
      <g fill="none" stroke={C.cream} strokeWidth={1.5} opacity={0.07}>
        {[-3, -2, -1, 0, 1, 2, 3].map((k) => (
          <path key={k} d={`M ${CX + k * 40} 80 Q ${CX + k * 330} 960 ${CX + k * 40} 1840`} />
        ))}
        {[300, 520, 760, 1000, 1240, 1480].map((y) => (
          <path key={y} d={`M 0 ${y} Q ${CX} ${y + 60} ${W} ${y}`} />
        ))}
      </g>
      {/* la bàn mờ */}
      <g transform={`translate(${CX} ${CY}) rotate(${rot})`} fill="none" stroke={C.cream} opacity={0.1}>
        <circle r={440} strokeWidth={3} />
        <circle r={400} strokeWidth={1.5} />
        {Array.from({length: 72}, (_, i) => (
          <line key={i} x1={0} y1={-400} x2={0} y2={i % 6 === 0 ? -430 : -414} strokeWidth={i % 6 === 0 ? 3 : 1.5} transform={`rotate(${i * 5})`} />
        ))}
        {[0, 90, 180, 270].map((a) => (
          <path key={a} d="M 0 -380 L 22 0 L -22 0 Z" fill={C.cream} stroke="none" transform={`rotate(${a})`} />
        ))}
      </g>
      {/* dấu ấn: kim giây nhích từng nhịp */}
      <g transform={`translate(${CX} ${CY}) rotate(${tick})`} opacity={0.32}>
        <line x1={0} y1={30} x2={0} y2={-440} stroke={C.amber} strokeWidth={3} strokeLinecap="round" />
        <circle cx={0} cy={-440} r={9} fill={C.amber} />
      </g>
      {/* biển ở đáy */}
      <g fill="none" stroke="#3b8aa3" strokeWidth={3}>
        {[0, 1, 2, 3, 4].map((r) => (
          <path key={r} opacity={0.1 + r * 0.03} d={Array.from({length: 22}, (_, i) => `${i ? 'L' : 'M'} ${i * 52 - 20} ${1560 + r * 70 + Math.sin(i * 0.9 + f * 0.04 + r * 1.3) * (8 + r * 2)}`).join(' ')} />
        ))}
      </g>
    </svg>
  );
};
