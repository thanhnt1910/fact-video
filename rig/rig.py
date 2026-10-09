"""
Rig ảnh nhân vật (PNG tách nền) thành hoạt hình có khớp xương, xuất chuỗi khung hình PNG trong suốt.
Chạy bằng môi trường riêng có animated_drawings + mediapipe (xem workflow anim-demo.yml).

  python rig/rig.py <nhân_vật.png> <chuyển_động: dance|walk> <thư_mục_ra> [fps=30] [giây=6]

Các bước: MediaPipe tìm khớp (vai, khuỷu, cổ tay, hông, gối, cổ chân) -> tạo cấu hình nhân vật
-> AnimatedDrawings (Meta, MIT) bẻ lưới ảnh theo dữ liệu chuyển động -> PNG từng khung hình.
"""
import os
import shutil
import sys
from pathlib import Path

os.environ.setdefault("PYOPENGL_PLATFORM", "osmesa")

import numpy as np
import yaml
from PIL import Image

HERE = Path(__file__).resolve().parent
AD_EX = Path(os.environ.get("AD_DIR", HERE.parent / "AnimatedDrawings")) / "examples" / "config" / "retarget"


def detect_joints(rgba):
    """Trả về dict tên khớp -> (x, y) theo pixel (quy ước AnimatedDrawings)."""
    import mediapipe as mp
    w, h = rgba.size
    bg = Image.new("RGB", rgba.size, (255, 255, 255))
    bg.paste(rgba, mask=rgba.getchannel("A"))
    arr = np.array(bg)
    with mp.solutions.pose.Pose(static_image_mode=True, model_complexity=1, min_detection_confidence=0.3) as pose:
        res = pose.process(arr)
    if not res.pose_landmarks:
        raise RuntimeError("không tìm thấy dáng người trong ảnh")
    L = res.pose_landmarks.landmark
    P = mp.solutions.pose.PoseLandmark
    pt = lambda k: np.array([L[k].x * w, L[k].y * h])
    ls, rs, lh, rh = pt(P.LEFT_SHOULDER), pt(P.RIGHT_SHOULDER), pt(P.LEFT_HIP), pt(P.RIGHT_HIP)
    nose = pt(P.NOSE)
    hip = (lh + rh) / 2
    sh = (ls + rs) / 2
    j = {
        "root": hip, "hip": hip,
        "torso": sh + (hip - sh) * 0.15,
        "neck": sh + (nose - sh) * 0.55,
        "right_shoulder": rs, "right_elbow": pt(P.RIGHT_ELBOW), "right_hand": pt(P.RIGHT_WRIST),
        "left_shoulder": ls, "left_elbow": pt(P.LEFT_ELBOW), "left_hand": pt(P.LEFT_WRIST),
        "right_hip": rh, "right_knee": pt(P.RIGHT_KNEE), "right_foot": pt(P.RIGHT_ANKLE),
        "left_hip": lh, "left_knee": pt(P.LEFT_KNEE), "left_foot": pt(P.LEFT_ANKLE),
    }
    # giữ khớp trong khung ảnh
    return {k: (float(np.clip(v[0], 1, w - 2)), float(np.clip(v[1], 1, h - 2))) for k, v in j.items()}


PARENT = {"root": None, "hip": "root", "torso": "hip", "neck": "torso",
          "right_shoulder": "torso", "right_elbow": "right_shoulder", "right_hand": "right_elbow",
          "left_shoulder": "torso", "left_elbow": "left_shoulder", "left_hand": "left_elbow",
          "right_hip": "root", "right_knee": "right_hip", "right_foot": "right_knee",
          "left_hip": "root", "left_knee": "left_hip", "left_foot": "left_knee"}


