#!/usr/bin/env python3
"""Subtítulos con el estándar del editor. Genera un .ass (para quemar o como capa con alfa) y un .srt.

Entradas:
  --palabras  JSON con las palabras y sus tiempos: [{"w": "Este", "s": 0.37, "e": 0.53}, ...]
              (también [["Este", 0.37, 0.53], ...]). Lo produce transcribir.py.
  --bloques   un bloque por línea, tal como debe verse en pantalla:
                "/"          salto de renglón dentro del bloque
                *palabra*    palabra en tipografía complementaria (cursiva con color)
                H:...        highlight acumulativo (las palabras se suman sin moverse)
                # ...        comentario; las líneas vacías se ignoran
              Cada palabra del bloque se empareja en orden con una de --palabras (sin tildes, mayúsculas
              ni puntuación). Lo que se ve es el texto de --bloques: nombres corregidos y voseo van ahí.

Formatos:
  --formato reel   (por defecto) Cal Sans SB 50 px (11 pt) + PlayfairDisplay-SemiBoldItalic crema, centro del renglón en y=1260 (-600 pt)
  --formato clip   clips de predicaciones: fuentes y tamaños por parámetro, primera línea anclada arriba en y=922 (centro)

Interlineado (regla permanente): "lo más cerca posible sin que se toquen". Cada renglón se dibuja solo con
libass (FFmpeg) sobre negro, se mide la tinta, y el renglón 2 se ubica para que su tinta empiece 6 px debajo
del final de la tinta del renglón 1. Necesita ffmpeg en el PATH.

Uso:
  python3 subtitulos.py --palabras p.json --bloques b.txt --fin 59.3 --salida trabajo/subtitulos [--sin-animacion]
"""
import argparse, json, os, re, subprocess, sys, tempfile, unicodedata
import numpy as np
from PIL import Image, ImageFont

PT = 4.54                 # 1 pt de CapCut ≈ 4,54 px en 1080×1920
LS = -2                   # interletrado CapCut -1 (≈ -2 px en libass) en la fuente base
WS = 4                    # compensación del espacio entre palabras al cerrar el interletrado
GAP_TINTA = 6             # px entre el final de la tinta de un renglón y el comienzo de la del siguiente
WHITE = '&HFFFFFF&'
POP = '\\fad(50,0)\\fscx106\\fscy106\\t(0,130,\\fscx100\\fscy100)'   # fade 50 ms + escala 106→100 % en 130 ms

FORMATOS = {
    'reel': dict(base='CalSans-SB.ttf', comp='PlayfairDisplay-SemiBoldItalic.ttf', tam=round(11 * PT), y=1260, ancla=5,
                 acento='#F6F6A8', sombra='B4', maxw=600, ls=LS, factor=None),
    'clip': dict(base='Manrope-ExtraBold.ttf', comp='DMSerifDisplay-Italic.ttf', tam=68, y=922, ancla=8,
                 acento='#F6F6A8', sombra='70', maxw=600, ls=0, factor=round(84 / 68, 3)),   # DM Serif 84 con Manrope 68 (aprobado)
}


def norm(t):
    t = unicodedata.normalize('NFD', t.lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^\w]', '', t)


def ts(t):
    t = max(t, 0); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def s2(t):
    ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def nombre_fuente(path):
    fam, estilo = ImageFont.truetype(path, 40).getname()
    italica = 'italic' in estilo.lower()
    if estilo.lower() in ('regular', 'italic'):
        return fam, italica
    return f"{fam} {estilo}", italica


def altura_x(path, size=200):
    b = ImageFont.truetype(path, size).getbbox('xnuv', anchor='ls')
    return -b[1]


def hex_ass(h):
    h = h.lstrip('#'); return f'&H{h[4:6]}{h[2:4]}{h[0:2]}&'.upper()


def hdr(fn, size):
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,{fn},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,90,90,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


