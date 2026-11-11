import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 8 (khoảng cách sao): bầu trời đêm xanh đen, sao lấp lánh, tương phản thấp.
// Dấu ấn riêng: một chấm sao nhỏ nhảy qua lại giữa hai vị trí mỗi 3 giây, giống ngón tay nhảy khi đổi mắt.
export const SaoBackground: React.FC = () => {
  const f = useCurrentFrame();
  const P = 90;
  const phase = Math.floor((f % (P * 2)) / P);
  const ease = Math.min(1, ((f % P) / 10));
  const xa = 150, xb = 215;
  const x = phase === 0 ? xa + (xb - xa) * (1 - ease) : xa + (xb - xa) * ease;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="skyN" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#0b1030" />
          <stop offset="0.6" stopColor="#141a45" />
          <stop offset="1" stopColor="#1f1d4a" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#skyN)" />
      {Array.from({length: 70}, (_, i) => {
        const sx = (i * 487) % 1060 + 10;
        const sy = (i * 733) % 1880 + 20;
        return <circle key={i} cx={sx} cy={sy} r={1.5 + (i % 3) * 0.9} fill="#dfe6ff" opacity={0.18 + 0.22 * Math.abs(Math.sin(f * 0.03 + i * 1.3))} />;
      })}
      <circle cx={x} cy={420} r={7} fill="#ffe9a8" opacity={0.85} />
      <circle cx={xa} cy={420} r={3} fill="none" stroke="#ffe9a8" strokeWidth={1.5} opacity={0.35} />
      <circle cx={xb} cy={420} r={3} fill="none" stroke="#ffe9a8" strokeWidth={1.5} opacity={0.35} />
    </svg>
  );
};
