# HyperFrames: herramientas sueltas

HyperFrames (HeyGen, licencia Apache 2.0) está instalado como **caja de herramientas**, no como motor: los gráficos se hacen en Remotion. Manual oficial completo en `.herramientas/manuales/hyperframes/` (`media-use/SKILL.md` y sus `references/`). Carga siempre el entorno antes (`source .herramientas/scripts/entorno.sh`): pone el CLI en el PATH, apunta al Chromium local y enlaza el modelo de recorte.

## Recorte de persona (texto o gráficos detrás de la persona)

- Imagen: `hyperframes remove-background foto.jpg -o recorte.png --device cpu --json`
- Video: `bash .herramientas/scripts/recorte_persona.sh <video> <ini_s> <fin_s> 3_Videos editados/<n>/trabajo/recorte_<id> 3_Videos editados/<n>/trabajo/entrega/2_GRAFICOS/<nombre>.mov` (reanudable; ~5 s por fotograma en CPU, así que úsalo en tramos cortos de 1–3 s).
- Modelo: `u2net_human_seg` en `.herramientas/modelos/` (local, gratis).
- En CapCut: video original abajo → gráfico/texto en el medio → recorte arriba, alineados en el mismo segundo.
- Úsalo solo cuando el efecto resuelve algo (palabra clave detrás de la cabeza en un remate). Revisa bordes de pelo y manos a tamaño real.

## Efectos de sonido

- 21 efectos de HyperFrames ya copiados en `4_Recursos/sfx_pixabay/` (licencia Pixabay: uso libre, comercial incluido). `manifest.json` describe cada uno (energía y uso recomendado).
- El mapa de sonidos de la persona (`estilo-por-defecto.md` → Sonido) manda: estos son alternativas cuando un sonido del mapa no funciona.
- La búsqueda en Openverse de `media-use` no está disponible (su cliente no pasa por el proxy). Para Openverse usa `buscar_sfx.py` en el espacio en la nube (`sonido-real-y-oido.md`).

## Color y looks

- `hyperframes media-treatment` y `grade-compare` trabajan sobre composiciones de HyperFrames. El color del video se corrige solo si la persona lo pide (`estilo-por-defecto.md` → 8). Úsalos solo para comparar grados sobre un fotograma (`grade-compare --for frame.png --luts a.cube,b.cube`) cuando haya LUT candidatos.

## Lo que no se usa

- HeyGen (avatares, voces, música de catálogo): es de pago. No lo uses sin que la persona lo pida.
- Voz sintética (Kokoro) y video generado: fuera del estilo por defecto salvo pedido explícito.
- HyperFrames como motor de gráficos: no, para no mezclar dos lenguajes visuales.
