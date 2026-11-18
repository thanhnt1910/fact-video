# Kiểm tra kỹ thuật video, giọng, workflow

> Chuyển nguyên văn từ CLAUDE.md, chờ gộp. Mục giọng gốc (06/11) là quy tắc giọng hiện hành. Nguồn: `archive/CLAUDE-truoc-tai-cau-truc-18-11.md`. Chuyển ngày 18/11/2026.

## Kiểm đường dẫn trong file quy tắc

Chạy `python tools/kiem_lien_ket.py` sau mỗi lần sửa hoặc chuyển file quy tắc; phải ĐẠT (mã 0). Công cụ quét mọi đường dẫn trong dấu huyền ở `CLAUDE.md`, `quy-tac/`, `mau-kich-ban/`, `PROMPT_KICH_BAN.md`, `review_checklist.md` và báo đường dẫn không tồn tại (bỏ qua `archive/`, mẫu có chữ N, sản phẩm tạm).


## Git và workflow (rút từ mục Tam Quốc cũ, còn hiệu lực với mọi series)

- Mọi commit dùng `user.email noreply@anthropic.com`, `user.name Claude`. Không đẩy lên `main` trừ khi chủ kênh yêu cầu.
- **Workflow chỉ chạy khi chủ kênh yêu cầu, và chỉ chạy đúng video được yêu cầu** (chủ kênh nhắc 21/10/2026). Không tự kích hoạt dựng, nhận dạng giọng hay vẽ ảnh.
- Workflow dựng và nhận dạng chạy khi có push đổi file kích hoạt. Push viết lại lịch sử làm GitHub coi mọi file là đã đổi nên chạy lại cả loạt: khi buộc phải viết lại lịch sử, commit cuối phải có `[skip ci]` trong tiêu đề.
- Commit tự động của workflow (`actions@users.noreply.github.com`) bị gắn "Unverified": đợi hết run rồi `git rebase --exec "git commit --amend --no-edit --reset-author -q" <SHA>^` và `git push --force-with-lease=<nhánh>:<SHA từ git ls-remote>`.
- Cảnh báo "commit chưa đẩy" của stop hook thường do tracking ref cũ: `git update-ref refs/remotes/origin/<nhánh> $(git ls-remote origin <nhánh> | cut -f1)` rồi đếm lại.
- Không chạy đồng thời hai workflow cùng đẩy lên một nhánh (giọng và nhận dạng); không chạy `dung_9x16.py` cho video khác khi đang dựng một video (dùng chung `data.js`).
- Cloudflare Workers AI (`cf-thuy-mac.yml`) dùng được cho ảnh thủy mặc; dừng ngay khi gặp HTTP 429. (Dòng "không dùng" trong mục Tam Quốc cũ chỉ đúng cho ảnh Tam Quốc.)


