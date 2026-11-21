# Clips verticales desde predicaciones largas

Metodología aprobada por la persona en la serie una serie de clips de referencia (YouTube, original 4K). Produce clips verticales de ~60 s para Reels, TikTok y Shorts. Cada clip junta varios recortes de la predicación en una enseñanza coherente, con recorte milimétrico sin silencios, encuadre vertical que sigue al predicador, subtítulos y, opcionalmente, una placa final que lleva a YouTube. Se entregan siempre dos versiones (subtitulada y limpia) y el `.srt`. Las reglas son de la persona, salvo donde dice "decisión técnica".

## Qué manda en este formato

Este formato tiene reglas propias que **mandan sobre `estilo-por-defecto.md`** en:
- posición de los subtítulos (al centro),
- tipografías (una combinación nueva por video),
- disimulo de los cortes con acercamiento alterno,
- umbral de pausas (0,16 s),
- exportación y placa final.

Todo lo demás se comparte con el estilo por defecto: transcripción literal con voseo, complementaria en cursiva con color, highlight acumulativo, términos propios, versículos NBLA, audio a −14 LUFS y medir antes de entregar.

## 0. Preguntas obligatorias antes de empezar (siempre)

Cada vez que la persona pida clips de un video largo, ANTES de analizar o editar, pregúntale **con la herramienta de preguntas**, no en texto suelto:

1. **¿Quieres agregar al final de los clips la placa que avisa que el video está disponible en YouTube?** Sí / No.
2. Si dice que sí: **¿Tienes la portada (miniatura) del video de YouTube para adjuntarla?** Sin la portada no se arma la placa: pídela y espera. No inventes una portada ni uses una captura del video en su lugar.
3. Si dice que sí: **¿Qué debe decir la leyenda principal de la placa?** Opciones: "MENSAJE COMPLETO", "NUEVA ENSEÑANZA", "EXTRACTO NUEVO" u otro texto (que lo escriba él). La subleyenda "Disponible en YouTube" queda fija, salvo que pida cambiarla.

4. **¿Los subtítulos llevan animación de entrada** (fundido de 50 ms + escala de 106 a 100 %) **o van sin animación?** Se decide en cada video, aclarando que es mínima: «¿Quieres que los subtítulos tengan una animación mínima de entrada? Es apenas un leve golpe que les da un poco de movimiento; si no, aparecen quietos.»

En los clips **no** se hace la pregunta de las pausas: el corte es siempre milimétrico (sección 4).

Si la persona ya respondió alguna en el mismo pedido (por ejemplo, adjuntó la portada y dijo el texto), no la repitas: confirma en una línea lo que entendiste y sigue.

Sin placa: el clip termina en la última palabra, con una salida de audio de 80 ms, y el acento de los subtítulos es el amarillo crema #F6F6A8.

## 1. Análisis y selección de clips

### 1.1 Transcripción con tiempos por palabra

- **Primera opción (decisión técnica, nov 2026): Whisper local** sobre el audio del original 4K, en la computadora de la persona. Extrae un WAV de 16 kHz y corre `transcribir.py` (ver `entorno-y-herramientas.md`). Da tiempos DTW por palabra. Una hora de video lleva ~4 horas de proceso en tramos. Por eso, **si el video está en YouTube, primero lee sus subtítulos automáticos** (la alternativa de abajo, un par de minutos) para encontrar los momentos candidatos, y después transcribe con Whisper, con precisión, solo esos tramos: los subtítulos de YouTube sirven para elegir, no para editar. Si no está en YouTube, ofrece transcribirlo entero o solo los minutos que indique: «Este video dura una hora. ¿Está subido a YouTube? Si me pasas el enlace, leo sus subtítulos para encontrar los mejores momentos y después transcribo con precisión solo esos tramos. Si no está en YouTube, puedo transcribirlo entero (unas 4 horas) o puedes decirme en qué minutos están las partes que te interesan.»
- **Alternativa (cuando solo hay link o para comparar): subtítulos automáticos de YouTube desde el Chrome de la persona** (Claude in Chrome), con JavaScript en la página:
  1. Activar los subtítulos en español: `movie_player.loadModule('captions')` y `setOption('captions','track',{languageCode:'es'})`.
  2. Leer en `performance.getEntriesByType('resource')` la URL de `timedtext` que usó el reproductor: ya trae el token. Un fetch directo a `baseUrl` devuelve vacío.
  3. Volver a pedirla con `fmt=json3`: trae `tStartMs` por evento y `tOffsetMs` por palabra.
  - La salida del JavaScript tiene un límite de ~1000 caracteres. Para textos largos, mete el texto en un `<article>` invisible de la página y léelo con `get_page_text`.
