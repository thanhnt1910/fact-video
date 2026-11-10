import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, clamp01, seg, sp} from '../lib/theme';
import {Big, Hero, Lab, Svg, lerp} from '../eratosthenes/v';
import {Dial, Head, Ship, Tag, Waves, mkV} from '../kinhdo/scenes';

export type Sc = {dur: number; bs: number[]};
const D = C.dim;
const SEAF = '#2f6f86';

// Người que thợ lặn: mũ đồng trùm kín đầu có cửa kính, ống thở lên mặt nước, bong bóng nổi lên từ ống (dùng riêng video 5).
const SailorHero: React.FC<{x: number; y: number; s?: number; walk?: number; cheer?: number}> = ({x, y, s = 1, walk = 0, cheer = 0}) => {
  const f = useCurrentFrame();
  const ch = clamp01(cheer);
  const bob = Math.abs(Math.sin(walk)) * 2.5 + ch * Math.abs(Math.sin(walk * 1.6)) * 7;
  const sw = 3 / s;
  return (
    <g>
      <Hero x={x} y={y} s={s} walk={walk} cheer={cheer} />
      <g transform={`translate(${x} ${y - bob * s}) scale(${s})`} stroke={C.cream} strokeWidth={sw} strokeLinejoin="round" strokeLinecap="round">
        <path d={`M -18 -88 Q -46 -96 -42 -130 Q -40 -160 -${46 + Math.sin(f * 0.05) * 3} -190`} fill="none" stroke="#6b5636" strokeWidth={6 / s * 1.4} />
        <circle cx={-46 - Math.sin(f * 0.05) * 3} cy={-190} r={4} fill="#b08a3e" />
        <rect x={-19} y={-58} width={38} height={9} rx={3} fill="#8a6a2c" />
        <circle cx={0} cy={-77} r={23} fill="#b08a3e" />
        <circle cx={5} cy={-77} r={10} fill="#9fd8e6" />
        <path d="M 1 -82 Q 4 -85 8 -83" fill="none" stroke="#fff" strokeWidth={sw * 0.8} />
        <circle cx={-14} cy={-92} r={1.8} fill={C.cream} stroke="none" />
        <circle cx={16} cy={-92} r={1.8} fill={C.cream} stroke="none" />
        <circle cx={-18} cy={-70} r={1.8} fill={C.cream} stroke="none" />
        <circle cx={0} cy={-100} r={3.5} fill="#8a6a2c" />
        {[0, 1, 2, 3, 4].map((k) => {
          const p = (f * 0.016 + k * 0.2) % 1;
          return <circle key={k} cx={-46 - Math.sin(f * 0.05) * 3 + Math.sin(f * 0.14 + k * 2) * 6} cy={-196 - p * 110} r={2.5 + p * 8} fill="none" stroke="#cfeef5" strokeWidth={sw * 0.8} opacity={0.95 * (1 - p)} />;
        })}
      </g>
    </g>
  );
};

