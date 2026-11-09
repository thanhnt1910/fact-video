import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, clamp01, sp} from '../lib/theme';
import {Ray, Sun} from '../thales/parts';
import {Big, Globe, Hero, Lab, MagMark, RAD, Svg, VW, lerp} from './v';

export type Sc = {dur: number; bs: number[]; t: Record<string, string>};

const D = C.dim;

// ============ 1. Mở đầu ============
export const Hook: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const b1 = bs[1];
  const gp = sp(f, 0, 26);
  const q = sp(f, 24, 44) * (1 - sp(f, b1 - 6, b1 + 8));
  const pulse = 1 + 0.05 * Math.sin(f * 0.3);
  // vệ tinh bay quanh, bị gạch chéo; máy bay bay ngang, bị gạch chéo
  const a = f * 0.035;
  const sx = 540 + 380 * Math.cos(a);
  const sy = 430 + 70 * Math.sin(a);
  const satO = sp(f, b1 + 6, b1 + 20) * (1 - sp(f, b1 + 70, b1 + 84));
  const x1 = sp(f, b1 + 28, b1 + 40) * (1 - sp(f, b1 + 70, b1 + 84));
  const pl = sp(f, b1 + 34, b1 + 66);
  const px = lerp(-80, 1160, pl);
  const plO = (1 - sp(f, b1 + 74, b1 + 88)) * clamp01(pl * 6);
  const x2 = sp(f, b1 + 52, b1 + 64) * (1 - sp(f, b1 + 74, b1 + 88));
  const hp = sp(f, b1 + 78, b1 + 96);
  return (
    <Svg>
      <Lab x={540} y={250} size={56} color={C.amber} o={sp(f, 0, 16)}>{t.year}</Lab>
      <Lab x={540} y={330} size={50} o={sp(f, 4, 20)}>{t.earthQ}</Lab>
      <g transform={`translate(540 800) scale(${pulse}) translate(-540 -800)`}>
        <Globe cx={540} cy={800} r={270} p={gp} />
      </g>
      <Big x={540} y={880} size={260} color={C.amber} o={q}>?</Big>
      {/* vệ tinh */}
      <g opacity={satO}>
        <g transform={`translate(${sx} ${sy}) scale(1.7)`}>
          <rect x={-14} y={-9} width={28} height={18} fill={C.cream} />
          <rect x={-46} y={-7} width={26} height={14} fill={C.amber} opacity={0.85} />
          <rect x={20} y={-7} width={26} height={14} fill={C.amber} opacity={0.85} />
        </g>
        <g transform={`translate(${sx} ${sy})`} stroke={C.amberDeep} strokeWidth={9} strokeLinecap="round" opacity={x1}>
          <line x1={-34} y1={-34} x2={34} y2={34} />
          <line x1={34} y1={-34} x2={-34} y2={34} />
        </g>
      </g>
      {/* máy bay */}
      <g opacity={plO}>
        <g transform={`translate(${px} 600) scale(1.8)`} fill={C.cream} stroke={C.cream} strokeWidth={2} strokeLinejoin="round">
          <path d="M -46 0 Q 0 -13 46 0 Q 0 13 -46 0 Z" />
          <path d="M -4 0 L -26 -34 L -12 -34 L 18 0 Z" />
          <path d="M -4 0 L -26 34 L -12 34 L 18 0 Z" />
          <path d="M -40 0 L -52 -16 L -44 -16 L -30 0 Z" />
        </g>
        <g transform={`translate(${px} 600)`} stroke={C.amberDeep} strokeWidth={9} strokeLinecap="round" opacity={x2}>
          <line x1={-34} y1={-34} x2={34} y2={34} />
          <line x1={34} y1={-34} x2={-34} y2={34} />
        </g>
      </g>
      <Lab x={540} y={1110} size={44} color={D} o={sp(f, b1 + 30, b1 + 48) * (1 - hp)}>{t.planes}</Lab>
      <Hero x={880} y={1110} s={1.9} p={hp} cheer={sp(f, b1 + 100, b1 + 116)} walk={f * 0.3} />
      <Lab x={400} y={1150} size={44} color={C.amber} o={hp}>{t.hero} {t.stickTag}</Lab>
    </Svg>
  );
};

