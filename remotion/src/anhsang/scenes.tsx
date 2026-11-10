import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, clamp01, seg, sp} from '../lib/theme';
import {Big, Hero, Lab, MagMark, Svg, lerp} from '../eratosthenes/v';

export type Sc = {dur: number; bs: number[]};

const D = C.dim;
const RAD = Math.PI / 180;
const LAMP = '#ffd884';
const JUP = '#c98f5e';
const EARTH = '#4a9aa6';

const Arrow: React.FC<{x1: number; y1: number; x2: number; y2: number; color?: string; w?: number; p?: number}> = ({x1, y1, x2, y2, color = C.amber, w = 8, p = 1}) => {
  const ex = lerp(x1, x2, p);
  const ey = lerp(y1, y2, p);
  const a = Math.atan2(y2 - y1, x2 - x1);
  const h = Math.max(14, w * 2.2);
  const hx = (k: number) => ex - h * Math.cos(a + k);
  const hy = (k: number) => ey - h * Math.sin(a + k);
  return (
    <g opacity={clamp01(p * 3)} stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" fill={color}>
      <line x1={x1} y1={y1} x2={ex} y2={ey} />
      <path d={`M ${ex} ${ey} L ${hx(0.5)} ${hy(0.5)} L ${hx(-0.5)} ${hy(-0.5)} Z`} />
    </g>
  );
};

const Sun: React.FC<{x: number; y: number; r: number; o?: number}> = ({x, y, r, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r * 1.7} fill="url(#sunGlow)" opacity={0.6} />
    <circle cx={x} cy={y} r={r} fill={C.amber} stroke={C.cream} strokeWidth={4} />
  </g>
);

const Planet: React.FC<{x: number; y: number; r: number; color?: string; o?: number; bands?: boolean}> = ({x, y, r, color = EARTH, o = 1, bands = false}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill={color} stroke={C.cream} strokeWidth={4} />
    {bands && (
      <g stroke="#7b4e2f" strokeWidth={r * 0.1} opacity={0.6} strokeLinecap="round">
        <line x1={x - r * 0.85} y1={y - r * 0.35} x2={x + r * 0.85} y2={y - r * 0.35} />
        <line x1={x - r * 0.98} y1={y + r * 0.05} x2={x + r * 0.98} y2={y + r * 0.05} />
        <line x1={x - r * 0.8} y1={y + r * 0.45} x2={x + r * 0.8} y2={y + r * 0.45} />
      </g>
    )}
  </g>
);

const Clock: React.FC<{x: number; y: number; r?: number; angle: number; color?: string; o?: number}> = ({x, y, r = 60, angle, color = C.cream, o = 1}) => (
  <g opacity={clamp01(o)}>
    <circle cx={x} cy={y} r={r} fill={C.bg1} stroke={color} strokeWidth={5} />
    <line x1={x} y1={y} x2={x + r * 0.75 * Math.sin(angle * RAD)} y2={y - r * 0.75 * Math.cos(angle * RAD)} stroke={C.amber} strokeWidth={6} strokeLinecap="round" />
    <circle cx={x} cy={y} r={5} fill={C.amberDeep} />
  </g>
);

