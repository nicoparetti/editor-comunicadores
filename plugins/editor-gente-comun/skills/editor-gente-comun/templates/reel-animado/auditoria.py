# Control de calidad de un reel animado.
#   python3 auditoria.py marcas voz.wav palabras.json [usadas.py ...]   → tramos de voz medidos + palabras sospechosas
#   python3 auditoria.py sonido graficos.mp4 sfx_eventos.json           → efectos sin cambio visual cerca
import json, re, sys, subprocess
import numpy as np

def envolvente(wav):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', wav, '-f', 'f32le', '-ac', '1', '-ar', '48000', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32); h = 480; n = len(x) // h
    return np.array([20 * np.log10(np.sqrt((x[k*h:(k+1)*h] ** 2).mean()) + 1e-9) for k in range(n)])

def tramos(e, umbral=-34):
    runs = []; on = None
    for k, v in enumerate(e > umbral):
        if v and on is None: on = k
        if not v and on is not None:
            if k - on >= 3: runs.append([on / 100, k / 100])
            on = None
    m = []
    for a, b in runs:
        if m and a - m[-1][1] < 0.06: m[-1][1] = b
        else: m.append([a, b])
    return m

def marcas(wav, pal, fuentes):
    W = json.load(open(pal)); R = tramos(envolvente(wav))
    for a, b in R:
        ws = [f"{i}:{W[i]['w']}@{W[i]['s']:.2f}" for i in range(len(W)) if a - 0.05 <= W[i]['s'] < b - 0.02]
        print(f"[{a:.2f}-{b:.2f}] " + ' '.join(ws))
    usadas = set()
    for f in fuentes:
        for mm in re.finditer(r'\bTE?\((\d+)\)', open(f).read()): usadas.add(int(mm.group(1)))
    print('\nSOSPECHOSAS (palabras que disparan algo):')
    for i in sorted(usadas or range(len(W))):
        s = W[i]['s']; f = []
        if not any(a - 0.03 <= s + 0.04 <= b for a, b in R):
            nxt = min((a for a, b in R if a >= s - 0.03), default=None)
            f.append(f'en silencio; voz en {nxt}' if nxt else 'en silencio')
        if i and s < W[i-1]['s'] + 0.05: f.append('se superpone con la anterior')
        st = [a for a, b in R if a <= s + 0.04]
        if st and s - st[-1] > 0.12 and i and W[i-1]['w'][-1] in '.,?:': f.append(f'tras pausa: el tramo empieza en {st[-1]}')
        if f: print(f"  {i} {W[i]['w']} {s} | " + '; '.join(f))

def sonido(video, eventos, salto=('tic', 'contador', 'pad')):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-vf', 'scale=270:480,format=gray', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    F = np.frombuffer(raw, np.uint8).reshape(-1, 480, 270).astype(np.int16)
    fr = lambda t: F[min(len(F) - 1, max(0, int(round(t * 30))))]
    for t, p, d in json.load(open(eventos)):
        if any(s in d for s in salto): continue
        ch = (np.abs(fr(t + 0.4) - fr(t - 0.1)) > 12).mean() * 100
        if ch < 0.15: print(f'  {t:7.2f}  {ch:5.2f}%  {d}  ← sin cambio visual')

if __name__ == '__main__':
    if sys.argv[1] == 'marcas': marcas(sys.argv[2], sys.argv[3], sys.argv[4:])
    else: sonido(sys.argv[2], sys.argv[3])
