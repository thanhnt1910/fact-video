import React from 'react';
import {Arrow, Big, C, Calc, Head, HatHero, Panel, Tag, clamp01, lerp, sp} from '../khoahoc/kit';

const WATER = '#2f6f96';
const WOOD = '#b98a52';
const SANDC = '#e8c77a';
const RED = '#e0613b';
const AM = C.amber;
const CX = 540;

const Hero2: React.FC<{f: number; x?: number; cheer?: number}> = ({f, x = 170, cheer = 0}) => <HatHero x={x} y={1250} s={2} walk={f * 0.13} cheer={cheer} hat="pirate" />;

const Sea: React.FC<{f: number; y?: number; bottom?: number}> = ({f, y = 820, bottom = 1200}) => {
  let d = '';
  for (let x = 300; x <= 990; x += 10) d += `${x === 300 ? 'M' : 'L'} ${x} ${y + 8 * Math.sin(x * 0.02 - f * 0.1)} `;
  return (
    <g>
      <path d={`${d} L 990 ${bottom} L 300 ${bottom} Z`} fill={WATER} opacity={0.5} />
      <path d={d} fill="none" stroke={C.cream} strokeWidth={5} />
    </g>
  );
};
const Ship: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M -90 0 L 90 0 L 65 44 L -65 44 Z" fill="#c9533a" stroke={C.cream} strokeWidth={5} strokeLinejoin="round" />
    <line x1={0} y1={0} x2={0} y2={-130} stroke={C.cream} strokeWidth={6} />
    <path d="M 0 -125 L 70 -30 L 0 -30 Z" fill={C.cream} opacity={0.9} />
  </g>
);
const Chip: React.FC<{x: number; y: number}> = ({x, y}) => (
  <g transform={`translate(${x} ${y})`}>
    <path d="M -26 -6 L 26 -6 L 0 36 Z" fill={WOOD} stroke={C.cream} strokeWidth={4} strokeLinejoin="round" />
  </g>
);
// Sợi dây nằm ngang từ x1 tới x2 ở độ cao y, nút thắt cách đều gap, trượt theo off.
const Rope: React.FC<{x1: number; x2: number; y: number; gap?: number; off?: number; n?: number}> = ({x1, x2, y, gap = 90, off = 0, n}) => {
  const ks: number[] = [];
  for (let x = x1 + ((off % gap) + gap) % gap; x <= x2; x += gap) ks.push(x);
  return (
    <g>
      <line x1={x1} y1={y} x2={x2} y2={y} stroke="#d8c39a" strokeWidth={8} strokeLinecap="round" />
      {(n ? ks.slice(0, n) : ks).map((x, i) => (
        <circle key={i} cx={x} cy={y} r={13} fill="#d8c39a" stroke={C.cream} strokeWidth={3} />
      ))}
    </g>
  );
};
const Glass: React.FC<{x: number; y: number; s?: number; t?: number}> = ({x, y, s = 1, t = 0}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M -50 -80 L 50 -80 L 8 0 L 50 80 L -50 80 L -8 0 Z" fill="none" stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
    <path d={`M ${-44 + 36 * t} ${-74 + 60 * t} L ${44 - 36 * t} ${-74 + 60 * t} L 4 -4 Z`} fill={SANDC} opacity={1 - t * 0.9} />
    <path d={`M -44 74 L 44 74 L 0 ${74 - 70 * t} Z`} fill={SANDC} />
    <rect x={-60} y={-92} width={120} height={12} rx={5} fill={WOOD} />
    <rect x={-60} y={80} width={120} height={12} rx={5} fill={WOOD} />
  </g>
);

