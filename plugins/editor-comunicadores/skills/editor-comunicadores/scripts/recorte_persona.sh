#!/usr/bin/env bash
# Recorta a la persona del fondo en un tramo de video (texto detrás de la cabeza, fondos cambiados).
# Usa el modelo local de HyperFrames (u2net_human_seg, CPU, ~5 s por fotograma). Reanudable:
# procesa fotogramas hasta ~140 s por llamada; si dice SIGUE, vuelve a correr el mismo comando.
# Uso (desde la raíz, con el entorno cargado):
#   bash .herramientas/scripts/recorte_persona.sh <video> <inicio_s> <fin_s> <carpeta_trabajo> <salida.mov>
# Salida: ProRes 4444 con alfa, a los fotogramas por segundo del original. Tramos cortos (1–3 s): es lento.
set -euo pipefail
VID="${1:?video}"; INI="${2:?inicio}"; FIN="${3:?fin}"; DIR="${4:?carpeta}"; OUT="${5:?salida.mov}"
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$VID")
mkdir -p "$DIR/frames" "$DIR/recorte"
if [ -z "$(ls -A "$DIR/frames" 2>/dev/null)" ]; then
  ffmpeg -hide_banner -loglevel error -ss "$INI" -to "$FIN" -i "$VID" -vsync 0 "$DIR/frames/f%05d.png"
fi
T0=$(date +%s); TOTAL=$(ls "$DIR/frames" | wc -l); HECHOS=0
for f in "$DIR"/frames/*.png; do
  n=$(basename "$f")
  [ -f "$DIR/recorte/$n" ] && { HECHOS=$((HECHOS+1)); continue; }
  if [ $(( $(date +%s) - T0 )) -gt 140 ]; then echo "SIGUE: $HECHOS/$TOTAL fotogramas listos. Vuelve a correr el mismo comando."; exit 0; fi
  hyperframes remove-background "$f" -o "$DIR/recorte/$n" --device cpu --json >/dev/null
  HECHOS=$((HECHOS+1))
done
ffmpeg -hide_banner -loglevel error -y -framerate "$FPS" -i "$DIR/recorte/f%05d.png" -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le "$OUT"
echo "LISTO: $TOTAL fotogramas → $OUT"
