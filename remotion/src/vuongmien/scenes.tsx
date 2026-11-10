import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, clamp01, seg, sp} from '../lib/theme';
import {Big, Hero, Lab, Svg, lerp} from '../eratosthenes/v';
import {Dial, Head, Ship, Tag, Waves, mkV} from '../kinhdo/scenes';

export type Sc = {dur: number; bs: number[]};
const GOLD = '#e9b94a';
const SILV = '#c9d3dc';
const WATER = '#2f8aa3';
void Dial; void Ship; void Waves;

const Crown: React.FC<{x: number; y: number; s?: number; o?: number}> = ({x, y, s = 1, o = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} opacity={clamp01(o)} stroke={C.cream} strokeWidth={4 / s} strokeLinejoin="round">
    <path d="M -120 0 L -120 -90 L -70 -40 L -30 -120 L 0 -50 L 30 -120 L 70 -40 L 120 -90 L 120 0 Z" fill={GOLD} />
    <rect x={-120} y={0} width={240} height={26} rx={6} fill="#c79a30" />
    {[-90, -30, 30, 90].map((cx) => (
      <circle key={cx} cx={cx} cy={13} r={7} fill="#c0392b" />
    ))}
  </g>
);
const Block: React.FC<{x: number; y: number; w: number; h: number; color: string; o?: number}> = ({x, y, w, h, color, o = 1}) => (
  <rect x={x - w / 2} y={y - h} width={w} height={h} rx={8} fill={color} stroke={C.cream} strokeWidth={4} opacity={clamp01(o)} />
);
const Beaker: React.FC<{x: number; y: number; w?: number; h?: number; level?: number; over?: number; f?: number}> = ({x, y, w = 200, h = 260, level = 0.8, over = 0, f = 0}) => (
  <g>
    <rect x={x - w / 2 + 6} y={y - h * level} width={w - 12} height={h * level} fill={WATER} opacity={0.75} />
    <path d={`M ${x - w / 2} ${y - h} L ${x - w / 2} ${y} L ${x + w / 2} ${y} L ${x + w / 2} ${y - h}`} fill="none" stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
    {over > 0 && (
      <g opacity={clamp01(over)}>
        <path d={`M ${x + w / 2} ${y - h} q 22 6 24 40 L ${x + w / 2 + 24} ${y}`} fill="none" stroke={WATER} strokeWidth={8 * clamp01(over) + 2} />
        {[0, 1, 2].map((i) => (
          <circle key={i} cx={x + w / 2 + 24} cy={y - 60 + ((f * 3 + i * 22) % 60)} r={5} fill={WATER} />
        ))}
      </g>
    )}
  </g>
);
const Balance: React.FC<{x: number; y: number; tilt: number; left?: React.ReactNode; right?: React.ReactNode}> = ({x, y, tilt, left, right}) => {
  const L = 230;
  const r = (tilt * Math.PI) / 180;
  const lx = x - L * Math.cos(r);
  const ly = y - L * Math.sin(r);
  const rx = x + L * Math.cos(r);
  const ry = y + L * Math.sin(r);
  return (
    <g stroke={C.cream} strokeWidth={6} strokeLinecap="round" fill="none">
      <path d={`M ${x} ${y} L ${x} ${y + 360}`} />
      <path d={`M ${x - 90} ${y + 360} L ${x + 90} ${y + 360}`} />
      <path d={`M ${lx} ${ly} L ${rx} ${ry}`} />
      <circle cx={x} cy={y} r={12} fill={GOLD} />
      <path d={`M ${lx} ${ly} L ${lx - 70} ${ly + 120} L ${lx + 70} ${ly + 120} Z`} strokeWidth={4} />
      <path d={`M ${rx} ${ry} L ${rx - 70} ${ry + 120} L ${rx + 70} ${ry + 120} Z`} strokeWidth={4} />
      <line x1={lx - 90} y1={ly + 120} x2={lx + 90} y2={ly + 120} />
      <line x1={rx - 90} y1={ry + 120} x2={rx + 90} y2={ry + 120} />
      <g transform={`translate(${lx} ${ly + 120})`} stroke="none">{left}</g>
      <g transform={`translate(${rx} ${ry + 120})`} stroke="none">{right}</g>
    </g>
  );
};
const SB = (a: number, b: number) => (f: number) => sp(f, a, b);

