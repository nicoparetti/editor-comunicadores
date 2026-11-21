import {Config} from '@remotion/cli/config';
import path from 'node:path';

// Navegador para renderizar: Chromium para Linux arm64 instalado en .herramientas/chromium (preparar_entorno.sh).
Config.setBrowserExecutable(path.join(process.cwd(), '..', '.herramientas', 'chromium', 'bin', 'chromium'));
Config.setChromiumOpenGlRenderer('swangle');
// 4 hilos: con 6 el render falló por tiempo de espera.
Config.setConcurrency(4);
// Los gráficos se superponen en CapCut: siempre con alfa (ProRes 4444).
Config.setVideoImageFormat('png');
Config.setPixelFormat('yuva444p10le');
Config.setCodec('prores');
Config.setProResProfile('4444');
