import React from 'react';
import {Arrow, Bar, Big, C, Calc, Dash, Head, HatHero, Lab, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const SNOW = '#e8f1ff';
const ROCK = '#3c5a86';

// Núi: đáy (x, y), rộng w, cao h; chóp tuyết.
const Mtn: React.FC<{x: number; y: number; w: number; h: number; o?: number}> = ({x, y, w, h, o = 1}) => (
  <g opacity={clamp01(o)}>
    <path d={`M ${x - w / 2} ${y} L ${x} ${y - h} L ${x + w / 2} ${y} Z`} fill={ROCK} stroke={C.cream} strokeWidth={5} strokeLinejoin="round" />
    <path d={`M ${x - w * 0.14} ${y - h * 0.72} L ${x} ${y - h} L ${x + w * 0.14} ${y - h * 0.72} L ${x + w * 0.06} ${y - h * 0.8} L ${x} ${y - h * 0.7} L ${x - w * 0.06} ${y - h * 0.8} Z`} fill={SNOW} />
  </g>
);
const Tree: React.FC<{x: number; y: number; h: number; o?: number}> = ({x, y, h, o = 1}) => (
  <g opacity={clamp01(o)}>
    <rect x={x - 16} y={y - h * 0.55} width={32} height={h * 0.55} fill="#7a5a36" stroke={C.cream} strokeWidth={4} />
    <circle cx={x} cy={y - h * 0.72} r={h * 0.28} fill="#3f9a5a" stroke={C.cream} strokeWidth={5} />
    <circle cx={x - h * 0.16} cy={y - h * 0.58} r={h * 0.2} fill="#3f9a5a" stroke={C.cream} strokeWidth={5} />
    <circle cx={x + h * 0.16} cy={y - h * 0.58} r={h * 0.2} fill="#3f9a5a" stroke={C.cream} strokeWidth={5} />
  </g>
);
// Góc ngắm: đỉnh góc (x, y), cạnh dài L, mở deg độ.
const Ang: React.FC<{x: number; y: number; L: number; deg: number; p?: number; label?: string; r?: number; lsize?: number}> = ({x, y, L, deg, p = 1, label, r = 120, lsize = 54}) => {
  const k = clamp01(p);
  const a = (deg * Math.PI) / 180;
  const ex = x + L * Math.cos(a) * k;
  const ey = y - L * Math.sin(a) * k;
  const ar = (deg * k * Math.PI) / 180;
  return (
    <g>
      <line x1={x} y1={y} x2={x + L} y2={y} stroke={C.cream} strokeWidth={6} strokeLinecap="round" />
      <line x1={x} y1={y} x2={ex} y2={ey} stroke={C.amber} strokeWidth={7} strokeLinecap="round" />
      <path d={`M ${x + r} ${y} A ${r} ${r} 0 0 0 ${x + r * Math.cos(ar)} ${y - r * Math.sin(ar)}`} fill="none" stroke={C.amber} strokeWidth={6} />
      {label && (
        <text x={x + r + 24} y={y - 16} fontFamily="BeVN" fontWeight={800} fontSize={lsize} fill={C.amber} opacity={clamp01(p * 2 - 1)}>{label}</text>
      )}
    </g>
  );
};
const Stake: React.FC<{x: number; y: number; h?: number}> = ({x, y, h = 70}) => (
  <g>
    <line x1={x} y1={y} x2={x} y2={y - h} stroke={C.cream} strokeWidth={8} strokeLinecap="round" />
    <circle cx={x} cy={y - h} r={9} fill={C.amber} />
  </g>
);
const River: React.FC<{y: number; o?: number}> = ({y, o = 1}) => (
  <g opacity={clamp01(o)}>
    <rect x={0} y={y} width={1080} height={110} fill="#2f6fa8" opacity={0.55} />
    <path d={`M 0 ${y + 30} Q 90 ${y + 12} 180 ${y + 30} T 360 ${y + 30} T 540 ${y + 30} T 720 ${y + 30} T 900 ${y + 30} T 1080 ${y + 30}`} fill="none" stroke="#9fd0ff" strokeWidth={4} opacity={0.6} />
  </g>
);
const Flag: React.FC<{x: number; y: number; h?: number; o?: number}> = ({x, y, h = 190, o = 1}) => (
  <g opacity={clamp01(o)}>
    <line x1={x} y1={y} x2={x} y2={y - h} stroke={C.cream} strokeWidth={8} strokeLinecap="round" />
    <path d={`M ${x} ${y - h} L ${x + 80} ${y - h + 24} L ${x} ${y - h + 50} Z`} fill="#e0613b" stroke={C.cream} strokeWidth={4} />
  </g>
);
const Earth: React.FC<{o?: number}> = ({o = 1}) => (
  <g opacity={clamp01(o)}>
    <path d="M 70 1250 A 800 800 0 0 1 1010 1250 L 1010 1320 L 70 1320 Z" fill="#244a73" stroke={C.cream} strokeWidth={6} />
    <path d="M 70 1250 A 800 800 0 0 1 1010 1250" fill="none" stroke="#9fd0ff" strokeWidth={7} />
  </g>
);
const Station: React.FC<{x: number; y: number}> = ({x, y}) => (
  <g>
    <circle cx={x} cy={y} r={14} fill={C.amber} stroke={C.cream} strokeWidth={4} />
    <line x1={x} y1={y + 14} x2={x} y2={y + 38} stroke={C.cream} strokeWidth={5} />
  </g>
);

// --- Cảnh 1 ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Núi Ê-vơ-rét cao hơn 8 000 mét" b="mà chưa ai lên tới đỉnh" />
    <Mtn x={640} y={1230} w={760} h={640} o={sp(f, 4, 22)} />
    <Big x={640} y={520} size={130} color={C.amber} o={sp(f, 18, 34)}>8 000+ m</Big>
    <HatHero x={150} y={1250} s={2} walk={f * 0.1} hat="scholar" />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Con số ấy được tính ra" b="từ nơi cách đỉnh hơn 170 km" />
    <HatHero x={150} y={1250} s={2} walk={f * 0.1} hat="scholar" />
    <Mtn x={840} y={1250} w={460} h={400} o={sp(f, 4, 18)} />
    <Dash x1={260} y1={1215} x2={640} y2={1215} p={sp(f, 12, 44)} />
    <Big x={450} y={1130} size={110} color={C.amber} o={sp(f, 30, 46)}>170 km</Big>
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Hóa ra bí mật chỉ là" b="một góc ngắm và một phép nhân" />
    <Ang x={130} y={1100} L={420} deg={32} p={sp(f, 8, 34)} r={110} />
    <Tag x={300} y={1180} color={C.cream} size={44} o={sp(f, 20, 34)}>góc ngắm</Tag>
    <Big x={780} y={900} size={250} color={C.amber} o={sp(f, 26, 44)}>×</Big>
    <Tag x={780} y={1040} color={C.cream} size={44} o={sp(f, 34, 48)}>phép nhân</Tag>
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Vậy góc ngắm" b="cho ta biết điều gì?" />
    <Ang x={180} y={1100} L={520} deg={40} p={sp(f, 6, 30)} r={130} />
    <Big x={800} y={880} size={220} color={C.amber} o={0.9 * sp(f, 14, 30)}>?</Big>
  </g>
);

