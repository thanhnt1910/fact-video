import {makeVideo} from '../khoahoc/kit';
import {CmBackground} from './Bg';
import {timeline} from './content';
import {PANELS} from './scenes';
import CAPS from './caps.json';

export const Canmattroi = makeVideo(CmBackground, '#14152e', timeline(), PANELS, CAPS);
