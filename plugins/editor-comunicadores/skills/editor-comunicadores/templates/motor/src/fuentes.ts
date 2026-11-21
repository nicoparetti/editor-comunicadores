import {continueRender, delayRender, staticFile} from 'remotion';

// Fuentes de la persona (copias de 4_Recursos/fuentes en public/fuentes). Los gráficos usan estos nombres de familia.
const FUENTES: {familia: string; archivo: string; estilo?: string; peso?: string}[] = [
  {familia: 'Cal Sans', archivo: 'fuentes/CalSans-SB.ttf', peso: '600'},
  {familia: 'Playfair Display Italic', archivo: 'fuentes/PlayfairDisplay-SemiBoldItalic.ttf', estilo: 'italic'},
  {familia: 'Oswald', archivo: 'fuentes/Oswald-Bold.ttf', peso: '700'},
  {familia: 'Playfair Display', archivo: 'fuentes/PlayfairDisplay-Variable.ttf', peso: '400 900'},
  {familia: 'Playfair Display', archivo: 'fuentes/PlayfairDisplay-Italic-Variable.ttf', estilo: 'italic', peso: '400 900'},
  {familia: 'EB Garamond', archivo: 'fuentes/EBGaramond-Variable.ttf', peso: '400 800'},
  {familia: 'EB Garamond', archivo: 'fuentes/EBGaramond-Italic-Variable.ttf', estilo: 'italic', peso: '400 800'},
  {familia: 'Courier Prime', archivo: 'fuentes/CourierPrime-Regular.ttf'},
];

let cargadas = false;
export const cargarFuentes = () => {
  if (cargadas || typeof document === 'undefined') return;
  cargadas = true;
  const h = delayRender('Cargando fuentes');
  Promise.all(
    FUENTES.map((f) =>
      new FontFace(f.familia, `url(${staticFile(f.archivo)})`, {style: f.estilo ?? 'normal', weight: f.peso ?? '400'}).load().then((ff) => document.fonts.add(ff)),
    ),
  )
    .then(() => continueRender(h))
    .catch((e) => { console.error(e); continueRender(h); });
};
