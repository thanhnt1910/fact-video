"""Nhận dạng giọng đọc để lấy mốc từng chữ: python phude_asr.py <kịch bản.json> <thư mục giọng> <ra.json> [mô hình]
Chạy trên GitHub Actions (cần tải mô hình từ HuggingFace). Ra: {"số câu": [[chữ, bắt đầu, kết thúc], ...]}"""
import json, os, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
def main():
    src, vd, dst = sys.argv[1:4]; mo = sys.argv[4] if len(sys.argv) > 4 else 'medium'; goi_y = not (len(sys.argv) > 5 and sys.argv[5] == 'khong_goi_y')
    if not goi_y: dst = dst.replace('.json', '_ngoai.json')   # nghe không gợi ý: ghi file riêng, không đè mốc chữ đang dùng
    m = WhisperModel(mo, device='cpu', compute_type='int8', cpu_threads=os.cpu_count() or 4)
    beats = json.load(open(src, encoding='utf-8'))
    res = json.load(open(dst, encoding='utf-8')) if os.path.exists(dst) else {}
    import hashlib; hp = dst + '.h.json'; HH = json.load(open(hp)) if os.path.exists(hp) else {}   # mã nội dung file giọng: giọng đổi thì nhận dạng lại
    for i, b in enumerate(beats):
        n = str(b['n'])
        hh = hashlib.md5(open(f'{vd}/{n}.mp3','rb').read()).hexdigest()
        if n in res and (n not in HH or HH[n] == hh): HH[n] = hh; continue
        au = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'{vd}/{n}.mp3','-f','s16le','-ac','1','-ar','16000','-'],capture_output=True).stdout, np.int16).astype(np.float32) / 32768.0
        segs, _ = m.transcribe(au, language='vi', word_timestamps=True, beam_size=1,
                               condition_on_previous_text=False, initial_prompt=(b['text'] if goi_y else None), vad_filter=False)
        HH[n] = hh
        res[n] = [[w.word.strip(), round(w.start, 3), round(w.end, 3)] for s in segs for w in (s.words or [])]
        if i % 20 == 0:
            json.dump(res, open(dst, 'w', encoding='utf-8'), ensure_ascii=False); json.dump(HH, open(hp, 'w')); print(i, len(beats), flush=True)
    json.dump(res, open(dst, 'w', encoding='utf-8'), ensure_ascii=False); json.dump(HH, open(hp, 'w'))
    print('xong', len(res))
if __name__ == '__main__': main()
