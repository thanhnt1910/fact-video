import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const RED = '#e0613b';
const AM = C.amber;
const CX = 540;

const Hero2: React.FC<{f: number; cheer?: number}> = ({f, cheer = 0}) => <HatHero x={170} y={1250} s={2} walk={f * 0.13} cheer={cheer} hat="gear" />;

// Màu thanh sắt nung theo độ nóng h (0 đỏ sẫm .. 1 trắng).
const STOPS = ['#8a2a1c', '#e0613b', '#f0a040', '#fff1d0'];
const mix = (a: string, b: string, t: number) => {
  const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
  const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
  return `rgb(${pa.map((v, i) => Math.round(v + (pb[i] - v) * t)).join(',')})`;
};
const heat = (h: number) => {
  const k = clamp01(h) * 3;
  const i = Math.min(2, Math.floor(k));
  return mix(STOPS[i], STOPS[i + 1], k - i);
};
const Iron: React.FC<{x: number; y: number; h: number; w?: number; o?: number}> = ({x, y, h, w = 520, o = 1}) => (
  <g opacity={o}>
    <circle cx={x + w / 2} cy={y} r={50 + 40 * h} fill={heat(h)} opacity={0.1 + 0.08 * h} />
    <rect x={x} y={y - 28} width={w} height={56} rx={28} fill={heat(h)} stroke={C.cream} strokeWidth={5} />
  </g>
);
const Sun: React.FC<{x: number; y: number; r: number; f: number; o?: number}> = ({x, y, r, f, o = 1}) => (
  <g opacity={o}>
    {Array.from({length: 12}).map((_, i) => {
      const a = (i / 12) * Math.PI * 2 + f * 0.01;
      return <line key={i} x1={x + Math.cos(a) * (r + 14)} y1={y + Math.sin(a) * (r + 14)} x2={x + Math.cos(a) * (r + 40 + 8 * Math.sin(f * 0.12 + i))} y2={y + Math.sin(a) * (r + 40 + 8 * Math.sin(f * 0.12 + i))} stroke={AM} strokeWidth={7} strokeLinecap="round" />;
    })}
    <circle cx={x} cy={y} r={r} fill="#f0a040" stroke={C.cream} strokeWidth={6} />
  </g>
);
const Star: React.FC<{x: number; y: number; r: number; color: string; f: number}> = ({x, y, r, color, f}) => (
  <g>
    <circle cx={x} cy={y} r={r * 1.7 + 4 * Math.sin(f * 0.1)} fill={color} opacity={0.15} />
    <circle cx={x} cy={y} r={r} fill={color} stroke={C.cream} strokeWidth={5} />
  </g>
);
const Grad: React.FC = () => (
  <defs>
    <linearGradient id="nmHeat" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stopColor="#8a2a1c" />
      <stop offset="0.4" stopColor="#e0613b" />
      <stop offset="0.7" stopColor="#f0a040" />
      <stop offset="1" stopColor="#fff1d0" />
    </linearGradient>
    <linearGradient id="nmRain" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stopColor="#8b2bd6" />
      <stop offset="0.25" stopColor="#2b6fd6" />
      <stop offset="0.5" stopColor="#3fc46a" />
      <stop offset="0.75" stopColor="#e8c52b" />
      <stop offset="1" stopColor="#e0402b" />
    </linearGradient>
  </defs>
);
// Đồ thị phổ: đường cong có đỉnh; p = tiến độ vẽ.
const GX0 = 340;
const GX1 = 940;
const GY = 1160;
const Spectrum: React.FC<{p: number; mark?: number}> = ({p, mark = 0}) => {
  const pts: string[] = [];
  for (let i = 0; i <= 60; i++) {
    const t = i / 60;
    const y = GY - 330 * Math.exp(-Math.pow((t - 0.5) / 0.2, 2)) * (t < 0.5 ? 1 : 1) - 8 * t;
    pts.push(`${i ? 'L' : 'M'} ${lerp(GX0, GX1, t)} ${y}`);
  }
  return (
    <g>
      <Grad />
      <line x1={GX0} y1={GY} x2={GX1} y2={GY} stroke={C.cream} strokeWidth={5} />
      <rect x={GX0} y={GY + 14} width={GX1 - GX0} height={26} rx={6} fill="url(#nmRain)" opacity={0.8} />
      <path d={pts.join(' ')} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - clamp01(p)} fill="none" stroke={AM} strokeWidth={8} strokeLinecap="round" />
      <g opacity={mark}>
        <line x1={lerp(GX0, GX1, 0.5)} y1={GY - 340} x2={lerp(GX0, GX1, 0.5)} y2={GY + 40} stroke={RED} strokeWidth={5} strokeDasharray="12 10" />
        <circle cx={lerp(GX0, GX1, 0.5)} cy={GY - 338} r={13} fill={RED} stroke={C.cream} strokeWidth={4} />
      </g>
    </g>
  );
};

