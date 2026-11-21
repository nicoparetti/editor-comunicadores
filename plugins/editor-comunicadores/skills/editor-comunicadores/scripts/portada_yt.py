#!/usr/bin/env python3
"""Generador de portadas YouTube.

Uso:
  python3 portada_yt.py fondo.jpg --titulo "¡QUE|VALGA|LA PENA!" \
      --encabezado "Enseñanza|completa" --extra "3 claves" \
      --lado auto --color auto --salida portada.jpg
  '|' = salto de línea manual (en título y encabezado).
Fuentes: Anton y Poppins Medium, en 4_Recursos/fuentes (o $EDITOR_FUENTES).
"""
import argparse, colorsys, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H = 1280, 720
M = 60                       # margen de seguridad
BRAND_RED = tuple(int(os.environ.get('COLOR_MARCA', '#B8442E').lstrip('#')[i:i+2], 16) for i in (0, 2, 4))   # color de marca del perfil
TEXT = (252, 240, 236)       # blanco cálido del título (se cambia con --color-texto)
SMALL_TEXT = (255, 255, 255)
HERE = os.path.dirname(os.path.abspath(__file__))
FUENTES = os.environ.get("EDITOR_FUENTES", os.path.join(HERE, "..", "..", "4_Recursos", "fuentes"))


def _font(*cands):
    for c in cands:
        if os.path.exists(c):
            return c
    raise SystemExit(f"Falta tipografía: {cands[0]}")


F_TITLE = _font(os.path.join(FUENTES, "Anton-Regular.ttf"), os.path.join(HERE, "fonts", "Anton-Regular.ttf"),
                "/usr/share/fonts/truetype/google-fonts/Anton-Regular.ttf")
F_SMALL = _font(os.path.join(FUENTES, "Poppins-Medium.ttf"), "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf",
                os.path.join(HERE, "fonts", "Poppins-Medium.ttf"))


# ---------- fondo ----------
def cover(img, focus=(0.5, 0.5), zoom=1.0):
    img = ImageOps.exif_transpose(img).convert("RGB")
    s = max(W / img.width, H / img.height) * zoom
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = int((img.width - W) * focus[0]); y = int((img.height - H) * focus[1])
    return img.crop((x, y, x + W, y + H))


def auto_side(img):
    """Lado con menos detalle (bordes) = donde va el fade y el título."""
    e = np.asarray(img.convert("L").filter(ImageFilter.FIND_EDGES), dtype=float)
    third_w, third_h = W // 3, H // 3
    scores = {"izquierda": e[:, :third_w].mean(), "derecha": e[:, -third_w:].mean(),
              "arriba": e[:third_h].mean() * 1.25, "abajo": e[-third_h:].mean() * 1.25}
    return min(scores, key=scores.get)  # penaliza arriba/abajo: el título vertical rinde más


def auto_color(img):
    """Color dominante saturado de la imagen, normalizado a la intensidad de la marca."""
    a = np.asarray(img.resize((160, 90)), dtype=float) / 255
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in a.reshape(-1, 3)])
    sat = hsv[(hsv[:, 1] > 0.35) & (hsv[:, 2] > 0.25)]
    if len(sat) < 0.12 * len(hsv):              # menos del 12 % con color fuerte = imagen neutra
        # imagen neutra/gris: el rojo no combina; tono oscuro sacado de las sombras de la foto
        dark = hsv[(hsv[:, 2] < 0.45) & (hsv[:, 1] > 0.08)]
        if len(dark) < 50:
            return (46, 42, 45)                       # grafito
        ang = dark[:, 0] * 2 * np.pi
        h = (np.arctan2(np.sin(ang).mean(), np.cos(ang).mean()) / (2 * np.pi)) % 1
        r, g, b = colorsys.hsv_to_rgb(h, 0.55, 0.32)
        return tuple(int(c * 255) for c in (r, g, b))
    hist, edges = np.histogram(sat[:, 0], bins=24, range=(0, 1), weights=sat[:, 1])
    h = (edges[hist.argmax()] + edges[hist.argmax() + 1]) / 2
    r, g, b = colorsys.hsv_to_rgb(h, 0.80, 0.84)
    return tuple(int(c * 255) for c in (r, g, b))


