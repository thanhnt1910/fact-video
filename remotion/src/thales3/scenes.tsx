import React from 'react';
import {useCurrentFrame} from 'remotion';
import {APEX_Y, C, GY, PB, PH, PX, clamp01, eio, sec, seg, sp} from '../lib/theme';
import {DimH, DimV, FlameMark, Ground, Ray, Shadow, Sun, Txt} from '../thales/parts';
import {At, Birds, Camel, Check, Cloud, Cross, Dunes, Ladder, Palm, Pyramid2, RopeCoil, Stick2, Walker} from '../thales2/parts2';
import {E32, E45, FX, Par, Sc, Sky, Svg, lerp, lin, pyrTip, tanE} from '../thales2/scenes';

const WATER = '#cfe3ea';

// ---------------------------------------------------------------- 1. Mở đầu (lạc đà đi qua, Thales tới, dấu hỏi)
export const Hook3: React.FC<Sc> = ({dur, bs, t}) => {
  const f = useCurrentFrame();
  const ground = sp(f, 0, sec(1.2));
  const pyr = sp(f, sec(0.4), sec(4.6));
  const zoom = 1 + 0.08 * seg(f, 0, dur);
  const titleO = seg(f, sec(0.3), sec(1.3)) * (1 - seg(f, sec(5.0), sec(6.2)));
  const caravan = 2150 - 170 * (f / 30);
  const wk = lin(f, bs[1] - sec(5.0), bs[1] - sec(1.4));
  const tx = lerp(1900, FX, wk);
  const walking = wk > 0 && wk < 1;
  const cl = sp(f, bs[2] + sec(0.2), bs[2] + sec(1.4));
  const q = sp(f, bs[2] + sec(1.2), bs[2] + sec(2.2));
  return (
    <Svg>
      <g transform={`translate(960 600) scale(${zoom}) translate(-960 -600)`}>
        <Dunes o={ground} />
        <Palm x={100} />
        <Birds />
        <Ground p={ground} />
        <Pyramid2 p={pyr} />
        <Sky e={32} p={sp(f, sec(5.2), sec(6.4))} />
        {[0, 330, 700].map((off, i) => (
          <Camel key={i} x={caravan + off} dir={-1} s={1.05} phase0={i * 1.3} />
        ))}
        <Walker x={tx} dir={-1} walking={walking} p={sp(f, 0, sec(0.6))} />
        <Cloud cx={1500} cy={360} rx={200} ry={110} p={cl} tail={[FX, GY - 130]}>
          <Txt x={1500} y={415} size={150} color={C.amber} opacity={q}>
            ?
          </Txt>
        </Cloud>
      </g>
      <text x={960} y={215} textAnchor="middle" fontFamily="Cormorant" fontWeight={600} fontSize={92} fill={C.cream} opacity={titleO}>
        {t.title}
      </text>
    </Svg>
  );
};

