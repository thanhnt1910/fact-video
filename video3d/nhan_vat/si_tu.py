# Dựng nhân vật sĩ tử (MPFB/MakeHuman CC0) mặc áo giao lĩnh, đội khăn, ngồi viết bài; render bằng Cycles.
# Chạy: python3 si_tu.py [ra.png|ra_dir] [khung_dau khung_cuoi] [mau]
# Biến môi trường: MH_ASSETS = thư mục gói makehuman_system_assets đã giải nén (nếu có: da, mắt, lông mày, lông mi).
import bpy, addon_utils, importlib, math, os, sys, glob
from mathutils import Vector, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
CL = os.path.join(HERE, '..', 'chat_lieu')
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/si_tu.png'
F0 = int(sys.argv[2]) if len(sys.argv) > 2 else 1
F1 = int(sys.argv[3]) if len(sys.argv) > 3 else F0
SAMPLES = int(sys.argv[4]) if len(sys.argv) > 4 else 48
RES = os.environ.get('RES', '960x540')
FPS = 24

bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("bl_ext.user_default.mpfb", default_set=True)
M = lambda p: importlib.import_module("bl_ext.user_default.mpfb." + p)
HS = M("services.humanservice").HumanService
HOP = M("entities.objectproperties").HumanObjectProperties
TS = M("services.targetservice").TargetService

# ---------------- người ----------------
h = HS.create_human()
for k, v in [('asian', 1.0), ('african', 0.0), ('caucasian', 0.0), ('gender', 1.0), ('age', 0.42),
             ('muscle', 0.45), ('weight', 0.4), ('height', 0.4), ('proportions', 0.7)]:
    HOP.set_value(k, v, entity_reference=h)
TS.reapply_macro_details(h)
# nét mặt thanh, gò má nhẹ (target có sẵn trong data/targets)
def tgt(name, val):
    for f in glob.glob(os.path.join(M("services.locationservice").LocationService.get_mpfb_data("targets"), '**', name + '.target.gz'), recursive=True):
        try:
            TS.load_target(h, f, weight=val, name=name)
        except Exception as e:
            print('target lỗi', name, e)
        return
for n, v in [('head-oval', 0.5), ('nose-scale-horiz-decr', 0.2), ('eyebrows-trans-down', 0.15)]:
    tgt(n, v)

rig = HS.add_builtin_rig(h, "game_engine")
bpy.context.view_layer.update()
MHA = os.environ.get('MH_ASSETS')
skin_done = False; HAS_EYES = False
if MHA and os.path.isdir(MHA):
    def find(pat):
        r = sorted(glob.glob(os.path.join(MHA, pat), recursive=True)); return r[0] if r else None
    sk = find('skins/young_asian_male/*.mhmat') or find('skins/**/*male*.mhmat')
    if sk:
        print('da:', sk); HS.set_character_skin(sk, h, skin_type=os.environ.get('SKIN_TYPE', 'ENHANCED_SSS')); skin_done = True
    for pat, typ in [('eyes/high-poly/high-poly.mhclo', 'Eyes'), ('eyebrows/' + os.environ.get('BROW', 'eyebrow010') + '/*.mhclo', 'Eyebrows'),
                     ('eyelashes/eyelashes02/*.mhclo', 'Eyelashes')]:
        f = find(pat)
        if f:
            try:
                o = HS.add_mhclo_asset(f, h, asset_type=typ, subdiv_levels=1 if typ == 'Eyes' else 0)
                print(typ, f, o.name if o else None)
                if typ == 'Eyes':
                    HAS_EYES = True
                    em = find('eyes/materials/brown.mhmat')
                    if em and o:
                        try:
                            MS = M("services.materialservice").MaterialService
                            MS.delete_all_materials(o)
                            mm = M("entities.material.makeskinmaterial").MakeSkinMaterial
                            mat = MS.create_empty_material('mat_mat', o); ms = mm(); ms.populate_from_mhmat(em); ms.apply_node_tree(mat)
                        except Exception as e:
                            print('màu mắt lỗi', e)
            except Exception as e:
                print('lỗi', typ, e)
if not skin_done:
    HS.set_character_skin(None, h, skin_type="LAYERED")
# chốt các shape key (hình dáng) vào lưới để toạ độ đỉnh là toạ độ thật
if h.data.shape_keys:
    bpy.context.view_layer.objects.active = h
    with bpy.context.temp_override(object=h, active_object=h, selected_objects=[h]):
        bpy.ops.object.shape_key_remove(all=True, apply_mix=True)
mw = h.matrix_world

def bone_head(n):
    return rig.matrix_world @ rig.data.bones[n].head_local
def bone_tail(n):
    return rig.matrix_world @ rig.data.bones[n].tail_local

# ---------------- vật liệu ----------------
def mat_basic(name, col, rough=0.7, sheen=0.0, spec=0.3):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1)
    b.inputs['Roughness'].default_value = rough
    if 'Sheen Weight' in b.inputs:
        b.inputs['Sheen Weight'].default_value = sheen
    if 'Specular IOR Level' in b.inputs:
        b.inputs['Specular IOR Level'].default_value = spec
    return m

