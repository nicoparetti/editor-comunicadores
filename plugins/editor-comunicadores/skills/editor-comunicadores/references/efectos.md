# Catálogo de efectos (86)

Los efectos especiales se suman a los criterios del formato, nunca los reemplazan. **Como máximo 3 por pieza**, propuestos en la hoja de edición (o en el hub) marcados "a decidir"; la persona elige. Ninguno se aplica por tu cuenta.

## Cómo pedir un efecto (4 partes)

1. **Qué:** el efecto ("una lupa", "una cita").
2. **Dónde:** la palabra o el segundo ("cuando digo *propósito*", "en 0:42").
3. **Cómo:** la variante si la hay ("de barras", "con fondo oscuro").
4. **Cuánto:** la intensidad o duración ("suave", "2 segundos").

Si falta alguna parte, elígela con los criterios de este editor y dila en la hoja.

## Origen y motor

Las recetas de `references/efectos/<efecto>.md` vienen de los packs gratuitos de Converzzo (licencia MIT; aviso en `templates/converzzo/*/LICENSE` y `NOTICE.md`). Funcionan con su motor, incluido en `templates/converzzo/efectos/` y `templates/converzzo/tipografia/`:
- Donde la receta dice `bash "<carpeta de esta skill>/../../preparar.sh"`, corre `bash templates/converzzo/efectos/preparar.sh` (o `tipografia/`) **en la computadora de la persona** (copia la carpeta a `.herramientas/converzzo/` y córrelo desde ahí). Instala el motor la primera vez (1 a 3 minutos).
- Donde dice `~/.claude/efectos-converzzo/GUIA.md`, la guía está en `templates/converzzo/efectos/GUIA.md` (y `tipografia/GUIA.md`).
- **Mandan los criterios de este editor** sobre los valores de la receta: zona segura, tamaños de subtítulos, volumen de sonidos (estándar común), colores del estilo y las reglas de animación (prohibido o permitido solo con función).

**Tanda 1** (12 efectos): revisados contra los criterios del editor; se proponen con confianza. **Tanda 2**: receta incluida, sin probar todavía en este editor: antes de usarla en un video, pruébala sobre un tramo corto y muéstrasela a la persona.

## Nivel 1 · Frecuentes (encajan con el estilo de fábrica)

| Efecto | Qué hace | Tanda |
|---|---|---|
| `zoom-in` | Zoom marcado y suave hacia la cara en una palabra clave de un video vertical u horizontal | 1 |
| `zoom-suave` | Acercamiento lento y cinematográfico hacia la cara durante una frase | 1 |
| `zoom-out` | Efecto de zoom out: el video arranca cerca de la cara y se abre el plano para revelar | 2 |
| `reencuadre` | Convierte un video horizontal en vertical 9:16 siguiendo la cara automáticamente | 1 |
| `cortar-silencios` | Corta automáticamente los silencios y pausas largas de un video hablado, con un zoom alterno en cada corte para que no se note el salto | 2 |
| `limpiar-voz` | Limpia la voz del video: reduce el ruido de fondo, quita el retumbe y las eses fuertes y da presencia a la voz, con volumen estándar de redes (−14 LUFS) | 2 |
| `efectos-sonido` | Agrega efectos de sonido sincronizados al video (whoosh, pop, click, impacto, notificación, caja registradora, obturador, teclas…) en los momentos que se elijan | 2 |
| `estabilizar` | Estabiliza un video grabado con el celular en la mano: quita el temblor y deja un movimiento de cámara suave, con un zoom mínimo para que no se vean bordes. Úsa | 2 |
| `cita` | Muestra una frase destacada con comillas grandes, en serif elegante, con autor y una palabra resaltada en cursiva | 1 |
| `dato` | Muestra un número que sube contando (+30.000, 97%, $2,5M) con una etiqueta, justo cuando se menciona en el video | 1 |
| `pregunta` | Muestra una tarjeta tipo encuesta con una pregunta y opciones (con porcentajes si los da la persona) para invitar a comentar | 1 |
| `cartel-nombre` | Pone el nombre y cargo de quien habla en un cartel inferior (lower third) que entra con una barra de color | 1 |
| `capitulo` | Pone un separador de sección (Parte 2, Paso 3, Error 1) con etiqueta de color y título, arriba de la cara o a pantalla completa | 2 |
| `paso-a-paso` | Muestra una lista numerada de pasos que van apareciendo y marcándose justo cuando se dice cada uno en el video | 1 |
| `gancho` | Pone un título grande en los primeros segundos del video para enganchar, palabra por palabra y con una palabra resaltada | 2 |
| `srt` | Exporta los subtítulos del video como archivo .srt (para subirlo a YouTube, TikTok, Facebook o editarlo en CapCut o Premiere), con la transcripción revisada. Ús | 2 |

