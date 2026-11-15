import React from 'react';
import {Arrow, Bar, Big, C, Calc, Dash, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const HG = '#c7ccd4';
const WAT = '#4f8fd6';
const AIR = '#9fd0ff';
const RED = '#e0613b';

// Ống thủy tinh đứng trong chậu: đỉnh ống yTop, đáy chậu yB; lv = phần chất lỏng tính từ mặt chậu lên (0..1 chiều cao ống).
const Tube: React.FC<{x: number; yTop: number; yB?: number; lv: number; color?: string; w?: number; o?: number; basin?: boolean}> = ({x, yTop, yB = 1200, lv, color = HG, w = 64, o = 1, basin = true}) => {
  const surf = yB - 60;
  const h = surf - yTop;
  const top = surf - h * clamp01(lv);
  return (
    <g opacity={clamp01(o)}>
      {basin && <path d={`M ${x - 170} ${yB - 90} L ${x - 150} ${yB} L ${x + 150} ${yB} L ${x + 170} ${yB - 90}`} fill="none" stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />}
      {basin && <path d={`M ${x - 164} ${surf} L ${x - 152} ${yB - 4} L ${x + 152} ${yB - 4} L ${x + 164} ${surf} Z`} fill={color} opacity={0.85} />}
      <rect x={x - w / 2} y={top} width={w} height={yB - 30 - top} fill={color} />
      <path d={`M ${x - w / 2} ${yB - 30} L ${x - w / 2} ${yTop + w / 2} A ${w / 2} ${w / 2} 0 0 1 ${x + w / 2} ${yTop + w / 2} L ${x + w / 2} ${yB - 30}`} fill="none" stroke={C.cream} strokeWidth={5} />
    </g>
  );
};
const Scale: React.FC<{x: number; y: number; o?: number}> = ({x, y, o = 1}) => (
  <g opacity={clamp01(o)}>
    <rect x={x - 150} y={y} width={300} height={110} rx={18} fill="#3a4658" stroke={C.cream} strokeWidth={5} />
    <rect x={x - 170} y={y - 16} width={340} height={20} rx={8} fill="#56647a" stroke={C.cream} strokeWidth={4} />
    <circle cx={x} cy={y + 55} r={36} fill="#1b2430" stroke={C.cream} strokeWidth={4} />
    <line x1={x} y1={y + 55} x2={x} y2={y + 26} stroke={RED} strokeWidth={5} strokeLinecap="round" />
  </g>
);
const Cloud: React.FC<{x: number; y: number; s?: number; o?: number}> = ({x, y, s = 1, o = 1}) => (
  <g opacity={clamp01(o)} transform={`translate(${x} ${y}) scale(${s})`} fill="#e6eef8" stroke={C.cream} strokeWidth={4 / s}>
    <ellipse cx={0} cy={0} rx={110} ry={44} />
    <ellipse cx={55} cy={-34} rx={66} ry={48} />
    <ellipse cx={-55} cy={-22} rx={56} ry={38} />
  </g>
);
// Cân đĩa: tilt âm = nghiêng trái.
const Balance: React.FC<{x: number; y: number; tilt?: number; left?: React.ReactNode; right?: React.ReactNode}> = ({x, y, tilt = 0, left, right}) => {
  const a = tilt * 0.25;
  const lx = x - 260 * Math.cos(a), ly = y - 260 * Math.sin(a);
  const rx = x + 260 * Math.cos(a), ry = y + 260 * Math.sin(a);
  return (
    <g>
      <line x1={x} y1={y} x2={x} y2={y + 420} stroke={C.cream} strokeWidth={8} />
      <path d={`M ${x - 90} ${y + 430} L ${x + 90} ${y + 430}`} stroke={C.cream} strokeWidth={10} strokeLinecap="round" />
      <line x1={lx} y1={ly} x2={rx} y2={ry} stroke={C.cream} strokeWidth={8} strokeLinecap="round" />
      <circle cx={x} cy={y} r={12} fill={C.amber} />
      {[[lx, ly, left], [rx, ry, right]].map(([px, py, node], i) => (
        <g key={i}>
          <line x1={px as number} y1={py as number} x2={(px as number) - 80} y2={(py as number) + 160} stroke={C.cream} strokeWidth={3} />
          <line x1={px as number} y1={py as number} x2={(px as number) + 80} y2={(py as number) + 160} stroke={C.cream} strokeWidth={3} />
          <path d={`M ${(px as number) - 100} ${(py as number) + 160} Q ${px} ${(py as number) + 200} ${(px as number) + 100} ${(py as number) + 160} Z`} fill="#56647a" stroke={C.cream} strokeWidth={4} />
          <g transform={`translate(${px} ${(py as number) + 160})`}>{node as React.ReactNode}</g>
        </g>
      ))}
    </g>
  );
};
const Mountain: React.FC<{o?: number}> = ({o = 1}) => (
  <g opacity={clamp01(o)}>
    <path d="M 90 1220 L 560 520 L 990 1220 Z" fill="#3f4b5e" stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
    <path d="M 480 640 L 560 520 L 640 640 L 600 610 L 560 650 L 520 610 Z" fill="#e6eef8" />
  </g>
);
const Weight: React.FC<{x: number; y: number; label: string; s?: number; o?: number}> = ({x, y, label, s = 1, o = 1}) => (
  <g opacity={clamp01(o)} transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M -70 60 L -50 -40 L 50 -40 L 70 60 Z" fill="#56647a" stroke={C.cream} strokeWidth={5} strokeLinejoin="round" />
    <path d="M -24 -40 Q 0 -80 24 -40" fill="none" stroke={C.cream} strokeWidth={6} />
    <text x={0} y={30} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={40} fill={C.cream}>{label}</text>
  </g>
);

// --- Cảnh 1 ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Không khí có nặng không?" b="nặng bao nhiêu?" />
    <Cloud x={420} y={640} s={1.3} o={sp(f, 4, 20)} />
    <Cloud x={780} y={760} s={0.9} o={sp(f, 10, 26)} />
    <Big x={640} y={1060} size={150} color={C.amber} o={0.9 * sp(f, 20, 36)}>?</Big>
    <HatHero x={200} y={1250} s={2} walk={f * 0.12} hat="goggles" />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Không thể bỏ bầu trời" b="lên bàn cân" />
    <Scale x={620} y={1040} />
    <Cloud x={620} y={lerp(560, 960, sp(f, 6, 34))} s={1.1} />
    <Tag x={620} y={1220} color={RED} size={46} o={sp(f, 36, 50)}>cân không nhúc nhích</Tag>
    <HatHero x={200} y={1250} s={2} walk={f * 0.12} cheer={sp(f, 4, 20)} hat="goggles" />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Chỉ cần một ống thủy tinh" b="và một chậu thủy ngân" />
    <Tube x={640} yTop={560} lv={0.76} o={sp(f, 4, 20)} />
    <HatHero x={220} y={1250} s={2} walk={f * 0.12} cheer={sp(f, 24, 40)} hat="goggles" />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Cái ống ấy cân" b="không khí thế nào?" />
    <Tube x={540} yTop={560} lv={0.76} />
    <Big x={820} y={760} size={140} color={C.amber} o={0.9 * sp(f, 10, 26)}>?</Big>
  </g>
);

