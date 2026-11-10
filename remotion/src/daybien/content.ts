import {FPS} from '../lib/theme';
import {beatSeconds} from '../thales/content';
import ledaDur from './leda_dur.json';

// Video khoa học số 5 (dọc 1080x1920, tiếng Việt): Vì sao đáy biển khó đo? Kịch bản: ke-hoach/khoa-hoc-video-5-day-bien-kich-ban.md
// Văn bản ở đây là PHỤ ĐỀ (chữ số); bản đọc nằm trong ke-hoach/giong-video-khoa-hoc-daybien.json.

export type SceneId = 'hook' | 'cu' | 'chal' | 'vang' | 'meteor' | 'nay';
export const END_C = 3.5;

export const TEXT_C: Record<SceneId, string[]> = {
  hook: [
    "Thời vệ tinh, ta vẫn chưa vẽ xong bản đồ đáy biển: mới chưa đến 30%.",
    "Đo độ cao núi thì dễ, nhìn từ xa là được. Vậy vì sao đo độ sâu của biển lại khó đến thế?",
    "Vì ta không nhìn thấy đáy, và sợi dây không báo lúc nào chạm đáy.",
  ],
  cu: [
    "Cách cũ: buộc quả nặng vào dây, thả xuống, đọc dây đã chạy ra bao nhiêu mét khi chạm đáy.",
    "Chỗ nông thì được. Chỗ sâu, dây tự nó rất nặng, nên quả nặng chạm đáy mà tay khó nhận ra.",
    "Sâu khoảng 2 700 m, quả nặng phải chìm khoảng 20 phút mới tới đáy.",
  ],
  chal: [
    "Tàu Challenger của Anh cũng đo bằng dây. Từ 1872 đến 1876, tàu chỉ đo chưa đến 500 lần.",
    "Chưa đến 500 điểm giữa đại dương mênh mông: chỉ là vài chấm nhỏ trên bản đồ trắng.",
    "Ngày 23 tháng 3 năm 1875, tàu đo được chỗ sâu 8 184 m, và đo lại lần hai.",
  ],
  vang: [
    "Ý mới: đừng thả dây. Gửi một tiếng động xuống đáy, đo bao lâu sau tiếng vang quay lại.",
    "Như hét vào thung lũng: núi càng xa, tiếng vang về càng muộn. Đáy càng sâu, vang càng chậm.",
    "Trong nước, âm thanh đi khoảng 1 500 m mỗi giây. Tiếng động đi xuống rồi dội lên: quãng đường là hai lần độ sâu.",
    "Nên độ sâu = tốc độ × thời gian ÷ 2.",
    "Vang về sau 4 giây: 1 500 × 4 = 6 000, ÷ 2 = 3 000. Đáy sâu 3 000 m.",
    "Chỉ mất vài giây, và tàu vừa chạy vừa đo, không phải dừng thả dây nhiều phút.",
  ],
  meteor: [
    "Máy đo tiếng vang ra đời đầu thế kỷ 20. Từ 1925, tàu Meteor của Đức dùng nó khảo sát Nam Đại Tây Dương.",
    "Tàu này đo khoảng 67 000 lần, nhiều gấp hơn 100 lần cả chuyến Challenger.",
    "Từ số đo ấy, họ vẽ được 14 mặt cắt của đáy Đại Tây Dương.",
  ],
  nay: [
    "Nay, dự án Seabed 2030 muốn có bản đồ trọn vẹn, bằng cách gom số đo của 220 tổ chức.",
    "Tháng 4 năm 2026, dự án báo đã có 104 triệu km² đáy biển, tức 28,7%.",
    "Cả đáy biển: 104 triệu ÷ 28,7% ≈ 362 triệu km².",
    "Một khảo sát ngoài khơi Alaska, chạy từng tuyến một, kéo dài 40 năm. Hơn 70% đáy biển vẫn là khoảng trắng.",
    "Nhờ thay sợi dây bằng tiếng vang, ta mới bắt đầu vẽ được đáy biển.",
  ],
};

export type Beat = {text: string; start: number; dur: number};
export type SceneTl = {id: SceneId; start: number; dur: number; beats: Beat[]; bs: number[]};
const ORDER: SceneId[] = ['hook', 'cu', 'chal', 'vang', 'meteor', 'nay'];

export function timeline(): {scenes: SceneTl[]; total: number; beats: Beat[]} {
  let f = 0;
  let voiceIdx = 0;
  const all: Beat[] = [];
  const scenes: SceneTl[] = ORDER.map((id) => {
    const texts = id === 'nay' ? [...TEXT_C[id], ''] : TEXT_C[id];
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
