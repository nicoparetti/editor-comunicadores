# Plantillas · reel animado narrado (sin cámara)

Copiar a `3_Videos editados/<proyecto>/trabajo/` y adaptar; las reglas están en `references/reels-animados.md`.

| Archivo | Qué hace |
|---|---|
| `corte.py` | Corte ajustado (silencios ≥ 0,2 s, cola 0,05 / entrada 0,04) y quita la toma fallida (`QUITAR`). Escribe `cortes.json`. |
| `mapear.py` | Lleva las palabras de Whisper del bruto al audio cortado. |
| `aire_ejemplo.py` | Inserta aire: pausa mínima entre oraciones + `HOLD` por índice de palabra; `NOMIN` exime una palabra del mínimo; `CORR` corrige marcas medidas. |
| `figuras.py` | Pictogramas (orando, martillando, sosteniendo, tarima) y líneas quebradas (`grieta_v`, `grieta_h`). |
| `mapas_base.py` | Mapas Natural Earth a escala fija para la cámara. |
| `graficos_base.py` | Generador de ejemplo del estilo por defecto: escenas, contadores, pictogramas, línea quebrada, frase palabra a palabra y subtítulos. `TEMA=gris|noche python3 graficos_base.py palabras.json` → `graficos.html`. Reescribir las escenas para cada reel. |
| `base/kit_base.py` | Las dos paletas (`TEMAS`), CSS y fuentes, piezas (`fx`, `escena`, `rotulo`, `tarjeta`, `contador`, `palabras`, `grieta`, `fuente_biblica`, `termino`, `pin`), subtítulos por bloques en y = 1350 y el motor `render(t)`. |
| `base/biblia3d.py` + `package.json` | Biblia abierta en 3D con Three.js en la paleta elegida (`npm install`; levanta un servidor http local). |
| `base/lamina.py` | Lámina del storyboard de 6 cuadros (tiempo, frase y nota). |
| `render.py` | Playwright + Chrome → pipe a ffmpeg. Uso: `python3 render.py <cuadro_ini> <cuadro_fin> salida.mp4 graficos.html <duración>` (dos procesos por mitades). |
| `sfx_base.py` | Pista de efectos con la paleta fija y pads sintetizados (`pad()`); adaptar la lista de eventos. |
| `auditoria.py` | `marcas` (palabras contra la voz) y `sonido` (efectos contra la imagen). Correr antes de cada entrega. |
| `preset/` | Voz con IA, aire de escenas, audio del clip de 7 s y del video completo, auditorías de zona segura y 3D, objetos 3D (ver su `LEEME.md`). |

Fuentes del HTML en `img/` junto al HTML (de `4_Recursos/fuentes/`): CalSans-Regular.ttf, Inter.ttf, InstrumentSerif-Italic.ttf, JetBrainsMono.ttf, PlayfairDisplay-SemiBoldItalic.ttf, GFSDidot-Regular.ttf, FrankRuhlLibre.ttf. Imágenes del proyecto también en `img/`.