// --- Cảnh 2: ống nước ---
const P4: Panel = ({f}) => (
  <g>
    <Head a="Dựng một ống rất dài" b="đổ đầy nước" />
    <Tube x={600} yTop={460} lv={sp(f, 4, 40)} color={WAT} />
    <HatHero x={220} y={1250} s={2} walk={f * 0.12} hat="goggles" />
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Nước dừng ở khoảng 10 mét" b="phía trên để lại khoảng trống" />
    <Tube x={600} yTop={460} lv={1 - sp(f, 4, 30) * 0.16} color={WAT} />
    <line x1={720} y1={1140} x2={720} y2={570} stroke={C.amber} strokeWidth={5} opacity={sp(f, 26, 40)} />
    <Tag x={830} y={870} color={C.amber} size={56} o={sp(f, 30, 44)}>10 m</Tag>
    <Tag x={830} y={520} color={C.cream} size={40} o={sp(f, 36, 50)}>khoảng trống</Tag>
    <HatHero x={220} y={1250} s={2} walk={f * 0.12} hat="goggles" />
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Vì sao nước dừng ở đó" b="mà không chảy hết ra?" />
    <Tube x={600} yTop={460} lv={0.84} color={WAT} />
    <Big x={860} y={800} size={150} color={C.amber} o={0.9 * sp(f, 10, 26)}>?</Big>
    <HatHero x={220} y={1250} s={2} walk={f * 0.15} hat="goggles" />
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Không khí đè lên mặt chậu" b="và đỡ cột nước lên" />
    <Tube x={540} yTop={460} lv={0.84} color={WAT} />
    {[-130, -90, 90, 130].map((dx, i) => (
      <Arrow key={i} x1={540 + dx} y1={900} x2={540 + dx} y2={1120} p={sp(f, 6 + i * 4, 30 + i * 4)} color={AIR} />
    ))}
    <Arrow x1={680} y1={1100} x2={680} y2={760} p={sp(f, 30, 56)} color={C.amber} />
    <Tag x={830} y={1010} color={AIR} size={40} o={sp(f, 20, 34)}>không khí đè</Tag>
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Như một chiếc cân đĩa" b="hai bên nặng bằng nhau" />
    <Balance x={540} y={600} tilt={0.15 * Math.sin(f * 0.1) * (1 - sp(f, 20, 60))}
      left={<rect x={-40} y={-150} width={80} height={140} fill={AIR} opacity={0.5} stroke={C.cream} strokeWidth={3} />}
      right={<rect x={-30} y={-120} width={60} height={110} fill={WAT} stroke={C.cream} strokeWidth={3} />} />
    <Tag x={280} y={1110} color={AIR} size={40} o={sp(f, 10, 24)}>cột không khí</Tag>
    <Tag x={800} y={1110} color={WAT} size={40} o={sp(f, 16, 30)}>cột nước</Tag>
  </g>
);