const pie = (cx: number, cy: number, r: number, frac: number) => {
  const a = Math.min(0.9999, Math.max(0.0001, frac)) * 2 * Math.PI;
  const x = cx + r * Math.sin(a);
  const y = cy - r * Math.cos(a);
  return `M ${cx} ${cy} L ${cx} ${cy - r} A ${r} ${r} 0 ${a > Math.PI ? 1 : 0} 1 ${x} ${y} Z`;
};
const Floor: React.FC<{y: number; o?: number}> = ({y, o = 1}) => (
  <path d={`M 0 ${y} L 120 ${y - 20} L 260 ${y + 10} L 420 ${y - 30} L 600 ${y} L 760 ${y - 24} L 920 ${y + 8} L 1080 ${y - 14} L 1080 ${y + 50} L 0 ${y + 50} Z`} fill="#3a2f27" stroke={C.cream} strokeWidth={4} strokeLinejoin="round" opacity={clamp01(o)} />
);
const Weight: React.FC<{x: number; y: number}> = ({x, y}) => (
  <path d={`M ${x - 22} ${y} L ${x + 22} ${y} L ${x + 14} ${y + 46} L ${x - 14} ${y + 46} Z`} fill="#7b7f86" stroke={C.cream} strokeWidth={4} strokeLinejoin="round" />
);
const Arrow: React.FC<{x1: number; y1: number; x2: number; y2: number; color?: string; o?: number}> = ({x1, y1, x2, y2, color = C.amber, o = 1}) => {
  const a = Math.atan2(y2 - y1, x2 - x1);
  const h = 22;
  return (
    <g opacity={clamp01(o)} stroke={color} strokeWidth={6} strokeLinecap="round" fill="none">
      <line x1={x1} y1={y1} x2={x2} y2={y2} />
      <path d={`M ${x2 - h * Math.cos(a - 0.5)} ${y2 - h * Math.sin(a - 0.5)} L ${x2} ${y2} L ${x2 - h * Math.cos(a + 0.5)} ${y2 - h * Math.sin(a + 0.5)}`} />
    </g>
  );
};

// ============ 1. Mở đầu ============
export const Hook: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const bob = Math.sin(f * 0.08) * 6;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Bản đồ đáy biển" b="mới có chưa đến 30%" />
        <circle cx={540} cy={820} r={260} fill={C.bg1} stroke={C.cream} strokeWidth={6} />
        <path d={pie(540, 820, 250, 0.287 * seg(f, 8, 50))} fill={C.amber} opacity={0.9} />
        <circle cx={540} cy={820} r={250} fill="none" stroke={C.cream} strokeWidth={3} opacity={0.35} strokeDasharray="6 14" />
        <Big x={540} y={1200} size={110} color={C.amber} o={sp(f, 40, 56)}>{'< 30%'}</Big>
        <Tag x={540} y={1262} color={C.cream} size={38} o={sp(f, 48, 64)}>đáy biển đã có bản đồ</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Đo độ cao núi thì dễ" b="đo độ sâu biển sao khó?" />
        <path d="M 120 1100 L 330 640 L 540 1100 Z" fill="#4b4036" stroke={C.cream} strokeWidth={5} strokeLinejoin="round" />
        <SailorHero x={lerp(100, 330, seg(f, b1 + 4, b1 + 120))} y={1100} s={1.6} walk={f * 0.25} />
        <line x1={600} y1={1100} x2={1000} y2={1100} stroke={C.cream} strokeWidth={4} opacity={0.5} />
        <Waves y={1040} f={f} />
        <Lab x={800} y={950} size={120} color={C.amber} o={0.9 * sp(f, b1 + 24, b1 + 40)}>?</Lab>
        <Tag x={330} y={1200} color={C.cream} size={38}>nhìn là thấy</Tag>
        <Tag x={800} y={1200} color={C.cream} size={38}>không thấy đáy</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Ta không nhìn thấy đáy" b="dây không báo lúc chạm đáy" />
        <rect x={0} y={640} width={1080} height={520} fill="#0a2a3c" opacity={0.7} />
        <Ship x={540} y={600 + bob} s={0.9} />
        <path d={`M 540 650 Q ${560 + Math.sin(f * 0.1) * 20} 850 540 ${650 + 400 * seg(f, b2 + 6, b2 + 50)}`} fill="none" stroke={C.cream} strokeWidth={4} />
        <Lab x={760} y={1000} size={110} color={C.amber} o={0.9 * sp(f, b2 + 50, b2 + 64)}>?</Lab>
        <Floor y={1180} />
        <Tag x={540} y={1290} color={C.cream} size={36}>dây chạm đáy lúc nào?</Tag>
      </g>
    </Svg>
  );
};