def mat_fabric(name, col, dark=0.75, scale=420.0):
    # vải dệt: noise nhỏ làm sợi + wave tạo thớ, nếp tối ở chỗ khuất (AO)
    m = mat_basic(name, col, 0.85, sheen=0.25, spec=0.15)
    b0 = m.node_tree.nodes['Principled BSDF']
    if 'Sheen Tint' in b0.inputs: b0.inputs['Sheen Tint'].default_value = (min(1,col[0]*3), min(1,col[1]*3), min(1,col[2]*3), 1)
    nt = m.node_tree; N = nt.nodes; L = nt.links; b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord')
    w1 = N.new('ShaderNodeTexWave'); w1.inputs['Scale'].default_value = scale; w1.inputs['Distortion'].default_value = 2
    w2 = N.new('ShaderNodeTexWave'); w2.inputs['Scale'].default_value = scale; w2.bands_direction = 'Y'
    L.new(tc.outputs['Object'], w1.inputs['Vector']); L.new(tc.outputs['Object'], w2.inputs['Vector'])
    mx = N.new('ShaderNodeMix'); mx.data_type = 'FLOAT'; mx.inputs[0].default_value = 0.5
    L.new(w1.outputs['Fac'], mx.inputs[2]); L.new(w2.outputs['Fac'], mx.inputs[3])
    ao = N.new('ShaderNodeAmbientOcclusion'); ao.inputs['Distance'].default_value = 0.06
    cr = N.new('ShaderNodeMix'); cr.data_type = 'RGBA'; cr.blend_type = 'MULTIPLY'
    cr.inputs[6].default_value = (*col, 1)
    ramp = N.new('ShaderNodeMapRange'); ramp.inputs[3].default_value = dark; ramp.inputs[4].default_value = 1.0
    L.new(ao.outputs['AO'], ramp.inputs[0])
    sh = N.new('ShaderNodeMath'); sh.operation = 'MULTIPLY'
    v = N.new('ShaderNodeMapRange'); v.inputs[3].default_value = 0.88; v.inputs[4].default_value = 1.0
    L.new(mx.outputs[0], v.inputs[0])
    L.new(ramp.outputs[0], sh.inputs[0]); L.new(v.outputs[0], sh.inputs[1])
    L.new(sh.outputs[0], cr.inputs[0])
    col2 = N.new('ShaderNodeMix'); col2.data_type = 'RGBA'; col2.inputs[0].default_value = 1.0
    col2.blend_type = 'MULTIPLY'; col2.inputs[6].default_value = (*col, 1)
    cv = N.new('ShaderNodeCombineColor')
    L.new(sh.outputs[0], cv.inputs[0]); L.new(sh.outputs[0], cv.inputs[1]); L.new(sh.outputs[0], cv.inputs[2])
    L.new(cv.outputs[0], col2.inputs[7])
    L.new(col2.outputs[2], b.inputs['Base Color'])
    bump = N.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.15; bump.inputs['Distance'].default_value = 0.002
    L.new(mx.outputs[0], bump.inputs['Height']); L.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m

def mat_tex(name, stem, scale=1.0, tint=(1, 1, 1)):
    m = mat_basic(name, (1, 1, 1), 0.8)
    nt = m.node_tree; N = nt.nodes; L = nt.links; b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord'); mp = N.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale,) * 3
    L.new(tc.outputs['UV'], mp.inputs['Vector'])
    def img(suf, nonc):
        p = os.path.join(CL, f'{stem}_{suf}.jpg')
        if not os.path.exists(p):
            return None
        t = N.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(p)
        if nonc:
            t.image.colorspace_settings.name = 'Non-Color'
        L.new(mp.outputs[0], t.inputs['Vector']); return t
    d = img('diff', False)
    if d:
        mu = N.new('ShaderNodeMix'); mu.data_type = 'RGBA'; mu.blend_type = 'MULTIPLY'; mu.inputs[0].default_value = 1
        mu.inputs[7].default_value = (*tint, 1)
        L.new(d.outputs['Color'], mu.inputs[6]); L.new(mu.outputs[2], b.inputs['Base Color'])
    r = img('rough', True)
    if r:
        L.new(r.outputs['Color'], b.inputs['Roughness'])
    n = img('nor', True)
    if n:
        nm = N.new('ShaderNodeNormalMap'); L.new(n.outputs['Color'], nm.inputs['Color']); L.new(nm.outputs[0], b.inputs['Normal'])
    return m

ROBE = mat_fabric('ao', (0.028, 0.036, 0.062))          # áo vải nâu nhạt (sĩ tử áo the/vải)
INNER = mat_fabric('ao_trong', (0.80, 0.76, 0.66))   # áo lót trắng ngà ở cổ giao lĩnh
BELT = mat_fabric('dai', (0.12, 0.10, 0.08), scale=600)
KHAN = mat_fabric('khan', (0.035, 0.03, 0.028), dark=0.6, scale=700)
def khan_ridges(m):
    N = m.node_tree.nodes; L = m.node_tree.links; b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord'); w = N.new('ShaderNodeTexWave'); w.wave_profile = 'SIN'
    w.bands_direction = 'Z'; w.inputs['Scale'].default_value = 30; w.inputs['Distortion'].default_value = 4.0
    w.inputs['Detail'].default_value = 1
    L.new(tc.outputs['Object'], w.inputs['Vector'])
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.3; bp.inputs['Distance'].default_value = 0.003
    L.new(w.outputs['Fac'], bp.inputs['Height'])
    old = b.inputs['Normal'].links[0].from_node if b.inputs['Normal'].links else None
    if old: L.new(old.outputs['Normal'], bp.inputs['Normal'])
    L.new(bp.outputs['Normal'], b.inputs['Normal'])
khan_ridges(KHAN)
HAIR = mat_basic('toc', (0.012, 0.01, 0.009), 0.45, sheen=0.4)
INK = mat_basic('muc', (0.01, 0.01, 0.01), 0.15, spec=0.6)

