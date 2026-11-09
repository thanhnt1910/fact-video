import React from 'react';
import {useCurrentFrame} from 'remotion';
import {APEX_Y, C, GY, PB, PH, PX, clamp01, seg} from '../lib/theme';

const LORA = "Lora, Georgia, serif";

/** Định nghĩa gradient dùng chung, đặt trong mỗi <svg> */
export const Defs: React.FC = () => (
  <defs>
    <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stopColor={C.amber} stopOpacity="0.35" />
      <stop offset="100%" stopColor={C.amber} stopOpacity="0" />
    </radialGradient>
    <linearGradient id="flameG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stopColor="#ffd98a" />
      <stop offset="100%" stopColor="#e8913a" />
    </linearGradient>
  </defs>
);

export const Ground: React.FC<{p: number}> = ({p}) => (
  <g opacity={clamp01(p * 3)}>
    <line x1={60} y1={GY} x2={60 + (1860 - 60) * p} y2={GY} stroke={C.cream} strokeWidth={3} opacity={0.45} />
    <line x1={60} y1={GY + 16} x2={60 + (1860 - 60) * p} y2={GY + 16} stroke={C.cream} strokeWidth={14} strokeDasharray="3 27" opacity={0.18} />
  </g>
);

export const Pyramid: React.FC<{p: number; axis?: boolean}> = ({p, axis = true}) => {
  const rows = Array.from({length: 8}).map((_, i) => {
    const y = APEX_Y + (PH * (i + 1)) / 9;
    const hw = (PB * (y - APEX_Y)) / PH;
    return {y, hw};
  });
  const fadeIn = clamp01((p - 0.55) / 0.45);
  return (
    <g>
      <path d={`M${PX} ${APEX_Y} L${PX + PB} ${GY} L${PX} ${GY} Z`} fill="#000" opacity={0.3 * fadeIn} />
      <path
        d={`M${PX - PB} ${GY} L${PX} ${APEX_Y} L${PX + PB} ${GY} Z`}
        fill="none"
        stroke={C.amber}
        strokeWidth={4.5}
        strokeLinejoin="round"
        pathLength={1}
        strokeDasharray="1 1"
        strokeDashoffset={1 - p}
      />
      {rows.map((r, i) => (
        <line key={i} x1={PX - r.hw} y1={r.y} x2={PX + r.hw} y2={r.y} stroke={C.amber} strokeWidth={2.5} opacity={0.38 * fadeIn} />
      ))}
      {axis && <line x1={PX} y1={APEX_Y} x2={PX} y2={GY} stroke={C.cream} strokeWidth={3} strokeDasharray="10 12" opacity={0.4 * fadeIn} />}
    </g>
  );
};

export const Sun: React.FC<{x: number; y: number; p?: number}> = ({x, y, p = 1}) => {
  const f = useCurrentFrame();
  return (
    <g transform={`translate(${x} ${y})`} opacity={clamp01(p)}>
      <circle r={150} fill="url(#sunGlow)" />
      <g transform={`scale(${0.4 + 0.6 * clamp01(p)})`}>
        <circle r={34} fill="none" stroke={C.amber} strokeWidth={5} />
        <circle r={22} fill={C.amber} opacity={0.4} />
        <g transform={`rotate(${f * 0.35})`} stroke={C.amber} strokeWidth={5} strokeLinecap="round">
          {Array.from({length: 12}).map((_, i) => (
            <line key={i} x1={50} y1={0} x2={70} y2={0} transform={`rotate(${i * 30})`} />
          ))}
        </g>
      </g>
    </g>
  );
};

/** Tia nắng: nét đứt chạy dần từ (x1,y1) tới (x2,y2) */
export const Ray: React.FC<{x1: number; y1: number; x2: number; y2: number; p: number; opacity?: number}> = ({x1, y1, x2, y2, p, opacity = 0.75}) => {
  const f = useCurrentFrame();
  return (
    <line
      x1={x1}
      y1={y1}
      x2={x1 + (x2 - x1) * p}
      y2={y1 + (y2 - y1) * p}
      stroke={C.amber}
      strokeWidth={3.5}
      strokeLinecap="round"
      strokeDasharray="16 12"
      strokeDashoffset={-f * 0.9}
      opacity={opacity * clamp01(p * 4)}
    />
  );
};

/** Đoạn bóng trên mặt đất, lớn dần từ x1 tới x2 */
export const Shadow: React.FC<{x1: number; x2: number; p: number; hot?: boolean}> = ({x1, x2, p, hot}) => (
  <line x1={x1} y1={GY} x2={x1 + (x2 - x1) * p} y2={GY} stroke={hot ? C.amber : C.amberDeep} strokeWidth={13} opacity={hot ? 0.9 : 0.55} />
);

