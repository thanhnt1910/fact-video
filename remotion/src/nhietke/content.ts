import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 11 (dọc 1080x1920, tiếng Việt): Nhiệt kế, độ C và độ F. Kịch bản: ke-hoach/khoa-hoc-video-11-nhiet-ke-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-nhietke.json.
export const SIZES = [4, 4, 4, 5, 6, 4, 2];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
