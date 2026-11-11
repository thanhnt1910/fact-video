import {makeVideo} from '../khoahoc/kit';
import {NkBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Nhietke = makeVideo(NkBackground, '#1f3a3a', timeline(), PANELS, CAPS);
