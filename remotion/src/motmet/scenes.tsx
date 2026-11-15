import React from 'react';
import {Arrow, Bar, Big, C, Calc, Dash, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const GOLD = '#c9a86a';
const RED = '#e0613b';
const PLAT = '#d6dbe2';
const RIVER = '#3f78b5';
const BEAM = '#9fe8ff';

const Earth: React.FC<{x: number; y: number; r: number; o?: number}> = ({x, y, r, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill="#2f6fa8" stroke={C.cream} strokeWidth={6} />
    <path d={`M ${x - r * 0.5} ${y - r * 0.55} q ${r * 0.35} ${-r * 0.1} ${r * 0.5} ${r * 0.2} q ${-r * 0.1} ${r * 0.4} ${-r * 0.45} ${r * 0.35} z`} fill="#4f9a5a" />
    <path d={`M ${x + r * 0.1} ${y + r * 0.15} q ${r * 0.4} ${-r * 0.1} ${r * 0.5} ${r * 0.25} q ${-r * 0.2} ${r * 0.4} ${-r * 0.5} ${r * 0.2} z`} fill="#4f9a5a" />
    <line x1={x - r} y1={y} x2={x + r} y2={y} stroke={C.cream} strokeWidth={2} strokeDasharray="8 8" opacity={0.6} />
  </g>
);
// Cung kinh tuyến từ cực Bắc (góc -90°) tới góc a (độ) theo nửa phải của vòng tròn.
const arcPath = (x: number, y: number, r: number, a0: number, a1: number) => {
  const p0 = [x + r * Math.cos((a0 * Math.PI) / 180), y + r * Math.sin((a0 * Math.PI) / 180)];
  const p1 = [x + r * Math.cos((a1 * Math.PI) / 180), y + r * Math.sin((a1 * Math.PI) / 180)];
  const large = Math.abs(a1 - a0) > 180 ? 1 : 0;
  return `M ${p0[0]} ${p0[1]} A ${r} ${r} 0 ${large} 1 ${p1[0]} ${p1[1]}`;
};
const Ruler: React.FC<{x: number; y: number; w: number; o?: number; color?: string}> = ({x, y, w, o = 1, color = GOLD}) => (
  <g opacity={clamp01(o)}>
    <rect x={x} y={y} width={w} height={70} fill={color} stroke={C.cream} strokeWidth={4} />
    {Array.from({length: 21}).map((_, i) => (
      <line key={i} x1={x + (w * i) / 20} y1={y} x2={x + (w * i) / 20} y2={y + (i % 10 === 0 ? 50 : i % 5 === 0 ? 36 : 22)} stroke="#2a2018" strokeWidth={3} />
    ))}
  </g>
);
const Tower: React.FC<{x: number; y: number; o?: number}> = ({x, y, o = 1}) => (
  <g opacity={clamp01(o)}>
    <path d={`M ${x - 30} ${y} L ${x - 18} ${y - 150} L ${x + 18} ${y - 150} L ${x + 30} ${y} Z`} fill="#8a7a62" stroke={C.cream} strokeWidth={4} />
    <path d={`M ${x - 26} ${y - 150} L ${x} ${y - 200} L ${x + 26} ${y - 150} Z`} fill="#6b5036" stroke={C.cream} strokeWidth={4} />
  </g>
);
const Dot: React.FC<{x: number; y: number; label?: string; lx?: number; color?: string; o?: number}> = ({x, y, label, lx = 40, color = RED, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={14} fill={color} stroke={C.cream} strokeWidth={4} />
    {label && <text x={x + lx} y={y + 14} textAnchor={lx < 0 ? 'end' : 'start'} fontFamily="BeVN" fontWeight={700} fontSize={40} fill={C.cream}>{label}</text>}
  </g>
);

// --- Cảnh 1 ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Vì sao một mét" b="dài đúng như vậy?" />
    <Ruler x={140} y={720} w={800} o={sp(f, 4, 20)} />
    <Tag x={540} y={880} color={C.amber} size={52} o={sp(f, 14, 28)}>1 mét</Tag>
    <Big x={540} y={1080} size={140} color={C.amber} o={0.9 * sp(f, 24, 40)}>?</Big>
    <HatHero x={180} y={1250} s={2} walk={f * 0.12} hat="pirate" />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Độ dài ấy không do ai" b="tùy tiện chọn" />
    <Ruler x={140} y={720} w={800} />
    <Tag x={540} y={920} color={RED} size={50} o={sp(f, 10, 24)}>✕ tùy tiện</Tag>
    <HatHero x={180} y={1250} s={2} walk={f * 0.12} hat="pirate" />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Lấy từ chính" b="kích thước Trái Đất" />
    <Earth x={540} y={820} r={260} o={sp(f, 4, 20)} />
    <Ruler x={390} y={1130} w={300} o={sp(f, 18, 32)} />
    <HatHero x={180} y={1250} s={2} walk={f * 0.12} cheer={sp(f, 24, 40)} hat="pirate" />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Đo cả Trái Đất" b="bằng cách nào?" />
    <Earth x={540} y={820} r={260} />
    <Big x={860} y={600} size={140} color={C.amber} o={0.9 * sp(f, 10, 26)}>?</Big>
  </g>
);

// --- Cảnh 2: thước chung ---
const P4: Panel = ({f}) => (
  <g>
    <Head a="Mỗi thị trấn" b="một kiểu đo khác nhau" />
    {[0, 1, 2, 3, 4].map((i) => (
      <Ruler key={i} x={140} y={560 + i * 120} w={500 + 300 * (0.5 + 0.5 * Math.sin(f * 0.06 + i * 1.7))} color={['#c9a86a', '#b08a52', '#d9b97c', '#a07448', '#c4a070'][i]} o={sp(f, 2 + i * 4, 14 + i * 4)} />
    ))}
    <HatHero x={540} y={1250} s={2} walk={f * 0.15} hat="pirate" />
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Khoảng 250 000" b="đơn vị đo khác nhau" />
    <Big x={540} y={800} size={170} color={C.amber} o={sp(f, 4, 22)}>250 000</Big>
    <Tag x={540} y={920} color={C.cream} size={48} o={sp(f, 16, 30)}>đơn vị đo (ước tính)</Tag>
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="pirate" />
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Một thước đo chung" b="lấy từ Trái Đất" />
    <Earth x={330} y={820} r={190} />
    <Arrow x1={560} y1={820} x2={700} y2={820} p={sp(f, 8, 28)} color={C.amber} />
    <Ruler x={720} y={785} w={240} o={sp(f, 20, 34)} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="pirate" />
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="1 mét = 1 phần 10 triệu" b="quãng cực – xích đạo" />
    <Earth x={420} y={820} r={260} />
    <path d={arcPath(420, 820, 260, -90, lerp(-90, 0, sp(f, 6, 34)))} fill="none" stroke={RED} strokeWidth={12} strokeLinecap="round" />
    <Dot x={420} y={560} color={C.cream} />
    <Tag x={300} y={540} color={C.cream} size={40}>Bắc Cực</Tag>
    <Tag x={830} y={1000} color={C.cream} size={40} o={sp(f, 30, 44)}>xích đạo</Tag>
    <Big x={540} y={1210} size={90} color={C.amber} o={sp(f, 34, 50)}>÷ 10 000 000</Big>
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Dọc đường kinh tuyến" b="chạy qua Pa-ri" />
    <Earth x={540} y={840} r={300} />
    <path d={`M 540 540 Q 680 840 540 1140`} fill="none" stroke={RED} strokeWidth={8} strokeDasharray="1000" strokeDashoffset={1000 * (1 - sp(f, 4, 34))} />
    <Dot x={598} y={680} label="Pa-ri" color={C.amber} o={sp(f, 24, 38)} />
  </g>
);

// --- Cảnh 3: đoạn đo ---
const P9: Panel = ({f}) => (
  <g>
    <Head a="Không ai đi bộ" b="từ cực tới xích đạo" />
    <Earth x={540} y={840} r={300} />
    <path d={arcPath(540, 840, 300, -90, 0)} fill="none" stroke={RED} strokeWidth={8} strokeDasharray="14 12" />
    <Tag x={870} y={620} color={RED} size={70} o={sp(f, 20, 34)}>✕</Tag>
    <HatHero x={540 + 300 * Math.cos(-Math.PI / 2 + sp(f, 0, 60) * 0.3)} y={840 + 300 * Math.sin(-Math.PI / 2 + sp(f, 0, 60) * 0.3) - 10} s={0.9} walk={f * 0.2} hat="pirate" />
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Chỉ đo một đoạn ngắn" b="Đăng-kéc → Bác-xê-lô-na" />
    <path d="M 420 520 Q 380 700 460 820 Q 300 900 330 1000 Q 520 1060 640 1110 L 760 1180" fill="none" stroke={GOLD} strokeWidth={5} opacity={0.6} />
    <line x1={540} y1={560} x2={540} y2={1180} stroke={RED} strokeWidth={10} strokeDasharray="700" strokeDashoffset={700 * (1 - sp(f, 6, 40))} />
    <Dot x={540} y={560} label="Đăng-kéc (Pháp)" />
    <Dot x={540} y={1180} label="Bác-xê-lô-na" o={sp(f, 30, 44)} />
    <Tag x={700} y={880} color={C.cream} size={36} o={sp(f, 16, 30)}>Pa-ri</Tag>
    <circle cx={548} cy={870} r={8} fill={C.cream} opacity={sp(f, 16, 30)} />
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Đơ-lăm-bơ và Mê-sanh" b="đo suốt hơn 6 năm" />
    <Big x={540} y={780} size={150} color={C.amber} o={sp(f, 10, 28)}>hơn 6 năm</Big>
    <HatHero x={330} y={1250} s={2} walk={f * 0.15} hat="pirate" />
    <HatHero x={750} y={1250} s={2} walk={f * 0.15 + 2} hat="scholar" />
  </g>
);

// --- Cảnh 4: phép tam giác ---
const P12: Panel = ({f}) => (
  <g>
    <Head a="Không kéo thước 1 000 km" b="mà dùng phép tam giác" />
    <path d="M 250 1100 L 830 1100 L 540 600 Z" fill="none" stroke={C.amber} strokeWidth={10} strokeLinejoin="round" strokeDasharray="1700" strokeDashoffset={1700 * (1 - sp(f, 6, 40))} />
    <HatHero x={180} y={1250} s={2} walk={f * 0.12} hat="pirate" />
  </g>
);
const P13: Panel = ({f}) => {
  const n = Math.floor(sp(f, 4, 50) * 8);
  return (
    <g>
      <Head a="Đo thật kỹ một đoạn thẳng" b="dài hơn 10 km" />
      {Array.from({length: n}).map((_, i) => (
        <rect key={i} x={140 + i * 100} y={900} width={96} height={30} fill={PLAT} stroke={C.cream} strokeWidth={3} />
      ))}
      <Tag x={540} y={1020} color={C.cream} size={42} o={sp(f, 24, 40)}>thước bạch kim nối nhau</Tag>
      <HatHero x={140 + n * 100} y={1250} s={2} walk={f * 0.2} hat="pirate" />
    </g>
  );
};
const P14: Panel = ({f}) => (
  <g>
    <Head a="Từ hai đầu đoạn" b="đo góc nhìn tới ngọn tháp" />
    <line x1={200} y1={1100} x2={880} y2={1100} stroke={PLAT} strokeWidth={10} />
    <Tower x={540} y={720} />
    <Dash x1={200} y1={1100} x2={530} y2={600} p={sp(f, 6, 30)} color={C.amber} />
    <Dash x1={880} y1={1100} x2={550} y2={600} p={sp(f, 14, 38)} color={C.amber} />
    <path d={arcPath(200, 1100, 90, -57, 0)} fill="none" stroke={C.amber} strokeWidth={6} opacity={sp(f, 30, 44)} />
    <path d={arcPath(880, 1100, 90, 180, 237)} fill="none" stroke={C.amber} strokeWidth={6} opacity={sp(f, 34, 48)} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Biết 1 cạnh và 2 góc" b="tính được 2 cạnh còn lại" />
    <path d="M 220 1080 L 860 1080 L 540 600 Z" fill="none" stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
    <line x1={220} y1={1080} x2={860} y2={1080} stroke={PLAT} strokeWidth={12} />
    <Tag x={540} y={1150} color={PLAT} size={40}>đã đo</Tag>
    <line x1={220} y1={1080} x2={540} y2={600} stroke={C.amber} strokeWidth={10} opacity={sp(f, 14, 30)} />
    <line x1={860} y1={1080} x2={540} y2={600} stroke={C.amber} strokeWidth={10} opacity={sp(f, 22, 38)} />
    <Tag x={300} y={800} color={C.amber} size={40} o={sp(f, 26, 40)}>tính ra</Tag>
    <Tag x={790} y={800} color={C.amber} size={40} o={sp(f, 30, 44)}>tính ra</Tag>
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Như đo bề rộng sông" b="mà không lội qua" />
    <rect x={90} y={700} width={900} height={220} fill={RIVER} opacity={0.75} />
    <path d="M 720 690 l 40 -100 l 40 100 z" fill="#4f9a5a" stroke={C.cream} strokeWidth={4} />
    <rect x={752} y={680} width={16} height={30} fill="#6b5036" />
    <line x1={260} y1={980} x2={620} y2={980} stroke={PLAT} strokeWidth={10} />
    <Dash x1={260} y1={980} x2={760} y2={700} p={sp(f, 8, 32)} color={C.amber} />
    <Dash x1={620} y1={980} x2={760} y2={700} p={sp(f, 14, 38)} color={C.amber} />
    <HatHero x={180} y={1250} s={2} walk={f * 0.12} hat="pirate" />
  </g>
);
const P17: Panel = ({f}) => {
  const pts = [[460, 520], [640, 600], [430, 700], [650, 790], [440, 880], [660, 970], [450, 1060], [640, 1150]];
  const n = Math.floor(sp(f, 2, 60) * (pts.length - 2));
  return (
    <g>
      <Head a="Nối nhiều tam giác" b="thành một chuỗi" />
      {Array.from({length: n}).map((_, i) => (
        <path key={i} d={`M ${pts[i][0]} ${pts[i][1]} L ${pts[i + 1][0]} ${pts[i + 1][1]} L ${pts[i + 2][0]} ${pts[i + 2][1]} Z`} fill={C.amber} fillOpacity={0.12} stroke={C.amber} strokeWidth={4} strokeLinejoin="round" />
      ))}
      <Dot x={460} y={520} label="Đăng-kéc" lx={-30} />
      <Dot x={640} y={1150} label="Bác-xê-lô-na" o={sp(f, 50, 62)} />
    </g>
  );
};

// --- Cảnh 5: tính ---
const P18: Panel = ({f}) => (
  <g>
    <Head a="Chuỗi dài khoảng 1 000 km" b="≈ 1 phần 10 quãng" />
    <Earth x={420} y={820} r={280} />
    <path d={arcPath(420, 820, 280, -90, 0)} fill="none" stroke={C.cream} strokeWidth={6} strokeDasharray="10 10" />
    <path d={arcPath(420, 820, 280, -54, -45)} fill="none" stroke={RED} strokeWidth={16} strokeLinecap="round" opacity={sp(f, 6, 20)} />
    <Tag x={850} y={600} color={RED} size={44} o={sp(f, 14, 28)}>1 000 km</Tag>
    <Tag x={850} y={1080} color={C.amber} size={44} o={sp(f, 28, 42)}>≈ 1/10</Tag>
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Cả quãng cực – xích đạo" />
    <Calc f={f} y={780} step={170} lines={[{t: '1 000 × 10', at: 6, size: 120}]} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="pirate" />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Cả quãng cực – xích đạo" />
    <Calc f={f} y={780} step={170} lines={[{t: '1 000 × 10', at: 0, size: 120}, {t: '= 10 000 km', at: 4, size: 120, color: C.amber}]} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.15} hat="pirate" />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Đổi ra mét" />
    <Calc f={f} y={780} step={170} lines={[{t: '10 000 km', at: 4, size: 110}, {t: '= 10 000 000 m', at: 20, size: 110, color: C.amber}]} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.15} hat="pirate" />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Chia thành 10 triệu phần" b="mỗi phần đúng 1 mét" />
    <rect x={110} y={720} width={860} height={60} fill={GOLD} stroke={C.cream} strokeWidth={4} />
    {Array.from({length: 41}).map((_, i) => (
      <line key={i} x1={110 + i * 21.5} y1={720} x2={110 + i * 21.5} y2={780} stroke="#2a2018" strokeWidth={2} opacity={sp(f, 6, 30)} />
    ))}
    <Big x={540} y={1000} size={150} color={C.amber} o={sp(f, 24, 40)}>1 m</Big>
    <HatHero x={540} y={1250} s={2} walk={f * 0.2} cheer={sp(f, 30, 50)} hat="pirate" />
  </g>
);

