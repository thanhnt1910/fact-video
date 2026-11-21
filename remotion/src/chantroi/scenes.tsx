import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const WATER = '#2f6f96';
const RED = '#e0613b';
const AM = C.amber;
const CX = 540;

// Hình học dùng chung: Trái Đất (tâm E, bán kính r), mắt ở trên cao (vẽ phóng đại), điểm chạm H.
const E = {x: 640, y: 1010};
const R = 300;
const EYE = {x: 640, y: 618};
const H = {x: 833, y: 780};

const Hero2: React.FC<{f: number; cheer?: number}> = ({f, cheer = 0}) => <HatHero x={170} y={1250} s={2} walk={f * 0.13} cheer={cheer} hat="goggles" />;

// Chữ có số mũ: "R^2 + d^2" => R² + d² (tspan hạ/nâng dòng, tránh ký tự Unicode).
const Fx: React.FC<{x: number; y: number; size: number; color?: string; o?: number; t: string}> = ({x, y, size, color = C.cream, o = 1, t}) => {
  const parts = t.split(/\^(.)/);
  const out: React.ReactNode[] = [];
  let raised = false;
  parts.forEach((p, i) => {
    if (i % 2 === 0) {
      if (p) out.push(<tspan key={i} dy={raised ? size * 0.38 : 0}>{p}</tspan>);
      if (p) raised = false;
    } else {
      out.push(<tspan key={i} dy={-size * 0.38} fontSize={size * 0.6}>{p}</tspan>);
      raised = true;
    }
  });
  return (
    <Big x={x} y={y} size={size} color={color} o={o}>
      {out}
    </Big>
  );
};

const Ball: React.FC<{o?: number}> = ({o = 1}) => (
  <g opacity={o}>
    <circle cx={E.x} cy={E.y} r={R} fill={WATER} fillOpacity={0.4} stroke={C.cream} strokeWidth={5} />
  </g>
);
const Eye: React.FC<{o?: number; label?: boolean}> = ({o = 1, label = false}) => (
  <g opacity={o}>
    <line x1={E.x} y1={E.y - R} x2={EYE.x} y2={EYE.y} stroke={AM} strokeWidth={5} />
    <circle cx={EYE.x} cy={EYE.y} r={15} fill={AM} stroke={C.cream} strokeWidth={4} />
    {label && <Tag x={EYE.x + 40} y={EYE.y + 10} color={C.cream} size={36} anchor="start">mắt bạn</Tag>}
  </g>
);
const Tangent: React.FC<{p?: number; color?: string; w?: number}> = ({p = 1, color = AM, w = 6}) => (
  <line x1={EYE.x} y1={EYE.y} x2={lerp(EYE.x, H.x, clamp01(p))} y2={lerp(EYE.y, H.y, clamp01(p))} stroke={color} strokeWidth={w} strokeLinecap="round" />
);
const RightAngle: React.FC<{o?: number}> = ({o = 1}) => {
  const u = {x: (E.x - H.x) / R, y: (E.y - H.y) / R};
  const v = {x: (EYE.x - H.x) / 252, y: (EYE.y - H.y) / 252};
  const k = 32;
  const a = {x: H.x + u.x * k, y: H.y + u.y * k};
  const b = {x: a.x + v.x * k, y: a.y + v.y * k};
  const c = {x: H.x + v.x * k, y: H.y + v.y * k};
  return <path d={`M ${a.x} ${a.y} L ${b.x} ${b.y} L ${c.x} ${c.y}`} fill="none" stroke={RED} strokeWidth={5} opacity={o} />;
};
const Tri: React.FC<{o?: number; fill?: number}> = ({o = 1, fill = 0.18}) => (
  <g opacity={o}>
    <path d={`M ${E.x} ${E.y} L ${EYE.x} ${EYE.y} L ${H.x} ${H.y} Z`} fill={AM} fillOpacity={fill} stroke={C.cream} strokeWidth={5} strokeLinejoin="round" />
  </g>
);
const Dot: React.FC<{x: number; y: number; r?: number}> = ({x, y, r = 13}) => <circle cx={x} cy={y} r={r} fill={C.cream} stroke={AM} strokeWidth={4} />;

