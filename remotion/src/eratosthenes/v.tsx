import React from 'react';
import {Img, staticFile, useCurrentFrame} from 'remotion';
import {C, clamp01, seg} from '../lib/theme';
import {Defs} from '../thales/parts';
import CAPS from './caps.json';

// Bộ phận hình cho khổ dọc 1080x1920.
export const VW = 1080;
export const VH = 1920;

export const VDefs: React.FC = () => (
  <defs>
    <radialGradient id="globeG" cx="38%" cy="32%" r="80%">
      <stop offset="0%" stopColor="#3f7a80" />
      <stop offset="100%" stopColor="#10272b" />
    </radialGradient>
    <radialGradient id="bgV" cx="50%" cy="38%" r="80%">
      <stop offset="0%" stopColor={C.bg1} />
      <stop offset="100%" stopColor={C.bg2} />
    </radialGradient>
    <pattern id="gridV" width="80" height="80" patternUnits="userSpaceOnUse">
      <path d="M80 0 L0 0 L0 80" fill="none" stroke={C.cream} strokeWidth="1.5" opacity="0.07" />
    </pattern>
  </defs>
);

export const VBackground: React.FC = () => (
  <svg width={VW} height={VH} viewBox={`0 0 ${VW} ${VH}`} style={{position: 'absolute', left: 0, top: 0}}>
    <VDefs />
    <rect width={VW} height={VH} fill="url(#bgV)" />
    <rect width={VW} height={VH} fill="url(#gridV)" />
    <rect x={24} y={24} width={VW - 48} height={VH - 48} rx={8} fill="none" stroke={C.cream} strokeWidth={2} opacity={0.14} />
  </svg>
);

/** Logo góc trên bên phải */
export const VHud: React.FC = () => (
  <div style={{position: 'absolute', right: 48, top: 40, display: 'flex', alignItems: 'center', gap: 16, opacity: 0.96}}>
    <Img src={staticFile('nguoi-giai-ma.png')} style={{width: 96, height: 96, borderRadius: 48, border: '3px solid #e9a84c'}} />
    <div style={{fontFamily: 'BeVN', fontWeight: 800, fontSize: 34, lineHeight: 1, color: C.cream}}>
      Người <span style={{color: C.amber}}>Giải Mã</span>
    </div>
  </div>
);

/** Phụ đề: nằm trong khoảng y 1180–1510, cách đáy hơn 400 điểm ảnh để không bị lớp chữ của Reels che */
export const splitWords = (text: string, max = 4): string[] => {
  const w = text.trim().split(/\s+/);
  const n = Math.ceil(w.length / max);
  const out: string[] = [];
  let i = 0;
  for (let k = 0; k < n; k++) {
    const take = Math.round((w.length - i) / (n - k));
    out.push(w.slice(i, i + take).join(' '));
    i += take;
  }
  return out;
};

/** Phụ đề ngắn: mỗi lần hiện tối đa 4 từ, mốc từng cụm tính từ giọng đọc thật (scripts/tao_phu_de.py -> caps.json) */
export const VCaptions: React.FC<{beats: {text: string; start: number; dur: number}[]; caps?: {text: string; start: number; end: number}[][]}> = ({beats, caps}) => {
  const f = useCurrentFrame();
  const bi = beats.findIndex((x) => f >= x.start && f < x.start + x.dur);
  const b = beats[bi];
  if (!b || !b.text) return null;
  const vi = beats.slice(0, bi).filter((x) => x.text).length;
  const items = (caps ?? (CAPS as {text: string; start: number; end: number}[][]))[vi];
  if (!items) return null;
  const t = (f - b.start) / 30;
  const c = items.find((x) => t >= x.start && t < x.end);
  if (!c) return null;
  const last = c === items[items.length - 1];
  const lf = f - b.start;
  const o = Math.min(seg(lf, c.start * 30, c.start * 30 + 2), last ? 1 - seg(lf, c.end * 30 - 3, c.end * 30) : 1);
  return (
    <div style={{position: 'absolute', left: 70, width: 940, top: 1330, height: 180, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: clamp01(Math.max(o, 0.0))}}>
      <div
        style={{
          fontFamily: 'BeVN',
          fontWeight: 800,
          fontSize: 68,
          lineHeight: 1.2,
          textAlign: 'center',
          color: '#fff',
          WebkitTextStroke: '10px #130c08',
          paintOrder: 'stroke fill',
        }}
      >
        {c.text.split('*').map((seg2, k) =>
          k % 2 ? (
            <span key={k} style={{color: C.amber, fontSize: '1.14em', WebkitTextStroke: '12px #130c08'}}>
              {seg2}
            </span>
          ) : (
            <span key={k}>{seg2}</span>
          ),
        )}
      </div>
    </div>
  );
};

export const Svg: React.FC<{children: React.ReactNode}> = ({children}) => (
  <svg width={VW} height={VH} viewBox={`0 0 ${VW} ${VH}`} style={{position: 'absolute', left: 0, top: 0}}>
    <Defs />
    <VDefs />
    {children}
  </svg>
);

/** Chữ nhãn (Lora nghiêng, có tiếng Việt) */
export const Lab: React.FC<{x: number; y: number; size?: number; color?: string; anchor?: 'start' | 'middle' | 'end'; o?: number; children: React.ReactNode; w?: number; plain?: boolean}> = ({
  x,
  y,
  size = 40,
  color = C.cream,
  anchor = 'middle',
  o = 1,
  children,
  w = 400,
  plain = false,
}) => (
  <text x={x} y={y} textAnchor={anchor} fontFamily="Lora, Georgia, serif" fontStyle="italic" fontWeight={w} fontSize={size} fill={color} opacity={clamp01(o)} stroke={plain ? 'none' : C.bg2} strokeWidth={size * 0.12} paintOrder="stroke">
    {children}
  </text>
);

