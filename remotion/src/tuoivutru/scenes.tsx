import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const GAL = '#c9b8ff';
const RAISIN = '#6b3a5a';
const DOUGH = '#e1b06b';
const RED = '#e0613b';
const AM = C.amber;
const CX = 540;

const Hero2: React.FC<{f: number; x?: number; cheer?: number}> = ({f, x = 170, cheer = 0}) => <HatHero x={x} y={1250} s={2} walk={f * 0.13} cheer={cheer} hat="goggles" />;

// Số khoa học: mantissa × 10^exp (viết mũ bằng tspan để khỏi lệ thuộc phông).
const Sci: React.FC<{x: number; y: number; size: number; m: string; e: string; color?: string; o?: number; suffix?: string}> = ({x, y, size, m, e, color = AM, o = 1, suffix = ''}) => (
  <text x={x} y={y} textAnchor="middle" fontFamily="Cormorant" fontWeight={600} fontSize={size} fill={color} opacity={clamp01(o)} stroke={C.bg2} strokeWidth={size * 0.06} paintOrder="stroke" style={{fontVariantNumeric: 'lining-nums'}}>
    {m} × 10<tspan dy={-size * 0.4} fontSize={size * 0.6}>{e}</tspan>
    {suffix && <tspan dy={size * 0.4}>{suffix}</tspan>}
  </text>
);

