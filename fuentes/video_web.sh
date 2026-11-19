#!/bin/bash
# Prepara el vídeo final para la web: 720p ligero + subtítulos .vtt + póster.
# Uso: bash fuentes/video_web.sh …/Montaje/Angelito_Burlon_v2.mp4 …/Montaje/Angelito_Burlon_v2.srt
IN="${1:?mp4}"; SRT="${2:?srt}"; mkdir -p video
ffmpeg -v error -y -i "$IN" -vf "scale=1280:-2:flags=lanczos" -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 25 -preset slow \
  -c:a aac -b:a 128k -movflags +faststart video/angelito_burlon.mp4
ffmpeg -v error -y -i "$SRT" video/angelito_burlon.vtt
ffmpeg -v error -y -ss 60 -i "$IN" -frames:v 1 -vf "scale=1280:-2" -q:v 3 video/portada_video.jpg