// ============ 2. Vì sao không đo thẳng được ============
export const Problem: React.FC<Sc> = ({dur, t}) => {
  const f = useCurrentFrame();
  const cx = 540;
  const cy = 800;
  const r = 270;
  const p = sp(f, 14, dur - 40);
  const th = (-90 + 135 * p) * RAD;
  const px = cx + r * Math.cos(th);
  const py = cy + r * Math.sin(th);
  const large = p * 135 > 180 ? 1 : 0;
  const q = sp(f, dur - 40, dur - 16);
  return (
    <Svg>
      <Lab x={540} y={330} size={50} o={sp(f, 0, 14)}>{t.earthQ}</Lab>
      <Globe cx={cx} cy={cy} r={r} p={1} />
      <path d={`M ${cx} ${cy - r} A ${r} ${r} 0 ${large} 1 ${px} ${py}`} fill="none" stroke={C.amber} strokeWidth={6} strokeDasharray="4 16" strokeLinecap="round" opacity={0.9} />
      <Hero x={px} y={py} s={1.25} walk={f * 0.5} rot={th / RAD + 90} stick={false} p={sp(f, 0, 12)} />
      <Big x={810} y={1030} size={150} color={C.amber} o={q}>?</Big>
      <Lab x={540} y={1110} size={46} color={C.cream} o={sp(f, 10, 24)}>{t.walk}</Lab>
      <Lab x={540} y={1150} size={28} color={D} o={0.8}>{t.illus}</Lab>
    </Svg>
  );
};

