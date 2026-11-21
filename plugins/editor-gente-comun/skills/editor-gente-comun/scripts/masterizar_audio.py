#!/usr/bin/env python3
"""Deja el audio de un video en el estándar del editor sin tocar la imagen.

  −14 LUFS integrados · pico verdadero ≤ −1 dBTP · AAC 48 kHz estéreo · video copiado tal cual

Método (lección aprendida): ganancia fija + limitador, nunca el modo dinámico de loudnorm (bombea el ruido).
El limitador trabaja sobremuestreado ×4 para controlar los picos entre muestras.
Uso: python3 masterizar_audio.py <entrada.mp4> <salida.mp4> [--tp -1.5]   (clips de predicaciones: --tp -1.5)
"""
import json, re, subprocess, sys

OBJ_I, OBJ_TP = -14.0, -1.0


def medir(path):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-map', '0:a:0', '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    resumen = err[err.rfind('Summary:'):]
    i = float(re.search(r'I:\s+(-?[\d.]+) LUFS', resumen).group(1))
    tp = float(re.search(r'Peak:\s+(-?[\d.]+|-inf) dBFS', resumen).group(1))
    return i, tp


def procesar(src, dst, gain, techo):
    filtro = (f'volume={gain:.2f}dB,aresample=192000,'
              f'alimiter=limit={10 ** (techo / 20):.4f}:attack=1:release=60:level=disabled,'
              'aresample=48000')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', src, '-map', '0:v:0', '-map', '0:a:0',
                    '-c:v', 'copy', '-af', filtro, '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-ac', '2',
                    '-movflags', '+faststart', dst], check=True)


def main():
    global OBJ_TP
    args = sys.argv[1:]
    if '--tp' in args:
        k = args.index('--tp'); OBJ_TP = float(args[k + 1]); del args[k:k + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    src, dst = args
    i0, tp0 = medir(src)
    print(f'Entrada: {i0:.1f} LUFS · pico {tp0:+.1f} dBTP')
    gain, techo = OBJ_I - i0, OBJ_TP - 0.5
    for intento in range(3):
        procesar(src, dst, gain, techo)
        i1, tp1 = medir(dst)
        print(f'Intento {intento + 1}: ganancia {gain:+.1f} dB → {i1:.1f} LUFS · pico {tp1:+.1f} dBTP')
        if abs(i1 - OBJ_I) <= 0.5 and tp1 <= OBJ_TP + 0.05:
            break
        gain += OBJ_I - i1                      # el limitador se come algo de volumen: compensar
        if tp1 > OBJ_TP: techo -= (tp1 - OBJ_TP) + 0.2
    ok = abs(i1 - OBJ_I) <= 0.5 and tp1 <= OBJ_TP + 0.05
    print(('LISTO' if ok else 'REVISAR') + f': {dst} · {i1:.1f} LUFS · pico {tp1:+.1f} dBTP · 48 kHz')
    print('Escuchar: que los whooshes y la voz no suenen aplastados después del limitador.')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