// ============ 2. Thả dây ============
export const Cu: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const drop = seg(f, 8, 70);
  const sag = seg(f, b1 + 10, b1 + 60);
  const min = seg(f, b2 + 10, b2 + 120) * 20;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Cách cũ: thả quả nặng" b="đọc số mét dây đã chạy ra" />
        <rect x={0} y={620} width={1080} height={560} fill="#0a2a3c" opacity={0.7} />
        <Ship x={380} y={590} s={0.8} />
        <line x1={380} y1={640} x2={380} y2={640 + 480 * drop} stroke={C.cream} strokeWidth={4} />
        <Weight x={380} y={640 + 480 * drop} />
        {[0, 1, 2, 3, 4, 5].map((i) => (
          <g key={i} opacity={sp(f, 14 + i * 8, 24 + i * 8)}>
            <line x1={410} y1={700 + i * 80} x2={470} y2={700 + i * 80} stroke={C.amber} strokeWidth={4} />
            <Tag x={500} y={712 + i * 80} color={C.amber} size={34} anchor="start">{`${i * 100} m`}</Tag>
          </g>
        ))}
        <Floor y={1180} />
        <SailorHero x={lerp(560, 930, seg(f, 10, 200))} y={1180} s={1.1} walk={f * 0.25} />
      </g>
      <g opacity={V(1)}>
        <Head a="Chỗ sâu: dây tự nó rất nặng" b="tay khó nhận ra chạm đáy" />
        <rect x={0} y={620} width={1080} height={560} fill="#0a2a3c" opacity={0.7} />
        <Ship x={300} y={590} s={0.8} />
        <path d={`M 300 640 Q ${300 + 300 * sag} 900 ${540} 1120`} fill="none" stroke={C.cream} strokeWidth={5} />
        <Weight x={540} y={1120} />
        <Floor y={1180} />
        <Lab x={760} y={820} size={110} color={C.amber} o={0.9 * sp(f, b1 + 40, b1 + 54)}>?</Lab>
        <Tag x={760} y={900} color={C.cream} size={36} o={sp(f, b1 + 44, b1 + 58)}>chạm đáy chưa?</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Sâu khoảng 2 700 m" b="quả nặng chìm khoảng 20 phút" />
        <Dial x={540} y={760} r={200} hand={0} min={min * 18} />
        <Big x={540} y={1120} size={120} color={C.amber} o={sp(f, b2 + 14, b2 + 28)}>20 phút</Big>
        <Tag x={540} y={1210} color={C.cream} size={42} o={sp(f, b2 + 24, b2 + 38)}>để tới đáy sâu 2 700 m</Tag>
      </g>
    </Svg>
  );
};