- Revisa la transcripción a mano: nombres, términos bíblicos y lógica del texto.

### 1.2 Intensidad de la voz

- **Primera opción (decisión técnica): medir sobre el WAV del original** en la computadora de la persona, con numpy:
  - volumen (RMS en dB) en bloques cortos,
  - tono por autocorrelación entre 70 y 400 Hz,
  - resumen por segundo: volumen máximo y tono medio, comparados con el promedio de toda la predicación.
  - **Intensidad = desviaciones de volumen + 0,5 × desviaciones de tono**, suavizada en ±3 s.
- **Alternativa sin el archivo (Chrome):** reproducir el video silenciado a 2,5–4x, con un ScriptProcessor de Web Audio conectado al `<video>` (salida en cero) que mide RMS, tono y el tiempo del video. Problemas conocidos:
  - YouTube pausa ("¿sigues mirando?"): vigilar y reanudar.
  - Al terminar salta al video siguiente: cortar la medición cuando el tiempo retrocede.
  - Navegar a otra página borra los datos: calcular todo antes de salir.
  - En una segunda medición, el volumen del reproductor puede cambiar: calibrar con fragmentos ya medidos (en la serie, la diferencia fue de +0,3).

### 1.3 Elegir los clips

- Cruza los picos de intensidad con el contenido: frases contundentes, ganchos, ilustraciones, momentos proféticos o de ministración.
- Descarta los picos que son aplausos o risas del público (trivias, juegos) y las frases que fuera de contexto pueden leerse como polémicas.
- **Los momentos clave que marque la persona tienen prioridad.**
- Cada clip:
  - dura ~60 s (aceptable entre 49 y 63 s),
  - se arma con 1 a 6 recortes, que pueden venir de momentos distintos,
  - sigue el arco gancho → desarrollo → clímax → cierre.
- **Revisión de puentes:** antes de cerrar un clip, revisa si a algún salto le falta contexto. Si falta, agrega la frase puente aunque haya que recortar otra cosa. Ejemplos reales:
  - "las tensiones te van a hacer amar al que piensa diferente" antes de "la unidad de la fe no es pensar igual",
  - quién era Bernabé antes de "¿de quién vas a ser el Bernabé?",
  - "¿qué puede hacer Dios cuando Satanás nos dice que somos anónimos?" para pasar del dato histórico a la persona que mira.
- Quita las frases repetidas entre recortes o las que quedan sueltas (ej.: "Toda yo oro en el nombre de Jesús, que…" entre dos ideas que deben ir seguidas).
- Presenta las propuestas en una **página (Artifact)** con:
  - ranking,
  - cada corte con su inicio y fin, link a YouTube en ese segundo y la frase,
  - la intensidad de cada corte,
  - el porqué y un texto de gancho sugerido.
- **La persona aprueba antes de editar.**

### 1.4 Propuestas de otras IA

Si la persona trae propuestas de otra IA (por ejemplo Gemini), verifícalas contra la transcripción. Errores típicos encontrados:
- tiempos redondeados al segundo, que cortan a mitad de palabra,
- clips de 100–110 s cuando se pedía 1 minuto,
- citas no textuales,
- tiempos corridos varios segundos.

## 2. Flujo técnico con el original 4K

### 2.1 Dónde se trabaja

- **Dónde va el original:** la persona deja el original 4K (HEVC 3840×2160, 25 fps; ~8 GB por hora) en `1_Videos sin editar/` de la carpeta Editor de Videos IA. Si todavía está en otra carpeta (por ejemplo "Escritorio/Videos YT"), pídele que lo arrastre a `1_Videos sin editar/` desde el Finder: en el mismo disco es instantáneo. No lo copies tú: duplicarías 8 GB.
- **Decisión técnica (nov 2026): todo el proceso corre en la computadora de la persona** (`device_bash`). Ahí ya están FFmpeg, Python con OpenCV 4.10 (`.herramientas/venv`) y el modelo YuNet (`.herramientas/modelos/face_detection_yunet_2023mar.onnx`). A la nube solo se pasan imágenes para mirarlas (hojas de contactos, fotogramas). Así no hay límites de 30 MB ni archivos que ir y venir.
- Intermedios (proxies, HQ verticales, audio, recorridos, versiones de revisión) en `3_Videos editados/<serie>/trabajo/`: es temporal y se borra al cerrar la serie. Lo que se guarda está en la sección 8.
- La duración del original coincide con la del video de YouTube, así que los tiempos coinciden 1:1. **Verifícalo en cada video.**