const Sea: React.FC<{f: number; y: number; bottom?: number}> = ({f, y, bottom = 1220}) => {
  let d = '';
  for (let x = 300; x <= 990; x += 10) d += `${x === 300 ? 'M' : 'L'} ${x} ${y + 6 * Math.sin(x * 0.02 - f * 0.1)} `;
  return (
    <g>
      <path d={`${d} L 990 ${bottom} L 300 ${bottom} Z`} fill={WATER} opacity={0.5} />
      <path d={d} fill="none" stroke={C.cream} strokeWidth={5} />
    </g>
  );
};
const ShipS: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M -80 0 L 80 0 L 56 40 L -56 40 Z" fill="#c9533a" stroke={C.cream} strokeWidth={5} strokeLinejoin="round" />
    <line x1={0} y1={0} x2={0} y2={-130} stroke={C.cream} strokeWidth={6} />
    <path d="M 4 -124 L 66 -30 L 4 -30 Z" fill={C.cream} opacity={0.9} />
  </g>
);
// Mặt biển cong (dùng cho cảnh 4 và 35): đường cong bậc hai, đỉnh ở (640, 880).
const CURVE = 'M 300 1000 Q 640 760 980 1000';
const Curve: React.FC = () => (
  <g>
    <path d={`${CURVE} L 980 1220 L 300 1220 Z`} fill={WATER} opacity={0.55} />
    <path d={CURVE} fill="none" stroke={C.cream} strokeWidth={5} />
  </g>
);

