# Remotion: dựng video bằng code (nhánh `remotion`)

Thử nghiệm dựng video bản đồ động bằng Remotion (React) thay cho Pillow/ffmpeg.
Chuyển động do code tính theo số khung hình, không dùng AI sinh video.

## Chạy

```bash
cd remotion
npm install
npm run studio          # xem trước, chỉnh trực tiếp
npx remotion render src/index.ts DemoBanDo out/demo.mp4   # xuất MP4
```

Nếu máy không tự tải được trình duyệt cho Remotion, thêm
`--browser-executable=<đường dẫn Chrome>`.

## Demo `DemoBanDo` (13 giây, 1080x1920, 30 fps)

- Bản đồ vẽ bằng SVG (nền giấy, sông, núi), có logo kênh và phụ đề từng câu.
- Quân (7 lính nhấp nhô khi bước) đi theo đường cong Bézier từ Thành A qua sông tới Thành B.
- Camera: toàn cảnh, zoom vào Thành A, đi theo quân, zoom ra Thành B.
- Video mẫu: `demo/demo-ban-do.mp4`.

Mã nguồn: `src/DemoBanDo.tsx` (cảnh), `src/Root.tsx` (khai báo video).
