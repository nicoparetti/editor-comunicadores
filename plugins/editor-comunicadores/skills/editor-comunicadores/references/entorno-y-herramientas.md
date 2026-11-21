# Entorno y herramientas

## Dónde se trabaja

- **Carpeta de trabajo:** `~/Desktop/Editor de Videos IA/` en la computadora de la persona. Si no está conectada a la sesión, pide acceso a esa carpeta.
- **Shell en la computadora de la persona** (`device_bash`): Linux arm64 dentro de la Mac, con la carpeta en `$HOME/mnt/Editor de Videos IA`. Todo lo que toca videos se hace ahí: los brutos 4K pesan demasiado para moverlos.
  - Cada llamada es un shell nuevo de **≤180 s**: los procesos en segundo plano mueren al terminar la llamada. Divide los trabajos largos en pasos; los scripts largos son reanudables (dicen `SIGUE`).
  - `/tmp` dura toda la sesión; el resto de la máquina (fuera de la carpeta) se borra entre sesiones. Por eso todas las herramientas viven en `.herramientas/` dentro de la carpeta.
  - Empieza cada comando con: `cd "$HOME/mnt/Editor de Videos IA" && source .herramientas/scripts/entorno.sh`.
  - Recursos de la máquina: 4 núcleos, ~3 GB de RAM. Usa 4 hilos como máximo.
- **Espacio en la nube** (`Bash`): para mirar imágenes o fotogramas (Read), para lo que necesite Playwright y para la revisión visual. Pasa solo lo necesario (fotogramas, hojas de contactos, gráficos chicos), nunca brutos.
- la persona no usa la Terminal: instala y ejecuta tú.

## Al empezar una sesión

1. `bash .herramientas/scripts/preparar_entorno.sh` → lista qué está listo y qué falta. Instala lo que falte con `preparar_entorno.sh <paso>` (un paso por llamada).
2. Compara `.herramientas/scripts/VERSION` con `scripts/VERSION` de esta skill. Si la skill es más nueva, copia los scripts de la skill a `.herramientas/scripts/`: cópialos a `/mnt/user-data/outputs/` en el espacio de la nube y escríbelos en la carpeta con `device_commit_files`. Usa un nombre de archivo nuevo cada vez que vuelvas a enviar un archivo ya enviado (la copia puede salir de una caché vieja) y verifica con `md5sum` en los dos lados.

## Borrado de intermedios

**Borrado de intermedios: sin preguntarle a la persona.** Todo lo intermedio se borra sin consultarlo en el chat: `trabajo/`, proxies, HQ verticales, pruebas, renders de revisión y versiones anteriores ya superadas. La app exige una aprobación de borrado por sesión: al empezar a trabajar, solicítala con `device_request_delete_permission` sobre la carpeta Editor de Videos IA, sin anunciarlo ni preguntarlo antes. La app de escritorio guarda una copia de lo que se envía al chat en `Claude outputs/` dentro de la carpeta: esas copias también son intermedias y se borran al terminar (la persona descarga desde el chat lo que necesite). **Nunca** borres originales (`1_Videos sin editar/`), videos finales aprobados, `2_Referencias/`, `4_Recursos/` ni nada fuera de la carpeta.

## Red

El acceso a internet sigue la lista de dominios permitidos de la cuenta.
- Funcionan: GitHub (y sus descargas), npm, PyPI, raw.githubusercontent.com.
- **Bloqueados:** huggingface.co (modelos de Whisper), storage.googleapis.com (Chrome oficial de Remotion), YouTube e Instagram. En el plan de la persona la lista de dominios es fija, así que no se pueden agregar.
- **Solución para lo bloqueado: la propia conexión de la Mac.** Los archivos `.command` de la raíz de la carpeta corren en macOS (no en la máquina Linux), con la internet de la persona, y él los abre con doble clic. No puedes ejecutarlos tú: pídele que haga doble clic y espera a que te avise.
  - `Instalar modelo Whisper.command` → baja el modelo a `.herramientas/whisper/` (reanudable).
  - `Descargar referencias.command` → baja los links de `2_Referencias/links.txt` con `yt-dlp_macos` + `ffmpeg` de macOS (`.herramientas/mac/`); si un link pide sesión (Instagram), reintenta con las cookies de Chrome.
