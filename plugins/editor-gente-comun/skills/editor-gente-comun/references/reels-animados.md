# Reels animados narrados (sin cámara)

Un reel **100 % animado**: la voz de la persona grabada aparte y gráficos a pantalla completa sincronizados palabra por palabra, sin plano de cámara. Estas reglas salen de dos reels de referencia trabajados en muchas rondas de corrección (uno da el estilo por defecto y el otro, la ubicación y el tamaño de subtítulos, tarjetas y textos). Valen para todos los reels de este tipo; si un video pide otra cosa, gana el pedido y se anota en `ESTADO.md`.

Manda sobre `reels-con-graficos.md` y sobre `estilo-por-defecto.md` en composición, tiempos, animación, sonido y subtítulos. De `estilo-por-defecto.md` siguen valiendo la transcripción literal, el máximo de dos tipografías por secuencia y la exportación. Plantillas de código en `templates/reel-animado/`.

Casi todas las correcciones en los reels de referencia fueron de **tiempo** y de **sonido**. Aplica estas reglas desde la primera versión.

## 1. Flujo

### 1.1 Antes de nada: el estilo de animación

**Si todavía no tiene un estilo propio guardado** (`5_Mi estilo/`), pregunta con dos caminos:

«¿Quieres que creemos tu propio estilo de animación a partir de referencias (una cuenta de Instagram que te guste), o elegimos uno de los estilos que ya traigo cargados? Te muestro las opciones.»

**(a) Estilo propio por referencia.** Explícale los pasos:
1. Entra a Instagram.
2. Elige una cuenta de videos animados que te guste.
3. Descarga unos 6 videos de esa cuenta con un descargador gratuito en línea (indícale uno que funcione hoy, verificándolo con una búsqueda; si deja de funcionar, que busque "descargar reels de Instagram").
4. Guárdalos en `2_Referencias/<nombre de la cuenta>/`.
5. Avísame en el chat para que los revise.

Al revisarlos (hojas de contactos, fotogramas, medición de cortes y sonidos, `base/analizador/`):
- **Imita su lenguaje lo más fielmente posible:** ritmo, transiciones, tipo de figuras, tipografía, uso del color, movimiento y sonido.
- **No copies** logos, marcas de agua, personajes reconocibles ni frases de la cuenta. Los videos se usan solo como referencia, nunca se republican.
- **Da tu veredicto:** si crees que la cuenta usa un programa de efectos visuales (After Effects, Cinema 4D, Blender u otro) y **qué porcentaje de parecido puedes alcanzar** con tus herramientas (HTML + Three.js + FFmpeg), explicando qué partes saldrán iguales y cuáles no.
- Guarda el resultado como ficha de estilo en `5_Mi estilo/` y ofrécele sumarla a su perfil.

Si no quiere hacer los pasos ahora, puede dejarlos para después y elegir un estilo precargado.

**(b) Estilos precargados.** Mándale la hoja `references/estilos-animados/hoja_estilos.jpg` y preséntalos en una línea cada uno (tabla de `estilos-animados/README.md`), con tu recomendación según el tema del guion:
- **Estilo de fábrica:** pictogramas, mapas de líneas, imágenes reales, contadores, frases-tesis palabra a palabra y la línea quebrada como motivo, con objetos en 3D, fuente bíblica arriba y términos en griego o hebreo (estos dos, solo con contenido cristiano). Ubicación y tamaño de subtítulos, tarjetas y textos según §4.1. Si lo elige, pregunta el color con dos opciones y muéstralas sobre una escena: «¿Con qué colores lo armamos? Te muestro las dos paletas sobre una escena: gris y crema, o azul noche y oro.»
- **Escala sin fin · Caricatura de los 50 · RPG de 16 bits · Diorama de pixeles · Isla isométrica:** si elige uno, lee **solo** su archivo en `references/estilos-animados/` y síguelo junto con este manual (el estilo cambia el aspecto; tiempos, aire, subtítulo continuo, zona segura, storyboard y auditorías siguen siendo los de aquí).

**Si ya tiene un estilo propio guardado:** úsalo, pero recuérdale en una línea que puede elegir otro: «Lo armo en tu estilo de siempre; si quieres probar otro, tengo seis precargados (el de fábrica, escala sin fin, caricatura de los 50, RPG de 16 bits, diorama de pixeles e isla isométrica): te mando la hoja». Si dice que no, se sigue sin insistir.