class Medidor:
    """Dibuja un renglón con libass y devuelve las filas donde empieza y termina la tinta."""

    def __init__(self, fuentes, header):
        self.fuentes, self.header, self.cache = fuentes, header, {}
        self.tmp = tempfile.mkdtemp(prefix='subs_')

    def tinta(self, texto, head):
        key = (texto, head)
        if key in self.cache: return self.cache[key]
        ass = os.path.join(self.tmp, 'm.ass'); png = os.path.join(self.tmp, 'm.png')
        with open(ass, 'w', encoding='utf-8') as f:
            f.write(self.header + f"Dialogue: 0,0:00:00.00,0:00:01.00,Sub,,0,0,0,,{{{head}}}{texto}\n")
        r = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:d=0.2',
                            '-vf', f"subtitles={os.path.basename(ass)}:fontsdir={self.fuentes}", '-frames:v', '1', os.path.basename(png)],
                           cwd=self.tmp, capture_output=True, text=True)
        if r.returncode != 0: sys.exit('No se pudo medir con FFmpeg/libass: ' + r.stderr[-400:])
        a = np.asarray(Image.open(png).convert('L')); filas = np.where(a.max(1) > 40)[0]
        res = (int(filas[0]), int(filas[-1])) if len(filas) else None
        self.cache[key] = res
        return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--palabras', required=True)
    ap.add_argument('--bloques', required=True)
    ap.add_argument('--fin', type=float, required=True, help='duración del video en segundos (fin del último bloque)')
    ap.add_argument('--salida', required=True, help='ruta sin extensión')
    ap.add_argument('--formato', choices=list(FORMATOS), default='reel')
    ap.add_argument('--fuentes', default=os.environ.get('EDITOR_FUENTES', '4_Recursos/fuentes'))
    ap.add_argument('--base'); ap.add_argument('--complementaria')
    ap.add_argument('--tam-base', type=int, help='tamaño de la fuente base en px del ASS')
    ap.add_argument('--y', type=int, help='posición de la primera línea')
    ap.add_argument('--acento', help='color de la complementaria, #RRGGBB (por defecto crema #F6F6A8)')
    ap.add_argument('--factor-complementaria', type=float, default=None,
                    help='por defecto se calcula para igualar la altura visual de las minúsculas')
    ap.add_argument('--sin-animacion', action='store_true', help='sin la entrada de 50 ms + escala 106→100 %')
    a = ap.parse_args()
    F = dict(FORMATOS[a.formato])
    for k, v in (('base', a.base), ('comp', a.complementaria), ('tam', a.tam_base), ('y', a.y), ('acento', a.acento)):
        if v is not None: F[k] = v
    BASE, Y, MAXW, ANCLA, LSB = F['tam'], F['y'], F['maxw'], F['ancla'], F['ls']
    ACC = hex_ass(F['acento'])

    base_path = os.path.join(a.fuentes, F['base']); key_path = os.path.join(a.fuentes, F['comp'])
    for p in (base_path, key_path):
        if not os.path.exists(p): sys.exit(f'Falta la fuente {p}')
    BASE_FN, _ = nombre_fuente(base_path); KEY_FN, KEY_IT = nombre_fuente(key_path)
    keyk = a.factor_complementaria or (F['factor'] if (F['factor'] and not a.base and not a.complementaria) else round(altura_x(base_path) / altura_x(key_path), 3))
    if not 0.9 <= keyk <= 1.35:
        sys.exit(f'Factor de complementaria raro ({keyk}); revisar las fuentes o pasar --factor-complementaria')
    KEYS = round(BASE * keyk)

    raw = json.load(open(a.palabras, encoding='utf-8'))
    W = [(d['w'], float(d['s']), float(d['e'])) if isinstance(d, dict) else (d[0], float(d[1]), float(d[2])) for d in raw]
    W = [w for w in W if norm(w[0])]
    B = [l.strip() for l in open(a.bloques, encoding='utf-8') if l.strip() and not l.strip().startswith('#')]

    fb = ImageFont.truetype(base_path, BASE); fk = ImageFont.truetype(key_path, KEYS)
    HEADER = hdr(BASE_FN, BASE)
    med = Medidor(os.path.abspath(a.fuentes), HEADER)

    def parse(body):
        out = []
        for li, l in enumerate(body.split('/')):
            for w in l.split():
                out.append((li, w.strip('*'), w.startswith('*')))
        return out

    def ancho(toks):
        w = 0
        for j, (_, t, k) in enumerate(toks):
            f = fk if k else fb
            w += f.getlength(t) + (0 if k else LSB * (len(t) - 1)) + ((f.getlength(' ') + WS) if j else 0)
        return w

    i = 0; blocks = []; maxw = 0
    for b in B:
        kind = 'H' if b.startswith('H:') else 'P'; body = b[2:].strip() if kind == 'H' else b
        toks = parse(body)
        for li in range(max(t[0] for t in toks) + 1):
            wl = ancho([t for t in toks if t[0] == li]); maxw = max(maxw, wl)
            if wl > MAXW: sys.exit(f'Renglón demasiado ancho ({wl:.0f} px > {MAXW}): "{b}". Pártelo en dos bloques o en dos renglones con "/".')
        idx = list(range(i, i + len(toks)))
        if idx[-1] >= len(W): sys.exit(f'Se acabaron las palabras del transcript en el bloque "{b}"')
        for k, t in zip(idx, toks):
            if norm(W[k][0]) != norm(t[1]):
                ctx = ' '.join(w[0] for w in W[max(0, k - 3):k + 4])
                sys.exit(f'No coincide: bloque "{b}" espera "{t[1]}" y el transcript dice "{W[k][0]}" (en {W[k][1]:.2f} s; contexto: {ctx})')
        i += len(toks)
        blocks.append(dict(kind=kind, body=body, toks=toks, idx=idx, start=max(0, W[idx[0]][1] - 0.04)))
    if i != len(W):
        sys.exit(f'Sobran {len(W) - i} palabras del transcript sin bloque (desde "{W[i][0]}" en {W[i][1]:.2f} s)')

    for n, bl in enumerate(blocks):
        nxt = blocks[n + 1]['start'] if n + 1 < len(blocks) else a.fin
        le = W[bl['idx'][-1]][2]
        bl['end'] = min(nxt, max(le + 0.35, bl['start'] + 0.4)) if nxt - le > 0.6 else nxt

    def wtag(word, key, alpha='00'):
        if key:
            return f"{{\\fn{KEY_FN}\\i{1 if KEY_IT else 0}\\fs{KEYS}\\fsp0\\1c{ACC}\\alpha&H{alpha}&}}{word}"
        return f"{{\\fn{BASE_FN}\\i0\\fs{BASE}\\fsp{LSB}\\1c{WHITE}\\alpha&H{alpha}&}}{word}"

    def texto_linea(toks, li, visible=None):
        s = ''; first = True
        for j, (l, w, k) in enumerate(toks):
            if l != li: continue
            if not first: s += f"{{\\fsp{WS}}} "
            first = False
            s += wtag(w, k, '00' if (visible is None or j < visible) else 'FF')
        return s

    def head(y): return f'\\an{ANCLA}\\pos(540,{y})\\bord0\\shad0\\q2'

    saltos = []
    def posiciones(toks):
        """y de cada renglón: el 1º siempre en Y; cada siguiente, 6 px de tinta debajo del anterior (medido)."""
        nl = max(t[0] for t in toks) + 1; ys = [Y]
        for li in range(1, nl):
            prev = med.tinta(texto_linea(toks, li - 1), head(ys[-1]))
            cur = med.tinta(texto_linea(toks, li), head(Y))
            ys.append(prev[1] + GAP_TINTA + 1 - (cur[0] - Y))
            saltos.append(ys[-1] - ys[-2])
        return ys

    POPX = '' if a.sin_animacion else POP
    ev = []; srt = []
    for bl in blocks:
        st, en, toks = bl['start'], bl['end'], bl['toks']
        srt.append((st, en, ' '.join(w for _, w, _ in toks)))
        ys = posiciones(toks)
        if bl['kind'] == 'P':
            for li, y in enumerate(ys):
                ev.append((st, en, '{' + head(y) + POPX + '}' + texto_linea(toks, li)))
        else:
            n = len(toks)
            for k in range(n):
                s0 = st if k == 0 else W[bl['idx'][k]][1] - 0.04
                e0 = W[bl['idx'][k + 1]][1] - 0.04 if k + 1 < n else en
                for li, y in enumerate(ys):
                    t = texto_linea(toks, li, k + 1)
                    if '&H00&}' in t:
                        fad = '\\fad(50,0)' if (k == 0 and not a.sin_animacion) else ''
                        ev.append((s0, e0, '{' + head(y) + fad + '}' + t))

    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    with open(a.salida + '.ass', 'w', encoding='utf-8') as f:
        f.write(HEADER)
        for s0, e0, t in ev:
            # sombra: copia negra desenfocada, sin desplazamiento, en la capa de abajo
            sh = re.sub(r'\\1c&H[0-9A-F]{6}&', r'\\1c&H000000&', t).replace('\\alpha&H00&', f'\\alpha&H{F["sombra"]}&').replace('\\bord0\\shad0', '\\bord0\\shad0\\blur14', 1)
            f.write(f"Dialogue: 0,{ts(s0)},{ts(e0)},Sub,,0,0,0,,{sh}\n")
            f.write(f"Dialogue: 1,{ts(s0)},{ts(e0)},Sub,,0,0,0,,{t}\n")
    with open(a.salida + '.srt', 'w', encoding='utf-8') as f:
        for n, (s0, e0, t) in enumerate(srt, 1):
            f.write(f"{n}\n{s2(s0)} --> {s2(e0)}\n{t}\n\n")
    print(f'Formato {a.formato} · {len(blocks)} bloques · {len(ev)} eventos · renglón más ancho {maxw:.0f}/{MAXW} px')
    print(f'Base: {BASE_FN} {BASE} px · Complementaria: {KEY_FN} {KEYS} px (factor {keyk}) · acento {F["acento"]}')
    if saltos: print(f'Interlineado medido (6 px de tinta): saltos entre renglones {sorted(set(saltos))} px')
    print('Animación de entrada: ' + ('no' if a.sin_animacion else 'sí (fade 50 ms + escala 106→100 %)'))
    print(f'Archivos: {a.salida}.ass · {a.salida}.srt')


if __name__ == '__main__':
    main()
