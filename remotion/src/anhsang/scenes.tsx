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

// ============ 1. Mở đầu ============
export const Hook: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const [, b1, b2] = bs;
  const c0 = sp(f, 0, 14) * (1 - sp(f, b1 - 6, b1 + 8));
  const c1 = sp(f, b1 + 4, b1 + 18) * (1 - sp(f, b2 - 6, b2 + 8));
  const c2 = sp(f, b2 + 4, b2 + 20);
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
      <g opacity={c0}>
        <Sun x={540} y={480} r={90} o={sunO} />
        <Lab x={540} y={620} size={40} color={C.amber} o={sp(f, 46, 64)}>Mặt Trời tắt</Lab>
        <line x1={540} y1={640} x2={540} y2={900} stroke={C.amber} strokeWidth={3} strokeDasharray="8 14" opacity={0.35} />
        {dots.map((s0, i) => {
          const k = seg(f, s0, s0 + 96);
          return k > 0 && k < 1 ? <circle key={i} cx={540} cy={lerp(640, 905, k)} r={12} fill={LAMP} opacity={0.95} /> : null;
        })}
        <Planet x={540} y={1010} r={100} o={1} />
        <circle cx={540} cy={1010} r={100} fill={C.bg2} opacity={0.6 * earthDim} />
        <Lab x={540} y={1170} size={40} color={C.cream} o={1 - earthDim}>Trái Đất vẫn sáng</Lab>
        <Lab x={540} y={1170} size={40} color={D} o={earthDim}>giờ mới tối</Lab>
        <g opacity={sp(f, 50, 66)}>
          <rect x={650} y={680} width={330} height={150} rx={20} fill={C.bg1} stroke={C.amber} strokeWidth={4} />
          <Big x={815} y={780} size={96} color={C.amber}>{`${mm}:${String(ss).padStart(2, '0')}`}</Big>
        </g>
        <Hero x={190} y={1250} s={1.7} p={sp(f, 6, 22)} />
      </g>
      <g opacity={c1}>
        <rect x={150} y={780} width={160} height={250} rx={24} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
        <rect x={205} y={lerp(830, 900, sw)} width={50} height={90} rx={12} fill={sw > 0.5 ? C.amber : D} />
        <line x1={310} y1={905} x2={520} y2={905} stroke={C.cream} strokeWidth={5} opacity={0.6} />
        <circle cx={700} cy={800} r={150} fill="url(#sunGlow)" opacity={0.95 * sw} />
        <circle cx={700} cy={800} r={70} fill={sw > 0.5 ? LAMP : '#6b5a45'} stroke={C.cream} strokeWidth={5} />
        <rect x={670} y={870} width={60} height={50} fill={C.bg1} stroke={C.cream} strokeWidth={4} />
        <Lab x={540} y={1200} size={44} color={C.amber} o={sp(f, b1 + 40, b1 + 60)}>bật đèn: sáng ngay</Lab>
      </g>
      <g opacity={c2}>
        <circle cx={540} cy={800} r={290} fill="none" stroke={C.cream} strokeWidth={3} strokeDasharray="6 14" opacity={0.5} />
        <Planet x={540} y={800} r={150} color={JUP} bands />
        <circle cx={540 + 290 * Math.cos(orb * RAD)} cy={800 + 290 * Math.sin(orb * RAD)} r={26} fill={C.cream} stroke={C.amberDeep} strokeWidth={4} />
        <Lab x={540} y={1190} size={44} color={C.cream} o={sp(f, b2 + 20, b2 + 40)}>sao Mộc và mặt trăng Io</Lab>
        <Big x={540} y={470} size={150} color={C.amber} o={sp(f, b2 + 30, b2 + 56)}>?</Big>
      </g>
    </Svg>
  );
};