## Nivel 2 · Por tipo de contenido

| Efecto | Qué hace | Tanda |
|---|---|---|
| `grafica-datos` | Muestra una gráfica animada con datos reales (barras, línea o dona) que crece mientras se habla de los resultados | 1 |
| `comparativo` | Muestra una comparación en dos columnas (A vs B, ellos vs nosotros, antes vs ahora) con chulos y equis que aparecen punto por punto | 2 |
| `antes-despues` | Muestra un antes y después en pantalla dividida con una barra deslizante, usando dos momentos del mismo video o dos fotos o videos que pase la persona | 2 |
| `lupa` | Pone una lupa que amplía un objeto del video (un detalle de un producto, una etiqueta, un ingrediente) y lo sigue aunque se mueva | 1 |
| `foco` | Oscurece todo menos un objeto o una persona, como un reflector que la sigue, para dirigir la mirada | 1 |
| `congelar` | Congela la imagen del video en un instante durante unos segundos y pone un texto con una flecha dibujada hacia la persona | 2 |
| `tier-list` | Muestra una tier list animada (S, A, B, C…) donde cada elemento cae en su nivel justo cuando la persona lo nombra en el video | 2 |
| `mockup-interfaz` | Muestra una interfaz animada genérica en el video: un chat con mensajes, notificaciones que caen o un prompt de IA que se escribe y responde | 2 |
| `carrusel-video` | Convierte las imágenes de un carrusel de Instagram en video: pasan deslizándose como en la app, con puntos de página y un zoom lento | 2 |
| `parallax-3d` | Convierte un momento del video (o una foto) en una escena 3D: separa el fondo de lo cercano por profundidad y mueve la cámara para dar volumen, como una foto qu | 2 |
| `widgets-vidrio` | Pone tarjetas de vidrio esmerilado con datos (números, progreso, minigráficas) flotando alrededor de la persona | 2 |
| `collage-halftone` | Convierte a la persona en un recorte de papel impreso con trama de puntos sobre papel kraft, con borde blanco, papeles rasgados y movimiento stop motion | 2 |
| `etiqueta-sigue` | Pone una etiqueta con nombre (y un dato corto) unida a un objeto del video con una línea, y la etiqueta lo sigue cuando se mueve | 2 |
| `reencuadre-objeto` | Convierte un video horizontal en vertical 9:16 siguiendo un objeto (un producto, un plato, una mascota) en vez de la cara | 2 |
| `palabra-clave` | Pone una sola palabra enorme que golpea la pantalla para remarcar una idea (GRATIS, ERROR, NUEVO) | 2 |
| `cuenta-regresiva` | Pone una cuenta regresiva: 3, 2, 1 grande con un anillo que se vacía, o un reloj de oferta (horas, minutos, segundos) que baja en vivo | 2 |
| `titulo-detras` | Pone un título gigante detrás de la persona: las letras suben desde abajo y la persona queda por delante, sin pantalla verde | 2 |
| `texto-animado` | Anima un texto libre con 9 animaciones: máquina de escribir, deslizar, rebote, ola, desenfoque, máscara, contorno, glitch o tipografía cinética | 2 |
| `traducir-subtitulos` | Traduce los subtítulos de un video a otro idioma (inglés, portugués u otro) y los pone en el video con cualquier estilo del plugin, además del archivo .srt trad | 2 |
| `ubicacion` | Muestra la ubicación de un negocio: mini mapa ilustrado con la ruta y un pin, nombre, dirección y horario | 2 |
| `logo-sting` | Anima la entrada del logo de la marca: a pantalla completa con fondo de color y destello, o pequeño en una esquina | 2 |
| `fondo-borroso` | Desenfoca el fondo del video y deja a la persona nítida, como el modo retrato del celular, sin pantalla verde | 2 |
| `color-pop` | Deja a la persona a color y el fondo en blanco y negro durante un tramo del video, sin pantalla verde | 2 |
| `camara-lenta` | Pone en cámara lenta un tramo del video, con movimiento fluido y el audio estirado o en silencio | 2 |
| `acelerar` | Acelera un tramo del video (x2, x4…) para pasar rápido por una parte larga, como un time-lapse | 2 |
| `rampa-velocidad` | Rampa de velocidad: el video pasa suave de velocidad normal a cámara lenta (o a rápido) y vuelve, como en los edits de acción y de producto | 2 |
| `dolly-zoom` | Efecto vértigo o dolly zoom: la persona queda del mismo tamaño mientras el fondo se estira o se encoge | 2 |
| `musica` | Pone música de fondo al video que baja sola cuando la persona habla y sube en las pausas (ducking), con entrada y salida suaves | 2 |

