"""Tạo map_relief.jpg từ map_pretty.jpg: nổi khối núi, màu theo độ cao, bờ biển sáng, biển có chiều sâu.
Giữ nguyên kích thước và hệ tọa độ (LON0=102, LAT1=24.8, 239.4 px/độ kinh, 260 px/độ vĩ).
Độ cao là mô phỏng theo địa hình chung (cao nguyên Vân Quý, Nam Lĩnh, dãy Trường Sơn, núi Hải Nam), không phải số liệu đo.
Chạy: python phim_ban_do/doc9x16/tao_relief.py
"""
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, distance_transform_edt

D = __file__.rsplit('/', 1)[0]
im = Image.open(f'{D}/map_pretty.jpg').convert('RGB')
W, H = im.size
a = np.asarray(im).astype('float32') / 255
rng = np.random.default_rng(7)
KX, KY = 239.4, 260.0
lon = 102 + (np.arange(W) / KX)[None, :] * np.ones((H, 1))
lat = 24.8 - (np.arange(H) / KY)[:, None] * np.ones((1, W))

# đất / biển
sea = (a[..., 2] > a[..., 0] + 0.05)
sea = gaussian_filter(sea.astype('float32'), 1.2) > 0.5
from scipy.ndimage import label
lab, nl = label(sea); sz = np.bincount(lab.ravel()); big = sz > 60000; big[0] = False
sea = big[lab]          # chỉ giữ biển lớn; sông và hồ nhỏ coi như đất, giữ nguyên nét vẽ
river = (lab > 0) & ~sea
land = ~sea
d_land = distance_transform_edt(land)      # px vào trong đất
d_sea = distance_transform_edt(sea)        # px ra biển

def blob(lo, la, rl, ra, h):
    return h * np.exp(-(((lon - lo) / rl) ** 2 + ((lat - la) / ra) ** 2))

# khung độ cao theo địa hình chung (0..1)
env = (blob(102.5, 23.5, 2.2, 1.6, 0.95)      # cao nguyên Vân Nam, Quý Châu
       + blob(104.5, 22.0, 1.6, 1.0, 0.60)     # Tây Bắc, Việt Bắc
       + blob(109.0, 25.3, 2.4, 0.5, 0.55)     # Nam Lĩnh
       + blob(111.5, 24.6, 1.8, 0.7, 0.35)
       + blob(105.6, 18.8, 0.7, 1.4, 0.70)     # Trường Sơn phía bắc
       + blob(104.4, 20.6, 0.7, 1.6, 0.55)     # biên giới Việt - Lào
       + blob(109.6, 19.1, 0.45, 0.35, 0.60))  # núi Hải Nam
env = np.clip(env, 0, 1)

def fbm(sig, n=5, base=1.0):
    f = np.zeros((H, W), 'float32'); amp = base; tot = 0
    for i in range(n):
        r = gaussian_filter(rng.standard_normal((H, W)).astype('float32'), sig / (2 ** i))
        f += amp * r / (r.std() + 1e-6); tot += amp; amp *= 0.55
    return f / tot
n1 = fbm(70, 4)
ridge = 1 - np.abs(n1) * 1.1            # đỉnh núi dạng sống núi
ridge = np.clip(ridge, 0, 1) ** 1.6
elev = env * (0.45 + 0.75 * ridge) + 0.05 * np.clip(d_land / 160, 0, 1)
elev = gaussian_filter(elev, 5.0) * land
elev = np.clip(elev, 0, 1.2)

# đổ bóng từ góc tây bắc
gy, gx = np.gradient(gaussian_filter(elev, 1.5) * 55)
shade = np.clip(0.5 + (-gx * 0.7 - gy * 0.7) * 0.9, 0, 1)
shade = (shade - 0.5) * 1.5 + 1.0

out = a.copy()
# địa hình thật: Natural Earth (domain công cộng), cắt đúng vùng, phóng 4 lần rồi thêm chi tiết mịn
G = np.asarray(Image.open(f'{D}/gray_crop.png').convert('L').resize((W, H), Image.BICUBIC)).astype('float32') / 255
C = np.asarray(Image.open(f'{D}/ne1_crop.png').convert('RGB').resize((W, H), Image.BICUBIC)).astype('float32') / 255
fine = fbm(5, 3) * 0.05 + fbm(14, 3) * 0.05
g = gaussian_filter(G, 0.8)
rel = np.clip((g - g.mean()) * 2.4 + 0.5 + fine * (0.5 + elev), 0, 1)
tone = np.array([1.02, 0.97, 0.82])                      # ngả màu da giấy cũ
base_col = np.clip(C * tone, 0, 1)
parch = np.array([0.80, 0.70, 0.46])
col = base_col * 0.80 + parch * 0.20
lum = 0.55 + 0.95 * rel                                   # sáng tối theo bóng núi
col = col * lum[..., None]
col = col + (grain := gaussian_filter(rng.standard_normal((H, W)).astype('float32'), 0.8) * 0.014)[..., None]
rim_in = np.exp(-d_land / 18)[..., None]
col = col + rim_in * np.array([0.10, 0.07, 0.01]) * land[..., None]
# sông giữ từ bản vẽ gốc
rv = gaussian_filter(river.astype('float32'), 0.8)[..., None]
col = col * (1 - rv * 0.9) + np.array([0.20, 0.50, 0.66]) * rv * 0.9
out = np.where(land[..., None], col, out)

# biển: sâu dần khi xa bờ, sóng mờ, bờ nước nông xanh ngọc
depth = 1 - np.exp(-d_sea / 220)
shallow = np.array([0.13, 0.46, 0.55]); mid = np.array([0.06, 0.24, 0.40]); deep = np.array([0.02, 0.09, 0.20])
sc = shallow * np.exp(-d_sea / 26)[..., None] + (mid * (1 - depth[..., None]) + deep * depth[..., None]) * (1 - np.exp(-d_sea / 26)[..., None])
wave = gaussian_filter(rng.standard_normal((H, W)).astype('float32'), 14)
wave = wave / (wave.std() + 1e-6) * 0.012
sc = sc + wave[..., None]
out = np.where(sea[..., None], sc, out)

# viền bờ phát sáng vàng
glow = np.exp(-np.abs(np.where(sea, d_sea, d_land)) / 5.0)
out = out + glow[..., None] * np.array([0.30, 0.24, 0.05]) * 0.55

# sắc độ chung ấm, tối dần ở góc
yy, xx = np.mgrid[0:H, 0:W]
r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.45) / (H * 0.70)) ** 2)
out = out * (1 - 0.40 * np.clip(r - 0.55, 0, 1)[..., None])
out = np.clip(out, 0, 1)
Image.fromarray((out * 255).astype('uint8')).save(f'{D}/map_relief.jpg', quality=90)
print('xong', W, H)
