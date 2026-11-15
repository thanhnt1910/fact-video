#!/usr/bin/env bash
# Dựng video từ giọng đã chốt. Chạy trong thư mục chứa render.py:
#   bash dung.sh <thư mục wav giọng> <tên file ra.mp4>
# Ví dụ: bash dung.sh ../../assets/trader9x/MACD2/Iapetus Trader9x_MACD_XAUUSD_giong-nam.mp4
set -euo pipefail
V=$1; OUT=$2
T=$(python3 voice_tl.py "$V" info | awk '/tổng/{print $2}')
python3 voice_tl.py "$V" audio                      # voice.wav + voice_times.json
HALF=$(python3 -c "print(round($T/2,1))")
rm -f va.mp4 vb.mp4
python3 voice_tl.py "$V" render va.mp4 0 "$HALF" &
python3 voice_tl.py "$V" render vb.mp4 "$HALF" 9999
wait
python3 nhac.py "$T" music.wav
printf "file 'va.mp4'\nfile 'vb.mp4'\n" > l.txt
ffmpeg -y -v error -f concat -i l.txt -c copy v.mp4
ffmpeg -y -v error -i v.mp4 -i voice.wav -i music.wav -filter_complex \
 "[1:a]aformat=channel_layouts=stereo,asplit=2[v1][v2];[2:a]volume=0.22[m];[m][v1]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];[md][v2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