### 2.2 Límites conocidos (decisiones técnicas)

- Cada llamada a `device_bash` dura como máximo 180 s y los procesos en segundo plano mueren al terminarla. Divide los renders largos en partes de ~21 s (unos 330 cuadros a 25 fps), que se decodifican en ~60 s.
- Si hace falta pasar archivos entre la Mac y la nube: subirlos tiene un máximo de 400 MB por archivo (si falla con "upload failed", reintenta de a uno); devolverlos, 30 MB por archivo (de a uno, y reintenta si se corta).
- **Bug de caché al devolver archivos:** si se devuelve un archivo con la misma ruta que uno anterior, puede llegar la versión vieja. Usa nombres nuevos y únicos, o escribe los textos chicos directo en la Mac con `device_bash`. Verifica en destino con `md5sum` o `head`.
- Los intermedios se borran sin preguntar (ver `entorno-y-herramientas.md` → Borrado de intermedios): al cerrar la serie se vacía `trabajo/` y se quitan las versiones anteriores.
- La Terminal de macOS no se usa. Lo que necesite la conexión de la Mac va por un `.command` que la persona abre con doble clic.

### 2.3 Pasos

1. Para cada recorte (cortes exactos, sin márgenes extra), con `-ss` ANTES de `-i`:
   - un proxy de 960×540 (h264 veryfast, CRF 23),
   - el audio en WAV PCM.
2. Analiza: rostros, cambios de cámara y silencios.
3. Genera el recorrido del recorte (archivo `sendcmd`, ver 3.2).
4. Renderiza un **HQ vertical nativo**: recorte de 1215×2160 del 4K que sigue al predicador, sin escalar, h264 CRF 15. Así los acercamientos posteriores no pierden calidad.
5. Edición fina, audio, subtítulos, placa y exportación final sobre los HQ.
6. Entrega (sección 8): se guarda solo la final con subtítulos; la limpia y el `.srt`, en el chat.

## 3. Encuadre vertical 9:16

### 3.1 Detección del predicador

- YuNet (OpenCV `FaceDetectorYN`), modelo `face_detection_yunet_2023mar.onnx`. Si hay que volver a bajarlo, viene de media.githubusercontent.com: raw.githubusercontent devuelve solo el puntero de LFS.
- **No funcionan:** las Haar cascades (falsos positivos con las calcomanías de la laptop y con caras del público) ni el HOG de personas (el público lo tapa).
- Solo cuentan las caras de la **mitad superior** de la imagen: el público está abajo.
- **Cambios de cámara:** diferencia de histograma HSV con Bhattacharyya mayor a 0,3.
- Dentro de cada plano:
  - al principio se toma la cara más grande,
  - después se sigue la más cercana a la anterior,
  - se descartan los saltos de más de 0,12 del ancho (otra cara del público),
  - se interpola y se suaviza hacia adelante y hacia atrás con coeficiente 0,25,
  - nunca se suaviza a través de un cambio de cámara.

### 3.2 Recorte

- Ancho del recorte: 1215/3840 del cuadro, centrado en la cara y limitado a los bordes.
- **Bug del cuadro de retraso:** `sendcmd` aplica el valor un cuadro tarde. En cada cambio de cámara, el primer cuadro mostraba la zona equivocada; parecía "un cuadro del público" y la persona lo detectó en 0:02 y 0:29.
  - Corrección: adelantar los comandos 0,04 s y poner como valor inicial del filtro de recorte la primera posición.
  - Verificación: buscar "cuadros de un solo cuadro" (dos diferencias grandes seguidas en el render). Tiene que dar cero.
- **Planos abiertos desde el fondo** (cara de menos de 0,115 del alto del cuadro): acercamiento base de 1,3–1,4, porque si no domina el público.
- Revisa una hoja de contactos de todo el clip (un cuadro cada 1–1,2 s). Si en algún plano se pierde al predicador, rehaz ese tramo desde el 4K con un recorrido corregido.
- Normal: la pantalla del fondo (transmisión en vivo) puede mostrar "dos Nicos". No es un error del recorte.

## 4. Edición milimétrica: cortes y silencios

