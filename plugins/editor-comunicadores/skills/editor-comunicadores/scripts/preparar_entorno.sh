#!/usr/bin/env bash
# Revisa e instala las herramientas del editor en la carpeta de trabajo (Linux arm64 dentro de la Mac).
# Uso, desde la raíz de la carpeta de trabajo:
#   bash .herramientas/scripts/preparar_entorno.sh            → estado de cada herramienta
#   bash .herramientas/scripts/preparar_entorno.sh <paso>     → instala un paso (carpetas, venv, chromium,
#                                                               motor, hyperframes, recorte, whisper, mac, manuales)
# Cada paso cabe en una llamada de shell (≤170 s). Si uno corta por tiempo, se vuelve a correr y sigue.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/entorno.sh"
R="$EDITOR_RAIZ"; H="$EDITOR_HERR"
CHROMIUM_PACK="https://github.com/Sparticuz/chromium/releases/download/v143.0.4/chromium-v143.0.4-pack.arm64.tar"
U2NET="https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx"
ok(){ printf "  [OK]   %s\n" "$1"; }; falta(){ printf "  [FALTA] %s → %s\n" "$1" "$2"; }

estado() {
  echo "Carpeta de trabajo: $R"
  for d in "1_Videos sin editar" "2_Referencias" "3_Videos editados" "4_Recursos/fuentes" "5_Mi estilo"; do [ -d "$R/$d" ] || { falta "carpetas" "paso carpetas"; break; }; done
  ENC="$(ffmpeg -hide_banner -encoders 2>/dev/null || true)"; FIL="$(ffmpeg -hide_banner -filters 2>/dev/null || true)"
  [[ "$ENC" == *prores_ks* && "$ENC" == *libx264* && "$FIL" == *subtitles* ]] && ok "FFmpeg $(ffmpeg -version | head -1 | cut -d' ' -f3) con ProRes, x264 y libass" || falta "FFmpeg" "no hay FFmpeg con ProRes/x264/libass en la máquina: avisar a la persona"
  python3 -c "import PIL, numpy" 2>/dev/null && ok "Python ($(command -v python3)) con PIL y numpy" || falta "PIL/numpy" "paso venv"
  [ -x "$H/venv/bin/python" ] && ok "venv (.herramientas/venv)" || falta "venv" "paso venv"
  [ -x "$H/venv/bin/yt-dlp" ] && ok "yt-dlp" || falta "yt-dlp" "paso venv"
  [ -x "$CHROMIUM_BIN" ] && "$CHROMIUM_BIN" --version >/dev/null 2>&1 && ok "Chromium arm64 ($("$CHROMIUM_BIN" --version 2>/dev/null))" || falta "Chromium" "paso chromium"
  [ -f "$R/.herramientas/motor/node_modules/remotion/dist/cjs/index.js" ] && ok "Motor Remotion (node_modules)" || falta "Motor Remotion" "paso motor"
  [ -x "$H/hyperframes/node_modules/.bin/hyperframes" ] && ok "HyperFrames CLI" || falta "HyperFrames CLI" "paso hyperframes"
  [ -d "$H/hyperframes/node_modules/onnxruntime-node" ] && [ -f "$H/modelos/u2net_human_seg.onnx" ] && ok "Recorte de persona (u2net)" || falta "Recorte de persona" "paso recorte"
  "$H/venv/bin/python" -c "import cv2, fontTools" 2>/dev/null && [ -f "$H/modelos/face_detection_yunet_2023mar.onnx" ] && ok "OpenCV + YuNet (encuadre vertical de clips)" || falta "OpenCV/YuNet" "paso venv y paso recorte"
  [ -x "$WHISPER_BIN" ] && ok "whisper.cpp" || falta "whisper.cpp" "paso whisper"
  [ -f "$WHISPER_MODEL" ] && ok "Modelo Whisper large-v3-turbo" || { [ -f "$R/0_Instalar/ggml-large-v3-turbo.bin" ] && falta "Modelo Whisper (ya descargado en 0_Instalar)" "paso modelo" || falta "Modelo Whisper" "pedir doble clic en 0_Instalar/Descargar transcriptor y arrastrar el archivo a 0_Instalar"; }
  [ -x "$H/mac/yt-dlp_macos" ] && [ -x "$H/mac/ffmpeg" ] && [ -f "$R/2_Referencias/Descargar referencias.command" ] && ok "Descarga de referencias (yt-dlp para macOS)" || falta "Descarga de referencias" "paso mac"
  [ -d "$H/manuales/remotion/skills" ] && ok "Manual oficial de Remotion" || falta "Manual Remotion" "paso manuales"
  [ -d "$H/manuales/hyperframes" ] && ok "Manual de HyperFrames" || falta "Manual HyperFrames" "paso manuales"
  [ -f "$H/scripts/VERSION" ] && echo "  Scripts: versión $(cat "$H/scripts/VERSION")"
}

