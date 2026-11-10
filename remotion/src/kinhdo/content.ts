import {FPS} from '../lib/theme';
import {beatSeconds} from '../thales/content';
import ledaDur from './leda_dur.json';

// Video khoa học số 4 (dọc 1080x1920, tiếng Việt): Làm sao biết tàu ở đâu giữa biển? Kịch bản: ke-hoach/khoa-hoc-video-4-kinh-do-kich-ban.md
// Văn bản ở đây là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-kinhdo.json.

export type SceneId = 'hook' | 'globe' | 'wreck' | 'clock' | 'harrison' | 'error' | 'now';
export const END_C = 3.5;

export const TEXT_C: Record<SceneId, string[]> = {
  hook: [
    "Năm 1714, nước Anh treo thưởng 20 000 bảng cho câu hỏi: tàu của tôi đang ở đâu giữa biển?",
    "Người tìm ra lời giải không phải nhà thiên văn, mà là một người thợ mộc.",
    "Lời giải của ông là một chiếc đồng hồ. Vì sao đồng hồ lại cho biết tàu đang ở đâu?",
  ],
  globe: [
    "Cần hai con số. Vĩ độ, bắc hay nam, đo dễ: đo góc Mặt Trời lúc giữa trưa.",
    "Kinh độ, đông hay tây, cần giờ ở cảng nhà. Trái Đất quay: 360° ÷ 24 giờ = 15° mỗi giờ.",
    "Giữa trưa trên tàu, đồng hồ nhà chỉ 3 giờ chiều. 3 giờ × 15° = 45°: tàu ở phía tây cảng nhà.",
    "Ở xích đạo, 1 phút sai = 1/4 độ ≈ 28 km.",
  ],
  wreck: [
    "Thiếu cách biết vị trí chắc chắn, tàu rất dễ lạc. Bảy năm trước đó, hạm đội Anh chạy về nước và lạc đường.",
    "Đêm 22 tháng 10 năm 1707, đô đốc Cloudesley Shovell tin tàu còn ở phía nam quần đảo Scilly. Họ chỉ ước chừng vị trí.",
    "Đội tàu lệch xa về phía bắc, đâm vào đá. Bốn chiến hạm vỡ tan, hơn 1 400 người chết.",
  ],
  clock: [
    "Cần đồng hồ chạy đúng nhiều tuần giữa biển. Nhưng sóng lắc làm quả lắc chạy loạn.",
    "Mức cao nhất: tàu lạc không quá nửa độ, tức đồng hồ sai không quá 2 phút.",
    "John Harrison, sinh năm 1693, là thợ mộc, làm đồng hồ lúc rảnh.",
  ],
  harrison: [
    "Ba chiếc đầu là cỗ máy lớn. Chiếc thứ tư chỉ như đồng hồ bỏ túi.",
    "Tháng 11 năm 1761, nó lên tàu từ Portsmouth đi Jamaica, con trai ông trông giữ.",
    "Sau 81 ngày, tàu cập bến. Đồng hồ chỉ chậm 5 giây.",
  ],
  error: [
    "5 giây = 1/12 phút. 28 ÷ 12 ≈ 2,3 km.",
    "Mức cho phép: 55 km. Sai số thật: 2,3 km, nhỏ hơn hơn 20 lần.",
    "Vậy mà hội đồng đòi thử thêm. Mãi đến 1773, sau khi ông xin nhà vua, mới trả khoản cuối.",
  ],
  now: [
    "Ý tưởng ấy sống trong điện thoại. Vệ tinh GPS mang đồng hồ nguyên tử, điện thoại tính tín hiệu bay mất bao lâu.",
    "Sai 1 phần tỉ giây thì vị trí lệch 30 cm.",
    "Mang theo giờ của nhà, bạn biết mình đang ở đâu.",
  ],
};

export type Beat = {text: string; start: number; dur: number};
export type SceneTl = {id: SceneId; start: number; dur: number; beats: Beat[]; bs: number[]};
const ORDER: SceneId[] = ['hook', 'globe', 'wreck', 'clock', 'harrison', 'error', 'now'];

export function timeline(): {scenes: SceneTl[]; total: number; beats: Beat[]} {
  let f = 0;
  let voiceIdx = 0;
  const all: Beat[] = [];
  const scenes: SceneTl[] = ORDER.map((id) => {
    const texts = id === 'now' ? [...TEXT_C[id], ''] : TEXT_C[id];
    const beats: Beat[] = texts.map((text) => {
      let sec = text ? beatSeconds('vi', text) : END_C;
      const d = (ledaDur as number[])[voiceIdx];
      if (text && d !== undefined) sec = Math.max(d + 0.5, 2.4);
      if (text) voiceIdx++;
      const dur = Math.round(sec * FPS);
      const b = {text, start: f, dur};
      f += dur;
      all.push(b);
      return b;
    });
    const start = beats[0].start;
    return {id, start, dur: f - start, beats, bs: beats.map((b) => b.start - start)};
  });
  return {scenes, total: f, beats: all};
}
