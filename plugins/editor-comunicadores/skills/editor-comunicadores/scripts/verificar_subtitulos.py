#!/usr/bin/env python3
"""Verifica un .ass contra el estándar de subtítulos de la persona: mide, no mira.

Comprueba en todos los eventos visibles (capa 1):
  · un solo tamaño por fuente en todo el video (base y complementaria)
  · el primer renglón de cada bloque siempre en la misma posición (reel: y=1260; clip: y=922)
  · en los bloques de dos renglones, dibujados con libass: entre la tinta de un renglón y la del
    siguiente quedan 6 px (se aceptan 5–8) y nunca se tocan
  · ningún renglón más ancho que 600 px, medido con las fuentes reales (zona segura unificada)
  · sin punto final y sin mayúsculas sostenidas
Uso: python3 verificar_subtitulos.py subtitulos.ass [--formato reel|clip] [--fuentes 4_Recursos/fuentes]
Sale con código 1 si encuentra errores.
"""
import argparse, collections, glob, os, re, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageFont

Y = {'reel': 1260, 'clip': 922}
MAXW = 600   # zona segura unificada IG + TikTok (references/zona-segura.md)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ass')
    ap.add_argument('--formato', choices=list(Y), default='reel')
    ap.add_argument('--fuentes', default=os.environ.get('EDITOR_FUENTES', '4_Recursos/fuentes'))
    a = ap.parse_args()
    fuentes_dir = os.path.abspath(a.fuentes)

    fuentes = {}
    for p in glob.glob(os.path.join(fuentes_dir, '*.[ot]tf')):
        fam, est = ImageFont.truetype(p, 40).getname()
        fuentes.setdefault(fam, p); fuentes.setdefault(f'{fam} {est}', p)

    texto = open(a.ass, encoding='utf-8').read()
    header = texto[:texto.index('[Events]')] + '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
    ev = collections.OrderedDict()      # (start, end) -> [(y, raw_text, words)]
    for l in texto.splitlines():
        if not l.startswith('Dialogue: 1,'): continue
        parts = l.split(',', 9)
        start, end, text = parts[1], parts[2], parts[9]
        m = re.search(r'\\pos\((\d+),(\d+)\)', text)
        y = int(m.group(2)) if m else None
        words = []
        for tags, word in re.findall(r'\{([^}]*)\}([^{]*)', text):
            fn = re.search(r'\\fn([^\\}]+)', tags); fs = re.search(r'\\fs(\d+)', tags)
            al = re.search(r'\\alpha&H([0-9A-F]{2})&', tags)
            if word.strip() and fn and fs:
                words.append((fn.group(1), int(fs.group(1)), word.strip(), (al.group(1) if al else '00') != 'FF'))
        ev.setdefault((start, end), []).append((y, text, words))

    tmp = tempfile.mkdtemp(prefix='verif_')

    def filas_tinta(lineas):
        with open(os.path.join(tmp, 'g.ass'), 'w', encoding='utf-8') as f:
            f.write(header)
            for _, raw, _ in lineas:
                quieto = re.sub(r'\\t\([^)]*\)|\\fad\([^)]*\)|\\fsc[xy]\d+', '', raw)   # sin animación: se mide el estado final
                f.write(f"Dialogue: 0,0:00:00.00,0:00:01.00,Sub,,0,0,0,,{quieto.replace('&HFF&', '&H00&')}\n")
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:d=0.2',
                        '-vf', f'subtitles=g.ass:fontsdir={fuentes_dir}', '-frames:v', '1', 'g.png'], cwd=tmp, check=True)
        img = np.asarray(Image.open(os.path.join(tmp, 'g.png')).convert('L'))
        return img.max(1) > 40

    errores = []; tam = collections.defaultdict(set); maxw = 0; gaps = []; vistos = set()
    for (s, e), lineas in ev.items():
        ys = sorted(y for y, _, _ in lineas if y is not None)
        if ys and ys[0] != Y[a.formato]: errores.append(f'{s}: primer renglón en y={ys[0]} (debe ser {Y[a.formato]})')
        for y, _, words in lineas:
            w = 0
            for j, (fn, fs, word, vis) in enumerate(words):
                tam[fn].add(fs)
                p = fuentes.get(fn)
                if p:
                    f = ImageFont.truetype(p, fs); w += f.getlength(word) + (f.getlength(' ') if j else 0)
            maxw = max(maxw, w)
            if w > MAXW + 10: errores.append(f'{s}: renglón de {w:.0f} px (máx. {MAXW})')
            t = ' '.join(x[2] for x in words)
            if t.endswith('.'): errores.append(f'{s}: punto final en "{t}"')
            if len(t) > 3 and t.isupper(): errores.append(f'{s}: mayúsculas sostenidas en "{t}"')
        if len(lineas) >= 2:
            clave = tuple(sorted((y, re.sub(r'\\alpha&H..&', '', raw)) for y, raw, _ in lineas))
            if clave in vistos: continue
            vistos.add(clave)
            filas = filas_tinta(lineas); idx = np.where(filas)[0]
            huecos = [(idx[k], idx[k + 1]) for k in range(len(idx) - 1) if idx[k + 1] - idx[k] > 1]
            if len(huecos) < len(lineas) - 1:
                errores.append(f'{s}: los renglones se tocan'); continue
            g = min(b - a - 1 for a, b in huecos[:len(lineas) - 1])
            gaps.append(int(g))
            if not 5 <= g <= 8: errores.append(f'{s}: {g} px entre la tinta de los renglones (debe ser ~6)')

    print('Tamaños por fuente:', {n: sorted(v) for n, v in tam.items()})
    for n, v in tam.items():
        if len(v) > 1: errores.append(f'La fuente "{n}" aparece con {len(v)} tamaños distintos: {sorted(v)}')
    print(f'Bloques revisados: {len(ev)} · renglón más ancho: {maxw:.0f} px · espacio de tinta en bloques de 2 renglones: {sorted(set(gaps)) or "—"} px')
    if errores:
        print(f'\n{len(errores)} ERRORES:'); [print(' -', x) for x in errores[:60]]; sys.exit(1)
    print('OK: un solo tamaño por fuente, primera línea fija, interlineado medido, anchos dentro del límite.')


if __name__ == '__main__':
    main()