const Lantern: React.FC<{x: number; y: number; on: number; s?: number}> = ({x, y, on, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <circle cx={0} cy={-18} r={90} fill="url(#sunGlow)" opacity={0.85 * clamp01(on)} />
    <line x1={0} y1={-60} x2={0} y2={-46} stroke={C.cream} strokeWidth={4} />
    <rect x={-16} y={-46} width={32} height={46} rx={8} fill={on > 0.5 ? LAMP : '#6b5a45'} stroke={C.cream} strokeWidth={4} />
  </g>
);

const Hill: React.FC<{x: number; y: number; w?: number; h?: number}> = ({x, y, w = 360, h = 90}) => (
  <path d={`M ${x - w / 2} ${y} Q ${x} ${y - h * 1.6} ${x + w / 2} ${y} Z`} fill="#3a2a1d" stroke={C.cream} strokeWidth={3} strokeOpacity={0.5} />
);

// ============ Bố cục chung (viết lại 10/11/2026) ============
// Vùng an toàn: tiêu đề y 200–340 (dưới logo), hình y 440–1260, phụ đề từ y 1330. Mọi chữ nằm trong x 90–990.
// Mỗi nhịp một tiêu đề ngắn nói đúng một ý; chữ nhỏ chỉ đi kèm vật trong hình.
const mkV = (f: number, bs: number[]) => (i: number) =>
  sp(f, bs[i] + 2, bs[i] + 14) * (i < bs.length - 1 ? 1 - sp(f, bs[i + 1] - 10, bs[i + 1]) : 1);

const Head: React.FC<{a: string; b?: string; o?: number}> = ({a, b, o = 1}) => (
  <g opacity={clamp01(o)}>
    <Lab x={540} y={b ? 252 : 290} size={52} color={C.cream}>{a}</Lab>
    {b && (
      <Lab x={540} y={322} size={52} color={C.amber}>
        {b}
      </Lab>
    )}
  </g>
);

const Tag: React.FC<{x: number; y: number; children: React.ReactNode; color?: string; o?: number; anchor?: 'start' | 'middle' | 'end'; size?: number}> = ({x, y, children, color = D, o = 1, anchor = 'middle', size = 36}) => (
  <Lab x={x} y={y} size={size} color={color} o={o} anchor={anchor}>
    {children}
  </Lab>
);

// ============ 1. Mở đầu ============
export const Hook: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const sunO = 1 - sp(f, 44, 58);
  const earthDim = sp(f, 134, 156);
  const t = 499 * (1 - seg(f, 52, 134));
  const mm = Math.floor(t / 60);
  const ss = Math.floor(t % 60);
  const dots = [0, 12, 24, 36];
  const sw = sp(f, b1 + 34, b1 + 38);
  const orb = (f - b2) * 3.2;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Mặt Trời tắt ngay bây giờ…" b="bạn vẫn thấy nó sáng thêm 8 phút" />
        <Sun x={540} y={580} r={90} o={sunO} />
        <line x1={540} y1={700} x2={540} y2={900} stroke={C.amber} strokeWidth={3} strokeDasharray="8 14" opacity={0.35} />
        {dots.map((s0, i) => {
          const k = seg(f, s0, s0 + 96);
          return k > 0 && k < 1 ? <circle key={i} cx={540} cy={lerp(700, 925, k)} r={12} fill={LAMP} opacity={0.95} /> : null;
        })}
        <Planet x={540} y={1030} r={100} o={1} />
        <circle cx={540} cy={1030} r={100} fill={C.bg2} opacity={0.6 * earthDim} />
        <g opacity={sp(f, 50, 66)}>
          <rect x={690} y={720} width={290} height={130} rx={20} fill={C.bg1} stroke={C.amber} strokeWidth={4} />
          <Big x={835} y={810} size={84} color={C.amber}>{`${mm}:${String(ss).padStart(2, '0')}`}</Big>
        </g>
        <Tag x={540} y={1190} color={C.cream} o={1 - earthDim} size={40}>Trái Đất vẫn sáng</Tag>
        <Tag x={540} y={1190} color={D} o={earthDim} size={40}>giờ mới tối</Tag>
        <Tag x={540} y={1245} color={D} size={28} o={0.8}>(hình minh họa)</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Nhưng bật đèn là sáng ngay" b="nhanh đến mức ta không kịp thấy" />
        <rect x={150} y={690} width={160} height={250} rx={24} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
        <rect x={205} y={lerp(740, 810, sw)} width={50} height={90} rx={12} fill={sw > 0.5 ? C.amber : D} />
        <line x1={310} y1={815} x2={520} y2={815} stroke={C.cream} strokeWidth={5} opacity={0.6} />
        <circle cx={730} cy={710} r={150} fill="url(#sunGlow)" opacity={0.95 * sw} />
        <circle cx={730} cy={710} r={70} fill={sw > 0.5 ? LAMP : '#6b5a45'} stroke={C.cream} strokeWidth={5} />
        <rect x={700} y={780} width={60} height={50} fill={C.bg1} stroke={C.cream} strokeWidth={4} />
        <Tag x={230} y={1000} color={D}>công tắc</Tag>
        <Tag x={730} y={1000} color={D}>đèn</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Người đầu tiên chứng minh điều đó" b="bằng một mặt trăng của sao Mộc" />
        <circle cx={540} cy={800} r={270} fill="none" stroke={C.cream} strokeWidth={3} strokeDasharray="6 14" opacity={0.5} />
        <Planet x={540} y={800} r={140} color={JUP} bands />
        <circle cx={540 + 270 * Math.cos(orb * RAD)} cy={800 + 270 * Math.sin(orb * RAD)} r={26} fill={C.cream} stroke={C.amberDeep} strokeWidth={4} />
        <Tag x={540} y={1150} color={C.cream} size={40}>sao Mộc và mặt trăng Io</Tag>
      </g>
    </Svg>
  );
};

