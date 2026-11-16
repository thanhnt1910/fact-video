import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 21 (dọc 1080x1920, tiếng Việt): Con lắc Phu-cô, Trái Đất quay. Kịch bản: ke-hoach/khoa-hoc-video-21-con-lac-phu-co-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-conlac.json.
export const SIZES = [4, 4, 5, 3, 7, 4];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
