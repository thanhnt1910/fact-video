import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, clamp01, sp} from '../lib/theme';
import {Big, Globe, Hero, Lab, MagMark, Svg, lerp} from '../eratosthenes/v';

export type Sc = {dur: number; bs: number[]; t: Record<string, string>};

const D = C.dim;
const LEAD = '#8e98a3';
const LEAD_D = '#4e5761';
const WOOD = '#b98a55';
const WATER = '#5aa7d8';
const RAD = Math.PI / 180;

/** Mũi tên từ (x1,y1) tới (x2,y2); p = tiến độ vẽ */
const Arrow: React.FC<{x1: number; y1: number; x2: number; y2: number; color?: string; w?: number; p?: number}> = ({x1, y1, x2, y2, color = C.amber, w = 8, p = 1}) => {
  const ex = lerp(x1, x2, p);
  const ey = lerp(y1, y2, p);
  const a = Math.atan2(y2 - y1, x2 - x1);
  const h = Math.max(14, w * 2.2);
  const hx = (k: number) => ex - h * Math.cos(a + k);
  const hy = (k: number) => ey - h * Math.sin(a + k);
  return (
    <g opacity={clamp01(p * 3)} stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" fill={color}>
      <line x1={x1} y1={y1} x2={ex} y2={ey} />
      <path d={`M ${ex} ${ey} L ${hx(0.5)} ${hy(0.5)} L ${hx(-0.5)} ${hy(-0.5)} Z`} />
    </g>
  );
};

