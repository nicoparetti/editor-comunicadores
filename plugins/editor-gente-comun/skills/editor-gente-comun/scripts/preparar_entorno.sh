#!/usr/bin/env bash
# Revisa e instala las herramientas del editor en la carpeta de trabajo (Linux dentro de la Mac o de la PC con Windows).
# Uso, desde la raíz de la carpeta de trabajo:
#   bash .herramientas/scripts/preparar_entorno.sh            → estado de cada herramienta
#   bash .herramientas/scripts/preparar_entorno.sh <paso>     → instala un paso (carpetas, venv, chromium,
#                                                               motor, hyperframes, recorte, whisper, mac, win, manuales)
# Cada paso cabe en una llamada de shell (≤170 s). Si uno corta por tiempo, se vuelve a correr y sigue.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/entorno.sh"
R="$EDITOR_RAIZ"; H="$EDITOR_HERR"
case "$(uname -m)" in aarch64|arm64) ARQ=arm64 ;; *) ARQ=x64 ;; esac   # Mac con chip Apple: arm64; PC con Windows: x64
CHROMIUM_PACK="https://github.com/Sparticuz/chromium/releases/download/v143.0.4/chromium-v143.0.4-pack.$ARQ.tar"
U2NET="https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx"
ok(){ printf "  [OK]   %s\n" "$1"; }; falta(){ printf "  [FALTA] %s → %s\n" "$1" "$2"; }
# Algunas carpetas compartidas (posible en Windows) no admiten enlaces simbólicos: venv y npm los usan.
# En ese caso el venv vive en /tmp (se rearma solo en cada sesión con el paso venv) y npm instala sin enlaces.
sin_enlaces() {
  [ "${EGC_SIN_ENLACES:-}" = 1 ] && return 0
  local t="$H/pruebas/.enlace"; mkdir -p "$H/pruebas" 2>/dev/null
  [ -L "$t" ] && return 1
  ln -s . "$t" 2>/dev/null && [ -L "$t" ] && return 1
  return 0
}
VENV_TMP=/tmp/egc-venv
# Crea en node_modules/.bin un lanzador (archivo común, no enlace) por cada comando de los paquetes instalados
crear_bins() {
  node -e '
    const fs=require("fs"),path=require("path"),nm=path.join(process.argv[1],"node_modules"),bin=path.join(nm,".bin");
    fs.mkdirSync(bin,{recursive:true});
    for (const d of fs.readdirSync(nm)) {
      if (d===".bin") continue;
      const ps=d.startsWith("@")?fs.readdirSync(path.join(nm,d)).map(x=>d+"/"+x):[d];
      for (const p of ps) {
        let pj; try { pj=JSON.parse(fs.readFileSync(path.join(nm,p,"package.json"),"utf8")); } catch(e) { continue; }
        let b=pj.bin; if (!b) continue; if (typeof b==="string") b={[pj.name.split("/").pop()]:b};
        for (const [n,f] of Object.entries(b)) { const w=path.join(bin,n); if (fs.existsSync(w)) continue;
          fs.writeFileSync(w,"#!/bin/sh\nexec node \"$(dirname \"$0\")/../"+p+"/"+f+"\" \"$@\"\n",{mode:0o755}); }
      }
    }' "$1"
}

