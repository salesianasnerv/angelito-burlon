#!/bin/bash
# Convierte los clips animados de Flow (Montaje/Video/Flow/renombrados) en bucles ligeros y mudos para la web.
# Uso: bash fuentes/clips_web.sh /ruta/a/renombrados
SRC="${1:?carpeta con clipNN.mp4}"
OUT=video/escenas; mkdir -p "$OUT"
for c in clip00 clip01a clip02 clip03a clip04a clip05a clip06a clip07a clip08a clip08b clip09a clip10a clip10b; do
  W=960; [ "$c" = clip00 ] && W=1280
  ffmpeg -v error -y -i "$SRC/$c.mp4" -an -t 7.9 \
    -vf "scale=$W:-2:flags=lanczos,fps=24" \
    -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 29 -preset slow -movflags +faststart "$OUT/$c.mp4"
done
