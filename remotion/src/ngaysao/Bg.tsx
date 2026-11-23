import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 30 (ngày sao): bầu trời đêm sẫm, các vòng sao xoay rất chậm quanh một điểm, tương phản thấp.
// Dấu ấn riêng: ở mép trái một chiếc đồng hồ nhỏ có kim giờ và kim phút đuổi nhau, lặp mãi.
export const NsBackground: React.FC = () => {
  const f = useCurrentFrame();
  const mn = (f * 3) % 360;
  const hr = mn / 12;
  const cx = 56;
  const cy = 820;
  const hand = (deg: number, len: number, w: number) => {
    const a = ((deg - 90) * Math.PI) / 180;
    return <line x1={cx} y1={cy} x2={cx + Math.cos(a) * len} y2={cy + Math.sin(a) * len} stroke="#e8c77a" strokeWidth={w} strokeLinecap="round" opacity={0.35} />;
  };
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="nsG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#141a30" />
          <stop offset="1" stopColor="#0d0f1a" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#nsG)" />
      <g transform={`rotate(${f * 0.04} 540 560)`}>
        {Array.from({length: 40}).map((_, i) => {
          const r = 120 + (i % 8) * 90;
          const a = (i * 137.5 * Math.PI) / 180;
          return <circle key={i} cx={540 + Math.cos(a) * r} cy={560 + Math.sin(a) * r} r={2.5 + (i % 3)} fill="#fff1d0" opacity={0.12 + 0.06 * Math.sin(f * 0.06 + i)} />;
        })}
      </g>
      <circle cx={cx} cy={cy} r={42} fill="none" stroke="#c8b08a" strokeWidth={4} opacity={0.3} />
      {hand(mn, 34, 4)}
      {hand(hr, 22, 6)}
    </svg>
  );
};
