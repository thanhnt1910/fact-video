"""
TỰ KIỂM TRA video / bài ảnh sau khi dựng, trước khi gửi đi.

  python review.py SL2                 kiểm tra mọi thứ đã dựng của SL2 (video ngắn + bài ảnh + video dài)
  python review.py SL2:ngan BA1:dai    chỉ video ngắn + bài ảnh của SL2, chỉ video dài của BA1
  python review.py --ci                kiểm tra các mã vừa dựng (ci_outputs.txt, ci_long.txt)
  python review.py SL2 --no-ai         chỉ kiểm tra kỹ thuật (không gọi Gemini, không tốn tiền)
  python review.py SL2 --telegram      gửi bản tóm tắt về Telegram (cần TG_TOKEN, TG_CHAT)

Tiết kiệm chi phí: chỉ gửi cả video cho Gemini xem lại khi lời kể / giọng đổi (REVIEW_VIDEO=always để luôn gửi);
mặc định dùng Flash-Lite; kịch bản được kiểm tra trước khi dựng (ci_render.py gọi precheck).

Các bước kiểm tra
  1. Kỹ thuật (ffmpeg, miễn phí): thời lượng, độ phân giải, có tiếng, khung đen, hình đứng im, mất tiếng, độ to.
  2. Kịch bản (Gemini đọc chữ): đối chiếu mục "Kiểm chứng" trong kế hoạch, số liệu khớp nhau, chính tả, nội dung cấm.
  3. Xem và nghe cả video (Gemini đọc video): giọng đọc đúng lời, hình đúng lời, chữ trên màn hình, chủ thể bị cắt.
  4. Soi từng khung hình rõ nét (Gemini đọc ảnh): lỗi tranh AI, ảnh sai nội dung, watermark, ảnh nhạy cảm.
  5. Bài ảnh Facebook: chữ trên ảnh, chính tả, ảnh hợp câu chữ.
  6. (Video dài) Đồng bộ: đoạn nào tốc độ đọc bất thường → ảnh có thể đổi sai chỗ.

Danh sách điều cần soi nằm trong review_checklist.md — thêm dòng vào đó mỗi khi gặp lỗi mới.

Kết quả trong output/<mã>/:
  <mã>_kiemtra_ngan.json / .txt   (video ngắn + bài ảnh)
  <mã>_kiemtra_dai.json  / .txt   (video dài)
Kết luận: "dat" (đạt) · "xem" (có cảnh báo, nên xem lại) · "loi" (có lỗi, không nên đăng).

Biến môi trường: GEMINI_API_KEY; REVIEW_MODELS (vd "gemini-3.8-flash,gemini-flash-latest");
REVIEW_DRY=1 (không gọi Gemini, chỉ ghi prompt ra output/<mã>/_review/ để xem thử).
"""
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
API = "https://generativelanguage.googleapis.com/v1beta"
UPLOAD = "https://generativelanguage.googleapis.com/upload/v1beta"
MODELS = [m.strip() for m in os.environ.get(
    # Flash-Lite trước (rẻ hơn vài lần), không dùng được thì lùi về Flash
    "REVIEW_MODELS", "gemini-flash-lite-latest,gemini-3.8-flash,gemini-flash-latest,gemini-2.5-flash").split(",") if m.strip()]
# REVIEW_VIDEO=always: luôn gửi cả video cho Gemini xem lại (mặc định chỉ gửi khi lời kể thay đổi)
VIDEO_ALWAYS = os.environ.get("REVIEW_VIDEO", "").strip().lower() == "always"
STAGE = "review"
CACHE = ROOT / "assets" / "tts_cache" / "review"
PLAN = ROOT / "ke-hoach" / "nguoi-gac-su-30-video.md"
CHECKLIST = ROOT / "review_checklist.md"
DRY = os.environ.get("REVIEW_DRY", "").strip() not in ("", "0")
_BAD_MODELS = set()   # model không dùng được (404…): lần sau bỏ qua luôn
FRAMES_PER_CALL = 10

PART_NAME = {"ngan": "video ngắn + bài ảnh", "dai": "video dài"}
VERDICT_TEXT = {"dat": "✅ ĐẠT", "xem": "⚠️ NÊN XEM LẠI", "loi": "❌ CÓ LỖI, CHƯA NÊN ĐĂNG"}

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def log(msg):
    print(msg, flush=True)


# ================================================================== tiện ích chung
def fmt_t(sec):
    sec = max(0, int(round(sec)))
    return f"{sec // 60:02d}:{sec % 60:02d}"


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run_ffmpeg(args, timeout=1800):
    r = subprocess.run([ffmpeg_exe(), "-hide_banner", "-nostdin"] + args, capture_output=True, timeout=timeout)
    return r.returncode, r.stderr.decode("utf-8", "replace")


def probe(path):
    """Thời lượng, kích thước, có tiếng hay không (đọc từ thông báo của ffmpeg, không cần ffprobe)."""
    _, err = run_ffmpeg(["-i", str(path)])
    info = {"duration": 0.0, "width": 0, "height": 0, "audio": "Audio:" in err}
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    if m:
        info["duration"] = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    m = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", err)
    if m:
        info["width"], info["height"] = int(m.group(1)), int(m.group(2))
    return info


def clean_voice(text):
    """Lời thoại như người xem sẽ nghe: bỏ thẻ [nhấn] [trầm]…, bỏ dấu ** tô màu."""
    return re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", text or "")).replace("**", "").strip()


def plain(text):
    return (text or "").replace("**", "").strip()


def issue(level, group, where, what, fix=""):
    return {"muc": level, "nhom": group, "vi_tri": where, "mo_ta": what, "sua": fix}


def checklist(section):
    if not CHECKLIST.exists():
        return ""
    txt = CHECKLIST.read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(section)}\s*$(.*?)(?=^## |\Z)", txt, re.S | re.M)
    return m.group(1).strip() if m else ""


def plan_notes(sid):
    """Mục của chuyện này trong kế hoạch 30 video (hook, diễn biến, cú lật, kiểm chứng)."""
    if not PLAN.exists():
        return ""
    txt = PLAN.read_text(encoding="utf-8")
    m = re.search(rf"^#### {re.escape(sid)}\..*?(?=^#### |^### |^## |\Z)", txt, re.S | re.M)
    return m.group(0).strip() if m else ""


# ================================================================== Gemini
class GeminiError(RuntimeError):
    pass


def _key():
    import gemini_keys
    k = gemini_keys.current() or (gemini_keys.all_keys() or [""])[0]
    if not k and not DRY:
        raise GeminiError("chưa có GEMINI_API_KEY")
    return k


def _request(url, data=None, method="GET", headers=None, timeout=300):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), r.headers
    except urllib.error.HTTPError as e:
        raise GeminiError(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:400]}")