// --- Cảnh 2 ---
const P4: Panel = ({f}) => (
  <g>
    <Head a="Thử với một cái cây:" b="bạn đứng cách gốc 30 mét" />
    <Tree x={830} y={1250} h={400} o={sp(f, 4, 18)} />
    <HatHero x={250} y={1250} s={2} walk={f * 0.1} hat="scholar" />
    <Dash x1={330} y1={1215} x2={780} y2={1215} p={sp(f, 14, 44)} />
    <Big x={555} y={1160} size={90} color={C.amber} o={sp(f, 30, 46)}>30 m</Big>
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Đường nhìn lên ngọn cây" b="tạo với mặt đất một góc" />
    <Tree x={830} y={1250} h={400} />
    <HatHero x={250} y={1250} s={2} walk={f * 0.04} hat="scholar" />
    <line x1={330} y1={1215} x2={780} y2={1215} stroke={C.dim} strokeWidth={5} strokeDasharray="12 10" />
    <Arrow x1={270} y1={1110} x2={810} y2={900} p={sp(f, 8, 36)} color={C.amber} />
    <Tag x={560} y={1170} color={C.amber} size={46} o={sp(f, 30, 46)}>góc ngắm</Tag>
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Giả sử góc ngắm là 45 độ" b="chếch lên đúng nửa góc vuông" />
    <Ang x={170} y={1150} L={640} deg={45} p={sp(f, 6, 34)} label="45°" r={170} lsize={80} />
    <line x1={170} y1={1150} x2={170} y2={700} stroke={C.dim} strokeWidth={5} strokeDasharray="12 10" opacity={sp(f, 14, 30)} />
    <Tag x={330} y={760} color={C.cream} size={42} o={sp(f, 22, 36)}>góc vuông 90°</Tag>
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Bảng toán cho một số gọi là tang" b="tang của 45 độ bằng 1" />
    <Calc f={f} y={720} lines={[{t: 'tang 45° = 1', at: 6, size: 110, color: C.amber}]} />
    <Tag x={540} y={900} color={C.cream} size={44} o={sp(f, 24, 38)}>tra trong bảng toán</Tag>
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="scholar" />
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Công thức thật" />
    <Big x={540} y={640} size={96} color={C.amber} o={sp(f, 6, 20)}>chiều cao</Big>
    <Big x={540} y={770} size={96} color={C.cream} o={sp(f, 16, 30)}>=</Big>
    <Big x={540} y={900} size={96} color={C.amber} o={sp(f, 24, 38)}>khoảng cách</Big>
    <Big x={540} y={1030} size={96} color={C.cream} o={sp(f, 32, 46)}>×</Big>
    <Big x={540} y={1160} size={96} color={C.amber} o={sp(f, 40, 54)}>tang góc ngắm</Big>
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Vậy cây cao" b="30 × 1 = 30 mét" />
    <Tree x={820} y={1250} h={400} />
    <Calc f={f} x={380} y={760} lines={[{t: '30 × 1', at: 6}, {t: '= 30 m', at: 24, color: C.amber, size: 110}]} />
  </g>
);

