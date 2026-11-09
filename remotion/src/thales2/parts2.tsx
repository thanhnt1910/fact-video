import React from 'react';
import {useCurrentFrame} from 'remotion';
import {APEX_Y, C, GY, PB, PH, PX, clamp01} from '../lib/theme';

const LORA = 'Lora, Georgia, serif';

export const Stick2: React.FC<{x: number; h: number; p?: number}> = ({x, h, p = 1}) => (
  <g opacity={clamp01(p * 3)}>
    <line x1={x} y1={GY} x2={x} y2={GY - h * clamp01(p)} stroke={C.amber} strokeWidth={9} strokeLinecap="round" />
    <line x1={x - 2} y1={GY} x2={x - 2} y2={GY - h * clamp01(p)} stroke="#ffe3a8" strokeWidth={2.5} strokeLinecap="round" opacity={0.7} />
  </g>
);

export const WALKER_H = 135;

const SKIN = '#d9a273';
const ROBE = '#ecd9ab';
const ROBE_D = '#b9955f';
const BROWN = '#6b4a32';

/** Thales: áo choàng Hy Lạp, râu bạc, mũ rộng vành, sandal. Thiết kế trên khung cao 80, phóng theo WALKER_H. */
export const Walker: React.FC<{x: number; dir?: 1 | -1; walking?: boolean; p?: number; staff?: boolean; shadowLen?: number; robe?: string; size?: number; noShadow?: boolean; hat?: boolean; speed?: number}> = ({x, dir = -1, walking = false, p = 1, staff = false, shadowLen = 0, robe = ROBE, size = WALKER_H, noShadow = false, hat = true, speed = 1}) => {
  const f = useCurrentFrame();
  // Người que có mũ: đầu tròn, thân một nét, tay chân gập ở khuỷu và đầu gối, nhịp bước mượt.
  const ph = walking ? f * 0.3 * speed : 0;
  const top = GY - 80;
  const bob = walking ? -Math.abs(Math.sin(ph)) * 2 : 0;
  const lean = walking ? dir * 2 : 0;
  const hipY = GY - 38;
  const shY = top + 27;
  const headY = top + 15;
  const leg = (o: number) => {
    const sw = walking ? Math.sin(ph + o) : o === 0 ? 1 : -1;
    const fx = x + dir * sw * (walking ? 13 : 6);
    const fy = GY - (walking ? Math.max(0, Math.cos(ph + o)) * 7 : 0);
    const kx = (x + fx) / 2 + dir * 5;
    const ky = (hipY + fy) / 2 - 1;
    return `M${x} ${hipY} L${kx} ${ky} L${fx} ${fy}`;
  };
  const arm = (o: number, front: boolean) => {
    if (front && staff) return `M${x} ${shY} L${x + dir * 14} ${shY + 12} L${x + dir * 24} ${top + 52}`;
    const sw = walking ? Math.sin(ph + o) : front ? 0.6 : -0.3;
    const hx = x + dir * sw * 12;
    const hy = shY + 24 - Math.abs(sw) * 2;
    return `M${x} ${shY} L${(x + hx) / 2 + dir * 3} ${shY + 12} L${hx} ${hy}`;
  };
  return (
    <g opacity={clamp01(p * 2)}>
      {shadowLen > 0 && <line x1={x} y1={GY} x2={x + shadowLen} y2={GY} stroke={C.amber} strokeWidth={14} opacity={0.9} />}
      <g transform={`translate(${x} ${GY}) scale(${size / 80}) translate(${-x} ${-GY})`}>
        {!noShadow && <ellipse cx={x} cy={GY} rx={20} ry={3} fill="#000" opacity={0.28} />}
        <g transform={`translate(0 ${bob})`} fill="none" stroke={robe} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round">
          {staff && (
            <g>
              <line x1={x + dir * 24} y1={GY - 1} x2={x + dir * 24} y2={top - 20} stroke={BROWN} strokeWidth={5} />
              <circle cx={x + dir * 24} cy={top - 21} r={4.2} fill="#8a5a33" stroke="none" />
            </g>
          )}
          <path d={arm(Math.PI, false)} opacity={0.75} />
          <path d={leg(Math.PI)} opacity={0.75} />
          <line x1={x + lean} y1={shY - 2} x2={x} y2={hipY} />
          <path d={leg(0)} />
          <path d={arm(0, true)} />
          <circle cx={x + lean} cy={headY} r={8.5} fill={robe} stroke="none" />
          {hat && (
            <g stroke="none">
              <ellipse cx={x + lean} cy={headY - 6} rx={14} ry={3.6} fill={C.amber} />
              <path d={`M${x + lean - 8} ${headY - 7} Q${x + lean} ${headY - 21} ${x + lean + 8} ${headY - 7} Z`} fill={C.amberDeep} />
            </g>
          )}
        </g>
      </g>
    </g>
  );
};

