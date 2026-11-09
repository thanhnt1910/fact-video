import React from 'react';
import {Composition} from 'remotion';
import {DemoBanDo, DEMO_DURATION} from './DemoBanDo';

export const Root: React.FC = () => {
  return (
    <Composition
      id="DemoBanDo"
      component={DemoBanDo}
      durationInFrames={DEMO_DURATION}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