### 4.1 El pedido

"Revisión fina y edición milimétrica": reducir al máximo los silencios, aunque sean pequeños, y que los empalmes parezcan cambios de cámara, no cortes.

### 4.2 Detección de silencios

- Energía en ventanas de 10 ms, suavizada en 3 ventanas.
- Umbral según cada fuente, a partir de sus percentiles:
  - fuentes limpias: −42 a −44 dB,
  - con música de fondo o más ruido: −37 a −40 dB.
- En tramos rápidos sin pausas claras, busca caídas de más de 18 dB respecto del máximo local de ±0,6 s.
- Cruza cada pausa con las palabras: tiene que caer entre palabras. La transcripción de YouTube puede estar corrida ±0,1–0,2 s; **manda la energía del audio**.

### 4.3 Reglas de recorte

- **Quita toda pausa de 0,16 s o más** y deja 0,04 s de cada lado (pausa final de ~0,08 s).
- **Las pausas de menos de 0,16 s se dejan:** cortarlas genera saltos de imagen demasiado seguidos.
- Bordes de cada recorte:
  - inicio en el arranque de la voz menos 0,03 s,
  - final en la última sílaba más ~0,04–0,06 s.
  - Ojo con los primeros 0,1 s de un recorte: pueden traer la cola de la palabra anterior (ej.: "decir," antes de "No te rindas").
- Calza los cortes a cuadros exactos (25 fps).

### 4.4 Disimular los cortes como cambios de cámara

- En cada salto, alterna el acercamiento: **1,00 ↔ 1,16**. En planos abiertos: 1,3/1,4 ↔ ×1,16.
- Si dos recortes seguidos son del mismo ángulo (por ejemplo, frente con frente), el segundo entra más cerrado.
- Si un salto cae a menos de 0,28 s de un cambio de cámara real, quedaría un plano de 2–7 cuadros (un parpadeo). Solución:
  - el video arranca en el cambio de cámara,
  - el audio arranca donde corresponde,
  - el hueco se rellena repitiendo el primer cuadro (`tpad` clone).
  - Si el salto cae poco después de un cambio de cámara (≤0,12 s), el video termina en el cambio y se repite el último cuadro.
- Divide los recortes en cada cambio de cámara para aplicar el acercamiento por plano.

### 4.5 Render de la edición (decisión técnica)

- **No** uses un `filter_complex` gigante con decenas de `trim` sobre la misma entrada: se queda sin memoria y el proceso muere.
- Renderiza cada pedazo por separado:
  - video: `-ss` antes de `-i` sobre el HQ, `-frames:v` exactos, recorte del acercamiento, escala a 1080×1920 lanczos, CRF 14;
  - audio por separado.
- Une todo con el concat demuxer (stream copy).

## 5. Audio

### 5.1 Pedazos

- **SIEMPRE `-ss` ANTES de `-i`** al extraer cada pedazo. Con `-ss` después de `-i`, los filtros ven los tiempos originales y `afade=out:st=X` silencia el pedazo entero. Así se perdieron ~30 s de audio en un clip entregado, y la persona lo detectó.
- Fundido de entrada de 6 ms y de salida de 8 ms solo en los pedazos con salto. Los pedazos contiguos (cambio de cámara sin corte) van sin fundido.

### 5.2 Volumen

- −14 LUFS, pico verdadero ≤ −1,5 dBTP, LRA 11, sin bombeo: `loudnorm` en dos pasadas en **modo lineal**, o `masterizar_audio.py --tp -1.5` (ganancia fija + limitador).

### 5.3 Verificación obligatoria antes de entregar (sobre el audio extraído del MP4 final)

- Cero tramos de silencio digital (muestras en 0) de más de 5 ms dentro de la parte hablada.
- Ninguna pausa de más de 120–150 ms por debajo de −45 dB.
- Cada empalme con salto cae en voz baja (−35 a −45 dB) a ambos lados. Los empalmes con voz alta solo pueden ser contiguos.
- Duración del audio igual a la del video (±0,02 s).
- Avisa siempre que mediste pero no puedes escuchar, y pide que lo escuche entero.

## 6. Subtítulos

### 6.1 Contenido

