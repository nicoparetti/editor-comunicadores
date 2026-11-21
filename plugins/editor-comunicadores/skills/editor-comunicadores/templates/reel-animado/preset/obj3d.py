# Objetos 3D (Three.js 0.170, mismo motor que biblia3d.py), con la paleta de la variable TEMA:
#   iglesia  · templo con torre
#   plataforma · rectángulo con escaleras laterales
#   altar    · altar rústico de piedras distintas con fuego arriba
# Uso: python3 obj3d.py <escena> <t> <salida.png> [m=0..1 transformación plataforma→altar]
import os, sys, subprocess, time
from pathlib import Path
HERE = Path(__file__).resolve().parent

JS = r"""
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

const BG = new THREE.Color('__BG__'), ACC = new THREE.Color('__ACC__'), ACCL = new THREE.Color('__ACCL__');
const W = 1080, H = 1920;
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('gl'), antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false); renderer.setPixelRatio(1);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 0.85;
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const scene = new THREE.Scene(); scene.background = BG;
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.22;
const camera = new THREE.PerspectiveCamera(30, W / H, 0.1, 100);
const SCENE = window.SCENE;

function radialTex() { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
  const r = g.createRadialGradient(128, 128, 0, 128, 128, 128); r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(0.25, 'rgba(255,255,255,.55)'); r.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = r; g.fillRect(0, 0, 256, 256); return new THREE.CanvasTexture(c); }
function shadowTex() { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
  const r = g.createRadialGradient(128, 128, 8, 128, 128, 128); r.addColorStop(0, 'rgba(0,0,0,.8)'); r.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = r; g.fillRect(0, 0, 256, 256);
  return new THREE.CanvasTexture(c); }
function contact(w, d, y = 0.002) { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d), new THREE.MeshBasicMaterial({ map: shadowTex(), transparent: true, depthWrite: false }));
  m.rotation.x = -Math.PI / 2; m.position.y = y; return m; }
const edgeMat = new THREE.LineBasicMaterial({ color: ACC, transparent: true, opacity: 0.9 });
function withEdges(mesh, op = 0.9) { const e = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry, 25), edgeMat.clone()); e.material.opacity = op; mesh.add(e); return mesh; }
// piso: grilla tenue en perspectiva
{ const grid = new THREE.GridHelper(14, 28, 0x3a2f28, 0x2a221d); grid.material.transparent = true; grid.material.opacity = 0.45; scene.add(grid); }
scene.add(new THREE.AmbientLight(0xffffff, 0.16));
const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: radialTex(), color: ACCL, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
scene.add(halo);
const key = new THREE.SpotLight(0xFFF1E4, 14, 16, Math.PI / 7, 0.65, 1.3); key.castShadow = true; key.shadow.mapSize.set(1024, 1024); key.shadow.radius = 5;
scene.add(key); scene.add(key.target);
const rim = new THREE.PointLight(ACC, 6, 8, 1.4); scene.add(rim);

// ---------- IGLESIA ----------
const iglesia = new THREE.Group();
{ const wall = new THREE.MeshStandardMaterial({ color: 0xD8CEC2, roughness: 0.92 });
  const roof = new THREE.MeshStandardMaterial({ color: 0x3A2F28, roughness: 0.7 });
  const win = new THREE.MeshStandardMaterial({ color: 0x2a1a10, emissive: ACCL, emissiveIntensity: 0.9, roughness: 0.5 });
  const nave = withEdges(new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.95, 2.3), wall), 0.35); nave.position.set(0, 0.475, -0.25); nave.castShadow = nave.receiveShadow = true; iglesia.add(nave);
  const sh = new THREE.Shape(); sh.moveTo(-0.84, 0); sh.lineTo(0, 0.62); sh.lineTo(0.84, 0); sh.lineTo(-0.84, 0);
  const rg = new THREE.ExtrudeGeometry(sh, { depth: 2.45, bevelEnabled: false }); rg.translate(0, 0, -1.225);
  const r = withEdges(new THREE.Mesh(rg, roof), 0.9); r.position.set(0, 0.95, -0.25); r.castShadow = true; iglesia.add(r);
  // torre al frente
  const tw = withEdges(new THREE.Mesh(new THREE.BoxGeometry(0.62, 1.55, 0.62), wall), 0.35); tw.position.set(0, 0.775, 1.05); tw.castShadow = true; iglesia.add(tw);
  const bel = withEdges(new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.42, 0.5), wall), 0.35); bel.position.set(0, 1.76, 1.05); iglesia.add(bel);
  for (const [x, z, ry] of [[0, 1.302, 0], [0.252, 1.05, Math.PI / 2], [-0.252, 1.05, -Math.PI / 2]]) {
    const o = new THREE.Mesh(new THREE.PlaneGeometry(0.18, 0.26), win); o.position.set(x, 1.77, z); o.rotation.y = ry; iglesia.add(o); }
  const cap = withEdges(new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.05, 0.58), roof), 0.9); cap.position.set(0, 1.995, 1.05); iglesia.add(cap);
  const sp = withEdges(new THREE.Mesh(new THREE.ConeGeometry(0.4, 1.05, 4, 1), roof), 0.9); sp.rotation.y = Math.PI / 4; sp.position.set(0, 2.545, 1.05); sp.castShadow = true; iglesia.add(sp);
  // puerta en arco y ventanas altas de la nave
  const door = new THREE.Mesh(new THREE.PlaneGeometry(0.24, 0.42), new THREE.MeshStandardMaterial({ color: 0x1a120d, emissive: ACC, emissiveIntensity: 0.25 }));
  door.position.set(0, 0.21, 1.362); iglesia.add(door);
  for (let k = 0; k < 4; k++) for (const s of [-1, 1]) {
    const o = new THREE.Mesh(new THREE.PlaneGeometry(0.16, 0.36), win); o.position.set(s * 0.752, 0.55, 0.55 - k * 0.52); o.rotation.y = s * Math.PI / 2; iglesia.add(o); }
  iglesia.add(contact(3.6, 4.2));
  scene.add(iglesia); }

// ---------- PLATAFORMA (con escaleras laterales) ----------
const plataforma = new THREE.Group();
{ const wood = new THREE.MeshStandardMaterial({ color: 0x5C4636, roughness: 0.7 });
  const top = withEdges(new THREE.Mesh(new RoundedBoxGeometry(1.9, 0.62, 1.1, 2, 0.02), wood)); top.position.y = 0.31; top.castShadow = top.receiveShadow = true; plataforma.add(top);
  for (const s of [-1, 1]) for (let k = 0; k < 3; k++) {
    const h = 0.62 * (3 - k) / 3.4; const st = withEdges(new THREE.Mesh(new THREE.BoxGeometry(0.22, h, 0.62), wood), 0.75);
    st.position.set(s * (0.95 + 0.11 + k * 0.22), h / 2, 0); st.castShadow = true; plataforma.add(st); }
  plataforma.add(contact(4.2, 2.2)); scene.add(plataforma); }

// ---------- ALTAR de piedras distintas ----------
const altar = new THREE.Group(); const stones = [];
{ let seed = 11; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
  const tones = [0x9A8F82, 0x857A6E, 0x6E6359, 0xA89C8E, 0x8F8173, 0x5F574F, 0xB3A592, 0x7D7064, 0x958775];
  function stone(w, h, d) { const g = new RoundedBoxGeometry(w, h, d, 3, Math.min(w, h, d) * 0.2); const p = g.attributes.position;
    const ph = [rnd() * 6, rnd() * 6, rnd() * 6];
    for (let v = 0; v < p.count; v++) { const x = p.getX(v), y = p.getY(v), z = p.getZ(v);
      const n = 1 + 0.13 * Math.sin(x * 9 + ph[0]) * Math.cos(z * 7 + ph[1]) + 0.08 * Math.sin(y * 11 + ph[2]);
      p.setXYZ(v, x * n, y * (0.92 + 0.12 * Math.sin(x * 5 + ph[1])), z * n); }
    g.computeVertexNormals(); return g; }
  const courses = [0.26, 0.2, 0.24, 0.18]; let y = 0;
  courses.forEach((h, ci) => { const half = 0.86 - ci * 0.04; let x = -half + 0.06 * rnd(); const end = half;
    while (x < end - 0.05) { let w = 0.18 + 0.4 * rnd() * rnd() + 0.12 * rnd(); if (x + w > end) w = end - x; if (w < 0.12) break;
      for (const zz of [-0.2, 0.2]) { const hh = h * (0.75 + 0.4 * rnd());
        const m = new THREE.Mesh(stone(w - 0.02, hh, 0.38 + 0.06 * rnd()), new THREE.MeshStandardMaterial({ color: tones[Math.floor(rnd() * tones.length)], roughness: 0.95 }));
        m.position.set(x + w / 2, y + hh / 2, zz + 0.03 * (rnd() - 0.5)); m.rotation.set(0.12 * (rnd() - 0.5), 0.22 * (rnd() - 0.5), 0.14 * (rnd() - 0.5));
        m.castShadow = m.receiveShadow = true; m.userData.base = m.position.clone(); m.userData.k = (ci + rnd()) / 4.5; altar.add(m); stones.push(m); }
      x += w; }
    y += h; });
  const slab = new THREE.Mesh(stone(1.5, 0.13, 0.86), new THREE.MeshStandardMaterial({ color: 0x8C8174, roughness: 0.9 }));
  slab.position.set(0, y + 0.06, 0); slab.castShadow = slab.receiveShadow = true; slab.userData.base = slab.position.clone(); slab.userData.k = 0.95; altar.add(slab); stones.push(slab);
  window.ALTAR_TOP = y + 0.12;
  altar.add(contact(3.0, 2.0)); scene.add(altar); }
// fuego: sprites aditivos que suben y titilan + luz cálida
function flameTex() { const c = document.createElement('canvas'); c.width = 128; c.height = 256; const g = c.getContext('2d');
  const r = g.createRadialGradient(64, 190, 4, 64, 160, 120); r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(0.25, 'rgba(255,214,170,.95)'); r.addColorStop(0.6, 'rgba(232,131,74,.55)'); r.addColorStop(1, 'rgba(232,131,74,0)');
  g.fillStyle = r; g.beginPath(); g.moveTo(64, 6); g.bezierCurveTo(118, 110, 120, 200, 64, 250); g.bezierCurveTo(8, 200, 10, 110, 64, 6); g.fill(); return new THREE.CanvasTexture(c); }
const fire = new THREE.Group(); const flames = [];
for (let i = 0; i < 34; i++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: flameTex(), transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
  s.userData = { a: (i * 0.618) % 1, x: (Math.sin(i * 2.3) * 0.2), z: Math.cos(i * 1.7) * 0.1 }; fire.add(s); flames.push(s); }
const fireLight = new THREE.PointLight(0xFFB070, 0, 5, 1.3); fire.add(fireLight); fireLight.position.y = 0.35;
fire.position.set(0, 0.98, 0); scene.add(fire);
const fireHalo = new THREE.Sprite(new THREE.SpriteMaterial({ map: radialTex(), color: ACC, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
fireHalo.position.set(0, 1.35, -0.2); scene.add(fireHalo);

const composer = new EffectComposer(renderer); composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), 0.55, 0.45, 0.9); composer.addPass(bloom); composer.addPass(new OutputPass());
const E = x => x < 0 ? 0 : x > 1 ? 1 : x, sm = x => { x = E(x); return x * x * (3 - 2 * x); };

window.render = (t, m = 0, luz = 1) => {
  iglesia.visible = SCENE === 'iglesia'; plataforma.visible = SCENE !== 'iglesia' && m < 0.999; altar.visible = SCENE !== 'iglesia' && m > 0.001;
  fire.visible = fireHalo.visible = altar.visible;
  if (SCENE === 'iglesia') {
    const a = -0.62 + 0.05 * sm(t / 6), dist = 15.5 - 0.6 * sm(t / 6);
    camera.position.set(Math.sin(a) * dist, 4.2, Math.cos(a) * dist); camera.lookAt(0, 1.25, 0.2);
    key.position.set(0.2, 6.5, 1.0); key.target.position.set(0, 0.6, 0.3); key.intensity = 14 * luz; key.angle = Math.PI / 6.5;
    halo.position.set(0, 3.25, 0.6); halo.scale.setScalar(1.9); halo.material.opacity = 0.32 * luz;
    rim.position.set(-1.5, 1.6, -2.5); rim.intensity = 5;
  } else {
    const a = 0.32 + 0.04 * Math.sin(t * 0.2), dist = 9.6 - 0.4 * sm(t / 6);
    camera.position.set(Math.sin(a) * dist, 3.0, Math.cos(a) * dist); camera.lookAt(0, 0.05, 0);
    // plataforma se hunde y las piedras suben una por una
    plataforma.scale.set(0.66, 0.66 * Math.max(0.001, 1 - sm(m * 1.4)), 0.66); plataforma.children.forEach(c => { if (c.material && c.material.opacity !== undefined && c.type === 'Mesh') {} });
    stones.forEach(s => { const p = sm((m * 1.6 - s.userData.k * 0.6)); s.position.y = s.userData.base.y - (1 - p) * 0.9; s.scale.setScalar(0.3 + 0.7 * p); });
    const f = sm((m - 0.75) / 0.25);
    flames.forEach((s, i) => { const u = s.userData, life = (u.a + t * 1.3) % 1;
      s.position.set(u.x * (1 - life * 0.85) + 0.03 * Math.sin(t * 7 + i), 0.08 + life * 0.62, u.z);
      const sc = (0.5 - 0.34 * life) * f * (0.9 + 0.2 * Math.sin(t * 11 + i)); s.scale.set(sc * 0.7, sc * 1.35, 1); s.material.opacity = (1 - life) * 0.55; });
    fireLight.intensity = 9 * f * (0.85 + 0.15 * Math.sin(t * 13)); fireHalo.material.opacity = 0.5 * f; fireHalo.scale.setScalar(2.4 + 0.15 * Math.sin(t * 5));
    key.position.set(0, 6.5, 0.8); key.target.position.set(0, 0.4, 0); key.intensity = 12 * luz; key.angle = Math.PI / 7;
    halo.position.set(0, 2.9, -0.4); halo.scale.setScalar(1.7); halo.material.opacity = 0.12 * luz;
    rim.position.set(0, 1.3, -2.0); rim.intensity = 4 + 3 * f;
  }
  composer.render();
};
window.ready = true;
"""

