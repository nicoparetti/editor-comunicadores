# Aire en los cambios de escena: inserta silencio en el punto de menor energía de la pausa que precede a la palabra k.
import json, subprocess, numpy as np
SR = 48000
EXTRA = {28: .30, 48: .35, 67: .25, 85: .30, 112: .35, 122: .25, 143: .30, 166: .20, 173: .25, 188: .30, 206: .35, 238: .55, 246: .25, 262: -.10}   # 262: La persona pidió menos silencio entre «ministro» y «De lunes a lunes»
x = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','voz_v1.wav','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout, np.float32).copy()
W = json.load(open('palabras_v2.json'))
hop = 480; n = len(x) // hop
db = 20 * np.log10(np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, 1)) + 1e-9)
ins = []
for k, d in sorted(EXTRA.items()):
    a, b = W[k - 1]['s'] + 0.15, W[k]['s']
    i0, i1 = int(a * 100), int(b * 100)
    seg = db[i0:i1]
    # centro de la zona más silenciosa (ventana de 60 ms)
    win = np.convolve(seg, np.ones(6) / 6, 'valid'); j = int(np.argmin(win)) + 3
    p = (i0 + j) / 100; ins.append((p, d, k, round(float(db[i0 + j]), 1)))
out = []; last = 0
for p, d, k, lv in ins:
    if d >= 0:
        out.append(x[int(last * SR):int(p * SR)]); out.append(np.zeros(int(d * SR), np.float32)); last = p
    else:                                  # quitar silencio centrado en p
        out.append(x[int(last * SR):int((p + d / 2) * SR)]); last = p - d / 2
out.append(x[int(last * SR):]); y = np.concatenate(out)
def nuevo(t): return round(t + sum(d for p, d, k, lv in ins if t >= p), 3)
W2 = [dict(w=w['w'], s=nuevo(w['s']), e=nuevo(w['e'])) for w in W]
json.dump(W2, open('palabras_v3.json', 'w'), ensure_ascii=False, indent=0)
json.dump(dict(FIN=round(len(y) / SR, 3)), open('voz_v2_cortes.json', 'w'))
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-c:a','pcm_s24le','voz_v2.wav'], input=y.tobytes(), check=True)
for p, d, k, lv in ins: print(f"antes de «{W[k]['w']}» ({p:.2f} s, {lv} dB): +{d:.2f} s")
print('duración', round(len(x) / SR, 2), '→', round(len(y) / SR, 2))
