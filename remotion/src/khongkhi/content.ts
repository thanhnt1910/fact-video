import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 16 (dọc 1080x1920, tiếng Việt): Không khí nặng bao nhiêu. Kịch bản: ke-hoach/khoa-hoc-video-16-khong-khi-nang-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-khongkhi.json.
export const SIZES = [4, 5, 4, 7, 3, 4, 3];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