// ---------------------------------------------------------------- 2. Dụng cụ thời đó: dây đo ruộng, đo cạnh đáy
export const Tools: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const fl = Math.sin(Math.PI * lin(f, bs[0] + sec(0.8), bs[0] + sec(6.4)));
  const waterY = GY + 70 - 84 * fl;
  const wave = Array.from({length: 49})
    .map((_, i) => `${i === 0 ? 'M' : 'L'}${i * 40} ${waterY + Math.sin(i * 0.8 + f * 0.12) * 7}`)
    .join(' ');
  const stakes = [1060, 1210, 1360, 1510, 1660];
  const walk = lin(f, bs[1] + sec(0.8), bs[1] + sec(6.6));
  const x2 = lerp(336, 946, eio(walk));
  const walking = walk > 0 && walk < 1;
  const ropeP = sp(f, bs[1] + sec(0.2), bs[1] + sec(0.8));
  const dim = sp(f, bs[1] + sec(6.8), bs[1] + sec(8.2));
  const ck = sp(f, bs[1] + sec(8.0), bs[1] + sec(8.8));
  const hd = sp(f, bs[2] + sec(0.4), bs[2] + sec(1.6));
  const pulse = 1 + 0.12 * Math.sin(f * 0.2);
  const knots: number[] = [];
  for (let k = 360; k < x2 - 14; k += 36) knots.push(k);
  return (
    <Svg>
      <Dunes />
      <Palm x={100} />
      <Birds />
      <Ground p={1} />
      <Pyramid2 p={1} />
      <Sky e={32} />
      {stakes.map((x) => (
        <line key={x} x1={x} y1={GY} x2={x} y2={GY - 42} stroke="#d9b27a" strokeWidth={6} strokeLinecap="round" opacity={1 - clamp01(fl * 1.8)} />
      ))}
      <path d={`${wave} L1920 1080 L0 1080 Z`} fill={WATER} opacity={0.14 * clamp01(fl * 3)} />
      <path d={wave} fill="none" stroke={WATER} strokeWidth={3} opacity={0.5 * clamp01(fl * 3)} />
      <g opacity={ropeP}>
        <path d={`M${342 + 16} ${GY - 36} Q${(342 + x2) / 2} ${GY - 20} ${x2 - 14} ${GY - 36}`} fill="none" stroke="#d9b27a" strokeWidth={4.5} strokeLinecap="round" />
        {knots.map((k) => (
          <circle key={k} cx={k} cy={GY - 30 + Math.sin(((k - 342) / (x2 - 342)) * Math.PI) * 9} r={4.6} fill={C.amber} />
        ))}
      </g>
      <Walker x={330} dir={1} robe="#a8c9a0" size={105} />
      <Walker x={x2} dir={1} walking={walking} robe="#e3ab78" size={105} speed={0.62} />
      <DimH x1={342} x2={938} y={GY + 52} label={t.base} p={dim} size={38} />
      <Check x={1010} y={GY + 40} r={26} p={ck} />
      <g transform={`translate(${302 - 60} ${(GY + APEX_Y) / 2}) scale(${pulse}) translate(${-(302 - 60)} ${-(GY + APEX_Y) / 2})`} opacity={hd}>
        <DimV x={PX - PB - 40} y1={GY} y2={APEX_Y} label="?" p={hd} size={80} color={C.amber} />
      </g>
    </Svg>
  );
};