// ============ 2. Hai chiếc đèn lồng của Galileo ============
export const Lantern2: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const [b0, b1, b2, b3, b4] = bs;
  const o = (a: number, z: number) => sp(f, a + 4, a + 20) * (1 - sp(f, z - 6, z + 8));
  const cBook = sp(f, 0, 18) * (1 - sp(f, b1 - 6, b1 + 8));
  const cField = sp(f, b1 + 4, b1 + 20) * (1 - sp(f, b4 - 6, b4 + 8));
  const cBars = sp(f, b4 + 4, b4 + 20);
  const on1 = sp(f, b2 + 14, b2 + 18);
  const on2 = sp(f, b2 + 52, b2 + 56);
  const go = seg(f, b2 + 18, b2 + 52);
  const back = seg(f, b2 + 56, b2 + 90);
  const px = go < 1 ? lerp(250, 830, go) : lerp(830, 250, back);
  const showPkt = (f > b2 + 18 && go < 1) || (f >= b2 + 52 && back < 1);
  return (
    <Svg>
      <g opacity={cBook}>
        <rect x={290} y={650} width={500} height={360} rx={14} fill="#6b4a2e" stroke={C.cream} strokeWidth={6} />
        <rect x={310} y={672} width={460} height={316} rx={8} fill={C.cream} />
        <line x1={540} y1={672} x2={540} y2={988} stroke="#6b4a2e" strokeWidth={5} />
        {[0, 1, 2, 3, 4].map((i) => (
          <g key={i} stroke="#b9a584" strokeWidth={5} strokeLinecap="round">
            <line x1={340} y1={720 + i * 52} x2={510} y2={720 + i * 52} />
            <line x1={570} y1={720 + i * 52} x2={740} y2={720 + i * 52} />
          </g>
        ))}
        <Big x={540} y={560} size={110} color={C.amber} o={sp(f, 14, 36)}>1638</Big>
        <Lab x={540} y={1110} size={44} color={C.cream} o={sp(f, 20, 40)}>Galileo mô tả một cách thử</Lab>
      </g>
      <g opacity={cField}>
        <Hill x={250} y={1040} w={440} h={80} />
        <Hill x={830} y={1040} w={440} h={80} />
        <Hero x={250} y={965} s={1.8} p={sp(f, b1 + 6, b1 + 24)} stick={false} />
        <Hero x={830} y={965} s={1.8} p={sp(f, b1 + 14, b1 + 32)} stick={false} />
        <Lantern x={300} y={900} on={on1 * (1 - sp(f, b2 + 60, b2 + 62) * 0)} />
        <Lantern x={780} y={900} on={on2} />
        <Arrow x1={250} y1={1160} x2={830} y2={1160} color={C.cream} w={5} p={sp(f, b1 + 30, b1 + 56)} />
        <Lab x={540} y={1215} size={42} color={C.cream} o={sp(f, b1 + 44, b1 + 64)}>chưa đầy 2 km</Lab>
        {showPkt && <circle cx={px} cy={820} r={14} fill={LAMP} />}
        <g opacity={sp(f, b2 + 6, b2 + 24) * (1 - sp(f, b3 + 40, b3 + 54))}>
          <rect x={410} y={420} width={260} height={120} rx={18} fill={C.bg1} stroke={C.amber} strokeWidth={4} />
          <Big x={540} y={500} size={74} color={C.amber}>{f < b2 + 90 ? '…' : '?'}</Big>
        </g>
        <Lab x={540} y={380} size={36} color={D} o={sp(f, b2 + 6, b2 + 24) * (1 - sp(f, b3 + 40, b3 + 54))}>chờ bao lâu?</Lab>
        <Lab x={540} y={620} size={46} color={C.amber} o={sp(f, b3 + 10, b3 + 34)}>không thấy độ trễ nào</Lab>
      </g>
      <g opacity={cBars}>
        <Lab x={110} y={620} size={36} color={D} anchor="start">ánh sáng chạy hết quãng đó</Lab>
        <rect x={110} y={650} width={4} height={56} fill={C.amber} opacity={sp(f, b4 + 16, b4 + 30)} />
        <Lab x={130} y={760} size={34} color={C.amber} anchor="start" o={sp(f, b4 + 20, b4 + 40)}>5 phần triệu giây</Lab>
        <Lab x={110} y={900} size={36} color={D} anchor="start" o={sp(f, b4 + 44, b4 + 60)}>bàn tay người phản ứng</Lab>
        <rect x={110} y={930} width={860 * sp(f, b4 + 50, b4 + 96)} height={56} rx={8} fill={C.cream} />
        <Lab x={110} y={1040} size={34} color={C.cream} anchor="start" o={sp(f, b4 + 80, b4 + 100)}>chậm hơn hàng nghìn lần</Lab>
        <Lab x={540} y={1190} size={28} color={D} o={0.8}>(vẽ không đúng tỉ lệ)</Lab>
      </g>
    </Svg>
  );
};

// ============ 3. Mặt trăng Io làm đồng hồ ============
const SX = 190;
const SY = 960;
const JX = 800;
const ER = 130;
const IR = 120;
const shadowH = (x: number) => lerp(62, 44, clamp01((x - JX) / 260));

