# Auditoría de zona segura sobre el HTML del reel (render(t)): mide la tinta real de cada texto visible y las cajas de fotos y tarjetas,
# cada 0,25 s, contra la zona segura unificada IG + TikTok (references/zona-segura.md): arriba 250 · abajo 1540 · izquierda 120 · derecha 950 hasta y = 720 y 840 desde ahí (columna de botones).
# Uso: python3 auditoria_zona.py reel.html <duración_s>
import sys
from playwright.sync_api import sync_playwright
JS = r"""() => { const out=[]; const vis=el=>{let o=1,e=el; while(e&&e.nodeType===1){const cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden')return 0; o*=parseFloat(cs.opacity); e=e.parentElement;} return o;};
  const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT); let n;
  while(n=w.nextNode()){ if(!n.textContent.trim())continue; const p=n.parentElement; if(p.closest('script,style'))continue; const o=vis(p); if(o<0.08)continue;
    const r=document.createRange(); r.selectNodeContents(n); for(const q of r.getClientRects()){ if(q.width<2)continue; out.push({t:n.textContent.trim().slice(0,30),x0:q.left,x1:q.right,y0:q.top,y1:q.bottom}); } }
  document.querySelectorAll('.photo,.card').forEach(e=>{ if(vis(e)<0.08)return; const q=e.getBoundingClientRect(); out.push({t:'['+e.className+']',x0:q.left,x1:q.right,y0:q.top,y1:q.bottom}); });
  return out; }"""
html, dur = sys.argv[1], float(sys.argv[2]); viol = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files']); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto(f'file://{html}'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500); t = 0.0
    while t < dur:
        pg.evaluate(f'render({t})')
        for it in pg.evaluate(JS):
            r = []
            if it['y0'] < 250: r.append('arriba')
            if it['y1'] > 1540: r.append('abajo')
            if it['x0'] < 120 and it['x1'] > 0: r.append('izq')
            lim = 950 if it['y1'] <= 720 else 840
            if it['x1'] > lim and it['x0'] < 1080: r.append(f'der>{lim}')
            if r: viol.setdefault((it['t'], tuple(r)), []).append(round(t, 2))
        t += 0.25
    b.close()
for (txt, r), v in sorted(viol.items(), key=lambda kv: kv[1][0]): print(f'{v[0]:6.2f}–{v[-1]:6.2f}  {r}  «{txt}»')
print('OK' if not viol else f'{len(viol)} elementos fuera de la zona segura (los que salen de cuadro en un viaje de cámara no cuentan)')