// ---------------------------------------------------------------- 3. Thất bại 1: thang và tháp người
export const LadderFail: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const u = lin(f, bs[0] + sec(0.8), bs[0] + sec(4.4));
  const climbing = u > 0 && u < 1;
  const ladderFade = 1 - seg(f, bs[1] - sec(0.4), bs[1] + sec(0.4));
  const tag = sp(f, bs[0] + sec(4.6), bs[0] + sec(5.8)) * ladderFade;
  const far = sp(f, bs[0] + sec(5.0), bs[0] + sec(6.2)) * ladderFade;
  const N = 6;
  const cols = ['#e3ab78', '#a8c9a0', '#c9a0c9', '#e8d070', '#8fb4c9', '#e07a6a'];
  const col = lin(f, bs[2] + sec(0.5), bs[2] + sec(2.4));
  const c2 = col * col;
  const sway = seg(f, bs[2] - sec(0.2), bs[2] + sec(0.5)) * (1 - seg(f, bs[2] + sec(0.5), bs[2] + sec(0.6)));
  const swayRot = Math.sin(f * 0.55) * 6 * sway;
  const ghost = sp(f, bs[1] + sec(3.6), bs[1] + sec(4.8)) * (1 - seg(f, bs[2] + sec(1.6), bs[2] + sec(2.4)));
  const puff = seg(f, bs[2] + sec(1.9), bs[2] + sec(3.0));
  const towerX = 1250;
  return (
    <Svg>
      <Dunes />
      <Palm x={100} />
      <Birds />
      <Ground p={1} />
      <Pyramid2 p={1} />
      <Sky e={32} />
      <DimV x={PX - PB - 40} y1={GY} y2={APEX_Y} label="147 m" p={sp(f, bs[0] + sec(0.2), bs[0] + sec(1.4))} color={C.amber} size={36} />
      <g opacity={ladderFade}>
        <line x1={905} y1={GY} x2={860} y2={GY - 100} stroke="#d9b27a" strokeWidth={6} strokeLinecap="round" />
        <line x1={927} y1={GY} x2={882} y2={GY - 100} stroke="#d9b27a" strokeWidth={6} strokeLinecap="round" />
        {[0.15, 0.32, 0.5, 0.68, 0.85].map((k) => (
          <line key={k} x1={lerp(905, 860, k)} y1={GY - 100 * k} x2={lerp(927, 882, k)} y2={GY - 100 * k} stroke="#d9b27a" strokeWidth={4} />
        ))}
        <At x={lerp(920, 874, u)} y={GY - 100 * u}>
          <Walker x={0} dir={-1} walking={climbing} size={54} noShadow robe="#a8c9a0" speed={1.3} />
        </At>
        <Txt x={1010} y={GY - 52} size={36} color={C.dim} anchor="start" opacity={tag}>
          {t.ladderTag}
        </Txt>
        <Txt x={1010} y={GY - 250} size={38} color={C.amber} anchor="start" opacity={far}>
          {t.farLeft}
        </Txt>
        <line x1={1000} y1={GY - 104} x2={1000} y2={APEX_Y} stroke={C.amber} strokeWidth={3} strokeDasharray="10 10" opacity={far} />
      </g>
      <g opacity={ghost}>
        <line x1={towerX - 70} y1={APEX_Y} x2={towerX + 70} y2={APEX_Y} stroke={C.amber} strokeWidth={4} strokeDasharray="12 10" />
        <Txt x={towerX} y={APEX_Y - 18} size={42} color={C.amber}>
          {t.men}
        </Txt>
      </g>
      <g transform={`rotate(${swayRot} ${towerX} ${GY})`}>
        {Array.from({length: N}).map((_, k) => {
          const appear = sp(f, bs[1] + sec(0.6 + 0.7 * k), bs[1] + sec(1.0 + 0.7 * k));
          if (appear <= 0) return null;
          const y0 = GY - k * 36;
          const drop = (1 - appear) * 160;
          const y = lerp(y0, GY, c2) - drop;
          const x = towerX + c2 * (60 + 52 * k);
          const rot = c2 * (75 + 22 * k);
          return (
            <At key={k} x={x} y={y} rot={rot}>
              <Walker x={0} dir={-1} size={42} noShadow robe={cols[k]} p={appear} />
            </At>
          );
        })}
      </g>
      {(() => {
        const shown = [0, 1, 2, 3, 4, 5].filter((k) => f >= bs[1] + sec(0.8 + 0.7 * k)).length;
        return shown > 0 ? (
          <Txt x={towerX} y={GY - shown * 36 - 70 + c2 * (shown * 36 + 40)} size={46} color={C.amber} opacity={1 - seg(f, bs[2] + sec(2.4), bs[2] + sec(3.2))}>
            {`${shown} / 86`}
          </Txt>
        ) : null;
      })()}
      <g opacity={0.5 * (1 - puff)}>
        {[0, 1, 2, 3, 4].map((i) => (
          <circle key={i} cx={towerX + 20 + i * 38} cy={GY - 8 - puff * 20} r={10 + puff * 26 + i * 3} fill={C.cream} opacity={0.35} />
        ))}
      </g>
    </Svg>
  );
};

