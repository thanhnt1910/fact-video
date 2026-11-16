import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 22 (dọc 1080x1920, tiếng Việt): Cân Mặt Trời nhờ tốc độ Trái Đất. Kịch bản: ke-hoach/khoa-hoc-video-22-can-mat-troi-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-canmattroi.json.
export const SIZES = [4, 4, 6, 5, 6, 4];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