# ---------------- áo giao lĩnh: nhân bản thân, đẩy ra ngoài, giữ trọng số xương ----------------
def dup(src, name):
    o = src.copy(); o.data = src.data.copy(); o.name = name
    bpy.context.collection.objects.link(o)
    for m in list(o.modifiers):
        if m.type != 'ARMATURE':
            o.modifiers.remove(m)
    return o

import bmesh
pel = bone_head('pelvis'); neck = bone_head('neck_01'); headb = bone_head('head')
handL = bone_head('hand_l'); handR = bone_head('hand_r')
footz = bone_head('foot_l').z

robe = dup(h, 'ao')
bm = bmesh.new(); bm.from_mesh(robe.data)
dl = robe.data.vertices
body_idx = robe.vertex_groups['body'].index
deform = bm.verts.layers.deform.verify()
kill = []
for v in bm.verts:
    g = v[deform]
    p = mw @ v.co
    inbody = body_idx in g
    if not inbody:
        kill.append(v); continue
    # bỏ đầu, cổ trên, bàn tay, bàn chân
    if p.z > neck.z + 0.03:
        kill.append(v); continue
    if abs(p.x) > abs(handL.x) - 0.035 and p.z > pel.z:
        kill.append(v); continue
    if p.z < footz + 0.06:
        kill.append(v); continue
bmesh.ops.delete(bm, geom=kill, context='VERTS')
# đẩy ra ngoài theo pháp tuyến; tay áo rộng dần về cổ tay (áo giao lĩnh tay thụng)
bm.normal_update()
for v in bm.verts:
    p = mw @ v.co
    off = 0.012
    ax = abs(p.x)
    sh = abs(bone_head('upperarm_l').x)
    if ax > sh and p.z > pel.z:
        t = min(1, (ax - sh) / max(0.01, abs(handL.x) - sh))
        off += 0.022 * t ** 1.6
        # tay thụng rủ xuống
        v.co += mw.inverted().to_3x3() @ Vector((0, 0, 0))
    if p.z < pel.z + 0.05:  # vạt áo dài phủ chân
        off += 0.025 + 0.05 * max(0, (pel.z - p.z)) / max(0.1, pel.z - footz)
    v.co += v.normal * off
bm.to_mesh(robe.data); bm.free()
robe.data.materials.clear(); robe.data.materials.append(ROBE)
sol = robe.modifiers.new('day', 'SOLIDIFY'); sol.thickness = 0.006; sol.offset = 1
sub = robe.modifiers.new('min', 'SUBSURF'); sub.levels = 1; sub.render_levels = 2
for m in robe.modifiers:
    pass
# đưa armature lên đầu, solidify/subsurf sau
while robe.modifiers[0].type != 'ARMATURE':
    bpy.context.view_layer.objects.active = robe
    bpy.ops.object.modifier_move_up(modifier=robe.modifiers[[m.type for m in robe.modifiers].index('ARMATURE')].name)
for p in robe.data.polygons:
    p.use_smooth = True

# cổ giao lĩnh: dải vải trắng ngà chéo từ vai phải xuống nách trái (vạt trái đè vạt phải)
def bind(o, bone):
    vg = o.vertex_groups.new(name=bone); vg.add(list(range(len(o.data.vertices))), 1.0, 'REPLACE')
    am = o.modifiers.new('xuong', 'ARMATURE'); am.object = rig
    o.parent = rig
    while o.modifiers[0].name != 'xuong':
        o.modifiers.move(len(o.modifiers) - 1, 0) if hasattr(o.modifiers, 'move') else None
        break
    # đưa armature lên đầu
    with bpy.context.temp_override(object=o):
        for _ in range(len(o.modifiers)):
            if o.modifiers[0].name == 'xuong':
                break
            bpy.ops.object.modifier_move_up(modifier='xuong')

def strip(name, pts, width, mat, thick=0.004, parent_bone='spine_03', normal=Vector((0, -1, 0))):
    bm = bmesh.new()
    prev = None
    for i, p in enumerate(pts):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        side = d.cross(normal).normalized() * width / 2
        a = bm.verts.new(p - side); b = bm.verts.new(p + side)
        if prev:
            bm.faces.new((prev[0], prev[1], b, a))
        prev = (a, b)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    s = o.modifiers.new('d', 'SOLIDIFY'); s.thickness = thick
    sb = o.modifiers.new('s', 'SUBSURF'); sb.levels = 1; sb.render_levels = 2
    for pl in me.polygons:
        pl.use_smooth = True
    bind(o, parent_bone)
    return o

from mathutils import Matrix
def Matrix_identity():
    return Matrix.Identity(4)

# tìm bề mặt ngực để đặt cổ áo: lấy các điểm gần nhất trên robe
deps = bpy.context.evaluated_depsgraph_get()
def surf(p, ofs=0.004):
    ok, loc, nor, idx = robe.closest_point_on_mesh(robe.matrix_world.inverted() @ p)
    return robe.matrix_world @ (loc + nor * ofs) if ok else p

sR = bone_head('clavicle_r'); sL = bone_head('clavicle_l'); sp3 = bone_head('spine_03'); sp1 = bone_head('spine_01')
front_y = sp3.y - 0.16
# cổ giao lĩnh và đai lưng tô thẳng lên lưới áo (thuộc tính màu theo đỉnh), nên đi theo mọi cử động
def seg_dist(p, a, b):
    ab = b - a; t = max(0, min(1, (p - a).dot(ab) / ab.dot(ab))); return (p - (a + ab * t)).length
