import {makeVideo} from '../khoahoc/kit';
import {MmBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Motmet = makeVideo(MmBackground, '#2b2419', timeline(), PANELS, CAPS);
