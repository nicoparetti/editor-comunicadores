#!/usr/bin/env python3
"""¿Un sonido con tono (campana, arpa, pop, shofar, chime) cae en la tonalidad de la música que suena debajo?
Si desafina, lo corre hasta ±2 semitonos (más los cents que lo dejan justo en la nota) para que caiga en una nota
del acorde. Los ruidos (whoosh, papel, viento, golpes) no tienen tono y se dejan como están.

Idea tomada de Real SFX (Clipwing, github.com/Clipwing/skills, MIT), reescrita para editor-gente-comun.
OJO: esto es para que un sonido no desafine con la música. NO sirve para variar un sonido repetido: La persona descartó
el mismo tap en otra nota ("es prácticamente lo mismo que el original").

Uso:
  python3 afinar_sfx.py SONIDO --musica MUSICA.wav --en 12.4                  dice qué notas tiene y si conviene afinar
  python3 afinar_sfx.py SONIDO --musica MUSICA.wav --en 12.4 --salida s.wav   además escribe la versión afinada
--en = segundo de la música en que entra el sonido. Necesita ffmpeg y numpy.
"""
import argparse
import subprocess
import sys

import numpy as np

SR = 48000
NOTAS = ["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"]


def leer(ruta, t0=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-ss", str(t0), "-i", str(ruta)]
    if dur:
        cmd += ["-t", str(dur)]
    cmd += ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32)


def midi(f):
    return 69 + 12 * np.log2(f / 440.0)


def nombre(m):
    k = int(round(m))
    return f"{NOTAS[k % 12]}{k // 12 - 1}"


def parciales(x, maximo=3):
    """Picos del espectro en los 0,5 s más fuertes del sonido (80–3000 Hz, 12 dB sobre la mediana)."""
    n = int(0.5 * SR)
    if len(x) > n:
        e = np.convolve(x ** 2, np.ones(n), mode="valid")
        i = int(np.argmax(e))
        x = x[i:i + n]
    N = 16384
    seg = np.pad(x, (0, max(0, N - len(x))))[:N] * np.hanning(N)
    mag = np.abs(np.fft.rfft(seg))
    fr = np.fft.rfftfreq(N, 1 / SR)
    banda = (fr >= 80) & (fr <= 3000)
    db = 20 * np.log10(mag + 1e-12)
    med = np.median(db[banda])
    # planitud espectral: ruido ≈ 1, tono ≈ 0
    plan = float(np.exp(np.mean(np.log(mag[banda] + 1e-12))) / (np.mean(mag[banda]) + 1e-12))
    picos = []
    idx = np.nonzero(banda)[0]
    for i in idx[1:-1]:
        if db[i] > db[i - 1] and db[i] >= db[i + 1] and db[i] > med + 12:
            a, b, c = db[i - 1], db[i], db[i + 1]  # interpolación parabólica del pico
            d = 0.5 * (a - c) / (a - 2 * b + c + 1e-12)
            picos.append((float(b), float((i + d) * SR / N)))
    picos.sort(reverse=True)
    elegidos = []
    for nivel, f in picos:
        if elegidos and nivel < elegidos[0][0] - 20:  # más de 20 dB abajo del principal: eco del análisis, no una nota
            break
        if all(abs(midi(f) - midi(g)) > 0.7 for _, g in elegidos):
            elegidos.append((nivel, f))
        if len(elegidos) >= maximo:
            break
    return [(midi(f), 10 ** ((nivel - elegidos[0][0]) / 20)) for nivel, f in elegidos], plan


def croma(x):
    """Energía por nota (12 clases) de la música, 80–2000 Hz."""
    N = 8192
    ch = np.zeros(12)
    fr = np.fft.rfftfreq(N, 1 / SR)
    sel = (fr >= 80) & (fr <= 2000)
    clases = np.round(midi(fr[sel])).astype(int) % 12
    for i in range(0, max(1, len(x) - N), N // 2):
        mag = np.abs(np.fft.rfft(np.pad(x[i:i + N], (0, max(0, N - len(x[i:i + N])))) * np.hanning(N)))[sel] ** 2
        np.add.at(ch, clases, mag)
    return ch / (ch.max() + 1e-12)


def puntaje(pars, ch, corr):
    s = 0.0
    for m, w in pars:
        pc = int(round(m + corr)) % 12
        s += w * (ch[pc] - 0.8 * max(ch[(pc + 1) % 12], ch[(pc - 1) % 12]))
    return s


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sonido")
    ap.add_argument("--musica", required=True)
    ap.add_argument("--en", type=float, required=True, help="segundo de la música en que entra el sonido")
    ap.add_argument("--max", type=float, default=2, help="semitonos enteros como máximo (por defecto 2)")
    ap.add_argument("--salida")
    a = ap.parse_args()

    pars, plan = parciales(leer(a.sonido))
    if not pars or plan > 0.35:
        print(f"{a.sonido}: sin tono claro (ruido, planitud {plan:.2f}): no se afina.")
        return
    ch = croma(leer(a.musica, a.en, 0.9))
    if ch.sum() < 1e-6:
        print("La música está en silencio en ese momento: no hay con qué afinar.")
        return
    tonica = pars[0][0]
    cents = round(tonica) - tonica  # lo que falta para caer justo en la nota más cercana
    print(f"Sonido: {', '.join(nombre(m) for m, _ in pars)} (nota principal {nombre(tonica)}, {(-cents) * 100:+.0f} cents)")
    fuertes = [NOTAS[i] for i in np.argsort(ch)[::-1][:4] if ch[i] > 0.35]
    print(f"Música en {a.en:.2f} s: {', '.join(fuertes)}")
    base = puntaje(pars, ch, cents)
    mejor = (base, 0)
    for k in range(-int(a.max), int(a.max) + 1):
        if k == 0:
            continue
        p = puntaje(pars, ch, k + cents) - 0.03 * abs(k)
        if p > mejor[0] + 0.1:
            mejor = (p, k)
    total = mejor[1] + cents
    if abs(total) < 0.15:
        print("Ya cae en la tonalidad: no hace falta afinar.")
        return
    if mejor[1] == 0:
        print(f"La nota ya es del acorde; solo le faltan {total * 100:+.0f} cents para quedar justo.")
    else:
        print(f"Conviene correrlo {total:+.2f} semitonos → {nombre(tonica + total)} (puntaje {base:.2f} → {mejor[0]:.2f}).")
    if a.salida:
        r = 2 ** (total / 12)
        subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-i", a.sonido, "-af",
                        f"aresample={SR},asetrate={SR * r:.3f},aresample={SR}", "-c:a", "pcm_s24le", a.salida], check=True)
        print(f"Escrito {a.salida} (cambia también el largo en ×{1 / r:.3f}, como un sampler)")


if __name__ == "__main__":
    sys.exit(main())