const System: React.FC<{earthA: number; ioA: number; o?: number; ring?: number; showShadow?: boolean; ghost?: boolean; line?: number}> = ({earthA, ioA, o = 1, ring = 0.25, ghost = false, line = 0}) => {
  const ex = SX + ER * Math.cos(earthA * RAD);
  const ey = SY + ER * Math.sin(earthA * RAD);
  const ix = JX + IR * Math.cos(ioA * RAD);
  const iy = SY + IR * Math.sin(ioA * RAD);
  const inShadow = ix > JX && Math.abs(iy - SY) < shadowH(ix);
  const gx = SX + ER;
  return (
    <g opacity={clamp01(o)}>
      <path d={`M ${JX} ${SY - 62} L 1040 ${SY - 44} L 1040 ${SY + 44} L ${JX} ${SY + 62} Z`} fill="#0b0705" opacity={0.85} />
      <circle cx={SX} cy={SY} r={ER} fill="none" stroke={C.cream} strokeWidth={2} strokeDasharray="6 10" opacity={0.4} />
      <Sun x={SX} y={SY} r={44} />
      <circle cx={JX} cy={SY} r={IR} fill="none" stroke={C.cream} strokeWidth={3} strokeDasharray="6 10" opacity={ring} />
      <Planet x={JX} y={SY} r={62} color={JUP} bands />
      {ghost && <circle cx={gx} cy={SY} r={20} fill="none" stroke={D} strokeWidth={3} strokeDasharray="5 6" />}
      {line > 0 && <line x1={JX} y1={SY} x2={lerp(JX, ex, line)} y2={lerp(SY, ey, line)} stroke={LAMP} strokeWidth={4} strokeDasharray="10 10" />}
      {line > 0 && ghost && <line x1={JX} y1={SY + 6} x2={lerp(JX, gx, line)} y2={SY + 6} stroke={D} strokeWidth={4} strokeDasharray="10 10" />}
      <Planet x={ex} y={ey} r={20} />
      <circle cx={ix} cy={iy} r={15} fill={C.cream} stroke={C.amberDeep} strokeWidth={3} opacity={inShadow ? 0.12 : 1} />
    </g>
  );
};