- Texto exacto: voseo, acentos, nombres propios. Sin resumir ni reescribir.
- Correcciones de estilo que pidió la persona (siempre, **solo en este formato**):
  - sin signos de interrogación de apertura ni de cierre ("qué es lo que", "por nosotros"). **Excepción:** si es claramente una pregunta completa, con su inicio y su fin dentro del mismo bloque o de bloques seguidos ("¿de quién vas a ser el Bernabé?"), los signos sí van;
  - "satanás" con minúscula,
  - sin puntos ni comas al final del bloque.
- Las muletillas o tropiezos ("lo, el llamado") se pueden sacar del subtítulo, pero se avisa en la entrega.
- Revisa los errores de la transcripción automática contra el audio y la lógica del texto.

### 6.2 Estructura

- Bloques cortos de 2 a 5 palabras, en una línea siempre que se pueda (~26 caracteres como máximo).
- **Ancho máximo: 600 px** (zona segura unificada IG + TikTok , `zona-segura.md`: a la altura de los subtítulos la columna de botones empieza en x = 840, así que un renglón centrado va de 240 a 840). Mide el ancho real dibujando el texto; el máximo de la serie anterior fue 687 px, así que esos renglones ahora se parten.
- Un solo estilo por video (bloques cortos). Dos líneas como máximo.
- Cada bloque empieza en su primera palabra menos 0,05 s y termina en el inicio del siguiente: sin huecos ni superposiciones, y el primero no empieza en tiempo negativo.
- Los tiempos se recalculan a la línea de tiempo editada: cada palabra se ubica en el pedazo que la contiene. Si cae en un tramo eliminado, pasa al inicio del pedazo siguiente.

### 6.3 Tipografías

- **No repetir la combinación del video anterior.** En cada video nuevo, propón una combinación distinta:
  - una base sans bold muy legible,
  - una complementaria serif en cursiva para las palabras clave,
  - máximo dos tipografías por secuencia.
- Combinaciones usadas (no repetirlas en la serie siguiente):
  - Bricolage Grotesque Bold + Instrument Serif Italic (versión 1),
  - **Manrope ExtraBold + DM Serif Display Italic** (aprobada).
- Las fuentes vienen de raw.githubusercontent.com/google/fonts/main/ofl/… y se guardan en `4_Recursos/fuentes/`.
- Si la fuente es variable, saca una versión fija del peso que necesitas con `fonttools varLib.instancer` (ej.: wght=800). libass toma el peso por defecto de la variable, que no es el buscado.
- Pasa `fontsdir` al filtro ass y verifica en el log que cargó las fuentes.
- Generador: `subtitulos.py --formato clip --base <base.ttf> --complementaria <cursiva.ttf> --tam-base <px> [--acento #RRGGBB] [--sin-animacion]` y después `verificar_subtitulos.py --formato clip`.

### 6.4 Medidas (1080×1920)

- **Base: el mismo tamaño visual que los 11 pt de CapCut del estilo por defecto, en TODO el video.** Con Manrope ExtraBold, eso es 68 en el ASS (PlayResY 1920). El número cambia con la fuente (Cal Sans da 50 para la misma altura), porque cada fuente tiene otras proporciones. Con una combinación nueva, calcula el tamaño igualando la altura de las minúsculas a la de la referencia aprobada (decisión técnica).
- **Palabra clave:** serif cursiva con su tamaño compensado (DM Serif 84 con Manrope 68) y el color de acento (6.7).
- **Posición: al centro de la pantalla** (el 0 del eje en CapCut). Anclaje superior (`\an8`) en y = 922 para la primera línea. En los bloques de dos líneas, la primera queda SIEMPRE en el mismo lugar que los de una línea y la segunda va debajo.
- Sombra muy suave y difusa: una capa de abajo con el mismo texto en negro, alfa 0x70, `\blur14`. Sin contorno ni sombra dura.
- Dentro de la zona segura unificada (`zona-segura.md`).

### 6.5 Interlineado de dos líneas (regla permanente)

"Lo más cercano posible sin que se toquen las líneas." No se usa un valor fijo. Para cada bloque:
1. dibuja cada línea sola sobre negro y mide dónde empieza y termina la tinta (incluye las letras que bajan, como q, p, g, y las que suben en la cursiva, como ll o la ñ);
2. ubica la línea 2 de modo que su tinta empiece **6 px debajo** del final de la tinta de la línea 1.

Ejemplo: con Manrope 68 y DM Serif 84, el salto entre líneas dio 51 px.

### 6.6 Highlight acumulativo

