# Estilo precargado · RPG de 16 bits

El reel se ve, suena y **se comporta** como un juego de rol de consola de los años 90: pixeles grandes, paleta limitada, cuadros de diálogo que se escriben letra por letra, menús con un cursor de mano, batallas por turnos, un mapa del mundo y puntos de guardado. La gracia está en contar algo serio con la gramática del juego: el llamado como misión, una decisión como menú, una lucha espiritual como batalla.

**Sirve para:** público joven; vocación y llamado ("elige tu clase", "tu misión principal"), decisiones, batallas espirituales (Efesios 6), historias bíblicas como aventura (David y Goliat, Josué, Pablo en el camino), crecer de nivel (madurez), "guardar la partida" (descanso, fidelidad).
**No sirve para:** temas de dolor o duelo (el tono es lúdico), contenido muy abstracto sin acción.

## 1. Las reglas que lo definen

1. **Resolución baja real.** Todo se dibuja en un lienzo de 270×480 pixeles y se agranda ×4 sin suavizar (1080×1920). Nada se dibuja a resolución alta encima, salvo el subtítulo continuo.
2. **Paleta limitada.** 24–32 colores en total para todo el video. Las sombras y luces son colores de la paleta, nunca transparencias. El tramado (patrón de puntos alternados) hace los degradados.
3. **Movimiento a pasos y en pixeles enteros.** Los personajes caminan con 4 dibujos a 8 por segundo; los parpadeos, fuegos y brillos a 12. La cámara se mueve de a pixel entero del lienzo chico.
4. **Se comporta como un juego.** Cuadros de diálogo que se escriben, menús que se abren, un cursor que duda, números de daño que saltan, un "GUARDADO" que confirma. Cada recurso de juego tiene que significar algo del guion, no ser decoración.
5. **Nada de marcas reales.** Ningún nombre, personaje, logo, interfaz, tipografía ni melodía de juegos existentes. Se toma la gramática, no los dibujos.

## 2. Paleta base (ampliable dentro del límite)

| Uso | Colores |
|---|---|
| Piedra / noche | `#1C1B2E` `#2E3050` `#4A4E78` `#6F75A6` |
| Ventana de diálogo | relleno `#1F3A8A` → `#2D56C2` en tramado, borde `#E8ECF5` |
| Luz / oro | `#FFF4C2` `#FFD86B` `#F2A33A` `#B9652A` |
| Rojo | `#7A1F2B` `#C2393F` `#F06A5A` |
| Verde | `#1E4D3A` `#3C8A54` `#7CC46A` |
| Piel (3 tonos por personaje) | a elección, siempre de la paleta |

Se puede cambiar: los tonos de la ventana de diálogo (a colores de marca), las rampas. No se cambia: el límite de colores, sin transparencias.

## 3. Composición vertical

- El lienzo chico es vertical (270×480). La escena de juego ocupa el centro (filas ≈ 70–300 del lienzo = y ≈ 280–1200).
- **Ventana de diálogo:** ancho completo menos márgenes (x ≈ 130–950 en pantalla), arriba de la escena (y ≈ 260–520) o abajo **por encima de y = 1200**. Mientras hay ventana con texto de la narración, el subtítulo continuo se oculta: la ventana *es* el subtítulo de ese tramo (se escribe al ritmo de la voz, palabra por palabra según Whisper).
- **Menús:** columna a la izquierda (lejos de los botones), 3–4 opciones, cursor de mano.
- **Barra de estado** (nombre, nivel, vida y fe como barras) arriba, chica, en momentos de batalla o de "subir de nivel".

## 4. Figuras

- **Personajes:** 16×24 a 24×32 pixeles del lienzo chico (64×96 a 96×128 en pantalla); cabeza grande, contorno oscuro de 1 pixel, 3 tonos por color. Vista de tres cuartos desde arriba en el mapa; de perfil en batalla.
- **Actuación de juego:** saltito hacia adelante para actuar, pose de lanzar, retroceso al recibir, arrodillarse, parpadeo al quedar fuera de combate. La respiración es subir los hombros 1 pixel.
- **Escenarios:** baldosas de 16×16 (piso, muro, pasto, agua animada en 3 dibujos), antorchas que parpadean, estandartes.

## 5. Movimiento

- **Ventanas:** se deslizan en 0,3 s con frenado al final, en pixeles enteros. El texto se escribe a 25–35 letras por segundo, atado a la voz.
- **Cursor:** la mano sube y baja 1 pixel a 4 por segundo; **se detiene cuando el personaje duda** (es la manera de mostrar una decisión difícil).
- **Esperas:** agua y fuegos animados, estrellas que titilan, el personaje respira, el cursor late. Ningún cuadro congelado.
- **Cambios de paleta** como efecto: un fundido a negro se hace por pasos (4 pasos de oscurecimiento de la paleta), no con transparencia.

## 6. Texto en pantalla

Una fuente pixel de 8×8 o 8×12 hecha a mano o libre (licencia OFL, por ejemplo "Press Start 2P" o "Pixelify Sans"), en el lienzo chico. Mayúsculas para títulos de ventana ("MISIÓN", "INVENTARIO"); frases cortas.

## 7. Transiciones

- **Entrar en batalla:** la pantalla se rompe en bloques que giran (remolino de pixeles), 0,5 s.
- **Viaje:** mapa del mundo con el personaje que camina por un camino de puntos.
- **Cambio de capítulo:** fundido de paleta a negro y título en ventana ("CAPÍTULO 2 · EL LLAMADO").
- **Guardar partida:** un cristal o una luz donde el personaje se detiene; "PARTIDA GUARDADA" con un brillo de 4 dibujos.

## 8. Sonido y música

- **SFX del banco** (siempre los aprobados), más los típicos del estilo hechos con código o del banco: "bip" de letra cada 2–3 letras de diálogo (muy bajo), cursor (clic), confirmar, golpe en batalla (golpe suave), subir de nivel (arpegio corto). Pocos y siempre los mismos.
- **Música (opcional):** `musica_estilo.py chip --dur <segundos de la voz>` (pulso, bajo triangular, ruido con eco). 18–22 dB por debajo de la voz; en los momentos de reflexión baja 6 dB más o se corta a la cama de siempre.

## 9. Cómo construirlo

- HTML con `render(t)`: un `<canvas>` de 270×480 donde se dibuja todo con coordenadas enteras, y se muestra escalado con `image-rendering: pixelated` a 1080×1920. El subtítulo continuo va en una capa aparte a resolución completa.
- Sprites definidos como texto (una letra por color de la paleta) dentro del código, convertidos a `ImageData` una sola vez. Así no hacen falta archivos de imagen y todo es propio.
- Tiempo a pasos: `cuadro = floor(t * 8)` para caminar, `floor(t * 12)` para fuegos y parpadeos.
- Es el estilo más liviano: renderiza rápido incluso en computadoras modestas.

## 10. Errores que hay que evitar

- Mezclar pixeles de distinto tamaño (un elemento dibujado a resolución alta en medio del pixel).
- Transparencias o suavizado (aparecen colores fuera de paleta).
- Recursos de juego sin significado (un menú porque sí).
- Copiar ventanas, fuentes o melodías de un juego conocido.

## 11. Antes de mostrar

Storyboard con: un mapa o escena con el personaje, una ventana de diálogo escribiéndose, un menú con cursor, una batalla o "subir de nivel" y un "partida guardada". En el clip de 7 s, revisa que el texto de la ventana va al ritmo exacto de la voz.
