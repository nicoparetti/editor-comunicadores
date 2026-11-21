# Biblia (o libro) abierta en 3D con Three.js, en la paleta del estilo por defecto (variable TEMA = gris | noche).
# Necesita three en node_modules: copiar package.json a la carpeta de trabajo y correr `npm install`.
# Uso: TEMA=gris DUR=6 python3 biblia3d.py   → biblia3d_<tema>/biblia3d.mp4 + 3 stills
import os, subprocess, time, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit_base import TEMAS

DUR, FPS = float(os.environ.get('DUR', 6.0)), 30
ROOT = Path(__file__).resolve().parent
TAPA = {'gris': '#2B2F36', 'noche': '#1B2C52'}
LUZ = {'gris': '#FFFDE0', 'noche': '#F6D893'}

JS = r"""
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const ACC = new THREE.Color('__ACC__'), ACCL = new THREE.Color('__ACCL__'), COVER = new THREE.Color('__COVER__');
const W = 1080, H = 1920;
const canvas = document.getElementById('gl');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, preserveDrawingBuffer: true });
renderer.setSize(W, H, false); renderer.setPixelRatio(1);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 0.85;
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const scene = new THREE.Scene(); scene.background = new THREE.Color('__BG__');
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.25;
const camera = new THREE.PerspectiveCamera(30, W / H, 0.1, 100);

// ---------- textura de página (dos columnas, versículos) ----------
function pageTex(seed, left) {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 1400; const g = c.getContext('2d');
  const grd = g.createLinearGradient(left ? 1024 : 0, 0, left ? 0 : 1024, 0);
  grd.addColorStop(0, '#A89F92'); grd.addColorStop(0.05, '#D2CABD'); grd.addColorStop(0.16, '#EEE8DE'); grd.addColorStop(1, '#F6F1E9');
  g.fillStyle = grd; g.fillRect(0, 0, 1024, 1400);
  const img = g.getImageData(0, 0, 1024, 1400); let rs = seed * 17;
  for (let i = 0; i < img.data.length; i += 4) { rs = (rs * 1103515245 + 12345) & 0x7fffffff; const n = ((rs >> 16) % 9) - 4; img.data[i] += n; img.data[i+1] += n; img.data[i+2] += n; }
  g.putImageData(img, 0, 0);
  let r = seed; const rnd = () => (r = (r * 9301 + 49297) % 233280) / 233280;
  g.fillStyle = 'rgba(34,30,27,.68)';
  for (let col = 0; col < 2; col++) {
    const x0 = 110 + col * 430;
    for (let y = 150; y < 1290; y += 34) {
      if (rnd() < 0.06) { y += 20; continue; }
      const w = 330 + rnd() * 60 - (rnd() < 0.15 ? 150 : 0);
      g.fillRect(x0, y, w, 9);
    }
  }
  g.fillStyle = 'rgba(40,36,32,.7)'; g.font = 'bold 44px serif'; g.fillText(left ? 'ÉXODO' : '31', left ? 440 : 500, 95);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.center.set(0.5, 0.5); t.rotation = Math.PI; if (!left) { t.wrapS = THREE.RepeatWrapping; t.repeat.x = -1; } return t;
}

// ---------- geometría: hoja curva (sale del lomo, sube y cae suave) ----------
const PW = 1.0, PH = 1.38, SEG = 48;
function lift(x) { return 0.16 * (1 - Math.exp(-x / 0.10)) - 0.05 * x * x; }   // altura según distancia al lomo
function curvedSheet(side, dz) {
  const geo = new THREE.PlaneGeometry(PW, PH, SEG, 4);
  const p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const u = p.getX(i) + PW / 2;              // 0..PW desde el lomo
    p.setXYZ(i, side * u, lift(u) + dz, p.getY(i));
  }
  geo.computeVertexNormals(); return geo;
}

const book = new THREE.Group(); scene.add(book);
const paperMat = (tex) => new THREE.MeshStandardMaterial({ map: tex, roughness: 0.85, metalness: 0, side: THREE.DoubleSide });
const edgeMat = new THREE.MeshStandardMaterial({ color: 0xE9E2D6, roughness: 0.9 });
const coverMat = new THREE.MeshStandardMaterial({ color: COVER, roughness: 0.55, metalness: 0.05 });
// tapas
for (const side of [-1, 1]) {
  const cv = new THREE.Mesh(new THREE.BoxGeometry(PW + 0.06, 0.028, PH + 0.08), coverMat);
  cv.position.set(side * (PW + 0.06) / 2, -0.016, 0); cv.rotation.z = side * 0.025; cv.castShadow = cv.receiveShadow = true; book.add(cv);
}
const spine = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, PH + 0.08, 16, 1, false, 0, Math.PI), coverMat);
spine.rotation.x = Math.PI / 2; spine.rotation.z = Math.PI; spine.position.y = -0.02; book.add(spine);
// bloque de páginas: varias hojas apiladas + canto
for (const side of [-1, 1]) {
  for (let k = 0; k < 9; k++) {
    const dz = -0.012 * k;
    const m = new THREE.Mesh(curvedSheet(side, dz), k === 0 ? paperMat(pageTex(side > 0 ? 7 : 3, side < 0)) : edgeMat);
    m.receiveShadow = true; m.castShadow = k === 0; book.add(m);
  }
}
// cantos del bloque de páginas
function edgeTex() { const c = document.createElement('canvas'); c.width = 64; c.height = 256; const g = c.getContext('2d');
  g.fillStyle = '#E4DCCD'; g.fillRect(0, 0, 64, 256);
  for (let y = 0; y < 256; y += 3) { g.fillStyle = y % 6 ? 'rgba(120,108,92,.28)' : 'rgba(255,255,255,.35)'; g.fillRect(0, y, 64, 1); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }
const edgeM = new THREE.MeshStandardMaterial({ map: edgeTex(), roughness: 0.95, side: THREE.DoubleSide });
const DEPTH = 0.105;
for (const side of [-1, 1]) {
  const fe = new THREE.Mesh(new THREE.PlaneGeometry(PH, DEPTH), edgeM);
  fe.rotation.y = Math.PI / 2; fe.position.set(side * PW, lift(PW) - DEPTH / 2, 0); book.add(fe);
  const geo = new THREE.PlaneGeometry(PW, DEPTH, SEG, 1); const p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) { const u = p.getX(i) + PW / 2; const y = p.getY(i) > 0 ? lift(u) : lift(u) - DEPTH * Math.min(1, u / 0.05);
    p.setXYZ(i, side * u, y, PH / 2); }
  geo.computeVertexNormals(); book.add(new THREE.Mesh(geo, edgeM));
}
// cinta marcadora en el color principal: corre por la página y cae por el pie del libro
{ const y0 = lift(0.035) + 0.006;
  const pts = [[0.035, y0, -0.25], [0.037, y0, 0.2], [0.04, y0, 0.6], [0.045, y0 - 0.01, PH / 2 + 0.01], [0.05, -0.04, PH / 2 + 0.035], [0.06, -0.09, PH / 2 + 0.07], [0.075, -0.11, PH / 2 + 0.16]]
    .map(p => new THREE.Vector3(...p));
  const rib = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 80, 0.02, 8, false),
    new THREE.MeshStandardMaterial({ color: ACC, roughness: 0.45, emissive: ACC, emissiveIntensity: 0.08 }));
  rib.scale.set(1, 0.35, 1); rib.position.y = 0.01; book.add(rib); }
// hoja que se da vuelta (derecha -> izquierda)
const turnGeo = new THREE.PlaneGeometry(PW, PH, SEG, 6);
const turnBase = turnGeo.attributes.position.array.slice();
const turnMat = new THREE.MeshStandardMaterial({ map: pageTex(5, true), roughness: 0.85, side: THREE.FrontSide });
const turnBack = new THREE.MeshStandardMaterial({ map: pageTex(11, false), roughness: 0.85, side: THREE.BackSide });
const turn = new THREE.Mesh(turnGeo, turnMat); turn.castShadow = true; book.add(turn);
const turnB = new THREE.Mesh(turnGeo, turnBack); book.add(turnB);
function setTurn(p) {           // p 0..1
  const pos = turnGeo.attributes.position;
  const theta = Math.PI * p;    // giro sobre el lomo
  const curl = Math.sin(Math.PI * p) * 1.4;   // curvatura durante el giro
  for (let i = 0; i < pos.count; i++) {
    const u = turnBase[i * 3] + PW / 2, z = turnBase[i * 3 + 1];
    const base = lift(u) + 0.004;
    // se eleva desde la curva de reposo y rota con curvatura progresiva
    const a = theta + curl * (u / PW) * (u / PW) * 0.5;
    const x = Math.cos(a) * u, y = base + Math.max(0, Math.sin(a)) * u * 0.95;
    pos.setXYZ(i, x, y, z);
  }
  pos.needsUpdate = true; turnGeo.computeVertexNormals();
}
book.rotation.x = 0; book.position.y = 0;

// ---------- luces ----------
scene.add(new THREE.AmbientLight(0xffffff, 0.18));
const key = new THREE.SpotLight(0xFFF4E8, 9, 14, Math.PI / 6, 0.7, 1.4);
key.position.set(0.4, 3.2, 1.6); key.target.position.set(0, 0, 0); key.castShadow = true;
key.shadow.mapSize.set(1024, 1024); key.shadow.radius = 6; scene.add(key); scene.add(key.target);
const rim = new THREE.PointLight(ACC, 9, 6, 1.4); rim.position.set(0, 0.9, -1.6); scene.add(rim);
const core = new THREE.PointLight(ACCL, 3.5, 3, 1.5); core.position.set(0, 0.75, -0.1); scene.add(core);
// piso que recibe la sombra (transparente salvo la sombra)
// sombra de contacto falsa (un degradé oscuro bajo el libro)
const shc = document.createElement('canvas'); shc.width = shc.height = 256; { const g = shc.getContext('2d');
  const r = g.createRadialGradient(128, 128, 10, 128, 128, 128); r.addColorStop(0, 'rgba(0,0,0,.75)'); r.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = r; g.fillRect(0, 0, 256, 256); }
const floor = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 2.4), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(shc), transparent: true, depthWrite: false }));
floor.rotation.x = -Math.PI / 2; floor.position.y = -0.045; scene.add(floor);

// ---------- luz que sube del libro: halo + partículas ----------
function radialTex() { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
  const r = g.createRadialGradient(128, 128, 0, 128, 128, 128); r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(0.25, 'rgba(255,255,255,.55)'); r.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = r; g.fillRect(0, 0, 256, 256); return new THREE.CanvasTexture(c); }
const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: radialTex(), color: ACCL, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
halo.scale.set(1.3, 1.3, 1); halo.position.set(0, 0.8, -0.5); scene.add(halo);
const N = 260, pg = new THREE.BufferGeometry(), pp = new Float32Array(N * 3), seeds = [];
for (let i = 0; i < N; i++) { seeds.push([Math.random(), Math.random(), Math.random(), Math.random()]); }
pg.setAttribute('position', new THREE.BufferAttribute(pp, 3));
const pts = new THREE.Points(pg, new THREE.PointsMaterial({ map: radialTex(), color: ACCL, size: 0.035, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
scene.add(pts);

// ---------- posproceso ----------
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), 0.5, 0.45, 0.96); composer.addPass(bloom);
composer.addPass(new OutputPass());

const E = x => x < 0 ? 0 : x > 1 ? 1 : x, sm = x => { x = E(x); return x * x * (3 - 2 * x); };
window.render = (t) => {
  // cámara: baja y se acerca lento, órbita mínima
  const a = -0.22 + 0.10 * sm(t / 6), dist = 9.0 - 0.8 * sm(t / 6), el = 0.66 - 0.08 * sm(t / 6);
  camera.position.set(Math.sin(a) * dist * Math.cos(el), Math.sin(el) * dist, Math.cos(a) * dist * Math.cos(el));
  camera.lookAt(0, 0.62, 0.05);
  // la hoja se da vuelta entre 1,6 y 3,1 s
  setTurn(sm((t - 1.6) / 1.5));
  // la luz crece cuando cae la hoja
  const glow = 0.35 + 0.65 * sm((t - 2.6) / 1.2);
  halo.material.opacity = glow * 0.26; halo.scale.setScalar(1.3 + 0.9 * glow + 0.04 * Math.sin(t * 3));
  core.intensity = 0.2 + 0.35 * glow; rim.intensity = 3 + 3 * glow;
  for (let i = 0; i < N; i++) { const s = seeds[i]; const life = (s[0] * 4 + t * (0.35 + 0.3 * s[1])) % 1;
    const rr = 0.05 + 0.45 * s[2] * (0.4 + life);
    pp[i * 3] = Math.cos(s[3] * 6.28) * rr; pp[i * 3 + 1] = 0.12 + life * 1.6 * glow + 0.02; pp[i * 3 + 2] = Math.sin(s[3] * 6.28) * rr * 0.6; }
  pg.attributes.position.needsUpdate = true; pts.material.opacity = 0.9 * glow;
  composer.render();
};
window.ready = true;
"""

