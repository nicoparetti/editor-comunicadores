# Reels con efectos visuales (motion graphics)

Lineamientos fijos para un reel guionado a cámara con gráficos encima. Salen de un reel de referencia trabajado en cinco rondas de corrección y valen para todos los reels de este tipo. **El estilo gráfico (colores, tipografías, papel/oscuro) puede cambiar en cada video; lo que sigue no**: formatos, animación, sincronía, maquetación, sonido, cortes y zooms. Si un video pide otra cosa, gana el pedido de la persona y se anota en la hoja.

Manda sobre `base/` y se complementa con `estilo-por-defecto.md` (subtítulos, exportación). Plantillas de código en `templates/reel-graficos/`.

## 1. Antes de diseñar nada

1. **Medir el encuadre del bruto** (la persona lo pidió como paso obligatorio): detectar la cara con YuNet en 1 fotograma por segundo y sacar la mediana de cabeza, mentón y centro x, más hasta dónde bajan las manos. Las zonas de abajo se recalculan para cada bruto; los números son los de un plano sentado típico (1080×1920): cara y ≈ 300–680 (mentón ≈ 700), subtítulos con su borde superior en y ≈ 1242.
2. **Tableros de estilo sobre fotogramas reales** antes de animar: 2–3 opciones, cada una con los tres formatos (A, B, C) y una muestra de subtítulos. Probar luego **una animación corta** (mapa o tarjeta) para aprobar el movimiento antes del resto.
3. **Hoja de edición con el segundo exacto de cada aparición**, sacado de las marcas por palabra del transcript del video ya cortado.

## 2. Los tres formatos

Van de más chico a más grande: **A** tapa solo el pecho, **B** tapa cara y pecho, **C** tapa todo (orden; en los archivos el reel de referencia con gráficos, anteriores a ese cambio, B era el insert completo y C el recuadro grande).


| Formato | Qué es | Dónde | Cuándo |
|---|---|---|---|
| **A · Franja del pecho** | Tarjeta sobre el pecho; la cara queda libre | **Centrada entre el mentón y el borde superior de los subtítulos** (mismo aire arriba y abajo; la persona corrigió esto midiendo con líneas). Fórmula: `top = (mentón + borde_sub)/2 − alto/2` | La base del reel: datos, listas, frases clave, contadores |
| **B · Recuadro grande** | Tarjeta grande que tapa cara y pecho; se ven costados y piernas | Arriba y al centro, más pequeña que la pantalla | Presentar a una persona (retrato + nombre) o un objeto clave |
| **C · Insert completo** | El gráfico reemplaza la imagen; la voz sigue | **Llena todo el alto** de arriba abajo (no solo la zona de la cara); la franja de subtítulos se oscurece apenas con un degradé inferior | Momentos visuales cortos y puntuales: mapas, la lista que se reordena |

- **B y C solo en tramos de 2–4 s, nunca dos seguidos.** Objetivo: la cara visible ≥ 75 % del reel. En el reel de referencia con gráficos terminó en ~20 % tapado.
- **Una cita no va en B:** va **en la zona de subtítulos**, sin tarjeta ni retrato, a 58 px la base y 66 px la complementaria, con la misma animación de entrada que los gráficos. Mientras está, el subtítulo común de esa frase no aparece. Dos opciones:
  1. **Cita fija:** la frase entra completa.
  2. **Cita con destacado acumulativo:** sigue la misma lógica del destacado acumulativo (`estilo-por-defecto.md` → 5), con los tamaños de la cita: las palabras se suman una a una sin moverse y la frase completa queda hasta el bloque siguiente; las palabras comunes en la fuente base y solo las clave en la complementaria; cada palabra destacada suena con su sfx al aparecer (si hay dos, el mismo sfx), revisando que no se cargue con otros sfx del mismo instante.
