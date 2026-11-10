import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, clamp01, seg, sp} from '../lib/theme';
import {Big, Hero, Lab, Svg, lerp} from '../eratosthenes/v';
import {Head, Tag, mkV} from '../kinhdo/scenes';

export type Sc = {dur: number; bs: number[]};
const SAND = '#d9b87a';
const BUG = '#8fd19e';
const RBC = '#d9453b';
const WATER = '#2f8aa3';

const Bug: React.FC<{x: number; y: number; r?: number; ph?: number; f: number; o?: number}> = ({x, y, r = 8, ph = 0, f, o = 1}) => (
  <ellipse cx={x + Math.sin(f * 0.1 + ph) * r * 0.8} cy={y + Math.cos(f * 0.13 + ph) * r * 0.6} rx={r * 1.4} ry={r} fill={BUG} stroke={C.cream} strokeWidth={Math.max(1.5, r / 4)} opacity={clamp01(o)} />
);
const Cell: React.FC<{x: number; y: number; r?: number; o?: number}> = ({x, y, r = 20, o = 1}) => (
  <g opacity={clamp01(o)}>
    <ellipse cx={x} cy={y} rx={r} ry={r * 0.9} fill={RBC} stroke={C.cream} strokeWidth={Math.max(2, r / 8)} />
    <ellipse cx={x} cy={y} rx={r * 0.4} ry={r * 0.35} fill="#9c2a24" />
  </g>
);
const Grain: React.FC<{x: number; y: number; r: number; o?: number}> = ({x, y, r, o = 1}) => (
  <ellipse cx={x} cy={y} rx={r * 1.2} ry={r} fill={SAND} stroke={C.cream} strokeWidth={4} opacity={clamp01(o)} />
);
const Lens: React.FC<{x: number; y: number; r?: number}> = ({x, y, r = 150}) => (
  <g>
    <circle cx={x} cy={y} r={r} fill="#bfe3f0" opacity={0.25} stroke={C.cream} strokeWidth={8} />
    <circle cx={x} cy={y} r={r + 22} fill="none" stroke="#b08a50" strokeWidth={16} />
    <path d={`M ${x - r * 0.55} ${y - r * 0.5} Q ${x - r * 0.2} ${y - r * 0.8} ${x + r * 0.2} ${y - r * 0.7}`} fill="none" stroke={C.cream} strokeWidth={6} strokeLinecap="round" opacity={0.7} />
  </g>
);

// ============ 1. Mở đầu ============
export const Hook: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Một giọt nước" b="có 1 triệu sinh vật?" />
        <path d="M 540 470 Q 740 760 740 900 A 200 200 0 0 1 340 900 Q 340 760 540 470 Z" fill="#7fc4e0" opacity={0.55} stroke={C.cream} strokeWidth={7} />
        {Array.from({length: 16}, (_, i) => (
          <Bug key={i} x={440 + (i % 4) * 66} y={820 + Math.floor(i / 4) * 58} r={6} ph={i * 1.7} f={f} o={sp(f, 8 + i * 2, 20 + i * 2)} />
        ))}
        <Lab x={870} y={640} size={110} color={C.amber} o={0.9 * sp(f, 40, 54)}>?</Lab>
        <Hero x={190} y={1230} s={1.7} walk={f * 0.25} />
        <Tag x={620} y={1250} color={C.cream} size={40}>làm sao đếm được?</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Người đếm là" b="một người bán vải ở Hà Lan" />
        <rect x={160} y={820} width={760} height={280} rx={10} fill="#6c4a32" stroke={C.cream} strokeWidth={6} />
        {['#b5473a', '#3e6fa6', '#d6a83a', '#4a8a5a'].map((c, i) => (
          <rect key={c} x={200 + i * 175} y={850} width={140} height={220} rx={6} fill={c} stroke={C.cream} strokeWidth={4} opacity={sp(f, b1 + 6 + i * 5, b1 + 20 + i * 5)} />
        ))}
        <Hero x={lerp(120, 540, seg(f, b1, b1 + 60))} y={1300} s={1.9} walk={f * 0.25} />
        <Tag x={540} y={760} color={C.amber} size={42} o={sp(f, b1 + 30, b1 + 44)}>thợ vải</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Vì sao đo được?" b="ông dùng hạt cát" />
        <Grain x={330} y={960} r={90} o={sp(f, b2 + 6, b2 + 22)} />
        <Bug x={760} y={960} r={10} f={f} o={sp(f, b2 + 20, b2 + 34)} />
        <line x1={420} y1={960} x2={700} y2={960} stroke={C.amber} strokeWidth={5} strokeDasharray="12 10" opacity={sp(f, b2 + 30, b2 + 44)} />
        <Lab x={560} y={1090} size={80} color={C.amber} o={0.9 * sp(f, b2 + 36, b2 + 50)}>so sánh</Lab>
        <Hero x={540} y={1300} s={1.6} walk={f * 0.25} cheer={sp(f, b2 + 40, b2 + 60)} />
      </g>
    </Svg>
  );
};