def make_character(png, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    im = Image.open(png).convert("RGBA")
    # thêm lề để tay chân có chỗ cử động
    pad = int(max(im.size) * 0.08)
    canvas = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    canvas.paste(im, (pad, pad))
    j = detect_joints(canvas)
    canvas.save(out_dir / "texture.png")
    mask = canvas.getchannel("A").point(lambda a: 255 if a > 100 else 0)
    mask.save(out_dir / "mask.png")
    cfg = {"width": canvas.width, "height": canvas.height,
           "skeleton": [{"name": k, "parent": PARENT[k], "loc": [int(round(v[0])), int(round(v[1]))]}
                        for k, v in j.items()]}
    (out_dir / "char_cfg.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False))
    # ảnh kiểm tra khớp
    from PIL import ImageDraw
    ov = canvas.copy()
    d = ImageDraw.Draw(ov)
    for k, v in j.items():
        p = PARENT[k]
        if p:
            d.line([j[p], v], fill=(255, 0, 0, 255), width=4)
        d.ellipse([v[0] - 6, v[1] - 6, v[0] + 6, v[1] + 6], fill=(0, 255, 0, 255))
    ov.save(out_dir / "joints.png")
    return out_dir / "char_cfg.yaml"


def retarget_cfg(kind, work):
    if kind == "mixamo":
        return str(AD_EX / "mixamo_fff.yaml")
    # cmu_walk: dữ liệu CMU dùng Spine1/FingerBase; chân và tay chiếu theo mặt cắt dọc để thấy bước đi
    txt = (AD_EX / "mixamo_fff.yaml").read_text()
    txt = txt.replace("Spine2", "Spine1").replace("LeftInHandIndex", "LeftFingerBase").replace("RightInHandIndex", "RightFingerBase")
    cfg = yaml.load(txt, Loader=yaml.Loader)
    for g in cfg["bvh_projection_bodypart_groups"]:
        if g["name"] in ("Lower Limbs", "Upper Limbs"):
            g["method"] = "sagittal"
    p = work / "cmu_walk.yaml"
    p.write_text(yaml.dump(cfg))
    return str(p)


def render(png, motion, out_frames, fps=30, seconds=6.0):
    from animated_drawings import render as ad_render
    from animated_drawings.controller import video_render_controller as vrc

    out_frames = Path(out_frames)
    work = out_frames.parent / (out_frames.name + "_rig")
    if out_frames.exists():
        shutil.rmtree(out_frames)
    out_frames.mkdir(parents=True)
    char_cfg = make_character(png, work)
    mv = yaml.safe_load((HERE / "motions.yaml").read_text())[motion]
    motion_cfg = {
        "filepath": str(HERE / mv["bvh"]), "start_frame_idx": 0, "end_frame_idx": None,
        "groundplane_joint": "LeftFoot", "scale": mv["scale"], "up": mv["up"],
        "forward_perp_joint_vectors": [["LeftShoulder", "RightShoulder"], ["LeftUpLeg", "RightUpLeg"]],
    }
    (work / "motion.yaml").write_text(yaml.safe_dump(motion_cfg))
    mvc = {
        "scene": {"ANIMATED_CHARACTERS": [{"character_cfg": str(char_cfg), "motion_cfg": str(work / "motion.yaml"),
                                           "retarget_cfg": retarget_cfg(mv["retarget"], work)}]},
        "view": {"USE_MESA": True, "WINDOW_DIMENSIONS": [720, 900], "CLEAR_COLOR": [0.0, 0.0, 0.0, 0.0]},
        "controller": {"MODE": "video_render", "OUTPUT_VIDEO_PATH": str(work / "out.gif")},
    }
    (work / "mvc.yaml").write_text(yaml.safe_dump(mvc))

    state = {"i": 0, "k": 0, "src_fps": None}

    def process_frame(self, frame):
        if state["src_fps"] is None:
            state["src_fps"] = 1.0 / max(1e-3, getattr(self, "_dt", 0.01))
        i = state["i"]
        state["i"] += 1
        src = state["src_fps"]
        if int(i * fps / src) == int((i - 1) * fps / src) and i > 0:
            return
        if state["k"] >= int(seconds * fps):
            return
        import cv2
        rgba = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)
        Image.fromarray(rgba).save(out_frames / f"{state['k']:04d}.png")
        state["k"] += 1

    orig_init = vrc.GIFWriter.__init__

    def init(self, controller):
        orig_init(self, controller)
        self._dt = controller.delta_t

    vrc.GIFWriter.__init__ = init
    vrc.GIFWriter.process_frame = process_frame
    vrc.GIFWriter.cleanup = lambda self: None
    import contextlib
    import io
    with contextlib.redirect_stderr(io.StringIO()):
        ad_render.start(str(work / "mvc.yaml"))
    n = state["k"]
    # vòng lặp: nếu chuyển động ngắn hơn thời lượng cần, lặp lại khung hình
    files = sorted(out_frames.glob("*.png"))
    k = len(files)
    while k < int(seconds * fps) and files:
        shutil.copy(files[k % len(files)], out_frames / f"{k:04d}.png")
        k += 1
    print(f"{Path(png).name}: {motion} -> {k} khung hình ({n} khung gốc)")


def crop_frames(*dirs):
    """Cắt mọi khung hình (của mọi chuyển động của 1 nhân vật) theo cùng một khung bao,
    để kích thước và mặt đất giống nhau khi chuyển từ đi sang nhảy."""
    files = [f for d in dirs for f in sorted(Path(d).glob("*.png"))]
    box = None
    for f in files[::2]:
        b = Image.open(f).getchannel("A").getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    if not box:
        return
    for f in files:
        Image.open(f).crop(box).save(f)


def rig_all(jobs_json):
    """jobs.json: [{"png": ..., "out": thư_mục, "motions": {"walk": giây, "dance": giây}}]"""
    import json
    for job in json.loads(Path(jobs_json).read_text()):
        dirs = []
        for motion, secs in job["motions"].items():
            d = Path(job["out"]) / motion
            render(job["png"], motion, d, 30, secs)
            dirs.append(d)
        crop_frames(*dirs)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0].endswith(".json"):
        rig_all(a[0])
    else:
        render(a[0], a[1], a[2], int(a[3]) if len(a) > 3 else 30, float(a[4]) if len(a) > 4 else 6.0)
        crop_frames(a[2])
