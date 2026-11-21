import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 28 (dọc 1080x1920, tiếng Việt): Mặt Trời nóng bao nhiêu (định luật Wien). Kịch bản: ke-hoach/khoa-hoc-video-28-nhiet-mat-troi-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-nhietmattroi.json.
export const SIZES = [3, 5, 2, 6, 6, 9, 3];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
