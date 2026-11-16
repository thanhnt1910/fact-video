"""Giãn dòng thời gian video theo độ dài giọng đọc thật."""
import json, wave, sys, subprocess, os
from pathlib import Path
import numpy as np
import render as R

PLAN = {
 "intro": [(0.3, ["b_intro"])], "card1": [(0.2, ["card1_1"])],
 "p1": [(0.2, ["b_p1_1"]), (3.5, ["b_p1_2"]), (10.5, ["b_p1_3", "b_p1_4"])], "card2": [(0.2, ["card2n"])],
 "p2": [(0.0, ["b_t1"]), (7.0, ["b_app1"]), (13.0, ["b_t2"]), (19.0, ["b_app2"]), (25.0, ["b_t3"]), (31.0, ["b_sq1"]), (37.0, ["b_sq2", "b_sq2b"]),
        (43.0, ["b_t4"]), (49.0, ["b_w1"]), (55.0, ["b_w2"]), (60.0, ["b_t5"]), (66.0, ["b_r1"]), (72.0, ["b_r2", "b_r2b"]),
        (77.0, ["b_sq3", "b_sq3b"]), (84.0, ["now1", "b_now1b"]), (89.0, ["b_now2"]), (94.0, ["b_now3"])],
 "check": [(0.8, ["b_c1"]), (1.7, ["b_c2"]), (2.6, ["b_c3"]), (3.5, ["b_c4"]), (4.4, ["check_5"]), (5.6, ["b_c6"])],
 "outro": [(0.4, ["b_outro"])],
}
GAP, TAIL = 0.25, 0.5

def wav_dur(p):
    with wave.open(str(p)) as w: return w.getnframes() / w.getframerate()

def build(vdir):
    old_start = R.starts(); scenes = []   # (name, new_start, new_dur, old_knots, new_knots)
    clips = []                             # (new_time, path)
    t_new = 0.0
    for name, du in R.SC:
        segs = PLAN[name]
        ok = [0.0]; nk = [0.0]
        for i, (knot, ids) in enumerate(segs):
            # lead/gap before this knot keeps old length
            nk.append(nk[-1] + (knot - ok[-1])); ok.append(knot)
            end_old = segs[i + 1][0] if i + 1 < len(segs) else du
            durs = [wav_dur(Path(vdir) / f"{x}.wav") for x in ids]
            need = sum(durs) + GAP * (len(durs) - 1) + TAIL
            span = max(end_old - knot, need)
            tt = t_new + nk[-1] + 0.08
            for x, d_ in zip(ids, durs):
                clips.append((tt, Path(vdir) / f"{x}.wav")); tt += d_ + GAP
            nk.append(nk[-1] + span); ok.append(end_old)
        scenes.append((name, t_new, nk[-1], ok, nk))
        t_new += nk[-1]
    return scenes, clips, t_new, old_start

def old_time(scenes, old_start, gt):
    for name, s0, du, ok, nk in scenes:
        if gt < s0 + du or name == scenes[-1][0]:
            tn = min(gt - s0, du - 1e-3)
            to = float(np.interp(tn, nk, ok))
            return old_start[name] + min(to, dict(R.SC)[name] - 1e-3)

if __name__ == "__main__":
    vdir = sys.argv[1]; mode = sys.argv[2]
    scenes, clips, T, old_start = build(vdir)
    if mode == "info":
        print("tổng", round(T, 1)); [print(n, round(s, 1), round(d, 1)) for n, s, d, _, _ in scenes]
    elif mode == "audio":
        sr = 44100; buf = np.zeros(int((T + 1) * sr))
        for t0, p in clips:
            with wave.open(str(p)) as w:
                a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
            i = int(t0 * sr); buf[i:i + len(a)] += a
        buf = buf[:int(T * sr)]
        with wave.open("voice.wav", "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(buf, -1, 1) * 32767).astype("<i2").tobytes())
        json.dump([(round(t, 2), p.stem) for t, p in clips], open("voice_times.json", "w"), indent=0)
        print("voice.wav", round(T, 2))
    elif mode == "render":
        out, a, b = sys.argv[3], float(sys.argv[4]), min(float(sys.argv[5]), T)
        p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{R.W}x{R.H}", "-r", str(R.FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", out + ".tmp.mp4"], stdin=subprocess.PIPE)
        for i in range(int(round(a * R.FPS)), int(round(b * R.FPS))):
            p.stdin.write(R.frame(old_time(scenes, old_start, i / R.FPS)).tobytes())
        p.stdin.close()
        if p.wait() == 0: os.rename(out + ".tmp.mp4", out)