// ============ 2. Hai chiếc đèn lồng của Galileo ============
export const Lantern2: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2, b3, b4] = bs;
  const field = sp(f, b1 + 2, b1 + 14) * (1 - sp(f, b4 - 10, b4));
  const on1 = sp(f, b2 + 14, b2 + 18);
  const on2 = sp(f, b2 + 52, b2 + 56);
  const go = seg(f, b2 + 18, b2 + 52);
  const back = seg(f, b2 + 56, b2 + 90);
  const px = go < 1 ? lerp(250, 830, go) : lerp(830, 250, back);
  const showPkt = (f > b2 + 18 && go < 1) || (f >= b2 + 52 && back < 1);
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Năm 1638, Galileo mô tả" b="một cách thử đo ánh sáng" />
        <rect x={290} y={520} width={500} height={360} rx={14} fill="#6b4a2e" stroke={C.cream} strokeWidth={6} />
        <rect x={310} y={542} width={460} height={316} rx={8} fill={C.cream} />
        <line x1={540} y1={542} x2={540} y2={858} stroke="#6b4a2e" strokeWidth={5} />
        {[0, 1, 2, 3, 4].map((i) => (
          <g key={i} stroke="#b9a584" strokeWidth={5} strokeLinecap="round">
            <line x1={340} y1={590 + i * 52} x2={510} y2={590 + i * 52} />
            <line x1={570} y1={590 + i * 52} x2={740} y2={590 + i * 52} />
          </g>
        ))}
        <Big x={540} y={1050} size={130} color={C.amber} o={sp(f, 14, 36)}>1638</Big>
      </g>
      <g opacity={field}>
        <g opacity={V(1)}>
          <Head a="Hai người, mỗi người một đèn lồng" b="đứng cách nhau chưa đầy 2 km" />
        </g>
        <g opacity={V(2)}>
          <Head a="Người 1 mở đèn. Người 2 thấy" b="thì mở đèn lại. Chờ bao lâu?" />
        </g>
        <g opacity={V(3)}>
          <Head a="Galileo không thấy độ trễ nào" b="với ông, ánh sáng nhanh vô cùng" />
        </g>
        <g transform="translate(0 -120)">
        <Hill x={250} y={1040} w={440} h={80} />
        <Hill x={830} y={1040} w={440} h={80} />
        <Hero x={250} y={965} s={1.8} p={sp(f, b1 + 6, b1 + 24)} stick={false} />
        <Hero x={830} y={965} s={1.8} p={sp(f, b1 + 14, b1 + 32)} stick={false} />
        <Lantern x={300} y={900} on={on1} />
        <Lantern x={780} y={900} on={on2} />
        <Arrow x1={250} y1={1130} x2={830} y2={1130} color={C.cream} w={5} p={sp(f, b1 + 30, b1 + 56)} />
        <Tag x={540} y={1195} color={C.cream} size={40} o={sp(f, b1 + 44, b1 + 64)}>chưa đầy 2 km</Tag>
        <Tag x={250} y={1090} color={D} size={30} o={sp(f, b1 + 20, b1 + 40)}>người 1</Tag>
        <Tag x={830} y={1090} color={D} size={30} o={sp(f, b1 + 20, b1 + 40)}>người 2</Tag>
        {showPkt && <circle cx={px} cy={760} r={14} fill={LAMP} />}
        <g opacity={V(2) * sp(f, b2 + 90, b2 + 110)}>
          <Big x={540} y={620} size={120} color={C.amber}>?</Big>
        </g>
        </g>
      </g>
      <g opacity={V(4)}>
        <Head a="Vì sao không thấy?" b="ánh sáng quá nhanh so với tay người" />
        <Tag x={110} y={560} color={C.cream} anchor="start" size={38}>ánh sáng chạy hết quãng đó</Tag>
        <rect x={110} y={590} width={8} height={56} rx={3} fill={C.amber} opacity={sp(f, b4 + 16, b4 + 30)} />
        <Tag x={140} y={700} color={C.amber} anchor="start" size={40} o={sp(f, b4 + 20, b4 + 40)}>5 phần triệu giây</Tag>
        <Tag x={110} y={830} color={C.cream} anchor="start" size={38} o={sp(f, b4 + 44, b4 + 60)}>bàn tay người phản ứng</Tag>
        <rect x={110} y={860} width={860 * sp(f, b4 + 50, b4 + 96)} height={56} rx={8} fill={C.cream} />
        <Tag x={110} y={990} color={C.amber} anchor="start" size={40} o={sp(f, b4 + 80, b4 + 100)}>chậm hơn hàng nghìn lần</Tag>
        <Tag x={540} y={1160} color={D} size={28} o={0.8}>(vẽ không đúng tỉ lệ)</Tag>
      </g>
    </Svg>
  );
};

// ============ 3. Mặt trăng Io làm đồng hồ ============
const JX0 = 540;
const JY0 = 830;
const IOR = 210;
const ioAt = (a: number) => ({x: JX0 + IOR * Math.cos(a * RAD), y: JY0 + IOR * Math.sin(a * RAD)});
const inShadowAt = (a: number) => {
  const p = ioAt(a);
  return p.x > JX0 && Math.abs(p.y - JY0) < 92;
};