// ============ 3. Hai chiếc bóng: giếng ở Syene và cột ở Alexandria ============
export const Clue: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const [c0, c1, c2, c3] = bs;
  // Hộp A (Syene)
  const aFrame = sp(f, c0 + 50, c0 + 70);
  const aO = aFrame * (1 - 0.45 * sp(f, c2, c2 + 18) * (1 - sp(f, c3, c3 + 14)));
  const heroO = sp(f, 0, 14) * (1 - sp(f, c2 - 4, c2 + 10));
  const pa = sp(f, c1 + 22, c1 + 62);
  // Hộp B (Alexandria)
  const phi = 18 * RAD;
  const u = {x: Math.sin(phi), y: -Math.cos(phi)};
  const n = {x: Math.cos(phi), y: Math.sin(phi)};
  const tip = {x: 620, y: 870};
  const gy = 1050;
  const sunB = {x: tip.x + 170 * u.x, y: tip.y + 170 * u.y};
  const bO = sp(f, c2, c2 + 20);
  const pb = sp(f, c2 + 16, c2 + 50);
  const shade = sp(f, c2 + 44, c2 + 70);
  const sh = 180 * Math.tan(phi);
  const beams = [-70, 0, 70].map((d) => {
    const s0 = {x: tip.x + 150 * u.x + d * n.x, y: tip.y + 150 * u.y + d * n.y};
    const tt = (gy - s0.y) / -u.y;
    return {x1: s0.x, y1: s0.y, tt};
  });
  const km = sp(f, c2 + 40, c2 + 62);
  const q = sp(f, c3 + 105, c3 + 125);
  return (
    <Svg>
      {/* mở đầu: nhân vật */}
      <g opacity={heroO}>
        <Hero x={300} y={1000} s={2.4} walk={f * 0.2} />
        <Lab x={300} y={1090} size={44} color={C.amber}>{t.hero}</Lab>
      </g>
      {/* Hộp A */}
      <g opacity={aO}>
        <rect x={40} y={210} width={1000} height={450} rx={16} fill="#000" opacity={0.14} stroke={C.cream} strokeOpacity={0.2} strokeWidth={2} />
        <Lab x={70} y={262} size={40} anchor="start" o={sp(f, c0 + 56, c0 + 74)}>{t.syene}</Lab>
        <Lab x={70} y={306} size={32} anchor="start" color={D} o={sp(f, c1 + 6, c1 + 24)}>{t.noon}</Lab>
        <line x1={70} y1={540} x2={672} y2={540} stroke={C.cream} strokeWidth={3} opacity={0.45} />
        <line x1={728} y1={540} x2={1010} y2={540} stroke={C.cream} strokeWidth={3} opacity={0.45} />
        <rect x={672} y={540} width={56} height={110} fill="#000" opacity={0.55} stroke={C.cream} strokeOpacity={0.5} strokeWidth={3} />
        <Sun x={700} y={300} p={sp(f, c1 + 6, c1 + 30)} />
        {[686, 700, 714].map((x) => (
          <Ray key={x} x1={x} y1={350} x2={x} y2={640} p={pa} opacity={0.8} />
        ))}
        <ellipse cx={700} cy={642} rx={24} ry={7} fill={C.amber} opacity={0.8 * clamp01((pa - 0.8) * 5)} />
        <line x1={480} y1={540} x2={480} y2={400} stroke={C.amber} strokeWidth={7} strokeLinecap="round" opacity={sp(f, c1 + 14, c1 + 30)} />
        <Lab x={480} y={598} size={30} color={D} o={clamp01((pa - 0.7) * 3)}>{t.noShadow}</Lab>
      </g>
      {/* khoảng cách giữa hai thành phố */}
      <g opacity={km}>
        <line x1={530} y1={668} x2={530} y2={686} stroke={C.amber} strokeWidth={4} />
        <Lab x={510} y={684} size={34} anchor="end" color={C.amber}>{t.km800}</Lab>
      </g>
      {/* Hộp B */}
      <rect x={40} y={690} width={1000} height={460} rx={16} fill="none" stroke={C.cream} strokeOpacity={0.14} strokeWidth={2} opacity={1 - bO} />
      <g opacity={bO}>
        <rect x={40} y={690} width={1000} height={460} rx={16} fill="#000" opacity={0.14} stroke={C.cream} strokeOpacity={0.2} strokeWidth={2} />
        <Lab x={70} y={742} size={40} anchor="start">{t.alex}</Lab>
        <Lab x={70} y={786} size={32} anchor="start" color={D}>{t.sameTime}</Lab>
        <line x1={70} y1={gy} x2={1010} y2={gy} stroke={C.cream} strokeWidth={3} opacity={0.45} />
        <Sun x={sunB.x} y={sunB.y} p={sp(f, c2 + 8, c2 + 28)} />
        {beams.map((b, i) => (
          <Ray key={i} x1={b.x1} y1={b.y1} x2={b.x1 - b.tt * u.x} y2={gy} p={pb} opacity={0.8} />
        ))}
        <line x1={tip.x} y1={gy} x2={tip.x} y2={tip.y} stroke={C.amber} strokeWidth={8} strokeLinecap="round" />
        <line x1={tip.x} y1={gy} x2={tip.x - sh * shade} y2={gy} stroke={C.amber} strokeWidth={14} opacity={0.9} />
        <Lab x={tip.x - sh * 0.5} y={gy + 40} size={30} color={D} o={shade}>có bóng</Lab>
      </g>
      {/* Câu hỏi */}
      <Big x={900} y={1010} size={170} color={C.amber} o={q}>?</Big>
    </Svg>
  );
};

