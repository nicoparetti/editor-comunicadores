#!/usr/bin/env python3
"""Cama musical hecha con código para los estilos precargados de reels animados. Es un RECURSO, no el sonido por defecto:
la cama por defecto sigue siendo el pad grave bajo la voz (reels-animados.md §6). Se ofrece cuando el estilo elegido lo pide y la
persona la quiere; si tiene su propia música, manda la suya. Para música grabada real: buscar_sfx.py "…" --musica
(la caricatura de los 50 pide jazz real: un jazz hecho con código sonó a "chiptune triste" en la prueba y se descartó).

Uso:
  python3 musica_estilo.py chip      --dur 62 [--tempo 112] [--tono C] [--salida musica.wav]   RPG de 16 bits
  python3 musica_estilo.py campanas  --dur 62 [--tempo 88]  [--tono D]                          isla isométrica, diorama de pixeles
  python3 musica_estilo.py cosmos    --dur 62 [--tono A]                                         escala sin fin
Siempre termina con un acorde y un fundido de 2 s. Salida: WAV 48 kHz estéreo, pico −6 dBFS, para mezclarla ≈ 18–22 dB por
debajo de la voz (la voz manda). Solo numpy y ffmpeg. Determinista (misma entrada → mismo archivo).
"""
import argparse
import subprocess

import numpy as np

SR = 48000
NOTAS = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
         "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
rng = np.random.default_rng(7)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env(n, a=0.005, d=0.1, s=0.6, r=0.1):
    """Envolvente ADSR de n muestras."""
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    e = np.full(n, s, np.float32)
    a = min(a, n); e[:a] = np.linspace(0, 1, a)
    d2 = min(d, max(0, n - a)); e[a:a + d2] = np.linspace(1, s, d2)
    r2 = min(r, n); e[n - r2:] *= np.linspace(1, 0, r2)
    return e


def t_(n):
    return np.arange(n) / SR


def pulso(f, n, duty=0.25):
    ph = (t_(n) * f) % 1.0
    return np.where(ph < duty, 1.0, -1.0).astype(np.float32)


def triang(f, n):
    ph = (t_(n) * f) % 1.0
    return (4 * np.abs(ph - 0.5) - 1).astype(np.float32)


def fm(f, n, ratio=3.5, indice=2.0, caida=4.0):
    """Campana / marimba FM con caída exponencial."""
    t = t_(n)
    i = indice * np.exp(-t * caida * 1.5)
    return (np.sin(2 * np.pi * f * t + i * np.sin(2 * np.pi * f * ratio * t)) * np.exp(-t * caida)).astype(np.float32)


def suave(x, corte=0.15):
    """Pasa bajos de un polo (corte 0–1)."""
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += corte * (v - acc); y[i] = acc
    return y


