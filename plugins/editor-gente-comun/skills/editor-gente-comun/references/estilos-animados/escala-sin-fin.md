# Estilo precargado · Escala sin fin

Un viaje continuo entre tamaños: se arranca en algo que se puede tocar (una mano, una semilla, una persona) y la cámara se aleja o se acerca sin cortes hasta lo inmenso (la Tierra, el sistema solar, la galaxia) o hasta lo diminuto (la célula, el átomo). Todo es plano, opaco, sobre un azul noche profundo. Un personajito redondo con un lente por ojo guía el viaje: donde mira, va la cámara. Una regla de escala en un costado dice cuánto se está viendo.

**Sirve para:** la grandeza de Dios y de la creación (Salmo 8, Salmo 19, Isaías 40, Job 38), "¿qué es el hombre?", lo pequeño que importa (el grano de mostaza, el pajarillo, los cabellos contados), perspectiva y propósito ("tu vida dentro de algo más grande").
**No sirve para:** historias con muchos personajes, diálogos, procesos paso a paso.

## 1. Las reglas que lo definen

1. **Plano y opaco.** Cada objeto es un color sólido con, como mucho, un segundo tono para el lado en sombra. Nada de degradados, desenfoques, transparencias, contornos ni sombras proyectadas.
2. **El brillo son anillos, no halos.** Algo luminoso (una estrella, el sol, una luz que señala) se apoya sobre dos discos concéntricos, uno y dos pasos más claros que el fondo, con borde duro. Nunca un resplandor difuso.
3. **Escala verdadera dentro del cuadro.** Lo que aparece junto en un mismo cuadro está a la misma escala. Si algo no entra a escala, no se muestra junto: se viaja hasta él.
4. **Un solo viaje.** El video es, en lo posible, un movimiento de cámara continuo con paradas. Las paradas son los momentos de la narración; entre paradas, la cámara viaja. Los cortes secos son la excepción (cambio temático evidente).
5. **El guía mira primero.** Antes de cada viaje, el personaje del lente dispara una línea de puntos desde su ojo hasta un anillo de "próxima parada"; recién entonces la cámara va.

## 2. Paleta base

| Uso | Color |
|---|---|
| Fondo (noche) | `#1B1F4A` con un segundo plano `#232A5E` |
| Anillos de brillo | `#2C3570` y `#38428A` |
| Acento cálido (lo importante, el guía) | `#F6B935` |
| Acento frío (cielo, agua, planetas) | `#3D7BE0` |
| Rojo de detalle | `#E2553F` |
| Crema (textos, estrellas) | `#F4EBDD` |

Se puede cambiar: el acento cálido (a un color de marca), el acento frío. No se cambia: el fondo oscuro azulado (es lo que hace que los anillos se lean), lo plano.

## 3. Composición vertical

- La parada ocupa el centro (y ≈ 500–1150). El guía vive abajo a la izquierda (x ≈ 140–360, y ≈ 1050–1230), fuera de la columna de botones, y se mueve poco.
- **Regla de escala:** una barra fina vertical en el borde izquierdo (x ≈ 130, de y ≈ 420 a 1180) con 5–6 marcas y un indicador que se desliza; arriba de la barra, el ancho de lo que se ve ("1 metro", "12 700 km", "100 000 años luz"). Es texto del estilo: va arriba de y = 1200 y nunca choca con el subtítulo.
- **Rótulo de parada:** "PRÓXIMA PARADA" en versalitas chicas + el nombre (Tierra, una célula) al lado del anillo, en crema.
- Fuente bíblica arriba (y ≥ 250) cuando el verso se cita textual.

## 4. Figuras

- **El guía:** un círculo de color con un lente grande (anillos concéntricos oscuro-claro-oscuro), dos "alas" rectangulares azules (paneles), una antena con una bolita roja. Respira (sube y baja 4 px en 2 s), parpadea el lente cada 4–6 s. Expresión con la inclinación del cuerpo, no con cara.
- **Personas:** siluetas planas simples (cabeza círculo, cuerpo trapecio), de un solo color, sin rasgos. Si la persona tiene un estilo de figuras propio, se usa ese en versión plana.
- **Astros y células:** círculos y elipses con un segundo tono en medialuna; galaxias como espirales de puntos de 2–4 colores; estrellas como cruces de 4 puntas y puntos.

## 5. Movimiento

- **Viaje de escala:** zoom exponencial (la escala se multiplica igual en cada segundo, no se suma), con entrada y salida suaves en las paradas. Un viaje de 3–4 órdenes de magnitud dura 1,5–3 s; nunca menos de 1 s.
- Durante el viaje, el número de la regla corre y el indicador se desliza; al llegar, el número se queda quieto y el anillo de la parada se dibuja.
- **Esperas:** las estrellas titilan (crema ↔ un paso más oscuro, a destiempo), las galaxias giran despacio, el guía respira. Nada queda congelado.
- **Lo que se nombra, se marca:** cuando la voz dice el nombre de algo, aparece su anillo (escala 0 → 1 con un pequeño rebote, 0,25 s).

## 6. Texto en pantalla

Sans redonda y geométrica para rótulos (la del estilo por defecto sirve en peso semibold). Números grandes en la regla. Nada de textos largos: la palabra o el número que la voz acaba de decir.

## 7. Transiciones

Todas por escala: el objeto actual se vuelve un punto dentro del siguiente (alejarse) o un punto crece hasta llenar la pantalla (acercarse). Entre mundos sin relación de tamaño (de una célula a una ciudad), fundido a azul noche de 0,3 s y la regla vuelve a cero.

## 8. Sonido y música

- **SFX del banco:** whoosh suave en cada viaje (0,13 s antes de que arranque), clic de texto cuando aparece un rótulo de parada, un pop cuando se dibuja un anillo, golpe suave en la revelación. Sin brillos chillones.
- **Música (opcional, la persona decide):** `musica_estilo.py cosmos --dur <segundos de la voz>`: un colchón cálido con pocos destellos de campana, 18–22 dB por debajo de la voz. Sin música, la cama grave de siempre.

## 9. Cómo construirlo

- Un solo HTML con `render(t)` (`templates/reel-animado/`). Coordenadas de mundo en escala logarítmica: cada objeto tiene un tamaño real y una posición; la cámara es un par (centro, ancho visible). Se dibuja con canvas 2D, sin filtros.
- Para que el zoom exponencial no tiemble: posiciones relativas al objeto de la parada actual (no a un origen lejano) y redondeo a medio píxel solo en los bordes.
- Las curvas de viaje se calculan desde la lista de palabras: cada parada empieza en la palabra que la nombra.

## 10. Errores que hay que evitar

- Objetos a escalas distintas en el mismo cuadro (una persona del tamaño de la Tierra).
- Viajes demasiado rápidos: el ojo no alcanza a leer la regla.
- Brillo hecho con blur o transparencia (rompe el estilo).
- El guía tapando el sujeto o metido en la columna de botones.

## 11. Antes de mostrar

Storyboard de 6 cuadros con al menos dos paradas de escalas muy distintas y un viaje a medio camino (cuadro con la regla corriendo). En el clip de 7 s, comprueba que el primer viaje se entiende sin la voz.
