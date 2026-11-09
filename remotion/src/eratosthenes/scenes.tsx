import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, clamp01, sp} from '../lib/theme';
import {FlameMark, Ray, Sun} from '../thales/parts';
import {Big, Globe, Hero, Lab, RAD, Svg, VW, lerp} from './v';

export type Sc = {dur: number; bs: number[]; t: Record<string, string>};

const D = C.dim;

// ============ 1. Mở đầu ============
export const Hook: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const b1 = bs[1];
  const gp = sp(f, 0, 26);
  const sat = 1 - sp(f, b1 - 6, b1 + 10);
  const xo = sp(f, 36, 50) * sat;
  const a = f * 0.035;
  const sx = 540 + 380 * Math.cos(a);
  const sy = 430 + 70 * Math.sin(a);
  const hp = sp(f, b1 + 4, b1 + 28);
  return (
    <Svg>
      <Lab x={540} y={250} size={56} color={C.amber} o={sp(f, 4, 20)}>{t.year}</Lab>
      <Lab x={540} y={330} size={50} o={sp(f, 12, 28)}>{t.earthQ}</Lab>
      <Globe cx={540} cy={800} r={270} p={gp} />
      <g opacity={sat * sp(f, 24, 38)}>
        <g transform={`translate(${sx} ${sy})`}>
          <g transform="scale(1.7)">
            <rect x={-14} y={-9} width={28} height={18} fill={C.cream} />
            <rect x={-46} y={-7} width={26} height={14} fill={C.amber} opacity={0.85} />
            <rect x={20} y={-7} width={26} height={14} fill={C.amber} opacity={0.85} />
          </g>
        </g>
        <g transform={`translate(${sx} ${sy})`} stroke={C.amberDeep} strokeWidth={9} strokeLinecap="round" opacity={xo}>
          <line x1={-34} y1={-34} x2={34} y2={34} />
          <line x1={34} y1={-34} x2={-34} y2={34} />
        </g>
      </g>
      <Lab x={540} y={1110} size={46} color={D} o={xo * sat}>{t.noSat}</Lab>
      <Hero x={540} y={530} s={1.8} p={hp} />
      <Lab x={540} y={1110} size={50} color={C.amber} o={hp}>{t.hero} {t.stickTag}</Lab>
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
  const b1 = bs[1];
  const aO = 1 - 0.5 * sp(f, b1, b1 + 18);
  const bO = sp(f, b1, b1 + 22);
  // Panel A: Syene (nắng thẳng xuống giếng)
  const pa = sp(f, 18, 60);
  // Panel B: Alexandria (nắng nghiêng 18 độ vẽ to cho dễ nhìn)
  const phi = 18 * RAD;
  const u = {x: Math.sin(phi), y: -Math.cos(phi)};
  const n = {x: Math.cos(phi), y: Math.sin(phi)};
  const tip = {x: 620, y: 870};
  const gy = 1050;
  const sunB = {x: tip.x + 170 * u.x, y: tip.y + 170 * u.y};
  const pb = sp(f, b1 + 14, b1 + 50);
  const shade = sp(f, b1 + 40, b1 + 62);
  const sh = 180 * Math.tan(phi);
  const beams = [-70, 0, 70].map((d) => {
    const s0 = {x: tip.x + 150 * u.x + d * n.x, y: tip.y + 150 * u.y + d * n.y};
    const tt = (gy - s0.y) / -u.y;
    return {x1: s0.x, y1: s0.y, tt};
  });
  const arcR = 80;
  const a0 = {x: tip.x, y: tip.y - arcR};
  const a1 = {x: tip.x + arcR * u.x, y: tip.y + arcR * u.y};
  return (
    <Svg>
      {/* Panel A */}
      <g opacity={aO}>
        <rect x={40} y={210} width={1000} height={450} rx={16} fill="#000" opacity={0.14} stroke={C.cream} strokeOpacity={0.2} strokeWidth={2} />
        <Lab x={70} y={262} size={40} anchor="start" o={sp(f, 2, 16)}>{t.syene}</Lab>
        <Lab x={70} y={306} size={32} anchor="start" color={D} o={sp(f, 8, 22)}>{t.noon}</Lab>
        <line x1={70} y1={540} x2={672} y2={540} stroke={C.cream} strokeWidth={3} opacity={0.45} />
        <line x1={728} y1={540} x2={1010} y2={540} stroke={C.cream} strokeWidth={3} opacity={0.45} />
        <rect x={672} y={540} width={56} height={110} fill="#000" opacity={0.55} stroke={C.cream} strokeOpacity={0.5} strokeWidth={3} />
        <Sun x={700} y={300} p={sp(f, 10, 30)} />
        {[686, 700, 714].map((x) => (
          <Ray key={x} x1={x} y1={350} x2={x} y2={640} p={pa} opacity={0.8} />
        ))}
        <ellipse cx={700} cy={642} rx={24} ry={7} fill={C.amber} opacity={0.8 * clamp01((pa - 0.8) * 5)} />
        <line x1={480} y1={540} x2={480} y2={400} stroke={C.amber} strokeWidth={7} strokeLinecap="round" opacity={sp(f, 14, 30)} />
        <Lab x={480} y={598} size={30} color={D} o={clamp01((pa - 0.7) * 3)}>{t.noShadow}</Lab>
      </g>
      {/* Panel B */}
      <rect x={40} y={690} width={1000} height={460} rx={16} fill="none" stroke={C.cream} strokeOpacity={0.14} strokeWidth={2} opacity={1 - bO} />
      <g opacity={bO}>
        <rect x={40} y={690} width={1000} height={460} rx={16} fill="#000" opacity={0.14} stroke={C.cream} strokeOpacity={0.2} strokeWidth={2} />
        <Lab x={70} y={742} size={40} anchor="start">{t.alex}</Lab>
        <Lab x={70} y={786} size={32} anchor="start" color={D}>{t.sameTime}</Lab>
        <line x1={70} y1={gy} x2={1010} y2={gy} stroke={C.cream} strokeWidth={3} opacity={0.45} />
        <Sun x={sunB.x} y={sunB.y} p={sp(f, b1 + 8, b1 + 28)} />
        {beams.map((b, i) => (
          <Ray key={i} x1={b.x1} y1={b.y1} x2={b.x1 - b.tt * u.x} y2={gy} p={pb} opacity={0.8} />
        ))}
        <line x1={tip.x} y1={gy} x2={tip.x} y2={tip.y} stroke={C.amber} strokeWidth={8} strokeLinecap="round" />
        <line x1={tip.x} y1={gy} x2={tip.x - sh * shade} y2={gy} stroke={C.amber} strokeWidth={14} opacity={0.9} />
        <line x1={tip.x} y1={tip.y} x2={tip.x} y2={tip.y - 120} stroke={C.cream} strokeWidth={3} strokeDasharray="8 8" opacity={0.6 * sp(f, b1 + 50, b1 + 66)} />
        <path d={`M ${a0.x} ${a0.y} A ${arcR} ${arcR} 0 0 1 ${a1.x} ${a1.y}`} fill="none" stroke={C.amberDeep} strokeWidth={5} opacity={sp(f, b1 + 56, b1 + 72)} />
        <Lab x={720} y={836} size={38} anchor="start" color={C.amber} o={sp(f, b1 + 62, b1 + 80)}>{t.ang}</Lab>
        <Lab x={540} y={1136} size={26} color={D} o={sp(f, b1 + 62, b1 + 80)}>{t.notScale}</Lab>
      </g>
    </Svg>
  );
};