### 1.2 Audio y recursos, siempre antes de animar

No empieces a animar hasta tener la voz, las imágenes (o la decisión de que las busques tú) y la respuesta sobre la música. **Recuérdaselo siempre, aunque no lo pregunte**, y explica paso a paso cómo enviarlas:

«Antes de animar necesito tres cosas: (1) la voz narradora, (2) las imágenes que quieras usar y (3) saber si quieres música. Te explico cómo grabar la voz con tu celular y cómo guardar las imágenes. Cuando las tengas en la carpeta, avísame y arranco.»

- **Voz narradora: recomienda siempre la voz humana, la propia.** Con el guion terminado, se graba con la app de notas de voz del celular, en un lugar silencioso, a un palmo de la boca, sin música. Se lee el guion completo de corrido y, si hay un error, se repite la frase entera (tú detectas y quitas la toma fallida). El archivo (m4a, mp3 o wav) va en `1_Videos sin editar/<nombre>/` o adjunto en el chat.
- **Voz sintética, solo si la pide** (no puede o no quiere grabar): ofrécela como recurso, no como recomendación. Dos caminos: que la genere en la app que ya use (por ejemplo CapCut) y la exporte como audio, o que la hagas tú con `scripts/voz_sintetica.py` (en el espacio en la nube; solo se sube el texto del guion). Primero mándale `voz_sintetica.py muestras` (tres voces leyendo la misma frase) para que elija. Con voz sintética se aplica el tramo de "voz con IA" de §1.3 (se respeta su cadencia).
- **Imágenes:** en una carpeta con el nombre del video dentro de `4_Recursos/imagenes/` (o adjuntas en el chat), con nombres que digan qué son y en qué momento van (`01_retrato.jpg`, `02_taller.jpg`); de al menos 1080 px de ancho y sin marca de agua. Si no tiene, propón cuáles buscar y búscalas en sitios de dominio público o licencia libre (Wikimedia Commons, museos con CC0).
- **Música (un recurso, no el valor por defecto):** por defecto va la cama grave bajo la voz (§6). Si el estilo elegido pide música (el RPG, la isla, la escala sin fin, la caricatura), pregúntale si la quiere: la cama hecha con código para ese estilo (`scripts/musica_estilo.py`), música real con licencia abierta (`buscar_sfx.py "…" --musica`), su propia música, o nada. Siempre bien por debajo de la voz.

### 1.3 Pasos

1. **Inventario de recursos:** hoja de contactos de las imágenes; resolución de cada una, qué falta, qué tiene marca de agua y qué no tiene fuente clara. Avisa enseguida.
2. **Transcribe** la voz con `transcribir.py` (§8 para los tramos).
3. **Voz propia: toma fallida.** Compara el texto de Whisper con el guion: Whisper "limpia" las repeticiones y esconde el error. Ubica las dos lecturas con la envolvente de energía y conserva la retoma completa. Después, **corte ajustado + aire** (§3).
   **Voz con IA: se respeta su cadencia.** Solo se acortan los silencios que pasan el tope (`preset/pausas_ia.py`): fin de oración 0,50 s · coma 0,45 s · quiebres hasta 0,60 s; se dejan intactas las pausas pedidas en el guion. Inicio 0,10 s, final 1,6 s. Informa la tabla de lo acortado.
4. **Aire en cada cambio de escena** (con cualquier voz): +0,25–0,35 s en el punto más silencioso antes de la primera palabra de cada escena; tras el remate de la aplicación, +0,55 s (`preset/aire_escenas.py`). Todo se re-temporiza desde la lista de palabras nueva.
5. **Voz:** pasa altos 80 Hz + compresión suave (umbral −22 dB, 2,5:1, ataque 10 ms, release 120 ms); el master va al final.
6. **Guion visual:** por cada frase, qué escena, qué figura, qué cambia en la palabra que lo nombra, dónde entra la fuente bíblica, qué 2–3 momentos llevan imagen real, qué objetos van en 3D y dónde hay corte seco (justificado).
7. **Punto de control antes de hacer el video: storyboard de 6 cuadros y clip de 7 s.**
   - **Storyboard:** los 6 cuadros más representativos (gancho, tesis, un mapa o imagen real, un objeto 3D, la revelación y el cierre), 1080×1920, hechos con el kit real (no bocetos), en una lámina con tiempo, frase y nota por cuadro.
   - **Clip de ≈ 7 s del gancho** con gráficos animados, subtítulos, SFX, cama sonora, voz tratada y master a −14 LUFS. Cortarlo en una pausa natural de la voz. Antes, corrige las marcas de esos segundos (§9.1).
   - **No se edita el resto hasta que apruebe los dos.**
