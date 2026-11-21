# Estilo por defecto

Este es el estilo con el que viene el editor: está decidido y medido, reel por reel, a lo largo de muchas rondas de corrección. Aplícalo tal cual mientras la persona no diga otra cosa. **Su perfil (`5_Mi estilo/mi-perfil.md`) manda sobre este archivo**, y lo que pida en la conversación manda sobre los dos; anota el conflicto en la hoja de edición.

## 1. Tono y contenido

- Pensado para **comunicadores que enseñan**, no para vender: claridad, profundidad y cercanía antes que efectos.
- El tono, el público y el tipo de contenido salen del perfil de la persona.
- **Contenido cristiano:** solo si el perfil dice que su contenido es cristiano se activan los versículos en pantalla (en la versión bíblica de su perfil), la fuente bíblica de los reels animados, los términos en griego y hebreo y las reglas de transcripción de términos bíblicos.
- Los guiones, copys e ideas viven en su **hub de contenido** (ver `hub.md`). Aquí llegan para producirse.

## 2. Formatos y ritmo

| Formato | Corte cada | Gráfico cada | Música | Subtítulos quemados |
|---|---|---|---|---|
| **Reel vertical 9:16, principal** | 2–4 s, corte en cada idea; ≤4 cortes de contenido del bruto | 3–6 s | 10–15 % bajo la voz | Énfasis frecuente + `.srt` |

**Ritmo de habla:** se mide con sus primeros videos (palabras por minuto de la transcripción) y se guarda en el perfil. Como referencia, un ritmo típico es de unas 172 palabras por minuto, y 1:10 de video son unas 200 palabras.

**Duración:** la decide la persona. Un reel suele rendir mejor hasta 1:10. Si el guion o el video que llega es claramente largo para un reel, ofrece acortarlo, sin hacerlo por tu cuenta: «El video dura 1:45, y en reels suele rendir mejor hasta 1:10. ¿Quieres que te proponga qué partes sacar para acortarlo, o lo dejamos completo?»

## 3. Exportación

- Reels 1080×1920 (9:16); YouTube 1920×1080. Fotogramas: los del bruto (por ejemplo, 29,97 o 30).
- H.264, 10–20 Mbps, **SDR (nunca HDR)**.
- **Audio de toda entrega: −14 LUFS integrados, pico verdadero ≤ −1 dBTP, AAC 48 kHz estéreo.** Las exportaciones de CapCut no llegan solas a ese nivel (suelen salir cerca de −19,5 LUFS y a 44,1 kHz). Por eso `revision.mp4` sale siempre masterizado, y cuando la persona exporta desde CapCut se le ofrece masterizar ese archivo final con `masterizar_audio.py` (copia la imagen tal cual y solo corrige el audio): «Tu video exportado suena más bajo de lo normal en redes. ¿Quieres que lo deje al volumen ideal? Es un paso rápido y no cambia nada más.» Después de masterizar, dile qué escuchar: que los whooshes y la voz no suenen aplastados por el limitador.
- **Mejor calidad en lo que se guarda:** H.264 `-preset slow -b:v 20M -maxrate 20M`, AAC 320 kbps.
- **Qué se guarda y dónde:** en la carpeta se guarda **solo el video editado final** (con subtítulos, en la mejor calidad) **y su portada**. La versión limpia (sin subtítulos), el `.srt` y cualquier otra capa se muestran **en el chat** y se aclara que no se guardan para no ocupar espacio: si los quiere, los descarga desde ahí. Los intermedios van a `trabajo/` dentro del proyecto y se borran al cerrar el video, sin preguntar.
- **Portada con cada entrega (los 4 tipos de contenido):** junto con la versión final va siempre una portada, en 1080 × 1920 y con lo esencial dentro del centro 1080 × 1350 para que se vea en la grilla del perfil. Se entregan una principal y una alternativa; la elegida se guarda junto al video. Criterio por tipo: `portadas.md`.

## 4. Cómo se graba y se limpia