// ============ 4. Ý tưởng: mặt đất cong ============
export const Idea: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const b0 = bs[0];
  const b1 = bs[1];
  const d0 = b1 - b0;
  const cx = 540;
  const cy = 830;
  const R = 300;
  const phi = 30 * RAD;
  const L = 110;
  const m = sp(f, b0 + d0 * 0.4, b0 + d0 * 0.74);
  const psi = phi * m;
  const S = {x: cx, y: cy - R};
  const baseA = {x: cx - R * Math.sin(phi), y: lerp(530, cy - R * Math.cos(phi), m)};
  const tipA = {x: baseA.x - L * Math.sin(psi), y: baseA.y - L * Math.cos(psi)};
  const shEnd = {x: baseA.x - L * Math.sin(psi), y: baseA.y + L * Math.tan(psi) * Math.sin(psi)};
  const circY = (x: number) => cy - Math.sqrt(Math.max(0, R * R - (x - cx) * (x - cx)));
  const plain = [440, 640, 740];
  const rp = sp(f, 8, 44);
  const p2 = sp(f, b1, b1 + 30);
  const arcP = sp(f, b1 + 26, b1 + 46);
  const rO = 130;
  const oA = {x: cx - rO * Math.sin(phi), y: cy - rO * Math.cos(phi)};
  const tr = 70;
  const tA = {x: tipA.x, y: tipA.y + tr};
  const tB = {x: tipA.x + tr * Math.sin(phi), y: tipA.y + tr * Math.cos(phi)};
  const names = sp(f, b0 + d0 * 0.72, b0 + d0 * 0.92);
  const chipFlat = (1 - sp(f, b0 + d0 * 0.4, b0 + d0 * 0.55)) * sp(f, 14, 30);
  const chipCurve = sp(f, b0 + d0 * 0.7, b0 + d0 * 0.9) * (1 - sp(f, b1, b1 + 10));
  const chipSame = sp(f, b1 + 24, b1 + 44);
  return (
    <Svg>
      <Lab x={540} y={212} size={38} o={chipFlat}>{t.flat}</Lab>
      <Lab x={540} y={212} size={38} o={chipCurve}>{t.curved}</Lab>
      <Lab x={540} y={212} size={44} color={C.amber} o={chipSame}>{t.sameAngle}</Lab>
      <Sun x={540} y={300} p={sp(f, 0, 20)} />
      {/* mặt đất phẳng, chuyển thành mặt cầu */}
      <line x1={190} y1={530} x2={890} y2={530} stroke={C.cream} strokeWidth={4} opacity={0.5 * (1 - m)} strokeDasharray="14 10" />
      <circle cx={cx} cy={cy} r={R} fill="url(#globeG)" fillOpacity={0.85 * m} stroke={C.cream} strokeWidth={4} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - m} />
      {/* tia nắng song song */}
      {plain.map((x) => (
        <Ray key={x} x1={x} y1={372} x2={x} y2={lerp(530, circY(x), m)} p={rp} opacity={0.6} />
      ))}
      <Ray x1={S.x} y1={372} x2={S.x} y2={530} p={rp} opacity={0.8} />
      <Ray x1={tipA.x} y1={372} x2={shEnd.x} y2={shEnd.y} p={rp} opacity={0.8} />
      {/* hai cây gậy */}
      <line x1={S.x} y1={S.y} x2={S.x} y2={S.y - L} stroke={C.amber} strokeWidth={8} strokeLinecap="round" />
      <line x1={baseA.x} y1={baseA.y} x2={tipA.x} y2={tipA.y} stroke={C.amber} strokeWidth={8} strokeLinecap="round" />
      <line x1={baseA.x} y1={baseA.y} x2={shEnd.x} y2={shEnd.y} stroke={C.amberDeep} strokeWidth={14} opacity={0.9} />
      <Lab x={576} y={470} size={36} anchor="start" o={names}>Syene</Lab>
      <Lab x={300} y={498} size={36} anchor="end" o={names}>{t.alex}</Lab>
      {/* kéo dài hai đường tới tâm Trái Đất */}
      <g opacity={p2}>
        <line x1={cx} y1={cy} x2={S.x} y2={S.y} stroke={C.cream} strokeWidth={3} strokeDasharray="10 10" opacity={0.7} />
        <line x1={tipA.x} y1={tipA.y} x2={cx} y2={cy} stroke={C.cream} strokeWidth={3} strokeDasharray="10 10" opacity={0.7} />
        <circle cx={cx} cy={cy} r={8} fill={C.cream} />
      </g>
      <g opacity={arcP}>
        <path d={`M ${cx} ${cy - rO} A ${rO} ${rO} 0 0 0 ${oA.x} ${oA.y}`} fill="none" stroke={C.amber} strokeWidth={6} />
        <Lab x={cx - 41} y={cy - 156} size={44} color={C.amber}>α</Lab>
        <path d={`M ${tA.x} ${tA.y} A ${tr} ${tr} 0 0 0 ${tB.x} ${tB.y}`} fill="none" stroke={C.amber} strokeWidth={6} />
        <Lab x={tipA.x + 20} y={tipA.y + 112} size={44} color={C.amber}>α</Lab>
      </g>
    </Svg>
  );
};

