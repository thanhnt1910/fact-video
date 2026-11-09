import React from 'react';
import {useCurrentFrame} from 'remotion';
import {APEX_Y, C, GY, PB, PH, PX, clamp01, eio, sec, seg, sp} from '../lib/theme';
import {Defs, DimH, DimV, FlameMark, Ground, Ray, Shadow, Sun, Txt} from '../thales/parts';
import {AngleArc, Birds, Camel, Clock, Cloud, Defs2, Dunes, Ladder, Palm, PlanView, Pyramid2, Stick2, WALKER_H, Walker} from './parts2';

export type Sc = {dur: number; bs: number[]; t: Record<string, string>};

export const Svg: React.FC<{children: React.ReactNode}> = ({children}) => (
  <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{position: 'absolute', left: 0, top: 0}}>
    <Defs />
    <Defs2 />
    {children}
  </svg>
);

export const RAD = Math.PI / 180;
export const tanE = (e: number) => Math.tan(e * RAD);
export const pyrTip = (e: number) => PX + PH / tanE(e);
export const lin = (f: number, a: number, b: number) => clamp01((f - a) / Math.max(1, b - a));
export const lerp = (a: number, b: number, k: number) => a + (b - a) * k;

export const FX = 1520; // chỗ Thales đứng ban đầu
export const EDGE = PX + PB; // mép đáy (938)
export const E45 = 45;
export const E32 = (Math.atan(2 / 3) * 180) / Math.PI; // 33,69 độ: gậy 80 -> bóng 120
export const TIP = PX + 1.5 * PH; // 1210
export const SH = 160; // chiều cao cây gậy vẽ
export const STICK_TIP = TIP + 1.5 * SH; // bóng gậy 3:2
const WH = WALKER_H;
const EQ_X = 1380;

/** Vị trí mặt trời nằm trên tia đi qua đỉnh kim tự tháp */
export const sunPos = (e: number) => ({x: PX - 420 * Math.cos(e * RAD), y: APEX_Y - 420 * Math.sin(e * RAD)});

/** Tia nắng song song kết thúc tại (tx, GY) */
export const Par: React.FC<{tx: number; e: number; p: number; o?: number}> = ({tx, e, p, o = 0.6}) => {
  const L = 1100;
  return <Ray x1={tx - L * Math.cos(e * RAD)} y1={GY - L * Math.sin(e * RAD)} x2={tx} y2={GY} p={p} opacity={o} />;
};

export const Sky: React.FC<{e: number; p?: number}> = ({e, p = 1}) => {
  const s = sunPos(e);
  return <Sun x={s.x} y={s.y} p={p} />;
};