8. **Gráficos** (§4, §5, §8): generador Python → HTML con `render(t)`; stills de control antes del render completo. En una serie de escenas parecidas, se aprueba la primera.
9. **Subtítulos** (§7) · **Sonido** (§6) · **Composición y master** (`masterizar_audio.py`).
10. **Control de calidad** (§9) → envío por el chat → `3_Videos editados/<nombre>/reel_<nombre>_vN.mp4` → borra la versión anterior → actualiza `ESTADO.md`.
11. **Portada** (`portadas.md`), principal y alternativa, con la entrega final.

## 2. Regla madre

Cada elemento entra **en el instante real** en que se dice la palabra que lo nombra, y la escena se entiende sin leer el subtítulo. Todos los tiempos de gráficos, sonidos y subtítulos salen de la misma lista de palabras (`T(i)` = inicio, `TE(i)` = fin de la palabra i). Si se corrige una marca, se mueve todo junto.

**Cada frase cambia algo en pantalla** (un cambio visual relevante cada 2–4 s), **cada sustantivo concreto del guion tiene su dibujo** y **la escena nunca queda quieta ni vacía**.

## 3. Tiempos y aire (voz propia)

**Corte ajustado:** quita los silencios ≥ 0,2 s, deja 0,05 s de cola y 0,04 s de entrada, micro fundido de 8 ms en cada empalme.

**Aire agregado:** silencio en el punto de menor energía entre dos palabras (nunca a mitad de sílaba).

| Momento | Aire |
|---|---|
| Entre oraciones | 0,45 s mínimo |
| Dentro de una misma oración | casi nada (≈ 0,1 s) |
| Tras la tesis del gancho | 0,5 s |
| Tras un remate | ≈ 0,4 s |
| Tras un dato con epígrafe para leer | ≈ 0,5 s |
| Tras un quiebre o una reprise | ≈ 0,7 s |
| Tras una frase palabra a palabra | 0,25–0,6 s |
| En cada cambio de escena | +0,25–0,35 s; tras el remate de la aplicación, +0,55 s |
| Final del video | 1,6 s |

- **Nunca una espera larga antes de un cambio de escena.** Si algo necesita tiempo para leerse, **adelanta su entrada** a una palabra anterior; no agregues silencio después. El aire de cambio de escena no va donde la frase sigue de corrido hacia el cierre.
- **Cambiar el aire de una versión armada:** corta o inserta en la voz final dentro de un tramo en silencio (verifica que lo quitado esté a −180 dB) y desplaza las marcas posteriores la misma cantidad.

**Marcas de Whisper:** se corren 0,1–0,5 s, sobre todo en palabras tras una pausa (marca tarde), en frases rápidas al final de una oración (llega a superponer palabras) y en números leídos. Antes de cada render, corrígelas con la auditoría de §9.1.

## 4. Diseño y composición (estilo por defecto)

### 4.1 Zona segura y franjas

**Zona segura unificada Instagram + TikTok** (`zona-segura.md`), obligatoria: arriba 250 px · abajo 380 px (nada importante debajo de y = 1540) · izquierda 120 px · derecha 130 px hasta y = 720 y **240 px desde y = 720** (columna de botones: x ≤ 840). Por debajo de y = 720, un bloque centrado mide como máximo 600 px; si necesita más, se corre a la izquierda (x 120–840).

| Franja | y (px) | Qué va |
|---|---|---|
| Fuente bíblica | 262–330 | Solo "■ FUENTE · LIBRO c:v" cuando corresponde; el resto del tiempo, vacía |
| Contenido principal | ≈ 360–1180 | Escena centrada. Lo que gira o se une va en el **centro real**: x = 540, y ≈ 860–960 |
| Tarjetas, rótulos y epígrafes | ≈ 1180–1310 | Tarjetas de personajes, nombres de lugares, epígrafes de fotos. **Se usa siempre**: la parte inferior no puede quedar sin uso |
| Subtítulo | **y = 1350** (primer renglón) | Con dos renglones llega a ≈ 1415 |
| Bajo el subtítulo | ≈ 1440–1530 | Solo rótulos cortos de una línea, si la franja de arriba está ocupada |

