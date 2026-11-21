import {makeVideo} from '../khoahoc/kit';
import {CtBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Chantroi = makeVideo(CtBackground, '#1a1d28', timeline(), PANELS, CAPS);