// ---------------------------------------------------------------- 1. Mở đầu
export const Hook: React.FC<Sc> = ({dur, bs, t}) => {
  const f = useCurrentFrame();
  const ground = sp(f, 0, sec(1.2));
  const pyr = sp(f, sec(0.4), sec(4.6));
  const zoom = 1 + 0.08 * seg(f, 0, dur);
  const titleO = seg(f, sec(0.3), sec(1.3)) * (1 - seg(f, sec(5.0), sec(6.2)));
  const caravan = 2150 - 170 * (f / 30);
  const wk = lin(f, bs[1] + sec(0.3), bs[1] + sec(3.6));
  const tx = lerp(1900, FX, wk);
  const walking = wk > 0 && wk < 1;
  const cl = sp(f, bs[2] + sec(0.2), bs[2] + sec(1.4));
  const cross = sp(f, bs[2] + sec(3.2), bs[2] + sec(4.4));
  const q = seg(f, bs[2] + sec(5.2), bs[2] + sec(6.2));
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
        <Walker x={tx} dir={-1} walking={walking} p={sp(f, bs[1], bs[1] + sec(0.6))} />
        <Cloud cx={1500} cy={360} rx={200} ry={110} p={cl} tail={[FX, GY - 100]}>
          <Ladder cx={1440} cy={360} />
          <g stroke={C.amber} strokeWidth={9} strokeLinecap="round" opacity={cross} fill="none">
            <line x1={1405} y1={315} x2={1405 + 70 * cross} y2={315 + 90 * cross} />
            <line x1={1475} y1={315} x2={1475 - 70 * cross} y2={315 + 90 * cross} />
          </g>
          <Txt x={1560} y={398} size={130} color={C.amber} opacity={q}>
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

// ---------------------------------------------------------------- 2. Mặt Trời và cái bóng
export const SunShadow: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const k = eio(lin(f, bs[2] + sec(0.4), bs[3] - sec(0.4)));
  const e = lerp(25, E45, k);
  const sunP = sp(f, sec(0.2), sec(1.2));
  const shP = sp(f, bs[1] + sec(0.2), bs[1] + sec(2.0));
  const rayP = sp(f, bs[1] + sec(1.2), bs[1] + sec(3.4));
  const arcP = sp(f, bs[1] + sec(3.2), bs[1] + sec(4.4));
  const dimP = sp(f, bs[3] + sec(0.4), bs[3] + sec(2.0));
  const eqP = sp(f, bs[3] + sec(2.4), bs[3] + sec(3.6));
  const hLen = WH / tanE(e);
  const tipF = FX + hLen;
  return (
    <Svg>
      <Dunes />
      <Palm x={100} />
      <Birds />
      <Ground p={1} />
      <Pyramid2 p={1} />
      <Shadow x1={PX} x2={pyrTip(e)} p={shP} />
      <Walker x={FX} dir={-1} shadowLen={hLen} />
      <Sky e={e} p={sunP} />
      <Par tx={pyrTip(e)} e={e} p={rayP} />
      <Par tx={tipF} e={e} p={rayP} />
      <AngleArc tx={tipF} e={e} p={arcP} />
      <Txt x={tipF - 118} y={GY - 20} size={34} color={C.amber} opacity={arcP * (1 - dimP)}>
        {t.angle}
      </Txt>
      <Clock x={130} y={130} hour={9 + 3 * k} o={sp(f, bs[1], bs[1] + sec(1))} />
      <DimV x={FX - 40} y1={GY} y2={GY - WH} label="h" p={dimP} size={38} />
      <DimH x1={FX} x2={FX + WH} y={GY + 52} label="s" p={dimP} size={38} color={C.amber} />
      <Txt x={FX - 60} y={330} size={104} color={C.amber} opacity={eqP}>
        s = h
      </Txt>
    </Svg>
  );
};

// ---------------------------------------------------------------- 3. Lúc bóng bằng người
export const Equal: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const tipP = PX + PH;
  const arcs = sp(f, bs[1] + sec(0.2), bs[1] + sec(1.6));
  const hDim = sp(f, bs[1] + sec(1.8), bs[1] + sec(3.4));
  const eq = sp(f, bs[1] + sec(3.6), bs[1] + sec(4.8));
  const wk = lin(f, bs[2] + sec(0.4), bs[2] + sec(5.4));
  const wx = lerp(FX, tipP, wk);
  const walking = wk > 0 && wk < 1;
  const pulse = 0.55 + 0.45 * Math.sin(f * 0.18);
  return (
    <Svg>
      <Dunes />
      <Palm x={100} />
      <Birds />
      <Ground p={1} />
      <Pyramid2 p={1} axis />
      <Shadow x1={PX} x2={tipP} p={1} hot={f > bs[1]} />
      <Sky e={E45} />
      <Par tx={tipP} e={E45} p={1} />
      <Par tx={FX + WH} e={E45} p={1} />
      <g opacity={arcs * (0.6 + 0.4 * pulse)}>
        <AngleArc tx={tipP} e={E45} p={arcs} />
        <AngleArc tx={FX + WH} e={E45} p={arcs} />
      </g>
      <Walker x={wx} dir={-1} walking={walking} shadowLen={WH} />
      <DimV x={PX - PB - 40} y1={GY} y2={APEX_Y} label="H" p={hDim} />
      <DimH x1={PX} x2={tipP} y={GY + 52} label="S" p={hDim} color={C.amber} size={38} />
      <Txt x={EQ_X} y={300} size={96} color={C.amber} opacity={eq}>
        H = S
      </Txt>
    </Svg>
  );
};