// ============ 4. Quả cam và hai cây tăm ============
export const Orange: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const [o0, o1, o2, o3] = bs;
  const cx = 540;
  const cy = 830;
  const R = 300;
  const phi = 30 * RAD;
  const L = 110;
  // m: 1 = mặt cong, 0 = mặt phẳng
  const m = f < o2 ? 1 : f < o3 ? 1 - sp(f, o2, o2 + 28) : sp(f, o3, o3 + 28);
  const psi = phi * m;
  const S = {x: cx, y: cy - R};
  const baseA = {x: cx - R * Math.sin(phi), y: lerp(530, cy - R * Math.cos(phi), m)};
  const tipA = {x: baseA.x - L * Math.sin(psi), y: baseA.y - L * Math.cos(psi)};
  const shEnd = {x: baseA.x - L * Math.sin(psi), y: baseA.y + L * Math.tan(psi) * Math.sin(psi)};
  const circY = (x: number) => cy - Math.sqrt(Math.max(0, R * R - (x - cx) * (x - cx)));
  const plain = [440, 640, 740];
  const appear = sp(f, 0, 24);
  const stk = sp(f, o0 + 70, o0 + 96);
  const torch = sp(f, o0 + 100, o0 + 124);
  const rp = sp(f, o0 + 112, o0 + 150) * (1 - 0);
  const shOp = sp(f, o1 + 8, o1 + 34) * (1 - sp(f, o2, o2 + 6)) + (f >= o2 + 6 ? 1 : 0) * 0;
  const earth = sp(f, o3 + 10, o3 + 40);
  const lines = sp(f, o1 + 40, o1 + 70) * (1 - sp(f, o2, o2 + 10)) + sp(f, o3 + 30, o3 + 56);
  const arcR = 130;
  const oA = {x: cx - arcR * Math.sin(phi), y: cy - arcR * Math.cos(phi)};
  const chip = (a: number, b: number, c: number, d: number) => sp(f, a, b) * (1 - sp(f, c, d));
  return (
    <Svg>
      <defs>
        <radialGradient id="orgG" cx="38%" cy="30%" r="85%">
          <stop offset="0%" stopColor="#f9bd63" />
          <stop offset="100%" stopColor="#b9570f" />
        </radialGradient>
      </defs>
      {/* đèn pin */}
      <g opacity={torch}>
        <rect x={510} y={236} width={60} height={86} rx={10} fill={C.cream} opacity={0.9} />
        <path d="M 504 322 L 576 322 L 590 352 L 490 352 Z" fill={C.amber} />
        <rect x={510} y={236} width={60} height={20} rx={6} fill={C.dim} />
        <Lab x={620} y={300} size={32} anchor="start" color={D}>{t.torch}</Lab>
      </g>
      {/* mặt phẳng (giấy) khi m nhỏ */}
      <g opacity={1 - m}>
        <rect x={190} y={530} width={700} height={14} fill={C.cream} opacity={0.25} />
        <line x1={190} y1={530} x2={890} y2={530} stroke={C.cream} strokeWidth={4} opacity={0.6} />
      </g>
      {/* quả cam / Trái Đất */}
      <g opacity={appear}>
        <circle cx={cx} cy={cy} r={R} fill="url(#orgG)" fillOpacity={m * (1 - earth)} stroke={C.cream} strokeWidth={4} strokeOpacity={m} />
        <circle cx={cx} cy={cy} r={R} fill="url(#globeG)" fillOpacity={0.9 * m * earth} stroke="none" />
      </g>
      {/* tia sáng song song */}
      {plain.map((x) => (
        <Ray key={x} x1={x} y1={372} x2={x} y2={lerp(530, circY(x), m)} p={rp} opacity={0.55} />
      ))}
      <Ray x1={S.x} y1={372} x2={S.x} y2={lerp(530, circY(S.x), m)} p={rp} opacity={0.8} />
      <Ray x1={tipA.x} y1={372} x2={shEnd.x} y2={shEnd.y} p={rp} opacity={0.8} />
      {/* hai cây tăm */}
      <g opacity={stk}>
        <line x1={S.x} y1={lerp(530, S.y, m)} x2={S.x} y2={lerp(530, S.y, m) - L * stk} stroke={C.cream} strokeWidth={7} strokeLinecap="round" />
        <line x1={baseA.x} y1={baseA.y} x2={baseA.x + (tipA.x - baseA.x) * stk} y2={baseA.y + (tipA.y - baseA.y) * stk} stroke={C.cream} strokeWidth={7} strokeLinecap="round" />
      </g>
      <line x1={baseA.x} y1={baseA.y} x2={shEnd.x} y2={shEnd.y} stroke={C.amberDeep} strokeWidth={14} opacity={0.9 * (shOp + sp(f, o3, o3 + 10) * (1 - sp(f, o2, o2 + 6)))} />
      {/* đường chỉ hướng về tâm */}
      <g opacity={lines}>
        <line x1={cx} y1={cy} x2={S.x} y2={S.y} stroke={C.cream} strokeWidth={3} strokeDasharray="10 10" opacity={0.7} />
        <line x1={tipA.x} y1={tipA.y} x2={cx} y2={cy} stroke={C.cream} strokeWidth={3} strokeDasharray="10 10" opacity={0.7} />
        <circle cx={cx} cy={cy} r={8} fill={C.cream} />
        <path d={`M ${cx} ${cy - arcR} A ${arcR} ${arcR} 0 0 0 ${oA.x} ${oA.y}`} fill="none" stroke={C.amber} strokeWidth={6} />
        <Lab x={cx - 40} y={cy - 156} size={44} color={C.amber}>α</Lab>
      </g>
      {/* tên hai nơi khi đã là Trái Đất */}
      <Lab x={576} y={470} size={36} anchor="start" o={earth}>Syene</Lab>
      <Lab x={300} y={498} size={36} anchor="end" o={earth}>{t.alex}</Lab>
      {/* nhãn theo từng nhịp */}
      <Lab x={540} y={1190} size={28} color={D} o={chip(o0 + 20, o0 + 40, o2 - 6, o2 + 4)}>{t.cam}</Lab>
      <Lab x={540} y={212} size={42} o={chip(o1 + 40, o1 + 62, o2, o2 + 10)}>{t.differ}</Lab>
      <Lab x={540} y={212} size={42} o={chip(o2 + 30, o2 + 50, o3, o3 + 10)}>{t.same}</Lab>
      <Lab x={540} y={212} size={42} color={C.amber} o={sp(f, o3 + 40, o3 + 62)}>{t.proof}</Lab>
      <Lab x={540} y={1150} size={30} color={D} o={chip(o2 + 20, o2 + 40, o3, o3 + 10)}>{t.paper}</Lab>
    </Svg>
  );
};