// ============ 3. Challenger ============
export const Chal: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const bob = Math.sin(f * 0.07) * 6;
  const dots = Array.from({length: 42}, (_, i) => ({x: 150 + ((i * 227) % 780), y: 560 + ((i * 131) % 560)}));
  const dd = seg(f, b1 + 10, b1 + 90);
  const dep = seg(f, b2 + 8, b2 + 60);
  const dep2 = seg(f, b2 + 80, b2 + 120);
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Tàu Challenger của Anh" b="cũng đo bằng dây" />
        <Waves y={1000} f={f} />
        <Ship x={540} y={900 + bob} s={1.4} rot={Math.sin(f * 0.06) * 3} />
        <line x1={190} y1={1210} x2={890} y2={1210} stroke={C.cream} strokeWidth={6} strokeLinecap="round" />
        <circle cx={190} cy={1210} r={12} fill={C.amber} />
        <circle cx={890} cy={1210} r={12} fill={C.amber} />
        <Tag x={190} y={1170} color={C.amber} size={44}>1872</Tag>
        <Tag x={890} y={1170} color={C.amber} size={44}>1876</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Chưa đến 500 điểm đo" b="trên một bản đồ trắng" />
        <rect x={90} y={500} width={900} height={680} rx={14} fill="#e8e0cf" opacity={0.9} stroke={C.cream} strokeWidth={5} />
        {dots.map((d, i) => (
          <circle key={i} cx={d.x} cy={d.y} r={7} fill={C.amberDeep} opacity={clamp01(dd * 42 - i)} />
        ))}
        <Big x={540} y={1280} size={96} color={C.amber} o={sp(f, b1 + 60, b1 + 74)}>{'< 500 lần đo'}</Big>
      </g>
      <g opacity={V(2)}>
        <Head a="23/3/1875: sâu 8 184 m" b="và đo lại lần hai" />
        <rect x={0} y={560} width={1080} height={640} fill="#0a2a3c" opacity={0.7} />
        <Ship x={300} y={530} s={0.7} />
        <line x1={300} y1={580} x2={300} y2={580 + 560 * dep} stroke={C.cream} strokeWidth={4} />
        <Weight x={300} y={580 + 560 * dep} />
        <Floor y={1190} o={dep} />
        <SailorHero x={lerp(620, 960, seg(f, b2 + 60, b2 + 200))} y={1190} s={1.0} walk={f * 0.25} />
        <Big x={700} y={860} size={110} color={C.amber} o={sp(f, b2 + 50, b2 + 64)}>8 184 m</Big>
        <Tag x={700} y={940} color={C.cream} size={40} o={sp(f, b2 + 70, b2 + 84)}>đo lại lần hai</Tag>
        <circle cx={700} cy={1030} r={26} fill="none" stroke={C.amber} strokeWidth={6} opacity={dep2} />
        <path d="M 688 1030 L 697 1040 L 714 1018" fill="none" stroke={C.amber} strokeWidth={6} strokeLinecap="round" opacity={dep2} />
      </g>
    </Svg>
  );
};

