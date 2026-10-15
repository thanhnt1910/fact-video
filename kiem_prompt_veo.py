"""
KIỂM PROMPT VEO: prompt (và tiền tố) gửi Google Flow / Veo không được nêu tên riêng của người thật nổi tiếng
(nhân vật lịch sử), vì vi phạm chính sách và clip bị từ chối. Ảnh khung đầu đã mang sẵn khuôn mặt, prompt chỉ cần mô tả chung.

  python kiem_prompt_veo.py ke-hoach/tam-quoc-tap-3-anh-va-veo.md [file khác ...]

Kiểm: (1) tiền tố trong dấu `…` bắt đầu bằng "Animate this"; (2) cột prompt chuyển động của các bảng Veo (cột cuối);
(3) mọi chữ viết hoa giữa câu trong các prompt đó; (4) danh sách tên đã biết (Liu Bei, Sun Jian, Lưu Bị, Tôn Kiên…).
Thoát mã 1 nếu có tên. Chỉ quét phần Veo (từ tiêu đề "Veo" / "Nhóm A" đến "Nhóm B"), không quét bảng "Cảnh" tham khảo.
"""
import re
import sys
from pathlib import Path

TEN = """liu bei,liu bi,guan yu,zhang fei,cao cao,sun jian,sun ce,sun quan,lu bu,dong zhuo,yuan shao,yuan shu,zhuge,zhou yu,gongsun,
han fu,hu zhen,wang yun,ding yuan,zu mao,hua xiong,liu yu,li su,huang zu,liu biao,xiahou,sima,diaochan,lưu bị,quan vũ,trương phi,tào tháo,
tôn kiên,tôn sách,tôn quyền,lữ bố,đổng trác,viên thiệu,viên thuật,gia cát,chu du,công tôn,hàn phức,hồ chẩn,vương doãn,đinh nguyên,
tổ mậu,hoa hùng,lưu ngu,hoàng tổ,lưu biểu,tư mã,điêu thuyền""".replace("\n", "").split(",")
BO_QUA = {"Animate", "Keep", "Han", "Motion", "Slow", "Very", "Static", "No", "Same", "Dust"}   # chữ viết hoa hợp lệ (đầu câu, tên triều đại)


def phan_veo(text):
    """Các dòng prompt Veo: tiền tố trong `…` và ô cuối của hàng bảng thuộc phần Veo."""
    out = []
    in_veo = False
    for l in text.split("\n"):
        if l.startswith("## "):
            in_veo = ("Veo" in l) or ("Nhóm A" in l)
        if not in_veo:
            continue
        for m in re.finditer(r"`(Animate[^`]*)`", l):
            out.append(m.group(1))
        if l.startswith("|") and not re.match(r"^\|[-| ]+\|$", l):
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if len(cells) >= 3 and re.match(r"^\d{3}$", cells[0]):
                out.append(cells[-1])
    return out


def main():
    files = sys.argv[1:] or ["ke-hoach/tam-quoc-tap-3-anh-va-veo.md"]
    bad = 0
    for f in files:
        prompts = phan_veo(Path(f).read_text(encoding="utf-8"))
        for p in prompts:
            low = p.lower()
            ten = [t for t in TEN if t in low]
            caps = [w for w in re.findall(r"(?<![.!?] )(?<!^)\b[A-Z][a-z]{2,}\b", p) if w not in BO_QUA]
            if ten or caps:
                bad += 1
                print(f"{f}: tên riêng trong prompt Veo: {sorted(set(ten + caps))} ← {p[:90]}")
        print(f"{f}: đã quét {len(prompts)} prompt Veo")
    print("ĐẠT" if not bad else f"LỖI: {bad} prompt có tên riêng, phải sửa trước khi gửi Veo")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