// ============ 5. Tính: một phần năm mươi vòng ============
export const Calc: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const [k0, k1, k2, k3, k4] = bs;
  const cx = 540;
  const cy = 640;
  const R = 270;
  const gp = sp(f, 0, 22);
  const pt = (deg: number, rr: number) => ({x: cx + rr * Math.cos(deg * RAD), y: cy + rr * Math.sin(deg * RAD)});
  const wedge = (i: number) => {
    const a = -90 + i * 7.2;
    const p0 = pt(a, 0);
    const p1 = pt(a, R);
    const p2 = pt(a + 7.2, R);
    return `M ${p0.x} ${p0.y} L ${p1.x} ${p1.y} A ${R} ${R} 0 0 1 ${p2.x} ${p2.y} Z`;
  };
  const w0 = sp(f, k0 + 20, k0 + 50);
  const cut = sp(f, k1 + 4, k1 + 40);
  const n = Math.floor(50 * sp(f, k3 + 12, k4 - 24));
  const done = sp(f, k4 + 8, k4 + 34);
  const cities = sp(f, k0 + 40, k0 + 64);
  const a0 = pt(-90, R);
  const a1 = pt(-82.8, R);
  const l1 = sp(f, k1 + 30, k1 + 50) * (1 - sp(f, k2 + 2, k2 + 16));
  const l2 = sp(f, k2 + 20, k2 + 44) * (1 - sp(f, k3, k3 + 12));
  const l3 = sp(f, k3 + 4, k3 + 22) * (1 - sp(f, k4, k4 + 12));
  return (
    <Svg>
      <g opacity={gp}>
        <circle cx={cx} cy={cy} r={R} fill="url(#globeG)" fillOpacity={0.55} stroke={C.cream} strokeWidth={4} />
        {Array.from({length: 50}).map((_, i) => {
          const a = pt(-90 + i * 7.2, R - 16);
          const b = pt(-90 + i * 7.2, R + 14);
          return <line key={i} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={C.cream} strokeWidth={2.5} opacity={0.5 * cut} />;
        })}
        {Array.from({length: 50}).map((_, i) => (
          <path
            key={'w' + i}
            d={wedge(i)}
            fill={C.amber}
            stroke={i === 0 ? 'none' : C.bg2}
            strokeWidth={2}
            opacity={i === 0 ? 0.9 * w0 : i < n ? (i % 2 ? 0.3 : 0.45) : 0.12 * cut * (i % 2 ? 0.6 : 1)}
          />
        ))}
      </g>
      {/* hai thành phố ở hai mép lát cắt */}
      <g opacity={cities}>
        <circle cx={a0.x} cy={a0.y} r={9} fill={C.cream} />
        <circle cx={a1.x} cy={a1.y} r={9} fill={C.cream} />
        <Lab x={a0.x - 20} y={a0.y - 26} size={34} anchor="end">Syene</Lab>
        <Lab x={a1.x + 24} y={a1.y - 24} size={34} anchor="start">{t.alex}</Lab>
      </g>
      <Lab x={540} y={1010} size={46} color={C.amber} o={sp(f, k0 + 50, k0 + 76) * (1 - sp(f, k1 + 4, k1 + 16))}>1/50 vòng</Lab>
      <Lab x={540} y={1010} size={42} color={C.amber} o={l1}>{t.slice1}</Lab>
      <Lab x={540} y={1060} size={30} color={D} o={l1}>{t.cake}</Lab>
      {/* khoảng cách */}
      <g opacity={l2}>
        <line x1={a0.x + 30} y1={a0.y + 40} x2={760} y2={300} stroke={C.amber} strokeWidth={3} />
        <Lab x={770} y={300} size={46} anchor="start" color={C.amber}>{t.km800}</Lab>
        <Lab x={770} y={344} size={30} anchor="start" color={D}>{t.counted}</Lab>
      </g>
      <Lab x={540} y={1010} size={42} color={C.amber} o={l2}>{t.km800}</Lab>
      {/* đếm các miếng */}
      <Big x={540} y={cy + 34} size={104} color={C.cream} o={sp(f, k3 + 10, k3 + 26) * (1 - sp(f, k4, k4 + 14))}>
        {n < 1 ? '' : `× ${n}`}
      </Big>
      <Lab x={540} y={1010} size={36} color={D} o={l3}>{t.km800} mỗi miếng</Lab>
      <Big x={540} y={1010} size={72} color={C.cream} o={done}>{t.mul}</Big>
      <Big x={540} y={1100} size={96} color={C.amber} o={done}>{t.total2}</Big>
      <Lab x={540} y={1148} size={28} color={D} o={done}>{t.round}</Lab>
    </Svg>
  );
};

