# Soạn file hướng dẫn làm clip Veo trong Google Flow cho tm28 và gom ảnh nguồn (16:9, đã bỏ dấu đỏ) vào /dev/shm/tm28/veo_nguon/.
import json,sys,os,cv2,zipfile
sys.path.insert(0,'/tmp/pc/phim_ban_do/thuymac')
import canh_tm28 as c
from lam_anh_tm28 import sach
J=json.load(open('/tmp/pc/ke-hoach/thu-giong-hai/tm28_full.json'))
TIEN=("Animate this exact sumi-e ink wash painting on rice paper. Keep the same loose brush style, monochrome ink with faint sepia, "
      "the same colours (only the one jade green boat is coloured), the same people, faces, clothes, weapons and number of people, arms and hands. "
      "No new people, no new objects, no text, no letters, no camera cut, no zoom into faces, no blood, silent, no music, no speech. Motion: ")
os.makedirs('/dev/shm/tm28/veo_nguon',exist_ok=True)
L=['# tm28 Chế Bồng Nga: 42 clip Veo làm trong Google Flow','',
'Chủ kênh chọn làm tay trong Flow (26/11). Ảnh nguồn gửi kèm trong `tm28_veo_nguon.zip`: mỗi clip một ảnh 1920×1080, tên trùng mã clip.','',
'## Cách làm mỗi clip','1. Flow → **Frames to Video**, tải ảnh `<mã>.jpg` làm khung đầu.','2. Dán nguyên **tiền tố** bên dưới, rồi dán **chuyển động** của clip ngay sau chữ `Motion:`.',
'3. Chọn 16:9, 8 giây (cảnh tĩnh, ít người có thể 6 giây), tắt âm thanh.','4. Tải về, đặt tên `<mã>.mp4` (ví dụ `a34.mp4`) rồi gửi lại cho tôi. Clip hỏng thì tạo lại tối đa 3 lần với cùng prompt.','',
'**Bỏ clip** nếu: thêm người hoặc vật, thừa tay chân, mặt méo, đổi áo hoặc vũ khí, ngựa thừa chân, xuất hiện chữ, có thêm thuyền xanh, kiểu vẽ đổi sang ảnh thật hay hoạt hình 3D, cảnh nhảy cắt. Xem ở khung đầu, giữa và cuối.','',
'## Tiền tố (dán vào MỌI clip)','','```',TIEN.strip(),'```','','## 42 clip','']
z=zipfile.ZipFile('/dev/shm/tm28/tm28_veo_nguon.zip','w')
for k,d,mo,veo in c.C:
    if not veo: continue
    im=sach(cv2.imread(f'/dev/shm/tm28/kg/{k}.jpg'));im=cv2.resize(im,(1920,1080),interpolation=cv2.INTER_LANCZOS4)
    f=f'/dev/shm/tm28/veo_nguon/{k}.jpg';cv2.imwrite(f,im,[cv2.IMWRITE_JPEG_QUALITY,92]);z.write(f,f'{k}.jpg')
    loi=J[d-1]['text']
    L+=[f'### {k} (đoạn {d})',f'> {loi}','','```',veo,'```','']
z.close()
open('/tmp/pc/ke-hoach/tm28-veo-flow.md','w').write('\n'.join(L)+'\n')
print(sum(1 for x in c.C if x[3]))
