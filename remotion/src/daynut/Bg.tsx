import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 26 (dây thắt nút): ván boong gỗ tối, vạch gỗ ngang, tương phản thấp.
// Dấu ấn riêng: ở mép trái một sợi dây buộc nút thắt nhỏ trượt từ trên xuống rồi hiện lại, lặp mãi.
export const DnBackground: React.FC = () => {
  const f = useCurrentFrame();
  const T = 140;
  const t = (f % T) / T;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="dnG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#2b2a2e" />
          <stop offset="1" stopColor="#15161a" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#dnG)" />
      {Array.from({length: 22}).map((_, i) => (
        <g key={i}>
          <line x1={0} y1={i * 90 + 20} x2={1080} y2={i * 90 + 20} stroke="#b98a52" strokeWidth={3} opacity={0.08} />
          <line x1={(i * 197) % 1080} y1={i * 90 + 20} x2={(i * 197) % 1080} y2={i * 90 + 110} stroke="#b98a52" strokeWidth={3} opacity={0.06} />
        </g>
      ))}
      <line x1={40} y1={380} x2={40} y2={1000} stroke="#c8b08a" strokeWidth={4} opacity={0.22} />
      {[0, 1, 2, 3, 4].map((i) => {
        const y = 380 + ((i * 130 + t * 130) % 650);
        return <circle key={i} cx={40} cy={y} r={9} fill="#c8b08a" opacity={0.3} />;
      })}
    </svg>
  );
};
