#!/usr/bin/env bash
# Arma (o actualiza) la carpeta de trabajo "Editor de Videos IA" desde el repositorio de GitHub.
# Se corre desde una copia del repositorio (git clone), en la shell de la computadora de la persona:
#   rm -rf /tmp/egc && git clone -q --depth 1 https://github.com/nicoparetti/editor-gente-comun.git /tmp/egc \
#     && bash /tmp/egc/plugins/editor-gente-comun/skills/editor-gente-comun/scripts/instalar_carpeta.sh "$HOME/mnt/Editor de Videos IA"
# Nunca pisa lo que la persona ya tiene (videos, perfil, links, recursos propios).
# Las herramientas (.herramientas/scripts y .herramientas/plantillas) sí se reemplazan por la última versión.
set -euo pipefail
R="${1:?Falta la ruta de la carpeta Editor de Videos IA}"
SK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"          # la skill dentro del repositorio
REPO="$(cd "$SK/../../../.." && pwd)"                            # raíz del repositorio
[ -d "$REPO/carpeta" ] || { echo "No encuentro la carpeta base en el repositorio ($REPO/carpeta)"; exit 1; }
H="$R/.herramientas"
mkdir -p "$R" "$H"

# 1) Carpetas, recursos y archivos de doble clic: se copian sin pisar lo existente
cp -Rn "$REPO/carpeta/." "$R/" 2> >(grep -v "non-portable" >&2)
# los archivos de doble clic y la página de descarga sí se actualizan siempre
for f in "0_Instalar/Instalar transcriptor.command" "0_Instalar/Instalar transcriptor (Windows).bat" \
         "0_Instalar/Descargar transcriptor.html" "2_Referencias/Descargar referencias.command" \
         "2_Referencias/Descargar referencias (Windows).bat"; do
  [ -f "$REPO/carpeta/$f" ] && cp -f "$REPO/carpeta/$f" "$R/$f"
done
chmod +x "$R"/0_Instalar/*.command "$R"/2_Referencias/*.command 2>/dev/null || true

# 2) Herramientas: siempre la última versión
rm -rf "$H/scripts" "$H/plantillas"
cp -R "$SK/scripts" "$H/scripts"
cp -R "$SK/templates" "$H/plantillas"
chmod +x "$H"/scripts/*.sh "$H"/scripts/*.py 2>/dev/null || true
[ -f "$H/motor/package.json" ] || { mkdir -p "$H/motor" && cp -R "$SK/templates/motor/." "$H/motor/"; }

# 3) Subcarpetas vacías que el editor necesita
bash "$H/scripts/preparar_entorno.sh" carpetas >/dev/null

echo "  [OK]   Carpeta lista en: $R"
echo "  Scripts: versión $(cat "$H/scripts/VERSION" 2>/dev/null || echo '?')"
