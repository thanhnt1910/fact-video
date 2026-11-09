import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, GY, clamp01} from '../lib/theme';

const LORA = 'Lora, Georgia, serif';

/** Người que đội mũ (Thales), cao 80 điểm ảnh. walking: chân tay đung đưa. */
export const WALKER_H = 100;
export const Walker: React.FC<{x: number; dir?: 1 | -1; walking?: boolean; p?: number; staff?: boolean; shadowLen?: number}> = ({x, dir = -1, walking = false, p = 1, staff = false, shadowLen = 0}) => {
  const f = useCurrentFrame();
  const ph = walking ? f * 0.34 : 0;
  const top = GY - 80;
  const hip = top + 54;
  const a = walking ? Math.sin(ph) * 0.6 : 0.22;
  const bob = walking ? -Math.abs(Math.sin(ph)) * 2.5 : 0;
  const leg = (ang: number) => ({x: x + dir * Math.sin(ang) * 26, y: hip + Math.cos(ang) * 26});
  const arm = (ang: number) => ({x: x + dir * Math.sin(ang) * 22, y: top + 32 + Math.cos(ang) * 22});
  const l1 = leg(a);
  const l2 = leg(-a);
  const a1 = arm(walking ? -a * 0.9 : -0.35);
  const a2 = arm(walking ? a * 0.9 : 0.35);
  return (
    <g opacity={clamp01(p * 2)}>
      {shadowLen > 0 && <line x1={x} y1={GY} x2={x + shadowLen} y2={GY} stroke={C.amber} strokeWidth={13} opacity={0.9} />}
      <g transform={`translate(${x} ${GY}) scale(${WALKER_H / 80}) translate(${-x} ${-GY}) translate(0 ${bob})`} stroke={C.cream} strokeWidth={5} strokeLinecap="round" fill="none">
        <circle cx={x} cy={top + 11} r={11} fill={C.bg2} />
        <path d={`M${x - 10} ${top + 1} Q${x} ${top - 12} ${x + 10} ${top + 1}`} stroke={C.amber} strokeWidth={5} />
        <line x1={x - 17} y1={top + 1} x2={x + 17} y2={top + 1} stroke={C.amber} strokeWidth={4} />
        <line x1={x} y1={top + 22} x2={x} y2={hip} />
        <line x1={x} y1={hip} x2={l1.x} y2={Math.min(GY, l1.y)} />
        <line x1={x} y1={hip} x2={l2.x} y2={Math.min(GY, l2.y)} />
        <line x1={x} y1={top + 32} x2={a1.x} y2={a1.y} />
        <line x1={x} y1={top + 32} x2={a2.x} y2={a2.y} />
        {staff && <line x1={x + dir * 24} y1={GY - 4} x2={x + dir * 24} y2={top + 6} stroke={C.amber} strokeWidth={6} />}
      </g>
    </g>
  );
};

/** Lạc đà có người cưỡi, quay mặt dir (1 = sang phải). s = tỉ lệ. */
export const Stick2: React.FC<{x: number; h: number; p?: number}> = ({x, h, p = 1}) => (
  <line x1={x} y1={GY} x2={x} y2={GY - h * clamp01(p)} stroke={C.amber} strokeWidth={8} strokeLinecap="round" />
);

export const Camel: React.FC<{x: number; dir?: 1 | -1; s?: number; phase0?: number}> = ({x, dir = -1, s = 0.9, phase0 = 0}) => {
  const f = useCurrentFrame();
  const ph = f * 0.22 + phase0;
  const bob = -Math.abs(Math.sin(ph)) * 2.5;
  const hips = [-46, -30, 26, 38];
  const offs = [0, Math.PI, Math.PI * 0.5, Math.PI * 1.5];
  return (
    <g transform={`translate(${x} ${GY}) scale(${dir * s} ${s})`}>
      <g transform={`translate(0 ${bob})`} stroke={C.cream} strokeWidth={4.5} strokeLinecap="round" strokeLinejoin="round">
        {hips.map((hx, i) => {
          const o = Math.sin(ph + offs[i]) * 13;
          const lift = Math.max(0, Math.cos(ph + offs[i])) * 6;
          return <line key={i} x1={hx} y1={-40} x2={hx + o} y2={-lift - bob} fill="none" />;
        })}
        <path d="M-58 -42 Q-58 -62 -42 -62 Q-34 -86 -24 -62 Q-12 -90 2 -62 Q34 -62 44 -50 L44 -42 Q-10 -34 -58 -42 Z" fill={C.bg2} />
        <path d="M36 -56 Q62 -60 60 -88" fill="none" />
        <path d="M56 -92 Q62 -102 76 -96 L82 -90 Q72 -84 60 -86 Z" fill={C.bg2} />
        <line x1={-18} y1={-76} x2={-18} y2={-98} />
        <circle cx={-18} cy={-108} r={8} fill={C.bg2} />
        <path d="M-27 -108 Q-18 -122 -9 -108" fill="none" stroke={C.amber} />
        <path d="M-18 -92 L-34 -78 L-4 -78 Z" fill={C.amber} opacity={0.5} stroke="none" />
      </g>
    </g>
  );
};

