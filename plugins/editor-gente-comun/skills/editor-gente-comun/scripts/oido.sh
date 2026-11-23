#!/usr/bin/env bash
# El oído del editor: Earshot (github.com/Leonxlnx/earshot, MIT) escucha audio con dos modelos abiertos (CLAP y AST)
# y lo describe con palabras y números. Corre en el ESPACIO EN LA NUBE (Bash), no en la máquina de la persona:
# pide ~2,5 GB de memoria y baja sus modelos de huggingface.co (bloqueado en la máquina de la persona).
# El espacio en la nube se borra al cerrar la sesión: el primer uso de cada sesión instala todo solo (~2 min).
#
# Uso (en el espacio en la nube):
#   bash oido.sh instalar                                  instala Earshot + modelos (solo si falta; ~2 min)
#   bash oido.sh revisar MEZCLA [CUES] [PERFIL]            escucha una mezcla o un video: línea de tiempo,
#                                                          hoja visual, realismo y comparación con el perfil
#   bash oido.sh elegir "descripción en inglés" ARCHIVOS…  ordena candidatos por parecido a la descripción
#   bash oido.sh ab A B ["descripción en inglés"]          compara dos versiones (antes / después)
#   bash oido.sh real ARCHIVOS…                            ¿suena grabado/producido o sintetizado con código?
#   bash oido.sh describir ARCHIVO                         qué es el sonido, en palabras
#   bash oido.sh perfil CARPETA_DE_REELS SALIDA.json       perfil de sonido a partir de reels aprobados de la persona
# CUES: "1.5,3.2,…" (segundos) o un JSON; PERFIL: JSON de `oido.sh perfil`. Salidas en ./oido_<nombre>/.
set -uo pipefail
VENV="${OIDO_VENV:-$HOME/.oido/venv}"
E="$VENV/bin/earshot"
export EARSHOT_THREADS="${EARSHOT_THREADS:-2}"

instalar() {
  if [ -x "$E" ] && "$E" doctor 2>/dev/null | grep -qi "clap" && [ -d "${EARSHOT_HOME:-$HOME/.cache/earshot}/hf" ]; then
    echo "Oído listo ($("$E" --version 2>/dev/null))"; return 0
  fi
  echo "Instalando el oído (Earshot + modelos, ~2 min, solo la primera vez de la sesión)…"
  [ -x "$VENV/bin/python" ] || python3 -m venv "$VENV" || return 1
  "$VENV/bin/pip" install -q torch --index-url https://download.pytorch.org/whl/cpu || return 1
  "$VENV/bin/pip" install -q "earshot[listen,measure,images] @ git+https://github.com/Leonxlnx/earshot" || return 1
  "$E" doctor --fetch >/dev/null 2>&1 || { echo "No pude bajar los modelos (huggingface.co)"; return 1; }
  echo "Oído listo ($("$E" --version 2>/dev/null))"
}

salida_de() { local b; b="$(basename "$1")"; b="${b%.*}"; echo "oido_${b}"; }

case "${1:-}" in
  instalar) instalar ;;
  revisar)
    F="${2:?falta la mezcla o el video}"; CUES="${3:-}"; PERFIL="${4:-}"
    instalar >/dev/null || exit 1
    O="$(salida_de "$F")"; mkdir -p "$O"
    C=(); [ -n "$CUES" ] && C=(--cues "$CUES")
    echo "== Línea de tiempo (qué pasa en cada momento) =="
    "$E" timeline "$F" "${C[@]}" --out "$O/linea_de_tiempo.json" | tee "$O/linea_de_tiempo.txt" | head -80
    "$E" sheet "$F" "${C[@]}" -o "$O/hoja_sonido.png" >/dev/null 2>&1 && echo "(hoja visual: $O/hoja_sonido.png)"
    echo; echo "== ¿Grabado o sintético? =="
    "$E" realness "$F" --out "$O/realismo.json" | tee "$O/realismo.txt" | head -20
    if [ -n "$PERFIL" ] && [ -f "$PERFIL" ]; then
      echo; echo "== Contra el perfil de los reels aprobados de la persona =="
      "$E" critique "$F" --profile "$PERFIL" --out "$O/contra_perfil.json" | tee "$O/contra_perfil.txt" | head -60
    fi
    echo; echo "Todo en $O/" ;;
  elegir)
    Q="${2:?falta la descripción}"; shift 2
    instalar >/dev/null || exit 1
    "$E" rank "$Q" "$@" ;;
  ab)
    A="${2:?falta A}"; B="${3:?falta B}"; Q="${4:-}"
    instalar >/dev/null || exit 1
    if [ -n "$Q" ]; then "$E" ab "$A" "$B" --query "$Q"; else "$E" ab "$A" "$B"; fi ;;
  real) shift; instalar >/dev/null || exit 1; "$E" realness "$@" ;;
  describir) instalar >/dev/null || exit 1; "$E" describe "${2:?falta el archivo}" ;;
  perfil)
    D="${2:?falta la carpeta de reels aprobados}"; OUT="${3:?falta el JSON de salida}"
    instalar >/dev/null || exit 1
    "$E" profile "$D" -o "$OUT" | tail -30 ;;
  *) sed -n 2,19p "$0"; exit 1 ;;
esac