const P0: Panel = ({f}) => (
  <g>
    <Head a="Đường chân trời" b="xa bao nhiêu?" />
    <Sea f={f} y={900} />
    <Big x={640} y={760} size={170} color={AM} o={sp(f, 10, 26)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Không cần thước dây" b="chỉ cần tam giác vuông" />
    <g opacity={sp(f, 2, 14)}>
      <rect x={380} y={560} width={420} height={60} rx={8} fill="#d8c39a" stroke={C.cream} strokeWidth={4} />
      {Array.from({length: 11}).map((_, i) => <line key={i} x1={400 + i * 38} y1={560} x2={400 + i * 38} y2={i % 5 === 0 ? 596 : 582} stroke={C.ink} strokeWidth={3} />)}
    </g>
    <line x1={360} y1={640} x2={820} y2={540} stroke={RED} strokeWidth={14} strokeLinecap="round" opacity={sp(f, 16, 30)} />
    <g opacity={sp(f, 24, 40)}>
      <path d="M 400 1180 L 920 1180 L 920 760 Z" fill={AM} fillOpacity={0.18} stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
      <path d="M 888 1180 L 888 1148 L 920 1148" fill="none" stroke={RED} strokeWidth={5} />
    </g>
    <Hero2 f={f} />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Con số ra rất bất ngờ" />
    <Sea f={f} y={1000} />
    <Big x={640} y={840} size={170} color={AM} o={sp(f, 4, 20)}>≈ 5 km</Big>
    <Hero2 f={f} />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Đường chân trời" b="là chỗ mặt biển cong khuất đi" />
    <Curve />
    <circle cx={436} cy={880} r={15} fill={AM} stroke={C.cream} strokeWidth={4} />
    <line x1={436} y1={880} x2={640} y2={880} stroke={AM} strokeWidth={5} strokeDasharray="12 10" opacity={sp(f, 8, 24)} />
    <Tag x={640} y={800} color={C.cream} size={38} o={sp(f, 14, 28)}>chân trời</Tag>
    <line x1={640} y1={880} x2={980} y2={880} stroke={RED} strokeWidth={5} strokeDasharray="12 10" opacity={sp(f, 26, 40)} />
    <Tag x={880} y={840} color={RED} size={38} o={sp(f, 28, 42)}>khuất</Tag>
    <Hero2 f={f} />
  </g>
);
const P4: Panel = ({f}) => (
  <g>
    <Head a="Trái Đất như quả bóng" b="mắt bạn là chấm nhỏ" />
    <Ball o={sp(f, 2, 16)} />
    <Tag x={E.x} y={E.y + 12} color={C.cream} size={46} o={sp(f, 10, 24)}>Trái Đất</Tag>
    <Eye o={sp(f, 18, 34)} label />
    <Hero2 f={f} />
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Tia nhìn xa nhất" b="lướt sát mặt bóng" />
    <Ball />
    <Eye label />
    <Tangent p={sp(f, 4, 44)} />
    <Hero2 f={f} />
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Điểm chạm ấy" b="là đường chân trời" />
    <Ball />
    <Eye />
    <Tangent />
    <circle cx={H.x} cy={H.y} r={16 + 5 * Math.sin(f * 0.25)} fill={RED} fillOpacity={0.6} stroke={C.cream} strokeWidth={4} opacity={sp(f, 2, 12)} />
    <Tag x={915} y={725} color={C.cream} size={36} o={sp(f, 8, 22)}>chân trời</Tag>
    <Hero2 f={f} />
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Đường thẳng chạm đường tròn" b="vuông góc với bán kính" />
    <Ball />
    <Eye />
    <Tangent />
    <line x1={E.x} y1={E.y} x2={lerp(E.x, H.x, sp(f, 2, 28))} y2={lerp(E.y, H.y, sp(f, 2, 28))} stroke={C.cream} strokeWidth={5} strokeDasharray="12 10" />
    <RightAngle o={sp(f, 26, 40)} />
    <Tag x={760} y={870} color={RED} size={38} o={sp(f, 30, 44)}>90°</Tag>
    <Hero2 f={f} />
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Ta có tam giác vuông" />
    <Ball o={0.6} />
    <Tri o={sp(f, 2, 18)} />
    <RightAngle />
    <Tag x={E.x} y={E.y + 56} color={C.cream} size={34} o={sp(f, 18, 30)}>tâm Trái Đất</Tag>
    <Tag x={EYE.x + 36} y={EYE.y - 20} color={C.cream} size={34} anchor="start" o={sp(f, 28, 40)}>mắt bạn</Tag>
    <Tag x={915} y={725} color={C.cream} size={34} o={sp(f, 38, 50)}>chân trời</Tag>
    <Dot x={E.x} y={E.y} r={11} />
    <Dot x={EYE.x} y={EYE.y} r={11} />
    <Dot x={H.x} y={H.y} r={11} />
    <Hero2 f={f} />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Cạnh tới chân trời" b="là bán kính Trái Đất" />
    <Ball o={0.6} />
    <Tri />
    <line x1={E.x} y1={E.y} x2={H.x} y2={H.y} stroke={AM} strokeWidth={12} strokeLinecap="round" opacity={sp(f, 2, 14)} />
    <Tag x={770} y={960} color={AM} size={36} o={sp(f, 10, 24)}>R ≈ 6.371 km</Tag>
    <Hero2 f={f} />
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Cạnh tới mắt dài hơn" b="bán kính cộng chiều cao mắt" />
    <Ball o={0.6} />
    <Tri />
    <line x1={E.x} y1={E.y} x2={EYE.x} y2={EYE.y} stroke={AM} strokeWidth={12} strokeLinecap="round" opacity={sp(f, 2, 14)} />
    <Tag x={545} y={830} color={AM} size={44} o={sp(f, 10, 24)}>R + h</Tag>
    <Hero2 f={f} />
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Cạnh còn lại" b="là khoảng cách cần tìm" />
    <Ball o={0.6} />
    <Tri />
    <Tangent color={AM} w={12} p={sp(f, 2, 18)} />
    <Tag x={880} y={655} color={AM} size={44} o={sp(f, 12, 26)}>d = ?</Tag>
    <Hero2 f={f} />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Định lý Pythagoras" />
    <Fx x={CX + 100} y={760} size={120} color={AM} o={sp(f, 2, 18)} t="c^2 = a^2 + b^2" />
    <g opacity={sp(f, 18, 34)}>
      <path d="M 460 1180 L 900 1180 L 900 900 Z" fill={AM} fillOpacity={0.15} stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
      <path d="M 868 1180 L 868 1148 L 900 1148" fill="none" stroke={RED} strokeWidth={5} />
      <Tag x={655} y={1020} color={AM} size={52}>c</Tag>
      <Tag x={680} y={1228} color={C.cream} size={52}>a</Tag>
      <Tag x={940} y={1050} color={C.cream} size={52}>b</Tag>
    </g>
    <Hero2 f={f} />
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Cạnh huyền" b="là cạnh tới mắt" />
    <Fx x={CX + 100} y={780} size={110} color={AM} o={sp(f, 2, 16)} t="(R + h)^2" />
    <Fx x={CX + 100} y={930} size={110} color={C.cream} o={sp(f, 18, 34)} t="= R^2 + d^2" />
    <Hero2 f={f} />
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Khai triển ra" b="phần bán kính triệt tiêu" />
    <Fx x={CX + 100} y={780} size={62} color={C.cream} o={sp(f, 2, 16) * (1 - 0.55 * sp(f, 34, 48))} t="R^2 + 2Rh + h^2 = R^2 + d^2" />
    <Fx x={CX + 100} y={930} size={96} color={AM} o={sp(f, 34, 50)} t="2Rh + h^2 = d^2" />
    <Hero2 f={f} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Còn lại" b="khoảng cách bình phương" />
    <Fx x={CX + 100} y={830} size={120} color={AM} o={sp(f, 2, 18)} t="d^2 = 2Rh + h^2" />
    <Hero2 f={f} />
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Mắt chỉ cao 1,7 mét" b="quá nhỏ so với bán kính" />
    <Big x={CX + 100} y={760} size={110} color={C.cream} o={sp(f, 2, 14)}>
      d<tspan dy={-42} fontSize={66}>2</tspan>
      <tspan dy={42}> = 2Rh + </tspan>
      <tspan fill={RED} opacity={1 - 0.5 * sp(f, 30, 44)}>h<tspan dy={-42} fontSize={66}>2</tspan></tspan>
    </Big>
    <g opacity={sp(f, 26, 40)}><line x1={CX + 380} y1={745} x2={CX + 470} y2={700} stroke={RED} strokeWidth={10} strokeLinecap="round" /></g>
    <Fx x={CX + 100} y={940} size={120} color={AM} o={sp(f, 40, 56)} t="d^2 ≈ 2Rh" />
    <Hero2 f={f} />
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Khoảng cách tới chân trời" />
    <Big x={CX + 100} y={800} size={150} color={AM} o={sp(f, 2, 18)}>d = √(2Rh)</Big>
    <Tag x={CX + 100} y={910} color={C.cream} size={38} o={sp(f, 18, 32)}>căn bậc hai của 2 × R × h</Tag>
    <Hero2 f={f} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Đổi ra ki-lô-mét" />
    <Calc f={f} x={CX + 100} y={760} step={150} lines={[{t: '1,7 m', at: 2, size: 130}, {t: '= 0,0017 km', at: 22, size: 130, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Hai lần bán kính" />
    <Calc f={f} x={CX + 100} y={760} step={150} lines={[{t: '2 × 6.371', at: 2, size: 130}, {t: '= 12.742', at: 22, size: 130, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Nhân với chiều cao mắt" />
    <Calc f={f} x={CX + 100} y={760} step={150} lines={[{t: '12.742 × 0,0017', at: 2, size: 100}, {t: '≈ 21,66', at: 22, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Lấy căn bậc hai" />
    <Calc f={f} x={CX + 100} y={760} step={150} lines={[{t: '√21,66', at: 2, size: 140}, {t: '≈ 4,65', at: 22, size: 150, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Người cao 1,7 mét" b="thấy chân trời cách" />
    <Big x={CX + 100} y={820} size={150} color={AM} o={sp(f, 2, 18)}>≈ 4,65 km</Big>
    <line x1={380} y1={980} x2={380 + 560 * sp(f, 6, 40)} y2={980} stroke={C.cream} strokeWidth={8} strokeLinecap="round" />
    <Dot x={380} y={980} />
    <Dot x={380 + 560 * sp(f, 6, 40)} y={980} />
    <Hero2 f={f} />
  </g>
);
const P23: Panel = ({f}) => {
  const p = clamp01(f / Math.max(60, 150));
  return (
    <g>
      <Head a="Quãng đi bộ" b="chưa tới 1 giờ" />
      <line x1={380} y1={900} x2={940} y2={900} stroke={C.cream} strokeWidth={8} strokeLinecap="round" />
      <Dot x={380} y={900} />
      <Dot x={940} y={900} />
      <circle cx={380 + 560 * p} cy={860} r={20} fill={AM} stroke={C.cream} strokeWidth={4} />
      <line x1={380 + 560 * p} y1={880} x2={380 + 560 * p} y2={900} stroke={AM} strokeWidth={8} />
      <Tag x={CX + 100} y={1010} color={C.cream} size={40} o={sp(f, 10, 26)}>đi bộ chưa tới 1 giờ</Tag>
      <Hero2 f={f} />
    </g>
  );
};
const P24: Panel = ({f}) => (
  <g>
    <Head a="Leo lên tháp" b="cao 100 mét" />
    <rect x={640 - 24} y={1200 - 480 * sp(f, 2, 30)} width={48} height={480 * sp(f, 2, 30)} fill="#8a8a8a" stroke={C.cream} strokeWidth={5} />
    <g opacity={sp(f, 24, 38)}>
      <circle cx={640} cy={700} r={16} fill={AM} stroke={C.cream} strokeWidth={4} />
      <Tag x={720} y={960} color={AM} size={44} anchor="start">100 m</Tag>
    </g>
    <g opacity={sp(f, 30, 44)}>
      <circle cx={520} cy={1176} r={8} fill={C.cream} />
      <line x1={520} y1={1184} x2={520} y2={1200} stroke={C.cream} strokeWidth={5} />
      <Tag x={520} y={1140} color={C.cream} size={32}>1,7 m</Tag>
    </g>
    <Hero2 f={f} />
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Mắt lúc này cao gấp" b="khoảng 59 lần" />
    <Big x={CX + 100} y={850} size={190} color={AM} o={sp(f, 2, 18)}>× 59</Big>
    <Tag x={CX + 100} y={960} color={C.cream} size={44} o={sp(f, 16, 30)}>100 ÷ 1,7 ≈ 59</Tag>
    <Hero2 f={f} />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Chân trời" b="không xa gấp 59 lần" />
    <Big x={CX + 100} y={850} size={190} color={C.cream} o={sp(f, 2, 14)}>× 59</Big>
    <line x1={CX - 130} y1={880} x2={CX + 330} y2={770} stroke={RED} strokeWidth={16} strokeLinecap="round" opacity={sp(f, 16, 30)} />
    <Hero2 f={f} />
  </g>
);
const P27: Panel = ({f}) => (
  <g>
    <Head a="Chỉ xa gấp khoảng" b="vì có căn bậc hai" />
    <Big x={CX + 100} y={850} size={200} color={AM} o={sp(f, 2, 18)}>× 7,7</Big>
    <Tag x={CX + 100} y={980} color={C.cream} size={40} o={sp(f, 16, 30)}>căn bậc hai của 59 ≈ 7,7</Tag>
    <Hero2 f={f} />
  </g>
);
const P28: Panel = ({f}) => (
  <g>
    <Head a="Tháp cao 100 mét" b="0,1 ki-lô-mét" />
    <Calc f={f} x={CX + 100} y={760} step={150} lines={[{t: '12.742 × 0,1', at: 2, size: 120}, {t: '≈ 1.274', at: 22, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P29: Panel = ({f}) => (
  <g>
    <Head a="Lấy căn bậc hai" />
    <Calc f={f} x={CX + 100} y={760} step={150} lines={[{t: '√1.274', at: 2, size: 140}, {t: '≈ 35,7', at: 22, size: 150, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P30: Panel = ({f}) => (
  <g>
    <Head a="Đứng trên tháp" b="thấy chân trời xa" />
    <rect x={400} y={950} width={34} height={250} fill="#8a8a8a" stroke={C.cream} strokeWidth={5} />
    <circle cx={417} cy={934} r={14} fill={AM} stroke={C.cream} strokeWidth={4} />
    <Big x={CX + 170} y={820} size={140} color={AM} o={sp(f, 2, 18)}>≈ 35,7 km</Big>
    <Arrow x1={470} y1={934} x2={940} y2={934} color={C.cream} p={sp(f, 10, 44)} w={7} />
    <Hero2 f={f} />
  </g>
);
const P31: Panel = ({f}) => (
  <g>
    <Head a="Thực tế không khí" b="bẻ cong tia sáng" />
    <Ball o={0.7} />
    <Eye />
    <line x1={EYE.x} y1={EYE.y} x2={900} y2={836} stroke={C.cream} strokeWidth={5} strokeDasharray="12 10" />
    <path d={`M ${EYE.x} ${EYE.y} Q 800 690 ${lerp(EYE.x, 925, 1)} 835`} fill="none" stroke={AM} strokeWidth={7} strokeLinecap="round" opacity={sp(f, 6, 30)} />
    <Tag x={890} y={690} color={AM} size={52} o={sp(f, 24, 38)}>+ 8%</Tag>
    <Hero2 f={f} />
  </g>
);
const P32: Panel = ({f}) => (
  <g>
    <Head a="Trên bãi biển" b="chân trời cách khoảng" />
    <Sea f={f} y={1000} />
    <Big x={CX + 100} y={840} size={170} color={AM} o={sp(f, 2, 18)}>≈ 5 km</Big>
    <Hero2 f={f} />
  </g>
);
const P33: Panel = ({f}) => (
  <g>
    <Head a="Tàu đi xa" b="thân mất trước, cột buồm mất sau" />
    <ShipS x={720} y={975} />
    <Sea f={f} y={930} />
    <Tag x={720} y={1110} color={RED} size={38} o={sp(f, 10, 24)}>thân tàu bị che</Tag>
    <Tag x={720} y={800} color={AM} size={38} o={sp(f, 20, 34)}>cột buồm còn thấy</Tag>
    <Hero2 f={f} />
  </g>
);
const P34: Panel = ({f}) => (
  <g>
    <Head a="Mặt biển cong" b="che phần thấp trước" />
    <ShipS x={878} y={957} />
    <Curve />
    <circle cx={436} cy={880} r={15} fill={AM} stroke={C.cream} strokeWidth={4} />
    <line x1={436} y1={880} x2={980} y2={880} stroke={AM} strokeWidth={5} strokeDasharray="12 10" opacity={sp(f, 6, 24)} />
    <Tag x={640} y={800} color={AM} size={36} o={sp(f, 24, 40)}>phần cao vẫn lộ ra</Tag>
    <Hero2 f={f} />
  </g>
);
const P35: Panel = ({f}) => (
  <g>
    <Head a="Cột buồm cao 30 mét" b="còn thấy thêm" />
    <Calc f={f} x={CX + 100} y={780} step={160} lines={[{t: '12.742 × 0,03', at: 2, size: 100}, {t: '≈ 19,6 km', at: 22, size: 150, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P36: Panel = ({f}) => (
  <g>
    <Head a="Thấy ngọn cột buồm" b="đến khoảng" />
    <Calc f={f} x={CX + 100} y={780} step={160} lines={[{t: '4,65 + 19,6', at: 2, size: 120}, {t: '≈ 24 km', at: 22, size: 160, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P37: Panel = ({f}) => {
  const p = clamp01(f / 120);
  return (
    <g>
      <Head a="Nếu mặt biển phẳng" b="tàu chỉ nhỏ dần" />
      <Sea f={f} y={1000} />
      <ShipS x={460 + 380 * p} y={960} s={1 - 0.65 * p} />
      <Tag x={CX + 100} y={820} color={AM} size={44} o={sp(f, 8, 22)}>nhỏ dần</Tag>
      <g opacity={sp(f, 40, 56)}>
        <Tag x={CX + 100} y={1100} color={RED} size={40}>không chìm từ dưới lên</Tag>
      </g>
      <Hero2 f={f} />
    </g>
  );
};
const P38: Panel = ({f}) => (
  <g>
    <Head a="Đường chân trời" b="cách ta khoảng 5 km" />
    <Big x={CX + 100} y={800} size={160} color={AM} o={sp(f, 2, 18)}>≈ 5 km</Big>
    <Tag x={CX + 100} y={920} color={C.cream} size={40} o={sp(f, 14, 28)}>tam giác vuông ấy</Tag>
    <Tag x={CX + 100} y={980} color={C.cream} size={40} o={sp(f, 18, 32)}>cho thấy Trái Đất tròn</Tag>
    <Hero2 f={f} cheer={sp(f, 10, 28)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30, P31, P32, P33, P34, P35, P36, P37, P38];
void lerp;