const Gal: React.FC<{x: number; y: number; r?: number; o?: number; rot?: number}> = ({x, y, r = 26, o = 1, rot = 0}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot})`} opacity={clamp01(o)} fill="none" stroke={GAL} strokeWidth={5} strokeLinecap="round">
    <path d={`M 0 0 Q ${r * 0.5} ${-r * 0.8} ${r} 0`} />
    <path d={`M 0 0 Q ${-r * 0.5} ${r * 0.8} ${-r} 0`} />
    <circle r={r * 0.2} fill="#fff" stroke="none" />
  </g>
);
const Raisin: React.FC<{x: number; y: number; r?: number}> = ({x, y, r = 14}) => <circle cx={x} cy={y} r={r} fill={RAISIN} stroke={C.cream} strokeWidth={3} />;

// Ổ bánh mì: k = độ nở (1..1.8). Hạt nho cố định theo tỉ lệ nên xa nhau dần.
const SPOTS: [number, number][] = [[-0.6, -0.3], [-0.1, -0.5], [0.5, -0.2], [-0.4, 0.3], [0.2, 0.25], [0.65, 0.4]];
const Loaf: React.FC<{k: number; cy?: number}> = ({k, cy = 820}) => (
  <g>
    <ellipse cx={CX + 60} cy={cy} rx={190 * k} ry={120 * k} fill={DOUGH} stroke={C.cream} strokeWidth={6} />
    {SPOTS.map(([a, b], i) => (
      <Raisin key={i} x={CX + 60 + a * 160 * k} y={cy + b * 100 * k} />
    ))}
  </g>
);

// --- Cảnh 1: câu hỏi ---
const P0: Panel = ({f}) => (
  <g>
    <Head a="Vũ trụ bao nhiêu tuổi" b="khi không ai đếm nổi?" />
    {[[420, 700, 40], [700, 640, 30], [560, 900, 50], [800, 960, 34], [380, 1010, 28]].map(([x, y, r], i) => (
      <Gal key={i} x={x} y={y} r={r} o={sp(f, 2 + i * 4, 16 + i * 4)} rot={f * 0.8 + i * 40} />
    ))}
    <Big x={CX + 330} y={620} size={150} color={AM} o={0.9 * sp(f, 24, 40)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Ta xem phim" b="chạy ngược" />
    <rect x={300} y={600} width={660} height={400} rx={24} fill="none" stroke={C.cream} strokeWidth={6} />
    {[0, 1, 2, 3, 4].map((i) => (
      <rect key={i} x={300 + 20 + i * 132} y={560} width={60} height={26} fill={C.cream} opacity={0.5} />
    ))}
    <Big x={CX + 60} y={850} size={190} color={AM} o={sp(f, 6, 22)}>◀◀</Big>
    <Hero2 f={f} />
  </g>
);
const P2: Panel = ({f}) => {
  const k = 1 + 0.01 * f;
  return (
    <g>
      <Head a="Thiên hà đang bay xa nhau" b="tốc độ cho biết thời gian" />
      {[[-1, -1], [1, -1], [-1, 1], [1, 1], [0, -1.4], [0, 1.4]].map(([a, b], i) => (
        <g key={i}>
          <Gal x={CX + 60 + a * 200 * k} y={850 + b * 150 * k} r={28} rot={f * 1.2 + i * 50} />
          <Arrow x1={CX + 60 + a * 120 * k} y1={850 + b * 90 * k} x2={CX + 60 + a * 175 * k} y2={850 + b * 130 * k} color={RED} p={sp(f, 8, 26)} w={6} />
        </g>
      ))}
      <Hero2 f={f} />
    </g>
  );
};
// --- Cảnh 2: bánh mì hạt nho ---
const P3: Panel = ({f}) => (
  <g>
    <Head a="Ổ bánh mì nhiều hạt nho" b="đang nở ra" />
    <Loaf k={1 + 0.5 * sp(f, 10, 90)} />
    <Hero2 f={f} />
  </g>
);
const P4: Panel = ({f}) => {
  const k = 1 + 0.6 * sp(f, 6, 80);
  const x1 = CX + 60 + SPOTS[1][0] * 160 * k, y1 = 820 + SPOTS[1][1] * 100 * k;
  const x2 = CX + 60 + SPOTS[2][0] * 160 * k, y2 = 820 + SPOTS[2][1] * 100 * k;
  const x3 = CX + 60 + SPOTS[5][0] * 160 * k, y3 = 820 + SPOTS[5][1] * 100 * k;
  return (
    <g>
      <Head a="Hạt nho càng xa nhau" b="càng rời nhau nhanh" />
      <Loaf k={k} />
      <Arrow x1={x2} y1={y2 - 30} x2={x2 + 40} y2={y2 - 30} color={AM} p={sp(f, 20, 36)} w={6} />
      <Arrow x1={x3} y1={y3 + 30} x2={x3 + 110} y2={y3 + 30} color={RED} p={sp(f, 26, 44)} w={7} />
      <Tag x={CX + 60} y={1130} color={AM} size={42} o={sp(f, 40, 56)}>xa hơn, chạy nhanh hơn</Tag>
      <Hero2 f={f} />
      <g opacity={0}><circle cx={x1} cy={y1} r={1} /></g>
    </g>
  );
};
const P5: Panel = ({f}) => (
  <g>
    <Head a="Thiên hà cũng vậy" b="càng xa ta, càng chạy nhanh" />
    <circle cx={CX - 160} cy={850} r={22} fill="#4a8fe0" stroke={C.cream} strokeWidth={4} />
    <Tag x={CX - 160} y={915} color={C.cream} size={36}>ta</Tag>
    <Gal x={CX + 40} y={850} r={26} rot={f} />
    <Arrow x1={CX + 40} y1={780} x2={CX + 110} y2={780} color={AM} p={sp(f, 8, 24)} w={6} />
    <Gal x={CX + 380} y={850} r={30} rot={f * 1.1} />
    <Arrow x1={CX + 300} y1={780} x2={CX + 440} y2={780} color={RED} p={sp(f, 16, 38)} w={8} />
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 3: Hubble và công thức ---
const P6: Panel = ({f}) => (
  <g>
    <Head a="Edwin Hubble" b="tìm ra điều ấy" />
    <Big x={CX + 60} y={830} size={210} color={AM} o={sp(f, 2, 18)}>1929</Big>
    <Hero2 f={f} />
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Hai năm trước" b="Lemaître đi tới kết luận tương tự" />
    <Big x={CX + 60} y={830} size={210} color={AM} o={sp(f, 2, 18)}>1927</Big>
    <Hero2 f={f} />
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Hubble viết" />
    <Big x={CX + 60} y={720} size={100} color={C.cream} o={sp(f, 2, 14)}>tốc độ =</Big>
    <Big x={CX + 60} y={880} size={110} color={AM} o={sp(f, 14, 28)}>H × khoảng cách</Big>
    <Hero2 f={f} />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="H là hằng số" b="khoảng 70 hiện nay" />
    <Big x={CX + 60} y={760} size={170} color={AM} o={sp(f, 2, 16)}>H ≈ 70</Big>
    <Tag x={CX + 60} y={880} color={C.cream} size={44} o={sp(f, 14, 28)}>km mỗi giây</Tag>
    <Tag x={CX + 60} y={950} color={C.cream} size={44} o={sp(f, 20, 34)}>trên mỗi mê-ga-pác-xéc (Mpc)</Tag>
    <Hero2 f={f} />
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="1 mê-ga-pác-xéc (Mpc)" b="là một khoảng cách" />
    <Big x={CX + 60} y={780} size={130} color={AM} o={sp(f, 2, 16)}>3,26 triệu</Big>
    <Tag x={CX + 60} y={890} color={C.cream} size={50} o={sp(f, 12, 26)}>năm ánh sáng</Tag>
    <Hero2 f={f} />
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Tức khoảng" b="30,9 tỉ tỉ ki-lô-mét" />
    <Sci x={CX + 60} y={800} size={120} m="3,09" e="19" suffix=" km" o={sp(f, 2, 18)} />
    <Hero2 f={f} />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Thiên hà cách 1 Mpc" b="chạy xa khoảng 70 km/s" />
    <Gal x={CX - 100} y={850} r={30} rot={f} />
    <Arrow x1={CX - 20} y1={850} x2={CX + 330} y2={850} color={RED} p={sp(f, 10, 36)} w={9} />
    <Big x={CX + 120} y={780} size={90} color={AM} o={sp(f, 24, 40)}>70 km/s</Big>
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 4: chiếu phim ngược, tính tuổi ---
const P13: Panel = ({f}) => (
  <g>
    <Head a="Chiếu phim ngược" b="thời gian = quãng đường ÷ tốc độ" />
    <Calc f={f} x={CX + 60} y={760} step={140} lines={[{t: 'thời gian', at: 2, size: 110}, {t: '= quãng đường ÷ tốc độ', at: 16, size: 76, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Xe 60 km/h, cách nhà 120 km" b="đã rời nhà 2 giờ trước" />
    <Calc f={f} x={CX + 60} y={760} step={150} lines={[{t: '120 ÷ 60', at: 2, size: 130}, {t: '= 2 giờ', at: 24, size: 150, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Với thiên hà ấy" b="chia khoảng cách cho tốc độ" />
    <Sci x={CX + 60} y={760} size={110} m="3,09" e="19" suffix=" km" o={sp(f, 2, 16)} />
    <Big x={CX + 60} y={880} size={110} color={C.cream} o={sp(f, 14, 28)}>÷ 70 km/s</Big>
    <Hero2 f={f} />
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Đổi thành giây" b="một con số rất lớn" />
    <Sci x={CX + 60} y={800} size={150} m="4,41" e="17" suffix=" giây" o={sp(f, 2, 18)} />
    <Hero2 f={f} />
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Đổi ra năm" b="1 năm ≈ 31,6 triệu giây" />
    <Big x={CX + 60} y={800} size={120} color={AM} o={sp(f, 2, 18)}>1 năm</Big>
    <Big x={CX + 60} y={950} size={120} color={C.cream} o={sp(f, 14, 30)}>≈ 31,6 triệu giây</Big>
    <Hero2 f={f} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Chia cho 31,6 triệu" b="ra khoảng 14 tỉ năm" />
    <Sci x={CX + 60} y={700} size={90} m="4,41" e="17" suffix=" ÷ 31,6 triệu" o={sp(f, 2, 14)} color={C.cream} />
    <Big x={CX + 60} y={900} size={150} color={AM} o={sp(f, 22, 38)}>≈ 14 tỉ năm</Big>
    <Hero2 f={f} cheer={sp(f, 30, 50)} />
  </g>
);
// --- Cảnh 5: mọi thiên hà cho cùng kết quả ---
const P19: Panel = ({f}) => (
  <g>
    <Head a="Thiên hà nào cũng" b="cho cùng kết quả" />
    {[[-1, -0.6], [1, -0.4], [-0.5, 0.8], [0.9, 0.9]].map(([a, b], i) => (
      <g key={i} opacity={sp(f, 4 + i * 8, 16 + i * 8)}>
        <Gal x={CX + 60 + a * 230} y={800 + b * 160} r={28} rot={f + i * 40} />
        <Tag x={CX + 60 + a * 230} y={800 + b * 160 + 70} color={AM} size={38}>14 tỉ năm</Tag>
      </g>
    ))}
    <Hero2 f={f} />
  </g>
);
const P20: Panel = ({f}) => {
  const k = 1 - 0.92 * sp(f, 8, 80);
  return (
    <g>
      <Head a="Mọi thứ từng ở cùng một chỗ" b="khoảng 14 tỉ năm trước" />
      {[[-1, -0.7], [1, -0.5], [-0.7, 0.9], [0.8, 1], [0, -1.1], [0, 1.2]].map(([a, b], i) => (
        <Gal key={i} x={CX + 60 + a * 260 * k} y={830 + b * 170 * k} r={28 * (0.4 + 0.6 * k)} rot={f + i * 40} />
      ))}
      <Hero2 f={f} />
    </g>
  );
};
const P21: Panel = ({f}) => (
  <g>
    <Head a="Tốc độ giãn nở có đổi" b="con số tốt nhất là 13,8 tỉ năm" />
    <Big x={CX + 60} y={830} size={170} color={AM} o={sp(f, 2, 18)}>13,8 tỉ</Big>
    <Tag x={CX + 60} y={950} color={C.cream} size={50} o={sp(f, 14, 28)}>năm tuổi</Tag>
    <Hero2 f={f} />
  </g>
);
// --- Cảnh 6: H đầu tiên của Hubble ---
const P22: Panel = ({f}) => (
  <g>
    <Head a="H đầu tiên của Hubble" b="lớn gấp hơn 7 lần bây giờ" />
    <rect x={CX - 160} y={1100 - 400 * sp(f, 4, 30)} width={140} height={400 * sp(f, 4, 30)} fill={RED} stroke={C.cream} strokeWidth={4} />
    <rect x={CX + 60} y={1100 - 56 * sp(f, 14, 40)} width={140} height={56 * sp(f, 14, 40)} fill={AM} stroke={C.cream} strokeWidth={4} />
    <Big x={CX - 90} y={680} size={90} color={RED} o={sp(f, 20, 34)}>500</Big>
    <Big x={CX + 130} y={980} size={90} color={AM} o={sp(f, 26, 40)}>70</Big>
    <Hero2 f={f} />
  </g>
);
const P23: Panel = ({f}) => (
  <g>
    <Head a="Với H = 500" b="vũ trụ chỉ khoảng 2 tỉ năm" />
    <Big x={CX + 60} y={800} size={190} color={RED} o={sp(f, 2, 18)}>2 tỉ</Big>
    <Tag x={CX + 60} y={920} color={C.cream} size={50} o={sp(f, 12, 26)}>năm tuổi?</Tag>
    <Hero2 f={f} />
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Đo lại khoảng cách" b="chính xác hơn" />
    <Big x={CX + 60} y={760} size={150} color={RED} o={1 - sp(f, 20, 36)}>H = 500</Big>
    <Arrow x1={CX + 60} y1={820} x2={CX + 60} y2={960} color={C.cream} p={sp(f, 10, 30)} />
    <Big x={CX + 60} y={1090} size={150} color={AM} o={sp(f, 20, 38)}>H ≈ 70</Big>
    <Hero2 f={f} />
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Tuổi vũ trụ tăng" b="chỉ nhờ đo lại khoảng cách" />
    <Big x={CX - 120} y={830} size={130} color={RED} o={sp(f, 2, 16)}>2 tỉ</Big>
    <Arrow x1={CX + 70} y1={800} x2={CX + 210} y2={800} color={C.cream} p={sp(f, 12, 30)} />
    <Big x={CX + 360} y={830} size={130} color={AM} o={sp(f, 22, 38)}>14 tỉ</Big>
    <Tag x={CX + 60} y={960} color={C.cream} size={46} o={sp(f, 30, 44)}>năm</Tag>
    <Hero2 f={f} />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Từ tốc độ các thiên hà" b="biết vũ trụ gần 14 tỉ năm tuổi" />
    {[[-1, -0.7], [1, -0.5], [-0.7, 0.9], [0.8, 1], [0, -1.1]].map(([a, b], i) => (
      <Gal key={i} x={CX + 60 + a * 230 * (1 + 0.005 * f)} y={820 + b * 160 * (1 + 0.005 * f)} r={28} rot={f + i * 40} />
    ))}
    <Hero2 f={f} cheer={sp(f, 8, 26)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26];
void lerp;
