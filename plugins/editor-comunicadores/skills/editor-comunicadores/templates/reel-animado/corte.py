# Corte ajustado: quita la toma fallida y silencios >= 0.2 s (cola 0.05 / entrada 0.04)
import json, sys, subprocess, numpy as np, wave
src, out_json = sys.argv[1], sys.argv[2]
QUITAR = [(19.30, 24.05)]   # primera lectura + tropiezo en "herederos"; queda la retoma
w = wave.open(src); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768
hop = int(sr*0.01); n = len(x)//hop
rms = np.sqrt(np.mean(x[:n*hop].reshape(n, hop)**2, axis=1)) + 1e-9
db = 20*np.log10(rms)
voz = db > -44
# silencios = corridas sin voz
sil = []; i = 0
while i < n:
    if not voz[i]:
        j = i
        while j < n and not voz[j]: j += 1
        sil.append((i*0.01, j*0.01)); i = j
    else: i += 1
dur = len(x)/sr
keep = []; cur = None
segs = []
# segmentos de voz entre silencios >= 0.2
t = 0.0
for a, b in sil:
    if b - a >= 0.2:
        if a > t: segs.append((t, a))
        t = b
if t < dur: segs.append((t, dur))
segs = [(max(0, a-0.04), min(dur, b+0.05)) for a, b in segs if b - a > 0.03]
# quitar rangos
def restar(segs, q):
    out=[]
    for a,b in segs:
        pieces=[(a,b)]
        for qa,qb in q:
            nxt=[]
            for pa,pb in pieces:
                if pb<=qa or pa>=qb: nxt.append((pa,pb)); continue
                if pa<qa: nxt.append((pa,qa))
                if pb>qb: nxt.append((qb,pb))
            pieces=nxt
        out+= [p for p in pieces if p[1]-p[0]>0.05]
    return out
res = restar(segs, QUITAR)
# fusionar solapados
m = []
for a, b in sorted(res):
    if m and a <= m[-1][1] + 0.001: m[-1] = (m[-1][0], max(m[-1][1], b))
    else: m.append((a, b))
json.dump([[round(a,3), round(b,3)] for a, b in m], open(out_json, 'w'))
print(len(m), 'segmentos', round(sum(b-a for a,b in m),2), 's de', round(dur,2))
for a,b in m:
    if 15<a<30: print(round(a,2), round(b,2))