cA = Vector((neck.x + 0.055, 0, neck.z - 0.005))       # vai trái người mặc
cB = Vector((neck.x - 0.15, 0, sp3.z - 0.10))          # xuống nách phải: vạt trái đè vạt phải
attr = robe.data.attributes.new('nghi', 'FLOAT_VECTOR', 'POINT')   # toạ độ tư thế nghỉ
for i, v in enumerate(robe.data.vertices):
    attr.data[i].vector = mw @ v.co
nt = ROBE.node_tree; N = nt.nodes; Ln = nt.links; bsdf = N['Principled BSDF']
src = bsdf.inputs['Base Color'].links[0].from_socket
at = N.new('ShaderNodeAttribute'); at.attribute_name = 'nghi'
sx = N.new('ShaderNodeSeparateXYZ'); Ln.new(at.outputs['Vector'], sx.inputs[0])
X, Y, Z = sx.outputs[0], sx.outputs[1], sx.outputs[2]
def mth(op, a, b=None, c=None):
    n = N.new('ShaderNodeMath'); n.operation = op
    for k, v in enumerate((a, b, c)):
        if v is None: continue
        if isinstance(v, (int, float)): n.inputs[k].default_value = v
        else: Ln.new(v, n.inputs[k])
    return n.outputs[0]
dx, dz = (cB - cA).x, (cB - cA).z; ln_ = math.hypot(dx, dz); ux, uz = dx / ln_, dz / ln_
# khoảng cách vuông góc tới đường cổ chéo
# khoảng cách có dấu tới đường vạt áo: âm = phía vạt trái (vạt ngoài), dương = phía vạt phải (vạt trong)
sd = mth('SUBTRACT', mth('MULTIPLY', mth('SUBTRACT', X, cA.x), uz), mth('MULTIPLY', mth('SUBTRACT', Z, cA.z), ux))
front = mth('LESS_THAN', Y, neck.y - 0.02)
zr = mth('MULTIPLY', mth('GREATER_THAN', Z, cB.z), mth('LESS_THAN', Z, cA.z + 0.03))
fm = mth('MULTIPLY', front, zr)
# nẹp cổ sẫm chạy dọc mép vạt ngoài (giao lĩnh)
lapel = mth('MULTIPLY', fm, mth('MULTIPLY', mth('LESS_THAN', sd, 0.0), mth('GREATER_THAN', sd, -0.034)))
# cổ áo lót trắng chỉ lộ một khe nhỏ ở chữ V gần cổ
inner = mth('MULTIPLY', fm, mth('MULTIPLY', mth('MULTIPLY', mth('GREATER_THAN', sd, 0.0), mth('LESS_THAN', sd, 0.016)),
                                   mth('GREATER_THAN', Z, neck.z - 0.075)))
rr = mth('SQRT', mth('ADD', mth('POWER', mth('SUBTRACT', X, neck.x), 2), mth('POWER', mth('SUBTRACT', Y, neck.y), 2)))
near = mth('LESS_THAN', rr, 0.095)
collar_back = mth('MULTIPLY', mth('GREATER_THAN', Z, neck.z - 0.045), near)
lapel = mth('MAXIMUM', lapel, collar_back)
inner = mth('MAXIMUM', inner, mth('MULTIPLY', mth('GREATER_THAN', Z, neck.z - 0.012), near))
beltm = mth('LESS_THAN', mth('ABSOLUTE', mth('SUBTRACT', Z, sp1.z - 0.015)), 0.026)
def mixc(fac, c1, c2):
    m = N.new('ShaderNodeMix'); m.data_type = 'RGBA'; Ln.new(fac, m.inputs[0])
    for idx, c in ((6, c1), (7, c2)):
        if isinstance(c, tuple): m.inputs[idx].default_value = (*c, 1)
        else: Ln.new(c, m.inputs[idx])
    return m.outputs[2]
c = mixc(lapel, src, (0.012, 0.011, 0.012))
c = mixc(inner, c, (0.70, 0.66, 0.57))
c = mixc(beltm, c, (0.02, 0.018, 0.016))
# nếp nhăn vải lớn (bump) để áo không trơn như da
nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 9; nz.inputs['Detail'].default_value = 3
if 'Distortion' in nz.inputs: nz.inputs['Distortion'].default_value = 1.5
tco = N.new('ShaderNodeTexCoord'); Ln.new(tco.outputs['Object'], nz.inputs['Vector'])
bp2 = N.new('ShaderNodeBump'); bp2.inputs['Strength'].default_value = 0.45; bp2.inputs['Distance'].default_value = 0.01
Ln.new(nz.outputs['Fac'], bp2.inputs['Height'])
oldn = bsdf.inputs['Normal'].links[0].from_node if bsdf.inputs['Normal'].links else None
if oldn: Ln.new(oldn.outputs['Normal'], bp2.inputs['Normal'])
Ln.new(bp2.outputs['Normal'], bsdf.inputs['Normal'])
Ln.new(c, bsdf.inputs['Base Color'])

# ---------------- khăn: các vòng vải quấn chồng (khăn xếp/khăn vấn) ----------------
top = max((mw @ v.co).z for v in h.data.vertices if h.vertex_groups['body'].index in [g.group for g in v.groups])
hc = Vector((headb.x, headb.y + 0.005, 0))
# khăn vấn: vỏ bám theo hình đầu, có các lằn vải quấn ngang
khan = dup(h, 'khan')
bm = bmesh.new(); bm.from_mesh(khan.data); deform = bm.verts.layers.deform.verify()
bi = khan.vertex_groups['body'].index
def zcut(p):
    return top - 0.068 - 0.035 * max(0.0, (p.y - headb.y) / 0.1)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if bi not in v[deform] or (mw @ v.co).z < zcut(mw @ v.co)
                           or abs((mw @ v.co).x - headb.x) > 0.11], context='VERTS')