// ============ 2. Kính, vật so sánh ============
export const Kinh: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const bob = Math.sin(f * 0.07) * 6;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Một thấu kính nhỏ" b="phóng to tới 275 lần" />
        <Lens x={540} y={850 + bob} r={170} />
        <Bug x={540} y={850 + bob} r={10 + 26 * sp(f, 14, 50)} ph={1} f={f} />
        <Big x={540} y={1180} size={120} color={C.amber} o={sp(f, 30, 44)}>× 275</Big>
        <Hero x={170} y={1290} s={1.4} walk={f * 0.25} />
      </g>
      <g opacity={V(1)}>
        <Head a="Thấy chưa đủ" b="phải biết to bao nhiêu" />
        <Bug x={540} y={900} r={40} f={f} />
        <Lab x={540} y={1060} size={120} color={C.amber} o={0.9 * sp(f, b1 + 10, b1 + 24)}>?</Lab>
        <Tag x={540} y={1220} color={C.cream} size={42} o={sp(f, b1 + 24, b1 + 38)}>to cỡ nào?</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="So với vật quen:" b="hạt cát, hạt kê, sợi tóc" />
        <Grain x={250} y={940} r={70} o={sp(f, b2 + 6, b2 + 20)} />
        <circle cx={540} cy={950} r={45} fill="#e0c060" stroke={C.cream} strokeWidth={4} opacity={sp(f, b2 + 18, b2 + 32)} />
        <path d="M 760 840 Q 800 940 770 1060" fill="none" stroke="#2b2118" strokeWidth={9} strokeLinecap="round" opacity={sp(f, b2 + 30, b2 + 44)} />
        <Tag x={250} y={1090} color={C.cream} size={38} o={sp(f, b2 + 10, b2 + 24)}>hạt cát</Tag>
        <Tag x={540} y={1090} color={C.cream} size={38} o={sp(f, b2 + 22, b2 + 36)}>hạt kê</Tag>
        <Tag x={790} y={1130} color={C.cream} size={38} o={sp(f, b2 + 34, b2 + 48)}>sợi tóc</Tag>
        <Hero x={lerp(120, 940, seg(f, b2, b2 + 90))} y={1300} s={1.5} walk={f * 0.25} />
      </g>
    </Svg>
  );
};

