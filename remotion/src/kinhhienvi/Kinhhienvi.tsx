import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame} from 'remotion';
import {Fonts} from '../lib/Fonts';
import {SceneFade} from '../thales/Thales';
import {SceneId, timeline} from './content';
import {Giot, Hook, Kinh, Lp, Nay, Nho, Sc} from './scenes';
import {VCaptions, VHud} from '../eratosthenes/v';
import {KhBackground} from './Bg';
import CAPS from './caps.json';

const Push: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
  const f = useCurrentFrame();
  const k = 1 + 0.02 * Math.min(1, f / Math.max(1, dur));
  return <div style={{position: 'absolute', inset: 0, transform: `scale(${k})`, transformOrigin: '50% 48%'}}>{children}</div>;
};

const SCENES: Record<SceneId, React.FC<Sc>> = {hook: Hook, kinh: Kinh, lp: Lp, nho: Nho, giot: Giot, nay: Nay};

export const Kinhhienvi: React.FC = () => {
  const tl = timeline();
  return (
    <AbsoluteFill style={{background: '#32241a'}}>
      <Fonts />
      <KhBackground />
      {tl.scenes.map((s) => {
        const Scene = SCENES[s.id];
        return (
          <Sequence key={s.id} from={s.start} durationInFrames={s.dur}>
            <SceneFade dur={s.dur}>
              <Push dur={s.dur}>
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