- 1 o 2 frases clave por clip, normalmente el clímax o el cierre.
- Las palabras se suman de a una cuando se dicen, sin que el texto se mueva, hasta armar la frase completa. Técnica: cada evento contiene la frase entera y las palabras que todavía no se dijeron van con alfa FF.
- Solo las palabras clave llevan la cursiva serif y el color.
- Ejemplos: "no es para quebrarte a vos / es para quebrar tu *orgullo*", "un Dios que nos ve / un Dios que no se *olvida*", "Dios está *reiniciando* / su propósito en nosotros".

### 6.7 Color de acento

- **Sin placa final:** amarillo crema #F6F6A8.
- **Con placa final:** se deriva del color de fondo de la placa, que sale de la portada (7.1). Una versión pastel o muy clara de ese tono, que combine y siga contrastando.
  - Ejemplo aprobado: placa #E27934 (naranja de la portada) → acento durazno claro #FFC896 (en ASS, `&H96C8FF&`).
  - Nunca un tono saturado u oscuro que pierda contraste.
- Pruébalo sobre ropa oscura y sobre fondos claros (pared blanca, pantalón claro). Si se pierde, sube la posición o refuerza la sombra.

## 7. Placa final "Disponible en YouTube" (solo si la persona la pidió en 0)

### 7.1 Diseño

- Lienzo 1080×1920, 25 fps, 4,0 s.
- **El color de fondo SIEMPRE combina con la portada que adjunta la persona.** No hay un color fijo.
  - Muestrea varios píxeles del color dominante de la portada (fondos y zonas planas, no piel ni texto) y elige un tono de esa familia, un poco más brillante que el promedio, para que la miniatura se despegue.
  - Ejemplo aprobado: portada naranja → fondo #E27934 (226,121,52).
  - Si la portada no tiene un color dominante claro (muy oscura o muy variada), propón 2 o 3 colores tomados de ella, con una muestra, antes de renderizar.
  - El triángulo del ícono va del mismo color que el fondo.
  - El acento de los subtítulos sale de este color (6.7).
- **Zona segura unificada IG + TikTok** (`zona-segura.md`): izquierda 120 px, y desde y = 720 nada a la derecha de x = 840 (columna de botones). Vale para cualquier texto o gráfico de la placa.
- Miniatura (la portada adjunta):
  - 720 px de ancho (alto proporcional), de x = 120 a 840 (alineada a la izquierda con el texto, para no pisar la columna de botones; antes 860 px centrada), borde superior en y = 600,
  - radio de 22 px,
  - sombra suave: 18 px hacia abajo, en un tono oscuro del color del fondo (con el naranja, RGB 60,30,0), alfa 120, desenfoque 28.
- Texto abajo a la izquierda, alineado con el borde de la miniatura:
  - **Leyenda principal: el texto que eligió la persona en la pregunta de la sección 0**, en mayúsculas, Manrope ExtraBold 58 px, RGB(20,20,20), 48 px debajo de la miniatura. Si es largo y choca con el ícono, achícalo de a 2 px hasta dejar al menos 40 px libres antes del ícono. Nunca lo pases a dos líneas sin consultarle.
  - "Disponible en YouTube": Manrope ExtraBold 36 px, mismo color con alfa 200, 74 px más abajo.
- Ícono abajo a la derecha:
  - botón de reproducir **genérico**, sin el logo oficial de YouTube (si lo quiere, la persona lo agrega en CapCut sobre la versión limpia),
  - rectángulo redondeado negro (RGB 20,20,20) de 120×85, radio 24, con un triángulo del color del fondo,
  - centrado verticalmente con el bloque de texto (centro = y de la leyenda + 58 px) y alineado con el borde derecho de la miniatura,
  - mismo peso visual que el texto (al principio medía 150×106 y quedaba grande).

### 7.2 Animación (ease-out cúbico: e(t) = 1 − (1 − t)³)

- 0–0,40 s: **el fondo sube desde abajo (slide up).** Es lo único que se mueve.
- 0,25–0,85 s: la miniatura y su sombra aparecen solo con fundido: sin subir, sin escala y sin giro.
- 0,60–1,00 s: la leyenda principal con fundido. 0,72–1,10 s: "Disponible en YouTube" con fundido.
- 0,95 s: el ícono aparece con efecto click, centrado y sin moverse de su lugar:
  - escala 0,6 → 1,15 en 0,10 s,
  - 1,15 → 0,88 en 0,08 s (la presión),
  - 0,88 → 1,0 en 0,12 s,
  - opacidad de 0 a 1 en 0,08 s.