- **Fondos, texturas y degradés ocupan todo el cuadro**, de borde a borde.
- **Zona segura auditada en cada render** (`preset/auditoria_zona.py`): mide la tinta real de cada texto y las cajas de fotos y tarjetas cada 0,25 s. Lo que más falla: textos grandes o fotos que bajan de y = 720 y llegan a la columna de botones, rótulos de mapa que se salen por los costados. Solución: subir o achicar el bloque, correrlo a la izquierda o mostrar el rótulo solo cuando la cámara se detiene.
- **También para los objetos 3D** (`preset/auditoria_3d.py`): se corrige alejando la cámara o achicando el objeto, nunca recortando.
- **Los textos no tiemblan:** nunca escales tarjetas, rótulos ni textos con un empuje de cámara de la escena. En los mapas, la deriva va en el zoom del mapa y los rótulos se reposicionan con `translate`.

### 4.2 Paleta (la persona elige entre las dos)

| Rol | Gris y crema | Noche y oro |
|---|---|---|
| Fondo | gris oscuro `#1B1F24` | azul noche `#0E1626` |
| Acento | crema `#F6F6A8` | oro `#E3A93A` |
| Texto y figuras | blanco `#F2F2EE` | marfil `#F3F0E8` |
| Rótulos | gris `#8E949C` | gris azulado `#8A93A3` |
| Tierra en los mapas | gris apenas más claro que el fondo | azul apenas más claro que el fondo |

- **Fondo:** color liso con una viñeta suave, de borde a borde.
- **Un solo acento de color por video.** Un acento por plano: dos acentos se anulan.
- Si la persona pide otro color, arma el tema con la misma estructura (fondo oscuro neutro del tono, acento, texto, rótulos) y muéstrale un cuadro antes de seguir. Valores en `templates/reel-animado/base/kit_base.py` (`TEMAS`).

### 4.3 Tipografía

| Uso | Fuente |
|---|---|
| Titulares y frases grandes | Cal Sans, con la palabra clave en Instrument Serif cursiva del acento |
| Números, años y cifras | Cal Sans grande |
| Citas | Instrument Serif cursiva |
| Rótulos, fechas, lugares | JetBrains Mono en mayúsculas espaciadas (mínimo 24 px; 28 px si es el único texto que se lee) |
| Rótulos fuertes (países, nombres) | Inter 800 en mayúsculas (mínimo 30 px) |
| Griego / hebreo | GFS Didot / Frank Ruhl Libre |

- **Sin cabecera fija.** La única es la **fuente bíblica** (solo con contenido cristiano): "■ FUENTE · ÉXODO 31:1–5" (mono, cuadradito del acento), arriba a la izquierda (y ≈ 262). Aparece y desaparece solo mientras se habla de ese pasaje, y solo si hay una cita bíblica exacta que respalde lo que se dice. Cita verificada con búsqueda web en la versión del perfil.
- **Términos clave en el idioma original** (solo con contenido cristiano): cuando un concepto clave tiene un término griego o hebreo que lo ilumina, va como escena propia: la palabra grande en el acento (griego en GFS Didot, hebreo con niqud en Frank Ruhl Libre, de derecha a izquierda), debajo la transliteración en mono y la traducción entre «» (κλῆσις · KLĒSIS «LLAMADO»). El subtítulo se oculta mientras está. Uno o dos por video, como mucho. **Verificación a tu cargo:** confirma en léxicos en línea (Blue Letter Bible o STEP Bible con número Strong; texto griego NA28/SBLGNT o hebreo BHS/WLC) la forma exacta, la transliteración, el significado y que el término aparezca de verdad en el pasaje citado. Si se muestra una forma distinta de la del versículo, dilo en el rótulo ("raíz", "de la misma familia").

### 4.4 Familias de escena

1. **Pictogramas:** figura sólida de un solo color (texto y figuras de la paleta), cabeza redonda separada del cuerpo, en la posición que pide la frase (ora, trabaja, sostiene, enseña, camina…). `figuras.py`. Dos figuras que contrastan: las dos de pie o las dos arrodilladas, nunca mezcladas. La comparación de dos figuras una frente a la otra, como mucho una vez por video.
2. **Objetos:** 2D de trazo fino del acento, o 3D real (§4.7).
3. **Mapas y líneas de tiempo** (§4.6).
4. **Imágenes reales** (§4.5).
5. **Tipografía protagonista:** años gigantes, cifras, frases-tesis palabra a palabra.

