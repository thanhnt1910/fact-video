#!/usr/bin/env bash
# Gửi kết quả về Telegram. Đọc ci_outputs.txt (video ngắn + bài ảnh) và ci_long.txt (video dài) trong thư mục hiện tại.
if [ -z "$TG_CHAT" ] && [ -f telegram_chat_id.txt ]; then TG_CHAT=$(cat telegram_chat_id.txt); fi
if [ -z "$TG_TOKEN" ] || [ -z "$TG_CHAT" ]; then
  echo "Chưa cài TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, bỏ qua bước gửi Telegram."
  exit 0
fi
api="https://api.telegram.org/bot${TG_TOKEN}"

# Chặn gửi bản bị tự kiểm tra báo LỖI (trừ khi FORCE_SEND=yes). Trả về 0 = bị chặn.
blocked() {
  local f="output/$1/$1_kiemtra_$2.json"
  [ "$FORCE_SEND" = "yes" ] && return 1
  [ -f "$f" ] || return 1
  python3 -c "import json,sys; sys.exit(0 if json.load(open('$f',encoding='utf-8')).get('ket_qua')=='loi' else 1)"
}
block_msg() {
  echo "Bỏ qua $1 ($2): tự kiểm tra báo lỗi (không gửi Telegram)"
}
# Gửi ảnh bìa dạng tệp (giữ nguyên chất lượng để tải lên YouTube/Facebook). Dùng: send_covers "chú thích" tệp1 tệp2 ...
send_covers() {
  local cap="$1"; shift
  local files=()
  for f in "$@"; do [ -f "$f" ] && files+=("$f"); done
  [ ${#files[@]} -eq 0 ] && return 0
  if [ ${#files[@]} -eq 1 ]; then
    curl -s -o /dev/null -w "Gửi ảnh bìa: %{http_code}\n" -F chat_id="$TG_CHAT" \
      -F document=@"${files[0]}" -F caption="$cap" "$api/sendDocument"
    return 0
  fi
  local media="[" args=() i=0
  for f in "${files[@]:0:10}"; do
    [ $i -gt 0 ] && media+=","
    if [ $i -eq $(( ${#files[@]} - 1 )) ] || [ $i -eq 9 ]; then
      media+="{\"type\":\"document\",\"media\":\"attach://f$i\",\"caption\":$(python3 -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$cap")}"
    else
      media+="{\"type\":\"document\",\"media\":\"attach://f$i\"}"
    fi
    args+=(-F "f$i=@$f")
    i=$((i+1))
  done
  media+="]"
  curl -s -o /dev/null -w "Gửi ảnh bìa: %{http_code}\n" -F chat_id="$TG_CHAT" -F media="$media" "${args[@]}" "$api/sendMediaGroup"
}
if [ -s ci_outputs.txt ]; then
  while read -r id || [ -n "$id" ]; do
    [ -z "$id" ] && continue
    if blocked "$id" ngan; then block_msg "$id" "video ngắn + bài ảnh" ngan; continue; fi
    if python3 da_gui.py check "$id" ngan; then echo "Bỏ qua $id (video ngắn): đã gửi trước đó, đặt GUI_LAI=yes nếu muốn gửi lại"; continue; fi
    mp4="output/$id/$id.mp4"
    cap="output/$id/${id}_caption.txt"
    title=$(python3 -c "import json,sys;print(json.load(open('scripts/$id.json',encoding='utf-8')).get('title',''))" 2>/dev/null)
    text="🎬 $id · $title — nội dung đăng ở tin ngay sau. Bài ảnh: Releases tag video-${id}${HAU_TO}"
    code=$(curl -s -o /dev/null -w "%{http_code}" \
      -F chat_id="$TG_CHAT" -F supports_streaming=true \
      -F video=@"$mp4" -F caption="$text" "$api/sendVideo")
    echo "Gửi $id: $code"
    [ "$code" = "200" ] && python3 da_gui.py mark "$id" ngan
    # thử nghiệm A/B (kế hoạch, mục Âm thanh C): bản cũ chỉ ảnh + giọng đọc một lượt
    if [ -f "output/$id/${id}_ban_cu.mp4" ]; then
      curl -s -o /dev/null -w "Gửi bản A/B $id: %{http_code}\n" -F chat_id="$TG_CHAT" -F supports_streaming=true \
        -F video=@"output/$id/${id}_ban_cu.mp4" \
        -F caption="🅰️ THỬ A/B $id — BẢN CŨ (chỉ ảnh + giọng đọc một lượt, không tiếng động). Video phía trên là BẢN MỚI. Đăng mỗi bản lên một nền tảng khác nhau (vd bản cũ TikTok, bản mới YouTube Shorts), sau 48 giờ so tỉ lệ xem quá 3 giây và thời gian xem trung bình." "$api/sendVideo"
    fi
    # tin thứ hai: đủ tiêu đề, caption, hashtag, tag, ghi chú để copy đăng ngay
    python3 tg_text.py "$cap" "📝 NỘI DUNG ĐĂNG $id (video ngắn)"
    # ảnh bìa: các phương án bìa video ngắn (thiếu thì dùng ảnh thumbnail)
    covers=$(ls output/$id/${id}_bia_*.jpg 2>/dev/null)
    [ -z "$covers" ] && covers="output/$id/${id}_thumbnail.jpg"
    send_covers "🖼️ Ảnh bìa video ngắn $id (chọn 1 phương án)" $covers
  done < ci_outputs.txt
fi
# video dài: bản xem trước nhẹ (giới hạn 50MB của Telegram) + link bản đầy đủ
if [ -s ci_long.txt ]; then
  while read -r id || [ -n "$id" ]; do
    [ -z "$id" ] && continue
    f="output/$id/${id}_dai.mp4"; [ -f "$f" ] || continue
    if blocked "$id" dai; then block_msg "$id" "video dài" dai; continue; fi
    if python3 da_gui.py check "$id" dai; then echo "Bỏ qua $id (video dài): đã gửi trước đó, đặt GUI_LAI=yes nếu muốn gửi lại"; continue; fi
    dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" < /dev/null)
    vb=$(python3 -c "print(max(300, int(44*8*1024/float('$dur') - 96)))")
    ffmpeg -nostdin -loglevel error -y -i "$f" -vf scale=1280:-2 -c:v libx264 -preset veryfast -b:v ${vb}k \
      -maxrate ${vb}k -bufsize $((vb*2))k -c:a aac -b:a 96k "output/$id/${id}_dai_tg.mp4"
    link="https://github.com/${GITHUB_REPOSITORY}/releases/tag/video-${id}${HAU_TO}"
    code=$(curl -s -o /dev/null -w "%{http_code}" -F chat_id="$TG_CHAT" -F supports_streaming=true \
      -F video=@"output/$id/${id}_dai_tg.mp4" \
      -F caption="🎬 VIDEO DÀI $id (bản xem trước 720p). Bản 1080p, ảnh bìa, phụ đề ($id.en_US.srt): $link" "$api/sendVideo")
    echo "Gửi video dài $id: $code"
    [ "$code" = "200" ] && python3 da_gui.py mark "$id" dai
    python3 tg_text.py "output/$id/${id}_dai_youtube.txt" "📝 NỘI DUNG ĐĂNG $id (video dài)"
    send_covers "🖼️ Ảnh bìa video dài $id: _dai_thumbnail = YouTube, _dai_thumbnail_fb = Facebook" \
      "output/$id/${id}_dai_thumbnail.jpg" "output/$id/${id}_dai_thumbnail_fb.jpg"
  done < ci_long.txt
fi
# Không gửi tin "chưa xong / lỗi / bị chặn" lên Telegram: Telegram chỉ nhận kết quả cuối cùng, mỗi video đúng một lần.
for f in ci_long_failed.txt ci_failed.txt ci_blocked.json; do [ -s "$f" ] && echo "(không gửi Telegram) $f: $(head -c 300 $f | tr '\n' ' ')"; done
exit 0
