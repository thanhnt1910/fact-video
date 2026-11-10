import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {C} from '../lib/theme';
import {Fonts} from '../lib/Fonts';
import {SceneFade} from '../thales/Thales';
import {SceneId, timeline} from './content';
import {Clockk, Err, Globe, Harr, Hook, Now, Sc, Wreck} from './scenes';
import {VBackground, VCaptions, VHud} from '../eratosthenes/v';
import CAPS from './caps.json';
import {useCurrentFrame} from 'remotion';

const STARS = Array.from({length: 46}, (_, i) => ({
  x: (i * 389) % 1040 + 20,
  y: (i * 617) % 1250 + 150,
  r: 1.5 + ((i * 7) % 4) * 0.7,
  ph: i * 0.9,
}));

const Stars: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', left: 0, top: 0}}>
      {STARS.map((s, i) => (
        <circle key={i} cx={s.x} cy={s.y - (f * 0.05) % 20} r={s.r} fill={C.cream} opacity={0.18 + 0.22 * Math.abs(Math.sin(f * 0.04 + s.ph))} />
      ))}
    </svg>
  );
};

const BASE: Record<string, number> = {};
const Push: React.FC<{dur: number; base?: number; children: React.ReactNode}> = ({dur, base = 1, children}) => {
  const f = useCurrentFrame();
  const k = base + 0.02 * Math.min(1, f / Math.max(1, dur));
  return <div style={{position: 'absolute', inset: 0, transform: `scale(${k})`, transformOrigin: '50% 48%'}}>{children}</div>;
};

const SCENES: Record<SceneId, React.FC<Sc>> = {
  hook: Hook,
  globe: Globe,
  wreck: Wreck,
  clock: Clockk,
  harrison: Harr,
  error: Err,
  now: Now,
};

export const Kinhdo: React.FC = () => {
  const tl = timeline();
  return (
    <AbsoluteFill style={{background: C.bg2}}>
      <Fonts />
      <VBackground />
      <Stars />
      {tl.scenes.map((s) => {
        const Scene = SCENES[s.id];
        return (
          <Sequence key={s.id} from={s.start} durationInFrames={s.dur}>
            <SceneFade dur={s.dur}>
              <Push dur={s.dur} base={BASE[s.id] ?? 1}>
                <Scene dur={s.dur} bs={s.bs} />
              </Push>
            </SceneFade>
          </Sequence>
        );
      })}
      <VHud />
      <VCaptions beats={tl.beats} caps={CAPS as {text: string; start: number; end: number}[][]} />
    </AbsoluteFill>
  );
};