# Colores por paleta (variable TEMA)
COLORES = {
    'gris':  dict(BG='#1B1F24', ACC='#F6F6A8', ACCL='#FFFDE0'),
    'noche': dict(BG='#0E1626', ACC='#E3A93A', ACCL='#F6D893'),
}
TEMA = os.environ.get('TEMA', 'gris')

def html(scene):
    c = COLORES[TEMA]
    js = JS.replace('__BG__', c['BG']).replace('__ACC__', c['ACC']).replace('__ACCL__', c['ACCL'])
    imp = ("<script type='importmap'>{\"imports\":{\"three\":\"./node_modules/three/build/three.module.js\","
           "\"three/addons/\":\"./node_modules/three/examples/jsm/\"}}</script>")
    return (f"<!doctype html><html><head><meta charset='utf-8'>{imp}<style>html,body{{margin:0;background:{c['BG']}}}</style></head>"
            f"<body><canvas id='gl' style='width:1080px;height:1920px'></canvas><script>window.SCENE='{scene}'</script>"
            f"<script type='module'>{js}</script></body></html>")

def stills(jobs):
    """jobs: [(escena, t, m, luz, salida.png)]"""
    from playwright.sync_api import sync_playwright
    srv = subprocess.Popen(['python3', '-m', 'http.server', '8766', '--bind', '127.0.0.1'], cwd=str(HERE), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        with sync_playwright() as p:
            br = p.chromium.launch(executable_path=os.environ.get('CHROME', '/usr/bin/google-chrome'), args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
            pg = br.new_page(viewport={'width': 1080, 'height': 1920})
            pg.on('pageerror', lambda e: print('pageerror:', e))
            cur = None
            for sc, t, m, luz, out in jobs:
                if sc != cur:
                    f = HERE / f'obj3d_{sc}.html'; f.write_text(html(sc))
                    pg.goto(f'http://127.0.0.1:8766/{f.name}'); pg.wait_for_function('window.ready === true', timeout=60000); cur = sc
                pg.evaluate(f'render({t},{m},{luz})'); pg.wait_for_timeout(100); pg.screenshot(path=str(out)); print('ok', out)
            br.close()
    finally:
        srv.terminate()

if __name__ == '__main__':
    stills([(sys.argv[1], float(sys.argv[2]), float(sys.argv[4]) if len(sys.argv) > 4 else 0, 1, sys.argv[3])])
