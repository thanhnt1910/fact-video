import React from 'react';
import {Arrow, Bar, Big, C, Calc, Dash, Head, HatHero, Lab, Panel, Tag, clamp01, lerp, seg, sp} from '../khoahoc/kit';

const BRASS = '#d6a83a';

const Pend: React.FC<{px: number; py: number; L: number; f: number; amp?: number; P?: number; ph?: number; r?: number; color?: string; o?: number}> = ({px, py, L, f, amp = 24, P = 60, ph = 0, r = 30, color = BRASS, o = 1}) => {
  const a = amp * Math.sin((f / P) * Math.PI * 2 + ph);
  return (
    <g opacity={clamp01(o)}>
      <g transform={`translate(${px} ${py}) rotate(${a})`}>
        <line x1={0} y1={0} x2={0} y2={L} stroke={C.cream} strokeWidth={5} />
        <circle cx={0} cy={L + r} r={r} fill={color} stroke={C.cream} strokeWidth={5} />
      </g>
      <rect x={px - 60} y={py - 16} width={120} height={16} rx={6} fill="#8a6a3a" stroke={C.cream} strokeWidth={4} />
    </g>
  );
};
const Face: React.FC<{x: number; y: number; r?: number; h: number; m: number; o?: number}> = ({x, y, r = 130, h, m, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill="#f4e9d0" stroke="#8a6a3a" strokeWidth={10} />
    {Array.from({length: 12}, (_, i) => <line key={i} x1={x + (r - 12) * Math.sin((i * Math.PI) / 6)} y1={y - (r - 12) * Math.cos((i * Math.PI) / 6)} x2={x + (r - 28) * Math.sin((i * Math.PI) / 6)} y2={y - (r - 28) * Math.cos((i * Math.PI) / 6)} stroke="#4a3a28" strokeWidth={5} />)}
    <line x1={x} y1={y} x2={x + r * 0.5 * Math.sin(h)} y2={y - r * 0.5 * Math.cos(h)} stroke="#2b2118" strokeWidth={9} strokeLinecap="round" />
    <line x1={x} y1={y} x2={x + r * 0.78 * Math.sin(m)} y2={y - r * 0.78 * Math.cos(m)} stroke="#2b2118" strokeWidth={6} strokeLinecap="round" />
    <circle cx={x} cy={y} r={9} fill="#c0392b" />
  </g>
);

// --- Cảnh 1 ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Đồng hồ lò xo thời xưa" b="chạy lệch tới 15 phút mỗi ngày" />
    <Face x={540} y={820} r={190} h={0.6 + f * 0.004} m={f * 0.05 + Math.sin(f * 0.2) * 0.3} />
    <Big x={540} y={1130} size={110} color={C.amber} o={sp(f, 20, 36)}>lệch 15 phút</Big>
    <Tag x={540} y={1230} color={C.cream} size={40} o={sp(f, 36, 50)}>mỗi ngày</Tag>
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Chỉ cần một sợi dây và một quả nặng" b="độ lệch giảm đi 60 lần" />
    <Pend px={300} py={560} L={380} f={f} />
    <Big x={730} y={760} size={160} color={C.amber} o={sp(f, 16, 32)}>÷ 60</Big>
    <Tag x={730} y={870} color={C.cream} size={42} o={sp(f, 28, 42)}>độ lệch</Tag>
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Bí mật đơn giản:" b="quả lắc đung đưa đều như nhịp tim" />
    <Pend px={540} py={520} L={430} f={f} amp={28} r={44} />
    <Tag x={240} y={1100} color={C.amber} size={42} o={Math.max(0, Math.sin((f / 60) * Math.PI * 2))}>tích</Tag>
    <Tag x={840} y={1100} color={C.amber} size={42} o={Math.max(0, -Math.sin((f / 60) * Math.PI * 2))}>tắc</Tag>
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Vì sao quả lắc" b="lại đều đến thế?" />
    <Pend px={400} py={520} L={430} f={f} amp={28} r={44} />
    <Big x={780} y={880} size={200} color={C.amber} o={0.9 * sp(f, 10, 26)}>?</Big>
  </g>
);

