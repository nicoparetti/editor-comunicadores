# Kit del estilo por defecto de reels animados (estilo de referencia "clásico"): dos paletas, piezas y motor render(t).
# Reglas en references/reels-animados.md. Uso típico desde un generador:
#   from kit_base import *
#   tema('gris')            # o tema('noche'); variable de entorno TEMA también sirve
#   S = [escena(0, 4.2, fx(0.1, '<div class="lab">hola</div>', 'position:absolute;top:400px;left:0;right:0;text-align:center'))]
#   open('graficos.html','w').write(pagina(S, subs=[...], fin=60))
# Fuentes en img/ junto al HTML: CalSans-Regular.ttf, Inter.ttf, InstrumentSerif-Italic.ttf, JetBrainsMono.ttf,
# PlayfairDisplay-SemiBoldItalic.ttf (o Playfair variable), GFSDidot-Regular.ttf, FrankRuhlLibre.ttf.
import json, os

TEMAS = {
    'gris':  dict(BG='#1B1F24', ACC='#F6F6A8', TXT='#F2F2EE', GRY='#8E949C', DIM='#5E6873', LINE='#454F5B',
                  LAND='#232930', LANDL='#46505C', CARD='rgba(36,42,50,.95)'),
    'noche': dict(BG='#0E1626', ACC='#E3A93A', TXT='#F3F0E8', GRY='#8A93A3', DIM='#566175', LINE='#2E3A50',
                  LAND='#16213A', LANDL='#33415C', CARD='rgba(22,33,56,.95)'),
}
T_ = dict(TEMAS['gris'])
def tema(nombre=None):
    """Elige la paleta ('gris' = gris y crema, 'noche' = noche y oro) y la deja en las variables globales del kit."""
    nombre = nombre or os.environ.get('TEMA', 'gris')
    T_.clear(); T_.update(TEMAS[nombre]); globals().update(T_); return T_
tema()

# ---------- piezas ----------
def fx(t_in, inner, style="", cls="", out=None, dy=14, dur=None, extra=""):
    """Elemento HTML que entra con fundido + subida en t_in (y sale seco en out)."""
    o = f' data-out="{out}"' if out is not None else ''
    d = f' data-dur="{dur}"' if dur else ''
    return f'<div class="fx {cls}" data-in="{t_in}"{o}{d} data-dy="{dy}" style="{style}" {extra}>{inner}</div>'
def gfx(t_in, inner, out=None, extra="", dy=0):
    """Grupo SVG que entra en t_in."""
    o = f' data-out="{out}"' if out is not None else ''
    return f'<g data-in="{t_in}"{o} data-dy="{dy}" {extra}>{inner}</g>'
def escena(a, b, *partes):
    """Escena visible entre a y b (segundos). Entra con su primer elemento ya visible."""
    return f'<div class="sc" data-a="{a}" data-b="{b}">' + ''.join(partes) + '</div>'
def svg(*partes, style=''):
    return f'<svg width="1080" height="1920" style="position:absolute;inset:0;{style}" fill="none">' + ''.join(partes) + '</svg>'
def rotulo(x, y, t_in, titulo, sub=None, t_sub=None, size=32, out=None):
    """Rótulo con barra del acento: título en Inter 800 + aclaración en mono."""
    s = f'<div class="mono fx" data-in="{t_sub or t_in}" data-dy="8" style="font-size:28px;color:{GRY};margin-top:10px;line-height:1.35">{sub}</div>' if sub else ''
    return fx(t_in, f'<div class="bar"></div><div><div class="lab" style="font-size:{size}px">{titulo}</div>{s}</div>', f'position:absolute;left:{x}px;top:{y}px', 'tag', out)
def tarjeta(t_in, img, iw, ih, titulo, dato, x=120, y=1180, t_dato=None, out=None, tsize=52):
    """Tarjeta de persona o lugar: foto + nombre en Cal Sans + dato en mono del acento. Franja 1180–1310 por defecto."""
    inner = (f'<img src="img/{img}" style="width:{iw}px;height:{ih}px;object-fit:cover;display:block">'
             f'<div style="display:flex;flex-direction:column;justify-content:center;padding:0 30px 0 2px">'
             f'<div style="font-family:CalSans;font-size:{tsize}px;line-height:1.02;letter-spacing:-1px">{titulo}</div>'
             f'<div class="mono fx" data-in="{t_dato or t_in}" data-dy="8" style="font-size:26px;color:{ACC};margin-top:12px;line-height:1.35">{dato}</div></div>')
    return fx(t_in, inner, f'position:absolute;left:{x}px;top:{y}px', 'card2', out)
def contador(cid, desde, hasta, t0, t1, style, out=None):
    """Número que avanza o retrocede desacelerando (dígitos de ancho fijo)."""
    o = f' data-out="{out}"' if out is not None else ''
    return f'<div class="num" id="{cid}" data-count="{desde},{hasta},{t0},{t1}"{o} style="{style}"></div>'