// --- Cảnh 6: thanh bạch kim và sai số ---
const P23: Panel = ({f}) => (
  <g>
    <Head a="Năm 1799" b="một thanh bạch kim" />
    <rect x={140} y={lerp(640, 780, sp(f, 4, 26))} width={800} height={60} rx={8} fill={PLAT} stroke={C.cream} strokeWidth={5} />
    <Tag x={540} y={940} color={C.amber} size={52} o={sp(f, 20, 34)}>mét mẫu</Tag>
    <HatHero x={540} y={1250} s={2} walk={f * 0.15} cheer={sp(f, 24, 44)} hat="pirate" />
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Nhân 4 quãng cực – xích đạo" b="được một vòng qua hai cực" />
    <Earth x={540} y={840} r={300} />
    {[0, 1, 2, 3].map((i) => (
      <path key={i} d={arcPath(540, 840, 300, -90 + i * 90, -90 + i * 90 + 90 * sp(f, 4 + i * 10, 14 + i * 10))} fill="none" stroke={[RED, C.amber, RED, C.amber][i]} strokeWidth={12} strokeLinecap="round" opacity={f > 4 + i * 10 ? 1 : 0} />
    ))}
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Vòng quanh Trái Đất qua hai cực" />
    <Calc f={f} y={780} step={170} lines={[{t: '10 000 × 4', at: 4, size: 120}, {t: '= 40 000 km', at: 22, size: 120, color: C.amber}]} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.15} hat="pirate" />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Ngày nay đo được" b="khoảng 40 008 km" />
    <Bar x={110} y={700} w={860} color={GOLD} p={sp(f, 4, 24) * 0.9998} label="định nghĩa: 40 000" />
    <Bar x={110} y={840} w={860} color={C.amber} p={sp(f, 10, 30)} label="đo thật: 40 008" />
    <Big x={540} y={1080} size={120} color={C.amber} o={sp(f, 24, 40)}>40 008 km</Big>
  </g>
);
const P27: Panel = ({f}) => (
  <g>
    <Head a="Thanh mét đầu tiên" b="ngắn hơn khoảng 0,2 mm" />
    <rect x={140} y={760} width={740} height={60} rx={8} fill={PLAT} stroke={C.cream} strokeWidth={5} />
    <line x1={900} y1={720} x2={900} y2={860} stroke={RED} strokeWidth={5} strokeDasharray="10 8" opacity={sp(f, 10, 24)} />
    <Tag x={900} y={690} color={RED} size={40} o={sp(f, 14, 28)}>đúng định nghĩa</Tag>
    <Big x={540} y={1060} size={140} color={C.amber} o={sp(f, 22, 38)}>0,2 mm</Big>
  </g>
);
const P28: Panel = ({f}) => (
  <g>
    <Head a="Chỉ bằng độ dày" b="hai tờ giấy" />
    <rect x={300} y={820} width={480} height={26} rx={3} fill="#f4efe2" stroke="#8a8270" strokeWidth={2} opacity={sp(f, 4, 14)} />
    <rect x={300} y={780} width={480} height={26} rx={3} fill="#f4efe2" stroke="#8a8270" strokeWidth={2} opacity={sp(f, 10, 20)} />
    <Tag x={540} y={960} color={C.amber} size={48} o={sp(f, 24, 38)}>2 tờ ≈ 0,2 mm</Tag>
    <HatHero x={170} y={1250} s={2} walk={f * 0.12} hat="pirate" />
  </g>
);