export const Io: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [b0, b1, b2, b3, b4, b5, b6, b7] = bs;
  const ioA = (f - b1) * 2.4 - 40;
  const a360 = ((ioA % 360) + 360) % 360;
  const dark = inShadowAt(a360);
  const flash = Math.abs(a360 - 28) < 9;
  const io = ioAt(a360);
  const jup = V(1) + V(2) > 0.01;
  // hàng nhịp (b3)
  const t1 = seg(f, b3 + 10, b3 + 130);
  const t2 = seg(f, b3 + 150, b3 + 260);
  const m = t1 - 1.5 * t2;
  const earthX = 560 - 310 * t1 + 450 * t2;
  const tickX = (k: number) => 150 + k * 150;
  const lightK = (i: number) => (f * 0.014 + i * 0.33) % 1;
  return (
    <Svg>
      {/* b0: đài thiên văn */}
      <g opacity={V(0)}>
        <Head a="Năm 1672, nhà thiên văn trẻ" b="Ole Rømer đến Đài Paris" />
        <Big x={540} y={560} size={110} color={C.amber} o={sp(f, 10, 34)}>1672</Big>
        <rect x={360} y={780} width={340} height={170} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
        <path d="M 400 780 Q 530 630 660 780 Z" fill="#40505a" stroke={C.cream} strokeWidth={5} />
        <line x1={590} y1={720} x2={690} y2={640} stroke={C.amber} strokeWidth={14} strokeLinecap="round" />
        <Hero x={850} y={950} s={1.7} p={sp(f, b0 + 20, b0 + 38)} stick={false} />
        <Tag x={850} y={1010} color={C.amber} size={36}>Rømer</Tag>
        <Tag x={530} y={1010} color={C.cream} size={36}>Đài thiên văn Paris</Tag>
      </g>

      {/* b1, b2: sao Mộc và Io */}
      {jup && (
        <g opacity={Math.max(V(1), V(2))}>
          <path d="M 540 738 L 1030 770 L 1030 890 L 540 922 Z" fill="#0b0705" opacity={0.9 * V(2)} />
          <circle cx={JX0} cy={JY0} r={IOR} fill="none" stroke={C.cream} strokeWidth={3} strokeDasharray="6 12" opacity={0.45} />
          <Planet x={JX0} y={JY0} r={92} color={JUP} bands />
          <circle cx={io.x} cy={io.y} r={22} fill={C.cream} stroke={C.amberDeep} strokeWidth={4} opacity={dark ? 0.14 : 1} />
          {flash && <circle cx={io.x} cy={io.y} r={44} fill="none" stroke={C.amber} strokeWidth={7} opacity={V(2)} />}
        </g>
      )}
      <g opacity={V(1)}>
        <Head a="Io quay quanh sao Mộc" b="một vòng hết 42 tiếng rưỡi" />
        <Tag x={JX0} y={1150} color={C.cream}>sao Mộc</Tag>
        <Tag x={io.x + 34} y={io.y - 26} color={C.amber} anchor="start" size={34}>Io</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Mỗi vòng Io chui vào bóng rồi ló ra" b="mỗi lần ló ra là một nhịp đồng hồ" />
        <Sun x={110} y={JY0} r={38} />
        <Tag x={110} y={JY0 + 80} color={D} size={30}>Mặt Trời</Tag>
        <Tag x={860} y={690} color={C.cream} size={32}>bóng của sao Mộc</Tag>
        {flash && (
          <Big x={540} y={1150} size={90} color={C.amber}>
            tích!
          </Big>
        )}
      </g>

      {/* b3: Trái Đất đi xa / lại gần, hàng nhịp */}
      <g opacity={V(3)}>
        <Head a={f < b3 + 140 ? 'Trái Đất đi xa sao Mộc' : 'Trái Đất lại gần sao Mộc'} b={f < b3 + 140 ? 'Io ló ra muộn dần' : 'Io ló ra sớm hơn'} />
        <Planet x={900} y={560} r={44} color={JUP} bands />
        <Planet x={earthX} y={560} r={24} />
        <Tag x={900} y={650} color={D} size={30}>sao Mộc</Tag>
        <Tag x={earthX} y={650} color={D} size={30}>Trái Đất</Tag>
        <Tag x={110} y={756} color={D} anchor="start" size={34}>giờ ló ra theo tính toán</Tag>
        <Tag x={110} y={936} color={C.amber} anchor="start" size={34}>giờ ló ra thực tế</Tag>
        {[0, 1, 2, 3, 4, 5].map((k) => (
          <g key={k}>
            <rect x={tickX(k) - 8} y={790} width={16} height={70} rx={4} fill={D} />
            <rect x={tickX(k) - 8 + k * 16 * m} y={970} width={16} height={70} rx={4} fill={C.amber} />
            {Math.abs(k * 16 * m) > 6 && <line x1={tickX(k)} y1={862} x2={tickX(k) + k * 16 * m} y2={968} stroke={C.amber} strokeWidth={2} strokeDasharray="5 7" opacity={0.6} />}
          </g>
        ))}
      </g>

      {/* b4: 40 vòng */}
      <g opacity={V(4)}>
        <Head a="Mỗi vòng chỉ lệch chút xíu" b="gộp 40 vòng thì lệch rất rõ" />
        <Tag x={110} y={560} color={C.cream} anchor="start" size={38}>1 vòng: lệch rất nhỏ</Tag>
        <rect x={110} y={590} width={8} height={50} rx={3} fill={C.amber} />
        <Tag x={110} y={760} color={C.cream} anchor="start" size={38} o={sp(f, b4 + 36, b4 + 56)}>cộng 40 vòng: lệch rõ ràng</Tag>
        <rect x={110} y={790} width={860 * sp(f, b4 + 50, b4 + 110)} height={50} rx={8} fill={C.amber} />
        <Big x={540} y={1050} size={150} color={C.amber} o={sp(f, b4 + 60, b4 + 90)}>× 40</Big>
      </g>

      {/* b5: đường dài hơn thì ánh sáng tới muộn */}
      <g opacity={V(5)}>
        <Head a="Io vẫn quay đều" b="nhưng ánh sáng đi đường dài hơn" />
        <Planet x={900} y={700} r={36} color={JUP} bands />
        <Planet x={560} y={700} r={24} />
        <line x1={864} y1={700} x2={588} y2={700} stroke={LAMP} strokeWidth={5} strokeDasharray="10 10" />
        <Tag x={560} y={780} color={C.cream} size={36} o={sp(f, b5 + 20, b5 + 40)}>gần: ánh sáng tới sớm</Tag>
        <Planet x={900} y={960} r={36} color={JUP} bands />
        <Planet x={230} y={960} r={24} />
        <line x1={864} y1={960} x2={258} y2={960} stroke={LAMP} strokeWidth={5} strokeDasharray="10 10" />
        <Tag x={560} y={1040} color={C.amber} size={36} o={sp(f, b5 + 50, b5 + 70)}>xa: ánh sáng tới muộn</Tag>
        {[0, 1, 2].map((i) => (
          <g key={i}>
            <circle cx={lerp(864, 588, lightK(i))} cy={700} r={9} fill={LAMP} opacity={0.95} />
            <circle cx={lerp(864, 258, lightK(i + 1))} cy={960} r={9} fill={LAMP} opacity={0.95} />
          </g>
        ))}
      </g>

      {/* b6: lá thư */}
      <g opacity={V(6)}>
        <Head a="Giống thư gửi đều mỗi ngày" b="đường dài thì thư đến muộn" />
        <rect x={90} y={760} width={84} height={96} rx={10} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
        <rect x={112} y={790} width={40} height={10} fill={C.amber} />
        <Tag x={132} y={910} color={D} size={30}>gửi đều</Tag>
        <line x1={190} y1={720} x2={620} y2={720} stroke={C.cream} strokeWidth={4} opacity={0.6} />
        <line x1={190} y1={930} x2={970} y2={930} stroke={C.cream} strokeWidth={4} opacity={0.6} />
        {[0, 1, 2].map((i) => {
          const k = (seg(f, b6 + 20, b6 + 200) * 3 + i * 0.34) % 1;
          return (
            <g key={i}>
              <rect x={lerp(200, 600, k)} y={704} width={44} height={30} rx={4} fill={LAMP} opacity={Math.sin(k * Math.PI) * 1.3} />
              <rect x={lerp(200, 950, k)} y={914} width={44} height={30} rx={4} fill={LAMP} opacity={Math.sin(k * Math.PI) * 1.3} />
            </g>
          );
        })}
        <Tag x={190} y={680} color={C.cream} anchor="start" size={34}>đường ngắn: thư đến sớm</Tag>
        <Tag x={190} y={1000} color={C.amber} anchor="start" size={34}>đường dài: thư đến muộn dần</Tag>
      </g>

      {/* b7: 9/11/1676 */}
      <g opacity={V(7)}>
        <Head a="Ngày 9/11/1676, Io ló ra" b="muộn 10 phút so với bảng giờ" />
        <rect x={340} y={450} width={400} height={250} rx={20} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
        <rect x={340} y={450} width={400} height={74} rx={20} fill={C.amberDeep} />
        <Lab x={540} y={506} size={40} color={C.bg2} plain>1676</Lab>
        <Big x={540} y={650} size={110} color={C.cream}>9/11</Big>
        <Clock x={340} y={860} r={80} angle={0} o={sp(f, b7 + 20, b7 + 40)} />
        <Tag x={340} y={990} color={D} size={32} o={sp(f, b7 + 20, b7 + 40)}>bảng giờ tính từ tháng 8</Tag>
        <Clock x={740} y={860} r={80} angle={60 * sp(f, b7 + 50, b7 + 90)} color={C.amber} o={sp(f, b7 + 44, b7 + 64)} />
        <Tag x={740} y={990} color={C.amber} size={32} o={sp(f, b7 + 44, b7 + 64)}>thực tế</Tag>
        <Big x={540} y={1150} size={100} color={C.amber} o={sp(f, b7 + 80, b7 + 110)}>muộn 10 phút</Big>
      </g>
    </Svg>
  );
};