// ============ 4. Tiếng vang ============
const Rings: React.FC<{x: number; y: number; f: number; t0: number; n?: number; color?: string; maxR?: number}> = ({x, y, f, t0, n = 3, color = '#7fd3e6', maxR = 160}) => (
  <g fill="none" stroke={color} strokeWidth={5}>
    {Array.from({length: n}, (_, k) => {
      const p = (((f - t0 - k * 16) % 70) + 70) % 70 / 70;
      return <circle key={k} cx={x} cy={y} r={20 + p * maxR} opacity={0.8 * (1 - p)} />;
    })}
  </g>
);
export const Vang: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2, b3, b4, b5] = bs;
  const bob = Math.sin(f * 0.07) * 5;
  const ping = (((f - b4 - 20) % 120) + 120) % 120 / 120;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Ý mới: gửi tiếng động" b="xuống đáy biển" />
        <rect x={0} y={640} width={1080} height={540} fill="#0a2a3c" opacity={0.7} />
        <Ship x={540} y={610 + bob} s={0.9} />
        <Rings x={540} y={780} f={f} t0={10} n={4} maxR={380} />
        <Floor y={1180} />
        <SailorHero x={lerp(120, 940, seg(f, 6, 200))} y={1180} s={1.0} walk={f * 0.25} />
        <Arrow x1={540} y1={820} x2={540} y2={1110} o={sp(f, 20, 34)} />
        <Tag x={540} y={1290} color={C.cream} size={38}>tiếng động đi xuống</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Như hét vào thung lũng" b="càng xa, vang càng muộn" />
        <SailorHero x={lerp(140, 400, seg(f, b1 + 4, b1 + 90))} y={760} s={1.2} walk={f * 0.25} cheer={0.5 + 0.5 * Math.sin(f * 0.3)} />
        <path d="M 560 760 L 640 620 L 720 760 Z" fill="#4b4036" stroke={C.cream} strokeWidth={5} strokeLinejoin="round" />
        <Arrow x1={200} y1={700} x2={560} y2={700} o={sp(f, b1 + 6, b1 + 20)} />
        <Tag x={640} y={820} color={C.cream} size={34}>gần: vang sớm</Tag>
        <SailorHero x={lerp(140, 620, seg(f, b1 + 20, b1 + 130))} y={1080} s={1.2} walk={f * 0.25} cheer={0.5 + 0.5 * Math.sin(f * 0.3 + 1)} />
        <path d="M 860 1080 L 940 940 L 1020 1080 Z" fill="#4b4036" stroke={C.cream} strokeWidth={5} strokeLinejoin="round" />
        <Arrow x1={200} y1={1020} x2={850} y2={1020} o={sp(f, b1 + 24, b1 + 40)} />
        <Tag x={640} y={1150} color={C.amber} size={34}>xa: vang muộn</Tag>
        <Tag x={540} y={1260} color={C.cream} size={40} o={sp(f, b1 + 60, b1 + 76)}>đáy càng sâu, vang càng chậm</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Trong nước, âm thanh đi" b="1 500 m mỗi giây" />
        <rect x={0} y={640} width={1080} height={540} fill="#0a2a3c" opacity={0.7} />
        <Ship x={300} y={610} s={0.7} />
        <Floor y={1180} />
        <SailorHero x={lerp(700, 980, seg(f, b2 + 10, b2 + 200))} y={1180} s={1.0} walk={f * 0.25} />
        <Arrow x1={380} y1={700} x2={380} y2={1110} o={sp(f, b2 + 10, b2 + 26)} />
        <Arrow x1={560} y1={1110} x2={560} y2={700} color={'#7fd3e6'} o={sp(f, b2 + 40, b2 + 56)} />
        <Tag x={300} y={900} color={C.amber} size={36} anchor="end" o={sp(f, b2 + 14, b2 + 28)}>đi xuống</Tag>
        <Tag x={620} y={900} color={'#7fd3e6'} size={36} anchor="start" o={sp(f, b2 + 44, b2 + 58)}>dội lên</Tag>
        <Big x={800} y={780} size={90} color={C.amber} o={sp(f, b2 + 14, b2 + 28)}>1 500</Big>
        <Tag x={800} y={840} color={C.cream} size={34} o={sp(f, b2 + 18, b2 + 32)}>m mỗi giây</Tag>
        <Big x={540} y={1290} size={64} color={C.cream} o={sp(f, b2 + 80, b2 + 94)}>quãng đường = 2 × độ sâu</Big>
      </g>
      <g opacity={V(3)}>
        <Head a="Độ sâu = tốc độ × thời gian ÷ 2" />
        <Big x={540} y={700} size={90} color={C.cream} o={sp(f, b3 + 6, b3 + 20)}>độ sâu =</Big>
        <Big x={540} y={860} size={100} color={C.amber} o={sp(f, b3 + 20, b3 + 34)}>tốc độ</Big>
        <Big x={540} y={990} size={100} color={C.amber} o={sp(f, b3 + 34, b3 + 48)}>× thời gian</Big>
        <Big x={540} y={1120} size={100} color={C.cream} o={sp(f, b3 + 48, b3 + 62)}>÷ 2</Big>
      </g>
      <g opacity={V(4)}>
        <Head a="Vang về sau 4 giây" b="đáy sâu bao nhiêu?" />
        <Big x={540} y={620} size={96} color={C.cream} o={sp(f, b4 + 4, b4 + 18)}>1 500 × 4 = 6 000</Big>
        <Big x={540} y={760} size={96} color={C.cream} o={sp(f, b4 + 30, b4 + 44)}>6 000 ÷ 2 = 3 000</Big>
        <rect x={0} y={880} width={1080} height={320} fill="#0a2a3c" opacity={0.7} />
        <Ship x={300} y={860} s={0.5} />
        <line x1={300} y1={900} x2={300} y2={1170} stroke={C.amber} strokeWidth={5} strokeDasharray="10 12" />
        <Floor y={1180} />
        <Big x={680} y={1060} size={110} color={C.amber} o={sp(f, b4 + 60, b4 + 74)}>3 000 m</Big>
      </g>
      <g opacity={V(5)}>
        <Head a="Chỉ vài giây" b="tàu vừa chạy vừa đo" />
        <rect x={0} y={760} width={1080} height={440} fill="#0a2a3c" opacity={0.7} />
        <Ship x={lerp(160, 920, seg(f, b5, b5 + 160))} y={730 + Math.sin(f * 0.07) * 5} s={0.6} />
        {[0, 1, 2, 3, 4].map((i) => {
          const x = lerp(160, 920, seg(f, b5, b5 + 160));
          const s0 = 30 + i * 26;
          const p = clamp01((f - b5 - s0) / 30);
          return p > 0 && p < 1 ? <line key={i} x1={160 + i * 190} y1={780} x2={160 + i * 190} y2={780 + 380 * p} stroke="#7fd3e6" strokeWidth={4} opacity={1 - p * 0.6} /> : null;
        })}
        <Floor y={1180} />
        <SailorHero x={lerp(160, 920, seg(f, b5, b5 + 160))} y={1180} s={1.0} walk={f * 0.3} />
        <Tag x={300} y={1290} color={C.amber} size={44}>vài giây</Tag>
        <Tag x={780} y={1290} color={D} size={44}>thay vì nhiều phút</Tag>
      </g>
    </Svg>
  );
};

