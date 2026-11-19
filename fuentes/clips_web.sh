#!/bin/bash
# Convierte los clips animados de Flow (Montaje/Video/Flow/renombrados) en bucles ligeros, mudos y SIN SALTO para la web.
# Truco del bucle: el clip empieza en el segundo F y sus últimos F segundos se funden con el principio (0..F),
# así el último fotograma coincide con el primero y al repetirse no se nota el corte.
# Uso: bash fuentes/clips_web.sh /ruta/a/renombrados
SRC="${1:?carpeta con clipNN.mp4}"
OUT=video/escenas; mkdir -p "$OUT"; F=1.5
for c in clip00 clip01a clip02 clip03a clip04a clip05a clip06a clip07a clip08a clip08b clip09a clip10a clip10b; do
  W=960; [ "$c" = clip00 ] && W=1280
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC/$c.mp4"); D=$(python3 -c "print(min(float('$D'),7.9))")
  L=$(python3 -c "print(round($D-$F,3))"); OFF=$(python3 -c "print(round($D-2*$F,3))")
  ffmpeg -v error -y -i "$SRC/$c.mp4" -an -filter_complex \
    "[0:v]scale=$W:-2:flags=lanczos,fps=24,format=yuv420p,split[a][b];[a]trim=$F:$D,setpts=PTS-STARTPTS[cuerpo];[b]trim=0:$F,setpts=PTS-STARTPTS[inicio];[cuerpo][inicio]xfade=transition=fade:duration=$F:offset=$OFF[v]" \
    -map "[v]" -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 29 -preset slow -movflags +faststart "$OUT/$c.mp4"
done
