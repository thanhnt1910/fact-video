import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const SUN = '#ffd24d';
const EARTH = '#4a90d9';
const RED = '#e0613b';
const VIOLET = '#b9a5e8';

const Hero2: React.FC<{f: number; x?: number; cheer?: number}> = ({f, x = 170, cheer = 0}) => <HatHero x={x} y={1250} s={2} walk={f * 0.13} cheer={cheer} hat="gear" />;

const SunIcon: React.FC<{x: number; y: number; r?: number; o?: number}> = ({x, y, r = 40, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill={SUN} stroke={C.cream} strokeWidth={5} />
    {Array.from({length: 8}).map((_, i) => (
      <line key={i} x1={x + (r + 10) * Math.cos((i * Math.PI) / 4)} y1={y + (r + 10) * Math.sin((i * Math.PI) / 4)} x2={x + (r + 28) * Math.cos((i * Math.PI) / 4)} y2={y + (r + 28) * Math.sin((i * Math.PI) / 4)} stroke={SUN} strokeWidth={6} strokeLinecap="round" />
    ))}
  </g>
);
const Orbit: React.FC<{cx: number; cy: number; r: number; prog: number; gap?: number}> = ({cx, cy, r, prog, gap = 0}) => {
  const a = -Math.PI / 2 + prog * 2 * Math.PI;
  return (
    <g>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={C.cream} strokeWidth={5} strokeDasharray="12 12" opacity={0.6} />
      <SunIcon x={cx} y={cy} r={34} />
      {gap > 0 && <path d={`M ${cx} ${cy - r} A ${r} ${r} 0 0 1 ${cx + r * Math.sin(gap * 2 * Math.PI)} ${cy - r * Math.cos(gap * 2 * Math.PI)}`} fill="none" stroke={RED} strokeWidth={14} strokeLinecap="round" />}
      <circle cx={cx + r * Math.cos(a)} cy={cy + r * Math.sin(a)} r={22} fill={EARTH} stroke={C.cream} strokeWidth={5} />
    </g>
  );
};
const Cal: React.FC<{x: number; y: number; w?: number; title: string; cells: string[]; cross?: number[]; hi?: number[]; o?: number}> = ({x, y, w = 560, title, cells, cross = [], hi = [], o = 1}) => {
  const cw = w / 7;
  return (
    <g opacity={clamp01(o)}>
      <rect x={x} y={y} width={w} height={90 + Math.ceil(cells.length / 7) * 84 + 30} rx={14} fill="#efe3c8" stroke={C.cream} strokeWidth={5} />
      <rect x={x} y={y} width={w} height={80} rx={14} fill={RED} />
      <text x={x + w / 2} y={y + 56} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={40} fill={C.cream}>{title}</text>
      {cells.map((c, i) => {
        const cx = x + (i % 7) * cw + cw / 2;
        const cy = y + 140 + Math.floor(i / 7) * 84;
        return (
          <g key={i}>
            {hi.includes(i) && <circle cx={cx} cy={cy - 12} r={30} fill={SUN} opacity={0.8} />}
            <text x={cx} y={cy} textAnchor="middle" fontFamily="BeVN" fontWeight={700} fontSize={34} fill="#2a2018">{c}</text>
            {cross.includes(i) && <line x1={cx - 22} y1={cy - 34} x2={cx + 22} y2={cy + 8} stroke={RED} strokeWidth={6} strokeLinecap="round" />}
          </g>
        );
      })}
    </g>
  );
};
const TL: React.FC<{y: number; x1?: number; x2?: number; p?: number; color?: string}> = ({y, x1 = 140, x2 = 940, p = 1, color = C.cream}) => (
  <line x1={x1} y1={y} x2={lerp(x1, x2, clamp01(p))} y2={y} stroke={color} strokeWidth={6} strokeLinecap="round" />
);

const OX = 540;
const OY = 830;
const OR = 280;

// --- Cảnh 1 ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Vì sao cứ 4 năm" b="lịch lại thêm một ngày?" />
    <Cal x={260} y={500} w={560} title="Tháng 2" cells={Array.from({length: 29}, (_, i) => String(i + 1))} hi={[28]} o={sp(f, 2, 14)} />
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Một năm không phải" b="365 ngày tròn" />
    <Big x={540} y={820} size={190} color={C.cream} o={sp(f, 2, 14)}>365</Big>
    <Tag x={540} y={960} color={RED} size={60} o={sp(f, 12, 26)}>không tròn!</Tag>
    <Hero2 f={f} />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Mỗi vòng quanh Mặt Trời" b="còn lẻ gần 1 phần 4 ngày" />
    <Orbit cx={OX} cy={OY} r={OR} prog={sp(f, 2, 34)} gap={sp(f, 30, 44) * 0.08} />
    <Tag x={820} y={560} color={RED} size={44} o={sp(f, 34, 46)}>lẻ ¼ ngày</Tag>
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Người xưa đo" b="phần lẻ ấy bằng cách nào?" />
    <Orbit cx={OX} cy={OY} r={OR} prog={0} gap={0.08} />
    <Big x={830} y={600} size={150} color={C.amber} o={0.9 * sp(f, 8, 24)}>?</Big>
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 2: hạ chí ---
const P4: Panel = ({f}) => (
  <g>
    <Head a="Cần một dấu mốc của năm" b="ngày hạ chí" />
    <path d="M 120 1000 A 420 420 0 0 1 960 1000" fill="none" stroke={VIOLET} strokeWidth={5} strokeDasharray="12 12" opacity={0.7} />
    <SunIcon x={540} y={560} r={50} o={sp(f, 6, 22)} />
    <line x1={60} y1={1000} x2={1020} y2={1000} stroke={C.cream} strokeWidth={5} />
    <Tag x={540} y={1110} color={C.amber} size={56} o={sp(f, 16, 30)}>hạ chí</Tag>
    <Hero2 f={f} />
  </g>
);
const P5: Panel = ({f}) => {
  const k = sp(f, 4, 36);
  const ang = lerp(Math.PI, Math.PI / 2, k);
  return (
    <g>
      <Head a="Mặt Trời lên cao nhất" b="giữa trưa, ở nơi như Hy Lạp" />
      <path d="M 120 1000 A 420 420 0 0 1 960 1000" fill="none" stroke={VIOLET} strokeWidth={5} strokeDasharray="12 12" opacity={0.7} />
      <SunIcon x={540 + 420 * Math.cos(ang)} y={1000 - 420 * Math.sin(ang)} r={50} />
      <line x1={60} y1={1000} x2={1020} y2={1000} stroke={C.cream} strokeWidth={5} />
      <Tag x={540} y={1110} color={C.cream} size={46} o={sp(f, 26, 40)}>điểm cao nhất lúc giữa trưa</Tag>
    </g>
  );
};
const P6: Panel = ({f}) => {
  const n = Math.floor(sp(f, 8, 50) * 365);
  return (
    <g>
      <Head a="Ghi ngày hạ chí" b="rồi đếm số ngày tới năm sau" />
      <TL y={800} p={sp(f, 2, 50)} />
      <SunIcon x={140} y={720} r={34} />
      <SunIcon x={940} y={720} r={34} o={sp(f, 46, 58)} />
      <Big x={540} y={960} size={150} color={C.amber}>{String(n)}</Big>
      <Tag x={540} y={1050} color={C.cream} size={44}>ngày</Tag>
    </g>
  );
};
const P7: Panel = ({f}) => (
  <g>
    <Head a="Mỗi lần sai vài giờ" b="chỉ đếm một năm chưa đủ" />
    <line x1={140} y1={820} x2={940} y2={820} stroke={C.cream} strokeWidth={6} />
    <rect x={460} y={760} width={160} height={120} fill={SUN} fillOpacity={0.3} stroke={SUN} strokeWidth={4} strokeDasharray="10 8" opacity={sp(f, 6, 20)} />
    <SunIcon x={540} y={740} r={30} />
    <Tag x={540} y={960} color={RED} size={50} o={sp(f, 14, 28)}>± vài giờ</Tag>
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 3: mẹo ---
const P8: Panel = ({f}) => (
  <g>
    <Head a="Đo hai hạ chí cách nhau xa" b="rồi chia cho số năm" />
    <TL y={820} p={sp(f, 2, 24)} />
    <SunIcon x={140} y={740} r={30} />
    <SunIcon x={940} y={740} r={30} o={sp(f, 18, 32)} />
    <Arrow x1={160} y1={960} x2={920} y2={960} p={sp(f, 18, 38)} color={C.amber} />
    <Tag x={540} y={1040} color={C.amber} size={50} o={sp(f, 26, 40)}>cách nhau thật xa</Tag>
    <Hero2 f={f} />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Như đo tờ giấy" b="đo chồng 100 tờ rồi chia 100" />
    {Array.from({length: 20}).map((_, i) => (
      <rect key={i} x={260} y={900 - i * 14 * sp(f, 2, 22)} width={560} height={12} fill="#efe3c8" stroke="#8a7a62" strokeWidth={2} />
    ))}
    <Big x={600} y={1010} size={80} color={C.amber} o={sp(f, 20, 36)}>chồng 100 tờ ÷ 100</Big>
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 4: Hip-pa-khốt ---
const P10: Panel = ({f}) => (
  <g>
    <Head a="Hip-pa-khốt, Hy Lạp" b="thế kỷ thứ 2 trước Công nguyên" />
    <SunIcon x={700} y={640} r={50} o={sp(f, 4, 18)} />
    <path d="M 120 1000 L 300 880 L 460 960 L 640 850 L 960 1000 Z" fill="#3b3158" stroke={C.cream} strokeWidth={5} opacity={sp(f, 2, 14)} />
    <Tag x={540} y={1130} color={C.cream} size={46} o={sp(f, 14, 28)}>nhà thiên văn Hy Lạp</Tag>
    <HatHero x={330} y={900} s={1.4} walk={f * 0.15} hat="gear" />
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="So hạ chí ông quan sát" b="với hạ chí ghi từ gần 300 năm trước" />
    <rect x={150} y={600} width={340} height={380} rx={14} fill="#d8c8a0" stroke={C.cream} strokeWidth={5} opacity={sp(f, 2, 14)} />
    <rect x={590} y={600} width={340} height={380} rx={14} fill="#efe3c8" stroke={C.cream} strokeWidth={5} opacity={sp(f, 10, 22)} />
    <Tag x={320} y={1060} color={C.cream} size={42} o={sp(f, 12, 24)}>ghi từ xưa</Tag>
    <Tag x={760} y={1060} color={C.amber} size={42} o={sp(f, 18, 30)}>ông quan sát</Tag>
    <Arrow x1={500} y1={790} x2={580} y2={790} p={sp(f, 16, 28)} />
    <Hero2 f={f} />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Giữa hai hạ chí ấy" />
    <Calc f={f} y={740} step={170} lines={[{t: '297 năm', at: 2, size: 130}, {t: '108 478 ngày', at: 14, size: 130, color: C.amber}]} />
    <Hero2 f={f} />
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Chia số ngày cho số năm" />
    <Calc f={f} y={800} step={170} lines={[{t: '108 478 ÷ 297', at: 4, size: 120, color: C.amber}]} />
    <Hero2 f={f} />
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Số ngày mỗi năm" />
    <Calc f={f} y={800} step={170} lines={[{t: '108 478 ÷ 297', at: 0, size: 90}, {t: '≈ 365,246', at: 6, size: 140, color: C.amber}]} />
    <Hero2 f={f} cheer={sp(f, 12, 28)} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Số đo hiện đại" />
    <Big x={540} y={820} size={150} color={C.amber} o={sp(f, 4, 18)}>365,2422</Big>
    <Tag x={540} y={930} color={C.cream} size={50} o={sp(f, 14, 28)}>ngày</Tag>
    <Hero2 f={f} />
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Ông chỉ lệch khoảng 6 phút" b="mỗi năm, không có máy móc" />
    <circle cx={540} cy={800} r={220} fill="#efe3c8" stroke={C.cream} strokeWidth={8} />
    <path d={`M 540 800 L 540 600 A 200 200 0 0 1 ${540 + 200 * Math.sin(lerp(0, Math.PI / 5, sp(f, 6, 24)))} ${800 - 200 * Math.cos(lerp(0, Math.PI / 5, sp(f, 6, 24)))} Z`} fill={RED} fillOpacity={0.7} />
    <Big x={540} y={1130} size={110} color={C.amber} o={sp(f, 16, 30)}>≈ 6 phút</Big>
  </g>
);
// --- Cảnh 5: lịch Giu-li-an ---
const P17: Panel = ({f}) => (
  <g>
    <Head a="Lịch Giu-li-an, từ năm 45 TCN" b="cứ 4 năm thêm 1 ngày" />
    {[365, 365, 365, 366].map((d, i) => (
      <g key={i} opacity={sp(f, 2 + i * 7, 14 + i * 7)}>
        <rect x={100 + i * 220} y={700} width={190} height={190} rx={18} fill={i === 3 ? SUN : '#efe3c8'} fillOpacity={i === 3 ? 0.9 : 1} stroke={C.cream} strokeWidth={5} />
        <text x={195 + i * 220} y={810} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={64} fill="#2a2018">{d}</text>
        <text x={195 + i * 220} y={940} textAnchor="middle" fontFamily="BeVN" fontWeight={700} fontSize={32} fill={C.cream}>năm {i + 1}</text>
      </g>
    ))}
    <Hero2 f={f} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Năm trung bình" />
    <Calc f={f} y={780} step={170} lines={[{t: '365 ngày + ¼ ngày', at: 2, size: 96}, {t: '= 365,25', at: 14, size: 150, color: C.amber}]} />
    <Hero2 f={f} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Dài hơn năm thật" b="khoảng 0,0078 ngày mỗi năm" />
    <Calc f={f} y={760} step={140} lines={[{t: '365,25', at: 2, size: 100}, {t: '365,2422', at: 10, size: 100, color: C.cream}, {t: 'lệch 0,0078', at: 20, size: 110, color: RED}]} />
    <Hero2 f={f} />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Từ năm 325 đến 1582" b="là 1 257 năm" />
    <TL y={800} p={sp(f, 2, 30)} />
    <Big x={140} y={730} size={72} color={C.cream}>325</Big>
    <Big x={940} y={730} size={72} color={C.cream} o={sp(f, 24, 36)}>1582</Big>
    <Big x={540} y={980} size={130} color={C.amber} o={sp(f, 20, 36)}>1 257 năm</Big>
    <Hero2 f={f} />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Lệch tích lũy" />
    <Calc f={f} y={780} step={170} lines={[{t: '1 257 × 0,0078', at: 2, size: 100}, {t: '≈ gần 10 ngày', at: 14, size: 130, color: RED}]} />
    <Hero2 f={f} />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Năm 1582" b="Gờ-rê-goa 13 bỏ 10 ngày" />
    <Big x={540} y={820} size={190} color={RED} o={sp(f, 4, 20)}>− 10 ngày</Big>
    <Hero2 f={f} />
  </g>
);
const P23: Panel = ({f}) => (
  <g>
    <Head a="Sau 4 tháng 10" b="là 15 tháng 10" />
    <Cal x={260} y={520} w={560} title="Tháng 10 / 1582" cells={['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']} cross={[4, 5, 6, 7, 8, 9, 10, 11, 12, 13].filter((_, i) => sp(f, 6 + i * 2, 12 + i * 2) > 0.5)} hi={[3, 14]} />
  </g>
);
// --- Cảnh 6: luật nhuận ---
const P24: Panel = ({f}) => (
  <g>
    <Head a="Luật nhuận mới" />
    <Big x={540} y={680} size={70} color={C.cream} o={sp(f, 2, 14)}>chia hết cho 4 → nhuận</Big>
    <Big x={540} y={820} size={70} color={C.amber} o={sp(f, 12, 26)}>trừ năm cuối thế kỷ</Big>
    <Big x={540} y={920} size={70} color={C.amber} o={sp(f, 14, 28)}>không chia hết cho 400</Big>
    <Hero2 f={f} />
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="1700, 1800, 1900 không nhuận" b="còn 2000 thì nhuận" />
    {[['1700', RED, '✕'], ['1800', RED, '✕'], ['1900', RED, '✕'], ['2000', '#58c27d', '✓']].map(([y, c, m], i) => (
      <g key={y} opacity={sp(f, 2 + i * 7, 14 + i * 7)}>
        <rect x={100 + i * 220} y={700} width={190} height={190} rx={18} fill="#efe3c8" stroke={c} strokeWidth={8} />
        <text x={195 + i * 220} y={800} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={56} fill="#2a2018">{y}</text>
        <text x={195 + i * 220} y={870} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={60} fill={c}>{m}</text>
      </g>
    ))}
    <Hero2 f={f} />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Cứ 400 năm" b="chỉ có 97 năm nhuận" />
    <rect x={100} y={760} width={880} height={90} rx={12} fill="#efe3c8" stroke={C.cream} strokeWidth={5} />
    <rect x={100} y={760} width={880 * 0.2425 * sp(f, 4, 30)} height={90} rx={12} fill={SUN} />
    <Tag x={310} y={920} color={C.amber} size={46} o={sp(f, 20, 34)}>97 nhuận</Tag>
    <Tag x={700} y={920} color={C.cream} size={46} o={sp(f, 24, 38)}>303 thường</Tag>
    <Hero2 f={f} />
  </g>
);
const P27: Panel = ({f}) => (
  <g>
    <Head a="Số ngày của 400 năm" />
    <Calc f={f} y={780} step={160} lines={[{t: '400 × 365 + 97', at: 2, size: 100}, {t: '= 146 097 ngày', at: 14, size: 120, color: C.amber}]} />
    <Hero2 f={f} />
  </g>
);
const P28: Panel = ({f}) => (
  <g>
    <Head a="Chia cho 400 năm" />
    <Calc f={f} y={780} step={160} lines={[{t: '146 097 ÷ 400', at: 2, size: 100}, {t: '= 365,2425', at: 14, size: 130, color: C.amber}]} />
    <Hero2 f={f} cheer={sp(f, 18, 34)} />
  </g>
);
const P29: Panel = ({f}) => (
  <g>
    <Head a="Gần sát năm thật" b="rất nhiều thế kỷ mới lệch 1 ngày" />
    <TL y={820} p={sp(f, 2, 40)} color={C.amber} />
    <SunIcon x={140} y={740} r={30} />
    <Tag x={540} y={940} color={C.cream} size={48} o={sp(f, 20, 34)}>nhiều thế kỷ → lệch 1 ngày</Tag>
    <Hero2 f={f} />
  </g>
);
const P30: Panel = ({f}) => (
  <g>
    <Head a="Cứ 4 năm thêm 1 ngày" b="vì năm dài hơn 365 ngày gần ¼" />
    <Orbit cx={OX} cy={820} r={250} prog={sp(f, 2, 40)} gap={0.07} />
    <Hero2 f={f} cheer={sp(f, 10, 28)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30];