- Paquetes npm que descargan binarios con su propio cliente fallan con 407: instala con `--ignore-scripts`.

## Herramientas instaladas (en la carpeta)

| Herramienta | Dónde | Para qué |
|---|---|---|
| FFmpeg 4.4 (sistema) | `ffmpeg`, `ffprobe` | Corte, voz, ProRes 4444 con alfa (`prores_ks`), H.264 (`libx264`), subtítulos (`libass`) |
| Python 3.10 + PIL + numpy (sistema) | `python3` | Scripts de subtítulos, medición, portadas |
| venv | `.herramientas/venv` | Python con PIL y numpy, `cmake` |
| yt-dlp + ffmpeg para macOS | `.herramientas/mac/` | Los usan los `.command` con la conexión de la Mac |
| Chromium 143 arm64 | `.herramientas/chromium/bin/chromium` | Render de Remotion, HyperFrames y HTML (carruseles) |
| Motor Remotion 4 | `Motor/` | Motion graphics (ver `base/motor-graficos.md`) |
| HyperFrames CLI | `.herramientas/hyperframes` | Recorte de persona, color, SFX (ver `hyperframes.md`) |
| whisper.cpp | `.herramientas/whisper/bin/whisper-cli` | Transcripción por palabra con DTW |
| Manuales oficiales | `.herramientas/manuales/remotion`, `.herramientas/manuales/hyperframes` | Leer antes de escribir código para esos motores |

## Transcripción

- `python3 .herramientas/scripts/transcribir.py <video> 3_Videos editados/<nombre>/trabajo/transcripcion` → `palabras.json` + `TRANSCRIPT.md`. Tramos de ~30 s cortados en silencios, **uno por llamada** (cada tramo tarda ~2 min: 1 min de video ≈ 4 min de transcripción); mientras diga `SIGUE`, se repite el comando. Usa `-nfa`: con flash attention, whisper.cpp no calcula las marcas DTW. Probado con el reel de referencia a cámara: 98,6 % de palabras iguales al ASR de CapCut y diferencia mediana de inicio 0,05 s; los nombres propios igual hay que corregirlos ("Blaes" → Blaise, "Compartil" → Compartí).
- Modelo: `.herramientas/whisper/ggml-large-v3-turbo.bin` (~1,6 GB). Si falta, pídele a la persona doble clic en `Instalar modelo Whisper.command`. Mientras falte, usa el ASR de CapCut como fuente (como en el reel de referencia a cámara) y avisa que no está verificado con Whisper.
- Usa las marcas **DTW** (los tiempos normales se desvían en silencios largos). Inicio de palabra ≈ DTW − 0,08 s (el script ya lo aplica).
- Después: corrige términos propios, nombres, términos bíblicos, griego/hebreo y anglicismos (`estilo-por-defecto.md` → Términos propios). Un error de transcripción es un error gráfico.

## Corte

- Los puntos de corte se eligen sobre la **envolvente de energía** del audio, no sobre las marcas de palabra.
- Voz por encima de −35 dB; seguir las colas hasta −44 dB para no cortar el final de las palabras.
- **Por defecto, corte ajustado:** se quitan también las pausas cortas (referencia: mediana de 0,25 s quitados en el reel de referencia a cámara), dejando solo el aire mínimo para que la unión no se coma el arranque ni la cola de la palabra. Si la persona decide para un video pausas más amplias, se conservan las de hasta 0,5 s (respiración natural).
- Micro-fundidos de unos milisegundos en cada unión.

## Zooms y cámara

Los parámetros de la persona (golpe de zoom ~130 % en el corte, escalera 120 → 140 %, acercamiento lento lineal hasta 140 %, salida rápida en 2 fotogramas) están en `estilo-por-defecto.md` → Zoom y cámara. En lo técnico:
- Cada cambio de escala brusco va **en un corte**: si hace falta, divide el clip sin quitar nada.
- Al hacer zoom, sube el encuadre para que la cara quede arriba. En FFmpeg, el `crop` va anclado más arriba del centro; en Remotion, `transformOrigin` va arriba del centro.
- Acercamiento lento: interpolación **lineal** de la escala a lo largo del clip (en Remotion, `interpolate` sin `easing`).

