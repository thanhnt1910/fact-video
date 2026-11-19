import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 23 (giếng sâu): tường đá cổ rêu xanh xám, tương phản thấp.
// Dấu ấn riêng: ở mép trái một giọt nước rơi từ trên xuống, chạm đáy thì gợn sóng, lặp mãi.
export const GiBackground: React.FC = () => {
  const f = useCurrentFrame();
  const T = 70;
  const t = (f % T) / T;
  const dy = 380 + 1.0 * 520 * t * t; // rơi nhanh dần
  const hit = t > 0.98 || t < 0.55 ? 0 : 0;
  void hit;
  const rip = (f % T) / T;
  const bottom = 900;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="giG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#2c3a38" />
          <stop offset="1" stopColor="#141c1d" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#giG)" />
      {Array.from({length: 14}).map((_, r) =>
        Array.from({length: 6}).map((__, c) => {
          const x = c * 190 + (r % 2 ? 95 : 0) - 60;
          const y = r * 150 + 20;
          return <rect key={r + '-' + c} x={x} y={y} width={176} height={136} rx={22} fill="none" stroke="#8fb0a4" strokeOpacity={0.08} strokeWidth={4} />;
        }),
      )}
      {[0, 3, 5, 8, 11].map((r, i) => (
        <ellipse key={i} cx={(i * 263 + 120) % 1080} cy={r * 150 + 150} rx={60 + i * 8} ry={14} fill="#6fa27a" opacity={0.1} />
      ))}
      <rect x={30} y={bottom} width={64} height={6} rx={3} fill="#7fc2d6" opacity={0.25} />
      <ellipse cx={62} cy={bottom + 3} rx={8 + 38 * rip} ry={3 + 7 * rip} fill="none" stroke="#9fd8e8" strokeWidth={2} opacity={0.5 * (1 - rip)} />
      {t < 0.75 && <path d={`M 62 ${dy - 22} Q 70 ${dy} 62 ${dy + 8} Q 54 ${dy} 62 ${dy - 22} Z`} fill="#9fd8e8" opacity={0.7} />}
    </svg>
  );
};