// --- Cảnh 3: thủy ngân ---
const P9: Panel = ({f}) => (
  <g>
    <Head a="Ống nước 10 mét quá khó dùng" b="nên thay bằng thủy ngân" />
    <Tube x={360} yTop={460} lv={0.84} color={WAT} />
    <Tube x={780} yTop={940} lv={0.8} o={sp(f, 16, 32)} />
    <Arrow x1={470} y1={800} x2={680} y2={900} p={sp(f, 8, 30)} color={C.amber} />
  </g>
);
const Cube: React.FC<{x: number; y: number; s: number; color: string; label: string; o?: number}> = ({x, y, s, color, label, o = 1}) => (
  <g opacity={clamp01(o)}>
    <rect x={x - s / 2} y={y - s / 2} width={s} height={s} fill={color} stroke={C.cream} strokeWidth={5} />
    <path d={`M ${x - s / 2} ${y - s / 2} l ${s * 0.25} ${-s * 0.25} l ${s} 0 l ${-s * 0.25} ${s * 0.25} Z`} fill={color} opacity={0.7} stroke={C.cream} strokeWidth={4} />
    <path d={`M ${x + s / 2} ${y - s / 2} l ${s * 0.25} ${-s * 0.25} l 0 ${s} l ${-s * 0.25} ${s * 0.25} Z`} fill={color} opacity={0.55} stroke={C.cream} strokeWidth={4} />
    <text x={x} y={y + s / 2 + 70} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={48} fill={C.cream}>{label}</text>
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Thủy ngân nặng gấp" b="khoảng 13,6 lần nước" />
    <Cube x={320} y={760} s={180} color={WAT} label="nước" o={sp(f, 4, 18)} />
    <Cube x={740} y={760} s={180} color={HG} label="thủy ngân" o={sp(f, 10, 24)} />
    <Big x={540} y={1130} size={130} color={C.amber} o={sp(f, 22, 38)}>× 13,6</Big>
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Ống dài khoảng 1 mét" b="úp ngược vào chậu" />
    <g transform={`translate(0 ${lerp(-260, 0, sp(f, 6, 40))})`}>
      <Tube x={560} yTop={600} lv={1} basin={false} />
    </g>
    <path d="M 390 1110 L 410 1200 L 710 1200 L 730 1110" fill="none" stroke={C.cream} strokeWidth={6} />
    <path d="M 396 1140 L 412 1196 L 708 1196 L 724 1140 Z" fill={HG} opacity={0.85} />
    <HatHero x={200} y={1250} s={2} walk={f * 0.12} cheer={sp(f, 30, 50)} hat="goggles" />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Thủy ngân đứng yên" b="ở khoảng 76 cm" />
    <Tube x={560} yTop={600} lv={1 - sp(f, 4, 34) * 0.24} />
    <line x1={680} y1={1140} x2={680} y2={777} stroke={C.amber} strokeWidth={5} opacity={sp(f, 30, 44)} />
    <Tag x={800} y={980} color={C.amber} size={56} o={sp(f, 34, 48)}>76 cm</Tag>
    <HatHero x={200} y={1250} s={2} walk={f * 0.12} hat="goggles" />
  </g>
);

