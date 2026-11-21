import numpy as np, subprocess, json
from scipy.signal import lfilter
SR = 48000
W = json.load(open('palabras_v3.json')); T = lambda i: W[i]['s']
END = json.load(open('voz_v2_cortes.json'))['FIN']; n = int(END * SR)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'voz_v2.wav', '-af', 'highpass=f=80,acompressor=threshold=0.0794:ratio=2.5:attack=10:release=120:makeup=1', '-ac', '2', '-ar', str(SR), 'voz_full.wav'], check=True)
v = load('voz_full.wav'); v = np.pad(v, ((0, max(0, n - len(v))), (0, 0)))[:n]; v *= 10 ** (-1 / 20) / np.abs(v).max()
vrms = np.sqrt(np.mean(v[np.abs(v).max(1) > 0.02] ** 2))
mix = np.zeros_like(v); cache = {}
EV = json.load(open('sfx_eventos.json'))
for t, f, pk, d in EV:
    if f not in cache: cache[f] = load('sfx/' + f)
    x = cache[f] * (10 ** (pk / 20) / (np.abs(cache[f]).max() + 1e-9)); i = int(t * SR); j = min(n, i + len(x))
    if i < n: mix[i:j] += x[:j - i]
def pad(freqs, t0, t1, rel_db, att=0.8, rel=1.2, bright=0.2):
    i0, i1 = int(t0 * SR), min(n, int(t1 * SR)); tt = np.arange(i1 - i0) / SR; dur = (i1 - i0) / SR; y = np.zeros(len(tt))
    for k, f in enumerate(freqs):
        for det in (-0.6, 0.6):
            ph = 2 * np.pi * (f + det) * tt + 0.003 * np.sin(2 * np.pi * 0.3 * tt + k) * f
            y += np.sin(ph) + bright * np.sin(2 * ph) / 2 + bright * .5 * np.sin(3 * ph) / 3
    y *= np.minimum(1, tt / att) * np.minimum(1, (dur - tt) / rel)
    a = np.exp(-2 * np.pi * 1800 / SR); y = lfilter([1 - a], [1, -a], y)
    core = y[int(min(att, dur / 3) * SR):max(int((dur - rel) * SR), int(min(att, dur / 3) * SR) + 1)]
    y *= vrms * 10 ** (rel_db / 20) / (np.sqrt(np.mean(core ** 2)) + 1e-9)
    mix[i0:i1] += np.stack([y, y], 1).astype(np.float32)
# Pads y cama: se suman octavas altas (262 · 392 · 523 Hz) porque el parlante del celular casi no reproduce < 150 Hz.
GRAVE = [65.41, 98.0, 130.81, 196.0, 261.63, 392.0, 523.25]
pad(GRAVE[:3] + GRAVE[4:6], 0, END, -12, att=1.0, rel=1.4, bright=.18)                         # cama continua (≈ 12 dB bajo la voz)
pad(GRAVE, T(166) - .2, T(173) + 1.0, -1, att=.6, rel=1.0, bright=.35)                        # momento espiritual: a la par de la voz
pad([146.83, 220.0, 293.66, 440.0, 587.33], T(179), T(188) + .4, -2, att=1.0, rel=.6, bright=.35)  # resplandor
pad(GRAVE, T(237), T(246), -2, att=.5, rel=1.0, bright=.3)                                    # momento espiritual
pad(GRAVE, T(262), END, -3, att=1.2, rel=1.2, bright=.3)                                      # cierre hasta el último cuadro
out = v + mix
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-af', 'alimiter=limit=0.89:attack=1:release=60:level=disabled', '-c:a', 'pcm_s24le', 'mezcla_full.wav'],
               input=out.astype(np.float32).tobytes(), check=True)
from collections import Counter
print(len(EV), 'efectos ·', round(len(EV) / END * 60), 'por minuto ·', Counter(e[1] for e in EV).most_common())