// --- Cảnh 3 ---
const P10: Panel = ({f}) => (
  <g>
    <Head a="Nhưng với ngọn núi" b="đâu thể mang thước tới đo" />
    <Mtn x={700} y={1230} w={760} h={640} />
    <line x1={90} y1={1215} x2={460} y2={1215} stroke={C.cream} strokeWidth={14} strokeLinecap="round" opacity={sp(f, 6, 20)} />
    {Array.from({length: 8}, (_, i) => <line key={i} x1={110 + i * 48} y1={1215} x2={110 + i * 48} y2={1185} stroke={C.cream} strokeWidth={4} opacity={sp(f, 6, 20)} />)}
    <g opacity={sp(f, 24, 38)} stroke="#e0613b" strokeWidth={14} strokeLinecap="round">
      <line x1={190} y1={1090} x2={360} y2={1250} />
      <line x1={360} y1={1090} x2={190} y2={1250} />
    </g>
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Ngắm cùng một vật" b="từ hai đầu của một đoạn đã biết" />
    <Stake x={220} y={1230} />
    <Stake x={620} y={1230} />
    <line x1={220} y1={1230} x2={620} y2={1230} stroke={C.cream} strokeWidth={6} />
    <circle cx={800} cy={760} r={26} fill="#e0613b" stroke={C.cream} strokeWidth={5} opacity={sp(f, 4, 16)} />
    <Arrow x1={220} y1={1160} x2={780} y2={790} p={sp(f, 10, 40)} color={C.amber} w={5} />
    <Arrow x1={620} y1={1160} x2={790} y2={800} p={sp(f, 20, 46)} color="#8fd1ff" w={5} />
    <Tag x={410} y={1310} color={C.cream} size={38} o={sp(f, 30, 44)}>đoạn đã biết</Tag>
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Bên kia sông có cột cờ" b="bên này hai cọc cách nhau 100 m" />
    <River y={820} o={sp(f, 2, 14)} />
    <Flag x={540} y={850} o={sp(f, 6, 20)} />
    <Stake x={340} y={1150} />
    <Stake x={740} y={1150} />
    <line x1={340} y1={1150} x2={740} y2={1150} stroke={C.cream} strokeWidth={6} />
    <Big x={540} y={1215} size={64} color={C.amber} o={sp(f, 24, 38)}>100 m</Big>
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Từ mỗi cọc nhìn sang cột cờ" b="góc đo được đều là 45 độ" />
    <River y={820} />
    <Flag x={540} y={850} />
    <Stake x={340} y={1150} />
    <Stake x={740} y={1150} />
    <line x1={340} y1={1150} x2={740} y2={1150} stroke={C.cream} strokeWidth={6} />
    <Arrow x1={340} y1={1080} x2={535} y2={875} p={sp(f, 6, 30)} color={C.amber} w={5} />
    <Arrow x1={740} y1={1080} x2={545} y2={875} p={sp(f, 16, 40)} color="#8fd1ff" w={5} />
    <Big x={250} y={1000} size={60} color={C.amber} o={sp(f, 30, 44)}>45°</Big>
    <Big x={840} y={1000} size={60} color="#8fd1ff" o={sp(f, 38, 52)}>45°</Big>
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Cột cờ cách đoạn nối hai cọc" b="100 ÷ 2 = 50 mét" />
    <Calc f={f} x={620} y={700} lines={[{t: '100 ÷ 2', at: 6}, {t: '= 50 m', at: 26, color: C.amber, size: 120}]} />
    <g opacity={sp(f, 4, 18)}>
      <path d="M 100 1150 L 500 1150 L 300 950 Z" fill="none" stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
      <line x1={300} y1={1150} x2={300} y2={950} stroke={C.amber} strokeWidth={6} strokeDasharray="12 10" />
      <Lab x={560} y={1050} size={44} anchor="start" color={C.amber}>cao 50 m</Lab>
      <Lab x={300} y={1215} size={38} color={C.cream}>100 m</Lab>
    </g>
  </g>
);
const P15: Panel = ({f}) => {
  const A = (i: number) => [110 + i * 125, 1230 - i * 60];
  const B = (i: number) => [170 + i * 125, 1030 - i * 60];
  const tri = (a: number[], b: number[], c: number[], k: number) => (
    <path key={k} d={`M ${a[0]} ${a[1]} L ${b[0]} ${b[1]} L ${c[0]} ${c[1]} Z`} fill={C.amber} fillOpacity={0.18} stroke={C.amber} strokeWidth={5} strokeLinejoin="round" opacity={sp(f, 6 + k * 4, 16 + k * 4)} />
  );
  const out: React.ReactNode[] = [];
  for (let i = 0; i < 6; i++) {
    out.push(tri(A(i), B(i), A(i + 1), i * 2));
    out.push(tri(B(i), A(i + 1), B(i + 1), i * 2 + 1));
  }
  return (
    <g>
      <Head a="Nối từng tam giác" b="từ bờ biển lên chân dãy núi" />
      {out}
      <path d="M 110 1290 Q 150 1262 190 1290 T 270 1290" fill="none" stroke="#9fd0ff" strokeWidth={5} opacity={0.8} />
      <Tag x={200} y={1335} color={C.cream} size={36} o={sp(f, 4, 16)}>bờ biển</Tag>
      <Mtn x={900} y={660} w={280} h={220} o={sp(f, 46, 60)} />
    </g>
  );
};

