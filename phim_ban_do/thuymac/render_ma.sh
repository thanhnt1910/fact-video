#!/bin/bash
# Dựng một tập: hai tiến trình song song, ghép với âm thanh
cd /tmp/gen/bd
for k in "$@"; do
  N=$(python3 -c "import dai_$k as V;print(int(V.TOTAL*24))"); H=$((N/2))
  python3 dai_$k.py render out/${k}_p1.mp4 0 $H 24 > out/${k}_r1.log 2>&1 &
  python3 dai_$k.py render out/${k}_p2.mp4 $H $N 24 > out/${k}_r2.log 2>&1 &
  wait
  printf "file '${k}_p1.mp4'\nfile '${k}_p2.mp4'\n" > out/l_$k.txt
  ffmpeg -y -loglevel error -f concat -safe 0 -i out/l_$k.txt -i out/am_$k.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out/${k}_thuymac_dai.mp4 && rm -f out/${k}_p1.mp4 out/${k}_p2.mp4 out/am_$k.wav
  echo "xong $k $(date +%T)"
done
