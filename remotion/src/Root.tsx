import React from 'react';
import {Composition} from 'remotion';
import {DemoBanDo, DEMO_DURATION} from './DemoBanDo';
import {Thales} from './thales/Thales';
import {timeline} from './thales/content';
import {FPS, H, W} from './lib/theme';

export const Root: React.FC = () => {
  return (
    <>
      <Composition id="DemoBanDo" component={DemoBanDo} durationInFrames={DEMO_DURATION} fps={30} width={1080} height={1920} />
      <Composition id="ThalesEN" component={Thales} durationInFrames={timeline('en').total} fps={FPS} width={W} height={H} defaultProps={{lang: 'en' as const}} />
      <Composition id="ThalesVI" component={Thales} durationInFrames={timeline('vi').total} fps={FPS} width={W} height={H} defaultProps={{lang: 'vi' as const}} />
    </>
  );
};