def upload_file(path, mime):
    """Tải file lên Gemini (Files API, file tự xóa sau 48 giờ). Trả về (uri, name)."""
    key = _key()
    size = path.stat().st_size
    _, h = _request(f"{UPLOAD}/files", json.dumps({"file": {"display_name": path.name}}).encode(), "POST", {
        "x-goog-api-key": key, "Content-Type": "application/json",
        "X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start",
        "X-Goog-Upload-Header-Content-Length": str(size), "X-Goog-Upload-Header-Content-Type": mime})
    up = h.get("X-Goog-Upload-URL") or h.get("x-goog-upload-url")
    if not up:
        raise GeminiError("không nhận được địa chỉ tải lên")
    body, _ = _request(up, path.read_bytes(), "POST", {
        "Content-Length": str(size), "X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"},
        timeout=900)
    info = json.loads(body)["file"]
    for _ in range(120):   # chờ Gemini xử lý video (tối đa ~10 phút)
        if info.get("state") != "PROCESSING":
            break
        time.sleep(5)
        body, _ = _request(f"{API}/{info['name']}", headers={"x-goog-api-key": key})
        info = json.loads(body)
    if info.get("state") != "ACTIVE":
        raise GeminiError(f"Gemini không xử lý được file ({info.get('state')})")
    return info["uri"], info["name"]


def delete_file(name):
    try:
        _request(f"{API}/{name}", method="DELETE", headers={"x-goog-api-key": _key()}, timeout=60)
    except Exception:
        pass


def ask(parts, tag, dump_dir, cache_key=""):
    """Gửi prompt (chữ + ảnh/video) cho Gemini, nhận về JSON. Lưu đệm theo nội dung để chạy lại không tốn tiền."""
    text_parts = [p["text"] for p in parts if "text" in p]
    h = hashlib.sha1(("\n".join(text_parts) + "|" + cache_key).encode("utf-8")).hexdigest()[:20]
    cf = CACHE / f"{tag}_{h}.json"
    if cf.exists():
        return json.loads(cf.read_text(encoding="utf-8"))
    if DRY:
        dump_dir.mkdir(parents=True, exist_ok=True)
        (dump_dir / f"{tag}.txt").write_text("\n\n----\n\n".join(text_parts), encoding="utf-8")
        n_media = sum(1 for p in parts if "text" not in p)
        return {"van_de": [], "tom_tat": f"(chạy thử: chưa gọi Gemini, {n_media} ảnh/video đính kèm)"}
    import gemini_keys
    key = _key()
    body = json.dumps({"contents": [{"role": "user", "parts": parts}],
                       "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}}).encode()
    errs = []
    for model in [m for m in MODELS if m not in _BAD_MODELS] or MODELS:
        for attempt in range(4):
            try:
                raw, _ = _request(f"{API}/models/{model}:generateContent", body, "POST",
                                  {"x-goog-api-key": key, "Content-Type": "application/json"}, timeout=600)
                res = json.loads(raw)
                try:
                    import chi_phi
                    chi_phi.add_usage(STAGE, model, res.get("usageMetadata"))
                except Exception:
                    pass
                cand = (res.get("candidates") or [{}])[0]
                txt = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))
                if not txt:
                    raise GeminiError(f"không có câu trả lời ({cand.get('finishReason') or res.get('promptFeedback')})")
                out = json.loads(re.sub(r"^```(?:json)?|```$", "", txt.strip()).strip())
                if isinstance(out, list):
                    out = {"van_de": out}
                out["_model"] = model
                CACHE.mkdir(parents=True, exist_ok=True)
                cf.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
                return out
            except (GeminiError, json.JSONDecodeError, urllib.error.URLError, TimeoutError) as e:
                msg = str(e)
                if gemini_keys.is_quota_error(msg) and "HTTP" in msg and len(gemini_keys.all_keys()) > 1:
                    if gemini_keys.mark_bad(key, msg):   # còn khóa khác: đổi khóa rồi thử lại ngay
                        key = gemini_keys.current()
                        continue
                if any(c in msg for c in ("429", "500", "503", "timed out")) and attempt < 3:
                    time.sleep(20 * (attempt + 1))
                    continue
                errs.append(f"{model}: {msg[:160]}")
                if "404" in msg or "not found" in msg.lower():
                    _BAD_MODELS.add(model)
                break
    raise GeminiError(" | ".join(errs))


def img_part(path):
    return {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(Path(path).read_bytes()).decode()}}


ANSWER_FORMAT = """
TRẢ LỜI bằng JSON đúng dạng sau, viết tiếng Việt:
{"van_de": [{"muc": "loi" hoặc "canh_bao", "vi_tri": "…", "mo_ta": "…", "sua": "…"}], "tom_tat": "một câu nhận xét chung"}
- "loi": chắc chắn sai và không nên đăng (sai sự thật, đọc sai tên/số, bỏ câu, hình sai nội dung,
  chủ thể bị cắt mất đầu, tranh AI dị dạng rõ, chữ tràn/che, nội dung cấm).
- "canh_bao": nghi ngờ, cần người xem lại (không chắc, hoặc lỗi nhỏ ảnh hưởng chất lượng).
- "vi_tri": nơi xảy ra, ví dụ "00:12", "cảnh 3", "khung 5", "ảnh bài đăng 2", "đoạn 14".
- "mo_ta": nói cụ thể thấy/nghe gì, đối chiếu với điều đúng. "sua": cách sửa ngắn gọn (sửa câu gì trong kịch bản, đổi ảnh…).
- Chỉ báo vấn đề có thật mà bạn thấy/nghe rõ. Không báo chuyện khen chê phong cách, không bịa lỗi.
  Không có vấn đề thì để "van_de": [].
"""


