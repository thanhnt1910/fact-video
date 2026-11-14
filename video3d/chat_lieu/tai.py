#!/usr/bin/env python3
"""Tải chất liệu CC0 từ Poly Haven (polyhaven.com, giấy phép CC0) cho engine arch3d.js.
  python video3d/chat_lieu/tai.py <thư mục ra> [độ phân giải=1k]
Mỗi vai trò (ngói, gỗ...) chọn mã đầu tiên có thật trong danh sách ưu tiên, không có thì lấy mã đầu tiên chứa từ khóa.
Ra: <vai>_diff.jpg, <vai>_nor.jpg, <vai>_rough.jpg và nguon.json (mã, tác giả, đường dẫn)."""
import json, sys, urllib.request
from pathlib import Path

ROLES = {
    'ngoi':   (['clay_roof_tiles_02', 'clay_roof_tiles', 'roof_tiles_14', 'roof_tiles'], ['roof_tile', 'clay_roof']),
    'go':     (['wood_planks', 'old_planks_02', 'weathered_planks', 'wood_planks_grey'], ['plank']),
    'go_tron':(['bark_brown_02', 'wood_table_001', 'dark_wood'], ['wood']),
    'vua':    (['painted_plaster_wall', 'plastered_wall_02', 'beige_wall_001', 'plastered_wall'], ['plaster']),
    'gach':   (['red_brick_03', 'red_brick', 'brick_wall_02', 'old_bricks_02'], ['brick']),
    'san':    (['floor_tiles_06', 'terracotta_tiles', 'red_laterite_soil_stones', 'square_floor_tiles'], ['floor_tile', 'terracotta']),
    'da':     (['granite_tile', 'stone_tiles_02', 'castle_brick_07', 'stone_wall'], ['stone_tile', 'stone']),
    'bia':    (['rock_surface', 'gray_rocks', 'rock_boulder_dry', 'concrete_wall_008'], ['rock']),
    'co':     (['grass_path_2', 'forest_ground_04', 'aerial_grass_rock', 'sparse_grass'], ['grass']),
    'dat':    (['brown_mud_leaves_01', 'dirt_floor', 'brown_mud_02', 'dirt'], ['dirt', 'mud']),
    'duong':  (['cobblestone_floor_04', 'gravel_road', 'cobblestone_floor_01', 'gravel_floor'], ['cobblestone', 'gravel']),
    'rom':    (['thatch_roof', 'straw_roof', 'hay'], ['thatch', 'straw']),
}
MAPS = {'diff': ['Diffuse'], 'nor': ['nor_gl'], 'rough': ['Rough', 'rough']}


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'fact-video-3d (texture fetch)'})
    return urllib.request.urlopen(req, timeout=60).read()


def main(out, res='1k'):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    allt = json.loads(get('https://api.polyhaven.com/assets?t=textures'))
    (out / 'danh_sach.txt').write_text('\n'.join(sorted(allt)))
    src = {}
    for role, (pref, kw) in ROLES.items():
        pid = next((p for p in pref if p in allt), None) or next((p for p in sorted(allt) if any(k in p for k in kw)), None)
        if not pid:
            print('KHÔNG có chất liệu cho', role); continue
        files = json.loads(get(f'https://api.polyhaven.com/files/{pid}'))
        for m, keys in MAPS.items():
            k = next((k for k in keys if k in files), None)
            if not k: continue
            node = files[k][res]
            url = (node.get('jpg') or node.get('png'))['url']
            (out / f'{role}_{m}.jpg').write_bytes(get(url))
        info = allt[pid]
        src[role] = {'ma': pid, 'ten': info.get('name'), 'tac_gia': list((info.get('authors') or {}).keys()), 'url': f'https://polyhaven.com/a/{pid}', 'giay_phep': 'CC0'}
        print(f'{role:8s} <- {pid}', flush=True)
    (out / 'nguon.json').write_text(json.dumps(src, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main(*sys.argv[1:])
