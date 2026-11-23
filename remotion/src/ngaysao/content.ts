import {buildTimeline} from '../khoahoc/tl';
import texts from './texts.json';
import ledaDur from './leda_dur.json';

// Video khoa học số 30 (dọc 1080x1920, tiếng Việt): Trái Đất quay một vòng bao lâu (ngày sao và ngày Mặt Trời). Kịch bản: ke-hoach/khoa-hoc-video-30-ngay-sao-kich-ban.md
// texts.json là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-ngaysao.json.
export const SIZES = [3, 8, 6, 9, 6];
export const timeline = () => buildTimeline(texts as string[], SIZES, ledaDur as number[]);