# ================================================================== 1. kỹ thuật
def tech_check(mp4, kind, narration=None, quiet_ranges=()):
    """kind: "ngan" (dọc 1080x1920, 55–90 giây) hoặc "dai" (ngang 1920x1080, độ dài theo nội dung, không còn sàn 10 phút từ 30/10/2026)."""
    out, label = [], ("Video ngắn" if kind == "ngan" else "Video dài")
    g = "Kỹ thuật"
    if not mp4.exists():
        return [issue("loi", g, label, f"không thấy file {mp4.name}")]
    info = probe(mp4)
    d = info["duration"]
    lo, hi = (55, 90) if kind == "ngan" else (300, 1200)  # video dài: không còn sàn 10 phút (30/10/2026); ngoài 5–20 phút = cảnh báo, dưới 3 phút hoặc trên 32 phút = lỗi
    if d < lo * 0.6 or d > hi * 1.6:
        out.append(issue("loi", g, label, f"thời lượng {fmt_t(d)} quá xa mức {fmt_t(lo)}–{fmt_t(hi)}"))
    elif not lo <= d <= hi:
        out.append(issue("canh_bao", g, label, f"thời lượng {fmt_t(d)} ngoài mức {fmt_t(lo)}–{fmt_t(hi)}"))
    want = (1080, 1920) if kind == "ngan" else (1920, 1080)
    if (info["width"], info["height"]) != want:
        out.append(issue("loi", g, label, f"kích thước {info['width']}x{info['height']}, cần {want[0]}x{want[1]}"))
    if not info["audio"]:
        out.append(issue("loi", g, label, "video không có tiếng"))
        return out

    freeze_d = 4 if kind == "ngan" else 10
    vf = f"scale=320:-2,blackdetect=d=0.4:pix_th=0.08,freezedetect=n=0.002:d={freeze_d}"
    code, err = run_ffmpeg(["-i", str(mp4), "-vf", vf, "-af", "ebur128", "-f", "null", "-"])
    if code != 0:
        out.append(issue("canh_bao", g, label, "ffmpeg không đọc hết được video (file có thể hỏng)"))
    for m in re.finditer(r"black_start:([\d.]+) black_end:([\d.]+)", err):
        a, b = float(m.group(1)), float(m.group(2))
        if a > 0.5 and b < d - 0.5:
            out.append(issue("loi" if b - a > 1.5 else "canh_bao", g, f"{label} {fmt_t(a)}",
                             f"màn hình đen {b - a:.1f} giây giữa video",
                             "xem ảnh của cảnh đó có tải được không"))
    starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", err)]
    durs = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", err)]
    for a, dur in zip(starts, durs):
        if a + dur < d - 7:   # cuối video đứng hình chờ lời chào là bình thường
            out.append(issue("canh_bao", g, f"{label} {fmt_t(a)}", f"hình đứng im {dur:.0f} giây (không chuyển động)",
                             "kiểm tra cảnh đó có bị thiếu ảnh / lỗi chuyển động không"))
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    if m:
        lufs = float(m[-1])
        if not -17 <= lufs <= -11:
            out.append(issue("canh_bao", g, label, f"độ to {lufs:.1f} LUFS (chuẩn mạng xã hội khoảng -14)"))

    # mất tiếng: đo trên giọng đọc gốc nếu có (nhạc nền che mất chỗ mất giọng), không thì đo trên video
    src, thr, min_d = (narration, "-40dB", 2.4) if narration and narration.exists() else (mp4, "-50dB", 2.5)
    _, err = run_ffmpeg(["-i", str(src), "-vn", "-af", f"silencedetect=n={thr}:d={min_d}", "-f", "null", "-"])
    s_starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    s_ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    for a, b in zip(s_starts, s_ends + [d] * (len(s_starts) - len(s_ends))):
        if a < 1 or b > d - 4:
            continue
        if any(qa - 2.5 <= a and b <= qb + 2.5 for qa, qb in quiet_ranges):   # thẻ chương + khoảng nghỉ trước/sau thẻ
            continue   # đoạn thẻ chương: im lặng có chủ đích
        out.append(issue("loi" if b - a > 4 else "canh_bao", g, f"{label} {fmt_t(a)}",
                         f"mất giọng đọc {b - a:.1f} giây", "nghe lại đoạn này; đọc lại câu bị thiếu"))
    return out


def extract_frame(mp4, t, out, width):
    run_ffmpeg(["-y", "-ss", f"{max(0, t):.2f}", "-i", str(mp4), "-frames:v", "1",
                "-vf", f"scale={width}:-2", "-q:v", "3", str(out)], timeout=120)
    return out.exists()


def small_copy(mp4, out, kind):
    """Bản nhẹ để tải lên Gemini (đủ để xem và nghe, rẻ và nhanh)."""
    if out.exists() and out.stat().st_mtime > mp4.stat().st_mtime:
        return out
    scale = "480:-2" if kind == "ngan" else "640:-2"
    code, err = run_ffmpeg(["-y", "-i", str(mp4), "-vf", f"scale={scale},fps=10", "-c:v", "libx264", "-preset",
                            "veryfast", "-crf", "30", "-c:a", "aac", "-b:a", "64k", "-ac", "1", str(out)])
    if code != 0:
        raise RuntimeError("không nén được video để gửi kiểm tra: " + err[-300:])
    return out


# ================================================================== dữ liệu kịch bản
def scene_onscreen(sc):
    """Chữ hiện trên hình của một cảnh video ngắn."""
    bits = []
    for k in ("text", "pre", "value", "unit", "caption", "title", "sub", "recap", "question", "answer"):
        if sc.get(k):
            bits.append(plain(str(sc[k])))
    for b in sc.get("bullets", []) or []:
        bits.append(plain(b.get("text", "") if isinstance(b, dict) else str(b)))
    for b in sc.get("items", []) or []:
        bits.append(plain(json.dumps(b, ensure_ascii=False) if isinstance(b, dict) else str(b)))
    return " · ".join(x for x in bits if x)


def short_scene_list(script, timeline):
    times = {}
    if timeline:
        for i, sc in enumerate(timeline.get("scenes", [])):
            times[i] = (sc["start"], sc["start"] + sc["dur"])
    lines = []
    for i, sc in enumerate(script.get("scenes", [])):
        t = f" [{fmt_t(times[i][0])}–{fmt_t(times[i][1])}]" if i in times else ""
        img = sc.get("image") or {}
        cred = img.get("credit", "")[:90] if isinstance(img, dict) else ""
        lines.append(f"Cảnh {i + 1}{t} ({sc.get('type')})\n  Lời đọc: {clean_voice(sc.get('voice'))}\n"
                     f"  Chữ trên hình: {scene_onscreen(sc)}" + (f"\n  Ảnh: {cred}" if cred else ""))
    return "\n".join(lines)


def long_beat_list(script, data=None, max_chars=None):
    lines, k = [], 0
    spoken = (data or {}).get("spoken") or []
    for ci, ch in enumerate(script["long"]["chapters"]):
        lines.append(f"## Chương {ci}: {ch.get('title') or '(mở đầu)'}")
        for b in ch["beats"]:
            t = f" [{fmt_t(spoken[k]['start'])}–{fmt_t(spoken[k]['speech_end'])}]" if k < len(spoken) else ""
            src = ("tranh AI: " + b["ai"][:140]) if b.get("ai") else (
                "ảnh tư liệu: " + (b.get("image") or {}).get("credit", "")[:90] if b.get("image") else "giữ ảnh đoạn trước")
            lines.append(f"Đoạn {k + 1}{t}: {plain(b.get('text'))}\n   ({src})")
            k += 1
    txt = "\n".join(lines)
    return txt[:max_chars] if max_chars else txt


