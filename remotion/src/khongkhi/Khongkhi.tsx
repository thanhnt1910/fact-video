import {makeVideo} from '../khoahoc/kit';
import {KkBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Khongkhi = makeVideo(KkBackground, '#1b2430', timeline(), PANELS, CAPS);