// ============ 5. Tính: một phần năm mươi vòng ============
export const Calc: React.FC<Sc> = ({dur, bs, t}) => {
  const f = useCurrentFrame();
  const b1 = bs[1];
  const cx = 540;
  const cy = 650;
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
  const k1 = sp(f, 12, 36);
  const n = Math.floor(50 * sp(f, b1 + 14, b1 + Math.max(30, (dur - b1) - 70)));
  const lead = pt(-86.4, R + 6);
  const done = sp(f, dur - 62, dur - 34);
  return (
    <Svg>
      <g opacity={gp}>
        <circle cx={cx} cy={cy} r={R} fill="url(#globeG)" fillOpacity={0.55} stroke={C.cream} strokeWidth={4} />
        {Array.from({length: 50}).map((_, i) => {
          const a = pt(-90 + i * 7.2, R - 16);
          const b = pt(-90 + i * 7.2, R + 14);
          return <line key={i} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={C.cream} strokeWidth={2.5} opacity={0.5} />;
        })}
        {Array.from({length: 50}).map((_, i) => (
          <path key={'w' + i} d={wedge(i)} fill={C.amber} opacity={i === 0 ? 0.9 * k1 : i < n ? (i % 2 ? 0.28 : 0.4) : 0} />
        ))}
      </g>
      {/* nhãn cho một phần */}
      <g opacity={k1 * (1 - sp(f, b1, b1 + 12))}>
        <line x1={lead.x} y1={lead.y} x2={700} y2={330} stroke={C.amber} strokeWidth={3} />
        <Lab x={720} y={318} size={44} anchor="start" color={C.amber}>{t.stadia5}</Lab>
        <Lab x={720} y={364} size={30} anchor="start" color={D}>{t.part1}</Lab>
      </g>
      <Lab x={720} y={404} size={28} anchor="start" color={D} o={k1 * (1 - sp(f, b1, b1 + 12))}>{t.counted}</Lab>
      <Lab x={540} y={1010} size={34} color={D} o={k1 * (1 - sp(f, b1 + 30, b1 + 44))}>{t.stadiaDef}</Lab>
      {/* đếm các phần */}
      <Big x={540} y={cy + 34} size={104} color={C.cream} o={sp(f, b1 + 10, b1 + 26)}>
        {n < 1 ? '' : `× ${n}`}
      </Big>
      <Big x={540} y={1010} size={72} color={C.cream} o={done}>{t.eq50}</Big>
      <Big x={540} y={1092} size={92} color={C.amber} o={done}>{t.total}</Big>
      <Lab x={540} y={1140} size={28} color={D} o={done}>{t.source}</Lab>
    </Svg>
  );
};

