import json,sys
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8")
seg,info=m.transcribe("assets/phan_tich/a.mp3",language="vi",vad_filter=True)
out=[(round(s.start,1),round(s.end,1),s.text.strip()) for s in seg]
json.dump(out,open("assets/phan_tich/asr.json","w"),ensure_ascii=False,indent=0)
print(info.duration,len(out))