// ---------------------------------------------------------------- 4. Thất bại 2: leo trơn, dây chỉ đo đường dốc
export const SlopeFail: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const sheen = lin(f, bs[0] + sec(0.4), bs[0] + sec(2.4));
  const attempt = (a: number, b: number, hi: number) => {
    const up = lin(f, a, b);
    const slip = lin(f, b, b + sec(0.5));
    return {u: up < 1 ? up * hi : hi * (1 - eio(slip)), slip: slip > 0 && slip < 1, done: slip >= 1, up};
  };
  const a1 = attempt(bs[0] + sec(2.2), bs[0] + sec(5.0), 0.3);
  const a2 = attempt(bs[0] + sec(6.2), bs[0] + sec(8.0), 0.18);
  const cur = f < bs[0] + sec(6.0) ? a1 : a2;
  const visible = f > bs[0] + sec(2.0) && !(a2.done && f > bs[0] + sec(9.0));
  const sx = 342 + 298 * cur.u;
  const sy = GY - 380 * cur.u;
  const climbing = cur.up > 0 && cur.up < 1 && !cur.slip;
  const rot = cur.slip ? -38 - 65 : -38;
  const rope = sp(f, bs[1] + sec(0.4), bs[1] + sec(2.8));
  const lab = sp(f, bs[1] + sec(2.4), bs[1] + sec(3.6));
  const tri = sp(f, bs[1] + sec(3.4), bs[1] + sec(4.6));
  const hq = sp(f, bs[1] + sec(4.6), bs[1] + sec(5.8));
  const stone = sp(f, bs[2] + sec(0.4), bs[2] + sec(2.0));
  const ang = (Math.atan2(PH, PB) * 180) / Math.PI;
    const hatch = Array.from({length: 14}).map((_, i) => APEX_Y + 40 + i * 24);
  return (
    <Svg>
      <defs>
        <clipPath id="leftFace">
          <path d={`M${PX - PB} ${GY} L${PX} ${APEX_Y} L${PX} ${GY} Z`} />
        </clipPath>
        <clipPath id="axisBand">
          <path d={`M${PX - PB} ${GY} L${PX} ${APEX_Y} L${PX + PB} ${GY} Z`} />
        </clipPath>
      </defs>
      <Dunes />
      <Palm x={100} />
      <Birds />
      <Ground p={1} />
      <Pyramid2 p={1} />
      <g clipPath="url(#leftFace)">
        <rect x={lerp(240, 700, sheen) - 40} y={APEX_Y - 40} width={60} height={PH + 80} fill="#fff7e0" opacity={0.35 * Math.sin(Math.PI * sheen)} transform={`skewX(-18)`} />
      </g>
      <path d={`M${PX} ${APEX_Y} L${PX} ${GY} L${PX + PB} ${GY} Z`} fill={C.amber} opacity={0.14 * tri} />
      <Sky e={32} />
      {visible && (
        <At x={sx - 10} y={sy + 4} rot={rot}>
          <Walker x={0} dir={1} walking={climbing} size={84} noShadow robe="#a8c9a0" speed={1.3} />
        </At>
      )}
      <path d={`M${PX} ${APEX_Y} Q${PX + PB * 0.55 + 38} ${APEX_Y + PH * 0.45 - 30} ${PX + PB + 6} ${GY}`} fill="none" stroke="#f3d9a4" strokeWidth={7} strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - rope} />
      {rope > 0.02 && <circle cx={PX} cy={APEX_Y} r={10} fill="#f3d9a4" />}
      <g transform={`translate(${PX + PB / 2 + 62} ${APEX_Y + PH / 2 - 38}) rotate(${ang})`} opacity={lab}>
        <text textAnchor="middle" fontFamily="Lora, Georgia, serif" fontStyle="italic" fontSize={42} fill={C.amber} y={0}>
          {t.slope}
        </text>
      </g>
      <line x1={PX} y1={APEX_Y} x2={PX} y2={GY} stroke={C.cream} strokeWidth={4} strokeDasharray="10 12" opacity={0.7 * hq} />
      <Txt x={PX + 52} y={APEX_Y + PH * 0.55} size={110} color={C.amber} opacity={hq * (1 - 0.0 * stone)}>
        ?
      </Txt>
      <g clipPath="url(#axisBand)" opacity={stone}>
        {hatch.map((y, i) => (
          <line key={i} x1={PX - 60} y1={y + 30} x2={PX + 60} y2={y - 30} stroke={C.cream} strokeWidth={2} opacity={0.35} />
        ))}
      </g>
    </Svg>
  );
};

