import {makeVideo} from '../khoahoc/kit';
import {SpBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Sopi = makeVideo(SpBackground, '#18222f', timeline(), PANELS, CAPS);