- **Línea quebrada** irregular en el acento como motivo de lo que se divide, con el sonido `snap`. Vuelve en el gancho, la reprise y el cierre. Para tachar un rótulo, una línea horizontal casi recta.
- **Lo simple gana en la tesis:** dos figuras y la línea quebrada entre ellas.
- **«Iglesia»: una iglesia en 3D**, no un púlpito dibujado. **«Éxito» o «grandeza»:** trofeo, medalla o cucarda.
- No repitas un ícono si otro ya lo representa todo.
- **Dibujos prolijos:** torres, techos y simetrías revisados a tamaño completo; si un objeto 2D queda desprolijo, pásalo a 3D.

### 4.5 Imágenes reales

**2 o 3 momentos con imágenes reales por video** cuando tengan sentido (grabados, pinturas, documentos, lugares, personajes históricos), **repartidas** a lo largo del video. Prefiere dominio público o licencia libre (Wikimedia Commons, museos con CC0; si la red de la nube devuelve error 429, descárgalas desde la computadora de la persona), anota la fuente en `ESTADO.md` y avisa si alguna tiene baja resolución o marca de agua. Nunca fotos de personas famosas actuales ni imágenes con derechos de autor claros. Formato: tarjeta opaca con bordes redondeados (foto + nombre + dato en mono), o ancho completo con epígrafe corto, centrado y pegado a la foto, dentro de la zona segura. Si una foto no se ve bien, sácala y pon la frase en grande.

### 4.6 Mapas

- **Mapas de líneas** (no de puntos): contornos de países y costas (Natural Earth 1:50m, `mapas_base.py`) en trazo fino del gris de rótulos, tierra apenas más clara que el fondo; la región destacada con borde del acento y relleno apenas más claro; ruta del acento que se dibuja; pin de destino; nombre de la región en Inter 800 y su aclaración en mono.
- **Con cámara:** abre en el continente, acerca a la región y **vuelve a alejarse** cuando el guion nombra un país actual, para que se entienda dónde estamos. Acercar/alejar 1,4–1,6 s; deriva lenta 1,00 → 1,04 mientras se mantiene.
- Rótulos, pines y rutas se dibujan **por encima** y se reposicionan en cada cuadro (no se agrandan con el zoom). La ruta no pasa sobre un rótulo. Los rótulos que solo tienen sentido acercados se ocultan al alejar.
- El año, grande y sin caja, arriba a la derecha.

### 4.7 Objetos en 3D (Three.js)

**Usa 3D siempre que se pueda** para objetos que se arman con formas simples (Biblia o libro, tabla, columna, ladrillos, vasija, montaña, lámpara, iglesia, plataforma, altar). Plantillas: `templates/reel-animado/base/biblia3d.py` y `preset/obj3d.py` (iglesia, plataforma, altar; `TEMA=gris|noche`).

- Three.js 0.170 servido por `python3 -m http.server`, WebGL por CPU, `render(t)` determinista. ≈ 0,4 s por cuadro: usa 3D solo en las escenas que lo piden.
- **Funciona bien:** libros (tapas, hojas curvas apiladas, texto en dos columnas, hoja que se da vuelta), ladrillos, columnas, vasos simples, montañas en capas, iglesia, plataforma con escaleras, altar de piedras distintas. **Evitar:** personas realistas, telas, física.
- Fondo de la escena opaco con el color del tema (nunca transparente); exposición ≈ 0,85; halo suave detrás del objeto, no encima; sombra de contacto falsa (degradé).
- Textos en texturas: revisa que no queden espejados.

## 5. Animación

| Elemento | Movimiento |
|---|---|
| Titulares, figuras y objetos grandes | Fundido + subida de 18–22 px en 0,45 s, ease-out |
| Elementos chicos (rótulos, íconos, pines) | Fundido de 0,33 s + subida de 8–18 px |
| Fotos | Fundido de 0,9 s sin movimiento, con el sonido de papel |
| Trazos (rutas, líneas, círculos) | 0,35–0,9 s con aceleración y frenada suaves |
| Fondos y mapas | La escena nunca queda quieta: deriva leve de cámara en mapas y objetos 3D |
| Contadores y años | Dígitos de ancho fijo, desaceleración al final |
| Frases-tesis | Palabra a palabra; la última en Instrument Serif cursiva del acento, más grande; subtítulo oculto mientras dura |
| Prohibido por defecto | Rebotes y escalas que saltan. Texto letra por letra solo con función (algo que se escribe dentro de la escena) |

