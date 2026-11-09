import React from 'react';
import {
  AbsoluteFill,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from 'remotion';

// Demo "bản đồ động": quân di chuyển theo đường hành quân, zoom theo cốt truyện, phụ đề từng câu.
// Toàn bộ chuyển động do code tính theo số frame (30 fps), không dùng AI sinh video.

const FPS = 30;
const W = 1080;
const H = 1920;

const fontCss = `
@font-face{font-family:'BeVN';font-weight:800;src:url(${staticFile('be-vietnam-pro-vietnamese-800-normal.woff2')}) format('woff2');unicode-range:U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB;}
@font-face{font-family:'BeVN';font-weight:800;src:url(${staticFile('be-vietnam-pro-latin-ext-800-normal.woff2')}) format('woff2');unicode-range:U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF;}
@font-face{font-family:'BeVN';font-weight:800;src:url(${staticFile('be-vietnam-pro-latin-800-normal.woff2')}) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;}
`;

// Các mốc trên "bản đồ" (toạ độ trong khung bản đồ 2000x2400, tâm khung nhìn sẽ zoom tới đây)
const POINTS = {
  thanhA: {x: 520, y: 1650, name: 'Thành A'},
  song: {x: 1000, y: 1250, name: 'Sông Lớn'},
  thanhB: {x: 1500, y: 700, name: 'Thành B'},
};

const MAP_W = 2000;
const MAP_H = 2400;

// Đường đi của quân: đường cong Bézier bậc 2 qua sông
const pathAt = (t: number) => {
  const p0 = POINTS.thanhA;
  const p2 = POINTS.thanhB;
  const c = {x: 1050, y: 1500};
  const u = 1 - t;
  return {
    x: u * u * p0.x + 2 * u * t * c.x + t * t * p2.x,
    y: u * u * p0.y + 2 * u * t * c.y + t * t * p2.y,
  };
};

const PATH_D = (() => {
  const p0 = POINTS.thanhA;
  const p2 = POINTS.thanhB;
  return `M ${p0.x} ${p0.y} Q 1050 1500 ${p2.x} ${p2.y}`;
})();

// Phụ đề: [bắt đầu giây, kết thúc giây, nội dung]
const CAPTIONS: Array<[number, number, string]> = [
  [0.6, 3.2, 'Đây là demo bản đồ động dựng bằng Remotion.'],
  [3.4, 6.4, 'Quân xuất phát từ Thành A, hướng về phía sông.'],
  [6.6, 9.2, 'Qua sông, camera zoom theo cốt truyện.'],
  [9.4, 12.2, 'Mọi chuyển động đều do code tính từng khung hình.'],
];

export const DEMO_DURATION = 13 * FPS;

const Terrain: React.FC = () => {
  // Nền giấy cổ + sông + núi + lưới nhẹ, vẽ bằng SVG
  return (
    <svg width={MAP_W} height={MAP_H} viewBox={`0 0 ${MAP_W} ${MAP_H}`}>
      <defs>
        <radialGradient id="paper" cx="50%" cy="45%" r="75%">
          <stop offset="0%" stopColor="#efdfb6" />
          <stop offset="100%" stopColor="#c9a96a" />
        </radialGradient>
        <filter id="rough">
          <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="3" seed="4" />
          <feDisplacementMap in="SourceGraphic" scale="14" />
        </filter>
      </defs>
      <rect width={MAP_W} height={MAP_H} fill="url(#paper)" />
      {/* lưới */}
      {Array.from({length: 20}).map((_, i) => (
        <line key={'v' + i} x1={i * 100} y1={0} x2={i * 100} y2={MAP_H} stroke="#8a6d3b" strokeOpacity={0.12} strokeWidth={2} />
      ))}
      {Array.from({length: 24}).map((_, i) => (
        <line key={'h' + i} x1={0} y1={i * 100} x2={MAP_W} y2={i * 100} stroke="#8a6d3b" strokeOpacity={0.12} strokeWidth={2} />
      ))}
      {/* sông */}
      <g filter="url(#rough)">
        <path
          d="M 200 1900 C 600 1500, 900 1450, 1100 1250 S 1500 1000, 1900 900"
          fill="none"
          stroke="#6fa3c7"
          strokeWidth={120}
          strokeLinecap="round"
          opacity={0.9}
        />
        <path
          d="M 200 1900 C 600 1500, 900 1450, 1100 1250 S 1500 1000, 1900 900"
          fill="none"
          stroke="#9cc7e0"
          strokeWidth={50}
          strokeLinecap="round"
          opacity={0.8}
        />
      </g>
      {/* núi */}
      {[
        [250, 600, 1],
        [420, 520, 1.3],
        [620, 640, 0.9],
        [1700, 1700, 1.2],
        [1450, 1900, 1],
        [1800, 2050, 1.4],
        [300, 1100, 1],
      ].map(([x, y, s], i) => (
        <g key={i} transform={`translate(${x} ${y}) scale(${s})`}>
          <polygon points="-90,60 0,-80 90,60" fill="#7a6a4a" />
          <polygon points="-30,60 0,-80 30,60" fill="#5d4f35" opacity={0.7} />
          <polygon points="-18,-48 0,-80 18,-48 0,-40" fill="#f4efe2" />
        </g>
      ))}
      {/* viền */}
      <rect x={20} y={20} width={MAP_W - 40} height={MAP_H - 40} fill="none" stroke="#5d4426" strokeWidth={10} />
    </svg>
  );
};

const City: React.FC<{x: number; y: number; name: string; color: string; appearAt: number}> = ({x, y, name, color, appearAt}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - appearAt, fps, config: {damping: 11, stiffness: 120}});
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <rect x={-70} y={-40} width={140} height={90} fill={color} stroke="#2b1d0e" strokeWidth={8} />
      {[-50, -17, 16, 49].map((dx) => (
        <rect key={dx} x={dx - 8} y={-62} width={22} height={26} fill={color} stroke="#2b1d0e" strokeWidth={6} />
      ))}
      <rect x={-18} y={5} width={36} height={45} fill="#2b1d0e" />
      <text x={0} y={120} textAnchor="middle" fontFamily="BeVN" fontWeight={800} fontSize={58} fill="#2b1d0e" stroke="#f3e6c2" strokeWidth={10} paintOrder="stroke">
        {name}
      </text>
    </g>
  );
};