- **En todo reel con gráficos va al menos una cita con destacado acumulativo.** Puede ser una cita real (lo que dijo un autor) o una frase muy relevante del propio video.
- **Nada de recuadros/píldoras detrás de rótulos de mapa** ("típico de edición de IA"): rótulos cartográficos con tinta oscura y halo del color del papel; el año, grande y sin caja, con una línea fina debajo.
- **Ilustraciones:** íconos de línea fina de un solo color (p. ej. un velero antiguo), **nunca emojis**. Personas históricas sin retrato confiable: silueta de perfil tipo camafeo de autoría propia (`retratos_camafeo.py`) y decirle a la persona que es evocativa, no un retrato fiel. Ojo con retratos mal rotulados en internet (el de peluca rizada que circula como "John el reel de referencia con gráficos" es el reel de referencia con gráficos Mather).

## 3. Maquetación

- Tarjetas **a la medida del contenido** (sin alto fijo): mismo aire arriba y abajo, medido sobre la **tinta** (comparar captura con y sin texto), no sobre las cajas. Tolerancia ±2 px. `medir_aire.js`.
- Texto en píldoras/cajas centrado por altura de mayúsculas (baseline = centro + capHeight/2), verificado midiendo la tinta.
- El texto se ajusta midiendo su ancho real y bajando el tamaño de a 1 px (`fit`), **con el elemento visible** (si está oculto mide 0 y lo achica a nada).
- Dígitos que cambian (contadores, año que retrocede): ancho fijo por dígito para que no "bailen".
- Colores del estilo 2A (referencia; puede cambiar): tarjeta `rgba(20,16,14,.74)`, radio 26, borde `rgba(255,255,255,.16)`; texto Cal Sans blanca + Playfair Display Italic crema `#F6F6A8`; inserts en papel `#EFE4CC` / tierra `#DCCBA6` / tinta `#3A2C1F`; pin `#8B1A1A`.

## 4. Animación

- **Entradas:** fundido de opacidad 0→1 en ~10 fotogramas (0,33 s) con ease-out cúbico + subida de 12–16 px. Líneas de una tarjeta: cada una entra con su palabra (fundido + 10 px).
- **Salidas: secas** (desaparece en un fotograma, sin fundido) — pedido explícito de la persona para inserts y tarjetas. Un insert sale **justo al terminar la palabra** que lo cierra (p. ej. "ciudad"), idealmente en un corte.
- **Sincronía con el habla:** cada línea, nombre, número o ítem aparece en el instante en que se dice (marcas por palabra). Nunca todo junto ni rápido.
- **Prohibido por defecto (huele a IA):** escalas que rebotan (springs, como un resorte), palabra que salta al decirse, brillos que barren el texto y "pop" de escala exagerado. No es pop la entrada de los subtítulos (106 % → 100 % en 130 ms): es un asentamiento casi imperceptible, sin pasarse de tamaño.
- **Permitidos solo con función** (si la escena lo justifica o se pide): **texto letra por letra**, solo cuando simula algo que se escribe dentro de la escena (un chat, una búsqueda, una máquina de escribir), nunca como forma general de poner texto; **desenfoque de entrada**, solo en un momento puntual (una imagen que se aclara cuando la idea se entiende, un recuerdo que aparece), corto y una sola vez por video.
- **Movimientos que sí:** ruta que se dibuja (máscara con stroke-dashoffset, ease-in-out ~2,2 s) con un ícono que la sigue; tilde que se traza; acercamiento lento del mapa 1,00→1,04–1,05 lineal; lista que se reordena con ease-in-out ~0,5 s; año que retrocede/avanza con desaceleración.

## 5. Subtítulos en un reel con gráficos

- Estándar de siempre (`estilo-por-defecto.md` → 5), **secos por defecto** (sin animación de entrada): la animación queda para los gráficos, si no "queda todo muy cargado". En este formato no se pregunta por la animación de los subtítulos; si se pide, se hace.
- **Se ocultan cuando el gráfico muestra el mismo texto** (listas, placas, preguntas citadas, cita en zona de subtítulos). Se generan completos y después se borran los eventos que empiezan en esos rangos; el `.srt` queda completo.
- Ningún gráfico A baja del borde superior de los subtítulos; los subtítulos nunca se mueven.
- Palabras destacadas solo donde el gráfico no repite la palabra.

