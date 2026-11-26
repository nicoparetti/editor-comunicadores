// Render del motor de gráficos sin volver a empaquetar en cada llamada.
// Uso:
//   node render.mjs stills <Composicion> <carpeta_salida> <f1,f2,…> [--escala 0.5]
//   node render.mjs video  <Composicion> <salida.mp4> [--frames a-b] [--crf 17] [--escala 1]          (H.264, sin alfa)
//   node render.mjs capas  <Composicion> <carpeta_salida> <timeline.json>                           (un .mov ProRes 4444 con alfa por gráfico)
import {bundle} from '@remotion/bundler';
import {openBrowser, renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';

const [modo, comp, salida, extra] = process.argv.slice(2);
const opt = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d; };
const raiz = path.dirname(fileURLToPath(import.meta.url));

// El empaquetado copia public/; para no duplicar el vídeo base (1,5 GB) se empaqueta con una carpeta pública
// vacía y se enlaza la real dentro del paquete.
const vacio = path.join(raiz, '.public-vacio'); fs.mkdirSync(vacio, {recursive: true});
// el paquete va en /tmp: ahí se puede borrar y enlazar sin permisos (también en Windows)
const outDir = path.join(os.tmpdir(), 'motor-bundle');
fs.rmSync(outDir, {recursive: true, force: true});
const serveUrl = await bundle({entryPoint: path.join(raiz, 'src/index.ts'), outDir, publicDir: vacio});
const pub = path.join(outDir, 'public');
fs.rmSync(pub, {recursive: true, force: true});
fs.symlinkSync(path.join(raiz, 'public'), pub);

const hilos = Number(opt('hilos', 4)); // con 6 hilos el render falló por tiempo de espera
// Chromium de .herramientas: el motor puede estar en .herramientas/motor o en Motor/ (raíz de la carpeta)
const candidatos = [process.env.CHROMIUM_BIN, path.join(raiz, '..', 'chromium', 'bin', 'chromium'), path.join(raiz, '..', '.herramientas', 'chromium', 'bin', 'chromium')].filter(Boolean);
const browserExecutable = candidatos.find((p) => fs.existsSync(p)) || candidatos[candidatos.length - 1];
const chromiumOptions = {gl: 'swangle'};
const escala = Number(opt('escala', 1));

if (modo === 'stills') {
  fs.mkdirSync(salida, {recursive: true});
  const navegador = await openBrowser('chrome', {browserExecutable, chromiumOptions});
  const composition = await selectComposition({serveUrl, id: comp, puppeteerInstance: navegador, browserExecutable});
  for (const f of extra.split(',').map(Number)) {
    const out = path.join(salida, `f${String(f).padStart(5, '0')}.jpg`);
    await renderStill({composition, serveUrl, output: out, frame: f, imageFormat: 'jpeg', jpegQuality: 88, scale: escala, puppeteerInstance: navegador, browserExecutable, chromiumOptions});
  }
  await navegador.close({silent: true});
  console.log('stills OK');
} else if (modo === 'video') {
  const composition = await selectComposition({serveUrl, id: comp, browserExecutable, chromiumOptions});
  const fr = opt('frames', null);
  let ultimo = 0;
  await renderMedia({
    composition, serveUrl, codec: 'h264', outputLocation: salida, imageFormat: 'jpeg', jpegQuality: 92, pixelFormat: 'yuv420p', crf: Number(opt('crf', 17)), scale: escala,
    frameRange: fr ? fr.split('-').map(Number) : null, concurrency: hilos, browserExecutable, chromiumOptions, muted: true, x264Preset: opt('preset', 'medium'),
    onProgress: ({renderedFrames, encodedFrames}) => { if (renderedFrames - ultimo >= 300) { ultimo = renderedFrames; console.log(`render ${renderedFrames} · codificados ${encodedFrames}`); } },
  });
  console.log('OK', salida);
} else if (modo === 'capas') {
  fs.mkdirSync(salida, {recursive: true});
  const tl = JSON.parse(fs.readFileSync(extra, 'utf8'));
  const solo = opt('solo', null);
  for (const g of tl.graficos) {
    if (solo && !solo.split(',').includes(g.id)) continue;
    const composition = await selectComposition({serveUrl, id: comp, inputProps: {solo: g.id}, browserExecutable, chromiumOptions});
    const out = path.join(salida, g.archivo);
    await renderMedia({
      composition, serveUrl, codec: 'prores', proResProfile: '4444', outputLocation: out, imageFormat: 'png', pixelFormat: 'yuva444p10le',
      frameRange: [g.from, g.from + g.dur - 1], concurrency: hilos, browserExecutable, chromiumOptions, muted: true, inputProps: {solo: g.id},
    });
    console.log(out);
  }
}
process.exit(0);
