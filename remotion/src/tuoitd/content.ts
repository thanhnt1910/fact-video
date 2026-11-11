import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 14 (dọc 1080x1920, tiếng Việt): Trái Đất bao nhiêu tuổi. Kịch bản: ke-hoach/khoa-hoc-video-14-tuoi-trai-dat-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-tuoitd.json.
export const SIZES = [4, 3, 5, 5, 6, 5, 3];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
