#!/usr/bin/env python3
"""Superpone la zona segura unificada (Instagram + TikTok) sobre un fotograma 1080×1920 para revisarlo.

Zona libre: y 250–1540 · x ≥ 120 · hasta y = 720: x ≤ 950 · desde y = 720: x ≤ 840 (columna de botones).
Detalle en references/zona-segura.md.
Uso: python3 zona_segura.py fotograma.png salida.jpg [--plantilla ruta/zona_segura_9x16.png]
"""
import argparse, os
from PIL import Image, ImageDraw

TOP, BOT, LEFT, RIGHT_UP, COL_Y, COL_X = 250, 1540, 120, 950, 720, 840


def dentro(x0, y0, x1, y1):
    """True si la caja (x0, y0, x1, y1) en px de 1080×1920 queda dentro de la zona segura."""
    if y0 < TOP or y1 > BOT or x0 < LEFT:
        return False
    lim = RIGHT_UP if y1 <= COL_Y else COL_X
    return x1 <= lim


def plantilla():
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im); m = (42, 46, 60, 200)
    d.rectangle([0, 0, 1080, TOP - 1], fill=m); d.rectangle([0, BOT, 1080, 1920], fill=m)
    d.rectangle([0, TOP, LEFT - 1, BOT - 1], fill=m); d.rectangle([RIGHT_UP, TOP, 1080, COL_Y - 1], fill=m)
    d.rectangle([COL_X, COL_Y, 1080, BOT - 1], fill=m)
    d.line([(LEFT, TOP), (RIGHT_UP, TOP), (RIGHT_UP, COL_Y), (COL_X, COL_Y), (COL_X, BOT), (LEFT, BOT), (LEFT, TOP)],
           fill=(255, 236, 0, 255), width=4)
    return im


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('entrada'); ap.add_argument('salida'); ap.add_argument('--plantilla')
    a = ap.parse_args()
    base = Image.open(a.entrada).convert('RGBA').resize((1080, 1920))
    ov = Image.open(a.plantilla).convert('RGBA') if a.plantilla and os.path.exists(a.plantilla) else plantilla()
    base.alpha_composite(ov); base.convert('RGB').save(a.salida, quality=92); print(a.salida)


if __name__ == '__main__':
    main()