def short_texts(script):
    p = script.get("post") or {}
    N = script.get("ngan")
    if N:   # khung video ngắn mới: chỉ đưa lời đọc + chữ trên màn hình (không đưa đường dẫn ảnh)
        lines = [f"CHỮ HOOK TRÊN MÀN HÌNH: {plain(N.get('hook_text', ''))}"]
        for i, b in enumerate(N.get("beats", []), 1):
            the = b.get("the") if isinstance(b.get("the"), dict) else {}
            chu = " · ".join(plain(str(v)) for k, v in the.items() if k != "type" and v and not isinstance(v, list))
            chu += "".join(f" · {plain(x)}" for x in the.get("bullets", []))
            lines.append(f"Cảnh {i} [{b.get('loai_canh', '')}] lời đọc: {plain(b.get('text', ''))}"
                         + (f" | thẻ chữ trên màn hình: {chu}" if chu else ""))
        lines += [f"Ảnh bìa {i}: " + " · ".join(plain(c.get(k, "")).replace("\n", " ") for k in ("nhan", "to", "nho") if c.get(k))
                  for i, c in enumerate(N.get("anh_bia", []), 1)]
        scenes_txt = "\n".join(lines)
    else:
        scenes_txt = short_scene_list(script, None)
    out = [f"TIÊU ĐỀ: {script.get('title', '')}", f"CAPTION: {(N or {}).get('caption') or script.get('caption', '')}",
           "CÁC CẢNH VIDEO NGẮN:", scenes_txt]
    if p:
        out += ["BÀI VIẾT FACEBOOK:", p.get("hook", "")] + p.get("paragraphs", []) + [p.get("ending", "")]
        out += ["CHỮ TRÊN CÁC ẢNH BÀI ĐĂNG:"] + [
            f"Ảnh {i + 1}: " + " · ".join(plain(s.get(k, "")) for k in ("kicker", "tag", "title", "text") if s.get(k))
            for i, s in enumerate(p.get("slides", []))]
    return "\n".join(out)


def long_texts(script):
    L = script["long"]
    return "\n".join([f"TIÊU ĐỀ YOUTUBE: {L.get('title', '')}", f"TIÊU ĐỀ TRÊN MÀN HÌNH: {plain(L.get('title_card', ''))}",
                      f"MÔ TẢ: {L.get('description', '')}", "LỜI KỂ VIDEO DÀI:", long_beat_list(script)])


# ================================================================== 2. kịch bản
def content_check(script, part, dump):
    sid = script["id"]
    mine = short_texts(script) if part == "ngan" else long_texts(script)
    other = ""
    if part == "ngan" and script.get("long"):
        other = long_texts(script)[:6000]
    elif part == "dai":
        other = short_texts(script)[:4000]
    pron = script.get("pronounce") or {}
    prompt = f"""Bạn là biên tập viên kiểm tra nội dung cho kênh kể chuyện lịch sử có thật "Người Gác Sử" (khán giả Việt Nam 18–45 tuổi).
Hãy kiểm tra PHẦN CẦN KIỂM TRA bên dưới ({PART_NAME[part]} của chuyện {sid}). Chỉ báo vấn đề nằm trong phần này.

ĐIỀU CẦN SOI:
{checklist("Nội dung")}
- Nếu bạn biết chắc một chi tiết lịch sử sai (theo hiểu biết phổ biến của giới sử học), báo "loi".
  Nếu chỉ nghi ngờ, báo "canh_bao" và nói rõ cần kiểm tra lại điều gì.

GHI CHÚ TỪ KẾ HOẠCH (chuẩn để đối chiếu):
{plan_notes(sid) or "(không có)"}

NGUỒN ĐÃ DÙNG: {"; ".join(script.get("sources", []))}
{("CÁCH ĐỌC TÊN RIÊNG (để giọng AI đọc đúng): " + json.dumps(pron, ensure_ascii=False)) if pron else ""}

===== PHẦN CẦN KIỂM TRA =====
{mine}

===== PHẦN CÒN LẠI CỦA CÙNG CHUYỆN (chỉ để đối chiếu số liệu, không báo lỗi phần này) =====
{other or "(không có)"}
{ANSWER_FORMAT}"""
    return ask([{"text": prompt}], f"noidung_{sid}_{part}", dump)


# ================================================================== 3. xem + nghe cả video
def video_check(script, part, mp4, work_small, dump, timeline=None, long_data=None):
    sid = script["id"]
    kind_txt = "video dọc ngắn (Reels/TikTok/Shorts)" if part == "ngan" else "video dài 16:9 cho YouTube"
    if part == "ngan":
        expected = short_scene_list(script, timeline)
    else:
        expected = long_beat_list(script, long_data)
    pron = script.get("pronounce") or {}
    prompt = f"""Bạn là người kiểm duyệt video trước khi đăng cho kênh kể chuyện lịch sử "Người Gác Sử".
Video đính kèm là {kind_txt} của chuyện {sid}, giọng đọc AI tiếng Việt (giọng Bắc), hình là ảnh tư liệu và tranh minh họa AI.
Hãy XEM và NGHE toàn bộ video, đối chiếu với kịch bản bên dưới.

GIỌNG ĐỌC — điều cần soi:
{checklist("Giọng đọc")}
- Nghe từng câu và so với "Lời đọc" trong kịch bản. Báo chính xác thời điểm (mm:ss), câu đúng là gì, nghe thành gì.
{("- Tên riêng được cố ý viết lại cho giọng AI đọc theo bảng: " + json.dumps(pron, ensure_ascii=False) + " — đọc theo cách đó là đúng.") if pron else ""}

HÌNH ẢNH — điều cần soi:
{checklist("Hình ảnh")}
- Ảnh đổi quá sớm hoặc quá muộn so với lời đọc (lời đã sang ý khác mà hình vẫn là ý cũ) cũng là lỗi.

KỊCH BẢN (thời gian trong ngoặc là dự kiến, có thể lệch vài giây):
{expected}
{ANSWER_FORMAT}"""
    if DRY:
        return ask([{"text": prompt}, {"text": f"(video {mp4.name})"}], f"video_{sid}_{part}", dump)
    # Lời kể không đổi so với lần đã xem video trước -> không gửi lại cả video (khoản tốn nhất của bước kiểm tra).
    # Ảnh vẫn được soi từng khung ở bước sau; lỗi giọng đọc của lần trước (nếu có) được nhắc lại.
    nk = narration_key(script, part)
    state = CACHE / f"video_ok_{sid}_{part}.json"
    if not VIDEO_ALWAYS and state.exists():
        try:
            prev = json.loads(state.read_text(encoding="utf-8"))
        except Exception:
            prev = {}
        if prev.get("nk") == nk:
            voice_rx = re.compile(r"đọc|giọng|nghe|phát âm|lời|câu", re.I)
            carry = [dict(v, mo_ta="(từ lần kiểm tra trước) " + str(v.get("mo_ta", "")))
                     for v in (prev.get("result") or {}).get("van_de", []) if isinstance(v, dict)
                     and voice_rx.search(str(v.get("mo_ta", "")))]
            log("     ⏭️  lời kể không đổi so với lần trước: không gửi lại cả video (tiết kiệm chi phí)")
            return {"van_de": carry, "tom_tat": "lời kể không đổi nên không xem lại cả video; hình ảnh vẫn được soi từng khung."}
    res = _video_check_upload(script, part, mp4, work_small, dump, prompt)
    CACHE.mkdir(parents=True, exist_ok=True)
    state.write_text(json.dumps({"nk": nk, "result": res}, ensure_ascii=False), encoding="utf-8")
    return res