// ---------------------------------------------------------------- 5. Ý tưởng: chiều cao nằm xuống thành cái bóng
export const Idea: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const i1 = sp(f, bs[0] + sec(1.4), bs[0] + sec(2.2));
  const i2 = sp(f, bs[0] + sec(3.0), bs[0] + sec(3.8));
  const i3 = sp(f, bs[0] + sec(4.6), bs[0] + sec(5.4));
  const icons = 1 - seg(f, bs[1], bs[1] + sec(0.8));
  const spark = sp(f, bs[1] + sec(1.0), bs[1] + sec(1.8));
  const burst = seg(f, bs[1] + sec(1.0), bs[1] + sec(2.4));
  const sunP = sp(f, bs[1] + sec(2.6), bs[1] + sec(3.8));
  const rot = 90 * eio(lin(f, bs[2] + sec(0.8), bs[2] + sec(3.6)));
  const landed = lin(f, bs[2] + sec(3.4), bs[2] + sec(3.6));
  const tipP = PX + PH;
  const hot = sp(f, bs[2] + sec(3.4), bs[2] + sec(4.0));
  const rays = sp(f, bs[2] + sec(3.8), bs[2] + sec(5.6));
  const sunNear = sp(f, bs[1] + sec(2.6), bs[1] + sec(3.8));
  return (
    <Svg>
      <Dunes />
      <Palm x={100} />
      <Birds />
      <Ground p={1} />
      <Pyramid2 p={1} />
      <g opacity={icons}>
        <g opacity={i1}>
          <Ladder cx={1120} cy={250} />
          <Cross x={1120} y={250} p={i1} />
        </g>
        <g opacity={i2}>
          <RopeCoil cx={1280} cy={250} />
          <Cross x={1290} y={250} p={i2} />
        </g>
        <g opacity={i3}>
          <rect x={1400} y={238} width={170} height={26} rx={4} fill="none" stroke={C.cream} strokeWidth={4} />
          {Array.from({length: 9}).map((_, i) => (
            <line key={i} x1={1400 + 10 + i * 18} y1={238} x2={1400 + 10 + i * 18} y2={238 + (i % 2 ? 12 : 18)} stroke={C.cream} strokeWidth={3} />
          ))}
          <Check x={1690} y={252} r={28} p={i3} />
        </g>
      </g>
      <Walker x={FX} dir={-1} />
      <g opacity={spark} transform={`translate(${FX - 32 * (0.4 + 0.6 * spark)} ${470 - 20 * spark}) scale(${0.4 + 0.6 * spark})`}>
        <circle cx={32} cy={52} r={90 * burst} fill="none" stroke={C.amber} strokeWidth={4} opacity={1 - burst} />
        <circle cx={32} cy={52} r={60} fill="url(#sunGlow)" />
        <FlameMark width={64} />
      </g>
      {sunNear > 0 && <Sky e={E45} p={sunNear} />}
      <Shadow x1={PX} x2={tipP} p={hot} hot />
      <g transform={`rotate(${rot} ${PX} ${GY})`}>
        <line x1={PX} y1={APEX_Y} x2={PX} y2={GY} stroke={C.amber} strokeWidth={8} strokeLinecap="round" opacity={sp(f, bs[2] + sec(0.2), bs[2] + sec(0.8))} />
        <circle cx={PX} cy={APEX_Y} r={9} fill={C.amber} opacity={sp(f, bs[2] + sec(0.2), bs[2] + sec(0.8))} />
      </g>
      <Par tx={tipP} e={E45} p={rays} />
      <DimV x={PX - PB - 40} y1={GY} y2={APEX_Y} label="H" p={sp(f, bs[2] + sec(0.2), bs[2] + sec(1.0)) * (1 - landed)} />
    </Svg>
  );
};

// ---------------------------------------------------------------- 11. Ngày nay: máy đo góc và tòa nhà
const SkylineBlds = [
  {x: 1130, w: 120, h: 230},
  {x: 1290, w: 170, h: 440},
  {x: 1480, w: 120, h: 300},
  {x: 1620, w: 140, h: 200},
  {x: 1780, w: 110, h: 340},
];

const Windows: React.FC<{f: number}> = ({f}) => (
  <g>
    {SkylineBlds.map((b, bi) => (
      <g key={bi}>
        <rect x={b.x} y={GY - b.h} width={b.w} height={b.h} fill="#1c130d" stroke={C.cream} strokeWidth={2} opacity={0.96} />
        {Array.from({length: Math.floor(b.h / 32) - 1}).map((_, r) =>
          Array.from({length: Math.floor(b.w / 28) - 0}).map((__, c) => {
            const h = (bi * 31 + r * 17 + c * 13) % 7;
            const lit = h < 3;
            return <rect key={`${r}-${c}`} x={b.x + 10 + c * 28} y={GY - b.h + 14 + r * 32} width={14} height={18} fill={lit ? C.amber : C.cream} opacity={lit ? 0.75 + 0.2 * Math.sin(f * 0.05 + h) : 0.1} />;
          })
        )}
      </g>
    ))}
  </g>
);

