#!/bin/bash
# Descarga el modelo de transcripción (Whisper large-v3-turbo, ~1,6 GB) usando la conexión de esta Mac.
# Doble clic para ejecutar. Si se corta, vuelve a hacer doble clic: continúa donde quedó.
cd "$(dirname "$0")" || exit 1
DEST=".herramientas/whisper/ggml-large-v3-turbo.bin"
URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin"
mkdir -p .herramientas/whisper
echo ""
echo "Descargando el modelo de transcripción (~1,6 GB). Puede tardar unos minutos..."
echo ""
curl -L -C - --fail --progress-bar -o "$DEST.parcial" "$URL"
TAM=$(stat -f%z "$DEST.parcial" 2>/dev/null || echo 0)
if [ "$TAM" -gt 1500000000 ]; then
  mv "$DEST.parcial" "$DEST"
  echo ""
  echo "LISTO. El modelo quedó instalado. Ya puedes cerrar esta ventana."
else
  echo ""
  echo "La descarga no terminó ($TAM bytes). Vuelve a hacer doble clic en este archivo para continuar."
fi
echo ""
read -n 1 -s -r -p "Presiona cualquier tecla para cerrar."
