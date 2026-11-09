import React from 'react';
import {useCurrentFrame} from 'remotion';
import {APEX_Y, C, GY, PB, PH, PX, clamp01, sec, seg, sp} from '../lib/theme';
import {Defs, DimH, DimV, Figure, FlameMark, Ground, Pyramid, Ray, Shadow, Stick, Sun, Txt} from './parts';

export type Sc = {dur: number; bs: number[]; t: Record<string, string>};

const Svg: React.FC<{children: React.ReactNode}> = ({children}) => (
  <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{position: 'absolute', left: 0, top: 0}}>
    <Defs />
    {children}
  </svg>
);

// Cảnh với tỉ lệ 3:2 (gậy 80 -> bóng 120; bóng kim tự tháp tính từ tâm = 570)
const TIP = PX + 1.5 * PH; // 1210
const STICK_X = TIP;
const STICK_TIP = TIP + 120; // 1330

export const Intro: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const ground = sp(f, 0, sec(1.2));
  const pyr = sp(f, sec(0.4), sec(4.6));
  const fs = bs[2] + sec(0.4);
  const figP = sp(f, fs, fs + sec(1.2));
  const figX = 1800 - 300 * sp(f, fs, fs + sec(2.6));
  const sunP = sp(f, bs[2] + sec(1.8), bs[2] + sec(3.0));
  const titleO = seg(f, sec(0.3), sec(1.3)) * (1 - seg(f, sec(5.2), sec(6.4)));
  return (
    <Svg>
      <Ground p={ground} />
      <Pyramid p={pyr} axis={false} />
      <Figure x={figX} p={figP} />
      <Sun x={220} y={100} p={sunP} />
      <text x={960} y={215} textAnchor="middle" fontFamily="Cormorant" fontWeight={600} fontSize={92} fill={C.cream} opacity={titleO}>
        {t.title}
      </text>
    </Svg>
  );
};

export const Rays: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const sunP = sp(f, sec(0.2), sec(1.2));
  const r1 = sp(f, bs[0] + sec(0.8), bs[0] + sec(3.0));
  const r2 = sp(f, bs[0] + sec(1.6), bs[0] + sec(3.8));
  const shP = sp(f, bs[1] + sec(0.3), bs[1] + sec(2.8));
  const stP = sp(f, bs[1] + sec(1.0), bs[1] + sec(1.8));
  const st2 = sp(f, bs[1] + sec(2.0), bs[1] + sec(3.0));
  const lab = sp(f, bs[1] + sec(3.2), bs[1] + sec(4.2));
  return (
    <Svg>
      <Ground p={1} />
      <Pyramid p={1} axis={false} />
      <Shadow x1={PX} x2={TIP} p={shP} />
      <Stick x={STICK_X} p={stP} />
      <Shadow x1={TIP} x2={STICK_TIP} p={st2} hot />
      <Sun x={220} y={100} p={sunP} />
      <Ray x1={257} y1={124} x2={TIP} y2={GY} p={r1} />
      <Ray x1={370} y1={120} x2={STICK_TIP} y2={GY} p={r2} />
      <Txt x={(PX + TIP) / 2} y={GY + 78} size={40} opacity={lab}>
        {t.longShadow}
      </Txt>
      <Txt x={(TIP + STICK_TIP) / 2 + 30} y={GY + 78} size={40} opacity={lab}>
        {t.shortShadow}
      </Txt>
    </Svg>
  );
};