export const Io: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const [b0, b1, b2, b3, b4, b5, b6, b7] = bs;
  const win = (a: number, z: number) => sp(f, a + 4, a + 20) * (1 - sp(f, z - 6, z + 8));
  const ioA = f * 2.4 - 40;
  const earthA = 160 * sp(f, b3 + 10, b3 + 110);
  const ph = (((ioA % 360) + 360) % 360);
  const flash = Math.abs(ph - 31) < 7 ? 1 : 0;
  const sysO = sp(f, 0, 16) * (1 - sp(f, b6 - 6, b6 + 8)) + sp(f, b7 + 40, b7 + 40) * 0;
  const sysBack = sp(f, b7 + 120, b7 + 140);
  const letter = win(b6, b7);
  const cal = sp(f, b7 + 4, b7 + 20);
  const lp = (k: number, x1: number, x2: number) => lerp(x1, x2, seg(f, b6 + 30, b6 + 30 + k));
  return (
    <Svg>
      <System earthA={earthA} ioA={ioA} o={(f < b6 ? sp(f, 0, 16) : 0) * (1 - sp(f, b6 - 6, b6 + 8)) * (f < b7 ? 1 : 0.0)} ring={f > b1 + 4 && f < b2 ? 0.9 : 0.25} ghost={f >= b5} line={f >= b5 ? sp(f, b5 + 6, b5 + 36) : 0} />
      {f > b3 + 20 && f < b6 && (
        <g>
          {[0, 1, 2, 3].map((i) => {
            const k = ((f * 0.012 + i * 0.25) % 1);
            const ex = SX + ER * Math.cos(earthA * RAD);
            const ey = SY + ER * Math.sin(earthA * RAD);
            return <circle key={i} cx={lerp(JX, ex, k)} cy={lerp(SY, ey, k)} r={9} fill={LAMP} opacity={0.9 * Math.sin(k * Math.PI)} />;
          })}
        </g>
      )}
      {/* 9: Đài thiên văn */}
      <g opacity={win(b0, b1)}>
        <rect x={380} y={520} width={320} height={160} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
        <path d="M 420 520 Q 540 380 660 520 Z" fill="#40505a" stroke={C.cream} strokeWidth={5} />
        <line x1={600} y1={470} x2={690} y2={400} stroke={C.amber} strokeWidth={14} strokeLinecap="round" />
        <Lab x={540} y={740} size={42} color={C.cream}>Đài thiên văn Paris, 1672</Lab>
        <Hero x={850} y={700} s={1.6} p={sp(f, b0 + 20, b0 + 38)} stick={false} />
        <Lab x={850} y={750} size={32} color={C.amber}>Rømer</Lab>
      </g>
      {/* 10: 42 tiếng rưỡi */}
      <g opacity={win(b1, b2)}>
        <Big x={540} y={600} size={96} color={C.amber}>42 tiếng rưỡi</Big>
        <Lab x={540} y={690} size={40} color={C.cream}>Io quay một vòng quanh sao Mộc</Lab>
        <Lab x={JX} y={SY + 160} size={32} color={D}>sao Mộc</Lab>
      </g>
      {/* 11: chui vào bóng */}
      <g opacity={win(b2, b3)}>
        <Lab x={900} y={SY - 110} size={34} color={C.cream}>bóng của sao Mộc</Lab>
        <Lab x={540} y={620} size={46} color={C.cream}>chui vào bóng: biến mất</Lab>
        <Lab x={540} y={690} size={46} color={C.amber}>ló ra: một nhịp "tích"</Lab>
        {flash > 0 && <circle cx={JX + 120 * Math.cos(31 * RAD)} cy={SY + 120 * Math.sin(31 * RAD)} r={34} fill="none" stroke={C.amber} strokeWidth={6} />}
      </g>
      {/* 12: Trái Đất đi xa thì Io ló ra muộn */}
      <g opacity={win(b3, b4)}>
        <Lab x={540} y={620} size={46} color={C.cream} o={sp(f, b3 + 10, b3 + 30)}>Trái Đất đi xa dần sao Mộc</Lab>
        <Lab x={540} y={690} size={46} color={C.amber} o={sp(f, b3 + 70, b3 + 100)}>Io ló ra càng muộn</Lab>
        <Lab x={SX} y={SY + 190} size={32} color={D}>Mặt Trời</Lab>
      </g>
      {/* 13: 40 vòng */}
      <g opacity={win(b4, b5)}>
        <Lab x={110} y={560} size={38} color={D} anchor="start">1 vòng: lệch rất nhỏ</Lab>
        <rect x={110} y={585} width={6} height={44} fill={C.amber} />
        <Lab x={110} y={720} size={38} color={C.cream} anchor="start" o={sp(f, b4 + 40, b4 + 60)}>gộp 40 vòng: hiện rõ</Lab>
        <rect x={110} y={745} width={860 * sp(f, b4 + 50, b4 + 110)} height={44} rx={8} fill={C.amber} />
        <Big x={900} y={540} size={110} color={C.amber} o={sp(f, b4 + 44, b4 + 70)}>×40</Big>
      </g>
      {/* 14: đường dài hơn thì tới muộn */}
      <g opacity={win(b5, b6)}>
        <Lab x={540} y={600} size={46} color={C.cream}>Io vẫn quay đều</Lab>
        <Lab x={540} y={670} size={46} color={C.amber} o={sp(f, b5 + 40, b5 + 64)}>nhưng ánh sáng đi đường dài hơn</Lab>
        <Lab x={420} y={SY + 190} size={30} color={D} o={sp(f, b5 + 30, b5 + 50)}>đường ngắn (nét xám)</Lab>
      </g>
      {/* 15: lá thư */}
      <g opacity={letter}>
        <rect x={90} y={820} width={80} height={90} rx={10} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
        <rect x={110} y={845} width={40} height={10} fill={C.amber} />
        <Lab x={130} y={965} size={30} color={D}>gửi đều</Lab>
        <line x1={190} y1={870} x2={640} y2={870} stroke={C.cream} strokeWidth={4} opacity={0.6} />
        <line x1={190} y1={1050} x2={990} y2={1050} stroke={C.cream} strokeWidth={4} opacity={0.6} />
        <rect x={lp(70, 200, 620)} y={850} width={44} height={30} rx={4} fill={LAMP} />
        <rect x={lp(70, 200, 970)} y={1030} width={44} height={30} rx={4} fill={LAMP} />
        <Lab x={640} y={820} size={34} color={C.cream} anchor="start" o={sp(f, b6 + 60, b6 + 90)}>đường ngắn: đến sớm</Lab>
        <Lab x={990} y={1110} size={34} color={C.amber} anchor="end" o={sp(f, b6 + 70, b6 + 100)}>đường dài: đến muộn dần</Lab>
      </g>
      {/* 16: ngày 9/11/1676 */}
      <g opacity={cal}>
        <rect x={110} y={560} width={420} height={300} rx={20} fill={C.bg1} stroke={C.cream} strokeWidth={5} />
        <rect x={110} y={560} width={420} height={80} rx={20} fill={C.amberDeep} />
        <Big x={320} y={780} size={90} color={C.cream}>9/11</Big>
        <Lab x={320} y={620} size={40} color={C.bg2} plain>1676</Lab>
        <Clock x={700} y={640} r={70} angle={0} o={sp(f, b7 + 20, b7 + 40)} />
        <Lab x={700} y={770} size={28} color={D} o={sp(f, b7 + 20, b7 + 40)}>bảng giờ (từ tháng 8)</Lab>
        <Clock x={900} y={640} r={70} angle={60 * sp(f, b7 + 50, b7 + 90)} color={C.amber} o={sp(f, b7 + 44, b7 + 64)} />
        <Lab x={900} y={770} size={28} color={C.amber} o={sp(f, b7 + 44, b7 + 64)}>thực tế</Lab>
        <Big x={800} y={900} size={96} color={C.amber} o={sp(f, b7 + 80, b7 + 110)}>muộn 10 phút</Big>
      </g>
    </Svg>
  );
};