// ============ 1. Mở đầu ============
export const Hook: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const bob = Math.sin(f * 0.07) * 8;
  const fill = 0.6 + 0.08 * Math.sin(f * 0.08);
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Vương miện vàng ròng" b="hay có trộn bạc?" />
        <Crown x={540} y={860 + bob} s={1.6} />
        <Lab x={760} y={620} size={110} color={C.amber} o={0.9 * sp(f, 20, 34)}>?</Lab>
        <Hero x={200} y={1200} s={1.8} walk={f * 0.25} />
        <Tag x={540} y={1240} color={C.cream} size={42}>làm sao biết mà không phá nó?</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Theo giai thoại" b="lời giải đến trong bồn tắm" />
        <path d="M 200 900 L 220 1130 Q 540 1190 860 1130 L 880 900 Z" fill="#6c4a32" stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
        <path d={`M 232 ${1000 - fill * 60} L 240 1100 Q 540 1150 840 1100 L 848 ${1000 - fill * 60} Z`} fill={WATER} opacity={0.8} />
        <Hero x={540 + Math.sin((f - b1) * 0.2) * 30} y={1010} s={1.7} walk={f * 0.25} cheer={sp(f, b1 + 10, b1 + 40)} />
        {[0, 1, 2, 3].map((i) => (
          <circle key={i} cx={216 + i * 6} cy={920 + ((f * 3 + i * 25) % 200)} r={6} fill={WATER} opacity={sp(f, b1 + 30, b1 + 44)} />
        ))}
      </g>
      <g opacity={V(2)}>
        <Head a="Nước tràn ra" b="cho biết vàng có pha bạc?" />
        <Beaker x={380} y={1130} h={300} level={0.95} over={sp(f, b2 + 8, b2 + 30)} f={f} />
        <Crown x={380} y={640 + seg(f, b2 + 4, b2 + 40) * 350} s={0.8} />
        <Lab x={760} y={820} size={130} color={C.amber} o={0.9 * sp(f, b2 + 40, b2 + 54)}>?</Lab>
        <Hero x={850} y={1180} s={1.6} walk={f * 0.25} />
      </g>
    </Svg>
  );
};

// ============ 2. Cân không đủ ============
export const Can: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2, b3] = bs;
  const wob = Math.sin(f * 0.2) * 4 * Math.exp(-(f % 400) / 40);
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Vương miện nặng đúng" b="bằng số vàng đã đưa" />
        <Balance x={540} y={700} tilt={wob} left={<Crown x={0} y={-8} s={0.5} />} right={<Block x={0} y={0} w={110} h={60} color={GOLD} />} />
        <Big x={540} y={1290} size={96} color={C.amber} o={sp(f, 20, 34)}>cân bằng</Big>
      </g>
      <g opacity={V(1)}>
        <Head a="Thay bớt vàng bằng bạc" b="cho đủ cân: cân không đổi" />
        <Balance x={540} y={700} tilt={Math.sin(f * 0.2) * 3 * Math.exp(-(f - b1) / 40)} left={<g><Block x={-30} y={0} w={60} h={60} color={GOLD} /><Block x={34} y={0} w={60} h={60} color={SILV} /></g>} right={<Block x={0} y={0} w={110} h={60} color={GOLD} />} />
        <Tag x={540} y={1250} color={C.cream} size={42} o={sp(f, b1 + 20, b1 + 34)}>vẫn cân bằng, ai cũng tưởng vàng</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Bạc nhẹ hơn vàng" b="cùng cân, bạc chiếm nhiều chỗ" />
        <Block x={300} y={1000} w={110} h={110} color={GOLD} />
        <Block x={700} y={1000} w={180} h={180} color={SILV} o={sp(f, b2 + 14, b2 + 30)} />
        <Tag x={300} y={1080} color={C.cream} size={40}>100 g vàng</Tag>
        <Tag x={700} y={1080} color={C.cream} size={40} o={sp(f, b2 + 18, b2 + 32)}>100 g bạc</Tag>
        <Hero x={540 + Math.sin(f * 0.1) * 16} y={780} s={1.6} walk={f * 0.25} />
      </g>
      <g opacity={V(3)}>
        <Head a="Đo xem nó chiếm" b="bao nhiêu chỗ" />
        <Crown x={330} y={900} s={1.0} />
        <Block x={740} y={900} w={150} h={110} color={GOLD} />
        <line x1={200} y1={1010} x2={460} y2={1010} stroke={C.amber} strokeWidth={6} opacity={sp(f, b3 + 10, b3 + 24)} />
        <line x1={660} y1={1010} x2={820} y2={1010} stroke={C.amber} strokeWidth={6} opacity={sp(f, b3 + 20, b3 + 34)} />
        <Lab x={540} y={1160} size={100} color={C.amber} o={0.9 * sp(f, b3 + 30, b3 + 44)}>?</Lab>
        <Tag x={540} y={1260} color={C.cream} size={40}>so với vàng ròng cùng cân</Tag>
      </g>
    </Svg>
  );
};