// ============ 3. Lập phương ============
export const Lp: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2, b3] = bs;
  const cube = (n: number, s: number, x0: number, y0: number, o: number) => (
    <g opacity={clamp01(o)}>
      {Array.from({length: n * n}, (_, k) => (
        <rect key={k} x={x0 + (k % n) * s} y={y0 + Math.floor(k / n) * s} width={s - 2} height={s - 2} rx={2} fill={BUG} opacity={0.75} stroke={C.cream} strokeWidth={1} />
      ))}
    </g>
  );
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Hạt cát dài gấp" b="12 lần con vật" />
        <Grain x={540} y={900} r={110} o={sp(f, 6, 20)} />
        {Array.from({length: 12}, (_, i) => (
          <ellipse key={i} cx={270 + i * 49} cy={1090} rx={19} ry={14} fill={BUG} stroke={C.cream} strokeWidth={2.5} opacity={sp(f, 14 + i * 3, 24 + i * 3)} />
        ))}
        <line x1={250} y1={1050} x2={830} y2={1050} stroke={C.amber} strokeWidth={5} />
        <Big x={540} y={1230} size={110} color={C.amber} o={sp(f, 50, 64)}>12 lần</Big>
      </g>
      <g opacity={V(1)}>
        <Head a="Dài gấp 12" b="thể tích không gấp 12" />
        <rect x={270} y={820} width={46} height={46} fill={BUG} stroke={C.cream} strokeWidth={4} />
        <Tag x={293} y={910} color={C.cream} size={34}>1</Tag>
        <path d="M 340 842 L 440 842" stroke={C.amber} strokeWidth={6} markerEnd="" />
        <Lab x={560} y={842} size={90} color={C.amber} o={0.9 * sp(f, b1 + 20, b1 + 34)}>≠ 12</Lab>
        {cube(12, 24, 360, 920, sp(f, b1 + 10, b1 + 30))}
      </g>
      <g opacity={V(2)}>
        <Head a="Rộng, dài, cao:" b="đều gấp 12 lần" />
        <Big x={540} y={780} size={100} color={C.cream} o={sp(f, b2 + 6, b2 + 20)}>12 × 12 × 12</Big>
        {cube(12, 20, 300, 880, 1)}
        <Hero x={140} y={1290} s={1.4} walk={f * 0.25} />
        <Tag x={720} y={1250} color={C.amber} size={38} o={sp(f, b2 + 40, b2 + 54)}>rộng × dài × cao</Tag>
      </g>
      <g opacity={V(3)}>
        <Head a="Hạt cát lớn gấp" b="1 728 lần con vật" />
        <Big x={540} y={820} size={140} color={C.amber} o={sp(f, b3 + 6, b3 + 22)}>1 728</Big>
        <Grain x={330} y={1080} r={110} o={sp(f, b3 + 14, b3 + 28)} />
        <Bug x={760} y={1080} r={8} f={f} o={sp(f, b3 + 20, b3 + 34)} />
        <Tag x={540} y={1260} color={C.cream} size={40} o={sp(f, b3 + 30, b3 + 44)}>1 hạt cát = 1 728 con</Tag>
      </g>
    </Svg>
  );
};