- **Cambios de escena:** corte seco o fundido corto; whoosh solo si hay movimiento. Una figura o una forma puede pasar de una escena a la siguiente cuando ayuda a la idea. El corte seco subraya los cambios de tema, época o personaje.
- **La escena nueva entra con su primer elemento ya visible** en la palabra que la abre. Nunca cuadros vacíos.
- **Nada aparece en el lugar de otra cosa:** si una pregunta queda en pantalla, la respuesta va debajo.
- **Una animación larga que se construye por partes** vale más que cambiar de dibujo varias veces.
- Un trazo que acompaña una frase empieza con su primera palabra y termina con la última. Un quiebre va inmediatamente después de la palabra que lo motiva.
- Lo que aparece a la vez aparece realmente a la vez, centrado y con un solo sonido.
- **Cierre:** siempre en un cuadro liso negro, sin logo. La última escena se funde a negro dentro del aire final de 1,6 s; el cuadro liso queda al menos 0,5 s, con la cama sonora apagándose hasta el último cuadro. El subtítulo sale antes del fundido.
- **Duración:** la marca el guion, en general un minuto o algo más.

## 6. Sonido

Antes de elegir cualquier efecto, lee `4_Recursos/BANCO_SFX.md` (copia en `references/banco-sfx.md`). Usa primero los de 5★, alterna con los de 4★.

**Cantidad alta (≈ 60 efectos por minuto, cada uno atado a algo que aparece), variedad baja.** Una versión con 34 sonidos distintos sonó "rara": más variedad = otro archivo de la misma familia, nunca otra familia.

| Familia | Cuándo |
|---|---|
| Clic de dibujo (tap con textura) | Aparece un dibujo, figura, ícono, tarjeta o imagen |
| Clic de texto (mouse) | Aparece una leyenda, rótulo, fecha, título o la fuente bíblica |
| Énfasis (clic de decisión) | Dato clave o palabra clave |
| Pop | Pines y años |
| Whoosh de escena | 0,13 s antes de un cambio de escena con movimiento |
| Whoosh de movimiento | Rutas, zooms, elementos que se mueven o se unen |
| Golpe suave | Remates |
| Papel | Entra una foto o un documento; hoja de la Biblia 3D que se da vuelta |
| Snap | La línea quebrada |
| Error | Una respuesta incorrecta o un conflicto |
| Deslizamiento metálico | Puertas que se cierran |
| Tic | Solo cuando se encienden las horas de un reloj |
| Contador | 25–30 clics continuos en ~1,3 s que se van espaciando (de ≈ 0,03 a ≈ 0,19 s), con variación leve de volumen |
| Momento de revelación | Pad luminoso que crece + golpe suave |

- Dos clics distintos (dibujo y texto) para no repetir el mismo cuatro veces seguidas.
- **Sin brillos chillones** (sparkle, chime, ping) ni cambios de tono.
- En frases palabra a palabra suena **solo la palabra clave**.
- Un cambio de escena sin movimiento no lleva whoosh.
- **Volumen:** el estándar común (`estilo-por-defecto.md` → 7): nivel base por importancia + 12 dB, limitador en la pista de efectos, master −14 LUFS / ≤ −1 dBTP.

**Pads sintetizados** (`pad()` en `sfx_base.py` y `preset/audio_full.py`): acorde grave solemne 65 · 98 · 131 (· 196) Hz para momentos espirituales o solemnes; acorde luminoso 147 · 220 · 294 · 440 Hz para la revelación. **Tienen que escucharse claramente:** a la par de la voz (≈ 0 a −2 dB, en volumen percibido) y con **octavas altas (262 · 392 · 523 Hz)** con brillo suave, porque el parlante del celular casi no reproduce por debajo de 150 Hz: un pad solo grave se mide fuerte pero no se oye.

**Cama sonora:** un pad de fondo de principio a fin, ≈ 12 dB por debajo de la voz, también con octavas altas. Si se pide otra cosa, silencio entre frases y cama solo en el cierre.

Pide siempre que escuche la cama, los pads, que los clics de énfasis no tapen palabras y que el contador se oiga: se miden, no se escuchan.

## 7. Subtítulos

