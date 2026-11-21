# Figuras tipo pictograma (trazo grueso redondeado + cabeza llena). Origen = pies; arriba es negativo.
C = '#F3F3EF'
def _g(body, color=C):
    return f'<g fill="none" stroke="{color}" stroke-linecap="round" stroke-linejoin="round">{body}</g>'
def orando(color=C):   # arrodillado de perfil, manos juntas en alto, mirando a la derecha
    return _g(f'''
 <circle cx="40" cy="-300" r="34" fill="{color}" stroke="none"/>
 <path d="M18,-246 C8,-206 -14,-166 -30,-118" stroke-width="40"/>
 <path d="M-30,-118 L44,-30" stroke-width="32"/>
 <path d="M44,-24 L-78,-18" stroke-width="28"/>
 <path d="M16,-232 L70,-196 L98,-268" stroke-width="22"/>
 <path d="M98,-268 L106,-312" stroke-width="16"/>''', color)
def martillando(color=C, banco='#7D8794'):   # de pie, de perfil a la derecha, martillo en alto
    return _g(f'''
 <path d="M80,-250 H236" stroke="{banco}" stroke-width="14"/><path d="M96,-250 V-6 M220,-250 V-6" stroke="{banco}" stroke-width="12"/>
 <circle cx="-6" cy="-414" r="34" fill="{color}" stroke="none"/>
 <path d="M-12,-360 C-16,-310 -18,-268 -20,-214" stroke-width="42"/>
 <path d="M-22,-210 L-56,-14" stroke-width="30"/><path d="M-18,-210 L24,-14" stroke-width="30"/>
 <path d="M-8,-340 L40,-290 L104,-268" stroke-width="22"/>
 <path d="M-12,-346 L-62,-410 L-40,-474" stroke-width="22"/>
 <path d="M-40,-474 L-6,-530" stroke="{color}" stroke-width="12"/>
 <path d="M-34,-552 L26,-516" stroke="{color}" stroke-width="30" stroke-linecap="butt"/>
 <path d="M120,-266 h46" stroke="{banco}" stroke-width="8"/>''', color)
def sosteniendo(color=C):   # de frente, brazos arriba
    return _g(f'''
 <circle cx="0" cy="-330" r="34" fill="{color}" stroke="none"/>
 <path d="M0,-276 V-150" stroke-width="46"/>
 <path d="M-8,-146 L-46,-14" stroke-width="30"/><path d="M8,-146 L46,-14" stroke-width="30"/>
 <path d="M-14,-264 L-76,-322 L-86,-404" stroke-width="22"/><path d="M14,-264 L76,-322 L86,-404" stroke-width="22"/>''', color)
def tarima(color='#7D8794'):
    return f'<path d="M-200,-424 H200" stroke="{color}" stroke-width="22" stroke-linecap="round" fill="none"/>'
def distinto(color='#F6F6A8'):
    return f'<g stroke="{color}" stroke-width="16" stroke-linecap="round" fill="none"><path d="M-62,-22 H62 M-62,22 H62"/><path class="slash" d="M30,-70 L-30,70"/></g>'
def sosteniendo2(color=C):   # de frente, rodillas algo flexionadas, brazos firmes hasta la tarima (manos en y=-412)
    return _g(f'''
 <circle cx="0" cy="-322" r="34" fill="{color}" stroke="none"/>
 <path d="M0,-268 C2,-230 2,-190 0,-150" stroke-width="48"/>
 <path d="M-10,-146 L-44,-82 L-54,-14" stroke-width="30"/><path d="M10,-146 L44,-82 L54,-14" stroke-width="30"/>
 <path d="M-20,-258 L-66,-300 L-74,-404" stroke-width="22"/><path d="M20,-258 L66,-300 L74,-404" stroke-width="22"/>
 <path d="M-90,-408 h32 M58,-408 h32" stroke-width="16"/>''', color)
def tarima2(color='#8A94A1'):
    return (f'<g><rect x="-210" y="-448" width="420" height="34" rx="10" fill="{color}"/>'
            f'<path d="M-196,-438 H196" stroke="#A7B0BB" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M-120,-426 h70 M30,-426 h90" stroke="#6E7884" stroke-width="3" stroke-linecap="round"/></g>')
def grieta_v(x=540, y0=440, y1=1060, seed=5, amp=30):
    import random
    r = random.Random(seed); pts = [f"M{x},{y0}"]; y = y0; side = 1
    while y < y1 - 40:
        y += r.uniform(38, 78); side = -side
        pts.append(f"L{x + side * r.uniform(amp * 0.35, amp):.0f},{min(y, y1):.0f}")
    pts.append(f"L{x + r.uniform(-8, 8):.0f},{y1}")
    return " ".join(pts)
def grieta_h(y=0, x0=-230, x1=230, seed=9, amp=22):
    import random
    r = random.Random(seed); pts = [f"M{x0},{y}"]; x = x0; side = 1
    while x < x1 - 30:
        x += r.uniform(30, 60); side = -side
        pts.append(f"L{min(x, x1):.0f},{y + side * r.uniform(amp * 0.35, amp):.0f}")
    return " ".join(pts)