// --- Cảnh 4 ---
const STX = [130, 290, 450, 610, 770, 930];
const P16: Panel = ({f}) => (
  <g>
    <Head a="Năm 1849: nhóm khảo sát" b="ngắm đỉnh từ 6 trạm" />
    <Mtn x={540} y={800} w={380} h={240} />
    {STX.map((x, i) => <Arrow key={i} x1={x} y1={1165} x2={540 + (x - 540) * 0.08} y2={600} p={sp(f, 6 + i * 6, 34 + i * 6)} color={i % 2 ? '#8fd1ff' : C.amber} w={3} />)}
    {STX.map((x, i) => <Station key={i} x={x} y={1180} />)}
  </g>
);
const NUMS = ['28 992', '29 005', '29 002', '28 999', '29 026', '28 990'];
const P17: Panel = ({f}) => (
  <g>
    <Head a="Mỗi trạm cho" b="một kết quả riêng (phít)" />
    {NUMS.map((n, i) => (
      <Big key={i} x={i % 2 ? 760 : 320} y={620 + Math.floor(i / 2) * 150} size={80} color={i % 2 ? '#8fd1ff' : C.amber} o={sp(f, 6 + i * 8, 16 + i * 8)}>{n}</Big>
    ))}
    <HatHero x={200} y={1250} s={2} walk={f * 0.12} hat="scholar" />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Trung bình của 6 kết quả" b="là 29 002 phít" />
    <Big x={540} y={820} size={150} color={C.amber} o={sp(f, 8, 26)}>29 002</Big>
    <Big x={540} y={960} size={90} color={C.cream} o={sp(f, 18, 34)}>phít</Big>
    <Mtn x={540} y={1250} w={420} h={260} o={sp(f, 26, 42)} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Năm 1856, ông Oóc" b="công bố con số ấy" />
    <Big x={540} y={860} size={230} color={C.amber} o={sp(f, 6, 24)}>1856</Big>
    <HatHero x={540} y={1250} s={2} walk={f * 0.2} hat="scholar" cheer={sp(f, 24, 44)} />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Một phít dài khoảng 30 cm" b="nên ta đổi sang mét" />
    <g opacity={sp(f, 6, 22)}>
      <rect x={140} y={760} width={800} height={110} rx={10} fill="#d6a83a" stroke={C.cream} strokeWidth={6} />
      {Array.from({length: 12}, (_, i) => <line key={i} x1={140 + (i + 1) * 61.5} y1={760} x2={140 + (i + 1) * 61.5} y2={i % 3 === 2 ? 820 : 800} stroke={C.ink} strokeWidth={4} />)}
    </g>
    <Big x={540} y={1000} size={110} color={C.amber} o={sp(f, 22, 38)}>1 phít ≈ 30 cm</Big>
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Đổi 29 002 phít" b="ra mét" />
    <Calc f={f} y={700} lines={[{t: '29 002 × 0,3048', at: 6, size: 84}, {t: '≈ 8 840 m', at: 26, color: C.amber, size: 130}]} />
  </g>
);

