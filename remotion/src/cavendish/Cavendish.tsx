import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {C} from '../lib/theme';
import {Fonts} from '../lib/Fonts';
import {SceneFade} from '../thales/Thales';
import {LAB, SceneId, timeline} from './content';
import {Calc, Check, Device, Hook, Idea, Mount, Outro, Sc} from './scenes';
import {VBackground, VCaptions, VHud} from '../eratosthenes/v';
import CAPS from './caps.json';

const SCENES: Record<SceneId, React.FC<Sc>> = {
  hook: Hook,
  mount: Mount,
  idea: Idea,
  device: Device,
  calc: Calc,
  check: Check,
  outro: Outro,
};

export const Cavendish: React.FC = () => {
  const tl = timeline();
  return (
    <AbsoluteFill style={{background: C.bg2}}>
      <Fonts />
      <VBackground />
      {tl.scenes.map((s) => {
        const Scene = SCENES[s.id];
        return (
          <Sequence key={s.id} from={s.start} durationInFrames={s.dur}>
            <SceneFade dur={s.dur}>
              <Scene dur={s.dur} bs={s.bs} t={LAB} />
            </SceneFade>
          </Sequence>
        );
      })}
      <VHud />
      <VCaptions beats={tl.beats} caps={CAPS as {text: string; start: number; end: number}[][]} />
    </AbsoluteFill>
  );
};