// ============ 4. 22 phút, người phản đối, người xác nhận ============
export const Romer: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const [, b1, b2] = bs;
  const win = (a: number, z: number) => sp(f, a + 4, a + 20) * (1 - sp(f, z - 6, z + 8));
  const c0 = sp(f, 0, 16) * (1 - sp(f, b1 - 6, b1 + 8));
  const c1 = win(b1, b2);
  const c2 = sp(f, b2 + 4, b2 + 20);
  const dash = sp(f, 24, 70);
  return (
    <Svg>
      <g opacity={c0}>
        <circle cx={540} cy={800} r={300} fill="none" stroke={C.cream} strokeWidth={4} opacity={0.6} />
        <Sun x={540} y={800} r={52} />
        <Planet x={240} y={800} r={26} />
        <Planet x={840} y={800} r={26} />
        <Arrow x1={270} y1={800} x2={270 + 540 * dash} y2={800} color={C.amber} w={6} p={1} />
        <Lab x={540} y={1180} size={40} color={C.cream} o={sp(f, 40, 60)}>đường kính quỹ đạo Trái Đất</Lab>
        <Big x={540} y={540} size={130} color={C.amber} o={sp(f, 50, 80)}>22 phút</Big>
        <Lab x={540} y={610} size={34} color={D} o={sp(f, 50, 80)}>ánh sáng đi hết (theo ước tính của Rømer)</Lab>
      </g>
      <g opacity={c1}>
        <Hero x={300} y={900} s={2.2} p={sp(f, b1 + 6, b1 + 24)} stick={false} />
        <Lab x={300} y={960} size={36} color={C.cream}>Cassini</Lab>
        <g transform="translate(300 620)" stroke={C.amberDeep} strokeWidth={14} strokeLinecap="round" opacity={sp(f, b1 + 30, b1 + 44)}>
          <line x1={-50} y1={-50} x2={50} y2={50} />
          <line x1={50} y1={-50} x2={-50} y2={50} />
        </g>
        <Planet x={720} y={640} r={70} color={JUP} bands />
        {[0, 1, 2].map((i) => (
          <circle key={i} cx={720 + 120 * Math.cos((i * 120 + f * 2) * RAD)} cy={640 + 120 * Math.sin((i * 120 + f * 2) * RAD)} r={14} fill={C.cream} />
        ))}
        <Lab x={720} y={850} size={36} color={C.cream} o={sp(f, b1 + 36, b1 + 56)}>các mặt trăng khác</Lab>
        <Lab x={720} y={905} size={36} color={C.amber} o={sp(f, b1 + 46, b1 + 66)}>không thấy hiệu ứng ấy</Lab>
      </g>
      <g opacity={c2}>
        <Big x={540} y={540} size={140} color={C.amber} o={sp(f, b2 + 8, b2 + 34)}>1729</Big>
        <Lab x={540} y={620} size={40} color={C.cream} o={sp(f, b2 + 14, b2 + 38)}>James Bradley</Lab>
        <g transform="translate(400 1080) rotate(-28)">
          <rect x={0} y={-30} width={420} height={60} rx={10} fill="#40505a" stroke={C.cream} strokeWidth={5} />
        </g>
        <circle cx={760} cy={730} r={16} fill={C.cream} />
        <line x1={760} y1={730} x2={560} y2={1010} stroke={LAMP} strokeWidth={4} strokeDasharray="10 10" opacity={sp(f, b2 + 30, b2 + 56)} />
        <Lab x={540} y={1240} size={42} color={C.cream} o={sp(f, b2 + 44, b2 + 64)}>cách đo hoàn toàn khác</Lab>
        <g opacity={sp(f, b2 + 70, b2 + 86)} stroke={C.amber} strokeWidth={14} strokeLinecap="round" fill="none">
          <path d="M 790 1180 l 30 34 l 66 -80" />
        </g>
        <Lab x={540} y={1300} size={38} color={C.amber} o={sp(f, b2 + 70, b2 + 90)}>ánh sáng cũng có tốc độ hữu hạn</Lab>
      </g>
    </Svg>
  );
};

