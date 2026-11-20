import {makeVideo} from '../khoahoc/kit';
import {StBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Songthan = makeVideo(StBackground, '#102838', timeline(), PANELS, CAPS);