// ============ 5. Meteor ============
export const Meteor: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const bob = Math.sin(f * 0.07) * 6;
  const k = seg(f, b1 + 10, b1 + 70);
  const prof = (i: number) => `M 90 ${600 + i * 44} ` + Array.from({length: 11}, (_, j) => `L ${90 + j * 90} ${600 + i * 44 + Math.sin(j * 1.3 + i * 0.7) * 14 + (j > 3 && j < 8 ? 14 : 0)}`).join(' ');
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Tàu Meteor của Đức, 1925" b="dùng máy đo tiếng vang" />
        <rect x={0} y={760} width={1080} height={440} fill="#0a2a3c" opacity={0.7} />
        <Ship x={540} y={730 + bob} s={1.2} rot={Math.sin(f * 0.06) * 3} />
        <Rings x={540} y={900} f={f} t0={8} n={3} maxR={200} />
        <Floor y={1180} />
        <SailorHero x={lerp(150, 900, seg(f, 6, 170))} y={1180} s={1.0} walk={f * 0.25} />
        <Tag x={540} y={1290} color={C.cream} size={40}>khảo sát Nam Đại Tây Dương</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Khoảng 67 000 lần đo" b="gấp hơn 100 lần Challenger" />
        <Tag x={110} y={700} color={C.cream} size={38} anchor="start">Challenger</Tag>
        <rect x={110} y={730} width={Math.max(6, 6 * seg(f, b1 + 4, b1 + 20))} height={60} rx={8} fill={C.amber} stroke={C.cream} strokeWidth={4} />
        <Tag x={110} y={860} color={C.cream} size={38} anchor="start">Meteor</Tag>
        <rect x={110} y={890} width={Math.max(6, 860 * k)} height={60} rx={8} fill={'#7fd3e6'} stroke={C.cream} strokeWidth={4} />
        <Big x={540} y={1120} size={110} color={C.amber} o={sp(f, b1 + 60, b1 + 74)}>67 000 lần</Big>
        <Tag x={540} y={1200} color={C.cream} size={40} o={sp(f, b1 + 66, b1 + 80)}>so với chưa đến 500</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Họ vẽ được 14 mặt cắt" b="của đáy Đại Tây Dương" />
        {Array.from({length: 14}, (_, i) => (
          <path key={i} d={prof(i)} fill="none" stroke={i % 2 ? C.cream : '#7fd3e6'} strokeWidth={5} strokeLinecap="round" opacity={clamp01(seg(f, b2 + 4 + i * 5, b2 + 20 + i * 5) * 1.2)} strokeDasharray="1200" strokeDashoffset={1200 * (1 - seg(f, b2 + 4 + i * 5, b2 + 24 + i * 5))} />
        ))}
        <Big x={540} y={1290} size={96} color={C.amber} o={sp(f, b2 + 80, b2 + 94)}>14 mặt cắt</Big>
      </g>
    </Svg>
  );
};