// ============ 3. Đo bằng nước ============
export const Nuoc: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Nhúng vào nước" b="chiếm chỗ bao nhiêu, đẩy nước bấy nhiêu" />
        <Beaker x={540} y={1150} h={320} level={0.9} over={sp(f, 40, 70)} f={f} />
        <Block x={540} y={760 + seg(f, 10, 50) * 300} w={120} h={90} color={GOLD} />
        <Hero x={190} y={1190} s={1.7} walk={f * 0.25} />
        <Tag x={540} y={1260} color={C.cream} size={40} o={sp(f, 50, 64)}>nước tràn = chỗ vật chiếm</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Hai khối cùng cân" b="vàng và bạc" />
        <Beaker x={300} y={1150} h={320} level={0.9} over={sp(f, b1 + 30, b1 + 50) * 0.6} f={f} />
        <Beaker x={760} y={1150} h={320} level={0.9} over={sp(f, b1 + 30, b1 + 50)} f={f} />
        <Block x={300} y={730 + seg(f, b1 + 8, b1 + 40) * 300} w={90} h={70} color={GOLD} />
        <Block x={760} y={700 + seg(f, b1 + 8, b1 + 40) * 330} w={140} h={110} color={SILV} />
        <Tag x={300} y={1260} color={C.cream} size={38} o={sp(f, b1 + 50, b1 + 64)}>vàng: tràn ít</Tag>
        <Tag x={760} y={1260} color={C.amber} size={38} o={sp(f, b1 + 50, b1 + 64)}>bạc: tràn nhiều</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Vương miện tràn nhiều hơn" b="khối vàng: có bạc" />
        <Beaker x={300} y={1150} h={320} level={0.9} over={sp(f, b2 + 20, b2 + 40) * 0.6} f={f} />
        <Beaker x={760} y={1150} h={320} level={0.9} over={sp(f, b2 + 20, b2 + 40)} f={f} />
        <Block x={300} y={730 + seg(f, b2 + 8, b2 + 40) * 300} w={110} h={80} color={GOLD} />
        <Crown x={760} y={780 + seg(f, b2 + 8, b2 + 40) * 280} s={0.55} />
        <Big x={540} y={620} size={110} color={C.amber} o={sp(f, b2 + 50, b2 + 64)}>có bạc!</Big>
        <Hero x={540} y={1190} s={1.4} walk={f * 0.25} />
      </g>
    </Svg>
  );
};