// ============ 4. 22 phút, người phản đối, người xác nhận ============
export const Romer: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2] = bs;
  const dash = sp(f, 24, 70);
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Rømer ước tính: ánh sáng cần" b="khoảng 22 phút qua quỹ đạo Trái Đất" />
        <circle cx={540} cy={760} r={280} fill="none" stroke={C.cream} strokeWidth={4} opacity={0.6} />
        <Sun x={540} y={760} r={50} />
        <Planet x={260} y={760} r={26} />
        <Planet x={820} y={760} r={26} />
        <Arrow x1={292} y1={760} x2={292 + 496 * dash} y2={760} color={C.amber} w={6} p={1} />
        <Tag x={540} y={1130} color={C.cream} size={36} o={sp(f, 40, 60)}>đường kính quỹ đạo Trái Đất</Tag>
        <Big x={540} y={1250} size={120} color={C.amber} o={sp(f, 50, 80)}>22 phút</Big>
      </g>
      <g opacity={V(1)}>
        <Head a="Giám đốc đài Cassini phản đối:" b="mặt trăng khác không có hiệu ứng ấy" />
        <Hero x={290} y={940} s={2.2} p={sp(f, b1 + 6, b1 + 24)} stick={false} />
        <Tag x={290} y={1010} color={C.cream}>Cassini</Tag>
        <g transform="translate(290 640)" stroke={C.amberDeep} strokeWidth={14} strokeLinecap="round" opacity={sp(f, b1 + 30, b1 + 44)}>
          <line x1={-50} y1={-50} x2={50} y2={50} />
          <line x1={50} y1={-50} x2={-50} y2={50} />
        </g>
        <Planet x={730} y={760} r={80} color={JUP} bands />
        {[0, 1, 2].map((i) => (
          <circle key={i} cx={730 + 140 * Math.cos((i * 120 + f * 2) * RAD)} cy={760 + 140 * Math.sin((i * 120 + f * 2) * RAD)} r={14} fill={C.cream} />
        ))}
        <Tag x={730} y={990} color={C.cream} size={34} o={sp(f, b1 + 36, b1 + 56)}>các mặt trăng khác</Tag>
        <Tag x={730} y={1040} color={C.amber} size={34} o={sp(f, b1 + 46, b1 + 66)}>không thấy hiệu ứng ấy</Tag>
      </g>
      <g opacity={V(2)}>
        <Head a="Năm 1729, James Bradley" b="đo bằng cách khác, cùng kết luận" />
        <g transform="translate(400 1000) rotate(-28)">
          <rect x={0} y={-30} width={420} height={60} rx={10} fill="#40505a" stroke={C.cream} strokeWidth={5} />
        </g>
        <circle cx={760} cy={650} r={16} fill={C.cream} />
        <line x1={760} y1={650} x2={560} y2={930} stroke={LAMP} strokeWidth={4} strokeDasharray="10 10" opacity={sp(f, b2 + 30, b2 + 56)} />
        <Tag x={760} y={605} color={D} size={30}>ngôi sao</Tag>
        <g opacity={sp(f, b2 + 70, b2 + 86)} stroke={C.amber} strokeWidth={14} strokeLinecap="round" fill="none">
          <path d="M 480 1170 l 36 40 l 78 -92" />
        </g>
        <Tag x={720} y={1195} color={C.amber} anchor="start" size={38} o={sp(f, b2 + 70, b2 + 90)}>tốc độ hữu hạn</Tag>
      </g>
    </Svg>
  );
};