// ============ 6. Ngày nay ============
export const Nay: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2, b3, b4] = bs;
  const dots = Array.from({length: 40}, (_, i) => ({a: (i * 137.5 * Math.PI) / 180, r: 330 + ((i * 53) % 130)}));
  const gather = seg(f, 10, 90);
  const lanes = seg(f, b3 + 10, b3 + 130);
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Dự án Seabed 2030" b="gom số đo của 220 tổ chức" />
        <circle cx={540} cy={860} r={130} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
        {dots.map((d, i) => (
          <circle key={i} cx={540 + Math.cos(d.a) * d.r * (1 - gather * 0.7)} cy={860 + Math.sin(d.a) * d.r * (1 - gather * 0.7)} r={11} fill={i % 2 ? C.amber : '#7fd3e6'} opacity={0.9} />
        ))}
        <Big x={540} y={1250} size={110} color={C.amber} o={sp(f, 50, 64)}>220 tổ chức</Big>
      </g>
      <g opacity={V(1)}>
        <Head a="Tháng 4/2026: 104 triệu km²" b="tức 28,7% đáy biển" />
        <circle cx={540} cy={850} r={260} fill={C.bg1} stroke={C.cream} strokeWidth={6} />
        <path d={pie(540, 850, 250, 0.287 * seg(f, b1 + 6, b1 + 60))} fill={C.amber} />
        <Big x={540} y={1210} size={110} color={C.amber} o={sp(f, b1 + 50, b1 + 64)}>28,7%</Big>
        <Tag x={540} y={1275} color={C.cream} size={38} o={sp(f, b1 + 56, b1 + 70)}>104 triệu km² đã có số đo</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Cả đáy biển rộng khoảng" b="362 triệu km²" />
        <Big x={540} y={720} size={90} color={C.cream} o={sp(f, b2 + 6, b2 + 20)}>104 triệu</Big>
        <Big x={540} y={850} size={90} color={C.cream} o={sp(f, b2 + 24, b2 + 38)}>÷ 28,7%</Big>
        <Big x={540} y={1010} size={120} color={C.amber} o={sp(f, b2 + 44, b2 + 58)}>≈ 362 triệu</Big>
        <Tag x={540} y={1090} color={C.cream} size={42} o={sp(f, b2 + 50, b2 + 64)}>ki-lô-mét vuông</Tag>
      </g>
      <g opacity={V(3)}>
        <Head a="Ngoài khơi Alaska" b="khảo sát từng tuyến, 40 năm" />
        <rect x={110} y={560} width={860} height={560} rx={12} fill="#0a2a3c" stroke={C.cream} strokeWidth={5} />
        {Array.from({length: 7}, (_, i) => (
          <line key={i} x1={130} y1={600 + i * 75} x2={130 + 820 * clamp01(lanes * 7 - i)} y2={600 + i * 75} stroke={i % 2 ? C.amber : '#7fd3e6'} strokeWidth={8} strokeLinecap="round" />
        ))}
        <Big x={540} y={1250} size={110} color={C.amber} o={sp(f, b3 + 60, b3 + 74)}>40 năm</Big>
      </g>
      <g opacity={V(4)}>
        <Head a="Hơn 70% vẫn là khoảng trắng" b="nhờ tiếng vang, ta bắt đầu vẽ" />
        <circle cx={540} cy={850} r={260} fill="#e8e0cf" opacity={0.9} stroke={C.cream} strokeWidth={6} />
        <path d={pie(540, 850, 250, 0.287)} fill={C.amber} />
        <Big x={540} y={1210} size={100} color={C.cream} o={sp(f, b4 + 10, b4 + 24)}>còn hơn 70%</Big>
        <SailorHero x={860} y={1300} s={1.6} cheer={1} walk={f * 0.2} />
      </g>
    </Svg>
  );
};
