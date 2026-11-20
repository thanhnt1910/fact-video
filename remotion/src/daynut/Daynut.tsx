import {makeVideo} from '../khoahoc/kit';
import {DnBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Daynut = makeVideo(DnBackground, '#1c1c20', timeline(), PANELS, CAPS);
