import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 6 (vương miện): nước xanh ngọc ấm như bể tắm cổ, vệt sáng lung linh trên mặt nước.
// Dấu ấn riêng: giọt nước rơi tạo vòng gợn lan ra mỗi nhịp 3 giây, kèm hạt vàng lấp lánh trôi chậm.
const W = 1080;
const H = 1920;

export const VmBackground: React.FC = () => {
  const f = useCurrentFrame();
  const P = 90;
  const t = f % P;
  const p = t / P;
  const drop = t < 14 ? {y: 300 + (t / 14) * 480, o: 0.8} : {y: 0, o: 0};
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="vmSea" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#1f6a68" />
          <stop offset="0.5" stopColor="#164a52" />
          <stop offset="1" stopColor="#0a1e26" />
        </linearGradient>
      </defs>
      <rect width={W} height={H} fill="url(#vmSea)" />
      {Array.from({length: 9}, (_, i) => (
        <path key={i} d={`M -40 ${160 + i * 190} ${Array.from({length: 14}, (_, j) => `L ${j * 90} ${160 + i * 190 + Math.sin(j * 0.9 + f * 0.03 + i * 1.4) * 22}`).join(' ')}`} fill="none" stroke="#9fe0d8" strokeWidth={3} opacity={0.07 + 0.03 * Math.sin(f * 0.02 + i)} />
      ))}
      {Array.from({length: 22}, (_, i) => {
        const x = ((i * 389) % 1000) + 40 + Math.sin(f * 0.02 + i) * 14;
        const y = ((i * 617) % 1500) + 200 + ((f * (0.2 + (i % 4) * 0.1)) % 120);
        return <circle key={i} cx={x} cy={y} r={2.5 + (i % 3)} fill="#e9c35a" opacity={0.15 + 0.2 * Math.abs(Math.sin(f * 0.06 + i))} />;
      })}
      <circle cx={540} cy={800} r={20 + p * 520} fill="none" stroke="#bff0e8" strokeWidth={4} opacity={0.26 * (1 - p) * (1 - p)} />
      <circle cx={540} cy={800} r={20 + Math.max(0, p - 0.12) * 480} fill="none" stroke="#bff0e8" strokeWidth={3} opacity={0.18 * (1 - p)} />
      {drop.o > 0 && <path d={`M 540 ${drop.y - 24} Q 560 ${drop.y + 4} 540 ${drop.y + 10} Q 520 ${drop.y + 4} 540 ${drop.y - 24} Z`} fill="#bff0e8" opacity={drop.o} />}
    </svg>
  );
};