// --- Cảnh 2 ---
const P4: Panel = ({f}) => (
  <g>
    <Head a="Ga-li-lê thấy: 2 con lắc dài bằng nhau" b="mỗi lượt đưa mất thời gian như nhau" />
    <Pend px={320} py={520} L={360} f={f} r={36} />
    <Pend px={760} py={520} L={360} f={f} r={36} color="#8fd1ff" />
    <Dash x1={150} y1={1000} x2={930} y2={1000} p={sp(f, 10, 40)} color={C.dim} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.1} hat="scholar" />
    <Tag x={540} y={968} color={C.amber} size={42} o={sp(f, 30, 46)}>cùng nhịp</Tag>
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Thời gian ấy chỉ phụ thuộc" b="độ dài dây, không phụ thuộc quả nặng" />
    <Pend px={320} py={520} L={360} f={f} r={22} />
    <Pend px={760} py={520} L={360} f={f} r={58} color="#8fd1ff" />
    <Tag x={320} y={1030} color={C.cream} size={40} o={sp(f, 8, 22)}>quả nhẹ</Tag>
    <Tag x={760} y={1060} color={C.cream} size={40} o={sp(f, 8, 22)}>quả nặng</Tag>
    <Tag x={540} y={1180} color={C.amber} size={44} o={sp(f, 30, 46)}>vẫn cùng nhịp</Tag>
  </g>
);
const Swing: React.FC<{x: number; f: number; big: boolean}> = ({x, f, big}) => {
  const a = 22 * Math.sin((f / 70) * Math.PI * 2);
  return (
    <g transform={`translate(${x} 560) rotate(${a})`} stroke={C.cream} strokeWidth={5} strokeLinecap="round">
      <line x1={-50} y1={0} x2={-50} y2={380} />
      <line x1={50} y1={0} x2={50} y2={380} />
      <line x1={-70} y1={380} x2={70} y2={380} strokeWidth={10} stroke="#b08a50" />
      <circle cx={0} cy={big ? 270 : 310} r={big ? 26 : 18} fill="#2b2118" />
      <line x1={0} y1={big ? 296 : 328} x2={0} y2={375} />
    </g>
  );
};
const P6: Panel = ({f}) => (
  <g>
    <Head a="Ví dụ: trên xích đu" b="bé hay người lớn đều cùng nhịp" />
    <line x1={140} y1={540} x2={940} y2={540} stroke="#b08a50" strokeWidth={14} strokeLinecap="round" />
    <Swing x={340} f={f} big={false} />
    <Swing x={740} f={f} big />
    <Tag x={340} y={1060} color={C.cream} size={40}>em bé</Tag>
    <Tag x={740} y={1060} color={C.cream} size={40}>người lớn</Tag>
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Muốn đo thời gian" b="chỉ cần đếm số lần đung đưa" />
    <Pend px={300} py={520} L={400} f={f} amp={28} r={40} />
    {Array.from({length: 9}, (_, i) => <Big key={i} x={600 + (i % 3) * 130} y={720 + Math.floor(i / 3) * 140} size={96} color={C.amber} o={sp(f, 14 + i * 12, 22 + i * 12)}>{String(i + 1)}</Big>)}
  </g>
);

// --- Cảnh 3 ---
const Clock: React.FC<{f: number; o?: number}> = ({f, o = 1}) => (
  <g opacity={clamp01(o)}>
    <rect x={340} y={480} width={400} height={760} rx={40} fill="#6a4a2a" stroke={C.cream} strokeWidth={8} />
    <Face x={540} y={680} r={130} h={0.3} m={f * 0.03} />
    <rect x={400} y={860} width={280} height={330} rx={20} fill="#2a1d12" />
    <Pend px={540} py={880} L={200} f={f} amp={22} r={34} />
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Năm 1657, Hây-ghen" b="được cấp bằng đồng hồ quả lắc" />
    <Clock f={f} o={sp(f, 6, 22)} />
    <Big x={880} y={820} size={100} color={C.amber} o={sp(f, 20, 36)}>1657</Big>
    <HatHero x={900} y={1250} s={2} walk={f * 0.2} hat="gear" />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Quả lắc điều khiển" b="nhịp chạy của kim đồng hồ" />
    <Clock f={f} />
    <Arrow x1={720} y1={1000} x2={720} y2={820} p={sp(f, 14, 40)} />
    <Tag x={850} y={900} color={C.amber} size={40} o={sp(f, 30, 46)}>điều khiển</Tag>
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Độ lệch giảm từ khoảng 15 phút" b="xuống còn khoảng 15 giây mỗi ngày" />
    <Lab x={110} y={700} size={40} anchor="start" color={C.cream}>trước: 15 phút</Lab>
    <Bar x={110} y={730} w={860} color="#e0613b" p={sp(f, 6, 30)} />
    <Lab x={110} y={900} size={40} anchor="start" color={C.cream}>sau: 15 giây</Lab>
    <Bar x={110} y={930} w={860} color="#6fd18f" p={sp(f, 24, 48) / 60} />
  </g>
);