export const Equal: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const sunP = sp(f, 0, sec(0.8));
  const figP = sp(f, sec(0.3), sec(1.2));
  const fshP = sp(f, sec(1.3), sec(2.9));
  const r2 = sp(f, sec(0.8), sec(2.9));
  const hDim = sp(f, sec(3.2), sec(4.2));
  const r1 = sp(f, bs[1] + sec(0.3), bs[1] + sec(2.4));
  const pshP = sp(f, bs[1] + sec(0.8), bs[1] + sec(3.4));
  const hP = sp(f, bs[1] + sec(3.6), bs[1] + sec(4.8));
  const halfP = sp(f, bs[2] + sec(0.3), bs[2] + sec(1.6));
  const measP = sp(f, bs[2] + sec(1.2), bs[2] + sec(2.4));
  const eqO = sp(f, bs[2] + sec(2.4), bs[2] + sec(3.4));
  const edge = PX + PB;
  const tip = PX + PH;
  return (
    <Svg>
      <Ground p={1} />
      <Pyramid p={1} />
      <Shadow x1={PX} x2={tip} p={pshP} />
      <Shadow x1={edge} x2={tip} p={measP} hot />
      <Figure x={1400} p={figP} />
      <Shadow x1={1400} x2={1480} p={fshP} hot />
      <Sun x={360} y={100} p={sunP} />
      <Ray x1={1000} y1={280} x2={1480} y2={GY} p={r2} />
      <Ray x1={400} y1={140} x2={tip} y2={GY} p={r1} />
      <DimV x={1360} y1={GY} y2={GY - 80} label="h" p={hDim} size={38} />
      <DimH x1={1400} x2={1480} y={GY + 52} label="h" p={hDim} size={38} />
      <DimV x={PX - PB - 40} y1={GY} y2={APEX_Y} label="H" p={hP} />
      <DimH x1={PX} x2={edge} y={GY + 52} label={t.halfBase} p={halfP} size={36} color={C.dim} />
      <DimH x1={edge} x2={tip} y={GY + 52} label={t.measured} p={measP} size={36} color={C.amber} />
      <Txt x={1380} y={300} size={54} opacity={eqO}>
        {`H = ${t.halfBase} + ${t.measured}`}
      </Txt>
    </Svg>
  );
};

export const Similar: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const rayO = sp(f, 0, sec(0.8));
  const stP = sp(f, bs[0] + sec(0.4), bs[0] + sec(1.4));
  const st2 = sp(f, bs[0] + sec(1.6), bs[0] + sec(2.6));
  const bigO = sp(f, bs[1] + sec(0.8), bs[1] + sec(2.4));
  const smallO = sp(f, bs[1] + sec(1.8), bs[1] + sec(3.2));
  const sameO = sp(f, bs[1] + sec(3.4), bs[1] + sec(4.4));
  const dimP = sp(f, bs[2] + sec(0.4), bs[2] + sec(1.8));
  const eqO = sp(f, bs[2] + sec(2.4), bs[2] + sec(3.6));
  return (
    <Svg>
      <Ground p={1} />
      <polygon points={`${PX},${APEX_Y} ${PX},${GY} ${TIP},${GY}`} fill={C.amber} opacity={0.14 * bigO} />
      <Pyramid p={1} />
      <Shadow x1={PX} x2={TIP} p={1} />
      <polygon points={`${STICK_X},${GY - 80} ${STICK_X},${GY} ${STICK_TIP},${GY}`} fill={C.amber} opacity={0.5 * smallO} />
      <Stick x={STICK_X} p={stP} />
      <Shadow x1={TIP} x2={STICK_TIP} p={st2} hot />
      <line x1={PX} y1={APEX_Y} x2={TIP} y2={GY} stroke={C.amber} strokeWidth={4} opacity={0.8 * bigO} />
      <Sun x={220} y={100} p={1} />
      <Ray x1={257} y1={124} x2={TIP} y2={GY} p={1} opacity={0.75 * rayO} />
      <Ray x1={370} y1={120} x2={STICK_TIP} y2={GY} p={1} opacity={0.75 * rayO} />
      <DimV x={PX - PB - 40} y1={GY} y2={APEX_Y} label="H" p={dimP} />
      <DimH x1={PX} x2={TIP} y={GY + 52} label="S" p={dimP} />
      <DimV x={STICK_X - 38} y1={GY} y2={GY - 80} label="h" p={dimP} size={38} />
      <DimH x1={TIP} x2={STICK_TIP} y={GY + 52} label="s" p={dimP} size={38} />
      <Txt x={1380} y={290} size={80} opacity={eqO}>
        {'H / S  =  h / s'}
      </Txt>
      <Txt x={1380} y={365} size={38} color={C.dim} opacity={sameO}>
        {t.sameShape}
      </Txt>
    </Svg>
  );
};

