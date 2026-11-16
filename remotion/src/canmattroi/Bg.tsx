import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 22 (cân Mặt Trời): bầu trời vũ trụ tím than, sao mờ, quỹ đạo elip mờ.
// Dấu ấn riêng: ở mép trái một "Mặt Trời" nhỏ vàng, một chấm xanh (Trái Đất) quay quanh nó, lặp mãi.
export const CmBackground: React.FC = () => {
  const f = useCurrentFrame();
  const sx = 62, sy = 420, R = 46;
  const a = f * 0.07;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <radialGradient id="cmG" cx="0.5" cy="0.4" r="0.9">
          <stop offset="0" stopColor="#1f2147" />
          <stop offset="1" stopColor="#0c0d22" />
        </radialGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#cmG)" />
      {Array.from({length: 40}).map((_, i) => (
        <circle key={i} cx={(i * 197) % 1080} cy={(i * 413) % 1920} r={1.5 + (i % 3)} fill="#fff" opacity={0.1 + 0.08 * Math.sin(f * 0.05 + i)} />
      ))}
      <ellipse cx={540} cy={1000} rx={470} ry={330} fill="none" stroke="#9fb0ff" strokeWidth={2} opacity={0.07} />
      <ellipse cx={540} cy={1000} rx={300} ry={210} fill="none" stroke="#9fb0ff" strokeWidth={2} opacity={0.06} />
      <circle cx={sx} cy={sy} r={R} fill="none" stroke="#f2c14e" strokeWidth={2} opacity={0.3} />
      <circle cx={sx} cy={sy} r={16} fill="#f2c14e" opacity={0.9} />
      <circle cx={sx + R * Math.cos(a)} cy={sy + R * Math.sin(a)} r={7} fill="#4a8fe0" opacity={0.95} />
    </svg>
  );
};
