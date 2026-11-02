"""Xuất giọng Gemini đã đọc (trong bộ nhớ đệm assets/tts_cache) của TQ9 ra mp3 theo từng câu và ghép liền."""
import array, hashlib, json, subprocess, tempfile
from pathlib import Path
import make_video as mv, long_video as L, am_thanh, gemini_tts
s = json.load(open("scripts/TQ9.json", encoding="utf-8"))
chs = s["long"]["chapters"]; voice = s["long"]["voice"]; tu = am_thanh.load_dict()
out = Path("assets/thu_giong_hai/TQ9_gemini"); out.mkdir(parents=True, exist_ok=True)
work = Path(tempfile.mkdtemp()); full = array.array("h"); n = 0; have = []; miss = []
for ci, ch in enumerate(chs):
    loai = ch.get("loai_canh") or ("hook" if ci == 0 else "ket" if ci == len(chs) - 1 else "boi_canh" if ci == 1 else "leo_thang")
    extra = (am_thanh.sac_thai(loai, s.get("phong_cach") == "huyen-bi") + " " + s.get("giong_them", "")).strip()
    style = L.LONG_STYLE + (" " + extra if extra else "")
    for b in ch["beats"]:
        n += 1
        t = am_thanh.chuan_hoa(gemini_tts.clean_text(b["text"])[0], tu)
        key = hashlib.sha1(f"{voice}|{style}|{t}".encode()).hexdigest()[:16]
        wav = L.TTS_CACHE / f"{key}.wav"
        if not wav.exists(): miss.append(n); continue
        one = L._can_am_luong(mv.read_wav(wav)); w2 = work / f"{n:03d}.wav"; mv.write_wav(w2, one)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(w2), "-b:a", "96k", str(out / f"{n:03d}.mp3")], check=True)
        full.extend(one); full.extend(mv.silence(0.35)); have.append(n)
print("ĐÃ CÓ", len(have), "câu:", have[:3], "…", have[-3:]); print("CHƯA CÓ", len(miss), "câu:", miss[:5], "…")
if have:
    mv.write_wav(work / "all.wav", full)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(work / "all.wav"), "-b:a", "96k", str(out / "TQ9_gemini_da_doc.mp3")], check=True)
