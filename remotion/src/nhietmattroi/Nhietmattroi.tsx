import {makeVideo} from '../khoahoc/kit';
import {NmBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Nhietmattroi = makeVideo(NmBackground, '#14131c', timeline(), PANELS, CAPS);
