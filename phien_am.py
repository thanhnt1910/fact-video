"""
Kiểm tra cách giọng đọc VieNeu sẽ phát âm tên riêng / từ nước ngoài trong kịch bản.

  python phien_am.py scripts/SL1.json        (cần thư viện sea_g2p — có sẵn trong .venv-tts)

VieNeu v3 Turbo đọc được tiếng Anh xen tiếng Việt: từ nào không có trong từ điển tiếng Việt
sẽ được đọc theo kiểu tiếng Anh. Vì vậy:
  - GIỮ NGUYÊN tên nước ngoài (Strasbourg, Shackleton…) — máy tự đọc kiểu Anh.
  - Tên không phải tiếng Anh mà máy đọc lệch (Troffea, Koepcke…) thì thêm vào "pronounce"
    một cách viết KIỂU ANH gần đúng âm gốc, vd "Troffea": "Troffaya".
  - KHÔNG phiên âm kiểu Việt ("Xtrát bua") — máy sẽ đọc thành chữ Việt, nghe rất sai.
"""
import json
import re
import sys

from sea_g2p import SEAPipeline

# Ký hiệu chỉ có trong âm tiếng Anh (tiếng Việt dùng tʃ, əɪ, ɣ… nên bỏ qua các cụm đó)
EN_MARKS = ("ɪ", "ʊ", "æ", "ɑ", "ɚ", "θ", "ð", "ʒ", "ɾ", "ʌ", "ɜː", "ɡ", "ʃ")


def is_english(ph):
    core = ph.replace("tʃ", "").replace("əɪ", "")
    return any(m in core for m in EN_MARKS)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    script = json.load(open(sys.argv[1], encoding="utf-8"))
    pron = script.get("pronounce", {})
    p = SEAPipeline("vi")
    seen = {}
    for sc in script["scenes"]:
        text = re.sub(r"\[[^\]]*\]", " ", sc.get("voice", ""))
        for k, v in pron.items():
            text = text.replace(k, v)
        words = re.findall(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", text)
        for i, w in enumerate(words):
            if w in seen:
                continue
            ph = p.run(w).strip(" .")
            if not is_english(ph):
                continue
            # xét cả từ đứng cạnh: "máy bay", "bay sang" trong câu vẫn được đọc kiểu Việt
            a = max(0, i - 1)
            win = words[a:i + 2]
            toks = p.run(" ".join(win)).strip(" .").split()
            if len(toks) == len(win):
                ph = toks[i - a]
            if is_english(ph):
                seen[w] = ph
    back = {v: k for k, v in pron.items()}
    print("Từ đọc theo kiểu tiếng Anh / tên riêng:")
    for w, ph in seen.items():
        src = f"  (thay cho {back[w]})" if w in back else ""
        print(f"  {w:<20} /{ph}/{src}")


if __name__ == "__main__":
    main()
