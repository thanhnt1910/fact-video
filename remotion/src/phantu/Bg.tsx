import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 19 (phân tử dày bao nhiêu): mặt nước ao xanh đậm có gợn sóng rất mờ.
// Dấu ấn riêng: một giọt dầu nhỏ ở mép trái rơi xuống rồi loang thành vòng tròn mỏng dần, lặp lại mỗi 3 giây.
export const PtBackground: React.FC = () => {
  const f = useCurrentFrame();
  const t = (f % 90) / 90;
  const fall = Math.min(1, t / 0.3);
  const spread = Math.max(0, (t - 0.3) / 0.7);
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <radialGradient id="ptG" cx="0.5" cy="0.45" r="0.8">
          <stop offset="0" stopColor="#14343f" />
          <stop offset="1" stopColor="#0a1a21" />
        </radialGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#ptG)" />
      {Array.from({length: 16}).map((_, i) => (
        <path
          key={i}
          d={`M 0 ${120 + i * 120} Q 270 ${100 + i * 120 + 14 * Math.sin(f * 0.03 + i)} 540 ${120 + i * 120} T 1080 ${120 + i * 120}`}
          fill="none"
          stroke="#8fd0e0"
          strokeWidth={2}
          opacity={0.06}
        />
      ))}
      {t < 0.3 && <circle cx={64} cy={380 + fall * 90} r={9} fill="#f2c14e" opacity={0.9} />}
      {t >= 0.3 && <circle cx={64} cy={470} r={10 + spread * 30} fill="none" stroke="#f2c14e" strokeWidth={Math.max(1, 5 * (1 - spread))} opacity={0.9 * (1 - spread * 0.8)} />}
    </svg>
  );
};
