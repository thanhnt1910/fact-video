"""Đọc kịch bản hài theo cụm câu (ít lượt gọi Gemini): python thu_giong_hai_cum.py <file.json> <giọng> <thư mục ra> [số câu mỗi cụm]
Chỉ đọc các câu còn thiếu; mỗi cụm gọi Gemini 1 lần rồi cắt thành từng câu theo khoảng lặng (như long_video.py)."""
import io, json, subprocess, sys, wave, hashlib
from pathlib import Path
import numpy as np
import gemini_tts, audio_fx
from thu_giong_hai import STYLE_HAI, TONE, STYLE_KE, TONE_KE
SR = 24000
STYLE_A = ("Native Vietnamese storyteller (Northern accent) telling a true story aloud to one listener: conversational yet resonant. "
           "Clear, bright, full voice with firm projection and crisp diction on every syllable and tone mark; medium pace, never rushed; "
           "natural flowing intonation so the sentences connect into one continuous narration, with only short natural breaths between them, no theatrical pauses. "
           "Stress key words and names; pitch lifts a little on questions and turning points and settles at the end of each sentence. "
           "Not a news anchor, not a stage actor, never mumbling, never whispering, never low or sleepy. ")
# Hồ sơ giọng cố định C = MẶC ĐỊNH từ 01/11/2026 (chủ kênh chọn nghe_C1): dùng nguyên văn cho mọi cụm, mọi tone. STYLE_VAR=B/A chỉ để thử A/B
STYLE_C = ("Native Vietnamese male narrator, Northern (Hanoi) accent, mature, bright and resonant, with clear diction. "
           "Documentary-style history storyteller: steady medium pace, even pitch and even energy from start to end, natural flowing intonation, short natural pauses between sentences. "
           "Stress only names and key actions, with light emotion that never changes the voice. Never whispering, never shouting, never theatrical, never sleepy or too low, not a news anchor. "
           "Keep exactly the same voice, pitch, pace and tone in every line.")
CONFIG_VERSION = "v3-2026-11-01-C"   # đổi khi đổi cách tổng hợp; nằm trong mã hash để nhận ra file âm thanh cũ
import os as _os
for _n in ["GEMINI_API_KEY"] + [f"GEMINI_API_KEY_{i}" for i in range(2, 16)] + ["GEMINI_API_KEYS"]:   # tên secret -> 4 ký tự cuối (không in khóa)
    _v = _os.environ.get(_n, "").strip()
    print(f"   [khóa] {_n}: " + (f"…{_v[-4:]}" if _v else "trống"), flush=True)

def split_by_pauses(samples, weights):
    """Chia âm thanh 1 chương thành các đoạn theo khoảng lặng gần nhất với tỉ lệ độ dài chữ."""
    x = np.frombuffer(samples.tobytes(), np.int16).astype(np.float32)
    win = int(0.02 * SR)
    k = len(x) // win
    rms = np.sqrt((x[:k * win].reshape(k, win) ** 2).mean(1) + 1e-6)
    speech = rms[rms > np.percentile(rms, 40)]
    thr = max(150.0, 0.1 * float(np.median(speech)) if len(speech) else 150.0)
    quiet = rms < thr
    # cắt lặng đầu/cuối
    nz = np.where(~quiet)[0]
    a, b = (nz[0], nz[-1] + 1) if len(nz) else (0, k)
    runs, i = [], a
    while i < b:
        if quiet[i]:
            j = i
            while j < b and quiet[j]:
                j += 1
            if j - i >= 12:            # ≥ 0,24 giây
                runs.append(((i + j) / 2, j - i))
            i = j
        else:
            i += 1
    total = b - a
    cum = np.cumsum(weights)[:-1] / sum(weights)
    cuts, last = [], a
    for c in cum:
        exp = a + c * total
        cands = [r for r in runs if r[0] > last + 25]
        if cands:
            best = min(cands, key=lambda r: abs(r[0] - exp) - 0.6 * r[1])
            pos = best[0] if abs(best[0] - exp) < 0.25 * total else exp
        else:
            pos = exp
        cuts.append(int(pos))
        last = pos
    bounds = [a] + cuts + [b]
    return [(bounds[n] * win, bounds[n + 1] * win) for n in range(len(bounds) - 1)], (a * win, b * win)

