"""Nhận dạng giọng đọc để lấy mốc từng chữ: python phude_asr.py <kịch bản.json> <thư mục giọng> <ra.json> [mô hình]
Chạy trên GitHub Actions (cần tải mô hình từ HuggingFace). Ra: {"số câu": [[chữ, bắt đầu, kết thúc], ...]}"""
import json, os, sys
from faster_whisper import WhisperModel
def main():
    src, vd, dst = sys.argv[1:4]; mo = sys.argv[4] if len(sys.argv) > 4 else 'medium'
    m = WhisperModel(mo, device='cpu', compute_type='int8', cpu_threads=os.cpu_count() or 4)
    beats = json.load(open(src, encoding='utf-8'))
    res = json.load(open(dst, encoding='utf-8')) if os.path.exists(dst) else {}
    for i, b in enumerate(beats):
        n = str(b['n'])
        if n in res: continue
        segs, _ = m.transcribe(f'{vd}/{n}.mp3', language='vi', word_timestamps=True, beam_size=1,
                               condition_on_previous_text=False, initial_prompt=b['text'], vad_filter=False)
        res[n] = [[w.word.strip(), round(w.start, 3), round(w.end, 3)] for s in segs for w in (s.words or [])]
        if i % 20 == 0:
            json.dump(res, open(dst, 'w', encoding='utf-8'), ensure_ascii=False); print(i, len(beats), flush=True)
    json.dump(res, open(dst, 'w', encoding='utf-8'), ensure_ascii=False)
    print('xong', len(res))
if __name__ == '__main__': main()
