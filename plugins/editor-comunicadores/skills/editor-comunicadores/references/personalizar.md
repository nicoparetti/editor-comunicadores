# Personalizar el estilo

Regla madre: **la persona elige mirando, no leyendo**. Ningún cambio visual se describe solo con palabras: se muestra.

## Cómo se hace una propuesta

1. **Fotogramas reales.** Saca 2–3 fotogramas de su video (`extraer_frames.sh`): uno con la cara, uno con un gráfico, uno con subtítulo. Si todavía no subió nada, usa los fotogramas de ejemplo de `templates/` y aclara que son de prueba.
2. **2 o 3 opciones, nunca más.** Distintas de verdad entre sí (no tres tonos del mismo azul). Cada una con un nombre corto y una frase de para qué sirve ("Cálida: transmite cercanía, va bien con testimonios").
3. **Un tablero por opción**: el mismo fotograma con la opción aplicada (subtítulo, una tarjeta de gráfico, un título) + la muestra de colores con sus códigos + las fuentes escritas con su nombre. Usa la composición `TableroEstilo` del Motor o HTML + captura.
4. **Que elija tocando**: herramienta de preguntas con las opciones y una más "mezclar" (por ejemplo, colores de A con fuentes de B).
5. **Guardar**: los valores van a `5_Mi estilo/mi-perfil.md` (con fecha) y el tablero elegido a `5_Mi estilo/tableros/`. Si el Motor se usa, vuelca los colores a `.herramientas/motor/src/tokens.ts`.

## Qué se puede personalizar y qué no

| Se cambia libremente (estilo) | Se mantiene salvo pedido explícito (criterios) |
|---|---|
| Colores base y de acento | Que los cambios bruscos de zoom caigan en un corte |
| Fuentes de subtítulos y de gráficos | Subtítulos del mismo tamaño en todo el video |
| Sonidos favoritos de cada familia | Que cada sonido esté atado a un evento de imagen |
| Estilo de los gráficos (tarjetas, papel, minimalista) | Zonas seguras de Instagram |
| Cantidad de zooms y de sonidos (más o menos) | Volumen final −14 LUFS |
| Animación de entrada de subtítulos | Transcripción literal y versículos verificados |

Los efectos especiales se eligen del catálogo `efectos.md`, como máximo 3 por pieza, y la persona decide.

Si la persona pide cambiar un criterio, hazlo, pero explícale en una frase qué problema resolvía ("si el zoom cae en medio de una frase se nota un salto"). La decisión es suya; guárdala en el perfil si dice que es para siempre.

## Pedidos típicos y respuesta esperada

- **"Quiero otros colores para mis reels animados"** → 3 paletas sobre una escena real del último reel animado (o una de ejemplo): fondo, texto, acento, mapa. Elige → se guarda.
- **"Cambia la fuente de los subtítulos"** → 3 fuentes libres del kit sobre el mismo fotograma, a tamaño real, con una palabra destacada en la complementaria.
- **"Menos sonidos" / "más sonidos"** → explica la densidad actual (por ejemplo, 10 por minuto en reels a cámara) y propón el nuevo número; aplícalo y guárdalo.
- **"Usa este sonido en vez del clic"** → agrégalo a su banco en `4_Recursos/sfx/`, puntúalo con la persona (1 a 5 estrellas) y anótalo en el perfil.
- **"Quiero que se parezca a este creador"** → flujo de análisis de referencia; al final ofrece sumar al perfil solo lo que la persona apruebe. En los reels animados, la referencia se imita lo más posible (`reels-animados.md` → 1.1); en los demás formatos se adapta su lógica.