// ---------------------------------------------------------------- 4. Vướng mắc: nửa cạnh đáy
export const Half: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const tipP = PX + PH;
  const wk = lin(f, sec(0.2), sec(1.4));
  const wx = lerp(tipP, EDGE, wk);
  const walking = wk > 0 && wk < 1;
  const axisP = sp(f, bs[0] + sec(1.8), bs[0] + sec(3.4));
  const hDim = sp(f, bs[0] + sec(3.0), bs[0] + sec(4.4));
  const cloudP = sp(f, bs[1] - sec(0.2), bs[1] + sec(1.2)) * (1 - seg(f, bs[2] - sec(0.4), bs[2] + sec(0.4)));
  const arrowP = sp(f, bs[1] + sec(1.4), bs[1] + sec(3.2));
  const half = sp(f, bs[2] + sec(0.2), bs[2] + sec(1.6));
  const meas = sp(f, bs[2] + sec(1.4), bs[2] + sec(2.8));
  const eq = sp(f, bs[2] + sec(2.6), bs[2] + sec(3.8));
  const hot = sp(f, sec(1.2), sec(2.2));
  return (
    <Svg>
      <Dunes />
      <Palm x={100} />
      <Birds />
      <Ground p={1} />
      <Pyramid2 p={1} />
      <Shadow x1={PX} x2={tipP} p={1} />
      <Shadow x1={EDGE} x2={tipP} p={hot} hot />
      <Sky e={E45} />
      <Par tx={tipP} e={E45} p={1} o={0.4} />
      <line x1={PX} y1={APEX_Y} x2={PX} y2={GY} stroke={C.amber} strokeWidth={6} strokeLinecap="round" opacity={0.9} strokeDasharray="1 1" pathLength={1} strokeDashoffset={1 - axisP} />
      <circle cx={PX} cy={GY} r={10 * axisP} fill={C.amber} />
      <circle cx={EDGE} cy={GY} r={10 * hot} fill={C.cream} />
      <Walker x={wx} dir={-1} walking={walking} shadowLen={0} />
      <DimV x={PX - PB - 40} y1={GY} y2={APEX_Y} label="H" p={hDim} />
      <Cloud cx={1340} cy={320} rx={290} ry={165} p={cloudP} tail={[tipP + 10, GY - 120]}>
        <PlanView cx={1270} cy={320} side={190} arrowP={arrowP} />
        <Txt x={1390} y={310} size={32} color={C.amber} anchor="start" opacity={arrowP}>
          {t.halfBase}
        </Txt>
      </Cloud>
      <DimH x1={PX} x2={EDGE} y={GY + 52} label={t.halfBase} p={half} size={34} />
      <DimH x1={EDGE} x2={tipP} y={GY + 52} label={t.measured} p={meas} size={34} color={C.amber} />
      <Txt x={EQ_X + 60} y={300} size={58} color={C.amber} opacity={eq}>
        {`H = ${t.halfBase} + ${t.measured}`}
      </Txt>
    </Svg>
  );
};

