# Imágenes: carruseles, placas y portadas

## Carruseles y placas

### Sistema visual por defecto: Kit 04 Serif Classic (salvo que pida otro)

- Fuentes: **Playfair Display**, **EB Garamond**, **Courier Prime** (en `4_Recursos/fuentes/`).
- Paleta: negro **#1A1411**, crema **#F5EFE3**, bordó **#8B1A1A**, dorado **#D4A82B**.

### Reglas

- Máximo **7 placas**.
- Totalmente tipográfico: sin fotos ni imagen de perfil.
- En cada placa solo van **título, cuerpo y palabras o frases destacadas** del cuerpo.
- Prohibido: etiquetas superiores tipo "EL PROBLEMA • 01/08", subtítulos al pie, numeración visible (se ve "muy de IA"). Frases como "para la nueva generación" le resultan cringe.
- Al pasarle los textos de las placas, no rotules cada línea con "Etiqueta / Pie / Destacado": solo título y cuerpo, con lo destacado marcado.
- Voz pastoral directa, sin emojis ni jerga juvenil forzada; cierre cristocéntrico fuerte.
- Versículos en NBLA, verificados (ver `estilo-por-defecto.md`).

### Render (HTML + navegador)

- Escribe cada carrusel como un HTML con una `.slide` por placa a **1080×1350**.
- Fuentes embebidas como TTF en base64 desde `4_Recursos/fuentes/` (si falta alguna, descárgala de `raw.githubusercontent.com/google/fonts/`; la API CSS de Google Fonts está bloqueada). Secuencia: TTF → base64 → `@font-face` en `fonts_embedded.css` → importar en el HTML.
- Captura cada `.slide` con **device scale factor 2**, esperando ~3 s después de cargar para que rendericen las fuentes variables. Oculta cualquier barra de descarga (`.dl-bar`) antes de capturar.
- Dónde: en la computadora de la persona con el Chromium de `.herramientas/chromium/bin/chromium` (puppeteer-core o Remotion `still`), o en el espacio de la nube con Playwright. Guarda los PNG finales en `3_Videos editados/<nombre>/`.

## Portadas de YouTube

Script: `.herramientas/scripts/portada_yt.py` (1280×720, ≤2 MB, estilo: foto tratada con grano y tinte, degradé del lado con menos detalle, título Anton con textura, nombre y encabezado en Poppins).

```bash
python3 .herramientas/scripts/portada_yt.py foto.jpg --titulo "¡QUE|VALGA|LA PENA!" \
  --encabezado "Enseñanza|completa" --extra "3 claves" --lado auto --color auto \
  --salida 3_Videos editados/<nombre>/portada.jpg
```

- `|` = salto de línea. `--color marca` usa el rojo de marca #D73F2A; `auto` toma el color dominante de la foto.
- Otros ajustes: `--foco x,y`, `--zoom`, `--tinte`, `--saturacion`, `--calidez`, `--ancho`, `--color-texto`.
- Mira siempre la portada resultante antes de entregarla (tildes, cortes del título, que la cara no quede tapada).

## Portadas de reels animados

Se generan siempre al aprobarse el reel, desde el mejor cuadro del video o compuestas con su mismo kit visual. Reglas completas en `reels-animados.md` §9.1-bis (1080×1920, título corto del guion en Instrument Serif con la palabra clave en itálica del acento, lo esencial en el centro 1080×1350 para la grilla del perfil).
