# Zona segura para las secuencias 3D (seq/<nombre>/*.jpg): cuenta los píxeles del objeto (luz > 30) fuera de la zona segura unificada IG + TikTok (references/zona-segura.md).
# Uso: python3 auditoria_3d.py seq/biblia seq/iglesia seq/altar
import glob, sys, numpy as np
from PIL import Image
Y, X = np.mgrid[0:1920:2, 0:1080:2]
fuera = (Y < 250) | (Y > 1540) | (X < 120) | ((Y <= 720) & (X > 950)) | ((Y > 720) & (X > 840))
for d in sys.argv[1:]:
    peor = (0, '')
    for f in sorted(glob.glob(f'{d}/*.jpg'))[::2]:
        a = np.array(Image.open(f).convert('L').resize((540, 960))).astype(int); c = int(((a > 30) & fuera).sum())
        if c > peor[0]: peor = (c, f)
    print(d, 'OK' if not peor[0] else f'{peor[0]} píxeles fuera (peor cuadro {peor[1]})')