def main():
    src, voice, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    per = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    beats = json.loads(Path(src).read_text(encoding="utf-8"))
    d = out / voice.lower(); d.mkdir(parents=True, exist_ok=True)
    fd = d / "thoi_luong.json"; dur = json.loads(fd.read_text()) if fd.exists() else {}
    hs = d / "hash.json"; H = json.loads(hs.read_text()) if hs.exists() else {}
    h2s = d / "hash_day_du.json"; H2 = json.loads(h2s.read_text()) if h2s.exists() else {}      # hash gồm chữ, tone, voice, prompt, model, phiên bản cấu hình
    lgs = d / "nhat_ky_giong.json"; LOG = json.loads(lgs.read_text()) if lgs.exists() else {}  # từng đoạn: model thực tế, voice, prompt, giờ tạo
    kh = d / f"khoa_model_{Path(src).stem}.json"   # model + phương thức đã chọn cho video này (chọn ở lần gọi thành công đầu tiên, sau đó khóa)
    if kh.exists():
        _k = json.loads(kh.read_text()); gemini_tts.LOCKED = (_k["kind"], _k["model"])
        print(f"   [giọng] model đã khóa cho video: {_k['model']} ({'interactions' if _k['kind']=='i' else 'generateContent'}), chọn lúc {_k['thoi_diem']}", flush=True)
    gemini_tts.REQ_LOG = str(d / "nhat_ky_request.jsonl")
    # tạo lại CÓ KIỂM SOÁT: GIONG_TAO_LAI="22001,22005-22010" -> file cũ được chuyển vào thư mục _cu (không xóa), rồi đọc lại đúng các đoạn đó
    for tok in [t for t in _os.environ.get("GIONG_TAO_LAI", "").split(",") if t.strip()]:
        a, _, z = tok.strip().partition("-"); 
        for n in range(int(a), int(z or a) + 1):
            f = d / f"{n}.mp3"
            if f.exists():
                (d / "_cu").mkdir(exist_ok=True); f.rename(d / "_cu" / f"{n}_{int(__import__('time').time())}.mp3"); dur.pop(str(n), None)
    todo = [b for b in beats if not (str(b["n"]) in dur and (d / f"{b['n']}.mp3").exists())]
    cu = [b["n"] for b in beats if str(b["n"]) in dur and str(b["n"]) not in H2]
    if cu: print(f"   [giọng] {len(cu)} đoạn chưa có hash đầy đủ (tạo trước khi có nhật ký): {cu[0]}…{cu[-1]}; dùng GIONG_TAO_LAI để đọc lại có kiểm soát", flush=True)
    print("còn thiếu", len(todo), "câu", flush=True)
    chunks, cur = [], []
    for b in todo:
        if cur and (len(cur) >= per or b["n"] != cur[-1]["n"] + 1 or (b["tone"] in TONE_KE and b["tone"] != cur[-1]["tone"])): chunks.append(cur); cur = []
        cur.append(b)
    if cur: chunks.append(cur)
    for ch in chunks:
        _sv = _os.environ.get("STYLE_VAR", "C")
        _svf = Path("ke-hoach/thu-giong-hai/style_var.txt")        # tệp chọn hồ sơ giọng (A/B/C) thay biến môi trường
        if _svf.exists() and _svf.read_text().strip(): _sv = _svf.read_text().strip()
        if _sv == "C":
            style = STYLE_C
        elif _sv == "A":
            style = STYLE_A
        elif _sv == "B":
            style = STYLE_KE + TONE_KE["story"]
        elif ch[0]["tone"] in TONE_KE:
            style = STYLE_KE + TONE_KE[ch[0]["tone"]] + " Read each sentence as its own beat with a clear short pause between sentences."
        else:
            calm = sum(1 for b in ch if b["tone"] == "calm") > len(ch) / 2
            style = STYLE_HAI + TONE["calm" if calm else "light"] + " Read each sentence as its own beat with a clear short pause between sentences."
        _ov = Path("ke-hoach/thu-giong-hai/style_thu.txt")      # prompt thử nghiệm (nếu có thì thay hồ sơ trên)
        if _ov.exists() and _ov.read_text(encoding="utf-8").strip():
            style = _ov.read_text(encoding="utf-8").strip(); _sv = "thu"
        text = "\n\n".join(b.get("tts", b["text"]) for b in ch)
        gemini_tts.CTX.update({"nhom": f"{ch[0]['n']}-{ch[-1]['n']}", "style_id": hashlib.md5(style.encode()).hexdigest()[:8], "style_var": _sv or "mac_dinh", "config": CONFIG_VERSION})
        try: wav = gemini_tts.synth(text, style, voice)
        except SystemExit: raise
        except Exception as e:
            print("LỖI cụm", ch[0]["n"], str(e)[:400], flush=True)
            if gemini_tts.LOCKED: print("   [giọng] DỪNG TOÀN BỘ: không chuyển model giữa chừng; file đã tạo được giữ nguyên", flush=True); break
            continue
        if not gemini_tts.LOCKED and gemini_tts.LAST:
            gemini_tts.LOCKED = ("i" if gemini_tts.LAST["kind"] == "interactions" else "g", gemini_tts.LAST["model"])
            kh.write_text(json.dumps({"kind": gemini_tts.LOCKED[0], "model": gemini_tts.LOCKED[1], "voice": voice, "thoi_diem": gemini_tts.LAST["time"], "du_phong": gemini_tts.LAST["fallback"]}))
            print(f"   [giọng] ĐÃ KHÓA model cho video: {gemini_tts.LOCKED[1]} ({gemini_tts.LAST['kind']}){' — LÀ MODEL DỰ PHÒNG' if gemini_tts.LAST['fallback'] else ''}", flush=True)
        with wave.open(io.BytesIO(wav)) as f:
            global SR; SR = f.getframerate(); x = np.frombuffer(f.readframes(f.getnframes()), np.int16)
        spans, _ = split_by_pauses(x, [max(1, len(b.get("tts", b["text"]).split())) for b in ch])
        for b, (s, e) in zip(ch, spans):
            s, e = max(0, int(s - 0.05 * SR)), min(len(x), int(e + 0.08 * SR))
            seg = x[s:e]; w = d / f"{b['n']}.wav"
            with wave.open(str(w), "wb") as o: o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes(seg.tobytes())
            mp3 = d / f"{b['n']}.mp3"
            subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(w),"-af",audio_fx.VOICE_CHAIN,"-ar","44100","-b:a","128k",str(mp3)],check=True); w.unlink()
            dur[str(b["n"])] = len(seg) / SR
            H[str(b["n"])] = hashlib.md5((b["text"]+b["tone"]+voice).encode()).hexdigest()
            H2[str(b["n"])] = hashlib.md5((b["text"]+b["tone"]+voice+style+gemini_tts.LAST.get("model","")+gemini_tts.LAST.get("kind","")+CONFIG_VERSION).encode()).hexdigest()
            LOG[str(b["n"])] = {"nhom": f"{ch[0]['n']}-{ch[-1]['n']}", "model": gemini_tts.LAST.get("model"), "cach_goi": gemini_tts.LAST.get("kind"), "voice": voice,
                                "style_id": hashlib.md5(style.encode()).hexdigest()[:8], "style_var": _sv or "mac_dinh", "thoi_diem": gemini_tts.LAST.get("time"),
                                "du_phong": gemini_tts.LAST.get("fallback"), "config": CONFIG_VERSION, "tone": b["tone"]}
        hs.write_text(json.dumps(H)); fd.write_text(json.dumps(dur))
        h2s.write_text(json.dumps(H2)); lgs.write_text(json.dumps(LOG, ensure_ascii=False, indent=0))
        print(f"   [giọng] nhóm {ch[0]['n']}-{ch[-1]['n']}: model={gemini_tts.LAST.get('model')} ({gemini_tts.LAST.get('kind')}) voice={voice} style={hashlib.md5(style.encode()).hexdigest()[:8]}/{_sv or 'mac_dinh'} dự_phòng={gemini_tts.LAST.get('fallback')} lúc {gemini_tts.LAST.get('time')}", flush=True)
        if gemini_tts.LAST.get("fallback"): print("   [giọng] CẢNH BÁO: nhóm này do model DỰ PHÒNG tạo, chất giọng có thể khác các nhóm còn lại", flush=True)
        print("OK cụm", ch[0]["n"], "-", ch[-1]["n"], round(len(x)/SR, 1), "giây", flush=True)

def bao_cao(beats, d):
    lg = json.loads((d / "nhat_ky_giong.json").read_text()) if (d / "nhat_ky_giong.json").exists() else {}
    ids = [str(b["n"]) for b in beats]; co = [i for i in ids if i in lg]
    print(f"[báo cáo giọng] {len(co)}/{len(ids)} đoạn có nhật ký tạo giọng")
    for k in ("model", "cach_goi", "voice", "style_id"):
        v = sorted({str(lg[i].get(k)) for i in co}); print(f"   {k}: {', '.join(v)}" + ("" if len(v) <= 1 else "   <-- KHÔNG ĐỒNG NHẤT"))
    thieu = [i for i in ids if i not in lg]
    if thieu: print(f"   {len(thieu)} đoạn không có nhật ký (tạo trước khi có nhật ký): {thieu[0]}…{thieu[-1]}")

if __name__ == "__main__":
    main()
    try:
        _b = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")); bao_cao(_b, Path(sys.argv[3]) / sys.argv[2].lower())
    except Exception as e: print("không in được báo cáo:", e)