/** Lạc đà một bướu có người cưỡi, quay mặt dir (1 = sang phải). */
export const Camel: React.FC<{x: number; dir?: 1 | -1; s?: number; phase0?: number}> = ({x, dir = -1, s = 1.1, phase0 = 0}) => {
  const f = useCurrentFrame();
  const ph = f * 0.2 + phase0;
  const bob = -Math.abs(Math.sin(ph)) * 2.2;
  const sway = Math.sin(ph) * 1.6;
  const leg = (hx: number, o: number, back: boolean) => {
    const sw = Math.sin(ph + o) * 14;
    const lf = Math.max(0, Math.cos(ph + o)) * 7;
    const kx = hx + sw * 0.35;
    const fx = hx + sw;
    const col = back ? '#4e2f1b' : '#6a3f23';
    return (
      <g key={hx}>
        <polyline points={`${hx},-44 ${kx},-23 ${fx},${-lf - bob - 3}`} fill="none" stroke="#e8c98f" strokeWidth={11.5} strokeLinecap="round" strokeLinejoin="round" opacity={0.85} />
        <polyline points={`${hx},-44 ${kx},-23 ${fx},${-lf - bob - 3}`} fill="none" stroke={col} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
        <ellipse cx={fx + 1.5} cy={-lf - bob - 1} rx={6.5} ry={3} fill="#2d1a0e" />
      </g>
    );
  };
  return (
    <g transform={`translate(${x} ${GY}) scale(${dir * s} ${s})`}>
      <ellipse cx={0} cy={1} rx={78} ry={5.5} fill="#000" opacity={0.3} />
      {[0, 1, 2, 3].map((i) => (
        <circle key={i} cx={-82 - i * 30} cy={-5 - ((i * 7) % 11)} r={5 + i * 3.2} fill={C.cream} opacity={0.17 - i * 0.04} />
      ))}
      <g transform={`translate(0 ${bob})`}>
        {leg(-46, 0, true)}
        {leg(32, Math.PI, true)}
        <path d={`M-64 -50 Q${-76 + sway} -34 ${-72 + sway * 2} -16`} fill="none" stroke="#4e2f1b" strokeWidth={4.5} strokeLinecap="round" />
        <ellipse cx={-72 + sway * 2} cy={-14} rx={3.6} ry={6} fill="#3a2314" />
        <path
          d="M-66 -50 C-72 -68 -56 -84 -40 -91 C-28 -104 -4 -99 8 -80 C16 -68 24 -66 31 -73 C45 -83 50 -104 55 -121 C61 -130 78 -130 86 -121 C93 -117 95 -110 88 -106 C82 -104 70 -104 65 -99 C61 -90 63 -70 57 -54 C51 -42 30 -38 10 -41 C-20 -37 -50 -37 -66 -50 Z"
          fill="#8a5330"
          stroke="#f0d9a2"
          strokeWidth={3}
          strokeLinejoin="round"
        />
        <path d="M-60 -52 C-40 -42 0 -44 30 -50 C45 -54 54 -62 58 -76" fill="none" stroke="#5b341d" strokeWidth={6} opacity={0.45} strokeLinecap="round" />
        <path d="M54 -121 C60 -128 74 -128 80 -122" fill="none" stroke="#b97b49" strokeWidth={3} opacity={0.8} strokeLinecap="round" />
        <path d="M63 -128 L66 -139 L70 -128 Z" fill="#8a5330" stroke="#f0d9a2" strokeWidth={2} strokeLinejoin="round" />
        <circle cx={77} cy={-119} r={2.6} fill="#1d110a" />
        <circle cx={90} cy={-109} r={1.5} fill="#1d110a" />
        <path d="M-44 -90 C-30 -102 -8 -97 4 -82 L8 -56 L-46 -62 Z" fill="#b5502a" stroke="#f0c070" strokeWidth={2} strokeLinejoin="round" />
        <path d="M-45 -76 L7 -72 M-46 -66 L7 -62" stroke="#f6d98c" strokeWidth={3} fill="none" />
        {[-40, -30, -20, -10, 0].map((fx) => (
          <line key={fx} x1={fx - 3} y1={-61} x2={fx - 3 + sway * 0.3} y2={-53} stroke="#f6d98c" strokeWidth={2.2} strokeLinecap="round" />
        ))}
        <path d="M-30 -96 L-9 -96 L-12 -124 L-27 -124 Z" fill="#efe2c0" stroke="#fff3d6" strokeWidth={1.5} strokeLinejoin="round" />
        <path d="M-30 -102 L-9 -96" stroke={C.amberDeep} strokeWidth={4} />
        <path d="M-22 -100 C-14 -92 -6 -84 2 -72" fill="none" stroke="#efe2c0" strokeWidth={9} strokeLinecap="round" />
        <line x1={-18} y1={-116} x2={4} y2={-106} stroke="#efe2c0" strokeWidth={6.5} strokeLinecap="round" />
        <path d="M3 -106 Q40 -112 86 -112" fill="none" stroke="#5b341d" strokeWidth={2} />
        <circle cx={-19} cy={-132} r={8.2} fill="#a8683f" />
        <ellipse cx={-19} cy={-139} rx={11} ry={6.5} fill="#f6ead0" stroke="#d8c49a" strokeWidth={1.2} />
        <path d="M-27 -137 Q-33 -128 -29 -118" fill="none" stroke="#f6ead0" strokeWidth={4.5} strokeLinecap="round" />
        <circle cx={-15} cy={-132} r={1.3} fill="#2b1a10" />
        {leg(-30, Math.PI * 0.5, false)}
        {leg(44, Math.PI * 1.5, false)}
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

export const Defs2: React.FC = () => (
  <defs>
    <linearGradient id="pyL" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0%" stopColor="#f5c071" stopOpacity="0.62" />
      <stop offset="100%" stopColor="#b8742e" stopOpacity="0.34" />
    </linearGradient>
    <linearGradient id="pyR" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stopColor="#3b2617" stopOpacity="0.95" />
      <stop offset="100%" stopColor="#150d08" stopOpacity="0.95" />
    </linearGradient>
    <linearGradient id="haze" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stopColor="#f2b35a" stopOpacity="0" />
      <stop offset="100%" stopColor="#f2b35a" stopOpacity="0.16" />
    </linearGradient>
  </defs>
);

export const Dunes: React.FC<{o?: number}> = ({o = 1}) => (
  <g opacity={o}>
    <rect x={0} y={GY - 300} width={1920} height={300} fill="url(#haze)" />
    <path d="M0 760 C 200 705, 430 690, 650 735 S 1110 705, 1400 738 S 1760 708, 1920 738 L1920 760 L0 760 Z" fill={C.cream} opacity={0.06} />
    <path d="M0 760 C 260 728, 560 720, 820 748 S 1400 726, 1920 752 L1920 760 L0 760 Z" fill={C.cream} opacity={0.07} />
    <path d="M150 742 L 215 668 L 280 742 Z" fill={C.cream} opacity={0.07} />
    <path d="M52 746 L 100 702 L 148 746 Z" fill={C.cream} opacity={0.06} />
  </g>
);

/** Kim tự tháp có mặt sáng, mặt tối, các lớp đá; vẽ dần bằng nét viền */
export const Pyramid2: React.FC<{p: number; axis?: boolean}> = ({p, axis = false}) => {
  const fadeIn = clamp01((p - 0.5) / 0.5);
  const rows = Array.from({length: 11}).map((_, i) => {
    const y = APEX_Y + (PH * (i + 1)) / 12;
    return {y, hw: (PB * (y - APEX_Y)) / PH};
  });
  return (
    <g>
      <ellipse cx={PX} cy={GY + 3} rx={PB + 24} ry={6} fill="#000" opacity={0.3 * fadeIn} />
      <path d={`M${PX - PB} ${GY} L${PX} ${APEX_Y} L${PX} ${GY} Z`} fill="url(#pyL)" opacity={fadeIn} />
      <path d={`M${PX} ${APEX_Y} L${PX + PB} ${GY} L${PX} ${GY} Z`} fill="url(#pyR)" opacity={fadeIn} />
      {rows.map((r, i) => (
        <g key={i} opacity={fadeIn}>
          <line x1={PX - r.hw} y1={r.y} x2={PX} y2={r.y} stroke="#ffe0a0" strokeWidth={1.8} opacity={0.3} />
          <line x1={PX} y1={r.y} x2={PX + r.hw} y2={r.y} stroke={C.amber} strokeWidth={1.6} opacity={0.18} />
        </g>
      ))}
      <path d={`M${PX - PB} ${GY} L${PX} ${APEX_Y} L${PX + PB} ${GY} Z`} fill="none" stroke={C.amber} strokeWidth={4.5} strokeLinejoin="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - p} />
      <line x1={PX} y1={APEX_Y} x2={PX} y2={GY} stroke="#ffe0a0" strokeWidth={1.5} opacity={0.3 * fadeIn} />
      {axis && <line x1={PX} y1={APEX_Y} x2={PX} y2={GY} stroke={C.cream} strokeWidth={3} strokeDasharray="10 12" opacity={0.5 * fadeIn} />}
    </g>
  );
};

/** Vài con chim bay ngang bầu trời */
export const Birds: React.FC<{o?: number}> = ({o = 0.5}) => {
  const f = useCurrentFrame();
  return (
    <g opacity={o} fill="none" stroke={C.cream} strokeWidth={3} strokeLinecap="round">
      {[0, 1, 2].map((i) => {
        const x = ((220 + i * 150 + 44 * (f / 30)) % 2300) - 150;
        const y = 190 + i * 38 + Math.sin(f * 0.04 + i * 2) * 10;
        const w = Math.sin(f * 0.32 + i * 1.7) * 7;
        return <path key={i} d={`M${x - 13} ${y + 2} Q${x - 6} ${y - w - 4} ${x} ${y} Q${x + 6} ${y - w - 4} ${x + 13} ${y + 2}`} />;
      })}
    </g>
  );
};

/** Cây cọ lay nhẹ */
export const Palm: React.FC<{x: number; h?: number}> = ({x, h = 190}) => {
  const f = useCurrentFrame();
  const sw = Math.sin(f * 0.045) * 4;
  const tx = x + 14 + sw * 0.3;
  const ty = GY - h;
  return (
    <g>
      <path d={`M${x} ${GY} Q${x + 24} ${GY - h * 0.5} ${tx} ${ty}`} fill="none" stroke="#6b4a32" strokeWidth={11} strokeLinecap="round" />
      <path d={`M${x - 2} ${GY} Q${x + 22} ${GY - h * 0.5} ${tx - 2} ${ty}`} fill="none" stroke="#a87c4f" strokeWidth={3} strokeLinecap="round" opacity={0.7} />
      {[-70, -35, 0, 35, 70, 110, -110].map((a, i) => {
        const r = ((a + sw * 1.5) * Math.PI) / 180;
        const len = 76;
        const ex = tx + Math.sin(r) * len;
        const ey = ty - Math.cos(r) * len * 0.5 + (Math.abs(a) > 60 ? 38 : 4);
        return <path key={i} d={`M${tx} ${ty} Q${tx + Math.sin(r) * len * 0.5} ${ty - 34} ${ex} ${ey}`} fill="none" stroke="#a8a35c" strokeWidth={5.5} strokeLinecap="round" />;
      })}
    </g>
  );
};

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

/** Đặt vật có chân ở GY (vẽ với x=0) tại điểm (x, y), xoay rot độ quanh chân */
export const At: React.FC<{x: number; y: number; rot?: number; children: React.ReactNode}> = ({x, y, rot = 0, children}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot}) translate(0 ${-GY})`}>{children}</g>
);

export const Cross: React.FC<{x: number; y: number; r?: number; p?: number; color?: string}> = ({x, y, r = 34, p = 1, color = '#ff8a5c'}) => (
  <g stroke={color} strokeWidth={9} strokeLinecap="round" opacity={clamp01(p * 3)}>
    <line x1={x - r} y1={y - r} x2={x - r + 2 * r * clamp01(p)} y2={y - r + 2 * r * clamp01(p)} />
    <line x1={x + r} y1={y - r} x2={x + r - 2 * r * clamp01(p)} y2={y - r + 2 * r * clamp01(p)} />
  </g>
);

export const Check: React.FC<{x: number; y: number; r?: number; p?: number}> = ({x, y, r = 34, p = 1}) => (
  <polyline
    points={`${x - r} ${y} ${x - r * 0.3} ${y + r * 0.7} ${x + r} ${y - r * 0.8}`}
    fill="none"
    stroke="#9bd68a"
    strokeWidth={10}
    strokeLinecap="round"
    strokeLinejoin="round"
    pathLength={1}
    strokeDasharray="1 1"
    strokeDashoffset={1 - clamp01(p)}
  />
);

export const RopeCoil: React.FC<{cx: number; cy: number}> = ({cx, cy}) => (
  <g fill="none" stroke="#d9b27a" strokeWidth={6} strokeLinecap="round">
    <circle cx={cx} cy={cy} r={36} />
    <circle cx={cx} cy={cy} r={24} />
    <circle cx={cx} cy={cy} r={12} />
    <path d={`M${cx + 36} ${cy} q30 -10 46 -40`} />
  </g>
);