## Voz

- Medir antes de filtrar. Corte de graves a 75 Hz + compresión suave. Objetivo **≈ −14 LUFS / −1 dBTP**.
- Sin reductor de ruido si el margen voz/ruido es bueno (~35 dB): mete artefactos.
- Medir el volumen en **estéreo** (en mono da 3 dB menos y se sobrecomprime).
- Normalizar con **ganancia fija + limitador** (el modo dinámico de `loudnorm` bombea el ruido). Entrega un A/B al mismo volumen.
- **Master final:** `python3 .herramientas/scripts/masterizar_audio.py <entrada.mp4> <salida.mp4>` deja cualquier video en −14 LUFS / ≤ −1 dBTP / AAC 48 kHz, con ganancia fija + limitador sobremuestreado ×4. Copia la imagen sin recodificar y tarda unos segundos. Úsalo en `revision.mp4` y en la exportación de CapCut que la persona quiera publicar. Probado con el reel de referencia a cámara: de −19,5 LUFS y +0,6 dBTP pasó a −14,1 LUFS y −1,4 dBTP.
- Tú mides el sonido pero no lo escuchas: di a la persona qué tiene que escuchar.

## Fotogramas y exportación

- **29,97 fps:** al pasar de 30 a 29,97 no uses un intermedio `.h264` crudo (deja los tiempos de presentación desordenados con fotogramas B y QuickTime lo muestra a saltos). Usa `-itsscale` y comprueba con `ffprobe` que los fotogramas quedan en su sitio.
- Final: H.264 10–20 Mbps (`-c:v libx264 -b:v 16M -maxrate 20M -bufsize 32M -pix_fmt yuv420p`), SDR, y el audio siempre pasado por `masterizar_audio.py`. Si el bruto es HDR (HLG/PQ, frecuente en cámaras de acción y celulares), conviértelo a SDR BT.709 antes (`zscale`/`tonemap`, o pide a la persona que exporte en SDR).
- Capa de subtítulos para un reel: `subtitulos_capa.sh subs.ass <duración> subs.mov 1080x1920 30000/1001 4_Recursos/fuentes` (el tamaño por defecto del script es 16:9).
- Los brutos 4K HEVC pesan mucho: cuida el disco y borra los intermedios pesados al cerrar el video, sin preguntar (ver Borrado de intermedios).

## Motor de gráficos (Remotion)

- `cd Motor` y luego `npx remotion still src/index.ts <Composicion> salida.png --frame=<n>` para revisar un fotograma, o `node render.mjs capas <Composicion> <carpeta> <timeline.json>` para un `.mov` ProRes 4444 por gráfico. `remotion.config.ts` y `render.mjs` ya apuntan al Chromium de `.herramientas` y usan 4 hilos.
- Un render largo no cabe en 180 s: renderiza por gráfico (`capas`) o por rangos (`--frames a-b`) y une con FFmpeg.
- Fuentes del motor en `Motor/public/fuentes/` (cargadas en `src/fuentes.ts`). Si agregas una, cópiala ahí y regístrala.
- Gráficos con alfa: ProRes 4444. Si en CapCut sale con fondo negro: `ffmpeg -i grafico.mov -c:v qtrle grafico_qtrle.mov`.
- Las plantillas (`Texto`, `Tarjetas`, `Abajo`, `Chips`, `Miniaturas`) son genéricas: re-tematízalas con los tokens de la persona y revisa sus textos de ejemplo antes de usarlas.

## Referencias de estilo de otros creadores

- Escribe los links en `2_Referencias/links.txt` (uno por línea, con un nombre de carpeta opcional) y pídele a la persona doble clic en `Descargar referencias.command`. Cada video queda en `2_Referencias/<nombre>/video.mp4` con su `video.info.json`. Solo para estudiar el estilo, nunca para republicar.
- Si algo no baja (un video privado, una historia), la persona puede grabar la pantalla del celular y dejar el archivo en `2_Referencias/<nombre>/`.
