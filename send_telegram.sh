#!/usr/bin/env bash
# Gửi kết quả về Telegram. Đọc ci_outputs.txt (video ngắn + bài ảnh) và ci_long.txt (video dài) trong thư mục hiện tại.
if [ -z "$TG_CHAT" ] && [ -f telegram_chat_id.txt ]; then TG_CHAT=$(cat telegram_chat_id.txt); fi
if [ -z "$TG_TOKEN" ] || [ -z "$TG_CHAT" ]; then
  echo "Chưa cài TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, bỏ qua bước gửi Telegram."
  exit 0
fi
api="https://api.telegram.org/bot${TG_TOKEN}"
if [ -s ci_outputs.txt ]; then
  while read -r id || [ -n "$id" ]; do
    [ -z "$id" ] && continue
    mp4="output/$id/$id.mp4"
    cap="output/$id/${id}_caption.txt"
    text=$(head -c 950 "$cap" 2>/dev/null || echo "$id")
    curl -s -o /dev/null -w "Gửi $id: %{http_code}\n" \
      -F chat_id="$TG_CHAT" -F supports_streaming=true \
      -F video=@"$mp4" -F caption="$text" "$api/sendVideo"
    # bài đăng ảnh Facebook: album ảnh + bài viết để copy
    if [ -f "output/$id/${id}_post_1.jpg" ]; then
      media="["; args=(); k=0
      for f in $(ls output/$id/${id}_post_*.jpg | sort -V); do
        [ $k -gt 0 ] && media+=","
        media+="{\"type\":\"photo\",\"media\":\"attach://p$k\"}"
        args+=(-F "p$k=@$f"); k=$((k+1))
      done
      media+="]"
      curl -s -o /dev/null -F chat_id="$TG_CHAT" -F text="🖼️ BÀI ĐĂNG ẢNH ($id) — tải các ảnh dưới đây, đăng thành 1 bài nhiều ảnh trên Facebook" "$api/sendMessage"
      curl -s -o /dev/null -w "Ảnh bài đăng $id: %{http_code}\n" -F chat_id="$TG_CHAT" -F media="$media" "${args[@]}" "$api/sendMediaGroup"
      curl -s -o /dev/null -w "Bài viết $id: %{http_code}\n" -F chat_id="$TG_CHAT" \
        -F text="$(head -c 4000 output/$id/${id}_post.txt)" "$api/sendMessage"
    fi
    if [ -f "output/$id/${id}_thumbnail.jpg" ]; then
      curl -s -o /dev/null -F chat_id="$TG_CHAT" \
        -F document=@"output/$id/${id}_thumbnail.jpg" -F caption="Ảnh bìa $id" "$api/sendDocument"
    fi
  done < ci_outputs.txt
fi
# video dài: bản xem trước nhẹ (giới hạn 50MB của Telegram) + link bản đầy đủ
if [ -s ci_long.txt ]; then
  while read -r id || [ -n "$id" ]; do
    [ -z "$id" ] && continue
    f="output/$id/${id}_dai.mp4"; [ -f "$f" ] || continue
    dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" < /dev/null)
    vb=$(python3 -c "print(max(300, int(44*8*1024/float('$dur') - 96)))")
    ffmpeg -nostdin -loglevel error -y -i "$f" -vf scale=1280:-2 -c:v libx264 -preset veryfast -b:v ${vb}k \
      -maxrate ${vb}k -bufsize $((vb*2))k -c:a aac -b:a 96k "output/$id/${id}_dai_tg.mp4"
    link="https://github.com/${GITHUB_REPOSITORY}/releases/tag/video-${id}"
    curl -s -o /dev/null -w "Gửi video dài $id: %{http_code}\n" -F chat_id="$TG_CHAT" -F supports_streaming=true \
      -F video=@"output/$id/${id}_dai_tg.mp4" \
      -F caption="🎬 VIDEO DÀI $id (bản xem trước 720p). Bản 1080p để đăng: $link" "$api/sendVideo"
    curl -s -o /dev/null -F chat_id="$TG_CHAT" -F document=@"output/$id/${id}_dai_thumbnail.jpg" \
      -F caption="Ảnh bìa YouTube $id" "$api/sendDocument"
    [ -f "output/$id/${id}_dai_thumbnail_fb.jpg" ] && curl -s -o /dev/null -F chat_id="$TG_CHAT" \
      -F document=@"output/$id/${id}_dai_thumbnail_fb.jpg" -F caption="Ảnh bìa FACEBOOK $id (chữ ở giữa, không bị cắt)" "$api/sendDocument"
    curl -s -o /dev/null -F chat_id="$TG_CHAT" -F text="$(head -c 4000 output/$id/${id}_dai_youtube.txt)" "$api/sendMessage"
    if [ -f "output/$id/${id}_dai_youtube_en.txt" ]; then
      curl -s -o /dev/null -F chat_id="$TG_CHAT" -F text="🌐 BẢN TIẾNG ANH $id (dán vào mục Phụ đề → Tiếng Anh):
$(head -c 3800 output/$id/${id}_dai_youtube_en.txt)" "$api/sendMessage"
    fi
    for srt in output/$id/${id}_dai_vi.srt output/$id/${id}_dai_en.srt; do
      [ -f "$srt" ] && curl -s -o /dev/null -F chat_id="$TG_CHAT" -F document=@"$srt" \
        -F caption="Phụ đề $(basename $srt)" "$api/sendDocument"
    done
  done < ci_long.txt
fi
if [ -s ci_long_failed.txt ]; then
  curl -s -o /dev/null -F chat_id="$TG_CHAT" \
    -F text="⏳ Video dài chưa xong: $(tr '\n' ' ' < ci_long_failed.txt)— có thể Gemini hết lượt hôm nay, máy sẽ tự thử lại sáng mai." "$api/sendMessage"
fi
if [ -s ci_failed.txt ]; then
  msg="⚠️ Dựng lỗi: $(tr '\n' ' ' < ci_failed.txt). Xem log: ${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"
  curl -s -o /dev/null -F chat_id="$TG_CHAT" -F text="$msg" "$api/sendMessage"
fi