const P0: Panel = ({f}) => (
  <g>
    <Head a="Giữa biển không cột mốc" b="tàu chạy nhanh bao nhiêu?" />
    <Sea f={f} y={900} />
    <Ship x={300 + f * 1.2} y={880} />
    <Big x={CX + 340} y={620} size={150} color={AM} o={0.9 * sp(f, 14, 30)}>?</Big>
    <Hero2 f={f} />
  </g>
);
const P1: Panel = ({f}) => (
  <g>
    <Head a="Chỉ cần mảnh gỗ, dây" b="và đồng hồ cát" />
    <g opacity={sp(f, 2, 14)}><Chip x={330} y={800} /></g>
    <g opacity={sp(f, 12, 24)}><Rope x1={420} x2={640} y={800} gap={55} /></g>
    <g opacity={sp(f, 22, 34)}><Glass x={820} y={800} s={1.1} t={clamp01((f - 24) / 80)} /></g>
    <Hero2 f={f} />
  </g>
);
const P2: Panel = ({f}) => (
  <g>
    <Head a="Nhờ sợi dây ấy" b="tốc độ tàu tính bằng nút" />
    <Rope x1={180} x2={960} y={800} gap={110} off={f * 0.8} />
    <Big x={CX + 60} y={1010} size={150} color={AM} o={sp(f, 10, 26)}>nút</Big>
    <Hero2 f={f} />
  </g>
);
const P3: Panel = ({f}) => (
  <g>
    <Head a="Muốn biết tốc độ" />
    <Calc f={f} x={CX + 60} y={720} step={150} lines={[{t: 'quãng đường', at: 2, size: 100, color: AM}, {t: '÷ thời gian', at: 22, size: 100}]} />
    <Hero2 f={f} />
  </g>
);
const P4: Panel = ({f}) => (
  <g>
    <Head a="Trên biển không có" b="cột cây số" />
    <Sea f={f} y={900} />
    <Ship x={CX + 60} y={880} />
    {[0, 1, 2].map((i) => (
      <g key={i} opacity={sp(f, 4 + i * 6, 14 + i * 6) * 0.9}>
        <rect x={CX - 280 + i * 280} y={720} width={40} height={90} fill="#8a8a8a" stroke={C.cream} strokeWidth={3} />
      </g>
    ))}
    <line x1={CX - 320} y1={680} x2={CX + 320} y2={860} stroke={RED} strokeWidth={14} strokeLinecap="round" opacity={sp(f, 24, 38)} />
    <Hero2 f={f} />
  </g>
);
const P5: Panel = ({f}) => {
  const sx = 420 + 360 * clamp01(f / 120);
  return (
    <g>
      <Head a="Lấy nước làm mốc" b="mảnh gỗ gần như đứng yên" />
      <Sea f={f} y={860} />
      <Chip x={380} y={870} />
      <Ship x={sx} y={840} />
      <Arrow x1={sx - 120} y1={760} x2={sx + 40} y2={760} color={RED} p={sp(f, 10, 30)} w={8} />
      <Hero2 f={f} />
    </g>
  );
};
const P6: Panel = ({f}) => {
  const sx = 420 + 380 * clamp01(f / 100);
  return (
    <g>
      <Head a="Tàu đi, dây buộc mảnh gỗ" b="tuột dần khỏi cuộn" />
      <Sea f={f} y={860} />
      <Chip x={380} y={870} />
      <line x1={380} y1={850} x2={sx - 60} y2={840} stroke="#d8c39a" strokeWidth={6} />
      <Ship x={sx} y={840} />
      <Hero2 f={f} />
    </g>
  );
};
const P7: Panel = ({f}) => (
  <g>
    <Head a="Trên dây có nút thắt" b="cách đều nhau" />
    <Rope x1={200} x2={960} y={800} gap={100} n={Math.floor(sp(f, 4, 50) * 8)} />
    <g opacity={sp(f, 30, 46)}>
      <line x1={250} y1={880} x2={350} y2={880} stroke={AM} strokeWidth={6} />
      <Tag x={300} y={940} color={AM} size={40}>bằng nhau</Tag>
    </g>
    <Hero2 f={f} />
  </g>
);
const P8: Panel = ({f}) => (
  <g>
    <Head a="Mỗi nút qua tay" b="là tàu đi thêm một đoạn" />
    <Rope x1={180} x2={960} y={800} gap={100} off={-f * 2.2} />
    <circle cx={CX + 40} cy={800} r={60} fill="none" stroke={AM} strokeWidth={6} />
    <Tag x={CX + 40} y={920} color={AM} size={42} o={sp(f, 10, 26)}>tay thủy thủ</Tag>
    <Hero2 f={f} />
  </g>
);
const P9: Panel = ({f}) => {
  const t = clamp01(f / 120);
  return (
    <g>
      <Head a="Lật đồng hồ cát" b="đếm nút tuột ra" />
      <Glass x={330} y={820} s={1.3} t={t} />
      <Rope x1={500} x2={960} y={820} gap={80} off={-f * 2.2} />
      <Big x={CX + 270} y={980} size={110} color={AM} o={sp(f, 10, 26)}>{String(Math.min(8, Math.floor(t * 8)))}</Big>
      <Hero2 f={f} />
    </g>
  );
};
const P10: Panel = ({f}) => (
  <g>
    <Head a="Cách đo này đã có từ" />
    <Big x={CX + 60} y={800} size={180} color={AM} o={sp(f, 2, 18)}>thế kỷ 16</Big>
    <Hero2 f={f} />
  </g>
);
const P11: Panel = ({f}) => (
  <g>
    <Head a="Khoảng cách giữa hai nút" b="phải chọn sao cho" />
    <Big x={CX + 60} y={780} size={100} color={AM} o={sp(f, 2, 16)}>số nút = tốc độ</Big>
    <Rope x1={260} x2={960} y={940} gap={140} />
    <Tag x={CX + 60} y={1010} color={C.cream} size={44} o={sp(f, 16, 32)}>hai nút cách nhau bao xa?</Tag>
    <Hero2 f={f} />
  </g>
);
const P12: Panel = ({f}) => (
  <g>
    <Head a="Mốc để so" b="là một hải lý" />
    <Big x={CX + 60} y={760} size={120} color={AM} o={sp(f, 2, 16)}>1 nút</Big>
    <Big x={CX + 60} y={900} size={90} color={C.cream} o={sp(f, 14, 28)}>= 1 hải lý / giờ</Big>
    <Hero2 f={f} />
  </g>
);
const P13: Panel = ({f}) => (
  <g>
    <Head a="Một hải lý" b="dài bao nhiêu?" />
    <Big x={CX + 60} y={800} size={130} color={AM} o={sp(f, 2, 18)}>1.852 m</Big>
    <Hero2 f={f} />
  </g>
);
const Earth: React.FC<{f: number; arc?: number}> = ({f, arc = 0}) => (
  <g>
    <circle cx={CX + 100} cy={820} r={170} fill="#2f6f96" stroke={C.cream} strokeWidth={6} opacity={0.9} />
    <path d={`M ${CX + 100} ${820 - 170} A 170 170 0 0 1 ${CX + 100 + 170 * Math.sin(arc)} ${820 - 170 * Math.cos(arc)}`} fill="none" stroke={AM} strokeWidth={14} strokeLinecap="round" />
  </g>
);
const P14: Panel = ({f}) => (
  <g>
    <Head a="Một hải lý" b="ứng với một phút vĩ độ" />
    <Earth f={f} arc={0.18 * sp(f, 4, 30)} />
    <Tag x={CX + 340} y={640} color={AM} size={44} o={sp(f, 20, 36)}>1 phút</Tag>
    <Hero2 f={f} />
  </g>
);
const P15: Panel = ({f}) => (
  <g>
    <Head a="Vòng Trái Đất" b="có 21.600 phút như vậy" />
    <Earth f={f} arc={Math.PI * 2 * sp(f, 4, 60)} />
    <Big x={CX + 100} y={1080} size={100} color={AM} o={sp(f, 30, 46)}>21.600</Big>
    <Hero2 f={f} />
  </g>
);
const P16: Panel = ({f}) => (
  <g>
    <Head a="Chia vòng Trái Đất" b="cho số phút" />
    <Calc f={f} x={CX + 60} y={740} step={150} lines={[{t: '40.000 ÷ 21.600', at: 2, size: 96}, {t: '≈ 1,85 km', at: 26, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P17: Panel = ({f}) => (
  <g>
    <Head a="Cát chảy hết 28 giây" b="một giờ có 3.600 giây" />
    <Glass x={340} y={820} s={1.2} t={clamp01(f / 100)} />
    <Big x={CX + 280} y={780} size={90} color={AM} o={sp(f, 4, 18)}>28 s</Big>
    <Big x={CX + 280} y={920} size={90} color={C.cream} o={sp(f, 18, 32)}>3.600 s</Big>
    <Hero2 f={f} />
  </g>
);
const P18: Panel = ({f}) => (
  <g>
    <Head a="Tàu chạy một nút" b="mỗi giờ đi 1.852 mét" />
    <Calc f={f} x={CX + 60} y={760} step={150} lines={[{t: '1 nút', at: 2, size: 120}, {t: '= 1.852 m / giờ', at: 22, size: 90, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P19: Panel = ({f}) => (
  <g>
    <Head a="Chia cho 3.600 giây" />
    <Calc f={f} x={CX + 60} y={760} step={150} lines={[{t: '1.852 ÷ 3.600', at: 2, size: 100}, {t: '≈ 0,5 m/s', at: 24, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P20: Panel = ({f}) => (
  <g>
    <Head a="Nhân với 28 giây" />
    <Calc f={f} x={CX + 60} y={760} step={150} lines={[{t: '0,5 × 28', at: 2, size: 120}, {t: '≈ 14,4 m', at: 24, size: 150, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P21: Panel = ({f}) => (
  <g>
    <Head a="Hai nút liền nhau" b="cách nhau khoảng 14,4 mét" />
    <Rope x1={200} x2={960} y={800} gap={220} />
    <line x1={420} y1={880} x2={640} y2={880} stroke={AM} strokeWidth={6} opacity={sp(f, 6, 24)} />
    <Big x={530} y={960} size={86} color={AM} o={sp(f, 10, 28)}>14,4 m</Big>
    <Hero2 f={f} />
  </g>
);
const P22: Panel = ({f}) => {
  const t = clamp01(f / 100);
  return (
    <g>
      <Head a="Trong 28 giây" b="8 nút tuột ra" />
      <Glass x={330} y={820} s={1.2} t={t} />
      <Rope x1={500} x2={960} y={820} gap={80} off={-f * 2.2} />
      <Big x={CX + 270} y={980} size={110} color={AM} o={sp(f, 6, 22)}>{String(Math.min(8, Math.floor(t * 8)))}</Big>
      <Hero2 f={f} />
    </g>
  );
};
const P23: Panel = ({f}) => (
  <g>
    <Head a="Tàu chạy 8 nút" b="tức 8 hải lý mỗi giờ" />
    <Sea f={f} y={900} />
    <Ship x={300 + f * 2} y={880} />
    <Big x={CX + 60} y={650} size={110} color={AM} o={sp(f, 6, 22)}>8 hải lý/giờ</Big>
    <Hero2 f={f} />
  </g>
);
const P24: Panel = ({f}) => (
  <g>
    <Head a="Đổi ra ki-lô-mét" />
    <Calc f={f} x={CX + 60} y={760} step={150} lines={[{t: '8 × 1,852', at: 2, size: 120}, {t: '≈ 14,8 km/h', at: 24, size: 140, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P25: Panel = ({f}) => (
  <g>
    <Head a="Nửa giờ đo một lần" b="rồi ghi vào sổ" />
    <rect x={330} y={640} width={560} height={420} rx={14} fill="#e8d9b4" stroke={C.cream} strokeWidth={5} opacity={0.95} />
    {[0, 1, 2, 3, 4].map((i) => (
      <g key={i} opacity={sp(f, 6 + i * 8, 16 + i * 8)}>
        <line x1={370} y1={700 + i * 70} x2={560} y2={700 + i * 70} stroke="#6b5a3a" strokeWidth={5} />
        <text x={620} y={712 + i * 70} fontFamily="Cormorant" fontWeight={700} fontSize={50} fill="#6b5a3a">8 nút</text>
      </g>
    ))}
    <Hero2 f={f} />
  </g>
);
const P26: Panel = ({f}) => (
  <g>
    <Head a="Chạy 8 nút" b="suốt một ngày" />
    <Calc f={f} x={CX + 60} y={760} step={150} lines={[{t: '8 × 24', at: 2, size: 130}, {t: '= 192 hải lý', at: 24, size: 130, color: AM}]} />
    <Hero2 f={f} />
  </g>
);
const P27: Panel = ({f}) => (
  <g>
    <Head a="Khoảng 356 ki-lô-mét" b="biết mình đã đi bao xa" />
    <Big x={CX + 60} y={800} size={150} color={AM} o={sp(f, 2, 18)}>≈ 356 km</Big>
    <line x1={260} y1={1000} x2={260 + 700 * sp(f, 6, 60)} y2={1000} stroke={RED} strokeWidth={10} strokeLinecap="round" />
    <circle cx={260} cy={1000} r={14} fill={C.cream} />
    <Hero2 f={f} />
  </g>
);
const P28: Panel = ({f}) => (
  <g>
    <Head a="Không cột mốc" b="vẫn đo được tốc độ tàu" />
    <g opacity={sp(f, 2, 14)}><Chip x={300} y={800} /></g>
    <g opacity={sp(f, 10, 22)}><Rope x1={400} x2={640} y={800} gap={60} /></g>
    <g opacity={sp(f, 18, 30)}><Glass x={820} y={800} s={1.1} t={clamp01((f - 20) / 80)} /></g>
    <Hero2 f={f} />
  </g>
);
const P29: Panel = ({f}) => (
  <g>
    <Head a="Tên gọi" b="còn lại đến nay" />
    <Rope x1={180} x2={960} y={760} gap={110} off={f * 0.8} />
    <Big x={CX + 60} y={960} size={170} color={AM} o={sp(f, 6, 22)}>nút</Big>
    <Hero2 f={f} cheer={sp(f, 10, 28)} />
  </g>
);

export const PANELS: Panel[] = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29];
void lerp;