def grade(img, color, amount=0.28, sat=0.75, warm=0.0):
    """Uniformiza: baja saturación, levanta negros (look film), tiñe con el color y agrega grano."""
    a = np.asarray(img, dtype=float) / 255
    lum = a @ [0.299, 0.587, 0.114]
    a = a * sat + lum[..., None] * (1 - sat)             # sat<1 desatura, >1 satura
    a = 0.06 + a * 0.90                                    # negros levantados, contraste suave
    if warm:                                               # empuja hacia lo cálido (ámbar)
        a = a * np.array([1 + 0.10 * warm, 1 + 0.03 * warm, 1 - 0.12 * warm])
    c = np.array(color) / 255
    tint = np.where(a < 0.5, 2 * a * c, 1 - 2 * (1 - a) * (1 - c))  # overlay
    a = a * (1 - amount) + tint * amount
    a += np.random.normal(0, 0.022, a.shape[:2])[..., None]          # grano
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype("uint8"))


def fade(img, color, side, solid=0.28, end=0.68):
    """Degradé desde un lado: sólido hasta `solid`, se desvanece hasta `end` (fracción del lado)."""
    n = W if side in ("izquierda", "derecha") else H
    t = np.linspace(0, 1, n)
    alpha = np.clip((end - t) / (end - solid), 0, 1)
    alpha = alpha ** 1.6 * 0.97 + 0.0                    # caída suave
    alpha[t < solid] = 0.97
    if side in ("derecha", "abajo"):
        alpha = alpha[::-1]
    mask = np.tile(alpha, (H, 1)) if n == W else np.tile(alpha[:, None], (1, W))
    m = Image.fromarray((mask * 255).astype("uint8"))
    return Image.composite(Image.new("RGB", (W, H), color), img, m)


# ---------- texto ----------
def cap_h(font):
    bb = font.getbbox("H", anchor="ls")
    return -bb[1]


ACC = set("ÁÉÍÓÚÜÑ")


def pitches(font, lines, gap=1.13):
    """Distancia entre líneas de base; suma aire si la línea siguiente lleva tilde/eñe para que no choque."""
    ch = cap_h(font)
    acc_extra = (-font.getbbox("Í", anchor="ls")[1]) - ch + ch * 0.04
    return [ch * gap + (acc_extra if ACC & set(lines[i + 1]) else 0) for i in range(len(lines) - 1)]


def fit_title(lines, box_w, box_h, gap=1.13):
    size = 190                                   # tope: títulos de 3–4 líneas como en las referencias
    while size > 40:
        f = ImageFont.truetype(F_TITLE, size)
        widths = [f.getbbox(l, anchor="ls")[2] - f.getbbox(l, anchor="ls")[0] for l in lines]
        total_h = cap_h(f) + sum(pitches(f, lines, gap))
        if max(widths) <= box_w and total_h <= box_h:
            return f, size
        size -= 4
    return ImageFont.truetype(F_TITLE, size), size


def textured_text_layer(lines, font, size, align, box, gap=1.13):
    """Título con textura de ruido (look serigrafía) en capa RGBA. Interlineado por línea de base."""
    x0, y0, x1, y1 = box
    layer = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(layer)
    ps = pitches(font, lines, gap)
    base = y1 - sum(ps)                                # anclado abajo, como las referencias
    for i, l in enumerate(lines):
        bb = font.getbbox(l, anchor="ls")
        w = bb[2] - bb[0]
        if align == "derecha":   x = x1 - w - bb[0]
        elif align == "centro":  x = x0 + (x1 - x0 - w) / 2 - bb[0]
        else:                    x = x0 - bb[0]
        d.text((x, base), l, font=font, fill=255, anchor="ls")
        base += ps[i] if i < len(ps) else 0
    noise = (np.random.rand(H, W) > 0.10).astype(float) * 0.18 + 0.80
    a = np.asarray(layer, dtype=float) * noise
    rgba = Image.new("RGBA", (W, H), TEXT + (0,))
    rgba.putalpha(Image.fromarray(a.clip(0, 255).astype("uint8")))
    return rgba


def small(draw, xy, text, anchor_right=False, size=25):
    f = ImageFont.truetype(F_SMALL, size)
    lines = text.split("|")
    x, y = xy
    for l in lines:
        w = draw.textlength(l, font=f)
        draw.text((x - w if anchor_right else x, y), l, font=f, fill=SMALL_TEXT)
        y += size * 1.05