## Nivel 3 · Solo si la persona lo pide

Efectos de look, de impacto o pensados para venta. No los propongas; si los pide, se hacen.

| Efecto | Qué hace | Tanda |
|---|---|---|
| `barrido` | Transición de barrido o whip pan: la imagen sale disparada hacia un lado con desenfoque de movimiento y vuelve a entrar, ideal en un corte o cambio de idea. Úsa | 2 |
| `cambiar-fondo` | Recorta a la persona y le pone otro fondo (una foto, un video o un color) sin pantalla verde | 2 |
| `color-auto` | Corrige automáticamente la exposición y el balance de blancos de un video oscuro, amarillo o azulado | 2 |
| `color-referencia` | Copia el color y el ambiente de una imagen de referencia (una foto, un fotograma de una película o un post que le guste a la persona) y lo aplica a todo el vide | 2 |
| `contorno-neon` | Dibuja una línea de luz neón alrededor de la persona o de un objeto que la sigue cuadro a cuadro | 2 |
| `cta-whatsapp` | Pone un llamado a la acción para escribir por WhatsApp: botón verde con número que aparece y se toca, ideal al final del video | 2 |
| `eco` | Deja una estela o eco de la persona o de un objeto que se mueve: copias que se van desvaneciendo detrás | 2 |
| `ficha` | Muestra una ficha de producto u outfit (nombre, detalles como talla, color o material, y precio) con una línea que señala el producto en el video | 2 |
| `flash` | Destello blanco (o de color) en un corte o cambio de idea de un video | 2 |
| `glitch` | Efecto glitch o falla digital en un tramo corto del video: los colores se separan y la imagen salta en franjas | 2 |
| `grano` | Agrega grano de película al video para darle textura analógica o de cine | 2 |
| `ingredientes` | Pone etiquetas que señalan partes o ingredientes de un producto o plato en el video, una por una, con un punto y una línea | 2 |
| `look-pelicula` | Da al video un look de película completo: color de cine, halo en las luces, leve vaivén de la imagen, grano, viñeta y bandas negras | 2 |
| `look` | Aplica un look de color a un video: cálido, frío, cine, blanco y negro, vintage o vivo, en todo el video o en un tramo | 2 |
| `pantalla-verde` | Quita una pantalla verde (o azul) del video con clave de color y pone otro fondo: una foto, un video o un color, o lo deja transparente | 2 |
| `pixelar` | Pixela o desenfoca algo que no se debe ver en el video (un documento, una placa, una pantalla, una cara, un logo) y lo sigue aunque se mueva | 1 |
| `precio-pop` | Pone en un video una etiqueta de precio animada con descuento (precio anterior tachado, precio nuevo que rueda, sello de porcentaje) cuando se menciona el produ | 2 |
| `quitar-fondo` | Quita el fondo del video y lo entrega con transparencia (.mov ProRes 4444 o .webm) para usar a la persona o al producto en cualquier editor, sin pantalla verde. | 2 |
| `rebobinar` | Efecto de rebobinar: el video retrocede rápido con look de cinta VHS y vuelve a reproducir el tramo | 2 |
| `sacudida` | Temblor o sacudida de cámara en un golpe o momento fuerte de un video | 2 |
| `sticker` | Convierte a la persona o un objeto del video en un sticker: borde blanco, sombra y un pequeño salto hacia adelante | 2 |
| `tallas-colores` | Muestra las tallas y colores disponibles de una prenda o producto en una tarjeta animada, marcando las agotadas | 2 |
| `zoom-al-ritmo` | Golpes de zoom sincronizados con el ritmo de la música: en cada beat (o cada 2 o 4) la imagen da un pequeño salto hacia adelante | 2 |
| `zoom-transicion` | Transición de zoom: la cámara entra rápido hacia la imagen hasta el corte y sale abriendo, como pasar a través de la pantalla | 2 |
| `fuentes` | Muestra la biblioteca de 40 fuentes gratuitas del plugin (impacto, modernas, elegantes, manuscritas, divertidas y retro) y ayuda a elegir una o a usar una fuent | 2 |
| `sub-3d` | Subtítulos con letras gruesas en volumen y sombra extruida | 2 |
| `sub-burbuja` | Subtítulos dentro de un globo de chat blanco, con la palabra que se dice en color | 2 |
| `sub-caja` | Subtítulos con la palabra que se dice dentro de una caja de color | 2 |
| `sub-clasico` | Subtítulos clásicos: blanco con borde negro y la palabra que se dice en amarillo | 2 |
| `sub-detras` | Subtítulos gigantes detrás de la persona: la persona queda por delante y tapa parte del texto | 2 |
| `sub-elegante` | Subtítulos serif elegantes con la palabra que se dice en cursiva dorada | 2 |
| `sub-emoji` | Subtítulos clásicos con un emoji que aparece arriba cuando se dice una palabra clave | 2 |
| `sub-impacto` | Subtítulos gigantes de 1 o 2 palabras con la palabra clave en otro color | 2 |
| `sub-karaoke` | Subtítulos que se van pintando de color a medida que se dicen | 2 |
| `sub-manuscrito` | Subtítulos en letra a mano que se escriben solos, con un subrayado dibujado | 2 |
| `sub-maquina` | Subtítulos que se escriben letra por letra como máquina de escribir, en una caja oscura con cursor | 2 |
| `sub-minimal` | Subtítulos discretos: letra fina, sin borde, abajo, y las palabras dichas se iluminan | 2 |
| `sub-neon` | Subtítulos con brillo de neón y un leve parpadeo al aparecer | 2 |
| `sub-pop` | Subtítulos donde cada palabra aparece con un salto | 2 |
| `sub-resaltador` | Subtítulos donde un marcador de color pasa detrás de la palabra que se dice | 2 |
| `sub-retro` | Subtítulos estilo pixel de videojuego, con colores que cambian | 2 |

- `mi-estilo` (fuentes y colores de marca): lo cubre el perfil de la persona (`personalizar.md`).
- `pixelar` sirve para ocultar caras del público, documentos o placas: **solo a pedido**.
- Los estilos de subtítulos `sub-*` reemplazan al estándar del editor: solo si la persona los pide para ese video.