/** Người que (Thales), cao 80 điểm ảnh, tay cầm gậy */
export const Figure: React.FC<{x: number; p?: number}> = ({x, p = 1}) => {
  const top = GY - 80;
  return (
    <g opacity={clamp01(p * 2)} stroke={C.cream} strokeWidth={5} strokeLinecap="round" fill="none">
      <circle cx={x} cy={top + 11} r={11} fill={C.bg2} />
      <line x1={x} y1={top + 22} x2={x} y2={top + 54} />
      <line x1={x} y1={top + 54} x2={x - 12} y2={GY} />
      <line x1={x} y1={top + 54} x2={x + 12} y2={GY} />
      <line x1={x} y1={top + 32} x2={x - 16} y2={top + 48} />
      <line x1={x} y1={top + 32} x2={x + 20} y2={top + 40} />
      <line x1={x + 22} y1={GY} x2={x + 22} y2={top - 6} stroke={C.amber} strokeWidth={6} />
    </g>
  );
};

/** Cây gậy dựng đứng cao 80 điểm ảnh */
export const Stick: React.FC<{x: number; p?: number}> = ({x, p = 1}) => (
  <line x1={x} y1={GY} x2={x} y2={GY - 80 * clamp01(p)} stroke={C.amber} strokeWidth={7} strokeLinecap="round" />
);

export const Txt: React.FC<{x: number; y: number; size?: number; color?: string; anchor?: 'start' | 'middle' | 'end'; opacity?: number; children: React.ReactNode; weight?: number}> = ({
  x,
  y,
  size = 44,
  color = C.cream,
  anchor = 'middle',
  opacity = 1,
  children,
  weight = 400,
}) => (
  <text x={x} y={y} textAnchor={anchor} fontFamily={LORA} fontStyle="italic" fontWeight={weight} fontSize={size} fill={color} opacity={opacity}>
    {children}
  </text>
);

/** Thước đo ngang. label đặt dưới đường (below) hoặc trên đường */
export const DimH: React.FC<{x1: number; x2: number; y: number; label: string; p: number; color?: string; size?: number; below?: boolean}> = ({x1, x2, y, label, p, color = C.cream, size = 40, below = true}) => {
  const xe = x1 + (x2 - x1) * clamp01(p);
  const o = clamp01(p * 3);
  return (
    <g opacity={o} stroke={color} strokeWidth={3} strokeLinecap="round">
      <line x1={x1} y1={y} x2={xe} y2={y} />
      <line x1={x1} y1={y - 10} x2={x1} y2={y + 10} />
      <line x1={xe} y1={y - 10} x2={xe} y2={y + 10} />
      <g stroke="none">
        <Txt x={(x1 + x2) / 2} y={below ? y + size + 12 : y - 16} size={size} color={color} opacity={clamp01((p - 0.5) * 2)}>
          {label}
        </Txt>
      </g>
    </g>
  );
};

/** Thước đo dọc (đi từ y1 lên y2), nhãn bên trái */
export const DimV: React.FC<{x: number; y1: number; y2: number; label: string; p: number; color?: string; size?: number}> = ({x, y1, y2, label, p, color = C.cream, size = 40}) => {
  const ye = y1 + (y2 - y1) * clamp01(p);
  const o = clamp01(p * 3);
  return (
    <g opacity={o} stroke={color} strokeWidth={3} strokeLinecap="round">
      <line x1={x} y1={y1} x2={x} y2={ye} />
      <line x1={x - 10} y1={y1} x2={x + 10} y2={y1} />
      <line x1={x - 10} y1={ye} x2={x + 10} y2={ye} />
      <g stroke="none">
        <Txt x={x - 18} y={(y1 + y2) / 2 + size / 3} size={size} color={color} anchor="end" opacity={clamp01((p - 0.5) * 2)}>
          {label}
        </Txt>
      </g>
    </g>
  );
};

export const FlameMark: React.FC<{width: number}> = ({width}) => (
  <svg width={width} height={(width * 470) / 300} viewBox="250 150 300 470">
    <Defs />
    <path d="M400 160 C 440 250, 540 320, 540 450 C 540 540, 480 610, 400 610 C 320 610, 260 540, 260 450 C 260 320, 360 250, 400 160 Z" fill="url(#flameG)" />
    <polyline points="330,455 385,510 478,385" fill="none" stroke={C.ink} strokeWidth={34} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export {seg};
