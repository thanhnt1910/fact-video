import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 28 (nhiệt độ Mặt Trời): bầu trời đêm sẫm, một dải phổ cầu vồng rất mờ ở đáy, tương phản thấp.
// Dấu ấn riêng: ở mép trái một thanh sắt nhỏ đổi màu đỏ sẫm, cam, trắng rồi nguội lại, lặp mãi.
const STOPS = ['#7a2418', '#d6542f', '#f0a040', '#fff1d0'];
const mix = (a: string, b: string, t: number) => {
  const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
  const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
  return `rgb(${pa.map((v, i) => Math.round(v + (pb[i] - v) * t)).join(',')})`;
};
export const NmBackground: React.FC = () => {
  const f = useCurrentFrame();
  const T = 200;
  const t = (f % T) / T;
  const h = t < 0.7 ? t / 0.7 : 1 - (t - 0.7) / 0.3;
  const k = h * 3;
  const i = Math.min(2, Math.floor(k));
  const col = mix(STOPS[i], STOPS[i + 1], k - i);
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="nmG" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#1a1830" />
          <stop offset="1" stopColor="#0f0e16" />
        </linearGradient>
        <linearGradient id="nmS" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stopColor="#8b2bd6" />
          <stop offset="0.25" stopColor="#2b6fd6" />
          <stop offset="0.5" stopColor="#3fc46a" />
          <stop offset="0.75" stopColor="#e8c52b" />
          <stop offset="1" stopColor="#e0402b" />
        </linearGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#nmG)" />
      <rect x={0} y={1720} width={1080} height={200} fill="url(#nmS)" opacity={0.08} />
      {[0, 1, 2, 3, 4, 5, 6].map((j) => (
        <circle key={j} cx={(j * 331 + 120) % 1000 + 40} cy={(j * 277 + 500) % 900 + 420} r={3} fill="#fff1d0" opacity={0.08 + 0.05 * Math.sin(f * 0.05 + j)} />
      ))}
      <rect x={30} y={700} width={26} height={300} rx={13} fill={col} opacity={0.38} />
      <circle cx={43} cy={850} r={30 + 20 * h} fill={col} opacity={0.08 + 0.1 * h} />
    </svg>
  );
};
