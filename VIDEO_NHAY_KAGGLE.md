# Video người nhảy bằng GPU Kaggle miễn phí

Phần thêm riêng, không sửa các phần khác của repo. Lấy chuyển động từ một video nhảy mẫu, áp lên người trong một ảnh, bằng Wan 2.2 Animate 14B (nén 4-bit để vừa GPU T4 16 GB).

Files: `kaggle_dance.py`, `.github/workflows/kaggle-dance.yml`. Kernel Kaggle riêng `ngs-dance-animate`, dataset riêng `ngs-dance-input` (đều riêng tư).

## Cách dùng

1. Đưa ảnh nhân vật và video nhảy mẫu vào repo, vd `dance_in/abc/anh.jpg`, `dance_in/abc/mau.mp4`.
   - Ảnh: thấy rõ người từ đầu đến chân, tỉ lệ khung gần giống video mẫu (cùng dọc hoặc cùng ngang).
   - Video mẫu: một người nhảy, thấy rõ cả người và mặt, góc quay cố định.
   - Chỉ dùng ảnh của chính bạn hoặc người đã đồng ý.
2. Vào Actions → "Video người nhảy (Kaggle, miễn phí)" → Run workflow:
   - `buoc = gui`, `thu = true` (lần đầu chỉ làm 3 giây để thử).
   - Quá trình gửi mất vài phút; Kaggle chạy nền.
3. Vài giờ sau chạy lại với `buoc = lay` (cùng `ten`, thêm `mau` để lấy nhạc). Video nằm ở mục Artifacts của lần chạy.
4. Nếu bản thử ổn, chạy lại `gui` với `thu = false` để làm đủ 30 giây (3 đoạn × 10 giây).

Chạy từ máy: `python kaggle_dance.py gui --ten abc --anh ... --mau ... --thu`, rồi `python kaggle_dance.py lay --ten abc --mau ...`.

## Lưu ý

- Chưa chạy thử trên Kaggle. Lần chạy thử 3 giây đầu tiên là để phát hiện lỗi; đọc `logs/kaggle_dance/<tên>_kaggle_log.txt` (bước `lay` tạo ra) nếu có lỗi.
- Ước tính chậm: có thể vài chục phút đến hơn một giờ cho mỗi 10 giây video ở khung 368x640. Hạn mức GPU Kaggle khoảng 30 giờ mỗi tuần (số do người dùng báo cáo, Kaggle không công bố). Hạ `--rong/--cao` hoặc `--buoc-suy-luan` để nhanh hơn, chất lượng giảm.
- Kernel dùng một slug cố định: mỗi lần chỉ một video, và không chạy cùng lúc với workflow Kaggle khác (vẽ ảnh, tranh thành video).
- Không có bước chỉnh dáng người theo ảnh (retarget): ảnh và video mẫu nên có dáng người và khung hình tương tự.
- Khung xương lấy bằng DWPose (controlnet-aux), mặt cắt bằng OpenCV YuNet. Hai phần này là bản xấp xỉ của bước tiền xử lý gốc của Wan-Animate nên chất lượng có thể kém bản gốc.
- Workflow không commit gì vào repo; video chỉ nằm ở Artifacts (giữ theo thời hạn mặc định của GitHub).