// --- Cảnh 4: phép cân ---
const P13: Panel = ({f}) => (
  <g>
    <Head a="Cân không khí" b="bằng cột thủy ngân" />
    <Balance x={540} y={600} tilt={0.1 * Math.sin(f * 0.1) * (1 - sp(f, 20, 50))}
      left={<rect x={-40} y={-150} width={80} height={140} fill={AIR} opacity={0.5} stroke={C.cream} strokeWidth={3} />}
      right={<rect x={-22} y={-70} width={44} height={60} fill={HG} stroke={C.cream} strokeWidth={3} />} />
    <Tag x={280} y={1110} color={AIR} size={40}>cột không khí</Tag>
    <Tag x={800} y={1110} color={HG} size={40} o={sp(f, 10, 24)}>cột thủy ngân</Tag>
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Đáy 1 xen-ti-mét vuông" b="cỡ móng tay út" />
    <rect x={430} y={640} width={220} height={220} fill={HG} opacity={sp(f, 4, 20)} stroke={C.cream} strokeWidth={6} />
    <Tag x={540} y={930} color={C.amber} size={48} o={sp(f, 14, 28)}>1 cm × 1 cm</Tag>
    <Tag x={540} y={1000} color={C.cream} size={38} o={sp(f, 22, 36)}>(phóng to)</Tag>
    <HatHero x={200} y={1250} s={2} walk={f * 0.12} hat="goggles" />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="1 xen-ti-mét khối thủy ngân" b="nặng khoảng 13,6 gam" />
    <Cube x={540} y={760} s={200} color={HG} label="1 cm³" o={sp(f, 4, 18)} />
    <Big x={540} y={1150} size={120} color={C.amber} o={sp(f, 18, 34)}>13,6 g</Big>
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Cột cao 76 xen-ti-mét" />
    <Tube x={240} yTop={760} lv={0.76} />
    <Calc f={f} y={860} step={150} lines={[{t: '76 × 13,6 g', at: 6, size: 100}]} />
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Khối lượng cột thủy ngân" />
    <Calc f={f} y={700} step={160} lines={[{t: '76 × 13,6', at: 0, size: 100}, {t: '= 1 033,6 g', at: 6, size: 110, color: C.amber}, {t: '≈ 1 kg', at: 24, size: 120, color: C.amber}]} />
    <HatHero x={180} y={1250} s={2} walk={f * 0.2} cheer={sp(f, 30, 50)} hat="goggles" />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Mỗi xen-ti-mét vuông" b="không khí đè như 1 kg" />
    <rect x={440} y={1000} width={200} height={70} fill={HG} stroke={C.cream} strokeWidth={5} />
    <Weight x={540} y={lerp(640, 900, sp(f, 6, 30))} label="1 kg" s={1.3} />
    <HatHero x={200} y={1250} s={2} walk={f * 0.12} hat="goggles" />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Ngày nay đo được" b="khoảng 1,03 kg" />
    <Big x={540} y={800} size={160} color={C.amber} o={sp(f, 4, 20)}>1,03 kg</Big>
    <Tag x={540} y={940} color="#6fd18f" size={54} o={sp(f, 20, 36)}>✓ khớp phép tính</Tag>
    <HatHero x={540} y={1250} s={2} walk={f * 0.2} cheer={sp(f, 24, 44)} hat="goggles" />
  </g>
);

// --- Cảnh 5: thử bằng nước ---
const P20: Panel = ({f}) => (
  <g>
    <Head a="Thử lại bằng nước" b="cột cao gấp 13,6 lần" />
    <Tube x={300} yTop={960} lv={0.76} />
    <Tube x={720} yTop={460} lv={sp(f, 6, 46) * 0.84} color={WAT} />
    <Tag x={300} y={1260} color={C.cream} size={38}>76 cm</Tag>
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Chiều cao cột nước" />
    <Calc f={f} y={760} step={170} lines={[{t: '76 cm × 13,6', at: 4, size: 100}, {t: '≈ 10,3 m', at: 24, size: 130, color: C.amber}]} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.15} hat="goggles" />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Đúng bằng cột nước" b="10 mét đã thấy" />
    <Tube x={600} yTop={460} lv={0.84} color={WAT} />
    <Tag x={820} y={870} color={C.amber} size={56}>10,3 m</Tag>
    <Tag x={820} y={950} color="#6fd18f" size={60} o={sp(f, 10, 26)}>✓</Tag>
    <HatHero x={220} y={1250} s={2} walk={f * 0.2} cheer={sp(f, 14, 34)} hat="goggles" />
  </g>
);