## 6. Cortes

- **Corte ajustado**: se quitan los silencios ≥ 0,2 s, dejando ~0,05 s de cola tras la palabra y ~0,04 s antes de la siguiente (envolvente de energía: voz > −35 dB, colas hasta −44 dB).
- **Los conectores se quedan** ("entonces", "en cambio", "mucho"…): no son muletillas. Solo se quita uno si la persona lo pide (en el reel de referencia con gráficos: "de hecho"); al quitar una palabra, cortar en el silencio previo y posterior medidos en la envolvente y desplazar todos los tiempos posteriores.
- Un reel con gráficos puede pasar de 1:10 (el reel de referencia con gráficos: 86,8 s) si el contenido lo pide; avisar la duración en la hoja.
- Cola final: congelar 0,6 s el último fotograma.

## 7. Zooms

- **Golpe de zoom = zoom-in rápido animado**, no salto en el corte: 100→130 % en 6 fotogramas (0,2 s) con ease-out cúbico, al inicio del tramo. Vuelve a 100 % en el corte siguiente (mejor si lo tapa un gráfico).
- **Acercamiento lento** en el clímax: 100→140 % lineal en ~3,4 s. **Anclado en la cara** (la cara queda en su lugar y crece). Después, **salida rápida** 140→100 % en 7 fotogramas al empezar la frase siguiente, con whoosh. Un regreso seco a 100 % se ve "raro".
- Ancla: centro de la cara medido en ese tramo (mediana YuNet). Fórmula zoompan sobre el cuadro superescalado ×2: `x = Fx·(1−1/z)`, `y = Fy·(1−1/z)`.
- **Técnico:** no usar `scale=eval=frame` + `crop` para zooms animados: `crop` no sigue el tamaño cambiante y la cara se corre al costado (fue el error de la v1). Usar `scale=2160:3840,zoompan=z='…':x='…':y='…':d=1:s=1080x1920:fps=30` con `on` (fotograma de salida) como tiempo local. Ver `base_corte_zoom.py`.

## 8. Sonido

- **Banco de SFX puntuado por la persona:** antes de elegir cualquier efecto, lee `4_Recursos/BANCO_SFX.md` en la carpeta de trabajo (copia en `references/banco-sfx.md`; si difieren, manda el de la carpeta). Ahí está el puntaje de cada sonido por categoría y sus notas. Usa primero los de 5★, alterna con los de 4★ y no uses los de 1–2★ salvo pedido de la persona. Los nuevos se suman a los de siempre, no los reemplazan. En este formato, `sfx/swish` quedó con 2★: para cambios de encuadre usa `sfx/swoosh`, `sfx_pixabay/whoosh-short` o los whooshes 5★ de `sfx/`.

- **Base moderna con textura de época** cuando el tema lo pide: efectos cortos (< 0,4 s) y secos; la época como textura (papel, tic-tac, golpe con algo de sello). Crujidos o tic-tac solo como acentos breves.
- **Familias:** aparece algo = tap / clic / pop (`sfx/tap_texture`, `click_decision`, `sfx/pop`); cambio de encuadre o movimiento = whoosh/swoosh 0,13 s antes (`sfx/swoosh`, `sfx/swish`); reloj que corre = `sfx/tic` repetido con la misma desaceleración que los dígitos; papel = `sfx/paper`.
- **La persona rechazó** el rasgueo de pluma sintetizado ("wish"): en ítems de lista va tap/pop/clic.
- **Cantidad:** en reels con gráficos la persona pidió más que el estándar de 8/min: el reel de referencia con gráficos cerró con **46 efectos en 87 s (~32/min)**, cada uno atado a un evento (aparición de línea/ítem/nombre, pin, golpe y salida de zoom, reordenamiento, palabra clave final). Ninguno de relleno; ninguno en el acercamiento lento.
- **Volumen:** el estándar de SFX de todos los tipos de reel (`estilo-por-defecto.md` → 7): niveles base por importancia, cada efecto a pico = nivel base **+12 dB** (3 dB más que en la primera referencia, donde se sintió "casi sin resaltar"), limitador propio en la pista de efectos (`alimiter limit=0.89`, ataque 1 ms, release 60 ms) **antes** de sumarla a la voz, y después `masterizar_audio.py` a −14 LUFS / −1 dBTP. Ver `sfx_pista.py` (`GAIN = 12`).
- Pedirle siempre a la persona que escuche: whooshes de zoom, tics y que la voz no quede aplastada.

