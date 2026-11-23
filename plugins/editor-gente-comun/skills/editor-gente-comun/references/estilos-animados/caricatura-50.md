# Estilo precargado · Caricatura de los 50

Una clase ilustrada de mitad del siglo XX: figuras humanas hechas de formas geométricas, fondos que son planos de color (no habitaciones dibujadas), el color impreso un poco corrido respecto del trazo, tarjetas numeradas, flechas curvas punteadas y un narrador que explica con calma, una idea por cuadro. Se anima "a pasos": el cuerpo queda quieto y lo que trabaja son las manos y los objetos.

**Sirve para:** lo didáctico y lo práctico: "tres claves para…", pasos de un hábito espiritual, cómo estudiar la Biblia, cómo descubrir tu llamado, conceptos explicados con orden.
**No sirve para:** momentos solemnes o de gran emoción (el tono es amable y simpático), historias épicas.

## 1. Las reglas que lo definen

1. **Trazo y color separados.** El trazo es tinta negra irregular, apenas quebrada; el color es plano y está corrido 3–6 px respecto del trazo (como una impresión mal registrada). Ese desfase es la firma del estilo.
2. **Figuras geométricas.** Cabeza = óvalo o rectángulo con esquinas redondeadas; torso = trapecio; brazos y piernas = líneas finas con manos de mitón. Ojos de punto, nariz larga de perfil. Nada anatómico.
3. **Fondo = planos de color.** Un "living" es un rectángulo ocre, un rectángulo verde y una lámpara de tres líneas. Nunca perspectiva ni sombras.
4. **Animación limitada.** El cuerpo mantiene la pose; cambian las manos, la boca y los objetos. Los dibujos cambian a 12 cuadros por segundo; la cámara, las flechas y los fundidos van suaves a 30.
5. **Una idea por cuadro.** Cada frase tiene su tarjeta, su número o su objeto. Al pasar a la siguiente idea, la anterior se va.

## 2. Paleta base

| Uso | Color |
|---|---|
| Papel de fondo | `#F1E6CF` |
| Plano cálido | `#E3A23B` (mostaza) |
| Plano frío | `#5E9EA0` (verde azulado) |
| Rojo | `#D9533A` |
| Azul profundo | `#2F4B7C` |
| Tinta | `#1E1A17` |
| Rosa suave (franjas) | `#EEC3B5` |

Se puede cambiar: los planos (a colores de marca, siempre en tonos apagados de época). No se cambia: el papel claro, la tinta negra, el desfase del color.

## 3. Composición vertical

- **Arriba (y ≈ 280–520):** el título de la idea o el número de paso en una medalla redonda (círculo con borde doble y número grande).
- **Centro (y ≈ 560–1180):** la figura y su objeto. La figura de cuerpo entero mide ≈ 520–620 px de alto, apoyada a la izquierda o a la derecha según la escena (nunca invadiendo la columna de botones desde y = 720).
- **Tarjetas de consejo:** un cartel con bordes en punta ("TIP" se reemplaza por "CLAVE", "OJO", "PASO 2") arriba de y = 1200.
- Cuando hay 3 pasos, se apilan en vertical (medallas una debajo de otra con flechas curvas punteadas que bajan), no en fila horizontal.

## 4. Figuras

- **El narrador en pantalla (opcional):** una figura que señala con el dedo, de perfil o tres cuartos, que aparece en los momentos de explicación y se va en los de ejemplo.
- **Gestos posibles:** señalar, contar con los dedos, rascarse la cabeza, sostener un objeto, encogerse de hombros. Cada gesto es un cambio de dibujo, no una interpolación.
- **Objetos:** hechos de 2–3 formas con su trazo y su color corrido (una Biblia = rectángulo con banda y cinta; un reloj = círculo con dos líneas).

## 5. Movimiento

- **Entradas:** los objetos aparecen de golpe en un cuadro (sin rebote) o con un "iris" (un círculo que se abre); las tarjetas bajan con una caída corta.
- **Flechas curvas punteadas:** se dibujan de un punto al siguiente en 0,4–0,6 s cuando la voz nombra el paso siguiente.
- **Esperas:** el color corrido "tiembla" 1 px cada 2–3 cuadros (como una película vieja), los objetos chicos oscilan, la figura parpadea. Ningún fondo quieto.
- Cada gesto cae en la palabra que lo pide (marca de Whisper).

## 6. Texto en pantalla

Tipografía de cartel de época: una serif gruesa y redondeada para títulos y una sans geométrica en versalitas chicas para subtítulos de tarjeta. Números grandes dentro de las medallas. Frases cortas.

## 7. Transiciones

Iris (círculo que se cierra sobre el objeto de la idea siguiente), barrido de un plano de color que cruza la pantalla, o corte seco con cambio de color de fondo. La cámara casi no se mueve: lo que se mueve es el dibujo.

## 8. Sonido y música

- **SFX del banco:** clic de texto por tarjeta, pop por medalla, swoosh corto en el iris, golpe suave en la clave final. Pocos y siempre los mismos.
- **Música (opcional):** el estilo pide jazz suave de combo (vibráfono, contrabajo, escobillas). No se fabrica con código (la prueba sonó falsa): se busca grabado con `buscar_sfx.py "jazz" --musica --licencia cc0,by --oir` (avisar si es CC BY: lleva crédito en la descripción) o la persona aporta la suya. Siempre 18–22 dB por debajo de la voz. Sin música, la cama grave de siempre.

## 9. Cómo construirlo

- HTML con `render(t)` y canvas 2D. Cada figura es una función que dibuja trazo y relleno por separado; el relleno se dibuja primero, desplazado (dx, dy) fijo por objeto.
- Trazo irregular: el contorno se dibuja con pequeñas variaciones de grosor (± 15 %) y un temblor de 0,5 px que cambia cada 2 cuadros, con semilla fija (sale igual en cada render).
- Tiempo a pasos: `paso = floor(t * 12) / 12` para gestos y temblor; `t` continuo para cámara, flechas y fundidos.
- Textura de papel: un ruido muy suave fijo sobre el fondo (no animado).

## 10. Errores que hay que evitar

- Degradados, sombras o perspectiva (deja de ser de época).
- Color perfectamente alineado con el trazo (pierde la firma).
- Movimiento interpolado de todo el cuerpo (debe ser limitado).
- Demasiadas ideas en un cuadro.

## 11. Antes de mostrar

Storyboard con una medalla de paso, una figura señalando, una tarjeta de clave y un iris a medio cerrar. En el clip de 7 s, revisa que los gestos caen en la palabra justa.