def palabras(renglones, top, size, lh, t_out=None, ultima_serif=True):
    """Frase-tesis palabra a palabra. renglones: [[(texto, t), ...], ...]. La última palabra va en serif cursiva del acento."""
    html = ''
    for k, line in enumerate(renglones):
        ws = ''
        for j, (tx, t) in enumerate(line):
            last = ultima_serif and k == len(renglones) - 1 and j == len(line) - 1
            st = f'font-family:Serif;font-style:italic;color:{ACC};font-size:{int(size*1.15)}px;letter-spacing:0' if last else ''
            ws += f'<span class="fx w" data-in="{t}" data-dy="18"{(" data-out=%s" % t_out) if t_out else ""} style="{st}">{tx}</span> '
        html += f'<div style="position:absolute;left:120px;right:240px;top:{top + k * lh}px;text-align:center;white-space:nowrap;font-family:CalSans;font-size:{size}px;line-height:1;letter-spacing:-2px">{ws}</div>'
    return html
def grieta(d, t0, t1, w=9, gone=None):
    """Línea quebrada (motivo de lo que se divide) que se dibuja entre t0 y t1."""
    g = f' data-gone="{gone}"' if gone else ''
    return f'<path d="{d}" data-draw="{t0},{t1}"{g} fill="none" stroke="{ACC}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
def trazo(d, t0, t1, w=6, color=None):
    return f'<path d="{d}" data-draw="{t0},{t1}" fill="none" stroke="{color or ACC}" stroke-width="{w}" stroke-linecap="round"/>'
def fuente_biblica(t_in, t_out, texto):
    """■ FUENTE · LIBRO c:v arriba a la izquierda (y ≈ 262). Solo mientras se habla de ese pasaje y solo con contenido cristiano."""
    return fx(t_in, f'<span style="display:inline-block;width:16px;height:16px;background:{ACC};margin-right:14px;vertical-align:1px"></span>{texto}',
              f'position:absolute;left:120px;top:262px;font-size:26px;color:{GRY}', 'mono', out=t_out, dy=6)
def termino(t_in, t_out, palabra, translit, traduccion, idioma='griego', top=640):
    """Término en griego o hebreo como escena propia (verificado en léxicos antes de usarlo)."""
    fam = 'Didot' if idioma == 'griego' else 'Hebreo'
    dirn = 'ltr' if idioma == 'griego' else 'rtl'
    return (fx(t_in, f'<div dir="{dirn}" style="font-family:{fam};font-size:170px;line-height:1.1;color:{ACC}">{palabra}</div>',
               f'position:absolute;left:120px;right:240px;top:{top}px;text-align:center', out=t_out, dy=20)
            + fx(t_in + 0.3, f'<div class="mono" style="font-size:30px;color:{GRY}">{translit} · «{traduccion}»</div>',
                 f'position:absolute;left:120px;right:240px;top:{top + 260}px;text-align:center', out=t_out, dy=8))
def pin(x, y, t_in, grande=False, out=None):
    r = 10 if grande else 7
    return gfx(t_in, f'<circle cx="{x}" cy="{y}" r="{r*3.4}" fill="url(#ptg)"/><circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>', out)

# ---------- subtítulos por bloques (y = 1350) ----------
def subtitulos(bloques):
    """bloques: [(t0, t1, ['renglón 1', 'renglón 2'])]. Palabras clave entre *asteriscos* → complementaria cursiva del acento;
    entre _guiones_ → color del acento con la misma fuente. Cal Sans 41,5 px; primer renglón con su centro en y = 1350."""
    import re
    out = ''
    for t0, t1, lines in bloques:
        html = ''
        for k, l in enumerate(lines):
            l = re.sub(r'\*(.+?)\*', lambda m: f'<span class="comp">{m.group(1)}</span>', l)
            l = re.sub(r'_(.+?)_', lambda m: f'<span style="color:{ACC}">{m.group(1)}</span>', l)
            html += f'<div class="sub" style="top:{1350 - 22 + 44 * k}px">{l}</div>'
        out += f'<div class="subb" data-a="{t0}" data-b="{t1}">{html}</div>'
    return out

