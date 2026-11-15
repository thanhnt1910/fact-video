import React from 'react';
import {useCurrentFrame} from 'remotion';

// Nền riêng video 17 (một mét dài bao nhiêu): giấy bản đồ cũ màu nâu sẫm, lưới kinh tuyến – vĩ tuyến rất mờ.
// Dấu ấn riêng: một tam giác nhỏ ở mép trái tự vẽ từng cạnh rồi xóa, lặp lại mỗi 3 giây (gợi phép tam giác).
export const MmBackground: React.FC = () => {
  const f = useCurrentFrame();
  const t = (f % 90) / 90;
  const p = Math.min(1, t / 0.6);
  const o = t < 0.8 ? 0.85 : (1 - t) / 0.2 * 0.85;
  const per = 3 * 52;
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <radialGradient id="mmG" cx="0.5" cy="0.4" r="0.8">
          <stop offset="0" stopColor="#30281c" />
          <stop offset="1" stopColor="#1a150e" />
        </radialGradient>
      </defs>
      <rect width={1080} height={1920} fill="url(#mmG)" />
      {Array.from({length: 10}).map((_, i) => (
        <path key={'v' + i} d={`M ${60 + i * 108} 0 Q ${60 + i * 108 + (i - 4.5) * 18} 960 ${60 + i * 108} 1920`} fill="none" stroke="#c9a86a" strokeWidth={2} opacity={0.07} />
      ))}
      {Array.from({length: 14}).map((_, i) => (
        <line key={'h' + i} x1={0} y1={80 + i * 140} x2={1080} y2={80 + i * 140} stroke="#c9a86a" strokeWidth={2} opacity={0.06} />
      ))}
      <path d="M 44 470 L 80 470 L 62 430 Z" fill="none" stroke="#f2c14e" strokeWidth={4} strokeLinejoin="round" strokeDasharray={per} strokeDashoffset={per * (1 - p)} opacity={o} />
    </svg>
  );
};
