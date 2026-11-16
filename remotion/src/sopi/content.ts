import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 18 (dọc 1080x1920, tiếng Việt): Số pi. Kịch bản: ke-hoach/khoa-hoc-video-18-so-pi-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-sopi.json.
export const SIZES = [4, 4, 7, 3, 5, 5, 3];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
