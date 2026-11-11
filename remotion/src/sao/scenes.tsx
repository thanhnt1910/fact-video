import React from 'react';
import {Arrow, Bar, Big, C, Calc, Dash, Head, HatHero, Hero, Lab, Panel, Tag, clamp01, lerp, seg, sp} from '../khoahoc/kit';

const STAR = '#ffe9a8';
const SKY = '#8fb4ff';

const Eye: React.FC<{x: number; y: number; o?: number}> = ({x, y, o = 1}) => (
  <g opacity={clamp01(o)}>
    <ellipse cx={x} cy={y} rx={44} ry={28} fill={C.cream} stroke={C.bg2} strokeWidth={4} />
    <circle cx={x} cy={y} r={14} fill="#2b3a67" />
  </g>
);
const Finger: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} stroke={C.cream} strokeWidth={5 / s}>
    <rect x={-22} y={-150} width={44} height={170} rx={22} fill="#e7b48f" />
    <line x1={-12} y1={-110} x2={12} y2={-110} stroke="#b9805c" strokeWidth={3} />
  </g>
);
const Star: React.FC<{x: number; y: number; r?: number; o?: number}> = ({x, y, r = 14, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r * 2.4} fill={STAR} opacity={0.18} />
    <circle cx={x} cy={y} r={r} fill={STAR} stroke={C.cream} strokeWidth={3} />
  </g>
);

const jump = (f: number) => (Math.floor(f / 28) % 2 ? 1 : -1);

// --- Cảnh 1: ngón tay nhảy ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Đưa ngón tay ra trước mặt" b="đổi mắt, ngón tay nhảy" />
    <Eye x={400} y={560} o={sp(f, 4, 14)} />
    <Eye x={680} y={560} o={sp(f, 4, 14)} />
    <line x1={120} y1={900} x2={960} y2={900} stroke={C.dim} strokeWidth={4} opacity={0.5} />
    {[220, 400, 580, 760, 900].map((x) => <circle key={x} cx={x} cy={900} r={9} fill={SKY} opacity={0.7} />)}
    <Finger x={540 + 60 * jump(f)} y={1120} s={1.2} />
    <Tag x={540} y={730} color={C.amber} size={44} o={sp(f, 16, 30)}>nhắm mắt này, rồi mắt kia</Tag>
    <HatHero x={190} y={1250} s={2} walk={f * 0.25} hat="helmet" />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Cái nhảy nhỏ xíu ấy" b="cho biết sao xa bao nhiêu?" />
    <Finger x={330 + 50 * jump(f)} y={1120} s={1.1} />
    <Dash x1={420} y1={900} x2={820} y2={640} p={sp(f, 10, 40)} />
    <Star x={860} y={600} r={18} o={sp(f, 6, 20)} />
    <Lab x={540} y={800} size={130} color={C.amber} o={0.9 * sp(f, 30, 44)}>?</Lab>
    <HatHero x={780} y={1250} s={2} walk={f * 0.25} hat="helmet" cheer={sp(f, 40, 60)} />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Sao ở rất xa" b="nên chỉ nhảy một chút xíu" />
    <Finger x={300 + 70 * jump(f)} y={1100} s={1.1} />
    <Tag x={300} y={1200} color={C.cream} size={38} o={sp(f, 10, 24)}>ngón tay: nhảy nhiều</Tag>
    <Star x={780 + 2 * jump(f)} y={800} r={16} />
    <Tag x={740} y={900} color={C.cream} size={38} o={sp(f, 20, 34)}>sao: gần như đứng yên</Tag>
    <Tag x={540} y={640} color={C.amber} size={42} o={sp(f, 30, 44)}>mắt thường không thấy</Tag>
  </g>
);

