import json,sys,subprocess
import numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8")
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","assets/phan_tich/a.mp3","-f","s16le","-ac","1","-ar","16000","-"],capture_output=True,check=True).stdout,np.int16).astype(np.float32)/32768
seg,info=m.transcribe(x,language="vi",vad_filter=True)
out=[(round(s.start,1),round(s.end,1),s.text.strip()) for s in seg]
json.dump(out,open("assets/phan_tich/asr.json","w"),ensure_ascii=False,indent=0)
print(info.duration,len(out))