def narration_key(script, part):
    """Mã nhận diện lời kể + giọng: đổi chữ, đổi cách đọc tên hay đổi giọng thì mới phải nghe lại."""
    try:
        cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    except Exception:
        cfg = {}
    if part == "ngan":
        texts = "\n".join(str(sc.get("voice", "")) for sc in script.get("scenes", []))
    else:
        texts = "\n".join(str(b.get("text", "")) for ch in (script.get("long") or {}).get("chapters", [])
                          for b in ch.get("beats", []))
    voice = {k: cfg.get(k) for k in ("tts_engine", "gemini_voice", "vieneu", "voice", "voice_rate", "long")}
    if part == "dai":
        voice["long_voice"] = (script.get("long") or {}).get("voice")
    raw = json.dumps([texts, script.get("pronounce"), voice], ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:20]


def _video_check_upload(script, part, mp4, work_small, dump, prompt):
    sid = script["id"]
    small = small_copy(mp4, work_small, part)
    st = small.stat()
    ck = f"{small.name}:{st.st_size}:{hashlib.sha1(small.read_bytes()[:2_000_000]).hexdigest()}"
    cf_probe = CACHE / f"video_{sid}_{part}_{hashlib.sha1((prompt + '|' + ck).encode()).hexdigest()[:20]}.json"
    if cf_probe.exists():   # đã kiểm tra đúng video này rồi: không tải lên lại
        return json.loads(cf_probe.read_text(encoding="utf-8"))
    log(f"     ⬆️  tải video lên Gemini ({st.st_size / 1e6:.1f} MB)")
    uri, name = upload_file(small, "video/mp4")
    try:
        return ask([{"file_data": {"mime_type": "video/mp4", "file_uri": uri}}, {"text": prompt}],
                   f"video_{sid}_{part}", dump, ck)
    finally:
        delete_file(name)


# ================================================================== 4. soi khung hình
def frame_points(script, part, mp4, timeline, long_data):
    """[(thời điểm, mô tả lời đọc lúc đó)] — giữa mỗi cảnh/ảnh."""
    d = probe(mp4)["duration"]
    pts = []
    if part == "ngan":
        scenes = (timeline or {}).get("scenes") or []
        if scenes:
            for i, sc in enumerate(scenes):
                pts.append((sc["start"] + sc["dur"] * 0.8,
                            f"Cảnh {i + 1}. Lời đọc: {clean_voice(sc.get('voice'))} | Chữ trên hình: {scene_onscreen(sc)}"))
        else:
            sc_all = script.get("scenes", [])
            n = max(1, len(sc_all))
            for i, sc in enumerate(sc_all):   # không có dòng thời gian: chia đều
                pts.append((d * (i + 0.8) / n, f"Khoảng cảnh {i + 1}. Lời đọc: {clean_voice(sc.get('voice'))}"))
    else:
        shots = (long_data or {}).get("shots") or []
        spoken = (long_data or {}).get("spoken") or []
        if shots:
            for s in shots:
                mid = s["start"] + min(s["dur"] * 0.5, 6)
                txt = " ".join(x["text"] for x in spoken if x["start"] < s["start"] + s["dur"] and x["speech_end"] > s["start"])
                pts.append((mid, f"Lời đọc trong lúc ảnh này hiện: {plain(txt)[:400]}"))
        else:
            cues = read_srt(mp4.parent / f"{script['id']}_dai_vi.srt")
            t = 8.0
            while t < d - 5:
                txt = " ".join(c[2] for c in cues if c[0] < t + 8 and c[1] > t - 8)
                pts.append((t, f"Lời đọc quanh thời điểm này: {txt[:300] or '(không rõ)'}"))
                t += 20
    return pts


def read_srt(path):
    if not path.exists():
        return []
    cues = []
    for blk in re.split(r"\n\s*\n", path.read_text(encoding="utf-8")):
        m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+) --> (\d+):(\d+):(\d+)[,.](\d+)\s*\n(.*)", blk, re.S)
        if m:
            g = [int(x) for x in m.groups()[:8]]
            cues.append((g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000,
                         " ".join(m.group(9).split())))
    return cues


def frames_check(script, part, mp4, frames_dir, dump, timeline=None, long_data=None):
    sid = script["id"]
    pts = frame_points(script, part, mp4, timeline, long_data)
    frames_dir.mkdir(parents=True, exist_ok=True)
    width = 720 if part == "ngan" else 1280
    items = []
    for k, (t, desc) in enumerate(pts):
        f = frames_dir / f"{part}_{k + 1:03d}.jpg"
        if extract_frame(mp4, t, f, width):
            items.append((k + 1, t, desc, f))
    result = {"van_de": [], "tom_tat": []}
    for b in range(0, len(items), FRAMES_PER_CALL):
        batch = items[b:b + FRAMES_PER_CALL]
        parts = [{"text": f"""Bạn kiểm tra chất lượng hình ảnh cho video kể chuyện lịch sử "Người Gác Sử" (chuyện {sid}, {PART_NAME[part]}).
Dưới đây là {len(batch)} khung hình chụp từ video thành phẩm, mỗi khung kèm lời đọc lúc đó.
Ảnh là ảnh tư liệu cũ, hoặc ảnh mô phỏng do AI tạo, hoặc tranh vẽ. Chữ, nhãn và khung trang trí là của kênh.
Chữ trên hình hiện dần theo hiệu ứng, nên khung chụp có thể chưa đủ hết chữ: đừng báo thiếu chữ, chỉ báo chữ sai/tràn/che.
Ảnh tư liệu cũ có thể mờ, ngả màu: đó là bình thường, không phải lỗi.

ĐIỀU CẦN SOI:
{checklist("Hình ảnh")}
Với mỗi khung, "vi_tri" ghi đúng dạng "khung <số> (<mm:ss>)".
{ANSWER_FORMAT}"""}]
        for n, t, desc, f in batch:
            parts += [{"text": f"--- Khung {n} ({fmt_t(t)}) — {desc}"}, img_part(f)]
        ck = "|".join(hashlib.sha1(f.read_bytes()).hexdigest()[:12] for *_, f in batch)
        r = ask(parts, f"khung_{sid}_{part}_{b // FRAMES_PER_CALL + 1}", dump, ck)
        result["van_de"] += r.get("van_de", [])
        if r.get("tom_tat"):
            result["tom_tat"].append(r["tom_tat"])
    result["tom_tat"] = " ".join(result["tom_tat"])
    result["so_khung"] = len(items)
    return result


