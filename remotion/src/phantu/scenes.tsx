import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const OIL = '#f2c14e';
const WATER = '#1d5163';
const MOL = '#ffd37a';
const RED = '#e0613b';

const Hero2: React.FC<{f: number; x?: number; cheer?: number}> = ({f, x = 170, cheer = 0}) => <HatHero x={x} y={1250} s={2} walk={f * 0.13} cheer={cheer} hat="goggles" />;

const Spoon: React.FC<{x: number; y: number; rot?: number; o?: number; fill?: number}> = ({x, y, rot = -25, o = 1, fill = 1}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot})`} opacity={clamp01(o)}>
    <line x1={0} y1={0} x2={190} y2={0} stroke={C.cream} strokeWidth={12} strokeLinecap="round" />
    <ellipse cx={0} cy={0} rx={52} ry={34} fill="#b9bdc4" stroke={C.cream} strokeWidth={6} />
    <ellipse cx={0} cy={2} rx={42} ry={24} fill={OIL} fillOpacity={0.9 * fill} />
  </g>
);
const Mol: React.FC<{x: number; y: number; s?: number; o?: number}> = ({x, y, s = 1, o = 1}) => (
  <g opacity={clamp01(o)} transform={`translate(${x} ${y}) scale(${s})`}>
    <circle cx={0} cy={0} r={12} fill={MOL} stroke={C.cream} strokeWidth={3} />
    <path d="M 0 12 q 6 12 0 24 q -6 12 0 24" fill="none" stroke={MOL} strokeWidth={4} strokeLinecap="round" />
  </g>
);
const Wave: React.FC<{f: number; y: number; amp: number; x1?: number; x2?: number; o?: number; color?: string}> = ({f, y, amp, x1 = 120, x2 = 960, o = 1, color = '#8fd0e0'}) => {
  const pts = Array.from({length: 41}, (_, i) => {
    const x = lerp(x1, x2, i / 40);
    return `${i ? 'L' : 'M'} ${x} ${y + amp * Math.sin(i * 0.9 - f * 0.18)}`;
  }).join(' ');
  return <path d={pts} fill="none" stroke={color} strokeWidth={6} strokeLinecap="round" opacity={o} />;
};
const Pond: React.FC<{o?: number; cy?: number}> = ({o = 1, cy = 840}) => (
  <ellipse cx={540} cy={cy} rx={430} ry={260} fill={WATER} stroke={C.cream} strokeWidth={6} opacity={clamp01(o)} />
);
const Court: React.FC<{x: number; y: number; o?: number}> = ({x, y, o = 1}) => (
  <g opacity={clamp01(o)} stroke={C.cream} strokeWidth={4} fill="#c98a4a" fillOpacity={0.55}>
    <rect x={x - 70} y={y - 38} width={140} height={75} />
    <line x1={x} y1={y - 38} x2={x} y2={y + 37} />
    <circle cx={x} cy={y} r={14} fill="none" />
  </g>
);

// --- Cảnh 1 ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Phân tử nhỏ đến mức" b="kính hiển vi thường không thấy" />
    <circle cx={500} cy={780} r={190} fill="#0f252d" stroke={C.cream} strokeWidth={10} />
    <line x1={640} y1={920} x2={780} y2={1060} stroke={C.cream} strokeWidth={22} strokeLinecap="round" />
    {[0, 1, 2, 3, 4].map((i) => (
      <circle key={i} cx={440 + (i % 3) * 50} cy={730 + Math.floor(i / 3) * 70} r={5} fill={MOL} opacity={sp(f, 6 + i * 3, 16 + i * 3) * 0.7} />
    ))}
    <Big x={860} y={640} size={150} color={C.amber} o={0.9 * sp(f, 20, 36)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Chỉ cần một muỗng dầu" b="và một cái ao" />
    <Pond o={sp(f, 2, 14)} cy={900} />
    <Spoon x={300} y={540} o={sp(f, 8, 22)} />
    <Hero2 f={f} />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Ước lượng độ dày" b="của một phân tử dầu" />
    <Mol x={540} y={700} s={4.5} o={sp(f, 4, 18)} />
    <Tag x={540} y={1130} color={MOL} size={46} o={sp(f, 16, 30)}>một phân tử dầu</Tag>
    <Hero2 f={f} />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Chuyện bắt đầu ở" b="một cái ao ngoài trời" />
    <Pond cy={860} />
    <Wave f={f} y={800} amp={14} x1={200} x2={880} o={0.7} />
    <Wave f={f + 20} y={900} amp={12} x1={200} x2={880} o={0.5} />
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 2: ao ---
const P4: Panel = ({f}) => (
  <g>
    <Head a="Thư năm 1773" b="Phrăng-lin kể lại cái ao" />
    <rect x={250} y={500} width={580} height={620} rx={14} fill="#e9dcc0" stroke={C.cream} strokeWidth={5} opacity={sp(f, 2, 14)} />
    {Array.from({length: 9}).map((_, i) => (
      <line key={i} x1={300} y1={580 + i * 48} x2={780 - (i % 3) * 60} y2={580 + i * 48} stroke="#8a7a62" strokeWidth={5} strokeLinecap="round" opacity={sp(f, 6 + i * 2, 16 + i * 2)} />
    ))}
    <Big x={540} y={1240} size={96} color={C.amber} o={sp(f, 14, 28)}>1773</Big>
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Gió làm ao nổi sóng" b="ông đổ xuống một muỗng dầu" />
    <Pond cy={900} />
    <Wave f={f} y={830} amp={20} x1={200} x2={880} />
    <Wave f={f + 15} y={920} amp={18} x1={200} x2={880} o={0.7} />
    <Spoon x={470} y={560 + 60 * sp(f, 8, 24)} rot={-25 - 40 * sp(f, 14, 30)} />
    <circle cx={470} cy={840} r={8 + 26 * sp(f, 22, 40)} fill={OIL} opacity={sp(f, 22, 34)} />
  </g>
);
const P6: Panel = ({f}) => {
  const k = sp(f, 4, 40);
  return (
    <g>
      <Head a="Cả một góc ao lặng đi" b="phẳng như mặt gương" />
      <Pond cy={900} />
      <ellipse cx={540} cy={900} rx={lerp(30, 370, k)} ry={lerp(18, 210, k)} fill={OIL} fillOpacity={0.28} stroke={OIL} strokeWidth={5} />
      <Wave f={f} y={880} amp={16 * (1 - k)} x1={170} x2={910} />
      <Tag x={540} y={1240} color={OIL} size={46} o={sp(f, 26, 40)}>lặng như mặt gương</Tag>
    </g>
  );
};
const P7: Panel = ({f}) => (
  <g>
    <Head a="Rộng chừng nửa mẫu Anh" b="khoảng 2 000 mét vuông" />
    <ellipse cx={540} cy={820} rx={400} ry={230} fill={OIL} fillOpacity={0.2} stroke={OIL} strokeWidth={6} strokeDasharray="16 12" opacity={sp(f, 2, 16)} />
    <Big x={540} y={840} size={120} color={C.amber} o={sp(f, 12, 28)}>2 000 m²</Big>
    <Tag x={540} y={1160} color={C.cream} size={46} o={sp(f, 20, 34)}>nửa mẫu Anh</Tag>
    <Hero2 f={f} />
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Bằng khoảng" b="5 sân bóng rổ" />
    <ellipse cx={540} cy={820} rx={400} ry={230} fill={OIL} fillOpacity={0.12} stroke={OIL} strokeWidth={5} strokeDasharray="16 12" />
    {[[370, 740], [540, 740], [710, 740], [455, 860], [625, 860]].map((p, i) => (
      <Court key={i} x={p[0]} y={p[1]} o={sp(f, 4 + i * 5, 16 + i * 5)} />
    ))}
    <Big x={540} y={1170} size={100} color={C.amber} o={sp(f, 26, 40)}>≈ 5 sân</Big>
  </g>
);
// --- Cảnh 3: mỏng thế nào ---
const P9: Panel = ({f}) => (
  <g>
    <Head a="Một muỗng dầu" b="trải rộng chừng ấy" />
    <Spoon x={200} y={820} rot={-12} />
    <Arrow x1={330} y1={820} x2={470} y2={820} p={sp(f, 6, 22)} />
    <ellipse cx={730} cy={820} rx={260} ry={170} fill={OIL} fillOpacity={0.2} stroke={OIL} strokeWidth={6} opacity={sp(f, 16, 30)} />
    <Big x={540} y={1130} size={100} color={C.amber} o={0.9 * sp(f, 24, 40)}>mỏng thế nào?</Big>
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Như phết bơ lên bánh mì" b="trải càng rộng càng mỏng" />
    <rect x={120} y={600} width={300} height={300} rx={40} fill="#d9a85a" stroke={C.cream} strokeWidth={5} />
    <rect x={150} y={640} width={110} height={110} rx={14} fill="#fff1a8" opacity={sp(f, 6, 18)} />
    <rect x={560} y={600} width={400} height={300} rx={40} fill="#d9a85a" stroke={C.cream} strokeWidth={5} />
    <rect x={590} y={630} width={340} height={240} rx={14} fill="#fff1a8" opacity={0.45 * sp(f, 16, 30)} />
    <Tag x={270} y={1000} color={C.cream} size={40} o={sp(f, 10, 22)}>bơ dày</Tag>
    <Tag x={760} y={1000} color={C.amber} size={40} o={sp(f, 20, 34)}>bơ mỏng</Tag>
    <Hero2 f={f} x={540} />
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Phrăng-lin không tính" b="Rây-lây mới tính" />
    <line x1={140} y1={820} x2={940} y2={820} stroke={C.cream} strokeWidth={6} />
    <circle cx={140} cy={820} r={16} fill={C.amber} />
    <circle cx={940} cy={820} r={16} fill={C.amber} opacity={sp(f, 14, 28)} />
    <Big x={140} y={760} size={64} color={C.cream}>1773</Big>
    <Big x={940} y={760} size={64} color={C.cream} o={sp(f, 14, 28)}>1890</Big>
    <Big x={540} y={960} size={100} color={C.amber} o={sp(f, 22, 36)}>hơn 100 năm</Big>
    <Hero2 f={f} />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Dầu trải đến khi chỉ còn" b="một lớp phân tử" />
    <rect x={100} y={880} width={880} height={110} fill={WATER} stroke={C.cream} strokeWidth={5} />
    {Array.from({length: 14}).map((_, i) => (
      <Mol key={i} x={140 + i * 61} y={850} s={1.5} o={sp(f, 2 + i * 2, 12 + i * 2)} />
    ))}
    <Tag x={540} y={1120} color={C.cream} size={44} o={sp(f, 26, 40)}>nằm cạnh nhau, một lớp</Tag>
    <Hero2 f={f} />
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Độ dày lớp dầu" b="= độ dày một phân tử" />
    <rect x={100} y={880} width={880} height={110} fill={WATER} stroke={C.cream} strokeWidth={5} />
    {Array.from({length: 14}).map((_, i) => (
      <Mol key={i} x={140 + i * 61} y={850} s={1.5} />
    ))}
    <path d="M 70 810 L 90 810 L 90 905 L 70 905" fill="none" stroke={C.amber} strokeWidth={6} opacity={sp(f, 6, 18)} />
    <Big x={540} y={1130} size={72} color={C.amber} o={sp(f, 12, 28)}>dày bằng 1 phân tử</Big>
    <Hero2 f={f} />
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Thể tích = diện tích × độ dày" b="độ dày = thể tích ÷ diện tích" />
    <path d="M 220 700 L 780 700 L 880 640 L 320 640 Z" fill={OIL} fillOpacity={0.3} stroke={OIL} strokeWidth={5} opacity={sp(f, 2, 14)} />
    <path d="M 220 700 L 780 700 L 780 750 L 220 750 Z" fill={OIL} fillOpacity={0.5} stroke={OIL} strokeWidth={5} opacity={sp(f, 2, 14)} />
    <path d="M 780 700 L 880 640 L 880 690 L 780 750 Z" fill={OIL} fillOpacity={0.4} stroke={OIL} strokeWidth={5} opacity={sp(f, 2, 14)} />
    <Tag x={540} y={600} color={C.cream} size={40} o={sp(f, 10, 22)}>diện tích</Tag>
    <Tag x={540} y={810} color={C.cream} size={40} o={sp(f, 14, 26)}>độ dày (rất mỏng)</Tag>
    <Calc f={f} y={1010} step={110} lines={[{t: 'độ dày = thể tích ÷ diện tích', at: 20, size: 66, color: C.amber}]} />
  </g>
);
// --- Cảnh 4: tính ---
const P15: Panel = ({f}) => (
  <g>
    <Head a="Một muỗng cà phê" b="chứa khoảng 5 cm³ dầu" />
    <Spoon x={380} y={820} rot={-15} o={sp(f, 2, 14)} />
    <Big x={540} y={1100} size={130} color={C.amber} o={sp(f, 12, 28)}>5 cm³</Big>
    <Hero2 f={f} />
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Đổi ra mi-li-mét khối" />
    <Calc f={f} y={780} step={160} lines={[{t: '5 cm³', at: 2, size: 120}, {t: '= 5 000 mm³', at: 14, size: 120, color: C.amber}]} />
    <Hero2 f={f} />
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Đổi diện tích" b="ra mi-li-mét vuông" />
    <Calc f={f} y={780} step={160} lines={[{t: '2 000 m²', at: 2, size: 120}, {t: '= 2 tỉ mm²', at: 14, size: 120, color: C.amber}]} />
    <Hero2 f={f} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Độ dày" />
    <Calc f={f} y={800} step={160} lines={[{t: '5 000 ÷ 2 tỉ', at: 4, size: 120, color: C.amber}]} />
    <Hero2 f={f} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Độ dày lớp dầu" />
    <Calc f={f} y={760} step={150} lines={[{t: '= 2,5 phần triệu', at: 2, size: 110, color: C.amber}, {t: 'mi-li-mét', at: 8, size: 110, color: C.amber}, {t: '0,0000025 mm', at: 16, size: 76, color: C.cream}]} />
    <Hero2 f={f} cheer={sp(f, 14, 30)} />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Tờ giấy dày 0,1 mm" b="gấp 40 000 lần lớp dầu" />
    <rect x={140} y={700} width={800} height={90 * sp(f, 2, 16)} fill="#e9dcc0" stroke={C.cream} strokeWidth={4} />
    <Tag x={540} y={870} color={C.cream} size={42} o={sp(f, 10, 22)}>tờ giấy: 0,1 mm</Tag>
    <rect x={140} y={960} width={800} height={3} fill={OIL} opacity={sp(f, 16, 28)} />
    <Tag x={540} y={1040} color={OIL} size={42} o={sp(f, 20, 32)}>lớp dầu: mỏng hơn 40 000 lần</Tag>
    <Hero2 f={f} />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="1 phần triệu mi-li-mét" b="= 1 na-nô-mét" />
    <Calc f={f} y={760} step={150} lines={[{t: '1 nm = 1 phần triệu mm', at: 2, size: 72, color: C.cream}, {t: 'lớp dầu ≈ 2,5 nm', at: 14, size: 100, color: C.amber}]} />
    <Hero2 f={f} />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Rây-lây tính ra cỡ 2 nm" b="cùng cỡ một phân tử dầu" />
    <Mol x={540} y={700} s={4.5} />
    <Big x={540} y={1130} size={110} color={C.amber} o={sp(f, 8, 24)}>≈ 2 nm</Big>
    <Hero2 f={f} cheer={sp(f, 14, 30)} />
  </g>
);
const P23: Panel = ({f}) => (
  <g>
    <Head a="Muỗng và diện tích ao" b="chỉ là ước chừng" />
    <Spoon x={260} y={800} rot={-15} />
    <Big x={260} y={960} size={120} color={C.amber} o={0.9 * sp(f, 6, 20)}>?</Big>
    <ellipse cx={720} cy={800} rx={220} ry={140} fill={OIL} fillOpacity={0.2} stroke={OIL} strokeWidth={5} strokeDasharray="14 10" />
    <Big x={720} y={960} size={120} color={C.amber} o={0.9 * sp(f, 12, 26)}>?</Big>
    <Tag x={540} y={1160} color={C.cream} size={46} o={sp(f, 20, 34)}>chỉ đúng về cỡ độ lớn</Tag>
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Phân tử nhỏ đến mức nào" b="mà vẫn đo được" />
    <Mol x={540} y={720} s={3.2} />
    <Tag x={540} y={1050} color={C.amber} size={52} o={sp(f, 10, 24)}>vẫn đo được!</Tag>
    <Hero2 f={f} cheer={sp(f, 12, 28)} />
  </g>
);
const P25: Panel = ({f}) => {
  const k = sp(f, 6, 40);
  return (
    <g>
      <Head a="Lăng-muya trải màng mỏng" b="ước diện tích mỗi phân tử" />
      <rect x={120} y={780} width={840} height={150} fill={WATER} stroke={C.cream} strokeWidth={5} />
      <rect x={120 + (840 - lerp(840, 520, k))} y={780} width={lerp(840, 520, k)} height={150} fill={OIL} fillOpacity={0.25} />
      <line x1={120 + (840 - lerp(840, 520, k))} y1={750} x2={120 + (840 - lerp(840, 520, k))} y2={960} stroke={RED} strokeWidth={10} />
      <Tag x={540} y={1060} color={C.cream} size={44} o={sp(f, 20, 34)}>nén màng dầu lại</Tag>
      <Hero2 f={f} />
    </g>
  );
};
const P26: Panel = ({f}) => (
  <g>
    <Head a="Muốn đo thứ nhỏ nhất" b="trải thật mỏng, chia thể tích" />
    <Spoon x={190} y={740} rot={-12} />
    <Arrow x1={330} y1={740} x2={450} y2={740} p={sp(f, 4, 18)} />
    <ellipse cx={700} cy={740} rx={230} ry={130} fill={OIL} fillOpacity={0.22} stroke={OIL} strokeWidth={5} opacity={sp(f, 12, 26)} />
    <Big x={540} y={990} size={84} color={C.amber} o={sp(f, 18, 34)}>thể tích ÷ diện tích</Big>
    <Hero2 f={f} x={540} cheer={sp(f, 18, 34)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26];
