# Sonidos reales, oído y afinación

Tres herramientas para el sonido (versión 0.5 de los scripts, 22 nov 2026). Nacieron de un reel de @nzstudio__._ que proponía tres herramientas gratis para que Claude "oiga": Earshot, Real SFX y Openverse. De Real SFX (Clipwing) se tomó solo la idea de afinar.

| Herramienta | Para qué | Dónde corre |
|---|---|---|
| `buscar_sfx.py` | Buscar y bajar grabaciones reales con licencia abierta (Openverse: Freesound, Wikimedia y otros) | **Espacio en la nube** (`Bash`); el resultado se pasa a la carpeta de la persona |
| `oido.sh` (Earshot) | Escuchar: qué pasa en cada segundo de una mezcla, si un sonido coincide con lo que se busca, A/B, grabado o sintético | **Espacio en la nube** siempre |
| `afinar_sfx.py` | Que un sonido con tono (arpa, campana, shofar, chime) no desafine con la música | Donde esté el audio (máquina de la persona o la nube); solo numpy y FFmpeg |

**Por qué en la nube:** Earshot necesita ~2,5 GB de memoria al escuchar (más de lo que suele tener libre la máquina de trabajo) y baja sus modelos de huggingface.co, que en la máquina de la persona está bloqueado.  El espacio en la nube **se borra al cerrar cada sesión**: el primer uso de cada sesión reinstala solo (≈ 1 min Earshot + ≈ 1 min modelos). La persona no hace nada.

**Preparar la nube en cada sesión que use estas herramientas:** copia `buscar_sfx.py`, `sonidos_biblicos.json`, `oido.sh` y `afinar_sfx.py` desde `scripts/` de esta skill a una carpeta de trabajo de la nube (por ejemplo `~/sonido/`) y corre `bash oido.sh instalar` en segundo plano mientras haces otra cosa.

## 1. Buscar sonidos reales (Openverse)

**Cuándo:** falta un sonido en el banco (un objeto, un lugar, un ambiente), la persona pide "sonidos bíblicos" o un tema concreto, o hace falta una cama de ambiente (fuego, viento, mar, multitud).

1. Mira qué temas ya están bajados en la carpeta: `device_list_dir` de `4_Recursos/sfx_openverse/`.
2. En la nube, con `EDITOR_RAIZ` apuntando a una carpeta que imite la de la persona (`mkdir -p ~/sonido/raiz && export EDITOR_RAIZ=~/sonido/raiz`):
   - `python3 buscar_sfx.py --temas`: los 50 temas bíblicos preparados (`sonidos_biblicos.json`: página de Biblia, pergamino, shofar, viento recio, lenguas de fuego, piedra del sepulcro, cadenas, velo que se rasga, gallo, ovejas, paloma, Mar de Galilea, Getsemaní, templo…).
   - `python3 buscar_sfx.py --tema shofar --oir`: un tema, ordenado por el oído de Earshot.
   - `python3 buscar_sfx.py "wooden boat creak" --max 5 --oir`: búsqueda libre. **Palabras en inglés**: así están etiquetados los audios.
   - `python3 buscar_sfx.py --todos`: todos los temas que falten. Reanudable: mientras diga `SIGUE`, se repite.
   - Si un tema nuevo se va a usar seguido, súmalo a `sonidos_biblicos.json` (en la skill y en `.herramientas/scripts/`).
3. Pasa cada carpeta de tema a la carpeta de la persona, en `4_Recursos/sfx_openverse/<tema>/`, con `device_commit_files`.
4. **Punto de control:** pásale a la persona `hoja.png` y `escuchar.mp3` por el chat. La hoja dice en qué segundo de `escuchar.mp3` está cada candidato, su licencia y qué oyó Earshot. La persona puntúa de 1 a 5★.
5. Con su puntaje, renombra cada archivo con el número adelante, como en `sfx/` (`5_pagina_biblia_04_cc0.wav`), y suma los de 4–5★ a `4_Recursos/BANCO_SFX.md` (y a la copia `references/banco-sfx.md`) en la sección "Sonidos reales (Openverse)". No borres nada de `4_Recursos/`.

**Licencias:**
- Por defecto solo **CC0 y dominio público**: no exigen crédito.
- **CC BY** (`--licencia cc0,by`) solo si CC0 no alcanza (el script lo avisa: el shofar, por ejemplo, casi no tiene grabaciones CC0). Exige el crédito en la descripción del reel: la línea de `CREDITOS.md`, en el formato «título», autor, CC BY 4.0, enlace. Avisa a la persona cada vez que un sonido CC BY entre en un video, con la línea lista para pegar.
- **Nunca** NC (no comercial) ni ND (sin derivados): el script no los baja.
- `fuentes.json` guarda autor, página, licencia y enlace de cada sonido: no lo borres, es la prueba de la licencia.

**Límites de Openverse:** sin cuenta acepta pocas consultas por minuto (error 429). El script reintenta y espera, pero `--todos` puede tardar varias llamadas. Si la persona quisiera bajar mucho, una clave gratuita de Openverse (`OPENVERSE_TOKEN`) sube el límite; no hace falta para el uso normal.