# ================================================================== 5. bài ảnh
def post_check(script, out_dir, dump):
    sid = script["id"]
    imgs = sorted(out_dir.glob(f"{sid}_post_*.jpg"), key=lambda p: int(re.findall(r"_(\d+)\.jpg$", p.name)[0]))
    if not imgs:
        return None
    post_txt = (out_dir / f"{sid}_post.txt")
    parts = [{"text": f"""Bạn kiểm tra một bài đăng Facebook dạng album ảnh của kênh kể chuyện lịch sử "Người Gác Sử" (chuyện {sid}).
Album có {len(imgs)} ảnh dọc theo thứ tự, kèm bài viết bên dưới.

ĐIỀU CẦN SOI:
{checklist("Bài ảnh")}
{checklist("Hình ảnh")}
- Bài viết: chính tả tiếng Việt, câu cụt, số liệu khớp với chữ trên ảnh.

BÀI VIẾT:
{post_txt.read_text(encoding="utf-8") if post_txt.exists() else short_texts(script)}
"vi_tri" ghi dạng "ảnh bài đăng <số>" hoặc "bài viết".
{ANSWER_FORMAT}"""}]
    small = []
    for i, f in enumerate(imgs):
        s = out_dir / "_review" / f"post_{i + 1}.jpg"
        s.parent.mkdir(parents=True, exist_ok=True)
        run_ffmpeg(["-y", "-i", str(f), "-vf", "scale=720:-2", "-q:v", "3", str(s)], timeout=60)
        small.append(s if s.exists() else f)
        parts += [{"text": f"--- Ảnh bài đăng {i + 1}"}, img_part(small[-1])]
    ck = "|".join(hashlib.sha1(f.read_bytes()).hexdigest()[:12] for f in small)
    return ask(parts, f"baianh_{sid}", dump, ck)


