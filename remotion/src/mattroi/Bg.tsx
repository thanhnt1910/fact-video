import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 10 (Mặt Trời – Mặt Trăng): bầu trời hoàng hôn xanh tím, Mặt Trăng bán nguyệt mờ, tương phản thấp.
// Dấu ấn riêng: tam giác nhỏ có ô góc vuông luôn nằm ở Mặt Trăng; góc nhìn từ Trái Đất mở ra rồi khép lại mỗi 6 giây.
export const MtBackground: React.FC = () => {
  const f = useCurrentFrame();
  const t = (f % 180) / 180;
  const ang = 40 + 48 * (0.5 - 0.5 * Math.cos(t * Math.PI * 2));
  const rad = (ang * Math.PI) / 180;
  const mx = 130, my = 372, ey = 432;
  const ex = mx - (ey - my) / Math.tan(rad) * -1;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#262552" />
          <stop offset="0.5" stopColor="#3a2f63" />
          <stop offset="1" stopColor="#5a3d63" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#dusk)" />
      {Array.from({length: 40}, (_, i) => <circle key={i} cx={(i * 463) % 1060 + 10} cy={(i * 811) % 900 + 30} r={1.6 + (i % 3) * 0.7} fill="#e9e4ff" opacity={0.15 + 0.2 * Math.abs(Math.sin(f * 0.03 + i))} />)}
      <circle cx={900} cy={1500} r={150} fill="#e9dcc0" opacity={0.08} />
      <path d="M 900 1350 A 150 150 0 0 0 900 1650 Z" fill="#e9dcc0" opacity={0.12} />
      <g opacity={0.45} stroke="#e9dcc0" strokeWidth={3} fill="none">
        <line x1={mx} y1={my} x2={mx} y2={ey} />
        <line x1={mx} y1={my} x2={mx + 230} y2={my} />
        <line x1={mx} y1={ey} x2={ex + 0} y2={ey} opacity={0} />
        <line x1={mx} y1={ey} x2={mx + 230} y2={my} />
        <rect x={mx} y={my} width={16} height={16} />
        <path d={`M ${mx} ${ey - 30} A 30 30 0 0 1 ${mx + 30 * Math.sin(Math.atan2(230, my - ey) + 0)} ${ey - 30}`} opacity={0} />
      </g>
      <circle cx={mx} cy={my} r={7} fill="#e9dcc0" opacity={0.7} />
      <circle cx={mx + 230} cy={my} r={9} fill="#f6c453" opacity={0.7} />
      <circle cx={mx} cy={ey} r={7} fill="#5fa0e0" opacity={0.7} />
      <path d={`M ${mx} ${ey - 46} A 46 46 0 0 1 ${mx + 46 * Math.sin(Math.atan2(230, ey - my))} ${ey - 46 * Math.cos(Math.atan2(230, ey - my))}`} fill="none" stroke="#f2b35a" strokeWidth={3} opacity={0.35 + 0.3 * Math.sin(rad)} />
    </svg>
  );
};
