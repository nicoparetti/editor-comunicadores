# Lámina del storyboard: 6 cuadros con tiempo, frase y nota (punto de control antes de hacer el video).
# Uso: python3 lamina.py storyboard.json salida.jpg
#   storyboard.json = {"titulo": "...", "subtitulo": "...", "cuadros": [{"img": "c1.png", "tiempo": "0:03", "frase": "...", "nota": "..."}, ...]}
# Fuentes: CalSans-Regular.ttf, JetBrainsMono.ttf e Inter.ttf en img/ (o variable FUENTES).
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

F = os.environ.get('FUENTES', 'img') + '/'
cfg = json.load(open(sys.argv[1]))
C = cfg['cuadros']
fT = ImageFont.truetype(F + 'CalSans-Regular.ttf', 60); fM = ImageFont.truetype(F + 'JetBrainsMono.ttf', 20)
fB = ImageFont.truetype(F + 'Inter.ttf', 24); fS = ImageFont.truetype(F + 'Inter.ttf', 20)
cols = 3 if len(C) > 4 else len(C)
rows = (len(C) + cols - 1) // cols
w, h = 420, 747; pad = 50; gap = 34; txt = 150
W = pad * 2 + cols * w + (cols - 1) * gap
H = 190 + rows * (h + txt + gap) + pad
s = Image.new('RGB', (W, H), (24, 27, 32)); d = ImageDraw.Draw(s)
d.text((pad, 40), cfg.get('titulo', 'Storyboard'), font=fT, fill=(242, 242, 238))
d.text((pad, 118), cfg.get('subtitulo', ''), font=fM, fill=(150, 156, 164))
def wrap(t, font, maxw):
    out, line = [], ''
    for word in t.split():
        test = (line + ' ' + word).strip()
        if d.textlength(test, font=font) <= maxw: line = test
        else: out.append(line); line = word
    return out + ([line] if line else [])
for k, c in enumerate(C):
    x = pad + (k % cols) * (w + gap); y = 190 + (k // cols) * (h + txt + gap)
    s.paste(Image.open(c['img']).convert('RGB').resize((w, h)), (x, y))
    d.text((x, y + h + 12), f"{k + 1:02d} · {c.get('tiempo', '')}", font=fM, fill=(150, 156, 164))
    yy = y + h + 42
    for l in wrap('«' + c.get('frase', '') + '»', fB, w)[:2]: d.text((x, yy), l, font=fB, fill=(242, 242, 238)); yy += 30
    for l in wrap(c.get('nota', ''), fS, w)[:2]: d.text((x, yy), l, font=fS, fill=(150, 156, 164)); yy += 26
s.save(sys.argv[2], quality=90); print(s.size)