// --- Cảnh 6: lên núi ---
const P23: Panel = ({f}) => (
  <g>
    <Head a="Lên cao thì còn" b="ít không khí đè lên hơn" />
    <Mountain />
    {Array.from({length: 160}).map((_, i) => {
      const r1 = Math.abs(Math.sin(i * 12.9898) * 43758.5453) % 1;
      const r2 = Math.abs(Math.sin(i * 78.233) * 12543.123) % 1;
      const y = 460 + Math.sqrt(r2) * 760;
      return <circle key={i} cx={110 + r1 * 860} cy={y} r={7} fill={AIR} opacity={0.75 * sp(f, 2 + (i % 20), 14 + (i % 20))} />;
    })}
    <Tag x={830} y={560} color={C.amber} size={42} o={sp(f, 26, 40)}>trên cao: thưa</Tag>
    <Tag x={250} y={1180} color={C.cream} size={42} o={sp(f, 30, 44)}>dưới thấp: dày</Tag>
  </g>
);
const P24: Panel = ({f}) => {
  const t = sp(f, 4, 80);
  return (
    <g>
      <Head a="Năm 1648, Pát-xcan nhờ" b="anh rể mang ống lên núi" />
      <Mountain />
      <HatHero x={lerp(200, 500, t)} y={lerp(1150, 700, t)} s={1.5} walk={f * 0.2} hat="goggles" />
    </g>
  );
};
const P25: Panel = ({f}) => (
  <g>
    <Head a="Càng lên cao" b="cột thủy ngân càng thấp" />
    <Mountain o={0.5} />
    <Tube x={270} yTop={860} yB={1220} lv={0.76} w={44} />
    <Tube x={720} yTop={460} yB={820} lv={0.76 - sp(f, 10, 40) * 0.12} w={44} />
    <Tag x={270} y={830} color={C.cream} size={36}>chân núi</Tag>
    <Tag x={880} y={600} color={C.amber} size={36} o={sp(f, 30, 44)}>thấp hơn</Tag>
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Lên cao 100 mét" b="sức ép giảm khoảng 1%" />
    <Bar x={110} y={700} w={860} color={AIR} p={1} label="mặt đất: 100%" />
    <Bar x={110} y={840} w={860} color={AIR} p={1 - sp(f, 8, 30) * 0.01} label="cao 100 m: 99%" />
    <Big x={540} y={1100} size={130} color={C.amber} o={sp(f, 20, 36)}>−1%</Big>
  </g>
);

// --- Cảnh 7: kết ---
const P27: Panel = ({f}) => (
  <g>
    <Head a="1 mét vuông, cỡ mặt bàn" b="không khí đè khoảng 10 tấn" />
    <path d="M 190 1000 L 890 1000 L 800 1100 L 280 1100 Z" fill="#6b5036" stroke={C.cream} strokeWidth={5} />
    {Array.from({length: 10}).map((_, i) => (
      <Weight key={i} x={290 + (i % 5) * 125} y={i < 5 ? 930 : 790} label="1 t" s={0.75} o={sp(f, 4 + i * 3, 12 + i * 3)} />
    ))}
    <Big x={540} y={620} size={110} color={C.amber} o={sp(f, 36, 52)}>10 tấn</Big>
  </g>
);
const P28: Panel = ({f}) => (
  <g>
    <Head a="Không khí ép đều" b="từ mọi phía" />
    {Array.from({length: 8}).map((_, i) => {
      const a = (i / 8) * 2 * Math.PI;
      const cx = 540, cy = 900;
      return <Arrow key={i} x1={cx + Math.cos(a) * 360} y1={cy + Math.sin(a) * 330} x2={cx + Math.cos(a) * 210} y2={cy + Math.sin(a) * 200} p={sp(f, 4 + i * 2, 24 + i * 2)} color={AIR} />;
    })}
    <HatHero x={540} y={1010} s={1.8} walk={f * 0.15} cheer={sp(f, 24, 44)} hat="goggles" />
  </g>
);
const P29: Panel = ({f}) => (
  <g>
    <Head a="1 kg trên mỗi xen-ti-mét vuông" b="cân bằng một ống thủy ngân" />
    <Tube x={720} yTop={560} lv={0.76} />
    <HatHero x={300} y={1250} s={2} walk={f * 0.25} cheer={sp(f, 16, 40)} hat="goggles" />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29];