- **Por bloques** (como en los otros formatos): cada bloque entra completo, en Cal Sans blanca, con sombra suave difusa, sin contorno ni fondo. Bloques de una frase corta (≈ 4–7 palabras, hasta 2 renglones); el bloque siguiente reemplaza al anterior. El bloque no se mueve.
- **Posición: primer renglón en y = 1350**; el segundo, debajo, con 6 px de tinta entre renglones.
- **Tamaño, el de siempre:** en HTML, Cal Sans **41,5 px**, interletrado −0,9 px, interlineado 44 px, y la complementaria (Playfair Display Italic semibold) con la altura compensada (≈ ×1,14). Equivale a los 11 pt de los otros formatos; `font-size: 50px` en CSS sale un 24 % más grande.
- **Énfasis** (uno por frase, como mucho dos): la palabra que nombra algo que se ve en pantalla, en el color del acento con la misma fuente; el remate emocional o lo que el gráfico no muestra, en la complementaria cursiva del acento.
- **Ocultos donde el gráfico ya muestra el texto** (preguntas, titulares, citas, frases palabra a palabra, términos en griego o hebreo). El titular y el subtítulo nunca repiten la misma frase.
- Franja oscura difusa detrás solo si la escena lo necesita.
- Transcripción literal, sin punto final, un renglón siempre que entre, nunca una preposición separada de su complemento.
- Se queman sobre el video final; el `.srt` va por el chat.

## 8. Técnica

- **Motor** (`templates/reel-animado/`): `graficos_base.py` lee `palabras_vN.json` y escribe el HTML. Escenas `div.sc` con `data-a`/`data-b`; elementos con `data-in` (+ `data-out`, `data-dy`, `data-dur`); trazos `data-draw="t0,t1"`; contadores `data-count`. Todo tiempo como `T(i)`/`TE(i)`. Pictogramas en `figuras.py`.
- **Kit del estilo por defecto** (`templates/reel-animado/base/`): `kit_base.py` (las dos paletas, fuentes, subtítulo por bloques, rótulos, fuente bíblica, término original), `biblia3d.py` (3D; `preset/obj3d.py` para iglesia, plataforma y altar), `lamina.py` (storyboard de 6 cuadros).
- **Mapas** (`mapas_base.py`): Natural Earth 1:50m desde GitHub, proyectado a píxeles; cámara por fotogramas clave (centro + zoom con interpolación logarítmica).
- **Render** (`render.py`, `preset/render_reel.py`): Playwright + Chrome, `render(t)` y captura JPEG q95 por cuadro en un pipe a ffmpeg (x264 CRF 12–14, BT.709). Dos procesos en paralelo por mitades. Si cambia solo una escena, re-renderiza solo esa mitad. En la computadora de la persona, corre ffmpeg en primer plano.
- **Sonido** (`sfx_base.py`, `preset/audio_full.py`, `preset/audio_preview.py`). Guarda la salida en un log (con `| head` el script se corta antes de escribir el WAV).
- **Composición:** concat de las mitades (`-c copy`) → subtítulos quemados → H.264 20 Mbps → `masterizar_audio.py`.
- **Whisper:** cada llamada dura ≤ 180 s; arma `tramos.json` en tramos de 10–13 s cortados en silencios. Para corregir tiempos sueltos, la envolvente de energía alcanza.

## 9. Control de calidad (antes de cada entrega)

1. **Marcas contra la voz** (`auditoria.py marcas`, `preset/marcas.py`): toda palabra que dispara algo, revisada contra los tramos de voz medidos (ventanas de 10 ms, umbral −34 dB).
2. **Sonido contra imagen** (`auditoria.py sonido`): ningún efecto sin un cambio en pantalla.
3. **Cuadros de transición:** un cuadro cada 0,2 s en cada cambio de escena; sin cuadros vacíos ni elementos superpuestos.
4. **Zona segura y franjas:** textos, fotos y objetos 3D auditados; subtítulo en y = 1350 sin taparse con tarjetas; la fuente bíblica solo mientras se habla del pasaje.
5. **Archivo final:** `ffprobe` (1080×1920, 30 fps, H.264, AAC 48 kHz), −14 LUFS ± 0,3, pico ≤ −1 dBTP.
6. **Lo que tiene que escuchar:** la cama, los pads, que los clics de énfasis no tapen palabras y que el contador se oiga.
7. **Portada** principal y alternativa (`portadas.md`).
