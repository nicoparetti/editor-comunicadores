// Opciones de estilo de gráficos para los tableros (2A "Continuidad" es el de fábrica).
// Cuando elija, sus valores se vuelcan a src/tokens.ts: los gráficos solo leen tokens.
export type Estilo = {
  id: string;
  nombre: string;
  idea: string;
  color: {fondo: string; texto: string; textoSobreVideo: string; metodo: string; acento: string; sobreAcento: string; semantico: string};
  fuente: {display: string; subtitulos: string; tarjetas: string; premium: string | null};
  peso: {display: number; subtitulos: number; tarjetas: number};
  displayMayus: boolean;
  radio: number;
};

export const ESTILOS: Record<string, Estilo> = {
  A: {
    id: 'A',
    nombre: 'Serif Classic',
    idea: 'El sistema de carruseles: serif clásica, bordó y crema, con dorado como acento.',
    color: {fondo: '#1A1411', texto: '#F5EFE3', textoSobreVideo: '#FFFFFF', metodo: '#D4A82B', acento: '#8B1A1A', sobreAcento: '#F5EFE3', semantico: '#8B1A1A'},
    fuente: {display: 'Playfair Display', subtitulos: 'Cal Sans', tarjetas: 'EB Garamond', premium: 'Playfair Display'},
    peso: {display: 700, subtitulos: 600, tarjetas: 500},
    displayMayus: false,
    radio: 6,
  },
  B: {
    id: 'B',
    nombre: 'Continuidad con los subtítulos',
    idea: 'Los gráficos hablan el mismo idioma que tus subtítulos: Cal Sans blanca y Playfair Display itálica crema sobre oscuro cálido.',
    color: {fondo: '#1A1411', texto: '#FFFFFF', textoSobreVideo: '#FFFFFF', metodo: '#F5EFE3', acento: '#F6F6A8', sobreAcento: '#1A1411', semantico: '#C0392B'},
    fuente: {display: 'Cal Sans', subtitulos: 'Cal Sans', tarjetas: 'Cal Sans', premium: 'Playfair Display Italic'},
    peso: {display: 600, subtitulos: 600, tarjetas: 600},
    displayMayus: false,
    radio: 14,
  },
  C: {
    id: 'C',
    nombre: 'Editorial claro',
    idea: 'Tarjetas claras tipo papel sobre la imagen. Más libro o revista que YouTuber.',
    color: {fondo: '#F5EFE3', texto: '#1A1411', textoSobreVideo: '#FFFFFF', metodo: '#8B1A1A', acento: '#D4A82B', sobreAcento: '#1A1411', semantico: '#8B1A1A'},
    fuente: {display: 'EB Garamond', subtitulos: 'Cal Sans', tarjetas: 'EB Garamond', premium: 'Playfair Display Italic'},
    peso: {display: 600, subtitulos: 600, tarjetas: 500},
    displayMayus: false,
    radio: 4,
  },
  '2A': {
    id: '2A',
    nombre: 'Continuidad · tarjetas oscuras + mapa claro (ELEGIDO para el reel de referencia con gráficos, 9/11/2026)',
    idea: 'Cal Sans + Playfair Display Italic crema sobre tarjetas oscuras translúcidas con bordes redondeados; inserts a pantalla completa en papel claro con píldoras oscuras.',
    color: {fondo: '#EFE4CC', texto: '#FFFFFF', textoSobreVideo: '#FFFFFF', metodo: '#F5EFE3', acento: '#F6F6A8', sobreAcento: '#1A1411', semantico: '#8B1A1A'},
    fuente: {display: 'Cal Sans', subtitulos: 'Cal Sans', tarjetas: 'Cal Sans', premium: 'Playfair Display Italic'},
    peso: {display: 600, subtitulos: 600, tarjetas: 600},
    displayMayus: false,
    radio: 26,
  },
  '2B': {
    id: '2B',
    nombre: 'Continuidad · todo claro y translúcido (referencia guardada)',
    idea: 'Mismas fuentes y radios que 2A, con tarjetas crema translúcidas (rgba(246,240,228,.86)) y texto oscuro; acento Playfair Display Italic en dorado oscuro #9A6B12.',
    color: {fondo: '#EFE4CC', texto: '#1A1411', textoSobreVideo: '#FFFFFF', metodo: '#5a4630', acento: '#9A6B12', sobreAcento: '#F6F0E4', semantico: '#8B1A1A'},
    fuente: {display: 'Cal Sans', subtitulos: 'Cal Sans', tarjetas: 'Cal Sans', premium: 'Playfair Display Italic'},
    peso: {display: 600, subtitulos: 600, tarjetas: 600},
    displayMayus: false,
    radio: 26,
  },
};