def pill(canvas, text, color, x_center, y_bottom, vertical=True):
    f = ImageFont.truetype(F_SMALL, 22)
    tw = int(ImageDraw.Draw(canvas).textlength(text, font=f))
    pw, ph = tw + 44, 38
    p = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(p)
    d.rounded_rectangle((0, 0, pw - 1, ph - 1), radius=ph // 2, fill=color + (255,))
    d.text((pw / 2, ph / 2 + 1), text, font=f, fill=(255, 255, 255), anchor="mm")
    if vertical:
        p = p.rotate(90, expand=True)                   # se lee de abajo hacia arriba
    canvas.alpha_composite(p, (int(x_center - p.width / 2), int(y_bottom - p.height)))


def hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------- composición ----------
def build(a):
    bg = Image.open(a.fondo)
    focus = tuple(float(v) for v in a.foco.split(","))
    img = cover(bg, focus, a.zoom)
    side = auto_side(img) if a.lado == "auto" else a.lado
    color = auto_color(img) if a.color == "auto" else (
        BRAND_RED if a.color == "marca" else tuple(int(a.color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)))

    global TEXT, SMALL_TEXT
    if a.color_texto:
        TEXT = SMALL_TEXT = hex2rgb(a.color_texto)
    img = grade(img, color, a.tinte, a.saturacion, a.calidez)
    img = fade(img, color, side, a.fade_solido, a.fade_fin)
    canvas = img.convert("RGBA")
    d = ImageDraw.Draw(canvas)

    lines = [l.strip() for l in a.titulo.upper().split("|")]
    top = M + 70                                          # deja aire a encabezado/nombre
    if side in ("izquierda", "derecha"):
        bw = int(W * a.ancho)
        box = (M, top, M + bw, H - M) if side == "izquierda" else (W - M - bw, top, W - M, H - M)
        align = side
    else:
        box = (M, top, W - M, H // 2 + 40) if side == "arriba" else (M, H // 2 - 20, W - M, H - M)
        align = "izquierda"
    font, size = fit_title(lines, box[2] - box[0], box[3] - box[1])
    canvas.alpha_composite(textured_text_layer(lines, font, size, align, box))

    # nombre en la esquina superior del lado del fade; encabezado en la opuesta
    name_right = side == "derecha"
    small(d, (W - M if name_right else M, M - 6), a.nombre, anchor_right=name_right, size=26)
    if a.encabezado:
        small(d, (M if name_right else W - M, M - 6), a.encabezado, anchor_right=not name_right, size=26)

    if a.extra:  # píldora vertical abajo, del lado de la imagen
        x = (W - M - 19) if side == "izquierda" else (M + 19)
        pill(canvas, a.extra, color, x, H - M + 5)

    out = canvas.convert("RGB")
    q = 95
    while True:                                           # YouTube: ≤2 MB
        out.save(a.salida, "JPEG", quality=q, optimize=True, subsampling=0)
        if os.path.getsize(a.salida) < 2_000_000 or q <= 70:
            break
        q -= 5
    print(f"OK {a.salida} | {W}x{H} | lado={side} | color=#{'%02X%02X%02X' % color} | "
          f"{os.path.getsize(a.salida) // 1024} KB")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("fondo")
    p.add_argument("--titulo", required=True)
    p.add_argument("--encabezado", default="")
    p.add_argument("--nombre", default="", help="nombre que aparece en la portada (del perfil)")
    p.add_argument("--extra", default="")
    p.add_argument("--lado", default="auto", choices=["auto", "izquierda", "derecha", "arriba", "abajo"])
    p.add_argument("--color", default="auto", help="auto | marca | #RRGGBB")
    p.add_argument("--foco", default="0.5,0.5", help="encuadre x,y 0–1 al recortar a 16:9")
    p.add_argument("--tinte", type=float, default=0.18)
    p.add_argument("--ancho", type=float, default=0.56, help="ancho del bloque de título (fracción)")
    p.add_argument("--zoom", type=float, default=1.0, help="acercar la foto (1.0 = sin zoom)")
    p.add_argument("--fade-solido", dest="fade_solido", type=float, default=0.28)
    p.add_argument("--fade-fin", dest="fade_fin", type=float, default=0.68)
    p.add_argument("--saturacion", type=float, default=0.75, help="1.0 = original")
    p.add_argument("--calidez", type=float, default=0.0, help="0–1, empuja la foto hacia tonos cálidos")
    p.add_argument("--color-texto", dest="color_texto", default="", help="#RRGGBB; usar oscuro si el fade es claro")
    p.add_argument("--salida", default="portada.jpg")
    random.seed(7); np.random.seed(7)
    build(p.parse_args())