// ============ 4. Nhỏ hơn nữa ============
export const Nho: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2, b3] = bs;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Loại dài bằng 1/4" b="4 × 4 × 4 = 64" />
        <Grain x={400} y={960} r={110} />
        {Array.from({length: 4}, (_, i) => (
          <ellipse key={i} cx={290 + i * 70} cy={1150} rx={26} ry={19} fill={BUG} stroke={C.cream} strokeWidth={3} opacity={sp(f, 10 + i * 4, 22 + i * 4)} />
        ))}
        <Big x={760} y={900} size={150} color={C.amber} o={sp(f, 30, 44)}>64</Big>
        <Tag x={760} y={1010} color={C.cream} size={38} o={sp(f, 36, 50)}>lần thể tích</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="1 728 × 64" b="= 110 592 con" />
        <Big x={540} y={760} size={96} color={C.cream} o={sp(f, b1 + 6, b1 + 20)}>1 728 × 64</Big>
        <Big x={540} y={920} size={130} color={C.amber} o={sp(f, b1 + 24, b1 + 38)}>110 592</Big>
        <Grain x={540} y={1130} r={90} o={sp(f, b1 + 30, b1 + 44)} />
        {Array.from({length: 30}, (_, i) => (
          <circle key={i} cx={470 + (i % 6) * 28} cy={1090 + Math.floor(i / 6) * 22} r={5} fill={BUG} opacity={sp(f, b1 + 36 + i, b1 + 46 + i)} />
        ))}
      </g>
      <g opacity={V(2)}>
        <Head a="Loại dài bằng 1/10" b="nhân thêm 1 000" />
        <Big x={540} y={780} size={96} color={C.cream} o={sp(f, b2 + 6, b2 + 20)}>10 × 10 × 10</Big>
        <Big x={540} y={930} size={110} color={C.amber} o={sp(f, b2 + 22, b2 + 36)}>= 1 000</Big>
        <Big x={540} y={1100} size={90} color={C.cream} o={sp(f, b2 + 40, b2 + 54)}>hơn 110 triệu</Big>
        <Hero x={170} y={1290} s={1.4} walk={f * 0.25} />
      </g>
      <g opacity={V(3)}>
        <Head a="100 hồng cầu xếp hàng" b="bằng một hạt cát" />
        {Array.from({length: 10}, (_, i) => (
          <Cell key={i} x={170 + i * 82} y={860} r={34} o={sp(f, b3 + 6 + i * 3, b3 + 18 + i * 3)} />
        ))}
        <Tag x={540} y={950} color={C.cream} size={36} o={sp(f, b3 + 30, b3 + 44)}>(vẽ 10 trong 100)</Tag>
        <Big x={540} y={1100} size={90} color={C.cream} o={sp(f, b3 + 36, b3 + 50)}>100 × 100 × 100</Big>
        <Big x={540} y={1230} size={110} color={C.amber} o={sp(f, b3 + 50, b3 + 64)}>= 1 triệu</Big>
      </g>
    </Svg>
  );
};

// ============ 5. Giọt nước ============
export const Giot: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2, b3] = bs;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="1677: đếm giọt nước" b="tính ra 2 730 000" />
        <path d="M 540 520 Q 710 780 710 900 A 170 170 0 0 1 370 900 Q 370 780 540 520 Z" fill="#7fc4e0" opacity={0.55} stroke={C.cream} strokeWidth={7} />
        {Array.from({length: 12}, (_, i) => (
          <Bug key={i} x={460 + (i % 4) * 54} y={860 + Math.floor(i / 4) * 50} r={6} ph={i * 1.3} f={f} />
        ))}
        <Big x={540} y={1180} size={110} color={C.amber} o={sp(f, 20, 34)}>2 730 000</Big>
        <Tag x={540} y={1260} color={C.cream} size={40} o={sp(f, 40, 54)}>ông báo: 1 triệu</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Hội Hoàng gia" b="kiểm tra lại rồi mới nhận" />
        {[0, 1, 2].map((i) => (
          <g key={i} opacity={sp(f, b1 + 6 + i * 8, b1 + 20 + i * 8)}>
            <circle cx={260 + i * 280} cy={900} r={52} fill="#e3c9a4" stroke={C.cream} strokeWidth={5} />
            <path d={`M ${190 + i * 280} 1010 Q ${260 + i * 280} 940 ${330 + i * 280} 1010 L ${330 + i * 280} 1100 L ${190 + i * 280} 1100 Z`} fill="#46494f" stroke={C.cream} strokeWidth={5} />
          </g>
        ))}
        <path d="M 440 1180 L 500 1240 L 620 1120" fill="none" stroke="#6fcf8a" strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" opacity={sp(f, b1 + 36, b1 + 50)} />
        <Tag x={540} y={760} color={C.cream} size={40}>các nhà khoa học</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Ông giữ kín" b="cách mài kính tốt nhất" />
        <rect x={340} y={900} width={400} height={260} rx={14} fill="#6c4a32" stroke={C.cream} strokeWidth={6} />
        <rect x={340} y={900} width={400} height={80 - 50 * sp(f, b2 + 10, b2 + 30)} rx={14} fill="#8a6a48" stroke={C.cream} strokeWidth={6} />
        <circle cx={540} cy={1040} r={22} fill="#e0b97a" stroke={C.cream} strokeWidth={4} />
        <Lens x={540} y={720} r={80} />
        <Tag x={540} y={1240} color={C.cream} size={40}>bí quyết không công bố</Tag>
      </g>
      <g opacity={V(3)}>
        <Head a="Ước chừng bằng mắt" b="nhưng gần số đo hiện đại" />
        <rect x={160} y={860} width={760} height={34} rx={10} fill="#3a2c20" stroke={C.cream} strokeWidth={4} />
        <circle cx={lerp(200, 880, 0.62 * sp(f, b3 + 6, b3 + 40))} cy={877} r={26} fill={C.amber} stroke={C.cream} strokeWidth={4} />
        <Tag x={200} y={820} color={C.cream} size={34} anchor="start">ông đếm</Tag>
        <Tag x={880} y={820} color={C.cream} size={34} anchor="end">số đo nay</Tag>
        <Tag x={540} y={1060} color={C.amber} size={44} o={sp(f, b3 + 40, b3 + 54)}>cùng bậc độ lớn</Tag>
        <Hero x={lerp(120, 900, seg(f, b3, b3 + 80))} y={1280} s={1.5} walk={f * 0.25} cheer={sp(f, b3 + 60, b3 + 80)} />
      </g>
    </Svg>
  );
};

