# Mapas base a escala fija y extensión amplia (para cámara con zoom). Natural Earth 1:50m desde GitHub:
#   curl -sS -o ne_50m_admin0.geojson https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson
# Salida: JSON con W, H, land/high/high2 (paths SVG en píxeles base) y pts (puntos con nombre en píxeles base).
import json, math, sys
g = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'ne_50m_admin0.geojson'))
def base(lon0, lon1, lat0, lat1, latc, s, hl=(), hl2=()):
    k = math.cos(math.radians(latc))
    P = lambda lon, lat: ((lon - lon0) * k * s, (lat1 - lat) * s)
    land, high, high2 = [], [], []
    for f in g['features']:
        geom = f['geometry']; nm = f['properties']['ADMIN']
        polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
        for poly in polys:
            ring = poly[0]; xs = [c[0] for c in ring]; ys = [c[1] for c in ring]
            if max(xs) < lon0 or min(xs) > lon1 or max(ys) < lat0 or min(ys) > lat1: continue
            d = "M" + " L".join(f"{P(x, y)[0]:.0f},{P(x, y)[1]:.0f}" for x, y in ring) + "Z"
            (high if nm in hl else high2 if nm in hl2 else land).append(d)
    return dict(W=round((lon1 - lon0) * k * s), H=round((lat1 - lat0) * s), land=land, high=high, high2=high2), P
# Ejemplo el reel animado de referencia: Europa (Chequia resaltada, Alemania al alejar), escala 186,6 px/° (≈ 9° de ancho visibles con zoom 1)
E, PE = base(-15, 45, 15, 72, 50, 186.6, ['Czechia'], ['Germany'])
E['pts'] = {k: [round(v, 1) for v in PE(*ll)] for k, ll in dict(herrnhut=(14.74, 51.02), suchdol=(17.93, 49.65), brno=(16.61, 49.2),
    dresde=(13.74, 51.05), zoom=(15.6, 50.15), wide=(14.0, 50.5), alemania=(9.5, 50.3)).items()}
sx, sy = E['pts']['suchdol']; hx, hy = E['pts']['herrnhut']; E['pts']['ctrl'] = [(sx + hx) / 2 + 40, max(sy, hy) + 40]  # ruta por debajo de los rótulos
json.dump(E, open('mapaE3.json', 'w'))
# Ejemplo el reel animado de referencia: Atlántico (Herrnhut → Copenhague → Santo Tomás), escala 14,2 px/°
M, PM = base(-110, 60, -30, 80, 36, 14.2, ['Denmark'])
M['pts'] = {k: [round(v, 1) for v in PM(*ll)] for k, ll in dict(herrnhut=(14.74, 51.02), copenhague=(12.57, 55.68), stthomas=(-64.93, 18.34),
    cam=(-25, 38), ctrl=(-26.7, 64.8)).items()}
json.dump(M, open('mapaM3.json', 'w'))
print('ok', E['W'], E['H'], M['W'], M['H'])
