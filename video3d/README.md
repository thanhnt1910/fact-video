# TQ Video Engine v2 (Three.js): dựng video 3D Tam Quốc từ kịch bản JSON

Bản v2 dựng cảnh bằng **Three.js (WebGL)**: lưới 3D thật cho thuyền, buồm, cờ, xích sắt, vách đá, lính và nhân vật; ánh sáng PBR (trăng + đèn lửa động); mặt nước phản chiếu như gương có sóng; hạt lửa, khói, tàn lửa; hậu kỳ bloom + FXAA. Âm thanh tổng hợp giữ nguyên như v1 (sóng, gió, lửa, trống, tù và, cồng, nổ, tên bay, rơi nước, nhạc nền).

**Định dạng spec JSON giữ nguyên như v1**, nên các spec cũ chạy được ngay. `engine.js` (canvas 2D) là bản v1, chỉ để tham khảo; `tqvideo.py` hiện tại dùng `engine3d.js`.

## Khôi phục trong chat mới (cho Claude)
1. `project_read` các file: `claude/tq-video-engine/engine3d.js`, `tqvideo.py`, `audio.py` và một spec mẫu (`xich_bich_30s.json`). Lưu vào `/home/claude/tqvideo/`.
2. Trong thư mục đó chạy `npm install three` (cần `node_modules/three` nằm cạnh `tqvideo.py`).
3. Yêu cầu: Chrome tại `/usr/bin/google-chrome`, Python có playwright, numpy, scipy, PIL; ffmpeg; font Lora + Noto Serif CJK SC. Không cần GPU: WebGL chạy bằng SwiftShader (đã cài sẵn cờ trong `tqvideo.py`).
4. `python3 tqvideo.py preview spec.json [t1,t2,...]` để xuất contact sheet; `python3 tqvideo.py frame spec.json 12.5` để xuất một khung full-size.
5. `python3 tqvideo.py render spec.json` để xuất `spec.mp4` có hình và tiếng. Tốc độ trên máy 2 nhân không GPU: khoảng 1–2,5 giây/khung, video 30 giây mất khoảng 30–40 phút, nên chạy nền bằng `nohup ... &`.

**Không đọc lại engine3d.js vào ngữ cảnh nếu không cần sửa engine.** Chỉ cần viết và chỉnh JSON.

## Lưu ý kỹ thuật
- Trang được phục vụ qua HTTP nội bộ (ES module + importmap), không mở bằng file://.
- Không dùng `page.screenshot` (Chrome headless + SwiftShader trả về ảnh đen); khung hình được ghép trong trang bằng `window.grab()` (WebGL + lớp phụ đề 2D).
- Chi phí lớn nhất là hạt khói kích thước lớn (overdraw). Nếu render chậm, giảm `quality.smokeRate` hoặc `quality.reflScale`.

## Hệ toạ độ
x sang phải (hướng gió đông thổi), y hướng lên (mặt nước y=0), z hướng vào sâu. Một chiến thuyền dài khoảng 14 đơn vị, người cao khoảng 1.8.