- Normalmente **varios clips**, cada uno con una parte del video final: ordenarlos y unirlos según el guion, y después cortar dentro de cada clip.
- A veces un plano fijo (la variedad sale de reencuadres y gráficos) y a veces muchos planos (cambios cada 3–5 s). Detecta en la ingesta cuántos planos hay y decídelo en la hoja.
- Limpieza: quitar las muletillas que tropiezan y las tomas repetidas (queda la última buena).
- **Pausas: corte ajustado por defecto.** Se quitan casi todas, también las cortas (mediana de pausa quitada de referencia: 0,25 s; ritmo en pantalla resultante: ~186 palabras por minuto). **Pregunta siempre en la hoja de edición** si este video da para dejar pausas más amplias (hasta 0,5 s): «¿Dejo pausas un poco más amplias para que el mensaje respire, o cortes bien ajustados?»
- **Arranque en movimiento (opcional):** el reel puede abrir con 2 micro-clips (~0,13 y ~0,17 s) del gesto previo a hablar (acomodarse, levantar el objeto), con un sonido de cuerpo o ambiente bajo (al ~70 %), y un clic cuando aparece el primer objeto en cámara. **Nunca lo agregues por tu cuenta:** si el bruto tiene ese gesto, pregunta: «Al inicio del video hay un gesto que sirve para arrancar en movimiento. ¿Lo usamos?»
- Texto y gráficos **pueden ir sobre la cara si el impacto lo justifica** (palabra clave a pantalla completa); por defecto, fuera de la boca.
- **Sin adornos de edición, por defecto:** cortes secos (sin fundidos ni cortinillas), sin filtros que cambien el look y sin efectos sobre el video (temblor, glitch, brillos). La luz o el color se corrigen solo si la persona lo pide, y el golpe de zoom de la idea central es la excepción. **Si pide un efecto, se hace**, siempre sutil y con una función en el mensaje. Ejemplo que funciona en videos de enseñanza: marcar un *blooper* o error que se deja a propósito, con la imagen en blanco y negro y la voz con efecto de micrófono de aire (como una radio vieja), y volver al color normal al seguir. No propongas efectos por tu cuenta salvo que el momento lo pida claramente; en ese caso, sugiérelo en la hoja y que decida.

### Términos de la persona

Lo que el transcriptor confunde (nombres, su cuenta, sus términos) está en la sección 7 de su perfil. Si el contenido es cristiano: Espíritu Santo, Biblia, Palabra, Cristo y Él (referido a Dios) van con mayúscula. Cada nombre propio nuevo se verifica y se suma al perfil.

## 5. Subtítulos (estándar cerrado tras muchas rondas de corrección)

Es lo que más rondas de corrección costó. No improvises nada aquí.

### Calibración (1080×1920)

- 1 pt de CapCut ≈ **4,54 px**. 11 pt ≈ **50 px**.
- Posición -600 pt ≈ **y = 1260 px** (-0,312 del cuadro).
- Ancho seguro de texto: **600 px** (zona segura unificada IG + TikTok, `zona-segura.md`).

### Base

- **Cal Sans SB** (archivo `CalSans-SB.ttf`, en CapCut "CalSans-SB"), **blanca**, **11 pt**, interletrado **-1**.
- Sin contorno ni fondo. Solo una **sombra muy suave y difusa** (copia negra desenfocada al ~30 %, sin desplazamiento).
- Posición **fija en -600 pt** todo el video. No subirla ni bajarla para esquivar objetos.
- **Excepciones:** reels 100 % animados (`reels-animados.md`) y clips de prédicas (`clips-de-predicaciones.md`).
- En dos renglones, el **primer renglón queda en -600** y el segundo va debajo. El bloque no se centra.
- **Tamaño estándar en todo el video: 11 pt**, destacados incluidos. Un cambio de tamaño a mitad del video es un error.
- **Única excepción: la tipografía complementaria.** Sus palabras llevan el tamaño en pt que haga falta para verse del **mismo tamaño visual** que Cal Sans a 11 pt (con PlayfairDisplay-SemiBoldItalic, ~15 % más: ≈12,5 pt). Se iguala la altura que se ve, no el número de pt; se calcula midiendo la altura de las minúsculas de ambas fuentes (lo hace `subtitulos.py`). Nunca se agranda una palabra para destacarla: el destaque lo dan la fuente y el color.
- Un solo estilo por video: **bloques de 2–4 palabras**, minúsculas normales, **sin punto final**.
- **Un renglón siempre que entre** (a 11 pt entran hasta 4 palabras). Dos renglones solo si no cabe en 600 px; si no, se corta en dos bloques. **Nunca separar una preposición de su complemento.**
- **Interlineado medido:** "lo más cerca posible sin que se toquen". En cada bloque de dos renglones se dibuja cada renglón, se mide la tinta (incluidas las letras que bajan, como q, p o g, y las que suben en la cursiva) y el segundo renglón se ubica a **6 px de tinta** del primero. Lo hace `subtitulos.py`.
- **Animación de entrada: opcional, se pregunta en cada video:** «¿Quieres que los subtítulos entren con un leve golpe o que aparezcan quietos? El golpe da más energía; quietos queda más sobrio.» Si va: cada subtítulo aparece casi al instante (fundido de 50 ms) y arranca apenas más grande para asentarse en su tamaño final (106 % → 100 % en 130 ms). Si no va: `--sin-animacion`.
- **Transcripción literal**: el texto en pantalla va tal como lo dijo, con su forma de hablar (voseo incluido si habla con voseo), sin resumir ni reformular. Se pueden omitir palabras sueltas que sobran (una "y" aislada) consultando. Los nombres propios se corrigen y se consulta si hay duda.