/** Chữ lớn (Cormorant) cho con số và tiêu đề */
export const Big: React.FC<{x: number; y: number; size?: number; color?: string; anchor?: 'start' | 'middle' | 'end'; o?: number; children: React.ReactNode}> = ({
  x,
  y,
  size = 80,
  color = C.amber,
  anchor = 'middle',
  o = 1,
  children,
}) => (
  <text x={x} y={y} textAnchor={anchor} fontFamily="Cormorant" fontWeight={600} fontSize={size} fill={color} opacity={clamp01(o)} stroke={C.bg2} strokeWidth={size * 0.06} paintOrder="stroke" style={{fontVariantNumeric: 'lining-nums', fontFeatureSettings: '"lnum" 1'}}>
    {children}
  </text>
);

/** Người que đội mũ, chân đặt tại (x, y), cao 92 điểm ảnh khi s = 1. walk: pha bước đi (radian) */
export const lerp = (a: number, b: number, k: number) => a + (b - a) * k;

export const Hero: React.FC<{x: number; y: number; s?: number; walk?: number; rot?: number; p?: number; stick?: boolean; cheer?: number}> = ({x, y, s = 1, walk = 0, rot = 0, p = 1, stick = true, cheer = 0}) => {
  const sw = Math.sin(walk);
  const ch = clamp01(cheer);
  const bob = Math.abs(sw) * 2.5 + ch * Math.abs(Math.sin(walk * 1.6)) * 7;
  const sk = 5 / s;
  return (
    <g transform={`translate(${x} ${y - bob * s}) rotate(${rot}) scale(${s})`} opacity={clamp01(p * 2)} stroke={C.cream} strokeWidth={sk} strokeLinecap="round" strokeLinejoin="round" fill="none">
      <circle cx={0} cy={-69} r={11} fill={C.bg2} />
      <path d="M -11 -80 Q -11 -98 0 -98 Q 11 -98 11 -80 Z" fill={C.amberDeep} stroke={C.amberDeep} />
      <line x1={-18} y1={-80} x2={18} y2={-80} stroke={C.amberDeep} strokeWidth={sk * 1.2} />
      <line x1={0} y1={-58} x2={0} y2={-26} />
      <line x1={0} y1={-26} x2={-10 + 12 * sw} y2={0} />
      <line x1={0} y1={-26} x2={10 - 12 * sw} y2={0} />
      <line x1={0} y1={-48} x2={lerp(-16 - 4 * sw, -24 + 5 * Math.sin(walk * 3), ch)} y2={lerp(-32, -82, ch)} />
      <line x1={0} y1={-48} x2={22} y2={-40} />
      {stick && <line x1={24} y1={0} x2={24} y2={-92} stroke={C.amber} strokeWidth={sk * 1.2} />}
    </g>
  );
};

/** Quả địa cầu: mặt cầu có kinh tuyến và vĩ tuyến */
export const Globe: React.FC<{cx: number; cy: number; r: number; p?: number}> = ({cx, cy, r, p = 1}) => {
  const lat = [-0.55, 0, 0.55];
  return (
    <g opacity={clamp01(p * 2)} transform={`translate(${cx} ${cy}) scale(${0.6 + 0.4 * clamp01(p)}) translate(${-cx} ${-cy})`}>
      <circle cx={cx} cy={cy} r={r + 36} fill="url(#sunGlow)" opacity={0.5} />
      <circle cx={cx} cy={cy} r={r} fill="url(#globeG)" stroke={C.cream} strokeWidth={4} />
      <g fill="none" stroke={C.cream} strokeWidth={2} opacity={0.2}>
        <ellipse cx={cx} cy={cy} rx={r * 0.35} ry={r} />
        <ellipse cx={cx} cy={cy} rx={r * 0.7} ry={r} />
        <line x1={cx} y1={cy - r} x2={cx} y2={cy + r} />
        {lat.map((k, i) => {
          const dy = r * k;
          const rx = Math.sqrt(r * r - dy * dy);
          return <ellipse key={i} cx={cx} cy={cy + dy} rx={rx} ry={rx * 0.16} />;
        })}
      </g>
    </g>
  );
};

export const RAD = Math.PI / 180;

/** Biểu tượng kính lúp của page Người Giải Mã. raw = chỉ vẽ phần hình, dùng trong svg có sẵn */
export const MagMark: React.FC<{size?: number; raw?: boolean}> = ({size = 44, raw = false}) => {
  const g = (
    <g>
      <circle cx={19} cy={19} r={13} fill="none" stroke={C.amber} strokeWidth={4.5} />
      <circle cx={19} cy={19} r={9} fill={C.bg2} opacity={0.5} />
      <line x1={29} y1={29} x2={40} y2={40} stroke={C.amberDeep} strokeWidth={6} strokeLinecap="round" />
      <line x1={19} y1={26} x2={19} y2={13} stroke={C.cream} strokeWidth={2.5} strokeLinecap="round" />
      <line x1={19} y1={26} x2={25} y2={26} stroke={C.amberDeep} strokeWidth={2.5} strokeLinecap="round" />
    </g>
  );
  if (raw) return g;
  return (
    <svg width={size} height={size} viewBox="0 0 44 44">
      {g}
    </svg>
  );
};