// ============ 4. Công thức, số liệu ============
const Bar: React.FC<{x: number; y: number; w: number; h?: number; color: string}> = ({x, y, w, h = 70, color}) => (
  <rect x={x} y={y} width={Math.max(2, w)} height={h} rx={10} fill={color} stroke={C.cream} strokeWidth={4} />
);
export const Cong: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2, b3, b4, b5] = bs;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Khối lượng riêng" b="1 cm³ nặng bao nhiêu gam?" />
        <Block x={300} y={950} w={130} h={130} color={GOLD} />
        <Block x={780} y={950} w={190} h={190} color={SILV} o={sp(f, 14, 28)} />
        <Big x={300} y={1100} size={90} color={C.amber} o={sp(f, 10, 24)}>19,3</Big>
        <Big x={780} y={1100} size={90} color={C.cream} o={sp(f, 24, 38)}>10,5</Big>
        <Tag x={300} y={1170} color={C.cream} size={36}>g mỗi cm³ (vàng)</Tag>
        <Tag x={780} y={1170} color={C.cream} size={36} o={sp(f, 28, 42)}>g mỗi cm³ (bạc)</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Công thức" />
        <Big x={540} y={720} size={96} color={C.cream} o={sp(f, b1 + 6, b1 + 20)}>thể tích =</Big>
        <Big x={540} y={880} size={100} color={C.amber} o={sp(f, b1 + 22, b1 + 36)}>khối lượng</Big>
        <Big x={540} y={1010} size={100} color={C.cream} o={sp(f, b1 + 38, b1 + 52)}>÷ khối lượng riêng</Big>
        <Hero x={200} y={1240} s={1.5} walk={f * 0.25} />
      </g>
      <g opacity={V(2)}>
        <Head a="Vương miện nặng 1 000 g" b="nếu là vàng ròng" />
        <Big x={540} y={760} size={96} color={C.cream} o={sp(f, b2 + 6, b2 + 20)}>1 000 ÷ 19,3</Big>
        <Big x={540} y={900} size={110} color={C.amber} o={sp(f, b2 + 24, b2 + 38)}>≈ 52 cm³</Big>
        <Bar x={110} y={1030} w={860 * 52 / 70 * seg(f, b2 + 30, b2 + 70)} color={GOLD} />
      </g>
      <g opacity={V(3)}>
        <Head a="Giả sử thay 30% vàng bằng bạc" />
        <Big x={540} y={720} size={84} color={C.cream} o={sp(f, b3 + 6, b3 + 20)}>700 ÷ 19,3 + 300 ÷ 10,5</Big>
        <Bar x={110} y={850} w={860 * 36.3 / 70 * seg(f, b3 + 20, b3 + 60)} color={GOLD} />
        <Bar x={110 + 860 * 36.3 / 70} y={850} w={860 * 28.6 / 70 * seg(f, b3 + 60, b3 + 100)} color={SILV} />
        <Tag x={300} y={980} color={C.cream} size={36}>vàng: 36,3</Tag>
        <Tag x={700} y={980} color={C.cream} size={36} o={sp(f, b3 + 70, b3 + 84)}>bạc: 28,6</Tag>
      </g>
      <g opacity={V(4)}>
        <Head a="≈ 65 cm³, lớn hơn" b="vàng ròng 13 cm³" />
        <Tag x={110} y={760} color={C.cream} size={38} anchor="start">vàng ròng</Tag>
        <Bar x={110} y={780} w={860 * 52 / 70} color={GOLD} />
        <Tag x={110} y={940} color={C.cream} size={38} anchor="start">vương miện</Tag>
        <Bar x={110} y={960} w={860 * 65 / 70 * seg(f, b4 + 6, b4 + 40)} color={SILV} />
        <rect x={110 + 860 * 52 / 70} y={955} width={860 * 13 / 70 * sp(f, b4 + 40, b4 + 54)} height={80} rx={6} fill="none" stroke={C.amber} strokeWidth={6} />
        <Big x={540} y={1200} size={110} color={C.amber} o={sp(f, b4 + 50, b4 + 64)}>+ 13 cm³</Big>
      </g>
      <g opacity={V(5)}>
        <Head a="13 ml nước, chậu rộng 20 cm" b="nước chỉ chênh 0,4 mm" />
        <rect x={110} y={900} width={860} height={260} fill={WATER} opacity={0.75} />
        <path d="M 110 800 L 110 1160 L 970 1160 L 970 800" fill="none" stroke={C.cream} strokeWidth={6} />
        <line x1={110} y1={900} x2={970} y2={900} stroke={C.cream} strokeWidth={3} strokeDasharray="12 10" />
        <rect x={110} y={892 - 8 * sp(f, b5 + 10, b5 + 40)} width={860} height={8 * sp(f, b5 + 10, b5 + 40)} fill={C.amber} opacity={0.9} />
        <Tag x={540} y={860} color={C.amber} size={40} o={sp(f, b5 + 30, b5 + 44)}>0,4 mm</Tag>
        <Tag x={540} y={1260} color={C.cream} size={38}>khó đo bằng mắt</Tag>
      </g>
    </Svg>
  );
};