### Complementaria y color

- Siempre **itálica y con color**: por defecto **PlayfairDisplay-SemiBoldItalic** (`PlayfairDisplay-SemiBoldItalic.ttf`), **amarillo crema #F6F6A8**.
- Máximo **dos tipografías por video** (o por secuencia). Serif o decorativas, solo ocasionalmente.
- Palabras clave sueltas: pocas por video, complementaria itálica crema, tamaño compensado, en el mismo renglón que el resto.
- Descartado: acento dorado #F5B714 con Oswald Bold y colorear la palabra activa.

### Destacado acumulativo (remates)

- Las palabras se suman una a una **sin moverse**; la frase completa queda hasta el bloque siguiente. 1–3 por video.
- **No** se colorea la palabra activa. Solo las palabras clave van en complementaria (ej.: "porque *largo* no es / sinónimo de *profundo*"); el resto en Cal Sans blanca.
- Mismo tamaño visual que el resto, nunca más grande.
- **Sonido:** la palabra destacada lleva un sfx que la acompaña al aparecer. Si en la frase hay dos palabras destacadas, las dos llevan el mismo sfx. Antes de ponerlo, revisa si en ese instante ya suenan otros sfx parecidos: si queda cargado, baja el volumen o deja uno solo.

### Golpe de la idea central

Cuando llega el remate de una idea central (la frase que resume el mensaje), va el sonido más fuerte del video: un tap con peso más un golpe de zoom. Puede haber uno o dos por video, según cuántas ideas fuertes tenga. Los demás destacados suenan suaves para que este se note. Los destacados caen donde están los zooms de la tesis y el cierre: texto y cámara refuerzan los mismos momentos.

### Entrega de subtítulos

- **Se guarda en la carpeta:** el video final con los subtítulos quemados, en la mejor calidad.
- **Solo en el chat** (no se guardan): la **capa transparente .mov** (ProRes 4444 con alfa, mismo tamaño y duración que el video) y el **`.srt`**.
- Método: `.herramientas/scripts/subtitulos.py` genera el `.ass` (mide cada renglón con PIL, valida ≤600 px, un evento por renglón para controlar el interlineado); FFmpeg lo renderiza (`subtitulos_capa.sh`, `quemar_subtitulos.sh`). Después, `verificar_subtitulos.py`.

## 6. Zoom y cámara (medido en el reel de referencia a cámara)

- **Base a 100 %** la mayor parte del tiempo (~75–80 % del video). El zoom se reserva para los momentos clave.
- **Ningún salto de escala dentro de un clip.** Todo cambio de escala brusco cae en un corte.
- **Golpe de zoom en el corte (punch): ~130 %** (rango 120–140 %), con el encuadre **subido** para que la cara quede arriba y el objeto entre en cuadro (en CapCut, posición y entre −0,07 y −0,23). Se usa en el **remate de cada ítem** de una lista y en la **mitad fuerte de una tesis**. Se vuelve a 100 % en el corte siguiente, sin sonido.
- **Escalera de zoom: 100 → 120 → 140 %** en dos cortes seguidos (~1 s y ~0,8 s) para el **clímax de una idea**. Sin sonido. Si hace falta, se corta el clip sin quitar nada solo para escalonar.
- **Acercamiento lento: 100 → 140 % en 2,7–3,4 s, lineal** (sin curva de aceleración), para **construir** hacia un giro o hacia el remate de una anécdota.
- **Salida rápida: 140 → 100 % en 2 fotogramas**, escondida en un gesto real (apartar el objeto) y con whoosh, en el **giro** del video (de la lista a la tesis).
- **Sin zoom en el llamado a la acción.** El llamado va de un tirón.
- **En reels con gráficos:** el golpe de zoom es un zoom-in rápido animado (0,2 s) y todo zoom animado va anclado en la cara; después de un acercamiento lento, salida rápida en 7 fotogramas con whoosh. Detalle en `reels-con-graficos.md` → 7.
- Los cortes de pausa no se tapan cambiando el zoom: los tapa el movimiento real (manos, objeto). Si el bruto está muy quieto, avísalo en la hoja en vez de inventar zooms.

## 7. Sonido

**Banco de sonidos puntuado:** antes de elegir cualquier efecto, lee `4_Recursos/BANCO_SFX.md` en la carpeta de trabajo (copia en `references/banco-sfx.md`; si difieren, manda el de la carpeta). Usa primero los de 5★, alterna con los de 4★ y no uses los de 1–2★ salvo pedido. Los nuevos se suman a los de siempre, no los reemplazan.

### Volumen de los SFX: un solo estándar para todos los tipos de reel