- Después, todo quieto.
- Correcciones de la persona: el fondo SÍ sube (un fundido del fondo fue descartado); los demás elementos NO suben (la primera versión, con rebote, giro y subida, fue descartada).

### 7.3 Sonido

- **Whoosh con el slide up:** ruido de 0,45 s con un pasabajos que abre progresivamente (coeficiente de 0,03 a 0,38), envolvente sen(π·x)^1,5, ganancia 0,42 (estaba en 0,16; pidió subirla).
- **Click en la presión del ícono (t = 1,05 s):** transitorio de 35 ms con tres capas:
  - ruido con caída exp(−420t) × 0,35,
  - seno de 1800 Hz con caída exp(−260t) × 0,30,
  - seno de 420 Hz con caída exp(−120t) × 0,25.
- Sin "pop", sin música y sin otros efectos: el resto de la placa queda en silencio.
- Los efectos se generan con numpy y se guardan como WAV estéreo de 48 kHz y 16 bits.
- Coincide con las dos familias de sonido de la persona: whoosh cuando algo se mueve, clic cuando algo aparece.

### 7.4 Sincronía: la placa arranca con la última palabra

- Mide en el audio editado dónde termina la última sílaba (caída final por debajo de unos −24 dB): ese instante es **TS**. En el ejemplo, la palabra fue "nosotros" y TS = 49,30 s en un clip de 49,40.
- La placa se genera como PNG RGBA transparentes (100 cuadros) y se superpone desde TS sobre el video todavía en movimiento. Nunca se pega al final del archivo: queda una pausa muerta.
- El video base se extiende repitiendo su último cuadro (`tpad stop_mode=clone`) durante 4,2 s.
- Los subtítulos se queman ANTES de superponer la placa.
- Audio: la voz con fundido de salida de 80 ms desde TS; los efectos con `adelay` = TS en milisegundos; mezcla con `amix … normalize=0` (que no baje la voz).
- Duración final = TS + 4,0.
- Comando de referencia (desde `trabajo/`; saca las dos versiones en una pasada: la subtitulada se guarda en la carpeta de la serie y la limpia queda en `trabajo/` para mandarla por el chat; TSMS = TS en milisegundos, por ejemplo 49300; TOTAL = TS + 4,0):

```bash
ffmpeg -i video.mp4 -i audio.wav -framerate 25 -i card/%03d.png -i card_sfx.wav -filter_complex "
[0:v]tpad=stop_mode=clone:stop_duration=4.2,trim=duration=TOTAL,setpts=PTS-STARTPTS,split=2[b0][b1];
[b1]ass=subs.ass:fontsdir=FONTS[bs];
[2:v]setpts=PTS-STARTPTS+TS/TB,format=rgba,split=2[k0][k1];
[bs][k0]overlay=eof_action=repeat[os];[b0][k1]overlay=eof_action=repeat[ol];
[1:a]afade=t=out:st=TS:d=0.08,apad[ma];[3:a]adelay=TSMS|TSMS[sx];
[ma][sx]amix=inputs=2:duration=first:normalize=0,atrim=duration=TOTAL,asplit=2[a1][a2]" \
-map "[os]" -map "[a1]" -c:v libx264 -preset slow -b:v 20M -maxrate 20M -bufsize 40M -pix_fmt yuv420p -c:a aac -b:a 320k -ar 48000 -movflags +faststart "../NN Titulo vN.mp4" \
-map "[ol]" -map "[a2]" -c:v libx264 -preset slow -b:v 20M -maxrate 20M -bufsize 40M -pix_fmt yuv420p -c:a aac -b:a 320k -ar 48000 -movflags +faststart "NN Titulo vN - limpio.mp4"
```

## 8. Exportación y entrega

- **Mejor calidad:** 1080×1920, 25 fps (los del original), H.264 `-preset slow -b:v 20M -maxrate 20M -bufsize 40M`, yuv420p, audio AAC 320 kbps a 48 kHz, `+faststart`. Los 3,5 Mbps de la serie anterior eran solo para que el archivo entrara en los 30 MB de traspaso desde la nube; ahora el render se hace directo en la Mac.
- **Qué se guarda y dónde:** Todo vive en la carpeta **Editor de Videos IA**. En la carpeta solo se guarda **la versión final con subtítulos**, en la mejor calidad. La versión limpia (sin subtítulos), el `.srt` y cualquier otra capa se le muestran a la persona **en el chat** para que los descargue si los necesita, pero no se guardan en la carpeta.
  - Se guarda: `3_Videos editados/<serie>/NN Título vN.mp4` (con subtítulos y, si corresponde, la placa).
  - En el chat (no se guardan): "NN Título vN - limpio.mp4" y "NN Título vN.srt". Se generan en `trabajo/`, se le pasan a la persona por el chat y se borran al cerrar.
