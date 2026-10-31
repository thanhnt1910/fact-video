"""Đo và ghép nghe thử A/B giọng: python ab_do.py   (đọc assets/ab_giong/<B|C><lần>/sadaltager)
B = hồ sơ cũ (STYLE_KE + tone story, đối chứng), C = hồ sơ cố định mới (STYLE_C). Mỗi lần gồm 2 cụm 16 đoạn tạo ở 2 request độc lập (nối tiếp).
Ra: assets/ab_giong/nghe_<B|C><lần>.mp3 (nghe liền) và assets/ab_giong/bao_cao.md"""
import json, os, re, subprocess, sys, statistics as st
sys.path.insert(0, "phim_ban_do")
import numpy as np
from kiem_cao_do import doc, f0_trung_vi
R = "assets/ab_giong"; KB = json.load(open("ke-hoach/thu-giong-hai/ab_mau.json", encoding="utf-8")); SR = 24000
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip() or 0)
def centroid(x):
    n = 2 ** int(np.log2(min(len(x), SR * 20))); X = np.abs(np.fft.rfft(x[:n] * np.hanning(n))); f = np.fft.rfftfreq(n, 1 / SR); return float((X * f).sum() / (X.sum() + 1e-9))
rows = {}
for var in "BC":
    for t in "123":
        d = f"{R}/{var}{t}/sadaltager"
        if not os.path.isdir(d): continue
        ids = [b["n"] for b in KB if os.path.exists(f"{d}/{b['n']}.mp3")]
        if len(ids) < len(KB): continue
        open("/tmp/l.txt", "w").write("".join(f"file '{os.path.abspath(d)}/{n}.mp3'\n" for n in ids))
        subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i","/tmp/l.txt","-c:a","libmp3lame","-b:a","96k",f"{R}/nghe_{var}{t}.mp3"],check=True)
        out = {}
        for ci, grp in enumerate((KB[:16], KB[16:])):
            xs = [doc(f"{d}/{b['n']}.mp3") for b in grp]; x = np.concatenate(xs)
            words = sum(len(re.sub(r"[^\w\s]", " ", b["text"]).split()) for b in grp)
            out[ci] = {"f0": f0_trung_vi(x), "wps": words / (len(x) / SR), "rms": float(20 * np.log10(np.sqrt((x / 32768) ** 2).mean() + 1e-9)) if False else float(20 * np.log10(np.sqrt(np.mean((x / 32768) ** 2)) + 1e-9)), "cen": centroid(x)}
        lg = json.load(open(f"{d}/nhat_ky_giong.json")) if os.path.exists(f"{d}/nhat_ky_giong.json") else {}
        out["model"] = sorted({v.get("model") for v in lg.values()}); out["dp"] = any(v.get("du_phong") for v in lg.values())
        rows[f"{var}{t}"] = out
L = ["# So sánh giọng: B (hồ sơ cũ) và C (hồ sơ cố định mới)\n", "Mỗi lần gồm 2 cụm tạo ở 2 request độc lập. f0 = cao độ trung vị (Hz), wps = chữ/giây, rms = mức (dB), cen = trọng tâm phổ (Hz, độ sáng).\n",
     "| Lần | model | dự phòng | f0 cụm1 | f0 cụm2 | lệch f0 | wps 1 | wps 2 | rms 1 | rms 2 | sáng 1 | sáng 2 |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for k, o in rows.items():
    L.append(f"| {k} | {','.join(map(str,o['model']))} | {o['dp']} | {o[0]['f0']:.1f} | {o[1]['f0']:.1f} | {abs(o[0]['f0']-o[1]['f0']):.1f} | {o[0]['wps']:.2f} | {o[1]['wps']:.2f} | {o[0]['rms']:.1f} | {o[1]['rms']:.1f} | {o[0]['cen']:.0f} | {o[1]['cen']:.0f} |")
L.append("\n## Tóm tắt theo hồ sơ (3 lần tạo)\n")
for var in "BC":
    ks = [k for k in rows if k[0] == var]
    if len(ks) < 2: continue
    f = [rows[k][c]["f0"] for k in ks for c in (0, 1)]; w = [rows[k][c]["wps"] for k in ks for c in (0, 1)]; j = [abs(rows[k][0]["f0"] - rows[k][1]["f0"]) for k in ks]; ce = [rows[k][c]["cen"] for k in ks for c in (0, 1)]
    L.append(f"- **{var}**: f0 trung bình {st.mean(f):.1f} Hz, độ lệch chuẩn {st.pstdev(f):.1f}; tốc độ {st.mean(w):.2f} chữ/giây, độ lệch chuẩn {st.pstdev(w):.2f}; độ sáng độ lệch chuẩn {st.pstdev(ce):.0f} Hz; lệch cao độ giữa hai cụm nối tiếp trung bình {st.mean(j):.1f} Hz")
L.append("\nĐộ lệch chuẩn càng nhỏ thì giọng càng ổn định giữa các lần và giữa các cụm. Số đo chỉ là chỉ báo; quyết định cuối cần nghe các file nghe_B*.mp3 và nghe_C*.mp3.")
open(f"{R}/bao_cao.md", "w", encoding="utf-8").write("\n".join(L)); print("\n".join(L))