// ============ 5. Phép chia ra tốc độ ============
const Frac: React.FC<{x: number; y: number; top: string; bottom: string; size?: number; o?: number; color?: string}> = ({x, y, top, bottom, size = 64, o = 1, color = C.cream}) => (
  <g opacity={clamp01(o)}>
    <Big x={x} y={y - 24} size={size} color={color}>{top}</Big>
    <line x1={x - 300} y1={y} x2={x + 300} y2={y} stroke={C.amber} strokeWidth={6} strokeLinecap="round" />
    <Big x={x} y={y + size + 6} size={size} color={color}>{bottom}</Big>
  </g>
);

export const Divide: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2, b3, b4] = bs;
  const board = sp(f, 0, 18) * (1 - sp(f, b4 - 10, b4));
  const real = sp(f, b3 + 20, b3 + 50);
  const icons = sp(f, b1 + 6, b1 + 30) * (1 - sp(f, b2 - 10, b2));
  const lap = seg(f, b4 + 10, b4 + 100) * 7.5;
  const ang = lap * 360;
  const head = f < b1 ? ['Giờ chỉ còn một phép chia', 'tốc độ = quãng đường ÷ thời gian'] : f < b2 ? ['Quãng đường khoảng 300 triệu km', 'thời gian 22 phút = 1 320 giây'] : f < b3 ? ['300 triệu ÷ 1 320', 'ra khoảng 227 nghìn km mỗi giây'] : ['Hơi thấp, vì ánh sáng thực', 'chỉ mất gần 17 phút'];
  return (
    <Svg>
      <g opacity={board}>
        <Head a={head[0]} b={head[1]} />
        <Big x={330} y={640} size={72} color={C.amber} anchor="end">tốc độ =</Big>
        <Frac x={650} y={650} top={f < b1 + 10 ? 'quãng đường' : '300 triệu km'} bottom={f < b1 + 10 ? 'thời gian' : f < b3 ? '1 320 giây' : '1 000 giây'} size={60} />
        <g opacity={icons}>
          <circle cx={270} cy={940} r={110} fill="none" stroke={C.cream} strokeWidth={4} opacity={0.6} />
          <Planet x={160} y={940} r={14} />
          <Planet x={380} y={940} r={14} />
          <line x1={176} y1={940} x2={364} y2={940} stroke={C.amber} strokeWidth={5} />
          <Tag x={270} y={1110} color={C.cream} size={34}>300 triệu km</Tag>
          <Clock x={780} y={940} r={90} angle={132 * sp(f, b1 + 20, b1 + 60)} />
          <Tag x={780} y={1110} color={C.cream} size={34}>22 phút</Tag>
        </g>
        <Big x={540} y={900} size={96} color={C.amber} o={sp(f, b2 + 10, b2 + 40) * (1 - real)}>≈ 227 nghìn km/giây</Big>
        <g opacity={real}>
          <Big x={540} y={880} size={96} color={C.amber}>≈ 300 nghìn km/giây</Big>
        </g>
        <g opacity={sp(f, b3 + 70, b3 + 96)}>
          <Tag x={110} y={1030} color={C.cream} anchor="start" size={34}>Rømer: 227 nghìn</Tag>
          <rect x={110} y={1045} width={860 * (227 / 300) * sp(f, b3 + 74, b3 + 110)} height={36} rx={8} fill={D} />
          <Tag x={110} y={1140} color={C.amber} anchor="start" size={34}>ánh sáng thực: 300 nghìn</Tag>
          <rect x={110} y={1155} width={860 * sp(f, b3 + 84, b3 + 120)} height={36} rx={8} fill={C.amber} />
        </g>
      </g>
      <g opacity={V(4)}>
        <Head a="Mỗi giây, ánh sáng chạy" b="quanh Trái Đất 7 vòng rưỡi" />
        <Planet x={540} y={880} r={140} />
        <circle cx={540} cy={880} r={225} fill="none" stroke={C.cream} strokeWidth={3} strokeDasharray="6 12" opacity={0.5} />
        <circle cx={540 + 225 * Math.cos((ang - 90) * RAD)} cy={880 + 225 * Math.sin((ang - 90) * RAD)} r={18} fill={LAMP} />
        <Big x={540} y={570} size={120} color={C.amber}>{`${(Math.floor(lap * 2) / 2).toFixed(1).replace('.', ',')} vòng`}</Big>
        <Tag x={540} y={1210} color={C.cream} size={40}>trong đúng 1 giây</Tag>
        <Tag x={540} y={1255} color={D} size={28}>(quay chậm lại cho dễ nhìn)</Tag>
      </g>
    </Svg>
  );
};