// ---------------------------------------------------------------- 5. Mẹo cây gậy: tam giác đồng dạng
export const StickTrick: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const k = eio(lin(f, sec(0.4), bs[1] - sec(0.4)));
  const e = lerp(E45, E32, k);
  const walk1 = lin(f, bs[1] + sec(0.3), bs[1] + sec(3.0));
  const plantStart = bs[1] + sec(3.0);
  const stickP = sp(f, plantStart, plantStart + sec(0.7));
  const walk2 = lin(f, plantStart + sec(0.9), plantStart + sec(4.2));
  const planted = f > plantStart;
  let wx = lerp(EDGE, TIP, walk1);
  if (f > plantStart + sec(0.9)) wx = lerp(TIP, FX, walk2);
  const walking = (walk1 > 0 && walk1 < 1) || (walk2 > 0 && walk2 < 1);
  const stickSh = sp(f, plantStart + sec(0.5), plantStart + sec(1.6));
  const rays = sp(f, bs[2] + sec(0.3), bs[2] + sec(2.4));
  const arcs = sp(f, bs[2] + sec(2.2), bs[2] + sec(3.4));
  const fills = sp(f, bs[3] + sec(0.1), bs[3] + sec(1.0)) * (1 - seg(f, bs[4] + sec(0.2), bs[4] + sec(1.2)));
  const grow = eio(lin(f, bs[3] + sec(1.6), bs[3] + sec(5.0)));
  const copyO = sp(f, bs[3] + sec(1.4), bs[3] + sec(1.8)) * (1 - seg(f, bs[4] + sec(0.2), bs[4] + sec(1.2)));
  const dims = sp(f, bs[4] + sec(1.0), bs[4] + sec(2.6));
  const eq = sp(f, bs[4] + sec(2.8), bs[4] + sec(4.0));
  const sameAngle = sp(f, bs[2] + sec(2.8), bs[2] + sec(3.8)) * (1 - seg(f, bs[3] - sec(0.2), bs[3] + sec(0.6)));
  const sameShape = sp(f, bs[3] + sec(4.6), bs[3] + sec(5.6)) * (1 - seg(f, bs[4] + sec(0.2), bs[4] + sec(1.0)));
  const raysO = 0.6 * (1 - 0.6 * seg(f, bs[4] + sec(0.2), bs[4] + sec(1.2)));
  const sc = lerp(1, PH / SH, grow);
  const tx = lerp(STICK_TIP, TIP, grow);
  const tipNow = pyrTip(e);
  return (
    <Svg>
      <Dunes />
      <Palm x={100} />
      <Birds />
      <Ground p={1} />
      <Pyramid2 p={1} />
      <Shadow x1={PX} x2={tipNow} p={1} />
      <path d={`M${PX} ${APEX_Y} L${PX} ${GY} L${TIP} ${GY} Z`} fill={C.amber} opacity={0.12 * fills} />
      <path d={`M${TIP} ${GY - SH} L${TIP} ${GY} L${STICK_TIP} ${GY} Z`} fill={C.amber} opacity={0.38 * fills} />
      <Sky e={e} />
      {planted && <Stick2 x={TIP} h={SH} p={stickP} />}
      <Shadow x1={TIP} x2={STICK_TIP} p={stickSh} hot />
      <Walker x={wx} dir={walk2 > 0 ? 1 : 1} walking={walking} staff={!planted} shadowLen={WH / tanE(e)} />
      <Par tx={TIP} e={E32} p={rays} o={raysO} />
      <Par tx={STICK_TIP} e={E32} p={rays} o={raysO} />
      <AngleArc tx={TIP} e={E32} p={arcs} r={60} />
      <AngleArc tx={STICK_TIP} e={E32} p={arcs} r={44} />
      {/* tam giác nhỏ được phóng to rồi chồng lên tam giác lớn */}
      <g opacity={copyO}>
        <g transform={`translate(${tx} ${GY}) scale(${sc}) translate(${-STICK_TIP} ${-GY})`}>
          <path d={`M${TIP} ${GY - SH} L${TIP} ${GY} L${STICK_TIP} ${GY} Z`} fill={C.cream} fillOpacity={0.18} stroke={C.cream} strokeWidth={4 / sc} strokeLinejoin="round" />
        </g>
      </g>
      <DimV x={PX - PB - 40} y1={GY} y2={APEX_Y} label="H" p={dims} />
      <DimH x1={PX} x2={TIP} y={GY + 52} label="S" p={dims} size={38} color={C.amber} />
      <DimV x={TIP - 30} y1={GY} y2={GY - SH} label="h" p={dims} size={34} />
      <DimH x1={TIP} x2={STICK_TIP} y={GY + 52} label="s" p={dims} size={38} />
      <Txt x={EQ_X} y={300} size={64} color={C.amber} opacity={sameAngle}>
        {t.sameAngle}
      </Txt>
      <Txt x={EQ_X} y={300} size={64} color={C.amber} opacity={sameShape}>
        {t.sameShape}
      </Txt>
      <Txt x={EQ_X} y={300} size={84} opacity={eq}>
        H / S  =  h / s
      </Txt>
    </Svg>
  );
};