// ============ 6. So với số đo ngày nay ============
export const Compare: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const b1 = bs[1];
  void b1;
  const x0 = 90;
  const W = 900;
  const wE = (W * 39375) / 40008;
  const e1 = sp(f, 0, 16);
  const bar1 = sp(f, 70, 112);
  const bar2 = sp(f, 20, 62);
  const dd = sp(f, 118, 140);
  const nt = sp(f, b1 + 10, b1 + 36);
  return (
    <Svg>
      <Lab x={540} y={300} size={44} color={D} o={e1}>{t.conv}</Lab>
      <Big x={540} y={410} size={110} o={sp(f, 6, 24)}>{t.total2}</Big>
      <Lab x={x0} y={560} size={34} anchor="start" o={bar1}>{t.barE}</Lab>
      <rect x={x0} y={590} width={W} height={56} rx={10} fill={C.cream} opacity={0.08} />
      <rect x={x0} y={590} width={wE * bar1} height={56} rx={10} fill={C.amber} />
      <Lab x={x0 + 20} y={630} size={36} anchor="start" color={C.ink} o={clamp01((bar1 - 0.8) * 5)} w={700} plain>39 375 km</Lab>
      <Lab x={x0} y={740} size={34} anchor="start" o={bar2}>{t.barNow}</Lab>
      <rect x={x0} y={770} width={W} height={56} rx={10} fill={C.cream} opacity={0.08} />
      <rect x={x0} y={770} width={W * bar2} height={56} rx={10} fill={C.cream} opacity={0.9} />
      <Lab x={x0 + 20} y={810} size={36} anchor="start" color={C.ink} o={clamp01((bar2 - 0.8) * 5)} w={700} plain>40 008 km</Lab>
      <Big x={540} y={930} size={78} o={dd}>{t.diff}</Big>
      <Hero x={170} y={1130} s={1.3} p={dd} cheer={dd} walk={f * 0.3} stick={false} />
      <Lab x={540} y={1010} size={30} color={D} o={nt}>{t.unsure1}</Lab>
      <Lab x={540} y={1056} size={30} color={D} o={nt}>{t.unsure2}</Lab>
    </Svg>
  );
};

