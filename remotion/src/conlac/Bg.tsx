import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 21 (con lắc Phu-cô): sàn đá cổ điển của một ngôi đền, ánh sáng xám vàng, hoa văn mờ.
// Dấu ấn riêng: một quả lắc nhỏ ở mép trái đung đưa, vạch phía sau xoay chậm từng chút, lặp lại.
export const ClBackground: React.FC = () => {
  const f = useCurrentFrame();
  const swing = Math.sin(f * 0.12) * 0.5;
  const px = 62;
  const py = 400;
  const L = 70;
  const trail = ((f * 0.4) % 360) * (Math.PI / 180);
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <radialGradient id="clG" cx="0.5" cy="0.45" r="0.8">
          <stop offset="0" stopColor="#38342b" />
          <stop offset="1" stopColor="#1a1812" />
        </radialGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#clG)" />
      {Array.from({length: 9}).map((_, i) => (
        <line key={'a' + i} x1={0} y1={i * 240} x2={1080} y2={i * 240 + 360} stroke="#d8c9a0" strokeWidth={2} opacity={0.05} />
      ))}
      {Array.from({length: 9}).map((_, i) => (
        <line key={'b' + i} x1={0} y1={i * 240 + 360} x2={1080} y2={i * 240} stroke="#d8c9a0" strokeWidth={2} opacity={0.05} />
      ))}
      <circle cx={540} cy={1000} r={470} fill="none" stroke="#d8c9a0" strokeWidth={2} opacity={0.06} />
      <line x1={px - 40 * Math.cos(trail)} y1={py + 90 - 40 * Math.sin(trail)} x2={px + 40 * Math.cos(trail)} y2={py + 90 + 40 * Math.sin(trail)} stroke="#f2c14e" strokeWidth={2} opacity={0.3} />
      <line x1={px} y1={py} x2={px + L * Math.sin(swing)} y2={py + L * Math.cos(swing)} stroke="#d8c9a0" strokeWidth={3} opacity={0.6} />
      <circle cx={px + L * Math.sin(swing)} cy={py + L * Math.cos(swing)} r={9} fill="#f2c14e" opacity={0.9} />
    </svg>
  );
};