bm.normal_update()
for v in bm.verts:
    p = mw @ v.co
    dz = p.z - zcut(p)
    # lằn quấn chéo nhẹ (khăn vấn xếp nếp), dày hơn ở viền dưới
    rid = 0.5 + 0.5 * math.cos((dz + 0.25 * (p.x - headb.x)) * 2 * math.pi / 0.017)
    v.co += v.normal * (0.012 + 0.007 * rid ** 3 + 0.006 * max(0, 0.02 - dz) / 0.02)
bm.to_mesh(khan.data); bm.free()
khan.data.materials.clear(); khan.data.materials.append(KHAN)
sk = khan.modifiers.new('day', 'SOLIDIFY'); sk.thickness = 0.006; sk.offset = -1
sbk = khan.modifiers.new('min', 'SUBSURF'); sbk.levels = 1; sbk.render_levels = 2
for p_ in khan.data.polygons:
    p_.use_smooth = True
# tóc mai đen lộ dưới khăn: phủ vùng da đầu
hair = dup(h, 'toc')
bm = bmesh.new(); bm.from_mesh(hair.data); deform = bm.verts.layers.deform.verify()
sc = hair.vertex_groups['scalp'].index if 'scalp' in hair.vertex_groups else -1
hb = hair.vertex_groups['body'].index
kill = []
for v in bm.verts:
    p = mw @ v.co
    g = v[deform]
    if hb not in g or p.z < headb.z + 0.035 or (p.y < headb.y - 0.06 and p.z < top - 0.06) or (p.y < headb.y - 0.085):
        kill.append(v)
bmesh.ops.delete(bm, geom=kill, context='VERTS'); bm.normal_update()
for v in bm.verts:
    v.co += v.normal * 0.004
bm.to_mesh(hair.data); bm.free()
hair.data.materials.clear(); hair.data.materials.append(HAIR)
bpy.data.objects.remove(hair)  # khăn đã phủ kín; bỏ lớp tóc để khỏi lộ mép răng cưa

# mắt: nếu chưa có gói tài nguyên thì làm mắt từ hình cầu hướng nhìn xuống bàn
# (helper-l-eye / helper-r-eye nằm sẵn trong lưới gốc)
def eye_from_helper(gname, nm):
    o = dup(h, nm)
    bm = bmesh.new(); bm.from_mesh(o.data); deform = bm.verts.layers.deform.verify()
    gi = o.vertex_groups[gname].index
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if gi not in v[deform]], context='VERTS')
    bm.to_mesh(o.data); bm.free()
    m = bpy.data.materials.new(nm); m.use_nodes = True; N = m.node_tree.nodes; L = m.node_tree.links
    b = N['Principled BSDF']; b.inputs['Roughness'].default_value = 0.05
    if 'Coat Weight' in b.inputs:
        b.inputs['Coat Weight'].default_value = 1.0
    # mống mắt: gradient theo hướng nhìn (trục -Y của mắt)
    tc = N.new('ShaderNodeTexCoord')
    ctr = sum((v.co for v in o.data.vertices), Vector()) / max(1, len(o.data.vertices))
    vm = N.new('ShaderNodeVectorMath'); vm.operation = 'SUBTRACT'; vm.inputs[1].default_value = ctr
    L.new(tc.outputs['Object'], vm.inputs[0])
    nrm = N.new('ShaderNodeVectorMath'); nrm.operation = 'NORMALIZE'; L.new(vm.outputs[0], nrm.inputs[0])
    dot = N.new('ShaderNodeVectorMath'); dot.operation = 'DOT_PRODUCT'
    look = Vector((0, -0.85, -0.5)).normalized()
    dot.inputs[1].default_value = look
    L.new(nrm.outputs[0], dot.inputs[0])
    rp = N.new('ShaderNodeValToRGB'); r = rp.color_ramp
    r.elements[0].position = 0.80; r.elements[0].color = (0.85, 0.82, 0.78, 1)
    r.elements[1].position = 0.83; r.elements[1].color = (0.12, 0.06, 0.03, 1)
    e = r.elements.new(0.94); e.color = (0.07, 0.035, 0.02, 1)
    e = r.elements.new(0.955); e.color = (0.005, 0.004, 0.004, 1)
    L.new(dot.outputs['Value'], rp.inputs[0]); L.new(rp.outputs[0], b.inputs['Base Color'])
    o.data.materials.clear(); o.data.materials.append(m)
    for p in o.data.polygons:
        p.use_smooth = True
    return o
if not HAS_EYES:
    eye_from_helper('helper-l-eye', 'mat_trai'); eye_from_helper('helper-r-eye', 'mat_phai')

# ---------------- tư thế: ngồi xếp bằng trên chiếu, cúi viết ----------------
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')
PB = rig.pose.bones
for pb in PB:
    pb.rotation_mode = 'XYZ'
def R(n, x=0, y=0, z=0):
    PB[n].rotation_euler = Euler((math.radians(x), math.radians(y), math.radians(z)), 'XYZ')