// ============ 6. Ngày nay ============
export const Nay: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2, b3] = bs;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Hồng cầu rộng khoảng" b="7 µm = 0,007 mm" />
        <Cell x={540} y={900} r={130 * sp(f, 6, 30)} />
        <line x1={410} y1={1090} x2={670} y2={1090} stroke={C.amber} strokeWidth={6} />
        <Tag x={540} y={1150} color={C.amber} size={44} o={sp(f, 26, 40)}>7 µm</Tag>
        <Tag x={540} y={1240} color={C.cream} size={36} o={sp(f, 36, 50)}>mỏng hơn sợi tóc</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="100 × 7 µm = 0,7 mm" b="đúng cỡ hạt cát thô" />
        {Array.from({length: 10}, (_, i) => (
          <Cell key={i} x={170 + i * 82} y={900} r={34} o={sp(f, b1 + 6 + i * 3, b1 + 18 + i * 3)} />
        ))}
        <Grain x={540} y={1100} r={50} o={sp(f, b1 + 36, b1 + 50)} />
        <Tag x={540} y={1230} color={C.amber} size={44} o={sp(f, b1 + 44, b1 + 58)}>= 0,7 mm</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="1 ml máu có" b="4–6 tỉ hồng cầu" />
        <path d="M 400 560 L 400 1060 Q 540 1140 680 1060 L 680 560" fill="none" stroke={C.cream} strokeWidth={7} />
        <path d="M 410 700 L 410 1050 Q 540 1120 670 1050 L 670 700 Z" fill={RBC} opacity={0.75} />
        {Array.from({length: 26}, (_, i) => (
          <Cell key={i} x={440 + ((i * 53) % 200) + Math.sin(f * 0.05 + i) * 6} y={740 + ((i * 97) % 280)} r={14} o={0.8} />
        ))}
        <Big x={540} y={1260} size={110} color={C.amber} o={sp(f, b2 + 24, b2 + 38)}>4–6 tỉ</Big>
      </g>
      <g opacity={V(3)}>
        <Head a="So với vật quen" b="rồi nhân lập phương" />
        <Grain x={250} y={940} r={70} />
        <line x1={380} y1={940} x2={470} y2={940} stroke={C.amber} strokeWidth={6} />
        <Cell x={560} y={940} r={34} o={sp(f, b3 + 10, b3 + 24)} />
        <line x1={640} y1={940} x2={730} y2={940} stroke={C.amber} strokeWidth={6} opacity={sp(f, b3 + 20, b3 + 34)} />
        <Big x={850} y={960} size={100} color={C.amber} o={sp(f, b3 + 26, b3 + 40)}>x³</Big>
        <Hero x={lerp(120, 940, seg(f, b3, b3 + 90))} y={1290} s={1.6} walk={f * 0.25} cheer={sp(f, b3 + 70, b3 + 90)} />
      </g>
    </Svg>
  );
};
