# Hub de contenido

El hub es un documento de Claude (Claude Docs) donde vive cada contenido de la persona, conectado al editor por un archivo del proyecto. Cuando diga "edita el reel de X", lees su pestaña y ya sabes el guion, la edición sugerida y los recursos.

## Cómo se arma (una sola vez)

1. **Proyecto de Claude.** El editor y el hub viven en el mismo proyecto. Si la persona no está trabajando dentro de un proyecto, explícale cómo crear uno ("Editor de videos") y que vuelva a escribirte desde ahí.
2. **Crea el documento** "Hub de contenido · <su nombre o cuenta>" con estas pestañas:
   - **Pestaña 1 · Resumen:** un cuadro con una fila por contenido (título, formato, estado: propuesto / idea / guion / grabado / editado / publicado, fecha, enlace a su pestaña). Debajo del cuadro, dos secciones: **Ideas en espera** y **Decisiones fijas** (lo que vale para todos sus contenidos).
   - **Una pestaña por contenido**, con el nombre del contenido (por ejemplo, "Reel · el llamado de Abraham"). Se crea una nueva por cada contenido.
   - **Una pestaña por video largo** del que se saquen clips (prédica, clase, charla), con todos sus clips adentro: ver "Pestaña de clips" más abajo.
3. **Conéctalo al editor.** Copia la plantilla `templates/HUB - leer primero.md`, pon el enlace del documento y pídele que la suba a los **archivos del proyecto** (Proyecto → Archivos → agregar). Explícale por qué: así, en cualquier conversación del proyecto, el editor encuentra su hub sin que tenga que pegarlo. Este paso solo lo puede hacer ella: guíala con una acción por mensaje, diciéndole qué va a ver en pantalla, y espera que te confirme que el archivo quedó subido antes de seguir con otra cosa.

## Cada pestaña de contenido

1. **Guion**, en un cuadro de dos columnas: a la izquierda el texto por bloques; a la derecha, la **edición sugerida** de cada bloque (tipo de plano o escena, zoom, gráfico, sonido, destacado).
2. **Recursos a descargar:** imágenes, mapas, retratos, documentos o referencias, con enlace y fuente.
3. **Copy:** el texto para la publicación.
4. **Otras observaciones:** investigación, frases, datos verificados, pendientes.

## Pestaña de clips (videos largos)

Cuando la persona pide clips de una prédica, una clase o un video largo, **todo va al hub**, no a un documento ni a una página aparte: es el único lugar donde vive su contenido. **Una pestaña por video largo, no una por clip**: elegir clips es comparar, y eso se hace con todos a la vista.

Nombre de la pestaña: **"Clips · <título del video>"**. Adentro, de lo general a lo particular:

1. **Ficha del video:** fecha, duración, enlace a YouTube (o la ruta del archivo) y la frase central del mensaje.
2. **Mapa del video:** un gráfico de la intensidad de la voz a lo largo de todo el video (`clips-de-predicaciones.md` → 1.2), con cada clip marcado como una franja de color y el pico señalado. Guarda la curva completa medida, para poder dibujarla por debajo de los recortes. Colores: cálido para los picos, gris para la calma.
3. **Ranking:** un cuadro con una fila por clip: número, título, duración, pico de intensidad, gancho y estado (propuesto · aprobado · editado · publicado), que la persona cambia desde la celda.
4. **Un apartado por clip**, en el orden del ranking:
   - sus recortes, cada uno con inicio y fin (el inicio abre YouTube en ese segundo) y la frase;
   - el porqué del clip y el gancho sugerido;
   - la nota de armado (puentes, frases quitadas);
   - la entrega, que se completa al terminar: ruta del video final y de su portada;
   - el copy, que se escribe cuando la persona aprueba el clip.

**En la pestaña Resumen:** una fila por clip (cada uno se publica por separado y tiene su estado), todas con enlace a la pestaña de clips de ese video.

**La persona aprueba en el hub antes de editar:** puede corregir, comentar ("este corte no", "sube este al puesto 2") y cambiar estados. Lee esos cambios antes de empezar a editar.

Si no tienes la herramienta de documentos de Claude en la conversación, arma la misma estructura en `Hub de contenido.md` (el gráfico como lista de tramos con su intensidad).

## Edición sugerida

- Incluye siempre los criterios base del formato (los de `estilo-por-defecto.md` y el manual del formato).
- Como máximo **3 efectos especiales por pieza** (del catálogo `efectos.md`), marcados **"a decidir"**, o ninguno si no hacen falta. La persona decide cuáles quedan.
- Usa el mismo vocabulario que el editor (golpe de zoom, destacado acumulativo, cita acumulativa, formato A/B/C) para que la edición sea directa.

## Cómo se usa después

- **Al editar:** si el contenido tiene pestaña, léela antes de la hoja de edición y respeta lo que diga; anota en la hoja los cambios respecto del plan.
- **Al terminar:** actualiza el estado en el cuadro resumen (editado) y anota en la pestaña la ruta del video final y su portada. En los clips, actualiza la fila de ese clip en el Resumen y en el ranking, y completa su "Entrega".
- **Ideas nuevas:** si la persona menciona una idea suelta, ofrécele anotarla en "Ideas en espera".