## Cấu trúc spec
```json
{
  "size": [1920,1080], "fps": 30, "seed": 1,
  "quality": { "exposure":1.0, "bloom":0.55, "msaa":0, "reflScale":0.5, "fog":0.0009,
               "fireRate":0.55, "fireAlpha":0.2, "smokeRate":0.09, "fireLight":180 },
  "world": { "wind": [5.5,0,1.2], "lights": [{ "from":[x,z], "to":[x,z], "count":60, "y":1 }] },
  "fleets": [{
    "id":"tao", "kind":"war|fire|small", "rows":4, "cols":7, "origin":[x,z], "spacing":[dx,dz], "stagger":4,
    "chained":true, "flag":"曹", "flagColor":[r,g,b], "sailColor":[r,g,b], "crew":4,
    "move":   { "by":[dx,dz], "t0":4, "t1":11, "ease":"accel|inout|linear|out|in" },
    "ignite": { "at":11, "spreadCol":0.6, "spreadRow":0.35, "jitter":0.6 }
  }],
  "volleys": [{ "at":15, "dur":3, "count":70, "from":[x,y,z], "spread":[sx,sz], "target":"tao", "flight":2, "height":30 }],
  "rocks":   [{ "pos":[x,0,z], "size":[w,h,d] }],
  "figures": [{ "name":"Chu Du", "pos":[x,y,z], "height":2, "sword":true, "look":[x,y,z] }],
  "shots": [{
    "name":"...", "dur":5, "fadeIn":1, "fadeOut":1,
    "cam": { "from":{ "pos":[x,y,z], "look":[x,y,z] }, "to":{...}, "ease":"inout",
             "follow":"fleetId:index", "shake":0.5, "fov":[50,42] },
    "captions": [{ "at":1, "dur":4, "text":"...", "sub":"...", "style":"lower|title", "cn":"赤 壁" }]
  }],
  "audio": {
    "ambience": { "water":0.6, "wind":0.45 }, "fire":1, "splash":0.7, "arrows":0.9, "ignite":0.6,
    "music": { "gain": [[t,g], ...] },
    "drums": [{ "from":6, "to":11, "bpm":100, "pattern":"X...x...", "crescendo":true, "gain":0.7 }],
    "cues":  [{ "at":11, "type":"boom|gong|horn|whoosh|taiko|splash", "gain":1, "dur":2, "pan":0 }]
  }
}
```
- `quality` là tuỳ chọn (mới ở v2). `figures[].look` (mới) là điểm nhân vật quay mặt về.
- Lửa, khói, lính nhảy xuống sông, ánh lửa trên mặt nước và tiếng lửa, tiếng nước đều **tự sinh** theo `ignite`. Tên lửa bắn trúng thuyền nào thì thuyền đó bắt lửa sớm hơn.
- Khi `follow` được bật, `pos` và `look` là độ lệch tương đối so với thuyền được bám theo.
- Video dọc cho TikTok: đặt `"size":[1080,1920]` và tăng `fov` lên khoảng 60–70.

## Engine kiến trúc sa bàn: arch3d.js (chủ đề lịch sử trường đại học)
- Đặt `"engine":"arch3d.js"` trong spec để dùng. `tqvideo.py` và `audio.py` dùng chung.
- Bộ dựng sẵn (`buildings[].type`): `hall` (sảnh 1–2 tầng mái, cột, cửa bức bàn), `gate` (cổng tam quan, có hoành phi chữ Hán), `khueVanCac`, `wall`, `pond` (mặt nước phản chiếu), `stelae` (bia trên rùa). Ngoài ra còn `ground` (cỏ, gạch bát, đường, đất), `trees`, `houses`, `crowds` (người đi lại), `birds`.
- Máy quay có thêm `orbit` (bay vòng quanh một điểm), `tilt` (độ mờ tilt-shift kiểu sa bàn) và `focus`. Phụ đề có thêm kiểu `"style":"year"` (số năm lớn).
- Âm thanh mới: `ambience.birds`, `music.style:"pentatonic"` (đàn dây ngũ cung), cue `bell` (chuông chùa).
- Mẫu: `make_vanmieu.py` sinh ra `van_mieu.json` (Văn Miếu – Quốc Tử Giám, 36,5 giây). Tốc độ khoảng 2,8 giây/khung trên máy không GPU.
- Lưu ý: hai lớp nền chồng nhau cần cách nhau ít nhất khoảng 5 cm (y), nếu không sẽ bị lỗi chập hình khi nhìn ở góc thấp.

## Chi phí token tham khảo
- Video mới dùng engine có sẵn: khoảng 5–15 nghìn token (viết JSON, xem 1–2 contact sheet, render).
- Thêm loại đối tượng mới vào engine (ngựa, thành trì, mưa, tuyết...): khoảng 20–40 nghìn token mỗi loại, chỉ trả một lần.

## Dựng trên GitHub Actions (song song)
- Workflow: `.github/workflows/dung-3d.yml`, chạy trên nhánh `dung-3d-sa-ban` khi đẩy `video3d/dung.txt`, hoặc bấm tay (workflow_dispatch).
- `video3d/dung.txt` dòng đầu: `<spec trong video3d/specs> <số đoạn 1–20>`, ví dụ `van_mieu.json 8`.
- Mỗi đoạn dựng trên một máy riêng (`tqvideo.py doan spec i n out.mp4`), đoạn 0 ghi thêm `log.json` (mốc âm thanh); job `ghep` nối đoạn và trộn âm thanh (`tqvideo.py ghep`). Video cuối nằm ở artifact `video-<tên spec>`.
- Chạy tay trên máy: `cd video3d && npm install && python3 tqvideo.py render specs/van_mieu.json`.
