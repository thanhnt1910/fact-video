import {makeVideo} from '../khoahoc/kit';
import {PtBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Phantu = makeVideo(PtBackground, '#0f252d', timeline(), PANELS, CAPS);