// ---------------------------------------------------------------- 6. Con số
export const Numbers: React.FC<Sc> = ({bs, t}) => {
  const f = useCurrentFrame();
  const stickD = sp(f, sec(0.6), sec(1.8));
  const shadowD = sp(f, sec(1.4), sec(2.8));
  const ratio = sp(f, bs[1] + sec(0.4), bs[1] + sec(1.6)) * (1 - seg(f, bs[2] + sec(0.2), bs[2] + sec(1.0)));
  const long = sp(f, bs[2] + sec(0.4), bs[2] + sec(2.2));
  const eq = sp(f, bs[2] + sec(2.6), bs[2] + sec(3.8));
  const res = sp(f, bs[2] + sec(4.8), bs[2] + sec(6.0));
  const hDim = sp(f, bs[2] + sec(5.0), bs[2] + sec(6.4));
  const cmp = sp(f, bs[3] + sec(0.4), bs[3] + sec(1.6));
  return (
    <Svg>
      <Dunes />
      <Palm x={100} />
      <Birds />
      <Ground p={1} />
      <Pyramid2 p={1} />
      <Shadow x1={PX} x2={TIP} p={1} />
      <Sky e={E32} />
      <Stick2 x={TIP} h={SH} />
      <Shadow x1={TIP} x2={STICK_TIP} p={1} hot />
      <Walker x={FX} dir={-1} shadowLen={WH / tanE(E32)} />
      <DimV x={TIP - 36} y1={GY} y2={GY - SH} label="2 m" p={stickD} size={36} />
      <DimH x1={TIP} x2={STICK_TIP} y={GY + 52} label="3 m" p={shadowD} size={36} color={C.amber} />
      <DimH x1={PX} x2={TIP} y={GY + 52} label="220 m" p={long} size={38} />
      <Txt x={EQ_X} y={290} size={58} color={C.amber} opacity={ratio}>
        {t.ratio}
      </Txt>
      <Txt x={EQ_X} y={290} size={72} opacity={eq}>
        H = 220 × 2 ÷ 3
      </Txt>
      <Txt x={EQ_X} y={392} size={112} color={C.amber} opacity={res}>
        ≈ 147 m
      </Txt>
      <DimV x={PX - PB - 40} y1={GY} y2={APEX_Y} label="≈ 147 m" p={hDim} color={C.amber} />
      <Txt x={EQ_X} y={480} size={40} color={C.dim} opacity={cmp}>
        {t.built}
      </Txt>
      <Txt x={EQ_X} y={534} size={40} color={C.dim} opacity={cmp}>
        {t.today}
      </Txt>
      <Txt x={1850} y={830} size={28} color={C.dim} anchor="end" opacity={0.75 * stickD}>
        {t.scale}
      </Txt>
    </Svg>
  );
};

// ---------------------------------------------------------------- 7. Kết
export const Finale: React.FC<Sc> = ({dur, bs, t}) => {
  const f = useCurrentFrame();
  const endStart = bs[bs.length - 1];
  const card = sp(f, endStart, endStart + sec(0.9));
  const word = sp(f, endStart + sec(0.5), endStart + sec(1.5));
  const tag = sp(f, endStart + sec(1.2), endStart + sec(2.2));
  const wk = lin(f, sec(0.4), sec(4.4));
  const wx = lerp(FX, 1380, wk);
  const caravan = -250 + 190 * (f / 30);
  const zoom = 1 + 0.06 * seg(f, 0, endStart);
  return (
    <>
      <Svg>
        <g opacity={0.95 - 0.85 * card}>
          <g transform={`translate(960 600) scale(${zoom}) translate(-960 -600)`}>
            <Dunes />
      <Palm x={100} />
      <Birds />
            <Ground p={1} />
            <Pyramid2 p={1} />
            <Shadow x1={PX} x2={TIP} p={1} />
            <Sky e={E32} />
            <Stick2 x={TIP} h={SH} />
            <Shadow x1={TIP} x2={STICK_TIP} p={1} hot />
            {[0, 330, 700].map((off, i) => (
              <Camel key={i} x={caravan - off} dir={1} s={1.05} phase0={i * 1.3} />
            ))}
            <Walker x={wx} dir={-1} walking={wk > 0 && wk < 1} shadowLen={WH / tanE(E32)} />
          </g>
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
