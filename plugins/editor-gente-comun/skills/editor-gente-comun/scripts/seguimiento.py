#!/usr/bin/env python3
"""Encuadre vertical 9:16 que sigue al predicador, con el método probado en clips de prédica aprobados (oct-nov 2026),
más un control antitemblor que impide entregar un recorte que vibra. NO reprogramar el seguimiento a mano: usar esto.

Uso (en la computadora de la persona, con el entorno cargado; corre en tramos de ≤150 s y es reanudable):
  python3 .herramientas/scripts/seguimiento.py detectar ORIGINAL --desde 2781.5 --hasta 2799 --carpeta trabajo/seg_A
  python3 .herramientas/scripts/seguimiento.py recorrido trabajo/seg_A [--modo auto|seguir|quieto]
  python3 .herramientas/scripts/seguimiento.py control trabajo/seg_A
Si `detectar` dice SIGUE, se vuelve a correr igual. `recorrido` hace también el control y escribe:
  recorrido.json  x del recorte por cuadro (px de la imagen de alto 2160), planos, modo, ampliación, acercamiento base
  cmd.txt         comandos de sendcmd, uno por cuadro con cambio, adelantados medio cuadro (evita el cuadro de retraso)
  filtro.txt      el filtro de FFmpeg listo:  [scale a alto 2160,]sendcmd=f=cmd.txt,crop@c=1216:2160:X0:0:exact=1,scale=1080:1920
  control.txt     resultado del control antitemblor (APROBADO / NO APROBADO y por qué)

Método (clips-de-predicaciones.md §3):
- Detección con YuNet en CADA cuadro, sobre una copia de 960 px de ancho; solo caras de la mitad superior.
- Cambio de cámara: histograma HSV, distancia de Bhattacharyya > 0,3. Nunca se suaviza a través de un cambio.
- En cada plano: primero la cara más grande; después la más cercana a la anterior; se descartan saltos > 0,12 del ancho;
  los huecos se interpolan cuadro a cuadro.
- Ampliación = 1080 / ancho del recorte en el original (4K: 1215 px → 0,89, se achica; Full HD: 608 px → 1,78, se amplía).
  Si el original es menor que 4K, se agranda a alto 2160 ANTES de recortar: el recorte se mueve de a 1 px de 4K.
- Modo "seguir" (el de los clips aprobados): suavizado ida y vuelta con coeficiente 0,25 y movimiento en cada cuadro.
- Modo "quieto" (para originales que se amplían): el recorte queda fijo mientras la cara esté en la zona central;
  si sale, se mueve con aceleración y frenado (0,6–1,5 s), cuadro a cuadro; mientras la cámara original panea, espera.
- "auto": seguir si la ampliación es ≤ 1 y el control aprueba; si no, quieto.
Necesita OpenCV (cv2) con FaceDetectorYN, numpy, ffmpeg/ffprobe y el modelo face_detection_yunet_2023mar.onnx.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

PROXY_W = 960
LIMITE_S = 150
SALIDA_W, SALIDA_H = 1080, 1920
# Umbrales del control, calibrados con clips de prédica aprobados y un recorrido "a saltos" (el error de la detección cada 3 cuadros).
MAX_SALTOS = 0.25     # fracción de cuadros con movimiento aislado (quieto-salto-quieto) entre los que se mueven
MAX_ACEL = 3.0        # px de salida por cuadro²: aceleración cuadrática media del recorte (clips aprobados: 1,4–1,8;
                      # el error a saltos ×1,78: 43–47; detección cruda sin suavizar: 7–12)
MAX_VUELTAS = 3.0     # cambios de dirección por segundo con movimiento de más de 1 px de salida


def raiz():
    return Path(os.environ.get("EDITOR_RAIZ") or os.getcwd())


def probe(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate", "-of", "json", str(video)],
                         capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return int(s["width"]), int(s["height"]), float(num) / float(den)


# ---------------------------------------------------------------- detectar
def detectar(a):
    import cv2
    carpeta = Path(a.carpeta); carpeta.mkdir(parents=True, exist_ok=True)
    W, H, fps = probe(a.video)
    ph = int(round(H * PROXY_W / W / 2)) * 2
    meta = {"video": str(Path(a.video).resolve()), "desde": a.desde, "hasta": a.hasta, "W": W, "H": H, "fps": fps,
            "proxy_w": PROXY_W, "proxy_h": ph}
    parcial = carpeta / "det.json"
    det = json.loads(parcial.read_text())["cuadros"] if parcial.exists() else []
    total = int(round((a.hasta - a.desde) * fps))
    if len(det) >= total:
        print(f"LISTO: {len(det)} cuadros ya detectados en {parcial}")
        return
    modelo = Path(a.modelo) if a.modelo else raiz() / ".herramientas/modelos/face_detection_yunet_2023mar.onnx"
    if not modelo.exists():
        sys.exit(f"No encuentro el modelo YuNet en {modelo} (ver clips-de-predicaciones.md §3.1)")
    yunet = cv2.FaceDetectorYN.create(str(modelo), "", (PROXY_W, ph), 0.6, 0.3, 5000)
    ini = a.desde + len(det) / fps
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-ss", f"{ini:.3f}", "-i", str(a.video), "-t", f"{a.hasta - ini:.3f}",
           "-vf", f"scale={PROXY_W}:{ph}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    tam = PROXY_W * ph * 3
    t0 = time.time(); prev_hist = None; prev_gris = None
    if det:  # para el primer cuadro del tramo nuevo no hay histograma previo: se marca sin corte
        pass
    while len(det) < total:
        buf = p.stdout.read(tam)
        if len(buf) < tam:
            break
        img = np.frombuffer(buf, np.uint8).reshape(ph, PROXY_W, 3)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [30, 32], [0, 180, 0, 256]); cv2.normalize(hist, hist)
        d = 0.0 if prev_hist is None else float(cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA))
        gris = cv2.cvtColor(cv2.resize(img, (PROXY_W // 2, ph // 2)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        pan = 0.0
        if prev_gris is not None and d <= 0.3:
            (sx, _sy), _r = cv2.phaseCorrelate(prev_gris, gris)
            pan = float(sx * 2)  # px del proxy por cuadro
        prev_hist, prev_gris = hist, gris
        _, caras = yunet.detect(img)
        F = []
        if caras is not None:
            for c in caras:
                x, y, w, h, s = float(c[0]), float(c[1]), float(c[2]), float(c[3]), float(c[14])
                if y + h / 2 < ph / 2:  # solo la mitad superior (el público está abajo)
                    F.append([round(x, 1), round(y, 1), round(w, 1), round(h, 1), round(s, 3)])
        det.append({"d": round(d, 3), "pan": round(pan, 2), "f": F})
        if time.time() - t0 > LIMITE_S:
            break
    p.kill()
    parcial.write_text(json.dumps({"meta": meta, "cuadros": det}))
    if len(det) < total:
        print(f"SIGUE: {len(det)}/{total} cuadros detectados. Vuelve a correr el mismo comando.")
    else:
        print(f"LISTO: {len(det)} cuadros detectados ({len(det) / (time.time() - t0 + 1e-9):.0f} por s en el último tramo)")


# ---------------------------------------------------------------- recorrido
def caminos_por_plano(det, pw, ph):
    n = len(det)
    cortes = [0] + [i for i, o in enumerate(det) if o["d"] > 0.3 and i > 0] + [n]
    xs = np.full(n, np.nan); hs = np.full(n, np.nan); plano = np.zeros(n, int); planos = []
    for si, (a, b) in enumerate(zip(cortes, cortes[1:])):
        if b <= a:
            continue
        plano[a:b] = si; prev = None
        for i in range(a, b):
            F = [(x + w / 2, y + h / 2, h) for x, y, w, h, s in det[i]["f"]]
            if not F:
                continue
            if prev is None:
                c = max(F, key=lambda f: f[2])
            else:
                c = min(F, key=lambda f: abs(f[0] - prev))
                if abs(c[0] - prev) > 0.12 * pw:
                    continue
            xs[i], hs[i] = c[0], c[2]; prev = c[0]
        seg = np.arange(a, b); ok = ~np.isnan(xs[a:b])
        if ok.sum() == 0:
            xs[a:b] = pw / 2; hs[a:b] = ph * 0.08
        else:
            xs[a:b] = np.interp(seg, seg[ok], xs[a:b][ok]); hs[a:b] = np.interp(seg, seg[ok], hs[a:b][ok])
        caraH = float(np.median(hs[a:b])) / ph
        planos.append({"desde": a, "hasta": b, "cara_alto": round(caraH, 3),
                       "acercamiento_base": 1.35 if caraH < 0.115 else 1.0, "sin_cara": int((~ok).sum())})
    return xs, plano, planos


def seguir(xs, planos):
    out = xs.copy()
    for p in planos:
        a, b = p["desde"], p["hasta"]; v = out[a:b].copy()
        for k in range(1, len(v)):
            v[k] = v[k - 1] + 0.25 * (v[k] - v[k - 1])
        for k in range(len(v) - 2, -1, -1):
            v[k] = v[k + 1] + 0.25 * (v[k] - v[k + 1])
        out[a:b] = v
    return out


def suave(v, n):
    if n <= 1 or len(v) < 3:
        return v.copy()
    n = min(n, len(v)); k = np.ones(n) / n
    pad = np.pad(v, (n // 2, n - 1 - n // 2), mode="edge")
    return np.convolve(pad, k, mode="valid")


def quieto(xs, planos, pan, fps, crop_proxy, px_salida=1.0):
    """Cuadro fijo mientras la cara esté en la zona central; movimientos con aceleración y frenado cuando sale."""
    out = np.empty_like(xs)
    zona = 0.18 * crop_proxy            # la cara puede moverse ±18 % del ancho del recorte sin que el cuadro se mueva
    urgente = 0.34 * crop_proxy         # a partir de acá se mueve aunque la cámara original esté paneando
    for p in planos:
        a, b = p["desde"], p["hasta"]
        f = suave(xs[a:b], int(round(fps)))           # intención de la cara (1 s), sin gestos
        c = float(np.median(f[: max(1, int(fps))]))  # arranque: donde está en el primer segundo
        i, m = 0, b - a
        while i < m:
            desvio = f[i] - c
            paneando = abs(pan[a + i]) > 1.5
            if abs(desvio) > zona and (not paneando or abs(desvio) > urgente):
                # Duración según la distancia en px de salida: la aceleración pico de la curva es 6·D/N²; con
                # N = √(4·D) queda en ≤ 1,5 px/cuadro² (un movimiento de 500 px dura ~1,8 s). Entre 0,6 y 2,5 s.
                d_sal = abs(desvio) * px_salida
                dur = int(round(np.clip(np.sqrt(4 * d_sal), 0.6 * fps, 2.5 * fps)))
                fin = min(m, i + dur)
                destino = float(np.median(f[i:fin]))
                t = np.arange(1, fin - i + 1) / dur         # si el plano termina antes, el movimiento queda a medias (sin apurarlo)
                e = t * t * (3 - 2 * t)                    # aceleración y frenado
                out[a + i:a + fin] = c + (destino - c) * e
                c = float(out[a + fin - 1]); i = fin
            else:
                out[a + i] = c; i += 1
    return out


def control(x_src, plano, fps, ampl):
    """Mide el recorte en px de la salida. Devuelve (aprobado, métricas, motivos)."""
    p = x_src * ampl
    dx = np.diff(p); mismo = np.diff(plano) == 0; dx = dx[mismo]
    mov = np.abs(dx) > 0.5
    aislados = 0
    idx = np.nonzero(mov)[0]
    for i in idx:
        if 0 < i < len(dx) - 1 and not mov[i - 1] and not mov[i + 1]:
            aislados += 1
    saltos = aislados / max(1, mov.sum())
    acels, vueltas, seg = [], 0, 0.0
    for s_ in np.unique(plano):
        v = p[plano == s_]
        if len(v) < 5:
            continue
        acels += list(np.diff(v, 2))                 # temblor = cambios bruscos de velocidad de un cuadro al otro
        d = np.diff(v); d = d[np.abs(d) > 1.0]
        vueltas += int(np.sum(np.sign(d[1:]) != np.sign(d[:-1]))); seg += len(v) / fps
    acel = float(np.sqrt(np.mean(np.square(acels)))) if acels else 0.0
    vps = vueltas / max(seg, 1e-9)
    motivos = []
    if saltos > MAX_SALTOS:
        motivos.append(f"se mueve a saltos ({saltos:.0%} de los movimientos son aislados; máx. {MAX_SALTOS:.0%})")
    if acel > MAX_ACEL:
        motivos.append(f"tiembla (aceleración {acel:.1f} px/cuadro²; máx. {MAX_ACEL})")
    if vps > MAX_VUELTAS:
        motivos.append(f"va y viene ({vps:.1f} cambios de dirección por segundo; máx. {MAX_VUELTAS})")
    met = {"saltos": round(float(saltos), 3), "aceleracion": round(acel, 2), "vueltas_por_s": round(vps, 2),
           "ampliacion": round(ampl, 2)}
    return not motivos, met, motivos


def recorrido(a):
    carpeta = Path(a.carpeta)
    d = json.loads((carpeta / "det.json").read_text()); meta, det = d["meta"], d["cuadros"]
    W, H, fps, pw, ph = meta["W"], meta["H"], meta["fps"], meta["proxy_w"], meta["proxy_h"]
    # Se recorta siempre sobre una imagen de alto 2160 ("4K virtual"): si el original es menor se agranda antes de
    # recortar. Así el recorte se mueve de a 1 px de 4K (< 1 px de salida) y no a saltitos de 2 px del original
    # ampliados (en Full HD eran 3,6 px de salida: temblor en cada arranque y frenado).
    k = max(1.0, 2160 / H)
    Wv, Hv = int(round(W * k / 2)) * 2, int(round(H * k / 2)) * 2
    crop_w = int(round(Hv * 9 / 16 / 2)) * 2         # 1216 (≈1215 del método original)
    ampl_real = SALIDA_W / (crop_w / k)               # cuánto se agranda el detalle del original (4K 0,89 · FHD 1,78)
    ampl = SALIDA_W / crop_w                          # px de salida por px del recorte (para medir el movimiento)
    escala = Wv / pw; crop_proxy = crop_w / escala
    xs, plano, planos = caminos_por_plano(det, pw, ph)
    pan = np.array([o.get("pan", 0.0) for o in det])
    modo = a.modo
    if modo == "auto":
        cand = seguir(xs, planos)
        ok, met, _ = control(np.clip(cand * escala - crop_w / 2, 0, Wv - crop_w), plano, fps, ampl)
        modo = "seguir" if (ampl_real <= 1.0 and ok) else "quieto"
    centro = seguir(xs, planos) if modo == "seguir" else quieto(xs, planos, pan, fps, crop_proxy, escala * ampl)
    x = np.round(np.clip(centro * escala - crop_w / 2, 0, Wv - crop_w)).astype(int)
    ok, met, motivos = control(x.astype(float), plano, fps, ampl)
    res = {"modo": modo, "ancho_recorte": crop_w, "alto": Hv, "agrandar": round(k, 4), "ampliacion": round(ampl, 3),
           "ampliacion_real": round(ampl_real, 3), "fps": fps,
           "x": x.tolist(), "plano": plano.tolist(), "planos": planos, "control": met, "aprobado": ok}
    (carpeta / "recorrido.json").write_text(json.dumps(res))
    with open(carpeta / "cmd.txt", "w") as f:
        for i in range(1, len(x)):
            if x[i] != x[i - 1]:
                f.write(f"{max(0.0, (i - 0.5) / fps):.4f} crop@c x {x[i]};\n")
    previo = f"scale={Wv}:{Hv}:flags=lanczos," if k > 1 else ""
    (carpeta / "filtro.txt").write_text(f"{previo}sendcmd=f={carpeta / 'cmd.txt'},crop@c={crop_w}:{Hv}:{x[0]}:0:exact=1,"
                                         f"scale={SALIDA_W}:{SALIDA_H}:flags=lanczos\n")
    informe(carpeta, ok, met, motivos, modo)
    if ampl_real > 1.0:
        print(f"Aviso: el original se amplía ×{ampl_real:.2f} (recorte de {crop_w / k:.0f} px del original). Pide a la persona el archivo de mayor "
              "calidad que tenga (4K si existe); con este se usa el modo quieto.")


def informe(carpeta, ok, met, motivos, modo):
    txt = (f"{'APROBADO' if ok else 'NO APROBADO'} · modo {modo} · ampliación ×{met['ampliacion']}\n"
           f"saltos {met['saltos']:.0%} (máx {MAX_SALTOS:.0%}) · aceleración {met['aceleracion']} px/cuadro² (máx {MAX_ACEL}) · "
           f"vueltas {met['vueltas_por_s']}/s (máx {MAX_VUELTAS})\n" + "".join(f"- {m}\n" for m in motivos))
    if not ok:
        txt += ("No entregar. Si el modo era seguir, probar --modo quieto; si sigue fallando, mirar en la hoja de contactos "
                "qué plano falla (cara perdida, público, paneo) y corregir ese tramo.\n")
    (carpeta / "control.txt").write_text(txt)
    print(txt.strip())


def control_cmd(a):
    carpeta = Path(a.carpeta); r = json.loads((carpeta / "recorrido.json").read_text())
    ok, met, motivos = control(np.array(r["x"], float), np.array(r["plano"]), r["fps"], r["ampliacion"])
    informe(carpeta, ok, met, motivos, r["modo"])
    sys.exit(0 if ok else 2)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="accion", required=True)
    d = sp.add_parser("detectar"); d.add_argument("video"); d.add_argument("--desde", type=float, required=True)
    d.add_argument("--hasta", type=float, required=True); d.add_argument("--carpeta", required=True)
    d.add_argument("--modelo")
    r = sp.add_parser("recorrido"); r.add_argument("carpeta"); r.add_argument("--modo", default="auto",
                                                                             choices=["auto", "seguir", "quieto"])
    c = sp.add_parser("control"); c.add_argument("carpeta")
    a = ap.parse_args()
    {"detectar": detectar, "recorrido": recorrido, "control": control_cmd}[a.accion](a)


if __name__ == "__main__":
    main()
