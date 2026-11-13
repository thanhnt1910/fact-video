import React from 'react';
import {Arrow, Bar, Big, C, Calc, Dash, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const BEAM = '#9fe8ff';
const MOON = '#d9d4c7';
const SUNC = '#f2c14e';
const RED = '#e0613b';

const Earth: React.FC<{x: number; y: number; r: number; o?: number}> = ({x, y, r, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill="#2f6fa8" stroke={C.cream} strokeWidth={6} />
    <path d={`M ${x - r * 0.5} ${y - r * 0.55} q ${r * 0.35} ${-r * 0.1} ${r * 0.5} ${r * 0.2} q ${-r * 0.1} ${r * 0.4} ${-r * 0.45} ${r * 0.35} z`} fill="#4f9a5a" />
    <path d={`M ${x + r * 0.1} ${y + r * 0.15} q ${r * 0.4} ${-r * 0.1} ${r * 0.5} ${r * 0.25} q ${-r * 0.2} ${r * 0.4} ${-r * 0.5} ${r * 0.2} z`} fill="#4f9a5a" />
  </g>
);
const Moon: React.FC<{x: number; y: number; r: number; o?: number}> = ({x, y, r, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill={MOON} stroke={C.cream} strokeWidth={5} />
    <circle cx={x - r * 0.3} cy={y - r * 0.2} r={r * 0.18} fill="#b5ae9f" />
    <circle cx={x + r * 0.35} cy={y + r * 0.25} r={r * 0.13} fill="#b5ae9f" />
    <circle cx={x + r * 0.1} cy={y - r * 0.45} r={r * 0.09} fill="#b5ae9f" />
  </g>
);
const Clock: React.FC<{x: number; y: number; r: number; spin?: number; o?: number}> = ({x, y, r, spin = 0, o = 1}) => {
  const a = spin * 2 * Math.PI - Math.PI / 2;
  return (
    <g opacity={clamp01(o)}>
      <circle cx={x} cy={y} r={r} fill="#101a33" stroke={C.amber} strokeWidth={r * 0.08} />
      {Array.from({length: 12}).map((_, i) => {
        const b = (i / 12) * 2 * Math.PI;
        return <line key={i} x1={x + Math.cos(b) * r * 0.8} y1={y + Math.sin(b) * r * 0.8} x2={x + Math.cos(b) * r * 0.92} y2={y + Math.sin(b) * r * 0.92} stroke={C.cream} strokeWidth={r * 0.05} strokeLinecap="round" />;
      })}
      <line x1={x} y1={y} x2={x + Math.cos(a) * r * 0.72} y2={y + Math.sin(a) * r * 0.72} stroke={C.cream} strokeWidth={r * 0.07} strokeLinecap="round" />
      <circle cx={x} cy={y} r={r * 0.08} fill={C.amber} />
    </g>
  );
};
// Tia sáng chạy từ (x1,y1) tới (x2,y2): đầu tia ở vị trí p (0..1), đuôi dài tail.
const Beam: React.FC<{x1: number; y1: number; x2: number; y2: number; p: number; tail?: number; color?: string}> = ({x1, y1, x2, y2, p, tail = 0.25, color = BEAM}) => {
  const q = clamp01(p);
  const s = clamp01(p - tail);
  if (q <= 0) return null;
  return (
    <g>
      <line x1={lerp(x1, x2, s)} y1={lerp(y1, y2, s)} x2={lerp(x1, x2, q)} y2={lerp(y1, y2, q)} stroke={color} strokeWidth={10} strokeLinecap="round" opacity={0.85} />
      <circle cx={lerp(x1, x2, q)} cy={lerp(y1, y2, q)} r={12} fill="#ffffff" />
    </g>
  );
};
// Tia đi rồi về theo chu kỳ T khung hình.
const Ping: React.FC<{f: number; x1: number; y1: number; x2: number; y2: number; T?: number; start?: number}> = ({f, x1, y1, x2, y2, T = 70, start = 0}) => {
  if (f < start) return null;
  const t = ((f - start) % T) / T;
  return t < 0.5 ? <Beam x1={x1} y1={y1} x2={x2} y2={y2} p={t * 2 * 1.25} /> : <Beam x1={x2} y1={y2} x2={x1} y2={y1} p={(t - 0.5) * 2 * 1.25} color={SUNC} />;
};
const Scene: React.FC<{o?: number}> = ({o = 1}) => (
  <g opacity={clamp01(o)}>
    <Earth x={300} y={1040} r={150} />
    <Moon x={820} y={580} r={75} />
  </g>
);
const Mirror: React.FC<{x: number; y: number; s?: number; o?: number}> = ({x, y, s = 1, o = 1}) => (
  <g opacity={clamp01(o)} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-60} y={-40} width={120} height={80} rx={6} fill="#26314f" stroke={C.cream} strokeWidth={4 / s} />
    {[0, 1, 2, 3, 4, 5].map((i) => (
      <circle key={i} cx={-38 + (i % 3) * 38} cy={-16 + Math.floor(i / 3) * 32} r={13} fill="#7aa7d8" stroke={C.cream} strokeWidth={2 / s} />
    ))}
    <line x1={0} y1={40} x2={0} y2={70} stroke={C.cream} strokeWidth={5 / s} />
  </g>
);
const Disc: React.FC<{x: number; y: number; r: number; cover: number}> = ({x, y, r, cover}) => (
  <g>
    <circle cx={x} cy={y} r={r} fill={SUNC} stroke={C.cream} strokeWidth={4} />
    <circle cx={x + (1 - cover) * r * 2} cy={y} r={r * 1.02} fill="#141b30" stroke="#5a6688" strokeWidth={3} />
  </g>
);

// --- Cảnh 1: câu hỏi ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Mặt Trăng xa bao nhiêu?" b="chính xác đến mi-li-mét" />
    <Scene o={sp(f, 4, 20)} />
    <Dash x1={400} y1={940} x2={760} y2={630} p={sp(f, 14, 40)} color={C.cream} />
    <Big x={620} y={850} size={120} color={C.amber} o={0.9 * sp(f, 26, 42)}>?</Big>
    <HatHero x={640} y={1250} s={2} walk={f * 0.1} hat="helmet" />
  </g>
);
const P1: Panel = ({f}) => {
  const p = sp(f, 6, 40) * 0.35;
  return (
    <g>
      <Head a="Không thể căng thước dây" b="từ Trái Đất lên tới đó" />
      <Scene />
      <line x1={420} y1={930} x2={lerp(420, 760, p)} y2={lerp(930, 630, p)} stroke={SUNC} strokeWidth={12} strokeDasharray="22 10" />
      <Tag x={700} y={940} color={RED} size={60} o={sp(f, 36, 50)}>✕</Tag>
      <HatHero x={640} y={1250} s={2} walk={f * 0.12} hat="helmet" />
    </g>
  );
};
const P2: Panel = ({f}) => (
  <g>
    <Head a="Chỉ cần một tia sáng" b="và một chiếc đồng hồ" />
    <Scene />
    <Ping f={f} x1={410} y1={940} x2={770} y2={620} start={6} />
    <Clock x={800} y={1050} r={90} spin={f * 0.02} o={sp(f, 20, 34)} />
    <HatHero x={560} y={1250} s={2} walk={f * 0.12} cheer={sp(f, 30, 48)} hat="helmet" />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Tia sáng ấy đo" b="khoảng cách thế nào?" />
    <Scene />
    <Ping f={f} x1={410} y1={940} x2={770} y2={620} />
    <Big x={640} y={1180} size={130} color={C.amber} o={0.9 * sp(f, 14, 30)}>?</Big>
  </g>
);

// --- Cảnh 2: người xưa ---
const Eye: React.FC<{x: number; y: number; s?: number; o?: number}> = ({x, y, s = 1, o = 1}) => (
  <g opacity={clamp01(o)} transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M -110 0 Q 0 -80 110 0 Q 0 80 -110 0 Z" fill="#f4efe2" stroke={C.cream} strokeWidth={5} />
    <circle cx={0} cy={0} r={34} fill="#3b6ea8" />
    <circle cx={0} cy={0} r={15} fill="#101010" />
  </g>
);
const P4: Panel = ({f}) => (
  <g>
    <Head a="Người xưa chỉ có" b="đôi mắt và hình học" />
    <Eye x={380} y={760} s={1.2} o={sp(f, 4, 18)} />
    <path d="M 640 960 L 900 960 L 770 640 Z" fill="none" stroke={C.amber} strokeWidth={8} strokeLinejoin="round" opacity={sp(f, 16, 32)} />
    <HatHero x={200} y={1250} s={2} walk={f * 0.12} hat="scholar" />
  </g>
);
const City: React.FC<{x: number; y: number; o?: number}> = ({x, y, o = 1}) => (
  <g opacity={clamp01(o)} fill="#3a4a72" stroke={C.cream} strokeWidth={3}>
    <rect x={x - 60} y={y - 70} width={36} height={70} />
    <rect x={x - 20} y={y - 110} width={40} height={110} />
    <rect x={x + 24} y={y - 50} width={36} height={50} />
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Cùng nhìn một nhật thực" b="từ hai thành phố" />
    <Disc x={540} y={650} r={110} cover={0.3 + sp(f, 4, 40) * 0.7} />
    <City x={280} y={1180} o={sp(f, 14, 28)} />
    <City x={800} y={1180} o={sp(f, 20, 34)} />
    <Dash x1={280} y1={1060} x2={510} y2={770} p={sp(f, 26, 46)} color={C.cream} />
    <Dash x1={800} y1={1060} x2={570} y2={770} p={sp(f, 30, 50)} color={C.cream} />
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Một nơi bị che hoàn toàn" b="nơi kia chỉ che một phần" />
    <Disc x={300} y={760} r={120} cover={sp(f, 4, 30)} />
    <Disc x={780} y={760} r={120} cover={sp(f, 4, 30) * 0.8} />
    <Tag x={300} y={960} color={C.cream} size={42} o={sp(f, 20, 34)}>che hoàn toàn</Tag>
    <Tag x={780} y={960} color={C.cream} size={42} o={sp(f, 26, 40)}>che một phần</Tag>
    <City x={300} y={1200} />
    <City x={780} y={1200} />
  </g>
);
const P7: Panel = ({f}) => {
  const hx = 540 + 200 * Math.sin(f * 0.05);
  return (
    <g>
      <Head a="Như ngón tay che đèn" b="đổi chỗ thì che lệch đi" />
      <circle cx={540} cy={560} r={46} fill={SUNC} opacity={0.95} />
      <circle cx={540} cy={560} r={80} fill={SUNC} opacity={0.15} />
      <rect x={515} y={760} width={50} height={150} rx={25} fill="#e8b48a" stroke={C.cream} strokeWidth={4} />
      <line x1={hx} y1={1110} x2={540} y2={560} stroke={C.cream} strokeWidth={3} strokeDasharray="10 10" opacity={0.6} />
      <HatHero x={hx} y={1250} s={2} walk={f * 0.15} hat="scholar" />
    </g>
  );
};
const P8: Panel = ({f}) => (
  <g>
    <Head a="Hi-pác-cơ vẽ một tam giác" b="hai thành phố và Mặt Trăng" />
    <Moon x={540} y={560} r={70} />
    <City x={250} y={1180} />
    <City x={830} y={1180} />
    <Dash x1={250} y1={1060} x2={520} y2={620} p={sp(f, 4, 30)} color={C.amber} />
    <Dash x1={830} y1={1060} x2={560} y2={620} p={sp(f, 10, 36)} color={C.amber} />
    <Dash x1={300} y1={1100} x2={780} y2={1100} p={sp(f, 20, 44)} color={C.amber} />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Ông tính ra: Mặt Trăng xa" b="60 đến 70 lần bán kính" />
    <Earth x={230} y={900} r={110} />
    <line x1={230} y1={900} x2={340} y2={900} stroke={SUNC} strokeWidth={8} opacity={sp(f, 6, 18)} />
    <Tag x={285} y={1060} color={C.cream} size={38} o={sp(f, 10, 24)}>tâm → mặt đất</Tag>
    <Big x={690} y={940} size={120} color={C.amber} o={sp(f, 18, 34)}>× 60–70</Big>
  </g>
);
const P10: Panel = ({f}) => {
  const m = 540 + 140 * Math.sin(f * 0.12);
  return (
    <g>
      <Head a="Đúng cỡ độ lớn" b="nhưng còn dao động nhiều" />
      <line x1={170} y1={820} x2={910} y2={820} stroke={C.cream} strokeWidth={6} />
      <rect x={360} y={780} width={360} height={80} rx={14} fill={C.amber} opacity={0.25} />
      <circle cx={m} cy={820} r={30} fill={C.amber} />
      <Tag x={540} y={960} color={C.cream} size={44} o={sp(f, 18, 34)}>độ lệch rất nhỏ</Tag>
      <HatHero x={540} y={1250} s={2} walk={f * 0.1} hat="scholar" />
    </g>
  );
};

// --- Cảnh 3: ánh sáng và công thức ---
const P11: Panel = ({f}) => (
  <g>
    <Head a="Cần cách đo" b="không dựa vào mắt nhìn" />
    <Eye x={540} y={780} s={1.2} />
    <line x1={400} y1={680} x2={680} y2={880} stroke={RED} strokeWidth={14} strokeLinecap="round" opacity={sp(f, 10, 26)} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="helmet" />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Ánh sáng mỗi giây đi" b="khoảng 300 000 km" />
    <Beam x1={120} y1={720} x2={960} y2={720} p={((f % 50) / 50) * 1.3} />
    <Big x={540} y={890} size={120} color={C.amber} o={sp(f, 10, 28)}>300 000 km</Big>
    <Tag x={540} y={980} color={C.cream} size={48} o={sp(f, 20, 36)}>mỗi giây</Tag>
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="helmet" />
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Biết ánh sáng chạy bao lâu" b="là biết quãng đường" />
    <Clock x={300} y={800} r={130} spin={f * 0.02} />
    <Beam x1={480} y1={800} x2={960} y2={800} p={((f % 50) / 50) * 1.3} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="helmet" />
  </g>
);
const P14: Panel = ({f}) => {
  const t = (f % 60) / 60;
  const bx = t < 0.5 ? lerp(330, 840, t * 2) : lerp(840, 330, (t - 0.5) * 2);
  return (
    <g>
      <Head a="Như ném bóng vào tường" b="thời gian đi về chia đôi" />
      <rect x={870} y={560} width={60} height={640} fill="#5a4a6a" stroke={C.cream} strokeWidth={4} />
      <circle cx={bx} cy={900} r={34} fill={RED} stroke={C.cream} strokeWidth={4} />
      <Tag x={590} y={1060} color={C.amber} size={46} o={sp(f, 20, 36)}>đi + về, rồi ÷ 2</Tag>
      <HatHero x={230} y={1250} s={2} walk={f * 0.1} cheer={t < 0.1 ? 1 : 0} hat="helmet" />
    </g>
  );
};
const P15: Panel = ({f}) => (
  <g>
    <Head a="Công thức đo khoảng cách" />
    <Calc f={f} y={680} step={150} lines={[{t: 'khoảng cách', at: 4, size: 84, color: C.cream}, {t: '= tốc độ × thời gian', at: 18, size: 76, color: C.amber}, {t: '÷ 2', at: 34, size: 96, color: C.amber}]} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="helmet" />
  </g>
);

// --- Cảnh 4: gương và laser ---
const P16: Panel = ({f}) => (
  <g>
    <Head a="Năm 1969, Apollo 11" b="đặt một tấm gương" />
    <path d="M 100 1000 Q 540 860 980 1000 L 980 1200 L 100 1200 Z" fill={MOON} opacity={0.85} />
    <Mirror x={680} y={900} s={1.6} o={sp(f, 10, 26)} />
    <HatHero x={380} y={1080} s={2} walk={f * 0.12} cheer={sp(f, 24, 44)} hat="helmet" />
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Như miếng phản quang" b="trên xe đạp" />
    <rect x={640} y={720} width={150} height={220} rx={30} fill={RED} stroke={C.cream} strokeWidth={6} />
    {[0, 1, 2, 3, 4, 5].map((i) => (
      <path key={i} d={`M ${665 + (i % 2) * 50} ${750 + Math.floor(i / 2) * 60} l 25 25 l -25 25 l -25 -25 z`} fill="#ff8a6a" opacity={0.8} />
    ))}
    <Arrow x1={200} y1={780} x2={610} y2={780} p={sp(f, 6, 28)} color={BEAM} />
    <Arrow x1={610} y1={880} x2={200} y2={880} p={sp(f, 24, 46)} color={SUNC} />
    <Tag x={400} y={1000} color={C.cream} size={42} o={sp(f, 36, 50)}>bật thẳng về chỗ cũ</Tag>
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Đài thiên văn Lick" b="bắn một xung laser" />
    <Scene />
    <rect x={250} y={860} width={34} height={90} fill="#c9d3ea" transform="rotate(48 267 905)" />
    <Beam x1={400} y1={930} x2={770} y2={620} p={sp(f, 10, 50) * 1.25} color="#7cff9a" />
    <Tag x={300} y={1240} color={C.cream} size={40} o={sp(f, 6, 20)}>California</Tag>
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Hơn 1 000 tỉ hạt bay đi" b="chỉ vài hạt quay về" />
    <Scene />
    {Array.from({length: 14}).map((_, i) => {
      const t = clamp01((f - i * 2) / 40);
      return <circle key={i} cx={lerp(410 + (i % 4) * 8, 770 + (i % 5) * 30 - 60, t)} cy={lerp(940, 620 - (i % 3) * 30, t)} r={7} fill={BEAM} opacity={t > 0 && t < 1 ? 0.9 : 0} />;
    })}
    {[0, 1].map((i) => {
      const t = clamp01((f - 46 - i * 6) / 40);
      return <circle key={i} cx={lerp(770, 410, t)} cy={lerp(620, 940, t)} r={9} fill={SUNC} opacity={t > 0 ? 1 : 0} />;
    })}
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Bấm giờ lúc bắn" b="đến lúc nhận lại" />
    <Clock x={540} y={800} r={190} spin={sp(f, 4, 60) * 2.5} />
    <Big x={540} y={1180} size={130} color={C.amber} o={sp(f, 30, 46)}>2,5 giây</Big>
  </g>
);

// --- Cảnh 5: tính ---
const P21: Panel = ({f}) => (
  <g>
    <Head a="Quãng đường đi và về" />
    <Calc f={f} y={760} step={170} lines={[{t: '300 000 × 2,5', at: 6, size: 110}]} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.12} hat="helmet" />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Quãng đường đi và về" />
    <Calc f={f} y={760} step={170} lines={[{t: '300 000 × 2,5', at: 0, size: 110}, {t: '= 750 000 km', at: 6, size: 120, color: C.amber}]} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.15} hat="helmet" />
  </g>
);
const P23: Panel = ({f}) => (
  <g>
    <Head a="Gồm đường đi và đường về" b="nên chia đôi" />
    <Scene />
    <Arrow x1={390} y1={920} x2={750} y2={610} p={sp(f, 4, 26)} color={BEAM} />
    <Arrow x1={790} y1={680} x2={430} y2={990} p={sp(f, 20, 42)} color={SUNC} />
    <Tag x={500} y={720} color={BEAM} size={44} o={sp(f, 14, 28)}>đi</Tag>
    <Tag x={700} y={900} color={SUNC} size={44} o={sp(f, 30, 44)}>về</Tag>
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Chia đôi" b="ra khoảng cách tới Mặt Trăng" />
    <Calc f={f} y={760} step={170} lines={[{t: '750 000 ÷ 2', at: 4, size: 110}, {t: '= 375 000 km', at: 24, size: 120, color: C.amber}]} />
    <HatHero x={540} y={1250} s={2} walk={f * 0.2} cheer={sp(f, 34, 52)} hat="helmet" />
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Số thật trung bình" />
    <Big x={540} y={680} size={130} color={C.amber} o={sp(f, 4, 20)}>384 400 km</Big>
    <Bar x={110} y={860} w={860} color={C.amber} p={sp(f, 14, 36)} label="số thật: 384 400" />
    <Bar x={110} y={1000} w={860} color={BEAM} p={sp(f, 20, 42) * 0.976} label="ta tính: 375 000" />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Lệch chưa tới 3%" b="vì ta đã làm tròn" />
    <Bar x={110} y={700} w={860} color={C.amber} p={1} label="số thật: 384 400" />
    <Bar x={110} y={840} w={860} color={BEAM} p={0.976} label="ta tính: 375 000" />
    <Big x={540} y={1100} size={140} color={C.amber} o={sp(f, 10, 28)}>&lt; 3%</Big>
  </g>
);

