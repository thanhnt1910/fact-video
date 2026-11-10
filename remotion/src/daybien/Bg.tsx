import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 5 (đáy biển): nước xanh sẫm dần xuống sâu, tia sáng từ mặt nước, bọt bay lên.
// Dấu ấn riêng: vòng sóng âm (sonar) lan ra từng nhịp 3 giây, ở mọi cảnh.
const W = 1080;
const H = 1920;

export const DbBackground: React.FC = () => {
  const f = useCurrentFrame();
  const PERIOD = 90;
  const rings = [0, 1, 2].map((k) => {
    const t = (((f - k * 14) % PERIOD) + PERIOD) % PERIOD;
    const p = t / PERIOD;
    return {r: 40 + p * 760, o: 0.3 * (1 - p) * (1 - p)};
  });
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="dbSea" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#1d5f78" />
          <stop offset="0.35" stopColor="#123f55" />
          <stop offset="0.7" stopColor="#0a2538" />
          <stop offset="1" stopColor="#050f19" />
        </linearGradient>
        <linearGradient id="dbRay" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#bfe9f2" stopOpacity="0.5" />
          <stop offset="1" stopColor="#bfe9f2" stopOpacity="0" />
        </linearGradient>
      </defs>
      <rect width={W} height={H} fill="url(#dbSea)" />
      {[0, 1, 2, 3, 4].map((i) => {
        const x = 120 + i * 220;
        const sway = Math.sin(f * 0.012 + i * 1.7) * 40;
        return <polygon key={i} points={`${x + sway} 0 ${x + 90 + sway} 0 ${x - 90 + sway * 1.6} 1100 ${x - 200 + sway * 1.6} 1100`} fill="url(#dbRay)" opacity={0.1 + 0.07 * Math.abs(Math.sin(f * 0.02 + i))} />;
      })}
      {Array.from({length: 26}, (_, i) => {
        const sp = 0.5 + ((i * 7) % 5) * 0.25;
        const y = 1900 - ((f * sp + i * 173) % 1850);
        const x = ((i * 389) % 1000) + 40 + Math.sin(f * 0.03 + i) * 12;
        return <circle key={i} cx={x} cy={y} r={3 + (i % 4)} fill="none" stroke="#cfeef5" strokeWidth={2} opacity={0.18} />;
      })}
      {rings.map((g, i) => (
        <circle key={i} cx={540} cy={800} r={g.r} fill="none" stroke="#7fd3e6" strokeWidth={4} opacity={g.o} />
      ))}
      <g fill="none" stroke="#3b8aa3" strokeWidth={3}>
        {[0, 1, 2].map((r) => (
          <path key={r} opacity={0.12 + r * 0.04} d={Array.from({length: 22}, (_, i) => `${i ? 'L' : 'M'} ${i * 52 - 20} ${1640 + r * 80 + Math.sin(i * 0.9 + f * 0.04 + r * 1.3) * (8 + r * 2)}`).join(' ')} />
        ))}
      </g>
    </svg>
  );
};