estado() {
  echo "Carpeta de trabajo: $R"
  for d in "1_Videos sin editar" "2_Referencias" "3_Videos editados" "4_Recursos/fuentes" "5_Mi estilo"; do [ -d "$R/$d" ] || { falta "carpetas" "paso carpetas"; break; }; done
  ENC="$(ffmpeg -hide_banner -encoders 2>/dev/null || true)"; FIL="$(ffmpeg -hide_banner -filters 2>/dev/null || true)"
  [[ "$ENC" == *prores_ks* && "$ENC" == *libx264* && "$FIL" == *subtitles* ]] && ok "FFmpeg $(ffmpeg -version | head -1 | cut -d' ' -f3) con ProRes, x264 y libass" || falta "FFmpeg" "no hay FFmpeg con ProRes/x264/libass en la máquina: avisar a la persona"
  python3 -c "import PIL, numpy" 2>/dev/null && ok "Python ($(command -v python3)) con PIL y numpy" || falta "PIL/numpy" "paso venv"
  "$H/venv/bin/python" -c 1 2>/dev/null && ok "venv (.herramientas/venv)" || falta "venv" "paso venv"
  sin_enlaces && echo "  [AVISO] La carpeta no admite enlaces: el venv vive en /tmp y se rearma en cada sesión con el paso venv"
  mkdir -p "$H/pruebas" 2>/dev/null; printf '#!/bin/sh\nexit 0\n' > "$H/pruebas/ejec.sh" 2>/dev/null; chmod +x "$H/pruebas/ejec.sh" 2>/dev/null
  "$H/pruebas/ejec.sh" 2>/dev/null || echo "  [AVISO] La carpeta no deja ejecutar programas: copia whisper-cli y Chromium a /tmp/egc-bin y úsalos desde ahí (entorno-y-herramientas.md → Windows)"
  [ -x "$H/venv/bin/yt-dlp" ] && ok "yt-dlp" || falta "yt-dlp" "paso venv"
  [ -x "$CHROMIUM_BIN" ] && "$CHROMIUM_BIN" --version >/dev/null 2>&1 && ok "Chromium $ARQ ($("$CHROMIUM_BIN" --version 2>/dev/null))" || falta "Chromium" "paso chromium"
  [ -f "$R/.herramientas/motor/node_modules/remotion/dist/cjs/index.js" ] && ok "Motor Remotion (node_modules)" || falta "Motor Remotion" "paso motor"
  [ -x "$H/hyperframes/node_modules/.bin/hyperframes" ] && ok "HyperFrames CLI" || falta "HyperFrames CLI" "paso hyperframes"
  [ -d "$H/hyperframes/node_modules/onnxruntime-node" ] && [ -f "$H/modelos/u2net_human_seg.onnx" ] && ok "Recorte de persona (u2net)" || falta "Recorte de persona" "paso recorte"
  "$H/venv/bin/python" -c "import cv2, fontTools" 2>/dev/null && [ -f "$H/modelos/face_detection_yunet_2023mar.onnx" ] && ok "OpenCV + YuNet (encuadre vertical de clips)" || falta "OpenCV/YuNet" "paso venv y paso recorte"
  [ -x "$WHISPER_BIN" ] && ok "whisper.cpp" || falta "whisper.cpp" "paso whisper"
  [ -f "$WHISPER_MODEL" ] && ok "Modelo Whisper large-v3-turbo" || { [ -f "$R/0_Instalar/ggml-large-v3-turbo.bin" ] && falta "Modelo Whisper (ya descargado en 0_Instalar)" "paso modelo" || falta "Modelo Whisper" "paso modelo (lo descarga solo; si está bloqueado, plan B de la bienvenida)"; }
  if [ -x "$H/mac/yt-dlp_macos" ] && [ -x "$H/mac/ffmpeg" ]; then ok "Descarga de referencias (Mac)"
  elif [ -f "$H/win/yt-dlp.exe" ] && [ -f "$H/win/ffmpeg.exe" ]; then ok "Descarga de referencias (Windows)"
  else falta "Descarga de referencias" "paso mac (si la persona usa Mac) o paso win (si usa Windows)"; fi
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
    PAQ="yt-dlp cmake pillow numpy fonttools opencv-python-headless==4.10.0.84"
    if sin_enlaces; then
      # venv en /tmp y lanzadores comunes en .herramientas/venv/bin (mismo camino para todos los scripts)
      [ -x "$VENV_TMP/bin/python" ] || python3 -m venv "$VENV_TMP"
      timeout 170 "$VENV_TMP/bin/pip" install -q --upgrade $PAQ || exit 1
      mkdir -p "$H/venv/bin"
      for b in "$VENV_TMP"/bin/*; do n="$(basename "$b")"; case "$n" in activate*|Activate*) continue ;; esac
        printf '#!/bin/sh\nexec "%s" "$@"\n' "$b" > "$H/venv/bin/$n"; chmod +x "$H/venv/bin/$n" 2>/dev/null; done
      "$H/venv/bin/python" -c "import PIL, numpy, cv2" && ok "venv en /tmp (carpeta sin enlaces) con yt-dlp, cmake, PIL y numpy"
    else
      [ -x "$H/venv/bin/python" ] || python3 -m venv "$H/venv"
      timeout 170 "$H/venv/bin/pip" install -q --upgrade $PAQ && ok "venv con yt-dlp, cmake, PIL y numpy"
    fi ;;
  chromium)
    # se descarga y descomprime en /tmp: así no quedan restos en la carpeta (borrar ahí necesita permiso)
    mkdir -p "$H/chromium/bin" /tmp/chromium-pack && cd /tmp/chromium-pack || exit 1
    [ -f pack.tar ] || timeout 150 curl -sSfL -o pack.tar "$CHROMIUM_PACK" || { echo "No se pudo descargar Chromium"; exit 1; }
    rm -rf x && mkdir x && tar -xf pack.tar -C x && cd x && node -e '
      const fs=require("fs"),z=require("zlib");
      for (const f of ["chromium.br","swiftshader.tar.br"]) fs.writeFileSync(f.replace(".br",""), z.brotliDecompressSync(fs.readFileSync(f)));' \
      && cp chromium "$H/chromium/bin/chromium" && chmod +x "$H/chromium/bin/chromium" && tar -xf swiftshader.tar -C "$H/chromium/bin" && cd /tmp && rm -rf /tmp/chromium-pack
    "$CHROMIUM_BIN" --version && ok "Chromium" ;;
  motor)
    [ -f "$H/motor/package.json" ] || { [ -d "$H/plantillas/motor" ] && cp -R "$H/plantillas/motor/." "$H/motor/"; }
    [ -f "$H/motor/package.json" ] || { echo "Falta el proyecto del motor: correr instalar_carpeta.sh (bienvenida, paso 3)"; exit 1; }
    mkdir -p "$H/motor/public/fuentes" "$H/motor/public/mock" && cp "$R"/4_Recursos/fuentes/*.ttf "$H/motor/public/fuentes/" 2>/dev/null
    NB=""; sin_enlaces && NB="--no-bin-links"
    cd "$H/motor" && timeout 170 npm install --ignore-scripts --no-audit --no-fund --loglevel=error $NB && { [ -z "$NB" ] || crear_bins "$H/motor"; } && ok "Motor Remotion" ;;
  hyperframes)
    mkdir -p "$H/hyperframes" && cd "$H/hyperframes" && { [ -f package.json ] || npm init -y >/dev/null; }
    NB=""; sin_enlaces && NB="--no-bin-links"
    timeout 170 npm install hyperframes@latest onnxruntime-node@1.21.1 --ignore-scripts --no-audit --no-fund --loglevel=error $NB && { [ -z "$NB" ] || crear_bins "$H/hyperframes"; } && ok "HyperFrames CLI"
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
    # 1) Si la persona ya lo dejó en 0_Instalar (o se movió desde Descargas), se verifica y se guarda.
    F="$R/0_Instalar/ggml-large-v3-turbo.bin"
    if [ -f "$F" ]; then
      T=$(stat -c%s "$F"); [ "$T" -gt 1500000000 ] || { echo "El archivo está incompleto ($T bytes): volver a descargarlo"; exit 1; }
      mkdir -p "$H/whisper" && mv "$F" "$WHISPER_MODEL" && ok "Modelo Whisper movido a .herramientas/whisper"; exit 0
    fi
    [ -f "$WHISPER_MODEL" ] && { ok "Modelo Whisper ya instalado"; exit 0; }
    # 2) Si no, se descarga directo, por tramos (cada llamada baja lo que puede en ~160 s y sigue donde quedó).
    mkdir -p "$H/whisper"; P="$WHISPER_MODEL.parcial"
    URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin"
    timeout 160 curl -sS -L -C - --fail -o "$P" "$URL"; RC=$?
    T=$(stat -c%s "$P" 2>/dev/null || echo 0)
    if [ "$T" -ge 1624555275 ]; then mv "$P" "$WHISPER_MODEL" && ok "Modelo Whisper descargado e instalado"
    elif [ "$T" -gt 0 ]; then echo "  [SIGUE] Modelo Whisper: $((T/1048576)) de 1549 MB. Volver a correr: paso modelo"
    else echo "  [BLOQUEADO] No se pudo descargar el modelo desde acá (código $RC). Plan B: bienvenida.md, paso 3.5"; exit 1; fi ;;
  manuales)
    # se clona en /tmp (git no puede trabajar bien dentro de la carpeta compartida) y se copia sin .git
    mkdir -p "$H/manuales" && rm -rf /tmp/remotion-skills && timeout 90 git clone -q --depth 1 https://github.com/remotion-dev/skills.git /tmp/remotion-skills \
      && rm -rf /tmp/remotion-skills/.git && mkdir -p "$H/manuales/remotion" && cp -R /tmp/remotion-skills/. "$H/manuales/remotion/" && cd "$H/manuales"
    if sin_enlaces; then mkdir -p hyperframes && cp -R ../hyperframes/node_modules/hyperframes/dist/skills/. hyperframes/; else ln -sfn ../hyperframes/node_modules/hyperframes/dist/skills hyperframes; fi && ok "manuales" ;;
  mac)
    mkdir -p "$H/mac" && cd "$H/mac" && { [ -x yt-dlp_macos ] || timeout 80 curl -sSfL -o yt-dlp_macos https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos; } \
      && { [ -x ffmpeg ] || timeout 90 curl -sSfL -o ffmpeg https://github.com/eugeneware/ffmpeg-static/releases/download/b6.1.1/ffmpeg-darwin-arm64; } \
      && chmod +x yt-dlp_macos ffmpeg && ok "yt-dlp y ffmpeg para macOS " ;;
  win)
    mkdir -p "$H/win" && cd "$H/win" && { [ -f yt-dlp.exe ] || timeout 80 curl -sSfL -o yt-dlp.exe https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe; } \
      && { [ -f ffmpeg.exe ] || timeout 120 curl -sSfL -o ffmpeg.exe https://github.com/eugeneware/ffmpeg-static/releases/download/b6.1.1/ffmpeg-win32-x64; } \
      && ok "yt-dlp y ffmpeg para Windows" ;;
  *) echo "Paso desconocido: $1"; exit 1 ;;
esac