export const Tripod: React.FC<{x: number; s?: number; angle: number}> = ({x, s = 1, angle}) => {
  const hy = GY - 95 * s;
  const L = 62 * s;
  const a = (angle * Math.PI) / 180;
  return (
    <g stroke={C.cream} strokeLinecap="round">
      <line x1={x} y1={hy} x2={x - 34 * s} y2={GY} strokeWidth={5 * s} />
      <line x1={x} y1={hy} x2={x + 34 * s} y2={GY} strokeWidth={5 * s} />
      <line x1={x} y1={hy} x2={x + 4 * s} y2={GY} strokeWidth={5 * s} />
      <rect x={x - 15 * s} y={hy - 16 * s} width={30 * s} height={20 * s} rx={4} fill="#3a2a1c" strokeWidth={3} />
      <line x1={x} y1={hy - 8 * s} x2={x + Math.cos(a) * L} y2={hy - 8 * s - Math.sin(a) * L} strokeWidth={9 * s} stroke={C.amber} />
      <circle cx={x} cy={hy - 8 * s} r={7 * s} fill={C.cream} stroke="none" />
    </g>
  );
};

export const Modern: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const tag = sp(f, sec(0.2), sec(1.2));
  const wipe = 1 - sp(f, 0, sec(1.0));
  const bx = 700;
  const hy = GY - 95 - 8;
  const roofX = 1290;
  const roofY = GY - 440;
  const theta = (Math.atan2(hy - roofY, roofX - bx) * 180) / Math.PI;
  const tele = eio(lin(f, bs[1] + sec(0.8), bs[1] + sec(3.4)));
  const ang = theta * tele;
  const sight = sp(f, bs[1] + sec(3.2), bs[1] + sec(4.6));
  const base = sp(f, bs[1] + sec(0.2), bs[1] + sec(1.4));
  const arcP = sp(f, bs[1] + sec(3.6), bs[1] + sec(4.8));
  const dimh = sp(f, bs[2] + sec(0.2), bs[2] + sec(1.6));
  const formula = sp(f, bs[2] + sec(1.4), bs[2] + sec(2.6));
  const r = 90;
  const a = (theta * Math.PI) / 180;
  return (
    <Svg>
      <Dunes />
      <Birds />
      <Ground p={1} />
      <Windows f={f} />
      <path d={`M${bx} ${hy} L${roofX} ${hy} L${roofX} ${roofY} Z`} fill={C.amber} opacity={0.12 * sight} />
      <line x1={bx} y1={hy} x2={bx + (roofX - bx) * sight} y2={hy - (hy - roofY) * sight} stroke={C.amber} strokeWidth={3.5} strokeDasharray="14 10" />
      <Tripod x={bx} angle={ang} />
      <Walker x={bx - 85} dir={1} size={100} robe="#8fb4c9" hat={false} />
      <path d={`M${bx + r} ${hy} A${r} ${r} 0 0 0 ${bx + r * Math.cos(a)} ${hy - r * Math.sin(a)}`} fill="none" stroke={C.amber} strokeWidth={5} strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - arcP} />
      <Txt x={bx + 150} y={hy - 28} size={36} color={C.amber} opacity={arcP}>
        {t.angle}
      </Txt>
      <DimH x1={bx} x2={roofX} y={GY + 52} label={t.baseLine} p={base} size={38} />
      <DimV x={roofX - 20} y1={GY} y2={roofY} label="h" p={dimh} size={40} color={C.amber} />
      <Txt x={900} y={190} size={50} color={C.cream} opacity={formula}>
        {t.formula}
      </Txt>
      <text x={110} y={140} fontFamily="Cormorant" fontWeight={600} fontSize={64} fill={C.amber} opacity={tag} letterSpacing={6}>
        {t.nowTag}
      </text>
      <rect x={0} y={0} width={1920} height={1080} fill={C.bg2} opacity={wipe} />
    </Svg>
  );
};