case "${1:-estado}" in
  estado) estado ;;
  carpetas)
    mkdir -p "$R/1_Videos sin editar" "$R/2_Referencias" "$R/3_Videos editados" "$R/5_Mi estilo/tableros" "$H/motor" "$R"/4_Recursos/{fuentes,sfx,musica,luts,logo,imagenes} "$H"/{scripts,whisper/bin,modelos,manuales,pruebas}
    ok "carpetas" ;;
  venv)
    [ -x "$H/venv/bin/python" ] || python3 -m venv "$H/venv"
    timeout 170 "$H/venv/bin/pip" install -q --upgrade yt-dlp cmake pillow numpy fonttools opencv-python-headless==4.10.0.84 && ok "venv con yt-dlp, cmake, PIL y numpy" ;;
  chromium)
    mkdir -p "$H/chromium/bin" && cd "$H/chromium" || exit 1
    [ -f pack.tar ] || timeout 150 curl -sSfL -o pack.tar "$CHROMIUM_PACK" || { echo "No se pudo descargar Chromium"; exit 1; }
    rm -rf x && mkdir x && tar -xf pack.tar -C x && cd x && node -e '
      const fs=require("fs"),z=require("zlib");
      for (const f of ["chromium.br","swiftshader.tar.br"]) fs.writeFileSync(f.replace(".br",""), z.brotliDecompressSync(fs.readFileSync(f)));' \
      && mv chromium ../bin/chromium && chmod +x ../bin/chromium && tar -xf swiftshader.tar -C ../bin && cd .. && rm -rf x pack.tar
    "$CHROMIUM_BIN" --version && ok "Chromium" ;;
  motor)
    SK=$(ls -d "$HOME"/.claude/plugins/*/*/skills/editor-comunicadores 2>/dev/null | head -1)
    [ -f "$H/motor/package.json" ] || { [ -n "$SK" ] && cp -R "$SK/templates/motor/." "$H/motor/"; }
    [ -f "$H/motor/package.json" ] || { echo "Falta el proyecto del motor: copiar templates/motor de la skill a .herramientas/motor"; exit 1; }
    mkdir -p "$H/motor/public/fuentes" "$H/motor/public/mock" && cp "$R"/4_Recursos/fuentes/*.ttf "$H/motor/public/fuentes/" 2>/dev/null
    cd "$H/motor" && timeout 170 npm install --ignore-scripts --no-audit --no-fund --loglevel=error && ok "Motor Remotion" ;;
  hyperframes)
    mkdir -p "$H/hyperframes" && cd "$H/hyperframes" && { [ -f package.json ] || npm init -y >/dev/null; }
    timeout 170 npm install hyperframes@latest onnxruntime-node@1.21.1 --ignore-scripts --no-audit --no-fund --loglevel=error && ok "HyperFrames CLI"
    npx hyperframes telemetry disable >/dev/null 2>&1 || true
    S="$H/hyperframes/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx"
    [ -d "$S" ] && mkdir -p "$R/4_Recursos/sfx_pixabay" && cp "$S"/* "$R/4_Recursos/sfx_pixabay/" && ok "sonidos de la biblioteca de HyperFrames en 4_Recursos/sfx_pixabay" ;;
  recorte)
    mkdir -p "$H/modelos" && cd "$H/modelos" && { [ -f u2net_human_seg.onnx ] || timeout 160 curl -sSfL -o u2net_human_seg.onnx "$U2NET"; } && { [ -f face_detection_yunet_2023mar.onnx ] || timeout 60 curl -sSfL -o face_detection_yunet_2023mar.onnx https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx; } && ok "modelos u2net y YuNet" ;;
  whisper)
    [ -x "$H/venv/bin/cmake" ] || { echo "Primero: paso venv"; exit 1; }
    [ -d /tmp/wsrc ] || timeout 60 git clone -q --depth 1 https://github.com/ggml-org/whisper.cpp.git /tmp/wsrc
    [ -f /tmp/wbuild/CMakeCache.txt ] || "$H/venv/bin/cmake" -S /tmp/wsrc -B /tmp/wbuild -DBUILD_SHARED_LIBS=OFF -DWHISPER_BUILD_TESTS=OFF -DGGML_NATIVE=OFF -DCMAKE_BUILD_TYPE=Release >/dev/null
    timeout 150 "$H/venv/bin/cmake" --build /tmp/wbuild -j4 --target whisper-cli >/dev/null && cp /tmp/wbuild/bin/whisper-cli "$H/whisper/bin/" && ok "whisper.cpp (si cortó por tiempo, volver a correr este paso)" ;;
  modelo)
    F="$R/0_Instalar/ggml-large-v3-turbo.bin"; [ -f "$F" ] || { echo "No está $F"; exit 1; }
    T=$(stat -c%s "$F"); [ "$T" -gt 1500000000 ] || { echo "El archivo está incompleto ($T bytes): volver a descargarlo"; exit 1; }
    mkdir -p "$H/whisper" && mv "$F" "$WHISPER_MODEL" && ok "Modelo Whisper movido a .herramientas/whisper" ;;
  manuales)
    mkdir -p "$H/manuales" && cd "$H/manuales" && rm -rf remotion && timeout 90 git clone -q --depth 1 https://github.com/remotion-dev/skills.git remotion && rm -rf remotion/.git
    ln -sfn ../hyperframes/node_modules/hyperframes/dist/skills hyperframes && ok "manuales" ;;
  mac)
    mkdir -p "$H/mac" && cd "$H/mac" && { [ -x yt-dlp_macos ] || timeout 80 curl -sSfL -o yt-dlp_macos https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos; } \
      && { [ -x ffmpeg ] || timeout 90 curl -sSfL -o ffmpeg https://github.com/eugeneware/ffmpeg-static/releases/download/b6.1.1/ffmpeg-darwin-arm64; } \
      && chmod +x yt-dlp_macos ffmpeg && ok "yt-dlp y ffmpeg para macOS " ;;
  *) echo "Paso desconocido: $1"; exit 1 ;;
esac