POSE = {
    'thigh_l': (-80, 0, -40), 'thigh_r': (-80, 0, 40),
    'calf_l': (140, 0, 0), 'calf_r': (140, 0, 0),
    'foot_l': (-20, 0, 0), 'foot_r': (-20, 0, 0),
    'spine_01': (14, 0, 0), 'spine_02': (8, 0, 0), 'spine_03': (6, 0, 0),
    'neck_01': (8, 0, 0), 'head': (9, 0, -4),
    'hand_r': (0, 0, 0), 'hand_l': (0, 0, 0),
    'index_01_r': (0, 0, 30), 'index_02_r': (0, 0, 30), 'middle_01_r': (0, 0, 40), 'middle_02_r': (0, 0, 40),
    'ring_01_r': (0, 0, 60), 'ring_02_r': (0, 0, 60), 'pinky_01_r': (0, 0, 65), 'pinky_02_r': (0, 0, 60),
    'thumb_01_r': (0, 20, 10), 'thumb_02_r': (0, 0, 20),
    'index_01_l': (0, 0, -10), 'middle_01_l': (0, 0, -12), 'ring_01_l': (0, 0, -15), 'pinky_01_l': (0, 0, -18),
}
import json
if os.environ.get('POSE_JSON'):
    POSE.update(json.loads(os.environ['POSE_JSON']))
for n, (x, y, z) in POSE.items():
    if n in PB and not os.environ.get('NOPOSE'):
        R(n, x, y, z)
bpy.ops.object.mode_set(mode='OBJECT')

bpy.context.view_layer.update()
# hạ cả người xuống để phần thấp nhất chạm chiếu
dg = bpy.context.evaluated_depsgraph_get()
he = h.evaluated_get(dg)
minz = min((he.matrix_world @ v.co).z for v in he.data.vertices)
rig.location.z -= minz - 0.015
bpy.context.view_layer.update()
P = rig.matrix_world @ rig.pose.bones['pelvis'].head
DESK_H = float(os.environ.get('DESK_H', 0.30))
dc = Vector((P.x, P.y - 0.40, DESK_H))
# IK hai tay: tay phải cầm bút trên giấy, tay trái giữ mép giấy
def ik(arm, target, pole):
    e = bpy.data.objects.new('ik_' + arm, None); bpy.context.collection.objects.link(e); e.location = target
    pl = bpy.data.objects.new('pole_' + arm, None); bpy.context.collection.objects.link(pl); pl.location = pole
    c = rig.pose.bones['lowerarm_' + arm].constraints.new('IK'); c.target = e; c.chain_count = 2
    c.pole_target = pl; c.pole_angle = math.radians(-90 if arm == 'l' else -90)
    return e, c
RT = Vector((P.x - 0.07, dc.y + 0.0, DESK_H + 0.075))
LT = Vector((P.x + 0.19, dc.y + 0.04, DESK_H + 0.05))
ikr, cr_ = ik('r', RT, Vector((P.x - 0.6, P.y + 0.1, P.z + 0.15)))
ikl, cl_ = ik('l', LT, Vector((P.x + 0.6, P.y + 0.1, P.z + 0.15)))
for n, v in json.loads(os.environ.get('POLE', '{}')).items():
    (cr_ if n == 'r' else cl_).pole_angle = math.radians(v)

# chuyển động viết: đích IK tay phải đi theo nét chữ (cột dọc từ trên xuống), đầu gật nhẹ, thở
def key_motion():
    for f in range(F0 - 2, F1 + 3):
        t = f / FPS
        stroke = (t * 1.3) % 1.0
        col = int(t * 1.3 / 3) % 4
        ikr.location = RT + Vector((-0.0 + 0.05 * col * 0 + 0.006 * math.sin(t * 9), 0.05 - 0.10 * ((t * 1.3 / 3) % 1.0), 0.004 * (1 - math.cos(stroke * 2 * math.pi))))
        ikr.keyframe_insert('location', frame=f)
        s2 = math.sin(t * 2 * math.pi * 0.27)
        hx, hy, hz = POSE['head']; PB['head'].rotation_euler = Euler((math.radians(hx + 1.5 * s2), math.radians(hy), math.radians(hz)))
        sx, sy, sz = POSE['spine_03']; PB['spine_03'].rotation_euler = Euler((math.radians(sx + 0.8 * math.sin(t * 2 * math.pi * 0.25)), math.radians(sy), math.radians(sz)))
        for n in ('head', 'spine_03'):
            PB[n].keyframe_insert('rotation_euler', frame=f)
if not os.environ.get('NOPOSE'):
    key_motion()
bpy.context.scene.frame_set(F0)
bpy.context.view_layer.update()

# ---------------- bút lông trong tay phải ----------------
def hand_point():
    dg = bpy.context.evaluated_depsgraph_get()
    pbm = rig.pose.bones['index_02_r']
    return rig.matrix_world @ pbm.tail, rig.matrix_world @ rig.pose.bones['thumb_02_r'].tail
ip, tp = hand_point()
grip = (ip + tp) / 2
tipp = Vector((grip.x + 0.004, grip.y - 0.012, DESK_H + 0.0035))
axis = (grip - tipp).normalized()
L_B = 0.17
mid = tipp + axis * (0.03 + L_B / 2)
bpy.ops.mesh.primitive_cylinder_add(radius=0.0042, depth=L_B, location=mid, vertices=16)
brush = bpy.context.active_object
brush.rotation_euler = axis.to_track_quat('Z', 'Y').to_euler()
brush.data.materials.append(mat_basic('tre', (0.55, 0.42, 0.22), 0.4))
bpy.ops.mesh.primitive_cone_add(radius1=0.0055, radius2=0.0004, depth=0.03, location=tipp + axis * 0.015, vertices=16)
tip = bpy.context.active_object; tip.rotation_euler = (-axis).to_track_quat('Z', 'Y').to_euler(); tip.data.materials.append(INK)
bpy.context.view_layer.update()
for o in (brush, tip):
    mwb = o.matrix_world.copy(); o.parent = rig; o.parent_type = 'BONE'; o.parent_bone = 'hand_r'
    bpy.context.view_layer.update(); o.matrix_world = mwb

