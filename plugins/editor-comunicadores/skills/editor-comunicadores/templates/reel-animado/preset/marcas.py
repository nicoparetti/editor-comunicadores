# Auditoría de marcas: la palabra que abre un tramo de voz (tras una pausa) se lleva al inicio real del tramo.
import json, subprocess, numpy as np
x = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','voz_v1.wav','-ac','1','-ar','48000','-f','f32le','-'],capture_output=True).stdout, np.float32)
hop = 480; n = len(x)//hop
db = 20*np.log10(np.sqrt(np.mean(x[:n*hop].reshape(n,hop)**2,1))+1e-9)
on = db > -34; segs = []; i = 0
while i < n:
    if on[i]:
        j = i
        while j < n and on[j]: j += 1
        segs.append([i/100, j/100]); i = j
    else: i += 1
m = []
for a, b in segs:
    if m and a - m[-1][1] < 0.12: m[-1][1] = b
    else: m.append([a, b])
W = json.load(open('voz_v1_palabras.json'))
CORR = {12: 4.02, 13: 4.63, 14: 4.77, 15: 5.04, 16: 5.35, 17: 6.18, 18: 6.31, 19: 6.57, 20: 6.70, 21: 7.16}
log = []
for a, b in m:
    # palabra cuya marca cae más cerca del inicio del tramo (dentro de ±0,45 s)
    cand = [k for k, w in enumerate(W) if a - 0.25 <= w['s'] <= a + 0.45]
    if not cand: continue
    k = min(cand, key=lambda k: abs(W[k]['s'] - a))
    if abs(W[k]['s'] - a) > 0.06 and k not in CORR:
        log.append(f"{k}:{W[k]['w']} {W[k]['s']:.2f}→{a:.2f}"); W[k]['s'] = round(a, 2)
for k, t in CORR.items(): W[k]['s'] = t
for p, q in zip(W, W[1:]):
    if q['s'] <= p['s']: q['s'] = round(p['s'] + 0.05, 3)
json.dump(W, open('palabras_v2.json', 'w'), ensure_ascii=False, indent=0)
print(len(log), 'corregidas'); print(' · '.join(log))