**Cómo entran en la mezcla:**
- Los candidatos llegan con el silencio inicial recortado y el pico a −3 dBFS: nivélalos como el resto del banco, relativos a la voz.
- Un sonido real nuevo es **otro archivo de la misma familia**, no una familia nueva: la página de Biblia de Openverse alterna con `sfx/paper.mp3` en la familia Papel; el shofar o el arpa son un énfasis puntual, no un clic. Se mantiene la regla de reels animados: mucha cantidad, poca variedad.
- **Camas de ambiente** (fogata, viento, mar, multitud, templo): bien por debajo de la voz, como los pads; propone el nivel y dile a la persona qué escuchar.
- Un sonido con tono sobre música pasa por `afinar_sfx.py` (§3).

## 2. El oído (Earshot)

Earshot (github.com/Leonxlnx/earshot, Leon Lin, MIT) escucha con dos modelos abiertos (CLAP y el etiquetador AudioSet) y devuelve palabras y números. **No reemplaza el oído de la persona:** da pistas medidas para decidir qué tiene que escuchar él.

**Qué se sube a la nube:** solo el audio, nunca brutos. En la máquina de la persona:
`ffmpeg -i revision.mp4 -vn -ac 2 -ar 48000 -c:a libmp3lame -b:a 192k trabajo/oido_mezcla.mp3`, después `device_stage_files`. Si importa el cruce con los cortes de imagen, sube además un proxy chico (`-vf scale=270:-2 -crf 32 -an`) y pásalo con `--video` (directamente con `earshot timeline`).

| Comando (en la nube) | Cuándo |
|---|---|
| `bash oido.sh revisar mezcla.mp3 "1.52,2.10,…" [perfil.json]` | Antes del punto de control 8 de cualquier video con SFX. Los tiempos son los de la lista de efectos del script de sonido (en reels animados, los eventos `EV` del script de SFX). Da la línea de tiempo (qué suena en cada momento), la sincronía (% de efectos con un ataque a menos de 40 ms de su marca), huecos, acentos más fuertes, sonoridad, una hoja visual y si suena grabado o sintético |
| `bash oido.sh elegir "a page of a book being turned" *.wav` | Elegir entre candidatos (lo mismo que `buscar_sfx.py --oir`) |
| `bash oido.sh ab v1.mp3 v2.mp3 ["descripción"]` | Antes de mandarle a la persona una corrección de sonido: qué cambió, en palabras |
| `bash oido.sh real pad.wav` | Si un pad o efecto hecho con código suena "a código"  |
| `bash oido.sh describir sonido.wav` | Qué es un sonido sin nombre claro (los `capcut_*` de la caché, por ejemplo) |
| `bash oido.sh perfil carpeta_reels/ perfil.json` | Una vez: perfil de sonido con 3–5 reels finales aprobados por la persona. Guárdalo en `4_Recursos/oido/perfil.json` y súbelo junto con cada mezcla para `revisar`. **No uses el perfil por defecto de Earshot**: son lanzamientos de producto, no reels de la persona |

**Cómo leerlo y cómo informarlo:**
- `verdict strong` / `z ≥ 3` = coincide claramente con la descripción. Por debajo de `plausible` (z < 2,5), desconfía.
- `sounds_most_like` usa un vocabulario de sonidos de producto y de cine: los sonidos bíblicos salen con nombres raros (al shofar lo llama "cow mooing" aunque lo da por bueno como shofar). Mira el `z` contra tu descripción, no ese nombre.
- Sincronía: si un efecto cae a más de 40 ms de su marca, revisa la marca de Whisper (`reels-animados.md` §9.1) antes de mover el sonido.
- A la persona dile qué oyó Earshot y en qué segundos tiene que escuchar él: "Earshot oye el whoosh de 0:12,4 como el acento más fuerte (+32 dB sobre la cama): escúchalo; puede estar alto". Nunca "suena bien".
- Earshot también **fabrica** sonidos con código (`earshot make`). Úsalo solo si lo piden: las grabaciones reales suenan mejor.

## 3. Afinar sonidos con tono (`afinar_sfx.py`)

`python3 afinar_sfx.py SONIDO --musica MUSICA.wav --en 12.4 [--salida afinado.wav]`

- Mide las notas del sonido y las que la música tiene en ese segundo. Si desafina, lo corre hasta ±2 semitonos (más los cents que lo dejan justo) para caer en una nota del acorde. Cambia también un poco el largo, como un sampler.
- Los ruidos (papel, whoosh, viento, golpes) no tienen tono: el script los deja como están.
- Úsalo con campanas, arpa, shofar, pops tonales y chimes encima de música o pads. **No** para "variar" un sonido repetido.
- Probado: una campana en Do# sobre un acorde de Do mayor → baja a Do; una en Sol → la deja igual; una página de Biblia → "sin tono, no se afina".