const P0: Panel = ({f}) => (
  <g>
    <Head a="Không ai mang nhiệt kế" b="tới Mặt Trời" />
    <Sun x={720} y={800} r={120} f={f} />
    <g opacity={sp(f, 4, 18)}>
      <rect x={425} y={650} width={34} height={280} rx={17} fill="none" stroke={C.cream} strokeWidth={6} />
      <circle cx={442} cy={955} r={34} fill={RED} stroke={C.cream} strokeWidth={6} />
      <rect x={433} y={760} width={18} height={190} rx={9} fill={RED} />
    </g>
    <g opacity={sp(f, 22, 36)} stroke={RED} strokeWidth={14} strokeLinecap="round">
      <line x1={370} y1={640} x2={520} y2={1010} />
      <line x1={520} y1={640} x2={370} y2={1010} />
    </g>
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Bí mật nằm ở" b="màu sắc" />
    <Grad />
    <rect x={340} y={800} width={600} height={90} rx={16} fill="url(#nmHeat)" stroke={C.cream} strokeWidth={5} opacity={sp(f, 2, 16)} />
    <Arrow x1={340} y1={980} x2={940} y2={980} color={AM} p={sp(f, 14, 44)} />
    <Tag x={CX + 100} y={1060} color={AM} size={46} o={sp(f, 30, 44)}>nhiệt độ tăng dần</Tag>
    <Hero2 f={f} />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Nhìn ánh sáng" b="đọc nhiệt độ từ rất xa" />
    <Sun x={860} y={800} r={60} f={f} />
    <Arrow x1={780} y1={800} x2={460} y2={800} color={AM} p={sp(f, 8, 40)} />
    <circle cx={420} cy={800} r={24} fill={C.cream} stroke={AM} strokeWidth={5} />
    <circle cx={420} cy={800} r={9} fill={C.ink} />
    <Tag x={CX + 150} y={730} color={C.cream} size={40} o={sp(f, 20, 34)}>ánh sáng</Tag>
    <Hero2 f={f} />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Thanh sắt" b="trong lò rèn" />
    <rect x={460} y={820} width={440} height={260} rx={24} fill="#3a2a26" stroke={C.cream} strokeWidth={6} />
    {[0, 1, 2].map((i) => <path key={i} d={`M ${560 + i * 100} 1070 q ${-20 + 8 * Math.sin(f * 0.2 + i)} -70 10 -110 q 40 40 20 110 Z`} fill={i === 1 ? '#f0a040' : RED} opacity={0.85} />)}
    <rect x={340} y={930} width={420} height={44} rx={22} fill="#7a7a80" stroke={C.cream} strokeWidth={5} />
    <Hero2 f={f} />
  </g>
);
const P4: Panel = ({f}) => (
  <g>
    <Head a="Mới nung" b="đỏ sẫm" />
    <Iron x={340} y={800} h={0.05 + 0.1 * sp(f, 0, 30)} w={600} />
    <Big x={CX + 100} y={1060} size={120} color={AM} o={sp(f, 8, 22)}>700–800 °C</Big>
    <Hero2 f={f} />
  </g>
);
const P5: Panel = ({f}) => (
  <g>
    <Head a="Nung thêm" b="màu cam" />
    <Iron x={340} y={800} h={0.2 + 0.3 * sp(f, 0, 30)} w={600} />
    <Big x={CX + 100} y={1060} size={120} color={AM} o={sp(f, 8, 22)}>≈ 1.000 °C</Big>
    <Hero2 f={f} />
  </g>
);
const P6: Panel = ({f}) => (
  <g>
    <Head a="Nóng hơn nữa" b="sáng trắng" />
    <Iron x={340} y={800} h={0.6 + 0.4 * sp(f, 0, 30)} w={600} />
    <Big x={CX + 100} y={1060} size={120} color={AM} o={sp(f, 8, 22)}>từ 1.300 °C</Big>
    <Hero2 f={f} />
  </g>
);
const P7: Panel = ({f}) => (
  <g>
    <Head a="Càng nóng" b="càng chuyển từ đỏ sang trắng" />
    <Grad />
    <rect x={340} y={800} width={600} height={90} rx={16} fill="url(#nmHeat)" stroke={C.cream} strokeWidth={5} />
    <circle cx={lerp(380, 900, sp(f, 4, 50))} cy={845} r={22} fill={C.cream} stroke={C.ink} strokeWidth={5} />
    <Arrow x1={340} y1={980} x2={940} y2={980} color={AM} p={sp(f, 4, 50)} />
    <Tag x={CX + 100} y={1060} color={AM} size={44} o={sp(f, 30, 44)}>nóng hơn</Tag>
    <Hero2 f={f} />
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Nhà vật lý Đức" b="biến điều này thành công thức" />
    <Big x={CX + 100} y={820} size={200} color={AM} o={sp(f, 2, 18)}>1893</Big>
    <Tag x={CX + 100} y={950} color={C.cream} size={60} o={sp(f, 14, 28)}>Wilhelm Wien</Tag>
    <Hero2 f={f} />
  </g>
);
const P9: Panel = ({f}) => (
  <g>
    <Head a="Rồi giải Nobel Vật lý" b="cho khám phá về bức xạ nhiệt" />
    <Big x={CX + 100} y={820} size={200} color={AM} o={sp(f, 2, 18)}>1911</Big>
    <Tag x={CX + 100} y={950} color={C.cream} size={56} o={sp(f, 14, 28)}>giải Nobel Vật lý</Tag>
    <Hero2 f={f} cheer={sp(f, 10, 28) * 0.6} />
  </g>
);
const P10: Panel = ({f}) => (
  <g>
    <Head a="Định luật Wien" />
    <Calc f={f} x={CX + 100} y={760} step={140} lines={[{t: 'bước sóng sáng nhất', at: 2, size: 84}, {t: '= hằng số ÷ nhiệt độ', at: 24, size: 84, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const wave = (x0: number, x1: number, y: number, amp: number, len: number, ph: number) => {
  let d = '';
  for (let x = x0; x <= x1; x += 6) d += `${x === x0 ? 'M' : 'L'} ${x} ${y + amp * Math.sin(((x - x0) / len) * Math.PI * 2 - ph)} `;
  return d;
};
const P11: Panel = ({f}) => (
  <g>
    <Head a="Bước sóng" b="là độ dài một sóng ánh sáng" />
    <path d={wave(340, 940, 800, 40, 240, f * 0.1)} fill="none" stroke="#e0402b" strokeWidth={8} opacity={sp(f, 2, 14)} />
    <Tag x={CX + 100} y={730} color="#e0402b" size={38} o={sp(f, 6, 18)}>đỏ: sóng dài</Tag>
    <path d={wave(340, 940, 1000, 40, 90, f * 0.2)} fill="none" stroke="#2b6fd6" strokeWidth={8} opacity={sp(f, 20, 32)} />
    <Tag x={CX + 100} y={930} color="#6fa0f0" size={38} o={sp(f, 24, 36)}>xanh: sóng ngắn</Tag>
    <Hero2 f={f} />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Đơn vị nano-mét" />
    <Big x={CX + 100} y={820} size={160} color={AM} o={sp(f, 2, 18)}>1 nm</Big>
    <Tag x={CX + 100} y={940} color={C.cream} size={44} o={sp(f, 14, 28)}>một phần triệu mi-li-mét</Tag>
    <Hero2 f={f} />
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Hằng số ấy là" />
    <Big x={CX + 100} y={820} size={140} color={AM} o={sp(f, 2, 18)}>2.898.000</Big>
    <Tag x={CX + 100} y={940} color={C.cream} size={46} o={sp(f, 14, 28)}>nano-mét × kelvin</Tag>
    <Hero2 f={f} />
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Kelvin" b="bắt đầu từ độ không tuyệt đối" />
    <Big x={CX + 100} y={830} size={170} color={AM} o={sp(f, 2, 18)}>0 K</Big>
    <Tag x={CX + 100} y={950} color={C.cream} size={46} o={sp(f, 14, 28)}>độ không tuyệt đối</Tag>
    <Hero2 f={f} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Đổi từ độ C sang kelvin" b="cộng khoảng 273" />
    <Calc f={f} x={CX + 100} y={780} step={150} lines={[{t: '0 °C ≈ 273 K', at: 2, size: 110}, {t: 'K = °C + 273', at: 24, size: 120, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Thử với thanh sắt" b="1.000 độ C" />
    <Iron x={340} y={800} h={0.5} w={600} />
    <Big x={CX + 100} y={1060} size={120} color={AM} o={sp(f, 8, 22)}>1.000 °C</Big>
    <Hero2 f={f} />
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Cộng 273" />
    <Calc f={f} x={CX + 100} y={760} step={150} lines={[{t: '1.000 + 273', at: 2, size: 120}, {t: '= 1.273 K', at: 22, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Lấy hằng số" b="chia cho nhiệt độ" />
    <Calc f={f} x={CX + 100} y={760} step={150} lines={[{t: '2.898.000', at: 2, size: 130}, {t: '÷ 1.273', at: 22, size: 130, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Ra khoảng" />
    <Big x={CX + 100} y={830} size={160} color={AM} o={sp(f, 2, 18)}>2.300 nm</Big>
    <Hero2 f={f} />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Dài hơn nhiều so với đỏ" b="vùng mắt không thấy" />
    <Grad />
    <rect x={340} y={820} width={260} height={70} rx={10} fill="url(#nmRain)" stroke={C.cream} strokeWidth={5} />
    <Tag x={470} y={940} color={C.cream} size={34}>mắt thấy</Tag>
    <Arrow x1={610} y1={855} x2={930} y2={855} color={AM} p={sp(f, 6, 40)} />
    <Tag x={820} y={800} color={AM} size={42} o={sp(f, 30, 44)}>2.300 nm</Tag>
    <Tag x={800} y={940} color={RED} size={34} o={sp(f, 34, 48)}>mắt không thấy</Tag>
    <Hero2 f={f} />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Mắt chỉ bắt được" b="phần đuôi màu đỏ" />
    <Iron x={340} y={800} h={0.2} w={600} />
    <Tag x={CX + 100} y={1050} color={C.cream} size={46} o={sp(f, 8, 22)}>nên sắt trông đỏ rực</Tag>
    <Hero2 f={f} />
  </g>
);
const P22: Panel = ({f}) => (
  <g>
    <Head a="Giờ đến Mặt Trời" b="tách ánh sáng thành từng màu" />
    <path d="M 700 720 L 820 920 L 580 920 Z" fill="#bfe3f0" fillOpacity={0.25} stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
    <line x1={340} y1={860} x2={640} y2={830} stroke={C.cream} strokeWidth={8} strokeLinecap="round" opacity={sp(f, 2, 14)} />
    {['#8b2bd6', '#2b6fd6', '#3fc46a', '#e8c52b', '#e0402b'].map((c, i) => (
      <line key={i} x1={770} y1={830} x2={lerp(770, 960, sp(f, 14 + i * 3, 36 + i * 3))} y2={lerp(830, 740 + i * 50, sp(f, 14 + i * 3, 36 + i * 3))} stroke={c} strokeWidth={9} strokeLinecap="round" />
    ))}
    <Hero2 f={f} />
  </g>
);
const P23: Panel = ({f}) => (
  <g>
    <Head a="Xem màu nào" b="mạnh nhất" />
    <Spectrum p={sp(f, 2, 50)} />
    <Tag x={CX + 100} y={760} color={C.cream} size={38} o={sp(f, 20, 34)}>độ mạnh của từng màu</Tag>
    <Hero2 f={f} />
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Mạnh nhất ở khoảng" b="500 nano-mét, màu lục" />
    <Spectrum p={1} mark={sp(f, 4, 20)} />
    <Tag x={CX + 100} y={760} color={AM} size={48} o={sp(f, 14, 28)}>≈ 500 nm</Tag>
    <Hero2 f={f} />
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Lấy hằng số" b="chia cho 500" />
    <Calc f={f} x={CX + 100} y={800} step={150} lines={[{t: '2.898.000 ÷ 500', at: 2, size: 100, color: C.cream}]} />
    <Hero2 f={f} />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Nhiệt độ bề mặt" b="Mặt Trời" />
    <Big x={CX + 100} y={830} size={160} color={AM} o={sp(f, 2, 18)}>≈ 5.800 K</Big>
    <Hero2 f={f} />
  </g>
);
const P27: Panel = ({f}) => (
  <g>
    <Head a="Đổi sang độ C" b="trừ khoảng 273" />
    <Calc f={f} x={CX + 100} y={760} step={150} lines={[{t: '5.800 − 273', at: 2, size: 120}, {t: '≈ 5.500 °C', at: 22, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P28: Panel = ({f}) => (
  <g>
    <Head a="Gần với giá trị" b="NASA ghi" />
    <Big x={CX + 100} y={830} size={160} color={AM} o={sp(f, 2, 18)}>5.772 K</Big>
    <Tag x={CX + 100} y={950} color={C.cream} size={40} o={sp(f, 14, 28)}>sát số vừa tính</Tag>
    <Hero2 f={f} />
  </g>
);
const P29: Panel = ({f}) => (
  <g>
    <Head a="Bề mặt Mặt Trời" b="không có ranh giới rõ" />
    <defs>
      <radialGradient id="nmSunG" cx="50%" cy="50%" r="50%">
        <stop offset="0.55" stopColor="#f0a040" stopOpacity={1} />
        <stop offset="1" stopColor="#f0a040" stopOpacity={0} />
      </radialGradient>
    </defs>
    <circle cx={CX + 160} cy={850} r={220 + 8 * Math.sin(f * 0.1)} fill="url(#nmSunG)" opacity={sp(f, 2, 18)} />
    <Hero2 f={f} />
  </g>
);
const P30: Panel = ({f}) => (
  <g>
    <Head a="Nên sách ghi quanh" />
    <Big x={CX + 100} y={830} size={120} color={AM} o={sp(f, 2, 18)}>5.700 – 6.000 K</Big>
    <Hero2 f={f} />
  </g>
);
const P31: Panel = ({f}) => (
  <g>
    <Head a="Cũng nhờ cách ấy" b="đo nhiệt độ các ngôi sao" />
    <Star x={430} y={850} r={34} color="#e0613b" f={f} />
    <Star x={640} y={780} r={42} color="#f0c040" f={f + 10} />
    <Star x={850} y={870} r={36} color="#8fb8ff" f={f + 20} />
    <Hero2 f={f} />
  </g>
);
const P32: Panel = ({f}) => (
  <g>
    <Head a="Sao sáng nhất ở bước sóng ngắn" b="thì nóng hơn Mặt Trời" />
    <Star x={470} y={850} r={40} color="#f0c040" f={f} />
    <Tag x={470} y={960} color={C.cream} size={34}>Mặt Trời</Tag>
    <Star x={820} y={850} r={64} color="#8fb8ff" f={f + 12} />
    <Tag x={820} y={990} color={AM} size={36} o={sp(f, 12, 26)}>nóng hơn</Tag>
    <Arrow x1={560} y1={850} x2={720} y2={850} color={AM} p={sp(f, 4, 24)} />
    <Hero2 f={f} />
  </g>
);
const P33: Panel = ({f}) => (
  <g>
    <Head a="Không ai chạm tới" b="màu ánh sáng cho biết" />
    <Sun x={CX + 160} y={780} r={90} f={f} />
    <Big x={CX + 100} y={1040} size={150} color={AM} o={sp(f, 6, 22)}>≈ 5.800 K</Big>
    <Hero2 f={f} cheer={sp(f, 10, 28)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30, P31, P32, P33];
void lerp;
