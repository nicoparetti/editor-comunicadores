#!/bin/bash
# Descarga los videos de referencia listados en 2_Referencias/links.txt usando la conexión de esta Mac.
# Un link por línea; opcional, después del link, un nombre para la carpeta:  https://...  reel-fulano
# Doble clic para ejecutar. Los videos son solo para estudiar el estilo, nunca para republicar.
cd "$(dirname "$0")" || exit 1
M=".herramientas/mac"
xattr -d com.apple.quarantine "$M/yt-dlp_macos" "$M/ffmpeg" 2>/dev/null
LINKS="2_Referencias/links.txt"
[ -f "$LINKS" ] || { echo "No encuentro $LINKS"; read -n 1 -s -r -p "Presiona una tecla para cerrar."; exit 1; }
OK=0; FALLO=0
while read -r URL NOMBRE; do
  case "$URL" in ""|\#*) continue ;; esac
  [ -n "$NOMBRE" ] || NOMBRE="%(uploader_id,uploader|ref)s-%(id)s"
  echo ""; echo "→ $URL"
  OPC=(--ffmpeg-location "$M/ffmpeg" -f "bv*[height<=1920][ext=mp4]+ba[ext=m4a]/bv*+ba/b" --merge-output-format mp4
       --no-playlist --write-info-json --no-overwrites -o "2_Referencias/$NOMBRE/video.%(ext)s")
  if "$M/yt-dlp_macos" "${OPC[@]}" "$URL"; then OK=$((OK+1))
  else
    echo "   Reintentando con la sesión de Chrome (para Instagram o videos que piden iniciar sesión)..."
    if "$M/yt-dlp_macos" "${OPC[@]}" --cookies-from-browser chrome "$URL"; then OK=$((OK+1)); else FALLO=$((FALLO+1)); echo "   No se pudo descargar: $URL"; fi
  fi
done < "$LINKS"
echo ""; echo "LISTO: $OK descargados, $FALLO con problemas. Los videos están en 2_Referencias/."
echo "Cuando quieras, vacía links.txt (los ya descargados no se repiten)."
read -n 1 -s -r -p "Presiona cualquier tecla para cerrar."