// ============ 6. So với số đo ngày nay ============
export const Compare: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const b1 = bs[1];
  const x0 = 90;
  const W = 900;
  const wE = (W * 39375) / 40008;
  const e1 = sp(f, 0, 24);
  const bar1 = sp(f, 18, 60);
  const bar2 = sp(f, b1 + 4, b1 + 44);
  const dd = sp(f, b1 + 40, b1 + 60);
  const nt = sp(f, b1 + 56, b1 + 80);
  return (
    <Svg>
      <Lab x={540} y={300} size={44} color={D} o={e1}>{t.conv}</Lab>
      <Big x={540} y={410} size={110} o={sp(f, 10, 34)}>{t.conv2}</Big>
      <Lab x={x0} y={560} size={34} anchor="start" o={bar1}>{t.barE}</Lab>
      <rect x={x0} y={590} width={W} height={56} rx={10} fill={C.cream} opacity={0.08} />
      <rect x={x0} y={590} width={wE * bar1} height={56} rx={10} fill={C.amber} />
      <Lab x={x0 + 20} y={630} size={36} anchor="start" color={C.ink} o={clamp01((bar1 - 0.8) * 5)} w={700} plain>39 375 km</Lab>
      <Lab x={x0} y={740} size={34} anchor="start" o={bar2}>{t.barNow}</Lab>
      <rect x={x0} y={770} width={W} height={56} rx={10} fill={C.cream} opacity={0.08} />
      <rect x={x0} y={770} width={W * bar2} height={56} rx={10} fill={C.cream} opacity={0.9} />
      <Lab x={x0 + 20} y={810} size={36} anchor="start" color={C.ink} o={clamp01((bar2 - 0.8) * 5)} w={700} plain>40 008 km</Lab>
      <Big x={540} y={930} size={78} o={dd}>{t.diff}</Big>
      <Lab x={540} y={1010} size={30} color={D} o={nt}>{t.unsure1}</Lab>
      <Lab x={540} y={1056} size={30} color={D} o={nt}>{t.unsure2}</Lab>
    </Svg>
  );
};

// ============ 7. Ngày nay: mét đầu tiên ============
export const Modern: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const b1 = bs[1];
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
  const gp = sp(f, 0, 30);
  const hp = sp(f, 24, 56);
  const rest = sp(f, 70, 130);
  const mO = sp(f, b1 + 6, b1 + 30);
  return (
    <Svg>
      <Lab x={540} y={250} size={52} color={C.amber} o={sp(f, 2, 20)}>{t.fr}</Lab>
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
        <Hero x={hx} y={gy} s={s} p={sp(f, 4, 22)} />
      </g>
      <g opacity={lg}>
        <g transform={`translate(${VW / 2 - 70} 360)`}>
          <FlameMark width={140} />
        </g>
        <Big x={540} y={680} size={96} color={C.cream}>
          Proof<tspan fill={C.amber}>wick</tspan>
        </Big>
        <Lab x={540} y={790} size={46} color={C.cream}>{t.tag}</Lab>
      </g>
    </Svg>
  );
};