// ============ 5. Phép chia ra tốc độ ============
const Frac: React.FC<{x: number; y: number; top: string; bottom: string; size?: number; o?: number; color?: string}> = ({x, y, top, bottom, size = 64, o = 1, color = C.cream}) => (
  <g opacity={clamp01(o)}>
    <Big x={x} y={y - 24} size={size} color={color}>{top}</Big>
    <line x1={x - 330} y1={y} x2={x + 330} y2={y} stroke={C.amber} strokeWidth={6} strokeLinecap="round" />
    <Big x={x} y={y + size + 6} size={size} color={color}>{bottom}</Big>
  </g>
);

export const Divide: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const [b0, b1, b2, b3, b4] = bs;
  const board = sp(f, 0, 18) * (1 - sp(f, b4 - 6, b4 + 8));
  const c4 = sp(f, b4 + 4, b4 + 20);
  const lap = seg(f, b4 + 10, b4 + 170) * 7.5;
  const ang = lap * 360;
  const real = sp(f, b3 + 20, b3 + 50);
  return (
    <Svg>
      <g opacity={board}>
        <Big x={290} y={520} size={80} color={C.amber} anchor="end">tốc độ =</Big>
        <Frac x={620} y={540} top={f < b1 + 10 ? 'quãng đường' : '300 triệu km'} bottom={f < b1 + 10 ? 'thời gian' : f < b3 ? '1 320 giây' : '1 000 giây'} size={62} />
        <g opacity={sp(f, b1 + 6, b1 + 30)}>
          <circle cx={250} cy={1000} r={110} fill="none" stroke={C.cream} strokeWidth={4} opacity={0.6} />
          <Planet x={140} y={1000} r={14} />
          <Planet x={360} y={1000} r={14} />
          <line x1={156} y1={1000} x2={344} y2={1000} stroke={C.amber} strokeWidth={5} />
          <Lab x={250} y={1170} size={30} color={D}>300 triệu km</Lab>
          <Clock x={760} y={1000} r={90} angle={132 * sp(f, b1 + 20, b1 + 60)} />
          <Lab x={760} y={1170} size={30} color={D}>22 phút</Lab>
        </g>
        <Big x={540} y={820} size={90} color={C.amber} o={sp(f, b2 + 10, b2 + 40) * (1 - real)}>≈ 227 nghìn km/giây</Big>
        <g opacity={real}>
          <Lab x={540} y={720} size={38} color={D}>ánh sáng thực chỉ mất gần 17 phút</Lab>
          <Big x={540} y={840} size={90} color={C.amber}>≈ 300 nghìn km/giây</Big>
        </g>
        <g opacity={sp(f, b3 + 70, b3 + 96)}>
          <rect x={110} y={1240} width={860 * (227 / 300) * sp(f, b3 + 74, b3 + 110)} height={36} rx={8} fill={D} />
          <rect x={110} y={1290} width={860 * sp(f, b3 + 84, b3 + 120)} height={36} rx={8} fill={C.amber} />
          <Lab x={110} y={1230} size={28} color={D} anchor="start">Rømer 227 nghìn</Lab>
        </g>
      </g>
      <g opacity={c4}>
        <Planet x={540} y={880} r={150} />
        <circle cx={540} cy={880} r={235} fill="none" stroke={C.cream} strokeWidth={3} strokeDasharray="6 12" opacity={0.5} />
        <circle cx={540 + 235 * Math.cos((ang - 90) * RAD)} cy={880 + 235 * Math.sin((ang - 90) * RAD)} r={18} fill={LAMP} />
        <Big x={540} y={520} size={130} color={C.amber}>{`${(Math.floor(lap * 2) / 2).toFixed(1).replace('.', ',')} vòng`}</Big>
        <Lab x={540} y={1190} size={44} color={C.cream}>trong đúng 1 giây</Lab>
        <Lab x={540} y={1250} size={28} color={D}>(quay chậm lại cho dễ nhìn)</Lab>
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
  const [b0, b1, b2, b3, b4, b5, b6] = bs;
  const win = (a: number, z: number) => sp(f, a + 4, a + 20) * (1 - sp(f, z - 6, z + 8));
  const cA = sp(f, 0, 16) * (1 - sp(f, b2 - 6, b2 + 8));
  const cB = win(b2, b6);
  const cC = sp(f, b6 + 4, b6 + 20);
  // chùm sáng
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
      <g opacity={cA}>
        <Hill x={200} y={1040} w={420} h={90} />
        <Hill x={880} y={1040} w={420} h={90} />
        <Hero x={540} y={790} s={2.0} p={sp(f, 6, 24)} stick={false} />
        <Big x={540} y={440} size={120} color={C.amber} o={sp(f, 10, 36)}>1849</Big>
        <Lab x={540} y={850} size={38} color={C.cream} o={sp(f, 14, 38)}>Hippolyte Fizeau</Lab>
        <Lab x={540} y={1190} size={42} color={C.cream} o={sp(f, 30, 52)}>đo ngay trên mặt đất</Lab>
        <g opacity={sp(f, b1 + 6, b1 + 26)}>
          <rect x={150} y={880} width={110} height={40} rx={8} fill="#40505a" stroke={C.cream} strokeWidth={4} />
          <rect x={830} y={880} width={110} height={40} rx={8} fill="#40505a" stroke={C.cream} strokeWidth={4} />
          <Arrow x1={210} y1={1130} x2={880} y2={1130} color={C.cream} w={5} p={sp(f, b1 + 14, b1 + 50)} />
          <Lab x={540} y={1100} size={40} color={C.amber} o={sp(f, b1 + 30, b1 + 54)}>hơn 8,6 km</Lab>
          <Lab x={200} y={1070} size={30} color={D}>Suresnes</Lab>
          <Lab x={880} y={1070} size={30} color={D}>Montmartre</Lab>
        </g>
      </g>
      <g opacity={cB}>
        <circle cx={90} cy={870} r={26} fill={LAMP} stroke={C.cream} strokeWidth={4} />
        <circle cx={90} cy={930} r={16} fill={C.bg2} stroke={C.cream} strokeWidth={4} />
        <line x1={90} y1={870} x2={300} y2={870} stroke={LAMP} strokeWidth={3} opacity={0.35} />
        <Wheel x={300} y={890} r={110} angle={ang} />
        <rect x={880} y={820} width={26} height={140} rx={6} fill="#9fb4bb" stroke={C.cream} strokeWidth={4} />
        <line x1={300} y1={870} x2={880} y2={870} stroke={C.cream} strokeWidth={2} strokeDasharray="4 12" opacity={0.4} />
        <line x1={300} y1={900} x2={880} y2={900} stroke={C.cream} strokeWidth={2} strokeDasharray="4 12" opacity={0.4} />
        {showLight && <circle cx={stopAt} cy={lightY} r={13} fill={LAMP} />}
        <Lab x={880} y={1000} size={30} color={D}>gương ở xa</Lab>
        <Lab x={540} y={1130} size={38} color={C.cream} o={win(b2 + 30, b3)}>ánh sáng chui qua khe, tới gương, dội về</Lab>
        <Lab x={540} y={620} size={44} color={C.cream} o={win(b3, b4)}>bánh xe quay nhanh dần</Lab>
        <g opacity={sp(f, b3 + 40, b3 + 60) * (1 - sp(f, b4 - 6, b4 + 8))}>
          <g transform="translate(330 900)" stroke={C.amberDeep} strokeWidth={10} strokeLinecap="round">
            <line x1={-30} y1={-30} x2={30} y2={30} />
            <line x1={30} y1={-30} x2={-30} y2={30} />
          </g>
          <Lab x={540} y={720} size={42} color={C.amber}>răng chắn lại: mắt không thấy gì</Lab>
        </g>
        <Lab x={540} y={620} size={44} color={C.cream} o={win(b4, b5)}>quay nhanh gấp đôi: lọt qua khe kế bên</Lab>
        <g opacity={win(b4 + 40, b5)}>
          <Big x={540} y={470} size={80} color={C.amber}>25 vòng/giây</Big>
          <Lab x={540} y={1140} size={38} color={C.cream}>mỗi khe chuyển khe mất 55 phần triệu giây</Lab>
        </g>
        <g opacity={win(b5, b6)}>
          <Arrow x1={300} y1={1060} x2={880} y2={1060} color={C.amber} w={6} />
          <Arrow x1={880} y1={1100} x2={300} y2={1100} color={C.amber} w={6} />
          <Big x={590} y={700} size={90} color={C.amber}>hơn 17 km</Big>
          <Lab x={590} y={1190} size={40} color={C.cream}>cả đi lẫn về, trong 55 phần triệu giây</Lab>
        </g>
      </g>
      <g opacity={cC}>
        <Frac x={540} y={540} top="17 km" bottom="55 phần triệu giây" size={66} />
        <Big x={540} y={860} size={100} color={C.amber} o={sp(f, b6 + 40, b6 + 70)}>≈ 313 nghìn km/giây</Big>
        <rect x={110} y={1000} width={860 * sp(f, b6 + 80, b6 + 120)} height={40} rx={8} fill={C.amber} />
        <rect x={110} y={1060} width={860 * (299.8 / 313.3) * sp(f, b6 + 90, b6 + 130)} height={40} rx={8} fill={C.cream} />
        <Lab x={110} y={990} size={28} color={D} anchor="start" o={sp(f, b6 + 90, b6 + 110)}>Fizeau</Lab>
        <Lab x={110} y={1130} size={28} color={D} anchor="start" o={sp(f, b6 + 100, b6 + 120)}>số đúng ngày nay</Lab>
        <Big x={540} y={1260} size={90} color={C.amber} o={sp(f, b6 + 120, b6 + 150)}>chỉ lệch 4,5%</Big>
      </g>
    </Svg>
  );
};

