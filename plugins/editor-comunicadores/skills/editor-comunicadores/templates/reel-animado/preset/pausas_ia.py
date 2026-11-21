# Pausas de voz IA (CapCut u otra): conserva la cadencia y solo acorta los silencios que se pasan de un tope.
# Uso: python3 pausas_ia.py voz.wav palabras.json salida_prefijo
# Topes: fin de oración 0,50 s · coma o pausa interna 0,45 s · excepciones por palabra (EXC).
import json, subprocess, sys, numpy as np
SR = 48000; HOP = int(0.01 * SR); THR = -40.0; MIN_RUN = 0.25; FADE = int(0.008 * SR)
CAP_ORACION, CAP_COMA = 0.50, 0.45
LEAD, TAIL = 0.10, 1.60
# palabra que termina la pausa (sin puntuación, minúsculas) -> tope propio (None = no tocar)
EXC = {'deo': None,          # «Coram Deo, | delante…»: freno pedido en el guion
       'púlpito': 0.60}      # quiebre «no pasó por el púlpito. | Perkins…»

src, pj, out = sys.argv[1], sys.argv[2], sys.argv[3]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).copy()
n = len(x) // HOP
db = 20 * np.log10(np.sqrt(np.mean(x[:n * HOP].reshape(n, HOP) ** 2, axis=1)) + 1e-9)
sil = db < THR
runs = []; i = 0
while i < n:
    if sil[i]:
        j = i
        while j < n and sil[j]: j += 1
        runs.append((i * 0.01, j * 0.01)); i = j
    else: i += 1
W = json.load(open(pj))
voz = np.where(~sil)[0]; v0, v1 = voz[0] * 0.01, (voz[-1] + 1) * 0.01

cuts = []   # (inicio, fin) en segundos del original a quitar
if v0 > LEAD: cuts.append((0.0, v0 - LEAD))
log = []
for a, b in runs:
    d = b - a
    if d < MIN_RUN or a < v0 or b > v1: continue
    prev = [w for w in W if w['s'] < a + 0.05]
    if not prev: continue
    pw = prev[-1]['w']; key = pw.strip('.,;:!?«»"').lower()
    cap = CAP_ORACION if pw.rstrip('»"').endswith(('.', '?', '!')) else CAP_COMA
    if key in EXC:
        cap = EXC[key]
    if cap is None or d <= cap + 0.02:
        continue
    quitar = d - cap
    c0 = a + cap / 2; cuts.append((c0, c0 + quitar))
    log.append(f'{a:7.2f}  «{pw}»  {d:.2f} → {cap:.2f} s  (−{quitar:.2f})')

# armar la voz nueva
keep = []; t = 0.0
for c0, c1 in cuts:
    keep.append((t, c0)); t = c1
keep.append((t, v1))
seg = []
for k0, k1 in keep:
    s = x[int(k0 * SR):int(k1 * SR)].copy()
    if len(s) > 2 * FADE:
        s[:FADE] *= np.linspace(0, 1, FADE); s[-FADE:] *= np.linspace(1, 0, FADE)
    seg.append(s)
y = np.concatenate(seg + [np.zeros(int(TAIL * SR), np.float32)])

def nuevo(t):
    q = 0.0
    for c0, c1 in cuts:
        if t >= c1: q += c1 - c0
        elif t > c0: q += t - c0
    return round(t - q, 3)

W2 = [dict(w=w['w'], s=nuevo(w['s']), e=nuevo(w['e'])) for w in W]
json.dump(W2, open(out + '_palabras.json', 'w'), ensure_ascii=False, indent=0)
json.dump(dict(FIN=round(len(y) / SR, 3), cortes=[[round(a, 3), round(b, 3)] for a, b in cuts]), open(out + '_cortes.json', 'w'), indent=1)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'pcm_s24le', out + '.wav'], input=y.tobytes(), check=True)
# verificación: lo quitado tiene que ser silencio
peor = max(float(np.max(np.abs(x[int(a * SR):int(b * SR)]))) for a, b in cuts)
print('\n'.join(log))
print(f'cortes: {len(cuts)} · quitado {sum(b - a for a, b in cuts):.2f} s · duración {len(x) / SR:.2f} → {len(y) / SR:.2f} s · pico en lo quitado {20 * np.log10(peor + 1e-9):.1f} dBFS')
