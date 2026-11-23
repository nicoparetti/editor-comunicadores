#!/usr/bin/env python3
"""Busca sonidos REALES con licencia abierta en Openverse (Freesound y otros), los baja, los prepara y deja una hoja
para que la persona los escuche y los puntúe de 1 a 5 estrellas antes de sumarlos al banco.

Uso (desde la raíz de la carpeta de trabajo, con entorno.sh cargado):
  python3 .herramientas/scripts/buscar_sfx.py --temas                         lista de temas bíblicos preparados
  python3 .herramientas/scripts/buscar_sfx.py --tema pagina_biblia            un tema de sonidos_biblicos.json
  python3 .herramientas/scripts/buscar_sfx.py "wooden door creak" --max 4     búsqueda libre (en inglés rinde más)
  python3 .herramientas/scripts/buscar_sfx.py --todos                         todos los temas que falten (reanudable: SIGUE)
  python3 .herramientas/scripts/buscar_sfx.py "cool jazz" --musica --licencia cc0,by   música real (≥ 15 s, hasta 180 s)
Opciones: --n 8 (candidatos), --min 0.15 / --max 6 (segundos), --licencia cc0 | cc0,by, --salida CARPETA,
          --oir (ordena los candidatos con el oído de Earshot si está instalado), --forzar (rehace un tema ya bajado).

Salida en 4_Recursos/sfx_openverse/<tema>/:
  <tema>_NN_<lic>.wav   el sonido: silencio inicial recortado, cola cortada con fundido, pico a -3 dBFS, 48 kHz estéreo
  escuchar.mp3          todos seguidos con 1 s de silencio entre uno y otro (el orden de la hoja)
  hoja.png              por candidato: número, título, autor, licencia, segundo en escuchar.mp3, forma de onda y espectrograma
  fuentes.json          todo lo que hace falta para citar y volver a bajar cada sonido
  CREDITOS.md           texto de atribución listo para pegar en la descripción (obligatorio con CC BY)
Licencias: solo CC0 y dominio público (pdm) por defecto; con --licencia cc0,by también CC BY (exige crédito).
Nunca baja NC (no comercial) ni ND (sin derivados).
Necesita curl, ffmpeg, numpy y PIL. La red pasa por curl (respeta el proxy).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.parse
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
API = "https://api.openverse.org/v1/audio/"
SR = 48000
PICO_DB = -3.0
LIMITE_S = 160  # presupuesto por llamada de shell (≤ 180 s)
LIC_TXT = {"cc0": "CC0 1.0 (dominio público)", "pdm": "Marca de dominio público", "by": "CC BY"}


def raiz():
    return Path(os.environ.get("EDITOR_RAIZ") or os.getcwd())


def slug(s, n=40):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower()
    return s[:n] or "sonido"


def curl(url, salida=None, tiempo=40):
    cmd = ["curl", "-sSfL", "--max-time", str(tiempo), "--retry", "3", "--retry-delay", "8", "--retry-max-time", "60",
           "-A", "editor-gente-comun/1.1 (banco de sonidos personal)"]
    if os.environ.get("OPENVERSE_TOKEN") and url.startswith(API):
        cmd += ["-H", "Authorization: Bearer " + os.environ["OPENVERSE_TOKEN"]]
    if salida:
        cmd += ["-o", str(salida)]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl {r.returncode}: {r.stderr.decode(errors='ignore').strip()[:200]}")
    return r.stdout


def buscar(q, licencias, dmin, dmax, n, musica=False):
    """Devuelve candidatos útiles en orden de relevancia de Openverse."""
    vistos, out = set(), []
    for pagina in (1, 2, 3):
        params = {"q": q, "license": ",".join(licencias), "page_size": 20, "page": pagina, "mature": "false"}
        try:
            datos = json.loads(curl(API + "?" + urllib.parse.urlencode(params)))
        except RuntimeError as e:
            if pagina == 1:
                raise
            print(f"  aviso: página {pagina} no respondió ({e})")
            break
        for r in datos.get("results", []):
            lic = (r.get("license") or "").lower()
            if lic not in licencias or r.get("mature"):
                continue
            if re.match(r"^LL-Q\d+", r.get("title") or ""):  # Lingua Libre: pronunciación de una palabra, no el sonido
                continue
            dur = (r.get("duration") or 0) / 1000
            if dur and dur < dmin:
                continue
            if dur and dur > max(dmax * 4, dmax + 6):  # muy largo: sería recortar un pedacito al azar
                continue
            clave = (r.get("creator", "").lower(), slug(r.get("title", ""), 24))
            if clave in vistos or not r.get("url"):
                continue
            vistos.add(clave)
            out.append(r)
            if len(out) >= n * 2:  # margen por si alguno falla al bajar o queda en silencio
                return out
        if pagina >= datos.get("page_count", 1):
            break
        time.sleep(1.5)  # Openverse limita las consultas sin cuenta
    return out


def decodificar(ruta):
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-i", str(ruta), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32)
    return x.reshape(-1, 2).copy()


def preparar(x, dmax):
    """Recorta el silencio inicial (umbral relativo al pico), corta la cola en dmax con fundido y lleva el pico a -3 dBFS."""
    mono = np.abs(x).max(axis=1)
    pico = float(mono.max()) if len(mono) else 0.0
    if pico < 1e-4:
        return None
    umbral = pico * 10 ** (-40 / 20)
    sobre = np.nonzero(mono > umbral)[0]
    ini = max(0, int(sobre[0]) - int(0.005 * SR))
    fin = min(len(x), int(sobre[-1]) + int(0.05 * SR))
    x = x[ini:fin]
    if len(x) > dmax * SR:
        x = x[: int(dmax * SR)]
        f = int(0.08 * SR)
        x[-f:] *= np.linspace(1, 0, f)[:, None]
    else:
        f = min(int(0.01 * SR), len(x) // 4)
        if f > 0:
            x[-f:] *= np.linspace(1, 0, f)[:, None]
    a = min(int(0.002 * SR), len(x) // 4)
    if a > 0:
        x[:a] *= np.linspace(0, 1, a)[:, None]
    x *= 10 ** (PICO_DB / 20) / (np.abs(x).max() + 1e-9)
    return x


def medir(x):
    """Palabras simples para leer el sonido sin oírlo (las mismas ideas que el banco: clic definido, grave, brillante)."""
    m = x.mean(axis=1)
    dur = len(m) / SR
    env = np.sqrt(np.convolve(m ** 2, np.ones(int(0.005 * SR)) / int(0.005 * SR), mode="same"))
    # ataque = tiempo hasta que la envolvente llega a la mitad de su máximo (el primer golpe, no el más fuerte)
    ataque = float(np.argmax(env >= env.max() * 0.5) / SR)
    seg = m[: min(len(m), SR)]
    esp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) if len(seg) > 64 else np.zeros(2)
    fr = np.fft.rfftfreq(len(seg), 1 / SR) if len(seg) > 64 else np.zeros(2)
    centro = float((fr * esp).sum() / (esp.sum() + 1e-9))
    graves = float(esp[fr < 200].sum() / (esp.sum() + 1e-9))
    rms = 20 * np.log10(np.sqrt((m ** 2).mean()) + 1e-9)
    pal = []
    pal.append("golpe seco" if ataque < 0.03 and dur < 0.6 else "ataque rápido" if ataque < 0.06 else "entra de a poco")
    pal.append("brillante" if centro > 4000 else "medio" if centro > 1500 else "oscuro")
    if graves > 0.35:
        pal.append("con peso grave")
    pal.append("cama larga" if dur > 6 else "corto" if dur < 0.8 else "mediano")
    return {"dur": round(dur, 2), "ataque_s": round(ataque, 3), "centro_hz": int(centro),
            "graves": round(graves, 2), "rms_db": round(float(rms), 1), "palabras": ", ".join(pal)}


def guardar_wav(x, ruta):
    p = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                        "-c:a", "pcm_s24le", str(ruta)], input=x.astype(np.float32).tobytes(), capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors="ignore")[:200])


def escuchar_mp3(archivos, ruta):
    """Todos seguidos con 1 s de silencio; devuelve el segundo en que empieza cada uno."""
    partes, inicios, t = [], [], 0.0
    sil = np.zeros((SR, 2), np.float32)
    for a in archivos:
        x = decodificar(a)
        inicios.append(round(t, 1))
        partes += [x, sil]
        t += len(x) / SR + 1.0
    todo = np.concatenate(partes) if partes else sil
    subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-c:a", "libmp3lame", "-b:a", "192k", str(ruta)], input=todo.tobytes(), check=True)
    return inicios


def fuente(tam):
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf"):
        if Path(f).exists():
            from PIL import ImageFont
            return ImageFont.truetype(f, tam)
    from PIL import ImageFont
    try:
        return ImageFont.load_default(size=tam)
    except TypeError:
        return ImageFont.load_default()


def dibujo_onda(m, w, h):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (w, h), (24, 24, 28))
    d = ImageDraw.Draw(im)
    if len(m) == 0:
        return im
    cols = np.array_split(np.abs(m), w)
    for i, c in enumerate(cols):
        v = float(c.max()) if len(c) else 0.0
        y = int(v / 0.75 * (h / 2 - 2))
        d.line([(i, h // 2 - y), (i, h // 2 + y)], fill=(255, 140, 40))
    return im


def dibujo_espectro(m, w, h):
    from PIL import Image
    nfft, hop = 1024, max(64, len(m) // w)
    if len(m) < nfft:
        m = np.pad(m, (0, nfft - len(m)))
    idx = range(0, len(m) - nfft + 1, hop)
    win = np.hanning(nfft)
    S = np.array([np.abs(np.fft.rfft(m[i:i + nfft] * win)) for i in idx]).T  # frec x tiempo
    fr = np.fft.rfftfreq(nfft, 1 / SR)
    # eje de frecuencia logarítmico 40 Hz – 20 kHz
    bordes = np.geomspace(40, 20000, h + 1)
    filas = []
    for a, b in zip(bordes[:-1], bordes[1:]):
        sel = (fr >= a) & (fr < b)
        filas.append(S[sel].max(axis=0) if sel.any() else S[np.argmin(np.abs(fr - a))])
    L = 20 * np.log10(np.array(filas[::-1]) + 1e-9)
    L = np.clip((L - (L.max() - 70)) / 70, 0, 1)
    rgb = np.stack([L ** 0.7 * 255, L ** 1.6 * 200, L ** 3 * 120], -1).astype(np.uint8)
    return Image.fromarray(rgb).resize((w, h))


def hoja(items, ruta, titulo):
    from PIL import Image, ImageDraw
    W, H, TX, WV = 1700, 150, 520, 580
    im = Image.new("RGB", (W, 70 + H * len(items)), (14, 14, 16))
    d = ImageDraw.Draw(im)
    d.text((20, 18), titulo, fill=(255, 255, 255), font=fuente(26))
    f1, f2 = fuente(20), fuente(16)
    for k, it in enumerate(items):
        y = 70 + k * H
        d.rectangle([0, y, W, y + H - 6], fill=(22, 22, 26))
        m = decodificar(it["ruta"]).mean(axis=1)
        im.paste(dibujo_onda(m, WV, H - 16), (TX, y + 5))
        im.paste(dibujo_espectro(m, W - TX - WV - 30, H - 16), (TX + WV + 10, y + 5))
        lic = it["licencia"].upper() + (" · pide crédito" if it["licencia"] == "by" else "")
        d.text((16, y + 8), f"{it['n']:02d}", fill=(255, 140, 40), font=fuente(34))
        d.text((80, y + 10), it["titulo"][:38], fill=(255, 255, 255), font=f1)
        d.text((80, y + 40), f"de {it['autor'][:30]} · {lic}", fill=(180, 180, 190), font=f2)
        d.text((80, y + 64), f"{it['medida']['dur']} s · {it['medida']['palabras']}", fill=(180, 180, 190), font=f2)
        d.text((80, y + 88), f"en escuchar.mp3: {int(it['en_escuchar'] // 60)}:{it['en_escuchar'] % 60:04.1f}",
               fill=(120, 200, 255), font=f2)
        if it.get("oido") is not None:
            col = (140, 220, 140) if it.get("oido_veredicto") == "coincide" else (230, 120, 110)
            d.text((80, y + 112), f"oído: {it['oido_veredicto']} (z {it['oido']:+.1f}) · parece {it['oido_parece'][:28]}",
                   fill=col, font=f2)
    im.save(ruta)


def earshot_bin():
    for c in (os.environ.get("EARSHOT_BIN"), str(Path.home() / ".oido/venv/bin/earshot"), shutil.which("earshot")):
        if c and Path(c).exists():
            return c
    return None


def oir(items, q):
    """Con el oído de Earshot (oido.sh, en el espacio en la nube): cuánto se parece cada sonido a la descripción.
    z ≥ ~3 = coincide claramente; veredicto strong / plausible / weak / no match. Ordena del más parecido al menos."""
    eb = earshot_bin()
    if not eb:
        print("  --oir: el oído no está instalado (bash oido.sh instalar, en el espacio en la nube); sigo sin él")
        return items
    r = subprocess.run([eb, "rank", q, *[str(i["ruta"]) for i in items], "--json"], capture_output=True, text=True,
                       timeout=900)
    try:
        datos = json.loads(r.stdout)
        por_ruta = {Path(f["path"]).name: f for f in datos.get("results", [])}
        for i in items:
            f = por_ruta.get(Path(i["ruta"]).name)
            if f:
                i["oido"] = float(f.get("z", 0))
                i["oido_veredicto"] = {"strong": "coincide", "plausible": "posible", "weak": "dudoso",
                                       "no match": "no coincide"}.get(f.get("verdict"), f.get("verdict"))
                i["oido_parece"] = f.get("sounds_most_like", "")
            else:
                i["oido"] = None
        items.sort(key=lambda i: -(i["oido"] if i.get("oido") is not None else -9))
    except Exception as e:  # nunca frenar la búsqueda por el oído
        print(f"  --oir: no pude leer la respuesta de Earshot ({e}); {r.stderr[-300:]}")
    return items


def un_tema(nombre, q, dmin, dmax, n, licencias, salida, usar_oido, forzar, musica=False):
    if (salida / "fuentes.json").exists() and not forzar:
        print(f"= {nombre}: ya estaba ({salida}); --forzar para rehacerlo")
        return True
    print(f"> {nombre}: buscando \"{q}\" ({'/'.join(licencias)}, {dmin}–{dmax} s)")
    cands = buscar(q, licencias, dmin, dmax, n, musica)
    if not cands:
        print(f"  sin resultados para \"{q}\": prueba otras palabras en inglés")
        return True
    salida.mkdir(parents=True, exist_ok=True)
    items, tmp = [], Path(tempfile.mkdtemp(prefix="sfx_"))
    for r in cands:
        if len(items) >= n:
            break
        try:
            bruto = tmp / f"b{len(items)}.{r.get('filetype') or 'mp3'}"
            curl(r["url"], bruto, tiempo=150 if musica else 40)
            x = preparar(decodificar(bruto), dmax)
            if x is None or len(x) < dmin * SR:
                continue
            lic = r["license"].lower()
            ruta = salida / f"{slug(nombre, 24)}_{len(items) + 1:02d}_{lic}.wav"
            guardar_wav(x, ruta)
            items.append({"n": len(items) + 1, "ruta": ruta, "archivo": ruta.name, "titulo": r.get("title") or "",
                          "autor": r.get("creator") or "", "autor_url": r.get("creator_url") or "",
                          "licencia": lic, "licencia_version": r.get("license_version") or "",
                          "licencia_url": r.get("license_url") or "", "pagina": r.get("foreign_landing_url") or "",
                          "origen": r.get("source") or r.get("provider") or "", "descarga": r["url"],
                          "atribucion": r.get("attribution") or "", "openverse_id": r.get("id"),
                          "medida": medir(x)})
        except Exception as e:
            print(f"  salteo \"{(r.get('title') or '')[:40]}\": {e}")
    shutil.rmtree(tmp, ignore_errors=True)
    if len(items) < max(3, n // 2) and "by" not in licencias:
        print(f"  solo {len(items)} en CC0: prueba con --licencia cc0,by (CC BY pide crédito) u otras palabras")
    if not items:
        print("  ningún candidato sirvió (silencio o fallas de descarga)")
        return True
    if usar_oido:
        items = oir(items, q)
        for k, it in enumerate(items, 1):  # renumerar según el oído
            nuevo = salida / f"{slug(nombre, 24)}_{k:02d}_{it['licencia']}.wav"
            if nuevo != it["ruta"]:
                it["ruta"].rename(salida / ("_tmp_" + nuevo.name))
                it["ruta"] = salida / ("_tmp_" + nuevo.name)
            it["n"] = k
        for it in items:
            if it["ruta"].name.startswith("_tmp_"):
                fin = salida / it["ruta"].name[5:]
                it["ruta"].rename(fin)
                it["ruta"], it["archivo"] = fin, fin.name
    inicios = escuchar_mp3([i["ruta"] for i in items], salida / "escuchar.mp3")
    for it, t in zip(items, inicios):
        it["en_escuchar"] = t
    hoja(items, salida / "hoja.png", f"{nombre} · \"{q}\" · {len(items)} candidatos · Openverse")
    for it in items:
        it["ruta"] = str(it["ruta"].relative_to(raiz())) if str(it["ruta"]).startswith(str(raiz())) else str(it["ruta"])
    (salida / "fuentes.json").write_text(json.dumps({"tema": nombre, "busqueda": q, "fecha": time.strftime("%Y-%m-%d"),
                                                     "sonidos": items}, ensure_ascii=False, indent=1))
    lineas = [f"# Créditos · {nombre}", "",
              "CC0 y dominio público no exigen crédito (se agradece igual). CC BY lo exige: si usas uno, pega su línea en la descripción.", ""]
    for it in items:
        lic = LIC_TXT.get(it["licencia"], it["licencia"].upper()) + (f" {it['licencia_version']}" if it["licencia"] == "by" else "")
        lineas.append(f"- `{it['archivo']}`: «{it['titulo']}», {it['autor']}, {lic}, {it['pagina']}")
    (salida / "CREDITOS.md").write_text("\n".join(lineas) + "\n")
    print(f"  listo: {len(items)} sonidos en {salida} → hoja.png, escuchar.mp3, CREDITOS.md")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("busqueda", nargs="?", help="palabras de búsqueda libre (mejor en inglés)")
    ap.add_argument("--tema", help="un tema de sonidos_biblicos.json")
    ap.add_argument("--temas", action="store_true", help="lista los temas preparados")
    ap.add_argument("--todos", action="store_true", help="baja todos los temas que falten (reanudable)")
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--min", type=float, default=0.15)
    ap.add_argument("--max", type=float, default=None)
    ap.add_argument("--licencia", default="cc0", help="cc0 (incluye dominio público) o cc0,by")
    ap.add_argument("--salida", help="carpeta de salida (por defecto 4_Recursos/sfx_openverse/<tema>)")
    ap.add_argument("--oir", action="store_true", help="ordena con el oído de Earshot (si está instalado)")
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--musica", action="store_true", help="busca música (no efectos): hasta 180 s, en sfx_openverse/musica_<busqueda>")
    a = ap.parse_args()

    temas = json.loads((AQUI / "sonidos_biblicos.json").read_text())
    temas.pop("_nota", None)
    if a.temas:
        for k, v in temas.items():
            hecho = "✓" if (raiz() / "4_Recursos/sfx_openverse" / k / "fuentes.json").exists() else " "
            print(f"{hecho} {k:16s} \"{v['q']}\" ≤{v['max']} s · {v['momento']}")
        return
    licencias = []
    for l in a.licencia.lower().replace(" ", "").split(","):
        if l in ("cc0", "pdm"):
            licencias += ["cc0", "pdm"]
        elif l == "by":
            licencias.append("by")
        else:
            sys.exit(f"Licencia no permitida: {l}. Solo cc0 y by (nunca NC ni ND).")
    licencias = sorted(set(licencias))
    base = raiz() / "4_Recursos" / "sfx_openverse"

    if a.todos:
        t0 = time.time()
        for k, v in temas.items():
            if (base / k / "fuentes.json").exists() and not a.forzar:
                continue
            if time.time() - t0 > LIMITE_S - 25:
                print("SIGUE: faltan temas; vuelve a correr el mismo comando")
                return
            un_tema(k, v["q"], a.min, a.max or v["max"], a.n, licencias, base / k, a.oir, a.forzar)
            time.sleep(3)
        print("Todos los temas listos.")
        return
    if a.tema:
        if a.tema not in temas:
            sys.exit(f"No conozco el tema '{a.tema}'. Mira --temas o usa una búsqueda libre.")
        v = temas[a.tema]
        q, nombre, dmax = a.busqueda or v["q"], a.tema, a.max or v["max"]
    elif a.busqueda:
        q, nombre = a.busqueda, ("musica_" if a.musica else "") + slug(a.busqueda, 30)
        dmax = a.max or (180 if a.musica else 6)
    else:
        ap.error("falta una búsqueda, --tema, --temas o --todos")
    salida = Path(a.salida) if a.salida else base / nombre
    un_tema(nombre, q, a.min if not a.musica else max(a.min, 15), dmax, a.n, licencias, salida, a.oir, a.forzar, a.musica)


if __name__ == "__main__":
    main()
