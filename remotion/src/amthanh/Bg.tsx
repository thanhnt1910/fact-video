import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 9 (tốc độ âm thanh): bầu trời giông xám xanh, mây thấp, mưa mảnh, tương phản thấp.
// Dấu ấn riêng: cứ 3 giây có một tia chớp lóe ở góc trái, rồi vòng sóng âm tròn lan chậm ra sau nó.
export const AmBackground: React.FC = () => {
  const f = useCurrentFrame();
  const P = 90;
  const t = f % P;
  const flash = t < 5 ? 0.22 * (1 - t / 5) : 0;
  const rr = 30 + (t / P) * 760;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="stormG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#2a3446" />
          <stop offset="0.55" stopColor="#222c3c" />
          <stop offset="1" stopColor="#131a26" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#stormG)" />
      {Array.from({length: 7}, (_, i) => (
        <ellipse key={i} cx={(i * 230 + f * 0.25) % 1300 - 100} cy={150 + (i % 3) * 120} rx={240} ry={70} fill="#3a465c" opacity={0.35} />
      ))}
      {Array.from({length: 40}, (_, i) => {
        const x = (i * 271) % 1080;
        const y = ((i * 523 + f * (14 + (i % 4) * 3)) % 1900);
        return <line key={i} x1={x} y1={y} x2={x - 8} y2={y + 36} stroke="#9fb3d4" strokeWidth={2} opacity={0.12} />;
      })}
      <rect width={1080} height={1920} fill="#cfe0ff" opacity={flash} />
      <path d="M 150 180 L 118 250 L 146 252 L 112 330" fill="none" stroke="#fff2b0" strokeWidth={5} strokeLinejoin="round" opacity={0.25 + (t < 6 ? 0.6 : 0)} />
      <circle cx={130} cy={330} r={rr} fill="none" stroke="#bcd0f0" strokeWidth={3} opacity={0.2 * (1 - t / P)} />
    </svg>
  );
};
