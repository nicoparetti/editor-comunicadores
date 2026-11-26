import {Config} from '@remotion/cli/config';
import path from 'node:path';
import fs from 'node:fs';

// Navegador para renderizar: Chromium de Linux (arm64 en Mac, x64 en Windows) instalado en .herramientas/chromium
// (preparar_entorno.sh). El motor puede estar en .herramientas/motor o en Motor/ (raíz de la carpeta).
const candidatos = [process.env.CHROMIUM_BIN, path.join(process.cwd(), '..', 'chromium', 'bin', 'chromium'), path.join(process.cwd(), '..', '.herramientas', 'chromium', 'bin', 'chromium')].filter(Boolean) as string[];
Config.setBrowserExecutable(candidatos.find((p) => fs.existsSync(p)) || candidatos[candidatos.length - 1]);
Config.setChromiumOpenGlRenderer('swangle');
// 4 hilos: con 6 el render falló por tiempo de espera.
Config.setConcurrency(4);
// Los gráficos se superponen en CapCut: siempre con alfa (ProRes 4444).
Config.setVideoImageFormat('png');
Config.setPixelFormat('yuva444p10le');
Config.setCodec('prores');
Config.setProResProfile('4444');