// --- Cảnh 6: mi-li-mét và kết ---
const P27: Panel = ({f}) => (
  <g>
    <Head a="Đo thời gian kỹ hơn" b="chính xác đến mi-li-mét" />
    <rect x={140} y={760} width={800} height={110} fill="#c9a86a" stroke={C.cream} strokeWidth={4} />
    {Array.from({length: 41}).map((_, i) => (
      <line key={i} x1={160 + i * 19} y1={760} x2={160 + i * 19} y2={760 + (i % 10 === 0 ? 70 : i % 5 === 0 ? 50 : 30)} stroke="#2a2018" strokeWidth={3} />
    ))}
    <Big x={540} y={1060} size={130} color={C.amber} o={sp(f, 14, 30)}>1 mm</Big>
    <HatHero x={180} y={1250} s={2} walk={f * 0.12} hat="goggles" />
  </g>
);
const P28: Panel = ({f}) => (
  <g>
    <Head a="1 mi-li-mét" b="dày bằng khoảng 10 tờ giấy" />
    {Array.from({length: 10}).map((_, i) => (
      <rect key={i} x={300} y={980 - i * 34} width={480} height={22} rx={3} fill="#f4efe2" stroke="#8a8270" strokeWidth={2} opacity={sp(f, 4 + i * 3, 10 + i * 3)} />
    ))}
    <Tag x={540} y={1110} color={C.amber} size={48} o={sp(f, 36, 50)}>10 tờ ≈ 1 mm</Tag>
    <HatHero x={170} y={1250} s={2} walk={f * 0.12} hat="goggles" />
  </g>
);
const P29: Panel = ({f}) => {
  const dx = sp(f, 6, 70) * 70;
  return (
    <g>
      <Head a="Mặt Trăng xa thêm" b="3,8 cm mỗi năm" />
      <Earth x={260} y={900} r={130} />
      <Moon x={720 + dx} y={760} r={70} />
      <Arrow x1={720} y1={880} x2={720 + dx + 40} y2={880} p={sp(f, 10, 40)} color={C.amber} />
      <Big x={600} y={1120} size={100} color={C.amber} o={sp(f, 20, 36)}>+3,8 cm / năm</Big>
    </g>
  );
};
const P30: Panel = ({f}) => (
  <g>
    <Head a="Đo bằng thời gian" b="một tia sáng đi và về" />
    <Scene />
    <Ping f={f} x1={410} y1={940} x2={770} y2={620} T={60} />
    <HatHero x={640} y={1250} s={2} walk={f * 0.25} cheer={sp(f, 20, 44)} hat="helmet" />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30];