## Giọng đọc: dùng nguyên giọng gốc của Gemini, KHÔNG chỉnh sửa gì (chủ kênh yêu cầu 06/11/2026, thay mọi bước cân/chuẩn hóa giọng ở các mục trên, áp dụng mọi video từ nay)
Các bước chuẩn hóa trước đây (cân tốc độ `atempo`, cân cao độ và âm sắc `can_giong_am_sac.py`, `chuan_hoa_giong.py`, `loudnorm`, nén, EQ, làm to giọng) làm giọng khác đi, nghe lệch. Chủ kênh yêu cầu bỏ hết.
- **Không** áp dụng lên file giọng: `atempo`, `rubberband`, `asetrate`, `loudnorm`, `acompressor`, `equalizer`, `alimiter`, tăng giảm âm lượng, cắt lại theo mốc chữ rồi kéo giãn. Giọng trong video là đúng những byte Gemini trả về (chỉ ghép các đoạn kề nhau).
- Lượt đọc cả kịch bản một lần (`cum.txt` = 15, giọng Orus), lấy đúng từng đoạn workflow `thu-giong-hai.yml` cắt ra (`assets/thu_giong_hai/orus/<số>.mp3`) làm giọng của video. Dùng bản chép tay của giọng trong thư mục riêng `<tên>_goc/` (chỉ sao chép, kèm `thoi_luong.json` đo thời lượng thật), không đổi gì.
- Dựng bằng `python phim_ban_do/dung_9x16.py <tên> assets/thu_giong_hai/<tên>_goc <ra.mp4> --khong-to` (tắt chuỗi nén, EQ, loudnorm của giọng). Phần tiếng hiệu ứng vẫn tự hạ khi có giọng; không đụng giọng.
- Đoạn nào Gemini đọc sai chữ (nhận dạng lệch dưới 90%) thì đọc lại đoạn đó (tối đa 3 lần) và chọn bản đọc đúng nhất; không tìm cách "chữa" bằng xử lý âm thanh. Báo chủ kênh đoạn nào còn lệch thay vì tự chỉnh.
- Nhận dạng giọng (`phude_asr.py`, `kiem_giong.py`) chỉ để đo và tính phụ đề, không làm thay đổi file âm thanh.

## Kiểm năm trong giọng đọc bằng nhận dạng KHÔNG gợi ý (rút từ tn11, chủ kênh phát hiện 12/11/2026)
- Bản nhận dạng có gợi ý (`asr_<mã>.json`) chép theo kịch bản nên có thể ghi đúng năm dù giọng đọc sai (tn11 đọc "1958" mà bản có gợi ý vẫn ghi 1951). Năm, số, tên phải so bằng `asr_<mã>_ngoai.json` (không gợi ý) và bản nhận dạng cả cụm; lệch thì coi là đọc sai.
- Gemini hay đọc sai năm viết bằng chữ (tn11 1951 → 1956/1958, tn12 1010 → 2010, tn15 1909 → 1905). Khi đã sai một lượt: ghi năm đó bằng chữ số trong trường `text` (phụ đề `hien` giữ nguyên), đọc lại cả video, kiểm lại bằng bản không gợi ý.
- Không chạy đồng thời hai workflow cùng đẩy lên nhánh (giọng và nhận dạng): lượt giọng tn13 từng mất vì bị từ chối đẩy. Không chạy `dung_9x16.py` cho video khác khi đang dựng một video (dùng chung `data.js`).

## Kiểm video trước khi giao (công cụ `phim_ban_do/kiem_video.py`, chủ kênh yêu cầu 21/10/2026)

- Sau khi chốt giọng và dựng, chạy: `python phim_ban_do/kiem_video.py <tên> --tts <các file tts> --video <mp4>` (cần `asr_<tên>_final.json` mới, chạy `phude-asr.yml` SAU khi file giọng đã chốt; công cụ báo "nhận dạng CŨ" nếu lệch với file giọng).
- Công cụ kiểm: chữ thừa/mất/lặp ở đầu và cuối mỗi câu, năm đọc sai, từ hay sai (kỵ), phụ đề trễ/sớm/trống, ô năm góc trái so với lời kể, cảnh gắn vào câu quá dài, giọng trong video lệch khỏi cảnh, im lặng dài, hình đen/đứng, độ dài. Báo cáo: `logs/kiem_video/<tên>.md`. Có ❌ thì không giao video.

### Không để giọng đọc lặp câu (chủ kênh yêu cầu 22/10/2026, từ demo Hồng Môn yến bị lặp câu 6009 và 6023)

