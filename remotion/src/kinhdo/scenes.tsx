import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, clamp01, seg, sp} from '../lib/theme';
import {Big, Hero, Lab, MagMark, Svg, lerp} from '../eratosthenes/v';

export type Sc = {dur: number; bs: number[]};

const D = C.dim;
const RAD = Math.PI / 180;
const SEA = '#2f6f86';
const WOOD = '#8a5a34';

const mkV = (f: number, bs: number[]) => (i: number) =>
  sp(f, bs[i] + 2, bs[i] + 14) * (i < bs.length - 1 ? 1 - sp(f, bs[i + 1] - 10, bs[i + 1]) : 1);

const Head: React.FC<{a: string; b?: string}> = ({a, b}) => (
  <g>
    <Lab x={540} y={b ? 252 : 290} size={52} color={C.cream}>{a}</Lab>
    {b && (
      <Lab x={540} y={322} size={52} color={C.amber}>
        {b}
      </Lab>
    )}
  </g>
);

const Tag: React.FC<{x: number; y: number; children: React.ReactNode; color?: string; o?: number; size?: number; anchor?: 'start' | 'middle' | 'end'}> = ({x, y, children, color = D, o = 1, size = 36, anchor = 'middle'}) => (
  <Lab x={x} y={y} size={size} color={color} o={o} anchor={anchor}>
    {children}
  </Lab>
);

