#!/usr/bin/env python3
"""Kiểm câu cụt kiểu biên niên (chủ kênh nhắc 19/11/2026, tm12). Xem quy-tac/thuy-mac-giong-van.md mục 5.
Cách dùng: python phim_ban_do/kiem_cau_cut.py <mã>   (đọc ke-hoach/thu-giong-hai/<mã>_full.json)
❌ phải sửa trước khi gửi duyệt, không được ghi "chấp nhận".
 1. Chuỗi vế cụt: một câu có từ 3 vế liền nhau (ngăn bằng dấu phẩy) mà mỗi vế dưới 7 chữ.
 2. Vế trơ ở cuối câu: vế cuối 1–3 chữ chỉ là động từ kết quả (tan vỡ, thất thủ, thua liền...).
 3. Câu trơ: câu dưới 7 chữ, không phải câu hỏi, không có chữ nối, kết bằng động từ kết quả.
 4. Kết quả không có đối tượng: "thua liền", "thắng liền", "đánh mãi" đứng cuối vế mà không nói thua ai, ở đâu, mấy trận.
⚠️ Câu có hơn 4 dấu phẩy: nên tách hoặc nối bằng chữ chỉ quan hệ (vì, nên, rồi, nhưng, đến nỗi, khi)."""
import json, os, re, sys
TRO = ['tan vỡ','thất thủ','thua liền','thắng liền','bị đánh tan','đều vỡ','chết trận','tan chạy','bị chiếm','không kịp trở tay']
NOI = ['vì','nên','rồi','nhưng','khi','nếu','thì','mà','để','đến','cho tới','còn','vậy','thế','sau','trước','lúc']
def cau(t): return [s for s in re.split(r'(?<=[.?!])\s+', t.strip()) if s]
def main(ma):
    p = os.path.join(os.path.dirname(__file__), '..', 'ke-hoach', 'thu-giong-hai', f'{ma}_full.json')
    J = json.load(open(p, encoding='utf-8')); nl = nc = 0
    for d in J:
        for s in cau(d['text']):
            v = [x.strip() for x in re.split(r',', s.rstrip('.!?')) if x.strip()]
            run = mx = 0
            for x in v:
                run = run + 1 if len(x.split()) < 7 else 0; mx = max(mx, run)
            if mx >= 3: print(f'❌ {d["n"]}: chuỗi {mx} vế cụt nối bằng dấu phẩy: "{s[:90]}"'); nl += 1
            last = v[-1].lower() if v else ''
            if len(v) > 1 and len(last.split()) <= 3 and any(last.endswith(w) for w in TRO):
                print(f'❌ {d["n"]}: vế trơ cuối câu "{v[-1]}": nói rõ ai, vì sao, kết quả ra sao'); nl += 1
            w = s.split()
            if len(w) < 7 and not s.endswith('?') and any(s.lower().rstrip('.').endswith(t) for t in TRO) and not any(x.lower() in NOI for x in w):
                print(f'❌ {d["n"]}: câu trơ "{s}": thêm đối tượng, nơi chốn hoặc lý do'); nl += 1
            for t in ('thua liền','thắng liền','đánh mãi'):
                for x in v:
                    if x.lower().endswith(t): print(f'❌ {d["n"]}: "{t}" không nói thua/thắng ai, ở đâu: "{x}"'); nl += 1
            if s.count(',') > 4: print(f'⚠️ {d["n"]}: {s.count(",")} dấu phẩy trong một câu: "{s[:70]}"'); nc += 1
    print(f'-> {nl} ❌, {nc} ⚠️')
if __name__ == '__main__': main(sys.argv[1])
