# Portadas de video (los 4 tipos de contenido)

Con cada entrega final va siempre una portada. No se pregunta si la quiere: se entrega junto con el video.

## Reglas comunes

- **Formato:** 1080 × 1920, JPEG calidad 95 (sRGB).
- **Grilla del perfil:** lo esencial (frase y protagonista) dentro del centro 1080 × 1350 (y ≈ 285–1635), que entra en el recorte 3:4 y en el 4:5. Respeta además la zona segura (`zona-segura.md`).
- **Frase:** corta (2–6 palabras), literal del video o del guion: la tesis, la pregunta del gancho o el remate. No inventes un eslogan. Si el cuadro ya muestra un titular que dice lo mismo, no agregues otro.
- **Tipografía:** la del video (la base de los subtítulos con la palabra clave en la complementaria y su color). Sin subtítulos, sin la fuente bíblica, sin logo salvo que se pida.
- **Dos opciones:** una principal y una alternativa (otro cuadro u otra frase), con una línea de por qué cada una representa el video. La elegida se guarda junto al video final como `portada_<nombre>.jpg`; la otra solo se muestra en el chat.
- **Control:** mírala a tamaño completo y en una vista simulada de la grilla (recorte 3:4 reducido a ≈ 360 px de ancho): que la frase se lea, que nada importante quede cortado y que tildes y acentos estén bien.

## Por tipo

| Tipo | Imagen | Frase |
|---|---|---|
| **Reel a cámara** | El fotograma con la mejor expresión: ojos abiertos, gesto claro, sin la boca a medio decir. Busca candidatos en una hoja de contactos cada 0,5 s | Frase gancho corta, sin tapar la cara |
| **Reel con gráficos** | Un fotograma con la cara y un elemento gráfico del video (un mapa, un retrato, una tarjeta), con el mismo estilo gráfico del reel | Frase gancho corta |
| **Reel animado** | El cuadro que mejor representa el video: un solo foco claro (figura, objeto 3D, mapa con la ruta, término en el idioma original), la idea central legible sin audio, contraste fuerte. Renderiza la pista de gráficos sin subtítulos y saca una hoja de contactos cada 0,5 s. Si ninguno sirve, compónla con los elementos del video (mismo color, figura u objeto protagonista, centrado) | Frase literal del guion, en la tipografía del reel |
| **Clips de prédicas** | Un fotograma del predicador en un gesto fuerte del clip | Una frase del clip, con las tipografías de la serie. Todas las portadas de una serie llevan el mismo diseño |

## Cómo se hace

Fotogramas con `extraer_frames.sh` o `hoja_contactos.sh`; composición en HTML + captura (Playwright) o PIL, con las fuentes de `4_Recursos/fuentes/`. Un degradé suave detrás de la frase si el fondo no da contraste; nunca una caja.