// --- Cảnh 5 ---
const P22: Panel = ({f}) => (
  <g>
    <Head a="Nhưng Trái Đất tròn" b="nên đỉnh ở xa trông thấp hơn" />
    <Earth o={sp(f, 2, 14)} />
    <Mtn x={930} y={1240} w={240} h={420} o={sp(f, 8, 22)} />
    <HatHero x={150} y={1210} s={1} walk={f * 0.1} hat="scholar" />
    <Dash x1={190} y1={1165} x2={930} y2={1165} p={sp(f, 18, 46)} />
    <Tag x={520} y={1100} color={C.amber} size={40} o={sp(f, 36, 50)}>đường ngắm thẳng</Tag>
  </g>
);
const P23: Panel = ({f}) => (
  <g>
    <Head a="Phần thấp đi =" b="khoảng cách × khoảng cách ÷ (2 × R)" />
    <Big x={540} y={700} size={78} color={C.amber} o={sp(f, 6, 20)}>d × d</Big>
    <Big x={540} y={820} size={78} color={C.cream} o={sp(f, 16, 30)}>÷ (2 × R)</Big>
    <Tag x={540} y={930} color={C.cream} size={42} o={sp(f, 26, 40)}>R là bán kính Trái Đất</Tag>
    <Earth o={0.9} />
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Hai lần bán kính Trái Đất" />
    <Calc f={f} y={700} lines={[{t: '2 × 6 371', at: 6}, {t: '≈ 12 742 km', at: 26, color: C.amber, size: 120}]} />
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Khoảng cách tới đỉnh" b="là 174 km" />
    <Calc f={f} y={700} lines={[{t: '174 × 174', at: 6}, {t: '= 30 276', at: 26, color: C.amber, size: 130}]} />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Rồi đem chia" />
    <Calc f={f} y={700} lines={[{t: '30 276 ÷ 12 742', at: 6, size: 84}, {t: '≈ 2,4 km', at: 26, color: C.amber, size: 140}]} />
    <Tag x={540} y={1030} color={C.cream} size={42} o={sp(f, 40, 54)}>đỉnh trông thấp đi chừng đó</Tag>
  </g>
);
const P27: Panel = ({f}) => (
  <g>
    <Head a="Phải cộng thêm phần ấy" b="và sửa cả chỗ không khí bẻ tia nhìn" />
    <Big x={540} y={700} size={150} color={C.amber} o={sp(f, 6, 22)}>+ 2,4 km</Big>
    <path d="M 120 1000 Q 300 930 540 1000 T 960 940" fill="none" stroke="#9fd0ff" strokeWidth={8} strokeLinecap="round" opacity={sp(f, 20, 36)} />
    <Tag x={540} y={1090} color={C.cream} size={42} o={sp(f, 30, 44)}>không khí làm cong tia nhìn</Tag>
    <HatHero x={200} y={1250} s={2} walk={f * 0.12} hat="scholar" />
  </g>
);

