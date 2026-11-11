import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 13 (núi cao): trời xanh lam tối, các dãy núi xa mờ, tương phản thấp.
// Dấu ấn riêng: một tia ngắm mảnh quét lên đỉnh núi nhỏ ở mép trái, chu kỳ 3 giây.
export const NcBackground: React.FC = () => {
  const f = useCurrentFrame();
  const t = (f % 90) / 90;
  const ang = 8 + 26 * Math.sin(Math.min(1, t * 1.4) * Math.PI * 0.5) * (t < 0.7 ? 1 : 1 - (t - 0.7) / 0.3);
  const rad = (ang * Math.PI) / 180;
  const L = 90;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="ncG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#1b2d4a" />
          <stop offset="1" stopColor="#0d1828" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#ncG)" />
      <path d="M 0 1500 L 160 1280 L 300 1420 L 470 1180 L 640 1400 L 800 1250 L 1080 1480 L 1080 1920 L 0 1920 Z" fill="#2a4166" opacity={0.28} />
      <path d="M 0 1640 L 220 1470 L 380 1590 L 560 1400 L 760 1580 L 920 1470 L 1080 1600 L 1080 1920 L 0 1920 Z" fill="#35527f" opacity={0.22} />
      <path d="M 0 1780 L 200 1680 L 420 1770 L 640 1650 L 860 1760 L 1080 1690 L 1080 1920 L 0 1920 Z" fill="#162338" opacity={0.6} />
      {[[90, 120], [300, 250], [520, 150], [760, 280], [960, 190], [200, 380], [860, 400]].map(([x, y], i) => (
        <circle key={i} cx={x} cy={y} r={2.2} fill="#cfe3ff" opacity={0.35} />
      ))}
      <g opacity={0.5}>
        <path d="M 52 405 L 150 405 L 150 330 L 118 372 L 100 345 L 78 372 Z" fill="none" stroke="#9fc4ff" strokeWidth={3} strokeLinejoin="round" />
        <line x1={52} y1={405} x2={52 + L * Math.cos(rad) * 1.1} y2={405 - L * Math.sin(rad) * 1.1} stroke="#e8c58a" strokeWidth={3} />
      </g>
    </svg>
  );
};
