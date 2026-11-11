import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 9 (dọc 1080x1920, tiếng Việt): Sấm chớp và tốc độ âm thanh. Kịch bản: ke-hoach/khoa-hoc-video-9-toc-do-am-thanh-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-amthanh.json.
export const SIZES = [4, 4, 3, 5, 5, 2];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
