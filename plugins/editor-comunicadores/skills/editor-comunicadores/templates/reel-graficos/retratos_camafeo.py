# Ilustraciones evocativas tipo "silueta de camafeo" (no son retratos fieles).
PERFIL=("M118 262 C100 246 88 214 88 182 C88 128 122 88 172 86 C200 85 214 100 220 120 "
        "C223 132 224 140 222 148 C228 158 236 166 240 174 C241 178 236 181 228 182 "
        "C228 186 229 189 231 192 C229 195 225 196 225 198 C228 200 230 203 229 206 "
        "C234 214 234 232 222 244 C212 252 200 252 192 254 C190 262 192 270 194 276 "
        "C220 284 246 300 256 320 L262 360 L58 360 L64 316 C76 292 98 276 118 262 Z")
def retrato(kind, ink='#2A211B', paper='#EFE4CC', w=300, h=360, uid=''):
    i=kind+uid
    ring=f'''<ellipse cx="150" cy="180" rx="140" ry="170" fill="{paper}"/>
<ellipse cx="150" cy="180" rx="128" ry="158" fill="none" stroke="{ink}" stroke-width="1.6" opacity=".5"/>'''
    capline=f'<path d="M98 150 C108 118 140 104 184 108 C198 109 210 112 219 118" fill="none" stroke="{paper}" stroke-width="2.4" opacity=".75"/>'
    if kind=='bandas':
        extra=(f'<path d="M196 262 L212 266 L210 306 L196 304 Z" fill="{paper}"/>'
               f'<path d="M214 268 L230 274 L224 312 L210 308 Z" fill="{paper}"/>')
    else:
        pts=[]
        import math
        cx,cy,rx,ry=184,268,62,20
        d=''
        n=14
        for k in range(n+1):
            a=math.pi*2*k/n
            x=cx+rx*math.cos(a); y=cy+ry*math.sin(a)
            d+=('M' if k==0 else 'L')+f'{x:.1f} {y:.1f} '
        pleats=''.join(f'<path d="M{cx+rx*0.9*math.cos(math.pi*2*k/n):.1f} {cy+ry*0.9*math.sin(math.pi*2*k/n):.1f} L{cx+rx*0.35*math.cos(math.pi*2*k/n):.1f} {cy+ry*0.35*math.sin(math.pi*2*k/n):.1f}" stroke="{ink}" stroke-width="1.6" opacity=".55"/>' for k in range(n))
        scal=''.join(f'<circle cx="{cx+rx*math.cos(math.pi*2*k/n):.1f}" cy="{cy+ry*math.sin(math.pi*2*k/n):.1f}" r="7.5" fill="{paper}"/>' for k in range(n))
        extra=f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{paper}"/>{scal}{pleats}'
    return (f'<svg viewBox="0 0 300 360" width="{w}" height="{h}">{ring}<clipPath id="cl{i}"><ellipse cx="150" cy="180" rx="128" ry="158"/></clipPath>'
            f'<g clip-path="url(#cl{i})"><path d="{PERFIL}" fill="{ink}"/>{capline}{extra}</g></svg>')
if __name__=='__main__':
    open('retratos_test.html','w').write('<body style="background:rgba(20,16,14,1);display:flex;gap:40px;padding:40px">'+retrato('bandas')+retrato('gola')+'</body>')
