# Plantillas: reel con motion graphics (reel el reel de referencia con gráficos, 10 nov 2026)

Código real del reel "el reel de referencia con gráficos". Copiar a `3_Videos editados/<nombre>/trabajo/` y adaptar tiempos, textos y estilo.

| Archivo | Dónde corre | Para qué |
|---|---|---|
| `base_corte_zoom.py` | Mac (device_bash) | Corta el bruto según `cortes.json`, aplica golpes de zoom animados y acercamiento lento anclados en la cara (zoompan sobre ×2). Uso: `python3 base_corte_zoom.py <seg_ini> <seg_fin> parte.mov` |
| `sfx_pista.py` | Mac | Arma la pista de SFX con numpy (eventos, nivel base + GAIN 9 dB, limitador propio) |
| `componer.py` | Mac | Base + capas VP9 con alfa + subtítulos `.ass` + mezcla → `comp.mov` (luego `masterizar_audio.py`). Uso: `python3 componer.py superfast` |
| `graficos_ejemplo.py` | Nube (Bash + Playwright) | Genera `graficos.html` con todos los gráficos y `render(g, t)`. Necesita `map.json` (d3-geo + world-atlas), las fuentes en `assets/` y el ícono del barco (función `ship`) |
| `retratos_camafeo.py` | Nube | Siluetas de perfil tipo camafeo (el reel de referencia con gráficos con bandas, Perkins con gola) |
| `render_capas.js` | Nube | Renderiza cada gráfico fotograma a fotograma con alfa (`node render_capas.js g1 g2 …`); después `ffmpeg … -c:v libvpx-vp9 -pix_fmt yuva420p` |
| `medir_aire.js` / `medir_pecho.js` | Nube | Verifican aire interno de tarjetas (tinta) y el centrado entre mentón y subtítulos |