// ---------------------------------------------------------------- 12. Everest
export const Everest: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const peak = {x: 1480, y: 330};
  const st = [460, 340, 220, 100];
  const sightP = sp(f, bs[0] + sec(0.6), bs[0] + sec(3.2));
  const far = sp(f, bs[0] + sec(3.0), bs[0] + sec(4.4));
  const tri = [0, 1, 2].map((i) => sp(f, bs[1] + sec(0.6 + 1.0 * i), bs[1] + sec(1.4 + 1.0 * i)));
  const std = sp(f, bs[1] + sec(3.8), bs[1] + sec(5.0));
  const v1856 = sp(f, bs[2] + sec(0.8), bs[2] + sec(1.8));
  const v2020 = sp(f, bs[3] + sec(0.8), bs[3] + sec(1.8));
  const hy = GY - 70;
  return (
    <Svg>
      <defs>
        <linearGradient id="mtn" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#4a3626" />
          <stop offset="100%" stopColor="#1b120c" />
        </linearGradient>
      </defs>
      <Dunes />
      <Birds />
      <Ground p={1} />
      <path d={`M1120 ${GY} L1250 570 L1320 610 L1410 450 L${peak.x} ${peak.y} L1560 470 L1620 440 L1740 600 L1860 ${GY} Z`} fill="url(#mtn)" stroke={C.cream} strokeWidth={3} strokeLinejoin="round" opacity={0.97} />
      <path d={`M1442 396 L${peak.x} ${peak.y} L1522 402 L1500 392 L1480 414 L1460 392 Z`} fill="#f6ead0" opacity={0.92} />
      <path d={`M1410 450 L1440 490 M1560 470 L1540 520`} stroke={C.cream} strokeWidth={2} opacity={0.3} fill="none" />
      {[0, 1, 2].map((i) => {
        const xa = st[i];
        const xb = st[i + 1];
        const xm = (xa + xb) / 2;
        return (
          <g key={i} opacity={tri[i]}>
            <path d={`M${xa} ${GY} L${xb} ${GY} L${xm} ${GY - 118 * tri[i]} Z`} fill={C.amber} fillOpacity={0.12} stroke={C.amber} strokeWidth={3.5} strokeLinejoin="round" />
          </g>
        );
      })}
      {st.map((x, i) => (
        <Tripod key={x} x={x} s={0.5} angle={i === 0 ? ((Math.atan2(hy - peak.y, peak.x - st[0]) * 180) / Math.PI) * sightP : 0} />
      ))}
      <line x1={st[0]} y1={hy} x2={st[0] + (peak.x - st[0]) * sightP} y2={hy - (hy - peak.y) * sightP} stroke={C.amber} strokeWidth={3.5} strokeDasharray="14 10" />
      <DimH x1={st[0]} x2={peak.x} y={GY + 52} label={t.far} p={far} size={36} color={C.amber} />
      <DimH x1={st[3]} x2={st[2]} y={GY + 52} label={t.baseStd} p={std} size={32} />
      <Txt x={900} y={190} size={54} color={C.cream} opacity={v1856}>
        {t.ev1856}
      </Txt>
      <Txt x={900} y={260} size={60} color={C.amber} opacity={v2020}>
        {t.ev2020}
      </Txt>
    </Svg>
  );
};