// --- Cảnh 2: vì sao nhảy, vì sao cần hai chỗ xa ---
const Sight: React.FC<{ex: number[]; ey: number; ox: number; oy: number; wy: number; p: number; o?: number}> = ({ex, ey, ox, oy, wy, p, o = 1}) => (
  <g opacity={o}>
    {ex.map((e, i) => {
      const k = (ey - wy) / (ey - oy);
      const wx = e + (ox - e) * k;
      const c = i ? '#f2b35a' : '#8fd1ff';
      return (
        <g key={i}>
          <line x1={e} y1={ey} x2={lerp(e, wx, p)} y2={lerp(ey, wy, p)} stroke={c} strokeWidth={5} strokeLinecap="round" />
          <circle cx={e} cy={ey} r={14} fill={c} stroke={C.cream} strokeWidth={3} />
          <circle cx={lerp(e, wx, p)} cy={lerp(ey, wy, p)} r={9} fill={c} opacity={clamp01(p * 2)} />
        </g>
      );
    })}
    <circle cx={ox} cy={oy} r={20} fill={STAR} stroke={C.cream} strokeWidth={4} />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Vì sao ngón tay nhảy?" b="hai mắt đứng 2 chỗ khác nhau" />
    <line x1={140} y1={560} x2={940} y2={560} stroke={C.dim} strokeWidth={5} opacity={0.6} />
    <Sight ex={[480, 600]} ey={1150} ox={540} oy={850} wy={560} p={seg(f, 8, 50)} />
    <Tag x={540} y={1215} color={C.cream} size={36} o={sp(f, 20, 34)}>hai mắt cách nhau chừng 6 cm</Tag>
  </g>
);
const P4: Panel = ({f}) => (
  <g>
    <Head a="Vật càng gần nhảy càng nhiều" b="vật càng xa nhảy càng ít" />
    <line x1={80} y1={500} x2={1000} y2={500} stroke={C.dim} strokeWidth={5} opacity={0.6} />
    <Sight ex={[280, 340]} ey={1180} ox={310} oy={900} wy={500} p={seg(f, 6, 44)} />
    <Sight ex={[760, 820]} ey={1180} ox={790} oy={640} wy={500} p={seg(f, 24, 60)} />
    <Tag x={310} y={1250} color={C.amber} size={38} o={sp(f, 10, 24)}>gần: nhảy rộng</Tag>
    <Tag x={790} y={1250} color={C.amber} size={38} o={sp(f, 28, 42)}>xa: nhảy hẹp</Tag>
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Muốn thấy sao nhảy" b="phải nhìn từ 2 chỗ thật xa" />
    <line x1={80} y1={500} x2={1000} y2={500} stroke={C.dim} strokeWidth={5} opacity={0.6} />
    <Sight ex={[240, 840]} ey={1180} ox={540} oy={640} wy={500} p={seg(f, 6, 60)} />
    <Tag x={540} y={1250} color={C.cream} size={38} o={sp(f, 20, 34)}>hai chỗ đứng cách nhau thật xa</Tag>
  </g>
);

// --- Cảnh 3: quỹ đạo Trái Đất ---
const Orbit: React.FC<{ang: number; ghost?: boolean; f: number}> = ({ang, ghost, f}) => {
  const cx = 540, cy = 860, r = 270;
  const ex = cx + r * Math.cos(ang), ey = cy - r * Math.sin(ang);
  return (
    <g>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={C.dim} strokeWidth={3} strokeDasharray="10 12" opacity={0.6} />
      <circle cx={cx} cy={cy} r={54} fill="#f6c453" stroke={C.cream} strokeWidth={5} />
      <circle cx={cx} cy={cy} r={86} fill="#f6c453" opacity={0.2 + 0.05 * Math.sin(f * 0.1)} />
      {ghost && <circle cx={cx + r} cy={cy} r={26} fill="none" stroke={SKY} strokeWidth={4} strokeDasharray="6 6" />}
      <circle cx={ex} cy={ey} r={26} fill="#3f86d6" stroke={C.cream} strokeWidth={5} />
      <ellipse cx={ex - 6} cy={ey - 4} rx={9} ry={6} fill="#5fa86a" />
    </g>
  );
};
const P6: Panel = ({f}) => (
  <g>
    <Head a="Trái Đất đi quanh Mặt Trời" b="6 tháng sau ở bên kia" />
    <Orbit ang={Math.PI * seg(f, 10, 80)} ghost f={f} />
    <Tag x={540} y={1240} color={C.amber} size={44} o={sp(f, 50, 66)}>nửa vòng = 6 tháng</Tag>
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Hai chỗ đứng cách nhau" b="khoảng 300 triệu km" />
    <Orbit ang={Math.PI} ghost f={f} />
    <Arrow x1={270} y1={1180} x2={810} y2={1180} p={sp(f, 8, 40)} />
    <Arrow x1={810} y1={1180} x2={270} y2={1180} p={sp(f, 8, 40)} />
    <Big x={540} y={1150} size={96} color={C.amber} o={sp(f, 24, 40)}>300 triệu km</Big>
  </g>
);

