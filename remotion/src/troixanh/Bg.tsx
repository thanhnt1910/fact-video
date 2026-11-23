import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 29 (bầu trời xanh): bầu trời xanh đậm chuyển sang cam tím ở đáy, tương phản thấp.
// Dấu ấn riêng: ở mép trái một tia sáng trắng nhỏ đi vào rồi tách thành tia đỏ và tia xanh, lặp mãi.
export const TxBackground: React.FC = () => {
  const f = useCurrentFrame();
  const T = 150;
  const t = (f % T) / T;
  const p = Math.min(1, t / 0.5);
  const q = Math.max(0, (t - 0.35) / 0.5);
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="txG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#14284a" />
          <stop offset="0.6" stopColor="#1d3358" />
          <stop offset="0.85" stopColor="#3a3350" />
          <stop offset="1" stopColor="#4a3340" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#txG)" />
      <line x1={10} y1={800} x2={10 + 50 * p} y2={800} stroke="#fff1d0" strokeWidth={6} strokeLinecap="round" opacity={0.3} />
      <line x1={60} y1={800} x2={60 + 55 * q} y2={800 - 55 * q} stroke="#e0402b" strokeWidth={5} strokeLinecap="round" opacity={0.3 * Math.min(1, q * 3)} />
      <line x1={60} y1={800} x2={60 + 55 * q} y2={800 + 55 * q} stroke="#3a7be0" strokeWidth={5} strokeLinecap="round" opacity={0.3 * Math.min(1, q * 3)} />
    </svg>
  );
};