// --- Cảnh 7: kết ---
const P29: Panel = ({f}) => (
  <g>
    <Head a="Người ta giữ nguyên" b="độ dài ấy" />
    <rect x={140} y={760} width={800} height={60} rx={8} fill={PLAT} stroke={C.cream} strokeWidth={5} />
    <Tag x={540} y={930} color="#6fd18f" size={54} o={sp(f, 14, 30)}>✓ giữ nguyên</Tag>
    <HatHero x={540} y={1250} s={2} walk={f * 0.15} hat="pirate" />
  </g>
);
const P30: Panel = ({f}) => {
  const t = (f % 50) / 50;
  return (
    <g>
      <Head a="Năm 1983" b="định nghĩa lại bằng ánh sáng" />
      <Ruler x={140} y={780} w={800} />
      <line x1={140} y1={720} x2={lerp(140, 940, t)} y2={720} stroke={BEAM} strokeWidth={10} strokeLinecap="round" />
      <circle cx={lerp(140, 940, t)} cy={720} r={12} fill="#ffffff" />
      <Tag x={540} y={960} color={C.cream} size={44} o={sp(f, 20, 34)}>vẫn giữ độ dài cũ</Tag>
      <HatHero x={540} y={1250} s={2} walk={f * 0.15} hat="pirate" />
    </g>
  );
};
const P31: Panel = ({f}) => (
  <g>
    <Head a="1 mét = 1 phần 10 triệu" b="quãng cực – xích đạo" />
    <Earth x={420} y={800} r={240} />
    <path d={arcPath(420, 800, 240, -90, 0)} fill="none" stroke={RED} strokeWidth={12} strokeLinecap="round" />
    <Ruler x={700} y={1050} w={260} />
    <HatHero x={560} y={1250} s={2} walk={f * 0.25} cheer={sp(f, 16, 40)} hat="pirate" />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30, P31];