// ============ 6. Bánh xe răng cưa của Fizeau ============
const Wheel: React.FC<{x: number; y: number; r: number; angle: number; o?: number}> = ({x, y, r, angle, o = 1}) => (
  <g opacity={clamp01(o)} transform={`translate(${x} ${y}) rotate(${angle})`}>
    <circle cx={0} cy={0} r={r} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
    {Array.from({length: 24}).map((_, i) => (
      <rect key={i} x={-9} y={-r - 16} width={18} height={30} fill={C.cream} transform={`rotate(${i * 15})`} />
    ))}
    <circle cx={0} cy={0} r={14} fill={C.amberDeep} />
  </g>
);

export const WheelScene: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs);
  const [, b1, b2, b3, b4, b5, b6] = bs;
  const rig = sp(f, b2 + 2, b2 + 14) * (1 - sp(f, b6 - 10, b6));
  const out = seg(f, b2 + 24, b2 + 74);
  const ret = seg(f, b2 + 74, b2 + 124);
  const ang = f < b3 ? (f - b2) * 2 : f < b4 ? (f - b3) * 9 : (f - b4) * 18;
  const blocked = f >= b3 + 40 && f < b4;
  const through = f >= b4 + 40;
  const lightX = f < b2 + 74 ? lerp(300, 880, out) : lerp(880, 300, ret);
  const lightY = f < b2 + 74 ? 870 : 900;
  const showLight = f > b2 + 24 && !(f >= b2 + 124 && !through && !blocked);
  const stopAt = blocked ? Math.min(lightX, 330) : lightX;
  return (
    <Svg>
      <g opacity={V(0)}>
        <Head a="Năm 1849, Hippolyte Fizeau" b="đo ánh sáng ngay trên mặt đất" />
        <Big x={540} y={600} size={120} color={C.amber} o={sp(f, 10, 36)}>1849</Big>
        <Hero x={540} y={900} s={2.2} p={sp(f, 6, 24)} stick={false} />
        <Hill x={200} y={1090} w={420} h={90} />
        <Hill x={880} y={1090} w={420} h={90} />
        <Tag x={540} y={965} color={C.cream} size={36} o={sp(f, 14, 38)}>Hippolyte Fizeau</Tag>
      </g>
      <g opacity={V(1)}>
        <Head a="Hai kính thiên văn cách nhau" b="hơn 8,6 km: Suresnes và Montmartre" />
        <Hill x={200} y={1040} w={420} h={90} />
        <Hill x={880} y={1040} w={420} h={90} />
        <rect x={145} y={890} width={110} height={44} rx={8} fill="#40505a" stroke={C.cream} strokeWidth={4} />
        <rect x={825} y={890} width={110} height={44} rx={8} fill="#40505a" stroke={C.cream} strokeWidth={4} />
        <Tag x={200} y={840} color={C.cream} size={34}>Suresnes</Tag>
        <Tag x={880} y={840} color={C.cream} size={34}>Montmartre</Tag>
        <Arrow x1={200} y1={1140} x2={880} y2={1140} color={C.cream} w={5} p={sp(f, b1 + 14, b1 + 50)} />
        <Tag x={540} y={1200} color={C.amber} size={42} o={sp(f, b1 + 30, b1 + 54)}>hơn 8,6 km</Tag>
      </g>
      <g opacity={rig}>
        <g opacity={V(2)}>
          <Head a="Giữa đường là bánh xe 720 răng" b="ánh sáng chui qua khe, dội gương về" />
        </g>
        <g opacity={V(3)}>
          <Head a="Bánh xe quay nhanh dần: răng chắn" b="ánh sáng dội về, mắt không thấy gì" />
        </g>
        <g opacity={V(4)}>
          <Head a="Quay nhanh gấp đôi: ánh sáng" b="lại lọt qua khe kế bên" />
        </g>
        <g opacity={V(5)}>
          <Head a="Đó cũng là thời gian ánh sáng" b="đi hơn 17 km, cả đi lẫn về" />
        </g>
        <g transform="translate(0 -150)">
        <circle cx={90} cy={870} r={26} fill={LAMP} stroke={C.cream} strokeWidth={4} />
        <circle cx={90} cy={930} r={16} fill={C.bg2} stroke={C.cream} strokeWidth={4} />
        <line x1={90} y1={870} x2={300} y2={870} stroke={LAMP} strokeWidth={3} opacity={0.35} />
        <Wheel x={300} y={890} r={110} angle={ang} />
        <rect x={880} y={820} width={26} height={140} rx={6} fill="#9fb4bb" stroke={C.cream} strokeWidth={4} />
        <line x1={300} y1={870} x2={880} y2={870} stroke={C.cream} strokeWidth={2} strokeDasharray="4 12" opacity={0.4} />
        <line x1={300} y1={900} x2={880} y2={900} stroke={C.cream} strokeWidth={2} strokeDasharray="4 12" opacity={0.4} />
        {showLight && V(5) < 0.5 && <circle cx={stopAt} cy={lightY} r={13} fill={LAMP} />}
        <Tag x={300} y={1060} color={D} size={30}>bánh xe răng cưa</Tag>
        <Tag x={880} y={1010} color={D} size={30}>gương ở xa</Tag>
        <Tag x={90} y={800} color={D} size={30}>đèn</Tag>
        <Tag x={540} y={1245} color={D} size={28} o={V(2)}>(vẽ 24 răng cho dễ nhìn)</Tag>
        <g opacity={sp(f, b3 + 40, b3 + 60) * (1 - sp(f, b4 - 10, b4))}>
          <g transform="translate(330 900)" stroke={C.amberDeep} strokeWidth={10} strokeLinecap="round">
            <line x1={-30} y1={-30} x2={30} y2={30} />
            <line x1={30} y1={-30} x2={-30} y2={30} />
          </g>
        </g>
        <g opacity={V(4)}>
          <Big x={540} y={1195} size={84} color={C.amber}>25 vòng/giây</Big>
          <Tag x={540} y={1255} color={C.cream} size={36}>mỗi khe chuyển khe mất 55 phần triệu giây</Tag>
        </g>
        <g opacity={V(5)}>
          <Arrow x1={300} y1={1120} x2={880} y2={1120} color={C.amber} w={6} />
          <Arrow x1={880} y1={1165} x2={300} y2={1165} color={C.amber} w={6} />
          <Big x={590} y={1250} size={84} color={C.amber}>hơn 17 km</Big>
        </g>
        </g>
      </g>
      <g opacity={sp(f, b6 + 2, b6 + 14)}>
        <Head a="Phép chia cuối cùng" />
        <Frac x={540} y={600} top="17 km" bottom="55 phần triệu giây" size={62} />
        <Big x={540} y={900} size={100} color={C.amber} o={sp(f, b6 + 40, b6 + 70)}>≈ 313 nghìn km/giây</Big>
        <Tag x={110} y={1000} color={C.amber} anchor="start" size={34} o={sp(f, b6 + 90, b6 + 110)}>Fizeau: 313 nghìn</Tag>
        <rect x={110} y={1015} width={860 * sp(f, b6 + 80, b6 + 120)} height={36} rx={8} fill={C.amber} />
        <Tag x={110} y={1110} color={C.cream} anchor="start" size={34} o={sp(f, b6 + 100, b6 + 120)}>số đúng ngày nay: 299,8 nghìn</Tag>
        <rect x={110} y={1125} width={860 * (299.8 / 313.3) * sp(f, b6 + 90, b6 + 130)} height={36} rx={8} fill={C.cream} />
        <Big x={540} y={1250} size={84} color={C.amber} o={sp(f, b6 + 120, b6 + 150)}>chỉ lệch 4,5%</Big>
      </g>
    </Svg>
  );
};

