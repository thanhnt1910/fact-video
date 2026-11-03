"""Thăm dò VieNeu: phiên bản, chế độ (mode) và đọc thử cùng một câu ở từng chế độ."""
import importlib.metadata as m, inspect, re, sys, time, os, pathlib
import vieneu
print("phiên bản gói vieneu:", m.version("vieneu"))
print("chữ ký Vieneu:", inspect.signature(vieneu.Vieneu))
src = inspect.getsource(vieneu)
print("--- docstring ---"); print((vieneu.Vieneu.__doc__ or "")[:2500])
try:
    print("--- mã nguồn Vieneu (đoạn có 'mode') ---")
    for i, l in enumerate(inspect.getsource(vieneu.Vieneu).splitlines()):
        if re.search(r"mode|turbo|standard|fast|gguf|onnx", l, re.I): print(i, l.strip()[:200])
except Exception as e:
    print("không đọc được mã:", e)
cands = sorted(set(re.findall(r"['\"]([a-z0-9_\-]{3,20})['\"]", " ".join(l for l in src.splitlines() if "mode" in l.lower()))))
print("ứng viên mode:", cands)
text = "Tào Tháo mang quân về phía bắc, và chuyện lớn chỉ mới bắt đầu."
out = pathlib.Path("demo/probe"); out.mkdir(parents=True, exist_ok=True)
for md in [None] + [c for c in cands if c in ("turbo", "standard", "fast", "quality", "remote", "gpu", "cpu", "v3", "turbo_gpu")]:
    try:
        t = time.time()
        tts = vieneu.Vieneu(mode=md) if md else vieneu.Vieneu()
        names = [str(v) for v in tts.list_preset_voices()]
        voice = next((n for n in names if "Đức Trí" in n), None)
        v = None
        try: v = tts.get_preset_voice("Đức Trí")
        except Exception: pass
        audio = tts.infer(text, voice=v) if v is not None else tts.infer(text)
        f = out / f"mode_{md or 'mac_dinh'}.wav"
        tts.save(audio, str(f))
        print(f"mode={md}: OK {time.time()-t:.0f}s, {len(names)} giọng ->", f)
    except Exception as e:
        print(f"mode={md}: LỖI {type(e).__name__}: {str(e)[:200]}")