// ============ 5. Galileo ============
export const Gal: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const tilt = (a: number) => a * sp(f, 10, 50);
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="1586: Ga-li-lê gọi" b="cách tràn nước là thô" />
        <Beaker x={540} y={1150} h={320} level={0.9} f={f} />
        <rect x={290} y={870} width={500} height={8} fill={C.amber} opacity={0.9} />
        <Tag x={540} y={820} color={C.amber} size={42}>chênh 0,4 mm</Tag>
        <Hero x={190 + Math.sin(f * 0.1) * 30} y={1190} s={1.7} walk={f * 0.25} />
        <Lab x={860} y={1000} size={96} color={C.amber} o={0.9 * sp(f, 24, 40)}>thô</Lab>
      </g>
      <g opacity={V(1)}>
        <Head a="Cân vật ngay trong nước" b="vật nhẹ đi" />
        <rect x={140} y={760} width={800} height={460} fill={WATER} opacity={0.5} />
        <path d="M 140 760 L 140 1220 L 940 1220 L 940 760" fill="none" stroke={C.cream} strokeWidth={6} />
        <line x1={540} y1={560} x2={540} y2={940} stroke={C.cream} strokeWidth={5} />
        <Block x={540} y={1000 + Math.sin(f * 0.12) * 4} w={140} h={100} color={SILV} />
        <Tag x={540} y={520} color={C.cream} size={38}>cân treo</Tag>
        <Tag x={540} y={1290} color={C.amber} size={40} o={sp(f, b1 + 30, b1 + 44)}>nhẹ đi = nước nó đẩy ra</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Trong nước, vương miện nhẹ" b="hơn khối vàng khoảng 13 g" />
        <rect x={110} y={780} width={860} height={440} fill={WATER} opacity={0.5} />
        <path d="M 110 780 L 110 1220 L 970 1220 L 970 780" fill="none" stroke={C.cream} strokeWidth={6} />
        <line x1={300} y1={560} x2={300} y2={900} stroke={C.cream} strokeWidth={5} />
        <line x1={780} y1={560} x2={780} y2={900 + 36 * sp(f, b2 + 20, b2 + 50)} stroke={C.cream} strokeWidth={5} />
        <Block x={300} y={1000} w={110} h={80} color={GOLD} />
        <Crown x={780} y={1000 + 36 * sp(f, b2 + 20, b2 + 50) - 20} s={0.5} />
        <Big x={540} y={1290} size={96} color={C.amber} o={sp(f, b2 + 50, b2 + 64)}>chênh 13 g</Big>
      </g>
    </Svg>
  );
};

// ============ 6. Ngày nay ============
export const Nay: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const sink = seg(f, 20, 70);
  const bobS = Math.sin(f * 0.08) * 6;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Kim hoàn cân hai lần" b="trong không khí, trong nước" />
        <line x1={300} y1={560} x2={300} y2={780} stroke={C.cream} strokeWidth={5} />
        <Block x={300} y={880} w={110} h={80} color={GOLD} />
        <Tag x={300} y={940} color={C.cream} size={36}>không khí</Tag>
        <rect x={600} y={880} width={300} height={260} fill={WATER} opacity={0.5} />
        <path d="M 600 880 L 600 1140 L 900 1140 L 900 880" fill="none" stroke={C.cream} strokeWidth={5} />
        <line x1={750} y1={560} x2={750} y2={960 + 20 * sink} stroke={C.cream} strokeWidth={5} />
        <Block x={750} y={1040 + 20 * sink} w={110} h={80} color={GOLD} />
        <Tag x={750} y={1190} color={C.cream} size={36}>trong nước</Tag>
        <Hero x={140} y={1290} s={1.4} walk={f * 0.25} />
      </g>
      <g opacity={V(1)}>
        <Head a="Tàu sắt vẫn nổi" b="đẩy ra nước nặng bằng cả tàu" />
        <rect x={0} y={1000} width={1080} height={260} fill={WATER} opacity={0.6} />
        <g transform={`translate(540 ${960 + bobS})`}>
          <path d="M -250 0 L 250 0 L 190 90 L -190 90 Z" fill="#6b707a" stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
          <line x1={0} y1={0} x2={0} y2={-170} stroke={C.cream} strokeWidth={6} />
          <path d="M 6 -165 L 120 -30 L 6 -30 Z" fill={C.cream} />
        </g>
        <path d={`M 540 1280 L 540 ${1130 - 30 * sp(f, b1 + 20, b1 + 40)}`} stroke={C.amber} strokeWidth={8} strokeLinecap="round" opacity={sp(f, b1 + 20, b1 + 34)} />
        <Tag x={700} y={1230} color={C.amber} size={38} o={sp(f, b1 + 24, b1 + 38)}>lực đẩy lên</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Chuyện bồn tắm chép lại" b="sau khoảng 200 năm" />
        <line x1={150} y1={820} x2={930} y2={820} stroke={C.cream} strokeWidth={6} strokeLinecap="round" />
        <circle cx={150} cy={820} r={14} fill={C.amber} />
        <circle cx={930} cy={820} r={14} fill={C.amber} />
        <Tag x={150} y={770} color={C.cream} size={38}>Ác-si-mét</Tag>
        <Tag x={930} y={770} color={C.cream} size={38}>người chép</Tag>
        <Big x={540} y={960} size={110} color={C.amber} o={sp(f, b2 + 24, b2 + 38)}>≈ 200 năm</Big>
        <Hero x={lerp(150, 930, seg(f, b2 + 10, b2 + 90))} y={1180} s={1.7} walk={f * 0.25} />
        <Tag x={540} y={1280} color={C.cream} size={40} o={sp(f, b2 + 70, b2 + 84)}>ý khoa học vẫn đúng</Tag>
      </g>
    </Svg>
  );
};
