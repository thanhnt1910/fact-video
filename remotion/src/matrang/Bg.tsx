import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 15 (Mặt Trăng xa bao nhiêu): trời đêm xanh đen, sao thưa, chân trời Trái Đất cong ở đáy khung.
// Dấu ấn riêng: một chấm sáng nhỏ ở mép trái bay từ dưới lên rồi tắt, lặp lại mỗi 3 giây, như một hạt ánh sáng đi về phía Mặt Trăng.
const STARS = Array.from({length: 46}).map((_, i) => {
  const a = Math.sin(i * 12.9898) * 43758.5453;
  const b = Math.sin(i * 78.233) * 12543.123;
  return [((a - Math.floor(a)) * 1000 + 40) | 0, ((b - Math.floor(b)) * 1500 + 60) | 0, 1.5 + (i % 3)];
});
export const MtBackground: React.FC = () => {
  const f = useCurrentFrame();
  const t = (f % 90) / 90;
  const y = 1240 - t * 800;
  const o = t < 0.85 ? 0.9 : (1 - t) / 0.15 * 0.9;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="mtG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#0d1428" />
          <stop offset="1" stopColor="#070a16" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#mtG)" />
      {STARS.map(([x, yy, r], i) => (
        <circle key={i} cx={x} cy={yy} r={r} fill="#dfe6ff" opacity={0.18 + 0.12 * Math.sin(f * 0.05 + i)} />
      ))}
      <path d="M -200 1960 Q 540 1560 1280 1960 Z" fill="#14305a" opacity={0.55} />
      <path d="M -200 1960 Q 540 1560 1280 1960" fill="none" stroke="#5f8fd0" strokeWidth={4} opacity={0.3} />
      <circle cx={62} cy={y} r={8} fill="#9fe8ff" opacity={o} />
      <line x1={62} y1={y + 10} x2={62} y2={y + 60} stroke="#9fe8ff" strokeWidth={4} strokeLinecap="round" opacity={o * 0.4} />
    </svg>
  );
};
