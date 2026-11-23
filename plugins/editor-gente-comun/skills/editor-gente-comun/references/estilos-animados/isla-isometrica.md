# Estilo precargado · Isla isométrica

Un mundito de bloques facetados, visto en diagonal sin perspectiva (todo a la misma escala, cerca o lejos), sobre un mar quieto y un cielo con degradado suave. Lo que importa es **ver crecer**: cada pieza (una casa, un árbol, un faro, una persona) llega con un pequeño rebote y suena con una nota. Calmo, prolijo, con mucho espacio vacío.

**Sirve para:** todo lo que crece de a poco o se construye: la iglesia de Hechos (de 12 a 3000), una misión en una isla, una vida edificada sobre la roca, una comunidad, el Reino como semilla, un proyecto o un llamado que se despliega.
**No sirve para:** conflicto o drama fuerte, explicaciones con muchos textos.

## 1. Las reglas que lo definen

1. **Todo es bloque.** Hexágonos o cuadrados de terreno, casas de caja con techo a dos aguas, árboles de conos o esferas facetadas, personas de cápsula. Caras planas con su sombreado, sin texturas.
2. **Cámara isométrica.** Vista en diagonal desde arriba, sin perspectiva (proyección ortográfica). La cámara gira despacio alrededor de la isla y se acerca o aleja, pero nunca baja a nivel del piso.
3. **Construir es la actuación.** Cada pieza que aparece llega con una curva de rebote (cae, se pasa un poco, vuelve) y una nota musical. A veces brota sola un detalle (una ventana que se enciende, humo de una chimenea, una flor).
4. **Espacio y calma.** Mucho mar y cielo alrededor. Pocas piezas a la vez; nunca una lluvia de objetos.
5. **Luz de un solo lado y cielo en degradado.** Una luz cálida principal y una luz ambiente fría; al anochecer, las ventanas y los faroles se encienden.

## 2. Paleta base

| Uso | Color |
|---|---|
| Cielo día (degradado) | `#BFE3E8` → `#F7E9D3` |
| Cielo noche | `#141A3C` → `#2A2F66` |
| Mar | `#3F8FB0` (aguas bajas `#6FC2C9`) |
| Pasto | `#8CC084` `#5E9C6A` |
| Piedra / arena | `#E8D6B0` `#C8B08A` |
| Techos | `#D9725B` `#B8574A` |
| Luz de ventanas | `#FFD27A` |

Se puede cambiar: techos y acentos (a colores de marca), el momento del día. No se cambia: los pasteles suaves y el degradado del cielo.

## 3. Composición vertical

- La isla ocupa el centro (y ≈ 450–1150) y crece hacia los costados sin salir de la zona segura; si crece mucho, la cámara se aleja en vez de recortar.
- Arriba (y ≈ 280–420), un título o un número grande en blanco con sombra suave ("12 → 3000").
- Rótulos chicos sobre piezas importantes (el nombre de un lugar) con una línea fina que baja hasta la pieza.
- El mar vacío de abajo deja aire al subtítulo continuo.

## 4. Figuras

- **Personas:** cápsulas con una esfera de cabeza, 2–3 colores de ropa; sin cara. Se mueven deslizándose y "saltando" de a una baldosa.
- **Piezas reutilizables:** terreno (pasto, arena, piedra, agua baja), casa, iglesia simple con campanario, faro, árbol, muelle, barco, puente, pozo, fogata.
- Cada pieza nueva puede brotar un detalle propio 0,3–0,6 s después (ventana encendida, bandera, humo).

## 5. Movimiento

- **Llegada de pieza:** cae desde 0,6–1 m arriba (o crece desde 0), 0,35–0,5 s, con un rebote que se pasa ≈ 8 % y vuelve. Siempre en la palabra que la nombra o en la cuenta que la voz hace.
- **Series** ("y se sumaron más y más"): las piezas llegan en cadena con 0,08–0,15 s entre una y otra, cada una con su nota (escala ascendente).
- **Esperas:** la cámara gira despacio (≈ 3–5° por segundo), el agua tiene olas facetadas, nubes chicas derivan, los barcos se mecen.
- **Día a noche:** el cielo pasa de un degradado al otro en 1,5–2 s y las ventanas se encienden una por una.

## 6. Texto en pantalla

Sans redondeada y limpia, en blanco o en el azul de la noche, con mucho interletrado en los títulos. Números grandes para los contadores.

## 7. Transiciones

- La cámara se aleja hasta que la isla queda chica y aparece otra isla (otro lugar, otra etapa).
- Un puente o un barco une dos islas: la cámara lo sigue.
- Fundido por el cielo: el degradado cambia y la escena siguiente ya está ahí.

## 8. Sonido y música

- **Cada pieza que llega suena** (es parte del estilo): una nota de campana o marimba de la escala de la música. Se genera con la misma función que `musica_estilo.py campanas` o con el pop del banco para las piezas chicas. Las series suben de nota.
- **SFX del banco:** whoosh suave en los alejamientos de cámara, golpe suave en el remate.
- **Música:** `musica_estilo.py campanas --dur <segundos de la voz>`, en la misma tonalidad que las notas de las piezas. 18–22 dB por debajo de la voz.

## 9. Cómo construirlo

- Three.js con `OrthographicCamera` (isométrica: rotación 45° en vertical, ≈ 35° de inclinación). Geometrías simples (`BoxGeometry`, `CylinderGeometry`, `ConeGeometry`, `IcosahedronGeometry` con pocas caras) con `flatShading`.
- Agua: un plano facetado con olas por vértice. Cielo: un plano de fondo con degradado.
- La lista de llegadas (pieza, momento, nota) sale de la lista de palabras de la voz; la misma lista genera los sonidos (sincronía exacta).
- **Es pesado** si hay sombras suaves: usar una sola luz con sombra y resolución moderada; medir un cuadro antes del render completo.

## 10. Errores que hay que evitar

- Perspectiva (deja de ser isométrico).
- Piezas que llegan sin sonido o sonidos sin pieza.
- Demasiadas piezas a la vez (pierde la calma).
- Colores saturados fuera de la paleta pastel.

## 11. Antes de mostrar

Storyboard con: la isla vacía al inicio, una pieza a mitad de su rebote, una serie creciendo, el pase de día a noche, la isla completa al final. En el clip de 7 s, revisa que cada pieza suena exactamente cuando aterriza.
