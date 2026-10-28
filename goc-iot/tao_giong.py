"""Đọc lời 6 video Góc IoT bằng giọng Gemini (mỗi cảnh một lượt đọc riêng).
Ra: goc-iot/giong/vN_sK.wav và goc-iot/giong/thoi-luong.json. Cảnh đã có file thì bỏ qua (chạy lại được)."""
import io, json, os, sys, wave
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
import gemini_tts
import am_thanh  # số, năm -> chữ (chỉ cho bản gửi giọng đọc, chữ trên màn hình giữ nguyên)

STYLE = ("Native Vietnamese voice (Northern accent, Hanoi) of 'Bóng', a friendly smart light-bulb who teaches ordinary "
         "families how to keep their smart home safe. Upbeat, playful and a little cheeky, dry sense of humor, clear diction, "
         "natural Vietnamese tones, medium pace. Slow down and soften for warnings and risks, then bounce back for the tips. "
         "Short natural pauses between sentences. Not robotic, not news-anchor flat.")

def dur(wav):
    with wave.open(io.BytesIO(wav)) as w:
        return w.getnframes() / float(w.getframerate())

def main():
    kb = json.loads((ROOT / "kich-ban.json").read_text(encoding="utf-8"))
    voice = os.environ.get("GOC_IOT_VOICE") or kb["giong"]
    pron = kb["phat_am"]
    out = ROOT / "giong"; out.mkdir(exist_ok=True)
    tl = out / "thoi-luong.json"
    info = json.loads(tl.read_text(encoding="utf-8")) if tl.exists() else {}
    only = [int(x) for x in os.environ.get("GOC_IOT_VIDEOS", "").replace(",", " ").split() if x]
    bad = []
    for v in kb["videos"]:
        if only and v["id"] not in only:
            continue
        for k, text in enumerate(v["scenes"], 1):
            name = f"v{v['id']}_s{k}"
            f = out / f"{name}.wav"
            if f.exists() and name in info:
                continue
            say = text
            for a in sorted(pron, key=len, reverse=True):
                say = say.replace(a, pron[a])
            say = am_thanh.chuan_hoa(say, tu_dien={})
            words = len(text.split())
            best = None
            for attempt in range(3):
                wav = gemini_tts.synth(say, STYLE, voice)
                d = dur(wav)
                wps = words / d
                print(f"{name} lần {attempt+1}: {d:.2f}s, {wps:.2f} từ/giây", flush=True)
                if best is None or abs(wps - 2.6) < abs(best[1] - 2.6):
                    best = (wav, wps, d)
                if 1.8 <= wps <= 3.6:   # tốc độ bình thường: không bỏ câu, không kéo dài
                    break
            wav, wps, d = best
            if not (1.8 <= wps <= 3.6):
                bad.append(name)
            f.write_bytes(wav)
            info[name] = {"giay": round(d, 3), "tu": words, "tu_moi_giay": round(wps, 2), "chu": text}
            tl.write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Cảnh tốc độ lạ (cần nghe lại):", bad or "không có", flush=True)

if __name__ == "__main__":
    main()
