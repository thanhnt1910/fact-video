import {makeVideo} from '../khoahoc/kit';
import {MtBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Mattroi = makeVideo(MtBackground, '#3a2f63', timeline(), PANELS, CAPS);