// ============ 7. Kết ============
export const Outro: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const V = mkV(f, bs.slice(0, 3));
  const [, b1, b2, e] = bs;
  const fade = 1 - sp(f, e, e + 18);
  const lg = sp(f, e + 6, e + 28);
  const lx = lerp(110, 970, seg(f, b1 + 30, b1 + 90));
  const v2 = sp(f, b2 + 2, b2 + 14);
  return (
    <Svg>
      <g opacity={fade}>
        <g opacity={V(0)}>
          <Head a="Tốc độ ánh sáng ngày nay" b="được đo chính xác" />
          <Big x={540} y={760} size={124} color={C.amber}>299 792 458</Big>
          <Tag x={540} y={870} color={C.cream} size={48}>mét mỗi giây</Tag>
        </g>
        <g opacity={V(1)}>
          <Head a="Từ năm 1983, người ta lấy luôn" b="tốc độ ấy làm chuẩn: 1 mét" />
          <line x1={110} y1={780} x2={970} y2={780} stroke={C.cream} strokeWidth={14} strokeLinecap="round" />
          <line x1={110} y1={750} x2={110} y2={810} stroke={C.amber} strokeWidth={8} />
          <line x1={970} y1={750} x2={970} y2={810} stroke={C.amber} strokeWidth={8} />
          <Tag x={540} y={720} color={C.amber} size={44}>1 mét</Tag>
          <circle cx={lx} cy={780} r={16} fill={LAMP} />
          <Tag x={540} y={930} color={C.cream} size={42}>là quãng ánh sáng đi trong</Tag>
          <Big x={540} y={1040} size={84} color={C.amber}>1/299 792 458 giây</Big>
        </g>
        <g opacity={v2}>
          <Head a="Một đèn lồng, một mặt trăng," b="một bánh xe: ba cách đo ánh sáng" />
          <Lantern x={210} y={800} on={1} s={2.2} />
          <Planet x={540} y={760} r={70} color={JUP} bands />
          <circle cx={540 + 110 * Math.cos(f * 0.1)} cy={760 + 110 * Math.sin(f * 0.1)} r={14} fill={C.cream} />
          <Wheel x={870} y={780} r={70} angle={f * 3} />
          <Tag x={210} y={950} color={C.cream} size={34}>đèn lồng</Tag>
          <Tag x={540} y={950} color={C.cream} size={34}>mặt trăng Io</Tag>
          <Tag x={870} y={950} color={C.cream} size={34}>bánh xe</Tag>
          <Hero x={540} y={1200} s={1.8} cheer={sp(f, b2 + 40, b2 + 60)} walk={f * 0.3} stick={false} />
        </g>
      </g>
      <g opacity={lg} transform={`translate(0 ${(1 - lg) * 20})`}>
        <g transform="translate(465 700) scale(3.4)">
          <MagMark size={44} raw />
        </g>
        <text x={540} y={930} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={74} fill={C.cream}>
          Người <tspan fill={C.amber}>Giải Mã</tspan>
        </text>
        <Lab x={540} y={1010} size={38} color={C.cream}>Đo ánh sáng bằng đèn lồng, mặt trăng và bánh xe.</Lab>
      </g>
    </Svg>
  );
};
