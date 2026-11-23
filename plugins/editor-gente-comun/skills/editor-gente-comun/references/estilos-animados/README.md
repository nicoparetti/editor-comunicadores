# Estilos de animación precargados

Estilos listos para reels animados narrados, además del estilo por defecto y del estilo propio que la persona arme con sus referencias. Cada uno vive en su archivo: **lee solo el del estilo elegido**, nunca todos.

| # | Estilo | Archivo | Qué es | Para qué contenido | Música que pide | Peso de render |
|---|---|---|---|---|---|---|
| 1 | Escala sin fin | `escala-sin-fin.md` | Formas planas sobre azul noche; un zoom continuo cruza tamaños (del átomo a la galaxia) guiado por un personajito con un lente por ojo | Grandeza de Dios y de la creación, "¿qué es el hombre?", lo pequeño y lo inmenso, perspectiva | `musica_estilo.py cosmos` | Liviano (2D) |
| 2 | Caricatura de los 50 | `caricatura-50.md` | Clase ilustrada de mitad de siglo: figuras geométricas, color corrido del trazo, tarjetas numeradas, un narrador calmo | Lo didáctico: pasos, claves, conceptos, "cómo se hace" | Jazz real: `buscar_sfx.py "jazz" --musica --oir` o la de la persona | Liviano (2D) |
| 3 | RPG de 16 bits | `rpg-16-bits.md` | Un juego de rol de consola de los 90: pixeles, cuadros de diálogo que se escriben solos, menús, batallas, "guardar partida" | Llamado como misión, decisiones, batallas espirituales, historias bíblicas como aventura; público joven | `musica_estilo.py chip` | Muy liviano |
| 4 | Diorama de pixeles | `diorama-pixel.md` | Personajes de pixel parados dentro de una maqueta 3D con niebla, faroles que dan sombra real y foco de miniatura | Historia: aldeas, viajes, escenas bíblicas de noche, misiones | `musica_estilo.py campanas` (o cama de pad) | Pesado (3D) |
| 5 | Isla isométrica | `isla-isometrica.md` | Un mundito de bloques visto en diagonal; cada pieza llega con un rebote y una nota | Algo que crece de a poco: una iglesia, una misión, una vida, una comunidad | `musica_estilo.py campanas` | Pesado (3D) |

**Hoja para mostrar:** `hoja_estilos.jpg` (una imagen por estilo, con su número). Mándala por el chat cuando presentes las opciones. Las imágenes son horizontales porque vienen de los cortos originales; aclara que el editor arma el estilo en vertical.

**Origen y crédito:** estilos inspirados en la biblioteca Lemo-Opuscar de Lemomo (LemoLab), github.com/lemomo-ai/lemo-opuscar. Los textos de estos archivos son propios (escritos desde cero para reels verticales narrados); las imágenes de la hoja son de Lemo-Opuscar con licencia CC BY 4.0. Los videos que se hacen con estos estilos son de quien los hace.

## Cómo se usan (vale para todos)

1. **Elegir.** Muestra la hoja y una línea por estilo (columna "Para qué contenido"). Si el guion ya está, recomienda uno o dos según el tema y di por qué en una frase; la persona elige.
2. **Recordar el audio y los recursos antes de animar** (`reels-animados.md` §1.2): la voz narradora (se recomienda siempre grabarla con la voz propia; la voz sintética, `voz_sintetica.py`, es un recurso solo si la pide), las imágenes y, si el estilo pide música, si quiere la cama del estilo, música propia o ninguna.
3. **Leer solo el archivo del estilo** y seguirlo junto con `reels-animados.md`: el estilo cambia el **aspecto** (paleta, figuras, materiales, movimiento, música); los **tiempos, el aire, el subtítulo continuo, la zona segura, la voz, el storyboard + clip de 7 s y las auditorías** son los de siempre.
4. **Paleta propia:** cada estilo trae una paleta base. Si la persona tiene colores de marca, se aplican dentro de la lógica del estilo (el archivo dice qué se puede cambiar y qué no).
5. **Primera vez con un estilo:** en el storyboard, mostrar los 6 cuadros en el estilo real (no bocetos) y anotar en `ESTADO.md` lo que la persona corrija; si corrige algo del estilo mismo, guárdalo como variante suya en `5_Mi estilo/` (no se cambian las reglas de arriba).
6. **Mezclar estilos:** no dentro de un mismo reel. Un estilo por video.

## Recordatorio en cada reel animado

Aunque la persona ya tenga su estilo propio, cada vez que pida un reel animado nuevo recuérdale en una línea que puede elegir otro: «Lo armo en tu estilo de siempre; si quieres probar otro, tengo cinco precargados (escala sin fin, caricatura de los 50, RPG de 16 bits, diorama de pixeles, isla isométrica): te mando la hoja». Sin insistir: si responde que no, se sigue.

## Base compartida de composición vertical

- **Lienzo:** 1080×1920, 30 fps de salida. Los estilos "a pasos" (pixel, caricatura) cambian dibujos a 8–12 fps, pero la cámara y los fundidos van a 30.
- **Franjas:** arriba la fuente bíblica cuando corresponde (desde y = 250); la acción entre y ≈ 300 y y ≈ 1250; el subtítulo continuo con su centro en y = 1350; nada importante debajo de y = 1540 ni dentro de la columna de botones (`zona-segura.md`).
- **Un sujeto grande por cuadro.** En vertical, lo que en horizontal era "paisaje con personaje chico" se cierra: el personaje o el objeto ocupa al menos un tercio del alto útil.
- **Los textos propios del estilo** (cuadros de diálogo, rótulos, tarjetas) nunca se pisan con el subtítulo: van arriba de y = 1200 o reemplazan al subtítulo en ese tramo (el subtítulo se oculta mientras dura, como en las frases palabra a palabra).
- **Ningún fondo quieto** (`reels-animados.md`): cada estilo dice qué se mueve en las esperas.
