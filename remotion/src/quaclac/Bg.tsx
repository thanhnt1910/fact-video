import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 12 (đồng hồ quả lắc): tường gỗ nâu ấm tối, bánh răng mờ xoay chậm, tương phản thấp.
// Dấu ấn riêng: một quả lắc nhỏ đung đưa đều ở mép trái, mỗi lượt đưa đúng 2 giây (như quả lắc 1 mét).
const Gear: React.FC<{x: number; y: number; r: number; rot: number}> = ({x, y, r, rot}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot})`} opacity={0.09} fill="none" stroke="#e8c58a" strokeWidth={5}>
    <circle r={r} />
    <circle r={r * 0.3} />
    {Array.from({length: 12}, (_, i) => <line key={i} x1={r} y1={0} x2={r + 22} y2={0} strokeWidth={14} transform={`rotate(${i * 30})`} />)}
  </g>
);
export const QlBackground: React.FC = () => {
  const f = useCurrentFrame();
  const a = 24 * Math.sin((f / 60) * Math.PI * 2);
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="woodG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#3b2a1d" />
          <stop offset="1" stopColor="#24180f" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#woodG)" />
      {Array.from({length: 9}, (_, i) => <line key={i} x1={i * 135} y1={0} x2={i * 135} y2={1920} stroke="#1d130c" strokeWidth={3} opacity={0.5} />)}
      <Gear x={940} y={1000} r={150} rot={f * 0.25} />
      <Gear x={760} y={1180} r={90} rot={-f * 0.42} />
      <Gear x={120} y={1500} r={120} rot={f * 0.3} />
      <g transform={`translate(95 372) rotate(${a})`} opacity={0.5}>
        <line x1={0} y1={0} x2={0} y2={60} stroke="#e8c58a" strokeWidth={3} />
        <circle cx={0} cy={68} r={10} fill="#e8c58a" />
      </g>
      <circle cx={95} cy={372} r={4} fill="#e8c58a" opacity={0.6} />
    </svg>
  );
};
