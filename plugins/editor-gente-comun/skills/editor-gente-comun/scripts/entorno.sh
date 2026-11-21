#!/usr/bin/env bash
# Entorno de herramientas de editor-gente-comun. Uso, desde la raíz de la carpeta de trabajo:
#   source .herramientas/scripts/entorno.sh
# Cada llamada de shell es nueva: hay que cargarlo en cada comando que use las herramientas.
_EN_SCRIPTS="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
export EDITOR_HERR="$(cd "$_EN_SCRIPTS/.." && pwd)"
export EDITOR_RAIZ="$(cd "$EDITOR_HERR/.." && pwd)"
export EDITOR_SCRIPTS="$_EN_SCRIPTS"
export EDITOR_FUENTES="$EDITOR_RAIZ/4_Recursos/fuentes"
export PATH="$EDITOR_HERR/whisper/bin:$EDITOR_HERR/venv/bin:$EDITOR_HERR/hyperframes/node_modules/.bin:$PATH"
export WHISPER_BIN="$EDITOR_HERR/whisper/bin/whisper-cli"
export WHISPER_MODEL="$EDITOR_HERR/whisper/ggml-large-v3-turbo.bin"
export CHROMIUM_BIN="$EDITOR_HERR/chromium/bin/chromium"
export PUPPETEER_EXECUTABLE_PATH="$CHROMIUM_BIN"
export HYPERFRAMES_NO_OPTIONAL_INSTALL=1
export HYPERFRAMES_TELEMETRY_DISABLED=1
# fontconfig con las fuentes de la persona (sin esto, drawtext/subtitles de FFmpeg no las encuentran)
_FC="$EDITOR_HERR/fonts.conf"
if [ ! -f "$_FC" ] || ! grep -q "$EDITOR_FUENTES" "$_FC" 2>/dev/null; then
  cat > "$_FC" <<EOF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>$EDITOR_FUENTES</dir>
  <include ignore_missing="yes">/etc/fonts/fonts.conf</include>
  <cachedir>/tmp/fontconfig-editor-gente-comun</cachedir>
</fontconfig>
EOF
fi
export FONTCONFIG_FILE="$_FC"
# El modelo de recorte de HyperFrames se guarda en la carpeta; la caché de la máquina se borra entre sesiones.
if [ -f "$EDITOR_HERR/modelos/u2net_human_seg.onnx" ]; then
  mkdir -p "$HOME/.cache/hyperframes/background-removal/models"
  ln -sf "$EDITOR_HERR/modelos/u2net_human_seg.onnx" "$HOME/.cache/hyperframes/background-removal/models/u2net_human_seg.onnx"
fi
unset _EN_SCRIPTS _FC