// ============ 7. Kết ============
export const Outro: React.FC<Sc> = ({bs}) => {
  const f = useCurrentFrame();
  const [, b1, b2, e] = bs;
  const win = (a: number, z: number) => sp(f, a + 4, a + 20) * (1 - sp(f, z - 6, z + 8));
  const fade = 1 - sp(f, e, e + 18);
  const lg = sp(f, e + 6, e + 28);
  const lx = lerp(110, 970, seg(f, b1 + 30, b1 + 90));
  return (
    <Svg>
      <g opacity={fade}>
        <g opacity={sp(f, 0, 16) * (1 - sp(f, b1 - 6, b1 + 8))}>
          <Big x={540} y={620} size={118} color={C.amber}>299 792 458</Big>
          <Lab x={540} y={720} size={46} color={C.cream}>mét mỗi giây</Lab>
          <Lab x={540} y={800} size={40} color={D} o={sp(f, 40, 70)}>chính xác</Lab>
        </g>
        <g opacity={win(b1, b2)}>
          <line x1={110} y1={850} x2={970} y2={850} stroke={C.cream} strokeWidth={14} strokeLinecap="round" />
          <line x1={110} y1={820} x2={110} y2={880} stroke={C.amber} strokeWidth={8} />
          <line x1={970} y1={820} x2={970} y2={880} stroke={C.amber} strokeWidth={8} />
          <Lab x={540} y={790} size={44} color={C.amber}>1 mét</Lab>
          <circle cx={lx} cy={850} r={16} fill={LAMP} />
          <Lab x={540} y={1010} size={42} color={C.cream}>ánh sáng đi hết trong</Lab>
          <Big x={540} y={1100} size={80} color={C.amber}>1/299 792 458 giây</Big>
          <Lab x={540} y={460} size={44} color={D}>từ năm 1983</Lab>
        </g>
        <g opacity={win(b2, e)}>
          <Lantern x={210} y={800} on={1} s={2.2} />
          <Planet x={540} y={760} r={70} color={JUP} bands />
          <circle cx={540 + 110 * Math.cos(f * 0.1)} cy={760 + 110 * Math.sin(f * 0.1)} r={14} fill={C.cream} />
          <Wheel x={870} y={780} r={70} angle={f * 3} />
          <Lab x={210} y={950} size={34} color={C.cream}>đèn lồng</Lab>
          <Lab x={540} y={950} size={34} color={C.cream}>Io</Lab>
          <Lab x={870} y={950} size={34} color={C.cream}>bánh xe</Lab>
          <Hero x={540} y={1200} s={1.8} cheer={sp(f, b2 + 40, b2 + 60)} walk={f * 0.3} stick={false} />
        </g>
      </g>
      <g opacity={lg} transform={`translate(0 ${(1 - lg) * 20})`}>
        <g transform="translate(465 770) scale(3.4)">
          <MagMark size={44} raw />
        </g>
        <text x={540} y={1000} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={74} fill={C.cream}>
          Người <tspan fill={C.amber}>Giải Mã</tspan>
        </text>
        <Lab x={540} y={1080} size={40} color={C.cream}>Đo ánh sáng bằng đèn lồng, mặt trăng và bánh xe.</Lab>
      </g>
    </Svg>
  );
};