/** Cân đĩa. Gốc tọa độ ở trục quay. tilt: độ (dương = bên trái hạ xuống) */
const Scale: React.FC<{x: number; y: number; s?: number; tilt?: number; left?: React.ReactNode; right?: React.ReactNode; o?: number}> = ({x, y, s = 1, tilt = 0, left, right, o = 1}) => {
  const half = 250;
  const a = tilt * RAD;
  const lx = -half * Math.cos(a);
  const ly = half * Math.sin(a);
  const rx = half * Math.cos(a);
  const ry = -half * Math.sin(a);
  const drop = 150;
  const pan = (px: number, py: number, kids: React.ReactNode) => (
    <g transform={`translate(${px} ${py})`}>
      <line x1={0} y1={0} x2={-80} y2={drop} stroke={C.cream} strokeWidth={4} />
      <line x1={0} y1={0} x2={80} y2={drop} stroke={C.cream} strokeWidth={4} />
      <path d={`M -110 ${drop} Q 0 ${drop + 50} 110 ${drop}`} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
      <g transform={`translate(0 ${drop - 2})`}>{kids}</g>
    </g>
  );
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`} opacity={clamp01(o)}>
      <line x1={0} y1={0} x2={0} y2={330} stroke={C.cream} strokeWidth={9} strokeLinecap="round" />
      <line x1={-110} y1={330} x2={110} y2={330} stroke={C.cream} strokeWidth={12} strokeLinecap="round" />
      <line x1={lx} y1={ly} x2={rx} y2={ry} stroke={C.amber} strokeWidth={11} strokeLinecap="round" />
      <circle cx={0} cy={0} r={14} fill={C.amberDeep} />
      {pan(lx, ly, left)}
      {pan(rx, ry, right)}
    </g>
  );
};

const Apple: React.FC = () => (
  <g>
    <circle cx={-14} cy={-30} r={30} fill="#d9503a" />
    <circle cx={14} cy={-30} r={30} fill="#d9503a" />
    <path d="M 0 -58 Q 6 -76 24 -80" stroke="#7a4a22" strokeWidth={6} fill="none" strokeLinecap="round" />
    <ellipse cx={22} cy={-72} rx={14} ry={7} fill="#6aa84f" transform="rotate(-25 22 -72)" />
  </g>
);

// ============ 1. Mở đầu ============
export const Hook: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const b1 = bs[1];
  const bal = sp(f, 16, 70);
  const tilt = lerp(16, 0, bal);
  const ok = sp(f, 80, 96) * (1 - sp(f, b1 - 4, b1 + 8));
  const sh = sp(f, b1, b1 + 26);
  const gp = sp(f, b1 + 6, b1 + 36);
  const q = sp(f, b1 + 30, b1 + 50);
  const x = sp(f, b1 + 50, b1 + 64);
  const sx = lerp(540, 250, sh);
  const sy = lerp(640, 960, sh);
  const ss = lerp(1, 0.42, sh);
  return (
    <Svg>
      <Scale
        x={sx}
        y={sy}
        s={ss}
        tilt={tilt}
        o={sp(f, 0, 14)}
        left={<Apple />}
        right={
          <g fill={LEAD} stroke={C.cream} strokeWidth={3}>
            <rect x={-40} y={-44} width={36} height={44} />
            <rect x={4} y={-44} width={36} height={44} />
          </g>
        }
      />
      <Lab x={540} y={1160} size={44} color={C.cream} o={ok}>{t.appleOk}</Lab>
      <Globe cx={640} cy={720} r={290} p={gp} />
      <Big x={640} y={810} size={260} color={C.amber} o={q}>?</Big>
      <g transform="translate(250 840)" stroke={C.amberDeep} strokeWidth={10} strokeLinecap="round" opacity={x}>
        <line x1={-70} y1={-70} x2={70} y2={70} />
        <line x1={70} y1={-70} x2={-70} y2={70} />
      </g>
      <Lab x={540} y={1160} size={44} color={C.cream} o={sp(f, b1 + 56, b1 + 74)}>{t.noScale}</Lab>
      <Hero x={880} y={1130} s={1.7} p={sp(f, b1 + 70, b1 + 88)} walk={0} />
    </Svg>
  );
};

// ============ 2. Người đi trước thử bằng ngọn núi ============
const MX = 770;
const GYM = 1060;
export const Mount: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const [m0, m1, m2, m3, m4, m5] = bs;
  const base = sp(f, 0, 24);
  const scene = base * (1 - sp(f, m5 - 6, m5 + 10));
  const a = 11 * RAD * sp(f, m2 + 14, m2 + 50);
  const bx = 390 + 200 * Math.sin(a);
  const by = 720 + 200 * Math.cos(a);
  const straight = sp(f, m1 + 10, m1 + 30) * (1 - sp(f, m3, m3 + 12));
  const pullM = sp(f, m2 + 40, m2 + 60) * (1 - sp(f, m3, m3 + 12));
  const forces = sp(f, m3 + 6, m3 + 30) * (1 - sp(f, m4, m4 + 10));
  const rock = sp(f, m4 + 4, m4 + 24) * (1 - sp(f, m5 - 6, m5 + 8));
  const b = sp(f, m5 + 6, m5 + 36);
  const bar = (v: number, p: number) => 800 * (v / 5.5) * p;
  return (
    <Svg>
      <g opacity={scene}>
        <Lab x={540} y={230} size={42} color={C.amber} o={sp(f, 4, 20)}>{t.place}</Lab>
        <line x1={70} y1={GYM} x2={1010} y2={GYM} stroke={C.cream} strokeWidth={3} opacity={0.45} />
        <path d={`M 450 ${GYM} L ${MX} 590 L 1060 ${GYM} Z`} fill="#4a3b2e" stroke={C.cream} strokeWidth={4} strokeOpacity={0.55} />
        <path d={`M ${MX - 60} 650 L ${MX} 590 L ${MX + 50} 640 L ${MX} 626 Z`} fill={C.cream} opacity={0.35} />
        <Lab x={MX} y={GYM + 54} size={34} color={D} o={sp(f, 10, 26)}>{t.mountain}</Lab>
        <g opacity={rock}>
          {[
            [700, 800, '#7b6a58'], [820, 760, '#3a2f26'], [760, 880, '#8a7762'], [680, 930, '#3a2f26'], [850, 900, '#6a5a49'], [770, 700, '#5e4e3f'],
          ].map(([x, y, c], i) => (
            <circle key={i} cx={x as number} cy={y as number} r={30} fill={c as string} opacity={0.9} />
          ))}
          <Big x={MX} y={960} size={150} color={C.amber}>?</Big>
        </g>
        <Hero x={200} y={GYM} s={1.9} stick={false} p={sp(f, 6, 24)} />
        <Lab x={200} y={GYM + 54} size={34} color={C.amber} o={sp(f, 14, 30)}>{t.maske}</Lab>
        <line x1={300} y1={GYM} x2={300} y2={720} stroke={WOOD} strokeWidth={9} strokeLinecap="round" opacity={sp(f, 10, 26)} />
        <line x1={296} y1={720} x2={394} y2={720} stroke={WOOD} strokeWidth={9} strokeLinecap="round" opacity={sp(f, 10, 26)} />
        <g opacity={sp(f, 14, 30)}>
          <line x1={390} y1={720} x2={bx} y2={by} stroke={C.cream} strokeWidth={4} />
          <circle cx={bx} cy={by} r={20} fill={C.amber} stroke={C.cream} strokeWidth={3} />
        </g>
        <Lab x={150} y={760} size={34} color={C.cream} o={sp(f, m1 + 4, m1 + 20) * (1 - sp(f, m2, m2 + 10))}>{t.plumb}</Lab>
        <g opacity={straight}>
          <line x1={390} y1={940} x2={390} y2={1050} stroke={C.cream} strokeWidth={4} strokeDasharray="8 8" />
          <Arrow x1={390} y1={950} x2={390} y2={1054} color={C.cream} w={6} p={straight} />
          <Lab x={390} y={1210} size={32} color={C.cream}>{t.straight}</Lab>
        </g>
        <g opacity={pullM}>
          <Arrow x1={bx + 24} y1={by} x2={bx + 120} y2={by - 6} color={C.amber} w={8} p={pullM} />
          <Lab x={560} y={1210} size={32} color={C.amber} o={sp(f, m2 + 56, m2 + 74)} anchor="start">{t.tilt}</Lab>
          <Lab x={700} y={1250} size={26} color={D} o={0.9}>{t.notScale}</Lab>
        </g>
        <g opacity={forces}>
          <Arrow x1={bx + 22} y1={by} x2={bx + 90} y2={by} color={C.amber} w={9} p={forces} />
          <Arrow x1={bx} y1={by + 24} x2={bx} y2={by + 104} color={C.cream} w={11} p={forces} />
          <Lab x={bx + 100} y={by - 14} size={30} color={C.amber} anchor="start">{t.fMount}</Lab>
          <Lab x={bx + 26} y={by + 78} size={30} color={C.cream} anchor="start">{t.fEarth}</Lab>
          <Lab x={540} y={1210} size={32} color={C.cream}>{t.ratio}</Lab>
        </g>
        <Lab x={MX} y={520} size={36} color={C.amber} o={rock}>{t.rock}</Lab>
      </g>
      <g opacity={b}>
        <Lab x={540} y={330} size={42} color={C.cream}>{t.densTitle}</Lab>
        <Lab x={540} y={376} size={30} color={D}>{t.densUnit}</Lab>
        <Lab x={140} y={470} size={32} color={D} anchor="start">{t.barH}</Lab>
        <rect x={140} y={490} width={bar(4.5, sp(f, m5 + 14, m5 + 50))} height={64} rx={10} fill={C.amber} />
        <Big x={170} y={540} size={52} color={C.bg2} anchor="start" o={sp(f, m5 + 30, m5 + 50)}>4,5</Big>
        <Lab x={140} y={650} size={32} color={D} anchor="start">{t.barNow}</Lab>
        <rect x={140} y={670} width={bar(5.5, sp(f, m5 + 40, m5 + 76))} height={64} rx={10} fill={C.cream} />
        <Big x={170} y={720} size={52} color={C.bg2} anchor="start" o={sp(f, m5 + 60, m5 + 80)}>5,5</Big>
        <Big x={540} y={900} size={74} color={C.amber} o={sp(f, m5 + 80, m5 + 106)}>{t.lower}</Big>
      </g>
    </Svg>
  );
};

// ============ 3. Ý tưởng mới: mang ngọn núi vào phòng ============
const Dumbbell: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <line x1={-40} y1={0} x2={40} y2={0} stroke={WOOD} strokeWidth={6} strokeLinecap="round" />
    <circle cx={-44} cy={0} r={12} fill={LEAD} stroke={C.cream} strokeWidth={2} />
    <circle cx={44} cy={0} r={12} fill={LEAD} stroke={C.cream} strokeWidth={2} />
  </g>
);

export const Idea: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const [i0, i1, i2] = bs;
  const k = sp(f, 14, 70);
  const first = 1 - sp(f, i1 - 6, i1 + 10);
  const room = sp(f, 10, 34);
  const ball = sp(f, 36, 66);
  const people = sp(f, i1 + 2, i1 + 22);
  const mich = lerp(1, 0.4, sp(f, i2, i2 + 18));
  const cloudX = lerp(330, 780, sp(f, i2 + 4, i2 + 40));
  const endTxt = sp(f, i1 + 60, i1 + 80);
  return (
    <Svg>
      <g opacity={first}>
        <rect x={110} y={330} width={860} height={640} rx={24} fill="none" stroke={C.cream} strokeWidth={5} opacity={room * 0.7} />
        <g transform={`translate(${lerp(540, 780, k)} ${lerp(880, 800, k)}) scale(${lerp(1, 0.2, k)}) translate(-540 -880)`} opacity={1 - ball * 0.9}>
          <path d="M 250 880 L 540 440 L 830 880 Z" fill="#4a3b2e" stroke={C.cream} strokeWidth={6} strokeOpacity={0.6} />
        </g>
        <Lab x={540} y={1010} size={42} color={D} o={(1 - k) * sp(f, 0, 14)}>{t.mountain}</Lab>
        <g opacity={ball}>
          <circle cx={780} cy={800} r={74 * ball} fill={LEAD} stroke={C.cream} strokeWidth={5} />
          <ellipse cx={756} cy={778} rx={20} ry={12} fill="#fff" opacity={0.25} />
        </g>
        <Lab x={780} y={940} size={38} color={C.amber} o={ball}>{t.lead}</Lab>
        <Arrow x1={520} y1={800} x2={680} y2={800} color={C.amber} w={8} p={sp(f, 30, 56)} />
      </g>
      <g opacity={people}>
        <g opacity={mich}>
          <Hero x={330} y={1060} s={2.4} stick={false} p={1} />
          <Lab x={330} y={1130} size={36} color={C.cream}>{t.michell}</Lab>
          <Lab x={330} y={1180} size={32} color={D} o={endTxt}>{t.michellEnd}</Lab>
        </g>
        <g>
          <circle cx={cloudX - 40} cy={560} r={70} fill={C.bg1} stroke={C.cream} strokeWidth={4} />
          <circle cx={cloudX + 40} cy={560} r={70} fill={C.bg1} stroke={C.cream} strokeWidth={4} />
          <circle cx={cloudX} cy={520} r={72} fill={C.bg1} stroke={C.cream} strokeWidth={4} />
          <circle cx={cloudX} cy={560} r={78} fill={C.bg1} />
          <Dumbbell x={cloudX} y={556} s={1.3} />
          <circle cx={cloudX - 60} cy={720} r={10} fill={C.bg1} stroke={C.cream} strokeWidth={3} opacity={0.9} />
          <circle cx={cloudX - 76} cy={780} r={6} fill={C.bg1} stroke={C.cream} strokeWidth={3} opacity={0.9} />
        </g>
        <g opacity={sp(f, i2 + 10, i2 + 30)}>
          <Hero x={760} y={1060} s={2.4} stick={false} p={sp(f, i2 + 10, i2 + 30)} cheer={sp(f, i2 + 60, i2 + 80)} walk={f * 0.3} />
          <Lab x={760} y={1130} size={36} color={C.amber}>{t.cav}</Lab>
          <Lab x={760} y={1180} size={32} color={D} o={sp(f, i2 + 50, i2 + 70)}>{t.cavTag}</Lab>
        </g>
      </g>
    </Svg>
  );
};

// ============ 4. Thiết bị của Cavendish (nhìn từ trên xuống) ============
const CX = 540;
const CY = 660;
const Ball: React.FC<{x: number; y: number; r: number; o?: number}> = ({x, y, r, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill={LEAD} stroke={C.cream} strokeWidth={3} />
    <ellipse cx={x - r * 0.3} cy={y - r * 0.3} rx={r * 0.35} ry={r * 0.22} fill="#fff" opacity={0.25} />
  </g>
);

export const Device: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const [d0, d1, d2, d3, d4, d5, d6] = bs;
  const rodP = sp(f, 0, 24);
  const bigIn = sp(f, d1 + 4, d1 + 40);
  // vị trí quả lớn: cấu hình A (trái ở dưới, phải ở trên) và B (đổi chỗ)
  const swap = sp(f, d6 + 20, d6 + 80);
  const lbA = {x: -205, y: 95};
  const rbA = {x: 205, y: -95};
  const lbB = {x: -205, y: -95};
  const rbB = {x: 205, y: 95};
  const lbx = lerp(-440, lerp(lbA.x, lbB.x, swap), bigIn);
  const lby = lerp(lbA.y, lerp(lbA.y, lbB.y, swap), bigIn);
  const rbx = lerp(440, lerp(rbA.x, rbB.x, swap), bigIn);
  const rby = lerp(rbA.y, lerp(rbA.y, rbB.y, swap), bigIn);
  // góc xoay thanh (độ): âm = trái đi xuống
  const turn = sp(f, d2 + 20, d2 + 70);
  let theta = -7 * turn;
  theta = lerp(theta, theta + 6 * Math.sin(f * 0.45) + 4 * Math.sin(f * 0.9), sp(f, d4 + 10, d4 + 24) * (1 - sp(f, d5 - 6, d5 + 6)));
  theta = lerp(theta, 7, swap);
  const faded = sp(f, d3, d3 + 14) * (1 - sp(f, d4, d4 + 14));
  const devO = 1 - 0.85 * faded;
  const shedP = sp(f, d5 + 4, d5 + 34);
  const scale = lerp(1, 0.62, shedP);
  const shedCy = lerp(CY, 640, shedP);
  // so sánh lực
  const cmp = sp(f, d3 + 10, d3 + 36) * (1 - sp(f, d4 - 6, d4 + 6));
  // gió
  const wind = sp(f, d4 + 6, d4 + 22) * (1 - sp(f, d5 - 4, d5 + 8));
  const tele = sp(f, d5 + 30, d5 + 56);
  const notes = sp(f, d6 + 70, d6 + 100);
  return (
    <Svg>
      <Lab x={540} y={230} size={32} color={D} o={sp(f, 0, 14)}>{t.topView}</Lab>
      <g opacity={devO}>
        {/* căn nhà kín */}
        <g opacity={shedP}>
          <rect x={120} y={340} width={730} height={600} rx={12} fill={C.bg1} fillOpacity={0.3} stroke={C.cream} strokeWidth={9} />
          <rect x={846} y={620} width={14} height={60} fill={C.bg2} />
          <Lab x={485} y={400} size={36} color={C.cream}>{t.shed}</Lab>
        </g>
        <g transform={`translate(${shedP > 0 ? lerp(CX, 485, shedP) : CX} ${shedCy}) scale(${scale})`}>
          {/* thanh gỗ + quả nhỏ, xoay quanh tâm */}
          <g transform={`rotate(${theta})`}>
            <rect x={-270 * rodP} y={-7} width={540 * rodP} height={14} rx={5} fill={WOOD} />
            <Ball x={-270} y={0} r={18} o={sp(f, 10, 28)} />
            <Ball x={270} y={0} r={18} o={sp(f, 10, 28)} />
          </g>
          <circle cx={0} cy={0} r={9} fill={C.amberDeep} />
          <Ball x={lbx} y={lby} r={52} o={bigIn} />
          <Ball x={rbx} y={rby} r={52} o={bigIn} />
          {/* lực hút giữa quả lớn và quả nhỏ */}
          {(() => {
            const ap = sp(f, d2 + 4, d2 + 30) * (1 - sp(f, d3 - 4, d3 + 6)) + sp(f, d6 + 90, d6 + 110) * 0;
            const lx = -270 * Math.cos(theta * RAD);
            const ly = -270 * Math.sin(theta * RAD);
            const rx = 270 * Math.cos(theta * RAD);
            const ry = 270 * Math.sin(theta * RAD);
            return (
              <g opacity={ap}>
                <Arrow x1={lx + 6} y1={ly + 14} x2={lx + 22} y2={ly + 62} color={C.amber} w={7} p={ap} />
                <Arrow x1={rx - 6} y1={ry - 14} x2={rx - 22} y2={ry - 62} color={C.amber} w={7} p={ap} />
              </g>
            );
          })()}
        </g>
        {/* chú thích nhịp d0 */}
        <g opacity={(1 - sp(f, d1 + 6, d1 + 20)) * sp(f, 24, 40)}>
          <Lab x={540} y={520} size={34} color={C.cream}>{t.rod}</Lab>
          <Lab x={290} y={760} size={32} color={C.amber}>{t.small}</Lab>
          <Lab x={540} y={810} size={32} color={D}>{t.wire}</Lab>
          <line x1={540} y1={668} x2={540} y2={790} stroke={D} strokeWidth={3} strokeDasharray="6 8" />
        </g>
        <g opacity={sp(f, d1 + 30, d1 + 46) * (1 - sp(f, d2, d2 + 10))}>
          <Lab x={540} y={1040} size={34} color={C.cream}>{t.big}</Lab>
        </g>
        <g opacity={sp(f, d2 + 50, d2 + 70) * (1 - sp(f, d3 - 4, d3 + 6))}>
          <Lab x={540} y={1040} size={34} color={C.amber}>{t.rotate}</Lab>
        </g>
        {/* gió, nhiệt */}
        <g opacity={wind}>
          {[0, 1, 2].map((i) => {
            const x0 = ((f * 7 + i * 260) % 1100) - 60;
            const y0 = 460 + i * 170;
            return <path key={i} d={`M ${x0} ${y0} q 30 -26 60 0 t 60 0 t 60 0`} fill="none" stroke={C.cream} strokeWidth={6} strokeLinecap="round" opacity={0.7} />;
          })}
          <rect x={540} y={420} width={420} height={480} fill="#d9503a" opacity={0.22} />
          <Lab x={800} y={980} size={32} color="#e9806c">{t.warm}</Lab>
          <Lab x={200} y={420} size={36} color={C.cream}>{t.wind}</Lab>
          <Lab x={540} y={1060} size={34} color={C.amber}>{t.shake}</Lab>
        </g>
        {/* kính thiên văn và người đứng ngoài */}
        <g opacity={tele}>
          <line x1={900} y1={1010} x2={862} y2={650} stroke={C.cream} strokeWidth={14} strokeLinecap="round" />
          <line x1={900} y1={1010} x2={870} y2={730} stroke={C.amber} strokeWidth={6} strokeLinecap="round" />
          <Hero x={930} y={1140} s={1.8} stick={false} p={tele} />
          <Lab x={700} y={1190} size={34} color={C.cream}>{t.tele}</Lab>
        </g>
        <g opacity={sp(f, d6 + 4, d6 + 24) * (1 - sp(f, d6 + 100, d6 + 120))}>
          <Lab x={485} y={1040} size={36} color={C.amber}>{swap < 0.5 ? t.swap : t.back}</Lab>
        </g>
        <g opacity={notes}>
          <rect x={120} y={1060} width={300} height={170} rx={10} fill={C.bg1} stroke={C.cream} strokeWidth={4} />
          {[0, 1, 2, 3, 4].map((i) => (
            <line key={i} x1={150} y1={1100 + i * 28} x2={150 + 220 * sp(f, d6 + 74 + i * 6, d6 + 96 + i * 6)} y2={1100 + i * 28} stroke={C.cream} strokeWidth={4} opacity={0.8} />
          ))}
          <Lab x={270} y={1260} size={30} color={C.amber}>{t.noteB}</Lab>
        </g>
      </g>
      {/* so sánh lực: sức nặng quả nhỏ và lực kéo của quả chì */}
      <g opacity={cmp}>
        <Arrow x1={330} y1={560} x2={330} y2={900} color={C.cream} w={16} p={cmp} />
        <Lab x={330} y={960} size={32} color={C.cream}>{t.weight}</Lab>
        <Arrow x1={720} y1={720} x2={724} y2={728} color={C.amber} w={4} p={cmp} />
        <circle cx={724} cy={724} r={7} fill={C.amber} />
        <Lab x={724} y={790} size={32} color={C.amber}>{t.pull}</Lab>
        <Lab x={540} y={1060} size={40} color={C.cream}>{t.tiny}</Lab>
      </g>
    </Svg>
  );
};

// ============ 5. Công thức: nhân 3 con số ============
const BX = [45, 395, 745];
const BW = 290;
export const Calc: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const [k0, k1, k2, k3, k4, k5] = bs;
  const c0 = sp(f, 0, 24) * (1 - sp(f, k1 - 6, k1 + 8));
  const board = sp(f, k1 + 4, k1 + 22);
  const pn = (k: number, kn: number) => sp(f, k + 4, k + 20) * (1 - sp(f, kn - 6, kn + 8));
  const i2 = pn(k2, k3);
  const i3 = pn(k3, k4);
  const i4 = pn(k4, k5);
  const i5 = sp(f, k5 + 4, k5 + 22);
  const box = (i: number, num: string, name: string, p: number, hl: boolean) => (
    <g opacity={p}>
      <rect x={BX[i]} y={330} width={BW} height={210} rx={22} fill={C.bg1} stroke={hl ? C.amber : C.cream} strokeWidth={hl ? 6 : 3} strokeOpacity={hl ? 1 : 0.5} />
      <Lab x={BX[i] + BW / 2} y={382} size={36} color={C.amber}>{'①②③'[i]}</Lab>
      <Big x={BX[i] + BW / 2} y={452} size={num.length > 9 ? 40 : 52} color={C.cream}>{num}</Big>
      <Lab x={BX[i] + BW / 2} y={510} size={26} color={D}>{name}</Lab>
    </g>
  );
  const dist = (p: number) => (
    <g opacity={p}>
      <circle cx={170} cy={900} r={92} fill={LEAD} stroke={C.cream} strokeWidth={5} />
      <Ball x={420} y={900} r={34} />
      <line x1={262} y1={1010} x2={386} y2={1010} stroke={C.amber} strokeWidth={6} />
      <Lab x={324} y={1060} size={30} color={C.amber}>{t.dNear}</Lab>
      <circle cx={760} cy={2300} r={1300} fill="url(#globeG)" stroke={C.cream} strokeWidth={5} />
      <Ball x={760} y={900} r={34} />
      <line x1={760} y1={950} x2={760} y2={1000} stroke={C.cream} strokeWidth={5} strokeDasharray="10 12" />
      <Lab x={760} y={1060} size={30} color={C.cream}>{t.dFar}</Lab>
      <Lab x={540} y={1180} size={40} color={C.amber}>{t.d28}</Lab>
    </g>
  );
  return (
    <Svg>
      {/* 19: hai lực lên cùng quả cầu nhỏ */}
      <g opacity={c0}>
        <circle cx={540} cy={1930} r={900} fill="url(#globeG)" stroke={C.cream} strokeWidth={5} />
        <Lab x={540} y={1120} size={30} color={D}>Trái Đất</Lab>
        <circle cx={800} cy={760} r={92} fill={LEAD} stroke={C.cream} strokeWidth={5} />
        <Ball x={540} y={760} r={34} />
        <Arrow x1={540} y1={812} x2={540} y2={1040} color={C.cream} w={14} p={sp(f, 14, 50)} />
        <Lab x={560} y={940} size={34} color={C.cream} anchor="start" o={sp(f, 30, 50)}>{t.eFall}</Lab>
        <Arrow x1={584} y1={760} x2={690} y2={760} color={C.amber} w={9} p={sp(f, k0 + 90, k0 + 120)} />
        <Lab x={640} y={660} size={34} color={C.amber} o={sp(f, k0 + 100, k0 + 124)}>{t.eSide}</Lab>
        <Lab x={540} y={1210} size={28} color={D} o={0.9}>{t.notRatio}</Lab>
      </g>
      {/* 20–24: bảng công thức */}
      <g opacity={board}>
        <Big x={540} y={250} size={50} color={C.cream}>{t.fTitle}</Big>
        {box(0, t.n1, t.nm1, sp(f, k1 + 10, k1 + 26), f >= k2 && f < k3)}
        {box(1, t.n2, t.nm2, sp(f, k1 + 22, k1 + 38), f >= k2 && f < k3)}
        {box(2, f >= k4 ? t.n3b : f >= k3 ? t.n3a : '?', t.nm3, sp(f, k1 + 34, k1 + 50), f >= k3 && f < k5)}
        <Big x={365} y={455} size={48} color={C.amber} o={sp(f, k1 + 22, k1 + 38)}>×</Big>
        <Big x={715} y={455} size={48} color={C.amber} o={sp(f, k1 + 34, k1 + 50)}>×</Big>
      </g>
      {/* 21: quả chì và lực mạnh hơn 48 triệu lần */}
      <g opacity={i2}>
        <circle cx={250} cy={900} r={92} fill={LEAD} stroke={C.cream} strokeWidth={5} />
        <Lab x={250} y={1040} size={32} color={C.cream}>{t.lead158}</Lab>
        <Arrow x1={620} y1={820} x2={700} y2={820} color={C.amber} w={9} />
        <Lab x={660} y={780} size={28} color={C.amber}>{t.fLead}</Lab>
        <Arrow x1={620} y1={960} x2={1000} y2={960} color={C.cream} w={22} p={sp(f, k2 + 40, k2 + 80)} />
        <Lab x={810} y={920} size={28} color={C.cream}>{t.fEarth2}</Lab>
        <Big x={810} y={1070} size={60} color={C.amber} o={sp(f, k2 + 70, k2 + 100)}>{t.m48}</Big>
      </g>
      {/* 22: khoảng cách */}
      {dist(i3 * 1)}
      {/* 23: xa gấp đôi, lực yếu 4 lần */}
      <g opacity={i4}>
        <Ball x={200} y={820} r={30} />
        <Arrow x1={200} y1={870} x2={200} y2={1070} color={C.amber} w={18} p={sp(f, k4 + 14, k4 + 40)} />
        <Lab x={200} y={1130} size={28} color={C.cream}>{t.d1}</Lab>
        <Ball x={640} y={820} r={30} />
        <Arrow x1={640} y1={870} x2={640} y2={920} color={C.amber} w={6} p={sp(f, k4 + 60, k4 + 80)} />
        <Lab x={640} y={1130} size={28} color={C.cream}>{t.d2}</Lab>
        <Lab x={420} y={720} size={34} color={C.amber} o={sp(f, k4 + 50, k4 + 70)}>{t.x4}</Lab>
        <Big x={540} y={1260} size={44} color={C.cream} o={sp(f, k4 + 100, k4 + 130)}>{t.sq}</Big>
      </g>
      {/* 24: phép nhân ra kết quả */}
      <g opacity={i5}>
        <Big x={540} y={700} size={50} color={C.cream} o={sp(f, k5 + 8, k5 + 30)}>{t.mulRow}</Big>
        <Arrow x1={540} y1={760} x2={540} y2={870} color={C.amber} w={10} p={sp(f, k5 + 40, k5 + 70)} />
        <Big x={540} y={990} size={78} color={C.amber} o={sp(f, k5 + 60, k5 + 96)}>{t.mass}</Big>
        <Lab x={540} y={1050} size={28} color={D} o={sp(f, k5 + 76, k5 + 100)}>{t.zeros}</Lab>
      </g>
    </Svg>
  );
};

// ============ 5b. Kiểm lại ============
export const Check: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const [, k3, k4] = bs;
  const c2 = sp(f, 0, 22) * (1 - sp(f, k3 - 6, k3 + 8));
  const c3 = sp(f, k3 + 4, k3 + 22) * (1 - sp(f, k4 - 6, k4 + 8));
  const c4 = sp(f, k4 + 4, k4 + 22);
  const tilt = 14 * sp(f, 20, 70);
  const bar = (v: number, p: number) => 760 * (v / 5.6) * p;
  return (
    <Svg>
      {/* 25: cân Trái Đất với khối nước cùng kích thước */}
      <g opacity={c2}>
        <Scale
          x={540}
          y={560}
          s={0.95}
          tilt={-tilt}
          left={<rect x={-60} y={-120} width={120} height={120} rx={8} fill={WATER} stroke={C.cream} strokeWidth={4} opacity={0.9} />}
          right={<rect x={-60} y={-120} width={120} height={120} rx={8} fill="#1f5a60" stroke={C.cream} strokeWidth={4} />}
        />
        <Lab x={290} y={1010} size={32} color={WATER}>{t.water}</Lab>
        <Lab x={790} y={1010} size={32} color={C.cream}>{t.earthSame}</Lab>
        <Big x={540} y={1160} size={84} color={C.amber} o={sp(f, 60, 90)}>{t.times}</Big>
      </g>
      {/* 26: bên trong phải có thứ nặng */}
      <g opacity={c3}>
        <circle cx={540} cy={680} r={270} fill="#1f5a60" stroke={C.cream} strokeWidth={6} />
        <circle cx={540} cy={680} r={252} fill="none" stroke="#a88a64" strokeWidth={22} opacity={0.85} />
        <circle cx={540} cy={680} r={110} fill={C.amberDeep} opacity={0.9 * sp(f, k3 + 30, k3 + 60)} />
        <Big x={540} y={730} size={150} color={C.bg2} o={sp(f, k3 + 40, k3 + 70)}>?</Big>
        <Arrow x1={170} y1={420} x2={290} y2={480} color={D} w={5} p={sp(f, k3 + 10, k3 + 34)} />
        <Lab x={60} y={400} size={34} color={D} anchor="start" o={sp(f, k3 + 10, k3 + 30)}>{t.crust}</Lab>
        <Lab x={540} y={1060} size={38} color={C.amber} o={sp(f, k3 + 50, k3 + 76)}>{t.core}</Lab>
        <Lab x={540} y={1130} size={34} color={C.cream} o={sp(f, k3 + 20, k3 + 40)}>{t.whole}</Lab>
      </g>
      {/* 27: khối lượng và so sánh với số đo ngày nay */}
      <g opacity={c4}>
        <Big x={540} y={360} size={78} color={C.amber} o={sp(f, k4 + 6, k4 + 36)}>{t.mass}</Big>
        <Lab x={540} y={420} size={28} color={D} o={sp(f, k4 + 24, k4 + 44)}>{t.zeros}</Lab>
        <Lab x={150} y={600} size={32} color={D} anchor="start" o={sp(f, k4 + 50, k4 + 66)}>{t.bCav}</Lab>
        <rect x={150} y={620} width={bar(5.48, sp(f, k4 + 56, k4 + 96))} height={58} rx={10} fill={C.amber} />
        <Lab x={150} y={740} size={32} color={D} anchor="start" o={sp(f, k4 + 76, k4 + 92)}>{t.bNow}</Lab>
        <rect x={150} y={760} width={bar(5.51, sp(f, k4 + 82, k4 + 122))} height={58} rx={10} fill={C.cream} />
        <Big x={540} y={960} size={72} color={C.amber} o={sp(f, k4 + 120, k4 + 150)}>{t.diff}</Big>
      </g>
    </Svg>
  );
};

// ============ 6. Kết ============
export const Outro: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const e = bs[1];
  const fade = 1 - sp(f, e, e + 18);
  const lg = sp(f, e + 6, e + 28);
  return (
    <Svg>
      <g opacity={fade}>
        <Globe cx={640} cy={720} r={250} p={sp(f, 0, 24)} />
        <Scale x={190} y={640} s={0.55} tilt={12 * (1 - sp(f, 10, 50))} o={sp(f, 0, 20)} left={<Ball x={0} y={-26} r={26} />} right={<Ball x={0} y={-26} r={26} />} />
        <Hero x={860} y={1130} s={2.2} p={sp(f, 4, 22)} cheer={sp(f, 50, 70)} walk={f * 0.3} stick={false} />
      </g>
      <g opacity={lg} transform={`translate(0 ${(1 - lg) * 20})`}>
        <g transform="translate(465 770) scale(3.4)">
          <MagMark size={44} raw />
        </g>
        <text x={540} y={1000} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={74} fill={C.cream}>
          Người <tspan fill={C.amber}>Giải Mã</tspan>
        </text>
        <Lab x={540} y={1080} size={40} color={C.cream}>{t.tag}</Lab>
      </g>
    </Svg>
  );
};