## 9. Flujo técnico que funcionó (máquina de la persona: 4 núcleos, llamadas ≤ 180 s)

1. **Transcripción:** Whisper turbo va a ~13× tiempo real: armar `tramos.json` con tramos de ~10–12 s cortados en silencios (uno por llamada). Revisar huecos: si entre dos palabras hay > 1 s con voz, re-transcribir ese tramo suelto (en el reel de referencia con gráficos faltaba "de nosotros mismos").
2. **Corte + zooms** (`base_corte_zoom.py`): en dos llamadas (segmentos 0–12 y 13–fin), x264 veryfast crf 15, audio PCM; unir con concat demuxer.
3. **Gráficos:** HTML con una función `render(g, t)` determinista, renderizado en la nube con Playwright fotograma a fotograma (`omitBackground`) a PNG con alfa → **VP9 con alfa (.webm, `yuva420p`)**: pesan KB y viajan rápido. En la Mac se superponen con `-c:v libvpx-vp9 -i capa.webm` (decodificador libvpx para conservar el alfa), `setpts=PTS-STARTPTS+t0/TB` y `overlay … enable='between(t,t0,t1)'`. Para el kit de CapCut se convierten a ProRes 4444 ahí mismo.
4. **Subtítulos:** `subtitulos.py --sin-animacion` sobre las palabras del video cortado; luego borrar los eventos de los rangos ocultos.
5. **SFX:** `sfx_pista.py` arma la pista con numpy; se suma a la voz en float (`mezcla.wav`).
6. **Composición** (`componer.py`): x264 **superfast** 16 Mbps para entrar en 180 s; luego `masterizar_audio.py`. Si solo cambia el audio, **no re-renderizar**: copiar el video de la composición anterior y cambiar la pista.
7. **Revisión:** hoja de contactos con fotogramas en los segundos clave (aparición, salida seca, zooms) antes de mandar nada, y vista previa liviana 540×960 por el chat; la calidad completa queda en `3_Videos editados/<n>/revision_vN.mp4` (se borra la anterior).
8. **Caché de archivos:** al reenviar a la Mac un archivo con el mismo nombre, `device_commit_files` puede escribir una copia vieja. **Siempre nombre nuevo (`_v2`, `_v3`…) y `md5sum` en los dos lados.**

## 9-bis. Portada

Un fotograma con la cara y un elemento gráfico del video (un mapa, un retrato, una tarjeta) más una frase gancho corta, con el mismo estilo gráfico del reel. 1080 × 1920, lo esencial dentro del centro 1080 × 1350; una principal y una alternativa (`portadas.md`).

## 10. Checklist específico

- [ ] Encuadre medido y zonas recalculadas para este bruto.
- [ ] Ningún gráfico A sobre la cara; A centrado entre mentón y subtítulos (aire igual, medido).
- [ ] B/C ≤ 4 s cada uno, nunca seguidos, cara visible ≥ 75 %.
- [ ] Cada aparición en su palabra; salidas secas; sin animaciones prohibidas; sin emojis; sin cajas detrás de rótulos de mapa.
- [ ] Subtítulos secos y ocultos donde el gráfico repite el texto.
- [ ] Golpes de zoom animados y anclados en la cara; acercamiento lento sin desplazamiento lateral; salida rápida con whoosh.
- [ ] SFX: cada uno atado a un evento, nivel de la sección 8, pista limitada antes de la mezcla.
- [ ] Al menos una cita con destacado acumulativo.
- [ ] Portada principal y alternativa.
- [ ] Capas reenviadas con nombre nuevo y md5 verificado.