const Soldier: React.FC<{dx: number; dy: number; phase: number; color: string}> = ({dx, dy, phase, color}) => {
  const frame = useCurrentFrame();
  const bob = Math.sin((frame + phase) / 3.2) * 7; // nhấp nhô khi bước đi
  return (
    <g transform={`translate(${dx} ${dy + bob})`}>
      <ellipse cx={0} cy={34} rx={20} ry={7} fill="#000" opacity={0.25} />
      <rect x={-12} y={-6} width={24} height={36} rx={6} fill={color} stroke="#2b1d0e" strokeWidth={4} />
      <circle cx={0} cy={-20} r={14} fill="#f1c99b" stroke="#2b1d0e" strokeWidth={4} />
      <line x1={20} y1={-40} x2={20} y2={30} stroke="#2b1d0e" strokeWidth={5} />
      <polygon points="20,-40 46,-30 20,-20" fill={color} stroke="#2b1d0e" strokeWidth={3} />
    </g>
  );
};

export const DemoBanDo: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;

  // Tiến độ quân: đứng yên 0-3.4s, đi 3.4s -> 9.4s (có làm mượt đầu/cuối), dừng
  const march = interpolate(t, [3.4, 9.4], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.cubic),
  });
  const army = pathAt(march);

  // Camera: bắt đầu nhìn toàn cảnh, zoom vào Thành A, đi theo quân, rồi zoom ra Thành B
  const zoom = interpolate(
    t,
    [0, 2.6, 3.4, 9.4, 10.6, 12.8],
    [0.8, 0.8, 1.25, 1.25, 1.6, 0.8],
    {extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)},
  );

  const camTarget = (() => {
    if (t < 3.4) {
      // toàn cảnh rồi lướt về Thành A
      const k = interpolate(t, [2.2, 3.4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
      return {
        x: interpolate(k, [0, 1], [MAP_W / 2, POINTS.thanhA.x]),
        y: interpolate(k, [0, 1], [MAP_H / 2, POINTS.thanhA.y]),
      };
    }
    if (t < 9.4) return army; // camera đi theo quân
    const k = interpolate(t, [9.4, 12.8], [0, 1], {extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
    return {
      x: interpolate(k, [0, 1], [army.x, MAP_W / 2]),
      y: interpolate(k, [0, 1], [army.y, MAP_H / 2 - 150]),
    };
  })();

  const tx = W / 2 - camTarget.x * zoom;
  const ty = H / 2 - camTarget.y * zoom;

  // Vết đường đi dần hiện ra
  const pathLen = 1800;
  const dash = interpolate(march, [0, 1], [pathLen, 0]);

  // Hướng quân (góc) theo tiếp tuyến
  const a = pathAt(Math.max(0, march - 0.01));
  const b = pathAt(Math.min(1, march + 0.01));
  const flip = b.x < a.x ? -1 : 1;

  const caption = CAPTIONS.find(([s, e]) => t >= s && t < e);
  const capIn = caption ? spring({frame: frame - Math.round(caption[0] * fps), fps, config: {damping: 14, stiffness: 140}}) : 0;

  const logoOpacity = interpolate(frame, [0, 20], [0, 0.95], {extrapolateRight: 'clamp'});
  const endFade = interpolate(frame, [DEMO_DURATION - 15, DEMO_DURATION], [0, 1], {extrapolateLeft: 'clamp'});

  return (
    <AbsoluteFill style={{background: '#2b1d0e', fontFamily: 'BeVN'}}>
      <style>{fontCss}</style>

      {/* Bản đồ + mọi vật thể trên bản đồ cùng chịu một phép biến đổi camera */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: 0,
          width: MAP_W,
          height: MAP_H,
          transformOrigin: '0 0',
          transform: `translate(${tx}px, ${ty}px) scale(${zoom})`,
        }}
      >
        <Terrain />
        <svg width={MAP_W} height={MAP_H} viewBox={`0 0 ${MAP_W} ${MAP_H}`} style={{position: 'absolute', left: 0, top: 0}}>
          <path d={PATH_D} fill="none" stroke="#b3261e" strokeWidth={10} strokeDasharray="30 22" opacity={0.35} />
          <path d={PATH_D} fill="none" stroke="#b3261e" strokeWidth={14} strokeLinecap="round" strokeDasharray={`${pathLen} ${pathLen}`} strokeDashoffset={dash} opacity={0.85} pathLength={pathLen} />
          <City {...POINTS.thanhA} color="#5a7fbf" appearAt={5} />
          <City {...POINTS.thanhB} color="#bf5a5a" appearAt={12} />
          <text x={POINTS.song.x + 120} y={POINTS.song.y - 90} fontFamily="BeVN" fontWeight={800} fontSize={54} fill="#1f4e6e" stroke="#f3e6c2" strokeWidth={9} paintOrder="stroke" transform={`rotate(-28 ${POINTS.song.x + 120} ${POINTS.song.y - 90})`}>
            {POINTS.song.name}
          </text>
          {/* Đội quân */}
          <g transform={`translate(${army.x} ${army.y}) scale(${flip} 1)`}>
            {[
              [-60, -40, 0],
              [0, -55, 4],
              [60, -40, 8],
              [-90, 20, 12],
              [-30, 10, 16],
              [30, 10, 20],
              [90, 20, 24],
            ].map(([dx, dy, ph], i) => (
              <Soldier key={i} dx={dx} dy={dy} phase={ph} color="#2f5aa8" />
            ))}
          </g>
        </svg>
      </div>

      {/* Logo kênh */}
      <Img src={staticFile('logo.png')} style={{position: 'absolute', top: 60, left: 60, width: 150, height: 150, borderRadius: 24, opacity: logoOpacity, objectFit: 'cover'}} />

      {/* Phụ đề */}
      <Sequence from={0}>
        {caption ? (
          <div
            style={{
              position: 'absolute',
              left: 60,
              right: 60,
              bottom: 260,
              textAlign: 'center',
              fontSize: 64,
              lineHeight: 1.25,
              color: '#fff',
              WebkitTextStroke: '10px #1a1208',
              paintOrder: 'stroke fill',
              transform: `translateY(${(1 - capIn) * 50}px) scale(${0.92 + 0.08 * capIn})`,
              opacity: capIn,
            }}
          >
            {caption[2]}
          </div>
        ) : null}
      </Sequence>

      <AbsoluteFill style={{background: '#000', opacity: endFade}} />
    </AbsoluteFill>
  );
};