// --- Cảnh 4: Bét-xen ---
const Scope: React.FC<{x: number; y: number; rot: number; o?: number}> = ({x, y, rot, o = 1}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot})`} opacity={clamp01(o)} stroke={C.cream} strokeWidth={5}>
    <rect x={-40} y={-30} width={230} height={60} rx={10} fill="#8a6a3a" />
    <rect x={190} y={-40} width={70} height={80} rx={10} fill="#b08a50" />
    <line x1={60} y1={30} x2={20} y2={150} />
    <line x1={60} y1={30} x2={110} y2={150} />
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Năm 1838" b="Bét-xen quyết đo một ngôi sao" />
    <Scope x={400} y={900} rot={-24 + 6 * Math.sin(f * 0.05)} />
    <Star x={820} y={640} r={16} o={sp(f, 10, 24)} />
    <HatHero x={230} y={1240} s={2} walk={f * 0.2} hat="scholar" />
    <Big x={780} y={1100} size={110} color={C.amber} o={sp(f, 20, 36)}>1838</Big>
  </g>
);
const CYG: [number, number][] = [[540, 560], [540, 760], [540, 960], [400, 760], [680, 760]];
const P9: Panel = ({f}) => (
  <g>
    <Head a="Một sao mờ trong chòm Thiên Nga" b="trôi nhanh hơn các sao khác" />
    <g stroke={C.cream} strokeWidth={3} opacity={0.4}>
      <line x1={540} y1={560} x2={540} y2={960} />
      <line x1={400} y1={760} x2={680} y2={760} />
    </g>
    {CYG.map(([x, y], i) => <Star key={i} x={x + (i === 4 ? 30 * seg(f, 30, 80) : 0)} y={y} r={i === 4 ? 12 : 17} o={sp(f, 4 + i * 3, 18 + i * 3)} />)}
    <Arrow x1={680} y1={760} x2={830} y2={760} p={sp(f, 30, 70)} />
    <Tag x={760} y={850} color={C.amber} size={38} o={sp(f, 40, 56)}>trôi nhanh</Tag>
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Ông nghĩ: sao trôi nhanh" b="thì có thể ở gần" />
    {['trôi nhanh', 'ở gần', 'nhảy đủ lớn để đo'].map((t, i) => (
      <g key={t} opacity={sp(f, 8 + i * 22, 22 + i * 22)}>
        <rect x={190} y={560 + i * 190} width={700} height={120} rx={24} fill="#1d2a66" stroke={C.cream} strokeWidth={5} />
        <Lab x={540} y={638 + i * 190} size={52} color={i === 2 ? C.amber : C.cream}>{t}</Lab>
        {i < 2 && <Arrow x1={540} y1={690 + i * 190} x2={540} y2={745 + i * 190} p={sp(f, 18 + i * 22, 34 + i * 22)} w={6} />}
      </g>
    ))}
  </g>
);

// --- Cảnh 5: giây góc ---
const P11: Panel = ({f}) => (
  <g>
    <Head a="Ông đo được cái nhảy" b="chỉ khoảng 0,314 giây góc" />
    <Star x={540 + 3 * jump(f)} y={760} r={18} />
    <Big x={540} y={1020} size={140} color={C.amber} o={sp(f, 12, 28)}>0,314″</Big>
    <Tag x={540} y={1120} color={C.cream} size={42} o={sp(f, 24, 38)}>giây góc</Tag>
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="1 giây góc" b="= 1/3 600 của 1 độ" />
    <rect x={110} y={760} width={860} height={90} rx={12} fill="#1d2a66" stroke={C.cream} strokeWidth={5} />
    {Array.from({length: 61}, (_, i) => <line key={i} x1={110 + i * 14.1} y1={760} x2={110 + i * 14.1} y2={i % 10 ? 800 : 850} stroke={C.cream} strokeWidth={i % 10 ? 1.5 : 3} opacity={sp(f, 6, 30)} />)}
    <Lab x={110} y={730} size={40} anchor="start" color={C.amber} o={sp(f, 10, 24)}>1 độ</Lab>
    <rect x={110} y={760} width={3} height={90} fill={STAR} opacity={sp(f, 36, 48)} />
    <Arrow x1={190} y1={1000} x2={114} y2={870} p={sp(f, 40, 60)} />
    <Tag x={330} y={1040} color={C.amber} size={38} o={sp(f, 44, 58)}>1 giây góc: mảnh siêu nhỏ</Tag>
  </g>
);
const P13: Panel = ({f}) => {
  const k = seg(f, 20, 100);
  const sc = lerp(1, 0.06, k);
  const x = lerp(240, 840, k);
  return (
    <g>
      <Head a="Ví dụ: đồng xu 2,5 cm" b="phải đặt xa 16 km" />
      <circle cx={x} cy={900} r={140 * sc} fill="#d6a83a" stroke={C.cream} strokeWidth={Math.max(2, 7 * sc)} />
      <Dash x1={240} y1={1100} x2={840} y2={1100} p={k} />
      <Big x={540} y={1200} size={90} color={C.amber} o={sp(f, 60, 80)}>16 km</Big>
      <Tag x={240} y={1060} color={C.cream} size={34} o={1 - k}>2,5 cm</Tag>
    </g>
  );
};

// --- Cảnh 6: công thức ---
const P14: Panel = ({f}) => (
  <g>
    <Head a="Công thức rất gọn" />
    <Lab x={540} y={620} size={52} color={C.cream} o={sp(f, 6, 20)}>khoảng cách (pác-xếch)</Lab>
    <Big x={540} y={780} size={110} color={C.amber} o={sp(f, 20, 34)}>= 1 ÷ góc nhảy</Big>
    <Lab x={540} y={860} size={44} color={C.cream} o={sp(f, 30, 44)}>(góc nhảy tính bằng giây góc)</Lab>
    <HatHero x={200} y={1250} s={2} walk={f * 0.25} hat="scholar" cheer={sp(f, 40, 60)} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Đổi đơn vị" b="1 pác-xếch ≈ 3,26 năm ánh sáng" />
    <rect x={110} y={640} width={400} height={200} rx={24} fill="#1d2a66" stroke={C.cream} strokeWidth={5} opacity={sp(f, 6, 20)} />
    <Big x={310} y={760} size={64} o={sp(f, 8, 22)}>1 pác-xếch</Big>
    <Big x={555} y={770} size={80} color={C.cream} o={sp(f, 16, 30)}>≈</Big>
    <rect x={610} y={640} width={360} height={200} rx={24} fill="#1d2a66" stroke={C.cream} strokeWidth={5} opacity={sp(f, 14, 28)} />
    <Big x={790} y={730} size={72} o={sp(f, 18, 32)}>3,26</Big>
    <Lab x={790} y={800} size={36} color={C.cream} o={sp(f, 22, 36)}>năm ánh sáng</Lab>
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Năm ánh sáng là quãng đường" b="ánh sáng đi trong 1 năm" />
    <line x1={120} y1={800} x2={lerp(120, 960, seg(f, 8, 60))} y2={800} stroke={STAR} strokeWidth={10} strokeLinecap="round" />
    <circle cx={lerp(120, 960, seg(f, 8, 60))} cy={800} r={18} fill={STAR} stroke={C.cream} strokeWidth={4} />
    <Big x={540} y={1000} size={96} color={C.amber} o={sp(f, 50, 66)}>gần 10 nghìn tỉ km</Big>
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Với ngôi sao của Bét-xen" />
    <Calc f={f} y={720} lines={[{t: '1 ÷ 0,314', at: 8}, {t: '≈ 3,2 pác-xếch', at: 30, color: C.amber}]} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Rồi đổi sang năm ánh sáng" />
    <Calc f={f} y={680} lines={[{t: '3,2 pác-xếch', at: 4, color: C.dim, size: 70}, {t: '3,2 × 3,26', at: 14}, {t: '≈ 10,4 năm ánh sáng', at: 36, color: C.amber, size: 80}]} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Ánh sáng sao ấy đi" b="hơn 10 năm mới tới mắt ta" />
    <Star x={170} y={800} r={16} />
    <line x1={190} y1={800} x2={880} y2={800} stroke={C.dim} strokeWidth={4} strokeDasharray="8 10" opacity={0.6} />
    {Array.from({length: 10}, (_, i) => <circle key={i} cx={210 + i * 70} cy={800} r={10} fill={STAR} opacity={sp(f, 8 + i * 6, 16 + i * 6)} />)}
    <HatHero x={940} y={880} s={1.0} walk={f * 0.1} hat="helmet" />
    <Big x={540} y={1060} size={90} color={C.amber} o={sp(f, 70, 86)}>10 năm</Big>
  </g>
);

// --- Cảnh 7: so sánh, kết ---
const P20: Panel = ({f}) => (
  <g>
    <Head a="Số đo ngày nay" b="khoảng 11,4 năm ánh sáng" />
    <Bar x={110} y={700} w={800} color="#f2b35a" p={sp(f, 6, 30) * 10.4 / 11.4} label="Bét-xen: 10,4" />
    <Bar x={110} y={820} w={800} color="#8fd1ff" p={sp(f, 18, 42)} label="Ngày nay: 11,4" />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Bét-xen chỉ lệch chừng" b="1 năm ánh sáng" />
    <Bar x={110} y={700} w={800} color="#f2b35a" p={10.4 / 11.4} label="10,4" />
    <Bar x={110} y={820} w={800} color="#8fd1ff" p={1} label="11,4" />
    <rect x={110 + 800 * 10.4 / 11.4} y={690} width={800 * 1 / 11.4} height={70} rx={8} fill="none" stroke={C.amber} strokeWidth={6} opacity={sp(f, 10, 26)} strokeDasharray="10 8" />
    <Tag x={540} y={990} color={C.amber} size={44} o={sp(f, 24, 40)}>với dụng cụ thời ấy là rất giỏi</Tag>
    <HatHero x={200} y={1250} s={2} walk={f * 0.25} hat="scholar" cheer={sp(f, 30, 50)} />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Sao gần Mặt Trời nhất" b="cũng nhảy rất ít" />
    <Star x={540 + 4 * jump(f)} y={800} r={18} />
    <Big x={540} y={1020} size={120} color={C.amber} o={sp(f, 12, 28)}>0,77″</Big>
    <Tag x={540} y={1110} color={C.cream} size={40} o={sp(f, 24, 38)}>giây góc</Tag>
  </g>
);
const P23: Panel = ({f}) => (
  <g>
    <Head a="Nó xa" b="4,24 năm ánh sáng" />
    <circle cx={190} cy={820} r={46} fill="#f6c453" stroke={C.cream} strokeWidth={5} />
    <Star x={880} y={820} r={14} />
    <Dash x1={250} y1={820} x2={850} y2={820} p={sp(f, 8, 50)} />
    <Big x={540} y={730} size={80} color={C.amber} o={sp(f, 40, 56)}>4,24</Big>
    <Lab x={540} y={930} size={40} color={C.cream} o={sp(f, 48, 62)}>năm ánh sáng</Lab>
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Từ cái nhảy của ngón tay" b="đo được khoảng cách tới các sao" />
    <Finger x={330 + 50 * jump(f)} y={1050} s={1.1} />
    <Dash x1={420} y1={820} x2={820} y2={620} p={sp(f, 10, 40)} />
    <Star x={860} y={580} r={18} />
    <HatHero x={760} y={1250} s={2} walk={f * 0.25} hat="scholar" cheer={sp(f, 20, 40)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24];
void Hero;