// ============ 7. Ngày nay: mét đầu tiên ============
export const Modern: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const b0 = bs[0];
  const b1 = bs[1];
  const b2 = bs[2];
  void b0;
  const O = {x: 230, y: 1080};
  const R = 640;
  const at = (lat: number, rr = R) => ({x: O.x + rr * Math.cos(lat * RAD), y: O.y - rr * Math.sin(lat * RAD)});
  const arc = (l0: number, l1: number) => {
    const a = at(l0);
    const b = at(l1);
    return `M ${a.x} ${a.y} A ${R} ${R} 0 0 0 ${b.x} ${b.y}`;
  };
  const pole = at(90);
  const eq = at(0);
  const dk = at(51.03);
  const bc = at(41.39);
  const gp = sp(f, b1, b1 + 30);
  const hp = sp(f, b1 + 24, b1 + 56);
  const rest = sp(f, b1 + 70, b1 + 130);
  const mO = sp(f, b2 + 6, b2 + 30);
  return (
    <Svg>
      <Lab x={540} y={250} size={52} color={C.amber} o={sp(f, b1 + 2, b1 + 20)}>{t.fr}</Lab>
      <g opacity={(1 - sp(f, b1 - 4, b1 + 8)) * sp(f, 0, 18)}>
        <circle cx={540} cy={640} r={200} fill="url(#globeG)" fillOpacity={0.55} stroke={C.cream} strokeWidth={4} />
        <path d={`M 540 640 L 540 440 A 200 200 0 0 1 ${540 + 200 * Math.sin(7.2 * RAD)} ${640 - 200 * Math.cos(7.2 * RAD)} Z`} fill={C.amber} opacity={0.9} />
        <Lab x={540} y={930} size={44} color={C.amber} o={sp(f, 8, 26)}>đo một phần nhỏ</Lab>
        <Lab x={540} y={990} size={44} o={sp(f, 36, 56)}>suy ra cả vòng</Lab>
      </g>
      <path d={arc(0, 90)} fill="none" stroke={C.cream} strokeWidth={5} opacity={0.5 * gp} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - gp} />
      <path d={arc(0, 41.39)} fill="none" stroke={C.cream} strokeWidth={4} strokeDasharray="4 14" strokeLinecap="round" opacity={0.7 * rest} />
      <path d={arc(51.03, 90)} fill="none" stroke={C.cream} strokeWidth={4} strokeDasharray="4 14" strokeLinecap="round" opacity={0.7 * rest} />
      <path d={arc(41.39, 51.03)} fill="none" stroke={C.amber} strokeWidth={16} strokeLinecap="round" opacity={hp} />
      <circle cx={pole.x} cy={pole.y} r={10} fill={C.cream} opacity={gp} />
      <circle cx={eq.x} cy={eq.y} r={10} fill={C.cream} opacity={gp} />
      <circle cx={O.x} cy={O.y} r={6} fill={C.cream} opacity={0.5 * gp} />
      <Lab x={pole.x - 14} y={pole.y - 30} size={36} anchor="start" o={gp}>{t.pole}</Lab>
      <Lab x={eq.x - 12} y={eq.y + 56} size={36} anchor="end" o={gp}>{t.equator}</Lab>
      <circle cx={dk.x} cy={dk.y} r={9} fill={C.amber} opacity={hp} />
      <circle cx={bc.x} cy={bc.y} r={9} fill={C.amber} opacity={hp} />
      <Lab x={dk.x + 28} y={dk.y - 14} size={38} anchor="start" color={C.amber} o={hp}>{t.dk}</Lab>
      <Lab x={bc.x + 28} y={bc.y + 32} size={38} anchor="start" color={C.amber} o={hp}>{t.bcn}</Lab>
      <Lab x={740} y={770} size={30} anchor="end" color={D} o={rest}>{t.rest}</Lab>
      <g opacity={mO}>
        <Lab x={410} y={900} size={54} color={C.cream}>{t.meter1}</Lab>
        <Big x={410} y={990} size={64} color={C.amber}>{t.meter2}</Big>
      </g>
    </Svg>
  );
};