- Lỗi hay gặp: giọng đọc cụm nhiều câu một lần rồi cắt, nên **đuôi câu trước bị đọc lại ở đầu câu sau** (6009 mở đầu bằng "Hạng Vũ nghe theo" của câu 6008) hoặc **đầu câu sau lẫn vào cuối câu này** (6023). Người nghe thấy một câu bị nhắc hai lần.
- `kiem_video.py` kiểm các dạng lặp sau, tất cả là ❌ (không giao video): thừa chữ ở đầu hoặc cuối câu (tính theo khối khớp đầu/cuối, không bỏ sót khi chữ thừa dính chữ lệch); đầu câu đọc lại 3–6 chữ cuối câu trước; cuối câu đọc lẫn 3–6 chữ đầu câu sau; một vế của câu bị đọc từ hai lần; giọng nhiều hơn kịch bản từ 4 chữ; lặp cụm 2–3 chữ liền nhau.
- **Báo cáo 0 lỗi chưa đủ:** sau khi dựng, mở `logs/kiem_video/<tên>.md` và nghe lại ít nhất chỗ nối giữa các câu đã sửa; câu nào ASR dài hơn kịch bản thì nghe lại.
- Cách sửa giống mục bố cục: xóa các câu lỗi khỏi `thoi_luong.json` và mp3, `cum.txt` = `1`, đẩy `chay.txt` (chỉ khi chủ kênh cho chạy), chạy lại nhận dạng và `phude_tinh.py`, rồi kiểm lại đến khi sạch. Chỉ sửa giọng thì phải dựng lại video.

## Bài học tập 2 dựng lại (chủ kênh phê bình 07/11/2026): giọng lệch, câu lặp, hiệu ứng đơn giản, icon dưới biển, chữ chồng chữ. Áp dụng mọi video từ nay
Lỗi: tôi giao video khi mới xem 8 khung thu nhỏ, kiểm giọng chỉ bằng ngưỡng khớp 90%, và chưa chạy kiểm tự động nào cho video đã dựng. Không lặp lại.

**Giọng đọc**
- Đọc lại đoạn lỗi bằng `cum=1` làm giọng khác hẳn các đoạn đọc trong cụm 15 (nhịp, âm sắc). Khi phải đọc lại vài đoạn: đọc lại CẢ cụm kề (đoạn lỗi cùng các đoạn trước và sau, cùng `cum`), hoặc đọc lại cả video nếu còn hạn mức; không chèn đoạn đọc riêng vào video đọc theo cụm.
- Trước khi dựng bắt buộc in bảng chữ/giây từng đoạn: đoạn lệch quá 15% so với trung vị (tập 2: 49011 và 49022 khoảng 4,7, 49023 chỉ 2,6, trung vị khoảng 3,6) phải đọc lại, không chỉ chờ nhận dạng.
- Khớp 90% không đủ: ngưỡng cho qua cả "ập tục" (tập), "tuyền bá" (truyền bá), chữ thừa "ừ". Đoạn nào ASR có chữ lạ hoặc thiếu chữ so với kịch bản đều phải đọc lại, đặt ngưỡng 95% và so từng chữ.
- Lặp câu: ngoài kiểm đầu lặp đuôi câu trước, kiểm cụm 3–6 chữ lặp liền nhau trong cùng đoạn (đã gặp "Lẽ nào chưa ạ? Lẽ nào chưa ạ?" ở 49025 lượt đầu). Sau khi dựng nghe lại chỗ nối các đoạn đã đọc lại; nghi ngờ thì hỏi số đoạn, không tự cho là sạch.
- `kiem_video.py` phải chạy được cho video 9x16 (có `phude_<tên>.json`) và báo 0 ❌ trước khi giao; không chạy được thì nói thẳng "chưa kiểm tự động", không viết như đã kiểm.

