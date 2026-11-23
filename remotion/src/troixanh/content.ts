import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 29 (dọc 1080x1920, tiếng Việt): Vì sao bầu trời xanh, hoàng hôn đỏ. Kịch bản: ke-hoach/khoa-hoc-video-29-troi-xanh-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-troixanh.json.
export const SIZES = [3, 6, 5, 5, 3, 4, 2];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