/** Đám mây suy nghĩ (viền lượn sóng) với đuôi bong bóng về phía đầu nhân vật. */
export const Cloud: React.FC<{cx: number; cy: number; rx: number; ry: number; p: number; tail?: [number, number]; children?: React.ReactNode}> = ({cx, cy, rx, ry, p, tail, children}) => {
  const n = 12;
  const pts = Array.from({length: n}).map((_, i) => {
    const th = (i / n) * Math.PI * 2;
    return [cx + rx * Math.cos(th), cy + ry * Math.sin(th)];
  });
  const chord = (2 * Math.PI * Math.sqrt((rx * rx + ry * ry) / 2)) / n;
  const r = chord * 0.62;
  let d = `M${pts[0][0]} ${pts[0][1]}`;
  for (let i = 1; i <= n; i++) {
    const q = pts[i % n];
    d += ` A${r} ${r} 0 0 1 ${q[0]} ${q[1]}`;
  }
  const o = clamp01(p * 2);
  const k = 0.6 + 0.4 * clamp01(p);
  return (
    <g opacity={o}>
      {tail &&
        [0.2, 0.45, 0.7].map((t, i) => {
          const sx = cx - rx * 0.4;
          const sy = cy + ry;
          const x = sx + (tail[0] - sx) * t;
          const y = sy + (tail[1] - sy) * t;
          const rad = 16 - i * 4.5;
          return <circle key={i} cx={x} cy={y} r={rad} fill={C.bg2} stroke={C.cream} strokeWidth={3.5} opacity={clamp01(p * 3 - (2 - i) * 0.4)} />;
        })}
      <g transform={`translate(${cx} ${cy}) scale(${k}) translate(${-cx} ${-cy})`}>
        <path d={d + ' Z'} fill={C.bg2} fillOpacity={0.94} stroke={C.cream} strokeWidth={4} strokeLinejoin="round" />
        {children}
      </g>
    </g>
  );
};

export const Clock: React.FC<{x: number; y: number; hour: number; o?: number; r?: number}> = ({x, y, hour, o = 1, r = 58}) => {
  const ha = (hour % 12) * 30;
  const ma = (hour % 1) * 360;
  return (
    <g opacity={o} transform={`translate(${x} ${y})`}>
      <circle r={r} fill={C.bg2} stroke={C.cream} strokeWidth={4} />
      {Array.from({length: 12}).map((_, i) => (
        <line key={i} x1={0} y1={-r + 6} x2={0} y2={-r + (i % 3 === 0 ? 17 : 11)} stroke={C.cream} strokeWidth={i % 3 === 0 ? 4 : 2.5} transform={`rotate(${i * 30})`} />
      ))}
      <line x1={0} y1={0} x2={0} y2={-r * 0.78} stroke={C.cream} strokeWidth={3} strokeLinecap="round" transform={`rotate(${ma})`} />
      <line x1={0} y1={0} x2={0} y2={-r * 0.52} stroke={C.amber} strokeWidth={6} strokeLinecap="round" transform={`rotate(${ha})`} />
      <circle r={5} fill={C.amber} />
    </g>
  );
};

/** Cung góc tại điểm chạm đất (tx, GY): giữa mặt đất (bên trái) và tia nắng (lên trái) */
export const AngleArc: React.FC<{tx: number; e: number; r?: number; p: number; color?: string}> = ({tx, e, r = 50, p, color = C.amber}) => {
  const rad = (e * Math.PI) / 180;
  return (
    <path
      d={`M${tx - r} ${GY} A${r} ${r} 0 0 1 ${tx - r * Math.cos(rad)} ${GY - r * Math.sin(rad)}`}
      fill="none"
      stroke={color}
      strokeWidth={5}
      strokeLinecap="round"
      pathLength={1}
      strokeDasharray="1 1"
      strokeDashoffset={1 - clamp01(p)}
    />
  );
};

/** Nhìn từ trên xuống: đáy vuông, các vòng đá, tâm và mũi tên nửa cạnh đáy */
export const PlanView: React.FC<{cx: number; cy: number; side: number; arrowP: number}> = ({cx, cy, side, arrowP}) => {
  const h = side / 2;
  return (
    <g fill="none" stroke={C.cream} strokeWidth={3.5}>
      {[1, 0.72, 0.44, 0.17].map((k, i) => (
        <rect key={i} x={cx - h * k} y={cy - h * k} width={side * k} height={side * k} opacity={i === 0 ? 1 : 0.5} />
      ))}
      <line x1={cx - h} y1={cy - h} x2={cx + h} y2={cy + h} opacity={0.35} />
      <line x1={cx + h} y1={cy - h} x2={cx - h} y2={cy + h} opacity={0.35} />
      <circle cx={cx} cy={cy} r={8} fill={C.amber} stroke="none" />
      <line x1={cx} y1={cy} x2={cx + h * arrowP} y2={cy} stroke={C.amber} strokeWidth={7} strokeLinecap="round" />
      {arrowP > 0.95 && <circle cx={cx + h} cy={cy} r={8} fill={C.amber} stroke="none" />}
    </g>
  );
};

export const Dunes: React.FC<{o?: number}> = ({o = 1}) => (
  <g opacity={o}>
    <path d="M0 760 C 200 705, 430 690, 650 735 S 1110 705, 1400 738 S 1760 708, 1920 738 L1920 760 L0 760 Z" fill={C.cream} opacity={0.06} />
    <path d="M0 760 C 260 728, 560 720, 820 748 S 1400 726, 1920 752 L1920 760 L0 760 Z" fill={C.cream} opacity={0.06} />
  </g>
);

export const Ladder: React.FC<{cx: number; cy: number}> = ({cx, cy}) => (
  <g stroke={C.cream} strokeWidth={5} strokeLinecap="round">
    <line x1={cx - 15} y1={cy - 62} x2={cx - 15} y2={cy + 62} />
    <line x1={cx + 15} y1={cy - 62} x2={cx + 15} y2={cy + 62} />
    {[-40, -16, 8, 32, 56].map((dy) => (
      <line key={dy} x1={cx - 15} y1={cy + dy} x2={cx + 15} y2={cy + dy} />
    ))}
  </g>
);

export {LORA};