# ---------------- bàn thấp, giấy, nghiên mực, chiếu, lều ----------------
desk_top = DESK_H
def box(name, loc, size, mat):
    bpy.ops.mesh.primitive_cube_add(location=loc); o = bpy.context.active_object
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2); o.name = name; o.data.materials.append(mat)
    bv = o.modifiers.new('bv', 'BEVEL'); bv.width = 0.004; bv.segments = 2
    bpy.ops.object.transform_apply(scale=True)
    return o
WOOD = mat_tex('go', 'go', 1.5, (0.55, 0.38, 0.25))
box('mat_ban', (dc.x, dc.y - 0.02, desk_top - 0.015), (0.7, 0.42, 0.03), WOOD)
for sx in (-1, 1):
    for sy in (-1, 1):
        box('chan', (dc.x + sx * 0.31, dc.y - 0.02 + sy * 0.17, (desk_top - 0.03) / 2), (0.04, 0.04, desk_top - 0.03), WOOD)
# giấy dó với chữ đã viết (vẽ bằng canvas PIL nếu có)
paper_m = mat_basic('giay', (0.86, 0.82, 0.70), 0.9, sheen=0.3)
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    W, Hh = 1024, 700
    im = Image.new('RGB', (W, Hh), (226, 214, 184)); dr = ImageDraw.Draw(im)
    import random; random.seed(3)
    for _ in range(3000):
        x, y = random.randrange(W), random.randrange(Hh); c = random.randint(200, 232)
        dr.point((x, y), (c, c - 8, c - 30))
    fnt = None
    for fp in glob.glob(os.path.expanduser('~/.fonts/*CJK*')) + glob.glob('/usr/share/fonts/**/*CJK*', recursive=True) + glob.glob('/usr/share/fonts/**/*Noto*Serif*', recursive=True):
        try:
            fnt = ImageFont.truetype(fp, 52); break
        except Exception:
            pass
    txt = '問治國之道何者為先人才為本'
    cols = 6
    k = 0
    for c in range(cols):
        x = W - 90 - c * 80
        for r in range(9):
            if k >= len(txt) * 3:
                break
            ch = txt[k % len(txt)]; k += 1
            if c == cols - 1 and r > 4:
                break
            if fnt:
                dr.text((x, 40 + r * 70), ch, font=fnt, fill=(18, 14, 12))
            else:
                dr.rectangle((x, 50 + r * 70, x + 40, 90 + r * 70), fill=(20, 16, 14))
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    pp = '/tmp/giay_si_tu.png'; im.save(pp)
    N = paper_m.node_tree.nodes; t = N.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(pp)
    paper_m.node_tree.links.new(t.outputs['Color'], N['Principled BSDF'].inputs['Base Color'])
except Exception as e:
    print('giấy không có chữ:', e)
bpy.ops.mesh.primitive_plane_add(size=1, location=(dc.x + 0.03, dc.y - 0.03, desk_top + 0.0012))
pap = bpy.context.active_object; pap.scale = (0.4, 0.28, 1); pap.rotation_euler.z = math.radians(180)
pap.data.materials.append(paper_m)
# nghiên mực đá
STONE = mat_tex('da', 'da', 2, (0.25, 0.25, 0.27))
box('nghien', (dc.x - 0.24, dc.y - 0.06, desk_top + 0.012), (0.09, 0.14, 0.024), STONE)
bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.004, location=(dc.x - 0.24, dc.y - 0.09, desk_top + 0.024))
bpy.context.active_object.data.materials.append(INK)
# đèn dầu đĩa đồng, ngọn lửa nhỏ, không chao kính
BRONZE = mat_basic('dong', (0.45, 0.30, 0.15), 0.35); BRONZE.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 1.0
lx, ly = dc.x + 0.27, dc.y + 0.1
bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.12, location=(lx, ly, desk_top + 0.06)); bpy.context.active_object.data.materials.append(BRONZE)
bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.012, location=(lx, ly, desk_top + 0.125)); bpy.context.active_object.data.materials.append(BRONZE)
flame = mat_basic('lua', (1, 0.5, 0.15), 1); fn = flame.node_tree.nodes['Principled BSDF']
fn.inputs['Emission Color'].default_value = (1, 0.55, 0.18, 1); fn.inputs['Emission Strength'].default_value = 40
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.008, location=(lx, ly, desk_top + 0.142)); fo = bpy.context.active_object
fo.scale = (1, 1, 2.4); fo.data.materials.append(flame)
bpy.ops.object.light_add(type='POINT', location=(lx, ly, desk_top + 0.15)); L1 = bpy.context.active_object
L1.data.energy = 16; L1.data.color = (1, 0.62, 0.32); L1.data.shadow_soft_size = 0.015
# chiếu cói
RUSH = mat_tex('chieu', 'rom', 3, (0.95, 0.85, 0.6))
bpy.ops.mesh.primitive_plane_add(size=1, location=(pel.x, pel.y - 0.1, 0.002)); ch = bpy.context.active_object
ch.scale = (1.0, 1.6, 1); ch.data.materials.append(RUSH)
# nền đất sân thi
GROUND = mat_tex('dat', 'dat', 6)
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0)); bpy.context.active_object.data.materials.append(GROUND)
# lều vải phía sau và hai bên (sĩ tử tự mang lều chõng vào trường thi)
TENT = mat_tex('leu', 'rom', 2, (0.75, 0.62, 0.45))
for sx in (-1, 1):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(pel.x + sx * 0.9, pel.y + 0.2, 0.9), rotation=(0, math.radians(90 + sx * 8), 0))
    o = bpy.context.active_object; o.scale = (1.9, 2.2, 1); o.data.materials.append(TENT)
    s = o.modifiers.new('d', 'SOLIDIFY'); s.thickness = 0.004