def build(tema):
    m = TEMAS[tema]
    j = JS.replace('__BG__', m['BG']).replace('__ACC__', m['ACC']).replace('__ACCL__', LUZ[tema]).replace('__COVER__', TAPA[tema])
    imp = ("<script type='importmap'>{\"imports\":{\"three\":\"./node_modules/three/build/three.module.js\","
           "\"three/addons/\":\"./node_modules/three/examples/jsm/\"}}</script>")
    return (f"<!doctype html><html><head><meta charset='utf-8'>{imp}<style>html,body{{margin:0;background:{m['BG']}}}</style></head>"
            f"<body><canvas id='gl' style='position:absolute;left:0;top:0;width:1080px;height:1920px'></canvas>"
            f"<div style='position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 45%,transparent 55%,rgba(0,0,0,.35) 100%)'></div>"
            f"<script type='module'>{j}</script></body></html>")

if __name__ == '__main__':
    from playwright.sync_api import sync_playwright
    tema = os.environ.get('TEMA', 'gris')
    out = ROOT / f'biblia3d_{tema}'; out.mkdir(exist_ok=True)
    f = ROOT / f'biblia3d_{tema}.html'; f.write_text(build(tema))
    n = int(DUR * FPS)
    srv = subprocess.Popen(['python3', '-m', 'http.server', '8765', '--bind', '127.0.0.1'], cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast',
                           '-crf', '14', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out / 'biblia3d.mp4')], stdin=subprocess.PIPE)
    try:
        with sync_playwright() as p:
            br = p.chromium.launch(executable_path=os.environ.get('CHROME', '/usr/bin/google-chrome'), args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
            pg = br.new_page(viewport={'width': 1080, 'height': 1920})
            pg.on('pageerror', lambda e: print('pageerror:', e))
            pg.goto(f'http://127.0.0.1:8765/{f.name}'); pg.wait_for_function('window.ready === true', timeout=60000)
            for i in range(n):
                pg.evaluate(f'render({i / FPS})'); ff.stdin.write(pg.screenshot(type='jpeg', quality=95))
            for t, k in ((0.5, 'a'), (2.3, 'b'), (4.8, 'c')):
                pg.evaluate(f'render({t})'); pg.screenshot(path=str(out / f'biblia3d_{k}.png'))
            br.close()
    finally:
        ff.stdin.close(); ff.wait(); srv.terminate()
    print('ok', n, 'cuadros')