// --- Cảnh 4 ---
const P11: Panel = ({f}) => (
  <g>
    <Head a="Ta tính thử" b="đổi 15 phút ra giây" />
    <Calc f={f} y={720} lines={[{t: '15 × 60', at: 6}, {t: '= 900 giây', at: 26, color: C.amber, size: 120}]} />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Rồi so với 15 giây" />
    <Calc f={f} y={720} lines={[{t: '900 ÷ 15', at: 6}, {t: '= 60 lần', at: 26, color: C.amber, size: 130}]} />
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Đồng hồ quả lắc" b="chính xác hơn khoảng 60 lần" />
    <Big x={540} y={860} size={230} color={C.amber} o={sp(f, 6, 24)}>60 lần</Big>
    <Clock f={f} o={0} />
    <HatHero x={200} y={1250} s={2} walk={f * 0.25} hat="gear" cheer={sp(f, 20, 40)} />
  </g>
);

// --- Cảnh 5 ---
const P14: Panel = ({f}) => (
  <g>
    <Head a="Công thức thật của quả lắc" />
    <Lab x={540} y={640} size={52} color={C.cream} o={sp(f, 6, 18)}>thời gian một lượt</Lab>
    <Big x={540} y={790} size={88} color={C.amber} o={sp(f, 16, 30)}>= 2 × π × √(độ dài ÷ g)</Big>
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="π là số khoảng 3,14" b="g là lực hút của Trái Đất" />
    <rect x={110} y={640} width={400} height={220} rx={24} fill="#2a1d12" stroke={C.cream} strokeWidth={5} opacity={sp(f, 6, 20)} />
    <Big x={310} y={770} size={90} o={sp(f, 8, 22)}>π ≈ 3,14</Big>
    <rect x={570} y={640} width={400} height={220} rx={24} fill="#2a1d12" stroke={C.cream} strokeWidth={5} opacity={sp(f, 20, 34)} />
    <Big x={770} y={750} size={90} o={sp(f, 22, 36)}>g ≈ 9,8</Big>
    <Lab x={770} y={820} size={32} color={C.cream} o={sp(f, 28, 42)}>lực hút Trái Đất</Lab>
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Thử với sợi dây" b="dài 1 mét" />
    <Pend px={400} py={520} L={460} f={f} amp={20} r={36} />
    <line x1={250} y1={520} x2={250} y2={980} stroke={C.amber} strokeWidth={6} opacity={sp(f, 10, 30)} />
    <Big x={190} y={760} size={64} color={C.amber} anchor="end" o={sp(f, 20, 36)}>1 m</Big>
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Bước 1: chia" />
    <Calc f={f} y={720} lines={[{t: '1 ÷ 9,8', at: 6}, {t: '≈ 0,1', at: 26, color: C.amber, size: 130}]} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Bước 2: lấy căn bậc hai" />
    <Calc f={f} y={720} lines={[{t: '√0,1', at: 6}, {t: '≈ 0,32', at: 26, color: C.amber, size: 130}]} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Bước 3: nhân với 2π" />
    <Calc f={f} y={640} lines={[{t: '0,32 × 6,28', at: 6}, {t: '≈ 2 giây', at: 26, color: C.amber, size: 130}]} />
    <Pend px={540} py={940} L={190} f={f} amp={30} P={120} r={26} o={sp(f, 36, 52)} />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Quả lắc dài gần 1 mét" b="cho nhịp tích tắc đúng 1 giây" />
    <Pend px={540} py={500} L={440} f={f} amp={28} P={60} r={40} />
    <Tag x={260} y={1130} color={C.amber} size={46} o={Math.max(0, Math.sin((f / 60) * Math.PI * 2))}>tích</Tag>
    <Tag x={820} y={1130} color={C.amber} size={46} o={Math.max(0, -Math.sin((f / 60) * Math.PI * 2))}>tắc</Tag>
  </g>
);

// --- Cảnh 6 ---
const P21: Panel = ({f}) => (
  <g>
    <Head a="Muốn đo thời gian thật đều" b="dựa vào một thứ lặp lại đều đặn" />
    <Pend px={300} py={520} L={380} f={f} amp={28} r={36} />
    {Array.from({length: 6}, (_, i) => <circle key={i} cx={560 + i * 80} cy={900} r={22} fill={C.amber} stroke={C.cream} strokeWidth={4} opacity={sp(f, 10 + i * 10, 18 + i * 10)} />)}
    <Tag x={760} y={1000} color={C.cream} size={40} o={sp(f, 60, 76)}>nhịp nào cũng như nhau</Tag>
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Mỗi ngày chỉ lệch khoảng 15 giây" b="thay vì 15 phút" />
    <Lab x={110} y={700} size={40} anchor="start" color={C.cream}>15 phút</Lab>
    <Bar x={110} y={730} w={860} color="#e0613b" p={1} />
    <Lab x={110} y={900} size={40} anchor="start" color={C.cream}>15 giây</Lab>
    <Bar x={110} y={930} w={860} color="#6fd18f" p={sp(f, 10, 30) / 60} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.25} hat="gear" cheer={sp(f, 30, 50)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22];