// ---------------------------------------------------------------- 13. Đời thường: đo cây bằng bóng, mô hình thu nhỏ
export const Everyday: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const A = 1 - seg(f, bs[1] - sec(0.4), bs[1] + sec(0.6));
  const treeH = 310;
  const tx = 500;
  const sx = 1250;
  const sh = 110;
  const e = E32;
  const treeTip = tx + treeH * 1.5;
  const stickTip = sx + sh * 1.5;
  const grow = sp(f, sec(0.2), sec(1.6));
  const sunP = sp(f, sec(0.2), sec(1.2));
  const rays = sp(f, bs[0] + sec(2.0), bs[0] + sec(4.4));
  const shp = sp(f, bs[0] + sec(3.6), bs[0] + sec(5.2));
  const eq = sp(f, bs[0] + sec(6.0), bs[0] + sec(7.4));
  const dims = sp(f, bs[0] + sec(4.8), bs[0] + sec(6.2));
  const B = sp(f, bs[1] - sec(0.2), bs[1] + sec(0.8)) * (1 - seg(f, bs[2] + sec(0.0), bs[2] + sec(1.0)));
  const sc = lerp(0.25, 1, eio(lin(f, bs[1] + sec(1.0), bs[1] + sec(5.2))));
  const C3 = sp(f, bs[2] + sec(0.6), bs[2] + sec(1.8));
  return (
    <Svg>
      <Dunes />
      <Birds />
      <Ground p={1} />
      <g opacity={A}>
        <g opacity={grow}>
          <rect x={tx - 15} y={GY - 130} width={30} height={130} fill="#6b4a32" />
          {[[tx, GY - 190, 72], [tx - 52, GY - 158, 56], [tx + 52, GY - 158, 56], [tx, GY - 252, 58]].map(([cx, cy, r], i) => (
            <circle key={i} cx={cx} cy={cy} r={r} fill="#7d8a4a" stroke="#c4cf8b" strokeWidth={2.5} opacity={0.95} />
          ))}
        </g>
        <Sun x={190} y={140} p={sunP} />
        <Shadow x1={tx} x2={treeTip} p={shp} />
        <Stick2 x={sx} h={sh} />
        <Shadow x1={sx} x2={stickTip} p={shp} hot />
        <Walker x={sx + 120} dir={-1} size={96} robe="#e8b86a" />
        <Par tx={treeTip} e={e} p={rays} o={0.5} />
        <Par tx={stickTip} e={e} p={rays} o={0.5} />
        <DimV x={tx - 100} y1={GY} y2={GY - treeH} label="?" p={dims} size={70} color={C.amber} />
        <DimH x1={tx} x2={treeTip} y={GY + 52} label="S" p={dims} size={38} />
        <DimV x={sx - 34} y1={GY} y2={GY - sh} label="h" p={dims} size={36} />
        <DimH x1={sx} x2={stickTip} y={GY + 52} label="s" p={dims} size={36} />
        <Txt x={1380} y={290} size={80} opacity={eq}>
          H / S  =  h / s
        </Txt>
      </g>
      <g opacity={B}>
        <g transform={`translate(${1100} ${GY}) scale(${sc}) translate(${-PX} ${-GY})`}>
          <Pyramid2 p={1} />
        </g>
        <Txt x={1100} y={GY + 62} size={40} color={C.amber} opacity={1 - seg(sc, 0.3, 0.6)}>
          {t.model}
        </Txt>
        <Txt x={1100} y={GY + 62} size={40} color={C.amber} opacity={seg(sc, 0.9, 1)}>
          {t.real}
        </Txt>
      </g>
      <g opacity={C3}>
        <rect x={0} y={0} width={1920} height={1080} fill={C.bg2} opacity={0.82} />
        <g transform="translate(960 420)">
          <line x1={-260} y1={-60} x2={-260} y2={60} stroke={C.cream} strokeWidth={6} strokeLinecap="round" />
          <line x1={-290} y1={-60} x2={-230} y2={-60} stroke={C.cream} strokeWidth={5} />
          <line x1={-290} y1={60} x2={-230} y2={60} stroke={C.cream} strokeWidth={5} />
          <path d="M-190 0 L-90 0" stroke={C.amber} strokeWidth={6} strokeLinecap="round" />
          <path d="M-110 -18 L-80 0 L-110 18" fill="none" stroke={C.amber} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" />
          <line x1={-40} y1={60} x2={260} y2={60} stroke={C.amber} strokeWidth={14} strokeLinecap="round" />
          <line x1={-40} y1={42} x2={-40} y2={78} stroke={C.amber} strokeWidth={4} />
          <line x1={260} y1={42} x2={260} y2={78} stroke={C.amber} strokeWidth={4} />
        </g>
      </g>
    </Svg>
  );
};