bpy.ops.mesh.primitive_plane_add(size=1, location=(pel.x, pel.y + 0.85, 0.9), rotation=(math.radians(90), 0, 0))
o = bpy.context.active_object; o.scale = (1.9, 1.9, 1); o.data.materials.append(TENT)
# lều phía xa (nền) để thấy cả trường thi qua cửa lều: vài lều nhỏ bên ngoài
for i in range(8):
    x = pel.x - 3 + i * 0.9; y = pel.y - 3.2 - (i % 3) * 0.6
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.6, depth=0.9, location=(x, y, 0.45), rotation=(0, 0, math.radians(45)))
    bpy.context.active_object.data.materials.append(TENT)

# ---------------- ánh sáng, máy quay ----------------
sc = bpy.context.scene
W0 = bpy.data.worlds.new('w'); sc.world = W0; W0.use_nodes = True
env = W0.node_tree.nodes.new('ShaderNodeTexEnvironment')
hdr = os.path.join(CL, 'troi_chieu.hdr')
if os.path.exists(hdr):
    env.image = bpy.data.images.load(hdr)
    W0.node_tree.links.new(env.outputs['Color'], W0.node_tree.nodes['Background'].inputs['Color'])
W0.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.6
bpy.ops.object.light_add(type='AREA', location=(pel.x - 1.4, pel.y - 1.6, 1.8)); key = bpy.context.active_object
key.data.energy = 90; key.data.size = 1.2; key.data.color = (1, 0.93, 0.85)
key.rotation_euler = (Vector((pel.x, pel.y, 0.8)) - key.location).to_track_quat('-Z', 'Y').to_euler()
bpy.ops.object.light_add(type='AREA', location=(pel.x + 1.0, pel.y + 0.6, 1.6)); rim = bpy.context.active_object
rim.data.energy = 60; rim.data.size = 0.6; rim.data.color = (0.85, 0.9, 1)
rim.rotation_euler = (Vector((pel.x, pel.y, 0.9)) - rim.location).to_track_quat('-Z', 'Y').to_euler()

face = bone_head('head') + Vector((0, -0.05, 0.02))
face = rig.matrix_world @ rig.pose.bones['head'].head + Vector((0, -0.06, 0.0))
target = (face * 0.6 + grip * 0.4) + Vector((0, 0, 0.025))
bpy.ops.object.camera_add(); cam = bpy.context.active_object; sc.camera = cam
cam.data.lens = 42; cam.data.dof.use_dof = True; cam.data.dof.aperture_fstop = 2.8
emp = bpy.data.objects.new('nhin', None); sc.collection.objects.link(emp); emp.location = target
fe = bpy.data.objects.new('mat_nhin', None); sc.collection.objects.link(fe); fe.location = face * 0.8 + grip * 0.2
cam.data.dof.focus_object = fe
tr = cam.constraints.new('TRACK_TO'); tr.target = emp; tr.track_axis = 'TRACK_NEGATIVE_Z'; tr.up_axis = 'UP_Y'
# máy quay trượt chậm vòng từ trước-trái sang trước-phải
for f in range(F0 - 2, F1 + 3):
    t = (f - 1) / FPS
    a = math.radians(-20 + 4.0 * t)
    d = 1.2 - 0.012 * t
    cam.location = target + Vector((math.sin(a) * d, -math.cos(a) * d, 0.06 + 0.004 * t))
    cam.keyframe_insert('location', frame=f)

if os.environ.get('CAMV'):
    cam.constraints.clear(); cam.animation_data_clear()
    a = math.radians(float(os.environ['CAMV'])); cam.data.lens = 35
    dd = float(os.environ.get('CAMD', 3.2)); zz = float(os.environ.get('CAMZ', 0.7))
    cam.location = Vector((math.sin(a) * dd, -math.cos(a) * dd, zz + 0.1)); emp.location = Vector((0, 0, zz))
    cam.rotation_euler = (emp.location - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.engine = os.environ.get('ENGINE', 'CYCLES')
sc.cycles.device = 'CPU'
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6
w, hh = map(int, RES.split('x'))
sc.render.resolution_x, sc.render.resolution_y = w, hh
sc.render.fps = FPS
sc.view_settings.view_transform = 'AgX'
try:
    sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    pass
sc.render.film_transparent = False
if F0 == F1:
    sc.frame_set(F0); sc.render.filepath = OUT; bpy.ops.render.render(write_still=True)
else:
    os.makedirs(OUT, exist_ok=True)
    for f in range(F0, F1 + 1):
        sc.frame_set(f); sc.render.filepath = os.path.join(OUT, f'{f:04d}.png'); bpy.ops.render.render(write_still=True)
print('XONG', OUT)