# ================================================================== 6. đồng bộ (video dài)
def sync_check(long_data):
    """Đoạn có tốc độ đọc bất thường = máy cắt giọng theo khoảng lặng bị lệch -> ảnh đổi sai chỗ."""
    out = []
    spoken = [s for s in (long_data or {}).get("spoken", []) if s.get("text")]
    rates = []
    for i, s in enumerate(spoken):
        dur = s["speech_end"] - s["start"]
        n = len(clean_voice(s["text"]))
        rates.append((i, s, dur, n / dur if dur > 0.2 else 999))
    if len(rates) < 5:
        return out
    med = sorted(r for *_, r in rates)[len(rates) // 2]
    for i, s, dur, r in rates:
        if dur < 0.8 or r > med * 1.7:
            out.append(issue("canh_bao", "Đồng bộ", f"Video dài {fmt_t(s['start'])} (đoạn {i + 1})",
                             f"đoạn này chỉ dài {dur:.1f} giây cho {len(s['text'])} ký tự lời kể (đọc nhanh bất thường) — "
                             "giọng có thể bị cắt sai chỗ, ảnh đổi lệch lời", "xem đoạn này; nếu lệch thì tách câu dài thành 2 đoạn"))
        elif r < med * 0.5 and dur > 4:
            out.append(issue("canh_bao", "Đồng bộ", f"Video dài {fmt_t(s['start'])} (đoạn {i + 1})",
                             f"đoạn này dài {dur:.1f} giây cho {len(s['text'])} ký tự (chậm bất thường) — "
                             "có thể có khoảng lặng lạ hoặc ảnh giữ quá lâu", "nghe lại đoạn này"))
    return out


# ================================================================== tổng hợp
MAX_LAP_ANH = 2


def _anh_key(im):
    if not isinstance(im, dict):
        return None
    if im.get("url"):
        return (im["url"].split("?")[0], json.dumps(im.get("crop")))
    if im.get("mo_phong"):
        return ("ai", im["mo_phong"])
    if im.get("anh_file"):
        return ("anh_file", im["anh_file"])
    return None


def lint_anh_lap(script, part):
    """Một ảnh không được xuất hiện quá MAX_LAP_ANH lần trong cùng một video (ngắn hoặc dài)."""
    items = []
    if part == "ngan":
        for b in (script.get("ngan") or {}).get("beats", []):
            ims = list(b.get("images") or [])
            if b.get("image"):
                ims.append(b["image"])
            if b.get("mo_phong"):
                ims.append({"mo_phong": b["mo_phong"]})
            items += ims
        if not items:
            items = [s.get("image") for s in script.get("scenes", [])]
    else:
        for ch in (script.get("long") or {}).get("chapters", []):
            for b in ch.get("beats", []):
                items.append(b.get("image") or ({"mo_phong": b["mo_phong"]} if b.get("mo_phong") else None)
                             or ({"anh_file": b["anh_file"]} if b.get("anh_file") else None))
    cnt = {}
    for im in items:
        k = _anh_key(im)
        if k:
            cnt.setdefault(k, [im, 0])[1] += 1
    out = []
    for k, (im, n) in cnt.items():
        if n > MAX_LAP_ANH:
            name = (im.get("credit") or im.get("mo_phong") or k[0])[:70]
            out.append(issue("loi", "Kịch bản", "ảnh lặp", f"ảnh dùng {n} lần (tối đa {MAX_LAP_ANH}): {name}",
                             "thay bằng ảnh khác cho các đoạn còn lại"))
    return out


def lint_script(script, part):
    """Kiểm tra nhanh bằng luật, không cần AI."""
    out, g = lint_anh_lap(script, part), "Kịch bản"
    if part == "ngan":
        scenes = script.get("scenes", [])
        for i, sc in enumerate(scenes):
            v = sc.get("voice", "")
            if not clean_voice(v):
                out.append(issue("loi", g, f"cảnh {i + 1}", "cảnh không có lời đọc"))
            if re.search(r"\d", clean_voice(v)):
                out.append(issue("canh_bao", g, f"cảnh {i + 1}", f"lời đọc có chữ số: \"{clean_voice(v)[:80]}\"",
                                 "viết số bằng chữ để giọng AI đọc đúng"))
        last = clean_voice(scenes[-1].get("voice")) if scenes else ""
        if "lạ hơn cả truyện" not in last:
            out.append(issue("canh_bao", g, "cảnh cuối", "lời kết thiếu câu \"Sử thật… lạ hơn cả truyện\""))
    else:
        k = 0
        for ch in script["long"]["chapters"]:
            for b in ch["beats"]:
                k += 1
                if re.search(r"\d", plain(b.get("text"))):
                    out.append(issue("canh_bao", g, f"video dài đoạn {k}", f"lời kể có chữ số: \"{plain(b['text'])[:80]}\"",
                                     "viết số bằng chữ để giọng đọc đúng"))
                if len(plain(b.get("text"))) > 420:
                    out.append(issue("canh_bao", g, f"video dài đoạn {k}", "đoạn quá dài (dễ lệch ảnh)", "tách thành 2 đoạn"))
    return out


def chi_phi_id(sid):
    """Ghi chi phí của các lần gọi Gemini tiếp theo cho mã này."""
    try:
        import chi_phi
        chi_phi.CURRENT = sid
    except Exception:
        pass


def precheck(sid, parts):
    """Kiểm tra kịch bản TRƯỚC khi dựng (chỉ đọc chữ: rẻ, có lưu đệm -> kịch bản không đổi thì không tốn thêm).
    Trả về danh sách vấn đề mức "loi". Có lỗi thì ci_render không dựng, đỡ tốn tiền giọng đọc / vẽ tranh / kiểm tra video."""
    global STAGE
    script = json.loads((ROOT / "scripts" / f"{sid}.json").read_text(encoding="utf-8"))
    rdir = ROOT / "output" / sid / "_review"
    rdir.mkdir(parents=True, exist_ok=True)
    found = []
    use_ai = __import__("gemini_keys").has_key() and not DRY
    for part in parts:
        if part == "dai" and not script.get("long"):
            continue
        found += [x for x in lint_script(script, part) if x["muc"] == "loi"]
        if not use_ai:
            continue
        STAGE = "precheck"
        try:
            res = content_check(script, part, rdir)
            found += [x for x in ai_issues(res, "Nội dung kịch bản") if x["muc"] == "loi"]
        except Exception as e:
            log(f"   (chưa kiểm tra được kịch bản {sid}:{part} trước khi dựng: {str(e)[:160]}, vẫn dựng tiếp)")
        finally:
            STAGE = "review"
    return found


def ai_issues(res, group, default_where=""):
    out = []
    for v in (res or {}).get("van_de", []) or []:
        if not isinstance(v, dict):
            continue
        lvl = "loi" if str(v.get("muc", "")).lower().startswith("loi") or "lỗi" in str(v.get("muc", "")).lower() else "canh_bao"
        out.append(issue(lvl, group, str(v.get("vi_tri") or default_where), str(v.get("mo_ta", "")).strip(),
                         str(v.get("sua", "")).strip()))
    return [x for x in out if x["mo_ta"]]


def review_part(sid, part, use_ai=True):
    script_path = ROOT / "scripts" / f"{sid}.json"
    script = json.loads(script_path.read_text(encoding="utf-8"))
    out_dir = ROOT / "output" / sid
    rdir = out_dir / "_review"
    rdir.mkdir(parents=True, exist_ok=True)
    issues, notes = [], []
    if part == "ngan":
        mp4, work = out_dir / f"{sid}.mp4", out_dir / "_work"
        tl = json.loads((work / "timeline.json").read_text(encoding="utf-8")) if (work / "timeline.json").exists() else None
        ld = None
        narration = work / "narration.wav"
        quiet = ()
    else:
        mp4, work = out_dir / f"{sid}_dai.mp4", out_dir / "_work_dai"
        tl = None
        ld = json.loads((work / "review_data.json").read_text(encoding="utf-8")) if (work / "review_data.json").exists() else None
        narration = work / "narration.wav"
        quiet = []
        for c in sorted((ld or {}).get("cards", []), key=lambda c: c["start"]):
            a, b = c["start"], c["start"] + c["dur"]
            if quiet and a - quiet[-1][1] < 2.5:   # hai thẻ liền nhau (thẻ tên phim + thẻ Phần 1)
                quiet[-1] = (quiet[-1][0], b)
            else:
                quiet.append((a, b))
    if not mp4.exists():
        return None
    chi_phi_id(sid)
    log(f"🔎 Kiểm tra {sid} – {PART_NAME[part]}")

    log("   • kỹ thuật")
    issues += tech_check(mp4, part, narration if narration.exists() else None, quiet)
    issues += lint_script(script, part)
    if part == "dai":
        issues += sync_check(ld)

    if use_ai:
        steps = [("Nội dung kịch bản", lambda: content_check(script, part, rdir))]
        steps.append(("Xem và nghe video", lambda: video_check(script, part, mp4, rdir / f"small_{part}.mp4", rdir, tl, ld)))
        steps.append(("Soi khung hình", lambda: frames_check(script, part, mp4, rdir / "frames", rdir, tl, ld)))
        if part == "ngan":
            steps.append(("Bài ảnh", lambda: post_check(script, out_dir, rdir)))
        for name, fn in steps:
            log(f"   • {name.lower()}")
            try:
                res = fn()
            except Exception as e:
                issues.append(issue("canh_bao", "Hệ thống", name, f"chưa kiểm tra được: {str(e)[:200]}",
                                    "chạy lại kiểm tra hoặc xem tay phần này"))
                continue
            if res is None:
                continue
            issues += ai_issues(res, name)
            if res.get("tom_tat"):
                notes.append(f"{name}: {res['tom_tat']}")

    n_loi = sum(1 for x in issues if x["muc"] == "loi")
    n_cb = sum(1 for x in issues if x["muc"] == "canh_bao")
    verdict = "loi" if n_loi else ("xem" if n_cb else "dat")
    report = {"id": sid, "phan": part, "ket_qua": verdict, "so_loi": n_loi, "so_canh_bao": n_cb,
              "thoi_gian": time.strftime("%Y-%m-%d %H:%M"), "ai": use_ai and not DRY, "nhan_xet": notes,
              "van_de": sorted(issues, key=lambda x: (x["muc"] != "loi", x["nhom"]))}
    (out_dir / f"{sid}_kiemtra_{part}.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    txt = summary_text(report)
    (out_dir / f"{sid}_kiemtra_{part}.txt").write_text(txt, encoding="utf-8")
    logs = ROOT / "logs"
    logs.mkdir(exist_ok=True)
    (logs / f"kiemtra_{sid}_{part}.txt").write_text(txt, encoding="utf-8")
    log(f"   → {VERDICT_TEXT[verdict]} ({n_loi} lỗi, {n_cb} cảnh báo)")
    return report


def summary_text(r, limit=None):
    head = f"🔎 KIỂM TRA {r['id']} · {PART_NAME[r['phan']]}\n{VERDICT_TEXT[r['ket_qua']]} — {r['so_loi']} lỗi, {r['so_canh_bao']} cảnh báo"
    if not r["ai"]:
        head += "\n(chỉ kiểm tra kỹ thuật, chưa có bước AI)"
    lines = [head, ""]
    for v in r["van_de"]:
        icon = "❌" if v["muc"] == "loi" else "⚠️"
        line = f"{icon} [{v['nhom']} · {v['vi_tri']}] {v['mo_ta']}"
        if v.get("sua"):
            line += f"\n   → Sửa: {v['sua']}"
        lines.append(line)
    if not r["van_de"]:
        lines.append("Không phát hiện vấn đề nào.")
    if r.get("nhan_xet"):
        lines += ["", "Nhận xét:"] + [f"• {n}" for n in r["nhan_xet"]]
    txt = "\n".join(lines) + "\n"
    if limit and len(txt) > limit:
        txt = txt[:limit - 60].rsplit("\n", 1)[0] + "\n… (còn nữa, xem file kiemtra đầy đủ)\n"
    return txt


def _cost(sid):
    try:
        import chi_phi
        return chi_phi.summary(sid)
    except Exception:
        return ""


def send_telegram(reports, blocked=None):
    token, chat = os.environ.get("TG_TOKEN", "").strip(), os.environ.get("TG_CHAT", "").strip()
    if not chat and (ROOT / "telegram_chat_id.txt").exists():
        chat = (ROOT / "telegram_chat_id.txt").read_text().strip()
    if not token or not chat:
        log("Chưa có TG_TOKEN / TG_CHAT, không gửi báo cáo Telegram.")
        return
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    msgs = []
    for f in ("ci_long_failed.txt", "ci_failed.txt"):   # dừng vì ảnh không đạt kiểm tra -> gửi danh sách ảnh lỗi
        fp = ROOT / f
        if not fp.exists():
            continue
        part = "dai" if "long" in f else "ngan"
        for sid in [x.strip() for x in fp.read_text(encoding="utf-8").splitlines() if x.strip()]:
            rep = ROOT / "logs" / f"anh_{sid}_{part}_kiemtra.txt"
            if rep.exists() and ("❌" in rep.read_text(encoding="utf-8")):
                bad = [ln for ln in rep.read_text(encoding="utf-8").splitlines() if "❌" in ln or ln.startswith("KIỂM TRA")]
                msgs.append(("⛔ CHƯA DỰNG " + sid + f" ({PART_NAME[part]}): có ảnh không đạt kiểm tra\n" + "\n".join(bad))[:3600]
                            + "\nĐổi ảnh trong kịch bản, hoặc chạy lại với ô 'Bỏ qua kiểm tra' = yes.")
    for sid, errs in (blocked or {}).items():
        lines = [f"⛔ CHƯA DỰNG {sid}: kịch bản có lỗi (đã kiểm tra trước khi dựng để khỏi tốn tiền)"]
        lines += [f"❌ [{x['vi_tri']}] {x['mo_ta']}" + (f"\n   → Sửa: {x['sua']}" if x.get("sua") else "") for x in errs]
        lines.append("Sửa kịch bản rồi đẩy lại, hoặc chạy workflow với ô 'Bỏ qua kiểm tra' = yes nếu bạn thấy không phải lỗi.")
        c = _cost(sid)
        msgs.append("\n".join(lines)[:3600] + (f"\n\n{c}" if c else ""))
    sent_cost = set()
    for r in reports:
        txt = summary_text(r, limit=3500)
        if r["id"] not in sent_cost:   # chi phí của cả mã, gửi kèm báo cáo đầu tiên của mã đó
            c = _cost(r["id"])
            if c:
                txt += f"\n{c}\n"
            sent_cost.add(r["id"])
        if repo:
            txt += f"\nVideo: https://github.com/{repo}/releases/tag/video-{r['id']}{os.environ.get('HAU_TO', '').strip()}"
        msgs.append(txt)
    for txt in msgs:
        data = urllib.parse.urlencode({"chat_id": chat, "text": txt, "disable_web_page_preview": "true"}).encode()
        try:
            urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=data, timeout=30).read()
        except Exception as e:
            log(f"Không gửi được báo cáo Telegram: {e}")


def main():
    args = sys.argv[1:]
    use_ai = "--no-ai" not in args
    targets = []
    if "--ci" in args:
        for fname, part in (("ci_outputs.txt", "ngan"), ("ci_long.txt", "dai")):
            f = ROOT / fname
            if f.exists():
                targets += [(x.strip(), part) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]
    for a in args:
        if a.startswith("--"):
            continue
        sid, _, part = a.partition(":")
        targets += [(sid, p) for p in (["ngan", "dai"] if part in ("", "all") else [part])]
    if not targets:
        print(__doc__)
        return
    if use_ai and not DRY and not __import__("gemini_keys").has_key():
        log("⚠️  Chưa có GEMINI_API_KEY: chỉ kiểm tra kỹ thuật.")
        use_ai = False
    reports = []
    for sid, part in dict.fromkeys(targets):
        try:
            r = review_part(sid, part, use_ai)
        except Exception as e:
            log(f"❌ Không kiểm tra được {sid}:{part}: {e}")
            continue
        if r:
            reports.append(r)
    blocked = {}
    if "--ci" in args and (ROOT / "ci_blocked.json").exists():
        try:
            blocked = json.loads((ROOT / "ci_blocked.json").read_text(encoding="utf-8"))
        except Exception:
            blocked = {}
    failed_any = any((ROOT / f).exists() and (ROOT / f).read_text(encoding="utf-8").strip()
                     for f in ("ci_long_failed.txt", "ci_failed.txt")) if "--ci" in args else False
    if "--telegram" in args and (reports or blocked or failed_any):
        send_telegram(reports, blocked)
    # chi phí ước tính: in ra log và lưu logs/chiphi_<mã>.txt
    try:
        import chi_phi
        for sid in dict.fromkeys([r["id"] for r in reports] + list(blocked)):
            c = chi_phi.summary(sid)
            if c:
                (ROOT / "logs").mkdir(exist_ok=True)
                (ROOT / "logs" / f"chiphi_{sid}.txt").write_text(c + "\n", encoding="utf-8")
        tot = chi_phi.summary()
        if tot:
            log(tot)
    except Exception:
        pass
    worst = max((["dat", "xem", "loi"].index(r["ket_qua"]) for r in reports), default=0)
    if "--strict" in args and worst == 2:
        sys.exit(2)


if __name__ == "__main__":
    main()