const Ship: React.FC<{x: number; y: number; s?: number; rot?: number; o?: number; dashed?: boolean}> = ({x, y, s = 1, rot = 0, o = 1, dashed = false}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`} opacity={clamp01(o)} stroke={C.cream} strokeWidth={5 / s} strokeLinejoin="round" strokeLinecap="round" strokeDasharray={dashed ? `${10 / s} ${12 / s}` : undefined}>
    <path d="M -90 0 L 90 0 L 60 42 L -60 42 Z" fill={dashed ? 'none' : WOOD} />
    <line x1={0} y1={0} x2={0} y2={-125} />
    <path d="M 6 -120 L 76 -22 L 6 -22 Z" fill={dashed ? 'none' : C.cream} fillOpacity={0.85} />
  </g>
);

const Waves: React.FC<{y: number; f: number; o?: number}> = ({y, f, o = 1}) => (
  <g opacity={o} stroke={SEA} strokeWidth={6} fill="none" strokeLinecap="round">
    {[0, 1, 2].map((r) => (
      <path key={r} d={Array.from({length: 11}, (_, i) => `${i ? 'L' : 'M'} ${40 + i * 100} ${y + r * 46 + Math.sin((i * 1.1 + f * 0.07 + r))* 10}`).join(' ')} />
    ))}
  </g>
);

const Dial: React.FC<{x: number; y: number; r?: number; hand: number; color?: string; o?: number; min?: number}> = ({x, y, r = 60, hand, color = C.cream, o = 1, min}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill={C.bg1} stroke={color} strokeWidth={5} />
    {Array.from({length: 12}, (_, i) => (
      <line key={i} x1={x + r * 0.82 * Math.sin(i * 30 * RAD)} y1={y - r * 0.82 * Math.cos(i * 30 * RAD)} x2={x + r * 0.94 * Math.sin(i * 30 * RAD)} y2={y - r * 0.94 * Math.cos(i * 30 * RAD)} stroke={color} strokeWidth={3} />
    ))}
    <line x1={x} y1={y} x2={x + r * 0.55 * Math.sin(hand * RAD)} y2={y - r * 0.55 * Math.cos(hand * RAD)} stroke={C.amber} strokeWidth={6} strokeLinecap="round" />
    {min !== undefined && <line x1={x} y1={y} x2={x + r * 0.78 * Math.sin(min * RAD)} y2={y - r * 0.78 * Math.cos(min * RAD)} stroke={C.cream} strokeWidth={4} strokeLinecap="round" />}
    <circle cx={x} cy={y} r={5} fill={C.amberDeep} />
  </g>
);

const Sunn: React.FC<{x: number; y: number; r: number; o?: number}> = ({x, y, r, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r * 1.7} fill="url(#sunGlow)" opacity={0.6} />
    <circle cx={x} cy={y} r={r} fill={C.amber} stroke={C.cream} strokeWidth={4} />
  </g>
);

const Rocks: React.FC<{x: number; y: number; o?: number}> = ({x, y, o = 1}) => (
  <g opacity={clamp01(o)} fill="#4b4036" stroke={C.cream} strokeWidth={4} strokeLinejoin="round">
    <path d={`M ${x - 120} ${y} L ${x - 80} ${y - 50} L ${x - 40} ${y - 15} L ${x} ${y - 70} L ${x + 50} ${y - 20} L ${x + 90} ${y - 55} L ${x + 130} ${y} Z`} />
  </g>
);

const Bar: React.FC<{x: number; y: number; w: number; h?: number; color: string; p?: number}> = ({x, y, w, h = 56, color, p = 1}) => (
  <rect x={x} y={y} width={Math.max(2, w * p)} height={h} rx={10} fill={color} stroke={C.cream} strokeWidth={4} />
);

// ============ 1. Mở đầu ============
export const Hook: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const bob = Math.sin(f * 0.08) * 8;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Năm 1714, nước Anh treo thưởng" b="20 000 bảng cho một câu hỏi" />
        <rect x={190} y={520} width={700} height={250} rx={24} fill={C.bg1} stroke={C.amber} strokeWidth={6} />
        <Big x={540} y={670} size={120} color={C.amber}>20 000 bảng</Big>
        <Waves y={1060} f={f} />
        <Ship x={540} y={1030 + bob} s={1.4} rot={Math.sin(f * 0.06) * 4} />
        <Lab x={540} y={900} size={96} color={C.cream} o={sp(f, 30, 44)}>?</Lab>
        <Tag x={540} y={1240} color={C.cream} size={42}>tàu của tôi đang ở đâu?</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Người giải được không phải" b="nhà thiên văn, mà là thợ mộc" />
        <rect x={250} y={1010} width={580} height={36} rx={6} fill={WOOD} stroke={C.cream} strokeWidth={4} />
        <Hero x={540} y={1010} s={2.4} walk={f * 0.12} />
        <Tag x={540} y={1180} color={C.cream} size={44}>một người thợ mộc</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Lời giải là một chiếc đồng hồ" b="vì sao nó cho biết tàu ở đâu?" />
        <Dial x={540} y={820} r={190} hand={f * 4} min={f * 24} />
        <Lab x={540} y={1130} size={120} color={C.amber} o={0.9 * sp(f, b2 + 20, b2 + 34)}>?</Lab>
        <Ship x={540} y={1240} s={0.8} />
      </g>
    </Svg>
  );
};

// ============ 2. Vĩ độ, kinh độ ============
export const Globe: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2, b3] = bs;
  const gx = 540;
  const gy = 840;
  const R = 250;
  const spin = (f - b1) * 1.2;
  const eq = 360 * 0 + seg(f, b1 + 30, b1 + 70);
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Vĩ độ: tàu ở phía bắc hay nam" b="đo dễ bằng góc Mặt Trời" />
        <line x1={110} y1={1180} x2={970} y2={1180} stroke={C.cream} strokeWidth={4} opacity={0.5} />
        <Sunn x={780} y={640} r={70} />
        <Hero x={300} y={1180} s={2.6} />
        <line x1={300} y1={1000} x2={780} y2={640} stroke={C.amber} strokeWidth={4} strokeDasharray="10 14" opacity={sp(f, 14, 30)} />
        <line x1={300} y1={1000} x2={620} y2={1000} stroke={C.cream} strokeWidth={4} opacity={0.5} />
        <path d="M 440 1000 A 140 140 0 0 0 413 918" fill="none" stroke={C.amber} strokeWidth={6} opacity={sp(f, 24, 38)} />
        <Tag x={470} y={960} color={C.amber} size={40} o={sp(f, 28, 42)}>góc</Tag>
        <Tag x={540} y={1260} color={C.cream} size={40}>giữa trưa</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Kinh độ cần giờ ở cảng nhà" b="vì Trái Đất tự quay" />
        <circle cx={gx} cy={gy - 50} r={R * 0.7} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
        {[-0.5, 0, 0.5].map((k, i) => (
          <ellipse key={i} cx={gx + Math.sin(spin * RAD) * 0} cy={gy - 50} rx={R * 0.7 * Math.abs(Math.cos((spin + i * 60) * RAD))} ry={R * 0.7} fill="none" stroke={C.cream} strokeWidth={3} opacity={0.5} />
        ))}
        <Tag x={gx} y={1030} color={C.amber} size={40}>quay một vòng trong 24 giờ</Tag>
        <Big x={540} y={1150} size={84} color={C.cream} o={sp(f, b1 + 30, b1 + 44)}>360° ÷ 24 giờ</Big>
        <Big x={540} y={1250} size={96} color={C.amber} o={sp(f, b1 + 60, b1 + 74)}>= 15° mỗi giờ</Big>
      </g>
      <g opacity={V(2)}>
        <Head a="Trên tàu đang giữa trưa" b="đồng hồ nhà chỉ 3 giờ chiều" />
        <Sunn x={270} y={600} r={50} />
        <Dial x={270} y={800} r={110} hand={0} min={0} />
        <Tag x={270} y={970} color={C.cream} size={36}>trên tàu: 12 giờ</Tag>
        <Dial x={810} y={800} r={110} hand={90} min={0} />
        <Tag x={810} y={970} color={C.cream} size={36}>đồng hồ nhà: 3 giờ</Tag>
        <Big x={540} y={1090} size={92} color={C.cream} o={sp(f, b2 + 24, b2 + 38)}>3 giờ × 15° = 45°</Big>
        <Tag x={540} y={1190} color={C.amber} size={46} o={sp(f, b2 + 60, b2 + 74)}>tàu ở phía tây cảng nhà 45°</Tag>
      </g>
      <g opacity={V(3)}>
        <Head a="Đồng hồ sai chỉ 1 phút" b="tàu đã lạc khoảng 28 km" />
        <Dial x={540} y={640} r={120} hand={0} min={seg(f, b3 + 10, b3 + 60) * 6} />
        <line x1={110} y1={950} x2={970} y2={950} stroke={C.cream} strokeWidth={10} strokeLinecap="round" />
        <line x1={110} y1={920} x2={110} y2={980} stroke={C.amber} strokeWidth={8} />
        <line x1={970} y1={920} x2={970} y2={980} stroke={C.amber} strokeWidth={8} />
        <Ship x={lerp(150, 880, seg(f, b3 + 30, b3 + 90))} y={880} s={0.6} />
        <Big x={540} y={1090} size={100} color={C.amber} o={sp(f, b3 + 50, b3 + 64)}>1 phút ≈ 28 km</Big>
        <Tag x={540} y={1180} color={D} size={34}>(ở xích đạo)</Tag>
      </g>
    </Svg>
  );
};

// ============ 3. Tai nạn 1707 ============
export const Wreck: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const sail = seg(f, 0, b1);
  const hit = seg(f, b2 + 10, b2 + 50);
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Năm 1707, một hạm đội Anh" b="chạy về nước và lạc đường" />
        <Tag x={190} y={560} color={D} size={34}>Gi-bran-ta</Tag>
        <Tag x={890} y={560} color={D} size={34}>nước Anh</Tag>
        <Waves y={1000} f={f} />
        {[0, 1, 2].map((i) => (
          <Ship key={i} x={lerp(150 + i * 60, 760 + i * 60, sail)} y={900 + i * 60 + Math.sin(f * 0.07 + i) * 6} s={0.55} />
        ))}
        <Lab x={540} y={1250} size={44} color={C.cream}>không ai biết chắc mình ở đâu</Lab>
      </g>
      <g opacity={V(1)}>
        <Head a="Đô đốc tin tàu còn ở phía nam" b="quần đảo Scilly" />
        <Rocks x={540} y={760} />
        <Tag x={540} y={820} color={C.cream} size={34}>quần đảo Scilly</Tag>
        <Ship x={540} y={1170} s={0.6} dashed o={sp(f, b1 + 10, b1 + 26)} />
        <Tag x={540} y={1240} color={C.cream} size={34} o={sp(f, b1 + 14, b1 + 30)}>vị trí tin</Tag>
        <Ship x={540} y={980} s={0.6} o={sp(f, b1 + 44, b1 + 60)} />
        <Tag x={800} y={990} color={C.amber} size={34} o={sp(f, b1 + 50, b1 + 66)}>vị trí thật</Tag>
        <Waves y={1040} f={f} o={0.5} />
      </g>
      <g opacity={V(2)}>
        <Head a="Tàu lệch xa về phía bắc, đâm vào đá" b="bốn chiến hạm vỡ tan" />
        <Rocks x={540} y={900} />
        <Ship x={540} y={880 + hit * 30} s={0.9} rot={hit * 28} o={1 - hit * 0.45} />
        <Waves y={1000} f={f} />
        <Big x={540} y={1180} size={110} color={C.amber} o={sp(f, b2 + 50, b2 + 66)}>hơn 1 400</Big>
        <Tag x={540} y={1250} color={C.cream} size={44} o={sp(f, b2 + 50, b2 + 66)}>người thiệt mạng</Tag>
      </g>
    </Svg>
  );
};

// ============ 4. Đồng hồ trên sóng ============
export const Clockk: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const rock = Math.sin(f * 0.12) * 7;
  const pend = Math.sin(f * 0.55) * 30 + Math.sin(f * 1.7) * 18;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Cần đồng hồ chạy đúng nhiều tuần" b="nhưng sóng làm quả lắc chạy loạn" />
        <g transform={`rotate(${rock} 540 1050)`}>
          <rect x={390} y={600} width={300} height={440} rx={26} fill={C.bg1} stroke={C.cream} strokeWidth={6} />
          <circle cx={540} cy={710} r={70} fill="none" stroke={C.cream} strokeWidth={5} />
          <line x1={540} y1={710} x2={540} y2={665} stroke={C.amber} strokeWidth={6} strokeLinecap="round" />
          <g transform={`rotate(${pend} 540 790)`}>
            <line x1={540} y1={790} x2={540} y2={960} stroke={C.cream} strokeWidth={6} />
            <circle cx={540} cy={975} r={30} fill={C.amberDeep} stroke={C.cream} strokeWidth={4} />
          </g>
        </g>
        <Waves y={1120} f={f} />
        <Tag x={540} y={1260} color={C.cream} size={40}>đồng hồ quả lắc trên tàu lắc</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Mức thưởng cao nhất:" b="tàu lạc không quá nửa độ" />
        <Big x={540} y={700} size={130} color={C.amber}>20 000 bảng</Big>
        <Dial x={300} y={950} r={100} hand={0} min={seg(f, b1 + 30, b1 + 70) * 12} />
        <Tag x={300} y={1120} color={C.cream} size={38}>sai không quá</Tag>
        <Big x={760} y={980} size={110} color={C.amber} o={sp(f, b1 + 36, b1 + 50)}>2 phút</Big>
        <Tag x={760} y={1060} color={D} size={34} o={sp(f, b1 + 40, b1 + 54)}>(nửa độ)</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Người nhận thử thách: John Harrison" b="sinh năm 1693, một thợ mộc" />
        <Hero x={380} y={1060} s={2.5} walk={f * 0.1} />
        <rect x={560} y={940} width={320} height={120} rx={14} fill={WOOD} stroke={C.cream} strokeWidth={4} />
        <Dial x={720} y={820} r={70} hand={f * 3} min={f * 18} />
        <Tag x={540} y={1200} color={C.cream} size={42}>làm đồng hồ lúc rảnh</Tag>
      </g>
    </Svg>
  );
};

// ============ 5. Đồng hồ Harrison ============
export const Harr: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const days = Math.round(81 * seg(f, b2 + 14, b2 + 80));
  const rs = [105, 90, 75, 44];
  const xs = [190, 400, 600, 820];
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Bốn chiếc đồng hồ đi biển" b="nhỏ dần qua từng chiếc" />
        {rs.map((r, i) => (
          <g key={i} opacity={sp(f, 6 + i * 12, 20 + i * 12)}>
            <Dial x={xs[i]} y={860} r={r} hand={f * 2 + i * 40} min={f * 12} />
          </g>
        ))}
        <Tag x={395} y={1060} color={C.cream} size={38} o={sp(f, 50, 64)}>ba chiếc đầu: cỗ máy lớn</Tag>
        <Tag x={820} y={1000} color={C.amber} size={38} o={sp(f, 54, 68)}>thứ tư: bỏ túi</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Tháng 11 năm 1761" b="từ Portsmouth đi Jamaica" />
        <Tag x={170} y={620} color={C.cream} size={36}>Portsmouth</Tag>
        <Tag x={900} y={620} color={C.cream} size={36}>Jamaica</Tag>
        <line x1={170} y1={680} x2={900} y2={680} stroke={C.cream} strokeWidth={4} strokeDasharray="10 16" opacity={0.5} />
        <Waves y={960} f={f} />
        <Ship x={lerp(170, 880, seg(f, b1 + 10, b1 + 110))} y={880} s={0.8} />
        <Tag x={540} y={1200} color={C.amber} size={42}>con trai ông trông giữ đồng hồ</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Sau 81 ngày, tàu cập bến" b="đồng hồ chỉ chậm 5 giây" />
        <Big x={540} y={700} size={140} color={C.amber}>{`${days} ngày`}</Big>
        <Dial x={300} y={960} r={100} hand={0} min={0} />
        <Dial x={780} y={960} r={100} hand={0} min={-0.8} color={C.amber} o={sp(f, b2 + 70, b2 + 84)} />
        <Tag x={300} y={1130} color={C.cream} size={36}>giờ đúng</Tag>
        <Tag x={780} y={1130} color={C.amber} size={36} o={sp(f, b2 + 70, b2 + 84)}>đồng hồ H4: chậm 5 giây</Tag>
      </g>
    </Svg>
  );
};

// ============ 6. Tính sai số ============
export const Err: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="5 giây là 1/12 phút" b="nên 28 km ÷ 12 ≈ 2,3 km" />
        <Big x={540} y={680} size={110} color={C.cream} o={sp(f, 8, 22)}>5 giây = 1/12 phút</Big>
        <Big x={540} y={860} size={110} color={C.cream} o={sp(f, 34, 48)}>28 ÷ 12 ≈</Big>
        <Big x={540} y={1010} size={150} color={C.amber} o={sp(f, 60, 74)}>2,3 km</Big>
      </g>
      <g opacity={V(1)}>
        <Head a="Mức cho phép: 55 km" b="Sai số thật: 2,3 km" />
        <Tag x={110} y={650} color={C.cream} size={36} anchor="start">mức cho phép</Tag>
        <Bar x={110} y={680} w={860} color={C.bg1} p={seg(f, b1 + 6, b1 + 40)} />
        <Big x={540} y={730} size={60} color={C.cream} o={sp(f, b1 + 30, b1 + 44)}>55 km</Big>
        <Tag x={110} y={900} color={C.amber} size={36} anchor="start">sai số của Harrison</Tag>
        <Bar x={110} y={930} w={36} color={C.amber} p={sp(f, b1 + 40, b1 + 56)} />
        <Big x={420} y={980} size={60} color={C.amber} o={sp(f, b1 + 50, b1 + 64)}>2,3 km</Big>
        <Tag x={540} y={1150} color={C.cream} size={44} o={sp(f, b1 + 66, b1 + 80)}>nhỏ hơn hơn 20 lần</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Hội đồng vẫn đòi thử thêm" b="đến năm 1773 mới trả khoản cuối" />
        <Hero x={300} y={1000} s={2} walk={0} />
        <Hero x={540} y={1000} s={2.2} walk={0} />
        <Hero x={780} y={1000} s={1.9} walk={0} />
        <Lab x={540} y={760} size={90} color={C.amber} o={0.9}>? ? ?</Lab>
        <Tag x={540} y={1120} color={D} size={36}>hội đồng chấm giải</Tag>
        <Big x={540} y={1240} size={120} color={C.amber} o={sp(f, b2 + 40, b2 + 56)}>1773</Big>
      </g>
    </Svg>
  );
};

// ============ 7. Ngày nay + kết ============
export const Now: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs.slice(0, 3));
  const [, b1, b2, e] = bs;
  const fade = 1 - sp(f, e, e + 18);
  const lg = sp(f, e + 6, e + 28);
  const dot = seg(f % 60, 0, 60);
  return (
    <Svg>
      <g opacity={fade}>
        <g opacity={V(0)}>
          <Head a="Ý tưởng ấy sống trong điện thoại" b="vệ tinh GPS mang đồng hồ nguyên tử" />
          <g transform="translate(540 640)" stroke={C.cream} strokeWidth={5} strokeLinejoin="round">
            <rect x={-40} y={-30} width={80} height={60} rx={8} fill={C.bg1} />
            <rect x={-170} y={-18} width={110} height={36} fill={C.amberDeep} />
            <rect x={60} y={-18} width={110} height={36} fill={C.amberDeep} />
          </g>
          <Tag x={540} y={735} color={C.cream} size={34}>vệ tinh GPS</Tag>
          <line x1={540} y1={760} x2={540} y2={1060} stroke={C.amber} strokeWidth={3} strokeDasharray="8 14" opacity={0.5} />
          <circle cx={540} cy={lerp(760, 1060, dot)} r={13} fill={C.amber} />
          <rect x={470} y={1070} width={140} height={230} rx={22} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
          <Tag x={540} y={1340} color={C.cream} size={34}>điện thoại tính thời gian tín hiệu bay</Tag>
        </g>
        <g opacity={V(1)}>
          <Head a="Đồng hồ sai 1 phần tỉ giây" b="vị trí lệch khoảng 30 cm" />
          <line x1={110} y1={780} x2={970} y2={780} stroke={C.cream} strokeWidth={14} strokeLinecap="round" />
          <line x1={110} y1={750} x2={110} y2={810} stroke={C.amber} strokeWidth={8} />
          <line x1={970} y1={750} x2={970} y2={810} stroke={C.amber} strokeWidth={8} />
          <Big x={540} y={700} size={100} color={C.amber}>30 cm</Big>
          <Tag x={540} y={930} color={C.cream} size={42}>ánh sáng đi trong</Tag>
          <Big x={540} y={1040} size={84} color={C.amber}>1 phần tỉ giây</Big>
        </g>
        <g opacity={V(2)}>
          <Head a="Mang theo giờ của nhà" b="là biết mình đang ở đâu" />
          <Dial x={300} y={840} r={120} hand={f * 3} min={f * 18} />
          <Ship x={760} y={880} s={1.1} rot={Math.sin(f * 0.06) * 4} />
          <g opacity={sp(f, b2 + 20, b2 + 34)}><circle cx={760} cy={690} r={26} fill={C.amber} stroke={C.cream} strokeWidth={4} /><path d="M 760 760 L 744 706 L 776 706 Z" fill={C.amber} stroke={C.cream} strokeWidth={4} strokeLinejoin="round" /></g>
          <Waves y={980} f={f} />
          <Hero x={540} y={1250} s={1.6} cheer={sp(f, b2 + 40, b2 + 60)} walk={f * 0.3} stick={false} />
        </g>
      </g>
      <g opacity={lg} transform={`translate(0 ${(1 - lg) * 20})`}>
        <g transform="translate(465 700) scale(3.4)">
          <MagMark size={44} raw />
        </g>
        <text x={540} y={930} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={74} fill={C.cream}>
          Người <tspan fill={C.amber}>Giải Mã</tspan>
        </text>
        <Lab x={540} y={1010} size={38} color={C.cream}>Biết tàu ở đâu giữa biển nhờ một chiếc đồng hồ.</Lab>
      </g>
    </Svg>
  );
};
