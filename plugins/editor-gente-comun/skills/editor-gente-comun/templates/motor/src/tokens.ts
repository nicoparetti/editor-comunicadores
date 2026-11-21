// Tokens de diseño: los gráficos solo leen de aquí.
// ESTADO: estilo 2A elegido el 9/11/2026 (reel el reel de referencia con gráficos): Cal Sans + Playfair Display Italic crema, tarjetas oscuras translúcidas,
// radio 26, inserts a pantalla completa en papel claro. 2B (todo claro) queda como referencia en estilos.ts.
// Tableros: 4_Recursos/imagenes/tableros/. Regla de maquetación: aire interno igual arriba y abajo (tarjetas a la
// medida del contenido) y textos de píldoras centrados por altura de mayúsculas, verificados midiendo la tinta.
export const T = {
  color: {
    fondo: '#1A1411',
    texto: '#FFFFFF',
    metodo: '#F5EFE3',
    acento: '#F6F6A8',
    sobreAcento: '#1A1411',
    semantico: '#C0392B',
    tarjeta: 'rgba(20,16,14,0.74)',
    pildora: 'rgba(20,16,14,0.78)',
    papel: '#EFE4CC',
    papelTierra: '#DCCBA6',
    papelTinta: '#5A4630',
    pin: '#8B1A1A',
    borde: 'rgba(255,255,255,0.16)',
    tenue: 'rgba(255,255,255,0.62)',
  },
  fuente: {
    display: '"Cal Sans", sans-serif',
    subtitulos: '"Cal Sans", sans-serif',
    tarjetas: '"Cal Sans", sans-serif',
    complementaria: '"Playfair Display Italic", serif',
    mono: '"Courier Prime", monospace',
  },
  peso: {display: 600, subtitulos: 600, tarjetas: 600},
  displayMayus: false,
  radio: 26,
  // Zonas seguras 16:9 (1920×1080)
  seguro: {arriba: 108, abajo: 130, lado: 96},
  // Zonas seguras 9:16 (1080×1920)
  seguroVertical: {arriba: 220, abajo: 400, derecha: 140},
  sombraTexto: '0 0 28px rgba(0,0,0,0.30)',
  sombraTarjeta: '0 30px 80px rgba(0,0,0,0.55), 0 8px 24px rgba(0,0,0,0.35)',
} as const;

export const W = 1920;
export const H = 1080;
export const WV = 1080;
export const HV = 1920;