// --- Cảnh 6 ---
const P28: Panel = ({f}) => (
  <g>
    <Head a="Năm 2020, Nê-pan và Trung Quốc" b="đo lại bằng góc ngắm và vệ tinh" />
    <Mtn x={540} y={1240} w={620} h={440} />
    <g transform={`translate(${760 + Math.sin(f * 0.05) * 20} 560)`} opacity={sp(f, 6, 20)}>
      <rect x={-34} y={-20} width={68} height={40} rx={8} fill="#b8c4d8" stroke={C.cream} strokeWidth={4} />
      <rect x={-96} y={-12} width={52} height={24} fill="#4a7fd0" stroke={C.cream} strokeWidth={3} />
      <rect x={44} y={-12} width={52} height={24} fill="#4a7fd0" stroke={C.cream} strokeWidth={3} />
    </g>
    <Dash x1={760} y1={600} x2={560} y2={830} p={sp(f, 20, 50)} />
    <Big x={300} y={720} size={110} color={C.amber} o={sp(f, 12, 28)}>2020</Big>
  </g>
);
const P29: Panel = ({f}) => (
  <g>
    <Head a="Nhờ vậy họ có kết quả mới" />
    <Big x={540} y={820} size={140} color={C.amber} o={sp(f, 8, 26)}>8 848,86</Big>
    <Big x={540} y={960} size={90} color={C.cream} o={sp(f, 18, 34)}>mét</Big>
    <Mtn x={540} y={1250} w={420} h={260} o={sp(f, 26, 42)} />
  </g>
);
const P30: Panel = ({f}) => (
  <g>
    <Head a="Số năm 1856 chỉ thấp hơn" b="khoảng 9 mét" />
    <Lab x={110} y={680} size={40} anchor="start" color={C.cream}>1856: 8 839,8 m</Lab>
    <Bar x={110} y={710} w={860} color="#e0613b" p={8839.8 / 8848.86} />
    <Lab x={110} y={880} size={40} anchor="start" color={C.cream}>2020: 8 848,86 m</Lab>
    <Bar x={110} y={910} w={860} color="#6fd18f" p={sp(f, 14, 40)} />
    <Big x={540} y={1130} size={110} color={C.amber} o={sp(f, 36, 52)}>lệch 9 m</Big>
  </g>
);
const P31: Panel = ({f}) => (
  <g>
    <Head a="Độ lệch so với chiều cao" />
    <Calc f={f} y={700} lines={[{t: '9 ÷ 8 849', at: 6}, {t: '≈ 0,001', at: 26, color: C.amber, size: 140}]} />
    <Tag x={540} y={1030} color={C.cream} size={46} o={sp(f, 40, 54)}>chỉ một phần nghìn</Tag>
  </g>
);
const P32: Panel = ({f}) => (
  <g>
    <Head a="Đo được ngọn núi" b="chưa ai lên tới" />
    {['một góc ngắm', 'một đoạn đã biết', 'một phép nhân'].map((t, i) => (
      <g key={i} opacity={sp(f, 6 + i * 12, 18 + i * 12)}>
        <rect x={160} y={620 + i * 150} width={760} height={110} rx={22} fill="#122238" stroke={C.cream} strokeWidth={5} />
        <Big x={540} y={700 + i * 150} size={62} color={C.amber}>{t}</Big>
      </g>
    ))}
    <HatHero x={200} y={1250} s={2} walk={f * 0.25} hat="scholar" cheer={sp(f, 30, 50)} />
    <Mtn x={800} y={1250} w={300} h={200} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30, P31, P32];
void lerp;
