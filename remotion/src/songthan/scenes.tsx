import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const WATER = '#2f7fa8';
const SAND = '#b89a62';
const RED = '#e0613b';
const AM = C.amber;
const CX = 540;

const Hero2: React.FC<{f: number; x?: number; cheer?: number}> = ({f, x = 170, cheer = 0}) => <HatHero x={x} y={1250} s={2} walk={f * 0.13} cheer={cheer} hat="helmet" />;

// Mặt sóng: đường lượn; amp là biên độ, k mật độ, v tốc độ trôi.
const waveD = (y: number, amp: (x: number) => number, k: number, ph: number, x0 = 300, x1 = 990) => {
  let d = '';
  for (let x = x0; x <= x1; x += 10) d += `${x === x0 ? 'M' : 'L'} ${x} ${y - amp(x) * Math.sin(x * k - ph)} `;
  return d;
};
const Sea: React.FC<{f: number; y?: number; amp?: (x: number) => number; k?: number; bottom?: number; floor?: (x: number) => number}> = ({f, y = 760, amp = () => 10, k = 0.02, bottom = 1200, floor}) => {
  const d = waveD(y, amp, k, f * 0.12);
  const fl = floor ? floor : () => bottom;
  let fd = '';
  for (let x = 300; x <= 990; x += 10) fd += `${x === 300 ? 'M' : 'L'} ${x} ${fl(x)} `;
  return (
    <g>
      <path d={`${d} L 990 ${fl(990)} ${[...Array(70)].map((_, i) => `L ${990 - i * 10} ${fl(990 - i * 10)}`).join(' ')} Z`} fill={WATER} opacity={0.55} />
      <path d={d} fill="none" stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
      <path d={`${fd}`} fill="none" stroke={SAND} strokeWidth={12} strokeLinecap="round" />
    </g>
  );
};
const Ship: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M -70 0 L 70 0 L 50 36 L -50 36 Z" fill="#c9533a" stroke={C.cream} strokeWidth={5} strokeLinejoin="round" />
    <rect x={-20} y={-34} width={40} height={34} fill={C.cream} />
    <rect x={-6} y={-60} width={12} height={26} fill={C.cream} />
  </g>
);
const Plane: React.FC<{x: number; y: number}> = ({x, y}) => (
  <g transform={`translate(${x} ${y})`} fill={C.cream}>
    <ellipse cx={0} cy={0} rx={62} ry={14} />
    <path d="M -10 0 L -40 -40 L -22 -40 L 20 0 Z" />
    <path d="M -10 0 L -40 36 L -22 36 L 20 0 Z" />
    <path d="M -52 0 L -70 -24 L -58 -24 L -40 0 Z" />
  </g>
);
const Car: React.FC<{x: number; y: number; c?: string}> = ({x, y, c = AM}) => (
  <g transform={`translate(${x} ${y}) scale(1.7)`}>
    <rect x={-44} y={-26} width={88} height={30} rx={8} fill={c} stroke={C.cream} strokeWidth={4} />
    <rect x={-24} y={-48} width={48} height={24} rx={8} fill={c} stroke={C.cream} strokeWidth={4} />
    <circle cx={-24} cy={6} r={9} fill="#222" stroke={C.cream} strokeWidth={3} />
    <circle cx={24} cy={6} r={9} fill="#222" stroke={C.cream} strokeWidth={3} />
  </g>
);

