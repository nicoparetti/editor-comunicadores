# Preset · reel animado (storyboard + clip de 7 s antes de editar)

Las reglas están en `references/reels-animados.md`. Copiar estos archivos a `trabajo/` junto con `../base/`.

| Archivo | Qué hace |
|---|---|
| `pausas_ia.py` | Voz con IA: acorta solo los silencios que se pasan de un tope (fin de oración 0,50 s · coma 0,45 s · excepciones por palabra en `EXC`), deja 0,10 s al inicio y 1,6 s al final, y reescribe las marcas de Whisper. Uso: `python3 pausas_ia.py voz.wav palabras.json voz_v1`. |
| `aire_escenas.py` | Suma aire antes de la primera palabra de cada escena (+0,25–0,35 s; tras el remate de la aplicación, +0,55 s) y re-temporiza todo. Editar `EXTRA` (índice de palabra → segundos). |
| `marcas.py` | Lleva la palabra que abre cada tramo de voz al inicio real del tramo (corrige marcas tardías de Whisper). |
| `audio_preview.py` | Audio del clip de 7 s: voz tratada, SFX con un sonido por aparición, cama sonora (≈ 12 dB bajo la voz, con octavas altas) y limitador; después `masterizar_audio.py`. |
| `audio_full.py` | Lo mismo para el video completo, con pads de los momentos espirituales a la par de la voz. |
| `obj3d.py` | Objetos 3D: `iglesia`, `plataforma` y `altar` (con transformación plataforma → altar). `TEMA=gris|noche python3 obj3d.py altar 2.4 salida.png 1`. |
| `render_reel.py` | Render por mitades de un HTML con `render(t)`. |
| `auditoria_zona.py` | Mide la tinta de cada texto y las cajas de fotos y tarjetas cada 0,25 s contra la zona segura. |
| `auditoria_3d.py` | Lo mismo para los objetos 3D. |