// ============ 8. Kết ============
export const Outro: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const e = bs[1];
  const sunP = sp(f, 0, 24);
  const fade = 1 - sp(f, e, e + 18);
  const lg = sp(f, e + 6, e + 28);
  const gy = 1020;
  const hx = 300;
  const s = 2.3;
  const tip = {x: hx + 24 * s, y: gy - 92 * s};
  const sunPos = {x: 520, y: 330};
  const dx = tip.x - sunPos.x;
  const dy = tip.y - sunPos.y;
  const shX = tip.x + (dx / dy) * (gy - tip.y);
  const sp2 = sp(f, 24, 52);
  return (
    <Svg>
      <g opacity={fade}>
        <Ray x1={sunPos.x} y1={sunPos.y} x2={shX} y2={gy} p={sp2} opacity={0.7} />
        <Sun x={sunPos.x} y={sunPos.y} p={sunP} />
        <line x1={90} y1={gy} x2={990} y2={gy} stroke={C.cream} strokeWidth={3} opacity={0.45} />
        <line x1={tip.x} y1={gy} x2={tip.x + (shX - tip.x) * sp2} y2={gy} stroke={C.amberDeep} strokeWidth={14} opacity={0.9} />
        <Hero x={hx} y={gy} s={s} p={sp(f, 4, 22)} cheer={sp(f, 60, 80)} walk={f * 0.3} />
      </g>
      <g opacity={lg}>
        <g transform={`translate(${VW / 2 - 70} 330)`}>
          <MagMark size={140} />
        </g>
        <Big x={540} y={680} size={96} color={C.cream}>
          Người <tspan fill={C.amber}>Giải Mã</tspan>
        </Big>
        <Lab x={540} y={790} size={46} color={C.cream}>{t.tag}</Lab>
      </g>
    </Svg>
  );
};
