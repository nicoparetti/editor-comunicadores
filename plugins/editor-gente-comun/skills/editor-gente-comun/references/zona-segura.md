# Zona segura unificada 9:16 (Instagram + TikTok)

Decidida por la persona . Une la plantilla de Instagram ("AllSocials") y la de TikTok tomando en cada borde **la más restrictiva**. Reemplaza a la plantilla de Instagram 2024 (250/385/70/55–193). Vale para **todo lo vertical 1080×1920**: reels a cámara, reels con gráficos, reels animados, clips de predicaciones (placa final incluida) y portadas de reels.

## Medidas (px, lienzo 1080×1920)

| Borde | Instagram | TikTok | Unificada | Límite en coordenadas |
|---|---|---|---|---|
| Arriba | 250 | 250 | **250** | nada importante con y < 250 |
| Abajo | 380 | 320 | **380** | nada importante con y > 1540 |
| Izquierda | 120 | 120 | **120** | nada importante con x < 120 |
| Derecha (parte alta) | 120 (borde dibujado en x = 952) | 120 | **130** | hasta y = 720: x ≤ 950 |
| Columna de botones | 200 de ancho, 1200 de alto (desde y = 720) | ≈ 240 de ancho, 768 de alto (desde y = 1152) | **240 de ancho desde y = 720** | desde y = 720: x ≤ 840 |

Área libre resultante:

- **y 250–720:** x 120–950 (830 px de ancho).
- **y 720–1540:** x 120–840 (720 px de ancho).
- **Ancho máximo de un elemento centrado en x = 540 por debajo de y = 720: 600 px** (x 240–840). Es el límite que más se toca.

Plantilla para superponer en las revisiones: `templates/zona-segura/zona_segura_9x16.png` (PNG con alfa: franjas oscuras semitransparentes y borde amarillo). Superposición rápida sobre un fotograma: `scripts/zona_segura.py fotograma.png salida.jpg`.

## Subtítulos

- Tamaño, tipografías y posición **no cambian** (reel y = 1260, clip y = 922, animado y = 1350), siempre centrados en x = 540.
- **Ancho máximo de renglón: 600 px** (antes 860). Los subtítulos típicos miden 350–500 px y entran con margen; solo los renglones de 4 palabras largas pasan de 600 (ej.: «responsabilidad, vocación y asignación» ≈ 694 px). Esos se parten en dos bloques o en dos renglones con `/`, sin separar una preposición de su complemento.
- `subtitulos.py` y `verificar_subtitulos.py` validan los 600 px.

## Gráficos, fotos, tarjetas y objetos 3D

- Todo lo importante (textos, rostros, fotos, tarjetas, objetos 3D) dentro del área libre. Fondos, texturas, halos de luz y degradés pueden ocupar todo el cuadro.
- Por debajo de y = 720 el centro útil está en x = 480, no en 540: un bloque que no entra centrado se corre a la izquierda (contenedor con margen derecho de 240 px) en lugar de achicarlo de más.
- Pares de fotos o tarjetas lado a lado: por encima de y = 720 tienen x 120–950; si bajan de 720, x 120–840.
- Auditorías automáticas con estos valores: `templates/reel-animado/preset/auditoria_zona.py` (textos, fotos y tarjetas del HTML) y `auditoria_3d.py` (secuencias 3D).
