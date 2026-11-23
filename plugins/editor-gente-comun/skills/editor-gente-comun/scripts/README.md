# Scripts

Se ejecutan en la carpeta de trabajo de la persona, copiados en `.herramientas/scripts/` (ver `../references/entorno-y-herramientas.md`). Siempre desde la raíz de la carpeta y con `source .herramientas/scripts/entorno.sh`.

Partes mecánicas del flujo. Requieren FFmpeg; los `.py` requieren Python 3 (y `medir_sonido.py`, numpy). Ninguno modifica los archivos originales.

| Script | Para qué | Uso |
|---|---|---|
| `preparar_entorno.sh` | Estado e instalación de las herramientas, por pasos | `preparar_entorno.sh [estado\|<paso>]` |
| `entorno.sh` | Rutas, fontconfig, Whisper, Chromium, caché del recorte | `source .herramientas/scripts/entorno.sh` |
| `transcribir.py` | Transcripción por palabra (whisper.cpp + DTW), por tramos y reanudable | `transcribir.py <video> <carpeta_salida>` |
| `subtitulos.py` | Subtítulos con el estándar del editor → `.ass` + `.srt` | `subtitulos.py --palabras p.json --bloques b.txt --fin <s> --salida <ruta>` |
| `verificar_subtitulos.py` | Mide tamaños, posiciones y anchos de un `.ass` | `verificar_subtitulos.py subs.ass` |
| `recorte_persona.sh` | Recorta a la persona del fondo (HyperFrames, local), reanudable | `recorte_persona.sh <video> <ini> <fin> <carpeta> <salida.mov>` |
| `masterizar_audio.py` | Audio final a −14 LUFS / ≤ −1 dBTP / 48 kHz, con la imagen intacta | `masterizar_audio.py in.mp4 out.mp4` |
| `portada_yt.py` | Portada de YouTube | ver `../references/imagenes.md` |
| `extraer_frames.sh` | Analizador: cortes, primer/último fotograma de cada plano, fotogramas por intervalo | `extraer_frames.sh video.mp4 2_Referencias/<n>/datos [umbral] [intervalo]` |
| `medir_ritmo.py` | Analizador: media, mediana, cortes por minuto (gancho y cuerpo) | `medir_ritmo.py 2_Referencias/<n>/datos [--gancho 30] [--excluir "245-269"]` |
| `medir_sonido.py` | Analizador: golpes de sonido, nivel respecto a la voz, color, % de cortes con golpe | `medir_sonido.py video.mp4 2_Referencias/<n>/datos [--excluir …]` |
| `buscar_sfx.py` | Sonido: busca y baja grabaciones reales CC0/CC BY de Openverse, hoja + escucha + créditos (**en la nube**) | `--temas` · `--tema shofar --oir` · `"wooden door" --max 4` · `--todos` |
| `sonidos_biblicos.json` | Sonido: 51 temas bíblicos con su búsqueda en inglés | lo lee `buscar_sfx.py` |
| `oido.sh` | Sonido: el oído (Earshot): revisar mezcla, elegir, A/B, grabado o sintético, perfil (**en la nube**) | `bash oido.sh revisar mezcla.mp3 "1.5,3.2"` |
| `voz_sintetica.py` | Voz: narración sintética con Kokoro (abierta, sin conexión una vez instalada) **solo si la persona la pide**; 3 voces en español (**en la nube**) | `voz_sintetica.py muestras` · `voz_sintetica.py guion.txt --voz em_alex` |
| `musica_estilo.py` | Música: cama hecha con código para los estilos precargados: `chip` (RPG), `campanas` (isla, diorama), `cosmos` (escala sin fin) | `musica_estilo.py chip --dur 62` |
| `afinar_sfx.py` | Sonido: corre un sonido con tono hasta ±2 semitonos para que no desafine | `afinar_sfx.py s.wav --musica m.wav --en 12.4` |
| `hoja_contactos.sh` | Revisión: un fotograma de TODOS los gráficos en una imagen | `hoja_contactos.sh 3_Videos editados/<n>/trabajo/entrega/2_GRAFICOS hoja.png [segundo] [columnas]` |
| `zona_segura.py` | Revisión: superpone la zona segura unificada IG + TikTok sobre un fotograma 1080×1920 | `python3 zona_segura.py fotograma.png salida.jpg` |
| `rejilla.sh` | Gráficos: rejilla de décimas sobre una captura para leer coordenadas | `rejilla.sh captura.png captura_rejilla.png` |
| `subtitulos_capa.sh` | Entrega kit: subtítulos `.ass` como capa ProRes 4444 con alfa | `subtitulos_capa.sh subs.ass <duración> subs.mov [1920x1080] [30] [fuentes]` |
| `quemar_subtitulos.sh` | Entrega vídeo único: quemar el `.ass` | `quemar_subtitulos.sh in.mp4 subs.ass out.mp4 [fuentes]` |

Notas:
- La detección de cortes es aproximada: con movimiento fuerte o zooms puede marcar de más. Ajusta el umbral (0,2 más sensible, 0,4 menos) y revisa `cortes/` si una cifra parece rara.
- `medir_sonido.py` puede confundir el arranque de una frase con un golpe (los marca como `dudoso_voz`). Verifica escuchando los golpes que importen.
- La carpeta de trabajo tiene espacios en el nombre ("Editor de Videos IA"): en filtros de FFmpeg (subtítulos) usa rutas **relativas** desde la carpeta del archivo (`cd` antes), nunca absolutas.
- El resto del flujo (transcripción, corte, limpieza de voz, render de gráficos, vista previa, exportación del kit) lo construye Claude con FFmpeg, el transcriptor y el motor de gráficos siguiendo las referencias.
