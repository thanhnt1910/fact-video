import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 8 (dọc 1080x1920, tiếng Việt): Ngôi sao xa bao nhiêu? Kịch bản: ke-hoach/khoa-hoc-video-8-khoang-cach-sao-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-sao.json.
export const SIZES = [3, 3, 2, 3, 3, 6, 5];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
