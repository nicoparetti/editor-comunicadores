#!/usr/bin/env python3
"""Voz sintética para un reel animado, SOLO si la persona la pide.
Recomendación de siempre: grabar con voz humana (la propia). Esto es el recurso para quien no puede o no quiere grabar.

Motor: Kokoro v1.0 (modelo abierto, licencia Apache 2.0; kokoro-onnx, MIT). Funciona sin conexión una vez instalado.
Corre en el ESPACIO EN LA NUBE (el modelo pesa ~350 MB y se baja de GitHub); se reinstala solo en cada sesión (~1 min).
Voces en español: ef_dora (mujer), em_alex (hombre), em_santa (hombre, más grave). Acento latinoamericano por defecto (es-419).

Uso:
  python3 voz_sintetica.py instalar
  python3 voz_sintetica.py muestras                      las 3 voces leyendo la misma frase → muestras_voz/ (para elegir)
  python3 voz_sintetica.py guion.txt --voz em_alex [--velocidad 0.95] [--salida voz.wav] [--acento es|es-419]
guion.txt: el texto tal cual se dice; cada línea vacía separa frases (entre frases deja --pausa segundos, 0,45 por defecto).
Salida: WAV 48 kHz mono + voz_frases.json (inicio y fin de cada frase). Después sigue el flujo normal: transcribir.py para las
marcas por palabra y pausas_ia.py para el aire, como con cualquier voz con IA.
Consejos: números y siglas escritos como se dicen ("mil setecientos treinta y dos"); nombres raros, con la ortografía que suena
bien; si un nombre bíblico sale mal, escríbelo como se pronuncia (y corrígelo en los subtítulos).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

DIR = Path(os.environ.get("VOZ_DIR", Path.home() / ".voz"))
VENV = DIR / "venv"
MODELO = DIR / "kokoro-v1.0.onnx"
VOCES = DIR / "voices-v1.0.bin"
URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
FRASE = ("En mil setecientos treinta y dos, dos jóvenes se vendieron como esclavos para llegar a una isla del Caribe. "
         "No iban a ganar nada. Iban porque Dios los había llamado.")


def instalar():
    DIR.mkdir(parents=True, exist_ok=True)
    py = VENV / "bin/python"
    if not py.exists():
        subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True)
    r = subprocess.run([str(py), "-c", "import kokoro_onnx, soundfile"], capture_output=True)
    if r.returncode:
        subprocess.run([str(VENV / "bin/pip"), "install", "-q", "kokoro-onnx", "soundfile"], check=True)
    for f in (MODELO, VOCES):
        if not f.exists() or f.stat().st_size < 1_000_000:
            print(f"bajando {f.name}…")
            subprocess.run(["curl", "-sSfL", "--retry", "3", "-o", str(f), URL + f.name], check=True)
    print("Voz sintética lista.")
    return py


def sintetizar(frases, voz, velocidad, acento, pausa, salida):
    py = instalar()
    codigo = r'''
import json, sys, numpy as np, soundfile as sf, subprocess
from kokoro_onnx import Kokoro
a = json.loads(sys.argv[1])
k = Kokoro(a["modelo"], a["voces"])
partes, marcas, t = [], [], 0.0
sil = None
for i, f in enumerate(a["frases"]):
    x, sr = k.create(f, voice=a["voz"], speed=a["vel"], lang=a["acento"])
    if sil is None: sil = np.zeros(int(sr * a["pausa"]), np.float32)
    marcas.append({"frase": i + 1, "texto": f, "inicio": round(t, 3), "fin": round(t + len(x) / sr, 3)})
    partes += [x.astype(np.float32), sil]; t += len(x) / sr + a["pausa"]
y = np.concatenate(partes[:-1]) if partes else np.zeros(1, np.float32)
tmp = a["salida"] + ".24k.wav"; sf.write(tmp, y, sr)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-ar", "48000", "-ac", "1", "-c:a", "pcm_s24le", a["salida"]], check=True)
import os; os.remove(tmp)
json.dump(marcas, open(a["salida"].rsplit(".", 1)[0] + "_frases.json", "w"), ensure_ascii=False, indent=1)
print(f"{a['salida']}: {t - a['pausa']:.1f} s, {len(marcas)} frases")
'''
    args = {"modelo": str(MODELO), "voces": str(VOCES), "frases": frases, "voz": voz, "vel": velocidad,
            "acento": acento, "pausa": pausa, "salida": str(salida)}
    subprocess.run([str(py), "-c", codigo, json.dumps(args, ensure_ascii=False)], check=True)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    if a[0] == "instalar":
        instalar(); return

    def opt(nombre, defecto):
        return a[a.index(nombre) + 1] if nombre in a else defecto
    voz, vel = opt("--voz", "em_alex"), float(opt("--velocidad", "0.95"))
    acento, pausa = opt("--acento", "es-419"), float(opt("--pausa", "0.45"))
    if a[0] == "muestras":
        d = Path("muestras_voz"); d.mkdir(exist_ok=True)
        for v in ("ef_dora", "em_alex", "em_santa"):
            sintetizar([FRASE], v, vel, acento, pausa, d / f"{v}.wav")
        return
    texto = Path(a[0]).read_text(encoding="utf-8")
    frases = [" ".join(b.split()) for b in texto.split("\n\n") if b.strip()]
    if len(frases) == 1:
        frases = [l.strip() for l in texto.splitlines() if l.strip()]
    sintetizar(frases, voz, vel, acento, pausa, Path(opt("--salida", "voz_sintetica.wav")))


if __name__ == "__main__":
    main()