# ---------- página ----------
def css():
    return f"""
@font-face{{font-family:'CalSans';src:url('img/CalSans-Regular.ttf')}}
@font-face{{font-family:'Inter';src:url('img/Inter.ttf');font-weight:100 900}}
@font-face{{font-family:'Serif';src:url('img/InstrumentSerif-Italic.ttf');font-style:italic}}
@font-face{{font-family:'Comp';src:url('img/PlayfairDisplay-SemiBoldItalic.ttf');font-style:italic}}
@font-face{{font-family:'Mono';src:url('img/JetBrainsMono.ttf');font-weight:100 800}}
@font-face{{font-family:'Didot';src:url('img/GFSDidot-Regular.ttf')}}
@font-face{{font-family:'Hebreo';src:url('img/FrankRuhlLibre.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:{BG};width:1080px;height:1920px;overflow:hidden}}
#frame{{position:relative;width:1080px;height:1920px;overflow:hidden;color:{TXT};background:{BG}}}
.vig{{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 45%,transparent 55%,rgba(0,0,0,.35) 100%);pointer-events:none}}
.sc{{position:absolute;inset:0;display:none}}
.fx{{opacity:0}} .w{{display:inline-block}}
.mono{{font-family:'Mono';font-weight:500;letter-spacing:.14em;text-transform:uppercase}}
.lab{{font-family:'Inter';font-weight:800;letter-spacing:.16em;text-transform:uppercase}}
.num{{font-family:'CalSans';line-height:1;letter-spacing:-4px}}
.num span{{display:inline-block;width:.58em;text-align:center}}
.tag{{display:flex;gap:18px;align-items:stretch}} .tag .bar{{width:3px;background:{ACC}}}
.card2{{display:flex;gap:28px;align-items:stretch;background:{CARD};border:1px solid rgba(255,255,255,.14);border-radius:22px;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.35)}}
.subb{{position:absolute;inset:0;display:none;pointer-events:none}}
.sub{{position:absolute;left:120px;right:240px;text-align:center;font-family:'CalSans';font-size:41.5px;letter-spacing:-.9px;line-height:44px;color:#fff;
     text-shadow:0 0 10px rgba(0,0,0,.30),0 0 22px rgba(0,0,0,.30);white-space:nowrap}}
.sub .comp{{font-family:'Comp';font-style:italic;font-size:47.3px;color:{ACC}}}
"""
JS = r'''
const ease=p=>1-Math.pow(1-p,3), eio=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2, cl=x=>Math.max(0,Math.min(1,x)), lerp=(a,b,p)=>a+(b-a)*p;
const L=new Map();
function digits(n){return String(n).split('').map(c=>`<span>${c}</span>`).join('')}
function camAt(keys,t){ // keys: [[t,cx,cy,z],...] con interpolación suave y zoom logarítmico
  if(t<=keys[0][0]) return keys[0].slice(1); for(let i=0;i<keys.length-1;i++){const a=keys[i],b=keys[i+1];
   if(t<b[0]){const p=eio(cl((t-a[0])/(b[0]-a[0]))); return [lerp(a[1],b[1],p),lerp(a[2],b[2],p),Math.exp(lerp(Math.log(a[3]),Math.log(b[3]),p))];}}
  return keys[keys.length-1].slice(1);}
window.render=function(t){
 document.querySelectorAll('.sc,.subb').forEach(s=>{s.style.display=(t>=+s.dataset.a&&t<+s.dataset.b)?'block':'none'});
 document.querySelectorAll('[data-in]').forEach(e=>{const a=+e.dataset.in,o=e.dataset.out?+e.dataset.out:1e9;
   if(t<a||t>=o){e.style.opacity=0;return}
   const p=ease(cl((t-a)/(+(e.dataset.dur||.33)))); e.style.opacity=p; const dy=+(e.dataset.dy||14); e.style.translate=`0px ${((1-p)*dy).toFixed(2)}px`;});
 document.querySelectorAll('[data-draw]').forEach(e=>{const [a,b]=e.dataset.draw.split(',').map(Number);
   if(!L.has(e))L.set(e,e.getTotalLength()); const len=L.get(e); const p=eio(cl((t-a)/(b-a)));
   e.style.strokeDasharray=`${len} ${len}`; e.style.strokeDashoffset=len*(1-p); e.style.opacity=t<a?0:1;});
 document.querySelectorAll('[data-gone]').forEach(e=>{const a=+e.dataset.gone; if(t>=a) e.style.opacity=1-ease(cl((t-a)/.35));});
 document.querySelectorAll('[data-count]').forEach(e=>{const [f,to,a,b]=e.dataset.count.split(',').map(Number);
   const o=e.dataset.out?+e.dataset.out:1e9; const vis=t>=a-0.25&&t<o; e.style.opacity=vis?ease(cl((t-(a-0.25))/.25)):0;
   const p=1-Math.pow(1-cl((t-a)/(b-a)),2.4); e.innerHTML=digits(Math.round(f+(to-f)*p));});
 document.querySelectorAll('[data-cam]').forEach(e=>{const k=JSON.parse(e.dataset.cam); const c=camAt(k,t); const Y=+(e.dataset.camy||860);
   e.style.transform=`translate(${540-c[0]*c[2]}px,${Y-c[1]*c[2]}px) scale(${c[2]})`;});
 const fin=window.FIN||1e9; const fo=document.getElementById('fundido'); if(fo) fo.style.opacity=cl((t-(fin-1.1))/0.6);
 if(window.extra) window.extra(t);
};
'''
def pagina(escenas, subs=(), fin=None, js_extra=''):
    """Arma el HTML completo. fin: duración del video (el último segundo se funde a negro)."""
    f = f'window.FIN={fin};' if fin else ''
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{css()}</style></head><body><div id="frame">'
            + ''.join(escenas) + subtitulos(list(subs))
            + '<div class="vig"></div><div id="fundido" style="position:absolute;inset:0;background:#000;opacity:0"></div></div>'
            + f'<script>{f}{JS}{js_extra}</script></body></html>')