def lp(x, hzc):
    """Pasa bajos rápido en frecuencia (FFT)."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / hzc) ** 4)
    return np.fft.irfft(X, len(x)).astype(np.float32)


def poner(buf, x, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    x = x[: len(buf) - i] * g
    buf[i:i + len(x), 0] += x * (1 - max(0, pan))
    buf[i:i + len(x), 1] += x * (1 + min(0, pan))


def eco(buf, seg=0.33, fb=0.3, mezcla=0.25):
    d = int(seg * SR); y = buf.copy()
    for k in range(1, 4):
        y[d * k:] += buf[:-d * k] * (mezcla * fb ** (k - 1)) if d * k < len(buf) else 0
    return y


def acordes(base, grados, mayor=True):
    esc = [0, 2, 4, 5, 7, 9, 11] if mayor else [0, 2, 3, 5, 7, 8, 10]
    out = []
    for g in grados:
        tri = [esc[(g + k) % 7] + 12 * ((g + k) // 7) for k in (0, 2, 4)]
        out.append([base + x for x in tri])
    return out


def chip(dur, tempo, tono):
    b = 60 + NOTAS[tono]; neg = 60 / tempo; sem = neg / 4
    prog = acordes(b, [0, 4, 5, 3])  # I V vi IV
    buf = np.zeros((int((dur + 3) * SR), 2), np.float32)
    patron = [0, 1, 2, 1, 0, 1, 2, 3]
    t, comp = 0.0, 0
    while t < dur:
        ac = prog[comp % 4]
        for k in range(16):  # semicorcheas del compás
            tt = t + k * sem
            if tt >= dur:
                break
            idx = patron[k % 8]
            m = (ac + [ac[0] + 12])[idx] + 12
            n = int(sem * SR * 0.9)
            poner(buf, pulso(hz(m), n, 0.25) * env(n, 0.002, 0.05, 0.5, 0.02), tt, 0.10, -0.2)
            if k % 4 == 0:  # bajo triangular en cada negra
                nb = int(neg * SR * 0.95)
                poner(buf, triang(hz(ac[0] - 24), nb) * env(nb, 0.003, 0.1, 0.8, 0.03), tt, 0.30)
            if k % 4 == 2:  # platillo de ruido en el contratiempo
                nh = int(0.04 * SR)
                poner(buf, rng.uniform(-1, 1, nh).astype(np.float32) * env(nh, 0.001, 0.03, 0.0, 0.005), tt, 0.05, 0.3)
        if comp % 2 == 1:  # melodía lenta de pulso ancho cada dos compases
            m = ac[2] + 24; n = int(neg * 2 * SR)
            poner(buf, pulso(hz(m), n, 0.5) * env(n, 0.01, 0.3, 0.4, 0.3), t + neg * 2, 0.06, 0.25)
        t += 4 * neg; comp += 1
    final(buf, dur, [hz(x + 12) for x in prog[0]], lambda f, n: pulso(f, n, 0.5), 0.05)
    buf = eco(buf, neg * 0.75, 0.35, 0.2)
    return np.stack([lp(buf[:, 0], 6000), lp(buf[:, 1], 6000)], 1)


def campanas(dur, tempo, tono):
    b = 60 + NOTAS[tono]; neg = 60 / tempo
    penta = [0, 2, 4, 7, 9]
    buf = np.zeros((int((dur + 4) * SR), 2), np.float32)
    prog = acordes(b, [0, 5, 3, 4])
    t, comp = 0.0, 0
    while t < dur:
        ac = prog[comp % 4]
        n = int(4 * neg * SR + 1.5 * SR)  # colchón: tres senos levemente desafinados
        pad = sum(np.sin(2 * np.pi * hz(m - 12) * (1 + d) * t_(n)) for m in ac for d in (-0.002, 0.002))
        poner(buf, pad.astype(np.float32) * env(n, 0.8, 0.5, 0.7, 1.2), t, 0.025)
        for k in range(8):  # corcheas, no todas suenan
            if rng.random() < 0.35:
                continue
            m = b + 12 + penta[int(rng.integers(0, 5))] + (12 if rng.random() < 0.3 else 0)
            nn = int(1.2 * SR)
            poner(buf, fm(hz(m), nn, ratio=4.0, indice=1.2, caida=5.0), t + k * neg / 2, 0.16,
                  float(rng.uniform(-0.5, 0.5)))
        nb = int(1.5 * SR)
        poner(buf, fm(hz(ac[0] - 12), nb, ratio=1.0, indice=0.8, caida=2.5), t, 0.25)
        t += 4 * neg; comp += 1
    final(buf, dur, [hz(x) for x in prog[0]], lambda f, n: fm(f, n, 4.0, 1.2, 1.2), 0.18)
    return eco(buf, neg * 0.5, 0.3, 0.18)


def cosmos(dur, tempo, tono):
    b = 48 + NOTAS[tono]
    buf = np.zeros((int((dur + 4) * SR), 2), np.float32)
    prog = acordes(b, [0, 5, 3, 0], mayor=True)
    largo = 8.0; t, k = 0.0, 0
    while t < dur:
        ac = prog[k % 4]; n = int((largo + 3) * SR)
        for m in ac + [ac[0] + 12]:
            for d in (-0.003, 0.0, 0.003):
                x = np.sin(2 * np.pi * hz(m) * (1 + d) * t_(n)).astype(np.float32)
                poner(buf, x * env(n, 2.5, 1.0, 0.8, 3.0), t, 0.032, d * 150)
        for _ in range(2):  # destellos, pocos
            m = ac[0] + 24 + [0, 4, 7, 11, 14][int(rng.integers(0, 5))]
            nn = int(2.5 * SR)
            poner(buf, fm(hz(m), nn, 5.0, 0.6, 2.0), t + float(rng.uniform(0.5, largo)), 0.022, float(rng.uniform(-0.7, 0.7)))
        t += largo; k += 1
    final(buf, dur, [hz(x) for x in prog[0]], lambda f, n: np.sin(2 * np.pi * f * t_(n)).astype(np.float32), 0.05)
    return eco(buf, 0.45, 0.45, 0.3)


def final(buf, dur, fs, voz, g):
    n = int(3 * SR)
    for f in fs:
        poner(buf, voz(f, n) * env(n, 0.01, 0.3, 0.7, 2.0), dur, g)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("estilo", choices=["chip", "campanas", "cosmos"])
    ap.add_argument("--dur", type=float, required=True, help="segundos (lo que dura la voz)")
    ap.add_argument("--tempo", type=float)
    ap.add_argument("--tono", default=None)
    ap.add_argument("--salida", default="musica.wav")
    a = ap.parse_args()
    defecto = {"chip": (112, "C"), "campanas": (88, "D"), "cosmos": (60, "A")}[a.estilo]
    gen = {"chip": chip, "campanas": campanas, "cosmos": cosmos}[a.estilo]
    x = gen(a.dur, a.tempo or defecto[0], a.tono or defecto[1])
    x = x[: int((a.dur + 3) * SR)]
    f = int(2.0 * SR)
    x[-f:] *= np.linspace(1, 0, f)[:, None]
    x *= 10 ** (-6 / 20) / (np.abs(x).max() + 1e-9)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le",
                    a.salida], input=x.astype(np.float32).tobytes(), check=True)
    print(f"{a.salida}: {a.estilo}, {len(x) / SR:.1f} s")


if __name__ == "__main__":
    main()