export const Numbers: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const stickDim = sp(f, bs[0] + sec(0.6), bs[0] + sec(1.8));
  const shadowDim = sp(f, bs[0] + sec(2.2), bs[0] + sec(3.4));
  const pDim = sp(f, bs[1] + sec(0.4), bs[1] + sec(2.0));
  const calc = sp(f, bs[2] + sec(0.3), bs[2] + sec(1.3));
  const result = sp(f, bs[2] + sec(1.8), bs[2] + sec(2.8));
  const hDim = sp(f, bs[2] + sec(2.6), bs[2] + sec(3.8));
  const cmp = sp(f, bs[3] + sec(0.5), bs[3] + sec(1.6));
  return (
    <Svg>
      <Ground p={1} />
      <Pyramid p={1} />
      <Shadow x1={PX} x2={TIP} p={1} />
      <Stick x={STICK_X} />
      <Shadow x1={TIP} x2={STICK_TIP} p={1} hot />
      <Sun x={220} y={100} p={1} />
      <Ray x1={257} y1={124} x2={TIP} y2={GY} p={1} opacity={0.4} />
      <Ray x1={370} y1={120} x2={STICK_TIP} y2={GY} p={1} opacity={0.4} />
      <DimV x={STICK_X - 38} y1={GY} y2={GY - 80} label="2 m" p={stickDim} size={38} />
      <DimH x1={TIP} x2={STICK_TIP} y={GY + 52} label="3 m" p={shadowDim} size={38} />
      <DimH x1={PX} x2={TIP} y={GY + 52} label="220 m" p={pDim} />
      <DimV x={PX - PB - 40} y1={GY} y2={APEX_Y} label="≈ 147 m" p={hDim} color={C.amber} />
      <Txt x={1400} y={250} size={60} opacity={calc}>
        {'H = 220 × 2 ÷ 3'}
      </Txt>
      <Txt x={1400} y={350} size={92} color={C.amber} opacity={result}>
        {'≈ 147 m'}
      </Txt>
      <Txt x={1400} y={440} size={40} color={C.dim} opacity={cmp}>
        {t.built}
      </Txt>
      <Txt x={1400} y={494} size={40} color={C.dim} opacity={cmp}>
        {t.today}
      </Txt>
    </Svg>
  );
};

export const Outro: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const endStart = bs[bs.length - 1];
  const card = sp(f, endStart, endStart + sec(0.9));
  const word = sp(f, endStart + sec(0.5), endStart + sec(1.5));
  const tag = sp(f, endStart + sec(1.2), endStart + sec(2.2));
  return (
    <>
      <Svg>
        <g opacity={0.9 - 0.8 * card}>
          <Ground p={1} />
          <Pyramid p={1} axis={false} />
          <Shadow x1={PX} x2={TIP} p={1} />
          <Stick x={STICK_X} />
          <Shadow x1={TIP} x2={STICK_TIP} p={1} hot />
          <Sun x={220} y={100} p={1} />
          <DimV x={PX - PB - 40} y1={GY} y2={APEX_Y} label="≈ 147 m" p={1} color={C.amber} />
        </g>
        <rect width={1920} height={1080} fill={C.bg2} opacity={0.94 * card} />
      </Svg>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 36, opacity: word, transform: `translateY(${(1 - word) * 24}px)`}}>
          <FlameMark width={110} />
          <div style={{fontFamily: 'Cormorant', fontWeight: 600, fontSize: 170, lineHeight: 1, color: C.cream, letterSpacing: '-0.01em'}}>
            Proof<span style={{color: C.amber}}>wick</span>
          </div>
        </div>
        <div style={{marginTop: 28, fontFamily: 'Lora, Georgia, serif', fontStyle: 'italic', fontSize: 46, color: C.dim, opacity: tag}}>{t.tag}</div>
      </div>
    </>
  );
};

export {clamp01};