- Mientras hay revisiones, cada versión lleva su número. Cuando la persona aprueba, queda solo la final: las versiones anteriores y `trabajo/` se borran, sin preguntar.
- **Portada de cada clip:** un fotograma del predicador en un gesto fuerte del clip más una frase del clip, con las tipografías de la serie; todas las portadas de una misma serie llevan el mismo diseño. 1080 × 1920, lo esencial en el centro 1080 × 1350; una principal y una alternativa (`portadas.md`). La elegida se guarda junto al clip.
- En el mensaje de entrega: qué cambió, qué verificaste y qué no puedes verificar (escucharlo). Sin rellenos.

## 9. Control de calidad (antes de cada entrega)

**Inicio**
- [ ] Hice las preguntas de la sección 0 (placa sí/no, portada, leyenda) o confirmé las respuestas que ya me dio.

**Imagen**
- [ ] Hoja de contactos de todo el clip: el predicador encuadrado en todos los planos.
- [ ] Cero parpadeos de un cuadro en los cambios de cámara.
- [ ] Los empalmes con salto alternan el acercamiento. No quedan planos de menos de 8 cuadros.
- [ ] Los planos abiertos están acercados y no domina el público.

**Audio**
- [ ] Cero silencios digitales de más de 5 ms en la parte hablada. Ninguna pausa de más de 0,15 s.
- [ ] Empalmes en voz baja. −14 LUFS y ≤ −1,5 dBTP sin bombeo.

**Subtítulos**
- [ ] Texto literal con las correcciones (sin ¿? salvo preguntas completas, "satanás" en minúscula, sin puntuación final).
- [ ] Animación de entrada según lo que la persona eligió para este video.
- [ ] Mismo tamaño en todo el video. Al centro. Primera línea siempre en el mismo lugar.
- [ ] Interlineado medido (6 px de tinta a tinta) en cada bloque de dos líneas, revisado ampliado.
- [ ] Acento correcto: crema sin placa, o la versión clara del color de la placa. Legible sobre fondos claros y oscuros.
- [ ] Ningún renglón de más de 600 px. Todo dentro de la zona segura unificada (`zona-segura.md`).

**Placa (si corresponde)**
- [ ] El fondo combina con la portada adjunta (color tomado de ella).
- [ ] La leyenda dice exactamente el texto que eligió la persona esta vez.
- [ ] El slide arranca en el cuadro de la última palabra (revisa 0,1 s antes y después).
- [ ] Solo el fondo sube; lo demás con fundido. Ícono con click y sonido sincronizado.
- [ ] Whoosh claramente audible. Ícono genérico. Miniatura, texto e ícono dentro de x 120–840.

**Archivos**
- [ ] En la carpeta, solo la final con subtítulos (20 Mbps, AAC 320 kbps). La limpia y el `.srt`, enviados por el chat.
- [ ] Contenido verificado en destino (`ffprobe`, `md5sum`).

## 10. Errores ya cometidos (no repetir)

1. Fundidos de audio con `-ss` después de `-i`: se perdieron ~30 s de audio. Siempre `-ss` antes de `-i`, y verificar silencios digitales.
2. Cuadro de retraso de `sendcmd` en los cambios de cámara: cuadros con la zona equivocada. Adelantar 1 cuadro y verificar parpadeos.
3. El detector siguió una cara del público en un plano abierto y el predicador salió de cuadro: seguimiento con rechazo de saltos, y rehacer ese tramo desde el 4K.
4. Un `filter_complex` enorme se quedó sin memoria: renderizar por pedazos.
5. Devolver archivos con la misma ruta trajo la versión vieja: nombres únicos y verificación en destino.
6. Placa pegada al final del archivo: pausa muerta. Superponerla desde el final de la última palabra.
7. Interlineado fijo de 80 px: demasiado aire. Medir la tinta en cada bloque.
8. Elementos de la placa que subían o rebotaban: descartado. Solo el fondo sube.
9. Leyenda de la placa sin consultar: siempre preguntar el texto (sección 0) y no reutilizar el del clip anterior.
