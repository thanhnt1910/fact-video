"""Tạo map_relief.jpg phủ kín khung dọc: địa hình thật Natural Earth (domain công cộng) + bờ biển/sông của map_pretty.jpg.
Vùng: kinh 102–116,8 đông; vĩ 13,5–30,5 bắc (cao 4420 px). Gốc tọa độ trong trang: x=(lon-102)*239,4; y=(24,8-lat)*260;
ảnh đặt ở y = -1482 (vĩ 30,5). Bản gốc map_pretty.jpg (vĩ 18,2–24,8) dùng để giữ bờ biển sắc nét và sông ngòi ở vùng đó.
Cần gray_crop.png, ne1_crop.png (cắt từ GRAY_HR_SR_W.tif và NE1_HR_LC_SR_W.tif của Natural Earth, đúng vùng trên).
Chạy: python phim_ban_do/doc9x16/tao_relief.py
"""
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, distance_transform_edt, label

D = __file__.rsplit('/', 1)[0]
LAT_TOP, LAT_BOT, KX, KY = 30.5, 13.5, 239.4, 260.0
W = 3542; H = int(round((LAT_TOP - LAT_BOT) * KY))
YB = int(round((LAT_TOP - 24.8) * KY))
rng = np.random.default_rng(7)

def fbm(sig, n=3):
    f = np.zeros((H, W), 'float32'); amp = 1.0; tot = 0
    for i in range(n):
        r = gaussian_filter(rng.standard_normal((H, W)).astype('float32'), sig / (2 ** i))
        f += amp * r / (r.std() + 1e-6); tot += amp; amp *= 0.55
    return f / tot

G = np.asarray(Image.open(f'{D}/gray_crop.png').convert('L').resize((W, H), Image.BICUBIC)).astype('float32') / 255
C = np.asarray(Image.open(f'{D}/ne1_crop.png').convert('RGB').resize((W, H), Image.BICUBIC)).astype('float32') / 255

# đất/biển: Natural Earth làm nền, bản gốc đè lên ở vùng có bờ biển sắc nét
sea = gaussian_filter(((C[..., 2] - C[..., 0]) > 0.15).astype('float32'), 1.5) > 0.5
base = np.asarray(Image.open(f'{D}/map_pretty.jpg').convert('RGB')).astype('float32') / 255
bs = gaussian_filter((base[..., 2] > base[..., 0] + 0.05).astype('float32'), 1.2) > 0.5
lab, _ = label(bs); sz = np.bincount(lab.ravel()); big = sz > 60000; big[0] = False
bsea = big[lab]; river = np.zeros((H, W), bool); river[YB:YB + base.shape[0]] = (lab > 0) & ~bsea
sea[YB:YB + base.shape[0]] = bsea
lab2, _ = label(sea); sz2 = np.bincount(lab2.ravel()); b2 = sz2 > 60000; b2[0] = False
sea = b2[lab2]; land = ~sea
d_land = distance_transform_edt(land); d_sea = distance_transform_edt(sea)

# đất: màu và bóng núi từ ảnh thật, ngả da giấy, tối hơn bản trước
fine = fbm(5) * 0.05 + fbm(14) * 0.05
g = gaussian_filter(G, 0.8)
rel = np.clip((g - g.mean()) * 2.4 + 0.5 + fine * 0.7, 0, 1)
col = np.clip(C * np.array([1.0, 0.95, 0.80]), 0, 1) * 0.80 + np.array([0.74, 0.64, 0.42]) * 0.20
col = col * (0.40 + 0.80 * rel)[..., None]
col = col + (gaussian_filter(rng.standard_normal((H, W)).astype('float32'), 0.8) * 0.014)[..., None]
col = col + np.exp(-d_land / 18)[..., None] * np.array([0.08, 0.055, 0.01])
rv = gaussian_filter(river.astype('float32'), 0.8)[..., None]
col = col * (1 - rv * 0.9) + np.array([0.20, 0.50, 0.66]) * rv * 0.9
out = np.where(land[..., None], col, 0)

# biển: nông ven bờ, sâu dần ra xa
depth = 1 - np.exp(-d_sea / 220)
shallow = np.array([0.13, 0.46, 0.55]); mid = np.array([0.06, 0.24, 0.40]); deep = np.array([0.02, 0.09, 0.20])
near = np.exp(-d_sea / 26)[..., None]
sc = shallow * near + (mid * (1 - depth[..., None]) + deep * depth[..., None]) * (1 - near)
w = gaussian_filter(rng.standard_normal((H, W)).astype('float32'), 14); w = w / (w.std() + 1e-6) * 0.012
sc = sc + w[..., None]
out = np.where(sea[..., None], sc, out)

# viền bờ sáng vàng
glow = np.exp(-np.abs(np.where(sea, d_sea, d_land)) / 5.0)
out = out + glow[..., None] * np.array([0.30, 0.24, 0.05]) * 0.5

# tối dần ở rìa ảnh
yy, xx = np.mgrid[0:H, 0:W]
r = np.sqrt(((xx - W / 2) / (W * 0.65)) ** 2 + ((yy - H / 2) / (H * 0.60)) ** 2)
out = out * (1 - 0.40 * np.clip(r - 0.60, 0, 1)[..., None])
out = np.clip(out, 0, 1)
Image.fromarray((out * 255).astype('uint8')).save(f'{D}/map_relief.jpg', quality=88)
print('xong', W, H, 'y gốc', -YB)
