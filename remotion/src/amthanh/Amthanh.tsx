import {makeVideo} from '../khoahoc/kit';
import {AmBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Amthanh = makeVideo(AmBackground, '#222c3c', timeline(), PANELS, CAPS);
