# Estilo precargado · Diorama de pixeles

Personajes de pixel, dibujados a mano como recortes planos, parados dentro de una maqueta en 3D: casas, muelles, caminos y rocas de bloques simples, con niebla, faroles y antorchas que dan luz y sombra de verdad, y un foco de miniatura (arriba y abajo desenfocado) que hace que todo parezca un juguete visto desde arriba. Es cálido, nocturno y teatral.

**Sirve para:** historia narrada con lugares: aldeas, puertos, viajes misioneros, escenas bíblicas de noche (Nicodemo, la pascua, Getsemaní, Pedro junto al fuego), una comunidad que se reúne, una luz que llega a un lugar oscuro.
**No sirve para:** conceptos abstractos sin lugar, explicaciones con muchos datos.

## 1. Las reglas que lo definen

1. **Personaje plano, mundo con volumen.** Los personajes son dibujos de pixel (planos, siempre mirando a cámara como un cartel) dentro de un escenario 3D. Esa mezcla es la firma.
2. **La luz cuenta la historia.** Cada lámpara, farol o fuego ilumina y proyecta sombras reales. Una escena empieza oscura y se enciende; lo importante es lo que está iluminado.
3. **Cámara alta en tres cuartos, foco de miniatura.** Se mira desde arriba en diagonal; una franja horizontal está nítida y lo de arriba y abajo se desenfoca. Parece una maqueta.
4. **Los dibujos van a pasos; lo demás se desliza.** Caminar: 4 dibujos a 6–10 por segundo; parpadear cada pocos segundos; cambio de pose = cambio de dibujo. Cámara, luces, partículas y niebla, en cambio, se mueven suave.
5. **Materiales simples.** Cajas y cilindros para construcciones; planos con textura de pixel para el follaje; agua con brillos en escalones. Nada de modelos detallados.

## 2. Paleta base

| Uso | Color |
|---|---|
| Noche, sombras | `#0E1524` `#1A2438` |
| Piedra, madera fría | `#3A4152` `#5A4A3E` |
| Madera iluminada | `#9A5A2E` `#C9793A` |
| Luz de fuego | `#FFC46B` (núcleo `#FFF1C8`) |
| Agua | `#12304A` con brillos `#5FA8C9` |
| Ropas de personajes | rojos y azules apagados de la paleta, 3 tonos cada uno |

Se puede cambiar: el color de la luz (más fría para "presencia", más cálida para "hogar"), las ropas. No se cambia: la noche como base y la luz como protagonista.

## 3. Composición vertical

- La cámara en vertical se acerca más que en horizontal: el escenario ocupa y ≈ 350–1200 y el personaje mide al menos 180–260 px de alto en pantalla.
- La franja nítida del foco de miniatura cae sobre los personajes (y ≈ 650–1000); arriba y abajo, desenfoque gradual.
- **Cuadro de diálogo** (si el guion lo pide): marco simple con borde de 2 px, arriba (y ≈ 280–480); mientras está, el subtítulo continuo se oculta.
- El viñeteado oscuro de los bordes ayuda a que los textos de arriba y el subtítulo se lean.

## 4. Figuras

- **Personajes:** 24×40 a 32×48 pixeles de arte, agrandados ×5–×6 sin suavizar; contorno oscuro, 3 tonos por color, un detalle que los identifica (un manto, un bastón, un farol en la mano).
- **Poses:** quieto (2 dibujos que alternan lento), caminar (4), levantar el farol, arrodillarse, señalar, abrazar (dos personajes que se juntan y cambian a un dibujo conjunto).
- **Escenarios:** se arman con piezas reutilizables (casa, muelle, puente, pozo, árboles, rocas) en escalas coherentes.

## 5. Movimiento

- **Cámara:** paneos lentos y continuos sobre la maqueta, acercamientos suaves a quien habla. Nada de sacudidas.
- **Luces:** las llamas titilan (intensidad ± 15 % a 10 por segundo), los faroles se balancean apenas. Encender una luz = la intensidad sube en 0,4 s y aparecen sus sombras.
- **Esperas:** niebla que deriva, partículas (brasas, luciérnagas, polvo) que suben despacio, agua con brillos. Ningún cuadro quieto.
- Cada acción del personaje cae en la palabra que la nombra.

## 6. Texto en pantalla

Fuente pixel legible (OFL) dentro de los cuadros de diálogo; títulos de capítulo en una serif clásica sobre fondo oscuro, centrados arriba.

## 7. Transiciones

- Viaje de cámara sobre la maqueta de un lugar a otro (preferido).
- Apagar todas las luces (fundido a noche) y encender las del siguiente lugar.
- Cambio de capítulo: la cámara sube y se aleja hasta ver la maqueta entera, corte, y baja al nuevo lugar.

## 8. Sonido y música

- **SFX del banco:** whoosh suave en los viajes de cámara, pasos (si se busca un sonido real de pasos: `buscar_sfx.py --tema pasos_piedra`), golpe suave en las revelaciones; el fuego puede llevar una cama de fogata real bajita (`--tema fogata`).
- **Música (opcional):** `musica_estilo.py campanas` (más lento, `--tempo 72`) o la cama grave de siempre. 18–22 dB por debajo de la voz.

## 9. Cómo construirlo

- Three.js (como los objetos 3D del motor): cámara en perspectiva con ángulo alto, luces puntuales con sombras (máximo 3–4 con sombra a la vez), niebla exponencial, viñeteado.
- Personajes como planos (`Sprite` o `PlaneGeometry`) con textura de pixel y filtro "nearest"; siempre de frente a la cámara.
- Foco de miniatura: dos pasadas (escena nítida + escena desenfocada) mezcladas con una máscara de franja horizontal; o, más barato, desenfoque solo en dos franjas superpuestas arriba y abajo.
- **Es pesado:** probar primero un cuadro (`still`) y medir cuánto tarda; si cada cuadro tarda más de 1 s, bajar la resolución de sombras, reducir luces con sombra o renderizar por tramos.

## 10. Errores que hay que evitar

- Personajes demasiado chicos (en vertical se pierden).
- Todo iluminado parejo (se pierde la noche y el juguete).
- Personajes de pixel suavizados o en otra escala de pixel que el resto.
- Más de 4 luces con sombra (el render se vuelve lentísimo).

## 11. Antes de mostrar

Storyboard con: la maqueta entera desde lejos, un acercamiento a un personaje con su luz, un momento de luz que se enciende, un viaje de cámara a medio camino. Medir el tiempo de render de un cuadro y anotarlo en `ESTADO.md` antes de comprometer el video entero.
