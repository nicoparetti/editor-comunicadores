#!/usr/bin/env python3
"""Transcripción con marcas por palabra (whisper.cpp + DTW), por tramos y reanudable.

Uso (desde la raíz de la carpeta de trabajo, con el entorno cargado):
  python3 .herramientas/scripts/transcribir.py 1_Videos sin editar/clip.mp4 3_Videos editados/<nombre>/trabajo/transcripcion
Corre por tramos de ≤40 s cortados en silencios. Cada llamada de shell dura poco: si el script dice
"SIGUE", se vuelve a correr el mismo comando y continúa donde quedó.
Al terminar escribe en la carpeta de salida:
  palabras.json   [{"w","s","e"}] con inicio = marca DTW − 0,08 s (para subtitulos.py)
  TRANSCRIPT.md   texto por frases con su tiempo, para leer y para la hoja de edición
Los puntos de corte del video se eligen sobre la envolvente de energía, no sobre estas marcas.
"""
import json, os, re, subprocess, sys, time

LIMITE_S = 25           # solo empieza un tramo nuevo si la llamada lleva menos de esto (cada tramo tarda ~2 min)
TRAMO = 30              # duración objetivo de cada tramo (s): ~2 min de proceso con 4 núcleos; nunca más de 40
# Términos que ayudan al transcriptor: se completan con la sección 7 del perfil (variable TERMINOS).
PROMPT = (os.environ.get('TERMINOS', 'Claude, CapCut.') + ' Transcripción literal en español, tal como habla la persona.')


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def duracion(p):
    return float(sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).stdout.strip())


def cortes(wav, dur):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-i', wav, '-af', 'silencedetect=noise=-35dB:d=0.25', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', err)]
    fin = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
    medios = [(a + b) / 2 for a, b in zip(ini, fin)]
    pts = [0.0]
    while dur - pts[-1] > 40:
        objetivo = pts[-1] + TRAMO
        cand = [m for m in medios if pts[-1] + 15 < m < pts[-1] + 40]
        pts.append(min(cand, key=lambda m: abs(m - objetivo)) if cand else pts[-1] + TRAMO)
    pts.append(dur)
    return pts


def palabras_de(jf, offset):
    data = json.load(open(jf, encoding='utf-8'))
    out = []
    for seg in data.get('transcription', []):
        for t in seg.get('tokens', []):
            txt = t.get('text', '')
            if not txt or txt.startswith('[_') or txt.startswith('<|'):
                continue
            a = t['offsets']['from'] / 1000; b = t['offsets']['to'] / 1000
            dtw = t.get('t_dtw', -1)
            s = (dtw / 100 - 0.08) if isinstance(dtw, (int, float)) and dtw >= 0 else a
            if txt.startswith(' ') or not out:
                out.append({'w': txt.strip(), 's': round(offset + max(s, 0), 3), 'e': round(offset + b, 3)})
            else:                                    # continuación de la palabra (o puntuación pegada)
                out[-1]['w'] += txt; out[-1]['e'] = round(offset + b, 3)
    return [w for w in out if w['w']]


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, outdir = sys.argv[1], sys.argv[2]
    model = os.environ.get('WHISPER_MODEL', ''); binw = os.environ.get('WHISPER_BIN', 'whisper-cli')
    if not os.path.exists(model):
        sys.exit(f'Falta el modelo de Whisper en {model}. Ver entorno-y-herramientas.md → Transcripción.')
    os.makedirs(outdir, exist_ok=True); t0 = time.time()
    wav = os.path.join(outdir, 'audio16k.wav')
    if not os.path.exists(wav):
        sh(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', src, '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', wav])
    plan = os.path.join(outdir, 'tramos.json')
    if not os.path.exists(plan):
        json.dump(cortes(wav, duracion(wav)), open(plan, 'w'))
    pts = json.load(open(plan))
    for i in range(len(pts) - 1):
        base = os.path.join(outdir, f'tramo_{i:03d}')
        if os.path.exists(base + '.json'):
            continue
        if time.time() - t0 > LIMITE_S:
            print(f'SIGUE: {i}/{len(pts) - 1} tramos listos. Vuelve a correr el mismo comando.'); return
        tw = base + '.wav'
        sh(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(pts[i]), '-to', str(pts[i + 1]), '-i', wav, '-c:a', 'pcm_s16le', tw])
        sh([binw, '-m', model, '-l', 'es', '-t', '4', '-ojf', '-dtw', 'large.v3.turbo', '-nfa',   # DTW no funciona con flash attention
            '--prompt', PROMPT, '-of', base, '-f', tw])
        os.remove(tw)
        print(f'tramo {i + 1}/{len(pts) - 1} listo ({pts[i]:.1f}–{pts[i + 1]:.1f} s)')
    W = []
    for i in range(len(pts) - 1):
        W += palabras_de(os.path.join(outdir, f'tramo_{i:03d}.json'), pts[i])
    for a, b in zip(W, W[1:]):                       # monotonía y duración mínima
        if b['s'] < a['s']: b['s'] = a['s']
        if a['e'] - a['s'] < 0.06: a['e'] = round(a['s'] + 0.06, 3)
    json.dump(W, open(os.path.join(outdir, 'palabras.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    with open(os.path.join(outdir, 'TRANSCRIPT.md'), 'w', encoding='utf-8') as f:
        f.write(f'# Transcript de {os.path.basename(src)}\n\nRevisar términos propios y nombres antes de usarlo en pantalla.\n\n')
        frase = []; ini = None
        for w in W:
            if ini is None: ini = w['s']
            frase.append(w['w'])
            if re.search(r'[.?!]$', w['w']) or len(frase) >= 18:
                f.write(f"[{int(ini // 60):02d}:{ini % 60:05.2f}] {' '.join(frase)}\n"); frase = []; ini = None
        if frase: f.write(f"[{int(ini // 60):02d}:{ini % 60:05.2f}] {' '.join(frase)}\n")
    print(f'LISTO: {len(W)} palabras → {outdir}/palabras.json y TRANSCRIPT.md')


if __name__ == '__main__':
    main()