**Bản đồ: icon, nhãn, quân**
- Mỗi điểm đặt trên bản đồ (thành, quân cờ, đồ vật, ruộng, tiền, cờ) phải nằm trên đất liền, kể cả điểm quân trong cặp, hàng, vòng tròn. Trước khi dựng chạy kiểm `sea(lon,lat)` cho TẤT CẢ điểm của từng cảnh, bao gồm bù (offset) và điểm giữa đường đi; cảnh nào có điểm biển thì sửa. Chủ kênh vẫn thấy icon dưới biển ở tập 2 (Nhật Nam, cặp người kết hôn, nhóm quân quanh Giao Chỉ).
- Không vật nào đè lên chữ khác: kiểm hộp bao của mọi nhãn và icon trong cùng một cảnh, không giao nhau, cách vùng phụ đề (y 1290–1500) và các dòng năm, nguồn, logo. Chữ trên cảnh không đè lên nhãn tên thành (đã thấy "Đền thờ khi còn sống" đè "Cửu Chân", nhãn "Nhâm Diên" đè "Cửu Chân", "Đặng Nhượng" sát "Giao Chỉ").
- Xem khung hình thật ở cỡ lớn (tối đa 3 khung một tấm) cho MỌI cảnh, mỗi cảnh ở đầu, giữa, lúc nhiều vật nhất; không chỉ 8 khung thu nhỏ.

**Hiệu ứng**
- Cảnh chỉ có một hai chấm và một icon đứng yên là quá đơn giản. Mỗi cảnh cần ít nhất ba lớp chuyển động có nghĩa: camera zoom hoặc trượt tới vị trí; vật xuất hiện, di chuyển, biến đổi theo lời (đường nét đứt, quân đi, vùng đổi màu, số đếm, vòng sóng); chi tiết nền (đường, sông, ruộng, thành). Đồ vật minh họa (đền, nông cụ, văn thư, đồng tiền) phải vẽ đủ chi tiết như cột đồng, kèm nhãn, không chỉ khối màu.
- Cảnh quan trọng (đền thờ, nông cụ, lễ cưới, thu thuế) zoom vào đúng nơi, vẽ vật to chiếm vùng giữa khung rồi mới thu về bản đồ. Không dùng chung một mẫu "thành + chấm + chữ" cho mọi cảnh.
- Trước khi giao nêu cho chủ kênh danh sách cảnh còn đơn giản thay vì tuyên bố đã xong; chủ kênh đã nói rõ cần "áp dụng cách dựng mới", phải so với video cột đồng đã duyệt.

## Chạy workflow và Git: bài học từ Hai Bà Trưng và Ngô Quyền (chủ kênh yêu cầu 24/10/2026)
- Job lỗi vì treo bước "Cài đặt" (apt/pip): dùng `gh run rerun <id> --failed` (chỉ chạy lại job lỗi, sau khi run đã kết thúc), KHÔNG hủy cả run. Ghép video dùng workflow riêng không `apt-get update` (`ghep-hbt.yml`, đổi tên cho từng video).
- Dựng video dài chia 16 đoạn song song, có thử lại bước cài đặt. Không chạy nhận dạng, giọng hay dựng khi chủ kênh chưa yêu cầu.
- **Bước cài đặt dùng chung** `.github/actions/cai-dat` (chủ kênh yêu cầu 24/10/2026): ffmpeg chỉ cài khi thiếu, không `apt-get update`, gói pip có cache, mỗi lần tối đa 150–200 giây và thử lại 3 lần. Workflow mới dùng `- uses: ./.github/actions/cai-dat` với `pip: "gói1 gói2"` ngay sau checkout và setup-python, không viết lại bước cài tay.

## Gemini trả 429 thì dừng, không gửi dồn (chủ kênh yêu cầu 25/10/2026)
- Khóa báo 429 (hết lượt) thì KHÔNG gửi thêm yêu cầu để thử lại liên tục: gửi nhiều có thể làm khóa bị khóa. `gemini_tts.py` đếm mọi lần 429 trong một lần chạy; đủ 8 lần (`GEMINI_MAX_429`) thì dừng hẳn (thoát mã 3), phần đã đọc vẫn được lưu. `max_wait.txt` = 30 giây.
- Gặp 429 theo ngày ("retry in" hàng giờ) thì đợi sang ngày, không chạy lại trong ngày. Chỉ chạy lại khi chủ kênh báo đã thêm khóa mới hoặc hạn mức đã có lại.