const P0: Panel = ({f}) => (
  <g>
    <Head a="Sóng chưa cao tới 1 mét" b="mà vào bờ lại tàn phá?" />
    <Sea f={f} y={820} amp={(x) => 8 + (x > 760 ? 70 * clamp01((f - 30) / 40) * clamp01((x - 760) / 200) : 0)} floor={(x) => 1100 - (x > 700 ? (x - 700) * 0.9 : 0)} />
    <Ship x={300} y={800} />
    <Big x={CX + 360} y={600} size={150} color={AM} o={sp(f, 20, 36) * 0.9}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Ngoài biển sâu" b="sóng thần nhanh ngang máy bay" />
    <Sea f={f} y={900} amp={() => 12} floor={() => 1180} />
    <Plane x={((f * 7) % 1000) + 100} y={660} />
    <Arrow x1={300} y1={760} x2={620} y2={760} color={RED} p={sp(f, 8, 26)} w={9} />
    <Hero2 f={f} />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Làm sao biết tốc độ" b="khi chưa kịp nhìn thấy sóng?" />
    <Sea f={f} y={880} amp={() => 12} floor={() => 1180} />
    <Big x={CX + 80} y={700} size={190} color={AM} o={sp(f, 4, 20)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Tốc độ chỉ phụ thuộc" b="độ sâu của biển" />
    <Sea f={f} y={700} amp={() => 10} floor={() => 1180} />
    <Arrow x1={CX + 200} y1={720} x2={CX + 200} y2={1160} color={AM} p={sp(f, 6, 30)} w={9} />
    <Tag x={CX + 340} y={950} color={AM} size={48} o={sp(f, 20, 36)}>độ sâu</Tag>
    <Hero2 f={f} />
  </g>
);
const P4: Panel = ({f}) => (
  <g>
    <Head a="Sóng thần cực dài" b="hơn 100 km giữa hai đỉnh" />
    <Sea f={f} y={820} amp={() => 50} k={0.0075} floor={() => 1180} />
    <line x1={380} y1={620} x2={860} y2={620} stroke={AM} strokeWidth={6} opacity={sp(f, 10, 26)} />
    <line x1={380} y1={600} x2={380} y2={640} stroke={AM} strokeWidth={6} opacity={sp(f, 10, 26)} />
    <line x1={860} y1={600} x2={860} y2={640} stroke={AM} strokeWidth={6} opacity={sp(f, 10, 26)} />
    <Big x={620} y={570} size={72} color={AM} o={sp(f, 18, 34)}>{'> 100 km'}</Big>
    <Hero2 f={f} />
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Biển sâu 4 km" b="bằng 1/25 chiều dài sóng" />
    <rect x={300} y={760} width={690} height={32 * sp(f, 4, 24)} fill={WATER} opacity={0.7} stroke={C.cream} strokeWidth={5} />
    <line x1={300} y1={700} x2={990} y2={700} stroke={AM} strokeWidth={5} opacity={sp(f, 14, 30)} />
    <Big x={640} y={660} size={64} color={AM} o={sp(f, 18, 34)}>100 km</Big>
    <line x1={270} y1={760} x2={270} y2={792} stroke={RED} strokeWidth={6} opacity={sp(f, 24, 40)} />
    <Big x={640} y={880} size={64} color={RED} o={sp(f, 26, 42)}>chỉ sâu 4 km</Big>
    <Hero2 f={f} />
  </g>
);
const P6: Panel = ({f}) => {
  const sw = 40 * Math.sin(f * 0.15);
  return (
    <g>
      <Head a="Cả cột nước đung đưa" b="đáy biển quyết định tốc độ" />
      <Sea f={f} y={620} amp={() => 12} floor={() => 1180} />
      {[0, 1, 2, 3, 4].map((i) => (
        <Arrow key={i} x1={CX + 100 - sw} y1={700 + i * 100} x2={CX + 100 + sw + 20} y2={700 + i * 100} color={AM} p={1} w={7} />
      ))}
      <Hero2 f={f} />
    </g>
  );
};
const P7: Panel = ({f}) => (
  <g>
    <Head a="Công thức" />
    <Big x={CX + 60} y={740} size={96} color={C.cream} o={sp(f, 2, 14)}>tốc độ =</Big>
    <Big x={CX + 60} y={890} size={100} color={AM} o={sp(f, 14, 28)}>√(g × độ sâu)</Big>
    <Hero2 f={f} />
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Số g làm đá rơi nhanh dần" b="chừng 9,8" />
    <Big x={CX + 60} y={760} size={170} color={AM} o={sp(f, 2, 16)}>g ≈ 9,8</Big>
    <circle cx={CX + 360} cy={lerp(660, 1100, clamp01((f % 60) / 60) ** 2)} r={26} fill="#9aa3a8" stroke={C.cream} strokeWidth={5} />
    <Hero2 f={f} />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Căn bậc hai" b="là số nhân với chính nó" />
    <Big x={CX + 60} y={780} size={110} color={C.cream} o={sp(f, 2, 14)}>√ số = ?</Big>
    <Big x={CX + 60} y={940} size={110} color={AM} o={sp(f, 16, 30)}>? × ? = số</Big>
    <Hero2 f={f} />
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Ví dụ" />
    <Calc f={f} x={CX + 60} y={740} step={160} lines={[{t: '√9 = 3', at: 2, size: 130, color: AM}, {t: '3 × 3 = 9', at: 28, size: 130}]} />
    <Hero2 f={f} />
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Giữa Thái Bình Dương" b="biển sâu 4.000 mét" />
    <Sea f={f} y={640} amp={() => 8} floor={() => 1200} />
    <Arrow x1={CX + 200} y1={660} x2={CX + 200} y2={1180} color={AM} p={sp(f, 6, 32)} w={9} />
    <Big x={CX - 60} y={930} size={96} color={AM} o={sp(f, 20, 36)}>4.000 m</Big>
    <Hero2 f={f} />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Nhân g với độ sâu" />
    <Calc f={f} x={CX + 60} y={760} step={150} lines={[{t: '9,8 × 4.000', at: 2, size: 110}, {t: '= 39.200', at: 24, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Lấy căn bậc hai" />
    <Calc f={f} x={CX + 60} y={760} step={150} lines={[{t: '√39.200', at: 2, size: 120}, {t: '≈ 198', at: 24, size: 150, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Gần 200 mét" b="mỗi giây" />
    <Big x={CX + 60} y={800} size={170} color={AM} o={sp(f, 2, 18)}>198 m/s</Big>
    <Arrow x1={300} y1={960} x2={900} y2={960} color={RED} p={sp(f, 10, 36)} w={10} />
    <Hero2 f={f} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Đổi ra km/h" b="nhân với 3,6" />
    <Calc f={f} x={CX + 60} y={760} step={150} lines={[{t: '198 × 3,6', at: 2, size: 120}, {t: '≈ 713 km/h', at: 24, size: 130, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Hơn 700 km/h" b="gần bằng máy bay phản lực" />
    <Plane x={((f * 6) % 800) + 150} y={760} />
    <Sea f={f} y={980} amp={() => 12} floor={() => 1200} />
    <Big x={CX + 60} y={600} size={110} color={AM} o={sp(f, 4, 20)}>713 km/h</Big>
    <Hero2 f={f} />
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Ngoài khơi sóng thấp" b="dưới 1 mét" />
    <Sea f={f} y={860} amp={() => 8} floor={() => 1200} />
    <Ship x={CX + 40} y={840} />
    <line x1={CX + 300} y1={860} x2={CX + 300} y2={800} stroke={AM} strokeWidth={6} opacity={sp(f, 12, 28)} />
    <Tag x={CX + 300} y={770} color={AM} size={44} o={sp(f, 14, 30)}>dưới 1 m</Tag>
    <Hero2 f={f} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Gần bờ biển nông dần" b="chỉ còn sâu 10 mét" />
    <Sea f={f} y={700} amp={() => 14} floor={(x) => 1180 - clamp01((x - 300) / 600) * 440 * sp(f, 4, 40)} />
    <Big x={CX + 360} y={900} size={80} color={AM} o={sp(f, 26, 42)}>10 m</Big>
    <Hero2 f={f} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Nhân g với độ sâu 10 mét" />
    <Calc f={f} x={CX + 60} y={780} step={150} lines={[{t: '9,8 × 10', at: 2, size: 130}, {t: '= 98', at: 24, size: 150, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Lấy căn bậc hai" />
    <Calc f={f} x={CX + 60} y={760} step={150} lines={[{t: '√98', at: 2, size: 130}, {t: '≈ 9,9 m/s', at: 24, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Chậm hơn gần 20 lần" />
    <rect x={CX - 40} y={1100 - 360 * sp(f, 4, 30)} width={110} height={360 * sp(f, 4, 30)} fill={RED} stroke={C.cream} strokeWidth={4} />
    <rect x={CX + 120} y={1100 - 18 * sp(f, 14, 40)} width={110} height={18 * sp(f, 14, 40)} fill={AM} stroke={C.cream} strokeWidth={4} />
    <Big x={CX + 15} y={690} size={72} color={RED} o={sp(f, 22, 36)}>713</Big>
    <Big x={CX + 175} y={1020} size={72} color={AM} o={sp(f, 28, 42)}>36</Big>
    <Hero2 f={f} />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Phần sóng sau" b="dồn vào phần sóng trước" />
    <Sea f={f} y={820} amp={() => 14} floor={() => 1180} />
    <Arrow x1={300} y1={700} x2={300 + 260 * sp(f, 6, 36)} y2={700} color={RED} p={1} w={10} />
    <Arrow x1={720} y1={700} x2={800} y2={700} color={AM} p={1} w={7} />
    <Tag x={430} y={650} color={RED} size={40}>sau: nhanh</Tag>
    <Tag x={780} y={650} color={AM} size={40}>trước: chậm</Tag>
    <Hero2 f={f} />
  </g>
);
const P23: Panel = ({f}) => {
  const g = 230 - 100 * sp(f, 10, 60);
  return (
    <g>
      <Head a="Như đoàn xe" b="xe sau dồn vào xe trước" />
      {[0, 1, 2, 3].map((i) => (
        <Car key={i} x={340 + i * g} y={1000} c={i === 3 ? AM : ['#5aa0d0', '#6fb86f', '#c05a7a'][i % 3]} />
      ))}
      <Hero2 f={f} />
    </g>
  );
};
const P24: Panel = ({f}) => (
  <g>
    <Head a="Nước dồn lại" b="sóng cao lên, dòng mạnh hơn" />
    <Sea f={f} y={900} amp={(x) => 10 + 55 * sp(f, 6, 70) * clamp01((x - 300) / 600)} k={0.014} floor={(x) => 1180 - clamp01((x - 300) / 600) * 300} />
    <Hero2 f={f} />
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Một công thức với độ sâu" b="giải thích sóng dữ ở bờ" />
    <Sea f={f} y={860} amp={(x) => 8 + 55 * clamp01((x - 500) / 450)} k={0.014} floor={(x) => 1180 - clamp01((x - 300) / 600) * 380} />
    <Big x={CX + 100} y={620} size={100} color={AM} o={sp(f, 10, 28)}>√(g × độ sâu)</Big>
    <Hero2 f={f} cheer={sp(f, 14, 32)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25];