Lo que se iguala es cuánto suena cada sonido frente a la voz, no la cantidad de sonidos (el reel animado lleva muchos más por minuto). Cada sonido tiene un nivel base según su importancia:

| Sonido | Nivel base |
|---|---|
| Golpe de la idea central | −4 / −5 |
| Taps de destacados e ítems | −5 / −6 |
| Golpes suaves | −5 / −8 |
| Clics de rótulos | −6 / −10 |
| Pops | −7 / −10 |
| Papel | −7 / −10 |
| Whooshes | −7 / −11 |
| Cambios de escena | −10 |
| Tics | −9 / −12 |

Cada efecto se normaliza a pico = nivel base **+12 dB**, la pista de efectos pasa por su propio limitador (`alimiter limit=0.89`, ataque 1 ms, release 60 ms) **antes** de sumarla a la voz, y después todo va a −14 LUFS. Como referencia del reel a cámara, así los whooshes suenan entre 6 y 8 dB sobre los picos de la voz y los clics entre −2 y +3 dB.

### SFX del reel a cámara

- **Pocos y con sentido, de principio a fin:** el mismo criterio vale para todo el video, también la reflexión, la anécdota, la aplicación y el cierre. Cada efecto sale de un evento de imagen (algo que aparece o un cambio de zoom), nunca de relleno. Densidad de referencia: **unos 10 por minuto, ~1 cada 3–4 cortes**.
- **Dos familias, cada una con un significado fijo:**

| Familia | Cuándo | Sincronía |
|---|---|---|
| **Clic / snap / botón / tap** | Aparece un objeto en cámara, un ítem nuevo de lista o un golpe de la tesis | Sobre el corte o hasta 0,07 s antes |
| **Whoosh / aire** | Cambio de encuadre: golpe de zoom o salida rápida de zoom; cortinilla o transición marcada | **0,13–0,17 s antes** del corte (el aire "trae" el cambio) |

Archivos: las familias del banco libre (`banco-sfx.md`), con los de 5★ primero.

- **Sin sonido:** la escalera de zoom, los acercamientos lentos, las vueltas a 100 % y los versículos. En el llamado a la acción, solo si hay un evento de imagen que lo pida.
- **Arranque (solo si se aprueba para ese clip):** sonido de cuerpo o ambiente bajo (al ~70 %) en los micro-clips iniciales, y clic cuando aparece el primer objeto.
- **Reels con motion graphics:** más efectos (~30/min), cada uno atado a un evento del gráfico (`reels-con-graficos.md` → 8). Ítems de lista con tap, pop o clic, nunca rasgueo de pluma.
- **Gráficos que todavía no tienen referencia** (contador, lista animada, tachado): usa la familia por analogía. Que algo aparezca es un clic; que algo cambie o se mueva es un whoosh. Propónlo en la hoja para que se apruebe.

### Voz

Corte de graves a 75 Hz + compresión suave, objetivo **−14 LUFS / −1 dBTP** en la mezcla final. Detalle técnico en `entorno-y-herramientas.md`.

### Música (se agrega en CapCut)

- Nunca tapa la voz: siempre muy por debajo (bajar más si compite). Reels: 10–15 % bajo la voz.
- Mood: reflexivo/íntimo (pads, piano) → épico/motivacional en el cierre. Sin letra bajo la voz.
- Entregar notas por bloques (timecode, energía, qué hace la música, términos de búsqueda). El editor no elige canciones; la biblioteca con licencia es de cada persona (`4_Recursos/musica/`).

## 8. Color

No menciones LUT ni corrección de color. Solo si la persona pregunta si puedes corregir el color, responde que sí: corrección sutil de luz y color, o su propio LUT (`.cube` en `4_Recursos/luts/`) aplicado a la mitad de intensidad, solo en la pista principal.

## 9. Diseño de gráficos y versículos

- **Estilo de gráficos por defecto: "Continuidad"**: Cal Sans + complementaria crema sobre tarjetas oscuras translúcidas (radio 26), inserts a pantalla completa en papel claro con rótulos cartográficos. Valores en `Motor/src/tokens.ts`. El estilo puede cambiar por video (tableros de estilo); los lineamientos de formatos, animación, sonido, cortes y zooms de `reels-con-graficos.md` se mantienen.
- Íconos: trazo fino, un solo color. No redibujar logos: se usan reales (`4_Recursos/logo/`).
- **Versículos** (solo con contenido cristiano): en la versión bíblica del perfil. Verificar siempre el texto con búsqueda web antes de ponerlo en pantalla. Formato: texto en cursiva y debajo la cita (libro capítulo:versículos, versión). La precisión bíblica no es negociable.
- Datos en pantalla: arrancar con el número duro, no con "un estudio dice…". Verificar cifras.
