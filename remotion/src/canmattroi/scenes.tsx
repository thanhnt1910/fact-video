import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const SUN = '#f2b53e';
const EARTH = '#4a8fe0';
const RED = '#e0613b';
const AM = C.amber;
const CX = 540;

const Hero2: React.FC<{f: number; x?: number; cheer?: number}> = ({f, x = 170, cheer = 0}) => <HatHero x={x} y={1250} s={2} walk={f * 0.13} cheer={cheer} hat="helmet" />;

const Sun: React.FC<{cx: number; cy: number; r: number; o?: number}> = ({cx, cy, r, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={cx} cy={cy} r={r * 1.5} fill={SUN} opacity={0.18} />
    <circle cx={cx} cy={cy} r={r} fill={SUN} stroke={C.cream} strokeWidth={5} />
  </g>
);
const Ear: React.FC<{cx: number; cy: number; r: number}> = ({cx, cy, r}) => <circle cx={cx} cy={cy} r={r} fill={EARTH} stroke={C.cream} strokeWidth={4} />;
// Quỹ đạo tròn: Mặt Trời ở giữa, Trái Đất chạy quanh.
const Orb: React.FC<{f: number; cy?: number; R?: number; speed?: number; sunR?: number; pull?: boolean; fixedAng?: number}> = ({f, cy = 820, R = 260, speed = 0.05, sunR = 60, pull = false, fixedAng}) => {
  const a = fixedAng !== undefined ? fixedAng : f * speed;
  const ex = CX + R * Math.cos(a), ey = cy + R * Math.sin(a);
  return (
    <g>
      <circle cx={CX} cy={cy} r={R} fill="none" stroke={C.cream} strokeWidth={3} strokeDasharray="10 12" opacity={0.5} />
      <Sun cx={CX} cy={cy} r={sunR} />
      {pull && <Arrow x1={ex} y1={ey} x2={ex + (CX - ex) * 0.35} y2={ey + (cy - ey) * 0.35} color={RED} w={7} p={1} />}
      <Ear cx={ex} cy={ey} r={28} />
    </g>
  );
};
const Ball: React.FC<{f: number; x: number; y: number; L?: number; speed?: number; cut?: number}> = ({f, x, y, L = 230, speed = 0.12, cut}) => {
  const a = f * speed;
  const bx = x + L * Math.cos(a), by = y + L * Math.sin(a);
  const gone = cut !== undefined && f > cut;
  const fx = bx + (gone ? (f - cut!) * 10 * -Math.sin(a) : 0);
  const fy = by + (gone ? (f - cut!) * 10 * Math.cos(a) : 0);
  return (
    <g>
      {!gone && <line x1={x} y1={y} x2={bx} y2={by} stroke={C.cream} strokeWidth={5} />}
      <circle cx={gone ? fx : bx} cy={gone ? fy : by} r={34} fill={RED} stroke={C.cream} strokeWidth={5} />
      <circle cx={x} cy={y} r={20} fill={C.cream} />
    </g>
  );
};

// --- Cảnh 1: câu hỏi ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Không ai đặt được" b="Mặt Trời lên cân" />
    <Sun cx={CX} cy={800} r={150} o={sp(f, 2, 16)} />
    <Big x={CX + 270} y={620} size={150} color={AM} o={0.9 * sp(f, 14, 30)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Mỗi ngày Trái Đất" b="đã tự cân nó giúp ta" />
    <Orb f={f} R={270} />
    <Hero2 f={f} />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Chỉ cần biết" b="Trái Đất chạy nhanh cỡ nào" />
    <Orb f={f} R={270} speed={0.08} />
    <Tag x={CX} y={1230} color={AM} size={46} o={sp(f, 12, 28)}>tốc độ chạy vòng</Tag>
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Mặt Trời hút" b="sao Trái Đất không rơi vào?" />
    <Orb f={f} R={270} pull />
    <Big x={CX + 300} y={560} size={130} color={AM} o={0.9 * sp(f, 12, 28)}>?</Big>
  </g>
);
// --- Cảnh 2: quả bóng buộc dây ---
const P4: Panel = ({f}) => (
  <g>
    <Head a="Vì Trái Đất" b="đang chạy vòng quanh nó" />
    <Orb f={f} R={270} speed={0.06} pull />
    <Hero2 f={f} />
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Như quay quả bóng" b="buộc dây" />
    <Ball f={f} x={CX} y={820} />
    <Tag x={CX} y={1170} color={AM} size={44} o={sp(f, 12, 26)}>dây kéo bóng vào tay</Tag>
    <Hero2 f={f} />
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Mặt Trời càng nặng" b="Trái Đất phải chạy càng nhanh" />
    <Orb f={f} R={270} speed={0.04} sunR={50} />
    <Orb f={f} R={270} speed={0.04} sunR={50} />
    <Sun cx={CX} cy={820} r={sp(f, 6, 30) * 40 + 50} />
    <Tag x={CX} y={1200} color={AM} size={44} o={sp(f, 20, 36)}>nặng hơn, chạy nhanh hơn</Tag>
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Tốc độ Trái Đất" b="cho biết Mặt Trời nặng bao nhiêu" />
    <Calc f={f} y={760} step={190} lines={[{t: 'tốc độ', at: 2, size: 120, color: AM}, {t: '→ khối lượng', at: 14, size: 110}]} />
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 3: ba con số ---
const P8: Panel = ({f}) => (
  <g>
    <Head a="Quy luật hút" b="do Niu-tơn tìm ra" />
    <Big x={CX} y={820} size={190} color={AM} o={sp(f, 4, 18)}>1687</Big>
    <Tag x={CX} y={980} color={C.cream} size={46} o={sp(f, 12, 26)}>năm xuất bản sách</Tag>
    <Hero2 f={f} />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Cần 3 con số" b="Thứ nhất: khoảng cách" />
    <Orb f={f} R={240} speed={0.03} />
    <Arrow x1={CX} y1={820} x2={CX + 240} y2={820} color={AM} w={7} p={sp(f, 6, 22)} />
    <Big x={CX} y={1210} size={80} color={AM} o={sp(f, 12, 28)}>150 triệu km</Big>
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Thứ hai: một vòng" b="là 1 năm" />
    <Orb f={f} R={240} speed={0.1} />
    <Big x={CX} y={1210} size={74} color={AM} o={sp(f, 10, 26)}>365 ngày và ¼</Big>
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Thứ ba là G" b="độ mạnh của lực hút" />
    <Big x={CX} y={820} size={300} color={AM} o={sp(f, 2, 16)}>G</Big>
    <Hero2 f={f} />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="G rất nhỏ" b="khoảng 6,7 phần 100 tỉ" />
    <Big x={CX} y={820} size={96} color={AM} o={sp(f, 2, 16)}>G ≈ 0,000 000 000 067</Big>
    <Tag x={CX} y={1000} color={C.cream} size={44} o={sp(f, 14, 28)}>6,7 phần 100 tỉ</Tag>
  </g>
);
const P13: Panel = ({f}) => {
  const a = Math.sin(f * 0.08) * 0.25;
  const bx = (cx: number, s: number) => cx + 90 * s;
  return (
    <g>
      <Head a="Năm 1798, Ca-ven-đít" b="dùng cân xoắn để ra G" />
      <g transform={`rotate(${a * 57} ${CX} 760)`}>
        <line x1={CX - 190} y1={760} x2={CX + 190} y2={760} stroke={C.cream} strokeWidth={8} />
        <circle cx={CX - 190} cy={760} r={34} fill={RED} stroke={C.cream} strokeWidth={4} />
        <circle cx={CX + 190} cy={760} r={34} fill={RED} stroke={C.cream} strokeWidth={4} />
      </g>
      <line x1={CX} y1={560} x2={CX} y2={760} stroke={C.cream} strokeWidth={4} />
      <circle cx={bx(CX, -2.8)} cy={880} r={64} fill="#6a6f86" stroke={C.cream} strokeWidth={5} opacity={sp(f, 6, 20)} />
      <circle cx={bx(CX, 2.8)} cy={640} r={64} fill="#6a6f86" stroke={C.cream} strokeWidth={5} opacity={sp(f, 6, 20)} />
      <Tag x={CX} y={1160} color={AM} size={44} o={sp(f, 16, 30)}>cân xoắn</Tag>
    </g>
  );
};
// --- Cảnh 4: tính tốc độ ---
const P14: Panel = ({f}) => (
  <g>
    <Head a="Độ dài một vòng" />
    <Calc f={f} y={740} step={160} lines={[{t: '2 × 3,14 × 150 triệu', at: 2, size: 78}, {t: '≈ 940 triệu km', at: 14, size: 110, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Một năm" b="đổi ra giây" />
    <Calc f={f} y={780} step={170} lines={[{t: '1 năm', at: 2, size: 120}, {t: '≈ 31,6 triệu giây', at: 12, size: 100, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Tốc độ" b="bằng quãng đường chia thời gian" />
    <Calc f={f} y={780} step={170} lines={[{t: '940 triệu', at: 2, size: 120}, {t: '÷ 31,6 triệu', at: 12, size: 120, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Kết quả" />
    <Big x={CX} y={800} size={130} color={AM} o={sp(f, 4, 18)}>≈ 29,8 km/s</Big>
    <Hero2 f={f} cheer={sp(f, 10, 26)} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Mỗi giây gần 30 km" b="mà ta không hề cảm thấy" />
    <Orb f={f} R={260} speed={0.12} />
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 5: tính khối lượng ---
const P19: Panel = ({f}) => (
  <g>
    <Head a="Công thức" b="khối lượng Mặt Trời" />
    <Calc f={f} y={740} step={170} lines={[{t: 'M = v × v × r', at: 2, size: 110, color: AM}, {t: '÷ G', at: 14, size: 120}]} />
    <Tag x={CX} y={1130} color={C.cream} size={42} o={sp(f, 20, 34)}>v: tốc độ, r: khoảng cách</Tag>
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Đổi ra mét" />
    <Calc f={f} y={780} step={170} lines={[{t: '29,8 km/s', at: 2, size: 110}, {t: '= 29 800 m/s', at: 12, size: 110, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Nhân tốc độ" b="với chính nó" />
    <Calc f={f} y={780} step={170} lines={[{t: '29 800 × 29 800', at: 2, size: 90}, {t: '≈ 888 triệu', at: 12, size: 120, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Nhân với khoảng cách" b="150 tỉ mét" />
    <Calc f={f} y={780} step={170} lines={[{t: '888 triệu × 150 tỉ', at: 2, size: 84}, {t: '≈ 133 tỉ tỉ', at: 12, size: 120, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P23: Panel = ({f}) => (
  <g>
    <Head a="Chia cho G" />
    <Calc f={f} y={740} step={170} lines={[{t: '133 tỉ tỉ ÷ G', at: 2, size: 100}, {t: '≈ 2 × 10³⁰ kg', at: 12, size: 120, color: AM}]} />
    <Hero2 f={f} cheer={sp(f, 14, 30)} />
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Tức khoảng" b="2 tỉ tỉ tỉ tấn" />
    <Sun cx={CX} cy={760} r={sp(f, 2, 24) * 120} />
    <Big x={CX} y={1090} size={96} color={AM} o={sp(f, 14, 30)}>2 000 000 000 000 000 000 000 000 000 tấn</Big>
  </g>
);
// --- Cảnh 6: kết ---
const P25: Panel = ({f}) => (
  <g>
    <Head a="So với Trái Đất" b="nặng gấp khoảng 333 nghìn lần" />
    <Sun cx={CX} cy={760} r={190} o={sp(f, 2, 16)} />
    <Ear cx={CX + 330} cy={1010} r={16} />
    <Big x={CX} y={1170} size={110} color={AM} o={sp(f, 14, 30)}>× 333 000</Big>
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Chạy nhanh gấp đôi" b="Mặt Trời nặng gấp 4" />
    <Calc f={f} y={780} step={170} lines={[{t: 'tốc độ × 2', at: 2, size: 120}, {t: 'khối lượng × 4', at: 12, size: 120, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P27: Panel = ({f}) => (
  <g>
    <Head a="Cùng cách ấy cân được" b="vật có vật khác chạy quanh" />
    <Orb f={f} R={190} speed={0.1} sunR={50} cy={640} />
    <Orb f={f} R={190} speed={0.07} sunR={40} cy={1000} />
    <Hero2 f={f} />
  </g>
);
const P28: Panel = ({f}) => (
  <g>
    <Head a="Mặt Trời nặng 2 tỉ tỉ tỉ tấn" b="nhờ Trái Đất chạy 30 km/s" />
    <Orb f={f} R={250} speed={0.07} />
    <Hero2 f={f} cheer={sp(f, 8, 24)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28];
void lerp;
