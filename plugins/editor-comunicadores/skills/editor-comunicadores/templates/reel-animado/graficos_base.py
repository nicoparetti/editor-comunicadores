# Generador de ejemplo del estilo por defecto: escribe graficos.html con render(t).
# Copiar junto con base/kit_base.py y figuras.py a trabajo/ y reescribir las escenas para cada reel.
# Tiempos: T(i) / TE(i) salen de palabras_vN.json (lista de {w, s, e}). Sin ese archivo usa tiempos de demostración.
# Uso: TEMA=gris|noche python3 graficos_base.py [palabras.json] [fin_s]
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base'))
from kit_base import *
from figuras import orando, martillando, grieta_v
tema()

if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    W = json.load(open(sys.argv[1]))
else:                                                     # demostración: una palabra cada 0,35 s
    W = [{'w': f'p{i}', 's': round(0.3 + i * 0.35, 2), 'e': round(0.6 + i * 0.35, 2)} for i in range(60)]
T = lambda i: W[i]['s']
TE = lambda i: W[i]['e']
FIN = float(sys.argv[2]) if len(sys.argv) > 2 else round(TE(len(W) - 1) + 1.6, 2)

def casa(x, y, s=1):
    return f'<g transform="translate({x},{y}) scale({s})"><path d="M-40,0 L0,-36 L40,0 V46 H-40 Z"/><path d="M-10,46 V18 H10 V46"/></g>'

S = []
# Escena 1 · el año que retrocede (gancho)
casas = ''.join(casa(300 + i * 105, 760 + (18 if i % 2 else 0), .95) for i in range(5))
S.append(escena(0, T(12),
    fx(T(0), f'<div class="lab" style="font-size:32px;color:{ACC}">hace casi</div>', 'position:absolute;left:120px;right:240px;top:380px;text-align:center', dy=10),
    contador('c1', 2026, 1727, 0.2, 1.75, 'position:absolute;left:120px;right:240px;top:440px;text-align:center;font-size:230px'),
    fx(T(3), f'<div class="mono" style="font-size:30px;color:{GRY}">≈ 300 años atrás</div>', 'position:absolute;left:120px;right:240px;top:700px;text-align:center'),
    fx(T(4), svg(f'<g stroke="{TXT}" stroke-width="4" stroke-linejoin="round" transform="translate(-60,140)">{casas}<path d="M240,832 H800" stroke="{DIM}"/></g>'), 'position:absolute;inset:0'),
    rotulo(120, 1200, T(7), 'una aldea', 'el lugar de la historia', size=34)))
# Escena 2 · dos figuras y la línea quebrada (tesis)
S.append(escena(T(12), T(26),
    fx(T(12), f'<div class="lab" style="font-size:32px;color:{ACC}">la idea</div>', 'position:absolute;left:120px;right:240px;top:300px;text-align:center', dy=10),
    svg(gfx(T(14), f'<g transform="translate(270,1000)">{orando(TXT)}</g>'),
        gfx(T(18), f'<g transform="translate(700,1000)">{martillando(TXT)}</g>'),
        grieta(grieta_v(480, 440, 1060), T(22), T(22) + .45)),
    fx(T(15), f'<div class="mono" style="font-size:28px;color:{GRY}">unos</div><div style="font-family:CalSans;font-size:52px;letter-spacing:-1px;margin-top:6px">oraban</div>', 'position:absolute;left:120px;width:320px;top:1060px;text-align:center'),
    fx(T(19), f'<div class="mono" style="font-size:28px;color:{GRY}">otros</div><div style="font-family:CalSans;font-size:52px;letter-spacing:-1px;margin-top:6px">trabajaban</div>', 'position:absolute;left:520px;width:320px;top:1060px;text-align:center')))
# Escena 3 · frase-tesis palabra a palabra
S.append(escena(T(26), T(40),
    palabras([[('cada', T(26)), ('trabajo', T(28))], [('puede', T(30)), ('ser', T(31)), ('un', T(32)), ('altar', T(33))]], 640, 96, 120)))
# Escena 4 · dato con contador y rótulo
S.append(escena(T(40), FIN,
    fx(T(40), f'<div class="lab" style="font-size:30px;color:{GRY}">durante</div>', 'position:absolute;left:120px;right:240px;top:520px;text-align:center'),
    contador('c2', 0, 100, T(41), T(44), f'position:absolute;left:120px;right:240px;top:580px;text-align:center;font-size:220px;color:{ACC}'),
    fx(T(44), '<div class="lab" style="font-size:40px">años</div>', 'position:absolute;left:120px;right:240px;top:820px;text-align:center', dy=18)))

subs = [(T(0), T(4), ['hace casi 300 años']), (T(4), T(12), ['en una _aldea_ pequeña']),
        (T(12), T(26), ['unos oraban', 'y otros *trabajaban*']), (T(40), FIN - 1.2, ['durante *100 años*'])]
open('graficos.html', 'w').write(pagina(S, subs, fin=FIN))
print('ok graficos.html · FIN', FIN, '· tema', ACC)
